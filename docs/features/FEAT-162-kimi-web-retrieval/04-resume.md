# FEAT-162 暂停与恢复记录

> 2026-10-28最新结果以[20号报告](20-client-e2e-results.md)为准。K3.1源码整合、新构建和零费用验证完成；真实客户端端到端FAIL。累计模型4次（1成功、3次response.failed/usage未知）、Search0、Fetch0；最新Kimi错误码rate_limit_exceeded并匹配服务繁忙。保守总预占¥42.710457，非实际账单；¥43内已不足下一次完整模型预占。19项离线检查、57项元仓测试通过；失败历史正常重开0新增HTTP。所有本任务进程已正常退出，台账全部halted/unarmed并保留。新增授权累计7次不是失败后自动重试许可，继续收费前必须重新明确服务和费用条件。日常构建、原数据、模型迁移及Codex内核保持。

以下为历史记录。

## 已完成

- 先落完整实施方案并通过 D0，再执行代码变更，初始证据保存在 `evidence/plan-before-implementation.json`。
- 目录上限按授权从 60 改为 62，实际 61 项；新增一个 `kimi-web` 连接器，两个工具 `kimi_web_search` 和 `kimi_web_fetch`。Search 返回标题/URL/摘要，Fetch 返回 URL/标题/Markdown 正文。
- Connectors 复用既有 Keyring、Broker/Gateway、选择、租约、逐次审批与 MCP 链路。没有重建 Agent 循环、修改 Codex 内核、实现无头浏览器或原始 HTML。
- Contracts 源契约、生成 reader 和工具 DTO、Connectors backend、Desktop 市场与图标均已完成。单轮选择上限仍为 58。
- 定向测试通过：Connectors 13 项、Desktop 前端 47 项与 Native 11 项、Contracts JS/Go/Rust 定向检查、Host 四包普通 allowlist race、真实 worker 子进程正常 lifecycle/EOF 四项、元仓 50 项；详见 `02-verification.md`。
- 底层 HTTP 默认重试 P1 修复并独立复审关闭，锁内同版 reqwest 显式无重试/无重定向；全部 876 个外部依赖记录不变。
- 因市场契约来源传递导致专家资源 pin 失效，已走 canonical producer 来源刷新，全部 75 个归档内容/元信息及授权审查保持一致；6 项普通测试和独立复审通过。没有手改哈希绕过检查。
- 最终标准 App 编译、打包和来源回执通过；真实业务和 UI 验收尚未通过。

## 暂停时构建与进程（历史）

- 标准入口：`YIJIE_FEAT156_LOCAL_CANDIDATE=true pnpm tauri:demo-fast:app`，目录为 `yijie-desktop`。
- App：`yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI.app`；二进制 SHA256 `0480c81eac5f833975ee70d301cf5cf66d0eea74ee12d26b26493fbb0753ff2a`。
- 最终来源回执：`yijie-desktop/.local/demo-fast/packaged-launch-receipt.json`，SHA256 `5569f56de59cde96626319ab7b53a4f9ce51473f4abf9b90eb25145d75e62a08`。
- Worker SHA256 `1f35e4ab2d392dab59383f2951c495117f001ededfa97150b6f78c5bf0a10745`；Host SHA256 `14a1f0304dd05bd7377480583db0f91712283e076806fdefcdd96298e0a67b45`。
- Runtime HEAD `9154f27d0cdb526a5f5ba0913fe3e2448014b4a1`，仓库干净；固定 Runtime 二进制 SHA256 `9766d7e10d25327f0595964a19ad67e1e1c1db0c22e5a65f9af66b547ab316c6`。原生搜索保留。
- 暂停前最后一次进程观察：App PID 64599 运行，未发现 Host/market worker/artifact/Runtime 子进程。标准启动终端 session 38315 随 App 保留，没有强杀或后台测试。
- 另有此前 formatter PID 10952 等待 stdin EOF，标记 **STOP_PENDING**；没有安全的原会话 EOF 通路，未强杀。新 formatter 正规临时文件路径已通过检查。恢复后也不得强杀。

## 暂停时阻塞（恢复后已修复）

Mac 最初锁屏，用户回复后 CUA 已能读取界面。App 首页显示“本地服务尚未就绪”“任务记录暂不可用”；点击一次正常“重试启动”后仍未就绪。随后连接器页面显示“连接器服务暂不可用 / 本机运行环境尚未就绪，请重新读取后继续”。

因此最终构建和进程启动成功，**本地服务就绪验收失败**。尚未看到市场目录，未安装 Kimi，未打开凭据配置页，未填写或保存密钥。根因尚未定位，不应归因于锁屏或宣称新连接器真实可用。

Host integration 子代理已确认停止，无进行中的命令，本轮未修改文件、启动进程或读取密钥。其在暂停前已取得一项遗漏候选：Host `yijie-agent-host/internal/skills/experts_candidate.go:26` 仍固定旧专家 manifest 摘要 `033689b0…`，而正规刷新后的 Desktop 专家资源 manifest 摘要为 `64721b4b…`。`VerifyExpertCandidate()` 会按旧摘要验证，可能导致 Host 启动后立即退出；**尚未取得本次运行错误确认因果**，不能称根因已定位。正常产品入口将 Host stderr 设为 null，没有现成标准 stderr 日志。恢复后先按 Contract First 原流程核对这一遗漏；暂停期间不修复、不继续诊断。

## 未通过/未运行

- 真实 Kimi `/models`、Search、Fetch、模型回合均为 0；没有本任务付费测试额度，没有复制/读取模型密钥作为连接器密钥。
- 市场安装、配置取消、选集审批拒绝、两工具真实结果、同构建重开历史尚未完成；AC-003/004/005/007 与整体 D4 保持未通过。
- 7 个全量 breaking 基线中 3 通过、4 因既有 scheduled-plan-draft 远程引用 EOF 退出 102；专家补充 34 通过、1 旧 schema 基线断言失败。原日志保留，不削弱检查。
- 首次 App 构建时因审查修复改变源码而被来源回执拒绝；最终重新构建已正常生成回执。
- 不运行强杀、攻击注入、恶意 fixture、可执行替换或权限破坏测试，详见用户长期安全约束和验证记录。

## 暂停时拟定的恢复顺序（本轮1至4已完成）

1. 先确认当前工作区和 App 状态是否变化；不要覆盖其他聊天已有修改。检查已有构建回执与来源，不重做已完成审计。
2. 从 Native 启动门禁查明本地服务未就绪原因，使用安全内容有限的诊断；不输出凭据，不猜测失败原因，不以弱化校验或改 pin 绕过。
3. 修复后按需 canonical 重构，使用正常 Cmd-Q/EOF 退出；无法安全退出则报告，不强杀。
4. 正常市场目录、Kimi 安装、首次无密钥配置取消与不可选状态验收。已有凭据的配置入口会执行 `/models`，不能视为零网络检查。
5. 本地实现可审查后，才向用户申请真实账户与收费验证额度并由用户在安全页面配置 Keyring。拟定 Search/Fetch 各一次、一次拒绝审批、最多两个模型回合及同构建正常重开；费用与 HTTP 额度须明确，不借用旧 Feature 授权。
6. 更新真实证据和 Must AC；只有全部真实验收到齐才能标 D4 PASS。

## 主要证据

`00-feature-brief.md`、`01-delivery-log.md`、`02-verification.md`、`feature.yaml` 以及 `evidence/` 中的 build、focused checks、independent review、provenance refresh、workspace-before 记录。当前产物均为本地候选 `release: false`。

## 当前恢复结果与后续边界

- Host旧manifest pin遗漏已修复：从完整校验后的来源生成`internal/skills/experts_assets.gen.go`，freeze/build强制只读核对；真实Host启动配置测试由FAIL转PASS，独立复审PASS。
- 正常恢复Docker及旧workflow容器后，标准App build和实际服务就绪PASS。恢复使用既有正规入口，原数据及保护副本保留，无强杀/删卷。
- 连接器市场61项、Kimi搜索/图标/详情、新安装、空密钥配置取消、未启用及对话switch禁用均PASS。
- Cmd-Q正常退出及所有App子进程结束PASS；同一构建--reopen回执和实际安装/取消状态保留PASS。亮色1180x760及键盘焦点PASS，窗口恢复1268x780。暗色实机NOT RUN，原因见02-verification。
- 当前App PID82390保持打开于Kimi详情。新安装已保留，未配置密钥、未启用。临时配置浏览器页已关闭。旧formatter在恢复时已不存在，未发送停止信号。
- 最新来源回执SHA256 `643a3ad24ca0ee349109141606c000f77ff144a42ae7435f5ab29f6f544a0bfe`；新App `a3c3996b4f8269ea5a146b56736ca9abbd8a7a08c43b53a0639293d9ac9d1fae`；新Host `566f61125caec1c2a80dc6daf7379d8b8e532dfb1bab45d46758cd15af47b14d`。Runtime/worker未变。
- 当前真实models/Search/Fetch及模型回合均0。用户明确要求暂不做收费API；不要继续真实调用、不要打开配置并提交密钥，除非未来用户明确要求。原Must真实服务项及D4继续NOT RUN；本轮恢复请求已完成。
- 最新证据：`evidence/app-resume-ui.json`、`evidence/host-expert-authority-sync.json`、`evidence/local-workflow-recovery.json`、`evidence/kimi-ui-no-provider-call.json`和7张UI截图。旧失败证据不覆盖，历史记录已标注后继报告。

## 模型密钥复用与共享窗口交接

更新：2026-10-24T12:09:32.875986+08:00。**后续直接可用流程正在实施；此前交接记录仅代表上一构建**。

- 已先给出05完整调整方案，再完成Contracts、Host、worker、Native/UI及canonical来源生成同步。配置复用Host已加载的Kimi模型Key，不再单独填写/保存；配置仅本地绑定，未启用、未联网验证。
- 真实App首次绑定成功。修正静态目录提示覆盖成功状态的问题后，最终构建及同构建重开验收PASS；1180×760、键盘和对话选用禁用均PASS。界面和诊断证据见06报告及model-key-reuse-ui.json。
- 当前App已正常Cmd-Q退出，所有本轮App/Host/market worker进程结束，窗口已释放；本地workflow既有容器保持健康。安装/本地绑定已保留，Kimi未启用。
- 专家资源canonical来源已刷新，75项metadata/archive不变；Host权威摘要已同步，严格来源检查和freeze通过，没有手改hash绕门禁。
- 保留FEAT-163的runtime_permissions.go、session_protocol.go、chat_models.go及前端变更；未使用其额度、独立meter或真实验收。本记录不表示FEAT-163第9/10回合或其他未完成验收已通过。
- 本任务真实models/Search/Fetch/模型回合全部0，D4继续NOT RUN；未运行无头浏览器，原生搜索/Agent循环/Codex内核未改。后续本任务真实调用须另有用户明确指令；不要自动点击“检查连接并启用”。
- 最终来源回执 `796a510907014b0e3dcf394fe75387b23892cf5d96ba3b2362d50968dc312102`；App `0d79ee061c1a284db20e274c66a3aaa8b5f23f194a8cfabf24ffbb5085cb0cc5`；Host `be5a7c27407520bec1975c66ccc4cb0ccb95c36a90c828f17baa8371b97603d8`；worker `7d7842ad9cae62f2913e381e7f4a115e8039e88180656b6c0c788350518a36f8`。完整回执保存在`evidence/model-key-reuse-packaged-receipt.json`，共享工作区状态见`evidence/model-key-reuse-workspace.json`。


## 自动复用凭据：用户再次暂停

暂停时间：2026-10-24 17:58（Asia/Shanghai）。用户最新选择：**自动复用客户端已有的 Kimi 模型凭据，不再配置或启用连接器**。真实收费API仍禁止。先审计并落盘07/08，再做本轮实现；不是共享服务端Key或把个人Key打入安装包。

已完成：

- Native按现有权限建立内置Kimi默认安装/desired意图，复用前端已有Enable恢复链及Host/worker；无单独Configure/Enable操作。明确停用/卸载保持，重开准备当前owner；无新Agent循环或Codex内核改动。
- Worker Probe仅本地准备canonical两个工具及当前凭据快照，已移除/models请求路径。ready只表示可接受受审调用，不表示真实供应商鉴权、余额或检索已验证。匿名FD正常关闭，Kimi Forget不读取/删除另一份Keyring或模型Key。
- Contracts41项+lint、前端159项、Native默认3项+连接器11项、Kimi worker14项、scoped ESLint/Rust fmt/Clippy、标准前端及worker构建通过。Host真实canonical worker直接Probe/Legacy Auth各有无普通内存来源4种情况通过，正常EOF退出；未请求供应商。
- 75项专家资源内容/授权未变，canonical来源刷新、Host authority同步、真实Host manifest检查及freeze通过。元仓50项、lint/shell与7仓diff检查通过；开发过程中旧文案/目录revision断言及测试类型不匹配已修复，结果见direct-use-checks.json。
- 第一次标准App启动在Docker检查处失败，未生成新App：Docker Desktop当时未运行。正常打开Docker后原6个依赖容器均记录退出255，按canonical recovery流程留存原数据保护副本、只读核对并正常停止，恢复ID `7cb2c072-e21e-47d4-8489-325751756d7d`，日志确认RECOVERY_COMPLETE。没有强杀、删卷、改权限或绕过门禁。

暂停时状态：

- **新App尚未完成构建/启动/UI验收**；没有发起第二次App构建。现存packaged App和旧回执仍是06的“手动绑定、未启用”版本，不能当作当前新流程结果。
- 没有本轮App/Host/market worker运行，所有命令会话均已结束。Docker Desktop保留运行；6个主要依赖容器及2个历史migration容器均正常Exited(0)，命名卷和保护副本保留。
- 新worker SHA256：`ebf7c834c95f4614365981aa7b99d04dcff37eb4d709cf4f84d0b04a8e073404`。Runtime HEAD仍`9154f27d0cdb526a5f5ba0913fe3e2448014b4a1`且工作区干净。
- 新代码、跨仓来源及文档未提交/推送/发布。FEAT-163已有改动保留，不借用其额度或宣称其验收完成。当前共享构建窗口尚未完成最终交接。
- /models、Search、Fetch和模型回合本任务真实调用均0，D4仍NOT RUN；禁止的故障/攻击测试未执行。

仅在用户明确恢复后继续：

1. 先读取本记录、07/08和 `evidence/direct-use-paused-state.json`，核对共享工作区与进程是否变化，不覆盖其他聊天修改。
2. 已有依赖恢复完成，使用Desktop标准入口 `YIJIE_FEAT156_LOCAL_CANDIDATE=true pnpm tauri:demo-fast:app`；下一日志使用 `direct-use-app-build-02.log`，保留第一份失败日志。
3. 验证已有模型凭据下Kimi自动“可使用”、无配置/启用步骤、任务选择开关可用；不发送模型任务，不执行收费请求。完成最小窗口/键盘、正常Cmd-Q及同构建--reopen。
4. 保存当前构建回执、准备诊断、UI证据和09验证报告，更新feature.yaml当前结果；完成后才标记共享源码/产物稳定和窗口可交接。真实Search/Fetch/模型/D4继续NOT RUN，除非另获用户明确授权。

证据：`evidence/direct-use-paused-state.json`（各仓HEAD/完整status、来源hash、进程、容器、下一步）、`evidence/direct-use-checks.json`、`evidence/direct-use-app-build.log`、`evidence/direct-use-workflow-recovery.log`。暂停后未继续实施或验收，仅落盘本检查点。


## 自动准备最终完成与交接

2026-10-24 21:24（Asia/Shanghai）。当前用户要求已按07/08完成：自动复用客户端已有Kimi模型凭据，无需单独安装、配置或启用连接器。正常App自动显示“可使用”，任务开关可选；已修正旧通用说明，最终构建及同构建重开PASS。准备全程无Kimi HTTP，真实模型/Search/Fetch均0；详细结果、限制与最终SHA见09和 `evidence/direct-use-ui.json`。

最终来源回执 `b749914b8bbec6341fffb87592c9eecb24ec4e64d597b51cb3df737391a217b1`，App `a6046baf63260743245d566dfa0df4a12afb7fc3772f72c81fa8152823b621ef`，Host `7b093b9a0ce5569f4b78157ae6c2d43193f146f5d19e0628f0627167e2d8a338`，worker `ebf7c834c95f4614365981aa7b99d04dcff37eb4d709cf4f84d0b04a8e073404`。Runtime HEAD/二进制不变且仓库干净。最终正常Cmd-Q，App/Host/worker/artifact子进程均结束；本地workflow六个服务健康保留，数据保护副本未删除。

**共享源码及生成物已稳定、App构建/验收窗口可交接。** 保留FEAT-163改动，不使用或宣称其额度/验收。下次如需展示本构建，先核对工作区/来源，再使用Desktop canonical `YIJIE_FEAT156_LOCAL_CANDIDATE=true pnpm tauri:demo-fast:app --reopen`；若来源变化，走正规重新freeze/build，不覆盖来源检查。实际供应商调用、生产发布及全新机器分发仍须另行授权和验收。当前实现任务无待办，仅保留这些未授权验证项。


## 真实最小验收启动失败，已停止

2026-10-24。用户明确确认10方案（Search1、Fetch1、¥0.02、模型0、先拒绝零HTTP、失败停止）。新增仅测试用的固定MCP驱动经过编译/普通协议解析/vet；正式启动命令因GOSUMDB=off禁止Go1.26.5工具链校验而立即退出1，未进入测试函数，未加载Key或启动worker。

实际Search0、Fetch0、模型0、费用¥0.00；拒绝门禁NOT RUN。按要求停止，没有重试。一次性运行目录已用明确的operator closure标记关闭，不能当作测试运行回执，也不得重用授权。11报告和 `evidence/live-minimal-result.json` 为最终事实。

仅新增Host的opt-in测试源码，生产代码/产品worker/App/Runtime未变；不存在运行中的App/Host/worker。后续须由用户明确要求恢复，先修正本地工具链启动配置；不得自动继续或以剩余额度执行请求。09已有实现验收不受本次启动错误影响，真实接口能力与整体D4仍未验收。


## Go启动已修复，第二轮本地预检失败停止

2026-10-24。用户授权先修复Go启动配置并完成本地预检，再按Search1/Fetch1、预算¥0.02、模型0验收；失败停止、不重试。新增正常校验的固定Go工具链测试启动脚本，以及不读取真实Key、不进行tools/call的预检模式；编译、解析检查、vet及Shell检查通过。

新的预检已进入测试并完成worker本地准备，随后在mcp_initialize阶段失败，正常EOF退出。没有重跑或启动真实验收；真实Key未加载，Search0、Fetch0、模型0、费用0，拒绝门禁NOT RUN。11旧失败记录保留；当前事实见12及live-minimal-round2-result.json。

停止后的静态线索为测试客户端SSE读取器可能未处理rmcp空priming事件，尚未取得握手响应证据，不能称根因确认。无App/Host/worker残留，产品worker和Codex内核未改。后续仅在用户明确指令后处理本地MCP初始化，不能自动使用剩余付费额度。


## Search与Fetch真实最小验收通过

2026-10-24。按用户“查出原因、做修复，目标是验证Search/Fetch”的指令持续完成本地排障：修复测试SSE客户端未处理空priming事件，以及未按现有Codex行为移除progressToken的问题。均为验收驱动修复，生产worker/Host代码/Runtime未变，无凭据泄漏或批准绕过。

无真实Key预检通过后，一次正式验收使用现有Kimi模型Key，先reject/decline确认HTTP0，再Search1（HTTP200，3条标题URL摘要）和Fetch1（HTTP200，751字符Markdown、未截断）均PASS。模型、/models、余额请求均0；无供应商重试。按官方单价合计¥0.02，未读取账户账单。worker正常EOF退出，当前无残留进程。

完整结果见13和 `evidence/live-minimal-round3-result.json`；本轮一次性额度已消费并关闭，不得再次执行。当前Search/Fetch工具功能验证目标已完成；完整模型驱动对话/Native UI审批和历史D4仍不在本轮范围。未提交、推送或发布，其他Feature改动/额度未触碰。

## 客户端真实对话方案待确认

2026-10-24。用户要求下一步先给最小端到端方案，确认后再执行。方案已保存[14](14-client-e2e-acceptance-plan.md)：一个新对话/一条用户消息，现有Kimi Key，模型HTTP最多3次、Search/Fetch各最多1次、总预算申请¥5，失败立即停止且不重试，正常重开检查历史不重新调用。

本轮仅阅读代码/既有证据/公开价格并新增方案，收费请求全部0，没有启动App/meter或修改产品实现。现有meter缺输入token与费用预留门禁，14明确要求确认后先补齐并做零费用检查，不能把提示词、已有请求次数限制或事后usage核算冒充金额上限；门禁不成立则不执行付费请求。14仍为PROPOSED，未取得本轮执行或付费授权，不能继承13或FEAT-163的额度。D4状态不变。

## 2026-10-28复审：当前基线未纳入，待确认继续整合

用户要求完整回顾实现程度、评估K3→K3.1 Pro影响并给继续方案。本轮已核对历史09/13/14、当前七仓、保全commit、generation20261028-02回执及官方API，结果见15和`evidence/k31-current-source-audit-20261028.json`。

历史工具已真实通过，模型驱动对话未验收；当前目录revision9/60项无kimi-web，web-retrieval、worker REST及Host FD3装配未在当前源，保全引用中仍存在。FEAT164第76/80号说明这是选择已审基线、未激活其它WIP的结果；不能说因换模型导致API不兼容。核心REST无model参数，推荐保留当前K3.1/r5，选择性整合原实现、修正Key语义残留、刷新契约和来源，再做新模型对话验收，不从头重写。

仅本轮审计/文档授权，未恢复代码、未启动App、未打开业务数据库、未读取Key值；模型/Search/Fetch全部0。14号旧执行清单已不适用当前基线，5元未确认且输入预算前置仍未实现；后续独立费用验收单待本地整合完成，不转用任何旧额度。FEAT164关闭状态及全部保全/账本保持。

本轮元仓pnpm lint、57项治理测试（0失败/0跳过）、Shell语法、diff空白及新报告本地链接/证据一致性检查通过；只证明文档与治理检查，不算新产品或真实调用验收。仅新增15号和只读审计证据、更新04/14提示，没有提交/推送。

## 2026-10-28整合实施：待本地提交授权才能完成新构建

Owner已授权审计并实施K3.1基线整合、零费用验证和新构建，真实收费仍须先给方案再确认。16号复审先落盘后执行；精确选择性移入Contracts、worker、Host、Native和UI代码，不整包合并保全分支。已完成canonical新worker与拒绝零HTTP预检，原日常App、数据与Runtime未动，未读取真实Key值。详见16号和本轮evidence记录。

关键发现：K3.1使用v2调用面，旧FEAT162 v1同步不能作为最终Host来源。源端已修正market-host/2 0.5.0、生成与46项契约检查通过；v2消费者必须从真实Contracts commit同步。当前Host生成物仍处于待v2覆盖的中间状态，**不可启动App或将其称为已完成K3.1整合**。整体TS与K3.1 feature Native复验、新客户端构建均待这一步。

已向Owner提出一次精确异步确认：仅本次需求相关的Contracts/Connectors/Skills/Host/Desktop/元仓文档按依赖顺序本地提交，不推送、不发布、不收费。原因是AGENTS禁止未明确授权commit，而原同步及primary构建门禁要求精确已提交来源、干净源码。尚未收到答复，不以等待时间视作批准；没有提交、绕过门禁或生成新App。收到授权后按16号续办顺序完成。

当前新增真实模型0、Search0、Fetch0，费用¥0；本地预检正常EOF。17号是新模型收费提案，仍未执行、不借用旧额度。D4继续NOT RUN。

## 2026-10-28本地提交获批：整合与新构建完成

Owner已明确授权本次必要本地提交。按依赖顺序完成Contracts、Skills、Connectors、Host、Desktop本地提交，v2消费者已从准确Contracts commit同步，原中间v1状态已消除，K3.1身份与缺凭据错误完整保留。没有推送、发布或修改Runtime。

新generation `20261028-03`标准prepare-only构建成功；App为`yijie-desktop/.local/builds/primary/20261028-03/target/debug/bundle/macos/易界 AI.app`。App SHA `9c7ebfea56398a0b7a20ba9dbe714f86715fabdfbcf8a5e7e92c74f1e466c9f6`，回执SHA `fea236b9a0067e4ce6b1c47af6c4c0f65bec83efec2c073974ee0666a8588d9c`。具体来源、检查数、真实失败及修正、制品摘要见18号及其3份evidence。

新包worker SHA `f0e5059386fe244bad93c911608b6b2d431951759fb44988ecec1bb90a448065`已重新完成拒绝零HTTP和正常EOF。前端68+2、K3.1 Native调用面4+Kimi选择重开1、Host实际资源及凭据、生成来源19、四组合闭合等通过。旧App119文件、旧Host/worker/adapter/Runtime均与原回执一致；75专家/普通资源内容保持。

本轮新增模型/Search/Fetch/账户API调用均0，费用¥0，没有读取真实Key值、打开用户业务数据库、新建激活批准或启动App。本次用户授权的整合、零费用验证和新构建目标已完成。下一步如继续真实客户端验收，先按17号确认新的模型≤3、Search≤1、Fetch≤1、保守预算≤¥43，并补齐独立计量前置和新构建准确激活条件；不能直接借旧generation批准/旧账本执行，也不能把本地Git授权当付费授权。D4仍NOT RUN。
