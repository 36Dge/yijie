# 过程展示真实验收与修复（2026-10-22）

状态：真实复验已完成（26 秒），四项展示检查通过；最终同步撤销竞态补丁、标准重建及真实历史复核均已完成。各项覆盖限制见验收矩阵。
Profile：demo_fast / local。用户要求 Kimi-K3、完全访问权限，重新执行
“从 5 个重要的维度对比杭州与苏州这两个城市？”，发现问题继续修复，非破坏性验证。
本记录接续 `conversation-process-fix-20261022.md`，不改写上轮“0 新真实模型回合”的历史结论。

## 范围与来源

本次修复 `contract-impact = none`：仅调整 Desktop 内存中的实时展示标记，以及 Host 原有
原生助手指令的文字；不新增/重解释 HTTP、SSE、IPC 字段、权限、工具、Runtime 生命周期或
持久记录。普通助手指令仍通过既有 baseInstructions/developerInstructions 通道发送，权限
策略与字段语义不变。沿用上轮版本化显示契约和 local candidate 来源；无 Runtime 修改。

所有源码相对本轮开始的基线保存在
`CrossBSD/.local/audits/conversation-process-live-20261022/baseline.json`，保留此前未提交改动。
真实 App 起始构建 receipt 的 1104 个输入文件无漂移。仅从正常产品入口发起验收；
不 seed 产品历史、不构造真实工具调用或模型输出，不强杀、不改权限、不注入攻击样本。

## 首次真实回合：未通过

- Desktop session：`01a1642f-f47d-7e22-9d77-220421ccc324`。
- Runtime thread：`01a1642f-f4b8-70b2-bd94-885fc45fa553`。
- Runtime turn：`01a1642f-f512-7fe2-95b2-ebd97a2d567a`。
- 实际配置：`kimi-k3`、`max`、summary `auto`、approval `never`、sandbox `danger-full-access`。
- 实际产生 6 次网页搜索、6 条 reasoning Item（每条 summary 文本均为空）和 6 次 exec_command；完整原生记录保留。
- 网页活动已显示为“已搜索网页”；普通主过程没有未知内容警告。空摘要 Item 进入详细过程。
  初次元数据中的相同摘要指纹是序列化数组的指纹，不能据此声称存在重复的非空文本；
  后续逐条长度检查已补入元数据。真正的非空重复摘要使用原截图对应真实历史复核。
- 发现实时展示间歇消失：“已处理”变成“上次记录为进行中”，停止入口消失；下一条原生事件
  到达后又恢复。Native 没有在这期间把 turn 标成完成。
- 模型自行生成 HTML，偏离了原始普通比较问题。含空格路径未加引号的命令实际失败，shell
  组合命令的最终退出码仍为 0；没有把真实输出删除或伪装成成功的城市回答。
- 通过 App 正常 Cmd+Q 退出，Runtime 记录 `turn_aborted / interrupted`，App、Host、Runtime
  均正常退出，无强杀。首轮没有完成答案，不能算真实 E2E PASS。
- 误创建的 `/Users/jack/Library/Application` 是 0 字节普通文件，birth/mtime 与该条错误命令
  的 `2026-10-22T15:20:27.680452Z` 一致；确认后可逆移动到审计目录 quarantine 保存。
  未删除或改写原有用户文件；正常受管任务工作区中的生成物仍保留。

## 两项后续修复

1. `yijie-desktop/src/stores/chat.store.ts`：已有 native live observation 在普通 readonly resync
   中被 `phase != streaming` 的 watcher 清掉。新逻辑只在同会话同步成功、原观察仍为原生
   inProgress、无终态或诊断时恢复该内存标记；新加载的历史不能建立 live observation。
   同步失败、无效事件、控制面缺口、权限撤销和切换会话仍清除标记。使用原有 store 和读取链路，
   无第二套执行状态机、自动重试或生命周期封口。收尾检查进一步复现“读取途中收到失效通知”
   的竞态，使用内存撤销版本阻止同步完成后恢复过期观察；测试先 FAIL，再修复 PASS。
2. `yijie-agent-host/internal/codex/runtime_permissions.go`：原普通任务只声明“coding assistant”，
   没有清晰说明普通问答的交付方式。本次保留原权限文字，改为通用助手，并要求普通问题/解释/
   比较直接在对话回答；只有请求或必要时才创建文件、网站、应用或图片。工具能力和完全访问
   不改变用户请求。工具前先给简短公共进度，实际需要 shell 时正确引用路径。
   这是提示约束，不是工具封禁；单次错误行为不足以证明角色文字是唯一原因，复验继续看实际输出。

只读同步问题先由正常事件单测复现 FAIL，再修复。213 项相关前端测试、全量 ESLint/类型检查，
Host 原权限模式/专家指令组合/原生推理配置测试和 go vet 已通过。覆盖正常通知触发同步、手工同步、
结束后清理、失败时撤销及冷历史不能变成实时状态。

## 修复后真实复验：通过

- 通过 App 正常新建任务，只发送原问题一次，没有追加诱导模型制造重复或空命令的提示。
- Desktop session：`01a16446-eca7-7971-9bdd-80d2d386e455`。
- Runtime thread：`01a16446-ecea-7b42-8629-9bb7ed6cf9a6`。
- Runtime turn：`01a16446-ed49-7b41-93fb-142b36144d0b`。
- 配置实证：`kimi-k3`、`max`、summary `auto`、approval `never`、sandbox `danger-full-access`。
- `task_started`：`2026-10-22T15:42:12.301Z`；`task_complete`：`15:42:38.470Z`。
  原生耗时 26.169 秒，UI 显示“已完成 26s”。
- 实际 1 次 `web_search_call`、1 条空 summary 的 reasoning Item、0 次命令调用、1 条
  phase 缺省的 assistant 最终回答；最终回答为 5 个维度的表格和文字建议，无网站/文件交付偏离。
- 过程折叠后保留最终答案；展开后为“已搜索网页”，进一步展开可读搜索词。原生空摘要 Item
  留在“查看详细过程（1 条记录）”，没有在主过程渲染空摘要或警告卡片。
- 本次实际共发起 **2 个模型用户回合**：首轮正常中断、修复后复验完成。没有另发 Codex 请求。

## 四项验收矩阵

| 优先项 | 真实 UI 与记录 | 结论与覆盖限制 |
| --- | --- | --- |
| 网页搜索显示未知 | 新复验 1 次 native search 正确显示网页图标、“已搜索网页”及搜索词 | 新链路通过。旧 v2 未存网页类型的记录仍保留为详情中的未知类型，不猜造/回写历史 |
| 重复摘要 | 原截图会话 `01a163b5-cb07-78f1-affc-a77e0e613418` 的第二条重复摘要显示为默认折叠的“重复摘要（原始记录）” | 实际旧历史和定向测试通过；本次两轮只产生空摘要，没有新触发非空重复 |
| 空命令卡片 | 同一旧会话 3 条成功且无输出命令收进详细过程；展开显示真实退出码 0 和“命令已结束，无可显示输出。” | 实际旧历史和定向测试通过；复验 0 次命令，不伪造新执行样本。首轮真实有内容的命令仍保留在主过程 |
| 进度消息分类 | 旧会话阶段文字在“处理过程”；最终答案单独保留。新复验 phase 缺省的最后一条可读回答正确留在答案区 | 实际历史及新复验通过；新复验没有独立公共进度文字，不能声称验证了新的 commentary 流 |

真实复验完成后，正常 Cmd+Q 退出（launcher exit 0、端口释放），通过 canonical
`pnpm tauri:demo-fast:app --reopen` 的 same-build 校验重开；同一 session 恢复完成状态、
26s、五维答案及网页活动，权限仍为完全访问、模型仍为 Kimi-K3。
最后增加的同步撤销版本补丁不改变投影和原生执行；其后仅标准重建并复核这条真实历史，
没有为了该内存竞态再消费一个模型回合。最终构建实际打开了同一成功会话，完成状态、搜索行、
答案和模型/权限均正确；receipt 全部 1104 个源输入无漂移。

## 验证记录与未执行项

- 最终前端定向测试：5 个文件、213 项 PASS；全量 `pnpm lint`（ESLint、vue-tsc）PASS。
- Host 原权限模式、专家指令组合及原生推理配置的定向 `go test` 与 `go vet ./internal/codex` PASS。
- 设计文档构建 PASS；canonical App 构建/来源检查及正常同构建 reopen PASS。
- 收尾第一次直接使用 Vitest 路径过滤时未带 canonical 排除项，误收集 `.local` 中旧源码副本，
  32 项旧副本组件测试失败（Vue runtime 不一致）；保留日志，不当作当前源码 PASS。
  按项目脚本的 `.local` 等排除规则重跑，实际当前 5 个文件 213 项全部通过；未改旧副本。
- 没有强杀、可执行文件替换、权限破坏或攻击注入。仅 normal UI、标准构建、普通内存事件测试、
  只读事件元数据核对；未执行历史故障注入/攻击型整套验收，故不声称全项目全套测试 PASS。
- 前一轮记录的全量 Host `make lint` 因既有脏契约源码的 clean-checkout 门禁受阻，本轮未弱化或绕过。
- 未审计城市对比答案全部数据的准确性；新答案未像 Codex 截图一样给出充分可点击引用，
  这是模型内容质量与引用生成的后续差异，不计为这四项过程展示验收的通过依据。
- 没有提交、推送、发版或修改 Runtime；交付为现有 working tree 上的可复现 local/demo_fast 开发构建。

## 对照口径

对照用户原 Codex 截图及已审计原始元数据，不另发一轮 Codex 模型请求。
Codex 参考显示的是公开进度文字和紧凑搜索活动；不把它描述为原始内部推理。
易界可对齐展示层，但模型是否给出公开进度、重复公开摘要或选择命令是独立的实际行为。
真实重复和命令仍需保留，不能靠删除记录做出“与 Codex 一样”的假象。

## 证据

本地目录：`CrossBSD/.local/audits/conversation-process-live-20261022/`。
原始 Runtime rollout 不复制到报告。`first-run-metadata.json` 只记录安全的事件身份、类型、
数量、摘要指纹和命令摘要；`preflight.png`、`running-01.png`、
`live-observation-lost.png` 记录实际界面。`cleanup.json` 记录可逆清理依据。

`acceptance-ledger.json` 汇总两次真实尝试；`retest-metadata.json` 记录第二次原生配置和事件。
`original-history-main.ax.txt`、`original-history-details.ax.txt`、`original-empty-command.ax.txt`
记录原问题历史的分类、去重和可展开空命令。`same-build-reopened.png` 记录正常同构建重开。
`final-build-process.png`、`final-build-process.ax.txt` 是最终构建的真实历史展示，
`final-verification.json` 保存源输入与 UI 核对结果，`final-source-delta.json` 确认本轮改动范围，
其余此前脏文件未变、所有仓库 HEAD 未变。测试误收集旧副本的失败日志与最终定向 PASS 日志均保留。
