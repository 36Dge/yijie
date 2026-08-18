# FEAT-127 发布、灰度与回滚 Runbook

> 当前范围没有部署、云资源、正式制品或生产数据。本文件记录未来激活前必须执行的顺序和本地最终 schema v7 数据边界，不代表发布已批准或执行。

## 1. Release Manifest

| Component | Version/tag | Full commit | Artifact digest | Contract pin | Environment |
|---|---|---|---|---|---|
| Contracts | `contracts-v0.3.0` 仅为候选名称；无 tag | `747cf740f2d91e76e5c1a130e8e009f1efa821b8` | OpenAPI `3d2f2273...`；fixture `ec464ce5...`；无 release artifact | N/A | pushed feature branch/local candidate |
| Agent Host | 未发布 | `e2f0f5d0e7273331e7e9eaeeb82be15955e94c86` | source commit only；无 release artifact | Contracts `747cf740...` | pushed feature branch/local candidate |
| Desktop | 未发布 | `2cb4ffdd87055e5f70aafacc63479154e0c62cad` | source commit only；无 signed artifact | Contracts `747cf740...`；Rust adapter under `EXC-127-002` | pushed feature branch/local candidate |

## 2. 当前发布判定

- G2A：`PASS WITH EXCEPTION (EXC-127-002)` for local candidate；不可变 full commit、下游 pin、semantic Owner/consumer review 与 conformance 已完成。release tag/supported 状态仍 PENDING，但不是本地 G2A 前置。
- G3：`PASS WITH EXCEPTION`；`EXC-127-001` 仅适用于当前本地候选，人工验收仍为 `PARTIAL`，真实 macOS 可访问性仍为 `NOT RUN`，到期或触发后回退 `PENDING`。
- G4：`PASS` for local candidate；最终 commits/pins、门禁、独立审查与 Reviewer 段成威批准已记录，受两项有期限例外约束。
- G5/G6：本地范围 N/A；没有生产配置、签名、公证、dashboard、告警、制品或批准。
- 当前允许动作：本地 synthetic 测试、构建和人工验收；已完成授权范围内的 commit/push。
- 当前禁止动作：merge、tag、signed/release build、部署、真实模型调用、购买/配置云资源。

## 3. 未来合并、迁移与启用顺序

| Order | Action | Preconditions | Verification | Rollback point |
|---:|---|---|---|---|
| 1 | 取得独立 release approval 后，为 Contracts `747cf740...` 创建不可移动 tag | local semantic review/checks 已完成；当前 release approval 未形成 | tag 解析到同一 full commit 与 OpenAPI/fixture digest | 不发布 tag，继续 v1 |
| 2 | 审查并合并已 pin exact contract 的 Host v2 provider `e2f0f5d...` | release identity 可用；v2 route 默认不被旧 Desktop 调用 | race/conformance/fixed Runtime fake vertical slice | 停用/不部署 v2 route，v1 保持 |
| 3 | 关闭或重新批准两项例外，审查 Desktop `2cb4ffd...` 并形成签名候选 | Host provider merge ready；v7 backup/forward-only 边界获批；真实 macOS accessibility 完成；Rust adapter generator/例外重新评审 | lint/test/build/Tauri bundle/manual accessibility/contract conformance | 不分发 Desktop candidate |
| 4 | 备份当前加密数据库后升级到 v7 | 备份与对应旧应用可读、密钥可用、磁盘空间充足 | v6+v7 ledger、history、draft target/order、TTL、WAL checkpoint smoke | 恢复完整迁移前 backup，旧应用不能打开 v7 DB |
| 5 | 小范围启用加号/拖拽与 v2 dispatch | Host/Desktop 版本组合兼容 | synthetic attachment smoke + telemetry redaction | 停止扩量；使用 v7 roll-forward 或恢复匹配旧版本的 backup |

## 4. Feature Control

当前候选没有可声称已部署的生产 feature flag。未来激活必须增加可审计的版本/渠道控制；默认状态为“不分发、不启用”。Kill switch 是停止分发 FEAT-127 Desktop/Host 组合并阻止新 v2 attachment turn，而不是静默剥离附件后降级为纯文本发送。

## 5. Migration 与数据恢复

| Phase | 行为 | Validation | Pause/recovery |
|---|---|---|---|
| Expand v6 | 应用 `0006_chat_attachments.sql`，新增 attachment、content block、chunk 与索引结构 | checksum ledger、FK、v1-v5 history preservation | transaction 失败则不提升 user_version |
| Expand v7 | 应用 `0007_chat_attachment_draft_targets.sql`，增加 composer target、稳定 ordinal、约束与索引 | populated-v6 bound history preserved；无 target ready rows fail-closed cleanup | 恢复 pre-v7 backup 或使用 v7 roll-forward |
| Backfill | N/A；旧纯文本消息读取时合成 text block | legacy history tests | 无批量写入可暂停 |
| Switch | 新 v2 create/submit 写 ordered blocks 与 attachment binding | one-message atomicity、operation idempotency | 停止新 v2 写入，保留已扩展 schema |
| Contract | 本期不删除 v1 字段、旧表或旧 route | v1 wire equality | 未来独立 Feature 才可清理 |

v7 是 forward-only。已升级数据库不能由 v5/v6 Desktop 原地打开；应用级回退只有两条安全路径：

1. 恢复迁移前完整、加密且已由对应旧版本验证可读的备份，再运行匹配应用。
2. 保留 v7 数据库并使用修复后的 v7 Desktop roll-forward。

不得手写 down migration 或只删除新表。当前没有生产数据库迁移；测试只操作合成临时数据库。

## 6. 未来灰度与 Smoke

| Stage | Scope | Success criteria | Stop condition |
|---|---|---|---|
| Internal | 单一合成租户/本地签名候选 | picker/drop、纯附件、mixed message、reopen、TTL、delete 全部通过 | duplicate turn、path/content leak、DB/WAL cleanup failure |
| Canary | 明确批准的少量测试账户 | send success/error、latency/resource 在批准阈值内 | crash/OOM、P1 security finding、unknown duplicate outcome |
| Expand | 分阶段扩大 | 观察窗口内稳定且无 confidential leak | 超过批准错误率/资源/安全阈值 |

Smoke 输入只允许合成 JPEG/PNG/PDF/TXT/DOCX 等 fixture，不使用真实商家文件。至少覆盖：统一加号、拖拽、10 MiB 边界、压缩包拒绝、Host 短暂不可用重试、重开历史、七天过期和永久删除。

## 7. 观测与停止信号

未来 G5 前必须提供真实 dashboard/query 与阈值，至少包括：attachment import/parse/index success、typed reject reason、v2 operation replay/conflict、Host/Runtime request size、Desktop memory/CPU、SQLCipher/WAL cleanup、expired content exclusion、path/body redaction。当前没有这些生产信号，不能填写或推断基线数值。

立即停止扩量的条件：重复消息或 Runtime turn、expired bytes 仍可读取、路径/正文/data URL 进入日志或 IPC、parser crash/OOM、WAL truncate 持续失败、v1 consumer 回归或不可恢复 migration。

## 8. 回滚决策

```text
发现停止条件
  -> 阻止新的 v2 attachment turn
  -> 保留证据并停止扩量
  -> 判断数据库是否已升级到 v7
  -> 未升级：回退应用/Host candidate
  -> 已升级：优先 v7 roll-forward；需要旧应用时恢复完整迁移前备份
  -> 复验 history、TTL、WAL、idempotency 与 redaction
```

代码回退不能删除或改写已绑定附件历史；过期/删除继续使用 v7 authority。任何恢复都必须验证 attachment BLOB/chunks、draft target/ordinal、outbox operation、message block ordinal 与 cleanup receipt 一致。

## 9. 命令、演练与批准

- Deploy/disable/rollback command：N/A；当前没有部署平台，Codex 不编造生产命令。
- 本地验证命令：见 `08-verification-report.md`，不等同部署或回滚演练。
- 正式回滚演练：NOT RUN；需在类生产签名 Desktop、真实版本 pin 和复制的加密数据库上执行。
- Release/Go-No-Go approver：段成威；当前未批准 release、tag 或生产激活。
- G3 exception owner：段成威；`EXC-127-001` 不适用于签名、公证或可分发候选，进入这些阶段前必须补验并关闭或重新审批。
- G2A/G4 adapter exception owner：段成威；`EXC-127-002` 在 approved Rust generator、schema/受锁 source 变化、到期或 signed/release candidate 前必须移除或重新审批。
- 联系路径与值班机制：N/A；单人本地开发阶段未建立生产 on-call。
