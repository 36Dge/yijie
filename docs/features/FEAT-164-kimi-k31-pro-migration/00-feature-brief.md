# FEAT-164 — Kimi K3.1 Pro 模型替换与历史兼容

> 当前口径：原主工作目录构建与退出修复见[76](76-primary-workspace-execution.md)/[77](77-primary-system-quit-root-cause-and-plan.md)，旧daily-source清理见[78](78-old-daily-source-retirement.md)，清理后一次真实启动、8会话/11轮历史UI与正常退出及后态验收见[79](79-post-cleanup-app-history-acceptance.md)。当前源码为原`CrossBSD/yijie-desktop`，generation `20261028-02`；模型HTTP新增0，新来源历史界面已实际通过，76原锁屏跳过记录仍保留。完整App正向never-sent取消仍NOT RUN且已有接受替代；搜索答案/外观专项永久移除。当前状态见[矩阵](current-acceptance-matrix.md)，下文旧阶段的“当前”均按各自时点解释。

## 第71—74号时点来源与清理历史（已由76号原主目录来源取代）

S1—S4、D1—D5在ADR-0022个人Mac范围完成；后续原仓来源/入口收敛C1—C5也已完成。当前Desktop为`a211c2d04def6091352c7b3674a49355cdee18ed`，Host为`7309101726dcecd48b2caa02401cfcdd6126f1fb`，固定来源在`yijie/.local/daily-source/20261027-01`；8个干净worktree连接原仓Git对象库，Runtime映射原仓。原主工作区及已有改动保留，尚未将集成分支合回主工作区；日常入口使用固定来源，8个来源仍须保留。

[71](71-original-repository-daily-entry-consolidation.md)记录新位置三轮实际启动/历史检查/正常退出与两个入口切换；[73](73-final-six-directory-cleanup-completed.md)记录最终6目录/26 worktree清理及清理后prepare-only通过。两轮共74个旧顶层目录已不存在。当前App、回执、绑定、数据及完整验收分类见矩阵；本次仅同步文档，0新增App/模型调用。never-sent已接受安全替代、完整App正向取消NOT RUN及Owner移除范围均保持。

## 第67/69号D5完成记录（历史，2026-10-27）

以下保留当时原文；其中旧提交、制品和“当前权威”不再代表现行来源。

当前权威[67](67-d5-entry-and-activation-implementation.md)：D5已按Owner明确批准的ADR-0022个人本机范围完成。新日常入口固定Desktop39b0fbe/原Home，默认启用Kimi K3.1 Pro；真实正常启用、暂停回退和同入口再次启用均通过，3次正常退出及完整后态通过。0模型验收调用，原历史/授权/账本/预占及dirty保留，仅本地提交不推送。G4/G5本机就绪与G6实际交付观察分别留证；不授权公网/云端/多人/签名发布。以下66及更早阶段按各自时点解释。

## 第64号历史D3实施结果（2026-10-27）

当前权威为[64 D3一次维护与后态审计](64-d3-controlled-migration-and-post-state-audit.md)。Owner批准的一次维护已完成，日常Native由SQL37升级到41后正常退出；候选、完整D2备份、实例锁/句柄及数据一致性先行核验，后态完整备份与只读复核通过。67张既有业务表全部旧行不变，仅新增4条迁移记录和3张空表；原Host/Runtime、密钥、账本/预占保持。

当前D3_COMPLETE_STOPPED，不进入D4。无GUI、Host、Runtime启动或新模型调用，无Runtime核心/补丁修改。下一步仍须单独批准D4并重验后态/锁/全模型无派发工作/既有workflow ready；D5长期入口、local G5/G6口径继续待收口。旧SQL37构建不可直接重开SQL41，未执行回退。58接受范围与Owner排除项保持。下列旧阶段按原时点解释。

## 60号历史D1实施结果（2026-10-27）

当前权威为[60 D1完成与离线资格](60-d1-daily-binding-and-offline-qualification.md)。59号D1已获批并完成六文件Desktop修正、安全测试和新canonical prepare-only/同回执复核；Host/Runtime采用已批准原Home绑定，daily不再隐式workflow-up。真实日常绑定未生成、D2—D5未执行、模型HTTP新增0、Runtime核心/补丁未改。原CUTOVER-01/03已离线修复，日常现场/启动资格仍无授权，G4不自动晋升。58接受的never-sent替代保留，完整App正向取消仍NOT RUN。

下方59及更早“尚未实施D1/原入口缺陷”按当时来源解释，不再作为当前D1未完成项。下一步仅在批准D2后进行完整冷备份和副本只读预检，不顺带迁移或启动。

## 59号历史日常切换边界（2026-10-27，S4AF）

以[59 日常切换方案](59-daily-cutover-minimal-plan-and-authorization.md)为当前部署权威。源码复审发现daily launcher将Host/Runtime Home改至候选新目录、与原Native日常库缺连续性；正常启动还可能隐式workflow迁移及恢复自动计划。日常activation为NO_GO，当前G4重新pending，先提限定部署入口修正及离线资格，尚未获准实施。58的已接受本地S1—S4/final证据与never-sent替代保持，完整App正向取消原执行仍NOT RUN；不是重新跑失败或取消Owner接受。

本轮仅方案和治理，无产品/Runtime改动，无日常数据访问/备份/预检/迁移/启动，无模型调用。阶段顺序为D1入口修正→D2完整冷备份与副本只读预检→D3一次Native维护→D4首次受限启动及退出核对→D5确认日常启用；D1—D5均未自动授权，具体边界见59。以下早期状态按各自时点解释。

## 58号历史已接受范围（2026-10-27，S4AE）

以[58 安全替代接受与最终收口](58-owner-accepted-substitute-and-final-closure.md)、feature.yaml和[当前矩阵](current-acceptance-matrix.md)为准。Owner明确接受57号never-sent正常Native API与生产消费链的安全分层替代；S4/TCONF04及三项适用最终验收按该方式收口，G4为本地代码完成。**完整App正向never-sent取消的原始执行状态仍为NOT RUN**，没有改写为已执行。原自然unknown缺Host回执，安全拒绝重发通过，原记录仍未恢复ready。

本轮仅只读审计和治理更新，真实/本机模型HTTP新增均0；产品、Runtime核心/补丁、来源锁不变。不启动或迁移日常库，日常候选保持prepare-only，G5/G6及正式交付仍pending。搜索答案正确性、亮暗/键盘/最小窗口专项保持OWNER_EXCLUDED，不恢复为待办。以下早期阶段记录按原时间和来源解释；本节覆盖其中过期的推进顺序、预算授权和“当前未通过”描述。

## 用户结果

将活动 Kimi 模型由 kimi-k3 更换为 **kimi-k3.1-pro**。普通聊天、旧会话继续、专家、标题、计划草案及执行使用新身份；旧 K3 不再可选、不发起新推理。历史、已接受操作及计划授权事实保持可读，MiniMax 不变。

建议内部 profile：kimi-k3-1-pro-max-v1；显示 Kimi K3.1 Pro；provider kimi；原 Responses endpoint、max、1048576 上下文保持。官方 model 中的点号必须保留，内部连字符只是避免当前 Go/Rust 生成标识符出现点号。

## 治理及边界

[ADR-0017 第11条](../../adr/ADR-0017-dual-profile-feature-delivery.md)把重要持久数据纳入 production_hardened。本需求涉及 SQLCipher 会话/操作/计划授权及 Host bbolt，新身份写入后旧 reader 不兼容，因此使用加固治理。不是因付费 API 归类，也不声称 SQL 本身绝对不可逆。

治理 delivery_profile 与应用 YIJIE_LOCAL_PROFILE 不同。FEAT-164保持production_hardened/local，应用沿用受控本机入口；仅按Owner已接受的[ADR-0022](../../adr/ADR-0022-feat164-personal-local-activation.md)适用ADR-0018的本需求个人Mac限定例外。完整G0—G6保留，本机G4/G5/G6已依67/69实际证据通过；这不构成公网、云端、多人、多租户或签名发布资格，也不改变其它需求的免登录边界。

范围：模型契约及传递依赖、受管配置、最小 Runtime 补丁及独立候选、读写兼容/准入、旧会话和未决操作、计划授权、UI与同源验证方案。

非目标：整个 Codex 上游升级、Chat Completions 迁移、新代理/进度引擎、开启 Coze 模型/记忆/视频/新生图服务、扩权、充值、全局 Codex 配置修改、完成 FEAT-162/163 独立验收、删除历史旧模型名称。

## 阅读顺序

[11 二次审计](11-second-audit.md) → [01 需求](01-requirements.md) / [03 决策](03-decisions-and-risks.md) → [04 契约](04-contract-change-plan.md) / [04A 时序](04A-temporal-contract-matrix.md) / [05 设计](05-technical-design.md) → [06 测试](06-test-plan.md) / [07 计划](07-implementation-plan.md) / [09 回滚](09-release-and-rollback.md)。实际状态见[当前验收矩阵](current-acceptance-matrix.md)、[08](08-verification-report.md)、[feature.yaml](feature.yaml)及67/69；[12 续办](12-resume.md)仅保留早期续办历史。

[首次审计](../../dev/kimi-k3-1-pro-migration-audit-20261024.md)保留为背景；冲突以本包二次修正为准。需求/技术/Reviewer/发布 Owner 默认段成威；Codex 复核不是独立人工批准。
