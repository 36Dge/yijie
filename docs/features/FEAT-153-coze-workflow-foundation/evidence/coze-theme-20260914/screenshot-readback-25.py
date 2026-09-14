"""GET-only comparison of the exact pre-existing screenshot workflow after theme 25."""
from pathlib import Path
from hashlib import sha256
import http.client
import importlib.util
import json
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/jack/Downloads/Personal_Info/CrossBSD')
HERE = Path(__file__).parent
WID = '7685031373442121728'
BEFORE = HERE / 'screenshot-workflow-before-ui.json'
AFTER = HERE / 'screenshot-workflow-after-25.json'
COMPARISON = HERE / 'screenshot-workflow-comparison-25.json'
spec = importlib.util.spec_from_file_location('workflow_controller_readonly', ROOT / 'yijie-infra/scripts/workflow-local.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

def read(path, credential, metadata):
    connection = http.client.HTTPConnection('127.0.0.1', 18888, timeout=10)
    try:
        headers = {'Authorization': 'Bearer ' + credential['token'], 'X-Yijie-Run-Epoch': credential['run_epoch'], 'Accept': 'application/json'}
        if metadata:
            headers['X-Yijie-Workflow-Metadata'] = 'description-v1'
        connection.request('GET', path, headers=headers)
        response = connection.getresponse()
        data = response.read(524289)
        c.require(response.status == 200 and len(data) <= 524288, 'Bounded GET did not return a valid response')
        return json.loads(data)
    finally:
        connection.close()

def main():
    c.require(not AFTER.exists() and not COMPARISON.exists(), 'New evidence targets required')
    before_raw = BEFORE.read_bytes()
    before = json.loads(before_raw)
    path = '/v1/workflows/' + WID
    c.require(before['path'] == path and before['metadata']['workflow_id'] == WID, 'Fixed baseline resource differs')
    activation = json.loads((HERE / 'activation-25.json').read_text())
    c.require(activation['manifest_sha256'].startswith('062565c6') and activation['source_digest'].startswith('168c5814'), 'Expected theme candidate differs')
    state = c.read_state()
    c.require(state['phase'] == 'ready', 'Controlled stack is not ready')
    credential = json.loads(c.secure_read(c.PRIVATE / 'k-na.json'))
    c.require(credential['run_epoch'] == state['run_epoch'], 'Credential epoch differs')
    legacy = read(path, credential, False)
    metadata = read(path, credential, True)
    c.require(legacy.get('workflow_id') == metadata.get('workflow_id') == WID, 'API resource binding differs')
    projection_matches = 'description' not in legacy and legacy == {key: value for key, value in metadata.items() if key != 'description'}
    c.require(projection_matches, 'Legacy metadata opt-in projection differs')
    after = {'path': path, 'legacy': legacy, 'metadata': metadata, 'legacy_projection_preserved': projection_matches}
    after_raw = json.dumps(after, ensure_ascii=False, indent=2) + '\n'
    comparison = {'schema_version': 1, 'observed_at_ms': int(time.time() * 1000), 'workflow_id': WID, 'run_epoch': state['run_epoch'], 'manifest_sha256': activation['manifest_sha256'], 'source_digest': activation['source_digest'], 'before_file': BEFORE.name, 'before_sha256': sha256(before_raw).hexdigest(), 'after_file': AFTER.name, 'after_sha256': sha256(after_raw.encode()).hexdigest(), 'full_legacy_response_unchanged': legacy == before['legacy'], 'full_metadata_response_unchanged': metadata == before['metadata'], 'complete_response_object_unchanged': after == before, 'observed_revision': metadata['revision'], 'canvas_sha256': sha256(metadata['canvas'].encode()).hexdigest(), 'source': 'GET only; no UI or workflow business writes. Existing API audit may append successful read records.', 'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}
    comparison_raw = json.dumps(comparison, ensure_ascii=False, indent=2) + '\n'
    c.require(c.read_state()['run_epoch'] == state['run_epoch'], 'Epoch changed during read')
    for file in ['k-na.json', 'k-ac.json']:
        secret = json.loads(c.secure_read(c.PRIVATE / file))['token']
        c.require(secret not in after_raw and secret not in comparison_raw, 'Credential found; evidence not written')
    with AFTER.open('x') as output:
        output.write(after_raw)
    with COMPARISON.open('x') as output:
        output.write(comparison_raw)
    print(json.dumps({key: comparison[key] for key in ['workflow_id', 'observed_revision', 'full_legacy_response_unchanged', 'full_metadata_response_unchanged', 'complete_response_object_unchanged', 'canvas_sha256']}, ensure_ascii=False))
    if not comparison['complete_response_object_unchanged']:
        raise SystemExit(2)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('READBACK STOPPED: ' + type(error).__name__ + ('; ' + str(error) if isinstance(error, c.WorkflowError) else '') + '; credentials and raw connection output withheld')
        raise SystemExit(1)
