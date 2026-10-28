# FEAT-165 — 原生产物文件支持与统一预览

> 2026-10-28 · schema v3 · demo_fast / local · Owner：段成威
> **用户已接受并授权实施；2026-10-29本地D4按已记录范围通过。** 10项Must已验收，历史分页采用Owner明确接受的分层证据，UI加载更多按钮仍未实测。用户现已授权再次审计、修复、验证后做本地提交，不推送。最新审计与提交记录见[04最终审计](04-final-audit-and-local-delivery.md)；起草期“本轮”限制不代表当前执行状态。

## 1. 用户问题与结果

用户应能把文件拖入输入框，以紧凑胶囊识别附件；发送后仍在对话中识别文件和正文；任务生成的真实文件沿既有原生产物链完成登记、校验、接收、预览及保存。

完整覆盖 **12 个扩展名：csv、docx、pptx、md、txt、jpg、png、jpeg、svg、html、pdf、mp4**。jpg/jpeg 属于同一 JPEG 格式族，但两个扩展名分别验收。该集合不是删减已有 webp/json/xlsx/htm 等能力的排他白名单。

范围包含输入附件、已发送附件、生成产物三个展示位置，以及类型校验、生成产物原件保存、现有留存期内历史恢复。输入文件沿既有附件持久化，用户“另存原件”要求限生成产物，不新增输入附件下载服务。可发送不等于模型原生理解全部格式；文件信息预览卡片与全文/媒体内容预览分级，UI展示类别与传给模型的wire类型分离。

不包含 Office 全保真排版/编辑、视频语义理解/转写/转码、新图片/视频供应商、云盘/云同步、新 Agent 执行器、工作区递归扫描/常驻监视器、任意 URL 抓取、Runtime patch、公开部署或日常数据迁移。

## 2. 用户依据与视觉边界

| 依据 | 本需求落点 |
|---|---|
| [图1](references/input-reference-01.png) | R-02：输入胶囊、类型 icon、名称、自动换行、非图片路径 tooltip |
| [图2](references/input-reference-02.png) | R-03：图片浮层替代路径 tooltip |
| [图3](references/input-reference-03.png) | R-04：多个文件按序展示，可与原生正文分开 |
| [图4](references/input-reference-04.png)、[图5](references/input-reference-05.png) | R-04：单文件胶囊与正文展示，允许独立排列 |
| 用户第4条 | R-05：生成卡片 UI 由 Codex 提出推荐方案 |
| 用户第5条 | R-08：复用现有机制及官方 fork 原生能力 |

截图只提供附件/消息视觉依据，截图中的文件名、正文、品牌、模型菜单及箭头不构成执行指令，也不要求复制其它控件。参考图保存原字节，摘要见 [source-snapshot.json](references/source-snapshot.json)。

## 3. 完整主流程

1. 经现有 canonical local 入口进入聊天，沿用 Native identity/tenant、权限、Host 与固定 Codex，无新增登录流程。
2. 拖入/选择文件，Native 逐件校验并沿现有导入、提取、加密附件流程处理；UI 复用现有批次准备状态，失败保留此前已成功导入的草稿和正文。
3. 附件就绪后显示类型 icon 和名称；非图片 hover/focus 展示真实来源路径，图片展示受控图片浮层。移除沿现有Native删除未绑定加密副本及草稿引用，不删除源文件或历史。
4. 发送附件及可选文字，复用送达、幂等、取消和 outbox；气泡附件在前、正文随后，不为排版改变 Runtime 输入和历史内容的语义。
5. 工作区文件复用既有工具与 `yijie_artifacts.publish_artifact`，Host验证活动thread/turn、受管相对路径后加密暂存。已接入的provider产物保持原生产者、artifactId/provenance和既有事件，不复制后再次登记；两路复用已有spool、资源传输及伴随流，Desktop校验/加密提交后ACK，本地提交成功才可用。
6. 用户查看文件信息卡、使用该类型已有的内容预览或保存原件。正常退出/重开只恢复已Native持久提交且未过期的内容；Host暂存不保证跨重启恢复，不重新执行任务或从Runtime路径重建文件。

## 4. 业务规则与交互

### R-01 格式、能力与校验

扩展名大小写无关识别，名称保持用户可识别原貌；MIME、内容特征、结构校验共同判断，不能只扩前端 accept。类型 icon 依据 Native 确认类型；校验复用现有实现，只补缺失格式，不以模型正文猜文件成功。输出校验复用输入中已有的结构验证函数，但不能把输入文本提取自动当成已有输出阅读器。本期不强制增加Office/PDF文本摘录或模型总结。

| 扩展名 | MIME / 类型 | 输入给模型的最低语义 | 生成产物预览候选 |
|---|---|---|---|
| csv | text/csv / 表格 | 既有有界文本上下文 | 既有表格预览，明确截断 |
| docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document / 文档 | 既有 OOXML 文本提取 | 复用文件信息卡与原件保存，标明暂不支持内置内容预览；不新增Office阅读器 |
| pptx | application/vnd.openxmlformats-officedocument.presentationml.presentation / 演示 | 既有 OOXML 文本提取 | 同DOCX，不伪造幻灯片缩略图 |
| md | text/markdown / Markdown | 既有有界文本上下文 | 复用文本投影新增有界源码预览，不执行 HTML |
| txt | text/plain / 文本 | 既有有界文本上下文 | 既有纯文本预览 |
| jpg | image/jpeg / 图片 | 既有 image/localImage 适配 | 既有图片预览/缩放 |
| png | image/png / 图片 | 同上 | 同上 |
| jpeg | image/jpeg / 图片 | 同 jpg，合法扩展名别名 | 同 jpg；保存默认保留 .jpeg，不强改 .jpg |
| svg | image/svg+xml / 矢量图片 | storage/wire保持file，复用有界SVG文本上下文；视觉图片类别不转成栅格image输入 | 既有 FEAT-159 图片上下文预览/缩放 |
| html | text/html / HTML | 既有文本提取，不执行网页 | 既有隔离内置预览，自包含内联交互 |
| pdf | application/pdf / PDF | 既有可提取文本；无文本按现有导入规则提示 | 保留当前文件信息卡与原件保存，不新增摘录/页渲染/OCR |
| mp4 | video/mp4 / 视频 | storage/wire保持file；候选说明仅安全名称、MIME、字节大小及“未解析画面/音频”，语义须在现有文件上下文契约中明确扩展 | 既有系统播放器，H.264/AAC、音画/进度/暂停；不自动播放 |

SVG/MP4输入与MD输出文本投影为候选薄扩展。SVG用file身份提供源文本、按mediaType显示图片icon/hover；MP4也用file，不新增video ContentBlock。现有context_chunks原义是文件中的非空原文摘录，MP4附件说明不是摘录，必须在原输入权威源/适配及消费者中区分这一语义，不能仅加入video/mp4枚举就视为闭环。最低说明不需要时长/codec/尺寸探测、ffprobe、新依赖或转码器。不能称模型读懂音画，不把二进制当文本，也不伪造上游file/video输入。仅附件发送继续沿原规则，不自动代写新的分析指令。

输入沿用每消息最多 **10件、每件10 MiB、栅格image输入累计10 MiB**；提取文字512 KiB、file context累计256 KiB。SVG即使视觉为图片，仍消费file上下文限额及独立SVG预览资源限制。输入TTL从导入起7天，输出从Native本地提交起168小时；不混同起算点。输出沿用图片20 MiB、其它64 MiB外层容量及更严格类型校验；Host spool每session256 MiB/全局1 GiB/临时24小时。publisher活动turn内最多12次不同路径登记，Native另有turn总量12件边界，不宣称Host已统一所有producer计数；保留现有各边界及超限反馈，不新建配额服务。12输入可分批覆盖。

接收容量、结构校验、预览源准入、投影截断四层分开：现有文本预览源1 MiB是硬限制，超出则提示“内容过大，暂不支持内置预览”并保留有效原件保存；源已准入后才按256 KiB投影/行列上限截断并提示。64 MiB不是所有格式/内容都应通过的承诺。DOCX/PPTX复用OOXML主类型/主文档、512条目、单entry8 MiB、总展开32 MiB及压缩比100等既有边界，不扩限或仅看ZIP magic；MD/TXT/CSV按既有UTF-8/NUL策略，不执行CSV公式。

### R-02 输入框胶囊

- 复用易界 tokens、YjIcon registry 和弹层组件；浅灰/暗色对应背景、全圆角、类型彩色 icon、文件名。11格式族可区分，jpg/jpeg共享 JPEG icon；不引入第二图标库。
- 按添加顺序左到右自动换行；推荐高度32–36px、间距6–8px，从现有tokens取最近值。长名收缩/省略但扩展名可辨，完整名称有可访问说明，不撑出输入框或挤走发送按钮。
- 非图片 hover/focus 显示真实来源完整路径，允许换行。无可证实路径显示“来源路径不可用”，不能拼造缓存路径或工作区地址。
- 来源路径展示是用户已明确要求的产品变化，构成旧FEAT-127禁止路径进入DOM规则的限定修订；不重复索取同一产品需求的许可。当前无现成来源路径字段，须沿既有导入结果/身份与draft授权补最小临时展示能力，不预先另建路径管理器、通用文件查询API或每次hover读盘机制。值仅当前草稿、当前上下文内有效，不作为读盘权限，不进入模型、Host wire、日志、遥测、全局Pinia或持久消息；发送/移除/切换/权限失效时清除。App重开后来源路径恢复不在本期，不为此加持久字段，未知时如实说明。
- 类型icon在hover/focus可于固定槽切换移除按钮，不能抖动；有可访问名称及键盘入口。移除沿现有流程清理该未绑定加密副本和临时路径/句柄；Native删除失败保留草稿并显示错误，不删源文件、同名其它文件或已发送历史。

### R-03 图片 hover

png/jpg/jpeg/svg hover/focus 显示图片浮层，替代且不同时出现路径tooltip。保留比例不裁切，推荐最大320×240px并受窗口可用区域约束；优先向上，不足时翻转。SVG复用安全图片上下文，不插主DOM、不进HTML执行窗。

当前附件只有pick/import/list/remove，没有现成附件内容预览API。应共享已有图片有界解码和租约安全原语，仅补受attachment/draft/context绑定的最窄读取与释放，不把artifact locator冒充attachment身份、不复制图片服务或另建文件服务器。仅按需申请、同时最多一个活动浮层；鼠标离开胶囊与浮层、Esc、移除、发送、换会话/关闭时释放。焦点操作与hover等价。加载中明确反馈，失败在图片浮层显示原因及适用重试，不退成路径tooltip。图片原件有效而预览失败可发送；内容校验失败不能发送该引用。MP4 hover不播放。

### R-04 已发送用户消息

单件展示胶囊及后续文字，允许附件与原生正文独立排列；无文字只有胶囊。多件按添加顺序流式换行，正文与文件组留合理间距，不产生重复正文或附件。发送后无草稿移除按钮。

必须覆盖“本地提交可见→观察到native userMessage→正常重开/分页”三个阶段。2026-10-28用户执行中明确修订：不得改变原生userMessage类型，文字与文件不强制同气泡，可参考新增图6独立排列。保留composeConversationView既有原生Item与本地attachment_reference两类记录；仅在视图层展示原本已按session/turn/本地message绑定的产品附件，不向原生Item追加附件、不改类型或回写wire顺序。本地原文在尚未观察到native userMessage时保留；观察到后保留原生记录不变；存在唯一且明确的本地session/turn提交绑定时，视图显示本地提交正文及独立附件记录，避免把Host附加的模型文件上下文包装展示成用户正文。纯附件只显示附件行；绑定缺失或存在多个原生userMessage时不替换或猜关联。不得用正文、ordinal或时间邻近猜关联，不新增会话状态机/历史重建。只有冷Runtime历史而缺本地绑定时如实降级，不冒称具有本地附件。已发送区不增加来源路径tooltip，过期/缺失胶囊仍保留。

### R-05 生成产物卡片（Codex推荐）

复用 `ChatArtifactShell/List/File/Image/Video`：随消息容器伸缩的单列卡片；首行“类型icon + 文件名”，次行“类型 · 已知大小 · 状态”，下方类型预览，内容预览可用时主操作“预览”、次操作“保存原文件”；只有文件信息卡时以“保存原文件”为主，明确“暂不支持内置内容预览”，不提供必失败按钮。按现有伴随流首次观察artifactId的合并ordinal展示，保留旧producer原ordinal，不按工具返回/文件名字典序重新裁决，不因正文链接或重复登记造第二卡。

- TXT/CSV复用内容投影；MD只扩现有有界文本映射。DOCX/PPTX/PDF使用文件信息卡＋原件保存，继承既有save-only模式；不强制新增输出projection、文本提取展示或Office/PDF阅读器。类型/大小/就绪/保存是真实可观察结果，不能把卡片称为全文预览。
- 图片/SVG保持比例缩略图及既有放大；视频使用poster或占位和显式播放，不因入流/hover播放；关闭或切会话正常停止播放和释放租约。
- HTML进入既有无宿主IPC的隔离内置窗，保留自包含内联交互，禁止外网、任意磁盘、持久网站存储；不放宽CSP/权限。
- 接收中按真实阶段反馈，无原生百分比则不定进度；ready/failed/cancelled/expired沿用原状态。预览loading/error属于展示状态，不反写Turn终态。
- 原件已提交而预览超限/失败/codec不支持时，明确原因并保留有效保存入口。12格式都有完整预览卡片，但内容预览能力严格按R-01分级，不以卡片存在冒称全文或音画成功。

### R-06 保存、留存与恢复

区分“Host staged”“Native持久提交ready”“用户另存原件”：ACK只能在Native校验/提交之后；Host收到ACK会释放spool，ACK失败沿既有pending ACK恢复，不撤销已提交文件，也不新建可靠投递服务。另存只用于生成产物，复用范围授权、rfd/macOS对话框、目标校验和atomic保存；覆盖确认属于原生对话框，atomic rename本身不是第二批准协议，不加自建二次弹窗。默认使用既有安全名称和合法后缀；补.jpeg别名不转码、不改变原件字节。取消不算错误、不记保存成功。

导出与完整接收原件字节/摘要一致，基准不是预览投影。输入hover依attachment身份，生成预览/保存依artifact身份，均不接收renderer任意路径。用户另存原件独立于应用TTL。只保证已Native提交资源在保留期内正常重开；未提交内容若Host关闭/重启、spool或内存stream重放窗口失效，沿既有expired/unavailable/stream错误反馈，不承诺自动补领，不从原路径或Runtime历史重建、不自动重跑模型。过期/缺失不抹掉历史，重新提供须用户明确操作。

### R-07 其它状态与边界

| 场景 | 行为 |
|---|---|
| idle/empty | 保持空草稿提示；无文字无附件不发送；无产物不显示空卡片 |
| loading | 复用现有批次准备、真实产物接收、独立预览加载；胶囊标识未就绪，不造百分比 |
| success | 附件ready可发送；Native提交成功产物才ready；保存结果另行反馈 |
| error/permission denied | 保留正文和此前成功草稿；使用现有可理解错误，不要求新增逐文件错误协议；不提权、不把路径输出到日志 |
| partial/limit | 复用原子批次导入：超数量整批在读取前拒绝，批内校验失败不提交半批；保留此前成功批次和正文。生成端多产物独立状态如实显示，不抹掉已成功产物 |
| timeout/retry | 复用现有超时/重试；导入失败仍“移除后重新选择”，不新增原地重试；传输/预览沿既有可重试语义，不自动重跑任务、不建新循环 |
| cancel/remove | 保存取消正常返回；移除不删源文件；任务取消尊重Runtime事实，已提交产物不凭空抹除 |
| duplicate/concurrent | 沿用operation及文件身份；publisher键为session/turn/relativePath，SHA/展示名/MIME一致才返回原receipt；同路径内容或展示名变化是冲突，不覆盖原卡，需另存新路径再正常登记；终态清注册，不承诺跨Host重启永久幂等 |
| recovery | 正常重开复用加密历史和引用；旧格式继续可读，无路径/过期如实显示，不回填猜测事实 |

基础交互适配现有亮暗主题、最小窗口、键盘焦点/Esc，不仅以颜色表状态。预览懒加载，复用虚拟化/资源上限，不为hover一次读入所有MP4/大文件。这里是本期附件基本可用性，不重启FEAT-164已经移出的独立外观专项。

## 5. Must验收标准（结果见02第11.1节及04最终审计）

| AC | 可判定结果 | 验证方式 |
|---|---|---|
| AC-001 | 12扩展逐一真实导入/识别/发送和产物接收；普通/已选工具/专家聊天输入契约一致，旧格式与既有producer保留 | 普通安全样本分批走实际入口与Runtime登记，至少一项现有工具生成任务闭环；不要求12种生成引擎或新增付费供应商 |
| AC-002 | 输入胶囊/icon/名称/换行、非图片真实路径tooltip及局部移除成立 | 单多件、中文长名、同名异路径、无来源路径；鼠标/键盘；路径不进模型/日志/持久消息 |
| AC-003 | png/jpg/jpeg/svg图片hover/focus取代tooltip；正常关闭/移除/换会话释放；MP4不自动播放 | 四图片扩展逐项普通样本和正常生命周期 |
| AC-004 | 单胶囊+正文、多文件、无文字在本地提交/native观察/历史分页重开均正确展示（可独立排列），原生userMessage不变、无重复；无本地绑定的冷历史不猜关联 | 图3—5与真实已有绑定核对；覆盖新普通和已有专家聊天，不重排wire/原生Item或重发 |
| AC-005 | 12格式预览卡片分级准确；DOCX/PPTX/PDF文件信息和保存可用，TXT/CSV/MD有界内容、HTML交互、SVG缩放、MP4音画/seek及关闭正常 | canonical App按R-01逐项；超预览源限额说明且可保存，不以卡片/metadata代替内容或音画 |
| AC-006 | 12扩展名原件保存字节一致、.jpeg合法命名、取消/同名确认正确；预览失败不误阻有效保存 | 原生保存与SHA-256/字节比较；正常取消，不破坏文件制造失败 |
| AC-007 | 已Native提交的附件/产物在保留期内正常重开，未提交/过期/缺失如实反馈，不承诺Host重启重投递或自动重生成 | 正常重开真实UI必验；过期/缺失优先自然记录，无记录则以普通纯值reader/组件状态检查验证，不改时间/权限/数据库；仍无覆盖则本AC不得PASS |
| AC-008 | 混合批次、正常超限/不支持/拒绝/取消及重试可恢复，正文保留且无重复派发/伪终态 | 10件/超限普通文件、正常不支持类型、取消重选；不用攻击样本 |
| AC-009 | 固定Runtime、已有生产者/登记/spool/ACK/预览保存复用，完整输入包装与历史reader兼容；新值只向能消费的端发出 | source-first及同源校验，旧生产者混合/登记幂等/无重复卡；保留既有受支持模型配置，不在K31开启被禁dynamic tools |
| AC-010 | 当前主题/最小窗口/键盘可完成胶囊和卡片关键动作，资源正常释放，无路径越权扩散 | focused组件+真实UI正常观察/关闭，不做攻击注入或强杀 |

## 6. 工程与契约边界

代码依据和Git来源见[01-delivery-log.md](01-delivery-log.md)。**需求起草阶段文档变更contract-impact=none**；**完整功能按breaking实施和评审**，现有输入和媒体闭集、持久reader、新格式和.jpeg保存语义、路径显示边界未经方向验证，不能以JSON形状相同判none/additive。

### R-08 不重复发明

1. Runtime复用Thread/Turn/Item、MCP/元数据、工具调用、权限、取消、read/resume。publisher已由thread/start和thread/resume的artifactThreadConfig注入，旧专家沿同一resume，不新增developer提示编排、MCP注册器、dynamic tool或专家专线。mention/TextElement不是文件传输/读盘授权；Runtime ImageGeneration.saved_path在Host尚无接纳链，不因上游源码有字段就自动读盘。禁止由正文/FileChange/stdout路径推定产物ready。
2. 工作区文件复用FEAT-159 publisher，已有provider输出沿原生产者进入同一spool/v3事件/media伴随流/content/Range/ACK，不要求二次publish。现有generate_image仅在其已支持配置中适用；Kimi K31候选禁止DynamicToolsEnabled的约束保持，不能借格式需求重新启用。保留旧producer及历史不等于所有当前模型都能运行它。不新建上传服务/扫描器/第二文件库，不建设12类生成器。
3. 输入复用Native import、OOXML/PDF/文本提取、加密附件/outbox；SVG/MP4薄适配，不把Runtime mention冒充通用文件协议；input-only计划草案仍禁工具/非文本，不扩散本期能力。
4. UI/保存复用现有组件、图片租约、HTML隔离窗、系统播放器、文件预览、原子保存；输入预览共享安全原语但保留attachment/draft授权身份，不伪装generated artifact。
5. 拟新增逻辑先列“现有入口→实证缺口→最小扩展→复用验证”。已支持直接接入；既有存储MIME为TEXT且有file/image、chunks/BLOB，不预定新表/路径持久字段。旧reader闭集风险单独审，必要时仅沿既有前向reader guard/migration机制。确需Runtime核心/patch另呈方案，本需求不默认授权。

source-first影响清单不能只含媒体枚举：Contracts的AgentHost StartTurnV2、chat/message历史metadata、market-selection身份提交、market-host不可变submission/HMAC、experts引用包装都要按同一输入来源核对；不得只修普通聊天而漏工具选集/专家。Desktop私有附件源`src-tauri/schemas/chat-ipc-v2.schema.json`及其Rust/TS消费者也必须同步；它既不归公共media generator，也不能以Contracts示例代替。输出公共media源与其v3→v9派生生成器、Desktop私有preview/save IPC源及实现一致性分别验证。私有file-native schema当前未列HTML而实现已支持，是既有漂移，实施时已随该表面同步收敛，不扩成全仓治理重构。详见01权威矩阵。

输入provider先支持新语义/值再发送，输出兼容reader或明确版本准入先就绪再发新值。当前只有显式版本路由，未证明按MIME动态协商；复用既有生成/来源绑定/路由，按方向兼容结果决定最小新版本或准入，不预占版本号，不新建协商框架，不原地扩旧闭集向旧端发新值。旧数据→新reader、新数据→回退reader或明确拒绝降级分别证明；不能因表能存就称兼容。不手抄DTO/手改生成物。若确实触及Runtime协议，Runtime canonical schema先行→Contracts投影→consumer，当前方案不需要此改动。需求起草阶段未运行生成器；实施后的生成物同源检查及限制见02和04。

## 7. 决策取舍与实施停止条件

| 决策 | 推荐及理由 | 未选方案 |
|---|---|---|
| Office/PDF预览深度 | 按用户“预览卡片”保留文件信息＋原件保存，不加内容阅读器 | 初稿强制文本摘录是额外设计，本轮移除；全文渲染/编辑不在本期 |
| SVG/MP4输入 | file身份与视觉分类分离；MP4仅已知描述信息并明确契约语义扩展 | 新video类型、ffprobe/转码/假image输入均不必要 |
| 路径显示 | 按用户明确要求限定修订旧Pattern，复用导入/draft身份提供临时值 | 新路径库/通用读盘API及全链传递不必要；仅文件名不满足要求 |
| 格式扩展 | 既有源契约/校验器/reader扩展 | 新传输/影子DTO重复建设且破坏旧consumer |

默认demo_fast/local仅规划个人本机非敏感样本，不授权访问/迁移/回退当前日常重要数据。若实施确认必须迁移重要持久数据、改变保留/删除、安全或不可逆职责，先显式选择production_hardened并给出方案，不能借FEAT-164/ADR-0022既有批准。样本限公开/合成数据。需求起草阶段预算为0；后续Owner已明确追加真实任务至20次，已用7次，外部MCP/生成供应商和生产写入仍不在授权范围。

需求起草阶段曾停在需求审计；后续Owner已接受需求并明确授权开发和真实验证。本次仅按既有授权范围审计修复，保持版本/reader兼容、原生消息展示绑定与最小附件预览边界。D0来自Owner明确接受，不能用文档或Agent审阅替代。

未来30分钟无新事实查真实输入/登记/ACK/预览链，90分钟同阻塞简化非核心视觉，核心240分钟或总16小时仍不通则呈报范围/方案调整，不删减12格式/原件保存Must造完成。退出一律走应用正常清理；强杀、二进制劫持、权限破坏、恶意资源/攻击fixture永久禁止。未执行项单列原因与影响，不伪造PASS。
