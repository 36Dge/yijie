# FEAT-165 调查、复用方案与需求审计

前6节为2026-10-28两轮需求审计历史，当时仅调查和写需求。后续Owner接受D0并授权实现、验证及Contracts本地提交；当前2026-10-29本地D4已通过，Owner现已授权最终审计修复、验证后本地提交，不推送；最新入口见04，03及02第11节保留前序验收。Agent审阅不等于独立人工批准。

## 1. 上下文与来源

依据元仓AGENTS、repos.yaml、codex-project-memory需求起草协议、Contract First、双Profile治理、ADR-0013/0017/0018、各仓规则和FEAT-127/159/164事实。FEAT-164的执行许可/额度及ADR-0022不移用。第二轮由Runtime/Host、Desktop、Contracts三路独立只读审计，主Agent交叉核对并修订。

| 仓库 | 当前branch | 第二轮HEAD | 当前状态 |
|---|---|---|---|
| yijie | chore/retirement-baseline-20260905 | 2e21790873cb3f824e03632fcec2b8da640dd8ae | 仅本需求目录untracked |
| yijie-desktop | feat/feat164-primary-20261028 | 0247b7cfbe3a4a2020a29417d96b8a5718b3923d | clean |
| yijie-agent-host | feat/feat164-primary-20261028 | 20539889259587a66a574201e521c2ea9469c54d | clean |
| yijie-contracts | feat/feat164-primary-20261028 | 2adfa2bef43d38a932f6249dbb0a229c173ff103 | clean |
| yijie-codex | chore/retirement-baseline-20260905 | 11fd4504c28afd0f65c6f5f62a6b5328dd437f5a | clean |

origin与repos.yaml匹配；Codex upstream为openai/codex且push禁用。第二轮修改前四份文档摘要、分支/远端/状态见[reaudit-source-snapshot.json](references/reaudit-source-snapshot.json)。行号绑定本表HEAD，只证明当前代码存在，不证明本轮功能验证。

初轮元仓HEAD为7552f097367ea68cd12b502f8fa065ae84a67f43；FEAT-162三项dirty在初轮被并行工作推进为当前2e217908提交（六文件均属FEAT-162）。本任务未修改/暂存/提交或回滚这些内容。原始快照[source-snapshot.json](references/source-snapshot.json)、初轮[documentation-checks.json](references/documentation-checks.json)保留原时点。五张用户参考图不改字节，内容只作视觉依据。

## 2. 真正复用的链路与必要增量

### 2.1 Runtime与Host：保留生产者，不另建执行链

| 能力 | 当前事实/路径 | 本需求处理 |
|---|---|---|
| 原生输入 | Codex `codex-rs/app-server-protocol/src/protocol/v2/turn.rs:289`有text/image/localImage/skill/mention；Host `internal/codex/session_protocol.go:166`消费text/image | 没有通用file/video UserInput；沿Host文件上下文适配，不改Runtime |
| mention/TextElement | Codex `codex-rs/protocol/src/user_input.rs:47`面向结构目标/文本span | 不拿mention或TextElement做文件传输/任意读盘或为胶囊修改上游wire |
| MCP身份 | Codex `codex-rs/core/src/mcp_tool_call.rs:577,1083,1127`提供thread/turn metadata；Host `artifact-mcp/src/main.rs:74`读取 | 不信模型参数选择thread/turn；不再建身份推导 |
| publisher发现 | Host `internal/codex/session_protocol.go:579,656`，`internal/codex/artifact_media.go:18`，`artifact-mcp/src/main.rs:47` | 已有start/resume配置与tools/list说明；普通/旧专家复用，不加prompt编排/注册器/专家专线 |
| 工作区文件登记 | Host `internal/session/artifact_media.go:103,118,148,175,200`：活动turn、非draft、受管cwd根、普通文件、摘要、白名单 | 仅补md/docx/pptx映射和校验；保留同一MCP adapter、登记与暂存 |
| 已有图片producer | Host `internal/session/provider_image.go:137,182,214,227`，`internal/session/artifacts.go:131`已有generate_image→spool→v3→media伴随流 | 保留artifactId/provenance/原生产者；禁止复制后再次publish、重复卡片 |
| 模型适用限制 | Host `internal/codex/runtime.go:109`禁止KimiK31Candidate与DynamicToolsEnabled并用 | 保留旧MiniMax图片链/历史，不代表本期在K31开启dynamic工具；不以复用为由破坏配置限制 |
| 上游ImageGeneration | Codex `app-server-protocol/src/protocol/v2/item.rs:915`和`ext/items/src/image_generation.rs`有result/saved_path；Host `internal/codex/native_conversation.go:62,81`未接纳该产物类型 | “源码有字段”不等于端到端可用；不新建自动读盘producer来填补未要求能力 |
| 终态与正常退出 | Host `internal/session/service.go:1246`清登记；adapter `artifact-mcp/src/main.rs:190` EOF/shutdown | 不新建执行生命周期/强杀清理；input-only草案继续禁非文本和工具 |

### 2.2 登记、接收、ACK、恢复的真实语义

- publisher幂等键为session/turn/relativePath，内容SHA、displayName、MIME都相同才返回原receipt；同路径变内容或名称为冲突。终态清注册，Host重启不是永久幂等窗口。不设计覆盖更新/修订协议；需要不同内容时正常生成新路径。
- `artifact_media.go:50-74`只为伴随流按首次观察artifactId分配合并ordinal，旧producer ordinal不改。UI沿既有合并次序，不能按工具返回或名称猜新顺序。
- publisher的12件限制只计算其登记；Native另有每turn总量限制。不能把它写成Host所有producer统一计数，也不借本需求新建跨producer配额服务。
- `internal/artifact/store.go:245,263-298`：ACK成功立即expire spool，同AckID/参数可幂等返回；`OpenStore:138`重启清旧spool；`internal/session/events.go:299-323`的内存stream有重放窗口/新stream错误。Native已提交资源独立保留，pending ACK沿既有恢复。未提交就丢失Host暂存不能承诺补领，不从Runtime历史或源路径重建，不自动重新生成。
- 复用现有v3 content/poster/Range/ACK与media伴随事件；`internal/app/app.go:879`是显式v9路由，没有已证明的任意MIME动态协商。新格式兼容先按源契约与旧consumer事实决定最小版本/准入，不新增协商框架。

### 2.3 Desktop：展示组合、预览、保存

| 能力 | 当前事实/路径 | 最小需求增量 |
|---|---|---|
| 输入导入 | `src-tauri/src/chat/attachment.rs:122,163,218,239,457`，`chat/ipc.rs:8099,8168` | 原子批次pick/import/准备/持久化不变；12目标缺SVG/MP4，失败移除重选 |
| 类型与内容 | `chat/database.rs:3759-3845`按kind选择File(context_chunks)/Image(data_url)，`chat/host_bridge.rs:2190`栅格image闭集 | SVG/MP4用file；视觉icon/hover由mediaType派生，不能把SVG作为栅格data URL |
| 最小MP4说明 | `database.rs:3785,6560`要求file非空chunks；视频准入`artifact_video_native.rs:1615`不做codec解码 | 仅安全名称/MIME/字节数及未解析音画说明；区别于原文摘录，不加时长探测/ffprobe |
| 结构验证复用 | `attachment.rs:592,597,1199-1270`有PDF/OOXML验证；`:1146`为输入提取 | Office输出复用preflight校验，不要求调用提取器生成阅读面；Host跨语言边界用同源策略/普通conformance最小落实 |
| 草稿UI | `src/components/chat/ChatComposer.vue:116,385,775`为两列卡片；`src/domain/chat-ipc.ts:239`无路径/bytes | 胶囊、类型映射与临时路径显示是必要增量；保持输入操作/状态顺序 |
| 附件hover读取 | `src/api/chat-client.ts:124-127,579-597`和`src-tauri/src/lib.rs:457`只有pick/import/list/remove | 没有现成attachment-preview API；共享图片解码/租约安全原语，补最窄draft受权读取，不用artifact locator或新服务 |
| 已发送真实组合层 | `src/domain/conversation-view.ts:399-439`保留本地attachment_reference，但native userMessage只从item.text生成；`ChatPage.vue:1239`仅slot | 必须在已有视图适配按明确绑定组合native正文和本地附件；不能仅改单slot，不靠正文/邻接/ordinal猜关联 |
| 已有消息来源 | `src/stores/chat.store.ts:1763,2736,3559`→`src/api/chat-approval-adapter.ts:140`→`src/api/chat-conversation-adapter.ts:137,280,430`→conversation-view→ChatTimeline/ChatTurnGroup→`src/pages/chat/ChatPage.vue:1239` | 覆盖本地提交/native观察/历史分页；无可靠本地绑定则如实降级，不造native Item或回写历史 |
| 文件卡内容能力 | `ChatArtifactFile.vue:33-41`仅TXT/CSV/JSON内联，PDF/XLSX save-only | DOCX/PPTX沿文件信息卡＋保存，PDF保持原模式；MD薄扩有界文本，不新增Office/PDF摘要/阅读器 |
| 文本预览限制 | `chat/artifact_file_native.rs:26,208,928`源1MiB硬准入，投影256KiB、响应512KiB及行列限制 | 接收/保存与预览分开，超源上限不读全量再截断，只说明并保留保存 |
| 图片/视频/HTML | `ChatArtifactImage.vue`、`ChatArtifactVideo.vue`、`chat/artifact_media.rs:18,164` | 复用图片/SVG上下文、opaque handle、controls/Range、Wry隔离窗；不新播放器/预览宿主 |
| 真实接线 | `src-tauri/src/lib.rs:512`、`chat/host_bridge.rs:981`、`chat/database.rs:960` | FEAT159真实存在，新增格式沿原接线，不重建伴随流 |
| 保存与JPEG | `chat/artifact_native.rs:803,857,863,927`；file native`:949,1086` | .jpeg合法别名只改默认名/目标验证，不转码；沿原生dialog覆盖确认＋atomic rename，不新二次确认/下载服务 |
| 图标 | `src/icons/registry.ts:139`已有YjIcon/Lucide registry | 扩格式映射和token；不加另一图标库 |

来源路径是用户明确要求，仅限定修订Desktop `docs/design/docs/design/05-patterns/13-feat-127-chat-attachments.md:43-44`禁止路径到DOM的旧规则；不视为读取/上传授权。不为同一已明确产品要求再索批；实施时同步Pattern和局部IPC边界。该Pattern:66原文字在前仍保持wire语义，视图另行组合。路径与hover借既有context/draft/operation，过期或切换清临时值，不加路径持久字段。

## 3. 权威源、派生与全部消费者

目标功能仍保守breaking：新增闭集与MP4上下文语义、旧reader、新展示/保存行为需要方向验证；本轮仅文档影响none。没有确定新版本号、tag或批准的migration。

| 边界 | 必须核对的源/派生 | producer / consumers与顺序 |
|---|---|---|
| 文件输入正文 | Contracts `openapi/agent-host/agent-host.yaml:529,2598-2611` StartTurnV2/file context；Host `internal/session/multimodal.go` | Native发输入→Host接受/适配→Runtime text/image；provider先接受新语义再发 |
| 历史附件metadata | Contracts `jsonschema/chat/message.schema.json:43-100` | Native持久/历史投影与renderer闭集一起核对；不要只改实时提交 |
| 工具选集输入身份 | Contracts `compatibility/market-selection-v2/wire.schema.json:49-94` | 复用attachmentId与file/image身份，不新增video类型 |
| 不可变提交 | Contracts `compatibility/market-host-v2/wire.schema.json:50-121`引用StartTurnV2并将完整contentBlocks纳入submission/HMAC；`scripts/generate-market-host-v2.mjs:44-51`生成闭集 | 同一来源贯通Native/Host，不能重新包装或绕过原submission/HMAC |
| 专家包装 | Contracts `compatibility/experts-v2/wire.schema.json:37-50`引用market提交/回执 | 普通/已选工具/专家共享来源；不用专家专属附件通路 |
| 公共产物媒体 | Contracts `jsonschema/artifact/media-v1.schema.json`；`scripts/generate-artifact-media.mjs:14-26`从v3派生硬编码v9 | source→生成policy/事件/DTO→Host/Native reader；旧consumer未就绪不发新值 |
| Desktop私有附件IPC | `src-tauri/schemas/chat-ipc-v2.schema.json:1-27,85-107,350-402`为Desktop-owned源，覆盖pick/import/list/remove及attachment/file/image闭集；`src/domain/chat-ipc.test.ts:150`有同源检查 | Native `chat/ipc.rs`与renderer `src/domain/chat-ipc.ts`为消费者；新SVG/MP4及临时展示边界须核此源，不由公共media generator代管、不复制第二套输入DTO |
| Desktop私有预览/保存 | `src-tauri/schemas/chat-artifact-file-native-v1.schema.json`等现有Native schema与相应Rust/TS parser | 不是公共media源的同一生成物；各自同源一致，不为每格式新建command |
| Runtime协议 | 固定yijie-codex canonical schema→Contracts兼容投影→Host | 本期无改Runtime的证实需求，不从易界产品schema反改上游 |

生成/同步继续沿现有入口：Contracts `scripts/generate.mjs:270,328`处理普通OpenAPI/消息SDK；`generate-market-selection-v2.mjs`、`generate-market-host-v2.mjs`、`generate-experts-v2.mjs`及各family source.lock，使用`sync-model-call-surfaces-v2.mjs`的既有同步；Desktop `scripts/check-agent-host-contract.mjs`核普通输入来源。媒体仍走`generate-artifact-media.mjs`；私有附件/preview/save由所属schema与Rust/TS同源测试核对，不复制公共生成链。仅更新实际受影响来源，不无条件改旧v1锁。本轮这些入口全部未执行。

已有漂移：私有file-native schema尚未列HTML save MIME/extension，但Rust实现已支持HTML。需求登记此事实；未来修改同一预览/保存表面时收敛其源/实现检查，不能以旧漂移为理由忽略MD/DOCX/PPTX，也不扩大成全仓schema重写。

当前是显式版本路由，不是通用能力发现。复用生成器、版本入口、来源锁及reader机制；兼容结论决定是否需要最小新版本或固定候选准入。旧端可能误解时不得原地扩旧闭集硬切；公共DTO不手抄、派生物不手改。

## 4. 数据、边界与最小方案

- 输入10件/件10MiB；栅格image累计10MiB，file context累计256KiB。SVG走file上下文而非image总量分支，其预览仍受SVG/图片资源限制。
- 输出图片20MiB、其它64MiB只是外层上限；Office原有512条目/单entry8MiB/展开32MiB/压缩比100、图像像素、视频容器等限制仍适用。文本源超过1MiB不提供内容预览；投影截断为不同层。
- 输入TTL从imported_at起7天；输出从local_committed_at起168小时；Host临时spool24小时且ACK/重启会提前释放。保存到用户目标的原件不受应用TTL管理。
- Desktop `0006_chat_attachments.sql` MIME为受长度约束TEXT、kind为file/image；`0008_chat_output_artifacts.sql` MIME为TEXT。现有表/chunks/BLOB可承载候选，不预定新表、路径字段或第二文件库。
- SQL列可容纳不等于旧reader可解释；`0036_artifact_media.sql`是已有前向reader guard示例。YAML的expand仅保留可能需要沿现有机制加reader guard的风险分类，不是必须新增迁移/列。若无需guard即收敛为none须有兼容证据；重要日常库迁移另定具体范围/profile，不能用本需求稿自动开放。
- scope.auth_permission_change=none表示不扩大文件读取/身份权限，不表示路径披露不受审查。路径只临时显示安全选择来源，不进模型、普通日志、全局store或历史。

未来整体实现顺序：实际源与消费者影响/兼容设计→适用生成/普通conformance→provider输入与产物接纳→兼容Native reader/必要最窄附件读取→现有视图组合→整体验证。不是治理切片。无证据不得新建Runtime机制、存储、协商框架、预览器或生成服务。

真实入口已只读识别：Desktop `tauri:demo-fast` / `tauri:demo-fast:app`调用`run-local-demo-fast.sh`，当前`daily:open`调用`feat164_primary.py open`。本轮未运行；后续按实际数据授权选择canonical入口，不另造第二测试产品App、不直接开日常库试错。已有预算不移用。

## 5. 第二轮审计发现与需求修正

“已修正”只指文档，不指产品实现。发现均已同步00、YAML和02计划。

| ID | 初稿遗漏/冲突或过度设计 | 当前修正 | 状态 |
|---|---|---|---|
| R2-01 | 全部产物强制publish会重复已有图片producer | 分开工作区publisher和已有provider入口，共享接收，保留模型适用限制/ID/provenance | 需求已修正 |
| R2-02 | 只查附件slot，漏native正文与本地附件独立记录 | 明确视图适配组合及提交/观察/分页三态；缺绑定不猜 | 需求已修正 |
| R2-03 | SVG视觉图片被误推成wire image；MP4“元数据”无范围 | file身份与视觉分类分离；MP4仅已知描述，明确不是原文摘录且须源语义扩展 | 需求已修正 |
| R2-04 | 输入只列Host OpenAPI，漏历史/market/专家/HMAC | 补完整引用消费者矩阵，不建新输入通道 | 需求已修正 |
| R2-05 | 强制新增Office/PDF文本摘要/阅读面 | 使用文件信息预览卡＋保存；MD仅现有文本薄扩 | 需求已修正 |
| R2-06 | 把输出图片lease误写成现成附件preview | 明示缺最窄draft受权读取，复用原语而非artifact身份/新服务 | 需求已修正 |
| R2-07 | 扩枚举仿佛自动支持预览/保存，未识别私有源漂移 | 补私有附件IPC与预览/保存源，和公共源分治；记录HTML漂移，仅同表面收敛 | 需求已修正 |
| R2-08 | “协商”“expand”容易推动新框架/表 | 当前显式路由；不预设新版本/业务表，guard仅条件性 | 需求已修正 |
| R2-09 | 统一数量、TTL/所有超限可截断的描述过强 | 分清producer计数、Native总量、TTL起点、源准入与投影限制 | 需求已修正 |
| R2-10 | 幂等/ACK/正常重开隐含跨重启重投递或改卡 | 限活动turn同路径同摘要等元数据；已提交恢复、未提交如实不可用 | 需求已修正 |
| R2-11 | 每格式必须新生成，潜在引入12生成器/付费视频 | 12格式真实接收仍必验，安全已备样本可经Runtime正常登记；代表性真实工具生成闭环 | 需求已修正 |
| R2-12 | 路径需求重复确认、另存范围及覆盖层级不清 | 尊重用户路径要求、临时最窄边界；仅生成产物另存；对话框确认与atomic写入分开 | 需求已修正 |

第一轮已核的原子批次、失败移除重选、草稿未绑定副本清理、.jpeg合法别名、AC-007缺覆盖不得PASS继续保留。初轮“摘要为摘录”仅修正了误解，却仍增加阅读面；本轮R2-05进一步收缩这一不必要要求，不修改初轮真实检查记录。

## 6. Fact / Assumption / Unknown / 当前判定

- Fact：12扩展与图1—5、路径tooltip、生成卡片、复用及只需求不执行来自用户；当前源码能力/缺口见上述行号与源快照。
- 推荐默认：Office/PDF文件信息卡、MD有界源码、SVG/MP4 file适配、只临时来源路径，均以保留现有机制为取舍，不是新增模型理解或永久保留承诺。
- 实施前仍须收口：原生消息可靠绑定的具体adapter点、最窄附件preview/schema入口、MP4上下文语义表达与闭集版本/reader准入、是否确需reader guard。文档给出了不能违反的边界，不伪造这些实现已完成。
- 当前结论：已纠正发现的复用遗漏与不必要设计；允许交付本次需求修订，**不构成D0确认、代码实施准入或任何AC/D4通过**。所有功能状态保持pending/NOT RUN。

本轮变更限本需求四文件与新增只读来源/文档检查证据；既有参考图和初轮证据不改，产品仓不改，不做服务操作/提交推送。最终检查与复审结论见02。

## 7. 实施授权与D0

2026-10-28用户明确：“接受修订后的FEAT-165需求，现在开始做执行，验证过程中，遇到问题，深入分析根因做修复。”据此记录D0产品/UX确认和整体实施授权，覆盖已审定的Contracts/Host/Desktop薄扩、相关生成/构建、非破坏验证与根因修复。前述两轮仅需求状态保留为历史，不再阻止当前实施。不得强杀、权限故障、二进制篡改或攻击fixture；Runtime核心不改；无Git提交/推送/发布授权。当前四产品仓仍clean、HEAD同第二轮；只写本需求范围。重要日常数据迁移、额外外部付费调用仍按具体边界审定，不借其它Feature额度。

## 8. 执行中确认与兼容收口（2026-10-28）

- 用户明确允许本次Contracts本地提交、不推送。已提交 `333cac6e0ba588bd65a8577d57af4c780bc48d2e`；现有immutable调用表面同步器已同步Host/Desktop。普通Host OpenAPI使用既有scoped同步/校验脚本，不复制或运行历史攻击fixture。
- 用户进一步明确“不得改变原生userMessage类型，文字与文件不用必须合并一个气泡”；本条覆盖原R-04/AC-004同气泡约束。撤回实施中未交付的合并逻辑，沿现有本地附件独立记录展示，不扩原生消息协议。新增图6只作为展示参考。
- 本候选新增闭集沿显式SSE v12发出；v9保持原媒体范围；输入SVG/MP4仍file。复用当前K3.1+media候选，新增Native v42仅作前向reader阻挡，不建文件表、不复制数据。当前日常profile启动迁移明确阻止，未访问/迁移日常数据。
- 图片输入浮层为现有图片校验/读取预算保护的有界投影，只有当前组件在展开期间保留；原生不保留预览bytes/伪造artifact locator，路径只在现有IPC runtime草稿上下文临时保存。此选择不引入图片服务。
- Contracts 8项专项测试、31 schema检查与lint已通过；全量安全生成/全量breaking因仓内其它族未解析远程引用失败，未计PASS，详见Contracts说明。实现/真实App/AC验证仍在进行。

来源最终收口：在同一已授权本地提交内补全共享输入的reverse-dependency（旧selection/broker锁、旧market-host/experts输入派生、chat-models-v2 bundle），最终Contracts commit为`61137174a25dc368e0006f27633fd4a9ad097aa6`，前述333cac6/ea49217只属未发布中间候选。Native conversation/MCP因共享generator摘要发生变更而用现有同步器更新来源锁，原生Item/userMessage类型字节未改。权限bundle同样引用StartTurnV2，沿现有同步器补精确commit同步，保留独立Host历史baseline+当前候选完整输入校验。专家资源既有审核pin保持旧commit的原始Git对象，资源schema逐字节对账，没有刷新资源摘要绕过审核。Connectors仅现有broker来源锁两项摘要同步，worker源代码未变。

当前专项实际结果：Contracts 8项；Host正常12格式登记/原件/ACK/幂等/v9隔离及旧媒体正常测试通过-race；Native12格式导入与图片投影、MD预览/Office保存边界、草稿读取、v41→v42表结构不变共4项通过；Native12格式SQLCipher提交/原子保存/正常重开/视频范围读取1项通过；前端胶囊/生命周期/原生独立显示与旧Composer共54项，IPC源对齐2项通过；Desktop lint和Rust clippy -D warnings、Host go vet通过。尚不构成真实App或全部AC/D4。

根因修复：EventHub闭集遗漏v12导致fallback为v1，已加明确版本并验证；旧Native PDF接收按%%EOF字节结尾误拒正常尾部换行，已改用现有有界PDF preflight并验证原件不变。首轮前端命令因Vitest路径子串匹配进入.local历史副本；重跑已按仓库标准排除.local等目录，结果54项通过，不计历史副本失败为当前源码缺陷。


## 9. 暂停与恢复（2026-10-28）

用户已明确批准最多3次真实任务提交：普通聊天1次，专家聊天创建及续聊最多2次；仅使用12种普通合成样本，分批登记并生成一份简单文件，不调用外部MCP或图片/视频供应商，不迁移日常数据库。批准后用户要求停止，已停止且未启动候选App、未发出真实任务。用户随后明确恢复执行并要求先回顾状态。

恢复前重新核对：所有产品仓HEAD、已记录未提交文件列表、7份验证日志及打包回执摘要与暂停前一致；Contracts为已授权本地提交61137174a25dc368e0006f27633fd4a9ad097aa6，Runtime和Skills工作树clean，无运行中的易界候选进程。真实任务已用0/3。元仓另有FEAT-162改动，属于本需求之外，保留不修改。

继续使用已有canonical K31 media隔离候选进行真实UI/Runtime验收。已通过检查仅作为对应层级证据；未完成的AC和D4仍保持NOT RUN。全量生成/全量breaking历史引用阻塞、未执行的攻击/故障测试保持如实登记，不以本次恢复抹除。

费用批准的原始消息未提供精确时间；feature.yaml 的 approved_at 记录本轮核验并落盘批准的时点（2026-10-28T20:47:57+08:00），不冒称原消息发送时间。

恢复后首轮真实App已从同构建canonical --reopen启动，来源核对通过。选择本轮合成目录为工作空间，原生选择器导入CSV及DOCX/HTML/JPEG/JPG/MD五件批次成功；CSV真实来源路径、JPEG图片浮层及Esc关闭已实际观察。尚未发送真实任务（0/3）。首次尝试键盘全选没有形成全选，实际仅导入CSV，因此不计为超限拒绝验收。

实际视觉发现：胶囊背景引用bg-subtle（亮色为白）导致包裹不可辨；YjIcon默认色覆盖容器类型色。已改用既有skill-pill背景和局部类型图标继承，避免新增颜色或改全局图标。通过应用Cmd-Q正常退出，Host/Runtime正常随退出，无强杀；正在按原入口重建并复核。

实际任务额度已用1/3：CUA逐键输入包含换行时提前触发发送，中文正文也未完整进入，故本次普通聊天指令为不完整正文；仍计真实提交，不重置预算。Runtime正常创建并登记generated-feat165.md（11bytes，只有标题），任务实际完成。停止尝试未成功停止已完成的任务，不记录为取消成功。未请求重跑。

根因继续收口：读取当前隔离Host自身v12只读回放，确认95条正常事件，其中58/59为产物started/completed；密文仍在spool，未ACK。媒体订阅源基于v3，但publishMedia直接接受含v4 phase的生命周期事件，Native按契约拒绝并停止伴随流。复用Host既有legacyEvent投影，保持原生native事件不变；补普通commentary→12产物→final跨Host/Native解码检查，并在伴随流错误时立即drop旧stream释放准入。

另一实际缺口：原生userMessage包含Host包装的文件上下文；视图现仅在同一已有本地session/turn绑定、唯一附件用户消息及唯一native userMessage时使用本地提交正文展示。原生类型、存储和wire不变，附件仍独立；无本地绑定/歧义时不猜关联。增加重开、冷历史及多native消息的普通纯值检查。


## 10. 恢复执行后的真实验收与续聊根因（2026-10-28）

- 真实提交共3/3：普通聊天1次（输入工具提前发送不完整正文，照计额度）、专家创建1次、同专家续聊1次。未提交第4次。底层Provider HTTP请求数未独立计量，不能用任务数冒称HTTP调用数。
- 专家创建：6种剩余输入实际发送成功（MP4/PDF/PNG/PPTX/SVG/TXT），本轮Runtime正常创建generated-feat165-verified.md（36 bytes），7个产物均显示Native已就绪，包含CSV/DOCX/HTML/JPEG/JPG/MD及生成MD；原生正文与本地附件独立，无模型文件上下文包装。
- 专家续聊：单HTML+正文发送，6次publisher调用中5次staged，PPTX拒绝；5份未Native提交，无新产物卡，不能把staged或模型回答当接收通过。只读回放有365条正常事件、两轮terminal与12对产物事件（第一轮7对+第二轮5对）。
- 第二处根因：v3权威turnCompletedPayloadV3允许空code/message；实际两轮terminal均message为空。Native旧分支却以非空字符串规则拒绝，续聊从头回放在前轮terminal提前结束。现改用已有bounded allow-empty primitive，不改变契约/终态/Runtime。完整真实两轮回放经Native解码已通过；当前仍需新构建和真实续聊复验，不能把离线回放计作真实补收。
- Host正常测试补完整commentary→12格式产物→final→正常terminal，27事件（24个产物生命周期），v9隔离与v3普通契约校验通过；Native8项普通测试全部通过，包含该Host事件流及本次真实两轮回放；Rust clippy、Host vet通过。前端15项相关测试通过；补正旧Markdown应拒绝的过时断言，新增普通Markdown正向解析测试通过。
- UI已实际验证：12件原生选择整批拒绝、原正文/专家保留，随后6件重选成功；CSV表格预览展示alpha/12与beta/34，系统保存对话框正常取消后仍ready；PNG/SVG/JPEG输入浮层与正常关闭，重开草稿路径未知如实提示；原普通任务历史重开无重复正文和上下文包装。
- 未完成：12格式逐件另存/摘要、HTML交互、图片放大、视频音画/seek、主题/最小窗口、专家已提交资源正常重开，以及剩余6格式完整接收复验。无外部MCP/图片视频供应商调用；日常数据与Runtime源码未变。
- UI工具随后报告Mac锁定，自动解锁失败；已请用户手动解锁。候选保持当前已完成任务状态，未强杀退出，未在运行中的App上覆盖新bundle。空terminal修复已通过源码测试，尚未重新打包。后续正常退出后用既有canonical入口重建；3次额度已用尽，任何额外真实任务须新增明确授权。D4仍NOT RUN。


## 11. 解锁后续验

用户已手动解锁。候选正常Cmd-Q退出后，最后空terminal修复已canonical重新打包并通过同构建reopen。已提交7份产物与专家两轮原始消息恢复正确，没有自动派发；CSV通过原生对话框成功另存到本轮saved-originals目录。

用户先批准追加1次，随后明确“可以额外追加2次”；保守按最新追加总计2次、需求累计上限5次记录。已开始第4次专家续聊，明确重新登记此前未接收的6份合成样本；不调用外部服务、不修改原件、不迁移日常数据。


## 12. 第4、5次真实任务与最新候选收口

第4次专家续聊将MP4/PDF/PNG/PPTX/SVG/TXT全部接收到Native ready，专家历史累计13份；第5次普通聊天使用长中文名称DOCX，生成ordinary-feat165-verified.md（262B）并真实登记、接收、预览、保存。预算累计5/5，不再自动提交。用户确认已听到3秒测试音。

逐件原生保存12格式＋两份生成MD，所有原件字节一致；另做预览失败图片保存副本、系统同名取消、切换目录与改名。修复图片保存依赖预览成功、Teleport弹窗按钮样式/反馈挤压及四图片并发直接拒绝；最后一项参照现有视频有界等待，保留原并发/内存/授权限制，普通测试和最终真实重开四图片通过。原生userMessage和Runtime未改。

用户明确批准临时切换系统深色。1180×760亮暗十附件、长名/同名异路径、图片浮层与卡片已检查，系统已恢复原浅色。正常退出和canonical重建/同构建reopen，无强杀；未覆盖日常App、未迁移日常库。

当前AC与缺口以02第9节为准：AC-001/004仍pending，D4未通过；其余8项按所列范围PASS。保留前三次任务失败与全量契约引用阻塞记录。最终diff复核无新增阻断发现，Contracts6113717本地提交仍clean，Runtime clean；其余实现未提交，未推送，元仓并行FEAT-162变更未触碰。


## 13. 真实拖入失败的根因修复

用户多次反馈CSV拖入无高亮、无附件。逐层只读观察确认原生投递到WebView，旧页面监听Window而漏收；真实落点均在composer内。改用已有Tauri WebView拖放API，保留Native导入/校验/权限与逻辑点命中。拆分事件target的回归测试3项通过。诊断未生成或派发任务，累计仍5/5；临时观察器经正常退出清理、原生logger源码已删除。最终构建和真实复验结果继续记入02第10节。


## 14. 拖入真实复验与诊断清理（2026-10-29）

用户确认CSV胶囊出现，CUA核对10附件与未发送状态，WebView事件目标修复完成真实复验。附加路径提示观察经计数诊断未复现为缓存清理，未作猜测性改动；临时诊断全部删除、Native源码与诊断前字节相同。最终canonical重新构建/同构建重开，新导入CSV的即时路径及前后台切换后路径正确。

57项治理测试、lint及需求包检查通过；当前状态以02第10.3节为准：AC-001/004 pending、其余8项按范围PASS，D4未通过。真实任务仍5/5；无新增付费请求、提交、推送、日常迁移或Runtime/userMessage改动。候选保留在新建任务10附件草稿、未发送状态。


## 15. 再审与新增真实任务授权（2026-10-29）

Owner要求审核实现进度、现有问题并继续FEAT-165，随后明确“真实任务额度继续授权5次”。累计上限10次，恢复时已用5次、可用5次；仍限合成样本、不调用外部MCP/图片视频供应商、不迁移日常数据，不包含额外Git提交或推送。首先补工具选集与纯附件提交，历史分页继续区分真实已有数据读取和UI分页，不能凑数或修改默认分页阈值冒充验收。之前5/5耗尽均为历史检查点，后续实际使用逐笔记账。

Owner随后再次明确“真实任务额度可以继续授权10次”：在累计10次之上新增10次，累计上限20次，当时已用7次、剩余13次。第6次选集+CSV/SVG、第7次纯TXT无正文均实际完成，未显示外部工具调用。继续按必要性使用，不以凑满UI分页阈值为由无意义消耗额度。

Owner已明确接受分页分层验收并保留UI按钮未实测。AC-004完成，全部Must按记录范围通过，进入本地D4最终门禁；累计7/20。补正两份Design Pattern的SVG/临时路径冲突与产物分级规则，新增同名附件分页/重开正常回归；未改产品运行代码、原生userMessage或Runtime。

最终严格D4与claim审计PASS，元仓57项治理测试/lint/Shell语法、Desktop lint和Design docs构建通过。feature usable、implementation complete；全部10项Must按列明范围完成，UI加载更多按钮仍NOT RUN并有Owner明确接受。Runtime/原生userMessage保持，候选停留在已完成两轮历史，没有运行任务；累计7/20，不自动消耗剩余13次。
