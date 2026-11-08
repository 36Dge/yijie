# FEAT-169 原生工具接入

2026-11-07。用户明确要求只接入 V2 多代理、apply_patch、Code Mode exec/wait 和四个 memories 工具，必须复用原生能力。该指令授权本地实现和必要适配，不授权付费模型验证、Git 提交/推送、清除历史或公开发布。

## 用户结果

在现有易界聊天、两种已支持主模型和正常权限模式下使用这四组工具。新执行统一 V2，不新增 V1 产品入口；旧执行事实保留。通过现有活动流、文件变更及产物展示承接结果，不为工具开关新增设置页面。

## 确定范围

- V2 直接复用原生 spawn/message/followup/wait/interrupt/list 与会话树、并发、预算、取消和历史。处理正常恢复的旧线程版本选择，不改写已有原生日志。
- apply_patch 和 Code Mode 复用原生执行器。为当前 Responses 提供方补最小函数输入适配，保留原工具名称、语法校验、生命周期及权限。
- memories 复用原生目录、追加笔记和 list/read/search。此轮仅接入用户点名的四工具，不自动提取、整理或清理原有聊天记忆；自动管线须遵守原生 generate_memories=false。
- 子代理的本地工具执行沿原生权限；连接器和产物上传继续由主会话持有其现有本轮授权，不将父轮 MCP 租约授予子代理。补子代理必要的原生审批承接。
- input-only 草案继续无工具。其他未点名工具不新增启用，不改变两个主模型身份、凭据来源、原生搜索和 Seedream 路由。

## 交互与失败

提交后沿现有活动显示真实工具进度；成功展示实际结果，补丁差异和文件沿原通道读取。空记忆明确为空，重复笔记和正常格式错误按原生错误返回。用户取消走原生 interrupt/取消令牌；未知提交不重发。恢复读取不能重新调用工具。旧会话在新配置下开始新执行时使用 V2，历史 V1 工具记录只作为既有事实保留。

## 技术与契约

最高 contract-impact=breaking：新执行统一 V2、模型工具输入表示与市场隔离配置发生语义变化。先在 fork 原生源码的可重放补丁中形成候选及 canonical schema，再由 Contracts 生成兼容投影/配置事实，再接 Host 和 Desktop。保留已有 Runtime 制品；新二进制只由 canonical Cargo 构建到独立候选目录。不开新第三方依赖，不复制 Agent、JS、补丁或记忆执行器。

源码依据：Runtime tools/spec_plan、features/feature_configs、core/session、ext/memories、memories/write；Host market_runtime/session_protocol/native_config_layers；Connectors worker Gateway 的 thread/turn lease；Desktop 原生审批与执行流。

Kimi 当前官方文档明确 custom 工具仅支持 apply_patch，因此 Code Mode 不可只打开开关：https://platform.kimi.com/docs/api/responses 。MiniMax 使用既有 Responses 的函数工具路径，不变更模型或地址。

## 验收与边界

见 02-verification.md。先进行正常本地协议和真实固定 Runtime 的定向验证，零供应商请求；真实模型使用在代码、候选和验证场景准备完成后单独确认额度。不得把回环响应当成真实模型自主选工具通过。现有用户改动原样保留，不运行攻击 fixture、强杀、权限破坏或可执行文件伪装测试。

## 用户追加的第二阶段（2026-11-08）

随后用户明确追加 request_user_input 与 get_context_remaining/new_context 两组，要求先源码审计并复用原生。已确认保留自动压缩、仅显式新窗口的策略。接入、独立8次Kimi额度（实际4次）及原开发入口加载结果见[06记录](06-user-input-context-execution.md)；前面的四组范围与40次额度保留为历史阶段，不混作同一授权。
