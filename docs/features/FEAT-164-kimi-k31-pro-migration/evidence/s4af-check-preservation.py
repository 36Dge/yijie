from pathlib import Path
import subprocess,json,hashlib,datetime,sys
R=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');A=R/'feat164-s4af-audit-20261027';B=json.loads((A/'baseline.json').read_text());fail=[]
def sha(p):
 with p.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
def git(p,*args):return subprocess.check_output(['git',*args],cwd=p,text=True).strip()
count=0
for name,s in B['repos'].items():
 root=R/name
 for p,h in s['dirty'].items():
  if name=='yijie' and p=='docs/dev/codex-project-memory.md':continue
  count+=1
  if not (root/p).is_file() or sha(root/p)!=h:fail.append(name+'/'+p)
 for k,args in [('branch',('branch','--show-current')),('remote',('remote','get-url','origin'))]:
  if git(root,*args)!=s[k]:fail.append(name+':'+k)
 if name!='yijie' and (git(root,'rev-parse','HEAD')!=s['head'] or git(root,'status','--porcelain')!=s['status']):fail.append(name+': state')
for p,h in B['ledgers'].items():
 if sha(Path(p))!=h:fail.append('ledger:'+p)
for name,s in B['qualified'].items():
 p=R/'feat164-s4ac-daily-candidate-20261027'/name
 if git(p,'rev-parse','HEAD')!=s['head'] or git(p,'status','--porcelain')!=s['status']:fail.append('qualified:'+name)
old=(A/'memory-before.txt').read_bytes();block=(A/'memory-owned-block.txt').read_bytes();current=(R/'yijie/docs/dev/codex-project-memory.md').read_bytes();same=current.count(block)==1 and current.replace(block,b'',1)==old
if not same:fail.append('mixed memory')
result={'at':datetime.datetime.now().astimezone().isoformat(),'status':'PASS' if not fail else 'FAIL','existing_dirty_files_excluding_memory':count,'ledgers_and_snapshots':len(B['ledgers']),'mixed_memory_unrelated_bytes_preserved':same,'qualified_sources_unchanged':not any(x.startswith('qualified:') for x in fail),'mismatches':fail,'daily_data_accessed_or_hashed':False,'note':'Workspace/source/ledger protection only. No claim of freshly inspected daily data; no daily operation was executed.'}
(A/('preservation-postcommit.json' if '--postcommit' in sys.argv else 'preservation.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False));raise SystemExit(bool(fail))
