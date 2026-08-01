# FEAT-125 交付总结与关闭记录

> 当前已到 S4 API producer committed candidate 阶段，不是业务功能交付完成记录。
> S1/S2/S3 已推送，S4 本地实现、审查和门禁证据已写入；Desktop、跨仓集成、发布和生产
> 栏位仍保持明确 `NOT RUN / Not delivered`。

## 1. 最终结果

- 用户可观察行为：尚未变化；Desktop 仍是 FEAT-124 candidate
  `be01cc2d0a1c9c4b057de616be201a4843d0a035`。
- 原目标是否达成：否；已完成 A1—A6、S1/S2 Contracts remote candidate、S3 API
  foundation，以及 S4 tenants/capabilities HTTP producer、逐请求 tenant 验证、稳定错误、
  revision、metrics recorder 与 conformance/fault tests；尚无 Desktop/跨仓/生产链路。
- 最终范围与非目标：见 00—07；G1/G2 于 2026-07-31 Passed，G2A 于 2026-08-01 Passed。
- 交付状态：`S1/S2/S3 Remote / S4 Local Commit + Structured Review PASS / Not delivered`。
- FEAT-124：G4-001 继续 Open，不得关闭。

## 2. 实际发布版本

| Component | Environment | Version/tag | Full commit | Artifact digest | Contract version/pin |
|---|---|---|---|---|---|
| yijie-contracts | repository remote candidate | 0.3.0 candidate；no release/tag | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | source `7bd40dd...`；tarball `43a54d7...` | candidate 0.3.0；supported release 仍 v0.2.0 |
| yijie-api | local test only | S4 commit；no release | `360a526b679147472e7cc82ca7ac9db9d18a371d`；not pushed | generated `a1801a...`；migration `51c4ced9...` | exact candidate `9ec34abd...` / oapi-codegen v2.7.2；feature flag false |
| yijie-desktop | none | no FEAT-125 release | `be01cc2d0a1c9c4b057de616be201a4843d0a035` remains current | N/A | no FEAT-125 pin |
| database | isolated local PostgreSQL 16.14 | goose migration v2 candidate；not deployed | API `fff0cbcba601...` | `51c4ced9...` | expand-only / no sessions or real seed |

## 3. 验收结果

| AC/NFR | 结果 | 自动化/人工证据 | Production evidence |
|---|---|---|---|
| AC-001/003/004/013/015/020 S3 foundation | PARTIAL PASS | JWT/JWKS、identity/tenancy/RBAC、2×2 matrix、migration integration | none |
| AC-014 contract candidate/pin | CONTRACT + API PIN PASS / Desktop pending | S1/S2 gates + S3 exact source/generated/generator checks | none |
| S4 API producer slice | PASS | `/v1/me/tenants`、`/v1/me/capabilities`、header 逐请求验证、稳定错误、revision、metrics recorder、canonical conformance/fault tests | none；flag default false |
| remaining AC/NFR | NOT RUN | Desktop/cross-repo/production slices pending | none |

## 4. 生产 Smoke 与观察

| Check/Metric | Window | Baseline | Actual | Threshold | Result |
|---|---|---:|---:|---:|---|
| capability success/error/latency | no deployment window | process-local recorder unit-tested only | N/A | G5 candidate | NOT RUN |
| tenant/context mismatch | none | 0 target | N/A | 0 | NOT RUN |
| unauthorized DOM/route/API | none | current G4-001 open | N/A | 0 | NOT RUN |

## 5. 安全与审计抽查

| 项目 | Trace/request/task/session 标识 | 结果 | Evidence |
|---|---|---|---|
| 授权/租户/审计/脱敏 | synthetic S3/S4 only | PASS for foundation + producer：fail-closed reads、cross-tenant FK、append-only、逐请求 membership/RBAC projection、稳定错误、secret-free diff；write/bootstrap/Desktop pending | 08 verification report |

## 6. 发布事件、回滚与数据状态

- Incident/异常：N/A；未部署。
- 是否触发停止或回滚：否；没有可回滚 FEAT-125 artifact。
- 数据/队列/缓存最终状态：只在隔离临时 PostgreSQL 创建并清理合成 auth/RBAC 数据；未触碰
  staging/production，未新增 session/cache。
- 回滚路径当前是否仍有效：应用可回退到 base `2834b412...`；expand schema 按设计保留并
  roll-forward，destructive down 明确拒绝；生产回滚尚未演练。

## 7. 未验证项、已知限制与接受风险

| Item | 影响 | Owner | 批准 | 截止/复查 |
|---|---|---|---|---|
| direct IdP JWT/native auth/tenant/RBAC | API S3 foundation + S4 endpoint producer PASS；真实 IdP 与 Desktop native auth 未实现 | 段成威 | G2A/S3/S4 approved | S5—S7/G3/G5 |
| migration/bootstrap/audit | expand migration/rehearsal PASS；bootstrap/writer transaction 未实现 | 段成威 | S3 foundation | S7 |
| contracts v0.3.0 downstream pin | API exact pin PASS；Desktop pin/tag 尚未形成 | 段成威 | G2A Passed | S5B/S8 |
| API/Desktop implementation | API producer local candidate；Desktop 与生产链路未实现 | 段成威 | S4 approved；其余 Pending | G4 |
| Tasks 双重隔离与 FEAT-126 | A6 已批准；ingress deny + service 不注册 handlers 尚未验证；FEAT-125 不提供 Tasks 资源级授权 | 段成威 | Approved temporary exception | G5；FEAT-126 生产启用或 2026-09-30 较早者 |
| production IdP/infra | audience 已固定 `https://api.yijie.ai`；vendor、issuer、client ID、JWKS、TLS/CSP 等仍待确定 | 段成威 | Pending | G3/G5 |

A6 是唯一已批准的有期限临时例外，只允许 legacy Tasks 保持不可达，不允许对外暴露或
宣称已有资源级授权；其余实现、集成和发布风险继续阻断对应 gate。

## 8. 后续清理

| Issue | 内容 | 触发条件 | Owner | 截止 |
|---|---|---|---|---|
| CLEAN-001 | 删除旧 Desktop optional/default visibility 接口 | 新 total policy 完成并兼容验证 | 段成威 | S6 后 |
| CLEAN-002 | 移除 candidate SHA provenance，切不可移动 tag | tag/digest verification PASS | 段成威 | S8 |
| CLEAN-003 | 评估 capability alias/deprecation | 未来 key 改名/删除 | 段成威 | future feature |
| CLEAN-004 | 以 FEAT-126 完成 Tasks resource-level auth/tenant hardening 并移除临时隔离例外 | FEAT-126 生产启用；若未完成则保持 Tasks 阻断并重新审批 | 段成威 | FEAT-126 生产启用或 2026-09-30 较早者 |
| CLEAN-005 | 删除 flags/双轨 | 全部 consumers 迁移且生产观察完成 | 段成威 | G6 后 |

## 9. 文档与运维交接

| Artifact | Final path/link | Owner | Updated |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-125-authoritative-permission-projection/` | 段成威 | 2026-08-01 |
| Security/architecture ADR | `yijie/docs/adr/ADR-0012-authoritative-identity-tenant-and-permission-boundary.md` | 段成威 | Accepted 2026-07-31 |
| Public API/release docs | `yijie-contracts/openapi/public/public.yaml` + `docs/releases/contracts-v0.3.0.md` | 段成威 | remote candidate 2026-08-01 |
| API/Desktop runbooks | planned in owning repos | 段成威 | not created |
| FEAT-124 G4 report | existing FEAT-124 `08-verification-report.md` | 段成威 | G4-001 remains open |

## 10. 复盘

- 做得有效的流程：先扫描四仓真实状态，再分别从 Contracts、API、Desktop 审核推荐方案；
  没有把“创建 endpoint”误写成可直接开工。
- 出现的返工/缺陷：现有 FEAT-124 需求曾假设“已有权限投影”，而仓库事实表明并不存在。
- 根因：需求层的未来依赖没有在 G2 前验证真实 provider/consumer call chain。
- 要沉淀的改进：任何 Must 权限 UI AC 必须在 G2 提供权威 Principal、tenant、policy
  source、production wiring 和 direct API enforcement 证据；纯 resolver 测试不足。

## 11. 关闭批准

| Gate | Owner | Decision | Date | Evidence |
|---|---|---|---|---|
| G6 Delivery Complete | 段成威 | Not approved / feature open | 2026-08-01 | S1/S2/S3 remote、G2A、S4 local commit/review/gates complete；S4 push、S5—S8/G4/G5/G6 Pending |

- 正式关闭时间：N/A。
