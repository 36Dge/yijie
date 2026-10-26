"""Read a complete retained copy only; emit hashes, never keys/message content."""
from pathlib import Path
import ctypes as C
import hashlib, json, sys

root = Path(__file__).resolve().parent
db_path, key_path, output = map(Path, sys.argv[1:])
assert db_path.resolve().is_relative_to(root)
assert not output.exists()
lib = C.CDLL('/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-s4r-audit-20261026/libsqlcipher-audit.dylib')
ptr = C.c_void_p
lib.sqlite3_open_v2.argtypes = [C.c_char_p, C.POINTER(ptr), C.c_int, C.c_char_p]
lib.sqlite3_key_v2.argtypes = [ptr, C.c_char_p, ptr, C.c_int]
lib.sqlite3_prepare_v2.argtypes = [ptr, C.c_char_p, C.c_int, C.POINTER(ptr), ptr]
lib.sqlite3_step.argtypes = [ptr]
lib.sqlite3_column_count.argtypes = [ptr]
lib.sqlite3_column_type.argtypes = [ptr, C.c_int]
lib.sqlite3_column_bytes.argtypes = [ptr, C.c_int]
lib.sqlite3_column_blob.argtypes = [ptr, C.c_int]
lib.sqlite3_column_blob.restype = ptr
lib.sqlite3_column_name.argtypes = [ptr, C.c_int]
lib.sqlite3_column_name.restype = C.c_char_p
lib.sqlite3_finalize.argtypes = [ptr]
lib.sqlite3_close.argtypes = [ptr]
connection = ptr()
assert lib.sqlite3_open_v2(str(db_path).encode(), C.byref(connection), 1, None) == 0
key = key_path.read_bytes()
assert len(key) == 32
buffer = C.create_string_buffer(key)
assert lib.sqlite3_key_v2(connection, None, buffer, 32) == 0
C.memset(buffer, 0, len(buffer))
del key, buffer

def query(sql):
    statement = ptr()
    assert lib.sqlite3_prepare_v2(connection, sql.encode(), -1, C.byref(statement), None) == 0, 'readonly prepare failed'
    columns = [lib.sqlite3_column_name(statement, i).decode() for i in range(lib.sqlite3_column_count(statement))]
    rows = []
    try:
        while True:
            code = lib.sqlite3_step(statement)
            if code == 101:
                break
            assert code == 100, 'readonly step failed'
            row = []
            for i in range(len(columns)):
                typ = lib.sqlite3_column_type(statement, i)
                length = lib.sqlite3_column_bytes(statement, i)
                value = lib.sqlite3_column_blob(statement, i)
                row.append((typ, C.string_at(value, length) if length else b''))
            rows.append(row)
    finally:
        assert lib.sqlite3_finalize(statement) == 0
    return columns, rows

query('PRAGMA query_only=ON')
_, integrity = query('PRAGMA integrity_check')
assert integrity == [[(3, b'ok')]]

result = {'read_only_copy':True,'tables':{}}
allowed = {'state','revision','schedule_epoch','next_at','updated_at','last_scheduled_at','scheduled_at','disposition','due_at','cursor_at','next_evaluation_at','last_evaluated_at','authorization_revision','automatic_consent_version','effective_from','lease_expires_at','created_at','reason','recorded_at','processed_at','completed_at'}
for table in ['chat_scheduled_plans','chat_scheduled_occurrences']:
 columns,rows=query('SELECT * FROM "'+table+'"')
 result['tables'][table]=[]
 for row in rows:
  item={}
  for name,(typ,value) in zip(columns,row):
   item[name]={'sha256':hashlib.sha256(bytes([typ])+value).hexdigest()}
   if name in allowed or name in ['plan_id','id','occurrence_id']:
    item[name]['value']=None if typ==5 else value.decode()
  result['tables'][table].append(item)
assert lib.sqlite3_close(connection)==0
output.write_text(json.dumps(result,indent=2)+'\n')
print('Read-only row field hashes recorded')
