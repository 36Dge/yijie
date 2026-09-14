# 原生 Coze 页面采用易界主题

FEAT-153 local 产品追加，Owner：段成威。用户明确要求原生页面/组件的蓝紫配色改为易界“白、青柠、石墨”，本请求重新开启22中按用户决定延期的主题工作。本轮已完成真实packaged主题追加验收；26最终候选及25功能回归的差异和证据分别记录于下文，不继承22或原D4为本轮通过。

`contract-impact = none`：只修改独立Coze页面的视觉颜色、主题令牌映射及图标颜色资源，不改变HTTP/bridge消息、身份、会话、图语义/序列化、存储、运行、删除、重试及部署权限。Desktop活跃`src/styles/variables.css`为易界颜色来源，Coze以可追踪生成快照消费选定颜色，独立构建不复制第二套手工色值或导入Desktop exports。原Coze布局、组件及交互保留；无新依赖、Tauri权限、网络目标、数据库迁移或Git交付。

## 设计与场景

- 亮色页面、画布、顶栏、节点、侧栏、输入、浮层为纯白，以中性边框和留白区分。暗色按易界page/card/elevated石墨层级，普通文字分别用primary/body/secondary/tertiary。
- 主操作用品牌青柠#C3F35B，hover#D0F780，pressed#B1E343，文字/图标固定石墨#25282B。禁用使用中性禁用前景/底色，不能让青柠白字或低对比浅紫继续出现。
- 工具图标、普通链接、表达式变量文本与焦点均按中性可读角色；节点/端口/连线的明确选中使用青柠并保留可辨轮廓。错误、警告、成功等真实状态保留易界独立语义色，不能把删除刷成品牌主操作。
- 原生节点标题浅色渐变、硬码SVG/边色、点阵、文本编辑器浅底白字和节点灰字是本轮已知覆盖点。只增加可选颜色接口或原始资源颜色投影，无local主题时保持上游默认；不自绘第二套页面，不改变节点字段或布局。
- 主题由当前两端已有系统偏好监听切换。当前Desktop没有独立light/dark/system设置UI，Coze亦无可选主题入口；不为此增加新wire字段。CSS变量覆盖到iframe body，确保挂在body的Modal/Popover/Menu也继承主题。
- 空白/加载/错误/只读/禁用/hover/pressed/selected/focus及主题切换均保持原本行为。主题切换不重载iframe、不丢未保存内容；数据、权限与确认文案不变。

备选：仅把紫色替换青柠会造成青柠细字和浅底白字，不采用；直接改全Coze全局主题会扩大到未接入页面，不采用。选择嵌入文档作用域的易界令牌映射和少量原组件颜色接口。

## 必要验证

1. source lock/生成主题快照检查、限定类型与构建检查、与本轮修改匹配的普通检查；不跑用户禁止的强杀/权限/攻击测试。
2. 正常入口真实packaged验证完整画布、顶栏、节点、侧栏、表达式、工具栏、添加面板、试运行、名称弹窗与菜单；亮暗及1180×760/较大窗口无旧蓝紫常规装饰、浅底白字或关键遮挡。
3. 主操作、disabled、hover/focus、输入error恢复与主题切换草稿保留；真实合成编辑保存重开/试运行回归。关键前景/背景取实际CSS颜色核对，不将token理论对比度当作全页WCAG通过。
4. 截图所用既有流程只读；新建具名合成流程用于必要写验证。旧资源API/DB记录保留；不删除任何旧流程，不物理清理。
5. 本轮记录独立于原17统一D4/22功能收口；dev/全量无障碍/生产及未执行项如实单列。

启动前用户App PID3416已在到期编辑页，通过返回无未保存提示正常关闭，再Cmd+Q退出；`make workflow-stop`正常STOPPED，命名卷保留。`evidence/coze-theme-20260914/workspace-before.json`保存各仓来源、remote/status与Desktop颜色源摘要。

## 已实现的来源与适配

- `workflow-editor-theme.mjs`从Desktop活跃CSS提取44个颜色/焦点/投影令牌，生成亮暗两组CSS及source.json（Desktop完整HEAD、原CSS摘要、palette摘要、生成CSS摘要）。`--check`逐字核对，未改Desktop源或颜色规范。
- `yijie-coze-theme.css`覆盖嵌入document根与body上的Coze RGB原色、workflow语义别名及Semi颜色；body portals共用映射。组件颜色状态提高到足以覆盖原生brand/highlight/disabled/focus的选择器优先级。普通标签及插值为可读中性色，真实状态前景和实心状态按钮底色分开。
- 原生四张SVG只通过既有SVGR入口在本地renderer着色，原path/rect几何、URL、模板及持久化icon字段不改；没有filter反相。标题取消白底混色渐变，原表达式/建议浮层通过可选变量修复暗色背景；节点、端口、线条继续用原生renderer/API。
- lineColor经真实Flowgram SVG gradient stop消费CSS变量，未把CSS变量字符串传给CanvasRenderingContext2D。原生local flags和三节点限制继续保持；所有新增修改上游文件已在source lock登记。
- current Desktop实际只跟随系统，未实现独立三选项设置。进入本地editor时将专用presentation preference `yijie-workflow-native-theme`固定为system，避免Coze Provider优先读取陈旧本地偏好导致父子主题不同；不访问身份/凭据键，不增加wire消息或刷新iframe。

直接生产源静态结果：主题projection 44 tokens check/脚本语法通过，原生10份TS/TSX有限语法、7份LESS编译通过；source preservation为15243原文件保持、6既有删除、56登记overlay。此处的有限语法检查不代表全量TypeScript通过，标准build仍执行原配对类型检查。独立源码复核已修正四个确定优先级/语义问题，没有按检查数量冒称全主题资格。

`palette-contrast.json`仅计算源令牌对比度：亮色primary/白14.82、secondary/card7.40、tertiary/card4.65、青柠/on-brand11.50；暗色body/card12.17、secondary/card8.72、tertiary/card5.47。必要输入轮廓light3.11/dark3.04，暗色浮层轮廓4.76。实际层叠、禁用态与截图仍需另行观察。

小地图补充审计发现：原`createMinimapPlugin.canvasStyle`固定浅灰/白色，实际为Canvas绘制，不能靠CSS字符串变量着色。锁定的`@flowgram.ai/minimap-plugin@0.1.28`无公共颜色更新方法；反复init会叠加entity监听，不采用。选择具名、明确记录为版本固定私有结构的本地adapter，只更新6个颜色字段并调用原service.render，不修改node_modules、原Rush锁或重建文档。可见时观察主题属性并在rAF读取已解析CSS颜色，隐藏/卸载清理观察器及rAF。此适配属于上游私有接口使用例外，未来升级必须重新审阅；不能称为原生公开API或新的自绘小地图。

## 真实 App 首轮发现与修正

2026-09-14 canonical23通过标准build/check并正常激活；22/23同输入385个资产逐字节及摘要一致，配对类型检查无新增诊断（126项上游基线仍保留），原CSP和资产预算不变。真实packaged打开既有截图流程7685031373442121728，只读检查未修改图或名称；第一次亮暗切换保留同一面板/画布，小地图内容确已重绘。

此轮实际发现首次鼠标/触控板引导“知道了”及小图仍固定紫/绿，暗色文本字段正文/列标题仍过暗，小地图外层固定白底。因此canonical23不能记作主题PASS。正常返回列表并Cmd+Q退出PID17861，随后canonical workflow-stop返回STOPPED，保留全部卷后修正。节点菜单此入口使用系统原生菜单，仅观察后Escape取消，没有执行删除。原生编辑名称弹窗深色标题/输入/取消/确认角色已正确，取消退出未保存。

canonical24修正限定为原生两份鼠标模式LESS、列标题、实际CodeMirror renderer baseTheme叶子、小地图public panelStyles及节点缩略颜色。小地图保留同一原service和几何，节点细边原0.145px不变，填充使用易界tertiary提高可见性。正文旧黑色的最终层叠来源尚未证实，因此不能把源码推断写成根因已确认；对实际renderer .cm-content/.cm-line明确消费body文字令牌，插值消费primary，待真实App判定效果。菜单覆盖只作用于原生MenuItem的文字角色。4份TS语法、2份LESS编译、61项上游overlay source preservation通过，不代表全量类型或UI通过。

24对23的真实资产差异：385份中379份保持SHA，变化为2 CSS、3 JS和HTML；原生9484包4462模块中只有4个变化（表达式baseTheme、小地图panelStyles、nodeColor、ColumnTitles），main的639模块逐字节一致。仅扫描3个变化JS的8个敏感位点，均为原runtime及原有4个fetch，无新Worker/WASM/eval或出站目标。按实际差异更新原45文件CSP审核目录中的3个hash，原策略与预算未放宽；25再验证同源构建一致性。

## canonical25 真实功能与主题记录

标准packaged App PID26504，manifest `062565c6cfe993f1676a72b4a7e4249d228c628484d75c1ca8b00c440feee147`；44主题令牌检查和24/25全部385资产一致，类型无新增诊断。已正常创建 `7685061713409867776 / FEAT153 易界主题验收 0914`，使用原生添加节点、键盘端口建立Start→Text→End，自动布局后输入 `易界主题：{{input}}`。亮→暗切换保留未保存内容及打开的面板/小地图；暗色正文、列标题、Map内容与外框已清晰，保存成功。返回列表新流程置顶，重开同3节点2连线与正文。

真实窗口逻辑尺寸1180×760及1346×850（请求1440×850，由当前屏幕可用范围限制宽度）。名称Modal实际验证空白禁用、中文恢复可确认、focus及取消；普通 `{{inpt}}` 拼写错误显示原生错误，修正后提示消失并回到原已保存状态，未提交错误草稿。真实试运行 `7685063555988586496` 输入亮暗切换，输出易界主题：亮暗切换；已内部发布v0.0.1，在原生运行面板和Desktop历史读回同一结果。`saved-draft25.json`、`final-workflow25.json`及11项离线核对记录证明API/MySQL画布、内部版、两库归属与回执一致。原截图流程完整API两投影仍与before-ui一致。

一次点击仅触发输入blur的场合以新AX与实际状态核对再操作，未按点击次数冒称成功。UI自动化几次提示窗口状态变化，均先刷新当前AX再执行；原生视口可自由缩放，不把截图视口缩放当作持久节点位置。

最后一处错误说明由原生Feedback/ErrorMessage的`text-[#ff441e]`硬编码造成，已在正常退出App并STOPPED后，仅追加本地精确class映射到易界semantic-error-ink；无DOM/JS/验证变化，选择器复核通过。故25整体颜色资格尚不能包含此错误文字，26/27需单独复验。Desktop既有历史表单仍显示系统输入焦点色，不把它误称为Coze原紫色组件；本轮未改Desktop全局输入规范。

## 最终结论（2026-09-14）

**PASS：已接入的原生工作流页面采用易界主题。** 最终canonical26 manifest为`725750097a463c3dc3a323b04c8b22e3650bfdc27ace60453f1c93ce2d00810c`，source_digest为`236d36286e96b4f7ad7fe5bb874528c67505c0835020b238cfe21179263bb120`。标准build/check通过，385资产45,317,972字节；25→26的235份JavaScript逐字节一致，只有entry CSS追加一条错误色规则及HTML更新CSS引用，CSP审核目录、原策略、依赖锁与预算均未改。25已完成同源重复构建，本次单条CSS未扩大重复测试，因此未运行27。完整增量见`canonical26-css-incremental-review.json/.md`。

最终标准packaged App PID31492重新打开同一流程，验证亮暗×1180×760/1346×850的实际显示。正文、列标题、错误字/边/插值、焦点、主动作与禁用态、节点图标/端口/连线、小地图内容/外框均采用对应易界色。`{{inpt}}`普通拼写错误在亮色为深红、暗色为浅红，回改`{{input}}`后提示消失并回到“已保存”；没有将错误草稿提交到服务端。通过原生缩放菜单“自适应”整理最终视图，未改持久节点位置。最终浅色外观恢复，App保持真实原生画布打开，受控服务保持健康供用户查看。

- [最终浅色完整画布](evidence/coze-theme-20260914/light-canvas26-final.png)
- [浅色节点面板与小地图](evidence/coze-theme-20260914/light-panel26-small.png)
- [暗色节点面板与小地图](evidence/coze-theme-20260914/dark-panel26-large.png)
- [浅色错误提示](evidence/coze-theme-20260914/light-error26.png) / [暗色错误提示](evidence/coze-theme-20260914/dark-error26.png)
- `final-visible26.json`、`restored-valid26.json`、`window26-large.json`记录最终AX/真实尺寸；`activation-26.json`验证实际服务入口及全部资产等于manifest，公开资源和捕获AX中当前两种机器凭据匹配为0。此范围不等同完整堆检查。

正常App/栈重启后，`final-workflow25-26-comparison.json`中16项业务检查通过：名称/描述、revision、完整画布、内部版本、history/run和两库归属/执行/回执保持一致；唯一真实试运行仍为`亮暗切换 → 易界主题：亮暗切换`。新增8条审计均为正常bootstrap/read/history/read_run，未将读审计增长伪称全库不变。旧截图流程完整两投影响应仍与主题工作开始前一致（`screenshot-workflow-comparison-26.json`）。

本轮修改位于Coze原生组件可选颜色接口、本地主题生成/映射、对应source/CSP登记与元仓证据。Desktop活跃palette文件摘要保持原值，原生布局/图标几何/三节点白名单/身份和会话桥/存储/运行语义未改；既有未提交改动及六份Coze文档删除保留，未Git暂存、提交或推送。

限制与未执行项：本次资格覆盖当前已接入的三节点原生工作流与真实packaged入口，不覆盖Coze未接入业务、所有节点、全量dev或重新统一D4。未重做自然到期/首次打开取消的完整资格、整页WCAG/屏幕阅读器评估、完整浏览器堆检查或生产发布；源令牌对比度及只读截图色值统计不冒称全页面可访问性认证。禁止的强杀、权限破坏、攻击注入与危险fixture均未执行。当前采用的MiniMap版本固定私有适配例外仍需在未来升级时复审。

交付前最后一次只读窗口观察：App已从合成主题流程切换到`FEAT153 原生终验 0913`，并显示未保存修改及新的节点摆放；这些发生在本轮最终有效草稿/截图记录之后，不是本轮自动化发起的编辑。立即停止UI操作，未保存、撤销、重连、导航或关闭当前草稿，保留用户当前工作。上述旧流程“响应未变”结论仅指具名API快照的观测时点，不声称之后的用户编辑不存在。

文档收尾：元仓`pnpm lint`（仓库清单/Contract First治理）通过，两仓`git diff --check`和44令牌projection check通过；`workspace-after.json`确认全部相关仓HEAD/remotes及Desktop颜色源保持初始值。本轮未形成Git提交。


## 2026-09-14 用户视觉反馈后的后续

用户明确不满意本轮石墨底板/连线与额外描边，确认保留Coze原生轻盈质感、淡渐变，采用青柠替换蓝紫主题。新的视觉目标和实施证据独立见[24](24-native-coze-lime-refinement.md)。本文的技术/运行证据是当时真实事实，不代表这套视觉已获用户最终认可；24取代本文关于重石墨装饰及抹平渐变的设计选择。
