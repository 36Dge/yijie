# FEAT-127 契约与兼容变更计划

## 1. Contract Impact 结论

- 分类：`semantic`。
- 理由：新增 `/v2/agent-sessions/{agent_session_id}/turns` 和可选 Chat `contentBlocks`，并保留 v1 turn request、v1 paths 与既有 `ChatMessage.content`；但有序 block、七天 Context 资格、进度顺序、草稿归属和 v7 恢复/清理规则改变跨进程与持久化重放语义，因此按最高风险分类为 semantic。
- 边界：Desktop IPC v2、Agent Host HTTP v2、Host 到固定 Runtime `turn/start` 的 `UserInput[]` 投影，以及跨版本历史内容块。
- 业务/安全语义变化：新增 confidential 附件上下文、七天失效、顺序保持和 turn 幂等；不扩大 Runtime `read-only / approvalPolicy=never` 权限。

如果实现修改 v1 required 字段、向 v1 返回新封闭变体，或让旧 reader 无法读取旧消息，分类必须升级为 `breaking`。

## 2. 权威源与责任

| 契约/边界 | 权威源 | Repository/path | Producer | Consumers |
|---|---|---|---|---|
| Host v2 turn | OpenAPI | `yijie-contracts/openapi/agent-host/agent-host.yaml` | Agent Host | Desktop |
| Chat history blocks | JSON Schema | `yijie-contracts/jsonschema/chat/message.schema.json` | Desktop repository/IPC | Desktop store/UI |
| Runtime input | pinned upstream schema | `yijie-codex` `0.144.6`, `turn/start` `UserInput` | Agent Host | Codex Runtime |
| Desktop persistence | private migrations | `yijie-desktop/src-tauri/migrations/chat/0006_chat_attachments.sql` + `0007_chat_attachment_draft_targets.sql` | Desktop | later Desktop versions |
| Attachment import progress | Desktop private Tauri event schema | `yijie-desktop/src-tauri/schemas/chat-ipc-v2.schema.json` | Desktop native | Desktop store/UI |

SDK、fixture、Host adapter、IPC DTO 和数据库行均为派生表示，不成为第二权威源。

## 3. Host v2 语义

### Request

- `operation_id`：required UUID；以 `(agent_session_id, operation_id)` 为范围。
- `content_blocks`：1..16 个有序 closed union；`text | image | file`，其中 image/file 合计不超过 10 项。
- image：JPEG/PNG/WebP/GIF data URL；单项 decoded bytes 不超过 10 MiB，全 turn image bytes 不超过 10 MiB；media type、decoded size与 SHA-256 必须一致。
- file：只携带安全名称、媒体类型、大小、SHA-256 和 Desktop 选出的 context chunks；Host 永不接收原文件字节或路径；全部 chunks UTF-8 合计不超过 256 KiB。
- `reasoning_effort`：沿用 `none | high`；省略等价 `none`。
- 认证：沿用本机 owner-only bearer；tenant/user 字段仅为 correlation，不授予权限。

### 幂等与错误

- 相同 session、operation ID 和 canonical ordered input：返回原 `turn_id`，不得再次调用 Runtime。
- 相同 session、operation ID 但 canonical input 不同：`409 turn_operation_conflict`。
- 活跃 turn：`409 turn_active`；session 不可用：`409 session_not_usable`。
- 非法 block、聚合超限、data URL/magic/size/hash 不符：`400 invalid_request`。
- Runtime 拒绝或 transport 失败：沿用 `502 runtime_request_failed`；不回显内容、路径或 provider 原文。

## 4. Chat 历史语义

- `content` 继续 required，作为旧 consumer 的纯文本投影。
- `contentBlocks` 为 optional ordered blocks；旧消息没有该字段时新 consumer 合成一个 text block。
- 附件历史只含 opaque ID、安全名称、媒体类型、大小、状态与到期时间；不含路径、BLOB、解析正文、data URL 或 chunks。
- 已发送附件状态只允许 `bound | expired`；到期保留 metadata 与顺序，内容不可再构造 Context。

## 5. 兼容方向

| Version combination | Expected | Evidence |
|---|---|---|
| old Host + old Desktop | v1 文本路径不变 | v1 wire equality |
| new Host + old Desktop | old Desktop 继续调用 v1 | Host v1 regression tests |
| new Host + new Desktop | Desktop 只在 v2 route ready 后发送 blocks | provider/consumer conformance |
| old Host + new Desktop | readiness/version 不支持时 fail closed，不降级丢附件发送 | Desktop failure tests |
| old DB + new Desktop | v6 expand + v7 draft target；旧消息合成 text block | migration/history tests |
| v6 candidate DB + v7 Desktop | 保留 bound history；删除无法安全归属 composer 的 ready 草稿 | populated-v6 migration test |
| v7 DB + old Desktop | old reader 对 future schema fail closed；不支持就地降级 | 迁移前完整加密备份恢复演练，或 v7 roll-forward |

顺序固定为 contract candidate -> Host provider -> Desktop consumer -> local activation。没有多仓同时硬切。

## 6. 支持基线、Generator 与 Digest

| Item | Value |
|---|---|
| supported breaking baseline | `contracts-v0.2.0` / `f16a497e1377f45747f8ff9292b4b60cf2027f88` |
| local implementation baseline | `yijie-contracts@98e89d8cccfe15256f09e9329d4bc1980d6da578` |
| planned version | `contracts-v0.3.0` semantic candidate；未 tag |
| OpenAPI digest | `3d2f2273160aa05112f63d67f170229780d4526d679cd449a267890a933ea177` |
| Chat schema digest | `3f277898f8204e02a400053cd56bec3b0eeb37ed2c50db3a6347e7fec61ddf34` |
| canonical turn fixture digest | `ec464ce56f749852e65be8d1472d8f5d8cccc82c89d2dd16fab33fbdbe62decc` |
| generators | `openapi-typescript 7.13.0`; `oapi-codegen v2.7.2`; repository-pinned Protobuf/JSON Schema generation；Desktop Rust generator 为 `N/A`，由 `EXC-127-002` 管理手写 adapter |
| immutable contract commit/tag | full commit `747cf740f2d91e76e5c1a130e8e009f1efa821b8` 已形成并推送；release tag 未形成，candidate 尚非 supported/release-ready |
| downstream exact pin | Host `e2f0f5d...` 与 Desktop `2cb4ffd...` 均固定 `747cf740...` |
| Desktop adapter/readiness digest | `host_bridge.rs` `c6e90e0e8eff736101fd2cf9eea39cf70064f9c59ab0bcd90b2e2fc9286e221d`; `chat/mod.rs` `9a0702519eb8ad39cab72aa6adf5b1e2bdc72103b84c92cc0b38e0f05b0a444a` |

## 7. Canonical Fixtures 与 Conformance

| Fixture/test | Authority | Purpose | Status |
|---|---|---|---|
| `tests/fixtures/agent/host-v2/turn-request.json` | contracts | ordered text/file/image + idempotency request；严格可解码 PNG | PASS schema/Go decode/size/SHA；digest `ec464ce5...` |
| `tests/agent-turns-v2.test.mjs` | contracts | closed union、bounds、v1 isolation | PASS |
| `tests/chat-message-multimodal.test.mjs` | contracts | legacy projection + attachment history | PASS |
| Host request/Runtime mapping tests | Host | semantic validation、order、idempotency、no persistence | PASS：race suite + fixed Runtime/local fake Responses vertical slice |
| Desktop HostBridge/contract lock tests | Desktop | source-aligned wire and fail-closed mapping；手写 Rust adapter 不冒充生成 DTO | PASS：Redocly+Ajv、byte-identical fixture、adapter/readiness digest、expiry/negative tests、Rust canonical serialization、v2 wire/order/hash、lost response、invalid 202、typed conflict |

## 8. 历史契约检查证据与重验要求

下表是 2026-08-17 保存的本地 candidate 输出，不替代 2026-08-18 修复后的最终重验；当前结果须以 `08-verification-report.md` 的最新记录为准。

| Check | Command | Exit | Result |
|---|---|---:|---|
| generate | `make generate` | 0 | OpenAPI、Protobuf 与 9 个 JSON Schema SDK sources 生成成功 |
| lint | `make lint` | 0 | OpenAPI/AsyncAPI/JSON Schema/Proto/TS/Go PASS |
| test | `make test` | 0 | 31 Node tests + Go tests PASS；29 个生成文件 current |
| build | `make build` | 0 | 重新生成后 TypeScript SDK 编译 PASS |
| breaking | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | 0 | OpenAPI、AsyncAPI、JSON Schema 无结构性 breaking |
| v1 equality | `pnpm check:v1-wire f16a497e1377f45747f8ff9292b4b60cf2027f88` | 0 | 2 Public + 7 Host v1 paths/reference closure equal |

## 9. Gate 2A 与评审

- 机器契约候选：2026-08-19 对最终 commit source 重跑 generate、lint、test 与 supported-baseline breaking check，全部通过；Go `kin-openapi` 兼容回归也已覆盖。
- Semantic Owner/consumer review：`APPROVED FOR LOCAL CANDIDATE`。段成威作为 Contracts/Host/Desktop Owner 于 2026-08-19 明确批准，Contracts release note 与 supported baseline 已记录；自动 breaking check 不冒充该人工语义结论。
- 不可变 full commit 与下游 pin：`FORMED, PUSHED AND VERIFIED`；Contracts `747cf740...` -> Host `e2f0f5d...` -> Desktop `2cb4ffd...`。release tag 未形成，因此不能声称已发布或 supported。
- Desktop Rust generator：`N/A`；`EXC-127-002` 固定 adapter/readiness 源摘要、schema/fixture conformance、Owner、期限和移除触发，自 2026-11-18 起自动闭门。
- Gate 2A：`PASS WITH EXCEPTION (EXC-127-002) FOR LOCAL CANDIDATE`。tag 是后续正式发布身份，不是本地 G2A 前置；`contracts-v0.3.0` tag 与 supported/release-ready 状态保持 `PENDING`。
- Reviewer approval：段成威在当前任务于 2026-08-19 明确要求记录本地候选 Reviewer 批准；范围仅 G4 code-complete，不批准 PR、merge、tag、signed build、release 或 activation。
