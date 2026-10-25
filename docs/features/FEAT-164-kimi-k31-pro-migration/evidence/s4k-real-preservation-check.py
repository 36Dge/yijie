from pathlib import Path
import json,hashlib,subprocess,tempfile,datetime,sys
r=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');e=r/'yijie/docs/features/FEAT-164-kimi-k31-pro-migration/evidence';a=r/'feat164-s4k-audit-20261026';b=json.loads((e/'s4k-start-baseline.json').read_text())
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args])
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
out={'at':datetime.datetime.now().astimezone().isoformat(),'repositories':[],'protected_dirty_files':0}
for name,v in b['repos'].items():
 p=r/name;head=git(p,'rev-parse','HEAD').decode().strip();owned=name=='yijie-desktop';patch=git(p,'diff','--binary',v['head'],head) if owned else b''
 if name not in ['yijie-desktop','yijie']:assert head==v['head'],name
 with tempfile.TemporaryDirectory(prefix='feat164-s4k-check-') as t:
  tmp=Path(t);changed=git(p,'diff','--name-only',v['head'],head).decode().splitlines() if owned else []
  for f in set(v['files'])|set(changed):
   if (p/f).is_file():dst=tmp/f;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((p/f).read_bytes())
  if patch:subprocess.run(['git','apply','--reverse'],cwd=tmp,input=patch,check=True,stderr=subprocess.PIPE)
  if name=='yijie':
   f='docs/dev/codex-project-memory.md';old=(a/'memory-before.md').read_text();now=(p/f).read_text();assert old[:old.index('## FEAT-164 ')]==now[:now.index('## FEAT-164 ')];assert old[old.index('## FEAT-163 '):]==now[now.index('## FEAT-163 '):];(tmp/f).write_text(old)
  for f,h in v['files'].items():assert sha(tmp/f)==h,(name,f)
 assert not git(p,'diff','--cached','--name-only');assert git(p,'branch','--show-current').decode().strip()==v['branch'];assert git(p,'remote','get-url','origin').decode().strip()==v['remote'];out['repositories'].append({'repository':name,'head':head,'dirty_files_preserved':len(v['files']),'index_empty':True,'branch_remote_unchanged':True});out['protected_dirty_files']+=len(v['files'])
for key,base in [('old_evidence',e),('resources',r),('daily_databases',Path('/'))]:
 for p,h in b[key].items():assert sha(base/p)==h,(key,p)
 out[key+'_unchanged']=len(b[key])
for root,files in b['old_bundles'].items():
 for p,h in files.items():assert sha(Path(root)/p)==h,('bundle',p)
out['old_bundle_files_unchanged']=sum(len(v) for v in b['old_bundles'].values())
for p,h in b['candidate_data']['files'].items():assert sha(a/'candidate-app-data'/p)==h,('backup',p)
out['candidate_backup_files_unchanged']=len(b['candidate_data']['files'])
out['current_candidate_data_audit']='s4k-real-data-audit.json: three saved completed turns, protected history retained, one explained paused-plan next_at cache advancement'
q=r/'feat164-s4k-qualification-20261026'
for name in b['qualification']:assert not git(q/name,'status','--porcelain'),name
ps=subprocess.check_output(['ps','-axo','pid=,comm='],text=True);owned=[x for x in ps.splitlines() if 'FEAT-164.app/' in x or '/kimi-k31-pro-r4/' in x or '/chat-models-web-sources/' in x];assert not owned,owned
out.update(real_model_http_added=3,candidate_app_started=True,active_candidate_processes=owned,app_state='normally exited; no candidate children remain',push=False)
ledger=json.loads((e/'g2v-real-budget-ledger-r3.json').read_text());assert len(ledger['requests'])==5 and ledger['meter_state']=='stopped_normally' and ledger['halted'] and ledger['charged_upper_micro_cny']==14679001;out['unused_authorized_http']=0
receipt=json.loads((e/'s4k-app-build-receipt.json').read_text());bundle=q/'yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI FEAT-164.app'
for p,h in receipt['inputs']['sources'].items():assert sha(q/'yijie-desktop'/p)==h['sha256']
for p,h in receipt['artifacts']['bundle'].items():assert sha(bundle/p)==h['sha256']
out['canonical_source_and_bundle_match']=True
ports=subprocess.run(['lsof','-nP','-iTCP:18083','-sTCP:LISTEN'],capture_output=True,text=True);assert ports.returncode==1 and not ports.stdout;out['real_meter_port_closed']=True
dest=a/'real-post-commit-preservation.json' if len(sys.argv)>1 else e/'s4k-real-preservation-audit.json';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
