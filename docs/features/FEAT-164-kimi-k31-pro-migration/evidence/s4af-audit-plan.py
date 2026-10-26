from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');A=R/'feat164-s4af-audit-20261027';Q=R/'feat164-s4ac-daily-candidate-20261027';D=Q/'yijie-desktop';E=R/'yijie/docs/features/FEAT-164-kimi-k31-pro-migration/evidence'
def sha(p):
 with p.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def git(p,*args):return subprocess.check_output(['git',*args],cwd=p,text=True).strip()
index=json.loads((E/'s4ae-audit-index.json').read_text());assert all(sha(E/n)==v for n,v in index['files'].items())
old=json.loads((E/'s4ac-daily-build-audit.json').read_text());receipt=D/'.local/feat164-daily/packaged-launch-receipt.json';assert sha(receipt)==old['receipt_sha256'];data=json.loads(receipt.read_text());bundle=Path(old['bundle']);assert set(str(p.relative_to(bundle)) for p in bundle.rglob('*') if p.is_file())==set(data['artifacts']['bundle'])
for rel,v in data['artifacts']['bundle'].items():
 p=bundle/rel;s=p.stat();assert sha(p)==v['sha256'] and s.st_size==v['bytes'] and s.st_mode&0o777==v['mode']
for rel,v in data['inputs']['sources'].items():
 p=D/rel;s=p.stat();assert sha(p)==v['sha256'] and s.st_size==v['bytes'] and s.st_mode&0o777==v['mode']
sources={n:{'head':git(Q/n,'rev-parse','HEAD'),'status':git(Q/n,'status','--porcelain')} for n in old['sources']};assert sources==old['sources']
files={}
def read(base,name):
 p=base/name;files[str(p)]={'sha256':sha(p),'lines':len(p.read_text().splitlines())};return p.read_text()
launcher=read(D,'scripts/run-local-demo-fast.sh');native=read(D,'src-tauri/src/chat/sidecar.rs');maintenance=read(D,'src-tauri/src/chat/isolated_model_migration.rs');lifecycle=read(D,'src-tauri/src/lib.rs');aut=read(D,'src-tauri/src/chat/schedules/automatic.rs');ipc=read(D,'src-tauri/src/chat/ipc.rs');db=read(D,'src-tauri/src/chat/database.rs');profile=read(D,'src-tauri/src/feat164_qualification.rs');host=read(Q/'yijie-agent-host','internal/session/store.go');activation=read(Q/'yijie-agent-host','internal/codex/kimi_k31_activation.go');workflow=read(R/'yijie-infra','scripts/workflow-local.py')
assert 'runtime_root="$desktop_root/.local/demo-fast"' in launcher
assert 'if [[ "$kimi_k31_daily" == "true" ]]; then\n  runtime_root="$desktop_root/.local/feat164-daily"\n  host_home="$runtime_root/host-home"\n  codex_home="$runtime_root/codex-home"' in launcher
assert 'YIJIE_AGENT_HOST_HOME="$host_home"' in launcher and 'YIJIE_CODEX_HOME="$codex_home"' in launcher
assert 'if isolated {\n            let host = base.join("host");' in native
assert 'Self::Daily => "demo-fast-v1"' in maintenance
assert maintenance.index('let (id, backup) = snapshot') < maintenance.index('let version = preflight') < maintenance.index('if version < 38')
assert 'SQLITE_OPEN_READ_WRITE' in maintenance and 'migrate_to_target' in maintenance
assert 'modelOperationsV2Bucket' in host and 'store.prepareModelV2Format(tx)' in host
up=workflow[workflow.index('def up():'):workflow.index('def status():')]
assert "'-migrate-local'" in up and "'/usr/local/bin/workflow-local-migrate', 'up'" in up
assert 'make -C "$workspace_root/yijie-infra" workflow-up' in launcher
assert 'write_json(STATE, state)' in workflow[workflow.index('def record('):workflow.index('def candidate(')]
assert 'return ready' in workflow[workflow.index('def status():'):workflow.index('def qualify_pg(')] and 'globals()[args.action]()' in workflow
assert 'future || pending' in (D/'src-tauri/src/chat/mod.rs').read_text() and 'minimax-m3-high-v1' in aut and 'start_scheduled_background' in ipc
for p in ['scripts/kimi-k31-packaged-receipt.mjs','src-tauri/src/single_instance.rs','src-tauri/src/chat/mod.rs','src-tauri/src/chat/schedules/candidate.rs','src-tauri/src/chat/schedules/model_retirement.rs']:read(D,p)
facts=[
 {'id':'CUTOVER-01','classification':'P1 deployment correctness, actual daily not executed','fact':'Daily K31 launcher assigns candidate-local Host and Runtime Homes while retaining original daily Native identity. Native rewrites Homes only for isolated profiles.','impact':'Existing Native-to-Host-to-Runtime mapping continuity is not established; do not activate current daily candidate.','status':'OPEN_DESIGN_FIX_REQUIRED'},
 {'id':'CUTOVER-02','classification':'authorization boundary','fact':'Migration CLI combines backup, copy preflight and actual write; internal snapshot covers conversations.db plus WAL/SHM and two secrets only.','impact':'Separate full cold backup and read-only copy preflight authorization must precede migration authorization; no existing standalone preflight flag.','status':'PLAN_REQUIRED'},
 {'id':'CUTOVER-03','classification':'authorization boundary and deployment prerequisite','fact':'Daily normal launcher calls workflow-up; stopped-stack branch mutates lifecycle/credentials and runs Coze/API migrations. workflow-status also writes state and CLI does not propagate false readiness into nonzero exit. Candidate workspace lacks Infra/Coze.','impact':'Need fail-closed existing-ready-only startup; no implicit workflow init/build/up/migration or silent profile disable.','status':'OPEN_DESIGN_FIX_REQUIRED'},
 {'id':'CUTOVER-04','classification':'zero-model-call boundary','fact':'App native setup can resume automatic scheduled work. K31 execution pause excludes K31 only; enabled MiniMax work may remain eligible.','impact':'No-send first-start gate requires no eligible future/pending work across all models, not only no currently in-flight operation.','status':'PRESTART_INVENTORY_REQUIRED'},
 {'id':'CUTOVER-05','classification':'write authorization boundary','fact':'Native maintenance does not start Host/Runtime. First normal startup can upgrade Host Store and managed Runtime config/catalog, start scheduling and advance local lifecycle facts.','impact':'Authorize Native migration and first-start Host/Runtime writes separately; first start is not read-only.','status':'PLAN_REQUIRED'}]
result={'feature':'FEAT-164','at':datetime.datetime.now().astimezone().isoformat(),'audit_result':'PASS_SOURCE_FACTS_CONFIRMED','daily_activation_readiness':'NO_GO','prior_58_index_files_verified':len(index['files']),'sources':sources,'infra_source':{'head':git(R/'yijie-infra','rev-parse','HEAD'),'status':git(R/'yijie-infra','status','--porcelain')},'daily_bundle_files':len(data['artifacts']['bundle']),'daily_app_sha256':old['app_sha256'],'daily_receipt_sha256':old['receipt_sha256'],'daily_source_inputs_verified':len(data['inputs']['sources']),'missing_candidate_siblings':[n for n in ['yijie-infra','yijie-coze'] if not (Q/n).exists()],'reviewed_files':files,'findings':facts,'daily_data_accessed':False,'daily_data_snapshot_or_preflight_performed':False,'app_launch':False,'workflow_commands_run':False,'runtime_core_or_patch_changed':False,'model_http_added':0}
(A/'source-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['audit_result','daily_activation_readiness','prior_58_index_files_verified','daily_bundle_files','daily_source_inputs_verified','daily_data_accessed']}))
