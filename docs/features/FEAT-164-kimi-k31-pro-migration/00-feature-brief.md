# FEAT-164 — Kimi K3.1 Pro 模型替换与历史兼容

## 当前D4启动前状态（2026-10-27）

当前权威[65](65-d4-preflight-and-workflow-restart-boundary.md)：Owner已批准D4首次受限启动，但预检在workflow读取容器时停止。原Docker Desktop/backend未运行、固定socket不存在，实时ready未获确认。候选、完整D2/D3备份、日常SQL41/三存储映射、实例锁与全模型零派发检查通过；App启动次数0、D4绑定未生成，0模型调用，不进入D5。新增依赖恢复范围已具体列入65，尚未获得本轮批准；既有D4授权不丢失，不改数据绕过ready。以下64及更早描述按各自时点解释。

## 当前D3实施结果（2026-10-27）

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

治理 delivery_profile 与应用 YIJIE_LOCAL_PROFILE 不同。现有模型功能精确要求 local + demo_fast，继续以既定受控本机入口作为未来验证对象；不因治理分类改环境变量或扩张 ADR-0018 免登录边界。当前无公网/生产激活，local exposure 不得宣称 G5/G6 通过。

范围：模型契约及传递依赖、受管配置、最小 Runtime 补丁及独立候选、读写兼容/准入、旧会话和未决操作、计划授权、UI与同源验证方案。

非目标：整个 Codex 上游升级、Chat Completions 迁移、新代理/进度引擎、开启 Coze 模型/记忆/视频/新生图服务、扩权、充值、全局 Codex 配置修改、完成 FEAT-162/163 独立验收、删除历史旧模型名称。

## 阅读顺序

[11 二次审计](11-second-audit.md) → [01 需求](01-requirements.md) / [03 决策](03-decisions-and-risks.md) → [04 契约](04-contract-change-plan.md) / [04A 时序](04A-temporal-contract-matrix.md) / [05 设计](05-technical-design.md) → [06 测试](06-test-plan.md) / [07 计划](07-implementation-plan.md) / [09 回滚](09-release-and-rollback.md)。实际状态见 [08](08-verification-report.md)、[feature.yaml](feature.yaml)、[12 续办](12-resume.md)。

[首次审计](../../dev/kimi-k3-1-pro-migration-audit-20261024.md)保留为背景；冲突以本包二次修正为准。需求/技术/Reviewer/发布 Owner 默认段成威；Codex 复核不是独立人工批准。
