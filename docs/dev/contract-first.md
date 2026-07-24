# Contract First 跨仓治理规范

## 1. 地位与目标

本文是 ADR-0004 和 ADR-0011 的现行操作规范，适用于易界多仓项目的需求、设计、实现、评审、合并和发布。各兄弟仓库的 `AGENTS.md` 与 CI 负责在本仓执行，不能依赖 `yijie/AGENTS.md` 的目录继承。

Contract First 的目标不是“多写一份 YAML”，而是在 producer 与 consumer 改动前先形成唯一、可评审、可生成、可验证、可版本化的边界语义，防止影子 DTO、协议漂移和多仓硬切。

本文中的“必须”“禁止”是规范性的合并与发布门禁。只有纯内部变更、明确的上游权威源或按第 8 节批准的临时例外可以偏离默认路径。

当前自动化覆盖 `yijie-contracts` 的结构/生成/breaking 门禁，以及本地
`make contract-governance` 对中央与兄弟仓规则是否存在的检查。元仓 PR 模板、
CODEOWNERS、workflow 和 branch protection 不会传播到兄弟仓，PR body 与逐仓
required checks 尚未完全机器化；reviewer 必须执行本文，且不得把当前状态描述为
不可绕过的自动门禁。

## 2. 先做契约影响分类

每个代码、配置、契约和发布变更 PR 必须在实现前标记；纯文档/治理 PR 也选择
`none` 并说明理由：

| 分类 | 判定 |
|---|---|
| `none` | 不改变跨进程、跨仓库、跨版本或持久化/重放边界的可观察行为 |
| `additive` | 增加能力且不改变既有交互解释，但仍需按输入/输出方向验证 consumer |
| `semantic` | 改变既有值/操作的解释、默认或行为，但经方向性验证仍兼容；与结构形状是否改变无关 |
| `breaking` | 现有 producer 或 consumer 可能无法继续正确工作 |

分类按 `breaking > semantic > additive > none` 的最高风险唯一选择：

- 任一仍受支持的 producer/consumer 或基线下有效交互可能失败、被拒绝或被错误解释时为 `breaking`；
- 改变既有值/操作的解释、默认或行为，但经方向性验证仍兼容时为 `semantic`，结构
  是否改变不影响该判断；
- 只有不改变既有交互解释并通过方向性 consumer 验证的新能力才为 `additive`；
- `none` 不是默认值，必须给出可复核理由。

无法确认时至少按 `semantic` 评审；存在未知不兼容风险时按 `breaking`，不能直接假定 additive。

满足任一条件即进入契约评审：

- 数据或操作跨进程、跨仓库、跨语言或跨独立发布单元；
- 数据成为跨独立发布单元或跨版本 durable event、queue、audit、cache/replay 格式；
- producer 和 consumer 需要共同理解字段、行为、失败或安全语义；
- 公共 SDK、MCP tool、Runtime 投影或自动生成接口发生变化。

契约不只包括 DTO 形状，还包括：

- HTTP/RPC/SSE/WebSocket 的路径、方法、header、状态码、错误码和流式 framing；
- required、null/omitted、default、enum、格式、单位、金额、时区、分页和排序；
- 认证、租户、权限、scope、审批、幂等、trace 和审计上下文；
- 事件 topic/channel、key、envelope、顺序、重复、重试、重放、终态和保留；
- MCP tool 名称、输入输出、风险等级、权限和失败语义；
- SDK 公共签名、JSON Schema、Protobuf tag 和 Runtime 能力/版本投影。

## 3. 权威源路由

| 边界 | 权威源 | 约束 |
|---|---|---|
| 易界 HTTP API | `yijie-contracts/openapi/` | handler/client 必须映射或生成，不以实现反推契约 |
| 易界 RPC 与 wire event | `yijie-contracts/protobuf/` | tag 不复用，删除需 reserve |
| 易界异步 channel/operation | `yijie-contracts/asyncapi/` | payload 必须引用或声明唯一权威 schema |
| JSON/SSE/tool/shared payload | `yijie-contracts/jsonschema/` | 不复制后独立演进 |
| MCP tool 公共表面 | `yijie-contracts` 中对应 schema | scope、风险、审批和错误模型与形状同审 |
| Codex app-server | 固定的 `yijie-codex` Runtime canonical schema | `yijie-contracts` 保存受评审的兼容投影，Agent Host 消费固定投影 |
| 第三方平台 API/webhook | 当前官方规范 | Connectors 适配；易界归一化公共表面仍归 `yijie-contracts` |
| 服务私有数据库/缓存 | 所属服务 migration/data compatibility | 不因内部持久化自动进入 contracts；被独立发布单元读取或成为 durable wire/audit/replay 时另建契约 |
| 纯进程内领域模型 | 所属仓库 | 可以手写，与 wire DTO 通过显式 mapper 隔离 |
| 部署配置、probe、环境变量 | 服务仓与 `yijie-infra` | 按部署接口治理，不强行放入 API 契约仓 |

生成物、SDK、快照、fixture 和文档示例不是第二权威源。发现多个表示时，必须声明唯一权威源、投影关系并增加一致性测试。

## 4. 不可绕过的开发与合并流程

1. **分类**：记录 `contract-impact`、Owner、producer、全部已知/登记 consumers、输入/输出方向和安全边界；未知公开 consumers 标记为 `unknown-public`。
2. **设计**：先修改实际权威源，补齐所有受影响且适用的成功/失败/边界示例、错误、幂等、审计、兼容窗口和回滚；不适用项写 `N/A`。
3. **生成与校验**：对 `yijie-contracts` 治理的边界执行 generate、完整 diff、lint、test，并相对所有仍受支持或处于生产兼容窗口的基线逐一执行 breaking check；若尚无已发布基线，使用 `yijie-contracts/docs/supported-baselines.md` 登记的 fallback 完整 commit，禁止零基线放行；私有存储只走所属仓 migration/data compatibility。
4. **分级评审**：additive 在存在 consumer 时至少由一个代表性 consumer Owner 认可；semantic/breaking 由所有受影响 consumer Owner 确认，或逐仓记录获批例外；`unknown-public` 使用最保守兼容假设并由 SDK/代表性客户端 Owner 评审；全新且无 consumer 时由架构及适用时的安全 Owner 评审。
5. **契约先合并**：契约 PR 在计划版本、评审、检查与发布方案齐全时即可合并，随后形成不可变完整 commit；生产版本必须使用不可移动 tag。
6. **逐仓锁定与实现**：每个下游实现 PR 在自身合并前记录精确版本、完整 commit 和可用时的 digest/generator 版本，从生成物或同源 validator 接入，并补 producer/consumer conformance、未知值及失败路径测试。
7. **按方向激活**：provider-first 变更允许 provider 实现先合并/部署但不要求 consumer 立即使用；新 response/event 或 breaking 切换必须等相应 consumers 就绪后才发出/启用。
8. **清理**：所有受影响 consumers 完成迁移并有观测证据后，才能弃用、删除旧字段/版本或停止双轨。

契约 PR 稳定后允许并行编写下游 draft，缩短等待时间；并行不改变合并和启用门禁。
不得先合并 endpoint、事件、tool 或临时 DTO，再以“后续补 contract”收尾。

“契约 PR ready”与“跨仓交付完成”是两个状态：前者不可能预先拥有合并后的最终 commit，
只要求计划版本与完整检查/评审；后者才要求最终完整 commit/tag、全部下游 pin、
conformance 和 rollout 证据。

## 5. 兼容方向与发布顺序

“新增”不等于端到端兼容。closed schema、`additionalProperties: false`、封闭联合类型、穷举 enum 和严格解码器都可能拒绝新增内容。

| 变更 | 安全顺序 |
|---|---|
| 新 endpoint / operation | contract → provider 支持 → consumer 调用 |
| 新 optional request/input 字段 | contract → provider 接受且忽略/处理 → consumer 发送 |
| 新 response/output 字段 | contract → 验证旧 consumer 容忍或先升级 consumer → producer 返回 |
| 新 request/input enum 值 | contract → provider 接受 → consumer 发送 |
| 新 response/output enum 值或 event variant | contract → consumer 支持 unknown 或先升级 → producer 发出 |
| required、删除、重命名、收窄 | 若使基线下有效交互失效则为 breaking；否则仍按输入/输出方向分阶段 |
| durable event/audit/replay payload | 同时验证旧数据→新 reader 与新数据→回滚旧 reader；必要时版本字段、dual reader/writer 和 migration |
| auth/scope/error/idempotency 改变 | 按 `semantic` 或 `breaking` 评审，并同步安全、审计和回滚 |

任何形状或语义变化一旦使仍受支持基线下曾经有效的 request、response、event 或旧端
行为失效，就归类为 `breaking`。兼容的 semantic 澄清仍需分阶段发布，但不强制 major
或双轨。

自动结构检查绿色不代表业务语义兼容、实现符合契约或端到端兼容。默认值、null/omitted、错误映射、权限、单位、排序、事件量、重试和时序仍需人工评审与 consumer test。

## 6. PR 必须提供的证据

涉及契约的 PR 必须填写：

- `contract-impact` 分类及理由；
- 权威源类别与路径，以及该权威源的不可变 tag、完整 commit、schema/version 或 migration 引用；
- 仅对 `yijie-contracts` 治理的公共跨仓 wire 边界填写 contracts PR、计划/不可变 tag、全部适用 breaking 基线或 fallback、生成物和 consumer pin；
- 私有存储、部署接口、Runtime/第三方上游边界填写各自的 migration/data/runtime/deployment compatibility 证据；不适用的 contracts 字段填写 `N/A` 并说明理由；
- Owner、producer、全部已知/登记 consumers，以及按变更级别要求的逐 consumer 评审/例外；
- 适用于该权威源的兼容基线、自动检查结果和人工语义兼容结论；
- 适用的生成物、migration、consumer pin 和 producer/consumer/affected-party conformance；
- 合并顺序、部署顺序、兼容窗口、迁移、灰度、观测和回滚；
- 认证、租户、权限、审批、审计和敏感数据影响。

`contract-impact = none` 也必须说明不涉及哪些边界。契约 PR 合并前填写计划
tag/版本，合并后由跨仓交付记录补最终完整 commit/tag。只勾选 checkbox、只链接实现
PR 或只声称“测试通过”均不是充分证据。

## 7. 明确禁止

- code-first endpoint/event/tool 后补契约；
- 复制或手写与公共 wire schema 重复的影子 DTO；
- 直接编辑生成文件，或从实现反向修改生成物；
- 从 dirty/floating sibling 制作可发布产物，或只写不存在的 tag；
- 关闭 lint、跳过 breaking、降低 schema 严格度或伪造版本/hash 以通过门禁；
- 把数据库行、前端类型、prompt 描述或第三方原始 payload 当作易界公共权威契约；
- 在 consumers 未迁移时多仓硬切或删除旧版本。

## 8. 例外与紧急变更

- 不发布的 spike 可以使用临时类型，但必须隔离在实验路径，不得合并到可发布分支、默认启用或被其它仓库依赖。
- 暂无 generator 的语言只能使用显式 adapter、同源 schema conformance test 和有 Owner、期限、移除条件的例外记录。
- 线上事故优先回滚、禁用或恢复既有兼容行为。若安全事故确实无法等待常规流程，必须取得用户明确确认，记录 Owner、原因、影响、期限、consumer、回滚和补偿 PR；不得借紧急名义让未文档化的新跨边界形状长期上线。

例外必须记录在实现 PR 的“临时例外”字段，并链接一个带 Owner、到期日和补偿 PR 的
跟踪 Issue。例外到期即视为失败门禁，不能以 TODO 无限延期；自动到期检查尚未接通，
由 reviewer/Owner 负责追踪。

## 9. 完成定义

当 `contract-impact != none` 时，所有路径都必须有权威源不可变引用、Owner/受影响方
清单、按影响级别取得的 review 或获批例外、方向性兼容结论、实现/迁移符合性、发布
顺序和回滚，并按第 3 节权威源路由补齐：

- `yijie-contracts` 治理的公共跨仓 wire 边界：源契约、适用生成物、全部适用 breaking
  基线（尚无已发布版本时为已登记 fallback 完整 commit）、最终 tag + 完整 commit、
  下游 pin 及 producer/consumer conformance；
- 私有存储与部署接口：对应 migration/config 权威源、旧数据/新 reader 与回滚 reader
  或 deployment compatibility、受影响服务/环境验证及迁移回滚；
- Runtime 与第三方上游边界：固定的上游 tag/完整 commit/schema/API 版本、易界兼容
  投影或 adapter、双向/runtime/受影响方验证及回滚。

不适用的 contracts 字段必须填写 `N/A` 和理由，不能伪造 contracts PR/tag。`none`
只需保留分类理由。尚未发布的 tag、独立 CI 中被跳过的 sibling 检查、占位 generator、
未迁移 consumer 或未完成 migration 必须明确列为未完成，不能用仓内绿色测试替代。
