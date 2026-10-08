# 固定Codex库的stdio正常EOF桥接资格

2026-10-07（Asia/Shanghai）。结果：[stdio-run-01.json](stdio-run-01.json)。正常本地协议资格 **PASS**，真实Google包及生产bridge仍NOT RUN/NOT IMPLEMENTED。

固定库来源 `yijie-codex@7fd463bcef07f37b0211acd9f62b9f93ea0a4b12`。本次没有修改、复制、重编译或覆盖Codex Runtime；沿Connectors的固定path依赖与外部lock闭包，使用原有Cargo target缓存正常构建本项目资格测试程序。

## 实际链路与结果

测试源为 `yijie-connectors/worker/tests/stdio_bridge.rs`，独立普通server源为 `worker/qualification/stdio_server.rs`。后者通过显式 `stdio-qualification` Cargo feature构建，不属于产品status worker控制协议，也不模仿npm/Google命令或覆盖已有可执行文件。

1. 公共 `RmcpClient::new_in_process_client` 调用实现的 `InProcessTransportFactory::open`，取得 `tokio::io::DuplexStream`。
2. 工厂启动一次自己拥有的普通server（标准Cargo编译产物），只配置stdin/stdout管道，env_clear、kill_on_drop(false)，没有密钥/文件/网络业务能力。
3. 两个普通字节转发task分别连接DuplexStream与child stdin/stdout。MCP JSON握手、发现、调用和结果处理仍由固定Codex库完成，没有重写MCP client。
4. initialize识别 `yijie-ordinary-stdio-qualification`，tools/list只有 `lookup`；一次lookup取得 `public-stdio-value`，isError=false。
5. `client.shutdown()`/drop结束库侧连接；独立owner显式关闭其child stdin（正常EOF），等待真实子进程完成，再join两个转发task。PID59462 exit0，childReaped=true，两个bridge均无错误，spawnCount=1。

server SHA-256 `de456dcd375ef89b96061e484e5c9ac2ea8c524f569e9ee8d8b140a86e229902`。零外部请求、零模型请求、零OAuth/凭据读写；没有强杀、恶意fixture、故障注入或可执行文件替换。

## 为什么绕开原生强杀路径

源码相对 `yijie-codex`：

- `codex-rs/rmcp-client/src/in_process_transport.rs:6-14` 为公开、可实现的工厂trait，返回DuplexStream。
- `codex-rs/rmcp-client/src/rmcp_client.rs:331-348` 的in-process构造明确 `stdio_process: None`；`:768-771` 直接使用工厂字节流。
- 同文件`:730-743` 的shutdown只在stdio_process存在时调用terminate；本次分支不存在该handle，释放RunningService不会进入LocalProcessTerminator。
- 原 `stdio_server_launcher.rs:258,330-334` 的kill-on-drop与TERM后强杀逻辑完全没有被调用。

正常EOF由独立owner控制，因此不用把库client Drop当成唯一子进程回收保证。测试里如果普通wait超过5秒会返回STOP_PENDING并保留owner，不调用kill或发进程信号；成功路径才解除owner。没有使用异常退出验证该分支，不能标记强杀/异常fixture测试为PASS。

## 适用范围与后续

已经证明推荐架构的公开字节接口和独立正常EOF owner可实现，无需为了进程退出修改Runtime。尚未证明真实npm包退出、进程树/后代处理、断开/重连、并发使用、stdio凭据与持久token安全、升级恢复或产品sidecar生命周期；这些继续按供应商及本地资格台账处理。Google Calendar的token文件问题仍保持阻断，不能因本次EOF成功将真实包标为可用。

命令：

```sh
python3 scripts/check-worker-source.py
YIJIE_STDIO_QUALIFICATION_EVIDENCE=/new/result.json make worker-stdio-qualification
CARGO_TARGET_DIR=/absolute/CrossBSD/yijie-codex/codex-rs/target cargo clippy --offline --locked --manifest-path worker/Cargo.toml --features stdio-qualification --test stdio_bridge --bin stdio-qualification-server --no-deps -- -D warnings
```

以上命令从Connectors仓运行；资格结果JSON不包含真实数据。常规worker构建不启用该feature，不扩大产品可执行接口。
