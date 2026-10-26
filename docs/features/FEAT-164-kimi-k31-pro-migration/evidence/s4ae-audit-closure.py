"""Read-only FEAT-164 evidence/source/artifact audit. No model, App or DB API."""
from pathlib import Path
import datetime
import hashlib
import json
import plistlib
import subprocess

ROOT = Path('/Users/jack/Downloads/Personal_Info/CrossBSD')
AUDIT = ROOT / 'feat164-s4ae-audit-20261027'
EVIDENCE = ROOT / 'yijie/docs/features/FEAT-164-kimi-k31-pro-migration/evidence'
QUAL = ROOT / 'feat164-s4ad-qualification-20261027'

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def read(path):
    return json.loads(path.read_text())

def git(repo, *args):
    return subprocess.check_output(['git', *args], cwd=repo).decode().strip()

failures = []
def require(condition, label):
    if not condition:
        failures.append(label)

def check_file(path, expected):
    if not path.is_file():
        failures.append('missing: ' + str(path))
        return
    value = expected if isinstance(expected, str) else expected['sha256']
    require(digest(path) == value, 'digest: ' + str(path))
    if isinstance(expected, dict):
        stat = path.stat()
        require(stat.st_size == expected['bytes'], 'size: ' + str(path))
        require(stat.st_mode & 0o777 == expected['mode'], 'mode: ' + str(path))

indices = []
for phase in ['s4s','s4t','s4u','s4v','s4w','s4x','s4y','s4z','s4aa','s4ab','s4ac','s4ad']:
    path = EVIDENCE / (phase + '-audit-index.json')
    data = read(path)
    rows = [(Path(row['path']), row['sha256']) for row in data['files']] if isinstance(data['files'], list) else [(EVIDENCE/name, value) for name,value in data['files'].items()]
    before = len(failures)
    for file, expected in rows:
        check_file(file, expected)
    private = data.get('private_read_only_facts', {})
    for name, expected in private.items():
        check_file(Path(data['private_root'])/name, expected)
    indices.append({'phase':phase,'index_sha256':digest(path),'indexed_files':len(rows),'additional_private_facts':len(private),'mismatches':len(failures)-before})

source_binding = read(EVIDENCE/'s4ad-source-binding.json')
sources = {}
for name, expected in source_binding['sources'].items():
    repo = QUAL/name
    actual = {'head':git(repo,'rev-parse','HEAD'),'status':git(repo,'status','--porcelain')}
    require(actual == expected, 'source ' + name)
    sources[name] = actual

test_repo = ROOT/'feat164-s4ad-tests-20261027/yijie-desktop'
require(git(test_repo,'rev-parse','HEAD') == source_binding['test_commit'], 'retained test commit')
require(not git(test_repo,'status','--porcelain'), 'retained test clean')
test_paths = git(test_repo,'diff','--name-only',source_binding['app_source'],'HEAD').splitlines()
require(sorted(test_paths) == sorted(source_binding['test_only_paths']), 'test-only delta')
for name, expected in read(EVIDENCE/'s4ad-desktop-staged.json')['sha256'].items():
    check_file(test_repo/name, expected)
require(git(QUAL/'yijie-desktop','diff','--name-only','c98eddfafb789520b4939bdca95bf8b27f28b7b6','HEAD') == 'src/domain/conversation-native-view.test.ts', 'previous qualification App product equivalence')

bundles = []
definitions = [
    ('feat164-s4ad-qualification-20261027','feat164-kimi-k31','易界 AI FEAT-164.app','com.yijie.ai.feat164-kimi-k31-r1','bbb09fd92d66f808180ee4d07331596b93650299be642159d4285b9d342fa744'),
    ('feat164-s4aa-qualification-20261027','feat164-qualification','易界 AI FEAT-164 验收.app','com.yijie.ai.feat164-qualification-v1','716ad8a4a623bbe5a1701995e60691f4a1aebce7f493861c2ba100f39a6dcac9'),
    ('feat164-s4ac-daily-candidate-20261027','feat164-daily','易界 AI.app','com.yijie.ai','ee4c53922b9642ffa81c3d6356827df6e8dbdcf6c0ec582e108bc954d768add7'),
]
for workspace, slot, name, identity, receipt_sha in definitions:
    desktop = ROOT/workspace/'yijie-desktop'
    receipt = desktop/'.local'/slot/'packaged-launch-receipt.json'
    check_file(receipt, receipt_sha)
    data = read(receipt)
    before = len(failures)
    bundle = desktop/'src-tauri/target/debug/bundle/macos'/name
    require({str(p.relative_to(bundle)) for p in bundle.rglob('*') if p.is_file()} == set(data['artifacts']['bundle']), 'bundle exact inventory ' + workspace)
    for relative, expected in data['artifacts']['bundle'].items():
        check_file(bundle/relative, expected)
    require(plistlib.loads((bundle/'Contents/Info.plist').read_bytes())['CFBundleIdentifier'] == identity, 'bundle identity ' + workspace)
    for relative, expected in data['inputs']['sources'].items():
        check_file(desktop/relative, expected)
    connectors = ROOT/workspace/'yijie-connectors'
    for relative, expected in data['inputs']['workerSources'].items():
        check_file(connectors/relative, expected)
    runtime = ROOT/workspace/'yijie-codex/.yijie/build/kimi-k31-pro-r5/aarch64-apple-darwin'
    worker_manifest = connectors/'bin/market-worker/current.json'
    artifacts = {
        'host':desktop/'.local'/slot/'bin/yijie-agent-host',
        'adapter':desktop/'.local'/slot/'bin/yijie-artifact-mcp',
        'runtime':runtime/'codex',
        'runtimeManifest':runtime/'runtime-manifest.json',
        'workerManifest':worker_manifest,
        'worker':Path(read(worker_manifest)['binary']),
    }
    for key, path in artifacts.items():
        check_file(path,data['artifacts'][key])
    bundles.append({'workspace':workspace,'identity':identity,'source':git(desktop,'rev-parse','HEAD'),'receipt_sha256':receipt_sha,'app_sha256':data['artifacts']['bundle']['Contents/MacOS/yijie-desktop']['sha256'],'bundle_files':len(data['artifacts']['bundle']),'source_files':len(data['inputs']['sources']),'worker_source_files':len(data['inputs']['workerSources']),'mismatches':len(failures)-before,'launched_this_audit':False,'daily_prepare_only':identity=='com.yijie.ai'})

result_file = EVIDENCE/'s4ad-retained-delivery-result.json'
check_file(ROOT/'feat164-s4ad-audit-20261027/feat164-retained-delivery-run1/result.json',digest(result_file))
result = read(result_file)
require(result['receipt'] == result['replayed_receipt'], 'same durable cancellation receipt')
require(result['dispatch_attempts'] == 0 and result['model_http'] == 0 and result['runtime_started'] is False and result['message_rows_retained'] == 1, 'retained normal cancellation invariants')
require('1 passed; 0 failed; 0 ignored' in (EVIDENCE/'s4ad-retained-delivery-test.log').read_text(), 'actual native positive executed')
require('1 passed' in (EVIDENCE/'s4ad-retained-consumer.log').read_text(), 'actual consumer positive executed')
require(all(x['exit_code'] == 0 for x in read(EVIDENCE/'s4ad-test-validation.json')), 'retained test source checks')
owner = read(AUDIT/'owner-acceptance.json')
require(owner['acceptance_status']=='ACCEPTED_SAFE_LAYERED_SUBSTITUTE' and owner['original_app_positive_execution_status']=='NOT RUN', 'owner acceptance/raw execution distinction')

record = {
    'feature':'FEAT-164','at':datetime.datetime.now().astimezone().isoformat(),
    'status':'PASS' if not failures else 'FAIL','failures':failures,
    'prior_evidence_indices':indices,'indexed_file_references':sum(x['indexed_files'] for x in indices),
    'additional_private_facts':sum(x['additional_private_facts'] for x in indices),
    'sources':sources,'test_commit':source_binding['test_commit'],'test_only_paths':test_paths,
    'bundles':bundles,'native_receipt_and_replay_match':result['receipt']==result['replayed_receipt'],
    'owner_acceptance_sha256':digest(AUDIT/'owner-acceptance.json'),
    'full_app_never_sent_positive_execution':'NOT RUN',
    'model_http_added':0,'loopback_model_http_added':0,'daily_open_or_migration':False,
    'scope_note':'Fresh read-only binding audit, not new App/E2E execution. Original source/time, raw failures and accepted substitution remain explicit. Environment hashes retained in prior canonical receipts; no claim of a new canonical environment check.',
}
(AUDIT/'closure-binding.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['status','indexed_file_references','additional_private_facts','failures']},ensure_ascii=False))
raise SystemExit(0 if not failures else 1)
