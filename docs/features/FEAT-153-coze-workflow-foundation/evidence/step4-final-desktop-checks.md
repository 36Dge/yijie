# FEAT-153 第 4 步最终 Desktop 消费检查

日期：2026-09-12。OperationReceipt.version 的源字段说明澄清已 canonical 同步：只表示 publish 的结果版本或 release 的明确执行版本；create/save/debug 不携带该字段。本次只验证同步后的 Desktop consumer，没有修改 Desktop runtime、Vue、CSP 或保留的用户文件。

Desktop `contracts/workflow-local.lock.json` SHA-256：

```text
9aa83fbec1c5f585b677d854da6e4f6d513e0d19a3826479d15f4e69fc468fd6
```

| 命令（工作目录 `yijie-desktop`） | 最终结果 |
|---|---|
| `cargo test --manifest-path src-tauri/Cargo.toml --locked --lib workflows:: -- --test-threads=1` | PASS：10 passed、0 failed、0 ignored、347 filtered out；[原始输出](step4-final-desktop-checks.txt) |
| `cargo fmt --manifest-path src-tauri/Cargo.toml -- --check` | PASS；只读检查，无格式化写入 |
| `node ../yijie-contracts/scripts/sync-workflow-consumer.mjs desktop --check` | PASS：`Verified yijie-desktop workflow-local candidate; old public/Runtime locks untouched.` |

测试仍使用正常进程内 loopback consumer、合成输入和运行时随机机密，覆盖编辑会话、过期/正常关闭、普通并发时序、operation 查询和未知结果保留；不能替代真实 Coze 或 WKWebView 资格。本次没有启动 App、Docker 或服务，没有执行攻击 fixture、权限破坏、信号注入或全量 Rust 测试。

Infra 同轮 `make workflow-check` 也已更新为 10/10 PASS，见 [Infra 输出](step4-infra-checks.txt) 和 [审阅记录](step4-infra-review.md)。本次未修改 controller、Compose 或服务源码，未影响主执行正在进行的镜像源码双采样。
