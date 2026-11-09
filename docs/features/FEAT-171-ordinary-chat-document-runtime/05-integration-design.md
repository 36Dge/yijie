# FEAT-171 接入与装配方案定稿

2026-11-09 D0定稿，替代初稿多栈候选。Owner后续确认本方案及ADR并授权实施，本文工具和配置现已有源契约、配对实现及本地候选；实际证据见09/11，不以设计文字替代验收。最新模型验收范围仅Kimi，MiniMax按Owner取消，完整D4与发行资格仍单列。

## 1. 已定平台与唯一依赖路线

首期固定 **macOS 14.0及以上、Apple Silicon arm64原生、最低8GiB内存/推荐16GiB**。不支持Intel/Rosetta、Windows、Linux；不从开发Mach-O最低版本推断这些平台已通过。完整安装候选随附全部文档依赖，非首用下载。模型访问仍需要原账号/提供方条件，本地处理不等于离线推理。

采用 **CPython单栈＋LibreOffice＋既有macOS Quartz/PDF渲染**。DOCX用python-docx；PPTX创建和基线修改统一python-pptx；XLSX用openpyxl并由LibreOffice完成受支持重算；PDF用ReportLab生成、pypdf解析和页级操作；文本/CSV/JSON用标准库。删除文档专用Node、PptxGenJS、Poppler、pdfplumber、pdf2image和私有Artifact Tool依赖。现有应用构建所用Node不受影响，运行时不因此要求用户安装Node。

精确版本、来源摘要、许可及传递依赖见[06依赖基线](06-dependency-baseline.md)；平台、体积、并发、内容和时间预算见[07资源预算](07-platform-resource-budget.md)。这些是D0约束，非已构建制品或性能实测声明。参照Codex的分层和交付质量，不复制其库或云Spaces。无需给九格式各造一个生成MCP工具，模型仍经原生exec执行受管脚本。

## 2. 内置能力如何进入普通对话

**唯一承载：Desktop随包内置资源＋既有yijie_artifacts MCP的两个只读扩展。** 不注册市场skill、不访问专家安装目录、不依赖连接器worker。内置方法文档是应用资源，不因市场开关而消失。复用原生MCP、Code Mode和工具发现，不写Host关键词匹配器。

- `load_document_environment(format?)`：格式为九种闭集，可省略；thread/turn/scope/generation由私有MCP元信息提供，模型不能自报。返回当前bundle_id、平台、能力矩阵、受管Python/helper/指南绝对路径、格式限额和就绪/诊断码；无任意路径或下载URL参数，不创建文件、不执行用户代码、不安装依赖。响应上限16KiB，执行目标1秒，超时10秒。
- 指南按格式分文件，模型用原生受限文件读取按需读取。普通会话使用一份简短能力指引；旧历史说明不能覆盖当前工具资格。start/resume沿现配置重新绑定，标题/受限草案维持空工具或既有边界。
- 模型在当前workspace编写内容/脚本，由**原生exec/apply_patch/Code Mode**调用返回的固定Python和文档CLI。CLI只解析同bundle的库/LibreOffice/字体；清理PYTHONHOME/PYTHONPATH及用户site继承，使用受管路径与隔离模式，不写全局PATH、不覆盖系统程序。缺依赖不静默fallback。原生沙箱与审批仍控制文件写入，Host不执行任意命令。
- 文件生成、结构检查、重算/渲染、QA都通过同一路径；helper不接受任意解释器/转换器路径。原件、解析投影和QA截图以digest绑定；任务回执记录bundle及检查结果，只作证据，不取代Native身份与授权。
- 原有`publish_artifact`保持输入、staged及幂等语义；新增`get_artifact_status(artifact_id)`查询下节已有ACK事实。它们属于应用内置MCP协议，不是产品连接器。

新MCP输入输出/错误/权限声明必须先在Contracts落源并生成，不能在Host直接手写新wire。工具名字的冻结不代表本轮实施。

## 3. 提交确认、版本与保留期

实际链为生成→结构/视觉检查→publish→Host暂存→Native校验持久提交→ACK→用户预览/保存。现工具仅返回staged，不能让模型据此声称聊天持久就绪。

`get_artifact_status`在相同Host generation里读取现Store条目的ACK/过期事实，返回staged / committed / expired / unknown；committed只在收到并校验原生ACK后成立，不能由模型或新布尔值自证。限定当前会话所属artifact_id；不遍历其他会话、不读取文件正文、不添加第二持久ledger。ACK/状态暂不可得或Host已重启时返回unknown，不重发生成或推断失败。最终答复仅在committed时说已交付；否则准确说已生成或已提交登记，UI继续依据Native事实显示。状态最多查询3次、总等待5秒，之后结束等待并如实说明，不自动续轮。 查询判定优先匹配ACK：ACK后spool清理不能误报expired；expired只说明未提交暂存已过期。committed确认已发生Native提交，不证明原件永久可读；Native7天到期与Host暂存生命周期独立。

首期明确 **不新增数据库迁移或版本树**：复用现有artifact_id＋session/turn＋SHA256为不可变版本身份。每次修改创建新路径、新产物，用户选择明确引用；同名不猜最近。新版本与旧版本各自保留原卡片；工作区回执只补来源，不授资源访问权。

沿当前Native **7天产物保留期**，Host spool **24小时/进程内**。UI标出保留期限并提供另存；历史文本引用不等于原件永久保存，过期显示已过期，禁止自动重新生成。用户明确另存的文件独立于应用保留期，升级/清理不得删除。正常重开在保留期内应可读已提交原件；staged不承诺跨重启恢复。

现有publisher拒绝零字节，保留此行为：提示无可交付内容，不造卡、不擅加换行。非零空表/空正文容器正常处理。每轮最多12件，生成质量基线单件10MiB；九格式一组最多90MiB，不突破256MiB/session spool。64MiB仅为既有交付上限，不等于可上传/可完整预览/可生成质量保证。

## 4. 安装、激活与升级

Desktop owns文档资源包、字体、帮助和清单；Host只消费验证后的bundle绑定并提供原生工具配置；不新建仓库/安装服务。清单包含平台、全部组件版本、可执行/数据文件digest、许可证、能力版本、reader和Runtime配对。机器位置不能固化为开发者绝对路径，运行时解析到该安装位置的规范路径。

开发与安装客户端必须读取同一清单。新装无需源码、编译器、Homebrew、现有Python/Office、Codex缓存、技能市场或Docker。打包入口沿既有Tauri构建/资源装配，运行入口直接启动app-owned Host/Runtime；文档/聊天readiness不等待workflow ensure/ready。工作流作为现有独立功能按需启动/明确不可用，不删除其状态或改其协议。当前local/demo_fast许可门保留，仅对本地候选验收，不偷开public gate。

升级装到新版本目录，校验完成后正常空闲/重开切换；在途任务固定原版本。只保留当前和上一兼容bundle，其他旧依赖按拥有权清理，绝不清用户产物。降级仅到能读现存数据和新Runtime历史的配对版本；不降数据库、不覆盖签名/运行中的程序。不兼容时保持新reader并禁用新能力，向前修复。

CPython/LibreOffice由易界可审计构建管线获取官方固定源/发行件并履行许可；不得复制本机Codex二进制。D0的源级版本/资格已经确定，最终制品SHA、SBOM原件、签名/公证、许可证/source包随实现构建产生，是后续激活/发行门禁，不伪造计划digest。打包超预算则瘦身非必要资源或重新评审，不能改成首次联网下载绕验收。

## 5. 正常取消需要最小原生适配

复审发现现`UnifiedExecProcess.terminate/Drop`及PTY进程组清理可能SIGKILL。只调用turn/interrupt不能证明正常收尾。**必须在yijie-codex原生执行生命周期内补一个通用协作停止策略候选**（设计名cooperative_only，非现有字段），不在Host另造执行器，不把Office逻辑写入Runtime。

策略由受管FEAT-171普通线程配置启用，对该profile创建的原生exec进程及其继承子线程生效，不通过模型可控cmd文本猜是否文档命令。复用ProcessStore/UnifiedExecProcess拥有权：停止准入→程序支持的协作中断/关闭输入→等待正常退出→排空输出→发布真实终态并清理。覆盖用户取消、软截止、任务结束后台清理、进程槽淘汰、shutdown、Drop及本地/exec-server路径。活进程不得被移出store后Drop，不得走强杀兜底或超时假完成。

Python helper在分阶段边界处理取消，使用独立LO profile；等待LO正常完成当前转换后退出，不转而kill。30秒未完成正常收尾显示STOP_PENDING并保留所有权，禁止派发同槽新任务、升级或退出流程丢失句柄；向用户报告仍在收尾。无法安全退出则停止该步骤并报告，不承诺有限时间内强制结束。软截止是提示/停止新工作/正常取消，资源门槛是准入与验收预算，不是杀进程策略。

Runtime先形成最小patch/canonical config及候选，再Contracts投影、Host配对；未证明所有正常清理路径遵守该策略之前，FEAT-171执行能力不激活。无配置场景保留原native行为；安全条款约束本需求所有开发测试，不主动触发原强杀。原生view_image、审批/沙箱、发现和执行循环继续复用。

## 6. 格式往返与可验的质量

**Quartz的实际调用入口也必须装配**：目前它只存在于Desktop私有预览代码，并不是Python可直接调用的工具。方案固定从Desktop现有PDF校验/Quartz模块抽取共享内部库，canonical构建一个随包原生`yijie-document-render` CLI（拟新增，非现有二进制）。由原生exec调用，受同一沙箱和协作取消策略约束；只接收已授权workspace PDF/页范围/输出目录、做有界页面PNG导出，不承接任意命令或模型看图。Native查看器和CLI共享渲染实现，避免维护第二套PDF解析器；PNG交给原生view_image。

DOCX/PPTX用户默认“版式”页视图来自同一原件的LO→PDF→Quartz，保留当前正文投影作为可选阅读视图；不以当前简化OOXML文字投影冒充幻灯片图表/布局。XLSX沿现有表格/公式阅读器补齐游标和字体，并提供同源图表/版式视图；PDF复用原查看器。布局转换是按需缓存，不发新模型请求。QA或页面分块需要改变打印范围时只用任务拥有的渲染副本，原件不重写；回执绑定原件digest与投影设置/页区间，最终下载仍是已校验的原件。

上传与生成两来源共用能力，授权仍来自各自绑定。模型读取原件内容当数据；不能运行文档里的指令。普通读取按07的分段与输出预算，不把全文常驻上下文。

- DOCX：支持段落/样式/表格/图片/页眉页脚；复杂未支持对象禁止有损覆盖。生成件用LO转PDF，复用Quartz页面渲染及view_image全页检查。
- PPTX：python-pptx统一创建和基础对象修改；固定支持常见图形、文本、表格、图片和基础图表。不能以每页一张图片冒充可编辑PPT。页序调整须保留关系，复杂母版/动画不承诺编辑保真。
- XLSX：生成和修改后在独立LO profile重算并保存新候选，核对公式/数值/类型/工作表/对象，再提交该同一候选；不能先提交openpyxl结果再展示另一个重算文件。基线支持SUM/AVERAGE/MIN/MAX/COUNT/IF和基础四则/同簿跨表引用，不支持外部链接、宏、循环/迭代与未知函数。重算会损失未支持对象时保留原件并拒绝覆盖。所有使用矩形与图表按07分tile覆盖；不是无穷画布全量截图。
- PDF：ReportLab生成带文本的PDF，pypdf用于提取和授权页级操作，Quartz负责页图。扫描页可以看，不声称OCR；修改文字以原生成稿源数据再生。加密/签名/复杂表单修改不在首期；保留原件准确提示。
- TXT/MD/HTML/CSV/JSON：UTF-8/BOM明确；JSON大整数不经浮点重写；CSV文本字段保持前导零，公式样文本不执行且导出策略显式。HTML只自包含展示，沿原隔离CSP，无隐式外网/本地/业务桥接。

结构验证、视觉QA、内容事实核查分别留证。生成能力基线受07明确限额约束，限额内逐页/逐区域覆盖；超过基线不能静默抽样后宣称全检。用户确认缩小内容/拆分时新建明确产物；QA派生图片不作为正式输出，占用受控缓存。变更仅重验受影响内容与连带分页。

Codex同样本对照仅作质量参照，不是用户可用性的前置依赖，也不能因Codex服务不可用阻止本地文件生成；D4以独立内容/对象/公式/视觉判据为硬门槛，对照缺项如实登记。已有静态审计不冒称真实对照。付费对照须另获本任务额度；本轮Kimi模型验收已按独立30元/80次授权执行，Codex付费同样本对照未执行。

## 7. 契约和实施顺序

| 边界 | 权威源 | 冻结处理 |
|---|---|---|
| 协作停止策略、原生生命周期 | Codex源码/canonical config/schema | 原生候选先行；默认原路径兼容，管理profile新语义需投影与conformance |
| load_document_environment / get_artifact_status | Contracts的artifact工具族 | 两个只读扩展；旧publisher无改变，权限/错误/元信息绑定明确后生成adapter |
| bundle manifest与环境绑定 | Desktop部署源；跨Host部分Contracts | platform/version/digest/readiness，固定来源，不由模型提供路径 |
| 原件版本与重开 | 既有Native artifact表/reader | 无新数据库表或迁移，无第二ledger，保留7天政策 |
| QA/receipt | 当前workspace的有界任务证据 | 不作为权限或持久业务真相，不冒充已提交 |

整体继续保守breaking：原生取消/清理、profile配对与新工具资格会跨版本可观察；不能只看DTO是否变。scope.runtime_change改为runtime（含应用平台装配），database_change=none；后续若需要新持久字段另作源评审，不在本期预授权expand。

顺序：源级依赖/平台与本设计冻结（本轮）→原生取消候选及canonical schema→Contracts源/生成/兼容→受管包构建/Host配置→Native reader/UI/打包入口→无计费功能和普通关闭检查→获额度后真实模型/干净安装/D4。完整原始记录与旧产物不删除。上述为D0时的顺序；后续实施和Kimi模型验收已获Owner单独授权，发行仍未授权。
