# FEAT-164 S4 r4 同源 App 与计划安全验收

结论：本轮发现并修复两处真实接线缺口，普通App与计划限定验收通过；完整FEAT-164未完成。最终来源Runtime a28130a r4 / Contracts1b357cc / Host7927ee7 / Desktop277f59e。新增真实模型HTTP0，计划最终关闭，App及fixture均已正常退出。

2026-10-25，Owner要求认真审计后继续下一步。沿用Runtime a28130a / Contracts1b357cc / Hostb9155a3 / Desktop2fb8989；新增真实模型HTTP许可0，仅FEAT-164本地提交，不推送。旧30元账本、2/2已用请求、14.188544元unknown预占和14.328134元累计上界保留。

本轮先做既有实现验收，contract-impact=none：不修改跨仓wire、存储格式或执行解释；FEAT-164整体breaking保持。如发现产品缺陷，先核对影响及授权再修复，不以测试修改伪造通过。

审计撤回一项初步担心：launcher里的新Host/Runtime空目录并非实际运行数据根。`ChatRuntime::from_environment`调用`SidecarSupervisor::with_scheduled_tasks`，在隔离模式下将两者统一绑定到候选App数据中的host/runtime，与SQLCipher位于同一产品根。无需搬库、改标识或放宽入口。继续沿原候选正常升级/重开，不运行旧writer写新失败历史。

起点已保存7仓496项工作区文件、908份旧证据、原资源/日常数据库及两套App构建摘要；候选App数据5583文件完整复制到独立审计目录并逐字核对，只用于保留，不作为降级启动来源。原工作区不改。当前r4 ordinary构建收据有效；本轮不将其写作专家/媒体组合资格。

执行顺序：先以相同构建、白名单环境、dummy key和固定18083本机服务重开；确认旧隔离历史保持且读取零请求；通过真实UI新Kimi请求、计划草案input-only、保存paused及明确手动执行、正常取消/关闭与同源重开。离线服务最多16请求，无外部客户端或转发；每次请求核对当前模型/推理档位，只回应明确S4F合成标记。不得制造unknown、篡改SQL/rollout或断进程来触发恢复/取消；不可自然到达的状态保留NOT RUN并依靠已审阅的普通结构化检查补充，不能冒称UI覆盖。

暂停/取消、退出、旧状态与完整G3分别判定；出现产品失败先保留证据并审计，不反复重试。所有服务正常停止，无强杀、攻击/故障注入、权限破坏或程序替换。未授权真实模型、搜索/图片服务或平台业务调用。结果随后按实际记录。

## 草案首轮失败与最小修复

r4同源重开正常，旧S1历史可读且请求0；新Kimi/max普通任务完成，fixture累计1。通过对话创建计划后停留“等待提交”，正常恢复确认先取消（0增量），再显式继续一次仍未继续；不重试、不改数据库。候选以⌘Q正常exit0，fixture自身shutdown停止。

只读Host查询显示draft capability ready，但原task映射404。正常关闭后对候选DB的immutable只读副本查询，仅输出本轮合成草案元数据：create_session failed、attempt_count2（本地任务绑定与会话创建分阶段claim）、create_attempted1、turn_attempted0、public binding已bound、Host未绑定；没有输出密钥或其它聊天正文，没有修改原DB。工具链接本项目现有SQLCipher库，新诊断文件不替换任何运行程序。

完整调用链：Desktop HostBridge model route将草案create/resume/turn映射到`/v2/model-chat/scheduled-plan-draft-sessions...`；Contracts1b357cc已有三条权威路由及原草案请求/回执，Host `registerChatModelsV2`仍只有普通路径。实际HTTP router定向回归在修复前复现404，说明前轮原生调用面子集不能替代真实HTTP路由接线。

本修复contract-impact=semantic：恢复已登记v2草案接口的既定行为，不新增wire/schema/数据表，不改变input-only或授权。已有不可变Contract源先于此次实现，不需要虚构新契约版本；Host沿现有身份、退役profile、feature gate与delegation统一处理增加三条route，继续调用原fixed-purpose handler。新增安全路由回归检查两种当前模型的三种操作，以及缺认证、无profile、旧K3、功能关闭的正常拒绝；不执行攻击或故障注入。后续Desktop仅重新冻结实际Host源和canonical构建，r4 Runtime/Contracts不改。

原失败草案已经尝试过创建，404不能改写成never-sent证明，也不能重置或自动补发。修复后使用新的明确UI提交作为正控，并再次确认原失败操作未重发；原界面未清楚呈现创建失败的限制另记，不以删除记录消除现场。

Host最小修复已仅本地提交`7927ee7b385cb5536c3647632d1bac0cb7c56fea`（产品route、独立回归、说明3文件），Desktop`7ca0d5f6fda8a01febc5324673d2b353335afc95`只重生成Host build锁；逆向差异证明原工作区内容保持。路由回归6条Go PASS记录及原草案handler3项、race/vet通过，0失败/跳过。新`feat164-s4f-qualification-20261025`隔离树构建，不更新旧两套App。首次新树构建缺tools/public-api-generator已安装依赖而停止；保留missing-generator-deps日志，在该工具被忽略的node_modules中复用原固定依赖后重新canonical构建，未改package/lock或产品校验。

## 当前事实格式的草案读取缺口

Host route修复后的新草案`01a17323-8807-7680-b4bc-672d4283a226`实际已完成，唯一新增请求Kimi K3.1/max、tools空、返回合法candidate；原attempted草案在重开时0补发。但UI摘要仍unavailable。正常退出后只读候选副本确认新回合的6条原生事实都是format4，包含完整agentMessage与completed终态。`native_conversation_storage::NATIVE_WRITE_FORMAT=4`，草案preview却把任何非2记录视为未知；不是模型或route再次失败。

最小修复contract-impact=semantic（既有私有持久格式的reader兼容）：草案读取明确支持已冻结格式2/3/4，分别经对应生成NativeNotification类型解码；未知格式仍拒绝，不迁移/重写历史，不从thread/read或空答案猜终态。实际成功终态、唯一完整正文、schema校验、原scope/thread/turn绑定、审批和保存许可不变。当前生产writer经原outbox/binding/NativeDisplayBuffer写入格式4的普通回归，修复前精确1FAIL，实际返回unavailable；新测试同时验证重复读取不写事实、不创建计划/授权/运行。独立版本解码测试覆盖2/3/4及未知版本拒绝，属于兼容性验证，未注入攻击或故障。

前一组route-only App已正常退出，原bundle和收据归档到本轮审计目录；仅通过canonical构建更新本轮新树产物。接下来重开后首先只读已有completed草案，验证无新增HTTP即可恢复候选，再保存/单次执行；不会重新提交同一已完成草案。

复核中保留两项非产品重复失败：扩大的FEAT-164测试选择器将需要paused=true的专属用例放进普通环境，结果33PASS/1环境前置FAIL；当前writer/reader回归已PASS，随后按普通与暂停环境拆分验证，不改该保护断言。Clippy要求将`2 | 3 | 4`写成等价固定范围`2..=4`，已修正；范围上限仍字面4，不跟随未来writer自动扩大。首次错误日志均保留。

## 最终结果、审计与下一步

| 项目 | 结果与适用来源 |
| --- | --- |
| Host v2草案路由 | `7927ee7b385cb5536c3647632d1bac0cb7c56fea`，6条Go PASS记录含3子用例，原草案handler3项PASS，race/vet通过 |
| Desktop持久reader | `277f59eeef538d159e43bb1570767ca4f2f5f72a`，当前writer事实预览/重复只读、2/3/4版本、暂停环境保护、原唯一完整成功/schema判定4项分别PASS，Clippy及fmt通过 |
| canonical装配 | 固定Runtime `a28130abb13d0f99a00107cd513a653bae878b77`、Contracts `1b357cce0575c492f3715b316ee5f254051acf80`；新目录ordinary构建，不含专家/媒体组合，旧两套App保持 |
| 当前草案UI | 原生已完成、实际Kimi K3.1 Pro/max、tools空。最终reader重开读取既有completed草案恢复候选，未重发 |
| 计划UI | 审阅默认当前模型，保存为关闭；明确点击“立即执行”完成一次，原答复/运行记录可追踪；取消未保存编辑保留原内容，计划始终关闭 |
| 正常重开 | 同一收据重开后计划仍关闭、原运行和答复保留，fixture仍2请求。无自动补发或新增授权 |
| 数据保护 | 原attempted失败草案的元数据逐项相同；completed草案原6条Native事实hash不变，只允许正常新增只读观察事实；没有手改SQL/rollout或将404当never-sent |

本轮App模型协议HTTP共3：早期2fb普通正控1、7ca新Host下draft1、最终277计划运行1。后两者同一独立fixture账本2请求，原账本1请求；两账本都正常stopped，拒绝0、外部0。进程内router测试及Native普通Host传输fixture不计作模型请求；不将合成usage解释为供应商费用。旧累计30元、2/2真实请求、14.188544元unknown预占与14.328134元上界不变。

首轮route失败与后续reader失败是不同checkpoint，各保留App观察与安全RED证据；每个在最小修复后验证通过，无第三次同点失败或伪造RCA cycle。源审计同时保留旧failure ledger；新增两项armed历史事件按现行validator规则记录，PASS单独列remediation。原失败草案安全保留为不可自动重发；此前观察到的“等待提交”提示和后续人工处置体验未专项修复，仍是待完善项；不能将本轮正控通过写成全部历史失败恢复已闭合。

下一步优先补齐原attempted/mapping missing草案的可见状态与安全处置判定，再以正常产品路径补旧模型计划退役、重新选择/重新授权及完整恢复取消UI。任何会改变unknown/attempted、取消或重发资格的方案必须先走Contract First，不能重置旧请求；当前源专家/媒体组合要独立canonical构建验收。其它平台、完整TCONF-164-04、当前G2V、逐切片G3/freshness与最终E2E仍未通过。已有HTTP许可0，真实能力验收另需明确额度，不继承预算余额。

未执行强杀、可执行替换、攻击/故障注入、权限破坏、日常库迁移、真实搜索/图片/平台调用或自动时间触发。取消恢复确认与取消编辑只证明对应UI动作零发送，不代表never-sent outbox取消或运行中断资格。没有开启任何自动计划，未来时间23:59不会由本轮计划触发。

最终治理与保留证据见`s4f-governance-results.json`、`s4f-preservation-audit.json`、`s4f-static-review.json`及`s4f-meta-isolation.json`，仅依据其实际结果判定。提交只含FEAT-164所属差异，长期记忆只暂存本需求段落；无push、tag、分支变更或发布。元仓SHA以包含本文的Git记录定位。

最终检查实测完成：claims/strict、元仓lint、53/53治理测试和7个shell语法检查通过；S4 G3实际仍BLOCKED。保留审计核对496原改动、908旧证据、154资源、7日常数据库文件、161旧App文件及5583项候选事前副本均保持；本轮route-only中间App亦留存。新source与canonical收据逐项一致，18083/18086已释放，无所属App/Runtime残留。完整摘要见[s4f-verdict](evidence/s4f-verdict.json)。

提交前审计的Node读取器因默认1MiB输出缓冲不足中止只读git show（较大的起点摘要约1.3MiB）；该环境限制不涉及App/Host/Runtime生命周期或验收执行。改用Python读取逐项比对暂存blob与文件，92项精确一致；不裁剪或改写大证据文件。
