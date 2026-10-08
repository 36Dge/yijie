# FEAT-157 私有 Broker 控制与下一步执行

2026-10-07，承接 [08 审计](08-implementation-audit-and-next-step.md)。本轮依据用户“给出下一步执行方案，并开始执行”推进本地实现；不继承旧功能的真实模型或平台调用额度。

## 本轮计划

1. Contracts 先新增独立 `market-broker-control/1`，复用既有选集源；明确进程、Native scope、不可变选集、真实 Turn、有限租期、单次调用决定和正常退出语义。
2. Connectors 实现常驻 Rust worker 控制模式和官方 rmcp Gateway；Host 直接持有进程与独占管道。保留原只读状态模式，全部真实服务仍未资格化。
3. 使用正常生命周期验证真实构建的 Host→worker 控制链，并以固定实际 Runtime→Rust Gateway 验证普通本地合成 lookup 的接受、拒绝和撤销。外部请求、真实凭据、付费模型均为零。
4. 审查实现与证据后，再接 Native→Host 的可信授权投影、版本化提交、通用审批与结果投影；最后解除有资格服务的 UI 发送门禁。

本轮独立私有 family 按 additive 实施：原 management 55 定义、selection 18 定义和旧 Native/Host 路径保持原解释；FEAT-157 整体仍沿用保守的 breaking 分类。当前是源码摘要固定的本地候选，不是已发布 pin 或人工审查批准。

## 已定实现边界

- Host 直接托管 Rust worker，不新增纯转发进程。控制面是独占 stdin/stdout JSONL；数据面是 loopback Streamable HTTP，复用官方 rmcp 和固定 Codex client。
- 内部随机 bearer 按 Runtime generation 管理，只用于数据入口认证。它不进入控制 DTO、参数、日志、回执或持久状态；非秘密 capabilityRef 只定位租期。平台凭据仍属于 Connectors。
- prepare 接受已经冻结的选集快照；租期最多 300 秒，并夹紧到可信 Native 授权到期时间，再用单调时间执行。重复操作不会续期或复活已撤销/过期能力。同一真实 turn operation 只能关联一份选集。
- 真实工具请求到达后才能创建 callRef。worker 冻结已校验参数、登记摘要及安全审阅投影；Host 查询该记录，不能从 metadata 拼造批准。私有决定和原生 elicitation 都同意后，只消费一次调用准入。
- EOF/关闭首先撤销新准入，再正常关闭 listener 和清理。超时保留 STOP_PENDING 及所有权，不强杀、不自动重建进程，不声称已发出的外部请求被撤回。
- Native→Host 可信 grant 尚未装配。当前内部状态机和资格驱动不对 renderer/HTTP 路由开放，不把结构有效的 scope JSON 当作产品授权。全部 51 项真实 provider 保持未资格化，UI 和 Native 执行门禁保持关闭。

## 本轮结果

私有控制源、Rust Broker/Gateway 和 Host owner 已实现。它们是本地内部基础能力，尚未连接 Native 授权投递或公开 Host 路由；产品执行仍关闭。

- Contracts 新 family 提供 55 个定义、8 个控制动作及 Go/Rust 投影；原 management/selection 源与旧 pinned generator 保持不变。18 项专项（JS 7、Go 5、Rust 6）、Clippy、lint、同源同步通过。
- Rust worker 保留原 auth_status 模式，新增常驻控制模式；HTTP Gateway 使用官方 rmcp 1.8，平台出站继续预留固定 Codex client adapter。新增准入、选集/真实 Thread/Turn 绑定、调用登记、单次决定、到期/撤销与 EOF 清理。最终 19 项普通单测通过，实际 Runtime 联调见下文。
- Host 新 `internal/marketbroker` 直接持有 canonical worker，校验产物、帧、响应及完整绑定；一次只发送一条控制请求，核验完响应才开放下一条。取消前不启动、关闭后不重开、超时只发送 EOF 并保留所有权。现行 Runtime 仅新增清理父环境中的同名内部能力，不注入新权限或改模型配置。
- Host 最终 6 项单元、4 项真实 owner 集成均通过 race 检查；本次最终集成的 5 个 worker 正常退出，其中 revoke/shutdown 各在 1024 条合法回执满容量后验证 EOF 退役。旧候选尝试保留，累计 18 个 worker 均正常退出。
- 最终 fresh [run-06](evidence/broker-qualification/run-06/verification.json) 通过：固定真实 Runtime 的新会话首轮批准后执行一次，同一会话续轮冷恢复后拒绝、零执行；冻结参数与原生 Tool Item 对应，撤销后的原 prepare 不复活。40 条控制帧通过同源 schema；4 次本地合成 Responses 请求、2 次 Gateway elicitation；Runtime/worker 均正常 EOF、exit 0。
- 内部随机能力原值未出现在本次观测的控制/原生/provider wire 或新建临时文件；检查只覆盖本次资格配置，不替代后续产品环境装配。真实外部 MCP、OAuth、账号凭据和收费模型调用均为零。

产物分别是产品 worker `f36db7e719175d4a60b7f0133776704cfe5d30faaf930f8981f75dff4322f415`、单独资格程序 `68d4e5c98d3ce46fc9703133f20bb8c2dc3e697ef6792219ec182f2893fb4fea`。资格程序明确 `qualificationOnly=true`，Host 产品准入拒绝该产物；它不会把合成工具加入 51 项目录。详细来源、普通容量/退出验证见 [Host 记录](../../../../yijie-agent-host/docs/market-broker-verification.json) 和 [Connectors 记录](../../../../yijie-connectors/docs/market-broker-verification.json)。

### 实测与审查推动的修正

| 问题 | 修正与证据 |
|---|---|
| 新 thread 尚无首轮时没有 rollout，不能 unsubscribe 后冷恢复装入连接器 | prepare 用必填 `nativeThreadId:null` 明确新会话意图；thread/start 一次带入 Gateway 配置，再以真实响应绑定 Thread/Turn。已有 thread 继续正常冷恢复。没有假 ID 或隐式暖机模型轮 |
| 正常权限续期改变 scope expiry/revision 可能改变去重键，使原轮次重新准备 | reservation 只用稳定 owner/tenant/Native epoch/session/真实 turn operation；续期不延长或复活原能力 |
| rmcp 官方 server 在派发时从 params 移走 `_meta` | 根据固定库 `service.rs:1168` 从 RequestContext.meta 读取真实关联；不改变 metadata 只作关联线索的地位 |
| 合成只读 lookup 未声明准确 annotations，触发额外原生审批 | 仅为固定合成工具补真实只读提示；没有把这些提示套给 51 项真实工具 |
| 取消发生于未绑定等待或 Accept 同时就绪时，仍可能登记/消费 | 等待监听取消，登记前后及 Broker 消费点复核，select 优先处理取消；三项普通取消测试通过 |
| 回执容量满也会拒绝 revoke/shutdown，可能留存活动租期 | Host 收到这两动作的 capacity_exceeded 后，在串行 gate 内发送 EOF、永久退役整代 owner，保留原 typed 错误，再确认正常退出或 STOP_PENDING；不伪造撤销成功或外部业务完成 |

首次资格失败、SDK 适配失败和观察器错误均保留于 [资格记录](evidence/broker-qualification/README.md)。其中 run-04 已通过首轮，但观察器在同 thread 的第二轮错误重读首轮 elicitation；run-05 修正为精确 Thread+Turn 过滤，run-06 在最终取消修复产物上重新验证。

### 未完成及未执行

- 当前 worker 最多保留 64 租期、128 个调用记录、1024 个变更回执。128 包括已终态记录，比 `maxPendingCalls` 更保守；不删除 tombstone 腾挪准入。产品长会话的正常 generation 更替仍须随 Host 装配处理。
- Native→Host 可信 grant、版本化提交、真实 Runtime 配置注入与通用审批/结果产品投影仍待实现。资格驱动只验证机制，不是产品审批 authority，不计 D4。
- 真实工具支持范围、OAuth/Keyring、Google 实际包、供应商 URL/费用/重试资格仍按 05 推进；51 项全部保持未资格化。
- Contracts 老全量生成受旧远程 schema fetch/EOF 阻断；正常 JS 全套仍有 2 项历史基线失败，详见其 [验证说明](../../../../yijie-contracts/docs/market-broker-control-validation-2026-10-07.md)。包含危险归档生成和攻击注入 fixture 的两项旧测试按用户安全条款未执行，不称全量绿色。
- 未启动 canonical Desktop、未迁移用户数据库、未更改 Runtime 源码或固定 binary、未提交/推送/发布。原用户三份店铺文件 diff 摘要保持不变。

元仓收尾的 lint、50 项治理测试、Feature Package 结构/claims、新文档链接与六仓 diff 检查通过。汇总与逐文件来源见 [broker-control-checks.json](evidence/broker-control-checks.json)；这些治理检查不是产品或供应商验收。

## 后续产品接线顺序

1. 从 Native 当前权限租期和 SQL31 快照生成可信投递，Host 固定校验本地 authority；安装状态和 generation 仍以 Native 为主，不在 Broker 新建安装数据库。
2. 版本化 Host 提交沿用现有操作锁和 pending/accepted/uncertain 回执。已有 accepted 回执先重读，模型和选集只在一次受管 idle/cold-resume 中合并变更；空集显式关闭所有市场入口。
3. 以真实原生 Turn 事实绑定，终态、取消、权限变化和进程 generation 关闭时撤销；通知早于响应时也不能猜测身份。
4. 通用 market 审批及 MCP 结果增加独立契约投影，复用既有回调和脱敏生命周期，不改变 Sorftime 专用语义。
5. 再完成 OAuth/Keyring、真实 stdio 包及逐服务工具/费用/重试资格，最后开放可验证的实际服务。真实外部条件不足时具体记录缺项，不用合成结果替代 51 项接通。
