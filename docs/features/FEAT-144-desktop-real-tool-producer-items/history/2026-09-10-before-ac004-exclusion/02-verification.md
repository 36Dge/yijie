# FEAT-144 — 当前 D0 核验记录

2026-09-10。**固定Runtime原生元数据连接阻塞已关闭；D0仍BLOCKED，产品实现/canonical/D4均NOT RUN。** 当前权威为[13](13-connection-closure-and-d0-review-2026-09-10.md)，调用以[共用台账](evidence/sorftime-discovery-ledger-2026-09-10.json)为准。

## 当前事实

| 项目 | 结果 |
|---|---|
| 固定Runtime原生接入 | 操作7：0.144.6 starting→ready；操作8：返回97工具，Sorftime MCP1.1.6 |
| 已验证配置 | 无query HTTPS URL、原生Bearer环境引用、真实User-Agent codex-mcp-client/0.144.6；二进制不变 |
| 历史失败与结论边界 | 操作6 initialize HTTP400/request error原样保留；真实UA配置修正有效，不声称已证明服务端唯一拒绝规则 |
| 工具/inputSchema | product_detail、asin必填、amz_site枚举含US/default Unknow；当前来源为固定Runtime操作8，与操作5一致；未证明完整工具目录 |
| 调用台账 | 8/10次元数据操作，剩余2；本轮文档收尾新增0；模型/业务/图片均0 |
| HTTP计数 | 操作7/8的6 POST span是同一进程共享摘要，不相加为12；完整底层HTTP尝试数未知 |
| 正常退出及秘密 | 正常unsubscribe/stdio EOF exit0；新目录和stdout/stderr秘密精确值扫描无命中；无等待输入/存留Runtime，不证明未来模型环境隔离 |
| 入口与范围 | 仅隔离原生app-server空临时线程；没有turn/start、yijie应用启动或永久MCP配置；不是业务或D4 |
| 展示设计 | 原生文本块及索引、有界纯文本和既有脱敏；不依赖缺失的outputSchema，不猜商品字段/原生终态 |
| 安全/审批/兼容 | 内存秘密+exclude/set检查；原生elicitation实际参数呈现；reader先行、单条recordDiagnostics隔离、高数据库版本拒绝及回滚边界；均待产品实施验证 |
| 剩余业务依据 | 当前账户计费/重试扣费与可安全执行的正常业务失败条件未明确；不承诺幂等，不套用API/CLI价格；空结果不能代替failed |
| D0/Must/D4 | D0 BLOCKED、product_ux pending、十项Must pending；连接、缺失outputSchema/annotations/progress、未编码或未运行D4不再列作D0阻塞 |
| 来源与交付 | 11仓来源、47锁定摘要及Desktop并发内容保护；仅元仓文档/证据修改，产品仓与pin不改；未提交/推送/tag/部署/触发CI |

## 本轮检查与分离审查

原生成功证据见[成功摘要](evidence/fixed-runtime-user-agent-success-2026-09-10.json)、[操作8](evidence/sorftime-native-discovery-operation-8-2026-09-10.json)及[固定版本工具schema](evidence/sorftime-product-detail-fixed-schema-2026-09-10.json)。官方资料/只读包审计和原生取样边界见[业务依据复核](evidence/d0-business-basis-review-2026-09-10.json)。

本轮实际检查：文档strict最终PASS；元仓lint、50/50测试、19个已提交需求包审计、7个Shell文件逐个语法检查及diff检查PASS。审计保留5个旧schema v1警告，且其“19包”仅覆盖已提交版本，不冒称覆盖本轮未提交修改；当前FEAT-144工作树另以strict/D0直接检查。strict首轮及后续说明中的相同占位字样被严格检查拒绝，已改为具体缺口说明，未更改状态或放宽检查器。

**D0实跑exit1，机器输出为product_ux.status必须PASS；实际保留pending的依据为AC-004缺少可执行的安全普通失败方案。** native/v4来源与FEAT-137永久退役检查PASS。实际命令输出见[门禁记录](evidence/d0-closure-checks-2026-09-10.json)；D0不能由诊断成功、文档strict或旧测试PASS代替。

[最终保护检查](evidence/d0-closure-final-workspace-2026-09-10.json)：11仓HEAD/分支/远端不变、10个产品仓干净、无暂存修改、4个来源锁和47项工作树/提交摘要一致、固定Runtime二进制/manifest未变、原四文件历史逐字相等、当前Markdown链接可解析、JSON有效、通用秘密模式无命中。本轮仅元仓文档和证据更新；该通用模式扫描不冒称再次检索用户秘密或数据库。

设计与执行阶段分开的代理审查覆盖原生结果/status/参数、文本块与脱敏、单条未知格式隔离、数据库版本保护，以及可选手工取样不经过模型工具预审批且不产生Tool Item的边界；不声称独立人工批准。必要的新字段设计见[12](12-independent-contract-and-reader-plan-2026-09-10.md)及13。Host/Native展示/SQLCipher的[既有基线](evidence/independent-native-baseline-checks-2026-09-10.json)仅作未来回归依据，不是本轮产品AC通过。

[14](14-bounded-native-business-sample-2026-09-10.md)仅为具体可审查的取样提案，NOT AUTHORIZED/NOT RUN；一次取样不能解决账户计费规则或保证找到自然失败。元数据剩余额度不能转作业务预算。D0通过且另获实施授权后才能编码。

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
