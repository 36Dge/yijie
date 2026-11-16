# 连接器 P1 修复与定向验证

2026-11-14。Owner 已授权实施，禁止真实供应商、付费模型、提交和推送。
`contract-impact=semantic`；结果元数据／可选关联字段为 additive，原生代理审批配置为 semantic。
仅本地工作树候选，release=false；不修改 yijie-codex 源码、补丁或已有 Runtime 制品，
不新增审批数据库，不重启日常客户端。

## 修改

- Contracts 先更新 Broker 0.8.0、Host v1 0.5.0／v2 0.7.0，生成共享 GatewayCallReceipt。
  字段从已有 CallRecord／decide_call 捕获；不带 credentialRef、capabilityRef、token、原始参数或权限上下文。
- Host 只为已 prepare 的 owned yijie_market 选择原生 approve；ask/on-request、user reviewer、
  Gateway 原生 elicitation、owner 决定和 HTTP 一次许可保持。显式逐工具规则不被覆盖。
- worker 在同一锁内完成准入判定与决定回执捕获，再在清洗后的 MCP 结果中附加
  `_meta["yijie.market.call"]`。已拒绝／取消／到期的登记调用返回自己的非执行回执。
  admissionConsumed 不等于 HTTP 已发送或外部业务成功。
- Host 读取实际原生 Item 元数据并核对已有 operation ledger；Native 对照原轮次的
  snapshot、digest、服务和安装引用。冲突／未知片段被省略，原生结果仍可读。
  Desktop 展示关联到该结果的决定，历史回执没有批准按钮。
- v2 同步增加显式 `--local-market-candidate`，只覆盖 market Host 与依赖它的 experts 派生物。
  工作树摘要和 worktree_head 不冒充 source_commit；默认不可变来源验证未放宽。
- compatibility checker 增加显式 --schema 定向范围，比较算法和默认全仓行为保持。
  不为可选关联字段收紧旧 ToolObservation 的条件必填性；关系校验由 Host／Native 承担。

## 逐仓修改点

| 仓库 | 手写实现与测试入口 | 派生物 |
| --- | --- | --- |
| yijie-contracts | `compatibility/market-broker-control/`、`compatibility/market-host/`、`compatibility/market-host-v2/` 源契约；对应 source/generate 脚本；`scripts/sync-model-call-surfaces-v2.mjs`；`scripts/check-jsonschema-breaking.mjs`；`tests/market-call-receipt.test.mjs`；`docs/market-call-receipt.md` | 同源 Go／Rust／TypeScript／JSON Schema；market-provider、experts v1/v2 的依赖摘要刷新 |
| yijie-agent-host | `internal/codex/market_turns.go`；新增 `market_proxy_policy_test.go`、`market_proxy_native_integration_test.go`；扩充 `tool_search_gateway_integration_test.go`；`internal/session/market_observe.go`、新增 `market_correlation.go`／测试及既有测试 stub | `api/` 候选来源／schema；`internal/contracts/marketbrokercontrol/` 与 `markethost/` |
| yijie-connectors | `worker/src/broker.rs` 的只读回执捕获和双批准测试；`worker/src/gateway.rs` 的结果包装、边界与预算测试 | Broker Rust 类型；`api/` Broker 与 Provider 候选来源 |
| yijie-desktop | `src-tauri/src/chat/connectors/observe.rs`；`src/api/market-host-native-client.ts`／测试；`src/components/chat/MarketChatActivity.vue`／测试；`src/test/market-chat-fixture.ts` | `contracts/`，Native Broker／Host 类型，前端 Host／依赖 experts 类型与 validator |
| yijie | ADR-0021 的本地修复细化与本记录 | 无 |
| yijie-codex | 无修改；复用固定 Runtime 的配置、server elicitation、MCP result `_meta` 和原生历史 | 未生成或替换 Runtime 制品；仅使用已有标准 Cargo 缓存构建连接器 worker |

## 基线与工作区保护

实施前 HEAD：Contracts `2592f5d5b07fcd92de10d25c4dcf73bd1ce03cb5`；
Host `8b6d7afa4122265951b3eeeacc81495b7684f87f`；Connectors
`37552bec1c31bca95457af7145e0dad206df1f8a`；Desktop
`eefb2ac92d8bff80aad00639794e40e1c1e190f6`；Runtime
`5c64ed3f03808639faf7c11674e87636a94ab221`。
先备份并逐文件记录原有 dirty/untracked 内容 SHA-256，交付前复核全部 43 个文件保持不变。
本次未改原有开发入口、provenance 刷新、worker source 检查等未提交工作。
所有仓库 HEAD 保持上述基线；Runtime 工作树干净；各仓 `git diff --check` 通过。

## 验证范围与结果

- Contracts：20 项定向 Node 测试通过；Broker／Host Go SDK 测试通过，v2 SDK 编译通过。
  与实施前完整 HEAD 比较的三个受影响 wire schema 结构检查通过；新旧读写方向样本通过。
  Broker 与 Host v2 两个消费者的显式本地生成／同步检查通过。
- Host：审批、关联投影、旧结果读取、正常 bbolt 重开、重复关联处理等定向测试及 race 检查通过；go vet 通过。
- worker：通用多服务同参数新审批、结果包装／拒绝／预算检查通过；scoped Clippy 通过。
  定向资格测试确认只有 native Accept 而没有 owner 决定不能消费许可，native Decline
  会取消既有批准并释放参数，已消费的一次许可不能重复执行。
  产品 worker 经原 canonical 脚本构建到独立临时内容寻址目录，未替换日常 worker。
- Desktop：19 项组件／client／composable 定向测试通过；受影响前端 lint 和 vue-tsc 通过；
  当前 feature 的原生选集关联测试通过。旧历史与当前权限不混用。
- 固定真实 Runtime：使用保留的 tool-search-v1 制品与普通 loopback 协议 peers，
  验证三次相同调用需要三次新 elicitation，拒绝业务计数为 0，两次允许各执行 1 次；
  显式逐工具 prompt 优先级保持；原生 `_meta` 经过正常 EOF 重启后仍可读取，没有重放业务。
  此测试使用协议宿主回调，不冒充整套产品批准成功路径。
- 真实产品 Host + 新 canonical worker + 固定 Runtime：通过现有 Kimi 本地准备（无 HTTP）、
  原生搜索／exec、真实 Host approval_decide 的拒绝路径，验证返回的 native MCP Item 中
  callRef、approvalId、decisionId 与原决定完全一致且 admissionConsumed=false。供应商请求为 0。

真实供应商、付费模型、日常客户端 GUI 全链路、公开／生产验收均未执行。
不把本机协议或分层证据描述为真实商家账号验收。

## 可复核命令与制品

以下均为定向范围，不代表全量测试：

- Contracts：`node --test tests/market-call-receipt.test.mjs tests/market-broker.test.mjs tests/market-host.test.mjs`；
  `GOTOOLCHAIN=go1.26.5 GOPROXY=off go test ./sdks/go/market-broker-control ./sdks/go/market-host ./sdks/go/market-host-v2`。
- 结构比较：`node scripts/check-jsonschema-breaking.mjs 2592f5d5b07fcd92de10d25c4dcf73bd1ce03cb5 --schema=compatibility/market-broker-control/wire.schema.json --schema=compatibility/market-host/wire.schema.json --schema=compatibility/market-host-v2/wire.schema.json`。
- 同步检查：Broker 对 connectors／agent-host 执行 `--check`；v2 对 desktop／agent-host 执行
  `--local-market-candidate --check`。未知 schema 范围被拒绝；默认 immutable 检查也仍拒绝当前未提交候选。
- Host：`go test -race ./internal/codex ./internal/session` 配合新审批配置、`TestMarketResult*`、
  既有审批 authority／双期限／原生结果投影用例筛选；`go vet ./internal/codex ./internal/session`。
  固定 Runtime 集成用例为 `TestMarketProxyNativeElicitationAndResultMetadata` 与
  `TestToolSearchRuntimeGatewayApprovalReject`，均使用 loopback 模型响应，不访问模型服务。
- worker：离线锁定依赖，仅运行 `sorftime_market_call_binds_exact_ref_and_requires_a_fresh_decision`、
  `result_receipt`、`actual_registered_call_requires_both_decisions_and_is_consumed_once`、
  `native_decline_cancels_owner_approval_and_releases_arguments`；后两项使用已有 `broker-qualification` feature。
  `cargo clippy --offline --locked --manifest-path worker/Cargo.toml --bin yijie-mcp-worker --no-deps -- -D warnings`。
- Desktop：Vitest 仅 `MarketChatActivity.test.ts`、`market-host-native-client.test.ts`、`useMarketChat.test.ts`；
  受影响文件 ESLint、`vue-tsc --noEmit`；Native 仅
  `chat::connectors::observe::tests::native_market_result_correlation_uses_original_selection_without_live_authority`。

真实 Runtime 为保留的 `tool-search-v1`／Codex 0.144.6 制品，SHA-256
`7d49018c29704fa9863da72a34d780b8ad0e67c9ffe1821ebd1c1b94d9a46d49`。
worker 经 `scripts/build-market-worker.sh --output-root <新临时目录>` 正常构建，最终 SHA-256
`03227da28cac244892e18639df0d50f27931bd9737873f922ccf5dd78049ee6f`，与产品拒绝链路验证的制品一致。
构建脚本按既有规则拒绝复用已有 manifest 的目录；最终使用新的 `worker-final` 目录，旧制品保留。
进程集成只使用正常 EOF／Shutdown，不强杀或改写可执行程序，不采用攻击或权限破坏 fixture。

## 已有兼容检查限制

默认全仓 JSON Schema checker 将未变化的对象／数组 default 按引用比较，
对未改动 runtime-skill-marketplace/config.schema.json 报告相同值变更。
保留该失败，不修改无关比较规则；本次定向检查明确只比较三个受影响 schema。
相对历史 `61137174a25dc368e0006f27633fd4a9ad097aa6` 的定向检查另报告
8 项早于本轮的 web 双期限／opt-in 条件必填差异；本轮对应定义与实施前 HEAD 相同。
因此不宣称全支持窗口或全仓兼容已通过；本地未提交候选也不通过默认 immutable 发布验证。

## 剩余边界与回滚

无 MCP 回包时仍没有可关联结果，不补造 Item；审批进行中关联 native Item ID 仍是上游缺口。
本次不处理独立持久审计和整线程轮询重构，也不改结构化结果展示策略。
回滚先通过正常退出／EOF 撤销当前租约，再选择保留的旧 Host／worker。恢复 auto 会恢复
通用工具的已知前置审批阻断；必要时使用既有 market 关闭开关。保留新 reader 和已写入的
历史回执，不降库、不删除凭据、不恢复旧许可、不重发结果未知的外部请求。

2026-11-15 复审修复：本地来源候选已接通固定开发入口，并纳入共享同步脚本涉及的
selection v2 来源；结果标题改用所属轮次快照。完整只读构建校验通过，未重启服务。
逐仓变更、验证与回滚见 `2026-11-15-p1-review-fixes.md`；前文为 11 月 14 日实施时的记录。
