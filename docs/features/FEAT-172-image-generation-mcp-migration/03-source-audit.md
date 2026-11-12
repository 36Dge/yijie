# FEAT-172 现有生图链路与工具族源码审计

> 历史审计/修订 2 记录。2026-11-12 用户追加“选定专家不可用不再内置兜底”；涉及兜底、preflight、结果归并的建议已撤回，以 [修订 3](04-implementation-design.md) 为准。源码证据保留，不作为当前实施或验收结论。

审计日期：2026-11-12（Asia/Shanghai）。本记录是源码与文档审计，不是运行验收。未启动/停止客户端、未重建 Runtime、未读取真实凭据、未调用生成模型。

同日深度复审补充了10个源码入口，完整67文件摘要见[review-source-audit.json](references/review-source-audit.json)。事实保持；下列“迁移影响”已按复审版调整，初稿的新增媒体API/数据库/回执协议和补丁重基不再是实施要求。新增原生复用证据见[06](06-design-reaudit.md)。

## 1. 范围、基线与证据性质

覆盖元仓、Runtime、Contracts、Agent Host、Connectors、Desktop、Skills、API、Infra 九仓。完整分支、HEAD、远端、工作区状态及 57 个相关源码文件的 SHA-256 见 [source-audit.json](references/source-audit.json)。Desktop 原有 69 条文件状态记录，包含正在进行的图片预览改动；本任务不修改这些文件。

| 仓库 | 审计 HEAD | 本轮职责 |
|---|---|---|
| yijie | b6565309bbf844b62c3cc7e0ecf09062f7353d1c | 需求、ADR、约束与方案落盘 |
| yijie-codex | fe3f5b1c768f2a1464314e2a350d419a3e63d9c6 | 工具装配、原生图像扩展、MCP 调度、补丁链 |
| yijie-contracts | d658a2bd5dd6ebd5ae5c79a547489eca205d6ede | Runtime 投影、专家路由、Artifact 与工具契约 |
| yijie-agent-host | c6b8b1a790b62b34a392f0f32a9485100a9eca2e | 生图执行、凭据、路由、MCP 配置、产物暂存 |
| yijie-connectors | 37552bec1c31bca95457af7145e0dad206df1f8a | 专家 MCP、调用准入、供应商执行边界 |
| yijie-desktop | 275b72b17dcb1a63cf78042915968d518e867938 | 启动、绑定、附件、持久化与预览；以含既有改动的工作树审计 |
| yijie-skills | 3698a970cf601afbb7fe1691e86d413df1481c09 | LinkFox 专家说明及失败流程 |
| yijie-api | 86444f305c71da7104a9880206ac53d4eea9908c | 平台权限、生成操作状态与凭据供给的既有能力核查 |
| yijie-infra | d8faafdfbd375f8b26088dd07106f9ffb74f67e0 | 本地部署、服务端密钥与云部署现状 |

Facts 来自下列函数、配置及本轮只读命令；Recommendations 属于 04 的拟实施方案。各仓 AGENTS.md 的规范继续适用，但其中早期 Baseline/“尚未实现”的现状段落不能覆盖后续源码。FEAT-168 的旧政策与本轮用户指令冲突时，以本轮指令为准，不回写旧验收结果。

## 2. 当前从启动到交付的实际链路

| 编号 | 阶段与现状 | 可复核入口 | 迁移影响 |
|---|---|---|---|
| A01 | 日常启动器读取 `.local/development/host-images.json`，转为 FEAT-168 环境选择；Shell 再选择 Runtime candidate、配置与构建检查 | [development-client.py](../../../../yijie-desktop/scripts/development-client.py) `daily_images_setting/environment`；[run-local-demo-fast.sh](../../../../yijie-desktop/scripts/run-local-demo-fast.sh) `host_images` 分支 | 新内置工具应随应用启用，移除面向 FEAT-168 的生图 opt-in/暂停选择及旧候选入口 |
| A02 | Host 仅在 `local + demo_fast + artifactV3 + multimodalV2` 接受 `YIJIE_FEAT168_HOST_IMAGES`；旧 FEAT-128 开关报退役错误 | [app.go](../../../../yijie-agent-host/internal/app/app.go) 220–230 行 | 新 MCP readiness 与媒体功能配置独立于旧图片开关、文档开关及市场选择 |
| A03 | `desktop-host` 构建 `NewSeedreamClient(ArkCredential(HostHome))`，注入 Session，并绑定 `SetHostImageHandler` | [main.go](../../../../yijie-agent-host/cmd/desktop-host/main.go) 163–183 行 | 复用现有客户端与Session，入口改接MCP；不绑定旧图片反向业务handler |
| A04 | start/resume 按 `ImageRoute(ctx)==builtin` 设置 `yijie_host_images`，给模型注入优先调用原生 `generate_image` 的提示 | [session_protocol.go](../../../../yijie-agent-host/internal/codex/session_protocol.go) 600、693 行附近；[host_image.go](../../../../yijie-agent-host/internal/codex/host_image.go) | 改为普通 MCP 装配；清除“跳过工具搜索、直接调用原生图片”的旧提示 |
| A05 | 0019 补丁把 Host backend 注入原生 image-generation 扩展；暴露平面函数 `generate_image(prompt,use_current_reference)`，发出 `ImageGenerationItem` 开始/结束 | [0019 补丁](../../../../yijie-codex/.yijie/patches/chat-models/0019-host-image-generation.patch) 96、194、370、392、456 行附近 | 属于 Runtime 原生扩展，不是 MCP；新调用应产生真实 `McpToolCall`，不伪造旧 imageGeneration item |
| A06 | Runtime 经现有 stdio JSON-RPC 发出 `item/imageGeneration/generate`；Host 校验五个字段及当前候选，返回 success boolean | [host_image.go](../../../../yijie-agent-host/internal/codex/host_image.go) `handleHostImage`；[契约投影](../../../../yijie-contracts/compatibility/runtime-host-images/source.lock.json) | 用当前原生配置关闭该入口，Host拒绝旧生产调用；不为删除方法重建固定Runtime/schema |
| A07 | 附件在 `beginImageTurn` 从本轮授权输入保存，后绑定真实 turn；提前到达的通知也走绑定；中断和终态释放引用 | [multimodal.go](../../../../yijie-agent-host/internal/session/multimodal.go) 238–285 行；[provider_image.go](../../../../yijie-agent-host/internal/session/provider_image.go) | 复用附件与 turn 权威，不允许模型改成任意路径、URL 或 base64 参数 |
| A08 | 每个 imageTurn 只有一个 `called` 布尔值；只允许 `route=builtin`；并发请求在锁内互斥，调用与发布分别校验取消状态 | [provider_image.go](../../../../yijie-agent-host/internal/session/provider_image.go) 166–246 行 | 不能用原布尔量直接承载“专家失败→内置兜底”；需要一个逻辑请求下的两个串行尝试状态 |
| A09 | 当前 prompt 最多 1500 Unicode 字符；单参考图 PNG/JPEG，解码最多 10,000,000 bytes；输出最多 20 MiB | [client.go](../../../../yijie-agent-host/internal/imagegen/client.go) 17–25 行；`validateReferenceDataURL/inspectImage` | 本期保持既有明确范围，迁移不顺带扩成多图、组图或任意编辑工具 |
| A10 | Seedream HTTP POST 固定模型 `doubao-seedream-5-0-pro-260628`、`1.5K`、`watermark=false`；省略 stream；结果只接受一张图片，校验允许的结果域并无凭据 GET 下载 | [seedream.go](../../../../yijie-agent-host/internal/imagegen/seedream.go) `seedreamPayload/Generate/seedreamResultURL` | 原客户端保留在既有Host模型适配边界；GET与生成POST的重试语义分开，不新增跨仓SDK包 |
| A11 | 缺少 Keychain 项时，`ArkCredential` 调起 osascript 掩码框，要求用户配置方舟 Key | [credential_darwin.go](../../../../yijie-agent-host/internal/imagegen/credential_darwin.go) 60–125 行 | 与本轮开箱可用要求直接冲突；不能仅改工具注册便宣称完成 |
| A12 | 图片 bytes 进入 Host 加密 spool；事件提供 artifact_id、MIME、大小、SHA-256、Host content href；Runtime 仅获得短结果 | [provider_image.go](../../../../yijie-agent-host/internal/session/provider_image.go) 238–262 行；[store.go](../../../../yijie-agent-host/internal/artifact/store.go) | 复用已有媒体交付通道；不把大图写进 MCP 文本或模型上下文 |
| A13 | Host 当前把 native `imageGeneration` 当作已有 Artifact 的伴随项，避免重复展示 | [native_conversation.go](../../../../yijie-agent-host/internal/session/native_conversation.go) `managedImageCompanion` | 清除只为旧图片入口存在的抑制逻辑；MCP 工具活动与图片产物保持不同对象，不靠工具名字推断图片 |
| A14 | Native 下载、校验、数据库提交，再 ACK；可重试的是内容传输/ACK，不是重新调用模型 | [artifact.rs](../../../../yijie-desktop/src-tauri/src/chat/artifact.rs) `transfer_completed/download_with_retry/acknowledge_committed` | 工具“供应商完成”不等于“图片已交付”；输出须区分 staged 与 committed |
| A15 | 当前图片 UI 经 Native preview lease 打开、释放、保存；既有工作树正在完善 loading、缩放等交互 | [useChatArtifactImage.ts](../../../../yijie-desktop/src/composables/useChatArtifactImage.ts)；[ChatArtifactImage.vue](../../../../yijie-desktop/src/components/chat/ChatArtifactImage.vue)；[artifact_native.rs](../../../../yijie-desktop/src-tauri/src/chat/artifact_native.rs) | 保留已存在的图片组件及授权链，不在入口迁移中重做查看器或覆盖未提交 UI 工作 |

现有测试源码包括 `TestHostImageNativeRequest`、`TestSeedreamSingleImage`、`TestSeedreamRejectedRequestIsNotResubmitted`、`TestProviderImageAllowsOnlyOneConcurrentPaidCallAndInterruptCancelsIt`。这些只是后续改测的入口，本轮没有运行它们，也没有复用 FEAT-168 的 PASS 作为 FEAT-172 证据。

## 3. 专家优先与兜底缺口

| 编号 | 核查结论 | 证据及影响 |
|---|---|---|
| E01 | 点名与界面选择形成版本化专家绑定；Host 用具体版本及 role digest 核验，非按工具名包含 image 猜测 | [explicit-expert.ts](../../../../yijie-desktop/src/domain/explicit-expert.ts)；[experts.go](../../../../yijie-agent-host/internal/session/experts.go) `contextForExpert`；[expert_instructions.go](../../../../yijie-agent-host/internal/codex/expert_instructions.go) |
| E02 | 当前仅有冻结的 LinkFox 生图路由：服务 linkfox、代理 proxy_call、业务方法 aigc/imageGenAsync | [expert-routes.json](../../../../yijie-contracts/compatibility/runtime-host-images/expert-routes.json)；能力事实应迁出 Runtime 图片兼容目录，成为独立媒体能力源 |
| E03 | 旧策略是严格互斥且失败停止；专家绑定时原生内置入口关闭 | [host_image.go](../../../../yijie-agent-host/internal/codex/host_image.go) 15–18 行；[market_approvals.go](../../../../yijie-agent-host/internal/codex/market_approvals.go) 122–139 行；本轮用户已改变该产品政策 |
| E04 | 专家资源、服务资格或 PrepareMarket 不可用时可能在 turn/start 前直接拒绝提交 | [market_submit.go](../../../../yijie-agent-host/internal/session/market_submit.go) 166–175 行；不能只设计工具执行后的 fallback，必须覆盖输入提交前的降级 |
| E05 | worker 的 consumed 是执行许可已消费，不是远端成功/失败；普通MCP错误不能独立证明业务失败 | [broker.rs](../../../../yijie-connectors/worker/src/broker.rs) `consume_execution`；[gateway.rs](../../../../yijie-connectors/worker/src/gateway.rs) 218–285 行。复审确认原生MCP item已经带result/error；优先解释完整原生结果，不必新增Broker回执协议 |
| E06 | generic adapter 只回传有界惰性文本/JSON，不下载图片；isError=false 也未必是生图成功，代理内层仍可能是业务失败/处理中 | [generic.rs](../../../../yijie-connectors/worker/src/generic.rs) `execute/safe_result`；不能全局把 MCP error、超时或 URL 缺失当作可兜底 |
| E07 | LinkFox 专家异步流程区分 taskId、PROCESSING、SUCCESS、FAILED；本轮本地素材上传未实现；旧说明规定失败停止且每轮至多一次查询 | [专家工具流程](../../../../yijie-skills/plugins/yijie-desktop-skills/experts/linkfox-expert-aigc-imagegen-mannequin-to-model/skills/mannequin-to-model/references/tool-workflow.md)；本地参考图无法按专家要求传入时，可在未提交前直接使用内置；不得为“先试专家”擅自上传 |

## 4. yijie-codex 工具族审计

统一装配入口是 [spec_plan.rs](../../../../yijie-codex/codex-rs/core/src/tools/spec_plan.rs) 的 `add_tool_sources`，最终得到模型工具声明及本地 `ToolRegistry`。原生 Handler、Extension、MCP、Dynamic 均有执行器；hosted spec 单独追加到模型请求。Function/Namespace 是声明形状，Direct/Deferred 是暴露策略，均不应被混称为工具来源。

| 编号 | 工具族/机制 | 源码事实 | FEAT-172 决定 |
|---|---|---|---|
| T01 | 原生 image-generation extension | `ThreadLifecycleContributor`、`ConfigContributor` 保存配置，`ToolContributor` 提供 executor；上游 backend 与易界 0019 注入的 backend 不同 | 复用当前配置关闭专用backend；保持固定上游子树、补丁链及canonical schema，不增加核心变更 |
| T02 | MCP | `McpHandler` 从发现的 ToolInfo 生成 Function/Namespace spec；原生 `handle_mcp_tool_call` 承接策略、审批、生命周期，connection manager 调用 server | 直接复用；不增加自研工具调用循环、审批器或 MCP client |
| T03 | MCP 发现 | [mcp_tool_exposure.rs](../../../../yijie-codex/codex-rs/core/src/mcp_tool_exposure.rs) 34–44 行：search 关闭直接暴露，开启则普通 MCP 工具全部 deferred | 纠正前轮泛化建议：当前没有现成的“仅把媒体工具设成 Direct”的逐工具配置；本期按实际模型 profile 复用 tool_search，不补专用常驻工具 patch |
| T04 | MCP 请求身份 | [mcp_tool_call.rs](../../../../yijie-codex/codex-rs/core/src/mcp_tool_call.rs) 注入 threadId 和 x-codex-turn-metadata；call_id 字段仅在 Codex Apps 分支注入 | 通用 MCP 不假定能取得原生 call_id；本期用受信 thread/turn 与 Host 已接受的 turn operation 绑定生成操作，JSON-RPC request ID 仅作瞬时 trace |
| T05 | Dynamic | 注册入口仍标记 `thread/start.dynamicTools` experimental；调用回到 item/tool/call，产出 DynamicToolCallItem | 不采用；既有旧 FEAT-128 adapter 和 DynamicToolCall 类型复用要退役，不以改名隐藏旧调用路径 |
| T06 | Hosted | `hosted_model_tool_specs` 根据主聊 provider 能力生成服务端专用 spec，本地没有对应 provider REST executor | 不采用；Seedream 是外部生成模型，不因此成为主聊 provider 的 hosted tool |
| T07 | MCP Tasks | [rmcp_client.rs](../../../../yijie-codex/codex-rs/rmcp-client/src/rmcp_client.rs) 625–647 行只接受普通 CallToolResult | 本期不启用Tasks/生成操作服务；视频另案，图片交付状态复用get_artifact_status |
| T08 | 现成应用内置 MCP | Host 注入 `yijie_artifacts`；Rust 官方 rmcp loopback gateway 仅薄转发 Host 私有接口；以关闭 stdin 正常停止 | 复用进程拥有权、受管 binary 校验及 transport 组织；媒体使用独立 server identity、路径和 token，不冒充市场插件 |
| T09 | 当前补丁依赖 | 0020/0021 的 manifest 依赖 0019；0022→0023→0024 继续串接；0024 补丁上下文引用 yijie_host_images | 既有配置已能停用，故本期不删除0019、不重基后继补丁。验证产品旧入口不可达即可，不把源码清理强加为迁移前置 |

## 5. 开箱可用的实际差距

现有 `yijie-connectors/internal/app/app.go` 只有 health/status 骨架；不能当成已存在的媒体网关。`yijie-api` 有身份、租户、权限与 Tasks 基础，但 [permission.go](../../../../yijie-api/internal/modules/authorization/domain/permission.go) 当前七个 capability 不包括媒体生成，也没有现成“平台媒体额度”服务。Infra 未实现公网生产密钥/部署体系。复审结论：这些是未来公开交付的设计输入，不能据此反推“本次本机入口迁移必须新增整套平台服务”。

本期由易界运营/开发方在当前非公开部署中预置其拥有的凭据，复用Host作用域与只读Keychain读取并禁止交互；最终用户不提供自己的Key。缺失配置不能以弹窗补齐冒充开箱可用。公开分发时仍不得把共享Key放入App，服务端代理届时另议；本期不新建认证、数据库或额度平台，也不绕过专家审批拒绝。

## 6. 外部依据与审计限制

- 2026-11-12 核对 [方舟图片 API](https://docs.volcengine.com/docs/ark/image-generation-api?lang=zh)：存在直接生成端点、API Key 鉴权和结果链接；本期保持当前代码已采用的模型与单图参数，不把官方更宽输入能力当作易界已支持。
- 核对 [MCP tools 规范](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)：采用 tools/list、tools/call 和普通 CallToolResult；具体 wire 以当前固定 rmcp/Runtime 实现为准，不随最新网站版本自动升级。
- 核对 [MCP Tasks 扩展](https://modelcontextprotocol.io/extensions/tasks/overview)：它需要额外协商与客户端处理，本期不启用。
- Seedance 仅作架构背景。此前官方检索确认创建任务为异步；本轮打开具体页面超时，未据此冻结视频模型、参数或实现，避免把未来能力混入本期验收。

源码审计不能证明模型是否正确选工具、实际付费接口可用、专家账户资格或图片质量。这些全部留在 02 的未来验证项，当前状态为 NOT RUN。
