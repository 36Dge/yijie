# ADR-0021: 本地连接器产品状态、凭据和执行职责

## 状态

Accepted — 限 FEAT-157 的 local + demo_fast 实施边界。

2026-10-07，Owner 在需求包、产品设计和架构候选形成后要求“根据需求包与设计包，开始实现feat-157需求，逐步实现”。本记录落实设计包推荐的 B 方案，不把该指令解释为技术资格、真实账户授权、付费调用、D4、公开发布或 Git 提交批准。

## 日期与负责人

2026-10-07；段成威。

## 背景

51 项市场目录需要区分安装、全局启用与当前轮选择。当前项目已有 Native SQLCipher、管理权限上下文、幂等操作、Codex MCP client 和原生 Thread/Turn/Item。另一个应用的服务清单只提供供应商候选资料，其宿主地址、授权方式和运行命令不能直接成为易界执行配置。

## 决策

1. 补充 ADR-0013 的本地产品状态范围：沿用 Desktop Rust/Tauri 持有的 SQLCipher，保存当前固定 identity/tenant 下的安装、非秘密配置引用、目录版本、用户启用意图、安装 revision/generation、操作回执和卸载 tombstone。安装使用前向 migration 30；后续审计实施的 migration 31 保存不可变提交选集/回执及create/turn操作别名。不改写历史 migration，不建立第二份 Connectors 安装业务数据库。
2. 延续 ADR-0005、ADR-0007：第三方凭据归 Connectors。Desktop renderer、Host 与 Runtime 不持有平台密钥。Native 产品库只存不透明 credential reference；OAuth/原生秘密输入与 Keyring 尚须完成对应实现和资格，不能因有该引用就声称已安全保存凭据。
3. Connectors 通过固定来源的 Codex 库窄 worker 复用 MCP HTTP/OAuth 等协议。来源、构建摘要和正常生命周期单独记录；不能替换用户 Codex 二进制，不能以同名假程序或强杀验证生命周期。
4. Codex 继续决定原生 Thread/Turn/Item 和工具执行事实。Host 只适配会话、版本化选集、工具审批和能力绑定，bbolt 仍不是安装或审批业务主状态。Gateway 在真实调用处校验选择、generation、真实 turn 和批准；metadata 只作关联线索，不是授权。
5. 原生管理面使用独立 Contracts family、生成 DTO 和严格输入验证。沿用 ADR-0018 固定本地 authority，按 read/manage/credentials.manage/use 分权限。UI 不能自选身份、提供任意端点或直接调用 Runtime。public/production 路径不激活。
6. 新能力默认关闭，仅精确 local + demo_fast + market feature flag 可用。目录的 51 项均可呈现和进行非秘密安装管理；服务未通过资格时不可有效启用、选择执行或显示“已连通”。空选集不授予市场工具能力。正常关闭、撤权和回执未确认的状态必须如实保留。
7. 用同一操作编号查询和重放原意图；不能因页面重载、未知回执或恢复会话而自动重复外部业务。卸载保留 generation 隔离和必要回执，历史显示副本不包含可执行能力。

## 尚未由本 ADR 决定的实现细节

Host/Gateway 控制面 carrier、精确审批关联、正常退出的 stdio 桥接、第三方 OAuth 注册与回调、库内重试对写调用的约束，仍以固定源码和无副作用资格为先，随后进入 Contracts 源。缺少证据时保持该路径关闭，不填造上游字段或服务资格。

## 备选方案与影响

2026-10-07 后续审计将产品进程拓扑收敛为 Host 直接持有 Connectors Rust worker，以独占 JSONL 管道传控制消息；后续 Broker 模式复用官方 rmcp server 和固定 Codex client，不增加 Go 纯转发子进程。专属环境能力的本地隔离机制已经资格化，具体产品控制源、TTL/撤权及审批接线仍需实施。该选择保持本 ADR 的仓库/凭据职责，不授予真实平台访问或 Runtime 核心变更。

- 将平台凭据直接写 Runtime config：与 ADR-0005 不符，也不能保证当前轮选择和撤权，未采用。
- 自建完整 MCP client：重复已有 Codex 能力，未采用。
- 另建安装数据库：造成产品状态双写和恢复歧义，未采用。

本地候选允许使用实际源码摘要和 sibling 开发来源锁；它不是不可变发行来源。发布前仍需固定来源与方向兼容验证。回退关闭 writer 和新能力、正常撤销和清理；保留前向 reader、已有记录和凭据，不降库、不清空 Keychain。

## 验证与关联

实施、测试和未完成项统一记录于 [FEAT-157 实施记录](../features/FEAT-157-desktop-market-connectors/07-implementation-progress.md)。本 ADR 不将合成协议或组件测试换算成真实 MCP/模型验收。

- [架构与契约设计](../features/FEAT-157-desktop-market-connectors/04-architecture-and-contracts.md)
- [服务目录与接入条件](../features/FEAT-157-desktop-market-connectors/05-service-catalog.md)

## 2026-10-08 通用工具准入补充（Owner 已确认）

Owner明确采用[通用发现＋逐次审批](../features/FEAT-157-desktop-market-connectors/15-generic-provider-execution-plan.md)。仅在固定51服务、真实已连接、已冻结且可完整本地校验schema、实际选集/身份/参数均匹配时，通用工具可进入审批；没有独立只读策略按高风险write展示完整参数并要求单次批准。明确破坏性且无专用影响策略的工具仍拒绝。未知身份/格式/无法完整审阅或含凭据的参数仍拒绝；OAuth授权不等于执行批准。批准后一次许可，不自动重试，不扩大自动/完全访问模式。此决策取代本需求中“所有非预置工具一律拒绝”的限制，不改变平台token、Native权限、Runtime、真实调用预算或强杀禁令。其余50项只做代码审计/本地测试，真实验收仅Tushare。


2026-10-08实施细化：Owner移除淘宝闪购，目录50项。Google地图/日历按官方现有远程MCP适配复用HTTP/Keyring；日历预注册Web OAuth配置留Connectors，默认只读，修改scope显式选择。参考本地包不再是产品依赖，无明文token/Node子进程。仅Tushare真实验收，其他49项代码审计及正常本地协议测试，详见FEAT-157/17。该实现选择承接Owner要求按易界特征调整来源应用方案，不改变账户同意、逐次审批、成本或发布授权。

2026-10-08最新Owner范围：移除豆蔻医生后共49项，淘宝闪购继续排除。Agentic Engine根据新提供的官方文档恢复范围，固定HTTP参考地址、显式导出Header配置，公开资料未给出该端点确切Header，因此不推断Bearer或API_TOKEN映射。此后其他48项只做代码审计/普通本地测试，真实验收仅Tushare；不因缺少全供应商实连而阻塞。

2026-10-08授权恢复补缺：通过新增Native管理命令重开原操作当前等待用户的授权/凭据页；operation ID及回执revision精确匹配，始终校验credentials.manage，不向Renderer返回URL，不重启OAuth/DCR/Probe。只读查询即使看到待授权状态也不能代替凭据管理权限打开浏览器。属于既定授权流程的恢复入口，不增加第三方范围或修改Runtime。
