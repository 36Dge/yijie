# FEAT-164 候选决策、风险及阻断

## 当前D3状态（2026-10-27）

以[64](64-d3-controlled-migration-and-post-state-audit.md)和[当前矩阵](current-acceptance-matrix.md)为准：一次D3已完成，原日常Native SQL37→41，后态完整备份/67旧业务表保持审计通过，D3_COMPLETE_STOPPED。没有GUI/Host/Runtime或模型调用；D4未授权/执行，D5和local G5/G6待收口。旧阶段授权及未执行描述仅代表当时状态，不许可重复迁移或自动回退。

## 60号历史D1实施结果（2026-10-27）

当前权威为[60 D1完成与离线资格](60-d1-daily-binding-and-offline-qualification.md)。59号D1已获批并完成六文件Desktop修正、安全测试和新canonical prepare-only/同回执复核；Host/Runtime采用已批准原Home绑定，daily不再隐式workflow-up。真实日常绑定未生成、D2—D5未执行、模型HTTP新增0、Runtime核心/补丁未改。原CUTOVER-01/03已离线修复，日常现场/启动资格仍无授权，G4不自动晋升。58接受的never-sent替代保留，完整App正向取消仍NOT RUN。

下方59及更早“尚未实施D1/原入口缺陷”按当时来源解释，不再作为当前D1未完成项。下一步仅在批准D2后进行完整冷备份和副本只读预检，不顺带迁移或启动。

## 59号历史日常切换边界（2026-10-27，S4AF）

以[59 日常切换方案](59-daily-cutover-minimal-plan-and-authorization.md)为当前部署权威。源码复审发现daily launcher将Host/Runtime Home改至候选新目录、与原Native日常库缺连续性；正常启动还可能隐式workflow迁移及恢复自动计划。日常activation为NO_GO，当前G4重新pending，先提限定部署入口修正及离线资格，尚未获准实施。58的已接受本地S1—S4/final证据与never-sent替代保持，完整App正向取消原执行仍NOT RUN；不是重新跑失败或取消Owner接受。

本轮仅方案和治理，无产品/Runtime改动，无日常数据访问/备份/预检/迁移/启动，无模型调用。阶段顺序为D1入口修正→D2完整冷备份与副本只读预检→D3一次Native维护→D4首次受限启动及退出核对→D5确认日常启用；D1—D5均未自动授权，具体边界见59。以下早期状态按各自时点解释。

## 58号历史已接受范围（2026-10-27，S4AE）

以[58 安全替代接受与最终收口](58-owner-accepted-substitute-and-final-closure.md)、feature.yaml和[当前矩阵](current-acceptance-matrix.md)为准。Owner明确接受57号never-sent正常Native API与生产消费链的安全分层替代；S4/TCONF04及三项适用最终验收按该方式收口，G4为本地代码完成。**完整App正向never-sent取消的原始执行状态仍为NOT RUN**，没有改写为已执行。原自然unknown缺Host回执，安全拒绝重发通过，原记录仍未恢复ready。

本轮仅只读审计和治理更新，真实/本机模型HTTP新增均0；产品、Runtime核心/补丁、来源锁不变。不启动或迁移日常库，日常候选保持prepare-only，G5/G6及正式交付仍pending。搜索答案正确性、亮暗/键盘/最小窗口专项保持OWNER_EXCLUDED，不恢复为待办。以下早期阶段记录按原时间和来源解释；本节覆盖其中过期的推进顺序、预算授权和“当前未通过”描述。

当前权威见[46](46-independent-legacy-app-qualification.md)及[当前验收矩阵](current-acceptance-matrix.md)。方案实施已批准；只本地、0新增真实模型调用，日常库迁移和新Runtime核心/补丁范围仍需单独确认。G2A与r4最小真实G2V已有历史资格，完整产品完成门禁仍pending。

下列方案已由Owner当前实施指令确认；实际源diff的Consumer审查与后续Gate另行记录。需求/技术/Reviewer/发布Owner均为段成威。

| 决策 | 推荐与取舍 |
|---|---|
| DEC-01 身份 | 新profile；拒绝旧profile偷偷指新模型和硬删所有历史旧值 |
| DEC-02 治理 | production_hardened/local；重要持久数据触发，运行环境profile保持 |
| DEC-03 协议 | 原Responses/max/1M及最小Runtime修订；不改API、不选highspeed、不夹带预算提升 |
| DEC-04 激活 | reader+停派发准入先就绪，再迁移和激活；不能仅靠最后Host拒绝 |
| DEC-05 unknown | 保留未知；明确恢复原目标resume，重新验证所有门禁；不新造只读线程设置协议 |
| DEC-06 取消 | 补普通/市场never-sent取消的最小领域能力；不能借删除chat |
| DEC-07 回退 | 可读两代且能独立停新Kimi的兼容构建/前向修复；不静默复活旧K3 |
| DEC-08 截止点 | 正常收敛所有受管模型工作后定义cutover；不以父thread idle代替全部工作结束 |

沿既有权威边界，不新建身份/权限/调度主状态；若后续选择新Runtime协议或跨仓职责变动，回G2及适用ADR评审。

## 当前事实与未知

Fact：模型替换、显式迁移/恢复/never-sent取消、计划退役和全调用面接线已实现；r5关闭修复与43号就绪修复已落地。44/45号有自然旧数据的领域/入口证明，尚不等于完整App升级流程。S4S新增固定独立验收身份，原SQL41候选无需再次结构迁移。

只读事实：1条unknown是原K3.1→MiniMax模型选择；2份occupied授权对应terminal/completed且native_terminal释放的运行，无reservation。它们不是全局执行占用，不能为了通过维护门禁而清理/退款/重发。原14.188544元unknown费用预占是独立账务事实。

Unknown：最终来源的全部AC与三项final、日常切换前的完整现场状态及真实供应商扩展场景资格。r4已验证账户最小文本主路径；不能继续笼统称账户完全未验证，也不能据此声称r5真实资格通过。

Assumption：固定离线身份可用正常旧App自然生成所缺数据；只有实际UI、受控迁移和重开证据才可转为Fact。锁屏/来源失败保持NOT RUN或FAIL。

## 初始设计阶段阻断台账（历史）

以下保留立项时问题分类，当前解除情况以46号和当前验收矩阵为准；其中“未实现/未构建”不再描述当前产品。

| ID | 尚缺事项 | 解除要求 |
|---|---|---|
| BL-01（已解除） | Owner已确认方案并要求实施 | G0/G1/G2记录用户当前指令；不推定Git/发布和付费许可 |
| BL-02 | 三层身份契约及方向兼容仍是候选 | G2审阅；G2A真实源diff、版本/full commit/digest、全部consumer评审 |
| BL-03 | unknown恢复、never-sent取消、准入/激活资格未实现 | 先审设计，再安全状态测试、G2V及slice证据；不称现成机制 |
| BL-04 | 三表/Host状态迁移及兼容回退无运行证据 | 先合成库/正常重开证明，再获准操作日常库；不得先迁后补 |
| BL-05（部分解除） | 新Runtime和独立Contracts投影已构建校验；Host/Desktop候选未产生 | 仍需源候选不可变commit与G2A，再进入最小纵向候选 |
| BL-06 | 真实模型/工具/图片/Guardian/标题无本次额度 | 单独批准用户回合、HTTP、工具次数、tokens/费用上限及停止条件 |
| BL-07 | 加固全门禁未完成且当前local | G5/G6保持pending；不改exposure或借旧D4制造关闭 |

三次同点失败启用append-only RCA，不机械第四次重试。禁止强杀、权限破坏、攻击fixture、可执行伪装/危险归档；若门禁只能靠禁止行为证明则NOT RUN并记录影响，不减弱断言伪造PASS。保留既有工作树改动与日常App；当前仅实施未激活源候选。

## S4M候选决策（未批准）

推荐所有者有序关闭，拒绝以末尾flush或手工checkpoint掩盖任务所有权缺口；详见40的取舍、实施面、超时保护、四池验证及回滚。审批尚未取得，保持现有Gate。
