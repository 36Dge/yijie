# FEAT-164 实施计划与当前门禁

> 当前S1（2026-10-25）：源实现、local/boundary及canonical构建已完成；本机新Kimi正控通过，暂停/MiniMax/重开及最终清理因Mac锁屏未完成，S1 G3不放行。新增真实模型HTTP为0，旧账本逐字保持。最新来源、未执行项和续办见[21](21-s1-implementation.md)。下方20及更早阶段结论按原来源和时间保留。

## 当前有效状态（2026-10-25，30元单次续验）

| 项目 | 当前结论 |
|---|---|
| 来源与工程门禁 | Runtime r2 / Contracts / Host固定；Desktop40908c7独立固化；G2A及当前Harness PASS |
| 真实G2V | 本次新增唯一HTTP200，正确答复42、usage/保存/重开/无补发/正常清理及组合oracle PASS；r1 FAIL保留 |
| 预算与请求 | 累计30元；仅新增1HTTP已耗尽。旧预占14.188544元＋本次保守0.139590元＝14.328134元；不再新增请求 |
| 已通过历史 | r2 canonical实际App本机合成答复、保存、重开、正常退出；不等于真实模型通过 |
| 尚未完成 | S1—S4、TCONF-164-01—04及三个final；不放行日常库迁移或发布 |
| Git | 仅FEAT-164本地提交已获授权，不推送；保留其它需求改动 |

本轮权威为[20 单次续验](20-budget-resume-and-g2v.md)、feature.yaml和追加后的真实账本。13—19按各自时间与来源保留历史语义。TCONF-164-01—04仍为计划目标，执行前核实selector存在且测试命中数非零。

## 门禁和技术依赖

G0/G1/G2审阅 → 实际业务契约源与适用G2A → 安全Harness资格 → 最小G2V → S1 → S2 → S3 → S4 → 三项final E2E/G4。G5/G6仍受local exposure及独立发布批准约束。

G2前不进行产品实施。G2/G2A之后允许的只是受限契约/垂直候选，不授权大规模分层实现。Runtime权威例外必须保留：最小Runtime候选先产生自己的canonical来源，Contracts随后投影；不能为满足业务Contract First伪造尚不存在的Runtime digest。该候选只用于资格验证，不能提前替换日常App。

## 切片

| Slice | 行为/AC | 未来改动仓库 | 前置 | required证据/回退 |
|---|---|---|---|---|
| S1 | 新活动身份、受管配置、独立候选/激活与退役准入骨架；AC001/002/007 | Contracts/Runtime/Host/Desktop | G2/G2A/G2V | local+boundary+vertical，TCONF-164-01；未激活时保持旧环境，不覆盖旧binary |
| S2 | reader/三表/Host状态迁移、模型选择与显式恢复、普通/市场never-sent安全取消；AC003/004/005 | Contracts/Host/Desktop | S1 | 同上，TCONF-164-02；兼容reader保持，无降库 |
| S3 | worker接管前保护、计划领域退役/重新授权及历史run；AC005/006 | Contracts/Host/Desktop | S2 | 同上，TCONF-164-03；暂停新派发、保留原run恢复 |
| S4 | 全实际调用面、UI、同源打包、正常退出/重开/兼容回退；AC007—010及全部回归 | Runtime/Contracts/Host/Desktop；Connectors回归 | S3 | 同上，TCONF-164-04及三个final独立判定；单独关新Kimi，MiniMax/历史可用 |

每片status=pending，commits为空，所有local/boundary/vertical=NOT RUN。源实现以本包职责为限，不混入FEAT-162/163补救、无关重构或旧证据批量改名。

## 具体序列

1. 再读本轮授权、各仓规则、dirty基线；范围和版本审阅后固定source-first依赖及全部consumer。
2. 权威模型源实现三层身份及版本兼容，刷新全部引用的生成物/validator/来源锁；不是手改派生物。
3. canonical最小Runtime修订及独立路径/manifest，验证旧input-only权威和当前web-sources schema；更新实际launcher路径与所有pins。
4. 完成兼容reader/版本握手和停派发能力，不让新Host启动时隐式激活；受管双文件过渡组合精确识别。
5. 先用普通合成旧库验证表约束、数据和恢复。日常迁移前必须有可读新旧数据的回退构建与明确操作许可。
6. 经正常应用流程收敛所有旧主聊/标题/审核/草案/子代理，确认无受管在途；不强杀，不启动旁路模型。
7. 在worker接管前迁移schema/分类旧身份/装准入；计划通过领域事务暂停撤授权。unknown保留，未结清不得派发。
8. 明确cutover；新聊天/标题等新任务允许新model，旧会话首次继续先完成新模型选择operation；旧计划保存后重新授权。
9. 按独立预算运行获准的真实验收，检查出站/流式/历史/计划/恢复；失败回滚到兼容组合或前向修复。

## 来源冻结及Git

Runtime → Contracts runtime projection → Host runtime constants/candidate → Desktop实际功能组合选择的artifact-media / experts / chat-model Host build candidate → canonical打包/运行receipt。模型业务源与consumer生成先完成；最终freeze必须绑定当前所有启用契约/专家/资源来源，覆盖experts=true且artifact_media=false的独立分支。

用户已授权仅本地固化FEAT-164及必要验证治理记录；按专属路径/差异逐仓提交，不混入FEAT-162/163。不新建branch、PR、推送、tag或发布；构建从固定提交的干净资格工作树产生。实际SHA产出后登记。

## 证据失效与停止

每个G3单片评定，commits覆盖自身和transitive前置，contract/fixture/harness/platform/bootstrap引用精确。任一变化使相关证据STALE。三次等价失败按fingerprint累计，进入append-only RCA，收敛唯一下一动作后才可在授权下重试；禁止第四次机械尝试。

设计变更回跳01/03，契约与语义回04/04A，数据/恢复回05，验证阈值回06。当前方案与实施已获Owner确认；G2A、当前Harness及预算受限文本G2V已通过。判定与预算恢复、本次唯一真实请求及正常重开已完成；S1—S4仍须逐片实施和新鲜证据，不能借用本次通过。后续代码改变使相应来源证据过期，追加真实模型请求须另有明确额度。
