# 工作区文件登记为聊天产物的修正方案与审计

2026-11-23。方案已接受并实施，适用入口是 `yijie_artifacts.publish_artifact`。本页保留设计阶段的审计，实测结果和验收边界见[实施与真实调用记录](05-workspace-artifact-publish-verification.md)。

## 建议改在哪里

由 Agent Host 的 `PublishArtifact` 决定最终文件名，MCP 工具让模型默认只填工作区相对路径。普通聊天、专家聊天和连接器生成后落在工作区的文件都使用这一入口。PNG、SVG、HTML、DOCX、PPTX 以及其他已支持类型共用一条命名规则。内置生图、生视频保留各自的直接交付流程。[Host 登记入口](../../../../yijie-agent-host/internal/session/artifact_media.go) · [现有文档和媒体能力](../../../../yijie-contracts/docs/document-runtime-v1.md)

百度二维码这轮的前三次调用分别指向实际存在的 PNG、HTML、SVG。三次都把含有 `https://` 的标题作为 `display_name`，触发入口处的斜杠检查。第四次重试还在文件名前多写了一层工作区目录。当前 HTTP 服务将登记逻辑返回的错误统一映射为 409，MCP 又将非成功状态统一翻译成检查工作区、格式和大小，模型据此无法判断该改哪个参数。[入口校验](../../../../yijie-agent-host/internal/session/feat134_projection.go) · [HTTP 错误](../../../../yijie-agent-host/internal/app/artifact_media.go) · [MCP 工具和反馈](../../../../yijie-agent-host/artifact-mcp/src/main.rs)

## 调用方式与命名

| 调用意图 | 建议的 `publish_artifact` 参数 |
| --- | --- |
| 使用二维码原文件名 | `{"relative_path":"baidu-qrcode.png"}` |
| 自定义可保存的中文名 | `{"relative_path":"baidu-qrcode.png","display_name":"百度二维码.png"}` |
| 登记子目录中的 Word 文档 | `{"relative_path":"exports/季度报告.docx"}` |

1. **文件来源。** Host 先核对活动会话和本轮授权，按原始 `relative_path` 在受管工作区内打开普通文件，沿用现有路径、符号链接、字节大小、格式、内容和接收端资格检查。目录中的 Unicode 拼写也按调用原样查找。文件名建议仅用于展示和另存，不能选取文件或指定 MIME。
2. **名称选择。** 对可选建议名去除首尾空白，按 Unicode NFC 规范化。合法中文、内部空格和原本可用的无后缀名称可以保留。省略名称，或名称含路径分隔符、控制字符、双引号、点目录名、超长文本时，取已核实文件路径的最后一段，再用同一规则检查。两个候选都不可用时，采用短基础名 `artifact` 和该文件类型的保存后缀。网址型标题整体放弃，查询参数不会被拼进回退文件名。源文件的字节、目录和磁盘名称保持原样。
3. **保存边界。** 最终显示名和 Native 建议的完整保存名均须在 255 个 UTF-8 字节内，计入补上的后缀。正常无后缀别名继续用于展示。实际类型始终由源文件扩展名及内容校验确定。当前 Native 已识别 JPEG 的两种后缀，文件另存函数却会把 `说明.htm` 变成 `说明.htm.html`。实施时在既有文件另存函数中，将同族别名 `.htm`、`.markdown` 的建议保存后缀换成 `.html`、`.md`，卡片继续显示原合法名字。用同一组样例验证 Host 的字节预算和 Native 的真实保存名。[Host 暂存名称检查](../../../../yijie-agent-host/internal/artifact/store.go) · [Native 事件名称检查](../../../../yijie-desktop/src-tauri/src/chat/artifact.rs) · [文件另存规则](../../../../yijie-desktop/src-tauri/src/chat/artifact_file_native.rs)
4. **重复登记。** 在创建产物 ID、占用本轮名额和发出开始事件前确定最终名称。开始和完成事件、暂存清单和幂等摘要使用同一个名字。保留现有的会话、轮次、原相对路径作为登记键。同键、同内容、同 MIME、同最终名称的重复及并发请求共用一个已成功登记的 ID。相同路径出现不同内容或不同有效别名时，沿用冲突语义。不同目录下的同名文件按各自路径登记。[登记键、摘要及回执](../../../../yijie-agent-host/internal/session/artifact_media.go)

## 工具契约和错误反馈

在 `yijie-contracts` 单独定义模型可见的登记输入，生成工具声明和适配器解码类型，并提供同源契约样例。`relative_path` 必填，`display_name` 是可选字符串。请求有体积上限，范围内包含斜杠的建议名可进入回退逻辑。工具说明以路径单参数为首例，保留旧双参数调用。沿用 Codex 原生 MCP 工具发现、调用和线程元数据。[现有媒体契约](../../../../yijie-contracts/jsonschema/artifact/media-v2.schema.json) · [契约生成器](../../../../yijie-contracts/scripts/generate-artifact-media.mjs) · [原生工具参数投影](../../../../yijie-codex/codex-rs/tools/src/responses_api.rs)

复用私有 `/internal/artifact-media/v1/publish`。新适配器向现有请求填齐两个字段。建议名省略、为空或超过私有字段上限时，传路径的最后一段。该段也无法装入字段时，传短默认候选名，保留可表示的短后缀。适配器只转换参数，文件读取、类型判断和最终命名归 Host。新输入和错误原因作为独立契约补充，沿现有生成和锁定流程同步。现有测试会逐字节比对两份历史媒体契约，旧适配器也会严格解码成功回执。[MCP 当前所读的 v1 定义](../../../../yijie-agent-host/artifact-mcp/src/main.rs) · [冻结基线用例](../../../../yijie-contracts/tests/document-runtime.test.mjs)

Host 在对应失败分支保留可判定的原因。建议在既有 400/409 响应上携带一个契约声明的可选原因头 `X-Yijie-Artifact-Reason`。旧适配器仍可读取原状态和响应体。新适配器只翻译列举的原因，以现有 MCP 错误结果向模型返回原因和可以采取的动作。正文、绝对路径、原始网址及系统异常不进入新增错误信息。

| 情况 | 给调用方的反馈和动作 |
| --- | --- |
| 当前已授权工作区内的相对路径不可用 | `workspace_file_unavailable` 对应“未能读取这个工作区文件，请核对相对路径。”只在本轮范围已确认后提供文件级反馈。 |
| 格式未接入、内容与类型不符、单文件超限 | 分别返回 `unsupported_type`、`invalid_content`、`file_too_large`。提示调整对应的内容或大小。 |
| DOCX、PPTX、Markdown 缺少当前会话的 v12 接收端 | `reader_unavailable` 对应“当前聊天暂时无法接收此类文档，原文件已保留。”恢复接收条件后按当前轮次权限交付。 |
| 同路径登记冲突、轮次失效、名额已满 | 分别提示既有登记、轮次或限额问题。对权限范围外的请求仅给一般的会话不可用信息。 |
| 原因未知或回执不确定 | 采用通用反馈。有产物 ID 时查询原 ID，不自动重新生成、改格式或重复发布。 |

成功沿用 `artifact_id` 和 `staged`，通过已有 `get_artifact_status` 获得 `committed` 后才报告聊天已接收。工具查看了一张图片、聊天已接收文件、用户已另存到磁盘，分别由各自操作确认。[交付状态契约](../../../../yijie-contracts/docs/document-runtime-v1.md)

## 方案审计与验收

| 审计发现 | 已纳入的修正与验收判据 |
| --- | --- |
| 模型看到的是 v1 输入定义，Rust 解码类型来自 v2，当前生成器产生必填字符串 | 单独生成新工具输入，直接验 `tools/list` 和 `tools/call`。只传路径、旧双字段、含网址的双字段都须能到达 Host，旧 HTTP 成功回执仍可严格解码。 |
| Host 入口按字符数检查，暂存按字节检查，Native 还要求 NFC、首尾无空白 | 用相同的普通命名样例核对三端。覆盖中文长度临界点、组合字符、日期斜杠、引号、无后缀名称与真实另存建议名。 |
| 幂等摘要目前包含原始显示名 | 原始网址标题、默认名以及显式传入相同有效名的三次调用，共用同一 ID 和一张卡片。另验不同内容冲突、并发重复和不同目录同名。 |
| 部分文档格式要求本会话已有 v12 订阅 | 在现代客户端分别登记真实 DOCX、PPTX 和 Markdown，验证提交、预览和原件另存。仅有旧接收端时验证可理解的原因。覆盖既有图片、HTML、PDF、XLSX 等格式和原有 MIME 分流。[格式协商](../../../../yijie-contracts/docs/feat165-artifact-files.md) |
| 错误发生在交付链的不同阶段 | 对正常缺失文件、普通不支持格式以及未知回执分别核对反馈。暂存或查看图片均不能被报告为已提交。只有确认未发生登记或已有可复用回执，才引导相应补救。 |

**本轮证据。** 对原会话四组实参做只读的命名与路径推演。前三组分别得到 `baidu-qrcode.png`、`baidu-qrcode.html`、`baidu-qrcode.svg`，第四组仍定位为工作区文件不可用。另用十组普通名称和三组后缀样例核对中文、空格、NFC、日期、字节边界、最终回退和建议保存名。用现行 v1、v2 schema 实测，两者均接受带网址的双参数请求，也均要求补齐名称才能转发路径单参数请求。

现有代码重新运行了 4 项 Host 测试与 4 项契约测试，全部通过。Host 测试读入既有 12 个扩展名样本和九格式文档样本，覆盖登记、内容读取、ACK、重复登记和新旧事件分流。[宿主多格式用例](../../../../yijie-agent-host/internal/session/feat165_files_test.go) · [九格式样本入口](../../../../yijie-agent-host/internal/session/document_runtime_test.go) · [新旧事件契约用例](../../../../yijie-contracts/tests/feat165-artifact-files.test.mjs)

**实施顺序。** 登记语义按 `contract-impact = semantic` 设计，原来会因显示名失败的请求可成功交付。契约与同源样例先行，随后接入能处理新旧请求的 Host，再启用新适配器。验证旧适配器可通过新 Host 登记原来的双参数请求，也验证新适配器遇到旧 Host 缺少原因头时仍能正确报告结果。使用现有服务配对，回退时先切回旧适配器。新版 MCP 到 Native 的全链路、历史重开和保存文件摘要对照列为实施验收。本轮证据限于设计审计与现有行为基线。
