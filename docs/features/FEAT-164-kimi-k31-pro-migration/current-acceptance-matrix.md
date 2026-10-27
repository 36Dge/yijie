# FEAT-164 当前验收与来源矩阵

2026-10-28。S1—S4及D1—D5在ADR-0022个人Mac范围完成，当前来源/日常入口资格见[71](71-original-repository-daily-entry-consolidation.md)，旧目录清理及保护后态见[73](73-final-six-directory-cleanup-completed.md)。本矩阵同步实际来源与已接受范围，不新增运行或发布资格；原67/69及切片执行记录保持历史含义。

## 完成状态与验收范围

| 分类 | 当前结论及严格边界 |
|---|---|
| 已完成 | S1—S4及D1—D5在ADR-0022单Owner个人Mac范围完成，后续C1—C5原仓来源/入口收敛与旧目录清理完成；模型替换、配置/历史/授权保护、实际启用调用面、三类适用final与本机G4/G5/G6有对应证据。PASS按下列替代和排除后的范围解释，不表示每项都做过完整App实跑。 |
| 已接受替代 | 仅完整App/WebView正向never-sent取消采用57/58中Owner接受的Native持久取消、重开、同回执及生产parser/composable/control分层证据；原完整App执行仍NOT RUN。适用于AC-005/010及S4/final，不替代其它主路径或权限不变量。 |
| 已移除 | 搜索答案正确性、指定页面命中及确定回答质量；亮暗、键盘/焦点、最小窗口专项。均为OWNER_EXCLUDED，已从本需求移除，不是延期或PASS，不重新安排。 |
| 仍保留的要求 | 搜索接线及实际返回sources的安全传递、原生事实如实呈现、模型/退役/恢复业务状态、Key/审批/计量和正常退出；未随质量或外观专项移除。 |
| 范围外或保留事实 | public/cloud/多人/签名发布及完整跨平台资格不由本机结论覆盖；自然unknown仍按原事实阻断，旧账本和两份预占不清零。workflow需实际ready，当前8个固定来源worktree、原Home及新回执须保留；旧顶层候选已清理，不能承诺依赖永久健康。 |

验收分类延续[70](70-document-scope-reconciliation.md)；当前来源同步见[74](74-current-consolidation-document-sync.md)。原报告及失败/未执行记录保持原日期、来源和状态；当前适用范围内无新增功能实施待办。

## 当前来源与入口

| 对象 | 当前固定事实（第71号资格、第73号清理后复核） |
|---|---|
| 来源根 | `/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/.local/daily-source/20261027-01`；8个干净worktree连接原仓Git对象库 |
| 本地集成分支 | Host、Desktop、Contracts原仓的`feat/feat164-consolidation-20261027`；原脏主工作区未切换，未推送 |
| Desktop | `a211c2d04def6091352c7b3674a49355cdee18ed`；与旧D5产品代码相同，仅冻结Host来源锁及生成资格pin更新 |
| Contracts / Host | `d5792d6aad18352ce8d1c5d510d345004cab3bd6` / `7309101726dcecd48b2caa02401cfcdd6126f1fb`；Host保留原d49c005测试，运行实现与旧D5一致 |
| Runtime | `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a`；原仓r5 SHA `283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e` |
| Connectors / 专家Skills | `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` / `595c927ae101d3d31c234f60565041eee0864680` |
| 必要历史来源 | 普通Skills `10c45bec29603b002e861e1499d5b4e684251af5`，Host `1b7bfd1`、`96b1fa1`独立固定来源；不混用普通与专家版本 |
| App | SHA `80b9514a9a389ed023286eee6f10021efc14caa242677b6af3d22ca192042f4e`；119包内文件 |
| Receipt | SHA `86de538f8bd6fc49c53a48d7cc3a9942c74a0c4b45d6763fc566602aa7420a8a`；1228源码输入 |
| 启用绑定 | schema2；SHA `57edb7a822ee0a9658c18be4efecd5c11bd74cf98689fa79c3eebb42f7aea37c`，位于当前Desktop的`.local/feat164-daily/activation/binding.json` |
| 正常入口 | `/Users/jack/Desktop/易界 AI.command`，当前新来源K31启用 |
| 兼容暂停入口 | `/Users/jack/Desktop/易界 AI（暂停 Kimi）.command`，正常退出后使用同一新来源，仅暂停Kimi、保留MiniMax |
| 原数据 | Native SQL41/Host11/原Runtime Home保持；71号历史、附件、已删除计划和grant保护通过，未重跑D3 |

第71号独立验证新位置的完整备份、历史、正常启动/退出与两个入口；第73号在清理后验证同构建prepare-only及保护后态。以下原AC/Gate证据保留原执行时间和来源；新来源与旧D5运行代码等价，新增绑定不把旧G2V或完整App未执行项伪造成新的实跑。

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

## 清理后态、数据与后续

[73](73-final-six-directory-cleanup-completed.md)已正常移除最后6目录/26 worktree，两轮共74个旧顶层`feat164-*`目录不存在；活动旧路径依赖为0。12原仓、当前8个固定来源、原改动、6个独立tip、归档/bundle、账本和预占保留。Host/Contracts/Desktop的产品tip已进入原仓集成祖先；3个验收工具/测试专属tip仍保留于引用和bundle，不混入日常构建。原主工作区未合并到集成tip，后续开发应识别当前来源边界。

最新实际完整后态属于[71](71-original-repository-daily-entry-consolidation.md)：17,400文件/522,551,359字节，Native67业务表、Host全部值、Runtime业务行/rollout保持，正常日志追加386；模型HTTP0、metadata HTTP9、业务工具0。三轮实际启动/正常退出属于71，清理后prepare-only属于73；本次文档同步没有重新启动、开库或复测workflow。其ready及App停止状态仅是71号观察时点。累计13模型请求、45元上限、29.740299保守累计及两份14.188544预占保持原记录，不据文档补结算。

暂停使用当前新来源的暂停入口；旧.command不能直接恢复运行。旧D5恢复须按[72](72-final-six-directory-cleanup-audit-and-plan.md)/[73](73-final-six-directory-cleanup-completed.md)从归档、两轮Finder补充、refs/bundle重建精确路径和worktree，补齐再生依赖、兼容性、完整备份及新运行资格；未做删除后重建运行演练，不覆盖新数据或清空WAL。归档同盘不等于异地灾备。

当前批准范围内无功能或目录清理待办；公开/云端/多人/签名及跨平台发布不在此范围。完整App正向never-sent取消仍NOT RUN且已接受替代；Owner排除项不重新安排。旧矩阵原文保存在[第67/69号历史快照](current-acceptance-matrix-history-report67-69.md)，历史报告和失败证据保持。
