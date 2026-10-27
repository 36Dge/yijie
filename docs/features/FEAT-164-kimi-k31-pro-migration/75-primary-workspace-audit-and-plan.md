# FEAT-164 第75号：原主工作目录构建运行审计与方案

2026-10-28。**仅审计与方案，未实施。推荐在完整保全已有改动后，让原主工作目录承载已审查的FEAT-164来源，再新增明确的primary部署模式，直接从该目录构建和运行。** 不以原目录脚本转调旧`daily-source`冒充完成，也不以清空`.local`作为目标。

本轮只读核对12原仓、Git谱系/工作区、`.local`、来源回执及现存保全材料；只新增本报告、脱敏证据和私有审计文件。没有合并、切换、暂存/提交、创建worktree、生成/构建、运行App、模型调用、数据库API、服务启停、恢复或删除。原已完成FEAT-164范围及Owner接受替代/排除不变；这是后续主目录运行方案，不是重新声称旧验收失败或新方案已通过。

审计增量contract-impact=none。未来建议的primary准入为**semantic私有部署接口变更**，权威在Desktop部署规范、validator、launcher与receipt；公共模型wire/SQL/Runtime本身不因路径切换改变。若纳入未审WIP并改变公共wire或持久化，须对该新增范围重新分类，不能套用本方案的semantic结论。

## 1. 目标与必须明确的选择

目标目录是`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop`：它的实际`src/`、`src-tauri/`、`scripts/`是编译输入，构建由本仓canonical入口发起，运行的是由这份源码新生成、通过资格并绑定原日常Home的App。必要历史pin可继续使用，构建输出可位于原仓忽略子目录；这些不是另一份活动Desktop源码。

推荐首版保持已验收的FEAT-164产品行为、Runtime r5、writer4＋兼容reader5、原identity/Home和权限/计划保护。其它工作区改动完整保全，先归属审阅，未经采纳的不进入首版活动源码。**完整保留改动，不等于始终让所有旧dirty字节仍留作主目录的活动编译输入。** 未来必须明确批准“可恢复保全后改变主工作区的活动版本”；不能一边保留writer5作为活动源码，一边把构建称为原writer4资格。

可行选项与取舍：

| 选项 | 范围与结论 |
|---|---|
| A：已审FEAT-164基线在原主目录运行（推荐） | 先保全全部WIP，再经批准在原物理目录选择已审集成版本，未采纳工作留在独立保护提交/分支或私有备份；新增primary部署适配。范围最可控。 |
| B：原目录现有全部WIP一起整合并启用 | 须审查258条改动，包括writer5、Contracts0.5.0、检索与过程展示等，补齐各需求的契约/兼容/运行资格；不能仅当目录搬迁。 |
| 继续使用现有fixed-source | 可以保持已验收来源，但不满足本轮“原主目录直接构建运行”的新目标；不作为最终交付。 |

## 2. 当前仓库事实

12原仓HEAD、分支、远端、index、status与worktree注册已记录；五个直接相关仓有258条未提交/未跟踪路径。元仓另有243条原工作，合计501条原WIP；其余六仓工作区clean。本轮未改变这些状态。

| 仓库 | 原主目录HEAD | 已审集成/固定HEAD | 原dirty条目 | 与集成改动交叉 |
|---|---|---|---:|---:|
| Host | `d49c005` | `7309101` | 55 | 4 |
| Contracts | `5b5dad9` | `d5792d6` | 65 | 2 |
| Desktop | `fd0c575` | `a211c2d` | 100 | 17 |
| Connectors | `cc56cda` | 同HEAD | 37 | 0 |
| Skills | `595c927` | 同HEAD | 1 | 0 |

三仓原HEAD均为集成tip祖先，分别尚有4/4/17个集成提交；没有已提交历史分叉。旧“23文件”本次复算仍相同，但只是文件集合交叉，不代表23个必然Git冲突或23个Bug。12文件存在保守行范围重叠，其中11有不同编辑，1只有相同编辑重叠但文件仍有其它差异；另11范围分离仍需语义审查。本轮没有实际合并。

还有**119个非交叉dirty文件已在现行资格输入清单内且字节不同**：Host32、Desktop66、Connectors21；另有新未跟踪源码。该清单也包含测试/工具，不等于全部链接到二进制，但足以说明不能只合23个文件、沿用旧receipt。Contracts和Skills是权威来源，未落入单一Desktop输入map不代表无影响。

完整23文件清单、行区间/摘要和258条分类见脱敏[方案证据](evidence/primary-workspace-audit-plan.json)及私有Git审计；不手拼生成物或修改digest解决冲突。

## 3. 当前不能直接构建启用的原因

**P1-SOURCE：未审持久化语义。** 原Desktop `src-tauri/src/chat/native_conversation_storage.rs:11`为未提交`NATIVE_WRITE_FORMAT=5`；已验收固定来源写4、读5，44/116行通过`native_archive::decode_v5`保留旧历史伴随信息。原Contracts `scripts/sync-native-process.mjs:42`为未提交family0.5.0，固定来源37行为0.4.0。原database/renderer/Host链也有相关变化。这不是已证明的Bug，但不能随路径切换自动激活。选A则先独立保全这些变更；选B须追加source-first读写/重放兼容范围。

**P1-BINDING：部署规则明确拒绝原主目录。** 原主目录尚无最新版`feat164-daily-deployment.py`和installer。固定来源helper105/109行要求原Desktop与构建来源不同址、不嵌套，且schema仅1/2；137–159行再核验绑定、完整receipt、policy和helper源码摘要。不能复制旧binding、改路径或删断言后直接运行。

**P1-PROVENANCE：原工作区不是当前合格输入集。** Host校验同时核对commit对象与实际tracked/untracked输入；canonical重开还检查资源和receipt。独立19项`generate:check:feat164`要求相关仓精确pin、全仓clean，但不是每次reopen直接调用；专家Skills同步则每次要求精确HEAD/全仓clean。单纯“没有Git冲突”或“把所有dirty做一次提交”都不等于产品已审合格。

**P1-OUTPUT：旧产物不能被无意覆盖。** 原`src-tauri/target/debug/bundle/macos`已有8个App。launcher及receipt硬编码该位置，只设`CARGO_TARGET_DIR`会使生成与检查取址不一致。worker默认target还指向原Runtime的`codex-rs/target`；新primary必须显式隔离输出，保留旧App、worker manifest和Runtime审计产物。

**P1-RECOVERY：此前部分回退材料已不可按旧路径使用。** 顶层`FEAT-164-preservation-20261027`、旧顶层规划目录及桌面两个.command目前不存在；未调查原因，也未搜索Trash或恢复。此前批准的verification清理在实际删除前中止，不能把整个归档缺失归因本助手已完成该清理。现存原仓、6个保护tip、新集成来源和部分.local备份仍在；不存在的旧74归档/旧3bundle不能继续作为实施前可恢复证明。

## 4. .local盘点与必须保留内容

| 仓库 | .local分配占用约GiB |
|---|---:|
| Desktop | 24.330 |
| 元仓yijie | 16.853 |
| Host | 0.655 |
| Skills | 0.021 |
| Connectors | 约60KiB |
| 其余七仓 | 无.local目录 |

合计约41.86GiB，属于审计时du结果，不是可删除或可释放空间。元仓`daily-source`约9.647GiB，`consolidation-audit`约6.524GiB；Desktop多个Rust target和历史UI资源/证据目录也很大，但不纳入本次整合顺手清理。

必须原位保留：Native `~/Library/Application Support/com.yijie.ai/demo-fast-v1`；原Desktop `.local/demo-fast/{host-home,codex-home}`；Host原Provider secrets引用；Infra原workflow状态/凭据；Runtime `.yijie/build/kimi-k31-pro-r5/…`。这些不是源码缓存。ordinary Skills10c45be及Host1b7bfd1/96b1fa1等必要历史输入可复用、重新验证；两个约12KiB的Host稀疏worktree只存权威锁，不是损坏。

当前fixed-source有8个worktree、1246链接、0断链，唯一跨出源集的链接为Runtime到原仓；119个App文件、1228源码输入、receipt及schema2绑定本轮重新hash保持。但桌面入口缺失，不能据此称“当前桌面入口已可使用”，也未验证服务即时ready。

仍存并hash匹配：619,250,003字节的历史WIP/制品压缩包、3份新集成bundle、两份Finder增量；第71号四套sealed/inspection目录和manifest存在且manifest摘要匹配。没有读取数据库载荷，不能证明今日新鲜度，也不能据新bundle推定消失旧bundle的全部独立tip覆盖。

## 5. 推荐的最小设计（待批准）

新增显式primary私有部署模式，建议schema3＋独立policy；名称和字段在实施前冻结：

- v1/v2保持原分离来源语义，不改现有fixed-source的receipt/binding。
- primary明确绑定真正的原main working tree、源码根、精确提交/完整输入、原数据根及受控输出generation。仅允许批准的“源码根等于原Desktop”，不开放任意同址、别名、嵌套路径或任意ambient环境覆盖。
- 新generation仅存标准构建产物、bin、receipt及activation，可放在原仓`.local/builds/primary/<approved-id>/`；没有复制src或新建活动源码worktree。固定路径需由一处layout resolver供launcher/receipt一致使用，拒绝覆盖已有generation，与`.local/demo-fast`及旧产物不重叠。
- Cargo/Tauri App、Host/adapter及worker显式取本次输出；保留原`target/debug`。前端dist与Skills资源采用限定字段的canonical输出布局，或先完整保全后按明确清单复用标准再生slot；实施前必须选定并记录，不能隐含覆盖。推荐新generation独立输出，必要Tauri overlay只允许frontendDist/resources等列明字段，不开放任意配置。
- worker独立target不等于manifest已隔离：现`yijie-connectors/scripts/build-market-worker.sh`仍会更新`bin/market-worker/current.json`。推荐新增受控generation manifest输出，并同步Desktop读取/receipt路径；这使该Connectors构建脚本及相应验证成为P2条件文件范围，须先冻结其私有构建接口。若选择复用标准slot，必须先完整保全原manifest及内容寻址产物，再按明确批准更新；不能隐含覆盖或手写manifest绕过canonical生成。
- 保留原identity、Home、凭据引用、实例锁、业务审批、计划grant、K3退役、unknown不重发及ready-only门禁。primary不提供D3迁移；不搬库、不降schema、不删WAL。
- 每次重开继续核验真实输入/制品/环境；缺失或漂移则停止，不能自动更新摘要或生成D5授权。新位置必须取得自己的D4/D5资格，不能套用71号实际运行摘要。

首版以仓内命令为入口，**不自动重建用户已移除的桌面.command**。建议接口如下，当前尚不存在、不得当作已可用命令：

```text
# cwd = 原 yijie-desktop
pnpm daily:prepare --generation <approved-id>
pnpm daily:open --generation <approved-id>
pnpm daily:open --generation <approved-id> --pause-kimi
```

别名须调用本仓canonical launcher，从指定generation读取经批准的binding/env/digest；不能转调旧fixed-source，也不能默认取得日常启用权限。若以后需要桌面快捷入口，另列安装范围。

最小新增适配候选文件为Desktop的`feat164-daily-deployment.py`、`run-local-demo-fast.sh`、`kimi-k31-packaged-receipt.mjs`、`package.json`、共享primary layout/有限overlay工具及相应安全测试/部署文档。`check-feat164-generation.mjs`、Host冻结锁及必要consumer pin仅按新已审提交canonical更新。`install-feat164-daily-entry.py`为可选。公共契约源仅在实际wire变更时另改；**不计划修改Runtime核心/补丁或Native SQL迁移**，发现确需修改即停下另报。

## 6. 分阶段实施与授权边界

| 阶段 | 工作及交付 | 退出条件 / 明确不包含 |
|---|---|---|
| P0 重新保护 | 当前501条WIP、索引/引用、关键制品及独立tip完整保全，重做bundle并独立恢复验证；记录旧归档缺口 | 验证真实可恢复；历史备份不冒充今日新备份。不开日常库、不改源码活动状态 |
| P1 选定活动来源 | 为五仓258条WIP逐项定归属/采纳/保全位置，23交叉逐段审阅；按Contracts→Host/Connectors/Skills→Desktop闭合来源。经批准将原物理目录切换到已审版本 | 原工作保留在可恢复提交/分支或私有备份；敏感材料不进Git。未采纳writer5/其它工作不自动激活；不使用reset/stash/整文件覆盖绕过审阅 |
| P2 primary规则与安全离线验证 | 先冻结私有部署规范/普通样例，再实现限定layout、receipt、入口及来源锁；旧schema兼容与原Home不变量验证 | 只实现及合成/离线验证，不启动日常App、服务或模型 |
| P3 原目录构建资格 | 从真实原主目录canonical构建新generation，完成必要生成/编译/来源/离线检查和prepare-only重开 | 回执显示真实主源码；不依赖旧fixed-source活动App/Host/worker；旧制品保留，0模型/0日常数据运行 |
| P4 日常受限资格 | 另批后正常停机、锁/无占用、新完整冷备份和副本预检、全模型无待派发、既有workflow真实ready；Kimi暂停，历史/权限检查与正常退出/后态 | 0新增模型HTTP；依赖未ready另列恢复授权，不隐式up；不强杀、不故障注入、不删WAL |
| P5 明确启用与入口观察 | 对新source/receipt绑定D5，仓内正常/暂停入口实际运行和正常退出验证，记录兼容回退 | 当前源与运行资格明确、旧source可受控回退。无新增模型验收调用，不自动清理旧source |
| P6 可选后续清理 | 如仍需要，再审计旧daily-source/.local项的归档、反向依赖与精确删除清单 | 独立批准；不是本轮目标的自动授权 |

建议下一轮先批准并完成**P0—P1**，交付“原工作可恢复、主目录选择了哪些内容、哪些未采纳WIP仍保留”的精确清单。新部署语义及代码范围P2在实施前确认；P4/P5涉及原日常数据/启动与启用，应以实际新候选为对象再批准。若选择B同时启用未审WIP，先重新评估Contract First和持久化范围，再改本表，不以扩大测试数量代替需求决定。

### P1的保存和切换方式（仅提案）

可提交的源码WIP按归属形成独立本地保护提交/分支，不能把WIP提交当作功能验收；凭据、数据库、缓存及不宜进入Git的材料保留在私有完整备份。每个未采纳路径都列出原内容摘要、恢复位置及是否移出活动输入，禁止丢弃。只有工作树中需保护的未提交内容全部得到可恢复处理后，才可经明确批准正常切换到已审分支，让该版本成为原目录的实际文件；不是在dirty状态下强行覆盖。`.local/demo-fast`等日常状态目录原位保留。23交叉文件的“处理”可以是明确不纳入首版并保全，不表示强制把两侧功能一起合并。

## 7. 验证要求、停止条件与回退

验证以普通安全样例覆盖旧schema1/2兼容、primary合法路径/摘要/代际匹配、普通无效参数拒绝、原Home绑定、D3禁止、输出无覆盖、来源漂移拒绝、prepare-only零启动、既有ready-only及正常退出。随后执行适用的源生成/完整来源、lint、类型检查、构建、Rust fmt/Clippy和安全聚焦测试；不运行历史攻击/故障注入用例。整项已接受的never-sent替代、完整App正向取消NOT RUN、搜索质量/亮暗/键盘/最小窗口专项OWNER_EXCLUDED保持，不重新安排。

无法证明WIP可恢复、出现未审writer/权限/wire变更、来源/pin漂移、需要覆盖未知/受审产物、实例占用不能正常退出、数据或依赖未知、出现额外模型派发，都应停在对应阶段审计。三次同点失败按项目熔断规则处理。不得把工具失败改写为PASS。

切换前保留现有fixed-source及其合格App/binding。新primary失败时，先正常退出，核验当前数据兼容、备份与原来源，再选择受控旧来源；桌面旧入口已缺失，不能承诺直接点击回退，也不自动重建。源码回退使用已批准的保护提交/完整备份，不抹去未采纳工作；不恢复旧DB覆盖新记录、不降schema、不重跑D3。

本报告不是实施批准。本轮原仓与日常数据不变、0模型调用、不推送；未做新主目录构建或运行验证，具体审计与保护记录见[方案证据](evidence/primary-workspace-audit-plan.json)。

## 本轮方案复审与文档检查结果

Git/WIP方案复审通过；部署方案复审建议已补入worker manifest保护/输出范围及never-sent替代的精确表述。它们是工具辅助复审，不冒充独立人工批准。元仓lint、57项治理测试、claims、strict/G6及7份Shell语法通过；这些仅验证文档/既有治理主张，不代表新primary模式通过构建或运行验收。

结束时12原仓的HEAD、分支、远端、refs、index、worktree注册和原状态保持，501条原WIP文件记录逐项复核保持。元仓只新增本报告和方案JSON，均未暂存或提交。私有分项报告、源/回执核验、.local用量、保全材料摘要及检查日志位于`yijie/.local/primary-workspace-audit/20261028-01/`。
