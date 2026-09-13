# FEAT-153 第 2 步：Coze 精确设计可行性核对

- 日期：2026-09-12。
- 前提：主代理告知用户已批准 ADR-0019 候选方向；本附件辅助精确设计和 D0，不实施运行集成。
- 范围：只读当前 Coze 源码，未启动服务、安装、调用业务接口、修改业务文件或进行攻击/故障注入。仅新建本附件。
- 路径：以下源码路径均相对 `yijie-coze/`。版本来源见该仓 `yijie-upstream.lock.json`。
- 状态：**静态可行性分析；所有“建议新增”均未实现，真实编辑器、服务和 D4 均未验收。** 本附件不替代正式 Contracts 源定义。
- 本步传输与会话技术权威为 [05-local-integration-design.md](../05-local-integration-design.md)。本附件保留 Coze 源事实与实现缺口；早期浏览器直接携带编辑 cookie 的候选已由最终方案替代。

## 结论

可信内部桥、受控三节点运行和同一编辑器可以沿用现有领域能力，但不是配置几个代理 URL 即完成。至少需要在 Coze 增加受认证的本地适配入口、固定主体初始化、草稿 CAS、与具体 revision 绑定的发布校验、指定发布版执行、真实运行列表及写操作关联记录。

三个容易误判的点已经核实：

1. Save 请求有 `submit_commit_id`，但后端没有用它实施 CAS；不能把字段存在当作并发保护。
2. `/v1/workflow/run` 实际选择最新发布版本；现有领域层才支持指定版本，不能直接代理公开 run 并承诺执行选定旧版。
3. `list_spans` 和 `get_trace` handler 返回空结构；`get_run_history` 仅按 execute ID 读取。历史列表需要真实新增查询。

## 1. 可信 local identity：可复用组件与必须新增的边界

### 已有事实

- `backend/domain/user/service/user.go:52–80` 定义 CreateUserRequest、用户创建和 space 查询能力。
- `backend/domain/user/service/user_impl.go:252–350` 可以创建用户、个人 space 和成员关联；会生成密码 hash，依次写 space、user、space_user。该调用链不是一个完整原子事务，不能被描述为现成幂等的 principal provisioning。
- `backend/domain/user/service/user_impl.go:438–465` 读取用户 space 成员关系；`backend/application/user/user.go:231–261` 已将其变成编辑器所需 space list。
- `backend/application/base/ctxutil/session.go:27–42` 从 context cache 中的 Session 读取 UID；Session 的字段在 `backend/domain/user/entity/session.go:25–31`。
- 当前全局中间件先 OpenAPI PAT、再 Web session，见 `backend/main.go:92–103`；现有公开接口没有“验证易界可信内部身份”的能力。

### 建议新增

1. **API 仍是易界固定 local scope 权威。** Native→API 的身份和编辑会话由本需求的跨仓安全设计定义；renderer 的 owner/tenant/space 仅可作为操作参数，不成为授权来源。
2. **Coze 自己维护 local principal 的对应行。** 新增受控 `EnsureLocalPrincipal` 服务，仅接受已经验证的固定 local scope，Coze 内部事务创建或读取其 synthetic user、space 和 membership。API 不直接写 Coze 私有表，不调用公开注册/登录，不让用户设置第二套密码。若复用现有用户创建字段，使用进程生成、永不用于公开登录的随机值，不以空密码或固定公开密码初始化。
3. **内部调用不走公开 PAT。** 新增仅供已认证 API 服务调用的窄 local adapter；服务凭据/签名与 exact local/profile/feature gate 全部通过后，由 Coze 根据持久映射构造固定 UID 的内部 context。调用领域方法，不伪造 OpenAPI ApiKey context，不把新增可信路径变成现有 SessionAuthMW 的通用放行条件。
4. **独立内部入口。** Coze 内部适配监听地址/路由由 Infra 限制为 API 可达，浏览器只访问 gateway；网络限制不能代替服务凭据验证。原有公开 OIDC 与 Coze 原接口语义保持分离。
5. **绑定需要核实真实记录。** 正常重启时读取已保存的 principal mapping，并核对 user、space、membership 是否仍一致；不以“同名 email 存在”就自动领用任意用户，也不在缺失时覆盖已有数据。

“API 验证 trusted scope → Coze 验证 API 服务来源 → Coze 读取固定 principal 和实际资源”是新的适配路径，不是现成上游功能。跨仓请求和状态先进入 yijie-contracts，Coze 私有 mapping/migration 留在 Coze。

## 2. 静态 iframe、MessageChannel 与窄服务入口

### 最少必要能力

编辑器需要独立静态 app 资源、当前 synthetic 用户信息、固定 space list、节点模板及画布读写；运行区还需要试运行与节点结果。`frontend/packages/workflow/playground/src/services/workflow-save-service.ts:307–328` 初始化节点、画布、变量与模型服务；`frontend/packages/workflow/playground/src/workflow-playground.tsx:69–85` 读取 space store。以上是现有依赖事实，不代表最后选择让 iframe 直接调用这些 HTTP API。

最终选择为：HTTP `/editor/` 只提供无秘密的静态 bundle/内置资源；数据经 typed MessageChannel → 父 Vue 容器 → 具名 Rust workflow command → 原生内存短会话 E → workflow-local API → 私有 Coze adapter。iframe 设置 `connect-src 'none'`，不直接访问 workflow、Coze 或身份服务。E 不写入 WKWebView cookie store；即便服务端采用 Set-Cookie 表达 E，也仅由原生 HTTP 端保存和附加，不向 iframe/父 renderer 暴露响应头或秘密。

`frontend/packages/workflow/nodes/src/utils/get-llm-models.ts:137–155` 即使当前图没有模型节点也会请求 GetTypeList。`workflow-save-service.ts:383–400` 在没有关联 bot/project 时可不加载全局变量。restricted editor 必须把必要元数据通过批准的 bootstrap 操作和 MessageChannel adapter 取得，限制或延迟无关功能初始化；不能为兼容旧请求就开放所有 `/api/*` 或取消 connect-src 限制。模型配置实际为空时，bootstrap 可表达真实的空列表；不得将依赖失败吞成伪成功以“让页面能开”。

### 适配要求

- MessageChannel operation、具名 native command、HTTP 方法和内部路由逐层精确 allowlist；分离静态只读资源、元数据读取、图写入、试运行与版本执行。原始 `nodeDebug`、copy/import、插件/知识库/数据库、文件上传、注册登录、PAT 管理和其它域默认不开放。
- 父容器校验 frame/source/origin、协议与容量，再调用具名 Rust command；Rust 重验固定身份、profile/enable、窗口和对应 editor binding。API 校验 K_NA、run epoch 和适用的 E；Coze 校验独立 K_AC。浏览器 origin 或 loopback 不代替认证；不得转发 iframe 提供的 URL、headers、actor 或服务身份参数。
- E、MessagePort 和 native editor binding 绑定同一个 workflow/scope 和有限权限。画布请求里的 workflow ID、space ID、execute ID 必须与绑定及资源真实记录一致；不能仅把请求 space 改写为固定值后放行任何 workflow ID。端口关闭或 E 到期只撤销后续访问，不取消已接受的运行。
- 图写入和运行必须通过同一 Coze local policy，不能让 Desktop 走归一化接口而 editor 直通未经保护的上游保存/运行端点。
- 静态 bundle 与图标仅走固定本地静态资产通道，不返回资源、身份或会话秘密；不开放 MinIO/上游远程图标或任意外域。MessageChannel 握手、CSP、导航隔离、到期重连与回跳在同一真实 App 的 dev/packaged 入口验证，不再以跨站 cookie 能否携带作为选型依赖。
- 编辑器的 MessageChannel adapter 需显式传递正确 revision 和选定版本/试运行关联；原生生成并保存写操作 ID，重试沿用同一操作。冲突/未知结果时保留未保存内容。现有 save 前端默认传 `vcsData.submit_commit_id || ''`，证据为 `frontend/packages/workflow/playground/src/services/workflow-operation-service.ts:143–161`，不能假定它已满足新 CAS 语义。

## 3. 三节点、4 KiB、单运行与 30 秒分别在哪层落实

| 约束 | 主执行层 | 精确定义与必要补充 |
| --- | --- | --- |
| 节点 allowlist | Coze local adapter 的 schema policy；UI 同步限制 | 只允许开始 ID 类型 1、文本处理类型 15 且 concat、结束类型 2 且 returnVariables；禁止子图、循环、其它节点、模型、HTTP、Code、插件、文件参数及跨流程引用。草稿可暂时不完整，但 run/publish 必须恰有有效三节点和开始→文本→结束两条边；不能要求创建后的空草稿立即可执行 |
| 输入 4 KiB | API 提前反馈，Coze 执行前最终检查 | 对解码后的 UTF-8 文本使用字节长度 ≤4096；只能传契约定义的单个 string 字段，不以字符数或 JSON body 长度替代。参数默认值也须受约束 |
| 图与输出上限 | Coze schema policy + 文本处理结果边界 | 4 KiB 输入本身不限制模板重复引用导致的输出增长。建议首期只允许前缀字面量+一次 input 引用；前缀、canvas 原始字节及最终输出另设明确上限。数值由主需求契约冻结，不能仅限定节点个数 |
| 同 scope 1 个在途执行 | Coze 运行准入；API 可同步做快速反馈 | 草稿试运行和发布版运行共用同一 scope 槽位，不能分别各放行一个；从执行登记到真实终态占用。HTTP 超时、关闭页面、取消轮询或 TTL 到期不能直接释放槽位 |
| 30 秒运行预算 | Coze executor 的 local 执行配置/runner context | 需要新增限定 local 执行的预算，不是 API HTTP client timeout。现有运行超时为 0，且 ExecuteConfig 没有 deadline 字段。预算在创建执行 context 后持续有效，AsyncExecute 返回时不能 defer cancel 立即取消，也不能随浏览器断开丢失控制 |

证据：TextProcessor 支持 concat/split（`backend/domain/workflow/internal/nodes/textprocessor/text_processor.go:57–82,122–170`）；默认限额为 0（`backend/domain/workflow/internal/execute/consts.go:24–28`）；ExecuteConfig 当前字段见 `backend/crossdomain/workflow/model/workflow.go:34–60`；runner 使用 context.WithTimeout 的扩展点见 `backend/domain/workflow/internal/compose/workflow_run.go:284–290`。

**30 秒是合作式执行预算，不是保证进程在 30 秒被终止。** Eino/节点须实际观察执行 context，正常 DeadlineExceeded 由 `backend/domain/workflow/internal/execute/event_handle.go:216–223` 映射 timeout 错误；结果必须由引擎持久终态确认。若预算到期仍没有引擎终态，显示 `unknown/awaiting_reconciliation`，保留在途限制并报告，不强杀、不由 API 伪造失败/取消终态。首期不开放用户“取消运行”；已有 Cancel 只用于内部已审阅的合作式取消方案时再明确接入，不能把停止轮询当远端取消。

单运行限制可采用 Coze 本地适配的 scope 记录+数据库事务登记；本期仅一份受控 Coze 实例，不声称分布式调度。正常结束释放槽位；服务异常或旧实例遗留需要根据真实执行状态核查，不能基于租约过期认定执行已结束。本轮只验正常结束后 stop/start。

## 4. 草稿 revision：原生字段存在，CAS 不存在

### 事实

- 原始权威 IDL `idl/workflow/workflow.thrift:416–424` 有 required submit_commit_id。
- `backend/application/workflow/workflow.go:316–320` 没有读取该字段，仅按 workflow ID 调用 Save。
- `backend/domain/workflow/service/service_impl.go:149–163` 每次生成新 commit ID。
- `backend/domain/workflow/internal/repo/repository.go:343–357` 调用无 expected revision 条件的 Save；draft table 确有 commit_id，见 `backend/domain/workflow/internal/repo/dal/model/workflow_draft.gen.go:14–23`。

### 必须新增

以 native `workflow_draft.commit_id` 的 string 形式作为公开 draft revision 候选，不另建竞争的 revision 计数。Coze local save 接受 `expected_revision`，在 Coze 自己的事务中锁定/核对当前 draft，更新 canvas、输入输出、新 commit ID 和 local operation 结果；0 rows affected 是冲突。不能用 API 的“先 GET 比较、随后旧 Save”代替 CAS，也不能只用浏览器按钮禁用或 Coze 进程内 mutex 保护持久数据。

保存成功返回同次事务产生的 `new_revision`；editor 更新本地基线。409 类冲突保留当前编辑内容，提供重新读取并比较的路径，不自动覆盖。已有前端冲突 modal 受 project 多标签 feature flag 限制（`workflow-save-service.ts:502–507`），需要本地模式明确处理，不假定现有 UI 会显示冲突。

未完成图可以保存以支持正常编辑；它必须保持安全结构/大小约束，但不标为 runnable。只有执行前的完整验证通过才进入试运行。

## 5. 试运行与发布必须绑定同一 revision

当前 TestRun 可以传 commit_id（`idl/workflow/workflow.thrift` 对应生成请求 `backend/api/model/workflow/workflow.go:30477–30488`），领域读取按它选择草稿或 snapshot；但一般编辑器对普通草稿默认传空值，见 `frontend/packages/workflow/playground/src/services/workflow-operation-service.ts:176–187`。

更重要的是成功回调 `backend/domain/workflow/internal/execute/event_handle.go:66–70` 仅按 workflow ID 调用 UpdateWorkflowDraftTestRunSuccess；repository 在 `:364–365` 也仅按 ID 更新。保存时的 `calculateTestRunSuccess` 会在执行 schema 相等时继承此前 bool（`backend/domain/workflow/service/service_impl.go:1920–1945`）。因此 **TestRunSuccess 不是“指定 revision 已被本次成功试运行证明”的充分证据**；编辑与试运行并发时尤其不能直接信任该 bool。

建议 local adapter：

1. 试运行请求明确 expected revision，Coze 在自己的事务/受控变更序列中检查当前版本并固定执行快照，再建立带 commit_id 的原生 execution；snapshot 必须在允许后续保存之前持久可读取，不能依赖稍后异步回调才补。
2. 运行记录已包含 workflow_id、space_id、mode、commit_id，见 `backend/domain/workflow/internal/repo/dal/model/workflow_execution.gen.go:11–37`。内部发布请求带 revision 与 successful_test_run_id，Coze 检查真实 execution 的 scope/workflow、debug mode、success 和 commit_id 全部一致。
3. 新保存产生新 revision 后，首期要求新 revision 重新试运行；不隐式采用上游按执行 schema 相等继承 bool 的宽松规则。
4. 发布时再次 CAS/锁定当前 draft revision，确认等于请求 revision；不开放 Force。可以复用已有版本 canvas 写入，但不能仅调用旧 Publish 并依赖 TestRunSuccess。

这是静态发现与建议修正，未并发实跑，不声称已复现竞态。

## 6. 内部版本格式与指定版本运行

- IDL 约定版本 `vx.y.z`（`idl/workflow/workflow.thrift:654`）。解析实现在 `backend/domain/workflow/service/utils.go:150–180`，按 v 前缀与三段整数拆分；递增比较在 `:183–198`。它不是完整 SemVer 验证器，不能承诺所有 prerelease/build 形式。
- 建议易界服务端分配 `v0.0.1` 起的单调 patch 版本，前端不输入任意版本字符串；同一次内部发布操作固定该版本，重试不能重新分配下一个版本。
- 版本表对 workflow_id+version 有唯一索引（`docker/volumes/mysql/schema.sql:112`），可作为重复发布检查的一部分；多次写入仍需 Coze 事务。已有 `CreateVersion` 依次更新 version/draft/meta 且最后 meta 错误只 warn，见 `backend/domain/workflow/internal/repo/repository.go:288–340`；本需求内部发布应事务化并读回，不沿用“返回成功就完成”的判断。
- 原 `/v1/workflow/run` 强制使用最新发布版，见 `backend/application/workflow/workflow.go:1776–1779`，不支持按易界请求任意指定旧版。
- 领域 ExecuteConfig 有 From/Version（`backend/crossdomain/workflow/model/workflow.go:34–38`），`GetEntity` 的 FromSpecificVersion 真正读取指定版本（`backend/domain/workflow/internal/repo/repository.go:582–594`），`GetVersion` 按 ID+version 查询（`:749–758`）。因此可信内部 adapter 可以直接以 FromSpecificVersion+明确 Version 调用领域 AsyncExecute；不用公开 PAT 或修改公开 run 语义。
- 图/版本/执行仍在 Coze；API 保存资源归属与 ID 关联，不复制另一份版本内容或运行状态机。

## 7. 历史列表：新增 Coze 查询，不能代理空 trace stub

`backend/api/handler/coze/workflow_service.go:630–641,646–657` 的 ListRootSpans/GetTraceSDK 仅返回 new response。`backend/application/workflow/workflow.go:1864–1912` 的 get_run_history 仅按 execute ID 读取。现有 SQL execution 表与索引已支持所需记录（`docker/volumes/mysql/schema.sql:104`），但本次未找到现成的有归属过滤的运行分页应用 API。

建议最小新增 `ListLocalWorkflowRuns`：在 Coze 内按服务端绑定的 scope/space、workflow ID、operator 和根执行过滤，区分 debug/release；使用稳定 `(created_at, id)` 倒序 cursor，限制页大小。返回真实 run ID、mode、draft revision 或 version、原生状态、时间和有界摘要。Node detail 沿用 GetExecution/GetNodeExecution 但先核对 execution 实际 workflow/space；不接受任意 execute ID 配上一个有权限的 workflow ID。

注意原 schema 注释说 root_execution_id 可空，但当前 Prepare 写入根 ID 自身（`backend/domain/workflow/internal/compose/workflow_run.go:264–280`）。首期新运行的根记录应按实际写入语义过滤（如 root_execution_id=id 且无 parent node），不能照旧注释排除所有真实根运行。

API/浏览器的历史列表须真正调用该查询；本地 memory 数组、搜索 stub 或仅保留浏览器发起的 run ID 不满足正常重开历史。原生状态枚举以 `backend/domain/workflow/entity/workflow_execution.go:58–63` 为准，不依赖 SQL 旧注释；不能将 Interrupted 当成功。

## 8. 创建、保存、试运行、发布、运行的可操作幂等与未知结果语义

### 共同原则

当前 Create/Save/TestRun/Publish/Run 均不是已验证的端到端幂等写入。特别是 `WorkflowRunner.Prepare` 每次分配 execute ID（`backend/domain/workflow/internal/compose/workflow_run.go:126–130`），在 `:264–280` 建运行记录后才由 AsyncRun 的 goroutine 执行（`backend/domain/workflow/internal/compose/workflow.go:160–170`）。仅由 API 保存 idempotency key 无法解决“Coze 已写成功、API 没拿到响应”的不确定窗口。

建议新增 **Coze local operation 关联记录**，归 Coze 私有持久数据所有：唯一 `(固定 scope, operation_id)`、动作类型、请求摘要、workflow ID、revision/version、可用时的 execute ID 和操作接收/关联状态。API 透传同一个 operation ID，保存必要业务关联；它不成为第二运行状态机。这里的操作状态只描述命令是否已经登记/关联效果，运行状态始终读取原生 execution。

| 操作 | 最少必要语义 |
| --- | --- |
| 创建 | 首次请求在 Coze 事务中创建 operation→workflow 关联、meta+draft。相同 key+摘要返回同一 workflow ID；同 key 不同摘要冲突。搜索通知失败不能使已创建资源丢失关联；读回确认后展示，不能盲目再次创建 |
| 保存 | operation 结果与 CAS draft 更新同事务写入；重复同一 key 返回原 new_revision。若新请求使用旧 expected revision，返回冲突。不能因相同 canvas 内容就断定某次未知写已经被唯一执行 |
| 试运行 | operation 绑定固定 draft snapshot/revision 与 server-generated execute ID；与 scope 单运行槽和原生 execution 登记形成同一次受控事务。重复请求查询同一个 run，不启动新 goroutine |
| 内部发布 | operation 绑定预分配 version、revision 与成功 test run；同次事务验证并写版本。重复请求读原 version。已有同 version 但 revision 不符是冲突，不返回成功，也不自动改发下一版本 |
| 发布版运行 | operation 绑定明确 workflow/version/输入摘要与 execute ID；重复同一 key 返回原 run；不同 key 才代表用户明确发起新的运行，但仍需通过单在途准入 |

运行事务需要对现有 Prepare 增加“使用已登记 server-generated execute ID/关联记录”的 local 扩展点，不能让外部 renderer 指定原生 ID，也不能在旧 AsyncExecute 返回后才追加 mapping 并声称消除了窗口。此扩展不等于构建任务队列；本期不做后台重放和在途恢复。

### 用户可观察结果

- 读超时：可重试读取；不能改写原生状态。
- 写调用未知：返回/保留 operation ID，显示“结果待确认”，通过 operation 查询获取 workflow/revision/version/run 关联；用户刷新后仍能查询。**禁止客户端或 gateway 自动换新 key 重发。**
- provider 有已登记结果：返回同一结果，并读原生资源/运行确认；不能把 operation 已接收等同 execution success。
- provider 暂无结果但此前调用仍可能在途：保持未知，不以一次 not-found 证明未执行；任何允许同 key 重交都必须由 provider 的唯一键与原子登记保证不会重复，不能交给 API 猜测。
- process 在原生 execution 登记后、goroutine 启动前停止：可见记录仍可能没有终态；本期不自动重放。显示 unknown/需要核查，保留原 ID 和证据，不伪标 success/cancel，不靠租约过期开放另一在途运行。
- 普通输入校验失败且未接受命令：给出明确参数错误；用户修正后发起新 operation。已接受的执行正常失败后，新 operation 才是一次新的运行，历史保留旧 run。

若不准备实现上述原子操作关联，正式契约必须降低为“禁止自动重发、未知结果需要人工查询且可能无法定位”的诚实语义，不能同时承诺可恢复查询和去重。本需求现有 Must AC 包含未知结果先查询及正常重开，应优先实现有界的 local 关联能力。

## 9. 最小改动清单与正常验证

1. Contracts：local 内部 bridge 与归一化操作的真实 source-first 契约，冻结 revision/version、operation ID、分页、限额与错误语义；不手抄生成 DTO。
2. Coze：local principal ensure、窄内部 adapter、实际资源核验、图与参数 policy；CAS 保存与原子内部发布；revision-bound 试运行证明；指定版本 AsyncExecute、单槽/预算、operation 关联、真实历史列表。
3. Editor：本地 restricted mode、typed MessageChannel adapter、revision 与 operation ID 生命周期、模型/无关节点初始化收口；保存冲突和未知结果不得丢失草稿，不直接 fetch 数据 API。
4. Native/API：具名 workflow command 持有 E 与受管 K_NA，API 验证可信 local scope/编辑会话并通过 K_AC 调用窄 Coze adapter；维护业务资源关联和审计。不读写 Coze 私有表，E 不入 WKWebView，不向 renderer 暴露 cookie、公开 PAT 或服务秘密。
5. Infra/正常验收：固定版本与独占数据，正常服务准备和退出；同一真实 App 完成三节点保存/重开/试运行/内部版本/选定旧版执行/历史。普通并发保存可验证 CAS；相同合法 operation 的正常重复请求可验证去重；不同普通内容的同 key 可直接在进程内 conformance 验证冲突，不构造攻击载荷或故障。

本轮未执行服务启动、真实 API/编辑器、并发 CAS、幂等、预算超时、正常 stop/start 或故障恢复。未执行原因是第 2 步精确设计范围及用户禁止故障/攻击注入；影响是本附件证明可改造的位置和需新增能力，**不证明任何上述新增能力已通过测试或 D4**。
