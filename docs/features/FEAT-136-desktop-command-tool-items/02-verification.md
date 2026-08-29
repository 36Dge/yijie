# FEAT-136 Demo 验证

> 当前 verdict：D0 governance PASS；Contracts slice complete；real-service 与 D4 NOT RUN；overall Feature in progress。
>
> 本文不会把 synthetic fixture、schema generation 或兼容检查写成 Host/Desktop/Runtime 真实能力。

## 1. D0 检查

| Check | Result | 实际事实 |
|---|---|---|
| Feature ID | PASS | 正式 feature 目录创建前无 FEAT-136，ID 可用 |
| schema/profile/exposure | PASS | schema v3 / demo_fast / local |
| Product/UX | PASS | 用户、问题、结果、主流程、7 个 UI 状态与 8 条可判定 Must AC 已冻结 |
| Contract classification | PASS | semantic；closed v4 使用显式协商 v5，不修改 v1 至 v4 |
| Runtime freeze | PASS | 0.144.6、0ce5902e、267 schema、固定 digest、experimentalApi=false |
| Scope exclusions | PASS | 无 Host/Desktop/Runtime 改动，无审批/FileChange/Diff/Artifact 合并，无真实 D4 |
| Tool gap | PASS | generic contract 可做；真实 Tool producer/GS-004 仍 blocked/not run，不阻塞 Command |
| Git protection | PASS | FEAT-138 治理 commit 已独立固化；其它已完成 commits 未改写 |

## 2. D0 与 Contracts focused checks

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| yijie | pnpm lint && pnpm test && pnpm feature:audit | 0 | PASS：10 repos、48 tests、15 committed claims；仅预期 legacy v1 warnings；当前未提交包另由 strict D0 gate 直接验证 | 2026-08-29 |
| yijie | strict D0 package check | 0 | PASS：schema v3 / demo_fast / local D0 gate | 2026-08-29 |
| yijie-contracts | scoped generation + repeated generated SHA comparison | 0 | PASS：Buf、Agent Host OpenAPI Go/TS、AsyncAPI、v5 JSON Schema TS；7 项 HASH_MATCH=true | 2026-08-29 |
| yijie-contracts | make lint | 0 | PASS：OpenAPI/AsyncAPI、15 JSON Schema、Buf、TS no-emit、Go vet | 2026-08-29 |
| yijie-contracts | safe Node suite / Go tests / direct TS build | 0 | PASS：63/63 Node（排除 archive fixture test）、go test ./...、tsc | 2026-08-29 |
| yijie-contracts | v1 equality / candidate + published breaking | 0 | PASS：v1 exact；两个 baseline 均无结构 breaking | 2026-08-29 |
| yijie-contracts | diff/protected/generated/semantic review | 0 | PASS：最终无 open P0/P1/P2；commit 3c3000a6fbe2f08ab2131a463a1691e867d661b1 clean | 2026-08-29 |

## 3. Contracts 验证矩阵

| Area | Required evidence | Current result |
|---|---|---|
| Command started/output/completed | canonical safe fixtures + schema/reducer conformance | PASS（Contracts）；real mapper NOT RUN |
| Command failed/declined | closed status/error fixtures | PASS（Contracts）；real Runtime vertical NOT RUN |
| Duplicate identity | same event_id consumed once | PASS（pure reducer model） |
| Legal duplicate text | identical text with distinct event_id retained twice | PASS（pure reducer model） |
| Output cap/truncation | 16 KiB delta、256 KiB complete/head-tail/unavailable snapshot、compact SSE 1 MiB | PASS（Contracts） |
| Secret/path boundary | closed field/path shape、cwd rejection、redaction order | PASS（contract shape/policy）；Host sanitizer NOT RUN |
| Tool progress/result/error | bounded metadata-only fixtures、Runtime is_error mapping | PASS（Contracts）；real Tool NOT RUN |
| Unknown Tool/event | fixed unknown sentinel；closed generic allowlist；unknown event discard/resync model | PASS（Contracts） |
| Protobuf semantic gate | Proto3 typed transport 必须拒绝所有 JSON-invalid message | PASS（contract/test）；Host/Desktop adapter NOT RUN |
| Completed reconciliation | authoritative completed snapshot and late-delta rule | PASS（pure reducer model） |
| v1-v4 compatibility | named-family isolation + v1 wire equality + dual breaking baselines | PASS |
| FEAT-138 exclusion | closed schema/proto/event/generic allowlist；不创建 FileChange/Diff fixture | PASS |

## 4. Must AC 状态

| AC | Result | 当前证据边界 |
|---|---|---|
| AC-001 | PENDING（Contracts partial PASS） | 真实 Command 下一批 |
| AC-002 | PENDING（Contracts reducer model PASS） | Host/Desktop conformance 下一批 |
| AC-003 | PENDING（Contracts completed model PASS） | persistence/hydration 下一批 |
| AC-004 | PENDING（closed shape/policy PASS） | Host sanitizer 下一批 |
| AC-005 | PENDING（Contracts shape PASS） | 真实 Tool blocked |
| AC-006 | PENDING（Contracts unknown model PASS） | Desktop parser 下一批 |
| AC-007 | PENDING（Contracts minimum shape PASS） | SQLCipher 下一批 |
| AC-008 | NOT RUN | UI/visual/a11y 全部在下一批 |

所有 Must AC 保持 pending。Contracts slice PASS 后也不得把本表改为完整 PASS。

## 5. 安全未执行项

- 未执行强杀、故障注入、权限破坏、可执行文件/binary 替换、fixture 提取或新增攻击载荷；这些行为由长期安全条款禁止。
- 初始标准门禁审计中，在识别前曾各调用一次 `make generate`、`node scripts/check-generated.mjs`、`make test`、`make build`；它们会创建或读取仓库预存 Zip Slip archive fixture。其机械 exit-0 结果不接受为 FEAT-136 证据，识别后未重跑，并改用定向生成、重复 digest、63 个非 archive Node tests、完整 Go tests 与 direct TS build。
- 未执行 Provider、模型、真实 Command、MCP、文件读写、生产写或公网访问。
- 未执行 FileChange/Diff synthetic event 或 fixture；不存在性只通过 source allowlist 静态审计证明。
- 影响：本批只能证明 Contracts source/generated 与确定性安全语义，不能证明 Host、Desktop、真实 Runtime、异常进程 cleanup 或 D4。

## 6. Worktree 与 diff

- yijie 治理起点：feat/feat-136-desktop-command-tool-items@67f219b6cf825357285215fcbaafb33c3978acb3。
- yijie-contracts 起点：feat/feat-136-desktop-command-tool-items@3832a6c5e99b2a6365f193280fdb887c8fdbc2de；最终 immutable local commit：3c3000a6fbe2f08ab2131a463a1691e867d661b1，clean。
- Host、Desktop、Runtime 只读且起始 clean。
- Contracts diff/protected/generated review PASS；最终 yijie governance commit 与各仓最终对账在本包提交后记录。

## 7. 结论

- D0：PASS。
- Contracts slice：COMPLETE / PASS（safety-compliant scoped gate）。
- Host/Desktop implementation：NOT STARTED。
- Real service / D4：NOT RUN。
- FEAT-136 overall：IN PROGRESS；不是 usable、implementation complete 或 Epic complete。
