# production_hardened Production Readiness

> 仅适用于生产激活。公开 Demo 的最小检查见 `public-demo-readiness.md`，DP 不替代 G5/G6。

## 发布候选

- [ ] 每个制品有 version/tag、完整 commit、digest 和来源
- [ ] 制品从干净、不可变、可复现的 source 构建
- [ ] Contract、Runtime、模型、Skill、Knowledge 和 migration 版本组合已固定
- [ ] core vertical、accessibility/visual、teardown 三项最终 E2E evidence 均绑定当前制品/平台/harness，且仍 fresh
- [ ] SBOM/provenance、依赖和许可证按组织要求完成
- [ ] 配置、secret、权限和容量已经在目标环境确认

## 发布与数据

- [ ] 合并、部署、migration、启用和清理顺序分别列明
- [ ] Feature Flag 默认关闭或处于经过批准的安全状态
- [ ] 新 request 由 provider 先接受；新 response/event 由 consumer 先容忍
- [ ] Migration/回填可暂停、可恢复，且已在类生产数据上演练
- [ ] 新旧应用与新旧数据组合有实际证据
- [ ] 不可逆步骤、备份/PITR、roll-forward 和数据补偿明确

## 灰度与观测

- [ ] 内部租户/canary/百分比放量顺序明确
- [ ] 每阶段观察窗口、成功阈值、停止阈值和决策人明确
- [ ] Dashboard、告警、日志、trace 和审计在启用前可用
- [ ] Smoke 覆盖关键用户结果且避免真实高风险副作用
- [ ] runtime harness qualification 与 failure taxonomy 仍对应当前 harness digest/commit
- [ ] 业务成功率、错误率、延迟、资源、成本和安全指标均有阈值
- [ ] AI 功能有线上抽检、质量退化和成本/延迟阈值

## 回滚

- [ ] Kill switch、停止扩量和流量隔离路径可用
- [ ] 上一制品仍可部署，权限和命令经负责人确认
- [ ] 回滚后的数据库、队列、缓存和事件兼容明确
- [ ] 无法安全 down migration 时有可执行 roll-forward
- [ ] 回滚已演练并保存证据
- [ ] 发布/回滚负责人和升级联系路径可用

## 批准

- [ ] G5 Production Ready 通过
- [ ] 业务、技术、发布及条件性安全/数据批准真实存在
- [ ] 所有 `NOT RUN` 与残余风险已由有权人接受
- [ ] 没有开放的 `RCA_REQUIRED` 或被绕过的三次失败熔断

## 线上关闭

- [ ] 生产 smoke 成功
- [ ] 观察窗口完成，关键指标稳定
- [ ] 权限、租户、审批、审计和脱敏完成抽查
- [ ] Incident/回滚/数据异常已记录并处置
- [ ] Release Record、Runbook、Changelog 和用户文档已更新
- [ ] 旧契约、旧列、双轨、临时 Flag 和例外有清理 Issue、Owner 和期限
- [ ] G6 Delivery Complete 通过后才关闭 Feature
