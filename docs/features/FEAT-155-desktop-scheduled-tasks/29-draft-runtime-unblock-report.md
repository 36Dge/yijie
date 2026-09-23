# FEAT-155 · 受限草案 Runtime 阻塞修复报告

2026-09-19。**阻塞已解决，限定于本轮精确本地候选。** 已实现原生input-only限制、stable实际策略查询、同源Contracts投影及原Host资格接线，并通过真实候选Runtime正常生命周期检查。旧固定产物的[27：NOT QUALIFIED](27-phase-3c-3b-3a-qualification-report.md)结论仍成立；本报告不是把旧产物改判为合格。

整体FEAT-155仍在实施中：阶段一、二及第三阶段至B1/B2已有候选代码，当前越过受限草案执行前提的阻塞。**B3B原生装配/草案恢复、页面、防空闲睡眠与真实Provider及Must验收尚未完成，D4 NOT RUN。** 普通Desktop schema15/Host Store5和显式候选22/6保持，日常用户库未访问或迁移。真实文本调用仍0/12，图片/商家/MCP外部调用0。

## 1. 根因与实际解决

旧Runtime的`read-only`仍有任务读权限，空MCP map不等于消除多层继承；指令、hooks、skills、plugins及工具注册发生在多个阶段。旧stable响应不能证明最终无工具、无额外指令和无任务读写权限。继续添加Host布尔开关或提示词不足以关闭缺口。

依照用户“实施解决方案，直到解决”的最新授权，实施[28执行定义](28-draft-qualification-unblock-execution.md)和[ADR-0020 DEC-155-09](../../adr/ADR-0020-local-scheduled-task-authority.md)。采用同一Runtime中的通用限制，不新增定时业务、第二执行服务或用户权限模式。具体技术选择由Codex在任务范围内作出，没有另行虚构用户逐字段审批或独立人工评审。

| 边界 | 实际实现与验证 |
|---|---|
| 额外指令与初始化 | 在文件解析/发现前去掉继承指令、模型/compact指令文件、角色文件、远端thread config；关闭AGENTS、skills、hooks、plugins/MCP/扩展、memory、shell snapshot和startup prewarm。Host显式草案说明保留。 |
| 文件与网络 | 原生有效权限为受限文件系统且无task roots、tool network关闭，审批never；线程自己的内部历史持久化和既有文本Provider通道保留，不能称为整个进程不读盘/不联网。 |
| 工具与输出 | 原生工具计划直接返回空可见集合和空可执行registry，包含hidden/deferred；请求`tool_choice=none`。非文本输入、非生命周期操作及放宽权限更新拒绝；非文本模型输出在item处理前失败，不通过unsupported-tool分支触发模型续调。 |
| 实际证据 | 新stable只读`thread/inputOnlyPolicy/read`读取已装载线程的有效snapshot、instruction sources和MCP配置；普通线程返回null。证据与固定原生执行分支共同证明约束，不只回显请求配置。 |
| Host闭环 | 原Manager/stdio/thread/turn及原operation互斥保持。准入核验精确产物、受管Provider配置、generation与不兼容能力；创建/恢复校验实际thread/cwd与全部策略事实；每轮再查回执、校验workspace/generation。正常关闭后旧generation失效，冷恢复重新取证。 |
| 契约 | 先Runtime源码/269份canonical schema，再Contracts机械生成Go/schema/pin，再Host消费。缺字段、未知字段、null工具数组拒绝；旧公开Host wire和草案outputSchema保持。 |

## 2. 精确来源与兼容方向

整体按`contract-impact=breaking`保守审查，原因是新原生能力及精确artifact/schema pin改变下游资格解释。旧产物继续支持普通会话；新请求只向已匹配的新候选发出，不对旧Runtime试探调用后降级。

- 上游：`rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d`，未升级。
- 活跃基线：`b2b20e2fc4a0c94834f34d8cc459e488a1b56277`中的FEAT-126/136两补丁；新补丁`input-only/0003-input-only-execution.patch`，SHA-256 `c340b6fc17419bcdc1ff45eebe3da40e5fde740c029102eb7a188f6b14eb41d8`；FEAT-137继续永久退役。
- 最终binary SHA-256：`bd7d26205e2d735dcac0f35fc089a7b30a5c18a54586b94a2c7f624f2f5b7672`，356184808 bytes，macOS Apple Silicon。
- 最终manifest SHA-256：`14d4073de87be137cf39f770c091b8ab62a7c34933bc49dc50f12b4ddd3a494a`。
- stable schema：269文件，tree SHA-256 `34d353815dc8d800cb432a876d5b43350511f63b91ad9766f861e8bc8290cc92`，stdio、experimentalApi=false。
- 新产物目录：`yijie-codex/.yijie/build/input-only/aarch64-apple-darwin/`；旧Host `.local/runtime-artifacts/feat-136-b2b20e2fc4a0`的binary/manifest摘要均与起点固定值一致。

[来源证据](evidence/draft-runtime-unblock/final-provenance.json)、[schema差异](evidence/draft-runtime-unblock/schema-compatibility.json)。相对旧267文件：新增查询参数/响应2文件，3个请求/协议聚合文件增加新方法，其余264文件逐字节不变，没有修改旧独立响应schema。默认`input_only=false`以及同进程普通会话通过定向验证。

构建从固定Git对象物化临时工作区，按精确顺序重放补丁，使用Rust1.95.0及offline Cargo和既有lock漂移校验；`codex-rs/`原样源树保持。`make input-only-build`是本候选canonical入口；未执行仍含退役补丁的历史default build/test入口。可按固定来源重建；没有宣称不同临时路径下的独立release构建字节级一致。

Contracts源锁记录native schema/patch/build脚本/generator摘要，Host生成快照逐字节一致。本地dirty候选不是生产发布引用；没有新增tag、提交、推送或consumer Owner人工签字。未来发布仍需固定不可变提交与适用发布门禁。

## 3. 实际检查

完整命令、退出码和日志索引见[checks.json](evidence/draft-runtime-unblock/checks.json)。

| 检查 | 结果与证明范围 |
|---|---|
| 原生定向core测试 | 4/4 PASS：继承源与权限封闭、普通默认保持、可见/可执行工具均空、非文本输出拒绝。普通合成数据，不执行攻击fixture。 |
| 原生构建/格式/schema | 最终canonical release build PASS（8m22s）、19份变更Rust文件fmt PASS、269份schema生成/完整tree校验PASS。 |
| 最终Host race | 14/14 PASS，包含真实候选正常create/两轮文本/退出重开/resume、普通会话共存，以及缺资格I/O前拒绝、用途隔离、重放、HTTP producer与旧权限路径。 |
| 真实原生 vs Provider | 使用真正的候选binary和原Host transport，无二进制替换/伪装、无test artifact policy绕过。最终测试2次本机HTTP文本fixture、MCP请求0；草案固定schema和tool_choice在实际请求中检查。真实MiniMax NOT RUN，不能把fixture输出质量作为Provider资格。 |
| Contracts | 同源生成/同步/check PASS；新原生族与既有草案族8/8 PASS；全仓pnpm lint退出0（12条已有Redocly warning）。 |
| 兼容基线 | fallback `db4458fe94572c4df41a114005d54a049bb79b1f`、已发布 `f16a497e1377f45747f8ff9292b4b60cf2027f88`、native `6f632f155eacdaf93df0e0b00b5dab9e369c5442`及`811f38d6b104fa18477107e7ac91a85e19c445d1`的结构breaking检查全部通过；不将结构通过当语义或生产验收。 |
| 其它检查 | Host scoped vet、脚本语法、元仓strict/D0/audit-claims与治理检查、五仓diff/status/起点文件审查单独记录。 |

开发中修正过一次`Option`误用的编译失败；日志保留为`policy-check.log`，最终编译通过。自审又发现角色文件/远端配置加载和unsupported-tool自动续调缺口，修复后分别重新构建；最终证据以`canonical-build-output-boundary.log`及`host-final-native-focused.log`为准，中间build不是最终候选。构建存在上游app-server `unused_mut` warning，未无关修改或冒称warnings全清。

本轮真实模型累计0；中间和最终原生集成各2次本机HTTP合成文本请求，共4次，没有外部Provider/MCP请求。临时目录由测试创建，所有受管Runtime正常关闭；停止超时会保留所有权/目录并报告，不强杀。

## 4. 结构化自审与范围保护

主代理复核了配置合并、初始化加载、原生输入/更新/输出边界、工具registry、回执严格解析、Host互斥与generation、源锁及artifact准入。修正StartTurnV2已有互斥下重复加锁的问题，最终正常两轮真实链路与race检查通过。未委派子代理、未声称独立人工评审。

[工作区审查](evidence/draft-runtime-unblock/workspace-review.json)记录起点与末尾HEAD/branch/remote、变更文件和摘要；已有工作区改动保留，Desktop起点文件逐字节未变。Runtime原样上游和现役两补丁未变；新产物是独立可重建项目输出，未覆盖用户固定产物。没有修改数据库schema、定时算法、三种目标、额度规则或默认产品入口。

未执行含强杀、权限破坏、危险/攻击fixture的历史全量套件，也未执行真实模型、日常库迁移、Keychain访问、签名打包、UI/系统通知/电源及D4验收。原因分别是用户硬性禁令或不属于本轮资格阻塞修复；影响是本报告只建立本地候选Runtime与Host资格，不建立完整产品/Provider/平台验收结论。

## 5. 回到需求主线

当前缺口从“Runtime受限能力无法证成”转为**既定B3B原生装配与草案恢复尚未接通**：统一候选装配、原生draft transport、正常重开后的来源重发现/unknown查询及失效处理。随后才是定时任务页面、两种创建入口和三种运行目标的完整使用路径，再完成防空闲睡眠、应用内更新及限额内真实Provider/Must验收。

这仍沿[26列明的B3B后续范围](26-phase-3c-3b-3a-qualification-plan.md)推进，不另建调度器、不恢复已延期的系统通知。缺资格、配置变更、旧产物或不完整回执继续拒发。回退时先停止新草案生产，保留兼容reader及历史，使用正常退出，不把数据库降回旧格式。本轮没有自动铺开后续页面实现。
