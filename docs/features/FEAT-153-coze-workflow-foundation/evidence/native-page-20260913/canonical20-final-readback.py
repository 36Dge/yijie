"""Fixed canonical 20 workflow: GET and SELECT only, before/after normal restart."""
from pathlib import Path
import fcntl
import importlib.util
import json
import os
import stat
import sys

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('canonical20_reader', HERE / 'canonical20-readback.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
WID = '7685031373442121728'
EXPECTED = {
    '7685032443987886080': {'mode': 'debug', 'input': '页面终验', 'output': '原生终验：页面终验'},
    '7685032637395632128': {'mode': 'release', 'input': '版本终验', 'output': '原生终验：版本终验'},
}

def main():
    phase = sys.argv[1] if len(sys.argv) == 2 else ''
    r.c.require(phase in ['before-normal-restart', 'after-normal-restart'], 'Explicit before/after observation required')
    destination = HERE / ('canonical20-final-' + phase + '.json')
    r.c.require(not destination.exists(), 'New evidence file required')
    fd = os.open(r.c.GENERATED / 'controller.lock', os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as lock:
        info = os.fstat(lock.fileno())
        r.c.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o600, 'Controller lock differs')
        fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        state = r.c.read_state()
        expected_epoch = '28a9b428-3eed-4b0e-ae96-5d1dc2001b92' if phase == 'before-normal-restart' else 'b13e0089-5888-43ac-b25b-0440956373ea'
        r.c.require(state['phase'] == 'ready' and state['run_epoch'] == expected_epoch, 'Expected canonical 20 epoch differs')
        credentials = json.loads(r.c.secure_read(r.c.PRIVATE / 'k-na.json'))
        r.c.require(credentials['run_epoch'] == state['run_epoch'], 'Credential epoch differs')
        items = r.c.all_containers()
        r.c.validate_owned(items, state)
        selected = {}
        network_name = r.c.PROJECT + '_workflow-private'
        network = json.loads(r.c.output(['network', 'inspect', network_name]))
        r.c.require(len(network) == 1 and network[0]['Internal'] is True, 'Dedicated private network differs')
        for service, password_file in [('workflow-postgres', 'postgres-password'), ('coze-workflow-mysql', 'mysql-password')]:
            matches = [i for i in items if i['labels'].get('com.docker.compose.service') == service and i['state']['Running'] and i['health'] == 'healthy']
            r.c.require(len(matches) == 1 and matches[0]['image_id'] == r.c.expected_image(service, state), 'Expected healthy database differs')
            item = matches[0]
            attached = json.loads(r.c.output(['inspect', '--format', '{{json .NetworkSettings.Networks}}', item['id']]))
            r.c.require(set(attached) == {network_name}, 'Database private network differs')
            password_path = str(r.c.PRIVATE / password_file)
            r.c.require(any(m['type'] == 'bind' and m['source'] in [password_path, '/host_mnt' + password_path] and m['target'] == '/run/private/' + password_file and not m['rw'] for m in item['mounts']), 'Read-only credential mount differs')
            selected[service] = item
        path = '/v1/workflows/' + WID
        workflow = r.read_api(path, credentials, True)
        baseline = json.loads((HERE / 'native20-saved.json').read_text())['metadata']
        r.c.require(all(workflow[k] == baseline[k] for k in ['workflow_id', 'name', 'description', 'canvas', 'revision']), 'First saved draft fields differ')
        r.c.require(workflow['published_version'] == 'v0.0.1', 'Expected published version differs')
        history = r.read_api(path + '/runs?limit=20', credentials)
        r.c.require({item['run_id'] for item in history['items']} == set(EXPECTED) and not history.get('next_cursor'), 'Exact known run history differs')
        runs = [r.read_api(path + '/runs/' + rid, credentials) for rid in sorted(EXPECTED)]
        for run in runs:
            expected = EXPECTED[run['run_id']]
            r.c.require(run['workflow_id'] == WID and run['revision'] == workflow['revision'] and run['terminal'] and run['state'] == 'succeeded', 'Terminal run binding/state differs')
            r.c.require(run['mode'] == expected['mode'] and run['input']['input'] == expected['input'] and run['output'] == expected['output'], 'Exact successful run input/output differs')
        mysql_sql = r.MYSQL_SQL.replace(','.join(r.IDS), WID).replace(r.SYNTHETIC, WID)
        pg_sql = r.PG_SQL.replace("'" + r.OLD + "','" + r.SYNTHETIC + "'", "'" + WID + "'").replace(r.SYNTHETIC, WID)
        mysql = r.db_query(selected['coze-workflow-mysql'], mysql_sql, True)
        postgres = r.db_query(selected['workflow-postgres'], pg_sql, False)
        r.c.require(mysql['facts']['snapshot'][0]['database'] == 'coze_workflow_local' and postgres['facts']['snapshot'][0]['database'] == 'yijie_workflow_local', 'Database identity differs')
        r.c.require(len(mysql['facts']['resource']) == len(postgres['facts']['resource']) == 1, 'Exact resource not unique')
        row, pg_row = mysql['facts']['resource'][0], postgres['facts']['resource'][0]
        r.c.require(all(row[k] == workflow[k] for k in ['workflow_id', 'name', 'description', 'revision', 'updated_at_ms']), 'API/MySQL resource mismatch')
        r.c.require(row['canvas_sha256'] == r.digest(workflow['canvas']) and row['canvas_bytes'] == len(workflow['canvas'].encode()), 'API/MySQL canvas bytes differ')
        r.c.require(row['principal_scope'] == r.SCOPE and row['creator_id'] == pg_row['coze_user_id'] and row['space_id'] == pg_row['coze_space_id'], 'Cross-database ownership differs')
        versions = mysql['facts']['version']
        r.c.require(len(versions) == 1 and versions[0]['version'] == 'v0.0.1' and versions[0]['revision'] == workflow['revision'] and versions[0]['canvas_sha256'] == row['canvas_sha256'], 'Published canvas/revision differs')
        executions = {run['run_id']: run for run in mysql['facts']['execution']}
        r.c.require(set(executions) == set(EXPECTED), 'Database run set differs')
        for rid, expected in EXPECTED.items():
            run = executions[rid]
            r.c.require(run['status'] == 2 and run['revision'] == workflow['revision'], 'Database terminal run state differs')
            r.c.require(json.loads(run['input'])['input'] == expected['input'] and json.loads(run['output'])['result'] == expected['output'], 'Exact persisted run input/output differs')
        pg_ops = {row['operation_id']: row for row in postgres['facts'].get('operation', [])}
        my_ops = {row['operation_id']: row for row in mysql['facts'].get('operation', [])}
        compared = []
        for oid in sorted(pg_ops.keys() & my_ops.keys()):
            left, right = pg_ops[oid]['receipt'], my_ops[oid]['receipt']
            fields = ['operation_id', 'kind', 'phase', 'workflow_id', 'revision', 'version', 'run_id']
            compared.append({'operation_id': oid, 'match': all(left.get(k) == right.get(k) for k in fields)})
        r.c.require(all(row['match'] for row in compared), 'Shared operation receipts differ')
        activation_file = HERE / ('activation-20-verification.json' if phase == 'before-normal-restart' else 'activation-20-restart-verification.json')
        csp_activation = json.loads(activation_file.read_text())
        result = {'schema_version': 1, 'recorded_at': r.now(), 'phase': phase, 'run_epoch': state['run_epoch'], 'workflow_id': WID, 'scope': 'Exact root-created canonical 20 workflow; GET + SELECT only, no runtime mutation', 'manifest_sha256': csp_activation['manifest_sha256'], 'source_digest': csp_activation['source_digest'], 'workflow': workflow, 'canvas_sha256': r.digest(workflow['canvas']), 'history': history, 'runs': runs, 'mysql': mysql, 'postgres': postgres, 'cross_database': {'ownership_match': True, 'canvas_utf8_bytes_sha256_match': True, 'version_canvas_revision_match': True, 'exact_expected_runs_match': True, 'shared_receipts': compared, 'postgres_only_operations': sorted(pg_ops.keys() - my_ops.keys()), 'mysql_only_operations': sorted(my_ops.keys() - pg_ops.keys())}, 'limits': 'Does not operate or independently qualify actual UI, native Undo/Redo, session revocation, dev or unified D4. SQL is independent ordinary SELECT snapshots.', 'script_sha256': r.digest(Path(__file__).read_bytes()), 'helper_sha256': r.digest((HERE / 'canonical20-readback.py').read_bytes())}
        if phase == 'after-normal-restart':
            before_file = HERE / 'canonical20-final-before-normal-restart.json'
            before = json.loads(before_file.read_text())
            checks = {key: result[key] == before[key] for key in ['manifest_sha256', 'source_digest', 'workflow', 'canvas_sha256', 'history', 'runs']}
            for engine in ['mysql', 'postgres']:
                left = {key: value for key, value in result[engine]['facts'].items() if key not in ['snapshot', 'audit']}
                right = {key: value for key, value in before[engine]['facts'].items() if key not in ['snapshot', 'audit']}
                checks[engine + '_persistent_rows'] = left == right
            old_audit = before['postgres']['facts'].get('audit', [])
            new_audit = result['postgres']['facts'].get('audit', [])
            appended = new_audit[len(old_audit):]
            checks['existing_audit_rows_preserved'] = new_audit[:len(old_audit)] == old_audit
            checks['appended_audit_rows_only_successful_reads'] = all(row['action'] in ['read', 'bootstrap', 'history', 'read_run'] and row['outcome_code'] == 'success' for row in appended)
            r.c.require(all(checks.values()), 'Before/after restart data differs')
            result['normal_restart_comparison'] = {'checks': checks, 'baseline_sha256': r.digest(before_file.read_bytes()), 'previous_run_epoch': before['run_epoch'], 'new_run_epoch': state['run_epoch'], 'activation_evidence': activation_file.name, 'activation_sha256': r.digest(activation_file.read_bytes()), 'audit_note': 'Normal App/API reads append service audit entries. Existing audit rows must remain identical and appended rows must contain only successful read/bootstrap/history/read_run actions; business resource/operation/version/execution rows are compared exactly.', 'appended_successful_read_audit_rows': len(appended)}
        r.c.require(r.c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during read')
        raw = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        for file in ['k-na.json', 'k-ac.json']:
            r.c.require(json.loads(r.c.secure_read(r.c.PRIVATE / file))['token'] not in raw, 'Secret exposure detected; evidence not written')
        with destination.open('x') as out:
            out.write(raw)
        print(json.dumps({'completed': True, 'phase': phase, 'workflow_id': WID, 'revision': workflow['revision'], 'published_version': workflow['published_version'], 'runs': len(runs), 'api_mysql_exact_outputs_match': True, 'cross_database_receipts_match': True, 'evidence': str(destination)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('READBACK STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, r.c.WorkflowError) else '') + '; raw connection output and credentials withheld')
        raise SystemExit(1)
