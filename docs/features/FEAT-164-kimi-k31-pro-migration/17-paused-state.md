# FEAT-164 暂停与恢复记录

2026-10-25 01:04（Asia/Shanghai），用户明确要求「记录状态与信息，暂停执行」。当前为用户主动暂停，不是完成或验收通过。等待用户明确恢复后再实施、构建、提交或发起真实调用；不自动续跑。

## 已有授权与实际提交

用户已批准新增 Host 23 文件、Desktop 33 文件中 FEAT-164 专属差异及对应治理记录的本地提交；禁止推送、混入其他需求。用户另批准本轮真实 Kimi 验证费用上限人民币 20 元，允许搜索和图片。该授权保留，但暂停期间不消耗；未继承 FEAT-162/163 额度。

| 仓库 | 已完成的本地提交 |
| --- | --- |
| yijie-codex | 57753db451b29a49315ddcb6449ca146171c4de7 |
| yijie-contracts | b0060c8bc4fb924cec14d98b193c32c69482b7b7 |
| yijie | 17345c91faf44dabb3b631b2d977ecefb85d6179（上一轮源固化） |
| yijie-agent-host | ff7d05dae4b3a48285e9bed63ba7253081da234c（本轮批准的 23 文件） |
| yijie-desktop | 3dc2205fba79a0a1d7fdea8a4b767d35f2c286b1（本轮批准的 33 文件） |

Host/Desktop 提交使用已经审阅的 FEAT-164 专属 patch 加入 index，没有整文件暂存共享改动。两仓提交前 `git diff --cached --check` 通过。提交后 index 为空，进入本轮时记录的所有工作文件内容摘要保持；没有追加实现编辑，没有 push、tag、分支切换或 Git 身份设置变更。精确清单与状态见 [暂停快照](evidence/paused-state-20261025.json) 和 [本轮起点](evidence/g2v-authorized-start.json)。

元仓上轮下游审计、证据及本轮暂停/授权记录仍在工作区，尚未完成对应治理记录的后续本地提交；用户暂停后只保存状态，不继续该提交。FEAT-162/163 及其它既有改动保持，尤其项目记忆只更新 FEAT-164 段。

## 门禁、验证与运行状态

- G0/G1/G2/G2A 已通过；G2V、S1—S4 和三项 final 仍 NOT RUN/pending。整体需求未完成。
- 上轮已验证默认关闭的最小候选、Runtime loopback 3 请求、App loopback 2 任务、持久历史恢复/续聊及同产物重开；详情见 [16 实施审计](16-downstream-candidate-audit.md)。本轮未追加产品验证，不将上轮本机结果改写成真实供应商资格。
- FEAT-164 至今真实模型请求 **0**，实际模型费用 **0 元**；本轮仅公开官方文档查询，没有读取真实 Key、查询账户余额或调用供应商 API。
- 暂停核验没有 FEAT-164 App/Host/Runtime 进程，loopback 18083/18086 均释放。此前服务均经正常流程退出；本轮无新服务需要停止。临时官方价格查询页已关闭。
- 新 Host commit 已改变构建来源。现有 `contracts/kimi-k31-host-build.candidate.json` 仍是当时审阅的 `local_worktree_candidate` 快照，不能冒充新提交的不可变 Host build pin；旧构建回执不得直接继承为 G2V 新证据。

## 已获得的官方信息与尚未完成的费用控制

本轮核对了官方 [模型首页](https://platform.kimi.com/)、[模型列表](https://platform.kimi.com/docs/models)、[Responses API](https://platform.kimi.com/docs/api/responses)、[推理计费说明](https://platform.kimi.com/docs/pricing/chat) 和 [搜索计费说明](https://platform.kimi.com/docs/pricing/websearch)。

官方首页当前展示 K3.1 Pro 输入/默认缓存写入 13 元/百万 tokens、输出 68 元/百万 tokens、缓存命中 1.30 元/百万 tokens。Responses 文档写明默认输出上限 131072、最大 1048576；默认 cache TTL 为 5m，usage 区分 cached/cache_write/uncached，不能按缓存写入缺失字段推导精确账单。

定价详情页 HTML、Markdown 和浏览器中的动态价格表为空；首页价目可以读到。搜索价目说明明确列出独立 Search Basic/Pro/Fetch 和旧 Chat Completions `$web_search`，本轮尚未确认 Responses 原生 `web_search` 的独立计费上界。不能把旧 `$web_search` 单价未经核实地当成新 Responses 搜索价目。

`scripts/chat-model-smoke-meter.py` 只支持旧 `kimi-k3` 等已有模型，会在非 preserve 模式注入 8192 输出上限；不具备本轮新模型的人民币硬限额。它有其它需求的既有改动，本轮只读，没有编辑或执行。新计量器/预算账本/安全 Harness 尚未编写或资格验证，用户回合、HTTP、token 操作上限尚未落盘。20 元与搜索/图片授权已存在，恢复时应在其以内设定保守可执行限额；无须重复索取已经给出的额度许可。不得先调用再补计量，也不得把带预算参数覆盖的验证写成原始产品请求验证。

## 明确恢复后执行顺序

1. 读取本文件、feature.yaml、16 及本轮起点/暂停快照，检查新增工作区变化并保留；不要因当前暂停或 dirty 状态 reset、覆盖或混入其他需求。
2. 完成已授权的相关 FEAT-164 治理记录本地提交；原 Host/Desktop 提交不重做，不重复询问许可。
3. 将 Host 构建来源固定到真实提交，准备可复核的隔离源构建和 Harness 不可变引用。当前已提交实现可以作为起点，但完整工作树里仍有其它需求变更；最终构建不能将它们默认为已提交来源。
4. 完成 H-F164-LOCAL 的实际观测点及正常状态资格，保持无正文 verdict、四类失败区分、协作超时和正常清理；现有 4 个观察器单测仍不足以独立证明完整 Harness 资格。
5. 落实 20 元以内的预算计量、请求/输出/token/图片/搜索边界与停止条件。所有辅助请求/重试也计入；缺少 usage 时保留未知或预占，不按 0 费用处理。确认官方计费证据后才发真实请求。
6. 通过前置资格后，用 canonical App 做真实 Kimi→原生返回→保存→同产物重开与正常退出；G2V 通过才进入 S1→S4。继续严格遵守长期安全条款，不强杀、不破坏权限、不用可执行替身或攻击 fixture。
