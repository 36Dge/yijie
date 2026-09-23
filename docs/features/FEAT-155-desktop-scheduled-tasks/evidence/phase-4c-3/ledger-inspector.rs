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
 "SELECT 'run='||r.run_id||';plan='||r.plan_id||';trigger='||r.trigger_source||';delivery='||r.delivery_state||';outcome='||r.native_outcome||';grant='||r.grant_id||';op='||r.operation_id||';original='||coalesce(r.original_run_id,'none')||';snapshot='||r.snapshot_digest FROM chat_scheduled_runs r",
 "SELECT 'grant='||grant_id||';max='||max_runs||';occupied='||occupied_runs||';expires='||expires_at FROM chat_scheduled_grants",
 "SELECT 'binding='||run_id||';conversation='||coalesce(conversation_id,'none')||';turn='||local_turn_id||';create_op='||coalesce(create_operation_id,'none') FROM chat_scheduled_run_bindings",
 "SELECT 'recovery='||run_id||';create_attempt='||create_attempt||';turn_attempt='||turn_attempt||';release='||coalesce(release_kind,'none')||';refunded='||refunded FROM chat_scheduled_recovery",
 "SELECT 'outbox='||o.operation_id||';kind='||o.kind||';state='||o.state||';attempts='||o.attempt_count FROM chat_outbox o WHERE o.scheduled_run_id IS NOT NULL",
 "SELECT 'plan='||plan_id||';state='||state||';revision='||revision||';grant='||coalesce(authorization_ref,'none') FROM chat_scheduled_plans",
 "SELECT 'reservation_count='||count(*) FROM chat_scheduled_reservation",
 "SELECT 'terminal='||json_extract(fact_json,'$.turn.id')||';native_status='||json_extract(fact_json,'$.turn.status') FROM chat_native_facts WHERE method='turn/completed'"
 ] {
  let mut statement=c.prepare(query).map_err(|_|"query unavailable")?;
  let values=statement.query_map([],|r|r.get::<_,String>(0)).map_err(|_|"facts unavailable")?;
  for value in values {println!("{}",value.map_err(|_|"fact unavailable")?);}
 }
 if v>=24 {
  for q in ["SELECT 'automatic_consent='||e.grant_id||';version='||coalesce(e.automatic_consent_version,0) FROM chat_scheduled_enable_receipts e", "SELECT 'future='||plan_id||';next='||coalesce(next_at,-1)||';hold='||coalesce(future_hold,'none') FROM chat_scheduled_plans", "SELECT 'slot='||plan_id||';at='||scheduled_at||';disposition='||disposition||';run='||coalesce(run_id,'none') FROM chat_scheduled_occurrences"] {
   let mut st=c.prepare(q).map_err(|_|"automatic query unavailable")?;
   for row in st.query_map([],|r|r.get::<_,String>(0)).map_err(|_|"automatic facts unavailable")? {println!("{}",row.map_err(|_|"automatic fact unavailable")?);}
  }
 }
 if v>=25 {
  let mut st=c.prepare("SELECT 'single='||s.grant_id||';version='||s.format_version||';kind='||s.trigger_source||';original='||coalesce(s.original_run_id,'none') FROM chat_scheduled_single_run_grants s").map_err(|_|"single query unavailable")?;
  for row in st.query_map([],|r|r.get::<_,String>(0)).map_err(|_|"single facts unavailable")? {println!("{}",row.map_err(|_|"single fact unavailable")?);}
 }
 Ok(())
}
fn main(){if let Err(code)=inspect(){eprintln!("{code}");std::process::exit(1)}}
