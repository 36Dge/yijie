# 13 位新增专家：现有易界架构复核（只读）

日期：2026-10-17。审计范围：Desktop、Host、Skills、Contracts、Connectors 当前源码、AGENTS/README/SECURITY，FEAT-158 的 17/19/20/27 历史记录。仅输出本笔记；没有改产品、启动/退出 App、安装包、读取凭据或业务调用，没有运行故障/攻击 fixture。当前审核本身 `contract-impact=none`；此分类不能沿用未来接入实施。

所有相对路径基于 `/Users/jack/Downloads/Personal_Info/CrossBSD/`。下述是静态实现判断，不冒称本轮运行或线上验证。

## 1. 真实现状与容量

读取当前 `yijie-skills/dist/skills-experts-seventh-group-v010/bundle-manifest.json`：bundle 0.11.0，52 条＝38 普通技能＋14 专家版本，11 个 expert_id。manifest 171,165 bytes，SHA256 `fa320bc5f3caa0caca0e7851061b186f4b975b20c2d0f6da8351715a2d377fa7`；authority 49,518 bytes。最大现有专家解包尺寸 1,161,613 bytes。

若每位新增一个适配版本，最终应为 **24 张卡、27 个专家版本、65 个总资源**。不需因65总数扩容：

- bundle v3 总条目最多256：Contracts `jsonschema/skills/skill-bundle-manifest-v3.schema.json:31`。
- Host普通管理快照最多256：`internal/skills/store.go:264`；公有SkillList/Scan wire对应 `yijie-contracts/openapi/agent-host/agent-host.yaml:2943`、`:2964`。
- Native `src-tauri/src/skills/catalog.rs:286–318` 的64限额统计 **(expert_id,version) 对**，不是总资源，新增后27远低于64；同时要求普通分类仍[5,9,7,9,8]。
- Native safe catalog wire 最多64张卡：Contracts `compatibility/experts/wire.schema.json:254–268`，新增后24。
- Native manifest/authority各1MiB：`src-tauri/src/skills/catalog.rs:9,252–256`；Desktop同步器更严格把authority限制256KiB：`scripts/sync-desktop-expert-resources.mjs:42`。适配打包后须实测最终体积，不靠原包数量推断。

现有14版本：jd 0.1.3；小红书0.1.0/0.1.1；漫剧0.1.0；跨境运营0.1.0/0.1.1；报价0.1.0；可视化0.1.0/0.1.1；TikTok、人台、视频复刻、1688、行业研究均0.1.0。新增13位不能覆盖任何旧安装id、版本、资源或精确引用。

**新增原材料的一个硬性阻断**：按导出 `原始资源/` 普通文件实际求和，美团32文件为 **68,933,291 bytes**，超过现行64MiB=67,108,864 bytes单包上限，并有2符号链接。原样导入不合格；其他12个原目录均低于7MiB。应该保留完整档案，执行包仅选审过的必要正文/适配脚本，不抬高门禁、不开启符号链接，也不把附带TGZ/二进制当成已接入运行时。

## 2. 资源包与权限边界

- Skills是内容唯一权威。`scripts/package-desktop-skills.mjs:58–72` 按每条 `package_files` 显式白名单收录普通文件，禁止符号链接；`:75–91` 校验逐文件内容审核记录；`:168–175` 只能扩展原38条v2源；`:183–204` local-development授权、同expert/version唯一、安装id/runtime_name唯一；`:259–286`生成authority。没有文件扩展名统一白名单；“能归档”不代表能安全执行/读取二进制。
- Host `internal/skills/archive.go:76–122`拒绝额外/嵌套SKILL.md、链接/特殊条目、路径/大小写碰撞，且验证数量和解包大小。每位必须一个根SKILL入口、一个ROLE、重写过的参考索引。原包54个子SKILL不能简单照搬并期待自动调度；改名也不是能力适配的证明。
- 单包压缩与解包均≤64MiB、≤2048普通文件：Contracts manifest-v2 `:381–383`，Native `catalog.rs:383–393`。
- ROLE≤32KiB；知识1–32项、每项≤8MiB；Host还重算路径/receipt/digest，要求UTF8无NUL；组合索引≤32KiB：`internal/skills/experts.go:83–160`；schema v3 `:143–175,258–264,838–856`。PDF/字体/图片/XLSX不能作为知识文本；必要模板可以是审过的包附属文件，但解析/渲染依赖须另验。
- 资源metadata仍tool-assisted/read/none/required_tools=[]：schema v3 `:794–836`。这表示只读受管资源且没有额外命名依赖/授权；不会自动注册插件或给工具许可。需要按连接器就绪状态自动决定“能执行”、自动配置依赖、增加必需工具声明时，须先设计源契约而非隐藏在描述里。
- Host `internal/skills/service.go:731–738`排除专家的全局Skill投影。`internal/codex/market_runtime.go:147–170`明确关闭hooks/plugins/apps/tool_suggest/shell_snapshot/multi_agent/js_repl/memories。WorkBuddy Agent、依赖插件、浏览器工具、会话记忆、子agent均不能直接继承。
- 所有非空专家统一关闭内置web_search：`internal/codex/expert_instructions.go:48–58`；取证搜索必须走现有已选连接器或用户文件。不要按新专家名字在Host开例外。
- `runtime_permissions.go:36–45` ask/auto是workspaceWrite+networkAccess=false，full为dangerFullAccess；非空连接器选集只支持ask：`market_turns.go:69–79`。不允许把切full当缺少provider/网络工具的接入方案。

## 3. UI、绑定、发送、恢复保持原路径

- Native从已固定manifest和authority解析：`src-tauri/src/skills/catalog.rs:241–318`；`skills/experts.rs:66–140`只接受expertId/version，产出archive/ROLE/knowledge-manifest三摘要ExpertRef，不接受renderer路径或角色正文。
- `skills/experts.rs:144–169`的available/ready仅资源状态，ready并不证明远端账号/模型/产物质量已验；`:182–206`用SemVer选最新卡片，旧版本仍可精确查找。并存通过独立安装槽：`:13–32`。
- `src/data/expert-showcase-catalog.ts:7`为空；不能为13位重新塞展示卡冒充接入。头像沿 `src/data/expert-avatars.ts:13–28`静态expertId映射，`ExpertAvatar.vue:9–18`失败回退icon，不加入ExpertRef/wire。
- `src/components/experts/ExpertMarketPanel.vue:96–155`现有目录/详情/状态/准备按钮；`src/composables/useExpertSummon.ts:42–90`先准备再绑定，参考问题只填草稿，旧草稿/切换需现有确认，不自动发消息。
- Native `chat/experts/store.rs:199–270`在既有SQLCipher记录pending意图与旧confirmed引用；pending/inflight/uncertain outbox、删除、模型切换互斥。`:403–500`复核并在原消息/outbox事务内冻结ExpertRef和binding revision，非第二套任务队列。
- 引用保护 `store.rs:539–572`同时看当前绑定、历史submission、pending/unknown绑定请求，覆盖跨scope历史；共存仅豁免可信目录证明的精确旧Ref，不删除ResourceInUse判断。
- Host每轮重验包：`internal/session/market_submit.go:148–152`、`session/experts.go:65–92`；组合完整普通权限基线＋ROLE＋短索引：`codex/expert_instructions.go:70–86`，解除则恢复普通基线。不会清除模型历史。
- Host绑定复用同Runtime thread并核对model/provider/effort：`session/experts.go:313–340`；旧工具选集/lease先清理，下一轮重新授权。模型切换保留专家：`session/chat_models.go:146–175`先重放已完成结果再解析当前绑定；不应增加新模型引擎或切换策略。
- Host读回与显式恢复分开：`session/experts.go:130–161,232–235`。read/repeated apply不重发；显式恢复只能对原idle thread重新建立证据。关闭专家要保留reader和历史、拒绝旧专家会话绕过绑定普通发送；`internal/session/experts_test.go:284`已有此正常场景测试。
- 当前SQL35/Host10沿用；无新增字段需求的资源接入不新增migration，不搬库、不回填旧会话、不自动重试unknown。

## 4. 新能力与provider判断规则

现有provider registry有60项，含wind/eastmoney/morningstar/gildata_finance_data_qwen、LinkFox、出海匠，以及可供MOSS复用的 `fanruan-growth-advisor`（显示名MOSS增长谋士，OAuth/HTTP，resource为 `https://www.mossdo.com/api/v1/mcp`）。MOSS并非缺少登记服务，但候选资格仍为 `not_run`，独立客户端OAuth、WorkBuddy特有header适配、longtask工具与完成/轮询语义须实际资格核对，不能认为既有登记等于已经通过。目录不含独立美团、WindAlice、Remotion或浏览器控制服务。不能据名称相似宣称WindAlice等于当前wind，也不能把Web链接等于已接API。源：`yijie-connectors/catalog/provider-registry.v1.json:263,311,327–332,499,511`、`catalog/provider-candidates.v1.json:407–413`及完整services枚举。

可以在原资源架构内做：文本咨询/规划/创作、用户文件计算和本地产物、现有工具schema支持的已选连接器调用指引与参数/结果校验。不新增权限且不改变wire，不要求新专家执行器；但每位的完整核心输入→产物要实际验证。

需要单独provider/部署适配或明确延期：新认证/API域、WorkBuddy私有代理/令牌、受管浏览器、外部文件公开上传/下载、Remotion/Chromium/FFmpeg依赖装配与输出、多媒体流承接、WindAlice会话状态续接、美团登录/账号/促销/下单等。其中第三方raw协议先以官方文档核对，归一化的易界wire/schema如发生改变必须source-first；纯新增provider registry不等于必然新专家wire。

通用MCP已有完整schema冻结和逐次批准，不能说易界只有占位：`worker/src/generic.rs:107–147,150–168,221–286`。但destructive明确拒绝、凭据参数拒绝、每次批准仅一次调用，错误/未知不自动重试。`:289–317`只接受惰性text/JSON，embedded resource/resource link/binary必须专门artifact策略，不能自动抓取。已有LinkFox图片/视频专家返回任务/URL处理不等于新口播模型、音频、人物保真都支持。

建议按依赖分层而非页面数量分组：
1. 复用现有本地资料咨询/文本输出（淘宝、拼多多、产品管理、小说）；要先处理平台资料时效与事实保真。
2. 本地文件与计算/交付（数据分析、UI设计、量化的本地回测范围）；运行库、解析、模板/渲染实测是先决，不只ROLE。
3. 现有provider真实路径适配（LinkFox口播、股票/行业研究中实际能用的现有金融/搜索工具）；账户缺失可跳过在线验收但不得把核心依赖删除后称完整。
4. 专用宿主/认证/产物重依赖（WindAlice、美团、Remotion，MOSS若依赖宿主私有能力）；先确认官方独立客户端协议/本地依赖再纳入批次。最终分组需与逐位内容审计合并，以上不是13位逐项内容审计结论。

## 5. 保留与标准执行顺序

现有同步器 `scripts/sync-desktop-expert-resources.mjs:64–74`已能多专家，只硬校验38普通归档库存＋jd0.1.3存在；**这不能证明其余13旧专家版本完整保留**。新增每组需对上一52条（以后逐组递增）的完整条目JSON及每个归档做逐字节/摘要对照；不能只验数量、jd或只保留最新版。

1. 在修改前记录七仓HEAD/dirty文件、当前52条、bundle/authority/已安装receipt，保留既有工作。不在审计阶段接App/改库。
2. 后续经用户要求实施后，逐位改写适配SKILL/ROLE、任务参考、模板/辅助程序、examples/checklist/eval/rubric；独立安装ID、版本与本地使用/来源审校记录。原13位完整归档保留，执行包只审阅白名单。
3. 有wire/provider变化先源契约/官方协议/consumer同步；纯资源使用当前experts/1与manifest3不改schema。基于既有17–27实施惯例，本地目录/部署接入按semantic兼容审查；实际每组按最高影响重新分类。
4. canonical `scripts/package-desktop-skills.mjs --source plugins/yijie-desktop-skills/experts/bundle-source.json --output dist/<new-reviewed-candidate>`；再次独立重建比较确定性；保留旧输出。
5. 更新Desktop `contracts/experts-assets.candidate.json`与sync脚本producerOutput、Host `internal/skills/experts_candidate.go`到真实生成摘要；更新实际目录测试及头像映射，不能手改generated DTO/schema。先资源同步并--check，再freeze。
6. `scripts/chat-model-build-candidate.mjs:69–76` freeze首先执行全部consumer/source/资源一致性检查；`:59–66`真实Host tree和候选pin严格匹配。仅审过的实际变更才能freeze，不能以旧clean checkout代替运行源码，也不能复制摘要消除失败。
7. 历史不可变门禁用既有 `resolve-pinned-checkout.mjs:14–29`，显式来源不回退、仍验证clean/origin/commit/字节。Desktop完整lint既有命令 `make lint CONTRACTS_DIR=.local/demo-fast-contracts`，同时当前v4/专家候选检查仍读真实sibling；旧源与当前运行候选分清。FEAT137历史NOT PASSED不能改为绿；27记录的历史global breaking旧schema EOF失败也不能由lint覆盖。
8. 后续若用户要求部署，先App正常Quit、进程正常退出/port18081释放，再私有备份SQLCipher/Bolt/WAL/SHM与Runtime/receipt，使用已审readonly检查器（不读出密钥/正文）。不要运行时对DB做Foundation metadata读回；19已确认会释放POSIX锁并造成WAL失效。
9. 标准 `scripts/run-local-demo-fast.sh --packaged`：worker正规构建、当前资源/source检查、Host正规build、Tauri App和精确回执；`:292–307`port gate、`:319–347`构建与receipt。保持com.yijie.ai/demo-fast-v1/.local/demo-fast；同构建重开走--packaged --reopen，不改旧回执。无强杀；若无法正常退出停止并报告。
10. 回滚保留当前兼容reader/旧包/收据，不能换成不认识新增Ref的旧Host/目录，更不能降库或删绑定。

## 6. 每批真正验收条件

- 结构：Skills lint/test；包确定性、白名单、receipt/source/authority；前一批全部原metadata/archive不变，27版本/65资源最终完整。
- 真实安装：Host实际candidate managed resource、旧安装升级共存、引用保护/普通基线；Native实际catalog/精确Ref，40项原事务/正常恢复/互斥方向保留。可复用 `internal/skills/experts_test.go`及 `session/expert_resources_test.go:35,163`等正常候选测试。
- 功能：从真正已安装目录读知识/执行每个适配辅助脚本，独立验证算法/产物、未知值与来源；只是package存在/0测试匹配/模型自评均不计通过。
- UI：真实资源卡→准备→选择→草稿→显式send；24卡搜索、详情、亮暗1180×760、原3列，不含团队。无真实模型预算时可先验证草稿与回执，但必须将模型内容质量标NOT RUN。
- 恢复：normal stop/reopen、旧绑定/旧model/普通chat/unknown不重发；快照对照数据库旧行（仅预期时间字段变化）、原Runtime文件、所有旧内容/receipt。
- 连接器：当前tools/list和schema、资格、selected精确身份、每次批准；普通in-process模拟能证明实现控制链，不能证明商用账号、配额、远端任务/数据质量。
- 缺少账号的线上授权/数据/媒体/费用/写操作均NOT RUN，记录每位被影响的实际能力；不能在卡片上把resource ready改成线上可用。
- 全量lint须按受影响仓规范完整跑；故障/攻击/强杀/权限破坏fixture不运行，安全focused测试与全库测试区分。后续只运行正常、非破坏验证。

当前笔记没有发现因24位/65条而必须重建专家架构、放宽限额或迁库的理由。真正制约是资源适配质量、未受管宿主依赖、provider认证/工具实际差异以及产物链；这些要在实施分组的范围和验收中明示。

## 7. 补审：真实文件交付与 Native Artifact 不是同一条已打通链

依据当前代码，不应将“辅助程序写出了文件”“对话里显示链接”“已有Artifact播放器”混称为一项已完成能力。

### 7.1 当前可识别格式和限制

`yijie-desktop/src-tauri/src/chat/artifact.rs:23–24,2969–2988`：

| kind | 可接受mediaType | 当前展示/保存 |
| --- | --- | --- |
| image | PNG、JPEG、WebP | Native图片预览，≤20MiB；**不含SVG** |
| video | MP4 | Native私有预览协议+保存，≤64MiB，另有严格容器约束 |
| file | TXT、CSV、JSON、PDF、XLSX | TXT/CSV/JSON内联文本预览（source≤1MiB）；PDF/XLSX保存为文件，无内联预览 |
| report | `application/vnd.yijie.report+json;version=1` | 当前结构化报告投影与图表；**不是任意HTML** |

文件预览/保存源：`artifact_file_native.rs:481,552,924–983`；UI `ChatArtifactFile.vue:32–63`明确PDF/XLSX为saveOnly。XLSX保存还执行 `attachment.rs:1182` OOXML验证，≤512 entries、展开总量32MiB、单entry8MiB、ratio100 (`:22–25,1199–1227`)，没有Office公式重算或通用格式等价验证。

MP4源：`artifact_video_native.rs:800`创建受context/session/turn/artifact绑定的预览，`:869`保存；`:1584–1615`要求32B–64MiB、首box ftyp、brand含avc1、moov在mdat前、**恰好一条轨道**；`:1655`唯一轨道必须vide；`:1647–1649`宽高1–8192；`:1634`时长≤24h；`:1690`samples≤100000。**常见带声音的MP4有视频+音频两轨，现行Native会拒绝；这对Remotion和带货口播都是真实缺口。** 不可以去掉检查来凑预览。

Host encrypted spool自身限图片20MiB/其他64MiB、每session256MiB、全局1GiB、TTL24h：`yijie-agent-host/internal/artifact/store.go:25–30`。其allowlist也没有HTML/SVG (`:478–500`)。

### 7.2 工作区文件目前不会自动成为Artifact

当前对Host产品源码检索 `s.artifacts.Put`，生产入口仅：
- `internal/session/artifacts.go:69–131`：明确synthetic测试producer；
- `internal/session/provider_image.go:214`：既有实际图片provider产物。

未发现把普通Command写到工作区的HTML/SVG/XLSX/MP4自动导入spool、签发artifact id、发布完整v3 lifecycle的通用生产入口；因此文件存在不代表已在Native预览/保存链。不能用synthetic producer填真实文件回执。

聊天Markdown链接在 `ChatSafeContent.vue:195–206`解析为inert_link，`:528–530`渲染为span＋目的地文本，并非<a>；当前没有通用“点击本地路径→系统打开”功能。不能因模型返回Markdown文件链接宣称用户能从易界一键预览/打开。

### 7.3 对本批方案的实际要求

- UI设计师至少真实产出可打开的离线HTML/SVG（必要时附PNG预览），验证响应式、中文字形、图标、资源路径/缺资源、无意外CDN依赖；不是只给设计建议/专家卡片。复用工具思想可以，直接写“调用已接report专家helper”不成立：专家资源不全局投影，跨包安装状态/版本/依赖没有自动保证。需要在本专家白名单内纳入已审复用源和具体版本/许可，或正式设计共享依赖；不得盲指向另一个专家安装绝对路径。
- Remotion必须装配经审阅的Node/React/Remotion/Chromium/FFmpeg依赖并走标准可复现构建/渲染，真实交付MP4并验证视频/音轨、尺寸、时长、可播放和输入素材一致性。角色/项目TSX生成只能算前半链，不能标视频生成通过；当前不可原样执行包内附带运行时/未知二进制或网络安装。
- 首期可明确使用现有会话权限写到用户选定工作区，以普通本地文件方式交付，记录绝对输出路径和独立校验，在允许的系统应用中实际打开/播放；这是实际产物验收，**与App内Artifact/点击打开仍未实现分列**。若工具安全策略拒绝本地URL等步骤，不能另设HTTP服务/改浏览器绕过，应记录并采用允许的渲染检查。
- 若范围要求App内HTML/SVG交互、任意音轨MP4、工作区产物自动登记或本地一键打开，必须作为独立受审产物桥接方案：路径/所属scope/来源/大小/类型校验、生命周期、用户手势、输出策略及native权限先明确，涉及wire或新command则按Contracts/Native源规范先行；保持原allowlist/CSP/门禁和旧产物兼容，不能把它藏在专家资源变更中。

本小节为源码审计，不声称上述新产物桥接、视频音轨支持或UI专家渲染已经实现。
