# FEAT-164 S4U：保留数据的 Runtime 验证与验收范围调整

2026-10-26。Owner要求审计后继续执行，执行中又明确移除“当前App亮暗、键盘和最小窗口验收”。本报告承接47；整项目标仍为全部活动Kimi替换为kimi-k3.1-pro，保留历史/原操作/授权事实和MiniMax。整项IN_PROGRESS，不把合成协议通过当供应商G2V或日常切换完成。

## 审计与最小实现

contract-impact=none：只修改Host三个显式FEAT164测试的目录放置和成功清理，并新增保留状态验证入口/说明。删除测试中的成功RemoveAll，继续走原Manager.Shutdown与server.Shutdown；保存每个home和完整副本、检查句柄与四库。没有改模型fixture、场景断言、产品源码、wire、SQL、Runtime核心或补丁。其余492个已跟踪文件逐字相同。

独立Host测试提交`7bf43fe0b18188e71442611b781ed87811911cde`，基于产品来源`8cd6bccbdc1ac3906aea53d95441299f7cfefcce`。测试原始结果记录执行时HEAD及dirty文件hash，提交后逐一绑定同字节；不能改写成“先前已经在新commit运行”。App继续使用47的固定Host来源和bundle，不因测试提交重建或刷新产品pin。

测试入口`scripts/feat164-retained-runtime-conformance.py`精确校验r5 SHA283d12e…、旧producer SHA9766d7e…、Go1.26.5；只继承普通构建环境，明示dummy凭据和本机端点，零重试。失败即停，无CommandContext/timeout kill、checkpoint、WAL删除或原数据回填。

## 本轮已执行

| 检查 | 实际结果 |
|---|---|
| Runtime调用面 | 1项、6loopback：文本/图片/文件、标题、input-only草案与resume、专家指令、本地读取工具回灌 |
| 原生辅助 | 4项、9loopback：子代理继承身份与终态、显式压缩、Guardian正常本地复制审批、计量配置双provider |
| 旧loaded/重放/自动压缩 | 7项、23loopback：旧父子同thread切换、退役父子拒绝、failed/errored与冷历史、同子新身份成功、两种previous-model guard及当前/迁移后自动压缩 |
| 保留状态 | 10完整home及副本；40个数据库只读integrity ok，正常退出后WAL0，无打开home句柄 |
| 四组合来源 | ordinary/market/experts/media均PASS；原App来源未改 |
| Host领域 | 10项PASS：市场/专家精确身份、旧回执重放、暂停拒绝、终态后显式切换与旧事实保持 |
| 前端业务状态 | 9文件22项PASS：unknown/never-sent、退役/暂停、原操作恢复、迟到结果、计划保存与v2 wrapper；不含已移除的亮暗/键盘/窗口验收 |
| 组合配置 | 5项PASS；未知组合/不配对配置不准入 |

共49项定向测试，零skip，加4组来源检查。38次本机HTTP中7次旧K3仅为旧producer在各自截止点前自然产生历史，其余31次为K3.1；每个cutoff后均零旧K3出站。真实模型HTTP新增0，没有新增模型额度。

正常关闭/断言均首次通过；保留入口的编译先以-run '^$'检查，不记为行为通过。两次辅助git diff调用在工作区父目录错误退出，已纠正工作目录后检查；不是产品/Runtime失败，不触发重复模型执行。测试不扩大到既有强杀、攻击归档或故障注入套件。

## Owner移除的验收

Owner原话：“接下来补当前 App 的亮暗、键盘和最小窗口验收，这个验收明确不做。从 feat-164 需求中移除。”

从当前需求、计划和完成门槛移除亮暗切换、键盘/焦点专项、1180×760最小窗口专项。状态为REMOVED_BY_OWNER，既非延期、阻塞，也非PASS；后续不得再安排这三项或以它们未执行阻止FEAT164收口。旧报告的历史观察保留，不删除历史事实。

收到指令时只读查看到系统原为浅色，尚未切换外观，也未做键盘/窗口验收。候选已由canonical启动，立即通过正常⌘Q退出exit0，零模型fixture正常shutdown，模型尝试0；原71表行全保留，仅增加正常停止代际行，四库WAL0/integrity ok。关闭本轮打开的系统设置，没有改系统偏好。

模型选择、退役/暂停、unknown/取消/恢复与计划授权的**业务状态行为**仍属于原模型迁移需求；这不重新引入已移除的外观专项。feature.yaml保留治理结构中accessibility_visual字段用于这些剩余业务状态的独立记录，并显式列出已排除项，不伪造ui_change=none或全局修改治理脚本。核心、数据、权限、预算和正常退出要求保持。

## 当前缺口与下一步

- 本轮已关闭当前r5辅助、子代理终态/冷历史和自动压缩的缺失验证；不要再把它们列成未执行或重复运行38次。
- 46自然旧App迁移/恢复/正常取消/旧计划重新授权、47媒体App、48当前Runtime/业务状态组共同组成按层证据。完整TCONF04、G3及final core仍不得把多批source-bound子集直接改成fresh全链路PASS；应逐项核对缺口与源连续性，而非不断重建同功能候选。
- unknown/never-sent在领域和前端已验证，本轮未制造App未知态。已有原SQL41 unknown继续保留；无可靠原生回执不能宣称已恢复，也不能清库重发。不能安全构造的完整App场景须如实记范围/影响。
- 正常Runtime关闭责任已有当前r5 10home/40库及46/47App证据；完整teardown判定仍要与最终适用任务范围逐项绑定，不再以“checkpoint根因未知”作为旧阻塞。
- r5真实Provider G2V缺口、最终激活与日常cutover仍需要独立授权，当前不能新增任何真实模型HTTP。历史5/5、30元cap、保守14.679001元和14.188544元unknown预占保持；旧r4真实结果不自动继承r5。日常切换前需具体候选/备份/兼容reader/回退清单，不能以离线通过直接实施。

无产品修复或新增Runtime范围需要批准。工作区和旧证据/制品保持，原主Host不快进，测试改动在s4u独立工作树；只本地提交，无推送。全部本轮服务已正常退出。证据索引s4u-audit-index及s4u-retained-summary；完整home/数据库/keys仅留私有audit目录，禁止提交Git。
