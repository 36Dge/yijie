# 第四组：人台换模特图专家与 LinkFox 接入

2026-10-17（Asia/Shanghai）。用户要求完整回顾审计方案，继续剩余4位中的下一组；严格复用现有专家架构，保留原专家与历史，完成深入代码审计和全量lint；没有账号的真实验证继续跳过。

## 回顾与范围

复核17原审计的全部九节、执行/打包/逐专家内容笔记及18—22的前三组结果。当前为7位原生专家、4位展示专家；48资源（38普通+10专家版本），59连接器，单专家会话、SQL35/Host10、既有outbox/审批与精确引用保持。原计划为“LinkFox先单图，再视频，再多源1688”；本组只推进人台换模特图专家，剩余视频/1688/行业研究后续继续。重新核对剩余4位共171份原始文件，导出和WorkBuddy缓存与摘要全部一致，无额外文件；原包不执行、不修改。

原包核心是图文提词→异步生图→查询结果，不是仅咨询。新增固定LinkFox OAuth MCP连接器、受管专家资源和无网络本地参数/结果核对工具；外部创建/查询仍由既有MCP发现、schema冻结、会话选择、逐次审批和Tool结果持久化负责。用户明确无账号，真实授权/发现/付费生成/模型/客户端D4均NOT RUN。

当前公开HTTPS图片URL可进入该流程；本地图片到公开OSS的原包PUT脚本不纳入，现有ask会话网络关闭，不能切full或让模型绕开Connectors上传。没有已批准的安全上传能力时明确要求用户提供已授权的公开HTTPS图片直链；结果交付为实际返回的图片链接，不假称本地文件。此边界在专家描述/参考中明示，完整本地素材上传与自动媒体下载仍未接入，不能声称原包所有能力完整可用。

## 协议与兼容决定

`contract-impact=breaking`：目录及安装快照需要59→60容量，新60项生产者不能与旧59项reader混装。仅market-connectors未发布族0.4.0→0.5.0的两个Snapshot数组maxItems改变；每轮选择仍58。源契约先生成并同步Desktop/Host/Connectors后再增加第60项目录。现有专家v3、OAuth、安全存储、权限、审批、Runtime与数据库schema不改。资产新增0.1.0，原48资产与全部精确历史引用保持；回退须保留兼容reader和旧资源，不覆盖安装或清理历史。

LinkFox原包固定MCP资源为 https://mcp-tool-gateway.linkfox.com/mcp/any-tool 。本次无凭据GET返回401与同源resource_metadata；根well-known返回资源基址/mcp、issuer https://tool-gateway.linkfox.com、scopes mcp:read/mcp:invoke。授权服务器公开metadata声明相同issuer、DCR、PKCE S256及public-client none；原DiscoveryPolicy已支持同源资源基址包含endpoint路径，无需放宽或按专家名称加例外。尚未执行注册/授权/工具发现；工具模型枚举、业务schema与真实质量未在线确认，源包矛盾需在调用前按当前已资格化工具核对，不默认降级模型。

## 实施与验收要点

1. 单一根SKILL/ROLE与任务索引；删除默认反馈外发、WorkBuddy授权、缺失wrapper、自动重试和已落盘假设。
2. 图像顺序、衣款视觉锚点和补全规则明确；显式模型/比例/分辨率，不靠未知枚举回退。
3. 本地辅助脚本仅构参/解析MCP回执/核对taskId；不联网、不上传、不轮询、不创建业务权限。交付JSON是可核对工作产物，原生Tool历史仍是执行事实。
4. 创建与查询分离；PROCESSING不能报成功，错误/空结果/未知任务不能触发重建。文本内容和单图URL必须源于对应实际回执。
5. 所有原资源/安装/历史保留；新资源安装、精确引用、UI召唤/预填和未授权拒绝均用正常本地测试。
6. 各受影响仓全量lint、canonical生成一致性、当前Host来源冻结、代码复审完成；真实部分标NOT RUN，不作D4或模型质量结论。

证据根：Desktop `.local/fourth-group-mannequin-20261017/`。基线记录7仓HEAD/分支/origin/status、diff和源码摘要；不提交推送、发布，不启动/替换正在运行的产品进程。


## 深入代码复核与修复结论

本次由同一 Codex 执行实现后的独立复读，不冒称独立人工或多 Agent 审批。对新增14份运行资源、21份原始资源及跨仓增量逐层核对；已有通用层只复核相关调用路径，不把整个 Runtime/所有历史代码声称为本轮逐行重审。

| 层 | 核对的实际实现 | 结论与限制 |
| --- | --- | --- |
| 原资料 | Agent、四个子技能、字段/流程参考、模板、helper、上传脚本、plugin/README/meta；171份剩余来源文件摘要 | 人台原包21份与导出/安装源一致。缺失wrapper、旧模型枚举、默认反馈、任意公开PUT和“结果即本地文件”均未照搬。 |
| Skills | `mannequin-to-model/ROLE.md`、参考、`scripts/prepare_mannequin.py`、例子/checklist/eval | 单入口、14份明确package_files、Python标准库；无HTTP库/凭据读取/后台任务/自动安装。素材顺序和模型组合先检查；结果缺失、业务错误、MCP错误、任务错配不当成功。辅助JSON不构成执行权威，历史Tool回执是事实源。 |
| 生成链 | canonical packager → authority/manifest → Desktop assets pin → Host `ReviewedExpertCatalogDigest` → canonical source freeze | 49资源、11专家版本；原48项manifest与archive逐项保持。未手改生成类型/摘要绕过门禁，不修改v2普通Skills槽。 |
| Host | `internal/skills/experts.go`、`internal/session/expert_resources*`、`internal/codex/expert_instructions.go`/`market_runtime.go` | 继续精确ROLE/知识摘要、原安装收据、单专家绑定、Core journal/outbox和retained保护。生产逻辑只更新reviewed bundle pin，无新任务表/Runtime修改。角色不能扩大当前权限，web_search仍关闭。 |
| Connector注册/授权 | fixed registry、`providers.rs`、`oauth_policy.rs`、`tushare_oauth.rs` | LinkFox作为第60项OAuth服务，不使用WorkBuddy请求channel或登录态。公开resource `/mcp`可涵盖同源endpoint `/mcp/any-tool`是现有策略；issuer精确相同，未加域名例外。DCR/PKCE/Keyring仍走原实现，真实账号流程未执行。 |
| 工具发现/执行 | `generic.rs`、`broker.rs` | 动态完整schema资格化与冻结、服务/安装/revision/generation精确绑定，所有未知风险按write逐次批准；拒绝0执行，批准1次，重复consume拒绝，其他服务0执行。没有重试器/无限轮询/图片二进制通道。代理内部业务枚举只能由当前远端schema/官方说明确认；本地例子不是在线资格。 |
| Native/UI | `skills/catalog.rs`/`experts.rs`、connectors store、Native catalog integration | 真实Native目录8位+独立展示3位=11位，无专家团；原头像映射/三列tokens保留。同ID展示卡移除，读取旧目录或失败时不伪造已接入卡片。快捷问题只预填，原准备/选择/显式发送不变。LinkFox未授权时required/disconnected、不能启用。 |
| 数据/权限 | SQL35/Host10、ask权限、已有资源目录与runtime历史 | 不迁移、不打开日常数据库写入，不安装到日常用户目录，不切full，不改变进程/二进制。现有已安装9个专家版本与相应canonical archive文件逐一匹配。 |

真实包加载检查曾发现本轮新增 `reviewed_at` 使用 `+08:00`，Native既有 `valid_date_time` 仅接受UTC `Z`。修复为同一时刻 `2026-10-16T16:00:00Z`，重新canonical打包、同步pin、冻结Host来源；保留初次失败日志，4项Native检查重跑全通过。未扩大Native允许格式或降低验证。`FAILED + errorMsg`按明确失败解释，返回taskId只记created，均有普通输入回归覆盖。

本地helper对URL只作语法检查，不证明公开可读、许可或图像内容。临时签名URL不持久化到该辅助产物，不擅自删query；原Native工具历史仍保留实际回执。真实业务如果只提供临时签名结果，需要在该原回执边界交付并另行审阅下载能力；不能宣称本版已自动保存图片。视觉保真仍需实际素材和模型结果验证。

## 最终检查与证据

证据均在本文件开头的Desktop证据根。所有本地测试使用普通合成数据、临时/内存数据库或in-process MCP；不是供应商真实验收。

| 检查 | 结果 / 证据 |
| --- | --- |
| Desktop全量lint | PASS，`make lint CONTRACTS_DIR=.local/demo-fast-contracts`，含完整生成一致性、ESLint零warning、vue-tsc、cargo fmt、all-targets Clippy；`desktop-lint-final.log`。沿用工程已有干净历史Contracts源校验旧Public/Host不可变对象；当前新协议检查仍直接读取实际sibling。 |
| 当前来源/权限链 | PASS，canonical source freeze后，`check-agent-host-v4-contract`、`check-approval-retirement`、专家49包与普通38包check；`current-preflight-final.log`。既有FEAT-137历史acceptance NOT PASSED未改写。 |
| Host | 全量`make lint` PASS；实际最终49包、11版本安装/读取、原39包升级保留、Core生命周期及3组旧新版本共存4组race测试PASS；`host-final.log`。 |
| Connectors | 全量`make lint`、catalog race、worker完整来源/格式/Clippy PASS；`connectors-checks.log`。新增两个Rust测试文件另做rustfmt check。 |
| 正常MCP/审批 | 6项PASS：公开OAuth metadata策略、五次手动异步阶段调用、LinkFox和旧Sorftime精确绑定及一次审批、60项registry、普通Bearer header模式；`worker-functional.log`。合成服务不证明实际账号/模型/费用可用。 |
| Skills | 全量lint PASS；33测试与72条合成eval结构校验PASS；`skills-checks.log`、修复后`skills-tests-final.log`。包含8项新helper行为测试，不包含真实模型评分。 |
| Native | 4项PASS，实际包加载、8位最新目录/精确引用、60项无secret目录、60安装快照及未授权不能启用；`native-functional-final.log`。旧失败留在`native-functional.log`。 |
| UI/构建 | 4文件77测试PASS，`ui-functional.log`；`pnpm build` PASS，`frontend-build.log`，既有大chunk提示保留。仅前端产物与测试编译，未重建/替换运行中的App。 |
| Contracts | 全量`make lint`及market-connectors专项12 Node、6 Rust、Go conformance、Clippy PASS；`contracts-checks.log`。canonical generate/sync源优先完成。 |
| 元仓 | pnpm lint、50 manifest测试PASS；`meta-checks.log`；最终diff检查和状态清单另存。 |
| 保留性 | 原48manifest项/archive逐一相等、原59 catalog/provider值不变；9原Runtime会话文件、110原安装资源/收据摘要不变；当前已安装9专家版本逐文件匹配新包中的历史archive。`preservation-final.json`。数据库动态/WAL不以文件摘要冒称全量重验。 |

全局兼容检查重新执行：`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1` PASS；`1a213ac8383e95ac6ec69363937687904fa3591c`、`35e0949c95d7a59ca5480715c225766dcc822056`、`e35ae9a0711014e4774a1347413e9a343ce7ab2c`仍在旧scheduled-plan-draft远程引用 `https://schemas.yijie.ai/scheduled-tasks/draft-execution/v1` 返回EOF处exit102。没有跳过该检查或标为PASS，记录在`breaking-results.json`。随后单独执行这三基线的Buf/AsyncAPI/JSONSchema，9项PASS，仅补充覆盖，不替代全局阻塞。

`capacity-source-conformance.json`确认相对本组开始时0.4.0源，只有version和两个maxItems改变；旧59 reader拒绝60、新60 reader接受58/59/60，61仍由专项测试拒绝。此为明确breaking、全consumer同步的本地候选，不能宣称发布兼容全部通过。

## 固定候选与后续边界

- `bundle_version=0.8.0`，输出`yijie-skills/dist/skills-experts-fourth-group-v010`，49资源=38普通+11专家版本，8位最新原生专家。
- manifest SHA-256：`70f3aa77bddc4ed685c7b34738106f5cae0e42ee7d6542520a767a9fb683f200`。
- authority SHA-256：`95a1da7b151f7d669f175b25058c2c92be984c771605f50b507a9ed30befed67`。
- 资源源树SHA-256：`0ba9997a040c0ed500596d423b2b80ad53eed59aa42cc1a711aa45d6fc5fe237`；expert Contracts lock SHA-256：`fe49fb6cd83e11dba69861025a23a8faf1d9d3740c887c1716a3637eb34154cb`。
- Desktop/Host pin与实际canonical包相同；这些是`release=false`工作树候选，不是发布tag或不可变Git集成提交。当前运行中的易界App未替换，因此本轮源码目录数量不等于已运行App画面已经更新。

NOT RUN：真实LinkFox DCR/登录/安全存储写入、tools/list资格、模型/额度/收费任务、真实图像效果、真实取消/网络异常恢复、App端到端D4。原因：用户明确无账号并要求跳过真实验证。影响：可以确认现有架构接入和本地协议/资源链，但不能宣布LinkFox实际可调用或衣款保真质量合格。原生图服务与本地文件上传/自动下载是不同完成项；后两项尚未实现，UI/角色均明示。

用户禁止的强杀、权限破坏、可执行文件替换/劫持、恶意资源及攻击fixture、危险归档测试均未执行；未运行包含这些历史场景的宽泛测试目标。没有伪造相关异常验收，没有提交/推送、发布或改动Runtime源码。

剩余3位：跨境电商爆款视频复刻专家、亚马逊1688找货源专家、行业研究员，继续维持展示态。按原依赖顺序继续复用本组LinkFox入口审阅视频/1688；不能据本组单图合成协议测试替代它们各自的业务适配和验证。原出海匠issuer精确匹配阻塞记录仍保留，本组没有静默放宽OAuth策略解决它。
