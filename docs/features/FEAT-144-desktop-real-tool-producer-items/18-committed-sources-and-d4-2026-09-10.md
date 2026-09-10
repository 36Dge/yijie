# FEAT-144 来源固定与真实验收记录

当前结果以[20](20-d4-permission-restart-blocker-2026-09-10.md)为准：真实查询/拒绝及返回值核对已完成，权限重启被受管配置门禁阻断，ask保持，D4未通过。以下按阶段保留历史，当时预算和等待输入不代表当前状态。

本地来源已按授权顺序提交，未推送、未打 tag、未部署。当前仅源码、兼容 reader 与安全定向检查通过；canonical 构建及来源门禁已通过，应用启动和真实 D4 尚未完成。历史检查保留原适用范围，AC-004 为 OWNER_EXCLUDED / NOT RUN，活动9项 AC 尚未关闭。

| 仓库/阶段 | 完整提交 |
|---|---|
| yijie-contracts | db54c617c65db5431b950eb297ba148a43a8e600 |
| yijie-agent-host | 31ee71889f83aff53dce6eeacd4b5ca4fd319c6b |
| Desktop 最低兼容 reader | 25b004fbd5a4dcf642a503d302c21a7d6e3b817f |
| Desktop 最终 writer/展示 | 9455179cac3772972dc19d16cd8dee3a5b95806f |
| Codex 未修改 | 6c1ad767f0997845b8258a1c452fd4eb7577579f |

reader 的实际提交树经过生成、TypeScript 类型检查及3项正常迁移/格式隔离验证，保持 writer=1/read=2。最终 writer=2 后于该 reader。回滚下限为该 reader，不能回到不认识 schema15 的旧程序。

Contracts 生成入口变更触及旧原生/权限来源摘要，因此更新真实锁；旧权限源规范语义没有改变。保留 FEAT-152 的完整 Host 构建源码校验。新 native v2/SSE v8、旧 v1/v7 各有真实消费者，兼容出口继续保留。

提交后的补充检查：Desktop 文档构建、cargo fmt、clippy lib -D warnings、4项 FEAT-144 Rust 测试通过；Host 定向 race、真实 MCP/权限来源检查、元仓 strict/D0 通过。clippy 首次发现条件可合并，已按同样条件修正并复测；不增加绕过项。详见 [完整来源证据](evidence/committed-sources-2026-09-10.json)。更早实现测试见17；未执行的攻击/故障注入测试不记PASS。

调用累计为业务0/10、元数据8/10、模型0/8、图片0。按本次授权通过既有计数器限制模型请求。正常入口使用普通 com.yijie.ai 身份及既有 app-data，Host Home 为日常 .local/demo-fast/host-home；不复制用户数据库。启动前核对进程与数据目录，仅在一个新验证线程启用 Sorftime，初始化与目录核验各消耗一次剩余元数据额度；重开不重新启用 Sorftime。

标准 canonical 构建已完成，当前停在系统隐藏密钥输入框，等待用户亲自输入。该输入属于既定仅内存秘密路径；不从聊天、磁盘或剪贴板取出密钥代填。模型计数器已就绪且0/8，未启动新模型或MCP操作。后续用户输入后继续实际应用与D4验收，不重复构建或消耗已验证连通性的额度。来源提交、日常启动、真实 D4、推送分别记录，任何阶段不代替其它阶段。


元仓来源记录提交为 `1b4b86b39d7004b87b590365ddb00803a225f9be`。标准构建的实际产物身份/摘要、秘密输入等待点及未运行范围见[canonical 构建检查点](evidence/canonical-build-and-input-checkpoint-2026-09-10.json)。应用尚未启动，因此用户数据前向迁移、正常退出重开、Tool成功和原生Prompt权限验收均不记PASS。


## 首次启动后的发现与修复

用户已完成隐藏输入。应用/Host/固定Runtime启动，healthz与readyz分别为ok/ready，但UI绑定报chat_host_not_ready，一次正常界面重试仍未恢复，未发送模型或业务请求。随后Cmd-Q正常退出，全部受管进程退出，计数器也正常停止。

凭据为空、无thread/start/工具列举的固定Runtime本地config/read证明：有效配置会补充environment_id=local和默认null字段，并省略supports_parallel_tool_calls=false。原校验错误地比对输入TOML形状；Host修复为精确匹配真实有效配置，不能把未知/空feature当false。另限制Sorftime启用时仅因读旧历史不自动恢复每个旧线程；存在旧活跃绑定时保持拒绝，先用普通入口正常处理。未启用Sorftime的FEAT-152恢复保持原行为，不改写旧Item/Turn状态、不猜身份。

必要修复本地提交：Host `635846f72ef4b0d940798215e7b79d58aed6c591` → Desktop `95afd425fd5b55ada9f13b43421ad2c06830dc5c`；Contracts源和最低reader不变，仅同步真实受影响Host pin。Host race/vet、Desktop fmt/clippy和5项定向Rust检查通过。当前进行不启用Sorftime的普通canonical验证；业务0/10、元数据8/10、模型0/8、图片0，D4不记通过。详见[实际失败与修复证据](evidence/canonical-startup-fix-2026-09-10.json)。


普通未启用Sorftime入口已通过：任务列表/Composer就绪，既有Command两种终态和安全输出可读，既有图片Artifact真实预览成功；旧附件过期、删除清理未完成、隔离历史缺Host权限映射均保持原提示。通过原生picker选择新合成scenario-project，未发送任务。再次Cmd-Q正常退出，Desktop/Host/Runtime均退出，进程exit0。源修复后的Sorftime入口正重新构建；之前输入的密钥随正常退出清除，需要用户在新隐藏框再次输入。全部调用计数不变，仍不关闭D4。


最新真实进度见[19](19-real-d4-progress-2026-09-10.md)：普通canonical已完成一次真实MCP调用和一次原生Prompt正常拒绝；元数据10/10、模型4/8、业务1次逻辑调用保守扣2/10尝试、图片0。UI/旧历史定向检查通过，权限停用与重开/独立返回值核对仍待完成；D4未关闭，AC-004仍排除。


## 权限切换与本轮结束

用户已授权当前FEAT144-D4-B临时切换并复原。auto切换触发旧Runtime正常退出，但原生projects信任写入使受管模板精确校验拒绝重启；权限持久值仍ask，full未尝试。已正常退出App/Host/Runtime和计数器。原生thread/read核对业务/data三字段与模型回答一致，SQLCipher保存事实存在，普通Tool重开尚未验证。元数据10/10、模型4/8、业务保守扣2/10、图片0。详见20及机器证据；无产品源码/来源锁新修改，无推送。
