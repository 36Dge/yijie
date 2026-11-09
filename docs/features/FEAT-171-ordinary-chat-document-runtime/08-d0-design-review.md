# FEAT-171 D0 分离架构复审

2026-11-09。审查对象为00/02/05、ADR-0024及相关现有源码。本页记录审查时发现与明确修订建议，供主方案收敛；不能单独视为产品实现、人工批准或D0通过。未修改产品代码、安装依赖、启动程序或执行故障/攻击验证。

## 1. 审查结论

原稿的产品目标、原生复用原则和依赖隔离方向正确，但“原生中断即正常退出”“staged之后模型即可确认聊天就绪”“历史版本永久可读”不能从现有代码推出。内置指南的承载、默认入口与版本身份也需要固定到可实现的路径。以下采用单一路线，源契约及实现仍由后续批准工作完成。

## 2. 应落实的设计收敛

| ID | 问题与现有证据 | 收敛方案 | 对D0/实施的影响 |
|---|---|---|---|
| AR-01 | `artifact-mcp/src/main.rs:56`目前只有publish_artifact，`internal/codex/artifact_media.go:18`负责内置MCP配置；原稿“通过原生工具/资源发现”没有具体承载 | 复用现有Host-owned artifact MCP，新增只读 `load_document_environment` 设计工具。其说明覆盖九格式与何时调用；返回经验证的bundle_id、专用Python及CLI绝对路径、指南路径、支持矩阵与限额。指南/模板/CLI源由Desktop内置资源包拥有，不注册现有市场Skill或依赖其安装目录 | 新工具先进入Contracts源；不新增MCP进程、Connector选择项或Host关键词路由。仅普通根会话，标题/草案/原子辅助会话不开放 |
| AR-02 | Code Mode本身无Node/FS/network；原生exec已可执行固定路径。把“通用文档执行”再做Host服务会复制核心机制 | 新文档CLI是普通应用资源程序，固定解析同bundle解释器、库和转换器；模型经现有exec调用。load_document_environment不执行转换、shell或用户代码。无专用Node/PptxGenJS/Poppler新增链，使用06冻结的Python单栈＋LibreOffice＋现有Quartz | 固定入口与真实子进程来源须验证；一般exec不被全局PATH劫持。指南不是权限边界 |
| AR-03 | `internal/session/artifact_media.go:254`返回staged；Native `artifact.rs:523`先提交再ACK；`internal/artifact/store.go:263`ACK按大小/摘要确认后清理spool | 既有publish返回语义保持；同一adapter新增只读 `get_artifact_status` 设计工具，只查询当前Host generation中同会话artifact的登记/ACK事实。只有匹配ACK已观察到时可返回`committed`；`staged`、失败、过期、unknown如实返回。Host重启无记录必须unknown，不能重登记或重新生成来“找回成功” | 不新建持久状态ledger。Native重开仍读自身已提交原件；最终模型没有confirmed就绪事实时只能说文件已生成/已登记，UI可独立显示其真实持久化状态 |
| AR-04 | `chat_output_artifacts`已保存artifact_id、session/turn、sha256；不同内容重复同路径被Host拒绝。原稿把数据库expand保留为悬而未决 | 首期用现有不可变artifact身份作为版本，文件路径每次修改唯一。每一版独立产物卡片；用户指向明确版本，旧卡片不偷偷指新字节。不引入版本树、自动latest指针或第二执行ledger。任务receipt记录bundle/操作/结构与QA覆盖，但不代替Native身份和授权 | 首期数据库默认none；若实现发现必须新增持久字段，另回源契约评审，不预设迁移。禁止依赖模型提供parent_id自证归属 |
| AR-05 | Native `src-tauri/src/chat/artifact.rs:21`保留时间是7天，`:1435`按提交时间计算到期；Host spool是进程暂存和24h TTL | 旧版本可追溯与重开承诺限定于既有7天有效期。到期显示原有过期事实，不静默重建。用户已另存的外部文件独立存续；重要文档引导另存，不承诺聊天产物永久保留 | 安装升级和重开测试必须覆盖“有效原件保持”“到期可解释”，不将7天行为写成数据丢失缺陷或无限存储 |
| AR-06 | 日常`development-client.py:157`先确保workflow服务；这不是独立安装产品入口 | 安装候选直接携带前端、Native、Host、Runtime与文档资源，不执行源码构建或要求Docker；普通聊天/文档readiness与工作流/连接器readiness分离。工作流不可用仅影响对应入口，不新增“文档模式” | 保持local direct-entry固定scope，不以此改变公开生产认证。正式分发、签名与真实后端资格仍独立 |
| AR-07 | openpyxl并非公式计算器；重算或修改可能改写未知OOXML对象，原稿对任意旧件容易过度承诺 | 新建和可支持基线文件走冻结Python库；XLSX在独立工作副本中经LibreOffice计算，再核对公式文本、工作表/图表、类型和独立预期值，以该最终文件做预览/交付。原件保留；不支持的外链、宏、迭代或复杂对象只读，不承诺有损往返 | 不用data_only读取后覆盖原件，不手造缓存宣称已计算。PPTX保持同样的支持集/关系检查，新增内容可编辑不等于任意原件全保真 |

## 3. 正常取消必须覆盖真实原生生命周期

### 已证实的缺口

- `yijie-codex/codex-rs/core/src/session/handlers.rs:63` 的turn中断调用`interrupt_task`，不应直接断言它一定强杀，也不能据此证明所有后台进程已正常结束。
- `core/src/unified_exec/process_manager.rs:1374` 的`terminate_all_processes`会drain拥有表并调用terminate；`:1411`的单进程终止、淘汰等路径同样可能进入terminate。
- `core/src/unified_exec/process.rs:208`传给PTY/exec-server终止；`:614`的Drop调用terminate。`utils/pty/src/process.rs:241`及Drop继续调用kill；`utils/pty/src/process_group.rs:165`在Unix发送SIGKILL。
- `core/src/session/handlers.rs:600`关闭会话时进入全部进程终止。因此只改变GUI停止按钮或“发一次SIGINT后照常退出”不足以守住用户禁止强杀的边界。

### 冻结的单一路线

复用原生UnifiedExecManager/ProcessStore，设计一个**通用、受管、协作退出策略**，暂称`cooperative_only`（拟新增配置，不是现有字段）。它不含Word/PDF业务逻辑、不创建Host执行器。由FEAT-171受管普通会话配置启用，作用于该profile创建的原生exec进程；不得通过模型可控命令字符串推测哪个PID属于“文档进程”。其他未启用profile行为保持。

1. Runtime原有执行/审批链负责启动和所有权。文档CLI使用已审包内解释器，在原工作区及允许临时目录运行；转换操作维持独立profile和输出路径。
2. 取消停止模型后续派发、关闭新的文档写入准入，然后由原生已有signal能力发协作中断/关闭输入；CLI在安全步骤边界停止写入，并调用转换器自身正常退出流程。支持SIGINT不是任意引擎均可安全退出的证明，需要正常样本资格化。
3. 软截止只返回“仍在收尾/StopPending”的操作事实，不升级SIGKILL。ProcessStore继续持有活进程句柄，退出观察和输出排空继续工作；不能drain最后一个Arc触发Drop终止，也不以取消Future当作进程结束。
4. 对该策略覆盖全部会走终止的相关入口：显式中断后的清理、后台进程清理、会话关闭、过期/容量淘汰、错误收尾以及Drop前的所有权处置。满额时拒绝新任务，不驱逐尚未正常退出的进程。
5. 进程正常结束后才登记退出、释放句柄和清理临时配置。若无法安全结束，停止后续步骤、保留所有权并报告；App正常退出/版本升级应等待此事实，不先关闭Runtime或删除在用bundle。不能伪报应用已退出。
6. 这构成一个需要Runtime候选和canonical config/schema投影的最小增量；只改当前固定上游的独立补丁/构建工作区，保留旧binary。先原生候选→Contracts投影→Host配对→Desktop收尾事实展示，不反向发明Runtime协议。

该策略是本轮设计决定，**未实现、未验证、未授权修改现有二进制**。实现阶段须用能正常协作退出的普通长任务验证中断、保留句柄、正常收尾、关闭/重开。不得用强杀、卡死故障注入、权限破坏或恶意fixture验证。无安全退出证据时不得激活本能力，也不得将“不强杀”写成有硬时限的进程终结保证。

## 4. 验收与批准语义

- D0应检查上述路线已成为主方案、源契约权威与技术限制明确、06依赖来源/许可和07预算已冻结；不要求本轮制造实现binary的digest或伪造clean-install/视觉结果。
- D0材料/机器门禁可通过，不等于Owner已批准技术ADR、产品实施、真实模型额度或签名分发。用户本轮明确“暂不实施产品代码”，implementation/activation授权应继续false。
- T03/T04检查内置环境工具与普通根会话的真实声明；T10增加同generation ACK查询、无ACK及重启unknown；T11增加7天有效/过期语义；T14/T18增加协作退出策略与App收尾的正常样本验证；T17检查实际解释器/包来源；其余原生安全边界保持。
- 参考Codex的产品步骤和结果质量，不复制私有实现，也不把Codex本机加载成功当作易界依赖资格和性能验收。

## 5. 当前处置状态

### 最终限范围复核（2026-11-09）

已复读更新后的00/02/05、feature.yaml、ADR-0024及06/07。本页第2—3节保留初始审查依据；最终设计以05—07为准。工具名统一为`load_document_environment`和`get_artifact_status`，旧建议名不代表新增的第三个工具。

| 复核点 | 当前主方案落实位置 | 本次判断 |
|---|---|---|
| 专用环境与内置指南 | 05第1—2节、06；现artifact MCP只读环境查询、Desktop内置指南、CPython单栈 | 已有具体承载，不注册市场技能，不新增Host通用执行器 |
| Quartz供模型QA使用 | 05第6节；共享现有Native PDF校验/Quartz库，canonical构建随包`yijie-document-render` CLI，由原生exec调用 | 已补实际导出入口；不是声称Python可以直接调用私有预览API。CLI只渲染，模型看图仍为原生view_image |
| 交付事实回传 | 05第3节、02 T10 | 只用同generation匹配ACK确认committed，ACK优先于spool清理，重启unknown不重放；不新增持久ledger |
| 版本与保留期 | 05第3节、scope.database_change=none、02 T11 | 既有artifact_id/session/turn/SHA256为版本身份；7天及另存独立存续明确。committed仅确认曾提交，不表示永久可读 |
| 正常取消与资源拥有权 | 05第5节、07、02 T14/T18；scope.runtime_change=runtime | 覆盖取消/清理/淘汰/shutdown/Drop及exec-server；30秒后STOP_PENDING保有句柄，已从不成立的“现有中断保证正常退出”修正为窄原生适配设计 |
| 平台、依赖与预算 | 06/07、planning.decisions | 单一版本路线和明确预算已写入；源级D0决定与后续构建hash/SBOM/性能实测分离，未借Codex缓存冒充易界制品；02 T17已同步Python单栈 |
| Codex对照与独立可用 | 05第6节、02第4节/T18 | 对照是质量参考，不是用户任务的运行前置；D4有独立内容/对象/公式/视觉判据 |
| 授权及完成声明 | 00第7节、planning、ADR状态 | D0技术材料不等人工签批、产品实施/激活/付费/发行授权；产品AC及T/F仍pending/NOT RUN |

**在本次限定复核范围内，未发现仍未闭环的P1设计问题。** 初始问题已在文档层解决，最终机器检查由主审统一执行。此结论不是实现资格或真实安装、视觉、取消验收。

本次仅修改本页，没有执行产品检查、模型调用、用户数据变更或Git提交；暂不实施产品代码的边界保持。
