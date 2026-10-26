import os,subprocess,json,re,datetime,hashlib
from pathlib import Path
w=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');a=w/'feat164-s4x-audit-20261026';d=w/'feat164-s4x-daily-candidate-20261026/yijie-desktop'
env={k:os.environ[k] for k in ['PATH','HOME','TMPDIR','CARGO_HOME','RUSTUP_HOME','SDKROOT','DEVELOPER_DIR'] if k in os.environ};env.update(CARGO_NET_OFFLINE='true',CARGO_BUILD_JOBS='4',YIJIE_ENV='local',YIJIE_LOCAL_PROFILE='demo_fast',YIJIE_CHAT_MODELS_ENABLED='true')
results=[]
def check(name,selector,flags,feature=True,ignored=False):
 cmd=['cargo','test','--offline','--locked','--manifest-path','src-tauri/Cargo.toml','--lib']+(['--features','kimi-k31-pro-candidate'] if feature else [])+[selector,'--','--exact','--nocapture','--test-threads=1']+(['--ignored'] if ignored else [])
 start=datetime.datetime.now().astimezone().isoformat()
 with (a/(name+'.log')).open('w') as log:p=subprocess.run(cmd,cwd=d,env={**env,**flags},stdout=log,stderr=subprocess.STDOUT)
 raw=(a/(name+'.log')).read_text();ok=p.returncode==0 and 'test result: ok. 1 passed; 0 failed; 0 ignored' in raw;r={'name':name,'command':cmd,'started_at':start,'finished_at':datetime.datetime.now().astimezone().isoformat(),'exit_code':p.returncode,'passed':ok,'source_head':'9f5814fec6cd071d39f0c12f8f48097ce661cb6a','source_state':'8 implementation files and tests reviewed dirty candidate','real_model_http':0};results.append(r);(a/'native-matrix.json').write_text(json.dumps(results,indent=2)+'\n');print(name,'PASS' if ok else 'FAIL',flush=True)
 if not ok:raise SystemExit(1)
check('daily-flags','feat164_qualification::tests::feat164_daily_identity_and_flags_are_closed',{})
check('feature-off','chat::database::isolated_model_migration::tests::feat164_disabled_migration_is_rejected',{},False,True)
for schema in [29,37]:
 root=a/f'feat164-natural-plans-sql{schema}';assert not root.exists()
 check(f'produce{schema}','chat::schedules::feat164_natural_plan_tests::feat164_natural_plan_upgrade',{'YIJIE_FEAT164_PLAN_ROOT':str(root),'YIJIE_FEAT164_PLAN_PHASE':'produce','YIJIE_ARTIFACT_MEDIA_ENABLED':str(schema==37).lower()},False,True)
 for case in ['review','held']:assert json.loads((root/case/'legacy.json').read_text())['schema']==schema
 for kind in ['isolated','daily']:
  daily=kind=='daily';flags={'YIJIE_KIMI_K31_PRO_CANDIDATE':'true','YIJIE_FEAT164_DAILY':str(daily).lower(),'YIJIE_FEAT155_SCHEDULED_CANDIDATE':str(not daily).lower(),'YIJIE_FEAT155_SCHEDULED_DAILY':str(daily).lower(),'YIJIE_FEAT164_NATURAL_SOURCE':str(root),'YIJIE_FEAT164_MIGRATION_TEST_ROOT':str(a/f'{kind}-sql{schema}')}
  check(f'{kind}-migrate{schema}',f'chat::database::isolated_model_migration::tests::feat164_controlled_{kind}_migration',flags,True,True)
print('Native matrix complete; all roots retained; no actual daily root accessed',flush=True)
