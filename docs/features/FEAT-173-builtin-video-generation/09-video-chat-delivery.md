# FEAT-173 第2版补充：视频在对话流内预览、播放与保存

本补充属于第2版，不另立播放器方案。当前是源码审计与计划，**没有实现Seedance或修改产品代码**。已有播放器/Native存储/协议不等于Seedance链路已接通；必须完成下列生产者接线和端到端验收。

## 1. 当前已有与仍需补齐

| 环节 | 当前源码事实 | 本期还需完成 |
|---|---|---|
| D01 取得最终视频 | 现有媒体MCP仅有generate_image，没有Seedance生产者 | 实现两视频工具、原task ID查询；queued/running继续原任务，succeeded后进入视频交付。MCP返回一句话/URL/任务ID不算产物交付 |
| D02 下载与暂存 | Host有加密Artifact Store和content端点，支持video/mp4/64MiB | 新Seedance适配器从允许域取真实MP4 bytes，执行大小/格式初检、计算SHA-256、形成稳定安全文件名并暂存；不向模型或Vue输出供应商URL |
| D03 产物身份与事件 | publishV3会转发到现有媒体事件流；Native按活动runtime turn过滤事件 | 新视频生产者发正确的provider/video started/completed；首次交付绑定当前观察root，确保查询恢复后的新轮次可接收，不能把创建root ID误当交付turn |
| D04 Native接收与提交 | application.rs已有独立Artifact订阅、decode、ArtifactTransferService、SQLCipher提交与ACK | 在真实日常profile验证媒体流确实开启并收到视频；补供应商到原入口的集成用例，不新增Native下载/ACK体系 |
| D05 放入对话正文 | chat.store同时刷新ArtifactProjection与artifact reference；ChatPage按context/session/turn/artifact ID匹配后才挂组件 | 验证通知、刷新、双索引和本地ID映射贯通；产物先于文字、纯视频无文字、新轮取回都能进正确回答内容区，不能只在工具详情显示链接 |
| D06 预览播放 | ChatArtifactShell已在video+ready时挂ChatArtifactVideo；已有Native预览command、自定义协议、Range、WebKit控件 | 用实际Seedance默认MP4核对元数据、声音、播放、seek、尺寸适配及句柄释放。播放器和协议均复用，无新组件/外链播放器 |
| D07 保存 | 已有saveVideo调用Native保存面板、二次授权校验和原子写入 | 验证保存出的MP4大小/hash与Native已提交bytes一致，取消保存/失败重试不生成新视频 |
| D08 失败与完成判定 | 播放失败已有“重新加载”；通用ArtifactShell失败文案却会建议重新提交需求 | 必须最小修正provider/video交付失败文案，避免诱导重复计费；补从真实创建到播放保存的验收，不能只检查MCP成功 |

D01–D03是需要实现的生产者能力；D04–D07是已经存在但必须和新生产者一起验证的链路；D08包含一处已经由源码确认的必要前端文案调整。因此将原05的“Desktop零功能修改”改为“保留组件/协议/存储，允许本期明确的文案与有证据的接线修正”，不扩成新的前端状态机或恢复平台。

## 2. 必须连通的实际调用路径

```text
原生 MCP get_video_result（当前观察root）
→ Seedance同一任务 succeeded
→ Host下载真实MP4、校验并放入Artifact Store
→ publishV3 → publishMedia → 既有媒体SSE
→ Native open_event_stream_v3 → decode_artifact_event_envelope_v3
→ ArtifactTransferService.ingest_event / transfer_completed
→ Native SQLCipher提交ready → 原ACK
→ artifact_changed → loadHistoryV3
→ ArtifactProjection索引＋artifact_reference索引
→ ChatPage artifact-reference slot
→ ChatArtifactList → ChatArtifactShell → ChatArtifactVideo
→ 原生预览句柄／本地Range播放／原生保存
```

拉取/ACK继续使用既有Native→Host的鉴权；不混用media MCP token、bridge token或Ark Key。供应商HTTP Content-Type若是通用二进制类型，不能仅据该header判断可播，须在验证实际MP4字节后才以video/mp4进入产物链。

这些箭头均有现成入口，新增Seedance应接入它们而不是从MCP文本解析URL后临时造卡片。视频生产者自己完成Artifact登记；MCP回执应明确只需核对原Artifact状态，不要求模型再curl下载、保存到工作区或调用publish_artifact重复登记。

原生工具item和视频Artifact是不同对象：MCP RPC completed不代表视频可播放，视频也不应伪装成imageGeneration或额外助手正文。

## 3. Host产物接线细则

使用领域Event和原publishV3/publishMedia，不手写另一套SSE生产者或把视频塞进native trace事件。

| 数据 | 要求 |
|---|---|
| 身份 | artifact_id稳定；事件agent_session_id属于当前Host会话；turn_id是当前交付观察root的原生turn。video_operation_id仍指原创建root，仅用于任务归属 |
| started | kind=video、provenance=provider、status=in_progress、相同artifact_id/ordinal、明确安全名称（例如“生成的视频.mp4”） |
| completed | 原事件类型item.artifact.completed、status=ready、media_type=video/mp4、真实size_bytes/SHA-256及原`/v3/agent-sessions/{agent_session_id}/artifacts/{artifact_id}/content`；和started身份一致 |
| 顺序 | 暂存成功→持久handoff标记→started→completed→MCP staged回执；标记不等于成功。原事件发布失败不能返回ok/staged |
| 结束 | 不得先给MCP staged再在后台异步发产物；必须在当前媒体turn.completed之前完成事件发布。Native收到该媒体终态后会结束本轮产物观察 |
| 可选项 | ordinal走原媒体统一分配；不伪造进度。poster非必需，保持return_last_frame默认省略，不另生封面 |

Native的runtime turn与本地turn是不同身份。现有decoder接受两组ID并转换；前端artifact locator使用Native本地session/turn。不得直接把MCP的delivery_turn_id或原创建ID写进前端本地索引。必须验收“创建轮次A→停止/等待后在B取回→视频只出现在B”的真实映射。

默认日常媒体profile由Native名为open_event_stream_v3的方法选择schema 9；文件/文档profile选择12，未开媒体才是3。Host应沿原分发和header校验，不能因方法名含v3就硬编码只订阅v3，也不能把native对话事件版本当Artifact版本。新视频不依赖文档开关，默认文档关闭的日常入口必须通过。

## 4. 提交、可播放与ACK是不同事实

| 阶段 | 含义 | 前端能做什么 |
|---|---|---|
| provider succeeded | 供应商有结果，未必下载成功 | 显示真实工具状态，不宣称视频已交付 |
| Host staged | Host已有临时bytes，尚未证明Native提交 | 原传输状态/产物占位；不能仅凭MCP字段置ready |
| Native本地ready | bytes大小/hash等验证完成并写入本地存储 | 现有视频组件可预览/播放/保存，**不以ACK已成功为额外展示门槛** |
| Host committed | 原Host观察到合法Native ACK | 模型可据get_artifact_status确认已交付 |
| WebKit实际播放 | 真实MP4容器/轨道/编码在客户端可解码 | 才证明本次视频实际可播；不能用文件扩展名、ftyp或ACK代替 |

当前Native提交会校验大小/hash及基础类型头，读取预览时再做较完整MP4容器校验，最终codec解码仍由WebKit负责。方案不能声称现有提交检查已经完整验证所有Seedance编码。默认有声MP4必须实机播放；不兼容时走既有播放错误，不能静默调供应商参数或新增自动转码。

维持第2版恢复边界：Host重启后status可能unknown，Native本地ready仍可展示；不写视频专用ACK/manifest副本、不重建spool、不重发产物、不改Native已失败终态。

## 5. 对话流展示与播放器行为

需同时满足：

- Native ingest完成后发出artifact_changed；chat.store通过loadHistoryV3既更新artifact.store的projection，也更新artifactReferenceItems并重组timeline。只有其中一份数据会导致卡片缺失或只显示“生成内容”占位。
- ChatPage的authority/context/selectedSession、timeline item的本地session/turn和artifact ID全部匹配。切换聊天不得串视频，回到原聊天从已提交历史重建展示；不依据正文URL/文件名或供应商task ID猜绑定。
- 视频在同轮回答内容区占既有视频布局，复用原正文/产物顺序。无正文也有视频，正文稍后到达不重挂播放器或复制卡片。
- ready时现有ChatArtifactVideo会自动申请本地预览句柄并加载metadata，在对话内显示播放器；点击现有标题/播放控件开始播放。**直接预览不等于自动有声播放**，保持既有浏览器手势要求。
- 原video controls、进度拖动、音量、preload=metadata、playsinline和object-fit=contain保留。横竖/自适应比例不可裁切；没有poster亦可播放，不保证预加载metadata时已解码静态封面。
- src使用Native返回的yijie-artifact-video本地句柄，Range/HEAD由原协议处理，seek不访问供应商；不把大视频Blob放进Vue/Pinia，不改CSP或增加外部URL权限。
- 卸载/切换聊天/上下文失效时暂停并释放旧句柄，迟到open结果也释放。释放预览只影响本地播放，不创建/查询/删除供应商任务，也不等同停止另一个正在运行的Agent回合。

## 6. 保存与失败文案的最小改动

保存继续走chat_save_artifact_video_v1：main窗口/上下文/产物归属校验→读取已提交bytes→原生保存面板→再次验证身份/大小/hash→原子写入。默认.mp4文件名安全且与卡片一致。保存成功以真实落盘结果为准；取消面板返回cancelled并保留视频；空间/权限/扩展名错误按已有code提示，重试仍读取同一产物。

**已确认需调整的位置：ChatArtifactShell.vue的failureGuidance。** 当前只有provider/image特殊分支，video会落入“生成失败，可重新提交需求”。Seedance已成功但交付失败时这句话事实不准确，也会诱导再次付费。增加provider/video的最小展示分支，表达“视频交付未完成，请核对原任务或已有产物；重新生成会创建新任务”。已进入handoff的操作不承诺可补领，不新增“重新生成”快捷按钮。取消/过期/未知也不自动切换供应商。

播放失败原“重新加载”保留，仅重新申请现有本地句柄；不得绑定generate_video/get_video_result或CDN。供应商创建/查询失败在原MCP状态中报告，不能伪造成Native播放失败；播放器失败不能改写供应商任务failed。

## 7. 完成门禁：必须看到对话内结果

| ID | 验收内容 | 通过依据 |
|---|---|---|
| VD01 | 新Seedance成功结果走Host provider/video事件 | 同Artifact身份、真实字节/大小/hash、事件顺序正确；staged只在事件成功后返回 |
| VD02 | 默认日常媒体通道且文档关闭 | Native实际接收schema9并提交；schema12既有profile按需回归，不为视频额外开文档功能 |
| VD03 | 实时/历史的两份索引与轮次映射 | 对话内存在ChatArtifactVideo；无正文/正文迟到、A创建B取回、切换聊天均正确且无重复卡片 |
| VD04 | 实际默认视频可播放 | 元数据、声音、播放/暂停/seek、横竖画幅完整；不能只凭HTTP200或ready断言 |
| VD05 | Native保存 | 原生面板保存文件与已提交Artifact大小/SHA-256一致；取消保存和普通错误不丢产物 |
| VD06 | 本地重试与重开 | 预览重新加载、保存重试、切换聊天/正常重开已提交视频：供应商POST/GET/CDN请求均无新增 |
| VD07 | 生命周期与错误 | ACK暂时未确认时Native ready仍可播；失败/未知不诱导重生；预览关闭释放、旧句柄/旧异步响应不串上下文 |

集成测试从回环供应商结果经**真实Host视频生产者**进入Native，不手工seed Store，不只单测播放器。真实验收沿既有FEAT-173四次建议创建预算复用同一批结果完成VD01–07，不因此额外生成视频；尚须另行授权预算。日志只记录本地关联ID、byte size/hash和阶段，不记录Key、prompt全文或签名URL。

本补充未执行上述产品测试、真实生成或GUI操作。播放器与保存是已有能力；Seedance生产者、贯通验证及失败文案调整仍待实施。

本次文档检查：严格Feature Package、元仓lint与57项治理测试、Shell语法、diff及内部链接通过；7仓HEAD、原55源文件与16项交付链证据保持，6个业务仓clean。结果见references/video-delivery-checks.json，仅证明方案文档一致，不证明上述产品环节已实现。
