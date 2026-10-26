# FEAT-164 S4AA：搜索来源最小修复及安全离线验收

2026-10-27。Owner已批准第53号限定方案。**该修复已实施并通过本轮定向及实际隔离App验收**；新增真实模型HTTP0、合成loopback1。整项FEAT-164仍IN_PROGRESS，不能把这次显示修复当作供应商检索答案正确或日常切换完成。

## 根因与最终改动

共享不透明串规则允许斜杠，整串URL检测把多个普通路径段连成32位以上标识，误删14/20来源。Host只将该规则限定到hostname、每个原始path段解码后的完整值、每个query key/value及fragment；先分原始结构再解码，编码分隔符不成为新边界。全局feat136_redaction.go逐字未变，全文Bearer/敏感名称/JWT/AWS/PEM/控制字符、HTTP(S)、userinfo、host/大小、去重、partial和旧版本降级全部保持。没有域名白名单、Runtime修改、数据库重写、UI产品改动或新依赖。

源语义分类为semantic，整项breaking不变。Contracts说明与25个普通样例先固定，canonical sync再把同源fixture及摘要交给Host；新旧wire/schema/SDK源树全部与ca06d099逐字一致。Host实现后本地提交，Desktop仅更新必要来源锁及显式生成检查pin。Owner段成威的本次批准覆盖该安全适用范围及Host/Desktop消费者本地验证；没有发布tag、远端PR或生产激活。

| 来源 | 本地完整提交 |
|---|---|
| Contracts | `c5d138374c102f1a8a11e328a869ec8f91724efd`（前置说明提交8bb8b584e2453116c0a344c056b952fb477b371e） |
| Host | `4f966e8ea810d5b094d0b797d291955d6c774844` |
| Desktop | `c98eddfafb789520b4939bdca95bf8b27f28b7b6` |
| Runtime | `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a`，沿用r5，core/patch/产物未改 |
| Connectors / Skills | `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` / `595c927ae101d3d31c234f60565041eee0864680`，未改 |

独立工作树为`feat164-s4aa-qualification-20261027`；App SHA `179dbd187220694d4666af5822466572f3b245a911501991cb0194f4308db195`，119包内文件及同构建回执均核验。原日常候选、旧App和用户dirty全部保留，不能将隔离提交混入主工作区或视为日常已切换。

## 实际验证

| 检查 | 结果 |
|---|---|
| Host映射/来源/降级/reader | 7个顶层测试PASS（其中25个同源URL子例）；20条批量→18条，32项及512标题限制保持；race、make lint通过 |
| Contracts | 5项v3/v4 conformance、定向OpenAPI lint、生成与不可变同步检查PASS；所有结构/SDK源树与增量基线一致 |
| Desktop | 19项来源检查、额外native-process不可变检查、6项生成入口测试PASS；ChatProcessPresentation20项PASS |
| canonical App | prepare-only成功；正常启动、实际任务completed、显示18来源及partial；同构建重开仍保留全部结果 |
| 本机实际路径 | 一次K31/max合成Responses含20条公开来源，Runtime两份原生记录均20条；Host/Native SQL视图/UI均18条且顺序/URL不改 |
| 正常关闭 | 两次⌘Q exit0；fixture正常shutdown204/exit0；无项目进程/句柄；四Runtime库两次WAL0/完整副本integrity ok |
| 保存及零补发 | 71表全部旧行hash保留，仅新任务/事实和停止代际追加；重开计数账本逐字不变，新增HTTP0 |

本轮任务`01a17910-bf4e-7142-af4a-04791d73cae1`。原真实搜索持久化6条事实原样保留，不回写历史以伪造修复；当前正常Host thread/read的来源投影由定向reader验证。2条单段长标识仍保守隐藏，不能写成20条全显。UI截图和AX证据见s4aa-offline-source-display，重开见s4aa-offline-source-reopen。

未执行亮暗、键盘/焦点、最小窗口专项（Owner已移除），未执行攻击/进程故障/权限破坏/二进制替身/手工checkpoint/WAL清理。完整全仓make test及发布breaking门禁不冒称通过，旧不适用/禁止用例未运行。

## 失败审计与边界

首次Host检查在测试前因PATH中的Go1.26.4低于go.mod1.26.5而停止；切换到已经安装的固定1.26.5、保持offline后通过，未修改依赖。初次失败与修正结果均保留。

额外Desktop回归28项为27PASS/1FAIL：旧FEAT132测试仍断言schemaVersion3接受、4拒绝，现有生成权威为4。测试、产品实现及validator与54e9618基线逐字相同，故不归因本次URL修复；没有放宽validator或把该失败隐藏。此旧测试迁移属于后续验证债务，**不声明全测试套件通过**。本轮搜索组件、Host旧读者及真实App路径已独立通过。

原真实4次结果已在53补齐：图片输入正确、函数调用及回灌通过；搜索HTTP200/completed/20来源传输通过，但回答未找到当前文档，答案正确性仍INCONCLUSIVE。修复Host的显示层不能改善供应商已经生成的答案，真实资格仍绑定原54e9618/8cd6bcc来源，不自动冒充新Host的再次真实调用。

## 保存与下一步

新增真实HTTP0；累计仍10。四账本相对本修复开始逐字不变，原6行、旧14.188544元预占及新搜索费用14.188544元保守预占保留，29.343192元为估算加预占而非精确账单。原497dirty、6498份活动隔离库之外保护文件均保持；混合memory仅精确暂存本轮段落，FEAT163不混入提交。所有App/fixture/meter已正常停止，无待答UI交接。

下一步从整项需求收口：将本轮显示修复绑定到S4/TCONF04及最终core/业务状态证据，审计并最小修正旧v3测试样例；将新Host来源用于日常候选的prepare-only资格，再形成可审阅的真实日常数据切换清单。日常数据库打开/迁移/激活仍未授权，本轮不执行；真实搜索内容质量保留独立缺口，禁止用合成通过替代。无需重跑已经无变化且通过的普通42/旧Runtime验收组。Runtime核心或补丁新范围仍须先提交方案，全部操作继续仅本地、不推送。

原始审计目录`feat164-s4aa-audit-20261027`保留构建、失败、完整私有副本和工具；仓库证据只保存脱敏检查、公开样例/UI和摘要，不提交数据库/密钥。来源与最终核对见evidence/s4aa-final-audit.json及evidence/s4aa-source-binding.json。
