# FEAT-136 原生 Command 调整验收

日期：2026-09-09。**本次八项 Must 满足，local D4 PASS。验收发生于当时的工作区候选；其后 Desktop 已提交为 8bfa5ca284fddb86d7cdd2a406c5041c49367688。** 原 2026-08-30 五项 Command D4 四文件完整归档于 history/2026-08-30；prior FAIL、原日期、源提交、调用数均不覆盖或继承。

## 当前来源与真实入口

Desktop 验收基线为 `6e5047d1c23041c46dd495ddb89e24c7e4db5d47`，交付提交为 `8bfa5ca284fddb86d7cdd2a406c5041c49367688`。原 [机器证据](evidence/native-command-d4-2026-09-09.json) 是验收时点快照，其 candidate_committed=false、工作区状态及逐文件 SHA-256 保留历史含义；当前 Git 状态见 [交付证据](evidence/delivery-status-2026-09-09.json)。提交对象中的 10 个源码/测试文件逐项匹配原 D4 哈希，仅 Desktop 文档追加验收与交付状态区分，其前后哈希另见提交前证据；没有在新提交上重跑 D4。Contracts `db7a607c1c091fc4f4243829d68d5b673eb7e2c3`、Host `f4cf01bd6f7e9f37792ef743d44f0ce10527c10b`、Codex `6c1ad767f0997845b8258a1c452fd4eb7577579f` 未改。native Contracts pin 仍为 `6f632f155eacdaf93df0e0b00b5dab9e369c5442`，权限 Host pin 不变。

日常标准入口为 `pnpm tauri:demo-fast:app`。所有构建保持原来源/权限检查；普通身份 `com.yijie.ai`，现有 app-data、原 `.local/demo-fast/host-home` 与 `codex-home`。没有隔离或复制用户数据库/凭据。真实请求阶段仅使用既有 `permission-smoke-meter.py` 固定路由计量器，转发原 MiniMax endpoint，关闭自动重试，不改正文或审批策略，不借此模拟服务。

本轮共五次标准构建启动及正常退出，前三次用于已有数据及布局定位；最终代码的一次真实 Command run 与一次正常重启构成当前验收。最终 App/Host/Runtime 全部退出，18081/18083 无监听，计量器在全部请求完成后通过自身 KeyboardInterrupt/server_close 路径正常结束。

## 八项结果

| AC | 证据与结果 | 状态 |
|---|---|---|
| AC-001 | 原生 Command 展示链路测试；真实 completed 1 / failed 1，exit 0 / 128、duration 均 0ms，“当前项目”保留；command_failed 为显式 status 的产品映射，不冒称原生 error | PASS |
| AC-002 | 更短、不同、合法空输出和直接 completed 的联合测试；真实仅两条 Command，重开后仍两条，无前缀对账/第二累计 | PASS |
| AC-003 | Turn completed/interrupted/failed、历史及 stream gap 下 UI 无错误 busy/正在执行播报，Item 最后观察事实不变；真实终态后无忙碌误报 | PASS |
| AC-004 | null/空/partial/零值与安全目录回归；partial 不再伪称上游截断，失败空输出不说成成功；真实目录/exit/duration/输出可读 | PASS |
| AC-005 | 保留 native final-only 安全输出；真实指针与 Tab→Return 复制均成功；合成精确复制/纯文本检查通过；会话诊断不猜 Item 归属 | PASS |
| AC-006 | SQLCipher 原生 Command 正常 reopen/cold conflict 通过；实际同一任务退出重开后仍各一条且字段/输出/失败码一致；旧 Command IPC/卡片兼容定向检查通过 | PASS |
| AC-007 | 最终 canonical 正常启动/切换/退出重启、light、键盘/aria-live、200%与恢复100%；旧历史、过期附件、Artifact预览、权限入口和 Composer 定向回归通过 | PASS |
| AC-008 | 与实现阶段分离的源码自审完成；删除与保留理由见交付记录；无新 reducer/状态推演/历史重建器/累积器，无 Runtime/Host/schema/权限改动 | PASS |

## 实际数据和调用

只在新建普通 `command-project` 中发送一次合成用户请求，请求执行两个独立只读命令：`git status --short` 成功，`git rev-parse --verify refs/heads/feat136-absent-ref` 正常缺失引用失败。实际仅观察到两条 Command Item，没有额外 Command Item 或重试观察；不从脱敏输出反推完整 shell 正文。验证任务为 `01a085a9-b561-7331-be8d-4aabf9c47757`，正常重启后读取同一任务。

用户授权本次独立上限 10 次 MiniMax-M3 文本 API 请求、0 次图片，包含标题/审批审查/自动请求与重试；实际 **3/10 文本、0/0 图片**，均 HTTP 200 并正常完成。台账没有转用历史额度；重开读取没有新增请求。详见 [调用台账](evidence/text-request-ledger-2026-09-09.json) 与 [授权记录](evidence/request-authorization-2026-09-09.json)。

原 8 条 Host 映射及原生终态逐项不变；本次只新增 1 条验证映射，总数 9、全部 idle。最后退出后的 Host 索引与 Command 完成后索引完全相等。权限始终“请求批准”，没有临时换模式。

## 检查、自审和过程失败

- 前端 11 份定向测试 251/251；App/zoom 另 10/10。新增 native Command 18 项，既有 Command/FEAT-134/store/Composer/Artifact/权限覆盖保留。
- 正常 SQLCipher reopen/cold conflict 扩展 Command 后 1/1；旧 Command IPC 原终态字段检查 1/1。
- make lint 包含生成来源、ESLint/TypeScript、fmt、clippy all-targets，全部通过；canonical 标准构建与 Desktop 文档构建通过。保留 Vite 既有大 chunk 与未签名开发构建提示。
- 初轮 4 项新测试失败源于错误的测试观察时机/未挂载 DOM；修正 harness 后通过，不修改产品迎合测试。
- 200% 曾暴露既有外壳宽度未消费缩放视口、长标题撑开默认 Grid 列的问题。先补宽度后仍需约束 Grid；最终两处最小 CSS 修复后，标题正常省略、右侧输入与发送控件在视口内，Command 失败说明及字段可滚动读取。原失败截图不改写为 PASS。
- 独立阶段自审检查 native/legacy 分支、零值/空内容、状态/诊断、复制、来源/权限、兼容与布局；无阻断问题。Reviewer 为 Codex 自审，不冒称独立人工批准。

## 保留限制

- Command 输出继续等原生最终对象，不声明独立 live started/output-delta 顺序已实测；Runtime cold history、phase/plan 仍可能缺失，不补造。
- 日常数据未提供真实旧 v5 Command 样本；旧兼容由定向测试验证，实际 canonical 的旧数据回归覆盖旧文本、附件与原生 Artifact。没有把 synthetic 写成真实旧 Command 验收。
- 旧清理未完成、附件自然过期、隔离任务缺少普通 Host 映射仍保留；不自动续跑、补发、修复删除或猜接管。
- Tool 仍为 FEAT-144 blocked / NOT RUN；dark、精确1180×760及原 FEAT-142/143 后移项不写 PASS。
- 不运行含强杀、攻击、权限破坏、故障注入等禁止场景的广泛 Host/Rust/Contracts 套件；没有关闭检查或批量跳过测试来制造绿色。
- 本次 FEAT-136 的本地验收、已提交和已推送状态分别见 [交付收尾记录](04-delivery-closure-2026-09-09.md)；FEAT-134 四个原提交不能代替本次新实现交付。

最终元仓 pnpm lint、pnpm test（50/50）、Shell 语法、feature:audit（19个包）、FEAT-136 D4 门禁及 diff/digest/原四文件归档完整性检查均 PASS；机器门禁不替代以上真实验收事实。
