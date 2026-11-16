# FEAT-175 修订 3 完整复审

历史范围说明：本文为实施前审计，实际S1／Q1结果与新增发现以[19](19-s1-q1-implementation.md)为准。原记录不回填为运行证据。

2026-11-15。用户要求把三个前置的实现方式、依赖和验收具体化，并再次完整审查。本文记录本 Codex 在起草后分开进行的复核，不冒充独立人工批准。第一／二版快照、原检查及源码证据均保留。

## 1. 结论与状态

三个前置的**推荐实现设计已定义**，分别见 [15 B01](15-identity-model-readiness.md)、[16 B02](16-expert-policy-implementation.md)、[17 B03](17-native-cancellation-routing-qualification.md)。不再以“后续确定签发方式／角色怎么办／如何验取消”作为实现空白；剩余的是这些设计的接受、基础依赖交付和真实验收。

未修改产品代码、实际契约／SDK、角色文件或环境；没有模型／搜索请求、部署、迁移、重启、提交。所有实施／运行资格仍 NOT RUN，G1／G2／G2V 不因文档检查而自动 PASS。

## 2. 三个前置的闭合方式

| 前置 | 方案确定内容 | 必需交接 | 通过判据 |
| --- | --- | --- | --- |
| B01 | API发行web-only不透明grant；Native主会话owner；300秒TTL、提前60秒续期；typed私有控制；原子claim、查询／取消和30天receipt窗口 | DEP-AUTH／WEB-AUTH／CARRIER／MODEL／CLOUD／DIST 的版本、scope、部署输入和证据 | B1-A1—A8，加新用户真实App资格；缺基础模型服务不能用直接REST替代 |
| B02 | 普通专家inherit；data-analyst-pro现有0.1.0/0.1.1/0.1.2保留disabled；源政策绑定精确版本／role摘要，原ResolveExpert先验证；无名称猜测 | 政策源／生成材料／现有精确资源，必要发行许可；未来联网版本单独审阅 | B2-A1—A7，实际provider/MCP工具表、调用入口和恢复行为一致 |
| B03 | 复用native工具组织、auto/prompt、turn与Item；Host只接IO撤销；nullable审批拒绝猜测；取消与dispatch claim按明确边界判定 | 固定正规Runtime、同源MCP和接口候选、模型资格及独立真实调用额度 | Q1零费用真实协议＋Q2小规模真实路线，再Q3冻结96任务／Q4新用户；所有失败和费用保留 |

实现依赖图为：源契约／现有接口审查 → Q1 → 获准的技术profile Q2 → 服务端与客户端完整接线 → 最终产品profile Q3 → 全部基础依赖就绪后的Q4。Q2可使用已获准本机profile前置，不能冒充公开资格，从而避免等云端完成才开始发现协议不可达的循环。

## 3. 本轮复审新增核对及修正

| 检查项 | 源码事实／潜在错误 | 已采用的设计处理 |
| --- | --- | --- |
| 登录复用 | Native已有OIDC、access/refresh和401恢复；API已有严格Verifier和授权revision | 保留主身份体系，只新增有限网页委派，不另建登录或JWT签名系统 |
| 轮换与撤销 | 若每次换token都取消关联操作，会在正常续期时中断研究；只撤最新token又会遗漏重叠旧token | credential revision不改变turn身份；旧grant最多60秒自然重叠；退出／换租户按binding撤全部grant，已准入操作和新准入分别处理 |
| 公开carrier | loadMarketProfile要求exact local＋demo_fast，不能直接当公开授权 | 显式DEP-CARRIER，复用transport而不复用固定本地身份；旧gate不放宽、单owner reader |
| 原生模型认证 | auth.command／refresh_interval_ms确实存在，但external_bearer含kill_on_drop(true) | 仅记录为DEP-MODEL可复用入口，FEAT-175不启用helper；禁止挂死／强杀资格测试，不以API存在等同可直接激活 |
| 专家底层依赖 | ExpertsEnabled还要求MarketEnabled | 区分市场框架与用户连接器选择；普通builtin-only和合法专家＋空选集分别验证，不强行拆专家系统 |
| 精确角色范围 | 三个数据分析版本限制agent；分镜仅限制校验脚本 | 三版本保留，其他正常专家inherit；角色字节不改；未来联网变体用新版本 |
| 配置组合顺序 | 新自动装配可能覆盖先写的disabled；media helper会重建namespace列表 | 最后一次应用网页限制；namespace集合追加去重；验证实际wire |
| 原生确认关联 | canonical turn_id可空且无通用tool item ID | 当前功能缺turn明确decline，只用原request ID回复，不猜Item关联或最后活跃turn |
| 派发与取消 | 数据库标记不能证明HTTP字节已送达供应商 | 将claim定义为保守派发授权点；之前取消零请求，之后可能计费，不声称exactly-once |
| 过期幂等ID | 只保留有限receipt却接受任意旧UUID会重新收费 | UUIDv7新准入5分钟/未来60秒；30天既有记录先查重，记录过期后旧ID拒绝 |
| 结果丢失 | 未存正文不能凭status重建旧MCP结果 | result_unavailable；无第四轮询MCP工具；不把native已失败Item改成成功 |
| 秘密的生成类型 | 新字段默认Debug／fmt可能暴露token | 源级秘密标记／wrapper和普通合成日志检查，ACK不返回秘密 |
| 费用／预算 | 96任务不等于96 HTTP；原生Token预算不等于人民币 | 各类请求／托管搜索／REST分账，使用原生已有推理预算，真实额度独立批准 |
| 文档时序一致性 | 旧概括要求内部execute前已有派发许可，与新claim顺序冲突 | 统一为ready→内部execute→claim→供应商HTTP；取消界限统一使用claim，不混称真实发送 |
| 分阶段资格 | 若Q1要求全部云端／分发用例完成，会反过来依赖S2—S5 | 明确Q1只计真实原生／本机覆盖；服务端与分发分项保持未通过，最终完整验收单独登记 |
| 机器账本一致性 | 首轮结构检查指出阶段图有环和新增TCONF未绑定不变量 | 按单事件阶段偏序修正，补齐专家／路由不变量及最终验收映射；保留首轮失败，不改治理校验器 |

## 4. 对修订 2 九项发现的复核

| 发现 | 设计覆盖 | 运行状态 |
| --- | --- | --- |
| R2-01 身份传递 | 15 第2、3节与B1-A1/A2/A8 | NOT RUN |
| R2-02 取消传播 | 17 第2、3节与N03/N05/N06 | NOT RUN |
| R2-03 多用户共享状态 | 14 第3节、17 第4节、N07 | NOT RUN |
| R2-04 幂等／恢复 | 15 第4节、B1-A4/A5/A6 | NOT RUN |
| R2-05 离线角色 | 16 的精确政策、版本流程和B2-A1—A7 | NOT RUN |
| R2-06 主模型前置 | DEP-MODEL／CARRIER／DIST与B1-A7 | NOT RUN |
| R2-07 路由评分 | 17 Q2/Q3、首次动作／固定分母／恢复单列 | NOT RUN |
| R2-08 worker生命周期 | 14 第7节、16 第4节、N10 | NOT RUN |
| R2-09 组合预算 | 17 第4节、N03/N04及最终MCP封包测量 | NOT RUN |

## 5. 全面性自检

- 用户结果：默认普通问答native、研究／采集／URL三工具、无额外搜索安装／授权／Key，均有必要工具及端到端用例。
- 原生复用：配置／注册／tool_search／Code Mode／审批／暂停／turn／Item／回灌保持；新状态只属于产品凭据、外部I/O和费用事实。
- 权限：本机capability、产品主会话、网页委派、内部服务身份、上游Key明确分开；模型不能填写这些身份；真实web权限独立于workspace.use。
- 失败：未派发、发送未知、busy、额度、鉴权、无正文、截断、拒绝／取消、正常重开均有状态；不存在自动换Key／换供应商补偿。
- 并发与恢复：每调用独立状态、原子claim、旧ID窗口、账号换代、控制pipe不得等待HTTP；无永久query去重或新Agent队列。
- 兼容：旧角色、绑定、历史和已冻结outbox保持；新操作在冻结前排除退役选集偏好；不降库、不回放旧外部请求。
- 部署：source-first、精确pin、server target、公开carrier、模型基础服务、许可与签名分别交接；本地通过不冒充分发完成。
- 验证安全：只有正常输入／状态／等待／停止；禁止强杀、可执行文件替换、权限破坏、恶意／攻击fixture；不为未执行项制造PASS。

本轮静态复核未再留下未说明处理方式的设计冲突。hosted预检索与自然语言工具选择的实际表现仍是明确的可行性风险，必须由Q2/Q3证明；若不达标按17的停止条件重新审阅，不用文档措辞掩盖。

文档检查、引用、历史快照及产品源保持证据见 references/revision-3-checks.json。实施授权和真实运行资格不在本轮交付范围内。
