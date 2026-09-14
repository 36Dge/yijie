"""GET-only preservation comparison against this round's fresh before-UI baseline."""
from pathlib import Path
import fcntl
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('this_round_baseline', HERE / 'workflow-baseline-28.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.r

def main():
    destination = HERE / 'existing-workflows-preserved-after28.json'
    r.c.require(not destination.exists(), 'New preservation evidence required')
    before_index = json.loads((HERE / 'before-ui-baseline28.json').read_text())
    r.c.require(before_index['manifest_sha256'] == m.MANIFEST and before_index['source_digest'] == m.SOURCE, 'This round baseline differs')
    fd = os.open(r.c.GENERATED / 'controller.lock', os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'r') as lock:
        fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        state = r.c.read_state()
        r.c.require(state['phase'] == 'ready' and state['run_epoch'] == before_index['run_epoch'], 'Expected ready before/after epoch differs')
        credential = json.loads(r.c.secure_read(r.c.PRIVATE / 'k-na.json'))
        r.c.require(credential['run_epoch'] == state['run_epoch'], 'Credential epoch differs')
        payloads, results = {}, []
        for wid in m.IDS:
            before_file = HERE / ('workflow-' + wid + '-before-ui28.json')
            before_raw = before_file.read_bytes()
            before = json.loads(before_raw)
            path = '/v1/workflows/' + wid
            legacy, metadata = r.read_api(path, credential), r.read_api(path, credential, True)
            r.c.require(legacy['workflow_id'] == metadata['workflow_id'] == wid, 'Fixed response resource differs')
            r.c.require('description' not in legacy and legacy == {key: value for key, value in metadata.items() if key != 'description'}, 'Legacy projection differs')
            after = {'path': path, 'legacy': legacy, 'metadata': metadata, 'legacy_projection_preserved': True}
            after_file = HERE / ('workflow-' + wid + '-after-ui28.json')
            r.c.require(not after_file.exists(), 'New response evidence required')
            after_raw = json.dumps(after, ensure_ascii=False, indent=2) + '\n'
            payloads[after_file] = after_raw
            results.append({'workflow_id': wid, 'name': metadata['name'], 'revision': metadata['revision'], 'before_file': before_file.name, 'before_sha256': r.digest(before_raw), 'after_file': after_file.name, 'after_sha256': r.digest(after_raw), 'legacy_complete_equal': before['legacy'] == legacy, 'metadata_complete_equal': before['metadata'] == metadata, 'full_response_object_equal': before == after})
        r.c.require(r.c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during reads')
        result = {'schema_version': 1, 'recorded_at': r.now(), 'run_epoch': state['run_epoch'], 'baseline_observed_at': before_index['observed_at'], 'baseline_index_sha256': r.digest((HERE / 'before-ui-baseline28.json').read_bytes()), 'manifest_sha256': m.MANIFEST, 'source_digest': m.SOURCE, 'workflows': results, 'all_full_responses_equal': all(row['full_response_object_equal'] for row in results), 'scope': 'Fresh current-round before-UI versus after-UI GET responses for two exact existing workflows. Earlier round timestamps are not used as preservation evidence. No business writes; ordinary GET audit may be appended.', 'script_sha256': r.digest(Path(__file__).read_bytes())}
        payloads[destination] = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        for secret_file in ['k-na.json', 'k-ac.json']:
            secret = json.loads(r.c.secure_read(r.c.PRIVATE / secret_file))['token']
            r.c.require(all(secret not in raw for raw in payloads.values()), 'Credential found; evidence not written')
        for path, raw in payloads.items():
            with path.open('x') as output:
                output.write(raw)
        print(json.dumps({'completed': True, 'all_full_responses_equal': result['all_full_responses_equal'], 'workflow_ids': m.IDS, 'evidence': str(destination)}, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('PRESERVATION STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, r.c.WorkflowError) else '') + '; credentials and raw connection output withheld')
        raise SystemExit(1)
