# FEAT-164 技术设计候选

本设计没有落地到产品。新增恢复/准入/激活能力均是待实现工作，不称现成能力。

> 2026-10-25 候选修正：实际 r1 出站包含官方 include 枚举未列出的 `reasoning.encrypted_content`；r2 将只对新 Kimi 省略该 opt-in，保留 max、搜索 sources、响应和历史处理。原预算适配器还须在去掉搜索时同步去掉依赖的 include。此修正仍按 Runtime 权威源先行和不可变下游 pin 执行；不是默认输出参数变更，也不证明首次 HTTP 400 的唯一原因。事实与限制见 [19](19-responses-400-audit.md)。

## 主链与身份

Contracts源 → Go/Rust/TS → Desktop/Native → Host模型路由与session → Runtime start/resume/turn → Moonshot Responses → 原生SSE/工具执行及结果回灌 → Host投影 → Native单一buffer/SQLCipher。

有效定义只有新Kimi及MiniMax；已知历史集合额外含旧K3。读取历史、终态回执与新执行拆开：HTTP header、schema、Host model availability、Native enum和相关market/experts包装全覆盖；若某旧consumer不能理解新值，来源/版本不匹配时拒绝混用。旧身份retired-known不等于实际选择unknown。

## 启动与截止点

拟增加同一管理边界内的activation资格与独立Kimi执行准入，不新增旁路服务。兼容构建须默认不领取尚未分类的旧模型工作，同时保持历史查询和MiniMax能力。当前总模型开关会关闭读取路由，不可拿它冒充所需能力。

顺序：核验来源与兼容reader → 在任何coordinator/market/scheduled worker启动前禁止派发 → 前向schema迁移及旧身份分类 → 安装claim/send双重退役准入 → 查询/正常恢复 → 正常收敛或明确取消所有受管模型工作 → 验证无旧进程/工作在途 → 固定cutover → 允许新profile新请求。

停止新增派发必须覆盖标题collector/pending starts、草案、工具后续Responses、Guardian及启用的子代理。父thread idle不是全图idle。若已有App仍在旧版本运行，先使用正常退出流程；不能对运行中数据进行本任务迁移。无法安全停止则不继续。

title outbox只有session ID，不能仅凭没有旧profile字段就放行。未派发的旧标题保留fallback标题并停止自动生成；阅读历史不触发新标题请求。新标题在确认当前选择后可沿现有链请求新模型。

## 受管配置和候选

冻结真实已知旧catalog/TOML前身，不再用新Definitions重建旧字节。分别执行原authority preflight/原子替换，保留trust和原Home。两个文件更新不是整体原子事务：必须明确允许的旧旧、新catalog+旧TOML、新新等实际可达过渡组合；只有精确受管来源可恢复到新新，任一未知漂移拒绝，Runtime启动在组合完成后。

Runtime修改canonical补丁及构建脚本，0006对新slug请求sources，0004/0005保留。新修订独立输出目录，不删除旧artifact腾位置。固定上游rust-v0.144.6/5d1fbf26c43abc65a203928b2e31561cb039e06d与Rust1.95.0。仅模型条件变化预期schema字节相同；若补其它协议字段必须重新判定。

身份链：Runtime patch/source/binary/manifest/schema → Contracts generate-runtime-chat-models及Go constants → Host runtimechatmodels/api candidate → Desktop runtime candidate → 由实际功能组合选择的artifact-media / experts / chat-model Host candidate → launcher实际路径/override和打包receipt。experts开启但artifact_media关闭时会选择experts-host-build.candidate.json，不能只验证日常media组合。旧binary留存不等于新Host baseline接纳旧manifest。

## 原thread迁移及恢复

正常历史打开只读。开始新执行前：读取旧Selection与revision → 确认retired-known → 校验idle/未决turn/批准/input/market/expert及辅助工作 → 创建**新的模型选择operation**，固定旧profile/revision、目标新profile和thread → durable intent → unsubscribe/resume到新目标 → 验完整thread/model/provider/effort回执 → Host提交selection/revision及终态operation → Native读取当前Selection → 才接受新turn。

普通ResumeSession要求传入profile等于stored profile，不能直接用新header续旧会话。新operation不得接管尚未完成的旧K3选择operation；后者只恢复事实或保留阻断。

候选operation阶段在既有model operation领域版本化保存：prepared、apply_dispatched、receipt_validated、committed及uncertain事实；不复用历史完成字段表达未证实成功。只保存非秘密身份/回执摘要。跨进程无事务，区分：

| 窗口 | 处理 |
|---|---|
| 意图已存且可证明未发配置调用 | 可明确取消该切换意图，保持原selection |
| 配置已发或回执缺失 | unknown；thread/read/config/read不足以证明model |
| Runtime成功但Host未提交 | 不显示成功；明确恢复同operation，重验完整Host和Runtime门禁后重新应用同一新目标 |
| Host已提交但Desktop未收 | 原回执只读返回，再取当前Selection；不再次配置或覆盖更高revision |

明确恢复是配置写操作，不能说“只读恢复已成功”。现有未完成同ID分支会绕过部分Host前置检查，必须补全再用；不自动重复resume。需要无写入自动确认时属于额外Runtime协议设计，本期不承诺。

专用恢复还须区分“本operation留下的switching/unknown”和其他未决工作：只有operation ID、原/目标profile、原revision、thread及持久阶段全部匹配，才允许处理自身非ready状态；普通选择仍要求ready。其他选择operation、turn、批准/input、market/expert及辅助工作继续阻断，不能泛化跳过。若该operation已committed，则只读返回原回执并读取当前Selection，绝不再次resume。测试必须同时覆盖“自身状态可恢复”和“其他未决状态仍拒绝”。

## 数据迁移与业务操作

候选0038仅扩三张子表profile CHECK，逐列复制原值，保留PK/FK/CASCADE/nullable、state/revision约束和隐式唯一索引；operation_id不增加outbox FK。使用本仓事务、foreign_key_check及migration ledger，不全局关闭约束、不修改旧0028。更新catalog、MAX_READABLE、migrate_to_target允许列表、models入口目标；覆盖15→新、29→新、37→新及已新重复启动。

Host bbolt恢复字段和reader格式按本仓source/version审查。新库写入前必须有可读新旧两代且能关新Kimi的兼容构建；没有就保持切换未激活。

普通/市场/专家请求取消是待实现独立领域能力。仅Native持久派发阶段及attempt事实足以证明never-sent时允许取消、释放其合法占用并保存回执；禁止依赖404/missing、当前无turn、空历史或重启来证明未发。queued并不天然等于never-sent。scheduled的现有证明规则可参考，不把专用API套到普通聊天。

旧payload/profile/digest不改；取消/对账合法变更delivery state。pending/unknown查询无法结清则可读但暂不可继续，用户重新发送也不能绕过同会话未决门禁。禁止用删除chat清理。所有claim/send（包括恢复/过期inflight/market）都受准入检查，避免盲claim耗attempt。

## 计划与授权

不直接UPDATE chat_plan_models.profile_id。先退役Kimi新执行资格，再用领域事务暂停旧计划、提升revision、撤有效grant、处理未来未执行slots；已占用run保持原snapshot/digest/预算事实且按恢复规则收敛。用户审阅新模型、保存新定义后再授权；已有聊天目标需与新确认selection一致。草案模型与执行模型分别核验，原input-only约束保持。MiniMax计划不变。

## Runtime辅助调用与参数

- Kimi现catalog无comp_hash，K3→新模型窗口相同，因此previous_model压缩通常不触发；Runtime确有该分支，必须用正常状态覆盖comp_hash/窗口/previous-turn组合。不能重写历史来躲过。
- 新子代理继承model/provider/effort；显式model override不自动切provider，role还可覆盖；已加载代理可能直接复用旧配置。迁移检查整个可达启用代理图，正常收敛后重建/恢复核验。market强制禁用multi_agent/memories路径保持禁用；不为AC启用。
- Guardian auto_review可选择专属model/override或当前model，计入预算并核实effective配置。review/start未发现Host暴露；memories默认关闭、另有独立模型默认值，保持关闭并证明不产生请求。
- reasoning.encrypted_content和其它额外字段接受情况为Unknown。沿实际Responses结构验证，不套Chat参数；保留tool_choice=auto、SSE终态工具参数恢复和原工具审批。
- 输出上限不能借升级改变：Runtime当前无max_output_tokens请求字段，旧8192是诊断meter覆盖。原始请求与预算覆盖请求分开记录；不能以截断场景成功/失败推断日常默认行为。
- Kimi网页Search/Fetch固定工具endpoint，不带主模型model字段；共享Key/FD/审批不改。独立产图服务不纳入模型ID替换。
