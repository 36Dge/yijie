# FEAT-153 第 3 步 API / Coze 独立收尾复核

日期：2026-09-12。复核者：API 边界实施代理，独立阅读 Coze 代理的实现。本附件中的仓库路径以 CrossBSD 工作区为根。复核仅阅读代码、契约与既有测试；没有启动服务、执行数据库迁移或重复运行已通过的测试。

## 结论

在本次限定的普通三节点链路中，没有发现剩余的 P1/P2 接口或执行语义阻断项。发现一项包含两个必填输入的 P2 部署说明遗漏，已获主任务授权补齐 API 部署权威说明。此结论不等于真实 MySQL/PostgreSQL 事务、Docker 拓扑或桌面编辑器已通过资格验证。

## 发现与关闭

**P2：Coze 容器监听地址与 MySQL 时间解析选项未完整写入部署输入。**

- 事实：`yijie-coze/backend/application/workflowlocal/config.go:76` 读取 `YIJIE_WORKFLOW_COZE_LISTEN_ADDR`；缺省仍为 `127.0.0.1:18889`。第 81 行只允许 container scope 下显式使用 `0.0.0.0`，不会自动切换监听地址。因此仅配置 `YIJIE_WORKFLOW_NETWORK_SCOPE=container` 时，API 的 `coze-workflow:18889` 连接不能到达该容器内 loopback listener。
- 事实：同文件第 84–89 行要求 MySQL `ParseTime=true`，不含 `parseTime=true` 的 DSN 会在启动前被拒绝。此选项与上游 `yijie-coze/docker/.env.example:18` 的原厂 DSN 一致。
- 已关闭的说明变更：`yijie-api/config/workflow-local-runtime.schema.json:25` 的 `x-coze-environment` 明确记录 `YIJIE_WORKFLOW_COZE_LISTEN_ADDR=0.0.0.0:18889` 和 DSN `parseTime=true`；`yijie-api/docs/workflow-local.md:35` 增加部署输入表和遗漏后的实际后果。没有修改 runtime 代码、wire schema、source lock 或任何 Coze 文件。
- 未知：第 4 步尚未创建实际拓扑；容器 DNS、挂载 UID、数据库连接与 listener 可达性仍须正常启动后验证。

## 审阅范围与依据

| 边界 | 阅读结论与证据 |
|---|---|
| 请求、响应、状态码 | API Coze client 的 13 项内部调用与 Coze handler 对齐：create 201，test/run 202，其余 200；E 创建/删除两项只属于 API，不属于 Coze 私有面。来源为 `yijie-api/internal/modules/workflows/infrastructure/coze/client.go:106`、`yijie-coze/backend/application/workflowlocal/handler.go:38`，对照 `yijie-contracts/openapi/workflow-local/workflow-local.yaml` 与生成的 `yijie-coze/contracts/workflow-internal.openapi.json`。 |
| 两段凭据 | API 新建 outbound headers，仅 K_AC + run epoch；Coze 拒绝 E 和 Cookie。双方角色独立，与 native 持有 E 的设计一致。证据：API client 第 73–80 行；Coze handler 第 130–148 行。 |
| scope 与资源 | Coze 固定 principal gate 行负责创建/校验 user、space、owner membership；资源同时约束 space、creator、app_id=0 和本 adapter 的 create receipt。API 另有 scope 映射；没有让调用方指定 arbitrary owner/tenant。证据：Coze `localadapter/store.go:65`、`:102`、`:129`；API `application/service.go:29`、`:61`。 |
| 创建、保存与回执 | Coze mutate 在锁定固定 principal 的事务内校验 operation hash、执行写入并登记 receipt。save 使用 expected revision 的 CAS，新 revision 与内容一起写入。API 先持久记录派发意图，再关联 Coze 结果；不确定结果走 operation 查询，不盲目再次派发。证据：Coze `localadapter/store.go:238`、`mutations.go:45`；API `application/service.go:112`、`:183`。 |
| 试运行快照 | 准备执行前保存精确 revision 的原生 snapshot；native runner 使用 commit ID 查询 draft/snapshot，不会把随后保存的草稿作为旧试运行内容。证据：Coze `localadapter/execution.go:46`、`store.go:280`，上游 `internal/repo/repository.go:821`。 |
| 发布与指定版本 | publish 读取同 workflow/space/operator、debug mode、相同 commit ID 的原生成功 execution，并检查本地 test receipt，然后递增 `v0.0.N` 写入版本。run 查询明确指定的 version，使用 FromSpecificVersion；不改成 latest。证据：Coze `localadapter/mutations.go:95`、`:105`、`:116`；`execution.go:75`；`store.go:280`。 |
| 登记与运行完成 | native Prepare 的注册 hook 在 runner goroutine 启动前，将 execution、operation receipt 和 active slot 放进同一事务。completed receipt 只表示登记成功，运行状态来自 native execution。证据：Coze `localadapter/execution.go:100`、`:126`、`:135`、`:144`；`internal/compose/workflow_run.go:280`。 |
| slot 与历史 | slot 仅在原生 success/failed/cancel 后可被下一次运行占用；超时、E 到期、epoch 更新不会直接清空。旧 epoch 非终态投影 unknown；history 用 summary，详情保留结果与三节点输出。证据：Coze `localadapter/execution.go:117`、`:172`；`history.go:98`、`:131`；`store.go:287`。 |
| 原生图与正常测试边界 | Coze policy 校验 start/TextProcessor/end、引用、线性边和文本限额；API只做基础形状和字节预算。读取了 Coze 的普通实际 native engine 测试及其 SQLite/miniredis setup；没有将它当成真实 MySQL 实证。证据：Coze `localadapter/policy.go:49`、`local_test.go:60`、`:235`。 |

## 本次实际检查

- 修改后的 deployment JSON 由 Python `json.loads` 解析：PASS，一次。
- 查看 schema 与文档的完整新增文件 diff，执行 API `git diff --check`：PASS；无运行代码修改。
- 更新 `step3-api-snapshot.json` 中上述两个文件的 SHA-256，并逐项比较其余 26 个文件：摘要均未变化。source lock、测试统计与已构建二进制摘要保留原记录。
- 本轮没有重新运行 API/Coze 的 lint/test/build。既有结果分别参照第 3 步 API、Coze 实施附件，不增加测试次数。

## 未覆盖与影响

- 真实 MySQL 的 DDL、事务隔离、行锁、affected-row 行为、原生表约束以及跨进程竞争：NOT RUN。SQLite 正常测试不能替代这些证据。
- 真实 PostgreSQL migration/事务/append-only audit 与 API→Coze HTTP、Redis、对象存储等原厂依赖启动：NOT RUN。
- Docker 挂载 credential 的实际 owner/euid/nlink、固定 DNS、单一 loopback 出口、正常 stop/reopen 和持久历史：NOT RUN，第 4 步正常验证。
- MessageChannel、native E 生命周期、真实编辑器和三节点桌面完整链路：NOT RUN，后续步骤资格验证。
- 攻击注入、危险 fixtures、权限破坏和强杀恢复测试：按用户硬性安全条款未执行；不能声明这些测试或相应故障恢复能力通过。
