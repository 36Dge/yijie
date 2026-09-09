# FEAT-134 原生展示调整验收

> 2026-09-09 当前依赖与证据适用范围：本需求当前八项 AC/local D4 以 2026-09-09 原生展示记录为准；远端交付单独记录于 04-remote-delivery-2026-09-09.md。FEAT-136 卡片调整已另行实施并取得自身 local D4，不继承或改写本需求验收。详见[整体一致性复核](../FEAT-131-desktop-codex-parity-baseline/06-native-consistency-review-2026-09-09.md)。

日期：2026-09-09。**八项Must AC满足，当前调整local D4 PASS**。原2026-08-29 D4及原提交的测试结果完整保留于history/2026-08-29，未作为本次新结果继承。

## 当前来源和正常入口

Contracts db7a607c1c091fc4f4243829d68d5b673eb7e2c3；Host f4cf01bd6f7e9f37792ef743d44f0ce10527c10b；Desktop 6e5047d1c23041c46dd495ddb89e24c7e4db5d47。Codex保持干净6c1ad767f0997845b8258a1c452fd4eb7577579f，保留FEAT-136 Runtime未改变。42个pin/digest来源条目及完整generate:check通过。无wire、private schema、数据库migration或权限语义变化，contract-impact=none。

使用原工作区pnpm tauri:demo-fast:app标准构建启动两次；普通身份com.yijie.ai，既有app-data及原.local/demo-fast Host/Codex Home，没有验收代理、隔离Home、数据库或凭据复制。首次和重启后readiness均ready；两次退出均通过应用Cmd+Q，原8条Host映射和最后Turn/native终态、schema5前后逐项一致，最终无活跃Turn、相关进程或18081监听。

## 八项验收结果

| AC | 证据与结论 | 状态 |
|---|---|---|
| AC-001 | 唯一Native缓冲的多Item、Unicode、segment索引及cursor去重定向测试通过；没有第二处正文追加。 | PASS |
| AC-002 | 原生phase/plan转发与selector定向检查；真实重启后未分类消息仍明确提示未标阶段、不视为final。没有伪造计划。 | PASS |
| AC-003 | 完整最终Item直接替换，普通合成的更短、不同及合法空正文通过；原生缓冲不做前缀对账。 | PASS |
| AC-004 | completed/interrupted/failed下未完成Item保留事实并关闭busy；有效订阅与切换测试通过。真实旧等待记录显示当前执行状态未确认，没有续跑。 | PASS |
| AC-005 | Host投影限额仅warning，不将原生completed改failed；Item availability及安全诊断测试通过，诊断不猜Turn归属。 | PASS |
| AC-006 | 插入summary时raw正文DOM/identity不变；两类索引、summary-only、纯文本和无产品复制回归通过。该正向组合使用合成组件测试，没有声称新模型产生了两类内容。 | PASS |
| AC-007 | Native/SQLCipher正常reopen、冷历史冲突与真实Host→Native→SQLCipher集成通过；canonical两次读取现有原生历史及旧档案、Artifact，Host映射/终态无变化。 | PASS |
| AC-008 | 两次canonical启动及正常退出、中间重启、会话切换、过期附件元数据和Artifact图片预览通过；权限三选项保持请求批准。200%缩放、键盘到达附件/权限按钮并恢复100%；Command/Composer/权限组件定向回归通过。 | PASS |

## 检查范围

- 前端10份审阅后定向测试233/233 PASS；包含native显示、有效订阅/选择隔离、旧历史、Command、Permission、ArtifactImage、Composer。
- Host9项原生/兼容定向测试及go vet PASS；Native buffer4/4、SQLCipher正常reopen4/4；跨仓脚本另启用并通过1项SQLCipher集成及真实Host安全投影导出。
- ESLint/TypeScript、Vite构建、Rust clippy all-targets、fmt、Desktop文档构建、元仓50项及D0通过。Vite既有大chunk提示保留。
- 独立于实现阶段的Codex自审完成：修正了把Native默认partial误当停止执行的初版判断，UI结合当前订阅、原生状态及明确缺失诊断；不冒充独立人工批准。
- 广泛Host/Rust历史测试包含禁止场景，未运行完整套件；远端CI未运行。本轮未推送、打tag、合并或部署。

## 真实数据及保留限制

- 原生图片历史的phase缺失继续为未分类；图片预览重启前后正常。该隔离D4任务没有日常Host映射，权限同步不可用继续保留，不重试或猜测接管。
- 旧附件显示自然过期及未完成清理，历史可读，输入入口继续禁用；切换至正常映射会话恢复操作入口。没有恢复过期文件或重试删除。
- 当前数据未提供完整的summary/raw双类别、显式phase/plan及Command流式正向模型样本；相关正向分支由定向测试验证。本轮未发送新模型Turn，不将现有数据读取冒充新流式模型验收。
- 固定Runtime冷历史仍不完整，Command输出在最终对象完成后展示；旧记录只读，没有自动续跑、补发或原生身份猜测。
- dark theme、Reduce Motion、精确1180×760保持原WAIVED / NOT REQUIRED，不作为PASS。

## 授权、台账与过程失败

用户在提交前核验后明确要求执行剩余步骤，授权本次本地提交、必要修复与真实pin更新。此前generate:check因未提交Contracts失败、D4因AC-007/008及真实入口未完成失败，均按门禁停止；授权后固定来源并完成对应验证，没有修改验证器或绕过检查。一次手动Vitest路径误纳入旧.local检出，随后按标准排除范围验证当前源码，未修改旧检出。

本次累计0次文本、0次图片。原FEAT-134 10/11和FEAT-132 19/25文本、1/3图片仅保留各自历史台账，不合并、不转用。操作未扩大权限、未强杀、未实施攻击/故障注入，未复制用户DB或凭据。

[机器可读canonical证据](evidence/native-adjustment-canonical-2026-09-09.json)记录来源、数据范围、两次进程、退出、映射比对和检查项；[实施及删除清单](03-native-display-adjustment.md)记录保留兼容边界。本地content-free日志位于工作区.local/feat134-native-adjustment-20260909，不保存对话正文或凭据。

最终D4需求包门禁已实际通过（exit 0）；随后按最终文档运行元仓治理检查。此前未通过的阶段保留在交付日志，未改写历史原始D4。
