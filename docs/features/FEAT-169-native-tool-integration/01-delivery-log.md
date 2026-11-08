# FEAT-169 实施记录

## 起点

2026-11-07，用户在两次源码审计后明确要求实施四组原生工具，V1/V2 统一选择 V2。当前基线：Runtime 7171b0b262c67a72725fa54f9ed39b50edd94b54；Host 435747780feaec2b8e914a97081024dc26730e0c；Contracts c24d73fde83a01b5dd2a9ded8defb5bbef34e311；Desktop b7ce363eb9ac8a37ba0f4fb1a178d392ba106b8c；Connectors de1fcdf8dabd9b08983bbf907f079db41da437fe。

工作区已有治理文档改动及 Desktop 49 条修改，均属于此前工作；本任务不覆盖、不回退、不提交。contract-impact=breaking；本地 demo_fast，不涉及生产发布。

## 已确认工程事实

1. 原生 V2、补丁、Code Mode、记忆工具执行器均已存在。
2. 市场层当前关闭 multi_agent 和 memories；审批按精确原生线程/轮次，不能只翻开关。
3. 旧线程的 MultiAgentVersion 会从原生历史固定，单改模型目录不能确保恢复线程统一 V2。
4. Code Mode 的 custom exec 不满足 Kimi 当前官方接口类型约束，需要薄输入适配。
5. memories 的自动启动管线只检查总开关，须保证本次仅四工具接入时不处理原历史或额外调用模型。
6. 本次付费调用额度为 0。实现和零费用验证先行；未完成真实模型验收不得写 PASS。

## 当前状态

已完成 overlay、受管配置、Contracts 兼容投影、Host 子任务审批归属与 Desktop 展示/入口适配；前两版本地候选保留，第三版已完成 canonical 构建。未激活日常入口，未完成 D4。

修复过程中真实发现并保留记录：JSON 配置整数转 TOML 时曾变为 4.0，导致原生 FeatureToml 拒绝启动，已改为保留整数；V2 不仅依赖命名空间，还默认使用加密工具参数和 agent_message 输入，已补入明确配置的明文消息路径与出站投影。回环接口现在检查外部提供方允许的输入类型，不以“原生进程内部能执行”替代 wire 兼容。

已通过：真实 Runtime 的补丁、四个记忆工具、V8 执行及挂起/等待；4 个定向原生单元用例；前端组件用例与类型检查；Desktop cargo check；Host 定向 vet。V2、恢复/隔离/审批的新版完整联调及定向 race 检查均已通过。所有模型响应均来自普通本地 HTTP，无真实供应商费用。


## 后续授权与入口

用户通过异步答复确认已正常退出，并授权最多 40 次真实模型 HTTP 请求；随后明确收窄为仅验收 Kimi K3.1 Pro，MiniMax 不做真实验收。额度保持总计 40 次，包含 V2 子代理。本次实际请求经 `chat-model-smoke-meter.py --qualify-native-tools` 共享计数，提供方白名单只有 Kimi；无任何 MiniMax 实际请求。

原入口的专家资源检查被此前 Skills AGENTS.md 修改阻止。使用已固定的 Skills 提交创建 detached 资源工作树，仅复制原正规产物并执行原 manifest/authority/每个归档哈希校验；38 Skills + 37 专家保持原值。没有放宽干净源码检查，没有改写用户修改。正常开发入口已完成原有来源检查并启动增量构建。


## 完成结果

Kimi 真实验收全部通过，共 19 次请求，含 V2 子代理，MiniMax 为 0；计量器正常关闭。实际工具输出已离线复核并形成脱敏摘要。正常入口首次发现市场启动校验仍走旧配置，已修正并补入真实 Runtime + canonical worker 启动测试。用户再次正常退出后，原 `pnpm client:dev` 完成增量构建并启动新候选，HTTP /readyz 返回 200 ready。Skills、专家、连接器启动正常。

已检查真实 Vue 组件的亮/暗色和 360px 布局；未伪称 Native 主窗口自动化完整录制。详细分层证据及限制见 02。工作区全部改动保持未提交；用户既有 UI/AGENTS 修改保留。


## 2026-11-08 接入复审

用户要求再次审计四组工具、发现问题直接修复。发现并修复子代理自动审核人工接管的线程归属、角色重载后的父 MCP 约束、函数别名后的 Code Mode 命名空间策略。删除冗余子代理树缓存，继续复用原生执行器和控制面。完整证据及原生冷恢复/不自动重放语义见 03-code-audit.md。

本轮新增付费请求为 0。新候选已构建并通过定向检查，待正常重开激活；没有使用强杀、破坏权限、替换既有二进制或攻击 fixture。

复审激活完成：用户正常退出后从原入口重开，新 Runtime dfa05c… 已实际运行，Host readyz=200 ready。原数据 Home、数据库和历史未重置。Rust 6 个定向用例、Go 19 个顶层定向用例与相关子例、来源/生成/入口准入检查通过；本轮真实付费调用 0。

## 2026-11-08 两组原生工具追加接入完成

用户恢复后完成问答与上下文工具，最终Runtime038d498...；本阶段Kimi4/8次全200、三个原生函数各1次；原 pnpm client:dev 已重开且readyz200，原自动摘要保持。详细实现、来源、失败修复及分层验证边界见[06执行记录](06-user-input-context-execution.md)。不借用前四组D4或旧40次额度，不新增其它工具。
