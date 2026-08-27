# Codex 风格近似一致性推测策略

> Policy ID: `codex-inspired-approximate-parity-v1-2026-08-27`
>
> Mode: `owner-approved-inference`
>
> Effective at: `2026-08-27`

## 1. Owner 决定

1. 不再要求或等待任何 Codex Desktop 人工截图、录屏、逐场景记录或版本专属 UI 证据。
2. 开发可以依据公开可理解的 Codex 类对话模式、Yijie 当前实现、固定 Runtime 能力和工程判断进行推测。
3. 验收目标是交互层级、状态反馈和整体布局“风格相近、易用且一致”，不要求与任何 Codex Desktop 版本逐像素或逐状态完全相同。
4. 先前提供的图 1、图 2、图 3 已全部撤回：它们不再是需求、设计、验收、Freeze 或 provenance 的依据；仓库中的副本和派生 manifest/hash/场景记录已删除。
5. 不建立 Codex Desktop version/build Freeze ID；后续 App 更新也不触发证据 drift 或人工补采任务。

对话系统中的原始附件不属于项目仓库文件，项目无法从对话历史中物理删除；本 Feature 明确禁止继续引用、复制或据其声明 observed parity。

## 2. 推测依据优先级

从高到低：

1. 当前用户明确的产品目标、主动排除项和后续验收反馈；
2. `yijie-desktop/docs/design/docs/design` 中的 Yijie UI 规范与既有组件/token；
3. 固定 `yijie-codex 0.144.6` stable schema、`experimentalApi=false` 和当前 Host/Contracts 权威投影；
4. Yijie 当前 Chat UI、store、scroll、history、error/recovery 等已实现行为；
5. 工程团队对 Codex 类桌面对话产品的通用推测。

任何推测都不得写成版本专属实测事实，也不得以“Codex 就是这样”为事实陈述。实现冲突时，Yijie UI 规范、固定 Runtime 边界和 Owner 最新决定优先。

## 3. 验收方式

- 不要求 Codex Desktop reference screenshot/video、版本/build 或证据 hash。
- 使用需求场景、组件/状态单测、生产 parser/store replay、light/dark/minimum-window、键盘/焦点/a11y 和真实 Yijie local smoke 验收。
- 视觉验收允许间距、色彩、图标、文案和局部布局与 Codex 不同；只要求整体信息层级清楚、状态可理解、主流程连贯，并遵守 Yijie UI 规范。
- `owner-approved-inference` 是产品设计依据，不是外部参考证据 provenance。

## 4. 主动排除项

以下 8 项均为 `intentional product difference`，本 Epic 不实现：

1. 语音；
2. 模型版本信息；
3. 模型推理强度信息；
4. 右上角分享；
5. 切换置顶摘要；
6. 显示侧边面板；
7. 分支到新聊天；
8. GS-006 文件修改与 Diff。

“模型推理强度信息”只指配置/档位 UI，不排除回答过程中的用户可见 reasoning summary。GS-006 的排除只针对文件修改与 Diff 交互；既有 Host v3 Artifact 展示能力不因此删除，但不得把 Artifact 卡片包装成 Diff。

## 5. 不变硬约束

- 不修改、升级、重编译、替换或同步 `yijie-codex` Runtime、binary、schema 或 pin。
- canonical local 入口继续要求 `experimentalApi=false`。
- 不伪造 Runtime/Host 未提供的生产事件。
- 不通过强杀、破坏权限、替换二进制、攻击载荷或其它危险故障注入制造验收结果。
