# FEAT-144 固定 Runtime 复测与 D0 决策

> 历史阶段记录：操作7/8已在固定0.144.6上成功，累计8/10；连接阻塞已关闭，当前业务依据与D0结论见[13](13-connection-closure-and-d0-review-2026-09-10.md)。下文失败、额度与待验证结论保留当时范围。

2026-09-10。本记录是本阶段的当前结论，补充并取代 03、05–09 中的待验证状态；历史记录及其适用范围保留。**固定 Runtime 接入仍阻塞，D0 BLOCKED；未进入产品实现。** 本轮实际 contract-impact=none，仅需求、诊断编排及证据；未来跨仓实施仍按 breaking 保守治理。

## 1. 同流程验证结果

使用 09 已成功的原生诊断编排，保留无 query URL、Bearer 环境引用、现有系统 HTTPS 代理、隔离 CODEX_HOME、空 ephemeral 线程、read-only/on-request/user、plugins=false 和 experimentalApi=false；仅更换被调用的原生二进制。新增 manifest 校验及证据目录/来源标签不改变 RPC 流程。没有修改全局 Codex 配置、启动 yijie 应用或创建模型 Turn。

| 对照 | 本地应用原生 0.153.4，操作 4/5 | 项目固定原生 0.144.6，操作 6 |
|---|---|---|
| thread/start 触发 MCP 初始化 | starting → ready | starting → failed |
| 原生错误 | 无 | initialize 返回 HTTP 400，响应预览为 `request error` |
| 后续工具列举 | 单独计数，返回 97 个工具 | 未执行；初始化失败即停止 |
| product_detail schema | 已取得 inputSchema | 未取得，不沿用应用结果冒称固定版本成功 |
| 退出 | thread/unsubscribe、stdio EOF、exit 0 | thread/unsubscribe、stdio EOF、exit 0 |
| 输入秘密检查 | 新目录/stdout/stderr 无精确值命中 | 新目录/stdout/stderr 无精确值命中 |

操作 6 的原生错误链明确为 `MCP startup failed` → `handshaking with MCP server failed` → `unexpected server response: HTTP 400: request error, when send initialize request`。失败发生在 MCP initialize 的 HTTP 响应阶段，尚未进入产品 Tool 执行。`failureReason` 为 null，不补造错误码。程序退出码 0 只证明正常关闭，不代表 MCP 成功。

本轮用了 **1 次**元数据操作；累计 **6/10，剩余 4**。本轮优先最多 2 次的上限没有用满，也不需要用满。原生内部 HTTP span 观察到 1 个 POST；重复 enter/exit 不是多个请求，完整底层请求数仍为 null。模型请求、业务 tools/call、图片均为 **0**。次数权威为[共用台账](evidence/sorftime-discovery-ledger-2026-09-10.json)，安全结果见[操作 6](evidence/sorftime-native-discovery-operation-6-2026-09-10.json)。

### 已定位的范围与尚未定位的根因

已经排除“只因旧 status-only 诊断隐藏启动失败，换诊断流程就能成功”的解释；同一 thread/start 流程在固定版本仍失败。旧 `mcpServerStatus/list` 路径丢弃启动事件接收器，过去只有 HTTP 400、没有具体启动错误；新流程解决的是可观测性。

固定代码在 `yijie-codex/codex-rs/codex-mcp/src/rmcp_client.rs` 的 `mcp_initialize_request_params` 以原生协议 **2025-06-18**、client `codex-mcp-client` 发起初始化。`rmcp-client/src/http_client_adapter.rs` 设置 JSON/Accept/Bearer 并由原生 HttpClient 发送，读取非 2xx 响应正文。现有 MCP 配置没有可核实的 protocol_version 覆盖项。

服务只返回通用 `request error`，未指明不兼容字段；应用与固定版本也不是同时请求。因此**不能宣称已证明协议日期、clientInfo、HTTP 实现或代理中的哪一项是唯一原因**，也不能据此判断密钥无效。没有抓取 Authorization、解密代理流量或自行重发 MCP HTTP 报文来定位。

### 处理路径

1. **首选保持冻结基线**：将时间、客户端版本、协议日期和脱敏错误整理给 Sorftime 支持方，请其确认是否接受该原生初始化及 Bearer，并提供 MCP 专属能力/费用/错误文档。本记录即提供可转交信息，不含凭据；本任务不自行发送外部消息。
2. 只有服务方或原生源码给出明确的受支持配置修正，才在剩余额度内做最小原生复测；不添加猜测 header、伪装版本或恢复 query-key。
3. 若服务要求变更 Runtime，则另立受权的 Runtime 兼容变更决策，重新核验来源、权限和受影响需求。**本任务不升级、替换、修改 Runtime，不把已安装 0.153.4 偷换成项目来源。**
4. 若保持当前 Runtime 且服务方不能兼容，FEAT-144 继续阻塞。应用版本成功仅作为服务与配置有效性的对照；不能通过新 MCP 客户端、bridge、代理或 SDK 绕过。

## 2. 来源与工作区

执行前已记录 11 仓分支、完整 HEAD、remote、未提交路径及 SHA-256，见[前置快照](evidence/fixed-runtime-comparison-preflight-2026-09-10.json)。五个主要仓库均为 `chore/retirement-baseline-20260905`：

| 仓库 | 完整 HEAD |
|---|---|
| 元仓 | 6f12939aa85f8a9c1f55e89f1018c60501a2f494 |
| Contracts | db7a607c1c091fc4f4243829d68d5b673eb7e2c3 |
| Host | f4cf01bd6f7e9f37792ef743d44f0ce10527c10b |
| Desktop | 228a95a4929a53bbb6aafc76156161d642d72153 |
| Codex | 6c1ad767f0997845b8258a1c452fd4eb7577579f |

Host/Desktop native Contracts pin 仍为 `6f632f155eacdaf93df0e0b00b5dab9e369c5442`，Desktop 权限 Host pin 为上述 f4cf01 完整提交；四份 lock 的 47 项内容摘要与固定提交及当前来源均一致。没有因文档修改机械更新 pin。

Runtime build `b2b20e2fc4a0c94834f34d8cc459e488a1b56277`；binary SHA-256 `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`；manifest SHA-256 `1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b`。固定 build 到当前 Codex HEAD 的 `codex-rs` 子树无差异。

Desktop 原 11 路径并发界面工作已经单独提交为 228a95a…，当前工作树干净；本次未覆盖或纳入 FEAT-144。元仓既有 FEAT-144 文档、历史和 FEAT-131/记忆修改保留。本阶段无提交、推送、tag、部署，canonical 入口仍是未来的 `pnpm tauri:demo-fast:app`。

## 3. 业务依据与准确缺口

| 项目 | 已有依据 | 本次决定/缺口 |
|---|---|---|
| 服务与工具 | 操作 5 原生发现的 Sorftime MCP 1.1.6、product_detail | 只允许原生 `enabled_tools=["product_detail"]`；不开放其余工具 |
| 输入 | 原生 required 只有 asin；amz_site 枚举含 US，默认 Unknow | 产品策略要求一个用户明确给出的公开 ASIN、显式 `amz_site=US`；不改写外部 schema 的 required/default |
| 用户价值与发起 | 单个 US 商品详情及忠实摘要 | 原有项目 Composer；缺参数先澄清，不搜寻、批量、写收藏或上传文件 |
| 只读 | 原生描述为单商品数据查询 | 可据此选型，尚无 readOnlyHint 或服务方无写副作用保证；发现目录不等于批准调用 |
| 幂等 | 无 annotations/正式承诺 | 不能承诺同一输入恒定结果、免费重试或账务幂等；原生重试语义保留 |
| 费用 | 官网将 MCP 能力文档/价格引向 MCP 控制台 | 本次公开访问仅取得需登录的控制台壳，未读取账号；API/CLI 调用量价格不适用于 MCP，账户价格/失败计费/重试计费未知 |
| 结果 | 原生未返回 outputSchema，也未调用 product_detail | 不预定价格、销量等字段名或单位；产品安全字段映射待正式 MCP 结果文档或另授权取样后固定 |
| 普通业务失败 | 未找到可核实、符合 inputSchema 的自然失败说明 | 不把无数据当失败，不试坏 key/异常网络/额度耗尽/攻击；AC-004 保持 pending |

原 inputSchema 与 SHA-256 保留在[单工具证据](evidence/sorftime-product-detail-schema-2026-09-10.json)，仍明确由应用 0.153.4 发现。没有 outputSchema、annotations 或 progress 不能通过文档补造。

本次只读查阅 [Sorftime MCP 官网](https://www.sorftime.com/zh-CN/mcp/index?tag=)及其链接的 [MCP 控制台](https://open.sorftime.com/mcp)，不登录、购买、请求账户记录或执行业务接口。官方 [Codex 接入说明](https://www.sorftime.com/zh-CN/mcp/Codex)的 Bearer 依据及操作 4/5 的成功继续有效。公开检索范围与文件摘要见[业务资料核验](evidence/sorftime-public-business-review-2026-09-10.json)。

**当前不申请或消耗业务取样额度**：固定 Runtime 尚未接通，先解除兼容问题和取得正式说明更有效。若之后仍缺结果样本，可单独提出 `product_detail({asin:一个已知公开US商品, amz_site:"US"})` 一次逻辑取样，明确原生内部重试/费用口径；必须先确定具体安全参数并获授权。没有正式正常失败条件时，不为凑失败测试盲试多个 ASIN。

## 4. 首期秘密与环境方案定稿（设计，未实施）

首期 **只存内存，不持久保存 MCP Account-SK**。复用现有 canonical 启动编排、Desktop 原生受管 sidecar 和 Host 原生 Runtime 子进程环境配置；不新建 vault、通用 SecretStore、凭据 HTTP API、秘密数据库或 Keychain 管理功能。既有数据库 Keychain 和 SQLCipher 保持其原职责，不借其保存 MCP token。本次真实诊断继续用隐藏输入，未安装产品入口。

未来实现路径固定为：canonical 原生隐藏输入 → 受管启动进程内存 → Desktop 原生层受控 sidecar 环境 → Host 内存 → 仅该 Runtime 子进程中的专用环境变量 → 原生 `bearer_token_env_var`。值不进入 shell 命令参数/历史、普通 env 文件、WebView/Composer、TOML、Host 状态或诊断输出。进程退出即不保留；正常重开需要重新输入，取消输入仅保持 MCP 不可用，旧历史仍可读。原生内存对象避免 Debug/Serialize、尽早释放可释放副本，不声称可擦除操作系统全部内存副本。

现有复用点是 Desktop `src-tauri/src/chat/sidecar.rs` 的 `env_clear`/显式 `environment`、Host `internal/codex/runtime.go` 的 `runtimeEnvironment` 以及 Codex 原生 `bearer_token_env_var`；**它们目前并未实现 Sorftime 传递**，后续只加该秘密的封闭分支，不能直接继承父进程全部环境或复用 MiniMax 的具体 Key 值。Host 在 spawn 前剔除外来同名值，仅注入本次显式输入；配置只包含环境变量名和固定无 query endpoint。不得读取用户已有凭据或把提供的 token 写成测试样例。

环境过滤必须用原生 `shell_environment_policy.exclude` 显式排除专用变量及入口别名，并在最终解析配置中检查。**原生 `protocol/src/shell_environment.rs` 先 exclude、后应用 set，set 可以重新加入被排除变量**；因此只写 exclude 不够，必须确认 set、shell 启动配置及其它启用的执行路径没有重新注入。`core/src/tools/handlers/shell/shell_command.rs` 与 `core/src/unified_exec/process_manager.rs` 复用原生环境构造；其它实际启用工具/子代理入口逐项核验，没有证明隔离时不激活 MCP，不自行改写 Runtime 环境引擎。

实施验收用普通合成哨兵值验证内存传递、环境过滤、日志/配置/新增事实无值；不打印真实值，不枚举用户秘密、不检查用户数据库、不使用攻击命令。真实 D4 的模型/命令环境验证仍 NOT RUN，本次无模型诊断的秘密检查不能冒充该验收。

当前代理条件只在本地诊断成立：沿用系统已有 `http://127.0.0.1:7890` HTTPS 代理，不新建代理、不关闭 TLS。未来 canonical 使用当前可用且批准的网络配置，不把本机代理地址固化为产品默认；不能确认网络条件就停止接入。本机同用户权限下的主动进程内存读取不在本期正常测试范围，不声称环境过滤提供进程级秘密沙箱。

## 5. 原生审批、展示与兼容方案

- 复用稳定默认 `mcpServer/elicitation/request`。仅 Sorftime、可信当前线程/非空 Turn、已确认的原生 Prompt 空 form；工具精确白名单及原生 per-tool prompt 配置先于调用生效。原生请求没有可靠 itemId/结构化 toolName，展示在线程请求面板，不猜 Tool 卡归属。accept/decline/cancel、serverRequest/resolved、回调失效由原生决定；一般表单/URL/认证/实验 requestUserInput 继续拒绝。保持 FEAT-152 三模式语义，不增设自动批准路径。
- 传输、鉴权和资源上限继续保留。结果来自真实完整 McpToolCall；安全投影采用待核实的最小字段，内容按不可信纯文本/安全结构显示，禁止激活返回链接、执行返回指令或读取远端图片来补卡。未知结构显示“结果格式尚未支持”，availability 降级但原生 status 不变，不能据此宣称真实商品成功。原始错误只用允许代码/固定文案，正文不入日志。
- 原生 Item/Turn、原生 status、内容 availability、当前 busy、观察/冷历史来源分离；完整对象替换，0/null/合法空保留。唯一 NativeDisplayBuffer、SQLCipher facts/views、thread/read/resume 强制复用，不再累积、对账、封口或猜身份。
- Contracts 先定义确实需要的最小身份/结果/诊断及审批请求边界，检查新旧方向；然后提交兼容 reader，确认所有受支持读取方能安全读取/拒绝新内容，再激活 Host/Desktop 新字段写入。旧闭合 schema 不原地扩展，旧 `deny_unknown_fields` 不假定自动兼容。回滚只能回到经过验证的兼容 reader；不能删新事实、改历史 migration 或令单条新 Tool 阻断全部旧历史。
- 执行顺序继续是 Contracts → 兼容 reader → Host/Desktop 原生适配 → 定向验证 → canonical → 真实 D4。受影响来源才按真实 commit/digest 更新 pin，不改 Codex Runtime、不重启 FEAT-137、不放宽门禁。

## 6. D0 审查与下一阶段条件

| D0 事项 | 本轮状态 | 剩余条件 |
|---|---|---|
| 固定 Runtime 可行性 | BLOCKED，已复现并取得原生失败原因范围 | 受支持配置/服务兼容证据及固定来源原生复测成功；或另获 Runtime 决策授权 |
| 工具/输入/用户入口 | DESIGN COMPLETE，输入有真实依据 | 原生白名单和参数约束实施属于后续 AC，不在 D0 编码 |
| 结果/只读幂等/费用/普通失败 | BLOCKED，未虚构字段或价格 | MCP 专属正式资料；必要时另授权安全业务取样 |
| 秘密/环境、审批、reader-first | DESIGN COMPLETE，implementation NOT RUN | 设计明确；后续实施的定向验证必须通过才激活 |
| 授权与交付边界 | 明确 | 元数据 6/10；未来模型/业务预算、实施、提交/推送另授权 |

因此本次不能将 product_ux 改为 PASS，十项 Must 继续 pending、实现 blocked、canonical/D4 NOT RUN。**阻塞是选定服务与固定来源未接通、业务依据不足，不是要求先有产品或先完成 D4 才过 D0。** 当前已完成可安全执行的核验和方案细化，未把未解决条件伪装成“完整实施依据”。

写入后进行与诊断运行分开的文档/源码自审：检查版本结论、计数、秘密入口、set 重注入、审批缺关联、结果缺字段、reader-first、历史范围和并发保护；这不冒称独立人工评审。适用文档检查及 D0 的真实退出码见[本轮检查](evidence/fixed-runtime-d0-checks-2026-09-10.json)。未运行产品测试、canonical、真实业务、模型和 CI；本轮未提交推送，也未触发远端 CI。

检查结果：strict、元仓lint、50/50测试、19包审计、Shell/diff、原生与v4来源、FEAT-137退役检查通过；D0实际exit1（product_ux.status仍pending）。[最终工作区记录](evidence/fixed-runtime-d0-final-workspace-2026-09-10.json)核实11仓HEAD与47项来源未变、非元仓干净及历史保护。当前结论为完成本阶段安全核验和决策记录，D0本身尚未通过。
