from pathlib import Path
import subprocess,json,hashlib,datetime
b=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');a=b/'feat164-s4ac-audit-20261027';q=b/'feat164-s4ac-daily-candidate-20261027';f=b/'yijie/docs/features/FEAT-164-kimi-k31-pro-migration/evidence'
sha=lambda x:hashlib.sha256(x).hexdigest()
def git(repo,*args):return subprocess.check_output(['git',*args],cwd=q/repo)
indices=[]
for phase in ['s4s','s4t','s4u','s4v','s4w','s4x','s4y','s4z','s4aa','s4ab']:
 p=f/(phase+'-audit-index.json');d=json.loads(p.read_text());files=d['files'];rows=[(Path(x['path']),x['sha256']) for x in files] if isinstance(files,list) else [(f/n,h) for n,h in files.items()]
 failures=[str(p) for p,h in rows if not p.is_file() or sha(p.read_bytes())!=h];indices.append({'phase':phase,'index_sha256':sha(p.read_bytes()),'files':len(rows),'mismatches':failures})
old={'yijie-desktop':'9f5814fec6cd071d39f0c12f8f48097ce661cb6a','yijie-agent-host':'8cd6bccbdc1ac3906aea53d95441299f7cfefcce','yijie-contracts':'ca06d0999c9a08afe80ab3f34a537d492b830ac7'}
deltas={}
for repo,base in old.items():
 head=git(repo,'rev-parse','HEAD').decode().strip();names=git(repo,'diff','--name-only',base,head).decode().splitlines();files={}
 for n in names:
  new=git(repo,'show',head+':'+n);oldp=subprocess.run(['git','show',base+':'+n],cwd=q/repo,capture_output=True)
  files[n]={'old_sha256':sha(oldp.stdout) if oldp.returncode==0 else None,'new_sha256':sha(new)}
 deltas[repo]={'from':base,'to':head,'changed':files}
# Source-domain binding, not a claim that old binaries were rebuilt or rerun.
paths=['src/domain','src/api','src/composables','src/components','src/pages','src/stores','src-tauri/src/chat/models.rs','src-tauri/src/chat/model_repository.rs','src-tauri/src/chat/model_recovery.rs','src-tauri/src/chat/model_delivery.rs','src-tauri/src/chat/schedules','src-tauri/src/chat/migrations.rs','src-tauri/src/chat/database.rs']
d='yijie-desktop';files=git(d,'ls-files',*paths).decode().splitlines();equal=[];different=[]
for n in files:
 if '.test.' in n or n.endswith('_tests.rs'):continue
 one=git(d,'show',old[d]+':'+n);two=(q/d/n).read_bytes();(equal if one==two else different).append({'path':n,'sha256':sha(two)})
# Exact c98 App product equivalence: only one frontend test may differ.
appdelta=git(d,'diff','--name-only','c98eddfafb789520b4939bdca95bf8b27f28b7b6','HEAD').decode().splitlines()
assert appdelta==['src/domain/conversation-native-view.test.ts']
record={'at':datetime.datetime.now().astimezone().isoformat(),'source_commits':json.loads((a/'setup.json').read_text()),'prior_evidence_indices':indices,'prior_evidence_count':sum(x['files'] for x in indices),'deltas_since_s4w':deltas,'desktop_business_domains':{'unchanged':equal,'changed':different},'actual_isolated_app':{'source':'c98eddfafb789520b4939bdca95bf8b27f28b7b6','app_sha256':'179dbd187220694d4666af5822466572f3b245a911501991cb0194f4308db195','difference_from_ea':appdelta,'product_equivalent':True},'qualification_rule':'Prior evidence retains actual source and time. Unchanged domains reuse narrowly; daily identity/migration changes use report51 four natural matrix plus current focused checks; Host source URL only uses report54 and current immutable checks. Not a fresh full end-to-end run.','search_quality':'OWNER_EXCLUDED','real_http_added':0,'status':'PASS' if not different and all(not x['mismatches'] for x in indices) else 'REVIEW_REQUIRED'}
(a/'source-evidence-binding.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':record['status'],'count':record['prior_evidence_count'],'equal_domains':len(equal),'changed_domains':different,'index_mismatches':[x for x in indices if x['mismatches']]},indent=2))
