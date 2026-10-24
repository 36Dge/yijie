# Kimi K3.1 Pro 替换审计与实施方案

> 2026-10-24 二次审计已形成 [FEAT-164](../features/FEAT-164-kimi-k31-pro-migration/00-feature-brief.md)。本文保留为首次调查记录；其中关于治理 Profile、普通未发送取消、unknown 恢复、压缩/子代理/Guardian、worker 接管和兼容回退的初步判断，以 [二次审计修正](../features/FEAT-164-kimi-k31-pro-migration/11-second-audit.md)及该需求包设计为准。本次落盘不授权产品实施。

日期：2026-10-24（Asia/Shanghai）。Owner：段成威。状态：**审计完成，实施方案待审阅；尚未实施模型替换，尚未进行新模型真实验收。**

本次文档的 contract-impact=none：只记录调查和方案，不改变产品。拟实施变更的整体 contract-impact=breaking：新旧模型身份跨 Contracts、Host、Runtime、Desktop、持久化和操作重放边界，现有封闭枚举、SQL CHECK 和精确配置校验不能直接接受替换。

**结论**

可以继续使用现有 Codex Runtime 原生 Responses 执行链，将有效 Kimi 模型替换为 `kimi-k3.1-pro`，不需要新增协议转换服务或另建 Agent 循环。但这不是全仓字符串替换：至少要同时处理模型契约、Host 受管配置升级、Runtime 搜索来源补丁、Desktop 严格身份校验、旧会话及计划的迁移。

推荐最终状态：

| 项目 | 目标值/行为 |
|---|---|
| 上游请求 model | `kimi-k3.1-pro`，不选择 highspeed 变体 |
| UI 名称 | `Kimi K3.1 Pro` |
| 新执行 profile | `kimi-k3-1-pro-max-v1`（内部标识建议；上游 model 必须保留点号） |
| provider / endpoint | `kimi` / `POST https://api.moonshot.cn/v1/responses` |
| reasoning / context | 保持现有 `max`；上下文 `1048576` |
| 当前可选模型 | Kimi K3.1 Pro、原 MiniMax M3；旧 Kimi K3 从可选目录及新执行路径移除 |
| 旧标识 | 仅用于历史事实、已完成回执和已知配置迁移；不再用于新的推理请求 |
| 密钥、权限、工具执行 | 复用现有边界；更换模型不扩大权限、不重新保存另一份 Kimi Key |

内部 profile 使用连字符，是因为现有多语言生成器按 `_`/`-` 转换标识符，点号会进入 Go/Rust 名称。见 [generate-chat-models.mjs](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/scripts/generate-chat-models.mjs:12)。这不会改变用户指定的官方模型 ID。

**审计范围与基线**

已按 repos.yaml 核对元仓和 11 个兄弟仓的分支、完整 HEAD、远端及工作树。远端均为各自 `36Dge/yijie-*` 仓库。下表的修改项数来自本次审计开始时 `git status --porcelain=v1`，包含已有未跟踪项，不代表本次改动数量。

| 仓库 | HEAD | 已有修改项 | 审计结论 |
|---|---|---:|---|
| yijie | `91b2b76e7afc7cb5373a381ce352f7d1eee4a134` | 5 | 治理、FEAT-156/162/163、运行与验收记录 |
| yijie-contracts | `bedf4159b0fa22e24efe6c295f8b0d4845df56b7` | 61 | 模型权威定义、相关 schema/SDK/锁，必须修改 |
| yijie-agent-host | `283dcbd7d79ca7bd7a56dba0cb915024fff8eb72` | 54 | 模型选择、受管配置、生命周期、历史、标题/草案，必须修改 |
| yijie-codex | `9154f27d0cdb526a5f5ba0913fe3e2448014b4a1` | 0 | 旧模型专属搜索来源条件，必须修订补丁和候选构建 |
| yijie-desktop | `6080a568332dbf18ff119501607bc7e7afa92f94` | 100 | UI/Native 验证、SQLCipher、计划授权、构建来源，必须修改 |
| yijie-connectors | `251a0e8854b646a2565a01317a95b037579d9b8e` | 37 | Kimi Search/Fetch 与共享凭据回归；没有主模型 ID 替换点 |
| yijie-skills | `595c927ae101d3d31c234f60565041eee0864680` | 1 | 搜到的旧名称属于历史 provenance；专家执行消费 Host 当前 profile |
| yijie-api | `041f40c69919e81ec72ccee4ea6dbb3ea012142d` | 0 | 未发现本次 Kimi 直接调用/默认模型配置点 |
| yijie-infra | `66b481552eb76d46b00875ac27794ed8e1eb504a` | 0 | 受控 workflow-local 不启用模型节点 |
| yijie-coze | `7bdcd0474e904cd3e8f8f68c903c0b8985baf52f` | 0 | 上游有独立模型设施；当前易界受控工作流没有启用 K3 主调用 |
| yijie-admin-web | `d009cafccb112c098114c075d60f67ee5e0296d8` | 0 | 未发现该模型调用链参与点 |
| yijie-knowledge | `e9091d2b673ba779ecb39271ce9148e3a41fc256` | 0 | 当前仍为知识服务骨架，没有已接通的 Kimi embedding/RAG 调用 |

元仓、Contracts、Host、Runtime、Desktop 当前分支均为 `chore/retirement-baseline-20260905`；API 为 `feat/feat-126-foundation-closure`，Infra 为 `feat/feat-126-s10e`，Coze 为 `main`，其余为 `develop`。

审计以**当前工作树**为准，尤其包含 FEAT-162 网页工具和 FEAT-163 过程展示的未提交修改。不能从旧 HEAD 重建后覆盖这些代码，不能把旧功能的验收结果当作本次新模型资格。未读取用户数据库正文、API Key 或私人会话内容。

**官方接口核对**

- 新模型已被 Responses API 列为支持的模型；接口、SSE、function/custom/namespace/web_search 工具模式可以继续使用。Responses 的 `tool_choice` 当前仅列出 `auto`；多轮及工具回传需要保留上轮 output 和对应 call_id。响应的 store/background 固定为 false，previous_response_id/conversation 固定为 null，不能改为依赖服务端保存会话。[Responses API](https://platform.kimi.com/docs/api/responses)
- 官方针对 Codex 的配置明确指定 `kimi-k3.1-pro`、原 Moonshot `/v1` 地址、Responses 和 `1048576` 上下文，并说明无须协议转换；`search_context_size` 不受支持。该页面是外部兼容依据，不是要求改动用户全局 `~/.codex/config.toml`；易界应继续通过 Host 自己的受管 Home 配置。[Kimi 的 Codex 集成](https://platform.kimi.com/docs/guide/codex-kimi)
- 模型参数页说明 K3.1 Pro 与 K3 的参数约束一致；推理档位为 low/high/max。该页主要描述 Chat Completions，不能把其顶层 `reasoning_effort` 或更宽的 tool_choice 枚举直接搬进 Responses 请求。易界现有 Responses `reasoning` 由 Runtime 生成，实施时对真实请求核对。[模型参数参考](https://platform.kimi.com/docs/api/models-overview)
- Responses 输出预算的文档默认值为 131072、可设最大值为 1048576。这不等于易界已设置该预算，也不等于本任务获准使用这么多 Token；现有 Runtime 请求结构没有 max_output_tokens，之前 FEAT-163 的 8192 是诊断计量器覆盖。保留实际请求差异，不能把换模型和增预算混为一个改动。[Responses API](https://platform.kimi.com/docs/api/responses)
- 新模型快速开始页注明账户解锁条件，并提示联网搜索仍在更新、不建议用于生产；Responses 和 Codex 集成页又明确描述可用的原生 web_search。应分别记录各接口能力和生产限制，通过本任务的真实验证判断可用性，不把页面文案差异解释为已证明不兼容，也不据此直接删掉现有工具。[K3.1 Pro 快速开始](https://platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart)

用户给出的 [API 概述](https://platform.kimi.com/docs/api/overview) 经网页工具获取超时后，已通过公开 HTTPS 只读获取到 HTTP 200 内容，核实协议基址；没有访问账户 API。文档核对只证明平台公开支持，不证明当前账户权限、余额、限速或新模型在本项目中的效果。

**现有执行链**

```text
Contracts 模型权威定义
  ├─ 生成 Go / Rust / TypeScript / JSON Schema
  ├─ 派生 market-selection / experts / scheduled families
  └─ Host 模型目录 + Desktop 校验

Desktop 模型选择、聊天/专家/计划意图
  → Tauri Native：profile/revision/权限/本地操作快照
  → Agent Host /v1/model-chat/*：校验、会话状态、幂等回执
  → codex.WithModelProfile
  → Runtime thread/start 或 thread/resume → turn/start
  → POST api.moonshot.cn/v1/responses
  → Runtime SSE / 原生工具执行 / 工具结果回传 / 后续 Responses
  → Host 原生事件投影 → Desktop 单一显示缓冲和 SQLCipher 历史

并行的网页工具链：
选中的 kimi_web_search/fetch → Host Broker 审批 → Connectors worker
  → /v1/tools/search 或 /v1/tools/fetch
```

主模型链入口见 [Host 路由](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/app/chat_models.go:46)、[thread/start](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/session_protocol.go:536)、[thread/resume](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/session_protocol.go:646)。正常模型切换复用 `thread/read → unsubscribe → resume`，保持 thread ID，并等待 Runtime 回执确认。[切换实现](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/chat_models.go:163)

**关键发现与必须处理的影响**

| 编号 | 已确认事实 | 直接替换的后果 / 实施要求 |
|---|---|---|
| A1 | [权威 schema](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/jsonschema/chat/model-selection-v1.schema.json:5) 同时定义旧 profile、model、label、effort、context；catalog 恰好两个活动模型 | 从源修改，不能只改 Host 字符串或生成 TS；active 定义与 legacy 读取要分开 |
| A2 | [市场选择源加载器](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/scripts/market-selection-source.mjs:31)、[计划源加载器](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/scripts/scheduled-schema-source.mjs:23)、experts-source 都引用模型源 | 必须重新生成所有传递依赖及锁，不能只跑 generate-chat-models |
| A3 | [Host 配置](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/chat_models.go:108) 固定旧 model；[turn 校验](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/session_protocol.go:785) 只为旧 profile 放行 max；runtime.go 和 session/chat_models.go 还有默认值 | 更名要覆盖默认、start/resume/turn、状态回执和 effort 校验，建议从同一活动定义派生 |
| A4 | [受管文件升级](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/chat_models.go:115) 用当前 Definitions 动态重建“旧”catalog，TOML 只接受 config→config | 换定义后无法识别磁盘中真正的旧字节；先冻结已知旧 catalog/TOML，沿精确 preflight 和原子替换升级，不能删 Home 或放宽检查 |
| A5 | [Runtime 搜索补丁](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/patches/chat-models/0006-native-web-search-sources.patch:168) 只在 slug 等于 kimi-k3 时追加 sources include | 新模型会丢失来源请求；修改可重放补丁并构建新候选，不直接编辑固定 codex-rs 源树或现有 binary |
| A6 | [TS catalog 验证](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src/api/chat-model-client.ts:18) 精确比较默认 profile 与每项定义；[Native 身份白名单](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/chat/host_bridge.rs:1631) 固定 model/provider | Host 单独上线会被 Desktop 拒绝；先完成兼容 reader/consumer，再激活新值 |
| A7 | [SQL migration 0028](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/migrations/chat/0028_chat_models.sql:1) 三张表的 CHECK 仅接受旧 Kimi/MiniMax | 新 profile 无法写入；必须追加 migration、扩展存储可读值，不能修改已应用 migration |
| A8 | [Host store](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/session/store.go:70) 和 Desktop 分别保存会话选择与原操作 profile | 当前会话绑定可以迁移，已接受操作/历史模型事实不能改写；未决发送不能改名后自动重投 |
| A9 | [选择逻辑](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/session/chat_models.go:133) 在读操作回执前检查请求和可用性；[响应校验](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/app/chat_models.go:21) 同样严格 | 硬删旧 enum 会阻断只读幂等回执或令旧 Selection 返回 503；区分历史合法性、终态回执读取与新执行资格 |
| A10 | [计划读取](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/chat/schedules/store.rs:111) 直接解码模型枚举，计划执行还绑定 profile/revision/grant | 旧计划必须可读；新模型身份需更新计划并重新授权，不能沿用旧 grant 自动执行 |
| A11 | [标题生成](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/title.go:121)、[草案生成](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/scheduled_draft.go:149)、market/expert submission 均使用选定 profile | 防止主聊已换但标题、草案、专家或定时执行仍调用旧模型；保留 input-only、权限和审批约束 |
| A12 | [Runtime 元数据 fallback](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/models-manager/src/model_info.rs:75) 为未知 slug 使用默认元数据 | 新模型必须进入 Host 受管目录；不能依靠通用 fallback 获得正确的 1M 上下文 |

Desktop 代码当前最多可读 schema 37；不同能力开关的迁移目标不同（仅 models 到 29，连接器启用可到 37）。这只是代码事实，本轮没有读取用户实库 user_version。新迁移建议用下一个可用编号（当前为 0038），并同时更新 migration catalog、可读版本和 models 启动目标；实施时应重新核对是否有并行任务占用该编号。旧 reader 不能直接读取新库，必须先建立兼容回滚版本。

**协议、能力和辅助路径的核查结果**

- **Responses/SSE**：现有直连链可复用。保留 0004 的 `tool_choice=auto`、0005 的终态完整工具参数恢复及其边界校验；不得因模型更新就删除它们。验证文本、推理、function_call、工具结果回传、搜索来源、completed/failed/incomplete 和正常取消，不能只测单轮文本。
- **请求参数**：Runtime 根据 catalog 生成 reasoning，并发送 `reasoning.encrypted_content` include；当前 Responses 文档只明确列出两种搜索 include。这属于需验证的文档/实现差异，不是已证明的故障。先抓取脱敏的实际请求字段，再判断是否需要最小 provider 兼容补丁。[请求构造](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/client.rs:802)
- **模型能力**：Host 从 MiniMax baseline 克隆 Kimi catalog，继承 reasoning summaries、text/image、parallel tools、900000 自动压缩阈值及 supports_search_tool=false 等值。后者不等同于关闭原生 web_search；不能仅凭名字改开关。把这些配置逐项明示，保留当前行为并针对新模型验证。[目录生成](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/chat_models.go:75)
- **上下文压缩**：Kimi 不走 OpenAI 的远端 compact 分支；本地编排通过当前 turn 的 model/effort 继续请求 Responses。需要验证迁移后压缩与续聊保持新模型。[compact](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/compact.rs:668)
- **子代理**：普通 spawn/fork 继承当前配置；新上下文和 role 可以覆盖模型/provider。不能只测父对话；还要核对可启用 role/显式覆盖是否可能请求退役模型。保持现有编排，不新增代理循环。[spawn](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs:89)
- **附件与图片**：沿现有受控附件、text/image 输入及历史解析。K3.1 Pro 多模态能力不自动意味着当前客户端新增视频入口；本任务不扩展输入协议或替换独立产图服务。
- **Kimi 网页工具**：worker 使用固定 `/v1/tools/search`、`/v1/tools/fetch`，不发送主模型 model 字段；复用 Host 已加载 Key，经私有启动管道传入。改名不应改变其安装、停用、凭据、逐次审批与零网络准备语义。[worker](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:182)、[凭据接收](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/model_credentials.rs:8)
- **Token/费用**：当前 Runtime 解析 input/output/total/cached/reasoning tokens，未覆盖 cache_write_tokens。可以保留本次范围，但不得声称已得到精确费用；验收同时记录真实用量、未知用量和预算覆盖差异。
- **独立工作流**：Coze 的模型管理属于另一执行路径；易界目前受控 workflow-local 限制节点且关闭模型，不应把上游模型模板批量改成 K3.1 Pro。API/Admin/Knowledge 没有发现需要随本次替换而改动的活动 Kimi 调用。

**推荐实施顺序**

1. **固定本次范围和已有工作树。** 建立当前本地候选实施记录，保护 FEAT-162/163 修改；把活动模型替换、历史兼容及以下 Must AC 一次写清。默认延续 local 开发范围；不混入上线、提交或推送。保存本次 source/patch/manifest 基线。
2. **先修改模型权威源。** 新建活动 profile `kimi-k3-1-pro-max-v1`，model/label 采用目标值，MiniMax 保持。活动 catalog 仍只有两个模型。定义旧身份的历史读取及迁移规则：新执行只能使用活动 profile，历史 Selection、plan 和已完成操作可以读取旧身份。更新本地 family 版本、源 schema、OpenAPI 和一致性测试；不要沿用旧 0.1.0 资格或把本地 candidate 当发布 tag。
3. **处理所有契约传递依赖。** 从 chat-models 源重新生成 Go/Rust/TS/JSON；继续刷新 market-selection、experts、scheduled draft/plan/execution 及其相关 native 投影/validator/锁。以依赖图和生成差异核对，不凭“生成命令退出 0”判全链路完成。只使用仓库 canonical generate/sync，生成物不手改。
4. **形成 Runtime 新候选。** 调整 0006 的模型条件，使新模型携带搜索来源 include，保持 0004/0005。为 canonical 构建和测试入口增加独立修订输出目录，保留已有构建产物；固定上游 `rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d` 和 Rust 1.95.0，不升级整个 Runtime。新 manifest 记录 source/patch/binary/schema hashes。预期此次模型条件修改不改变 app-server schema，与当前 web-sources schema逐字比较。
5. **更新 Runtime 投影和 Host。** 新 Runtime 候选完成后更新 runtime-chat-models 权威投影及下游锁；Host 默认、catalog、status、start/resume/turn、effort、标题、草案全部消费新身份。冻结已知 K3 受管文件 predecessor，沿原 authority 升级。不修改用户全局 Codex 配置。将历史回执读取与新执行可用性检查分离，保留身份/授权/operation 参数一致性校验。
6. **先完成可读迁移，再允许新写入。** Desktop 新增 SQL migration，受控重建三张模型子表的 CHECK、逐行保留原数据，并同步更新 `migrate_to_target` 允许列表、catalog 和能力开关的迁移目标；不能只改 Rust 枚举或旧 0028。Host bbolt 按本仓存储规则处理。更新 TS/Native 的默认值与模型映射。原生会话保持同一 thread，只有 idle、无 pending/unknown 操作、无待批工具且 Runtime resume 确认成功后，才保存新 profile/revision。Desktop 以 Host 返回事实刷新，不能先改本地标签再期待 Runtime 跟上。
7. **单独处理计划与未决操作。** 旧计划保持可读，旧 Kimi 计划提示升级并停止自动派发；更新新模型后，旧授权失效，沿现有流程重新审阅授权。历史 operation/outbox/digest 不改写；已完成仅返回原回执。确认从未发送的待提交操作走正常取消，再由用户明确新提交；unknown 先查询原生/Host 状态，仍不确定则继续阻止切换，不自动生成新请求。用户明确重新发送时使用新 operation 和新 profile。MiniMax 计划与正常历史维持原语义。
8. **标准构建、验证、再激活。** 先完成兼容 reader、生成校验、普通本地集成及候选产物锁，再通过正常入口构建本地 App。等待活动任务正常结束或用户正常停止，使用应用自身退出流程载入新 Host/Runtime。对实际出站 model、工具回传、历史与计划完成验证后，才把迁移标为完成。

模型业务契约先行；Runtime 二进制身份/协议投影则必须遵守 `Runtime candidate → Contracts projection → Host/Desktop` 的上游权威顺序。这两条依赖不能互相倒置。当前 `generate-runtime-chat-models.mjs` 固定 web-sources 输出路径，必须随新候选输出位置更新；不能只改 manifest hash。[Runtime 投影生成器](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/scripts/generate-runtime-chat-models.mjs:12)

现成 `test-chat-model-stream-args.sh` 固定旧 stream-args 目录、只重放到 0005，不能用它的 PASS 证明新的含 0006 候选。需为新候选建立/参数化同源验证入口。[现有测试入口](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/scripts/test-chat-model-stream-args.sh:6)

Desktop 构建还有一个容易遗漏的来源分支：当前启用组合可能实际选择 FEAT-159 的 `artifact-media-host-build.candidate.json`，而不是名称带 chat-model 的候选；必须按真实选中组合重新 freeze Host source digest、相关契约及 experts/resources，再正常构建。不能只更新其中一个 candidate 便宣布 App 已使用新模型。[候选选择与校验](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/scripts/chat-model-build-candidate.mjs:40)、[正常启动入口](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/scripts/run-local-demo-fast.sh:155)

UI 改动需同时覆盖 `ChatModelControl`、`useChatModels`、内存 composer drafts、`ChatPage` 草案退出默认、`useScheduledPlanModel`、`ScheduledPlanForm` 和计划详情名称。尽量统一读取生成定义，避免新聊天已显示新名称而计划仍显示 Kimi-K3。`kimi-web` 是独立服务 ID，保持原名。

**兼容与回滚规则**

| 对象 | 升级时行为 | 失败/回滚时行为 |
|---|---|---|
| 新聊天/新草案 | 默认新 Kimi profile | 明确不可用/重试；不静默请求 K3 或 MiniMax |
| 已结束旧 Kimi 会话 | 通过正常原 thread resume 完成下一次执行身份升级；旧消息仍标原事实 | 未确认成功不提交新选择；显示升级失败/unknown，允许正常恢复 |
| 活动会话/待批工具 | 等待正常终态或正常取消，禁止中途改身份 | 不强杀、不伪造结束 |
| 已完成 operation | 可读取原回执，不产生模型 HTTP | 不重写原 profile/digest，不重执行 |
| pending/unknown/outbox | 查询并对账原状态；不把旧请求替换后自动发送 | 保留可见未决状态，需要明确新提交才调用新模型 |
| 旧 Kimi 定时计划 | 可读、待升级；新模型执行需更新计划和授权 | 继续停用自动派发，保留计划/历史/墓碑 |
| Runtime/Host/Desktop | 候选和来源锁形成一致组合 | 回退到能读两代数据的兼容构建，或前向修复/停用新 Kimi 执行 |
| 数据库和历史 | 追加有序迁移，保留原事实 | 禁止降库或用旧数据库覆盖新历史；旧二进制不作为默认回滚方案 |

不采用“保留旧 profile 名但偷偷把它指向新模型”：这会混淆已接受操作、计划授权和历史执行身份。不采用“删除所有旧字符串”：历史文件、兼容 reader 和旧受管配置指纹必须保留。最终零残留要求应针对**活动配置、新执行路径和出站请求**，不是篡改历史证据。

**必须通过的验收标准**

| AC | 可判定标准 |
|---|---|
| 01 活动目录 | UI/API 仅提供 Kimi K3.1 Pro 与 MiniMax；默认新 Kimi；无可选择的旧 K3 |
| 02 精确请求 | 普通聊天、续聊、标题、专家、草案、计划的 Kimi 请求都为 `kimi-k3.1-pro`/max；没有旧 K3 请求，也无静默 provider fallback |
| 03 首启升级 | 已知旧 catalog/TOML 正常升级，未知配置不被覆盖；不删 CODEX_HOME，不改变用户全局配置 |
| 04 会话与操作 | 旧历史可读、原 thread 续聊、模型切换后 revision 正确；已完成回执不重执行，未决 outbox 不自动改名重发 |
| 05 工具闭环 | 正常本地工具调用→参数完整→执行→结果回灌→最终回答；input-only 草案不获得执行工具 |
| 06 联网与凭据 | 原生 web_search 的真实 sources 到 UI；Kimi Search/Fetch 共享密钥/审批语义保持；两类调用分账，不将本地 ready 当上游鉴权成功 |
| 07 图片与长上下文 | 图片输入可用；长上下文压缩、子代理继承及恢复无旧模型路由；历史附件原状态保留 |
| 08 计划授权 | 旧 Kimi 计划升级后旧 grant 不可执行，新计划/重新授权可执行；MiniMax 计划不受影响 |
| 09 状态与恢复 | loading/缺凭据/权限拒绝/不可用/取消/失败/incomplete 如实呈现；正常重开历史不丢失，不伪造最终成功 |
| 10 构建与界面 | 同源 Runtime/Contracts/Host/Desktop receipt一致；模型长名称在亮暗/窄窗口可读；标准入口和正常退出通过，兼容 reader回滚方案经普通合成数据验证 |

验证分层：先源契约与安全单元测试，再新候选 Runtime 的本机普通 HTTP/SSE 集成和合成存储迁移，最后真实 canonical App 的付费小规模验收。错误分类通过纯内存/普通本地协议数据验证，禁止强杀、权限破坏、恶意载荷和二进制伪装。测试预先按函数名建立安全 allowlist，不盲跑含历史危险测试的全量入口。

真实验收必须另列本任务的用户回合、模型 HTTP、图片、原生搜索、独立 Search/Fetch、输入/输出预算与停止条件；额度不足时保留 NOT RUN，不沿用 FEAT-156/162/163 剩余额度，不充值、不自动追加。标题/草案/工具后的后续 Responses 也计入模型 HTTP。预算覆盖和日常原始请求分开记录，输出截断不能通过擅自提高上限掩盖。

**本次已经执行的验证**

| 验证 | 结果 | 能证明的范围 |
|---|---|---|
| 12 仓 branch/HEAD/remote/status 核查、源码和已有设计审计 | 已完成 | 当前工程基线及替换影响 |
| `node --test tests/chat-models.test.mjs`（Contracts） | 3/3 PASS | 旧两模型身份、请求约束、路由来源 |
| `node scripts/generate-chat-models.mjs --check` | PASS | 现有权威源与生成物一致，未写入 |
| `node scripts/sync-chat-models.mjs --check` | PASS | 现有 Host/Desktop 派生物与源一致，未写入 |
| Host 8 个精确名称普通单元测试 | 8/8 PASS | 现有配置升级、切换、effort、凭据、回执及草案存储基线 |
| 新模型真实请求/账号权限/质量/费用 | NOT RUN | 本轮只做审计与方案，不是迁移验收 |
| 新 Runtime 构建、SQL migration、App 启停/真实 UI | NOT RUN | 尚未实施；没有改变当前应用和用户数据 |
| 全量测试及禁止的故障/攻击项目 | NOT RUN | 未执行强杀、可执行伪装、权限破坏、攻击 fixture；不宣称全量通过 |

Host 实际执行命令（事先逐项审查安全性；仅本地编译、普通内存/临时数据）：

```sh
go test ./internal/codex ./internal/session ./internal/app -run '^(TestChatModelProgressUpgradePreservesOwnedCatalogCompatibility|TestChatModelSwitchAfterTerminalErrorRetainsNativeLifecycle|TestChatModelCatalogKeepsLegacyEffortsAndExactKimiMax|TestChatModelVerificationCoversBothProvidersAndCredentialsAreScoped|TestChatModelSelectionRevisionReplayAndLegacyProtection|TestChatModelAcceptedTurnKeepsOriginalSnapshotAfterSelectionChange|TestChatModelStorePreservesDraftPurposeInVersionSeven|TestChatModelCredentialSources)$' -count=1
```

本轮 11 项测试都是**现有 K3 实现基线**，不能写成 K3.1 Pro 已兼容。FEAT-163 的长任务进度、空操作和 8192 诊断上限下交付失败依旧是原任务未关闭问题；模型升级后需要重新观察，不能预先承诺升级即修复。[既有未完成状态](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/docs/features/FEAT-163-codex-process-parity/04-resume.md:5)

本轮仅新增此审计方案文档；没有修改产品代码、配置、数据库或二进制，没有提交/推送/发布，没有真实模型或工具业务调用。
