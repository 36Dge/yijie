import os,json,pathlib,tempfile,subprocess,socket,time,uuid,urllib.request,urllib.error,signal
base=pathlib.Path(__file__).parent
root=pathlib.Path(tempfile.mkdtemp(prefix='feat155-b3b-smoke-',dir='/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/.local')).resolve()
owner='00000000-0000-4000-8000-000000000155';tenant='00000000-0000-4000-8000-000000000156'
home=root/'host';runtime_home=root/'runtime';workspace=root/'scheduled-workspaces'/tenant/owner
for p in [home,runtime_home,workspace]:p.mkdir(mode=0o700,parents=True)
wid=str(uuid.uuid4());(workspace/wid).mkdir(mode=0o700)
artifact=pathlib.Path('/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/build/input-only/aarch64-apple-darwin')
result={'kind':'real-host-runtime-no-model','root':str(root),'model_turn_posts':0,'runs':[]}
def cycle(mapping=None):
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 nonce=str(uuid.uuid4()); env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','HOME':str(root),'TMPDIR':str(base),'YIJIE_ENV':'local','YIJIE_LOCAL_PROFILE':'demo_fast','YIJIE_MODEL_PROVIDER':'minimax','YIJIE_MINIMAX_API_KEY':'synthetic-unused-no-model-key','YIJIE_RUNTIME_PERMISSIONS_ENABLED':'true','YIJIE_AGENT_HOST_PORT':str(port),'YIJIE_AGENT_HOST_HOME':str(home),'YIJIE_CODEX_HOME':str(runtime_home),'YIJIE_CODEX_BINARY':str(artifact/'codex'),'YIJIE_CODEX_MANIFEST':str(artifact/'runtime-manifest.json'),'YIJIE_AGENT_HOST_PARENT_PID':str(os.getpid()),'YIJIE_AGENT_HOST_INSTANCE_NONCE':nonce,'YIJIE_SCHEDULED_CANDIDATE':json.dumps({'schema_version':1,'owner_user_id':owner,'tenant_id':tenant,'workspace_root':str(workspace)})}
 log=open(root/f'host-{len(result["runs"])+1}.log','w');p=subprocess.Popen([str(base/'desktop-host')],env=env,stdout=log,stderr=subprocess.STDOUT)
 run={'pid':p.pid,'nonce':nonce,'requests':[]};result['runs'].append(run);token=None
 def request(method,path,data=None):
  headers={'Content-Type':'application/json'}
  if token:headers['Authorization']='Bearer '+token
  q=urllib.request.Request(f'http://127.0.0.1:{port}'+path,data=None if data is None else json.dumps(data).encode(),headers=headers,method=method)
  try:
   with urllib.request.urlopen(q,timeout=15) as response:status=response.status;value=json.load(response)
  except urllib.error.HTTPError as e:status=e.code;value=json.load(e)
  run['requests'].append({'method':method,'path':path,'status':status,'value':value});return status,value
 try:
  deadline=time.monotonic()+45
  while True:
   if p.poll() is not None:raise RuntimeError('Host exited before readiness')
   try:
    status,value=request('GET','/readyz')
    if status==200:break
   except (OSError,urllib.error.URLError):pass
   if time.monotonic()>deadline:raise RuntimeError('readiness deadline')
   time.sleep(.2)
  candidates=list(home.glob('*token*'));assert len(candidates)==1,[q.name for q in candidates]
  token=candidates[0].read_text().strip()
  status,cap=request('GET','/v1/scheduled-plan-draft-capability');assert status==200 and cap['available'],cap
  if mapping is None:
   task=str(uuid.uuid4());status,receipt=request('POST','/v1/scheduled-plan-draft-sessions',{'schema_version':1,'policy_version':1,'task_id':task,'workspace_id':wid});assert status==200,receipt
  else:task=mapping['task_id']
  status,read=request('GET','/v1/scheduled-plan-draft-session-mappings/'+task);assert status==200 and read['mapping_state']=='bound' and read['responding_host_instance_id']==nonce,read
  if mapping:
   assert {k:v for k,v in mapping.items() if k!='responding_host_instance_id'}=={k:v for k,v in read.items() if k!='responding_host_instance_id'}
  # Explicit, no-model resume is recorded separately. Never POST a model turn.
  status,resume=request('POST','/v1/scheduled-plan-draft-sessions/'+read['agent_session_id']+'/resume',{'schema_version':1,'policy_version':1})
  run['explicit_resume_status']=status
  if not mapping:assert status==200,resume
  else:
   assert status==503 and resume['code']=='operation_unknown',resume
   run['cold_empty_history']='unavailable_preserved'
   status,session=request('GET','/v1/agent-sessions/'+read['agent_session_id']);assert status==200 and session['session']['state']=='idle',session
   status,again=request('GET','/v1/scheduled-plan-draft-session-mappings/'+task);assert status==200 and again==read,again
  run['mapping_preserved']=True
  return read
 finally:
  if p.poll() is None:p.send_signal(signal.SIGTERM)
  try:run['exit_code']=p.wait(timeout=45)
  except subprocess.TimeoutExpired:
   run['normal_stop_pending']=True;(base/'native-smoke-result.json').write_text(json.dumps(result,indent=2));p.wait()
  log.close()
try:
 first=cycle();cycle(first);result['passed']=all(r.get('exit_code')==0 for r in result['runs'])
except Exception as e:result['passed']=False;result['failure']=str(e)
finally:(base/'native-smoke-result.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'passed':result['passed'],'failure':result.get('failure'),'runs':len(result['runs']),'root':str(root)}))
raise SystemExit(0 if result['passed'] else 1)
