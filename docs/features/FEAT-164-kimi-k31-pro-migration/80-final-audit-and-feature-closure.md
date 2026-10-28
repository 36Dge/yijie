# FEAT-164 第80号：最终审计与需求关闭

2026-10-28。Owner在复审第79号与当前后态后，明确要求“将本轮审计结论落盘，完成 FEAT-164 最终收口……完成检查与本地提交，不改产品或 Runtime。最后关闭 feat-164 需求。”

**结论：FEAT-164 已完成并按Owner要求关闭。** 关闭范围是ADR-0022限定的个人本机交付，包括Kimi K3.1 Pro替换、历史与授权保护、S1—S4、D1—D5、原主工作目录构建运行、已批准旧目录清理，以及清理后实际App历史和正常退出验收。批准范围内无开放阻断项、待补验收或继续实施步骤；这不扩大为公开、云端、多人或签名发布。

本轮增量`contract-impact=none`：仅将已核实结论、Owner范围决定和需求关闭状态落盘；不改变跨仓接口、模型行为、数据格式、权限、部署绑定或Runtime。整项需求原有breaking分类和全部历史门禁证据保持。`feature.status`保留`completed`，新增`final_closure.status: closed`记录已完成后的关闭，不使用“未完成验收永久终止”的`terminated`语义。

## 已完成

| 范围 | 最终结论及证据 |
|---|---|
| 模型与全调用面 | 活动Kimi为`kimi-k3.1-pro`，旧K3退役；普通、标题、专家、草案、计划、压缩、允许的子代理及Guardian按已启用范围完成验证。历史身份可读，MiniMax及原Key、权限和审批保护保持。AC-001—010按[当前矩阵](current-acceptance-matrix.md)及各原始来源判定，不把历史模型回合写成本轮执行。 |
| 旧线程、操作与计划 | 显式模型选择、恢复/取消的证明边界、unknown不重发、旧计划重新审阅和授权失效保护完成；历史失败/unknown、原operation及grant事实保留。AC-005/010中完整App正向取消采用下述Owner接受替代。 |
| 日常切换 | D1—D5及G0—G6在已批准的个人本机范围完成，原Home/身份/数据保持；不重跑D3、不覆盖日常库。依据64、66—69及后续来源资格。 |
| 原主目录构建运行 | [76](76-primary-workspace-execution.md)/[77](77-primary-system-quit-root-cause-and-plan.md)已从原`CrossBSD/yijie-desktop`实际源码构建运行，generation为`20261028-02`，不转调旧daily-source。五仓当前本地分支为`feat/feat164-primary-20261028`，不是声称已合并默认分支或推送。 |
| 旧目录清理 | [73](73-final-six-directory-cleanup-completed.md)的两轮74个旧顶层目录清理保留其原始记录；[78](78-old-daily-source-retirement.md)另完成旧`daily-source/20261027-01`及8个worktree移除。当前12仓登记、符号链接及活动入口元数据无旧目录依赖。 |
| 清理后实际验收 | [79](79-post-cleanup-app-history-acceptance.md)已完成一次零模型canonical启动、8会话/11轮实际UI历史、2附件、命令详情和旧计划保护，随后App自身⌘Q正常退出。停止代123→124，活动WAL/SHM0，旧业务及授权保持。此前因锁屏跳过的新来源历史界面项已补齐；原跳过及失败记录不改写。 |

## 本轮只读复核

本轮重新核验并留存[关闭审计证据](evidence/final-closure-audit.json)：

- 当前六仓来源、1,410项源码输入与制品、正常/暂停D5绑定通过；Desktop仍为`24a231f96f08ed077e53f9bd73a2aac93ee6cba8`，Runtime原仓r5不变。
- 当前日常17,401个普通文件与第79号完整退出后快照逐项一致；91份私有证据文件及公开摘要/UI引用哈希一致，无项目进程残留。只读取文件，不通过数据库API打开原日常库。
- 12个原仓无旧目录worktree登记，14,378个符号链接无旧目标，8份当前入口元数据无旧daily-source引用。空的`yijie/.local/daily-source/`父目录保留，不是活动源码或未完成清理。
- 3,701,716,249字节完整压缩归档SHA仍为`7ed1fd6afe1ac8cb7495c7dd04d37c9583a51a9955cc1bce35e539711d10ddbf`；五仓bundle哈希、`git bundle verify`及全部保存引用保持。独立解包/恢复/fsck沿用76/78真实记录，本轮未另解包、删除或重建。
- 七份旧账本及其中两份预占不变，不因关闭需求释放预占、补结算或重置调用次数。原243项meta改动及其它11仓状态保留。

本轮没有启动App、模型HTTP、workflow探测/生命周期操作、产品/Runtime/来源锁改动或推送。第79号的workflow ready仅指其观测时点，本轮不将历史ready冒充新探测。私有完整检查记录位于`yijie/.local/final-closure/20261028-01/`；真实数据、凭据及完整UI文本不进入Git。

## 已接受替代、已移除与范围外

| 分类 | 关闭时保留的准确事实 |
|---|---|
| 已接受替代 | 完整App/WebView正向`never-sent`取消仍为**NOT RUN**。依[57](57-natural-unknown-and-safe-delivery-verification.md)及[58](58-owner-accepted-substitute-and-final-closure.md)的Owner确认，采用正常Repository API的持久取消/正常重开/回执重放，加实际Native输出经生产parser/composable/control的安全分层证据。接受不等于完整App路径实际执行。 |
| 已移除 | 搜索答案正确性、指定页面命中及确定回答质量；亮暗、键盘焦点、最小窗口专项，均为**OWNER_EXCLUDED**。不计为PASS、不再作为待办。搜索sources安全传递、Key、审批、退役保护及业务状态验收仍保留。 |
| 范围外 | 公网、云端、多人、多租户、签名及完整跨平台发布；默认分支合并/推送；启用未采纳的其它需求WIP；额外目录或归档清理。不能从本次关闭推导这些操作的授权。 |

历史失败、unknown、未执行项、原始来源及执行日期全部保留。FEAT-162/163等独立需求不由本需求关闭。

## 日常使用与保全边界

在原`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop`运行：

```bash
pnpm daily:open --generation 20261028-02
```

正常退出后，同命令追加`--pause-kimi`可使用已验收的暂停入口。普通`tauri:dev`保留历史开发语义。仓内`.local`的制品、固定版本资源、数据、备份和证据继续保留；它们不是已删除的旧Desktop源码副本。

后续源码修改需按canonical流程形成新generation、重新取得对应资格及显式绑定，不能刷新旧回执冒充原验收。回退先正常退出、备份和验证兼容来源；归档用于恢复审阅，不直接覆盖日常数据库、不降schema、不重跑D3、不删除/截断WAL。

## 治理检查与关闭

本轮元仓`pnpm lint`、57项`pnpm test`（失败0、跳过0）、7份`scripts/*.sh`语法、Feature claims及`--strict --gate G6`均通过。实际命令、退出码、时间、工具版本和日志哈希已写入关闭审计证据。提交前分离复核通过：27个文档链接有效，2,271份未涉及的历史需求文件逐字保持，243项原改动及11个兄弟仓状态保持；仅本地提交所属文档。

Owner关闭授权来自本轮明确请求；Codex完成与文档编写阶段分离的结构化复核，不声称独立人工评审。关闭后的批准范围内剩余事项为`[]`；无自动续办、补跑模型或重新验收已移除项目的计划。
