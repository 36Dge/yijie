# FEAT-164 技术设计候选

> 当前（2026-10-25，S4旧线程/子代理/自动压缩）：Host验证提交df06a3c仅新增测试、driver和说明，产品组合仍为Desktopa0a4743/Hostcac2d4d/Runtime074417e5。干净来源独立子集6项PASS、14次loopback，覆盖旧父子loaded后正常停机/显式切换、当前及迁移后自动压缩、previous_model两分支零旧出站。但旧模型子代理被guard拒绝后，wait_agent和thread/read仍报告completed，实际缺陷保持FAIL；S4 blocked，完整TCONF/G2V/G3/final不放行。全轮71次合成本机HTTP、真实新增0；旧账本/预占保留。最新权威见[30](30-s4-loaded-legacy-compaction.md)及feature.yaml；下方各批次保留原来源。

> 当前（2026-10-25，S4同源App/UI）：Desktopa0a4743在固定Hostcac2d4d/Runtime074417e5及专家资源上完成本机App验收子集；修复Worker物理路径、最小窗口裁切和暂停Kimi历史阻断启动。普通/专家媒体、历史重开、暂停与MiniMax、亮暗最小窗口及正常清理已验证。10次loopback、真实模型新增0；系统浅色已恢复，旧账本/预占和原工作区保留。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final仍pending。最新权威见[29](29-s4-canonical-app-ui.md)与feature.yaml；下方记录按原时间与来源保留。

> 当前（2026-10-25，S4专家/媒体/辅助续办）：专家pin已按Skills595c927不可变同内容来源修复；Hostcac2d4d、Desktop56f5284、Connectors1f15726已仅本地固化。四组合source、37专家版本安装/解析/重开及专家/媒体/原生辅助调用安全离线验证通过；S2/S3/S4当前源回归通过。完整TCONF-164-04、App/平台/G2V/G3/final仍未完成，真实模型新增0，旧账本/预占保留。最新见[28](28-s4-expert-media-auxiliary.md)及feature.yaml；下方段落保留各阶段历史范围。

当前S1活动身份、候选受管配置和执行准入已实现并本地固化，详见21。S2的Host持久操作/显式恢复已实现（22），Native恢复接线已在23实现；未发送取消、计划及全调用面仍待完成，不称完整产品可用。

> 2026-10-25 候选修正：实际 r1 出站包含官方 include 枚举未列出的 `reasoning.encrypted_content`；r2 将只对新 Kimi 省略该 opt-in，保留 max、搜索 sources、响应和历史处理。原预算适配器还须在去掉搜索时同步去掉依赖的 include。此修正仍按 Runtime 权威源先行和不可变下游 pin 执行；不是默认输出参数变更，也不证明首次 HTTP 400 的唯一原因。事实与限制见 [19](19-responses-400-audit.md)。

## 主链与身份

Contracts源 → Go/Rust/TS → Desktop/Native → Host模型路由与session → Runtime start/resume/turn → Moonshot Responses → 原生SSE/工具执行及结果回灌 → Host投影 → Native单一buffer/SQLCipher。

有效定义只有新Kimi及MiniMax；已知历史集合额外含旧K3。读取历史、终态回执与新执行拆开：HTTP header、schema、Host model availability、Native enum和相关market/experts包装全覆盖；若某旧consumer不能理解新值，来源/版本不匹配时拒绝混用。旧身份retired-known不等于实际选择unknown。

## 启动与截止点

S1已在候选同一管理边界增加受管前身资格与独立Kimi执行暂停，不新增旁路服务。兼容构建须默认不领取尚未分类的旧模型工作，同时保持历史查询和MiniMax能力。当前总模型开关会关闭读取路由，不可拿它冒充所需能力。

顺序：核验来源与兼容reader → 在任何coordinator/market/scheduled worker启动前禁止派发 → 前向schema迁移及旧身份分类 → 安装claim/send双重退役准入 → 查询/正常恢复 → 正常收敛或明确取消所有受管模型工作 → 验证无旧进程/工作在途 → 固定cutover → 允许新profile新请求。

停止新增派发必须覆盖标题collector/pending starts、草案、工具后续Responses、Guardian及启用的子代理。父thread idle不是全图idle。若已有App仍在旧版本运行，先使用正常退出流程；不能对运行中数据进行本任务迁移。无法安全停止则不继续。

title outbox只有session ID，不能仅凭没有旧profile字段就放行。未派发的旧标题保留fallback标题并停止自动生成；阅读历史不触发新标题请求。新标题在确认当前选择后可沿现有链请求新模型。

## 受管配置和候选

S1冻结Host5022435真实已知旧catalog/TOML字节；v1原文件保持不改，沿既有独立v2候选文件名写入。显式前身许可才接受完整旧v1对；v2只接受空空、新catalog+空、新新这三种可达组合。原authority preflight/原子写入与最终重验保持；未知漂移、半个v1对或只有v2 TOML均拒绝，完整双文件完成后才启动Runtime。trust和原Home保留；这不是数据库迁移许可。

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

## S2 Native已实施增量（23）

SQL39新增私有chat_model_operations_v2，保存v2原session/Host/thread/旧profile/目标/expected revision及prepared/dispatched/unknown/committed和原终态回执；不改0038或回填旧pending。兼容reader支持39，旧MAX38构建拒绝；默认v1兼容构建不派发39模型工作。候选入口仅允许0/38/39，不扩大到日常15/29/37库。

Native先持久化prepared，最后POST前重验scope/会话绑定/未决工作并保存dispatched；沿原SubmitTurn及生命周期permit/epoch，新增本地chat_recover_model_v2明确动作，不扩大权限或外部端点。普通refresh只有GET；仅prepared且Host无记录可首次提交原意图，dispatched/unknown且404不证明未发。新select不能自动reapply已存在未决操作。原回执经过source-generated校验保存，再读取current Selection，迟到回执不能回退revision或在同revision替换profile。旧无v2证明pending只读阻断。

该表只证明模型配置意图，不代替普通聊天、market、expert或计划的业务派发证据；其取消仍待下一步。

## S4实施补充（2026-10-25）

见[27](27-s4-call-surface-wiring.md)：market-selection/market-host/experts独立v2只扩已知模型身份，旧源及snapshot/digest版本不变；Native私有草案IPC v2此前已引用storage-v2，无需再造schema。候选全调用面显式选择且仍经过原权限/模型准入。Host标题收集器接受固定Runtime的正常userMessage通知，不将其作为标题正文；未知项/工具项继续失败。私有草案Config仅允许127.0.0.1显式端口/v1的本机资格路由，外部env-loader仍精确锁定18083/v1，受限policy、无工具及无重试保持。无新增权限、服务端或外部目标。
