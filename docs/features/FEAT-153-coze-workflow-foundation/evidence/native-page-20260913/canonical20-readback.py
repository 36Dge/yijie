"""Read two fixed resources after normal restart. GET and SELECT only; no UI/lifecycle."""
from pathlib import Path
from datetime import datetime, timezone
import fcntl
import hashlib
import http.client
import importlib.util
import json
import os
import re
import stat
import subprocess

ROOT = Path('/Users/jack/Downloads/Personal_Info/CrossBSD')
EVIDENCE = Path(__file__).parent
DEST = EVIDENCE / 'canonical20-readback.json'
OLD = '7684953519702409216'
SYNTHETIC = '7685009958215090176'
IDS = [OLD, SYNTHETIC]
SCOPE = '12500000-0000-4000-8000-000000000001:12500000-0000-4000-8000-100000000001'
spec = importlib.util.spec_from_file_location('workflow_controller_readonly', ROOT / 'yijie-infra/scripts/workflow-local.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()

def now():
    return datetime.now(timezone.utc).isoformat()

def read_api(path, credential, metadata=False):
    conn = http.client.HTTPConnection('127.0.0.1', 18888, timeout=10)
    try:
        headers = {'Authorization': 'Bearer ' + credential['token'], 'X-Yijie-Run-Epoch': credential['run_epoch']}
        if metadata:
            headers['X-Yijie-Workflow-Metadata'] = 'description-v1'
        conn.request('GET', path, headers=headers)
        response = conn.getresponse()
        raw = response.read(524289)
        c.require(response.status == 200 and len(raw) <= 524288, 'Bounded API read did not return a valid response')
        return json.loads(raw)
    finally:
        conn.close()

MYSQL_SQL = f"""
SELECT 'snapshot', JSON_OBJECT('database',DATABASE(),'observed_at',CAST(UTC_TIMESTAMP(6) AS CHAR));
SELECT 'resource', JSON_OBJECT('workflow_id',CAST(m.id AS CHAR),'name',m.name,'description',m.description,'creator_id',CAST(m.creator_id AS CHAR),'space_id',CAST(m.space_id AS CHAR),'app_id',CAST(m.app_id AS CHAR),'latest_version',m.latest_version,'revision',d.commit_id,'updated_at_ms',d.updated_at,'canvas_bytes',OCTET_LENGTH(d.canvas),'canvas_sha256',SHA2(d.canvas,256),'principal_scope',p.scope_key) FROM workflow_meta m JOIN workflow_draft d ON d.id=m.id JOIN yijie_workflow_local_principal p ON p.user_id=m.creator_id AND p.space_id=m.space_id WHERE m.id IN ({','.join(IDS)}) AND m.app_id=0 AND m.deleted_at IS NULL AND d.deleted_at IS NULL AND p.scope_key='{SCOPE}' ORDER BY m.id;
SELECT 'version', JSON_OBJECT('workflow_id',CAST(workflow_id AS CHAR),'version',version,'revision',commit_id,'canvas_bytes',OCTET_LENGTH(canvas),'canvas_sha256',SHA2(canvas,256),'created_at_ms',created_at) FROM workflow_version WHERE workflow_id={SYNTHETIC} AND deleted_at IS NULL ORDER BY id;
SELECT 'execution', JSON_OBJECT('run_id',CAST(id AS CHAR),'workflow_id',CAST(workflow_id AS CHAR),'version',version,'revision',commit_id,'status',status,'mode',mode,'input',input,'output',output,'error_code',error_code,'created_at_ms',created_at,'updated_at_ms',updated_at) FROM workflow_execution WHERE workflow_id={SYNTHETIC} ORDER BY id;
SELECT 'operation', JSON_OBJECT('operation_id',operation_id,'kind',kind,'workflow_id',CAST(workflow_id AS CHAR),'run_id',CAST(run_id AS CHAR),'run_epoch',run_epoch,'receipt',CAST(receipt AS JSON)) FROM yijie_workflow_local_operation WHERE scope_key='{SCOPE}' AND workflow_id={SYNTHETIC} ORDER BY created_at,operation_id;
"""
PG_SQL = f"""
SELECT json_build_object('section','snapshot','database',current_database(),'observed_at',clock_timestamp());
SELECT json_build_object('section','resource','workflow_id',r.workflow_id,'scope_key',r.scope_key,'owner_user_id',s.owner_user_id::text,'tenant_id',s.tenant_id::text,'coze_user_id',s.coze_user_id,'coze_space_id',s.coze_space_id) FROM workflow_resources r JOIN workflow_scope_bindings s USING(scope_key) WHERE r.scope_key='feat-153-local-v1' AND r.workflow_id IN ('{OLD}','{SYNTHETIC}') ORDER BY r.workflow_id;
SELECT json_build_object('section','operation','operation_id',operation_id::text,'kind',kind,'phase',phase,'workflow_id',workflow_id,'receipt',jsonb_strip_nulls(jsonb_build_object('operation_id',receipt->>'OperationID','kind',receipt->>'Kind','phase',receipt->>'Phase','workflow_id',NULLIF(receipt->>'WorkflowID',''),'revision',NULLIF(receipt->>'Revision',''),'version',NULLIF(receipt->>'Version',''),'run_id',NULLIF(receipt->>'RunID',''),'error_code',NULLIF(receipt->>'ErrorCode','')))) FROM workflow_operations WHERE scope_key='feat-153-local-v1' AND workflow_id='{SYNTHETIC}' ORDER BY created_at,operation_id;
SELECT json_build_object('section','audit','operation_id',operation_id::text,'workflow_id',workflow_id,'action',action,'outcome_code',outcome_code,'occurred_at',occurred_at) FROM workflow_audit WHERE scope_key='feat-153-local-v1' AND workflow_id='{SYNTHETIC}' ORDER BY id;
"""

def db_query(item, sql, mysql):
    # Credentials stay inside the existing container process environment, never
    # in host arguments, output, evidence or a new credentials file.
    c.require(all(part.strip().upper().startswith('SELECT ') for part in sql.split(';') if part.strip()), 'SQL must contain SELECT statements only')
    password_file = 'mysql-password' if mysql else 'postgres-password'
    prefix = "set +x\nset -eu\npassword=''\nIFS= read -r password < /run/private/" + password_file + " || [ -n \"$password\" ]\n[ \"${#password}\" -eq 64 ]\ncase \"$password\" in *[!0-9a-f]*) exit 1;; esac\n"
    command = ('MYSQL_PWD="$password" mysql --no-defaults --no-login-paths --default-character-set=utf8mb4 --batch --raw --skip-column-names --connect-timeout=5 -h 127.0.0.1 -P 3306 -u workflow coze_workflow_local' if mysql else 'PGPASSWORD="$password" psql -h 127.0.0.1 -p 5432 -U workflow -d yijie_workflow_local --no-psqlrc --no-password --quiet --tuples-only --no-align --set ON_ERROR_STOP=1')
    script = prefix + command + " <<'READ_ONLY_SELECT_SQL'\n" + sql + '\nREAD_ONLY_SELECT_SQL\nunset password\n'
    started = now()
    result = subprocess.run(c.docker_args(['exec', '--user', '0:0', item['id'], '/bin/sh', '-c', script]), env=c.environment(), capture_output=True, text=True)
    c.require(result.returncode == 0 and len(result.stdout.encode()) <= 524288, 'Bounded SELECT read did not complete; raw stderr withheld')
    sections = {}
    for line in result.stdout.splitlines():
        if mysql:
            section, raw = line.split('\t', 1)
            row = json.loads(raw)
        else:
            row = json.loads(line)
            section = row.pop('section')
        sections.setdefault(section, []).append(row)
    return {'started_at': started, 'finished_at': now(), 'container_id': item['id'], 'image_id': item['image_id'], 'statements': 'SELECT only; ordinary autocommit reads, not a cross-database atomic snapshot', 'facts': sections}

def main():
    c.require(not DEST.exists() and all(re.fullmatch('[1-9][0-9]{0,18}', v) for v in IDS), 'Fixed IDs/new evidence target required')
    fd = os.open(c.GENERATED / 'controller.lock', os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as lock:
        info = os.fstat(lock.fileno())
        c.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o600, 'Controller lock identity differs')
        fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        state = c.read_state()
        c.require(state['phase'] == 'ready' and state['run_epoch'].startswith('28a9b428-'), 'Expected canonical 20 ready epoch differs')
        credential = json.loads(c.secure_read(c.PRIVATE / 'k-na.json'))
        c.require(credential['run_epoch'] == state['run_epoch'], 'Credential epoch differs')
        items = c.all_containers()
        c.validate_owned(items, state)
        selected = {}
        network_name = c.PROJECT + '_workflow-private'
        network = json.loads(c.output(['network', 'inspect', network_name]))
        c.require(len(network) == 1 and network[0]['Internal'] is True, 'Dedicated private network differs')
        for service, password_file in [('workflow-postgres', 'postgres-password'), ('coze-workflow-mysql', 'mysql-password')]:
            matches = [i for i in items if i['labels'].get('com.docker.compose.service') == service and i['state']['Running'] and i['health'] == 'healthy']
            c.require(len(matches) == 1 and matches[0]['image_id'] == c.expected_image(service, state), 'Expected healthy database differs')
            item = matches[0]
            attached = json.loads(c.output(['inspect', '--format', '{{json .NetworkSettings.Networks}}', item['id']]))
            c.require(set(attached) == {network_name}, 'Database network differs')
            password_path = str(c.PRIVATE / password_file)
            c.require(any(m['type'] == 'bind' and m['source'] in [password_path, '/host_mnt' + password_path] and m['target'] == '/run/private/' + password_file and not m['rw'] for m in item['mounts']), 'Existing password mount differs')
            selected[service] = item
        workflows = {}
        for wid in IDS:
            path = '/v1/workflows/' + wid
            workflows[wid] = {'path': path, 'legacy': read_api(path, credential), 'metadata': read_api(path, credential, True), 'legacy_projection_preserved': True}
            c.require('description' not in workflows[wid]['legacy'], 'Legacy metadata opt-in changed')
            expected_legacy = {k: v for k, v in workflows[wid]['metadata'].items() if k != 'description'}
            c.require(workflows[wid]['legacy'] == expected_legacy, 'Legacy projection differs')
        before = json.loads((EVIDENCE / 'existing-screenshot-workflow-before.json').read_text())
        c.require(workflows[OLD] == before, 'Original screenshot workflow changed')
        saved = json.loads((EVIDENCE / 'native-keyboard-undo-saved.json').read_text())
        c.require(all(workflows[SYNTHETIC]['metadata'][k] == saved['metadata'][k] for k in ['canvas', 'name', 'description', 'revision']), 'Saved synthetic draft differs after restart')
        path = '/v1/workflows/' + SYNTHETIC
        history = read_api(path + '/runs?limit=20', credential)
        c.require(len(history['items']) <= 20 and not history.get('next_cursor'), 'Bounded expected history differs')
        runs = []
        for item in history['items']:
            rid = item['run_id']
            c.require(re.fullmatch('[1-9][0-9]{0,18}', rid), 'Run ID shape differs')
            run = read_api(path + '/runs/' + rid, credential)
            c.require(run['workflow_id'] == SYNTHETIC and run['run_id'] == rid, 'Run binding differs')
            runs.append(run)
        expected_outputs = {'7685025979823030272': '原生画布：易界验收', '7685026094679851008': '原生画布：版本执行验收', '7685027859953352704': '原生画布：修正验收'}
        run_by_id = {run['run_id']: run for run in runs}
        for rid, expected in expected_outputs.items():
            run = run_by_id[rid]
            c.require(run['terminal'] and run['state'] == 'succeeded' and expected in json.dumps(run, ensure_ascii=False), 'Known successful run result differs')
        mysql = db_query(selected['coze-workflow-mysql'], MYSQL_SQL, True)
        postgres = db_query(selected['workflow-postgres'], PG_SQL, False)
        c.require(mysql['facts']['snapshot'][0]['database'] == 'coze_workflow_local' and postgres['facts']['snapshot'][0]['database'] == 'yijie_workflow_local', 'Database identity differs')
        resources = {row['workflow_id']: row for row in mysql['facts']['resource']}
        pg_resources = {row['workflow_id']: row for row in postgres['facts']['resource']}
        c.require(set(resources) == set(pg_resources) == set(IDS), 'Exact scoped resources differ')
        for wid in IDS:
            db = resources[wid]
            api = workflows[wid]['metadata']
            c.require(all(db[k] == api[k] for k in ['name', 'description', 'revision', 'updated_at_ms']), 'Database resource fields differ from API')
            c.require(db['canvas_sha256'] == digest(api['canvas']) and db['canvas_bytes'] == len(api['canvas'].encode()), 'Database canvas bytes differ from API')
            c.require(db['principal_scope'] == SCOPE and db['creator_id'] == pg_resources[wid]['coze_user_id'] and db['space_id'] == pg_resources[wid]['coze_space_id'], 'Cross-database ownership differs')
        db_runs = {row['run_id']: row for row in mysql['facts']['execution']}
        for rid, expected in expected_outputs.items():
            c.require(db_runs[rid]['status'] == 2 and expected in db_runs[rid]['output'], 'Database execution output differs')
        versions = mysql['facts']['version']
        c.require(len(versions) == 1 and versions[0]['version'] == 'v0.0.1' and versions[0]['revision'] == workflows[SYNTHETIC]['metadata']['revision'], 'Published version readback differs')
        c.require(versions[0]['canvas_sha256'] == resources[SYNTHETIC]['canvas_sha256'], 'Published canvas differs')
        pg_ops = {row['operation_id']: row for row in postgres['facts'].get('operation', [])}
        my_ops = {row['operation_id']: row for row in mysql['facts'].get('operation', [])}
        receipt_matches = []
        for oid in sorted(pg_ops.keys() & my_ops.keys()):
            left, right = pg_ops[oid]['receipt'], my_ops[oid]['receipt']
            fields = ['operation_id', 'kind', 'phase', 'workflow_id', 'revision', 'version', 'run_id']
            receipt_matches.append({'operation_id': oid, 'match': all(left.get(k) == right.get(k) for k in fields)})
        c.require(all(row['match'] for row in receipt_matches), 'Persisted operation receipts differ')
        c.require(c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during read')
        result = {'schema_version': 1, 'recorded_at': now(), 'run_epoch': state['run_epoch'], 'scope': 'Two exact workflows after root-performed normal App/stack restart; GET and SQL SELECT only', 'original_workflow_full_legacy_and_metadata_unchanged': True, 'synthetic_draft_fields_and_canvas_equal_last_saved': True, 'publication_since_saved_baseline': {'published_version_before': saved['metadata'].get('published_version'), 'published_version_now': workflows[SYNTHETIC]['metadata'].get('published_version'), 'updated_at_ms_before': saved['metadata']['updated_at_ms'], 'updated_at_ms_now': workflows[SYNTHETIC]['metadata']['updated_at_ms'], 'note': 'The saved baseline precedes normal publication; publication/version timestamp changes are not asserted byte-identical. Canvas, name, description and revision are identical.'}, 'original_baseline_sha256': digest((EVIDENCE / 'existing-screenshot-workflow-before.json').read_bytes()), 'synthetic_last_saved_sha256': digest((EVIDENCE / 'native-keyboard-undo-saved.json').read_bytes()), 'workflows': workflows, 'history': history, 'runs': runs, 'expected_successful_outputs': expected_outputs, 'mysql': mysql, 'postgres': postgres, 'cross_database': {'ownership_match': True, 'canvas_utf8_bytes_and_sha256_match_api': True, 'shared_receipts': receipt_matches, 'postgres_only_operations': sorted(pg_ops.keys() - my_ops.keys()), 'mysql_only_operations': sorted(my_ops.keys() - pg_ops.keys())}, 'limits': 'Does not perform UI, prove memory-only session revocation, or qualify canonical 20 first save/Undo/dev/D4. SQL reads are independent ordinary SELECT snapshots.', 'script_sha256': digest(Path(__file__).read_bytes())}
        raw = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        for file in ['k-na.json', 'k-ac.json']:
            c.require(json.loads(c.secure_read(c.PRIVATE / file))['token'] not in raw, 'Secret exposure detected; evidence not written')
        with DEST.open('x') as out:
            out.write(raw)
        print(json.dumps({'completed': True, 'original_unchanged': True, 'synthetic_saved_canvas_unchanged': True, 'runs': len(runs), 'known_successful_runs': len(expected_outputs), 'version': versions[0]['version'], 'cross_database_receipts_match': True, 'evidence': str(DEST)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('READBACK STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, c.WorkflowError) else '') + '; raw connection output and credentials withheld')
        raise SystemExit(1)
