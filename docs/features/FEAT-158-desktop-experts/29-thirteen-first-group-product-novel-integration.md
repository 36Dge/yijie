# 新增十三位第一组：产品管理与小说创作真实接入

2026-10-17。用户授权按[28号总审计](28-thirteen-expert-integration-feasibility-audit.md)实施第一组，要求真实功能、文件产出、深入代码审计及全量lint。已完整回顾总方案、内容与架构附录，以及21号本地文件接入、27号整体回归。**本组两位已完成真实接入及本地验收，当前共13位专家；原11位及历史保留。** 以下区分程序校验、真实模型产物、内容改稿和未实现边界，不把首稿自评或静态检查当成验收结果。

## 范围与决策

`contract-impact=semantic`：新增两份行为资产和本地目录／部署pin，沿用manifest3、experts/1、SQL35/Host10、原生绑定／outbox／Runtime及权限；无新公共wire、数据库迁移、Tauri command、连接器、依赖库。Skills为内容权威，Desktop和Host为消费者，Owner沿用段成威。使用当前working-tree本地候选，不合并、不发布、不提交推送。源码内容→确定性包→消费者pin→兼容验证→canonical正常运行。

产品管理采用六流程参考、来源台账、Decimal RICE及本地Markdown/JSON版本目录；小说采用Brief/Bible、真实章节、四台账、引用检查与版本目录。辅助程序只读输入、只在用户指定的新输出目录写文件，不授予额外权限，不自动联网或调用其他专家。使用Python标准库，不安装新依赖。文档与章节质量需实际模型及逐项读回，机械校验不等于事实或文学质量保证。

每位独立0.1.0；初始52条资源与14个专家历史版本全部保留，目标54条资源、13位最新专家。工作区基线和原52条manifest/authority已留存于Desktop `.local/thirteen-first-group-20261017/`；七仓原dirty工作不覆盖。原始23份资料文件只读，不修改WorkBuddy或用户归档。用户的真实功能验证授权用于本组正常合成文本/文件任务，不转用历史任务额度、不测试任何外部商用服务。

## 本组Must验收

1. 两位进入真实Native目录，可准备、召唤、填草稿、显式发送；无展示占位或专家团。
2. 产品六类流程真实产出文件；引句与输入对应，RICE缺值/0/单位正确，修改路线图保留旧版。
3. 小说实际生成Bible和至少两章；后续读取保存文件继续，四台账引用一致；改设定给出影响且旧稿保留。
4. 输入不足与重复输出目录正常提示；未选择连接器无外部工具调用；权限、未知状态不重发保持。
5. 原11位、全部52条资源、旧会话/消息/收据/Runtime记录保持，正常退出后只读比较，再同构建重开。
6. 完成实现后的独立审查阶段、正常focused测试及受影响仓全量lint；所有未运行项单列，不用合成模型或静态结构代替真实产物。

文件通过现有会话权限写用户选择的工作区，明确绝对路径并读回。未扩展Native Artifact/本地链接打开；从Finder或允许的系统应用打开文件。禁止强杀、权限破坏、攻击fixture和运行时劫持；包含禁止行为的历史全套测试不运行，正常覆盖另留证据。

## 实施与验证

### 已完成的实现

| 层 | 本组变化 | 保持的架构 |
| --- | --- | --- |
| Skills | `product-management@0.1.0`（19文件）、`novel-creator@0.1.0`（15文件），各一份ROLE/SKILL、参考、实例、检查表、评测和标准库Python程序 | 单专家入口、显式package_files、逐文件来源审校 |
| Host | `internal/skills/experts_candidate.go`固定新manifest摘要，扩展实际包安装/会话回归期望 | 原安装、精确引用、角色组合、权限、Runtime执行 |
| Desktop | 资源candidate、canonical producer路径、当前Host真实tree freeze、两头像映射、目录测试期望 | Native目录/准备/绑定/outbox；没有增加wire或业务状态表 |
| 保留保护 | Skills测试和Desktop同步入口逐条核对固定旧manifest的52条完整metadata/archive | 旧38技能及14个专家历史版本保持原ID、版本和摘要 |

当前bundle为`0.12.0`，54条资源、16个专家版本、13张最新专家卡片。不是把新增13位全部完成；本轮只接入第一组2位，余11位仍依28号计划。

生成目录：`yijie-skills/dist/skills-experts-thirteen-first-v010`。manifest SHA256：`eae61812cdb372924b97628cdba45b4d4716303341b8f6654dde33f00c941c68`；authority SHA256：`ebc9f9d42ab7b3b59abd9cb44e02273859c2ab9a0342281ad0c6d94931dda6ad`，57,427 bytes。旧manifest固定摘要`fa320bc5f3caa0caca0e7851061b186f4b975b20c2d0f6da8351715a2d377fa7`，在Skills `docs/provenance/FEAT-158-retained-resources-v0.11.0.json`保留。

来源与本地授权：Skills `docs/provenance/FEAT-158-thirteen-first-group-local-use-v0.1.0.md`、两份`source-audits/FEAT-158-{product-management,novel-creator}-content-audit-v0.1.0.json`。产品原13文件、小说原10文件逐项核对。内容改写与自有辅助程序替代WorkBuddy工具假设，保留原产品管理Apache许可证；没有宣称头像等其他素材同属该许可或取得公开再分发资格。

### 实现后代码审计

审计与实现分阶段进行，由本任务重新逐函数检查；不是独立人工批准。完整记录在Skills `docs/provenance/FEAT-158-thirteen-first-group-content-review-v0.1.0.md`。

- 产品程序检查来源ID、逐字引句、Decimal计算、置信度0–1、周期/单位、正工作量；真实0参与计算，null不参与排名。六种Markdown与输入/来源快照及文件收据真实写出。检查范围不包括所有自然语言结论的真实性。
- 小说程序检查六要素、确认来源、章节/人物/事实引用、四台账、时间与知识不引用未来、连续编号；续写核验上版文件摘要、稳定ID和revision+1。修改列出影响与尚待复核章，正文仍必须阅读。
- 复核发现“新增章节未更新timeline也能通过”，已在首次安装前补齐每章时间线覆盖校验并加正常数据回归。未发布旧0.1.0，不存在覆盖已安装版本。
- 两程序均先验证再创建新目录、独占写文件、最后写receipt；拒绝既有输出和安装资源内写入。部分生成失败保留文件并要求新目录；无网络/凭据/DB调用，无新依赖或守护进程。此校验不是替代宿主权限的沙箱。
- 本轮既有文件差异与开始时dirty基线比较：Skills 2个、Host 3个、Desktop 7个；无原文件删除。Contracts、Connectors、Runtime未改。不能把Git HEAD到当前的累积差异都算成本轮修改。

### 检查结果

证据根为Desktop `.local/thirteen-first-group-20261017/`，所有结果来自实际命令日志。

| 检查 | 结果／证据 |
| --- | --- |
| Skills `make lint`、`make test` | PASS，93项实际测试；118条eval为格式检查，不是118次模型功能验收 |
| Host `make lint` | PASS，原来源锁和工程门禁保留 |
| Host focused `go test -race` | PASS，实际包安装、旧专家版本共存、生命周期、绑定/模型切换/正常恢复及普通权限基线；`host-01.log` |
| Desktop UI focused | 13文件141项PASS，`ui-01.log`；初次旧producer路径断言失败后修正当前路径，并增加全旧资源保护断言 |
| Desktop Native focused | 40项PASS；`native-01..12.log`及`native-commands-corrected.log`。首次commands过滤器未匹配（0项），更正为真实模块后9项通过，0项不能计通过 |
| 旧资源保护测试 | 两项PASS，合法追加与普通缺失/metadata差异均按预期处理 |
| Desktop全量lint | `make lint CONTRACTS_DIR=.local/demo-fast-contracts` PASS，包含来源检查、ESLint、TypeScript、Rust fmt及全targets Clippy；最终`desktop-full-lint-final.log` |
| 元仓lint/test及Shell语法 | PASS，50项测试；`meta-lint.log`、`meta-test.log`、`meta-shell-syntax.log` |

Host/Desktop历史全套测试套件未执行：其中含用户禁止的强杀、权限破坏、恶意资源或运行时替换类别；采用以上正常数据、正常拒绝和正常关闭/重开focused覆盖，不声明被跳过的异常分支已通过。全量lint完整执行。没有以禁用规则、清dirty或借其他checkout摘要通过门禁。

### 实际模型与产品文件

正常canonical打包并启动本工程开发App：`scripts/run-local-demo-fast.sh --packaged`，日志`build-and-launch.log`与`packaged-launch-receipt.json`。App为`src-tauri/target/debug/bundle/macos/易界 AI.app`，`release=false`，未安装到系统Applications、未宣称签名发布。98个App文件及Host/Runtime/worker等5项摘要均一致（`artifact-consistency-current.json`）。

两位通过真实Native资源准备；目录可见13位且全部ready；快捷问题只填草稿，显式发送后执行。使用当前`Kimi-K3 / max / ask(on-request)`，未选择连接器；不更改全局权限。工作空间为本证据根下`eval-workspace`，所有输入为本任务合成资料，不涉及真实业务账号或生产数据。

产品真实会话`01a147b7-63b6-7283-b37b-f9ec8edd322a`：

1. 首轮353秒，读取materials和已安装专家程序，真实输出六份文档及RICE、快照、receipt。A=96/B=40/D=0，C缺reach不排名；两访谈引句正确、不完整周不冒称增长、竞品未知保留。
2. 本任务逐项读回发现开发状态推断、成功率粒度、B含义及建议验收项混入确认范围。首稿留存，未采信模型“全部通过”的自评。第二轮530秒，以新来源S3纠正六稿并将A工作量2→3，A=64，明确A+B占满4人月的容量取舍。
3. 第二轮为缩字提出删除当轮输出，现有ask审批被拒绝；模型保留超长草稿为`pm-v2-draft-overlength`，再生成正式`pm-v2`。删除未执行，v1全部10文件和输入计划11项hash不变。
4. 本任务比对最终六稿、引用、计算与三套receipt，系统TextEdit实际打开`pm-v2/prd.md`中文正文。`product-manual-review.json`、`pm-receipts-verification.json`保存结果。产物是需审阅的产品决策草稿，不是已获确认的排期或自动发布。

小说真实会话`01a147c7-c6a2-7fa0-a78a-94a61d757c93`，使用同一个Runtime thread，三轮均完成：

1. 首轮396秒，真实读取已确认Brief和安装包，生成Bible、两章正文、四台账及收据；正文527/521汉字。首版12个实际文件（11个被receipt记录的文件＋receipt自身），不是模型自报的11个总文件。
2. 第二轮404秒，从磁盘读取首版，纠正信封保存位置、岛内路线和离岛居民/备用船的连续性，续写第三章；第二版13个文件。读回发现“固定少亮一分钟”被解释成逐日累积、日志叙述作者离开后的未来、柜子十几年未开与三年前存日志冲突，未把结构通过当成内容通过。
3. 第三轮478秒，确认人物职业与信封颜色的新设定并纠正上述因果，真实改动三章正文、Bible、事实和四台账。最终577/568/610汉字，9项事实变化、3章受影响并实际修订，`review_required_chapters=[]`。旧看守去向和待换零件仍作为故事开放线索，不伪称已回收。
4. 本任务重新读取全部最终正文和台账；第一章未拆封、第二章只得钥匙、第三章开柜，岚不会游泳、弟弟仍在大陆、许叔没有预知日志内容。人物职业/红信封同步，机械原因改为固定晚开一分钟且熄灯独立不变。TextEdit实际打开最终第三章，中文正文正常。它是可审改的三章创作稿，不是长篇零矛盾或机械维修知识的证明。

独立文件校验脚本`verify-live-outputs.py`及`live-output-verification.json`核对六个产出目录的全部文件hash/长度、产品RICE与逐字引用、小说版本链/稳定ID/四台账及目标文本。PM首版及其输入11项、小说首版及输入13项、小说第二版及输入14项摘要全部保持；初始原材料不改。最终产品目录`eval-workspace/pm-v2/`，小说目录`eval-workspace/story-v3/`。模型只是生成和调用已安装程序；主任务没有代写这六套验收产物。

`runtime-execution-evidence.json`与`live-ledger.json`记录2个产品轮次、3个小说轮次及真实已安装helper读取/调用；工具只有现有`exec_command`，未调用连接器或网络命令（模型推理API本身不计为业务连接器）。离线Native检查在正常退出后进行：两位绑定均`ready@0.1.0`，两个prepare均`succeeded`，5次dispatch均accepted且无错误、5个turn completed，outbox均done，权限始终ask、授权revision=1；见`pm-native-execution.txt`、`novel-native-execution.txt`。

### 历史保留与正常退出

启动前App已停止，按私有权限备份SQLCipher/WAL/SHM、Host Bolt、10份Runtime历史和246份安装文件；没有在运行中打开会话数据库。原资深电商专家0.1.3历史在UI中实际打开，原回答、版本和绑定仍可读取，没有发送新任务。

五轮完成后用App正常Cmd+Q退出。canonical启动进程exit=0，18081端口释放，App/Host/worker/Runtime相关进程全部退出；没有强杀。随后只读核对：

- SQL：原10会话、73消息、37轮次、5专家绑定、15专家提交、15资源操作、642 Native事实等全部原行内容保留；原有计划/审批/连接器数据也无丢失。唯一旧行差异是`chat_market_dispatch.updated_at`，逐字段复核仅更新时间，业务状态/收据不变。35条迁移记录完全不变。
- Host：所有旧绑定、资源操作、模型/回合操作、cleanup收据、索引保留；12个原session仅4条`updated_at`正常变化，其余业务字段不变，无记录丢失。
- 资源安装日志：原4,115条操作逐字保留，新增两条prepare后4,117条。原246份安装文件中仅该日志DB整体摘要随新增记录变化，另外245份逐字相同。
- 原10份Runtime历史逐字相同。七仓HEAD/分支未变，无原文件删除，全部`git diff --check`通过；Contracts/Connectors/Runtime无本轮源码变化。

证据：`normal-shutdown.json`、`sql-preservation-after.json`、`sql-row-diff-after.json`、`host-preservation-after.json`、`installed-journal-preservation-after.json`、`preservation-files-after.json`。备份包含私有历史，保持在本机证据目录，不加入版本库。

随后执行canonical `scripts/run-local-demo-fast.sh --packaged --reopen`，出现`Same-build expert reopen verified; local QA provenance only`，readyz返回200/ready。重开后实际UI再次核对：13位专家全部ready；产品2轮、小说3轮原历史及各自0.1.0绑定恢复、ask不变，无自动发送；App停留专家页供继续使用。98项App文件及5项运行产物摘要均未漂移，992份Desktop构建源摘要与回执一致。`reopen.log`、`reopen-verification.json`记录该结果。未在重开运行期间再次打开会话数据库。

本组6项Must均完成：实际目录与绑定、产品六流程/版本、小说多轮/四台账/影响、普通缺输入与重复输出拒绝/原审批、旧资源历史保留/正常恢复、深入审计/受影响仓全量lint。一次canonical构建完成全部真实轮次，最后同构建重开。两个专家的推理和正文仍会受模型质量影响，本次是有读回审查和改稿的真实工作流验收，不能推导为无人审阅的文稿永远正确。

### 能力边界

本组完成范围是本机真实资源与会话执行、用户工作区Markdown/JSON文件、产品六流程及小说短篇多轮改稿。未实现也未宣称Figma/Jira服务、自动访谈采集/持续监控、全局记忆、长篇零矛盾、任意文件自动注册Native Artifact或聊天链接直接预览。外部账号业务调用不属于这两位本地模式；其余专家无账号项目继续NOT RUN。本轮无公开分发、签名发布、commit/push或新provider授权。
