# FEAT-144 原生工具审计与定稿决策

2026-09-10。保存完整审计结论和用户四项要求；仅需求，不是实现报告。用户委托 Codex 选择/定稿，以下为委托下的需求决策，不冒称另一次人工批准。

## 原需求、审计与本轮授权

原 FEAT-144 在 2026-08-30 从 FEAT-136 拆出 CAP-017/GS-004，目标为一个真实 MCP 工具的接入、过程/结果、安全失败及正常重开历史。8 AC 全 pending，D0/implementation blocked，verification/Tool D4 NOT RUN，独立额度 0。2026-09-10 复查 D0 实际 exit 1：product_ux.status must be PASS for D0。

缺失的决策包括真实工具、价值/入口、producer 所属、参数/数据分类、访问/副作用、成功失败方式及额度。通用 schema/mapper/卡片测试不能证明真实 Tool。Codex 已有 MCP 引擎，而 Connectors 只有健康/状态骨架，示例 Skill 的 MCP 配置占位。

用户本轮要求：①落盘并记住完整审计，能复用 Codex 必须复用；②选 Codex 内置工具；③修正全部过期实施依据；④由模型给出工具、用户问题、入口、访问、安全验收方案。明确只落需求。当前首期因此改为 view_image 原生内置工具；原 MCP CAP-017/GS-004 延期未交付，后续仍需真实 MCP 产品决策与验收，不被本次看图 D4 替代。

原四文件逐字节从元仓基线 6f12939aa85f8a9c1f55e89f1018c60501a2f494 归档于 history/2026-08-30；原日期、来源、阻塞及 pending 不覆盖。

## 来源和并发保护

| 仓库 | 完整 HEAD |
|---|---|
| 元仓 | 6f12939aa85f8a9c1f55e89f1018c60501a2f494 |
| Contracts | db7a607c1c091fc4f4243829d68d5b673eb7e2c3 |
| Host | f4cf01bd6f7e9f37792ef743d44f0ce10527c10b |
| Desktop | 8bfa5ca284fddb86d7cdd2a406c5041c49367688 |
| Codex | 6c1ad767f0997845b8258a1c452fd4eb7577579f |

五仓分支 chore/retirement-baseline-20260905。完整远端、其它仓来源及并发路径 SHA-256 见 evidence/requirements-audit-2026-09-10.json。native Contracts pin 为 6f632f155eacdaf93df0e0b00b5dab9e369c5442，权限 Host pin 为 f4cf01bd6f7e9f37792ef743d44f0ce10527c10b，均不变。

Runtime 构建提交 b2b20e2fc4a0c94834f34d8cc459e488a1b56277、0.144.6、experimental_api=false。实查 build commit 到当前 Codex HEAD 的 codex-rs 子树零差异；HEAD 与构建来源不得混称，不能启用历史 FEAT-137 patch 或重建 Runtime。

Desktop 初始 10 个并发路径包含两个设计文档、ChatComposer.vue、ChatPage.vue、variables.css、home-opening 验证文档及四个组件/几何测试文件。本轮不修改、覆盖或提交它们，其测试不计本需求证据。其它代码仓初始干净；只在元仓落需求。

## 完整工程事实

以下路径相对 CrossBSD；行号为审计定位，后续按固定源码复核。

| 事实 | 源码 | 意义 |
|---|---|---|
| MCP 原生 id/server/tool/status/arguments/result/error/duration 已具备 | yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/item.rs:301；core/src/mcp_tool_call.rs:876 | 不自研 Tool 引擎；未接业务工具不等于 Codex 没能力 |
| Host native MCP 仅工具调用/参数已隐藏/结果已接收，恒 partial，未传 Tool error/duration | yijie-agent-host/internal/session/native_conversation.go:168 | 不完整兼容基础，不是完整业务 Tool |
| Desktop native MCP 借旧 DTO 伪填 started/lastSource、identity unknown、progress=[]、error=null | yijie-desktop/src/domain/conversation-view.ts:375 | 不把该分支用作新 ImageView 模型；MCP 缺口留后续 |
| Tool 卡片有参数/结果/进度/错误/复制 renderer，旧 in_progress 判断可能误报历史忙碌 | yijie-desktop/src/components/chat/ChatToolItem.vue:38；ChatToolItem.test.ts:46 | 合成 renderer 测试不是原生调用证据；复用正确 busy 规则 |
| MCP progress 协议存在，未找到 app-server 生产发送点；底层 handler 记录通知，native switch 未接入 | yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/mcp.rs:214；rmcp-client/src/logging_client_handler.rs:61；Host native_conversation.go:318 | 不据 schema 承诺持续进度；0 progress 合法 |
| Legacy 保存 McpToolCallEnd，原生 builder 可构造 MCP 历史 | yijie-codex/codex-rs/rollout/src/policy.rs:102；app-server-protocol/src/protocol/thread_history.rs:787 | MCP 与 Command/ImageView 的冷历史规则不能混同 |
| ImageView 只有 id/path | yijie-codex/codex-rs/app-server-protocol/src/protocol/v2/item.rs:367 | 独立原生类型，没有 status/error/duration/progress |
| view_image 用原生 FS/sandbox；读 bytes 后发 started/completed，再处理图片输入 | yijie-codex/codex-rs/core/src/tools/handlers/view_image.rs:143–201、221 | 复用执行器；记录结束不等于解码或模型理解完成 |
| 文件失败 RespondToModel，发生于 Item 创建前 | 同上:156；core/tests/suite/view_image.rs:1255 | 不制造 failed ImageView，助手解释不当原生失败 |
| NativeItem enum 闭合无 imageView，Host 降为 unknown/unavailable | yijie-contracts/openapi/native-conversation/native-conversation.yaml:124；Host native_conversation.go:57 | 契约先行，不能只改 Vue 或冒充 MCP |
| Legacy 不持久化 ImageView ItemCompleted，旧 ViewImageToolCall 也 transient | yijie-codex/codex-rs/rollout/src/policy.rs:88、121 | 已观察 SQLCipher 可重开；冷历史不保证完整 |
| 唯一缓冲、Item 整体替换、原生保存和来源分离已具备 | yijie-desktop/src-tauri/src/chat/native_conversation.rs:132；native_conversation_storage.rs:82；application.rs:2218 | 不新增 reducer、历史构建器、累积器、保存链 |
| Connector 只有 health/status；示例 MCP 占位 | yijie-connectors/internal/app/app.go:30；yijie-skills/plugins/amazon-listing-optimizer/mcp/servers.toml:1 | 本期不顺带建设平台执行器 |

## 选型与五项产品决策

| 方案 | 依据与取舍 | 决策 |
|---|---|---|
| view_image | 内置、只读、无需新服务；有 ImageView，失败/冷历史可见性有限 | 唯一新增支持类型，明确限制 |
| Command 查文件 | 已有 native status/exit/安全输出/保存；FEAT-136 已交付 | 复用 exec_command 作可选路径检查和正常失败回归，不重复实施 |
| web_search / update_plan | MiniMax supports_search_tool=false；plan 已归 FEAT-134 且非独立 Tool Item | 不作本期新增样板 |

固定 handlers 未发现独立 read_file/list_dir/grep_files，不能按印象创建。view_image 已加入内置工具集（core/src/tools/spec_plan.rs:750）；MiniMax 已声明 text/image 输入（Host internal/codex/provider.go:404）。macOS UnifiedExec 默认启用并覆盖 shell_type，实际注册 exec_command（features/src/lib.rs:818、tools/src/tool_config.rs:105、core/src/tools/spec_plan.rs:628）。实际注册仍在未来来源核验中确认。

| 需明确的问题 | 定稿方案 |
|---|---|
| 工具 | view_image；可选检查复用现有 exec_command |
| 用户价值 | 看当前项目指定图片，读助手解释，辨认原生查看记录与信息缺失 |
| 入口 | 当前项目的普通 Composer，无直接执行按钮、MCP 注册、Tauri command 或第二入口 |
| 访问 | 意图仅指定普通 PNG/JPEG和显式只读检查；实际权限由既有 sandbox/FEAT-152控制，不声称单文件 OS 白名单；图片进入当前模型 |
| 成功/失败 | 合成 PNG 真 ImageView；显式 test -f 普通缺失路径的真实 Command 检查失败；用户改为有效图片恢复；同一已保存记录正常重开 |

Command exit 1 只表示普通文件检查不通过，不保证唯一原因，不是 ImageView failed。不能用其通过结果关闭旧 MCP 失败 AC。直接 view_image 失败无结构化 Item 是已知来源限制；不为了捕获失败额外调用或造事件。建议未来专属 10 次含图 Responses、0 生图，当前 allowed=false/max_actions=0。

## 源契约、保存兼容与实施边界

本轮实际改动为文档，contract-impact=none；feature.yaml 的 breaking 是后续实现的保守分类。闭合 enum/版本校验存在，不能未经方向验证就宣称 additive 或复用旧版本透传新类型。

1. 从冻结 Runtime ImageView canonical schema 定义新版本安全投影，只保留原生 id/type 及一个安全路径标签。不得新增 status/error/duration/progress、注册身份或原始图片数据；不得为标签读图片。
2. 推荐候选 native v8 事件面和独立版本 native history 面；旧 v7及旧 /v1/.../native-thread 保持原合同。具体路由、schema_version、版本错误、SDK/generator、source locks 先在 Contracts 固定。本文版本是设计候选，不是已发布接口；不得原地扩旧闭合 enum。
3. 新端只订阅一个匹配版本 native 主通道；不兼容明确提示并停用新能力，不双订阅、不静默旁路、不自动补发。必要的版本安全投影复用 Host 传输设施，不新增生命周期表。
4. Host 保留原生 id/type，复用身份/权限、路径脱敏与容量边界；不替 Runtime 执行图片工具、不猜工具身份/状态、不解析模型正文。
5. Desktop 使用生成类型及 native 专用只读分支，保留 Item/source/lastMethod；在既有 NativeDisplayBuffer 接受适用版本，完整对象走同一替换链，不套旧 MCP DTO。
6. 复用 commit_native_view、SQLCipher facts/views 与原生读历史。无新表/图片缓存/保存器。验证旧 v7事实→新 reader、新事实→仍支持旧 reader 的安全 unknown/版本不可读提示，不能因一个新类型损失全部旧历史。旧端不兼容必须先确定明确拒绝及回滚方案，不能删除新事实或暗改旧 migration。数据库 schema 变更不在默认范围。
7. 未来按 Contracts → Host → Desktop固定真实来源；只有受影响来源才repin。Codex、Connectors、Skills不修改。新native版本是已有架构的兼容演进，不是第二引擎或 Runtime 升级。

旧v4/v5 DTO、IPC、表、reader、资源/安全helper仍有消费者，保留兼容职责，不整包删除。FEAT-134/136对完整对象、availability、busy的边界不回退。来源/兼容不通过就停，不放宽门禁。

## 旧条款逐项处置

| 旧要求 | 当前处理 |
|---|---|
| v5 主链与8月基础提交 | 保留历史；新增能力走FEAT-132原生架构及版本化安全投影 |
| completed reconciliation / late-event seal / replay重建 | 删除新实现要求；只验证既有去重、完整对象替换、不串ID、Turn不封口Item |
| 每个Tool必有progress/failed/error/duration | 按原生类型裁剪；ImageView字段缺失保留，不要求延时或持续忙碌 |
| SQLCipher hydration/expand | 复用现有保存及thread/read/resume；默认无新表/migration，仍验证持久兼容 |
| 工具失败必须合成稳定failed | 不制造ImageView失败；Command检查失败和模型解释分别记录 |
| unknown必须resync恢复 | 安全unknown/availability，不自动读历史、重放或猜接管 |
| Connector执行、Skill声明 | 本期Codex已有内置处理器执行，不向Host/Runtime写新业务；MCP路线延期 |
| permission变更 | none；意图与实际权限分开，权限扩大不在本期 |
| 旧D0阻塞/8AC/旧额度 | 原四文件归档；新10Must从pending开始，旧MCP未交付，额度不转用 |

## 场景推演、自审与非目标

成功、无Item、路径隐藏、内容缺失、模型不支持图片、权限拒绝、失败不可见、超时/连接不明、取消、重复、并发会话、用户重试、重开、版本拒绝均在场景文件分开。既有业务outbox、transport去重、加密与权限适配不是重复执行引擎，仍保留。

不做真实商家MCP、工具市场、插件安装、OAuth、外部网络检索、图片生成/编辑、FileChange/Diff、FEAT-137、FEAT-152改权、Runtime升级、实验历史、rollout解析或ThreadHistoryBuilder复制。MCP的既有展示缺口记入延期范围，不借本期通过关闭。

遵循最新ADR-0013/0016的FEAT-132补充。旧豁免与后移检查不自动恢复，也不冒称PASS；本期新增ImageView的light/dark、键盘、最小窗口/200%是本期要求，不重开FEAT-136/143旧门禁。

写作后安排独立阶段的源码/需求自审，检查原生事实、可行性、失败证据、兼容、预算、并发保护和MCP未交付标记；结果见02-verification.md。不冒称独立人工批准，不以实现/真实调用填补本轮文档缺口。
