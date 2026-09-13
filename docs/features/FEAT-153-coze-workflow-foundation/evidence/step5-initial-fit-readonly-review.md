# 第 5 步首次画布适配：独立只读复核

2026-09-12。`contract-impact=none`：本轮只读核对并新增该证据，不改业务、契约、生成物、构建或部署。已读取 Coze AGENTS；未执行 UI、构建、栈、数据库、HTTP 或测试。Mac 锁定期间不能提供真实 WebKit 视觉 PASS。

结论：在本次锁定的本地 Flowgram 0.1.28 实现及最小三节点图范围内，没有发现“首次测量必然触发 runtime.emit，导致自动适配被提前取消”的 P1/P2 问题。加载、图层完成、尺寸测量存在可实际连通的触发链；尺寸与 zoom 的比较单位一致。此结论不证明真实 App 首屏已适配成功。

本次读取的源码 SHA-256：

- `yijie-coze/frontend/apps/workflow-local/src/native-canvas.tsx`：`2a1f2053b05b23a4a863e0fe559c24d15c939c8c92a0b12c1f390a1a13798170`
- `yijie-coze/frontend/apps/workflow-local/src/initial-canvas-fit.ts`：`1dc2bdafff1f476868dc7b0fb68b6f1bc8510d85fa03d11423b30fd3848c2e97`

## 本地依赖证据路径

以下路径相对 CrossBSD 根；别名仅用于本证据中简写行号，不是第二源码。

| 别名 | 已安装的锁定依赖文件 |
| --- | --- |
| CORE | `yijie-coze/bin/workflow-editor/build-workspace/node_modules/.pnpm/@flowgram.ai+core@0.1.28_react-dom@18.2.0_react@18.2.0/node_modules/@flowgram.ai/core/dist/index.js` |
| DOC | `yijie-coze/bin/workflow-editor/build-workspace/node_modules/.pnpm/@flowgram.ai+document@0.1.28_react-dom@18.2.0_react@18.2.0/node_modules/@flowgram.ai/document/dist/index.js` |
| FREE | `yijie-coze/bin/workflow-editor/build-workspace/node_modules/.pnpm/@flowgram.ai+free-layout-core@0.1.28_react-dom@18.2.0_react@18.2.0/node_modules/@flowgram.ai/free-layout-core/dist/index.js` |
| RENDER | `yijie-coze/bin/workflow-editor/build-workspace/node_modules/.pnpm/@flowgram.ai+renderer@0.1.28_react-dom@18.2.0_react@18.2.0/node_modules/@flowgram.ai/renderer/dist/index.js` |
| STACK | `yijie-coze/bin/workflow-editor/build-workspace/node_modules/.pnpm/@flowgram.ai+free-stack-plugin@0.1.28_react-dom@18.2.0_react@18.2.0_styled-components@6.1.19/node_modules/@flowgram.ai/free-stack-plugin/dist/index.js` |

依赖版本声明在 `yijie-coze/frontend/packages/common/flowgram-adapter/free-layout-editor/package.json:40`；当前最小 app 仍使用 Coze `WorkflowRenderProvider`，未绕过其 Loader 和图层贡献。

## 首次测量不会直接变成内容编辑

- `native-canvas.tsx:121` 将 document.onContentChange 接至 runtime.emit；`:22` 确实会取消初始 fit，因此必须区分测量与内容事件。
- RENDER:698 的真实 ResizeObserver 先 requestAnimationFrame，确认节点挂在 DOM 且可测量，再把 contentRect 四舍五入至 0.1 CSS px 写入 FlowNodeTransformData.size。
- DOC:504 只更新尺寸并 fireChange；FREE:1839 的订阅进入 FreeLayout.syncTransform，FREE:1633 仅执行 TransformData.update({size})。CORE:1002 将 size 更新到 SizeData，没有更新 PositionData。
- FREE:1859 的 MOVE_NODE 内容事件只监听 PositionData；不会仅因 SizeData 变化触发。无表单的最小 LocalNode 也没有首次表单初始化产生异步 NODE_DATA_CHANGE 的路径。原生文本输入的显式 runtime.emit 是真实用户编辑。
- 初始 ADD_NODE 与 ADD_LINE 同步在 fromJSON/renderJSON 内产生，FREE:1801 的 changeEntityLocked 与 FREE:1779 的 _loading 均覆盖加载；FREE:2023 抑制这些内容事件。连线的 ADD_LINE 位于 FREE:1400 的 createLine，不是在后续端口测量完成时另行发出。正常测量因此保留 initialFit.pending。

## load、图层与测量的先后

- `yijie-coze/frontend/packages/workflow/render/src/workflow-loader.tsx:35` 的 layout effect 调 doc.load；FREE:1778 等待 DOC:1771 的所有 loadDocument，然后清 _loading 并 fire onLoaded。`native-canvas.tsx:114` 在自己的 loadDocument 返回之前已绑定 node transform 与 onLoaded 订阅。
- CORE:7063 的 React effect 将 playground 插入父 DOM、调用 ready；CORE:6638 注册/渲染图层后调用 contributions.onReady。CORE:6487 在实例构造时已绑定所有图层完成事件，因此不会因为应用 contribution.onReady 尚未调用而丢失该事件。
- CORE:4765 的事件表示 React 图层首次报告完成，不代表 ResizeObserver 已同步真实尺寸。`initial-canvas-fit.ts:44` 只设置 rendered 并排队；`:54` 还检查 document.loading、连接状态、非零 viewport 和每个节点的实际尺寸与 engine 尺寸。
- 图层先完成时，之后的 onLoaded/节点测量/viewport resize 会重新 request；文档先加载时，onAllLayersRendered 会 request。request 在同一帧合并，检查未通过不会自行无限轮询；真实测量事件会再次唤醒。
- FREE:1975 的 getAllNodes 排除虚拟 ROOT。DOC:2096 与 RENDER:1005 的节点渲染按 render tree/hidden 属性，当前普通三节点不依赖 viewport 相交后才挂载；未发现“必须先 fit 才能测量、必须先测量才能 fit”的此类循环。

## viewport、缩放和一次性行为

- `native-canvas.tsx:74` 读取 playground.node.getBoundingClientRect；CORE:6659 的内核 resize 同样读取该元素并将 width/height 写入 config，再发 onResize。viewport 两端都是未作画布缩放的同一 DOMRect 单位，不应额外乘 zoom。
- 节点读取的是实际 renderState.node 与 TransformData.bounds（`:79`），后者正是 FREE:132 的 fitView 使用的尺寸来源。Coze `workflow-render-contribution.ts:74` 将节点移到真正 STACK render-layer；STACK:272 对该层应用 scale(zoom)。所以节点 DOMRect 与 engine bounds × playground.config.zoom 的比较正确；CORE:5134 在禁用 zoom 时返回 1，也与渲染倍率语义相符。
- 当前节点外包 `.gedit-flow-activity-node` 只设 absolute（Coze render `index.module.less:184`），测量的 wrapper 没有额外 border/padding。`initial-canvas-fit.ts:23` 的 0.5 CSS px 容差覆盖此版本 0.1 px 尺寸舍入，不把节点默认尺寸视为已测量。
- `initial-canvas-fit.ts:59` 在 fit 之前 dispose，解绑尺寸/viewport/用户事件，再调用 fitView(false)；fit 改 zoom/scroll 或 forceUpdate lines 不会启动第二次自动 fit。FREE:132/CORE:5452 只改视口，不改持久化节点坐标。
- 用户 pointerdown/wheel/keydown、添加节点/编辑内容、手动 fit、replace/reconnect、卸载会永久取消当前实例的初始 fit（`native-canvas.tsx:22`、`:25`、`:42`、`:97`、`:103`）。这符合“不抢回用户视口/重连不重排”的意图；不能期待用户已开始操作后再次 resize 自动恢复首次 fit。

## 剩余验证边界

现有 `initial-canvas-fit.test.mjs` 是手动 scheduler/geometry 的正常单元夹具，未实例化真实 renderer；只能验证控制器状态，不能单凭这些用例证明首次 DOM 测量会到达。本文补充了实际调用链只读证据，但仍未覆盖真实 WebKit 的测量/字体/窗口变化。

解锁后建议普通 App 验证：分别打开初始两节点和已保存三节点两线，在任何鼠标/键盘操作前观察首屏是否完整入画；再正常改变窗口大小及主题，确认不会持续抢回用户视口；最后手动适应画布并核对节点持久位置未改变。若首屏尚未得到真实几何事件，控制器会保持等待且提供手动适配入口，不能将其记录为自动适配成功。全程不需要强杀、故障注入、权限破坏或攻击 fixture。
