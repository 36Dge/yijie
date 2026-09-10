# FEAT-144 原生产品接入实施记录

2026-09-10。用户已明确执行完整七步计划，包含最小源契约、兼容reader和前向格式保护、Host原生薄适配与Desktop展示。此次产品实现/新增前向migration已授权；本地提交、模型预算及推送仍独立授权。AC-004维持OWNER_EXCLUDED/NOT RUN，活动9项AC不提前标PASS。

## 实施依据修正

1. 真实秘密入口：已在现有canonical脚本增加显式本地配置 `YIJIE_DEMO_FAST_SORFTIME_ENABLED=true pnpm tauri:demo-fast:app`；构建完成后使用macOS隐藏输入框，取消只关闭Sorftime。尚未真实启动此入口。秘密只进入本次启动进程内存和受管Desktop→Host→Runtime环境白名单；不进入WebView、argv、文件、TOML、日志或数据库，不新增凭据存储。正常退出清理，重开重新输入。原生shell_environment_policy.exclude排除该变量，同时验证set不重注入。秘密由Desktop一次性交给Host后清除保留副本；当前为已实现但尚待canonical验证的新适配。
2. 权限生效：首期仅请求批准/on-request/user/workspaceWrite且网络默认关闭；原生Prompt真实参数确认，不猜Item绑定。显式使用现有稳定tool_call_mcp_elicitation=true；Prompt不提供记住批准的persist选项，未支持的元数据拒绝，不自行解析为新审批政策。模式变化前先让相关Turn正常结束；原生reload返回只算已排队，不算失效。实现选用受管Runtime正常退出并以禁用Sorftime配置重启。先检查已有活跃Turn/待决审批，随后逐个读取当前Runtime实际加载线程的原生idle状态；请求启动与停用共用操作互斥。必须确认进程退出、transport清理、原有来源检查后的重启及新配置不再启用MCP，再允许界面保存新模式。返回请求批准不自动重新连接。不强杀，不自动切换用户权限，不恢复FEAT-137。
3. canonical范围：普通入口保留已有图片工具及其experimentalApi=true；FEAT-144只使用固定Runtime稳定MCP方法，不新增实验能力。稳定诊断的experimentalApi=false与普通产品入口分别记录，不擅自关闭图片能力凑验收。
4. 兼容reader先于writer：新原生展示版本与前向持久格式标记严格分开；recordDiagnostics只在Desktop私有读取/worker/IPC/前端流转，不放入Codex事实。未知view格式既不冷读补建，也不让active stream当作无记录重新建buffer。facts只保存格式标记，不新增fact replay reader。
5. 显示容量：在唯一NativeDisplayBuffer中保留新完整Item的原生身份/状态；内容超限明确省略，不恢复旧Item及旧生命周期，不新增累积器。
6. 额度：元数据8/10、业务0/10（含原生重发）、模型/图片0。S01的原生诊断引用已有7/8证据，不重复试连；产品必须的初始化/发现/重开单独记账，超出现有余量则停止该真实步骤。无需再补业务失败依据、重新申请同范围业务预算或等待扣费公式。

7. 网络：沿用系统当前HTTPS代理，不把诊断机地址固定为默认；canonical显式读取系统配置，只支持无鉴权HTTP CONNECT代理或直接连接，PAC/SOCKS未验证时停止该入口。Desktop白名单传给Host，Runtime复用现有HTTPS_PROXY支持，并保持MiniMax与loopback直连；不建代理、不改系统网络、不关闭TLS。
8. 实际注册：Thread原生startupStatus必须为ready。首次业务Turn之前另做一次原生mcpServerStatus/list（toolsAndAuthOnly），确认bearerToken、唯一product_detail和与操作8一致的inputSchema；失败不由外层重试重新发现。工具schema本身存入源契约兼容资料并同源同步，缺失outputSchema/annotations/progress不补造。

## 实施顺序与状态

- 依据修正与D0：前置重跑已PASS；本轮最终文档同步后还将重新运行。
- 最小版本化源契约：已实现native v2/SSE v8及MCP审批v2；旧源版本保持原样。候选生成、类型与三组历史baseline的兼容检查通过。修正breaking脚本临时目录的相对引用解析，不跳过旧规范。
- 兼容reader：已实现schema15前向迁移、facts/views格式标记、独立recordDiagnostics及worker/IPC/前端传递；旧JSON不改写，未知格式不能补建或开启活跃缓冲。writer=1候选已单独保存为Git blob清单，尚无真实reader提交。
- Host：原生配置、实际参数Prompt、原生文本块、旧v7出口、正常停用流程已实现。固定0.144.6的本地features list已成功解析相同配置；未带凭据、没有MCP连接或模型调用。真实激活/停用仍待D4。
- Desktop：新增Native Tool卡片、移除新链路旧DTO伪填、保留原生索引和空/缺失/容量状态、修复容量回退及历史忙碌。兼容旧Tool读取保留。当前writer=2只在候选代码中，canonical来源门禁仍阻止未固定来源启动。
- 提交、canonical与D4：未开始；提交和模型预算仍待本次明确授权。活动9项AC保持pending，AC-004始终用户排除。

原配置、正常终态、权限、来源和SQLCipher机制继续复用。不会实现业务失败分支/专用错误字段，不新增MCP客户端、桥接器、状态推演、正文对账、历史重建或自动封口。旧v7/v1与旧权限端点保持各自语义，新消费者明确选择新版本。


## 真实验证的最小编排

一次启用Sorftime的验证线程：原生初始化占剩余额度第9次；首次发送前的原生目录核验占第10次。随后同一线程验证一次真实详情成功及一次原生Prompt正常拒绝（拒绝不消费业务调用）。每次逻辑业务操作先保守预留2次tools/call尝试，包含原生404恢复重发，不加外层重试。模型预算另行授权，并复用现有计数代理记录所有模型请求；不授权图片。

验证权限模式切换时先结束活跃Turn；Sorftime停用后不自动重连。普通退出重开时不再次输入Sorftime密钥，只读取已有原生加密事实、旧历史、附件/Artifact/Command及权限入口，因此不需要第三次元数据初始化。若真实过程需要更多元数据操作，停止对应真实步骤，不转用业务额度。

提交候选顺序为Contracts→Host→Desktop兼容reader→Desktop最终展示/writer→元仓。Host新出口和旧出口共用事件缓冲；新持久格式只在最终Desktop writer启用。reader候选在Host产品编写前已保存，提交时使用真实Contracts/Host来源锁替换候选来源清单，保留其writer=1。回滚只到该已提交并验证的兼容reader；它保证格式识别和旧JSON保留，不承诺最终Native Tool界面的全部功能。


当前进度以[18：来源固定与真实验收](18-committed-sources-and-d4-2026-09-10.md)为准：Contracts、Host、Desktop reader及最终writer已本地提交，真实来源锁已固定；本次模型预算0/8已授权，业务0/10、元数据8/10、图片0。此前“等待提交/模型授权”仅为历史阶段状态，canonical及D4仍未完成。
