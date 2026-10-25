#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
extern int sqlite3_key_v2(sqlite3*,const char*,const void*,int);
int main(int argc,char **argv){
 if(argc!=3)return 2;
 unsigned char key[32];FILE *f=fopen(argv[2],"rb");if(!f||fread(key,1,32,f)!=32)return 3;fclose(f);
 sqlite3 *db=0;if(sqlite3_open_v2(argv[1],&db,SQLITE_OPEN_READONLY|SQLITE_OPEN_URI,0)!=SQLITE_OK)return 4;
 int rc=sqlite3_key_v2(db,0,key,32);memset(key,0,sizeof key);if(rc!=SQLITE_OK)return 5;
 const char *sql="SELECT json_object('kind',o.kind,'state',o.state,'attempt_count',o.attempt_count,'payload_version',o.payload_version,'next_attempt_at',o.next_attempt_at,'profile',m.profile_id,'create_attempted',x.create_attempted,'turn_attempted',x.turn_attempted,'public_state',b.state,'public_error',b.last_error_code,'host_bound',s.agent_session_id IS NOT NULL,'turn_status',t.status,'submission_status',t.submission_status) FROM chat_outbox o JOIN chat_scheduled_draft_sources x ON x.create_operation_id=o.operation_id OR x.operation_id=o.operation_id JOIN chat_sessions s ON s.id=o.session_id JOIN chat_turns t ON t.id=x.local_turn_id LEFT JOIN chat_operation_models m ON m.operation_id=o.operation_id LEFT JOIN chat_public_task_bindings b ON b.session_id=s.id WHERE s.id='01a17315-c3f9-7e93-a6f8-56a7b7876520' ORDER BY o.kind";
 sqlite3_stmt *q=0;if(sqlite3_prepare_v2(db,sql,-1,&q,0)!=SQLITE_OK){fprintf(stderr,"query_error: %s\n",sqlite3_errmsg(db));return 6;}
 while((rc=sqlite3_step(q))==SQLITE_ROW)puts((const char*)sqlite3_column_text(q,0));
 sqlite3_finalize(q);sqlite3_close(db);return rc==SQLITE_DONE?0:7;
}
