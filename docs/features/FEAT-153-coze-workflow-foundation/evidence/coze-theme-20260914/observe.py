"""Read-only observations of the canonical local workflow API; never record credentials."""
from pathlib import Path
import json,sys,urllib.request
ROOT=Path(__file__).resolve().parents[6]
creds=json.loads((ROOT/'yijie-infra/environments/local/generated/feat-153/private/k-na.json').read_text())
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs): return None
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
def get(path,metadata):
 headers={'Authorization':'Bearer '+creds['token'],'X-Yijie-Run-Epoch':creds['run_epoch'],'Accept':'application/json'}
 if metadata:headers['X-Yijie-Workflow-Metadata']='description-v1'
 req=urllib.request.Request('http://127.0.0.1:18888'+path,headers=headers)
 with opener.open(req,timeout=10) as response:return json.load(response)
path='/v1/workflows?limit=50' if len(sys.argv)<3 else '/v1/workflows/'+sys.argv[2]
old=get(path,False);new=get(path,True)
items=lambda value:value['items'] if 'items' in value else [value]
assert all('description' not in w for w in items(old))
assert [w['workflow_id'] for w in items(old)]==[w['workflow_id'] for w in items(new)]
result={'path':path,'legacy':old,'metadata':new,'legacy_projection_preserved':True}
Path(sys.argv[1]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'count':len(items(new)),'ids':[w['workflow_id'] for w in items(new)][:2],'legacy_projection_preserved':True}))
