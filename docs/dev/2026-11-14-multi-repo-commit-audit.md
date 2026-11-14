# 2026-11-14 多仓提交与推送审计

用户明确授权审计易界全部仓库，对所有改动执行 `git add`、自行归纳 `git commit -m` 并推送到各自远端分支。范围按 `repos.yaml` 为元仓及 11 个兄弟仓；本次是提交前改动、来源、数据与 Git 状态审计，不冒称对全部历史代码或所有测试做了全量审查。

开始时 6 仓有改动，6 仓干净。全部 origin 与仓库清单一致；fetch 后 12 仓均未落后或分叉。未切换分支、重写历史、修改远端或强制推送。按 Runtime → Contracts → Skills → Host → Desktop → 元仓提交，提交说明记录功能摘要和上游依赖。

## 已提交并核对远端的业务仓

| 仓库 | 提交 | 远端分支 | 内容 |
| --- | --- | --- | --- |
| yijie-codex | [`5c64ed3f03`](https://github.com/36Dge/yijie-codex/commit/5c64ed3f03808639faf7c11674e87636a94ab221) | `origin/chore/retirement-baseline-20260905` | 原生本地技能市场策略、库存读取与显式刷新补丁及构建来源 |
| yijie-contracts | [`2592f5d5b0`](https://github.com/36Dge/yijie-contracts/commit/2592f5d5b07fcd92de10d25c4dcf73bd1ce03cb5) | `origin/feat/feat164-primary-20261028` | 技能市场、导入、未派发证明及多语言生成物 |
| yijie-skills | [`1cc5abd979`](https://github.com/36Dge/yijie-skills/commit/1cc5abd979baf58c7314d36c55794a7743dc0860) | `origin/feat/feat164-primary-20261028` | 原生技能源打包、可变发行目录与临时产物忽略规则 |
| yijie-agent-host | [`8b6d7afa41`](https://github.com/36Dge/yijie-agent-host/commit/8b6d7afa4122265951b3eeeacc81495b7684f87f) | `origin/feat/feat164-primary-20261028` | 原生生命周期接入、导入、迁移、回滚、续办及提交拒绝证明 |
| yijie-desktop | [`eefb2ac92d`](https://github.com/36Dge/yijie-desktop/commit/eefb2ac92d8bff80aad00639794e40e1c1e190f6) | `origin/feat/feat164-primary-20261028` | 技能市场接线、拒绝后新轮次恢复、聊天阅读与媒体预览缓存 |

元仓的技能方案、审计与验收证据、日志跟踪规则及本报告一并提交到 `origin/chore/retirement-baseline-20260905`；最终元仓 SHA 随完成回复给出，避免提交内自引用。

无改动仓库：`yijie-admin-web`、`yijie-api`、`yijie-connectors`、`yijie-coze`、`yijie-infra`、`yijie-knowledge`。它们与各自跟踪分支一致，不制造空提交。

## 提交审计处理

- 保存各仓原 HEAD、分支、改动文件 SHA-256 和 diff；提交前复核原有代码及媒体修复没有被覆盖。源记录使用规范生成器更新，未手改生成摘要。
- 扫描 341 个待提交文件和验收日志，未发现真实私钥、常见供应商/GitHub/AWS token 或长字面 bearer。3 处匹配均为 Host 测试中明确的 `ordinary-local-*` 合成常量；未改成真实凭据，也未将秘密文件纳入索引。
- `yijie-skills/.local/feat174-source-reproduction-*` 为 298 个临时复现输出，新增精确忽略规则，文件原样保留本地；未删除或改动已跟踪的历史复现材料。
- 元仓通用 `*.log` 忽略规则会遗漏 FEAT-174 报告引用的 35 份验收日志。为该特定证据目录增加例外，随报告和原有 SHA 清单一并提交；不提交运行缓存、二进制、密钥或日常数据库。
- 修正技能契约 generator 的一处真实行尾空格，并重新生成全部消费锁。Runtime patch 的 5 处单空格是 unified diff 的空白上下文标记，原样保留；逐行确认 patch 新增的源码没有行尾空格，其余源文件执行暂存区空白检查。验收日志保留工具输出的末尾空行，未为通过空白检查而改写证据字节。
- Runtime 提交后用 `generate-runtime-skill-marketplace.mjs --sync` 记录实际 Runtime commit；Skills 提交后用既有资源同步脚本刷新其来源 commit；Host 提交后用 `native-skill-build-candidate.mjs --freeze` 绑定完整 Host 提交并验证 649 个源码输入。资源内容与固定 Runtime binary 不变。

## 本轮提交前验证

| 范围 | 结果 |
| --- | --- |
| Desktop 改动前端 | 11 个测试文件，350 项通过、7 项按安全或 feature/环境条件跳过；41 个受影响 TS/Vue 文件 ESLint、`vue-tsc --noEmit` 通过 |
| 开发资源装配 | 1 项正常 staging/reopen 用例通过；源码资源与接线检查通过 |
| Contracts | 6 项技能目录/拒绝证明用例、两个 OpenAPI lint、Runtime 与 Host/Desktop/Skills 的同源生成检查通过 |
| Skills | 移除、新增、屏蔽、空目录四个正常发行变体通过 |
| Host | 4 个 Session/HTTP 定向用例、受影响包 `go vet` 通过；执行源码与先前 34 项真实 Runtime/迁移/回滚/冷启动验收保持一致 |
| Runtime | 新增 Shell/Python 脚本语法、固定产物/补丁/schema 来源检查通过；canonical `codex-rs/` 未改 |
| Git | 暂存文件检查、原改动保护及各仓远端 SHA 核对；无 force push |

详细功能验收保留在 [FEAT-174 最终报告](../features/FEAT-174-native-skill-marketplace/11-six-fixes-verification.md) 及 Desktop 的媒体、历史修复、会话阅读缓存报告。本轮没有重复执行付费调用、完整 GUI、全部原生/后端/历史回归或禁止的故障/攻击测试，没有重启或关闭在用客户端和服务。前述功能报告中的“未 commit/push”表示其当时状态，本次 Git 授权与结果由此报告补充。

整体变更仍按 FEAT-174 的最高 `contract-impact=breaking` 管理；媒体/阅读缓存保持原记录的进程内展示边界。所有候选继续为 local / release=false。本次仅推送现有分支，不创建 tag，不部署、不签名、不晋升生产支持版本。

本轮命令日志和机器状态位于 ignored `.local/git-sync-audit-20261114/`。已提交的历史验收日志不重写、不裁剪，也没有把中间失败或未执行项目标为通过。
