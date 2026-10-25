#include <sqlite3.h>
#include <stdio.h>
#include <string.h>
extern int sqlite3_key_v2(sqlite3*,const char*,const void*,int);
int main(int argc,char **argv){
 if(argc!=3)return 2;
 unsigned char key[32];FILE *f=fopen(argv[2],"rb");if(!f||fread(key,1,32,f)!=32)return 3;fclose(f);
 sqlite3 *db=0;if(sqlite3_open_v2(argv[1],&db,SQLITE_OPEN_READONLY|SQLITE_OPEN_URI,0)!=SQLITE_OK)return 4;
 int rc=sqlite3_key_v2(db,0,key,32);memset(key,0,sizeof key);if(rc!=SQLITE_OK)return 5;
 const char *sql="SELECT json_object('event_id',f.event_id,'format_version',f.format_version,'fact_json',f.fact_json) FROM chat_native_facts f JOIN chat_turns t ON t.id=f.turn_id WHERE t.session_id='01a17323-8807-7680-b4bc-672d4283a226' ORDER BY f.event_id";
 sqlite3_stmt *q=0;if(sqlite3_prepare_v2(db,sql,-1,&q,0)!=SQLITE_OK){fprintf(stderr,"query_error: %s\n",sqlite3_errmsg(db));return 6;}
 while((rc=sqlite3_step(q))==SQLITE_ROW)puts((const char*)sqlite3_column_text(q,0));
 sqlite3_finalize(q);sqlite3_close(db);return rc==SQLITE_DONE?0:7;
}
