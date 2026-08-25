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
- R-019：严格 local synthetic profile 可以为 `image | video | file | report` 四类发出固定 fixture；`provenance=synthetic` 必须持久化并显著展示。synthetic 与真实 provider 配置互斥，前者不能冒充后者的能力证据。
- R-020：当前取消只复用既有 turn interrupt；它把该 turn 内尚未终态的 Artifact 映射为 `failed(error_code=turn_interrupted)`，Desktop 显示 `cancelled`。本候选没有 artifact-specific cancel endpoint 或卡片级取消按钮。
- R-021：MiniMax-M3 只能通过 Runtime 的结构化 `generate_image` dynamic tool 表达生图意图；Host 不得按关键词、附件存在与否或自由文本猜测并触发付费调用。
- R-022：Host provider adapter 固定调用 `POST https://api.minimaxi.com/v1/image_generation`，固定 `model=image-01`、`response_format=base64`、`n=1`；拒绝 `image-01-live`、`style`、任意 endpoint 与模型覆盖。
- R-023：生图工具输入只允许非空 `prompt`（最多 1500 字符）、`mode=text_to_image|subject_reference` 与可选
  `aspect_ratio`；比例闭集为 `1:1|16:9|4:3|3:2|2:3|3:4|9:16|21:9`，默认 `1:1`。首版不暴露
  `n`、provider/model、URL、path、base64、watermark、prompt optimizer 或任意 provider 参数。
- R-024：图生图首版只支持 `mode=subject_reference`，且当前 turn 必须恰有一张已通过现有附件校验的 PNG/JPEG 参考图；Host 以完整 Base64 Data URL 映射为一个 `subject_reference`，`type=character`。零张、多张、GIF/WebP、文件大小 `>=10,000,000` bytes 或 authority 不匹配时拒绝，不接受模型提供的 URL、路径或图片正文。
- R-025：Host 不能只看 HTTP 200；还必须验证 `base_resp.status_code=0`、`data.image_base64` 恰有一个成员、
  `metadata.success_count=1/failed_count=0`（兼容官方 schema 整数与示例十进制字符串后再归一化），并严格 base64
  解码、限制响应/解码大小、检查图片 magic/MIME/尺寸、计算 SHA-256，随后才发布 `provenance=provider` 的 v3 image Artifact。
- R-026：MiniMax Key 只由 Host 安全配置读取，不进入 Desktop/WebView、Runtime prompt/tool arguments、公共事件、日志、错误或 Artifact metadata。用户参考图属于一次明确生成请求的数据外发，只在当前 turn/operation 的短期 owner-only 边界内使用。
- R-027：Runtime `call_id` 与 session/turn 共同构成 Host 付费操作幂等键。重复调用不得二次计费；请求发送后发生超时/取消时结果记为 `provider_outcome_unknown`，不得自动重试，只有用户明确的新操作可再次调用。
- R-028：付费验证全功能总上限为 5 次发送尝试且每次 `n=1`；计划使用 4 次（S12E 的 T2I/I2I
  capability 各一次，S12F 的真实对话 T2I/I2I vertical 各一次），另有 1 个 repair slot 只供明确根因修复后的复验；
  它是总预算中的第 5 个额度，不要求按物理发送顺序恰为第 5 次。台账必须分开
  `reserved_slots` 与 `used_calls`：并发/预算判断前原子 reserve；pre-send reject/cancel 释放 reservation 且不增加 used；
  紧邻首次网络 write 前转 `sent` 并不可逆增加 used。sent 后的成功、provider 失败、网络错误、超时或 outcome unknown
  均计入 used；fake HTTP 永不计入。ledger 必须区分 `quota_class=planned|repair`：普通计划调用要求
  `planned_used+planned_reserved<4` 且总量 `<5`；repair 必须绑定一次性 Owner authorization、明确 RCA 与原失败。
  最多允许 4 个 planned send attempts，
  以及最多 1 个可在任一 planned failure 后使用的 repair send attempt；repair 不能被新场景挪用。未授权 repair、
  任意第 6 个总 attempt 或任一分类超额都在网络前 fail closed。startup 对各分类 orphan reservation 转
  `failed_pre_send` 并释放，不补发请求。整个验证使用一个不可按 runner/run-root 重置的 durable campaign ledger：
  `campaign_id=feat128-s12-image-validation-20260823`，slot 固定为 `P1=S12E/T2I`、`P2=S12E/I2I`、
  `P3=S12F/T2I`、`P4=S12F/I2I`、`R1=repair(original_slot_id)`；两个 runner 必须对同一 authority 做 slot CAS。
  slot 只能原子 `available → reserved → sent`；pre-send 释放回 `available`，`sent` 与分类/总计更新以及 R1 authorization
  消费必须同事务持久化。aggregate counters 只能由 slots 推导/核对，不能独立重置。restart、并行进程、新 run root 或
  删除临时目录都不能恢复已 sent slot；ledger 缺失/漂移时禁止网络并要求 Owner 对账。
- R-029：S12E/F 只使用合成 prompt 与合成参考图。发送到 MiniMax 后，本地 kill switch/cleanup 不能证明 provider
  侧删除；S12E 前必须复核官方当时的数据保留/删除政策并记录已知或 `UNKNOWN`。在生产 Go/No-Go 单独批准前，
  不外发真实用户、商家、品牌或受限素材。

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

Given 普通安装或未满足 exact real-image 配置，When 应用启动，Then synthetic 与真实 image producer 均默认关闭；Key 存在不等于启用。Given 开发验证显式启用且 capability、模型/API pin、费用台账与前置门禁成立，Then 只允许 image kind 的有界调用；生产启用仍需单独 Go/No-Go。

### AC-013 真实文生图端到端

Given real-image 验证配置已显式启用，When 用户明确要求生成图片，Then MiniMax-M3 发出一次结构化
`generate_image(mode=text_to_image)` 调用，Host 只调用一次固定 `image-01`，将真实输出发布为
`provenance=provider` image Artifact；Desktop 在对应 assistant turn 中预览、历史重开并可 native save。

### AC-014 真实人物参考图生图端到端

Given 当前 turn 恰有一张合格 PNG/JPEG 人物参考图，When 用户明确要求基于该人物生成新图片，Then 工具调用使用
`mode=subject_reference`，Host 只将该附件映射为一个 `subject_reference.character` 并完成同一 Artifact 链路；
零张、多张或不支持格式时不外发且返回可恢复错误。

### AC-015 不误触发与工具决定

Given 用户只要求识图、总结图片或进行普通文本对话，When MiniMax-M3 处理请求，Then 不发起生图工具调用且调用台账不增加；Host 不用关键词规则补发调用。

### AC-016 Provider 失败与付费幂等

Given 鉴权、余额、限流、内容安全、参数、超时、网络、5xx、畸形 base64、重复 call 或取消，When Host 执行工具，Then 返回稳定 content-free 失败、Artifact 只进入 failed/不创建、同一幂等键最多一次外部请求，且不自动付费重试。

### AC-017 Secret、内容与响应隔离

Given T2I/I2I 成功或失败，When 检查 Runtime、v3 事件、Desktop DB/DOM、Host/Desktop 日志和验证制品，Then
API Key/Authorization 在 Host secret/HTTP header 之外零命中，provider base64/raw response/raw error 在 Host 有界
处理中之外零命中。用户 prompt 与参考附件只允许出现在既有授权的 Desktop user-turn authority、Runtime 当前轮输入/
tool arguments、Host 当前轮 provider request 和 MiniMax request 中；不得被 tool result、Artifact metadata、日志、遥测或
验证制品重复。只有经校验的生成图片 bytes 进入现有加密 Artifact authority。

## 4. 非功能要求

- NFR-001：announced 到可见占位 p95 小于 300ms；progress 合并刷新不高于 10Hz。
- NFR-002：对话滚动时单个 Artifact renderer 不阻塞主线程超过 50ms；长列表使用懒加载和离屏暂停。
- NFR-003：preview 内存峰值目标不超过 Artifact 大小的 2.5 倍；超过本地预览上限时降级为 metadata + 保存。
- NFR-004：所有读取、保存、解码、图表和历史操作可取消，并在组件卸载时释放 object URL、timer 和 media handle。
- NFR-005：测试数据全部合成；禁止真实卖家文件、商家数据、API Key、cookie、路径或品牌受限素材。
- NFR-006：真实图片调用默认单并发；适配器遵守官方当前图片限流基线，不排队形成无界积压，所有 HTTP/JSON/base64/decoded image 缓冲均有硬上限。
- NFR-007：每次付费调用的 content-free 台账记录 operation、模式、开始/终态、调用计数、图片计数、稳定失败类、延迟区间与配置 identity；不记录 prompt、附件或 provider payload。

## 5. 当前事实与限制

- 历史基线只证明 MiniMax-M3 的 text/image 输入和真实文本输出；它没有自动调用真实图片 provider。
- 固定 Runtime 已有 experimental `thread/start.dynamicTools` 与反向 `item/tool/call`，本期选择它作为
  M3→Host 的结构化工具通道；内置 `imageGeneration` 扩展依赖 OpenAI auth 且固定 OpenAI 图片模型，不能用于本需求。
- MiniMax 官方当前证明的 I2I 是单张 `subject_reference.character`，因此首版不承诺通用图片编辑。
- S10D-H 是 strict-local/keyless/synthetic 验证骨架，已实现并尝试运行但尚未通过；它与真实 image-01 S12 阶段互不替代。
