# 第5步：真实 Desktop 最小编辑闭环资格

2026-09-12。用户明确恢复解锁后的真实 App 验证，并指定 dev → 会话/边界 → packaged 顺序。
本页记录本次实际操作，保留[09](09-step5-headless-progress.md)及之前证据的历史时点；
不把此前 API-only 或构建检查回填为本次 App 结果。**dev 与 packaged 最小编辑资格通过；5.4 尚未开始，D4 NOT RUN。**

## 运行来源与安全范围

- 原厂 Docker Desktop 正常启动；本次未再观察到此前残留的 credential helper，未强杀或更改 Keychain。
- 通过 Infra canonical up 恢复已登记候选，epoch 为 `bdc6b8e8-0314-4a7d-9e33-f0ea4902c54a`。
  六个服务及宿主认证 ready；editor manifest 保持 `fdbb9a3fb1b76d12efe38de13f44e74e98e323e72b9a86181d97db4614792007`。
- dev 使用标准 `pnpm tauri:dev`，仅 native 取得 absolute credential 文件路径；初次实际 App PID 88322。
  [来源摘要](evidence/step5-real-app/dev-candidate.json)与[正常退出](evidence/step5-real-app/dev-original-normal-quit.json)分别记录。
- 无账号登录、模型/平台/付费调用、真实商家数据、commit/push/tag、远端创建或发布。
  未强杀、劫持执行程序、破坏权限或使用攻击/故障注入 fixture。

## dev 实际闭环

通过真实 App 创建 `7684595660317786112`，初始 revision `7684595660326174720`。
使用画布的添加按钮、文本输入、端口拖线和节点标题拖动，组成开始→文本处理→结束。
保存后返回列表再打开，名称、前缀、两条边和节点位置均保持；API 读回 `runnable=true`。

核心保存 revision 为 `7684599752406597632`；开始 `(80,160)`、文本 `(405,91)`、结束 `(760,160)`。
文本节点相对中途已保存快照 `(470,131)` 经正常鼠标拖动 `(-65,-40)`；未用数据库或 HTTP 补写画布。
证据：[保存](evidence/step5-real-app/dev-api-core-saved.json)、[重开读回](evidence/step5-real-app/dev-api-reopened.json)、
[真实重开截图](evidence/step5-real-app/dev-reopened.png)。

完整图再次修改前缀为“真实 Desktop 到期重连：”，不保存并等待原会话自然到期。
到期遮罩保留可见画布与前缀，iframe 从可交互 AX 树中移除；正常点击保存未改变服务端 revision。
显式重新连接后，同一草稿保留原 base revision、两条边与位置，再通过 App 保存为
`7684601577516040192`。没有修改 TTL、系统时钟或自动重发保存。
证据：[到期截图](evidence/step5-real-app/dev-full-expired.png)、[到期时读回](evidence/step5-real-app/dev-api-expired-save-blocked.json)、
[重连](evidence/step5-real-app/dev-full-reconnected.png)、[保存读回](evidence/step5-real-app/dev-api-reconnect-saved.json)。

未保存时返回列表、切换“新建任务”均触发离开确认；选择继续编辑后前缀保留。
干净状态切到 Chat 后，仅剩 `http://localhost:1420/chat` WebView，编辑器 iframe 被移除，任务输入界面存在；
没有发送模型任务。见[Chat 切换记录](evidence/step5-real-app/dev-chat-summary.json)。

最终 PG/MySQL 只读快照与 App/API 的名称、revision、前缀、三节点位置和两条边一致；
双方 1 create＋4 save 回执按语义归一后相同，版本和执行数均为 0。
MySQL 客户端显式 UTF-8，与数据库侧字节数和 SHA-256 相符。
见[最终数据库记录](evidence/step5-real-app/dev-final-db-readonly.json)及[说明](evidence/step5-real-app/dev-final-db-readonly.md)。

## 原生关闭诊断补齐

本次子变更 `contract-impact=additive`：新增 exact-local 的私有原生观测输出；
FEAT 整体仍为 semantic。业务 HTTP/IPC/MessagePort、身份、数据和权限语义不变，业务 wire 生成 N/A。
源权威为 Desktop `workflows/runtime.rs`；不新增 command、route、capability 或日志服务。

仅在 `Configuration::Enabled` 与 exact-local 均成立，且认证 DELETE 返回 200、源 schema 校验成功、
`closed=true` 后，向 native stderr 输出 `YIJIE_WORKFLOW_LOCAL_DIAGNOSTIC remote_close_confirmed`。
字段仅为 App PID、公开 bridge/workflow/generation/epoch 及布尔确认；不输出 session ID、E、机器凭据、
binding、URL、headers 或任意错误对象。无 binding、epoch 不同和失败分支不输出成功行。

标准重新构建 dev 后，PID 94626 在真实 UI 打开上述流程并点击返回；已取得对应原生确认，且列表重新出现。
见[原生关闭与 UI 关联记录](evidence/step5-real-app/dev-native-close-confirmed.json)。
DELETE 为幂等操作，此事实表示 API 确认已关闭，不冒称执行了旧 E 重放探测或一定删除了仍有效记录。
`cargo fmt --check`、`cargo clippy --lib -- -D warnings`、13 项安全 native 定向测试均通过。

## 视觉与工具边界

CUA 无法识别无 bundle ID 的 dev 可执行进程；本次改用标准 macOS AX、鼠标/键盘事件和窗口截图操作同一个真实 App。
截图接口初始未授权，用户明确回复“已完成”后已核验权限并取得截图；此前 AX 观察不冒充视觉结果。
早期 AX 设置值或发往后台 PID 的鼠标不总会触发正常输入，最终使用已激活窗口的正常鼠标、键盘和结果读回确认动作。

实际 `1180×760` 窗口中，使用现有“适应画布”并正常滚动后，工具栏、三节点、连线及 footer 无重叠且可查看。
首次视口可能裁切开始节点，手动适应有效；这与源缺首次自动 fit 一致，但未把未激活时 AX 空断言为渲染故障。
见[最小窗口](evidence/step5-real-app/dev-min-fit.png)。

35 份实际 dev AX 快照在可信检查进程内比对当前 K_NA/K_AC，匹配数均为 0；未把秘密作为查询注入页面。
这只证明所检查的页面/AX 文本表面，不宣称进行了完整浏览器 heap 或 MessagePort dump。
原生 DTO、受限 channel 与 CSP 的同源检查和真实编辑路径共同支撑凭据隔离结论。
见[实际 AX 检查范围](evidence/step5-real-app/dev-ax-credential-scan.json)。

## packaged 与最终收尾

使用 canonical unsigned 开发包和标准 `pnpm tauri:demo-fast:app`，未覆盖用户提供、已签名或已发布的二进制。
CUA 正确识别 `com.yijie.ai` 的真实 bundle，PID 96901；父页实际为 `tauri://localhost/workflows`，
同 App 内加载固定 Coze editor，未出现登录页。

独立创建 `7684605114128007168`，初始 revision `7684605114132201472`。
正常添加文本节点、输入“Packaged 中文验收：”、拖两条端口连线、移动文本节点并保存为
`7684605840325607424`；返回列表重开后，UI 前缀和两条可见连线保留，完整 Workflow API 读回逐字段不变。
文本坐标为 `(452.5842696629214,111.68539325842696)`；非整数来自实际画布缩放下的鼠标拖动，按原值保留。
见[保存](evidence/step5-real-app/packaged-api-core-saved.json)、[重开](evidence/step5-real-app/packaged-api-reopened.json)。

Tab 从真实 textarea 进入父页面“查看全部”，Shift+Tab 回到同一 textarea，焦点边框可见。
使用现有适应画布和正常滚动后，工具栏、三节点、两条线和保存 footer 均可见且不重叠。
这些 packaged 视觉观察由当前 CUA 截图直接记录在本次任务中；没有把 dev 的 PNG 当成 packaged 截图。
返回列表和后来干净切换 Chat，分别取得 generation 1、2 的 native `remote_close_confirmed`；
最后为 `tauri://localhost/chat`，iframe 已移除，未发送任务。
见[UI 与两次关闭确认](evidence/step5-real-app/packaged-ui-and-close.json)。

第二资源的 PG/MySQL 快照与 API 完全对应，1 create＋1 save 回执一致，版本和执行数均为 0。
见[packaged 数据库记录](evidence/step5-real-app/packaged-final-db-readonly.json)及[说明](evidence/step5-real-app/packaged-final-db-readonly.md)。
当前整个生成 App bundle、Desktop dist、editor dist 共 91 个普通文件扫描当前 K_NA/K_AC 均为 0，
无超限跳过；公共 editor 响应保留原 CSP。见[包来源与公开产物检查](evidence/step5-real-app/packaged-candidate-and-public-scan.json)。

两次 dev 和 packaged 均经 App 正常退出，启动器 exit 0、自有 App/Host/Codex 进程消失。
Infra canonical stop 确认全部自有容器正常退出并保留卷；确认没有其它运行容器后，原厂 Docker Desktop 正常 stop exit 0。
见[清理记录](evidence/step5-real-app/normal-cleanup.json)和[十二仓/既有设计保护](evidence/step5-real-app/workspace-final.json)。
不把正常退出换算为在途恢复或强制故障恢复资格。

本轮13项原生定向和50项元仓测试、需求包结构/声明与来源保护检查通过，见[验收检查汇总](evidence/step5-real-app/qualification-checks.json)。

本阶段已达到用户指定的最小编辑闭环标准，可以进入 5.4 的完整产品页工作。
首次自动 fit、暗色主题与 1440×900、完整新增可访问性及试运行/内部发布/指定版本执行/结果历史仍须在后续范围内补齐；
AC-010 与整体 fresh D4 没有因此通过。保留既有青柠对比度限制，未暗改用户配色。
