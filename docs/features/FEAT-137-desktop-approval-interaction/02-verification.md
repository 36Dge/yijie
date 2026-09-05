# FEAT-137 — D0 与 source implementation 验证

> 2026-09-05 最终处置：Owner 永久终止，未完成验收。以下 BLOCKED、NOT RUN、pending 和 source PASS 均为原始证据，不继续补齐、不改写为通过。退役检查只验证保留功能与清理结果，不能兑换 FEAT-137 D4。

> 当前 verdict：**D0、Runtime stable sandbox provenance patch、Contracts v6 compatibility v3、Host/Desktop refreeze 与 clean-tree source conformance PASS；fresh real D4 的既有 BLOCKED 结论不变**。本批 D4 额度 0、真实调用 0；历史 canonical D4 累计仍为 4/7，decision POST为0，accept/cancel均未完成。

## 1. D0 checklist

| Check | Result | Evidence |
|---|---|---|
| Feature envelope | PASS | schema v3 / demo_fast / local；FEAT-137 四文件包 |
| Owner security decision | PASS | exact gate、on-request/read-only、唯一 Command、两个决定、TTL/reconnect/audit/v6 均已明确授权 |
| Product/user result | PASS | primary user、problem、真实结果、main flow 与 inline UI 已闭合 |
| UI states | PASS | idle/loading/success/empty/error/retry/cancel 及 pending/submitting/resolved 扩展状态均有定义 |
| Must planning | PASS | 10 条可操作 Must；全部保持 pending |
| Contract classification | PASS | breaking at pinned Runtime stable-wire consumer boundary；版本化 Contracts compatibility v3 → Host → Desktop；Yijie public v6与v1-v5保持不变 |
| Permission boundary | PASS | exact local-only；默认 never；read-only；无网络、写入、额外权限或 unsandboxed escalation |
| Data/audit boundary | PASS | pending memory-only；content-free 128/session；随 session 删除；raw 内容禁止进入 UI/log/copy/storage |
| External authorization | PASS | D0 真实调用、破坏性操作与 production writes 全部为 0/禁止 |
| Runtime freeze | PASS | Owner-authorized three-patch authority `acf2da55…` / 0.144.6；只增加必填 provenance，不改变执行权限、审批决定或 public v6 API |

## 2. Owner decision coverage

| Decision | D0 value | Implementation evidence |
|---|---|---|
| Gate/profile | exact local + demo_fast + FEAT-137；默认/非 local never | Host config/wire matrix与 Desktop exact entrypoint/sidecar gate source PASS；真实启动 NOT RUN |
| Runtime approval policy | stable on-request | Host thread/resume/turn wire focused PASS；真实 Runtime NOT RUN |
| Sandbox | always read-only；Runtime provenance必须存在，只有 `use_default` eligible | Runtime三值透传与Host缺失/未知/escalated/additional fail-closed focused PASS；执行权限未改变 |
| Command | single argv git rev-parse --is-inside-work-tree | Host exact prompt/mapper allowlist PASS；真实 producer NOT RUN |
| Cwd/shell | workspace root；无 wrapper/pipe/redirect/env/multi-action | Host canonical cwd + closed params/action negatives PASS |
| User decisions | accept once / cancel current turn | Host mapper/session single-response + ack + idempotency与 Desktop GET→single POST/no-retry source PASS；真实 vertical NOT RUN |
| TTL | 120 seconds；TTL 先胜时 single Runtime Cancel + stable expired；Runtime/Item/Turn cleanup 先胜时 resolved_elsewhere、no response | Host monotonic TTL、decision commit→late ack、deadline→cleanup deterministic races PASS；retained/HTTP window closed；自然 expiry NOT RUN |
| Reconnect | actions disabled；Host snapshot reconcile | Host owner-bound memory snapshot/closed generation与 Desktop disconnect/revoke/resync source PASS；自然 reconnect NOT RUN |
| Pending storage | Host memory only | Host source/focused PASS |
| Resolved audit | content-free；128/session；delete with session | Host bounded retention/timestamps/redaction/cleanup focused PASS |
| Contract | new negotiated public v6；versioned Runtime compatibility v3；v1-v5/public v6 unchanged | Runtime `acf2da55…`、Contracts `aeccf5d5…`、Host `078769a2…`、Desktop `56f88856…` immutable source conformance PASS |
| Real calls | D0 quota 0；2026-08-31 fresh D4 quota 7为历史授权；2026-09-01 provenance批quota 0 | 本批0；历史4/7；decision POST 0，剩余额度未用于本批 |

## 3. Baseline preflight

| Repository | Expected HEAD | Preflight |
|---|---|---|
| Runtime | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277` | clean / exact |
| Contracts | `87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` | clean / exact |
| Host | `96b1fa19783694aef583b614c492fd2b6b5c15cc` | clean / exact |
| Desktop | `7026b47828961e58854b06c822c9c9e11252260d` | clean / exact |
| yijie | `ed6e8cc6d4a0cc9e675f189be0973c38ad193e3a` | clean before this D0 diff |

当前 freeze checkpoint：Runtime `acf2da55d8a53175343aaf112e03368dfef9922a` / tree `97557e0bd736a91bbbf94ccfa11b57a4bbf23a74`；Contracts `aeccf5d561bd4259389cdb325bae84ce3e0dea86` / tree `7a864645bf552a8b7457b6338a30f6626ce15d3a`；Host `078769a22d035c2921e315e5776185bed6f7feeb` / tree `df7e5b6bc4994a1a4023793e766a87c7806f1e07`；Desktop `56f88856125d2affd98f4c0c984792d47b444ca7` / tree `2d580bbe70ebe537cbfc13dae0d9b50b57a007c8`。Runtime/Contracts/Host clean；Desktop immutable commit在隔离worktree clean且authority精确pin Runtime/Host/Contracts与stable artifact，主checkout仅保留未纳入的FEAT-151 dirty files。

## 4. Governance checks

| CWD | Command | Exit | Result |
|---|---|---:|---|
| yijie | `check-feature-package.sh --gate D0 .../FEAT-137-desktop-approval-interaction` | 0 | PASS：schema v3 semantics 与 D0 结构/语义门禁通过 |
| yijie | `check-feature-package.sh --strict --gate D0 .../FEAT-137-desktop-approval-interaction` | 0 | PASS：strict D0 门禁通过 |
| yijie | `check-feature-package.sh --strict .../FEAT-137-desktop-approval-interaction` | 0 | PASS：whole-package strict，无模板变量或未完成标记 |
| yijie | `pnpm lint` | 0 | PASS：10 个 repo entries 与 contract governance 有效 |
| yijie | `pnpm test` | 0 | PASS：48 passed、0 failed |
| yijie | `pnpm feature:audit` | 0 | PASS：仅 legacy schema-v1 warnings；审计 17 个 committed packages |
| yijie | `bash -n scripts/*.sh docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS |
| yijie | `git diff --check` | 0 | PASS |
| yijie-contracts | frozen SHA focused v1-v6/HTTP/Runtime compatibility + safety-compliant Node suite | 0 | PASS：25/25 + 88/88；不含既有攻击归档 fixture |
| yijie-contracts | frozen SHA `go test ./...`、`pnpm lint`、`pnpm check-generated:safe`、`pnpm build:safe`、legacy equality、双基线 breaking、clean-tree audit | 0 | PASS：immutable commit `2e490dea…`；详见 `docs/reviews/FEAT-137-semantic-review.md` 与 delivery log §8 |
| yijie-agent-host | `make test-feat137` | 0 | PASS：exact contract/generated/equality；Codex/Session/App focused race；desktop-host compile-only |
| yijie-agent-host | `make test-feat136` | 0 | PASS：v1-v5 equality超集检查、FEAT-136 Session/App race regression、Runtime adapter compatibility |
| yijie-agent-host | `make lint` | 0 | PASS：gofmt、go vet、shell syntax |
| yijie-agent-host | `git diff --check` | 0 | PASS |
| yijie-agent-host | deterministic deadline repair tests：commit-before-deadline/ack-after-deadline、late Runtime/Turn cleanup、generation/request/session teardown、retained/HTTP window negatives | 0 | PASS：non-expired terminal 固定使用 deadline 前 decision commit time；deadline 后 pending cleanup 归并 TTL winner |
| yijie-agent-host | repair commit clean-tree `make test-feat137 && make test-feat136 && make lint && git diff --check` | 0 | PASS：`118651804…` / tree `9ae73d7b…` clean |
| yijie-desktop | v6 authority checker、Web focused、Rust focused、pnpm lint/build、Cargo fmt/check、scoped strict Clippy、diff | 0 | PASS：`918bd26b…` clean；Web 291/291、Rust 19/19；raw Clippy 唯一命中 base 既有 type_complexity |
| Contracts→Host→Desktop | immutable clean-tree structured source conformance | 0 | PASS：原 TTL/ack P1 已闭合；exact gates、v6/v1-v5、closed mapping、single POST/no retry、SQLCipher/redaction/safe-copy、S10/dependency边界均通过；无剩余 P0–P2 |
| yijie-codex | FEAT-137 patch replay/source/focused/fmt/scoped Clippy/release build/schema generation/stable normal-EOF/authority | 0 | PASS：`acf2da55…` clean；stable request必填三值provenance，267-file schema；binary `84bb0445…`，manifest `e62d8210…`；无thread/turn/Provider/model |
| yijie-contracts | v3 focused 13/13、non-attack Node 80/80、Go、lint、safe generated/build、legacy equality、three-baseline breaking、clean audit | 0 | PASS：`aeccf5d5…` clean；历史v1/v2 digest与public v6不变；archive/Zip Slip与structured-artifact injection-invalid未执行 |
| yijie-agent-host | current `make test-feat137`、`make test-feat136`、`make lint`、diff、pinned Runtime integration | 0 | PASS：`078769a2…` clean；仅`use_default` eligible，其它 provenance fail closed；normal EOF、无Provider/model |
| yijie-desktop | isolated current v4/v6 authority、runner/v4 25/25、full non-attack Web、lint/typecheck/build、canonical stable bundle、diff | mixed | PASS for FEAT-137/runner：`56f88856…` clean audit；Runtime/Host stable artifact exact pin与原始stable build PASS；parent FEAT-137 Web 244/244、Rust 32/32保持不变；full Web 1070/1071，唯一FEAT-132 replay失败在base `7026b478…`同样存在；不计PASS也不属于本批回归 |
| yijie | current D0、strict D0、whole-package strict、lint、test、feature audit、shell syntax、diff | 0 | PASS：tests 48/48；18 committed packages；仅既有schema-v1历史warning；未跟踪FEAT-151 package未纳入 |

最终 source conformance 执行日期：`2026-08-31`。治理提交前重新运行直接 D0、strict D0、whole-package strict、lint、test与 feature audit；结果见本批最终 audit。

Contracts 的 post-commit 结果绑定完整 SHA `2e490dea4444ea1e33c2df1a5267b2bff5bfb8e6`，且 clean-tree authority audit PASS。默认 `pnpm test` / `pnpm generate` / `pnpm build` 未作为验收门禁，安全替代门禁范围已在 Contracts semantic review 中明确记录。历史独立复审误执行的 Zip Slip 运行继续排除；冻结提交后的验收只计入明确列出的非攻击性门禁，未重跑 archive suite。

## 5. 明确未执行项

- Canonical authority composition repair：`PASS`。Desktop `56f88856…`从历史immutable Git object校验v4 source/digest，当前Runtime `acf2da55…`、Host `078769a2…`与stable artifact由v6 checker提供实际运行authority；macOS Bash 3.2 nounset空数组入口已闭合；isolated clean-tree、原始stable build与focused门禁PASS。
- Fresh D4 canonical startup/build：`PASS`；真实approval vertical：`BLOCKED`。4次请求没有形成可操作的inline approval card：declined without action UI、direct Command completion without approval、generation failure、persistent waiting across normal reopen。
- Contracts v6 local immutable commit、clean-tree SHA audit 与 authority freeze：PASS；published tag/release：NOT RUN。
- Host consumer pin、source implementation、unit/race/contract conformance与pinned Runtime normal-EOF integration：PASS（immutable clean commit）；真实Provider/model vertical：NOT RUN。
- Desktop closed consumer、SQLCipher、inline UI source、lint/test/build：PASS（immutable clean commit）；真实 UI smoke：NOT RUN。
- 历史 App/Host/Runtime/Provider/model startup：PASS at canonical entrypoint；2026-09-01 provenance批没有启动Desktop/Provider/model，仅执行Runtime normal-EOF与Host integration；所有停止均为正常生命周期。
- Real accept/cancel：BLOCKED / NOT RUN；没有decision POST。普通Command item在正常重开后只hydration一次；真实approval hydration/cardinality仍NOT OBSERVED。
- Natural reconnect：OBSERVED for normal app close/reopen；approval replay、expiry：NOT OBSERVED，未注入或伪造。
- Light：OBSERVED at 100% generic task UI；dark、exact 1180×760、200%、approval keyboard/focus/aria-live/safe-copy与VoiceOver：NOT RUN，因为没有真实approval card。未更改系统辅助功能设置。
- D4：BLOCKED after historical canonical startup；本批NOT RUN、真实调用0；历史累计4/7，剩余3次未用于本批。
- Governance：D0、strict、lint、tests 48/48与17-package audit PASS；D4 closure gate正确拒绝未完成的Feature，未强行关闭Must AC。

## 6. Non-evidence 与限制

- Runtime provenance schema 与 Contracts/Host/Desktop source/focused tests不能证明真实 Provider 会自然产生 request或真实 vertical 已闭环。
- Runtime 可能发送的 experimental `availableDecisions` 不是 stable Yijie authority；Host 后续必须兼容忽略并使用 Owner-fixed decision set。
- FEAT-136 Command terminal/UI foundation 不能证明 approval pending/decision 闭环。
- synthetic fixture 只能证明 parser/reducer/UI，不得冒充真实 reverse request 或 D4。
- Runtime/Contracts/Host/Desktop local commits 已建立 immutable source authority/conformance；Desktop 主checkout另有未纳入的FEAT-151 dirty files；真实 vertical 和 published/supported release仍未建立。
- Canonical stable runner 的v4/v6 authority composition已修复并冻结；当前阻断转移到真实producer/task lifecycle、Host pending与Desktop inline action authority未能闭环。
- `decline-and-continue`、session approval、network/permission amendment、CAP-020/021 与 FileChange/Diff 均不在第一阶段。

## 7. 结论

- D0：PASS（Owner decision、四文件包、依赖重基线与静态治理门禁均完成）。
- Runtime local immutable patch authority / artifact audit：PASS（`acf2da55…` / 0.144.6）。
- Contracts local immutable authority / clean-tree audit：PASS（`aeccf5d5…`）。
- Feature：active。
- Contract authority / immutable commits：PASS；`contract.status=PASS`。Host 与 Desktop exact consumer pins PASS；public v6 API与权限语义不变。
- Component source implementation/conformance与canonical entrypoint repair：PASS；aggregate Feature implementation仍BLOCKED于真实approval authority。live verification、D4与十条Must AC保持BLOCKED/NOT RUN/pending；真实调用4/7、decision POST 0。
- Epic：未完成；不代表 production approval ready。
