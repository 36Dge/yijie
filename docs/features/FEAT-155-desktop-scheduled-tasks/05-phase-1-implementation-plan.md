# FEAT-155 第一阶段实施方案：契约与只读恢复基础

> 2026-09-18 · 第一阶段实施已授权。用户最新要求：“下一步只修订上述方案定义，再实施第一阶段的契约与两类只读查询。”
> 原方案与审计已完成；四处定义及阶段一实施结果见[06](06-phase-1-implementation-report.md)，已停止，不自动推进阶段二。

## 1. 分阶段方式与总目标

已接受的ADR-0020、完整需求目标、16小时不阻断、系统通知延期和12次文本预算保持有效。本次只改变推进方式：按阶段实现、检查和报告，不能凭整体授权自动连续铺开后续阶段。用户指定的分阶段方式优先于demo_fast原先默认连续实施；不引入production_hardened的治理切片或新增G门禁。

| 阶段 | 唯一结果 | 边界 |
|---|---|---|
| **第一阶段：契约与只读恢复基础** | 后续调度能以稳定身份读取既有Host映射/投递事实，有唯一源契约及安全失败语义 | 本文详细规划；不触发模型、不写用户计划数据 |
| 第二阶段：本地计划与时间/存储基础 | Desktop能正确保存计划、算下一次时间、管理occurrence并验证兼容reader | 再细化方案；不提前迁移日常用户DB |
| 第三阶段：受管执行闭环 | 调度通过同一native授权/预约/outbox发起原生执行，包含三目标、草案创建、恢复与正常退出 | 自动触发前完成睡眠事件监听/恢复屏障/不补跑和计划有限授权；验收按12次总预算控制调用 |
| 第四阶段：页面集成与最终验收 | 完成PDF页面/交互、应用内通知、macOS防空闲睡眠开关及真实完整验收 | 睡眠恢复屏障已在第三阶段生效；系统通知继续延期；最终统一验证全部十项Must |

阶段划分不删减AC-001至AC-010，也不表示某阶段通过即可宣称FEAT-155完成。UI不以假数据/模拟成功替代最终真实服务验收。

## 2. 为什么第一阶段先做这件事

现有Host已经保留task/session/thread映射及turn operation的pending/accepted/uncertain事实，但没有面向Desktop的只读恢复查询。调度未来遇到回执丢失或重开时，如果只能猜测状态，就可能重复创建会话、重复提交turn。先把这一必要边界接好，可以在不启动调度、不调用模型、不迁移用户库的情况下验证跨仓接入正确性。

第一阶段不是构建新调度引擎，也不建立通用任务平台。只补FEAT-155已经确认需要的两类查询与最小数据语义，并为后续对话草案提供固定schema来源。

## 3. 第一阶段具体内容

### 3.1 Source-first：最小契约与数据语义

在yijie-contracts建立独立FEAT-155契约族，不改现有native聊天、FEAT-152权限和FEAT-144 MCP协议的解释。

- 明确plan、run、conversation/task、Host session、Runtime thread/turn、operation ID的职责和关联，禁止混用plan_id与task_id。
- 定义“按task_id查询会话映射”和“按session_id + operation_id查询投递结果”的请求/响应、可访问scope、错误及缺失含义。
- 查询只返回必要标识、状态、可用性和Host实例来源；不返回prompt、消息、路径、凭据或bbolt内部记录。
- accepted只能返回已持久确认的原turn；pending/uncertain保持原值；映射不存在、字段缺失、native idle/notLoaded均不能被解释为“以前一定没有执行”。
- 冻结有限计划草案schema：需澄清/候选计划、名称、内容、频率/时区与目标意图；身份、原生目录、授权和保存结果由native决定，不由模型填写。此阶段只定义与校验schema，不透传执行、不调用模型。
- 仅在精确local + demo_fast注册查询；Host沿现有owner-only loopback bearer校验凭据、规范ID和session-operation关联。Trace中的tenant/user是可变追踪字段，不作为资源授权。查询不接收tenant/user自授权参数，不承诺Host多租户隔离。阶段三的Desktop native消费者先校验当前authority→本地计划/会话scope→受管Host关联，renderer不得直接持有bearer。不新增公网服务或另一套鉴权。
- `responding_host_instance_id`仅表示本次响应的Host实例；未配置时省略，消费者视为unknown。它不是原投递所属的Runtime generation，不能证明旧执行终止或释放预约。阶段三由native生命周期账及正常停止结果确认旧generation；阶段一不增加历史实例持久字段或迁移。

后续阶段的计划CRUD、平台电源接口和新workspace来源，在各自真正实施前继续source-first；第一阶段不预铺尚未需要的完整管理平台API。

### 3.2 生成与消费方式

- 使用独立源文件与leaf generator，生成实际需要的Go类型、schema投影及消费清单；Desktop所需类型可以形成待消费产物，但不提前接入页面/native调用。
- 不修改已被历史consumer按digest锁定的通用generator/package文件来制造无关来源变化；不手改生成文件、不复制影子DTO。
- 在本地候选中记录契约base commit、源与生成物digest、generator身份；同步Host时复核同源。未经提交/推送授权不制造Git pin/tag，不将dirty候选称为发布版本。
- 普通字段/枚举的无效输入仅作为安全conformance数据；不生成恶意归档、攻击载荷或权限故障fixture。

建议落点（最终文件命名随现有目录约定微调，不增加职责）：

| 仓库 | 预计新增/调整 |
|---|---|
| yijie-contracts | 独立scheduled-tasks支持查询OpenAPI、计划草案JSON Schema、leaf generate/check、同源生成物及定向conformance |
| yijie-agent-host | 同源契约快照/生成类型、只读service/store适配、两类GET handler和必要注册、定向普通单元测试 |
| yijie | 本方案、实际实施记录、契约影响/来源/验证结果 |
| yijie-desktop | 第一阶段仅只读核对消费者需要；不修改页面、native运行逻辑、DB或lockfile |

### 3.3 Host只读实现

- 会话查询复用现有task→session索引；原thread/session创建逻辑不修改，不补发thread/start。
- 投递查询复用现有TurnOperation记录；不重新调用turn/start，不修改pending/uncertain，不执行resume来猜测过去是否成功。
- Store输出通过显式领域映射到生成响应，避免直接暴露私有bbolt结构。
- 沿既有鉴权注册端点，检查ID格式和可访问关联；只读查询不因结果不明触发任何执行副作用。
- 不新增计划表、scheduler循环、后台重试、审批代理或业务成功分类器。

## 4. 检查方法与阶段完成标准

第一阶段只运行安全、定向的契约/Host检查，不运行带攻击fixture或进程故障注入的历史全量测试。实际执行结果另记实施报告，不将本检查计划写成已通过。

| 检查点 | 可判定标准 |
|---|---|
| 唯一权威源 | 所有新增wire类型可追溯到Contracts源；重新生成无漂移，Host消费digest一致 |
| 正常查询 | 已有映射与accepted/pending/uncertain操作按事实返回，ID关联正确，缺失有明确错误 |
| 只读性 | 相同查询可重复且状态/持久记录不变；测试运行时adapter可记录调用数，确认thread/start、turn/start、resume、审批决定均未被调用 |
| 输入与权限 | 普通无效ID、未知资源、未认证/不可访问请求按既有安全边界拒绝，不返回秘密或原始内部对象 |
| 草案schema | 普通完整/缺参候选、字段边界和未知字段处理符合定义；没有模型结果被伪报为保存成功 |
| 兼容保护 | 既有协议源/生成物/Runtime锁保持不变；相关focused回归通过，新增查询不改变旧接口 |
| 工作区与记录 | 逐仓diff/status与实际命令/结果完整；未执行项说明原因，不标D4或业务Must PASS |

定向恢复检查包含临时Store正常关闭/重开、正常清理后缺失、相同operation ID在不同session下的关联、responding instance缺省/变化仍保持pending/uncertain；全部通过正常接口准备数据，不强杀或注入故障。

第三阶段自动执行前必须落实计划有限授权：保存允许paused；开启前展示并确认本次有限验证的次数与到期时间，由native绑定plan及revision、grant ID、有效期和余额，出站前原子占用，unknown不返还；变更内容/时间/目标后需重新确认适用授权。未授权、额度耗尽或到期时停止新投递并显示原因。首期复用现有native授权边界，只覆盖有限合成/公开只读验证，不新增计费平台。12次是本FEAT全部真实文本验收请求总账；计划run额度不能代替该总账，草案调用也计入总账。具体存储/IPC在阶段二、三source-first细化，阶段一不实施。

验收材料只包含源契约、生成差异、Host实现、正常合成数据的测试结果和受影响文件清单。合成数据仅在临时测试存储内通过正常写入接口准备，不访问或复制用户日常Host Home/数据库，不启动真实Runtime或Provider。

预计第一阶段约3–5小时，作为工作安排参考，不设16小时禁止条件。若发现原只读索引不足，先说明具体缺口；不能把阶段一扩为计划引擎、重试平台或整个聊天重构。

## 5. 阶段结束后的交付与停点

第一阶段实际完成后，报告：改了哪些契约/Host文件、读取什么已有事实、哪些检查通过、哪些风险仍在；然后给出第二阶段的具体实施方案。本阶段不自动进入第二阶段，也不提前启动UI、计划调度或数据库迁移。

当前已授权实施阶段一；实际完成与验证以追加报告为准。Runtime/服务和模型不在本阶段启动，模型调用0/12，图片及商家接口0；不将整体设计批准视为功能验收通过。
