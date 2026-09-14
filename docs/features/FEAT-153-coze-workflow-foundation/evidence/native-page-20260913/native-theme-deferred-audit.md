# 原生 Coze 页面主题审计：延期

状态：**DEFERRED，未通过主题验收**。用户明确要求当前暂停主题验收，后续统一将 Coze 蓝色调整为易界主题。此次未发布主题修复，未构建 canonical21/22。

## 已观察事实

canonical20 实际 App 在系统暗色下，iframe html 为 `dark`、body 为 `theme-mode=dark`，说明原生 ThemeProvider 已生效。实际截图为同目录 `app20-dark-1346x849.png` 与 `app20-dark-1180x760-sidebar.png`。节点标题白色渐变、亮色网格、文本编辑框浅底白字，以及紧凑节点标签过暗均可见；不能将当前暗色显示标记为通过。

只读来源定位（以下均为 yijie-coze 仓路径）：

- `frontend/packages/workflow/playground/src/form-extensions/components/node-header/index.tsx:306` 使用 `getBgColor(mainColor, 0.08)` 作为渐变起点。其 `utils/get-bg-color.ts` 的 `rgbaToHexWithBackground` 默认将颜色混到白色 RGB 255；终点 `--coz-bg-plus` 已随主题变暗，形成明显白顶渐变。
- `frontend/packages/workflow/render/src/layer/background-layer.tsx` 在原生 SVG circle 写死 `stroke="#eceeef"`，`DOT_SIZE=1`、`RENDER_SIZE=20` 仍按原生缩放计算。暗色亮点并不是第二套网格或旧自绘布局。
- `frontend/packages/workflow/playground/src/nodes-v2/components/expression-editor/container/index.module.less` 的背景使用 `--semi-color-white`，文本使用 `--semi-color-text-0`。实际已构建主题中暗色 `--semi-color-white` 仍为 `#e4e7f5`，文本已按暗色变亮，产生浅底白字。
- `frontend/packages/workflow/playground/src/components/node-render/node-render-new/fields/field.module.less` 的 12px 标签使用 `--coz-fg-dim`。实际暗色 token 为白色、alpha `.22`，在 `--coz-bg-plus`（RGB 28,32,48）上难以辨认；这不是缺失主题类。

以上是已观察的限定页面与源码证据，不代表全主题、全尺寸或 WCAG 检查完成。未继续扩大颜色/布局调整。

## 未保留的短暂主题增量

App 与工作流栈正常停止后，曾在上述 NodeHeader、Field 样式、ExpressionEditor 样式，以及 `frontend/apps/workflow-local/src/style.css` 加入仅 `.dark .editor-shell` 启用的颜色变量与原生 SVG circle 颜色覆盖，并在 source lock 登记两份新增 LESS overlay。尚未检查、构建或重新启动时收到用户暂停指令。

随后仅用该轮 patch 的精确反向操作撤销这 4 个源文件的主题增量，并移除 source lock 的两项新增 overlay 与本轮说明；保留全部此前适配、首存比较修复和既有 `.dark .editor-shell` 画布背景设置，没有执行整体 checkout/reset。

首次撤销后的 manifest check 发现源摘要差异。对照 canonical20 prepared source 确认唯一残差是 ExpressionEditor LESS 原有的末尾一个空白行被 patch 工具移除；仅补回该换行并断言逐字节一致后，标准入口检查通过。

最终验证命令：`node scripts/yijie/workflow-editor.mjs check`，真实 tool result `4881cb`，退出 0，输出 `VERIFIED: bounded local editor manifest, asset hashes, source and Contracts lock; static CSP aids passed, browser qualification remains separate`。

当前保留 canonical20 源摘要：`feaa8e90180db13d2b479c0cd36bd24c624df20dc176e144837c5e950ab4d95c`。主题实现与主题验收待后续易界品牌主题统一需求推进，不能继承本轮主链路通过结论。
