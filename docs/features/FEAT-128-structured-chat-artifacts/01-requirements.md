# FEAT-128 需求与验收标准

## 1. 业务规则

- R-001：Assistant turn 可同时包含 Markdown 文本和零到多个结构化 Artifact；Artifact 不通过 Markdown URL、HTML 或约定字符串伪装。
- R-002：Artifact kind 首期为 `image | video | file | report`；公共 wire 使用显式 v3 协商，v1/v2 不发送新事件。
- R-003：每个 Artifact 使用不可复用的 opaque UUID，与 tenant、user、session、turn 和 item 绑定；跨 scope 读取或保存必须拒绝。
- R-004：wire 生命周期固定为 `item.artifact.started -> item.artifact.progress* -> item.artifact.completed|item.artifact.failed`；Desktop 本地状态映射为 `announced -> generating/processing -> transferring -> ready`，失败/取消进入 `failed | cancelled`，retention 后为 `expired`。各层终态单调，重复事件幂等，倒序/缺口触发 resync。
- R-005：`announced` 到达即可创建占位。progress 可以只有阶段而没有百分比；UI 不伪造进度，不把固定动画时长解释为真实生成进度。
- R-006：`item.artifact.completed` 的 wire `status=ready` 只携带安全 metadata 与 opaque content reference，不携带 base64、绝对路径、bearer、原始 provider payload 或文件正文；Desktop 在本地 transfer/commit 成功后才标记 local `ready`。
- R-007：内容读取必须经过本机认证边界，支持完整性校验、长度上限、超时、取消和流式写入；重定向、外部 URL 与路径穿越默认拒绝。
- R-008：Desktop 是本地历史展示 authority。ready 内容先由 native 边界校验并写入加密存储，再对 WebView 标记可预览。
- R-009：图片允许 PNG/JPEG/WebP/GIF，首期最大 20 MiB；视频允许 MP4/WebM，首期最大 64 MiB；文件/报告导出物最大 64 MiB；每轮 Artifact 总量最大 128 MiB、最多 12 项。
- R-010：图片显示原始宽高比，支持点击放大、缩放、重置与保存；不自动裁切关键信息。
- R-011：视频不自动播放，默认静音状态由用户控制；提供播放/暂停、时间、拖动、音量、全屏和保存，失败时显示可执行恢复。
- R-012：文件展示名称、媒体类型、大小与安全预览。文本/Markdown/JSON/CSV 使用有界只读预览；PDF/Office 等未实现安全 renderer 的格式显示 metadata 和“另存为”，不伪装已预览。
- R-013：报告使用版本化结构化 document，支持摘要、指标、段落、表格、有限图表和提示块；canonical 内容为 `application/vnd.yijie.report+json;version=1`；禁止 raw HTML、脚本、iframe、远程资源和任意 ECharts option，PDF/Markdown 仅可作为后续派生导出。
- R-014：保存动作必须由用户显式触发 native save dialog；写入临时文件后原子替换，失败不删除本地 authority 副本。
- R-015：历史重开、分页与 resync 后，Artifact 的顺序、状态、metadata 和 preview eligibility 必须一致。会话永久删除级联清除 Artifact 内容、metadata、临时传输和预览缓存。
- R-016：Artifact 默认本地保留七个 24 小时；`expires_at = local_committed_at + 168h`，其中 `local_committed_at` 是 Desktop 完成完整性校验并提交 SQLCipher 的时间。`now >= expires_at` 时清除内容与 preview cache，保留最小历史 metadata 和 `expired` 状态。未来改变保留期或起算点需独立数据决策。
- R-017：permission denied、unsupported、failed、cancelled 和 expired 均保留类型图标、状态说明和下一步，不只靠颜色表达。
- R-018：MiniMax“支持多模态”不能等同于“当前 provider 已启用输出生成”。真实 producer 必须通过 capability probe、固定模型/API 版本和集成测试后才可启用。
- R-019：严格 local synthetic profile 可以为 `image | video | file | report` 四类发出固定 fixture；`provenance=synthetic` 必须持久化并显著展示。真实 `provider | tool` producer 继续按 kind 关闭，不能用真实 producer 的未知项阻断本地 synthetic 契约候选。
- R-020：当前取消只复用既有 turn interrupt；它把该 turn 内尚未终态的 Artifact 映射为 `failed(error_code=turn_interrupted)`，Desktop 显示 `cancelled`。本候选没有 artifact-specific cancel endpoint 或卡片级取消按钮。

## 2. 可观察状态

Wire 事件名称和 Desktop 本地展示状态是两层语义：`started` 创建 `announced` 占位；`progress.stage` 映射为
`generating` 或 `processing`；wire `completed/status=ready` 表示 Host 资源已可认证读取，Desktop 随后进入
`transferring`，校验并提交到 SQLCipher 后才进入 local `ready`；wire `failed` 映射为 `failed` 或
`cancelled`。`expired` 只由本地 retention maintenance 产生。

```text
announced -> generating -> processing -> transferring -> ready -> expired
     |            |             |              |
     +----------> failed <------+--------------+
     +----------> cancelled (turn-level interrupt only)
```

- `ready`、`failed`、`cancelled`、`expired` 为 UI 终态；`ready -> expired` 是 retention maintenance 的唯一合法终态迁移。
- 事件缺口、stream id 变化或 manifest/content 不一致时，Artifact 进入 `resync_required` 页面状态，不继续使用缓存内容。

## 3. 验收标准

### AC-001 流式占位

Given 模型文本仍在输出，When v3 `item.artifact.started` 到达，Then 对话中 300ms 内出现固定尺寸占位、类型和等待/阶段状态（本地状态为 `announced`），不等待 turn terminal，后续文本和进度不会导致消息列宽跳动；取消只通过既有 turn-level stop，不显示未定义的 Artifact 级取消操作。

### AC-002 单调进度与恢复

Given progress 重复、倒序、缺号或断线，When Desktop 接收事件，Then 重复被幂等忽略，倒序/缺号触发 resync；已 ready/failed/cancelled 的 Artifact 不退回 generating。

### AC-003 图片结果

Given 合法图片 ready，When 用户查看结果，Then 按真实宽高比显示清晰预览；可键盘打开 lightbox、缩放/重置并通过 native dialog 保存。损坏、digest 不符或过大内容不会进入 DOM。

### AC-004 视频结果

Given 合法 MP4/WebM ready，When 用户操作播放器，Then 可播放、暂停、拖动、调音量、全屏和保存；默认不自动播放，加载失败显示原因和重试/保存边界。

### AC-005 文件结果

Given text/Markdown/JSON/CSV 文件 ready，When 用户打开预览，Then 只读预览有长度/行列上限、搜索与截断说明，并可另存为；Given 不支持 inline renderer 的格式，Then 只显示 metadata 和保存操作。

### AC-006 结构化报告

Given report document v1 ready，When Desktop 渲染，Then 显示标题、摘要、指标、表格、有限图表、结论与来源时间；图表有 tooltip 和文字摘要；未知 section 显示“不支持此报告区块”且其余区块继续可用；下载保存同一版本的 canonical Report JSON，PDF/Markdown 不属于本候选验收范围。

### AC-007 历史与过期

Given 用户重开包含 Artifact 的会话，When history/resync 完成，Then 顺序、状态和 metadata 恢复；到期后内容不可读取或保存，UI 显示“结果已过期”，会话文本仍保留。

### AC-008 安全读取与保存

Given 跨 tenant/session ID、过期 reference、重定向、路径穿越、MIME/魔数不一致或 digest 错误，When native 读取 Artifact，Then fail closed；事件、错误、日志和 DOM 不包含路径、token、正文或 provider raw payload。

### AC-009 兼容性

Given v1/v2 Desktop 或未声明 v3 的请求，When Host 发布 Artifact，Then旧 consumer 不接收新事件且既有文本流保持逐事件语义；Given tolerant v3 consumer 收到未来 envelope 中的未知 kind/section，Then 由 adapter 显示 `unsupported` 占位并继续处理同一 turn 的已知内容；当前 strict Host/schema 不主动发出未评审 kind。

### AC-010 视觉与可访问性

Given light/dark、1180x760、200% zoom、keyboard、VoiceOver 和 reduced motion，When 查看四类 Artifact 的 loading/ready/error/permission/expired 状态，Then 无重叠或横向主体滚动，图标按钮有 accessible name/tooltip，焦点可见，状态不只依赖颜色。

### AC-011 本地无云验证

Given 无云服务器、数据库、对象存储和真实付费调用，When 启用严格 local-only synthetic profile，Then 固定 fixture 可重复产生 image/video/file/report 的 announced/progress/ready/failed 路径并完成 UI 与协议验收；这四类 synthetic fixture 不依赖真实 producer authority，界面明确不把 fixture 标记为真实模型生成。

### AC-012 真实 producer 启用门禁

Given MiniMax provider 尚未证明 output generation capability，When 应用正常启动，Then synthetic profile 默认关闭、真实生成入口不出现；只有 capability、模型/API pin、费用授权和集成测试全部形成后才允许启用对应 kind。

## 4. 非功能要求

- NFR-001：announced 到可见占位 p95 小于 300ms；progress 合并刷新不高于 10Hz。
- NFR-002：对话滚动时单个 Artifact renderer 不阻塞主线程超过 50ms；长列表使用懒加载和离屏暂停。
- NFR-003：preview 内存峰值目标不超过 Artifact 大小的 2.5 倍；超过本地预览上限时降级为 metadata + 保存。
- NFR-004：所有读取、保存、解码、图表和历史操作可取消，并在组件卸载时释放 object URL、timer 和 media handle。
- NFR-005：测试数据全部合成；禁止真实卖家文件、商家数据、API Key、cookie、路径或品牌受限素材。

## 5. 当前限制

- 固定 MiniMax-M3 catalog 只声明 `text/image` 输入；这不是媒体输出能力证据。
- 固定 yijie-codex Runtime 有 `imageGeneration` item，但当前 MiniMax provider 未启用对应 extension；视频/文件/report 没有既有 Runtime output item。
- 因此本包把通用协议/UI设计与 producer activation 分开；本地合成 vertical slice 可以验收展示链路，但不能证明真实生成质量或费用可控。
