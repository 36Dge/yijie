# Shopify 启用与选择修复（2026-10-12 至 13 日）

本次仅处理用户截图中的 Shopify 不可用。真实日常客户端重建后，Shopify 已启用，并成功选入聊天输入框。本结论不扩展为商品查询、模型调用、专家整体验收或 D4 通过。

## 定位依据

开始时运行中的 worker 已是阶段7的 `f77ba40baf0c3ae7090bd61f076ade4c62298f138351563c7835556924f88bb3`，不能归因为未更新 worker。用户此前三次初始化失败的日志保留，均为 HTTP200 后初始化失败；仅凭这些枚举日志不能唯一解释当时的服务响应。

本次先以实际 Reqwest 传输、再以固定 SDK 加生产 HTTP 适配器，各进行一次 initialize 诊断（各2个 HTTP请求）。当前通知确为4字节 null，命中原精确兼容规则，SDK初始化成功。临时诊断代码随后移除，原测试文件 SHA256 恢复为 `7d8fcc5796621887fb5cb38c19ba924a260ea511444347664a812dd901d6c1b6`。没有猜测性放宽握手规则。

随后在原运行 App 点击一次启用：操作 `88fc848a-11e9-450b-a5e6-c6dbb4d97237` 的 initialize、tools/list、metadata_artifact 全部成功，但界面显示“连接待恢复”。Sorftime 与 Tushare 也处于待恢复。代码确认 Snapshot 将所有 desired-enabled 项当作严格的整批选择核验；一项旧 Host 记录失败会丢弃整批证据，使健康项也不可用。

## 修复边界

Desktop `src-tauri/src/chat/connectors/provider.rs` 为 Snapshot 分离逐项观察，继续调用原有严格 Host 核验，只合并成功且仍有效的证据，并保留最早有效期。单项缺少原操作、旧 Host 或其他不合格状态只影响该项。

显式 Selection、preflight、发送与 dispatch 保持整批严格验证。快照查询仍不启动 Host、不访问第三方、不写启用状态。没有新增依赖、command、capability、权限、数据库迁移或公共 wire。contract-impact=semantic，具体兼容与回退说明位于 Desktop `docs/shopify-snapshot-recovery.md`；仅本地开发修复，未发布、提交或推送。

## 已执行验证

- 12项 Native provider 回归通过，包含 Shopify 当前连接与另一个旧 Host 安装共存、缺少定位记录、全部旧化、混合选择仍拒绝。测试使用普通内存数据库与既有内存管道，无第三方请求。
- 初次新增用例因安装时间104晚于共用启用助手时间101而违反数据库时间约束；修正为合法时间后通过。初次失败日志保留，不计作产品缺陷或伪造红例。
- Rust fmt、all-targets Clippy `-D warnings`、diff检查、文档构建通过；canonical `./scripts/run-local-demo-fast.sh --packaged` 完成前端及 Native 构建，并正常启动日常 App。
- 原 App 通过 Cmd+Q 正常退出，原 Desktop/Host/worker/Runtime 进程均消失、18081端口释放后再构建。保留原用户历史、安装及其他连接器，无强杀或数据重置。
- 重建后仅点击一次启用。操作 `9f1cb9b4-1f7b-425b-898e-144dd5971ae8` 的 initialize、tools/list、metadata_artifact 均成功，共3个HTTP请求。
- 真实 UI 显示 `Shopify MCP，已启用`；聊天添加菜单显示 `本轮使用 Shopify MCP，已启用` 和启用开关 on。点击选中后 toggle 为 on，输入框出现 `移除 Shopify MCP` 胶囊。另两项仍显示待恢复，证明不再互相遮蔽。

## 调用与未执行

本次共10个公开元数据 HTTP 请求：两次定点诊断4个、原 App 一次启用3个、修复 App 一次启用3个。真实模型消息0，业务 tools/call 0，未发送任务或商品查询。明细见 `evidence/phase8-shopify-ledger.json`，产品诊断只保存固定阶段、状态码、时间及安全错误枚举。

外观仍跳过；未扩大到其他连接器修复、专家内容评测、FEAT-158剩余AC或整体验收。未运行含用户禁止的强杀、权限破坏、恶意资源或攻击注入的全量历史测试，故不声称全库测试通过。此前三次初始化失败的唯一现场原因仍无法由旧日志证明；本次当前真实握手和启用选择均已通过，不补写历史成功。
