# FEAT-160 实施记录

2026-10-18：只读审计确认Host旧active与同一Codex turn interrupted不一致，以及Native对busy的unknown处理。提出复用现有恢复/状态写入路径的最小修复。无模型调用，额度问题待答复。

## 实现与本地检查

- Contracts transport semantic 说明先行，使用既有 generate-experts/sync-experts 更新 Host、Desktop、Skills 精确摘要；DTO、wire 形状和数据库 schema 均未改。
- Host 增加只读原生终态核对，复用 Store.Resume、NativeRevision 及既有两把锁；所有原 admission 检查保留。expert_submission_read 在相同提交锁下分别确认 market/turn 两本原账本真实缺失，保持 task/session/scope 映射；存储错误不再冒充 not_found。
- Native 唯一 Coordinator 先读原回执；accepted 沿原 expert_accept，只有持久化可信 busy 与 Host 确认缺失同时满足才沿原 market_mark(blocked)。不自动重发，不增加恢复队列。
- `go test -race ./internal/session -run '^TestFEAT160' -count=1` PASS；正常专家提交/重开/模型切换/移除/既有普通线程绑定以及 pending apply/cleanup 保护定向回归 PASS；`go vet ./internal/session` PASS。
- Rust FEAT160 两项正常样本 PASS（确认拒绝正常重开保留、无 busy 的 unknown 保留）；既有 unknown 两项和 accepted receipt 绑定一项 PASS。clippy 首次发现 enum 大小警告，改为 Box 后 `-D warnings` PASS，未抑制检查。
- Contracts 生成与三个 consumer check PASS；normal source/digest/同源/既有恢复契约 5 项 PASS。
- 原 App 正常 Cmd+Q：原 session 53707 exit 0，原 App/Host 进程和 18081 监听均退出；未强杀。
- canonical freeze 首次发现专家资源 provenance 仍引用旧 Contracts lock。沿原 Skills package、Desktop sync 流程刷新来源证据与审核摘要；逐项确认全部 75 条资源 metadata 和 75 个 archive SHA 不变。仅 bundle 顶层 source/provenance 摘要变化；无 prompt/资源/安装历史改动。然后 freeze PASS。
- `pnpm tauri:demo-fast:app` 构建进行中，日志 `.local/feat160-canonical-build.log`。继续沿 FEAT159 日常 profile 现有 candidate 入口，不新增开关。
- D0 门禁 PASS。Codex 工作树干净，binary/manifest 摘要与 FEAT159 完全相同。

本任务模型请求仍 0 次，单独额度问题尚待答复，不转用前次余额。未运行攻击/强杀/权限破坏/存储损坏等故障注入测试；这些覆盖不能宣称通过。

## 首次真实 App 观察

canonical 构建成功并正常启动。进入原 UI 设计师聊天，旧 attempt 通过原 Coordinator 查询收敛为“提交失败”，输入区不再因 unknown 锁定，专家仍为 UI设计师 0.1.1；旧原生轮次仍 interrupted。Host 只读 API 确认仍恰好一条原生旧轮次，未自动补发。

实际页面发现 failed 标题下仍显示“本轮正在等待处理”。修复既有 ChatTurnGroup 的 local submission 显示分支：failed/cancelled 保留原消息与终态说明、不显示等待进度，不改变原生执行状态。FEAT158 uncertain/FEAT160 terminal 两项 UI 测试 PASS，vue-tsc/改动文件 ESLint PASS。

再次通过正常 Cmd+Q 退出，session23491 exit0，App/Host/adapter 和18081均清理。最终canonical构建日志 `.local/feat160-final-build.log`，未进行新的模型请求。

最终canonical构建及启动完成，读取API确认无新turn；CUA报告Mac锁定，已请手动解锁。未绕过锁屏；当前等待解锁和本任务额度，模型0次。D4保持NOT RUN，不将已解除本地unknown等同于Host真实续聊已验收。

用户明确批准本任务最多3次短文本请求（2次正常验证、最多1次修复复验），并确认已解锁Mac。开始最终真实收发/正常重启验收；当前计数0/3。不调用图片、视频或商家工具。

2026-10-18T08:52:59.942183+00:00：通过最终构建的原UI设计师聊天发送第1次短文本恢复验收，计数1/3。可见新轮次开始生成；旧failed说明正确且不再显示queued。

第1次真实验收PASS：原UI聊天收到“UI设计师恢复验收完成”，新增turn `01a14e36-a7cc-7fd2-ad94-27d856cd5dca` completed；原thread、session、task不变，UI设计师0.1.1保留。原生恰好从1轮增至2轮，旧轮仍interrupted；新轮item仅userMessage/reasoning/agentMessage，无工具。Host state=idle、active_turn_id为空。通过Cmd+Q正常退出（session44499 exit0），App/Host/adapter与18081已清理；启动同一canonical构建的`--reopen`进行第2次验证。

2026-10-18T08:54:53.250472+00:00：同构建reopen成功，原聊天旧interrupted、旧本地failed、第一条新回复及UI设计师0.1.1全部恢复；Host idle，原生轮次仍2条。已发送第2次短文本，计数2/3。

## 最终真实验收完成

第2次真实验收PASS：正常reopen后的原聊天收到“UI设计师重启恢复验收完成”，新增turn `01a14e38-6541-7b30-9ea7-214a48dfb1cb` completed。原生轮次计数1→2→重启仍2→3，每次恰好新增1轮，旧未接收消息没有自动补发；两次新轮均只有userMessage/reasoning/agentMessage，无工具调用。Host和native status均idle，active_turn_id为空。原专家UI设计师0.1.1、原聊天/session/task/thread均保留；失败提示修复在最终构建和重启后确认。

最终模型额度2/3，第三次未用，无图片/视频/商家工具调用；不继续消费额度。应用保持在原聊天的完成页面供用户查看。最终工程检查沿已通过的相同源码结果，不无因重复全套测试；继续执行D4文档门禁。

最终D4门禁PASS：`./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D4 docs/features/FEAT-160-expert-history-recovery`，exit0。全部Must AC已有当前最终构建的真实依据；仅声明local/demo_fast通过，不等同production_hardened。

2026-10-18 后续：用户明确授权连同FEAT159复审后提交推送。恢复核心实现复审无新增变更，定向race/Native/UI回归通过；完整跨仓来源与推送记录见../FEAT-159-native-artifact-media/03-final-review-and-push.md。此后提交授权取代此前“本轮不提交/推送”的阶段限制。

四个代码仓库已普通push并逐一核对远端HEAD；已提交源码canonical构建和现有内容观察通过。元仓将记录本次审核、完整commit及来源顺序；未发布安装包或部署。
