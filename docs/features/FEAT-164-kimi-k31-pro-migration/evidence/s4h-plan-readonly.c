#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
extern int sqlite3_key_v2(sqlite3*,const char*,const void*,int);
int main(int argc,char **argv){
 if(argc!=3)return 2;
 unsigned char key[32];FILE *f=fopen(argv[2],"rb");if(!f||fread(key,1,32,f)!=32)return 3;fclose(f);
 sqlite3 *db=0;if(sqlite3_open_v2(argv[1],&db,SQLITE_OPEN_READONLY|SQLITE_OPEN_URI,0)!=SQLITE_OK)return 4;
 int rc=sqlite3_key_v2(db,0,key,32);memset(key,0,sizeof key);if(rc!=SQLITE_OK)return 5;
 const char *sql="SELECT json_object('kind','plan','id',p.plan_id,'value',json_array(p.revision,p.schedule_epoch,p.name,p.content,p.rule_json,p.target_mode,p.conversation_id,p.target_state,p.state,p.next_at,p.authorization_ref,p.authorization_expires_at,m.profile_id)) FROM chat_scheduled_plans p LEFT JOIN chat_plan_models m ON m.plan_id=p.plan_id WHERE p.plan_id='01a1732e-d1d4-7d82-ad09-0274ee75feb0' UNION ALL SELECT json_object('kind','grant','id',grant_id,'value',json_array(owner_user_id,tenant_id,request_id,request_digest,plan_id,plan_revision,authorization_revision,definition_digest,workspace_source,workspace_id,max_runs,occupied_runs,expires_at)) FROM chat_scheduled_grants WHERE plan_id='01a1732e-d1d4-7d82-ad09-0274ee75feb0' UNION ALL SELECT json_object('kind','run','id',run_id,'value',json_array(owner_user_id,tenant_id,format_version,plan_id,plan_revision,schedule_epoch,request_id,request_digest,operation_id,trigger_source,original_run_id,logical_slot,grant_id,snapshot_json,snapshot_digest,workspace_source,workspace_id,permission_mode,delivery_state,native_outcome,needs_attention)) FROM chat_scheduled_runs WHERE plan_id='01a1732e-d1d4-7d82-ad09-0274ee75feb0' UNION ALL SELECT json_object('kind','selection','id',session_id,'value',json_array(profile_id,state)) FROM chat_model_selections WHERE session_id='01a1732e-f1ad-7ea3-aa00-1a41bb512e10'";
 sqlite3_stmt *q=0;if(sqlite3_prepare_v2(db,sql,-1,&q,0)!=SQLITE_OK){fprintf(stderr,"query_error: %s\n",sqlite3_errmsg(db));return 6;}
 while((rc=sqlite3_step(q))==SQLITE_ROW)puts((const char*)sqlite3_column_text(q,0));
 sqlite3_finalize(q);sqlite3_close(db);return rc==SQLITE_DONE?0:7;
}
