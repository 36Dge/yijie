# FEAT-162 路由与构建修复实施前复审

2026-10-30，Asia/Shanghai。Owner 已接受上一轮根因审计方案，并要求先复审再实施：同步需求/验收，修复 Host 条件路由、artifact adapter 收集及缓存复用，零费用验证后复审。明确不构建 App、不收费，保留第 08、09 代和全部历史证据。本轮不改变旧账本、授权 JSON 或验收结果。

## 事实、原因与限制

第 07、08 代相同 E1 输入均声明 hosted `web_search` 和三项 Kimi MCP 工具。第 08 代实际请求已包含新的 connector 优先指令，仍出现 `web_search_call`；不是指令没有进入产物。[Kimi Responses 官方说明](https://platform.kimi.com/docs/api/responses)将 hosted web_search 定义为服务端按输入先检索、再注入模型上下文。仅改自然语言指令无法关闭该请求层能力。事件只证明观察到 native search item，不证明已完成或账单金额；第 06 代首因仍未知。

Host adapter 脚本继承新 `CARGO_TARGET_DIR` 编译，却固定复制 `artifact-mcp/target/debug`。08/09 收集文件摘要为 `82f6d2ee3e3769897412b8ebcf432327816ce7bfecbb03a51ac671dc04914249`，当代 target 产物为 `f537dd882c08d5db73afc56edc6e95e2164c5e9a81e7fc7d3b5de9b487115d51`。证明来源收集错误，不据此推断其业务行为不同。

每代独立 target 导致中间依赖重复编译。已安装 Cargo/Rust 1.95 支持稳定的 [build.build-dir](https://doc.rust-lang.org/cargo/reference/config.html#buildbuild-dir)。采用该配置分离中间缓存和最终 target；不用 nightly、不复制旧 deps、不绕过 Cargo 或来源校验。

## 决策与契约

本轮 `contract-impact=semantic`：改变 Runtime 原生配置及私有跨仓构建环境语义；FEAT-162 总体仍 breaking。公共 Host/MCP DTO、工具 schema、数据格式不变，Contracts 新版本/生成 N/A；既有固定 Runtime r5 和 Contracts 权威来源继续适用。Owner 本轮确认覆盖三个受影响消费者；不是独立人工代码审查或发布批准。

1. Host 只在有效 K3.1 模型 intent、授权 Services 与 snapshot 引用一致、worker prepare 成功且包含 `kimi-web` 时设置 `web_search=disabled`。三个 MCP 工具、auto tool choice、批准链保持。其他连接器不会触发此条件。清空选择/切模型/普通恢复不保留覆盖，按原 cwd 配置恢复；专家最后覆盖继续禁用。失效授权拒绝发送，不降级为原生搜索。
2. adapter 使用本次成功 Cargo JSON 的唯一匹配 `compiler-artifact.executable` 收集，并校验 manifest/bin 身份、普通文件和输出摘要。编译失败、缺失/歧义产物不回退旧路径。
3. 新 generation descriptor v2 冻结缓存身份和环境；v1 reader 保持，08/09 不迁移。Desktop、worker、adapter 独立中间目录；最终 target、worker 内容寻址产物、App、回执及 activation 仍逐代独立。身份包含规范工作区、工具链、SDK、目标、profile/features/flags、依赖锁，不包含 generation/Git HEAD。仅原生 Cargo 决定增量有效性。
4. 缓存目录有限额、构建互斥和可用空间预检；超限停止并报告，不自动清理。缓存不是来源权威，也不成为已构建 App 重开的依赖。旧 08/09 缓存不移入、不改写。所有现有 source/generated/版本检查移至编译前，构建前后摘要及最终精确产物校验继续执行。

## 验收规则修订

“保留原生搜索”明确为未选 Kimi 连接器时保持普通能力；选中且授权有效的 K3.1 普通对话由正常产品 Host 关闭 hosted 搜索。验收代理仍逐字节转发该正常产品请求，不得临时删除工具或改输入。E1—E7 原冻结输入、期望工具和次数不变；旧 FAIL 不改判。

零费用补充检查：R1 模型×服务×选集矩阵；R2 固定 Runtime 新建/恢复/清空选择的真实 loopback 请求及三工具发现、专家隔离；R3 失效准备不发 turn；B1 Cargo 产物选择/失败关闭；B2 缓存身份、分组件环境、并发/容量普通预检、v1 兼容、全 preflight 顺序；B3 标准微型 Cargo 工程验证中间复用和独立最终输出（不构建 App/worker/adapter）；P1 08/09 与历史证据清单、元数据和关键摘要前后比对。

执行顺序：本需求/验收权威文本 → Host → adapter/worker 构建接口 → Desktop 缓存与前置检查 → 零费用定向检查 → 分离复审。来源冻结/生成 pin 必须走 canonical 流程，不能手改 hash。此轮只产生本地候选；新准确 App、E1—E7 和 D4 均待后续授权，不以 loopback 或缓存实验代替。

回滚按消费者优先：恢复旧 canonical 脚本和 Host 源码；v1 产物原样保留，v2 需要其匹配 reader。缓存可弃用但本轮不删除。保持历史读能力、原数据和账本。禁止强杀、替换受保护二进制、权限故障和攻击性 fixture；不能安全执行的历史测试记 NOT RUN 及影响。
