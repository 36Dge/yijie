# FEAT-136 整体实现与调试记录

> 当前状态：D0、Contracts、Host/Desktop 本地实现、source-anchored conformance 与 canonical D4 entrypoint gate repair 已完成并固化为 clean 本地 commits；修复后独立审查无 P0/P1/P2。真实 Command D4 已用尽 3/3 次授权调用并最终 FAIL：成功投影与单 Item hydration 可见，但隔离 Git repo 内两个 exit 128 结果没有形成 failed Command Item/stable error。overall Feature active / in progress。
>
> 第三批范围：先单独修复并审查 canonical runner/stable build/sidecar gate，再执行最多 3 次真实 Provider/模型请求的安全只读 Command D4；Tool D4 继续等待 producer/Owner。

## 1. D0 结论与实施方案

- Feature ID：FEAT-136 已复核可用，正式 schema v3、demo_fast + local 四文件包已建立。
- contract-impact：semantic。原因是 v4 event/item union 闭合；采用显式协商 v5，保留 v1 至 v4。
- Command：CAP-016 / GS-003，是本 Feature Must，当前稳定 Runtime facts 足以建立安全契约。
- Tool：CAP-017 / GS-004 只建立 generic stable projection。真实产品 Tool/producer 保持 capability gap；Runtime MCP Tool 没有 declined status。
- Contract First 顺序：固定 Runtime只读 → Contracts v5 source → generated projections → compatibility → immutable local commit → Host → Desktop → source-anchored conformance。
- 事件原则：event_id 去重而不是内容去重；item.completed 封口 Item；turn.completed 唯一封口 Turn。
- 安全原则：allowlist、redaction before byte counting、bounded summaries/output、显式 truncation、unknown fail-soft/closed、无 raw wire。

## 2. Git 与治理记录

| 时间 | Repository | 动作 | 结果 |
|---|---|---|---|
| 2026-08-29 | yijie | 从 FEAT-135 dependency-complete HEAD 创建 feat/feat-136-desktop-command-tool-items | PASS |
| 2026-08-29 | yijie | 先独立提交 FEAT-138 取消范围的 6 个 FEAT-131 正式文档 | PASS：67f219b6cf825357285215fcbaafb33c3978acb3 |
| 2026-08-29 | yijie | 提交 FEAT-136 D0 与 Contracts slice 记录 | PASS：c7bc206e89692b591eb044af09de21fdb4f1154d |
| 2026-08-29 | yijie-contracts | 从 FEAT-134 candidate 3832a6c5e99b2a6365f193280fdb887c8fdbc2de 创建同名 FEAT-136 分支 | PASS；创建时 clean |
| 2026-08-29 | yijie-contracts | 提交 v5 source/generated candidate | PASS：3c3000a6fbe2f08ab2131a463a1691e867d661b1；提交后 clean，未 push/tag/publish |
| 2026-08-30 | yijie-agent-host | 在完整依赖 HEAD b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe 上提交 reviewed FEAT-136 draft | PASS：83d3163e21579042d2cc21f303e943946ff97eb0；clean，未 push/tag/publish |
| 2026-08-30 | yijie-desktop | 从 fc52ef33cdf040d9b6e8d71bd7498811c5c38c51 创建 feat/feat-136-desktop-command-tool-items 并提交 reviewed core | PASS：69bfacd25b48917cb6102cf1b1b85ca0f9f6bdba |
| 2026-08-30 | yijie-desktop | 单独提交 canonical D4 entrypoint gate repair | PASS：65ee3062833ef3d185511599d8f3a4018f635369；clean，未 push/tag/publish |
| 2026-08-30 | yijie | 提交 Host/Desktop source conformance 与 canonical gate repair 证据 | PASS：82e4010ff34309998c405085c14e3a8988c7113a；本次 D4 evidence delta 基于该 commit |
| 2026-08-29 | yijie-codex | 只读核验 0ce5902ed400866be0196886bb78f693a004d68d | clean；未 fetch/pull/build/modify |

## 3. Contracts 已交付改动

| Authority / projection | 已交付行为 | 边界 |
|---|---|---|
| AgentSessionEventV5 JSON Schema | named v4 families + closed generic allowlist + Command/Tool strict lifecycle/delta/progress | JSON/SSE authority；v1 至 v4 权威源不变 |
| Protobuf v5 | typed transport projection；JSON-equivalent semantic gate | 新 package/tag numbers，不修改旧 proto；可解码不等于有效 |
| Agent Host OpenAPI v5 route | required event_schema_version=5 | 旧 route 保留 |
| AsyncAPI v5 | channel/message/operation | 旧 channel 保留 |
| Runtime compatibility manifest | 仅增加两个已存在 stable notification | Runtime identity、sandbox、approval 不变 |
| v5 fixtures/tests | 11 个无敏感 synthetic conformance fixtures | 不冒充 Host sanitizer/Desktop/real-runtime |
| generated SDK/bundle | 只通过 repository generator 产生 | 禁止手改 sdks |
| version/release/review docs | 0.7.0 local candidate 与 semantic review | 不创建 tag、不发布 |

## 4. Contracts 验证结果

1. `pnpm install --frozen-lockfile`：PASS。
2. Buf、Agent Host OpenAPI Go/TS、AsyncAPI bundle 与 v5 JSON Schema TS 定向生成：PASS；重复生成的 7 项 generated/protected SHA-256 完全一致。
3. `make lint`：PASS；OpenAPI/AsyncAPI、15 个 JSON Schema、Buf、TypeScript no-emit、Go vet 全部通过。
4. 全部非 archive Node tests：63/63 PASS；`go test ./...` PASS；`pnpm exec tsc -p tsconfig.json` PASS。
5. v1 wire equality 对 published f16a497e1377f45747f8ff9292b4b60cf2027f88：PASS（Public 2 paths、Agent Host 7 paths/reference closure）。
6. breaking check 对 FEAT-134 candidate 3832a6c5e99b2a6365f193280fdb887c8fdbc2de：PASS。
7. breaking check 对 published baseline f16a497e1377f45747f8ff9292b4b60cf2027f88：PASS。
8. `git diff --check`、v1-v4 protected-source review、source/generated digest 与两轮独立 semantic review：PASS；最终无 open P0/P1/P2。
9. Contracts 本地不可变 commit 3c3000a6fbe2f08ab2131a463a1691e867d661b1 已形成，工作树 clean。

仓库 composite generate/test/build 路径会创建或读取预存 Zip Slip archive fixture，违反长期安全条款；初始标准门禁审计中识别该事实前曾各调用一次，其机械 exit-0 结果不作为 FEAT-136 证据，之后不再运行。最终只采用上述安全定向替代并如实登记影响。

## 5. Host 本地实现

- 精确 pin Contracts v0.7.0 / `3c3000a6fbe2f08ab2131a463a1691e867d661b1`；checker 逐字节比对 v5 schema 与 11 个普通 fixture，并且对禁止触达的 archive/attack fixture 只比较 immutable Git tree object ID。
- 新增显式 `event_schema_version=5` route；只有 `YIJIE_FEAT136_COMMAND_TOOL_ITEMS_ENABLED=true`、local/demo_fast 且 FEAT-134 gate 已开时协商 v5，v1 至 v4 route/consumer 保持原样。
- Runtime CommandExecution/output delta 映射为安全 Command started/delta/completed；实现 display summary、结构化 cwd、保守 redaction、先脱敏后 UTF-8 caps、complete/head-tail/unavailable、stable error、缺失 started 重建与 completed authority 对账。
- MCP Tool 只映射固定 Runtime 已有 stable lifecycle/progress；identity 无真实批准 registry 时固定 unknown，arguments/result 只给 metadata/count summary，不注册或制造 producer，不猜测 declined。
- event_id/replay、sequence/protocol conflict、late event、active turn ordering 与 compact JSON 1 MiB 限制由 race-enabled focused tests 覆盖。

## 6. Desktop 本地实现

- vendored v5 schema 与 11 个普通 fixture 使用 exact commit/version/schema/fixture digest lock；v5 parser 闭合拒绝未知 variant、非法 null 与越界字段，并在 EOF/decoder error 时发布 protocol resync；v1 至 v4 decoder 不变。
- reducer 只按 event_id 去重，保留不同 event_id 的相同文本；Command/Tool 以 item identity 聚合，completed snapshot 重建并覆盖 started identity/summaries，late delta/progress 不回滚终态。
- SQLCipher v10 使用 additive private migration；保存 source schema authority、Command/Tool 安全字段与 bounded progress，mixed legacy/v4/v5 session 按每个 Turn 的真实 authority hydration，不把旧行改标 v5。
- TypeScript IPC/API/store 使用 closed v5 response decoder；gate 开启时可 hydration 旧 legacy/v4 Turn 与新 v5 Turn，unknown v5 event 进入保守 resync，不 raw fallback。
- 活跃 v4 Turn 通过 v5 私有订阅延续时，仅 inherited v4 semantic event 带 `sourceSchemaVersion=4`；真正 v5 event 不带 marker，generic Command/Tool 仍 fail closed。Command/Tool completed-only 权威快照可在 Native 与 Web reducer 中直接重建 sealed Item。
- `artifact.rs` 的改动只为 inherited v5 Artifact 事件提供 closed-decoder/Unicode 边界兼容；未新增或改变 Artifact producer/产品能力，也未把 Artifact 合并或包装为 Command/Tool。
- 新增 Command/Tool 独立组件并接入 timeline；running 默认展开、terminal 默认折叠，只复制安全 output，status 同时使用图标和文字，提供 `aria-expanded`/`aria-controls`/稳定 `aria-live`，窄宽样式避免主体溢出。
- canonical gate repair 使 `tauri:demo-fast:stable` runner 同时开启 FEAT-134/136 Native/Web gates；stable build 只编译 Web gates，运行期 Native gate 由 launcher 注入。default/raw/release/build 路径显式清 ambient 136。
- sidecar 仅接受 exact `true` + `local/demo_fast` + FEAT-134 依赖；Host-disabled 时 ambient 136 fail closed，`env_clear()` 子进程只白名单转发 Native FEAT-136，不转发 Vite flag。
- 原 FEAT-134 v4 preflight/lock 精确重基线到 Contracts `3c3000a6…` 与 Host `83d3163e…`，仍校验 clean checkout/origin/source digests、未变化的 v4 schema/proto/5-fixture tree、Runtime 0.144.6、experimentalApi=false、read-only/never 与 closed notification set。

## 7. Source-anchored conformance 与审查

- Host 与 Desktop 都从同一 clean Contracts commit 读取同一 schema 和 11 个普通 fixture；Host producer projection/schema tests 与 Desktop consumer decoder/reducer/hydration tests 共同构成 source-anchored conformance。
- 该证据不启动固定 Runtime、Provider、模型或 Tool，不等于真实 Command D4，也不证明真实 Tool producer。
- 独立只读审查推动修复 v5 Unicode char/UTF-8 双界限、mixed v4/v5 history hydration、sticky-v4 live marker 与 completed-only Web reducer；最终 Desktop delta 无剩余 P0/P1/P2。Host 无 P0/P1，保留 Contracts 未冻结 active-item count cap 的后续 resource-hardening P2。

## 8. 外部授权与实际调用

| 类型 | 授权 | 上限 | 当前结果 |
|---|---|---:|---|
| Host/Desktop/yijie 本地 commits | 当前用户明确要求执行 | 本批所需 | Host `83d3163e…` 与 Desktop `69bfacd…`、`65ee306…` 已提交；yijie source evidence 为 `82e4010…`，本次只再形成一个 D4 evidence commit；未 push/tag |
| 既有 yijie / yijie-contracts 本地 commits | 先前批次明确授权 | 既有范围 | 既有 commits 未 amend/改写 |
| push/tag/merge/PR/publish/deploy | 未授权 | 0 | 未执行 |
| Provider/模型 Command D4 请求 | 用户初始授权最多 3 次，并在 Call 1 后明确允许 Call 2/3 | 最多 3 次；不得自动、隐式或超额重试 | 已用 3/3，额度耗尽；仅使用两个闭合的 allowlisted 只读 Command 形式 |
| Tool 请求 / Tool D4 | 未授权且 capability blocked | 0 | BLOCKED / NOT RUN |
| 破坏性、生产写、权限扩大 | 未授权 | 0 | 未执行 |

## 9. 真实、安全、只读 Command D4

- canonical local/demo_fast stable 入口实际开启 FEAT-134/136 gates；一个 success Command 的 v5-only 投影可见。未检查、记录或展示握手/Runtime wire，因此不把它扩大表述为 wire-level negotiation 证据。
- Call 1 使用既有 security bookmark 绑定到一个非 Git 的历史空 smoke 目录；两次 allowlisted 只读尝试均为 exit 128，Desktop 没有生成 Command Item。该轮结论是环境/项目绑定失败，而不是 Command lifecycle PASS。
- 随后定位该 bookmark 的精确目标，并在同一个空目录内初始化无 remote 的隔离 Git repo；只创建一个 benign untracked 文件，没有敏感数据。
- Call 2 只有两次 `exec_command`，参数逐字匹配允许列表，结果依次为 exit 0 与 exit 128，没有第三条或越界命令。成功结果投影为唯一一个 completed Command Item，显示 exit 0、duration 0、安全 cwd 与脱敏输出；失败结果没有对应 failed Item 或 stable error。
- Call 3 只有一次 allowlisted missing-ref `exec_command`，结果 exit 128，无额外命令；仍没有 Command Item，只出现过程/未分类消息。
- Call 2/3 是用户在 Call 1 绑定失败后明确允许的追加请求：Call 2 重复两个允许形式验证修复后的项目绑定，Call 3 重复失败形式隔离投影缺口。没有自动、隐式或超出 3/3 授权的重试。由于 Git 仓内的两个正常、非破坏性失败结果均缺失 Command lifecycle/stable error，Command D4 最终为 FAIL。
- started/output delta 因命令执行过快未直接观察；真实 event_id 幂等、completed authoritative reconciliation 与 late event 不回滚未独立观察；正常 replay 为 NOT OBSERVED，未通过断连、注入或伪造制造。
- App 正常 Cmd+Q 后 runner exit 0；canonical 重开后 SQLCipher hydration 恰好恢复一个 success Command Item，未重复。最终再次正常 Cmd+Q，runner exit 0。
- 最终 App/Host 已停止且 loopback 端口 idle。Host bbolt metadata-only 检查为 format 2、store schema 4、7 个预期 bucket、unknown/malformed 0；14/14 session safe projection 可解析，唯一 latest session 为 idle/completed 且 active turn 为空。该证据只证明 durable session 已终态 reconciliation/无 active turn；DB 不含 v5/event journal/Command exit/duration，store schema 4 不能解释为 wire v4/v5。
- success Item 的折叠、键盘、状态文字、AX live announcement 和安全复制 live 可见 PASS；状态图标只有 component 证据，未单独做 live 判定。当前 light 主题 live PASS；通过键盘缩放到 AX 明确的 200%，布局仍可键盘/AX 访问，随后正常恢复 100%。窗口配置静态覆盖 width 1180、height 780、minWidth 1180、minHeight 760，但本轮未精确调整到 1180×760，因此该精确尺寸 live NOT RUN；dark 跟随 macOS 系统外观，本轮未更改系统设置，live NOT RUN。
- Command Item 自身只显示闭合状态和脱敏投影，未暴露 producer raw command、绝对路径、secret、bookmark 或 Runtime wire；但用户消息为指定 allowlist 而显示了用户亲自输入的命令文本，所以整个 WebView 的字面 no-raw 标准不满足。四文件与保留截图/证据不记录命令字面量、绝对路径、secret、bookmark、prompt 或 Runtime wire。

## 10. 已知限制与停止状态

- Contracts 可以定义 generic Tool surface，但当前固定 Runtime 没有 MCP declined status，也没有已批准的真实产品 Tool producer；真实 GS-004 继续 blocked/not run。
- Synthetic fixtures 与 source-anchored conformance 只能证明 Host/Desktop 对同一 authority 的确定性实现；本次真实 D4 只补充一个 success Command、两个未投影失败结果、单 Item hydration 与局部 live UI 证据。
- Host active turn 的 v5 Item 集合沿用进程内生命周期，但 Contracts 没有冻结 item-count cap；这是后续 Owner/Contracts resource-hardening 项，不在本批制造额外 wire 约束。
- Desktop 私有 512 Item 上限继承既有 bounded history resource policy，不宣称为 v5 wire limit。
- 真实、安全、只读 Command D4 已执行 3/3 次且 FAIL；额度耗尽，不再发起请求。缺口是 failed Command lifecycle、stable error、整个 WebView 的字面 no-raw 标准，以及未独立观察的 event_id/reconciliation/late-event/replay 证据。
- Tool D4 保持 blocked/not run，直到出现真实 stable producer 和 Owner 决策；不得用 synthetic Tool 或 dynamic tool 冒充。
