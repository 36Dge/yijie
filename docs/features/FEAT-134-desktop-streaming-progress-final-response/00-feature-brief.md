# FEAT-134 — 基于 Codex 原生事实的流式与过程展示

> 2026-09-09 当前依赖与证据适用范围：本需求当前八项 AC/local D4 以 2026-09-09 原生展示记录为准；远端交付单独记录于 04-remote-delivery-2026-09-09.md。FEAT-136 卡片调整已另行实施并取得自身 local D4，不继承或改写本需求验收。详见[整体一致性复核](../FEAT-131-desktop-codex-parity-baseline/06-native-consistency-review-2026-09-09.md)。

Profile：demo_fast；Exposure：local。2026-09-09 用户确认并授权本次原生适配调整，D0 PASS；本次原生展示调整已完成来源固定及 canonical 既有数据验证，八项 Must AC 满足，local D4 PASS。

## 产品目标与当前事实

用户能区分流式回答、处理过程、计划、推理摘要、原始模型推理记录与最终回答，并准确理解执行结束和信息缺失。FEAT-132 已建立 native v7、NativeDisplayBuffer、thread/read/resume 与 SQLCipher 原生事实保存；FEAT-134 直接消费该链路。当前不再以旧 ConversationState/reducer 为执行权威。

固定 Runtime 决定 thread/turn/item 身份、phase、内容和执行结果；Host 只做受权限控制的安全投影及传输；Native 是唯一显示追加位置；Vue 只映射完整视图。业务 outbox、附件、Artifact、FEAT-152 和旧档案保留各自边界。

## 必须遵守的规则

1. item/completed 的完整对象直接替换临时正文，包括更短、不同及合法空正文。不做正文前缀比较、冲突裁决或重复 final。
2. turn/completed 只确认 Turn 结果，不封口剩余 Item、不补造结束时间。缺少 Item 结束记录通过展示提示表达。
3. 原生执行状态、内容 availability 与当前 UI 忙碌分别表达。仅当前有效订阅收到的可信活跃 Turn 可驱动忙碌；旧历史、断线和未确认信息不能冒充正在执行。
4. reasoning summary/content 分别保留原生索引；显示标识由原生 Item、内容类别和 segment index 组成。summary-only 明确为摘要，不能作为 raw reasoning 正文存在的证据。
5. reasoning 继续纯文本渲染，不激活链接、不提供产品级复制按钮；不进入日志、遥测、错误正文或未加密存储。
6. phase 缺失即未分类；plan 缺失即无计划。不得按正文、顺序、最后一项或时间推断。
7. 历史复用 FEAT-132 原生读取及加密事实；已观察终态优先，冷历史集合不按身份、正文或 ordinal 猜测混合。旧档案只读。
8. projection/availability 问题不改变执行结果。诊断只映射安全代码；没有可信范围的提示按会话展示，不猜测归属 Turn 或 Item。

## 界面和场景

- 等待/流式：仅真实活跃通知显示忙碌；不产生虚构步骤、进度或耗时。
- 内容分层：commentary、plan、reasoning 次级可折叠，final 默认展开；摘要与原始正文有独立标签。
- Turn 结束而 Item 未结束：保留原生最后观察状态，关闭 UI busy，提示未观察到该项结束记录。
- 内容缺失：在对应 Item 显示 available/partial/unavailable 的含义；会话诊断提示具体可展示原因。
- 历史/切换：旧记录与原生来源明确，选择和订阅隔离继续复用既有 store，不触发续跑或补发。
- 权限/错误：沿用 FEAT-152 与资源校验，不以展示变化扩大权限；故障、重试、清理仍归各自既有协调器。

## 范围与非目标

实施覆盖元仓需求、Contracts 旧说明、Host 兼容测试及无调用常量、Desktop 展示和无调用发布残留。已有 public/private wire 与数据库字段足够；contract-impact=none：本轮只改变进程内展示、无调用代码、测试及说明，不再次改变 FEAT-132 已批准的跨进程执行语义、持久化格式或权限。若发现实际 wire/持久化缺口，先重新分类并走源契约流程。

不修改 yijie-codex、Runtime patch/产物/版本；不恢复 FEAT-137；不改变 FEAT-152；不新增状态推演、历史重建、正文对账或自动封口。旧 v4/v5 路由、历史 DTO/IPC、表及 Artifact/Command 依赖仍保留，不整包删除。local high/raw 开关不扩大到其它环境。

## 八项 Must AC

| AC | 当前要求 |
|---|---|
| AC-001 | 多 Item、Unicode 和原生 reasoning 分段只由唯一 Native 缓冲追加；传输重复只在既有入口处理。 |
| AC-002 | commentary/final/plan 仅来自原生字段，缺失时不推断。 |
| AC-003 | 原生完整 Item 直接替换草稿，更短、不同和合法空内容均可接受，无正文对账或重复 final。 |
| AC-004 | Item 与 Turn 生命周期独立；Turn 结束不封口 Item，UI 停止误报忙碌。 |
| AC-005 | 原生执行结果与 availability/诊断分离，投影和存储问题不伪造终态。 |
| AC-006 | summary/raw 分类及索引稳定，纯文本且无产品复制按钮，summary-only 不冒充 raw。 |
| AC-007 | 加密已观察事实正常重开保持来源；冷历史不覆盖已观察终态、不猜身份；旧档案可读。 |
| AC-008 | canonical 启动、切换、退出重启和展示/a11y 定向检查通过；附件、Artifact、Command、FEAT-152 无定向回归。 |

原 dark theme、Reduce Motion、精确 1180×760 的 WAIVED / NOT REQUIRED 保留，不恢复为门禁，不写为 PASS。

## 授权及历史

用户已授权本轮实施和正常非破坏性验证。用户随后以“执行 FEAT-134 剩下的步骤”授权上述本地提交、必要修复和真实 pin 更新；未授权推送或新增付费调用。原 FEAT-134 10/11、FEAT-132 19/25 文本及 1/3 图片均仅为各自历史台账，不合并、不转用。本轮默认只读既有数据。

[原 D4 完整记录](history/2026-08-29/02-verification.md)按原日期与原提交保留；原始四份需求文件及 evidence 已逐字节归档。本轮验收见 [02-verification.md](02-verification.md)，实施与来源见 [03-native-display-adjustment.md](03-native-display-adjustment.md)。历史 PASS 不自动继承。
