# FEAT-173 契约、改动地图与实施顺序（修订2）

当前实施状态：已按修订2及09补充落地并完成本机真实验收；结果、用量与保留限制见[12-real-acceptance.md](12-real-acceptance.md)。以下设计和历史审计约束继续保留。

仅方案，所有下述产品文件都是拟修改位置。本轮文档任务contract-impact=none；拟实施仍为additive。修订2删除对已有ACK/Artifact恢复语义的修改，详见08；未执行源契约生成或实现。

## 权威与兼容

新增独立`jsonschema/video-generation/v1.schema.json`及Go/Rust投影，MCP server仍为yijie_media。旧图片请求/结果、专家协议、Artifact/SSE/IPC、get_artifact_status、AcknowledgeArtifact和播放器保持。新增操作只在新Host/adapter同源构建就绪后启用；旧Host不接新视频操作，旧客户端继续消费既有video Artifact。

Owner为Agent Runtime Team、Platform Team、Client Team；项目实际负责人/Reviewer为段成威，技术方案尚未接受。直接fallback为Contracts `cca445ca30c8d13b11185212b3d709bae67cf4aa`，原支持窗口保留；没有新发布tag或contract commit。独立bucket的旧writer保持性要在实施时证明；若必须升级旧库/收紧旧wire或改变旧终态解释，先提高最高impact并修订方案，不暗中突破additive。

## 拟议线协议

| 边界 | 内容与约束 |
|---|---|
| Generate输入 | prompt、image_mode、image_indices；不接受URL/路径/Key/模型ID/强制重建参数 |
| Get输入 | 可选video_operation_id；省略时只按04第2节解析本聊天本地记录，歧义只返回最多5条候选和是否完整，不猜最新或查询账户列表 |
| 操作引用 | 复用创建root turn ID，Host以session+root+video验证归属；不是供应商task ID、新UUID服务或Code Mode cell_id |
| 私有HTTP | POST `/internal/media-generation/v1/generate-video`、`/internal/media-generation/v1/get-video-result`；原metadata包装thread_id/turn_id；专用media bridge bearer；请求/响应16KiB |
| 短回执 | 新VideoResult有source=builtin、状态/code/next_action、可选本地操作引用和最近实际provider_status/观察时间；不返回供应商ID/URL/原始错误 |
| Artifact引用 | staged/committed携带artifact_id与delivery_turn_id；delivery_unconfirmed也可携带原引用，但存在ID不代表成功。新类型明确条件约束，不修改旧图片union |
| 私有记录 | 一条原root对应一条版本化提交/归属记录，另含一次交付标记；不保存ACK、manifest或产物副本，随原session cleanup清理 |

VideoResult的status建议pending/staged/committed/blocked/failed/unknown。code包括provider_pending、ok、existing_operation、selection_required、operation_not_found、expert_required、input_unsupported、operation_conflict、service_unavailable、outcome_unknown、provider_failed、provider_expired、delivery_rejected、delivery_unconfirmed、local_cancelled。next_action只能指向查询原操作、选择明确操作、核对原Artifact或报告状态，不能含retry_create/fallback。无task ID的unknown禁止GET；有task ID的暂时GET错误不能改成供应商failed。

pending、existing_operation和selection_required作为有结构的正常业务分支返回，MCP isError=false，不能据工具RPC完成显示“视频已生成”。既有Native McpToolCall生命周期保持；Host显示投影用稳定短标签区分已受理/仍运行/需选任务/交付未确认。真正拒绝或失败按明确code返回，不泄露供应商正文。条件必填/枚举/长度/候选数量/未知值策略先写入源契约，再生成消费者。

供应商HTTP DTO留在Host第三方适配边界，和易界公共DTO分开；凭据/endpoint与model只由Host决定。Native普通tools/call未提供业务幂等或方舟任务持久身份，不能把JSON-RPC ID/原生cell当业务记录。

## 拟改动地图

| 仓库 | 位置 | 边界 |
|---|---|---|
| Contracts | 新video-generation schema、generator、投影/source.lock、tests及generation-plan登记 | 既有图片/专家/Artifact/AdapterStartup源不改 |
| Host provider | 新internal/videogen/seedance.go及定向测试 | stdlib HTTP、同ArkCredential；一次POST、精确GET、允许域下载 |
| Host session/store | 视频操作及本地归属查找；现有prepared turn、取消、cleanup接线 | 同root幂等＋同聊天未决屏障，使用已有root ID；不建Agent状态机/配额/定时清理服务 |
| Host Artifact生产者 | 新视频生产者调用原Put/publishV3；一次交付标记 | 原Store/ACK/Status/Native恢复不改，不持久化视频专用ACK |
| Rust adapter | media.rs及新同源video_types | 两新tool，原server/process/token/超时边界；pending与选择分支不是工具异常 |
| Runtime装配 | media_generation.go、现有effective isolation/approval检查 | 原生白名单、精确审批、两模型namespace；不改Runtime源码/patch/协议 |
| Host入口/提示与展示 | app/main、私有路由、native_mcp.go与既有媒体提示入口 | 增加视频受理/恢复说明和稳定标签，不伪造Native执行事实或承诺自动续轮 |
| Desktop | ChatArtifactShell.vue的provider/video失败文案；原application/host_bridge、chat.store/artifact.store、ChatPage组件链的接线验证与必要修正；canonical来源回执 | 复用现有播放器、Native command/协议、SQL与ACK；不再预设Desktop绝对零修改。详见09，不增加恢复机制 |
| Meta | 本需求及ADR-0026 | 已接受并实施；历史方案与当前验证分开记录 |

Skills/Connectors只读，保留LinkFox专家本身的选集、参数及审批。API/Infra、新Tauri command/capability、任务中心、参数面板、额外MCP client均不进入本期。

## 连续实施依赖顺序

1. 用户接受修订2范围与D0；重新核对当前来源/dirty和运营资格输入，费用仍另批。
2. Contracts先定义两新操作、无句柄恢复、既有未决拒绝、交付未知的封闭回执；完成生成/方向兼容和新族定向检查。
3. Host实现最小记录、原root引用、同聊天事务预占、同Key客户端和正常取消；先证明无模型/供应商重建循环。
4. 接入同源adapter、原生搜索/Code Mode/审批与专家隔离；GET/下载绑定当前观察root，不复用旧创建context。
5. 按09完成Host视频bytes/事件、当前交付turn映射、既有schema9/12订阅、Native提交通知、projection/reference双刷新与对话流组件接线；最小修正provider/video失败文案，不修改ACK/Status或新增播放器。完成02恢复矩阵、VD01–07、两模型固定Runtime回环及FEAT-172回归。
6. 代码/构建审查完成后正常退出App，用canonical日常入口激活；必要时对新Host构建做已有运营凭据复核，不改Keychain条目或搬Key。
7. 独立批准FEAT-173额度后再做四场景真实生成和自然语言停止/恢复验收，核对默认body、音轨、体积、播放/seek/保存。否则所有真实AC保持未运行。

## 回退

仅禁用新视频工具/停止当前观察，保留新reader、操作记录与历史视频；原图片、专家及本地已提交产物继续。关闭/清理不自动DELETE，不降库/删历史。换回旧Host前必须证明其保留新私有bucket；未证明只关闭能力。已有供应商任务可能继续，Artifact跨Host不可补领的情况如实报告，不借回滚重发。

## 第2版对话流交付补充

详见[09](09-video-chat-delivery.md)：视频事件沿既有Artifact wire；该展示文案修正自身contract-impact=none，整体新增视频工具仍按additive。没有理由仅为视频另加SSE版本、Tauri command/capability、CSP外链或数据库迁移。若发现确需改变既有线协议/持久语义，仍先在权威源更新，不以“接线修复”绕过Contract First。

实现复审的增量影响为semantic（详见13）：工具描述/权威语义明确，但wire字段、枚举和调用名不改；生成器同步当前本地候选，不刷新既有Runtime族的来源pin。
