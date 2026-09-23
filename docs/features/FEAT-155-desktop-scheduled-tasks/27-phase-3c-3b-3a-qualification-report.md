# FEAT-155 · 3C-3B3A 受限草案执行资格收口报告

2026-09-19。按用户授权执行[26方案](26-phase-3c-3b-3a-qualification-plan.md)后停止。**调查已收口，结论是 NOT QUALIFIED，不能放行真实草案。** 已核对固定产物、配置加载与能力边界，并完成零真实调用的定向验证；没有修改 Host、Contracts、Desktop 或 Runtime。第三步的 Host 修正以“stable 证据完整”为前提，本次未满足，因此没有实施。

本轮 `contract-impact=none`：只保存调查、检查证据与未批准的决策建议，没有改变 wire、持久化或运行行为。完整 FEAT-155 的 breaking 分类和既有 D0 范围不变；普通 Desktop SQL15 / Host Store5、显式候选 SQL22 / Store6 保持。Provider 资格、正常原生装配与 D4 均 NOT RUN。真实文本累计 **0/12**，图片、商家及 MCP 外部调用均0。

## 1. 四步执行结论

| 步骤 | 本轮结果 | 结论边界 |
|---|---|---|
| 固定产物与配置来源 | 已核对 binary、manifest、两补丁、来源 Git tree 和267份固定 stable schema；梳理 Host 受管配置、目录和请求覆盖链 | 来源检查 PASS；未执行二进制、未读取用户日常配置/库/Keychain，不冒充活进程采样 |
| 核实受限能力 | 完成下述权限/工具矩阵及87个 stable client method 的相关查询能力复核 | 已有部分有效控制；当前输入配置有具体缺口，最终线程权限/工具和初始化边界仍不能证成 |
| 最小 Host 修正 | **条件不成立，未修改**；保留实际 `ScheduledDraftReady() == false` | 没有只修空 MCP map 或旧键后就解锁，也没有堆叠仍永远拒绝的新候选代码 |
| 零调用验证与决策 | 11项 Host 定向 race 回归、scoped vet 与文档治理检查完成；形成 DEC-155-09 建议 | 进程内 fixture 只验证用途、幂等、存储与拒发，不作为真实 Runtime 隔离证明 |

这不是“Runtime 永远做不到”的结论，也不是“只缺 experimental 回执”。准确结论是：**现有固定产物、stable 接口和当前 Host 策略组合，尚未形成足以放行的、可绑定到该草案会话的完整证据链；同时存在实际配置继承缺口。**

## 2. 固定来源与配置链

新采集的[固定来源记录](evidence/phase-3c-3b-3a/fixed-provenance.json)保留267个 schema 的逐文件摘要、完整 method 清单、关键响应形状和 manifest 原值。

| 项目 | 本轮核对结果 |
|---|---|
| 已有固定产物 | `yijie-agent-host/.local/runtime-artifacts/feat-136-b2b20e2fc4a0/codex`，355676760 bytes；SHA256 `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d` |
| manifest | SHA256 `1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b`；stdio、experimentalApi=false、aarch64-apple-darwin、0.144.6；版本是 manifest 记录，本轮未另执行 `--version` |
| 固定来源 | `b2b20e2fc4a0c94834f34d8cc459e488a1b56277`；上游 `rust-v0.144.6` / `5d1fbf26c43abc65a203928b2e31561cb039e06d` |
| 源码对应 | 来源和当前 HEAD 的 `codex-rs` tree 均为 `755f32c45a4c30e805e3c7fe1db89dcb4dcc6e41`；另核对两份补丁摘要及变更文件，不把基础 tree 单独当成完整构建来源 |
| 两补丁 | FEAT-126 日志过滤 `6b337a02caf064c6819fab5c7367a485004c85cce0d42acb06fa6d5003e599a0`；FEAT-136 command lifecycle `43de168e1443f4b9ca60d7f61e3de2daf20e1cfea14d2e196d28ba417bf3e06d`。未改本报告审查的配置编译、工具注册或会话初始化文件 |
| **采用的 stable schema** | 从上述不可变 source commit 读取267份，按 canonical 路径/内容 framing 重算 `82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1`，与 manifest/Host pin 相同 |
| 当前工作树 schema 的区别 | 当前 `.yijie` schema tree 为 `d82a33f683e554c10dd056a0101c26fd24477928e3f98ee3d9ef250b97395228`，**不是固定产物 schema**。当前 build/schema 脚本仍保留历史四补丁路径；本轮未运行它们、未重新生成或替换固定产物 |

该区别符合 Runtime [FEAT-137永久终止说明](../../../../yijie-codex/docs/feat137-retirement.md)，不是发现正在使用未知二进制。FEAT-137 不重启；其四补丁候选/旧开关不用于本需求。固定 Host policy 见 [baseline.go](../../../../yijie-agent-host/internal/codex/baseline.go)109—135。

实际配置路径是：原 Manager 的受管 CODEX_HOME 权威 → MiniMax 固定模型目录/Provider 配置，按既有 FEAT-144 状态加入或不加入 Sorftime → native config layers 将受管字段转为原进程 CLI overrides，保留原用户 trust → thread/start 或 resume 的 `config` 请求覆盖 → Runtime ConfigBuilder 合并配置层、requirements 和 fallback → compiled permission / session 初始化 / turn 工具计划。依据 [runtime.go](../../../../yijie-agent-host/internal/codex/runtime.go)350—395、[native_config_layers.go](../../../../yijie-agent-host/internal/codex/native_config_layers.go)98起、[provider.go](../../../../yijie-agent-host/internal/codex/provider.go)230—279、[config_manager.rs](../../../../yijie-codex/codex-rs/app-server/src/config_manager.rs)187—245。

草案目录由 native opaque workspace ID 解析为既有、canonical、空的受管目录；普通入口没有候选 writer/root。用途和 schema/policy/workspace 不可变，不得把普通聊天变为草案或反向转用；见 [Host草案服务](../../../../yijie-agent-host/internal/session/scheduled_draft.go)。**目录为空只能证明该目录状态，不能证明 Runtime 不会加载用户/系统/祖先目录指令或外部扩展。** 本轮没有把另一 CODEX_HOME 的成功样例当成产品共存证明。

## 3. 权限与工具证据矩阵

本表“已有控制”是固定源码支持的控制点，不等于本轮已在活线程观察到生效。所有未知项均保持拒发。源码文件摘要见[本轮来源清单](evidence/phase-3c-3b-3a-source-20260919.json)。

| 边界与要求 | 已有控制和源码事实 | 仍缺的证明 / 准入结论 |
|---|---|---|
| 文件读写：限明确草案根，禁止业务写入 | Host `scheduled_draft.go:30–43`输入命名 profile、`cwd:read`；Runtime `core/src/config/mod.rs:3696–3778`编译权限、应用 requirements 与额外读根 | stable start/resume 只返回旧 SandboxPolicy，readOnly没有读根；不能区分受限读和全盘读。没有线程绑定的最终读写边界证据，拒绝 |
| 网络：禁止工具/MCP/扩展联网；未来明确授权的模型文本请求单独计费 | Host profile `network.enabled=false`、web_search disabled；Runtime 有网络策略编译 | 不能由工具沙箱网络字段推出 Runtime 进程所有初始化通道都关闭；本批连模型请求也为0，未通过零外部请求预检 |
| shell / unified exec / 扩权 | ShellTool=false 确实在 `tools/src/tool_config.rs:81–110`使 shell type Disabled；request_permissions 和 unified_exec 显式 false；approval_policy=never | 这是有效控制点；仍需最终 feature/工具计划证据，且不会自动关闭 hooks 或其他工具执行器 |
| MCP工具、资源与凭据继承 | `config/src/merge.rs:11–31`递归覆盖，空 `mcp_servers:{}`不会删除基底 server；Host `sorftime.go:60–106`开启时包含 enabled Sorftime | 当前输入配置**确实不足以屏蔽已开启的基底 MCP**。会话初始化可创建连接；不能靠approval=never或空工具调用记录证明未联网/未读资源 |
| skills / AGENTS / 指令文件 | `core/src/config/mod.rs:3625`的 include_instructions 默认为true；`core-skills/src/loader.rs:240–360`含用户、repo、系统、admin等来源；`core/src/session/session.rs:907–926`先refresh指令并warm plugins/skills | 禁止依赖安装不等于禁止发现/读取；现有草案 overlay 未封闭这些来源。stable instructionSources可作部分事后线索，不能在读取前阻止或覆盖全部来源 |
| hooks / legacy notify | `features/src/lib.rs:481`忽略已移除的plugin_hooks；真正hooks在967起，stable默认true；`core/src/session/mod.rs:4045–4075`独立构造hooks并接入notify | 候选plugin_hooks=false无效。Sorftime基底已有hooks=false，但无Sorftime的普通基底没有同等闭合；不能断言所有上下文必然执行hook，也不能证明都关闭。notify另需审查 |
| plugins / apps / 扩展 | Host有plugins/apps/tool_suggest等false；工具计划 `core/src/tools/spec_plan.rs:583`分别收集多类来源，923起还处理extension executors | 输入flag不是最终执行器白名单；初始化warmup与配置来源仍需证明。不能只枚举常见工具名 |
| apply_patch / model特殊工具 | `spec_plan.rs:739`由model info独立决定；**当前固定MiniMax目录 `provider.go:404,412`明确apply_patch=nil、experimental_supported_tools=[]** | 当前固定目录有正向约束，不能声称apply_patch已经暴露；若目录/模型改变必须失效重验，也不能以此代替其他写/执行路径封闭 |
| 图片读取 / 图片生成 | image_generation=false；`spec_plan.rs:750`在有环境时仍加view_image；`handlers/view_image.rs:150–171`通过文件系统sandbox读取 | 图片生成flag不移除view_image。该读取器受真实文件系统策略约束，恰需验证最终读根；禁止图片调用预算不等于已从工具集中移除 |
| Web / 浏览器 | Host web_search disabled、in_app_browser=false；固定模型supports_search_tool=false；tool plan另按effective值选择hosted工具 | 有关闭输入，仍须证明最终状态及全部网络执行路径；不能以prompt限制代替 |
| 协作 / fanout / memory | Host相关feature=false；工具计划有各自条件，关闭memories也避免该分支加入memory读根 | 最终feature与原会话resume一致性未被stable完整回执覆盖；不得由单个multi_agent=false推出所有扩展已关 |
| 辅助读根 / requirements / fallback | `core/src/config/permissions.rs:478–504`增加zsh及execve wrapper所需根；wrapper只在CODEX_HOME/tmp/arg0下才取其父目录。`config/mod.rs:4228–4255`可因requirements选择fallback | 辅助根不等于放开整个CODEX_HOME，也不自动判失败；需逐项批准必要根并比对实际结果。fallback和未知根不可默认为与请求一致 |
| 仅展示工具 | `spec_plan.rs:683`加入update_plan | 可接受的展示事件不当作执行能力；不能因此误报“出现任何工具即隔离失败” |
| start / resume / follow-up | Host固定start/resume参数相同，turn沿固定outputSchema；三入口均先经过实际资格false；用途不变和unknown不重投已有定向测试 | 所需资格必须绑定artifact/config代次/cwd/purpose/schema及会话；resume、重开、配置或工具变化须失效。当前未实现、未伪造此正向资格 |

上表不穷举每个历史experimental工具作为独立开发任务；收口要求是按实际注册/初始化路径证明完整边界。本批没有新增通用资格平台或第二套执行器。

## 4. 现有查询能证明什么，为什么不能直接解锁

基于固定267份 schema 的87个 client method 及相应handler，重点核对以下路径；没有把“没有找到一个字段”写成全库绝对不存在。

| 路径 | 实际能力 | 不足 |
|---|---|---|
| stable `config/read` + `configRequirements/read` | config/read接受cwd/includeLayers，返回配置层合并后ConfigToml及origins/layers；既有Sorftime校验方式可复用 | 不接受thread ID或本次请求覆盖；不返回最终compiled permission和完整工具计划。`config_manager_service.rs:110–155`与真实thread `load_with_overrides`不是同一证据 |
| stable `permissionProfile/list` | 列出id、description、allowed；handler按cwd读取catalog | 可选性不是已生效权限；没有最终读写根/网络/工具。见 `protocol/v2/permissions.rs:361–389`、`catalog_processor.rs:427–476` |
| stable `thread/start` / `thread/resume` | 有cwd、approval、legacy sandbox、instructionSources | instructionSources是已加载来源路径；legacy readOnly没有限制读根；既不能防止此前读取，也不是初始化与完整工具证据 |
| stable `mcpServerStatus/list` | 可按threadId查询工具、资源和resource templates；相关handler会取得runtime配置并收集MCP快照 | 它提供MCP视角，并非所有工具/指令/权限证明；不能把可能需要连接/查询的目录采集当成无副作用的启动前预检。本轮未调用 |
| stable skills/plugin/model相关查询 | 各自目录、配置或Provider能力投影 | 不是一次turn最终注册集合与初始化拒绝证明；按cwd的skills查询也不等于实际线程的所有指令来源 |
| experimental activePermissionProfile / settings | activePermissionProfile只有id/extends，`protocol/src/models.rs:458–475`明示展示元数据；settings接口整项experimental | 本批不启用；即使启用也不能只凭profile ID资格通过 |
| 原有debug config lock导出 | 导出合并/部分resolved设置 | **`core/src/session/config_lock.rs:210–226`主动清除permissions/default_permissions/sandbox字段**；且在AGENTS/skills warmup之后导出（session.rs:907–943），不能补此缺口，不新增影子权威 |
| `attestation/generate` | server向client请求用于upstream的opaque token，见 `protocol/v2/attestation.rs`及v1 capabilities说明 | 与本线程有效权限/工具资格不是同一证明，不借同名概念替代 |

因此，最早缺失的能力是：**在可能的额外读取/连接之前，原生执行受限会话的封闭约束；随后给 Host 可验证、与实际会话及配置代次绑定的最终权限和能力结果。** 只增加回执、不封闭继承和初始化，同样不足。

## 5. 零外部请求预检与本轮验证

预检没有通过，故没有启动真实 Host/Runtime。具体依据：

- `core/src/session/session.rs:1209–1249`在session init创建并安装MCP连接管理器；现有空map无法保证继承server已关闭。
- `session.rs:907–926`在回执前刷新指令并warm plugins/skills；`1252`还安排启动预热，`session_startup_prewarm.rs:184–194`可进入auth预热。这里只确认存在需证明的初始化路径，**不声称所有路径每次必然联网**。
- app-server有Online模型目录刷新worker；但当前Host固定本地catalog对应 `models-manager/src/manager.rs:494–503`的static分支，不应把worker名称当作本配置必然联网的证据。此项局部澄清不能抵消前两项。

| 本轮实际检查 | 结果与证据 |
|---|---|
| 来源/协议静态核对 | PASS；binary/manifest/两补丁/固定schema和源码对应检查见[provenance](evidence/phase-3c-3b-3a/fixed-provenance.json)。schema来自Git对象，不调用Runtime generator |
| Host安全定向回归 | **11/11 PASS，含race**：[日志](evidence/phase-3c-3b-3a/host-focused-go1265.log)。6项FEAT155Draft覆盖I/O前拒发、用途隔离/幂等/unknown、正常临时Store5→6与重开、canonical空目录及进程内HTTP；5项普通路径覆盖权限模式/验证策略、accepted replay、native配置层保留trust与精确来源 |
| scoped go vet | PASS，三个相同包；[日志](evidence/phase-3c-3b-3a/host-vet.log)为空表示无诊断，实际命令与退出码见[来源清单](evidence/phase-3c-3b-3a-source-20260919.json) |
| 检查工具版本问题 | 首次强制GOTOOLCHAIN=local选到Go1.26.4，低于go.mod的1.26.5而拒绝，见[原始日志](evidence/phase-3c-3b-3a/host-focused.log)。随后直接使用**已有缓存**Go1.26.5、GOPROXY=off/GOSUMDB=off/GOTOOLCHAIN=local复验通过；未安装依赖或更新lock |
| 元仓治理与工作区 | strict、D0、audit-claims、lint、治理测试、Shell语法、文档链接与五仓diff/起点摘要检查，详见[检查记录](evidence/phase-3c-3b-3a/checks.json) |

定向回归准确命令（在Host仓执行；清除可选fixture输出目录环境变量，避免写入外部路径）：

```bash
env -u YIJIE_FEAT155_CONFORMANCE_DIR GOPROXY=off GOSUMDB=off GOTOOLCHAIN=local \
  /Users/jack/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.5.darwin-arm64/bin/go test -race \
  ./internal/codex ./internal/session ./internal/app \
  -run '^(TestFEAT155Draft.*|TestRuntimePermissionModes|TestRuntimePermissionVerificationPolicyIsOptIn|TestRuntimePermissionAdmissionPreservesAcceptedReplay|TestFEAT144NativeRootMigrationPreservesTrustBytes|TestFEAT144NativeManagedFileStillRequiresExactSource)$' \
  -count=1 -v
```

| 未执行项 | 原因及影响 |
|---|---|
| 活Runtime initialize/config/read、thread start/resume及正常进程重开 | 不具备启动前零外部请求保证，依26预检条件跳过；没有真实线程配置/工具观测，不宣称实际隔离PASS |
| Provider固定outputSchema与真实草案 | 本批0模型授权；Runtime资格也未成立，Provider资格仍NOT RUN，12次总额未使用 |
| Desktop完整装配、草案恢复/来源重新发现、UI、真实发送与日常库迁移 | 不在本批，普通15/5、候选22/6不变；不能宣称AC-002或全Must/D4完成 |
| 全量历史Runtime/Host故障套件、四补丁build/schema生成 | 有超出范围或不符合用户长期安全条款的历史流程；使用已审阅的普通定向回归。不用强杀、权限破坏、攻击fixture或可执行文件替换来补证据 |
| Contracts/Desktop总生成及全量测试 | 产品文件未改，不重跑无必要的跨仓生成；25记录的dirty Contracts保护与总generate失败保持原事实，未清理、绕过或改写为PASS |

## 6. DEC-155-09：最小后续决策建议（未批准、未实施）

Owner：段成威。建议选择 **A：单独开展最小原生受限能力的设计评审**。本次只提出该决策，不取得Runtime修改/升级/替换、付费调用或B3B实施授权。

| 选择 | 内容、收益和代价 | 推荐 |
|---|---|---|
| A. 批准小范围设计评审，暂不批准Runtime实施 | 保留两种创建方式、同一Host/Runtime和既定隔离目标。设计一个通用原生受限约束及可验证回执，先评估在固定双补丁基线上最小扩展能否满足；不把FEAT业务调度放入Runtime。需新增Runtime职责决策、来源/协议兼容评审和以后重新冻结产物 | **推荐**；直接处理已查明缺口，不靠页面或开关掩盖 |
| B. 暂缓该能力决策，保持草案禁发 | 零新增Runtime风险/工作；已实现候选继续保留 | 可选，但AC-002及整体D4继续未完成，不等于批准删去对话创建或将其永久延期 |

不建议“打开experimental”“增加第二Provider/Runtime通道”“改用全盘readOnly”“手动置ready”“只依赖prompt”。这些既不能完整解决上面的初始化和工具边界，也可能违反已接受复用与范围约束。

**A的最小设计输入已经具体到以下职责，不是要求重写执行平台：**

1. 在原Runtime thread/start、resume和每次turn准备的既有路径，对通用限制进行原生拒绝/执行：明确读根及必要辅助根、禁止业务写/执行与扩权、关闭非模型网络和MCP/skills/AGENTS/hooks/plugins等额外来源；约束必须先于相关初始化副作用。仅展示事件可保留。模型连接是后续用户批准的唯一文本生成通道，不另建Provider。
2. 从实际compiled permission与实际工具/指令/扩展选择结果产生stable可查询的证明；把它绑定到原线程及配置代次。不能让Host提交一份期望配置，再仅回显期望值当作事实。完整final集合与初始化时序无法证明时继续拒绝。是否可完全利用既有类型、最少新增哪些字段由下一次设计决定，本报告不手写wire DTO。
3. Host只消费和严格校验该证据，将自身artifact/hash、受管配置代次、cwd、purpose、schema/policy与其绑定；start/resume/follow-up、正常重开和配置变化重新核实。共享普通聊天不得被全局清空MCP/skills或改变Ask/Auto/Full；不新增用户权限模式。

**源码范围/兼容影响/验证代价：**

| 层 | 最小评审范围 | 必须承担的代价与边界 |
|---|---|---|
| Runtime | `app-server-protocol`及原thread handler；`core/config`、`core/session`初始化和`tools/spec_plan`的必要约束点；只有直接依赖所需才触及MCP/skills manager | 从不可变双补丁来源设计新候选，不能用当前四补丁build产物。Runtime canonical源/schema先行，独立验证默认普通行为不变、start/resume/turn及配置失效、初始化不触发额外请求；需新的可复现构建、manifest和pin评审。**不重启FEAT-137，不扩展调度器** |
| Contracts | 原Runtime兼容投影及来源锁；若Host公开能力语义确需变化，再按实际范围source-first | 新optional类型只有方向兼容证据充分才可称additive；Host资格默认/解释变化至少semantic，任一既有consumer不兼容则breaking。整体FEAT仍breaking；不预设新公共endpoint |
| Host | 原Manager的草案adapter、配置验证和资格失效；复用原operation和用途隔离 | 先兼容reader/协议适配，再替换经批准的新pin及激活；保留普通聊天/原MCP行为回归。旧Runtime缺证明继续拒发。禁止人工开关资格 |
| Desktop / 存储 | 本设计阶段只确认现有能力错误能承接，不提前装配/UI | 不预设SQL23或Host7；B3B及恢复另批。Runtime资格通过后，Provider仍须在12次总额内另作真实验证，不能拿零调用证据替代 |

代价不是补一个布尔值：至少涉及Runtime来源/稳定协议、Contracts兼容投影、Host消费三处及正常/受限共存验证。当前未授权的设计尚未确定字段和最小patch，**不提供貌似确定的实施小时承诺**；下一次设计应先冻结这些最少变化和测试集合，再给增量估时。既有允许超过16小时的授权保持，不以时间盒删减Must。

## 7. 技术自审、需求边界与停止

主代理完成来源、正反控制、协议替代路径、初始化时序、start/resume/follow-up与检查事实的结构化自审；无新增子代理，也不声称独立人工批准。重点避免了四个误判：CLI `--profile`不支持不等于命名权限不存在；apply_patch在固定目录中没有启用；局部static模型目录不等于完整零外部请求；当前schema工作树不等于固定产物schema。

已保留前序165份业务候选摘要及四个产品仓起点文件；五仓HEAD/branch/remote保持，详见本轮来源清单。未改Accepted ADR、未提交/推送/发布、未改固定二进制或用户配置。系统通知仍延期；本App防空闲睡眠/应用内重要更新、三目标、两种创建方式、恢复和页面仍按原需求后续完成，没有扩大或静默删减。

**本批执行结束并停止：调查收口，草案资格 NOT QUALIFIED；DEC-155-09未批准，不自动进入Runtime设计/修改、B3B、页面或真实调用。**
