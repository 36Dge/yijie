# FEAT-171 本机 Codex 文档能力参照审计

日期：2026-11-09。状态：**只读工程审计完成；不代表易界实现完成、依赖选型获批或九格式验收通过。**

本轮核对本机桌面应用、可用工具、官方插件说明、托管依赖实物与选定的打包代码片段。没有修改参照应用、替换二进制、安装依赖、创建云端文档或调用付费模型。本文的文档写入 `contract-impact=none`；FEAT-171 后续产品实现的分类以本需求包为准。

## 1. 审计范围与证据层级

目标格式为 TXT、Markdown、HTML、CSV、JSON、DOCX、PPTX、XLSX、PDF。图片和视频不作为本需求交付格式；文档页面的内部 QA 截图仍属于文档校验材料。

| 事实 | 本轮观察 |
|---|---|
| 当前应用身份 | `com.openai.codex`，应用版本 `26.1103.41825`，build `25679`；本机 bundle 位于 `/Applications/ChatGPT.app`，不可仅根据目录显示名推断产品边界 |
| 托管依赖版本 | `load_workspace_dependencies` 实际返回 `26.1104.22356` |
| 依赖根 | `/Users/jack/.cache/codex-runtimes/codex-primary-runtime/dependencies/` |
| 官方能力包 | 本机已安装 Documents、Presentations、Spreadsheets、PDF，版本均为 `26.1104.22356` |
| Node 文档库 | `@oai/artifact-tool 2.8.129`，提供文件导入导出及 Artifact Session 入口 |
| 专用 Python | `3.12.14`，与前序杭州任务使用的系统/Homebrew Python 环境不同 |

证据分为三层：**Fact** 为本轮文件、包元数据或工具返回可以确认的事实；**Inference** 为从接线与说明推导出的工程含义；**Not run / Unknown** 为尚未执行或公开/本机证据不足的部分。机器摘要见 [codex-reference.json](references/codex-reference.json)。本机绝对路径是审计定位信息，不是易界将来运行时的固定路径。

## 2. 实际分层与普通对话接入

**Fact：参照产品不是仅在 Rust Codex 二进制里实现九种文档生成器。** 当前本机能力由以下部分共同装配：

| 层 | 参照实现 | 易界应借鉴的职责 |
|---|---|---|
| 原生执行 | Codex 文件修改、命令执行、工具编排、审批与 `view_image` | 必须复用 `yijie-codex`，不在 Host 另建 planner、执行循环或审批事实 |
| 任务方法 | 官方能力包中的技能说明、脚本、模板与 API 文档 | 随应用提供普通对话可用的方法和接口说明；不能依赖用户选择/安装现有市场专家、技能或连接器 |
| 专用环境 | 应用管理的 Python、Node、库、LibreOffice、Poppler 及版本化安装/缓存 | 普通文档任务使用可定位、可校验的专用环境，不默认系统解释器、系统 Office 或开发机缓存 |
| 文件/文档会话 | 本地文件、Artifact Tool、Artifact Session，演示文稿可连接 Spaces | 统一原件身份、修改版本与预览来源；云端目标不得成为易界本地普通对话的隐含前置 |
| 用户查看器 | DOCX、PDF、表格、演示文稿、HTML 与文本视图 | 复用易界既有产物与侧栏入口，补足与生成版本一致的正文预览和回读 |
| 视觉校验 | 渲染页面图片后检查，必要时修正并重渲染 | 结构校验与视觉校验分开；内部 QA 图片交给原生 `view_image` |

**Inference：**用户在普通对话中直接要求生成文件时，方法、执行环境和查看器的协作才形成“开箱即用”。仅增加扩展名/MIME 准入或展示一个下载链接不足以达到同等标准。

用户明确“不依赖易界现有专家、技能、连接器”，应在 FEAT-171 落成可测试的产品约束：市场零安装、全部停用、未选专家、无连接器授权时，九格式仍可生成、解析、预览和保存。平台内部随应用装配的方法资源不应被伪装成对用户市场安装状态的依赖。

## 3. 逐格式生成、解析与预览

| 格式 | 已确认生成路径 | 解析和用户预览 | 校验注意点 |
|---|---|---|---|
| TXT | 原生通用写文件工具、标准字符串处理 | 文本读取/查看 | UTF-8、换行、空文件与长文本范围 |
| Markdown | 通用文本生成 | Markdown 渲染或源码视图 | 标题、列表、表格、代码、链接及资源解析 |
| HTML | 通用文件/代码生成 | 应用 HTML 渲染预览与源码视图 | 内容可读、脚本/资源边界；页面交互不等于授权业务操作 |
| CSV | 标准数据处理；表格任务可使用 Artifact Tool | CSV 解析、表格处理/查看 | 引号、换行、分隔符、中文、数字/日期与文本类型 |
| JSON | 标准 JSON 序列化和文件工具 | JSON 结构解析与文本查看 | 语法、类型、编码、输出与正文事实一致 |
| DOCX | 默认 Python `python-docx`；另有 JS `docx` | OOXML 结构读取；应用内 docxjs 解析/DOM 页面渲染 | LibreOffice→PDF→PNG，检查正文、分页、表格、图片、字体与裁切 |
| PPTX | 当前技能默认 Spaces＋Artifact Session；明确本地路由使用 Artifact Tool | `PresentationFile.importPptx/exportPptx` 与演示文稿模型/查看器 | 每页渲染与检查；文件导出与 live 文档修复不能脱节 |
| XLSX | 默认 Artifact Tool JS；已装 Python 库是补充而非默认路径 | `SpreadsheetFile.importXlsx/exportXlsx`，工作簿计算、检查、渲染与查看器 | 公式、缓存、错误值、单元格类型、图表、工作表和导出回读 |
| PDF | ReportLab，或从现有文档转换 | pypdf/pdfplumber 读取；应用内 PDF.js 查看器 | Poppler 渲染；扫描页、可提取文字和可编辑表单须分别判定 |

前五类并非五个独立“专用生成服务”；同样，DOCX/PPTX/XLSX/PDF 并不是模型直接输出二进制即告完成。它们使用通用执行器加格式库/转换器，再进入文件或文档会话链。

### 已安装不等于默认使用

本机包元数据确认：

- Python：`python-docx 1.2.0`、`python-pptx 1.0.2`、`openpyxl 3.1.5`、`xlsxwriter 3.2.9`、`reportlab 4.4.9`、`pypdf 6.10.0`、`pdfplumber 0.11.9`、`pdf2image 1.17.0`。
- Node：`@oai/artifact-tool 2.8.129`、`docx 9.6.1`、`pptxgenjs 4.0.1`、`pdf-lib 1.17.1`、`pdfjs-dist 5.6.205`。
- LibreOffice 与 Poppler 位于同一个托管依赖树，入口脚本解析到包内程序。此事实不表示易界可以直接复制这些本机二进制。

当前电子表格技能明确默认 Artifact Tool，非默认 openpyxl/xlsxwriter；演示文稿技能默认 Spaces 会话。不能仅凭安装清单推断每次任务实际使用哪套库。

## 4. 两条预览链必须区分

### 4.1 用户预览

从应用包选定代码可确认：DOCX preview 调用 `parseAsync`、`renderDocument`，使用 docxjs 渲染模块；PDF 使用 PDF.js worker；Artifact Session 有独立查看器接线。用户在界面中阅读已有文件不应被替换成一次新的模型请求。

### 4.2 模型视觉 QA

官方 DOCX 方法要求渲染全部页面 PNG 并检查；PPTX 方法要求逐页渲染并检查。QA 图片是派生视图，不是新的用户交付原件。生成器成功退出、ZIP/XML 解析成功或文件大小非零，只证明相应机械步骤成功，不能替代排版检查。

易界的图片读取必须复用已有 `ViewImageHandler`，来源为 `yijie-codex/codex-rs/core/src/tools/handlers/view_image.rs:84`。该实现保留模型图片输入资格检查，沿原生文件系统/沙箱读取，并通过原生 item 和图片内容返回。不要在 Host/Desktop 新增另一套“模型看图”实现，也不能绕过模型能力和原生权限。

DOCX/PPTX/PDF 等转页面图片仍是文档渲染器的职责；`view_image` 不承担 Office 转换。该 QA 使用不扩大本需求到图片/视频创作产品。

## 5. 精确定位与可追溯性

以下插件路径以 `P=/Users/jack/.codex/plugins/cache/openai-primary-runtime` 为根；版本只代表本次参照快照。

| ID | 源文件/位置 | 支撑事实 |
|---|---|---|
| C01 | `P/documents/26.1104.22356/skills/documents/SKILL.md:31` | 专用 runtime 路径优先，禁止默认使用系统解释器/仓库依赖 |
| C02 | 同目录 `tasks/create_edit.md:3` | DOCX 默认 python-docx |
| C03 | 同目录 `SKILL.md:74` | render→逐页检查→迭代，默认只交付目标文件 |
| C04 | 同目录 `render_docx.py:45` | 解析包内 LibreOffice；缺失时明确失败 |
| C05 | 同文件 `:16`、`:21`、`:257`、`:403` | pdf2image、macOS 临时目录处理、PDF 转换和页面渲染 |
| C06 | `P/spreadsheets/26.1104.22356/skills/spreadsheets/SKILL.md:16` | Artifact Tool 和专用运行环境约束 |
| C07 | `P/presentations/26.1104.22356/skills/presentations/SKILL.md:14`、`:33` | 目的地路由、创建与连接会话分离 |
| C08 | 同目录 `references/artifact_sessions.md:5`、`:67`、`:73` | 稳定 artifactRef、渲染和同一文档内修复 |
| C09 | `P/pdf/26.1104.22356/skills/pdf/SKILL.md:25`、`:88` | PDF 生成、解析和渲染依赖 |
| C10 | `yijie-codex/codex-rs/core/src/tools/handlers/view_image.rs:84`、`:179` | 原生图片读取与模型图片返回 |

本机应用包内代码位于 `/Applications/ChatGPT.app/Contents/Resources/app.asar`。其 entry 的摘要与检出的标识见机器证据。它们是打包 JS，没有可用的原始源文件行号；不得编造行号或把解包路径写成已经存在的本地文件。

公开产品边界的辅助来源（前序已打开核对）：

- [Work with files](https://learn.chatgpt.com/docs/artifacts-viewer)：桌面预览与 CLI 文件生成能力分属不同使用表面。
- [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins)：技能、MCP 工具与可选 UI 的职责。

这些公开页面支持架构边界，不足以证明内部组件许可证或与易界的二进制兼容性。

## 6. 参照不等于复制

1. **可直接复用的项目能力**：`yijie-codex` 已有执行、审批、工具发现、文件操作和 `view_image`；易界已有产物登记/原件提交/ACK/预览入口。是否需要适配由本需求工程审计逐项说明。
2. **应参照的装配模式**：版本化依赖、显式运行路径、内置方法资源、原件与预览一致、结构与视觉双校验、正常失败反馈。
3. **不能默认复制的材料**：本机 Codex app.asar、已签名应用、私有 Artifact Tool/会话服务及缓存内依赖二进制。当前四个技能插件 manifest 的 MIT 声明不能外推为整个应用或完整依赖树的许可。
4. `@oai/artifact-tool/package.json` 本次没有 `license` 字段，依赖包含 `@oai/walnut`。因此直接把它选为易界分发依赖的资格为 **Unknown**，不能写成“已有可分发依赖”。应逐组件核实许可、公开获取渠道、平台支持、字体授权、来源固定和可复现构建。
5. 不能把参照产品的 Spaces/Google/SharePoint 目标接入变成易界本地普通对话的新账号或连接器依赖。工程应交付等价的文档结果与阅读体验，外部云目标不属于本轮用户要求。

## 7. 必须补入需求的差异与未验事项

| 事项 | 判定与影响 |
|---|---|
| Windows 参照限制 | `render_docx.py:62`、`:76` 明确 Windows 使用系统安装的 LibreOffice；不能凭本机 macOS 审计宣称跨平台专用环境已解决。易界必须明确支持平台及其独立装配验收 |
| 干净用户环境 | 必须在没有系统 Python/Node/Office、没有专家/技能安装和旧缓存的条件下验证；现有开发机/Codex 缓存不能冒充易界开箱即用证据 |
| 依赖就绪 | 必须区分安装/准备中、可用、损坏/不兼容、空间不足等正常状态；不将下载成功当作所有格式可执行；用户不应手动 pip/npm 安装 |
| 版本一致 | 原件、模型解析、用户预览和 QA 派生文件均绑定相同产物版本；重试、修改、重开不得显示旧预览或重复成功 |
| Office 质量 | 基本正文/表格预览与完整分页、主题、图表、公式结果不等价；需按格式声明支持边界和可验的参照结果 |
| HTML 与公式 | 文档内容/脚本/外链不是操作授权；生成、解析、预览须沿原有权限边界，不能通过文档内容发起业务动作 |
| 视觉 QA | 文本/数值正确与视觉排版正确分别留证；模型不具备图片输入或渲染未完成时不可伪称视觉检查通过 |
| 运行与恢复 | 正常取消、部分成功、保存失败、缺依赖、重开和回退应保留原件与真实状态；所有停机使用正常收尾，不做用户禁止的强杀或攻击注入 |
| 本轮未执行 | 新装/升级/回退、逐格式新建/导入/修改/保存、真实模型路由、完整 GUI/视觉验收均未运行；前序库可加载证据不替代这些验收 |

上述差异是 FEAT-171 设计与验收输入，不是已获授权的产品修改、发布或付费模型测试。具体 Must AC、实现责任与批准状态由需求主文档、`feature.yaml` 和验证台账统一记录。
