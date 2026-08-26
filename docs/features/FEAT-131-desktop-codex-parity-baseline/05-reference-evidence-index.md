# FEAT-131 — Codex Desktop 参考证据索引

> Freeze ID：`codex-desktop-26.818.61809-build-7019-2026-08-26`
>
> Runtime baseline：`yijie-codex 0.144.6` / `experimentalApi=false`
>
> 当前结论：D0 候选行为 ID 已固定，当前隔离 canonical stable startup 已以 `experimental_api=false` 通过；版本专属 Codex UI 观察仍待人工补采。当前 canonical real smoke 因授权额度已用而 NOT RUN；predecessor submission 未到 Runtime，因此基线尚未冻结，Epic 尚未完成。

## 1. 证据状态与 provenance

| Value | 含义 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| `local-metadata-observation` | 对本机已安装 App 或仓库执行只读元数据核对 | version、build、hash、commit 等身份 | 版本专属 UI 行为 |
| `reference-observation` | 与冻结 version/build 匹配、已脱敏且可复核的截图、录屏或操作记录 | Codex Desktop 的可观察交互 | Runtime/Host 是否提供同一语义 |
| `reference-unobserved` | 没有取得满足上述条件的参考证据 | 明确当前证据缺口 | 不可用记忆、通用文档或 fixture 补成已观察事实 |
| `real-runtime` | 通过正常 Yijie 入口由固定 Runtime 真实产生 | 当前 Runtime/Host/Desktop 路径的真实结果 | Codex Desktop 版本专属表现 |
| `synthetic` | 无敏感数据的 test-only 确定性事件回放 | parser、reducer、UI 状态机的可重复行为 | 真实 Runtime producer、Host supported projection 或参考 App 行为 |
| `implementation extension observed` | 代码中存在、但未进入锁定 compatibility manifest 的路径 | 实现事实 | 受支持投影承诺 |
| `NOT RUN` | 尚未执行或尚未登记结果 | 当前执行状态 | 任何 PASS 结论 |
| `BLOCKED` | 依赖 Owner 决策、未投影能力或冻结 Runtime 禁止的能力 | 明确停止条件 | 不得用模拟生产事件绕过 |

所有版本专属 Codex Desktop 交互当前统一为 `reference-unobserved`。本索引没有登记任何版本专属截图或录屏，也没有把 Runtime schema、Yijie 当前 UI、synthetic fixture 或模型记忆写成 `reference-observation`。

## 2. 冻结参考 App 身份

| Evidence ID | Fact / artifact | Authority | Status | Notes |
|---|---|---|---|---|
| EVID-REF-001 | Freeze ID、冻结时间与证据类型 | `references/codex-desktop-build-metadata.md:1-5` | `local-metadata-observation` | 只读身份元数据，不是 UI 观察 |
| EVID-REF-002 | App bundle、short version `26.818.61809`、build `7019`、Info.plist SHA-256 与本机 mtime | `references/codex-desktop-build-metadata.md:7-18` | `local-metadata-observation` | mtime 不是 OpenAI 发布日期；系统主题不证明 App 内主题 |
| EVID-REF-003 | App 内主题、窗口尺寸、交互配置、截图/录屏 | `references/codex-desktop-build-metadata.md:20-27` | `reference-unobserved` | 当前安全自动化不能读取目标窗口；不绕过该边界 |
| EVID-REF-004 | Freeze/drift 规则 | `references/codex-desktop-build-metadata.md:29-34` | frozen | 本机版本漂移只登记 drift，不覆盖本 baseline |
| EVID-REF-005 | 人工采集全局材料、GS-001～013 每个 variant、YAML 记录、文件名/hash、脱敏与安全边界 | `references/manual-capture-checklist.md` | `NOT RUN` | 采集前必须再次核对 version/build；无法安全执行时登记 `NOT RUN` |
| EVID-REF-006 | 当前未生成 Codex Desktop 截图/录屏，未使用旁路采集 | `references/manual-capture-checklist.md` | `reference-unobserved` | 无空白占位图，无 Yijie/synthetic 冒充 |

`feature.yaml:40-58` 与 `00-feature-brief.md:5-29` 定义产品目标和冻结范围；它们是治理事实，不替代 EVID-REF-001～006 的观察证据。

## 3. Runtime、Contracts 与 Host 权威证据

### 3.1 固定 Runtime 身份

| Evidence ID | Fact | Authority | Status |
|---|---|---|---|
| EVID-RT-001 | fork commit、upstream tag/commit、Runtime `0.144.6`、stdio、`experimental_api=false`、267 个 schema 与 schema tree SHA-256 | `yijie-contracts/compatibility/agent-host-runtime-v1.json:4-13` | frozen |
| EVID-RT-002 | upstream tag/commit、Runtime version、toolchain、target、`experimentalApi=false` 与 stdio | `yijie-codex/.yijie/schemas/app-server/baseline.json:3-9` | frozen / read-only |
| EVID-RT-003 | 实施前 Runtime HEAD、clean worktree、schema hash 与“不 fetch/pull/rebase/build/upgrade”边界 | `references/runtime-freeze-evidence.md:7-21` | captured-before |
| EVID-RT-004 | 实施后 Runtime/manifest 精确对账 | `references/runtime-freeze-evidence.md:33-49` | `PASS` |

### 3.2 固定 Runtime stable surface

| Evidence ID | Capability group | Authority | Interpretation |
|---|---|---|---|
| EVID-SCHEMA-001 | `thread/start`、`thread/resume`、`thread/fork`、`thread/archive`、`thread/list`、`thread/read` | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ClientRequest.json:4870`、`:4894`、`:4918`、`:4942`、`:5254`、`:5302` | stable client methods present in frozen schema |
| EVID-SCHEMA-002 | `turn/start`、`turn/steer`、`turn/interrupt`、`review/start` | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ClientRequest.json:6023`、`:6047`、`:6071`、`:6095` | stable client methods present in frozen schema |
| EVID-SCHEMA-003 | thread status、turn diff/plan、assistant/command/file/MCP/reasoning delta notifications | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ServerNotification.json:5787`、`:6087`、`:6107`、`:6207`、`:6311`、`:6352`、`:6412`、`:6612`、`:6652` | schema presence does not imply current Host projection |
| EVID-SCHEMA-004 | Command/FileChange approval、MCP elicitation、permission approval、dynamic tool server requests | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ServerRequest.json:1796-1846`、`:1873-1946` | approval/security policy remains an Owner decision |
| EVID-SCHEMA-005 | `item/tool/requestUserInput` 带 EXPERIMENTAL 协议注释，但仍存在于 non-experimental generated schema，且 variant 没有 runtime gate attribute | `yijie-codex/codex-rs/app-server-protocol/src/protocol/common.rs:1474-1478`；generated `ServerRequest.json:1848-1871` | 不能归因为 `experimentalApi=false` 阻断；保持 `requires Host/Contracts projection` 与 Owner 决策 |
| EVID-SCHEMA-006 | ThreadItem variants include user/agent message, plan, reasoning, command, file, MCP/dynamic/collab/subagent tools, web/image/sleep/review/compaction | `yijie-codex/.yijie/schemas/app-server/generated-json-schema/ServerNotification.json:3974-4679` | item availability and experimental markers must still be evaluated per item |

### 3.3 当前 supported Host projection 与实现扩展

| Evidence ID | Fact | Authority | Status |
|---|---|---|---|
| EVID-HC-001 | local HTTP/SSE、owner-only bearer、read-only、approval `never` | `yijie-contracts/compatibility/agent-host-runtime-v1.json:15-19` | supported projection |
| EVID-HC-002 | 锁定的 7 个 Runtime methods 与 9 个 notifications | `yijie-contracts/compatibility/agent-host-runtime-v1.json:20-39` | supported projection |
| EVID-HOST-001 | Session methods 与固定 `never` / `read-only` | `yijie-agent-host/internal/codex/session_protocol.go:19-44` | implementation agrees with the baseline for listed session methods |
| EVID-HOST-002 | `thread/delete` 与 dynamic `generate_image` 常量/路径 | `yijie-agent-host/internal/codex/session_protocol.go:19-28`、`:171-215` | `implementation extension observed`; not promoted to locked projection |
| EVID-HOST-003 | generic Item mapper保留 item type，但只对 agent text/reasoning 做有限内容处理 | `yijie-agent-host/internal/session/service.go:543-630` | command/tool/file/phase 等详细语义未投影 |
| EVID-HOST-004 | completed/error/warning 到 Host event 的终态与安全消息映射 | `yijie-agent-host/internal/session/service.go:631-706` | 当前基础 Turn/error projection |

由此得到的能力分类以 `03-capability-matrix.md` 为唯一 FEAT-131 映射表。任何只存在于 schema、但没有进入 EVID-HC-002 的事实，不能写成当前 Host supported projection；任何实现扩展也不能反向修改 frozen manifest 的含义。

## 4. 当前 Desktop 证据

| Evidence ID | Fact | Authority | Current support |
|---|---|---|---|
| EVID-DESKTOP-001 | Live wire 仅有 assistant/reasoning append、turn state/terminal、cleanup、resync、context invalidation | `yijie-desktop/src/domain/chat-ipc.ts:446-488` | 基础 stream/reasoning/terminal/resync；无 command/tool/diff/approval item |
| EVID-DESKTOP-002 | Store 校验 context/subscription/session、sequence/event ID，并聚合 assistant/reasoning；terminal 后 resync | `yijie-desktop/src/stores/chat.store.ts:808-872` | 可做确定性 replay；未知/缺口会触发保守 resync |
| EVID-DESKTOP-003 | streaming 时发送和附件禁用 | `yijie-desktop/src/components/chat/ChatComposer.vue:73-83` | 当前无 active-turn steer composer |
| EVID-DESKTOP-004 | Enter 发送、Shift+Enter 换行、IME composing 时不提交 | `yijie-desktop/src/components/chat/ChatComposer.vue:141-149` | 基础键盘交互存在 |
| EVID-DESKTOP-005 | reasoning disclosure、assistant stream、Artifact list、停止/失败终态 | `yijie-desktop/src/pages/chat/ChatPage.vue:499-552` | 基础可见内容；Artifact 不能代替 Runtime Diff |
| EVID-DESKTOP-006 | Composer interrupt wiring 与只读权限说明弹窗 | `yijie-desktop/src/pages/chat/ChatPage.vue:577-633` | Stop 与策略说明存在；没有 Runtime action approval |
| EVID-DESKTOP-007 | 自动跟随、回到底部、reduced motion、分页位置保持 | `yijie-desktop/src/composables/useChatScroll.ts:11-70` | 基础长对话滚动存在；完整 parity 未观察/未验收 |
| EVID-DESKTOP-008 | `tauri:demo-fast:stable` closed launcher、隔离 bundle/app-data/Host home、stable-only instance branch、MiniMax 文本 Provider 与 image dynamic tool 分离、Desktop supervisor cleanup policy | `yijie-desktop/package.json`、`scripts/run-local-demo-fast.sh`、`src-tauri/tauri.feat131-stable.conf.json`、`src-tauri/src/lib.rs`、`src-tauri/src/chat/sidecar.rs` | Desktop-local canonical 验证入口；不是公共 wire/Runtime 能力；不证明 Host 内部 fallback |
| EVID-REAL-001 | 当前 `com.yijie.ai.feat131-stable` debug App 的 `/readyz` 与 `/v1/status` | `02-verification.md` §2 | current startup `PASS`：Runtime `0.144.6`、MiniMax-M3、`experimental_api=false`；两次正常 Cmd-Q 后端口/owned processes 清空 |
| EVID-REAL-002 | predecessor 单次 UI submission 与脱敏 Runtime 事件聚合 | `02-verification.md` §2 | predecessor `pre-runtime: FAIL`：Desktop 本地消息出现，但 Runtime thread/turn/delta/terminal 均未观察到；Provider 调用/计费未确认。当前 canonical real smoke `NOT RUN` |

EVID-DESKTOP 代码证据只能证明 Yijie 当前实现；EVID-REAL 只证明这一次 Yijie local 验证结果。它们都不是 Codex Desktop 的参考证据，也不表示 `03-capability-matrix.md` 中 Desktop-only 后续工作已经完成。

## 5. 黄金场景证据账本

`04-golden-scenarios.md` 是场景定义 authority。以下每行都是唯一 evidence slot；未来补证据时保留 Scenario ID，只填写实际 artifact、SHA-256、采集环境与 provenance，不覆盖旧 baseline。

`scenario-catalog.json.variants` 表示场景要求全集；只有同时出现在 catalog `replayedVariants` 与对应 fixture `coveredVariants` 的 variant 才可写 `synthetic: PASS`。当前 GS-013 仅 `missing-delta` 已回放，`unknown-item` 与 `missing-final` 仍为 metadata-only。

| Scenario | Reference artifact / SHA-256 | Codex reference status | Yijie evidence status | Primary evidence anchors | Owner |
|---|---|---|---|---|---|
| GS-001 普通流式完成 | none | `reference-unobserved` | streaming/completed `synthetic: PASS`; current canonical `real-runtime: NOT RUN`; predecessor `pre-runtime: FAIL` | EVID-SCHEMA-002/003、EVID-HC-002、EVID-DESKTOP-001/002、EVID-REAL-001/002 | FEAT-134、FEAT-135 |
| GS-002 过程更新/推理信息 | none | `reference-unobserved` | metadata only；`real-runtime: NOT RUN` | EVID-SCHEMA-003、EVID-HOST-003、EVID-DESKTOP-001/005 | FEAT-134 |
| GS-003 Command 成功/失败 | none | `reference-unobserved` | metadata only；real projection unavailable | EVID-SCHEMA-003、EVID-HOST-003/004、EVID-DESKTOP-001 | FEAT-136 |
| GS-004 Tool 成功/失败 | none | `reference-unobserved` | metadata only；real projection unavailable | EVID-SCHEMA-003/006、EVID-HC-002、EVID-HOST-002/003 | FEAT-136 |
| GS-005 命令审批允许/拒绝/过期 | none | `reference-unobserved` | `BLOCKED`: Owner security decision | EVID-SCHEMA-004、EVID-HC-001、EVID-DESKTOP-006 | FEAT-137 |
| GS-006 文件修改与 Diff | none | `reference-unobserved` | `BLOCKED`: Owner security decision | EVID-SCHEMA-003/004、EVID-HC-001、EVID-DESKTOP-005 | FEAT-138 |
| GS-007 active Turn steer | none | `reference-unobserved` | metadata only；Host projection unavailable | EVID-SCHEMA-002、EVID-HC-002、EVID-DESKTOP-003 | FEAT-139 |
| GS-008 Stop active Turn | none | `reference-unobserved` | `real-runtime: NOT RUN` | EVID-SCHEMA-002/003、EVID-HC-002、EVID-DESKTOP-006 | FEAT-139 |
| GS-009 Retry/Continue | none | `reference-unobserved` | metadata only；`real-runtime: NOT RUN` | EVID-SCHEMA-002、EVID-DESKTOP-002/006 | FEAT-139 |
| GS-010 历史切换/恢复 | none | `reference-unobserved` | `real-runtime: NOT RUN` | EVID-SCHEMA-001、EVID-HC-002、EVID-DESKTOP-002 | FEAT-140 |
| GS-011 上滚/新内容/回到底部 | none | `reference-unobserved` | `synthetic: NOT RUN`; visual smoke `NOT RUN` | EVID-DESKTOP-005/007 | FEAT-141 |
| GS-012 SSE/Host 恢复 | none | `reference-unobserved` | safe `synthetic: PASS`; real lifecycle `NOT RUN` | EVID-HC-001/002、EVID-DESKTOP-001/002 | FEAT-142 |
| GS-013 unknown/missing delta/missing final | none | `reference-unobserved` | safe sequence-gap `synthetic: PASS`; unknown-item/missing-final metadata only | EVID-SCHEMA-003/006、EVID-HOST-003/004、EVID-DESKTOP-001/002 | FEAT-142 |

当真实固定 Runtime 或 Provider 不能自然产生某场景时，该场景保持 `NOT RUN` 或 capability gap；不得改 Runtime、开启 experimental API、硬编码生产事件或把 synthetic 结果升级为 `real-runtime`。

## 6. 证据处理与安全规则

- 证据和 fixture 不得包含真实 prompt、用户正文、绝对路径、账号、头像、邮箱、手机号、secret、token、私钥、PII、商家、店铺或订单数据。
- 参考截图/录屏只作 `internal` 证据；采集前关闭无关窗口/通知，完成后裁剪或模糊身份信息，并登记文件名、SHA-256、version/build、主题、窗口尺寸、缩放和采集时间。
- 不复制 Codex Desktop 源码、品牌资产、私有文案或视觉素材到 Yijie 生产 bundle；参考媒体也不得进入生产 bundle。
- 不通过强杀进程、破坏权限、替换 binary、攻击载荷或恶意 fixture 制造失败。进程级验证只使用应用自身正常启动、停止、退出与清理流程。
- 无法安全执行的证据项记录 `NOT RUN`、原因、影响和 Owner；不得生成占位证据或伪造 PASS。

## 7. Freeze、drift 与完成规则

1. 本索引固定 `26.818.61809` build `7019` 与 Runtime `0.144.6`；App 或仓库后续漂移不会静默改写本 baseline。
2. 只有 Owner 明确批准新 baseline，才新建 Freeze ID、证据索引和 drift 记录；旧证据保留。
3. 后续 Feature 必须引用稳定的 `CAP-*` 与 `GS-*` ID；取得新证据只补 provenance/status/artifact，不把 synthetic 或实现推断变成参考观察。
4. 当前隔离 canonical startup 已 PASS；`02-verification.md` 中 D4 在 current real smoke、版本专属参考证据、representative real failure/recovery 与独立 diff review 完成前保持未通过。自动化 Must AC 与 synthetic replay 可分别记录实际 PASS，但不据此宣称 D4 PASS。
5. 实施后必须再次核对 Runtime HEAD、clean status、schema tree hash 与 compatibility manifest；任何差异都违反 frozen Runtime 硬性条件。

D0 候选行为 ID 已固定；证据采集、Owner 审核与 D4 尚未完成，因此基线尚未冻结，Epic 尚未完成。
