# 网页深度搜索实施与验收

2026 年 11 月 19 日，本机易界日常开发版使用 Kimi K3.1 Pro 和 MiniMax M3 各完成一轮杭州行程。两轮使用相同的 2026 年 11 月 20 至 22 日行程、自动工作空间和请求批准设置，先后从桌面发起。下表仅统计内置工具 `kimi_web_search_pro`。[逐项回执、操作和制品摘要](../../../../yijie-desktop/.local/development/deep-web-search-v2-verification-20261119/live-verification.json)

| 实跑 | 模型调用 | 不同完整参数 | 实际派发 | 繁忙未派发 | 同参复用 | 首次查看 / 客户端重开后的卡片 | 整轮用时 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Kimi K3.1 Pro | 9 | 9 | 9 | 0 | 0 | 9 / 9 | 9m53s |
| MiniMax M3 | 34 | 34 | 30 | 4 | 0 | 34 / 34 | 7m20s |

按原生轮次的授权范围查询了数据库中的所有操作，并逐项核对 claim、执行器发送和供应商响应。39 项派发均各有 1 次 claim、1 次发送和 1 个 HTTP 200。Kimi 另有 14 次原生 `webSearch`，两个模型各有 4 次网页读取。MiniMax 的 4 个繁忙请求在 8.014 至 8.017 秒返回，均未创建供应商操作。本次实际观测的供应商并发峰值为 Kimi 1、MiniMax 2。两轮结束后正常退出客户端，再从侧栏分别重开任务，Runtime、worker、桌面制品摘要一致，新增深度搜索操作为 0。[Kimi 桌面](../../../../yijie-desktop/.local/development/deep-web-search-v2-verification-20261119/kimi-desktop.json) · [MiniMax 历史重开](../../../../yijie-desktop/.local/development/deep-web-search-v2-verification-20261119/minimax-history-desktop.json)

**回答覆盖。** Kimi 的首次灵隐定向检索返回 0 条。换词后收到 10 条资料，独立的天气查询收到 8 条。最终回答给出了灵隐实名预约入口和逐日天气来源，游船具体票价留待当天公告确认。MiniMax 回答列出了预约入口、两类游船票价和逐日天气，并附来源。Kimi 回答的 3 个链接均能对应到检索来源。MiniMax 的 14 个链接中，13 个直接对应来源网址，另 1 个出现在已返回的网页内容中。此处核对的是模型取得和使用的材料。[Kimi 实际回答](../../../../yijie-desktop/.local/development/deep-web-search-v2-verification-20261119/kimi-answer.md) · [MiniMax 实际回答](../../../../yijie-desktop/.local/development/deep-web-search-v2-verification-20261119/minimax-answer.md)

## 固定回放与交互验证

| 场景 | 验证结果 |
|---|---|
| 杭州预约、船票和天气三主题 | 9 个录制请求产生 3 次回放派发，每个主题保留 5 个来源。在实际 Kimi Runtime 向本地模型端发送的下一步输入中，逐一匹配了 3 个主题、15 个来源的索引和网址，批次正文为 8,921 字节。 |
| Kimi 原来的空结果循环 | 整轮 20 个逻辑调用对应 10 个原操作。其中 11 个同参调用跨两个活动组，只占一张「0 条结果 · 已复用 10 次」主卡，展开保留 11 条明细。 |
| MiniMax 旧记录 | 按原记录还原繁忙位置后，24 个逻辑调用中 19 项派发、5 项未派发。包含 1 项 HTTP 已响应但业务校验失败的原操作。 |
| 模型继续要求相同结果 | 两种模型配置均通过本地可交互测试。首次完整空结果后连续两次只请求原材料，Runtime 给出一次可继续用工具的纠偏，再进入有界作答。同一步混合原空结果、天气补查和读取新正文时，模型端能收到相应材料。 |
| 恢复、权限、排队和返回质量 | 已结算失败、发送后结算未知、调用方断开、凭据续期、撤权、缓存逐出、参数变化和新轮次均经验证。四路提交最多占用两个执行位，正常取消排队请求得到未派发回执。国际化网址规范化、部分有效资料、真实空结果和接近 64 KiB 的回执均有回归覆盖。 |

固定回放使用原始查询参数和录制的供应商业务结果，通过新版网关、隔离 PostgreSQL、产品 API、Host 展示投影和桌面组件执行。Kimi、MiniMax 的真实任务均未提出完整参数相同的请求，重复展示和纯重复收尾由录制回放及交互测试触发。旧 MiniMax 的 HTTP 200 后无效结果没有保留具体失败字段，本次验证覆盖了该状态下同参重读的行为。[回放结果](../../../../yijie-desktop/.local/development/deep-web-search-v2-verification-20261119/fixed-replay.json) · [可复跑的本地入口](references/replay-scoped-search.py)

## 实现与兼容

- Host 为已授权的根轮次、调用轮次和绑定派生可恢复的搜索范围。产品 API 对绑定、准入授权版本、范围和完整参数摘要建立事务性唯一关联。模型调用保有自己的 ID，已知原操作使用专门的鉴权 GET 取数，已确认发送或可能已发送的操作保留原引用。已获准入的操作可在独立等待者离开后按原截止时间结算。[操作准入与读取](../../../../yijie-api/internal/modules/webretrieval/infrastructure/postgres/repository.go) · [网关合并与订阅](../../../../yijie-connectors/worker/src/builtin_web_gateway/scoped.rs)
- Runtime 在内层取得受信回执，在整个采样步骤结束时核对实际交给模型的材料。Kimi 的工具发现、Code Mode 和 MiniMax 的平铺工具名共用判断。包含新材料或其他工作的步骤继续执行，最终收尾前检查仍在运行的任务。[Runtime 实现](../../../../yijie-codex/.yijie/patches/chat-models/0027-scoped-search-progress.patch)
- 桌面先按整轮原操作归并，再生成活动分组。主卡位于首次出现的位置，明细保留逻辑调用 ID 和原顺序。旧记录使用原有投影。私有准入、执行结算和 Native 显示均保留旧读端可接受的格式，新读端协商取得版本化回执。[Host 投影](../../../../yijie-agent-host/internal/session/deep_search_receipt.go) · [桌面分组](../../../../yijie-desktop/src/domain/conversation-activity-presentation.ts)
- 网关保留两个执行位，按剩余时限等待最多 8 秒，获槽后复核授权并预留供应商请求及结算所需时间。执行器按返回行使用公共契约校验，保留可读来源、丢弃数和脱敏诊断字段。日常客户端先完成 worker 构建，再启动使用该制品的执行器。本地数据库已通过标准迁移入口升级到版本 8。[规范化逻辑](../../../../yijie-connectors/worker/src/kimi_web_content.rs) · [服务启动](../../../../yijie-infra/scripts/builtin-web-session.py)

四份变更后的 OpenAPI 已分别对照 Contracts 基线 `00c371a3b5dc480a1d3ef79961bd6b965827347c` 进行兼容检查。原生历史与旧版本投影另外运行了闭合 schema 回归。验证范围为本机日常开发版。
