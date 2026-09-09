# FEAT-131～136 原生机制一致性复核

日期：2026-09-09。范围：当前源代码、依赖说明与验收证据适用性；`contract-impact=none`，仅修正文档，不改变 wire、运行行为、历史存储或权限。

## 当前统一权威

Codex 决定 Thread/Turn/Item 身份、消息 phase、最终内容和执行结果。FEAT-132 native v7、唯一 NativeDisplayBuffer 和 SQLCipher 原生事实/显示副本为当前对话主链路。FEAT-133/134/136 消费只读 ConversationView；FEAT-135 的草稿、提交去重和 durable acceptance 是产品事务，不是另一套模型/执行状态机。

| 需求 | 当前职责与需要保留的边界 | 原验收适用范围 |
|---|---|---|
| FEAT-131 | 能力矩阵、场景与参考策略；测试回放应经过当前 native 入口，不恢复 Store reducer | 原 stable 隔离身份/数据与纯文本 D4 仅证明其固定基线；日常入口以 FEAT-132/134 的普通 app 记录为准 |
| FEAT-132 | 原生协议、身份绑定、单一显示缓冲、原生读历史、SQLCipher 保管与旧档案只读 | 2026-09-09 十项 AC/local D4 及单独日常入口结果；冷历史、清理/附件/映射限制保留 |
| FEAT-133 | Timeline selector、Item shell、布局、折叠、安全渲染/复制；不解析 raw wire | 2026-08-28 的页面/主题/布局证据不证明旧 ConversationState 或 rollback 仍存在；原旧历史 reasoning metadata note 不覆盖 native 已保存正文 |
| FEAT-134 | 原生 phase/plan 与 summary/raw 分段展示；availability、诊断、busy 分离 | 2026-09-09 八项 AC/local D4；原 2026-08-29 证据已归档。summary/raw 正向组合使用合成回归，不冒称新模型样本 |
| FEAT-135 | Composer 目标草稿、ordered blocks、operation ID、本地 durable acceptance 后清空；后续事实由 native 主链显示 | 原 2026-08-29 D4 保持；新 queued 是本地提交记录，不得伪造 Codex 原生 UserMessage 身份或用正文匹配 |
| FEAT-136 | Command 原生事实的安全只读卡片；最终输出来自 Codex aggregatedOutput；旧 v5 仅兼容 | 原 2026-08-30 Command 五项 AC 是历史 v5 D4。原生显示信息损失已修复，独立八项 local D4 PASS；真实3/10文本，验收时为工作区候选，后固定 Desktop 8bfa5ca284fddb86d7cdd2a406c5041c49367688；远端状态另记交付记录 |

当前 full commits、代码证据与 FEAT-136 调整任务书见[FEAT-136 审计方案](../FEAT-136-desktop-command-tool-items/03-native-command-audit-and-plan-2026-09-09.md)。FEAT-134 远端步骤见[交付记录](../FEAT-134-desktop-streaming-progress-final-response/04-remote-delivery-2026-09-09.md)。

## 已修正的依赖描述

- 131/133/135 旧文档的 ConversationState、Store reducer、terminal reconciliation、旧 rollback 开关，只作为当时实现证据；后续实现引用当前 ConversationView/NativeDisplayBuffer，不按旧源码保护哈希恢复已删除文件。
- FEAT-133 的 error/warning 按已知来源范围展示；只有 thread 范围的 notice 留在会话层，不能猜测归属于当前 Turn。
- FEAT-135 的本地 queued/durable acceptance 与 Runtime 原生 Item 身份分开；保留用户意图/operation ID 幂等事务，不对历史任务自动补发或猜接管。
- `pnpm tauri:demo-fast:app` 是当前普通日常 canonical 入口；`pnpm tauri:demo-fast:stable` 的独立 bundle/app-data/Host Home 是原隔离验收环境，不能相互替代数据接管证据。FEAT-132 日常收尾已检查原 8 条 Host 映射，未证明隔离任务自动得到普通 Host 映射。
- 原 `read-only/never` 是对应历史验收配置；当前权限由 FEAT-152 原生策略与当前用户选择决定。不得为了匹配旧文档改变权限或放宽来源检查。
- FEAT-137 永久终止、未通过验收；旧 source PASS 不表示可用。FEAT-152 作为独立需求拥有自己的权限验收，不继承 FEAT-137 的 CAP/GS/D4，也不恢复旧入口。
- FEAT-144 继续负责真实 Tool，blocked / NOT RUN。FEAT-142/143 在本次检索中只有延期职责引用、没有独立 feature.yaml 包；不能宣称它们已有完整计划、额度或已执行门禁。将来建包必须复用 native 机制。
- Command output-delta 的原生能力存在，但 native v7 当前只投影等待最终输出的诊断。旧 v5 流式验收不再适用于新通道；先明确安全流式契约，不能因 FEAT-143 的旧描述恢复 v5 旁路。

## 后续需求与评审的固定检查项

1. 新数据从 native v7 与既有 NativeDisplayBuffer 进入；不得加入 ConversationState reducer、正文累积器或换名后的同类机制。
2. 完整 item/completed 直接替换临时对象；Turn 结束只更新 Turn，不生成 Item 结束状态、时间或正文。
3. phase/plan/reasoning 内容类别从原生字段取值；缺失保留缺失，summary 不冒充 raw。
4. 执行结果、内容可用性、界面 busy 分开；缺信息不推演失败，不因保存失败伪造 Runtime terminal。
5. 历史复用 thread/read/resume 与加密事实；冷/已观察来源分开，旧记录只读，不复制 ThreadHistoryBuilder、不解析 rollout、不用正文对账。
6. 保留必要的鉴权、传输 cursor 去重、资源容量、脱敏、加密存储、产品 outbox 和兼容 reader。出现“两个适配文件”不等于可删除其中一个，必须列真实消费者。
7. 验收必须标明代码提交、入口身份、实际数据/Host Home、模型请求及未执行项目。历史 PASS、结构门禁 PASS、synthetic PASS 和真实新 D4 分别记录，豁免不改写为 PASS。

这些是既有 FEAT-132/134 与 ADR-0013/0016 补充的复述，不新增权限、产品范围或门禁。

## 审计阶段验证与限制（实施前）

- 审计开始时五仓均 clean；修改范围仅元仓文档。没有 Runtime/Host/Desktop/Contracts 产品代码改动或消费者 pin 变化。
- Desktop `generate:check` 重新执行通过，包含 native 源快照与退役引擎边界检查。旧 v4 验证输出仍指向其历史锁，不能误报新 native 活跃来源。
- 安全定向检查：前端 native readonly view 6 项及旧 Command 卡片安全字段/复制 1 项通过；其余 20 项未被本次 `-t` 选择，不计入本次覆盖。Host 4 项原生最终 Item、元数据不改终态、原生读取及 Turn 不造 Item 检查通过。它们不覆盖本次指出的所有 native Command 适配缺口。
- 42 个 source lock 条目逐项与固定 Git 对象和当前工作树 SHA-256 相等（native 两份各 11，权限 Contracts 5、Host 15）；Desktop generate:check 通过。
- 元仓 pnpm lint、pnpm test（50/50）、bash -n scripts/*.sh、feature:audit（19 个已登记包）及六个需求的 D4 文档门禁通过。这里的 D4 checker 是对已记录验收范围的结构/语义检查，不是六项需求重新运行真实 D4，更不是 FEAT-136 新方案已验收。
- 未运行广泛 Host/Rust/Contracts 套件中的禁止场景，不触发包含它们的远端 PR/workflow。没有新增测试代码、关闭检查或修改断言。
- 本轮没有启动应用、改变权限、读取或复制用户数据库、发起模型/图片请求。调用累计：本轮文本 0、图片 0；各历史预算独立，不转用。
- 该审计阶段没有执行 FEAT-136 新方案的产品实现或 D4；不存在“六项需求整体完成”的结论。

## 授权后的实施结果

用户后续授权执行，并单独批准 FEAT-136 本次最多10次文本请求。原生 Command 展示和两处必要缩放布局修复已完成，251项前端、10项App/zoom、原生SQLCipher/旧Command IPC各1项及真实成功/失败/正常重开通过，本次八项 local D4 PASS；累计3/10文本、0图片，计量器正常关闭。Runtime/Host/Contracts源与权限不变，旧8条Host映射不变，仅新增1条验证映射。

FEAT-134四个原提交已按依赖顺序推送并核对远端SHA，精确SHA无Actions运行，CI NOT RUN。本次新增提交和推送已取得明确授权，Desktop 已固定为 8bfa5ca284fddb86d7cdd2a406c5041c49367688；元仓及远端实际状态见 FEAT-136 的 04-delivery-closure-2026-09-09.md，并发原始内容保留。最终权威见FEAT-136的02-verification.md及机器证据，原审计阶段0调用和历史FAIL不被覆盖。
