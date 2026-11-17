# 连接器 P1/P2 实机验收记录

日期：2026-11-17。本轮范围是用户已批准的隔离本地连接器入口和 Native→Host→产品 Gateway→普通本地 MCP→GUI 实机验证。真实模型已获得用户许可并实际调用。未提交、未推送。

## 结论

逐次审批、原生 `_meta` 关联、SQL 47 决定事实、结构化展示和正常完成的事件刷新均有实机证据；真实 Kimi K3.1 Pro 也完成了一次审批后的本地样本调用。

正常停止存在一项明确边界：停止后的晚到原生结果可能不再通过实时事件送达，须显式读取历史或重开。界面已修正为保留只读决定/结果未确认，不再持续显示过期的“执行中”，不猜测成功、不自动重试。不能将本轮结果表述为所有取消时序和故障边界均已通过。

证据目录：`yijie-desktop/.local/market-architecture-verification/2026-11-17-local-protocol/`。下文 JSON、日志均在该目录；源状态清单在 `repos-final.json`，包括完整 HEAD、变更文件及初始状态。

## 实机结果

| 项目 | 实际观察 | 证据 |
| --- | --- | --- |
| 拒绝 | 真实审批卡点击拒绝，上游 tools/call 增量 0；原生结果 failed、decision=reject、许可未消费；SQL requested/acknowledged 各 1 | `case-reject-result.json` |
| 同轮相同参数两次批准 | 两张独立审批卡，分别允许一次；恰好新增 2 次上游调用；argsDigest 相同，callRef、decisionId、nativeItemId 各不相同 | `case-twice-result.json` |
| 原生关联 | 对全部 11 个有终态的工具 Item，逐项读取 Runtime rollout 的 `mcp_tool_call_end.result.Ok._meta["yijie.market.call"]`，与 Host correlation 完全相同；再核对原 thread/turn/operation/selection/ref 与 SQL 决定 | `native-correlation-matrix.json`、`real-model-native-meta.json` |
| SQL 47 | 通过 Native 正常决定写入从 45 升至 47，最终 22 条 requested/acknowledged 事实；两次正常关闭/重开分别保留 14、20 条，outbox 的状态和 attempt_count 没有因重开增加 | `native-final-closed.json`、`case-reopen-result.json`、`case-reopen-r7-result.json` |
| 结构化结果 | 纯 JSON 可见；不同文本摘要与 JSON 同时展示；普通 isError=true 仍显示执行失败，批准/许可消费不会变成成功 | `case-structured-error-result.json`、`case-twice-result.json` |
| 正常慢调用 | 普通 MCP 等待 12 秒；驱动接续真实 Code Mode cell 的原生 wait；GUI 自动由执行中变为完成，没有点刷新 | `case-events-result.json`、`peer-r4/protocol.jsonl` |
| 观察开销 | 此慢调用测量窗内：23 次 approvals、5 次 events、0 次 history/thread_read；随后空闲 32.922 秒无新增读取 | `slow2-inflight.json`、`slow2-idle-start.json`、`slow2-idle-end.json` |
| 正常停止 | 真实“停止生成”，没有强杀。SQL 决定保持；MCP 端真实收到请求，随后正常返回。原生晚到回执为 failed/结果未确认，admissionConsumed=true；未据此声称上游未执行或成功 | `case-cancel-result.json` |
| 停止后刷新 | 轮次结束时仅对仍未结束的快照补一次原生 history；此次即时读取尚无终态，界面保留只读决定且不再显示执行中。空闲 26.375 秒无新增读取；重开显示后来保存的原始失败回执与批准关联 | `cancel2-idle-end.json`、`case-reopen-r7-result.json` |
| 真实模型 | 原入口 `--market-acceptance p1p2-20261117 --real-model`，原生模型 `kimi-k3.1-pro`、approval_policy=on-request；真实 tool_search/Code Mode 调用，只新增 1 次 marker=real-20261117 的本地 MCP 请求；本地 Responses peer 请求数保持 8，Native 有真实 token_count 记录；GUI 最终完成 | `case-real-model-result.json`、`real-model-native-context.json`、`real-model-routing-and-usage.json` |

实时事件开销测量期间没有调用审计脚本的 Host history 接口；之后的显式历史证据采集不计为产品轮询。普通本地 Responses 驱动的任务不冒称真实模型推理；只有最后一轮使用真实模型路由。未调用真实连接器供应商。

## 实机发现与修正

1. **决定时间单位错误。** `decision_facts.rs` 复用了安装状态的秒级 now()，使毫秒契约的 UI 显示 1970 年。现在 writer 独立写 epoch milliseconds；新决定实机显示 2026/11/17。旧 append-only 事实保持原值，展示明确标注时间单位异常，不猜测修正时间，不影响按 append 顺序、原身份关联。
2. **停止后的旧执行中快照。** Native 历史已有/稍后写入终态，但停止时事件快照未闭合。`useMarketChat` 在 active→idle 的最后事件读取后，仅对未结束项补一次原生 history；有结果就采用原生结果，无结果就保留只读决定。没有持续空闲轮询、Runtime 补丁或新审批数据库。
3. **验收驱动两处真实错误。** 初次按 worker 长名拼 JS binding，未使用 Codex 缩短后的原生发现名称；后来慢调用未接续 yielded cell。现改为读取真实 tool_search 输出及最新当前轮次的 cell ID，调用原生 wait。失败现场保留，未补写成功记录。
4. **隔离装配与说明。** 本地模式关闭统一媒体开关时还需同步关闭 image generation；补齐并通过 Host 装配定向测试。本地无密钥服务不再沿用 Shopify 商品目录说明。
5. **启动检查器。** gofmt 经 stdin 在本机嵌套入口阻塞，改用自身临时 Go 源文件调用同一个标准格式化器。7 份 SDK 输出逐字不变；按 canonical 脚本重新生成来源锁并同步 Connectors、Broker 下游。没有手工伪造 hash 或跳过检查。

## 修改边界及原生复用

`contract-impact=semantic`，源配置版本 0.1.0、release=false；仅为当前 sibling 工作树的本地候选，不是发布兼容性批准。

| 仓库 | 修改范围 |
| --- | --- |
| yijie-contracts | `compatibility/market-local-acceptance/profile.json` 为唯一隔离配置源；同步脚本复制三个消费者；格式化器 IO 修复及 canonical 来源元数据 |
| yijie-connectors | 同一个正常产品 worker 的显式隔离参数与固定 loopback provider；普通默认注册表仍为 61 项，资格测试二进制仍不能充当产品 worker |
| yijie-agent-host | 独立 Home/标签校验、正常 Owner/worker 装配、关闭未选供应商功能、有限且不含参数/凭据的验收读计数 |
| yijie-desktop | canonical start-ui 隔离入口、独立 Native 数据、单一验收目录、明显环境提示、普通协议端；决定毫秒时间修复、历史异常时间提示、停止后单次原生对账 |
| yijie | 方案和本报告 |
| yijie-codex | 无源码改动，工作区干净 |

运行继续复用固定 Codex 的推理循环、tool_search、Code Mode/原生 wait、MCP client、原生 elicitation、线程历史和 `_meta`。没有另造执行器、审批数据库、权限缓存或 Runtime 补丁。新验收分支仍复用正常 generic adapter、Gateway 的逐次 owner/native 决定及单次 HTTP 许可。

最终正常构建 Native SHA-256：`0946e39f545ea8b698cbf49f5541ffbaf47ffcb1424b8f9918bdd0f0c150d5ce`。
固定 Runtime 源 HEAD：`5c64ed3f03808639faf7c11674e87636a94ab221`。六仓 HEAD 均未改变。

## 定向验证和未覆盖项

- 同源配置检查、canonical 启动前/启动后来源检查通过；Host 受影响 app/owner/proxy/http 测试及 go vet 通过。
- Worker cargo check、隔离默认关闭测试及 strict Clippy 通过；Native cargo check、隔离配置测试通过。
- Native 决定模块 2 项测试通过，包含毫秒单位和正常 SQLCipher 重开不重放。
- 先前相关前端 42 项通过；时间/目录展示补充 31 项通过；最终停止刷新/展示相关 34 项通过（集合有重叠，不能相加为独立总数）。受影响 ESLint、最终 vue-tsc、六仓 git diff --check 通过。
- Native strict Clippy 仍被当前 HEAD 已存在的 `native_auth/local_service.rs` 六处 unit_arg 告警阻挡；该文件本轮未修改。不声称 Native 全量 lint 通过。
- 128 条窗口、精确并发/乱序竞态、跨版本生产发布、真实供应商认证、全部主题/最小窗口视觉覆盖未在本轮实机穷尽；旧定向测试不能代替这些实机证明。
- 没有制造决定送达不确定、进程崩溃、文件权限异常或攻击 fixture。因此 unconfirmed 送达路径没有实机故障覆盖。
- 原生通用 elicitation 仍不提供审批前 Item ID；终态通过原生 `_meta` 与原身份闭合。本轮 1 次早期驱动提前结束没有原生终态结果，保留未关联的决定事实，不报告成功。
- 保留一次自然审批超时（第二次没有点击成功）以及早期驱动失败；相应 JSON 明确不是通过记录。

## 清理与回滚

已通过 GUI 正常停用隔离连接器、⌘Q 退出 App；canonical 启动进程 exit 0。普通协议端在 inflight=0 后调用自身 stop 接口退出。没有强杀产品进程、改权限或替换二进制；正常构建产物均由项目入口生成。此前阻塞的无副作用 gofmt 子进程仅用一次普通 SIGINT 取消，失败日志保留。

日常 `demo-fast-v1` 数据库和密钥文件哈希与验收前一致，WAL/SHM 状态未变（`daily-before.json` / `daily-after.json`）；没有打开日常 Native 数据库做迁移。隔离 Native、Host、Runtime 数据与全部证据保留。

回滚隔离入口：正常关闭后，不传验收 selector，按原日常入口启动；不移用隔离 Home。若撤销候选源码，使用标准构建重新生成产物，不复制覆盖旧二进制。保留决定时间修复；回退到旧 writer 会再次写错单位。SQL47 不降级、不删除事实；不支持 47 的旧 reader 不能直接打开该隔离库。恢复日常入口不会重放验收决定。
