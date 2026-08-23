# {{FEATURE_ID}} 测试与 Eval 计划

## 1. 测试策略

- 风险等级：TBD
- 阻断质量门槛：TBD
- 类生产依赖：TBD
- 不可执行环境：TBD

## 2. AC → 测试追踪矩阵

| AC/NFR | 风险 | Test ID | 层级 | 场景 | 环境 | 预期证据 |
|---|---|---|---|---|---|---|
| AC-001 | TBD | T-001 | unit/integration/contract/E2E | TBD | TBD | TBD |

每个 Must AC 和高风险项至少映射一个可重复证据。

## 3. 领域与边界测试

| 类别 | 正常 | 边界 | 非法/失败 | Test IDs |
|---|---|---|---|---|
| 核心业务规则 | TBD | TBD | TBD | TBD |
| 公共 API/事件 | TBD | TBD | TBD | TBD |
| 数据库/事务 | TBD | TBD | TBD | TBD |
| 外部服务 | TBD | TBD | TBD | TBD |
| UI/可访问性 | TBD | TBD | TBD | TBD |

## 4. 兼容与 Conformance

- 未知字段：TBD
- 未知 enum/event：TBD
- 新旧 producer/consumer：TBD
- 生成漂移：TBD
- Canonical fixture：TBD
- Runtime/第三方兼容：TBD

## 5. 安全与隐私测试

| Test ID | 威胁 | 场景 | 预期结果 |
|---|---|---|---|
| SEC-001 | 未认证/越权/跨租户/注入/泄漏 | TBD | TBD |

## 6. 韧性与故障测试

| Test ID | 故障 | 注入方式 | 恢复预期 | 观测信号 |
|---|---|---|---|---|
| RES-001 | 超时/限流/断线/重启/部分失败 | TBD | TBD | TBD |

## 7. Migration 演练

| 组合 | 数据状态 | Reader/Writer | 预期 | 校验 |
|---|---|---|---|---|
| old app + expanded schema | TBD | TBD | TBD | TBD |
| new app + old/new data | TBD | TBD | TBD | TBD |
| rollback/roll-forward | TBD | TBD | TBD | TBD |

无数据库变化：`N/A + 理由`。

## 8. 性能与容量

| Metric | Workload | Baseline | Pass threshold | Stop threshold |
|---|---|---:|---:|---:|
| TBD | TBD | TBD | TBD | TBD |

## 9. AI Eval 专项

| 项目 | 固定值/版本 |
|---|---|
| Dataset 与 holdout | TBD |
| Model/prompt/skill/knowledge/tool schema | TBD |
| Seed/temperature/runner | TBD |
| 结构通过率 | TBD |
| 任务成功率 | TBD |
| 工具选择/参数正确率 | TBD |
| 引用/无答案/安全 | TBD |
| 延迟与成本 | TBD |
| 相对基线不可退化阈值 | TBD |

非 AI 功能：`N/A + 理由`。禁止用少量主观对话替代固定 Eval。

## 10. Fixture 与测试数据

| Fixture/Dataset | 权威位置 | 数据分类 | 合成/脱敏方式 | Consumer |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## 11. 实际执行命令

| 层级 | Repository/CWD | Command | 环境依赖 | 预期时长 |
|---|---|---|---|---|
| lint/typecheck/build | TBD | TBD | TBD | TBD |
| unit/integration | TBD | TBD | TBD | TBD |
| contract/conformance | TBD | TBD | TBD | TBD |
| E2E/security/eval | TBD | TBD | TBD | TBD |

命令必须来自仓库脚本或 CI 配置；示例命令不能被当作真实能力。

## 12. Runtime Harness Qualification

| Harness ID | Full commit/digest | Real platform | Production bootstrap | Positive control | 4 negative controls | Timeout | Cleanup/content-free | Result |
|---|---|---|---|---|---|---|---|---|
| H-VERTICAL-001 | TBD | TBD | yes/no | TBD | TBD | TBD | TBD | NOT RUN |

Harness 成为阻断证据前必须证明 closed、content-free verdict 能唯一分类：

| Failure class | 判定条件 | Control/Test ID |
|---|---|---|
| product_failure | qualified harness 抵达正确生产观测点后产品行为违约 | TBD |
| harness_failure | controller/fixture/assertion/evidence transport/orchestration 自身失败 | TBD |
| platform_failure | OS/WebView/Runtime/环境前置条件失败 | TBD |
| gate_failure | checker/allowlist/治理规则错误拒绝合法证据 | TBD |

无法分类时保持 `DIAGNOSIS_REQUIRED`，不得猜成 product failure。
每个 control 必须有独立 `08-verification-report.md#<EVIDENCE-ID>`，negative control 的
`observed_class` 必须与被注入的四类之一精确相等；qualification 还必须记录 exact command、environment、
exit code、验证时间、harness full commit 和 digest。

## 13. G2V 与最终 E2E 独立 Verdict

| Verdict | 阶段 | Required | Exact command/environment | Pass 条件 | Evidence freshness | 当前结果 |
|---|---|---|---|---|---|---|
| G2V minimal core | 大规模实现前 | yes/no | TBD | 真实平台 + production bootstrap + 最小代表性数据 + cleanup | TBD | NOT RUN |
| core_vertical | G4 前 | yes/no | TBD | 完整关键用户纵向结果 | TBD | NOT RUN |
| accessibility_visual | G4 前 | yes/no | TBD | axe/键盘/焦点/视口/主题/截图 | TBD | NOT RUN |
| teardown | G4 前 | yes/no | TBD | process/connection/WAL/spool/temp/listener/handle/run-root cleanup | TBD | NOT RUN |

三个最终 verdict 独立保存；一项 PASS 不得覆盖另一项 `FAIL/NOT RUN`。

## 14. 通过、失败、Flaky 与三次熔断策略

- PASS：命令完成、退出码与断言符合预期；
- FAIL：任何阻断断言失败；
- NOT RUN：环境缺失、被跳过、输出截断或进程未完成；
- Flaky：先调查根因，不允许“重跑到绿”作为通过证据；
- Snapshot/golden：必须人工审阅语义 diff。

同类失败 fingerprint：`feature + slice + gate + evidence/harness ID + owner layer + stable failure code/checkpoint`。
第三次出现后进入 `RCA_REQUIRED`，禁止第四次重试、自动 retry、延长 timeout、改名清零或继续局部补丁。

| Incident ID | Fingerprint | Attempt 1 | Attempt 2 | Attempt 3 | RCA evidence | Product/Harness/Platform/Gate | Owner-approved single next action |
|---|---|---|---|---|---|---|---|
| RCA-001 | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## 15. 测试计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 测试/技术 Owner | TBD | Approve/Reject | TBD |
| 安全/数据 Owner | TBD | Approve/Reject/N/A | TBD |
