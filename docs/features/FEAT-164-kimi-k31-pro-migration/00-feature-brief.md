# FEAT-164 — Kimi K3.1 Pro 模型替换与历史兼容

> 当前按[50 前三切片收口与日常部署方案](50-slice-evidence-closure-and-daily-deployment-plan.md)：S1—S3的G3已通过，S4完整验收仍缺；Owner已批准8文件日常候选实现及离线验证，明确不迁移真实日常库。此前状态按原阶段解释。

> 当前以[49 r5真实功能与日常边界](49-r5-real-qualification-and-daily-cutover-boundary.md)为准：Owner已明确授权必要真实功能调用且不要求精确查价；本轮1次r5真实42、保存/重开零补发和正常退出通过。旧账本/预占保持，日常迁移未执行；完整core/剩余业务状态仍按明确缺口判定。已移除外观专项不再作为门槛。

2026-10-26 当前状态：**IN_PROGRESS，尚未切换日常入口。** Owner已批准继续实施及必要真实功能验证、FEAT-164专属本地提交；本轮新增真实模型HTTP1，r5最小文本G2V和正常退出通过，日常迁移、推送和发布保持关闭。r5六文件关闭修复已经批准、构建并取得限定资格，不能再按40/41号历史待批准状态解释。

Owner已从本需求移除App亮暗、键盘/焦点和最小窗口专项验收，不再作为完成门槛。

当前来源、AC差距和下一步统一见[49 r5真实功能及日常切换边界](49-r5-real-qualification-and-daily-cutover-boundary.md)、[48 保留状态验证与范围调整](48-retained-runtime-qualification-and-scope-update.md)、[47 同源媒体App资格](47-current-media-app-and-retained-state-qualification.md)、[46 独立旧数据App资格](46-independent-legacy-app-qualification.md)与[当前验收矩阵](current-acceptance-matrix.md)。Runtime11fd/r5保持；S4S独立部署代码及旧模式来源整理已实施。r4真实G2V/视觉PASS保留原来源；r5完整S2/S3/S4和三项final不能继承。原unknown、已消耗计划额度与费用预占均保留。

2026-10-24创建 · schema v3 · production_hardened · exposure: local · active。早期审批、故障、预算与通过结论见12—45号历史报告，按各自时间和来源解释，不作为本页当前授权。

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
