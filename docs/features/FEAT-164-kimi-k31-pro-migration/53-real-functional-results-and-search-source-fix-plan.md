# FEAT-164 S4Z：真实非文本结果与搜索来源最小修复方案

2026-10-27。Owner交回窗口后，沿原schema5及同一54e9618 App完成4次真实模型HTTP，全部HTTP200/response.completed：图片1、函数调用与回灌2、原生搜索1。没有重建账本或补额。真实日常库未访问；Runtime/core/patch未改，当前产品源码仍未因搜索问题修改。

## 已观察结果

- 图片任务01a178f8-3678-7c11-8c22-7b90cd44714a：真实input_image=1，准确回答蓝色/正方形，App completed，无工具/搜索。
- 工具任务01a178f9-7e95-7852-a7bd-073cf2f290e8：第一次response含1个function_call，第二请求含1个function_call_output；只读文件内容标记FEAT164_TOOL_ROUNDTRIP_OK_82C19原样返回，Native命令退出码0，App completed。没有写文件或联网。
- 搜索任务01a178fa-e800-7ab3-a292-e0c87f8020ec：原生web_search_call=1、供应商sources=20；Runtime保留20条且canonical摘要与计量器原返回一致，Host/Native/界面只有6条并显示partial。最终回答明确未能确认Responses能力，只引用旧视觉文档，**不把检索任务正确性标PASS**。
- 真实会话正常⌘Q exit0，四Runtime库WAL0/完整副本integrity ok；同构建重开及最终保留核验继续完成后追加记录。旧4次本机请求和真实调用分开，不能混算。

原三账本/前6行及14.188544元历史预占保留；累计模型HTTP10，新4/4已耗，禁止自动追加。普通usage按保留估算结算，搜索虽执行completed但独立费用未结，保留该请求完整14.188544元新预占，当前估算＋预占合计29.343192元（不是精确账单）。搜索账本status=unknown_reserved表示费用未结，不是模型执行unknown；原执行终态仍completed。后续真实调用不因旧计数重复索批，但本轮失败即停/四次范围及30元保守账保持，不擅自释放预占。

## 根因：显示筛选与供应商检索质量是两个问题

保留rollout中的20条来源为20个不同URL、类型全部url；两处原生记录完全一致，原始sources canonical摘要等于供应商流计量摘要。没有Runtime字段丢失、重复去重或数量截断。

Host `internal/session/native_process.go` 的safeNativeSourceURL把**整个URL一次解码后**交给共享不透明串检测；`v5OpaqueTokenPattern`允许字母、数字、下划线、加号、斜杠、等号和短横线的32位连续串。URL多个普通路径段通过斜杠连在一起，误匹配为凭据。逐条重算完整解释14个丢失项，保留6条与Native事实及界面逐字一致。官方`https://platform.kimi.ai/docs/guide/use-kimi-vision-model`也因此被隐藏。全局规则本为命令输出保守保护，不适合直接识别结构化URL；不得为了来源完整而删除全局规则。

供应商此次检索未返回当前`platform.kimi.com/docs/api/responses`，而返回旧guide/模型资料，故模型给出不确定回答。Host显示过滤发生在供应商完成推理之后，**不能解释模型回答不确定**；修显示不会把该答案变为正确。真实图片本身已经证明当前Responses路径可接受图片；当前官方文档也已核验，原搜索回答仅作为质量未完成样例保留。

## 建议的限定方案（方案提出时待确认，随后已批准）

推荐只修Host结构化来源URL判断；不改Runtime/core/patch、模型调用、原生工具、HTTP权限、旧库或旧事实。

1. 保留HTTP(S)、无userinfo、合法host、长度/控制字符、secret名称/Bearer/JWT/AWS/PEM等现有拒绝规则及partial语义；全局命令/工具输出脱敏函数及正则完全不动。
2. 只将**来源URL的不透明串检测范围**从整个URL改为URI组件：host、逐个原始path segment解码后的值、逐个query key/value和fragment。先按原始结构分段再解码，编码后的分隔符仍留在原组件内接受检测；不拆分不透明组件内部的短横线或编码内容，不添加信任域白名单，不绕过凭据检测。
3. 正常公开长路径可显示；任何单个不透明长组件仍保守隐藏并标partial。当前20条来源的只读算法预演为18条保留、2条仍触发独立长组件检测；不承诺20条全显，不伪造完整metadata。原始Runtime20条仍全留存。
4. 已有持久化事实不重写，不清除partial记录；新Host对后续原生通知和正常thread/read应用同一投影。历史重开是否经原snapshot更新按既有产品流程验证，不为了显示修复直接改SQL。

实施文件范围：Contracts `docs/native-search-sources-v4.md`及新增普通URL样例（源语义先行）；Host `internal/session/native_process.go`、对应test、SECURITY说明；必要的Host/Desktop原生来源与构建来源锁由已有canonical生成器同步，及FEAT164只读generation入口固定新commit。无新依赖/schema字段/数据库版本/UI能力。若现有同步工具不能精确绑定语义说明，先收敛其最小来源清单变化，不手写派生锁。

增量contract-impact=semantic：新producer会保留此前误删的合法来源，旧consumer已支持相同sources结构；所有旧字段、限制和降级路径保持。Contracts说明/普通fixture先本地固定，Host固定新来源后实现、定向纯映射/降级/生成/兼容检查，再Desktop固定Host来源并安全离线验收。公开source只作不可变本地来源，不推送/发布。

验证只使用这次真实返回的普通公开URL、普通缺省/重复/长度边界和既有非攻击控制；不构造恶意资源/攻击载荷、不注入运行时故障、不强杀。验证URL组件判断与原保护条件、32来源上限、旧v7/v8/v10降级、Native reader及同构建正常重开。**本修复阶段新增真实模型HTTP为0**，保留当前所有真实证据、账本、预占和App产物。

本次需要针对该范围确认，因为改变的是秘密识别/脱敏规则的结构化适用边界；元仓AGENTS“必须先确认的决策”包含“认证、租户、RBAC、审批、审计、数据保留和秘密管理”，且public wire语义仍遵循Contract First。它不是Runtime核心审批，也不是重新申请模型预算。当前只落盘审计和具体方案，尚未修改该保护规则。


## 后续确认与真实会话重开结果（2026-10-27）

Owner已明确答复“批准最小修复及离线验证”，授权记录见evidence/s4aa-owner-authorization.json。仅新增Host来源URL组件范围修复、必要Contract First下游及安全离线验证；本修复阶段新增真实调用为0，不访问日常库、不改Runtime核心或补丁。

本报告提出前的同一54e9618 App已完成第二次正常启动，图片、工具回灌、搜索三任务历史均可见且completed。重开期间计量账本逐字未变，没有新增调用。随后正常⌘Q exit0、计量器control/stop 204并exit0；两次完整停止副本的四Runtime库WAL均0、integrity均ok。原handoff等待状态仅为历史，当前无窗口交接待答，禁止按原handoff余4次重新执行。

搜索回答正确性仍INCONCLUSIVE；显示修复不改变该结论。后续修复来源和离线验证结果见第54号报告，旧真实证据与预占保持原样。
