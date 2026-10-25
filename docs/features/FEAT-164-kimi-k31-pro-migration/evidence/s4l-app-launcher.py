import os,sys,subprocess,json,datetime,hashlib
from pathlib import Path
r=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');d=r/'feat164-s4k-qualification-20261026/yijie-desktop';e=r/'yijie/docs/features/FEAT-164-kimi-k31-pro-migration/evidence'
phase=sys.argv[1];assert phase in ['active','paused','reopen'];f=d/'.local/feat164-s4k-fixture'
for name in ['kimi','minimax']:assert (f/name).read_text()=='feat164-local-dummy\n' and (f/name).stat().st_mode & 0o777==0o600
env={k:os.environ[k] for k in ['PATH','HOME','TMPDIR','CARGO_HOME','RUSTUP_HOME','SDKROOT','DEVELOPER_DIR','PKG_CONFIG_PATH'] if k in os.environ};env.update(YIJIE_KIMI_K31_CALL_SURFACES='media',YIJIE_DEMO_FAST_PROVIDER_KEY_FILE=str(f/'minimax'),YIJIE_KIMI_API_KEY_FILE=str(f/'kimi'),YIJIE_PERMISSION_VERIFICATION_BASE_URL='http://127.0.0.1:18083/v1',CARGO_NET_OFFLINE='true',GOTOOLCHAIN='local',GOPROXY='off',GOSUMDB='off',npm_config_offline='true',YIJIE_KIMI_K31_EXECUTION_PAUSED='true' if phase=='paused' else 'false');env['YIJIE_WORKER_TARGET_DIR']=str(r/'feat164-s4i-worker-build-20261025/target');env['PATH']='/Users/jack/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.5.darwin-arm64/bin:'+env['PATH']
cmd=['bash','scripts/run-local-demo-fast.sh','--packaged','--kimi-k31-pro','--reopen'];log=e/f's4l-{phase}-app-launch.log';assert not log.exists()
info={'started_at':datetime.datetime.now().astimezone().isoformat(),'phase':phase,'command':cmd,'local_adapter_endpoint':True,'real_model_mode':False,'real_model_http_added':0}
print('Canonical same-build '+phase+' startup; log '+str(log),flush=True)
with log.open('wb') as stream:
 result=subprocess.Popen(cmd,cwd=d,env=env,stdout=stream,stderr=subprocess.STDOUT)
 print('canonical child PID',result.pid,flush=True)
 result.wait()
info.update(exit_code=result.returncode,finished_at=datetime.datetime.now().astimezone().isoformat(),log_sha256=hashlib.sha256(log.read_bytes()).hexdigest());(e/f's4l-{phase}-app-exit.json').write_text(json.dumps(info,indent=2)+'\n');print('App normal wrapper return',result.returncode,flush=True);raise SystemExit(result.returncode)
