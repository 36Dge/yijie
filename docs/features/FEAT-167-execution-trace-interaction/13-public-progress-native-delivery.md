# 公开开场与中途说明：原生链路交付

2026-11-05。当前本地实现与验收结论，以本文及机器可读账本为准。
11、12号文保留此前审计、授权、失败和修复过程，不能将其中旧时点的待审或暂停状态当作当前状态。

`contract-impact = semantic`：产品生成指令、受限模型公开消息适配和阅读投影有语义变化。
Runtime 原生消息/循环/预算/取消/权限继续复用；269份 canonical schema 不变。
SQL45、Native6/SSE13/IPC6保持。没有Host执行循环、diff能力、清库或迁移。
必要本地固化已获明确批准；未推送、打tag或发布，不晋升历史Feature正式门禁。

## 实现与固定来源

Runtime允许精确v1声明当前公开消息；流式和完成态统一解析，原始正文/phase保留。
有效非空过程声明沿同一turn的原生循环继续，原生phase/end_turn仍优先。
多声明冲突不拆Item、不触发声明续行；原生两次answer-only恢复只用于完成保护。
缺失声明仍为unknown，不能因此隐藏完整答案。r3识别实际出现的两种精确命名拼写；
先用旧r2正常回环复现漏判，再以同一回环验证修复，未继续扩充中文词表。

产品指令要求多数实质任务先开场、中途有真实信息增量；普通字数、语言、排版不构成豁免。
简单对话、单行、仅JSON、只要结果和必要澄清保留直接回答路径。
Skills原生显式与隐式加载均保留。普通start/resume及模型/专家切换同源策略验证通过。
前端保持公开说明独立、推理不切开工具组、正文开始后默认折叠及手动选择优先；
补齐Kimi broker可读标题，真实失败时去掉“不代表执行失败”的矛盾后缀。

| 仓库 | 精确提交 |
| --- | --- |
| yijie-codex | `2b79447c363165ecd3b9d12dffe300c1adddbbb0` |
| yijie-contracts | `62070251d0da84ce4c5eba0c7b25d9a48e5d5929` |
| yijie-agent-host | `0bae91eab00c31669dbce469d424330a20e7af60` |
| yijie-connectors | `2cac4658472731f0ac3348fe40085be89fe703ee` |
| yijie-desktop | `d11021e68994dee6dbb20284cf046e9e10afb40d` |

Runtime SHA256：`cf358a9140a5e1f7e74c02bf94d55c871c28d3f5f871dfd95fbdd0e7a327b0aa`。
用户提醒避免机械重复编译后仅构建一次Runtime，复用既有target；后续Host/UI调整未重编Runtime。
Desktop本地构建还包含已记录并保留的工作区改动，以上commit不代表干净源码发布制品。

## 真实模型结果

当前候选Kimi：20个实质场景，开场20/20（100.0%），开场＋合格中途
17/20（85.0%）；预先声明无工具11个，严格联合
10/11（90.9%）。4个窄例外全部直接回答，占当前24轮16.7%。
初始16个与追加授权的4个分别保留；此前失败、版本试验、协议诊断不混入此分母。
本任务Kimi共28/32用户轮，MiniMax8轮后按Owner要求停止。
未用额度不继续消耗。结果是当前样本的质量结论，不保证每轮或所有提供方遵循。

T11四次原生搜索违反两次上限且未核验官网；T12验收人员未及时处理审批而过期，0外呼；
T13与T20缺独立中途；T14目标读取被拒、只有官方摘要且第二次搜索过期；
T18违反不调用工具要求而调用空update_plan。以上失败/缺项均保留在分母。
E25已实际隐式读取copywriting，但最终消息漏声明，阶段unknown及完整正文均保持。
E26真实同会话追加任务保持先前上下文和独立阶段说明。

付费网页工具请求6次、实际外呼3次，未用满独立9次上限。
当前24轮记录76条用量结算；结算记录不等于所有HTTP尝试或收费金额。
完整轮次、请求边界、tokens和失败事实见 `model-call-ledger.json`、`kimi-web-tool-ledger.json`。

## 验证、数据及限制

M01–M14与原26项逐项结果分别保存为 `acceptance-current.json` 和 `interaction-26-current.json`。
同响应多真实Item、end_turn=false、工具驱动继续、正常interrupt和下一轮历史等由真实Runtime正常回环验证；
提供方本批主要通过显式声明适配续行，不能冒称它返回了原生phase/end_turn。
Host→Native→SQLCipher→正常重开→Vue链路通过。首公开delta与实际UI可见时点分别记录，未伪造精确首帧延迟。

r3完成保护10、公开消息7、解析器29项及scopedClippy通过；前端r3定向64项、最终工具呈现74项、
lint/类型及构建通过。历史全量安全前端2125项/脚本27项并非本轮全量重跑；21项安全排除不冒充执行。
UI主题、保存记录、展开、重开和固定入口状态以 `final-ui-verification.json` 为准；
1180×760、200%及减少动态效果的旧证据与本轮观察分开列出。
旧FEAT137 Runtime静态边界检查、Contracts冻结HEAD断言仍限制全仓检查；未为通过而改写它们。

当前37会话/41轮；SQL45未变。
原候选前6/9、r2前8/11、r3前11/14的记录逐行摘要均保持。旧轮内容不变，新增验收正常追加。
不承诺正常应用写入后整库文件逐字不变。原有工作区修改保留，仅任务相关文件必要本地提交。
无强杀、权限破坏、可执行文件伪装或攻击注入；无生产发布/签名/公网上线。
报告的file://内置浏览器预览被URL策略拒绝，采用离线结构及链接检查，不记作报告视觉预览通过。

完整本地报告：[/Users/jack/.codex/visualizations/2026/11/03/01a19f3c-608f-7090-8af9-7a63c92bfbf2/public-progress-native-mechanism-20261105/implementation-progress.html](/Users/jack/.codex/visualizations/2026/11/03/01a19f3c-608f-7090-8af9-7a63c92bfbf2/public-progress-native-mechanism-20261105/implementation-progress.html)。
证据根目录：`/Users/jack/Downloads/Personal_Info/CrossBSD/.local/diagnostics/2026-11-04-public-progress-v3`。
