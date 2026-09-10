# FEAT-144 — 当前实施与验收记录

当前本地D4保持PASS，九项活动Must满足、AC-004始终用户排除。获本次明确授权后，22个提交已按Contracts→Host→Desktop→元仓普通推送，逐仓远端SHA一致；CI均未触发，NOT RUN。累计文本9/13、元数据14/20、业务2逻辑调用保守扣4/10、图片0，本次新增0。实际来源与远端结果见[26](26-remote-delivery-2026-09-11.md)；本次新增结果记录仅本地提交，不超出22个提交追加推送。

## 当前核验事实

最终逐项AC、三仓完整来源、兼容/回滚边界、分账与限制见[24最终报告](24-final-native-decline-and-delivery-2026-09-11.md)；[F原生终态及正常重开证据](evidence/native-decline-final-2026-09-11.json)保存真实ID和无正文核验。

- 当前最终来源为Contracts811f38d6、Host0e47766f、Desktop7abf89e8；Runtime0.144.6未改。
- F实际原生Prompt拒绝、rejected、Tool failed/0ms/resultnull、Turn completed；没有追加业务调用。普通重开保持来源与ask，旧审批不恢复。
- E成功/数据对照/三模式检查保留真实旧提交，十二相关行为文件逐字未变证明适用；最终来源实际重开E历史。不能称所有检查在同一提交或进程实跑。
- 旧B queued/failed出站及无原生Turn的执行不确定性保持；原生当前notLoaded不推导过去终态。无数据库或凭据副本。
- 九项活动Must完成；AC-004 OWNER_EXCLUDED / NOT RUN。禁止的攻击/故障/强杀测试未执行，不计PASS。最终门禁输出单独保存。

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

## 用户范围调整阶段的审查与检查（历史）

原AC-004和旧四文件已逐字归档；活动Must由10项改为9项且不重用编号，排除不记PASS。业务失败分支/错误扩展/专用样本已移出设计，原生事实、安全拒绝及通用保护保留。通用D4代表性拒绝仅评价AC-007仍要求的原生权限边界，不能变相计为AC-004业务失败通过。

当前用户直接授权覆盖业务额度和余额决定；按更保守的10次tools/call尝试（含原生重发）分账，不解读为20次业务尝试或模型额度。本轮在文档落地后再自审；未新启子代理，不把前轮分离审查说成本轮独立审查。

适用strict/D0、元仓lint/test、已提交需求包审计、Shell及工作区/来源核验见[本轮实际检查](evidence/owner-scope-d0-checks-2026-09-10.json)。前次50项测试与门禁结果不自动继承。

本轮最终结果：strict/D0均exit0；lint、50/50测试、19个已提交需求包审计（5个历史schema v1警告）、7个Shell逐个语法与diff检查通过。没有新MCP/模型调用，未实施产品或修改全局检查器；适用工作树和来源保护见本轮JSON证据。
