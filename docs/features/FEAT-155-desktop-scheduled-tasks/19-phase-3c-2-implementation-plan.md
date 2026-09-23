# FEAT-155 下一步执行方案：3C-2 自动触发与独立重跑

后续结果：用户已明确授权本方案六步实施，本批候选交付见[20](20-phase-3c-2-implementation-report.md)，完成后停止。下文“本轮仅方案/未实施”保留方案形成时含义。

2026-09-18。用户本轮要求“给出下一步执行方案”。本轮仅只读调查、保存方案和检查需求文档，不开始实现。起点为[18：3C-1实施报告](18-phase-3c-1-implementation-report.md)，原目标、授权与分批安排沿[04](04-owner-approval-and-implementation.md)、[17](17-phase-3c-1-implementation-plan.md)及[ADR-0020](../../adr/ADR-0020-local-scheduled-task-authority.md)。

## 1. 下一批与完成边界

**建议下一次只实施3C-2：显式启用、自动到点裁决与独立重跑。** 在3C-1原组合事务和发送链上补齐另外两类触发来源，完成零真实调用的组合验证后报告停止，不自动进入草案、typed IPC/页面或真实激活。

本批交付native候选：明确启用后的计划能在有证明的连续清醒区间内到点消费一次；忙碌/错过有真实记录；显式重跑用当前配置产生新run。普通App仍迁移目标15、默认禁发；存储模式、新状态或恢复就绪均不能单独赋予调度/发送权。既有真实平台/Provider资格仍NOT RUN，不因代码或合成检查通过解除阻断。

本轮文档`contract-impact=none`。未来本批最高按**breaking**管理，预计新增Desktop私有schema21，影响槽处置、触发身份及跨重开解释。公共边界只在确有消费变化时回源，不预铺完整管理API；固定Runtime、Host执行协议和职责保持。

本批支撑AC-004/005/006/007/009/010的时间、启停、去重、关联、重跑与恢复，也为AC-008的计划生命周期提供事实。全部Must仍须后续真实产品验收，不能用本批检查标PASS。三目标、两种创建方式及本机唤醒目标不缩减；系统通知继续延期，超过16小时不构成停止或减范围条件。

## 2. 源码事实与选择理由

已复核[3C-1来源证据](evidence/phase-3c-1-source-20260918.json)99份业务候选，摘要一致；五仓HEAD、branch、remote保持，Runtime clean。18中的57项native、19项旧回归和最终2项复验是上批结果，本轮没有重跑产品测试。两项只读技术复核分别覆盖自动事务与重跑/发送/生命周期，不是独立人工批准。

下表Desktop路径相对`src-tauri/`，行号为本轮候选：

| 现有事实 | 本批必须补齐的内容 |
|---|---|
| `src/chat/schedules/execution.rs:299`确认grant后仍paused；`store.rs:299–350`只有暂停/删除 | 显式启用与最终revision/grant必须原子一致，不能自授或静默续额 |
| `execution.rs:162–168,209–242`授权摘要绑定revision/epoch/定义/目录 | 不能enable先加revision再继续使用旧grant；内部停止未来不能误拒本run最后一次预扣额度 |
| `execution.rs:389`固定manual；`execution/dispatch.rs:70`只允许manual | 参数化原准备事务，同时分别校验三种触发身份，不能只删条件 |
| `execution/preparation.rs:36`请求摘要仅含grant/revision/request | 新automatic/rerun请求须区分来源、槽/原run及确认配置，保留旧manual重放兼容 |
| `migrations/chat/0016_scheduled_plan_foundation.sql:53`无已消费、迟到、忙碌等槽处置 | 新增21及兼容reader，旧1—20不改；消费事实不能由未来预览覆盖 |
| `time.rs:165–180`已有60秒/恢复优先纯判定，preview最多16候选 | 接入真正native连续性证据，复用既有日历计算，不遍历多年历史 |
| `lifecycle.rs:14–19`只有phase/epoch/最近时钟；恢复统一传Recovered | 补恢复原因、截止时刻和连续区间，区分offline与clock_discontinuity |
| `application.rs:2306`仅无恢复run时推进计划时钟；`:2800–2805`SSE内未观察时钟 | 计划时间恢复独立于旧run；内外循环共用tick，长turn期间也处理到点忙碌 |
| `execution/dispatch.rs:216`never受阻后五秒复验，没有自动期限 | automatic必须在实际I/O前复验槽时效，不能变成无限迟发队列 |

可选顺序是先做自动、先做重跑，或在同一批内复用触发身份/事务完成两者。**推荐第三种**，保持17已给出的3C-2边界：先完成自动所需的时间和启用规则，再接很小的重跑预览/确认分支，共用原事务与发送检查；不另外扩建调度框架或提前接草案/UI。

## 3. 按顺序实施

### 第一步：冻结最小触发、启用与存储语义

先形成manual、automatic、rerun的判定表，再改consumer。继续复用共享RunTrigger/RunView已有的logical_slot、original_run_id等字段。native内部的触发输入、扫描票据、差异确认参数和SQL实现留Desktop；若新增独立消费的共享类型、错误或输出，先更新Contracts权威源、生成与严格conformance，再消费。没有注册renderer入口前，也不能手写一套声称已发布的IPC。

新增下一私有迁移，当前候选**schema21**，只增加本批需要的事实：

- occurrence的消费/run关联及明确未执行原因：已消费、迟到、忙碌、目标/权限/资源不可用、授权不足等，与既有暂停/离线/时钟不连续/取消分开。
- 自动run的原槽、计划epoch、native进程代次/连续性证据和发送有效边界；仅epoch数字不足以跨重开识别，不能把新进程的同号epoch当作旧许可。
- 显式启用的请求幂等及未来触发的暂停/需确认事实；区分用户操作、未知执行、预算和普通待审批。
- 新触发请求的摘要解释与旧manual摘要兼容。可以用版本/命名空间等最小方式区分，不能批量改历史hash或让同一request跨trigger复用。

不是另一份队列或聊天历史。消费事实一旦建立，即使本地取消/退款也不能把该自动槽重新变为planned；旧`insert_future`对cancelled未来预览的重建不能覆盖已消费记录。计划时间编辑才改变schedule_epoch，启用/重跑不借增epoch重复消费过去槽。

先实现读取/未知格式拒绝，再允许候选writer写入。正常临时SQLCipher验证20→21及重开、旧manual请求回执、旧聊天/授权/恢复记录保持；普通入口仍15。旧1—20 SQL/checksum不改，回退保留21 reader并关闭writer/dispatch，不降级或复制日常库。

### 第二步：显式确认并启用，只安排未来槽

推荐新增一个明确的native“确认有限授权并启用”动作，复用已有确认参数和当前UI管理授权，不改变旧`confirm_grant`只确认不启用的含义。

同一worker事务：先按请求检查幂等 → 当前scope/UI管理能力、expected revision、目标/Ask和占用 → 确定最终revision → 建立绑定最终revision/当前定义的有限grant → 写enabled及授权引用 → 求严格未来的next_at/候选槽 → 记启用回执。旧grant不静默重绑或补额；重放同一请求返回原确认及当前状态，不重新启用已暂停/编辑的计划。对没有内部未来停用限制、当前有效enabled的计划，新启用请求返回状态冲突/当前状态，不悄悄续额。因unknown/预算等内部原因停用未来触发的计划，在原run满足处置/释放前提后，可以通过本动作的新明确确认建立新最终revision/grant、清除未来限制并安排严格未来槽；旧请求重放永远不能清除该限制。

- 当前有本plan未处置run时，不通过重授权改变它的执行含义；沿既有预约/占用规则处理。
- 当前配置没有未来时刻的once计划不能直接重新开启，须先编辑时间。暂停期间的过去槽不补跑。
- 启用本身不创建run、聊天、outbox、reservation或占额度，也不发模型请求。
- 用户暂停/编辑和claim在同一writer串行裁决；用户操作引起的revision/授权变化仍阻止尚未开始的I/O，不强行中断已经提交的native turn。
- 额度耗尽停止**新增预约**，已合法预扣的最后一额在grant仍有效且其它资格满足时可发送；内部因耗尽停止未来，不能先撤销自身grant而误拒该run。授权到期则阻止所有尚未开始阶段的新I/O，已attempted操作只继续观察/恢复，不因到期退款或伪造终态。

真实attempted未知必须持久停止未来自动触发，并要求用户明确确认后才恢复未来槽；仅释放unknown的互斥不能自动清除这一限制。普通pending审批只保持预约/需处理，不等同执行未知，不自动批准，也不因回调消失推定完成。内部暂停未来不得盲目调用会增加revision/清grant的用户pause，误伤已有run；已有run的只读恢复与native终态观察一直保留。

### 第三步：到点裁决与同库组合事务

未来只保存计划和planned槽，不提前创建运行或占额。到点时先重读当前native计划；只有可能符合条件的候选才做目录准备和必要的有界只读检查。已有会话的执行/审批未知或忙碌不能靠另开聊天绕过；新聊天仍使用3B-1的受管目录。

目录/必要读取之后，回到原worker的一次SQL事务，用新now、当前连续性票据和精确槽重验全部条件：

`(owner, tenant, plan_id, schedule_epoch, logical_slot, scheduled_at, revision)` → enabled/未来触发限制 → grant/目标/Ask/全局占用 → 一次消费槽 → 冻结run → 原聊天/原outbox/绑定 → 一次额度 → cursor/严格未来next_at及下个候选槽。

复用3C-1的组合事务helper和原发送器，不串几次worker调用冒充原子，不将Host POST放入SQL事务。稳定槽唯一键决定自动幂等；每次tick新建request ID不能绕过去重。目录按稳定槽准备标识复用，重复tick不制造不同受管资源；文件系统准备仍不冒称SQL原子。

| 裁决 | 持久结果与副作用 |
|---|---|
| 同一已消费槽再次到达 | 返回既有处置/run，不新建、不扣额、不重投 |
| 连续清醒且`scheduled_at ≤ now ≤ scheduled_at+60`，其余条件满足 | 原组合事务接纳一次automatic run |
| 前台/定时/待审批/删除占用 | 记录本槽busy并推进未来，无run/outbox/额度；不等待占用释放后补跑该槽 |
| 目标、权限、资源或授权不可用 | 记录对应安全未执行原因并处理未来资格；不创建假成功run或无限排队 |
| 迟到超过60秒 | missed_late，推进严格未来，不逐槽补跑 |
| 重开/sleep-wake/时钟不连续区间 | 优先记录对应错过区间，再求未来；即使醒来仍在60秒内也不补跑 |

同一时刻多个计划按`scheduled_at, plan_id`确定性排序，当前全局预约仍占用时，其余记录busy；不新增“同一UTC时刻永久只准一个run”的限制。扫描使用固定有界批次（建议每次最多32个计划）和到点索引/游标，处理后yield；不能每50毫秒读取全部计划，不能因全局忙就完全停止扫描并遗漏busy事实。多年离线每计划压缩记录一个跨过区间，复用最多16候选的时间evaluator，不创建成千上万个历史槽或run。

### 第四步：统一native tick与发送时效，保持原恢复规则

在原生命周期owner/唯一Coordinator上增加同一个native tick，覆盖外层等待和长时间SSE内的dispatch机会。顺序为：观察墙钟/单调时钟及epoch → 处理恢复原因/截止边界 → 有界恢复计划时间 → 到点裁决 → 原dispatch。暂停/编辑/启用等变更唤醒同一等待器；无需第二Coordinator、OS cron、后台守护进程或新的OS唤醒服务。

ReadyForObservation不等于有连续清醒证明。新启动、wake和时钟跳变先关自动资格，记录当前进程代次、epoch、原因及恢复截止时刻；完成对应时间恢复后才证明后续区间连续。计划时钟恢复必须独立于是否存在待恢复run；某个run仍unknown或Host未ready，不能让旧到期槽因此留到恢复后执行。回拨不越过持久cursor，向前跳变不产生补跑风暴。

3C-1的双层默认拒绝保持；候选内部逐trigger验证。manual沿原行为，rerun要求原run及确认事实，automatic必须关联已消费的原槽和native时间资格。实际I/O前在Host ready/token/目录/审批等await之后，再核验当前时间、epoch/进程代次、plan/grant/目标/占用，不能只在claim时验60秒。

自动运行的两阶段边界采用保守规则：

- create和turn各自**首次**可能I/O前都要满足原槽窗口和同一连续性资格。正常远端创建后的turn仍在窗口内才继续；不能把已claim当作无限期发送许可。
- 完整never的自动run遇窗口失效或sleep/reopen，按可信证据同事务取消原未发outbox、记录已消费槽的未执行原因、释放并一次退款；该槽仍不能再次claim。
- create已经attempted/远端已创建而turn仍never时，若窗口/连续性失效，不再补发turn；保留真实绑定及需处理原因，不伪称全未发或退款，释放仍按已有可信终态/正常代次停止证据。
- 已经attempted的原操作永不重新POST；精确accepted继续read/SSE/审批观察。时间截止、暂停或新nonce不构成原生终态或释放证据。
- 普通短暂不可用若尚在原窗口内，可在有界等待后重新核验首次发送资格；已确认busy应结束本槽，不沿manual的五秒复验无限排队。所有跨await后的检查和未知证据处理继续复用原链。

因此3C-1“已确认create、有效never turn可接续”的恢复规则必须按trigger区分：manual/rerun仍依有效授权继续；automatic还须原槽时效/连续性有效。没有新增强制结束、强制释放或自动重跑入口。

once的`next_at=None`只表示无未来候选，不能在claim时就标completed。对应自动义务取得精确native终态，或槽明确错过/未执行且无未来时刻后，才按既有产品规则完成；unknown保持暂停/需处理。循环计划单次终态不完成整个计划；native completed不表示商家业务成功。

### 第五步：显式重跑用当前配置创建新run

在同一native执行服务增加最小只读预览和明确确认；本批不做详情UI或renderer command。

1. 以当前权限读取原run，验证owner/tenant、同一plan、原快照digest。计划已删除禁止重跑，不能恢复其正文或授权。
2. 比较原快照与当前已保存的**PlanDefinition**，返回真实内容/名称/规则/目标差异；grant、状态和计数等元数据不伪装成内容差异。快照/定义沿现有同源类型，不复制聊天正文。
3. 确认绑定原run、原snapshot digest、当前revision/定义摘要和当前grant；实际提交再次核验。期间编辑则返回冲突，不能静默采用用户未确认的新内容。
4. 在原组合事务建立新request、新run、新operation和一次新额度，保存`trigger=rerun`与`original_run_id`。原run结果/快照、原自动槽、cursor和next_at不改；手动/重跑不完成或重开原自动调度义务。
5. 同请求重放先返回原回执，不重复占额；同request改原run/trigger/确认配置必须冲突。已有有效paused计划可显式重跑；原run仍占用、pending审批或未释放unknown均返回忙碌，不借重跑强制解锁。unknown已经依法解除互斥时，仍保留旧结果，新run由明确确认独立产生。

三目标沿当前保存的目标执行，不重放旧历史目录或旧权限；新聊天模式产生新会话，专属/已有模式在授权和空闲条件满足时复用正确会话。发送和审批沿3C-1同一native链，不恢复旧operation。

### 第六步：安全验证、报告并停止

| 检查组 | 完成标准 |
|---|---|
| 启用与兼容 | 明确确认绑定最终revision/grant；启用幂等不续额/复活旧状态；20→21正常前向/重开与旧聊天/manual回执保持；普通15/reader零scheduled POST |
| 自动原子性 | 三目标，槽/run/原聊天/outbox/额度/cursor一起提交；重复tick、同槽竞争、正常重开只一条运行；不提前准备可执行队列 |
| 时间与占用 | 四频率/DST、60秒两端、多年离线、回拨/前跳、已有恢复run时wake；SSE内也记录busy；有界批次，不补跑/无限排队 |
| 发送前变化 | 目录准备/ready/审批await期间编辑、暂停、授权到期、busy、sleep/stop均生效；最后预扣额度仍可用；过期自动never与create已尝试分别正确处置 |
| 恢复与计划状态 | attempted不重投；unknown释放互斥后未来仍需确认；pending审批不误当unknown；once不提前completed，原索引/占用/删除/中断语义保持 |
| 重跑 | 差异预览、确认后编辑冲突、同请求幂等、错来源/已删计划拒绝；新身份/新扣额，原历史和自动cursor保持 |

使用普通临时SQLCipher、纯时间参数、受控native事件、真实native服务/原Coordinator和进程内HTTP正常响应；分别记录合成组合证据与真实平台资格。不改设备时钟、强制睡眠、强杀进程、破坏权限、攻击注入或替换Runtime，不运行含禁止fixture的历史全量套件。

有变化的共享源才执行相应source-first生成/同步、strict conformance和适用四基线；Desktop做本批及受影响旧路径定向检查、fmt/clippy、必要lint/build/docs build。保留失败与修正、具体命令和来源摘要，不继承上批PASS。元仓strict/D0/audit-claims与必要文档检查收尾，报告后停止。

## 4. 仓库与未执行边界

Desktop承担私有21、启用/触发/重跑事务、连续性与原Coordinator接线；Contracts仅处理实际跨边界变化；Host优先复用既有能力，不新增scheduler/API。Runtime/API/Infra固定只读，日历库不升级，元仓保存方案/报告和来源。

本批仍为零真实文本调用，累计**0/12**，图片0、商家接口0；不启动真实App/Host/Runtime/Provider，不访问日常库/Keychain，不迁移普通用户数据，不提交/推送/发布。实际macOS、Provider审批/恢复、正常产品入口和D4继续NOT RUN，候选timer通过不等于可以正式激活。

完成3C-2后停止。草案/outputSchema及最小typed IPC留3C-3，页面、应用内重要更新、防空闲睡眠及真实激活资格留第四阶段。已有总预算和授权保持，本轮方案请求不是立即实施3C-2的指令。

最终方案复核已拆开额度耗尽与授权到期，并闭合内部未来停用后的新确认恢复路径；旧确认不清限制，原run未处置不重授权。同时明确多计划只受当前有效预约限制，不新增同一UTC时刻的永久运行上限。修正后无其余必须修改项；技术复核不是独立人工批准。

本轮strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、五仓diff及93处文档链接/空白检查实际PASS；99份业务候选摘要、HEAD/branch/remote与已有dirty条目数保持。以上仅证明方案/记录一致，不表示3C-2已实施或产品验收通过。
