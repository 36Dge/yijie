"""Scan the authorized main-window AX evidence in memory before persisting it."""
from pathlib import Path
import json, stat, subprocess, sys, time

root = Path(__file__).resolve().parents[6]
raw = subprocess.check_output(['/tmp/feat153-native-page-observe-ax', sys.argv[1], *sys.argv[3:]], text=True)
assert len(raw.encode()) <= 2 * 1024 * 1024
matches = {}
for name in ['k-na', 'k-ac']:
    path = root / ('yijie-infra/environments/local/generated/feat-153/private/' + name + '.json')
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) in (0o400, 0o600) and info.st_size <= 1024
    token = json.loads(path.read_text())['token']
    matches[name] = raw.count(token)
assert sum(matches.values()) == 0
data = json.loads(raw)
data.update(credential_matches=matches, observed_at_ms=int(time.time() * 1000))
target = Path(__file__).with_name(sys.argv[2])
assert target.suffix == '.json'
with target.open('x') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps({'path': str(target), 'nodes': len(data['nodes']), 'truncated': data['truncated'], 'credential_matches': matches}))
