# FEAT-165 文档验证与功能验收

2026-10-28。用户已确认D0并授权实施；下文第1—2节为需求阶段历史记录。已完成12格式真实接收、预览/保存、正常重开及拖入根因修复；上轮状态见第10节，2026-10-29续验见第11节及03审计。Owner已先新增5次、再新增10次，累计上限20次，使用明细见机器账本。Owner分层接受与D4结论见第11节末；本次最终审计与本地提交见04。其它Feature历史PASS不继承。

## 1. 第一轮实际文档验证（历史证据）

CWD为`yijie`。以下均为第一轮实际执行，机器结果摘要见[documentation-checks.json](references/documentation-checks.json)。

| 检查 | 退出码/结果 | 证明范围 |
|---|---|---|
| `bash docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --strict docs/features/FEAT-165-native-artifact-files-and-preview` | 0 / PASS | 四文件结构、模板及未完成标记检查；不是D0批准 |
| `node docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs --audit-claims docs/features/FEAT-165-native-artifact-files-and-preview` | 0 / PASS | schema v3及实际声明一致；未声明D0/D4通过 |
| `pnpm lint` | 0 / PASS | 11仓manifest与中央/11兄弟仓治理规则存在性 |
| `pnpm test` | 0 / 57项通过 | 元仓既有Feature治理/manifest测试，不是产品测试 |
| `bash -n scripts/*.sh` | 0 / PASS | 元仓Shell语法 |
| `git diff --check` | 0 / PASS | tracked差异；本轮untracked文档另逐文件查尾随空白/链接 |
| 新包本地链接、尾随空白、5图SHA-256 | PASS | 本需求文档与原图一致性 |
| 四产品仓HEAD/status及元仓并行变化审阅 | PASS（按实际范围） | 产品仓未变；元仓FEAT-162由其它工作推进，未回滚/覆盖，不能称全仓字节不变 |

`pnpm test`执行前已审入口；仅治理纯值/临时普通文档与canonical新包脚本，没有强杀、权限破坏或攻击载荷。完整业务测试均未运行。第一轮实际结果及当时复审记录见原始documentation-checks.json；第二轮当前修订见01第5节，不重写第一轮结果。

## 2. 第二轮文档审计与验证

当前修订已按三路只读发现及主Agent交叉核对收敛，12项修正见01第5节。Desktop/Contracts分别再审四文件，结论为无阻断本次需求修订的问题；最后补齐Desktop私有附件IPC权威、修正初轮历史索引，均只改文档。初态与修改前摘要见[reaudit-source-snapshot.json](references/reaudit-source-snapshot.json)，第二轮实际命令见[reaudit-documentation-checks.json](references/reaudit-documentation-checks.json)。

| 本轮实际检查（CWD=yijie） | 结果 | 边界 |
|---|---|---|
| Feature Package `--strict` | exit 0 / PASS | 文档结构，无D0批准 |
| validator `--audit-claims` | exit 0 / PASS | 实际状态/声明一致，不含功能PASS |
| `pnpm lint` | exit 0 / PASS | 11仓manifest和治理规则 |
| `pnpm test` | exit 0 / 57项通过、0失败 | 本轮新运行的元仓治理测试，非产品测试 |
| `bash -n scripts/*.sh`、`git diff --check` | exit 0 / PASS | Shell语法/已跟踪diff；新包另查空白 |
| 12扩展/10项AC与YAML、未执行状态 | PASS | 正文与机器索引一致 |
| 本地链接/空白/5图摘要、五仓HEAD/status | PASS | 参考图未变，产品仓clean且HEAD不变，元仓仍仅本目录untracked |

不把这些结果或第一轮历史结果当作任何产品AC/D4。新契约生成、业务focused、App/Runtime与模型调用均未运行。

## 3. 原始 focused 验证计划（历史；当前结果见第9节）

| 面向 | 必须验证 | 对应AC | 状态 |
|---|---|---|---|
| 输入Contracts/包装 | StartTurnV2、chat/message历史metadata、market-selection、market-host不可变submission/HMAC、experts引用全部同源；SVG视觉与file身份分离、MP4说明不是原文摘录 | 001/004/009 | NOT RUN |
| 输出Contracts/私有IPC | 公共media源与派生事件/policy、私有file/image/video预览保存源各自一致；HTML既有漂移在同表面收敛；版本准入不是新动态协商框架 | 001/005/006/009 | NOT RUN |
| Host/Runtime复用 | publisher start/resume发现、受限draft禁用；已有provider独立身份/provenance、伴随流合并、同路径幂等/冲突；不在K31启用被禁dynamic tools | 001/008/009 | NOT RUN |
| Native输入 | Desktop私有chat-ipc-v2源及Rust/TS一致；12扩展、原子批次/失败重选、SVG/MP4 file非空上下文；临时路径与hover仅draft/context受权 | 001/002/003/008 | NOT RUN |
| 真实用户消息组合 | 现有视图adapter按明确本地绑定组合native正文/附件；提交→观察→历史分页无重复，只有Runtime冷历史不猜附件 | 004/007 | NOT RUN |
| 文件信息与内容预览 | Office/PDF信息卡＋保存；TXT/CSV/MD有界投影，1MiB源准入与投影截断不同；HTML/SVG/MP4原组件正常能力 | 005/006 | NOT RUN |
| 保存与恢复 | 原件摘要/.jpeg别名/原生dialog取消覆盖；Native提交后ready/ACK重试，只有已提交资源正常重开；Host丢失暂存如实 | 006/007/009 | NOT RUN |
| 基础交互 | 胶囊长名/同名/换行、tooltip与图片浮层互斥、焦点/Esc/换会话释放、主题与窗口 | 002/003/004/010 | NOT RUN |

运行前审测试入口，仅用普通文件、纯值/reader组件测试及正常生命周期，不跑历史攻击/权限故障/强杀fixture。所有产品focused均未运行，具体命令取最终真实实现路径，不能现在填造结果。

## 4. 真实服务验收计划及AC（原计划；当前结果见第9节）

1. 后续用户授权开发/验证时，按实际数据范围使用既有canonical Desktop/Host/固定Runtime组合，核就绪、来源及正常退出。不得直接开日常重要库试错或另造第二产品App。以同次fresh run覆盖目标真实路径，普通focused状态检查标明层级。
2. 12扩展分批逐一导入/识别/发送（最多10件/批）。单DOCX+正文、单HTML+正文、多件与纯附件、长中文名/同名不同路径；至少覆盖新普通聊天、既有专家聊天及现有工具选集提交路径。不得为通过文件类型验收新增外部工具发现/商家调用。
3. 验证4图片扩展hover/focus和非图片来源路径；SVG视觉图片但实际file上下文。移除/切换/发送/权限失效释放临时信息，重开草稿无路径时如实显示。超数量整批拒绝、普通不支持类型失败后移除重选，已有草稿/正文保持。
4. **12种输出都经真实原生产物入口接收**，不等于建设12类生成能力。普通合法样本可由现有canonical工具产生，或将已备公开/合成文件置于受管工作区后由真实Runtime正常调用publisher；不得seed数据库、注入伪事件或以模型链接代替登记。至少一个代表性文件任务验证“现有工具生成→登记→Native提交”的真实闭环。二进制图片/视频不要求新增付费生成商、编解码器或模型视频能力。
5. 保留已支持provider原链和artifactId/provenance，混合producer排序/不重复登记用适用配置的普通focused检查覆盖；若未触及既有provider实现，不为此强制再付费生成。真实provider调用只在当前受支持配置及明确授权下执行；不能在K31候选打开被禁dynamic tools，也不把未运行的provider实测写PASS。新普通/既有专家publisher发现均复用start/resume。
6. 实际观察本地发送→native userMessage到达→正常重开/分页的独立展示/允许同气泡、原生userMessage不变及无重复。用真实已有绑定核验；无本地绑定冷历史的降级用普通reader/组件检查，不拼造Runtime Item或关联。
7. 按R-01逐格式判定卡片与内容预览：DOCX/PPTX/PDF必须有真实名称/类型/大小/状态及原件保存，明确不支持内容预览；TXT/CSV/MD在现有限额内展示，超源上限明确提示并可保存；HTML普通自包含交互、SVG缩放、MP4实际音画/seek/关闭停止。metadata/截图不能代替音画。不要求Office/PDF全文或新增转码。
8. 12扩展逐一原生另存并核对完整原件字节/SHA-256、合法后缀（含.jpeg）。正常取消与同名选择/取消由系统对话框承担，验收最终字节和未授权覆盖未发生；不增加自建二次确认，不改用户原件制造失败。
9. 正常退出/同构建重开，只有已Native提交且未过期的附件/产物应恢复，0自动派发。ACK失败用普通状态检查证明沿既有pending ACK恢复，不强杀/断进程制造它；Host重启清暂存、内存流过期的未提交资源只说明无法恢复，不自动读盘重建。过期/缺失优先自然记录，无记录时普通纯值reader/组件检查，不改系统时钟/权限/数据库。无覆盖AC-007不得PASS。
10. 同次fresh run验证现有主题/最小窗口/键盘关键操作及正常资源释放，保存逐格式结果与安全截图/receipt。后续费用必须属于本需求明确授权，不借其它Feature预算。

| AC | 当前结果 | 未来证据重点 |
|---|---|---|
| AC-001 | NOT RUN | 12输入/12输出实际接收、代表性生成、普通/工具/专家输入来源 |
| AC-002 | NOT RUN | 胶囊与临时来源路径作用域 |
| AC-003 | NOT RUN | 4图片扩展hover与正常释放，SVG为file语义 |
| AC-004 | NOT RUN | 提交/native观察/重开分页正确独立展示、原生userMessage不变、无重复/猜关联 |
| AC-005 | NOT RUN | 12格式分级预览卡，内容能力和限制真实 |
| AC-006 | NOT RUN | 12扩展原件摘要、.jpeg合法别名、系统取消/覆盖 |
| AC-007 | NOT RUN | 已提交恢复，未提交/过期/缺失如实且无重生成 |
| AC-008 | NOT RUN | 原子批次、普通失败/恢复、原状态与幂等保持 |
| AC-009 | NOT RUN | 全部权威输入包装/reader、已有producer、原生机制复用 |
| AC-010 | NOT RUN | 基础交互可用与租约/临时信息正常释放 |

普通fixture只证明所测reader/纯值/组件层，不代替真实文件接收、代表性生成、正常重开或音画/另存。任何内容/调用未实际覆盖都要如实列明，不能以省事或缩减成本删12格式接收目标。

## 5. 当前实现验证（2026-10-28）

当前机器记录见[implementation-validation.json](references/implementation-validation.json)，包括完整commit/工作树状态、日志摘要和canonical App构建回执摘要。Contracts精确提交为`61137174a25dc368e0006f27633fd4a9ad097aa6`（仅本地，未推送）。Host/Desktop实现仍为未提交本地候选，Connectors仅来源锁更新；原生userMessage类型与yijie-codex源码未改。

| 实际检查 | 结果 | 范围 |
|---|---|---|
| Contracts 31个schema、8项专项及全部受影响source-lock闭包 | PASS | v9不扩新输出；v12明确新文件；输入及model/market/expert引用一致 |
| Host `go test -race ./internal/session -run '^(TestFEAT165Normal\|TestArtifactMediaNormal)' -count=1`，配置普通12格式样本目录；`go vet ./...` | PASS | 正常登记、原件读取、ACK、幂等、v9隔离和既有媒体；非真实模型 |
| Native normal专项4项 | PASS | 12格式导入，图片有界投影，MD预览、Office保存边界，草稿元数据读，v41→v42不新增表 |
| Native `media_normal_commit_save_and_reopen`，同一12格式样本目录 | PASS | SQLCipher提交、原子保存字节不变、正常重开、MP4范围读 |
| 前端4个相关suite 54项＋IPC权威源对齐2项 | PASS | 输入capsule、浮层状态/迟到响应释放、原生消息和本地附件独立呈现、旧Composer回归 |
| Desktop `pnpm lint`、Native `cargo fmt --check` / `cargo clippy --lib --features kimi-k31-pro-candidate -- -D warnings` | PASS | 静态检查与编译；不是UI人工/真实运行资格 |
| `env YIJIE_KIMI_K31_CALL_SURFACES=media ./scripts/run-local-demo-fast.sh --packaged --kimi-k31-pro --prepare-only` | PASS | canonical候选构建及现有完整来源检查；App未启动、模型请求0 |
| 元仓严格检查、claim audit、lint及57项治理测试 | PASS | 文档与治理声明一致，不将专项冒充D4 |

用户执行中进一步明确：原生userMessage类型不得改变，不强制与文件同气泡；已落实原生消息/本地附件分开保留，参考[图6](references/06-separate-message-display.png)。上述单元/集成检查使用普通合成样本，尚不能代替真实App中的hover、键盘、另存对话框、HTML交互与MP4音画验收。

## 6. 恢复执行前的未执行记录（历史）

| 项目 | 原因 | 影响 |
|---|---|---|
| 真实App启动、视觉/原生对话框/播放与真实模型生成 | 候选已构建；用户已批准最多3次真实任务后要求暂停，现已恢复。恢复前确认尚未启动候选、已用0/3 | AC整体/D4仍NOT RUN；不声称实际界面或生成可用已验收 |
| 历史全量safe生成及全量breaking通过 | 完整生成器仍有未解析的model-selection引用；全量breaking停止在scheduled-task draft-execution引用，详见Contracts说明 | 聚焦源闭包/专项PASS不替代完整基线检查，未声明全部generate/test/breaking通过 |
| 全量业务测试中的攻击/故障注入项目 | 用户永久禁止强杀、权限破坏、二进制劫持及攻击fixture | 仅执行明确的正常样本/纯值检查；相关攻击测试覆盖不宣称通过 |
| 日常数据库迁移/回退、公开/生产部署、其它仓Git提交/推送 | 未授权且不在本次local候选范围 | v42只用于授权的样本候选；代码明确阻止当前daily profile迁移；无上线结论 |

## 7. 恢复执行前状态（历史）

D0已由Owner确认，implementation active；Contracts源及实现候选已形成并完成上述专项验证，canonical App build PASS。真实App/模型验收已授权，恢复执行前已用0/3，全部Must AC最终结论及D4保持NOT RUN，DP N/A。不把构建/组件测试当作真实UI、实际模型生成或独立人工审阅。


## 8. 前三次任务检查点（历史；问题已在第9节复验）

| 层级/场景 | 结果 | 当前实际证据与限制 |
|---|---|---|
| canonical App启动与正常退出 | PASS | 同构建reopen来源校验通过；两次Cmd-Q清理均正常，无强杀 |
| 12种输入格式 | PARTIAL | 已分两批通过原生选择器导入并真实发送；普通6种、专家6种。拖入、全部键盘/长名等仍待覆盖 |
| 专家创建真实生成与接收 | PASS（场景） | 7个ready卡片，含Runtime新建36-byte Markdown；不代表全部AC |
| 专家续聊剩余6格式 | FAIL（本次实跑） | 5个staged未Native提交，PPTX未登记；根因空terminal已修，待新构建实跑复验 |
| 绑定与重开 | PARTIAL | 普通历史原文/附件正确，原生userMessage未改；专家资源正常重开待验 |
| CSV预览/原生保存取消 | PASS（场景） | 实际表格与取消反馈；尚未成功另存任何文件，摘要比对NOT RUN |
| Host/Native正常连续流 | PASS | Host27条正常事件含24个artifact生命周期；Native完整解码本次365条两轮回放，8项测试通过 |
| 前端/静态检查 | PASS（专项） | 15项绑定/胶囊＋Markdown正向解析；lint/Native clippy/Host vet，日志见references机器记录 |
| 最后修复App打包/UI复验 | NOT RUN | Mac锁定，需手动解锁并正常退出当前App后沿canonical重建；不强杀或覆盖运行中的bundle |

真实任务额度已用3/3，不再自动提交。未完成逐格式保存/HTML交互/视频音画/专家恢复等检查，全部Must AC最终状态仍pending，D4 NOT RUN。第6节“尚未启动/0次”是恢复前历史检查点，以本节为最新状态。原始首次生成失败、全量breaking/生成阻塞及安全跳过记录保持不变。


## 9. 验收检查点（2026-10-28，拖入修复前；最新见第10节）

**D4未通过。** 真实任务累计5/5，全部已完成；不再自动发起模型任务。12种文件均真实导入发送并经publisher到Native提交。专家13份输出和普通新生成Markdown在正常退出/最终同构建重开后恢复；原生userMessage类型、wire、存储和Runtime源码未改。机器证据见[implementation-validation.json](references/implementation-validation.json)的`final_ui_checkpoint`。

| AC | 当前结论 | 实测与边界 |
|---|---|---|
| AC-001 | pending | 12输入/12输出、普通与专家真实生成/登记/Native ready通过。现有工具选集共享契约闭包已验证，但未另做选集真实提交；Finder跨应用拖入未实测，原生选择器已逐项验证 |
| AC-002 | PASS | 1180×760实际长中文名保留扩展名、两同名异路径分别显示a/b路径；局部移除、十件换行、无来源路径提示和正文保留成立 |
| AC-003 | PASS | jpg/jpeg/png/svg逐一真实focus图片浮层、Esc关闭；切换会话释放；MP4输入只有信息，不自动播放 |
| AC-004 | pending | 单长DOCX+正文、单HTML+正文、多附件、普通/专家重开无重复和上下文包装；唯一明确提交绑定及冷/歧义历史纯值测试通过。纯附件无文字真实提交、实际触发历史分页未覆盖，不冒充通过 |
| AC-005 | PASS（分级范围） | Office/PDF信息卡和保存；TXT/CSV/MD实际内容；HTML按钮交互；SVG125%缩放；MP4画面、Play/Pause、seek、切离关闭及用户确认测试音。超源预览上限依赖既有reader限额，未另做真实模型超限产物任务 |
| AC-006 | PASS | 12扩展原件逐件保存且摘要一致，另含两份真实生成MD；.jpeg保留；系统Cancel/Replace取消、改名和切换目录保存成功；真实PNG预览错误时仍能保存原件 |
| AC-007 | PASS | 最终候选重开13份专家产物和普通生成物、原附件/原文，无自动派发；过期/缺失只用普通reader错误码组件状态覆盖，不改时钟/数据库/权限；不承诺未提交staged恢复 |
| AC-008 | PASS | 12件整批超限拒绝后6件重选；最新十件混合正常导入；.log在原生选择器置灰，取消后原附件/正文保留；真实图片重载恢复、系统保存取消/重试成立 |
| AC-009 | PASS（local候选） | 固定Contracts6113717、v12显式消费/v9隔离、源闭包与正常Host/Native测试；沿publisher/spool/ACK/既有预览保存，Runtime clean。未执行外部provider；全量生成/breaking既有引用阻塞仍未解决，不能据此声称生产兼容 |
| AC-010 | PASS（已实测界面） | 实际1180×760亮暗布局、十附件、图片浮层、文件卡片及图片弹窗工具栏；焦点/Esc/取消可用。用户批准临时macOS深色，检查后已恢复原浅色。拖入仍归AC-001未验 |

最近根因修复及证据：

- 图片原件保存不再依赖缩略图成功；仍由Native授权/完整性校验。真实PNG预览失败状态另存成功，字节一致；3项普通图片组件测试通过。
- 图片lightbox Teleport脱离原容器导致按钮样式丢失，反馈宽度又挤出缩放工具；局部样式同时覆盖弹窗并允许工具栏换行。最终真实SVG125%与取消保存反馈无重叠。
- 四图片历史重开稳定出现后两张加载失败。原生图片协议会先消耗一次性handle，再因已有2个读取直接拒绝。参照现有视频reader，在消耗handle前有界等待读槽；仍为2并发/40MiB、4个pending、10秒等待，排队后重新取当前时间并走原授权校验，不加服务、不扩读取权限。普通四并发测试通过，最终真实历史四图片一次全成功。
- Host v4 phase→v3 media、Native允许空terminal两处修复的首次失败仍保留；第4次专家续聊实收全部剩余6格式，第5次普通聊天新生成262B Markdown并Native ready。
- 两次早期“切换目录后点击保存”未观察到文件或反馈，未记PASS，也无足够证据归因为产品故障。最终用系统面板实际改名/切换新目录并点击Save成功，字节核对一致；不为未复现现象添加猜测性修复。

最新检查：Native四图片并发1项PASS；普通过期/缺失组件4项PASS（2个文件/Shell状态＋2个图片错误码）；新build前lint、Native clippy -D warnings均PASS；canonical `--prepare-only`和同构建`--reopen`通过。前序8项Native、Host race、契约8项、54项UI及后续15项绑定检查仍保留各自源码检查点，不伪称全量业务测试。

剩余项：真实Finder拖入、工具选集真实提交、纯附件无文字真实提交、实际历史分页。拖入工具只能取得各App独立窗口坐标，当前未可靠建立跨窗口目标位置；未用系统脚本绕过CUA。新增模型任务须先扩展已耗尽的5次授权。不得以组件测试或选择器操作代替这些实跑结论。日常迁移、外部MCP/provider、公开部署及禁止的攻击/故障测试均未执行。


## 10. 用户真实拖入失败反馈与继续诊断

用户报告sample.csv拖入未成功，且没有提示或高亮；当前界面仍9个附件、原文保留。AC-001由未验改为FAIL，不能沿第9节把拖入继续称作未尝试。已复核锁定Wry/Tauri源码，macOS逻辑点并未转物理像素，不做猜测性倍率修补。正在用现有Web Inspector/事件订阅进行只读观察，只输出真实drop的文件数量、坐标及DOM边界，不打印路径或文件内容、不造事件、不调用导入命令、不发模型任务。临时观察器将在正常App生命周期清理，待下一次真实拖放定位。


### 10.1 已定位并修复事件目标不匹配

实际原生日志有4次`surface=webview`的drop，每次1个文件；Window层没有drop。前端Any-target观察收到相同坐标，均落在composer `(374,266)—(1134,642)` 内。这直接排除了当前症状由坐标倍率、文件类型或剩余容量引起：页面订阅`getCurrentWindow().onDragDropEvent`，但本构建发出WebView-target事件，过滤后页面永远收不到。

改为官方现有`getCurrentWebview().onDragDropEvent`，完整复用现有命中检查和Native导入。没有扩大监听权限、增设DOM导入分支、调整倍率、添加新IPC或修改Runtime。原单测将回调直接挂在Window mock上，不能检出真实事件目标差异；现将两个target拆开，断言只订阅WebView，并验证范围命中/不可发送/发送中三种普通状态，3项PASS。

证据：[drop-root-cause.json](references/drop-root-cause.json)。临时原生logger已从源码移除；候选正常Cmd-Q exit0清除了只读JS观察器。最后canonical构建及真实拖放复验仍进行中，AC-001保持FAIL直至真实复验成功，不以单测替代。没有新增模型提交。


修复版后续检查：另5项连接器选择/草稿回归PASS；lint、canonical打包及同构建reopen PASS。最终运行版本不含临时logger/观察器，9份附件已正常恢复，等待用户真实CSV拖入反馈后再更新AC。任务预算仍5/5，无新提交。


### 10.2 真实拖入复验通过（2026-10-29记录）

用户确认“出现了 CSV 胶囊”；CUA核对新任务草稿共有10个附件，其中包含sample.csv，没有点击发送、没有运行任务。拖入场景记PASS，AC-001回到pending，因为工具选集真实提交仍未覆盖。保留前述失败和根因证据。

附加复核发现CSV来源路径曾从可见变为“当前草稿来源路径不可用”；普通选择器重导也再次观察到。只读Native查询确认来源路径为空，草稿仍ready，前端观察未发现context或发送状态变化。AC-002暂退回pending，继续定位清理来源；不靠猜测延长保留或放宽授权。本轮新增模型任务0。


### 10.3 无诊断最终候选与当前结论

临时来源路径诊断中的新CSV记录始终存在、context/draft匹配且未过期；多次正常展开和应用前后台切换均返回真实路径，没有观察到该轮导入后被清理。此前“路径不可用”提示与一次只读缺失观察保留为未确认现象，不能据此断言缓存清理根因，也没有添加猜测性修补。诊断源码已完全移除，与诊断前Native源码逐字节相同；观察器随正常Cmd-Q exit0清理。

最后沿canonical重新构建及同构建reopen通过。最终无诊断候选正常恢复10份草稿；仅移除并重新选择合成sample.csv，等待实际导入完成后，路径浮层显示正确；Esc关闭、切到Finder再回到易界后再次展开仍正确。没有发送任务、没有追加费用、没有修改Runtime/userMessage或持久化路径。AC-002恢复为按已实测范围PASS；不把未确认现象说成已定位修复。

当前结论：真实Finder拖入PASS；AC-001与AC-004仍pending，其余8项维持所列范围PASS，D4仍未通过。剩余工具选集真实提交、纯附件无文字真实提交及实际历史分页。现有本轮专家历史3轮，小于正常页面20轮的分页阈值，没有通过更改阈值、写入伪历史或额外付费凑数制造分页通过。模型任务额度5/5已耗尽，后续付费提交需要新增明确授权。

本轮核验：拖放target/准入3项、连接器草稿回归5项、Desktop lint及canonical构建/重开PASS；元仓lint、57项治理测试、Shell语法和需求包严格/claim检查PASS。源码diff无临时logger/观察器，Contracts与Runtime仍clean；没有新的Git提交或推送。最新日志摘要与活动候选状态见implementation-validation.json的source_path_followup和drag_drop_followup。


## 11. 2026-10-29续验与审计

Owner先新增5次、后再新增10次真实任务，累计上限20次。第6次工具选集+CSV/SVG、第7次普通续聊纯TXT均完成；两轮原生Item仅userMessage/reasoning/agentMessage。正常退出、最终canonical构建/同构建重开后两轮三附件和原文正确恢复，纯附件无空正文/重复气泡、无自动派发。使用7/20，尚余13次，不要求耗尽。

实际Native分页两页各1轮、游标前进/集合不重叠、原turn绑定正确，重复原生读取相同、现有历史不变。新增正常store分页+重开组合测试1项PASS，158无关项目未运行。真实UI每页20轮、当前只有2轮，加载更多按钮未实测；已向Owner提出分层接受问题，答复前AC-004 pending、D4未通过，不能以诊断调用冒充UI按钮操作。

本轮发现并修复Design Pattern遗漏，详见03；未发现新的已确认产品缺陷。路径不可用的前序未确认观察仍保留。首次测试类型拼写错误被lint检出，修正测试后lint及定向测试通过。31 schemas/8契约专项、媒体生成check、两个基线JSON Schema及受影响OpenAPI比较、v9字节保持通过，本地契约资格收口PASS；其它族的完整生成/breaking失败保留，不改变生产限制。

当前AC-001/002/003/005/006/007/008/009/010按各自范围PASS；AC-004等待Owner对分层验收方式的明确决定。完整细节见[03审计与续验](03-current-audit-and-next-steps.md)及机器记录resume_20261029/local_contract_review。


### 11.1 Owner接受分层验收与D4收口

Owner明确接受分层验收，并要求记录UI按钮未实测。AC-004据实际Native分页、正常store分页组合回归及真实App正常重开的证据记PASS；加载更多按钮仍NOT RUN。所有10项Must在本需求已说明范围通过，implementation complete、feature usable，本地D4完成。最终严格/claim/D4门禁结果见机器账本；不继承其它Feature批准，不把分层接受转换成未执行的UI事实。

保留限制：完整safe生成和跨其它族breaking历史引用未解决；D4不是生产资格。没有日常迁移/外部MCP或生成供应商/新Git提交推送。真实任务累计7/20，剩余13次不自动使用。


## 12. 最终逐项审计与本地提交（2026-10-29）

最新核对见[04最终审计](04-final-audit-and-local-delivery.md)。新增修复：Esc后Enter重开、键盘进入图片重试浮层的焦点保留、11格式族实际图标区分，以及旧规划状态与当前执行授权的文档矛盾。21项UI/绑定、1项分页重开、9项Native正常样本/真实回放、Host race/vet、8项Contracts及来源check、lint/fmt/clippy、文档构建通过。最新canonical App十附件、路径/图片Esc→Enter、历史及1180×760亮暗复验通过，原浅色/窗口已恢复。累计仍7/20真实任务。用户已授权本地提交，不推送；最终SHA见04及机器账本。历史分页按钮仍NOT RUN，Owner分层接受不变；全量其它族契约阻塞和禁止测试未执行记录保持。
