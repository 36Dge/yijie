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
WID = '7685061713409867776'
EXPECTED_MANIFEST = '725750097a463c3dc3a323b04c8b22e3650bfdc27ace60453f1c93ce2d00810c'
EXPECTED_SOURCE = '236d36286e96b4f7ad7fe5bb874528c67505c0835020b238cfe21179263bb120'

def main():
    stage = sys.argv[1] if len(sys.argv) == 2 else ''
    r.c.require(stage in ['saved-draft26', 'final-runs26', 'final-workflow26', 'after-normal-restart26'], 'Explicit snapshot stage required')
    destination = HERE / (stage + '.json')
    r.c.require(not destination.exists(), 'New evidence file required')
    activation = json.loads((HERE / 'activation-26.json').read_text())
    r.c.require(activation['manifest_sha256'] == EXPECTED_MANIFEST and activation['source_digest'] == EXPECTED_SOURCE, 'Expected canonical 26 activation differs')
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
        path = '/v1/workflows/' + WID
        legacy = r.read_api(path, credentials)
        workflow = r.read_api(path, credentials, True)
        r.c.require(workflow['workflow_id'] == legacy['workflow_id'] == WID, 'Exact workflow binding differs')
        r.c.require('description' not in legacy and legacy == {key: value for key, value in workflow.items() if key != 'description'}, 'Metadata projection differs')
        graph = json.loads(workflow['canvas'])
        r.c.require(len(graph['nodes']) == 3 and len(graph['edges']) == 2, 'Expected three-node/two-edge draft differs')
        text_nodes = [node for node in graph['nodes'] if str(node['type']) == '15']
        r.c.require(len(text_nodes) == 1, 'Expected text node is not unique')
        parameters = text_nodes[0]['data']['inputs']['concatParams']
        values = [item['input']['value']['content'] for item in parameters if item['name'] == 'concatResult']
        r.c.require(values == ['易界主题：{{input}}'], 'Exact synthetic text prefix differs')
        history = r.read_api(path + '/runs?limit=20', credentials)
        r.c.require(len(history['items']) <= 20 and not history.get('next_cursor'), 'History exceeded the bounded snapshot')
        runs = []
        for row in history['items']:
            rid = row['run_id']
            r.c.require(r.re.fullmatch('[1-9][0-9]{0,18}', rid), 'Run ID shape differs')
            run = r.read_api(path + '/runs/' + rid, credentials)
            r.c.require(run['workflow_id'] == WID and run['run_id'] == rid, 'Run binding differs')
            runs.append(run)
        mysql_sql = r.MYSQL_SQL.replace(','.join(r.IDS), WID).replace(r.SYNTHETIC, WID)
        postgres_sql = r.PG_SQL.replace("'" + r.OLD + "','" + r.SYNTHETIC + "'", "'" + WID + "'").replace(r.SYNTHETIC, WID)
        r.c.require(all(old not in mysql_sql + postgres_sql for old in r.IDS), 'A previous workflow ID remains in SELECT scope')
        mysql = r.db_query(selected['coze-workflow-mysql'], mysql_sql, True)
        postgres = r.db_query(selected['workflow-postgres'], postgres_sql, False)
        r.c.require(mysql['facts']['snapshot'][0]['database'] == 'coze_workflow_local' and postgres['facts']['snapshot'][0]['database'] == 'yijie_workflow_local', 'Database identity differs')
        r.c.require(len(mysql['facts']['resource']) == len(postgres['facts']['resource']) == 1, 'Exact scoped database resource is not unique')
        row, pg_row = mysql['facts']['resource'][0], postgres['facts']['resource'][0]
        r.c.require(all(row[key] == workflow[key] for key in ['workflow_id', 'name', 'description', 'revision']), 'API/MySQL draft metadata differs')
        r.c.require(row['canvas_sha256'] == r.digest(workflow['canvas']) and row['canvas_bytes'] == len(workflow['canvas'].encode()), 'API/MySQL UTF-8 canvas bytes differ')
        r.c.require(row['principal_scope'] == r.SCOPE and row['creator_id'] == pg_row['coze_user_id'] and row['space_id'] == pg_row['coze_space_id'], 'Cross-database ownership differs')
        pg_ops = {item['operation_id']: item for item in postgres['facts'].get('operation', [])}
        my_ops = {item['operation_id']: item for item in mysql['facts'].get('operation', [])}
        comparisons = []
        for oid in sorted(pg_ops.keys() & my_ops.keys()):
            left, right = pg_ops[oid]['receipt'], my_ops[oid]['receipt']
            fields = ['operation_id', 'kind', 'phase', 'workflow_id', 'revision', 'version', 'run_id']
            comparisons.append({'operation_id': oid, 'match': all(left.get(key) == right.get(key) for key in fields)})
        r.c.require(all(item['match'] for item in comparisons), 'Shared operation receipts differ')
        r.c.require(r.c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during read')
        result = {'schema_version': 1, 'recorded_at': r.now(), 'stage': stage, 'workflow_id': WID, 'run_epoch': state['run_epoch'], 'manifest_sha256': EXPECTED_MANIFEST, 'source_digest': EXPECTED_SOURCE, 'scope': 'Only this exact root-created synthetic workflow. GET + SELECT only; API reads may append successful read audits.', 'legacy': legacy, 'workflow': workflow, 'canvas_sha256': r.digest(workflow['canvas']), 'canvas_bytes': len(workflow['canvas'].encode()), 'node_summary': [{'id': node['id'], 'type': node['type'], 'position': node.get('meta', {}).get('position')} for node in graph['nodes']], 'edges': graph['edges'], 'history': history, 'runs': runs, 'mysql': mysql, 'postgres': postgres, 'cross_database': {'ownership_match': True, 'draft_metadata_match': True, 'canvas_utf8_bytes_and_sha256_match': True, 'updated_at_matches_at_observation': row['updated_at_ms'] == workflow['updated_at_ms'], 'shared_receipts': comparisons, 'postgres_only_operations': sorted(pg_ops.keys() - my_ops.keys()), 'mysql_only_operations': sorted(my_ops.keys() - pg_ops.keys())}, 'limits': 'Independent GET/SELECT snapshots; not a cross-database atomic snapshot, UI/theme/Undo qualification, session revocation evidence or D4 claim. Root may continue test/publication after this observation.', 'script_sha256': r.digest(Path(__file__).read_bytes()), 'helper_sha256': r.digest(HELPER.read_bytes())}
        raw = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        for file in ['k-na.json', 'k-ac.json']:
            r.c.require(json.loads(r.c.secure_read(r.c.PRIVATE / file))['token'] not in raw, 'Secret exposure detected; evidence not written')
        with destination.open('x') as output:
            output.write(raw)
        print(json.dumps({'completed': True, 'stage': stage, 'workflow_id': WID, 'name': workflow['name'], 'revision': workflow['revision'], 'nodes': len(graph['nodes']), 'edges': len(graph['edges']), 'runs': len(runs), 'api_mysql_canvas_match': True, 'cross_database_ownership_match': True, 'shared_receipts_match': True, 'evidence': str(destination)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('READBACK STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, r.c.WorkflowError) else '') + '; credentials and raw connection output withheld')
        raise SystemExit(1)
