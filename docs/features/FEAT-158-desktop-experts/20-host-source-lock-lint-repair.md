# Host 固定来源与全量 lint 修复

2026-10-16，用户要求解决19记录中的Host来源锁阻断，严格遵守现有规范、不得降低/绕过门禁，保留原专家和历史，重新检查。

`contract-impact = none`：本轮只修正Desktop开发工具的历史来源目录选择，不改变固定Contracts/Host Git对象、摘要、generator、运行候选验证、应用wire、权限、数据库或专家内容。实际Host、Skills、Contracts源码与原dirty工作区不改；不需要为消除dirty状态替用户提交，也不重置/回退开发目录。

## 根因与方案

默认 `make lint` 在 `check-agent-host-skills-contract.mjs` 的 `Agent Host checkout is not clean` 失败。该检查实际用 `git show <固定完整commit>:<path>` 读取历史合同/Skills消费锁，却默认拿持续开发的Host sibling做干净状态检查。后续v4历史检查也有同样选择问题。固定历史契约基线与当前应用构建来源是两项不同验证，不能为让历史检查通过而刷新锁到新HEAD。

复用工程2026-10-03已有的Skills来源选择：提取共享 `resolve-pinned-checkout.mjs`，原Skills入口保持兼容，Host历史Skills/v4及普通Skills双渠道资源消费者按各自完整commit选择已有精确HEAD副本。显式来源不替换，副本缺失/HEAD不同则停止；选择器不下载、checkout、修改锁或忽略dirty。原消费者继续核对干净状态、canonical origin、完整Git对象、provider锁、内容摘要和生成物。资源CLI的 `--agent-host-root` 显式值仍优先，未指定时不提前填入浮动sibling。

两份本机历史参考为 `.local/agent-host-pinned-1b7bfd1`、`.local/agent-host-pinned-96b1fa1`，分别固定原Skills v1与v4的完整Host提交。使用独立detached sparse worktree，仅展开两份正常文本锁，避免物化历史危险归档或故障fixture；其余锁定Git对象仍由原检查器读取。新建no-checkout副本的空索引先在sparse模式下正常初始化，只有最终工作区干净才进入检查。原Host HEAD/分支/文件保持。

v4及资源同步的原local candidate路径仍验证实际Host build checkout，不走历史副本；当前FEAT-158完整source snapshot、原权限来源和generator门禁保留。默认历史基线通过不能冒充当前执行来源通过。原v4测试中的旧sibling HEAD字面量断言改为验证固定对象和执行前后HEAD不变，不把新HEAD抄进期望值。

## 验证记录

证据根为 Desktop `.local/host-source-lock-repair-20261016/`。`source-baseline.json` 保存五仓HEAD、分支、远端、状态与全部受版本管理/未忽略文件摘要。

| 检查 | 实际结果 | 证据 |
| --- | --- | --- |
| 默认完整 `make lint` | PASS，exit0；未加临时Host/Skills路径或local候选环境替代默认检查，完整执行generate:check、ESLint、Rust fmt、all-targets Clippy | `lint-final-verified.log`（此前成功记录亦保留） |
| Skills/Host来源选择与固定契约 | 18+5=23项PASS；v4文件另9项不在本次source focused选择内 | `source-tests-final.log` |
| 双渠道资源及发布边界 | PASS，原38项、5/9/7/9/8分类、各归档/来源/overlay边界保持 | `skills-final-verified.log` |
| 显式指定当前dirty Host给旧契约检查 | 按预期拒绝，exit1：`Agent Host checkout is not clean` | `explicit-dirty-source.log` |
| 显式指定dirty Host给双渠道资源检查 | 按预期拒绝，exit1；未静默改用缓存 | `resource-explicit-dirty-source.log` |
| 当前专家Host真实source snapshot/权限消费链 | PASS，原local/demo_fast/专家候选条件下检查实际开发Host；不启动Runtime或模型 | `current-host-candidate.log` |
| 当前Host候选的普通Skills资源链 | PASS，保持相同实际build checkout，不使用历史副本 | `current-host-resource-candidate.log` |
| 历史副本作为可执行候选 | 按预期拒绝，缺失当前权限来源文件，未把历史基线当作新专家构建资格 | `historical-source-not-executable.log` |
| Host lint、设计文档build | PASS | `host-lint.log`、`docs-build-final.log` |

失败记录未覆盖：`lint-before.log`为原阻断；`skills-boundary.log`记录补查发现的第三入口同类问题，修复后由final日志复验；第一次定向Vitest命令按子串匹配到 `.local` 中前期独立源码副本，执行了那些副本的旧测试并失败（`source-selection-tests.log`）。修正测试命令为明确排除 `.local` 参考材料后，仅当前仓库指定的4个测试文件23项通过；没有修改Vitest全局门禁或历史副本，也不把第一次失败说成通过。此范围限定不用于完整 `make lint`。

补充检查：元仓lint与50项测试、受影响仓库diff空白检查通过。`gate-preservation.json`逐函数证明12个原来源/摘要/权限验证函数与修复前字节一致，默认完整lint未设置Host/Skills目录覆盖或local候选环境。另增加显式无效来源不可回退的测试，保持失败关闭。

## 数据与已有工作区

`source-preservation.json`逐项证明：五仓HEAD、分支、远端都不变；Host、Skills、Contracts全部源码字节及已有未提交修改保持。本轮Desktop只新增/修改来源选择器、三个消费者、对应测试和开发说明，元仓只新增本报告。原所有契约/资产/source snapshot锁均不刷新，原专家UI、Rust/数据库、Host运行代码和专家内容没有改动。

`expert-history-preservation.json`完成只读文件核对：原8份Runtime历史不变；前轮基线中77份旧安装内容/收据（排除3份正常操作日志）不变；当前6个已安装专家版本的101份资源逐字节等于固定归档，包括小红书/跨境0.1.1及保留的0.1.0、漫剧0.1.0、原京东0.1.3。manifest仍为 `afada34e6aa816b4173c390b2a290fa16d8a5bf6b656949531f68e04b3c23847`。

本轮没有重启客户端、打开/写入SQLCipher或Host数据库、改写安装收据、重发任务或新增模型调用。数据库逐行保留和实际专家功能结论仍以19的原证据为准，本轮工具修复不冒称重新做了模型验收。

未执行强杀、权限破坏、攻击注入、危险归档或运行时替换。没有运行含这些行为的未筛选全库测试；完整lint与全量故障测试不是一回事。没有提交、推送、tag、签名或发布，远端CI未运行。本轮工具修改会被既有packaged源码回执发现；未来需要同构建 `--reopen` 时，应先按正常canonical入口重新构建，不改旧回执来掩盖源码变化。
