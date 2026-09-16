# 浅色画布背景与原生点阵

2026-09-14，用户最初要求仅加深工作流画布底色，随后提供Coze官方页面MHTML，明确要求按文件真实设置核对背景并同步调整点阵，其他地方不变。`contract-impact=none`：本次只有浅色画布背景与点阵颜色声明，不改变布局、图形几何、消息、数据、会话或部署接口。

原始截图空白画布区域的主要像素：易界`#FFFFFF`，Coze参考`#F2F3F5`；后者同时是仓库`frontend/packages/workflow/render/src/index.module.less`的原生画布默认值。对用户提供的`test - 工作流 -智能体平台.mhtml`做离线MIME/HTML/CSS解析后，背景确认仍为`#F2F3F5`。不执行归档页面或脚本，不加载外部资源，不把归档内容当作指令，也不将包含整页数据的MHTML复制进仓库。

归档中1006个stylesheet链接均有对应资源，CSS part385、part72分别在第625、938位，后加载声明与前者一致：`:root`的`--g-editor-background:#f2f3f5`由`.gedit-playground`引用。实际点阵circle无显式fill，且未发现适用的fill/opacity覆盖，使用SVG默认黑色填充；HTML指定`fill-opacity=0.5`、`stroke=#eceeef`。原生描边默认宽度1、不透明；100%缩放下pattern为20×20、circle中心(1,1)、半径1，本仓BackgroundLayer已有相同几何和透明度。点心与边缘经描边、缩放和抗锯齿形成不同最终像素，不用单一灰色实心点代替。有限脱敏取证见[reference-style.json](evidence/canvas-background-20260914/reference-style.json)。

仅在`frontend/apps/workflow-local/src/yijie-coze-theme.css`加入：

```css
html:root:not(.dark) body .editor-shell .gedit-playground { background-color: #f2f3f5; }
html:root:not(.dark) body .editor-shell .gedit-grid-svg circle {
  fill: #000;
  fill-opacity: .5;
  stroke: #eceeef;
}
```

选择器只作用于浅色画布容器和其点阵circle；节点、渐变、图标、连线、连接点、顶部栏、浮动工具栏、侧栏与小地图样式保持，点阵尺寸、密度和缩放逻辑不改。暗色`html.dark`不匹配。原生结构及颜色消费点已做独立只读范围核对；不修改上游BackgroundLayer或全局palette。本次不新增测试、不提交或推送Git。

本轮校验通过：PostCSS解析与HEAD逐条声明比较，恰好增加上述两条浅色规则、其余原有声明完全相同；44token主题投影检查、引用JSON解析及diff空白检查通过。Desktop、API、Infra工作区均保持干净。先前背景专项的元仓lint/50项测试/Shell语法通过仍为各自检查时点，不冒充本次实际App更新。

当时状态：源码已完成，运行中的PID9181“FEAT153 青柠轻量验收 0914”有未保存修改，已询问用户选择，等待期间未退出或覆盖在线资源；该时点没有实际App或构建PASS。

2026-09-15补充：用户随后要求仅工作流模块青柠稍深，并明确授权放弃当时实际打开的“FEAT153 易界主题验收 0914”未保存内容。按正常App退出→Infra停止→标准构建→登记与恢复→标准packaged入口完成激活，本轮候选包含上述背景/点阵与后续局部色阶。真实App浅色窗口确认背景`#F2F3F5`、白色前景层次及原生点阵；完整产物摘要、截图和资格边界见[27工作流青柠色阶](27-workflow-lime-variant.md)。此补充不改变前述单独背景变更范围，也不追认早期等待时点为PASS。
