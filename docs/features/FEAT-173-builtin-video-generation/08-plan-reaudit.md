# FEAT-173 深度复审与方案修订2

2026-11-12。用户授权只读复审并直接修订方案，仍不实施。本轮contract-impact=none（文档）；拟实施additive保持，但删除了可能改变既有Artifact行为的部分。修订1归档可核验，当前04/05/02/07及ADR/manifest均为修订2。

## 已确认的方案缺口

| ID/级别 | 原问题 | 源码/事实依据 | 修订 |
|---|---|---|---|
| R01 / P1 | 视频持久ACK、manifest恢复与重建spool被写成原链路复用，实际会建立另一套恢复语义 | Host artifact.Store.OpenStore/Status/Acknowledge为当前代事实；Desktop recover_pending_acknowledgements不能弥补Host无entry，begin_artifact_transfer拒绝failed/cancelled | 删除专用ACK/manifest与spool重建；只记录首次handoff标记；交付后只引用原Artifact，未知如实报告 |
| R02 / P1 | get要求模型提供可能从未收到的句柄，创建已成功但MCP返回丢失时恢复入口不闭环 | Host持久task ID并不保证工具结果已经进入Native历史；普通MCP没有替业务找回供应商ID | get ID可省略，仅解析本聊天确定归属；歧义返回有界本地候选，不猜最新、不查供应商列表 |
| R03 / P1 | 同root幂等挡不住停止后新root误调用创建，可能重复计费 | 原生新用户回合有新turn ID；root预占键会变化 | 同聊天未决检查与新预占放同事务；原操作未决/unknown时拒绝跨root新POST；首期并发独立需求用新建任务 |
| R04 / P1 | 创建root与后续查询root生命周期没有明确分开，容易复用已取消context或被旧终态误取消 | FEAT-172按匹配turn收尾；恢复发生在新的合法根轮次 | 身份保留创建root，观察使用当前root context；网络/锁后/下载/发布前检查；旧停止只管旧观察 |
| R05 / P2 | 用当前150s配置作为单工具方案不适用的主要理由，易误判原生能力；next_action也不能假设自动调度 | mcp_types.rs允许配置Duration；原生Code Mode已支持yield/wait；结果仍由模型续轮决定 | 明确原生长等待已有；选两工具为持久归属；不造Agent等待/自动续轮系统 |
| R06 / P2 | 专家隔离原则正确，但恢复与选择生效前后HTTP的边界欠明确 | 现有expertBinding revision、Idle/ActiveTurnID、pending selection门禁可复用 | 每个恢复/后续请求按当前绑定复核；只保证选择生效后不发新请求，不声称已经发出的HTTP从未发生 |
| R07 / P2 | 新UUID、独立8天TTL/1024配额清理与ACK副本超出最小记录需求 | root ID、session cleanup、Artifact存储均已有 | 复用root ID与聊天清理；一root一有界记录、更新原位，不建轮询事件库/配额守护 |
| R08 / P3 | 首尾同图要求用户重复附图，增加不必要操作 | 供应商允许相同首尾图，现有索引足以表达 | first_last_frames允许[1,1]；reference_images仍不重复 |

这些是方案缺口，不是声称已有FEAT-173产品Bug或已执行回归。重点源码摘要见references/reaudit-source-evidence.json；未运行产品测试或真实调用。

## 保留与收窄

应用内置MCP归属、同Key、固定模型、默认参数、四种文本/图片输入组合、专家不兜底、原视频组件均保持。没有新增Runtime、Skill、Broker、前端或凭据机制。

恢复现在按三层分清：

1. 原生执行/等待由yijie-codex提供，不能用Host取代。
2. 已存供应商身份的首次交付前操作可跨合法观察root继续；POST结果无ID只能保留unknown，不凭空恢复。
3. Artifact首次交付后保持既有Native提交/预览与ACK行为；Host重启unknown不能倒推出失败，也不承诺自动补领。

一次handoff标记只用于禁止重复生产，记录在首个事件之前；标记后即使没能发出事件也只能报告未确认，这是明确的保守边界。它没有持久化Native提交事实，不演变成影子ACK系统。

## 原生并行与幂等复核

McpHandler允许readOnlyHint=true的工具并行，即使server显式false；因此取结果仍设readOnlyHint=false，复用原生执行配置，同时用单操作预占确保不会重复下载/交付。原生rmcp-client当前只对特定tools/list错误重试，不替tools/call实现业务重试。不能把hint、MCP RPC完成、Code Mode cell完成或工具正文当视频任务完成/Native提交。

## 官方语义复核

重新阅读[取消/删除](https://docs.volcengine.com/docs/ark/cancel-or-delete-video-generation-tasks-api?lang=zh)与[精确查询](https://docs.volcengine.com/docs/ark/get-video-generation-task-api?lang=zh)：running不支持DELETE，终态DELETE删除记录；原任务与产物URL有效期不同。首期不自动DELETE/列表的决定保持。复核只访问文档，没有调用账户API。

## 验证与授权

修订2增加无句柄恢复、同聊天跨root防重、观察context分离、选择切换、handoff标记前后以及Host unknown/Native ready并存测试；同时要求自然语言“停止后继续/刚才的视频呢”验收，避免只测人为正确ID。

本轮只执行文档结构、元仓治理和源码保持检查，结果在references/reaudit-checks.json。全部产品Must AC仍pending、D4 NOT RUN、调用额度0，未提交/推送。自审不是独立人工批准；方案仍Proposed。

本次实际检查：严格Feature Package结构/语义、元仓lint、57项文档治理测试、Shell语法、diff、内部链接与源码保持均通过。7仓HEAD、原55个源文件和16个重点复核条目未变，6个业务依赖仓clean；PASS仅适用于文档。
