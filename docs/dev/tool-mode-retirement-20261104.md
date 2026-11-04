# 工具模式设计撤回完成

2026-11-04，Owner 在实际界面明确要求完整撤回轻量模式，并再次强调移除所有相关
逻辑。已撤销此前的可选轻量方案；新建聊天直接使用原有完整能力，没有模式选择器。

已删除前端控件/标记、草稿偏好、Native/Host 模式状态与传参、原生 feature 关闭
投影、持续偏好写入、启用开关、对应功能测试和生成契约定义。未保留隐藏开关。
普通请求实际回环确认多代理、get_goal/create_goal/update_goal 均在原生工具面内；
原生预算控制仍有效。独立提示词精简（6161→4150 字符）与原生压缩保持。

最高 `contract-impact = breaking`：Owner 明确撤回未发布且仅本机消费的候选输入；
已知消费者配对回退。自动 breaking checker 未识别该行为变化，不能宣称旧模式
请求兼容；新的符合性测试明确拒绝 tool_profile 参数，普通 P1 请求保持有效。

前端先停止发送，再切换配对 Native/Host。用户通过客户端 ⌘Q 正常退出；退出后
保存 Native 数据库/WAL/SHM 与 Host 数据库的定点副本，不强杀、不删历史、不降库。
SQL 45 删除空的新增偏好表；历史迁移 44 的 checksum 保持。Host 私有包络 13
在正常前向迁移中退役旧偏好字段。历史迁移与退役步骤仅用于数据兼容，不具有
轻量模式的选择或执行能力。

固定入口已成功启动，Native 增量构建 31.22 秒。实际 Host build revision 为
d6f6bf5d596547e916e5b60e52e0f5776b2417e0，`/readyz` 返回 200 / runtime ready。
技能、专家和既有连接器启动就绪。实际 renderer 已无模式控件或传参引用。
Runtime 保持 55b4e51049d6f4fc0af4b35f12832357f5e4ea06，SHA-256 为
50d89e152c90e660331326506d372b986acd0279324376cb77385959698219d7。

只读后态确认 Native 44→45，旧偏好表不存在；3 个会话、12 条消息、6 内容块、
6 轮、111 原生事实、6 视图、3 模型选择及其它已核对表的原行摘要完全相同。
3 份 rollout 的原前缀保持，新增 task_started/token_count 均为 0。21 项原有 UI
文件逐字节保持，未混入本次回退提交。客户端保留打开，没有付费模型测试。

Contracts 安全生成、lint、符合性检查通过；Host 迁移、完整工具面/原生预算及技能
重放通过；Native 退役/重开/旧摘要保持、fmt、两种 profile 的 Clippy、前端 lint/
构建/文档构建通过。前端完整安全回归 2117 项通过，来源 pin 的旧断言同步后其
5 项独立复测通过，node:test 27 项通过。旧失败记录保留，不伪造首次全绿。
攻击 fixture、强杀、权限破坏等用例未执行；原有安全排除保持。HMR Native 窗口
无法被自动化识别，完整原生视觉验收未执行，以实际 renderer/source 和运行后态
核验撤回，不用浏览器模拟冒充原生 UI 验收。

最终本地来源：Contracts 64ed36dfb2c4df7645d969e0eaf1b3f3bb0a50c4；Host
d6f6bf5d596547e916e5b60e52e0f5776b2417e0；Connectors
5733c9c79ca3a65d290b1a56fedbc2fac81342fe；Desktop
e6a9522bf9a428fb8d56f36579c03e3fbd51dee1。没有推送或 tag。
证据目录：工作区 `.local/diagnostics/2026-11-04-light-mode-retirement/`，包括
`activation-verification.json`、前后数据摘要、冷副本和所有检查日志。
