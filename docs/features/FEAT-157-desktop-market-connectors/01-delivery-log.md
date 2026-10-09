> **2026-10-08 13:20 本地 D4 已验收**：Owner明确回复“接受分阶段证据，完成本地 D4（推荐）”。当前49项（淘宝闪购、豆蔻医生已移除），AC-001–010均已通过；采用Tushare原f8构建真实批准/拒绝与最新ea84构建本地回归，保留各自证据，不合称同构建实跑。D4验收未新增模型或服务调用；后续获准的Git交付见[19](19-git-delivery-2026-10-08.md)，未发布。最终记录见[18收尾矩阵](18-closeout-audit-and-acceptance-matrix.md)及[验收证据](evidence/closeout-verification-2026-10-08.json)。以下早期状态均为历史。

# FEAT-157 调查、候选设计与交付记录

> 最新实施见 [09 私有 Broker 控制](09-broker-control-implementation.md)。用户再次要求下一步并执行后，完成独立控制源、Host owner、Rust Gateway、普通取消/满容量终止修复及固定 Runtime 的最终本地合成资格。真实51服务与产品D4仍未完成；以下起草日志为历史。

> **2026-10-07实施更新**：用户已明确“根据需求包与设计包，开始实现feat-157需求，逐步实现”。按包内推荐方案开展本地source-first实现，D0产品方案确认；下文起草阶段的“未确认/只落需求”保留为历史。外部账户、付费调用、Git交付未授权，D4仍未完成。进展见[07实施记录](07-implementation-progress.md)。
> 2026-10-07（Asia/Shanghai）。本次只有需求文档，不是产品实现日志。

## 1. 本轮范围与事实分级

用户要求认真读取PDF，落FEAT-157，指定51 MCP、图标目录、易界配色及店铺授权右侧聊天入口，强调参考应用实现不能照搬、应复用Codex。已发出一次范围澄清，尚无回复，先完成全部需求/设计候选。没有把未回复当成实施、安全设计或外部操作批准。

| 类型 | 事实/结论 |
|---|---|
| Fact | 已逐页检查PDF全部9页及两图，MD/CSV51条匹配，图标全在；实际auth44/1/6 |
| Fact | 当前Desktop无市场连接器管理；Composer原生textarea，店铺入口为演示；文字草稿会随路由卸载 |
| Fact | Codex已有MCP client/HTTP/OAuth/stdio/工具生命周期，Host已有限定Sorftime链路，Connectors仍骨架 |
| Fact | 原生OAuth默认可能明文回退；stdio launcher有强杀兜底；loaded resume会忽略config；多工具审批关联不完整 |
| Assumption | 本期local、单身份每应用单账户、一次选集仅当轮、空选集无市场工具、多选、默认不带入计划 |
| Unknown | 易界供应商client/scopes、三HTTP凭据规则、淘宝资格、Google固定包、Keyring/安全EOF/可信选集的实际资格 |
| Conflict | 来源auth摘要与逐项数据矛盾；另一宿主网关与易界身份不通用；直接Runtime OAuth与ADR-0005冲突 |

这些Assumption均作为候选明确写出，未冒称用户原话或批准。外部未知的每项解除条件在05/06中保留。

## 2. 基线与已有改动保护

完整branch/HEAD/remote/status见 [workspace-before.json](evidence/workspace-before.json)。元仓初始干净。Codex/Host/Contracts/Connectors/API/Infra均无未提交变更；Desktop已有：

- docs/store-dashboard-plan-2.md
- src/pages/store/StorePage.vue
- src/styles/store-dashboard.css

本轮不修改这些文件，不切分支、不reset/checkout、不更新任何consumer pin。只在元仓新建FEAT-157目录。PDF渲染中间件放在CrossBSD/.local/feat-157/pdf，未进入需求仓，不更改原PDF/图标。

现有仓README/AGENTS部分“尚未实现”陈述过时；调查以具体源码、固定协议和当前来源锁为依据，保留差异，不顺手批量改写兄弟仓说明。

## 3. 实际工作与产物

| 工作 | 产物/证据 |
|---|---|
| 加载项目约定 | 元仓AGENTS、长期记忆、交付Handbook/Contract First、ADR与安全规范；相关仓规则按任务阅读 |
| 视觉来源读取 | PDF9页渲染和文字；两图；产品逐页映射见03 |
| UI与数据调查 | 导航、路由权限、Yj/Naive/token、Composer双入口、draft/模型submit/历史decoder；03路径行号 |
| Runtime/后端调查 | 固定Codex原生能力、Sorftime例外、Connectors骨架；04路径行号及资格条件 |
| 服务/资产调查 | 51条原值JSON、分类、图标哈希/格式/尺寸、官方依据；05和sources |
| 完整设计 | 00概要、03交互、04架构/契约、06决策/依赖/数据生命周期/回滚 |
| 验收设计 | 02十项Must、正常安全测试、逐服务账本与未执行项 |
| 机器状态 | feature.yaml的draft/pending/NOT RUN，不伪填D0/D4 PASS |

使用canonical脚手架实际路径为docs/dev/codex-feature-delivery/scripts/new-feature.sh；README示例scripts/new-feature.sh在此checkout不存在，首次该路径调用未写文件，改用真实路径成功。系统缺pdftotext，使用已安装pypdf提取并pdftoppm渲染；未安装依赖。

## 4. 交叉审查

分工调查后，UI与Runtime审查者互读整包，重点查来源、草稿/模型、选集隔离、凭据、审批和完成口径。此为Codex结构化交叉审查，不是独立人工批准。

已将以下容易误实现的问题提前纳入需求：

- 连接器不是插件安装API；店铺UI演示不是账户/租户授权源。
- 目录收录/安装/授权/可用/本轮选择/实际执行不是一个boolean。
- 管理往返需共享正文/选集及新任务模型/工作空间意图，不能仅在ChatPage临时ref保存。
- 非秘密安装记录推荐复用Native SQLCipher，Connectors不再增设产品数据库，异步revision回执与Keyring查证分开。
- 51服务与每服务审核工具集的完成口径统一；Calendar自管token不被通用Keyring自动覆盖。
- 当前日常Runtime基线修正为FEAT-156五patch候选及实盘哈希，不以旧stable来源冒称当前装配。
- 连接器refs需覆盖普通与模型submit分支，并版本化reader-first，不能塞入旧contentBlocks。
- OAuth secret只在Connectors边界；Keyring的namespace不能靠CODEX_HOME自动隔离。
- 原生MCP配置重载不代表立即撤权；最终执行必须Broker校验可信会话/turn绑定。
- 原生多工具审批不能猜最近Item或泛化Sorftime单工具推断。
- 库内session-expired恢复可能再次调用工具，写工具必须有相应幂等/不重放证据。
- Google stdio不能复用有强杀升级的launcher；公开字节流桥接仍需正常资格验证。
- 来源清单宿主路径、淘宝网关、图标JPEG伪扩展名、Google Maps归档均如实登记。

最终检查命令和审查修正追加在02，不重复以设计自检冒称产品运行成功。

## 5. 未来连续实施顺序

按06推荐方案和04资格条件：固定原生/供应商依据 → Contracts权威源 → provider与兼容reader → Host/Native可信执行快照 → UI → focused checks → canonical真实主路径和逐服务证据。demo_fast不建立治理切片；任何新增安全边界、存储、依赖或Runtime核心改动须由具体候选方案评审后实施。

本轮不变更Accepted ADR。新功能风险按breaking保守管理；当前文档变更none。局部复用事实不等于资格通过，文档候选不等于编译产物或已发布接口。

## 6. 外部授权与调用

| 类型 | 上限 | 实际 | 说明 |
|---|---:|---:|---|
| 模型/图片 | 0 | 0 | 不继承既有需求预算 |
| MCP元数据/业务调用 | 0 | 0 | 未运行initialize/tools/list/tools/call |
| OAuth/账号/凭据配置 | 0 | 0 | 未创建、读取或存储真实secret |
| npx包安装/本地服务运行 | 0 | 0 | 只读包维护者资料 |
| 付费/业务写入/生产发布 | 0 | 0 | 未授权、未执行 |
| Git提交/推送/tag | 0 | 0 | 仅新需求目录 |
| 官方公开文档查询 | 只读 | 已执行 | 用于协议事实和维护状态，不触达用户账户 |

未进行进程强杀、可执行文件替换、权限破坏、恶意资源或攻击fixture注入。后续验收同样遵守；跳过项必须记录原因和影响。

## 7. 当前交付状态

完整候选需求、UX、51清单、后端复用/补缺、契约顺序、风险与验收计划已落盘。尚未确认的实质决策和外部条件集中在06，不分散成隐含实现假设。D0 pending，产品实现pending，D4 NOT RUN，DP N/A；业务代码和日常环境未动。

最终回执：元仓lint、50项test、shell语法、需求结构/claims及51条目/资产核对均通过，详见[02 §7](02-verification.md#7-最终文档检查回执)。产品运行全部NOT RUN，未消耗外部调用。


## 2026-10-08 完整范围复审（Owner再次确认仅Tushare真实验收）

依据最新指令，其他50项只作代码审计与本地测试；旧诊断不足不阻塞。51项代码审计揭示非Tushare provider仍被专用分支拒绝，不能把目录和可安装等同执行已实现。已补历史轮次结果查看、原名称快照、未确认审批跨会话保留、普通无市场历史无需Host，以及准确的未完成入口文案。标准重建后重开原Tushare四轮并读取09:31成功结果通过；本轮新增模型/业务查询0。详情及后续直接实现provider顺序见[14](14-completion-audit-2026-10-08.md)。

## 2026-10-08 通用执行与最新49项范围收尾

Owner采用通用发现＋逐次审批，继而移除淘宝闪购、豆蔻医生，提供Agentic Engine官方资料恢复其接入。已完成49项目录/注册表/图标映射/Native/客户端同步；AE自有安全页按导出HTTP Header配置，官方资料未明确字段，不猜Bearer。

Tushare通用候选f8真实批准返回HTTP200/close=11.5，拒绝0发送；追加额度已耗尽。后续c39标准构建包含执中query认证及最新范围，普通回归Worker56/Native38/UI56/Contracts15通过，Clippy/lint/source checks通过，真实App目录与AE详情已读屏核对。此后新增模型/业务请求均0；其他48家没有真实调用。详见17与scope49-local-verification证据。

未修改固定Runtime、未覆盖用户并行改动、未commit/push/发布。整体D4仍按完整Must矩阵记录，不把专项PASS或不同构建证据混成一次fresh run。


## 2026-10-08 13:20 Owner确认完成本地D4

本轮补齐原操作授权页重开，以及自动/显式打开均须凭据管理权限的校验，契约family 0.2.0源先行生成同步。最新专项UI59、邻近69、Native39、Worker56、管理JS11/Rust6/Go、依赖JS22及Host9通过，标准应用安装/重启/取消卸载/确认卸载/草稿往返和旧历史查看通过。

Owner明确选择“接受分阶段证据，完成本地 D4（推荐）”：AC010及本地D4关闭，当前49项实现complete/usable。f8真实批准1发送HTTP200、拒绝0发送与ea84本地回归各自留据。本次模型/业务查询/非Tushare真实认证或metadata均0；没有获得新额度，不提交、推送或发布。详见18及closeout-verification。


## 2026-10-08 Git交付

Owner在本地D4完成后明确授权提交推送。已按契约→Connectors→Host→Desktop顺序交付，Desktop独立功能分支避免携带已有店铺提交和其他未提交UI修改；元仓随后提交本包和跨仓交付记录。详见[19](19-git-delivery-2026-10-08.md)。本阶段新增真实模型和供应商调用均0。


2026-10-08跨境扩展已实现：新增9项及图标、目录58/7分类；契约源先行生成，Shopify Global Catalog无密钥UCP、Sorftime旧执行退役。修复Native/worker/renderer数量限制及领星大目录容量。34项契约、59项worker、40+2项Native、69项UI/client/store/launcher和Host/Runtime普通专项通过（Host固定Runtime正常退出重启亦通过）。标准App曾确认58项/九应用搜索与Sorftime详情；最终容量调整重建成功后Mac锁屏，未冒称同构建再次实机通过。外部与模型调用0，未Git提交推送。详见[20](20-cross-border-commerce-extension.md)及证据JSON。

2026-10-08后续：按Owner要求将FastMoss从行业数据移至跨境电商，目录revision7（10/16，总58）；原身份/认证/执行保持不变。已重建并完成解锁后的同构建窗口检查，关闭先前锁屏缺项。17项前端/1项Native目录检查与Go目录检查通过，无真实调用，未提交推送；详见20和fastmoss-window-recheck证据。


2026-10-08 Sorftime 配置页重设计：Owner 确认手工 Account-SK 方案，OAuth 决策已关闭。worker 安全页采用易界 token/品牌与 Sorftime 原图标，隐藏 Header/格式，提供获取密钥、显示/隐藏、保存并连接、取消及一致的错误/过期/回执。62 worker 回归、Clippy/rustfmt、JS 语法、token 快照检查和亮暗/窄屏视觉检查通过。细节与标准构建记录见 [21](21-sorftime-credential-page.md)。本阶段未发生模型或供应商请求，未提交推送。

2026-10-08 对话菜单精简：主菜单行高36px，添加文件与连接器图标区分；技能/连接器悬停展开260px级联，保留父菜单；子菜单只保留搜索、列表、必要状态与无描边管理按钮。快速展开的动画测量重叠已修复，最终标准App与管理导航检查完成。36项专项、lint、类型和构建通过；全量前端17项失败在改动前菜单上均复现，未冒称全套通过。误启动含禁止fixture的Native全套后已正常中断、披露并登记，不重跑、不计通过。详情见[22](22-composer-cascade-refinement.md)。本次外部/模型调用0，Sorftime真实复验尚未获得新一次请求授权，因此没有执行，未提交推送。


2026-10-08 20:44 Sorftime已保存密钥复验通过：Owner放开1次连接/发现及必要重试/模型；实际只发起1次正常配置流程，初始化和工具列表均成功，HTTP200/202/200，UI旧错误清除并显示可启用。重试0、模型0、业务0；保留待启用状态，未宣称业务批准/拒绝已验收。详见21最新段落与`sorftime-metadata-retest-20261008`证据。本轮无产品代码变更、无Git提交推送。

2026-10-09 连接器行内展示：输入区无边框的通用连接器图标＋青柠名称与正文同一行；发送后用户消息以“/ 原轮次名称”前缀展示。原生textarea保留，支持窄宽度、多选、换行与移除。菜单图标20px、普通行32px。31项专项、lint与构建通过；亮暗、1180×760及200%缩放的生产组件预览通过。实际窗口为未打包开发进程，CUA无法连接，已请求Owner正常退出后继续标准窗口复验，未强杀。外部调用0，未提交推送；详见[23](23-connector-inline-presentation.md)。
