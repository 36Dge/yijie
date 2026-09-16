# FEAT-154 步骤 1：生命周期与契约影响定稿

日期：2026-09-15。只读源码调查与方案草案，无源码修改、生成、测试、App/服务启停。已读 yijie、yijie-contracts、yijie-desktop、yijie-coze 的 AGENTS 及相关源/现有契约说明。以下行号基于本次工作树。

用户已于本轮明确选择：**保持纯前端范围：页面离开确认，关闭应用不保证保留**。该选择覆盖本文此前的推荐/备选边界；当前权威入口见[07](07-integration-design.md)。

## 1. 定稿结论

按 PDF 的纯前端范围：采用同一 iframe 生命周期内的内存设计态，保护应用内页面返回/路由切换，明确正常关闭 App/窗口、刷新、重启会丢失本次设计；本期不新增 native close/exit guard。**不能再把“正常 App 关闭保护已存在”写成事实**。

未来实施整体 `contract-impact = semantic`。新增电商节点及私有设计模型不进入 wire/存储/执行面，但需要扩大现有跨 renderer `dirty_changed` 的明确语义，让它涵盖无法持久保存的页面设计内容。源 schema 现在只给 Boolean，源说明只讨论 dirty/base revision，不能据形状未变降为 none。现有全部直接 consumers 只用 dirty 决定“有待保护本地内容”，不会触发保存；方向性源码核对表明旧 reader 能继续处理相同 true/false，不需要新 MessageChannel kind/字段/native command。semantic 结论是工程设计结论，未代替 Owner 确认或运行验证。

本次仅写需求资料，实际文档工作仍 `contract-impact=none`；feature 的未来实现分类为 semantic，两者应明确分开。

## 2. 当前代码事实与准确定位

| 事实 | 源码定位 |
|---|---|
| 权威 envelope 仅有 dirty:boolean，无“可保存”承诺 | yijie-contracts/jsonschema/workflow-editor/bridge-v1.schema.json:35、141；对象 additionalProperties:false 位于 :3 |
| 权威说明保留 dirty/base revision，未定义不可保存设计态 | yijie-contracts/docs/workflow-local-v1.md:65–67 |
| producer 本来就把待确认运行也投射为 dirty，而非只代表可保存图差异 | yijie-coze/frontend/apps/workflow-local/src/main.tsx:82–86、129–133：`model.dirty || !!runs.pending` |
| dirty 消息仅带现有当前 binding + Boolean | yijie-coze/frontend/apps/workflow-local/src/bridge.ts:71–78 |
| Desktop 接受 dirty 后只调 hook；close/history 是 UI 回调 | yijie-desktop/src/api/workflow-editor-channel.ts:90–118 |
| UI 回调校验当前 bridge/generation | yijie-desktop/src/components/workflows/WorkflowEditorPane.vue:63–83 |
| 页面退出先阻挡正在写/创建/重连/关闭/发起版本运行，再针对 dirty 或未知 run 弹确认 | yijie-desktop/src/components/workflows/WorkflowLocalWorkspace.vue:39–66 |
| 确认后是关闭编辑会话，没有保存动作 | 同上 :55–63；yijie-desktop/src/pages/workflows/use-workflow-workspace.ts:146–164 |
| 原提示已经表达“本地内容及待确认操作查询入口” | WorkflowLocalWorkspace.vue:97–103 |
| 路由返回与同组件参数更新都走 leaveEditor | WorkflowLocalWorkspace.vue:65–67；:75 接原返回 |
| history 打开同页 modal，iframe 不卸载 | WorkflowLocalWorkspace.vue:75、91–96；它不是离开 |
| 原 history 可显式执行既有内部版本，页面文字已说明未保存草稿不影响已发布版本 | yijie-desktop/src/components/workflows/WorkflowRunPanel.vue:24–40 |
| 重连只重绑 port，不重建 iframe | WorkflowEditorPane.vue:96–97；父页 key 是 workflow_id，WorkflowLocalWorkspace.vue:73 |
| 重连保留宿主 dirty，首次不同 workflow 打开才清空 | use-workflow-workspace.ts:57–83，尤其 :72 |
| dirty/uncertain 原草稿收到新 revision 不会替换 | yijie-coze/frontend/apps/workflow-local/src/draft-model.ts:19–28 |
| 原 normalizer 只允许保留执行含义的 native normalization | draft-model.ts:30–35 |
| 保存快照和未知操作标识独立保留，不应丢失或重发 | draft-model.ts:36–57；main.tsx:162–186、223–242 |
| 连接变更保护 active operation ticket 并使保存/试运行/发布进入未知状态 | main.tsx:87–115；bridge.ts:80–85 |
| SaveService 本地变更直接走 adapter.change，没有调用 upstream debounce autosave | yijie-coze/frontend/packages/workflow/playground/src/services/workflow-save-service.ts:671–690 |
| 原 save 入口对 localAdapter 委托 | workflow-save-service.ts:449–451 |
| 自动读回替换目前以 !next.dirty + revision 变化为条件 | workflow-save-service.ts:691–719；这正是设计态必须覆盖的风险点 |
| 当前 readonly 仅断连/替换中；needsReview 只给 savingError，不会自动 readonly | workflow-save-service.ts:659–668 |
| native 只在 window 已 Destroyed 后撤销会话，并在 App 已 Exit 时正常清理；未找到 CloseRequested/ExitRequested 拦截 | yijie-desktop/src-tauri/src/lib.rs:189–196、435–444；全源码 rg 无关闭请求 guard |
| native close 只校验调用者并调用 runtime.close | yijie-desktop/src-tauri/src/workflows/commands.rs:70–77 |
| native App exit 只 retire session，不保存图 | yijie-desktop/src-tauri/src/workflows/runtime.rs:861–870 |
| 当前 capability 仅 core app default、event listen/unlisten，未允许 window.close 或任意 event emit | yijie-desktop/src-tauri/capabilities/default.json:7–11 |

## 3. 最小内存隔离设计

### 3.1 状态所有权

- `DraftModel` 继续只拥有可保存的原三节点 name/canvas/revision/baseline/dirty/conflict/uncertain。其三节点 codec 与 payload 校验保持，禁止用通用设计 codec 代替。
- 新进程内 `EcommerceUiDraftModel`（统一设计名称）拥有 `active`、进入时原生文档深拷贝、当前设计文档、设计名称、原 workflow_id/baseRevision、设计选择/本地 edit sequence/需核对标志。这些不是 public DTO，不写 localStorage/文件/数据库。
- 首次点击添加电商节点时，先同步捕获官方原生文档与名称，再进入设计态，再进行 add；若 base 尚未加载/断连/readonly/busy/存在 conflict、unknown save/test/publish 或在途 test，则阻止首次进入并解释需先核对。允许原草稿已有普通未保存修改，原 dirty 不被清零，不为了进入设计先自动保存。
- 进入时不重建或替换 DraftModel。设计状态复制其当前可见文档；base 的原内容、baseline、revision、dirty、已有 test 事实保持。随后所有 native add/delete/move/line/field/name/undo/redo 都只改变设计状态。
- `normalize/change/changeName` 在 localAdapter 处按 `active` 分流。设计 normalization 使用私有设计校验/比较器；不把含新 nodeType 的图传给 `decodeCanvas`/`DraftModel.normalize`。连接断开前已排队变更只允许落到相同挂载实例和当前设计 epoch，不能落到新工作流或已退出设计态。
- `snapshot.dirty` 必须是保护标志：`design.active || model.dirty || unresolvedEditorOperation`。不要以“当前剩余电商节点数量=0”替代 active；否则撤销首次添加/删最后一个节点会误让新图可保存或被服务端重载。
- 单独保留实际提交资格 `canSave/canTest/canPublish=false` 与 action guard `if (design.active) return`，覆盖快捷键、service save/reload、异步回调。按用户最新确认，header、节点卡片和test panel的试运行展示入口可点击，只显示未接入提示，不调用实际执行action。新图永远不进入 `save_draft`、`test_draft`、`publish_internal`。
- 明确“放弃本次设计，恢复原草稿”才退出 active：确认 → 冻结编辑并生成新的documentEpoch → 保留原稿和设计快照启动reload → 仅当前epoch的reload/normalize成功后恢复原内容/原dirty/原名称并结束active → 清理设计态。失败保留设计/保护位、继续阻写，可重试恢复或明确离开。仅删最后一个节点/关闭侧栏/清空全部新增字段不退出。

### 3.2 官方 SaveService 接入细节

`LocalWorkflowSnapshot` 是同一 Coze 构建内的私有接口（typing/local-workflow-adapter.ts:4），可新增 `documentKey` / `documentEpoch` / `readonly` / `mode` 等进程内状态，**不要**扩进 wire。

当前订阅在 :695 只根据 server revision 重载，不能实现同 revision 的“恢复原草稿”。推荐将“选中的 UI 文档身份”单独表达为单调 epoch；normal edit 不增 epoch，进入或明确恢复等主动切换增 epoch，clean remote reload 仍走现有 revision 分支。主动切换必须先冻结编辑，用 fromJSON/reload 从受控快照替换，并以 epoch + mounted generation 检查完成回调；重置/隔离 native undo/redo 历史，避免恢复原草稿后 Ctrl-Z 再引入设计节点。已补核对 `frontend/packages/workflow/history/src/hooks/use-clear-history.ts:26–36`，原生 `HistoryService.clear()` 真实存在。进入/恢复均经 stop→clear→reload→clear→start（恢复原disabled状态）隔离撤销栈；不造另一套undo。保存进入时原内容/dirty，不承诺恢复进入前撤销历史。

设计 active 期间无论收到哪个 server revision，都禁止 `workflowDocument.reload(remote)`、禁止 remote normalize 覆盖设计内容。可将新 remote 只存待核对摘要/快照。服务器同 revision：当前图与选择不动，恢复连接后继续；服务器不同 revision：保留设计文档与原 DraftModel，标记冲突；原 baseline revision 不改写，不自动重放/合并。退出设计后pendingRemote继续存在并阻写，保留原内容不能清掉冲突解禁。明确放弃全部本地内容并重载时，按07创建全新候选DraftModel调用receive验证（不在dirty原模型直接receive），原生reload/normalize成功后才切换main的modelRef；失败保留原状态。

既有 readonly 弱于 needsReview：为 UI 设计 explicitly 提供 readonly 状态，断连、重连 bootstrap、替换中、冲突核对期间统一冻结 add/delete/move/field/name/undo/redo。只读状态仍允许浏览当前配置、关闭面板和走宿主离开流程。没有升级会话授权或离线编辑新能力。

### 3.3 未知回执

进入设计前遇 unknown 时保留旧查询入口，不允许“进入设计”清空它。设计期间不会新发写请求。迟到旧消息只能通过 operation ticket/generation/revision/epoch 判断归属，不替换设计图；保存结果只能更新它所对应的原 DraftModel 快照。`read_operation` 始终查询原 operation ID，无码则保留“无法自动重发”的原提示；不得为了清状态自动再 save/test/publish。退出/离开确认同时提示已有 pending 查询上下文会丢，已提交业务操作不会因离开被撤销。

## 4. 离开、重连与历史矩阵

| 用户动作 | 推荐行为 | 接入点 |
|---|---|---|
| 关闭节点浮层/侧栏、Esc | 只关面板，保留设计值和选中实例上下文；不是结束设计 | Coze 原面板/侧栏 |
| 切换节点 | 从实例存储读回完整字段，保留 false/0/空串/未设置区别 | 私有设计模型 + official node form |
| 画布/工具栏返回 | transport.close → Desktop router.push → leaveEditor → 统一确认 | main.tsx:334、WorkflowLocalWorkspace.vue:67 |
| Native error boundary 返回、等待页返回 | 同 transport.close，不单独丢弃/卸载 iframe | main.tsx:44–61、357 |
| 会话恢复遮罩里的返回 | emit close → 同 router guard | WorkflowEditorPane.vue:134–135 |
| 宿主侧栏导航、浏览器 back、切换 workflow 路由参数 | onBeforeRouteLeave / onBeforeRouteUpdate 统一确认；取消保持路径和当前实例 | WorkflowLocalWorkspace.vue:65–66 |
| 有在途写/重连/关闭/版本运行提交时返回 | 原 busy 阻挡，等待真实结果；不伪造失败/关闭 | WorkflowLocalWorkspace.vue:41–43 |
| dirty / design active / unknown 时确认离开 | “继续编辑 / 放弃本页未保存内容并离开”；副文案分别解释设计没有持久保存、原草稿未保存修改及查询入口 | 原 NModal，改为适用于全部本地内容的文案 |
| 确认离开 native.close 失败 | 不卸载编辑器，不清空设计/dirty；显示错误可重试 | use-workflow-workspace.ts:146–164 |
| 请求历史 | 打开原同页 modal，不触发离开/不清空设计；重复点击仍同一 modal | request_history → showHistory |
| 关闭历史 | 仅关闭 modal，返回原设计与当前实例；不得 reload 图 | WorkflowLocalWorkspace.vue:91–96 |
| 在历史显式执行旧内部版本 | 保留既有能力，仅运行服务端指定版本，不发送设计图；现有页面已有明确文案 | WorkflowRunPanel.vue:25–34 |
| 会话正常到期/重连，同 revision | iframe 活着、设计实例不变；bootstrap 后继续，重新投影 dirty=true | EditorPane :96；main reset/onConnect + 新模型 |
| 重连服务端 revision 不同 | 本地设计与原 baseline 都保留，标记需核对；不自动覆盖/merge | 新设计模型 + DraftModel + SaveService |
| 删除最后一个新节点/撤销首次添加 | 保持 active 和写禁用；显式恢复原稿才退出 | 新设计模型 |
| 明确恢复原草稿 | 确认放弃设计，受控同 revision 图切换，恢复原 dirty；新图不混入旧 undo | adapter/SaveService epoch |
| 正常关闭窗口、Cmd-Q/退出 App、刷新/重启 | **本期无阻止/确认保证，内存设计丢失**；进入设计时需清楚显示限制 | 现有 native 无 guard；推荐不扩本期 |

注意：历史不是离开。禁止为了阻止设计执行将 `dirty` 直接当 history `busy`，否则原本允许“修改草稿时执行已发布版本”的有效交互会被无端禁用，构成潜在 breaking。若产品想禁整个历史执行面，必须作为单独改变明确决定，不能藏在 pure UI 分类。

## 5. semantic 权威源最小修订方案

### 5.1 源语义文本候选

在 bridge schema `dirty` 的 description 和 `dirty_changed` 专项说明中定义：

> 当前 editor 页包含离开会失去的本地内容或待确认操作查询上下文。true 包含可保存草稿差异、仅保留于本页内存且尚不支持持久保存的 UI 设计状态、尚待核对的操作上下文；false 表示当前 producer 确认这些保护条件均不存在。此标志只驱动宿主应用内离开确认，不代表内容已发送/已保存、内容可被 save_draft 接受、执行权限、操作终态或原生窗口/应用退出已被拦截。consumer 不得据此自动保存、试运行、发布或取消既有操作。消息只作用于当前 ready port / bridge_id / generation；重连必须重投当前值，切换连接不能清空仍存在的保护条件。

同时明确 `request_close` 为请求宿主尝试页面导航，由宿主统一确认和 session close；`request_history` 为当前页面打开历史面板，没有新保存/执行/离开或图替换副作用。不得添加未请求的设计字段或新 event kind。

### 5.2 消费者兼容矩阵（源码工程复核，运行均 NOT RUN）

| Producer → consumer | 变化/兼容结论 |
|---|---|
| 旧 Coze → 新 Desktop | Boolean/现有 kind 均不变；旧 model dirty + runs.pending 条件都被新通用文案包含，原可保存/运行语义不变 |
| 新 Coze → 现有 Desktop Vue/channel | shape 同源 validator 可读。true 只触发已有 modal；原 modal 已称本地内容及查询上下文、关闭不自动保存。因此能保守保护内存设计，不误发图、不 auto-save；新文案提高明确性 |
| Desktop → Coze (connect/response) | 不改字段、kind、绑定、generation、顺序与 errors；保留 current ticket guards |
| Desktop Vue → Rust | 不改 8 个 IPC command、payload、close 行为；dirty 不进入 Rust，无新增原生拦截承诺 |
| Desktop Rust → API → Coze service | 新节点不跨边界。原三节点 canvas/保存CAS/试运行/发布/版本执行/回执全部保持 |
| API/Coze service 的 source-lock reader | 源 schema description 若变化会更新来源摘要，应按 canonical generate/sync 同步 locks，不能以 reader 不解释 dirty 为由留下不匹配 bundle |
| 更旧 1.2 Desktop + 1.3 新 history producer | 既有不支持组合仍不支持：旧严格 validator 拒绝 request_history。FEAT-154 不修复、不扩大这项兼容承诺；继续成对同源本地候选 |

分类为 semantic 的依据是扩大旧保护位解释但经全部直接消费者方向性代码核对仍兼容；不是新增业务能力，也未发现支持的旧交互被删/误解。反之如果后续改变 save 语义、发送新 kind、禁历史既有版本运行或让旧 reader 未防护就失去内容，应重审并升 breaking。

### 5.3 实施顺序与证据

1. Contracts schema description + docs/workflow-local-v1.md + 合成真/假保护标志示例/专门 conformance；沿 canonical generator 生成（不得手改 TS/validator）。计划版本统一为1.4.0-local-candidate；只更新同族候选元数据和语义描述，当前尚未生成/发布，不伪造source commit。
2. 当前 source lock 是 `1.3.0-local-candidate`，base_commit 为 `32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4`。实施时复核 supported-baselines 的本族 fallback + 已发布与旧 pin 全部适用基线，不把 dirty sibling 当不可变发布。
3. Desktop 统一确认文案/聚焦 consumer cases → Coze producer/model/adapter → 全部相关来源锁同步，一致后本地启用。
4. 正常合成检查覆盖：dirty=true 不保存；取消保留；关闭失败保留；重连同 revision/不同 revision；已有 dirty 进入并明确恢复；删最后节点不解禁；history 不卸载；异步旧回调不覆盖。未做 App 正常关闭拦截测试应写“范围外、该能力未实现”，不能 PASS。
5. rollback 正常退出候选 App、回退 UI producer/consumer/来源锁组合，保留原三节点服务数据；设计数据本来只在内存，因此退出即不保留，交付说明须一致。

## 6. 已排除的 native 关闭保护（记录取舍）

本轮用户未选择此路径，以下仅保留范围取舍说明，不进入本期实施清单。未来另行扩范围时，才新增正常 `WindowEvent::CloseRequested` 和 `RunEvent::ExitRequested` 拦截并接统一退出确认；当前 `Destroyed`/`Exit` cleanup 保留。单靠 Vue route guards/beforeunload 或 iframe confirm 不能称覆盖 native App close。

最小可靠方案是有限 native leave guard：新 renderer 显式注册当前 main editor guard；native 收到 close/exit 生成单次 request token 并阻止默认销毁，通过已授权 event listen 的限定新事件通知 Vue；Vue 统一检查在途/dirty/unknown，用户决定后经具名 resolve command 答复；native 只接受当前 guard/request 的 allow/keep，超时或无响应保持窗口；allow 后正常 close/exit，原 session/sidecar cleanup 执行。command 不收图/身份/任意 window label/任意执行路径。

这涉及 yijie-contracts 权威 IPC/event、generated TS/Rust、Desktop commands/runtime/lib.rs/API adapter、main-window authorization；新的消费者应 opt-in，不能向旧 Vue 无条件发新事件。只有未来另行授权时才独立检查方向兼容和权限范围后再定整体分类，不能直接凭“新增命令”称 additive。无需商品/模型/媒体 API，仍不持久化设计状态，但明显超出最小纯前端 UI 范围。

## 7. 用户决定与当前状态

本轮用户明确选择纯前端：页面离开确认，关闭应用不保证保留。范围问题已关闭，不再索取同一决定；不新增native guard、command、event、capability或CSP。

D0完整方案确认状态以07/02记录为准；全部真实业务/UI实现、跨仓生成与产品D4仍未执行。本文的源码方向兼容结论不是运行测试通过。
