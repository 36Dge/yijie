# FEAT-144 配置兼容后的连接、权限与正常重开

> 本文保留该阶段的来源、结果、预算与未完成事项；当前原生拒绝和普通重开已完成，最终来源/分账/D4见[24最终报告](24-final-native-decline-and-delivery-2026-09-11.md)。以下“当前/下一步/未执行”仅指本文记录时点，不作为继续调用指令。

配置兼容阻塞已关闭。本次标准入口真实Tool成功、Sorftime正常停用、auto/full/ask切换、同一数据正常退出重开均PASS。D4仍未关闭：本修复来源下的原生Prompt正常拒绝尚未复验，旧B拒绝保持历史范围，不能替代fresh run。AC-004仍为用户排除，不实现、不验证、不算PASS。

## 来源与复用

- Contracts：`db54c617c65db5431b950eb297ba148a43a8e600`，本轮无变化。
- Host：`ccd815ff63542674daa80172a1c71ac7478edd0f`，配置兼容和日常回滚下限；之前分层修复提交`65f7b3212fbeb62b3b828cc1ca8997076f1f6b29`不含bootstrap修复。
- Desktop：`a5975f48e63d3f1d3a262e9e8dfc57ca0d923961`；最低SQLCipher reader仍为`25b004fbd5a4dcf642a503d302c21a7d6e3b817f`。本轮仅来源pin变更，无UI源码修改。
- Codex：`6c1ad767f0997845b8258a1c452fd4eb7577579f`工作区未改；固定0.144.6二进制SHA仍为`4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`。

继续复用原生MCP、elicitation、config CLI层、thread/read、FEAT-132唯一NativeDisplayBuffer和SQLCipher。Host使用已授权TOML库处理配置，不实现MCP客户端或trust状态机。精确模板、来源门禁及FEAT-152语义保留。细节见[21](21-native-config-ownership-2026-09-10.md)。

## 本次真实证据

使用com.yijie.ai原app-data、日常Host Home和CODEX_HOME，没有复制数据库或凭据。用户在canonical隐藏输入框启用本次Sorftime；新E任务首轮只有模型文字，没有Tool，第二轮经正常澄清出现实际原生Prompt，核对单ASIN和US后批准一次。Tool completed/414ms，两个Turn分别completed；原生phase缺失仍未分类，内容整体安全脱敏与原生完成分开。

正常退出后用同一Home的固定原生thread/read读取E历史，仅在内存对照/data/title、brand、price，均与界面回答一致。没有解析rollout，没有保存业务原文；仓内仅字段路径/摘要/匹配布尔。见[机器证据](evidence/connected-config-recheck-2026-09-10.json)。

用户明确授权当前E任务临时auto/full再恢复ask。第一次切换先正常停止原MCP Runtime，新的无MCP Runtime就绪；三种模式的界面与SQLCipher持久值一致，最终ask。受管配置不再含MCP server，原生trust原字节SHA保持`40838b962f2314c89af7f3942d187761ea28ca010de19d4bd6bef6e172c5764d`。期间没有新任务、工具或模型请求。

通过`pnpm tauri:demo-fast:app`再次标准构建/启动，E的同一已保存Tool保持身份、来源、completed、414ms、partial和安全文本；ask保持，旧审批回调未恢复。切换旧Command见failed/exit128及安全输出；旧Artifact仍ready，其隔离任务Host映射缺失如实保留；旧附件expired和清理未完成也保留。最后正常Cmd-Q，App/Host/Runtime均退出，launcher exit0，计数器正常停止。

## 调用与剩余范围

元数据12/20；MiniMax文本7/8；业务2逻辑调用，HTTP实际尝试次数未知，按原生每次可能重发一次保守扣4/10；图片0。初始化与目录分别记两次元数据，权限切换/重开/本地thread/read无新增外部调用。不能跨账使用余额。为正常拒绝及模型收尾已提出最多追加2次文本申请，未收到授权前不新增请求。

旧B的MCP冷任务续跑在本轮被拒绝，发生于模型/MCP请求前，保留本地outbox failed及无原生Turn记录。它不能由新E成功掩盖；没有自动恢复、猜测接管或自动封口。原生progress/outputSchema/annotations/phase缺失、冷历史不完整、Command完成后显示、旧附件/隔离映射限制不变。

D4未关闭，当前预算不足以稳妥覆盖新一次原生Prompt拒绝和模型收尾；不以到限拦截伪造失败，也不把旧B拒绝PASS搬到当前fresh run。此前UI多主题/最小窗口/200%等仍限于原验证来源与未变化的UI内容；本轮重新核验折叠、实际布局、历史和相关入口。没有攻击/故障注入、强杀、权限破坏、Runtime修改、推送、tag、部署或远端CI。

## 来源范围复核与本轮文档检查

实际`git diff 95afd425fd5b55ada9f13b43421ad2c06830dc5c..a5975f48e63d3f1d3a262e9e8dfc57ca0d923961 --stat`仅有runtime-permissions.lock.json，UI与Rust产品内容未变；因此原UI专项结果保留其准确来源，并结合本轮真实布局/历史/权限定向核验，不声称重跑了所有UI专项。当前native/MCP/权限源门禁、FEAT-137退役检查通过；strict/D0、元仓lint与50/50测试通过。D4实跑结论单独记录，不能由这些检查替代。
