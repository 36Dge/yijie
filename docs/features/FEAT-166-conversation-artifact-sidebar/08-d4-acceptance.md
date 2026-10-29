# FEAT-166 D4 本地验收报告

2026-10-29：**Local Demo Usable，10 项 Must AC 通过。** 结论来自修复后的同一次 canonical App 运行，包含真实 Host/Runtime/publisher、原生已发送附件读取、Native 文件展示与正常退出。此前锁屏和失败候选是历史记录，不用于替代本轮通过证据。D4 仅适用于 `demo_fast / local`，不是公开发布或生产验收。

## 1. 候选与真实入口

- 在 `yijie-desktop` 执行 `YIJIE_KIMI_K31_CALL_SURFACES=media ./scripts/run-local-demo-fast.sh --packaged --kimi-k31-pro`，由标准脚本构建并启动；沿用既有 FEAT-164 canonical profile 和 App 名称。
- 本轮 App PID **92234**；UI 验证从 **11:02:32** 持续至正常退出，**11:27:06 +08:00** 日志确认 `normal app cleanup complete`，launcher 退出码 0，相关 App/Host/publisher 进程退出。没有强杀或替换运行时。
- App 免登录进入正式业务首页；使用项目 `fixtures-20261028` 内现有隔离会话。普通会话 F：`01a18359-3f62-7a70-888b-aaaf9126c9a3`；代表失败及旧媒体会话 B：`01a182a7-c027-7600-b692-a7f808cc0112`。
- 回执中 **1,257 个源文件**与最终候选一致；可执行文件 SHA-256：`e3dffa403dd37634dfccce88eb6112b793451b9a73a8583365a8c7cb225aa2b6`。详见 [最终来源与正常退出](references/d4-final-source.json)。构建产物是标准可复现本地候选，未签名、未发布。

## 2. 本轮 Must 结果

| AC / 场景 | 实际结果 | 证据层级 |
|---|---|---|
| AC-001 默认关闭、双入口、空态 | 新进历史会话关闭，无分隔线；按钮展开空态。新产物到达时不自动开栏；换会话与返回仍关闭。 | 本轮真实 UI、运行中产物到达 |
| AC-002 HTML 与原 NSD | 两种来源 HTML 显示 inline render、脚本生成 record/42，业务按钮 disabled；原 NSD 显示标题、统计和 8 条动态记录。 | 真实消息绑定/产物卡片→同一 Native 阅读器；原件另见第 3 节 |
| AC-003 媒体排除 | PNG/JPEG/WebP/SVG（含大写 `.SVG`）仍打开原图片查看器，MP4 保持原播放器；展开/关闭右栏均不被改变。已有已发送媒体保持容器行为。 | 真实媒体 UI；通用分类与已发送附件兼容另有 focused 检查 |
| AC-004 标签归属、去重、容量 | 两个空页分别按激活空优先、剩余空页填入；同名 DOCX 输入/产物形成两个标签；重复同身份不新增；10 页后新文件被容量提示阻止，已有文件仍可激活。 | 真实 UI + 全分支领域检查 |
| AC-005 关闭、焦点、位置 | 方向键移动焦点不激活；Delete 关闭非激活页后回当前页，关闭激活页选右邻；末页关闭保持空右栏。PPTX 第 2 页、PDF 第 2 页/150%、XLSX Details 跨切换或收起恢复。换会话清空。 | 真实键盘、控件值、正文及状态检查 |
| AC-006 正文阅读 | 来源×格式矩阵全部支持项显示实际正文/页面；大 DOCX 分段、XLSX 跨行列/工作表、PPTX 第 10 页顺序、PDF 扫描页均可读。 | 第 4 节逐类实际内容，不用信息卡计成功 |
| AC-007 宽度与拖动 | 实际鼠标 616→516；键盘 Right=500、Shift+Left=564、Home=400、End=627、Enter=616。最小窗展开左导航 W940→右539，收起左导航 W1108→右664；复位后按比例重新计算。 | 真实物理拖动/键盘与截图尺寸；全部公式边界另有纯值检查 |
| AC-008 失败与恢复 | B 中合法但缺页面关系的旧最小 PPTX 显示不支持，不提供无效原地重试；切换 PDF 正常恢复，未困住对话。 | 真实普通失败；完整性/忙/超时/拒绝等用正常状态映射与源审查，不注入故障 |
| AC-009 复用与生命周期 | 第 2 次任务实际执行既有 `yijie_artifacts / publish_artifact` 3 次，客户端出现 3 个已就绪产物。标签跨正常 context 续接和前后台保留，内容重新授权；正常退出清理完成。 | 真实工具记录/Native 卡片/生命周期 + schema/SQLCipher/并发定向检查 |
| AC-010 布局与对话回归 | 1180×760 亮暗主题、10 标签溢出和中文长名可用；200% 自动收起且保留输入焦点与草稿，回 100% 不擅自展开。真实任务运行中可拖动，停止生成入口可达；生成完成后原标签与手动宽度保留。 | 真实 UI、58 秒任务与 focused 回归 |

实际截图由本聊天的 CUA 工具直接采集、逐张检查；归档保留下面的脱敏文字观察和源摘要，不将原 NSD 页面中的演示手机号等内容复制到仓库。[逐项观察摘要](references/d4-live-observations.json)记录验证层级。此结论是 Codex 执行与自审，不冒充 Owner 独立人工验收。

## 3. 原 NSD 与模型调用边界

原件 `01 NSD服务可视化管理后台.html`：**85,749 B**，SHA-256 `0d6ae31aacf66cae2c9caf255ae083fe092bb147ff929701d835c084862273de`。本机普通文件登记进入 publisher→spool→Native 提交/ACK→已就绪产物卡片→新右栏，显示 `NSD 服务`、概览及脚本生成的 `共 8 条` 检测记录，实际滚动可以阅读记录表。搜索、筛选、导出和页内分页控件为禁用状态；新增右栏只有标签管理、阅读控件，没有文件编辑/保存等操作。

这是**原件的真实生成产物链验证**，不是同名静态替代，也不是“原 NSD 已发送附件”验证。原 NSD 没有作为模型附件或正文发送；模型仅收到已授权的本地登记路径。HTML 的普通合成样本另外覆盖了已发送附件读取链。原件源摘要复核不变。

用户授权上限 2 次，实际 **2/2**，不再有剩余额度。第 1 次 FEAT166_A：9 个合成输入，12 个登记/已就绪产物；第 2 次 FEAT166_B：3 个合成输入，3 次登记/3 个已就绪产物，58 秒正常完成。输入、时点和结果见 [调用账本](references/live-validation-calls.json)。没有借用其他需求额度。

## 4. 来源×格式的实际内容

以下文件都以真实会话绑定或已提交产物打开；不是本地路径直读或 seed UI/数据库。F 的第 3 轮包含第一组输入/产物；第 4 轮是本次 fresh run 新提交。身份定位采用真实会话、轮次、来源和文件名；UI 脱敏工具记录不公开底层 UUID，不伪造 UUID。源字节摘要见 [第一组样本](references/live-samples.json)和[本轮新样本](references/fresh-samples.json)。

| 文件/格式 | 已发送附件实际结果 | 已提交生成产物实际结果 |
|---|---|---|
| `rendered.html` | 标题 Inline Render、脚本行 Rendered record / 42；业务按钮 disabled | 同样实际内容；不同来源独立标签 |
| `fresh.html`（第 4 轮） | 新绑定直接显示 fresh body / Normal final-run artifact | 新 publisher 卡片显示同一实际正文 |
| `normal.txt` | ordinary text body | 同一正文 |
| `normal.md` | Markdown 标题与 Local reading body；沿用已有文本投影 | 同一投影 |
| `normal.csv` | alpha=12、beta=34 的真实表格 | 同一真实表格 |
| `normal.json` | title=FEAT-166 normal JSON、count=42 | 同一 JSON 正文 |
| `compact.docx` | 标题、正文、两项列表、North/South 数字表格、内嵌图 | 同样正文、表格与实际图片 |
| `reading.pptx` | 第 1 页文本/表格；12 页中的第 10 页正确；第 2 页三色图 | 第 1 页文本与表格；Native 同一阅读路径 |
| `reading.xlsx` | A1:C2 合并、Shared string、123、25.00%、2026-10-29、缓存公式 3、无缓存公式明确提示；BA6、Row101 和 Details 均可达 | 首段同样的实际单元格与公式缓存语义 |
| `reading.pdf` | 第 1 页标题、文字与表格；第 2 页三色图；150% 可用 | 第 1 页相同实际图形页面 |
| `scanned.pdf` | 不扩大原输入准入，本次不作为已发送输入 | 图片页真实显示；不以缺少可提取文本降级为空白卡片 |
| `reading.docx`（2,182,060 B） | 大文档容量以产物代表样本测试；DOCX 输入另见 compact | 初段及下一段 Paragraph 0254 可读，上一段可达 |

媒体实际覆盖：B 的 PNG/JPEG/JPG/SVG 和 MP4、F 新产物 WebP/大写 SVG 在右栏开关两态保持原查看器/播放器；PNG 弹层在原生 PDF 上、WebP 弹层在原生 HTML 上均完整显示，关闭后恢复原标签和宽度。已发送 PNG/MP4/SVG/WebP 的旧容器行为实际检查；JPEG 输入共用同一排除分支，覆盖源审查与组件测试，未冒称逐一发送全部媒体后缀。

## 5. 本轮修复与重验

1. 默认原生按钮外观不符合 token：修正按钮 appearance、边框、背景，真实亮暗复验。
2. 300 秒 Native operation context 正常续接误清空标签：以会话/身份权限 scope 决定清空，短期 context 续接先释放内容，再用新 context 重新授权，保留同 scope 标签元信息。没有延长授权或略过校验。
3. XLSX 单元格过窄逐字换行：用有界列宽与横向阅读，真实普通表格复验。
4. Wry 新视图抢焦点：创建时不主动获取焦点，标签键盘行为保持。
5. Native PDF 覆盖图片弹层：识别现有 `aria-modal=true` 和 dialog，弹层期间隐藏 Native 视图，关闭恢复。修复后新鲜运行中 PNG/PDF、WebP/HTML 实测通过。

前一个候选 PID48890 因第 5 项未通过 D4，正常退出后才重建最终候选。没有用旧候选通过项拼接成新候选结论。[07 调试记录](07-live-validation.md)保留此前失败。部分 CUA 早期判断存在异步快照未完成、把末尾焦点说明重复计为标签、样本标题预期拼写不准确；最终使用实际渲染与行首控件计数复核，记录层修正不涉及产品绕过或伪造。

## 6. 检查、保护与明确边界

- 最终源定向测试：前端/同源 **34** 项、既有兼容 **9** 项、Native 正常文档/schema **7** 项、真实 SQLCipher 绑定读取 **1** 项通过，合计 **51** 项。见 [d4-focused-checks.json](references/d4-focused-checks.json)。未选中的历史测试不计通过。
- lint、生成一致性、candidate clippy、标准构建和设计文档构建的阶段性证据分别保存在 [实施检查](references/implementation-checks.json)、[修复检查](references/live-fix-checks.json)；最后 canonical 回执与当前源完全一致。最终治理检查另见 [d4-governance-checks.json](references/d4-governance-checks.json)。
- Runtime、Host、公共 Contracts 无改动；没有新依赖、plugin、主窗 CSP/capability 扩大、数据库迁移、模型工具或传输服务。新增的是复用现有链的 Desktop 私有展示适配。
- 元仓 11 个既有 FEAT-162 文件摘要保持；Desktop 变更限定本需求；未 commit/push/tag/发布、未迁移日常数据。最终 diff/status 已自审，源清单见 [d4-final-source.json](references/d4-final-source.json)。
- Office 是基本正文/页面的只读内容视图，复杂排版/对象不是全保真编辑器；PDF 非 OCR。保留既有格式准入子集与限额，不能把未支持格式冒称已支持。
- 未做攻击注入、危险归档、权限破坏、强杀、二进制伪装或故障制造；全量历史危险套件不运行。完整性/拒绝/资源忙/15 秒超时采用普通映射、正常异步和源审查层证据，不声称这些故障都在真实客户端触发。
- CUA 的拖动为完整手势，未单独物理演示“按住鼠标时 Esc/pointercancel/resize”；取消分支经源审查，正常拖动、端点、复位和 resize 实测。未做完整 VoiceOver 专项、长期内存/性能或生产安全专项；不把这些非核心专项写成已通过。
- 验证后系统恢复原浅色，窗口恢复 1268×780/100%，清除本次测试草稿，原首页草稿附件保留；App 通过自身 Quit 正常关闭。



最终治理首跑发现`paid_calls.approved_at`仍是日期，允许调用时schema要求完整ISO时点，因而D0/D4/claim及元仓两项声明测试失败。已使用调用账本已有的授权登记时点补齐并注明时间依据，未扩大授权或伪造用户点击时刻。失败保留于[首跑记录](references/d4-governance-first-pass.json)；重跑严格结构、D0、D4、claim均通过，元仓57/57通过。
