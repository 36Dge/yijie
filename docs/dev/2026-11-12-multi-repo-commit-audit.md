# 2026-11-12 多仓提交审计

用户本轮明确授权审计本目录全部仓库，并执行 `git add`、自行总结提交信息、`git commit -m` 及推送到对应远端分支。此授权覆盖本次 Git 操作；此前 FEAT-172 记录中的“未授权提交/推送”保留其历史时间语义，不被改写成此前已经获准。

## 范围与来源

按 `repos.yaml` 核对元仓及 11 个兄弟仓。开始时共 4 个工作树有改动：Contracts 18 个文件、Host 42 个、Desktop 81 个、元仓 37 个；Desktop 另有未推送提交 `275b72b17dcb1a63cf78042915968d518e867938`。其余 8 仓无改动，也无待推送提交。

审计前已更新各仓 origin 跟踪分支，均未落后或分叉。未切换分支、重写历史、调整远端或强制推送。记录了各仓初始 HEAD、文件摘要，并在提交前复核没有其他任务并发改动。新增内容为文本源文件、契约、测试和文档；常见私钥、API/GitHub/AWS token 与长字面 bearer 扫描未发现命中。

本轮提交身份如下；前三仓已推送并通过 `git ls-remote --heads` 核对远端 HEAD。元仓方案、ADR、证据与本报告在 `chore/retirement-baseline-20260905` 上一并提交。

| 仓库 | 本轮提交 | 远端分支 |
| --- | --- | --- |
| yijie-contracts | `cca445ca30c8d13b11185212b3d709bae67cf4aa` | `origin/feat/feat164-primary-20261028` |
| yijie-agent-host | `da19be66b80dd3235a7622983e58f471a58da9ee` | `origin/feat/feat164-primary-20261028` |
| yijie-desktop | `ed5ee7a52ddef30006ad91d3f9231ebd7c17f065`，同时包含此前未推送的 `275b72b` | `origin/feat/feat164-primary-20261028` |

完整跨仓改动按最高风险为 `contract-impact=breaking`：FEAT-172 停用旧生图入口及用户录入凭据流程，改为本地内置 MCP 和运营方预置凭据；固定 Runtime canonical 协议不变。文档连续阅读、受限图片投影与原生复制分别保留既有授权/身份/持久来源边界。元仓本身为 `contract-impact=none`，只记录方案和验证，不改变任何运行接口或状态。所有候选继续标记 local/release=false；本次 Git 推送不构成 tag、公开部署或生产发布批准。

## 审计修正

1. ChatPage 测试仍期待“正在建立索引”过程文字，与已确认的附件交互不符。改为确认真实 composer 仍处于导入忙碌状态、添加入口禁用，且不显示已取消的过程文案。
2. catalog 测试硬编码旧 commit，并要求当前 sibling HEAD 停留于旧位置。改为读取既有 FEAT-164 receipt 的 `source_commit`，通过当前开发入口同用的 retained-source helper 验证固定 Git 对象，同时断言 sibling HEAD 与三份 catalog/receipt 字节不变。
3. `document-build.candidate.json` 落后于当前 Host：7 个已登记文件摘要不同，并遗漏 2 个新增正常回归文件。使用现有 `document-build-candidate.mjs --freeze` 更新，随后调用 `verifyDocumentBuildCandidate` 成功核对全部 570 个 Host 输入，基线为本轮 Host 完整提交。未手改摘要或发布来源锁。
4. media 验收计数脚本先做数值比较、后检查额度类型，缺少或非整数额度会触发 TypeError。调整为先校验整数与范围，再检查追加授权，不改变有效额度或放宽准入。
5. 图片规范和此前审计表仍写“灰色描边”。补充最新用户决定：普通、悬停及展开状态均无边框；保留此前历史调整记录及键盘焦点提示。

## 本轮验证

| 范围 | 实际结果 |
| --- | --- |
| Contracts | `node --test tests/generation-workspace.test.mjs tests/media-generation.test.mjs tests/document-runtime.test.mjs`：10 项通过；media Host、document Host/Desktop 同源 `--check` 通过；`pnpm lint` 通过，含既有 Redocly warning |
| 兼容性 | `check-breaking.sh` 对实施前 `d658a2bd5dd6ebd5ae5c79a547489eca205d6ede` 和已发布 `f16a497e1377f45747f8ff9292b4b60cf2027f88` 均通过；不冒称全部历史支持窗口/生产资格审查 |
| Host | app/session/artifact 21 个顶层正常用例带 `-race` 通过；显式专家和内置 MCP 配置 2 项通过；受影响包 `go vet`、Go 格式检查及 Rust adapter `cargo check --locked` 通过 |
| Desktop 前端 | 受影响文件 ESLint 与 `vue-tsc --noEmit` 通过；19 个相关测试文件初跑 442 通过、2 失败、7 跳过。两项失败即上表的旧断言，修复后定向复跑 2/2 通过；修复文件 lint 通过。未把初次失败改写为一次全绿 |
| Desktop 原生 | 当前 `kimi-k31-pro-candidate` feature 下 4 个连续文档用例、1 个有界图片投影、1 个已绑定图片读取、1 个私有 pasteboard 图片复制用例，共 7 项通过；未改动用户剪贴板 |
| 开发入口 | 7 个 Python 正常配置用例、launcher Shell 语法、全部修改 JSON/Python 语法检查通过；文档来源 receipt 再验证通过 |
| 元仓 | `pnpm lint` 与 57 个文档治理测试通过；FEAT-172 的文档结构及 D4 声明校验通过（不是本轮重新执行真实验收）；提交前逐仓 `git diff --check` / staged diff 检查通过 |

前一轮同一图片按钮代码的 1180×760 浏览器验证已经检查亮/暗主题、悬停、菜单展开、边框为 0 以及键盘焦点。原生完整客户端与真实供应商验收采用 FEAT-172 原有分次证据，本轮没有重跑付费调用或重启客户端。

## 已知限制及未执行项

- 完整安全生成 `node scripts/generate.mjs --check --skip-skill-fixture-generation` 仍失败，唯一差异为保留族 `compatibility/runtime-chat-models/source.lock.json`。旧生成器以当前 Runtime HEAD 替换其原记录的 `runtime_source.base_commit`；与实施复审记录一致。本轮不重写该来源锁以掩盖失败。本次 media/document family 和消费者检查通过，不等于全量生成通过。
- Rust 格式检查按仓库 edition 区分；共享生成代码保持 generator 的 2021 格式，不能按 Host 2024 edition 手改生成物。Desktop `application.rs`、`attachment.rs`、`database.rs` 的全文件格式差异已对初始 HEAD 复核为既有问题，本轮新增/修改片段未引入新的格式差异；未批量格式化无关源码。
- 前端 7 项跳过中，1 项为用户禁止的 DOM 注入 fixture；另外 6 项由既有原生/模型候选环境条件跳过。原生命令同时加载 `scripts/test-safety-exclusions.json` 的排除名单，仅执行上述正常用例。未执行攻击注入、危险归档、权限破坏或强杀类验证，相应防御结果不作通过声明。
- 未运行全部仓库回归、真实模型/Seedream/LinkFox调用、凭据授权交互、生产部署、安装包/签名/公证；未修改或替换运行中的二进制、数据库或服务。本轮验证不代表上述范围已经通过。
