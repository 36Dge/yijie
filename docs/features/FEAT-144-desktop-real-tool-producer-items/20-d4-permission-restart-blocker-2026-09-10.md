# FEAT-144 实际 D4 结果与权限重启阻塞

2026-09-10。本记录覆盖19的待执行状态。真实查询、原生参数批准/拒绝、返回值核对与部分UI检查已完成；**D4未通过，需求保持active**。AC-004始终为OWNER_EXCLUDED / NOT RUN。

## 本次执行结果

用户已当场授权仅在FEAT144-D4-B验证任务中临时切换自动/完全访问并恢复请求批准，期间不发任务。点击“帮我批准”后，旧Runtime PID 51713正常退出，Host的后续启动失败，`/v1/status`返回`provider_config_failed`、ready=false。界面提示权限同步失败，仍为“请求批准”；SQLCipher只读核对确认该任务持久mode仍为ask，没有auto/full落库。

因此未继续点击完全访问，也没有通过API改模式。此次失败关闭路径保持了权限，但不能当作正常停用/重启验收通过。随后用Cmd-Q正常退出应用，canonical进程exit0；Desktop 48617、Host 51711及原Runtime均已退出。计数器正常Ctrl-C退出0，无强杀。

## 根因证据与边界

受管`config.toml`出现两个原生`projects.<path>.trust_level=trusted`条目，其中一个对应实际D4独立项目。只读比较生成模板与实际配置，归一化模板中的model_catalog_json目录后，除projects外所有TOML字段一致；实际文件SHA-256为`ab41ac0422cf53ef2c1ea277af415c17cb8160146565293fdeed0f471d4e96b5`。未删除、忽略或改写这些条目。

固定Runtime对应源码的`app-server/src/request_processors/thread_processor.rs`中，thread_start_task在显式cwd、尚无trust_level且请求/有效权限信任项目时，调用原生`set_project_trust_level`并重载配置。Host的`prepareMcpPermissionScope`正常Shutdown后调用Start；`prepareMiniMaxCodexHomeForAuthority`通过`preflightManagedFile`只接受精确受管模板。新增projects使重启前置校验拒绝覆盖。配置差异、源码条件与真实failure_code相互支持这一原因；没有读取或输出原始敏感异常来代替证据。

这是**受管配置与Codex原生可写信任状态的所有权冲突**，不是Sorftime HTTP400复发，也不是Git消费者pin漂移。启动前的Git来源/摘要门禁与运行后CODEX_HOME配置门禁是不同检查。不得把projects从比较中剔除来放行，不得删除用户原生信任记录，不得默认信任所有目录、换CODEX_HOME掩盖日常重开问题或修改Runtime。

## 已完成的独立结果与保存核对

正常退出后，使用同一固定Runtime的initialize、config/read和thread/read(includeTurns=true)做本地只读诊断；显式禁用MCP，没有thread/start/resume、工具列举、模型Turn、rollout解析或业务调用。第一次确认公开字段，第二次补充JSON路径以区分`/doc`说明和`/data`实际值；两次均正常EOF exit0、stderr为空。

原生成功Item的`/data/title`、`/data/brand`、`/data/price`与模型最终回答一致；USD由返回的`/doc/price`说明提供。仓库仅记录字段路径、匹配布尔值和摘要，不保存完整业务响应。成功Item仍completed/342ms；第二个被用户拒绝的Item仍failed/0ms/result=null，两个Turn均completed。

SQLCipher原库只读核对：schema15、两条view的format_version=2/source=native_observed，三个outbox操作均done，两个Turn原生绑定及completed仍在，任务权限ask。此项证明数据已保存，不代替普通应用重开。受管配置门禁失败后，依照用户停止条件不再重试canonical；Tool正常重开仍未验证。

## 活动AC结论

| AC | 本轮结果 | 依据或缺口 |
|---|---|---|
| AC-001 | PASS | 真实单工具schema/配置、Composer、实际ASIN/US审批与独立预算已核对 |
| AC-002 | PASS | 原生McpToolCall真实完成；身份、342ms和完整替换定向检查 |
| AC-003 | PASS | 原生/data三字段与模型回答匹配；文本整体脱敏、partial与completed分离；空/缺失/容量定向检查见16/17 |
| AC-005 | PASS | 两个Item与Turn独立；切换、终态、缺记录不busy；定向检查与原生历史一致 |
| AC-006 | pending | SQLCipher与原生thread/read已核对；普通应用的Tool历史重开被配置门禁阻断 |
| AC-007 | fail | 实际Prompt批准/拒绝通过，权限失败时仍ask；正常停用后重启未完成，auto/full成功路径未运行 |
| AC-008 | fail | 启动/切换/旧Command、Artifact/附件/UI检查通过；新增MCP记录后的正常重启未完成 |
| AC-009 | PASS | Contracts→reader→writer及真实来源已固定；schema15、未知格式隔离/方向验证见17/18 |
| AC-010 | PASS | 原生连接/审批/调用/history与唯一缓冲、SQLCipher复用；删除/兼容及分离阶段自审见16/17 |

PASS只适用于本轮明确证据，不代表整体验收或发布。原生Prompt拒绝只算权限回归，绝不替代已排除的AC-004。配置兼容修复后应重新审查受影响AC并进行fresh run，不能自动继承本表。

## 下一步与停止条件

先审定Host受管配置与Runtime原生项目trust写入的兼容方案。优先核对固定Runtime支持的配置分层/内存覆盖能力，保持项目授权范围、既有trust语义、精确安全配置及原生事实权威；没有来源证明时不猜项目根目录、不造trust映射。若固定版本无法分离，明确提出受管文件所有权/兼容方案审查，不能将任意projects作为额外允许字段。

先以无密钥、无MCP线程的正常本地配置生命周期验证方案，再实施必要Host薄适配和针对性回归。只有真实源码内容变化才更新Host完整commit及Desktop pin。当前受管配置保留原样，未重跑已知失败入口。修复后先恢复普通canonical重开；需要重新连接Sorftime验证停用时另取明确元数据额度，现有10次已用尽。已有业务和模型剩余额度不转为元数据额度，不重用当前任务临时UI授权作为未来无限权限授权。

## 来源、预算与限制

Contracts `db54c617c65db5431b950eb297ba148a43a8e600`；Host `635846f72ef4b0d940798215e7b79d58aed6c591`；Desktop `95afd425fd5b55ada9f13b43421ad2c06830dc5c`；最低reader `25b004fbd5a4dcf642a503d302c21a7d6e3b817f`；Codex `6c1ad767f0997845b8258a1c452fd4eb7577579f`未修改。本次阻塞诊断不修改产品源码、来源锁或权限配置。仅本地提交验收文档，不推送/tag/部署。

模型4/8，均计数器HTTP200；元数据10/10；业务1次逻辑调用，HTTP尝试精确数未观测，按原生重发上界保守扣2/10；图片0。此次权限操作及本地历史诊断新增网络调用0。各进程已正常结束，没有等待输入。

保留整体结果文本脱敏、缺phase/plan/reasoning/progress/outputSchema/annotations、冷历史itemsComplete=false、Command完成后输出、旧附件过期/清理未完成/隔离Host映射不全，以及首个仓内验证目录被未知workspace配置拒绝后的本地等待提交记录。没有用这些限制伪造成功、重建历史或自动封口。

机器证据见[实际阻塞与核对](evidence/d4-permission-restart-blocker-2026-09-10.json)，前序实施/真实证据见16–19。[本次最终检查](evidence/d4-checkpoint-checks-2026-09-10.json)记录strict/D0通过、50项元仓测试通过及源码检查通过；D4实跑exit1，仅保留真实未满足项，不以文档结构PASS代替D4。
