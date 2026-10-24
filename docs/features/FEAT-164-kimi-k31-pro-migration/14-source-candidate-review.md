# FEAT-164 源候选审计与G2A评审材料

> 2026-10-25 当前进度：原隔离清单三仓已本地提交，G2A PASS；Host/Desktop 最小候选及普通本机联调完成，G2V、S1—S4/final 仍 pending。当前证据和续办边界以 [16 下游候选审计](16-downstream-candidate-audit.md) 与 feature.yaml 为准；以下早期阶段记录保留其历史含义。

本报告是Codex在源实现完成后进行的结构化复核，不是独立人工评审，也不是G2A或产品交付批准。Owner为段成威；实现授权来自当前用户明确确认方案和开始实施的指令。

## 实际变更与边界

| 仓库/源 | 本阶段结果 | 下游含义 |
|---|---|---|
| Contracts model-selection-v2、chat-models-v2 0.2.0 | 新活动profile为kimi-k3-1-pro-max-v1，wire model为kimi-k3.1-pro；MiniMax保持；v1源不改 | `/v2/model-chat`独立协商；旧consumer不能直接收到新身份 |
| Contracts snapshot/receipt/recover | 历史v1请求和成功结果直接引用v1权威；当前Selection与原回执分离；新选择/recover目标只接受活动身份 | 仍需Host实现session/op/digest/revision一致性、全部busy条件以及相同目标恢复；不是凭类型解码就安全 |
| Runtime0007 | 构造Responses请求前拒绝旧slug；仅新slug搜索请求追加真实sources；保留auto和SSE终态参数修复 | 涵盖使用此构造器的普通/辅助Responses及compact；不是全局provider开关 |
| Runtime独立构建与Contracts投影 | kimi-k31-pro-r1，269 schema与旧web-sources相同，真实binary/hash可核验 | 不修改日常launcher，不替代G2A不可变commit，也不允许只改Host pin就激活 |

## 审计发现与处置

1. **已修复：原回执版本被改变。** 最初result只引用v2 Selection；现在SelectionResultSnapshot明确保留v1/v2原版本，并拒绝版本混配。旧成功回执不加availability，不冒充当前Selection；Node与Rust普通往返覆盖。
2. **已修复：错误与可用性契约不闭合。** 目录available/reason一致；转发路由保留原业务错误，并显式声明准入400/409/503的v2 Error。
3. **已修复：生成与来源完整性。** generator拒绝重复枚举/生成符号碰撞；离线bundle覆盖本仓canonical依赖和discriminator；来源锁记录实际依赖hash。SDK仍不是完整业务validator，跨字段/常量须继续schema conformance。
4. **保留边界：Runtime并非所有API总开关。** `summarize_memories`和realtime不经过Responses构造器；本需求不启用这些表面，当前受管market明确memories=false。将来若实际启用或存在override，必须在cutover前重新审计/准入，不能用这3项请求构造测试宣称这些路径已覆盖。旧线程previous_model、已加载子代理、Guardian/标题仍由后续Host/Native门禁和真实调用面验证闭合。
5. **保留边界：Source-first尚未闭合为下游资格。** 未新增Host handler或Desktop DTO/SQL；市场/专家/计划等后续引用族必须先做各自源契约版本化及相应检查，不能把本模型family的结果外推。
6. **工作树与制品保护。** 新文件与共享Makefile/支持基线/项目记忆的FEAT-164局部段落可独立审查。旧0001—0006与input-only/web-sources binary摘要匹配；上游源码原样。所有既有FEAT-162/163修改不纳入本轮源候选提交。

## 基线解析失败RCA

原`check-breaking.sh`在35e0949c、54be9314、bedf4159三个基线出现相同checkpoint的exit102；停止原入口重试。日志共同定位scheduled-plan-draft对canonical schema URL的解析，尚未进入该族差异判定。候选原因：契约真的删除/不兼容、来源文件缺失、URL标识符被当成下载地址。

区分证据：三个基线都含匹配`$id`的本仓JSON Schema；旧入口只archive openapi且未登记canonical URL到本地schema。新独立比较工具对baseline/current分别取本仓源，仅在临时副本翻译引用位置，不改变type/enum/required/default/additionalProperties，不略过scheduled。7基线的全部既有OpenAPI及原Protobuf/AsyncAPI/JSON Schema检查通过，结果和原失败同时保留。结论是比较器来源解析问题，不能把原入口失败称产品协议不兼容，也不能把替代结果称原入口PASS。

该替代入口已完成工程实现和安全限定验证。机器台账保留原三次失败及RCA材料，尚未伪填Owner对RCA/Consumer语义diff的最终批准；本次G2A评审需明确接受离线等价检查并关闭这一门禁事件。

## 提交与后续门禁

当前请求审阅的对象是实际源候选及08证据，不再次请求“是否开始实施”。所需下一授权为：批准本报告的模型v2方向兼容/历史语义及离线比较结论，并允许按隔离清单进行FEAT-164本地提交，先Runtime，再刷新Contracts来源并提交，最后治理材料。无push、tag、分支、发布，不将已有FEAT-162/163变更混入。

[隔离提交清单](evidence/commit-scope.json)逐文件记录本轮6个Runtime文件、19个Contracts文件及两个共享文件的限定段落；元仓仅FEAT-164材料和对应记忆段。该清单是审阅材料，没有stage或commit；当前base HEAD不是新增实现SHA。

原因是元仓AGENTS.md明确“不自动commit、push、创建分支……除非用户明确要求”；production_hardened的QUALITY_GATES.md G2A要求候选完整commit/digest、Consumer评审及下游不可变引用，并写明未满足时“不得开始或合并下游候选实现”。当前实施授权允许准备源码和可审阅证据，但没有明确Git动作许可。

之后仍须最小安全Harness资格/G2V，再依次实现S1—S4。真实模型预算和用户日常库/应用激活是后续具体候选具备资格时的操作边界，当前没有提前申请或消耗。整体未完成、所有Must AC保持pending。
