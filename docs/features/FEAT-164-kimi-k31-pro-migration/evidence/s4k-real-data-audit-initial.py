from pathlib import Path
import json,subprocess,hashlib,shutil,datetime
r=Path('/Users/jack/Downloads/Personal_Info/CrossBSD');e=r/'yijie/docs/features/FEAT-164-kimi-k31-pro-migration/evidence';a=r/'feat164-s4k-audit-20261026';prior=r/'feat164-s4i-audit-20261025';base=Path('/Users/jack/Library/Application Support/com.yijie.ai.feat164-kimi-k31-r1/demo-fast-model-candidate-v1');dest=a/'final-data';before=a/'candidate-app-data/chat/conversations.db';after=dest/'conversations.db'
def read(binary,p):
 v=subprocess.run([str(binary),'file:'+str(p)+'?immutable=1',str(base/'secrets/chat-sqlcipher-v1.secret')],capture_output=True,text=True);assert v.returncode==0,v.stderr;return [json.loads(x) for x in v.stdout.splitlines()]
plans=read('/tmp/feat164-s4h-plan-readonly',before);assert plans==read('/tmp/feat164-s4h-plan-readonly',after)
failed=read('/tmp/feat164-s4f-readonly',before);assert failed==read('/tmp/feat164-s4f-readonly',after)
def facts(p):return {x['event_id']:hashlib.sha256(x['fact_json'].encode()).hexdigest() for x in read('/tmp/feat164-s4f-fact-hash',p)}
assert facts(before)==facts(after)
unknown=read(prior/'operation-readonly',after);assert unknown==read(prior/'operation-readonly',before)
old=read(prior/'switch-readonly',after);assert old==read(prior/'switch-readonly',before)
new=read(prior/'paired-switch-readonly',after);assert new==[{'profile':'kimi-k3-1-pro-max-v1','state':'ready','revision':3,'model_operations':2,'market_submissions':2,'unsettled_market':0,'expert_state':'ready'}],new
operations=read(prior/'paired-operation-readonly',after);assert len(operations)==2 and all(x['phase']=='committed' for x in operations);assert {x['target_profile_id'] for x in operations}=={'kimi-k3-1-pro-max-v1','minimax-m3-high-v1'}
current=read(a/'real-readonly',after);turns=[x for x in current if x['kind']=='turn'];answers=[x for x in current if x['kind']=='answer'];session=[x for x in current if x['kind']=='session']
assert len(turns)==3 and all(x['status']=='completed' and x['submission_status']=='submitted' and x['profile']=='kimi-k3-1-pro-max-v1' and x['facts']==8 for x in turns)
assert len({x['operation_id'] for x in turns})==3 and len({x['runtime_turn_id'] for x in turns})==3
assert [x['text'] for x in answers]==['42','50','8']
assert len(session)==1 and session[0]['state']=='ready' and session[0]['title_job_status']=='not_started' and session[0]['title_source']=='fallback'
ledger=json.loads((e/'g2v-real-budget-ledger-r3.json').read_text());assert len(ledger['requests'])==5 and ledger['meter_state']=='stopped_normally' and ledger['halted'] and all(x['status']=='settled' for x in ledger['requests'][2:])
out={'at':datetime.datetime.now().astimezone().isoformat(),'all_original_plan_grant_run_and_selection_records_unchanged':len(plans),'original_attempted_draft_metadata_unchanged':True,'old_completed_draft_facts_unchanged':len(facts(before)),'old_unknown_operation_unchanged':unknown,'old_expert_selection_and_submission_counts_unchanged':old,'paired_expert_selection_unchanged':new,'paired_expert_model_operations_unchanged':operations,'current_real_session':current,'real_model_http_added':3,'read_only_audit':True,'database_sha256':hashlib.sha256(after.read_bytes()).hexdigest()}
p=e/'s4k-real-data-audit.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS: original plan/grant/run/draft/facts/unknown and expert records retained; three real completed turns saved')
