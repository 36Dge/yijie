# 第三组：数据分析专家与 UI 设计师真实接入

## 范围与复核

2026-10-17，按用户要求回顾 28 号总审计及附录、29/30 号前两组实施和 31 号全工作区 lint 修复记录。推进 data-analyst-pro、ui-designer 两位；不增加专家团，不替换原 15 位最新专家及其 20 个历史资源版本，不改历史会话绑定。

contract-impact=semantic。权威源为 Skills 版本化行为资产；沿现有 bundle/authority → Native 准备与精确 ExpertRef → SQL/outbox → Host 验证 ROLE/index → Runtime 工具链。公共 wire、SQL35/Host10、manifest3、experts/1、provider、Tauri capability、审批策略均不变；公共 Contracts 新版本 N/A。本次仍是 demo_fast/local-development，dirty sibling 不是生产发布来源。

原包与用户资料归档逐文件核对：数据分析 5 个文件、UI 144 个文件全部一致。本机 Python3.14.5 可用，pandas/numpy/scipy/sklearn/matplotlib/openpyxl 不存在；Chrome 及现有界面工具可操作本地开发页面。不会把 Codex 私有依赖路径写入产品资产。

## 实现及依赖决策

- 数据分析：显式数据字典和缺值/去重策略，CSV/JSON/值型 XLSX，标准库完成描述统计、分组、日期趋势与显式分箱。输出清洗行账、源数据摘要、结构化结果、本地 ECharts 报告和可复算脚本。复用已审查的表格读取实现与已有 ECharts 许可文件。没有统计推断/机器学习依赖时不声称完成建模或显著性检验，不自动安装库。
- UI：模型按实际需求生成页面与交互，优先当前工程组件/设计规范；独立 HTML 原型复用当前易界 token 快照，标明原型范围。补充本地资源校验、只读回环预览及交付清单，实际浏览器验收独立记录。静态校验不能冒充浏览器验收。
- 不引入原 UI 包的身份覆盖、MiniMax 客户端/密钥、云浏览器、cookie/profile 导出、隧道及远程安装；不复制缺少完整许可映射的字体，不假装存在 brand-guidelines/canvas-design 能力。原资料中的要求仅作为审计对象，不成为当前任务指令。
- 本组无业务账号依赖。浏览器验收针对本组新生成的本地开发页面；不转发之前被工具拒绝的 file:// 报告。页面不是 Native Artifact，不新增 HTML 自动执行或 App 内嵌预览入口。

## 兼容、顺序与验收

先实现 Skills 私有资源和正常确定性回归，独立打包两次；用原 bundle0.14.0 manifest `d5bf48f6ea6e9fad6ed51a80c02bf8c13ab7ec92c1589b4875166f7d029ea2b8` 保护全部 58 份旧资源。目标 bundle0.15.0/60资源/22专家版本/17位最新专家。再同步 Desktop/Host 摘要和来源锁，完成 focused conformance 与全工作区 lint，通过 canonical 脚本构建更新本机 App。

必须验证：真实专家会话与工具执行；数据独立复算、缺值不补零、重复策略可追踪；实际文件产出及打开；UI 主交互、键盘、亮暗主题、1180×760 和窄屏；原专家/历史内容与安装文件保留；正常退出、相同构建重开。源码审计覆盖输入/输出边界、源哈希、资源引用、事实保真、异常与部分成功。只允许正常非破坏性测试，不执行强杀、权限破坏、攻击注入等历史故障测试。

升级前通过应用正常退出并确认全部相关进程退出及端口释放，才备份/检查 SQLCipher 与 Bolt；运行中不读取数据库。回滚只通过 canonical 已有构建流程，保留新增版本及绑定，不删除或降级历史数据。

## 证据状态

本地证据目录为 `yijie-desktop/.local/thirteen-third-group-20261017/`，已保存十二仓基线、原 58 资源 manifest/authority 与原包一致性。初次会话和最终修复复测分别保留，以下记录全部对应实际检查。

## 真实验收发现与修复

1. 数据 0.1.0 报告长 SHA256 在 390px 下使页面宽度达到 520px；0.1.1 加入段落断行，0.1.2 实际报告亮暗主题均为 390/390，无页面级溢出，宽表在自身滚动容器内。
2. 数据 0.1.0 模型解读误用“人工解读”，并混淆清洗文件物理行与 `source_row`，对覆盖率差异表达过强。0.1.1 起 ROLE、评测与清单明确模型/自动复核来源、原始行号和可比性边界；实际复测采用 0.1.2。
3. 修复候选时间戳为 Python ISO `+00:00`，不符合现有 Native 要求的 UTC `Z`。修正 producer 元数据并增加消费一致性断言，没有改 Native 校验器。
4. UI 0.1.0 的真实已批准 Python 预览导入生成 `__pycache__`，使严格资源完整性检查拒绝整个资源。正常退出后确认原始包文件完全未变，仅将这份附带缓存按原 SHA 存入证据目录。UI 0.1.1 和数据 0.1.2 在本地模块导入前设置 `sys.dont_write_bytecode`，使用说明要求 `python3 -B`。普通可写目录中省略 `-B` 的正常调用也通过文件树不变回归。未覆盖旧源文件、回执或数据库，未放宽 Host 门禁。历史 UI 0.1.0 继续保留，旧绑定不会自动升级；若继续调用旧预览须用 `-B`。
5. 历史会话复核发现 ChatPage 用“只含最新版卡片”的目录判断旧版绑定是否可发送，导致旧包完整也被误判不可用。沿现有 Native binding read/operation read 增加精确版本资源检查，只投影当前可用状态，不写绑定表；聊天页消费该检查结果，未绑定草稿仍要求目录精确版本 ready，执行环境及 Host 每次 apply/turn 的资源与权限校验不变。新增 4 个版本兼容 UI 回归，覆盖旧绑定、资源不可用、执行环境不可用和未绑定草稿，未增加 wire/capability/数据库结构。
6. 扩大 ChatPage 回归时发现 5 个旧测试仍用 legacy archive 伪装实时状态、缺少本地 queued submission 或假定添加附件会自动选工作区。测试改为现有 Native observed/live-turn 和 local submission 事实，并同步当前界面文案；没有改产品行为来迎合旧断言。整个文件默认模式 65 PASS，开启模型 flag 的另外 2 项 PASS；未新增 skip。

修复版本从现有版本化资源路径追加，不回写已安装的包。最终 bundle0.17.0/63资源/25专家版本/17位最新专家，取代上文的首次候选目标。manifest SHA256 为 `6e66f10188eabecaeb2893a57dc6c335c4e2ee8c0311d0dae0fe1173aa467830`，authority SHA256 为 `2e111b6f25310974eb9c50c3497f7feadce64f5c387faf5c335864420f2e2390`。

## 确定性检查与代码审计

- Skills：107 个 Node 测试通过；161 个合成 eval 案例、27 个数据集通过格式校验。这不是 161 次模型验收。
- Native：43 个正常 focused tests；Host：实际资源目录/版本共存/精确绑定/正常重开及会话 race tests；UI：13 文件、141 个测试；全部通过。
- 资源保留：保护原 58 份以及本轮前序版本，当前回归基线覆盖前 61 份资源全部 metadata/hash；独立构建两次共 65 文件逐字节一致。
- 全工作区 `make lint` exit 0，覆盖元仓及 11 个兄弟仓，Compose v2 门禁实际执行；未降级任何门禁。Coze 现有 canonical target 只覆盖集成治理，不能写成 Coze 上游应用全量 lint。
- 代码审计覆盖显式字典/缺值/重复语义、Decimal 与分母、来源快照/回执/复算、只写新输出目录、HTML 转义/本地引用、有限文件预览、精确资源版本/摘要和历史绑定。UI 静态回执明确浏览器 NOT RUN，真实浏览器记录单独保存。
- 公共协议、数据库 schema、provider、审批策略和原生 capability 均无新增。未执行用户禁止的强杀、权限破坏、二进制替换及攻击注入测试；这些破坏性路径不属于本次验证覆盖。

## 真实模型、文件及浏览器验收

四个合成任务会话均使用实际本机 App、Kimi-K3/max、workspace-write/on-request。初版数据/UI 分别执行 37/38 次工具调用，修复版数据 0.1.2 和 UI 0.1.1 分别生成 `live-data-v2/`、`live-ui-v2/`，完整命令与收尾事件保留在用户日常 Runtime 历史中。SQL/Host 只在正常退出后读取；四会话均 completed、outbox done、无孤立 delta，具体次数和精确绑定见 `final-live-sessions.json`。

- 数据：9 行原始数据按明示策略保留 8 行；金额缺值 1、无效值 1，不补零；重复 ID 保留，原始 source_row 可追踪。金额已知合计 575.5、支出合计 105；日期窗口外/无效日期只从趋势排除。另用不导入专家代码的独立脚本复算，31 项全部通过。v1/v2 除专家版本外结果一致；输入与生成回执逐文件 SHA 均正确。模型解读准确标明 AI 生成，不再冒充人工，并将覆盖率差异表述为可比性限制。实际 HTML 亮暗 1180×760、390×844、趋势/分箱切换、同源数值表、键盘焦点和控制台检查通过。
- UI：模型实际生成 HTML/CSS/JS、项目清单、需求/README 和静态回执。v2 去掉自造品牌字块，遮罩及加载动画改用已有 token，app.js 与已验收 v1 完全一致。真实浏览器执行搜索无结果/清除、状态筛选、必填校验、Tab 焦点、新建计数 4→5、完成计数 1→2、Escape/取消无新增、loading/empty/error/permission-denied/ready 与恢复、刷新恢复 4 条合成数据。亮暗 1180×760、390×844 无页面溢出；窄屏弹窗 x=17..373，控制台无 warn/error。静态回执中的 NOT RUN 保持原样，独立浏览器证据另存 `ui-browser-final.json`。
- 浏览器曾断线，用户恢复连接后在同一 Chrome 恢复验收；视口曾作用于另一验收标签，该次读数标为 invalidViewportTarget，关闭已完成的数据标签后真实 390px 复测通过。未把 1180px 读数冒充窄屏结果。
- 安装目录三个检查对象（数据 0.1.2、UI 0.1.1、旧 UI 0.1.0）在执行及预览后文件树/hash 均未变。UI 0.1.1 预览以普通 `python3` 运行也未产生缓存；两预览服务均 stdin stop 正常结束。

本组真实接入范围是可复算本地描述性分析及真实页面代码交付。合成经营任务页面是 UI 专家的输出样本，不是新增经营业务模块；没有将演示任务伪装成真实店铺接口。ML/推断建模、云图片/视频、外部字体及生产发布均不在本次已验收范围。

## 最终构建与历史保留

历史版本修复后全工作区 lint 再次 exit 0，日志 `workspace-lint-final-complete.log`。随后使用 canonical `scripts/run-local-demo-fast.sh --packaged` 更新日常 `com.yijie.ai` 的易界 AI.app。最终回执的 112 项 App/Host/Runtime/worker 文件哈希全部匹配；这是标准本地 QA 无签名构建，不是生产发行。

最终构建中实际续聊：旧 UI 0.1.0、数据 0.1.2、UI 0.1.1 均读取了指定实际文件并完成回答，绑定版本、revision 和 thread 不变。最终四个本组合成会话共 7 轮全部 completed，工具调用总数分别为 37/39/35/47；各轮 outbox done、无 issueCode/receiptError、无孤立 delta。旧版 0.1.0 的资源不可用误判已实际解除。

正常退出确认 App/Host/Runtime/worker 均结束且 18081 释放后，比对三个备份基线：

- 本轮前：16 会话、91 消息、46 轮、16 个 Runtime 历史文件；全部历史内容保留，当前为 20 会话。
- 首次验收后：18 会话、95 消息、48 轮；原始记录、专家绑定和资源回执保留。
- 最后修复前：20 会话、99 消息、50 轮；本次仅在明确的三个合成验收会话追加续聊。Runtime 原始字节前缀一致；SQL 只允许这些会话活动时间以及既有刷新时间变动；Host 只允许这些会话的最新 turn/revision 投影和时间更新，其他历史行不得改写。
- 原 427 个安装文件（不含追加式 journal）全部保留；后续两个基线分别 468/507 文件也全部保留，唯一附带 Python 缓存按原 SHA 归档而非修改源包。旧资源操作 journal 4,121/4,123/4,125 行分别原样保留。

证据为 `final-history-preservation.json`、各基线 SQL/Bolt 差异、`final-live-sessions.json`、`final-build-hash-check.json`。没有重置数据库、删除聊天、覆盖历史包或自动换绑专家。

最后以 `--packaged --reopen` 正常重开，canonical 回执逐项检查通过且回执字节未变；界面确认原资深电商运营操盘手及全部 17 位最新专家均“资源已准备”。App 保持打开。浏览器临时视口已恢复，验收标签与前台预览均正常清理。`completion.json` 为本次本地交付索引。
