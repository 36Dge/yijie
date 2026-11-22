# 连接器三种审批模式的本地实施记录

2026-11-22 · FEAT-157 · local / demo_fast · contract-impact = breaking

## 发送和执行

Desktop 用当前 Native 权限冻结新提交，连接器选集、模式和审批版本一起进入原有出站事务。Host 在私有握手中报告固定 Runtime 的能力。Native 同时从每个所选安装的实时 Worker 状态核对版本。配对成功后，「帮我批准」使用原生 Guardian，「完全访问」使用用户已确认的原生 full 策略，「请求批准」展示本次 MCP 确认实际提供的选项。旧版本配对仍可按「请求批准」处理单次决定。其他模式返回可识别的发送错误，编辑器保留草稿和选集。[提交准入与冻结](../../../../yijie-desktop/src-tauri/src/chat/connectors/selection.rs) · [Worker 能力核对](../../../../yijie-desktop/src-tauri/src/chat/connectors/provider.rs) · [原生模式映射](../../../../yijie-agent-host/internal/codex/runtime_permissions.go)

MiniMax-M3 通过 Codex 既有的 MCP 命名空间适配器接收市场工具的直接函数。Kimi K3.1 Pro 通过原生工具发现和 Code Mode 调用同一 Gateway。首次配对验证发现 MiniMax 收到未经适配的 namespace；将已选市场服务加入原生函数配置后，两种模型均取得带原生 Item 的真实调用回执。[Host 市场工具装配](../../../../yijie-agent-host/internal/codex/market_turns.go) · [共用原生函数配置](../../../../yijie-agent-host/internal/codex/native_tools.go)

Gateway 先按逐轮选集登记实际工具、参数、安装和调用截止。Runtime 经现有 MCP elicitation 回调查证该笔调用，再交给原生审批。批准结果由 Host 通过既有私有管道送回原 Worker。Gateway 收到原生许可且成功消费该笔一次性许可后才向供应商发送。Guardian 拒绝、本人拒绝、取消和单笔到期均可独立结束该次尝试。原始业务结果和决定来源使用既有原生 Item 的市场回执关联。[Runtime 适配](../../../../yijie-codex/.yijie/patches/chat-models/0032-native-market-approval.patch) · [Host 回调](../../../../yijie-agent-host/internal/codex/market_approvals.go) · [Worker 发送许可](../../../../yijie-connectors/worker/src/gateway.rs)

## 工具授权如何记住

- 「允许一次」只完成当前调用。「本会话允许此工具」使用 Codex 的 `ApprovalStore`。同一原生 thread 因下一轮市场配置变化而重新建立 session 时，原生 store 仅交接该 thread 的市场工具会话决定。新 thread 独立审批。
- 「始终允许此工具」复用 Codex 的工具批准配置项与配置编辑器。键按用户、租户、安装代际、已绑定账号、最近一次改变授权的管理操作、实际工具、schema 和目标派生。启动时重新探测会提高安装 revision；同一账号的正常探测沿用原生授权。更换账号、重新授权、停用或重装会使原授权失效。新进程沿用同一产品 Home 时可读取同一授权。选择长期记忆后，界面依据实际回读结果显示长期或会话范围。连接器详情可以查看长期授权并逐项撤销。[作用域与原生决定](../../../../yijie-agent-host/internal/codex/market_native_approval.go) · [原生配置读取与撤销](../../../../yijie-agent-host/internal/codex/market_remembered_rules.go)
- Sorftime 的 11 个已审阅 Amazon 查询方法按真实方法名和完整输入 schema 摘要核对，调用时校验站点和声明参数。其他方法继续依照各自的业务审核要求处理。原生长期授权只省去同范围的人工确认，下一次调用仍要取得当前轮次有效许可。[Sorftime 工具资格](../../../../yijie-connectors/worker/src/generic.rs)
- Native SQLCipher 50 为新提交记录协商版本，旧行保持原有语义。决定历史继续使用现有观察表，原生配置仍是长期授权来源。回滚须保留能读取 50 的客户端，关闭新 writer 并正常撤销活动租约。[迁移](../../../../yijie-desktop/src-tauri/migrations/chat/0050_market_native_approval.sql)

## 验证范围

| 场景 | 可复核的观察 |
| --- | --- |
| 原生批准与冷启动 | 在独立 Home 运行标准构建的真实 app-server。回环 Responses 端提供普通模型与 Guardian 响应，本地 MCP 在接到许可时计数。读取原生 user config、通过标准输入 EOF 正常退出，再启动新进程及新 thread。11 个场景均通过，冷启动后的首次调用记录为 native_always，本地服务收到一次。 |
| 原生撤销 | 以原生 user layer 的版本调用 `config/batchWrite`，回读已清除的工具规则。原活动 thread 下一次调用重新出现单次确认。 |
| Native 配对与存储 | SQLCipher 测试覆盖三模式的已配对提交、两个方向的旧组件回退、历史回执和版本 50 正常重开。独立的启动回归按正常路径重新探测，验证 revision 增加、原账号授权仍可识别、显式停用后其标识改变。 |
| 界面 | 生产审批卡的会话和长期按钮分别提交对应的原生决定。长期规则列表验证分页、只读权限和撤销后的回读。1180×760 亮暗主题及 380×720 窄屏均通过键盘选中长期授权的检查。Vue 类型检查和前端构建通过。 |
| Sorftime 续期 | 使用冻结的真实 `product_search` schema 与进程内本地 MCP。十次同身份续期跨越 40 分钟可控时钟，旧批准到期；新调用匹配 full 来源，发送一次，二次消费失败。另三项 Worker 续期回归覆盖缩短、撤权和旧证明。 |
| 轮次终止兼容 | 在 0031 基线上验证后，又用新的 0032 Runtime、产品 Worker 和本地模型实跑 Code Mode。旧单笔拒绝后同一轮仍可继续，续期最终到期后缓存的兄弟市场工具停止，普通计算继续。 |

[构建摘要与逐笔实测结果](evidence/2026-11-22-native-approval/implementation-results.json) · [独立 Runtime 复验程序](evidence/2026-11-22-native-approval/native_approval_probe.py) · [真实 Host / Runtime / Worker 配对用例](../../../../yijie-agent-host/internal/app/market_native_approval_integration_test.go) · [Worker 续期用例](../../../../yijie-connectors/worker/src/broker.rs) · [桌面 SQLCipher 用例](../../../../yijie-desktop/src-tauri/src/chat/connectors/provider.rs)

业务数据验证使用回环或进程内样本。真实 Sorftime 排名、真实账号的供应商额度及付费模型调用未纳入本轮实测。所有重启均在独立路径正常退出；日常客户端和个人数据库未用于迁移或重启。未执行强杀、权限破坏、可执行文件替换或攻击注入类用例。

## 配对验收

Runtime 补丁 0032 已提交到 `yijie-codex`，提交号为 `7653af22da39898c86128904540eeb2eeedc26da`。标准生成器已核验该提交内的补丁、构建脚本、实际 Runtime 以及 276 个 app-server schema，并将同一配对清单同步到 Host 和 Desktop。日常桌面入口已通过标准来源、契约、Runtime 及资源预检。Broker Control 0.10.0、Market Provider 0.7.0、Market Host v1 0.7.0 / v2 0.9.0 为本次本地候选。

配对用例通过生产私有 JSONL 通道注册选集和决定，经带鉴权的 Host HTTP 接口提交并读取终态。两个独立的操作系统进程先后承载生产 Host 会话服务，各自启动真实 Runtime 和产品 Worker。第一进程正常退出后，第二进程才重新打开原数据。11 个场景均逐笔核对了原生决定来源、原轮次、安装、单笔许可消费和本地 MCP 收到的业务请求，合计 8 次。

| 场景 | 实测结果 |
| --- | --- |
| Kimi 会话授权 | 「允许一次」后下一轮重新询问。选择「本会话允许」后，同一会话第三轮命中 `native_session`，执行一次。 |
| MiniMax 跨重启 | 选择「始终允许」后从原生配置读到一条规则。正常关闭私有通道、Runtime 和 Worker，重开同一 Host 数据库和 Codex Home，用新进程身份重新探测安装。新会话第一笔命中 `native_always`，业务请求恰好一次。 |
| 撤销与重装 | 撤销后回读零条规则，下一笔出现审批，点「取消本次」后业务请求为零。再次保存长期授权后，正常移除并登记新的安装代际；同名工具重新请求确认，拒绝后业务请求为零。 |
| 帮我批准与完全访问 | 实际 Guardian 分别处理允许和拒绝，业务请求计数为 1、0。MiniMax 的已确认完全访问产生一次业务请求。 |
| Sorftime 授权续期 | 6 项 Sorftime 定向检查与 3 项通用续期检查通过。配对 Runtime 的真实 Code Mode 轮次到期回归也通过。 |

原生数据库和界面回归采用独立数据。付费模型、真实供应商查询、日常账号窗口及发布均不在本次验收范围内。


用于复验的入口为 `yijie-desktop/scripts/market-local-protocol.py --output <新的临时目录>` 和 `yijie-agent-host` 下的 `go test -count=1 ./internal/app -run '^TestMarketApprovalThroughProductRoutesAndRestart$' -v`。测试选择器为 `YIJIE_MARKET_NATIVE_APPROVAL_E2E=true`。将 `YIJIE_CODEX_INTEGRATION_BINARY`、`YIJIE_CODEX_INTEGRATION_MANIFEST` 指向配对清单 `runtime_relative_path` 下的 `codex`、`runtime-manifest.json`，将 `YIJIE_MARKET_BROKER_TEST_MANIFEST` 指向 Connectors 的 `bin/market-worker/current.json`。协议端在业务请求结束后经自身的 `POST /control/stop` 正常退出。

## 分仓提交后复验

本次使用下列提交运行标准生成器，并从已提交的 Connectors 源码重新构建 Worker。Runtime 和 Worker 的 SHA-256 均与前次验收一致。

| 仓库 | 复验提交 | 内容 |
| --- | --- | --- |
| `yijie-codex` | `7653af22da39` | 0032 原生审批补丁 |
| `yijie-contracts` | `e2f107e06527` | Runtime 与契约依赖的来源记录 |
| `yijie-connectors` | `8590ee3dc7af` | Worker 兼容的 Runtime 源码与协议摘要 |
| `yijie-agent-host` | `7994bbaac314` | Host 调用接口的配对提交 |
| `yijie-desktop` | `3450d5fd2b49` | 桌面引用的 Host、契约与资源版本 |
| `yijie-api` | `2644a8018352` | API 引用的内置检索契约摘要 |
| `yijie-skills` | `a4abcb8d0fdf` | 专家目录引用的市场契约摘要 |

两个独立 Host 进程先后打开同一份临时数据。MiniMax 在第一个进程保存长期授权，第二个进程的新会话首次调用命中 `native_always`，本地 MCP 收到一次请求。撤销后取消、重新安装后拒绝的请求计数均为零。11 个产品链路场景通过，共产生 8 次本地业务调用。

Sorftime 专项 6 项、通用续期 3 项及真实 Code Mode 到期回归均通过。可控时钟覆盖 40 分钟、同一身份连续续期 10 次，旧调用仍到期，新调用只消费一次许可。桌面来源预检、2 项 Native 重开检查和 3 项审批组件检查也通过。完整提交号和独立计数保存在[验证结果](evidence/2026-11-22-native-approval/implementation-results.json)的 `postCommitVerification`。
