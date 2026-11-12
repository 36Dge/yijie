# FEAT-172 图片入口迁移实施方案（修订 3）

2026-11-12，Accepted / 已实现并完成本地验收。用户已授权实现，并追加“选定专家不可用时不再内置兜底”。本版取代修订 2 的兜底、预检与结果关联设计；[03源码审计](03-source-audit.md)、[06复审记录](06-design-reaudit.md)保留历史事实。

## 1. 原生复用与入口

应用自动装配 `yijie_media.generate_image`。固定 yijie-codex 源码、二进制、canonical schema 和补丁链均不变；通过现有配置固定 `yijie_host_images=false`、`features.image_generation=false`，不注册 dynamic 图片工具，不绑定旧反向图片业务 handler。Runtime 自带的 OpenAI `imagegen` 系统技能也通过原生 `skills/list` + 精确路径 `skills/config/write` 停用；其旧指南对应已退役入口，不适用于应用 MCP。不改写技能文件、不按名字屏蔽用户同名技能、不关闭其他技能。

工具发现、调用、超时、原生审批与事件、Code Mode、工具后 `needs_follow_up` 全部沿 Runtime。tool_search 开启时采用既有 deferred MCP 策略，关闭时直接暴露；不增加 Direct patch 或 Host 搜索/执行循环。MiniMax 对两个应用 MCP namespace 复用已有 `code_mode.function_namespaces` 函数适配；Kimi 保留标准 namespace 与 deferred 搜索。线程配置用 dotted leaf keys，避免覆盖整个 features 表。

## 2. 进程与传输

复用 Host 拥有的 `artifact-mcp` 进程，在独立 `/media/mcp` 路径提供媒体 MCP；媒体 MCP capability、Artifact capability 和 Host 私有媒体桥接 token 分离，均由 Host 随进程生成。供应商 Key 不进入 Runtime、MCP、模型、日志或前端。沿原 EOF/取消/等待退出，无强杀与自动重启。

`POST /internal/media-generation/v1/generate-image` 仅桥接当前 Session 与 SeedreamClient。Gateway 从原生 `_meta.threadId` 和 `_meta.x-codex-turn-metadata.turn_id` 取身份；Host 验证当前活动主轮、已接受会话、专家绑定、取消和附件。普通 MCP metadata 不含通用 call_id，因此不用自造原生调用 ID；当前轮最多一次内置派单，用封闭输入摘要识别重复，原生 item ID 继续用于显示。

共享进程随应用媒体功能装配，不依赖文档开关或非空市场选集。进程不可用时对应 MCP 不可调用，普通文本 Runtime 保留。内置生图不要求选择、安装或授权市场服务；应用基础设施就绪与专家提交仍沿原有资格、资源、scope 和选择校验，不增加故障降级提交分支。

## 3. 工具与交付契约

唯一新工具 `generate_image(prompt, use_current_reference)`。两字段必填，prompt 非空且有界；不接受 provider/key/URL/path/base64/身份/强制路由参数。`use_current_reference` 只引用当前用户输入的一张 PNG/JPEG；图片分析不得调用生成。

工具 readOnly=false、destructive=false、openWorld=true、idempotent=false；150 秒超时、禁止并行工具调用。沿已有应用内置使用政策以原生逐工具 `tools.generate_image.approval_mode=approve` 调用（`auto` 会按写操作注解要求额外确认，不能将两者混同），Host 一次派单约束保留；专家审批原样保留。

返回封闭 receipt：status、code、next_action、source，以及成功时的 artifact_id。staged 仅表示 Host 暂存，committed 由已有 Native ACK 决定。生成 bytes 沿 Artifact spool、v3 事件和现有图片查看器，不经模型传递。继续复用 `get_artifact_status`，将其资格与文档环境加载解耦，不新增查询媒体任务的工具或数据库。

同轮相同输入复用原 receipt；进行中返回 state_pending，参数变化返回 operation_conflict。超时/未知不自动重发；新用户请求才建立新 turn。取消沿 HTTP、MCP 与 Runtime/Session 传递，迟到结果不得发布为成功。

## 4. 专家选择是执行约束

已验证的专家 ID/version/role digest 继续由原有专家绑定和提交机制冻结。已审阅图片专家的服务/方法路由常量迁至媒体契约，既有专家审批与一次创建限制复用；未知专家不会被解释为“未选专家”。

所有选定专家会话禁用 `yijie_media` 的原生 MCP 配置；Host 调用入口另查当前 turn 路由与存储中的专家绑定，以覆盖历史中留存的工具定义。失败、不可用或能力不匹配不会改变此约束。

| 当前选择/状态 | 行为 |
|---|---|
| 未选专家 | 自动装配内置 MCP，正常生成 |
| 已选专家且能力可用 | 使用专家配置的工具和原审批 |
| 资源、工具、授权或 worker 不可用 | 现有提交/执行路径返回不可用，保留选择 |
| 输入不支持、任务失败、处理中、未知 | 报告专家状态，按专家既有规则查询；内置调用数为零 |
| 用户拒绝或取消 | 沿现有停止流程，不换提供方 |
| 用户显式更改/移除专家 | 原绑定操作成功后的新请求按新选择执行 |

不引入 `media_preflight`、preferred/effective 双选集、跨轮兜底标记、专家终态解释器、Host 原生结果归并或媒体协调器。无需修改专家提交 wire/schema、专家数据库或 Skills 的失败即停止约束。

## 5. 凭据

当前非公开 local 范围复用 Host 作用域的 Seedream Keychain 条目，由运营方预置。Host 查询必须禁止认证 UI，不创建/复制/更新/解锁凭据；缺失或需要交互时返回服务不可用。移除旧用户输入 Key 的弹窗。只有运营方明确执行有人值守的 `--authorize-media-credential` 才会请求系统授权；普通生成和只读检查始终禁止交互。供应商、模型和参数沿既有批准实现，不给模型选择接口。

无需新建 API/Infra/数据库/额度平台。该方案只覆盖当前受管本机；公开共享服务应另案设计服务端凭据与额度，不能把共享 Key 打包到客户端。凭据预置与真实调用需作为验收事实，代码存在不代表已可用。

## 6. 实施与验收

整体 contract-impact=breaking（入口和凭据交互），Runtime canonical 协议不变。按 [05契约地图](05-contract-and-change-map.md) 先源后消费者；本地工作树 candidate 必须标明非发布来源，已有不可变来源模式不放宽。

Contracts → Host/MCP/凭据/Artifact → 日常 launcher 与同源检查 → 非计费定向验证 → 有明确额度后真实 UI/供应商验收。保留用户原有 Desktop 改动。不提交/推送/公开部署，不构建新 Runtime，不触碰历史数据。
