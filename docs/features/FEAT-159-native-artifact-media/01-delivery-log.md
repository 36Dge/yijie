# FEAT-159 实施记录

2026-10-18：用户批准后再次审查，开始source-first实现。基线Contracts 9743173474cb68f665044d3ac5765a0f18f16397、Host 87e8f8c7bd43035cffcd151da2de26efa6593f48、Desktop 299818cd8703fd202a000596479fdcb709b287df、Runtime 7fd463bcef07f37b0211acd9f62b9f93ea0a4b12；工作区初始干净。

- Contracts：独立schema9从原v3机械派生；旧源未改；新增工具闭集DTO/媒体策略和双consumer摘要同步。
- Host：复用MCP固定SDK 1.8.0（新增受控adapter）、GetByThread/Cwd/os.Root/Store/EventHub/resource/ACK。只向v9发新媒体；旧线程沿既有SwitchThread/resume；原生Runtime不改。
- Desktop：SVG复用图片入口；MP4保留边界检查、由WebKit解码音视频，删除旧单轨fixture解析；HTML用无IPC的raw Wry/WebKit独立窗口。原生窗口API使用现有Tauri同版本的unstable GUI feature，与Codex experimental API无关。
- 本地source candidate复用FEAT156/158现有工作树freeze机制，增加FEAT159来源集合；没有关闭committed/legacy来源检查。首次freeze因旧market-catalog引用的base_commit落后失败，确认catalog字节摘要相同后用原sync脚本更新base_commit，未改变目录或启用provider。
- 首次UI测试误匹配到.local内历史source副本，14失败不计结果；改用项目规定的.local/source排除范围后当前代码7项控件测试通过。
- 普通SQLCipher测试首次用了1970时间戳，正常重开清理已过期记录而失败；已按真实当前提交时间修正测试，不修改产品过期规则。
- 标准应用经canonical packaged入口成功启动，显示原有专家聊天；目录选择器已授权本次feat159-workspace。正常退出App/Host/Runtime/adapter完成。CUA后续读取曾重新启动一个无环境窗口，已正常退出；无强杀。
- 静态复核补齐首次Artifact引用早于历史轮次到达的展示；五项原生视图测试通过，不从产物状态推断原生Turn状态。
- 模型额度待用户回答；至此模型调用0、外部商家调用0。
- 再次复核补齐：schema9伴随流统一各producer产物序号（旧v3原值不改）；真实终态后和会话删除时清理登记权威；HTML窗口按授权context与artifact绑定，复用ChatAuthorizationManager监视授权失效并以持久化过期时间/30分钟上限关闭。前端身份切换/卸载释放对应窗口。
- Host普通链路race测试2项、Native普通媒体/SQLCipher恢复2项、最终普通控件选择6项通过；设计文档构建通过。
- 标准packaged入口再次构建运行；通过正常Cmd+Q退出并以`--reopen`验证同构建receipt与已有任务列表恢复。此证据不冒充新媒体真实界面验收。最后的context窗口标签修正纳入最终标准构建。

- 用户明确答复“批准本次最多 4 次”；额度仅本轮短文本请求，新聊天和已有专家各1次，最多2次修复复验，不调用付费图片、视频或商家工具。锁屏已解除，继续真实验收。
- 真实模型请求 1/4 已发送（新普通聊天，2026-10-18 14:19:38）。仅要求登记已存在的普通 HTML/SVG 和用户原视频副本，不修改文件，不使用其他工具。
- 请求1/4完成，真实工具成功登记3份产物；HTML内置中文与按钮0→1、SVG预览与100%→125%通过；三类Native保存和HTML保存取消通过，保存字节与SHA-256完全一致。视频控件7秒进度与未静音状态已观察，实际声音及灰色抓图是否为捕获限制待用户确认。
- 经系统文件夹选择器重新授权原final-workspace后，已在原UI设计师聊天发送请求2/4；继续等待原操作查询，未重复发送。
- 正常退出后，以 bbolt 官方库 ReadOnly 打开 Host 存储，仅查看目标会话状态：原 UI设计师 thread 01a14a7b-eeea-7221-a62a-d14902dbeb7f 从 2026-10-17T15:29:58Z 起保留 active_turn_id；原生 rollout 末尾却为同日15:47:30Z的turn_aborted。本轮没有该线程的新原生turn或Host提交receipt。判定为既有中断恢复状态不一致，未改数据库，未重复发送该原操作，不能算验收通过。
- 已正常重开；请求3/4在既有、终态已确认的跨境电商带货口播专家聊天发送，界面确认进入“正在生成”。请求次数按提交保守计3，真实新模型轮次至此2。
- 请求3/4成功：既有口播专家保留同一native thread，3次publish_artifact后task_complete；三份ready卡片，HTML交互0→1通过。CUA随后持续noWindowsAvailable/timeoutReached；仅重置一次工具REPL并做只读sample，未强杀。已请求用户将易界主窗口置前。

- 用户确认首次视频验收实际灰屏且无声，判定FAIL，不归因于截图限制。复用现有协议诊断发现正常音视频并发Range超过两路即撤销句柄，后续404。保留两路读取和64 MiB限制，用现有Tokio信号量提供16个请求的有界等待及10秒超时；不改播放器或Runtime。
- 复验：原视频画面可见，用户明确确认“画面和声音都正常”；612次Range全部206、拒绝/限额/404均0。进度条点击可跳到3秒；SQLCipher跨页与尾部分段逐字节比较通过。临时计数日志已从产品源移除，仅保留原有feature-gated诊断。
- 一次正常Cmd+Q触发SIGSEGV：系统只读崩溃报告表明主线程由NSApplication terminate直接进入sqlcipher_atexit，数据库线程同时仍执行pending_artifact_acknowledgements。原有ExitOwner未承接系统默认Quit菜单。主窗口关闭入口经ExitOwner正常exit0；修复只替换默认菜单Quit动作，复用同一ExitOwner清理协调器，无强杀或新生命周期实现。最终构建与重启复验继续。

- 最终源码保持冻结后canonical构建成功；修复后的Cmd+Q在视频播放中正常exit0，Host/adapter/18081均停止，未再次出现该崩溃。正在同构建--reopen验收持久化媒体。

- 同构建重启后，两类聊天的6份产物恢复；HTML按钮0→1、SVG125%、原视频画面再次通过。三类文件经Native保存到after-restart，逐字节与原件一致；最终保存取消通过。1180×760亮暗色检查完成，已恢复系统外观和原窗口尺寸。最终本地候选验收PASS，历史UI设计师状态不一致另列未修复；没有新模型请求、提交、推送或发布。

2026-10-18 后续：用户授权复审后提交推送。复审修正合法带命名空间前缀SVG的Native兼容性，复用quick-xml NsReader，普通样本及保存重开测试通过。详见03-final-review-and-push.md。此前“未提交、未推送”和UI设计师历史异常是当时状态；后者已由FEAT160真实验收解决。

四个代码仓库已普通push并逐一核对远端HEAD；已提交源码canonical构建和现有内容观察通过。元仓将记录本次审核、完整commit及来源顺序；未发布安装包或部署。
