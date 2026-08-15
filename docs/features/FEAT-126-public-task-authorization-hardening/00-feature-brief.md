# FEAT-126 — 安全的新建任务对话、任务记录与 Public Tasks 授权加固

## 1. 文档信息

| 字段 | 内容 |
|---|---|
| 状态 | G1/G2/G2A Passed / R8 Convergence Corrective Campaign Held / DESIGN-126-028 Accepted / LIA-126-050 Governance-only Authority Consumed / DEC-126-088 Accepted / G3 Partial / G4/G6 Pending |
| 需求负责人 | 段成威 |
| Product/Design 决策人 | 段成威 |
| 技术负责人 | 段成威 |
| Reviewer | 段成威 |
| 发布负责人 | 段成威 |
| 创建日期 | 2026-08-01 |
| 最后更新 | 2026-08-15 |
| 原始需求来源 | 段成威 2026-08-01 对话需求及 4 张 Codex 局部交互截图 |

## 2. 一句话目标

让已授权用户从 `/chat` 以纯文本和明确的本地项目/权限上下文安全创建任务，进入可恢复的极简流式对话，管理本地 session 与聊天项目；同时完成 ADR-0012 已预留给 FEAT-126 的 Public Tasks 服务端身份、租户和资源级授权加固。

本需求采用DEC-126-022的`Local-only Delivery Strategy`：最终可观察交付是在Owner本机启动API、Agent Host、Desktop和固定Runtime并完成全链路E2E。它不包含线上部署、Production Ready、tag、package publish、registry、云数据库或真实用户数据；未来若产生上线意图必须重开生产轨。

## 3. 问题与用户价值

- 目标用户：已登录且在当前租户拥有 `task.create`/`task.read` 及适用项目权限的易界 Desktop 用户。
- 当前问题：FEAT-124 的 `/chat` 只有页面内 textarea，不能发送、持久化或进入真实会话；`/tasks` 仍是静态样例；Desktop 尚未接入 Agent Host sidecar。
- 安全问题：现有 Public `/v1/tasks*` 没有 bearer 认证，创建请求信任客户端 `tenant_id`，按 ID 读取不做 tenant/resource check；FEAT-125 因而只允许双重隔离，不能开放这些路由。
- 用户可观察结果：一次提交只创建一个本地 session；流式结果、标注为“模型推理记录”的 raw reasoning、历史和标题可恢复；列表与项目菜单严格裁剪；无权限、失败、断线与物理删除都有明确结果。
- 为什么现在做：入口 UI、MiniMax text turn 基线和本地身份/权限工程基线已经存在，但真实对话与任务安全边界尚未闭环。

## 4. 编号与范围治理

Accepted ADR-0012 与 FEAT-125 已把 `FEAT-126-public-task-authorization-hardening` 预留给 legacy Public Tasks 的 breaking auth/tenant/resource hardening，并把临时隔离例外绑定到“FEAT-126 生产启用或 2026-09-30，取较早者”。段成威于 2026-08-01 在 G1 明确接受以下合并方案：

1. 保留既有 slug 与安全责任；
2. 把本次“新建任务对话”作为同一安全纵向需求的 Desktop/Agent Host 产品轨；
3. Public Tasks hardening仍是未来任何线上启用的release-blocking轨；Local-only G6要求本地安全实现/E2E，但不退出FEAT-125生产隔离例外；
4. 该合并只确认产品范围与编号治理；DEC-126-022把当前交付限定为本机运行，未来生产启用必须重开生产G5及相关安全证据。

## 5. 范围

### In Scope

- 新建任务入口：纯文本 composer、发送按钮、本地项目/工作区入口、权限审批策略入口。
- 从 durable local create 进入稳定 session 路由，接入 Agent Host/Runtime 的 text turn 与 SSE 流。
- 活跃对话：用户/模型消息、处理中/完成/失败/中断、标注为“模型推理记录”的 raw reasoning 纯文本展开/折叠、回到底部。
- 极简动作集：用户消息无复制/二次编辑；模型消息无复制/like/dislike/分叉；会话页无页级置顶和二级侧栏显隐。
- 任务记录：元数据倒序、置顶分组、按 session 点击懒加载消息、模型自动标题、人工重命名、置顶/取消置顶、永久删除。
- 聊天项目：选择本地目录上下文；项目菜单仅置顶/取消置顶与移除；移除不删除磁盘文件。
- Desktop-owned local conversation repository、schema version、事务、迁移、删除、租户/OS 用户隔离与未来 storage port。
- Agent Host Desktop sidecar 接入、stream cursor 恢复、allowlisted raw-reasoning 投影及 Runtime 残留清理能力调查。
- Public `/v1/tasks*` 的 bearer、权威 tenant、resource/action authorization、IDOR 防护、审计、consumer migration 与 FEAT-125 临时隔离退出。
- FEAT-126 Chat/App Shell Pattern已于2026-08-02 Accepted；只取代当前Pattern中的FEAT-126冲突段落。

### Out of Scope

- 文件、图片、音频、语音、链接附件或拖拽上传；文本粘贴除外。
- 模型选择、推理强度选择、provider 切换或用户可见 token/cost 调节。
- 工具/MCP/Skills/Plugins、写文件、shell、平台写操作或真实审批执行；当前 Runtime 继续 fail closed。
- 回答的复制按钮、评价、分叉、重新生成、用户消息二次编辑。
- 云端会话同步、多设备合并、共享协作、导入导出、归档与回收站。
- 项目编辑、Finder 展示、归档或删除本地目录/仓库文件。
- Admin Web、Connectors、Knowledge、Skills 或商业平台能力接入。
- LIA-126-001/002与DEC-126-026已完成S4–S6；DEC-126-027/028/030/031/033/034已接受S7A–S8B Closure。Owner随后明确授权将已接受的yijie/API/Host/Desktop checkpoints推送到各自专用候选分支，远端SHA已复验并由DEC-126-035接受；这只改变可达性，不改变G3/G4/G6、flag、merge或发布状态。LIA-126-007的test-only S9已由DEC-126-036接受。Owner于2026-08-06接受DEC-126-059 Option A与S10BRP1 Closure，API/Infra形成clean local checkpoints并关闭`S10B-BLK-006`；随后正式消费LIA-126-022执行一次S10B-R6。R6在S10B-001 image resolver阶段以`preflight_image_resolver_failed` fail closed，S10B-002–012未运行。Owner批准DEC-126-060 Option A后又单独授权BLK-007设计评审；2026-08-08继续执行指令接受DEC-126-061 Option A并单独授权/消费LIA-126-023。closed child result、parent leaf映射、0600 evidence与自动化已实现。2026-08-09 canonical run `624bd64c-b378-4d53-97c0-05790e7e4657`完成S10BEP1-014：3个immutable identity、3个no-start probe、closed parent、no-log与资源归零均PASS，且`s10b_r7_executed=false`。Owner随后通过DEC-126-062明确接受LIA-126-023/S10BEP1 Corrective Closure并关闭`S10B-BLK-007`，再通过DEC-126-063仅授权形成Infra/Governance本地clean checkpoints。G3保持Partial，fresh R7仍未授权；S11、MiniMax、feature activation及一切新增远端动作仍不在授权范围。
- 后续Owner已单独授权并消费LIA-126-024/S10B-R7；当前事实由§11/§12最新记录覆盖：S10B-001 PASS，002因完整四组件orchestrator缺失fail closed，003–011 NOT RUN，012仅abort cleanup subset。Owner已接受DEC-126-064/065 Option A并授权LIA-126-025/S10BO1 repository corrective。四仓实现、S10BO1-001–014、API/Host/Desktop/Infra全量门禁、Governance门禁与七仓diff检查全部PASS；Owner现通过DEC-126-066接受Corrective Closure并关闭`S10B-BLK-008`。该接受不等于fresh S10B/G4/G6 PASS。
- FEAT-126本期不创建`contracts-v0.3.0` tag、不发布SDK/package、不配置registry，不进行线上部署、生产灰度/启用、云数据库接入或真实用户数据处理。

## 6. 候选成功指标

以下是设计评审候选阈值，不是已测基线或已批准 SLO。

| 指标 | 当前基线 | 候选目标 | 测量窗口 | 数据来源 |
|---|---:|---:|---|---|
| 首次提交去重 | 无真实提交 | 10,000 次双击/重试测试中重复 session/turn 为 0 | G4 测试 | Desktop repository + Host conformance |
| 列表按需读取 | 静态样例 | 首屏只查元数据，0 条消息正文被加载 | 每次列表加载 | DB query/contract test |
| 本地列表响应 | 无基线 | 1,000 sessions 冷启动 P95 ≤ 200ms | 性能测试 30 次 | Desktop integration benchmark |
| 会话打开 | 无基线 | 已缓存元数据后首批历史 P95 ≤ 300ms，不含 Runtime resume | 性能测试 30 次 | Desktop integration benchmark |
| 授权隔离 | legacy route 未授权 | 未认证、无权限、跨租户/IDOR 测试 0 次越权 | 每次 CI + 类生产 | API security suite |
| 流式恢复 | Desktop 未接入 | 支持窗口内无重复渲染；游标失效有确定恢复态 | 故障矩阵 | Host/Desktop E2E |
| 可访问性 | 活跃对话未实现 | 键盘主流程全可达，axe 阻断级问题为 0 | 每次候选构建 | 自动化 + VoiceOver 人工检查 |

## 7. 约束

- 成本：不增加用户模型选择；标题生成必须有调用次数上限、超时和确定性 fallback，不得阻塞首轮回答。
- 兼容：最高 contract impact 为 `breaking`；旧 Public Tasks consumer 未迁移前保持路由隔离，不能多仓硬切。
- 数据：prompt、message、raw reasoning、项目路径均按 `confidential/restricted`；不进入 URL、普通日志、遥测、审计正文或错误上报。
- 安全：前端 capability 只改善 UX；API 与本地 sidecar 分别执行自己的认证、tenant/resource/action check。
- IPC：ConversationApplication继续只在Rust内持有权威状态；S8A已实现DESIGN-126-005定义的versioned、closed、capacity-bounded私有投影。WebView不能接触Host bearer、数据库key、canonical path或Host原始wire；S8B0发现的readiness/storage投影缺口必须先走DEC-126-032，不得由Vue猜测或调用旧裸command。
- 可用性：1180×760 最小窗口、亮/暗/跟随系统、键盘与 VoiceOver、reduced motion 均须覆盖。
- Runtime：当前固定 read-only、`approvalPolicy=never`；权限入口不得伪装成可提升权限的控制。
- 删除：用户要求数据库物理删除；DB 外 Runtime rollout 与最小审计残留边界必须在 G2 前明确。

## 8. 已确认事实、假设、未知项与冲突

| 类型 | 内容 | 证据/来源 | Owner | 处理状态 |
|---|---|---|---|---|
| Fact | 用户要求纯文本发送、极简对话、任务记录、模型标题、本地 DB、session 永久删除及项目置顶/移除 | 2026-08-01 原始需求 | 段成威 | Confirmed source |
| Fact | FEAT-126 已被 Accepted ADR-0012 预留给 Public Tasks hardening | `docs/adr/ADR-0012-*.md` §上下文/后续行动 | 段成威 | Confirmed |
| Fact | FEAT-124 `/chat` 当前只有本地 textarea，无发送/网络/持久化 | `yijie-desktop/src/pages/chat/ChatPage.vue` | client-team | Confirmed |
| Fact | DESIGN-126-005形成时`ConversationApplication`仍是Rust内部对象；随后S8A已实现20个private commands、单一listen-only event、strict TS client与authoritative Pinia reducer | `yijie-desktop/src-tauri/src/chat/ipc.rs`、`src/domain/chat-ipc.ts`、`src/api/chat-client.ts`、`src/stores/chat.store.ts` | client-team | DEC-126-031 Accepted；S8A Closure Passed |
| Fact | S8B0只读盘点发现的UI gate、session路由guard、permission↔chat生命周期、store project/paging/cleanup、closed readiness/storage projection与`sampleTasks`生产路径缺口，已在LIA-126-005本地checkpoint`5dab02a1ad5f03fead236aa7060fa6a75a234d85`关闭 | Desktop schema/Rust/TS/router/store/Tasks实现与全量门禁 | client-team | DEC-126-033 Accepted / S8B0 Closure Passed；不授权S8B |
| Fact | Agent Host 已支持 text turn、interrupt、resume 和 8 类 SSE 投影，但不保存正文 | `yijie-agent-host/README.md`、`docs/runtime-baseline-2.md` | agent-runtime-team | Confirmed |
| Fact | 当前 Host 固定 read-only、`approvalPolicy=never`，reasoning summary 默认 `none` | `internal/codex/provider.go`、compatibility manifest | agent-runtime-team | Confirmed |
| Fact | MiniMax 配置使用中国站 `/v1` + `wire_api="responses"`；既有真实 turn 测试曾通过 | Host provider code + 2026-08-01 本地 `make runtime-turn-test` 结果 | agent-runtime-team | Confirmed for baseline only |
| Fact | pinned Runtime canonical schema/source 已有 `thread/delete`、`thread/name/set`、public-summary与raw-reasoning notifications、turn `outputSchema`；当前 Host 尚未暴露 delete/name/reasoning variants | Runtime app-server README/schema/source/tests + Host manifest/provider | agent-runtime-team | Confirmed schema/source; integration pending |
| Fact | 固定 Runtime 既有 fake-provider fixtures 已验证 pathless ephemeral thread、turn-scoped strict structured output、reasoning summary request 与 delta/item 关联；5 个窄测试最终 PASS，一次默认 worker stack overflow 以 32MiB stack 重跑同一断言后 PASS | 2026-08-02 / `08-verification-report.md` | agent-runtime-team | Confirmed for Runtime/fake only |
| Fact | Owner 批准的 MiniMax 合成验证已按 hard cap 执行2次且0 retry：`MM-126-001` strict title PASS；`MM-126-002` 无public-summary event并出现7 raw reasoning delta + 1 completed raw content part，按当时ADR-0015门槛FAIL | ADR-0015 §4.1 / `08-verification-report.md` | agent-runtime-team | Calls exhausted；历史结果不改写；raw事件成为ADR-0016能力输入 |
| Fact | fixed `codex-cli 0.144.6` 在临时 `CODEX_HOME` 的一次无模型删除验证通过 live-store/restart 不可恢复，但 canary/ID 仍可在 Runtime SQLite WAL/log 字节中检测到；临时目录已清理 | SPIKE-126-002 / `08-verification-report.md` | agent-runtime-team | Functional delete PASS；forensic erase not provided |
| Decision | Desktop 本地会话正文/状态由 Rust/Tauri-owned embedded SQLite 持有；API PostgreSQL、Redis、pgvector 与 Host bbolt 保持各自职责 | ADR-0013 | 段成威 | Accepted 2026-08-02 / narrow G2 data authority |
| Decision | “不提供复制”指不提供产品级按钮，仍允许系统原生文本选择和 `⌘C` | 可访问性与平台惯例 | 段成威 | Accepted 2026-08-01 / G1 |
| Decision | 项目“移除”只移除聊天项目引用，不删除目录或历史 session | 最小破坏原则 | 段成威 | Accepted 2026-08-01 / G1 |
| Decision | 项目在首次提交及后续 turn 前必选，避免隐式或不安全 cwd | Host `StartSessionRequest.cwd` 必填 | 段成威 | Accepted 2026-08-01 / G1 |
| Decision | 权限审批入口只读展示 fixed read-only/deny 策略，不提供权限提升 | 当前 Host `approvalPolicy=never` | 段成威 | Accepted 2026-08-01 / G1 |
| Decision | `rusqlite 0.40.1 + bundled-sqlcipher`、`rusqlite_migration 2.6.0`、Keychain key、0700/0600、WAL/FULL/secure_delete/checkpoint，以及 Desktop→Host→Runtime 删除、30 天 content-free receipt 和限定 backup/uninstall 文案 | ADR-0014 + isolated Rust build/Runtime residue evidence | 段成威 | Accepted 2026-08-02；不等于 G2/实现批准 |
| Decision | 标题继续使用pathless ephemeral Runtime operation；reasoning改为展示Runtime/model实际raw reasoning纯文本，标注“模型推理记录”，不进logs/telemetry/audit；缺raw阻断功能Gate，不静默时长-only | ADR-0015/0016、DEC-126-007/015、Q-008/Q-009 | 段成威 | Accepted 2026-08-02；Q-009 Resolved；G2 Passed，G2A current |
| Decision | raw reasoning流式阶段在内存展示，terminal/显式incomplete record写入Desktop SQLCipher，随历史session懒加载并随session物理删除；不写Host业务DB/云端、不依赖Runtime rollout | ADR-0016、DEC-126-016/Q-016 | 段成威 | Accepted 2026-08-02；细节由DESIGN-126-003/DEC-126-017候选承接 |
| Conflict | 当前 Accepted Chat Pattern 要求完整 active chat 的附件/右侧面板，与本需求的极简纯文本相反 | `02-chat-workspace.md` 1.1.0 | 段成威 | Pattern update required before code |
| Decision | 不新增 Chat 二级侧栏显隐，保留 FEAT-124 全局 240/72 收起；后续 Pattern 候选须固化该边界 | `01-app-shell-navigation.md` 2.0.0 + G1 批准 | 段成威 | Accepted 2026-08-01 / G1 |

## 9. 初始仓库基线

扫描时间：2026-08-01，Asia/Shanghai。仅记录事实；未切分支、未 fetch、未改 sibling 仓库。

| Repository | Remote | Branch | Full HEAD SHA | Worktree | Existing changes owner |
|---|---|---|---|---|---|
| yijie | `https://github.com/36Dge/yijie.git` | develop | `6c23dc3d9fa0d979948dbb10356fc5929ac2513b` | dirty before FEAT-126 | FEAT-123 整包删除属于用户/前序任务，保持不动 |
| yijie-desktop | `https://github.com/36Dge/yijie-desktop.git` | develop | `155854cf3662384caa2c8bffe0a47935ef4a70b5` | clean | N/A |
| yijie-api | `https://github.com/36Dge/yijie-api.git` | develop | `faeb78019d95aaf9dcfbd8493f8bc2ecf7e4bf34` | clean | N/A |
| yijie-agent-host | `https://github.com/36Dge/yijie-agent-host.git` | develop | `34e94acf293f6daad61c4d42fa47028a2d1318e4` | clean | N/A |
| yijie-contracts | `https://github.com/36Dge/yijie-contracts.git` | develop | `9ec34abd6e7dfb5a23b0154d467694167224ebbb` | clean | N/A |
| yijie-infra | `https://github.com/36Dge/yijie-infra.git` | develop | `f040492e7c4af4aa7cc94a343140c58befae3af2` | clean | N/A |
| yijie-codex | `https://github.com/36Dge/yijie-codex.git` | develop | `3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f` | clean | N/A |

## 10. 视觉参考登记

截图来自本轮聊天附件的临时 OS 路径，可能被系统清理；本包只保存内容摘要、尺寸和 SHA-256，不把临时路径写成可发布权威源。G1 批准的是产品语义，不是截图像素；规则已固化到Accepted FEAT-126 Pattern。

| ID | SHA-256 | 尺寸 | 仅作为交互事实 |
|---|---|---:|---|
| VIS-126-001 | `f56a1638f28efe2c4084e7418022d24595eee2d34c70aaa5fb0a9c4c468884f0` | 550×218 | composer 内的“选择项目”入口 |
| VIS-126-002 | `af71cce695d8e68bd7de2bbd71bd049743946a1320c0a9d0bfbd66a23fa9c700` | 1260×244 | 浮动回到底部按钮 |
| VIS-126-003 | `c158882cdfe69b0615fc80e3aa01bf13718093528309089e9966a7666ef534d1` | 668×186 | “已处理 6m 22s”折叠入口 |
| VIS-126-004 | `d266babd892f27e6df0becc20042244da37639a092f9e4e78f0bbb29fdae8085` | 750×402 | 项目及其 session 层级菜单 |

视觉候选遵循易界 token；参考 Codex 的信息层级，并借鉴 Apple macOS 的克制原生感与 Linear 的高密度 hairline/surface 体系：系统字体、单一品牌 accent、无渐变、少阴影、明确焦点、最小 32px 控件和不小于 44px 的触控/鼠标复合命中区。上述原则不替代 Desktop Accepted Design Pattern。

## 11. 里程碑与状态

| 里程碑 | 目标日期 | Owner | 状态 |
|---|---|---|---|
| G0 需求建档 | 2026-08-01 | 段成威 | Passed |
| G1 需求/范围/产品安全语义确认 | 2026-08-01 | 段成威 | Passed：推荐产品方案获明确批准 |
| G2 可开始契约候选 | 2026-08-02 | 段成威 | Passed：DEC-126-017、DEC-126-011/012与Chat/App Shell Pattern Accepted；允许进入G2A source-contract candidate评审，不授权业务编码 |
| G2A 契约就绪 | 2026-08-02 | 段成威 | Re-review Passed：DEC-126-024 Accepted，`29317b6426578749dc698fc2ad32b986ee5c8e9f`为唯一source-contract candidate；现已精确推送到`origin/feat/feat-126-content-free-candidate`，`origin/develop`、历史`c000a024`与Draft PR #1均不变；远端可达不等于merge/发布/实现完成 |
| Contract Draft PR / merge readiness | 2026-08-02 | 段成威 | DEC-126-021 Accepted/HOLD：Draft PR #1固定SHA且保持Draft；红色CI只阻断merge，不回退G2/G2A；未来需本地跨仓E2E、audit修复、远端CI全绿及单独merge批准 |
| Local-only Delivery Strategy | 2026-08-02 | 段成威 | DEC-126-022 Accepted；目标改为Local Runtime Ready；tag/publish/deploy/G5均N/A；LIA-126-001后续仅授权S4–S6 |
| G3 本地切片完成 | 未排期 | 段成威 | Partial：Owner已通过DEC-126-076接受DESIGN-126-019/LIA-126-033 repository Corrective Closure；Desktop/Infra checkpoints、targeted/full门禁、独立审查及Compose 5.3.0 semantic gate均PASS。真实Tauri `AppHandle/setup` direct fixture仍为P2/live；尚无新的isolated-live PASS或完整fresh S10B-001–012 PASS，G4/G6 Pending |
| S8B0 UI Integration Readiness Review | 2026-08-03 | 段成威 | DESIGN-126-006/DEC-126-032与DEC-126-033 Accepted；LIA-126-005 / S8B0 Closure Passed |
| S8B Vue UI Closure Review | 2026-08-03 | 段成威 | DEC-126-034 Accepted / S8B Closure Passed；不自动授权S9/S10/activation，VoiceOver人工项保留到S11/G6 |
| Remote State Reconciliation | 2026-08-04 | 段成威 | DEC-126-035 Accepted：五仓候选ref/clean clone精确PASS；四个S4–S8B checkpoints已按Owner明确授权远端可达；不改变G3/G4/G6或后续切片授权 |
| S9 fake-provider Eval Closure | 2026-08-04 | 段成威 | DEC-126-036 Accepted；Host/Desktop checkpoints继续仅本地；禁止MiniMax、真实数据、flag和S10 |
| G4 Local Code Complete | 未排期 | 段成威 | Pending：R7未形成S10B-001–012完整PASS；仍需API/Host/Desktop/Runtime同run权威编排与完整对话E2E |
| G5 Production Ready | N/A | 段成威 | Out of Scope；未来上线必须重开生产轨 |
| G6 Local-only Delivery Complete | 未排期 | 段成威 | Pending：Owner验收本地启动和功能链路；不代表Production Ready |

## 12. 变更日志

> 2026-08-11：单独config-only授权已补齐LIA-126-033唯一未通过的Infra Compose semantic环境门禁。Compose `5.3.0`、直接`config --no-interpolate --quiet`、Infra `make lint`与`make test` `192/192`均PASS；未执行任何lifecycle或live，`s10b_r8_executed=false`。Corrective Closure仍为Review Ready / Pending Owner Acceptance，本门禁不授权isolated-live。

> 2026-08-12：Owner通过DEC-126-076接受DESIGN-126-019/LIA-126-033 Corrective Closure并关闭environment-bound Compose gap。G3保持Partial，G4/G6 Pending；真实Tauri `AppHandle/setup` direct fixture保留为P2/live。后续isolated-live必须基于本次新Governance checkpoint和其余六仓精确SHA取得另一份一次性授权。

| 日期 | 修改人 | 变化 | 原因/批准 |
|---|---|---|---|
| 2026-08-01 | Codex | 创建 00–10 需求设计包；未改业务代码 | 段成威要求完善并创建需求，不做执行 |
| 2026-08-01 | Codex | 同步 ADR-0012 关联需求状态为“已创建、G1 待评审、尚未实施” | 修正需求创建后的事实，不改变 Accepted 安全决策 |
| 2026-08-01 | Codex | 记录 G1 Passed；关闭 Q-001–Q-005/Q-011–Q-014 并接受对应产品决策 | 段成威明确回复“同意按 FEAT-126 推荐方案关闭 G1 产品问题”；G2 技术问题和实现仍未批准 |
| 2026-08-02 | Codex | 启动 G2 设计评审；以 ADR-0013 冻结 Desktop SQLite 与 PostgreSQL/Redis/pgvector/bbolt 职责；补充删除、Runtime/MiniMax 与 Public Tasks 兼容证据 | 段成威同意推荐存储方案并要求进入 G2；G2 未通过，仍不授权编码 |
| 2026-08-02 | Codex | 形成 ADR-0014：冻结 SQLite driver/migration/保护参数、跨 Desktop/Host/Runtime 删除、receipt、备份/卸载限定语义；完成一次临时 `CODEX_HOME` 固定 Runtime 删除残留验证 | 用户要求提交 DEC-126-006 与 Q-006/Q-015 结论供批准；无 MiniMax、无真实数据、无业务编码 |
| 2026-08-02 | Codex | 将 ADR-0014 与 DEC-126-006 标为 Accepted，Q-006/Q-015 标为 Resolved；保持 G2 Review In Progress | 段成威明确批准并重申 G2 仍不通过、不开始编码 |
| 2026-08-02 | Codex | 以固定 Runtime 既有 fake-provider fixtures 冻结标题隔离、public-summary v2 Host事件与降级契约；新增 ADR-0015 Proposed，提交 DEC-126-007/Q-008 与最多两次 MiniMax 合成验证方案，Q-009保持待证据 | 用户要求 G2 能力评审；未修改业务代码、未调用 MiniMax、未触碰真实数据 |
| 2026-08-02 | Codex | 将 ADR-0015/DEC-126-007 标为 Accepted并关闭Q-008；按Owner批准各执行一次MM-126-001/002，title PASS、public-summary因raw reasoning暴露FAIL；summary flag关闭、时长-only，Q-009 Ready for Owner Closure | 两次provider预算已耗尽、0 retry；无业务代码、无真实数据，G2仍不通过 |
| 2026-08-02 | Codex | 新增ADR-0016/DEC-126-015，取代public-summary-only/raw-drop/时长降级语义：UI必须展示raw reasoning纯文本，缺raw阻断功能Gate；Q-009按负向事实关闭 | 段成威明确批准六点变更；保留MM-126-002旧FAIL，不追加调用、不编码 |
| 2026-08-02 | Codex | 提交DEC-126-016/Q-016推荐：raw reasoning写入Desktop SQLCipher、随历史加载并随session物理删除 | Codex明确推荐；等待段成威批准，G2继续不通过 |
| 2026-08-02 | Codex | 将DEC-126-016标为Accepted并关闭Q-016；冻结流式内存展示、terminal/显式incomplete落SQLCipher、历史懒加载和session级联物理删除边界 | 段成威明确批准；schema/caps/contract仍待G2，继续不编码 |
| 2026-08-02 | Codex | 完成DESIGN-126-003与4项fixed Runtime raw fixtures，提交DEC-126-017；完成Public Tasks consumer inventory，提交DEC-126-011/012并关闭Q-010；提交独立Proposed Chat/App Shell Pattern和G2总评审 | 按段成威G2 Closure指令执行；无MiniMax、无业务代码、无契约源变更；等待Owner决定 |
| 2026-08-02 | Codex | 将DEC-126-017、DEC-126-011/012与FEAT-126 Pattern标为Accepted，记录G2 Passed并进入G2A source-contract candidate评审 | 段成威明确批准；仍不开始业务编码 |
| 2026-08-02 | Codex | 建立FEAT-126 G2A本地source contract candidate：Public Tasks v2、Host v2 title/cleanup/events、AgentSessionEventV2及fixtures/generated SDK；全仓27/27、build/pack、支持基线breaking与v1 wire equality PASS，提交DEC-126-018 | 未调用MiniMax、未改业务仓代码、未创建tag/pin/commit；等待Owner批准source shape，G2A仍未通过 |
| 2026-08-02 | Codex | 按Owner批准接受DEC-126-018并形成`yijie-contracts@c000a0245acb5c3f7ead5d2a877fb60c281c588c`本地immutable candidate；提交后复跑generate/lint/test/build/pack、支持基线breaking与v1 wire equality并回填摘要，提交DEC-126-019最终G2A批准 | 仅本地commit；未push/tag/pin、未改业务代码、未调用MiniMax；G2A等待Owner批准 |
| 2026-08-02 | Codex | 将DEC-126-019标为Accepted并记录G2A Passed；固定`c000a0245acb5c3f7ead5d2a877fb60c281c588c`为唯一source-contract candidate | 段成威明确批准；批准仅代表契约就绪，不授权push/tag/merge、远端可用性、downstream pin、业务编码或生产启用 |
| 2026-08-02 | Codex | 按DEC-126-020仅创建远端`feat/feat-126-contract-candidate`并在临时clean clone完成SHA、generate、lint/test/build、breaking、v1 equality与九项摘要复验 | remote SHA=`c000a024…588c`；`origin/develop`保持`9ec34abd…ebbb`；未merge/tag/发布/pin/编码；临时目录已移入废纸篓 |
| 2026-08-02 | Codex | 按Owner授权创建[yijie-contracts Draft PR #1](https://github.com/36Dge/yijie-contracts/pull/1)，base=`develop`、head=`feat/feat-126-contract-candidate`、head SHA固定为`c000a024…588c`；登记9项摘要并观察CI到终态 | run 30741466028在传递依赖`brace-expansion 2.1.2` high audit失败；候选未改manifest/lockfile，source门禁先行PASS，但`govulncheck`/`origin/main` breaking skipped；未重跑/豁免/修复/push/merge，提交DEC-126-021 HOLD建议 |
| 2026-08-02 | Codex | 按Owner指令接受DEC-126-021 HOLD并新增/接受DEC-126-022，将FEAT-126调整为Local-only Delivery：本机四组件启动与完整E2E是目标；merge延后单审，tag/publish/deploy/G5 N/A | 仅更新需求包；红色CI只阻断merge；Local Implementation Authorization仍Pending；无业务代码、MiniMax、push、tag、publish或线上动作 |
| 2026-08-02 | Codex | 按LIA-126-001完成S4 API授权加固、S5 Host v2 raw/title/cleanup基础、S6 Desktop SQLCipher/project/sidecar基础；三仓契约生成、lint、race/unit、migration/integration与Desktop build通过并完成结构化安全审查 | 仅本地未提交draft，所有新能力默认关闭；无MiniMax、Runtime/Infra修改、远端写入、merge/tag/publish/deploy或S7–S11 |
| 2026-08-02 | Codex | 按LIA-126-002建立四仓仅本地closure分支/WIP checkpoint；独立复审把S4–S6降为Conditional，并发现Public Tasks任意`input`及`conversation input.text` fixture与content-free-only数据边界冲突；依预设停止条件暂停代码修复，提交DEC-126-023/G2A复审 | 未修改contracts/Runtime，未调用MiniMax，未push/merge/tag/publish/deploy；FEAT-123删除未进入checkpoint |
| 2026-08-02 | Codex | 按Owner批准接受DEC-126-023方案C并关闭Q-017；从未修改的`c000a024`形成本地replacement `yijie-contracts@29317b6426578749dc698fc2ad32b986ee5c8e9f`，将Public Tasks v2收窄为closed content-free request/success/error，更新fixtures/generated SDK与迁移说明并完成post-commit全门禁 | 旧candidate、Draft PR #1和远端不变；无业务源码、MiniMax、push/merge/tag/publish/deploy；提交DEC-126-024最终G2A审批，LIA-126-002继续暂停 |
| 2026-08-02 | Codex | 将DEC-126-024标为Accepted并记录FEAT-126 G2A Re-review Passed；确认`yijie-contracts@29317b6426578749dc698fc2ad32b986ee5c8e9f`为新的唯一source-contract candidate | Owner明确批准；`c000a024`仅保留历史远端身份，Draft PR #1不变；不授权恢复LIA-126-002、业务源码、远端动作、MiniMax或S7–S11 |
| 2026-08-02 | Codex | 完成Remote State Reconciliation：登记sole contract candidate与yijie/API/Host/Desktop checkpoint分支的精确远端SHA；记录Owner恢复LIA-126-002，仅继续S4–S6 Corrective Closure | 最新Owner明确指令；`origin/develop`、旧Draft PR #1、merge/tag/publish/deploy均不变；不追加push，不启用flag，不进入UI/S7–S11或MiniMax |
| 2026-08-02 | Codex | 完成LIA-126-002本地Corrective Closure候选：S4审计/幂等/contract drift，S5 cleanup/lease/title/receipt/no-log，S6 reasoning/migration/cascade/sidecar nonce列明P1全部具备本地证据；提交DEC-126-026 Closure Review | API隔离PostgreSQL与race测试、Host race/fixed Runtime、Desktop TS/Rust/lint/build及总文档门禁通过；diff未提交/未push，0 MiniMax，0 UI/S7–S11，所有flags保持关闭 |
| 2026-08-02 | Codex | 按Owner批准接受DEC-126-026并仅执行S7A Desktop Rust Host Bridge/Domain：实现exact loopback/no-proxy/no-redirect、spawn nonce preflight、owner-only bearer、严格HTTP/SSE v2 parser与typed session/turn/reasoning/cleanup domain；提交DEC-126-027 Closure Review | Desktop lint/test/build全绿；113 TS、66 Rust（65 pass/1既有ignored）；含聚合多frame chunk回归；未新增Tauri/Vue入口，0 MiniMax、0 flag activation、0远端动作；S8–S11继续禁止 |
| 2026-08-03 | Codex | 记录Owner接受DEC-126-027并按单独授权完成S7B Desktop Rust Application Orchestration/Domain：持久化outbox、严格/批量event reducer、历史加载编排与标题优先级；提交DEC-126-028 Closure Review | Desktop `make lint/test/build`全绿；113 TS、79 Rust（78 pass/1既有ignored）；fake TCP Host应用链与10,000 delta回归通过；无Tauri/Vue入口，0 MiniMax、0 flag activation、0远端动作；G3仍Partial，S8–S11继续禁止 |
| 2026-08-03 | Codex | 按Owner审批将DEC-126-028登记为Accepted，S7B Desktop Rust Application Orchestration/Domain Closure Passed | G3保持Partial；未授权S8–S11/UI、MiniMax、feature activation或任何远端/发布动作 |
| 2026-08-03 | Codex | 完成DESIGN-126-005 Desktop IPC/ViewModel Contract Review：盘点ConversationApplication/Tauri invoke差距，冻结Rust-bound context、closed commands/events/cursor/error、纯文本投影caps、sequence/backpressure/cancel/stale/reconnect，并重切S7C/S8A/S8B；提交DEC-126-029 | 仅需求、设计、契约和计划文档；未改业务代码或Vue，未运行实现测试、未启用flag、未调用MiniMax、未修改contracts/Runtime pin、未作远端写入 |
| 2026-08-03 | 段成威 | 批准DESIGN-126-005与DEC-126-029，并以LIA-126-003单独授权S7C Desktop Rust实现 | G3保持Partial；只允许authorization context、session/project actions、interrupt、持久化delete/cleanup、background coordinator和restart/resync source；S8A/S8B/Tauri conversation IPC/TS/Vue、MiniMax、flag与远端/发布动作继续禁止 |
| 2026-08-03 | Codex | 完成LIA-126-003 / S7C本地Rust切片并提交Closure Review | SQLCipher schema v4、300s opaque auth context/revision invalidation、授权facade、session/project actions、stable interrupt、持久化cleanup saga、独立receipt HMAC key、30天content-free receipt、coordinator/restart/resync/live raw source完成；Desktop `make lint/test/build` PASS，113 TS + 88 Rust（87 pass/1既有ignored）；无conversation Tauri invoke/event、TS/Vue、MiniMax、flag或远端动作；G3仍Partial，S8A/S8B未授权 |
| 2026-08-03 | 段成威 | 批准DEC-126-030并接受S7C Closure；以LIA-126-004单独授权S8A Desktop IPC与TypeScript ViewModel | G3保持Partial；只允许窄Tauri private IPC、TS validators/client/Pinia store；S8B Vue UI、MiniMax、flag、central pin与远端/发布动作继续禁止 |
| 2026-08-03 | Codex | 完成LIA-126-004 / S8A本地切片并提交DEC-126-031 Closure Review | 20个versioned commands、listen-only event、closed Schema/fixtures、Rust-bound context/cursor、strict TS validators、真实Tauri client和authoritative Pinia reducer完成；Desktop `make lint/test/build` PASS，127 TS + 94 Rust（93 pass/1既有ignored）；secret/path/raw-wire no-log与无Vue diff扫描PASS；G3仍Partial，S8B未授权 |
| 2026-08-03 | 段成威 | 批准DEC-126-031，接受S8A Closure Review | S8A Closure Passed；G3继续Partial；不自动授权S8B、feature activation、MiniMax或远端/发布动作 |
| 2026-08-03 | Codex | 保存四仓Accepted本地checkpoint并完成S8B0 UI Integration Readiness Review；提交DESIGN-126-006/DEC-126-032候选 | yijie/API/Host/Desktop分别形成仅本地commit；逐仓门禁与scope/no-log/diff检查通过。识别出closed readiness/storage private IPC缺口后停止源码实施；未push、未改contracts/Runtime、未开发Vue或启用flag |
| 2026-08-03 | 段成威 / Codex | Owner批准DEC-126-032并单独授权LIA-126-005；Codex完成S8B0本地实现并提交DEC-126-033 Closure Review候选 | Desktop `5dab02a1…34d85`：22个closed commands、exact-off gate、route/lifecycle/store/readiness/storage/Tasks接线；135 TS与95/96 Rust通过（1既有ignored）；未进入S8B、未启用flag、未调用MiniMax、未远端写入 |
| 2026-08-03 | 段成威 | 批准DEC-126-033并接受S8B0 Closure Review | S8B0 Closure Passed；G3继续Partial；不授权S8B、S9–S11、feature activation、MiniMax或远端/发布动作 |
| 2026-08-03 | 段成威 / Codex | Owner单独授权LIA-126-006 / S8B；Codex实现真实`/chat`与`/chat/:sessionId`、App Shell项目/session树、纯文本composer、assistant/raw reasoning、菜单/删除/scroll及light/dark/zoom/keyboard/focus/a11y，并提交DEC-126-034 Closure Review候选 | Desktop local checkpoint=`35f27447398529cca4dec85fa1f67e779c7a7cbd`；29/29个TS测试文件、164/164 tests、axe 0 serious/critical、Vite build、95/95 Rust（另1既有ignored）、npm audit与安全/bundle扫描PASS；flag仍off，0 IPC/Rust/contracts/Host/Runtime改动，0 MiniMax/远端动作；G3仍Partial、等待Owner接受DEC-126-034 |
| 2026-08-03 | 段成威 | 批准DEC-126-034并接受S8B Closure Review | S8B Closure Passed；G3继续Partial；不授权S9–S11、feature activation、MiniMax、四组件E2E或远端/发布动作；VoiceOver未声明人工通过并保留到S11/G6 |
| 2026-08-03 | 段成威 / Codex | Owner明确授权推送所有涉及改动的仓库；Codex将yijie/API/Host/Desktop既有FEAT-126 commits推送到各自`feat/feat-126-foundation-closure`并复验远端SHA | 四仓当时worktree均clean，无需新增或空commit；contracts候选已远端可达；未merge/tag/publish/deploy/activation |
| 2026-08-03 | Codex | 完成五仓`ls-remote`和临时clean clone复验，校正远端事实并提交DEC-126-035候选及LIA-126-007/S9授权建议 | 仅治理文档；未执行S9–S11、MiniMax或任何新增远端写入 |
| 2026-08-04 | 段成威 | 批准DEC-126-035并单独授权LIA-126-007 / S9 fake-provider Eval | 只允许Host权威dataset/runner、Desktop exact fixture消费与本地checkpoint；禁止MiniMax、flag、S10及远端/发布动作 |
| 2026-08-04 | Codex | 完成`feat126-title-raw-v1`确定性Eval并提交DEC-126-036 Closure Review候选 | Host `8707dea…c9378`、Desktop `adfdb5b…af9cb`均仅本地；title/raw/security gates PASS；G3仍Partial，S10–S11未授权 |
| 2026-08-04 | 段成威 | 批准DEC-126-036并接受S9 Closure Review | S4–S9 Closure Passed；G3继续Partial；不授权S10–S11、MiniMax、flag activation或远端动作 |
| 2026-08-05 | 段成威 / Codex | Owner批准DEC-126-053 Option A并校正R3根因；Codex完成DESIGN-126-011/S10BD0只读Docker execution capability与immutable resolver设计，提交DEC-126-054候选和LIA-126-017建议 | R3 fail-closed事实接受、Closure拒绝、BLK-004保持Open；current daemon endpoint不可达被existing verifier误报为image unavailable；未启动Docker/container/S10B，未修改Infra/业务源码，未授权LIA-126-017/S10B-R4/S11/远端动作 |
| 2026-08-05 | 段成威 | 批准DEC-126-054 Option A | 接受DESIGN-126-011的capability-first、closed failure classes、原始Compose pin identity与单独授权resolver probe方案；只批准设计决策，LIA-126-017仍未授权，BLK-004保持Open，未授权源码、Docker/probe、S10B-R4、S11或远端动作 |
| 2026-08-05 | 段成威 | 单独批准LIA-126-017，并明确不能自动进入实施 | S10BD1授权状态为Approved / Held / Not Started；本轮未修改Infra或业务源码，未启动Docker/probe，授权未消费；BLK-004保持Open，S10B-R4/S11/MiniMax/远端动作仍未授权 |
| 2026-08-05 | 段成威 / Codex | Owner随后明确指令开始并消费LIA-126-017；完成S10BD1 capability-first verifier、immutable identity与no-start resolver实现和验证，提交DEC-126-055 Closure候选 | Governance执行基线`075a5051b538ce8f28834db70de8f4f544ce4484`；Infra clean checkpoint `2a643caef210e32cab80242ede46b96927b2097a`；S10BD1-001–012、Infra 99/99与live 3 identity/3 probe PASS，资源归零且Docker恢复停止；BLK-004在Owner接受DEC-126-055前仍Open，未授权S10B-R4/S11/MiniMax/远端动作 |
| 2026-08-05 | 段成威 | 批准DEC-126-055推荐方案A，接受S10BD1 Closure并关闭S10B-BLK-004 | S10B-BLK-001–004现均Closed；G3仍Partial、G4/G6 Pending；此次接受不自动授权S10B-R4、S11、MiniMax、activation或远端动作 |
| 2026-08-05 | 段成威 | 单独授权LIA-126-018 / S10B-R4一次fresh四组件本地E2E | 仅S10B-001–012；不授权S11、MiniMax、源码修改、重跑或远端动作 |
| 2026-08-05 | Codex | 消费LIA-126-018：七仓SHA、S10BD1 resolver、fresh依赖、TLS/OIDC、synthetic users、migration/bootstrap与API readiness通过；fake-provider readiness因请求fixture身份错误返回403并按停止条件结束 | run `96a0a80d-27d4-4022-a470-4a7f004d9c4c`；正确run ID仍把S9 dataset bundle `feat126-title-raw-v1`误作Host固定fixture `normal-000`；S10B-001 FAIL、002–012 NOT RUN；登记S10B-BLK-005和DEC-126-056候选；清理后0 listener/container/network，4 volumes按边界保留，Docker恢复停止；0 MiniMax/Keychain/真实数据/源码/远端写入 |
| 2026-08-05 | 段成威 / Codex | Owner接受DEC-126-056 Option A并单独授权LIA-126-019；Codex实现Host-owned fake readiness与Infra唯一preflight runner并执行fresh组合预检；Owner随后接受DEC-126-057 Option A | Host `1ca4ee5…a560`、Infra `5723ffd…c0c9`；run `ed22fc82…f3f4`通过七SHA、依赖、identity、migration/bootstrap、API/fake readiness与no-log，summary `8198442e…f7d9`；S10BF1 Closure Passed、BLK-005 Closed；资源归零、Docker恢复停止，`s10b_r5_executed=false`；fresh R5仍须单独授权 |
| 2026-08-05 | 段成威 / Codex | Owner单独授权并消费LIA-126-020/S10B-R5；唯一组合preflight通过，但继续完整run时发现API runtime service-profile authority不一致，按停止条件fail closed并提交DEC-126-058候选 | run `24ae14b7…ad6`；S10B-001 PASS，summary `b3e4b833…b1f8`；S10B-002在API readiness前停止，003–012 NOT RUN；登记S10B-BLK-006 Open；0 Public Task/conversation/MiniMax/Keychain/真实数据/源码/远端写入；容器/网络/端口清理，4 volumes披露保留，Docker恢复停止 |
| 2026-08-06 | 段成威 / Codex | Owner以“正式增加closed `feat-126-s10-local-lab`并统一preflight/后续完整链消费、不得只改字符串或绕过校验”的明确指令接受DEC-126-058 Option A并单独授权/消费LIA-126-021/S10BRP1；API与Infra形成未提交本地corrective候选，提交DEC-126-059 Closure Review | API严格校验nonproduction、双exact flag、专用DSN、issuer/JWKS、CA pin、canonical port、loopback与v1隔离，FEAT-125语义保持；Infra以单一closed authority驱动preflight，由summary的`api_binary_sha256`绑定preflight-built binary，并由唯一continuation入口实际消费同run summary、reader与builder。Infra 113/113及launcher真实harness/负向矩阵通过，但未启动Docker/服务或执行S10B-002–012；BLK-006在Owner接受DEC-126-059前仍Open |
| 2026-08-06 | 段成威 / Codex | Owner批准DEC-126-059 Option A；S10BRP1 Closure Passed并关闭`S10B-BLK-006`。随后形成API与Infra clean local checkpoints，并单独授权LIA-126-022/S10B-R6 | API `d1c72b29ffc567abdb4521343a73ceef9ac9da34`、Infra `8f9b8965dbd32bb7273059a80bb818d4344e7135`，均clean/not pushed；fresh R6仅为Authorized / Not Consumed / Not Executed，本轮未启动Docker/服务，S10B-002–012、S11、MiniMax、activation与远端动作均未执行 |
| 2026-08-06 | 段成威 / Codex | 正式消费LIA-126-022执行唯一fresh S10B-R6；七仓SHA/clean与Docker 29.6.1/Compose 5.3.0通过，run `28afba8b…9cf0`在S10B-001 image resolver阶段fail closed，提交DEC-126-060处置候选 | 顶层closed class=`preflight_image_resolver_failed`；只读复核三项exact image Id/Descriptor/RepoDigest/OS/arch均匹配，但父runner未保留子级closed class，登记`S10B-BLK-007 Open`。S10B-002–012 NOT RUN；container/network/volume/listener=0，REJECTED hash=`7c7c5f61…5e11`，secret evidence hits=0；未修复、重跑、MiniMax、Keychain、真实数据、源码或远端动作 |
| 2026-08-06 | 段成威 / Codex | Owner批准DEC-126-060 Option A | 接受R6 fail-closed事实并拒绝R6 Closure；`S10B-BLK-007`保持Open。此次批准不授权错误传播纠偏、fresh R7、S11、MiniMax、activation或远端动作 |
| 2026-08-06 | 段成威 / Codex | Owner单独授权BLK-007 resolver错误透传设计评审；完成DESIGN-126-013并提交DEC-126-061候选 | 只读确认parent折叠child leaf；推荐closed result v1 + 同源validator + mapped leaf + 0600 evidence；冻结14项矩阵与old/new兼容。未改Infra源码、未运行Docker/resolver/S10B，LIA-126-023仍未授权 |
| 2026-08-08 | 段成威 / Codex | Owner继续执行指令接受DEC-126-061 Option A并单独授权/消费LIA-126-023；完成S10BEP1 repository corrective | resolver/parent/测试/Infra runbook已实现；128/128 tests、static validate、syntax/diff PASS。当前Docker CLI不能发现Compose且daemon访问permission denied，故full `make lint/test`尾段与isolated live resolver未完成；BLK-007继续Open，R7/S11未授权 |
| 2026-08-09 | 段成威 / Codex | 在Docker client/server 29.6.1、Compose 5.3.0与daemon access均通过后，仅执行S10BEP1-014 isolated live closure并重跑Infra/Governance门禁 | run `624bd64c-b378-4d53-97c0-05790e7e4657` exact passed envelope：3 identity/3 no-start probe；0600 evidence SHA-256 `e13f633f…6b34`，no-log/敏感payload命中0；三项exact image Id/RepoDigest/platform前后逐项一致且全局image count均为6，container/network/volume/listener=0；Infra 128/128、targeted 34/34、validate/make lint/test与Governance七类门禁PASS。`s10b_r7_executed=false`；Corrective Closure Review Pending、BLK-007仍Open，未commit/push |
| 2026-08-09 | 段成威 | 接受LIA-126-023/S10BEP1 Corrective Closure并形成DEC-126-062 | 确认S10BEP1-014、Infra全量门禁与Governance门禁PASS，关闭`S10B-BLK-007`；决策登记后的Governance default/strict/G2A/unique-key YAML/lint/test/shell/diff复跑PASS。G3保持Partial、G4/G6 Pending；fresh R7、S11、MiniMax、activation、真实数据、commit/push及其他远端写入仍未授权 |
| 2026-08-09 | 段成威 / Codex | Owner仅授权DEC-126-062后的local clean checkpoint closure并形成DEC-126-063 | 七仓范围与冻结SHA复核通过；Infra全量及Governance门禁复跑PASS。Infra形成clean local checkpoint `0842ff2dcf9be6fce7aa6b19adbb6ea475607136`，Governance由包含本决策的本地commit形成clean checkpoint；两仓均不push。fresh R7、S11、MiniMax、activation、真实数据及其他远端写入未授权 |
| 2026-08-09 | 段成威 / Codex | Owner单独授权并消费LIA-126-024 / S10B-R7 | 七仓exact/clean及Docker 29.6.1/Compose 5.3.0/daemon gate PASS；canonical run `d553e6ea-e10f-4470-b357-a41807d6fb06`的唯一preflight完成3 identity/3 no-start probe、fresh依赖、synthetic identity、migration/bootstrap、API/fake readiness与no-log，S10B-001 PASS。仓库不存在完整四组件S10B-002–012权威orchestrator，唯一continuation只启动API，因此S10B-002在任何continuation/业务链启动前fail closed，003–011 NOT RUN，012仅执行abort cleanup subset；4 volumes保留，container/network/process/listener=0，`s10b_r7_executed=true`。登记`S10B-BLK-008 Open`并提交DEC-126-064 Owner Closure Review，不自动纠偏、重跑或进入S11 |
| 2026-08-09 | 段成威 / Codex | Owner接受DEC-126-064 Option A，并仅授权S10B-BLK-008四组件orchestrator设计评审 | 接受R7 fail-closed事实、拒绝R7 Closure；只读冻结DESIGN-126-014：Infra单入口、same-run preflight、Infra→Desktop→Host→Runtime所有权、Desktop test driver/PKCE、Host Runtime/fake证据、API verifier、closed state/no-log/cleanup。DESIGN-126-014 Complete，DEC-126-065 Pending Owner Review；Governance default/strict/G2A/unique-key YAML/lint/test/shell/diff首轮及证据登记后复跑均PASS；本轮contract-impact=`none`，未来实现预期仅private interface `semantic`、central G2A=N/A；未实施、未启动服务、未commit或执行远端动作 |
| 2026-08-09 | 段成威 / Codex | Owner接受DEC-126-065 Option A并授权LIA-126-025/S10BO1 repository corrective；首次受限环境复验为Closure Pending（historical） | Infra/API/Host/Desktop实现DESIGN-126-014，Contracts/Runtime源码不变；S10BO1-001–014 targeted matrix 14/14及新增针对性测试、lint/build通过。API/Host全量测试受沙箱loopback listener限制，Host另有一项Runtime artifact测试在并行沙箱中被killed；Desktop全量Rust测试受loopback/SQLCipher文件属性/native bookmark/子进程能力限制，Infra完整Make门禁受Compose plugin不可见影响，故该次尝试不得形成Closure或commit；Governance default/strict/G2A/unique-key YAML/lint/test/shell/diff最终复跑PASS；未运行Docker live、isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认功能启用或远端动作 |
| 2026-08-09 | 段成威 / Codex | 无沙箱能力环境完成S10BO1 Corrective Closure全量门禁复验，提交Owner Review准备 | Docker client/server 29.6.1、Compose 5.3.0、daemon、loopback、0700/0600、subprocess、native bookmark及SQLCipher能力PASS；API/Host lint/race/build PASS；Desktop默认clippy首次暴露两个driver-only方法缺少feature cfg，Owner单独授权最小`contract-impact=none`修复后，30/167 TS、129 PASS/3 ignored Rust、production/default/feature build、feature clippy、driver 2/2及bundle driver-absent PASS；Infra validate/lint/test、142/142、Compose semantic及S10BO1 14/14 PASS；Governance与七仓diff PASS。状态为Review Ready / Pending Owner Acceptance，BLK-008仍Open；无live、fresh R8、commit或远端动作 |
| 2026-08-09 | 段成威 | 接受LIA-126-025/S10BO1 Corrective Closure并形成DEC-126-066 | 确认能力前置、API/Host/Desktop/Infra全量门禁、S10BO1-001–014与Governance门禁PASS，关闭`S10B-BLK-008`。决策后Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`复验PASS。G3保持Partial、G4/G6 Pending；isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认功能启用、commit、push及其他远端写入仍未授权 |
| 2026-08-09 | 段成威 / Codex | Owner仅授权DEC-126-066后的local clean checkpoint closure并形成DEC-126-067 | 七仓exact HEAD与scope复核通过；API/Host/Desktop/Infra全量门禁、Infra 142/142与S10BO1 14/14、Desktop default/feature及Governance全门禁均PASS。形成API `451940b282d8dd3e232ed414bd44b0677897f4c4`、Host `c5939b4d8b5ebc318a7beeb49b20f343802e59b9`、Desktop `d51e435cb8ea224e69f9707831ee71022d0a7b6e`、Infra `0b05ab3270b9d00fa2aec1c85a8c3bee7f33c25c`及包含本决策的Governance本地checkpoint；Contracts/Runtime不变。未执行isolated live、fresh R8、S11、MiniMax、真实数据/Keychain、默认启用或远端写入 |
| 2026-08-09 | 段成威 / Codex | Owner接受Desktop + Infra跨仓corrective评审Option A并形成DEC-126-068 / DESIGN-126-015；授权并完成LIA-126-026 / S10BO2 repository corrective | Desktop non-publishable feature build实际bootstrap、真实authorization-code + PKCE synthetic agent、trusted tenant/project native bookmark、Vue/Pinia/Tauri driver及FD3/FD4 closed控制通道完成；Infra startup/abort runner与ownership/termination/cleanup state machine完成。Desktop全量门禁、174/174 TS、default 134 PASS/3 ignored、feature 143 PASS/3 ignored、driver TS 7/7与Rust 6/6 PASS；Infra validate/lint/test 162/162及S10BO1+S10BO2 targeted 34/34 PASS。Desktop checkpoint `95f19ad557da0bf4cead90ed55d1e3ec60aefbc4`，Infra checkpoint `0fed8187d6051c011e67142d90feff89de326cfe`；`S10B-BLK-009 Open`，G3 Partial、G4/G6 Pending，`s10b_r8_executed=false`。Corrective Closure仍待Owner接受；未执行Docker live、isolated live、fresh R8或业务调用 |
| 2026-08-09 | 段成威 | 授权更新FEAT-126治理文档、提交所有相关本地改动并推送对应远端分支 | 本次远端授权仅覆盖Governance、API、Host、Desktop与Infra现有FEAT-126候选提交；Contracts/Runtime无新提交，不制造空commit。不得据此执行merge、tag、publish、deploy、isolated live、fresh R8、S11、MiniMax、真实数据/Keychain或默认功能启用 |
| 2026-08-09 | 段成威 | 接受LIA-126-026/S10BO2 Corrective Closure并关闭S10B-BLK-009 | 确认Desktop完整门禁、feature Rust 143 PASS/0 FAIL/3 ignored、Infra 162/162、S10BO1+S10BO2 targeted 34/34、no-log、production driver-absent及ownership/cleanup门禁全部PASS；决策登记后Governance default/strict/G2A、unique-key YAML、lint/test、shell syntax与`git diff --check`复跑PASS。G3保持Partial、G4/G6 Pending；`s10b_r8_executed=false`；isolated live、fresh R8、业务调用、S11、MiniMax、真实数据/Keychain、默认启用、commit、push及其他远端写入仍未授权 |
| 2026-08-09 | 段成威 / Codex | Owner单独授权并消费LIA-126-027 / S10BO2 isolated live startup/abort | 七仓exact/clean、Docker client/server 29.6.1、Compose 5.3.0、daemon、loopback、SQLCipher/0600、native bookmark及subprocess能力PASS。canonical run `b68804f0-aaf9-4da4-95e1-aa3b605bfada`在preflight创建run root前fail closed，最终closed frame=`orchestrator_cleanup_unknown`；只读诊断确认orchestrator未把七个SHA作为子Make要求的`GOVERNANCE_SHA`等变量传入，随后absent-run stop把cleanup标记unknown并覆盖原始preflight leaf。run root/五进程身份/no-log证据不存在，故isolated live Closure FAIL并登记`S10B-BLK-010 Open`、`DEC-126-069 Pending Owner Review`。该project container/network/volume=0，六端口listener=0，daemon恢复6 containers/0 running/6 images；无服务、业务case或provider调用，`s10b_r8_executed=false`；Governance八项门禁首轮及证据回写后最终复跑均PASS；不重试、不修复、不commit/push |
| 2026-08-09 | 段成威 / Codex | 接受DEC-126-069 Option A，完成DESIGN-126-016并实施LIA-126-028 / S10BO3 Infra corrective | 保留失败run不可复用且不重跑live；修复七SHA单一Make authority、primary/secondary failure projection、attempt ledger、pre-run/partial-run cleanup与no-log scopes、phase/process-role reconcile和exact volume/listener inventory。Infra Node syntax、validate、lint、180/180 full tests、四个targeted文件59/59及`git diff --check`全部PASS；S10BO3-001–014全部PASS。`S10B-BLK-010`在Owner Corrective Closure前保持Open，G3 Partial、G4/G6 Pending，`s10b_r8_executed=false`；isolated live、fresh R8、业务case、commit和远端写入均未执行 |
| 2026-08-10 | 段成威 / Codex | 完成S10BO3 Corrective Closure Review准备 | Infra `make test` 在最小Darwin vmmap能力提升下 `186/186 PASS`；S10BO3 targeted 扩展为 `65/65 PASS`（含015–020：成功immutable closure、preflight failure-class绑定、Compose日志抓取/泄漏拒绝、API/fake前后投影不变、marker-only reconcile、Host/Runtime持久证据）；`pnpm validate`、`make lint`、Compose semantic、Node syntax、`git diff --check`全部PASS。未执行Docker live、isolated live、fresh R8、业务调用或远端写入；状态仍为Review Ready / Pending Owner Acceptance，`S10B-BLK-010 Open`，`s10b_r8_executed=false` |
| 2026-08-10 | 段成威 | 接受LIA-126-028 / S10BO3 Corrective Closure | 确认DESIGN-126-016完成、Infra `186/186`、S10BO3-001–020及targeted `65/65`、Node syntax、`pnpm validate`、`make lint`、Compose semantic、`git diff --check`与Governance全部门禁PASS，关闭`S10B-BLK-010`；保留`b68804f0-aaf9-4da4-95e1-aa3b605bfada`失败且不可重用，`s10b_r8_executed=false`、G3 Partial、G4/G6 Pending；未授权live、fresh R8、业务调用、commit或远端写入 |
| 2026-08-10 | 段成威 / Codex | Owner仅授权S10BO3后的Infra + Governance local clean checkpoint closure并形成DEC-126-070 | 七仓HEAD/scope复核通过，仅Infra五个S10BO3 corrective文件与Governance既有九份治理文件进入候选；Infra `186/186`、targeted `65/65`与Governance全门禁PASS。Infra形成clean local checkpoint `91f7ec03372b1528abb93818abfad432a83327c4`，Governance由包含本记录的本地commit形成checkpoint；不push。G3 Partial、G4/G6 Pending、`s10b_r8_executed=false`保持，未执行live、fresh R8或业务case |
| 2026-08-10 | 段成威 / Codex | Owner单独授权并消费LIA-126-029 / S10BO3 isolated-live startup/abort | 七仓以Governance `f7532cc9d138a2215f75441a737be4079642ed0e`、Infra `91f7ec03372b1528abb93818abfad432a83327c4`及其余五仓既定SHA保持exact/clean。canonical run `8b94dc6d-5984-4579-9e0c-bed43a4b872f`在attempt marker、preflight与run root创建前以`orchestrator_process_identity_unknown`停止：Make用相对`node`启动，Darwin `ps comm=`只返回`node`，不能满足绝对binary identity。startup/ownership/abort与业务case均NOT RUN；Public Tasks/conversation/turn/provider调用为0，project container/network/volume、固定listener观测为0，`s10b_r8_executed=false`。因ledger/no-log/cleanup证据未创建，正式no-log和cleanup Closure均NOT ESTABLISHED；该run永久不可重试、续跑或复用 |
| 2026-08-10 | 段成威 / Codex | Owner单独授权DESIGN-126-017 / LIA-126-030单仓Infra corrective并接受Closure | canonical Make入口改为解析和调用绝对Node；在进程身份检查前以0600/O_EXCL canonical preclaim预占run，并在marker前失败时写入绑定preclaim SHA-256的content-free failure。失败或不完整preclaim继续fail closed且不可执行，preclaim纳入no-log source set，legacy marker-only attempt保持兼容。Infra四文件corrective通过Node syntax、`pnpm validate`、`make lint`、Compose semantic、`make test` `188/188`、四文件targeted `67/67`、绝对Node self identity与`git diff --check`；未执行live、fresh R8或业务case |
| 2026-08-10 | 段成威 / Codex | Owner仅授权形成新的Infra/Governance clean checkpoint并接受DEC-126-072 | Infra四个corrective文件形成local clean checkpoint `c7edbc344daecb84553efafe86dfe335a5c0c72d`；Governance只更新既有九份FEAT-126文件并形成包含该精确SHA的本地checkpoint。其余五仓保持既定clean SHA；两个checkpoint均不push。获得新的精确SHA与另一份isolated-live一次性授权前，禁止再次执行live；fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用及远端动作仍未授权 |
| 2026-08-10 | 段成威 / Codex | Owner授权DESIGN-126-019 / LIA-126-033一次性综合startup-surface corrective；实施完成并进入Owner acceptance review | 最小产品范围保持Desktop五个授权文件、Infra既有orchestrator与两个targeted tests及FEAT-126治理记录。Desktop `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd`和Infra `5fdba2b22b343237683f383f098fa2ffaea5bc54`已形成local clean/not-pushed checkpoint；Desktop TS `178/178`、default Rust `134 pass/3 ignored`、feature Rust `149 pass/3 ignored`、targeted TS/Rust各`11/11`及lint/build/clippy通过；Infra targeted `50/50`、full `192/192`、syntax/validate/diff通过。独立审查发现的v3 reader canonical source绑定与`APIKey`/plural/pretty JSON两个P1均已修复并回归；无open P0/P1。`make lint`只执行到`pnpm validate`通过，随后本机`docker compose`发现失败并以125停止，未启动容器；corrective禁止Docker，故未重试或伪报Compose semantic PASS。Contracts/API/Host/Runtime不变；未执行isolated live、fresh R8、业务case、S11、MiniMax、真实数据/Keychain、默认启用或远端动作；`s10b_r8_executed=false`。Corrective Closure为Review Ready / Pending Owner Acceptance |
| 2026-08-12 | 段成威 / Codex | Owner接受DESIGN-126-019 / LIA-126-033 Corrective Closure并形成DEC-126-076 | 只读复核Desktop `e8e56df00cd7acd6c99fcfb36bedc6e892fa7fdd`、Infra `5fdba2b22b343237683f383f098fa2ffaea5bc54`及Compose semantic证据完整：targeted/full门禁PASS、独立审查无open P0/P1、Compose 5.3.0 direct config与Infra `make lint/test` `192/192` PASS。environment-bound gap Closed；真实Tauri `AppHandle/setup` direct fixture保留P2/live；G3 Partial、G4/G6 Pending。仅形成Governance本地clean checkpoint；未执行Docker lifecycle、isolated-live、fresh R8、业务调用或远端动作，`s10b_r8_executed=false` |
| 2026-08-13 | 段成威 / Codex | DEC-126-085接受LIA-126-047 isolated-live startup/abort成功Closure，并授权后续一次fresh R8 | run `7e18d0aa-317e-4fa5-a7a5-a93d7880eb8e`以七仓exact clean SHA完成API/fake/Desktop/Host/Runtime startup、ownership/readiness、single abort、no-log与cleanup；runtime-log-scan v4 `4 sources/69 rows/0 hits`，整体`31 local files + 4 external sources/95 rows/0 hits`，业务调用和provider调用均为0，`s10b_r8_executed=false`。Owner接受该startup/abort Closure但不把它冒充S10B-001–012、G4或G6。LIA-126-048只授权在本Governance checkpoint后，以新七仓exact clean SHA、现场生成的新UUIDv4和真实canonical full-case入口执行一次frozen synthetic `normal-000`/fake-provider fresh R8；入口缺失或preflight失败时不得拼装、重试或降级 |
| 2026-08-14 | 段成威 / Codex | Owner接受DESIGN-126-027 / LIA-126-049 post-ready failure durability Corrective Closure并形成DEC-126-087 | LIA-126-048 run `2cc440eb-632d-456b-abb1-f95b12c14b5a`已消费且永久不可复用；历史primary为`orchestrator_control_eof` at `runtime_ready`，五组件process evidence齐全，runtime-log-scan v4为`4 sources/69 rows/0 hits`，但整体no-log closure因reached-phase evidence集合错误而失败。Desktop `88382304b46002ce3e44f7f3bb30104dbd4b11ea`增加post-ready content-free terminal、first-terminal-wins及默认非feature cfg闭包；Infra `06baf058d6bafd7bce6310574066b990098e80f4`持久化post-ready leaf、仅在无完整frame时投影exit/EOF并按实际phase要求no-log evidence。两仓全量/targeted/build/config-only门禁及只读复审通过，无open P0/P1；corrective阶段未执行R8、isolated-live或Docker lifecycle，下一次R8仍需新七仓SHA、fresh UUIDv4和单独一次性授权 |
| 2026-08-15 | 段成威 / Codex | Owner以DEC-126-088接受DESIGN-126-028 Host bbolt opaque CWD authority；LIA-126-050仅消费Governance更新授权 | exact FEAT-126 profile可在private run-scoped bbolt中以metadata `feat126_cwd_encoding=opaque-project-v1`和record sentinel `feat126-s10-project`代替absolute project bytes；每次打开及planned restart均须重新验证同一run authority并只在内存重建canonical `<run_root>/project`。默认模式、public Host wire和schema shape保持不变；Host contract描述须在后续corrective从权威source同步，明确private persistence representation不属于wire contract。本轮允许Host/Desktop/Infra保持既有dirty draft但不接受、不暂存、不提交；禁止Docker/live/R8/MiniMax及远端动作 |
