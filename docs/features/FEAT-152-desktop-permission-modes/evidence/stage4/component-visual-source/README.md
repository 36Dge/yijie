# 生产权限组件视觉检查的复现

这四个文件原位于 `yijie-desktop/.local/feat152-s4/visual/`。本目录保留其原文；复现时将它们放回该位置，在 yijie-desktop 根执行：

```sh
pnpm exec vite --config .local/feat152-s4/visual/vite.config.mjs
```

浏览器访问 `http://127.0.0.1:5177/`，将视口设置为 1180×760。依次检查浅色菜单与首次确认取消，切换页面上的“深色”，检查菜单、首次确认和三档选择。完成后复原浏览器视口，正常 Ctrl-C 停止 Vite。

Preview.vue 直接导入生产 ChatPermissionControl 和正式主题，无复制的权限菜单实现，无 Native/Host/Runtime 连接，无真实审批回调，也没有付费请求。页面本地属性仅服务于组件交互/视觉检查，不作为真实审批 E2E。源 SHA-256 见相邻 `component-visual-provenance.json`，最终截图和几何见相邻 `component-*.png` 与 `component-visual-metrics.json`。
