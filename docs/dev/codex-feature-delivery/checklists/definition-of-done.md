# production_hardened Definition of Done

> 仅适用于显式 `production_hardened`。D4 表示本地 Demo 可用，不等于本清单的 G4 Code Complete。

## 需求与实现

- [ ] 每条 AC/NFR 都映射到最终实现和可重复证据
- [ ] 最终代码与批准的需求、契约和设计一致
- [ ] 范围变化已回写文档并重新批准
- [ ] 无生产路径 mock、placeholder、硬编码 fixture、调试后门或阻塞 TODO
- [ ] 无未经批准的无关重构、依赖升级或全仓格式化

## 正确性

- [ ] 正常、边界、非法输入和错误路径测试通过
- [ ] 事务、并发、幂等、超时、取消、重试、限流和部分失败已处理
- [ ] Unit、Integration、Contract/Conformance 和适用 E2E 通过
- [ ] 所有 required slices 的 `G3/<slice-id>` 均 PASS，prerequisites 与 evidence freshness 仍有效
- [ ] final `core_vertical`、`accessibility_visual`、`teardown` 分别 PASS 或有真实 `N/A + Owner 理由`
- [ ] Flaky 测试已调查；没有“重跑到绿”
- [ ] runtime harness 已资格验证；harness/platform/gate failure 没有被冒充 product failure
- [ ] 没有开放的三次同类失败熔断、未完成 RCA 或未经批准的第四次尝试
- [ ] Snapshot/golden/fixture 差异已经人工审阅

## 契约与数据

- [ ] 契约权威源、生成物和 canonical fixture 一致
- [ ] 相对所有受支持基线执行 breaking check
- [ ] 语义兼容经过人工与 Consumer Owner 评审
- [ ] 下游固定 version、完整 commit、digest 和 generator
- [ ] Migration 新旧 reader/writer、回填、校验与恢复已验证
- [ ] 没有从 dirty/floating source 构建发布候选

## 安全与隐私

- [ ] 认证后执行资源级授权和租户隔离
- [ ] 输入、SQL、命令、HTML、路径、URL 与模板参数安全
- [ ] Secret/token/PII 不进入代码、fixture、日志、文档或制品
- [ ] 审批、审计、幂等和高风险操作范围符合设计
- [ ] 新依赖完成必要性、版本、漏洞、许可证和供应链检查

## 可维护与可运维

- [ ] 错误表达稳定，日志、指标、trace、告警和审计足够定位故障
- [ ] Feature Flag 默认安全并有 kill switch
- [ ] Runbook、配置、API/ADR、Changelog 与代码一致
- [ ] 完整 diff、生成物、lockfile、migration 和制品内容已审阅
- [ ] 一个提交/PR 表达一个可审查意图，并能追踪 Feature/AC

## 独立审查与证据

- [ ] 独立 Reviewer 未沿用实现上下文进行自我批准
- [ ] P0/P1 清零；P2 已修复或有 Owner、期限和批准
- [ ] 最终验证记录了 command、cwd、SHA、工具版本、时间、退出码和日志
- [ ] 未执行项被标记为 `NOT RUN`，风险和补验证条件明确
- [ ] Temporal Contract Matrix 的阻断 invariants 均有 executable PASS evidence
- [ ] 工作区无未知改动、秘密、本机路径或临时文件

## Done 结论

- [ ] G4 Code Complete 通过
- [ ] 技术负责人和 Verifier 签认

Code Complete 不等于已经生产交付；仍需 Production Readiness、发布和线上观察。
