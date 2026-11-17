# 2026-11-17 多仓提交、缓存清理与日常版本接入

用户本轮明确授权审计全部待提交改动、逐仓提交并推送、清理无用构建产物，以及将当前业务逻辑接入日常服务。此前验收记录中的“不提交、不推送”是当时的操作边界；本轮授权不改写那些历史事实。

本轮交付按 `contract-impact=semantic` 记录：启用既有 Native 观察生命周期和隔离验收配置改动。维护过程中没有新增业务实现、公共 wire、Runtime 补丁、审批数据库或数据迁移。纯缓存清理和等价来源记录更新为 none。

## 源码审计与提交

检查 CrossBSD 下12个主仓的分支、远端、未提交文件、忽略目录和工作树登记；14个仍存在的附加来源 worktree 均只读检查且干净，保留其来源用途。最初5仓共62个待提交文件全部纳入审计和提交；61份文件保持本轮开始时的原字节，另1份 Desktop Host 构建候选由 canonical freezer 更新来源。没有 reset、覆盖用户源码、改分支或 force push。

| 仓库 | 目标远端分支 | 本轮实现/记录提交 | 最终代码提交 |
| --- | --- | --- | --- |
| yijie-contracts | origin/feat/feat164-primary-20261028 | `1eaa552aee3d4fc70dcb605bc4ad412e13e7f868` | 同左 |
| yijie-connectors | origin/feat/feat164-primary-20261028 | `9321d4a56659403d97f3fcf24ae72d9d6896d441` | 同左 |
| yijie-agent-host | origin/feat/feat164-primary-20261028 | `cf1191a437f876d8f5cf459014b2abce2b6a615e` | `400257c31aff5e51535bceda0689554b7e47f3b3` |
| yijie-desktop | origin/feat/feat164-primary-20261028 | `0564244b4bdb3a15a9898bfebafeae3b19a96d8d` | `45b08d0f94696e6ab5e21d8cd86f15509fe8bc14` |
| yijie | origin/chore/retirement-baseline-20260905 | 既有7份验收文档：`ae29fece51d136c56a3fad0b93377ab0c05fbab6` | 本交付记录另行提交 |

其余7仓（Admin、API、Codex、Coze、Infra、Knowledge、Skills）无待提交源码，不制造空提交；原分支和 HEAD 保持。Runtime 始终为 `5c64ed3f03808639faf7c11674e87636a94ab221`。

审计确认继续复用原生推理循环、tool_search、Code Mode/wait、MCP client、elicitation、线程事件/历史和 `_meta`。新本地协议端是显式隔离验收入口，日常 worker 仍为普通产品模式。65秒仅限制只读观察，不授予执行许可；未知结果不合成成功，逐次批准不变。

**接入时修正的来源缺口：** Contracts 提交后，日常 preflight 正确拒绝 Host/Desktop 的6份旧 `worktree_head` 候选记录。使用 `sync-model-call-surfaces-v2.mjs --local-market-candidate` 同步，逐文件证明仅来源提交号变化，wire/生成代码不变；先固化 Host，再用 `native-skill-build-candidate.mjs --freeze` 更新 Desktop 的实际 Host 提交与源码摘要。两个补充提交已推送；未跳过来源校验或把本地候选改成 release=true。

## 定向验证

- Native：8项安全定向用例通过，覆盖截止点、不续期、普通 SSE 晚到 Item、独立连接释放、重叠观察、原轮 `_meta` 关联及毫秒时间单位；严格 lib Clippy 通过。
- Host：11项顶层定向用例通过，覆盖隔离装配、原生历史/终态、关联冲突、结构化结果和事件缓存读取。
- Worker：默认关闭本地 provider 的1项用例、固定 Codex 来源校验和严格 Clippy 通过。
- 前端：38项组件/composable测试及1项 store 定向测试通过；受影响 ESLint、vue-tsc 通过。
- Contracts：隔离配置及3个 connectors、2个 broker 消费者同源检查通过；首次使用错误 consumer 名称 `host` 的检查失败保留，改用脚本要求的 `agent-host` 后通过。
- 12仓 `git diff --check`、元仓 lint、canonical 日常构建及启动前后来源核验通过。

不是全量回归或生产跨版本资格。构建仍有既有 Vite HMR 配置弃用提示和旧 schema unused-component 提示；本轮严格 Clippy 无告警。不执行安全排除清单中的攻击、权限破坏、二进制伪装或强杀 fixture。没有为本轮维护提交真实供应商/模型任务。

## 清理范围与空间

正常构建退出后，持有原 canonical cache advisory lock，并确认目标缓存没有打开句柄，才逐项删除已记录且 Git 忽略的目录：

- Desktop `.local/cache`：定向测试 Cargo 中间缓存；
- Desktop `.local/build-cache/feat162-v1/19faea4f2fc45066f45469562ace9946953108486d0675da37d53d592f177598`：canonical Cargo 中间缓存；保留锁文件；
- Desktop `node_modules/.vite`；Contracts 两个 Rust 契约测试的 `target`；五处 Python `__pycache__`。

删除时 `du` 分配量合计 **18.9346 GiB**；删除窗口整卷可用空间增加 **18.4782 GiB**，该差值包含系统同时写入，不冒称精确物理归因。工作区 `du` 从69,796,492 KiB降至50,182,840 KiB（约66.56→47.86 GiB）；启动后必要的少量缓存正常重建。

保留日常/验收 Native、Host、Runtime 数据及凭据、Docker volumes、Git 历史与来源 worktree、当前制品/运行资源、固定 Runtime、已审计历史构建、恢复归档和验收证据。旧 `.app`/`.dmg`、Skills 包、文档运行资源和保全副本没有因位于 ignored/bin/dist 就被误删；未确认无用的备份不作废弃判定。未运行全局 clean、volume prune 或强杀。清理后、日常启动前，11项数据/密钥/配置保护记录哈希全部保持。

缓存可由项目标准构建重建；下次确有源码变化时首次编译会变慢。运行制品未删除，清理后的 canonical 启动实际复用 native/helper/Host/worker/media，resources单独核验，前端沿用 Vite HMR。

## 日常版本实际状态

先用 `python3 -B scripts/development-client.py build` 标准构建，未启动 App、任务队列或模型；服务随后由原流程正常停止。锁屏使桌面“易界.app”的 UI 操作被工具拒绝，已请求用户解锁；本轮改用该桌面入口实际调用的同一个 `development-client.py start`，不传任何 acceptance/meter 参数。

日常启动记录 `db806593-1000-457f-bb1a-fc2d78af004b` 已 verified，Native PID83899、Host PID83904、普通产品 worker PID83929、固定 Runtime PID83931在核验时运行。Host `/readyz` 返回 `status=ready`、`runtime_state=ready`。当前 Native SHA-256 为 `1e164a363dd73946d3e2b7421c58a7851c39c62b6b5351f299eff88649074c1f`；Host、worker、媒体和 Runtime 的实际文件摘要均与来源回执相符。

打开句柄确认 Native 使用 `com.yijie.ai/demo-fast-v1`，Host/Runtime 使用 Desktop `.local/demo-fast/{host-home,codex-home}`。没有打开 `market-local-acceptance` 数据；实际 worker 参数为 `--broker-control-stdio`，日常配置的 `YIJIE_MARKET_LOCAL_ACCEPTANCE` 为空。既有配置、技能、专家与连接器启用意图沿用，没有重放验收决定。服务保持运行，后续通过 App 菜单或⌘Q正常退出即可沿原流程停止专用服务。

**未完成的界面核验：** Mac 两次均被工具确认为锁屏，故本轮未直接查看日常连接器页面或做 GUI 抽查，不能把进程/ready/source 核验称为 GUI 验收。此前4类P2的实际覆盖及两个不能自然触发的 SSE 子分支仍以 [实机结果](../features/FEAT-157-desktop-market-connectors/2026-11-17-p2-gui-results.md) 为准；本轮未扩大其通过范围。

## 证据与回滚

私有完整证据位于 Desktop `.local/maintenance/2026-11-17-delivery/`：基线/diff/原文件哈希、12仓远端、全部定向日志、源码保护比较、清理计划与逐项执行清单、空间测量、来源修正说明、构建/启动日志、`daily-running-verification.json` 及真实 `startup-check.json`/`startup-build.json` 回执副本。该版本不生成 `startup-last-success.json`；采集器最初尝试复制此可选文件失败，随后改用实际存在的两份 verified 回执，未伪造记录。

源码回滚须先正常退出，再在相应仓库以新的 revert 提交撤销明确范围，并按依赖顺序同步来源、标准重建；不 force push、不复制替换受审计二进制、不覆盖日常数据。SQL47/Native格式6不降级、不删除决定事实；不支持该格式的旧 reader 不可直接打开当前库。撤销晚到观察修复会恢复原来的刷新缺口，并非修复缺口的替代方案。
