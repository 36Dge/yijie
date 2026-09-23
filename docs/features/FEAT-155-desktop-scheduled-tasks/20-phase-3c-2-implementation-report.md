# FEAT-155 3C-2 实施报告：自动触发与独立重跑

2026-09-18。按用户明确授权实施[19方案](19-phase-3c-2-implementation-plan.md)六步。本批完成native候选、零真实调用组合验证与结构化自审后停止，未进入3C-3、页面或真实激活。

**结论：显式启用、自动到点消费和独立重跑已接入原执行链；普通入口继续schema15、scheduled默认禁发。** 实际macOS、Host/Runtime/Provider与产品D4仍NOT RUN，全部Must仍pending。文本累计0/12，图片0、商家接口0。

## 1. 范围、契约与来源

本批`contract-impact=breaking`，权威源为Desktop私有迁移21及native触发/重放语义。Owner/受影响consumer均为既有Desktop负责人；用户本轮批准19的范围和决策。共享RunTrigger/RunView已经表达manual/automatic/rerun及原run/槽，继续使用Contracts同源生成物；没有新增公共wire、typed IPC、Host路由、Runtime协议、依赖或服务。公共Contracts变更/pin/新四基线为N/A（本批源未变），不把私有native参数声明成已发布IPC。

开始前核对上批99份业务候选摘要，保存五仓工作区基线，保护所有既有dirty改动。[本批来源证据](evidence/phase-3c-2-source-20260918.json)记录候选SHA、旧迁移、实际命令及producer；共102份业务候选，本批Desktop18份文件变化（15既有、3新增）；所有HEAD/branch/remote保持，Contracts、Host、Runtime源未变，Runtime clean。候选尚未提交/发布，不是不可变发布pin。没有Git提交、推送、分支/远端变更或发布。

21 reader先于候选writer解释新事实；普通构造仍CompatibleReader/目标15。正常临时20库前向21、重开与旧manual摘要/回执/聊天保持。旧1—20 SQL字节不改；旧20 binary不能回退打开21，回退必须保留21 reader并关闭writer/dispatch，禁止down migration、删表、重置或复制日常用户库。

## 2. 实现结果

| 项目 | 本批行为 |
|---|---|
| 最小私有21 | 槽消费/明确未执行原因及run关联；trigger事实格式、自动进程代次/epoch/连续区间/60秒截止；独立发送关闭原因；启用回执和内部future_hold。仍只有原outbox，没有第二队列/历史 |
| 显式启用 | 当前UI/native授权，幂等优先；最终revision、新有限grant、enabled、严格未来next_at/槽和回执同事务。启用不创建run/聊天/outbox或扣额；旧回执不续额、复活暂停或清限制。已enabled不能经grant-only静默续额 |
| 到点组合事务 | 精确scope/plan/revision/epoch/槽、当前授权/Ask/目标/占用重验；消费槽、run快照、原聊天/outbox/绑定、一次额度、cursor/未来时间同事务。请求身份从稳定逻辑槽派生，并发/重复tick不多建或多扣 |
| 有界时间推进 | 按next_at/plan_id索引排序，每轮最多32项并yield；每秒扫描，变更通知唤醒同一等待器。忙碌仍扫描并记录busy；暂停后取消槽也推进游标，避免占满批次。多年离线每计划一个压缩区间，不逐次补跑，复用既有16候选evaluator |
| 原生命周期与Coordinator | 外层及SSE内层使用同一tick。先观察墙钟/单调时钟、恢复原因/截止并推进计划，再做Host恢复与到点裁决。旧unknown/Host未就绪不阻止处理恢复区间。新进程、wake及跳变清除自动连续性；回拨不倒退持久cursor |
| 最后发送检查 | 原HostBridge在ready/token/目录/审批await之后，通过worker重验，再记录首次attempt。automatic的create和turn都受原60秒窗口及同一进程/epoch约束；manual/rerun沿原有效授权。存储版本、enabled和观察ready均不能单独授予自动资格 |
| 错过与释放 | 已确认busy关闭该槽；完全never失效按充分证据同事务取消原outbox、保留已消费关联、释放并一次退款。create已attempted/已创建不补发过期turn、不退款，保留绑定/需处理，仅凭原生终态或可信正常代次停止释放。attempted不重POST |
| 未来限制与额度 | 内部budget/unknown等future_hold不改revision/清grant，最后预扣额度可发送自身run。到期阻止未开始阶段；未知尝试持久停止未来触发，释放互斥不清限制，须新的明确确认。pending审批只保持预约/attention，不误当unknown |
| 计划完成 | once消费时next_at=None仍不completed；对应自动义务的精确native终态或确定未执行且无未来时刻才完成。循环计划单次终态保持计划；manual/rerun不改变自动义务 |
| 独立重跑 | 只读预览比较原快照与当前PlanDefinition；明确确认绑定原run/snapshot digest、当前revision/definition digest/grant。事务重验后产生新run/operation和一次额度；当前三目标解析，原结果、槽、cursor和next_at不改。编辑冲突不静默采用新配置，原run占用/审批仍busy |

文件系统准备与SQL不是跨资源原子事务，仍沿3B-1稳定受管目录；SQL与网络POST也不是跨进程原子事务，attempt标记后的不确定结果只观察/恢复。没有自建聊天状态机、审批绕过、自动重跑或强制释放接口。

## 3. 实际验证

| 检查 | 实际结果 |
|---|---|
| FEAT-155安全集合 | `cargo test --manifest-path src-tauri/Cargo.toml --lib feat155 -- --test-threads=4`：**74/74 PASS**，含本批新增17项；本次采集实际producer |
| 旧路径回归 | 17个明确迁移/聊天/native观察/中断/正常退出case及authorization模块2项：**19/19 PASS**，名称及日志见来源证据 |
| 收尾复验 | 专属目标在启用时补查scope/项目可用性及删除状态；随后本批**17/17再次PASS**，见来源证据 |
| Rust静态 | `cargo fmt --manifest-path src-tauri/Cargo.toml --check`；`cargo clippy --manifest-path src-tauri/Cargo.toml --all-targets -- -D warnings`：**PASS** |
| 同源conformance | 既有plan/execution/recovery四份实际Rust输出通过严格源schema；新增实际automatic/rerun RunView逐项通过相同canonical execution schema |
| Desktop | `pnpm lint`、`pnpm build`、`pnpm docs:build`：**PASS**；保留既有chunk大小提示 |

新增17项覆盖：启用最终revision/幂等/禁止静默续额；三目标自动执行、最后预扣额度、重复/竞争tick；35计划的32项批次/忙碌跳过；60秒两端、late/offline、十年时钟跳变与回拨；ready await期间pause/sleep/stop；SSE内busy及原Coordinator自动终态/正常stop；完整never一次退款与create后禁止迟发；pending审批不变unknown、旧run不掩盖wake恢复；unknown正常释放后的新确认及旧回执不清限制；旧20手动回执/聊天→21及普通15；新进程不继承自动资格；重跑差异/编辑/幂等/删除拒绝和原自动cursor/历史保护。

所有数据库为正常临时SQLCipher，所有HTTP为进程内声明协议响应。使用真实native服务/原worker/Coordinator/HostBridge和原read/SSE事实提交，不启动真正App/Host/Runtime/Provider。时间检查传入墙钟/单调时钟参数或声明native事件，不修改设备时钟或强制睡眠；正常停止/退出，无强杀、权限破坏、攻击fixture或可执行文件替换。历史全量含禁止行为的套件未运行，不声称全仓测试通过。

本批没有共享源变化，因此没有重跑Contracts生成、完整lint/四基线或Host业务测试；前序报告保持历史含义，不继承为本次实际运行。五份producer保存于本需求evidence；包括新的[automatic/rerun输出](evidence/phase-3c-2-trigger-native-producer.json)。

## 4. 失败修正与分离自审

- 初始编译修正catalog长度、SQLite有符号epoch转换、statement临时借用和统一tick返回值；未降低静态规则。
- 首轮62项为60 PASS/2 FAIL：once完成SQL的JSON路径缺少`$`，导致确定取消/原生终态事务返回DatabaseUnavailable。修正路径后定向和完整集合通过，首次失败日志保留。
- 实现后的结构化审查发现暂停取消槽可能占满到期页，已补游标推进并用同批用例验证，不扩大为历史逐次补跑。
- 审查发现通用诊断错误可能覆盖busy关闭原因，已将`send_closed_reason`独立持久化；通用重试等待到期后仍不能重新取得发送资格。完全never已取消的操作报告FailedSafely，不误报未知提交。
- 连续性审查补齐恢复中再次发生时钟跳变的截止更新；OS转换清除旧时钟样本，避免把已知wake误当普通连续区间。
- 最后检查启用时专属目标的scope/项目/删除状态；不会因授权策略不含首次聊天绑定而跳过实际目标可用性。

| 自审维度 | 结论及证据 |
|---|---|
| 范围/权威源 | 仅私有native触发与21；共享源/Host/Runtime未改，无IPC/UI/真实激活 |
| 原子/重放/历史 | 原事务helper参数化，manual摘要保持；槽永久关联，rerun新身份、旧历史/时间不动；重复worker请求验证 |
| 权限/费用/审批 | 当前native+明确管理确认；有限grant、新预约与已扣额分开；pending/unknown分开，不自动审批或释放 |
| 连续性/发送 | 进程UUID+epoch+连续下界和原60秒窗口；内外循环、await后、两阶段分别核验；不可恢复关闭事实独立 |
| 兼容/回退 | 20→21/reopen、旧manual/聊天和普通15实测；1—20摘要一致；回退保留21 reader、关闭writer/dispatch |
| 测试与真实边界 | 临时存储/HTTP组合，不当作真实平台/模型或D4；禁止fixture未运行且影响明示 |

本轮未使用子agent；上述为Codex技术自审，不是独立人工批准。收尾无剩余阻断本批候选交付的问题；真实平台资格仍阻断日常激活。

## 5. 停点与未执行项

- **停止在3C-2**。草案/outputSchema及typed IPC留3C-3；页面、应用内重要更新、防空闲睡眠和真实激活资格留第四阶段，系统通知继续延期。
- 实际macOS sleep/wake、窗口退出、真实Host/Runtime/Provider审批恢复和正常产品入口：**NOT RUN**。组合PASS不能替代这些资格，普通15/默认禁发保持。
- 日常用户库/Keychain未访问、复制或迁移；无真实模型/商家接口、Git外部操作或发布。
- FEAT-155整体仍in_progress，全部Must pending、D4 NOT RUN；本批文本0次，累计**0/12**，图片/商家均0。

本轮元仓strict、D0、audit-claims、lint、50/50治理测试、Shell语法、五仓diff及155处本地链接检查均PASS；102份候选、5份原样producer与20份旧迁移摘要复核一致。D0只保持既有产品/设计批准，不代表真实激活或D4通过。收尾17项复验、fmt/clippy及Desktop lint/build/docs build均PASS，当前停点仍为3C-2完成后停止。
