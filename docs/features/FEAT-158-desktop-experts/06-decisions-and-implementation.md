> **2026-10-13范围更新**：AC-007 内容质量验收已依用户明确指令移除，外观仍跳过；当前活动验收与剩余项以 [02](02-verification.md)、[13](13-scope-adjustment.md) 和 feature.yaml 为准。下文原始资格表、内容评测和待执行措辞保留设计时历史，不新增当前完成门槛。

> **2026-10-11实施更新**：用户在本包交付后要求分阶段实施，以下DEC-158-01至12作为推荐方案获准用于本地实现；资格项仍须实际验证。起草时“只需求设计/待D0”的措辞保留历史语义，实施记录见07。

# FEAT-158 专家功能决策与实施依赖

> **Draft · 2026-10-11 · 本轮仅需求设计**。以下为供段成威 D0 评审的推荐方案，不是实施、Runtime 资格、模型质量、D4、Git 交付或发布批准。本轮未修改产品代码、未启动或构建服务、未执行模型及外部业务调用。

推荐采用“受管专家包适配”：专家内容在 `yijie-skills` 维护；Desktop 管理专家和会话绑定；Host 把经校验的专家上下文送入已有 Codex 原生执行链路。安装、版本校验、聊天、审批、历史与本地持久化沿用现有机制。WorkBuddy 的 Plugin 组织用于理解内容边界，不直接成为易界的运行时格式或安装路径。

产品流程与验收以本需求包的产品、验证文档为准；本文记录工程依据、方案取舍、D0 决策和实施前资格。具体 Runtime 投送与内容映射分别由本包 `04`、`05` 专题文档约束，不在此另立一份协议。

## 1. 事实、假设、未知与冲突

### 1.1 Fact 已核对事实

源码证据对应 [仓库基线](evidence/repository-baseline.json) 中的工作树。行号用于定位本轮调查内容，不替代后续实现时的完整 commit、实际构建摘要或方向兼容证据。

| ID | 已核对事实 | 工程依据 |
|---|---|---|
| F-01 | 易界领域 Skills、Plugins、Prompt Packs、Evals 属于 `yijie-skills`，Host 负责加载；不把电商角色写入 Runtime 内核 | [ADR-0003](../../adr/ADR-0003-skills-outside-codex-core.md)，第 17、27 行 |
| F-02 | 当前 Desktop 有 Skill 广场及连接器页面，没有独立专家路由或专家领域；现有 `amazon-listing-expert` 是 Skill 标识 | [router/index.ts](../../../../yijie-desktop/src/router/index.ts)，第 26–46、117–131 行；[skill-icons.ts](../../../../yijie-desktop/src/icons/skill-icons.ts)，第 31 行 |
| F-03 | Skill 的安装、启停、卸载最终调用 Host managed-skill 接口；UI 已有 loading、empty、permission-denied、unavailable、incompatible 和逐项操作反馈 | [skills/host.rs](../../../../yijie-desktop/src-tauri/src/skills/host.rs)，第 127–183 行；[skill.store.ts](../../../../yijie-desktop/src/stores/skill.store.ts)，第 20–28、112–126、185–233 行 |
| F-04 | Skill 根由 Native 路径解析器确定：内置资源为 `resource_dir/skill-packages`，受管安装为 `app_data_dir/skills/installed`；Renderer 不能提交安装目标路径 | [skills/resources.rs](../../../../yijie-desktop/src-tauri/src/skills/resources.rs)，第 11–14、70–109 行 |
| F-05 | 当前 Skill 目录固定包版本 `0.3.0`、来源 commit、tree/manifest 摘要、38 项和分类数量；不是投放任意文件即可接入的开放 Plugin 目录 | [skills/catalog.rs](../../../../yijie-desktop/src-tauri/src/skills/catalog.rs)，第 8–18、214–259 行 |
| F-06 | Skill 全局启停与本轮选择是不同机制。聊天技能开关直接调用 `skills.setEnabled`，当前不会冻结单轮 Skill 选择 | [ChatPage.vue](../../../../yijie-desktop/src/pages/chat/ChatPage.vue)，第 104–110 行；[ChatSkillControl.vue](../../../../yijie-desktop/src/components/chat/ChatSkillControl.vue)，第 30–32 行 |
| F-07 | FEAT-157 已有 installation/revision/generation 引用、提交时冻结的选择与显示副本、幂等回执；冻结和消息/outbox 使用同一事务，并唤醒同一个 Coordinator | [connectors/selection.rs](../../../../yijie-desktop/src-tauri/src/chat/connectors/selection.rs)，第 183–310、315–330、514–520 行 |
| F-08 | 历史连接器标签来自对应已接收轮次的显示快照，不读取当前 catalog；新草稿与各会话草稿分开，管理页导航保留草稿；本地 durable accepted 后才清空正文和本轮连接器选择 | [ChatPage.vue](../../../../yijie-desktop/src/pages/chat/ChatPage.vue)，第 337–348、601–634 行；[chat-composer-drafts.store.ts](../../../../yijie-desktop/src/stores/chat-composer-drafts.store.ts)，第 8–42 行 |
| F-09 | 当前市场工具只有真实 ready、effective enabled、使用权限和执行能力同时满足才能选择；有非空连接器选集时仅支持用户手动选择“请求批准” | [market-connectors-ui.ts](../../../../yijie-desktop/src/domain/market-connectors-ui.ts)，第 85–138 行；[ChatPage.vue](../../../../yijie-desktop/src/pages/chat/ChatPage.vue)，第 364–383 行；[connectors/selection.rs](../../../../yijie-desktop/src-tauri/src/chat/connectors/selection.rs)，第 229–234 行 |
| F-10 | 产品持久状态沿用 Native SQLCipher。当前基础 activated schema 为 15，最大兼容 reader 为 33，连接器启用时会迁至 33；不能为专家随意复用历史 migration 编号 | [chat/migrations.rs](../../../../yijie-desktop/src-tauri/src/chat/migrations.rs)，第 180–222 行；[chat/database.rs](../../../../yijie-desktop/src-tauri/src/chat/database.rs)，第 923–933 行 |
| F-11 | `yijie-skills` 已有确定性 ZIP、显式文件清单、入口校验、来源摘要及 manifest schema 校验，可复用这些机制包装专家入口和参考文件 | [package-desktop-skills.mjs](../../../../yijie-skills/scripts/package-desktop-skills.mjs)，第 56–69、84–118、121–172 行 |
| F-12 | 当前 Skill manifest 的 `model-only` 强制无网络、无文件权限、无工具；按需用文件工具读取知识库不符合这个声明 | [skill-bundle-manifest-v2.schema.json](../../../../yijie-skills/contracts/skill-bundle-manifest-v2.schema.json)，第 200–223 行 |
| F-13 | Skill UI 只接安全投影，不允许 archive、path、root、digest、skillcontent、token 等字段；现有本地安装事实不来自前端布尔值 | [skill-marketplace.ts](../../../../yijie-desktop/src/domain/skill-marketplace.ts)，第 51–75、134–148 行；[skills/host.rs](../../../../yijie-desktop/src-tauri/src/skills/host.rs)，第 139–155 行 |
| F-14 | 完整知识采集、chunking、embedding、索引、检索、rerank、citation 与 eval 的职责属于 `yijie-knowledge`；一份随包参考 Markdown 不等于已实现 RAG | [ADR-0008](../../adr/ADR-0008-rag-knowledge-service-boundary.md)，第 13–27 行 |
| F-15 | Host 已有同一 thread 的 `SwitchThread`：确认原生 idle/notLoaded/systemError、无待批后 unsubscribe/resume；resume 组合现有权限、模型和市场配置。这是候选复用入口，不证明专家角色覆盖已通过资格 | [chat_models.go](../../../../yijie-agent-host/internal/codex/chat_models.go)，第 142–178 行；[session_protocol.go](../../../../yijie-agent-host/internal/codex/session_protocol.go)，第 597–648 行 |

### 1.2 Assumption 推荐方案依赖的设计假设

| ID | 设计假设 | 失效时的处理 |
|---|---|---|
| A-01 | 首期一个本地会话同一时刻只绑定一名专家；角色持续影响后续提交 | D0 如要求多专家协作，必须另补冲突优先级、执行身份和 UI，不把几个角色文本直接拼接 |
| A-02 | 首期用经适配的专家入口及版本化本地参考资料即可覆盖用户问题，无需向量检索 | 若真实内容评估证明无法稳定找全证据，记录范围缺口；扩展 RAG 前单独设计，不静默引入 embedding 或服务 |
| A-03 | FEAT-129 安装与校验实现可提取必要复用点，保留现有 Skill 行为；专家产品元信息可作为独立版本化扩展 | 若既有包格式不能表达专家身份/依赖，扩源契约与 reader；不修改固定摘要或降低校验来容纳新内容 |
| A-04 | 每次提交都能由 Host 明确绑定专家版本、角色输入和知识引用；移除后未来轮次停止激活专家 | 必须完成 Q-01/Q-02；不能仅凭配置字段存在或生成了请求就判定角色生命周期通过 |

### 1.3 Unknown 实施前待取得的证据

- 固定运行二进制与当前 Runtime 源码是否一致支持所选原生输入路径，以及同一已加载 thread 的角色增加、替换、清除如何可靠生效；具体限制以 `04` 为准。
- 专家入口及知识正文的实际读取、上下文预算、裁剪/超限反馈与引用准确性。不能仅凭 Markdown 能打包就承诺模型已读完整知识库。
- 专家包身份、版本、引用计数和清理机制的最终契约；尚无可供 consumer 固定的 FEAT-158 发行版本。
- 用户提供资料的产品分发许可、样例中的成绩和政策时效。提供文件用于需求研究不等于已批准再分发或核实全部事实。
- 正常重开时，旧专家绑定、历史轮次与当前 Runtime 有效配置之间的兼容证据；现有其他需求的 D4 不自动覆盖专家。
- FEAT-158 新增 Native 能力、持久数据与协议是否需独立 Proposed ADR 补充。已有 ADR 证明复用方向，不替 FEAT-158 批准新范围。

### 1.4 Conflict 必须在设计中消解的差异

| 冲突 | 处理原则 |
|---|---|
| WorkBuddy 的 Plugin 名称及三级目录与易界当前受管 Skill 包/根不同 | 复用身份、版本、资源解耦的思路，实际目录与权限采用易界 Native 管理；不扫描、导入或修改用户的 WorkBuddy 安装 |
| 参考配置可能声明易界没有的模型、工具、hook、长期记忆或自动动作 | 在 `05` 逐项标明支持、适配、移除或待资格；不通过角色文本声称能力存在 |
| 现有 Skill 全局启用，专家需要会话范围 | 新建明确的专家会话绑定语义；不能通过发送前后开关全局 Skill 模拟，也不能让专家隐式进入其他会话 |
| FEAT-157 提交成功会清空本轮连接器选择，专家应持续 | 复用事务和幂等机制，不照搬清空规则；专家绑定单独保留，连接器继续按原有本轮选择执行 |
| “移除专家”容易被误解成清除历史或撤销已发出的调用 | `×` 仅从后续提交停止激活；不删除消息/结果、不承诺模型遗忘、不撤回外部事实；活动/待批/未知出站期间禁止改绑定 |
| 项目旧测试入口可能包含强杀、权限破坏、替换程序或攻击 fixture | 用户长期硬性安全条款优先；先检查所选用例，跳过禁止项并记录原因与影响，不用全套命令名作为绕过理由 |

## 2. 方案比较

| 方案 | 可复用部分 | 主要代价与风险 | 结论 |
|---|---|---|---|
| A 直接使用 Runtime 原生 Plugin | 原生插件识别、资源组织和加载入口，如固定 Runtime 确实支持 | 宿主产品的 Plugin 文件不代表易界协议兼容；来源/版本/生命周期资格、角色清除、权限与现有市场映射仍缺证据；升级或更换固定 Runtime 会扩大范围 | 不作为首期主路径。保留为以后经精确来源和正常资格验证的优化候选 |
| B 受管专家包适配 | `yijie-skills` 内容/打包，FEAT-129 安装校验，Native SQLCipher、FEAT-157 冻结提交、现有 Chat/Host/Codex/审批/历史 | 需要最小专家元信息、会话绑定、版本化提交与原生上下文适配；需补旧包/旧聊天消费者兼容 | **推荐**。增加用户可理解的专家能力，保持已有执行和数据边界 |
| C 完整 RAG 专家平台 | `yijie-knowledge` 的既定职责、将来可支持多来源检索与时效管理 | 要增加数据源、分块/embedding/索引、检索质量、服务部署、费用和授权，不是首期一份参考资料的必要前提 | 首期不选；确有跨文档检索需求时按独立范围设计 |

B 方案不是把所有专家伪装成现有全局 Skill 条目。推荐在同一受管资源机制上明确“专家”产品身份，并避免默认隐式全局调用；是否以入口 Skill、受管角色输入或其组合激活，由固定 Runtime 的资格结果决定。角色和业务内容留在 Skills，Host 只做可信适配，不成为新的 Agent 编排平台。

与 `04` 对齐的候选投送方式是：专家用途的受管资产排除出普通全局 Skill 投影；新会话使用原生 `thread/start`，已有会话复用同 ID 的 `SwitchThread` 与 `thread/resume`，在完整既有 `baseInstructions` 上组合专家角色，并保留当前模型、权限模式及 MCP 配置。解除专家时显式恢复完整的普通基础指令，不依赖 `developerInstructions`、`null` 或字段省略实现清除。原生已加载/仍订阅 thread 可能不采用覆盖，因此必须先通过 Q-01/Q-02，不能只检查请求已发出。

## 3. D0 推荐决策登记

以下均为 **Proposed / 待 Owner D0 确认**。本轮用户确认“只需求设计”，不构成这些产品和技术选择的实施批准。

| ID | 推荐决定 | 条件与可见影响 |
|---|---|---|
| DEC-158-01 | 首期 `demo_fast + local`，采用 B 受管专家包适配 | public/production、多设备同步、用户任意 Plugin 导入、多人共享和完整 RAG 不在首期 |
| DEC-158-02 | 一会话一专家，选择在会话内持续，普通无专家聊天维持原行为 | 新对话与各已有会话绑定隔离；计划草案/定时任务不隐式继承 |
| DEC-158-03 | 每次提交冻结专家身份、精确包/角色/知识版本及不可变引用；会话默认绑定是下一次提交的意图 | 与消息/outbox 同事务；已受理任务不能因后续升级、卸载、切换页面而换内容；重复提交返回原回执 |
| DEC-158-04 | `×` 解除专家绑定，从后续轮次生效；替换绑定也只作用后续提交 | 当前轮活动、待处理审批、存在未解决的相关 outbox/回执不确定时禁止改绑定；可先走现有正常停止/处理审批流程，确认状态后再改 |
| DEC-158-05 | 保留历史专家显示快照与既有消息；不把历史快照用作执行授权 | 解除不删除历史、不回滚外部操作、不承诺已进入上下文的内容被遗忘；新发起需重新核对当前可用性 |
| DEC-158-06 | 首期专家以经适配内容和本地参考材料交付，明确证据时效及来源 | 不承诺“资深”角色具有人类真实经营履历；材料中的收益目标、政策、经验阈值不转为事实保证 |
| DEC-158-07 | 专家需要的连接器复用 FEAT-157 管理/本轮选择/逐次审批，普通 Skill 复用 FEAT-129 | 安装专家不代替配置连接器、账户授权、模型调用预算或一次执行批准；不自动启用、切换权限或调用外部服务 |
| DEC-158-08 | 复用 Native app-data、安装完整性校验、SQLCipher/worker/outbox/Coordinator | 不增加第二套产品数据库；专家包路径、内容与数据库密钥不下发 Renderer；具体目录与 migration 由 `04` 定义 |
| DEC-158-09 | 专家包升级不静默改变会话已选版本；新版本由用户明确采用，历史仍指向原版本 | 若旧版本已不可执行，应阻断下一次专家提交并给出升级或解除入口；不能偷偷回退普通聊天 |
| DEC-158-10 | 新权限沿用现有 `plugin.read`/`plugin.manage` 和聊天执行权限的职责，再由 Host/Native 校验资源 | 该复用映射需 D0 确认；若必须新增公开 capability，先改权威契约。前端可见按钮不是权限事实 |
| DEC-158-11 | 第一次实现按 `breaking` 保守评审，采用新版本或兼容扩展，不多仓硬切 | 当前 closed projection、固定包目录和 durable replay 的未知兼容风险尚未解除；后续只有证据充分才重分类 |
| DEC-158-12 | 只采用正常、非破坏性的开发和验证 | 禁止强杀制造故障、替换/伪装运行程序、破坏权限、攻击性资源/归档或注入测试；安全验证不能替未执行项目伪造 PASS |

本轮纯需求文档的实际改动 `contract-impact = none`：没有改变产品代码、IPC、API、Runtime、持久格式或执行权限。上表 DEC-158-11 是未来实现的保守分类，不能把文档 `none` 带入实现。

## 4. 实施前资格项

这些项目是事实资格，不是额外产品范围。D0 选择方案后仍须取得对应证据；任何不通过项均不得由 UI 成功提示掩盖。

| ID | 资格 | 正常验证方法与通过条件 | 当前状态 |
|---|---|---|---|
| Q-01 | 固定 Runtime 原生角色输入 | 核对固定产物、canonical schema、Host 请求路径；普通新 thread 和已有 thread 的无副作用配置/输入往返。涉及模型的行为验证另取得额度 | NOT RUN；源码事实见 `04` |
| Q-02 | 会话绑定、替换和清除 | 正常连续提交、正常结束、用户显式切换/解除，再验证后续提交只携带当前角色；不能依靠 `null`/字段省略的猜测；旧角色文本仍存在于历史的限制明确 | NOT RUN |
| Q-03 | 不可变版本与同事务提交 | 用普通本地合成数据验证消息、专家快照和 outbox 原子保存、相同 operation 回执重放、不同意图冲突、合法升级前后版本固定；不制造崩溃 | NOT RUN |
| Q-04 | 专家入口不会全局隐式激活 | 同时打开普通与专家会话，核对 Host/Runtime 投送范围；未选专家时不自动注入专家入口；既有普通 Skill 开关保持原语义 | NOT RUN |
| Q-05 | 知识读取与引用 | 用获授权的普通参考材料完成真实提问，检查相关章节、版本、来源、缺失证据与超限提示；结构校验不替代模型质量评估 | NOT RUN |
| Q-06 | 连接器和审批兼容 | 无连接器时不发业务调用；有选择时原有资格、ask 模式和逐次批准保持；真实第三方查询、发现和模型调用分别需明确预算 | NOT RUN |
| Q-07 | reader、安装及清理兼容 | 普通安装/卸载/版本切换、正常退出重开；新 reader 读旧记录，允许回滚的 reader 可读新历史；包有未完成提交引用时不被清理 | NOT RUN |
| Q-08 | 产品状态与原生视觉 | canonical 入口、亮暗主题、`1180×760`、键盘/焦点，检查缺依赖、加载、只读历史、忙、待批、自然不可用和正常重试；浏览器 mock 不计原生 D4 | NOT RUN |

Q-01/Q-02 失败时先调整最小 Host/原生适配设计并说明影响；不能擅自升级 Runtime、换程序、重建聊天历史、添加平行运行引擎或把专家解除改成仅隐藏标签。

## 5. 仓库职责与技术依赖顺序

### 5.1 职责分配

| 仓库 | 本需求拟承担职责 | 必须复用及明确边界 |
|---|---|---|
| `yijie` | 需求、决策、跨仓来源、D0/D4 和限制记录 | 不承载产品实现；不改已有 Accepted ADR 来假装专家获批 |
| `yijie-contracts` | 专家安全目录/绑定/提交/历史投影的易界公共边界、版本、生成及 conformance | 修改唯一权威源后生成；Codex 原生字段仍以固定 Runtime canonical schema 为源；不直接手改 Desktop/Host generated DTO |
| `yijie-skills` | 专家内容、包元信息、参考资料、适配映射、示例和 eval | 复用 [打包器](../../../../yijie-skills/scripts/package-desktop-skills.mjs)；不实现客户端、OAuth、数据库或 RAG 服务 |
| `yijie-agent-host` | 受管包解析/安装复用、专家输入与原生 thread/turn 适配、执行前资格和映射 | 原生生命周期入口见 F-15，受管安装与详情见 `04`；不复制专家业务正文为代码、不另存会话正文或新建 Agent 执行状态机 |
| `yijie-desktop` | 专家目录/详情/安装管理、会话绑定、输入区标签、安全 IPC、持久快照和历史展示 | 复用 Skill/Connector 市场组件与状态模式、SQLCipher/worker/outbox/Coordinator、现有 Chat/审批/附件/Artifact；不让 Vue 解析本地包或拼接 Runtime 配置 |
| `yijie-codex` | 默认仅作为固定 Runtime 权威源进行资格核对 | 首期不修改内核；若必须扩原生协议，另明确最小变更和构建来源，先形成 Runtime 候选再同步兼容投影 |
| `yijie-connectors` | 已有连接器、凭据及真实工具批准边界 | 不复制专家配置中的外部端点，不为专家重复建设 OAuth/MCP；没有新已确认连接器需求时无需改代码 |
| `yijie-knowledge` | 仅在后续明确完整检索需求时承担 RAG | 首期不因参考文档名称含“知识库”而新增服务、embedding 或数据库 |

### 5.2 连续实施的依赖顺序

本需求采用 `demo_fast`，**不建立治理切片**。以下只是一次完整用户结果的技术依赖顺序，不允许把某个模块完成换算为整体可用。

1. **确认 D0 与真实基线**：评审产品流程、DEC-158-01 至 12；重新读取各仓 AGENTS/README/安全和相关设计，核对分支、remote、状态、来源 pins，保护已有改动。先完成 Q-01/Q-02 的正常资格设计；任何模型/外部步骤在单独预算后执行。
2. **先改权威源**：按 `04` 明确身份、版本、绑定 revision、提交、历史与错误的唯一权威；更新 Contracts 源、成功/自然失败示例、生成器/兼容检查。Runtime 如确需扩展，遵循 Runtime canonical schema → Contracts 兼容投影 → consumers。持久私有 schema 留所属仓 migration，不复制为影子公共 DTO。
3. **内容与受管包**：按 `05` 完成角色/工具/知识映射和来源许可；复用确定性打包、摘要、安装收据、启停/卸载与扫描。支持新专家元信息的 consumer 先就绪，再产生并启用新格式；固定目录数量/摘要随真实来源合法升级，不降低校验。
4. **Host 与 Native 接线**：接入原生输入路径、会话绑定验证和引用保护；在同一个 SQLCipher worker/transaction 写消息、专家版本快照和 outbox；使用既有 Coordinator 调度；保留无专家旧入口，专家不支持时明确拒绝，不能掉回旧入口丢字段。实现前确认下一 migration 编号，不改历史 migration。
5. **产品界面与共享草稿**：复用现有市场/详情、输入区资源菜单、token/Yj/Naive 和消息/工具/审批组件。专家会话绑定持久，未发送选择意图与正文按会话隔离；导航不丢草稿，accepted 只清当次输入，保留专家绑定。版本升级、停用、卸载后的显示与执行资格分开。
6. **正常验证与真实闭环**：执行审查过的 focused checks、兼容性和正常重开；采用 canonical 日常入口完成全部 Must AC 和代表性正常恢复。模型质量、真实外部服务与本地结构验证分别记账，任何未执行项不得算 PASS。只在同一次 fresh run 满足验收时记 D4。
7. **交付固化另行授权**：记录精确来源和各仓 diff；Git commit/push、tag、签名发布、公开或生产激活不由本需求草案自动授权。普通本地候选不冒称发布物。

## 6. 常规验证入口与证据要求

以下是从现有仓库读取的入口，**本轮未执行**，也不是不经审查直接跑全套的命令清单。实施前须检查脚本及选定测试是否含用户禁止的行为，选择已有 safe/focused 入口；若没有，先建立不含禁止行为的精确普通用例清单，不更改真实程序来造假环境。

| 仓库 | 现有入口 | 适用范围和限制 |
|---|---|---|
| `yijie` | `pnpm lint`、`pnpm test`、`pnpm feature:audit`；[package.json](../../../package.json) | 元仓结构与需求包检查；检查结果不代表产品实现。根 `make lint/test` 会调兄弟仓脚本，本轮不把它当文档检查捷径 |
| `yijie-contracts` | `pnpm generate:safe`、`pnpm check-generated:safe`、`pnpm lint`、`pnpm breaking`；[package.json](../../../../yijie-contracts/package.json) | safe 入口跳过 Skill fixture 生成；对所有适用已登记基线做 breaking。新专家 family 的 focused generate/check/conformance 在实施时随源定义，不预造一个已存在命令 |
| `yijie-skills` | `make lint`、`make test`、`make package`；[Makefile](../../../../yijie-skills/Makefile) | 先检查具体测试；package 是本地候选，不是发布授权；现 `run-evals.mjs` 的数据结构检查不代表模型质量 |
| `yijie-agent-host` | `make lint`、`make contract-check`；已有 `make test-feat136-safe`、`make test-feat137-safe`、`make market-daily-host-test`；[Makefile](../../../../yijie-agent-host/Makefile) | 旧特性回归按相关性选取；新增专家正常用例先有精确名单。旧 safe target 名称不自动证明未来新增用例安全；宽泛 `make test` 不未经审查执行 |
| `yijie-desktop` | `make lint`、`make test`、`make build`；`pnpm docs:build`；[Makefile](../../../../yijie-desktop/Makefile)、[package.json](../../../../yijie-desktop/package.json) | 代码变更按仓规则完成适用检查，但 Cargo/前端测试须先审查并排除禁止行为，记录未执行范围；文档站构建不等于窗口视觉验收 |
| Desktop canonical 入口 | `pnpm tauri:dev` / `pnpm tauri:demo-fast` / `pnpm tauri:demo-fast:app` | 均走项目既有启动器；本轮不运行。应用停止走正常退出和自身清理，无法安全退出时停止并报告，不强杀 |

验证证据至少分别记录：命令与选定用例、源码/包/Runtime 来源、实际环境、模型及外部额度、真实结果、未执行项/原因/影响。未知回执保持未知；UI 标签到位、静态 schema 通过、打包成功均不证明专家真正激活或知识引用正确。

## 7. 回滚、撤销与既有功能保护

### 7.1 会话与版本生命周期

- **解除与替换**：只允许在会话无活动轮、无待批、无相关未解决出站或不确定回执时提交绑定变更；Native/Host 再次校验，不只依赖按钮 disabled。变更后下一次提交冻结新绑定或显式无专家，旧轮保持原快照。
- **已受理提交**：固定精确内容和身份；后续停用、卸载、升级不得把待处理提交换成另一版本或普通聊天。若无法继续执行，沿现有机制呈现明确失败/不可用/待确认，不猜测已执行、不自动重发。
- **升级**：当前会话继续使用已选择的版本，直到用户明确采用新版本；旧包有活动/待处理引用时保留所需不可变内容。卸载和清理对包引用、历史展示、执行资格分别处理，不删除历史来腾出清理条件。
- **重开**：读取已保存会话绑定与历史，但执行前重新核对当前包、能力、权限和 Runtime；历史显示不恢复一次性工具批准，也不把旧连接器 ready 当实时事实。
- **删除会话**：延续既有会话删除职责；仅在现有删除完成语义下释放其专家引用。不得因此卸载全局共享包、其他会话所需内容或连接器凭据。

### 7.2 功能回退

1. 首选关闭新专家选择/新 writer，停止接纳新专家提交；保留兼容 reader 和历史显示。现有专家绑定会话明确提示当前不可继续，而不是静默转普通聊天。
2. 正常完成或停止现有轮次与批准流程，逐项确认 outbox/回执；存在 unknown 就保留 unknown。不能重放旧输入来“恢复结果”，也不能用强杀解除忙状态。
3. 数据库仅做前向兼容。回滚代码必须能读取已产生的新记录，不能降低 `user_version`、改旧 migration、复制日常数据库或清空用户历史以让旧版本启动。
4. 恢复包版本只使用来源固定、可复现且已核对兼容的受管内容；已受理任务仍引用原版本。禁止替换用户提供、已签名/发布/受审计或来源不明的程序；正常标准构建只写当前项目自己的开发产物。
5. 无法安全复用固定 Runtime 时，保持新能力关闭并报告资格缺口。未经新授权不升级 Runtime、不引入第二个运行器、不改变 Accepted ADR。

### 7.3 必须保留的既有能力

- 普通无专家 Chat、附件、模型意图、工作空间、Artifact、原生工具展示、停止与重开继续走既有路径。
- FEAT-132 的原生 Thread/Turn/Item 执行事实和 Native 唯一显示缓冲不改为自建 reducer、正文对账或自动封口。
- FEAT-129 的普通 Skill 全局安装/启停语义与来源校验保留；专家不可造成跨会话隐式激活。
- FEAT-152 的权限模式语义、FEAT-157 的连接器本轮选择/凭据/逐次批准边界保留；不恢复已退役的 FEAT-137 或旧 Sorftime 专用执行路径。
- 已有历史、只读访问、任务删除、计划草案及定时任务保持原功能范围；不把“会话持续专家”隐式传播为定时执行授权。
- 任何源码、用户数据、Keyring、WorkBuddy 原目录与已有未提交改动都不因专家功能被清理或覆盖。

## 8. 停止条件与当前交付状态

当前只交付需求设计；所有产品实施、运行时资格、模型行为评估、真实服务及 D4 状态均为 **NOT RUN / pending**。后续 12 小时目标、16 小时停点沿用项目 `demo_fast` 时间盒，不承诺外部资格一定能在此时限内取得。

30 分钟无新事实先扩大只读诊断；90 分钟同一核心阻塞评估最小适配；非核心验证 120 分钟登记限制；核心阻塞 240 分钟重新评估架构或请 Owner 决定范围。未经 Owner 决定不降低 Must AC。

以下情况停止依赖步骤并如实记录：固定 Runtime 不能满足可清除的绑定语义、身份或包来源不明、需未授权模型/外部调用、需改 Accepted 安全边界、发生无法安全退出的进程，或验收只能依靠禁止行为。仍可继续不依赖该缺口的文档及正常静态工作，不伪造完成或 PASS。
