# FEAT-173 源码审计

本次重新读取当前源码，不将FEAT-172的历史03审计当作迁移后的实现。FEAT-172此前实现/复审现已进入新的仓库提交；本轮起点7仓均clean。逐文件SHA-256、远端和行数见[来源证据](references/source-audit.json)。没有读取运行中数据库、Keychain或真实供应商状态。

## 1. 当前来源

| 仓库 | 完整HEAD | 分支 | 开始状态 |
|---|---|---|---|
| yijie | `80c29c7261f90af524da4a129a8e82ac142fed5f` | `chore/retirement-baseline-20260905` | clean |
| yijie-agent-host | `da19be66b80dd3235a7622983e58f471a58da9ee` | `feat/feat164-primary-20261028` | clean |
| yijie-desktop | `ed5ee7a52ddef30006ad91d3f9231ebd7c17f065` | `feat/feat164-primary-20261028` | clean |
| yijie-contracts | `cca445ca30c8d13b11185212b3d709bae67cf4aa` | `feat/feat164-primary-20261028` | clean |
| yijie-codex | `fe3f5b1c768f2a1464314e2a350d419a3e63d9c6` | `chore/retirement-baseline-20260905` | clean |
| yijie-skills | `3698a970cf601afbb7fe1691e86d413df1481c09` | `feat/feat164-primary-20261028` | clean |
| yijie-connectors | `37552bec1c31bca95457af7145e0dad206df1f8a` | `feat/feat164-primary-20261028` | clean |

Fixed Runtime来源仍为`fe3f5b1c768f2a1464314e2a350d419a3e63d9c6`；日常tool-search候选由Contracts lock固定，二进制SHA为`7d49018c29704fa9863da72a34d780b8ad0e67c9ffe1821ebd1c1b94d9a46d49`。本轮只读候选来源，没有启动/重建Runtime。

## 2. 已有生图端到端事实

| ID | 源码入口 | 当前事实与对视频的意义 |
|---|---|---|
| S01 | Host `internal/app/app.go`，`cmd/desktop-host/main.go` | 完整local媒体profile自动开启BuiltinMedia；同一Host创建SeedreamClient与artifact-mcp，应用拥有能力生命周期，不依赖用户市场安装 |
| S02 | Host `internal/artifact/adapter.go`；`artifact-mcp/src/main.rs` | 标准构建摘要校验、stdin启动数据与EOF退出；同进程提供artifact/media路由，MCP capability和Host bridge token分离；无需给视频另起服务进程 |
| S03 | Host `internal/codex/media_generation.go` | `yijie_media`原生MCP配置；精确image工具approve；150s tool timeout；Kimi原生搜索与MiniMax函数namespace适配，features使用leaf override保留完整profile |
| S04 | 同文件及`runtime.go` | 旧yijie_host_images与features.image_generation关闭；原生Skills API仅禁用旧系统imagegen路径，用户技能/其他能力保持 |
| S05 | Host `artifact-mcp/src/media.rs` | 工具输入封闭；threadId/turn_id来自原生metadata；145s HTTP桥接，16KiB结果限额；结果含短回执和下一步，不带图片数据/供应商URL |
| S06 | Host `internal/app/media_generation.go` | 专用bridge bearer、16KiB请求、严格生成DTO解码；生成器在Host执行。视频应按同样边界增加新操作，不向模型暴露供应商配置 |
| S07 | Host `internal/session/media_generation.go`、`provider_image.go` | 当前根会话、持久专家绑定、5s原生binding等待、一轮一次、摘要幂等、匹配turn取消/终态；复审修复保证迟到旧通知不伤新轮及成功回执不被取消改写 |
| S08 | Host `internal/session/multimodal.go` | 原附件入口支持PNG/JPEG/WebP/GIF，10MiB每附件、10附件每消息；图像bytes由本轮内容归属。MP4作为file仅携带说明，不是已经接通视频参考API |
| S09 | Host `internal/imagegen/seedream.go` | 既有图片provider是同步images/generations，固定Seedream且显式size/watermark；这些请求字段不能复用为Seedance默认参数 |
| S10 | Host `internal/imagegen/credential_darwin.go/.m` | 同一HostHome哈希作用域的com.yijie.ai.seedream；非交互读取，独立运营CLI才可请求系统授权；直接复用resolver即可，无第二套Key配置 |
| S11 | Host `internal/artifact/store.go`、`internal/session/artifacts.go` | 加密临时spool、原ACK；image20MiB/其它64MiB，每会话256MiB/全局1GiB/24h；进程重开清旧spool，当前ACK tombstone在内存，不能宣称天然跨重启可查询 |
| S12 | Host `internal/session/document_runtime.go` | get_artifact_status已独立于文档环境，要求当前合法根轮次；仅说明Artifact staged/committed等，不表示Seedance任务状态 |
| S13 | Desktop `src-tauri/src/chat/artifact.rs` | Native验证、下载、SQLCipher提交、pending ACK恢复、幂等已提交分支存在；应在这套事实链上对接视频回执，不能从MCP正文伪造commit |
| S14 | Desktop `artifact_video_native.rs`、`ChatArtifactVideo.vue` | video/mp4、64MiB、scoped本地协议、Range、预览授权、保存、释放；当前MP4检查有界多轨容器，WebKit解码，不是只能播放历史合成样本；封面非必需 |
| S15 | Desktop设计pattern 14 | 只保证已Native提交且未过期的内容重开；明确不承诺所有Host未提交spool跨重启补领。本方案不能偷偷改成无限自动恢复 |

关键路径：[MCP配置](../../../../yijie-agent-host/internal/codex/media_generation.go)、[Host准入](../../../../yijie-agent-host/internal/session/media_generation.go)、[供应商图片适配](../../../../yijie-agent-host/internal/imagegen/seedream.go)、[现有视频组件](../../../../yijie-desktop/src/components/chat/ChatArtifactVideo.vue)、[Native视频边界](../../../../yijie-desktop/src-tauri/src/chat/artifact_video_native.rs)。

## 3. 原生工具族与等待能力

| 工具族/能力 | 现状证据 | FEAT-173决定 |
|---|---|---|
| 原生handler/extension | FEAT-172旧image-generation扩展仍在固定Runtime，但产品已关闭 | 不扩成视频核心工具；不恢复旧图片入口 |
| MCP | `core/src/tools/handlers/mcp.rs`、`mcp_tool_call.rs` | 复用发现、原生权限/审批、生命周期与结果继续执行 |
| dynamic tools | Host仅动态注册时才产生外部工具，现BuiltinMedia配置拒绝并存旧producer | 不新增dynamic注册/回调协议 |
| hosted spec | 属于模型API服务端承接的工具声明，与当前Ark模型服务不是一回事 | 不将Seedance API假称hosted原生能力 |
| Code Mode exec/wait | `core/src/tools/code_mode/{execute_handler,wait_handler}.rs`；`code-mode/src/service.rs` | 复用正在执行cell的yield、wait与取消，不另建Agent等待机制 |
| MCP持久任务扩展 | 当前`rmcp-client/src/rmcp_client.rs:call_tool`只接收CallToolResult；审计调用链没有tasks/get/result/cancel接入 | 不能因rmcp依赖可能有类型就宣称已能管理方舟任务；只加业务MCP查询操作，不改Runtime |

还只读核对了当前Runtime bundled skills文件清单和相关patch：未发现已装配的Sora/视频生成系统入口；不因视频接入再禁用用户技能或另写供应商CLI指南。

原生metadata里的thread/turn是可信绑定入口，不能假定普通MCP含稳定call_id，也不能把Code Mode cell_id当供应商task ID或计费幂等键。

## 4. 专家链

已审计Skills中`linkfox-expert-aigc-videogen-sale`与`linkfox-expert-aigc-videogen-viral-replicate`角色及工具约束，以及Connectors的LinkFox目录/registry。专家目前沿既有generic MCP、资源资格与逐次审批，且有自己的模型、音频和时长限制。这些约束不应被内置Seedance默认值覆盖；本方案不修改专家资源、目录、授权或Broker执行。

Host持久`expertBinding`与Runtime原生工具配置双重排除内置能力，是必须保留的实际约束。单凭“有个视频专家名字”或工具报错不能改路由。

## 5. Fact / Assumption / Unknown / Conflict

- Fact：用户给定准确模型ID、同Key、参数默认、无专家兜底；已确认文生＋图片生。供应商默认异步/不可取消running，现有150s工具链与64MiB视频交付均有源码/官方依据。
- Proposed：两视频工具、既有bbolt中的最小归属记录、无默认DELETE/列表、分段等待以及有限恢复；仍需用户接受，不冒称实施已获批。
- Unknown：运营账号的Seedance资格/实际默认视频体积与编码、默认生成耗时、真实下载域是否覆盖官方样例；本次不通过付费或Keychain探测补证，纳入实现验收。
- Conflict：旧README/AGENTS的“当前实现”段落有早期骨架措辞，与当前活动源码不同；以当前源码和绑定制品定位能力，不将历史说明当缺能力证据。FEAT-172原03为迁移前事实，本次使用当前源码和09修复结果。
- Existing limitation：FEAT-172复审记有旧runtime-chat-models生成器来源漂移；本次未运行全量generate、未刷新旧锁掩盖。实现门禁应如实隔离旧基线问题与新增视频族检查。

## 修订2补充源码结论

- `codex-rs/config/src/mcp_types.rs`的tool_timeout_sec为可配置Duration；150s仅当前Host设置。`rmcp_client.rs`对tools/list的重试不能泛化成tools/call业务重试。
- `tools/handlers/mcp.rs: supports_parallel_tool_calls`会接受readOnlyHint=true，因此取结果工具必须保留readOnlyHint=false；hint不代替业务交付幂等。
- Host Store.Status/ACK都是当前代内存事实，启动清旧spool；Desktop recover_pending_acknowledgements只重发请求，无法在Host无entry时创造回执。Native begin_artifact_transfer不允许failed/cancelled恢复。故修订1的ACK/manifest恢复不是“直接复用”，现已删除。
- 现有专家切换已检查Idle/ActiveTurnID及binding revision，可复用而非另造preflight；恢复root仍须重新核验，不能继承旧root许可。

重点源码摘要见references/reaudit-source-evidence.json，修订理由见08。这里仍是只读审计结论，未执行产品测试。
