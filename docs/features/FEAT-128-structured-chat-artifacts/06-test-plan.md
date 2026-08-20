# FEAT-128 测试与 Eval 计划

## 1. 测试策略

- 风险等级：high；重点是 closed event compatibility、confidential content、native 文件写入、大媒体资源、历史/删除和 capability 误启用。
- 阻断质量门槛：Contracts/Host/Desktop 对应 generate、lint、test、build 全绿；v1/v2 equality 与双基线 breaking 通过；P0/P1/P2 清零；light/dark/1180x760/200%/keyboard/axe 通过；真实 VoiceOver 结果如实记录。
- 类生产依赖：本期没有生产环境。Runtime handshake 可以使用固定本地产物；媒体内容使用 deterministic synthetic fixture。
- 不可执行环境：真实 MiniMax image/video/file/report generation、费用/延迟/质量 Eval、签名 Desktop、生产监控和云回滚当前均未授权或不存在，记录为 BLOCKED/NOT RUN。
- 测试数据：仅合成安全数据，包含 canary path/token/body 字符串用于证明不会泄漏。

## 2. AC -> 测试追踪矩阵

| AC/NFR | 风险 | Test ID | 层级 | 场景 | 环境 | 预期证据 |
|---|---|---|---|---|---|---|
| AC-001/NFR-001 | 占位晚出现/布局跳动 | EVT-001, UI-001, PERF-001 | contract/store/visual | started 在 terminal 前到达，300ms 内稳定显示 | synthetic local | event timestamp、DOM state、layout shift screenshot |
| AC-002 | 重复/乱序/双终态 | EVT-002, STORE-001, RES-001 | contract/unit/integration | duplicate、gap、percent regression、late progress | no network | 幂等、resync、终态不回退 |
| AC-003 | 图片炸弹/handle 重放/保存越界 | ART-IMG-001, SEC-001/007/009, UI-002 | Host/native/UI | PNG/JPEG/WebP、magic/20MiB、one-shot handle、lightbox/save | synthetic PNG/JPEG/WebP only | schema、双次 digest、protocol、keyboard、atomic save evidence |
| AC-004 | 视频不可 seek/OOM/autoplay | ART-VID-001, SEC-002, UI-003 | Host/native/UI | MP4/WebM metadata/range/64MiB/autoplay off | synthetic tiny media + boundary stream | 206/416、controls、memory、fallback |
| AC-005 | 文件内容执行/截断不明 | ART-FILE-001, SEC-003, UI-004 | native/UI | text/MD/JSON/CSV preview；PDF/Office unsupported preview | synthetic files | text-only DOM、row/byte caps、save/fallback |
| AC-006 | report XSS/任意 chart option | ART-RPT-001, SEC-004, UI-005 | schema/adapter/UI | safe sections、unknown optional accepted/opaque、unknown required rejected、HTML/URL/script rejection | report v1 fixtures | schema errors、chart text summary、no `v-html` |
| AC-007 | 历史丢失/过期残留 | DB-001, DB-002, E2E-001 | migration/integration/E2E | v7->v8、reopen、TTL、WAL、delete | temp SQLCipher DB | metadata order、content physically absent、cleanup receipt |
| AC-008 | 跨租户/路径/token 泄漏 | SEC-005, SEC-006, ACK-001 | integration/security | wrong session/token、redirect、href/path injection、ACK digest/conflict/replay、log/DOM scan | loopback fake Host | 404/deny、idempotent receipt、canary hit count 0 |
| AC-009 | 旧 consumer 被击穿 | COMP-001..004 | contract/producer/consumer | old/new Host/Desktop matrix | canonical fixtures | v1/v2 byte equality、v3 explicit negotiation |
| AC-010 | 主题/窗口/a11y 回归 | UI-006..010 | component/visual/manual | light/dark、1180x760、200%、keyboard、axe、VoiceOver/reduced motion | visual harness + macOS | screenshots、axe JSON、manual checklist |
| AC-011 | synthetic 冒充真实 | CFG-001, E2E-002 | config/E2E | exact local profile、default off、visible synthetic source | local only | startup rejection/default-off/fixture flow |
| AC-012 | provider 未验证却开启 | CAP-001, CFG-002 | runtime/config | capability false/unknown、real flag request | fixed Runtime fake | no producer/no UI capability；typed readiness |
| NFR-002/003 | UI 卡顿/内存放大 | PERF-002, PERF-003 | performance | burst progress、12 artifacts、20/64MiB preview | local sampled build | <=10Hz、<50ms long task target、<=2.5x memory target |
| NFR-004 | 资源泄漏 | RES-002 | unit/integration | switch session/close modal/expire/replay handle/abort save | synthetic | handle/read/temp/decoded image counters released |

## 3. 领域与边界测试

| 类别 | 正常 | 边界 | 非法/失败 | Test IDs |
|---|---|---|---|---|
| Artifact 状态机 | started-progress-completed | 无百分比、0/100、duplicate replay | progress-before-start、回退、double terminal、gap | EVT-001/002, STORE-001 |
| 公共 API/SSE | v3 route、content/poster GET/HEAD、ACK、range | `after` cursor、first/last byte、HEAD、duplicate ACK、12 items | `after_sequence` alias、v1/v2 emission、wrong version、redirect、404/409/410/416/500 | COMP-001..004, SEC-005, ACK-001 |
| Desktop DB/事务 | transfer commit/history/save | crash before/after commit、same digest | storage full、WAL busy、integrity mismatch、cleanup partial | DB-001/002, RES-001 |
| 媒体/文件 | allowlisted kinds/formats | exact size、dimensions/duration/rows | MIME/magic mismatch、malformed JSON、decode bomb | ART-*、SEC-001..004 |
| UI/可访问性 | loading/ready/preview/save | long names、12 items、zoom | permission/expired/unsupported/unknown/error | UI-001..010 |
| 配置/provider | synthetic exact local、capability true | host old/new | non-local synthetic、provider unknown、flags conflict | CFG-001/002, CAP-001 |

## 4. 兼容与 Conformance

- 未知字段：v3 readers 忽略 schema 允许的 additive optional fields；required/closed object drift 拒绝并 resync。
- 未知 enum/event：v1/v2 永不接收 Artifact。Desktop 先用宽 envelope 捕获未知 kind/status/version，再将该项映射为
  `unsupported` 占位；已知 variant 才进入 strict schema/renderer。未知 report optional section 同样由 report
  adapter 降级并继续同一文档；Host 不发未经评审的 enum。
- 新旧 producer/consumer：覆盖 04 文档的七种组合，尤其 new Host + old Desktop 与 old Host + new Desktop。
- 生成漂移：Contracts `check-generated`、Host `contract-check`、Desktop `generate:check` 必须从同一不可变 commit 通过。
- Canonical fixture：唯一位于 `yijie-contracts/tests/fixtures/agent/session-event-v3/` 与 report v1 schema fixture；下游只引用/pin，不复制修改。Desktop private IPC 计划路径为 `yijie-desktop/src-tauri/schemas/chat-ipc-v3.schema.json`，版本 3，不能替代公共 v3 event schema。
- Runtime 兼容：固定 `yijie-codex@0ce5902...` imageGeneration started/completed shape映射测试；`savedPath` 和 raw base64 不出现在 Host event。
- Breaking：同时对 published `f16a497e...` 和当前 downstream candidate `747cf740...` 执行完整 baseline 检查，并人工验证 v1/v2 equality。

## 5. 安全与隐私测试

| Test ID | 威胁 | 场景 | 预期结果 |
|---|---|---|---|
| SEC-001 | 图片炸弹/伪装 MIME | 巨大像素、小 bytes、magic mismatch、truncated image | 签发及 protocol GET 双次拒绝；Vue/Pinia/DOM 不收到 bytes/base64/digest/path |
| SEC-002 | 视频 range/解码滥用 | multi-range、invalid range、伪装 container、超时 stream | 仅单 range；416/timeout；降级不崩溃 |
| SEC-003 | 文件内容执行 | Markdown HTML、CSV formula、JSON control、active link | 普通文本展示；无 HTML/script/network/tool action |
| SEC-004 | report 注入 | raw HTML、javascript URL、任意 ECharts option、unknown optional/required、超大 table | known invalid/unknown required 拒绝；unknown optional opaque fallback；无遍历/执行 |
| SEC-005 | 越权/资源枚举 | wrong bearer/session/tenant/artifact | fail closed，404 不泄露存在性 |
| SEC-006 | secret/path/body 泄漏 | canary 放入 savedPath、provider error、filename、content | SSE/log/DOM/snapshot 命中 0 |
| SEC-007 | 任意文件写/覆盖 | `../` 名称、symlink、已有文件、取消 dialog、写满磁盘 | 只写用户选择目标；原子覆盖需明确确认；temp 清理 |
| SEC-008 | synthetic 误启用 | production/non-local/default env | 配置启动失败或 capability false |
| SEC-009 | opaque handle/协议重放 | 猜测、重复 GET、跨 WebView/context/session、query/body/HEAD/Range、过期/重启、并发/容量超限 | 仅 first bound GET 200；其它 empty 404 或 stable typed limit；无 CORS/redirect/oracle |
| SEC-010 | CSP/capability 越界 | Artifact 尝试 asset/blob/data/fetch，或新增 fs/shell/dialog plugin/capability | 仅 `img-src yijie-artifact-preview:` delta；forbidden changes hit count 0 |

## 6. 韧性与故障测试

| Test ID | 故障 | 注入方式 | 恢复预期 | 观测信号 |
|---|---|---|---|---|
| RES-001 | SSE gap/Host restart | 丢 sequence、换 stream_id | 停止局部应用，resync；已存 ready 可用 | typed resync code，无重复 transfer |
| RES-002 | UI 卸载/取消 | 切 session、关闭 lightbox、handle TTL/consume、abort save | clear img src、release registry、cancel、删 normal-failure temp | handle/read/temp counter 回零；restart handle invalid |
| RES-003 | storage full/WAL busy | temp volume limit、held reader | 不置 ready，保留可重试 transfer | typed storage code |
| RES-004 | staging TTL/ack loss | duplicate/conflicting ack、丢 ack、推进 `staged_at`、Host restart | 相同 ACK 幂等、冲突拒绝；Desktop 已存内容不受影响；Host encrypted spool 清除 | receipt + bytes counter 归零 |
| RES-005 | partial turn | 一项 complete、一项 failed、turn complete | ready 保留，failed 卡稳定，turn terminal 正确 | per-artifact + turn state |
| RES-006 | save failure | permission denied、disk full、cancel | authority copy 保留，可再次保存 | no stored target path |

## 6A. S6A 测试先行门禁

S6A 必须先提交失败测试并记录 RED，再写最小 native boundary；S6B renderer 不得出现在 S6A diff。

| Layer | 必须先失败的测试 | GREEN 必须证明 |
|---|---|---|
| private schema/TS parser | 3 command names、identity-only payload、closed result/error 枚举不存在 | schema/TS exact-key；path/name/MIME/digest/href/bytes/base64 字段全部拒绝 |
| repository/worker | ready image content reader 不存在 | owner+tenant+session+turn+artifact、state/kind/MIME/size/BLOB/digest/image limits 双次复核；expired/foreign/not-ready fail closed |
| handle registry | registry/limits/release 不存在 | 256-bit/43-char handle、30s absolute TTL、one-shot atomic consume、4 per WebView/1 per Artifact、2 reads/40MiB、session/context/restart cleanup |
| custom protocol | scheme handler 不存在 | exact host/path/GET；200 headers；no CORS/redirect/HEAD/Range/query/body；全部失败 empty 404；main WebView binding |
| native save | image save operation 不存在 | explicit intent、canonical extension、native cancel/overwrite、symlink/nonregular reject、0600 temp、chunk digest、fsync/atomic replace、normal failure cleanup、authority retained |
| leak/config | current baseline only | no bytes/base64/digest/Host href/path/bearer in Vue/Pinia/DOM/log/snapshot；only one `img-src` scheme delta；capability/deps/lockfile unchanged |

S6A focused commands must include Rust unit/integration tests for `artifact_native` repository/registry/protocol/save plus
Vitest schema/client negative tests. `pnpm lint`、`pnpm test`、`make build`、`pnpm docs:build` 与 `git diff --check`
随后全量通过。S6A 只能在这些证据和 atomic Desktop commit 后记为 PASS；readiness 文档不是测试结果。

## 7. Migration 演练

| 组合 | 数据状态 | Reader/Writer | 预期 | 校验 |
|---|---|---|---|---|
| old app + expanded v8 DB | future schema | old reader | fail closed，不损坏 DB | explicit user_version rejection |
| new app + v1-v7 DB | legacy messages/attachments | new reader/migrator | migration 成功，旧消息无 Artifact | checksum + populated fixtures |
| new app + v8 Artifact | announced/transferring/ready/failed/expired | new reader/writer | reopen 顺序/状态/bytes 正确 | crash-point + history tests |
| rollback/roll-forward | v8 DB | old/new binary | 旧 binary 不原地打开；恢复升级前加密备份或 v8 roll-forward | backup restore rehearsal |
| cleanup | ready content + WAL/cache/staging | deletion/TTL worker | bytes、relation、preview、staging 均不可读 | checkpoint/reopen/forensic query |

## 8. 性能与容量

| Metric | Workload | Baseline | Pass threshold | Stop threshold |
|---|---|---:|---:|---:|
| announced visible p95 | 100 synthetic turns | 未建立 | <300ms | >=1000ms |
| progress render rate | 100 events/sec burst | 未建立 | <=10Hz/component | >20Hz sustained |
| long task | 12 mixed artifacts | 未建立 | no task >50ms target | any task >200ms |
| preview memory | 20MiB image / 64MiB video | 未建立 | <=2.5x bytes target | >3x or crash/OOM |
| transfer integrity | range/full content | 未建立 | 100% digest match | any silent mismatch |
| cleanup | 128MiB turn | 未建立 | content inaccessible after completion | any residual readable content |

这些阈值是 G2 候选；实际 baseline、工具和样本数必须在实现前由 Owner 批准，未测结果不能写成 PASS。

## 9. AI Eval 专项

| 项目 | 固定值/版本 |
|---|---|
| Protocol/UI dataset | deterministic synthetic `feat128-artifact-v1`，包含四 kind、失败、乱序、过期和注入样本 |
| Model/prompt/skill/knowledge/tool schema | synthetic 阶段 N/A；MiniMax-M3/Runtime 只作为 capability 调查基线 |
| Seed/temperature/runner | synthetic exact fixture，无采样 |
| 结构通过率 | 100% canonical accepted；100% invalid rejected |
| 任务成功率 | synthetic vertical slice 100% |
| 工具选择/参数正确率 | N/A，首期不启真实 tool producer |
| 引用/无答案/安全 | unsupported provider 必须文本说明且不产生虚假 Artifact |
| 延迟与成本 | synthetic cost 0；真实 provider值 BLOCKED |
| 相对基线不可退化阈值 | v1/v2 text/reasoning/session tests 0 regression |

真实 MiniMax image/video/file/report Eval 需用户单独授权付费调用、固定 provider API/model、最多调用次数、质量 rubric 和成本停止阈值；当前不执行。

## 10. Fixture 与测试数据

| Fixture/Dataset | 权威位置 | 数据分类 | 合成/脱敏方式 | Consumer |
|---|---|---|---|---|
| v3 lifecycle JSON | `yijie-contracts/tests/fixtures/agent/session-event-v3/` | public synthetic | UUID、1x1/小媒体、无路径/正文 | Host/Desktop |
| report document v1 | `yijie-contracts/jsonschema/report/report-document-v1.schema.json` + canonical fixtures | public synthetic | 虚构指标/日期/来源，无店铺数据；media type `application/vnd.yijie.report+json;version=1`；PDF/Markdown 仅作 derived export | SDK/Desktop renderer |
| media boundary corpus | implemented S3/S4 testdata + future UI corpus | public synthetic | generated headers/containers/corruption | Host/Desktop native validators PASS；UI later |
| canary leak corpus | implemented native checks + planned DOM scanner | restricted synthetic marker only | 明确 path/token/body canary，不含真实 secret | native no-content projection PASS；DOM later |
| migration DB corpus | Desktop temp fixtures | confidential synthetic | v1-v8 fake tenant/session | Rust repository tests |

## 11. 实际执行命令

| 层级 | Repository/CWD | Command | 环境依赖 | 预期时长 |
|---|---|---|---|---|
| package G2 structure | yijie | `docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G2 docs/features/FEAT-128-structured-chat-artifacts` | bash | <1 min |
| governance docs | yijie | `pnpm lint && pnpm test && bash -n scripts/*.sh` | Node 24/pnpm 11 | <2 min |
| contracts | yijie-contracts | `pnpm generate && pnpm lint && pnpm test && pnpm build` | locked Node/Go/buf generators | 2-5 min |
| breaking published | yijie-contracts | `./scripts/check-breaking.sh f16a497e1377f45747f8ff9292b4b60cf2027f88` | git baseline | 1-3 min |
| breaking current candidate | yijie-contracts | `./scripts/check-breaking.sh 747cf740f2d91e76e5c1a130e8e009f1efa821b8` | git baseline | 1-3 min |
| Host | yijie-agent-host | `make lint && make test && make runtime-test` | fixed Runtime artifact for runtime-test | 3-8 min |
| Desktop | yijie-desktop | `make lint && make test && make build && pnpm docs:build` | Node/Rust/pnpm | 5-15 min |
| Desktop all Rust | yijie-desktop | `cargo test --manifest-path src-tauri/Cargo.toml --all-targets --all-features` | Rust toolchain | 5-15 min |
| visual/a11y | yijie-desktop | FEAT-128 Vite harness + Playwright screenshots/axe command recorded when harness exists | local browser | 3-10 min |
| real MiniMax | isolated local environment | command not defined or authorized | API key, paid network, fixed provider evidence | BLOCKED |

## 12. 通过、失败与 Flaky 策略

- PASS：命令完成、退出码为 0、断言与人工语义检查符合 AC；visual golden 由人审阅。
- FAIL：任何阻断断言失败、silent skip、canary 泄漏、P0/P1/P2、未知真实费用或旧 consumer 回归。
- NOT RUN：环境缺失、被跳过、输出截断、进程未完成或尚未有实现/命令。
- Flaky：先定位时间、媒体解码、端口或资源根因；不允许“重跑到绿”。
- Snapshot/golden：必须检查 light/dark、1180x760、200% 和最长中文/文件名，不以像素接近替代行为验收。

## 13. 测试计划批准

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 测试/技术 Owner | 段成威 | G2A APPROVED；S1/S2/S2P evidence PASS | 2026-08-20 |
| 安全/数据 Owner | 段成威 | G2A boundary APPROVED；S3/S4/S5 evidence PASS；S6A readiness APPROVED，implementation NOT RUN | 2026-08-20 |

Contracts、pin conformance 与 S3/S4/S5 命令已实际执行并记录于 08；S6A/S6B 及以后仍须按本计划执行，不能因
readiness 批准或 G3 对基础切片通过而预先记为通过。
