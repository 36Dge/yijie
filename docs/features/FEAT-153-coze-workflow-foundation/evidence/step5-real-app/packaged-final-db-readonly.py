"""One fixed synthetic App resource, normal read-only DB snapshots, no service lifecycle."""
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
from datetime import datetime, timezone

ROOT = Path('/Users/jack/Downloads/Personal_Info/CrossBSD')
WID = '7684605114128007168'
EPOCH = 'bdc6b8e8-0314-4a7d-9e33-f0ea4902c54a'
SCOPE = '12500000-0000-4000-8000-000000000001:12500000-0000-4000-8000-100000000001'
DEST = Path(__file__).with_suffix('.json')
spec = importlib.util.spec_from_file_location('workflow_controller', ROOT / 'yijie-infra/scripts/workflow-local.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

def now():
    return datetime.now(timezone.utc).isoformat()

MYSQL_SQL = f"""START TRANSACTION WITH CONSISTENT SNAPSHOT, READ ONLY;
SELECT 'snapshot', JSON_OBJECT('database',DATABASE(),'observed_at',CAST(UTC_TIMESTAMP(6) AS CHAR),'session_default_read_only',@@transaction_read_only);
SELECT 'resource', JSON_OBJECT('workflow_id',CAST(m.id AS CHAR),'name',m.name,'space_id',CAST(m.space_id AS CHAR),'creator_id',CAST(m.creator_id AS CHAR),'app_id',CAST(m.app_id AS CHAR),'latest_version',m.latest_version,'revision',d.commit_id,'updated_at_ms',d.updated_at,'modified',d.modified,'test_run_success',d.test_run_success,'canvas',d.canvas,'server_canvas_bytes',OCTET_LENGTH(d.canvas),'server_canvas_sha256',SHA2(d.canvas,256),'principal_scope',p.scope_key) FROM workflow_meta m JOIN workflow_draft d ON d.id=m.id JOIN yijie_workflow_local_principal p ON p.user_id=m.creator_id AND p.space_id=m.space_id WHERE m.id={WID} AND m.app_id=0 AND m.deleted_at IS NULL AND d.deleted_at IS NULL AND p.scope_key='{SCOPE}';
SELECT 'operation', JSON_OBJECT('operation_id',operation_id,'kind',kind,'workflow_id',CAST(workflow_id AS CHAR),'run_id',CAST(run_id AS CHAR),'run_epoch',run_epoch,'created_at_ms',created_at,'receipt',CAST(receipt AS JSON)) FROM yijie_workflow_local_operation WHERE scope_key='{SCOPE}' AND workflow_id={WID} ORDER BY created_at,operation_id;
SELECT 'counts', JSON_OBJECT('versions',(SELECT COUNT(*) FROM workflow_version WHERE workflow_id={WID} AND deleted_at IS NULL),'executions',(SELECT COUNT(*) FROM workflow_execution WHERE workflow_id={WID}));
COMMIT;
"""
PG_SQL = f"""BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT json_build_object('section','snapshot','database',current_database(),'observed_at',clock_timestamp(),'read_only',current_setting('transaction_read_only'));
SELECT json_build_object('section','resource','workflow_id',r.workflow_id,'scope_key',r.scope_key,'created_at',r.created_at,'owner_user_id',s.owner_user_id::text,'tenant_id',s.tenant_id::text,'coze_user_id',s.coze_user_id,'coze_space_id',s.coze_space_id) FROM workflow_resources r JOIN workflow_scope_bindings s USING(scope_key) WHERE r.scope_key='feat-153-local-v1' AND r.workflow_id='{WID}';
SELECT json_build_object('section','operation','operation_id',operation_id::text,'kind',kind,'phase',phase,'workflow_id',workflow_id,'created_at',created_at,'updated_at',updated_at,'receipt',jsonb_strip_nulls(jsonb_build_object('operation_id',receipt->>'OperationID','kind',receipt->>'Kind','phase',receipt->>'Phase','workflow_id',NULLIF(receipt->>'WorkflowID',''),'revision',NULLIF(receipt->>'Revision',''),'version',NULLIF(receipt->>'Version',''),'run_id',NULLIF(receipt->>'RunID',''),'error_code',NULLIF(receipt->>'ErrorCode','')))) FROM workflow_operations WHERE scope_key='feat-153-local-v1' AND workflow_id='{WID}' ORDER BY created_at,operation_id;
SELECT json_build_object('section','audit','id',id::text,'operation_id',operation_id::text,'workflow_id',workflow_id,'action',action,'outcome_code',outcome_code,'occurred_at',occurred_at) FROM workflow_audit WHERE scope_key='feat-153-local-v1' AND (workflow_id='{WID}' OR operation_id IN (SELECT operation_id FROM workflow_operations WHERE scope_key='feat-153-local-v1' AND workflow_id='{WID}')) ORDER BY id;
COMMIT;
"""

MYSQL_COMMAND = """set +x
set -eu
umask 077
option_file=$(mktemp /tmp/yijie-app-db-read.XXXXXXXXXX)
trap 'rm -f -- "$option_file"' EXIT
password=''
IFS= read -r password < /run/private/mysql-password || [ -n "$password" ]
[[ "$password" =~ ^[0-9a-f]{64}$ ]] || exit 1
printf '[client]\\nuser=workflow\\npassword=%s\\nhost=127.0.0.1\\nport=3306\\nprotocol=tcp\\n' "$password" > "$option_file"
unset password
mysql --defaults-file="$option_file" --no-login-paths --default-character-set=utf8mb4 --batch --raw --skip-column-names --connect-timeout=5 coze_workflow_local <<'APP_READ_ONLY_SQL'
""" + MYSQL_SQL + 'APP_READ_ONLY_SQL\n'

PG_COMMAND = """set +x
set -eu
umask 077
option_file=$(mktemp /tmp/yijie-app-db-read.XXXXXXXXXX)
trap 'rm -f -- "$option_file"' EXIT
password=''
IFS= read -r password < /run/private/postgres-password || [ -n "$password" ]
[ "${#password}" -eq 64 ] || exit 1
case "$password" in *[!0-9a-f]*) exit 1;; esac
printf '127.0.0.1:5432:yijie_workflow_local:workflow:%s\\n' "$password" > "$option_file"
unset password
PGPASSFILE="$option_file" psql -h 127.0.0.1 -p 5432 -U workflow -d yijie_workflow_local --no-psqlrc --no-password --quiet --tuples-only --no-align --set ON_ERROR_STOP=1 <<'APP_READ_ONLY_SQL'
""" + PG_SQL + 'APP_READ_ONLY_SQL\n'

def query(container, shell, script, mysql):
    start = now()
    args = c.docker_args(['exec', '--user', '0:0', container['id'], shell, '-c', script])
    process = subprocess.Popen(args, env=c.environment(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    stdout, _ = process.communicate()  # Normal finite read; no timeout/kill or raw stderr dump.
    c.require(process.returncode == 0 and len(stdout.encode()) <= 524288, 'A bounded read-only database snapshot did not complete')
    rows = {}
    for line in stdout.splitlines():
        if mysql:
            section, value = line.split('\t', 1)
            row = json.loads(value)
        else:
            row = json.loads(line)
            section = row.pop('section')
        rows.setdefault(section, []).append(row)
    return {'started_at': start, 'finished_at': now(), 'container_id': container['id'], 'image_id': container['image_id'], 'facts': rows}

def main():
    c.require(WID.isdigit() and 0 < int(WID) <= 9223372036854775807 and not DEST.exists(), 'Fixed resource or new evidence target differs')
    fd = os.open(c.GENERATED / 'controller.lock', os.O_RDWR | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as lock:
        info = os.fstat(lock.fileno())
        c.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid() and info.st_nlink == 1 and stat.S_IMODE(info.st_mode) == 0o600, 'Controller lock identity differs')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = c.read_state()
        c.require(state['run_epoch'] == EPOCH and state['phase'] == 'ready', 'The expected ready epoch is not active')
        items = c.all_containers()
        c.validate_owned(items, state)
        network_name = c.PROJECT + '_workflow-private'
        network = json.loads(c.output(['network', 'inspect', network_name]))
        c.require(len(network) == 1 and network[0].get('Internal') is True and network[0].get('Labels', {}).get('com.docker.compose.project') == c.PROJECT, 'Dedicated internal network identity differs')
        selected = {}
        for service, filename in [('workflow-postgres', 'postgres-password'), ('coze-workflow-mysql', 'mysql-password')]:
            matches = [i for i in items if i['labels'].get('com.docker.compose.service') == service and i['state']['Running'] and i['health'] == 'healthy']
            c.require(len(matches) == 1 and matches[0]['image_id'] == c.expected_image(service, state), 'Expected healthy database container differs')
            item = matches[0]
            attached = json.loads(c.output(['inspect', '--format', '{{json .NetworkSettings.Networks}}', item['id']]))
            c.require(set(attached) == {network_name}, 'Database is not confined to the owned internal network')
            expected_path = str(c.PRIVATE / filename)
            c.require(any(m['type'] == 'bind' and m['source'] in [expected_path, '/host_mnt' + expected_path] and m['target'] == '/run/private/' + filename and not m['rw'] for m in item['mounts']), 'Expected read-only password mount differs')
            selected[service] = item
        mysql = query(selected['coze-workflow-mysql'], '/bin/bash', MYSQL_COMMAND, True)
        pg = query(selected['workflow-postgres'], '/bin/sh', PG_COMMAND, False)
        c.require(mysql['facts']['snapshot'][0]['database'] == 'coze_workflow_local' and pg['facts']['snapshot'][0]['database'] == 'yijie_workflow_local', 'Dedicated database identity differs')
        c.require(len(mysql['facts'].get('resource', [])) == len(pg['facts'].get('resource', [])) == 1, 'The exact scoped synthetic resource is not unique')
        resource = mysql['facts']['resource'][0]
        canvas = resource.pop('canvas')
        # Root may rename this resource during ordinary UI qualification. Its
        # authorization boundary is the exact ID and fixed scope, not old UI text.
        c.require(isinstance(canvas, str) and len(canvas.encode()) <= 262144 and resource['workflow_id'] == WID and resource['principal_scope'] == SCOPE, 'Unexpected fixed resource or canvas budget')
        graph = json.loads(canvas)
        nodes = []
        for node in graph['nodes']:
            prefix = None
            for value in node.get('data', {}).get('inputs', {}).get('concatParams', []):
                if value.get('name') == 'concatResult':
                    literal = value.get('input', {}).get('value', {}).get('content')
                    if isinstance(literal, str) and literal.endswith('{{input}}'):
                        prefix = literal[:-9]
            nodes.append({'id': str(node['id']), 'type': str(node['type']), 'position': node.get('meta', {}).get('position'), 'prefix': prefix})
        resource['canvas_bytes'] = len(canvas.encode())
        resource['canvas_sha256'] = hashlib.sha256(canvas.encode()).hexdigest()
        c.require(resource['canvas_bytes'] == resource['server_canvas_bytes'] and resource['canvas_sha256'] == resource['server_canvas_sha256'], 'UTF-8 canvas bytes differ from the database-side byte count or SHA-256')
        resource['nodes'] = sorted(nodes, key=lambda node: node['id'])
        resource['edges'] = graph['edges']
        resource['node_count'] = len(nodes)
        resource['edge_count'] = len(graph['edges'])
        pg_ops = {i['operation_id']: i for i in pg['facts'].get('operation', [])}
        my_ops = {i['operation_id']: i for i in mysql['facts'].get('operation', [])}
        compared = []
        for operation_id in sorted(pg_ops.keys() & my_ops.keys()):
            left, right = pg_ops[operation_id]['receipt'], my_ops[operation_id]['receipt']
            fields = ['operation_id', 'kind', 'phase', 'workflow_id', 'revision', 'version', 'run_id']
            compared.append({'operation_id': operation_id, 'fields_match': all(left.get(k) == right.get(k) for k in fields), 'pg_phase': pg_ops[operation_id]['phase'], 'mysql_phase': right.get('phase')})
        current = c.all_containers()
        c.validate_owned(current, state)
        c.require(all(any(i['id'] == item['id'] and i['state']['Running'] and i['health'] == 'healthy' for i in current) for item in selected.values()), 'Database readiness changed during the normal read')
        final_state = c.read_state()
        c.require(final_state['run_epoch'] == EPOCH, 'Epoch changed during read')
        by_id = {node['id']: node for node in nodes}
        expected = {
            'revision': resource['revision'] == '7684605840325607424',
            'name': resource['name'] == 'FEAT-153 Packaged App 验收 20260912-1912',
            'three_nodes': len(nodes) == 3 and {key: value['type'] for key, value in by_id.items()} == {'100001': '1', '200001': '15', '900001': '2'},
            'start_position': by_id.get('100001', {}).get('position') == {'x': 80, 'y': 160},
            'text_position': by_id.get('200001', {}).get('position') == {'x': 452.5842696629214, 'y': 111.68539325842696},
            'end_position': by_id.get('900001', {}).get('position') == {'x': 760, 'y': 160},
            'prefix': by_id.get('200001', {}).get('prefix') == 'Packaged 中文验收：',
            'two_edges': len(graph['edges']) == 2 and {(edge.get('sourceNodeID'), edge.get('targetNodeID')) for edge in graph['edges']} == {('100001', '200001'), ('200001', '900001')},
            'one_create_one_save': sorted(item['kind'] for item in pg_ops.values()) == ['create', 'save'] and sorted(item['kind'] for item in my_ops.values()) == ['create', 'save'],
            'no_versions_or_executions': mysql['facts']['counts'] == [{'versions': 0, 'executions': 0}],
            'all_receipts_match': bool(compared) and all(item['fields_match'] for item in compared) and pg_ops.keys() == my_ops.keys(),
        }
        result = {'schema_version': 1, 'observation': 'packaged_final_app_single_resource_readonly', 'completed_read': True, 'workflow_id': WID, 'run_epoch': EPOCH, 'recorded_at': now(), 'observed_revision': resource['revision'], 'snapshot_note': 'Final packaged resource observation at the stated times; PostgreSQL and MySQL are separate read-only snapshots. Root paused resource edits during the read. This does not establish full UI/session-close qualification.', 'expected_packaged_resource_checks': expected, 'postgres': pg, 'mysql': mysql, 'cross_database': {'scope_identity_match': pg['facts']['resource'][0]['coze_user_id'] == resource['creator_id'] and pg['facts']['resource'][0]['coze_space_id'] == resource['space_id'], 'shared_operations': compared, 'postgres_only': sorted(pg_ops.keys() - my_ops.keys()), 'mysql_only': sorted(my_ops.keys() - pg_ops.keys())}, 'session_close': 'NOT OBSERVED: API sessions are memory-only; database rows do not prove revocation', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        outfd = os.open(DEST, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(outfd, 'w') as out:
            json.dump(result, out, ensure_ascii=False, indent=2)
            out.write('\n')
            out.flush()
            os.fsync(out.fileno())
        print(json.dumps({'read_completed': True, 'workflow_id': WID, 'observed_revision': resource['revision'], 'node_count': len(nodes), 'edge_count': len(graph['edges']), 'pg_operations': len(pg_ops), 'mysql_operations': len(my_ops), 'shared_receipts_match': all(i['fields_match'] for i in compared), 'expected_packaged_resource_matches': all(expected.values()), 'evidence': str(DEST)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except c.WorkflowError as error:
        print('APP_DB_READONLY: ' + str(error))
        raise SystemExit(1)
    except Exception as error:
        print('APP_DB_READONLY: ' + type(error).__name__ + '; no raw connection output or credentials displayed')
        raise SystemExit(1)
