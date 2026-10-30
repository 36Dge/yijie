# FEAT-162 条件路由、产物收集与缓存修复结果

2026-10-30。按35号实施前复审和Owner授权完成。本轮 App 构建/启动 0、worker 重编 0、adapter 重编 0、供应商调用 0、收费 0；没有创建新的 App generation 或生产缓存目录。未推送。旧 E1 FAIL、E2—E7 NOT RUN、D4 未通过保持。

## 实现事实

- Host 在 Native submission 校验、引用匹配及 worker prepare 成功之后，对 K3.1 + kimi-web 设置原生 `web_search=disabled`。固定 Runtime 实际请求证明三个 MCP 工具仍在、tool_choice 为 auto。未选/清空/切模型恢复原配置；专家隔离与授权失败关闭保持。没有 Runtime 核心修改或额外分类调用。
- adapter 改用本次成功 Cargo JSON 的唯一匹配 executable，编译失败/缺失/歧义不回退旧目录。复制后校验摘要并记录来源。Host 来源锁覆盖新增收集脚本，新 generation 回执覆盖该收集记录且要求源文件位于当代 target。
- Desktop primary 新 descriptor v2 冻结缓存身份及三个组件目录。使用 `CARGO_BUILD_BUILD_DIR`，最终 target/bin/worker/App/receipt/activation 独立。身份含工作区、实际工具链、SDK、profile/features、锁文件和 Cargo 配置摘要，不含 Git HEAD/generation；Cargo 自行判断增量。v1 保持可读，未迁移08/09。
- 缓存全程普通互斥；最多2个身份桶，构建前逻辑大小64 GiB阈值和至少12 GiB可用空间检查，超过即停止并报告，不自动删除。此为启动前检查，不能宣称运行中空间硬上界。新缓存首轮仍可能冷编译；不搬运旧08/09缓存。
- worker 新增 `--check-only`，把固定源/生成物检查前置。Host/Contracts/资源/Runtime及来源锁门禁全部先于 worker/Host/App 编译；原构建前后摘要检查保留。primary 先检查 Cargo支持及 Go版本，避免 worker 编完才发现 Host 工具链不满足。

## 零费用验证

| 检查 | 结果与实际边界 |
|---|---|
| Host 路由2项 | PASS；9种模型/服务组合；固定r5 + 正规09 worker，6个场景真实loopback请求，三工具发现，新建/恢复/清空/重选/切模型/返回Kimi；使用新operation的失效revision准备被拒绝 |
| Host普通/专家回归4项 | PASS；普通图文、标题、草稿、专家、本地正常读取及continuation共6个loopback请求；三项专家纯配置测试 |
| Session4项 | PASS；新会话/重放/续轮/清模型，撤权，截止预算，正常预取消不进入Runtime |
| adapter4项 | PASS；成功/缓存命中消息、错误/缺失/歧义关闭、普通非可执行数据复制及摘要；未运行替代程序，未实际重编adapter |
| 缓存/descriptor25项 | PASS；组件隔离、不同最终目录、身份变更、普通锁竞争、空间/容量预检、v1/v2读兼容、先检查后编译、保留旧generation、失败不dispatch；App调用均mock且未发生 |
| observation5项 | PASS；保留09新增的显式观察模式和本机计量器启动保护 |
| Desktop脚本64项 | PASS，1项旧专家实际来源资格用例未启用；未运行App |
| 微型标准Cargo库实验 | PASS；离线第一次 fresh=false，保持同一中间目录、切换最终目录后 fresh=true，两个最终rlib均存在；改源码第三次重编fresh=false，前两代最终文件SHA256保持。仅验证稳定Cargo机制，不冒充实际App温缓存或耗时证据 |
| 工具链只读预检 | 默认Go低于go.mod要求，被编译前拒绝；使用机器上已有Go1.26.5后PASS。Cargo/Rust1.95支持所选机制；未安装工具链 |
| 来源/静态 | Host `make lint`、Desktop四脚本ESLint、Shell/Python语法、worker `--check-only`、两消费者FEAT162契约投影、native已提交来源、Kimi完整候选来源、六仓clean source_facts均PASS |
| 元仓治理 | lint、57项测试、严格D0 PASS；不是D4 |
| 保护核对 | 541800个文件/目录清单及大小/权限/mtime/inode一致，其中382285个文件另校验SHA256；08/09、真实验收目录、清理证据全部一致 |

成功路由验证初跑与最后一次增强失效revision验证各6次，加普通回归6次，本轮累计18次本机模拟Responses；供应商模型/REST均0。本轮私有日志在 `.local/feat162-route-cache-20261030/`，脱敏结果及日志摘要见 [evidence/route-cache-checks-20261030.json](evidence/route-cache-checks-20261030.json)。

初次检查中的问题如实保留：新测试缺少临时Runtime Home、未提供模型effort，均在发送模型请求前失败，修正测试装配后通过；缓存继承测试缺少明确临时根，补齐普通临时根后通过；首个Vitest命令误匹配历史.local副本且macOS临时路径含别名，按现有仓库规范排除历史副本并指定规范临时根后通过；Connectors新提交导致精确目录pin过期，经canonical同步后通过。未通过改产品断言、改历史证据或重建App处理这些问题。

## 本地源码闭合

沿用Owner先前“允许仅本地提交FEAT-162”的授权，按生产者→消费者固化必要来源，没有推送：

| 仓库 | commit |
|---|---|
| Host | `ffdb3e66f292339fabccea6b1018bed6bba9c3b8` |
| Connectors | `7f42cd9d775777abe59ac7cdc17d3fe15261ffc6` |
| Desktop | `fd105a952479c33ffd55d5e71b569117171b7216` |

Contracts `d191ad6ed08f0e8cc89dfea1346b5ecdf010e776`、Skills、Runtime均未改变。Host构建pin由 `kimi-k31-build-candidate.mjs --freeze-commit` 生成；目录pin由 `feat164-market-catalog.mjs` 从真实提交生成，目录内容摘要未变。没有手改生成摘要、绑定或旧回执。

费用规则不变：20元软停止阈值，允许在途超过后停止，不要求硬费用上界；本轮执行暂停来自Owner明确指令。既有3次模型/0REST/3元unknown估算和旧42.710457元独立预占均原样保留，不清零、不认为已知账单。继续真实执行仍须新的准确App及同源资格；08/09不能承载本次源码修改。
