# FEAT-136 提交与远端交付收尾

记录始于 2026-09-09；远端核验完成于 2026-09-10（Asia/Shanghai）。当前阶段：**本次实现与验收提交已按 Desktop → 元仓普通推送，远端 SHA 核验通过，CI 未触发。** 此记录区分本地验收、Git 提交和远端同步，不把任一状态替代为另一状态。

| 状态 | 当前事实 |
|---|---|
| 本地验收 | 2026-09-09 八项 Must / local D4 PASS，真实验收发生在工作区候选上，原日期及逐文件 SHA-256 保持不变 |
| 已提交 | Desktop 8bfa5ca284fddb86d7cdd2a406c5041c49367688 已形成，11 个提交文件逐项核验；元仓验收与一致性文档由 4e6645574fdfe7d29f7c551564bf807cf8222d48 固定，35 个文件逐项核验 |
| 已推送 | Desktop 8bfa5ca284fddb86d7cdd2a406c5041c49367688 → 元仓 4e6645574fdfe7d29f7c551564bf807cf8222d48，两次普通 push 均 exit 0，随后 ls-remote 完整 SHA 逐一相等 |
| CI | 两个精确提交的 gh run list 均为空，NOT RUN；当前 chore 分支不匹配 push workflow，且两仓均无该分支的开放 PR；未创建 PR 或手动触发 workflow |

## 本轮复核与提交范围

- 复核开始时，Desktop 11 个改动文件全部与原 D4 证据 SHA-256 相等，没有额外并发文件或已暂存内容。元仓原有 32 个文件是 FEAT-131～136 一致性、FEAT-134 远端记录、FEAT-136 原生调整/验收及四份历史归档；本轮再增加本记录、提交前机器证据及独立交付状态证据，共 35 个文件；新增代码不混入其它仓库。
- 原历史四文件逐字节等于元仓基线提交中的原包。保留日期、旧源提交、prior FAIL、原调用台账和旧验收范围。
- 本轮只追加修正 Desktop 的 docs/chat-native-conversation.md 一句话：明确 D4 在当时工作区候选完成，后续提交/推送另记且不代表重跑 D4。其余 10 个源码/测试文件继续匹配 D4 原哈希。文档的原哈希与修订后哈希均记录于 [提交前机器证据](evidence/delivery-preflight-2026-09-09.json)，不覆盖 [原 D4 证据](evidence/native-command-d4-2026-09-09.json)。
- contract-impact=none；本轮只有交付文档修订和核验，没有产品行为、wire、private IPC、数据库、Runtime 或权限修改。Contracts、Host、Codex 保持干净和原提交，不机械更新消费者 pin。

## 本轮检查结果

- Native 两份来源锁各 11 条，加权限 Contracts 5 条、Host 15 条，共 42 条；与固定 Git 对象及当前工作树 SHA-256 逐项一致。
- 首次直接 pnpm generate:check 未通过：默认 sibling Skills HEAD 488714a8d96f40806a257aae097683815b1dd458 不等于锁定 10c45bec29603b002e861e1499d5b4e684251af5。没有切换或修改该 sibling，也没有刷新来源锁。
- 按原验收环境指定既有、干净的 .local/skills-pinned-10c45be（HEAD 为锁定完整提交），重新执行完整 generate:check PASS。该路径由既有 YIJIE_DESKTOP_SKILLS_DIR 配置支持，仍执行 exact provider、source digest、生成快照和退役引擎检查。
- Desktop pnpm docs:build PASS；元仓 pnpm lint、pnpm test（50/50）、Shell 语法、feature:audit（19 包）及 FEAT-131～136 六个 D4 文档门禁 PASS。原 schema v1 历史提示保持；文档门禁不表示六个需求重新真实验收。
- git diff --check PASS；未新增生成物、锁文件、迁移或依赖。未重跑应用/模型验收或含禁止场景的广泛测试，原源码/测试哈希未变，原本地验收仍按其明确范围适用。
- 远端 URL 为 https://github.com/36Dge/yijie-desktop.git 与 https://github.com/36Dge/yijie.git；目标分支均为 chore/retirement-baseline-20260905。只读 ls-remote 与 gh pr list 已核对；每次推送前再次确认远端基线没有并发前进、本地只有预期提交和干净工作区，未出现冲突或强推。

## 已执行的交付顺序

1. Desktop 11 文件逐项核验、暂存并提交为 8bfa5ca284fddb86d7cdd2a406c5041c49367688，提交信息 fix(FEAT-136): render command items from native facts。
2. 将真实 Desktop commit 写入元仓，35 文件逐项核验、暂存并提交为 4e6645574fdfe7d29f7c551564bf807cf8222d48，提交信息 docs(FEAT-136): record native command acceptance and delivery。原 D4、授权前 preflight 和历史归档字节不改。
3. 保留来源及权限检查，按 Desktop → 元仓使用完整 SHA refspec 普通推送；两次成功并分别核对远端 SHA，无额外 tag、PR、合并或部署。
4. 查询两个精确 SHA 的 Actions，均无运行，记录为 NOT RUN。依据已有授权补充本次远端回执，不将其改写为 CI PASS。

本记录及交付状态 JSON 的补充提交只记录以上已核验的交付提交，不嵌入补充提交自身 SHA，以免产生自引用提交循环。最终承载这份回执的提交及其远端同步由 Git 历史、远端分支和任务最终报告核对；不把尚未发生的推送预写为成功。

用户对“按 Desktop → 元仓顺序提交并普通推送已核验修改，以及必要的交付结果补充提交”明确回复“授权”。本次授权不包含强推、tag、PR、合并、部署、模型请求或启动 FEAT-144；此前 FEAT-134 四个固定提交的授权不作为此次依据。提交前机器证据中的 pending 是授权前时点事实，当前授权见独立交付状态证据。

## 调用与保留限制

本轮无新增模型请求；FEAT-136 累计仍为 **3/10 文本、0 图片**，不转用旧需求预算。Command 最终安全输出策略、冷历史缺项、附件过期、清理未完成、隔离任务缺少普通 Host 映射和旧历史只读均保留。真实旧 v5 Command 样本、dark/精确最小窗口及原后移项仍按验收记录标明限制。

FEAT-144 尚未启动；仍需先明确真实 Tool 的产品入口与权限边界。
