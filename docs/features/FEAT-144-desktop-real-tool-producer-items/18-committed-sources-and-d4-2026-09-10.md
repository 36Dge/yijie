# FEAT-144 来源固定与真实验收记录

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
