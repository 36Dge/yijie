# canonical14 Tauri 事件清理错误基线

记录日期：2026-09-13。范围：FEAT-153 原生 Coze 页面复验中的只读诊断，App PID `85986`。
`contract-impact=none`：本文件只记录已观察的控制台现象和源码证据，不修改 Desktop、Tauri、
Coze、契约、运行配置或持久状态；未执行脚本注入、故障制造、构建、重启或进程操作。

## 现场基线及本次观察范围

[打开前控制台](app14-console-before-open.json)记录 Web Inspector 中 **3 条错误**，
内容均为 `Unhandled Promise Rejection: TypeError: undefined is not an object
(evaluating 'listeners[eventId].handlerId')`。界面把其中两条合并显示计数 `2`，另有一条独立记录；
因此不能按 AX 中相同错误字符串只出现两次推断为两条错误。位置显示 `user-script:7:11`。
另有 `addLine`、`addNode` operation meta 重复注册的两条警告，属于另一类记录。

基线并非“从 App 启动至此没有操作”：用户在根代理接续复验前已经打开并正常关闭过旧工作流，
[原生日志](packaged-launch-14.txt)已有 `remote_close_confirmed`。不能把基线错误时间归入
随后某次创建、编辑或关闭，也不能据此推断其在原生 Coze 挂载之前已经发生。

截至本记录，根代理正常重开旧工作流及新建工作流期间没有观察到新增同类 Tauri 错误。
[新建后控制台](app14-console-after-new-workflow.json)仍保留原有 Tauri 两组记录；
控制台总错误数已变为 **4**，新增的是独立 `ReferenceError: Cannot access 'p' before initialization`。
后者不在本文件的 Tauri 归因范围，不能把“同类 Tauri 错误未增加”写成“控制台没有新增错误”。
后续正常 Chat／工作流切换的观察尚由根代理继续；本文件不预先宣布 Chat 生命周期通过。

## 可以确定的源码归属

已安装依赖为 Rust `tauri 2.11.5` 与前端 `@tauri-apps/api 2.11.1`。
两者在当前源码锁中均已存在，本轮没有修改 `src-tauri/Cargo.lock` 或 `pnpm-lock.yaml`。
不能仅因二者 patch 版本不同就判定依赖不兼容。

错误表达式直接对应锁定 Tauri Rust 源码：

- `tauri-2.11.5/src/event/mod.rs:208–222` 的 `unlisten_js_script` 生成注销用脚本。
  它取得 `listeners = (window[listeners_object_name] || {})[event]` 后，只检查事件容器存在，
  未检查其中 `listeners[eventId]`，便读取 `.handlerId`。
- `tauri-2.11.5/src/event/plugin.rs:57–69` 把该脚本装入
  `window.__TAURI_EVENT_PLUGIN_INTERNALS__.unregisterListener`，因此控制台会标为注入的
  `user-script`，而不是业务源码文件。
- `@tauri-apps/api/event.js:42–47` 的 `_unlisten` 先调用上述同步注销函数，再
  `await invoke('plugin:event|unlisten', ...)`。若读取 `.handlerId` 时发生异常，
  本次 Promise 会在原生注销命令发出前拒绝。

因此，可以确定这是 **Tauri 事件注销路径中，事件容器存在而指定 ID 缺失时的空值访问**。
它不是 Coze 的 `MessageChannel` 信封、工作流 ID、`request_history` 导航事件或画布节点数据校验错误。
不能仅凭这条表达式判断 ID 为什么缺失；注册时序、上下文变化或某条业务清理路径均需更多调用证据。

## 当前应用中的相关清理入口

Desktop 源码中可见以下正常 Tauri 注销调用，均早于本轮原生页面调整：

| 入口 | 确定行为 | Git 来源 |
|---|---|---|
| `src/pages/chat/ChatPage.vue:525–563` | 安装原生拖放监听；页面卸载时调用 `dragDropUnlisten`，并调用 `deactivatePageSession` | `3efed9aba5faab90ca3ea397a4d6489890df2026`（2026-08-19）；会话卸载接入来自 `86f02b4def4d07f76d66ebdafafda5a9bb75035c`（2026-08-22） |
| `src/stores/chat.store.ts:946–1003` | native-view／Chat 事件监听以组合函数注销，artifact 监听独立注销；`releaseSessionListeners` 调用这些函数后清空本地引用 | session／artifact 清理来自 `86f02b4def4d07f76d66ebdafafda5a9bb75035c`；两监听组合来自 `fe66786e3eed00a42821c4509b940ba889b89bf8`（2026-09-09） |
| `@tauri-apps/api/window.js:1667–1706` | `onDragDropEvent` 依次建立四条 Tauri 事件监听，返回的清理函数调用四个 unlisten | 已锁定的 `@tauri-apps/api 2.11.1` |
| `src-tauri/Cargo.lock:4165–4169` | 锁定 `tauri 2.11.5` 及原 checksum | 当前可用 Git 历史中的初始锁来源 `86a28d31c5a8c780d6828a28c7b057049a86ec55`（2026-07-05） |

上述调用方没有消费注销 Promise 的拒绝，能够解释控制台的 `Unhandled Promise Rejection` 形态。
但现有折叠记录没有给出事件名、event ID 或完整业务调用栈，**不能断言这三条分别对应哪几个监听**。
特别是三条错误的数量不能直接证明来自两条 Chat 监听加一条 artifact 监听，也不能排除拖放清理。

只读 `git status --porcelain` 已核对以下文件没有本轮改动：
`ChatPage.vue`、`chat.store.ts`、`chat-client.ts`、`chat-artifact-live-client.ts`、
`pnpm-lock.yaml`、`src-tauri/Cargo.lock`。工作流编辑器使用有限 MessageChannel 和具名 native command，
本轮没有为其新增 Tauri `listen`／`unlisten`。

## 不能作出的结论及影响边界

- 源码和锁早已存在，只能证明“这些实现不是本轮新增”；不能证明该运行时错误以前已经复现。
- 当前所检查的历史验收材料没有找到同类控制台文本，因此不能把旧 D4 当作本错误的既有豁免。
- 不能断言错误只是无害日志。按源代码执行顺序，该次原生 unlisten 可能没有发出，监听清理可能不完整；
  是否存在实际残留、重复回调或 Chat 功能影响，当前没有充分运行证据。
- 尚未观察到新增同类错误，不等于证明 Chat 切换、退出、重入和事件生命周期全部正确。
- 当前表达式不包含凭据或工作流正文；也不能仅据这条异常给出凭据、权限或身份边界的全面结论。
- `addLine/addNode` 警告、另一个 `ReferenceError` 与本 Tauri 注销错误分开追踪；不合并归因。

本记录保留基线，不改写计数，不清除错误来制造通过，也不修改依赖脚本或在线 App。
进一步定位仅使用正常界面切换和已有日志／完整调用栈观察；若需修复，须在后续明确候选中实施、
正常停止后重建并重新验证，不能把本只读诊断写成修复完成。
