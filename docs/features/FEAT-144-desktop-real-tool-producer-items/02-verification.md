# FEAT-144 — 当前实施与验收记录

配置兼容阻塞已关闭：当前Host ccd815ff63542674daa80172a1c71ac7478edd0f、Desktop a5975f48e63d3f1d3a262e9e8dfc57ca0d923961。新E真实Tool completed/414ms，原生返回三字段对照通过；Sorftime正常停用、auto/full/ask、原数据canonical退出重开均PASS。累计元数据12/20、模型7/8、业务2逻辑调用保守扣4/10、图片0；应用与计数器均已正常退出。D4尚未关闭：当前来源下的原生Prompt正常拒绝未复验，不能继承旧B结果；已申请最多追加2次文本，未获授权不调用。AC-004始终用户排除。 详见[22](22-connected-permissions-and-reopen-2026-09-10.md)。

## 当前核验事实

| 项目 | 结果及证据范围 |
|---|---|
| 来源 | Contracts db54c617c65db5431b950eb297ba148a43a8e600；Host ccd815ff63542674daa80172a1c71ac7478edd0f；Desktop a5975f48e63d3f1d3a262e9e8dfc57ca0d923961；固定Runtime0.144.6不变 |
| 配置兼容 | 原生CLI配置层、独立精确受管模板、原生trust原字节保留；bootstrap cwd独立于任务cwd。无调用原生集成及当前来源检查通过，详见21 |
| 实际数据 | com.yijie.ai原app-data、日常Host/Codex Home；无数据库或凭据副本；schema15/view2，reader下限25b004fbd5a4dcf642a503d302c21a7d6e3b817f |
| 普通重开 | 修复后旧B两条Tool在canonical重开：342ms成功与0ms拒绝、来源/脱敏保留，正常退出；不是自动续跑证明 |
| 新E成功 | 本轮actual native Prompt批准ASIN/US，Tool completed/414ms，两Turn completed，安全正文partial/content_redacted；最终标题品牌价格与正常退出后的原生thread/read三字段对照PASS |
| 原生拒绝 | 旧B实际decline通过，保留旧提交范围；当前E未重跑decline，不自动继承为当前fresh run |
| 模式切换 | 当前E明确授权后正常停用MCP，auto/full/ask均与持久值一致，trust字节不变；产品实际切换PASS，旧B失败历史保留 |
| UI/相关回归 | 旧B的light/dark、1180×760、200%、键盘/复制、Command/Artifact/附件检查保留当时范围；当前E已核对展开、参数、来源和结果文案 |
| 调用累计 | 元数据12/20；模型7/8；业务2逻辑调用、实际HTTP次数未知、保守扣4/10；图片0 |
| 兼容限制 | 当前MCP启用不自动resume旧线程；旧B新本地投递被拒绝且未调用模型/MCP，记录保留；不猜绑定、不自动封口 |
| 交付 | 产品修复及pin已本地提交；当前证据更新中；未推送、tag、部署或远端CI |

新E详见[连接复验](evidence/connected-config-recheck-2026-09-10.json)，配置与普通重开详见[21](21-native-config-ownership-2026-09-10.md)；20保留历史失败。当前D4保持未关闭，未运行项不写PASS。AC-004继续OWNER_EXCLUDED / NOT RUN；未做攻击、故障注入、强杀或权限破坏。

## 前次连接闭环检查与分离审查（历史）

原生成功证据见[成功摘要](evidence/fixed-runtime-user-agent-success-2026-09-10.json)、[操作8](evidence/sorftime-native-discovery-operation-8-2026-09-10.json)及[固定版本工具schema](evidence/sorftime-product-detail-fixed-schema-2026-09-10.json)。官方资料/只读包审计和原生取样边界见[业务依据复核](evidence/d0-business-basis-review-2026-09-10.json)。

本轮实际检查：文档strict最终PASS；元仓lint、50/50测试、19个已提交需求包审计、7个Shell文件逐个语法检查及diff检查PASS。审计保留5个旧schema v1警告，且其“19包”仅覆盖已提交版本，不冒称覆盖本轮未提交修改；当前FEAT-144工作树另以strict/D0直接检查。strict首轮及后续说明中的相同占位字样被严格检查拒绝，已改为具体缺口说明，未更改状态或放宽检查器。

**前次D0实跑exit1；当时AC-004仍为Must，缺少业务失败方案。该结论保留历史，已由用户当前范围决策解除，不能覆盖本轮新D0结果。** native/v4来源与FEAT-137永久退役检查PASS。实际命令输出见[门禁记录](evidence/d0-closure-checks-2026-09-10.json)；D0不能由诊断成功、文档strict或旧测试PASS代替。

[最终保护检查](evidence/d0-closure-final-workspace-2026-09-10.json)：11仓HEAD/分支/远端不变、10个产品仓干净、无暂存修改、4个来源锁和47项工作树/提交摘要一致、固定Runtime二进制/manifest未变、原四文件历史逐字相等、当前Markdown链接可解析、JSON有效、通用秘密模式无命中。本轮仅元仓文档和证据更新；该通用模式扫描不冒称再次检索用户秘密或数据库。

设计与执行阶段分开的代理审查覆盖原生结果/status/参数、文本块与脱敏、单条未知格式隔离、数据库版本保护，以及可选手工取样不经过模型工具预审批且不产生Tool Item的边界；不声称独立人工批准。必要的新字段设计见[12](12-independent-contract-and-reader-plan-2026-09-10.md)及13。Host/Native展示/SQLCipher的[既有基线](evidence/independent-native-baseline-checks-2026-09-10.json)仅作未来回归依据，不是本轮产品AC通过。

[14](14-bounded-native-business-sample-2026-09-10.md)是业务预算内未启用的备用取样，不作D0必经步骤；元数据与业务不互借。产品实施仍按此前授权边界，当前仅更新需求/预算。

## 操作1–5历史证据和审查范围

原生返回：[操作1](evidence/sorftime-native-discovery-operation-1-2026-09-10.json)、[操作2](evidence/sorftime-native-discovery-operation-2-2026-09-10.json)、[操作3](evidence/sorftime-native-discovery-operation-3-2026-09-10.json)。多条HTTP span进入/退出事件不能多算成请求；完整HTTP尝试数为null。

前3次执行工具只调用固定app-server的initialize/config-read/status-list；操作4/5使用本地应用原生稳定thread/start(ephemeral)、startupStatus/updated与thread/unsubscribe补充启动诊断，没有turn/start或业务tools/call。没有实现MCP HTTP客户端、业务执行器或产品状态机。执行前独立代理审查已检查路径、秘密输入、原生字段、有界读取及正常关闭，并修正debug:null、超限后继续排空和Popen清理边界。恢复后仅定向增加无正文HTTP诊断，当时应用协议由其自带generator离线核验，编排与文档作写入后本地自审；不声称独立人工批准，也不把发现脚本当成产品实现验收。

## 历史结论保留范围

| 阶段 | 原结论及保留位置 |
|---|---|
| 2026-08-30原MCP包 | D0 BLOCKED、8AC pending；[原四文件](history/2026-08-30/02-verification.md)与基线逐字相等 |
| 未实施view_image备选 | 曾通过当时D0/strict、元仓50项测试和19包审计；已被真实Sorftime目标取代，见[历史说明](history/2026-09-10-builtin-proposal/README.md)，不算MCP成功 |
| Sorftime初始文档核验 | strict及元仓检查PASS，D0因安全/schema等BLOCKED；[当时检查](evidence/d0-document-checks-2026-09-10.json)保留，未实际连接 |
| query-only安全审计 | [05](05-d0-preflight-2026-09-10.md)中的日志风险事实保留；Header支持未知和0额度属于当时阶段，已由06/08更新 |
| 5次授权与暂停 | [06](06-header-auth-and-discovery-budget-2026-09-10.md)记录授权口径，[07](07-paused-state-2026-09-10.md)保留当时1/5暂停状态，后续累计8/10，以当前台账为准 |

此前豁免、冷历史/进度缺失及未执行项目均保持原范围；没有复制用户数据库、测试攻击载荷、故障注入或Runtime修改。

## 本次用户范围调整的审查与检查

原AC-004和旧四文件已逐字归档；活动Must由10项改为9项且不重用编号，排除不记PASS。业务失败分支/错误扩展/专用样本已移出设计，原生事实、安全拒绝及通用保护保留。通用D4代表性拒绝仅评价AC-007仍要求的原生权限边界，不能变相计为AC-004业务失败通过。

当前用户直接授权覆盖业务额度和余额决定；按更保守的10次tools/call尝试（含原生重发）分账，不解读为20次业务尝试或模型额度。本轮在文档落地后再自审；未新启子代理，不把前轮分离审查说成本轮独立审查。

适用strict/D0、元仓lint/test、已提交需求包审计、Shell及工作区/来源核验见[本轮实际检查](evidence/owner-scope-d0-checks-2026-09-10.json)。前次50项测试与门禁结果不自动继承。

本轮最终结果：strict/D0均exit0；lint、50/50测试、19个已提交需求包审计（5个历史schema v1警告）、7个Shell逐个语法与diff检查通过。没有新MCP/模型调用，未实施产品或修改全局检查器；适用工作树和来源保护见本轮JSON证据。
