# FEAT-132 来源固定与真实验收推进（2026-09-09）

用户已授权本次 Contracts → Host → Desktop → 元仓的本地提交、必要修复提交和真实 pin 更新；不推送、不打 tag、不部署。2026-09-09 又单独批准真实调用预算，随后将总上限增加至 25 次 MiniMax-M3 文本请求和 3 次 image-01 图片请求；包含标题、审批审查及自动请求/重试，共用台账，到限停止。

## 已固定来源

- Contracts：6f632f155eacdaf93df0e0b00b5dab9e369c5442。
- Host：9e9d317f7e4ecff5f8aeec94fa467f9bede32139。
- Desktop：fe66786e3eed00a42821c4509b940ba889b89bf8；canonical 隔离验证补充提交 2da23988028fec5e2d037e4aa81b448376beab65。
- 两端 native-conversation.lock.json 均从实际 Contracts Git 对象生成；FEAT-152 既有完整 Host SHA/digest 校验已更新并通过，权限语义不变。
- FEAT-137 历史 SDK 漂移经标准 generate:safe 对齐既有 source，完整 check-generated:safe 通过；retirement authority、Runtime 和激活开关未改变。

原工作区出现 3 处其他任务修改（09-settings-permissions.md、ChatPermissionControl.vue、variables.css），没有纳入本次提交或修改。后续真实验证使用 `.local/feat132-validation-20260909` 下三个精确提交的 detached worktree，使用原有 canonical stable 入口和独立端口/Host Home，不覆盖原工作区产物，不复制用户数据库。

canonical runner 允许以绝对路径重用同一份已有 Runtime 目录和 key 文件；仍强制原来的 Runtime binary/manifest SHA、非符号链接文件和 Native owner-only 检查。没有拷贝密钥，也没有改动已有 Runtime。

## 真实验证前已执行

- Host 实际输出 7 个 NativeEvent → Native SSE decoder（分块传输）→ 单一 buffer → SQLCipher → 正常 close/reopen，PASS；无 ID 改写，无冷热集合合并，failed 不被冷 completed 覆盖。
- 原生 API producer conformance、12 项 Host 原生测试及权限定向回归通过。
- schema 13 的有效加密数据库，保留旧 completed/failed/queued 记录，前向迁移到 14、重复启动和正常 reopen 通过；没有 backfill 原生来源，没有更改旧正文与权限模式。
- Contracts lint、安全全量生成、两个固定 baseline breaking check、Desktop 完整 generate:check（使用现有固定 Skills worktree）、clippy 和前端 build 通过。

## 已批准的模型预算与场景

用户批准的当前硬上限：MiniMax-M3 文本 API 请求 25 次（含标题、原生审批审查、自动请求或重试）；image-01 图片 API 请求 3 次。文字请求复用既有 FEAT-152 本地计量代理，整个验收共用一个不含正文/凭据的 ledger，到限即停，不自动追加。图片只在已保留的 canonical 图片入口中发起一个明确请求，复用既有 Host 每 Turn 一次的生成限制，无自动重试。

验证素材只使用本地新建验证目录中的普通合成文本/CSV/PNG，发送到现有 MiniMax 服务；不发送用户业务文件。Command/审批只针对该验证目录中的普通新文件，不使用攻击、权限破坏、二进制替换或强杀场景。

1. canonical stable 正常启动，核对固定 Runtime、原生接口、无登录阻塞、旧档案可读和新建任务 readiness。
2. 短文本对话：观察原生 ID/phase/final/status，重开保持结果。
3. 普通合成附件读取与 Composer，两个任务间切换，观察内容不串写。
4. 正常命令及现有原生审批回调，检查审批/执行/显示状态分开；不扩大永久权限。
5. 用应用的停止按钮正常中断一个验证 Turn；随后正常退出/重启，核对已观察终态和内容。
6. 预算允许时经现有 canonical 图片路径生成一个简单无人物图案，检查 Artifact 交付、存储和重开。该既有能力不新增实验 API 或 Runtime patch。
7. 亮/暗主题及 1180×760 最小窗口检查；更新十项 AC，以真实证据决定 D4。

原应用的一条旧 FEAT-131 等待记录保留；没有删除、补发或伪造原生终态。旧应用经 ⌘Q 正常退出，原 Desktop/Host/Runtime 三个进程全部退出后启动验证构建。canonical 全局单实例检查仍有效；没有删除锁或绕过检查。稳定和普通图片入口均读取各自现有 app-data，未复制数据库；旧历史仍按“旧版记录”显示。

## D4 发现并修复的问题

1. `17a680f783a9ab2b06e47109247d6e920368ef87`：AJV CommonJS helper 在浏览器打包后变成 exports 对象，真实 Item 引发 TypeError。修正生成脚本并重新生成；新增真正打包后调用校验器的回归，修复前失败、修复后通过，保留 Unicode 长度边界。
2. `9c5eafd2c31ba65f2a4132a77c6f5aa668c7575f`：旧历史 DTO 给空助手 outbox 占位补空格，与空正文不一致，阻断原生视图读取。只读投影略去没有正文或内容块的 pending 助手占位，保留数据库和所有实际内容；历史回归和 Clippy 通过。
3. `5e6ada73ed8b9d49dde51e4b6659ce5337304a6e`：SSE 接收占住后台循环，中断 outbox 等到 Turn 结束才分发。流保持打开时复用既有 outbox dispatcher；中断提交不再改写已绑定原生 Turn 的执行状态。持有正常 SSE 的回归确认终态前收到 interrupt，原生最终值/旧 Host 恢复回归及 Clippy 通过。

## 当前真实结果

- canonical stable 与 canonical 普通图片入口均通过来源门禁、标准构建和 readiness；前者 experimental_api=false，后者仅沿用 FEAT-128 已有 generate_image 例外。没有新增 Runtime patch 或实验能力。
- 首条请求因上述显示错误未展示，但真实 completed 已保存；修复后正常重启，无新模型调用即可恢复原文。
- 合成 CSV/PNG 已由真实模型读取：total=100、左红右蓝。后台命令期间切换会话没有串写；命令输出及验证文件内容正确。
- 第一次长文本自然完成，不计中断通过。修复后第二次通过停止按钮键盘触发，UI 已中断、Host idle、原生 thread/read=interrupted；后续新 Turn 不覆盖该中断记录，reasoning Item 仍保留原生未完成状态。
- 请求批准的 approve-once 与拒绝均通过；拒绝后文件不存在且未重试。用户另行明确授权本次临时切换三种权限模式；帮我批准完成普通文件写入并实际消耗两次原生审批审查请求；完全访问完成指定文件写入，随后已切回请求批准。
- 最小窗口 1180×760 的完整亮/暗布局已通过 CUA 实际检查，WebView 客户区实测 1180×728、DPR=2；暗色通过 WebKit 原生偏好模拟触发完整应用主题，诊断面板分离后观察主窗口，之后恢复 System (Light) 并关闭诊断窗口。
- 图片通过既有 canonical 入口生成、预览并正常保存为 JPEG（76380 bytes），SHA-256 `25319bafd736019f370cffef28fa01e0542dbcece2be415c7d08a383048e9005`。正常重启后的 Artifact 与中断历史复核均通过，D4 已关闭为 PASS。
- 最终累计文本19次、图片1次，未超25/3总上限；文本代理保留所有既有记录，增加额度时在无活跃请求下正常退出并重启。

实际 Host 原生 SSE 元数据、只读 thread/read、来源索引与不含正文/凭据的台账保留于工作区 `.local/feat132-validation-20260909/evidence`。无强杀、故障注入、权限破坏、危险 fixture、原数据库复制或 Runtime 二进制替换。

最终结论与十项 AC 见 [02-verification.md](02-verification.md)；原先“未执行”的9月8日快照已归档。最后一轮稳定入口正常重启后继续原生会话返回 FEAT132_RESTART_OK，所有验证进程正常退出。
