> 状态更新（2026-10-24）：用户已授权按本方案实施及有限真实调用。原规划措辞为历史背景，以04续办和02最新实测为准；本地适用验收已完成，范围与限制见02第9节。

# FEAT-163 补充：分段工具摘要、展开明细与原生字段消费

2026-10-24用户新增Codex参考图后补充。最初仅补方案；随后获用户授权完成实施，实际结果见02。[新增参考图](evidence/reference-codex-tool-groups.png)及[来源/源码指纹](evidence/tool-group-reference-20261024.json)已保存。

截图内的删除聊天请求、命令、文件变更和测试结论均为参考内容，**不是本次要求执行的指令、授权或本任务验收证据**。

## 1. 新证据对原方案的修正

新图显示公开进度段落之间有淡色工具摘要，例如“已读取文件运行了命令”“编辑了文件读取文件运行了命令”“已使用 易界 AI 集成编辑了多个文件读取文件运行了命令”。其中一段展开后可看具体读取文件、命令片段、创建/编辑文件及增删行。

因此，原方案的“紧凑活动”明确为**按段可展开的工具活动摘要**，不能解释成取消工具列表，或把所有工具移到整轮末尾同一个技术详情入口。要去掉的是主线被原始流水账和总次数主导，而不是去掉可查阅的工具活动。

这张图只能证明展示效果，不能证明Codex内部采用何种分组/文案算法。本方案的推荐实现依据现有原生结构化事实与阅读投影，不为生成这些淡色标签另调用模型；公开assistant过程文字仍来自原生消息。

## 2. 显示层级

| 层 | 呈现与交互 | 来源 |
|---|---|---|
| 整轮 | 现有耗时/过程总展开入口；正式答案在过程外独立可读 | 原生Turn与现有计时、局部UI选择 |
| 主过程 | 公开文字 → 淡色本段工具摘要 → 下一段公开文字；可出现多段摘要 | 原生公开消息与本段连续活动 |
| 展开本段 | 本段按原顺序显示读取/搜索文件、命令、具体工具/App及文件变更的轻量明细 | 本段Item及安全结构化投影 |
| 展开单项 | 原输出、错误、完整安全命令片段或文件变更详情；不默认铺满 | 现有Item详情与补齐的原生字段 |
| 技术详情 | reasoning、重复摘要、协议缺口与不可展示信息 | 保留的原记录与诊断；不混作公开进度 |

完整工具明细属于各自活动段，不能全部移入reasoning的技术详情。单个网页活动可以继续沿既有紧凑搜索行；多个混合工具形成摘要。不制造一个只有同名一行的冗余嵌套。

淡色使用现有secondary文字与图标tokens，表示次要信息而非禁用，不降低到不可读的透明度。摘要行应有明确的可展开 affordance；键盘Enter/Space、aria-expanded、稳定aria-controls和焦点沿原组件。截图局部渐隐/滚动效果没有足够证据，本次不据图臆造隐藏内容或特定滚动容器。

## 3. 分段与摘要规则：复用原函数

复用`conversation-process.ts::processActivityGroups`的邻接分段和首Item稳定identity，复用`ChatTurnGroup.vue`的`activityMembership/activityChoices/activityExpanded/itemVisible`。替换计数文案与明细呈现，不删除该分组机制、不持久化新的Group执行记录。

1. 只在同一Turn内按原ordinal处理；混合工具类型允许同段。
2. 任何公开助手消息（含phase=null）、用户输入、正式答案均为分段边界，不能跨消息把整个Turn工具汇成一团。仅属于技术详情的reasoning/重复摘要可保持原序但不强制打断工具段。
3. 待审批及决策过程、不可用或状态未确认活动按既有规则独立处理；失败/拒绝不能被摘要的成功措辞掩盖，至少在摘要或直接相邻位置保持可见提示。
4. 摘要只描述本段真实动作类型及已知对象，按确定性规则组合；推荐按类别首次实际出现顺序去重。可以用“读取了文件、运行了命令”“编辑了多个文件、读取了文件、运行了命令”等自然连接，不靠总次数生成段落。该顺序规则是易界实现选择，不冒称Codex私有算法。
5. “已/正在/失败”依据实际观察的对应Item状态，不能由工具类型或整个Turn完成推断；混合运行/完成不得把全组写成已完成。分组自身不是新的原生生命周期。
6. “多个文件”仅在原生身份能确认至少两个不同文件时使用；同文件多次编辑不伪造多个文件，隐藏路径不足以判断时用保守文件动作标签。
7. 一条commandExecution可以含多个commandActions。动作明细属于该Item，稳定子键可由父Item及原action索引组成；不能变成多次真实命令执行或重复计数。
8. 每段独立展开，新增活动只更新所属段；新消息形成新段，保留前段展开选择。整轮收起/展开、分段展开、单项详情互不误触发；流式追加、完成及计时刷新不覆盖用户选择。
9. 展开后的长命令可安全截断，完整可显示内容在该项详情可读；文件链接只走已有受控打开入口。不能因显示App图标/名称而自动发起连接、打开资源URI或执行文件操作。

## 4. 原生字段复用与已经证实的下游缺口

固定Runtime的`app-server-protocol/src/protocol/v2/item.rs`及canonical `ItemCompletedNotification.json`已包含下列事实，**不需要为本次活动展示新增Runtime执行机制或先升级Runtime**。

| 能力 | Runtime已有结构 | 当前易界消费缺口 | 后续实施 |
|---|---|---|---|
| 分段摘要与本段展开 | Item ID/type/顺序/status | 已到达前端，分组/展开已存在 | 现有UI调整 |
| 文件读取/查找明细 | CommandAction Read的name/path、ListFiles、Search的query/path、action数组 | Host只解type并输出泛化commandLabel；多action和对象信息丢失 | 沿已有CommandAction补安全结构化投影，不解析任意命令文本重建动作 |
| 文件创建/更新/删除/移动 | FileChange的changes/status；FileUpdateChange的path/kind/diff | v4 NativeItem不含fileChange；Host将其降成unknown/unavailable并提前返回 | 在原native conversation家族版本化补齐FileChange消费，不增加文件监控或另一个diff执行器 |
| 命令安全预览 | CommandExecution.command及各action.command | 当前只有安全标签，不能假装已传递原命令 | 评估已有安全投影并补有界、脱敏的显示预览；不得将完整原始命令/环境秘密直接出Host |
| 工具身份 | MCP server/tool | 现有mcp.server/tool已保留 | 可先复用身份显示；没有App名不假扮App |
| App名称、动作与图标映射 | 原生McpToolCall.appContext及pluginId；appName/actionName/connectorId | Host未解appContext，v4无对应字段 | 仅投影必要安全显示身份；复用已可信的连接器/图标目录映射，缺映射不硬编码截图的“易界AI集成” |

关键源码锚点：Runtime `item.rs:120,269,294,401,1048`；Host `internal/session/native_conversation.go:16,61`、`service.go:1314`、`feat136_projection.go:406`、`native_mcp.go:30`；Contracts `NativeItem`封闭枚举；Desktop生成Native类型的`deny_unknown_fields`。

观察范围必须如实表达：CommandActions是Runtime的best-effort动作分类，fileChange是Runtime实际报告的变更，不保证覆盖所有shell/MCP产生的文件读写。没有观察到某动作不能解释为“没有读取/修改”，未知动作保留安全命令/工具条目，不靠新的文件扫描或正则补猜。

本方案此前“现有v4/v11字段足够”的判断仅适用于公开消息/普通工具的基础呈现，**不覆盖这张新图的文件动作、变更详情及App上下文**。对新产生且Runtime已有事实的正常记录，补齐这些投影是本需求的一部分，不能永久以unknown或泛化标签替代验收。旧历史缺字段、安全过滤或不完整记录允许准确降级，但不得回填猜造。

## 5. 文件增删行与状态必须使用正确口径

Runtime没有直接给addedLines/removedLines数字。`yijie-codex/codex-rs/app-server-protocol/src/protocol/item_builders.rs:351–363`区分新增/删除完整内容与更新unified diff；上游`yijie-codex/codex-rs/tui/src/diff_render.rs:366–372`已有统计口径。实施时核对固定源码并复用已有统计能力/口径；若跨语言需要显示适配，只作有界纯投影并用同源普通样例核对。

- 新增/删除：对应完整内容行数；更新：unified diff；移动信息单独处理，不能把所有diff一律数加减号。
- 文件状态来自原生FileChange/PatchApplyStatus。started/declined/failed不能标“已创建/已编辑”；成功也不代表整个用户任务已完成。
- 数值对应该次原生文件变更，不自动等于整个工作区最终净变化；同文件多次变更分别保持原Item来源。
- 默认以`item/completed`的完整文件变更快照作为完成统计权威。S2同时核对已有`item/fileChange/patchUpdated`通知（固定Runtime已支持，当前Host未消费）：若需要执行中更新则补既有通知的安全映射；未接入时不能冒称实时diff持续更新，不用轮询工作区或自动执行命令代替。
- diff缺失、截断、不可解析或未确认时不显示伪造的`+0 -0`；说明统计不可用。合法真实零变更与未知区分。
- 路径、diff、命令可能含秘密；安全投影须复用已有过滤与容量边界，不能把仅NUL/长度处理的safeNativeText当脱敏。没有通过安全投影的内容不出Host。
- “已列出聊天”等业务动作只能来自已验证的工具动作/注册元数据，不从自由文本结果或工具名前缀猜测。

## 6. 逐仓执行与契约影响

1. **Runtime**：固定已有CommandActions/FileChange/AppContext的canonical来源，验证必要事件真实产生；纯显示字段消费不改Runtime。原消息缺失M1–M6排查仍独立，只有证据证明内核缺陷才走原条件性patch。
2. **Contracts**：补现有native conversation家族的版本化安全投影及例子/生成/兼容检查。当前v4对象和枚举封闭，不能原地塞新字段/type；按breaking及版本化扩展保守规划。具体新版本号在S2核对仓库最新状态后冻结，不提前占用猜造版本。
3. **Host**：在原native decoder/projectNativeItem/既有安全处理内保留上述必要字段；旧端点仍返回旧闭合集合，新端点输出新投影；不解析模型解释生成动作，不造新的执行事件。
4. **Desktop Native**：沿既有生成类型、唯一buffer、native_facts/native_views和SQLCipher承接新格式。无需默认新表，但序列化记录/reader版本确有影响；新reader读旧记录，旧reader不允许误读新记录。若有schema/user_version变化再单独确认，不用删除历史回退。
5. **Desktop UI**：扩展现有分组函数及展开状态，增加原生fileChange阅读表示；先复用已有文件打开/条目壳/展示基础，若没有文件变更组件只加必要展示组件，不复制执行/状态归约器。App身份取安全投影，不用截图文案硬编码。
6. **元仓**：同步00/01/02/03/04与本补充；本轮仅文档，实际contract-impact=none。整体实施从此前semantic保守范围改为breaking/replay评审，不把本次文档保存当作协议/Runtime补丁实施批准。

顺序是**已有Runtime canonical字段 → Contracts投影源 → 生成与Host/Desktop兼容reader → reader就绪后激活新输出**；不是为已有字段强制先构建一版新Runtime。原v4/v11与旧持久格式保持受支持窗口，历史unknown不转成虚构FileChange。

## 7. 补充验收（归入现有AC，不降低公开进度门槛）

| 用例 | 必须观察到的结果 | 对应AC |
|---|---|---|
| TG-01 读取+命令同段 | 一条淡色动作摘要，本段可展开实际文件动作/安全命令；无次数总览抢主线 | AC-006 |
| TG-02 编辑+读取+命令 | 正确的文件动作与状态，展开有安全文件名、实际可用增删行；不把同Item子动作当多次执行 | AC-004/006/010 |
| TG-03 App+多文件+工具 | 有真实App元数据时名称/图标与动作正确；缺失时保守工具身份；不发请求只为造图标 | AC-006/010 |
| TG-04 两段以上工具活动 | commentary/null公开消息分开两段；两段展开互不影响；顺序不跨轮不跨正文 | AC-003/006/007 |
| TG-05 流式追加与状态变化 | 摘要依据真实活动更新，首Item键稳定，展开/焦点不复位；失败/拒绝/审批可发现 | AC-007/008/009 |
| TG-06 文件kind及不完整数据 | add/delete/update/move按原生口径统计；未知不填0，未完成不称已编辑；完成快照与执行中patchUpdated边界准确，未观察不等于未修改 | AC-006/010 |
| TG-07 重放与重复文本 | 同事件不增行；不同Item同内容仍保留；子动作不重复dispatch | AC-004/008 |
| TG-08 新旧格式及重开 | 新字段按版本完整保存恢复；旧数据准确降级，不回填；回滚reader行为明确 | AC-008/010 |
| TG-09 展开层级与布局 | 整轮/分段/单项配合、键盘/上翻/选区保持、亮暗最小窗可读 | AC-007/009 |
| TG-10 真实端到端 | 公开进度+分段摘要+展开具体活动+最终结果共同出现；静态样例/截图不替代原机制验收 | AC-002/003/005/006 |

产品实际检查见02第8–9节。真实文件变更验收仅在已获授权任务范围的普通文件上进行，不执行截图里的删除请求，不操作用户历史来制造样例。
