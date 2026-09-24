# FEAT-155 普通客户端日常接入修复

2026-09-25。Owner明确授权“普通客户端启动定时任务功能正常可以使用，接通日常入口”。该授权覆盖原日常SQL15→26及Host Store5→6的已有兼容迁移。仍为local/demo_fast，不是生产发行；防自动空闲睡眠、睡眠后停止发送仍OWNER_EXCLUDED，系统通知延期。

## 根因与最小改动

普通launcher只启用了旧SQL15 writer/Store5和保留的FEAT136 Runtime，因此管理capabilities真实返回storage_disabled。旧FEAT155 candidate虽然通过验收，却会切换独立数据根并禁用图片，不能直接作为日常修复。

新增native-only daily selection，canonical dev/packaged入口默认启用，继续原`demo-fast-v1`、Host Home、Runtime Home和SQLCipher密钥，复用SQL16～26/Store6及唯一worker/Coordinator/outbox。明确isolated candidate与daily互斥；raw/显式禁用不取得新执行资格。没有新schema、DTO、调度服务或第二个Runtime。

固定input-only Runtime不变（`fb79b1d53501ec90084b584af5fdbe221c7a25aa`，binary SHA256 `bd7d26205e2d735dcac0f35fc089a7b30a5c18a54586b94a2c7f624f2f5b7672`）；Contracts不变（`54be9314dce5319b049dc0a236800fd1a1fdd7a1`）。Host仅解除“普通图片协商必然不具备草案资格”的过宽排斥：普通线程仍注册图片工具，草案start/resume不注册，每轮仍取得真实native input-only/空工具/无继承回执。Fake与retired approval仍拒绝。

首页和普通聊天页的“通过当前输入创建定时任务”已移除；管理页“通过对话创建”、专用草案模式、普通目录/附件/权限与原工作流配置保留。

日常库实际运行还发现3条旧v1明确failed操作保留queued projection，及2条已耗尽重试的清理记录，全局占用查询误认为它们仍在运行。修复只排除精确turn payload匹配的failed操作、无native绑定、无同轮非failed操作且submission仍queued/null的历史；submitted、uncertain、streaming、stopping、pending/inflight继续阻挡。清理仅在retry_limit_exceeded且lease=0时不占全局通道。旧历史、原目标索引和删除保护保持，不伪造终态，不重发旧请求，不删除清理证据。

## 契约与版本

`contract-impact=semantic`，权威源为私有启动选择、既有migration和调度占用实现。既有共享payload、IPC、Runtime projection未变，公共契约增版/生成变更N/A。受影响消费者为Host/Desktop，Owner为用户本人，本轮授权是日常启用决策；没有独立人工Reviewer。

Host已固定到`1d62b19`；Desktop同时更新scheduled Host全构建输入锁与原权限Host锁，均从真实Git对象生成，不放松dirty/source校验。旧Runtime产物未覆盖。回退应正常暂停/退出，保留SQL26/Store6兼容reader及原数据根，禁止降级数据库；保留旧Runtime不具备草案资格。

## 数据和验证事实

升级前正常Cmd+Q退出，使用SQLCipher/Bolt只读检查器记录表/索引计数和SHA256，无密钥或用户文本进入证据。第一次升级后再次正常退出比较：

- SQL15→26，除migration表新增11条外，36张旧业务表在原列上的计数与内容摘要全部一致，包括15聊天、7项目、21轮次、39消息、34 outbox、10 native bindings、84 native facts。
- Host5→6，15条session保留，task/thread/turn-operation索引摘要全部相同。Store6增加ordinary purpose，打开旧聊天可刷新运行元数据；原始session bytes摘要发生变化，未宣称逐字节相同。
- 升级前后使用同一日常目录，未复制验收库覆盖用户库。普通页面能读取旧项目/聊天，首页红框按钮消失，定时任务页两个创建按钮正常。
- 固定Runtime原生共存测试：4次有界localhost文本请求，普通图片工具声明保留、草案无工具，正常重开后两类线程resume通过；图片工具实际调用0。

最终UI闭环、定向检查及最后客户端配置见本报告后续完成记录。首次UI手动运行明确返回reservation_busy，未创建run/扣额；已定位上述真实日常历史兼容问题，没有跳过检查或改用户记录解锁。

追加的原生复测发现预约与发送前存在两次占用检查，已共用同源条件，回归覆盖预约后真正发送资格。另一个由正常退出复测暴露的边界：从未发送的首次专属create取消后留下本地占位，不能当成已绑定Runtime聊天继续enqueue。现在仅在同scope/计划、never_sent_cancel+退款、create/turn均never、create计数0、无Host/Runtime绑定且无其它关联运行的情况下，新确认可建立新会话/新操作；同一组合事务重验并更新当前专属关联，旧历史和旧操作均保留，不将未知执行重试。

## 完成记录

- Host固定：`1d62b198d2430be985d2a1164647b7163edfcd92`；Desktop固定：`cb78880058a883c9a0b3b3a522de689d72ae5de4`。Runtime/Contracts保持上述固定版本，未改二进制。
- 最终原生回归 **135 PASS**；Clippy all-targets零warning、前端lint/类型、4文件22项定向UI/launcher测试、native/typed IPC源校验、Host lint及app/session FEAT155 race回归、元仓lint/test通过。
- 定向新fixture最初两次因测试记录未满足public-task error字段约束失败，已修正为有效声明记录；完整135项为最终通过依据，原输出保留。工作流旧静态测试仍期待曾经的条件强杀逻辑，更新断言以匹配HEAD已有的全面正常退出行为，未新增强杀路径。
- 实际普通原生UI完成“管理入口→受限对话草案→审阅保存暂停→正常重开→单次确认→原Coordinator投递→原生终态→时间耗时→对应对话/轮次定位”，应用内重要更新出现。完成run为`01a0d47c-f6d8-79b0-b1ec-3dd4db429bea`，原生时间`2026-09-25 01:35:54 Asia/Shanghai`，耗时`0.021秒`。UI本机文本2次（草案1、执行1），与Host原生共存测试本机文本4次分开记账。**真实模型0，图片0，商家0，外部MCP0**；付费累计仍13/14，剩余1。
- 正常退出后已预约但从未发送的旧run被取消并退款；旧create保留attempts0且不能出站，新run独立完成，预约释放。验证计划仍暂停，没有新增自动授权。没有手工改日常SQL解锁，也没有删除失败历史或清理记录。
- 此轮自动触发、三目标、重跑等采用既有组合回归覆盖，未再次发真实Provider请求；这次本机fixture不能表述为新的真实模型验收。旧聊天仍有历史内容完整性提示，与52记录的既有3项ChatPage展示断言失败一致，本修复不改聊天投影语义。
- 全量`pnpm generate:check`仍在既有Skills源码HEAD与固定10c45…不符处停止；与本修复无关，未为通过门禁改Skills pin。已单独执行本次涉及的全部native/typed IPC源校验。不是全量CI全部通过的声明。

详细日志、只读摘要与原生观察见[evidence/daily-entry-activation](evidence/daily-entry-activation/)。最终交付客户端恢复原日常Provider与原工作流配置，不保留本机文本fixture作为用户默认服务；正常重开后的最终观察和远端提交回执随后登记。

最终正常重开已确认：真实受管配置恢复`MiniMax-M3 / https://api.minimaxi.com/v1`（仅读取非秘密模型/地址字段），本机fixture已正常关闭。原工作流入口保留，验证时切到Ask的普通新任务偏好已恢复为原“帮我批准”；定时执行自身仍固定Ask。记录页重新读到同一已完成run、真实时间/耗时和旧取消记录，验证计划保持暂停，客户端留在可用页面。原日常两条耗尽清理记录摘要未改变。

Host→Desktop已按既有明确Git授权依次提交并推送，各自远端分支`chore/retirement-baseline-20260905`与本地完整HEAD一致、工作区clean。元仓本报告及证据随本次收尾提交推送；Runtime/Contracts本轮无修改。feature.yaml v3 claims审计通过。
