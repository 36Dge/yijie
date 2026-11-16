# 两个 P1 的复审问题修复

2026-11-15。用户授权修复复审发现的构建入口阻断（P1）与结果标题快照错用（P2），
并明确暂不重启易界服务。未提交或推送，未调用真实供应商／付费模型，未替换运行制品。

`contract-impact=semantic` 仅涉及私有构建／预检入口：显式本地候选现在可由固定开发
入口检查。公共 HTTP/IPC、MCP 回执、审批与持久化格式均不变，公共 wire 版本调整 N/A。
先补充 Contracts 的 `docs/market-call-receipt.md` 约束，再修改检查与消费者。

## 修改清单

| 仓库 | 修改 |
| --- | --- |
| yijie-contracts | 本地 `--local-market-candidate` 同时检查／同步 selection、Host、experts 三个 v2 表面；刷新三个同源来源锁；补充构建契约说明 |
| yijie-agent-host | 同步三个 v2 candidate 来源记录；本轮未改 Host Go 实现、审批或数据库 |
| yijie-desktop | 新增 `scripts/check-market-call-surfaces.mjs` 和测试；Kimi 构建校验与日常启动脚本的两处检查统一调用它；同步三个 v2 candidate；用原 canonical freezer 刷新 Native Skill 的 Host 输入快照；修复 `MarketChatActivity.vue` 标题与组件测试 |
| yijie | 本记录及前一轮实施记录的后续说明 |
| yijie-connectors／yijie-codex | 本轮无修改 |

selection 的 wire 与 SDK 没有变化。其来源锁也包含共享同步脚本，故本地检查必须纳入
selection，不能仅允许 Host／experts 而遗漏剩余来源检查。

检查入口只在 `local + demo_fast + YIJIE_DEVELOPMENT_CLIENT=true +
YIJIE_KIMI_K31_PRO_CANDIDATE=true` 下接受完整 `market-p1` 候选：两个消费者的三个
来源记录必须全部使用同一模式，包含 worktree_head、release=false，不得包含
source_commit。随后调用 canonical generator／sync 的只读检查，逐项验证来源和
生成输出。混合模式被拒绝；其他构建模式继续要求原不可变来源，没有失败后降级路径。
现有 Host／Runtime／资源／分组件构建检查继续执行。

结果标题按 nativeTurnId 查原轮次 availableTurns，并同时匹配 serviceId、installationId、
revision、generation。只有显式读取同一历史轮次时才兼容旧 reader 的 selectionDisplay；
默认观察不能将最新未绑定提交的名称用于旧结果。缺少可信原始名称时显示 serviceId，
保留结果与状态，不改动审批按钮和执行逻辑。

## 验证结果

- 新增 Node 来源模式／入口接线测试：4 项通过。
- 实际 `check-market-call-surfaces.mjs --check`：三个 v2 表面及两端消费者全部通过。
- 实际完整 `verifyKimiK31BuildCandidate`：使用固定开发客户端原环境，包含完整 media
  表面及 native Skills，全部只读检查通过，核对 653 个 Host 输入。目录／专家资源使用
  已保留的固定来源，没有新增 checkout 或启动服务。
- 非固定开发环境检查、默认 immutable 同步检查仍拒绝当前未提交候选，符合预期。
- `MarketChatActivity.test.ts`：11 项通过，含新提交未绑定、空选集、另一轮次、安装代次
  变化、旧 reader、批准与失败分别显示等情形。
- 受影响前端／检查脚本 ESLint、`vue-tsc --noEmit`、启动脚本 `bash -n`、各仓
  `git diff --check` 通过。

完整来源检查起初发现 Host 输入快照仍早于两个 P1。经既有
`scripts/native-skill-build-candidate.mjs --freeze` 更新后通过；JSON 对比确认只有
host_sources 变化，Runtime、资源、feature、release 和 baseline 均保持原值。
这是本地构建来源更新，不是运行成功或发布批准。

未运行易界启动／停止／重启、打包、GUI 验收、真实供应商或付费模型调用；未重复运行
本轮未修改的 Rust／Go／Runtime 执行测试。只读构建检查通过不代表实际服务重新装载。

## 工作区保护与回滚

修改前备份并记录六个相关仓库的 HEAD、全部 135 个已有 dirty/untracked 文件摘要。
在原有修改基础上增量编辑；已有日常入口只替换两处检查调用，原预检、正常退出和
分组件构建实现保留。来源记录使用 canonical 生成器更新，没有手改 SDK/schema。
未改变分支／HEAD，未提交、推送或修改日常运行制品。

本轮没有数据库 migration。标题修复可独立回滚。构建入口回滚须同时恢复匹配的同步
脚本、来源锁和消费者候选；不能只补 source_commit 或关闭校验。回到此前本地候选会
恢复本次修复前的入口阻断，不应视为完整可用回滚。后续用户正常重启仍走原预检和
按组件增量构建，不沿用旧许可或重放结果未知的工具调用。

前轮已经记录的无回包关联、审批进行中 Item 关联、真实供应商成功链路与混合版本
进程回滚验收边界仍然存在；本轮未将其标记为通过。
