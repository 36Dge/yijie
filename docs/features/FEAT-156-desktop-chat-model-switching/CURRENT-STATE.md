# FEAT-156 当前状态

2026-10-02（Asia/Shanghai）。**本地实现与真实验收已完成，10项Must PASS；当前结论见02-verification.md §8。** 最后治理校验结果写入evidence/d4-checks.json。此文件覆盖旧暂停点；PAUSED-STATE.md及交付日志的历史失败继续保留。

- 功能：发送/停止左侧两模型入口，新聊Kimi K3/exact max，旧MiniMax独立保留；同thread两向切换、原生附件/工具、受限草案和三目标计划贯通。日常canonical入口默认启用。
- 最小Runtime修复：0004 auto+0005严格恢复完整终态工具参数，权限/沙箱/input-only不变。独立chat-models-stream-args产物binary SHA-256 `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`；旧两组产物不变，复用原target缓存。
- 最终fresh真实请求31–44：双向上下文、两模型工具exit0/图片/草案、三目标计划、模型冲突拒投/重审、缺配置恢复、正常Stop、亮暗/1180×760/200%及正常重开均有证据。没有用旧独立成功覆盖MiniMax跨模型失败。
- 调用：累计授权50HTTP/4图片、单次8192；实际44HTTP/4图片，余6HTTP未用。synthetic17；标题/生图/外部MCP0。meter61350已正常停止（exit0），台账stopped_normally，禁止再用历史图片聊天做请求。
- 日常App：canonical `./scripts/run-local-demo-fast.sh --packaged`、原daily数据/18081/SQL29/Host7、launcher82834运行；无meter覆盖，readyz=ready。后续不要把该正常运行误当未关闭的验收代理。用户可直接使用；验收结束不再发送模型请求。
- 三个最终验收计划均off。MiniMax额外草案只审阅取消，没有保存新计划。永久删除仅执行此前已授权失败草案147a52f0；其它记录保留。
- 最后原生重开：MiniMax草案保持MiniMax，远山主聊保持Kimi及中断历史，默认新聊Kimi；系统浅色、缩放100%、原窗口恢复。
- 资格：Runtime4新/34全部SSE、真实固定Runtime本机6请求、Contracts确定生成/同步、Host模型与权限协议、Desktop7原生/27模型与计划/2页面、lint/fmt/clippy/build/generate/docs通过。完整命令和边界见02。
- 限制：ChatPage既有5项基线失败；FEAT155授权刷新会关闭未提交计划表单，基线逻辑未改；禁止的历史攻击/伪Runtime/破坏测试未运行；真实生图/MCP/标题未运行；未作全量CI或生产发布承诺。
- Owner先授权分仓提交，后明确授权当前目录所有仓库改动推送。四个产品仓已成功推送到各自origin的chore/retirement-baseline-20260905；Desktop原20份界面改动单独提交为b133af65ac5d572b88c4a4f4cbbb30a04c1dc166，全部纳入本次推送。元仓随本记录提交后推送；其余7仓与远端一致。完整回执见01 §22。本地提交阶段的保留事实仍由evidence/local-commit-review.json记录。未打tag或生产发布，新家族仍为local candidate。
