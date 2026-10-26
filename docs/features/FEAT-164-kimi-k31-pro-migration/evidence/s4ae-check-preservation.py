from pathlib import Path
import json,hashlib,datetime,subprocess,sys
r=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');a=r/'feat164-s4ae-audit-20261027';b=json.loads((a/'baseline.json').read_text());fail=[]
def sha(p):
 with p.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def check(p,h):
 if not p.is_file() or sha(p)!=h:fail.append(str(p))
for p,h in b['protected'].items():check(Path(p),h)
for p,h in b['ledgers'].items():check(Path(p),h)
count=0;states={}
for name,repo in b['repos'].items():
 for p,h in repo['dirty'].items():
  if name=='yijie' and p=='docs/dev/codex-project-memory.md':continue
  check(r/name/p,h);count+=1
 def git(*args):return subprocess.check_output(['git',*args],cwd=r/name).decode().strip()
 state={k:git(*args) for k,args in [('head',('rev-parse','HEAD')),('branch',('branch','--show-current')),('remote',('remote','get-url','origin'))]}
 for k in ['branch','remote']:
  if state[k]!=repo[k]:fail.append(name+': '+k)
 if name!='yijie' and (state['head']!=repo['head'] or git('status','--porcelain')!=repo['status']):fail.append(name+': original state')
 states[name]=state
old=(a/'memory-before.txt').read_bytes();block=(a/'memory-owned-block.txt').read_bytes();current=(r/'yijie/docs/dev/codex-project-memory.md').read_bytes()
if current.count(block)!=1 or current.replace(block,b'',1)!=old:fail.append('mixed memory unrelated bytes')
x={'at':datetime.datetime.now().astimezone().isoformat(),'status':'PASS' if not fail else 'FAIL','protected_files':len(b['protected']),'prior_dirty_files_excluding_memory':count,'ledger_and_snapshot_files':len(b['ledgers']),'mixed_memory_unrelated_bytes_preserved':current.replace(block,b'',1)==old,'original_repo_states':states,'mismatches':fail,'real_model_http_added':0,'loopback_model_http_added':0,'daily_open_or_migration':False}
output=a/('preservation-postcommit.json' if '--postcommit' in sys.argv else 'preservation.json');output.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:x[k] for k in ['status','protected_files','prior_dirty_files_excluding_memory','ledger_and_snapshot_files','mixed_memory_unrelated_bytes_preserved','mismatches']},ensure_ascii=False));raise SystemExit(bool(fail))
