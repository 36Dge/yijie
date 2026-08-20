# FEAT-128 - 对话流结构化 Artifact 展示与操作

## 1. 问题与用户价值

当前 Chat 的模型输出只有 Markdown/纯文本增量。即使 Agent 或模型生成了图片、视频、文件或数据分析报告，Desktop 也没有稳定协议、流式状态、专业预览和保存操作来承接，用户只能看到文字说明，无法在对话上下文中直接使用结果。

FEAT-128 把 Assistant 输出扩展为“文本 + 结构化 Artifact”。Artifact 在生成开始时立即进入对话流，随后按真实阶段更新，完成后提供与类型匹配的预览、详情和本地保存能力。

## 2. 目标用户与核心场景

- 用户：使用 macOS Desktop 本地 Chat 的已授权卖家。
- 图片：生成开始后显示占位与阶段，完成后直接预览，可放大并保存图片。
- 视频：生成开始后显示封面占位与阶段，完成后可播放、暂停、拖动进度并保存视频。
- 文件：完成后显示安全文件名、格式、大小与内容预览；支持“另存为”。
- 报告：以结构化摘要、指标、图表、表格和结论展示，不执行原始 HTML/脚本；本候选可预览并另存 canonical Report JSON（`application/vnd.yijie.report+json;version=1`），PDF/Markdown 仅作为后续派生导出。
- 流式体验：文本增量与 Artifact 生命周期可以交错到达，用户不必等待整轮完成才看到工作进度。

## 3. 当前范围

- 新 Agent Host v3 Artifact 事件与资源读取契约，保留现有 v1/v2 语义。
- Provider-neutral Artifact manifest、状态机、完整性校验、失败与过期语义。
- Desktop 本地加密持久化、历史恢复、会话删除级联与保存到用户选择位置。
- 图片、视频、通用文件和结构化报告四类 UI renderer。
- loading、empty、error、permission denied、ready、expired 和 unsupported 状态。
- 本地合成 producer 与固定 fixture，用于无云资源、无付费调用的完整流式 UI/协议验证。
- 对固定 Runtime `imageGeneration` item 的候选适配设计；只在 provider capability 真实可用后启用。

## 4. 明确非目标

- 本期不购买云服务器、数据库、对象存储、CDN 或转码服务。
- 不部署到 staging/production，不签名、公证、发布或启用生产流量。
- 不声称当前 MiniMax-M3 接入已经能生成图片、视频、文件或报告。
- 不在 WebView 执行 Artifact 中的 HTML、JavaScript、宏、外部链接或任意 ECharts option。
- 不提供协作分享、公开链接、多设备同步、版本管理、在线编辑、视频转码或云端缩略图。
- 不把文件保存动作解释为高风险业务写操作；保存范围只限用户通过 native dialog 明确选择的本机目标。

## 5. 成功标准

- Artifact 开始事件到达后，Desktop 在 300ms 内创建稳定占位，文本流继续更新且布局不跳动。
- ready 前不显示可用预览/保存；失败、取消、断线与过期均保留明确状态和恢复动作。
- 图片、视频、文件、报告均有类型匹配的专业展示，亮色/暗色、1180x760、键盘和 reduced motion 可用。
- 原始路径、bearer、API Key、文件正文和 provider raw error 不进入公共事件、DOM、日志或遥测。
- v1/v2 consumer 不接收新 Artifact 事件；v3 consumer 对未知 Artifact kind fail soft。
- 本地固定 fixture 可重复证明 announce -> progress -> ready/failed 的流式路径，不依赖云资源或真实模型费用。

## 6. Owner 与授权边界

| 角色 | Owner |
|---|---|
| 需求负责人 | 段成威 |
| Product/Design 决策人 | 段成威 |
| 技术负责人 | 段成威 |
| Reviewer | 段成威 |
| 发布负责人 | 段成威 |

2026-08-20 的用户请求授权创建本需求交付包，并明确本期只要求本地可用、不准备部署或购买云资源。用户随后明确要求执行 G2 closure rewrite、记录 Product/Design、Technical、Security/Data Owner 的 G2 批准，并在 G2 后只启动 `yijie-contracts` S1/S2；只有真实 generate、breaking、semantic review、immutable commit 与 downstream exact pin 全部通过 G2A 后，才允许开始 Host/Desktop 业务切片。该条件已满足，随后 S3/S4 按序完成并以实际证据通过 G3 slice gate。本授权仍不包含 push、tag、契约发布、真实付费模型调用、生产激活或 G4-G6 批准。

标准流程备注：本地-only synthetic profile 只能作为隔离验收入口，默认关闭；它不改变既有 v1/v2 文本流程，也不能替代 G2/G2A、真实 provider capability 或生产门禁。

## 7. 当前状态

- 状态：`G3 PASS for Host S3 + Desktop S4 native foundations / S5-S11 pending / real providers closed`。
- `contract-impact = semantic`：虽然计划用显式 v3 协商保持 v1/v2 wire 兼容，但现有 Runtime `imageGeneration` item 的解释将从“信息性 item”变为可持久化、可预览、可保存 Artifact，跨进程与持久化语义发生变化，按最高风险归类。
- G0/G1/G2 与 G2A 均有可复核证据；Contracts immutable candidate 及两端 exact pin 已形成并通过完整检查。
- G2A 后已严格按依赖完成 Host S3，再完成 Desktop S4；这只证明本地 Host/native foundation，不代表
  renderer、synthetic 端到端、真实 provider、发布或生产门禁通过。
