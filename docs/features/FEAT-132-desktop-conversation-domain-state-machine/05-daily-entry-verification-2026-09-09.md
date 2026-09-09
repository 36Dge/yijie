# FEAT-132 交付收尾与日常入口验证

日期：2026-09-09，**日常入口验证PASS**。原生机制实现和原D4结论见 [02-verification.md](02-verification.md)。本轮沿用用户明确授权，完成文档同步、当前普通应用的正常验证、发现问题的定向修复与必要本地提交。`contract-impact=none`：本轮未改变协议、执行语义、权限或持久化格式。

## 来源与工作区

- Contracts：`6f632f155eacdaf93df0e0b00b5dab9e369c5442`。
- Host：`9e9d317f7e4ecff5f8aeec94fa467f9bede32139`。
- Desktop最终日常构建：`c0dd70c240d48c2c16d046aa27c9b32ec4d32c5b`。依次包含原D4实现、既有UI提交`a46cd0e5106684faa6ba944a798997f39bff5f0e`、接入说明修正`98bccad38676ffb38fb00302c1cfa2327d2a13a0`及本轮历史读取修复。
- Codex源码仍为`6c1ad767f0997845b8258a1c452fd4eb7577579f`；保留FEAT-136 Runtime及manifest的SHA-256与原D4一致。
- 开始时五个相关仓库均干净。前轮的3处并发修改已由既有UI提交保存：权限设计说明、ChatPermissionControl.vue和variables.css。本轮不修改这3个文件，记录内容摘要；其差异涉及图标、布局、颜色和尺寸token，权限选择与确认脚本未变。
- 两端native来源锁以及FEAT-152的Contracts/Host锁，共42个来源条目，与固定Git对象和当前文件逐字节摘要一致。canonical来源及FEAT-137永久退役门禁通过，未更新或放宽pin。

## 文档收尾

修正元仓需求简述、原生实施说明及Desktop接入说明中的“D4待执行/预算为0”等过期文字。明确此前D4使用固定提交隔离构建、既有app-data和隔离Host Home；不将旧档案可读表述为原Host全部映射已接管。保留phase缺失、冷历史不完整、Command完成后才提供最终输出等限制。

## 日常入口与数据范围

- 命令：在原`yijie-desktop`工作区运行`pnpm tauri:demo-fast:app`，未设置验收代理或隔离路径覆盖。
- 普通应用身份：`com.yijie.ai`；app-data：`~/Library/Application Support/com.yijie.ai`，对话库为`demo-fast-v1/chat/conversations.db`。
- Host Home：原工作区`yijie-desktop/.local/demo-fast/host-home`；Codex Home：同级`codex-home`；Host端口18081。
- 启动前没有易界Desktop/Host/Runtime进程；原Host索引通过只读方式核对，共8条会话映射，均idle，无active_turn_id。未复制数据库或凭据。

## 发现与修复

CrossBSD下的旧附件任务选择后跳回新建页。通过正常Web Inspector，只观察无正文的状态及既有授权只读IPC结果：`chat_load_history_v2/v3`均成功返回1轮历史，`chat_resync_session_v2`也成功，且包含未完成的清理记录；`chat_list_draft_attachments_v2`返回`chat_resource_not_found`。Native的`validate_draft_target`按既有规则禁止为已有清理记录的会话开放草稿，保护本身正确。问题在于界面将草稿失败作为读取历史的前置失败，尚未展示清理状态就跳转。

修复只修改Desktop选择流程：仅遇到草稿NotFound时，继续由既有授权resync确认是否存在清理记录；没有清理证据仍保留拒绝。有清理记录则清除草稿展示状态，正常加载历史，再复用`revokeSelectedRealtimeAuthorityForCleanup`撤销实时订阅和输入能力。没有改变Native校验、清理状态、权限、数据库、Runtime或对话执行事实，也不重试删除。

新增普通内存回归先复现`chat_resource_not_found`，修复后保留历史及Artifact元数据、禁用输入、不调用删除；另验证没有清理证据时仍拒绝，以及切换到正常会话可重新建立草稿。完整定向前端集合760/760 PASS，ESLint/TypeScript与完整generate:check PASS。不是重新运行含故障/攻击fixture的广泛Rust/Host测试。

真实复查确认原附件记录可读，显示`reference-portrait.jpg`的“已过期”状态和原回答，同时显示“任务删除尚未完成”，发送与附件入口禁用。切换到已有几何图片Artifact后，预览正常。该修复与此前权限弹窗样式提交无关。

## 检查结果

- Desktop文档构建PASS；权限组件现有定向回归8/8 PASS（两个Vitest项目）。
- 元仓lint、50/50测试、Shell语法与D4需求包门禁PASS。
- 普通canonical入口的标准构建、readiness及首次正常退出重启PASS；包含原日常Host映射的旧任务可读，权限入口保持请求批准。
- 新权限入口的青柠图标和布局已实际观察；三种菜单项及当前选择通过可访问树核对，组件确认/取消/键盘/禁用回归8/8 PASS。本轮未扩大权限模式，也未声称重新验证所有主题下的完整弹层视觉。
- 此前隔离D4的图片任务在当前app-data中可读、可预览，但原日常Host没有它的映射，权限同步仍提示不可用；没有导入或猜测绑定。
- 原FEAT-131等待记录仍显示等待处理/旧版记录，没有补发或伪造终态。
- 修复后最终正常退出重启PASS：旧附件历史、清理保护、切换到正常会话后的输入入口、已有Artifact预览均再次确认；readiness=200/ready。原Host的8条映射及最后Turn身份/状态前后一致，仍无活跃Turn。3处既有UI文件摘要完全一致。
- 最终应用、Host和Runtime均正常退出，18081/18083/18085端口无监听。没有为凑额度增加请求，累计仍为19/25次文本、1/3次图片。

## 操作与数据边界

权限菜单的部分AX取消/焦点操作没有产生预期结果，后用正常键盘选中当前请求批准项返回；未更改权限。首次正常退出后，工具继续读取界面意外拉起一个未带canonical环境的裸应用实例，已通过⌘Q正常关闭，再从标准入口启动。后续退出均以进程/端口检查确认，不在退出后继续调用会自动拉起应用的界面读取。

诊断快捷键曾被现有Tauri权限拒绝，未放宽该门禁；随后使用WebKit已有的原生Inspect Element入口。诊断仅观察状态与调用既有授权只读IPC，不输出凭据或历史正文。诊断窗口和临时观察器随正常应用退出结束。

本地日志及不含正文/凭据的元数据记录于工作区`.local/feat132-daily-entry-20260909`。调用预算累计上限25次文本、3次图片；本轮没有发送任务或调用图片生成，累计仍为19次文本、1次图片。

历史清理未完成、附件自然过期、隔离Host缺少映射均保留实际状态。本轮不修复历史删除操作、不恢复过期附件、不接管无可信绑定任务。原D4十项AC结果保留其固定提交与证据范围，本报告补充当前日常构建的真实结果；未推送、打tag或部署。

完整来源、检查结果、调用累计及18份本地证据摘要见 [机器可读记录](evidence/daily-entry-2026-09-09.json)。
