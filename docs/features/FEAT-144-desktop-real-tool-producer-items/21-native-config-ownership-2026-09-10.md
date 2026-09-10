# FEAT-144 原生配置所有权兼容修复

配置兼容阻塞已关闭：当前Host ccd815ff63542674daa80172a1c71ac7478edd0f、Desktop a5975f48e63d3f1d3a262e9e8dfc57ca0d923961。新E真实Tool completed/414ms，原生返回三字段对照通过；Sorftime正常停用、auto/full/ask、原数据canonical退出重开均PASS。累计元数据12/20、模型7/8、业务2逻辑调用保守扣4/10、图片0；应用与计数器均已正常退出。D4尚未关闭：当前来源下的原生Prompt正常拒绝未复验，不能继承旧B结果；已申请最多追加2次文本，未获授权不调用。AC-004始终用户排除。 详见[22](22-connected-permissions-and-reopen-2026-09-10.md)。

用户已授权解决20所记问题并完成正常重开/权限切换，另增10次原生元数据操作；累计上限20，既有已用10。本地提交及必要修复授权沿用，推送未授权；模型4/8、业务保守扣2/10、图片0不变。

## 当前原生依据与决定

固定0.144.6的CLI与源码确认：app-server不接`--profile`，debug-only配置文件替换不作为产品方案；原生`-c key=value`覆盖支持app-server并保留base config。无密钥、MCP或模型调用的真实本地测试已验证：原生CLI受管模型/策略保持，原生thread/start自行写入trust，正常EOF重启后trust仍存在，两个Runtime均exit0。见[前置证据](evidence/config-ownership-preflight-2026-09-10.json)。

本修复采用原生CLI配置层：Host安全/Provider/MCP模板保存为独立精确受管文件，读取已校验字节生成固定原生`-c`参数；参数只有公开配置与环境变量名，不含凭据。Codex的`config.toml`只承载其原生projects/trust记录，继续由Codex决定项目根、信任写入与重载。Host不生成trust记录、不推断哪个目录应信任、不接管模型生命周期。

## 迁移与安全边界

本次`contract-impact=breaking`仅针对Host私有持久配置格式和native invocation；没有新增HTTP/SSE/IPC字段，不机械升级Contracts。既有FEAT-144安全/审批源契约不变。

- 仅现行MiniMax + RuntimePermissions的local路径采用新层；历史FEAT-137 profile及其严格门禁不改动、不激活。
- 旧config必须完整匹配已知受管模板的精确前缀；尾部必须经现成TOML库严格解析为原生projects及可选trusted/untrusted值，额外字段、类型冲突或无归属内容拒绝迁移。
- 提取尾部原始字节保留原生trust内容，先准备并精确验证独立受管文件，再用既有authority/文件身份/原子替换设施将根config保留为该尾部；不复制用户数据库或凭据，不清空trust，不接受任意projects扩展安全模板。
- 新布局的根config只允许受限原生项目记录，未知顶层/嵌套字段仍拒绝；独立受管模板继续逐字节校验、白名单源版本转换和临写前身份验证。运行前再次检查两者，不以CLI覆盖为借口接受危险/漂移配置。
- 受管参数沿固定原生CLI输入，既有thread权限响应、有效MCP配置、实际Prompt及秘密exclude/set校验保留。其它native系统/项目层仍由Codex加载，既有有效配置门禁保持。
- 新布局不能回滚到不支持分离配置的旧Host；最低Host回滚基线须固定实际兼容提交。Desktop schema15 reader基线不变。中途已有精确新受管文件但旧root尚未迁移时可正常继续；未知或不完整文件仍停止，不用重试覆盖。

用户已明确授权`go-toml/v2@v2.4.3`，固定模块校验和与官方tag来源已记录。它只解析/编码配置，不作为MCP客户端；没有自写TOML解析器。此前将“信息不足时询问”解释成所有新依赖均须另批属于过度解释，已向用户更正；其后收到的明确授权也已记录。

## 验证顺序

先以普通合成配置验证：旧模板精确前缀、原生trust字节保留、重复正常启动、MCP启用/停用模板转换、合法空与拒绝未知配置，不使用恶意/故障注入。再在同一固定Runtime做无密钥、无MCP/模型的真实thread/start与正常退出重开，证明trust继续由原生写入。

必要源码修复完成并分离阶段自审后，本地提交Host、更新Desktop真实Host commit/digest/pin并提交；Contracts/Codex不变。普通canonical读取现有数据和Tool历史，正常退出后以用户隐藏输入重新启用Sorftime。按台账预留初始化/单工具目录验证，不消耗模型或业务额度验证单纯切换。界面扩大权限时取得适用于当前验证的当场确认，正常停用后auto/full→ask，正常退出重开。D4依全部活动AC的实际结果决定，20历史失败保留，AC-004继续排除。


## 实施与来源固定（分阶段历史，当前以22为准）

Host已提交`65f7b3212fbeb62b3b828cc1ca8997076f1f6b29`，也是新配置布局最低可回滚Host基线；Desktop仅更新真实Host来源pin，提交`c784d842b59c063b4f357fce8445d9edb808370f`。Contracts db54c617c65db5431b950eb297ba148a43a8e600及Codex不变。三项新普通配置测试、Host FEAT144定向race/vet、模块校验与三项固定Runtime无调用集成通过；审查后再次验证有效MCP配置、正常停用重启和trust字节保留。首次集成发现原生CLI不解引号key路径，已按固定native语法改为受限bare segments后通过，未修改Runtime。详见[实现与审查证据](evidence/config-ownership-implementation-2026-09-10.json)。

当时开始普通未启用Sorftime的canonical构建/重开验证；使用原计数器4/8上限，不重建预算。元数据10/20、业务保守2/10、图片0不变；尚未将本轮产品重开或D4标PASS。


首次普通canonical实际迁移保留两个trust条目，但启动器工作目录为已被原生信任的Desktop仓库，固定Runtime因此加载该仓不支持的workspace配置并退出。已以相同真实Home、相同配置，仅改变bootstrap cwd的无调用对照证实：仓内初始化失败、中性根目录初始化exit0。Host追加`ccd815ff63542674daa80172a1c71ac7478edd0f`，Desktop pin追加`a5975f48e63d3f1d3a262e9e8dfc57ca0d923961`；新配置布局的日常回滚下限以该Host为准。实际任务仍传入原cwd并加载其项目配置，既有不支持workspace的任务目录限制没有绕过。三项无调用集成与来源检查再次通过，当前第二次普通canonical构建中，证据见[native-bootstrap-cwd](evidence/native-bootstrap-cwd-2026-09-10.json)。


修复后普通canonical实际PASS：同一app-data/Host Home/CODEX_HOME正常启动，旧FEAT144-D4-B两个Tool已重开，342ms成功及0ms拒绝、原生观察来源、脱敏/缺结果语义保留；模式ask。原模板+现root尾部重新合成的摘要等于原ab41...，证明trust原字节保留。Cmd-Q正常退出且所有受管进程消失，计数未增加。详见[canonical证据](evidence/config-ownership-canonical-2026-09-10.json)。当时准备Sorftime隐藏输入后的真实连接/停用（现已完成，见22）；D4暂不关闭。


本次最后检查：Host make lint、模块校验、定向race及三项原生无调用集成通过；元仓strict/D0、lint及50项测试通过。没有运行受禁止的全量故障/攻击测试，没有推送或触发远端CI。阶段检查点（已由22取代）：标准Sorftime构建已完成、隐藏输入等待用户；计数器4/8沿用原台账，新10次元数据尚未使用。

## 当前真实连接复验

当前配置兼容修复已本地提交：Host ccd815ff63542674daa80172a1c71ac7478edd0f、Desktop a5975f48e63d3f1d3a262e9e8dfc57ca0d923961。普通canonical重开旧B任务已通过；用户隐藏输入后，新E任务真实Tool completed/414ms、两轮均完成。累计元数据12/20、模型7/8、业务2逻辑调用保守扣4/10尝试、图片0。本次E模式切换与正常重开已通过；不再等待密钥或切换授权。D4尚未关闭，AC-004继续用户排除。

新E任务首轮模型只用聊天文字请求权限，未调用工具；明确原生工具schema后第二轮产生真实Prompt，核对ASIN/US并批准一次。它没有使用聊天确认替代原生审批。原任务B的冷启动提交在模型/MCP调用前被拒绝，保留无原生Turn绑定的本地失败投递，不自动续跑或补封口。新E事实已保存于原SQLCipher schema15/view2；显示partial与原生completed分别保留。原生返回三字段已在正常退出后经thread/read独立对照通过，不另建保存/历史重建链。
