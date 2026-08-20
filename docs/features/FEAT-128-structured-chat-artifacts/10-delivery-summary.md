# FEAT-128 交付总结与关闭记录

## 1. 当前结果

- G2 closure rewrite、Product/Technical/Security/Data Owner sign-off 与 UI Pattern 1.0.0 `Accepted` 已完成。
- Contracts S1/S2 已形成真实、不可变、未发布的 `0.4.0` local candidate；locked generation、lint、test、
  build、双 baseline breaking、v1/v2 equality 与 semantic review 全部通过。
- Host/Desktop 只完成 downstream exact pin 与 conformance preflight；Artifact 业务 endpoint、staging、
  SQLCipher migration、native transfer、IPC v3 和 UI renderer 均未开始。
- G2A 已批准。下一步可以启动 S3，S3 conformance 后再启动 S4；真实 provider、tag、push、release、
  production 与 G3-G6 仍关闭。

## 2. 实际版本与提交

| Component | Version/status | Full commit | 说明 |
|---|---|---|---|
| Feature package | G2A approved | 本次 `yijie` 文档提交 | governance only |
| Desktop Pattern | Accepted 1.0.0 + G2A record | `35efa1475af4679b5974663593831d07759c3728` | design docs only；initial acceptance at `e97b2dab...` |
| Contracts | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | immutable；no tag/release |
| Agent Host | pin conformance PASS | `dea84d0768ebc017b7ee5faedab7f9a49ce74875` | no S3 business code |
| Desktop | pin conformance PASS | `96094419d963745529ed0fa246919089e659f20d` | no S4-S9 business code |

关键 source digests：OpenAPI `cf72ba8dd6910e8454ad60feeffa5e82583303b441dad78e49910fbdb9f5420f`，
event v3 `87b1284056529bde8314e6cfa6ad1fb27ffefef50ea86033875fda795330939f`，report v1
`94715e5b821cca686405d06004b805e9eac6d39dc61e19c9fc38925102f79556`，v3 Proto
`5021a0342b84cdea0e1dd773728e4c8f013ce7d03377ade18f06f6716a81b70d`。

## 3. 验收结果

| 范围 | 结果 | Evidence |
|---|---|---|
| Requirements/design traceability | PASS | 00-07 + Pattern Accepted + package checks |
| Contracts S1/S2 | PASS | `pnpm generate/lint/test/build`、39/39 Node + Go、双 breaking、semantic review |
| Host exact pin | PASS | sync/contract-check/lint/test at `dea84d...` |
| Desktop exact pin | PASS | generate-check/lint/test/build/docs at `960944...` |
| AC contract portions | CONTRACT PASS | lifecycle/resource/ACK/report/fixtures/negative cases |
| AC runtime/UI portions | NOT RUN | S3-S10 未开始 |
| Real provider capability | BLOCKED/UNKNOWN | 无付费调用或 authority |

## 4. 安全、数据与兼容边界

- v1/v2 wire、schema、fixtures 与语义保持不变；v3 使用显式 path 与 `event_schema_version=3`。
- Artifact content/poster/ACK、owner/session scope、relative href、MIME/size/digest、range 与 stable errors 已入契约。
- Report known sections strict；unknown 只允许 `required=false`、opaque、128 KiB/depth 8，禁止 HTML/URL/script。
- Host encrypted spool、24h TTL 与 ACK cleanup 仍待 S3 实现；Desktop commit+168h retention、native save/CSP
  与 cleanup receipt 仍待 S4/S7 实现。
- 四种 exact-local synthetic fixtures 已存在；真实 `provider|tool` activation 仍分 kind blocked。

## 5. G2/G2A Owner 结论

用户明确要求 Codex 将其 Owner 指令分别记录为 Product/Design、Technical、Security/Data 的
`G2 APPROVED`，并把 UI Pattern 改为 `Accepted`。用户还明确给出 G2A 条件：真实 generate、breaking、
semantic review 与 immutable pin 完成后才能开始 Host/Desktop。实际证据满足后，G2A 记录为
`APPROVED`。这是用户授权的 Owner capture，不是 Codex 自称独立人工批准。

| Gate | Decision | Date | Evidence |
|---|---|---|---|
| G0 Intake | PASS | 2026-08-20 | explicit request + 00/feature.yaml |
| G1 Design Ready | PASS | 2026-08-20 | 01-03 + repository investigation |
| G2 Implementation Ready | APPROVED for S1/S2 | 2026-08-20 | 03 §2A/2B + 04-07 + Pattern Accepted |
| G2A Contract Ready | APPROVED | 2026-08-20 | Contracts immutable candidate + dual breaking + semantic review + downstream exact pins |
| G3/G4 | PENDING | N/A | no Host/Desktop business implementation |
| G5/G6 | NOT PASSED | N/A | local-only scope has no release/deployment/production evidence |

## 6. 未验证项与已知限制

| Item | 状态 | 下一证据 |
|---|---|---|
| Host v3 route/staging/resource/synthetic producer | NOT RUN | S3 focused + full Host gates |
| Desktop SQLCipher/native transfer/history/private IPC | NOT RUN | S4 migration/security/conformance |
| image/video/file/report renderers | NOT RUN | S5-S9 component/visual/a11y |
| synthetic local vertical slice | NOT RUN | S10 E2E/security/performance/visual |
| MiniMax real image | BLOCKED | fixed provider capability + separate paid authorization/eval |
| real video/file/report producers | BLOCKED | per-kind authority/ownership/security design |
| release/deployment | N/A current scope | separate G5/G6 package if later requested |

## 7. 下一步与停止条件

1. 从 Host S3 开始：实现 v3 dual route、encrypted staging、content/poster/ACK、range、replay 与
   exact-local synthetic producer，继续默认关闭。
2. S3 conformance 通过后开始 Desktop S4：v8 SQLCipher、native transfer/ACK、history/private IPC 与 cleanup。
3. 任何 ACK、limits、retention clock、report compatibility、auth/CSP 或 authority 漂移先重开 G2；
   Contracts pin 漂移先重开 G2A。
4. 不启动真实 provider，不 tag/push/publish/release，不把 pin conformance 描述成 Code Complete。

## 8. 文档与交接

| Artifact | Path | Owner | 状态 |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-128-structured-chat-artifacts/` | 段成威 | G2A updated |
| Desktop UI Pattern | `yijie-desktop/docs/design/docs/design/05-patterns/14-feat-128-structured-chat-artifacts.md` | 段成威 | Accepted 1.0.0 |
| Contracts semantic review | `yijie-contracts/docs/reviews/FEAT-128-semantic-review.md` | Contracts Owner | PASS |
| Release/rollback plan | `09-release-and-rollback.md` | 段成威 | no release executed |

正式关闭时间尚未形成。当前准确状态是：`G2A Approved; S3/S4 authorized but not started; real providers and G3-G6 closed`。
