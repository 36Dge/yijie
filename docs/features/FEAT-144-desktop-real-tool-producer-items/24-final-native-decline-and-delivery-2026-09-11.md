# FEAT-144 最终原生拒绝复验与本地交付

真实原生拒绝及普通重开已完成，九项活动Must已逐项复核；AC-004继续为用户排除，不实现、不验证、不算PASS。最终D4门禁结果记录在本报告末尾及机器证据。本次仅本地交付，不代表远端CI、公开发布或生产验收。

## 最终来源与兼容

| 仓库 | 完整提交及范围 |
|---|---|
| Contracts | `811f38d6b104fa18477107e7ac91a85e19c445d1`，独立原生当前状态只读端点，旧history/权限wire不变 |
| Host | `0e47766f494977c94bfea0e89cfbdf45a7fafa2b`，复用固定thread/read，不resume、不写状态 |
| Desktop | `7abf89e84ffcbe56360d8c9943390e0640d9e239`，精确本地条件＋当前原生状态确认，旧不确定投递保留 |
| Codex | `6c1ad767f0997845b8258a1c452fd4eb7577579f`未改；实际0.144.6 binary SHA `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d` |
| 元仓 | 验收文档与本地提交状态独立记录；本报告所属Git提交可追溯，不填造自身提交号 |

当前native/MCP/权限来源锁按实际共享generator变化更新，全部门禁保留。独立状态DTO不写history，无新migration；SQLCipher schema15/format2及最低兼容reader `25b004fbd5a4dcf642a503d302c21a7d6e3b817f`不变。需要新状态读取的Desktop先使用已实现该端点的Host；旧Host缺能力时拒绝依赖动作，不降级猜测。详见[23修复](23-native-status-startup-repair-2026-09-11.md)。

## 真实拒绝与正常重开

最终标准构建在原com.yijie.ai app-data、日常Host Home/CODEX_HOME启动。用户经系统隐藏输入启用Sorftime；没有复制数据库或凭据。旧B原生状态实际为notLoaded，本地queued/null-native-ID/failed-outbox逐项保持，界面恢复可读，新任务能够正常发起。

新F任务只请求sorftime/product_detail、ASIN B07H9PZDQW、显式US。真实Prompt显示实际参数后点击拒绝，Host审批`c57f8f99-698b-42db-b3e1-2370a8781f34`变为rejected；原生唯一Tool `call_01a08c16aebe75d1820f1e30`保持failed、0ms、result=null，原生拒绝错误存在，Turn正常completed。模型明确说明没有取得新商品数据、不重试、不引用旧结果，没有追加工具或命令。

业务新增0的依据是实际拒绝决议、完整原生Turn和固定Codex在decline分支先返回、未进入call_tool的代码路径；没有宣称HTTP抓包观察0。原生thread/read独立复核也只见一个Tool和一个completed Turn，未解析rollout。见[实际终态与原生核验](evidence/native-decline-final-2026-09-11.json)、[实时审批和状态](evidence/native-decline-live-2026-09-11.json)。

正常Cmd-Q后，通过普通canonical再次构建启动，F失败/0ms/null结果/原生观察来源和ask模式保留，旧审批回调未恢复；E成功历史仍为completed/414ms/partial脱敏。同一SQLCipher的F view revision25、出站done，B旧行/出站/17与20历史revision未变。最终App/Host/Runtime、计数器和只读原生诊断均正常退出，exit0。

## AC逐项证据

| AC | 判定与真实适用范围 |
|---|---|
| 001 | PASS：单工具/schema/ASIN/US/原生配置核验；F真实初始化、实际Prompt和独立预算 |
| 002 | PASS：E实际成功Item与F实际拒绝Item均来自Codex；ID/status/duration不改写；相关执行代码未变 |
| 003 | PASS：E标题/品牌/价格与原生返回独立匹配；F真实null结果；安全文本、availability和执行结果分开；空/容量的合成定向测试保持原来源范围 |
| 005 | PASS：Item/Turn独立，缺phase/itemsComplete不补造；F原生failed而Turn completed，重开不busy |
| 006 | PASS：最终来源普通重开F和E，已保存原生事实、身份和来源保持，B旧不确定记录不被接管或封口 |
| 007 | PASS：E实际批准、正常停用/auto/full/ask，F最终来源真实拒绝与收尾/重开；秘密和原生权限边界不变，未重放审批 |
| 008 | PASS：canonical启动/切换/正常退出重开、折叠及安全结果；既有UI多主题/最小窗口/200%/键盘/复制按未变UI来源继续适用，当前历史与入口实际复查；旧Command/Artifact/附件限制保留 |
| 009 | PASS：原reader先于writer的完整提交保留，当前独立读取provider-first；旧JSON/migration不变，真实来源与生成门禁通过 |
| 010 | PASS：Codex MCP/elicitation/thread-read、唯一NativeDisplayBuffer和SQLCipher复用；无新执行器、正文对账、身份猜测、历史重建或自动封口 |
| 004 | OWNER_EXCLUDED / NOT RUN；业务失败实现与验收均由用户明确排除，不计入九项PASS |

证据由分次canonical验证和定向检查组成，不是同一任务、同一进程一次运行。E保留实际Host ccd815ff/Desktop a5975f48来源；本次新增状态读取不改变其执行、权限、保存及展示路径，十二个相关文件逐字不变的[适用性审查](evidence/native-status-evidence-applicability-2026-09-11.json)已记录。F在最终完整提交上重验新启动路径和真实拒绝，不能把旧B拒绝或旧测试数量搬成新实跑。

## 调用与剩余限制

累计MiniMax-M3文本 **9/13**；元数据 **14/20**，本轮2次（不超过本轮5次）；业务 **2次逻辑调用、保守扣4/10次尝试**，本轮新增0；图片 **0**。实际HTTP尝试数仍未知，保守扣账不返还、不跨账。剩余授权不自动用于其它需求。

旧B投递结果仍不确定、不能自动续跑；原生notLoaded只表示当前Runtime未加载。Tool正文被既有安全规则整体脱敏，partial与completed独立。缺失phase/plan/reasoning、outputSchema/annotations/progress和冷历史完整性继续保留。Command仍在完成后展示输出；过期附件、历史清理未完、隔离任务无日常Host映射不在本次伪装修复。

本次启动修复没有删除文件。整个FEAT-144已移除新Tool链路的startedSource、空时间/序号、未知identity、空progress/error等旧DTO伪填，以及容量超限时恢复旧Item/弹掉新Item的分支；详见[17删除与保留](17-implementation-review-and-precommit-2026-09-10.md)。仍有消费者的v4/v5/v7、旧Tool renderer、历史DTO/表、存储及权限适配保留。没有Runtime修改/升级、FEAT-137复活或FEAT-152语义改变，没有故障/攻击注入、强杀或权限破坏。未运行禁止的测试不记PASS；没有推送、tag、部署或远端CI。

## 检查与提交

源契约5项Node＋2项Go、57份安全生成、lint和三固定基线通过；Host新读取与既有FEAT144/FEAT132安全定向回归通过；Desktop七项Rust、clippy、fmt、文档构建及canonical构建通过。此前各检查的来源/时间详见23与提交前证据，不冒称全部在最后一步重跑。最终元仓strict/D0/D4、文档及仓库状态核验见最终检查文件。


最终元仓 strict、D0、D4 均实跑 exit0；manifest/Contract First lint、50/50 测试、FEAT-131 strict、diff 和四项 Desktop 来源/退役检查通过，实际命令及输出见[最终检查](evidence/final-document-and-source-checks-2026-09-11.json)。本地 D4 已关闭，feature=usable、implementation=complete；不等于公开/生产交付。

本次文档收尾同步需求四文件、验收场景、FEAT-131能力/黄金场景/证据索引及项目记忆，历史报告保留原来源并指向当前结论。提交前逐文件SHA、十一仓状态和检查后核验见[最终工作区审计](evidence/final-workspace-audit-2026-09-11.json)。元仓提交仅包含这些已核验的文档与证据，提交号由本报告所属Git提交追溯；产品三仓已提交、远端未推送、CI未触发分别记录，不以本地PASS代替远端结果。
