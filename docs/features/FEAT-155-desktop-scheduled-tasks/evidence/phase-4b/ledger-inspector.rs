use rusqlite::{Connection,OpenFlags};
fn inspect()->Result<(),&'static str>{
 let root=std::path::Path::new("/Users/jack/Library/Application Support/com.yijie.ai/demo-fast-scheduled-candidate-v1");
 let mut key=std::fs::read(root.join("secrets/chat-sqlcipher-v1.secret")).map_err(|_|"candidate key unavailable")?;
 if key.len()!=32{return Err("invalid candidate key length")}
 let c=Connection::open_with_flags(root.join("chat/conversations.db"),OpenFlags::SQLITE_OPEN_READ_ONLY).map_err(|_|"candidate database unavailable")?;
 let ok=unsafe{rusqlite::ffi::sqlite3_key_v2(c.handle(),std::ptr::null(),key.as_ptr().cast(),key.len() as i32)};key.fill(0);
 if ok!=rusqlite::ffi::SQLITE_OK{return Err("candidate key setup failed")}
 c.execute_batch("PRAGMA query_only=ON").map_err(|_|"readonly setup failed")?;
 let v:i64=c.query_row("PRAGMA user_version",[],|r|r.get(0)).map_err(|_|"schema unavailable")?;
 println!("schema={v}; open_mode=read_only; scope=isolated_scheduled_candidate");
 for table in ["chat_scheduled_plans","chat_scheduled_requests","chat_scheduled_grants","chat_scheduled_runs","chat_outbox","chat_turns","chat_sessions","chat_scheduled_draft_sources"]{
   let n:i64=c.query_row(&format!("SELECT count(*) FROM {table}"),[],|r|r.get(0)).map_err(|_|"count unavailable")?;
   println!("{table}={n}");
 }
 for query in [
 "SELECT 'confirmed_plan=' || p.plan_id || ';state=' || p.state || ';revision=' || p.revision || ';created_known=' || (p.created_at IS NOT NULL) FROM chat_scheduled_plans p JOIN chat_scheduled_draft_sources d ON d.plan_id=p.plan_id",
 "SELECT 'output_kind=' || coalesce(json_extract(json_extract(fact_json,'$.item.text'),'$.kind'),'not_canonical') FROM chat_native_facts WHERE method='item/completed' AND json_extract(fact_json,'$.item.type')='agentMessage'",
 "SELECT 'turn=' || status || ';submission=' || coalesce(submission_status,'missing') FROM chat_turns",
 "SELECT 'outbox=' || kind || ':' || state FROM chat_outbox",
 "SELECT 'fact=' || method || ';availability=' || coalesce(json_extract(fact_json,'$.availability'),'missing') || ';phase=' || coalesce(json_extract(fact_json,'$.item.phase'),'missing') || ';itemsComplete=' || coalesce(json_extract(fact_json,'$.turn.itemsComplete'),'missing') FROM chat_native_facts WHERE method IN ('item/completed','turn/completed')",
 "SELECT 'source=' || source_id || ';turn=' || local_turn_id || ';attempts=' || create_attempted || ',' || turn_attempted || ';confirmed=' || (plan_id IS NOT NULL) FROM chat_scheduled_draft_sources"
 ] {
  let mut statement=c.prepare(query).map_err(|_|"query unavailable")?;
  let values=statement.query_map([],|r|r.get::<_,String>(0)).map_err(|_|"facts unavailable")?;
  for value in values {println!("{}",value.map_err(|_|"fact unavailable")?);}
 }
 Ok(())
}
fn main(){if let Err(code)=inspect(){eprintln!("{code}");std::process::exit(1)}}
