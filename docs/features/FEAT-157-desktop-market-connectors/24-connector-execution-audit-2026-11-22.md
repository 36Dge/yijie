# 连接器执行链审计 · 2026-11-22

**结论。** Sorftime 所走的市场连接器链路已经支持本轮授权续期。续期使长任务可以继续登记新调用，每笔调用仍有自己的截止时间和一次性发送许可。当前代码继续要求非空选集使用「请求批准」。要支持另外两种模式，最先要解决的是如何把 **Codex 对某笔调用的真实决定** 交给连接器执行端。调整菜单或延长超时都不能完成这项接入。[续期契约](../../../../yijie-contracts/docs/market-broker-control-v1.md#L7) · [后续实施方案](25-connector-approval-modes-plan.md)

## 本次审计的版本

重新读取了下表中的工作树、暂停以来的提交和实际构建清单。审计开始时下表各仓工作树均干净。证据来自本机 local / demo_fast 链路。本文仅记录当前实现和验证，`contract-impact = none`。

| 仓库 | 审计 HEAD | 本次核对的边界 |
| --- | --- | --- |
| yijie | `5d4644900c55` | 已接受的连接器架构、三种权限模式和高风险业务审批 |
| yijie-desktop | `98fda7f2888a` | 草稿选集、Native 入队与派发、权限续期、审批卡及历史 |
| yijie-contracts | `f2de6f9282dc` | Broker 0.9.0、market-host v1 家族 0.6.1、v2 家族 0.8.1、provider 0.6.0 |
| yijie-agent-host | `617d58120266` | 冻结意图、线程配置、私有控制、原生审批与结果关联 |
| yijie-connectors | `51c7753a9932` | 服务注册、工具发现、Worker、Gateway、调用额度和供应商发送 |
| yijie-codex | `c5786ce51ac4` | 固定 Runtime 0.144.6、原生 MCP 审批、Guardian、0031 轮次停止 |
| yijie-api | `592cb5fd6811` | 业务审批边界。本次市场续期走 Native 和 Host 的私有管道 |

日常最近一次构建记录为 `verified`。本次集成用例使用同一 Runtime 和产品 Worker，运行前重新核对了实际文件摘要。Runtime SHA-256 为 `36c27d7640aeeec74d4bee5670cfa8c7a53d68a142774e1a1e2415c4c64d9fe0`，Worker 为 `3108ad1ca32fde8f441bc13e59455d2c16dd408b8a2b49309d527a696823491a`。Runtime 清单的源码提交 `5fb7f7f3fd44` 与当前 Codex HEAD 的 Git tree 相同，清单含补丁 0031。这是本地候选制品。[Desktop 固定清单](../../../../yijie-desktop/contracts/runtime-skill-marketplace.candidate.json) · [Worker 契约版本](../../../../yijie-connectors/api/market-broker-control.candidate.json)

## 从选中 Sorftime 到实际执行

| 阶段 | 当前行为与核对结果 |
| --- | --- |
| 1. 安装、启用、发现 | Desktop Native 保存安装引用、revision、generation 和启用意图。Worker 在凭据边界内建立连接、发现工具并核验 schema。Sorftime 使用通用远程 MCP 链路。安装成功、持有凭据、服务可选、选中工具、同意一次调用是不同的状态。原 FEAT-144 Sorftime 专用执行路径已退役。[安装记录](../../../../yijie-desktop/src-tauri/src/chat/connectors/store.rs#L216) · [发现与注册](../../../../yijie-connectors/worker/src/providers.rs#L828) · [统一 Sorftime 入口](20-cross-border-commerce-extension.md) |
| 2. 选择、发送与冻结 | 聊天输入框按草稿保存服务与安装引用。发送前检查已有待审批操作、非空选集的权限模式、所选安装是否就绪。Native 按当前身份核验提交，冻结内容、模型意图、选集及权限，把本地消息和待派发记录放进事务。相同操作重读原回执。新任务、已有会话、专家提交及空选集有各自分支。[前端选择与检查](../../../../yijie-desktop/src/pages/chat/ChatPage.vue#L728) · [Native 入队](../../../../yijie-desktop/src-tauri/src/chat/connectors/selection.rs#L303) · [分发前复核](../../../../yijie-desktop/src-tauri/src/chat/connectors/dispatch.rs#L238) |
| 3. 组装本轮工具 | Native 经私有控制通道注册提交授权。Host 用已冻结的意图准备同一个 Runtime 线程，Worker 在 `prepare` 中把真实已启用的安装、作用域与选集绑定。新轮获得真实线程／轮次后执行 `bind_turn`。Host 配置受管 `yijie_market` 代理，Gateway 按租约返回工具。空选集不会开放市场工具。目录 revision 11 有 61 项，选集契约上限 58，每项服务及整个选集的通用工具上限分别为 512。[Host 注册](../../../../yijie-agent-host/internal/session/market_authority.go#L148) · [线程装配](../../../../yijie-agent-host/internal/codex/market_turns.go#L56) · [Worker 准备](../../../../yijie-connectors/worker/src/broker.rs#L418) · [目录](../../../../yijie-connectors/catalog/market-catalog.v1.json) · [选集](../../../../yijie-desktop/contracts/market-selection-v2.schema.json) |
| 4. 登记真实调用 | 模型选择工具后，Gateway 从真实 MCP 请求读取 thread、turn 和租约，Worker 校验服务、安装代际、具体工具与实际参数，生成新的 `callRef` 和参数摘要。通用工具名按服务与上游工具名生成，schema 单独计算摘要。当前通用 `review` 保守显示为写入风险，明确破坏性且缺专用策略的调用会被拒绝。自然语言里说“只查排名”无法证明供应商工具的效果。[Gateway 入口](../../../../yijie-connectors/worker/src/gateway.rs#L185) · [调用登记](../../../../yijie-connectors/worker/src/broker.rs#L939) · [通用工具定义与风险](../../../../yijie-connectors/worker/src/generic.rs#L91) |
| 5. 展示与确认 | Gateway 发原生 MCP 空表单，元数据只给出调用引用和类型。Host 用真实线程、轮次和 `callRef` 从 Worker 查回审核内容；专家生图路由与单轮次数也在这里校验。Desktop 展示工具及可审阅参数。点击决定后，Host 先经 owner 私有控制通道发送 `decide_call`，成功后答复原生表单。会话、代际、授权版本、参数与截止时间均参与对应环节的校验。[原生回调](../../../../yijie-agent-host/internal/codex/market_approvals.go#L73) · [决定提交](../../../../yijie-agent-host/internal/codex/market_approvals.go#L193) · [桌面审批卡](../../../../yijie-desktop/src/components/chat/MarketChatActivity.vue#L73) |
| 6. 执行与回传 | Broker 在锁内同时检查原生接受、同笔调用的 owner 决定、活跃租约和取消状态，随后消费一次执行许可。连接器发送层再次核对具体工具及参数，防止 SDK 重连或重试重复发送。Gateway 清洗供应商元数据后写入自己的小型回执，Host 将其与原提交、实际线程／轮次和 Item 对照。Desktop 分别记录决定是否送达、许可是否消费及真实业务结果。历史读、迟到结果、刷新或冷启动都不能充当新授权。[执行许可](../../../../yijie-connectors/worker/src/broker.rs#L1107) · [发送许可](../../../../yijie-connectors/worker/src/daily.rs#L59) · [回执清洗](../../../../yijie-connectors/worker/src/gateway.rs#L380) · [结果关联](../../../../yijie-agent-host/internal/session/market_correlation.go#L12) · [本地决定事实](../../../../yijie-desktop/src-tauri/migrations/chat/0047_market_decision_facts.sql) |

## Sorftime 修复改变了哪些时间边界

| 对象 | 当前规则 | 对新增模式的约束 |
| --- | --- | --- |
| 本轮市场租约 | Desktop 续同一上下文时，Native 复核身份、权限版本、`task.read`、`task.create`、`connector.use`。经现有私有管道发 `renew_market_scope`，Host 转给已拥有的 Worker。只更新同一 owner、tenant、Native epoch 和授权 revision 下、供应商仍可用的 prepared/bound 租约。每次时长取可信证明剩余时间、原请求 TTL、300 秒三者最小值。同一证明幂等，旧序号拒绝。 | 身份、权限版本或安装发生实质变化时走撤权。短证明能缩短有效期，已到期或已撤销的租约不能复活。心跳不启动新 Worker。 |
| 每次调用 | 登记时冻结独立截止，普通审批至多 60 秒并受租约剩余时间限制；需保留正文读取预算的 Kimi 网页工具另有决定／执行双截止。续长轮次不延长已登记的调用，缩短授权会取消越界的等待与既有执行许可。 | 人工、Guardian、会话和长期记忆命中均须使用本次新调用的 `callRef` 和原截止。 |
| 轮次停止 | Gateway 仅在确认尚未发送的租约过期或撤权时产生 `yijie.market.turnStop`。0031 只接受受管市场 server 的指定错误标记，撤下本轮直接及延迟发现的市场工具，拦住 Code Mode 已缓存的后续调用。 | 单次拒绝、单次审批到期、已发送而结果未知，必须保持各自语义。其他计算和新轮次仍有独立生命周期。 |

[Native 续期和缩短回执处理](../../../../yijie-desktop/src-tauri/src/chat/authorization.rs#L156) · [Host 续期](../../../../yijie-agent-host/internal/session/market_provider.go#L19) · [Worker 续期](../../../../yijie-connectors/worker/src/broker.rs#L522) · [Gateway 终止分类](../../../../yijie-connectors/worker/src/gateway.rs#L58) · [0031 原生补丁](../../../../yijie-codex/.yijie/patches/chat-models/0031-market-turn-admission.patch)

## 对接审批前必须处理的发现

1. **五个检查点仍限制为 ask。** 前端发送、Native 入队、Native 派发、Host 注册以及 Runtime 准备均有相应判断，其中最后两项都在 Host 仓。即使仅放开前端，后续层仍会拒绝。兼容分支还需处理已接收回执、专家提交和冻结模式与当前有效模式的核对。[前端](../../../../yijie-desktop/src/pages/chat/ChatPage.vue#L754) · [Native](../../../../yijie-desktop/src-tauri/src/chat/connectors/selection.rs#L365) · [派发](../../../../yijie-desktop/src-tauri/src/chat/connectors/dispatch.rs#L238) · [Host 注册](../../../../yijie-agent-host/internal/session/market_authority.go#L152) · [运行准备](../../../../yijie-agent-host/internal/codex/market_turns.go#L72)
2. **自动结果与人工回调的时序不同。** 当前 Gateway 收到原生 `accept` 就尝试消费。此时如果 owner 尚未将该笔调用标为 Approved，Broker 会取消待处理调用。在现有人工流程中 owner 决定先到；原生自动审核和完全访问可能直接返回，连人工回调都不会出现。新流程须可靠收齐这两份事实。Gateway 只看表单的 `action`，Host 人工回复的 `_meta` 固定为空。[Gateway 等待逻辑](../../../../yijie-connectors/worker/src/gateway.rs#L248) · [Broker 消费条件](../../../../yijie-connectors/worker/src/broker.rs#L1107) · [Host 回复](../../../../yijie-agent-host/internal/codex/market_approvals.go#L162)
3. **下拉选项与权限持久化来自不同的原生路径。** Desktop 当前「允许类似命令」绑定 shell 的 argv 前缀。市场卡只有允许一次、拒绝、取消。Codex 的 MCP 有原生 `session / always` 选项、会话记忆与配置持久化；这些效果目前由调用前审批应用。市场代理的 server 级 `approve` 抑制了重复的调用前提示；Worker 自己发出的确认表单不会仅凭返回 `persist` 就写入上述记忆。Host 对原生配置文件另有限定的可写范围。直接套用共享 `yijie_market + 工具名` 也无法区分账号与安装。[通用卡](../../../../yijie-desktop/src/components/chat/ChatApprovalPrompt.vue#L82) · [代理配置](../../../../yijie-agent-host/internal/codex/market_turns.go#L112) · [原生选项与键](../../../../yijie-codex/codex-rs/core/src/mcp_tool_call.rs#L1397) · [原生保存](../../../../yijie-codex/codex-rs/core/src/mcp_tool_call.rs#L1952) · [Host 配置边界](../../../../yijie-agent-host/internal/codex/native_config_layers.go#L39)
4. **业务限制目前有一部分只在人工回调执行。** 专家生图要核对真实方法、所选路由以及单轮次数。新增无弹窗流程时，所有决定来源都要经过同一已有校验。通用工具描述还写着“每次调用必须单独批准”，需要与实际可用模式一并调整。[生图路由](../../../../yijie-agent-host/internal/codex/market_approvals.go#L122) · [通用工具描述](../../../../yijie-connectors/worker/src/generic.rs#L107)
5. **多选上限在菜单中缺少即时反馈。** 满 58 项后，父页面直接忽略第 59 次选择，而菜单按钮的可用判断只检查服务可选性。该条件需要已安装足够多的服务，与这次单选 Sorftime 的红字无关。这是独立的静态交互发现。[页面上限](../../../../yijie-desktop/src/pages/chat/ChatPage.vue#L734) · [菜单判断](../../../../yijie-desktop/src/components/chat/ChatConnectorControl.vue#L64)

## 固定 Runtime 的三个原生对照

另外对原生**调用前审批**做了独立实测。使用相同的 0.144.6 Runtime、动态注入的 `yijie_market` 服务、一个只会计数并返回 42 的本地 MCP 和回环模型响应。测试界面仅能选择原生请求实际提供的范围。每组在同一会话调用两次，再正常退出 Runtime，沿用同一临时 Home 开新会话调用第三次。这里直接观测 Codex，本组不经过产品 Worker。[可复跑的独立用例](evidence/2026-11-22-native-approval/market_scope_probe_test.go)

| 选择 | 三次调用分别新增的弹窗 | 重启前原生用户配置中的该工具规则 | 观察 |
| --- | --- | --- | --- |
| Ask，选择本会话允许 | 1、0、1 | 无 | 原生提供 session、always 两项。会话记忆生效，新会话重新询问 |
| Ask，选择始终允许 | 1、0、1 | 无 | 原生提供相同选项。当前动态挂载方式实际只覆盖了本会话 |
| Full | 0、0、0 | 无 | 三次本地调用均完成，运行时没有向界面请求决定 |

两组 Ask 的第二次调用都无需点击，三个分组各实际执行三次本地查询。这个结果支持直接复用原生会话记忆，也定位了长期授权的配置归属问题。固定源码在自定义 server 缺少可写配置归属、持久化出错时会保留会话记忆。生产 Gateway 的身份校验、owner 决定和一次性发送许可仍需单独接入。Guardian 的原生映射与拒绝承接已核对；产品连接器的完整 auto 放行属于新能力验收。[原生持久化与失败处理](../../../../yijie-codex/codex-rs/core/src/mcp_tool_call.rs#L1978) · [原生配置归属判断](../../../../yijie-codex/codex-rs/core/src/mcp_tool_call.rs#L2087)

从 `yijie-agent-host` 根目录可重跑这三个对照。Go overlay 只添加测试文件，运行时从既有清单读取；后续版本运行产生的是对应版本的新证据。

```sh
python3 - <<'PY'
import json, os, subprocess, tempfile
from pathlib import Path

host = Path.cwd()
root = host.parent
pin = json.loads((host / "api/runtime-skill-marketplace.candidate.json").read_text())
runtime = root / "yijie-codex" / pin["runtime_relative_path"]
case = root / "yijie/docs/features/FEAT-157-desktop-market-connectors/evidence/2026-11-22-native-approval/market_scope_probe_test.go"
env = dict(os.environ, GOPROXY="off", YIJIE_CODEX_INTEGRATION_BINARY=str(runtime / "codex"),
           YIJIE_CODEX_INTEGRATION_MANIFEST=str(runtime / "runtime-manifest.json"))
with tempfile.TemporaryDirectory() as work:
    overlay = Path(work) / "overlay.json"
    name = host / "internal/codex/audit_native_market_scope_choices_test.go"
    overlay.write_text(json.dumps({"Replace": {str(name): str(case)}}))
    subprocess.run(["go", "test", "-count=1", "-v", "-overlay", str(overlay),
                    "-run", "^TestAuditNativeMarketScopeChoices$", "./internal/codex"], env=env, check=True)
PY
```

## 本次复核证据

下表记录本轮实际运行的定向用例。原生集成使用隔离的临时 Home、真实固定 Runtime 和产品 Worker，模型响应来自本机回环服务，按正常 Shutdown 收尾。

| 验证面 | 本轮结果 | 能证明的行为 |
| --- | --- | --- |
| Contracts | 3 项通过 | Broker 正常请求／响应、首次线程绑定、兼容旧调用的双截止字段 |
| Worker | 5 项通过 | 可控时钟跨越 40 分钟；到期或撤权后不复活；较短证明与旧序号；Sorftime 服务身份用本地 MCP 在拒绝和允许后分别观察调用次数；真实轮次停止与单次审批错误区分 |
| Agent Host | 9 项通过 | 原生权限映射和自动拒绝承接、专用市场决定入口、双截止、受管代理配置、续期路由、首次提交与重读、工具关联及撤销 |
| Desktop | 原生 1 项、Vue 4 项通过 | 临时加密数据库验证非空选集拒绝 auto/full，空选集保留原模式；审批卡的展示、动作、断连与历史 |
| 固定 Runtime + 产品 Worker | 1 项通过，约 12 秒 | `TestMarketRenewalAndTerminalStopAcrossToolsInCodeMode` 跨过原始截止后出现新的审批。该调用被拒绝，随后权限自然到期，同一 Code Mode 脚本后续市场调用停止，普通计算仍返回 42 |

上述 **23 项现有链路检查通过**，另完成上节的 **3 个原生对照**。40 分钟是可控时钟覆盖的跨度。Sorftime 用例走本地正常协议端，集成用例走 `kimi-web` 的本地元数据及拒绝／到期分支。真实 Sorftime 排行榜数据、付费模型、线上供应商写操作和新增三模式的端到端效果均未在本次审计验证。全量回归和故障／攻击注入不属于此次定向审计，相关结果不计入通过数。[Worker 用例](../../../../yijie-connectors/worker/src/broker.rs#L1704) · [Native 模式用例](../../../../yijie-desktop/src-tauri/src/chat/connectors/selection_tests.rs#L459) · [实跑集成用例](../../../../yijie-agent-host/internal/codex/tool_search_gateway_integration_test.go#L186)
