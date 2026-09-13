# FEAT-153 第 5 步：无 GUI 编辑器状态复核

日期：2026-09-12。状态：**只读审查完成；随后获主任务授权的候选源码修复已落盘，完整检查待统一执行；非真实 WK 资格，D4 未通过。**

本次 `contract-impact = none`：只新增审查证据，不修改跨仓/跨进程协议、持久化、重放、部署配置或业务行为。后续修复仍由主任务按真实影响分类和统一执行。

## 范围与方法

用户外出无法解锁期间，读取 Coze 最小编辑器 `main.tsx`、`bridge.ts`、`draft-model.ts`、`native-canvas.tsx`，Desktop 的 channel、Pane、workspace 关闭/重连逻辑，以及 native HTTP 预算与 operation 分配位置。只做正常用户动作的源码时序推演；没有启动 App、浏览器、容器、网络服务或执行动态代码，没有延迟/故障注入、权限改动、攻击 fixture 或强杀。

此记录不重复已审的 vendor/CSP 构建例外，不把 TypeScript、单元测试、源码推演或已有无 GUI 服务证据当作 WKWebView、MessageChannel 实际载体或桌面交互通过。真实 dev/packaged WK 加载、焦点、到期遮罩、保存重开仍为 **NOT RUN**。

以下是发现时的代码事实。主任务后续修复会改变源码；不能把这些快照当作修复后验收结果。

## 发现

### H1 / P1：确定未提交的到期拒绝被置为不可查询的未知保存

证据：Coze `main.tsx:55–60` 把 `session_expired` 与 `operation_unknown` 一并写入 `model.uncertain`；`main.tsx:68–69` 在缺少 operation ID 时拒绝任何核对。Desktop `workflow-editor-channel.ts:130` 在调用 `native.exchange` 之前即可直接返回不带 operation ID 的 `session_expired`；Pane 的到期时间每 250 ms 刷新。

正常时序：用户在到期遮罩刷新前点击保存 → 父 channel 发现已到期，确定没有调用 native 写入 → 子页仍进入 uncertain → 用户正常重连，`DraftModel.receive` 保留 uncertain → 核对按钮因缺少 operation ID 直接报错 → 保存继续禁用。用户只能丢弃内存草稿并重新打开。

建议：明确区分分配/发出写入之前的拒绝与已提交未知；确定的到期拒绝应保留脏草稿并允许重连后按原 CAS revision 再保存。不能为这类未提交请求补造 operation ID。

状态：已向主任务报告；本次未修改、未运行时复测。

### H2 / P1：15 秒子页超时丢失迟到保存结果及查询 ID

证据：Coze `bridge.ts:61–64` 在 15 秒超时后删除 pending 项；`:46–47` 随后丢弃相同 request ID 的迟到响应。Desktop native `runtime.rs` 的 `exchange` 先执行 `ready()`/status，再进行写入请求；`transport.rs` 为每次 HTTP 请求分别设置 10 秒预算。两次串行正常等待之和可能超过子页 15 秒。原 operation ID 在 native exchange lease 分配，并随结果或写入错误返回。

正常时序：保存请求 status 与写入两段都未超过各自 HTTP 预算，但总时间超过 15 秒 → 子页先记为无 operation ID 的 unknown → 后续真实保存完成或带 operation ID 的 unknown 到达 → channel 正常回复、释放 pendingWrites，子页却因 pending 已删除忽略响应。此后核对入口无法查询原 operation，重连也不恢复它。

建议：保留有界的超时请求关联，接收同一 binding/generation/request 的迟到结果和 operation ID；或先使端到端等待预算与 native 全链路一致，并仍提供迟到结果收敛。不要重发写入，也不要仅靠“重新打开”宣称已确认原操作。

状态：已向主任务报告；本次没有运行人为延迟、故障或网络测试。

### H3 / P1：重连 bootstrap 尚未核对时允许保存，迟到读响应可回退模型

证据：Coze `main.tsx:34–39` 在请求 bootstrap 前就设置 `connected=true`，bootstrap 不设置 busy；`:99` 保存按钮不检查 bootstrap 完成。Desktop Pane `:42` 的 blocked 不包括 `!ready`，`:67` 的真实 bootstrap 仅设置 ready/显示状态。`DraftModel.receive:21–26` 对当前干净模型无条件接受远端 revision；Desktop `acceptEditorResult` 也可接受同 workflow 的较旧读取结果。

正常时序：脏草稿重连 → bootstrap 读取旧 revision 的响应尚在途 → 用户已能保存，同一旧 revision 的 CAS 保存成功 → `acceptSave` 更新新 revision 且模型变干净 → 先前的 bootstrap 响应稍后到达 → `receive` 覆盖回旧 canvas/name/revision。界面显示回退，下一次保存会产生不必要的 CAS 冲突。

建议：bootstrap 核对结束前不开放数据操作；对异步读取增加当前连接/读取票据或模型基线检查，不能用旧读取覆盖之后已确认的保存。重连继续保留原 iframe 与脏草稿，不能用 reload 规避时序问题。

状态：已向主任务报告；本次未伪造响应顺序或在运行环境注入竞态。

### H4 / P1：存在未知保存时，内容恢复旧基线会被当作可直接关闭

证据：`DraftModel.dirty:17` 只比较名称/画布与旧基线，未反映 uncertain。保存期间名称和画布仍允许继续编辑。Coze `refresh` 只向父页投影 `model.dirty`；Desktop `WorkflowLocalWorkspace.vue:29–38` 阻挡 createUncertain/pendingWrites，但未知保存完成本地等待后只依据 dirty 决定是否直接关闭。

正常时序：基线名称 A → 修改为 B 并保存 → 等待期间又正常改回 A → 保存结果为 operation_unknown → 当前内容等于旧基线，dirty=false，但 uncertain 及原 operation ID 仍存在 → 用户返回时无需确认便可关闭 iframe，销毁唯一保存查询入口。内容相同不能证明原写入未发生。

建议：离开策略单独考虑未确认写入，或在现有契约允许范围内保守投影未收敛状态；不能因内容等于旧基线就失去查询原 operation 的入口。如何允许用户明确离开以及查询信息的后续保留，由主任务结合已批准的仅内存草稿边界统一实现，不新增未批准的草稿持久化。

状态：已向主任务报告；未执行运行时场景。

## 已核实的正确边界与剩余交互限制

- 同一脏草稿接收相同 revision 时保留本地内容；不同 revision 会置 conflict 并禁止保存，不自动覆盖。干净草稿的普通重读可替换本地内容；H3 针对的是交错读取与保存，而非否定普通重读。
- `acceptSave` 以提交时 snapshot 更新基线，保存等待期间的后续编辑仍可保持 dirty；真实数据 CAS 与 operation 去重仍由 native/API/Coze 执行。
- 父页在有 pendingWrites 时阻挡重连和关闭；到期遮罩保留 iframe。未确认结果不是 pendingWrites 的同义词，H2/H4 仍需单独处理。
- 读操作通常捕获异常并保留画布；旧 port 被替换后不会接收旧 port 响应。当前缺少对完整模型与异步交互的 headless 覆盖证据，本次不补写虚构 PASS。
- 当前冲突提示主要引导返回列表重开，关闭弹窗只有继续编辑/明确放弃，未提供同页远端比较或“保存后返回”。这些属于剩余交互范围记录，不能把当前最小载体称为最终第 5/6 步完整交付。

## 发现时源码 SHA-256

路径均相对于同一个 CrossBSD 兄弟仓工作区。哈希仅用于定位本次审查版本，不代替各仓候选锁和构建登记。

| 文件 | SHA-256 |
|---|---|
| `yijie-coze/frontend/apps/workflow-local/src/main.tsx` | `c2a07e345dca94495bf6ab231ae2f0c3679280c76149aadb837b352e7ea5d760` |
| `yijie-coze/frontend/apps/workflow-local/src/bridge.ts` | `34ff1802651a6f7c9cc77d5a40226189e3b238db0017d28397a59e6bd384cb3a` |
| `yijie-coze/frontend/apps/workflow-local/src/draft-model.ts` | `9b6319b1b57411de51ee4154a2d7b85aacd992e9de9e9e718dce3f7a9e3de8bf` |
| `yijie-desktop/src/api/workflow-editor-channel.ts` | `61fe3b048643d6950af0bf48835551918f7c900ff56f414439e6c49f1ffe2365` |
| `yijie-desktop/src/components/workflows/WorkflowEditorPane.vue` | `f4b54dc9b7c6c8e5bbb40f9e8cc8287a4d9b45cb05a750aacaeb823b5dc17842` |
| `yijie-desktop/src/components/workflows/WorkflowLocalWorkspace.vue` | `645147191d7e4ba9af3261de77865a1b175f2eeb0e94d0f133f6b6641a7885e4` |
| `yijie-desktop/src/pages/workflows/use-workflow-workspace.ts` | `0db607ff5ca1f57d7a51a9aba3188e606fffc3ac4b45166c5c92b05db7ebb696` |
| `yijie-desktop/src-tauri/src/workflows/runtime.rs` | `36d29e0108847efdc56a8e35749f37ef2436992d7f10333aab187d127684d0b8` |
| `yijie-desktop/src-tauri/src/workflows/transport.rs` | `552dd587ffa50c7f42b00bae140adb1980f2a8032c8d40e414df954a334b36a6` |

## 验证结论

首轮结果是 **REVIEW FINDINGS**，不是场景 PASS。首轮没有运行 App、WK、容器或网络，也没有修改业务源码、生成物、依赖或运行状态，只新增本文件。修复后需要主任务记录新的源码/构建快照、正常合成 headless 测试结果，并在能解锁后继续真实 WK 资格。

## 随后授权的候选修复与交接

主任务接受 H1–H4，授权本审查子任务仅修改 Coze `main.tsx`/`bridge.ts` 与 Desktop `WorkflowEditorPane.vue`；主任务独占 `draft-model.ts`、native client、关闭确认文案及对应测试。业务修复沿既有源契约收敛状态解释，`contract-impact = semantic`；未新增 wire 字段、原生命令、权限、持久化或网络目标。

本子任务完成的候选：

- 移除子页 15 秒 deadline，保存 request 关联保留到 native typed 回复或真实 port 关闭；没有取消 native 既有 HTTP 上限或自动重发写入。
- bootstrap 完成前不开放数据操作，旧画布保持挂载但 inert；保存/读取入口有同步 active ticket，包含当前实际 bridge ID/generation 的 connection key 与本地连接代数，每次 await 后核验 ticket，读取还核验请求开始时的模型 revision。
- 实际连接更换/关闭会使旧 ticket 失效；在途保存仍通过主任务新增的 `failSave` 保守登记未知，旧读响应不写入新会话模型。已获得 operation ID 后如本地结果一致性检查失败，保留该 ID 供核对。
- Pane 在未 ready 时遮挡交互并显示“正在连接/核对草稿”；只有实际失败或到期才出现重连入口。watch 分别观察 bridge ID 和 generation，不因普通 workflow 结果更新重新 bind。
- H1/H4 的最终错误分类与 dirty 规则由主任务的 `DraftModel.failSave`/dirty 改动承接；本子任务不覆盖主任务文件或代报其测试通过。

限定静态检查：使用已安装锁定的 Babel parser 7.27.5 解析两个 TS/TSX 文件，并使用已安装 Vue compiler-sfc 解析 Pane，再以 Babel 解析其 TypeScript setup；仅内存解析，三个文件均 **STATIC PARSE PASS**，未发现尾部空白。此检查不执行应用代码，不生成工作区或 bundle，不等同类型检查或行为测试。

| 本子任务交接文件 | SHA-256 |
|---|---|
| `yijie-coze/frontend/apps/workflow-local/src/main.tsx` | `f5fa2db90c4f5d75b86271c90b0f00a10967899e0a8edbfd4f874a28f08e9029` |
| `yijie-coze/frontend/apps/workflow-local/src/bridge.ts` | `43578645b82ee7ed0ded3580b7b74e4f0e6cbfadb193eccd475f26f526e8ad99` |
| `yijie-desktop/src/components/workflows/WorkflowEditorPane.vue` | `095b9068c68d157f6b2f8646ea28e1ef4eb2c8bfd7dd4992783b3681e8eee78b` |

没有运行 canonical prepare、install、build、App 或容器；没有修改已挂载的 bin/dist。受控栈和构建登记由主任务先正常停止后统一更新。类型检查、正常 headless 回归、更新 bundle/登记及真实 WK 资格仍待对应主任务证据，不能由本静态解析结果替代。
