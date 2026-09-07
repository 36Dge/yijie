# S4 验证记录（本轮结论：未通过）

本阶段沿用同一实际请求账本，授权累计上限为 25，实际累计 23，剩余 2。所有真实审批均来自正常 UI → Native → Host → retained Runtime；测试使用普通临时文件及公开网页 HEAD 请求。

## 零付费检查

- Host 新增进程内协议单元测试，验证人工接管保留原 thread/turn/review/action 关联、其它任务不能决策、重复批准只发一次原生 RPC、原生返回失败不能标记批准。测试不启动 Runtime 或模型，其固定输入不作为真实自动拒绝或 E2E 证据。
- 人工接管的原生方法仍为 `thread/approveGuardianDeniedAction`；批准仅注入具体操作授权，不创建新回合，不直接宣称操作已执行。真实原生语义核对沿用 S3。
- 修复审批提交失败提示被下一次成功轮询过早清除的问题；只要同一请求仍待处理，就保留失败提示并允许在恢复权威连接后重试。请求解决或切换任务后清除。
- scoped Vitest 6 文件 78 项 PASS，Host focused race tests PASS，Desktop/Host lint PASS，Contracts 3 项 PASS，生成消费同步与旧 FEAT-137 退役检查 PASS。
- 首次构建发现新代码的 TypeScript 空值收窄错误；通过稳定局部引用修复，失败日志与最终成功 canonical 构建日志分别保留。没有屏蔽类型检查。
- 真实菜单 AX 已确认三项标题、描述、选中状态和键盘操作。工具在菜单弹出时只暴露原生菜单树，无法取得弹出菜单截图；随后通过直接渲染生产组件补齐了亮暗菜单/确认视觉矩阵；这不是全应用弹出菜单截图。`dark-menu-closing.jpg` 是菜单已关闭后的画面，不能作为打开菜单的视觉证据。
- 真实主窗口分别在浅色、深色及最小 1180×760 检查：输入框和权限入口未截断；完全访问警示文字改用设计系统现有 `--yj-color-semantic-warning-ink`，未修改全局主题。静态颜色计算：浅色原警示色/白底 3.19、现有警示文字色/白底 7.09；深色原警示色/#2e3237 为 4.05、现有警示文字色为 8.95。后续生产组件菜单截图独立完成视觉检查，此计算仅作补充。
- 系统原设置为浅色，深色检查后已恢复浅色。首次完全访问的真实取消/确认沿用 S3；S4 确认交互单元测试及生产组件的取消/确认视觉检查通过，未重置真实数据库标记来伪造首次用户。正常重启后选择 full 没有重复首次弹窗，随后切回 ask。

## 真实自动审核

Desktop 任务 `01a07a39-100b-78d3-8a70-6278d3153173`，Runtime 父线程 `01a07a39-1043-73b2-8596-dc97aa705528`，guardian 子会话 `01a07a39-3b2f-7022-80dc-6836713ee0a2`。

请求 14 是父任务，15/16 是 guardian 的两个结构化请求（原生审核中有一次 exec_command 工具调用），17 是父任务后续回复。实际 guardian 为 MiniMax-M3/minimax、read-only/never，结果 `allow`。普通项目外文件 `auto.txt` 内容为 `S4-auto`，退出码 0，无人工批准。

**自然自动拒绝 → 真实人工接管 NOT RUN**：本次安全场景仍自然允许；没有伪造回调、制造危险操作或改写原生审核结果。AC-003 全分支不能通过。

## 正常重启及实际回归结果

应用通过 Cmd-Q 正常退出，canonical `pnpm tauri:demo-fast:stable` 重新构建并启动。S4 任务保存的 auto、S3 任务保存的 ask 互不覆盖；重启后新任务默认为 ask，S4 历史和 auto 设置恢复。

同一 S4 任务切到 full 后再切回 ask，发起第二轮；请求 18 一次产生三项独立原生工具请求：项目内默认权限写入、公开网页 HEAD 联网审批、项目外写入审批。项目内 `s4-inside.txt` 已成功写入 `S4-inside`。项目外 `rejected.txt` 尚不存在。

继续读取真实审批 UI 时曾因 Mac 锁定暂停；用户解锁后在原回合通过 UI 拒绝外部写入、批准联网请求。Runtime 分别返回 `command_declined` 与 `HTTP/2 200`，联网命令退出码 0，外部 `rejected.txt` 未生成。第 19 次为后续模型回复，回合正常完成。没有重新创建任务、重发操作或抹去暂停事实。

用户再次明确追加 5 次（2026-09-07T05:33:10.840Z），累计上限增为 25。计数器空闲时通过正常 Ctrl-C 结束，原账本保留 19 条请求后调整上限并重新启动。

第三轮 full 实际执行使用 `danger-full-access / never / user`，项目外 `full.txt` 为 `S4-full`，退出码 0，无新增审批；请求 20/21。第四轮切回 ask 后恢复 `workspace-write / on-request / user / network_access=false`，项目外写入重新显示人工审批，经 UI 拒绝后 `after-full.txt` 不存在，Runtime `command_declined`；请求 22/23。

S4 总共使用 10 次（14–23），累计 **23/25，剩余 2**。最后任务保持 ask，应用 Cmd-Q 正常退出（launcher exit 0），计数器正常 Ctrl-C 退出（exit 0）。未为消耗剩余额度反复尝试自然拒绝。

## 补充生产组件视觉检查

原生应用菜单截图限制通过分层证据处理：真实应用证明入口位置、Native 主窗口亮暗/最小尺寸和实际菜单 AX/键盘；临时 Vite 页直接导入原 `ChatPermissionControl.vue`、`YjIcon.vue` 与正式主题/CSS，检查弹出菜单和确认弹窗。页面明确标注“仅组件状态，不连接 Native、Host 或 Runtime”。组件属性只在本页保存，没有后端请求或原生审批回调，不作为真实 Runtime E2E。

在实际设置的 1180×760 浏览器视口，浅/深色菜单和确认弹窗均完整可见；检查了 ask/auto/full 的独立选中勾、浅色取消保留 ask、深色确认后 full。菜单宽 520、高约 223.2，完整位于视口内，三项 clientWidth/scrollWidth 均为 502，无横向溢出。共 6 张 `component-*.png` 图片、DOM 几何和生产源 SHA-256 保留；可复现入口见 `component-visual-source/README.md`。

AC-001 的组件测试/视觉与真实入口分层检查通过。浏览器视口已 reset，临时 tab 关闭，Vite 通过 Ctrl-C 正常关闭（exit 130）；未改变生产组件逻辑或系统外观。原生弹出菜单没有被截图的事实保留。

## 本轮交付结论

AC-001/002/004/005/006/007/008 已有对应阶段/本轮证据；AC-003 的自然自动拒绝后真实人工接管仍 **pending / NOT RUN**。这一轮曾保留严格 Native Clippy 失败；后续用户授权修复后最新检查已 PASS（见 closeout）。原失败日志保留为历史。

**S4 本轮验收记录已完成，但 S4 和完整需求尚未通过；D4 FAIL。** 功能默认关闭，feature 与 S4 仍 active，不把单元测试、组件截图或模型口头报告当作缺失的真实接管验证。未执行的攻击/故障注入场景因用户禁止而跳过，不伪造通过。

## 安全与边界

Codex 核心仓仍干净，retained Runtime / manifest SHA-256 与 S1–S3 相同。没有强杀、攻击注入、权限破坏或运行时替换；没有 commit、push 或发布。其它任务的设计文档、图标和构建脚本改动保留。


## 后续授权收尾更新

Clippy、fmt 与 Native 3 项相关检查均已通过；当前不再有 Clippy 门禁阻断。真实接管仍 NOT RUN，后续原生临时文档复核规则场景已准备并通过零付费配置联调，尚待用户确认配置验收范围与新增调用。详见 closeout/manual-takeover-plan.md。付费账本仍 23/25，本次追加请求未获批前不执行。
