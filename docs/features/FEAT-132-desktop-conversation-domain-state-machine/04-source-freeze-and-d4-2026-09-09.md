# FEAT-132 来源固定与真实验收推进（2026-09-09）

用户已授权本次 Contracts → Host → Desktop → 元仓的本地提交、必要修复提交和真实 pin 更新；不推送、不打 tag、不部署。真实模型预算仍待单独批准。

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

## 待批准的模型预算与场景

建议一次性硬上限：MiniMax-M3 文本 API 请求 20 次（含标题、原生审批审查、自动请求或重试）；image-01 图片 API 请求 1 次。文字请求复用既有 FEAT-152 本地计量代理，整个验收共用一个不含正文/凭据的 ledger，到限即停，不自动追加。图片只在已保留的 canonical 图片入口中发起一个明确请求，复用既有 Host 每 Turn 一次的生成限制，无自动重试。

验证素材只使用本地新建验证目录中的普通合成文本/CSV/PNG，发送到现有 MiniMax 服务；不发送用户业务文件。Command/审批只针对该验证目录中的普通新文件，不使用攻击、权限破坏、二进制替换或强杀场景。

1. canonical stable 正常启动，核对固定 Runtime、原生接口、无登录阻塞、旧档案可读和新建任务 readiness。
2. 短文本对话：观察原生 ID/phase/final/status，重开保持结果。
3. 普通合成附件读取与 Composer，两个任务间切换，观察内容不串写。
4. 正常命令及现有原生审批回调，检查审批/执行/显示状态分开；不扩大永久权限。
5. 用应用的停止按钮正常中断一个验证 Turn；随后正常退出/重启，核对已观察终态和内容。
6. 预算允许时经现有 canonical 图片路径生成一个简单无人物图案，检查 Artifact 交付、存储和重开。该既有能力不新增实验 API 或 Runtime patch。
7. 亮/暗主题及 1180×760 最小窗口检查；更新十项 AC，以真实证据决定 D4。

原应用仍有一条旧 FEAT-131 等待记录；不删除、不补发、不伪造原生终态。隔离验证不抢占该应用端口/运行目录，不把隔离新 Run 描述为原数据库已完成切换。
