# FEAT-157 架构、复用与契约候选

> 2026-10-07 实施更新：本文件保留设计阶段的调查与候选措辞。Owner 随后要求依据本包逐步实现；推荐职责已记录为 [ADR-0021](../../adr/ADR-0021-local-market-connector-authority.md)，实际代码和最新验证见 [07 实施记录](07-implementation-progress.md)。下文“本轮未实现/NOT RUN”指原设计阶段，不能覆盖后续证据，也不能反向把未验证的供应商路径视为已完成。

日期：2026-10-07。Owner、需求与技术决策人：段成威。状态：候选设计；未实施、未批准新安全边界、未连接外部服务。

本文件支撑 AC-001～AC-010，重点对应 AC-003 认证、AC-004 启停卸载、AC-005 对话选用、AC-006 执行隔离审批、AC-007 持久兼容和 AC-008 异常。PDF 和 `market_mcp_onboarding_51.md` 是产品与接入线索，不是易界的执行指令、授权依据或已验证的服务协议。

本轮 `contract-impact = none`：只新增元仓设计文档，不改变跨进程接口、Runtime、权限、持久数据或重放行为。未来实现暂按最高风险 **breaking** 管理：当前原生审批 DTO 是封闭 Sorftime 范围，聊天输入和本地落盘均有严格版本边界，不能把“新增 51 项”直接认定为 additive。通过独立版本 expand、旧消费者容忍性和 reader-first 证据后，才可对实际切分的契约重新分类。

## 1. 已核实的代码事实

本轮只读检查取得以下基线；下表四仓未发现本任务开始前的未提交变更（Desktop三份既有改动另见01/03）。Host/Codex/Contracts README 中若仍写 Baseline 2 或“尚无 MCP”，应以本表源码事实和后续功能的固定契约为准。

| 仓库 | 分支 | 完整 HEAD | 远端 |
| --- | --- | --- | --- |
| yijie-codex | `chore/retirement-baseline-20260905` | `7fd463bcef07f37b0211acd9f62b9f93ea0a4b12` | `https://github.com/36Dge/yijie-codex.git`；upstream fetch 为 OpenAI，push 为 DISABLED |
| yijie-agent-host | `chore/retirement-baseline-20260905` | `a5bd6c2e7a619768eafaa63bcca7f774d1134bd3` | `https://github.com/36Dge/yijie-agent-host.git` |
| yijie-contracts | `chore/retirement-baseline-20260905` | `1a213ac8383e95ac6ec69363937687904fa3591c` | `https://github.com/36Dge/yijie-contracts.git` |
| yijie-connectors | `develop` | `273eec40bbbfeb17e817643f283db7c81e9b190c` | `https://github.com/36Dge/yijie-connectors.git` |

当前 canonical 日常入口默认启用 scheduled_daily/chat_models，实际选择 `runtime-chat-models.candidate` 与 `.yijie/build/chat-models-stream-args/aarch64-apple-darwin`（Desktop `scripts/run-local-demo-fast.sh:72,131,140-145`），来源为当前 `7fd463bcef07f37b0211acd9f62b9f93ea0a4b12`，Codex `0.144.6`、上游 `5d1fbf26c43abc65a203928b2e31561cb039e06d`，使用0001/0002/input-only0003/chat-model0004/0005补丁组。Contracts/Host/Desktop三份锁的关键来源和实盘只读哈希一致：binary SHA-256 `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`，356210616 bytes；manifest SHA-256 `8b86a1a661f50beda1e0a0c96f81ddbdf959a9a07c2e756cc4b9b0eabc053b27`；269 schemas，tree digest `34d353815dc8d800cb432a876d5b43350511f63b91ad9766f861e8bc8290cc92`。Host `baseline.go:157`按该manifest准入。FEAT-136的 `b2b20e2fc4a0c94834f34d8cc459e488a1b56277`仅为保留stable/显式回退来源，不能冒称当前日常产物。codex-rs子树对该旧来源无差异只证明基础源码一致，不能代替补丁/构建资格；下文原生能力是候选静态证据，本轮未运行新worker或真实MCP。实际补丁分别涉及日志、Command生命周期、input-only禁用MCP、tool_choice和终态工具参数；未直接改写rmcp-client、app-server/src/request_processors/mcp_processor.rs、app-server-protocol/src/protocol/v2/mcp.rs、core/src/mcp_tool_call.rs，所以下述具体库发现仍适用，但选集/metadata/审批资格必须在当前制品验证，input-only保持零MCP。

### 1.1 复用矩阵

所有代码路径相对于表中同名兄弟仓；行号为上述 HEAD 的一基行号。

| 能力 | 事实与位置 | 结论 |
| --- | --- | --- |
| MCP 配置、transport、工具 allowlist | Codex `codex-rs/config/src/mcp_types.rs:435-462` 支持 stdio 和 streamable HTTP；HTTP 有 URL、bearer 环境变量、固定/环境 header。Host `internal/codex/sorftime.go:75-87` 已投影 `enabled_tools`、Prompt、超时和并行限制 | 复用配置与客户端；不重写 Agent 工具执行器。不能把平台 secret 写入这些配置 |
| 原生 OAuth 登录 | `app-server-protocol/src/protocol/common.rs:960-975` 有 `mcpServer/oauth/login`、`config/mcpServer/reload`、`mcpServerStatus/list`；`app-server/src/request_processors/mcp_processor.rs:112-222` 返回授权 URL，并异步发完成通知；仅支持 streamable HTTP | 可复用算法/库；不直接由 Agent Runtime 持有真实服务 OAuth token |
| 原生 OAuth 注销 | `codex-rs/cli/src/mcp_cmd.rs:503-535` 的 `codex mcp logout` 删除凭据；该 app-server method 集无对应 MCP logout | 不发明 `mcpServer/oauth/logout` RPC；Broker 可调用公开库函数删除自己命名空间内的凭据。删除本地凭据不等于远程平台 revoke |
| OAuth 存储 | `rmcp-client/src/oauth.rs:69-80,261-281`；`config/src/types.rs:102-115`：默认 Auto 会退回 `CODEX_HOME/.credentials.json`，Keyring 模式失败则报错 | 默认 Auto/File 不符合本候选；强制 Keyring，失败保持待配置/认证失败，不静默明文回退 |
| OAuth/HTTP 复用库 | `rmcp-client/src/lib.rs:16-47` 公开 discovery、login-return-url、save/delete、RmcpClient；`rmcp_client.rs:386-428,489-655` 公开 HTTP、初始化、工具/资源列表和调用 | 可候选复用固定 `codex-rmcp-client` 于 Connectors 窄 Rust worker；不复制协议栈，不先确定新增 SDK |
| stdio 生命周期 | `rmcp-client/src/stdio_server_launcher.rs:72` launcher trait sealed；`:258` kill-on-drop；`:330-334` TERM 后两秒升级强杀；`rmcp_client.rs:730-743` shutdown 使用该 terminator | 不可直接用于本需求。用户要求正常退出、不得因退出失败继续强杀；采用独立 EOF owner 与公开字节流桥接资格方案，见第 4 节 |
| 原生状态与分页 | `app-server-protocol/src/protocol/v2/mcp.rs:35-77` 返回 auth、tools/resources、nextCursor；`:236-251` startup 为 starting/ready/failed/cancelled | 可复用；ready/auth/tool 可见性是不同事实，不合并为单一“已连接” |
| 原生 reload | `app-server/src/mcp_refresh.rs:11-30,79-91` 仅把 refresh 入队；`core/src/session/mcp.rs:409-447` 稍后消费且解析可失败 | 不能把空 reload response 当停用完成、撤权完成或当前轮工具已收窄 |
| 每线程 config | `app-server-protocol/src/protocol/v2/thread.rs:94,380` 有 start/resume config；`request_processors/thread_processor.rs:131-133,3080-3122` 已加载且仍订阅时可忽略 resume config | 可候选用于新线程/正常 cold resume；不得承诺热 resume 自动切换选集 |
| 每轮选用/mention | `protocol/v2/turn.rs:68-158` 无通用 MCP allowlist 字段；`core/src/plugins/mentions.rs:41-59,62-102` 对 app/plugin mention 做特定收集 | UI chip/Mention 是意图表示，不是权限白名单；不能用虚构 `mcp://` 语义作执行隔离 |
| 原生 MCP 元数据 | `core/src/mcp_tool_call.rs:577,1083-1124,1127-1146` 附加 threadId、x-codex-turn-metadata；`core/src/responses_metadata.rs:280-300` 包含 thread/turn 及工作区元数据 | 可以作为绑定校验输入，不能独立作为授权。Broker 对远端移除内部 thread/turn/路径/仓库等无关元数据 |
| 原生工具审批 | `protocol/v2/mcp.rs:297-312` 有 thread、可空 turn、server，但明确尚无 tool Item 关联；`core/src/mcp_tool_call.rs:1705-1800` Prompt metadata 不含通用 tool_name | 不能从审批消息自然语言猜工具；必须证明对应实际调用，未证明时禁止高风险执行 |
| Host 原生 MCP | `internal/codex/session_protocol.go:298-313` MCP callback 路由至 Sorftime；`sorftime.go:231-303,440-512` 只接纳 exact server/product_detail/单 ASIN/US/实际 active turn | 复用线程、权限回调和生命周期；此封闭 allowlist 需版本化增量，不能直接泛化 |
| Host 输入/传输 | `session_protocol.go:164-201` 当前仅 text/image 输入；`:916-929` request helper 为私有通用 RPC 调用，不是开放给前端的任意代理 | 新 connector selection 必须是正式契约。所谓 Host allowlist 主要落实于方法投影、专用 handler 与配置/参数准入，不应声称已有万能动态白名单 |
| 当前 MCP 投影 | Contracts `compatibility/agent-host-native-mcp-v2.json:9-39` 仅选 Sorftime 的 status/config/elicitation/startup 等稳定方法、单工具和 ask 模式 | 未包括通用配置写、OAuth 管理或市场选集；新方法须从固定 canonical schema 投影并单独验证 |
| Connectors 现状 | `internal/app/app.go:30-42` 只有静态 health/ready/status；其 AGENTS/SECURITY 明确 vault/OAuth/MCP/审计未实现 | 这是待建立的接入边界，不能把骨架 ready 当 51 个 MCP 可用 |

### 1.2 安全决策与历史例外

Accepted [ADR-0005](../../adr/ADR-0005-token-boundary-and-approval-policy.md) 第 17 行要求平台 token 留在后端/Connectors；[ADR-0007](../../adr/ADR-0007-single-connectors-repo-first.md) 要求接入统一在 Connectors。Runtime 和 Host 仓规则也禁止直接获取、刷新或转发原始商家平台 token。

FEAT-144 实际采用经该需求授权的临时例外：`sorftime.go:28-42` 只允许显式 local profile 的内存凭据，`runtime.go:700-716` 把该账户 SK 注入 Runtime 子进程，固定单工具、Prompt、ask、公开商品查询。此事实与广义“任何平台 token 都不进 Runtime”表述存在需要明确界定的冲突，不能抹去或用“原生能力”自动扩大。FEAT-157 不继承 FEAT-144 真实服务、预算、token、权限或失败场景排除授权；也不重启已永久终止的 FEAT-137。

## 2. 推荐边界与方案取舍

推荐保持 ADR-0005：**Connectors 承载第三方凭据和接入；Codex 继续做原生 MCP client；Host 只做会话、策略与能力适配。** 所谓复用 Codex 不要求把认证和凭据都放进 Agent Runtime 进程。

| 方案 | 代价与适用性 | 本候选选择 |
| --- | --- | --- |
| 把 51 项直接写入 Runtime config，使用原生 OAuth | 开发量较低，但 token/refresh 进入 Runtime；OAuth 默认可明文回退；无法单靠 mention/全局 reload 保证每轮选集与撤权；stdio 自带强杀退出 | 不采纳。若未来考虑，须新的 Accepted ADR 和用户明确改变安全边界 |
| Connectors Gateway + 固定 Codex 库窄 worker | 保留凭据边界，复用 HTTP/OAuth/发现/调用；增加一个受管 worker 和精确源构建依赖；仍需补能力、审批与生命周期契约 | 推荐候选。先做无外部副作用的资格验证，资格通过后定稿实现 |
| 新建完整 MCP/OAuth/Agent 引擎 | 重复 Codex 已有能力，协议与安全维护面最大 | 不采纳。个别平台适配只能补真实差异，不能扩成第二套 Agent 平台 |

候选数据流：

```text
Desktop UI ──已有 native scope / 正式连接器契约──> Host
    │                                               │
    │ native 管理入口只提交设置意图                   │ 创建/收窄/撤销受管能力
    ▼                                               ▼
Connectors 管理面 ────────────────> Gateway 会话与凭据边界
                                          │
Host ──固定 app-server stdio──> Codex Runtime│
                               │          │
                               └─原生 MCP─> Gateway ─> 窄 Rust worker ─> 第三方 MCP
                                  本地受限能力          固定协议库      平台凭据仅此处
```

该图描述候选职责，不意味着已有相应 API、鉴权方案、端口或 worker。不新增仓库、不把 Connectors 源码复制到 Host、不把平台配置放进 Runtime fork；不默认搭建云服务、数据库、队列或一项一进程的 51 个常驻服务。服务客户端按有效连接和需求延迟建立，空闲资源有界释放。

Runtime 只接收短期、本机、当前 scope 内的 **Broker 调用能力**，它不是第三方 access/refresh token，不能兑换第三方凭据，也不能调用任意 URL。能力不得进入模型文本、工具结果、历史 chip 或日志。具体 carrier（受限本机端点/原生 header/受管 IPC）、保存位置、租约时长与撤销方式均需先形成契约和资格证据；不凭此文件发明 JWT、签名格式或“localhost 就可信”的规则。

## 3. 产品状态与后端真相

管理页面的“安装、配置、启用”和聊天中的“选用”是不同操作，必须分离保存、验证和投影。

| 对象/事实 | Owner 与生命周期 | 不得隐含的行为 |
| --- | --- | --- |
| CatalogEntry | Connectors 维护的非秘密版本化目录，稳定 service ID、分类、icon、传输/认证线索、官方证据与资格记录 | 目录存在不等于已安装或可调用；参考文件的 authType 不直接决定运行 |
| Installation | Desktop Native既有SQLCipher为唯一产品权威，按local identity/scope保存安装、非秘密config、目录/连接revision、desiredEnabled、opaque credentialRef和管理operation/tombstone；是对ADR-0013范围的候选补充 | 安装不能自动开启付费业务调用；外部依赖下载须确定版本、来源和许可 |
| Connection / CredentialRef | Connectors Keyring为秘密唯一权威；进程内维护当前授权、真实scope、到期/连接事实与attempt。Native仅保存不可兑换secret的不透明引用及非秘密状态投影 | 凭据原文不回传 renderer/Host/Runtime；同服务多个实例如本期不支持必须明确单实例规则 |
| Enabled state | 全局“允许用于聊天”的用户意图与实际执行闸门状态，存在 desired/effective 区别 | UI 开关变灰、配置写成功不等于旧连接撤销；撤权未完成显示处理中/失败 |
| Draft selection | Desktop 当前未发送输入的 chip；仅可选 effective enabled 且可用条目；可删除 | 不是持久运行授权，重新打开旧消息不能自动激活连接器 |
| TurnSelection | Host 接纳的当前 turn 选集快照，含所选 connection/config revision 与 scope；被 Broker 执行检查 | 不从历史文本、chip 名称、模型提到的应用名推导权限；不沿用前一轮选择 |
| Runtime observation | startup/auth/tools 清单和 actual Item/Turn 回执 | 服务“授权成功”和“当前工具 ready”分别展示；没有返回值时不能补造成功 |

全局停用先阻断新的 Gateway 执行准入，再处理已有调用与原生目录更新。运行中请求按真实取消能力处理：已送达远端而未确认结果只能记录不确定，不标“已撤回”。卸载撤销能力、清除安装配置及所属凭据引用；远程平台 revoke 不支持/失败需明确报告，不能把本地删除当远程注销成功。历史消息保留可读显示快照，且无可重新使用的授权材料。

推荐复用Native SQLCipher保存非秘密产品状态，不在Connectors新建安装业务数据库；该范围扩展须以Proposed ADR补充ADR-0013并由Owner确认，不能称现有已授权。Native单事务写入operation ID、expected revision、新意图与待应用状态；Host/Broker按同operation+revision幂等apply，回执只更新匹配revision的observed事实。停用/卸载未收到撤权/cleanup回执前保持pending/unknown，不展示完成。重开恢复desired，但执行先关闭，重新核验后才恢复effective，绝不复活turn能力。Keyring写入成功而Native回执丢失时，按同operation/opaque reference查证，不盲目重新授权；过期revision不能覆盖新token，孤儿引用需正常可追踪清理。Host bbolt仅mapping/能力，不存第二份产品真相；Connectors管理operation/attempt仅内存，重启后凭Native记录和Keyring所有权查证，无法证明则要求用户重试，不能伪恢复callback。秘密不得临时存localStorage/TOML/fixture/明文JSON。

## 4. 窄 worker 的复用与资格

### 4.1 固定库与构建边界

`codex-rmcp-client` 不是可以不加验证就复用的独立已发布 SDK。其 Cargo.toml 依赖 codex-api/config/exec-server/keyring-store/protocol/secrets 等 workspace crate。候选是在 Connectors 的受管 worker 内使用固定 Git 对象对应的库源和依赖 lock，按 canonical 构建流程产生独立可追溯制品；记录完整 source SHA、库/依赖 digest、构建器版本、许可证和 artifact digest。不从浮动 sibling 路径制作发布产物，不把整棵 Codex 子树维护成新 fork，也不覆盖日常 Runtime 或已签名/受审计二进制。

先验证 workspace 依赖闭包、macOS Keychain 行为、正常退出和可重现构建；之后才决定最小构建适配或必要依赖。若无法通过公开库边界复用，记录具体缺口和替代方案，禁止以“不能重复造轮子”为由静默引入未经评估的 SDK/补丁。

### 4.2 OAuth 与凭据

标准 OAuth 优先复用公开 `perform_oauth_login_return_url_with_http_client`、discovery、refresh 和 `delete_oauth_tokens`。worker 持有 token；管理面只投影授权 URL、operation ID、状态与安全错误。浏览器 URL、callback origin、scope 与远端 discovery 结果均限制在该目录服务的已验证范围；不把参考应用的 qwenwork gateway/client 注册信息当易界身份。

强制 `OAuthCredentialsStoreMode::Keyring` 并验证失败不产生 `.credentials.json`。Keyring 默认 service 名为 `Codex MCP Credentials`（`oauth.rs:69`），存储 key 为 server_name 加 URL 摘要（`:773-783`），不是按 CODEX_HOME 自动隔离的账户。因此 worker 必须使用稳定且不碰用户 Codex 的易界账户/连接别名，分别证明安装、重装、账户切换、并发 refresh、撤销与回滚不会读写另一实例。若原生命名机制无法满足已确认的 vault 所有权，才提出窄 storage adapter；不得声称仅换 CODEX_HOME 已隔离 Keychain。

API key、secret file 和 stdio 子服务私有授权只在 Connectors 的安全配置入口处理。确需用户输入秘密时，应通过经过评审的原生/Connectors 安全入口直接提交到所属边界，renderer 仅取得凭据引用和状态；不让秘密绕 Host 暴露。认证失败不删除仍可恢复的已有凭据，不以盲重试覆盖新 token。

`none` 只表示来源应用未管理 OAuth，不表示不需要账号或凭据。淘宝闪购来源是其它应用的代理 URL，须取得官方可用于易界的授权/接入依据或自有适配，未满足时如实阻断，不能借用第三方内部网关身份。

### 4.3 stdio 正常退出

两个 Google stdio 条目需独立验证固定包版本、启动参数、运行依赖、授权文件/Key、作用域及退出语义。不能把来源中的浮动 `npx` 命令作为已批准安装方案。Google Calendar自管OAuth，通用Codex Keyring不会自动保护它的credentials/token文件；普通私有目录也不等于安全存储。该包的凭据读取和token持久路径必须逐一审计，优先验证受支持的Keyring/内存storage adapter；如包强制文件持久而无法在Connectors边界安全适配，此项保持blocked，提出明确最小包适配或经Owner批准的加密存储替代方案后再实现，不放宽为明文目录。

原生 `LocalStdioServerLauncher` 会在 close/drop 时主动终止并升级强杀，且 trait sealed，不能外部注入替代 launcher。候选使用公开 `RmcpClient::new_in_process_client`（`rmcp_client.rs:331`）与 `InProcessTransportFactory::open -> DuplexStream`（`in_process_transport.rs:6-14`）：由 Connectors 的独立 owner 持有真实子进程，将 MCP 字节流桥接到库。这里只适配字节流和进程所有权，仍复用库的协议握手、tools/list/call，不写第二套 MCP 协议栈。

owner 必须使用正常 EOF/应用协议关闭、等待退出和可见 cleanup 状态；禁止 kill-on-drop、强杀升级、删除正在使用的目录。未能正常退出时记录 STOP_PENDING/清理失败并停止后续变更，不能伪造停用/卸载成功。桥接方式、库重连时的 owner 引用计数和不重复启动行为尚需资格测试；若公开 in-process 边界不足，候选退路是经过批准的最小库扩展，不能直接进入原强杀路径。

### 4.4 重试与资源上限

库 `rmcp_client.rs:939-973` 会对 session-expired 404 重建会话并重做 operation；`:1058-1071` 还对 tools/list 的特定 transport 错误重试。因此不能承诺“一个逻辑调用就是一次 HTTP”“MCP 无自动重试”。Gateway 和 worker 分别记录逻辑调用与实际外部尝试；写调用不具备幂等/明确未执行证据时禁止自动重放。复用库内恢复前必须证明符合服务契约；如需限制通过公开 HTTP client adapter 或明确最小扩展实现并测试，不能用外层一次重试计数掩盖库内再次执行。

限制单服务连接/发现/调用时间、目录分页、工具数量、schema/content 总量、并发数和缓存寿命；值在契约定稿时给出可测常量。鉴权失败、业务拒绝和权限不足不盲重试；网络/未知结果与业务失败分开。第三方 tool annotation 是声明，不自动成为风险豁免。

## 5. 当前轮选集的真实执行约束

选中 chip 后，Desktop 在发送时提交稳定 connection ID 与所见 revision；Host 根据当前 scope、安装、认证、effective enabled 和目录资格重新验证。旧 revision、已停用或已卸载返回明确可恢复错误，不静默删除后照常发送，也不自动扩大到所有连接器。

候选必须同时拥有两个边界：

1. **工具可见范围**：原生 MCP 客户端的当前线程 catalog 只呈现该次有效选集的工具。不是向模型注入“请只使用这些工具”的提示。
2. **最终执行范围**：Gateway 在每个 tools/call 前校验受管能力、真实绑定、当前 enabled/config generation、准确工具/参数与适用审批。即使 Runtime 缓存了旧工具或 refresh 尚未完成也拒绝旧能力。

Host→Gateway 的控制面候选建立不透明 managed session：绑定 local identity/scope、Host/Runtime generation、agent session、native thread、已批准的选集版本与有效时窗。在 `turn/start` 产生真实 native turn ID 前只允许必要 discovery，不允许业务调用；取得可信 response/notification 后完成 turn 绑定。存在事件与调用竞态时业务调用有界等待绑定或明确失败，不根据 payload 自报 turn ID 激活。

tools/call 的原生 `_meta.threadId` 和 `x-codex-turn-metadata` 可用于比对，不能替代能力。它们既不是签名批准，也不证明来自当前允许的 Runtime。Gateway 必须通过受管私有通道/受限能力验证来源，再与 Host 控制面记录进行精确绑定。能力不得授权任意 thread、后继 turn、工具或服务。远端只取得必要业务参数；内部路径、模型、git/workspace、Host identity 等字段不透传。

### 5.1 不存在的“简便接口”

- 不能调用虚构的 per-turn MCP allowlist RPC；固定 `turn/start` 没有此字段。
- 不能把 `app://` 的 Codex Apps 生态或 `plugin://` 的插件选择直接等价为易界任意市场 MCP。`mcp://` 链接最多是文本线索，没有已证明的选集 authority。
- 不能用全局配置写 + reload 隔离并发聊天。reload 对所有 loaded threads 入队，且旧线程可能保留原 override/缓存。
- 不能在已订阅 loaded thread 上简单 resume 新 config；源码明确允许忽略。
- 不能只在前端移除 chip、后台保留有效能力；也不能用“下次 turn 才刷新”解释撤权延迟窗口。

### 5.2 候选路径与必须证明的资格

优先候选为每线程受管 Gateway 会话加服务器配置投影，目录与最终调用都按该会话选集过滤。新线程通过原生 start config 建立；改变选集仅在实际 idle、无待决审批和无未知外部操作时进行。先撤销旧执行能力，再完成正常 unsubscribe/卸载/cold resume 或经验证的原生目录更新，并读取实际新 catalog；失败保留可见恢复状态，不自动回退到全局工具面。

以下资格验证均先使用普通、本地、合成且无攻击载荷的 MCP 服务；不改用户日常库、不连真实账号、不故意制造进程异常：

| 编号 | 要证明的事实 | 失败时的候选退路 |
| --- | --- | --- |
| Q-SEL-01 | 固定 start config 真正覆盖目标 thread 的服务器集，空选集不继承全局 server；两个普通 thread 的不同选集互不污染 | 不激活每轮选择，重新审议原生投影方式；不能用 UI 白名单代替 |
| Q-SEL-02 | 普通 turn→idle→正常 unsubscribe/完成卸载→cold resume 原 thread 的 config 变更生效，历史/订阅和计划用途不受损 | 保留旧线程只读状态；审议受限的正常重载方案或最小上游能力扩展，不新建隐藏聊天替换用户历史 |
| Q-SEL-03 | reload/缓存/延迟到达的旧请求都不能越过 Gateway 撤权；同一选集版本不得跨 turn 复活 | 收紧会话租约与 generation 绑定；无法证明则不允许该路径业务调用 |
| Q-SEL-04 | 原生 thread/turn metadata 的固定 schema、来源和正常缺失语义可以匹配 Host 确认的当前 turn；pre-turn discovery 不获得业务权限 | 未绑定时拒绝；不把元数据当授权，不向工具参数偷偷添加自报身份 |
| Q-SEL-05 | Tool Item、Gateway 请求、审批决策能够绑定同一真实工具和参数，重复调用、取消、结果不确定不会复用一次批准 | 未形成可信关联的写/高风险工具不可激活；按第 6 节重新审议 |
| Q-SEL-06 | 正常停用/卸载、进程正常退出、Host 重启使旧 session 能力失效，重开只恢复设置不恢复执行授权 | 展示未完成清理/需重连；禁止强杀、自动重新授权或假成功 |

“目录过滤 + Gateway 最终校验”是两层要求。可以先证明 Gateway 阻断再补目录新鲜度，但不能因最终会拒绝就声称 UI 的当前轮选集已经完整可用；没有通过 Q-SEL-01/02 不算 AC-005 完成。若固定 Runtime 无法以公开扩展点完成，须明确暴露缺口并提出最小 Runtime 变更候选，走原有 Runtime→canonical schema→Contracts 投影→Host 顺序；不能先在 Host/Contracts 发明上游字段。

## 6. 工具审批、风险和审计

复用现有 policy/API 作为审批权威，原生 MCP elicitation、Host callback 与 Desktop 卡片用于承接。不得建立新“连接器开关即无限批准”的审批系统；ask/auto/full 的既有 FEAT-152 语义不因连接器可见而被静默改写。

当前原生 Prompt 对通用多工具缺少可直接使用的 Item 关联和 tool_name。FEAT-144 通过唯一 enabled tool 推定 `product_detail`，代码在 `sorftime.go:492-494` 明确说明此限制。因此以下行为禁止：从显示标题/自然语言解析工具，拿最近一个 Item 配对，假定一次批准覆盖同服务全部工具，或把原生 `accept` 原样当成已签名的 API 审批证明。

可进一步验证的候选为 Broker-origin 的精确调用关联：Gateway 已掌握将要执行的 server/tool/原始参数与内部 call identity，经 Host 可信控制面请求既有审批，卡片确认后由 Gateway 校验同一批准上下文；原生 elicitation 仍用于客户端承接，其 metadata 只能携带不透明关联线索，不能自己授予权限。是否可在固定协议下避免双重审批、如何区分普通上游 elicitation 与 Gateway 请求，必须取得 Q-SEL-05 证据并完成契约设计。不能把此候选写成当前已存在的机制。

其它真实备选是单工具原生 server 别名（可沿用唯一工具证明，但有工具数量/命名/启动成本）或经过批准的最小上游关联扩展（增加构建与兼容成本）。默认不选伪造 call_id、推断 Item 或自建审批签名。不符合可信绑定的高风险工具保持未激活并显示原因。51项指51个服务均具备已明确且经审核的支持工具集，不默认承诺供应商全部工具；每项在联通后冻结工具名称/schema/风险/权限和排除原因，按00/02的统一完成口径验收。未冻结支持范围、必需工具缺失、或以只读样例冒称该服务全部功能，仍属于未完成。

工具注册必须包含官方 scope、输入 schema、风险、幂等和真实错误语义。未知风险默认拒绝，不因服务名或 `readOnlyHint` 自动降低。高风险批准至少绑定 identity/scope、task/session/turn、connection/config generation、server/tool、参数摘要、影响对象和有效期；签名/凭证形式复用已批准权威，缺失时等待确认，不在本文件指定新格式。

审计保存最小调用意图、批准引用、逻辑 operation ID、外部 attempt/request ID（可得时）、结果分类与耗时；token、授权码、原始 header/query、PII/完整经营数据和内部 `_meta` 不进入日志。沿用原生 Tool/Turn 生命周期和现有脱敏结果投影；不合成 Tool completed、不把审批 declined 等价成整个 Turn failed、不重建原生历史事实。

## 7. Contract First 与落盘设计

以下为要形成的契约清单，不是已定稿的 endpoint、DTO 或 schema。源文件、版本号和权限名称在源契约评审时确定；不得在 Vue/Go/Rust 三处手写同一 wire 模型。

| 边界 | Authority / producer → consumer | 需要表达的语义 |
| --- | --- | --- |
| 市场目录和管理面 | Contracts；Connectors/Host 适配 → Desktop native/UI | 稳定 service/installation/connection identity、分页/分类、认证需求、能力资格、desired/effective 状态、安全错误、版本/并发控制 |
| 安装/配置/授权/启停/卸载操作 | Contracts；管理服务 → Desktop | 幂等 operation ID、pending/success/failed/unknown、可恢复步骤、取消与实际副作用边界；secret 只用引用 |
| 当前 turn selection | Contracts；Desktop native → Host；Host → Gateway | current scope、选择 ID/revision、空集、当前 turn 生效、不可继承/重放、明确冲突和撤权语义 |
| Host↔Gateway 受管能力 | Contracts；Host 控制面 → Gateway | 来源校验、生命周期 generation、discovery-only/执行绑定、scope/工具过滤、撤销、过期、重放与正常清理；不含平台 token |
| 通用审批关联 | 既有 policy/API 权威 + Contracts 版本化投影 | 稳定调用身份、工具/参数/影响绑定、一次性决策、失效/拒绝/取消及结果不确定；旧 Sorftime DTO 不被放宽改义 |
| 原生 Runtime 使用面 | 固定 canonical schema；Contracts compatibility → Host | 实际需要的方法/通知、start/resume config、status/reload 语义、metadata/elicitation 能力与明确限制；不发明上游 RPC |
| 原始第三方 MCP | 当前官方服务规范及真实正常取样；Connectors adapter | endpoint、transport、OAuth issuer/client/scopes、tools schema、配额、许可与错误/幂等；参考清单只作线索 |
| 私有本地存储 | 所属仓 migration/data compatibility | Native SQLCipher的非秘密连接器设置/管理operation/credential reference、历史chip显示快照和格式版本；Connectors Keyring独立秘密生命周期；不属于公共契约时记录 N/A 理由，不能绕过兼容 |

Desktop 已有 SQLCipher/格式保护与 native conversation 版本；新增 chip/selection 持久化前先确定 reader-first 最低回退版本。旧消息与旧数据库不回填虚构选集，历史 chip 已卸载仍能显示但不能复活授权；未知格式记录诊断并禁止执行，不整段误解析为文本命令。私有连接器状态与 token vault 分开：加密聊天库不是放置第三方 token 的替代 vault。

发布/激活顺序：固定外部依据和 Runtime 资格 → Contracts 源与版本化兼容验证 → 兼容 reader → Connectors/worker 与 Host provider → Desktop 请求和 writer → 逐服务真实验收。新响应/枚举先证明旧消费者可容忍或升级消费者；新请求先有 provider；移除旧表面采用 expand/migrate/contract，不多仓硬切。demo_fast 本地候选可用当前 sibling 的适用 source-first 结果验证，不能冒充不可变发布 pin、tag、Owner 批准或 supported 版本。

回退先关闭新请求/writer 和新能力颁发，Gateway 撤销新租约并正常清理，保留最低兼容 reader、已加密凭据与历史。不得降数据库版本、覆盖旧二进制、删除用户全局 Codex 配置或清空 Keychain 作为回滚。凭据存储迁移独立记录 origin/revision，不因应用回退把旧 token 覆盖新 token。

## 8. 验证、失败语义和完成边界

### 8.1 普通安全验证

本任务只允许正常、非破坏性的开发与验证。可用合成配置、正常本地服务、正常用户取消/拒绝、合法空结果、官方说明的普通错误和静态 conformance；不注入攻击 payload、危险归档，不破坏权限，不替换可执行文件，不通过强杀/崩溃制造异常。仓库现存旧测试含危险 fixture 时必须筛除，并记录未执行项、原因和影响，不能用全仓 PASS 掩盖跳过。

| 对应 AC | 需要的证据 |
| --- | --- |
| AC-001 目录 | 51 个稳定 ID 与 icon/分类对应，来源差异和未知项可追溯；无借用他人内部凭据/身份 |
| AC-002 安装 | 幂等、版本/依赖资格、普通取消与重开；未完成的安装不能标已可用 |
| AC-003 认证 | discovery→正常授权/取消→Keyring→refresh/失效状态；无明文 fallback、无 token 进入 Runtime/UI/日志；服务官方依据 |
| AC-004 启停卸载 | desired/effective 区分、先执行撤权、正常清理、旧 lease 无效、卸载后历史可读 |
| AC-005 对话选用 | Q-SEL-01～04；空集、选择变更、两个正常聊天隔离、已停用条目阻断，chip 与实际工具面一致 |
| AC-006 执行隔离审批 | Q-SEL-05；既有权威审批关联、准确参数、普通拒绝/取消、过期后不复用；无批准则不触达高风险外部操作 |
| AC-007 持久兼容 | reader-first、旧库/旧消息原样兼容、普通退出重开、未知格式安全诊断及兼容回退 |
| AC-008 异常 | 普通网络/认证/限流/平台拒绝/结果不确定分类、有限重试、操作查证、cleanup pending；未验证的服务错误不可伪造 |
| AC-009 视觉键盘 | 沿用 Desktop 易界 token、明暗主题、1180×760、焦点与键盘；管理状态与对话 chip 的真实回执对应 |
| AC-010 逐服务真验收 | 每项记录授权来源、服务/工具/schema/config revision、真实认证/发现/一次正常调用及结果证据、成本/副作用、未完成原因 |

“同一协议 family 的 fake 通过”“已列出 51 张卡片”“认证 URL 能打开”均不能代替 AC-010。受外部 client 注册、scope、付费额度、第三方内部 gateway 或正常测试条件限制的条目必须列 BLOCKED/NOT RUN，整体不报 51 项接入完成。逐服务真实调用仅按用户明确账户/费用/外部副作用授权执行，不继承旧 FEAT-144 的剩余额度。

### 8.2 本轮未执行与影响

本轮只读取仓库及提供的清单、形成设计文档；未构建 worker、未写契约/产品代码、未修改 Runtime、未创建/读取真实凭据、未调用 OAuth/MCP/模型、未启动或停止应用，未进行数据库迁移、提交/推送/部署。Q-SEL、Keyring、stdio 桥接和逐服务资格均 **NOT RUN**。因此本文件提供可审阅的架构候选和明确资格路径，不证明这些能力已实现或产品已通过 D4。

需要最终定稿的实质决策是：Connectors 窄 worker 与固定库构建方式、vault/账户命名隔离、Host↔Gateway 能力 carrier 与可信绑定、通用审批关联方案，以及逐服务官方授权/费用/正常测试条件。上述问题可在当前代码事实基础上准备具体契约和安全资格结果；没有依据时不得以“已安装”“已启用”或文案上的“Beta”掩盖缺口。


## 9. 管理面和权限的推荐逻辑契约

以下名称是本包候选语义，正式wire名称/路径/字段由Contracts源生成；不是已经发布的RPC或可直接使用的DTO。

| 操作 | 输入意图与幂等 | 权威效果/失败 |
|---|---|---|
| catalog/read、installations/read | current scope + known catalog revision；只读 | 固定51目录与当前scope的安装投影；不连接全部外部服务、不显示别的scope账号 |
| install | catalog ID、expected revision、operation ID | Native一次事务登记且desired=false；重复同ID同意图返回同结果，不运行包/业务 |
| configure/authorize | installation ID、expected generation、operation ID；secret只走原生安全入口到Connectors | 绑定当前attempt/scopes/redirect、Keyring保存后返回opaque ref；取消使attempt失效，浏览器回跳只查证 |
| enable/disable | installation ID、expected revision、目标desired、operation ID | Native写意图→Broker确认应用→更新effective；disable先撤销新执行能力，清理pending单独显示 |
| uninstall | installation ID、expected revision、operation ID、产品确认 | tombstone阻止新能力/授权；正常清理后完成；清理部分失败保留可恢复记录，历史不删 |
| operation/read、cancel | 当前scope及原operation ID/revision | 查询原事实；取消只作用于仍可取消阶段，外部已发出不承诺撤销 |
| turn/submit版本化扩展 | existing submission identity/模型/正文附件 + connector refs及generation | Native原子出站快照→Host再校验→当前turn能力；不兼容或选集变化直接拒绝，不转文本忽略 |

同operation ID不同参数返回冲突；不同operation但同目标旧revision返回冲突并读取最新状态。管理记录只保存安全字段，不保存OAuth URL参数、secret原文或远端敏感响应。UI关闭不取消后端attempt；取消/卸载/换账户会令旧attempt完成失效。

候选权限分为四项：connector.read（目录/当前安装只读）、connector.manage（安装/启停/卸载）、connector.credentials.manage（原生凭据配置/重授权）、connector.use（本轮使用）。不复用knowledge.read或plugin.manage暗授权限。local direct-entry需在Contracts/native固定scope/Host准入中显式加入对应能力；public模式须由API权威身份/RBAC发放且本期保持不激活。只拥有read可浏览，缺manage不能操作开关；有manage无credentials可安装/停用但不能改账号；use仍须该连接已配置/启用且请求属于当前scope。管理权限不等于使用/写工具批准。

每个管理请求由Native验证当前scope/capability，Host验证受管调用方和scope，Broker验证Host控制面能力、版本与credential归属；任何一层拒绝都不能由UI绕过。业务tools/call再由Gateway检查current turn、connection generation、supported tool、参数和批准上下文。缺少capability或未知权限枚举默认拒绝；不发送新枚举给仍严格拒绝的旧consumer。

统一逻辑错误族：not_configured、authorization_required、authorization_cancelled、dependency_missing、provider_onboarding_required、permission_denied、revision_conflict、unsupported_capability、rate_limited、temporarily_unavailable、operation_pending、outcome_unknown、cleanup_pending。正式错误码先入Contracts；UI映射可理解恢复动作。已受理未知先查询原operation；未受理配置错误允许原意图重试；已完成外部写入未知不自动再发。

本包默认管理操作等待窗口30秒后转为查询原operation，OAuth attempt候选5分钟超时（供应商更短限制优先，具体值进入受管目录），单应用同一时间一个管理操作；切换app不影响其他项。网络重连/分页/工具预算沿Codex已支持限制与供应商正式配额定稿，并记录有效值；没有上限不得激活。超时表示观测或等待到期，不能推断未执行。
