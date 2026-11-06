# FEAT-168 需求治理复审

2026-11-07 · Codex 复核 · 范围为元仓需求包，产品与技术决定负责人为段成威。

**复审时点结论：需求包可提交 D0 确认。** 后续段成威于 2026-11-07 确认整包需求，并要求先不执行开发。[D0 确认记录](references/d0-confirmation.json) 用户已确定默认生图模型与参数、移除图片 API 流式约束、专家工具在显式选择期间跨轮优先，LinkFox 专家保留。首稿把专家选择和外部调用准入、Runtime 现有能力和所需补丁、临时图片和历史原件分别写得过于接近。已在主需求、工程设计与验收计划中区分这些边界。8 项功能验收尚未运行。

## 复审发现与处置

| 优先级 | 原稿的问题 | 修订结果与验收依据 |
|---|---|---|
| P1 | 仅靠主模型选择工具，普通会话仍可能通过已启用的 LinkFox 通用代理创建图片。 | 两条创建路径在真正提交前核验同一次用户操作、已冻结的专家与本轮授权。普通会话中“仅启用连接器”的创建请求须在出站前被拒绝，其他获准查询照常办理。AC-001、002、004。 |
| P1 | fork 的原生实现会在选择 backend 前读取路径或跨轮图片，并可能把生成结果的 base64 和保存路径带回模型。原稿低估了切换供应商的范围。 | 复用同一原生执行器、开始/结束事件和取消；收窄易界 profile 的可见参数和解析入口。参考图取自当前受信操作，易界结果只交短回执及 Artifact。分别检验两种主聊模型、直接与嵌套调用及历史恢复。AC-003、004、006。 |
| P1 | 旧 `item/tool/call` 仅接收实验 dynamic tool，日常 profile 关闭该开关；原生图像 backend 没有可直接配置的 Host RPC。 | 先审定能否复用现有 stdio 反向请求的**语义**。若固定版本不可承载，只提同一 transport 内最小且可协商的候选接口，独立审批前不打 patch。AC-004、008。 |
| P1 | 原计划把绑定原有日常 Homes 的 `pnpm client:dev` 与“隔离环境”并列，会使验收误触真实对话和凭据。 | 产品正常入口与隔离资格分开。D4 候选须有经核实的独立 Native/Host/Runtime Homes、同源启动链、相同模型/权限/专家/媒体配置。任何一项未证明即保留未验证状态。AC-001 至 008。 |
| P1 | Host 暂存或方舟返回临时 URL 不能证明图片已在 Native 提交。旧实现只有进程内的本轮调用标记，也不能支持重开后再次派单。 | 按“供应商受理 → 取回并校验 → Native 提交 → ACK”区分状态。预览重读、补 ACK 和重连都不能重新生图。提交结果不明时保留原操作，不推断费用已撤销。AC-005、006、008。 |
| P2 | 数据只标为 Confidential，历史保护范围、谁有权配置密钥以及外调审批不清。 | 凭据按 Restricted 管理；联调用公开或合成人物图。配置弹窗与付费批准分开。按 ADR-0023 保护当前受支持格式中已有的图片，保留过期信息，不恢复退役的 reader，不实施迁移。AC-002、005、007。 |

源码证据与符号集中在[工程记录](01-delivery-log.md)。其中包含原生工具注册与结果的全部出口、Host 的图片/专家绑定以及 worker 的真实调用准入。各行的验证方法及通过条件见[验收矩阵](02-verification.md)。

## D0 决策与授权

| 事项 | 当前决定 |
|---|---|
| 已确认的规则 | 没有选择专家、或专家确实未配置生图能力时走 Seedream。显式选择的专家提供生图工具时，在选中期间跨轮优先，LinkFox 继续走自己的配置；已选路径失败时停止。内置默认 `1.5K`、`watermark=false`，不传 `stream`。旧 MiniMax 生图按计划退役，保留 MiniMax 文本对话。 |
| 纯文本点名后的下一轮 | Owner 已于本轮明确：文字点名与界面选择都是显式声明；选中期间专家提供的同领域工具始终优先，无轮数上限。两种入口共用会话绑定并显示胶囊，直至移除或切换，每轮冻结自己的选择和授权。本包验证生图，其他领域不随此需求改代码。 |
| 隔离 Demo 与正式启用 | 沿用 ADR-0017/0018 的 `demo_fast / local` 和免登录直达，仅覆盖独立数据目录与公开/合成样本。正式日常是产品目标，写入用户日常环境需另行批准；涉及重要持久数据迁移、真实 PII 或生产责任时重新评定 Profile。FEAT-164 的 ADR-0022 仅适用于该需求。 |
| 技术决策 | 建议 Host 持有独立方舟凭据并完成图片 API 请求，fork 执行原生工具调度。另将凭据引入 Runtime 会改变现有持有边界，重启旧实验 dynamic tool 则违背日常 stable 资格。若需新增跨仓协议、权限边界或 fork 核心 patch，先由技术负责人审定契约及适用 ADR，保留独立的明确授权。 |
| 成本和秘密 | Kimi/MiniMax 主聊、Seedream、LinkFox 的业务创建/可能计费查询分别记账；本次允许的账户操作及付费调用均为零。后续真实联调须先有具体 provider、场景和上限。弹窗输入仅在真正配置独立 Ark 凭据时进行，取消不出站；记录配置状态，不记录内容。 |

普通等待时沿用活动提示，成功后显示可读原图；失败说明可恢复操作。沿现有图片卡片、键盘焦点和主题回归。生产容量、公开部署、压测和额外画布均不进入这个本地 Demo。本包的时间盒只用于后续诊断，不能替代任何 Must AC。[质量门禁](../../dev/codex-feature-delivery/QUALITY_GATES.md) · [本地身份边界](../../adr/ADR-0018-local-demo-direct-entry.md) · [日常格式范围](../../adr/ADR-0023-native-execution-trace-v6.md) · [数据等级](../../security/data-classification.md)

## Contract First 与切换条件

最高 `contract-impact = breaking`。旧本地 profile 中发往 `image-01` 的有效操作会被退役；新增的专家出站限制也会改变单纯启用 LinkFox 时可获准的操作。元仓登记影响，以下各边界保留各自的权威源。

| 权威源与责任方 | Producer → Consumer，实施时需证明的条件 |
|---|---|
| [固定 fork 的图像扩展](../../../../yijie-codex/codex-rs/ext/image-generation/src/extension.rs) 和 [候选锁](../../../../yijie-contracts/compatibility/runtime-kimi-k31-pro/source.lock.json)，Runtime / Contracts | fork 先产出候选，Contracts 按 canonical schema 固定投影；核对 Runtime→Host 请求与 Host→Runtime 结果两侧兼容。未协商能力的任一端停止新生图，普通聊天可继续。不可借 `image-01` 或放宽全局 experimental 设置回退。 |
| [专家绑定](../../../../yijie-contracts/compatibility/experts-v2/transport.json) 和 [Broker 协议](../../../../yijie-contracts/compatibility/market-broker-control/wire.schema.json)，Contracts / Desktop / Host / Connectors | Native 冻结 revision 和旧版/当前专家的有效资源；Host 核验实际 turn；worker 对已发现方法消费原有审批。若现有消息不足以证明该绑定，先改权威源，再配对消费者，最后放行创建。仅凭模型参数或外层 `proxy_call` 名称不授权。Skills 用既有专家版本验证，不将全局技能发现改为仅显式。 |
| [方舟图片生成 API](https://console.volcengine.com/ark/region:cn-beijing/docs/image-generation-api)，Host | 校验受信操作、参考图和出站字段；单图结果须有可用 URL，取得合法图像后才交付。模型鉴权不随取图或跳转转发。账户是否开通该型号只能由后续授权实调证明。 |
| [Host 媒体](../../../../yijie-agent-host/internal/session/artifact_media.go)、[Native 提交与 ACK](../../../../yijie-desktop/src-tauri/src/chat/artifact.rs)，Contracts / Host / Desktop | 既有图片 Artifact 伴随流负责交付，主流 Native6/SSE13/IPC6 保留原语义。先核验新旧 reader、过期、ACK 和重开，再让 writer 产生可用图片。若只能通过改变受支持的存储格式交付，则暂停并先评估迁移范围。 |

配对次序为权威源/候选 → 支持新能力但未发新请求的双方 → 已核准隔离环境内验证双路由和历史 → 单独批准后切换目标入口。暂停或撤回内置生图时保留兼容 reader 和原 LinkFox 权责。日常旧库重置、旧二进制覆盖和自动回退到旧模型均未获准。方向兼容检查与回滚需要实际 consumer 证据；旧功能整包通过不能替本需求签收。[跨仓规范](../../dev/contract-first.md) · [受支持基线](../../../../yijie-contracts/docs/supported-baselines.md)

## 本轮证据与门禁

[文档审计证据](references/requirements-audit.json)记录复审前的四份文件摘要、核对的仓库版本、实际命令、退出码和检查范围。复审当时的 D0 显式检查因 `product_ux.status=pending` 返回退出码 1，作为确认前历史保留；严格包校验、声明审计和元仓治理测试检验文档及规则，不能代替 Owner 确认。

整包 D0 确认、Runtime 技术批准、隔离真实账户联调、D4 和日常启用属于不同决定。本轮无 App/Runtime 构建或启动、模型/业务工具调用、凭据读取或配置。禁止的强杀、权限破坏、可执行文件篡改、攻击性样本均未执行；异常制造情形无验证结论。后续只能用正常取消、自然错误或正常协议回放覆盖相应用户结果。
