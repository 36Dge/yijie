"""Read the authorized native AX surface; scan secrets in memory, persist workflow-only evidence."""
from pathlib import Path
import subprocess,json,stat,sys,time
ROOT=Path('/Users/jack/Downloads/Personal_Info/CrossBSD')
helper='/tmp/feat153-dev-ui-assist-11566-v2'
raw=subprocess.check_output([helper,'snapshot'],text=True)
assert len(raw.encode())<1048576
matches={}
for name in ['k-na','k-ac']:
 p=ROOT/('yijie-infra/environments/local/generated/feat-153/private/'+name+'.json')
 s=p.lstat();assert stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o600 and s.st_size<=1024
 token=json.loads(p.read_text())['token'];matches[name]=raw.count(token)
assert sum(matches.values())==0
d=json.loads(raw)
kept=[];skip_depth=None
for n in d['nodes']:
 if skip_depth is not None and n['depth']<=skip_depth:skip_depth=None
 if n.get('description')=='主导航':skip_depth=n['depth']
 if skip_depth is None:kept.append(n)
d['nodes']=kept
d['credential_matches']=matches;d['observed_at_ms']=int(time.time()*1000)
d['scope']='Actual AX roles, labels, values and focus only; no page heap/MessagePort claim'
out=Path(__file__).with_name(sys.argv[1]);assert out.suffix=='.json'
with out.open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2)
print(json.dumps({'path':str(out),'credential_matches':matches,'focused':[n for n in d['nodes'] if n.get('focused')=='1']},ensure_ascii=False))
