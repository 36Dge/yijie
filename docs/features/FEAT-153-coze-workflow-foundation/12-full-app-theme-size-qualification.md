# 完整 App 与主题、窗口尺寸验收

2026-09-13。用户明确“真实 App、亮暗主题及两种窗口尺寸验收（已解锁）”。本轮packaged验收完成；当前dev完整UI受工具限制，整体D4保持NOT RUN。

源码与11末尾基线一致后，通过原厂 Docker 及 canonical up 恢复六服务和认证 ready，epoch `94935fff-6e10-44a4-855b-0f259e97b596`。本轮所有 UI 操作仅使用 CUA；没有 Swift/AX 辅助脚本、故障注入、强杀、API业务补写或对外发布操作。

## 首轮真实 packaged 事实

标准 `pnpm tauri:demo-fast:app`，实际 App PID10814。真实创建 `7684681543721156608`（FEAT-153 完整App验收 20260913-A），双节点首次自动完整入画。不完整草稿正常试运行明确提示检查节点连线；经真实文本输入、端口拖线和节点拖动修正，保存并试运行成功。

R1 `7684682576279109632`、前缀“版本一：”，debug run `7684682601549791232` 成功后内部发布 v0.0.1。修改为“版本二：”并保存 R2 `7684682741815705600` 后旧发布证明失效；重新 debug run `7684682769036738560` 成功，再发布 v0.0.2。

编辑会话自然到期后，父运行面板仍可执行明确选择的 v0.0.1，release run `7684682943674974208` 返回“版本一：固定版本验证”；三节点状态3及原生输出、历史均对应。返回重开三节点两条线、位置与R2保持，首次自动适应有效。

真实系统浅色→深色切换保留未保存“主题切换草稿：”，后经App保存为 R3 `7684683724541132800`；两次返回取得 native remote_close_confirmed。App随后 Cmd+Q 正常退出，launcher exit0。首轮API只读对应见[a-api-before-theme-fix.json](evidence/step5-full-app-20260913/a-api-before-theme-fix.json)；本次中途曾保存单边不完整图，保留原始快照，不冒充可运行版本。

## 实测发现与修复范围

暗色实测发现：外围与节点已同步暗色，真实 Coze 画布背景仍消费上游固定浅色 `--g-editor-background`。在本地 editor stylesheet 中限定覆盖为现有 `--yj-color-bg-page`，网格点使用现有边框/次文字 token；不改上游文件、主题桥、图数据或持久位置。子项 contract-impact=none，仅本地视觉修正。

CUA App 截图为缩放后的1196×768，不能据此猜实际逻辑窗口大小。沿用现有exact-local私有native诊断，新增 window_geometry，仅从Tauri读取实际inner/outer逻辑宽高和scale_factor及App PID；初始化/真实Resized事件输出，不改变窗口、不增加command/capability/CSP/URL/身份/秘密或IPC字段。此观测子项 contract-impact=additive，权威为Desktop私有window.rs，公共wire生成N/A。用户本次实际窗口验收范围已授权，标准构建后与CUA实际拖动互相对应，未伪装二进制或造验收值。

以上修复先正常退出App、canonical stop栈，再标准构建、登记、恢复并重新验收。新候选与主题/尺寸结果待追加；首轮暗色画布问题保持FAIL历史，不回填为成功。

dev标识排查依据本机锁定 `tauri-codegen 2.6.3/src/context.rs:301`：canonical dev从项目 `src-tauri/Info.plist`读取并嵌入标准元数据；缺文件时只加入名称和版本，没有CFBundleIdentifier。新增该标准源文件，仅填与原 `tauri.conf.json`、packaged一致的 `com.yijie.ai`，由Tauri正常构建生成开发产物。此dev平台身份子项为semantic，整体仍semantic；不新增身份值、权限、capability或存储schema，packaged标识保持。是否改善CUA识别以实际dev启动为准，不复制/伪装包、不替换已有或已发布binary，不改固定Codex Runtime。

该标准元数据尝试未解决CUA控制限制：新dev PID18299正常启动，原生报告1180×780、scale2；可执行路径返回Invalid app，bundle ID因多个历史包被判歧义，精确包路径仍timeout。没有第二个App进程；用户已用Cmd+Q正常退出dev，launcher exit0、App/Host/Codex PID均消失，不发送强杀或其它UI技术。未证明改善的Info.plist已从本轮源码移除，最终候选不包含该尝试；未在进程运行期间覆盖其binary。此项dev UI资格仍NOT RUN，保留真实编译/启动来源记录。


## 修复后 packaged 四组合实测

canonical 重建并恢复 epoch `b5a2c028-e3ac-41d2-9ce6-7edeb7441d2d`，editor manifest SHA-256 `4053ced07c85188dfa17ef9be905792446277a738095997879c5e7bafaa518b4`，实际 App PID19114。新资源 B `7684687185122951168` 全部通过 CUA 真实 UI 创建与操作，没有通过 API 补写。

| 真实逻辑窗口 | 浅色画布、结果/历史 | 暗色画布、结果/历史 |
| --- | --- | --- |
| 1180×760，scale2 | PASS | PASS，原背景缺陷已消除 |
| 1440×900，scale2 | PASS | PASS |

尺寸来源为 native `window_geometry`，不使用缩放截图反推。原默认显示缩放1512×982时窗口受桌面可用高度约束；通过系统设置临时选1800×1169，再正常拖边达到精确1440×900。完成后已恢复默认缩放和浅色，Dock快捷切换共两次，设置确认自动隐藏off。CUA截图仅保留在本次会话工具输出，[b-ui-matrix.json](evidence/step5-full-app-20260913/b-ui-matrix.json)记录观察；没有虚构本地图片文件。

B初始双节点首次自动入画；正常不完整试运行提示invalid_draft，真实拖线/拖动后保存R1 `7684687450811138048`。debug `7684687473561042944`成功，内部发布v0.0.1；release `7684687586501066752`返回“尺寸验收一：暗色最小窗口”。

大窗口修改前缀并保存R2 `7684690083189882880`，旧试运行证明失效、内部发布禁用；debug `7684690100101316608`成功后发布v0.0.2。显式执行仍选定的v0.0.1，release `7684690435574333440`返回“尺寸验收一：大窗口固定版本”，没有被新草稿覆盖。查询终态与历史为两个显式快照，点击“刷新历史”后记录一致，不能描述为自动实时同步。

暗色大窗口返回重开，三节点/两线/R2正确，首次自动适应完整入画。缩小窗口保留当前视口，可能暂时裁切远端节点；手动“适应画布”恢复完整且不保存、不修改持久位置。主题切换保留未保存前缀。浅色大窗口确认框Tab/Tab/Shift+Tab/Return能选中继续编辑，暗色Chat离开确认也能取消并保留同一画布。

## 导航标题缺陷与限定修复

真实暗色Chat切换后取消，URL和画布留在workflows，文档标题误写成“新建任务 · 易界 AI”。定位为现有router.afterEach未判断navigation failure，同时可能错误触发页面标题焦点。新增一个正常导航取消/随后成功导航的回归测试，旧实现确实FAIL；仅在成功导航后同步标题与heading focus。子项contract-impact=none：只修正同一renderer本地展示和焦点，不改变导航授权、HTTP/native/消息、持久状态或Chat协议。整体FEAT-153仍semantic。

`pnpm lint`及指定router、workflow目录和workspace测试149/149 PASS；测试先红后绿。未运行历史危险fixture或全仓测试。新构建的真实App复验结果与最终数据/清理待追加；本次dev界面资格仍受CUA无法识别裸进程限制，整体D4仍NOT RUN。


## 最终重建复验、数据和清理

未保存“保留草稿验收：”自然到期，页面明确禁写并保留同一图；显式重连后保存R3 `7684692064230965248`。API、MySQL与PostgreSQL只读核对三节点两线和位置/UTF-8摘要一致，B两版内部版本、四次成功运行、十份共同completed回执一致；另有一份正常不完整试运行的API rejected回执，没有把拒绝改写成成功。见[b-cross-database-and-session.json](evidence/step5-full-app-20260913/b-cross-database-and-session.json)。

正常退出PID19114（exit0）、canonical stop/up后epoch变为 `c8287004-65b9-4f00-b522-5ea87eea7b3d`，再标准构建并启动最终PID24567。1180×760原生读数确认；零登录打开B，首次入画、R3和前缀保留。临时编辑后取消Chat离开，文档标题仍为“工作流 · 易界 AI”，URL和画布未变；正常导航到Chat后标题为“新建任务 · 易界 AI”。临时草稿没有保存，随后重开并选择原历史run `7684690435574333440`，旧版输出和三节点原生状态3全部读回。期间CUA报告外部窗口变化的一次后续放弃/导航动作实际落在Store，不计为Chat放弃测试；另一次明确的正常Chat导航才计入PASS。见[final-app-retest.json](evidence/step5-full-app-20260913/final-app-retest.json)。

正常重启前后完整Workflow、历史、四run及其receipt逐字段相同，见[normal-reopen-readback.json](evidence/step5-full-app-20260913/normal-reopen-readback.json)。最终91个公开产物/实际包文件中K_NA/K_AC匹配均0；未做heap或MessagePort dump，隔离结论同时依靠既有源契约/native边界，不能升级为全量渗透认证。12仓身份、原设计文件及Codex Runtime保持，失败的dev Info.plist尝试没有留在源码。

最终App两次编辑会话均取得API typed closed=true对应的native确认；Cmd+Q后launcher exit0，自有App/Host/Codex/Vite及credential helper无残留。canonical stop后八容器均exit0，宿主18888/1420/1421无监听；确认没有其它运行容器后，原厂Docker Desktop正常stop exit0。四卷保留，系统外观/缩放/Dock恢复，见[normal-cleanup.json](evidence/step5-full-app-20260913/normal-cleanup.json)。无强杀、攻击fixture、权限破坏、外部provider、模型、商家、付费、commit/push/tag或对外发布。

本轮结论：packaged完整产品链路和四种主题/尺寸组合通过，两个实际缺陷已修复。当前dev完整产品UI仍NOT RUN（CUA不识别裸开发进程），首次open进行中取消和完整新增可访问性审计未全覆盖，原白底青柠contrast限制保留；不得把这些分项结果写成整体fresh D4或全页axe PASS。


最终治理检查：元仓lint/50 tests/Shell语法/11 sibling contract-governance PASS；feature strict、D0与audit-claims PASS。Coze接入检查实际结果为15,297份未改源文件、2个已登记overlay、6份保留缺失，仅证明来源保持，不等于全Coze测试。三仓diff空白检查通过；源锁与三consumer锁摘要不变，详见[qualification-checks.json](evidence/step5-full-app-20260913/qualification-checks.json)。
