# 第一组 3 位专家真实接入

2026-10-16。用户明确要求按 [17 的审计](17-ten-expert-integration-feasibility-audit.md) 实施小红书、漫剧、跨境电商运营三位专家，复用现有架构，保留原专家与历史数据，并完成实际功能验证。本记录是该新增范围的实施/验收记录，不覆盖原 FEAT-158 历史结论。

## 范围与设计

Profile 为 `demo_fast + local`。本次 `contract-impact=semantic`：增加可执行专家内容与固定的本地资产目录来源，改变其从展示到可选用的行为；不改变 `experts/1`、manifest v3 的形状、数据库版本、Runtime 权限或审批语义。权威源为 Skills 专家内容与规范打包产物；现有 Contracts 完整提交 `e35ae9a0711014e4774a1347413e9a343ce7ab2c` 保持。

复用唯一入口、ROLE、知识索引、受管安装、精确 ExpertRef、SQLCipher 绑定/outbox、Native 独占控制管道、Host 同 thread 角色组合和正常恢复。专家资源不进入全局 Skills。原 jd-ops-expert 0.1.3、38 普通技能和历史引用保持；不重置/降级数据库，不自动改绑旧会话。

| 专家 | 易界适配身份/版本 | 本次用户结果 |
| --- | --- | --- |
| 小红书爆款笔记策划 | xiaohongshu-copywriter / 0.1.0 | 根据用户材料生成选题、标题、封面文案、正文和标签；不声称实时热度或自动发布 |
| 漫剧编剧与分镜师 | agentgrid-comic-storyboard-director / 0.1.0 | 生成故事/角色约定和分镜 JSON/表；在当前会话工具权限内运行标准库校验器，报告真实校验结果；不生成视频 |
| 跨境电商运营专家 | cross-border-ecommerce-operations-expert / 0.1.0 | 完整离线商品/Listing/视觉文案/视频策划与推广建议；区分输入事实与假设，不伪造经营数据；轻流可选且不自动启用 |

三个运行版本独立于 WorkBuddy 原版本，原版身份/源摘要保留为来源证据。所有源说明作为待适配数据，不作为本轮执行指令。漫剧脚本只做正常文本/JSON 校验，不带网络、自动安装依赖或权限修改。

UI 仍为 11 张卡：4 位真实专家（原 1 + 新 3），其余 7 位展示专家。新三位使用真实 Native 目录、原资源准备/召唤/快捷问题流程；移除对应静态展示行，保留受控本地头像和易界三列设计。旧目录、服务错误或资源缺失时不伪造可执行卡。

## 状态与操作

- 资源可准备/处理中/已准备/失败由原服务状态投影；错误可沿原操作查询与恢复，不隐式重发。
- 选择只准备资源并更新草稿或原绑定；快捷问题只填入输入框。用户发送才执行任务。
- 空目录/搜索无结果/权限不足/Host不可用使用原 UI 状态；忙碌、审批、pending/unknown 阻止冲突切换。
- 同会话切换保留历史、重组新角色；解除才恢复普通基线；正常重开恢复精确绑定。
- 只有本轮既有会话工具和授权允许才写出或校验文件；选专家不扩大权限，不切换 full。

## 实施顺序与边界

Skills 新增受审资源和来源/本地授权记录 → 规范打包并逐项证明原39项不变 → Desktop 泛化单专家同步检查及固定新资产来源 → Host 固定新 manifest 并验证四位资源生命周期 → 原 canonical freeze/build → 真实日常客户端功能和保留验证。

用户本轮授权包含这些范围内的跨仓适配、规范构建和本机功能验证；不创建新仓/分支，不提交推送或发布，不改 Runtime，不开展第三方业务。模型验证采用现有受管模型，先限三条合成文本任务（一位一条）；不复用历史预算。若出现失败，先记录原因并缩小补验，不机械重发。无付费生成、供应商授权或真实商家数据调用。

工作区基线在 Desktop `.local/first-three-experts-20261016/baseline.json`。原有 UI/设计改动保留，原始专家资源目录不修改。正式测试前正常退出客户端并保存新一轮加密库/Host库及 Runtime、已安装资源摘要；不用旧验收基线替代本轮保留证明。

## Must AC

| ID | 可判断结果 | 状态 |
| --- | --- | --- |
| A1 | 四位真实目录 + 七位展示，无专家团/重复；新三位真实版本为0.1.0 | PASS：Native目录、实际卡片与去重测试 |
| A2 | 新三包通过规范打包与消费者校验；原 jd 完整元数据/归档、38普通包不变 | PASS：42项产物，原39项metadata/归档逐项不变 |
| A3 | 各位正常准备/选用，经既有 Native→Host→Runtime 发出任务，非UI模拟 | PASS：同会话3轮completed，19次真实工具调用均exit 0 |
| A4 | 小红书合成任务生成指定内容、遵守事实边界 | 部分通过：数量/格式/执行通过；事实保真FAIL，见下文 |
| A5 | 漫剧生成有效分镜文件并由受管脚本完成真实校验；不虚报结果 | PASS：4镜20秒无对白，实际脚本exit 0，独立重算一致 |
| A6 | 跨境运营缺少轻流仍完成离线策划，不伪造销量/媒体生成/外部写入 | 受测功能PASS；营销效果事实保真另有FAIL，见下文 |
| A7 | 同会话切换/解除、正常重开恢复、参考问题不自动发送，原普通提交链保持 | PASS：同一构建重开后3轮结果、跨境0.1.0绑定恢复，输入框为空且未发送 |
| A8 | 原数据库记录、原专家资源与历史保留；无旧 outbox 重发 | PASS：706条原行原值保留，7份旧rollout原样，原安装内容原样 |
| A9 | 正常缺字段/取消等代表性错误可理解并可恢复；相关 focused checks 通过 | 取消更换PASS；首次项目配置错误不够明确，保留为已知问题 |
| A10 | 正常客户端亮/暗与最小窗口可用；来源固定、构建回执、审查和限制有记录 | 部分通过：亮色三列、构建与审查完成；暗色/精确最小窗口未验 |

禁止强杀、故障注入、权限破坏、恶意归档/攻击 fixture 或运行时劫持测试；历史全量套件若包含这些行为则跳过，明确影响。验证只用正常应用操作、合成文本/JSON、只读保留对照及规范构建。

## 兼容与回退

不更改 SQL35/Host10。保留原专家所有精确资源和旧记录，新三位各自独立安装 ID。回退需保留新增 catalog/pin、资源及兼容 reader 才能继续执行新绑定；如关闭全局专家开关，已有专家会话保留可读并拒绝不兼容发送，不默降为普通会话。删除/升级继续遵守 retained 引用保护。

## 实际结果

三位专家的真实接入与实际执行已完成；本轮**不宣称全部 Must AC 或 D4 通过**。两份营销文案事实保真失败、既有配置错误的呈现、暗色/最小窗口覆盖仍有缺口。下面明确区分接入功能、模型内容质量和运行环境问题。

### 实现与构建

- Skills 增加三个独立 `ROLE.md`、唯一 `SKILL.md`、引用索引、任务参考、来源审计和本地使用授权。漫剧附 Python 标准库校验器、JSON schema 和正常样例；跨境包含六项任务方法，轻流为可选依赖。
- Desktop 的同步入口从原固定39项/1专家泛化为38普通技能与受限数量专家，仍验证权威声明、归档及摘要；UI仅新三位改用真实Native目录，头像仍受本地ID映射控制。
- Host 生产变更只有候选manifest摘要；没有新增第二套专家引擎，没有修改Runtime、数据库schema、权限或审批协议。
- 使用 canonical `chat-model-build-candidate.mjs --freeze` 与 `./scripts/run-local-demo-fast.sh --packaged`；后续仅 `--packaged --reopen`，没有替换受审Runtime或伪造二进制。该产物为dirty sibling工作树的本地开发候选，不是发布版。
- bundle版本 `0.5.0`；manifest SHA-256 `363fa8c3146fbef079dda840069853da7191a9e03c9fdd9a56b47e3856803818`；authority SHA-256 `3f7ce598fdf3cb66734e879ca0d9d50b482234fcd85f37a89dad1d23cae463bd`。
- 原jd归档SHA-256仍为 `baa8c8550b8b82b5f1be7bcfc59693c8920ff438fa854e84450936685e3d3b80`，版本仍0.1.3；原ROLE、knowledge及38普通包内容均不变。

本机证据根目录：`yijie-desktop/.local/first-three-experts-20261016/`。`packaged-launch-receipt.json`为实际构建回执；`canonical-build.log`和`reopen-final.log`为构建/重开日志；`integration-review.md`是独立子代理结构复核，不冒充人工批准。

### 三次真实模型任务

工作空间 `/Users/jack/Downloads/yijie-first-three-20261016`。同一Desktop会话 `01a14472-e0e4-7d33-95f0-48b0b60075c9`，Runtime thread `01a14472-e142-7c01-b26a-d79426fdcccc`。Kimi-K3，`ask / on-request`，`workspace-write`，Runtime网络关闭；三个submission均accepted，三个turn均completed，四条对应outbox均done且attemptCount为0。

| 专家 | 实际结果 | 运行证据 |
| --- | --- | --- |
| 小红书 | 5个标题、封面、正文、10标签及9项待确认信息；首轮94.659秒 | 3次读取安装目录index/note-method/editorial-check，全部exit 0；`xiaohongshu-completed.txt` |
| 漫剧 | 新建4镜、每镜5秒、无对白JSON和校验报告；99.988秒 | 10次工具调用全部exit 0，其中真实运行安装目录`scripts/validate_storyboard.py`；`comic-completed.txt` |
| 跨境 | 未连接轻流时生成英文标题/3卖点、15秒分镜、7天排期和待补数据；104.709秒 | 6次读取安装目录任务参考，全部exit 0；`cross-border-completed.txt` |

完整模型输入为 `functional-prompts-clean-workspace.json`。精简 `runtime-functional-evidence.json`只提取本次合成会话的公开工具命令、退出码、时间与权限，不含思维链、凭据或旧聊天。`native-success-metadata.txt`是正常停机后只读取得的本次提交状态/绑定摘要。没有平台发布、真实商家数据调用或付费媒体生成。

漫剧产物为 `/Users/jack/Downloads/yijie-first-three-20261016/comic-storyboard.json` 和 `comic-validation.json`。校验结果 `pass`、`shotCount=4`、`actualDurationSec=20.0`、`targetDurationSec=20`、零容差、errors/warnings均空。原始工具调用 `exec_command_11_9785f52c`确实执行受管脚本且exit 0；独立只读重算与报告逐字段一致。该通过只覆盖结构、引用、ID、版本、时长；未宣称自动验证全部叙事连续性或生成媒体。

**内容质量失败必须保留**：小红书输出“清洁少死角”“边角都能照顾到”“减少隔天串味”；跨境输出“rinse every corner”“helping reduce coffee residue and lingering odor”。输入只确认350ml及杯盖可拆洗，这些效果推断缺少证据，且模型自述“仅使用已知事实”不成立。两份结果的事实保真FAIL，不能用数量/格式通过抵消，也不能写成仅风格问题。本轮未偷偷更改已绑定0.1.0的精确内容；若改进，应建立新版本候选、重新评测并保留失败证据与旧引用。

### 会话与数据保留

实际完成小红书→漫剧→跨境切换、取消一次更换再重试、解除跨境后保留三轮历史、通过跨境快捷问题重新绑定且只填草稿；随后清空本轮验收草稿，没有额外发送。绑定最终为跨境0.1.0、revision4。`expert-unbound.txt`、`quick-prompt-not-sent.txt`均为完整AX快照；早期`quick-prompt-draft.txt`只有delta，不能作为完整证据。

最终使用同构建canonical `--packaged --reopen`，等待Host `/readyz`返回ready后打开本轮会话，3轮分别94/99/104秒的已完成结果和跨境0.1.0标签均恢复，输入框为空、发送按钮disabled。完整证据为`same-build-restored.txt`；没有追加模型回合。保留应用在该验收会话，便于直接检查。

本轮模型账本共4次UI提交：首次项目配置错误未进入Runtime；后续3次真实模型任务全部完成。没有重放首次失败，也没有删除该失败任务或改写历史数据。

本次19时验收正常Cmd+Q退出，canonical启动进程exit 0，Host端口和Desktop进程均消失后才读取数据库：

- SQLCipher schema35：原67表706条记录全部按原列逐行摘要保留，当前865行；原行缺失或变化为0。
- Host schema10：原9会话全部保留，新增1会话；其中4个旧会话仅`updated_at`因正常恢复而变化，其余字段不变。
- 7份旧Runtime历史文件逐字节不变，未发现旧回合重发；原33安装文件中32不变，唯一变化为正常新安装使用的`.yijie-state/operations.v2.db`，原jd与invoice内容/回执全部不变。
- 证据：`sql-preservation-after.json`、`host-preservation-after.json`、`file-preservation-after.json`、`normal-exit.json`；本轮原始备份保留在`preservation-before/`，未用旧验收备份替代。

### 检查、失败与未执行项

- Skills lint、16项测试/31条合成eval格式、补充7项内容测试、Contracts skills检查、规范42包打包通过；eval格式通过不等于真实模型质量通过。
- Desktop最终6文件95项UI/launcher测试通过（实际命令、exec 82614 / result 4c394c、exit 0见`frontend-deployment-final-verification.md`，明确为工具输出转录）；vue-tsc/Vite、设计文档build、ESLint、Rust fmt/Clippy、两个真实Native目录测试通过。
- Host lint、8项角色/会话测试（race）及实际四位准备/解析/提交/引用保护/移除/重开测试通过；原39目录升级到42目录保持jd精确引用、27文件/回执的测试通过。
- 元仓manifest lint、50项测试及shell语法检查通过。
- **保留检查失败**：早期`deployment-tests.log`为1失败/48通过，源输出路径期望修正后95项复验通过。Desktop `make lint`仍因旧Host不可变锁检查拒绝dirty Host失败；未削弱门禁，不声称全量lint通过，开发候选使用canonical本地候选校验。
- **项目目录问题**：首次将repo内`.local/.../task-output`作为工作空间，可信父级`.codex/config.toml`含固定Runtime不接受的`workspace`字段。隔离`config/read`诊断确认严格解析失败；未进入Host durable operation或Runtime模型回合，UI呈现“提交结果待确认/context_invalid”。保留错误任务，改用独立正常工作空间完成3次实测；未改用户配置、跳过严格解析或伪造成功。该错误文案与恢复缺口未在本次专家接入中修复。
- **退出异常**：16:31曾在正常退出时观察SIGBUS/SQLite WAL读取栈，报告`yijie-desktop-2026-10-16-163157.ips`。没有强杀或损坏文件；根因未确定，不能归因或宣称已修复。后续避免应用运行时跨进程检查SQLCipher，本次19时完整三轮后正常退出0，保留核对无损；一次未复现不等于根因闭环。
- **UI覆盖缺口**：实际亮色三列目录和详情可用，见`catalog-final-light.png`。当前设置/显示菜单没有应用内暗色切换入口，本轮未改全局系统外观；未完成暗色及精确1180×760窗口人工验收，不将组件测试代替该结论。
- **安全跳过**：未执行历史全量套件中可能包含强杀、故障注入、危险归档或权限破坏的项目，采用已审focused正常资源/会话路径。未验证平台发布、实时热度、轻流API、生图/视频或public/production发布；不在本轮范围。
