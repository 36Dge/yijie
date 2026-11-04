# FEAT-167 本地验收报告

本文件保留前轮验证记录。2026-11-04 的复审修复、v2 A01–A26 逐项结果及数据保护证据以 [10-reaudit-repair-delivery.md](10-reaudit-repair-delivery.md) 为准；不能再用下面的“40 次调用组”概括最终工具行数量。

2026-11-03；范围：本地开发交付，不是签名发布或 production_hardened 全部治理门禁声明。当前改动落在 Contracts、Host、Desktop及元仓；yijie-codex源码未修改。

<!-- evidence: CONTRACT-LOCAL-001 -->
## CONTRACT-LOCAL-001

Contracts固定 `dfd9012954c716d360f702d6be3bdbdef75e0633`，Host/Desktop两个native-process.lock均指向该提交。新契约4项正常样例测试通过，包含动作边界、retry四种输入、独立版本及无diff；旧V4源与实施前b51d260逐字相同。生成check、Contracts lint、v6单独OpenAPI lint通过；相对b51d260的breaking检查通过。旧端点退役是已批准的运行时兼容破坏，不以旧源文件未改冒充HTTP兼容。

<!-- evidence: HOST-NATIVE-001 -->
## HOST-NATIVE-001

Host gofmt/vet/shell检查通过；NativeTrace/NativeProcess/原生消息阶段及路由测试通过，相关session/app race测试通过。旧Native history及SSE路由404、当前路由认证/no-store、动作原始索引、无shell推断、元数据边界、retry意图都有正常样例。

`node scripts/check-native-conversation-integration.mjs` 通过：实际Host投影字节 → Native SSE decoder → 原生显示buffer → SQLCipher → 正常关闭重开。另新增format6读回测试，动作元数据保存后保持。

Native安全全套最终默认配置：625通过、0失败、14 ignored、27按长期安全条款过滤。日常Kimi配置完整运行658通过、2条旧SSE11断言失败、16 ignored、27过滤；修正两条夹具/断言后，日常配置两个对应测试均定向通过。未把初跑失败日志写成全量PASS。Rust fmt、clippy -D warnings通过。

<!-- evidence: FRONTEND-001 -->
## FRONTEND-001

前端安全回归最终：257个文件，2075通过、16跳过；另node:test脚本26通过。最后组内滚动CSS修复后，相关组件测试3通过，并以真实客户端复验。前端lint/类型检查、生成check、Vite build及文档build通过。构建保留既有bundle体积警告，不伪称无警告。

关键用例：32搜索＋32推理＋8命令仅一个40次调用组；公开说明分段；命令动作与调用/来源计数分离；未分类最后回答保留；失败/审批/瞬态决策在折叠外；同一轮增量保留用户选择；结构化结果、附件、复制、原始来源链接和完整消息阶段不被重写。

<!-- evidence: REAL-MODEL-001 -->
## REAL-MODEL-001

用户授权先2轮、后更新为MiniMax/Kimi各2轮。实际只发4个用户回合，无失败追加重跑。Kimi简单/多步分别12s、70s；MiniMax分别4s、35s；均收到真实结束与回答。它们是UI用户回合数，不等于仅4笔provider HTTP。

Kimi多步：4个native search、3个command调用，主阅读层为两个有调用的活动组。MiniMax多步：2个search、6个open_page，按公开中间消息分段。原始记录完整保留；没有把命令动作另算成调用。详见 evidence/real-model-observations.json。

两个模型均省略phase。真实公开说明及未知阶段降级阅读已验证；原生显式commentary/final字段在Host/Native/前端正常样例中通过，但本次真实模型未覆盖该字段。不能据此声明两个提供方都完整输出原生phase，也不保证模型遵守提示词中的搜索次数/字数上限。

<!-- evidence: VISUAL-001 -->
## VISUAL-001

在标准Tauri调试.app中人工通过桌面自动化观察：浅色/深色，1268×780及1180×760，100%和200%缩放；正文/标题/工具栏可读，活动组可展开、滚动，最终回答可见。系统原来为浅色，测试后已恢复；缩放恢复100%。

键盘Tab进入活动viewport、Page_Down组内滚动、Shift+Tab回到组标题、Return收起均成功。真实验收发现短滚动条接入需grid父容器；修复后在最小窗口复验，末端滚动值46，无此前的额外空白区，滑块位于右侧。axe、选区和减少动态效果相关正常组件回归随安全套件执行；未声称真人VoiceOver全流程验证。

同机512条记录纯投影基准：旧流程中位0.0721ms，新流程0.0441ms；7批×500次，原始样本见 evidence/reading-benchmark.json。这不是浏览器FPS或生产吞吐指标。

<!-- evidence: RESET-REPLAY-001 -->
## RESET-REPLAY-001

用户明确授权后，正常停止状态下运行 reset-trace-v6-data.py --apply，清理旧会话库、Host会话映射及易界独立Runtime历史/状态。保留密钥、配置、技能/连接器资源、工作空间文件，未触碰Codex自身数据。启动首先显示空任务列表，之后生成本次两个验收会话。

多个正常退出/重开均完成原生cleanup与专用服务清理；新格式历史读取、两模型标识、耗时、原消息/活动可正常展示，重开未重发用户回合。开发窗口缺少bundle identifier时桌面工具无法定位，经用户明确同意才使用标准debug.app验证；未覆盖签名/已发布应用。

## 逐项结论

| 标准 | 结论与证据 |
|---|---|
| AC1 公开说明和原生复用 | 公开说明/直接回答通过；真实提供方phase缺失，使用已验证降级，显式阶段生产能力未获本次证明 |
| AC2 连续活动组 | 通过：40调用压力样例及真实7/8调用记录 |
| AC3 标题和计数 | 通过：安全native动作、可信元数据、诚实兜底，三类计数独立 |
| AC4 状态区分 | 通过正常样例；四次真实成功终态已验，未人为制造真实失败/重试 |
| AC5 展开阅读 | 通过：独立控制、用户选择、历史收起、键盘和末尾可读 |
| AC6 异常/审批/计划 | 正常状态样例通过；真实任务未触发审批弹窗，不声称触发过 |
| AC7 一致性 | 通过：按ID更新、迟到delta保护、重复/来源/重开及跨仓实际字节测试 |
| AC8 新格式/退役 | 通过用户修订标准：6/13/6/6，旧Native接口退役，旧数据已清理 |
| AC9 视觉/性能 | 上述尺寸、主题、缩放、键盘及纯投影测量通过；限定于所述验证面 |
| AC10 产品闭环 | 两模型4轮真实链路、保存/重开通过；无diff；未签名发布 |

## 未执行与限制

不执行强杀、可执行文件替换/劫持、权限破坏、恶意载荷和危险归档注入；严格按scripts/test-safety-exclusions.json过滤。未额外花费模型额度制造失败、审批或重试样本。没有push、签名、公证或生产发布；下游工作树待用户代码评审，不把本地检查当作独立人工评审和G0–G6全绿。

初期失败已区分并修复：schema字段名、Go枚举生成名、旧协议fixture、只读草案遗漏format6、过时UI断言、通知语义标签、短滚动条grid接入。所有结果依上面的最终运行口径记录。


## 收尾状态

最后一次组内滚动修复已在1180×760实机窗口复验；随后正常退出调试版，专用服务正常停止，再由 `pnpm client:dev` 恢复固定开发入口。启动日志确认Runtime、技能、专家与连接器就绪。原始四轮记录重开后的task_started/task_complete仍各4次，见evidence/reopen-counts.json。系统浅色、100%缩放已恢复；固定入口重新启动为1268×780。

本地日志哈希与仓库状态见evidence/delivery-state.json；真实模型元数据不含原始推理正文或凭据。最后CSS修改没有改变协议或模型输出，定向组件回归及实际键盘/最小窗口复验通过。
