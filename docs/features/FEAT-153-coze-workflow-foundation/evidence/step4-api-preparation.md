# FEAT-153 第 4 步 API 镜像与真实验证准备

日期：2026-09-12。本附件记录 API 代理冻结的实现和本地编译检查；Docker 构建、服务启动、显式 migration 和真实资格由主任务统一调度，结果另行记录。当前不是第 4 步运行通过结论。

## 可调度交付

- `yijie-api/Dockerfile.workflow-local`：`workflow-runtime` scratch 镜像含 server 与 migrate；`workflow-test-runner` 目标含 Go 工具链与新 PostgreSQL 测试，build 时不自动执行测试。`GO_IMAGE` 必填，由 Infra 的镜像锁传入原厂 Go 1.26.5 镜像与 digest，编译采用 `-p=2 -mod=readonly -trimpath -buildvcs=false`、清空 build ID；runtime 为 CGO=0。测试目标启用 CGO/race，缓存写入 `/tmp/workflow-go-build`。
- 专用 Dockerignore 和显式 COPY 只接收 workflows、credential config、同步 DTO/schema、最小 database 包和两个入口。没有把旧业务测试、历史危险 fixtures、private 配置、DSN、bin 或其他仓库送入 context。
- `workflow-local-server --check-ready`：固定 `127.0.0.1:18888/v1/workflow-local/status`，K_NA + epoch，3 秒 deadline，无 proxy/redirect，校验同步源 schema、ready/state/protocol/epoch。仅进行一次已鉴权读取；不启动服务、不连接数据库、不迁移、不 EnsurePrincipal，不接受 URL 参数，可直接用作 scratch 镜像 healthcheck。
- `YIJIE_WORKFLOW_POSTGRES_DSN_FILE`：容器优先采用 file 输入，与旧 direct DSN 环境变量互斥。文件要求绝对路径、普通文件、当前 euid、单链接、0400/0600、≤4096 bytes；使用 no-follow descriptor 与读后稳定复验。内容仅在进程内传入现有配置解析器，不写入 `os.Environ`。原 direct DSN 兼容入口保留。
- 配置 schema 同步 Coze 的 `YIJIE_WORKFLOW_MYSQL_DSN_FILE`、Redis password file、MinIO access/secret file、各自限额与 direct 输入互斥规则。完整部署输入见 API `config/workflow-local-runtime.schema.json` / `docs/workflow-local.md`。

## 真实验证入口与顺序

1. 主任务启动唯一专用栈的依赖，并显式执行 `/usr/local/bin/workflow-local-migrate up`。API 主库只能是 `yijie_workflow_local`，DNS 固定 `workflow-postgres:5432`。此命令使用同一 private config；服务器本身仍不隐式迁移。
2. 正常启动 Coze 和 API，由现有 API 启动流程持久绑定真实 Coze principal；测试不能预先伪造 principal。
3. 宿主执行 `make workflow-qualify-build`，然后标准构建产物 `bin/workflow-local/workflow-local-qualify --evidence <new absolute path>`。仅需 exact local/demo_fast/enable/API profile 和原规范 K_NA 文件；HTTP 地址始终固定 loopback 18888。
4. HTTP 脚本覆盖创建、bootstrap、保存/原 operation replay、普通 stale revision CAS 冲突及其原 operation 查询；真实 debug/test→内部发布 v1，修改前缀后 test→发布 v2；同一第二 revision 使用新 operation 再发布 v3，验证 MySQL 的正常重复 publish 行为；实际执行 v2 后再执行旧 v1，检查两次 debug 与两次 release 的真实 output、三节点历史和分页。图结构与输出名已由 Coze 代理独立只读确认符合其 policy/native fixture。
5. 脚本在 finally 中正常关闭 E。artifact 只包含源生成 workflow/run/receipt DTO 与 attempted operation IDs；没有机器凭据、E、raw headers、DSN 或 raw 服务错误。失败记 `complete: false`；未知写入不盲目重试，不伪造成功。
6. 主任务使用测试 builder 目标，在唯一专用 network 中运行 `go test -p=2 -mod=readonly -race -count=1 -tags=workflowintegration ./internal/modules/workflows/infrastructure/postgres`。设置 `YIJIE_WORKFLOW_PG_QUALIFICATION=normal`，并提供 HTTP 实际创建的 `YIJIE_WORKFLOW_QUALIFICATION_WORKFLOW_ID`。该测试读取上述 private config、既有 migration book、真实 principal/resource；8 个并发 Claim 只创建一个 recorded 意图，再保留明确声明的 storage qualification unknown receipt。它没有运行引擎，不宣称 completed/succeeded。
7. PG 测试仅正常 audit insert/read，静态读取已启用 trigger/function 确认 append-only 定义；不故意 UPDATE/DELETE audit，不清表、不改其他数据库。关闭并重新打开连接后核对 scope/receipt/resource。数据库进程/卷持久性仍须下一项验证。
8. 主任务正常停止并重开整个栈、轮换 epoch 后，宿主使用新 K_NA 执行 `--verify-evidence <same path>`：只发 GET，核对原 workflow、实际运行、receipts、workflow summary 和历史。此模式不创建新工作流、不再次执行版本。

测试 builder 需要挂载同 UID 的 K_NA、K_AC、PG DSN 文件；Go cache/temp 由容器正常可写临时目录承载。无需发布 PostgreSQL/MySQL 宿主端口。没有 shell/curl healthcheck 依赖。

## 实际完成的非破坏性检查

使用缓存原厂 Go `/Users/jack/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.5.darwin-arm64/bin/go`，统一 `GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off`。

| 检查 | 结果与次数 |
|---|---|
| `go test -race -count=1 ./internal/workflowlocal ./cmd/workflow-local-qualify` | PASS，1 次；runtime config 两个顶层正常测试，qualifier 无单元测试。 |
| `go test -race -count=1 ./internal/workflowlocal` | PASS，1 次；将 DSN 不写环境的断言改为检查实际 process environment 后复验。 |
| `go test -tags=workflowintegration -run '^$' ./internal/modules/workflows/infrastructure/postgres` | PASS，1 次，仅编译新 PG 测试，明确输出 `[no tests to run]`；没有数据库连接。 |
| `make workflow-lint workflow-qualify-build workflow-build` | PASS，1 次；新增范围 gofmt/vet、canonical consumer/source check、正常宿主构建。 |
| `make workflow-qualify-build` | PASS，1 次；补 workflow summary 与 response headers 核验后重建 qualifier。 |
| `make workflow-lint workflow-build` | PASS，1 次；增加固定地址 readiness helper 后重建 server/migrate。 |
| 独立 canonical consumer check | PASS，1 次；其他三次由以上 Make 构建统一执行。旧 public/Runtime lock 未改。 |
| deployment JSON 解析 / `git diff --check` | PASS。11 项第 4 步文件和三个宿主产物摘要见 `step4-api-preparation-snapshot.json`。 |

上述宿主构建产物尚未被本代理执行。未复跑历史默认全仓测试；无需下载或改动 go.mod/go.sum。旧 api-server/app/全局 migration/public lock/public DTO 与 go.mod/go.sum 7 项保护文件仍与 HEAD 字节相同。

## 明确未执行

本代理没有 Docker build/start/run，没有执行实际 migration，没有连接真实 PostgreSQL/MySQL/Coze，没有执行 HTTP qualifier、healthcheck 或正常整栈 stop/reopen。主任务随后运行的结果必须以实际输出另记，不能从本附件的编译 PASS 推断运行 PASS。

强杀、攻击注入、恶意 fixtures、权限破坏、故意破坏 audit 的异常测试均未执行，受用户长期安全条款禁止。测试记录不会把跳过项换算成通过，也不会把 storage unknown 探针当成真实工作流成功。
