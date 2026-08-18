# FEAT-127 需求与验收标准

## 1. 业务规则

- R-001：Message 是有序内容块容器，支持 `text`、`file`、`image`；现有纯文本消息保持有效。
- R-002：加号是图片与文件的唯一选择入口；位于输入框底部操作区最左侧，不显示“文件/图片”两个按钮。
- R-003：整个 composer 支持拖拽；拖拽和加号必须复用同一 native 校验、解析和持久化逻辑。
- R-004：每个附件最大为 `10 * 1024 * 1024` 字节；每条消息最多 10 个附件；图片原始字节合计最多 10 MiB，避免超过固定 Runtime 16 MiB transport。
- R-005：图片允许 JPEG、PNG、WebP、GIF；文件首期允许 PDF、TXT、Markdown、CSV、JSON、YAML、XML、HTML、RTF、DOCX、XLSX、PPTX。legacy binary DOC 不在首期，因为当前没有可有界验证的本地解析器。扩展名、声明 MIME 和 magic/容器语义必须一致。
- R-006：ZIP、RAR、7Z、TAR、GZ 等压缩包、目录、可执行文件、SVG、Office 宏格式全部拒绝。OOXML 虽以 ZIP 为容器，但只有结构验证为 DOCX/XLSX/PPTX 时允许。
- R-007：选择后按整次 operation 依次显示“排队、导入、解析、建立索引、已就绪”状态；进度事件只包含 opaque context/operation、sequence、item count、stage 和 issue，不广播文件名或附件 metadata。任一附件未就绪时不能发送；失败的整次选择提示“移除后重新选择”，不提供原地重试。
- R-008：允许仅文本、仅附件或文本加附件发送；成功持久化前不得清空草稿与附件。
- R-009：文件按有界文本分块建立本地索引，按用户问题选择相关片段作为 Context；图片作为 Runtime image input。解析内容不进入 Public Tasks、API PostgreSQL、Host bbolt、日志或遥测。
- R-010：附件二进制、解析文本与索引在 Desktop SQLCipher 中保存；WebView 不持久化或展示原始路径，也不接收数据库路径或存储密钥。Tauri 拖拽事件中的用户显式路径只允许作为 native import command 的瞬时参数，禁止进入 Pinia、DOM、response、日志、错误和持久化。
- R-011：附件从导入成功时起保留七个 24 小时。到期清除 Desktop 二进制和索引，保留安全名称、媒体类型、大小、内容块顺序、过期时间和 `expired` 状态用于消息历史。已经发送给 Runtime 的历史 rollout 不能在本期按附件单独追溯擦除；永久删除会话仍走既有 multi-surface cleanup。
- R-012：同一附件只能原子绑定一次消息；跨 owner/tenant、已绑定、已删除、解析失败或已过期附件不可发送。
- R-013：会话删除级联清除附件内容块、二进制、索引和 staging 记录，并沿用现有 checkpoint/cleanup 语义。
- R-014：生成的图片与文件展示及操作不在本期范围。

## 2. 可观察状态

`queued -> importing -> parsing -> indexing -> ready -> bound -> expired`

失败进入 `error_terminal`；用户移除未发送附件进入 `removed`，随后可通过统一加号或拖拽重新选择。

## 3. 验收标准

### AC-001 统一入口

Given composer 可用，When 用户查看底部操作区，Then 权限入口前存在一个 40px 稳定尺寸的加号图标按钮，名称和 tooltip 均为“添加图片或文件”，不存在第二个图片按钮。

### AC-002 选择与拖拽等价

Given 用户选择或拖入同一组支持文件，When native import 完成，Then 两条入口返回相同附件元数据、校验结果、解析状态和持久记录；绝对路径只可在拖拽回调到 native command 之间瞬时存在，不得进入 UI state、DOM、响应或持久化。

### AC-003 大小与格式拒绝

Given 文件超过 10 MiB、为压缩包/目录/宏文档，或扩展名与 magic 不一致，When 用户导入，Then native 层拒绝该项，消息未绑定，错误说明原因和恢复动作，其他已就绪项不丢失。

### AC-004 多模态发送

Given 文本、一个文件和一张图片均 ready，When 用户发送，Then 同一 user message 按顺序持久化三个内容块；文件相关片段与图片分别成为同一 Runtime turn 的 text/image input。

### AC-005 附件单独发送

Given 文本为空且至少一个附件 ready，When 用户发送，Then 发送允许且会话标题使用安全附件名派生的回退标题；没有附件且文本空时仍禁用发送。

### AC-006 原子性与失败恢复

Given Host 暂不可用或数据库提交失败，When 发送失败，Then 文本和未绑定附件保留；重试使用幂等 operation，不能创建重复消息或重复附件绑定。

### AC-007 历史持久化

Given 一条包含附件的消息已提交，When 用户重新打开应用和会话，Then 消息内容块、名称、类型、大小、状态和到期时间按原顺序加载，原始路径不出现在 IPC。

### AC-008 七天过期

Given 当前时间达到 `created_at + 604800` 秒，When 应用启动、加载历史或尝试构造 Context，Then 二进制与索引被清除，内容块变为“已过期”，且不可再发送给 Runtime。

### AC-009 删除

Given 用户删除含附件会话且现有跨表面 cleanup 成功，When Desktop 删除事务与 WAL truncate 完成，Then 附件 BLOB、chunks、message links 和 staging 数据均不可再由应用读取。

### AC-010 可访问与响应式

Given 亮/暗主题及 1180x760 窗口，When 使用键盘、VoiceOver 或拖拽，Then 入口焦点可见、状态不依赖颜色、名称长文本省略不挤压发送按钮、拖拽 overlay 不引发布局位移。

### AC-011 既有兼容与回退边界

Given 现有纯文本调用方和 v1-v5 历史数据库，When 升级到 FEAT-127 schema v7，Then v1 Host turn、`content` 文本投影和旧消息读取继续工作，升级不丢失旧历史数据。v7 是 forward-only；旧 Desktop 会拒绝打开 future schema，因此不支持在已升级数据库上原地降级。本地回退必须恢复迁移前的完整加密备份，或使用 v7 应用 roll-forward。对于未发布 v6 candidate，v7 保留已绑定附件历史，但会安全删除无法判定 composer 归属的 `ready` 草稿。

## 4. 错误和恢复文案

- 太大：“文件不能超过 10 MB。”
- 不支持：“不支持此文件格式，请选择常用文档或图片。”
- 压缩包：“暂不支持压缩包，请先解压后选择文件。”
- 解析失败：“无法读取此文件，可移除后重新选择。”
- 过期：“附件已过期，无法继续作为对话上下文。”
- 本地存储不足：“本机存储空间不足，请释放空间后移除并重新选择。”

## 5. 非功能要求

- 所有计数和解码均有上限；解析单文件最多输出 512 KiB 文本，Runtime 文件 Context 合计最多 256 KiB。
- 不记录正文、文件名、原始路径、base64、解析片段或图片数据；全局 Tauri 进度事件同样不得携带这些内容或完整附件 metadata。
- 测试仅使用合成 fixture。
- 本地可用是当前完成目标；生产部署、真实账户和付费模型调用不属于验收。
