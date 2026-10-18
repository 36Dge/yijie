# FEAT-160 原专家聊天历史状态恢复

2026-10-18。用户明确要求继续审计修复原UI设计师聊天，复用恢复能力、不改Codex内核、不直接改数据库、正常真实验收。contract-impact=semantic；local/demo_fast。本轮不提交/推送/发布。

## 已核实事实与方案

只读现有Host API返回会话d0f8c98b-c7ff-4123-92b1-a999ce8b3034仍active、active_turn_id=01a14a7b-ef40-7700-8ae9-cbb9b80eae24；同一原生线程01a14a7b-eeea-7221-a62a-d14902dbeb7f当前notLoaded，原生历史该轮次interrupted。市场/专家提交在SwitchThread之前被旧Host状态拦截，普通ResumeSession又刻意拒绝market purpose。Desktop把可信busy拒绝也一律保存为uncertain，查询无原回执后持续等待。

方案：Host在可信新提交、原身份/模型/专家及无未决操作检查之后，仅以匹配的原生终态和非active当前状态作为证据，复用Store.Resume及native revision保护收敛私有运行索引；原有SwitchThread仍执行正常unsubscribe/resume。原生历史/消息/专家绑定不重建。

Native继续首先查询原提交。仅原attempt持久化了来自可信pipe的busy，且当前相同scope/task/session的Host明确确认原账本缺失，才用原market_mark(blocked)结束该次准入失败；不自动补发。原回执已accepted优先沿既有accept绑定。404独立、缺失/损坏账本、超时或其他错误仍unknown。Host读接口只在真正ErrNotFound且仍有同一合法会话映射时返回not_found，不把存储读取错误伪装为不存在。

复用来源：Codex stable thread/read、Host ReadNativeThreadV2/ReadNativeThreadStatusV2/Store.Resume、原有modelOperationMu/notificationMu/NativeRevision、Native唯一Coordinator和market_mark/expert_accept。无新增endpoint、command、权限、依赖、DB schema或第二套恢复引擎。

不采用：直接清库/改状态、把notLoaded当历史未执行证明、重发旧未知操作、重建专家聊天或另起原生线程。

## 必须验收

1. 旧原生interrupted历史保留；同一聊天/线程/专家恢复可继续发送。
2. 真实新请求仅执行一次，原未知消息不自动补发；正常重启后恢复结果保留。
3. 普通样本验证active/缺少匹配终态/审批/未决回执仍不放行，较新的notification胜过旧读结果。
4. trusted busy和真正缺失回执可收敛；accepted优先；其他unknown不转failed、不重发。
5. Codex源码/二进制摘要不变，已有FEAT159媒体功能改动保留。

已有工作树含FEAT159未提交代码，全部保留；本次只增加恢复修复与同源消费pin。源顺序：Contracts transport语义→现有生成/sync→Host/Native→canonical本地freeze和构建。旧reader仍可读现有blocked/failed，无存储迁移；回退不撤销已确认原生事实。

## 安全和验证

正常只读查询、单元/race测试、正常退出重开和真实模型短文本。禁止强杀、权限破坏、二进制篡改及攻击fixture。模型额度单独获批最多3次，实际使用2次，原聊天真实收发及正常重启通过；不转用FEAT159余额。真实用户数据库只由正常应用流程操作。
