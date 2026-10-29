# FEAT-162 — 准确来源本地提交清单

> 当前状态（2026-10-29）：第八代E1仍失败，累计3次模型HTTP、0REST、3元未知用量估算；Owner已暂停构建与收费验收，方案A清理完成。现已另行授权全仓Git提交/推送；完整当前状态见[34号](34-paused-state-and-cleanup.md)。下文授权与执行进度按历史时点理解。

2026-10-29。以下清单为当前可审查工作区差异，目标是满足准确App构建要求。Owner已明确回复“允许仅本地提交 FEAT-162，不推送”。据此按清单固化本需求及必要来源同步；推送、合并、tag及发布仍禁止。

顺序：Contracts本地来源提交→按真实新commit正规同步Connectors/Host/Desktop消费来源及资源→逐仓本地提交→独立新generation构建→准确App预检/收费/D4→最后仅FEAT-162文档证据提交。Skills与Runtime当前干净，保持原commit，不修改或提交。

后续正规同步仅限本需求已列消费契约/构建来源文件；若发现无关dirty，停止归并并单独保留。旧账本、生成日志、私有凭据、.local构建与备份不进入Git。

本次软预算实现6项普通测试通过；前轮全部生成/43项Contracts/计量与治理验证仍有原始记录。金额不再要求硬上界；本清单不申请额外收费授权。

## yijie-contracts（79 个当前路径）

- `.gitignore`
- `compatibility/artifact-media/source.lock.json`
- `compatibility/chat-models-v2/source.lock.json`
- `compatibility/chat-models/source.lock.json`
- `compatibility/experts-v2/source.lock.json`
- `compatibility/experts/source.lock.json`
- `compatibility/market-broker-control/control.json`
- `compatibility/market-broker-control/source.lock.json`
- `compatibility/market-broker-control/wire.schema.json`
- `compatibility/market-host-v2/source.lock.json`
- `compatibility/market-host-v2/transport.json`
- `compatibility/market-host-v2/wire.schema.json`
- `compatibility/market-host/source.lock.json`
- `compatibility/market-host/transport.json`
- `compatibility/market-host/wire.schema.json`
- `compatibility/market-provider/source.lock.json`
- `compatibility/native-turn-timing/source.lock.json`
- `compatibility/scheduled-draft/source.lock.json`
- `compatibility/web-retrieval/legacy/0.2.0/tools.json`
- `compatibility/web-retrieval/legacy/0.2.0/wire.schema.json`
- `compatibility/web-retrieval/source.lock.json`
- `compatibility/web-retrieval/tools.json`
- `compatibility/web-retrieval/wire.schema.json`
- `docs/contract-change-policy.md`
- `docs/full-generation.md`
- `docs/offline-breaking-checks.md`
- `docs/supported-baselines.md`
- `docs/web-retrieval-basic-pro-v03.md`
- `scripts/check-breaking.sh`
- `scripts/check-generated.mjs`
- `scripts/check-workflow-local.mjs`
- `scripts/generate-artifact-media.mjs`
- `scripts/generate-chat-models-v2.mjs`
- `scripts/generate-chat-models.mjs`
- `scripts/generate-core.mjs`
- `scripts/generate-market-broker.mjs`
- `scripts/generate-market-host-v2.mjs`
- `scripts/generate-market-host.mjs`
- `scripts/generate-native-turn-timing.mjs`
- `scripts/generate-scheduled-draft.mjs`
- `scripts/generate-web-retrieval.mjs`
- `scripts/generate.mjs`
- `scripts/generation-plan.mjs`
- `scripts/generation-workspace.mjs`
- `scripts/market-broker-source.mjs`
- `scripts/market-host-source.mjs`
- `scripts/market-host-v2-source.mjs`
- `scripts/prepare-breaking-inputs.mjs`
- `scripts/sdk-exports.json`
- `scripts/sync-feat162-local.mjs`
- `scripts/web-retrieval-source.mjs`
- `sdks/go/market-broker-control/types.gen.go`
- `sdks/go/market-host-v2/types.gen.go`
- `sdks/go/market-host/types.gen.go`
- `sdks/jsonschema/market-broker-control.schema.json`
- `sdks/jsonschema/market-host-native.schema.json`
- `sdks/jsonschema/market-host-v2-native.schema.json`
- `sdks/jsonschema/market-host-v2.schema.json`
- `sdks/jsonschema/market-host.schema.json`
- `sdks/jsonschema/web-retrieval.schema.json`
- `sdks/jsonschema/web-retrieval.tools.json`
- `sdks/rust/market-broker-control/types.gen.rs`
- `sdks/rust/market-host-v2/types.gen.rs`
- `sdks/rust/market-host/types.gen.rs`
- `sdks/rust/web-retrieval/types.gen.rs`
- `sdks/typescript/src/api/generated/market-host-native-validator.gen.js`
- `sdks/typescript/src/api/generated/market-host-v2-native-validator.gen.js`
- `sdks/typescript/src/api/generated/web-retrieval-validator.gen.d.ts`
- `sdks/typescript/src/api/generated/web-retrieval-validator.gen.js`
- `sdks/typescript/src/domain/market-host-native.generated.ts`
- `sdks/typescript/src/domain/market-host-v2-native.generated.ts`
- `sdks/typescript/src/domain/web-retrieval.generated.ts`
- `tests/feat162-owner-stop-contract.test.mjs`
- `tests/generation-workspace.test.mjs`
- `tests/market-broker.test.mjs`
- `tests/model-call-surfaces-v2.test.mjs`
- `tests/offline-breaking-inputs.test.mjs`
- `tests/rust-web-retrieval/src/lib.rs`
- `tests/web-retrieval.test.mjs`

## yijie-connectors（15 个当前路径）

- `Makefile`
- `api/market-broker-control.candidate.json`
- `api/market-broker-control.schema.json`
- `api/market-provider.candidate.json`
- `api/web-retrieval.candidate.json`
- `api/web-retrieval.schema.json`
- `api/web-retrieval.tools.json`
- `docs/kimi-web-retrieval.md`
- `worker/src/broker.rs`
- `worker/src/broker_generated.rs`
- `worker/src/gateway.rs`
- `worker/src/kimi_web.rs`
- `worker/src/kimi_web_content.rs`
- `worker/src/kimi_web_tests.rs`
- `worker/src/web_retrieval_generated.rs`

## yijie-agent-host（10 个当前路径）

- `api/feat162.local-candidate.json`
- `api/market-broker-control.candidate.json`
- `api/market-broker-control.schema.json`
- `api/market-host-v2.schema.json`
- `docs/feat162-basic-pro-local.md`
- `internal/codex/market_approvals.go`
- `internal/codex/market_approvals_test.go`
- `internal/codex/market_turns.go`
- `internal/contracts/marketbrokercontrol/types.gen.go`
- `internal/contracts/markethost/types.gen.go`

## yijie-desktop（33 个当前路径）

- `contracts/feat162.local-candidate.json`
- `contracts/market-host-v2-native.schema.json`
- `contracts/market-host-v2.schema.json`
- `docs/design/docs/design/05-patterns/02-chat-workspace.md`
- `docs/feat162-owner-stop.md`
- `eslint.config.js`
- `scripts/feat162-basic-pro-meter.py`
- `scripts/feat162-client-meter.py`
- `scripts/feat162-soft-budget-meter.py`
- `scripts/feat162_owner_stop.py`
- `scripts/feat164_primary.py`
- `scripts/test-feat162-basic-pro-meter.py`
- `scripts/test-feat162-observation-profile.py`
- `scripts/test-feat162-owner-stop.py`
- `scripts/test-feat162-soft-budget-meter.py`
- `src-tauri/src/chat/connectors/broker_generated.rs`
- `src-tauri/src/chat/connectors/host_v2_generated.rs`
- `src-tauri/src/chat/sidecar.rs`
- `src/api/generated/market-host-v2-native-validator.gen.js`
- `src/api/generated/web-retrieval-validator.gen.d.ts`
- `src/api/generated/web-retrieval-validator.gen.js`
- `src/components/chat/MarketChatActivity.vue`
- `src/components/chat/WebRetrievalResult.test.ts`
- `src/components/chat/WebRetrievalResult.vue`
- `src/composables/useMarketChat.test.ts`
- `src/composables/useMarketChat.ts`
- `src/domain/market-host-v2-native.generated.ts`
- `src/domain/web-retrieval-display.ts`
- `src/domain/web-retrieval.generated.ts`
- `tests/visual/feat-162/index.html`
- `tests/visual/feat-162/main.ts`
- `tests/visual/feat-162/preview.css`
- `tests/visual/feat-162/vite.config.ts`

## yijie（33 个当前路径）

- `docs/features/FEAT-162-kimi-web-retrieval/00-feature-brief.md`
- `docs/features/FEAT-162-kimi-web-retrieval/01-delivery-log.md`
- `docs/features/FEAT-162-kimi-web-retrieval/02-verification.md`
- `docs/features/FEAT-162-kimi-web-retrieval/04-resume.md`
- `docs/features/FEAT-162-kimi-web-retrieval/21-basic-pro-plan-audit.md`
- `docs/features/FEAT-162-kimi-web-retrieval/22-basic-pro-intent-routing-plan.md`
- `docs/features/FEAT-162-kimi-web-retrieval/23-requirements-gap-closure-reaudit.md`
- `docs/features/FEAT-162-kimi-web-retrieval/24-basic-pro-implementation-and-zero-cost.md`
- `docs/features/FEAT-162-kimi-web-retrieval/25-implementation-reaudit.md`
- `docs/features/FEAT-162-kimi-web-retrieval/26-offline-compatibility-and-zero-cost-followup.md`
- `docs/features/FEAT-162-kimi-web-retrieval/27-offline-compatibility-reaudit.md`
- `docs/features/FEAT-162-kimi-web-retrieval/28-next-plan-reaudit.md`
- `docs/features/FEAT-162-kimi-web-retrieval/29-next-implementation-and-verification.md`
- `docs/features/FEAT-162-kimi-web-retrieval/30-next-implementation-reaudit.md`
- `docs/features/FEAT-162-kimi-web-retrieval/31-real-app-soft-budget-plan.md`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/basic-pro-requirements-before-20261028.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/basic-pro-requirements-checks-20261028.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/eof-before-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/eof-checks-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/eof-component-ui-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/eof-projections-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/eof-ui-dark-1180.jpg`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/eof-ui-light-1180.jpg`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/implementation-before-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/implementation-checks-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/next-authorization-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/next-checks-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/requirements-reaudit-before-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/requirements-reaudit-checks-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/evidence/requirements-reaudit-plan-20261029.json`
- `docs/features/FEAT-162-kimi-web-retrieval/feature.yaml`
- `docs/features/FEAT-162-kimi-web-retrieval/history/00-feature-brief-before-basic-pro.md`
- `docs/features/FEAT-162-kimi-web-retrieval/history/feature-before-basic-pro.yaml`
