# 连接器全局启用与当前对话选用纠正

2026-11-01。用户澄清：列表应表达连接器全局已经启用，关闭的开关仅表示当前对话未选用；同时修复开关轨道和圆钮显示。此前将“启动默认关闭”解释成全局停用属于错误实现，本轮撤回该行为，技能/专家资源修复保留。

`contract-impact = semantic`：调整本地启动恢复行为及 Desktop 进程内展示，复用现有 SetEnabled/provider_probe、真实回执、权限和 Native 选集校验，无公共 wire/schema、Runtime 或业务数据库格式变化。用户已授权修正、恢复启用和审计；已于本轮确认正常退出。现有工作树补丁保存在 `.local/audits/connector-enabled-selection-20261101/before.patch`，不提交、推送或覆盖其他工作。

## 真实状态审计

在客户端及子进程均停止后，使用此前审计的只读 SQLCipher helper 查询安装和操作历史，仅读取非秘密状态。只读打开、query_only、trusted_schema=OFF；查询前后原数据库 SHA-256 完全相同，没有数据迁移或手改状态。

| 连接器 | 历史事实 | 修复前事实与处理 |
|---|---|---|
| Shopify | 曾 72 次启用成功；上一轮启动停用为 suspend | 安装/配置保留，恢复真实全局启用；当前对话不自动选择。 |
| Kimi 网页检索 | 曾 33 次启用成功；上一轮两次停用为 suspend | 配置保留，复用客户端 Kimi 凭据恢复启用；准备不派发模型轮次。 |
| Sorftime | 曾配置成功、6 次启用成功；最新历史停用的 provider kind 为 forget | 当前 generation=4、credential_ref 为空；需要用户在原安全配置入口重新配置。不能仅修改标签为已启用。 |
| Tushare | 曾授权成功、4 次启用成功；最新历史停用的 provider kind 为 forget | 当前 generation=2、credential_ref 为空；需要用户在原浏览器授权入口重新授权。不能使用旧成功回执作为当前连接证明。 |

记录证明的是凭据绑定被历史清除；本轮没有输出、恢复或猜测凭据正文，也没有任意复用旧 generation。机器证据为工作区 `.local/audits/connector-enabled-selection-20261101/actual-connector-state.json`。此表记录重新配置前的审计状态，配置完成后的真实状态见下文最终核验。

## 修复

- Native 启动恢复 `desiredEnabled=true` 的已配置连接，使用新 Host 的正常 provider probe 获取实时就绪；不自动调用授权/配置、不派发业务工具、不自动选用到聊天。
- 对本轮明确要求恢复且配置仍在的 Shopify/Kimi，分别使用两个固定、scope 绑定的普通 Enable operation ID 完成一次纠正；结果由原 provider/receipt 路径生成。之后用户明确停用时已有该回执，启动不再覆盖该选择。失败/未决也保留原回执，不重复发送同一启用。
- 一个供应商探测失败不能隐藏其他连接器目录；缺少配置的条目不进入自动探测队列。
- 连接器菜单始终显示真实的“已启用”全局状态，不再隐藏或映射成“不可用”。开关仍取 `selectedIds`，全局已启用而当前对话未选用时 `aria-checked=false` 且可操作；使用权限/任务状态仍可独立限制选用。
- 保留 Naive UI Switch，局部修正禁用轨道和白色圆钮 token，避免退化成孤立灰点。未就绪连接器仍不能凭 UI 开关绕过配置和真实资格。

## 验证

- 58 项前端/资源定向测试通过；包含全局已启用与未选用并存、对话开关不触发全局启停、失联可取消选用、配置缺失提示及资源保持。
- Native 一次恢复、真实回执后的用户停用保持及正常关闭/重开凭据保留回归通过；没有外部供应商调用的测试 fixture。
- 前端 lint/build、文档构建、最终 Native Clippy `--all-targets --features kimi-k31-pro-candidate -- -D warnings`、`git diff --check` 均通过。
- 通过现有日常入口重开，实际 Native 最初报告 Shopify probe pending，随后同一操作经正常观察完成：重新配置前 snapshot 为 installed=4、enabled=2、pending=0。Shopify/Kimi 恢复真实连接，未向聊天自动加入选集。技能仍为 7 项已安装/已启用，专家仍为 21 位（19 位资源 ready）。没有为了造绿重发启用或调用业务工具。
- 实际浏览器渲染生产 `ChatConnectorControl`：合成的全局已启用状态与四个关闭、可操作的对话开关并存；点击选用仅改变 selectedIds 0→1→0，全局状态保持；亮/暗主题及禁用态已检查。开关为 32×18，亮色轨道 rgb(231,231,231)、暗色轨道 rgb(81,86,93)，圆钮均为 rgb(255,255,255)，没有孤立灰点。
- 样式截图分别保存在 `.local/audits/connector-enabled-selection-20261101/switch-style-light.jpg` 和 `switch-style-dark.jpg`。截图页面明确标注合成状态，不作为真实供应商连接证据；真实状态来自 `live-startup-diagnostics.txt` 及上述只读数据库记录。
- **最终核验通过**：用户已在原产品安全入口完成 Sorftime 配置、Tushare 授权并启用。随后真实 Native snapshot 为 `installed=4, enabled=4, pending=0`，四项全局启用均已确认。服务 readiness 为 ready，7 项技能已安装、已启用且 runtime-visible，专家目录仍为 21 位（19 位资源 ready）。证据保存为工作区 `.local/audits/connector-enabled-selection-20261101/final-verification.json`。客户端保持运行。

上述配置完成时的启用状态来自真实 Native/provider 观察；当时默认关闭的当前对话选集及开关外观通过组件交互与亮暗主题检查验证，尚未进行四项配置完成后的额外重启。随后按用户要求完成下面的实际日常重启复验。

## 四项配置完成后的日常重启复验

2026-11-01，用户明确要求再按原日常入口正常重启一次。本次仅执行正常启停与只读核验，`contract-impact = none`，没有实现、契约或持久化语义变更。

- 用户通过“易界 → 退出易界”正常退出；系统进程核对确认 Native、Host、Worker、Runtime 和启动器均已退出，原数据根校验通过。未发送强杀信号。
- 通过 `/Users/jack/Applications/易界.app` 原入口打开，观察到“正在启动服务并加载易界…”；专用服务经原数据核验正常就绪，新 Native 进程 PID 为 7845。
- 仅核对本次启动日志（起始 byte offset 485982）：技能 `installed=7, enabled=7`；专家 `experts=21, resources_ready=19`；连接器保存启用意愿为 4。一个原启用操作短暂 pending，随后正常观察得到 `installed=4, enabled=4, pending=0`。未为验收重发启用或派发业务工具/模型调用。
- 电脑控制工具无法读取未打包的原生窗口，因此实际界面由用户目视核验。用户明确回复“全部正常”：7 个技能、21 位专家正常显示；4 个连接器显示“已启用”；当前对话 4 个开关默认关闭，完整灰色轨道与白色圆钮显示正常。该结论不使用合成组件截图代替实际界面验收。
- 原 authenticated workflow readiness 通过，客户端保持运行。证据保存于工作区 `.local/audits/connector-enabled-selection-20261101/daily-restart-before.json`、`daily-restart-diagnostics.txt` 和 `daily-restart-verification.json`。

未执行强杀、权限破坏、攻击注入、二进制替换或付费模型/业务工具测试。真实外部账号配置、授权由用户通过原产品入口完成；不能在聊天中索要密钥或把未配置状态伪装为已启用。
