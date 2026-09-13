"""Read only the exact synthetic workflow made in the real App and its runs."""
import hashlib
import http.client
import json
from pathlib import Path
import re
import stat
import sys
import time

ROOT = Path('/Users/jack/Downloads/Personal_Info/CrossBSD')
WID = '7684864630077784064'
credential = ROOT / 'yijie-infra/environments/local/generated/feat-153/private/k-na.json'
info = credential.lstat()
assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) in (0o400, 0o600) and info.st_size <= 1024
c = json.loads(credential.read_text())

def read(path):
    conn = http.client.HTTPConnection('127.0.0.1', 18888, timeout=10)
    try:
        conn.request('GET', path, headers={'Authorization': 'Bearer ' + c['token'], 'X-Yijie-Run-Epoch': c['run_epoch']})
        response = conn.getresponse()
        raw = response.read(524289)
        assert response.status == 200 and len(raw) <= 524288
        return json.loads(raw)
    finally:
        conn.close()

workflow = read('/v1/workflows/' + WID)
assert workflow['workflow_id'] == WID
history = read('/v1/workflows/' + WID + '/runs?limit=20')
runs, receipts = [], []
assert len(history['items']) <= 20
for item in history['items']:
    rid = item['run_id']
    assert re.fullmatch('[1-9][0-9]{0,18}', rid)
    run = read('/v1/workflows/' + WID + '/runs/' + rid)
    assert run['workflow_id'] == WID and run['run_id'] == rid
    oid = run['operation_id']
    assert re.fullmatch('[0-9a-f-]{36}', oid)
    runs.append(run)
    receipts.append(read('/v1/workflow-local/operations/' + oid))
out = Path(__file__).with_name(sys.argv[1])
assert out.suffix == '.json' and not out.exists()
result = {'observed_at_ms': int(time.time()*1000), 'run_epoch': c['run_epoch'], 'workflow': workflow,
          'canvas_sha256': hashlib.sha256(workflow['canvas'].encode()).hexdigest(),
          'history': history, 'runs': runs, 'receipts': receipts,
          'source': 'Bounded read-only API; all create/save/test/publish/run actions were performed in the real App through user-authorized macOS AX/CGEvent.'}
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'workflow_id': WID, 'revision': workflow['revision'], 'runs': len(runs),
                  'all_runs_succeeded': all(r['terminal'] and r['state'] == 'succeeded' for r in runs), 'evidence': str(out)}))
