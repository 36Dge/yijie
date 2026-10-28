# FEAT-164 当前验收与来源矩阵

2026-10-28。原S1—S4/D1—D5完成范围保持；已实现**直接从原`CrossBSD/yijie-desktop`实际源码构建运行**，不转调`.local/daily-source`。构建运行以[76](76-primary-workspace-execution.md)、[77](77-primary-system-quit-root-cause-and-plan.md)及[机器证据](evidence/primary-workspace-execution-result.json)为准；随后[78](78-old-daily-source-retirement.md)已按Owner授权清理旧`daily-source/20261027-01`及8个worktree，完整归档/bundle保留，清理后来源和入口只读检查通过。第71—74号完整矩阵保存在[历史快照](current-acceptance-matrix-history-report71-74.md)，原执行时间、失败、接受替代和Owner排除不改写。

第79号补充：旧目录清理后，同一generation已完成一次零模型canonical启动、8会话/11轮实际UI历史、定时任务历史保护及正常⌘Q退出。该次完整后态通过，停止代123→124，活动WAL/SHM0；原锁屏跳过的历史界面项已补齐。第76—78号矩阵原文保存在[历史快照](current-acceptance-matrix-history-report76-78.md)。

## 当前完成及验收边界

| 分类 | 结论 |
|---|---|
| 本轮已完成 | 501项原工作可恢复保全；已审基线在原主目录成为活动源码；primary v3及独立新输出、canonical构建、来源/回执核对；真实D4暂停/D5启用/D5暂停三轮ready、只读模型目录、正常退出与完整后态通过。 |
| 新来源历史界面 | PASS，见[79](79-post-cleanup-app-history-acceptance.md)：实际读取8会话/11轮、2附件、命令详情和旧计划；原76锁屏跳过仍为历史事实，未改写原结果。 |
| 已接受替代 | 原57/58 never-sent安全分层替代保持，完整App正向never-sent取消仍NOT RUN；不扩展该接受为本轮UI已执行。 |
| 已移除 | 搜索答案正确性/指定页面命中/确定回答质量，亮暗/键盘焦点/最小窗口专项均OWNER_EXCLUDED，不恢复为待办或PASS。 |
| 仍保留 | 模型/退役/恢复/计划授权、搜索sources安全传递、Key与审批预算、旧unknown事实及正常退出。 |
| 范围外 | public/cloud/多人/签名/完整跨平台发布及进一步目录清理。78仅清理已审旧daily-source；完整归档、bundle、12原仓和原数据保留。 |

## 当前来源与仓内入口

| 对象 | 当前事实 |
|---|---|
| 实际源码 | `/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop`；同父目录原Host/Contracts/Connectors/Skills/Runtime；无活动Desktop源码复制 |
| 分支与原工作 | 五仓`feat/feat164-primary-20261028`；原分支未移动，254源码WIP路径在`retained/primary-wip-20261028-01`及bundle，4缓存单独保全，不把它们自动启用 |
| Desktop | `24a231f96f08ed077e53f9bd73a2aac93ee6cba8` |
| Contracts / Host | `d5792d6aad18352ce8d1c5d510d345004cab3bd6` / `7309101726dcecd48b2caa02401cfcdd6126f1fb` |
| Connectors / 专家Skills | `8e62101ff8ca94c2f9e12f4e415f20df41a7deed` / `595c927ae101d3d31c234f60565041eee0864680` |
| Runtime | 原仓`11fd4504c28afd0f65c6f5f62a6b5328dd437f5a`、r5；核心/补丁未改 |
| 历史资源pin | 普通Skills10c45be与Host1b7bfd1/96b1fa1继续独立固定，不混用专家来源 |
| generation | 原Desktop`.local/builds/primary/20261028-02`，仅制品/回执/授权 |
| App SHA | `c2f5cba634bf4a8d567b534e798d86a076e5a53d98183afd5ce780f8c40a3629`；119包内文件 |
| Receipt SHA | `28141579143c6da10ac47f11a164e7394cec83ae3559aa9dd50db5057c4cd915`；1230输入 |
| v3启用绑定SHA | `169d6713703abaaf35ad84fdcdbdc0778159fec0a18cf50f1bd4a339ad80a87c` |
| 正常入口 | 在原Desktop运行`pnpm daily:open --generation 20261028-02`；真实catalog确认Kimi K3.1 Pro/max可用、旧K3不在活动目录 |
| 暂停入口 | 同命令追加`--pause-kimi`，先正常退出；真实catalog确认Kimi暂停、MiniMax可用 |
| 原数据与服务 | 原Native SQL41、Host11、Home/身份/权限保持，D3未重跑；79依此前65授权恢复同一workflow栈，四卷备份/原卷保留、既有幂等迁移及正常凭据轮换完成，六primary真实ready |

原桌面两个.command与顶层旧preservation在76开始前已缺失，76/78未删除/恢复它们；不能再把旧路径写成当前可用入口。新归档及五仓最终bundle已独立恢复校验。旧daily-source已由78清理；旧来源仅保存在完整归档和Git引用/bundle中，需按78恢复并重新审定，不参与当前构建/运行。

## 新来源实际证据

79新增一次清理后canonical启动与正常⌘Q退出，UI历史已实际通过；71张Native表仅停止代123→124，其余原业务行/授权、Host值、Runtime业务/rollout保持，Runtime日志追加608行。完整后态17,401文件/523,139,568字节；模型HTTP0、provider metadata HTTP0、业务工具0，App已停止、锁与句柄释放。workflow恢复前四份停止态卷副本保留，恢复和up仅追加两条正常principal审计，其余业务事实保持；六primary在App退出后仍健康。详细来源/时间和UI证据见[79](79-post-cleanup-app-history-acceptance.md)。下段76记录保持其当时数字。

初始generation01系统Quit绕过自定义ExitOwner，退出资格FAIL，原记录保留。仅Desktop标准`aevt/quit` handler接入既有清理链后独立构建generation02；三轮正常退出日志/停止代120→123/活动WAL和SHM0/无进程句柄均通过。遗留WAL由新App正常打开和退出处理，未手工checkpoint或删除。Native71表仅停止代追加，Host所有持久值、Runtime业务/rollout、旧历史与授权不变。最终完整后态17401文件/522889712字节。

本轮新增真实模型HTTP0；初始失败运行有既有provider只读metadata HTTP3，最终三轮0，业务工具0。七份旧账本及两预占保持，不因本轮检查补结算。当前App已正常退出，正常入口下一次可明确启用Kimi；暂停参数不是永久修改默认入口。

19项同源检查、104项安全聚焦测试、Rust Clippy/fmt、脚本语法、聚焦eslint与文档构建通过。历史危险/攻击/权限破坏/强杀fixture未执行。治理检查结果见76末尾；没有将本机资格扩大为公开发布。

以下AC及阶段判定保留原执行来源/时间，新的来源绑定和系统退出增量由上述本轮证据补充；不把旧UI或旧模型调用冒充本轮执行。

## 验收判定

| AC | 当前判定与来源 |
|---|---|
| 001 活动目录/参数 | PASS；原S1/49/56/57及67实际日常K31可用/默认、K3不在活动目录 |
| 002 受管配置 | PASS；原S1/51/56、63精确前身、66 Host11正常准备；67保持原Home及受审来源 |
| 003 SQL兼容 | PASS；46/51/56正常旧库组合，64日常37→41；66/67原业务行保持，不重跑迁移 |
| 004 原thread/恢复 | PASS；原46/56/57限定结果及66的8会话完整读取、67已有答案；旧unknown状态不伪造恢复 |
| 005 退役/取消 | PASS，含已接受替代；57安全分层与58 Owner接受；完整App正向取消仍NOT RUN |
| 006 计划/授权 | PASS；原46/51/56及66/67旧计划不复活、已删除目标禁重跑；新日常启用不是计划grant |
| 007 全调用面 | PASS；48辅助/子代理/压缩，52专家媒体，56/58精确绑定；66/67相关源与canonical完整media装配保持，无新增模型回合 |
| 008 响应语义 | PASS；原49/53/54/55/56证据，66补format5只读兼容；搜索答案正确性OWNER_EXCLUDED |
| 009 Key/审批/预算 | PASS；原共享Key/原生权限及逐次授权不改；7账本/两预占保持，67新增模型HTTP0 |
| 010 生命周期/状态 | PASS，含既有替代；66关闭/历史、67三次正常退出/完整后态/活动WAL0 |

## 最终证据与治理范围

| 项目 | 判定及边界 |
|---|---|
| core_vertical | PASS；既有真实业务结果及58接受保留；66真实历史修复、67日常入口增量资格，不伪造新模型执行 |
| accessibility_visual | PASS于现存业务状态范围；67 K31启用/暂停/恢复、旧模型保护实测；外观/键盘/最小窗口专项OWNER_EXCLUDED |
| teardown | PASS；67三次⌘Q退出0、锁句柄释放、业务旧行保持；活动DB WAL/SHM0、历史备份WAL保留 |
| S1/S2/S3/S4 G3 | 原已接受PASS与执行时点保留，新增来源/引用独立关联66/67事实 |
| G4 / G5 | PASS；本次限定个人本机范围；启用前单独验证与提交7a2b7c3，不改exposure为public |
| G6 / D5 | PASS；已批准范围实际启用、暂停回退、同入口重开和完整后态交付观察完成；不是签名/云端/公开发布 |

完整App正向never-sent取消仍NOT RUN；Owner接受的安全分层替代不冒充完整App。搜索答案正确性、亮暗/键盘/最小窗口已从本需求移除，记OWNER_EXCLUDED。所有原失败日志与来源保持。


## 保全与后续

此前两轮74个旧顶层目录清理结论仍是73号历史事实。78另按精确清单清理`daily-source/20261027-01`及8个worktree，12原仓、所有保护引用、旧账本/预占及新备份/bundle保留；缺失更早归档的事实不被新备份掩盖。旧daily-source完整归档已独立恢复75,547项，清理后19项来源和1410项输入/制品核对通过，原日常数据保持。恢复未采纳WIP或旧来源须从保护提交/bundle/归档按需求审阅，不直接整份启用；回退先正常退出、备份和验证兼容来源，不降schema、覆盖日常库、重跑D3或清空WAL。

原主目录构建运行与清理后实际历史/退出验收已完成，没有待补的新来源历史界面项。原完整App正向never-sent取消仍NOT RUN且已有接受替代，永久排除项不重新安排。未来开发改变主源码后应canonical新generation构建、资格及显式绑定，旧回执不能自动刷新。
