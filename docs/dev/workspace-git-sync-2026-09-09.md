# 多仓改动审计与远端同步（2026-09-09）

用户明确要求审计当前CrossBSD目录下所有仓库，执行适用的git add、git commit并推送到对应远端。本次覆盖repos.yaml的10个兄弟仓库及yijie元仓，额外检查历史隔离检出。只同步现有工作分支，不合并、打tag或部署。

## 审计结果与提交

开始时11个主工作区全部干净，刷新各自origin后无分叉或落后；4个仓库共有13个未推送提交。没有为干净仓库创建空提交。本次额外修正3份组件说明并提交审计记录，均为文档变更，contract-impact=none。

| 仓库 | 当前分支 | 本轮同步范围 |
|---|---|---|
| yijie-contracts | chore/retirement-baseline-20260905 | 原生契约提交及说明修正，共2个提交；远端已核对至e63aafbcb3e2f4fabf0064feec48e7eece3d7046 |
| yijie-agent-host | chore/retirement-baseline-20260905 | 原生薄投影提交及说明修正，共2个提交；远端已核对至26ee8a12f737bb258c717a41d829e8ea706197fe |
| yijie-desktop | chore/retirement-baseline-20260905 | 原生接入、D4修复、权限UI及历史读取修复，共8个提交；远端已核对至c0dd70c240d48c2c16d046aa27c9b32ec4d32c5b |
| yijie | chore/retirement-baseline-20260905 | 原有3个FEAT-132记录提交及本审计记录；随本记录提交后推送 |
| yijie-admin-web | develop | 无新增改动；d009cafccb112c098114c075d60f67ee5e0296d8 |
| yijie-api | feat/feat-126-foundation-closure | 无新增改动；f9d730a157bcb012a8fe178cbfebcd4ea27419fc |
| yijie-codex | chore/retirement-baseline-20260905 | 无新增改动；6c1ad767f0997845b8258a1c452fd4eb7577579f |
| yijie-connectors | develop | 无新增改动；273eec40bbbfeb17e817643f283db7c81e9b190c |
| yijie-infra | feat/feat-126-s10e | 无新增改动；19b7920696904f83030a8ddaba71af15c3c05ad8 |
| yijie-knowledge | develop | 无新增改动；e9091d2b673ba779ecb39271ce9148e3a41fc256 |
| yijie-skills | develop | 无新增改动；488714a8d96f40806a257aae097683815b1dd458 |

逐仓核对分支upstream、origin fetch/push URL及远端引用；目标均为各自`https://github.com/36Dge/<仓库>.git`，未向Codex的OpenAI upstream写入。推送顺序为Contracts→Host→Desktop→元仓，使用已审查的完整提交和明确branch refspec，禁止force和自动附带tag。

组件说明修正：Contracts的native-conversation-v1.md、supported-baselines.md以及Host的native-conversation.md仍残留“未提交/预算0/D4未执行”。已同步真实来源和验收状态。源契约及实现字节未变，消费者继续固定有效的Contracts `6f632f155eacdaf93df0e0b00b5dab9e369c5442`与Host `9e9d317f7e4ecff5f8aeec94fa467f9bede32139`；未将文档提交误当作新的契约版本，也未改published=false。

## 审查与验证范围

- Contracts、Host、Desktop分别进行独立只读审查；初始待推送差异为14/21/76个文件，元仓为23个文件。复核原生事实权威、唯一显示缓冲、SQLCipher/迁移、权限/来源、旧引擎删除、中断和cleanup历史修复，以及UI提交的边界。
- 按每个待推送提交的新增内容执行常见凭据格式扫描，并检查敏感文件路径与二进制差异；未发现新凭据、用户数据库、Runtime二进制或.local构建产物夹带。此项为定向扫描与人工审查，不冒充全面秘密审计证明。
- git diff --check通过；两端native固定对象与consumer同步检查通过。FEAT-137 SDK差异与既有schema标准生成结果逐字节一致，退役权威未改。
- 文档修正提交后，Desktop完整generate:check通过，证明原生与FEAT-152来源pin仍然有效；复用已有固定Skills来源，没有放宽检查。
- 元仓文档与治理检查通过：pnpm lint、pnpm test（50/50）、scripts/*.sh语法检查以及git diff --check；没有将这些结果扩大为完整跨仓测试通过。
- 本次没有运行模型、启动应用或执行禁止的强杀、权限破坏、二进制伪装、攻击/故障fixture。既有D4和日常验收的事实保留原时间、来源和验证范围，见FEAT-132的02及05报告。

## 合并前仍须处理的问题

1. **Desktop CI来源与目录布局未同步。** `.github/workflows/ci.yml`仍检出旧Contracts `164b14f...`和Host `1b7bfd...`，旧Contracts对象中不存在新native同步脚本；现有CI使用`.contracts-source`等嵌套目录，而新native生成/同步脚本要求真实兄弟仓布局。应在后续CI修复中采用一致的兄弟目录、固定新C/H源码提交并安装冻结生成依赖，保留所有来源门禁。本次未修改workflow，不能声称PR集成验证通过。
2. **Host部分旧测试仍断言已移除的合成行为。** `internal/session/service_test.go`的`TestServiceMarksOversizeReasoningUnavailableWithoutBody`仍期待finalized/unavailable，`feat134_projection_test.go`的`TestFEAT134AgentDeltaRequiresSameTurnAgentLifecycleOnlyInV4`仍期待旧状态机关联错误，与已批准的原生单向投影不一致。应更新断言验证新语义，不能恢复旧引擎或笼统跳过测试。本次为静态确认，未运行这些测试或声称完整Go测试集通过。

四个有待推送提交的仓库均通过GitHub查询确认没有关联当前head分支的open PR；其workflow的push分支条件不包含当前chore分支。当前推送用于同步已审查的开发分支，不是远程CI通过、可合并或发布结论。

## 历史隔离检出

额外发现13处辅助Git检出：固定来源/验证worktree、历史构建检出及无origin的Runtime临时plugin仓。它们不是11个主仓库之外的新业务仓库，没有把detached HEAD或临时plugin main推送到主仓工作分支。

两处旧Desktop检出存在dirty/untracked文件，逐文件确认均已集成：

- `.local/chat-ui-sync-20260908-source`的6个图标与当前主仓逐字节相同，已由`3448784`提交。
- `.local/skill-card-build-source`的6个图标同上；其余9个TS/Vue/测试文件（含3个显示untracked的文件）均对应已集成的`c3a6195`。其中旧registry及其测试比当前少了`29d6ad4`加入的3项权限图标，不能覆盖回当前版本。

这三个引用提交均为当前Desktop HEAD祖先。没有独有未整合改动；历史检出原样保留，不追加重复提交、不清理、不回退主仓。不得将“11个主工作区干净”表述为这些旧检出也已清空。

原始本地审计清单、额外检出清单、固定推送计划、来源复核与各仓push结果位于工作区`.local/git-push-audit-20260909`；最终同步结论须以逐仓远端引用与本地HEAD一致为准。
