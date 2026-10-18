# FEAT-160 最终验证记录

2026-10-18，canonical local/demo_fast，原日常数据。最终实现与真实验收通过；仅本地候选，未提交、推送或发布。本任务获批最多3次短文本，实际2次，未使用第三次或图片、视频、商家工具。

## 结果

原UI设计师聊天已恢复可连续收发。最终构建中首次请求和正常退出重开后的第二次请求均收到真实模型回复，每次恰好增加一个原生轮次。原专家、聊天身份和历史保留，旧准入失败消息没有被自动补发。

| 标识 | 保留值 |
|---|---|
| 本地聊天 | `01a14a7b-ee79-79d1-9950-a75762a3fbe8` |
| Task | `01a14a7b-ee79-79d1-9950-a76d2e8f49f2` |
| Host session | `d0f8c98b-c7ff-4123-92b1-a999ce8b3034` |
| Codex thread | `01a14a7b-eeea-7221-a62a-d14902dbeb7f` |
| 专家 | UI设计师 0.1.1 |

| 阶段 | 实际观察 |
|---|---|
| 修复前 | Host active/旧active_turn_id；原生notLoaded，唯一旧turn interrupted；本地第二次提交长期uncertain并锁输入区 |
| 原回执恢复 | 原Coordinator确认可信busy及真正无原回执，旧本地提交转failed、原消息保留；原生仍只有1个旧轮次，无自动补发 |
| 最终构建页面 | failed下显示“本次提交未成功，原消息已保留。”，不再误显示正在等待；专家绑定保留 |
| 第1次真实提交，16:52 | 回复“UI设计师恢复验收完成”；turn `01a14e36-a7cc-7fd2-ad94-27d856cd5dca` completed；原生计数1→2，Host idle/active为空 |
| 正常退出重开 | Cmd+Q，launcher44499 exit0；App/Host/adapter和18081清理。`pnpm tauri:demo-fast:app --reopen`同构建来源核对通过；原历史、旧failed、第一条新回复及专家全部恢复。Host仍idle，原生仍2轮 |
| 第2次真实提交，16:54 | 回复“UI设计师重启恢复验收完成”；turn `01a14e38-6541-7b30-9ea7-214a48dfb1cb` completed；原生计数2→3，Host及原生status均idle、active为空 |

旧原生turn `01a14a7b-ef40-7700-8ae9-cbb9b80eae24`始终interrupted。两条新轮次的item类型都仅为userMessage/reasoning/agentMessage，无工具调用。没有换聊天、换线程、删除历史或重发旧操作。应用最终留在原聊天完成页面。

## 定向工程检查

| 检查 | 结果 |
|---|---|
| Host `go test -race ./internal/session -run '^TestFEAT160' -count=1` | PASS：正常重开后同线程续聊和幂等回执；运行中或不匹配终态拒绝；新通知胜过旧读取；串行且双账本缺失才返回not_found |
| Host 既有正常专家提交、模型切换/移除、正常存储重开、普通线程绑定、pending apply/cleanup保护 | PASS |
| Host `go vet ./internal/session` | PASS |
| Native `cargo test --lib feat160_` | 2 PASS：确认busy结束等待并正常重开保留；其他unknown保持且不进入legacy重发 |
| Native 既有unknown两项与accepted原回执绑定一项 | 3 PASS |
| Native `cargo clippy --lib -- -D warnings` | PASS |
| UI ChatTurnGroup FEAT158 uncertain / FEAT160 terminal | 2 PASS，23未执行 |
| UI `vue-tsc --noEmit` 与两个改动文件ESLint | PASS |
| Contracts generate/check，Host/Desktop/Skills sync/check | PASS |
| Contracts正常源帧、digest、同源生成、既有恢复契约 | 5 PASS |
| canonical最终构建、同构建reopen、真实UI与Host API交叉验证 | PASS |
| D0 / D4 feature-package门禁 | PASS，exit0 |

首次clippy发现enum大小警告，改为Box后通过，没有抑制检查。首次真实UI发现failed下残留queued提示，已修复并用最终构建和重启复验。canonical freeze首次发现专家资源来源摘要未随Contracts更新，沿现有打包/同步流程修复后通过。首次最终UI检查遇Mac锁屏，等待用户手动解锁后继续，未绕过系统锁。具体过程见01记录。

## 实现与复用

- Host在新提交的原身份、模型、专家、审批及未决操作检查后，调用现有ReadNativeThreadV2/ReadNativeThreadStatusV2。只有同一原生线程最后一轮与Host旧active turn完全一致、全部读取轮次终态明确、当前非active，才复用Store.Resume和NativeRevision保护更新运行索引。既有SwitchThread继续执行正常unsubscribe/resume，不产生另一条线程。
- Native唯一Coordinator先查询原操作；accepted优先使用原expert_accept。只有持久化的可信busy与当前Host确认同scope/task/session下market和turn两本原账本都不存在，才沿原market_mark(blocked)结束本地等待。缺失回执本身、读取错误、超时及其他unknown不触发失败判定或重发。
- ChatTurnGroup复用现有状态显示分支，修正本地failed/cancelled下的等待提示，不修改原生执行事实。
- 无新增endpoint、权限、依赖、DB schema、migration或恢复引擎。业务状态只经应用既有事务更新，未直接修改用户数据库。

## 来源与安全

Contracts experts transport为semantic变更，wire版本不变。所有consumer通过既有生成与sync取得精确来源摘要。源锁更新通过原Skills package/Desktop sync刷新provenance，75条资源metadata及全部75份archive SHA逐项不变；Host仅同步审核目录摘要，无专家prompt/资源内容/安装历史变化。

构建复用日常FEAT159的existing source candidate，全部来自canonical脚本。FEAT159未提交改动保留，没有覆盖用户提供、已签名或发布的二进制。Codex工作树干净，固定产物摘要与任务前完全相同：

- binary SHA256 `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`
- manifest SHA256 `8b86a1a661f50beda1e0a0c96f81ddbdf959a9a07c2e756cc4b9b0eabc053b27`

未执行任何攻击fixture、故障注入、强杀、权限破坏或运行程序篡改。原因是用户硬性安全要求；影响是不能声称这些故障条件已有动态覆盖。只验证正常状态转换、既有保护逻辑及真实历史恢复。

## 限制与交付边界

仅本地candidate，没有公开发布资格。原生历史部分信息提示和旧中断事实如实保留，不补造缺失内容；原生终态不确定、读取失败或历史达到1024条投影上限时继续拒绝收敛。旧reader仍能读取现有failed/blocked状态，无数据库迁移；回退不撤销已确认的原生执行事实。跨仓交付顺序为Contracts源语义及生成物、consumer来源pin、Host/Native、canonical构建；本次未提交或发布不可变版本。

证据在Desktop `.local/feat160-before.json`、`feat160-after-receipt-recovery.json`、`feat160-first-model.json`、`feat160-after-reopen.json`、`feat160-second-model.json`及`feat160-final-build.log`、`feat160-reopen.log`。只读JSON只保存必要ID、状态和item类型，不含token或消息正文。UI真实回复及原专家由CUA读取核对。最终D4门禁结果在feature.yaml与01记录中登记。

后续状态：用户已授权复审后提交推送。对应记录见[提交前复审与来源](../FEAT-159-native-artifact-media/03-final-review-and-push.md)；本文保留原验收时间与历史故障事实。
