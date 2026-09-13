# FEAT-153：Coze 工作流引擎接入前静态审计

- 审计日期：2026-09-12。
- 范围：`yijie-coze` 的工作流 API 调用链、身份与资源归属、编辑器依赖、节点能力、存储及正常启动/停止路径。
- 方法：只读源码、构建与部署配置；未启动服务、安装依赖、执行测试、调用业务 API 或读取真实秘密。收到主代理写入指令后，仅新建本审计附件。
- 证据路径：下文所有 `backend/`、`frontend/`、`docker/`、`scripts/`、`Makefile` 路径均相对兄弟仓库 `yijie-coze/`，行号来自本次读取的现有源码。
- Git 来源、文件完整性、远端接入情况由 FEAT-153 独立来源审计附件负责；本附件不重复推断来源，也不证明镜像与源码一致。

## 结论与适用边界

现有源码具备无需模型的工作流创建、保存、重新读取、试运行、发布内部版本、运行及结果查询路径，适合作为易界工作流引擎候选。建议保留独立 Coze 前后端构建与存储边界，先做固定本地 identity/space 的基础集成，再扩展电商业务节点。

当前不能直接把 Coze Web API 视为易界公开或多租户授权边界，不能把启动容器、创建空画布或已有单元测试存在视为基础集成完成。下文涉及资源归属和 PAT 的发现均为**静态代码审计发现，未实跑、未进行利用验证、未证明真实部署存在可利用漏洞**。public/production 问题应登记并在对应暴露前收口；不据此将本需求扩大为完整生产多租户改造。

优先级定义：P1 表示对应接入或暴露前必须收口的问题；P2 表示需要明确产品限制、验证或后续修复的可靠性问题。每项单独说明是否阻塞受控的 `demo_fast + local`。

## 真实能力与调用链

路由定义位于 `backend/api/router/coze/api.go:418–451` 和 `:531–544`。下表不是设计中的目标 API，而是当前源码真实路径。

| 能力 | 路径与调用链证据 | 对基础集成的含义 |
| --- | --- | --- |
| 创建 | `POST /api/workflow_api/create` → `backend/api/handler/coze/workflow_service.go:53` → `backend/application/workflow/workflow.go:239–279` → `backend/domain/workflow/service/service_impl.go:105–125` | 创建元信息并保存初始化草稿，尚未形成可运行流程 |
| 保存 | `POST /api/workflow_api/save` → `backend/application/workflow/workflow.go:316–320` → `backend/domain/workflow/service/service_impl.go:128–163` → `backend/domain/workflow/internal/repo/repository.go:343–357` | 保存 canvas、输入输出、试运行状态；每次生成草稿 commit ID |
| 重新读取 | `POST /api/workflow_api/canvas` → `backend/application/workflow/workflow.go:448–457` → `backend/domain/workflow/internal/repo/repository.go:545–580,821–844` | 可重新读取草稿；指定 commit 时还可能读取快照 |
| 试运行 | `POST /api/workflow_api/test_run` → `backend/application/workflow/workflow.go:540–572` → `backend/domain/workflow/service/executable_impl.go:208–301` | Canvas 转内部 schema、编译、建立 execution 并异步执行 |
| 试运行结果 | `GET /api/workflow_api/get_process` → `backend/application/workflow/workflow.go:670–698` | 读取工作流执行和节点结果；相应节点历史端点也已注册 |
| 发布内部版本 | `POST /api/workflow_api/publish` → `backend/application/workflow/workflow.go:2169–2183` → `backend/domain/workflow/service/service_impl.go:695–744` | 版本须递增，默认要求试运行成功；本需求入口不应传入绕过条件的 `Force` |
| 运行发布版 | `POST /v1/workflow/run` → `backend/application/workflow/workflow.go:1741–1754,1799–1847` | 未发布会拒绝；支持同步和异步，返回 execute ID |
| 发布版运行记录 | `GET /v1/workflow/get_run_history` → `backend/application/workflow/workflow.go:1864–1912` | 按 execute ID 查询输入、输出、状态和错误；不能把它误写成已有分页运行列表 API |

Web 编辑 API 使用 Coze session cookie，证据为 `backend/api/middleware/session.go:55–71`；OpenAPI 使用 PAT，证据为 `backend/api/middleware/openapi_auth.go:113–159`。仅配置 PAT 不能打通完整编辑器。

## 无模型最小闭环

建议使用合成文本完成“输入字符串 → 文本处理节点拼接固定前缀 → 输出字符串”。不需要调用代码执行器、HTTP、插件、模型或真实商家平台。

| 部件 | 当前实现证据 |
| --- | --- |
| 开始节点 | `backend/domain/workflow/internal/nodes/entry/entry.go:87–114`：纯输入映射与默认值 |
| 文本处理节点 | `backend/domain/workflow/entity/node_meta.go:436–451`：节点 ID 15，TextProcessor；`backend/domain/workflow/internal/nodes/textprocessor/text_processor.go:96–170`：concat/split 实现，不调用模型或代码运行器 |
| 结束节点 | `backend/domain/workflow/internal/nodes/exit/exit.go:102–120`：`returnVariables` 返回映射 |
| 节点注册 | `backend/domain/workflow/internal/canvas/adaptor/to_schema.go:597–645`：已注册上述节点的适配器 |
| 模型缺省 | `backend/application/base/appinfra/app_infra.go:142–150`：内建知识召回模型未配置时警告；该事实仅证明此处未强制要求模型，不等于整个部署已经无模型启动成功 |
| 默认画布 | `backend/domain/workflow/entity/vo/canvas.go:678–750`：开始/结束节点、结束引用为空、`edges: []`；创建后必须实际配置节点、引用和连线 |

产品流程应体现草稿、试运行和内部发布版的区别：创建 → 编排与保存 → 重新打开 → 试运行 → 发布内部版本 → 运行 → 查看结果与历史。此处“发布”是工作流内部版本管理，不是生产部署。

## 发现清单

### C-01｜P1｜本地身份与编辑会话桥接缺失

**事实。** `frontend/apps/coze-studio/src/routes/index.tsx:254–261` 的工作流页面设置 `requireAuth: true`；`backend/api/middleware/session.go:55–71` 要求 Coze session。

**影响。** 沿用 Coze `/sign` 注册登录流程会破坏易界 ADR-0018 的正常本地直达；只提供 OpenAPI PAT 也不能支持现有编辑器。阻塞固定本地 scope 的完整产品闭环。

**最小收口。** 由易界 API/Coze 内部适配建立固定 local user/space 与编辑会话；浏览器不接触长效 PAT；不能依据客户端提交的任意 user/space 建立身份。仅实现当前本地 scope，不在 FEAT-153 中扩展为完整生产账号系统。

**验证。** 从易界正常入口直接进入工作流页面并创建、编辑、返回；无 Coze 注册登录前置；确认服务端映射与请求使用同一固定本地 scope。

### C-02｜P1｜正常启动脚本存在额外安装、格式化和构建写入

**事实。** `scripts/setup/server.sh:35–40` source env 并可能通过 curl 安装 Deno；`:47–56` 在检测到 goimports 后自动格式化大量后端源码；`:62–64,83–90` 删除重建本项目 bin/config。`Makefile:35–41` 的 server 入口会调用该脚本。

**影响。** 不能把 `make server` 当作无副作用启动或普通检查直接运行。阻塞安全、可预测的易界正常启动入口，但不意味着禁止使用标准构建工具产生可复现的本项目构建产物。

**最小收口。** Infra 提供明确的构建与启动步骤；正常易界启动不隐式安装工具、不全仓格式化、不清理已有数据。保留上游脚本，分开依赖准备、canonical build 与运行。构建输出须明确属于当前项目、可复现，不能覆盖未知来源或用户提供的既有二进制。

**验证。** 先静态检查正常入口，再执行标准构建及启动，记录构建来源和前后 Git 状态；不调用 clean，不通过权限破坏或二进制替换制造异常。

### C-03｜P1｜镜像浮动与后端 readiness 证据不足

**事实。** `docker/docker-compose.yml:389,421` 使用 latest；Coze Web 在 `:431–432` 仅依赖 Coze server 已启动，server 部分 `:385–415` 没有应用健康检查。

**影响。** 无法仅据现有 Compose 证明运行的代码等于审计源码或后端已经可用。阻塞可复现的本地验收基线。

**最小收口。** 固定来源对应的构建或不可变镜像，验证后端 API readiness 与编辑器资源就绪，记录实际构建引用；不能依据容器 Started 放行。

### C-04｜P1｜本地节点范围与运行上限须由后端约束

**事实。** `backend/domain/workflow/internal/execute/consts.go:24–28` 中执行超时与节点数量上限均为 0，注释含义为无限制。现有引擎注册的节点远多于基础集成需要。

**影响。** 直接暴露完整节点集会扩大本地实现与验收范围。本需求不需要任意代码、外部 HTTP、插件、模型、循环或商家凭据；仅隐藏 UI 不能限制请求中的节点。

**最小收口。** FEAT-153 UI 和服务端共同限定开始、文本处理、结束及受支持的无环编排，限制正常输入大小与节点数。产品边界和校验契约应由本需求先定义；不把本地范围限制写成生产沙箱已经合格。

**验证。** 正常三节点编辑与运行；使用普通不完整配置触发表单/服务校验，修正后成功。不得编制攻击载荷或故意制造死循环测试。

### C-05｜P1｜Web API 资源归属与请求 space 的绑定缺口（静态发现）

**事实。** `backend/application/workflow/workflow.go:316–320` 的 SaveWorkflow 先验证请求提供的 space_id，再按 workflow_id 保存；Canvas、TestRun、Publish 分别在 `:448–457,540–553,2169–2180` 呈现同样模式。`checkUserSpace` 在 `:3897–3915` 仅检查传入 space 是否在用户列表中；`backend/domain/workflow/internal/repo/repository.go:343–357` 的保存也未附加资源真实 space 条件。

**结论边界。** 这是对已读取调用链的资源归属绑定缺口判断，**未执行跨用户/跨租户请求、未利用验证，不宣称已验证真实部署漏洞**。OpenAPI Run/History 会先获取真实资源 space 再检查（`workflow.go:1741–1754,1864–1875`），不能据此推断 Web API 也具备同样边界。

**影响与范围。** 阻塞 public/production 或不可信客户端直接使用这些 Web API。对于当前受控单用户 local，可在服务端固定资源映射、禁用任意 scope 输入、限制网络暴露后继续，不要求在本需求完成所有上游 API 的多租户治理。

**最小收口。** 易界 API 根据服务端持有的 workflow→固定本地 scope 映射访问；如直接复用 Coze 编辑写 API，适配路径须核对 workflow 的真实 SpaceID。公开前另行逐资源核权，不能把前端 space 当作授权事实。

**安全验证。** 审阅映射、资源读取与服务端判断代码；以正常固定 scope 流程记录资源 ID 和归属一致性。未执行攻击或越权利用测试。

### C-06｜P1｜内容日志不适合真实账号和商家数据

**事实。** `backend/api/middleware/log.go:64–79` 在 debug 日志输出 query、request、response 片段，各最多 3 KiB。可能包含用户输入、登录或运行结果。`backend/api/middleware/openapi_auth.go:153` 还记录 API key 元信息；但当前 CheckPermission 返回值在 `backend/domain/openauth/openapiauth/api_auth_impl.go:118–124` 没有填入 token 字段，不能误报为已经确认输出明文 PAT。

**影响与范围。** 受控 local 使用合成文本并禁止 DEBUG 内容日志可继续；引入真实账号、凭据或商家数据前必须收口。

**最小收口。** 基础集成只保留 allowlist 的必要状态元数据日志，不记录 body、cookie、token 或真实用户内容。通过日志配置和代码复核，不以真实秘密作为测试输入。

### C-07｜P1｜现有 PAT 机制不能直接作为易界公开凭据体系

**事实。** `backend/domain/openauth/openapiauth/internal/dal/api_key.go:91–97` 按 ID 确定性派生 PAT；已读取的验证链 `backend/domain/openauth/openapiauth/api_auth_impl.go:109–125`、`backend/application/openauth/openapiauth.go:221–230` 比对 key，未见 ExpiredAt 校验。

**结论边界。** 静态发现，不曾生成、猜测、获取或调用任何真实 token，也没有验证可利用性。

**影响与范围。** 阻塞将此机制直接用作易界 public/production 身份凭据。local 可使用受控内部适配，避免依赖用户手工创建公开 PAT 的登录流程。

**最小收口。** 不把 Coze PAT 作为易界用户身份权威；如 local 内部调用采用 PAT，凭据须进程管理且不暴露给前端。public 前另行完成随机性、有效期、权限及秘密管理审计。

### C-08｜P2｜创建与发布存在部分成功状态

**事实。** 创建依次写 meta、draft，再通知搜索；通知失败可能返回错误但元信息已经存在，见 `backend/domain/workflow/service/service_impl.go:105–125`、`backend/application/workflow/workflow.go:279–293`。发布依次更新引用、version、draft、meta，meta 更新错误在 warn 后仍返回 nil，见 `backend/domain/workflow/internal/repo/repository.go:288–340`。

**影响。** 不应承诺原子发布或安全自动重试；首次本地闭环仍可正常验证，但返回成功后必须读取确认真实状态。

**最小收口。** 创建、保存、发布后重新读回；普通重试前先查询，防止盲目重复创建/发布同版本。事务、幂等和失败补偿作为后续可靠性工作，不需要为证明问题执行故障注入。

### C-09｜P2｜进程内异步执行不等于持久任务调度

**事实。** `backend/domain/workflow/internal/compose/workflow.go:160–170` 通过 goroutine 运行；`backend/domain/workflow/service/executable_impl.go:289–301` 建 execution 后调用 AsyncRun。Redis checkpoint 期限为 7 天（`backend/infra/checkpoint/redis.go:34–51`）；中断事件期限 24 小时（`backend/domain/workflow/internal/repo/interrupt_event_store.go:41`）。

**影响。** execution 落库和 checkpoint 存在不能证明进程停止后自动恢复、在途 drain、定时调度、重试补偿或可靠消息投递。不是短流程本地集成的阻塞项，但不能把这些能力写为已交付。

**最小收口。** 仅承诺短流程正常执行和已完成记录持久化；停止前让当前运行完成。FEAT-153 不承诺跨进程在途恢复、定时任务、补偿及持久队列。

## 编辑器边界

可复用独立 React 页面 `/work_flow?space_id=...&workflow_id=...`；参数读取位于 `frontend/packages/workflow/adapter/playground/src/hooks/use-page-params.ts:25–68`，支持 execute_id 定位运行结果。`frontend/packages/workflow/adapter/playground/src/page.tsx:60–102` 暴露 onBackClick/onPublish，可接入易界返回行为。

该页面不是独立的小型可安装组件。`frontend/packages/workflow/adapter/playground/package.json:8–24` 使用 Rush workspace，包自身 build 为 `exit 0`，必须构建实际 app bundle。画布读取 Coze space store（`frontend/packages/workflow/playground/src/workflow-playground.tsx:69–85`）；初始化还读取节点、变量、模型列表（`frontend/packages/workflow/playground/src/services/workflow-save-service.ts:307–328`）。无模型工作流不等于可以删除模型列表端点。

建议保留独立前端构建，限制入口、节点与返回衔接，不在首轮将 React 包整体移植到 Vue。后端亦是全应用初始化：`backend/application/application.go:123–168,214–230` 初始化用户、插件、Memory、Knowledge、Search 等，不能简单复制 workflow 目录就声称得到可独立运行引擎。

节点扩展已有适配注册机制，但本轮仅使用现有 TextProcessor。后续电商能力节点应经易界 Connectors 既有权限与凭据边界调用，不把平台 token 存入画布或节点输出。

## 部署、持久化与正常停止

- `backend/application/base/appinfra/app_infra.go:67–123` 初始化 MySQL、Redis、OSS、ES 和事件生产者。现有 Compose 还包括 MinIO、etcd、Milvus、NSQ；首轮保持上游应用边界，依赖瘦身另行评估。
- 草稿、内部版本、workflow/node execution 在 MySQL。持久化证据为 `backend/domain/workflow/internal/repo/repository.go:299–357`、`backend/domain/workflow/internal/repo/execute_history_store.go:74–96,202–205,321–329`。
- 流式临时结果、取消标记、中断和 checkpoint 使用 Redis，证据为 `backend/domain/workflow/internal/repo/execute_history_store.go:300–307`、`backend/infra/checkpoint/redis.go:34–51`。Redis 不应一概归类为可丢弃缓存。
- 工作流仓库还依赖 OSS 与搜索通知，见 `backend/application/workflow/init.go:89–110`、`backend/application/workflow/eventbus.go:43–57`。现有 `docker/docker-compose.yml:352–370` 的 nsqd 配置未见持久数据 volume；不能据此承诺搜索通知持久投递。
- 正常停止入口可参考 `Makefile:79–85` 的 Compose down，并保留数据；`Makefile:87–89` 的 clean 会删除 docker/data，不得作为本需求验收清理手段。
- HTTP 服务调用 Hertz `Spin()`（`backend/main.go:104`），共享信号等待工具监听正常退出信号（`backend/pkg/lang/signal/signal.go:25–28`）。未验证服务停止时是否完整等待在途工作流。停止脚本必须优先正常退出，不能升级强杀来伪造完成；无法安全退出时报告而不强制继续。

## 可正常执行的验收建议

以下为后续基础集成的建议验收，**本次均未执行**：

1. 固定已审计构建来源、明确依赖和安全启动入口，记录环境及各仓现有变更。
2. 从易界正常本地入口进入工作流，无第二套注册登录或用户手工 PAT 配置；检查固定身份与 scope 的服务端绑定。
3. 创建合成流程，实际编辑开始、文本处理、结束三个节点及输入引用与连线；保存后关闭编辑页，再重新打开验证一致性。
4. 试运行普通输入字符串，检查结果为预期前缀加原文，并有三节点实际执行记录。
5. 试运行成功后发布内部版本；重新读取发布状态和版本，再通过真实服务运行发布版。结果与 workflow ID、version、execute ID 对应。
6. 使用普通的缺失必填输入或不完整节点配置验证清晰的校验提示；修正配置后重试成功。此步骤仅正常表单校验，不包含攻击载荷、恶意资源、权限破坏或故意死循环。
7. 短流程完成后正常停止并重启，确认草稿、内部版本和已完成历史仍可读取。不得声称此项证明在途执行恢复。
8. 检查实际界面加载、返回、刷新、错误提示和结果展示；检查日志仅含允许的状态元数据，记录实际服务端结果与前后工作区状态。

现有 `backend/api/handler/coze/workflow_service_test.go:179–219` 测试直接提供 session/auth context；`:264–278` 连接固定测试 MySQL 并使用 miniredis；`:288–322` mock 领域服务、搜索通知和身份。它们可以作为实现参考，不能代替真实身份与存储的最终 E2E；不得未审阅便对用户当前 MySQL 运行整套测试。

## 未执行事项、原因和影响

| 未执行事项 | 原因 | 对结论的影响 |
| --- | --- | --- |
| 全栈安装、构建、启动、模型配置 | 接入前只读审计范围；现有启动脚本有需先收口的隐式写入 | 尚未证明本机完整构建与无模型启动可用 |
| 正常 API/编辑器端到端验收、持久化重启 | 本次未启动服务 | 调用链与节点证明技术路径存在，不等于 D4 或真实可用性通过 |
| 跨用户/跨租户利用请求、PAT 猜测及攻击注入 | 用户禁止攻击注入测试；审计仅读代码 | 资源归属和 PAT 问题是静态发现，未证实真实部署的可利用性 |
| 强杀、故障注入、权限破坏、二进制替换、危险 fixture | 用户长期安全条款禁止 | 未验证异常崩溃恢复；后续采用正常停止、合成数据及普通校验路径 |
| 全上游测试套件 | 测试包含固定数据库、mock 和不同节点依赖，未获本轮运行范围 | 不宣称上游测试通过，不以 mock 结果代替基础集成验收 |

本附件支持 FEAT-153 的边界和分步实施决策；运行通过、公开安全合格、生产可用性均须由后续真实证据单独证明。
