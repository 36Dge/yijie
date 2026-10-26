package main

import (
 "crypto/sha256"
 "encoding/hex"
 "encoding/json"
 "fmt"
 "os"
 "path/filepath"
 "strings"
 bolt "go.etcd.io/bbolt"
)

func main() {
 if len(os.Args)!=3 { panic("copy path and output required") }
 path,out:=os.Args[1],os.Args[2]
 root:="/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-s4ad-audit-20261027/"
 if !strings.HasPrefix(filepath.Clean(path),root)||!strings.HasPrefix(filepath.Clean(out),root) { panic("copy only") }
 before,err:=os.ReadFile(path);if err!=nil { panic(err) }
 db,err:=bolt.Open(path,0600,&bolt.Options{ReadOnly:true});if err!=nil { panic(err) }
 counts:=map[string]int{};matches:=[]map[string]any{};fingerprints:=map[string]string{}
 op:="f38666dc-d2d8-4101-b498-eccf3045b6dd"
 err=db.View(func(tx *bolt.Tx)error{return tx.ForEach(func(n []byte,b *bolt.Bucket)error{return b.ForEach(func(k,v []byte)error{
  counts[string(n)]++;x:=sha256.Sum256(v);fingerprints[string(n)+":"+hex.EncodeToString(k)]=hex.EncodeToString(x[:])
  if !strings.Contains(string(v),op) {return nil}
  var m map[string]any;if json.Unmarshal(v,&m)!=nil {return nil}
  safe:=map[string]any{"bucket":string(n),"value_sha256":hex.EncodeToString(x[:])}
  for _,key:=range []string{"version","session_id","thread_id","previous_profile","request","stage","result","receipt","model_profile","model_revision","model_selection_state","model_operation_id","model_requested_profile","model_expected_revision"} {if val,ok:=m[key];ok {safe[key]=val}}
  matches=append(matches,safe);return nil
 })})});if err!=nil {panic(err)}
 if err=db.Close();err!=nil {panic(err)}
 after,err:=os.ReadFile(path);if err!=nil||sha256.Sum256(before)!=sha256.Sum256(after) {panic("copy changed")}
 data,err:=json.MarshalIndent(map[string]any{"copy_read_only":true,"bucket_counts":counts,"matching_operation":matches,"value_fingerprints":fingerprints},"","  ");if err!=nil {panic(err)}
 f,err:=os.OpenFile(out,os.O_WRONLY|os.O_CREATE|os.O_EXCL,0600);if err!=nil {panic(err)};defer f.Close()
 if _,err=f.Write(data);err!=nil {panic(err)}
 short,_:=json.MarshalIndent(map[string]any{"copy_read_only":true,"bucket_counts":counts,"matching_operation":matches},"","  ");fmt.Println(string(short))
}
