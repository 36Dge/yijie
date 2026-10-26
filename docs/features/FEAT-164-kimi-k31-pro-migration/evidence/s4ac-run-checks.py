import os,json,subprocess,datetime,re
from pathlib import Path
b=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');a=b/'feat164-s4ac-audit-20261027';d=b/'feat164-s4ab-qualification-20261027/yijie-desktop';h=d.parent/'yijie-agent-host'
e={k:os.environ[k] for k in ['PATH','HOME','TMPDIR','CARGO_HOME','RUSTUP_HOME','SDKROOT','DEVELOPER_DIR'] if k in os.environ}
e['PATH']='/Users/jack/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.5.darwin-arm64/bin:'+e['PATH']
e.update(CARGO_NET_OFFLINE='true',CARGO_BUILD_JOBS='2',GOPROXY='off',GOSUMDB='off',GOTOOLCHAIN='local',npm_config_offline='true',YIJIE_ENV='local',YIJIE_LOCAL_PROFILE='demo_fast',YIJIE_CHAT_MODELS_ENABLED='true',YIJIE_KIMI_K31_PRO_CANDIDATE='true',VITE_YIJIE_ENV='local',VITE_YIJIE_LOCAL_PROFILE='demo_fast',VITE_YIJIE_CHAT_MODELS_ENABLED='true',VITE_YIJIE_KIMI_K31_PRO_CANDIDATE='true')
prev=json.loads((b/'feat164-s4u-audit-20261026/renderer-business-state.log').read_text());files=[str(Path(t['name']).relative_to(b/'feat164-s4t-media-qualification-20261026/yijie-desktop')) for t in prev['testResults']]
checks=[('renderer-business',d,['pnpm','exec','vitest','run','--maxWorkers=2','--reporter=json',*files]),('daily-profile',d,['node','--test','scripts/tests/feat164-daily-profile.test.mjs']),('generation',d,['node','scripts/check-feat164-generation.mjs',str(a/'generation')])]
for c in json.loads((b/'feat164-s4w-audit-20261026/host-controls.json').read_text()):checks.append((c['name'],h,c['command']))
base=['cargo','test','--offline','--locked','--manifest-path','src-tauri/Cargo.toml','--features','kimi-k31-pro-candidate','--lib']
checks += [('s2-native-delivery',d,base+['feat164_delivery','--','--test-threads=1']),('s2-native-recovery',d,base+['feat164','--',*sum([['--skip',k] for k in ['feat164_surfaces','feat164_delivery','feat164_native_host_boundary','chat::schedules::model_retirement_tests::','chat::database::isolated_model_migration::','chat::schedules::feat164_natural_plan_tests::']],[]),'--test-threads=1']),('s3-native',d,['node','scripts/feat164-s3-conformance.mjs',str(a/'s3-controls')])]
results=[]
for name,root,cmd in checks:
 start=datetime.datetime.now().astimezone().isoformat()
 with (a/(name+'.log')).open('x') as f:p=subprocess.run(cmd,cwd=root,env=e,stdout=f,stderr=subprocess.STDOUT)
 results.append({'name':name,'cwd':str(root),'command':cmd,'started_at':start,'finished_at':datetime.datetime.now().astimezone().isoformat(),'exit_code':p.returncode})
 (a/'current-checks.json').write_text(json.dumps(results,indent=2)+'\n');print(name,p.returncode,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
