# 工作区产物登记修复与真实调用验收

2026-11-23，易界本机日常开发版默认通过 v12 接收聊天产物，覆盖全部 17 个工作区扩展名。旧客户端仍可使用 v9 对应的 13 个扩展名。[日常 v12 逐文件回执](../../../../.local/audits/daily-artifact-v12-20261123-2ZRaqxoE/daily-v12-verification.json) · [方案与设计审计](04-workspace-artifact-publish-design-review.md)

## 日常入口统一使用 v12

日常构建自带 v12 产物读取能力。Desktop 在原有媒体 profile 中按构建能力订阅 v12，普通新任务和已有会话使用同一套选择逻辑。Host 保留 v9，是为了让只识别旧 MIME 集合的客户端继续接收其能处理的事件。日常用户无需选择协议版本。[Native 产物能力](../../../../yijie-desktop/src-tauri/src/chat/artifact_media.rs) · [订阅入口](../../../../yijie-desktop/src-tauri/src/chat/host_bridge.rs) · [兼容契约](../../../../yijie-contracts/docs/feat165-artifact-files.md)

本次 `contract-impact = semantic`，变更位于 Desktop 的默认订阅选择。按日常 Cargo 构建特性及启动标志，在独立临时工作区执行两轮真实 Runtime、MCP、Host 和 Native 调用，可选文档环境使用日常默认设置。两轮在实际 v12 事件中分别接收 9 和 8 个扩展名，17 个均由 Native 提交并收到 `committed`，重开数据库后另存的字节均与原件一致。旧 v9 的接收限制和显式文档模式的 v12 分别通过方向性复测。[日常文档与图片](../../../../.local/audits/daily-artifact-v12-20261123-2ZRaqxoE/daily-office/verification.json) · [日常数据文件与视频](../../../../.local/audits/daily-artifact-v12-20261123-2ZRaqxoE/daily-media/verification.json) · [旧版兼容](../../../../.local/audits/daily-artifact-v12-20261123-2ZRaqxoE/legacy-nine/verification.json)

固定日常入口已重建并重新打开易界，已在新建任务页核对就绪状态。运行中的应用二进制及两个订阅源文件的 SHA-256 与本轮启动回执一致，日常标志开启，可选文档环境保持默认。首次启动检查卡在只读 `gofmt` 的标准输入等待，经采样确认后对该工具一次正常中断，使用项目支持的 Node 24.22.3 重跑标准入口并通过全部启动检查。[当前日常运行回执](../../../../.local/audits/daily-artifact-v12-20261123-2ZRaqxoE/daily-client.json)

## 修复

- `publish_artifact` 默认只填 `relative_path`，兼容带 `display_name` 的已有调用。Rust 适配器依照独立的模型输入契约解码，向既有私有 HTTP 接口补齐文件名。[登记契约](../../../../yijie-contracts/jsonschema/artifact/workspace-publish-v1.schema.json) · [适配器](../../../../yijie-agent-host/artifact-mcp/src/main.rs)
- Host 依据经过授权的路径读文件。输入的名称含网址斜杠、控制字符、双引号或超出可保存长度时，取文件原名。有效中文名可以保留，首尾空白和 Unicode 组合字符统一处理。计算长度时计入保存扩展名。文件身份、暂存清单、开始及完成事件和重复登记校验都使用最终名称。路径错误、内容校验失败、超限、接收端不可用及冲突有各自的反馈。[宿主登记](../../../../yijie-agent-host/internal/session/artifact_media.go) · [名称选择](../../../../yijie-agent-host/internal/artifact/store.go) · [错误响应](../../../../yijie-agent-host/internal/app/artifact_media.go)
- 桌面端将 `.htm` 和 `.markdown` 的建议保存后缀规范化，避免双后缀。既有图片、视频和文件的无后缀名称在补上扩展名后超长时，使用可保存的短名称。[文件另存](../../../../yijie-desktop/src-tauri/src/chat/artifact_file_native.rs)

## 首轮五种格式的真实调用

使用原会话的三份二维码文件和两份正常 Office 样本。在独立测试工作区内，真实 Codex Runtime 调用新 MCP 适配器，Host 通过正式事件和资源接口交给桌面原生接收器。接收器使用产品的 SQLCipher 存储，成功提交后才发送 ACK。验证程序重新打开数据库，读取产物，通过对应的图片或文件原子保存函数另存，再与源文件逐字节和 SHA-256 比较。模型协议端只在本机给出工具指令，所有 ID 和交付状态均取自实际服务。供应商模型和二维码平台调用数均为 0。

| 源文件 | 字节数 | SHA-256 前 12 位 | v12 | v9 |
| --- | ---: | --- | --- | --- |
| baidu-qrcode.png | 2,311 | f33b3b4e6e7b | committed | committed |
| baidu-qrcode.svg | 3,833 | 4affa11a88a8 | committed | committed |
| baidu-qrcode.html | 4,096 | 620e37cc1622 | committed | committed |
| 示例.docx | 37,751 | 4fd70f845619 | committed | 当前聊天暂时无法接收此类文档 |
| 示例.pptx | 29,287 | 7bf7748609f8 | committed | 当前聊天暂时无法接收此类文档 |

两种接收端均实际执行了 7 次登记。第一次给 PNG 传入与原事故同型的带网址标题，第二次仅传相对路径，两次获得同一个 ID。其余四个文件分别只传相对路径。最后一次故意多写一层普通目录，收到“未能读取当前工作区中的文件，请核对相对路径”。成功暂存的文件均使用原 ID 查询状态，直至收到 `committed`。两种配置均只保存各自实际接收的文件。[v12 调用回执](../../../../.local/audits/workspace-artifact-publish-20261123-TN4vTL5M/final-v12/verification.json) · [v9 调用回执](../../../../.local/audits/workspace-artifact-publish-20261123-TN4vTL5M/final-v9/verification.json)

以另存的 Office 原件调用易界已校验的内置文档渲染器，并查看了全部页图。Word 的一页正文和表格、PowerPoint 的两页标题与项目均可见。[Word 页图](../../../../.local/audits/workspace-artifact-publish-20261123-TN4vTL5M/preview-docx/page-001.png) · [PPT 第一页](../../../../.local/audits/workspace-artifact-publish-20261123-TN4vTL5M/preview-pptx/page-001.png) · [PPT 第二页](../../../../.local/audits/workspace-artifact-publish-20261123-TN4vTL5M/preview-pptx/page-002.png)

## 全部工作区格式补验

每种扩展名都实际调用两次 `publish_artifact`。先传入含 `https://` 的显示名，再以同一相对路径省略显示名。对每个受支持文件，验收逐一匹配两次的产物 ID、`committed` 回执和桌面原生记录。重开 SQLCipher 数据库后，分别通过图片、文件或视频的原生保存实现导出，与工作区原件比较字节和 SHA-256。

| 产物 | 兼容 v9 | v12 | 另存后的复核 |
| --- | --- | --- | --- |
| Excel 工作簿 `.xlsx` | committed | committed | 内置文档工具读到 1 张工作表、8 个单元格 |
| JSON `.json` | committed | committed | 内置文档工具解析成功，638 字节 |
| 纯文本 `.txt`（`text/plain`） | committed | committed | 内置文档工具读取成功，200 字节 |
| MP4 视频 `.mp4` | committed | committed | 重开数据库后按两段读取全部 40,599 字节，并对导出的 3 秒 H.264 视频和 AAC 音轨完成解码 |

其余两端均通过的扩展名为 `.png`、`.svg`、`.jpg`、`.jpeg`、`.webp`、`.html`、`.htm`、`.csv`、`.pdf`。另有 `.docx`、`.pptx`、`.md`、`.markdown` 在 v12 全部通过。v9 对这四个扩展名的两次调用都明确提示当前聊天暂时无法接收此类文档。已对照 Host 的扩展名映射和两个接收端的 MIME 契约，v9 实际提交 11 种 MIME、13 个扩展名，v12 实际提交 14 种 MIME、17 个扩展名。[四组原始回执与逐文件摘要索引](../../../../.local/audits/workspace-artifact-formats-20261123-Zi9ReyLM/coverage.json) · [文档读取结果](../../../../.local/audits/workspace-artifact-formats-20261123-Zi9ReyLM/managed-file-inspection.json) · [视频解码结果](../../../../.local/audits/workspace-artifact-formats-20261123-Zi9ReyLM/mp4-decode.json)

前两次批量补验遇到测试版 SSE 的 100 毫秒空闲超时，登记回执停在 `staged`，两次均未计入通过。跨进程验收改用日常客户端的 30 秒空闲时限，随后在两个接收端各完整跑两组。本次补验只调整验收行为，`contract-impact = none`。测试使用固定本机协议驱动，供应商调用数为 0。

## 回归与验收范围

契约和双端生成物校验通过。历史 v1/v2 媒体契约、v9/v12 事件定义与改前基线逐字节相同。Host 定向 race 测试覆盖并发重复、不同有效名称冲突、缺失文件、旧接收端、12 个扩展名及九格式文档样本。真实适配器分别核对了新错误原因头与旧服务无原因头时的反馈。Rust 名称测试、Native 数据库重开与 Office 文件校验、Go vet 和适配器 Clippy 均通过。真实专家会话测试的搜索能力断言现按已解析的专家策略求值，保留原检查，二维码修复无需更改搜索策略。

复跑入口接收一个样本目录和一个新输出目录。每个选中的扩展名提供一个普通文件，默认格式为 PNG、SVG、HTML、DOCX、PPTX。默认使用日常构建及启动配置。下列两组覆盖全部扩展名，并符合单轮最多 12 个产物的登记限额。显式传入 `--reader 9` 可复验旧客户端兼容路径。[验收入口](../../../../yijie-desktop/tests/acceptance/workspace-publish/verify.py) · [Host 验收协调程序](../../../../yijie-agent-host/tests/integration/workspacepublish/main.go) · [Native 接收与重开校验](../../../../yijie-desktop/src-tauri/src/chat/workspace_publish_native_test.rs)

```sh
python3 -B tests/acceptance/workspace-publish/verify.py "$samples" "$output/data-video" --formats xlsx json txt mp4 csv pdf png svg
python3 -B tests/acceptance/workspace-publish/verify.py "$samples" "$output/images-documents" --formats jpg jpeg webp html htm docx pptx md markdown
```

上面的 v9 验收反映默认切换前的日常配置。当前日常入口使用本页「日常入口统一使用 v12」所述的接收策略。

Mac 在界面验收中途锁屏。图形界面的卡片点击和系统另存面板仍未复验，以上保存证据来自实际桌面原生接收及写入函数。普通测试使用已有文件、自然缺失路径与正常退出。攻击注入、破坏权限及强杀不属于本轮验证，依用户长期安全要求未执行，其结果不计入验收。本次交付范围为本机开发工作树。
