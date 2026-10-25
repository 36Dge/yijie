# FEAT-164 — Kimi K3.1 Pro 模型替换与历史兼容

> 最新续办与整项目标以[35 当前组合与完成差距](35-s4-current-media-and-completion-audit.md)、feature.yaml及S4I证据为准。旧阶段记录保留其原来源和时间；当前仍未切换日常入口，不新增真实模型HTTP。

> S4I结果：Desktop399bb19/Host090c2db配对专家切换、r4媒体/正常中断/图片、同源重开及清理通过；旧unknown仍保留阻断。当前安全子集分组通过不等于完整TCONF/G2V/G3/final。后续按35末节整项执行单推进。

> 最新（2026-10-25）：首次真实G2V返回HTTP400、无usage，14.188544元预占保留。已自行修正include规范差异并本地固化r2，离线验证进展见[19](19-responses-400-audit.md)；更早阶段的授权、预算与通过结论仅按当时范围解释。

> 2026-10-25 用户已明确恢复，沿用 20 元及搜索/图片授权。当前进度与预算边界见 [18 恢复实施记录](18-resumed-g2v.md)；17 保留暂停时历史状态。G2V 尚未通过。

> 2026-10-25 当前进度：原隔离清单三仓已本地提交，G2A PASS；Host/Desktop 最小候选及普通本机联调完成，G2V、S1—S4/final 仍 pending。当前证据和续办边界以 [16 下游候选审计](16-downstream-candidate-audit.md) 与 feature.yaml 为准；以下早期阶段记录保留其历史含义。

> 实施授权更新：Owner现已确认FEAT-164方案并要求开始实施和审计验证。此前“仅文档”段落是上一轮历史边界；当前状态以feature.yaml及13-implementation-log.md为准。G0/G1/G2记录本次方案确认；G2A/G2V及产品完成门禁仍未通过。无新增Git/付费/日常库激活许可。

2026-10-24（Asia/Shanghai） · schema v3 · production_hardened · exposure: local · active。

**Owner 已确认方案并授权实施、安全验证和审计。当前已完成未激活的源契约/Runtime候选；G0/G1/G2通过，G2A及后续门禁pending。** Host/Desktop迁移、日常激活和真实模型验证尚未执行，整体功能未完成。实际结果与Git批准边界见08/13/14。

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
