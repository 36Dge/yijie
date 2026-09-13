# 第 5 步 Desktop 原生与标准入口审计

日期：2026-09-12。范围：按已批准的第 5 步方向，准备同一个 `main` 窗口的真实 dev/packaged 资格验证。本文记录原生与入口实现及安全 focused checks；**本审计执行者没有启动 App、运行 Docker、打包 App 或调用模型**。实际 WKWebView、页面和正常退出结果由第 5 步主记录另行填写，不以本文替代。

权威仍为 `05-local-integration-design.md`、`06-step3-implementation.md` 和 `08-step5-desktop-integration.md`。本次未新增 wire DTO、IPC command 或远程 capability；沿用已生成的八个 workflow commands、300 秒 E 和 K_NA FILE 边界。FEAT-153 的新增跨仓能力分类不变；以下是已批准设计的具体实现和进程内竞态修复。

## 修改与代码事实

| 项目 | 实现与出处（路径从工作区根起） |
| --- | --- |
| 同一 App | `yijie-desktop/src-tauri/tauri.workflow-local.conf.json:1` 只合并配置；不改 productName、identifier 或原窗口尺寸。`main` 设置 `create:false`，由 `src-tauri/src/workflows/window.rs:25` 使用原 `WindowConfig` 的 `WebviewWindowBuilder::from_config` 创建。普通未选 overlay 的入口保持原自动创建。 |
| 精确门禁 | `src-tauri/src/workflows/mod.rs:15` 要求 `YIJIE_ENV=local`、`YIJIE_LOCAL_PROFILE=demo_fast`、`YIJIE_WORKFLOW_ENABLED=true` 同时满足；workflow overlay 在未满足时拒绝创建。 |
| 导航与窗口 | `src-tauri/src/workflows/window.rs:5` 允许原 `http://localhost:1420` 与 `tauri://localhost` app 文档；`:13` 新增唯一 `http://127.0.0.1:18888/editor/`，无 userinfo/query/fragment；`:44` 安装 URL 导航判断，`:45` 拒绝新窗口。URL hook 不具备 frame 标记，父页仍负责 iframe 的固定 src 与 sandbox。 |
| CSP 与旧资源 | overlay 仅新增精确 `frame-src http://127.0.0.1:18888`。原 `img-src` 的 `yijie-artifact-preview:` 和 `media-src` 的 `yijie-artifact-video:` 保留。这些现有 Chat 图片/视频是子资源，不是新文档；没有扩大为任意导航来源。默认 capability 文件未修改、无 remote ACL。 |
| 窗口失效 | `src-tauri/src/workflows/window.rs:46` 读取真实顶层 `window.url()`，避免把 iframe load 当作主文档离开；`src-tauri/src/lib.rs:195` 在 main 销毁时同样失效。`runtime.rs:766` 同步推进 context revision，随后正常 DELETE 清理；`:774` 只清理旧 revision，避免迟到清理清掉新 binding。 |
| 原生约束 | `src-tauri/src/workflows/commands.rs:22` 起仍为 status/list/create/open/exchange/close/run_start/run_query 八项；调用者要求 app main。`runtime.rs:177` 在 open 第一次 await 前捕获 context；`:292`、`:340` 在 exchange 前后核对当前 revision。binding 的新增 revision 字段为原生私有状态，不进入 renderer DTO。 |
| 不强杀本地 Host | `src-tauri/src/chat/sidecar.rs:394` 仅在 exact workflow 路径返回 forceful cleanup=false，`:699` 因而关闭 kill_on_drop。`:1035` 正常停止仍核对自有 PID 身份并发送 SIGTERM；3 秒观察窗口到期返回未清理，不进入 `start_kill`。保留 unknown/PENDING，不能把它记成退出完成。 |
| FILE 入口 | `scripts/run-local-demo-fast.sh:8` 保存 K_NA FILE 路径后从准备进程环境移除；`:75` 只检查 absolute/regular/non-symlink/current uid/0400 或 0600/nlink=1/有界文件元数据，不读 token。`:240` 才送入 native 启动环境。没有传入 K_AC。 |
| 公开 UI 开关 | `scripts/run-local-demo-fast.sh:71` 在 packaged 构建前设 `VITE_YIJIE_WORKFLOW_ENABLED` 为已验证的 true/false；默认 false 覆盖 ambient 值。`scripts/run-workflow-dev.mjs:34` 在 exact gate 后设 true。只有 boolean 可供 renderer，FILE 和 token 不使用 VITE。 |
| Host 隔离 | `src-tauri/src/chat/sidecar.rs:247` 的显式环境白名单不含任何 workflow 变量；`:684` 的 env_clear 阻止原生环境透传给 Host。Host/Runtime 代码未修改，K_NA FILE 不转交给 Host/Codex。 |

本节 `src-tauri/`、`scripts/` 简写均位于 `yijie-desktop/`。

## 标准 dev helper 的必要性与安全路径

安装版本为 Tauri 2.11.5、tauri-runtime-wry 2.11.4、Wry 0.55.1、CLI 2.11.4。原 CLI 的 beforeDev 子进程清理和 watch 重启具有 kill 路径，所以没有直接把普通 dev 脚本当作安全停止依据。

已批准的 `scripts/run-workflow-dev.mjs:29` 仍由原 `pnpm tauri:dev` 进入，使用相同 Vite config 与同一 App。helper 在导入 Vite 前去掉 workflow 私有环境键；用 Vite `createServer` 开启 localhost:1420，在 CLI 正常结束后 `server.close()`。它固定 spawn 原厂 `pnpm exec tauri dev`，附加 demo-fast/workflow overlay 与 `--no-watch`，不接受额外参数、任意 shell 或自定义 runner。子进程独立 session，helper 收到 SIGINT/SIGTERM 只提示 PENDING，不转发信号、不强停。进程记录仅含 PID、phase、origin、时间和退出码，不含凭据或 FILE 路径。

这一判断经过 **CLI 精确 tag 的主来源只读核对**，并非推断 kill 在所有 Tauri 用法中消失：

- [tauri-cli-v2.11.4 dev.rs](https://raw.githubusercontent.com/tauri-apps/tauri/tauri-cli-v2.11.4/crates/tauri-cli/src/dev.rs)：141–146 跳过空 beforeDev；302–348 的退出清理仅在 BEFORE_DEV 存在时进入子进程清理。workflow overlay 的 beforeDevCommand 明确为空。
- [同 tag interface/rust.rs](https://raw.githubusercontent.com/tauri-apps/tauri/tauri-cli-v2.11.4/crates/tauri-cli/src/interface/rust.rs)：196–203 的 no_watch 分支只启动一次并等待通知，不进入含 `.kill()` 的 watcher 分支。
- [同 tag interface/rust/desktop.rs](https://raw.githubusercontent.com/tauri-apps/tauri/tauri-cli-v2.11.4/crates/tauri-cli/src/interface/rust/desktop.rs)：111–114 先等待 dev child 自然退出，再调用 NormalExit；DevChild 没有 Drop 强停实现。该证据只覆盖正常 App 退出路径。

Host 现有正常停止也可复用：`yijie-agent-host/cmd/desktop-host/main.go:224` 依次执行 HTTP Shutdown 与 Runtime Shutdown，超时后的第二次清理使用无期限 context；`internal/codex/runtime.go:590` 关闭 stdin 并等待 exitDone，超时不会杀进程或释放仍活跃的 lease。因此没有修改 Host 或保留的 Runtime。

## 远程 iframe 的 native 隔离证据与实际验证边界

本机依赖源码（Cargo registry `index.crates.io-1949cf8c6b5b557f`）：

- `wry-0.55.1/src/wkwebview/class/wry_web_view_delegate.rs:50` 从 `WKScriptMessage.frameInfo.request.URL` 建立 IPC 请求 URI；不是借用顶层窗口 URL。
- `tauri-2.11.5/src/webview/mod.rs:1744` 根据请求 URL 判断 local；`:1820` 起远程请求需 ACL，即使是自定义 commands，也不能仅凭 main window label获得访问。
- `tauri-2.11.5/src/webview/webview_window.rs:150`、`:266`、`:315` 提供本次使用的 from_config/navigation/new-window 正式 API；没有替换 WK navigation delegate、使用私有 CookieStore、增加 scheme 或安装 CA。

以上为源码审计和正常纯测试证据。两种真实 WK 入口的 iframe native 隔离、MessagePort/source/origin、CSP 执行、握手与 300 秒会话到期，仍需在实际 App 中资格验证；本附件记录 **NOT RUN**，不会把源码判断写成平台实测 PASS。父页需保留早关后迟到 open 的显式 close、dirty canvas 的会话重连和 revision 比较；原生不声称替代这些 UI 行为。

## 实际执行的检查

执行目录为 `yijie-desktop`。全部为限定、正常、非破坏性检查。

| 命令 | 结果 |
| --- | --- |
| `cargo check --manifest-path src-tauri/Cargo.toml --locked --lib` | PASS |
| `cargo test --manifest-path src-tauri/Cargo.toml --locked --lib workflows:: -- --test-threads=1` | **13 PASS**，347 filtered；原始输出 `step5-desktop-native-tests.txt` |
| `cargo fmt --manifest-path src-tauri/Cargo.toml -- --check` | PASS |
| `cargo clippy --manifest-path src-tauri/Cargo.toml --locked --lib -- -D warnings` | PASS |
| `pnpm exec vitest run scripts/workflow-desktop-foundation.test.mjs --maxWorkers=1` | **6 PASS**；UI boolean 小修后重跑，原始输出 `step5-desktop-foundation-static.txt` |
| `pnpm exec eslint scripts/run-workflow-dev.mjs scripts/workflow-desktop-foundation.test.mjs --max-warnings=0` | PASS |
| `bash -n scripts/run-local-demo-fast.sh`、`node --check scripts/run-workflow-dev.mjs` | PASS |
| `node ../yijie-contracts/scripts/sync-workflow-consumer.mjs desktop --check` | PASS |
| `git diff --check` | PASS |

新 Rust 检查覆盖正常 URL/门禁及正常延迟清理与新会话并发；使用现有合成 loopback fixture，无恶意输入、故障注入、权限破坏或替换可执行文件。未运行全 Rust/历史攻击 fixture/强杀测试；早前已知 Chat tests 的 `cloned_ref_to_slice_refs` lint 不在 `clippy --lib` 范围，本文不声称 all-target lint PASS。未生成新的 Runtime，保留制品 SHA 检查与 canonical Host 可复现构建流程未绕过。

## 交给真实资格执行者的标准操作

先使用已批准 Infra controller 的 status 核对当前栈真实 ready，并确认没有另一 Desktop/Host 占用 18081、没有另一 Vite 占用 1420。不要为释放端口杀进程。

在 `yijie-desktop` 执行标准 dev 入口（只传非机密路径）：

```bash
env YIJIE_WORKFLOW_ENABLED=true \
  YIJIE_WORKFLOW_CREDENTIAL_FILE="$PWD/../yijie-infra/environments/local/generated/feat-153/private/k-na.json" \
  pnpm tauri:dev
```

packaged 使用相同 env 和 `pnpm tauri:demo-fast:app`，由原 canonical 工具链生成同一个 debug unsigned `.app`。不用 raw 入口、FEAT-131 第二 App、签名产物覆盖或人为 Runtime 替换。

正常退出使用 App 菜单退出/Cmd-Q，等待 native 正常 shutdown、CLI 自然退出和 Vite.close。`.local/demo-fast/workflow-dev/processes.json` 的 stopped 只证明 helper 的 CLI/Vite 链结束；还需只读确认自有 Desktop、Host、Codex PID 与 18081/1420 均正常退出。Ctrl-C 不是 App 退出方式；PENDING 或 cleanup_unknown 不算成功，不能接着强杀、覆盖二进制或再次启动竞争实例。

原有八项用户 dirty 文件及工作流布局/青柠色由主任务单独保护和增量集成，本审计没有格式化或编辑它们。生产、签名、公证、外部平台、ERP 服务和模型调用均不在本次验证范围；D4 状态由主任务真实验收决定。
