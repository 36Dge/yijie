# 简化示例：只读任务历史导出

> 这是演示文档如何串联的虚构示例，不代表任何真实仓库、接口、测试或发布结果。示例只展示内容质量，实际 Feature 必须从真实工具输出取得 SHA、命令和证据。

## 0. Brief

- Feature ID：`FEAT-123`
- 用户结果：有 `task:read` 权限的租户管理员可以把最近 7 天任务历史导出为 UTF-8 CSV。
- 非目标：不支持定时导出、不跨租户、不导出请求/响应正文。
- 成功指标：95% 的 10,000 行以内导出在 10 秒内完成；导出失败率低于 1%。

## 1. Requirements 与 AC

| AC | Given | When | Then |
|---|---|---|---|
| AC-001 | 管理员有 `task:read` 且租户有 50 条任务 | 导出最近 7 天 | CSV 恰好包含授权租户的 50 行、稳定表头和 UTF-8 编码 |
| AC-002 | 用户无 `task:read` | 请求导出 | 返回统一拒绝错误，不生成文件，并记录拒绝审计 |
| AC-003 | 存在其他租户记录 | 请求本租户导出 | 结果中无跨租户行，日志不含任务正文 |
| AC-004 | 查询超过 10,000 行 | 请求导出 | 返回可识别限制错误，提示缩小时间范围 |

## 2. Impact

- API 服务：新增只读导出 use case 和 handler。
- 数据库：只增加参数化只读查询，不改 schema。
- Web：新增导出按钮及 loading/error 状态。
- 公共边界：新增响应类型 `text/csv` 和稳定错误，分类为 `additive`；需要确认 SDK/代理是否能接受非 JSON 响应。
- 安全：资源授权、租户过滤、CSV 注入、敏感日志和导出审计。

这个步骤发现“返回 CSV 不是普通 JSON DTO”，因此不能仅凭“新增 endpoint”就宣称无兼容影响。

## 3. Decisions/Risks

| Decision/Risk | 结论/控制 |
|---|---|
| 同步还是异步 | v1 在 10,000 行内同步；超限拒绝，不隐式创建后台任务 |
| CSV 公式注入 | 以 `= + - @` 开头的单元格按批准规则转义，并有测试 |
| 敏感字段 | 不导出请求/响应正文，只导出 ID、状态、时间和安全摘要 |
| 大查询 | 限制时间范围与行数，使用只读超时，记录资源指标 |

## 4. Contract Plan

- 权威源：公共 API Schema。
- Producer：API 服务。
- Consumers：Web 客户端、SDK、网关。
- 顺序：API Schema 与 consumer 容忍测试 → provider 实现 → Web 启用。
- 兼容证据：generate drift、supported baseline breaking、SDK 对 `text/csv` 的 conformance。

## 5. Technical Design

```text
Web export button
  → authenticated API handler
  → authorization + tenant-scoped export use case
  → read-only repository with limit/timeout
  → streaming CSV encoder
  → audit event + metrics
```

- Handler 只解析/鉴权/映射，不放业务规则。
- Repository 查询必须带 `tenant_id`、时间范围和 hard limit。
- Encoder 逐行写出，客户端取消时停止查询并释放资源。
- 审计只写筛选范围、行数、结果和关联 ID，不写 CSV 内容。

Temporal Contract Matrix 另行冻结：授权通过 → 查询/编码 → 响应提交 → 下载完成/取消 → 审计终态
→ stream/query cleanup；取消或 terminal 不得越过仍持有的查询资源，每个不变量绑定 executable Test ID。

## 6. Test Plan

| AC/Risk | 测试 |
|---|---|
| AC-001 | use case 单测 + repository 集成 + API E2E |
| AC-002 | 未认证、缺权限、错误结构与拒绝审计 |
| AC-003 | 两租户合成 fixture，验证查询和结果隔离 |
| AC-004 | 10,000/10,001 边界 |
| CSV 注入 | 属性/表格用例覆盖危险前缀、引号、换行和 Unicode |
| 取消/超时 | 客户端取消，验证查询取消与资源释放 |
| Contract | generate、breaking、SDK/网关 conformance |

## 7. Implementation Slices

1. `S1/G2A`：权威 Schema、canonical fixture、consumer 容忍测试与不可变 pin。
2. `H1`：默认关闭的真实 browser/API harness qualification，覆盖四类失败与 cleanup。
3. `VS1/G2V`：production Web bootstrap 下，使用两租户合成数据走通按钮 → API → 查询 → CSV
   用户结果 → cleanup 的最小真实纵向链路。
4. `S2`：在已通过的 vertical 上扩展完整 encoder、注入防护、边界与取消。
5. `S3`：扩展租户范围 repository、授权、限制和审计。
6. `S4`：扩展 Web loading/error/download 状态与可访问性。
7. `S5`：指标、告警、Runbook 和 feature flag。

每个切片只允许修改列明模块，并分别记录 prerequisites、完整 commit、local/boundary/vertical
evidence 与 freshness。任何 required evidence 为 `NOT RUN/FAIL/STALE` 时不能通过该切片 G3。

## 8. Verification（格式示意）

| 结论 | 证据 | 结果 |
|---|---|---|
| AC-003 租户隔离 | `真实仓库命令应填在这里` | 示例中不声称 PASS |
| 生成物无漂移 | `真实 generate + diff 命令应填在这里` | NOT RUN |
| SDK 兼容 | `真实 conformance 命令应填在这里` | NOT RUN |
| G2V 最小真实纵向 | `真实平台、production bootstrap、harness commit/digest` | NOT RUN |
| Final core vertical | `完整用户路径` | NOT RUN |
| Final accessibility/visual | `axe/键盘/焦点/视口/主题` | NOT RUN |
| Final teardown | `stream/query/process/temp cleanup` | NOT RUN |

真正的报告还应记录 CWD、完整 SHA、工具版本、时间、退出码和日志位置。

## 9. Release/Rollback

- 默认 flag 为 off；先内部租户 smoke，再 5%、25%、100%。
- 观察导出成功率、p95、取消率、数据库读取时间、审计失败和跨租户拒绝。
- 达到停止阈值时先关 flag；因为无 schema 写入，可以回退 API/Web 制品。
- 发布前必须演练 flag 关闭和上一制品回退，不能只写“可回滚”。

## 10. Delivery Summary

最终关闭时应记录：

- 实际 API/Web 完整 commit 和制品 digest；
- 每条 AC 的生产或预生产证据；
- 灰度窗口内真实指标；
- 权限/租户/审计抽查；
- 已知限制、后续异步导出 Issue；
- G6 关闭批准。

这个示例的关键不是 CSV，而是任何业务需求都能形成：

```text
用户结果
→ 编号 AC
→ 仓库/契约/风险
→ Temporal Contract Matrix
→ Harness Qualification 与早期 G2V
→ Per-slice G3
→ AC 对应的真实测试证据
→ 灰度和回滚
→ 生产观察与关闭
```
