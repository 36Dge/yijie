# 复用 Coze 原生工作流编辑页

2026-09-13，FEAT-153 本地产品追加，Owner：段成威。用户明确要求先审计 `yijie-coze`，存在原生工作流前端则直接复用，不自行仿制布局。本文与证据目录 `evidence/native-page-20260913/` 独立记录本次候选；17 的 D4 和 19–21 的追加验收保留原范围。

当前状态：**本轮原生页面接入与 packaged 功能验收完成**。真实创建/编排/首存/撤销/保存重开、试运行/内部发布/版本执行/历史、Chat 草稿保护及正常App/栈重启读回已验证。主题与品牌配色按用户决定 **DEFERRED BY USER**；不计主题PASS，不宣称重跑了dev或统一fresh D4。

## 源码审计结论

锁定上游 `fefb05ff27be1da939612fbf9faf5db62583b8ae` 中存在完整原生页面：

| 内容 | 实际源码（相对 yijie-coze） |
| --- | --- |
| `work_flow` 路由 | `frontend/apps/coze-studio/src/routes/index.tsx` |
| 原生页面入口 | `frontend/packages/workflow/adapter/playground/src/page.tsx` |
| 可直接挂载的编辑页 | `frontend/packages/workflow/playground/src/workflow-playground.tsx` |
| 顶栏、无限画布、底部浮动栏和侧栏组合 | `frontend/packages/workflow/playground/src/components/workflow-container/index.tsx` |
| 原生顶栏 | `frontend/packages/workflow/playground/src/components/workflow-header/index.tsx` |
| 缩放、交互、自动布局、小地图、加节点和试运行 | `frontend/packages/workflow/playground/src/components/toolbar/components/tools.tsx` |
| 紧凑节点、端口及点击打开配置 | `frontend/packages/workflow/playground/src/components/node-render/node-render-new/index.tsx` |
| 节点表单侧栏 | `frontend/packages/workflow/playground/src/components/node-side-sheet/index.tsx` |

旧 `workflow-local/src/main.tsx` 自行组合多行 header、工具栏与试运行输入，`native-canvas.tsx` 自行实现 LocalNode。旧接入真实复用了 `@coze-workflow/render` / Flowgram 底层，但没有挂载完整 `WorkflowPlayground`。这解释了用户两张截图的结构差异，不能将旧结果称为已经复用原生完整页面。

原生页面默认获取 space、节点模板、模型、变量、trigger，并调用上游保存、试运行和发布 API；直接替换 URL/import 会改变已批准的身份与运行边界。现有 `nodeRegistries` prop 只有声明，实际注册并未使用它，不能靠传参声称白名单成立。截图中个别 SaaS 控件由 `IS_OPEN_SOURCE` 隐藏，不为逐像素匹配开启 SaaS 标记或伪造其服务。

## 实施决定与边界

`contract-impact = breaking`：2026-09-14 Git交付审计纠正实现阶段的semantic分类及事件additive判断。
旧Desktop的严格validator拒绝`request_history`后进入`protocol_mismatch`恢复状态，令iframe inert、
显示重连遮罩并阻断画布交互；该分支不会直接撤销API会话或销毁草稿。原生表单/图序列化的
semantic核对仍保留，整个替换取桥跨版本breaking为最高风险。仅启用同源配套local候选，
先升级Desktop reader，再启用Coze producer；不得将结构检查通过称作旧reader兼容、生产资格或发布批准。

- `workflow-local` 继续承担静态 React 独立入口和现有有限 MessageChannel，挂载真实 `@coze-workflow/playground/workflow-playground`。复用上游 WorkflowContainer、节点 renderer、节点表单、无限画布、浮动工具栏及开源设计系统。
- 在原生组件和服务中增加明确的进程内 local adapter 注入口，以现有 WorkflowJSON 交互，不另造业务 wire DTO。默认无 adapter 的上游路径保持原语义；所有受影响的上游文件在 source lock 逐项登记。
- 原 DraftModel / EditorRunModel 继续掌管 CAS、保存快照、原 operation 查询、明确终态与成功试运行后内部发布。页面渲染、Promise 返回和按钮点击均不构成成功证据。
- 初期仍只有开始、文本处理、结束，注册、添加与表单入口采用真实限制。模型、插件、Code、HTTP、知识库、SaaS、账号登录和平台调用不在本轮授权内。预算为零。
- 原生工具栏打开试运行表单，原生顶栏承接返回、明确保存、发布与运行记录；Desktop 全页移除重复标题栏。正常首次加载、错误、到期和关闭期间仍可返回；到期保留同一 iframe 草稿，显式重连，不刷新丢弃内容。
- `request_history` 仅携带协议版本、request ID、bridge ID/generation，无 workflow ID、凭据或业务 payload。Desktop 使用当前已验证资源打开既有运行记录。权威源为 Contracts `jsonschema/workflow-editor/bridge-v1.schema.json`，候选版本 `1.3.0-local-candidate`；旧严格 consumer 会拒绝新 kind，先同步 Desktop reader，再由已登记的同源编辑器产物发送。API/Coze/HTTP/native 操作权限不因导航事件扩大。
- 不改变数据库 schema、已有草稿、版本、历史或删除 tombstone；不改 Chat、Codex Runtime、Tauri capability、CSP、网络地址和机器凭据边界。若序列化不兼容，应修复局部 adapter，不静默改写旧数据或扩大 provider 能力。
- 构建使用固定上游 Rush lock 的真实依赖与源码，保留 frozen-lockfile / ignore-scripts。包内 alias 可在可追踪构建投影中解析，原始源文件不因此改写，不用 stub 代替原生模块，不放宽 CSP 掩盖运行问题。

备选方案：仅调整旧页面 CSS 无法满足用户要求，弃用；直接挂完整 Coze Studio 会引入另一套账户和服务，弃用。选择原生页复用加有限数据适配，理由是同时满足视觉来源和已有工作流闭环。

## 本次验收要求

1. 同一个正常 packaged App 进入真实原生页面，单一紧凑顶栏、完整无限画布、原生紧凑节点/侧栏与底部工具栏可见；1180×760 及较大窗口、亮暗主题无关键遮挡。
2. 使用新建合成工作流完成节点/连线编辑、保存、返回、重开，核对内容和位置；已有工作流只读兼容，不覆盖截图对应资源。
3. 原生 UI 完成试运行、内部发布，并从真实运行记录执行版本和查看结果；错误输入可修正，未知写不自动重发。
4. 未保存内容自然到期后保留，显式重连后保存；正常关闭/重开不混用会话，原 Chat 边界保留。
5. source-first、生成消费副本、限定静态/状态/服务检查与原生页面构建分别记录；未执行的 dev/全量 D4 或无障碍专项不得混记 PASS。

App PID 52971 在开始构建前实际处于用户截图对应编辑页，状态为草稿已读取、会话到期；已用“返回工作流”正常关闭该会话，无放弃未保存内容提示，再用 Cmd+Q 正常退出。Infra `make workflow-stop` 返回 STOPPED，原容器正常退出，四数据卷保留。没有强杀、权限改动或数据清理。

后续提交仍需 Contracts 先形成不可变完整提交，再逐消费者重新 pin 和提交，最后元仓记录。本轮未授权新的 Git 交付，不执行 add/commit/push；当前候选不适用于生产发布。

## 构建诊断事实（进行中）

第一次真实类型检查发现旧构建排除规则 `output.*` 会误删原生 `src` 下 output/outputs/output-tree 业务模块；已改为只排除明确的包根构建产物。原生 exports/typesVersions 和已使用的真实 src 子路径也需要准确投影，不能以 stub 或删除类型断言代替。

标准 Rsbuild 诊断曾因 Tailwind `design-token` 的 re-export 间接加载 `tailwind-contents → monorepo-kits → Rush SDK → install-run-rush.js --help`，触发 Rush 自举。该前台构建经一次正常 Ctrl+C 结束（exit 130），rsbuild PID 67366 及子进程正常退出，无升级信号。产生的仅 ignored `common/temp/install-run/@microsoft+rush@5.147.1/` 引擎缓存被保留，tracked common 未改；没有由其启动应用或工作流服务。

修正方式是在受控 prepare 中单独投影上游原始 `designTokenToTailwindConfig` 纯函数前缀（截至最后 re-export 之前），记录原始与投影摘要。App Tailwind 只导入该构建模块和原生 preset/token，不再加载 Rush 发现器。该记录不是忽略错误后的构建 PASS，最终 bundle 和 App 验收仍待完成。

原生 Rsbuild 已成功生成约 43.1 MB 的真实完整资源，但当前候选未激活：原静态 gate 拦下了 Worker 构造代码，544 个资源也超过既有 512 文件上限。正在做锁定模块的可达性审查，并使用标准 chunk 合并控制体积/数量；不扩大 worker-src、unsafe-eval、网络目标或 manifest 预算。

类型检查采用同一 TypeScript 5.8.2/严格配置对照锁定的原始 Git blob。当前完整应用 126 条诊断与原始基线的 126 条完全相同；仅允许字节未改的上游源具有同位置/code/message 的既有诊断，新/修改源和缺模块诊断一律不豁免。结果为 `PASS_WITH_REPORTED_UPSTREAM_BASELINE`，不是上游全仓零类型错误。完整诊断留在配对 JSON 中，不删 `@ts-expect-error` 或使用 `noCheck`。

只读键盘审计发现原生节点/端口默认无等效的方向键移动和键盘连线，正在原生组件及原生 document/history API 上补齐可访问操作。旧图340像素的横向间距与原生360像素节点可能产生20像素重叠，读取时保持既有位置；原生“自动布局”是明确、可撤销、待保存的编辑动作，不能在 normalize 中默默改变已存布局。


构建 06/07 的差异已逐 Webpack 模块、逐字节定位：Semi 聚合导出模块的 Row/Col 局部绑定顺序交换，入口两个聚合模块的同集合依赖/纯 helper 顺序改变，独立 Worker 资源仅 full build hash 变化。采用标准 Rspack `optimization.concatenateModules: false` 保留模块边界，产物不做后处理。08 的 382 文件、45,218,799 字节和最大 11,804,583 字节仍在原预算内；待同输入连续构建比对及精确摘要静态审查后才允许激活。

最终只读审查发现上游 `workflow/nodes/src/workflow-json-format.ts` 的 `formatOnSubmit` 无条件向 console 输出完整图，原生首次归一化和每次变更都会触发。已删除这条调试日志并登记 source lock；不改变图数据和序列化。该确定修复使先前 08/09 不能充当最终同源双构建证据，后续重新冻结核验。


断连边界最终审查发现：仅父 iframe inert 无法作为原生事件层的唯一保护，旧 adapter 在 `ready=false` 时丢弃 change，可能使断连边界晚到的编辑事件与可见原生文档不同步。修复为 native playground readonly 与 global preview 同时跟随 `!connected || localReplacing`，远端读回完成后按最新会话状态恢复；当前已挂载草稿接受已发生的本地 change/name 事件，保存、试运行、发布和读请求仍由原 binding/ready/generation 控制。此修复不允许离线网络写入。实际自然到期→重连→保存仍须独立观察。


最终源 canonical10/11 的 382 个资源路径、大小、SHA256 全部一致（45,218,737 字节，单文件最大 11,804,583 字节）。关闭 scope hoisting 后确认构建可复现。对该冻结字节建立 40 个明确路径的静态审查目录，逐条分类 127 个实际语法位点及 244 个正则命中；未分类、变更摘要、缺文件仍阻断。该目录只解释保守源码扫描的命中，不提供浏览器执行权限；API 原 `connect-src 'none'`、`worker-src 'none'`、不含 `unsafe-eval` 的脚本策略和 512 文件/64 MiB 总预算均未改。

独立只读检查最终10的真实拆模块调用链：Text 使用原生 preset-expression 与 mixLanguages({})，未加载独立 TypescriptEditor Worker；get-intrinsic 全部当前调用者仅请求 String/Map/WeakMap 固定方法，不进入 Async/Generator 动态构造分支。此结论不代替实际 App 控制台观察。9 项有限静态审查测试通过；Desktop 标准 unsigned packaged debug 构建通过，尚未启动。


## 首次真实 App 结果（未通过，修复中）

canonical12 经 `make workflow-editor → workflow-build → workflow-up` 正常恢复，ready 为 true。标准 packaged launcher 生成并启动 PID 80144（1180×780）；通过工作流列表只读打开 `7684953519702409216` 后，bootstrap 成功但原生 React 页面空白。未创建或修改流程。标准 WK Inspect Element 打开的控制台实际发现：

- eager `code-editor-adapter → preset-code → Shiki` 顶层创建高亮器，默认 Oniguruma 尝试 WebAssembly，被现有 `script-src 'self'` 拒绝。此前静态审查遗漏 WASM 这一类执行入口；Text 不加载 TS Worker 的结论不能覆盖此链。12 不是 App PASS。
- 原生 `registerRenderer → registerLayers → registerLayer` 期间 Inversify 缺少服务绑定（minified `g`），导致 React 树退出。
- 有 addLine/addNode operation meta 重复注册警告，仍须确认与修复范围。
- 控制台更早的一条 `webview.internal_toggle_devtools not allowed` 来自本次使用标准快捷键尝试打开检查器，被原有 Tauri permission 拒绝；随后使用 WebKit 原生 Inspect Element 成功，没有新增权限。它不是 workflow CSP 结果。

控制台完整 AX 与截图留在 `first-app-console-failure.*`，页面留在 `first-app-blank.*`，原生 AX 在内存扫描 K_NA/K_AC 均为零匹配。未据此宣称 heap/端口全量扫描。通过侧栏工作流链接正常返回列表、关闭会话，再 Cmd+Q 正常退出；launcher exit0、`make workflow-stop` 正常退出，原命名卷保留。

下一候选修复使用锁内 Shiki 原生 JavaScript RegExp 引擎替代其默认 WASM 引擎，保留实际语法、主题、API，不使用假 WASM/stub。另修复缺失的原生 DI，并增加 React 错误恢复边界，失败时保留明确重试与返回入口。所有修复完成后需重新冻结、构建、登记和真实 App 验证；CSP 与 Tauri 权限仍不变。


真实 DI 根因为 local 注册 Export 贡献但剔除了其注入依赖 Copy。现仅绑定原始 `WorkflowCopyShortcutsContribution` 单例供原 Export 调用，不把 Copy 注册为快捷键，不恢复 Copy/Paste/Load 入口。真实类只注入 document/select/globalState，无构造或 postConstruct 网络副作用；原导出行为保留。原生错误堆栈和模块映射见 `native-12-runtime-di-copy-fix.md`。

高亮修复采用仅匹配 `shiki` 根 specifier 的源码适配，原 `shiki/dist/index.mjs` API 全量重导出，只在 createHighlighter 未显式提供 engine 时选择同锁 `createJavaScriptRegexEngine({ target: 'ES2018' })`。锁内原 md/js/ts/python × github-dark/one-dark-pro 八种组合的真实 token 与 HTML 高亮检查通过；脚本及输出已归档。此检查不伪造 WebAssembly/global 对象，不执行被禁止能力。静态扫描新增 WASM namespace 与别名调用分类；旧12的审查因缺该字段会被明确拒绝，不能沿用旧清单掩盖遗漏。


## canonical14 部署及当前阻塞

包含 Shiki JavaScript 引擎、真实 Copy DI 绑定和 React 恢复入口的新候选，经 canonical13/14 正常构建，382 个资产逐文件路径/大小/SHA 全部一致。canonical14 build/check、10 项有限静态检查、8 项真实高亮 smoke 通过；原126条上游类型基线单独保留，新修改源无新诊断。manifest 为 `2dfbe477ac2b38ad6b84093306d34785a91983c9ae6fa2d1cce8742a4cfe03ac`，source_digest 为 `302f55d847d02354964b545b2b852352e5086e443d1324e789ebbc990319f975`。

按标准入口重新登记、构建镜像、恢复服务，真实 ready 通过；标准 packaged launcher 启动 PID 85986，构建记录为1180×780。接着调用 CUA 选择正常运行的 App 时，工具明确返回 `The Mac is locked and automatic unlock could not unlock it`。已请求用户手动解锁，未用 AX 或其他方式绕过锁屏继续操作。

可独立完成的只读核对：382个已部署资产共45,278,718字节全部匹配manifest；实际HTTP入口与本地index.html逐字节相同；响应仍为原CSP，无unsafe-eval/wasm-unsafe-eval，worker/connect均none；内存扫描K_NA/K_AC在所有已登记公开资产中零匹配。截图对应工作流 `7684953519702409216` 的完整legacy/metadata响应、revision、canvas、名称、描述、位置与本轮开始前完全相同。

当前 App/栈保持正常运行，尚未在14候选打开任何编辑会话，未创建、保存、发布或删除工作流。待解锁后从真实页面首次加载及控制台复查开始，继续本文五项实际验收；不得用12的失败界面、13/14的构建或以前17/19–21的验收冒充本次通过。没有执行新的Git add/commit/push。


## 用户解锁后的14候选复验

PID85986与原local栈保持同一候选，真实ready仍为true。CUA读取到工作流列表；标准WebKit Inspect Element进入检查器，无权限变化、无页面脚本注入。开始操作前的控制台基线为3条Tauri event unlisten错误和2条Coze operation meta注册警告，已独立留证，未清空日志伪造零错误。原生页面没有新增WASM或缺DI错误。

- 从列表只读打开旧图 `7684953519702409216`，原生单一顶栏、名称、说明、保存/记录/发布控件正常出现。`DraftModel.normalize`发现原生序列化与旧图的表示差异，原生错误页阻止继续加载；未保存或修改服务端图。源码证明差异为原Text格式化器对字符串literal补 `{rawMeta:{type:1}}`，并非正文变化。拟仅在语义比较中认可这一个精确冗余表示，原graph仍保留metadata；其它值/type/meta/ref/位置变化仍阻断。
- 正常返回后，用户授权范围内新建合成流程 `7685009958215090176`，名称 `FEAT153 原生画布验收 0913`，描述为33字的合成验收说明。确认创建成功并返回真实ID；API legacy/metadata读回一致，新图有开始/结束两节点。进入画布时原 `DragTooltip` collector同步读取尚未赋值的解构变量，出现真实 `ReferenceError: Cannot access 'p' before initialization`；原生错误fallback保留返回入口。没有重复创建、保存、发布、运行或删除。
- 通过fallback正常返回，native日志确认session remote close，再Cmd+Q退出；launcher与`make workflow-stop`均exit0、四数据卷保留。待两处局部修复完成后，复用这个已创建的合成ID继续验收，避免制造重复测试流程。

本次证据为 `app14-console-before-open.json`、`app14-existing-normalization-stopped.json`、`app14-new-workflow-fallback.json`、`app14-console-after-new-workflow.json` 和 `native-workflow-created.json`；所有已记录AX在内存扫描K_NA/K_AC均零匹配。源码定位见 `native-14-drag-tooltip-tdz.json`。原Tauri注销脚本问题仍单列为基线，未因其源码无本轮修改就声称无影响。


两处最小修复已完成：

- `localDocumentMeaning` 仅对string输入、literal字符串内容、rawMeta精确唯一键type=数值1，比较时去掉该冗余hint。实际graph保留rawMeta，不改后端、不清空字段；其它metadata双向差异、内容、type、ref、位置仍拒绝。相关state检查12/12通过。
- 原DragTooltip在collector内部先读取monitor的item/sourceClientOffset局部快照，避免React DnD首次同步收集时读取外层未初始化解构变量；保留真实Tooltip、拖拽服务与反馈。普通初始/拖拽/坐标更新三种同步collector状态验证通过，原源码与脚本/结果留证，不把此纯collector验证冒充实际React/App通过。

原Tauri清理问题的源码基线与未归因边界见 `native-tauri-listener-baseline.md`；14的旧图打开和新建流程阶段没有新增Tauri该类错误，新增总error的第四条是上述独立DragTooltip TDZ。待更新候选重新执行真实页面闭环。


## 16候选真实进展及界面收尾修复

正常部署16后，packaged PID93579从干净控制台开始本轮操作，未使用Tauri devtools快捷命令或清空日志。旧图`7684953519702409216`完整加载原生顶栏、三节点/两连线、画布及底部浮动工具栏；打开原生Text侧栏真实读回`创建确认：{{input}}`，保存保持disabled/已保存。返回后没有未保存提示，未对旧图写入。证据 `app16-existing-canvas-loaded.json`、`app16-existing-prefix-read.json`。已有80/420/760位置保持原样，原生360宽节点存在已知20像素相邻重叠；不自动重写原用户布局。

复用已创建的合成ID打开两节点页面，原生添加面板正常显示唯一Text选择。点击添加后，本地单Text限制把可添加分类过滤为空数组；原NodeList却向子组件传`[nodeCategoryList[0]]`即`[undefined]`，真实控制台出现categoryName解构错误。已定位并仅改原渲染传参为`nodeCategoryList.slice(0,1)`；空/非空正常用例检查通过，原生卡片、分类和单Text限制均保留。证据 `native-16-empty-category-source.json`、`native-16-empty-category-check.txt`。

该次添加已经形成未保存本地内容，未执行保存/试运行/发布。正常返回显示确认，已通过App显式选择放弃**本轮代理刚添加的合成测试节点**；创建记录和服务端两节点草稿保留，旧用户流程未动。native close确认后Cmd+Q/launcher与受控stop均正常exit0。不得将这次未保存添加当作成功编辑闭环。

另外，End节点输出类型曾显示`workflow_241111_02`。原中文资源已正确包含“返回变量”；原生模块在locale ready之前把I18n.t结果缓存为常量，非资源缺失。相关183个唯一literal key在固定中文资源均存在，此数量含隐藏分支，不称183个可见控件。现将原生WorkflowPlayground改为locale完成后才执行的React.lazy模块；顶部EditorBridge早注册不变，加载期间保留原生Button返回，正常重绘保持同一lazy/native DI实例，显式重试才更换lazy实例避免缓存的导入失败。有限语法及只读加载链审查通过，无手写布局/翻译表或CSP变化。17/18候选仍待真实闭环复验。


## canonical18 真实主链路与首存修复

17/18 同输入标准构建的385个资产路径、大小、SHA均一致，合计45,281,867字节；manifest为 `f10f0b90eadc611c327e456cb9db4b92436b1e7c7268cccec90dadf12f34d970`。受控入口启动的packaged PID696真实加载原生页面；End字段显示“返回变量”，添加唯一文本节点后不再崩溃。

复用合成流程 `7685009958215090176`，通过键盘端口操作完成开始→文本处理→结束，原生自动布局后在原生文本侧栏输入 `原生画布：{{input}}`。未保存内容自然到期后，同一画布节点、边和内容仍保留，显式重连并保存成功。原生方向键移动文本节点并保存，真实API确认位置从640,0到690,-10；聚焦空白画布后使用原生Cmd+Z撤销并保存，API确认回到640,0。回到列表再重开，内容、两条边和三个位置均读回。

原生底栏“试运行”打开侧栏，输入“易界验收”取得成功及输出“原生画布：易界验收”；内部发布得到真实v0.0.1。从原生顶栏打开版本与运行记录，执行v0.0.1取得成功及输出“原生画布：版本执行验收”。普通不存在版本v0.0.99显示资源错误，修正为v0.0.1、输入“修正验收”后成功输出“原生画布：修正验收”，运行ID `7685027859953352704`。这些是实际UI动作与服务端终态，不以running或点击当作成功。

首个新增节点保存仍发现一个体验缺口：原生文档顺序Start/End/Text与保存快照Start/Text/End不同，整图key保留数组顺序，误判外部改变并reload，关掉面板且清原生history。后续顺序一致的移动保存不会触发，原生Undo已通过真实API核对。因此增加仅用于整图比较的顶层nodes/edges规范排序；不改实际图、嵌套数组、通用JSON比较和所有字段。此修复后需要重新构建及实际首存/撤销复验。

完成上述观察后，PID696通过Cmd+Q正常退出，受控 `make workflow-stop` exit0，命名卷保留。未做强杀、数据清理、时钟调整或故障注入。首次lazy加载返回按钮在点击前已消失，CUA报stale element，故首次加载取消仍标NOT VERIFIED。证据：`app18-natural-expiry-dirty.*`、`native-keyboard-move-undo-verified.json`、`app18-run-version-success.json`、`app18-version-error-recovered.json`。


## canonical20 首存修复资格与深色阻塞

19/20的385资产路径/字节/SHA一致，总45,282,354字节，manifest `d5176e19616f5935ec85d1aa3e9efa7c54ef8d15d7de97a19270009b0a5fa79a`，source_digest `feaa8e90180db13d2b479c0cd36bd24c624df20dc176e144837c5e950ab4d95c`。14项focused测试通过，严格类型配对仍为126条未修改上游基线、无新诊断。45文件审查仅对3个已定位模块变化/构建hash传播更新，实际131个语法位点和301扫描命中未新增类别；没有扩大CSP/预算/依赖。

真实packaged PID10839通过创建表单创建单独的最终合成流程 `7685031373442121728`（FEAT153 原生终验 0913）。原生三节点/两边、键盘端口连接、自动布局、文本`原生终验：{{input}}`，首次保存revision `7685031776485376000`成功，侧栏仍打开。聚焦原生空白画布Cmd+Z恢复`{{input}}`并标dirty；切换Chat出现未保存提示，选择继续编辑保留；Cmd+Shift+Z恢复前缀且重新识别已保存。随后正常切换空Chat输入页，未发送任何消息或模型请求，再从列表首位重开读回内容和位置。首存误reload及丢失history问题在真实App已修复。

该候选在UI完成草稿run `7685032443987886080`（页面终验→原生终验：页面终验）、内部发布v0.0.1、版本run `7685032637395632128`（版本终验→原生终验：版本终验），结果及刷新后history均显示成功。read-only API/MySQL验证首存canvas字节一致、两次run输入/输出一致、PG/MySQL五份共享回执一致，完整重启前快照为`canonical20-final-before-normal-restart.json`。旧截图流程完整legacy/metadata响应与本次开始前仍完全一致。

亮色实际1180×760与较大1346×849的顶栏、三节点、连线和底栏无关键遮挡（大尺寸原请求1440×850被系统按屏幕范围限制，以实际CG窗口尺寸记录）。深色html.dark/body theme-mode=dark确实生效，但实际存在节点/侧栏标题浅色渐变、过亮点阵、文字区浅底白字和节点标签低可读性；不计主题PASS。分别保存`app20-light-*`、`app20-dark-*`原始截图。原生WebKit Console在整个本轮创建/编辑/运行/重开后0error，6个warning是原有addLine/addNode重复注册及Semi Tooltip delay警告，无WASM/CSP/DI/Tauri unlisten新增错误；控制台未清空。

深色截图后自然到期，再显式重连，已保存图与侧栏内容保留。正常返回关闭会话，再Cmd+Q，PID消失、launcher exit0、workflow-stop STOPPED，数据卷保留；系统恢复浅色。等待只修主题适配后的最终构建和实际复验。本轮未执行强杀、权限改动、网络放宽或Git交付。


## 用户范围调整：主题延后

用户明确“主题验收可以暂时不做，因为后续还要调整这个页面的颜色主题（coze颜色主题是蓝色的，和yijie是不符合的）”。因此停止主题实现与21/22构建；待统一易界品牌配色时另做主题验收。已经观察到的暗色标题渐变、点阵亮度、文字区可读性保留在上述20截图和审计记录中，标DEFERRED BY USER，不伪造PASS。

主题代理刚开始的一轮局部CSS变量增量（未构建、未激活）精确撤销，保留之前的原生组件替换、首存修复与全部既有用户改动。最终功能候选继续使用canonical20，以原manifest与source digest重新核对后正常重启、读取已保存流程和运行事实。没有启动21/22构建或修改已部署产物；后续品牌色设计不在本轮继续展开。


## 最终功能交付结论

用户暂缓主题后，未启动21/22；仅精确撤销本轮尚未构建的主题增量。canonical20 source/manifest check重新通过，四个主题源码与之前字节一致，首存修复保留。`native20-source-restored-check.txt`与`native-theme-deferred-audit.md`记录恢复过程；没有改manifest摘要去掩盖来源漂移。

受控栈正常重启为epoch `b13e0089-5888-43ac-b25b-0440956373ea`，旧epoch `28a9b428-3eed-4b0e-ae96-5d1dc2001b92`单独保留。正常packaged launcher启动PID18490，重新从列表进入 `7685031373442121728`：原生三个节点、两条连接、83%适应画布、已保存状态与`原生终验：{{input}}`在真实界面读回；历史列出两条原成功运行，选择v0.0.1的历史显示`原生终验：版本终验`。没有在重启后重复执行或保存来制造一致性。

`canonical20-final-after-normal-restart.json`逐字段证明：workflow/canvas/revision/v0.0.1/完整history/两个run与重启前一致；MySQL资源、版本、执行、操作及PG资源/操作一致。原审计行完整保留，新行均为正常成功read/bootstrap/history/read_run；GET触发审计追加属于既有服务行为，因此不要求审计总行数静止，也不宣称整个数据库完全无写。公开静态资产再次与同manifest逐字节一致，机器凭据零匹配；AX材料各次均零匹配，这不是完整浏览器heap证明。

实际UI证据为`app20-first-save-sidebar-preserved.json`、`app20-first-save-undo-preserved.json`、`app20-chat-after-clean-close.json`、`app20-version-run-and-history-success.json`、`app20-restart-actual-prefix.json`、`app20-restart-actual-version-result.json`及`native-coze-page-final.png`。正常关闭与重启日志分别在packaged-launch-20、packaged-launch-20-restart和infra-workflow-up-20-restart材料中。

| 本轮项目 | 结论与边界 |
| --- | --- |
| 直接复用Coze原生完整页 | PASS：活动入口使用原始WorkflowPlayground/Container、Header、紧凑节点、无限画布、浮动工具栏及侧栏；旧自画页不再活动 |
| 创建、中文元信息、编排、首存、Undo/Redo、保存重开 | PASS：同20候选真实UI及数据库读回；首存排序误reload已修复 |
| 试运行、内部发布、版本执行、结果/历史 | PASS：真实UI取得成功终态，与API/MySQL一致 |
| 未保存离开确认、取消、Chat切换 | PASS：20真实操作；未发送Chat或模型调用 |
| 到期/重连 | 18已观察未保存图自然到期→同页保留→重连保存；20观察已保存图自然到期重连。明确区分候选，不合并为新D4 |
| 正常App/栈重启读回、旧用户资源保护 | PASS：20同源产物、不同正常epoch、实际UI和两库业务事实逐字段一致；旧截图流程完整响应未变 |
| 主题和最终易界品牌配色 | DEFERRED BY USER：浅色两尺寸已观察，暗色存在记录的可读性缺口；不继续实现或计通过 |
| 首次异步加载过程中取消 | NOT VERIFIED：操作前加载已完成，未用延迟/故障注入制造窗口 |
| 全量无障碍专项、dev和统一fresh D4 | NOT RUN：局部键盘连线、撤销、焦点操作不等于全页无障碍通过；旧17 D4保持原范围 |
| 公网/生产/模型/商家节点及Git交付 | OUT OF SCOPE：仅本地合成文本；未新增提交、推送或发布 |

原Coze少量控件仍有未命名AX按钮、dim token对比度和Tooltip/operation-meta警告，按原生来源与后续主题/无障碍工作记录，不声称商业视觉和所有边界已完全定稿。当前功能未见阻断崩溃或数据丢失。最终App保留在原生画布供查看，服务健康运行，系统浅色已恢复；不会自动续期编辑会话。

跨仓交付顺序仍为Contracts源契约形成不可变提交→API/Coze/Desktop精确消费pin→各自提交及Infra登记→元仓收口；本轮仅在已记录的local-candidate工作区验证，`workspace-final.json`保存各仓HEAD/status。所有已有用户修改与六份上游既有删除保留。
