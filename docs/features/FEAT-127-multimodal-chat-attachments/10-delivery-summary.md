# FEAT-127 交付总结与关闭记录

## 1. 最终结果

- 用户可观察行为：Chat composer 在权限入口前提供一个统一加号，支持选择或拖拽常规图片/文件；草稿显示附件状态，可发送纯附件或 mixed message，历史恢复安全 metadata，七天后显示已过期且不再进入 Runtime context。
- 原目标：本地候选范围已实现并完成自动化与合成验证；用户 Desktop 人工验收已部分进行，没有形成 release tag、签名制品或生产激活。
- 非目标保持不变：不处理模型生成文件/图片的展示操作，不使用云存储/服务端解析，不支持压缩包、SVG、宏文档、legacy DOC、OCR 或远程 URL。
- 交付状态：`Manual Acceptance In Progress / Source Commits Pushed / Production Activation Blocked`。

## 2. 实际候选版本

| Component | Environment | Version/tag | Full commit | Artifact/contract identity |
|---|---|---|---|---|
| Contracts | pushed feature branch | `0.3.0 candidate`，无 tag | `ebdd30f076614ebc7f5149aebf70e851b81ff32b` | OpenAPI `3d2f2273...`；Chat Schema `3f277898...` |
| Agent Host | pushed feature branch + fixed Runtime fake integration | 未发布 | `673de86d3d076f4600eb0d0bfb215382677afd72` | pins Contracts `ebdd30f...`；Runtime 0.144.6 binary `98910475...` |
| Desktop | pushed feature branch / visual harness | 未发布 | `3efed9aba5faab90ca3ea397a4d6489890df2026` | pins Contracts `ebdd30f...`；private IPC `b03e3c8f...`；migrations `60b08d6c...` + `aae67ca5...` |

完整 commit 是不可变 source identity，Host/Desktop exact pin 已形成；digest 用于文件级一致性。它们仍不是 release tag、签名制品或部署证据。

## 3. 验收结果

| AC/NFR | 结果 | 自动化/人工证据 | Production evidence |
|---|---|---|---|
| AC-001..009、AC-011 automated | PASS（人工验收候选） | Contracts/Host/Desktop suites、fixed Runtime fake vertical slice、migration/security/failure tests | N/A：未部署 |
| Desktop functional manual acceptance | PARTIAL | picker 与仅附件 Runtime 路径通过；格式拒绝提示符合预期；drop 修复后复验及 mixed send/reopen/recovery 待完成 | N/A：未部署 |
| AC-010 accessibility/responsive | PARTIAL | light/dark、1180x760、equivalent 200% CSS viewport、axe 0 violations、keyboard/component tests | N/A；VoiceOver/真实系统缩放/reduced motion 未执行 |
| AI input mapping | PASS（无模型） | ordered file chunks/image input 到固定 Runtime turn | 不证明真实模型答案质量 |

完整 AC 映射与命令见 `08-verification-report.md`。

扩展候选复验于 2026-08-18 完成，包含 all-targets/all-features Rust 208 passed / 3 ignored、视觉矩阵与本地 API/gateway 检查。2026-08-19 对最终 commit/pin 再执行标准门禁：Contracts generate/lint/31 Node tests + Go validator/breaking PASS；Host lint/race tests/runtime-test PASS；Desktop lint、34 files / 263 Vitest、Rust 174 passed / 3 ignored、build 与 docs build PASS。没有真实模型调用。

## 4. 生产 Smoke、指标与安全抽查

- 生产 Smoke：N/A；用户明确本期无部署计划。
- 线上指标/观察窗口：N/A；没有生产服务、dashboard 或流量。
- 授权/租户/脱敏：本地合成测试 PASS；没有真实账户或商家数据抽查。
- 审批/审计：本功能不新增高风险业务工具执行；release/production approval 未形成。
- Incident/回滚：没有生产 incident，也没有触发生产回滚。

## 5. 已修复的审查缺陷

独立 Codex audit、主代理审查与提交门禁共识别并修复十三个 P1：原有 parser、WAL、worker、草稿恢复/顺序和 progress 终态问题之外，本轮补充修复拖拽监听被未授权 `scaleFactor()` 调用阻断，以及 OpenAPI PCRE 正则不兼容 Go validator。所有对应自动回归通过，当前没有开放 P0/P1；拖拽修复后的用户复验仍待完成。这些结果均不替代完整人工验收。

## 6. 已知限制与阻断

| Item | 影响 | Owner | 状态/触发条件 |
|---|---|---|---|
| G2A semantic review/release tag | source commit 与 downstream pins 已形成，但尚不能宣称 contract release ready | Contracts/Host/Desktop Owner | 明确 Owner/consumer review；进入发布时创建并核对 tag |
| 现代、增量、加密或复杂过滤器 PDF fail closed | 部分可阅读 PDF 会提示不支持/内容无效 | Client Owner | 用户可另存兼容 PDF；扩兼容需独立 parser Feature |
| VoiceOver、真实系统缩放、reduced motion | 自动化证据不等同 macOS 手工可访问性验收 | Product/Design Owner | 签名 Tauri candidate 阶段执行 |
| 真实模型答案质量 | 不能声称附件提升回答质量 | Product/AI Owner | 批准模型、dataset 与 threshold 后 Eval |
| 签名、公证、生产资源、监控和回滚演练 | 不能进入 G5/G6 | Release Owner | 真实部署准备阶段补齐 |

## 7. 后续工作

| Issue | 内容 | 触发条件 | Owner |
|---|---|---|---|
| FEAT-127-REVIEW | Contracts semantic Owner/consumer review、PR/merge 与适用 release tag | 决定进入合并/发布流程 | 段成威 |
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
| G2A contract ready | PENDING | 2026-08-19 | full commit/pins and machine checks PASS；Owner/consumer review and release tag absent |
| G3 Slice Complete | PENDING | 2026-08-19 | automated gates PASS；user Desktop manual acceptance partial |
| G4 Code Complete | PENDING | 2026-08-19 | source commits pushed；complete manual acceptance、G2A and Reviewer approval remain |
| G5 Production Ready | N/A for current local scope, not passed | 2026-08-17 | no production preparation |
| G6 Delivery Complete | N/A for current local scope, not passed | 2026-08-17 | no deployment/smoke/observation |

- Desktop 人工验收候选形成时间：2026-08-18。
- 本地人工验收：2026-08-19 部分完成；等待 post-fix drag 与其余场景结果。
- 正式需求关闭时间：未形成；等待完整人工验收、G2A/Reviewer 决策；生产阶段仍不在当前范围。
