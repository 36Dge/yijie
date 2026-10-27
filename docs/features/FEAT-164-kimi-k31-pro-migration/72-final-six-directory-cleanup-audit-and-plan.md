# FEAT-164 第72号：剩余六目录复审与最终清理清单

2026-10-28。**审计完成；可作为下一轮明确批准的候选清单。本轮未删除任何目录或worktree。**

权威机器清单：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/.local/cleanup-audit/20261028-final-six/final-cleanup-manifest.json`。SHA-256：`0322ee3b6eaed59db30cefe8fe8f2222c3ada25c019c096f9e11c1058e19827e`。

所有候选路径均在 `/Users/jack/Downloads/Personal_Info/CrossBSD` 下；不允许通配符扩展范围。删除顺序按调用目录先于依赖目录，恢复顺序相反。

| 顺序 | 精确顶层目录 | worktree数 | 当前du占用GiB |
|---|---|---:|---:|
| 1 | `/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-d5-candidate-20261027` | 4 | 4.78 |
| 2 | `/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-d4-history-fix-candidate-20261027` | 4 | 6.00 |
| 3 | `/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-d3-ready-candidate-20261027` | 4 | 6.47 |
| 4 | `/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-s4f-qualification-20261025` | 4 | 22.06 |
| 5 | `/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-s4e-qualification-20261025` | 4 | 20.64 |
| 6 | `/Users/jack/Downloads/Personal_Info/CrossBSD/feat164-qualification-20261025` | 6 | 13.60 |

合计26个worktree，当前du约73.55GiB；APFS共享、稀疏文件和归档保留会影响实际可释放空间，不承诺等额释放。

## 26个worktree的精确顺序

| 顺序 | 路径（相对于上述CrossBSD根） | 原仓 | 完整HEAD |
|---:|---|---|---|
| 1 | `feat164-d5-candidate-20261027/yijie-agent-host` | `yijie-agent-host` | `a3d8767add3855a28c18adbbd51251fae3520ac0` |
| 2 | `feat164-d5-candidate-20261027/yijie-connectors` | `yijie-connectors` | `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` |
| 3 | `feat164-d5-candidate-20261027/yijie-contracts` | `yijie-contracts` | `d5792d6aad18352ce8d1c5d510d345004cab3bd6` |
| 4 | `feat164-d5-candidate-20261027/yijie-desktop` | `yijie-desktop` | `39b0fbeb3a8c092768a7f0dfe64bd595d5e6be00` |
| 5 | `feat164-d4-history-fix-candidate-20261027/yijie-agent-host` | `yijie-agent-host` | `a3d8767add3855a28c18adbbd51251fae3520ac0` |
| 6 | `feat164-d4-history-fix-candidate-20261027/yijie-connectors` | `yijie-connectors` | `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` |
| 7 | `feat164-d4-history-fix-candidate-20261027/yijie-contracts` | `yijie-contracts` | `d5792d6aad18352ce8d1c5d510d345004cab3bd6` |
| 8 | `feat164-d4-history-fix-candidate-20261027/yijie-desktop` | `yijie-desktop` | `71e39c4e9fc38940c03b49f9b945fd4c5f6d987c` |
| 9 | `feat164-d3-ready-candidate-20261027/yijie-agent-host` | `yijie-agent-host` | `a3d8767add3855a28c18adbbd51251fae3520ac0` |
| 10 | `feat164-d3-ready-candidate-20261027/yijie-connectors` | `yijie-connectors` | `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` |
| 11 | `feat164-d3-ready-candidate-20261027/yijie-contracts` | `yijie-contracts` | `c5d138374c102f1a8a11e328a869ec8f91724efd` |
| 12 | `feat164-d3-ready-candidate-20261027/yijie-desktop` | `yijie-desktop` | `841f7c71ed3549fe02a70cff608cbbae713d6808` |
| 13 | `feat164-s4f-qualification-20261025/yijie-desktop/.local/skills-pinned-10c45be` | `yijie-skills` | `10c45bec29603b002e861e1499d5b4e684251af5` |
| 14 | `feat164-s4f-qualification-20261025/yijie-agent-host` | `yijie-agent-host` | `7927ee7b385cb5536c3647632d1bac0cb7c56fea` |
| 15 | `feat164-s4f-qualification-20261025/yijie-contracts` | `yijie-contracts` | `1b357cce0575c492f3715b316ee5f254051acf80` |
| 16 | `feat164-s4f-qualification-20261025/yijie-desktop` | `yijie-desktop` | `277f59eeef538d159e43bb1570767ca4f2f5f72a` |
| 17 | `feat164-s4e-qualification-20261025/yijie-desktop/.local/skills-pinned-10c45be` | `yijie-skills` | `10c45bec29603b002e861e1499d5b4e684251af5` |
| 18 | `feat164-s4e-qualification-20261025/yijie-agent-host` | `yijie-agent-host` | `b9155a3936c6ff5c6aedd52778d975de52b95d06` |
| 19 | `feat164-s4e-qualification-20261025/yijie-contracts` | `yijie-contracts` | `1b357cce0575c492f3715b316ee5f254051acf80` |
| 20 | `feat164-s4e-qualification-20261025/yijie-desktop` | `yijie-desktop` | `2fb898942cb4c3b81e34feb5169bd861340a4040` |
| 21 | `feat164-qualification-20261025/yijie-desktop/.local/skills-pinned-10c45be` | `yijie-skills` | `10c45bec29603b002e861e1499d5b4e684251af5` |
| 22 | `feat164-qualification-20261025/connectors-s4-source` | `yijie-connectors` | `1f157260d6dd339172712e1c649258902db45050` |
| 23 | `feat164-qualification-20261025/skills-s4-source` | `yijie-skills` | `595c927ae101d3d31c234f60565041eee0864680` |
| 24 | `feat164-qualification-20261025/yijie-agent-host` | `yijie-agent-host` | `cac2d4d7e1df02868a370e204959e1842c3362c3` |
| 25 | `feat164-qualification-20261025/yijie-contracts` | `yijie-contracts` | `eddc64f95d81c26ca1678cc648d177c081f7904d` |
| 26 | `feat164-qualification-20261025/yijie-desktop` | `yijie-desktop` | `a0a474333ba03186b36f30fa3ab86287abfc5c15` |

全部为detached且clean，均有原仓命名引用可达；无locked/prunable。3个嵌套普通Skills worktree先于各自Desktop父worktree。逐项命令数组、Git目录/index摘要、inode/device、归档与source manifest摘要、34个缓存根和反向依赖前置均见机器清单。

## 归档与Git保护

六份既有PAX/zstd归档共3,046,894,426字节，重新计算SHA通过，预期解包成员的源码/制品/链接内容复核通过。六树当前34,437项非缓存/制品材料已刷新内容和元数据清单。旧资格解包副本仅新增Finder .DS_Store并改变顶层目录mtime，预期成员无缺失；原归档及原源码未变。

新增的12个Finder .DS_Store（含target内2个）及目录元数据已保存为新的补充归档，不改旧归档：`finder-metadata-delta.tar.zst`，6,805字节；12文件/28成员内容和模式、uid/gid、mtime、flags、ACL及原属性通过。解包副本12个文件由macOS新增provenance属性，如实保留，未清除属性造绿。

原3份bundle和新集成3份bundle均重新hash/verify，已有独立bare恢复仓fsck通过。6个独立tip保留分支仍精确对应。Host/Contracts/Desktop的18个候选worktree历史被旧bundle覆盖；其余8个Skills/Connectors worktree由保留原仓develop引用保护，完整文件快照也已归档；不能把后两仓谎称包含在三仓bundle里。

34个再生缓存根共115,041条元数据，常规文件逻辑总量约85.59GB；缓存不承诺完整内容备份。全部6个canonical App与直接可执行产物已在非缓存归档中保全。除了12个已补归档Finder文件，没有新状态或源码差异。

旧qualification顶层的`s4c-before-build-20261025/.../runtime/.tmp/plugins`是一份完整历史Git副本，不是第27个注册worktree，也不是原仓。原件和归档恢复件fsck及refs一致，随精确顶层容器保留/处理，不追踪链接操作外部对象。

## 反向依赖与保留清单

12原仓+6候选全树不跟随symlink扫描：189,511目录、1,159,960普通文件、15,977链接；另扫描43,716个小型操作配置/脚本路径引用。没有原仓/新固定来源指向旧六目录的活动链接；4个文本命中均是候选自己的worker manifest。六树之间16条链接形成11条目录依赖边，已按拓扑安排顺序。Desktop入口、用户LaunchAgents、Dock固定/最近记录无旧路径。原仓Git worktree注册与历史文档是有意保留的管理/证据引用，不作活动依赖。

保留12个原仓、新来源`yijie/.local/daily-source/20261027-01`及其8个worktree、原Runtime r5、当前两入口及新激活绑定、原Native/Host/Runtime Home与凭据、所有旧新归档/bundle/独立恢复仓、六个保留tip、新集成分支、71号完整备份、账本与预占、本次审计与Finder增量。

只读检查时旧六目录无打开句柄；新入口/激活绑定/119个App文件/1228来源输入与71号一致。71号145证据文件和前轮125交付文件已重hash。本轮没有运行App、模型、workflow生命周期或打开日常数据库API。

## 获得批准后的最小删除规则

1. 先明确批准本清单摘要及6/26范围；重新核验上述所有摘要、引用、当前文件状态、inode/device、无句柄和反向依赖。期间有新变化先停止审计，不自动扩清单。
2. 按表中顺序，只对26条精确路径执行原仓的普通`git worktree remove -- <绝对路径>`；禁止`--force`、`git clean`、批量prune、reset或删除保留分支。嵌套worktree先于父级。ignored内容只有在归档/缓存边界复核后才允许被正常移除。
3. 每个顶层的注册worktree全部移除后，核验没有遗留注册，再按精确inode/device和已归档清单处理剩余普通容器；只用不跟随链接、遇错立即抛出的正常移除。不得chmod、ignore_errors或追踪symlink删除原仓目标。
4. 任一普通移除失败、活动进程无法正常退出、source/backup/权限/路径漂移即停止；不强杀、不更换二进制、不手工checkpoint、不删除或截断WAL。
5. 完成后核对26注册消失、六根缺席、12原仓及原改动/账本保持、保留引用和全部归档存在、新入口/制品和依赖仍有效。此时不自动重跑模型或启动服务。

## 删除后的回退

**即时安全选择**：现有新来源与两个入口不在清理范围。需要暂停Kimi时，先正常退出，使用「易界 AI（暂停 Kimi）.command」。这仍是同一版本，MiniMax保留，不应描述为所有模型暂停或旧版本回退。

**旧D5版本恢复**：删除后仅把旧.command恢复到桌面会指向不存在的目录，禁止这样宣称可回退。恢复需要另行明确数据/启动范围：

1. 核验六归档、Finder增量、旧D5回执/绑定、Git refs和bundle。先在新的私有空目录正常解包核对，不覆盖现有原仓或Home。
2. 保持原12仓/当前新来源；依赖先行按`qualification → s4e → s4f → d3 → d4 → d5`重建原六路径。逐条从精确HEAD登记worktree；不要把归档中的旧`.git`指针直接覆盖新登记文件。保留历史嵌套Git快照的独立归档边界。
3. 恢复已归档非缓存材料、canonical App/sidecar/worker、普通和专家Skills、回执/绑定及原文件模式；从冻结lock与缓存元数据恢复依赖。node_modules/Rust target大缓存未全部备份，必要时走canonical离线再生；若离线依赖缺失或需改工具版本，停止另报，不改回执hash或伪造旧环境。原D5环境含CARGO_BUILD_JOBS=4，新入口固定为2，分别以各自记录为准。
4. 以旧D5同源receipt进行prepare-only/reopen检查，核验当前原Home数据schema/兼容性、完整冷备份和workflow ready，建立实际零模型受限启动/正常退出资格。不是把71号新构建验收当作旧恢复验证。
5. 验证通过且正常退出后，保留当前两个入口，再恢复71号entry-rollback中的旧入口原件。不恢复旧数据库覆盖新数据、不降schema、不重跑D3、不删WAL。

本轮只验证归档可读、预期恢复内容、Git对象及新来源仍独立；没有实际删除或重建旧六树，没有实施清理后旧D5运行演练，也不承诺恢复耗时。所有材料仍在同一磁盘，不能视为异地灾备。

历史功能范围保持：never-sent已接受安全替代；完整App正向取消仍NOT RUN；搜索正确性和亮暗/键盘/最小窗口仍OWNER_EXCLUDED。

## 本轮证据与授权边界

[机器清单](evidence/final-six-cleanup-manifest.json)与[审计摘要](evidence/final-six-cleanup-audit.json)保存精确路径、完整HEAD、原仓引用、归档摘要和前置条件。私有逐文件清单、Finder补充归档及校验副本位于`yijie/.local/cleanup-audit/20261028-final-six/`。第71号验收仍属当时的实际结论；本轮只读复核其来源、制品、入口及证据，没有重新启动App或验证workflow即时健康。contract-impact=none，不改业务协议、存储、原Home、权限或Runtime。

本轮批准范围是审计、备份补全和清单落盘，删除授权仍为false。不得套用前次68目录/79worktree授权，也不得删除本报告列出的任何保留项。

独立收尾复核发现10个Finder文件的flags为UF_HIDDEN显示提示，已依据本机Darwin SDK确认；初始“flags必须全零”的观察假设已纠正，原记录保留，没有修改flags、权限或元数据。未发现immutable/append/nounlink删除限制。元仓lint、57项测试、claims、strict/G6文档语义与7份Shell语法通过；这些检查不代表实际清理或恢复运行已经执行。
