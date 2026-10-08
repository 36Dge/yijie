# FEAT-157 Desktop 组件视觉与专项检查记录

> 归档说明：本报告复制自 `yijie-desktop/.local/feat157-visual/README.md`。下文“本目录”指该临时组件目录；专项日志另归档为本证据目录的 `ui-specialized-tests.log`，原 HEAD 对照日志为 `chatpage-baseline-tests.log`。无独立截图文件。

日期：2026-10-07（Asia/Shanghai）。执行者：ui_audit 子代理。

## 范围与限制

本目录是临时组件预览，使用真实 ConnectorMarketView、详情、ChatComposer、ChatConnectorControl 和易界 tokens。顶部明确标注“组件视觉检查 · 合成状态 · 非真实接入验收”。目录为本地 51 服务公开目录副本；7 条 installed/ready 状态以及长名称均为普通合成数据。页面按钮只产生组件事件，不调 Native、Broker、模型或外部 MCP。不代表 D4/51 服务真实接通或应用端到端验收。

标准 Vite createServer 开于 127.0.0.1:1437；SIGINT/SIGTERM handler 调用 await server.close() 再 process.exit(0)。各次重启均通过 PTY Ctrl-C，最终 session 15748 正常关闭并返回 exit_code=0；未使用强杀、破坏权限或攻击 fixture。

浏览器为 CUA Chrome，viewport 设置 1180×760，结束已 reset 并关闭本次检查 tab。模拟 sidebar 仅用于预留真实工作区宽度，不是完整应用 shell。200% 使用 src/domain/ui-zoom 的方法，将 CSS zoom 及 viewport/minimum variables 写入 documentElement，与应用缩放入口相同。

## 实际观察

- 亮色 100% 市场：六类、51 项的组件数据呈现；三列布局、局部纵向滚动、长名称截断；DOM scrollWidth=clientWidth=1180，无水平溢出。
- 暗色 100% 市场/已安装列表：行 switch/状态清晰，provider 原 logo 保持，透明黑字图标通过专门的白色 artwork token 可读。
- 安装详情：返回真实 connector.description 与接入未配置说明，启用不被静态伪造。Esc 关闭后 activeElement 返回原目录卡片。
- Composer：关联店铺右侧连接器入口；所选长名 chip 截断，移除按钮独立；全局 switch 与单次选择为两个独立控件。
- 键盘：ArrowDown 从触发器打开后聚焦搜索；Tab 到首项；ArrowDown 到下一项；End 到最后一项并滚动到可见位置（实测 listScroll=166.5，最后按钮 top=332.47/bottom=402.06）；Esc 聚焦回连接器触发器。
- 暗色真实 root zoom 200%：修正后菜单 physical rect left=348/right=1148/top=25.625/bottom=721.625，完全位于 1180×760 内，正文列表可滚动，管理页脚保留。
- 暗色真实 root zoom 200% 详情：修正后 modal rect left=110/right=1070/top=32/bottom=728；内容 clientHeight=292、scrollHeight=552、overflow=auto；页脚 top=616/bottom=728 完整可见。

## 由视觉检查发现并修复

1. YjSection 默认 aria 标签写“Skill”，增加可选 countLabel，连接器分类输出“n 个连接器”。
2. NSwitch 禁用状态只反映 CSS，连接器组件显式设置 aria-disabled。
3. 暗色下透明黑字品牌图标难以辨识，ConnectorIcon 使用新增 neutral artwork token 托底。
4. 200% popover 起点保持 trigger 左边时右侧超出 viewport，加入缩放感知的横向偏移。
5. Naive 当前正文 class 是 n-card-content，详情原 selector 不匹配，导致内容顶出固定页脚；更正 selector 并固定 footer flex。
6. 详情/卸载 NModal 的空 default slot warning，条件改到 NModal 根。
7. 键盘 Home/End/上下键选择后滚动当前行到可见位置。

## 截图证据

实际截图已由 CUA screenshot 捕获并在工具 trace 中展示：亮色市场、暗色市场/已安装列表、暗色详情、亮/暗 Composer 菜单、200% 溢出前后及 200% 详情修复前后、亮色 End 键焦点状态。CUA 的截图接口只返回 JPEG bytes/内联图像，无独立保存路径。临时页面的正常下载尝试未生成可确认文件，因此本目录不声称存在截图文件；证据为工具 trace，未重绘或生成替代截图。

## 专项结果

命令及摘要见 ui-final-tests.txt；9 文件 84/84 通过：

- src/stores/market-connectors.store.test.ts
- src/stores/chat-composer-drafts.store.test.ts
- src/domain/market-connectors-ui.test.ts
- src/components/chat/ChatConnectorControl.test.ts
- src/components/chat/ChatComposer.test.ts
- src/composables/useChatModels.test.ts
- src/navigation/app-nav.test.ts
- src/authorization/app-permission-policy.test.ts
- src/router/index.test.ts

覆盖含安装真实回执、unknown 原 operation 查询/同参数显式重放、pending 精确取消、context 续期保留原意图并丢弃旧响应、tenant/revoke 清除、降到 readonly 可读回执但不可重发 mutation、unknown install 详情重试入口、全局启停与单轮选择分离、普通草稿向计划只复制文字和跨页面草稿保留。类型/lint/build 由 root 汇总。

ChatPage 原有 5 个 legacy 失败已用 HEAD 源的临时基线复现实证，未纳入本次 84 PASS，也未为本需求扩修；基线日志 /tmp/feat157-baseline-chat.txt。

## 未执行

未启动 Native 产品/本机持久数据库，未启动 Broker/runtime/模型或任何第三方服务，未授权供应商账号，未进行 D4 逐服务真实验收。完整产品集成与供应商验收仍需要后续阶段。
