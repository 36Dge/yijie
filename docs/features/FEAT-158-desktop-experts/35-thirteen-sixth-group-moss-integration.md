# 第六组 行业研究专家 MOSS

2026-10-17，local/demo_fast 限定范围接入及验收完成。用户授权按28总方案推进第六组，指定Kimi-K3真实会话、文件和交互验证，深入代码审计、全工作区lint及canonical本机更新。账号不可用的线上验证跳过。

## 回顾与依赖

已完整回顾28总方案的架构、13项缺陷、八组顺序、产物边界和保留策略，external-content的MOSS专项、architecture附录及34第五组最终实况。当前基线0.21.0，69资源＝38普通＋31专家版本，共20位。12仓HEAD、branch、remote、dirty及原文件摘要已记录。MOSS源1.0.6与用户归档292文件逐项SHA256一致，原件不改。

源Agent、研究与深搜方法、计算器、交付编排和五种格式组件分别审阅。原MOSS强制授权、WebSearch优先与易界关闭内置搜索的差异采用明确两模式：用户资料offline；已有当前选中合格连接器取得的connector-evidence。后者必须保留service/tool/receipt来源；离线不冒充MOSS执行。原caller_expert仅在实际schema支持时传；不传X-Moss-WorkBuddy身份。现有fanruan-growth-advisor已登记OAuth/HTTP，但静态candidate仍not_run且activationAllowed=false，不将资源ready视为线上资格。

Office shim、受限moss-pdf代码、缺失PPT模板、宿主present_files/execute_python、额外子代理/专家团均不迁入。自有Python3.10+标准库计算与OOXML生成；PDF可选显式已安装的正常LibreOffice可执行路径，缺依赖明确失败、不自动安装、不修改全局运行时。当前本机已有普通LibreOfficeDev26.8.0.0.alpha0可转换，路径和摘要进回执；不将其打包或承诺其他电脑有此依赖。Codex文档/演示/PDF工具只作独立QA，不进入产品运行包。

## 实施范围与验收

contract-impact=semantic：新增本地受管内容、目录和信任摘要，保持experts/1、单入口资源、精确ExpertRef、现有SQLCipher绑定/outbox、Host组合与Runtime工具链；无新wire/provider/迁库/安全权限。

独立moss-industry-research@0.1.0，与market-researcher并存。Plan、同一research_state、来源原文与引文、事实/推断/假设/建议、缺口和下一步；显式边界/年份/单位的TAM/SAM/SOM、CAGR、完整/部分集中度、权重/收益成本方向/并列/缺失评分与情景。固定计算插值避免模型心算数值；结构校验不声称自动语义审查。

冻结包含状态和重新计算结果的内容摘要，HTML/XLSX/DOCX/PDF/PPTX仅取同一冻结内容；当前state变化则验证拒绝，另存再冻结，旧输出不改。receipt记录每个真实文件SHA和实际依赖；generated/structural、视觉检查、内容审查和线上资格分开。文件由Finder/系统应用打开，HTML受限loopback交互；没有新增App内产物桥接。

本次验收覆盖：独立数学回归（包括缺值、0、部分份额和并列）、冻结过期检查、五格式生成及逐页渲染、真实Kimi多轮读取与修改另存、实际打开/浏览器交互、旧69资源逐项保留、正常退出重开与原26会话历史检查、现有完整lint及标准构建回执。只使用普通非破坏流程，不读运行中数据库。

证据目录：`yijie-desktop/.local/thirteen-sixth-group-20261017/`。启动App已正常Quit，进程/18081退出后完整备份db/wal/shm、Host、26份Runtime历史和609份安装文件。最终执行结果和结论见下文。

## 代码审计与首轮工程记录

自有计算器、输入/引用校验、冻结复算、格式路由、回执、正常Office转换和前台预览逐项审阅。普通回归独立答案：TAM12000000/SAM4800000/SOM480000，低高情景240000/720000；2023→2025增长10000000→12100000，CAGR0.1；完整份额0.4/0.3/0.2/0.1的CR2=0.7/HHI3000，部分0.4/0.3只给HHI2500下界；权重0.6/0.4且成本反向后a=76/b=68/c未知不排序。已验证零值、缺值、并列、口径不一致、来源日期/quote和冻结过期等正常边界，不使用攻击fixture。

预渲染发现中文字体缺失，已通过系统Heiti SC与正常FONTCONFIG_FILE修复，缓存仅位于新输出profile；没有修改可执行文件、系统字体或全局配置。DOCX换行和长XLSX文本分行也修正。正常Office产出5页DOCX/PDF、21页PPTX简报并渲染检查；首轮缺字样本保留。最终App输出仍需重新逐格式验收，不能以预检代替。

资源保留基线0.21.0的漂亮打印JSON为265771字节，超过既有256KiB读取门禁，首次sync/freeze因此失败。改用仅去空白的199707字节保留快照，69条完整metadata/archive值逐项相同，原manifest保留；门禁未调大。原manifest SHA756ce70db4df8158b414a1b114f2a8753c7e40e0847f14911c85fbbbab05f552，紧凑快照SHAcc82a93449551b2a9abc57ea9752b3b4bce21c08a1e4e6d832ca0981d6e8e472。

canonical bundle0.22.0：70资源/32专家版本/21位，manifest45a2908c0a727de12e074dde32377c9218e9ae29309a4339d97838d831819c27、authority2a8ff309f34178c1a89e8eda95b3a0b2074499301aaf0446ca75e05edf197a1a；72文件二次确定性一致，全部旧69条metadata及archive精确保留。Native目录测试漏改69→70首次失败，补齐精确断言后重跑；不放宽数量上限或删旧版。

## 真实首轮及兼容性修订

用户明确答复无 MOSS／帆软账号，线上服务验收 `NOT RUN`。Kimi-K3 首轮真实 Native session `01a14a0a-8759-7bc3-9943-fd562153b242`、Runtime `01a14a0a-87c6-7190-91fe-02902584eb44`，ask/workspace-write/max，已于 2026-10-17 21:32 正常完成。实际从安装包执行 freeze/deliver/verify，生成五格式和模型复核说明；独立数字与全文检查通过，XLSX/DOCX 在 WPS 正常打开。模型明确未代为宣称人工/视觉验收。

实际打开 PPTX 时 WPS 拒绝，LibreOffice 可渲染不足以证明编辑器兼容性。排查为自有 OOXML 生成器缺少 slide → layout → master → theme 关系与 presentation master/property 部件。依据 Microsoft PresentationML 标准结构补全原创空白母版、版式、主题和属性，未引入上游模板/SDK；相同冻结内容的预检修订稿已能在 WPS 打开 21 页。失败文件、截图和原包均保留，0.1.1 新资源与 0.1.0 并存。标准结构参考：<https://learn.microsoft.com/en-us/office/open-xml/presentation/structure-of-a-presentationml-document>。

正常 Quit 后确认 App/Host/worker/Runtime 退出、18081 释放，再备份 27 份 Runtime 历史、630 个安装文件及完整 Native/Host 数据，读取首轮已完成状态。未读取运行中 SQLCipher/Bolt，未强杀。此前26份历史仍按原基线在最终验收中核对。

0.1.1 对应 bundle 0.23.0：71资源＝38普通＋33专家版本，21位最新专家。0.22.0完整70条metadata/archive以204086字节紧凑快照保留，SHA `781d78952bcf9a6b28040dd1d237a18c13a2ff9c15e8caeb9e0712a034f440d9`。新manifest `cdb89e828a8cfafcfda9368cb0f521289f97e35535f9f73a2372e00b04309cd9`，authority `fb9c2f537627e49da1ac05c41797dbb26201b3ba8a2cc12102c861870cfe5f90`。新增正常关系图回归覆盖全部内部目标、每页版式、母版主题及属性。

明确范围：离线四类有界计算、多情景、证据台账与文本型五格式交付；不宣称移植原MOSS全部计算器、任意Office编辑器、品牌模板、自动监控或在线深搜服务。XLSX是保留数值类型的冻结结果，不是动态公式模型；HTML包含章节跳转/文本筛选。真实线上资格、账号、schema和服务结果仍待可用账号后单独验收。

修订版工程检查：Skills 139 测试通过，221 个合成 eval／35 数据集仅结构校验；Native 15 条命令覆盖 43 个测试、UI 141 测试通过。全工作区 `make lint CONTRACTS_DIR=.../.local/demo-fast-contracts` exit0（53.89s），Compose 语义检查通过；Coze 按工程脚本仅 integration governance，上游 application lint NOT RUN，既有 OpenAPI 非阻断 warnings 不写成无警告。

首次修订版 Host 回归识别固定 manifest digest 仍旧，已同步真实manifest摘要后重跑，未弱化精确比对。一次来源冻结的只读 gofmt 等待 stdin EOF，sample记录 read 阻塞，使用一次正常 SIGINT 取消该只读工具后原流程退出失败；与既有21报告记录的现象一致，不归因为已证明的Node版本缺陷。未操作产品进程、未强杀；随后完整 canonical freeze 及 workspace lint 通过，未改工具或门禁。

## 最终真实验收与交付

本组按限定范围完成：`moss-industry-research@0.1.1`，现有专家架构和 `fanruan-growth-advisor` 选择/资格/审批边界复用；没有新增Provider、独立安装器、数据库迁移或专家团。原有20位专家保持，最新目录共21位。默认单专家任务可真实读取用户资料、复算、冻结、生成文件及另版更新。

最终 Native `01a14a1c-3ea1-7ff3-adbf-082988a636ed`，同一 Runtime `01a14a1c-3f18-7420-aef1-ec9cd12bd6e4`。Kimi-K3/max/on-request/workspace-write 两轮正常完成（181s、193s），真实调用安装包正式入口8次（freeze 2次、deliver 2次、verify 4次）。Native dispatch accepted、outbox done、两turn completed、资源准备 succeeded；保留旧会话仍绑定0.1.0，新会话固定0.1.1。没有模型替换或隐式fork。另有修复前0.1.0一轮，合计本组3个真实turn；失败PPTX仍是失败证据，不提升为通过。

2026-10-17整体审计更正：原统计9次误计入了仅写模型说明文档、正文提及入口的 `exec_command_22_fd5d368d`。原始日志与此前聚合JSON保持不变；[第36报告](36-thirteen-experts-overall-status-audit.md)及其派生校正记录说明排除规则。此更正不改变两轮完成、8次实际执行及文件验收结果。

| 验收 | 实际结果 |
|---|---|
| 基准计算 | TAM12000000/SAM4800000/SOM480000，低/高240000/720000，CAGR0.1，CR2=0.7/HHI3000，a76/b68/c未知；独立Decimal及XLSX数值回读通过 |
| 同Thread修订 | 仅capture假设0.10→0.12与版本溯源变化；SOM576000（+20%），其余计算与c缺值不变；新来源另存、不篡改原材料 |
| 旧输出失效与保留 | 新state验证旧交付得到正常stale拒绝exit1；旧state仍验证旧交付通过；旧118个输出文件逐字节不变 |
| 五格式 | 两轮分别真实生成HTML/XLSX/DOCX/PDF/PPTX及17个文件hash回执；各格式完整文本、核心值、缺值和冻结内容一致 |
| 实际打开与视觉 | 最终XLSX（9表）、DOCX（5页）、PPTX（21页）在WPS打开；原PDF在Preview打开。最终DOCX/PDF各5页、PPTX21页均渲染逐页查看，中文可读、无裁切重叠 |
| HTML交互 | 当前Chrome未连接，使用可用IAB；v2的576000筛选2条、N/A筛选3条、清空101条，章节跳转#section-2正常，browser error/warn为空。两个预览均stdin stop正常结束 |
| 深入审计与工程 | 0.1.1源码20项摘要审阅；关系图/数值/缺值/过期/保留回归通过；Host race真实33资源生命周期、旧版共存和模型/普通绑定检查通过（148.39s）。Worker沿首轮已通过15个Rust用例及Go目录回归，无真实在线调用 |
| 构建与重开 | 全量lint后canonical `--packaged` 更新同一App，120个文件与回执摘要/大小/权限精确一致；正常Quit后 `--packaged --reopen` 复验同一回执，真实UI恢复两轮、新旧版本各自绑定，无自动发送 |

最终冻结：base `bd3043b16cb02a631004d10000d62ba5b61c46a899870a6daa5006fb1cadce58`；revised `6857c14d56b0a4b09e05e3045d89789322ef361e93ace2c13d1ff2212d28d80a`。回执仍不自封视觉/语义PASS，外部验收在独立证据中记录。WPS一次名称框定位操作产生未保存的合成表格输入，已通过“不保存”关闭，文件SHA精确未变；随后重新打开原文件留证，未把误操作保存为产物。

历史核对在确认所有产品进程正常退出且18081释放后进行：原26个会话、133条消息、67轮、327条Host旧记录、4131条安装journal旧行、26份Runtime与608个安装文件保持；仅1条dispatch updated_at改变。另对0.1.1构建前27会话/135消息/68轮基线核对通过，27份Runtime、629个安装文件不变，旧0.1.0精确保留。当前28会话。安装0.1.1的21个文件执行前后树/hash相同，无导入缓存污染。源与归档292原件不变、12仓HEAD/branch未变，未提交或推送。

核心证据位于 `.local/thirteen-sixth-group-20261017/`：`actual-runtime-evidence.json`、`final-actual-sql-v011.txt`、`final-acceptance.json`、两份`final-history-preservation*.json`、`implementation-audit-v011.json`、`determinism-v011.json`、`checks-v011/`、`packaged-launch-receipt-v011.json`、真实打开截图与逐页PNG。最终可复查产物在 `eval-workspace/delivery-v011-revised/`；完整真实来源/重跑代码/冻结状态随交付目录保存。

MOSS账号、OAuth、线上资格/工具schema和真实服务调用因用户无账号明确跳过，状态NOT RUN；不以离线合成验收冒充在线行业研究或全部上游能力。后续按28方案进入第七组Remotion；WindAlice与美团仍需各自独立前置方案，本轮未实现。

最终文档收口后元仓 pnpm lint、pnpm test 与7项Shell语法检查共9项均通过，跨12仓diff检查通过。完整来源/输入/产物摘要最后复核无变化。App保持在最终0.1.1验收会话，预览服务已正常停止。
