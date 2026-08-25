# FEAT-128 — 真实图片生成 Demo Brief

> Usable route: `demo_fast` · Exposure: `local` · Created: `2026-08-23` · D4: `PASS`
>
> 原 schema v2 / S12 / S10D-H 路线保留为历史 `production_hardened` 账本。S10D-H 仍为
> `FAIL/PAUSED` 且 fuse open；本路线不关闭、不重试、不借用其证据。

## 1. 用户问题与结果

- 目标用户：在 macOS Desktop 快速验证本地 Chat 的 Owner。
- 当前问题：文本对话和图片理解已经可用，但用户输入“生成一张海报”时只会得到文字；现有图片
  Artifact 展示链路没有真实模型 producer。
- 用户结果：用户在同一条消息中看到真实 `image-01` 图片的生成状态、结果、预览与保存；附带一张
  人物图片时，可明确要求参考该人物生成新图。
- In scope：MiniMax-M3 工具决策、Host `image-01` adapter、文生图、单张人物参考图生图、v3 Artifact、
  Desktop 展示/预览/保存、真实本地启动。
- Out of scope：任意编辑、多图/非人物参考、其他模型/媒体类型、公网部署、SLA、多租户和完整生产加固。

## 2. 完整主流程

1. 用户运行标准命令 `pnpm tauri:dev`（`pnpm tauri:demo-fast` 为同义显式别名）；launcher 先构建当前开发态 Agent Host，再以 Tauri dev app 使用 bundled
   Codex Runtime。Native 自动绑定固定 local identity/tenant/capabilities，Desktop 无登录页面、浏览器或账号
   密码并直达 `/chat`，同时自动启动 Host/Runtime；这不是 packaged release 启动链。
2. 用户发送明确的生图请求；参考图生图时，在当前轮附带一张 PNG/JPEG 人物图并明确要求参考人物。
3. MiniMax-M3 只在明确生图意图下调用 flat `generate_image` dynamic tool；普通对话/看图分析保持文本。
4. Host 固定调用 `https://api.minimaxi.com/v1/image_generation`、`image-01`、base64、`n=1`，
   参考模式只发送一个 `subject_reference.character`。
5. Host 校验 HTTP、业务状态、响应计数、base64、文件魔数/尺寸/大小，随后通过现有 v3 Artifact 发布。
6. Desktop 在当前 assistant 消息中展示 loading/progress/ready，复用 lightbox 和 native save。
7. 失败或取消时显示安全终态与重新提交建议；不发布伪 ready，也不自动重复付费调用。

## 3. 交互与 UI

- 视觉：复用当前 Artifact card，不增加生图工作台；卡片与文本同处一条消息，信息层级保持稳定。
- Idle/Empty：没有工具调用时只有正常文本，不显示空媒体框。
- Loading：立即显示稳定占位、阶段与进度，禁止 preview/save。
- Success：显示真实图片；点击进入 lightbox，保存使用 native dialog。
- Error：显示脱敏说明，不暴露 provider raw error、Key、Data URL/base64。
- Retry：提示在输入框重新提交或调整要求；不做自动付费重试。
- Cancel：停止本轮并关闭在途 Artifact，下一轮不继承旧附件或 tool 状态。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-IMG-001 | 明确 T2I 请求获得真实 image-01 图片 | fresh real Desktop，核对 Artifact/预览 |
| AC-IMG-002 | 单张人物附件可作为人物参考生成新图 | fresh real Desktop I2I，确认不是附件回显 |
| AC-IMG-003 | 普通对话/看图分析不调用生图 | 消息、事件与调用计数 |
| AC-IMG-004 | loading/success/error/retry/cancel 清晰且不卡死 | focused UI test + real smoke |
| AC-IMG-005 | ready 图片可预览与 native save | 真实 Tauri 预览、保存、解码 |
| AC-IMG-006 | Key/base64/Data URL/raw error 不进入公共面 | security tests + 脱敏日志检查 |
| AC-IMG-007 | provider/校验失败 fail closed 且无盲目重试 | fake provider failure smoke |
| AC-IMG-008 | local demo fresh 启动零登录交互、自动 Host/Runtime、直达 `/chat`；非该 profile 保持原认证 | canonical launcher 进程链 + 同 profile latest debug app fresh/Settings 重启 UI + exact profile 负向回归 |

## 5. 工程事实与边界

- 受影响仓库：`yijie`、`yijie-agent-host`、`yijie-desktop`。
- 真实入口：Tauri dev app 中的真实 ChatPage → launcher dev-built Host → bundled Runtime → MiniMax-M3 tool →
  Host image-01 provider → v3 Artifact → Desktop。
- `contract-impact=semantic`：图片 dynamic tool/provider 子变化仍为 additive，但 ADR-0018 改变了 local Desktop
  的身份入口、public-task 与 sidecar 启动语义；公共 wire 与非 local/production OIDC 不变。
- Source first：Runtime canonical protocol → Host router/provider → 既有 Contracts v3 → Desktop consumer。
- Key 仅允许 owner-only 文件路径传给 Host；不通过 argv、WebView、公共事件或日志。付费调用 hard max 5，
  每次 `n=1`；未知超时不盲重试。
- 2026-08-23 23:31 +08:00 已用 fresh isolated Demo DB/secret 在 canonical 等价完整环境验证无登录直达
  `tauri://localhost/chat`，真实普通文本 1 turn 返回 `DEMO_FAST_OK`；本轮无图片 Artifact、未触发
  `generate_image`，`image-01` 调用 0，既有图片调用账本保持 3/5。
- canonical launcher 已通过 fresh Desktop/Host/Runtime 进程链、污染环境启动、正常/异常退出；标准
  `pnpm tauri:dev` 与显式别名 `pnpm tauri:demo-fast` 均指向该 launcher；同 profile
  latest debug app 的 fresh 与 Settings→quit→restart UI 均直达 `/chat`，Settings 不含登录控件。
- 2026-08-24 10:00 +08:00，真实 Desktop T2I、仅看图分析、人物参考 I2I、preview、native save、重启持久化与窗口失焦恢复全部通过；8/8 Must AC 和 D4 为 PASS，付费调用账本最终 5/5。
- 工作区已有 S12A 文档修改，必须保留；Host/Desktop 当前功能改动属于本快速路线，不覆盖用户改动。

## 6. 推荐方案与停止条件

- 推荐方案：flat legacy `generate_image` dynamic tool + Host 内部严格 adapter；不新建公共 Artifact DTO、不增加
  Desktop renderer，通过最短纵向链路复用现有能力。
- 30 分钟无新证据：读取完整 Runtime reverse-request、Host provider 与 Artifact 日志，停止猜测式补丁。
- 90 分钟同一阻塞：简化为已证明可用的单请求/单参考实现，关闭非核心 UI 花活；不回到 S10D-H harness。
- 240 分钟核心 vertical 仍不可用：重新选择工具桥接方式或先缩减为 T2I，但不得把 I2I 标成完成。
- 超过 16 小时仍未 D4：停止累积基础设施，重新确认最小范围和架构。
