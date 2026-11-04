# 最终实现：9个模块

本地工程实现完成。复用固定 yijie-codex，不新增 Runtime patch、planner、重试器、预算机制或任务重放。原兼容读取、SQL43/per-turn profile、双通道方案由用户后续决定撤销。

| 模块 | 实际落点 | 最终职责 |
|---|---|---|
| M1 原生执行能力 | yijie-codex，现有 execution-progress-v1 | 原生 Item/Turn、公开消息、命令动作、重试意图；版本不变 |
| M2 契约与生成 | yijie-contracts/openapi/native-conversation-v6；generate/sync-native-process | Native6/SSE13，动作/工具元数据/nullable retry；固定 dfd9012954c716d360f702d6be3bdbdef75e0633 |
| M3 Host 投影与指令 | internal/session/native_trace.go、native_conversation.go；internal/app/native_conversation.go；internal/codex/runtime_permissions.go | 安全最小化投影、当前路由、真实阶段沟通要求；旧 Native 路由退役 |
| M4 Native传输与归并 | host_bridge.rs、host_domain.rs、native_conversation.rs | 只接Native6/SSE13，按ID归并；原生状态及通知保留 |
| M5 Native历史与IPC | native_conversation_storage.rs、schedules/drafts.rs、ipc.rs、lib.rs及schema/生成物 | 只写读format6，事务后发布IPC6；定时草案消费6；旧IPC/archive退役 |
| M6 前端接入与事实视图 | chat-client.ts、chat.store.ts、conversation-view.ts、conversation-timeline.ts及validator | 消费history6和chat:native-view:v6，建立只读事实视图，不另建执行状态机 |
| M7 纯阅读索引 | conversation-activity-presentation.ts、conversation-activity-summary.ts | 公开消息分段、连续调用组、调用/命令动作/来源分别计数；不改事实 |
| M8 组件 | ChatTurnGroup、ChatActivityGroup、ChatActivityRow、ChatTraceNotices | 轻量概要与有界明细；复用命令、网页、工具、安全正文；异常/审批保持可见 |
| M9 阅读与设计 | chat-trace-presentation.store.ts、ChatTimeline、tokens/设计文档 | 只在内存保存展开选择，复用既有帧合并/滚动；组内采用短滚动条要求的网格布局 |

## 当前模型省略 phase

真实 Kimi/MiniMax 样例均没有返回 phase。保持原值，不把未知阶段写成 commentary/final_answer。复用既有 observedProgressMessages：只有后续真实活动已被观察到，中间消息才可进入普通过程；最后一条可读回答始终保留，结构化草案不套用该判断。该规则只改变阅读，不创建模型消息、执行事件或持久字段。

## 安全和状态

命令动作只取 Runtime canonical commandActions，最多64项、原始索引不变，不解析shell重新猜动作。父Item仍是一笔调用。路径、查询、标题按既有安全规则脱敏及限长。来源数是检索结果中的去重URL数，不等于已阅读或被答案引用的来源数。

错误/警告不完成Turn；willRetry缺失/null为未知，不是false。公开中文提示使用已有diagnostic白名单，原始代码不进入主阅读区。计划终态仍保留未完成步骤，不自动勾选。阅读、展开、复制不会派发或重放任务。

新格式上线前清理了已获授权的旧会话存储；凭据、配置、资源与工作空间文件保留。普通业务、Artifact和权限协议不属于本次旧 Native V4/SSE11退役范围。
