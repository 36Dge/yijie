# 新增13位专家：整体接入状态审计与下一步

日期：2026-10-17。依据：[原始接入方案28](28-thirteen-expert-integration-feasibility-audit.md)、第29—35报告、当前Skills/Host/Desktop/Connectors源码、当前App构建回执及六组实际交付证据。

`contract-impact = none`：本轮是现状审计、证据统计纠正与下一步建议，只修改元仓文档和派生审计记录；不改变资源、代码、公共协议、认证、持久化、历史重放或App行为。本轮未构建、调用模型/线上服务、操作App或读取运行中的SQLCipher/Bolt。

## 1. 结论与计数口径

**13位尚未全部接入。已接入10位，未接入3位。当前易界最新目录共21位＝原11位＋本轮新增10位。**

“已接入”指在下表明确范围内，已经进入现有真实资源准备、精确版本绑定、Host/Runtime执行和工作区文件交付链，并有实际App验收；不表示完整复制WorkBuddy所有能力、所有线上服务已验证或已生产发布。33个专家版本包含历史版本，不能计为33位专家。

| 组 | 专家 | 最新适配版本 | 已有真实证据 | 剩余边界 |
| --- | --- | --- | --- | --- |
| 1 | 产品管理 | 0.1.0 | Kimi多轮，六类产品文档、来源台账与修改保留 | 无Jira/Figma等自动业务集成 |
| 1 | 小说故事创作 | 0.1.0 | Kimi多轮，三章小说、设定及连续性台账、改稿 | 不保证长篇自动持续创作或零矛盾 |
| 2 | 淘宝天猫运营 | 0.1.1 | CSV/XLSX真实离线诊断、确定性财务计算及HTML文件 | 浏览器样式验收NOT RUN；无店铺线上操作 |
| 2 | 拼多多运营 | 0.1.1 | 独立平台口径、缺值/零值、真实诊断文件 | 浏览器样式验收NOT RUN；无店铺线上操作 |
| 3 | 数据分析 | 0.1.2 | 本地描述性分析、独立复算、真实HTML交互 | 不含完整机器学习/推断统计能力 |
| 3 | UI设计师 | 0.1.1 | 真实页面与搜索/筛选/表单/状态/主题/窄屏交互 | 不含云媒体或真实业务后端 |
| 4 | 跨境带货口播视频 | 0.1.0 | 三方案、事实台账、制作请求草稿，复用LinkFox broker边界 | 无账号，真实生成NOT RUN；上传/自动下载/本地MP4未实现 |
| 5 | 股票研究 | 0.1.2 | 离线估值、可复算报告，最终Kimi两轮及修订 | 线上金融取数NOT RUN；完整首次覆盖长报告未实现 |
| 5 | 量化策略回测 | 0.1.1 | 逐笔回测、费用/持仓/指标、真实dashboard及修订 | 线上行情NOT RUN；复杂组合与做空等未实现 |
| 6 | MOSS行业研究 | 0.1.1 | Kimi两轮、四类计算、HTML/XLSX/DOCX/PDF/PPTX实际交付与打开 | 用户无账号，OAuth/schema/服务调用NOT RUN；非上游全部能力 |
| 7 | 视频生成专家Remotion | 未接入 | 完整资料与方案 | 无受管专家包及产品渲染依赖锁，尚无真实MP4验收 |
| 8 | WindAlice万得金融专家 | 未接入 | 完整资料与方案 | 独立A2A provider、正式资格/认证/费用/任务状态未实现 |
| 8 | 美团生活助手 | 未接入 | 完整资料与方案 | 独立provider、客户端/scope/SDK资格及位置/交易边界未实现 |

逐组证据：[29产品/小说](29-thirteen-first-group-product-novel-integration.md)、[30淘宝/拼多多](30-thirteen-second-group-taobao-pdd-integration.md)、[32数据/UI](32-thirteen-third-group-data-ui-integration.md)、[33口播](33-thirteen-fourth-group-sales-video-integration.md)、[34股票/回测](34-thirteen-fifth-group-equity-backtest-integration.md)、[35 MOSS](35-thirteen-sixth-group-moss-integration.md)。

## 2. 当前工程与证据复核

三路只读审计分别核对当前架构与打包、六组实际交付、剩余三位依赖，主审交叉检查方案、报告及统计误差。

- 当前bundle为0.23.0，71项资源＝38普通技能＋33专家版本，21个不同专家ID。展示目录为空，卡片来自实际Native目录，不存在以静态展示卡计算接入数量的情况。
- 33个专家版本的634个源文件与归档逐字节相同；0.22.0全部70项旧metadata与archive摘要精确保留。authority引用的68项来源/审核摘要匹配。
- Skills产物、Desktop候选、Host固定值、实际App的专家manifest SHA均为 `cdb89e828a8cfafcfda9368cb0f521289f97e35535f9f73a2372e00b04309cd9`；authority SHA为 `fb9c2f537627e49da1ac05c41797dbb26201b3ba8a2cc12102c861870cfe5f90`。
- 当前App回执120个构建产物重新校验一致；1000份Desktop、54份Worker及实际激活专家Host候选351份源文件与冻结记录相符。未激活的普通Host旧候选有源漂移，不混同为当前专家App来源锁失败。
- 六组38份实际产物回执中的387项文件摘要复算均一致。这证明已归档产物存在且未漂移，不替代重新运行当前App或重新审阅全部内容语义。
- 仍复用 `canonical资源 → 精确manifest/authority → Native准备与ExpertRef → 持久绑定/outbox → Host验证组合 → 现有Runtime/普通工具/显式选中连接器`。未新增专家引擎、专家团或因本批专家新建历史数据迁移。
- 原专家、旧精确版本及历史保留由各组正常退出后的核对记录支持；第35报告最终基线覆盖原26会话、133消息、67轮及Runtime/安装文件，并另核对0.1.1构建前27会话。本轮没有再次打开运行中数据库，也不将保存的历史核对冒充新跑结果。
- 当前属于 `local-development / release:false / working-tree candidate`。各仓仍有前序未提交工作，不能写成正式发布或生产就绪。

当前构建及保留证据在 `yijie-desktop/.local/thirteen-sixth-group-20261017/`：`packaged-launch-receipt-v011.json`、`built-artifacts-verification-v011.json`、`final-history-preservation.json`、`final-history-preservation-v011.json`、`implementation-audit-v011.json`、`determinism-v011.json`。实际源入口为Skills的 `plugins/yijie-desktop-skills/experts/bundle-source.json` 与 `dist/skills-experts-thirteen-sixth-v011/bundle-manifest.json`。

## 3. 已处理的问题与不能扩大解释的结果

接入过程中确实发现并修复了实际问题：淘宝/PDD财务口径与缺值处理；多会话Native观察不完整；Python导入缓存污染严格资源目录；股票DCF和回测净值/费用/时点口径；模型修订中错报数值/状态；MOSS PPTX被WPS拒绝及中文字体问题。对应报告保留失败、修订版本、独立复算与实际复测，旧版本没有覆盖删除。

Host来源锁及Docker Compose缺失也经过现有规范修复。[31报告](31-workspace-compose-lint-repair.md)及第35报告的最近全工作区 `make lint CONTRACTS_DIR=.../.local/demo-fast-contracts` 为exit0，Compose语义检查通过。这个结果不等于全工作区所有测试通过；Coze仅执行集成治理检查，其上游application lint仍NOT RUN，既有OpenAPI warnings保留。历史不适用或用户禁止的故障注入测试未执行，不能因lint通过改写为PASS。

MOSS调用统计有一处审计更正：此前聚合JSON用文本命中入口，误收录仅写说明文件的 `exec_command_22_fd5d368d`。实际入口执行为**8次：freeze 2、deliver 2、verify 4**，其中含新state校验旧输出的正常stale拒绝。已修正第35报告；原始日志和此前聚合JSON原样保留，派生纠正记录见 [moss-call-count-correction.json](sources/thirteen-experts-overall-audit-20261017/moss-call-count-correction.json)。该统计误差不推翻两轮完成与产物结果。

## 4. 仍需关闭的缺口

| 缺口 | 分类与影响 | 应如何处理 |
| --- | --- | --- |
| 缺少同一最新构建的10位整体业务终验 | 验证覆盖缺口；各组业务验收在各自构建完成，最新工程生命周期回归不能替代每位业务流程重跑 | 固定当前构建回执，10位各做代表性真实会话、文件打开及修订，旧专家/普通会话交叉回归 |
| 淘宝/PDD HTML浏览器验证缺失 | 现有报告明确只经TextEdit静态打开；后续其他专家HTML通过不能替代 | 使用现有受限本地预览方式验证真实六份报告的渲染、长表/缺值、主题/窄屏与可用交互 |
| LinkFox、金融、MOSS线上未验 | 账号/资格及验证缺口；用户授权无账号项跳过 | 保持NOT RUN，拿到可用资格后独立核对实际schema、权限、任务与结果，不伪造远端成功 |
| 口播上传/下载/本地MP4等未实现 | 功能范围缺口；即使将来有账号，也不能自动变成端到端交付 | 单列实现与验收，不能只补账号便宣称全部视频能力完成 |
| App内统一产物承接不足 | 跨专家产品缺口；当前工作区文件不自动成为HostArtifact，Markdown路径不等于一键打开，任意HTML及有声MP4不在现有Native支持范围 | 独立评审产物登记、用户手势打开/预览、生命周期与契约；不能删校验或伪造Artifact producer |
| 剩余3位未接入 | 实现与依赖缺口 | 按第5节推进，WindAlice/美团不能仅记“无账号跳过”后计为完成 |

现有 `artifact_video_native.rs` 只接受单视频轨MP4；有声Remotion产物首版按原方案通过工作区文件和系统播放器交付。如果目标是App内有声播放，应纳入独立产物能力设计。

## 5. 下一步优先级

**第一优先：对当前已接入10位做一次同构建整体回归收口，补齐已有验收缺口。** 理由是这些组共同依赖的Native、Host、资源与产物辅助程序已多次变化；目前静态来源一致和逐组历史通过仍不足以证明10位在最新App的一次整体验收。此项不需要新增外部账号，也不需要新架构。

最小收口范围：固定一个当前canonical构建；使用Kimi-K3；每位完成输入→实际执行→可打开文件→一次修订/缺值处理；优先补淘宝/PDD浏览器检查；抽查旧专家、旧版本绑定、普通会话和正常退出重开；保留原数据。无账号部分继续NOT RUN，模型限流不改写为通过；只有发现需要修代码时才修复、重跑相应检查及全量lint并按标准更新App。

**下一位新接入：第7组Remotion视频生成专家。** 它可复用既有资源和普通工具链，不依赖LinkFox账号。实施前核对适用许可与当前官方依赖资料，固定Node/React/Remotion/浏览器/编码器及字体素材来源；本报告没有选择或宣称任何当前版本/许可证已满足要求。真实出口必须是15—30秒带声音MP4：独立核对尺寸、fps、codec、时长，抽帧、中文字体与音画播放，改文案后另存重渲，保留分镜/TSX/依赖锁/回执。仅生成代码不算完成。完成后本批将为11/13，目录为22位（原11＋新11）。

**随后分别处理WindAlice与美团前置项目。** WindAlice原包是A2A JSON-RPC/SSE，现有`wind` MCP不是同一服务；需要正式客户端/认证/费用资格，以及Connectors任务、context归属、恢复/取消和受控附件。美团需要正式客户端scope、可审SDK、私有凭据和明确位置授权，优先只读检索，领券/订单/支付再逐项评审。不得直接迁移原包WorkBuddy身份、明文凭据、脱管进程或生产交易路径。

统一产物承接是跨10位最有价值的后续产品改进，可与剩余外部资格调研并行设计，但应有独立范围和契约评审，不塞入某一专家包。正式发布/提交也需独立授权，当前审计不执行。

## 6. 本轮检查范围

本轮重新检查当前来源/资源/App及已归档产物；真实模型业务、浏览器、线上服务、App更新和正常重开均未重跑。最近产品全量lint通过引用第35报告，本轮不因纯审计文档修改重复构建或批量运行产品测试。

本轮元仓 `pnpm lint` 通过（11仓清单及Contract First治理），`pnpm test` 50/50通过；7项Shell语法、`git diff --check`及本报告9个本地链接检查通过。既有未提交工作、原始验收日志、旧版本与用户历史保持原样；本轮只更正第35报告统计并新增本报告及派生审计记录。
