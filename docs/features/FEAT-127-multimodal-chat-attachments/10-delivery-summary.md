# FEAT-127 交付总结与关闭记录

## 1. 最终结果

- 用户可观察行为：Chat composer 在权限入口前提供一个统一加号，支持选择或拖拽常规图片/文件；草稿显示附件状态，可发送纯附件或 mixed message，历史恢复安全 metadata，七天后显示已过期且不再进入 Runtime context。
- 原目标：本地候选范围已实现并完成自动化与合成验证；用户 Desktop 人工验收已部分进行，没有形成 release tag、签名制品或生产激活。
- 非目标保持不变：不处理模型生成文件/图片的展示操作，不使用云存储/服务端解析，不支持压缩包、SVG、宏文档、legacy DOC、OCR 或远程 URL。
- 交付状态：`G4 PASS for local candidate with EXC-127-001/002 / Source and Evidence Commits Pushed / Production Activation Blocked`。

## 2. 实际候选版本

| Component | Environment | Version/tag | Full commit | Artifact/contract identity |
|---|---|---|---|---|
| Contracts | pushed feature branch | `0.3.0 candidate`，无 tag | `747cf740f2d91e76e5c1a130e8e009f1efa821b8` | OpenAPI `3d2f2273...`；Chat Schema `3f277898...`；fixture `ec464ce5...` |
| Agent Host | pushed feature branch + fixed Runtime fake integration | 未发布 | `e2f0f5d0e7273331e7e9eaeeb82be15955e94c86` | pins Contracts `747cf740...`；Runtime 0.144.6 binary `98910475...` |
| Desktop | pushed feature branch / visual harness | 未发布 | `2cb4ffdd87055e5f70aafacc63479154e0c62cad` | pins Contracts `747cf740...`；Rust adapter `c6e90e0e...` under `EXC-127-002`；private IPC `b03e3c8f...`；migrations `60b08d6c...` + `aae67ca5...` |

完整 commit 是不可变 source identity，Host/Desktop exact pin 已形成；digest 用于文件级一致性。它们仍不是 release tag、签名制品或部署证据。

两个 focused Store tests、最终 contract lock/conformance 与证据文档均进入可审查提交并推送。元仓交付包由包含本文件的提交标识，不在正文自引用该提交 SHA，以避免循环身份。

## 3. 验收结果

| AC/NFR | 结果 | 自动化/人工证据 | Production evidence |
|---|---|---|---|
| AC-001..009、AC-011 automated | PASS（人工验收候选） | Contracts/Host/Desktop suites、fixed Runtime fake vertical slice、migration/security/failure tests | N/A：未部署 |
| Targeted acceptance regression | PASS | 自动覆盖移除后不恢复、10 MiB/10 MiB+1、压缩包、10+1 容量；新增 2 个精确 Store tests，7 个 native focused tests 与完整 Desktop 门禁通过 | N/A：未部署 |
| Desktop functional manual acceptance | PARTIAL | 人工通过 picker、仅附件 Runtime、不支持格式提示、修复后图片拖拽、图文文件 mixed send、已发送历史重开、未发送附件草稿重开；移除/边界/容量为 automated-only | N/A：未部署 |
| AC-010 accessibility/responsive | PARTIAL | 自动：light/dark、1180x760、equivalent 200% CSS viewport、axe 0 violations、keyboard/component tests；人工：`NOT RUN` | N/A；VoiceOver/真实系统缩放/reduced motion 未执行 |
| AI input mapping | PASS（无模型） | ordered file chunks/image input 到固定 Runtime turn | 不证明真实模型答案质量 |

完整 AC 映射与命令见 `08-verification-report.md`。

扩展候选复验于 2026-08-18 完成，包含 all-targets/all-features Rust 208 passed / 3 ignored、视觉矩阵与本地 API/gateway 检查。2026-08-19 最终 reconciliation 后：Contracts generate/lint/31 Node tests + Go validator/build/breaking/v1 equality PASS；Host lint/race tests/runtime-test/contract-check PASS；Desktop `make lint/test/build` 与 docs build PASS，35 Vitest files / 270 tests、Rust 175 passed / 3 ignored；all-target/all-feature Rust 209 passed / 3 ignored。最终 contract focused tests 为 2 files / 8 tests，Rust canonical serialization 1/1。没有真实模型调用。

## 4. 生产 Smoke、指标与安全抽查

- 生产 Smoke：N/A；用户明确本期无部署计划。
- 线上指标/观察窗口：N/A；没有生产服务、dashboard 或流量。
- 授权/租户/脱敏：本地合成测试 PASS；没有真实账户或商家数据抽查。
- 审批/审计：本功能不新增高风险业务工具执行；release/production approval 未形成。
- Incident/回滚：没有生产 incident，也没有触发生产回滚。

## 5. 已修复的审查缺陷

独立 Codex audit、主代理审查与提交门禁共识别并修复十四个 P1、两个 P2：除 parser、WAL、worker、草稿恢复/顺序、progress、拖拽和 Go regex 兼容问题外，最终审查还关闭了 Rust conformance 可静默消失、readiness 注释伪装和 exception 到期误绿。所有对应回归通过，P0/P1/P2 均清零；用户已完成修复后图片拖拽复验。这些结果不替代完整人工验收，Codex audit 也不冒充段成威的 Reviewer 批准。

## 6. 已知限制与阻断

| Item | 影响 | Owner | 状态/触发条件 |
|---|---|---|---|
| Contract release tag/status | semantic review、source commit 与 downstream pins 已形成，但 candidate 尚非 supported/release-ready | Contracts/Release Owner | 进入正式发布并取得 release approval 后创建、核对不可移动 tag |
| `EXC-127-001` 临时验收例外 | 自动证据可能遗漏真实 Desktop 集成差异；延期可访问性可能使平台问题晚发现 | 段成威 | 有效至 2026-11-17（含）；签名/分发、staging/release、相关代码/平台变更、问题反馈等可更早触发失效，G3 回退 `PENDING` |
| `EXC-127-002` 临时 Rust adapter | 无批准 Rust generator；未来 adapter/schema 漂移可能误解释 wire | 段成威 | 有效至 2026-11-17（含）；approved generator、受锁 source/schema 变化或 signed/release candidate 可更早触发移除/重审 |
| 现代、增量、加密或复杂过滤器 PDF fail closed | 部分可阅读 PDF 会提示不支持/内容无效 | Client Owner | 用户可另存兼容 PDF；扩兼容需独立 parser Feature |
| VoiceOver、真实系统缩放、reduced motion | 自动化证据不等同 macOS 手工可访问性验收 | Product/Design Owner | 签名 Tauri candidate 阶段执行 |
| 真实模型答案质量 | 不能声称附件提升回答质量 | Product/AI Owner | 批准模型、dataset 与 threshold 后 Eval |
| 签名、公证、生产资源、监控和回滚演练 | 不能进入 G5/G6 | Release Owner | 真实部署准备阶段补齐 |

## 7. 后续工作

| Issue | 内容 | 触发条件 | Owner |
|---|---|---|---|
| FEAT-127-ACCEPTANCE-EXCEPTION | 跟踪 `EXC-127-001`；触发后补做移除后重开、大小/压缩包、10+1 容量和三项真实 macOS 可访问性验收，并关闭或重新审批例外 | 2026-11-17 或 `03-decisions-and-risks.md` 所列任一触发条件，以较早者为准 | 段成威 |
| FEAT-127-RELEASE | PR/merge、release review 与适用不可移动 tag；不重复已完成的本地 semantic review | 决定进入合并/发布流程 | 段成威 |
| FEAT-127-RUST-GENERATOR | 评估批准的 Rust OpenAPI generator，或在 `EXC-127-002` 触发时重做 adapter review | 2026-11-17 或任一触发条件，以较早者为准 | 段成威 |
| FEAT-127-A11Y | VoiceOver、真实 200% 缩放、reduced motion、签名 bundle 检查 | 准备 Desktop 分发 | 段成威 |
| FEAT-127-PDF | 评估隔离 parser/子进程资源限制以扩展现代 PDF 兼容 | 兼容性反馈达到立项条件 | 段成威 |
| FEAT-127-PROD | 生产配置、监控、灰度、备份与回滚演练 | 决定购买/准备资源并部署 | 段成威 |

旧 v1 route、`content` 文本投影和 v1-v5 reader 兼容路径本期不清理；只有 consumers 迁移和生产观测完成后才能另行删除。

## 8. 文档与交接

| Artifact | Path | Owner | Updated |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-127-multimodal-chat-attachments/` | 段成威 | 2026-08-19 |
| Desktop design pattern | `yijie-desktop/docs/design/docs/design/05-patterns/13-feat-127-chat-attachments.md` | 段成威 | 2026-08-19 |
| Local release/rollback boundary | `09-release-and-rollback.md` | 段成威 | 2026-08-19 |

## 9. 复盘

- 有效流程：先冻结 screenshot 语义和 semantic、versioned v2 contract surface，再并行实现 Host/Desktop；固定 Runtime + fake Responses 提供了不付费的真实协议垂直证据。
- 返工：初版 parser/cleanup/recovery review 暴露 PDF/OOXML 放大与 WAL/unknown-outcome 缺口；前端 accepted-command 与 projection refresh 也曾耦合。
- 根因：初版资源模型按唯一对象或声明元数据估算，未按实际引用/读取量推演；提交成功与读取投影未完全分离。
- 沉淀：新增 adversarial parser、WAL busy/reopen、invalid 202 same-operation replay、Schema instance validation 和 accepted-create refresh failure tests。

## 10. Gate 与关闭状态

| Gate | Decision | Date | Evidence |
|---|---|---|---|
| G2 local implementation design | PASS under explicit local implementation request | 2026-08-17 | `00`..`07` |
| G2A contract ready | PASS WITH EXCEPTION (`EXC-127-002`) for local candidate | 2026-08-19 | full commit/pins/checks/semantic review PASS；Rust adapter exception active；release tag/supported status pending |
| G3 Slice Complete | PASS WITH EXCEPTION (`EXC-127-001`) | 2026-08-19 | targeted automated regression substitutes removal/bounds/capacity；manual remains partial；macOS accessibility remains NOT RUN；temporary local-only exception |
| G4 Code Complete | PASS for local candidate | 2026-08-19 | final commits/pins/gates pushed；P0/P1/P2 clear；Reviewer 段成威 approved；`EXC-127-001/002` active |
| G5 Production Ready | N/A for current local scope, not passed | 2026-08-17 | no production preparation |
| G6 Delivery Complete | N/A for current local scope, not passed | 2026-08-17 | no deployment/smoke/observation |

- Desktop 人工验收候选形成时间：2026-08-18。
- 本地人工验收：2026-08-19 部分完成；picker、仅附件、修复后拖拽、mixed send、已发送历史重开和未发送草稿重开通过；移除/边界/容量为 automated-only，可访问性手工项 `NOT RUN`。
- 本地 Code Complete 时间：2026-08-19；G4 在两项有期限例外下通过。
- 正式发布/生产关闭时间：未形成；tag、PR/merge、signed artifact、G5/G6 与生产阶段仍不在当前范围。
