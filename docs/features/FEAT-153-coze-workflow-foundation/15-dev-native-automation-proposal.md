# dev A 原生界面自动化接替方案

2026-09-13 11:03，用户询问是否可由Codex代为完成dev人工操作A。本页为具体操作范围与工具限制记录；替代技术尚未执行，不代表A或D4通过。

## 已确认事实

- 标准dev的实际App PID4642、CLI PID4608、launcher PID2760仍运行，launcher记录cli_running、http://localhost:1420。
- lsof确认App实际可执行文件为 `yijie-desktop/src-tauri/target/debug/yijie-desktop`；不是packaged bundle。
- 本轮重新读取CUA应用列表仍无该dev；按其实际可执行文件调用getApp返回Invalid app。
- 当前可调用工具没有另一个能直接绑定该裸进程的App界面连接器。voice专用屏幕接口不用于本次文字任务。

## 拟采用的限定方式

由macOS原生辅助功能AX读取这一个dev进程的窗口/控件，以CGEvent发送普通鼠标、拖动和键盘事件；需要画布定位时只截图该窗口。开始操作前与每次动作前核实PID和实际可执行路径，前台窗口变化时先停止动作并重新观察。

操作范围完全沿用13的A：真实App内创建指定合成流程、普通不完整图提示、添加文本节点/拖线/移动、输入、保存、返回重开、试运行、内部发布v1/v2、明确执行v1并核对结果和历史。该方法只替换界面控制工具；API和数据库继续只读取证，不补写业务结果。

不改dev源码/可执行文件或构建身份，不创建伪装App包，不注入页面JS或修改会话，不扩大native capability或网络范围，不发送模型/商家/付费请求。需要退出时使用App自己的正常退出流程。

## 当前工具约束

CUA的Computer Use文档明确要求：除非用户特别要求其它技术，所有电脑界面操作使用cua_repl（原文：Do not use other technologies besides cua_repl for computer interactions, unless specifically requested by the user）。用户本次已授权代操作目的；采用AX/CGEvent这类替代技术仍需一次明确指示。取得该指示后再实施和验证上述限定方式，不把提案或工具尝试写作完成。


用户随后明确反馈人工A已经完成，因此该替代自动化方案暂不执行，不再请求AX/CGEvent控制授权。当前优先核对人工反馈与实际资源，见13的11:08记录。


## 11:15 用户要求接手 B 与继续 D4

用户明确希望由Codex操作B并继续D4。当前dev仍是PID4642，工具控制限制未解除；未用API代替UI。已准备仅绑定该PID及可执行路径的[源脚本](evidence/step6-d4-20260913-1041/dev-ui-assist.swift)，包含AX快照、单窗口截图、显式激活、窗口范围内点击/拖动/滚动、有限按键和普通合成文字输入；每次动作核对前台进程。它不含权限修改、强杀、业务HTTP调用、页面注入或二进制覆盖。

仅执行swiftc -typecheck且通过；没有生成可执行工具，也没有执行任何AX/CGEvent界面操作。明确允许该替代技术后，由Codex完成B并自行补齐可追踪的新流程证据，继续后续packaged验收；当前A反馈与服务数据仍分别保留，D4不提前通过。


2026-09-13 收口：授权后的dev与packaged真实验收、键盘修复复验和正常重启读回均完成，最终本地D4结论见[17](17-d4-final-qualification.md)。保留前述方案/准备阶段的原始状态，不将当时未执行改成历史通过。
