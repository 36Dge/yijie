# FEAT-144 — 当前实施与验收记录

2026-09-10；当前权威为[20实际D4与权限重启阻塞](20-d4-permission-restart-blocker-2026-09-10.md)。产品已实施并本地提交，真实Sorftime成功调用和原生Prompt正常拒绝完成；D4为FAIL/未关闭，不能写成未运行全部业务，也不能写成整体PASS。AC-004为用户排除，不实现、不验证、不算PASS。

## 当前事实

| 项目 | 结果 |
|---|---|
| 固定Runtime | 0.144.6不变，Bearer环境引用、无query URL、真实版本User-Agent；原生调用已验证 |
| 实际来源 | Contracts db54c617c65db5431b950eb297ba148a43a8e600；Host 635846f72ef4b0d940798215e7b79d58aed6c591；Desktop 95afd425fd5b55ada9f13b43421ad2c06830dc5c |
| reader/存储 | 最低reader 25b004fbd5a4dcf642a503d302c21a7d6e3b817f先提交；实际schema15、view格式2，旧JSON不改写 |
| canonical范围 | 普通com.yijie.ai、现有app-data、日常Host Home、独立合成项目；真实查询及旧Command/Artifact/附件兼容展示已检查 |
| 真实成功 | product_detail单ASIN/US，原生completed/342ms；thread/read的/data标题、品牌、价格匹配模型回答 |
| 安全展示 | 实际结果文本整体脱敏，availability=partial，与completed分开；卡片可复制脱敏文本，无活动链接 |
| 原生拒绝 | 同一线程第二次Prompt正常拒绝，failed/0ms/result=null，Turn completed；没有第二次业务调用；只算权限回归 |
| 权限模式 | 用户已授权本次临时切换；请求auto后旧Runtime正常退出，新Runtime因受管config出现原生projects而拒绝启动；ask保持，full未尝试 |
| 正常重开 | Tool数据已保存且原生历史可读；普通应用Tool重开因上述门禁未运行，不能由只读SQLCipher检查代替 |
| UI | light/dark、1180×760、200%、键盘展开、安全复制和会话切换已检查；恢复浅色及100% |
| 调用 | 元数据10/10、模型4/8、业务1逻辑调用按原生重发上界扣2/10尝试、图片0；HTTP业务精确次数未知 |
| 清理 | App/Host/Runtime及计数器正常退出；没有强杀、复制数据库/凭据或改写受管配置 |
| AC/D4 | AC-001/002/003/005/009/010 PASS；AC-006已在21的普通canonical重开中PASS；AC-007/008保留失败历史，当前实际连接后的切换尚未完成；AC-004排除；D4未通过 |
| 交付 | 产品及来源已本地提交，当前验收文档另行本地提交；未推送/tag/部署，未触发远端CI |

## 本轮证据与未运行范围

[16实施](16-native-implementation-2026-09-10.md)、[17分离阶段自审](17-implementation-review-and-precommit-2026-09-10.md)、[18来源与修复历程](18-committed-sources-and-d4-2026-09-10.md)、[19真实D4过程](19-real-d4-progress-2026-09-10.md)、[20当前阻塞](20-d4-permission-restart-blocker-2026-09-10.md)。原有安全定向测试、来源锁及实际生成证据保持各自提交和日期，不把历史测试数量继承为新fresh run。

首次有效配置序列化和Sorftime旧历史逐个resume问题已修复并提交；此次项目trust/模板冲突尚未修复。Git源码pin通过不代表运行后CODEX_HOME配置通过。auto/full成功路径和普通Tool重开未运行；不得删除projects、忽略漂移、换空Home或缩小断言伪造通过。AC-004、既有攻击/故障注入豁免保持原状态。完整业务返回不入版本库，字段对照仅存路径、匹配值摘要。

最终结构/D0与D4实际门禁结果记录于当前检查证据；文档结构通过不证明真实生命周期可用。

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

当前续办授权：用户另增10次原生元数据操作，累计10/20、本轮新增0；兼容修复按[21](21-native-config-ownership-2026-09-10.md)推进。固定Runtime原生CLI分层与Host无调用集成证明已通过，TOML依赖已获明确授权，Host修复及Desktop真实pin已本地提交；现正验证普通canonical，历史D4失败结论保留。

当前运行检查点：Host配置兼容与初始化cwd修复已固定来源，普通Tool历史重开通过；Sorftime标准构建已完成并停在用户隐藏输入框，模型计数器保持4/8，元数据10/20、业务保守2/10、图片0。实际连接后的停用与权限切换完成前不关闭D4。
