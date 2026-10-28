# FEAT-164 当前交付状态

> 最终关闭（2026-10-28）：Owner已要求完成最终收口并关闭FEAT-164，结论见[80](80-final-audit-and-feature-closure.md)及[关闭审计证据](evidence/final-closure-audit.json)。S1—S4、D1—D5、原主目录构建运行、已批准旧目录清理及79清理后实际验收均完成，批准范围内无剩余事项。完整App正向never-sent取消仍NOT RUN且已接受安全替代；搜索答案正确性与亮暗/键盘/最小窗口专项为OWNER_EXCLUDED。79仍是最新实际App运行证据，80只做最终审计与文档关闭，不新增产品、Runtime或模型执行。以下历史记录保留原时点语义。

> 当前口径：原主工作目录构建与退出修复见[76](76-primary-workspace-execution.md)/[77](77-primary-system-quit-root-cause-and-plan.md)，旧daily-source清理见[78](78-old-daily-source-retirement.md)，清理后一次真实启动、8会话/11轮历史UI与正常退出及后态验收见[79](79-post-cleanup-app-history-acceptance.md)。当前源码为原`CrossBSD/yijie-desktop`，generation `20261028-02`；模型HTTP新增0，新来源历史界面已实际通过，76原锁屏跳过记录仍保留。完整App正向never-sent取消仍NOT RUN且已有接受替代；搜索答案/外观专项永久移除。当前状态见[矩阵](current-acceptance-matrix.md)，下文旧阶段的“当前”均按各自时点解释。

## 第71—74号来源、入口与清理记录（历史，2026-10-28）

S1—S4、D1—D5在ADR-0022个人Mac范围完成；后续原仓来源/入口收敛C1—C5也已完成。当前Desktop为`a211c2d04def6091352c7b3674a49355cdee18ed`，Host为`7309101726dcecd48b2caa02401cfcdd6126f1fb`，固定来源在`yijie/.local/daily-source/20261027-01`；8个干净worktree连接原仓Git对象库，Runtime映射原仓。原主工作区及已有改动保留，尚未将集成分支合回主工作区；日常入口使用固定来源，8个来源仍须保留。

[71](71-original-repository-daily-entry-consolidation.md)记录新位置三轮实际启动/历史检查/正常退出与两个入口切换；[73](73-final-six-directory-cleanup-completed.md)记录最终6目录/26 worktree清理及清理后prepare-only通过。两轮共74个旧顶层目录已不存在。当前App、回执、绑定、数据及完整验收分类见矩阵；本次仅同步文档，0新增App/模型调用。never-sent已接受安全替代、完整App正向取消NOT RUN及Owner移除范围均保持。

## 第67/69号D5完成记录（历史，2026-10-27）

以下保留当时原文；其中旧提交、制品和“当前权威”不再代表现行来源。

当前权威[67](67-d5-entry-and-activation-implementation.md)：D5已按Owner明确批准的ADR-0022个人本机范围完成。新日常入口固定Desktop39b0fbe/原Home，默认启用Kimi K3.1 Pro；真实正常启用、暂停回退和同入口再次启用均通过，3次正常退出及完整后态通过。0模型验收调用，原历史/授权/账本/预占及dirty保留，仅本地提交不推送。G4/G5本机就绪与G6实际交付观察分别留证；不授权公网/云端/多人/签名发布。以下66及更早阶段按各自时点解释。

## 第64号历史D3实施结果（2026-10-27）

当前权威为[64 D3一次维护与后态审计](64-d3-controlled-migration-and-post-state-audit.md)。Owner批准的一次维护已完成，日常Native由SQL37升级到41后正常退出；候选、完整D2备份、实例锁/句柄及数据一致性先行核验，后态完整备份与只读复核通过。67张既有业务表全部旧行不变，仅新增4条迁移记录和3张空表；原Host/Runtime、密钥、账本/预占保持。

当前D3_COMPLETE_STOPPED，不进入D4。无GUI、Host、Runtime启动或新模型调用，无Runtime核心/补丁修改。下一步仍须单独批准D4并重验后态/锁/全模型无派发工作/既有workflow ready；D5长期入口、local G5/G6口径继续待收口。旧SQL37构建不可直接重开SQL41，未执行回退。58接受范围与Owner排除项保持。下列旧阶段按原时点解释。

当前候选仍Desktop841f7c7/Hosta3d8767，App SHA4f7adcadc59db4a6e4cf23e700ebab5858b6ae9d953cd7401780d5778cab0f42、receipt0e6fe8191ffc027d4f1efedf14f7e8562ee1d876068aafa7386410202a2878a7；119包内文件/1216源码输入不变。本轮未改产品代码或重建制品；原工作区、全部账本及两份14.188544元预占保持，累计13次、45元cap及29.740299元保守累计不变。只做本地治理提交，不推送。
