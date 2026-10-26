# FEAT-164 S4AB：旧v3测试已修复，搜索答案质量由Owner移出范围

2026-10-27。**旧v3测试基线失败已修复并验证；“搜索答案正确性”按Owner最新明确指令从FEAT-164需求和验收门槛移除，记OWNER_EXCLUDED，不计PASS、不延期。** 本轮三次已授权真实请求的结果原样保留，不再为该质量项目补试、增加检索工具或修改Runtime。

排除的是搜索答案语义正确性，以及本轮指定官方文档是否命中、能否回答图片支持问题的质量判定。原AC-008/009中的实际sources传递、协议事实、共享Key/审批/预算，以及历史和正常清理要求保留。整项仍active；此排除不自动晋升所有Gate。确认见evidence/s4ab-owner-scope-exclusion.json。

## 测试根因与已完成修复

当前NativeConversationViewEvent权威是v4，generator另有独立Rust v1/v2/v3历史reader。旧测试手写未受生成类型约束的v3 IPC并期待当前validator接受，把当前v4当未知版本拒绝，还把仍支持的持久格式3称为unsupported。这是当前IPC与历史存储版本混淆。statusSource在当前schema是optional，缺省不是失败原因；54号RCA的附带描述在此纠正，旧证据不覆盖。

仅改Desktop src/domain/conversation-native-view.test.ts：以生成NativeConversationViewEvent类型的satisfies约束v4正例，显式拒绝旧v3 IPC与未来v5；unsupported持久格式示例改为5。实际v3兼容由现有Rust reader独立验证；没有放宽validator或改schema、生成物、产品实现。

本地提交`ea8763dfc40466e9b808a1b39afad71dbff1ac56`，位于feat164-s4ab-qualification-20261027/yijie-desktop。增量contract-impact=none；生产源码/生成物/依赖与父c98eddf逐字一致。28前端（8 Native view＋20搜索展示）、2当前client边界、1 Rust v3/v4读取、19来源检查、native-process不可变检查及pnpm lint通过。client按名称选2项，另23项未选，不能计PASS；Rust1项0ignored。全仓套件不因此宣称通过。

## 三次搜索调查的实际结果

实际App始终为S4AA c98eddf/Host4f966e8/Runtime11fd-r5，App SHA179dbd187220694d4666af5822466572f3b245a911501991cb0194f4308db195、119文件，原包和回执未覆盖。新Desktop只改测试，未冒称重建了产品App。

| 请求 | 唯一变化和实际结果 | 当时调查判定 |
|---|---|---|
| 累计11 | 提供当前官方URL；验收relay只保留web_search声明。HTTP200/completed，仅reasoning，无搜索/最终文本 | 未完成搜索题 |
| 累计12 | 同profile，改为明确site站内查询。HTTP200/completed，仍无搜索/最终文本 | 改查询词未解决 |
| 累计13 | 保持第12题不变，撤销search-only覆盖，恢复产品原始工具声明；增加不含正文的输出类型诊断。HTTP200/completed，reasoning＋message，答案无法确认，仍无搜索 | 返回文本，但未完成核验 |

前三次都没有函数调用/图片输入；三轮任务分别01a17933-3770-7ee3-b259-b90bcf1675f5、01a17938-9f75-7020-bc6f-0a92ed0f1a18、01a17940-9876-7470-bf4a-ea0ebb6773c6。前三轮结果不因Owner排除而改写为成功答案。第三次恢复文本与工具覆盖差异有相关性，但单次对照不足以证明供应商内部因果；前两次受限工具profile不能代表原始产品请求。

排查排除了本地丢失最终答案：第一轮原始rollout无assistant message；第三轮供应商流done和terminal均只有reasoning/message，无web_search_call，Native持久视图与UI一致；原生搜索声明在三次出站均为1，不能把模型“没有工具”的自述当配置权威。Host来源过滤位于答案生成之后，不会改变模型收到的服务端搜索上下文。

[官方Responses完整参数定义](https://platform.kimi.com/docs/api/responses)表明该搜索由服务端按输入自动决定执行，tool_choice仅auto；external_web_access/indexed_web_access被忽略，不能靠切换live强制检索。filters.allowed_domains受支持，但不会改变自动判断语义；未进行第四次请求。官方文档直接说明文本/图片输入，前序真实图片也已通过，但这不等于搜索答案通过。供应商内部查询改写、索引/排序和为何未触发仍缺遥测，不作确定归因。私有下载快照SHA e642a214977c62a023ef421c6bacc0766ac1cbc5e360a61d6665b5e7dd1f14ac；不将完整网页正文提交仓库。

调查到此因Owner范围变更结束。没有新增独立search_pro/fetch接口、没有扩张动态工具准入或把密钥传给工具进程，也没有为此修改Runtime核心/补丁。此前“继续修复搜索答案/再做真实复验”的计划已取消作为FEAT164交付项。

## 授权、计量与保护

Owner先批准累计45元/新增1次，随后增为2次、最后允许第3次；每次均在前次结果审计后独立准入，无自动网络重试。schema6工具提交d4050044d2c6a77ab3ba00907b650126dc5db0f8，45项控制通过；schema7工具提交92ef0411a6e98f36886f2b7a2017e40fe2d21340，49项控制通过。二者在独立工具工作树，非产品代码。旧schema1—5行为保持，schema6每轮halt/复审后才能第二次，schema7独立继承前12行，只允许一笔，不允许第四次。

本轮新增真实3、累计13；本轮按历史保守单价估算0.397107元，总估算加保留预占29.740299元，未超过45元，不冒称精确账单。原四账本逐字不变；schema6保留原10行，schema7逐字继承前12行。第1与第10笔的两份14.188544元unknown预占均未释放；新增三笔均有usage且无搜索费用事实，依既有规则结算。最新账本g2v-real-budget-ledger-search-third.json已halted/stopped_normally，3次授权已消耗，不复用余额擅自续发。

三次App均正常⌘Q exit0；三次完整停止副本四Runtime库WAL均0/integrity ok，71表全部旧行hash保持，仅新任务/事实/正常停止代际追加。最后一轮后额外UI重开因范围变更未执行，不写成PASS；实际持久视图已在完整副本只读验证。meter正常control/stop204/exit0，无待答交接或活动服务。

原497dirty、6498份活动隔离库外保护文件、119份S4AA包内文件保持，混合memory只精确提交本轮段落；FEAT163不混入。工具导入产生的旧__pycache__仅为新增审计缓存，保留且未提交；旧tracked源码未改。一次测试命令目录错误在发现测试前停止，修正后通过；失败原因保留。无强杀/攻击/权限破坏/替身程序/手工checkpoint/WAL清理，日常库未打开或迁移。

## 剩余执行方向

不再把搜索答案正确性作为S4或整项阻塞。继续按原整项目标收口仍在范围内的来源绑定、模型切换/历史/授权及核心业务状态最终判定，再做当前来源的日常候选prepare-only和具体切换清单。日常数据执行仍须对应批准；新增Runtime核心/补丁仍先方案。已移除的亮暗/键盘/最小窗口与本次搜索答案质量均不恢复为门槛。

原始审计目录feat164-s4ab-audit-20261027保留完整私有副本及原始日志；脱敏证据见evidence/s4ab-audit-index.json。所有提交仅本地，无push/tag/release。
