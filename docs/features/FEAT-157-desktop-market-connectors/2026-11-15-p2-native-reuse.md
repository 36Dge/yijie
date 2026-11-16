# 连接器剩余三个 P2：方案与实施记录

2026-11-15。用户要求承接原审计第 3／4／5 项，细化后直接实施；继续保护未提交工作，
不调用真实供应商／付费模型，不提交推送，不重启易界服务。截图用于定位原记录，
完整原审计已从“审计易界连接器运行架构”聊天读取。

## 范围与原生复用

1. **决定历史**：P1 已通过原生结果 `_meta` 保存有回包调用的关联。无回包的决定在
   现有 Native SQLCipher 会话库追加只读事实：发送前的用户决定意图、经过核对的 Host
   确认、未取得确认。记录原 callRef／decisionId／thread／turn／选集／参数摘要；不保存
   原始参数、credentialRef、capabilityRef、令牌或可重放请求。不创建新的数据库、审批
   状态机、发送队列或恢复执行入口。事实随原会话删除，只读查询有上限与截断标记。
2. **结果投影**：抽取同一个有界、脱敏的原生 MCP 结果投影，用于市场历史、原生通知与
   普通原生 MCP 展示。结构化 JSON 转成安全展示文本；纯 JSON 可供旧 reader 阅读，
   与文本相同的 JSON 去重，不同的文本／JSON 分别标明来源。只在实际省略／限长时标记
   截断，不将批准、许可消费或有回包解释为业务成功。
3. **观测复用**：复用 Runtime 原生 item/started、item/completed、turn 通知及现有
   Native 会话订阅。Host 只维护有界、可丢弃的结果展示快照，不建立调用执行生命周期。
   当前结果由原生通知触发刷新；定时查询只读轻量审批。完整 thread/read 保留在首次
   缺失快照、明确刷新、重连恢复与历史轮次查看，不再每秒／空闲每三秒重读整线程。

不修改 Runtime；不扩展原生事件 wire，沿用其现有文本展示与身份字段。市场 `_meta`
关联仍由 P1 的可信结果回执核对，不能通过模型文本、时间或同名工具猜测。

## 契约与存储

`contract-impact=breaking`：HTTP/IPC 新字段为 additive，观测语义为 semantic；
SQL 47 拒绝旧 reader，因此整体按最高风险分类。先更新 market-host v1/v2 的 canonical source，再生成并
同步消费者。新增可选的结构化展示来源、只读决定事实和查询方式；旧请求默认保持
历史读取语义，旧 reader 可忽略新增输出。当前本地来源采用已接通的完整 v2 候选检查，
release=false，不伪造 immutable commit。

SQL 47 writer 限定于当前 `kimi-k31-pro-candidate` 产品；旧 profile 命令保持原存储
行为，决定事实输出可缺省。SQL 前向 migration 47 只新增会话内的决定事实表，不改旧迁移、旧事实或 Native 历史
格式。首次写决定前先持久化意图；持久化失败不发送决定。确认必须匹配当前 scope、
原审批身份和决定 ID；未确认只表示信息不足。读取事实不能重新生成批准或许可。
旧库没有新表时可读为空；47 的 reader 必须先于 writer 就绪。回滚保留新 reader，
不得降 user_version、删除事实或把未知操作重新发送。

## 定向验收计划

- 正常批准／拒绝／取消，决定意图与确认分离，无回包时不声称成功；正常关闭重开后
  原事实可读；跨会话／原轮次校验、会话删除级联与旧库读取。
- 纯结构化、文本与 JSON 相同／不同、空结果、isError、普通长结果和脱敏；原生通知
  与历史投影一致，原状态及 P1 关联不变。
- 多次轻量审批轮询不触发 thread/read；原生开始／完成通知刷新同一快照；首次、
  重连、用户历史读取允许一次实际读取；读取与通知竞态、快照淘汰和迟到 UI 请求。
- 只运行上述相关 Go／Rust／前端与契约检查；无攻击 fixture、权限破坏或强杀。
  最后独立源码复审、检查生成物来源与原有工作区差异。实际服务迁移及 GUI 复验未执行。

## 已实施的最小方案

| 原 P2 | 实现与复用点 | 主要源码 |
| --- | --- | --- |
| 第 3 项：决定历史 | 沿用原生结果 `_meta` 保存完成调用；Native 在现有 SQLCipher 库追加 requested／acknowledged／unconfirmed 事实。历史只读，未确认事实不会自动重发；重新打开界面也不会把同一未确认决定变成新的可点击审批 | Desktop `connectors/decision_facts.rs`、`connectors/observe.rs`、migration `0047_market_decision_facts.sql` |
| 第 4 项：结构化结果 | 同一投影函数处理文本／JSON、完整拷贝去重、脱敏、原始数字和总 64 KiB 展示预算；市场的纯结构化结果走 resultText，来源为 structured；不同 JSON 走 structuredResultText | Host `internal/session/market_result.go`；Desktop `MarketChatActivity.vue` |
| 第 5 项：重复观测 | 复用现有原生通知入口和会话订阅；Host 展示快照最多 64 轮、共 8 MiB；前端事件触发当前快照读取，活动期定时查询只取审批，已连接空闲时停轮询；明确历史读取与恢复仍读取 Runtime | Host `market_tool_snapshots.go`、`native_conversation.go`、`market_http.go`；Desktop `chat.store.ts`、`useMarketChat.ts`、`host_bridge/market.rs` |

契约先行更新为 market-host v1 **0.6.0**、v2 **0.8.0**。复用 canonical generator／sync
生成 Go、Rust、TS 和 JSON Schema；provider／experts 的依赖来源记录一并刷新。
Connectors 仅更新 provider 来源记录，没有修改执行代码；yijie-codex 完全未改动。
当前仍是显式本地候选，不能当作 immutable 发布来源。

结构化结果没有伪装成原生 content：v6 原生视图保持原始 content 下标及既有整行脱敏
语义，没有内容块时不编造 index 0；不属于原始 content 的 JSON 在该视图如实标为
partial／unsupported，并通过市场观察字段提供有界 JSON 展示。没有新增原生协议或
Runtime 补丁，也没有为这一步另建执行结果数据库。

补充修复了复用过程中发现的实际缺口：通用 worker 工具名称为 `m_<60 位小写十六进制>`，
原命令令牌过滤器会将其整体过滤。现在仅对 owned `yijie_market` 的此种公开名称放行
显示；其他 server 与结果正文的保密规则保持。测试用 worker 相同算法构造普通工具名。

## 决定与结果事实的含义

| 事实 | 能证明 | 不能证明 |
| --- | --- | --- |
| requested | 用户决定意图已在 Native 持久化 | 已经送达 Host／worker |
| acknowledged | Host 回复的审批身份、决定 ID、原参数摘要及决定状态已核对 | HTTP 已发送、平台业务成功 |
| unconfirmed 或只有 requested | 尚无可验证的确认回执 | 请求未发送、用户拒绝、可以自动重试 |
| `_meta.admissionConsumed` | 此次许可是否已消费 | 外部平台是否执行成功 |
| 原生 Item 状态与结果 | Runtime 所观察的本次工具调用状态和返回内容 | 任意业务 JSON 字段之外的额外业务结论 |

离线时局部审计事实仍可读，remoteIssue 禁用实时决定操作。新查询字段遇到旧 Native
的 invalid_request 时，仅只读查询退回原请求形状；审批、提交没有此重试路径。旧 Host
HTTP reader 未显式选择 source 时，保留对其无法显示的独立 JSON 的截断提示。

## 已执行验证

- Contracts：23 项定向 Node 测试通过；Host Go SDK 测试通过，v2 SDK 编译通过。
  相对实施前 HEAD `2592f5d5b07fcd92de10d25c4dcf73bd1ce03cb5` 的两个 Host wire schema
  定向结构检查通过；旧响应 reader／旧请求兼容样本及新只读查询模式通过。
- Host：7 项新增 P2 顶层测试及相关 P1／旧投影回归通过，包含 race；go vet 通过。
  覆盖纯 JSON、不同 JSON、业务错误、原始内容下标、合法哈希工具名、限长、普通脱敏、
  缓存热读不重读 thread、读期间通知、迟到 started、淘汰／失效、重复关联不会复活，
  Runtime 未就绪时不把缓存充当实时状态。
- Native：1 项新增真实临时 SQLCipher 测试及 5 项原观察测试通过。实际完成 46→47、
  意图／确认／未确认记录、重复事实保留、正常关闭重开、原 outbox 计数／尝试次数保持、
  scope／轮次隔离、会话删除级联和 foreign_key_check。没有操作日常数据库。
- 前端：38 项 client／组件／composable 测试通过；受影响文件 ESLint、vue-tsc 通过。
  覆盖离线只读事实、不从历史批准、相同未确认决定不重发、不同调用仍需新决定、首次失败
  恢复、空闲停轮询、轻量查询不清空工具、通知合并及导航后的迟到响应。
- canonical 同步检查通过；完整固定开发客户端只读构建检查通过，核对 **656 个 Host
  输入**。原 `native-skill-build-candidate.mjs --freeze` 仅刷新 host_sources；Runtime、
  资源、release 和 baseline 身份不变。各仓 diff 检查通过。

严格 Clippy **未通过**：现有 `database.rs` 的 nonminimal_bool 与
`document_preview_native.rs` 的 cmp_owned 被 `-D warnings` 提升为错误。两处表达式已
逐行核对与 HEAD 相同，本轮未修改或屏蔽；没有宣称全仓静态检查绿色。
没有执行全量测试、恶意资源／攻击注入、权限破坏、强杀、真实供应商、付费模型或 GUI
业务验收；未重启服务、提交或推送。测试进程仅使用普通退出和临时存储。

## 独立复审与回滚

实现后的复审单独核对了执行与显示边界。逐次批准、owner＋native 双条件和单次 HTTP
许可没有改动；所有新增字段与快照只读。读期间通知采用版本检查，淘汰／失效也阻止旧
快照重新写回；关联冲突在返回视图中过滤，内部保留原始已验证事实，重复通知不能恢复
冲突链接。不存在审批进行中猜测 Item ID、依据文本猜测 callRef 或从历史恢复权限。

SQL 47 在当前 Kimi candidate **首次记录新决定前**按 canonical migration 写入，
本轮日常库尚未迁移。回滚不能直接启用最多只读 46 的旧客户端；保留 migration 47
与事实 reader，可撤销决定写入接线或关闭连接器 writer，并用标准构建生成匹配版本。
保留所有既有数据与原生回执，不降 user_version、不删除事实或重放未知操作。Legacy
profile 保持原存储行为，不启用该事实 writer。

既有原生 v6 历史格式不变；市场 UI 沿用最近 128 轮索引，每次最多返回 128 条决定事实，
超出时有截断标记。升级前缺失的无回包决定不会被推测或补写。无 MCP 回包仍无可绑定的
原生 Item，审批进行中的 Item ID 关联仍是上游缺口；本次解决的是其决定证据保留，
不会把它宣传为已经获得执行结果。实际激活、GUI 和供应商业务验收待用户后续重启后进行。

工作区在实施前完整记录并备份了既有 dirty/untracked 文件。原启动与分组件构建改动、
Runtime 来源工作、P1 审批配置／结果关联和 worker 实现均保留；本轮在相关文件上增量
修改，所有仓库 HEAD 未变化，yijie-codex 工作树仍干净。

## 后续落地复审更正

本记录的测试是当时的分层证据；随后沿真实 HTTP 接线复审发现 source 参数被旧校验
拒绝、事件读取时序与决定历史窗口等遗漏。修复和最终验证见
[三个 P2 落地复审与修复](2026-11-15-p2-implementation-reaudit.md)。
当前本地 Host 候选为 v1 0.6.1／v2 0.8.1，仍未重启激活，不以本历史记录替代最新结果。
