# FEAT-166 实施阶段快照

> 本文保留锁屏时点的实施事实及未执行项。当前已解锁并完成真实客户端D4，最终结论以[08](08-d4-acceptance.md)为准；本文“NOT RUN/额度0/active”不是当前状态。短期operation context正常续接保留标签的最终规则见00 R-07和07。

## 1. 接受与范围

2026-10-29用户明确接受修订后的需求包，要求按治理实施、严格复用yijie-codex及现有产物机制，并完成真实客户端验证。D0产品/UX接受已取得，进入demo_fast/local整体实现；不建立治理切片。

用户补充：验证阶段如果电脑已经锁屏，可先跳过依赖屏幕的项目。跳过项保留NOT RUN/锁屏原因及影响，不能记PASS或借此伪造D4。非屏幕检查继续；原长期禁止强杀、二进制伪装、权限破坏和攻击注入保持。

本次不提交/推送，不改Runtime/Host生产链，不迁移日常库，不消耗其他需求的模型额度。优先复用尚有效真实样本；需要新增付费调用时另记必要性和本需求额度。起点见`references/implementation-start.json`：Desktop干净，元仓FEAT-162已有改动保护。

## 2. 最小实现选择与权威源先行

- 原Runtime工具、MCP publisher、spool、事件、Native校验提交/ACK及SQLCipher存储完全复用。源基线仍为05记录的Runtime/Host/Desktop，当前无修改Runtime的理由。
- 新增同一Desktop私有预览族`chat-document-preview-v1.schema.json`，一个窄command按open/resize/position/close动作工作；请求只接受context及artifact或已绑定attachment身份、视口和阅读位置，不接受文件路径/任意URL/脚本。旧预览v1保持。
- source类型明确区分artifact(session/turn/artifact)与attachment(session/message/attachment)。刚发送时Vue只有临时message ID，messageId显式为null，由Native按attachment+session解析其已有持久消息绑定；仍强制user消息、file类型、content block和owner/tenant关联，不接受临时ID、路径或自行推造ID。历史真实messageId可继续作为附加约束。附件只读查询加入现有Native repository/application，按owner/tenant、真实message与session、bound状态、TTL/大小/摘要校验，不改变草稿接口或原生userMessage。
- HTML/文档内容复用已安装Wry的无宿主IPC隔离WebView及自定义资源响应，改为主窗内子视图。页面业务事件禁用，隔离内联渲染保留；无外网/导航/下载/持久站点状态。视口按主窗口边界校验，只有一个活动内容视图，关闭/失效正常释放。
- 文本继续复用原投影；Office复用既有OOXML预检、quick-xml与zip，新增结构化阅读适配而非新文件工具。PDF复用原结构准入和macOS自带CoreGraphics页面渲染，不安装第三方库或外部转换进程。页面/静态图片受已接受的预算限制。
- Native响应只传元信息/阅读导航/有效期，正文及图片留在隔离视图受权资源中，不把大图base64塞进JSON或主DOM。私有事件只通知当前视图加载完成或失效，窗口前后台复用Tauri原有focus/blur事件，不引入第二事件总线。
- 页面结构为现有Chat工作区列＋布局分隔组件＋标签/只读标题/阅读控件/Native内容占位。统一UI状态、10标签、宽度公式、手动激活和正常请求收尾，样式走现有token与YjIcon。

该设计是已接受需求中“最窄private边界/现有载体/系统渲染”的具体化，未扩大文件权限或新外部目标。新增源/派生类型和同源检查先于消费者；方向验证完成前contract仍semantic/NOT RUN。不以代码编译代替真实兼容。

## 3. 已实现内容与复用边界

1. 默认关闭的正式对话分栏、双入口、空状态、10标签容量、空页分配与按真实身份去重；同页收起保留标签和阅读位置，换会话或权限上下文清空。
2. 分隔线1px、8px命中区，默认/最小/最大按00公式；鼠标、键盘、复位、取消及窄窗口收起。原对话不卸载，输入区同步缩窄。
3. DOCX标题段落、基础列表、表格、图片；PPTX按relationship定义的真实顺序逐页显示正文与图片；XLSX真实行列、共享字符串、合并范围、日期/百分比、公式缓存；PDF由CoreGraphics显示实际图形页面。文本沿用已有投影。复杂排版不是完整办公编辑器，未呈现对象/限额截断显示部分内容提示。
4. HTML保留内联渲染脚本，隔离响应CSP禁止外部网络、导航、frame、表单、新窗口和下载；阅读默认事件保留，页面业务事件与控件禁用。主页面未扩大CSP/capability；无新依赖/plugin、无模型工具或publisher。
5. 一个活动Native内容视图，单在途读取+一个最新待发意图；切换先隐藏，不能取消的工作正常结束。Native关闭意图阻止晚到内容重现；持续每秒复核源有效性，背景释放、返回重新授权。正文/大图不经过主Vue DOM或JSON。
6. 新schema、TypeScript派生及正常请求fixture已同源纳入检查；不改变Runtime/Host/Contracts公共协议，不迁移数据库，不持久化标签或新增内容缓存。私有schema源位于Desktop `src-tauri/schemas/chat-document-preview-v1.schema.json`。

实现仅为local candidate，现有准入子集和预算保持。标准构建的App未签名、未发布；不能据此声明生产可用。

## 4. 正常验证与失败修复记录

最终命令、开始时间、退出码、原始输出及输出SHA见[implementation-checks.json](references/implementation-checks.json)。源码/依赖/构建回执摘要与最后治理检查见`references/implementation-final.json`。

| 检查层 | 当前事实 |
|---|---|
| 前端领域、生命周期、附件及schema | 31项定向测试通过；含后台恢复、连续切换及旧结果释放 |
| 旧组件兼容与Chat页回归 | 9项通过，85项未选；不是全量suite |
| Rust内容与schema | 7项通过：6项普通文档+1项同源请求往返 |
| SQLCipher绑定读取 | 1项通过：真实持久消息、临时ID为空时由Native解析、过期检查、跨scope拒绝及重开读取 |
| lint / 静态检查 | make lint；另执行candidate feature的全target clippy -D warnings |
| 构建 | make build与设计文档构建；canonical media候选prepare-only，无App启动/模型请求 |
| 真实客户端 | NOT RUN：工具报告Mac锁屏，用户允许先跳过屏幕依赖项目 |

保留修复历史：

- 首轮Rust编译发现文字MIME生命周期及Wry回调Fn闭包问题，已修正，后续检查通过。
- 首份普通PDF fixture用了当前准入不支持的xref-stream。改用项目已经支持的cross-reference table格式，未扩大准入。随后像素验证发现系统GetDrawingTransform只缩小、显式坐标翻转又造成方向错误，已改为正确的像素缩放与系统坐标，红/蓝位置断言通过。
- schema往返首次严格JSON比较遇到整数与浮点表示差异；样本按字段的number类型明确使用浮点，JS/Rust共同验证通过，不改变数值语义。
- 首次旧组件回归命令误匹配.local历史源码副本，记录为无效验证，明确排除后只跑当前源码。当前ChatPage历史断言仍引用FEAT-165已替换的附件卡片/大小文案；对照HEAD确认是过时断言，更新为现有chip与PDF可访问标签后9项通过。
- 自审发现临时消息ID不具Native授权资格，改为nullable messageId和Native现有绑定解析；文件去重使用稳定session+attachment身份。数据库普通测试覆盖该分支。
- 持续校验中的数据库暂时失败原会误归为过期，现归为可重试unavailable；窗口后台与恢复复用原Tauri事件，不引入新的事件总线。

不运行全量make test/cargo test：已有历史套件包括危险归档/攻击fixture、权限故障或强制进程/二进制操作，违反用户长期条款。定向普通测试是安全替代，不构成攻击测试或完整历史回归通过；没有强杀、权限破坏、二进制伪装或恶意样本。

## 5. 锁屏待验与恢复

`cua.getState()`真实返回“The Mac is locked and automatic unlock could not unlock it.”。依用户补充，不要求解锁后才能继续编译，不尝试绕过锁屏，不伪造截图或验收。真实App启动、文件点击、Native子视图定位、原NSD脚本记录表、逐来源Office/PDF、图片/视频/SVG回归、拖动/键盘/读屏、1180×760亮暗主题及资源性能保持NOT RUN。

恢复后入口为 `YIJIE_KIMI_K31_CALL_SURFACES=media ./scripts/run-local-demo-fast.sh --packaged --kimi-k31-pro --reopen`（在yijie-desktop执行）。仅在最终回执仍与当前源码/环境一致时使用；脚本拒绝失配则正常重新prepare，不能绕过。使用该canonical local media候选，优先复用尚有效且来源可核的已有真实产物/已发送附件。原NSD原件仅限本机授权呈现，不提交模型；合成同名文件不能替代。若不存在可复用真实样本，模型调用额度仍为0，不能借FEAT-165额度；普通文件选择和阅读不需要模型调用。

`feature.status=active`，D4不运行、不记录PASS，10项Must保留pending。源码自审与静态方向性证据不能替代Native平台兼容。全程未commit/push/tag/发布，未改日常数据或执行迁移。
