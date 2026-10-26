from pathlib import Path
import os,sys,json,time,hashlib,subprocess,selectors,struct,datetime,shutil,sqlite3
r=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');a=r/'feat164-s4m-audit-20261026';e=r/'yijie/docs/features/FEAT-164-kimi-k31-pro-migration/evidence';h=a/'credential-free-home';h.mkdir(exist_ok=False)
binary=r/'yijie-codex/.yijie/build/kimi-k31-pro-r4/aarch64-apple-darwin/codex'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(binary)=='3821bb6063825bdb0e30e367757117f7b3bc9bca84f0275cbdef9e9c660e1e5f'
config='''model = "kimi-k3.1-pro"
model_provider = "audit_loopback"
cli_auth_credentials_store = "file"
approval_policy = "never"
sandbox_mode = "read-only"
[analytics]
enabled = false
[feedback]
enabled = false
[features]
hooks = false
plugins = false
apps = false
tool_suggest = false
shell_snapshot = false
[model_providers.audit_loopback]
name = "FEAT164 zero-turn lifecycle audit"
base_url = "http://127.0.0.1:9/v1"
wire_api = "responses"
requires_openai_auth = false
supports_websockets = false
request_max_retries = 0
stream_max_retries = 0
'''
(h/'config.toml').write_text(config)
env={k:os.environ[k] for k in ('PATH','HOME','TMPDIR') if k in os.environ};env.update(CODEX_HOME=str(h),CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED='1',RUST_LOG='codex_app_server=info,codex_app_server_transport=debug')
cmd=[str(binary),'app-server','--listen','stdio://','--strict-config'];result={'started_at':datetime.datetime.now().astimezone().isoformat(),'command':cmd,'binary_sha256':sha(binary),'normal_eof_only':True,'real_model_http_added':0,'turn_start_requests':0,'credential_environment_names':[],'provider_base_url':'http://127.0.0.1:9/v1','run_count':1,'scope':'existing unchanged r4 binary; fresh credential-free home; initialize/initialized only'}
err=(a/'eof-stderr.log').open('wb');p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,env=env,cwd=h);result['pid']=p.pid
request={'method':'initialize','id':1,'params':{'clientInfo':{'name':'feat164_s4m_audit','version':'0.1.0'},'capabilities':{'experimentalApi':False}}}
p.stdin.write((json.dumps(request)+'\n').encode());p.stdin.flush();sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ);output=[];buffer=b'';deadline=time.monotonic()+20;success=False
while time.monotonic()<deadline:
 if not sel.select(min(1,max(0,deadline-time.monotonic()))):continue
 chunk=os.read(p.stdout.fileno(),65536)
 if not chunk:break
 buffer+=chunk
 while b'\n' in buffer:
  line,buffer=buffer.split(b'\n',1)
  if not line:continue
  v=json.loads(line);output.append(v)
  if v.get('id')==1:success='result' in v
 if success:break
if success:p.stdin.write(b'{"method":"initialized","params":{}}\n');p.stdin.flush()
p.stdin.close();result['initialize_ok']=success;result['sent_methods']=['initialize']+(['initialized'] if success else []);start=time.monotonic()
try:result['exit_code']=p.wait(timeout=20)
except subprocess.TimeoutExpired:
 result.update(status='STOP_PENDING',process_retained=True);(e/'s4m-normal-eof-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(1)
err.close();result['normal_exit_elapsed_seconds']=round(time.monotonic()-start,4);(a/'eof-stdout.json').write_text(json.dumps(output,indent=2)+'\n');assert success and result['exit_code']==0
result['databases']=[];snap=a/'fresh-runtime-readonly-snapshot';snap.mkdir()
for db in sorted(h.glob('*.sqlite')):
 files=[Path(str(db)+s) for s in ('','-wal','-shm')];before={str(f):sha(f) for f in files if f.exists()};rec={'name':db.name,'files':{f.name:{'bytes':f.stat().st_size,'sha256':sha(f)} for f in files if f.exists()}}
 shm=Path(str(db)+'-shm')
 if shm.exists() and shm.stat().st_size>=100:
  d=shm.read_bytes();rec.update(mxFrame=struct.unpack_from('<I',d,16)[0],nBackfill=struct.unpack_from('<I',d,96)[0])
 for f in files:
  if f.exists():shutil.copyfile(f,snap/f.name)
 # Only a full snapshot is opened, query-only. No checkpoint or original DB connection.
 conn=sqlite3.connect((snap/db.name).as_uri()+'?mode=ro',uri=True);conn.execute('PRAGMA query_only=ON');rec['snapshot_integrity']=conn.execute('PRAGMA integrity_check').fetchall();conn.close();assert {str(f):sha(f) for f in files if f.exists()}==before
 rec['source_db_wal_shm_unchanged_by_inspection']=True;result['databases'].append(rec)
result['normal_exit_trace']=[line for line in (a/'eof-stderr.log').read_text().splitlines() if any(t in line for t in ['stdin reader finished','processor task exited','outbound router task exited','accept loop stopped','client disconnected'])]
result.update(status='AUDIT_COMPLETE_NOT_TEARDOWN_PASS',manual_checkpoint=False,wal_delete=False,signals_sent=[],finished_at=datetime.datetime.now().astimezone().isoformat())
(e/'s4m-normal-eof-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(e/'s4m-eof-config.toml').write_text(config);print(json.dumps(result,ensure_ascii=False))
