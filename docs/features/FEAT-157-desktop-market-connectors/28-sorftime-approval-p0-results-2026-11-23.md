# FEAT-157 · Sorftime 原生审批 P0 验证记录

2026-11-23，北京时间。共检查 14 条 P0 用例。TC-14 根据用户最新要求排除。

**已在真实 Sorftime 安装证明「始终允许此工具」跨桌面重启生效。** 账号 A 的 `category_name_search · US` 对照组保存成功，重启后新会话首笔命中 `native_always`。原用例指定的 `product_search · US` 在保存步骤失败，两种模型都只显示单次人工审批。当前商品查询尚不能按 FEAT-157 的原用例验收。[冷启动证据](evidence/2026-11-23-sorftime-p0/cold-restart.json) · [真实工具定义与审核摘要](evidence/2026-11-23-sorftime-p0/tool-definitions.json)

## 真实冷启动

| 检查点 | 账号 A 的实际结果 |
| --- | --- |
| 保存 | MiniMax-M3、请求批准、US、类目词 `outdoor`。在下拉中点击「始终允许此工具」，回执 `approve_always`、`appliedPersist=always`、`admissionConsumed=true`，外发 1 次并收到响应。界面显示「已保存长期授权」，详情和原生配置均读到 `category_name_search · US`。 |
| 正常退出 | 通过 ⌘Q 正常退出。桌面、Host、Worker、Runtime 的旧 PID 分别为 81286、81291、81295、81297，随后均已结束。 |
| 同目录重开 | 新 PID 分别为 4304、4310、4314、4316。启动时正常探测一次。退出前、完全退出、重开就绪三个检查点的累计业务外发数均为 8。重开后原生配置仍是 `approval_mode=approve`。 |
| 首笔 | 新建 MiniMax 会话，显式选「请求批准」和同一安装。第一次调用没有人工卡，回执为 `native_always`、`admissionConsumed=true`，新发 1 次并收到响应，累计数升至 9。保存笔与重开首笔都收到 4 条类目记录。 |
| 调用关联 | 保存笔 `dacff1c7-2e80-4d36-b625-de9cf5cfcfc1`，重开首笔 `56ebbf80-aa54-4887-b0d3-73c9780b62f1`。线程和调用编号均已更换。安装 ID 与 generation 1 保持一致，启动探测使 revision 从 4 变为 5。 |
| 原商品查询 | 另做过一次完整冷启动。保存前没有长期选项，首笔自然到期；同目录重开后新会话仍出现人工卡，选择取消。两笔分别外发 0 次，第一次冷启动本身也外发 0 次。 |

[带 PID、原生规则、调用与计数的快照](evidence/2026-11-23-sorftime-p0/cold-restart.json) · [每笔 Runtime 回执与 Worker HTTP 记录](evidence/2026-11-23-sorftime-p0/desktop-calls.json)

## 工具定义

| 工具 | Worker 已审核的完整 schema SHA-256 | 账号 A 实连，Host 记录的 Worker schema SHA-256 | 原生资格 |
| --- | --- | --- | --- |
| `product_search` | `d17fb37f0a94847b073735527f9e0feda5b79bcc5dd249ecefe33ae63635b5a4` | `29698a089c8b9182ae19e171054e4b072062b0bba8662e716482811ce389a452` | `risk=write`，无 `persistOptions`。表示 Worker 未确认只读。 |
| `category_name_search` | `af32a2bbe17bf185d958e11ec12e3bd703e284a8a5aa11a11c4df77fbdd273af` | `af32a2bbe17bf185d958e11ec12e3bd703e284a8a5aa11a11c4df77fbdd273af` | `risk=read`，实际提供 `session` 和 `always`。 |

原用例 Q 使用 `{"amz_site":"US","search_name":"outdoor"}`。账号 A 当前收到的商品工具声明提供 `keyword`，已没有 `search_name`。另用当前声明的 `{"amz_site":"US","keyword":"outdoor"}` 重发，仍显示相同的单次人工卡。Worker 同时检查完整定义摘要和实际参数字段。当前改用 `keyword` 可以发起正确形状的查询，完整定义的只读资格仍需独立审阅。[真实调用与字段差异](evidence/2026-11-23-sorftime-p0/tool-definitions.json) · [Worker 审核逻辑](../../../../yijie-connectors/worker/src/generic.rs#L179)

## 逐项结果

表中「基准」均指用例指定的商品查询 Q。「类目对照」使用同一真实账号的 `category_name_search`。计数为 Worker 发出的 Sorftime 业务 HTTP 请求增量。

| 用例 | 结果 | 观察与证据 |
| --- | --- | --- |
| TC-02 三种模式发送 | 发送通过，榜单口径受限 | 三个独立新会话都保留了 Sorftime 和选定模式，均未出现旧红字。三次均调用 `product_search(US, keyword=outdoor)`，人工允许后各外发 1 次。每次原始响应 20 条，含月销量、年销量与子类排名，缺少七日销量。这些数据无法验证最近一周户外类目销量前 30。回环模型的回复明确说明了缺口，本轮未测线上模型自行选工具或撰写榜单的能力。[三笔调用](evidence/2026-11-23-sorftime-p0/desktop-calls.json#L700) |
| TC-03 允许一次与下拉 | 基准下拉失败，单次通过 | MiniMax、Kimi 各自第一次为 `approve_once`、1 次，再次发 Q 都重新询问，`cancel`、0 次。基准缺少会话和长期选项。真实类目卡显示了三个选项，组件测试也逐一点击验证了它们。[桌面回执](evidence/2026-11-23-sorftime-p0/desktop-calls.json#L37) · [审批卡测试](evidence/2026-11-23-sorftime-p0/component-results.json) |
| TC-04 拒绝与取消 | 通过 | 三个不同 `callRef` 的决定依次为 `reject`、`cancel`、`cancel`。三笔均未消费许可，外发量为 0、0、0。[三笔回执](evidence/2026-11-23-sorftime-p0/desktop-calls.json#L149) |
| TC-05 会话授权 | 基准无法保存，类目对照通过 | 真实 GB 类目卡选择「本会话允许此工具」后显示「仅本会话有效」。保存和同会话续轮分别为 `approve_session`、`native_session`，各 1 次。另一会话和冷启动恢复的原会话都重新询问，各取消 0 次。原生配置只出现另外保存的 US 长期规则。冻结版 Q 在三个独立 Runtime 进程的协议验证中也满足会话边界。[真实记录](evidence/2026-11-23-sorftime-p0/desktop-calls.json) · [原生协议记录](evidence/2026-11-23-sorftime-p0/component-results.json) |
| TC-06 始终允许跨重启 | **基准失败，真实类目对照通过** | 商品工具无法保存长期规则。类目工具实测保存、重启、首笔的业务增量为 **1、0、1**。另用已审核的历史商品定义在独立原生 Runtime 复验，进程 57202 保存 `product_search · US`，进程 57265 新会话首笔命中 `native_always`，本地协议端也是 1、0、1。[两次桌面冷启动](evidence/2026-11-23-sorftime-p0/cold-restart.json) · [冻结版原生复验](evidence/2026-11-23-sorftime-p0/component-results.json) |
| TC-07 管理与撤销 | 类目实连通过，基准无法建规则 | 在详情撤销 `category_name_search · US`，界面回读为空。返回命中过旧规则的同一会话，重新出现审批卡，取消后为 0 次。查看、撤销和刷新均未发起业务查询。另以只读权限的组件身份验证可以查看规则，不能点击撤销。[撤销后回执](evidence/2026-11-23-sorftime-p0/desktop-calls.json#L1455) · [权限组件记录](evidence/2026-11-23-sorftime-p0/component-results.json) |
| TC-08 工具和站点范围 | 基准缺少前置规则，类目对照通过 | 基准改 GB、换类目方法以及换 `camping` 都出现人工卡。建立真实 US 类目规则后，同工具同站点换 `camping` 命中 `native_always`、1 次；另一会话的 GB 类目与 US 商品均重新询问，各取消 0 次。冻结版 Q 同时验证换站点、换方法各 0，换普通关键词 1。[桌面记录](evidence/2026-11-23-sorftime-p0/desktop-calls.json) · [冻结版范围验证](evidence/2026-11-23-sorftime-p0/component-results.json) |
| TC-09 换绑、停启、重装 | 两个实连分支通过，原地换绑未验 | 每个类目分支均重新建立并确认 US 规则。账号 A 停启后列表为空，同方法拒绝 0 次。正常卸载并由用户在新表单重新录入同一个 A，安装 generation 从 1 变为 3，列表为空，拒绝 0 次。两个操作顺序使用同一隔离配置。已启用的桌面安装提供停用与卸载，缺少独立的原地换绑入口。B 仅在本地账号范围样本中验证，不作为真实换绑通过。旧范围在隔离 Runtime 配置中仍有两条存储记录，当前安装的列表和实际调用均未继承。[逐笔安装代际](evidence/2026-11-23-sorftime-p0/desktop-calls.json#L1763) · [最终原生配置快照](evidence/2026-11-23-sorftime-p0/cold-restart.json) |
| TC-10 帮我批准允许 | 基准回退人工，类目对照通过 | MiniMax 提交 Q 后出现人工卡，取消 0 次。已确认只读的真实类目查询进入原生 Guardian，回执 `native_auto`、1 次。[真实决定来源](evidence/2026-11-23-sorftime-p0/desktop-calls.json) |
| TC-11 帮我批准拒绝与超时 | 基准回退人工，类目对照通过 | Kimi 基准的拒绝来自本人，单笔自然到期也未外发。类目工具经过 Guardian 后取得 `native_auto_reject`，0 次。随后在「自动审核需人工确认」卡上点「允许一次」，旧调用仍未执行，总数维持 11。另发新调用并让审核自然超过单笔截止，原生结果为「单次审批已到期」，许可未消费、0 次。[Guardian 回执](evidence/2026-11-23-sorftime-p0/desktop-calls.json#L1543) · [人工接管前后计数](evidence/2026-11-23-sorftime-p0/cold-restart.json) |
| TC-12 完全访问 | 风险确认通过，基准回退人工，类目对照通过 | 取消风险弹窗后仍是「请求批准」，下一笔取消为 0。用户确认启用完全访问后，MiniMax 新会话和 Kimi 续轮的基准都出现人工卡，各取消 0。真实合格类目在两条模型路径均得到独立 `native_full` 回执，各 1 次。[桌面回执](evidence/2026-11-23-sorftime-p0/desktop-calls.json) · [风险弹窗组件测试](evidence/2026-11-23-sorftime-p0/component-results.json) |
| TC-13 缺少站点 | 通过 | 三种模式实际参数都只有 `search_name=outdoor`，审批卡没有记忆下拉，三次取消均为 0。另用冻结定义先保存 US 的 Q 规则，再用缺站点输入验证，三种模式均只提供单次人工选项且不命中旧规则。[真实三笔](evidence/2026-11-23-sorftime-p0/desktop-calls.json#L285) · [已有 US 规则的对照](evidence/2026-11-23-sorftime-p0/component-results.json#L832) |
| TC-16 整轮自然到期 | 受控时钟与原生 Runtime 分层通过 | 生产 Worker 受控时钟推进到最后一份证明自然到期，旧许可、重新发现及缓存工具均不能发送。真实 Runtime 的 MiniMax 直接调用和 Kimi 缓存调用均收到终止标识并移除市场工具；Kimi 在同轮继续计算得到 42。新的 Worker 轮次重新批准 Q，本地 Sorftime 查询端收到 1 次。整个用例未调用续期接口。[Worker 到期结果与两条模型路径](evidence/2026-11-23-sorftime-p0/component-results.json#L731) |
| TC-17 不配对旧端 | 兼容样本分层通过 | Host 或 Worker 分别不报告原生审批版本时，「帮我批准」「完全访问」四个组合都在入队前被拒绝，SQLCipher 中待发提交为 0。界面测试确认错误提示、草稿、Sorftime 选集和模式保留，手动切回「请求批准」后可重发相同请求。Native 兼容样本接受请求批准，旧卡允许选项只有「允许一次」，Worker 的本地查询端收到 1 次。[兼容矩阵、草稿和旧 Worker 回执](evidence/2026-11-23-sorftime-p0/component-results.json#L760) |

## 证据口径

- 桌面实连使用独立 Native、Host 和 Codex Home，账号 A 的凭据由用户在 Worker 表单输入。桌面固定构建使用 MiniMax-M3 和 Kimi K3.1 Pro 的原生模型路径，模型端和 Guardian 判词来自本地可重复的 Responses 测试端。Sorftime 工具发现与业务响应来自真实供应商。[版本、构建及环境](evidence/2026-11-23-sorftime-p0/environment.json)
- 共观察到 **43 个不同的 Sorftime 业务调用编号**。其中 15 笔消费许可并发出业务 HTTP 请求，15 笔均收到响应。另 28 笔均未消费、未外发。商品查询 5 次，类目查询 10 次。每笔按相同 `callRef` 关联 Runtime 原生回执和 Worker 的发送、响应记录，已排除初始化、工具发现及模型请求。用户确认 Sorftime 后台看不到独立明细，按要求跳过供应商后台对账。[43 笔明细](evidence/2026-11-23-sorftime-p0/desktop-calls.json)
- 历史定义的协议样本、受控时钟以及旧版本兼容用例都在独立测试数据中运行。报告保留了它们各自的模型路径、原生阶段、业务计数和断言。[分层测试证据](evidence/2026-11-23-sorftime-p0/component-results.json)
- 日常客户端已从标准入口重新启动，日常 Sorftime 显示「已启用」，窗口已恢复到原先的「扩展」页。与本轮相关的新增文件为本报告及证据，产品代码没有改动。[验证环境](evidence/2026-11-23-sorftime-p0/environment.json)

[原测试用例及验收标准](27-sorftime-approval-test-cases.md)

