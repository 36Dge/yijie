# 暂停检查点（2026-10-23）

后续状态：用户已要求继续，本检查点为历史暂停记录。恢复、修复与真实验收结果见
[本轮完成报告](dual-progress-resume-20261023.md)；Docker 阻塞已正常解除，原生搜索来源扩展和最终直连启动已完成。

状态：用户明确要求暂停。停止开发、构建、模型请求和验收，等待用户恢复；未创建或修改 Git 提交、分支或远端记录。

## 已确认的目标与约束

- 用户接受两种来源并明确区分：模型实际发出的文字标为“模型进度”；根据真实 Runtime 事件生成的客观说明标为“执行进度”。
- 优先复用 yijie-codex → Host → Desktop 原有执行链路，保留真实执行记录、安全边界和现有未提交改动。
- 不伪造模型进度、引用或验收结果。仅正常、非破坏性开发和测试；禁止强杀、故障注入、二进制伪装与权限破坏。

## 已完成

- Desktop 新增只读执行进度投影和 ChatExecutionProgress 组件；按实际网页搜索、页面操作、命令与工具记录生成客观说明，连续同类记录可合并。
- 真实模型进度单独标注来源；等待状态采用客观表述。冷历史、失去实时观察、错误和待审批记录不冒充正在执行。
- 沿用已有网页搜索、重复摘要、空命令详情及消息分类修复。本次没有新增 Runtime、Host 或 Contracts 协议修改，也没有新增模型消息或持久化的生成进度记录。
- 定向前端测试 4 个文件、61 项通过；pnpm lint（ESLint 与 vue-tsc）、文档构建及 git diff --check 通过。

主要改动位于 yijie-desktop/src/domain/conversation-process.ts、src/components/chat/ChatExecutionProgress.vue、ChatTurnGroup.vue、ChatProcessPresentation.test.ts、ChatNativeStreaming.test.ts，以及聊天设计文档。

## 未完成与当前阻碍

- 本轮尚未完成新的 App 构建和真实 Kimi-K3 验收，没有发送新的模型请求。
- 旧 App 已正常退出。首次 canonical 启动因 Docker 未就绪失败；经正常启动 Docker Desktop 后重试，最终仍失败：WORKFLOW: Abnormal owned containers retained; inspect before reopening。workflow-up 退出 1，启动命令退出 2；最后检查没有 18081 监听。
- Docker 与已有容器保持原状，未强杀、删除、重建或绕过启动检查。暂停期间不要继续处理。
- 引用链路仍待后续修复：此前真实 Kimi 原始响应只有最终回答，没有独立进度、URL 或引用注解；强化提示词未改变这一事实。原生 Runtime 目前没有完整请求/映射 web_search_call.action.sources 的链路，不能补造来源或把搜索结果冒充具体论断的引用。

## 恢复位置

1. 阅读本检查点及下列报告；保留所有既有未提交改动。
2. 只读检查 canonical workflow 与已有 Docker 容器状态；修改基础设施前读取适用 AGENTS.md。仅使用正常恢复流程，不绕过检查。
3. 通过 pnpm tauri:demo-fast:app 完成标准构建与启动，再用 Kimi-K3、完全访问权限执行原题“从 5 个重要的维度对比杭州与苏州这两个城市？”。
4. 验证开始、执行中、完成和历史回看，检查双来源标签、网页搜索、重复摘要、空命令卡片和进度分类；如模型未发出 commentary，明确记录该真实分支未触发，不能声称模型进度已实测。
5. 继续审计并按 canonical Runtime/版本化协议路径处理真实来源信息；不伪造引用。

## 报告与证据

- 实现报告：yijie/docs/dev/dual-source-progress-20261023.md
- 本轮证据：.local/audits/dual-progress-20261023/（baseline.json、focused-tests.log、lint.log、docs-build.log、build.log、build-retry.log）
- Kimi 深度审计：yijie/docs/dev/kimi-progress-citations-20261023.md；.local/audits/kimi-progress-citations-20261023/
- 早期修复与真实验收：yijie/docs/dev/conversation-process-fix-20261022.md、conversation-process-live-20261022.md

上述路径均相对 /Users/jack/Downloads/Personal_Info/CrossBSD。不得将“定向检查通过”表述为本轮真实端到端验收通过。
