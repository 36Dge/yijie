# FEAT-166 真实客户端调试记录（历史）

用户于2026-10-29确认电脑已解锁，要求继续真实客户端验证、直接修复问题并完成D4。此前锁屏未执行结论保留在06及旧快照中。本记录保留调试与失败候选；最终修复候选的同次fresh验收与D4结论见[08](08-d4-acceptance.md)。

## 调用与数据边界

用户单独授权最多2次真实任务提交，最终累计2/2（逐次记录见下方历史及08）。使用标准普通合成Office/PDF与文本附件；原NSD不作为模型附件/正文发送，只通过既有publisher按本地路径登记，源字节留本机。逐次提交记录见`references/live-validation-calls.json`。不借用FEAT-165额度，不seed数据库，不改变既有授权/准入策略。

## 第一次真实运行

canonical命令：`YIJIE_KIMI_K31_CALL_SURFACES=media ./scripts/run-local-demo-fast.sh --packaged --kimi-k31-pro --reopen`。回执/source guard通过；2026-10-29实际App PID2069，Host25976，artifact-mcp25978。通过正常Cmd-Q退出，launcher退出码0，无强杀。

- 正式历史会话初始右栏关闭。按钮打开空状态，W1028默认右侧616 CSS px。
- 实际生成sample.pdf显示FEAT-165 normal PDF页面；sample.docx显示正常正文；sample.html显示普通交互报告且业务按钮禁用。
- 旧sample.pptx显示不支持：已核源fixture缺少真实页面关系，不能用其代替正文验收。新样本采用标准Office库生成12页PPTX。
- 分隔线键盘Home400/End627/Enter616正确；实际鼠标拖动616→516。10个标签后加号禁用；焦点手动移动、Delete及同次收起恢复有效。
- 跨操作曾观察到右栏和标签被清空，尚在诊断；不能将状态持续性记为PASS。
- 顶部两个原生外观按钮不符合设计token，已修正CSS，待候选构建和复验。

## 安全与未执行

未执行强杀、故障注入、二进制篡改、权限破坏、恶意资源/攻击测试。全量历史危险套件继续不执行。测试和构建仅标准canonical入口，不覆盖来源不明或发布二进制。D4、原NSD与完整来源×格式矩阵当前仍待验。

## 诊断与修复

- 诊断运行PID92534由canonical prepare→same-build reopen启动，正常Cmd-Q退出，launcher返回0。
- 临时只含布尔值的UI诊断显示`scope=false context=false enabled=false->true`，证明同会话临时readiness重新就绪会走原有清空分支。修复：scope/context变化仍清空；readiness变化仅暂停/重载。permission capability加入scope，撤权不能保留内容。新增回归测试覆盖暂停保留与撤权清理；23项相关测试PASS。
- 临时诊断UI已移除。窗口最小化后工具鼠标动作未稳定生效，此段不作鼠标/后台恢复PASS证据；使用正常退出和canonical重新打开复验，不强杀。
- 源码变更后的第一次直接reopen被same-build检查拒绝；保留失败日志，随后按canonical prepare正常重建，未绕过回执校验。

## 第1次授权提交与真实内容

- 当前累计1/2次。正式普通会话`01a18359-3f62-7a70-888b-aaaf9126c9a3`提交FEAT166_A，9个普通合成附件。UI实际完成80秒，12个publisher登记均staged且生成12个已就绪卡片；没有第二次提交。
- 初版合成PPTX包含python-pptx默认可选printerSettings.bin，PDF包含ReportLab默认ASCII85组合滤镜；原准入拒绝。已保留失败样本并生成无可选打印机二进制设置、使用普通DCT图片滤镜的合法文件，9个文件均通过既有prepare_paths。未放宽任何原有准入/安全预算。
- 临时本机纯读取诊断只输出样本名/Result，结束后移除测试；没有恶意fixture/故障注入/权限变化。单独TXT及完整9附件导入均已实际成功。
- 已发送compact.docx在右栏显示标题、两项列表、North/South表格及图片；已发送PPTX显示真实第1页文本和表格；XLSX显示合并格、shared string及缓存语义，但列宽过窄逐字换行，须修复。
- 原NSD作为第12个本地产物登记，85,749字节；实际新右栏显示NSD服务、统计概览及脚本生成的8条记录。AX确认搜索/导出disabled，滚动查看表格成功。原件未作为输入附件或正文发送。
- 原NSD进入完整publisher→Native提交→卡片→右栏链，不能将此写为原NSD已发送附件验证。此前最小HTML只作为普通对照。
- 阅读页码选择尚未生效，跨操作的标签仍出现清空；追加内容无关的临时事件诊断定位，D4保留未通过。
- App PID56436，标准same-build启动；任务结束后正常Cmd-Q退出，launcher退出码0。

## 已定位的生命周期事实

诊断运行PID24120观察到同一组件instance 1连续事件：`CLEAR scope=true context=true parts=false,true,false,true tabs=2`→`enabled false`→新context→同session重选。结合`chat/authorization.rs`的300秒context上限和store正常expiry/rebind，确认这是操作context自然续接导致标签误清空，而非用户换会话。产品权威R-07明确区分正常续接与身份/租户/权限权威失效：前者只保留同级历史标签元信息，旧内容立即释放，新context重新授权后恢复；后者仍清空。

PPTX页码并非阅读器失败：临时事件记录实际`navigate 9/0 → ready 9/0`、`navigate 1/0 → ready 1/0`，第10页和第2页图片均真实呈现；早先部分工具快照早于异步更新，不能据此写成已确认缺陷。表格列宽修复后实测Shared string、123、25.00%、2026-10-29、已保存公式3、无缓存公式提示均完整可读。

Wry新子视图默认focused=true；设为false，避免预览异步创建夺走主页面标签焦点。未新增权限或桥接。临时事件诊断已移除，24项前端定向测试通过；最终构建及fresh验收仍待完成。


## 弹层回归发现与修复

候选PID48890完成一轮格式、多标签与分栏交互：两种来源的HTML/TXT/MD/CSV/JSON/DOCX/PPTX/XLSX/PDF正文、原NSD 8条动态记录、扫描PDF、2.1 MiB DOCX分段、PPTX第10页及图片页、XLSX跨行列及工作表、PDF页码/150%缩放均实际呈现；10标签容量、同名异源、关闭邻居、收起恢复、拖动与键盘宽度、1180×760和200%降级亦通过。但PNG原查看器打开时，Native PDF覆盖弹层右半部，故本候选不能记D4通过。

修复为在原弹层检测中识别既有`aria-modal=true`及原生dialog，弹层打开时仅隐藏Native阅读视图，关闭后恢复，标签与阅读位置保留。增加普通组件回归；25项相关前端检查与lint通过。PID48890正常Quit后短暂显示STOP_PENDING，随后日志确认normal app cleanup complete，相关进程退出；没有强杀。最后验收须以此修复后的canonical构建重新运行。


最终PID92234于11:02—11:27执行fresh验收，普通失败恢复、原NSD、两来源正文、多标签、分栏、媒体弹层、亮暗/最小窗和持续输出通过；正常退出完成。后续新增3个普通合成媒体/HTML附件的批量UI导入观察不足，改用单个正常选择均成功，没有修改准入策略。最终结论、工具观察纠正和准确未执行边界见08。
