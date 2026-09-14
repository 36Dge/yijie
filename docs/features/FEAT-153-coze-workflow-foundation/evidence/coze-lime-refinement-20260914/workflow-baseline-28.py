"""Fresh before-UI GET baselines; never assume equality to any earlier task snapshot."""
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
spec = importlib.util.spec_from_file_location('fixed_get_reader', HELPER)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
IDS = ['7685061713409867776', '7685031373442121728']
MANIFEST = '6cf9228ae89480f94197ff48193fdaa0e0580a65cae893ae8c93001489b12def'
SOURCE = 'b69117dec6ff31092f6078dad3281d5ca73270042f2e6ebf05a43dd5cebe1fdf'

def main():
    index_file = HERE / 'before-ui-baseline28.json'
    targets = {wid: HERE / ('workflow-' + wid + '-before-ui28.json') for wid in IDS}
    r.c.require(not index_file.exists() and all(not p.exists() for p in targets.values()), 'Fresh evidence targets required')
    activation_file = HERE / 'activation28.json'
    activation = json.loads(activation_file.read_text())
    r.c.require(activation['manifest_sha256'] == MANIFEST and activation['source_digest'] == SOURCE, 'Expected canonical 28 activation differs')
    fd = os.open(r.c.GENERATED / 'controller.lock', os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as lock:
        info = os.fstat(lock.fileno())
        r.c.require(stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid() and stat.S_IMODE(info.st_mode) == 0o600, 'Controller lock identity differs')
        fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        state = r.c.read_state()
        r.c.require(state['phase'] == 'ready', 'Controlled stack is not ready')
        credential = json.loads(r.c.secure_read(r.c.PRIVATE / 'k-na.json'))
        r.c.require(credential['run_epoch'] == state['run_epoch'], 'Credential epoch differs')
        observed_at = r.now()
        payloads = {}
        facts = []
        for wid in IDS:
            path = '/v1/workflows/' + wid
            legacy = r.read_api(path, credential)
            metadata = r.read_api(path, credential, True)
            r.c.require(legacy['workflow_id'] == metadata['workflow_id'] == wid, 'Exact workflow binding differs')
            r.c.require('description' not in legacy and legacy == {key: value for key, value in metadata.items() if key != 'description'}, 'Legacy metadata projection differs')
            value = {'path': path, 'legacy': legacy, 'metadata': metadata, 'legacy_projection_preserved': True}
            raw = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
            payloads[targets[wid]] = raw
            facts.append({'workflow_id': wid, 'name': metadata['name'], 'revision': metadata['revision'], 'updated_at_ms': metadata['updated_at_ms'], 'canvas_sha256': r.digest(metadata['canvas']), 'evidence_file': targets[wid].name, 'evidence_sha256': r.digest(raw)})
        r.c.require(r.c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during reads')
        result = {'schema_version': 1, 'observed_at': observed_at, 'completed_at': r.now(), 'phase': 'fresh_before_UI_baseline', 'run_epoch': state['run_epoch'], 'manifest_sha256': MANIFEST, 'source_digest': SOURCE, 'activation_file': activation_file.name, 'activation_sha256': r.digest(activation_file.read_bytes()), 'workflows': facts, 'scope': 'GET both projections for these two exact existing workflows only. This records their current state; it does not compare to earlier task snapshots or claim the user has not modified them since then.', 'limits': 'Not an after-UI preservation result, UI qualification, database snapshot or D4 claim. GET may append normal successful read audits; no workflow business writes.', 'script_sha256': r.digest(Path(__file__).read_bytes()), 'helper_sha256': r.digest(HELPER.read_bytes())}
        payloads[index_file] = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        for secret_file in ['k-na.json', 'k-ac.json']:
            secret = json.loads(r.c.secure_read(r.c.PRIVATE / secret_file))['token']
            r.c.require(all(secret not in raw for raw in payloads.values()), 'Credential found; evidence not written')
        for destination, raw in payloads.items():
            with destination.open('x') as output:
                output.write(raw)
        print(json.dumps({'completed': True, 'phase': result['phase'], 'workflow_baselines': facts, 'index': str(index_file)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('BASELINE STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, r.c.WorkflowError) else '') + '; credentials and raw connection output withheld')
        raise SystemExit(1)
