# FEAT-157 实施记录

> 最新审计与后续执行见 [08 审计和执行方案](08-implementation-audit-and-next-step.md)：已修复卸载/worker生命周期问题，新增版本化选集源、SQL31原子冻结和兼容reader隔离。以下保留第一轮实施事实。

## 授权与范围

2026-10-07用户明确要求根据需求包与设计包开始逐步实现。本轮采用已展示的B方案：平台凭据在Connectors、Native SQLCipher保存非秘密产品状态、Codex原生MCP执行，Contract First。本次用户请求是本地实施授权；不等于付费/账户/生产写入/Git提交推送授权。

整体contract-impact仍保守breaking；独立新family及expand改动按实际兼容证据逐项记录。D0产品方案据本轮明确指令确认；Q-SEL原生资格与供应商接入资格不是D0状态替代品，未通过不得激活相应能力。

## 实施顺序与当前活动

1. 固定Runtime本地无秘密/无外部网络资格：start选集、loaded/cold resume、正常EOF退出；无需商业模型。
2. Contracts独立market-connectors本地family，生成TS/Rust/Go，保留旧严格协议。
3. Native SQLCipher非秘密安装、幂等操作/revision、scope权限和同源IPC。
4. 市场/已安装/详情与Composer纯组件，接真实管理状态后进行整合。
5. 按资格结果补Host/Broker选集与凭据流程；供应商未知项不猜测。
6. 正常安全验证、逐项结果记录、审查与后续继续。

当前仅按技术依赖逐步编码，不新设治理切片或宣称部分功能等于51项完成。基线与用户原改动见evidence/implementation-start.json。

## 已实现的本地候选

| 仓库 | 实际改动 | 当前边界 |
|---|---|---|
| Contracts | 独立 market-connectors 源、55 个定义、9 个 Native IPC、TS/Rust/Go 及 AJV 生成、开发来源摘要与同步脚本 | 旧 family/source pin 不变；开发候选不是发布来源。私有执行控制面另列设计，尚未注册 |
| Connectors | 51 项无秘密公开目录、独立供应商候选资料、固定 Codex 库 Rust worker、Go 正常 EOF owner 与内部装配点 | 当前 worker 仅提供真实进程的 auth_status；HTTP/OAuth 库适配编译通过，目标未准入，不执行外部请求 |
| Desktop Native | SQL30 前向扩展、固定作用域权限、9 个生成协议 IPC、原子安装/本地卸载与幂等回执、revision/generation 隔离 | 不含平台凭据；未配置服务不能启用；清理需 Broker 时不假报完成 |
| Desktop UI | 六类市场/已安装/详情、51 本地图标、聊天店铺右侧入口和可移除标签、管理往返共享草稿与模型/工作空间意图 | 使用生成客户端读取 Native 状态；全部真实服务仍未资格化，未开放带连接器的 turn 提交 |
| 元仓 | 本实施记录、运行资格证据、ADR-0021、源材料保留 | D0 已由本轮明确要求确认；D4 尚未运行 |

安装不会启动 npx、打开 OAuth 或调用模型。51 项“目录已收录”不表示“51 项已接通”。所有服务的实际连接资格继续未通过；当前无可有效启用的市场连接器。旧普通对话入口保留，非空连接器选集不会偷偷降级为旧提交格式。

## 固定 Runtime 的本地资格

证据见 [runtime-qualification](evidence/runtime-qualification/README.md)。使用原有 FEAT-156 五补丁实际二进制，没有改写 Runtime 源码或制品。仅运行普通 loopback MCP 与合成 Responses 数据，不访问第三方、账户或收费模型。

- Q-SEL-01：空 `mcp_servers` 对象不能清掉全局服务器；必须显式将未选全局项关闭。两线程能够获得各自选集。状态查询会进行真实发现，不能当成完全无作用的读操作。
- Q-SEL-02：已加载线程直接 resume 会忽略配置；idle 后正常 unsubscribe，再携带完整配置 cold resume，可以保持原 thread/历史并变更新选集。
- Q-SEL-05：标准 form elicitation 的 `_meta` 可原样携带 opaque callRef。Gateway 先登记实际调用，Host 独立查询同一工具/参数/turn 并登记决定，再回复原生 elicitation；两个正常示例分别接受后执行一次、拒绝后执行零次。见 [审批资格报告](evidence/runtime-qualification/qsel05-report.md)。这是本地机制证明，尚非产品审批主链。
- stdio：公开 `InProcessTransportFactory/DuplexStream` 可桥接独立 owner 持有的真实子进程；初始化/列工具/只读 lookup 后，通过关闭 stdin 正常 EOF 回收，子进程 exit0。见 [stdio 资格报告](evidence/runtime-qualification/stdio-report.md)。未运行真实 Google 包，不代表其 token 文件已解决。
- 退出均走正常 EOF；没有强杀、替换程序、权限故障或攻击性 fixture。

## 已完成的专项验证

最终命令结论、六仓 diff 检查和原用户改动保护摘要见 [implementation-checks.json](evidence/implementation-checks.json)。

| 检查 | 结果与证据范围 |
|---|---|
| Desktop `cargo test feat157 --lib` | 8 PASS；SQL29→30 保留普通既有会话项目行和 migration ledger；原子回执、重复意图、重装 generation、未配置启用与作用域权限 |
| Desktop `cargo clippy --all-targets -- -D warnings` | PASS |
| Desktop `pnpm check:native` | PASS；既有 Native/计划家族及新连接器生成物一致 |
| Desktop `pnpm lint`、`pnpm build` | 最终 UI 源码冻结后 PASS；构建仍有已有的大 chunk 提示 |
| Desktop 生成客户端专项 | 8 PASS；严格请求、响应版本/关联、前向字段投影与可用状态一致性；变更回执不可确认时保留原操作编号 |
| Desktop UI/路由/权限/草稿专项 | 9 文件 84 PASS；含管理回执、context 续期、只读权限禁止重投、unknown install 恢复、聊天标签与模型草稿。见 [测试日志](evidence/ui-specialized-tests.log) |
| 浏览器组件视觉 | 亮暗 1180×760、200% 缩放、详情/菜单滚动与键盘焦点检查通过；使用明确标注的合成状态，不是 Native 产品验收。见 [视觉记录](evidence/ui-verification.md) |
| Contracts | JS 9、Go 5、Rust 5、Clippy/TS、仓库 lint PASS；三个历史 breaking 基线 PASS。当前 fallback 检查被旧 scheduled-plan-draft 外部 schema 下载 EOF 阻断，未改写为 PASS |
| Connectors | 固定源码闭包、Rust 3 tests/Clippy、canonical worker 构建、真实 worker 往返、Go race/vet PASS；详见该仓 `docs/market-connectors-foundation-verification.json` |

上述不是全仓 CI、真实供应商测试或 D4。ChatPage 的同样 5 项失败已用 HEAD 原始源码对照复现（50 PASS、2 SKIPPED）；没有修改这些旧断言以掩盖基线问题，见 [原 HEAD 对照日志](evidence/chatpage-baseline-tests.log)。浏览器截图已在工具 trace 中查看，但独立文件未成功归档，因此不提供假截图路径。Vite 已正常关闭，测试浏览器标签已关闭。

审查修正：不能识别或不属于本请求的 mutation 回执统一视为结果未知，沿原 operation 查询；响应操作、应用、安装、动作相互匹配后才接受。相同本地 scope 的权限 context 续期保留原请求/回执并隔离旧异步响应，真实账户/权限切换才清除。初始三份用户店铺改动的合并 diff SHA256 仍为 `50ca7a1165be0732b4e74d119340303c39529e5bd40b9845bed0c02d672b4eeb`，没有混改。

## 接下来仍需完成

1. 将已通过的 Broker 实际调用与原生审批关联机制落实为正式控制契约：定稿控制面 carrier、Native 冻结选集的 digest 和参数摘要规则，再 source-first 生成。
2. 接入 Host/Gateway 可信 turn 能力及撤销、单次批准、正常清理；补版本化提交/outbox/历史 refs 和原生结果投影。
3. 完成真实凭据原生交接、OAuth/Keyring、Google 正常 EOF bridge 与 token 存储资格；处理库内重试语义。
4. 按供应商事实逐项关闭接入条件，确定支持工具、合法账号和调用范围；再执行 canonical 全路径及 51 项真实资格。

下一步控制契约的具体候选保存在 Contracts 的 `docs/market-connectors-broker-control-candidate.md`：优先复用父进程独占 JSONL 管道，Native 在提交事务冻结专用 selectionDigest，实际调用参数由 worker 冻结并登记；尚未生成未验证的授权端点。当前控制能力和平台凭据分开，不将测试临时控制 header 作为正式 API。

未调用真实模型、外部 MCP 元数据/业务、OAuth 或真实平台凭据；未迁移用户日常数据库、未提交/推送或发布。禁止行为保持未执行，其影响是不能声称强杀恢复或攻击测试覆盖；替代证据只来自正常开发和测试。
