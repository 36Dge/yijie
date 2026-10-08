> **2026-10-08 13:20 本地 D4 已验收**：Owner明确回复“接受分阶段证据，完成本地 D4（推荐）”。当前49项（淘宝闪购、豆蔻医生已移除），AC-001–010均已通过；采用Tushare原f8构建真实批准/拒绝与最新ea84构建本地回归，保留各自证据，不合称同构建实跑。D4验收未新增模型或服务调用；后续获准的Git交付见[19](19-git-delivery-2026-10-08.md)，未发布。最终记录见[18收尾矩阵](18-closeout-audit-and-acceptance-matrix.md)及[验收证据](evidence/closeout-verification-2026-10-08.json)。以下早期状态均为历史。

> **2026-10-08前序阶段记录（D4确认前）**：Owner已移除淘宝闪购和豆蔻医生，当前49项；Agentic Engine恢复本轮范围，按官方导出的HTTP Header配置。真实验收仅Tushare，其余48项只做代码审计/正常本地测试。Worker56、Native38、前端56、Contracts15项通过；最终49项标准应用已启动并确认两项移除及AE详情。Tushare批准1次HTTP200、拒绝0发送的真实证据固定到f8f85fa4，后续c39ce878仅本地回归，未合称一次fresh run。完整Must矩阵/D4未整体置PASS。当前证据见[17](17-generic-provider-implementation-and-scope.md)、[49项回归](evidence/scope49-local-verification-2026-10-08.json)和[真实调用](evidence/generic-final-acceptance-2026-10-08.json)。

> 2026-10-08 Owner再次明确：真实服务仅验证Tushare，其余50项仅代码审计与适用的无外部调用本地测试。下文设计阶段的“逐服务真实调用/全部真实资格”不再是验收门槛。51项实现范围保持不变；旧诊断不足不阻塞。当前代码缺口见[14](14-completion-audit-2026-10-08.md)，Tushare真实批准/拒绝见[13](13-tushare-real-query-and-permissions.md)。

# FEAT-157 文档验证与未来验收

> **最新验证**：[09](09-broker-control-implementation.md) 已补控制契约18项、Host普通/满容量真实owner、Rust19项及 [实际Runtime→Gateway最终run06](evidence/broker-qualification/run-06/verification.json)。仅本地合成协议资格，真实供应商/产品Must AC和D4继续NOT RUN；旧失败和安全条款要求的跳过项未计PASS。

> **2026-10-07实施更新**：用户已明确“根据需求包与设计包，开始实现feat-157需求，逐步实现”。按包内推荐方案开展本地source-first实现，D0产品方案确认；下文起草阶段的“未确认/只落需求”保留为历史。外部账户、付费调用、Git交付未授权，D4仍未完成。进展见[07实施记录](07-implementation-progress.md)。
> 2026-10-07 · 需求包检查与产品运行验收分开。D0 pending，实施pending，D4 NOT RUN。

## 1. 本轮实际检查

| 检查 | 实际内容 | 结果 |
|---|---|---|
| 来源阅读 | PDF全部9页逐页渲染检查，提取文字；阅读51项MD/CSV、两张补图 | 完成，非产品验收 |
| 数据核对 | 51唯一条目，MD/CSV对应字段一致；类别2/6/2/14/18/9；49HTTP+2stdio | 完成 |
| 授权统计 | 实际44oauth+1gateway-oauth+6none；修正文档摘要45/1/5的矛盾 | 完成 |
| 图标核对 | 51文件，实际44PNG+1JPEG+6SVG；thinkingdata.png格式不符，尺寸非统一240 | 完成 |
| 工程审计 | 当前HEAD/branch/remote/status、实际Composer/提交/历史、Host/Codex/Connectors代码 | 完成，见01/03/04 |
| 公开资料 | MCP授权规范、FTShare、Google包、其余可查维护者说明；未访问业务接口或授权账户 | 完成，见05 |
| 包结构、链接、格式、元仓检查 | 最终命令与退出码记录在evidence/document-checks.json及本页末尾 | PASS（仅文档检查，详见§7） |
| Owner确认 | 候选方案已成文，未收到确认 | pending |

文档检查PASS只证明包结构/数据对应与已执行的本地检查，不证明供应商可用、原生接口资格或安全边界已批准。不会为通过D0机器检查把product_ux.status伪填PASS。

## 2. 未来验收计划

| ID / AC | 正常操作/前置条件 | 可判定结果与证据 |
|---|---|---|
| T01 / 001 | canonical进入连接器，切tab、筛选、搜索不存在名称、清空搜索；对照catalog51 | 六分类精确51；状态计数正确；没有自定义入口；每图标实际可渲染；目录失败/无权有出口 |
| T02 / 002 | 点卡片/加号；安装同一应用、普通重复点击、退出正常重开 | 只有一份安装；默认关闭；无OAuth/业务/npx隐式执行；成功状态权威一致 |
| T03 / 003 | 每类服务合法配置；合法OAuth同意、用户拒绝/取消；正常重新授权 | attempt/scope/连接generation匹配；授权/持久化/初始化/工具目录分别记录；迟到完成不会反启用 |
| T04 / 004 | 详情/已安装/聊天启停；已选草稿中停用；正常运行时请求停用；卸载确认与取消 | 三处一致；禁止新调用，在途真实；原有历史不删；清理未完成可重试；不强杀 |
| T05 / 005 | 新任务和已有聊天中多选/去重/移除；新任务选择MiniMax及非默认工作空间，进入管理再返回；输入中文/附件/按Esc | 正文、附件、选集、模型不丢；标签在输入区；空文本仅标签不可发；只durable acceptance清草稿 |
| T06 / 006 | 正常两个会话A/B使用不同合法选集；服务停用后再次请求；用户原生拒绝工具 | Gateway校验可信binding而非prompt/metadata；未选应用不执行；审批展示可信工具/参数且拒绝不调用；真实token不进模型/Runtime/日志 |
| T07 / 007 | 旧历史、新快照、模型submit分支、正常重开、查询原operation | reader兼容；名称snapshot保留；同请求同选集；新请求新ID；旧记录不回填；计划input-only不引入连接器 |
| T08 / 008 | 正常缺配置→补齐→显式重试；供应商文档化错误用声明式普通返回；授权过期状态 | 保留草稿；错误安全可理解；可恢复而不循环；未知写入不自动重发；不可用不假绿 |
| T09 / 009 | 亮/暗1180×760与常用窗口；200%缩放；长名称；全键盘操作 | 无遮挡，popover有界滚动，hover操作focus可达；焦点回触发器；IME/Enter无误提交 |
| T10 / 010 | 同一最终候选canonical启动和整体验收；逐服务资格按下表记录 | Must全部满足及原生截图/请求ID/来源版本；51项各项有证据；无阻断不能冒称全部接入 |

T06的权限校验采用代码审查、合法scope状态组合与普通声明式验证，不构造攻击请求或恶意fixture。限流/超时等可用正常声明式返回做单测；未获准外部真实失败不通过故障注入制造。不得用取消/空结果冒充某个供应商真实业务失败已测。

## 3. 逐服务验证账本格式

sources/catalog-51.json固定全部外部verification为NOT RUN。51服务目标不等于自动开放供应商所有工具；每服务的支持工具集、必需用例与排除项须由Owner确认，未确认保持待定，不凭一次只读样例声称全功能。实施时另建资格证据，不覆盖来源值：

| 字段 | 记录要求 |
|---|---|
| service_id/source_revision | 稳定ID、参考来源sha、实际经确认endpoint版本，不输出secret |
| provenance | Contracts/Host/Desktop/Broker/Runtime和本地包精确来源；所需本地构建digest |
| auth | 认证策略、credentialRef（不含值）、批准scope摘要、回调类型、取消与恢复结论 |
| metadata | initialize协议版本、tools/list分页完整性、工具数/schema digest、风险映射、更新时间；支持/必需/排除工具及Owner确认 |
| safe_business | 经批准工具、参数范围、外部副作用与额度、脱敏结果/时间；缺少安全读工具则明确blocked |
| lifecycle | 停用再启用、正常重开/stdio EOF退出、卸载清理结果；不从截图推断 |
| result | PASS/FAIL/BLOCKED/NOT RUN及对应证据；卡片存在不允许标PASS |

浏览器示意、纯mock或共享框架单测不是逐服务联通证据；真实业务验证要限定不含商家/个人敏感信息的目标。需要真实个人日历、医疗、商家账号等时先明确数据与调用范围，不复用其它需求批准。

## 4. 契约、数据与本地资格

- 源先行：Contracts新管理/提交/历史/错误/能力字段与版本；按新请求provider-first、新响应reader-first；适用generate/lint/focused conformance。
- Fixed Runtime：公开MCP方法/notifications按固定canonical投影；已加载thread忽略config、重载异步、审批关联不足分别验明，不冒造mcp scope API。
- 无凭据/模型资格：正常本地MCP服务使用合法静态schema/无敏感数据，进行initialize/tools/list/正常退出；不替换任何可执行文件。
- 持久化：隔离可复现普通数据验证expand migration、新旧reader、accepted快照/outbox原子性；不复制用户日常数据库，不降库、不破坏权限。
- 生命周期：应用自身退出/正常stop、stdio EOF和受支持正常清理；无法退出即报告并停止该步，不以kill -9/故障式强杀验收。
- 既有回归：普通无连接器对话、Kimi/MiniMax分支、FEAT-152权限、FEAT-144限定Sorftime、FEAT-155计划input-only、附件/Artifact/历史。不继承旧结果作为本次PASS。

## 5. 本轮未执行项、原因与影响

| 未执行项 | 原因 | 影响 |
|---|---|---|
| 产品实现、跨仓契约生成、DB migration | 当前交付需求候选，尚未进入实施 | 不能声明代码完成 |
| OAuth/令牌配置/外部MCP发现和调用 | 缺供应商资格、真实配置及明确调用额度 | 51项真实兼容全部NOT RUN |
| 模型调用/原生真实主路径 | 本轮无对应授权/实现 | D4未运行 |
| 新Keyring/本地Broker/Google包运行 | 依赖与安全边界为候选，未安装运行 | 不证明credential持久或stdio正常退出可用 |
| 强杀、可执行文件替换、权限故障、攻击fixture | 用户长期硬性禁止 | 改用正常验证；无法覆盖的异常不伪造PASS |
| 真实高风险写操作与生产发布 | 未授权，非本轮范围 | 不证明商家写入/生产可用 |
| Git提交、推送、tag | 未明确要求 | 仅工作区文档，无远端交付 |

## 6. 结论

需求与设计可供评审；产品AC-001至AC-010全部pending。D0 pending（候选决策与外部依赖尚未确认），D4 NOT RUN，DP N/A。文档质量检查的命令证据另记，不改变这些门禁。


## 7. 最终文档检查回执

2026-10-07实际运行，完整输出见 [document-checks.json](evidence/document-checks.json)，数据/链接/工作区复核见 [static-review.json](evidence/static-review.json)。

| Command / 检查 | Exit | 实际结论 |
|---|---:|---|
| ./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh docs/features/FEAT-157-desktop-market-connectors | 0 | schema v3结构/模板替换有效；未指定D0/D4 |
| node docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs --audit-claims docs/features/FEAT-157-desktop-market-connectors | 0 | 声明与机器状态有效；没有声称产品PASS |
| pnpm lint（元仓） | 0 | 11仓清单、中央Contract First及11兄弟仓规则检查通过 |
| pnpm test（元仓） | 0 | 50 tests通过，0失败；这是元仓治理测试，不是产品或跨仓全量测试 |
| bash -n scripts/*.sh（元仓） | 0 | shell语法通过 |
| 51源条目逐字比对、51资产sha256、Markdown相对链接/占位/尾空格 | 0 | 完整一致，无失效相对链接 |
| git diff --check及8仓HEAD/7兄弟仓status核对 | 0 | 仅元仓新需求目录；兄弟仓状态与初始快照一致 |

交叉审查修正了五项：管理往返模型/工作空间意图保留；51服务与经审核工具子集的完成口径；Calendar独立token存储；当前五patchRuntime来源；非秘密安装产品状态复用Native SQLCipher，并补齐权限/provider及revision回执。

结果：需求包文档检查通过；D0仍pending、产品AC全pending、实施pending、D4 NOT RUN。没有把治理单测/来源哈希当成MCP真实接入证据。
