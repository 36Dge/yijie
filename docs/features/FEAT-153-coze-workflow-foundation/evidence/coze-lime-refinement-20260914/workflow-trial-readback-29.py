"""Fixed UI-created theme workflow, GET/SELECT snapshots; no business writes or UI."""
from pathlib import Path
import fcntl
import importlib.util
import json
import os
import stat
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
HELPER = HERE.parent / 'native-page-20260913/canonical20-readback.py'
spec = importlib.util.spec_from_file_location('fixed_workflow_reader', HELPER)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
WID = '7685078769316397056'
EXPECTED_MANIFEST = '2a2fa3d5ac83d50994970b8ba62077f7743366aab8b683da171761e06e0b2a44'
EXPECTED_SOURCE = '8ccbc99c0529a85dc93e9694d53b1b51e9c441bd54af52c5fc19cd4ea052a689'

def main():
    stage = 'final29-after-trial'
    destination = HERE / (stage + '.json')
    r.c.require(not destination.exists(), 'New evidence file required')
    activation = json.loads((HERE / 'activation29.json').read_text())
    r.c.require(activation['manifest_sha256'] == EXPECTED_MANIFEST and activation['source_digest'] == EXPECTED_SOURCE, 'Expected canonical 29 activation differs')
    fd = os.open(r.c.GENERATED / 'controller.lock', os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as lock:
        info = os.fstat(lock.fileno())
        r.c.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o600, 'Controller lock identity differs')
        fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        state = r.c.read_state()
        r.c.require(state['phase'] == 'ready', 'Controlled stack is not ready')
        credentials = json.loads(r.c.secure_read(r.c.PRIVATE / 'k-na.json'))
        r.c.require(credentials['run_epoch'] == state['run_epoch'], 'Credential epoch differs')
        items = r.c.all_containers()
        r.c.validate_owned(items, state)
        selected = {}
        network_name = r.c.PROJECT + '_workflow-private'
        network = json.loads(r.c.output(['network', 'inspect', network_name]))
        r.c.require(len(network) == 1 and network[0]['Internal'] is True, 'Private network identity differs')
        for service, password_file in [('workflow-postgres', 'postgres-password'), ('coze-workflow-mysql', 'mysql-password')]:
            matches = [item for item in items if item['labels'].get('com.docker.compose.service') == service and item['state']['Running'] and item['health'] == 'healthy']
            r.c.require(len(matches) == 1 and matches[0]['image_id'] == r.c.expected_image(service, state), 'Expected healthy database differs')
            item = matches[0]
            attached = json.loads(r.c.output(['inspect', '--format', '{{json .NetworkSettings.Networks}}', item['id']]))
            r.c.require(set(attached) == {network_name}, 'Database network differs')
            password_path = str(r.c.PRIVATE / password_file)
            r.c.require(any(m['type'] == 'bind' and m['source'] in [password_path, '/host_mnt' + password_path] and m['target'] == '/run/private/' + password_file and not m['rw'] for m in item['mounts']), 'Read-only mounted credential differs')
            selected[service] = item
        before = json.loads((HERE / 'final29.json').read_text())
        expected_revision = '7685082330511179776'
        r.c.require(before['workflow_id'] == WID and before['workflow']['revision'] == expected_revision, 'Expected current draft baseline differs')
        path = '/v1/workflows/' + WID
        workflow = r.read_api(path, credentials, True)
        r.c.require(workflow['workflow_id'] == WID, 'Exact workflow binding differs')
        history = r.read_api(path + '/runs?limit=20', credentials)
        r.c.require(len(history['items']) <= 20 and not history.get('next_cursor'), 'History exceeded bounded observation')
        previous_runs = {row['run_id']: row for row in before['history']['items']}
        new_runs = [row for row in history['items'] if row['run_id'] not in previous_runs]
        r.c.require(len(new_runs) == 1, 'Expected exactly one new trial')
        run_id = new_runs[0]['run_id']
        r.c.require(r.re.fullmatch('[1-9][0-9]{0,18}', run_id), 'Run ID shape differs')
        run = r.read_api(path + '/runs/' + run_id, credentials)
        operation_id = run['operation_id']
        r.c.require(run['workflow_id'] == WID and run['run_id'] == run_id and r.re.fullmatch('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', operation_id), 'New run binding differs')
        old_flows = []
        for old_id in ['7685061713409867776', '7685031373442121728']:
            old_path = '/v1/workflows/' + old_id
            legacy = r.read_api(old_path, credentials)
            metadata = r.read_api(old_path, credentials, True)
            r.c.require(legacy['workflow_id'] == metadata['workflow_id'] == old_id, 'Old workflow identity differs')
            baseline_name = 'workflow-' + old_id + '-after-ui29.json'
            baseline = json.loads((HERE / baseline_name).read_text())
            old_flows.append({'workflow_id': old_id, 'baseline_file': baseline_name, 'baseline_sha256': r.digest((HERE / baseline_name).read_bytes()), 'legacy': legacy, 'metadata': metadata, 'legacy_complete_equal': legacy == baseline['legacy'], 'metadata_complete_equal': metadata == baseline['metadata']})
        mysql_parts = [part.strip() for part in r.MYSQL_SQL.split(';') if part.strip()]
        mysql_parts = [part for part in mysql_parts if any("SELECT '" + section + "'," in part for section in ['snapshot','resource','execution','operation'])]
        mysql_sql = ';'.join(mysql_parts) + ';'
        mysql_sql = mysql_sql.replace(','.join(r.IDS), WID).replace(r.SYNTHETIC, WID)
        mysql_sql = mysql_sql.replace('WHERE workflow_id=' + WID + ' ORDER BY id', 'WHERE workflow_id=' + WID + ' AND id=' + run_id + ' ORDER BY id')
        mysql_sql = mysql_sql.replace('AND workflow_id=' + WID + ' ORDER BY created_at,operation_id', 'AND workflow_id=' + WID + " AND operation_id='" + operation_id + "' ORDER BY created_at,operation_id")
        pg_parts = [part.strip() for part in r.PG_SQL.split(';') if part.strip()]
        pg_parts = [part for part in pg_parts if any("'section','" + section + "'" in part for section in ['snapshot','operation'])]
        postgres_sql = (';'.join(pg_parts) + ';').replace(r.SYNTHETIC, WID)
        postgres_sql = postgres_sql.replace("AND workflow_id='" + WID + "' ORDER BY created_at,operation_id", "AND workflow_id='" + WID + "' AND operation_id='" + operation_id + "' ORDER BY created_at,operation_id")
        r.c.require(all(old not in mysql_sql + postgres_sql for old in r.IDS), 'Previous helper workflow remains in SQL scope')
        r.c.require(' AND id=' + run_id in mysql_sql and mysql_sql.count(operation_id) == 1 and postgres_sql.count(operation_id) == 1, 'Exact new run/operation SQL scope differs')
        mysql = r.db_query(selected['coze-workflow-mysql'], mysql_sql, True)
        postgres = r.db_query(selected['workflow-postgres'], postgres_sql, False)
        r.c.require(mysql['facts']['snapshot'][0]['database'] == 'coze_workflow_local' and postgres['facts']['snapshot'][0]['database'] == 'yijie_workflow_local', 'Database identity differs')
        r.c.require(len(mysql['facts']['resource']) == len(mysql['facts']['execution']) == len(mysql['facts']['operation']) == len(postgres['facts']['operation']) == 1, 'Exact resource/run/receipt is not unique')
        resource = mysql['facts']['resource'][0]
        execution = mysql['facts']['execution'][0]
        my_receipt = mysql['facts']['operation'][0]['receipt']
        pg_receipt = postgres['facts']['operation'][0]['receipt']
        r.c.require(resource['workflow_id'] == execution['workflow_id'] == WID and execution['run_id'] == run_id and my_receipt['operation_id'] == pg_receipt['operation_id'] == operation_id, 'Database record binding differs')
        checks = {
          'draft_canvas_name_description_revision_unchanged': all(workflow.get(k) == before['workflow'].get(k) for k in ['canvas','name','description','revision']),
          'latest_revision_is_expected': workflow['revision'] == expected_revision,
          'trial_uses_latest_revision': run['revision'] == execution['revision'] == workflow['revision'],
          'api_trial_success': run['state'] == 'succeeded' and run['terminal'] is True and run['mode'] == 'debug',
          'api_trial_input_output': run['input'] == {'input':'最终青柠复验'} and run['output'] == '轻盈青柠：最终青柠复验',
          'mysql_trial_success': execution['status'] == 2 and execution['mode'] == 1 and execution['error_code'] == '',
          'mysql_trial_input_output': json.loads(execution['input']) == {'input':'最终青柠复验'} and json.loads(execution['output']) == {'result':'轻盈青柠：最终青柠复验'},
          'mysql_draft_metadata_matches_api': all(resource[k] == workflow[k] for k in ['workflow_id','name','description','revision']),
          'mysql_canvas_matches_api': resource['canvas_sha256'] == r.digest(workflow['canvas']) and resource['canvas_bytes'] == len(workflow['canvas'].encode()),
          'both_database_receipts_equal': my_receipt == pg_receipt,
          'receipt_completed_and_bound': my_receipt.get('phase') == 'completed' and my_receipt.get('kind') == 'test' and my_receipt.get('workflow_id') == WID and my_receipt.get('revision') == expected_revision and my_receipt.get('run_id') == run_id,
          'previous_history_items_preserved': all(next((row for row in history['items'] if row['run_id'] == rid), None) == item for rid,item in previous_runs.items()),
          'old_two_workflow_full_responses_preserved': all(row['legacy_complete_equal'] and row['metadata_complete_equal'] for row in old_flows),
        }
        r.c.require(r.c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during reads')
        result = {'schema_version':1, 'recorded_at':r.now(), 'stage':stage, 'workflow_id':WID, 'run_epoch':state['run_epoch'], 'manifest_sha256':EXPECTED_MANIFEST, 'source_digest':EXPECTED_SOURCE, 'baseline_file':'final29.json', 'baseline_sha256':r.digest((HERE / 'final29.json').read_bytes()), 'workflow':workflow, 'canvas_sha256':r.digest(workflow['canvas']), 'workflow_response_changed_keys':[k for k in sorted(before['workflow'].keys() | workflow.keys()) if before['workflow'].get(k) != workflow.get(k)], 'history':history, 'run':run, 'mysql':mysql, 'postgres':postgres, 'old_workflows':old_flows, 'checks':checks, 'all_checks_pass':all(checks.values()), 'scope':'One new trial and its exact operation receipt, synthetic draft plus two fixed old workflow projections. API GET and database SELECT only. No audit SELECT or whole-database equality check; normal read audits may append.', 'limits':'Independent observations, not an atomic database snapshot or UI/dev/D4 claim. Observer made no business mutation and infers no save actor.', 'script_sha256':r.digest(Path(__file__).read_bytes()), 'helper_sha256':r.digest(HELPER.read_bytes())}
        raw = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        for secret_file in ['k-na.json','k-ac.json']:
            r.c.require(json.loads(r.c.secure_read(r.c.PRIVATE / secret_file))['token'] not in raw, 'Credential exposure detected; evidence not written')
        with destination.open('x') as output:
            output.write(raw)
        print(json.dumps({'completed':True,'all_checks_pass':result['all_checks_pass'],'failed_checks':[k for k,v in checks.items() if not v],'run_id':run_id,'revision':run['revision'],'evidence':str(destination)},ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('TRIAL READBACK STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, r.c.WorkflowError) else '') + '; raw connection output and credentials withheld')
        raise SystemExit(1)
