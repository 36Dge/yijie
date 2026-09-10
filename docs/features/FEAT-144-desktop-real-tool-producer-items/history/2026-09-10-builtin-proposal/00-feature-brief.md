# FEAT-144 — Codex 内置本地图片查看与原生工具记录

修订：2026-09-10；demo_fast / local。用户委托 Codex 自行选择适当内置工具并确定完整方案。本轮**只落需求，不实施、启动、调用模型、提交或推送**。编号和目录不变；原四文件包完整归档于 [history/2026-08-30](history/2026-08-30/00-feature-brief.md)。

## 产品目标与范围决策

本地用户在已有项目会话中请求查看指定截图、商品图片或设计图片，阅读助手解释，并辨认真实图片查看记录、原生观察阶段和信息缺失。

主选 **Codex 内置 view_image**，唯一新增展示类型为原生 **ImageView**。用户可另行请求通过已有 **exec_command / CommandExecution** 执行 `test -f ./images/product.png` 做普通只读路径检查；完全复用 FEAT-136，不新建 Command 能力，也不将其设为每次看图的强制预检流程或隐藏补发命令。

view_image 已在固定 Runtime 内置，MiniMax 模型目录声明支持图片输入；无需新 MCP 服务、Connector、Skill、账户或图片执行器。它读取图片并将其作为当前模型输入，**不是离线预览或 image-01 图片生成**。真实可用性仍需后续验收。

原 FEAT-144 的真实 MCP producer/入口/安全边界及 8 项待验收 AC 保留历史含义。用户本轮要求改选内置工具，因此当前包改为图片查看样板；**CAP-017 / GS-004 的真实 MCP 目标继续延期、未交付、D4 NOT RUN**，留在本编号后续 MCP 扩展范围。ImageView 不能包装成 McpToolCall；当前新 D0/D4、Command 或 CAP-018 图片生成都不能关闭旧 MCP 目标。

## 用户入口和显示

沿用“选择项目 → 当前会话 Chat Composer → 正常发送”，例如“请使用 view_image 查看 ./images/product.png，说明主要颜色和文字，不修改文件”。调用由 Codex 决定；未观察到 ImageView 时不依据提示词、图片附件或助手声称生成卡片。不新增直接执行工具按钮、Tauri command、注册器或第二提交入口。

卡片复用现有 Timeline/Item shell：标题“查看本地图片”，显示安全图片标签、原生观察阶段，支持折叠、键盘及安全文字复制。不新增预览、打开文件、下载或 Artifact 通道。

- item/started：“已观察到图片查看开始”；忙碌只沿用既有可信活跃 Turn/订阅规则。
- item/completed：“已观察到图片查看记录结束”；不证明图片已解码或模型已完成分析。助手分析仍是独立 AgentMessage。
- 原生 ImageView 只有 id/path，没有 status/error/duration/progress，不造成功/失败码、耗时、步骤或百分比。
- Turn 已结束、历史或连接不明时停止忙碌，缺 Item 结束记录时保留提示，不封口 Item。
- 只复制允许展示的安全文字，不传原始路径、URI、base64、图片 bytes 或原始错误到卡片/日志。

## 访问、数据与费用

产品意图限用户明确指定的当前项目普通 PNG/JPEG；默认 detail，不承诺 original。D4 只用新建验证目录里的普通合成图片、普通路径及只读命令，无商家/账户/凭据/个人信息。不扫描其它目录，不沿链接扩大意图，不读取隐藏配置、用户数据库或凭据。

真实访问权限继续由 Codex filesystem/sandbox 和 FEAT-152 当前模式控制。**意图范围不等于现有系统已提供单文件 OS 白名单**，不得把 prompt 当权限校验。D4 保持“请求批准”；拒绝按原生事实处理，不切换权限促成调用，不改 FEAT-152，不重启 FEAT-137。

Host 复用既有路径脱敏与容量约束，将原生 path 转为安全标签；不能安全显示时用“图片路径已隐藏”和独立 availability/diagnostic，不重读图片生成标签。SQLCipher 复用已观察原生事实和安全显示副本，不新建图片库/缓存/表，不保存新图片二进制副本，不改历史 migration，不复制用户 DB/凭据。

后续建议另行申请最多 **10 次 MiniMax-M3 Responses 请求（含图片输入、标题、审查、自动请求及重试），0 次图片生成**。建议不是授权，本需求当前额度仍为 0，不转用 FEAT-136 的 3/10 或其它历史额度。

## 成功、失败、恢复与历史

成功必须经 canonical 观察真实 ImageView，并正常重开同一已保存记录；附件或助手口述不能替代。

代表性正常失败采用用户显式请求的可选路径检查：对从未创建的 `./images/not-present.png` 执行 `test -f`。读取真实 CommandExecution status 与 exitCode；exit 1 仅表示未通过普通文件检查，不推导唯一原因，不称其 ImageView failed。之后用户明确改为有效图片并再次请求查看，验证恢复。命令可能有环境输出，不要求输出必须为空。

view_image 自身查找/读取失败会 RespondToModel，但发生在 ImageView 创建前，协议没有 failed ImageView。该边界以源码及安全定向测试核验；真实运行自然遇到时记录可观察性限制。助手报错只是模型回答，不能当结构化失败证据；不从无 Item、正文或 Turn 结果推断失败，不为捕获它追加调用、解析 rollout 或修改 Runtime。

重试只来自新用户意图，不自动修复路径/补发。取消走现有 turn/interrupt，不新增 Tool cancel。已观察记录复用 SQLCipher 重开；固定 Legacy 不保留完整 ImageView 冷历史，缺失如实保留，不重建、猜身份或开启实验历史。

## 强制复用与实现边界

能复用 Codex 机制的必须复用：内置工具注册/执行、filesystem/sandbox、ImageView 身份/通知；FEAT-132 native 架构、唯一 NativeDisplayBuffer、thread/read/resume、SQLCipher；FEAT-134/136 的执行事实与 availability/busy 分离；既有 Composer、Command、权限与资源边界。

当前 native v7 的闭合 NativeItem enum 没有 imageView，Host 降级为 unknown/unavailable。后续按 **breaking** 保守治理：推荐版本化 native v8 事件面和独立版本 history 读取面，旧 v7/旧 history 面保持原语义；具体路由与 schema、生成来源须先在 Contracts 固定，本文候选版本不冒充现有接口。不原地扩旧 enum、不手写影子 DTO。

新旧 native 版本仍复用一个显示缓冲和保存链。完整 Item 直接替换；Turn 不补 Item 终态。不新增 reducer、第二累计、正文对账、身份猜测、历史重建或自动封口。保留真实 v4/v5 历史/资源消费者。验证旧新数据方向兼容；默认无新表/migration，不能以回滚为名删除新事实。

未来实现顺序 Contracts → Host → Desktop；仅影响被校验来源时更新真实 commit/digest/pin。Codex、Connectors、Skills 不改。协议不兼容明确阻止新能力，不静默绕过或双订阅。

## 验收与当前状态

完整审计、方案取舍和旧条款处置见 [03-native-audit-and-decisions-2026-09-10.md](03-native-audit-and-decisions-2026-09-10.md)；十项新 Must 全 pending，场景见 [04-acceptance-scenarios.md](04-acceptance-scenarios.md)。D0 只表示用户委托模型定稿后的需求检查；实现、契约生成、真实调用、D4、提交/推送均 NOT RUN。后续实施须有新指令，付费调用单独核对授权。
