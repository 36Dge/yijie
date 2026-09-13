# 第5步编辑器构建与状态模型核对

日期：2026-09-12；这是构建/源码证据，不能替代真实 App 资格。

- 复用上游 `@coze-workflow/render` 的 Provider、Playground renderer 与端口，固定 Flowgram 0.1.28；源码副本仅在 ignored 的 canonical build-workspace，未改上游 Rush manifest 或 lock。
- 首轮状态测试发现新增 `newTextNode` 字面对象缺少闭合括号；修正后 5/5 正常状态测试通过。覆盖不透明字符串 revision、保存期间后续编辑、同版本重连保留草稿、异版本冲突、未确认保存不能仅凭内容相同认定提交，以及多语言字面前缀。没有真实会话到期或攻击 fixture。
- 修正 `DraftModel` 原来错误的数字 revision 递增假设；现在保存响应采用服务端不透明 revision，未确认保存需按原 operation ID 查询 completed receipt 与精确 revision，再读取草稿核对。
- bridge 在模块入口监听，避免父 iframe load 早于 React effect 的连接丢失；同 iframe 重连保留模型和原始 base revision。父页面 pendingWrites 门保护在途回执。
- Flowgram 源码审查发现 `fromJSON` 不清除既有节点/线；干净草稿替换先 clear 再加载，finally 恢复 muted。`canAddLine` 第三参数实际为 manager，改为限定两条合法路径，底层原生去重；拖动位置经 TransformData 和原生 content change 保存。
- canonical prepare/install 正常完成一次新的 frozen install receipt（pnpm 8.15.8，ignored scripts），随后首轮 tsc 阻止构建：上游将 render 的 React/ReactDOM 与类型放在 devDependencies；isolated 投影剥离后无法解析。另发现 adapter 不导出 OptionsDefault，现配置本地所需 from/to/cursors；补入原生 CSS 入口。未绕过 tsc，也未把该轮记为 build PASS。
- 专用 app 的 TypeScript 采用上游 render 的 DI 初始化与 implicit-any 设置；保留 strictNullChecks 等类型检查。CSS adapter 映射 Desktop 已有语义配色，嵌入页面的 light/dark 行为尚需 WK 实测。
- 构建脚本审查收紧自有源码副本清理、精确 workspace 集、成功安装 receipt、完整 manifest 和实际写出字节预算；静态 CSP 扫描只是辅助，不是完整 JS 安全证明。

后续构建、manifest 登记、真实 App 及最终结果另记实际证据。
