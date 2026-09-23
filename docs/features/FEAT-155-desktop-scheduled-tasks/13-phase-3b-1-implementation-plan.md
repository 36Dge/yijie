# FEAT-155 下一步执行方案：3B-1 目标绑定、受管目录与组合事务

2026-09-18。本轮只读调查并制定方案，未开始3B代码、生成、迁移或产品检查。[12契约收口](12-phase-3a-contract-closure-report.md)已经完成，原[09第三阶段方案](09-phase-3-implementation-plan.md)的产品范围保持。

后续实际状态：用户明确授权本方案3B-1，现已实施、验证并停止，见[14实施报告](14-phase-3b-1-implementation-report.md)。下文“仅方案/未开始”保留制定方案时含义；3B-2/3C仍未开始。

## 1. 下一步与停点

**建议下一次只实施3B-1：稳定授权目标、受管目录和手动执行的同库组合事务。** 完成正常合成数据验证、来源检查与报告后停止。3B-2再接只读恢复、审批观察、正常退出和sleep/wake屏障；3C再接自动触发、重跑及草案后端。此次细分是用户要求的分步工作安排，不新增产品需求或生产治理切片。

下一批交付结果是：三种目标都能正确准备目录和本地聊天关联；一次内部手动请求原子形成run、原聊天outbox和一次额度占用；重复请求不重复创建。**这些记录仍不可出站，也不表示用户运行已受理。** 普通入口仍以schema15为迁移目标，预检继续返回`execution_not_ready`，没有新renderer command、自动扫描、服务启动或模型调用。

本轮文档`contract-impact=none`，未改变协议或行为。未来3B-1最高按**breaking**处理：新增持久关联和workspace来源解释，需新reader与前向兼容证明。已有共享类型如确需变化，先改Contracts权威源并同源生成；纯native绑定和SQL留Desktop，不预铺额外API。

## 2. 已核实的起点与取舍

本轮复核[收口来源证据](evidence/phase-3a-contract-closure-source-20260918.json)全部77份兄弟仓候选文件，摘要未变。五仓HEAD、分支和远端保持12所记，Runtime clean；既有未提交改动保留。12中的17项契约、22项native等PASS是上批实际结果，本轮没有重跑或继承为3B通过。

以下Desktop路径以`src-tauri/`为基准，行号是当前候选：

| 已有事实 | 方案约束 |
|---|---|
| `src/chat/schedules/execution.rs:136,164`把有conversation_id的目标解释成UserProject，并将definition/workspace纳入grant摘要 | 专属会话实际绑定必须与已授权目标策略分开，不回写用户definition制造grant stale |
| `src/chat/schedules/store.rs:89`只允许existing_chat携带conversation_id；`:399`的删除关联只查询原plan绑定 | 新专属绑定采用native独立关联，同时补齐删除/失效检查 |
| `migrations/chat/0001_chat_core.sql:8,26`要求project非空书签、session指向project；`src/chat/application.rs:1693`统一解析书签 | 仅新增目录表不足以接原聊天链；必须显式区分受管来源并保留旧用户项目语义 |
| `src/chat/database.rs:1750,2145`创建/追加自己开事务，`:1823`新聊天有独立create/turn操作身份 | 抽最小事务helper；一次worker事务组合，不串联两次提交；run关联turn operation，创建操作身份独立保留 |
| `src/chat/database.rs:8305`普通新聊天继承并重置前台draft_mode | 定时创建显式Ask，不能借普通helper改变前台偏好 |
| `src/chat/schedules/execution_guard.rs:38,76`分别扣住claim和真正出站；`execution.rs:532`预检最终未就绪 | 本批三处保护继续保留，不通过解除guard验证事务 |

选择“先本地准备/事务、后恢复/生命周期”，因为前者可用普通临时数据独立验证，后者直接影响真实出站、审批与退出。把整套3B一次接通会同时混入新的存储、目标、观察与进程行为，超出下一小批的合理验证边界。三目标不裁减；只把触发来源限定为内部显式manual，automatic/rerun仍按09后续接入。

## 3. 按顺序实施

### 第一步：冻结稳定目标与实际绑定的边界

- 用户definition继续表达名称、内容、时间和目标意图；已有聊天保留明确conversation_id。专属/每次新聊天的definition不接收或回填native会话ID。
- grant继续绑定已批准的revision、schedule_epoch、definition和稳定workspace策略；managed策略引用仍可为plan级资源身份，实际每个聊天的目录/会话关联另存native记录。目录准备或专属首次绑定不改用户revision，不静默重签授权，也不改已保存run快照。
- 优先保持现有grant摘要公式及旧字段含义。以正常schema17合成grant证明升级重开后仍能校验；若实施中确需改变摘要解释，必须显式版本化并使旧grant重新确认，不能覆盖旧digest伪装兼容。
- 明确身份：request去重一次手动操作；run关联一次运行；run.operation_id绑定原turn operation；create_operation_id沿原聊天创建/public-task binding保留；conversation/task、Host session、native thread/turn不混用。重复请求返回原身份。

受管目录接入推荐在**现有project记录增加明确来源分支**，保留session→project关联，native根据来源解析用户书签或应用受管资源。受管记录不是用户选择的项目：不得伪造bookmark，不能出现在普通项目选择列表，也不能经普通注册、刷新、置顶、移除或书签接口被当作用户项目管理。会话/历史读取仍须正确保留受管聊天关联。

旧项目默认保持user_project及原ID/书签/canonical hash；source与书签/资源ID组合须有明确约束，普通注册/刷新不能通过hash冲突的UPSERT覆盖managed记录。会话列表和单会话读取不能套用“只列用户项目”的过滤。existing_chat若引用受管聊天，也须按实际目录来源核权，不能再次被解释成UserProject。

若现有bookmark非空约束需要调整，只在新增migration中做保留旧ID、旧书签和引用完整性的前向变更；旧用户项目约束不放松，managed分支绑定受控资源而非任意路径。实施开始先列出相关SQL、查询与mapper的最小差异并自审。另建独立workspace主库再重接所有session引用影响更广，本批不采用；不扩建通用项目平台或增加项目UI。

当前迁移runner在事务中运行并检查外键（`src/chat/migrations.rs:146`），父表调整必须在含旧session/message/turn/outbox的正常合成库证明行数、引用、ledger及重开保持；不使用writable_schema或关闭最终完整性检查绕过问题。若在现runner下不能保留这些不变量，停在格式设计处报告具体阻断，不擅自扩大为全库重构。

### 第二步：兼容reader与必要持久格式

当前catalog为17，新增格式候选为**18**，内容只覆盖受管来源、专属实际绑定、run与原聊天/创建操作的必要关联。已有字段能无歧义复用时不复制；不建立第二run/outbox数据库或队列。

1. migration1—17原字节和checksum不改；仅正常合成临时库验证15→17→18（含完整中间migration）、重开及原聊天/权限/历史保持。
2. 普通入口仍使用CompatibleReader、迁移目标15；本批writer只经明确native候选构造用于定向检查。3A的17 reader不能冒称理解18；回退须保留已验证的18 reader并关闭新writer/出站，不降级、删表或复制日常库。
3. 兼容读取区分用户项目与受管资源，未知来源/格式拒绝；普通15/16/17路径不能无条件查询18新增列。writer关闭时所有scheduled outbox仍被扣住。
4. 新持久内容只存必要身份、引用和状态，不复制聊天/tool/Artifact正文或凭据。旧grant、原run快照和已保存请求的解释单独验证。

### 第三步：native幂等准备受管目录

- 根目录由native配置和应用数据位置决定；请求、renderer和模型不能传原始路径或伪造目录来源。资源按当前owner/tenant和稳定plan/request身份关联，入库前后均核对scope及目标。
- 专属聊天首次准备并绑定，后续使用同一有效关联；每次新聊天按不同逻辑请求准备独立会话/资源，同请求重试复用；已有聊天保持其原目录和授权引用，不复制目录。
- 文件系统准备在SQL事务外，随后事务内重新验证。普通准备失败不生成run/outbox；准备成功但事务因revision/占用冲突拒绝时可留下未绑定目录，下次同请求安全复用，不新增后台孤儿清理或删除用户目录。
- 准备前先核对当前native权限/scope并查询该request的既有结果；重试已提交请求只返回原事实，不因目录失效重新准备。此预查不能替代提交事务内的第二次去重与重验。
- 受管目录缺失/失效时返回明确不可用，不静默改路径、换项目或重建已经绑定的聊天。实际路径解析保持native来源判断；本批不启动Host使用该目录。

### 第四步：仅manual的同库组合事务

沿原SQLCipher/worker抽出创建/追加的最小事务helper，保持普通聊天外层接口和行为。内部手动请求只能来自受控native服务；不接受任意trigger、scope、permission或路径，不新增调试command。

一次事务先校验当前native authority/scope，再查同scope+request的既有run并比对稳定输入摘要：相同输入只返回原事实，不赋予新执行资格、不重复扣额；不同输入冲突。**仅全新request**继续plan/revision、目标/目录引用、Ask、grant次数/期限及前后台占用重验 → 预约和固定run快照 → 创建或复用本地conversation/task/message/turn及必要绑定 → 写**原chat_outbox** → 一次额度占用 → 提交。这样重复请求不会被自己的预约或已经消耗的最后一次额度拒绝。远端session/thread尚未创建，不能声称跨进程原子性。

- 新聊天的create记录以及由其后续派生的start_turn记录都须保持同一scheduled_run_id和正确的操作关联；不能漏标第一条create而被普通dispatcher送出。本批不实际执行后续派发。
- 专属/新聊天写Ask且不读写前台draft_mode；已有目标非Ask则拒绝，不自动切换。复用显式幂等turn路径的准备语义，不能回落到无operation的legacy文本v1。
- 同请求同输入返回既有整组身份，不重复扣额或创建；同request不同输入冲突。revision变化、已删除目标、前台占用、授权过期/耗尽等正常拒绝不留下部分数据库记录。
- **manual不claim自动occurrence，也不推进next_at/cursor。** 自动槽原子claim和推进等到3C真正消费时扩展同一事务；rerun也是后续独立请求语义，本批不预铺producer。
- 保留唯一预约及unknown阻断。没有真实终态就不返还在途额度/释放；本批不增加“强制完成/释放”入口。专属复用第二次运行以普通合成的已结束关联验证，不把合成状态冒充真实Codex执行。

### 第五步：关联保护、定向检查和报告

新增绑定必须接入当前删除/失效查询：dedicated/existing目标删除不能留下可继续执行的引用；new_chat某次历史聊天删除不影响未来目标策略。对本批尚不支持安全处置的在途关联采用明确拒绝，不能悄悄删预约；不提前实现完整取消/恢复状态机。删计划不级联删除聊天或目录，保留ADR-0014既有正文清理边界。

## 4. 完成标准

| 检查组 | 本批必须证明 |
|---|---|
| 目标/授权 | 专属首次绑定不改变grant；真正修改定义仍使旧授权失效；三目标关联正确，越scope/非Ask拒绝 |
| 幂等/事务 | 同请求仅一组run/聊天/outbox和一次占额；输入冲突、revision冲突、忙碌、授权不足无部分记录；manual不改变自动时刻 |
| 目录/项目 | 正常重复准备复用；失败无run/outbox；受管资源不进入普通用户项目操作，旧用户书签/会话读取保持 |
| 兼容/重开 | 1—17不变；临时18库正常重开；15默认不升级；旧grant/聊天保持；未知格式拒绝，回退reader边界明确 |
| 删除/关联 | 专属与已有目标失效可识别，new_chat历史删除不误停未来；在途未具备处置能力时明确拒绝 |
| 防误发 | create/start相关记录均有scheduled标识；claim筛选、实际dispatch及CompatibleReader均拒绝；预检仍未就绪 |
| 普通聊天回归 | 原用户项目、创建/追加、权限偏好、历史、删除相关定向用例保持，不全面重构旧链 |

先审查测试行为再运行：既有安全`feat155_`集合加本批必要用例，实际Rust producer conformance；Rust fmt/clippy及相关旧聊天定向回归；源变动时执行三族leaf生成/严格检查/同步、完整Contracts lint及12登记的四基线；涉及生成TS/前端类型则做相应lint/build，修改Desktop文档按仓规做docs build。元仓strict/D0/audit-claims、lint/test、diff/status和来源hash收尾。结果只在实际运行后填入后续报告，不预填PASS。

只使用普通合成输入、正常临时SQLCipher/目录和显式事务回滚。禁止强杀、故障注入、权限破坏、攻击fixture、替换二进制或改系统时钟；不跑包含这些行为的全量历史套件，并说明未覆盖范围。没有真实服务/Provider/UI证据时，三目标真实执行、恢复、平台资格和D4均保持NOT RUN。

## 5. 修改范围与后续依赖

| 仓库 | 3B-1范围 |
|---|---|
| Desktop | 目标/目录引用、私有migration/reader、最小project来源适配、同worker事务helper、必要删除/防误发保护与安全定向检查 |
| Contracts | 仅实际变化的共享语义/最小类型及派生物；无变化则复用并检查，不预铺管理/恢复API |
| Host | 本批不改；两个只读GET保持，消费留3B-2 |
| 元仓 | 方案、实际结果、来源与边界 |
| Runtime/API/Infra | 只读，不升级、不新增服务 |

3B-2仍需先消费Host原task映射和session/operation查询，再接原生审批观察、统一Coordinator、可取消退出、STOP_PENDING和真实sleep/wake屏障，之后才评估受控出站资格。当前Desktop退出过晚且超时会丢失受管句柄/身份；Host已有正常关闭实现可复用（`cmd/desktop-host/main.go:223`、`internal/codex/runtime.go:616`），不重做Host整套shutdown。missing、pending、uncertain及当前Host nonce都不能证明历史未执行或允许重投。

这些仍是原09/ADR-0020的范围，本次不提前实施。3C自动触发/重跑/草案、第四阶段页面/应用内更新/防空闲睡眠开关和最终验收均保留；系统通知继续延期。

另有明确的激活前UI接续：`src/components/chat/ChatSidebarTree.vue:40`当前把不在projects列表的会话组视为“项目已移除”，`src/pages/chat/ChatPage.vue:125`名称回退为“本地项目”。受管记录隐藏后聊天查询可保留，但旧标签不正确；本批仅未激活候选，不修改页面或冒称已承接。后续激活前补最小来源投影及标签适配（若跨边界则source-first），不能为绕过标签问题把受管资源放回用户目录选择列表。

## 6. 本轮与下一批的明确边界

本轮只保存方案，3B-1尚未授权为本轮立即实施；两项只读技术交叉复核不属于独立人工批准。下一次若按本方案实施，完成3B-1检查和报告后停止，不自动接3B-2或3C。

本轮及推荐3B-1均不访问日常数据库/Keychain、不迁移日常库、不启动App/Host/Runtime/Provider，不发起模型/图片/商家调用，不新增renderer入口或绕过guard。文本总额度保持**0/12**，图片0、商家0；未提交、推送、发布或改分支/远端。超过16小时已获允许，但不扩大功能目标。

本轮文档收尾检查：strict、D0、audit-claims、元仓lint、50/50治理测试、Shell语法、diff、链接与来源摘要复核均PASS；只证明方案和记录一致，不表示3B实施/验收通过。
