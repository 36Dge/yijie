# FEAT-134 调整交付记录

## 2026-09-09 — 用户确认并授权原生展示收敛

用户确认八项 AC，要求复用 FEAT-132 原生机制、删除无调用残留并修复展示信息折损。五个相关主仓开始时均干净，分支为 chore/retirement-baseline-20260905；准确 SHA 与来源见 03-native-display-adjustment.md。

实现保持 native v7 / NativeDisplayBuffer / thread/read / SQLCipher；展示分开 summary/content，保留 Item availability，诊断按会话显示且只用安全文案；活跃 UI 由有效原生视图事件的订阅观察驱动，加载历史不能开启 busy。

Host 修订三项旧测试，确认投影问题不制造 finalized 或失败终态；删除无调用常量与辅助函数。Desktop 删除无调用 publish_feat134/publish_feat136 及专属辅助代码，保留历史类型和读取。

Desktop CI 已确认旧来源及嵌套检出布局不满足 native 脚本；做最小配置修复：真实兄弟目录、不可变来源、完整 Git 对象与冻结 Contracts 依赖，原检查不删减。

当前正在执行定向验证与实施后独立自审，尚未标记新 D4 PASS。付费请求为 0。Host 全构建输入受来源门禁保护，必须形成真实提交并更新消费者 pin 才能继续 canonical；未绕过或借用旧推送授权。

## 历史

原 2026-08-28/29 的实现、授权、失败、修复及 D4 记录完整保留于 [历史交付记录](history/2026-08-29/01-delivery-log.md)。不改变历史调用次数、不转移历史授权、不将原源码的测试结果视为当前结果。

提交前核验完成后已向用户提交本次本地提交授权请求；范围为已审阅的C/H/D/元仓修改及必要pin/修复提交，不含push/tag/部署/模型调用。等待回复期间未执行提交或canonical启动。D4门禁已实际运行并因尚未完成AC-007/008和真实入口验证而正确失败。


## 2026-09-09 — 来源固定和 canonical 收尾

用户明确要求继续执行剩余步骤，作为对前述本地提交、必要修复及pin更新范围的授权，不含push、模型调用或权限扩大。Contracts提交db7a607c1c091fc4f4243829d68d5b673eb7e2c3；Host提交f4cf01bd6f7e9f37792ef743d44f0ce10527c10b；Desktop提交6e5047d1c23041c46dd495ddb89e24c7e4db5d47，消费者和CI固定真实Host提交，42个来源条目及generate:check通过。

普通pnpm tauri:demo-fast:app标准构建和启动通过，使用原com.yijie.ai app-data与原.local/demo-fast Host/Codex Home。旧等待历史正确显示当前执行状态未确认；旧附件过期/清理未完成保持可读及输入保护；原生图片历史、未分类消息和Artifact预览正常；切换到正常映射会话后权限入口恢复，三选项可见且仍为请求批准。200%与键盘检查后恢复100%，两次Cmd+Q正常退出，中间再次从相同canonical入口正常构建重启。

所有8条原Host映射、最后Turn/native terminal及schema前后一致，均无活跃Turn，最终相关进程和18081监听已退出。没有新增模型请求、重试删除、重建附件或猜测接管。AC-007/008已取得实际既有数据验证，本次local D4闭环；正向summary/raw分层与不同Item结束状态由定向合成测试证明，不冒充新真实模型Turn。
