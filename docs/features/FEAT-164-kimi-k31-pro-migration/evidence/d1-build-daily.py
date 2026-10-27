import os,json,subprocess,datetime
from pathlib import Path
b=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');a=b/'feat164-d1-audit-20261027';d=b/'feat164-d1-candidate-20261027/yijie-desktop'
e={k:os.environ[k] for k in ['PATH','HOME','TMPDIR','CARGO_HOME','RUSTUP_HOME','SDKROOT','DEVELOPER_DIR'] if k in os.environ}
e['PATH']='/Users/jack/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.5.darwin-arm64/bin:'+e['PATH']
e.update(CARGO_NET_OFFLINE='true',CARGO_BUILD_JOBS='4',GOPROXY='off',GOSUMDB='off',GOTOOLCHAIN='local',npm_config_offline='true')
assert not (a/'daily-canonical-build.log').exists()
(a/'daily-build-environment.json').write_text(json.dumps(e,indent=2)+'\n')
c=['bash','scripts/run-local-demo-fast.sh','--packaged','--kimi-k31-daily','--prepare-only'];start=datetime.datetime.now().astimezone().isoformat()
with (a/'daily-canonical-build.log').open('x') as f:p=subprocess.run(c,cwd=d,env=e,stdout=f,stderr=subprocess.STDOUT)
r={'command':c,'started_at':start,'finished_at':datetime.datetime.now().astimezone().isoformat(),'exit_code':p.returncode,'app_launch':False,'model_http':0,'actual_daily_database_open':False}
(a/'daily-canonical-build.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
raise SystemExit(p.returncode)
