# FEAT-164 续办入口

> 2026-10-25 用户已明确恢复，沿用 20 元及搜索/图片授权。当前进度与预算边界见 [18 恢复实施记录](18-resumed-g2v.md)；17 保留暂停时历史状态。G2V 尚未通过。

> 2026-10-25 当前进度：原隔离清单三仓已本地提交，G2A PASS；Host/Desktop 最小候选及普通本机联调完成，G2V、S1—S4/final 仍 pending。当前证据和续办边界以 [16 下游候选审计](16-downstream-candidate-audit.md) 与 feature.yaml 为准；以下早期阶段记录保留其历史含义。

> 实施授权更新：Owner现已确认FEAT-164方案并要求开始实施和审计验证。此前“仅文档”段落是上一轮历史边界；当前状态以feature.yaml及13-implementation-log.md为准。G0/G1/G2记录本次方案确认；G2A/G2V及产品完成门禁仍未通过。无新增Git/付费/日常库激活许可。

当前feature=active，源候选已实施并完成安全限定验证；G0/G1/G2 pass，G2A/G2V及S1—S4 pending，整体产品verification=NOT RUN。先读13/14和08的最新证据。

先读00/11/03，再读04/04A/05/07。初版dev文档只作背景，本包修正优先。不得复用FEAT-162/163许可、额度、进程或验收结果。

下一步审阅14中的实际源候选与离线比较RCA，取得仅FEAT-164源候选的本地提交许可；Runtime先固化，再刷新Contracts来源并固化。G2A通过后才实现最小Harness/G2V候选。现有实施授权持续有效；付费、日常用户库迁移、App激活和发布另按范围核对。

必须保留：

1. 加固治理不改local/demo_fast应用环境或扩张ADR-0018。
2. reader/迁移/退役准入须在worker接管前完成，claim/send均检查；只读查询不禁。
3. 普通never-sent取消非现成机制，不删chat；原operation/profile/payload/digest不改，合法状态变化单独记录。
4. 旧线程先做选择新目标操作再turn；status/config不能证明模型；unknown明确恢复是重新resume配置写入。
5. missing不是never-sent，unknown不允许用新提交绕过；无法安全恢复则可读但不可继续，限制必须可见。
6. 三表扩约束不改旧migration；计划用领域事务暂停/撤授权，历史run/grant不改。
7. previous_model压缩、已加载子代理、role/override、Guardian和并行标题纳入截止点；禁用能力不为验收开启。
8. 保留0001—0006，新0007及独立Runtime目录、实际artifact-media候选和所有传递锁一起freeze；旧binary留存不等于新Host接纳它。
9. 新源候选检查与真实端到端资格分开；尚未创建的TCONF不得空跑标PASS。所有真实模型验收须本Feature预算和证据。

阻断BL-01—07见03。证据与文档检查见08/evidence；本任务无服务需要启动或停止。
