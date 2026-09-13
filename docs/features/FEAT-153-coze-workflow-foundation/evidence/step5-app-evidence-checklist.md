# Step 5 — real App evidence checklist

日期：2026-09-12。本文是只读核对方案，**所有项目待实际观察，不填写 PASS**。
本次只新增核对文档，contract-impact=none；不改变业务、wire、数据库或部署行为。
根代理负责真实 App 操作、受控服务生命周期和实际读取。本文不声称 UI、保存或会话资格已通过。

## 1. 将真实 App 操作与唯一资源对应

- [ ] 分开登记 dev / packaged 载体、本次 App 构建路径与摘要、启动来源、实际操作时间窗、
  provider image IDs、run epoch、Contracts producer/consumer locks、editor manifest SHA。
  dirty candidate 摘要与 Git base commit 分开记录，不把当前 HEAD 当完整构建来源。
- [ ] 本次通过 App 创建带唯一验收后缀的普通合成名称；记录 UI 实际输入，避免与此前
  HTTP/session qualification 资源混淆。由现有受控客户端只读 list/detail，或受限 SQL
  将名称/创建时间窗对应到唯一 workflow ID；后续一律用该 ID，不仅凭名称匹配。
- [ ] workflow ID、revision、Coze user/space ID 始终作为十进制字符串保存，不能经过
  JavaScript Number。不得手工编造 operation ID 来代替 App/native 实际生成的 ID。
- [ ] 保存前后各记录一次真实 Workflow 详情：workflow_id、name、revision、updated_at_ms、
  runnable、published_version 的存在性、canvas 字节数及 SHA-256。HTTP 内容用当前生成
  Workflow schema 校验；读取使用固定受控入口，不接受替代 URL/headers/actor。

权威映射：`yijie-coze/backend/domain/workflow/localadapter/store.go:151` 的 workflowView
将 `workflow_draft.commit_id` 作为 revision、原始 canvas 作为 Workflow.canvas。
API 的 workflow_resources 只保存归属，不保存权威 canvas 或当前 revision。

## 2. 图、节点位置与 prefix

- [ ] 创建后记录初始 revision R0。真实 App 添加/编排普通开始→文本处理→结束并执行保存后，
  记录 R1；同一 ID 保持不变，成功新 save 的 revision 应改变。每次进一步保存均单独记录
  对应 revision，不把最终 revision 倒填到先前 save 回执。
- [ ] 只解析本次合成 Workflow.canvas，输出有限的节点/边摘要与 raw canvas SHA；不扫描其它
  工作流、用户表正文、运行输入或日志，不输出凭据。原始 canvas 如需保留，只限本次合成
  资源并遵守 256 KiB 上限，不能通过日志 dump 全部响应。
- [ ] 节点从 `nodes[]` 按 `id` 匹配，不能依赖数组下标：开始 ID `100001`/type `"1"`，
  文本处理 type `"15"`（当前编辑器新增 ID `200001`），结束 ID `900001`/type `"2"`。
  最多三个节点、两条边；边比对 `sourceNodeID` / `targetNodeID`。
- [ ] 拖动前后比对同一节点的 `meta.position.x/y` 数值；保存后读回以及返回再打开后的
  canvas 应保留保存位置。屏幕像素受缩放/平移影响，不拿截图绝对像素替代图坐标。
  新建默认草稿可能尚无 meta.position，编辑器读取会补默认坐标，不能把该正常化当丢失。
- [ ] prefix 位于文本节点 `data.inputs.concatParams[]` 中 `name=="concatResult"` 的
  `input.value.content`。其保存值应为 App 实际输入的字面前缀 + `{{input}}`；UI 显示前缀
  不含末尾模板。按 UTF-8 字节核对前缀，不能只按字符数。不要另造 editable DTO。
- [ ] 保存后再读和返回重开的 name、prefix、边与 position 摘要应与已保存版本一致；
  如保存期间仍有后续编辑，将“本次提交已保存”和“后续仍 dirty”分开记录。

源码依据：
`yijie-coze/frontend/apps/workflow-local/src/canvas-data.ts:9`、`:21`、`:27`、`:47`、`:52`；
`yijie-coze/frontend/apps/workflow-local/src/native-canvas.tsx:78` 序列化实际 TransformData.position；
`yijie-coze/backend/domain/workflow/localadapter/mutations.go:46` 以 commit_id 做 CAS，并将请求
canvas 与新 revision 在同一事务中保存，不重建用户位置。

## 3. 只读数据库核对

- [ ] 仅连接本项目现有专用 `yijie_workflow_local` PostgreSQL 和 `coze_workflow_local` MySQL，
  先核验容器归属标签/精确 image/network 与数据库名。通过现有受控凭据文件消费方式连接，
  不把密码/DSN 放 argv、终端、证据、Config.Env 或 SQL 正文。
- [ ] 使用只读事务和参数化 workflow ID，读取本次资源所需列；不运行 migration、UPDATE、
  DELETE、INSERT、锁表或权限故障检查。只读事务正常 COMMIT；不停止任何服务。
- [ ] PostgreSQL 中确认唯一 workflow_resources 归属及 fixed scope binding；读取该资源
  的 create/save operations 和对应 audit。不得把 read/principal 的普通 audit 当成 session
  open/close 的专用审计。
- [ ] MySQL 中 join workflow_meta / workflow_draft 与固定 principal，确认 creator/space
  与 API binding 对应、app_id=0、无 deleted_at；读取 commit_id 和 canvas。仅当前资源。
- [ ] 若本轮仅创建/保存，workflow_version / workflow_execution 不应因这些 UI 动作新增；
  不要求整个历史数据库或 scope 的旧执行槽为空，避免误判此前保留的合法资格数据。

以下为**未执行的参数化查询模板**。占位符由受控 DB client 绑定实际 ID，不拼接任意 SQL。

PostgreSQL（`$1` 为实际 workflow ID）：

```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT current_database();
SELECT r.workflow_id, r.scope_key, r.created_at,
       s.owner_user_id::text, s.tenant_id::text, s.coze_user_id, s.coze_space_id
FROM workflow_resources r JOIN workflow_scope_bindings s USING (scope_key)
WHERE r.scope_key = 'feat-153-local-v1' AND r.workflow_id = $1;
SELECT operation_id::text, kind, phase, workflow_id, created_at, updated_at,
       receipt->>'OperationID' AS receipt_operation_id,
       receipt->>'Kind' AS receipt_kind, receipt->>'Phase' AS receipt_phase,
       receipt->>'WorkflowID' AS receipt_workflow_id,
       NULLIF(receipt->>'Revision', '') AS revision,
       NULLIF(receipt->>'Version', '') AS version,
       NULLIF(receipt->>'RunID', '') AS run_id,
       NULLIF(receipt->>'ErrorCode', '') AS error_code
FROM workflow_operations
WHERE scope_key = 'feat-153-local-v1' AND workflow_id = $1
ORDER BY created_at, operation_id;
SELECT id, operation_id::text, action, outcome_code, occurred_at
FROM workflow_audit
WHERE scope_key = 'feat-153-local-v1' AND workflow_id = $1
ORDER BY id;
COMMIT;
```

MySQL（每个 `?` 均绑定同一实际、校验后的正 int64 workflow ID）：

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT, READ ONLY;
SELECT DATABASE();
SELECT CAST(m.id AS CHAR) AS workflow_id, m.name,
       CAST(m.space_id AS CHAR) AS space_id, CAST(m.creator_id AS CHAR) AS creator_id,
       m.app_id, m.latest_version, d.commit_id AS revision,
       d.updated_at, d.modified, d.test_run_success, d.canvas
FROM workflow_meta m JOIN workflow_draft d ON d.id = m.id
JOIN yijie_workflow_local_principal p ON p.user_id = m.creator_id AND p.space_id = m.space_id
WHERE p.scope_key = '12500000-0000-4000-8000-000000000001:12500000-0000-4000-8000-100000000001'
  AND m.id = ? AND m.app_id = 0 AND m.deleted_at IS NULL AND d.deleted_at IS NULL;
SELECT operation_id, kind, CAST(workflow_id AS CHAR) AS workflow_id,
       CAST(run_id AS CHAR) AS run_id, run_epoch, created_at, receipt
FROM yijie_workflow_local_operation
WHERE scope_key = '12500000-0000-4000-8000-000000000001:12500000-0000-4000-8000-100000000001'
  AND workflow_id = ? ORDER BY created_at, operation_id;
SELECT COUNT(*) AS version_count FROM workflow_version WHERE workflow_id = ? AND deleted_at IS NULL;
SELECT COUNT(*) AS execution_count FROM workflow_execution WHERE workflow_id = ?;
COMMIT;
```

schema 依据：
`yijie-api/internal/modules/workflows/infrastructure/postgres/migrations/00001_workflows.sql:1`；
`yijie-coze/backend/domain/workflow/localadapter/migrations/001_local_adapter.sql:1`。
已有 `yijie-infra/scripts/workflow-local-mysql-read.py:35` 输入校验固定要求第4步的四次执行/
十个 completed operations/v0.0.3，**不能直接拿它验证仅创建/保存的 App 资源，也不能为了
套用该脚本伪造运行证据或放宽其原断言**。这里只复用其受控连接/只读思路。

## 4. 真实操作回执与 audit

- [ ] 从本次 workflow ID 对应的真实持久记录取得 create/save operation IDs；再通过
  `/v1/workflow-local/operations/{operation_id}` 的既有只读入口交叉核对生成的
  OperationReceipt。MessageChannel request_id 与 operation_id 不同，不能互换。
- [ ] 对每次成功 create/save 核对 operation_id、kind、phase=completed、workflow_id、
  该次提交 revision；create/save 不应带 ambient published_version，且无 run_id。
  unknown/recorded/rejected 如出现，按真实状态保留，不能为匹配 UI 字样改写为 completed。
- [ ] API 私有 receipt JSON 使用 `OperationID/Revision/Version` 等 PascalCase；
  Coze/private wire 和 API HTTP 使用 snake_case。按字段语义归一比较，不能 raw JSON
  全等。API 私有空 Version/RunID 与公开 DTO 省略对应字段等价。
- [ ] API operation 行与 audit 的 recorded→completed 应关联同一 operation ID；
  Coze operation 的 scope/workflow/receipt 应相同。request_sha256 与 request_hash 是
  各自内部算法的结果，不预设跨服务必须字节相等。
- [ ] 只保存后的最新 draft revision 应等于最后一次成功 save；旧成功 save 的 receipt
  继续保留其原 revision。API/Coze 回执发现差异须保留原证据并报告，不为验收改数据。

依据：`yijie-api/internal/modules/workflows/domain/model.go:40`；
`yijie-api/internal/modules/workflows/infrastructure/postgres/repository.go:106`、`:152`；
`yijie-api/internal/modules/workflows/application/service.go:133`；
`yijie-coze/backend/domain/workflow/localadapter/store.go:231`、`:238`。

## 5. App close 与后端会话撤销的证据边界

- [ ] **数据库不能证明某条 App E 被关闭**。API session 仅存在 Handler 内存 map，保存
  workflow 绑定、随机 session ID、E 的 SHA-256 和到期时间；没有 session SQL 表、持久 E
  或专用 open/close audit。Coze 不持有该 E。SQL 无 session 行不是“已撤销”证据。
- [ ] 记录本次 App 返回动作、未保存处理、结果是否正常返回列表、再打开时的新真实读回。
  该观察配合源码能支持关闭调用路径；不能单凭“窗口消失/回到列表”宣称捕获了 DELETE 200。
- [ ] 若已有受控的非秘密实际 command/HTTP 结果记录，核对本次绑定的 CloseResult.closed=true
  或相应 DELETE 成功；不得为截图/调试把 E、K_NA、session DTO 或 native 内存导出给浏览器。
  当前无该直接记录时，明确标记“本次 App E 的服务端撤销未独立观察”。
- [ ] API-only 自然生命周期资格能证明同一 provider 的 300 秒、显式新 E、close 后原 E
  被拒绝等机制；它针对自己的 session，不能替代本次 App E 的直接事实，也不能替代
  dirty 画布保留、焦点或 dev/packaged WebKit 验收。
- [ ] App 的重连应保持同一 iframe/画布并使用新 bridge/generation/port；返回后重开是新的
  读取流程。分别记录，不把“重新加载后内容一致”写成“过期重连保留未保存画布”。

源码依据：`yijie-api/internal/modules/workflows/interfaces/http/handler.go:27`、`:46`、`:107`、
`:224`；`yijie-desktop/src-tauri/src/workflows/runtime.rs:696`、`:715`、`:731`；
`yijie-desktop/src/pages/workflows/use-workflow-workspace.ts:143`（await native close 后清空 editor）。

本清单编写期间未调用 UI、HTTP、Docker/数据库或其它 App，未读 PRIVATE 值、未改业务代码/
Contracts/生成物。所有核对结果需根代理依据本次真实观察另行填写；禁止攻击 fixture、权限
破坏、故障注入、强杀或伪造任何缺失证据。
