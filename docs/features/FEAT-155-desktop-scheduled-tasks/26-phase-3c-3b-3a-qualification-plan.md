# FEAT-155 · 下一步执行方案：3C-3B3A 受限草案执行资格收口

2026-09-19。本轮用户要求根据当前实现给出下一步方案；**只读复核并保存方案，没有开始本批实现、启动服务或真实调用。** 推荐下一次只执行本方案，报告后停止，不自动进入完整原生装配或第四阶段页面。

本轮文档 `contract-impact=none`。未来若修改 Host 固定配置/准入解释，至少按 semantic 重新分类；新增 wire、持久格式或 Runtime 变化需按实际最高影响重新审议。本方案不预设新 SQL23、Host7、依赖或 Runtime 补丁。

## 1. 为什么现在先做这一步

[25报告](25-phase-3c-3b-implementation-report.md)的 B1/B2 候选实现与合成证据继续有效。当前165份业务候选摘要全部吻合，五仓 HEAD/branch/remote 未变；普通 Desktop SQL15、Host Store5，显式候选22/6，实际 `ScheduledDraftReady()` 恒 false。候选代码通过不等于真实草案可用。

现在最有价值的结果是回答：**固定 Runtime、stable 协议、复用原 Host/Runtime 的既定边界内，能否证明草案只生成建议而不会执行任务或读取不应读取的数据？** 先解决它，才能准确决定后续原生装配与页面的能力提示、失败出口和实际验收。总生成入口的 dirty Contracts 保护继续保留，不通过清理工作区或修改无关 public API 生成链来推进。

| 本轮核实的事实 | 对下一步的影响 |
|---|---|
| Host `internal/codex/baseline.go:109–135`固定双补丁产物；保留 binary SHA `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`、manifest SHA `1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b`吻合；来源 `b2b20e2fc4a0c94834f34d8cc459e488a1b56277:codex-rs` 与当前 Runtime HEAD 的 tree 同为 `755f32c45a4c30e805e3c7fe1db89dcb4dcc6e41` | 目前没有证据支持“源码与实际 Runtime 版本错配”；仍需固定完整来源链再验证策略 |
| FEAT-144 的“不支持 profile”指 app-server CLI `--profile`，不是 `default_permissions`；见该需求21文档第11行 | 不能据此否定命名权限配置，也不能据源码参数存在宣布配置已生效 |
| Runtime `protocol/v2/thread.rs:193,426`的 activePermissionProfile 属 experimental；`protocol/src/models.rs:458–475`只定义 id/extends | 即使开 experimental，单一 profile ID 也不证明有效读根或完整工具范围；不采用“开实验字段即可解锁” |
| Runtime `config/src/merge.rs:11–31`递归合并 map，空 `mcp_servers:{}`不删除基底服务器 | 当前草案输入配置不能单凭空 map 声称已关闭继承的 MCP；必须核实合并后的真实状态 |
| Runtime `core/src/config/mod.rs:3711–3778,4228–4255`含 fallback 与辅助读根；`core/src/tools/spec_plan.rs:678–757`仍有 update_plan/view_image | 普通 readOnly、prompt、禁用几个工具名均不是完整证明；展示工具与可读取/执行工具需按实际行为区分 |
| Host `internal/codex/sorftime.go:231–295`已有 stable config/read 的原生配置校验模式 | 可以复用检查方式，但 config/read 不自动等于 thread override 之后的最终权限/工具状态 |

上述是两项并行只读技术复核与主代理源码复核，不是独立人工批准；没有使用合成结果证明真实权限。

## 2. 下一批只做以下四步

| 顺序 | 执行内容 | 完成标准 |
|---|---|---|
| 1 | 固定产物、配置层、目录及协议证据 | 明确实际 binary/manifest/schema 来源、原 Host 配置加载链、草案目录和普通会话共存边界；不把 CLI profile 与权限 profile 混为一谈 |
| 2 | 建立逐项权限与能力证据表 | 对读写根、网络、shell/扩权、MCP及资源、图片/Web、skills/hooks/plugins、协作/记忆、辅助根/fallback 分别记录“允许什么、凭什么证明、缺什么即拒绝”；start/resume/follow-up 一致；字段/别名/已移除键以固定 Runtime 为准 |
| 3 | 只修能够被证明的最小 Host 策略和判定 | 先确认 stable 证据可闭合，再修固定配置、必要内部 adapter 和资格失效条件；复用原 Manager、原 operation/恢复接口。不得用人工 bool、环境开关、单一 profile ID、prompt 或模拟 Runtime 返回值替换证明 |
| 4 | 零调用验证、技术审查与明确结论 | 同源配置/协议检查、普通聊天权限回归和必要正常重开通过；明确输出“已具备策略资格”或“具体证据不足，需要哪一个最小决策”，报告停止 |

第三步有依赖，不能无条件承诺把 false 改成 true。若第二步已经证明现有 stable 路径无法覆盖必要边界，应结束该条实现路线，完成第四步的决策稿；不能继续堆叠永远拒绝的候选代码并宣称已经解除阻断。

### 资格判定必须包含的语义

- 资格绑定当前实际产物、受管配置及其代次、确切草案目录、schema/policy 和会话用途；正常重开、resume、配置或能力变化均重新核实，不复用过期证明。
- 禁用继承 MCP/skills/hooks 等必须依据合并后状态及实际注册/执行路径；不能为草案修改全局普通聊天的 FEAT-152 或 FEAT-144 行为。
- 任意未知、fallback、目录不符、受限配置缺证据或可执行工具仍可达，均保持明确不可用。可接受的仅展示事件不应被误当成执行能力。
- Runtime 策略资格、Provider 对固定 outputSchema 的真实支持、产品发送资格是不同事实。前者通过不消除后两者的验证要求；不把本批结果写成对话创建已真实验收。

### 验证边界

先进行源码/同源 schema 和普通进程内协议验证。获准执行本方案后，若能在启动前证明不会触发模型、MCP/商家或其它外部请求，可使用**原 Host 与已固定 Runtime 的正常协议入口**进行最小 config/read/start/resume 观察，并正常停止/EOF清理；这些是零模型协议证据，不是端到端产品验收。零外部请求预检覆盖 Runtime、MCP、plugins、skills 初始化和模型目录自动刷新，而不只是检查是否发送 turn；任一项无法证明零请求，即不启动。正常观察限一次完整采样和一次正常重开，仅在有明确修正时复验；这些观测本身不能证明模型实际可用工具范围或 Provider 的 outputSchema 支持。若无法预先保证零外部调用，跳过该项并记录缺失证据，不以临时代理、另一 Runtime、伪造可执行文件、另一个 Codex Home 成功结果或覆盖用户配置来宣称当前产品合格。

本批模型调用0、图片0、商家/MCP外部调用0；12次文本总额不变、累计0/12。不得强杀、破坏权限、注入攻击资源或替换已固定二进制。不读取/迁移日常用户库或 Keychain，不启动定时投递、执行 turn 或真正生成草案。不新增通用资格平台、执行器、测试App或长期常驻进程。

## 3. 决策分支与交付标准

推荐优先验证**现有 stable 能力 + 同一 Host 的最小严格校验**，因为它保留已接受职责和固定 Runtime。退出结论分开记录：

1. **可证成**：明确证据完整性与失效条件，落最小 Host 修正，定向验证后报告；普通入口仍15/5、候选22/6，真实发送/Provider验收不自动开启。
2. **不能证成**：给出最早缺失的具体原生证据或隔离能力，以及最小新增能力的源码范围、契约/兼容影响和验证代价；资格仍 NOT QUALIFIED。需要改固定 Runtime、开启 experimental、改变普通权限/共享运行方式或降低既定隔离目标时，作为新决策交用户，不擅自实施。这种结果表示可行性调查收口，不能标注草案资格 PASS。

不推荐先做完整页面：布局能够推进，但核心“通过对话创建”只能不可用，能力与失败文案仍依赖上述结论。不推荐默认升级/patch Runtime 或增加独立 Provider/Runtime 通道：会越过本需求已批准复用和固定来源边界。不能静默删掉对话创建、放宽为普通全盘 readOnly 或只保留手动创建来取得表面完成。

交付物只包括：固定来源证据、权限/工具证据表、最小 Host 变更（仅可证成时）、同源及安全检查、普通路径回归、明确的资格或阻断结论。不以16小时时间盒阻断本需求；也不在没有新增证据时重复探测。

## 4. 后续顺序，只登记不在本批实施

| 后续批次 | 已知必须完成的原需求事项 |
|---|---|
| 3C-3B3B：原生装配与恢复 | 统一 SQL22/Host6、同一 scope/受管根/Coordinator 的候选装配；分别授予读取/保存/手动/自动/草案资格。当前三个 worker candidate constructor 尚未组成正常产品入口 |
| 同批必要恢复与能力投影 | draft attempted 保留但尚不在 scheduled run 的恢复扫描内；复用 task mapping/session-operation 查询补精确绑定与原生观察，不重发、不清 attempted、不猜 Host 来源。补按 conversation/turn 重新发现 draft source 的只读方式，以及按操作划分的诚实能力/原因；需要新字段/格式时先另行 source-first 评估，不预设 SQL23 |
| 第四阶段：页面及必要查询补齐 | 接 PDF 页面和两种创建/三目标、卡片/历史/完整对话；补名称与内容搜索、创建时间正倒序（当前只有名称搜索，缺创建时间事实）、真实运行时钟投影；历史或确实缺失事实保留 unknown，不以始终 unknown 替代详情要求。不能把当前 IPC 存在当作原页面需求已全部覆盖 |
| 同阶段原范围能力与最终验收 | 应用内重要更新、macOS本App生命周期防空闲睡眠；系统通知仍延期。正常入口、预算计数与 Provider 资格就绪后再安排12次文本总额内的真实验证，全部 Must 同次 fresh run 后才判断 D4 |

不扩大云调度、退出后运行、OS cron、跨设备、MCP工具服务或新权限模式。本轮也修正 feature.yaml 中仍写“B1/B2未实施、候选21”的当前状态字段；历史报告和旧测试结果保持原语义。

**本方案执行后报告停止；没有自动推进 B3B、页面、日常库激活、付费调用或提交推送发布的授权。**

本轮方案检查：strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法及五仓diff检查均PASS；122处变更文档本地链接有效。仅修改7份元仓需求文档，四个产品仓全部起点文件逐字节保持，五仓HEAD/branch/remote未变；没有产品测试、服务、日常库/Keychain或真实调用。两项只读技术审查的修订已纳入，未发现剩余方案阻断；这不等于真实策略资格通过。

## 执行结果（2026-09-19，保留上文原方案含义）

用户随后授权执行本方案；结果见[27资格报告](27-phase-3c-3b-3a-qualification-report.md)。四步按条件分支完成：来源与能力调查、零真实调用定向回归及最小决策已交付；stable证据不足，Host修改前提不成立，真实草案仍NOT QUALIFIED。未改Runtime/Host或扩大到B3B；报告后停止。
