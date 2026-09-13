# FEAT-153 完整工作流产品页：现有接口只读审计

日期：2026-09-12。范围：Contracts workflow-local / editor bridge 源、Desktop native consumer、API workflows 模块与 Coze localadapter。仓库路径均相对 CrossBSD 工作区根目录；行号为本次读取时的位置，UI 实现仍可能并行变化。

本次 `contract-impact = none`：只核查现有行为、写本证据，不修改 wire、源契约、生成物、服务、持久状态或部署。整个 FEAT-153 的既有 semantic 分类不因此降级。已读取 Meta、Contracts、Desktop、API、Coze 各仓 AGENTS。未启动/停止服务，未运行 App、HTTP、数据库、模型或测试，未提交代码。本文不是完整产品页真实验收 PASS。

## 结论与能力范围

现有 source/native/provider 已能表达“保存 → 已保存草稿试运行 → 同 revision 成功证明 → 内部发布 → 指定发布版本执行 → 历史摘要/结果详情”，不需要为该基本闭环新增 DTO、HTTP 路由或 native command。

版本采用用户明确输入（可默认当前 `published_version`）是可实施方案。应显示“当前已发布版本”，不声称存在完整版本目录。现有契约没有版本列表，亦未保证 `1..当前最大 patch` 是可枚举库存；不能生成伪版本列表。当前 Coze 在固定 scope 的事务锁内按 patch 加一只是实现事实，不能替代公共目录契约。

需要保持三项语义：试运行的是已保存草稿；发布要求该 revision 的真实成功试运行；`receipt.completed` 只证明登记完成，执行是否成功须另读 `Run.state/terminal`。编辑会话过期后，结果/历史/原操作查询应走独立 native `query`，不能继续依赖受 E lease 限制的 editor exchange。

## 可直接使用的调用

权威 DTO 源为 `yijie-contracts/openapi/workflow-local/workflow-local.yaml`。Desktop 使用现有 `WorkflowSchemas` / canonical AOT `validators`，不要手抄 DTO。客户端方法见 `yijie-desktop/src/api/workflow-native-client.ts:89`。

| 用户操作 | 已有 native client 输入 | 成功结果 / HTTP 状态 | 关键边界 |
| --- | --- | --- | --- |
| 工作流列表 | `list({cursor?, limit?})` | `WorkflowList` / 200 | summary 无 canvas；继续使用原样 next_cursor |
| 创建 | `create({name})` | `Workflow` / 201 | native 分配 operation_id；不要通过列表猜测失败写入不存在 |
| 打开/重连 | `open({workflow_id})` | `EditorOpenedView` | 公开 view 不含 E；新 bridge/generation，原生持有秘密 |
| 保存 | `exchange`，operation=`save_draft`，expected_revision、name、canvas | `EditorExchangeResult.workflow` / 200 | E 必需；CAS；native 分配 operation_id |
| 试运行 | `exchange`，operation=`test_draft`，expected_revision、input=`{input:文本}` | `EditorExchangeResult.run` / 202 | E 必需；请求不含未保存 canvas |
| 内部发布 | `exchange`，operation=`publish_internal`，expected_revision、successful_test_run_id | `EditorExchangeResult.workflow` / 200 | E 必需；从结果读 published_version，不能客户端自增 |
| 指定版本执行 | `run({workflow_id, version, input:{input:文本}})` | `Run` / 202 | K_NA；不需要 E；native 生成 operation_id |
| 运行详情 | `query({kind:"run", workflow_id, run_id})` | `RunQueryResult.run` / 200 | 不带 limit/cursor；可在 E 到期/关闭后查询 |
| 历史 | `query({kind:"history", workflow_id, cursor?, limit?})` | `RunQueryResult.history` / 200 | summary，无 input/output/nodes；选择条目再读详情 |
| 原操作查询 | `query({kind:"operation", operation_id})` | `RunQueryResult.receipt` / 200 | 不带 workflow_id、limit 或 cursor |

所有 exchange 另有共同字段：`bridge_id`、`generation`、`protocol_version:1`、唯一 `request_id`。仅允许对应操作的字段；`operation_id` 在 exchange 中仅属于 `read_operation`，不是浏览器指定写入身份。源定义见 `workflow-local.yaml:2375`、`:2434`、`:2497`、`:2505`。native 严格消费见 `yijie-desktop/src-tauri/src/workflows/runtime.rs:279`、`:344`、`:547`、`:616`。

HTTP 真实路由见 `yijie-api/internal/modules/workflows/interfaces/http/handler.go:48`；源路径分别为 `workflow-local.yaml:209`、`:420`、`:752`、`:874`、`:996`、`:1223`、`:1331`。不存在 GET versions、cancel run、调度或流式推送接口。

## 草稿、试运行和发布规则

1. **dirty/保存中/保存结果未知**：若界面宣称测试当前可见画布，先完成保存并取得确定 revision。不能把已有 saved revision 的成功测试当作新 dirty 画布的证明。安全但尚未完整连线的草稿可以保存，`runnable=false` 应显示原因或引导完善连线。
2. **保存一定产生新 revision**，即使文本内容相同；Coze 清除 `test_run_success`。旧成功测试 proof 因 revision 不同失效。依据：`yijie-coze/backend/domain/workflow/localadapter/mutations.go:47`，特别是 `:63`、`:71`。
3. **试运行快照固定**：Coze 比较 expected_revision，将已保存草稿快照后交引擎；后续保存不会改写该次执行。依据：`yijie-coze/backend/domain/workflow/localadapter/execution.go:46`。输入只来自 TextInput，未保存 canvas 不在请求里。
4. **发布资格**：必须同 workflow、同固定 scope/user、mode=debug、同 expected_revision、真实成功状态，并关联一条本地 test operation。前端启用条件至少应为 `run.mode === "debug" && run.terminal && run.state === "succeeded" && run.workflow_id === 当前资源 && run.revision === 当前已保存revision`，并且没有 dirty/不确定保存。服务端最终裁决。依据：`mutations.go:87`、`:108`、`:112`。
5. **重复发布**：同 revision 使用新的 operation_id 会产生新的版本；重放原 operation_id 才保持原版本。因此“发布未知后再点一次”不是安全重试。依据：`mutations.go:118`；正常既有测试见 `yijie-coze/backend/domain/workflow/localadapter/local_test.go:304`，本轮没有执行该测试。
6. **发布与试运行输入**：源的发布 proof 绑定图 revision 和 run，不单独绑定某个 UI 输入。只更换测试输入而未改图不会自动使已有成功 proof 失效；若产品希望必须使用最新输入测试，可作为更严格的本地 UI 规则，不能误称后端要求。
7. **指定版本执行与 dirty 草稿独立**：释放版从真实 `workflow_version` 读取不可变 canvas/revision；不存在时返回 resource_not_found。可以允许在 draft dirty 时执行明确选择的旧版本，但文案必须明确“执行已发布版本”，不能显示为执行当前未保存画布。依据：`execution.go:75`。

## 原操作与执行状态

源 `OperationReceipt` 的说明在 `workflow-local.yaml:2210`、`:2245`。UI 必须分开显示“操作登记状态”和“执行状态”：

| receipt.phase | 可作的判断 | 建议后续 |
| --- | --- | --- |
| recorded | API 已记录意图，结果尚未确定 | 保存原 operation_id，查询原操作 |
| unknown | 尚不能确定登记/提交结果 | 继续查询原操作；不自动另建 operation |
| completed | 资源提交或 execution 登记已完成 | 若有 run_id，再 query run；发布版本使用 receipt.version |
| rejected | 原意图已确定拒绝 | 显示固定错误码文案；修正条件后的新操作必须是新明确意图 |

API 对未确定意图进行 Coze reconcile；Coze 暂无可读回执时，可以返回 **200 + receipt.phase=unknown**，不是只通过 HTTP 409 表达未知。API 已完成的旧保存/发布回执不会被后来的当前 draft 替换。依据：`yijie-api/internal/modules/workflows/application/service.go:97`、`:155`、`:182`、`:188`。

`receipt.version` 仅属于该次 publish 或 release run，create/save/debug test 不携带环境中已有的 published_version；源 `workflow-local.yaml:2231`，API `service.go:133`。查询旧回执后如果当前资源 revision 已变化，应展示两者差异，不能覆盖尚未保存的本地画布。

native 每次新的 create/save/test/publish/run 调用都会分配新 operation_id。HTTP 发出后的不确定结果携带原 operation_id；保留它及当时 workflow/revision/version/input，以便查询而不重复执行。客户端处理未类型化 IPC 异常或不合 schema 的写入结果时可能只有 `operation_unknown`、没有 operation_id（`yijie-desktop/src/api/workflow-native-client.ts:69`）。此时无法可靠精确查询，不能用空列表/空历史证明未执行；应保留“结果不确定”并禁止自动重发。不要读取或显示错误原文来补造 ID。

运行以 `terminal` 为是否结束的权威字段，不能根据 HTTP 返回、30 秒预算、会话关闭或 `state` 未识别来推断结束。当前 Coze 映射 `running/succeeded/failed/cancelled/interrupted/native_<值>`，跨 epoch 未完成记录为 `unknown`。其中只有原生成功/失败/取消是 terminal；interrupted 仍非终态。固定 scope 同时只允许一项真实非终态执行，包括其他工作流，不能因 UI 计时结束释放 busy。依据：`yijie-coze/backend/domain/workflow/localadapter/history.go:98`、`store.go:287`、`execution.go:117`、`:172`。

202 可以很快已是 terminal success；不必强制先显示虚假的等待阶段。读取进行中执行时使用正常节奏的查询，避免重叠请求，响应按 workflow/run/当前页面 generation 校验；卸载只停止前端查询，不等于取消引擎。`pendingWrites` 表示 HTTP/IPC 写入尚未完成，不能替代活跃 run 状态。

## 结果、历史、版本与限制

- `Run` 可包含输入、输出、节点结果、revision/version、时间、错误；`RunSummary` 不包含正文。源见 `workflow-local.yaml:2077`、`:2171`、`:2621`。历史按 created_at DESC、id DESC 分页，默认 20、最大 50；cursor 必须原样传回，不解码后自行拼页。实现：`yijie-coze/backend/domain/workflow/localadapter/history.go:207`。
- 节点结果 state 是原始数值的字符串，当前上游 1=Waiting、2=Running、3=Success、4=Fail。总执行 state 的 `succeeded` 文案不能直接套在节点原值上。保留未知值兜底；NodeResult schema 是开放字符串。依据：`history.go:183`、`yijie-coze/backend/api/model/workflow/workflow.go:1959`。
- 真实最终 output 来自 native `result`；开始、文本、结束节点的输出分别从 `input`、`output`、`result` 提取。成功但缺失真实输出是 provider 错误，不应把空字符串拼成假结果。依据：`history.go:160`、`:171`、`:189`。
- 输入上限 4096 UTF-8 bytes、前缀 1024、输出 5120、canvas 262144、完整消息 524288；最多 3 个节点、1 个活动执行、执行预算 30 秒、E 300 秒。源 `workflow-local.yaml:1703`。文本计数应使用同源 AOT 验证/UTF-8 字节数，不能只看 JS string.length；完整消息上限包括 JSON 转义和包络。
- `Version` 源语法为 `v0.0.<正整数>`、最长 32 字符（`workflow-local.yaml:1655`）；provider 当前只生成/接受最多 9 位 patch（`yijie-coze/backend/domain/workflow/localadapter/policy.go:19`、`mutations.go:128`）。这是已识别的范围差异：普通已生成版本不受影响，但契约并未完整说明发行上限。当前 UI 使用源校验，provider 决定版本是否真实存在，不扩大成“任意源格式版本必可执行”。本轮不改源，也不通过伪版本请求测试边界。
- 现有列表没有版本目录，不能根据 published_version 枚举 1..N。明确输入 + 当前发布版本提示 + 历史中真实版本信息，足以满足“指定版本执行/历史查看”。若以后需要完整选择器，应先在源定义版本 summary/list、分页/排序/不存在语义与 native query 能力，再生成并逐消费者对齐；不在 UI 造第二库存。

## 会话与主题交互

E 是绝对 300 秒有效期，无读取续期，API 只存在内存 map；关闭幂等删除。依据：`yijie-api/internal/modules/workflows/interfaces/http/handler.go:224`、`:245`。E 到期后的 native `exchange` 所有操作均受 lease 检查，包括 read_run/read_operation（`yijie-desktop/src-tauri/src/workflows/runtime.rs:279`）。独立 `query` 和 release `run` 仅机器身份，不依赖编辑会话（`:547`、`:616`）。

因此父页结果/历史/原操作查询控件应保持可用，编辑器到期覆盖层只禁派发受 E 管理的操作。显式重连使用新 binding/port，不 reload 丢弃 dirty canvas；pendingWrites 时先等写调用得出可记录结果，不能靠重连把未知写变成未发生。现有 workspace 防护见 `yijie-desktop/src/pages/workflows/use-workflow-workspace.ts:56`。关闭 E 不取消实际执行，也不删除历史。

桥源 `yijie-contracts/jsonschema/workflow-editor/bridge-v1.schema.json:13` 已有 connect/ready/request/response/dirty_changed/request_close；generation 在 `:29`，响应共用源 ErrorResponse/EditorExchangeResult（`:37`）。现无 theme 消息，不应临时发送未经源定义的 postMessage。

当前 Desktop 只跟随系统亮/暗模式：`yijie-desktop/src/App.vue:113`、`:210`，父页 CSS `color-scheme` 见 `src/styles/variables.css:2`、`:162`。Coze 编辑器样式已有对应 `prefers-color-scheme` 与 light/dark：`yijie-coze/frontend/apps/workflow-local/src/style.css:1`。保留现有 CSS 方案即可，不新增跨仓主题 wire；实际 WebKit/两主题/窗口尺寸效果仍要由真实 App 证据验证，源码存在不等于视觉通过。

如果以后新增独立于系统的手动主题且现有 iframe color-scheme 不能满足，再评审非秘密 light/dark theme 字段及动态消息。应先改桥权威源、条件字段约束、AOT/TS 生成与所有消费者锁/解析，再允许 producer 发送；不能把主题塞进资源 DTO、native secret 或未定义消息。本轮无该变更。

## 未执行与建议普通资格

本轮仅源代码/文档检查，没有新测试 PASS。禁止的攻击载荷、故障注入、强杀、权限破坏、危险 fixture 全部未执行，不以这些手段验证 unknown/终态。静态结论不覆盖真实 DB 事务、App 渲染、主题、运行调度或会话自然到期。

完整页后续普通资格可沿真实 UI 完成：保存 R1 → 试运行并读实际节点/结果 → 用同 R1 成功 proof 发布 v1 → 修改保存 R2 → 再测试/发布 v2 → 明确选择 v1 执行并核对仍为 v1 输出 → 历史摘要进详情 → 查询已有 operation_id → 正常到期后仍能查询结果/历史并显式重连。用既有正常异步 mocks 检查 pending/unknown 展示和旧响应不覆盖新选择，无需制造真实服务故障。所有 App 事实由实际执行者另行记录。
