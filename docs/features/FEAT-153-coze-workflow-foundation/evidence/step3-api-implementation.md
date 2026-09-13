# FEAT-153 第 3 步 API 实现与安全验证

日期：2026-09-12。API 基线 `f9d730a157bcb012a8fe178cbfebcd4ea27419fc`。
结论：独立 workflow-local API 候选已实现，安全 focused lint/test/build 通过；未启动真实服务或执行数据库 migration，不是第 4/5/6 步或 D4 通过。

## 已实现

- `yijie-api/cmd/workflow-local-server`：exact local/demo_fast/workflow enable/专用 API profile；固定主机 loopback 或明确 container 内部监听。启动校验独立 schema，再经真实 Coze client 正常 EnsurePrincipal、API 事务 BindPrincipal，成功后才打开 listener；不要求 Desktop 先手动 POST principal 才能 ready。
- `cmd/workflow-local-migrate`：显式 `up`，独立 goose Provider/book 与独立数据库 `yijie_workflow_local`。服务器启动不隐式迁移；旧 API migration version 4 不变。
- `internal/modules/workflows`：domain/application/HTTP/Coze/PostgreSQL 分层；使用源生成 DTO 的显式 mapper，按已同步 source schema 检查所有 HTTP 输入输出。
- 四张私有表：固定 principal、scope 资源映射、operation 意图/摘要/receipt、append-only audit；图、revision 内容、版本及执行事实不复制到 API 数据库。
- create/save/test/publish/run 先记录意图，再向 Coze 同一 operation ID 派发；重复请求先查询/读回，内容变化明确冲突。unknown 不自动重启作业，receipt completed 只代表资源/execution 登记。
- K_NA/K_AC 两段独立文件/epoch/令牌；API 每个业务请求验证机器凭据和 epoch，Coze client 只发送 K_AC、固定 epoch，不转发 E、Cookie 或客户端任意 headers。无环境代理、redirect 或通用浏览器 CORS 代理。
- E 独立随机、资源绑定、300 秒绝对过期、仅 API/native 内存；JSON secret 仅由具名 native transport 持有。open 201、幂等 close 200，close 不要求未过期 E；bootstrap/save/test/publish 要求 E。API 正常退出清除 E，不冒称取消引擎执行。
- Credential reader 使用 `O_RDONLY | O_NOFOLLOW | O_CLOEXEC`，检查 descriptor/path 的 regular、当前 euid、0400/0600、nlink=1、≤1 KiB，并在读后复核稳定身份/大小/模式/修改时间。正常测试创建新的 owner-only 文件，没有制造 symlink/hardlink/权限故障。
- API 校验 UTF-8 input/canvas/prefix 字节预算、2–3 节点/≤2 边、仅 type 1/15/2 和禁止嵌套子图；完整原生引用/可执行性/CAS/槽位由 Coze 最终执行。未完成的正常双节点草稿可保存。
- 列表使用新 WorkflowSummary/RunSummary。完整 JSON 先序列化、source 校验并检查 512 KiB 后才写 HTTP header/body，不能截断 JSON。写入后响应构造失败返回原 operation ID 的 operation_unknown；请求校验阶段的大输入仍是确定拒绝。
- 保留原生 unknown/terminal 语义；空字符串输出与输出缺失分别保留。
- 正常 Interrupt/SIGTERM 使用 Server.Shutdown，无强制 Close 或 kill fallback；30 秒未结束只报告 pending 后继续等待正常清理。

配置来源为 `yijie-api/config/workflow-local-runtime.schema.json`，使用说明为 `yijie-api/docs/workflow-local.md`。Coze DNS `coze-workflow:18889`、API PG DNS `workflow-postgres:5432`，Coze MySQL 约束同步写入部署 schema。静态 editor 第 5 步实现，本步未开放未完成的静态代理。

## 实际验证

在 `yijie-api` 执行最终命令：

```sh
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off make workflow-lint workflow-test workflow-build WORKFLOW_GO=/Users/jack/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.5.darwin-arm64/bin/go
```

结果：exit 0。包含新增范围的 gofmt 检查、go vet、Contracts canonical consumer checksum/source lock 同步检查、`go test -race -count=1` 与两项 canonical 二进制构建。Go 1.26.5 使用已有原厂缓存，本轮无需下载依赖、修改 go.mod/go.sum 或替换现存 Runtime。

**16 个顶层 focused tests 通过**，其中正常路由测试含 **9 个具名子用例**；editor 生命周期用例另覆盖 save/test/publish，所有 15 项 HTTP operations 的正常状态码与 source 响应形状均被 exercised。16 项分布：application 4、domain 1、Coze HTTP client 2、API HTTP 5、transport 2、runtime config 2。统计只指这些新测试，不是全仓测试数。

覆盖正常创建/重试/内容冲突、recorded→completed 查询核对、unknown 引擎结果、资源不存在、E 到期/关闭、摘要分页、UTF-8 文本上限、空输出、正常 JSON 空白导致的响应包络膨胀，以及写后响应失败的原 operation ID。没有运行攻击 payload、危险归档、权限破坏、异常进程或真实业务请求。

构建文件位于 API 仓被忽略的标准项目产物目录：

- `bin/workflow-local/workflow-local-server`
- `bin/workflow-local/workflow-local-migrate`

仅正常构建，没有执行这些二进制。源码清单、产物 SHA-256、实际测试名称和受保护文件摘要见 [step3-api-snapshot.json](step3-api-snapshot.json)；最后一次命令及完成输出见 [step3-api-checks.txt](step3-api-checks.txt)。`git diff --check` 实际通过。

## 独立审阅修正

主任务预审发现的写后响应错误歧义已修正：不再将已发生副作用后的序列化/容量问题作为 input_too_large 确定拒绝，始终保留原 operation ID 的 unknown。正常容量测试覆盖该路径。

跨端 ready 初始化问题已修正：API 启动正常 Ensure/BindPrincipal 完成后才监听，Desktop 的 ready-first 调用不会陷入必须先手动 principal POST 的死锁。

Credential reader 的初版 Lstat→Open 检查已按联审修正为 descriptor no-follow、nlink 与读后稳定验证；只通过正常 owner-only 文件验证，不用危险 fixture 验收。

以下受保护文件与基线逐字相同：旧 `cmd/api-server/main.go`、`internal/app/app.go`、旧全局 migrations.go、`contracts/public-api.lock.json`、旧 public `types.gen.go`、go.mod、go.sum。API 仅在 AGENTS/README/Makefile 加入本需求说明及独立入口，修正“旧 API 尚无 lock”的过时事实，没有关闭旧生成门禁。

## 限制与未执行项

| 项目 | 当前真实状态和影响 |
|---|---|
| PostgreSQL migration/事务/append-only trigger/正常数据重开 | NOT RUN。SQL 已实现并嵌入编译；测试 repository 为单元端口，不能替代真实 PG 事务或持久化证明。第 4 步需要真实独立数据库验证。 |
| 真实 Coze HTTP adapter、引擎运行、跨仓 principal/操作关联 | NOT RUN。client 使用正常 httptest server 验证传输/映射；不是实际 Coze 服务资格。 |
| 旧写入 full Workflow 重放 | 已完成 create/save/publish 若之后草稿 revision 已变化，API 不回传新草稿冒充旧结果；返回原 ID 的 operation_unknown，而 GET operation 仍提供真实 completed receipt。要返回旧完整画布需要明确历史 revision provider/source 能力，API不保存第二份canvas。 |
| 完整原生图合法性/引用/CAS/试运行成功绑定/运行槽位 | Coze 实现为最终权威；API当前做通用图/字节/类型限额，不声称其map检查就是完整引擎校验。真实联测尚未执行。 |
| Credential 容器挂载 | nlink/owner/euid严格校验；第 4 步须核对实际容器 USER 与只读文件UID，不靠调整既有权限或跳过校验过门禁。 |
| Docker、readiness、正常 stop/reopen、editor/MessageChannel/native资格 | NOT RUN。机器端口/来源/退出模型目前为代码与设计，未产生第 4/5 步的运行证据。 |
| 历史默认全量测试与攻击/权限故障/强杀测试 | NOT RUN，用户硬性安全条款禁止。没有声明全仓绿色或这些异常恢复能力。 |
| Public/production、模型/平台/付费调用、commit/push/tag | 未执行，模型和业务调用均为 0；local candidate 不等于 release 或生产兼容批准。 |

本附件只完成 FEAT-153 第 3 步中的 API 实现与安全本地检查。跨仓集成、真实数据层验证和最终 D4 由后续步骤继续，不能把本附件状态换算为完整工作流已经可用。
