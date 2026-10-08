# FEAT-157 产品执行链与 Tushare 验证

2026-10-07，承接 [09 Broker 控制实现](09-broker-control-implementation.md)。用户本轮明确继续执行推荐顺序，并把真实服务逐项验证缩小为 **Tushare 一项**；51 项目录与通用接入目标仍保留。随后用户明确选择：本轮非空连接器选集只支持「请求批准」。普通聊天的三种权限模式保持原有行为。

## 执行顺序

1. 补齐 Native → Host 的可信投递，接通实际 Runtime 的新会话和续轮，复用已有消息、附件、模型及 outbox。
2. 接入独立的连接器审批、工具结果和前端选集。非空选集在 auto/full 模式提示用户手动切换，不隐式改变权限。
3. 接入单一 Host-owned Rust worker 的 OAuth/Keyring，使用 Tushare 进行实际验证。先完成授权与 initialize/tools/list，读取实际 schema 后确定只读工具。其他 50 项本轮不逐项实际验证，不据此声称其真实调用已通过。

Contract impact 仍取整个需求的最高风险 **breaking**。新增 market-host/1、market-provider/1；未发布 Broker 本地候选升级 0.2.0，使 externalCallsEnabled 如实表示供应商网络装配能力。旧 management/selection、旧普通聊天与 Sorftime 的含义保持。全部是源摘要固定的本地候选，尚无发布 pin、提交、推送或生产启用。

## 产品边界

Native 的现有 SQLCipher 保存安装意图、不可变选集、原消息/附件引用及投递状态，不保存平台 token、活动 grant 或授权 URL。SQL32 增加接受时的权限版本、Native process epoch、权限模式与独立投递状态。SQL31 旧记录默认权限版本 0，仍可读，但不补授执行权。OAuth 操作的后续迁移单独向前扩展。

Native 通过自己创建的 Host stdin/stdout 独占 JSONL 管道完成 hello、注册完整提交意图、撤销与审批决定。HTTP 只提交 opaque grantRef 和原 turnOperationId，不能修改正文、附件、模型、目录或选集，也不能批准工具调用。父管道失效即正常 EOF；不使用新的监听器、JWT 或共享明文凭据。

Host 从 SQL32 的授权版本、当前 Native 权限租期和安装 generation 接收权威。新轮完整意图只注册一次；原 accepted 先查事实，pending/uncertain 只沿原操作查询，不自动创建新操作。Native 首轮本地接受不等于模型接受，只有 Host 返回实际 Thread/Turn 后才原子绑定并进入原有观察链。首次 Host 绑定前失败的本地会话不能冒充已建立会话续发；新的重试需新对话。权限变化或退出先失效父管道，正常等待退出，未退出保留所有权/STOP_PENDING。

同一个 Host 直接拥有一个 Rust worker，同时承接 OAuth 与数据 Gateway。OAuth 不依赖模型就绪；缺模型配置时可以显式 provider-only 启动，不能造 Runtime generation。实际聊天仍需真实 Runtime 握手、模型配置、合格工具和本轮权限。正常关闭后才切换完整模式，不创建第二个凭据进程。

Tushare 采用已发现的 OAuth base URL。OAuth 使用官方 rmcp AuthorizationManager/AuthorizationSession；取消和凭据提交由同一个 worker 生命周期约束，存取复用 Codex Keyring 接口。固定、独立的 library home 防止读取用户原有 Codex 凭据。没有 File/Auto secret fallback，不要求把 token 粘贴到聊天或 renderer。

## 验证记录与边界

实现与验证仍在进行中；本记录不宣布 D4 完成。当前产品执行与管理代码已装配；最新 daily profile 的代码检查已完成，真实应用内的启用与业务查询结果按下方时间顺序记录。

- Contracts 新 Host/Provider 专项 14 项及 Broker JS 7 项通过；源生成、Go/Rust/TS/AJV 和 7 路消费同步通过。见 [Contracts 验证](../../../../yijie-contracts/docs/market-host-validation-2026-10-07.md)。
- Native 最终连接器相关 28 项普通测试通过，包括 SQL30/31/33、scope、安装、OAuth 操作、首轮实际绑定、未知操作原号恢复和 ask-only 模式；Clippy（含 tests）通过。前端 client/composable/审批组件/管理轮询合计 23 项最终复跑通过，另提交 store 两项通过；TypeScript、目标 ESLint、构建通过。
- 截至首次 UI 授权尝试前，Tushare 只执行过五次不带凭据的公开 metadata GET。2026-10-08 已从标准应用包点击一次授权，结果见下；公开发现和合成 OAuth 测试不是真实账号验收。
- 未运行用户禁止的强杀/故障注入、二进制替换、破坏权限或攻击 fixture。既有依赖这些做法的验收不计通过，采用正常退出、正常取消和普通本地交互验证。
- 固定 Codex Runtime 不修改，不继承历史付费模型调用预算；真实登录交互、金融查询和模型调用结果将分别记录，不能用合成结果替代。

## 本轮审计修正

- Native 新提交受理后显式唤起原 Coordinator；独立 market dispatcher 保留旧 outbox 的执行隔离。
- 原操作回执查询改为 Host liveness、nonce 和 bearer 的只读路径，不要求模型 Runtime 就绪，也不依赖可授予新权力的管道。
- 安装变更与最终选集读取、grant 注册、发送使用同一个 Native 异步准入锁，消除先撤销、后注册旧选集的并发窗口。全局权限撤回仍同步退休管道，不等待此锁。
- 管理快照按当前 revision/generation/cref 投影后台操作，保留授权非秘密事实；历史连接状态不能复活为 effectiveEnabled。可见管理页查询原操作，串行、退避且最多 120 次/5 分钟；离页、隐藏、撤权停止。
- Host 私管道独立读取 EOF，即使在途方法阻塞也先撤准入，再正常等待 dispatcher/reader；worker OAuth 回调超时保留 JoinHandle，后续继续正常清理，不丢失所有权。
- Go consumer 重写 import 路径后再由同源 sync 脚本 gofmt，未手改生成 DTO。

Host 定向产品测试、普通模型/权限/Sorftime 回归、source check 和 lint 通过，详见 [产品记录](../../../../yijie-agent-host/docs/market-product-integration.md) 与 [证据](../../../../yijie-agent-host/docs/market-product-verification.json)。本轮与历史累计 31 个 owner 验证 child 正常退出，不能换算成 31 次真实供应商调用。

## Canonical 启动观察

两次启动尝试因 Host 本地源快照漂移被门禁正常拒绝，没有启动应用。完成上述源审查和校验后，用既有 canonical freeze 脚本记录新的 `local_worktree_candidate / release=false` 摘要，再启动隔离开发实例。固定 Runtime 未改。

随后 Native、Host 和产品 worker `f52d2f51109b6ce7779866b034cd0dbb8567f8683700453e98ca1b7164752e5e` 已实际运行；本地 18087 的 healthz/readyz 都返回 200，nonce一致、runtime_state=ready。该观察证明启动链，不证明一次真实工具调用或完整 UI 验收。

当前 UI 自动化不能附着未打包开发进程。已请求用户在开发窗口正常 ⌘Q 退出，准备通过标准应用包继续，未使用强杀或进程替换。Tushare DCR、授权 token、Keyring、工具 schema 和金融查询仍未真实执行；既有其他应用的 Tushare 登录页不作为本产品授权事实。

2026-10-08 继续：用户已正常退出首个未打包实例，CLI exit 0，Host/worker及占用端口均已消失。随后标准应用包成功构建并启动，实际界面显示六类共51项；Tushare本机安装成功，未自动授权或启用。真实UI发现旧availability门禁误藏授权按钮，已通过源新增可选authorizationAvailable（缺省false），Native仅为已装配的Tushare授权adapter返回true，前端据此显示独立“授权连接”。工具qualification与execution仍关闭；新增UI回归通过。

本次授权成功后会在同一个worker操作中做只读initialize/tools/list并记录安全schema摘要，避免用户还需隐式Enable才能验证连接；不会调用金融工具、不会自动启用、不会延长原期限。元仓50项测试、lint和Feature Package结构/已声明claims通过；两条普通多模态附件回归通过。

首次标准包授权尝试：使用 worker `1bcaa666c50fa4071e6e0a54f1d5aacc6eee162b4a3441bfac024334cab7ad06`，从详情点击一次“授权连接”后先显示“操作结果待确认”，随后原操作显示“连接未完成 / 连接器服务暂不可用”。Chrome 未观察到新的 Tushare 授权页；Host/worker 仍存活，readyz 返回 200。当前缺少足以确定失败阶段的安全证据，不能把这次尝试计为 OAuth 成功，也不能继续沿用“DCR 请求数为零”的断言。未进行账号授权、金融工具调用或模型发送。正在修正已关联拒绝被误映射为未知结果，以及完整聊天启动误用 HostLive 提前返回的问题；保留原操作事实，不自动重复授权。

上述修复已完成并交叉审查：完整模型模式复用原有有界循环等待真实 RuntimeReady，仅明确 provider-only 且已完成可信 hello 才以 HostLive 返回，3 条普通 loopback 测试与 Clippy 通过。Native 对已关联控制拒绝保留安全错误分类，只有本次新 INSERT、未观察到供应商状态且明确被拒绝的 begin/probe 才终结；旧 Pending/NULL、Unknown 和 replay 不据后续拒绝补造失败。Worker 新增仅包含固定阶段/事件/失败枚举、HTTP 状态码及时间的诊断；单文件 128 条、单条 512 字节，目录 128 文件/8 MiB，满额停止写入，不影响授权、不删除既有证据。详情相同错误只显示一次，3 个相关组件共 11 项测试通过。

新 worker canonical 构建为 `6d4d37b2c54f5d2503e2c39978647af0d69ddbda0c59f9d999cdc3bf79c044f0`，旧制品保留。当前 UI 工具因用户操作保护两次拒绝发送退出快捷键，已请求用户正常退出仍运行的旧标准包后，再进行重建与下一次有阶段诊断的授权验证；未强杀或覆盖运行中的包。元仓 lint、50 项测试和需求包 claims 校验通过。D4 仍未完成。

用户再次正常退出后，CLI exit 0 且原进程消失。新版标准包首次直接进入可用聊天，默认请求批准，不再需要手动重试；readyz 200。Worker 默认28项/资格35项、Native连接器32项及Clippy通过。实际隔离Host Home由 scheduled candidate 装配为 `~/Library/Application Support/com.yijie.ai/demo-fast-model-candidate-v1/host`，并非启动脚本的初始host-home路径。

新版首个有诊断授权操作已确认：公开资源challenge 401、两份metadata 200、DCR 201、授权URL校验通过；Chrome实际打开应用名“Yijie Tushare”的官方授权页。此前仅看易界“操作结果待确认”而推断未开页并不成立，该文案把已知pending也覆盖成未知，已安排只修正文案投影，不改变授权/恢复链。该操作因等待超过五分钟正常expired并cleanup成功，诊断没有token exchange事件。随后从Native显式重新发起一次新授权，关闭过期页面并保留新官方页，等待用户当场同意账号信息/只读TOKEN访问。未代用户点击同意、未取出或展示凭据；实际账号授权、Keyring保存及MCP工具目录尚待确认。

等待用户授权期间，Pending/Unknown显示修复已完成：已知授权pending显示“正在授权，请在浏览器中完成”，配置pending显示“正在连接”；只有真正unknown或尚无回执才显示“操作结果待确认”。执行、重试、取消及轮询实现未改变，28项定向测试、ESLint、TypeScript与diff检查通过。为保留正在等待的授权回调，当前运行包尚未重建加载这一纯UI修复，待该操作结束后统一验证。

截至 2026-10-08 00:49，后续操作 `d50c205a-6351-418d-9d4b-99ce3fd4c44c` 也已在原 Native 权限期限内 expired 并正常 cleanup（授权窗口取剩余权限期限与五分钟上限的较小值）。两份诊断均证明各一次 DCR 201、没有 token exchange 启动；此前无诊断尝试的计数仍未知。用户尚未确认完成授权，已关闭过期页面，不自动再次注册；等待用户准备好后再从 Native 开启有效页面。当前应用保留运行，纯 UI 文案补丁待后续重建，真实 OAuth token/Keyring/工具目录及业务验证仍未完成。

用户随后准备继续时，实际应用已显示“已授权，工具待验证”。只读核对新增操作 `62a7c0e8-1e5a-436c-a774-808baa0fe783` 的安全诊断，确认 token 响应 200、Keyring commit、initialize、tools/list 和 metadata artifact 均 succeeded；不再重新授权。前一新增操作 `feb252e1-5388-4137-98c9-f316049cd84f` 在 token transport 阶段失败，没有成功响应或本地Keyring提交事实，不据此断言供应商端未执行。未读取或输出原始凭据。

真实目录含 254 个工具，exact `daily` 唯一，原始输入 schema 摘要为 `ec10409543d1ae690de2b5da5893a0e69387cdd5a398f976fb04d187fc632ae1`。下一步使用新的 `tushare-daily-v1` 本地 profile，仅开放归一化的 `tushare_daily`：单个A股代码、单个合法交易日期、最多一行公开日线数据；范围/多标的/额外字段拒绝。`000001.SZ / 20260105` 仅是首个真实验收样本，不写死为产品数据。参数、风险和审批策略先进入Contracts权威源；官方[日线说明](https://tushare.pro/document/2?doc_id=27)作为平台依据，实际MCP schema优先于Python SDK示例。

Probe只证明当前受管连接具有该能力，不等于显式启用或本轮许可。Native必须保留Enable意图，再从同一Host/Native epoch/权限revision、同一安装revision/generation/credentialRef的活动worker取得短期证据。管理快照、选择校验、提交和最终发送共用证据；SQL历史不能直接恢复effectiveEnabled。Host每轮prepare复核已有live binding，不新增重复Probe操作；原accepted回执读取先于新准入，不启动Host或重发。完整业务/模型调用仍未执行，非空选集继续仅支持请求批准，D4仍未完成。

2026-10-08 daily 候选完成：canonical worker SHA 为 `0aacce914f889a822fcc9e3774af273d77eef03b66f1c782309b2d259c371cfa`。Worker 37 项默认测试、44 项资格回归、两类 Clippy、Go race/vet 和真实 status-only child 正常 EOF 通过；Native 35 项连接器回归及 Clippy 通过。Host 专项 9 项 race 与源码同步通过。输出契约要求至多一行、匹配请求的股票/日期，非空行必须含有限收盘价；身份字段空壳和未知结果包装不能冒充成功。审批只许可一次实际 HTTP 工具请求，SDK 连接恢复不能自动重发业务调用。

前端恢复入口已补齐：已有启用意图但当前连接失效时显示“连接待恢复”，可显式重新启用；已有账户授权与当前可执行连接分开显示。相关 29 项前端测试、TypeScript、定向 ESLint 及全量 `pnpm lint` 通过。Native 对原 accepted 操作先读原回执；新提交和最终投递在同一准入锁内使用新鲜权限与活动连接证据。旧标准应用已通过正常 ⌘Q 退出、CLI exit 0，Host/worker 正常消失；准备加载新包读取已保存 Keyring 授权，不重新发起 OAuth。

2026-10-08 02:04，新标准包正常启动，readyz 200、worker 实际路径 SHA 与冻结清单一致。真实 UI 显式 Enable 操作 `d2ed9a82-70da-4484-86cb-b5aa7fd9d74a` 复用已有 Keyring 授权，initialize 38.964 秒、tools/list 343 毫秒、artifact 15 毫秒，共 39.322 秒完成。Probe 路径没有新 OAuth/DCR；Keyring读取、网络、刷新耗时未单独细分，不推测其次数。安全 metadata artifact 的 `dailyPolicyReviewPassed=true` 且输入摘要匹配；artifact 自身仍仅表示元数据证据，不能替代活动 ProviderStatus 与 Native 显式启用。

实际 UI 已验证已安装列表开关为 on、聊天店铺右侧连接器入口可选 Tushare、输入框显示所选标签；“管理连接器→返回对话”保留完整正文与选集。首个单日查询草稿已准备但未发送，当前模型为 Kimi-K3，权限为请求批准。金融工具调用和本轮付费模型轮次均为 0；已请求最多 2 轮文本对话、1 次该公开日线读取的预算，以验证批准/拒绝和结果链，收到明确授权前不发送。启用 Pending 时一处说明仍错误回落为 OAuth 引导，已定位为纯文案投影，不会触发新授权；补丁单独记录加载状态。

2026-10-08 02:09，用户明确回复“授权上述上限，继续验收”：最多 2 轮当前 Kimi-K3 文本对话、1 次 `000001.SZ / 20260105` 的 Tushare 只读查询，使用现有额度，不充值、不订阅，失败不自动重发；授权包含一次批准与一次拒绝流程验证。02:09:26 从已选连接器的真实 UI 发送第 1 轮，新会话 `01a1178e-53f2-7db2-9ed1-6f2bd58c8ec9`，等待实际审批/结果。一次用户提交不等于一次底层模型 HTTP 请求，预算按用户授权的对话轮次计，底层请求次数没有独立观测则不推断。

首轮真实 Native 审批卡片展示正确的 Tushare、股票、日期与只读范围，点击“批准本次”后返回 `Connector call did not produce a verified result. No automatic retry was made.`；28 秒结束，未获得可信行情结果。该版 Gateway 把准入失败、传输失败和结果校验失败合并，现有诊断不足以证明具体阶段及实际业务 HTTP 次数。模型回答中的“已执行一次”和“无数据”不能作为供应商执行或空结果证据；本次真实业务验收不计通过，一次读取额度保守视为已用完，不自动重试。

02:11:21 在同会话发送第 2 轮，仅验证相同参数的拒绝审批；Native 卡片点击“拒绝”后显示“已拒绝”，32 秒结束。模型仍收到同一通用错误，无法判断拒绝与调用失败，是本轮发现的错误语义缺陷，需修复确定性拒绝的安全结果映射。两轮预算均已用完，后续只允许本地诊断/修复；未再发起金融或模型请求。尝试离开重开会话时界面工具两次报告用户正在操作窗口，已停止 UI 操作，历史重开暂不计通过。

Pending Enable 说明补丁已在源码完成，回归 10/10、ESLint、TypeScript 与 diff 检查通过；当前运行包尚未加载这条纯文案修正。
