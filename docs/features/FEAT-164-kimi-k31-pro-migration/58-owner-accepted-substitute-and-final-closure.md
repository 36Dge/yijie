# FEAT-164 S4AE：接受安全替代，收口S4与最终验收

2026-10-27。本轮依据Owner直接指令复审57号及当前实现，接受never-sent安全分层证据，完成本地S4/TCONF04与三项适用最终验收的判定。G4按本地代码完成范围核验；feature保持active，日常切换、发布及G5/G6保持pending。**本轮真实/本机模型HTTP均0，未启动App、未打开或迁移日常库，产品与Runtime核心/补丁零修改。**

## 接受的范围与保留的执行事实

Owner原话：“确认接受 never-sent 的安全分层替代证据，保留完整 App 正向取消未执行的事实，继续收口 FEAT-164 的 S4 与最终验收。”独立决策F164-S4AE-OWNER-SAFE-SUBSTITUTION保存在evidence/s4ae-owner-acceptance.json。

| 项目 | 原执行事实 | 本轮验收判定 |
|---|---|---|
| 原隔离自然unknown | 57实际App明确恢复安全拒绝、历史可读、禁发、原ID保持 | PASS_SAFE_REFUSAL；仍未恢复ready |
| never-sent Native正例 | 正常Repository API入队/领取/取消/关闭重开/相同回执；1 PASS、0 ignored；无sender/模型 | PASS，证据有效 |
| 生产前端消费链 | 实际Native结果经生产parser/composable/control；仅IPC transport重放；1 PASS、0 skip | PASS，接受的替代层 |
| 完整App/WebView正向never-sent取消 | **NOT RUN**，自然库无该正例 | **ACCEPTED_SAFE_LAYERED_SUBSTITUTE**；不改写原执行状态 |

替代只针对最后一项，不能推导出任何“missing即never-sent”、自动重发或取消未知操作权限。其它真实App主路径、计划、历史、模型切换和正常退出仍按原实际证据判定。搜索答案质量与外观专项仍OWNER_EXCLUDED，不记PASS、不延期补验。

## 当前实现与证据绑定复审

增量contract-impact=none：仅证据判定和治理文本变化，不修改wire、持久化/重放、生成物、模型配置、授权或Runtime补丁。完整需求原breaking分类保留。

只读脚本audit-closure.py实际执行exit0：46—57的12份索引共587个文件引用、另12份私有事实哈希一致；6个当前来源提交干净。测试4e1f1f980d148a6b46e21e68eb508caa4da5dae4与产品ea8763d仅3个登记的测试/说明文件不同，实际执行文件SHA与提交相同。56已证明310个业务实现文件与9f基线相等；日常入口新增分支和Host来源过滤分别沿51、54专属证据，不伪称全部实现逐字相同。

三套App各119文件、全部已记录Desktop/worker源码输入和Host/Runtime/worker/adapter制品哈希、大小、mode均相符；此处是文件只读复核，不是新canonical环境检查或启动。R1：4b0ec55；资格：179dbd1；日常prepare-only：c29f7e0。完整digest和回执在evidence/s4ae-closure-binding.json。当前Runtime11fd/r5 SHA283d12e不变。

S1—S3原9f/8cd/ca06及当前ea/4f/c5与共同Runtime/Connectors组成8项不可变commit并集，最终判定同时绑定该集合；旧证据的执行来源和时间不重写。时间戳表示本轮绑定与接受判定，不声称新做一次全范围E2E。当前真实文本/图片/工具证据不因本轮零调用而失效，也不追加相同模型回合。

## 与实现阶段分离的结构化审查

Codex本轮重新检查unknown恢复准入、never-sent事务和回执幂等、生产消费链导航/权限控制、计划退役和claim/send授权、Host原操作绑定、r5正常退出，以及回退和证据freshness。逐文件SHA和发现见evidence/s4ae-structured-review.json；这是Codex审查，不称独立人工评审。Owner此次确认仅记录其实际接受的替代方式，不虚构发布批准。

没有发现已接受本地范围内新增P0/P1产品问题，不需要产品或Runtime修复。需保持的限制：

- 原unknown缺Host回执，保留未决是安全结果；不能清空、换operation或重复恢复以“结清”。
- 完整App正向取消没有执行，替代层不证明WebView到Tauri的完整正向按钮路径；风险由本轮Owner明确接受。
- 57原“全行相等=false”保留。正常计划cursor/next、paused时间槽与Host updated_at变化由字段审计解释；不伪造“数据库完全没变”。
- 历史三次失败事件已有RCA后合格证据；三个两次失败armed记录原样保留，子代理/草案路由/reader修复证据31/32/33/48/56可追踪。没有开放三次失败熔断，不能把armed历史视为新增失败或删除原记录。
- 全仓CI和公开/生产资格未声明通过。当前功能定向测试、严格Clippy、lint/build/docs及生成资格按原精确范围使用，危险fixture不运行。
- 回退继续保留新兼容reader并暂停Kimi，不降库、不恢复旧K3 writer、不覆盖日常数据。

## S4与三项最终结论

| 判定 | 当前结果 | 证据边界 |
|---|---|---|
| S1—S3 G3 | PASS | 原实际来源、56当前回归与本轮绑定保持 |
| S4 G3 / TCONF-164-04 | PASS | 46—57真实调用面/生命周期，加Owner接受的never-sent替代 |
| core_vertical | PASS | 实际App主路径/跨组件持久结果与已接受替代，非新一次全量运行 |
| accessibility_visual | PASS | 仅现存模型/退役/错误/恢复/取消/计划授权业务状态；已排除专项不参与 |
| teardown | PASS | 57正常退出exit0、四Runtime库自然WAL0/integrity，业务数据保持；本轮零进程启动 |
| G4 Code Complete | PASS（本地已接受范围） | 结构化审查与实际治理门禁；不等于上线或完整交付 |
| G5/G6、日常迁移与启用 | pending / NOT RUN | 未授权执行，日常候选仅prepare-only |

全部AC按上述本地实现/验收范围PASS；没有将日常部署当成已经发生。机器字段保留full_app_positive_execution=NOT RUN，57原报告和原始日志不改。

## 数据保护、验证与提交

本轮基线记录12441份受保护文件、500份既有dirty文件（另含混合memory）与7份账本/历史快照。提交前后逐字核验；memory只精确追加本轮段落。累计真实HTTP13、45元cap、29.740299元保守累计与两份14.188544预占不变，不结算或覆盖旧账本。项目进程及验收监听均为空，无UI交接待答。

新只读来源脚本PASS；验收包audit-claims、strict、四片G3、G4及元仓lint、53/53测试、7份Shell语法全部exit0，精确命令见evidence/s4ae-governance-checks.json。首次audit-claims因新Markdown标题缺少要求的唯一HTML证据锚点退出1；补齐3个锚点后通过。原失败日志和原因保留，没有改校验器或产品。元仓检查只证明其真实覆盖范围，不等于全部业务仓CI。只有FEAT-164治理文件和memory专属段落进入本地提交，不推送。

## 后续边界

已接受范围内不再安排never-sent完整App补试、不重复点击原unknown、不恢复已移除的搜索质量或外观验收。日常候选准备资格已完成并保持；下一阶段若需要日常切换，先形成具体目标identity、完整备份/停止、只读预检、显式维护与回退范围，取得该数据动作授权后才执行。当前指令明确不迁日常库，因此本轮到本地代码与验收收口为止，整体不标delivery complete。

证据索引：evidence/s4ae-audit-index.json。完整私有保护清单与只读审计脚本保存在feat164-s4ae-audit-20261027；数据库、Key和完整用户内容不提交。
