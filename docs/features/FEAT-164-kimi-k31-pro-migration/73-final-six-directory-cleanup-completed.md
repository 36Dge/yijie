# FEAT-164 第73号：旧六目录及26个worktree清理完成

2026-10-28。**按Owner本轮明确批准，第72号精确清单中的6个旧目录、26个worktree已全部正常移除；CrossBSD根下已无`feat164-*`目录。12个原仓、新日常来源与两个入口、归档及bundle、已有改动、旧账本和预占均保留。** 清理后同构建prepare-only检查通过，未启动App、调用模型或推送。

本报告更新当前目录与回退状态；第71号的“旧六目录保留”和第72号的“尚未授权/未删除”仍保留其历史时点含义。FEAT-164功能范围和完成结论不因目录清理改变。增量contract-impact=none：只退役已完成入口切换的闲置worktree与容器，不改产品、Runtime、协议、存储、原Home或权限边界。原脏主工作区没有切换分支或合并；当前干净集成来源仍在原仓内固定目录。

## 授权与清理范围

批准的机器清单SHA-256为`0322ee3b6eaed59db30cefe8fe8f2222c3ada25c019c096f9e11c1058e19827e`。未修改该历史清单，新增执行授权和日志单独绑定它。

以下路径均相对于`/Users/jack/Downloads/Personal_Info/CrossBSD`，按此顺序完成：

| 顺序 | 精确旧目录 | 正常移除worktree数 |
|---:|---|---:|
| 1 | `feat164-d5-candidate-20261027` | 4 |
| 2 | `feat164-d4-history-fix-candidate-20261027` | 4 |
| 3 | `feat164-d3-ready-candidate-20261027` | 4 |
| 4 | `feat164-s4f-qualification-20261025` | 4 |
| 5 | `feat164-s4e-qualification-20261025` | 4 |
| 6 | `feat164-qualification-20261025` | 6 |

26条绝对路径、原仓、完整HEAD、inode/device与移除命令沿用[第72号清单](evidence/final-six-cleanup-manifest.json)。3个嵌套Skills worktree先于父Desktop；调用方目录先于其依赖目录。逐项普通`git worktree remove -- <精确路径>`成功后核对注册消失，顶层没有剩余worktree、余项与归档一致且无占用，才用不跟随链接的fd-safe正常移除处理容器。没有`--force`、全局prune、git clean、reset、chmod或错误忽略；原仓其他注册包括无关历史记录保持。

## 重新核验与Finder差异处理

最初预检检测到第72号之后Finder产生的`.DS_Store`变化，立即停在删除之前。完整差异审计确认：17个新增、4个修改的Finder元数据文件及相关目录时间/大小变化；无源码、业务状态、ACL或其他内容漂移。21个文件具有普通Finder文件头，均位于已批准的六根内。

另建`finder-supplement.tar.zst`保全这21文件及祖先目录元数据，共44成员、10,291字节，SHA-256：`ac3973a60b238c8c2598243f4dd6208a01483a6e93ed40866c9617bf44eaf99b`。独立私有解包的内容、模式、uid/gid、mtime、flags、ACL和原xattrs通过；macOS在21个恢复副本增加provenance属性，如实记录，没有清除或修改源属性。原六归档、第72号Finder增量及原清单保持不变。

同一授权路径范围内完成补充保护后，刷新34,449条非缓存/制品材料、34个缓存根的115,046条元数据并重新通过严格比较，才开始删除。没有因差异自动扩展清单或把不一致直接当作通过。再生缓存仍不承诺完整内容备份；canonical App和直接产物保全边界沿用第72号。

删除前重新验证六份原归档、原3份与新集成3份bundle的hash/verify及独立bare恢复仓fsck；6个独立tip引用与所有候选HEAD命名引用保持。Host/Contracts/Desktop共18个worktree历史由旧bundle覆盖，其余8个Skills/Connectors仍由保留原仓develop引用保护，不谎称它们已包含在三仓bundle。完整历史plugins Git副本的原件和归档恢复件也通过fsck；它不是额外注册worktree，随qualification容器处理。

12原仓和六候选的扫描未发现活动外部反向依赖；原16条候选内部链接与拓扑顺序一致。Desktop入口、LaunchAgents和Dock检查无旧路径。每组、每个worktree执行前复核文件、Git引用、索引、状态、句柄和进程路径；全部26次普通Git移除及6次容器移除成功。

## 清理后的日常入口与保护状态

保留来源：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/.local/daily-source/20261027-01`及8个干净worktree、指向原Runtime的来源引用。保留两个桌面入口：`易界 AI.command`和`易界 AI（暂停 Kimi）.command`；启用配置及原数据Home不变。

清理后执行canonical `run-local-demo-fast.sh --packaged --kimi-k31-daily --prepare-only --reopen`，固定原`CARGO_BUILD_JOBS=2`、worker来源及离线工具环境，退出0。119个包内文件、1228个来源输入、回执、schema2启用绑定及两个入口hash与第71号一致；8个新来源worktree在检查后仍clean。此项验证同源回执、投影和入口准备，不是重新启动App/UI，也不代表workflow即时健康。第71号3次真实启动/正常退出仅作为历史运行资格。

清理后再次扫描12个原仓：174,582目录、1,026,712普通文件、15,607链接，38,107个小型操作文本文件；活动旧目录链接和操作配置引用均0，扫描异常0。历史文档、归档和Git管理事实按证据用途区分，保留不删。

12个原仓的HEAD/分支/远端/index及原有改动保持，26项注册准确消失，其余注册保持。510份保护文件（含账本/预占，桌面入口按第71号批准的新hash）保持；六归档、六bundle及两轮Finder补充归档复核通过。后续本地治理提交只增加本报告与脱敏结果，不混入旧改动。

执行期间观测文件系统可用空间增加39,270,260,736字节，约36.57GiB；这是当时整卷可用空间差值，不是精确物理回收量，不把原du占用或逻辑字节数等同于释放量。

## 清理后回退与验收边界

当前两个新入口不依赖已清理目录。需要暂停Kimi时先正常退出再使用暂停入口；MiniMax仍保留，这不是旧版本回退。

旧D5恢复必须遵守第72号顺序：先校验归档、两轮Finder补充、引用及bundle，在私有空目录核对；依赖先行重建精确六根与26个worktree，不能直接覆盖旧`.git`指针；还原保全材料、从冻结锁及缓存清单恢复再生依赖，然后核验旧回执、当前Home兼容性、完整备份和workflow ready，完成新的零模型受限运行资格后才选择旧入口。只把旧`.command`拷回桌面会指向缺失目录，不能当作可用回退。

不覆盖新日常数据、不降schema、不重跑D3、不手工checkpoint、不删/截断WAL。未实际重建旧六树或进行删除后的旧D5运行演练；所有保全材料仍在同一磁盘，不是异地灾备。

本轮0新增模型HTTP、0推送、0App启动、0workflow生命周期操作，未打开日常数据库API。never-sent安全分层替代仍为Owner接受；完整App正向取消仍NOT RUN；搜索答案正确性、亮暗/键盘/最小窗口专项仍OWNER_EXCLUDED。清理不重新扩大或改变这些验收口径。

脱敏结果：[最终清理执行证据](evidence/final-six-cleanup-execution.json)。完整逐项日志、授权、Finder差异与补充归档、当前快照、入口日志、失败前置记录和后态位于`yijie/.local/cleanup-execution/20261028-final-six/`；旧归档`FEAT-164-preservation-20261027/`和第72号私有审计目录完整保留。治理检查结果另附执行证据目录，不以文档门禁替代运行验收。

治理复核已通过：元仓lint、57项测试、FEAT-164 claims、strict/G6文档语义及7份Shell语法。它们仅证明所列治理检查；本轮实际入口验证范围仍是prepare-only，不改写历史App/模型验收事实。
