"""GET + SELECT snapshot of the exact canonical 20 UI-created workflow."""
from pathlib import Path
import fcntl
import importlib.util
import json
import os
import stat

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('canonical20_reader', HERE / 'canonical20-readback.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
WID = '7685031373442121728'
DEST = HERE / 'canonical20-first-save-db-readback.json'

def main():
    r.c.require(not DEST.exists(), 'New evidence file required')
    fd = os.open(r.c.GENERATED / 'controller.lock', os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as lock:
        info = os.fstat(lock.fileno())
        r.c.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o600, 'Controller lock differs')
        fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        state = r.c.read_state()
        r.c.require(state['phase'] == 'ready' and state['run_epoch'].startswith('28a9b428-'), 'Expected canonical 20 epoch differs')
        credentials = json.loads(r.c.secure_read(r.c.PRIVATE / 'k-na.json'))
        r.c.require(credentials['run_epoch'] == state['run_epoch'], 'Credential epoch differs')
        items = r.c.all_containers()
        r.c.validate_owned(items, state)
        matches = [i for i in items if i['labels'].get('com.docker.compose.service') == 'coze-workflow-mysql' and i['state']['Running'] and i['health'] == 'healthy']
        r.c.require(len(matches) == 1 and matches[0]['image_id'] == r.c.expected_image('coze-workflow-mysql', state), 'Expected healthy MySQL differs')
        item = matches[0]
        network_name = r.c.PROJECT + '_workflow-private'
        network = json.loads(r.c.output(['network', 'inspect', network_name]))
        attached = json.loads(r.c.output(['inspect', '--format', '{{json .NetworkSettings.Networks}}', item['id']]))
        r.c.require(len(network) == 1 and network[0]['Internal'] is True and set(attached) == {network_name}, 'Dedicated private network differs')
        password_path = str(r.c.PRIVATE / 'mysql-password')
        r.c.require(any(m['type'] == 'bind' and m['source'] in [password_path, '/host_mnt' + password_path] and m['target'] == '/run/private/mysql-password' and not m['rw'] for m in item['mounts']), 'Read-only mounted credential differs')
        actual = r.read_api('/v1/workflows/' + WID, credentials, True)
        baseline = json.loads((HERE / 'native20-saved.json').read_text())
        baseline = baseline['metadata']
        fields = ['workflow_id', 'canvas', 'name', 'description', 'revision']
        r.c.require(all(actual[k] == baseline[k] for k in fields), 'First saved fields changed before observation')
        resource_sql = next(part for part in r.MYSQL_SQL.split(';') if "SELECT 'resource'" in part).replace(','.join(r.IDS), WID) + ';'
        mysql = r.db_query(item, resource_sql, True)
        rows = mysql['facts'].get('resource', [])
        r.c.require(len(rows) == 1 and rows[0]['workflow_id'] == WID, 'Exact scoped resource is not unique')
        row = rows[0]
        r.c.require(all(row[k] == actual[k] for k in ['name', 'description', 'revision', 'updated_at_ms']), 'API and MySQL fields differ during observation')
        r.c.require(row['canvas_sha256'] == r.digest(actual['canvas']) and row['canvas_bytes'] == len(actual['canvas'].encode()), 'API and MySQL canvas bytes differ')
        graph = json.loads(actual['canvas'])
        r.c.require(len(graph['nodes']) == 3 and len(graph['edges']) == 2 and '原生终验：{{input}}' in actual['canvas'], 'Expected three-node synthetic draft differs')
        r.c.require(r.c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during read')
        result = {'schema_version': 1, 'recorded_at': r.now(), 'run_epoch': state['run_epoch'], 'workflow_id': WID, 'scope': 'Exact root-created canonical 20 synthetic resource; no UI, writes or lifecycle operations', 'api': actual, 'mysql': mysql, 'first_saved_fields_match': fields, 'canvas_utf8_sha256_match': True, 'canvas_utf8_bytes_match': True, 'first_save_baseline_sha256': r.digest((HERE / 'native20-saved.json').read_bytes()), 'limits': 'Snapshot verifies persistence only. First-save panel preservation, native Undo/Redo, themes and Chat must use separate actual UI evidence. UI may continue publication after this observation.', 'script_sha256': r.digest(Path(__file__).read_bytes()), 'helper_sha256': r.digest((HERE / 'canonical20-readback.py').read_bytes())}
        raw = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        for file in ['k-na.json', 'k-ac.json']:
            r.c.require(json.loads(r.c.secure_read(r.c.PRIVATE / file))['token'] not in raw, 'Secret exposure detected; evidence not written')
        with DEST.open('x') as out:
            out.write(raw)
        print(json.dumps({'completed': True, 'workflow_id': WID, 'revision': actual['revision'], 'node_count': len(graph['nodes']), 'edge_count': len(graph['edges']), 'first_saved_canvas_match': True, 'api_mysql_match': True, 'evidence': str(DEST)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('READBACK STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, r.c.WorkflowError) else '') + '; raw connection output and credentials withheld')
        raise SystemExit(1)
