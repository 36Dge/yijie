# FEAT-153 完整产品页面独立源码审查

审查时间：2026-09-12T12:05:46.102470+00:00。`contract-impact=none`：本子任务只读源码与源契约，并记录审查意见，未改变任何实现或跨仓可观察语义。

这是与本轮产品页实现分离的结构化源码审查；本审查者仅实现过独立首次适应画布，不在这里评价自己的 fit 实现。
初次独立审查没有修改被审文件，没有运行测试、构建、App、容器、数据库或网络，没有凭据读取、故障注入、攻击 fixture、进程终止或 Git 写操作。随后按主任务明确授权新增的独立组件测试另记于下方。
以下结论是可从当前代码追踪的行为与待修正项，**不构成 UI、主题/尺寸、无障碍或 D4 PASS**。

## 首轮 P1：无操作编号的不确定版本执行没有恢复或离开路径（源码修复已复核）

位置：`yijie-desktop/src/pages/workflows/use-workflow-runs.ts:77–79,83–85,101–105`；
`yijie-desktop/src/components/workflows/WorkflowRunPanel.vue:35–38`；
`yijie-desktop/src/components/workflows/WorkflowLocalWorkspace.vue:41–44`。

正常失败处理路径中，`workflow-native-client.ts:75–83` 把派发后的无类型 IPC 失败或无法校验的写响应保守解释为
`operation_unknown`，可能拿不到 operation ID。`start()` 仍保存 `pending`，这是正确的防重复方向；但
`reconcile()` 在编号缺失时直接返回，查询按钮也不显示。页面要求刷新历史核对，而 `refresh()`、`read()`、
`accept()` 都不能处理/解除这个 pending。与此同时，`askToClose()` 对任何 `uncertainRun` 无条件拒绝离开，
因此即使用户已经看到真实运行记录，也无法返回工作流或切换 Chat；只能退出 App。

该问题不要求制造故障验证：它来自实现明确覆盖的未知回执分支。不能为了移除阻塞直接清空 pending 或重新提交。
应补显式恢复/离开流程，例如展示已保存的工作流/版本/输入关联信息，允许用户核对真实历史后明确选择关联已观察运行，
或确认保留“执行结果未知”事实后离开。没有足够证据时不得把运行标记为成功；不会自动重复执行。
建议用正常合成异步单元案例验证：无编号 pending → 查看历史 → 明确选择恢复/离开；无需真实 IPC 故障注入。

## 首轮 P2：已有历史读取期间，新运行所需刷新会丢失（源码修复已复核）

位置：`yijie-desktop/src/pages/workflows/use-workflow-runs.ts:23–36,53–58`。

打开工作流会发起历史读取。若该读取尚未结束，新的试运行或版本执行已登记并返回，`accept()` 会调用 `refresh()`，
但 `loading` 为 true 时该调用直接返回。此前发出的历史请求随后可能返回不含新 run 的有效旧快照，替换列表。
最终运行结果面板已经显示新 run，而历史仍为空或缺少该 run，直到用户再手动刷新。

建议在 loading 期间记录一次重新读取需求并在当前请求结束后串行刷新，或把已确认的运行合入摘要后仍补一次读取。
应继续保留 workflow/epoch 校验、分页游标和去重；不能把延迟历史响应当作新运行未发生。
这个案例可用普通延迟 Promise 的历史快照顺序验证，不需要修改系统时间或注入运行时故障。

## 已核对的边界与非问题

- `useWorkflowRuns.current()` 使用 workflow ID、epoch 和 disposed；读取详情另有 `readTicket`，避免旧工作流/旧选项迟到覆盖。
  同一 workflow 重新连接 E 不重置版本执行状态，与版本执行由 native 独立授权、而不是使用 editor E 的实现一致。
- `main.tsx` 的 active ticket 同时绑定 generation、MessagePort binding 和读取时 revision；save/test/publish 顺序化，
  用户在等待结果时编辑的本地草稿不会因一次普通 `receive` 被无条件覆盖。
- `EditorRunModel.canPublish()` 要求同 workflow、同 revision、debug、terminal、succeeded 和无未保存修改/待确认试运行。
  已保存 revision 变化后旧成功试运行不再构成新 revision 的发布证明。服务端另有真实成功试运行核验。
- operation receipt 的 completed 被用于确认登记，再读取 run；并未直接等价为引擎执行成功。
  未知引擎 state 在父结果页按文字显示，terminal 标志另外展示。
- 发布后版本输入保留用户已选旧版本，而提示最新版本，是显式指定版本行为；不应未经判断把它改成自动切换。
- 父结果页使用文本插值，不向页面输出任意 provider 原始异常；浏览器桥仍以既有生成 validator、固定父 origin、MessagePort 与 generation 做校验。
- 父页面按 child pending writes 阻止关闭；child 的未确认写通过 dirty 提示离开确认。独立 release pending 的首轮不可离开问题及修正见 P1 和下方复核。

## 视觉与焦点待真实验证

从源码可见：新 runbar 支持换行，窄 iframe header/footer 支持换行，父运行面板有容器查询、最小宽度和长文本换行；
输入有 label，历史按钮有 aria-pressed，details/summary 保留原生键盘语义，主要状态使用 status/alert。
但这些只能说明存在相应声明，不能证明 1180×760 / 1440×900、明暗主题、Tab/Shift+Tab、滚动与焦点恢复已通过。
iframe 内 `prefers-color-scheme` 与父 CSS `color-scheme` 的实际 WK 行为必须由同一个真实 App 验证。
本次没有以 headless 模拟或代码声明代替这些资格。

## 修复后独立复核

复核时间：2026-09-12T12:07:51.267338+00:00。首轮行号保留用于说明发现时的流程；主任务在审查过程中完成修正，以下以新的源码时点为准。

- **P1 源码层关闭**：`WorkflowLocalWorkspace.vue:41–53` 不再对 uncertainRun 无条件拒绝。
  操作派发仍在进行时保持阻止离开；结果已经未知时转入现有确认框，取消会保留状态，明确确认后才关闭编辑器。
  `:152–157` 清楚提示查询入口将丢失、已提交操作不撤销、服务端历史保留；未自动重提或将 unknown 标记成功。
- **P2 源码层关闭**：`use-workflow-runs.ts:22,28,39–43` 在既有读取期间记录一次完整 refresh 需求，并在其结束后串行补读；
  `:122–124` 在 workflow/epoch 切换时清队列，迟到旧页面请求不会启动新页面的补读。
- **非终态保持**：`use-workflow-runs.ts:12,57,62–74` 独立保留 activeRun，在终态读回后才解除重复发起限制。
  `WorkflowRunPanel.vue:34–36` 有具体运行编号和显式核对入口。选择其他历史不等价于当前活动运行已结束。
  `main.tsx:217,274–275` 对 child 当前未终态试运行也阻止重新试运行并保留更新结果入口。
- 同 revision 的真实成功试运行证明、active operation ticket、selected read ticket、workflow epoch 和 typed receipt 关联保持。

本轮发现的两个问题均在源码复核中关闭，当前未发现额外实现阻断；这不等价于真实 UI / 全主题尺寸 / D4 通过。
本审查者没有重跑主任务报告的 21 项编辑器、24 项 Desktop 测试或 canonical unsigned 构建，其执行事实由主任务独立记录。
复核时已建议补充直接覆盖“加载中的历史补排刷新”和“无 ID unknown 经明确确认离开”的正常案例。主任务负责排队刷新测试；
本审查者随后获明确授权新增离开确认组件测试，见下。真实 App 验证仍需解锁后执行，不通过强杀、攻击或 IPC 故障注入制造场景。

## 后续授权的独立组件验证

时间：2026-09-12T12:11:08.091550+00:00。仅新增 `yijie-desktop/src/components/workflows/WorkflowLocalWorkspace.test.ts`，没有改产品实现。
`contract-impact=none`：测试不改变 Desktop/native/API 协议、本地持久状态或生产行为。

- 挂载真实 `WorkflowLocalWorkspace`、运行面板和两个真实 composable；客户端提供普通、源定义的 `operation_unknown` 无 ID 状态。
- 编辑器替身不创建 iframe；对话框替身只保留 show/slot 行为；路由 hook 捕获真实组件注册的 guard。
- 验证输入并发起一次版本执行后保留 unknown 状态；选择“继续编辑”时 guard 返回 false、页面和查询提示保留、native close 未调用。
- 再次离开，验证风险文案后明确点击“放弃本地内容并返回”，guard 返回 true，close 仅调用一次，编辑器移除并回到列表；原执行未重提。
- 所有真实 Tauri invoke 调用为零；没有网络、App、容器、数据库、系统时钟或权限改变。

命令 `pnpm exec vitest run src/components/workflows/WorkflowLocalWorkspace.test.ts --maxWorkers=1`：1 文件、1 案例通过。
针对该文件的 ESLint 及仓库 `git diff --check` 均 exit 0。首次测试因 Naive UI 组件实际名称为 Modal、测试替身未命中而找不到 wrapper 内 dialog；
仅补齐测试替身名称后复跑通过，产品实现未修改。测试不证明真实 Naive UI 焦点圈定、WK、真实路由跳转或视觉布局。

测试源码 SHA-256：`0b2bad68b36911ebc0e7867abb9b4320736c3fc8ee5705bc2e24dfded46ffdd6`。

## 修复后复核版本

下列摘要是结束时采样的当前修复版本，不冒充首轮缺陷版本的完整源快照。原始发现行号属于上面的首轮记录；
工作区仍可能被主任务继续修改，新改动需要重新判断相关结论。

| 文件 | SHA-256 |
|---|---|
| `yijie-desktop/src/pages/workflows/use-workflow-runs.ts` | `2bb96cbbe4d979c8c6ca80cef0eafe6ee33648a4eea7cc6d5d0595ab23632e93` |
| `yijie-desktop/src/components/workflows/WorkflowRunPanel.vue` | `ca4f2d870e27a85bf82e2a5d3e4675de49af6a843b98016617bce473de10283d` |
| `yijie-desktop/src/components/workflows/WorkflowLocalWorkspace.vue` | `2065b300f9dc6c1a3da0e8c7b551cdd27723fb68450614695598fab670c267fb` |
| `yijie-desktop/src/api/workflow-native-client.ts` | `43d33d99464f80565a43042d1827fb081ccae11021f9b5322b48c2267dfb0d7b` |
| `yijie-coze/frontend/apps/workflow-local/src/main.tsx` | `7707201a0d6d72a830b1de94d500d1ecc7592b937abb8534c036825b175ff9ca` |
| `yijie-coze/frontend/apps/workflow-local/src/run-model.ts` | `404f1886599bc63879ab75a37968e24c41bc605f7f7e79acfc789738b224ad9c` |
| `yijie-coze/frontend/apps/workflow-local/src/bridge.ts` | `8964f4e0df4b397c2f65f139c7d6ec77b0aee9222e9d744a5ebee81d45a2d8c1` |
| `yijie-coze/frontend/apps/workflow-local/src/style.css` | `5444b68e7899abf237077f466162bce0abccbafcfd3187307f2c2a71ef84018e` |
