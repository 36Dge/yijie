# FEAT-157 卸载恢复界面复核

日期：2026-10-07，Asia/Shanghai。执行者：desktop_audit 子代理。

## 范围

使用真实 `ConnectorMarketView`、`ConnectorDetailsDialog` 和现有易界 theme/tokens，入口为 Desktop `.local/feat157-visual/uninstall.html`。顶部明确标注“卸载组件检查 · 合成数据 · 非 D4”；状态和查询/取消计数只存在组件预览内存。未启动 Native、Broker、Runtime、真实模型、OAuth 或外部 MCP，未访问用户持久数据库。本记录不是产品端到端验收，也不表示任何供应商已接通。

## 浏览器观察

通过 CUA Chrome 检查 1180×760 viewport，分别覆盖亮色/暗色、100%/200%。200% 使用项目 `ui-zoom` 的 root zoom 与 viewport/minimum CSS 变量。

- 四种主题/缩放组合均能完整阅读 pending 卸载说明，“关闭窗口”“重新确认状态”“取消操作”互不重叠，均位于窗口内。
- 100% 卸载弹窗：left=350、right=830、top=223.60、bottom=536.39；操作按钮 bottom=516.39。
- 200% 卸载弹窗：left=110、right=1070、top=67.21、bottom=692.79；操作按钮 top=580.79、bottom=652.79。
- 点击关闭窗口后 pending 状态保持，查询/取消计数未变化；Esc 也能正常退出 pending 窗口。
- 重新从已安装行打开详情，查询和取消入口均可见。点击查询只增加查询计数；明确点击取消后回到未启用状态。
- 暗色 200% 重开详情：left=110、right=1070、top=32、bottom=728；正文 clientHeight=292、scrollHeight=518，可滚动；固定操作页脚 top=616、bottom=728，操作保持可见。
- 只读合成状态仅保留“重新确认状态”，不显示取消或卸载操作。
- 最后关闭详情时焦点返回原已安装行按钮。

## 发现与修正

复核发现详情对所有 cancellable 动作使用“取消连接”，导致未完成的卸载操作也显示该标签。将 `ConnectorDetailsDialog.vue` 的通用标签改为“取消操作”，未改变取消事件或权限语义；HMR 后再次完成暗色 200% 查询/取消检查。

新增组件集成回归：pending 卸载关闭后重新打开详情，仍查询原 operationId；取消传递同一个 operationId/revision，未重复提交卸载。

`pnpm exec vitest run src/components/connectors/ConnectorMarketView.test.ts --maxWorkers=2`：5 PASS。

定向 ESLint（MarketView、DetailsDialog、MarketView test）：PASS。最终全项目 lint/build 由 root 汇总。

## 证据与清理

亮暗 100%/200% 截图，以及修改后的暗色 200% 详情截图，已通过 CUA screenshot 查看并展示于本次工具 trace；截图接口未返回独立保存文件，因此没有提供虚构截图路径或生成替代图片。

浏览器 viewport override 已 reset，本次测试 tab 已关闭。Vite 使用本地 `server.mjs`，Ctrl-C 触发注册的 SIGINT handler，执行 `await server.close()`，session 36813 返回 exit_code=0。未强杀进程。
