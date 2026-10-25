# FEAT-164 S1—S4 证据绑定与三项最终验收

2026-10-26（Asia/Shanghai）。Owner确认38号结果后，授权在零新增真实模型调用下收口证据与最终验收；另明确锁屏时可跳过依赖解锁的项目。此次桌面实际可用，未发生锁屏跳过。仅验证与治理记录，`contract-impact=none`；产品源码、契约、SQL、权限和Runtime均未修改，整项breaking分类保持。

## 当前来源与验证

继续使用已经构建并通过真实文本G2V的同一候选：Desktop `ea9b1e499d86bb92eea360a62707027485790e22`、Host `090c2dbeeeceb0fc87e576d8e13f5c339bf106f0`、Contracts `1b357cce0575c492f3715b316ee5f254051acf80`、Runtime `a28130abb13d0f99a00107cd513a653bae878b77`、Connectors `7ea3df41818fd69f4736722d01f0686d584d1a71`、Skills `595c927ae101d3d31c234f60565041eee0864680`。新验证目录为既有 `feat164-s4k-qualification-20261026`，没有复制或替换执行程序。

原slice索引仍混用早期r2、174fbaf/ddc840f/4d04597等引用。按既定失效规则，在当前来源仅运行一次已审查的安全allowlist，重新绑定实际命令、时间、完整commit、契约、fixture与qualified harness；不把旧结果改名成当前运行。旧manifest完整留在 `evidence/s4l-prior-feature.yaml`。

| 本次实际执行 | 结果与范围 |
|---|---|
| S1 | 11项（10子例＋父项），配置前身/未知配置拒绝/暂停/退役准入 |
| S2 | 25/2/12/17/1五组，共57项，存储、恢复、未发送取消及真实Native/Host/Runtime边界 |
| S3 | 5项exact Native用例，计划退役、授权、重放与worker顺序 |
| S4基础 | 7/4/4/4/5，共24项，服务、真实Runtime、Native、renderer、组合配置 |
| S4专家/媒体/辅助 | 4个source组合＋9行为检查，37专家资源、worker/adapter、代理/Guardian/压缩 |
| S4旧loaded/原生终态 | 7项，旧父子图、退役guard、失败重放及自动压缩 |
| Renderer / 判定器 | 18 / 10项 |

合计 **141项测试＋4个source组合检查，全部通过且无skip**。S4三个driver共42次本机合成HTTP，App另4次，真实模型新增0。没有运行攻击、危险fixture、权限破坏、强杀或程序替身测试；没有重跑真实Provider。各子集的边界说明保持，不据此宣称完整TCONF-164-04通过。

## 当前 App 验收

canonical同构建运行，Kimi与MiniMax均使用明确dummy凭据和只会返回合成协议的127.0.0.1 fixture；没有读取真实Provider凭据或启用付费计量器。本轮复用既有fixture原文件，其S4K标记表示fixture版本，新的账本、任务名和证据均独立归属S4L。

1. 新Kimi任务正常完成；第二轮正常流式输出时，通过应用“停止生成”按钮中止；第三轮显式新请求正常完成。会话 `01a17447-527f-7123-ab85-942f28a8e7ff` 最终为completed/interrupted/completed，23条本轮Native事实中的该会话占17条，不覆盖中断状态。
2. 正常⌘Q后，以同构建及已有暂停开关重开。Kimi显示“模型暂未启用”、不自动换模型，历史可读；显式键盘选择MiniMax后，新任务 `01a1744b-c762-70c2-b1ac-7a24fa81b5a3` 使用MiniMax-M3/high完成，新增6条Native事实。
3. 再正常⌘Q、恢复普通候选配置重开。新建任务默认K3.1，两个任务的模型、完成/中断状态和内容保存。重开与历史查询没有新增fixture请求，最终再次正常退出。
4. 只读检查既有unknown专家/媒体会话，提示与发送阻断保持，未点击恢复、切模型或重发；查看既有关闭计划和编辑表单后取消，没有保存、开启或单次授权。

本轮App账本共4次：Kimi/max三次、MiniMax/high一次；拒绝0、外部请求0。fixture正常shutdown返回204并退出。三个App实例均正常退出，没有进程信号或强杀。

## 三项独立最终结论

| 最终项 | 结论 | 依据与边界 |
|---|---|---|
| core_vertical | **NOT RUN（完整范围未满足）** | 当前文本、暂停回退、正常中断和历史子集通过，38号同源真实文本G2V继续有效；候选无自然可达旧K3会话/计划，旧K3完整App迁移/取消/重新授权未实测，真实图片/搜索/工具Provider覆盖未执行。不能改库制造场景或增加真实调用。 |
| accessibility_visual | **PASS（当前FEAT164可达界面范围）** | 新模型/显式MiniMax菜单、键盘Down/Up/Enter及Escape焦点返回、100%缩放下1180×760逻辑尺寸、亮暗主题、流式/中断/完成/unknown/暂停不可用状态及计划模型表单已观察。模型名称和关键操作可读。原浅色已恢复，普通重开恢复原1268×780窗口。旧K3自然迁移弹窗仍是core缺项，不宣称该弹窗已视觉实测；原生CUA无DOM执行桥，axe未运行，不声明完整WCAG合规。 |
| teardown | **NOT RUN（完整checkpoint结论未收口）** | 正常取消、三次退出、重开零补发、App/Host/Runtime/worker/adapter、监听端口及数据库句柄释放均通过。SQLCipher关闭与旧数据保护通过；Runtime三份WAL仍有未backfill的帧，完整关闭/checkpoint责任边界未定，不把资源释放子集等同完整teardown。 |

独立结果保存为 `s4l-final-core_vertical.json`、`s4l-final-accessibility_visual.json`、`s4l-final-teardown.json`；没有用一项PASS覆盖另外两项。

## WAL 发现与安全审计

首次数据审计使用“所有WAL必须为空”的过强断言而停止。实际观察：`logs_2.sqlite-wal` 4,165,352字节、`state_5.sqlite-wal` 2,669,792字节、`goals_1.sqlite-wal` 41,232字节，均无打开句柄；SHM的mxFrame分别374/648/10、nBackfill均0。旧基线已经存在这些WAL，本轮正常运行后内容变化，不能将它们当垃圾删除。

当前Runtime的StateRuntime使用WAL模式且提供异步close；app-server正常退出路径会排空后台工作并关闭threads，尚需进一步核实StateRuntime及日志池的最终关闭责任。这里只登记待验证假设，不把“未找到显式close”直接写成已证明的产品缺陷。

在所有候选进程正常退出后复制完整DB＋WAL＋SHM作为审计快照，使用SQLite只读连接执行integrity_check，三份均为ok。原DB/WAL及审计副本DB/WAL字节保持，未执行checkpoint、VACUUM、修复或删除。只读完整性通过说明数据可一致读取，不能证明checkpoint完成。修正审计后仅把资源释放/可读性子集记为通过，完整teardown继续未通过；首次发现和RCA均保留。

SQLCipher只读比较确认：旧计划六类记录、grant/run、失败草案、完成草案事实、unknown原操作、专家选择/操作以及上一轮真实42/50/8记录逐值保持。本轮没有旧计划next_at变化。新任务只有四条已提交终态，operation/runtime-turn各不重复。

## S1—S4 收口边界与下一步

- **S1**：当前local、真实本机boundary、canonical身份/暂停/显式MiniMax/历史纵向证据和freshness已具备，绑定当前H-F164-LOCAL；不再引用未完成的旧S1锁屏harness冒充当前结果。
- **S2**：当前local/boundary及来源已绑定；当前unknown只读UI证据补齐，但完整旧K3自然App迁移/恢复/取消纵向仍缺，slice保持未通过。
- **S3**：当前local/boundary及来源已绑定，既有计划只读/取消编辑保护已核验；旧K3自然计划迁移和重新授权纵向未实测，slice保持未通过。
- **S4**：当前基础、专家/媒体/辅助、旧loaded/终态与UI证据逐项绑定；完整TCONF04、核心最终验收及checkpoint闭环仍缺，slice保持未通过。

下一步先做零模型调用的Runtime正常关闭/checkpoint责任审计，给出一个最小、可证伪的关闭方案及回滚；若涉及新增Runtime核心或补丁范围，单独提交具体方案审批，不为消除WAL记录而手工checkpoint或删除文件。同时保留旧K3自然App场景清单，日常数据/入口切换另需范围确认。真实调用累计5/5已耗尽，不因仍有预算余额而继续调用。

本轮仍仅本地提交，不推送、不迁移日常库。保护审计确认497份既有dirty、1438份旧证据（含两个真实账本）、154份资源、7个日常数据库、406份旧bundle文件及5526份事前候选备份保持。完整FEAT-164保持IN_PROGRESS，尚未完成日常模型替换。


## 实际治理复核

当前claims、strict、G3/S1、元仓lint、53项元仓测试和7份Shell语法均通过。G3/S4与G4实际退出1，保留其明确未满足项；未为通过整体门禁修改required、invariant、断言、harness资格或批准记录。索引verified_at表示本轮来源/证据绑定核对时间，原始执行的started/finished时间与完整命令仍保存在s4l-driver-results及各result/log中。

本轮失败发现限于数据审计的过强WAL断言；没有产品测试失败或重试真实调用。将Runtime WAL与主库一起保留、完整性通过，不构成checkpoint策略的豁免。整项teardown继续NOT RUN，后续必须完成责任审计或经批准的最小正常关闭修复。

首次G4诊断还暴露来源集合遗漏：当前S1验收实际运行media组合，canonical依赖固定Connectors worker，原S1四仓集合未列该依赖。按实际执行补入其原7ea3df4来源，并同步S1—S3传递来源与TCONF索引；没有修改或放宽任何产品/测试内容。最终五仓集合与当前制品一致，Skills资源另由原精确pin绑定。首次诊断日志保留。
