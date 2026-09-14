"""Verify immutable public local editor bytes and headers; never record credentials."""
from pathlib import Path
from hashlib import sha256
import json,sys,time,urllib.request
root=Path(__file__).resolve().parents[6]
dist=root/'yijie-coze/bin/workflow-editor/dist'
raw=(dist/'manifest.json').read_bytes(); manifest=json.loads(raw)
secrets=[json.loads((root/'yijie-infra/environments/local/generated/feat-153/private'/name).read_text())['token'].encode() for name in ('k-na.json','k-ac.json')]
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
count=0; total=0
for entry in manifest['files']:
 data=(dist/entry['path']).read_bytes()
 assert len(data)==entry['bytes'] and sha256(data).hexdigest()==entry['sha256']
 assert not any(secret in data for secret in secrets)
 count+=1; total+=len(data)
with opener.open('http://127.0.0.1:18888/editor/',timeout=10) as response:
 body=response.read(); headers=dict(response.headers)
assert body==(dist/'index.html').read_bytes()
csp=headers['Content-Security-Policy']
assert "connect-src 'none'" in csp and "worker-src 'none'" in csp
assert 'unsafe-eval' not in csp and 'wasm-unsafe-eval' not in csp
result={'observed_at_ms':int(time.time()*1000),'manifest_sha256':sha256(raw).hexdigest(),'source_digest':manifest['source_digest'],'asset_count':count,'total_bytes':total,'assets_match_manifest':True,'machine_credential_matches':0,'served_entry_match':True,'headers':headers,'actual_app_qualification':'recorded separately; this is not a UI or heap scan'}
with open(sys.argv[1],'x') as out:json.dump(result,out,ensure_ascii=False,indent=2);out.write('\n')
print(json.dumps({key:result[key] for key in ('manifest_sha256','source_digest','asset_count','assets_match_manifest','machine_credential_matches','served_entry_match')}))
