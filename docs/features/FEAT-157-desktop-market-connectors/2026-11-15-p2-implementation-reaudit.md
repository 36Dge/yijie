# 三个 P2 落地复审与修复

2026-11-15。Owner 授权复审并直接修复。保持逐次批准，保护既有修改，不重启服务、
调用真实供应商／付费模型、提交或推送。

相对上一轮 P2 候选，`contract-impact=semantic`：修复展示读取与事实窗口的语义，
不增加 HTTP/IPC 形状、执行权限或存储版本；仍为 SQL 47，旧迁移不改。
Host v1／v2 候选修订为 0.6.1／0.8.1，先更新权威契约，再实现并用 canonical generator
生成、同步。此前 P2 整体因 SQL 47 对旧 reader 的影响仍按 breaking 分类，本次不降级
它的存储兼容风险。来源仍为 release=false 的本地候选，没有伪造发布 commit。

## 复审结论与已修复问题

三个 P2 的主要接线存在，但上一轮测试未覆盖实际 HTTP 查询参数路径与若干正常时序
边界，不能据此声称完整落地。以下五处问题均已修复；其中路由阻断按实际影响列为 P1。

| 优先级／对应原项 | 实际缺口与影响 | 本次最小修复及源码 |
| --- | --- | --- |
| P1／P2-5 观测复用 | Native 实际发出 `?source=events/history`，Host 工具路由先调用 `marketReadID`，其内部 `validRecoveryRequest` 拒绝全部查询参数。尚未到达新增分支就返回 400；历史和事件读取均失败 | Host `internal/app/market_http.go` 新增局部 `marketToolReadID`，只允许工具 GET 的单个 source=history/events，再复用原无 body／canonical ID／请求头校验。其它读路由保持无查询参数；旧客户端缺省 source 的截断提示保留 |
| P2／P2-3 决定证据 | 只读最近 128 行会排除同轮仍 pending 调用的既有决定，界面重开可能再次提供点击；墙钟回拨也会让旧事实排在新事实之前 | Desktop `connectors/decision_facts.rs` 使用追加行序；窗口截断时，`observe.rs` 先核验 Host 活跃审批，再按准确 approvalId＋callRef、当前选定原轮次补入每个调用的确认或最新证据，再填近期历史，最多 128 条。`MarketChatActivity.vue` 保留追加顺序与 acknowledged 的更强证据，不用时间推断阶段 |
| P2／P2-5 观测复用 | 首次 Runtime 历史读取期间迟到的 turn/started 建立空 complete 缓存；历史 seed 被版本检查拒绝后，事件读取误选空快照。迟到的 item/started 同样可能遮住已读终态 | Host `market_tool_snapshots.go` 只有在缓存覆盖刚读到的全部 native Item 且不将终态退回 in_progress 时才优先返回；否则保留真实历史响应并失效不完整缓存，下次正常读取建立基线 |
| P2／P2-5 观测复用 | 刷新循环已结束、Promise finally 尚未运行时到达的通知只进入 queuedRead；空闲停轮询后可能长期不再读取 | Desktop `useMarketChat.ts` 清理当前请求时立即处理余下队列；继续使用原 context/session/epoch 与卸载隔离 |
| P2／P2-4 结果展示 | JSON 去重仅比较 compact 字节，同一对象的键顺序不同会被显示两次、浪费预算，甚至产生不必要的截断提示 | Host `market_result.go` 用标准 JSON decoder＋UseNumber 解码后比较；忽略对象键顺序和空白，保留数组顺序、大整数精度与数字字面差别。没有改变参数摘要或审批身份计算 |

## 原生能力与执行边界复核

- 执行仍由 yijie-codex 的推理循环、ToolRouter、MCP client 和原生 elicitation 驱动。
  展示仍接现有 `item/started`、`item/completed`、turn 通知与原生 `thread/read`，
  没有新增 Runtime 补丁、第二个订阅或完整执行状态机。
- `_meta["yijie.market.call"]` 仍是有回包时的可信关联来源。Host 核对原 operation／
  选集，Native 核对原 thread／turn／selection。缓存只是展示投影；未出现 Item 时
  不编造 ID，不凭工具名称、结果文字或时间补关联。
- 决定事实仍追加在原 SQLCipher 库，迁移 47 字节不变。查询既不派发决定也不恢复权限；
  优先证据只用于当前选定原轮次的活跃读取，显式历史查询不会混入其它轮次。查询失败
  不暴露可操作审批，仍由 remoteIssue 或既有错误路径禁用操作。
- 保留 ask/on-request、user reviewer、Gateway 原生 elicitation、owner decide_call
  和一次 HTTP 许可；逐次批准策略及 worker 执行代码未改。未知确认、许可消费、原生
  completed 不能额外推导成供应商业务成功。

## 实际验证

修复前新增用例分别复现：HTTP `source=history` 返回 400、Promise 清理窗口少一次
observe、迟到 started 遮住历史结果、不同键顺序的 JSON 不能去重；修复后定向回归通过。

- Host：相关 session／HTTP 路由定向测试含 `-race` 通过；go vet 通过。新路由测试
  核对缺省/history/events 的分发、请求 ID 回显、旧客户端截断提示，以及重复／未知
  source、额外参数仍拒绝，且无提交副作用。首次读取用例同时覆盖空 started 和含
  同 Item 的 started，并核对下一次正常重建快照。原关联冲突、原生身份、失败状态、
  通知热读不重读 thread 的回归保持通过。
- Desktop 前端：40 项 API client／组件／composable 用例通过；最后一次修改后的
  composable 15 项复验通过。vue-tsc、受影响文件 ESLint 通过。覆盖空闲结束窗口
  通知、导航隔离、不同调用需要新决定、未知决定不重发及时间回拨时的展示顺序。
- Native：1 项真实临时 SQLCipher 持久化测试与 5 项观察测试通过；rustfmt 通过。
  SQL 测试使用正常关闭重开，实际验证 46→47、132 条事实窗口、最多 128 个准确
  pending 身份优先保留、ack／unconfirmed 不丢失、墙钟回拨、scope／轮次隔离、
  事实去重、原 outbox 计数和尝试次数不变、会话删除级联及外键检查。未打开日常库。
- Contracts：23 项定向 Node 用例通过；Go Host SDK 测试通过、v2 SDK 编译通过。
  两个 Host wire schema 相对 fallback `2592f5d5b07fcd92de10d25c4dcf73bd1ce03cb5`
  的定向结构破坏检查通过。语义方向另按下述发布与回滚约束复核，不把结构绿色冒充
  所有跨版本行为兼容。
- 严格 Clippy 仍因两处既有代码失败：`database.rs:2885` nonminimal_bool 与
  `document_preview_native.rs:997` cmp_owned；这两个文件相对本轮前逐字未改。
  未压制告警，也不声称全仓静态检查通过。

## 兼容、启用和回滚

1. 本次不增加 DTO 字段、枚举或数据库迁移；契约所有者仍为 Contracts，Host 生产
   工具快照，Desktop Native／UI 消费。Provider／Experts 只因共用 source loader
   刷新来源记录，Connectors 执行协议和实现不变。
2. 新 Host 接受旧工具 GET（无 source），保留旧 reader 对独立 JSON 的不完整提示；
   新 Native 的显式 source 需要支持该选项的 Host。旧 Native 的只读形状回退不等于
   可以把新 Native 与任意旧 Host 混搭。应先具备本次 Host，再通过正常入口装配
   匹配的 Native/UI；本次只验证本地候选，没有提交、发布或重启激活。
3. 当前 SQL 47 的存储格式和事实内容保持；仅取消本轮读取修复无需降库。若整体回滚
   P2，必须保留支持 47 的 reader，关闭 writer 也不能降 user_version、删除事实或
   重发未确认决定。撤销本轮修复会恢复上述缺口，不能当作已验证的可靠回滚版本。
4. 使用修改前逐文件副本核对增量；禁止 reset 整仓，尤其不能覆盖已有启动／来源记录
   与两项 P1。来源候选必须由 canonical 脚本重新生成，不能手改摘要绕过检查。

## 尚未执行与边界

没有重启易界或执行真实 GUI／供应商／付费模型验收，也没有强杀、可执行文件替换、
权限破坏或攻击性 fixture；测试只用普通 JSON、正常异步通知顺序和临时数据库。
因此这是源码、契约与定向分层验证完成，不是当前运行实例已激活，也不是生产发布验收。
升级前没有持久化的决定不会补造；没有 MCP 回包时仍无可关联的原生 Item；原生 v6
对独立 structuredContent 的部分展示边界仍由市场结果视图补充，不扩展 Runtime 协议。

## 最终来源与工作区核验

canonical generate／sync 与完整固定开发客户端只读构建来源检查均通过；检查核对
656 个 Host 构建输入。`native-skill-build-candidate.mjs --freeze` 相对本轮前仅改变
host_sources，release=false、Runtime 和其它来源身份保持。该步骤没有启动服务、
安装或替换正在运行的制品。

最终改动范围：元仓 2 份文档；Contracts 19 份源／生成／来源文件；Host 12 份文件
（5 份实现／测试，其余为消费快照和来源）；Desktop 20 份文件（6 份 Native／前端
实现及测试，其余为生成或构建来源）；Connectors 仅 1 份 provider 来源记录。
所有仓库 HEAD 不变；Runtime 工作树干净；原未提交启动脚本、迁移 47、P1 策略／
worker 执行改动等非本轮修改文件保持字节一致；逐仓 `git diff --check` 通过。

主要可复跑命令（均离线或仅本地）：

```sh
# yijie-agent-host
GOTOOLCHAIN=go1.26.5 GOPROXY=off go test -race ./internal/session ./internal/app -run '^(TestMarketP2.*|TestFEAT157MarketCompleteStructuredCopyIsNotTruncated|TestMarketResult.*|TestFEAT157MarketToolProjectionKeepsNativeIdentityWithoutGuessingCall|TestMarketHTTPReadOnlyViewsAndOpaqueTrigger)$' -count=1
GOTOOLCHAIN=go1.26.5 GOPROXY=off go vet ./internal/session ./internal/app
# yijie-desktop
pnpm exec vitest run src/components/chat/MarketChatActivity.test.ts src/api/market-host-native-client.test.ts src/composables/useMarketChat.test.ts
pnpm exec vue-tsc --noEmit
# 两条 Native 命令使用原 .local/development/target 与 .local/cache/desktop 缓存
cargo test --offline --locked --manifest-path src-tauri/Cargo.toml --lib --features kimi-k31-pro-candidate chat::connectors::decision_facts::tests:: -- --nocapture
cargo test --offline --locked --manifest-path src-tauri/Cargo.toml --lib --features kimi-k31-pro-candidate chat::connectors::observe::tests:: -- --nocapture
# yijie-contracts
node --test tests/market-observation-p2.test.mjs tests/market-call-receipt.test.mjs tests/market-host.test.mjs tests/market-broker.test.mjs
node scripts/check-jsonschema-breaking.mjs 2592f5d5b07fcd92de10d25c4dcf73bd1ce03cb5 --schema=compatibility/market-host/wire.schema.json --schema=compatibility/market-host-v2/wire.schema.json
```

未执行不安全测试或全量回归；本轮新例均为普通输入、参数选项或正常通知到达顺序。
