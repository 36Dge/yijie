# 原生对话过程展示修复（2026-10-22）

状态：四项代码修复及非破坏性定向验证已完成；本地开发构建验证见下文。Owner：段成威。Profile：demo_fast / local。
授权：用户明确要求按已完成审计完整修复四类过程展示，并优先复用工程原有执行链路。

## 范围与工程事实

复用固定 yijie-codex 0.144.6 的 `ThreadItem::WebSearch`、`Reasoning`、
`CommandExecution`、`AgentMessage.phase`、原生 Item ID 和 started/completed 生命周期。
不增加执行引擎、消息 reducer、文本累积器、检索工具、模型请求或 Runtime 补丁。
继续使用 Host 原生投影、一个 Native 显示缓冲、原生 SQLCipher 历史和现有审批链。

上游 TUI 对 absent phase 保留旧模型回答展示，不能直接解决 Kimi 中间消息缺阶段；
因此仅在 Desktop 阅读布局中，将后面确有同轮原生工具/推理活动的无阶段完整消息
放入过程区，不修改 phase、消息类型、执行状态或持久记录，不以关键词猜测。
明确 final_answer、用户追加输入、草案专用校验和最后的无阶段回答保留原语义。

## 契约与兼容

contract-impact = breaking，采用版本化扩展，绝不在旧封闭枚举上硬切。
新 native-thread v3 / SSE v10（v9 已被 Artifact 占用）承接安全的 webSearch 投影。
v1/v2 history、v7/v8 SSE 保持旧闭合形状，通过现有降级适配投影未知类型。
新 Desktop IPC v3 与 Native 持久格式 3；新 reader 可读取 1/2/3，旧 reader 对 3
沿现有 recordDiagnostics 拒绝解析，不损坏库或补建历史。已有记录不回填、不重写。
本地候选按源契约→生成→Host→Desktop 顺序；未获 Git 提交/发布授权，不伪造 immutable pin。

## 产品规则与验收

1. 搜索、打开网页、页内查找来自原生 WebSearchAction；正常结果显示紧凑活动行。
   搜索词经既有完整文本脱敏与容量限制；URL 不透传凭据、查询参数或自动打开链接。
2. 公开 commentary 在主过程显示。reasoning 可展开查看，重复的完整摘要只在阅读层
   合并；所有原始 Item 仍可在执行详情检查，不按正文修改原生 ID 或去重事实。
3. 成功且无可显示输出的命令归入执行详情，正常空/缺省输出用中性文案。
   失败、拒绝、待审批、未完整结束及需要操作的状态始终可见；原命令脱敏不放宽。
4. 缺 phase 的中间文字仅在存在后续原生活动证据时按过程布局；不能由 Turn 结束
   合成 final_answer 或 Item completed。调整模型公共进度指引，避免 true/echo 充当进度。
5. 未支持的非阻断内容进入详情；保留类型不可用的真实说明，不冒充搜索或执行失败。
6. 流式、完成、正常历史重开、亮暗主题、1180×760、键盘展开与受保护内容均验证。
7. 原生事实、顺序、审批、状态、错误、原始 phase 与旧记录保持；生成物来源可追踪。

## 替代与边界

本次用户授权替代旧 Pattern 中“所有 unknown/partial 固定在折叠外”的纯展示规则，
以及每条摘要重复展示技术说明的布局；不改变 ADR-0016/FEAT-132 的事实与安全边界。
不从 rollout 回写 SQLCipher 或为已丢失的旧 unknown 推断 webSearch。
普通无阶段回答继续可读，布局兼容证据只限本轮已观察的后续原生活动。
没有任何新自动重试、执行权限、远程发送、外部写入或生产部署。

## 非破坏性验证

使用正常合成事件、已有兼容样本与纯组件测试；不创建攻击性 fixture，不注入故障，
不修改权限，不强杀，不替换既有已发布二进制。构建仅使用项目标准工具生成开发产物。
在完整代码、契约和定向验证就绪后检查正常本地入口；不能执行的检查逐项记录原因与影响。
真实模型付费验收不借用历史 Feature 额度，也不把合成测试冒称真实 Provider 通过。

## 最终实现与证据

| 优先项 | 根因与修复 | 主要代码 |
| --- | --- | --- |
| 网页搜索被显示为未知内容 | 原生 WebSearch 已存在，Host 旧封闭类型没有投影。新增安全显示扩展，覆盖 search/openPage/findInPage/other；不再执行一次搜索 | `yijie-agent-host/internal/session/native_process.go`；`yijie-desktop/src/components/chat/ChatWebSearchItem.vue` |
| 重复摘要 | 不同原生 Item 的完整摘要本身相同。只在阅读布局折叠完全相同的已完成 summary；保留每个 Item，点击可检查原记录；移除逐条重复的“未提供原始推理正文”说明 | `yijie-desktop/src/domain/conversation-process.ts`；`ChatTurnGroup.vue`；`ChatTimelineItemShell.vue` |
| 空命令卡片 | 原例中的 true 是真实命令，不能删掉执行记录。成功且无可显示输出的命令进入详细过程；中性空输出文案，原耗时/退出码保留；有输出的 echo 仍正常展示 | `conversation-process.ts`；`ChatCommandItem.vue` |
| 进度消息分类 | Kimi 原例两条 agentMessage 均缺 phase。仅在已有后续原生活动证据时按进度排版，明确 final/user 输入为边界；已结束轮次保留最后一条有正文的无阶段回答，包含尾部推理和空消息情况 | `conversation-process.ts`；`ChatTurnGroup.vue` |

现有 Host `permissionInstructions` 增补简短公共进度指引，提醒模型不要仅为宣布进度运行
true/echo；用户任务确需的命令仍然允许。该指引不是命令拦截器，不能保证某个 Provider
今后绝不生成无意义调用。实际调用仍进入原有执行与审计链。

Runtime 复用依据：`yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/item.rs`
已有 `ThreadItem::WebSearch`、公开可选 `AgentMessage.phase` 以及 WebSearchAction 转换。
本次 `yijie-codex` tracked 文件相对任务开始时零变化，无新补丁、依赖或第二套执行引擎。

## 验证结果

- 前端定向测试：**242 项通过**。7 个组件/领域/IPC 测试文件 89 项，Chat Store 153 项。
  覆盖流式显示、结束折叠、手动展开保留、搜索动作、摘要重复、真实空命令、失败/审批保持可见、
  已有内容保护、缺 phase 的中间消息、明确边界、尾部活动/空消息下最终回答不丢失。
- Contracts：**8 项通过**。验证新/旧封闭形状、已有 MCP/权限语义不变、WebSearch 容量限制，
  以及固定 Runtime 本身已有相应能力。新生成物、两消费者快照与 candidate 内容哈希检查通过；
  原 native-conversation/native-mcp committed source 校验继续通过。
- Host：session/app/codex 定向测试通过。v10→v8/v7 和 history v3→v2/v1 不修改共享缓冲、ID、
  游标或原生生命周期；新增路由继续校验 bearer，正常/缺失历史响应禁止缓存。
- 跨仓库：运行既有 `scripts/check-native-conversation-integration.mjs`，实际 Host 投影字节经
  SSE 分块解码→单个 NativeDisplayBuffer→SQLCipher→正常关闭/重开，搜索动作、查询词和原生 ID 保留。
  未启动 Runtime 或请求模型。既有格式兼容测试验证 reader 1/2/3 及不支持未来格式的拒绝边界。
- `pnpm lint`（全仓 ESLint + vue-tsc）、`cargo fmt --check`、
  `cargo clippy --all-targets -- -D warnings`、`pnpm docs:build` 均通过。
- 通过标准 `pnpm tauri:demo-fast:app` 构建并启动项目 debug App；未签名、未发布。
  canonical launcher 校验源候选、构建 Host/前端/Rust、生成本地 build receipt，继续复用固定 Runtime。
  测试期间仅正常 Cmd+Q 退出空闲 App；临时 Vite 验收页经 server.close 正常关闭。
- 真实组件视觉与键盘：1180×760 浅色/深色、Enter 展开主过程/详细过程/命令通过。
  合成组件验收页没有模型请求或产品历史写入。
- 原始真实对话正常重开：主过程不再出现三张 unknown 卡片及三条空命令；9 条详细记录仍在，
  重复摘要默认折叠，有输出的真实命令仍在主过程，35 字中间消息显示为处理过程，最终回答及
  “完全访问权限”保持。旧 unknown 因历史已丢失类型，不改写成搜索。

本地证据目录（不含密钥或内部推理正文）：
`CrossBSD/.local/audits/conversation-process-fix-20261022/`。
包含开始时 tracked 内容哈希、验证记录、开发构建日志，以及 `process-light.png`、
`process-dark-details.png`、`existing-conversation-fixed.png`。

## 未执行项、原因与影响

1. `make lint` 总入口尝试后被既有 `generate-public-api.mjs` 的 clean-checkout 门禁拦住：
   `contracts checkout has tracked changes`。任务开始时 Contracts 已有 29 项未提交变动；
   不清理用户工作、不伪造 commit、不放宽旧门禁。本次版本化扩展通过独立 source-first candidate
   校验，实际 ESLint/类型/fmt/Clippy 分项通过。不能宣称完整 release gate 通过。
2. 未无差别执行完整 `make test`/所有 Rust 测试：仓库含历史故障/攻击 fixture 验收，
   与用户长期规则不兼容；选择普通合成事件、正常关闭/重开及纯组件验证。不包含强杀、
   二进制伪装、权限破坏或攻击注入测试；相应历史异常验收不计为通过。
3. 新真实付费模型回合未执行，模型请求数为 0。新网页显示通过实际 Host→Native→持久化链与
   真实 Vue 组件验证；原有真实历史通过 App 验证。Provider 是否遵循新增进度指引仍需真实回合观察。
4. 没有 Git 提交、推送、生产发布、签名或公证。新 family 当前是明确的 local-working-tree-candidate，
   并由 canonical 本地构建记录来源；发布前仍须按 contract-first 取得真实 immutable pin。

## 升级及回滚边界

新 Host 保留旧读接口和事件版本，新 Desktop 可读已有格式 1/2，读取不会批量升级旧记录。
新回合写格式 3。回滚至旧 Desktop 后，这些新记录走原有 format_unsupported 诊断，
不会删除、转换或从 rollout 重建。再次使用新版本即可读取格式 3。

保留了任务开始前的专家、连接器、样式等未提交工作；只对重叠的数据库测试、入口注册、
对话设计规则和本地开发构建 candidate 做必要的定点修改。
