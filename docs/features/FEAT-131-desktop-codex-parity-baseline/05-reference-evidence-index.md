# FEAT-131 — 设计依据与验证索引

> Reference policy：`codex-inspired-approximate-parity-v1-2026-08-27` / `owner-approved-inference`
>
> Runtime baseline：原始 freeze `0ce5902…`；Owner-authorized FEAT-136 minimal producer patch 后最终 re-freeze `b2b20e2…` / `yijie-codex 0.144.6` / `experimentalApi=false`
>
> 当前结论：Codex Desktop 人工媒体、App version/build 和 UI Freeze 均不再需要。后续 Feature 以 Owner 批准的近似策略、Yijie UI 规范和可核对的 Runtime/Host/Desktop 事实实施；current real smoke、真实 safe failure/retry 与 scoped diff review 已完成，FEAT-131 D4 `PASS`。

## 1. Design basis 与 provenance

| Value | 类型 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| `owner-approved-inference` | 设计依据 | Owner 允许开发推测 Codex-inspired 的布局、信息层级和交互 | 不是视觉实测、版本专属事实或完全一致承诺 |
| `owner-excluded` | 产品范围 | Owner 已明确不实现该能力 | 不表示等待参考证据或等待后续 Feature |
| `real-runtime` | 执行 provenance | 固定 Runtime/Host/Desktop 正常路径的真实结果 | 不能证明参考 App 行为 |
| `synthetic` | 执行 provenance | test-only parser/reducer/UI 状态机的可重复行为 | 不能证明真实 producer 或 supported projection |
| `implementation extension observed` | 代码事实 | 代码中存在、但未进入 compatibility manifest 的路径 | 不是受支持投影承诺 |
| `NOT RUN` | 验证状态 | 尚未执行或未取得结果 | 不能写成 PASS |
| `BLOCKED` | 验证状态 | 当前依赖 Owner 决策、未投影能力或固定 Runtime 边界 | 不得用模拟生产事件绕过 |

`owner-approved-inference` 与 `real-runtime`/`synthetic` 位于不同轴：前者描述设计依据，后两者描述执行证据。catalog 和 harness 必须通过固定 policy ID 保持二者分离。

## 2. Owner 范围与参考策略

| ID | Fact / artifact | Authority | Status | Notes |
|---|---|---|---|---|
| BASIS-001 | Codex-inspired approximation；无需一模一样或逐像素一致 | `references/reference-inference-policy.md`、`00-feature-brief.md` | `owner-approved-inference` | Yijie UI 规范优先；实现不得宣称版本实测 |
| BASIS-002 | 不再采集或要求 Codex Desktop 人工媒体、App version/build、UI Freeze、hash、drift 或补采清单 | `references/reference-inference-policy.md`、`feature.yaml` | approved | 缺少人工材料不是 blocker |
| BASIS-003 | 先前提供的全部人工材料已撤回；仓库副本及派生记录已删除 | `01-delivery-log.md`、`references/reference-inference-policy.md` | rescinded / removed | 不保留材料内容、身份、hash 或观察结论；不参与设计和验收 |
| BASIS-004 | Owner 排除语音、模型版本信息、模型推理强度信息、分享、切换置顶摘要、显示侧边面板、分支到新聊天、GS-006 File modification & Diff | `feature.yaml`、`00-feature-brief.md`、`03-capability-matrix.md` | `owner-excluded` | 共 8 项；模型推理强度信息不等于 CAP-011 reasoning summary |

本节是产品设计 authority，不是 Codex Desktop 观察记录。仓库中不应存在参考客户端媒体目录、capture manifest、人工采集清单、App build metadata freeze 或 supersession history。

## 3. Runtime、Contracts 与 Host 权威事实

### 3.1 固定 Runtime 身份

| Evidence ID | Fact | Authority | Status |
|---|---|---|---|
| EVID-RT-001 | 原始 fork freeze、upstream tag/commit、Runtime `0.144.6`、stdio、`experimental_api=false`、267 个 schema 与 schema tree SHA-256 | `references/runtime-freeze-evidence.md`、FEAT-131 original D4 evidence | historical original freeze `0ce5902…` |
| EVID-RT-002 | upstream tag/commit、Runtime version、toolchain、target、`experimentalApi=false` 与 stdio | `yijie-codex/.yijie/schemas/app-server/baseline.json:3-9` | fixed / read-only |
| EVID-RT-003 | 实施前 Runtime HEAD、clean worktree、schema hash 与“不 fetch/pull/rebase/build/upgrade”边界 | `references/runtime-freeze-evidence.md:7-21` | captured-before |
| EVID-RT-004 | FEAT-131 实施后原始 Runtime/manifest 精确对账 | `references/runtime-freeze-evidence.md:33-49` | historical `PASS` at `0ce5902…` |
| EVID-RT-005 | Owner-authorized FEAT-136 minimal early-denial producer patch 后的 final commit、upstream/version/schema digest 与 compatibility 精确对账 | `yijie-contracts/compatibility/agent-host-runtime-v1.json:4-13`；FEAT-136 `00-feature-brief.md` §2 | final re-freeze `b2b20e2…`；0.144.6；267 schemas；同一 tree digest；此后 read-only |

### 3.2 固定 Runtime stable surface

| Evidence ID | Capability group | Authority | Interpretation |
|---|---|---|---|
| EVID-SCHEMA-001 | `thread/start`、`thread/resume`、`thread/fork`、`thread/archive`、`thread/list`、`thread/read` | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ClientRequest.json:4870`、`:4894`、`:4918`、`:4942`、`:5254`、`:5302` | stable methods present；不表示当前 Host 已投影 |
| EVID-SCHEMA-002 | `turn/start`、`turn/steer`、`turn/interrupt`、`review/start` | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ClientRequest.json:6023`、`:6047`、`:6071`、`:6095` | stable methods present；不表示当前 UI 已实现 |
| EVID-SCHEMA-003 | thread status、turn diff/plan、assistant/command/file/MCP/reasoning delta notifications | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ServerNotification.json:5787`、`:6087`、`:6107`、`:6207`、`:6311`、`:6352`、`:6412`、`:6612`、`:6652` | schema presence 不等于 supported projection；FileChange/Diff 已被 Owner 排除 |
| EVID-SCHEMA-004 | Command/FileChange approval、MCP elicitation、permission approval、dynamic tool server requests | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ServerRequest.json:1796-1846`、`:1873-1946` | 只保留 schema 事实；GS-005 仅涵盖 Command approval，FileChange approval 已排除 |
| EVID-SCHEMA-005 | `item/tool/requestUserInput` 在 non-experimental schema 中存在，但带 EXPERIMENTAL 协议注释 | `yijie-codex/codex-rs/app-server-protocol/src/protocol/common.rs:1474-1478`；generated `ServerRequest.json:1848-1871` | 保持 `requires Host/Contracts projection`，不归因为 `experimentalApi=false` |
| EVID-SCHEMA-006 | ThreadItem 包含 user/agent、plan、reasoning、command、file、MCP/dynamic/collab/subagent、web/image/sleep/review/compaction | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ServerNotification.json:3974-4679` | 每项必须独立判断 producer、projection 和产品范围 |

### 3.3 当前 supported Host projection 与实现扩展

| Evidence ID | Fact | Authority | Status |
|---|---|---|---|
| EVID-HC-001 | local HTTP/SSE、owner-only bearer、read-only、approval `never` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:15-19` | supported projection |
| EVID-HC-002 | 锁定的 7 个 Runtime methods 与 13 个 notifications，包含 Command output delta、MCP Tool progress、reasoning text delta 与 turn plan update | `yijie-contracts/compatibility/agent-host-runtime-v1.json:20-43` | final supported projection at Contracts v0.7.0 |
| EVID-HOST-001 | Session methods 与固定 `never` / `read-only` | `yijie-agent-host/internal/codex/session_protocol.go:19-44` | implementation agrees with baseline |
| EVID-HOST-002 | `thread/delete` 与 dynamic `generate_image` 常量/路径 | `yijie-agent-host/internal/codex/session_protocol.go:19-28`、`:171-215` | `implementation extension observed`，不提升为 locked projection |
| EVID-HOST-003 | generic Item mapper 保留 item type，但只对 agent text/reasoning 做有限内容处理 | `yijie-agent-host/internal/session/service.go:543-630` | command/tool/file/phase 详细语义未投影 |
| EVID-HOST-004 | completed/error/warning 到 Host event 的终态与安全消息映射 | `yijie-agent-host/internal/session/service.go:631-706` | 当前基础 Turn/error projection |

任何只存在于 schema、但没有进入 EVID-HC-002 的事实，不能写成当前 Host supported projection；实现扩展也不能反向修改 compatibility manifest 的含义。

## 4. 当前 Desktop 与真实运行事实

| Evidence ID | Fact | Authority | Current support |
|---|---|---|---|
| EVID-DESKTOP-001 | Live wire 仅有 assistant/reasoning append、turn state/terminal、cleanup、resync、context invalidation | `yijie-desktop/src/domain/chat-ipc.ts:446-488` | 基础 stream/reasoning/terminal/resync；无 command/tool/diff/approval item |
| EVID-DESKTOP-002 | Store 校验 context/subscription/session、sequence/event ID，并聚合 assistant/reasoning；terminal 后 resync | `yijie-desktop/src/stores/chat.store.ts:808-872` | 可做 deterministic replay；未知/缺口触发保守 resync |
| EVID-DESKTOP-003 | streaming 时发送和附件禁用 | `yijie-desktop/src/components/chat/ChatComposer.vue:73-83` | 当前无 active-turn steer composer |
| EVID-DESKTOP-004 | Enter 发送、Shift+Enter 换行、IME composing 时不提交 | `yijie-desktop/src/components/chat/ChatComposer.vue:141-149` | 基础键盘交互存在 |
| EVID-DESKTOP-005 | reasoning disclosure、assistant stream、Artifact list、停止/失败终态 | `yijie-desktop/src/pages/chat/ChatPage.vue:499-552` | Artifact 不能代替 Runtime Diff；FileChange/Diff 不实现 |
| EVID-DESKTOP-006 | Composer interrupt wiring 与只读权限说明 | `yijie-desktop/src/pages/chat/ChatPage.vue:577-633` | Stop 与策略说明存在；没有 Runtime Command approval action |
| EVID-DESKTOP-007 | 自动跟随、回到底部、reduced motion、分页位置保持 | `yijie-desktop/src/composables/useChatScroll.ts:11-70` | 基础长对话滚动存在；近似目标由 FEAT-141 完成 |
| EVID-DESKTOP-008 | stable closed launcher、隔离 identity/data root、MiniMax 文本 Provider、image tool disabled、Desktop cleanup policy | `yijie-desktop/package.json`、`scripts/run-local-demo-fast.sh`、`src-tauri/tauri.feat131-stable.conf.json`、`src-tauri/src/lib.rs`、`src-tauri/src/chat/sidecar.rs` | canonical local 入口；不证明 Host 内部 fallback |
| EVID-REAL-001 | canonical `/readyz` 与 `/v1/status`、正常 `Cmd-Q` | `02-verification.md` §2 | startup `PASS`：Runtime `0.144.6`、MiniMax-M3、`experimental_api=false`；正常退出后端口/owned processes 清空 |
| EVID-REAL-002 | current canonical 单次受限 UI submission；精确终态文本保存在隔离 local conversation 数据中并登记在验证文档 | `02-verification.md` §2、`feature.yaml.verification.real_smoke` | `real-runtime: PASS`：精确返回 `FEAT-131_SMOKE_OK`，无工具调用、无重试；该已保存结果是 D4 local Artifact，不是 Codex 参考媒体 |
| EVID-REAL-003 | stable-only 第二实例 fail-closed 与 canonical retry/restart | `02-verification.md` §2、`feature.yaml.verification.representative_failure` | `real-service: PASS`：第二实例 exit 1/already-running；首实例保持 ready；退出后 canonical restart 再次 ready，最终正常清理 |
| EVID-REAL-004 | predecessor 单次 UI submission 与脱敏 Runtime 事件聚合 | `02-verification.md` §2 | `pre-runtime: FAIL`；历史失败保持独立，未改写成 current PASS |

### 4.1 FEAT-136 后续 Command 与 Tool foundation 证据

以下记录发生在 FEAT-131 D4 之后；上表原始 Desktop/Host 行保留其捕获时事实，不追溯改写。

| Evidence ID | Fact | Authority | Current support |
|---|---|---|---|
| EVID-F136-001 | final Runtime/Contracts/Host/Desktop commits、cross-pins、stable artifact digest/version 与 clean audit | FEAT-136 `00-feature-brief.md` §2、`02-verification.md` §1 | `PASS`；Runtime final re-freeze `b2b20e2…`；Contracts `87f94c9…`；Host `96b1fa1…`；Desktop `7026b47…` |
| EVID-F136-002 | fresh real Command completed 与 failed terminal/cardinality、exit/duration/stable error | FEAT-136 `02-verification.md` §3；yijie evidence commit `3a6b37ee708a71af561929429fdcf778d5667c32` | `real-runtime: PASS`；completed=1、failed=1；historical calls 1/5 |
| EVID-F136-003 | Command closed safety projection、safe copy、normal SQLCipher reopen/hydration 与 core UI | FEAT-136 `02-verification.md` §3 | `real-runtime: PASS`；each terminal once；light/keyboard/status/icon/aria-live/200% PASS |
| EVID-F136-004 | live started/output-delta、event_id、late event、natural replay、unknown/resync、dark 与 exact 1180×760 边界 | FEAT-136 `02-verification.md` §5 | `NOT OBSERVED` / `NOT RUN`；分别转 FEAT-142/143，不伪造 PASS |
| EVID-F144-001 | producer-neutral Tool contract/Host/Desktop foundation 与 real product boundary | FEAT-144 four-file package；FEAT-136 `01-delivery-log.md` §3 | generic source conformance `PASS`；Owner producer/entrypoint/security decision `BLOCKED`；real Tool / GS-004 / D4 `NOT RUN` |

这些事实只能证明 Yijie 当前实现或本次 local 运行，不能把 `owner-approved-inference` 升级成外部参考观察。

## 5. 黄金场景账本

`04-golden-scenarios.md` 是场景定义 authority。每个稳定 ID 只有一个账本行。`scenario-catalog.json.variants` 表示要求全集；只有同时出现在 catalog `replayedVariants` 与 fixture `coveredVariants` 的 variant 才可写 `synthetic: PASS`。

| Scenario | Reference basis | Yijie evidence status | Primary anchors | Owner |
|---|---|---|---|---|
| GS-001 普通流式完成 | `owner-approved-inference` | streaming/completed `synthetic: PASS`; current `real-runtime: PASS`; predecessor `pre-runtime: FAIL` | EVID-SCHEMA-002/003、EVID-HC-002、EVID-DESKTOP-001/002、EVID-REAL-001/002/004 | FEAT-134、FEAT-135 |
| GS-002 过程更新/reasoning summary | `owner-approved-inference` | metadata-only；`real-runtime: NOT RUN` | EVID-SCHEMA-003、EVID-HOST-003、EVID-DESKTOP-001/005 | FEAT-134 |
| GS-003 Command 成功/失败 | `owner-approved-inference` | current terminal scope `real-runtime: PASS`；完整 started/delta live 顺序未捕获 | EVID-HC-002、EVID-F136-001/002/003/004 | FEAT-136；FEAT-143 承接完整状态顺序 |
| GS-004 Tool 成功/失败 | `owner-approved-inference` | generic source conformance `PASS`；real producer/entrypoint `BLOCKED`；Tool D4 `NOT RUN` | EVID-SCHEMA-003/006、EVID-HC-002、EVID-F144-001 | FEAT-144 |
| GS-005 Command 审批允许/拒绝/过期 | `owner-approved-inference` | `BLOCKED`: Owner security decision | EVID-SCHEMA-004、EVID-HC-001、EVID-DESKTOP-006 | FEAT-137 |
| GS-006 文件修改与 Diff | `owner-excluded` | metadata-only exclusion；无 fixture/真实验收 | BASIS-004、EVID-SCHEMA-003/004、EVID-DESKTOP-005 | FEAT-131 scope decision |
| GS-007 active Turn steer | `owner-approved-inference` | metadata-only；Host projection unavailable | EVID-SCHEMA-002、EVID-HC-002、EVID-DESKTOP-003 | FEAT-139 |
| GS-008 Stop active Turn | `owner-approved-inference` | `real-runtime: NOT RUN` | EVID-SCHEMA-002/003、EVID-HC-002、EVID-DESKTOP-006 | FEAT-139 |
| GS-009 Retry/Continue | `owner-approved-inference` | metadata-only；`real-runtime: NOT RUN` | EVID-SCHEMA-002、EVID-DESKTOP-002/006 | FEAT-139 |
| GS-010 历史切换/恢复 | `owner-approved-inference` | `real-runtime: NOT RUN` | EVID-SCHEMA-001、EVID-HC-002、EVID-DESKTOP-002 | FEAT-140 |
| GS-011 上滚/新内容/回到底部 | `owner-approved-inference` | `synthetic: NOT RUN`; Yijie visual smoke `NOT RUN` | EVID-DESKTOP-005/007 | FEAT-141 |
| GS-012 SSE/Host 恢复 | `owner-approved-inference` | safe `synthetic: PASS`; real lifecycle `NOT RUN` | EVID-HC-001/002、EVID-DESKTOP-001/002 | FEAT-142 |
| GS-013 unknown/missing delta/missing final | `owner-approved-inference` | sequence-gap `synthetic: PASS`; other variants metadata-only | EVID-SCHEMA-003/006、EVID-HOST-003/004、EVID-DESKTOP-001/002 | FEAT-142 |

当固定 Runtime 或 Provider 不能自然产生场景时，保持 `NOT RUN` 或 capability gap；不得修改 Runtime、开启 experimental API、硬编码生产事件或把 synthetic 升级为 `real-runtime`。

## 6. 数据与安全规则

- fixture 不得包含真实 prompt、用户正文、绝对路径、账号、头像、邮箱、手机号、secret、token、私钥、PII、商家、店铺或订单数据。
- 不复制 Codex Desktop 源码、品牌资产、私有文案或视觉素材到 Yijie；仓库不保存人工参考媒体。
- 不通过强杀进程、破坏权限、替换 binary、攻击载荷或恶意 fixture 制造失败。进程级验证只使用应用自身正常启动、停止、退出与清理流程。
- 无法安全执行的验证记录 `NOT RUN`、原因和影响；不得生成占位结果或伪造 PASS。

## 7. Policy 与完成规则

1. 本索引固定 reference policy ID 与 final re-freeze Runtime `b2b20e2…` / `0.144.6`；原始 `0ce5902…` 保留历史；它不固定任何 Codex Desktop App version/build。
2. policy 的变更只接受 Owner 明确范围决定；不建立 UI Freeze、drift 或 supersession 流程。
3. 后续 Feature 必须引用稳定的 `CAP-*`、`GS-*` 与 policy ID；实现结果按 `synthetic`/`real-runtime` 如实登记。
4. GS-006 和另外 7 项主动排除不需要证据、不进入 replay、不作为 D4 缺口。
5. D4 依据 current real smoke、stable-only 真实 safe failure/retry、focused checks 与 scoped diff review 通过；缺少 Codex 人工参考媒体不是 gate。Host abnormal-cleanup fault injection 未执行且不在 PASS 声明内。
6. 后续实施必须再次核对 final Runtime HEAD、clean status、schema tree hash 与 compatibility manifest；任何未获新 Owner 授权的差异都违反最终冻结硬性条件。

当前 reference policy、38 个能力 ID、13 个场景 ID 与 8 项主动排除已固定，FEAT-131 D4 已通过；完整 Epic 尚未完成。
