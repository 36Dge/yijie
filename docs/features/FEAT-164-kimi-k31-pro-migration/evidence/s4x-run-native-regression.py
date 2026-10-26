import os,subprocess,json,re,datetime
from pathlib import Path
w=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');a=w/'feat164-s4x-audit-20261026';d=w/'feat164-s4x-daily-candidate-20261026/yijie-desktop'
e={k:os.environ[k] for k in ['PATH','HOME','TMPDIR','CARGO_HOME','RUSTUP_HOME','SDKROOT','DEVELOPER_DIR'] if k in os.environ};e.update(CARGO_NET_OFFLINE='true',CARGO_BUILD_JOBS='4',YIJIE_ENV='local',YIJIE_LOCAL_PROFILE='demo_fast',YIJIE_CHAT_MODELS_ENABLED='true',YIJIE_KIMI_K31_PRO_CANDIDATE='true',YIJIE_KIMI_K31_EXECUTION_PAUSED='false')
base=['cargo','test','--offline','--locked','--manifest-path','src-tauri/Cargo.toml','--features','kimi-k31-pro-candidate','--lib']
skips=['feat164_surfaces','feat164_delivery','feat164_native_host_boundary','chat::schedules::model_retirement_tests::','chat::database::isolated_model_migration::','chat::schedules::feat164_natural_plan_tests::','feat164_daily_identity_and_flags_are_closed']
listed=[line[:-6] for line in (a/'native-test-inventory.log').read_text().splitlines() if line.endswith(': test')];selected=[x for x in listed if not any(k in x for k in skips)];assert len(selected)==20,selected
checks=[('s2-native-delivery',base+['feat164_delivery','--','--test-threads=1'],12),('s2-native-recovery',base+['feat164','--',*sum([['--skip',k] for k in skips],[]),'--test-threads=1'],20)]
results=[]
for name,cmd,want in checks:
 start=datetime.datetime.now().astimezone().isoformat();p=subprocess.run(cmd,cwd=d,env=e,capture_output=True,text=True);raw=p.stdout+p.stderr;(a/(name+'.log')).write_text(raw);m=re.search(r'test result: ok\. (\d+) passed; 0 failed; (\d+) ignored',raw);passed=int(m[1]) if m else 0;skipped=int(m[2]) if m else None;r={'name':name,'command':cmd,'started_at':start,'finished_at':datetime.datetime.now().astimezone().isoformat(),'exit_code':p.returncode,'passed':passed,'ignored':skipped,'expected':want};results.append(r);(a/'native-controls.json').write_text(json.dumps(results,indent=2)+'\n');print(r,flush=True)
 if p.returncode or passed!=want or skipped:raise SystemExit(1)
p=subprocess.run(['node','scripts/feat164-s3-conformance.mjs',str(a/'s3-controls')],cwd=d,env=e,capture_output=True,text=True);(a/'s3-driver.log').write_text(p.stdout+p.stderr);print('S3 driver',p.returncode,p.stdout,flush=True);raise SystemExit(p.returncode)
