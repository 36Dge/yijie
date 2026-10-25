#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
extern int sqlite3_key_v2(sqlite3*,const char*,const void*,int);
int main(int argc,char **argv){
 if(argc!=3)return 2;
 unsigned char key[32];FILE *f=fopen(argv[2],"rb");if(!f||fread(key,1,32,f)!=32)return 3;fclose(f);
 sqlite3 *db=0;if(sqlite3_open_v2(argv[1],&db,SQLITE_OPEN_READONLY|SQLITE_OPEN_URI,0)!=SQLITE_OK)return 4;
 int rc=sqlite3_key_v2(db,0,key,32);memset(key,0,sizeof key);if(rc!=SQLITE_OK)return 5;
 const char *sql="SELECT json_object('kind','turn','id',t.id,'operation_id',t.operation_id,'runtime_turn_id',t.runtime_turn_id,'status',t.status,'submission_status',t.submission_status,'profile',m.profile_id,'facts',(SELECT count(*) FROM chat_native_facts f WHERE f.turn_id=t.id)) FROM chat_turns t JOIN chat_operation_models m ON m.operation_id=t.operation_id WHERE t.session_id='01a17433-9720-7043-b659-5a6c27a20f4c' UNION ALL SELECT json_object('kind','session','id',s.id,'agent_session_id',s.agent_session_id,'runtime_thread_id',s.runtime_thread_id,'profile',m.profile_id,'state',m.state,'title_source',s.title_source,'title_job_status',s.title_job_status) FROM chat_sessions s JOIN chat_model_selections m ON m.session_id=s.id WHERE s.id='01a17433-9720-7043-b659-5a6c27a20f4c' UNION ALL SELECT json_object('kind','answer','turn_id',f.turn_id,'text',json_extract(f.fact_json,'$.item.text')) FROM chat_native_facts f JOIN chat_turns t ON t.id=f.turn_id WHERE t.session_id='01a17433-9720-7043-b659-5a6c27a20f4c' AND f.method='item/completed' AND json_extract(f.fact_json,'$.item.type')='agentMessage'";
 sqlite3_stmt *q=0;if(sqlite3_prepare_v2(db,sql,-1,&q,0)!=SQLITE_OK){fprintf(stderr,"query_error: %s\n",sqlite3_errmsg(db));return 6;}
 while((rc=sqlite3_step(q))==SQLITE_ROW)puts((const char*)sqlite3_column_text(q,0));
 sqlite3_finalize(q);sqlite3_close(db);return rc==SQLITE_DONE?0:7;
}
