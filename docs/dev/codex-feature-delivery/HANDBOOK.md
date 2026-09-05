# Codex 双模式需求交付手册

## Profile 路由

新需求使用 schema v3，并在创建时固定：

- `delivery_profile: demo_fast`：默认。目标是 8–16 小时内完成真实可用 Demo。
- `delivery_profile: production_hardened`：显式选择。执行后文完整生产生命周期。
- `exposure: local | public`：决定是否需要公开 Demo 检查，不改变 Profile 本身。

历史 schema v1/v2 保持原语义；schema v2 视为历史 `production_hardened`，不会自动降级为 Demo。

## A. demo_fast：真实服务快速闭环

### Owner 永久终止（未完成验收）

Owner 明确决定不再实现时，schema v3 可将 `feature.status` 与 `implementation.status` 设为 `terminated`，并记录 `termination.owner/confirmed_at/reason/permanent: true/acceptance_passed: false/implementation_resumes: false`。确认时间不推定最初关闭日期。历史验证证据、Must AC 和失败结论保留；不再为该需求实施、补跑验收或消耗调用额度。永久终止不能声明 D4/DP/G4–G6，不能重新变为 active。检查器验证终止记录及决策不可逆性，不把关闭当作验收通过。归档恢复只用于审计和误删恢复。

### A0. 产品、逻辑与 UX 一次定稿

Codex 在实现前完成一个推荐方案，包含：

- 目标用户、问题、真实用户结果、In/Out scope；
- 主流程和必要业务规则；
- 最多 5—10 条 Must AC；
- `idle/loading/success/empty/error/retry/cancel` 中每个状态的行为；
- 布局、主次操作、反馈、预览/保存和视觉方向；
- 真实代码入口、受影响仓库和工作区已有改动；
- `contract-impact`、权威源和 source-first 实施顺序；
- 付费调用、破坏性操作、生产写入和真实数据边界。

不影响用户目标、安全、数据、成本或不可逆架构的未知项，由 Codex 给出推荐默认值继续，不逐项等待。

退出条件 D0：逻辑与 UI 没有阻断性空洞；Must AC 可操作判断；Contract First 和外部授权边界明确。

### A1. 整个需求连续实现

不建立治理切片，不执行 per-slice G3。Codex 可以按以下技术依赖顺序编码：

```text
权威契约/官方第三方协议
  → provider/domain/storage
  → event/API boundary
  → consumer/UI
  → focused checks
```

这只是编码顺序，不是多个交付 Gate。最终只用完整用户结果判断完成。

保留的工程要求：

- 契约源先于下游，生成物通过正确入口产生，不复制影子 DTO；
- 只补能保护核心逻辑、错误映射和真实边界的 focused tests；
- 不夹带无关重构、全仓格式化或未经批准的依赖升级；
- 不使用真实 PII，不泄漏 secret，不超出付费/外部副作用授权；
- 实现完成后立即启动正常真实服务，而不是先扩建治理 harness。

明确延后到公开/生产升级的内容：完整性能、安全、韧性、migration 矩阵、baseline breaking matrix、
harness qualification、三项拆分 E2E、全仓 full-green、灰度、Dashboard、发布/回滚和线上观察。

### A2. 真实服务启动与 Bug 循环

`exposure=local` 默认先执行 ADR-0018 `local_demo_direct`：canonical launcher 自动绑定固定本地
identity/tenant/capabilities、启动必要 sidecar 并进入首个业务主页面。正常 Demo 启动不得显示登录页、
打开 OIDC 浏览器或要求账号密码。Host 内部 token 与 Provider Key 属于自动管理的机器凭据，不等于
用户登录；public/production 不适用此例外。

```text
正常启动真实服务
  → 检查 readiness
  → 操作真实 happy path
  → 检查最终用户结果/Artifact
  → 验证一个代表性 failure/retry
  → 有 Bug：定位、修复、重启、复测
  → 一次 fresh run 中全部 Must AC 通过
```

真实服务是产品实际入口、真实 Runtime/Provider/数据库/Host/Desktop 组合。browser-only、mock-only、
synthetic Artifact、直接 seed Store 或第二个测试 App 不能满足 D4。

### A3. 时间盒与停止条件

| 条件 | 必须动作 |
|---|---|
| 30 分钟没有新增事实 | 停止猜测式局部补丁，读取真实日志和完整调用链 |
| 90 分钟同一核心阻塞 | 采用最简单方案、关闭非核心花活或提出一个 workaround |
| 非核心验证累计 120 分钟 | 登记限制并降级，不继续阻断业务结果 |
| 核心路径累计 240 分钟仍不可用 | 更换架构、缩小 MVP 或请求一个关键决定 |
| 总工时达到 16 小时仍未 D4 | 停止扩建流程，重新定范围和估时 |

以下情况无论 Profile 都要立即停止并请求明确授权：真实敏感数据、生产写入、破坏性 migration、
超出预算的付费调用、公开部署、commit/push/tag 或会改变安全/契约权威边界的决定。

### A4. D4 完成标准

- 正常本地启动命令和 readiness 成功；
- fresh local 启动零登录交互，并直达实际业务主页面；
- 所有 Must AC 在一次 fresh run 中 PASS；
- 真实 happy path 产生可观察/可保存结果；
- 一个代表性错误能正确提示并重试或恢复；
- focused build/test/check 通过；
- Loading/error/retry 不会困住用户；
- 有截图、录屏、Artifact 或脱敏 request ID；
- 完整 diff/status 已检查；
- 没有崩溃、数据破坏、秘密泄漏、死循环或阻断使用的 Bug；
- 已知非阻断限制被明确记录。

D4 表示“本地真实 Demo 可用”，不表示 G4、Production Ready 或 Delivery Complete。

### A5. DP 公开 Demo

`exposure: public` 在首次对外访问前必须额外验证：

1. secret 只在服务端环境或 Keychain，不进入客户端、源码、日志和错误；
2. 鉴权与数据边界适合公开访问，或公开服务不处理受保护数据；
3. 输入、文件、URL、大小与超时有边界；
4. 付费 API 有调用频率、并发和成本上限；
5. 错误不泄露敏感内容或调试栈；
6. 有最简停止/恢复方式；
7. 公网入口执行一次真实 smoke。

以下任一出现时，不再只用 DP，而应建立显式 `production_hardened`：付费用户、SLA、多租户/PII、
重要持久数据、不可逆 migration、合规、团队值班或业务依赖。

---

## B. production_hardened：完整生产生命周期

## 一、工作方式

### 1. AI 的正确定位

在生产工程中，Codex 应被视为：

- 高速代码调查员；
- 设计与文档草拟者；
- 在明确边界内工作的实现者；
- 测试与验证执行者；
- 可以发现问题、但不能自我批准的 Reviewer。

Codex 不是业务 Owner、安全批准人、生产事实来源或测试结果的替代品。

### 2. 证据优先

以下内容必须由可复核证据支持：

- “仓库是干净的”需要 `git status`；
- “测试通过”需要实际命令和输出；
- “契约兼容”需要基线检查和 consumer 验证；
- “数据库可回滚”需要 migration/reader 兼容和回滚演练；
- “生产可用”需要部署、探针、指标和关键路径 smoke；
- “模型效果变好”需要固定数据集、模型版本和 Eval 对比。

没有执行的验证必须写成“未执行”，不能用推断替代。

### 3. 文档不是事后说明

需求交付目录是 Codex 的上下文包，也是工程审查和发布证据。文档随着事实变化持续更新：

```text
需求事实 → 设计约束 → 实现切片 → 验证证据 → 发布与回滚
```

不要求为低风险任务制造大量文档，但任何被省略的材料都必须有“为何不适用”的理由。

---

## 步骤 0：建立需求交付工作区

### 目标

为需求建立唯一身份、责任人和可持续更新的上下文目录，避免需求散落在聊天记录里。

### 要做什么

1. 分配 Feature ID 和简短名称。
2. 创建 feature package。
3. 记录仓库、分支和已有工作区改动。
4. 明确谁负责需求、技术、评审和发布。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `00-feature-brief.md` | 保存需求入口、目标、非目标、Owner 和当前状态 | 由需求负责人提供事实，Codex 按模板整理 |
| 初始 Git 状态记录 | 防止覆盖用户改动和在错误分支开发 | Codex 实际运行 `git status`、`git branch`、`git remote` 后填写 |

### 退出门禁

- Feature ID 唯一；
- Owner 明确；
- 工作区已有改动已记录；
- 未在未知 dirty worktree 上直接开始批量修改。

---

## 步骤 1：澄清需求与验收标准

### 目标

把“想要一个功能”变成可判定是否完成的需求。

### 要做什么

1. 写清用户、场景、触发条件和用户价值。
2. 区分目标与非目标。
3. 把验收标准写成可观察行为。
4. 覆盖成功、失败、权限不足、空数据、超时和部分成功。
5. 记录性能、合规、可访问性、兼容性和成本约束。
6. 把未决问题列出来，不让 Codex自行猜测。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `01-requirements.md` | 需求真相源，指导设计、测试和验收 | 人提供业务语义，Codex 将自然语言转成场景和 Given/When/Then |
| Open Questions | 阻止隐含假设进入实现 | Codex 从歧义、缺失字段和冲突规则中提取，人逐项确认 |

### 文档质量要求

好的验收标准：

```text
Given 用户有 report:read 权限且存在 50 条任务
When 用户按最近 7 天导出 CSV
Then 返回 UTF-8 CSV，包含 50 条授权范围内的记录，审计一次导出行为
```

坏的验收标准：

```text
导出功能正常、体验良好、没有 Bug
```

### 退出门禁

- 每个验收标准都可通过测试或人工步骤判定；
- 非目标明确；
- 阻塞性问题已回答；
- 需求负责人确认。

---

## 步骤 2：扫描现状与评估影响

### 目标

理解真实代码和系统边界，避免 Codex 根据目录名或文档想象实现。

### 要做什么

1. 阅读每个受影响仓库的 `AGENTS.md`、README、SECURITY、CONTRIBUTING、架构与 ADR。
2. 检查分支、远端、工作区状态和最近提交。
3. 找到真实入口、调用链、持久化、测试和发布脚本。
4. 识别 producer、consumers、数据方向和权威源。
5. 识别 API、事件、SDK、数据库、缓存、配置、Runtime、第三方和 UI 状态影响。
6. 搜索占位实现、TODO、mock、重复 DTO 和未接通路径。
7. 标记依赖的环境、外部服务、真实账户和成本。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `02-impact-assessment.md` | 记录受影响仓库、边界、风险和现状证据 | Codex 只读扫描后草拟，技术负责人核对 |
| Repository Status Snapshot | 保护已有改动，明确分支与基线 | 由实际 Git 命令生成 |
| Dependency/Data-flow Map | 找出跨组件发布顺序和失败传播 | 从代码调用与契约生成，不能只依赖架构图 |

### Contract Impact 分类

每个需求必须选择一个最高风险分类：

| 分类 | 判断 |
|---|---|
| `none` | 不改变跨进程、跨仓、跨版本、持久化或重放边界的可观察行为 |
| `additive` | 增加能力，不改变既有交互解释，并已验证方向兼容 |
| `semantic` | 形状可能不变，但默认值、错误、权限、顺序或行为语义改变 |
| `breaking` | 任一仍受支持 producer/consumer 可能失败或错误解释 |

不要因为 DTO 没变就选择 `none`。

### 退出门禁

- 受影响仓库没有遗漏；
- 现状事实有文件或命令证据；
- contract-impact 已分类并说明方向；
- 未把占位实现当成已完成能力。

---

## 步骤 3：关闭关键决策与风险

### 目标

在写代码前解决会改变架构、安全或数据语义的决策。

### 必须停下来确认的事项

- 认证、会话、租户与 RBAC；
- 数据库 schema、保留期、回填和删除；
- token、secret、PII 与数据出境；
- 高风险操作、审批、幂等与审计；
- 新基础设施、队列、缓存、云服务和外部依赖；
- 第三方 API、SDK、许可、费用和生产账户；
- Runtime、模型、embedding 与 Eval 阈值；
- breaking change、兼容窗口和发布顺序。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `03-decisions-and-risks.md` | 集中记录已确认决定、风险和批准 | Codex 列选项与权衡，Owner 选择并签认 |
| ADR（条件性） | 保存高成本、跨团队或难回滚决定 | Codex 从决策记录起草，架构 Owner 审核 |
| Threat/Data Review（条件性） | 明确信任边界、数据等级和攻击面 | 安全负责人提供策略，Codex映射到数据流 |

### 风险处理格式

每项风险包含：

- 风险事件；
- 触发条件；
- 影响；
- 预防控制；
- 检测方式；
- 回滚或恢复；
- Owner。

### 退出门禁

- 阻塞性决策均有明确结论；
- 安全和数据分类已确认；
- 未决项不会迫使实现者自行发明业务语义。

---

## 步骤 4：先完成契约设计与兼容计划

### 目标

让所有独立发布单元在实现前共享同一边界语义。

### 适用内容

- HTTP/RPC/SSE/WebSocket；
- 事件、队列和 durable payload；
- MCP/tool schema；
- SDK 公共签名；
- 认证、权限、幂等、错误和审计语义；
- 跨版本持久化/重放格式。

服务私有数据库、部署配置、Runtime 上游和第三方协议使用各自权威源与兼容方法，不能伪造中央契约。

### 要做什么

1. 确定权威源、Owner、producer 和全部 consumers。
2. 设计请求/响应、错误、权限、幂等、分页、顺序和重试。
3. 分析请求、响应和事件的兼容方向。
4. 列出所有 supported baselines、generator 和实际检查命令。
5. 规划 SDK/类型生成、漂移检查和下游 pin 格式。
6. 取得业务语义、Contracts Owner 和 Consumer Owner 的设计评审。
7. 写清合并、部署、启用、兼容窗口和回滚顺序。

本步骤只冻结设计，不把尚未生成的 commit、tag、digest 或检查结果写成事实。权威源落地、generate、breaking check 和不可变候选引用在步骤 9 的第一个切片执行。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `04-contract-change-plan.md` | 保存契约分类、权威源、consumer 和方向性发布计划 | Codex 根据影响扫描起草，Contracts/Consumer Owner 评审 |
| `04A-temporal-contract-matrix.md` | 固定 producer、持久化、通知、replay、terminal、cleanup 的顺序与不变量 | 从真实调用链建立 Phase/Invariant/Test ID，Producer/Persistence/Consumer Owner 评审 |
| OpenAPI/Proto/Schema/Event 设计稿 | 让各方在编码前审查边界语义 | 从权威源结构起草；在此阶段不手写下游 DTO |
| Compatibility Test Plan | 规定如何证明结构与实现方向兼容 | 列出真实 breaking、generate-drift、producer/consumer conformance 命令和基线 |

### 退出门禁

- 契约草案和失败语义完整；
- breaking/semantic 影响已完成人工设计评审；
- 不可变引用、generator、baseline 和 consumer pin 方案明确；
- 不允许“先写临时 DTO，之后再补契约”；
- 尚未执行的 generate/breaking/conformance 明确标记为 `NOT RUN`。
- 每个阻断时序不变量已映射到能在错误实现下失败的 executable temporal conformance；完全不适用时记录 `N/A + Owner 理由`。

---

## 步骤 5：完成技术设计

### 目标

把需求和契约转成可实现、可运行、可恢复的系统设计。

### 设计必须回答

- 模块职责与依赖方向；
- 关键流程和状态机；
- 数据模型、事务和一致性；
- 并发、幂等、超时、取消、重试和部分失败；
- 权限、租户、数据隔离和脱敏；
- 日志、指标、trace、告警和审计；
- migration、双读/双写、回填和回滚；
- 容量、性能、费用和降级；
- feature flag、灰度和兼容窗口。
- 最小 production vertical、production bootstrap、真实平台与 runtime harness 的边界；
- process、连接、WAL/spool/temp、handle 与 run-root 的 teardown 所有权和顺序。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `05-technical-design.md` | 实现的技术真相源 | Codex 基于已确认需求/契约起草，技术负责人审查 |
| Sequence/State/Data Diagram | 揭示时序、状态和故障传播 | 从真实调用链生成并逐节点核对 |
| Migration Plan（条件性） | 保证新旧版本和数据可共存 | 数据 Owner 提供约束，Codex形成 expand/migrate/contract 步骤 |

### 退出门禁

- 正常与失败路径都能解释；
- 新旧版本共存期间行为明确；
- 没有把授权、事务或审批留给 UI/prompt；
- 回滚不依赖临时现场猜测。

---

## 步骤 6：在实现前设计测试

### 目标

先明确什么证据能证明功能正确，再写实现。

### 测试分层

| 类型 | 证明什么 |
|---|---|
| Unit | 纯领域规则、边界和错误分类 |
| Integration | 数据库、队列、文件、网络适配和事务 |
| Contract | 源结构、生成漂移、版本兼容 |
| Conformance | producer/consumer 实际行为符合契约 |
| E2E | 关键用户路径在真实组合中工作 |
| Security | 越权、跨租户、注入、秘密泄漏和审批绕过 |
| Failure/Resilience | 超时、取消、重试、断线、部分成功和恢复 |
| Migration | 空库、旧数据、新旧 reader/writer 和回滚 |
| AI Eval | 固定模型/数据/参数下的质量、安全和回归 |
| Visual/Accessibility | 目标视口、键盘、焦点、主题和可读性 |
| Harness Qualification | 证明 runtime harness 自身能区分 product/harness/platform/gate failure，并正确 cleanup |

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `06-test-plan.md` | 将验收标准映射到测试和环境 | Codex 从需求/设计生成矩阵，测试 Owner 补充真实环境 |
| Test Fixtures Plan | 防止真实敏感数据进入测试 | 按数据分类使用公开、授权或合成数据 |
| Eval Plan（AI 功能） | 防止用主观体验宣称模型效果 | 固定数据集、模型、参数、指标和通过阈值 |

### 退出门禁

- 每条验收标准都有测试或明确人工验证；
- 负向、安全和失败场景不是事后补充；
- 外部服务、真实账户和不可执行项已标注；
- 测试不会访问未知生产资源。
- G2V 所需 harness 的 positive/negative controls、超时、cleanup 与 content-free verdict 已设计；
- 最终 E2E 已拆为 core vertical、accessibility/visual、teardown 三项独立 verdict。

---

## 步骤 7：拆分实现计划

### 目标

将大需求拆成小而可验证、可回滚的切片，控制 Codex 的改动范围。

### 推荐切片顺序

1. 权威契约/类型候选，并在适用时通过 G2A；
2. 资格验证默认关闭的 runtime harness；
3. 在真实平台和 production bootstrap 上完成最小纵向 Walking Skeleton，通过 G2V；
4. 按用户结果拆分后续纵向切片，每个切片同步完成领域、provider、持久化、consumer/UI 中适用部分；
5. 每个切片完成 local、boundary、vertical evidence 并通过自己的 G3；
6. 完成观测、发布开关、兼容清理和文档；
7. G4 前执行完整 core vertical、accessibility/visual、teardown 三项最终 E2E。

实际顺序必须服从数据方向。例如新请求字段先 provider，新增响应 enum 先 consumer 容忍。
不得先横向完成所有 provider/persistence/consumer/UI，最后才第一次运行真实 production vertical。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `07-implementation-plan.md` | 定义切片、文件范围、依赖和验证命令 | Codex 根据设计生成，技术负责人调整依赖 |
| Per-slice Acceptance | 防止切片“代码写了但不可证明” | 每个切片绑定测试、命令和预期 diff |

### 每个切片应满足

- 通常只跨一个清晰边界；
- 可以独立验证；
- 不夹带无关重构；
- 失败时可以回退；
- 明确允许和禁止修改的文件；
- 完成后有可观察结果。

### 退出门禁

- 没有“大包实现整个功能”的任务；
- 关键依赖和跨仓顺序明确；
- 每个切片都有验证方法。
- 每个切片明确 prerequisites、不可变 commit、required local/boundary/vertical evidence 与 freshness 失效规则。

---

## 步骤 8：建立可重复的开发基线

### 目标

证明开始编码前仓库本身可构建、可测试，并分离既有失败与本次回归。

### 要做什么

1. 再次记录 `git status`。
2. 确认工具链和依赖版本。
3. 运行与需求相关的 baseline lint/test/build。
4. 检查本地服务 readiness，而非只看启动命令退出码。
5. 记录无法执行的验证和原因。

### 输出

将命令、版本、结果、时间和环境写入 `08-verification-report.md` 的 Baseline 部分。

### 退出门禁

- 既有失败已记录并与本需求区分；
- 不在错误工具链或未知数据库上继续；
- 不自动清理、reset 或覆盖用户工作区。

---

## 步骤 8A：资格验证 Harness 并通过 G2V

### 目标

在大规模实现前，用最小成本证明真实平台上的 production 组合方向成立，并先证明负责给出阻断
结论的 runtime harness 本身可信。

### 适用性

风险为 high/critical，或涉及跨仓/进程、公共契约、持久化/重放、Runtime/平台、认证/权限、
用户可见工作流语义时，G2V 必须执行。其他低风险场景由 Technical Owner 写
`N/A + 可复核理由`。`contract-impact != none` 时必须先通过 G2A。

### Harness Qualification

在 harness 证据可以阻断产品门禁前，固定其 commit/digest、目标平台、production bootstrap、fixture
和 closed evidence schema，并通过 positive control、negative controls、timeout 与 cleanup。结果必须互斥区分：

- `product_failure`：qualified harness 已到达正确生产观测点，产品行为违反预期；
- `harness_failure`：controller、fixture、断言、证据传输或编排本身失败；
- `platform_failure`：OS/WebView/Runtime/环境前置条件不成立；
- `gate_failure`：checker、allowlist 或治理规则错误拒绝合法实现/证据。

后三类只能阻断验证，不得当成 product failure 后修改业务代码。无法唯一分类时保持
`DIAGNOSIS_REQUIRED`，不得猜测。

### G2V Walking Skeleton

1. fresh build/固定真实制品；
2. 真实目标平台和 production bootstrap/entrypoint；
3. 最小代表性合成或已授权数据；
4. 穿过适用 producer、边界、durable authority、consumer 和用户可观察结果；
5. 验证错误传播与资源释放；
6. 记录完整 commits、harness 引用、环境、命令、时间、结果和未覆盖风险。

禁止用 browser-only、mock-only、第二个测试 App、直接 DB/Store seed、替代路由或伪造 DOM 结果
满足 G2V。允许实现严格受限、默认关闭的最小 skeleton；它不授权大规模业务实现，也不替代最终 E2E。

### 退出门禁

- Harness Qualification PASS；
- G2V PASS，或真实低风险 `N/A + Owner 理由`；
- 失败能唯一归入四类之一，未覆盖风险已登记；
- 未开始与最小 skeleton 无关的横向大规模实现。

---

## 步骤 9：执行 Codex 小步实现循环

### 目标

让每轮 AI 修改都可理解、可验证、可恢复。

### 固定循环

```text
读取上下文
  → 复述当前切片与边界
  → 检查相关代码和测试
  → 先补证明行为的测试
  → 实现最小改动
  → 运行局部验证
  → 检查完整 diff/status
  → 更新验证证据
  → 核对 boundary/vertical evidence freshness
  → 通过 G3/<slice-id>
  → 再进入下一切片
```

### 契约影响需求的第一个切片

当 `contract-impact != none` 时，业务 provider/consumer 代码之前先完成：

```text
修改权威契约源
  → 使用锁定 generator 重新生成
  → lint + test + 全部支持基线 breaking check
  → 人工语义兼容与 Consumer Owner 评审
  → 形成不可变完整 commit/tag/digest
  → 下游固定 version + full commit + digest + generator
```

这一步必须在步骤 8 已记录的干净、可重复基线上执行。只有上述证据齐全，才通过 Gate 2A，
进入最小 G2V provider/consumer Walking Skeleton；大规模业务实现仍须等待 G2V。

### Per-slice G3

每个切片独立记录 prerequisites、各仓完整 commit、local evidence、boundary evidence、vertical
evidence 与 freshness。一个 slice 可包含多个仓库 commit，freshness 必须精确覆盖它自身及所有
transitive prerequisite commits，并绑定适用 contract/fixture、qualified harness 的 commit/digest、
真实平台与 production bootstrap。required evidence 中出现 `NOT RUN`、`FAIL`、`STALE`，或任一
绑定与当前权威值不一致时，切片不得 PASS。

`feature.yaml` 保存机器索引，实际证据只通过 `08-verification-report.md#<EVIDENCE-ID>` 引用；该
ID 在验证报告中必须有且只有一个 `<!-- evidence: <EVIDENCE-ID> -->`。这样既允许报告保留未来切片
的 `NOT RUN`，又不能用任意非空字符串伪造 G2V/G3 evidence。

任何 prerequisite、契约 pin、fixture、runtime/platform、production bootstrap、harness/controller
或实现 commit 变化，都必须按失效规则重算相关 evidence；不能用旧 runtime 结果证明新 diff。

### Codex 必须报告

- 修改了什么以及为什么；
- 实际运行了哪些命令；
- 成功、失败和跳过项；
- 是否生成或修改了 lockfile、SDK、migration；
- 剩余风险和下一切片；
- 是否遇到需要人确认的新决定。

### 停止条件

遇到以下情况立即暂停当前切片：

- 需求与代码事实冲突；
- 需要改变认证、安全、数据或架构决定；
- 需要新增高成本依赖或生产资源；
- 工作区出现未知改动；
- 契约权威源或版本不可用；
- 测试只能通过降低断言、关闭门禁或修改生成物；
- 修复范围明显超出当前切片。

### 三次同类失败熔断

以 Feature、Slice、Gate、evidence/harness ID、责任层和稳定 failure code/checkpoint 识别实质同类失败。
第三次出现后立即进入 `RCA_REQUIRED`：禁止第四次重试、自动 retry、继续局部补丁、延长 timeout
或通过改名规避计数。先扩大只读审计，形成时间线及 `Fact / Assumption / Unknown / Conflict`，
区分 product/harness/platform/gate，列出可证伪候选和最小区分证据，只推荐一个下一动作。
Owner 批准后仅取得一次新执行授权；RCA、授权和该次结果追加为一个 cycle。若仍为同一失败则
立即回到 `RCA_REQUIRED`；不得删除旧 cycle、覆盖历史或重新取得三次额度。

### 输出

- 小步代码与测试；
- 可审查的 diff；
- `08-verification-report.md` 持续证据；
- 需要时更新设计和决策记录；
- 小而单一目的的提交。

---

## 步骤 10：持续集成并完成三项最终 E2E

### 目标

持续证明每个切片在真实边界中的组合仍成立，并在 G4 前形成三项互不覆盖的最终 verdict。

### 要做什么

1. 根据依赖顺序同步不可变契约和生成物。
2. 执行 provider/consumer conformance。
3. 运行数据库、队列、sidecar、Runtime 或第三方 sandbox 集成。
4. 验证 trace、错误传播、取消和重试。
5. 验证 unknown 字段、enum、事件和版本不兼容路径。
6. 运行最终 `core_vertical`：production bootstrap、用户操作、跨组件/durable 链路和最终用户结果。
7. 运行最终 `accessibility_visual`：适用的 axe、键盘、焦点、视口、主题和真实截图。
8. 运行最终 `teardown`：process/connection/checkpoint、WAL/spool/temp、listener、handle 和 run-root cleanup。
9. 检查所有仓库生成前后状态和三项 evidence freshness。

### 输出

| 文档 | 作用 | 如何生成 |
|---|---|---|
| Integration Evidence | 证明跨边界真实组合工作 | 记录实际环境、版本、命令、日志摘要和结果 |
| Compatibility Matrix | 证明部署窗口内版本组合可用 | 测试旧/新 producer、consumer、reader、writer |

### 退出门禁

- 不用 mock-only 测试冒充集成完成；
- 跳过的 sibling、数据库、Runtime 或 sandbox 检查明确标记；
- 端到端失败可以通过 trace 定位。
- 三项 verdict 分别保存 `PASS/FAIL/NOT RUN/N/A`；一项 PASS 不覆盖另一项失败或未运行；
- 所有阻断 harness 均已资格验证，且不存在开放的三次失败熔断/RCA。

---

## 步骤 11：独立审查与加固

### 目标

打破实现对话中的共同盲点，主动寻找“能跑但不安全、不兼容或不可运维”的问题。

### 推荐审查层次

1. Codex 自查当前 diff；
2. 新会话/独立 Agent 只读审查；
3. 领域 Reviewer 审查业务语义；
4. Consumer Owner 审查兼容；
5. 安全/数据/基础设施 Owner 条件性审查。

### 必查问题

- 是否真的满足每条验收标准；
- 是否跨越仓库职责边界；
- 是否存在越权、跨租户、PII 或 secret 泄漏；
- 是否遗漏事务、幂等、并发和部分失败；
- 是否对未知 enum/event 采取错误穷举；
- 是否把固定响应、mock 或占位留在生产路径；
- 是否手改生成物或复制 DTO；
- 测试是否只证明实现本身，而未证明需求；
- migration 是否可在滚动发布期间共存；
- 日志、指标、告警和 runbook 是否能支撑故障定位。

### 输出

- 带严重级别、证据和复现方式的 review findings；
- 修复提交；
- 无法修复的已接受风险和批准记录。

### 退出门禁

- P0/P1 问题清零；
- P2 问题已修复或有 Owner、期限和跟踪项；
- Reviewer 未发现通过降低门禁掩盖问题的行为。

---

## 步骤 12：形成最终验证报告

### 目标

用一份可复核记录证明“代码完成”。

### 要做什么

1. 从干净工作区运行最终 lint/test/build/generate。
2. 检查生成物漂移和完整 diff。
3. 运行适用 integration、contract、E2E、安全、migration 和 Eval。
4. 验证最小/目标视口与可访问性。
5. 复核依赖、许可证、漏洞和制品内容。
6. 确认没有 secret、真实 PII、调试后门和本地路径。

### 输出文档

`08-verification-report.md`，至少包括：

- commit/tag/digest；
- 环境和工具版本；
- 命令与结果；
- 验收标准映射；
- 覆盖的失败路径；
- 未执行项及原因；
- 已知限制；
- Reviewer 结论。

### 退出门禁

- 任何“通过”都能找到证据；
- 工作区干净；
- 未执行项不会被描述为已验证；
- Definition of Done 通过。

---

## 步骤 13：准备并执行发布

### 目标

把代码安全地变成生产行为，并可以快速停止或回退。

### 发布计划必须包含

- 制品、版本、commit、tag 和 digest；
- 合并、部署、migration 和功能启用顺序；
- feature flag 与默认状态；
- 配置、secret、权限和手工步骤；
- 灰度范围和扩量条件；
- 指标、日志、告警和 dashboard；
- smoke 场景；
- 回滚触发器、执行人、命令和数据处理；
- 不可逆步骤和恢复方案。

### 输出文档

| 文档 | 作用 | 如何生成 |
|---|---|---|
| `09-release-and-rollback.md` | 发布运行手册和故障止损方案 | Codex 从设计和验证草拟，发布负责人填真实环境 |
| Release Notes | 告知行为、兼容和限制 | 从 diff、契约、migration 和用户影响生成 |
| Change/Approval Record | 记录谁批准何时发布 | 来自组织真实流程，Codex 不得伪造 |

### 发布执行

```text
plan → review → backup/readiness → deploy → migrate → verify → enable
→ observe → expand or rollback
```

不能因为部署命令退出码为 0 就宣布成功。必须检查 readiness、smoke 和关键指标。

### 退出门禁

- 回滚可执行且责任人在线；
- 告警和 dashboard 在启用前可用；
- 灰度成功标准与停止条件明确；
- 生产变更获得真实批准。

---

## 步骤 14：线上验证与关闭需求

### 目标

确认生产中的用户结果，而不只确认部署完成。

### 要做什么

1. 执行生产 smoke，避免真实高风险副作用。
2. 观察错误率、延迟、资源、业务成功率和审计。
3. 验证无越权、跨租户、重复执行和数据异常。
4. 在灰度窗口内决定扩量、保持或回滚。
5. 更新 runbook、架构、ADR、契约支持窗口和用户文档。
6. 关闭临时 flag、兼容代码和例外时建立后续任务。
7. 复盘实际问题和流程改进。

### 输出文档

`10-delivery-summary.md`：

- 最终用户行为；
- 发布版本与环境；
- 验收结果；
- 线上指标与观察窗口；
- 回滚状态；
- 已知限制与后续 Issue；
- 文档与 Owner；
- 正式关闭时间。

### 完成定义

只有在以下条件同时满足时，需求才算“全部开发完成”：

- 需求验收完成；
- 代码、测试、契约和文档合并；
- 生产发布和 smoke 成功；
- 关键指标稳定；
- 审计与安全证据完整；
- 回滚方案仍有效；
- 遗留问题已明确归档而非隐藏。

---

## 二、按风险裁剪流程

| 变更类型 | 可以合并的材料 | 不能省略 |
|---|---|---|
| 纯文案/内部小改 | Brief + Requirements + Impact 可合并 | 验收、diff、验证、交付总结 |
| 单仓内部逻辑 | Decisions/Design 可合并 | 影响分类、测试计划、验证、回滚 |
| 公共 API/事件/SDK | 不建议合并 Contract 文档 | 权威源、基线、consumer、conformance、发布顺序 |
| 数据库/migration | Design 与 Migration 可同文档 | 旧数据兼容、回填、回滚、集成验证 |
| 高风险写操作 | 不裁剪 | 权限、审批、幂等、审计、安全测试 |
| AI/Prompt/RAG | Design 与 Eval 可组合 | 固定数据/模型、基线、负向用例、质量阈值 |
| Runtime/基础设施 | 使用专属升级/部署 runbook | 不可变来源、环境验证、观测、恢复 |

裁剪应降低文档重复，不得降低工程证据。

## 三、最常见的失败模式

1. 只给 Codex 一句话，让它跨仓实现整个功能。
2. 没有验收标准，最后用“看起来能用”判断完成。
3. 根据文档声称能力存在，不检查真实代码。
4. 先写实现，再补契约和 migration。
5. 只测 happy path，遗漏权限、超时、取消和部分失败。
6. 使用 mock 绿色冒充真实集成，或把 G2V 冒充最终完整 E2E。
7. 让 Codex修改测试以迁就错误实现。
8. 手改生成文件或复制 DTO。
9. 把 localStorage、日志或 fixture 当临时 secret 存储。
10. 多仓同时硬切，没有兼容窗口。
11. 发布前没有指标、告警和回滚触发器。
12. 部署成功后不做业务 smoke 和观察。
13. 把 Codex 的总结当成命令执行证据。
14. 同一失败第三次后继续机械重试或局部补丁，而不进入根因审计。
15. 用单一 E2E PASS 覆盖 accessibility/visual 或 teardown 的 FAIL/NOT RUN。
16. 大范围格式化或重构掩盖业务 diff。
17. 在 dirty worktree 上 reset、覆盖用户改动。
