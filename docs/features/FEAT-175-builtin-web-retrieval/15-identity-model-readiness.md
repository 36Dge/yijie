# FEAT-175 B01：身份、检索委派与基础模型服务

2026-11-15，修订 3 设计。实现方式和验收已定义，代码／部署／真实资格仍 NOT RUN。用户已确认服务端托管搜索 Key、普通只读自动执行；下面的参数是本次推荐设计，不是已部署配置或费用授权。

## 1. 直接复用与最小新增

| 能力 | 复用入口 | 本次最小新增 |
| --- | --- | --- |
| 产品登录、refresh token、静默续期、退出 | Desktop NativeAuthRuntime／AuthService／OperationTransport | 正常身份下取得及撤销网页委派；不新增登录流程 |
| 主 access token 验证 | API authn.Verifier，固定 RS256／issuer／audience、10 分钟最大时长 | 不更改验证算法、audience 或绕过生产配置 |
| 用户、租户、角色、权限版本 | API identity／authorization／PostgreSQL | 源先行增加 web.retrieve 权限及服务资格；不能把 workspace.use 当收费工具授权 |
| Native→Host 权威通道 | Native-owned control pipe、hello、scope／process epoch、封闭 JSONL 与正常 EOF | 专用网页凭据安装／清除方法；承接秘密不进入既有市场业务正文 |
| Host→worker | 现有受管 owner、私有控制 transport、generation | 网页能力更新／撤销和每调用授权；不另建 Agent 调度器 |
| 公开 REST 执行 | Connectors 参数／结果纯逻辑与有界 HTTP | 服务端每 operation 独立执行上下文、准入与派发记录 |

新增部分属于产品权限和外部调用适配，Codex 没有替产品发行账户／管理供应商额度的职责。原生工具组织、审批、执行、事件和回灌不复制。

## 2. 凭据选择：API 签发的不透明短期委派

采用 API 自有的不透明随机 bearer，**不新增一套 JWT 签名密钥／登录系统**。主 access token 仍由原身份提供方签发、Native 持有、现有 API Verifier 验证。网页委派仅由 API 在已有用户／租户权限核验后发行。

候选参数：

| 项目 | 规则 |
| --- | --- |
| 随机材料 | 标准安全随机数 32 bytes；编码后加固定格式版本，不包含用户资料 |
| 服务 audience | 服务端记录固定 builtin-web-retrieval/1；该 token 不能调用其他 API |
| 权限 | search、search_pro、fetch、自己操作的 status／cancel；不是平台管理员凭据 |
| 有效期 | 最长 300 秒；Native 剩余 60 秒时触发正常续期，后台无活动会话时可不续 |
| 持久化 | 服务端只保存 token SHA-256、grant ID、主体／租户、授权 revision、期限和撤销状态；不保存 token 原文 |
| 客户端 | Native、Host、worker 必要内存；不写 App 配置／renderer／Runtime env／日志／bbolt。Runtime 仅持独立的本机 MCP capability |
| 续期 | Native 重新用有效主会话取得新 grant，原子安装新 generation；不是给 worker 一个 refresh token |
| 撤销 | API 新准入时检查当前用户、成员资格、权限 revision 和 grant 状态；claim 时复核已准入操作的 binding、当前权限和自身期限；退出／换租户先关闭本地准入，再尽力撤销云端 |

主会话在 Native 续期的原有 401 一次恢复机制可复用。网页 execute 的认证失败只有在 API 明确确认**本 HTTP 尝试未派发**时，才允许刷新委派后以同 operation ID 重送一次；不换 ID。网络中断、超时、未知、429／5xx 不自动重发业务 POST。供应商 401 必须映射为运营服务错误，不能透传成产品会话 401 诱导错误续期。

必须区分进程epoch、登录／租户binding epoch、服务端authorization_revision和credential_revision。正常刷新只增加credential_revision，不撤销正在研究的turn，也不取消已准入operation。旧grant在剩余不超过60秒时与新grant短暂并存并自然到期；过期只阻止新准入，已准入请求仍按自身期限和当前账户权限结束。

claim 不因正常 credential 到期而取消已接受工作，但必须拒绝已撤销 binding、已失去执行权限或超过操作自身 deadline 的派发；上述复核与 claim 状态变更使用同一服务端原子条件。权限 revision 变化须重新计算权限，不能把正常续期误判成退出。

退出／换租户使用binding级撤销，关闭该binding下全部未到期grant并取消尚未claim的操作；权限变更由当前authorization_revision检查处理。不能用普通token轮换模拟退出，也不能只撤销最新grant而遗漏重叠期旧grant。

退出后本机准入立即失效。若云端撤销因断网未得到确认，不宣称已即时全局撤销：残余凭据最多存活至其 300 秒期限，且仍受服务端当前权限与额度检查。已经派发的请求另按 B03 收尾，不承诺停止计费。

## 3. 接口与本机更新路径

以下为待进入 Contracts 的候选 v1 操作，不是现有接口：

| 接口 | 认证／输入 | 结果与约束 |
| --- | --- | --- |
| POST /v1/web-retrieval/delegations | Native 主产品 bearer、既有 X-Yijie-Tenant-ID、native binding reference | API 从可信主体／租户求权限，发行固定范围委派；不接受客户端扩大 scopes |
| POST /v1/web-retrieval/bindings/{id}/revoke | 当前主会话或该binding所属grant，仅能操作自己的binding | 幂等撤销binding内所有grant并标记未claim操作取消；正常续期不调用此接口 |
| POST /v1/web-retrieval/operations | 网页 grant；operation_id、tool 枚举、对应封闭参数 | 原子查重／准入，然后一次执行；返回标准化结果或明确状态 |
| GET /v1/web-retrieval/operations/{id} | 当前有效网页 grant，主体／租户必须拥有记录 | 只读状态，不重新搜索；不消耗执行额度 |
| POST /v1/web-retrieval/operations/{id}/cancel | 同上 | 幂等取消请求；区分未派发取消与派发后尽力停止，不额外收费 |

额度耗尽不能阻止正常 status／cancel。执行权限撤销时，服务端同步阻止新 dispatch，关联操作的撤销不依赖已失效 worker token 再发一次成功请求。Native 主会话可执行自己的撤销管理；主凭据仍不离开 Native。

Native 在应用正常身份／租户绑定后、用户发起任务前异步准备 grant。API 网络请求不放在 5 秒的 Native control exchange 内；拿到 grant 后才发送专用 web_capability_install。Host 校验原 hello 的身份、native epoch、scope 和 grant revision，内存替换后返回不含秘密的 ACK。专用方法在 capability 协商后才可用，旧 Host 不接受时报告版本不支持，不退回 renderer HTTP 授权。

Host 再经 worker 私有通道更新有界网页能力；通道解码、Debug、错误和诊断均不回显秘密。普通 turn 的等待不会改变 grant 的账号／租户。换身份时清除旧 capability 和 I/O 准入，再绑定新身份，不能把缓存的 grant 静默复用于新账户。所有更新／清除为 typed、幂等操作，不能重放供应商请求。

秘密字段的生成／消费必须有显式脱敏规则：不能让新 generated DTO 的默认 Debug／fmt／错误快照输出 bearer。复用现有 SecretValue／受管 secret wrapper；需要生成支持时从源标记和 generator 增补，不手改生成文件。用合法合成委派检查普通日志／错误／状态输出，不使用真实 Key 或攻击性反射 fixture。

当前 loadMarketProfile 明确只准入 local＋demo_fast。复用的是 Native-owned pipe 的 transport／owner，不是沿用固定本地身份作为公网授权。公开 App 的 carrier 必须依据真实产品 scope 装配独立 builtin_web 方法；仅一个 stdin reader 分派已协商的方法，不增加第二个读者。旧 market router 和本地专用 gate 原样保留，不能伪造 MarketEnabled 或把发布 App 冒充 local demo。普通聊天／专家的公开 carrier 资格纳入 DEP-CARRIER。

## 4. 原子派发和保留窗口

API 复用现有 PostgreSQL／迁移／事务和审计模块，增加最小 delegation 与 operation 记录；不新增队列系统、模型规划器或全文缓存。

- operation ID 使用现有 UUID 库的 UUIDv7，在 Host 接受一次真实 MCP invocation 时分配；同 invocation 的协议重投复用 ID，不按 query 合并不同调用。
- 请求摘要绑定契约版本、工具名和校验后的参数（补齐该版本默认值、稳定对象键序），不改写查询文本、不按语义合并。已有 ID 不接受变更后的工具／参数／契约解释。
- 新 operation 首次准入要求 UUIDv7 时间在服务端过去 5 分钟至未来 60 秒内；时间仅用于过期／重放窗口，不授予权限。已有记录先按真实主体查重，不能被时间条件误当新请求。
- operation 元信息保留 30 天；超过窗口的旧 ID 因时间过期被拒绝，不能删记录后又被当成新付费调用。正常新用户请求新建 ID；离线用户提交内容恢复后，实际 MCP 调用发生时才分配新 ID。
- grant 过期／撤销元记录可保留 24 小时后清理；审计沿现有保留政策，不因删除 grant 记录删除审计。期限为候选产品参数，不代表法规要求。

派发状态使用 ready → dispatch_committed → completed／unknown，以及 ready → cancelled／rejected。API 记录 ready 和配额预占，向 Connectors 发送一次内部执行请求。Connectors 在 HTTP 前通过内部 claim 接口取得原子 dispatch 许可；同 ID 只有一次 claim 成功。claim 后进程结束或结果未知也不能再次 claim，从而保证服务最多一次派发，而非供应商 exactly-once。

API↔Connectors 使用部署方管理的服务身份和相互 TLS 验证；明确允许的服务证书身份，不能信任自报 service_name，也不能用终端用户 grant 调内部 claim／finish。复用服务 TLS 库和秘密注入，不引入新 service mesh。候选内部操作为 execute、claim、finish／status；claim 返回绑定 op／参数摘要／executor instance 的 receipt，finish 必须匹配原许可。正式路径、错误及 receipt 由同一 Contracts 源冻结。

**dispatch_committed 是本服务的保守派发授权点，不等于字节已经到达 Moonshot。** cancel 与 claim 在同一记录上竞争：cancel 先成功则保证零供应商发送；claim 已成功则返回可能已发送，允许本地取消进一步阻止实际发送，但不能保证免计费。API→Connectors 的自动 POST 重试关闭；即使内部重复投递，也必须被 claim 拦住。

重开／重启不扫描 ready／unknown 自动补发。迟到的可信执行回执只能更新同 operation 的真实结果，不能将完成改成未执行。没有保存正文时 status 只能返回事实及 result_unavailable；不会自动 Fetch 或伪造空结果。元记录不保存完整 query、URL、网页正文或秘密。

status／cancel 供本机适配与明确恢复／状态展示使用，不新增第四个供模型轮询的业务 MCP 工具。迟到费用回执不把已结束的 native MCP Item 从 failed/cancelled 改成 completed；需要继续给模型材料仍须经过真实原生工具结果，不能由 Host 补造消息。

配额按工具调用类别预占，供应商调用和模型 Token 费用分开。未派发或有明确不计费证据时释放；发送未知维持保守占用，不记免费。每日工具上限、主体并发上限和运营账户总上限均须为有限配置；缺配置不开放公网执行，不能采用无限默认值。无需新增用户购买／计费界面。

## 5. 依赖及完成交接

所有 Owner 默认段成威，实际交接结果必须有完整来源和证据，不虚构其他批准人。

| 依赖 | 提供方／交接物 | 消费点 | 完成判据 |
| --- | --- | --- | --- |
| DEP-AUTH | Desktop Native Auth＋API 身份／租户服务；生产 origin／issuer／JWKS／角色配置 | delegation mint、Native scope | 两个正常测试账户登录／续期／退出／换租户可用；没有 local direct-entry 对外使用 |
| DEP-WEB-AUTH | Contracts、API、Native、Host、worker 的上述委派及控制投影 | 每次内置调用 | TTL、身份换代、精确权限和无秘密泄漏的正常路径通过；没有搜索 OAuth |
| DEP-CARRIER | 已有公开 App／Chat／专家功能提供真实产品 scope 的 Native-owned carrier，或在其来源边界补齐 | Host private dispatcher、会话绑定 | 无固定 demo 身份；单 owner reader；普通／专家的实际提交可用；其他本地专用功能没有被一并开放 |
| DEP-MODEL | 现有模型接入功能 Owner 提供两个模型的受支持产品 profile、凭据 resolver 与真实 Responses 资格 | Codex ModelProvider、ModelAvailable | 目标账户在正常 App 中能分别调用 Kimi K3.1 Pro／MiniMax M3，恢复和正常停止可用；不依赖开发者私有目录或秘密 |
| DEP-CLOUD | API／Connectors 服务身份、TLS、数据库、运营 Kimi Key、有限额度、server target 构建 | 执行／claim／结果 | 已授权的 Basic／Pro／Fetch真实资格及正常取消；Key 从未下发客户机 |
| DEP-DIST | 正常分发渠道、签名制品及获准资源集合 | 新设备 App | 普通用户安装后无需搜索 Key／连接器动作；local-use-only 资产不自动获得公开分发资格 |

DEP-MODEL 是明确的基础产品依赖，**不由 FEAT-175 默默实现一座新推理网关**。推荐消费已获准的产品模型服务；若基础产品选择 BYOK，应明确这是模型服务既有步骤，而不能宣传“完全免模型配置”。搜索功能不再要求另一份 Key。若要求整款 App 也完全免模型配置，DEP-MODEL 必须提供相应托管 profile 后，完整开箱验收才能成立。

Codex 已有 model_providers.<id>.auth.command／refresh_interval_ms，可供该依赖复用；与 env_key／requires_openai_auth 不能混用。但当前 external_bearer helper 有 kill_on_drop(true) 路径，**FEAT-175 不新增或启用该 helper**，也不做挂死／强杀验证。未来模型接入若采用它，须在自己的范围内证明正常退出与用户安全约束；不能因为 API 字段存在就直接激活，也不能在 Host 另造轮询认证循环。

## 6. B01 验收标准

| 编号 | 可执行验收 | 必须保留的证据 |
| --- | --- | --- |
| B1-A1 | 正常产品会话发行 web-only grant；本机工具发现不触发 Moonshot 请求 | 主体／租户及权限版本摘要，供应商计数为 0 |
| B1-A2 | 正常经过 300 秒期限／提前 60 秒续期；已接受操作不被普通轮换中断；退出／换租户撤销该 binding 的全部重叠 grant | 真实期限、credential／binding revision、更新 ACK 与发送次数；无 Token 原文；grant 到期与权限撤销分别判定 |
| B1-A3 | 默认只读工具无需安装／授权／勾选；API权限／额度缺失有明确状态 | 新用户 UI 与调用链证据，不借假 installed／authorized 记录 |
| B1-A4 | 同 operation 正常重复投递、并发 claim、状态查询只产生最多一次派发 | API事务结果、Connectors发送计数、合法输入摘要 |
| B1-A5 | 正常取消在 claim 前／后分别执行；既有 dispatch 记录经正常服务重开不重发 | cancelled／may_have_dispatched／unknown 事实分开；不强杀制造窗口 |
| B1-A6 | 没有原正文时查询原操作显示 result_unavailable；不会再搜索 | 查询与供应商计数，Native 已保存结果仍可重开 |
| B1-A7 | 新设备分别完成两个主模型的普通回复和三工具闭环 | 受支持 profile／build／cloud 版本及真实资格；不以直接 REST 替代 App |
| B1-A8 | 合法委派的序列化、正常错误、状态／Debug／观测路径 | 无 bearer／refresh／上游Key原文；响应仅有安全ID／期限，实际秘密只在受管carrier与请求header |

身份、期限和事务可先用普通合法本机 fixtures／虚拟时间验证；真实供应商资格、公开环境和额度仍须后续明确授权。方案定义完成不等于 B01 运行验收通过。
