# 执行循环修复：原生预算复用与本机接入

2026-11-03。Owner 要求再次复审方案，明确已有 Codex 机制必须复用，并授权实施；随后明确允许本次修复及 canonical 引用的本地提交，不推送、不打 tag。Owner 已通过正常入口退出旧客户端。

`contract-impact = semantic`。普通聊天执行与终态行为调整，app-server 的 269 份 schema、权限、审批、模型、历史格式和上游版本保持。连接器仅通过已有兼容 wrapper 清单新增同一库树的精确来源，目录也仅更新不可变来源引用。

## 复审结论与更正

前序审计遗漏了 `features.rollout_budget`，另建消费计数器的建议撤回。实现使用原生：

- `auto_compact_token_limit`：上下文压缩；
- `features.token_budget`：上下文提醒；
- `features.rollout_budget`：根线程驻留会话树共享加权用量、提醒和 `SessionBudgetExceeded`；
- `goal.token_budget`：用户显式目标的原生预算；普通问题不自动创建 Goal；
- `UpdatePlanArgs` / `PlanHandler`、既有 `answer_completion` / 工具过滤 / 原生失败与取消。

预算相关五个原生实现文件在构建树与固定源码逐字节相同。Host 没有额外用量账本、重试循环或命令去重引擎。原生预算默认口径为未缓存输入加输出，响应 usage 结算时检查，不是人民币封顶或跨重载永久额度。

## 已实现

1. 在原生计划处理成功后，连续相同的计划步骤／状态达到三次时，进入已有最多两次无工具补答。explanation 与搜索事件 ID 不算计划推进；其它工具工作清除这个窄判定，一般循环由原生预算兜底。不全局禁用合法 `pwd/true`，不静默返回伪造的旧结果。
2. 普通受管聊天直接配置 `rollout_budget`：limit=250000，权重各 1，剩余 125000/50000/25000 时由原生提醒。专家与 input-only 草案不强加普通默认；已有明确传入的 native override 保持。
3. 普通业务指令仅放 developer，base 保持简短。专家保留原完整系统基线与 role/index 的优先级。Kimi 提示按实际工具暴露说明 hosted search 不等价于可调用的 query/open/find；已选 Search Pro/Fetch 路由和审批保持，不自动修改选集。
4. Desktop 只展示已有原生预算错误及失败事实；只有已观察到 failed 终态才显示预算停止原因，不创建新的执行或计数逻辑。

## 验证

- 新 Runtime canonical 重放、7 项核心测试、定向 Clippy、release build 通过；schema 与上一受审产物逐字节相同。
- 新产物／正式 Host 适配器的普通回环：重复计划三次后第四次工具为空（包括 hosted search）；有答案共四次 completed，无答案共五次 failed。原七类补答、短答、只要计划、补答期间拒绝工具场景通过。
- 原生预算回环：缓存读取不计入原生 weighted 口径；两个用户轮共享用量，耗尽进入原生 failed；实际普通业务指令一份。供应商请求为零。
- Host 配置、检索路由和专家基线回归、Go vet 通过；Contracts 模型回归 12 项通过；Desktop 投影测试 16 项、目录来源测试 5 项、TypeScript、定向 ESLint、前端与文档构建通过。
- 启动前完整消费者／Runtime／worker 来源检查通过。启动曾因两个精确来源引用未更新而正常停止：库 wrapper 和目录 checkout；未跳过校验。核对库 tree 和目录 bytes 完全未变后，分别通过既有兼容清单和目录生成器接入。

## 实际接入

固定入口正常启动，Native 增量构建 9.89 秒。Runtime 路径选择 `execution-progress-v1`，实际 SHA-256：

`50d89e152c90e660331326506d372b986acd0279324376cb77385959698219d7`

Host `/readyz` 返回 200 且 Runtime 为 ready。原 5 份 rollout 均可解析，原内容前缀保持；新 task_started=0、新 token_count=0。客户端保持打开。用户原有 49 项 Desktop 工作区改动未混入本次提交。

本地来源：Runtime `55b4e51049d6f4fc0af4b35f12832357f5e4ea06` → Contracts `b51d26063f03f8fdb4109e03ede0738053740ed3` → Host `99d3f6ea192f5c17326283f08c1b86c8526bb96b`；Connectors `203544a9e371916db4928f9771e362f282c5be65`；Desktop `a552532b15c40ec87837b6c9a60048089fd8074b`。无推送、tag、安装包或全量备份。

## 限制与保留

没有新增真实 Kimi 对话或付费效果评测；普通协议样例只证明执行控制，不冒称真实模型回答质量。历史大上下文不删除或自动重写。未执行强杀、二进制伪装、权限破坏或攻击 fixture；未运行含上述历史用例的全仓套件，使用本次相关的正常定向验证。已有 app-server unused_mut、构建 chunk-size 提示不是本次新增问题。

本机完整证据在工作区 `.local/diagnostics/2026-11-03-execution-progress-implementation/`：`native-reuse-proof.json`、`new-runtime-integration.log`、`host-reviewed-regression.log`、`startup-source-preflight.json`、`worker-source-review.json`、`catalog-source-review.json`、`activation-current.log`、`activation-verification.json`。前两次启动失败事实保持，最终成功不覆盖原记录。
