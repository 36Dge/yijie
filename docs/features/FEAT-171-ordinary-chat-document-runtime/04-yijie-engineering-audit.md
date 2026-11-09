# FEAT-171 易界现有工程审计与复用边界

审计日期：2026-11-09。本轮只读检查代码、配置与 Git 状态，没有修改业务代码、启动/停止应用、安装依赖、调用模型或执行测试。本文是需求设计依据，不是实现或验收通过证明。

本次文档写入 `contract-impact = none`：没有改变 wire、权限、运行环境、数据库、持久化或重放行为。部署/能力默认语义局部至少涉及semantic；本需求总体按00/05采用保守 **breaking** 规划，因为新增版本/持久化的reader方向兼容尚未证明。新增接口能否单独归为additive须有证据，不能用“JSON未变”降级。

## 1. 来源与现场

仓库位置按元仓 `repos.yaml`，均为兄弟独立仓。读取了 Runtime、Host、Desktop、Skills 的各自 `AGENTS.md`；Contracts 仅作源契约定位与状态读取，不修改其文件。

| 仓库 | HEAD | 分支 | 审计时工作树 |
|---|---|---|---|
| yijie-codex | `db3c7b56c390215803449b38fd7599ab4f5715f3` | `chore/retirement-baseline-20260905` | clean |
| yijie-agent-host | `b5a302dee53408299ff5835d51a3f3509ce4c682` | `feat/feat164-primary-20261028` | clean |
| yijie-desktop | `311bd1c54bdcaca85ae486e47fda97b698b64346` | `feat/feat164-primary-20261028` | clean |
| yijie-skills | `3698a970cf601afbb7fe1691e86d413df1481c09` | `feat/feat164-primary-20261028` | clean |
| yijie-contracts | `babc097206fb4edc772532d1d19e41597b6d6e50` | `feat/feat164-primary-20261028` | 已有 untracked `.local/`，未读取其业务内容、未清理 |

各仓 origin 均为 `https://github.com/36Dge/<仓库名>.git`；Runtime另有只读上游 `https://github.com/openai/codex.git`，upstream push 被禁用。源码固定上游仍为 `rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d`。不能把历史 README 的 Baseline 状态替代当前候选配置与源码事实。

下表路径从 CrossBSD 工作区起算，行号为本次 HEAD 下的定位点；不是授权清单。

## 2. 原生 Runtime 能力必须复用

| 能力 | 当前源码事实 | FEAT-171 处理 |
|---|---|---|
| shell / exec_command / write_stdin | `yijie-codex/codex-rs/core/src/tools/spec_plan.rs:628` 按模型和原生 feature 选择并注册；统一执行路径保留 sandbox 与 approval | 原生执行器负责调用托管解释器和生成/渲染脚本；Host 不新增通用命令执行引擎 |
| apply_patch | 同文件 `:735` 依据已有模型 metadata 注册 | 文本/脚本文件修改复用现有工具，不增加重复写文件工具 |
| Code Mode | `yijie-codex/codex-rs/code-mode-protocol/src/description.rs:12` 定义 V8 编排；`:17` 明确无 Node、文件系统和网络 | 编排原有工具；不能把它当成已安装 npm/Python/Office 的生成环境 |
| view_image | `.../core/src/tools/spec_plan.rs:750` 注册 `ViewImageHandler`；`.../handlers/view_image.rs:84` 检查模型图像输入，`:150` 使用原生文件沙箱，`:188` 由原生历史路径解码/缩放并发布 ImageView | 文档渲染后的页面图片由该工具交给模型检查；禁止另造模型看图工具。排除图片/视频产物开发不等于排除文档内图片和内部页面图 QA |
| 原生配置投影 | `yijie-agent-host/internal/codex/native_tools.go:64` 合成现有目录，`:87` 固定受管配置，再走原生 `-c` 参数 | 依赖定位与工具接入优先使用现有配置、MCP 和原生工具扩展点；不能因未暴露能力而修改 Runtime 核心 |

在 Runtime 的依赖清单、构建脚本和补丁中未找到 `python-docx`、`python-pptx`、`openpyxl`、ReportLab、LibreOffice 或 `load_workspace_dependencies` 的文档环境装配。该阴性检索不等于“Runtime不能生成文档”：它已有执行能力，但尚没有产品专用的生成依赖包。

## 3. 现有产物通道可以继续使用

现有路径为：模型经原生执行工具写入工作区文件 → `publish_artifact` → Host加密 spool与事件 → Native下载/校验/本地提交 → ACK → 原生预览/另存。

| 环节 | 事实与来源 | 重构约束 |
|---|---|---|
| 工具公开 | `yijie-agent-host/artifact-mcp/src/main.rs:56` 只有 `publish_artifact`，说明明确“先生成文件，再登记” | publisher不是生成器；为九格式提供应用自有工具资源包及生成依赖，不将登记成功冒充生成质量通过 |
| 注册配置 | `internal/codex/artifact_media.go:18` 注入 Host-owned `yijie_artifacts`；`session_protocol.go:606`、`:699` 分别在普通start/resume接入 | 无须要求用户选择市场连接器；保留内部MCP鉴权，不将“无连接器依赖”解释为禁止使用MCP协议 |
| 安全读取 | `internal/session/artifact_media.go:153` thread/turn来自内部元信息，`:162` 检查相对路径，`:169` rooted读取，`:176` 拒绝链接 | 不扩大到任意磁盘文件，不接受模型自报会话/租户/授权事实 |
| 格式接纳 | 同文件 `:259` 已识别TXT/MD/HTML/CSV/JSON/DOCX/PPTX/XLSX/PDF | 九格式名称本身不需要另造事件族；新增能力描述、版本、状态须另作契约评审 |
| 幂等/上限 | 同文件 `:199` 按session/turn/path及摘要去重；`:188` 单文件64 MiB；`:216` 每轮最多12项 | 明确多格式请求及QA中间物策略；页面PNG默认不登记为用户产物，避免消耗12项上限；修改后的文件版本不能复用旧摘要回执 |
| 生命周期 | `internal/artifact/store.go:28` 256 MiB/session、1 GiB/global、24h TTL；`:149` 打开spool会清理旧目录并重建进程密钥 | 现有 staged 不保证Host重启后恢复；不得宣称中间交付已持久。持久恢复增强须单独设计版本与兼容 |
| Native提交/ACK | `yijie-desktop/src-tauri/src/chat/artifact.rs:523` 下载后本地提交再ACK，`:604` 恢复待ACK；Host `store.go:263` 校验ACK摘要/大小与幂等 | 成功口径应绑定本地提交结果，不能只有模型文字或Host staged。保留既有提交和ACK链 |
| 保存 | `artifact_file_native.rs:582` 原生保存面板；`:1110` 校验原件，`:1158` sync，`:1168` rename | “对话产物已就绪”与“已保存到桌面”是两个结果。目标路径写权限、覆盖冲突、取消和失败必须独立表达 |

重要现状：`yijie-agent-host/internal/app/app.go:394` 的 ArtifactMedia 当前限定 `local + demo_fast`；`:911` 才注册v9/v12和publish路由。FEAT-171必须说明本地候选安装验收与公开/生产分发的区别，不能只启动开发开关就宣称所有安装用户可用。

## 4. 解析与预览不是空白能力，但保真和计算存在边界

| 格式 | 当前实现 | 相对目标需补齐 |
|---|---|---|
| TXT/Markdown/CSV/JSON | `yijie-desktop/src-tauri/src/chat/document_preview_content.rs:539` 走已有有界投影；MD在`:557`渲染，CSV在`:563`表格展示，JSON为校验后的文本；此处文本源有1 MiB限制 | 将编码、换行、CSV引号/多行、JSON结构以及截断提示列入正常样本验收；不丢原件 |
| HTML | 同文件 `:532` 保留HTML源码；`document_preview_native.rs:753` 限定导航；`:762` CSP阻断连接、外部框架、对象及表单 | 保留隔离和只读展示；明确支持的内联交互及资源范围。业务执行不能借HTML脚本跨入宿主 |
| DOCX | `document_preview_content.rs:599` 解析OOXML；`:609`将段落、表格及关系投影为HTML，分段阅读 | 不是Word全保真排版引擎；要定义与Codex参照样本可比较的基本版式、中文字体、分页、图片、表格支持范围，并增加独立页面渲染QA |
| PPTX | 同文件 `:632` 按presentation/slide关系读取基本内容 | 有页序和基本内容，不等于完整幻灯片布局引擎。不能以XML能打开代替布局/字体/溢出验收 |
| XLSX | 同文件 `:938` 明确“公式显示已保存结果，未重新计算”；分行列读取 | 生成阶段须有真实计算/缓存策略及一致性校验，预览不得将过期缓存当新结果；不支持公式应明示 |
| PDF | `document_preview_content.rs:581` 调用页面渲染；`document_preview_pdf.rs:175` 用Quartz绘制PDF页成PNG | 可复用当前macOS阅读器；PDF生成、文本提取、字体与页面质量检查另设能力。扫描PDF不自动等于OCR |

`src-tauri/Cargo.toml:39` 的 pdf-extract、`:40` 的Markdown、`:41` XML及`:58` ZIP依赖是当前解析基础。没有因此形成通用文档生成环境。应逐格式选择保留/适配/替换，避免整体推翻已验证的资源授权、历史文件和预览入口。

## 5. 现有专家脚本的价值与限制

`yijie-skills/plugins/yijie-desktop-skills/experts/moss-industry-research/versions/0.1.1/moss-workbench/` 中：

- `scripts/office.py:28`、`:60` 分别生成DOCX/PPTX，依赖Python标准库ZIP/XML；`:32`和`:61`直接写入行业研究语义、revision与内容摘要，属于特定报告模板。
- `scripts/artifacts.py:16` 已有XLSX写入器；主要能力为简单OOXML表格、样式和公式缓存，不是完整电子表格计算引擎。
- `scripts/delivery.py:69` 先校验冻结研究state，`:73` PDF要求显式正常soffice路径，`:100`调用外部转换；`:118`回执明确不替代视觉审核。
- `SKILL.md:12` 要求外部Python3.10+及PDF依赖；`:14`输出来自冻结研究内容。

这些代码可提供已验证的格式经验、普通样本和业务兼容测试，不能直接把专家安装目录作为普通聊天运行依赖。用户卸载/禁用全部Experts、Skills、Connectors后，九格式基础能力仍应存在。若抽取通用模块，必须剥离研究角色、数据结构、供应商与市场安装状态，并形成独立应用资源来源与版本。

## 6. 托管环境与安装现状

`yijie-desktop/scripts/feat164_primary.py:20` 白名单继承PATH；`:137`从当前环境构建配置。`scripts/development-client.py:93`增加Go路径及开发选择，没有文档依赖解析器或专用Python/Node选择。

现有 `docs/development-client.md:11` 的桌面入口会打开Docker并启动本地服务；`:13`说明它是指向源码目录的开发启动器。`scripts/run-local-demo-fast.sh:647`构建Host，`:652`构建artifact adapter；当前流程不是可据此认定的无开发工具用户安装包。

因此干净机器的开箱即用验收必须使用真正的应用候选与同源文档依赖包，而不能借用开发机Homebrew、Codex缓存、用户Python虚拟环境或已安装专家内容。基础文档工具、字体与转换器应由应用管理；模型请求仍遵循已有账号/供应商配置，不把“离线本地处理”写成离线大模型推理。

## 7. 推荐重构边界与契约路由

推荐参照Codex的分层装配，而不是复制其未获再分发确认的缓存/私有库：

1. **Desktop应用资源/部署层**：管理可复现、版本固定、校验和与许可清单完整的Python/Node/文档库/渲染器/字体资源包；提供健康状态与规范绝对路径。原子安装、升级和回退针对自有新版本目录，保留使用中的版本，不覆盖用户已签名程序或系统解释器。
2. **Host薄适配层**：向普通会话提供应用自有依赖查询、API文档/模板资源入口和有限结果回执；复用现有MCP与原生配置装配。避免重做规划器、技能匹配器、任意命令服务或第二套审批。
3. **Runtime执行层**：复用exec/apply_patch/Code Mode、原生sandbox/approval、turn取消及view_image。通过明确托管解释器路径运行生成代码；不能靠把系统PATH放前面“碰巧找到”依赖，也不应全局劫持用户其他命令。
4. **产物交付层**：复用publisher→spool→Native commit→ACK→保存机制；生产文件、QA派生物、最终原件应绑定同一内容revision/hash。生成、校验、登记、持久、预览、另存各阶段的事实不得混为一个成功状态。
5. **解析/预览层**：复用文件授权与九格式入口，按参照样本替换/补齐质量不足的格式适配器。用户界面预览与模型视觉QA分开；模型看图统一原生view_image。

契约权威：新增MCP工具及Host↔Desktop能力状态走 `yijie-contracts`；依赖manifest、健康与升级协议走实际部署权威并登记consumer；Desktop私有预览IPC/持久格式走本仓schema/migration。只有证实原生缺口后才考虑 `yijie-codex` 候选补丁；不预设Runtime升级。新增reader先就绪再发新值；不得破坏旧产物重开、原始文件字节及历史回执。

## 8. 建议进入需求验收的缺口

- 在清洁目标机器、无系统Python/Node/Office、无任何专家技能连接器安装的条件下，普通聊天完成九格式生成、结构校验、正确交付与预览。
- 普通中文/英文及混排字体、表格分页、标题层级、页码、长文档、PPT布局/图片/备注、XLSX公式/图表/数字日期格式、PDF页面与文本必须有明确基线；不使用“与Codex完全一致”作为不可判定AC。
- 同一产物经用户后续对话修改时，源文件、预览、导出、校验报告引用同一revision；不覆盖旧版本或显示旧缩略图。
- 用正常取消、无输入/正常不支持格式、自然依赖不可用的纯值状态测试及普通恢复验证错误分支；禁止强杀、权限破坏、攻击性归档与载荷，未执行的专项要记录原因和影响。
- 容量/并发/取消/部分成功/磁盘空间不足状态与首启准备界面需明确；成功生成不能被不必要的额外格式失败抹掉；未知外部操作不自动重放。
- 依赖包下载若采用首启安装，要明确网络、代理、离线完整包与用户等待体验；默认不要求用户执行终端或手工装pip/npm/Office。依赖资源可本地处理不等于已完成公开签名分发。

未执行：模型调用、真实普通聊天九格式fresh run、Office应用逐件打开、GUI/渲染质量检查、干净机器安装、升级/回退与生产发布资格。本文仅支持需求设计与源复用判断。
