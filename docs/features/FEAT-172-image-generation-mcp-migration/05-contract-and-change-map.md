# FEAT-172 契约与改动地图（修订 3）

2026-11-12，contract-impact=breaking。Runtime 固定版本与 schema 不变，未公开产品按用户授权直接切换；没有旧客户端兼容窗口或历史迁移。

## 权威源与生成

- `yijie-contracts/jsonschema/media-generation/v1.schema.json`：MCP 输入/结果、专用 Host 桥接、工具说明与已审阅专家路由。Owner：Agent Runtime Team；producer：Host；consumer：应用 MCP；native display 复用同源 Go 类型。
- `jsonschema/document-runtime/v1.schema.json`：原 AdapterStartup 增加配对的媒体 capability/私有桥接 token；已有 Artifact status 资格移除文档环境依赖。Owner：Agent Runtime Team；consumer：Host 与 adapter。原 status DTO 与路由复用。
- `scripts/generate-media-generation.mjs` 与原 document generator 生成 Go/Rust/TypeScript 和 Host 快照；媒体 family 无 Desktop wire 消费，不额外生成 Native DTO。
- 原专家提交、market、native conversation/Artifact 事件源、Skills、Codex canonical schema 均不改变。没有 media_preflight、fallback_reason、专家来源 ID 或第二套生成状态协议。

生成来源与摘要写入显式 `local_worktree_candidate`、release=false 回执。Contracts 基线为实施前 `d658a2bd5dd6ebd5ae5c79a547489eca205d6ede`；已有发布支持窗口按 supported-baselines.md 校验。未经提交不伪造不可变新版本，不改变旧 immutable 同步方式。

## 逐仓实现

| 仓库 | 本期改动 |
|---|---|
| Contracts | 新媒体源与生成器、同源验证；共享 adapter startup 与 Artifact status 语义 |
| Host codex | 关闭旧生图配置；普通会话装配 MCP，已选专家禁用；沿原生 MCP/搜索/审批 |
| Host session | 唯一内置 producer、绑定校验、一次派单、取消、Artifact receipt；旧 handler 不派单 |
| Host artifact-mcp | 独立媒体路由和 capability，桥接现有 Host；共享 get_artifact_status |
| Host imagegen | 保留 SeedreamClient，普通Keychain读取只读且无交互；独立有人值守运营CLI仅请求系统授权 |
| Desktop scripts | 固定日常入口默认 MCP，移除图片启停设置与旧 candidate 启动，更新受管 build/source 检查 |
| Meta | 最新选择政策、ADR、实现与验证证据 |
| Codex/Skills/Connectors/API/Infra | 无实现修改；沿审计的现有能力 |

产品切换时 Host/adapter/launcher 一起从当前源码构建；固定 Runtime 二进制不变。退回时整体退回对应本地应用构建，不能单独打开原生图片开关造成双 producer；不重放旧生成请求。
