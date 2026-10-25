from pathlib import Path
import subprocess,json,hashlib,datetime,re
r=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');m=r/'yijie';d=m/'docs/features/FEAT-164-kimi-k31-pro-migration';e=d/'evidence';q=r/'feat164-s4k-qualification-20261026'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((e/n).read_text())
now=datetime.datetime.now().astimezone().isoformat();repos={}
for name in ['yijie-codex','yijie-contracts','yijie-agent-host','yijie-desktop','yijie-connectors','yijie-skills']:
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=q/name);repos[name]=subprocess.check_output(['git','rev-parse','HEAD'],cwd=q/name,text=True).strip()
drivers=load('s4l-driver-results.json');assert len(drivers)==6 and all(x['exit_code']==0 for x in drivers)
s1=[json.loads(x) for x in (e/'s4l-s1-driver.log').read_text().splitlines() if x.startswith('{')];assert sum(x.get('Action')=='pass' and bool(x.get('Test')) for x in s1)==11 and not any(x.get('Action') in ['fail','skip'] for x in s1)
counts={'s1':11}
for name,count in [('s2',57),('s4',24),('s4b',9)]:
 v=load('s4l-'+name+'/result.json');assert v['status']=='PASS';checks=v['checks'];assert all(x['result']=='PASS' and x['skipped']==0 for x in checks);assert sum(x['passed_cases'] or 0 for x in checks)==count
 for x in checks:
  log=e/('s4l-'+name)/(x.get('log') or x['name']+'.log');assert sha(log)==x['sha256']
 counts[name]=count
s3=load('s4l-s3/result.json');assert s3['passed'] and len(s3['results'])==5 and all(x['passed'] for x in s3['results']);counts['s3']=5
s4e=load('s4l-s4e/result.json');assert s4e['status']=='PASS_FOR_NATIVE_TERMINAL_SUBSET' and len(s4e['passed'])==7;counts['s4e']=7
text=(e/'s4l-renderer.log').read_text();v=json.loads(text[text.index('{'):]);assert v['numPassedTests']==18 and v['numFailedTests']==0 and v['numPendingTests']==0;counts['renderer']=18
text=(e/'s4l-verdict.log').read_text();assert 'pass 10' in text and 'fail 0' in text and 'skipped 0' in text;counts['verdict']=10
for item in load('s4l-final-checks.json'):assert item['exit_code']==0 and sha(e/('s4l-'+item['name']+'.log'))==item['log_sha256']
h=load('s4k-harness-qualification.json');assert h['desktop_commit']==repos['yijie-desktop']
for f,s in h['source_sha256'].items():assert sha(q/'yijie-desktop'/f)==s
fixture=load('s4l-app-loopback-ledger.json');assert fixture['attempts']==4 and fixture['external_requests']==0 and not fixture['rejected'] and fixture['state']=='stopped_normally'
assert [x['model'] for x in fixture['requests']]==['kimi-k3.1-pro']*3+['MiniMax-M3'];assert fixture['requests'][1]['stream_outcome']=='client_closed_stream'
audit=load('s4l-data-audit.json');assert audit['normal_app_exits']==3 and not audit['owned_processes'] and not audit['database_handles'] and all(x['unchanged'] for x in audit['old_record_checks'].values())
assert 'Kimi K3.1 Pro' in (e/'s4l-light-model-menu.ax.txt').read_text() and 'MiniMax-M3' in (e/'s4l-light-model-menu.ax.txt').read_text()
assert 'focused UI element is 70' in (e/'s4l-keyboard-return-focus.ax.txt').read_text()
assert '(selected' in (e/'s4l-appearance-before.ax.txt').read_text().split('Description: 浅色')[0].splitlines()[-1]
assert '按钮 (selected' in (e/'s4l-appearance-restored.ax.txt').read_text() and 'Description: 浅色' in (e/'s4l-appearance-restored.ax.txt').read_text()
for name in ['s4l-light-minimum-empty.jpg','s4l-dark-chat.jpg']:
 v=subprocess.check_output(['sips','-g','pixelWidth','-g','pixelHeight',str(e/name)],text=True);assert 'pixelWidth: 2360' in v and 'pixelHeight: 1520' in v
out={'at':now,'contract_impact':'none','source_commits':repos,'qualified_harness':{'id':h['id'],'commit':h['desktop_commit'],'digest':h['digest']},'test_counts':counts,'all_tests':sum(counts.values()),'source_profile_checks':4,'headless_s4_loopback_http':42,'app_loopback_http':4,'real_model_http_added':0,'real_ledgers_byte_identical':audit['real_ledgers_byte_identical'],'full_tconf04':'NOT RUN','source_artifact_match_ref':'s4l-preservation-audit.json','driver_refs':['s4l-driver-results.json','s4l-final-checks.json'],'evidence_reason':'Fresh execution at the existing immutable candidate; historical results were not relabelled'}
(e/'s4l-evidence-binding.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
verdicts={
 'core_vertical':{'status':'NOT RUN','executed_subset':'current canonical identity, text, normal interruption, paused reader/MiniMax, history; current S4K real-text G2V remains valid','missing':['natural old-K3 App migration/never-sent cancellation and old-plan reauthorization are unavailable in this candidate','real image/search/tool supplier coverage not executed; new paid calls prohibited'],'evidence':['s4l-active-positive.ax.txt','s4l-normal-cancel.ax.txt','s4l-paused-history.ax.txt','s4k-real-verdict.json'],'failure_class':None},
 'accessibility_visual':{'status':'PASS','scope':'FEAT164 available model control and status feedback in the current macOS candidate','checks':['K3.1/explicit MiniMax menu and no active old K3','keyboard Down/Up/Enter and Escape focus return','100% scale 1180x760 logical viewport in light/dark','streaming/interrupted/completed/unknown/paused unavailable states','plan model label and edit-cancel preserves authority','light appearance restored and original 1268x780 window restored on normal reopen'],'axe':'NOT RUN: native CUA has no DOM execution bridge; no full WCAG compliance claim','legacy_migration_dialog':'not naturally reachable; remains a core workflow gap, no visual claim for that dialog','evidence':['s4l-light-model-menu.ax.txt','s4l-keyboard-return-focus.ax.txt','s4l-light-minimum-empty.jpg','s4l-dark-chat.jpg','s4l-dark-model-menu.jpg','s4l-dark-unknown-bottom.jpg','s4l-paused-empty.ax.txt','s4l-plan-readonly-editor.ax.txt','s4l-appearance-restored.ax.txt'],'exit_code':0},
 'teardown':{'status':'NOT RUN','passed_subset':['three normal Cmd-Q exits','normal user stop and explicit subsequent turn','reopen no extra fixture requests','App/Runtime/worker/adapter/listeners/database handles absent','SQLCipher closed and old persistent records retained','three Runtime DB+WAL snapshots integrity OK'],'unresolved':'Runtime WAL frames remain not backfilled; normal close/checkpoint lifecycle still requires a decision and verification; do not declare full checkpoint complete','evidence':['s4l-normal-stop.json','s4l-data-audit.json','s4l-wal-audit-first-findings.json','s4l-runtime-wal-readonly-integrity.json','s4l-wal-audit-rca.json'],'failure_class':None}
}
for name,v in verdicts.items():v.update(verified_at=now,real_model_http_added=0,source_commits=repos);(e/('s4l-final-'+name+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'tests':sum(counts.values()),'source_profiles':4,'real_http_added':0,'finals':{k:v['status'] for k,v in verdicts.items()}}))
