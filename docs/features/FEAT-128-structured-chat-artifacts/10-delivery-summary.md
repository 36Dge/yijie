# FEAT-128 交付总结与关闭记录

## 1. 当前结果

- G2 closure rewrite、Product/Technical/Security/Data Owner sign-off 与 UI Pattern 1.0.0 `Accepted` 已完成。
- Contracts S1/S2 已形成真实、不可变、未发布的 `0.4.0` local candidate；locked generation、lint、test、
  build、双 baseline breaking、v1/v2 equality 与 semantic review 全部通过。
- G2A 后严格先完成 Host S3：v3 dual route、bounded encrypted staging、owner-only content/poster、range、
  ACK/TTL/restart cleanup 与四类 exact-local synthetic producer。
- Host S3 通过后完成 Desktop S4：SQLCipher v8、closed event/report adapter、native transfer/commit/ACK、
  168h retention/delete、metadata-only history v3 与实现级 pin；没有 renderer、CSP 或 save。
- Desktop S5 已完成 provider-neutral identity/status/progress reducer、按 session/turn/Artifact 管理的 Pinia store
  与稳定 generic metadata shell/list；只消费 parser-approved metadata，没有 preview/action/wire parsing。
- S3/S4/S5 的 G3 slice gate 已通过。S6-S12、真实 provider、tag、push、release、production 与 G4-G6 仍关闭。

## 2. 实际版本与提交

| Component | Version/status | Full commit | 说明 |
|---|---|---|---|
| Feature package | G3 recorded for S3/S4/S5 | 本次 `yijie` 文档提交 | governance/evidence only |
| Desktop Pattern | Accepted 1.0.0 + G2A record | `35efa1475af4679b5974663593831d07759c3728` | design docs only；initial acceptance at `e97b2dab...` |
| Contracts | `0.4.0 local candidate` | `ea48fe190e18afba728712d1e2cc79cda57f581b` | immutable；no tag/release |
| Agent Host | S3 PASS; default off | `4017785adb08e1114781d3d844e9a10a683fa933` | pin base `dea84d...`; strict-local synthetic only |
| Desktop | S4/S5 PASS; default off | S5 `7548ea8aeacfd7274f1107786ce48ddc6789cd45`; S4 `09220dd8319cfb8ec0c4d1531514bb5169107983` | pin base `960944...`; generic shell only，no S6-S9 renderer/save/CSP |

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
| Host S3 | PASS | contract-check/lint/test/runtime-test at `4017785...` |
| Desktop S4 | PASS | generate-check/lint/test/build/docs at `09220dd...`; TS 276/276, Rust 184 pass/3 ignored |
| Desktop S5 | PASS | RED first；19 focused tests；`make lint/test/build`、`pnpm docs:build`、diff checks；TS 295/295, Rust 184 pass/3 ignored at `7548ea8...` |
| AC contract portions | CONTRACT PASS | lifecycle/resource/ACK/report/fixtures/negative cases |
| AC Host/native foundation portions | PARTIAL PASS | S3/S4 lifecycle/resource/persistence/history/retention conformance |
| AC generic shell portion | S5 FOUNDATION PASS | monotonic/closed reducer、history/live shared store、generic accessible metadata shell |
| AC type renderer/E2E portions | NOT RUN | S6-S10 未开始 |
| Real provider capability | BLOCKED/UNKNOWN | 无付费调用或 authority |

## 4. 安全、数据与兼容边界

- v1/v2 wire、schema、fixtures 与语义保持不变；v3 使用显式 path 与 `event_schema_version=3`。
- Artifact content/poster/ACK、owner/session scope、relative href、MIME/size/digest、range 与 stable errors 已入契约。
- Report known sections strict；unknown 只允许 `required=false`、opaque、128 KiB/depth 8，禁止 HTML/URL/script。
- Host encrypted staging、24h TTL 与 ACK cleanup 已在 S3 实现；Desktop commit+168h retention 与 cleanup
  receipt 已在 S4 实现。Native save/CSP/preview handle 仍待 S6-S8 独立安全切片。
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
| G3 Slice Complete | PASS for S3/S4/S5 | 2026-08-20 | immutable Host/Desktop commits + focused/full gates + diff/clean checks |
| G4 Code Complete | PENDING | N/A | S6-S11、全部 AC/E2E/独立 review 未完成 |
| G5/G6 | NOT PASSED | N/A | local-only scope has no release/deployment/production evidence |

## 6. 未验证项与已知限制

| Item | 状态 | 下一证据 |
|---|---|---|
| Host v3 route/staging/resource/synthetic producer | S3 PASS | S10 cross-process/restart walking skeleton |
| Desktop SQLCipher/native transfer/history/private IPC | S4 PASS | S10 integrated lifecycle |
| Desktop generic domain/store/shell | S5 PASS | S10 history/live integrated lifecycle + visual/performance evidence |
| image/video/file/report type renderers | NOT RUN | S6-S9 component/visual/a11y |
| synthetic local vertical slice | NOT RUN | S10 E2E/security/performance/visual |
| synthetic video playback/seek | NOT RUN | 当前 S3 MP4 fixture 无 `moov`，S7/S10 需可播放本地 fixture + controls/range smoke |
| MiniMax real image | BLOCKED | fixed provider capability + separate paid authorization/eval |
| real video/file/report producers | BLOCKED | per-kind authority/ownership/security design |
| release/deployment | N/A current scope | separate G5/G6 package if later requested |

## 7. 下一步与停止条件

1. S5 已完成且本轮不继续实施。下一计划切片为 S6 image renderer，必须由新的明确任务授权；不得顺带启动 S7-S12。
2. 后续按 S6-S9 分别处理 image/video/file/report；新增 CSP、native save/capability 前单独复核安全边界。
3. 任何 ACK、limits、retention clock、report compatibility、auth/CSP 或 authority 漂移先重开 G2；
   Contracts pin 漂移先重开 G2A。
4. 不启动真实 provider，不 tag/push/publish/release，不把 pin conformance 描述成 Code Complete。

## 8. 文档与交接

| Artifact | Path | Owner | 状态 |
|---|---|---|---|
| Feature package | `yijie/docs/features/FEAT-128-structured-chat-artifacts/` | 段成威 | G3 updated for S3/S4/S5 |
| Desktop UI Pattern | `yijie-desktop/docs/design/docs/design/05-patterns/14-feat-128-structured-chat-artifacts.md` | 段成威 | Accepted 1.0.0 |
| Contracts semantic review | `yijie-contracts/docs/reviews/FEAT-128-semantic-review.md` | Contracts Owner | PASS |
| Release/rollback plan | `09-release-and-rollback.md` | 段成威 | no release executed |

正式关闭时间尚未形成。当前准确状态是：`G3 PASS for S3/S4/S5 foundations; S6-S11 pending; real providers closed; G4-G6 not passed`。
