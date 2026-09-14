# Canonical12 实际 App DI 缺口定位与最小修复

状态：实际 App 首次启动失败已定位；仅源码修复与有限静态检查完成，修复后构建和真实 App 重验尚未执行。本文件不代表原生页资格通过。

整体 FEAT-153 本次追加仍采用 `contract-impact=semantic` 最高风险。此单项修复为进程内原生服务依赖补全；无 wire DTO、跨仓/跨进程协议、持久化/重放或部署语义变化。

## 真实观察来源

父代理在正常启动的 canonical12 Desktop、已有合成草稿内，通过实际 WebInspector 展开错误后传回以下栈摘要。此子代理未操作浏览器或注入页面脚本，未重新触发故障；只读取当时冻结的真实 dist 和对应源码。

- `Error: No matching bindings found for serviceIdentifier: g`
- `6245.7dc08b2e.js:323:635264`（Inversify 无 binding 抛错处）
- 同文件 `:323:628180` → `:29:14067 ne`（child container `get(layerClass)`）
- `registerLayer :29:5843` → `registerLayers :288:93973`
- `index.862a78e9.js:71:9519 registerRenderer`
- `6245.7dc08b2e.js:288:93459 init`
- `index.862a78e9.js:71:8796`（React `useMemo` 初始化）

同时观察到 addLine/addNode operation meta already registered 警告。没有证据把它们认定为本次缺失 binding 的原因；本修复未更改历史注册。独立 WASM 启动问题由构建代理处理。

## bundle → source 确切映射

1. index 模块 `87998` 的 `WorkflowRenderContribution.registerRenderer` 调用 `e.registerLayers(l.Em,l.lV,s.h,c.N)`，对应原 `frontend/packages/workflow/render/src/workflow-render-contribution.ts` 的 FlowNodesContentLayer、FlowScrollBarLayer、HoverLayer、ShortcutsLayer。
2. `c.N` 来自 index 模块 `979773` 的原 `ShortcutsLayer`，它 `@inject(l.k)` 依赖 `WorkflowShortcutsRegistry`。源码为 `frontend/packages/workflow/render/src/layer/shortcuts-layer.tsx`。
3. index 模块 `635781` 导出 `k` 的原 `WorkflowShortcutsRegistry`（class d）通过 multiInject `WorkflowShortcutsContribution` 解析快捷键贡献。真实 render container 模块 `908497` 已绑定该 registry，不是 registry 自身丢失。
4. index 模块 `381382` 导出 `f` 的 `WorkflowExportShortcutsContribution`（class d）通过 `@inject(c.b)` 依赖原 Copy；`c=o(734487)`。
5. index 模块 **`734487` 导出 `b` 的 class g** 即 `WorkflowCopyShortcutsContribution`，源码为 `frontend/packages/workflow/playground/src/shortcuts/contributions/copy/index.ts`。因此错误中的 g 已精确还原，而非凭压缩变量名猜测。
6. local `createWorkflowPageContainerModule()` 未向 `bindShortcuts()` 传 Copy/Paste，却仍传 Export。原 `shortcuts/utils/register.ts` 仅绑定传入贡献，造成 Export → Copy 的真实依赖断开。

## 修复

在 local 分支补 `bind(WorkflowCopyShortcutsContribution).toSelf().inSingletonScope()`，用于原 Export 序列化依赖。仍不把 Copy/Paste/Load 放入本地 WorkflowShortcutsContribution 贡献列表；没有开启复制/粘贴/导入快捷键，也未替换服务、增加 dummy binding 或引入平台请求。

只读依赖核对：原 Copy 只有 WorkflowDocument、WorkflowSelectService、WorkflowGlobalStateEntity 三个字段注入；没有 constructor/postConstruct 网络动作。原 Export 的 toJSON 调用 Copy.toSource/toJSON，保持原有导出行为；原 Copy 的 clipboard.write 只在其 handle 执行时发生，本地没有注册该快捷键。local 节点 meta 的 copyDisable 保持生效，原复制菜单不展示。

父代理已在源修改前确认 App 与 local 栈均通过正常入口停止，没有覆盖在线构建。

## 有限验证

- TypeScript 5.8.2 `transpileModule` 对此次唯一变更 TS 文件检查：0 errors。真实 tool result `247dd0`，命令退出 0。
- `git diff --check -- frontend/packages/workflow/playground/src/container/workflow-page-container-module.ts yijie-upstream.lock.json`：退出 0。
- 该源路径原已登记在 upstream lock；仅补充 `integration_overlay_notes` 的修复原因。
- 未额外扩展测试；未执行修复后构建、完整类型检查、实际 DI 实例化或 App 重验，均由后续 canonical 候选和真实 UI 负责。

## 诊断资产与修改源摘要

- `bin/workflow-editor/dist/assets/js/index.862a78e9.js`: `0f54c212aa523e51dadc3e44511adac5265afec0696a665bf4bfaf4422256b11`
- `bin/workflow-editor/dist/assets/js/6245.7dc08b2e.js`: `64e5a5ec324a0fc3245ce1c85198c8d2aa9860b3ef0c93182d5de4678a130256`
- `frontend/packages/workflow/playground/src/container/workflow-page-container-module.ts`: `59c744709238c11505feefb0cb92a5eb7bf8034caf27cbb81b8370e9499375bb`
