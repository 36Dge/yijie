# FEAT-175 第二次方案审计

2026-11-15。审计对象为第一版方案、当前工作树和固定 Runtime／依赖源码；未修改产品代码，未发起模型／搜索调用。第一版原文保存在 history/revision-1，原 source-evidence 和 plan-checks 保留。本审计由当前 Codex 执行，不冒充独立人工评审。

## 结论

第一版主方向可以保留，但**尚不具备直接进入大规模实施的条件**。发现 9 项需处理的问题：6 项 P1、3 项 P2。修订 2 已补设计规则与验收要求；运行可行性、公开前置和产品边界仍不能由文档检查代替。

## 发现

| ID | 优先级 | 第一版问题及实际影响 | 证据 | 修订 2 处理 |
| --- | --- | --- | --- | --- |
| R2-01 | P1 | “worker 自动使用产品会话”没有 Token owner、传递、续期、退出／换租户边界；可能被实现为把主 access/refresh token 下发 worker | Native AuthService 自己持有 access／refresh 并处理 401；Host 目前只有本机 capability，不存在已完成的网页委派通道 | 指定 Native 为主会话 owner，新增仅网页权限的委派契约候选；Host／worker 不能持主 refresh token；换身份撤销及执行前核验必测 |
| R2-02 | P1 | 将 MCP 取消、HTTP 断开和远端停止视作自动贯通，无法保证停止后没有新发送 | 当前 RmcpClient tools/call 使用 no_options＋await_response；外层 active_time_timeout 不等于 RequestHandle.cancel；rmcp 1.8.0 显式 cancel／自身 timeout 才发送取消通知的路径可见 | 新内置路径必须接 Host 原生 turn 生命周期撤销；客户端停止与远端确认分开，定义发送线性化点和 unknown；G2V 验明实际通知，不把未来回调当已有事实 |
| R2-03 | P1 | 只写“复用现有 REST adapter”，未指出 Backend 带共享 permit、串行锁和 cancelled 状态；原样云端共享会造成排队、跨调用状态或整实例撤销 | Backend 字段及 execute_inner 的 serial.lock；Codex 对 readOnlyHint=true 支持并行，即使服务器未显式 opt-in | 复用纯参数／归一化与 HTTP 策略；许可、取消、期限改为每次调用状态；全局仅有明确限额／并发准入，不能用一个用户的取消 revoke 全局 Backend |
| R2-04 | P1 | “相同 operation ID 不重复执行”未定义 ID 生命周期、原子发送状态、服务端重启、结果丢失和查询接口；不能据此承诺 exactly-once | 普通 custom MCP meta 没有通用 native call_id；现有 adapter 只有进程内状态，没有公开服务 durable 幂等闭环 | 限定同业务操作 ID 的 at-most-once dispatch，发送前落原子状态，发送后未知不再派发；增加只读状态／取消契约；未保存正文时明确 result_unavailable，不能自动再次 Fetch |
| R2-05 | P1 | 只移除专家 blanket 配置会留下真实角色冲突，第一版“不批量改角色”遗漏了需要定向处理的受管资源 | data-analyst-pro 的 ROLE.md 明确“不联网”；其他命中如分镜专家只是说明校验脚本不联网，二者不能等同 | 列出真实 agent 级离线约束，做版本化资源评审；默认继承与明确离线政策区分，不能靠专家名称／关键词自动判断，也不能擅自将所有脚本禁网说明改掉 |
| R2-06 | P1 | “无供应商 Key 的新设备双模型验收”遗漏主模型推理可用性；托管搜索 Key 不会自动让两个模型能运行 | ModelAvailable 对 Kimi 检查 KimiAPIKey，对 MiniMax 检查其配置；本方案没有新增模型推理托管服务 | 将“无需额外搜索 Key”与基础模型服务分开；公开产品身份及主模型服务均为前置，未完成时不能宣称完整安装即用，也不默默扩大成新的模型网关项目 |
| R2-07 | P2 | 路由评分“研究有 Pro”可把先选错再补对判为正确；重复率分母、额外 REST、每类分布和精确模型资格未明确 | 第一版 06 的条件与 feature.yaml 只有整体 95%／5%；没有真实模型新资格 | 定义首次有意义提议、参数与结果三类证据、每类报告及重复分母；把双模型 hosted／MCP 可行性前置，后续结果不补洗首次错误 |
| R2-08 | P2 | “复用同一 worker”缺少市场关闭时的 owner 生命周期、能力隔离、startup 版本和互不撤销规则 | 当前 StartMarketProvider gated by MarketEnabled；worker 入口只有 status 与 broker-control；gateway 的 EOF／shutdown 同时停止 broker 和 providers | 共享 owner 的 feature 集合与独立 capability／准入明确；关市场不关内置；云端 target／依赖资格另证，不能拿桌面 build 当云端制品 |
| R2-09 | P2 | 60／45／35 秒只是各层数字；没有说明凭据刷新、网络、排队、metadata 开销及取消竞争如何影响“完整预算” | 原生 read-only 可并行，旧 adapter 串行锁会排队；原输出预算也要容纳新应用元信息 | 定义各计时起点、准入与剩余预算判定，不能把父请求剩余不足变成缩短的 Pro；最终 MCP 封包测量包含新元信息，未知计费保留 |

## 关键代码定位

- R2-01：[Native AuthService 调用与续期](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/native_auth/runtime.rs:927)、[授权上下文换代](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/chat/authorization.rs:396)。
- R2-02：[Runtime tools/call](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/rmcp-client/src/rmcp_client.rs:599)、[外层计时](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/rmcp-client/src/rmcp_client.rs:181)、[rmcp RequestHandle](/Users/jack/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rmcp-1.8.0/src/service.rs:358)、[显式取消](/Users/jack/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rmcp-1.8.0/src/service.rs:467)。这是方案保证缺证据，不据此宣布整个 Runtime 取消机制有缺陷。
- R2-03：[Backend 状态](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:204)、[串行执行](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/kimi_web.rs:410)、[只读并行判定](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/tools/handlers/mcp.rs:76)。
- R2-04：[custom MCP metadata](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/codex-rs/core/src/mcp_tool_call.rs:1083)。call_id 的特殊插入只针对 Codex Apps，不可借用其 namespace 冒充业务调用。
- R2-05：[数据分析角色](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-skills/plugins/yijie-desktop-skills/experts/data-analyst-pro/skills/data-workbench/ROLE.md:7)、[0.1.2 角色](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-skills/plugins/yijie-desktop-skills/experts/data-analyst-pro/versions/0.1.2/data-workbench/ROLE.md:7)、[仅脚本说明的对照](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-skills/plugins/yijie-desktop-skills/experts/agentgrid-comic-storyboard-director/skills/comic-storyboard/ROLE.md:13)。本次未断言用户当前选中的就是这些版本。
- R2-06：[模型前置](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/chat_models.go:38)、[API 公开资格边界](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-api/internal/app/app.go:169)。
- R2-08：[Host owner 启动](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/market_runtime.go:43)、[worker 模式](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/main.rs:86)、[统一退出](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/gateway.rs:433)。

## 审计后的状态

修订 2 的规范补充见 [14 边界闭合](14-revision-2-boundaries.md)，并已同步主方案、需求、契约、用例、发布和 feature.yaml。所有修复均为文档层，不是产品实现结果。

仍须闭合三个前置条件：B01 公开产品身份／检索委派／主模型服务的发布基线；B02 明确离线专家资源的产品政策与版本评审；B03 固定 Runtime 的实际取消链及两模型路由可行性。未闭合前 G1／G2／G2V 不标通过，Runtime 零补丁只是目标，不能提前作为已证明结论。

文档严格检查、引用检查与源码摘要复核结果见 references/reaudit-checks.json。未做付费调用、产品测试、云部署、数据库迁移、App 重启、提交或推送；用户禁止的破坏性与攻击性验证均未执行。
