# FEAT-164 S4 同源构建与 App/UI 验收

本轮已完成记录范围内的macOS本机合成App验收及三项必要修复；完整FEAT-164仍未完成。最终产品来源Desktop `a0a474333ba03186b36f30fa3ab86287abfc5c15`，本轮新增真实模型HTTP **0**。

2026-10-25，Owner明确授权本轮先正常退出活动S1 App并核验清理，再推进固定来源canonical构建及App/UI验收。新增真实模型HTTP为0，仅本地提交、不推送；原工作区、两份真实账本与旧预占均保留。总需求contract-impact=breaking保持；单纯构建/验收无新公共wire或权限设计，发现接线缺陷按所属源和最高影响处理。

## 当前审计与执行顺序

前轮Host cac2d4d、Desktop56f5284、Connectors1f15726、Skills595c927、Contractseddc64f、Runtime074417e5已完成专家pin与安全离线扩展。完整App/WebView、当前源旧隔离历史、暂停Kimi/MiniMax回退及正常重开仍未验收。旧30元额度2/2 HTTP已耗尽，14.188544元未知预占与0.139590元保守费用保留；预算余额不授权新HTTP。

本轮先记录7仓既有改动与资源/账本基线，正常⌘Q退出S1；确认App/Host/Runtime结束后，通过独立fixture自身/shutdown接口停止它。正常退出后留存S1开发构建与隔离数据的本地审计副本，只通过canonical工具更新本项目候选输出。既有真实账本逐字不动；旧合成fixture仅由其正常退出流程更新state，原请求条目保留并另存退出前快照。

同源构建拟使用media组合覆盖普通/市场/专家/媒体入口，仍沿原权限/安装/审批链；所有模型provider通过受限18083本机fixture，注入明确合成凭据，fixture没有外部转发能力。UI依次核验旧隔离历史、普通Kimi/MiniMax、专家资源/媒体、暂停Kimi后的MiniMax与历史、同构建正常重开；补亮暗/最小窗口和正常退出。仅操作隔离候选数据，不迁移日常库，不安装外部市场服务或读取其凭据。合成模型内容不证明真实供应商能力。

## 构建前发现

只读检查确认canonical Worker构建将manifest中的binary写为物理connectors-s4-source路径，FEAT-164 receipt则用yijie-connectors链接路径做字符串等值比较。两者对应同一固定仓库和同一内容寻址文件；此路径表达差异会阻断同源构建回执。拟将receipt的期望目录正规化为realpath，再保留文件名、SHA、大小及完整源码/环境校验。该修复contract-impact=semantic（私有部署来源兼容），不扩大制品或程序来源集合，不改Worker/Runtime制品。

构建前路径修复已仅本地提交Desktop `f4db8eacea44508dda6b602764e7624bf8d1fedd`，ESLint和源差异检查通过。第一次canonical预检在普通Skills固定commit10c45be检出缺失处正常拒绝；随后在默认`.local/skills-pinned-10c45be`位置创建对应detached检出，与专家595c927分开。未改两套pin，也未改原dirty Skills。普通资源仍按38项原权威确定性打包，专家仍按75项新不可变来源同步。

S1正常退出和旧fixture自身shutdown均exit0，18083/18086释放，无所属App/Host/Runtime残留。旧S1开发bundle、Host及隔离App数据已保存到资格树`s4c-before-build-20261025`审计副本（不用于降库或回退启动），摘要见[s4c-s1-normal-cleanup.json](evidence/s4c-s1-normal-cleanup.json)。仅此次正常关闭改变旧合成fixture的state，原1请求不变，退出前快照保留；两份真实预算账本不变。

## 首次 App 观察与修复

新候选正常启动后，旧S1合成历史和既有真实答复42均可只读恢复，fixture请求保持0。随后Kimi/max正控、同聊天切换MiniMax/high继续、专家JD0.1.3+HTML/SVG三请求组合完成；预览与正常导出通过，导出与普通源文件逐字一致，共5次loopback，无真实请求。

Owner另明确批准暂时切换系统外观并恢复原设置；原设置为浅色。深色1180×760实际窗口发现聊天输入区底部裁切：App shell已为32px标题栏预留空间，ChatPage又把整窗760px下限作用于剩余内容区，造成额外竖向溢出。该问题在原候选样式已有，不涉及模型wire或权限。修复contract-impact=none，仅进程内布局：聊天grid保持height100%并将min-height设为0，整窗下限仍由shell/native维护。需正常退出后canonical重建，复验亮暗最小窗口、原5请求历史和媒体恢复；不会通过改截图或隐藏控件取得PASS。


## 暂停配置的实际启动缺陷

Desktop554d0e2正常重开后，旧媒体ready与三轮普通聊天恢复，Kimi/max继续对话成功，fixture累计6请求。随后正常退出0、所属子进程清理、18086释放后，以同一回执和`YIJIE_KIMI_K31_EXECUTION_PAUSED=true`启动。Host ready，但App持续显示“本地服务尚未就绪”，一次正常“重试启动”仍未恢复；不把这个禁用态写成暂停保护通过。

源码定位：Native `feat137_resume_bound_sessions_with_host`在启动时遍历已绑定会话。现有只读保留条件仅接受catalog的`not_configured`，未包含v2既有`activation_required`。终态Kimi历史因暂停无法达到`model_ready`，使全局恢复失败，连MiniMax和本地历史入口一起受阻。该因果先用普通结构化catalog/terminal测试复现，再以真实App复验确认；不强行改数据库、Host返回或权限。

拟修复contract-impact=semantic（既有v2暂停语义的Native恢复实现）：仅对已确认无active local/runtime/operation身份、且权威catalog中该Kimi不可用且reason=activation_required的历史沿既有只读保留分支跳过模型resume。active/unknown、缺catalog、其它reason/模型继续保持原恢复要求；不授执行、切换或新outbox许可，不改公共wire与存储。已有v2契约来源f2819c66/S4eddc64f与Owner批准的暂停读历史/MiniMax回退设计不变，不新增ADR或能力。回退仍保留SQL41 reader，不降库。


最小布局修复已仅本地提交`554d0e2a1d73dc52f09ac282f8c94f35bcb2dc71`；该构建亮/暗1180×760实际截图通过，输入区和操作按钮均在窗口内，系统外观已恢复浅色。42项相关前端测试PASS；首次遗漏candidate环境的40PASS/2FAIL原日志保留，补正确运行配置后通过，未改测试断言。

暂停历史回归在修复前精确命中1项并失败（exit101），修复后同项1PASS/0ignored，Rust fmt与candidate product Clippy PASS。该修复已仅本地提交`a0a474333ba03186b36f30fa3ab86287abfc5c15`；只修改`src-tauri/src/chat/mod.rs`，原工作区其它差异经逆向补丁逐字核对保留。失败App已正常退出0、18086释放，fixture保持6请求。a0a4743的第四次canonical构建已通过（回执SHA e3695d260de3814125d4cfb5fa5c43e481be5fdc3ff92c4b4782176627f56047，119 bundle文件）；随后复验，不继承554的App成功作为新逻辑的通过。


## 修复后的暂停验收

a0a4743同一canonical回执以paused=true正常启动，App现在展示旧历史及媒体ready。旧Kimi会话有非空输入时显示“模型暂未启用”、发送禁用；模型菜单Kimi不可选、MiniMax可选。启动/历史/填写期间fixture保持6请求、增量0。明确切到MiniMax后沿原模型选择/权限链发送，显示第4轮已完成，唯一新增请求为MiniMax-M3/high，累计7次；没有暂停Kimi出站。App正常⌘Q退出0，Host/Runtime/Worker/adapter无残留、18086释放。[暂停零请求](evidence/s4c-paused-zero-http.json)、[禁用状态](evidence/s4c-paused-kimi-disabled.ax.txt)、[回退成功](evidence/s4c-paused-minimax-positive.ax.txt)、[清理](evidence/s4c-paused-fixed-cleanup.json)。这组事实确认上述启动缺陷已修复，不是只通过单元断言。


## 最终结果与来源

最终源a0a4743的同一构建先paused=true完成历史/禁发/MiniMax，再正常退出并以paused=false重开；保存的第4轮与MiniMax选择保持，读取阶段请求仍7。新建专家任务`01a172c4-2ef0-7ce0-aa3e-f194fc0b32a9`沿正常工作空间、已准备专家、原权限链执行，3次实际Kimi/max loopback分别为HTML发布、SVG发布与合成正文。两产物ready，HTML受管窗口与SVG弹窗预览通过，累计10次。旧f4db8ea阶段的两文件导出字节一致性保留其原来源，不冒充a0a4743重新导出。

| 本轮项目 | 判定与证据 |
|---|---|
| 来源与canonical构建 | [当前来源/构建](evidence/s4c-current-build-provenance.json)、[完整回执](evidence/s4c-current-packaged-receipt.json)，119 bundle文件；无签名/发布 |
| 普通模型与旧历史 | 首次候选Kimi/max、MiniMax/high成功；旧S1与42可读；a0a4743正常重开[零补发](evidence/s4c-current-reopen-zero-http.json) |
| 暂停与回退 | [RCA及回归](evidence/s4c-paused-startup-audit.json)；非空Kimi输入禁发，MiniMax显式切换完成；不是全局禁用的假PASS |
| 专家与媒体 | a0a4743[实际ready记录](evidence/s4c-current-media-ready.ax.txt)、[HTML预览](evidence/s4c-current-html-preview.jpg)、[SVG预览](evidence/s4c-current-svg-preview.jpg)；原阶段[导出字节核对](evidence/s4c-media-export-check.json) |
| 最小窗口与外观 | a0a4743[亮色](evidence/s4c-current-min-light.jpg)/[深色](evidence/s4c-current-min-dark.jpg)均1180×760，输入与按钮无裁切；[浅色已恢复](evidence/s4c-current-theme-state.json)，窗口回1268×780 |
| 工程检查 | 42项前端子集、暂停历史1项回归、fmt/Clippy、canonical Vue/TS/Rust构建通过；[Native检查](evidence/s4c-paused-native-checks.json)、[前端结果](evidence/s4c-focused-ui-tests-candidate.log) |
| 正常清理 | [最终App清理](evidence/s4c-final-app-cleanup.json)，App及fixture正常exit0、所属子进程为空、18083/18086释放；fixture使用自身/shutdown |
| 总判定 | [记录范围的本机子集PASS](evidence/s4c-app-verdict.json)；10合成HTTP、0拒绝、0外部模型HTTP；不等于供应商质量或完整Gate PASS |

本轮Desktop仅本地提交：`f4db8eacea44508dda6b602764e7624bf8d1fedd`、`554d0e2a1d73dc52f09ac282f8c94f35bcb2dc71`、`a0a474333ba03186b36f30fa3ab86287abfc5c15`；三次均逐文件/逆向补丁核对，没有混入原工作区差异。Host、Contracts、Runtime、Connectors、Skills无新源码提交。元仓本轮提交由Git记录定位，不填写自引用SHA。

## 审计边界与剩余执行顺序

- 真实预算两份文件逐字保留：累计30元、2/2 HTTP已经使用；14.188544元unknown预占及14.328134元保守累计上界不变。新模型HTTP许可仍0，不能以预算余量重试。
- 原7仓496个既有改动文件、154个原ignored资源、7个日常数据库文件保持；原S1 bundle/Host/隔离数据5593项归档保留。允许的变化只有本轮专属补丁、canonical产物及隔离App正常持久化。旧合成S1账本只由自身正常shutdown更新state，1条原请求不改；这不是清空真实账本。
- 旧历史读取覆盖原隔离候选已有K3.1记录，**不证明旧K3已加载线程/子代理cutover**。下一步先补旧K3与自动大上下文压缩的非破坏性离线验证设计/执行，再逐项补计划及显式恢复/取消的完整App流程；保留原请求身份和授权，不为制造unknown改库、断进程或注入故障。
- 其它支持平台、完整freshness、当前来源G2V、S1—S4完整G3和三项final仍缺；本轮不把macOS子集、合成服务或旧来源结果提升为完整PASS。需要真实供应商能力时，必须另有明确HTTP次数授权；当前不执行。
- 模型显式切换时观察到已有`conversation_warning`通用提示，未隐藏；源码与Runtime模型变化warning一致，但未留存原始warning，唯一原因只能列为推断，见[审计](evidence/s4c-runtime-warning-audit.json)。App本轮未观察到自动标题HTTP，原S4b的辅助调用检查只按其原来源适用。
- 禁止项均未执行；全仓危险fixture/强杀/权限破坏/攻击注入覆盖继续NOT RUN。此前宽范围基线失败也不因本轮focused PASS关闭。

后续从本报告、feature.yaml与08锚点续办。当前没有需用户代退的App或活动fixture；仅本地提交，不推送、改远端、建分支、tag或发布，不启动归档旧reader写入新库。

最终治理审计：claims/strict、元仓lint、53项治理测试及7个shell文件语法检查通过；G3/S4实际门禁仍拒绝放行，保持前置G2V、slice资格、完整TCONF和freshness缺口。保留审计已实测核对496原改动、154原资源、5593归档项、7日常DB、两真实账本及当前119 bundle文件，均符合本轮保留要求。
