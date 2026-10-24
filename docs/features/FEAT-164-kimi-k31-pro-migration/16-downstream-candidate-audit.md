# FEAT-164 下游候选实施与审计（2026-10-25）

> 2026-10-25 用户已明确恢复，沿用 20 元及搜索/图片授权。当前进度与预算边界见 [18 恢复实施记录](18-resumed-g2v.md)；17 保留暂停时历史状态。G2V 尚未通过。

当前结论：已完成原隔离清单的三仓本地提交，并继续实现默认关闭、独立 App 身份、仅支持新建数据目录的最小纵向候选。G2A 已通过；G2V、S1—S4、三项 final 均未通过，整体功能仍未完成。没有推送、发布或日常库迁移，真实模型请求为 0。

## 本地提交与隔离

| 仓库 | 本地提交 | 范围 |
| --- | --- | --- |
| yijie-codex | 57753db451b29a49315ddcb6449ca146171c4de7 | 原清单 6 文件，独立 Runtime 候选 |
| yijie-contracts | b0060c8bc4fb924cec14d98b193c32c69482b7b7 | v2 模型源、Runtime 投影、生成物与比较工具；共享文件只提交 FEAT-164 段落 |
| yijie | 17345c91faf44dabb3b631b2d977ecefb85d6179 | 当时的 FEAT-164 包、首次审计、项目记忆的 FEAT-164 段 |

提交证据见 [local-commit-audit.json](evidence/local-commit-audit.json)。元仓提交前 whitespace 检查报告 3 份原始日志末尾空行；保留原始日志，没有改写失败证据，也没有将该检查写成通过。

后续 Host 23 文件、Desktop 33 文件改动尚未提交，见 [下游隔离清单](evidence/downstream-review-scope.json) 与两份 FEAT-164 专属差异：[Host](evidence/yijie-agent-host-feat164-only.diff)、[Desktop](evidence/yijie-desktop-feat164-only.diff)。这些差异以本轮起点工作区为基底，不能直接把整份共享文件加入暂存区。9 个原本已有改动的共享文件，逐一反向移除本轮差异后，原内容摘要均与进入本轮时相同，证据见 [保留核验](evidence/downstream-partial-preservation.json)。

又在临时 index/source 中将专属差异应用到各仓干净 HEAD：两仓均能应用；Host 的 FEAT-164 定向测试和 Desktop 候选 Rust/前端编译均通过。实际工作区和 index 未改变，临时源正常清理；见 [隔离源验证](evidence/downstream-isolated-source-results.json) 与 [前端结果](evidence/desktop-isolated-renderer-result.json)。其中未配置 Runtime 的隔离源测试明确 SKIP 本机集成；其独立实际执行证据另列。最终复核 12 仓 index 为空、分支未变，483 个范围外既有文件内容/权限未变化；两份旧 Runtime binary、6 份旧 patch 摘要保持，见 [最终保留核验](evidence/downstream-final-preservation.json)。

## 已实施的最小候选

- Host/Desktop 从上述 Contracts 的真实 Git 对象同步各自独立 v2 DTO、schema 和来源锁；保留原有 v1 生成物。历史已知身份与可执行身份分开。
- Host 新增显式候选开关、精确 Runtime 产物检查和独立受管配置；候选只接受新目录，不自动改写旧配置。v2 catalog/selection 与普通 start/resume/turn 链路接线；活动身份和当前 Runtime readiness 分开判定，退役 K3 拒绝新执行。
- Desktop 新增默认关闭的 Cargo/Vite 开关及独立 bundle ID `com.yijie.ai.feat164-kimi-k31`。新建任务展示 Kimi K3.1 Pro；历史身份仍可识别。旧 market/expert/plan 契约族不接受新身份，避免未完成版本化时泄露新枚举。
- 私有 SQL 38 扩展三张表的身份约束，保留旧值、revision、operation、未知意图、级联及既有无 outbox FK 语义。仅候选新库实际使用；既有日常数据库不进入迁移。迁移兼容测试不是日常迁移资格。
- canonical launcher 新增 `--packaged --kimi-k31-pro`、`--prepare-only`、`--reopen`。Host、Runtime home 和 App 数据身份独立；候选关闭 market/experts/artifact/workflow/image generation。重开前校验源码、构建环境摘要、整份 App bundle、Host、Runtime 与 manifest 的产物回执，不重新构建。
- 增加无正文的观察分类器和协作取消控制；只有普通状态输入，不发送进程终止信号、不替换可执行文件、不破坏权限。分类器单测不等于完整 Harness 资格。

候选仍有明确边界：尚未实现旧会话新模型选择/recover、旧任务未发送取消、计划退役及重新授权、全部辅助模型截止点、最终多种功能组合资格。当前 Host/Desktop 构建包含保留下来的既有工作区源，属于可审阅工作树候选；不是不可变实现提交，不可用于宣称 G2V。

## 实际验证

| 验证 | 实际结果与证据 |
| --- | --- |
| 原源候选 | 已接受的离线比较按 RCA 执行一次有界复核 PASS；G2A 机器检查 PASS，见 [g2a-source-freeze.log](evidence/g2a-source-freeze.log) |
| Host | v2 schema、HTTP auth/header/retired 准入、选择历史/readiness、Runtime 配置测试通过；相关包 `go vet` 通过。原先空 selector 仅记编译检查，不计测试通过 |
| 实际 Runtime 本机协议 | [host-native-candidate.log](evidence/host-native-candidate.log)：新 Kimi→MiniMax→新 Kimi，同线程 3 次 loopback Responses，退役身份拦截，正常清理；不是供应商资格 |
| Desktop Rust | 候选 3 项测试 PASS，包含三表数据保留和 canonical 15/29/37/38 迁移；候选 clippy `-D warnings`、fmt、默认功能编译均 PASS |
| 前端 | [desktop-model-client-tests.log](evidence/desktop-model-client-tests.log)：实际命中 10 文件、23 测试；完整 `pnpm lint`（含类型检查）PASS |
| 安全观察控制 | [verdict-controls.log](evidence/verdict-controls.log)：4 测试 PASS，覆盖正例、归因/歧义、封闭无正文输出、正常完成/协作超时各一次 cleanup。完整 Harness 资格仍 NOT RUN |
| canonical 构建 | 独立 App 构建 PASS。首轮锁字段读取错误已修正，失败日志保留；无运行时二进制替身。无签名本地开发产物，不是发布产物 |
| App 普通本机联调 | [local-assembly-result.json](evidence/local-assembly-result.json)：2 个用户任务、2 次 loopback 请求，均为 `kimi-k3.1-pro / max`；完成、保存、同会话重开、续聊均可见；App 与 fixture 正常退出，端口释放 |

本机联调仅发送普通合成文本，临时凭据也是普通合成值。Fixture 只接受本机连接，不代理供应商，不实际执行模型工具；`builtin_search_offered=true` 仅表示请求包含该工具声明，不能作为搜索已运行的证据。截图和 AX 证据均来自独立候选 App 的合成对话。

发现并修正了两项验收准备问题：

1. UI 工具最初在 canonical build 完成前自动打开 App，缺少运行环境。该实例没有发送 Responses；正常退出后，等待 Host 就绪再选择 App，真实 canonical 链路通过。原日志保留。
2. 原重开方式再次构建，App binary 摘要变化，Host/Runtime 不变。因此该次只能证明同源数据恢复，不能证明同产物重开。补充专属 packaged receipt 和无重建 `--reopen`，其独立验证见 [同产物重开记录](evidence/local-same-build-result.json)。不回填或覆盖此前不相等的事实。

## 未执行与下一道门禁

G2V 仍 NOT RUN：缺少 Host/Desktop/Harness 不可变提交、完整安全 Harness 资格和独立真实模型预算。当前的 loopback 与源码测试不得替代这三项。S1—S4 不越过该门禁提前宣称完成。

未执行真实账户查询、供应商 HTTP、付费图片/搜索、商家平台请求、生产数据迁移、攻击 fixture、强杀或权限破坏。原因分别是没有独立账户/费用授权，或长期安全条款明确禁止。影响是目前尚不能确认供应商可用性、真实生成/工具行为、旧数据完整迁移及最终产品资格。

后续按以下顺序继续：

1. 审阅本报告和下游专属差异，明确新增 Host/Desktop/Harness 本地冻结范围；原三仓提交已经完成，不重复索取许可。冻结前必须检查与保留工作区前置改动的依赖，不能将 FEAT-162/163 顺带提交。
2. 完成 H-F164-LOCAL 的实际观测点/内容无关判定/正常超时与清理资格，冻结其真实 commit/digest。当前 4 个单测仅是准备材料。
3. 单独确认真实 Kimi 最小 G2V 的账户、用户回合、全部 HTTP/辅助调用、token/费用、搜索/图片边界和停止条件。原预算仍为 0；旧计量器只允许旧 K3，且可能注入 `max_output_tokens`，必须先形成可审阅的新候选，不能直接复用旧额度或修改后声称原始产品参数通过。
4. 有资格和预算后跑 canonical App 的真实新模型→原生返回→保存/同产物重开，更新 G2V；通过后才继续 S1→S4 和三个独立 final。
