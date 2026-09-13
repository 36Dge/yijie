# FEAT-153 分步实施记录

最新追加：用户外出，授权先做不依赖解锁的任务；本轮修复编辑器普通异步/unknown状态，完成API自然301秒会话、packaged构建与两类标准入口正常退出、最终静态部署/重开与凭据产物检查，见[09](09-step5-headless-progress.md)。App、测试栈和Docker现已正常停止，保留数据；4个旧凭据助手仍等待。真实界面资格/5.4/D4继续保持未通过。

最新进度（第5步，2026-09-12）：按用户指定顺序完成5.1环境恢复、5.2最小真实Coze编辑器与Desktop桥实现/构建、静态产物登记及精确服务栈恢复。canonical dev App已启动，但Mac锁屏阻止CUA真实操作，等待手动解锁。5.2闭环/5.3真实会话与packaged/5.4完整页面尚未通过；详细过程和实际失败保留在[08](08-step5-desktop-integration.md)、[构建证据](evidence/step5-editor-build.json)、[运行静态证据](evidence/step5-dev-start-and-static.json)。没有将App进程启动等同于产品验收，没有开始试运行/发布UI。

本轮纠正了不透明revision、消息监听时机、旧画布替换、在途保存与重连、取消打开清理顺序，以及工作流生成入口干扰原Chat提交校验的问题。原Chat `--require-committed` 保持并通过；具体工作流生成迁到独立入口，原锁未刷新。构建依赖按上游精确版本投影，原Rush/lock不变；固定vendor保留旧动态代码能力，CSP禁止执行的边界未放宽。测试/构建初轮失败与修复均在08和专项证据注明。

## 2026-09-12：第 0 步审计 → 第 1 步本地仓库接入

用户要求先认真审计、再分步接入，并建立 FEAT-153。审计先于任何 Coze 仓库改动，按元仓/来源、Coze、Desktop、API/Contracts/Infra 四条线核查。结论和代码证据见 03 及 evidence。执行顺序以 04 为准，没有创建 production 治理切片。

| 顺序 | 实际动作 | 结果 |
|---|---|---|
| 0.1 | 读取各仓规则、交付手册、Contract First、ADR-0018、FEAT-151、真实代码与状态 | 完成只读审计；保留资料与代码不一致的记录 |
| 0.2 | 查询官方 commit/tree，15,305 项源树逐文件 blob/mode 对照 | 15,299 个现存文件一致；6 份指南已缺失；0 内容/模式修改 |
| 0.3 | 核查 manifest、remote、toolchain、Docker 应用与原厂 Compose | 不可访问的 36Dge/yijie-coze 未登记成已有远端；未启动 Docker |
| 0.4 | 冻结已有仓状态与 Desktop 八份修改文件哈希 | 文件/分支/remote 保持 |
| 1.1 | 原 Coze 目录 init main、fetch 精确 SHA、read-tree 建初始索引、update-ref 恢复 HEAD/tracking | 只新增 Git 元数据；无 checkout/reset 或源文件覆盖；shallow 范围如实记录 |
| 1.2 | 加入 repos.yaml，精确允许 Coze 上游 URL/path/main，保留其它仓 develop 与 URL 策略 | 项目 12 仓；没有创建或引用不存在的易界远端 |
| 1.3 | Coze 添加 AGENTS、README.yijie、source lock、.codex 与只读检查；Makefile 末尾追加 lint/test | 原 Makefile 前缀与默认目标保持；上游目标未改语义 |
| 1.4 | 同步元仓 README、AGENTS、架构/services 索引、CODEOWNERS 和 manifest 测试 | 本地治理接入完成；运行依赖尚未激活 |
| 1.5 | 执行安全检查、核验源保持及其它仓状态 | 见 02 与 step1-verification.json；AC-001 PASS，其余运行 AC 无证据 |

## 改动边界

当前只修改 yijie 治理文件和 yijie-coze 接入文件。Contracts、API、Infra、Desktop 业务代码没有变化；原 Desktop 未提交设计改动未被覆盖。Coze git diff 中六份删除是恢复 Git 元数据后显现的原有缺失，**不是本次删除**，不能混入未来提交。提交前必须重新逐文件审阅。

source origin 是用户提供的 coze-dev 地址。没有新建易界 GitHub 仓库、新建提交、push、tag、发布、模型或商家调用、业务 migration。未发布的易界适配不能由新机器单独 clone 上游获得。

## 实际检查与独立复核

元仓 pnpm lint/test、Shell 语法、require-siblings 治理、Coze 专用 lint/test 已执行。元仓 50 项测试仅覆盖元仓结构/治理；Coze 两个目标仅覆盖接入和来源，均不是引擎或 UI E2E。

独立只读复核发现并修正两处 P2：

1. Coze README 原误称本仓 make lint 会检查元仓登记；删去此声明，登记由元仓 pnpm lint/test 独立负责。
2. 原第 2 步要求真实 editor 资格，但 Contracts/provider/Infra 尚未就绪。已改成第 2 步具体设计+D0，第 3/4 步最小契约/provider/受控栈，第 5 步先真实载体资格再扩展完整 Desktop 功能。不能用 mock/session 捷径跨越依赖。

复核同时确认原 Makefile 默认 debug 未改变、六份源文档缺失未被改写、没有伪称 D4 或服务已接通。跨仓 make lint/test/generate 未执行：下游默认链含用户禁止的历史攻击 fixture、危险归档或权限故障，后续只用已审查的 safe/focused 检查并登记影响。

## 第 1 步结束时的停点（后续已由第 2 步更新）

本地仓库接入已完成，下一步为 Proposed ADR-0019 的具体 native/CSP/session 设计确认及 D0。推荐同一 App 的独立 React editor、精确 loopback origin、editor 无 native capability、native/server 固定 scope 和受控短会话。尚未批准这一具体新安全边界，不提前实现开放权限或登录旁路。

这不是缺少审计材料，也不是未创建的 fork 阻断；第 1 步已经完成。只有依赖新安全设计的后续产品集成暂停。D0 pending，D4 NOT RUN。真实载体资格在最小 provider/受控栈可用后执行。

## 调用与费用

| 类型 | 范围 | 已用/状态 |
|---|---|---|
| 官方源查询/下载 | GitHub metadata/tree、精确 SHA fetch | 已执行；无业务写入，只恢复本地 Git 元数据 |
| 模型、平台、付费 API | 无 | 0，未执行 |
| 生产、GitHub 仓库创建、commit/push/tag | 无 | 0，未执行 |
| 危险 fixture/故障/攻击注入、破坏性操作 | 无 | 0，用户永久禁止 |


## 2026-09-12：第 2 步具体设计与 D0

用户实际回复“批准该方案，继续第2步”。已记录原话、范围与技术细化，见 evidence/step2-decision-record.json；不重复索取该架构授权。ADR-0019 转 Accepted，05 作为具体设计基线。

本步先核对实际 Tauri/Wry、Coze 领域和API/Infra代码，新增三份 step2 feasibility 附件。确认：上游缺草稿CAS、revision绑定成功试运行证明、指定旧版公开运行、真实历史列表和原子operation关联，这些由第3步在正确存储边界实现；30秒是合作式执行预算，不是HTTP超时。

HTTP跨站iframe Cookie与custom scheme各有平台/权限限制，因此在已批准范围内收敛为固定HTTP静态editor + 有限MessageChannel→具名native业务入口。短会话留Rust/API内存，不进入WK/renderer，不新增系统CA或scheme。固定gate、两段机密、300秒E、到期显式重连及资源校验已落文档。

独立审查修正：通用身份检查与editor绑定分开，首次打开/列表/关闭后的运行查询可用；URL-only导航hook不再冒称区分frame；window握手与port绑定区分；到期不reload iframe、不覆盖未保存图。正常容器停止明确SIGTERM+timeout=-1，避免默认有限timeout回退强杀。

本轮没有写第3步源契约/provider或第4/5步运行/UI代码，没有启动应用/容器、创建机密、执行migration、模型/平台调用、commit或push。第1步源检查证据保留原时点；新的设计文档不冒称运行证据。实际D0命令和结果见02与step2校验附件。

## 2026-09-12：第 3 步源契约 → 最小服务端与原生会话桥接

用户本轮明确要求先定义源契约，再实现最小服务端与原生会话桥接。实际 contract-impact=semantic；先完成独立 workflow-local/bridge 源、生成和初轮6项源校验，再让API、Coze和Desktop按同源候选并行实现。后续列表摘要和按operation限制字段均先修源、重新生成/测试、同步consumer，再对齐实现。没有先合并/部署provider再补契约。

Contracts新增Go/TS/Rust类型、JSON Schema和私有OpenAPI投影、桥接TS类型、精确来源/生成摘要锁及正常safe生成/验证/漂移入口。版本为1.0.0-local-candidate，base是真实811f38d...，不是虚构合并SHA；三个consumer独立锁保持旧public/Runtime来源不变。三固定baseline breaking、安全全量生成与lint、7项源测试通过。

API新增独立server/migrate入口、四张独立PG表、固定scope与真实Coze client、操作意图/receipt和审计、300秒E；原api-server/OIDC/global migration不改。Coze补真实CAS、原子operation/执行登记、同revision成功试运行证明、事务内部版本、指定版本执行、真实分页历史和共用slot。Desktop新增8个具名native入口、固定身份、E/epoch/context/generation、固定HTTP与正常清理，未改Vue/CSP。

跨端联审修正了列表/节点输出超限、私有写HTTP响应形状与状态、写后响应失败保留unknown/原ID、初始化principal顺序、凭据descriptor边界、容器监听范围、本地预算与迟到open。原生输出在SQLite/miniredis正常测试中由真实Eino/Coze引擎产生，明确不将其称为真实MySQL/Redis/容器栈。

本步结果：API 16项顶层tests+9路由子例及race/vet/build，Coze 9项正常tests及race/vet/build，Desktop 10项native tests/check/fmt/生产lib clippy，三consumer摘要检查均通过。Desktop包含tests的严格clippy被原Chat:1351既有lint阻挡，已记录，不改无关Chat。源保护仍保留七个未参与仓、全部原Git身份、八份用户Desktop文件和Coze六份既有缺失。

详细实现：[06](06-step3-implementation.md)；检查与范围：[step3-checks.json](evidence/step3-checks.json)；工作区保护：[step3-workspace-review.json](evidence/step3-workspace-review.json)。第3步源码/候选验证完成，D0继续PASS、D4 NOT RUN。未启动App/Docker/实际服务，未执行真实migration，没有ERP、模型/平台/付费调用、commit/push/tag或远端创建。下一步为第4步受控local栈，不提前把第5步UI/平台资格标为可用。

## 2026-09-12：第4步受控local栈与真实数据库验证完成

按用户本轮授权完成专用六服务/四命名卷、精确来源构建、PG/MySQL显式migration、六服务与宿主认证ready、真实HTTP/并发CAS/PG事务/MySQL交叉核验、正常停止及新epoch保卷重开。仅API接专用edge进行loopback18888发布，Coze/依赖保持internal；生命周期修复端口检查、凭据轮换、当前ready、已知旧构建容器清理及正常中断观察。

实库对账发现初轮save回执错误引用旧published版本；保留初轮失败证据及历史回执，按源OperationReceipt说明澄清/canonical生成/三端同步后修复API映射，再以新W3/W4验证通过。最终主流程4次真实成功运行、3个内部版本、12条原生节点记录与10条Coze已提交操作匹配；PG正常8并发Claim唯一登记和审计/reconnect通过。

最终专用栈全部exit0/noOOM、18888释放、volume保留，原六容器和八份Desktop文件保持。原厂Docker Desktop正常stop命令exit0，daemon socket不再可用；早期下载凭据助手等待进程另行记录，未强杀/改Keychain。没有App/iframe/具体ERP/模型/平台/付费调用或Git发布。完整结果见[07](07-step4-local-stack.md)；当时第5步未开始，D0保留PASS、D4 NOT RUN。

## 2026-09-12：第5步解锁后真实App最小资格完成

用户明确执行dev→会话/边界→packaged验收。本次先通过canonical入口恢复受控栈，随后在真实dev创建独立合成流程，
添加文本节点、编辑中文前缀、拖两条连线和节点位置、保存返回重开；完整图自然到期后保留未保存前缀，正常点击保存被阻止，
显式重连再保存成功。未保存离开/Chat切换可取消并保留草稿，干净切换显示原Chat界面且移除editor。

packaged使用标准unsigned开发构建，从实际tauri://localhost进入同App编辑器，独立创建另一流程，完成同样的核心闭环。
Tab与Shift+Tab能跨iframe切换并回到文本输入，实际窗口中手动适应与正常滚动后关键控件/画布可查看。
两资源分别与API、PG、MySQL读回对照；dev1create+4save、packaged1create+1save，没有新增版本或执行。

为取得真实App关闭的直接证据，仅在Desktop原生增加exact-local且Configuration::Enabled的关闭诊断：
认证DELETE 200及typed closed=true后输出公开关联标识，不输出session ID/E/机器密钥/URL/headers。
该私有观测子变更为additive，整体FEAT仍semantic，业务wire不变；13项安全native测试、fmt、strict lib clippy和标准构建通过。
新dev及packaged的实际返回/Chat切换均取得对应remote_close_confirmed；幂等确认不冒称旧E攻击重放探测。

截图权限初始不可用，用户回复“已完成”后再执行真实视觉观察。最初自动化AX输入/后台鼠标并非每次生效，均以实际UI与持久化结果确认；
未把尝试动作记作成功。MySQL只读客户端初次编码错误的快照保留，显式utf8mb4复核与数据库侧字节/hash一致，未改业务数据来配合验收。

所有App及自有服务均正常退出，端口释放、四卷保留；确认无其它运行容器后原厂Docker Desktop正常停止，未强杀或改权限。
12仓HEAD/branch/origin保持，7份原设计原样保留、8份设计本轮均未改变；Coze6份原缺失和editor6个资产摘要保持。
结果与限制见[10](10-step5-real-app-qualification.md)。5.2/5.3最小资格通过，5.4尚未开始、D4 NOT RUN；
首次自动fit、暗色/1440×900与完整新增可访问性随后续产品页面补齐，不继承历史D4或全页axe结论。

## 2026-09-12：完整产品页与首次自动适应实现，真实视觉待解锁

用户明确授权首次自动fit、完整产品页面与全主题/尺寸验证。已在已有源契约上接入画布内试运行、同revision成功证明后的内部发布，以及Desktop明确版本执行、完整输入/输出/节点、分页历史与原操作查询。首次fit只在真实图层/测量完成后执行一次，用户操作/重连/卸载取消迟到适配，不改持久坐标。编辑时收起方案示意，保留真实入口和原Chat边界。

独立审查发现无操作ID的未知执行会阻止离开、旧历史读取期间新运行刷新被丢弃；已增加明确离开确认与排队刷新。非终态运行保持待核对，不将completed回执或未知state说成成功。标准编辑器/unsigned开发包与定向检查通过，当前服务栈正常恢复、宿主认证ready、原packaged资源完整读回一致，公开产物机器凭据匹配0。

CUA两次报告Mac当前锁定，已异步请用户解锁；没有绕过锁屏或启动一个无法正常UI退出的App。新全流程、首次fit实际效果、light/dark × 1180×760/1440×900仍NOT RUN。服务正常停止、四卷保留，不回填旧App截图作为新页证据。详见[11](11-step5-full-workflow-product.md)，D4保持NOT RUN；未提交/推送/发布，无模型/商家/平台/付费调用。


## 2026-09-13：真实 packaged 完整产品与四主题尺寸组合验收

按用户解锁后的指示完成真实创建、节点/连线编辑、保存重开、试运行、两次内部发布、指定旧版执行和结果历史；新B两版/四run与API和两库一致，正常App和受控栈stop/up后完整读回相同。亮/暗×1180×760/1440×900由CUA实际观察和native尺寸验证。暗色画布仍浅色、取消Chat后文档标题错误两个问题已修复，149前端定向测试、13native测试与canonical构建通过；最终App复验标题、重开历史及关闭确认PASS。

当前dev裸进程CUA仍不可控，标准元数据尝试未解决且已撤回，用户明确已用Cmd+Q退出；dev完整页UI不计PASS。自有App/Host/Codex/Vite与栈、Docker均正常停止，四卷和所有既有设计文件保留，系统浅色/默认缩放/Dock恢复。91公开文件凭据匹配0，无任何模型/平台/商家/付费调用或提交发布。详细证据见[12](12-full-app-theme-size-qualification.md)；整体D4保持NOT RUN。


## 2026-09-13 10:41：启动统一 D4，人工 dev 待反馈

用户明确要求按dev人工操作、剩余边界和统一fresh D4收口。已冻结五候选并核对12仓，恢复同源受控栈、启动标准dev PID4642；人工A清单已提供，等待实际操作反馈与新资源读回。16 UI/state、13 native、11 Contracts、13 Infra及API/Coze正常测试通过；摘要不变，公开响应/实际binary凭据匹配0。新增控件源码可访问性和六仓提交顺序已整理，未把测试替身或历史packaged数据当成本轮App通过。详见13/14，D4仍NOT RUN；本次App与栈暂时保留供人工验收。


## 2026-09-13 11:08：收到人工 A 完成反馈，定位资源对应关系

用户先询问能否由Codex代操作，重新核实CUA对当前dev仍Invalid app；限定AX/CGEvent替代方式只形成15的提案，未执行。随后用户明确“A完成”。当前epoch全部9条合成流程和无分页遗漏的运行历史只读核对没有发现本轮新资源或新run，已记录反馈并请求实际操作的名称/版本/输出以定位。B与D4依赖步骤暂待对应确认，不补写或伪报通过。


## 第6步收口：最终候选统一D4

2026-09-13。用户明确授权AX/CGEvent后完成真实dev A/B；发现键盘画布缺口，正常停止后仅修改Coze本地UI三个文件，21项普通测试与canonical构建通过。新资格ea50e666-898c-4107-9568-10e3e3d63416固定候选后，dev/packaged各新建合成流程，完成键盘/鼠标编排、保存重开、两版试运行发布、旧版执行、结果/历史、自然到期重连及Chat取消。四主题尺寸组合实测；正常App/栈重开，两个资源的完整workflow/canvas/history/runs/receipts相等，真实App再次读取。最终App/Host/Runtime退出、8容器正常停止、4卷保留、端口释放，亮色和默认显示缩放恢复；无Git或对外发布。完整证据与未执行项见[17](17-d4-final-qualification.md)，交付顺序见14。

## 2026-09-13：按用户授权完成 Git 交付

用户确认需求完成后明确要求暂存、提交并推送。先形成 Contracts 不可变提交，补齐生成基线重放和完整提交逐文件验证，再同步三个消费者；九份wire/schema/validator保持D4字节。Contracts/API/Infra/Desktop已按顺序提交并推送且远端SHA相等，用户另行授权新建私有36Dge/yijie-coze，Coze已补齐上游历史并推送，元仓最后记录需求与证据。未向coze-dev推送。Desktop混合文件按来源暂存，两个既有共享设计依赖具名纳入，其余设计改动与Coze既有删除保留。暂存快照类型检查、21项测试、构建及source/consumer/baseline检查通过。完整提交和实际远端状态见[18](18-git-delivery.md)，不声明CI/merge/tag或生产发布。
