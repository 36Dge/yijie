# FEAT-132 原生机制调整验收记录

日期：2026-09-08；2026-09-09 新进展见 [来源固定与当前验证](04-source-freeze-and-d4-2026-09-09.md)。**源码实施候选已完成定向验证；真实应用验收/D4 NOT RUN。** 所有 Must AC 的正式状态仍为 pending，不能把组件测试累计为真实 D4。原 2026-08-27 验收见 [历史归档](history/2026-08-27/02-verification.md)，本次不继承其预算或 PASS。

## 已执行结果

| 验证 | 实际结果 |
|---|---|
| Rust `cargo test --lib feat132_` | 8/8：真实 SSE 解码→缓冲→SQLCipher、原生失败保留、UI history 只读、Host 换代恢复、旧行不升级、提交失败/未知响应不制造执行终态 |
| Rust `cargo test --lib chat::native_conversation::tests` | 4/4：多 Item / segment 交错、重复 cursor、最终值替换、Turn 不封口 Item、容量/投影异常不变失败 |
| Rust `cargo test --lib chat::application::tests::v2_turn_` | 2/2：本地冲突失败不重试、不绑定无关原生 Turn |
| Rust clippy | `cargo clippy --lib --tests -- -D warnings` PASS；default lib/test 编译通过 |
| Artifact feature 编译 | `cargo check --lib --features feat128-s10-runtime` PASS；不是 Artifact E2E |
| Host 原生协议 | `go test -race ./internal/session ./internal/app ./internal/codex -run '^TestFEAT132Native' -v` 12/12 PASS |
| Host 权限回归 | 模式映射、原生审批回调 roundtrip、已接受 operation replay 的 3 个安全定向测试 PASS；不等于权限 E2E |
| Host 静态与编译 | `go vet ./...` PASS；`go test ./... -run '^$'` PASS（只编译，未执行全量测试） |
| Vue / Pinia / timeline / client | 两批共 341/341：主链 279 项，旧读取/审批档案/帧批处理/权限 consumer 62 项；未包含 .local 源码快照 |
| 前端静态与构建 | `vue-tsc --noEmit`、目标 src/scripts ESLint、`pnpm build` PASS |
| 设计文档构建 | `pnpm docs:build` PASS；Vite 存在既有大 chunk 提示，未扩大到无关拆包 |
| 来源与删除门禁 | Desktop `pnpm check:native`、Contracts `pnpm check-generated:native`、跨仓 sync `--check` PASS；真实执行源中旧 reducer/hydrate/reconcile/fallback 符号扫描为空 |
| FEAT-137 永久退役 | `node scripts/check-approval-retirement.mjs` PASS，未激活 FEAT-137 |
| Contracts lint / compile | `pnpm lint`、TS noEmit、Go native SDK 编译 PASS；NativeEvent 为 SSE data schema，Redocly 有一条 unused-component 提示 |
| breaking check | 对 published `f16a497e1377f45747f8ff9292b4b60cf2027f88` 和工作区基线 `468aecec53cd708286988a221061a2e5ccd2479d` 均 PASS；不替代语义/端到端审查 |
| 元仓治理 | `pnpm lint` PASS；`pnpm test` 50/50 PASS；shell 语法检查 PASS |
| 独立审查 | 最后一轮无新的可复现 P1/P2；仅只读代码审查，没有独立执行测试或真实 UI |

测试明细和来源摘要见 [native-adjustment-checks-2026-09-08.json](evidence/native-adjustment-checks-2026-09-08.json)。Rust 与 Host 最终日志保存在同一 evidence 目录。

主要命令分别在各仓执行。所有 cargo 命令使用 `--manifest-path src-tauri/Cargo.toml`。Vitest 指定源测试路径，显式排除 `**/.local/**`、`**/.contracts-source/**`、`**/.agent-host-source/**`、`**/.skills-source/**`；早期一次误纳入 .local 旧源码快照的结果已废弃，未修改那些快照，也不计入最终 341 项。

全量安全生成曾发现既有 FEAT-137 compatibility TS SDK 与其旧 source 不同步。完整重生成后 check 曾通过，但本次将该无关生成产物恢复为开始时的确切 HEAD 字节；最终只声明原生子集 generation/check PASS，**不声明最终全量 generated check PASS**。未启用或修复已退役的 FEAT-137。

## 十项验收的证据与剩余条件

| AC | 已验证部分 | 正式验收仍待 |
|---|---|---|
| 001 原生 ID/phase/status/final | Runtime client 实际 JSONL RPC、Host conformance、Native SSE→SQLCipher、Vue 完整视图 | 固定真实 Runtime 完整运行 |
| 002 交错与重复 | 唯一 buffer 多 Item / part / cursor 测试 | 真正并发流现场 |
| 003 final 与 delta 不同 | Native final 直接替换、原生 ID 不变 | 真实模型样本 |
| 004 无自动封口 | Item complete 不结束 Turn；Turn failed 不改变未完成 Item | 正常中断真实验证 |
| 005 不伪造 failed | 元数据异常、未知 terminal、projection notice、容量、失联/未知提交结果定向覆盖 | 正常应用恢复场景 |
| 006 失败保留 | SQLCipher 正常 close/reopen、cold conflict、Host resume revision | 正常 Desktop 退出/重启 |
| 007 来源不混合 | 每 Turn 一个集合、native/legacy provenance、不同冷 ID 不 join | 真实 Legacy history 验证 |
| 008 消费者保持 | UI/附件 history/Command/Composer、权限及 Artifact 编译、scope/delete 定向回归 | 附件/Artifact/FEAT-152 真实 E2E |
| 009 无旧引擎 | 删除文件/调用链/开关扫描、独立审查 | 固定候选后最终发布差异审查 |
| 010 正常生命周期 | 暂无本候选真实桌面证据 | canonical 来源固定后启动、发送、切换、中断、正常退出重启 |

## 未执行项目、原因与影响

- **canonical 真实启动**：执行了正常 runner 调用的只读 preflight，实际错误为 `FEAT-152 Contracts source differs from its committed pin: scripts/generate.mjs`。新源码还未提交，Contracts generator 和 Host build inputs 尚未重新固定。未绕过或降低校验，未运行后续 bundle/Runtime 启动；因此不能声明当前桌面可正常启动。
- **视觉实机检查**：当前构建未通过 canonical 来源门禁，未执行亮/暗主题及 1180×760 最小窗口实机检查；已通过组件测试和前端构建，不以此替代原生视觉验收。
- **真实模型 / 新 D4**：本次明确 paid budget=0，未发送模型请求。旧 D4 额度和结果均不继承。
- **用户数据库切换、恢复/回滚与真实 Artifact/审批 E2E**：未在用户数据上执行；需要真实 pinned 构建后，先在旧版正常结束活跃 Turn，再正常退出并执行前向迁移。无来源的旧活跃行不会被自动升级或伪造结束。
- **既有广泛 make test / runtime-test / 全量 Rust 测试**：含 binary impersonation、故障强杀、权限破坏或攻击性 fixture 的家族按用户硬性条款跳过。没有执行攻击/危险资源注入。采用普通内存 JSONL、mock HTTP、正常临时 SQLCipher open/close/reopen 与有效普通文本替代；覆盖范围不能等同于原全量门禁。含 `<script>` 攻击字符串的旧 ChatTurnPlan 用例未运行。
- **全 features 测试编译**：早期 compile-only 检查遇到既有 sidecar test 的 SidecarConfig initializer 缺少 feat134/136/137 字段；没有扩大到修复无关 sidecar fixture。最终 default lib/tests 与 feat128-s10-runtime lib 已通过。
- **提交、推送、tag、部署、付费操作、Runtime patch/binary 更新**：均未执行，未获本任务书授权。

## 原生能力缺口

固定 Legacy history 不保存全部流式 delta、Command、plan 或 error，冷 ID 可能与实时不同，甚至冷 completed 与已观察 failed 冲突；本地 paginated history 不可用。已保存原生事实优先，缺失内容标记 partial，不能补造事实。Command 输出 delta 目前只报告 pending-final，最终安全正文来自 completed。容量限制仅影响显示，不制造 Runtime failed。

## 交付状态

代码、契约、前向迁移和当前文档均保留为未提交候选。yijie-codex 保持开始 HEAD 且工作树无变化。原生复用与删除/回滚说明见 [03-native-protocol-adjustment.md](03-native-protocol-adjustment.md)。后续正式来源固定和真实验证属于尚未完成的验收，不宣称整个 FEAT-132 已 D4 完成。
