# FEAT-155 第一阶段实施报告

2026-09-18：用户授权“只修订上述方案定义，再实施第一阶段的契约与两类只读查询”。已完成该范围及定向检查，停在第一阶段。整体FEAT-155仍在实施中，十项Must未验收，D4 NOT RUN；没有启动Desktop/Host真实服务、Runtime、Provider或访问用户日常数据库。

## 1. 审计定义已收敛

| 审计项 | 已落实定义 | 实施边界 |
|---|---|---|
| 查询权限 | 精确local/demo_fast；Host bearer、规范ID及session-operation关联；Trace不作身份权威 | 本阶段已实现；Desktop authority/plan/conversation scope在第三阶段消费时落实 |
| 实例来源 | responding_host_instance_id仅描述响应Host；缺失省略并保持unknown，不能证明旧执行已终止 | 已实现字段和缺省/变化测试；无历史generation字段或DB迁移 |
| 睡眠恢复 | sleep/wake监听、恢复屏障和不补跑须先于第三阶段自动触发；第四阶段只接防空闲睡眠开关/展示 | 只修订方案，本阶段无电源代码 |
| 有限授权 | native绑定计划/revision、grant、次数及期限；耗尽/到期停止新投递；内容/时间/目标变更重确认 | 只修订方案；阶段二、三再细化存储/IPC；12次验收总账不替代产品授权 |

没有引入云调度、多租户Host、常驻服务或计费平台。超过16小时仍可继续；系统通知继续延期。

## 2. 实际改动

Contract-impact：**本阶段additive**，整体未来存储兼容影响仍按原breaking处理。先在Contracts形成源、生成并通过校验，再同步Host候选并实现；没有手写wire DTO或修改既有consumer pin。

- Contracts：独立OpenAPI `openapi/scheduled-task-recovery/scheduled-task-recovery.yaml`、受限计划草案schema、Go类型与同源JSON Schema投影、leaf generate/check/sync、5项schema测试、来源manifest和兼容说明。草案只有澄清/候选两种结果；不调用模型、不透传任意outputSchema、不保存计划。
- Host：`internal/session/scheduled_recovery.go`通过同一db.View读取既有task索引/会话；投递查询调用既有TurnOperation组合键读取。`internal/app/scheduled_recovery.go`注册两个GET并显式映射生成DTO。既有创建、投递、审批、Runtime和bbolt schema 5保持。
- 元仓：修订03—05、00/01/02及feature.yaml，记录本报告和源摘要。保留原调查记录，不把历史pending或文档检查写成产品通过。
- Desktop、Codex：HEAD及工作区保持原样，未修改页面/native逻辑、lockfile、数据或二进制。

新增接口：

| 查询 | 返回的已有事实 |
|---|---|
| GET /v1/tasks/{task_id}/agent-session-mapping | task/session及可选thread；reserved或bound仅表示持久映射情况 |
| GET /v1/agent-sessions/{agent_session_id}/turn-operations/{operation_id} | 原operation的pending/accepted/uncertain；只有accepted带原turn ID |

两个接口均经现有owner-only bearer，拒绝非规范ID和query/body参数，所有响应no-store。没有Runtime读取/执行、resume、审批决定、重试或写事务。404也可能来自正常清理；503、pending和uncertain保持未知，accepted不表示原生终态或业务成功。不返回cwd、Trace、正文、凭据、输入摘要或原始内部错误。

## 3. 来源与兼容

本轮起点：

| 仓库 | 完整HEAD |
|---|---|
| Contracts | db4458fe94572c4df41a114005d54a049bb79b1f |
| Host | 0e47766f494977c94bfea0e89cfbdf45a7fafa2b |
| Desktop | 4a8a67bec4903624ca98a1098572fa26f3a20849 |
| Codex | 6c1ad767f0997845b8258a1c452fd4eb7577579f |
| 元仓 | 2f616f4d24c001812c6279a520ba69ea9875247e |

元仓起始已有ADR索引和FEAT-155文档改动，本轮保留；两个实现仓起始clean。实际25个Contracts/Host源、生成物、测试及说明文件摘要见[证据](evidence/phase-1-source-20260918.json)。这些HEAD是起点，**不是包含本轮改动的提交**。

独立manifest记录base、全部源/生成物SHA-256及oapi-codegen/v2@v2.7.2身份，mode=local_candidate/release=false。Host精确复制源及生成DTO，check验证一致。旧通用generator、package/依赖锁、原OpenAPI族、旧SDK、Host旧锁和Store格式未变；无新增依赖安装。

已逐一运行现有breaking脚本，全部退出0：

- 当前fallback：db4458fe94572c4df41a114005d54a049bb79b1f。
- 已发布支持：f16a497e1377f45747f8ff9292b4b60cf2027f88。
- native-v1来源：6f632f155eacdaf93df0e0b00b5dab9e369c5442。
- native-v2来源：811f38d6b104fa18477107e7ac91a85e19c445d1。

脚本验证旧OpenAPI/Proto/AsyncAPI/JSON Schema的结构兼容；新族在这些基线不存在，由新增源lint/conformance及路径审查验证。旧源/生成物相对当前fallback逐字节未改另行核对。没有声称工具检查证明生产、多租户或端到端兼容。

部署顺序仍为源契约→Host支持→后续Desktop消费。没有合并、提交、推送、tag或发布；local候选不能充当不可变发布来源。回退本阶段不涉及DB降级；未来consumer遇到旧Host/缺失查询保持unknown并阻断依赖它的自动投递。

## 4. 实际检查

| 仓库/命令 | 结果与范围 |
|---|---|
| Contracts `make scheduled-recovery-generate` | PASS；只生成本族Go/schema/manifest |
| Contracts `make scheduled-recovery-check scheduled-recovery-test` | PASS；确定性生成及5项schema测试 |
| Contracts `pnpm exec redocly lint openapi/scheduled-task-recovery/scheduled-task-recovery.yaml --config redocly.yaml` | PASS；现有recommended配置；早先minimal配置亦通过 |
| Contracts `go vet ./sdks/go/openapi/scheduled-task-recovery` | PASS |
| Contracts `bash scripts/check-breaking.sh <上述每个完整SHA>` | 四个基线均PASS |
| Host `make scheduled-recovery-check` | PASS；来源摘要、可再生、consumer逐字节一致 |
| Host `go test -race ./internal/session ./internal/app -run '^TestFEAT155Recovery' -count=1 -v` | PASS；4个顶层测试，HTTP三状态子例；正常Store关闭/重开/清理、同operation跨session、重复读取无写事务、缺省/变化实例、400/401/404/503、精确local开关、schema conformance |
| Host `make lint` | PASS；gofmt检查、go vet全包和Shell语法；没有运行历史测试 |
| Host已审查6项旧测试（下列完整名单） | PASS；race检查 |
| 三仓 `git diff --check`及元仓strict/D0/audit-claims、pnpm lint/test、Shell语法 | PASS；元仓50/50测试，见02末尾；不代替产品D4 |

旧回归精确命令：

```sh
go test -race ./internal/session ./internal/app -run '^(TestTurnOperationAcceptedReplayAndConflictSurviveRestart|TestTurnOperationPendingAndUncertainRemainFailClosedAfterRestart|TestTurnOperationScopeIsPerSessionAndCleanupRemovesOperations|TestFEAT132NativeRoutesKeepBearerAuthorityAndNoStore|TestFEAT144NativeThreadStatusRoutePreservesAuthorityAndSafeErrors|TestMultimodalTurnV2HTTPIdempotencyAndPendingRetry)$' -count=1 -v
```

首轮新增测试编译失败：两处fixture调用既有BindThread时漏了runtimeSessionID参数。已按真实五参数签名修正，后续上述测试全部通过；这是测试代码编译问题，没有运行产品或产生外部调用。没有隐藏失败、改门禁或降低断言。

元仓D0首次检查拒绝schema未定义的contract.status=PARTIAL；已改为整体NOT RUN并单独记录phase_1_status=PASS，明确其余契约尚未执行，复验通过。没有修改validator。

未执行：全量Contracts generate/test和Host make test含历史攻击归档、权限/进程故障等fixture，按用户长期安全条款跳过，使用独立leaf流程及已审查定向测试替代。因此不声明全仓测试全部通过。真实Desktop/Runtime/Provider、调度、迁移、审批交互、UI、电源和最终D4均未执行，属于后续阶段。

## 5. 与实现分离的结构化自审

代码及检查完成后，重新核对来源→注册→鉴权→ID校验→service→Store→显式投影→生成schema。未发现阶段一剩余阻断项：

- 查询不变更会话/operation、不利用Trace作授权；没有新执行入口。
- 任务索引和会话同一只读事务，operation保持session组合键及已有解码约束。
- 响应Host标识不替代历史generation；缺失、unknown与accepted没有被升级为可重投/业务成功。
- 源和生成物一致；旧协议/Store/Runtime未改；local候选与发布pin明确区分。
- 睡眠屏障、计划授权和Desktop scope仅落设计，不提前实施后续阶段。

这是Codex结构化自审，不冒充独立人工评审。当前完成的是阶段一基础，完整计划数据、调度触发、三目标执行、审批/恢复UI、唤醒均未完成。

## 6. 停点

第一阶段完成后停止，不自动进入第二阶段。下一阶段仍仅是已有方案中的Desktop本地计划/时间与存储基础，需先细化对应源与兼容reader，再实施；本轮未展开。

真实模型验收 **0/12**，图片 **0**，商家接口 **0**。本阶段使用进程内HTTP recorder和临时合成Store，没有访问或复制用户日常Host Home/数据库，没有强杀、权限破坏、攻击fixture或可执行文件替换。
