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
| AC-004 | 视频不可 seek/OOM/autoplay | ART-VID-001, SEC-002/011, UI-003 | Host/native/UI | frozen MP4 metadata/range/64MiB/autoplay off；WebM 未批准 | canonical 1,642-byte MP4 + boundary responses | 200/206/416、controls、memory、fallback |
| AC-005 (`PARTIAL`) | 文件内容执行/截断不明；Markdown 不在 v3 output | ART-FILE-001, SEC-003/006, UI-004 | native/UI | plain/JSON/CSV bounded preview；PDF/XLSX unsupported-inline + save；Markdown contract blocker | Desktop-private synthetic files | text-only DOM、exact caps、search/save/fallback；G4 不通过 |
| AC-006 | report XSS/任意 chart option/consumer 漂移 | ART-RPT-001, SEC-004, UI-005 | schema/native/UI | contract-valid Unicode/date-time/duplicate/mismatched chart；known sections；unknown optional omitted、unknown required rejected；HTML/URL/script rejection | report v1 fixtures + Desktop-private valid differential cases | S9A/S9B-D/checker repair/S9B-R separate PASS；production vertical NOT RUN |
| AC-007 | 历史丢失/过期残留 | DB-001, DB-002, E2E-001 | migration/integration/E2E | v7->v8、reopen、TTL、WAL、delete | temp SQLCipher DB | metadata order、content physically absent、cleanup receipt |
| AC-008 | 跨租户/路径/token 泄漏 | SEC-005, SEC-006, ACK-001 | integration/security | wrong session/token、redirect、href/path injection、ACK digest/conflict/replay、log/DOM scan | loopback fake Host | 404/deny、idempotent receipt、unauthorized/path/token/raw-error canary hit count 0 |
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
| SEC-002 | 视频 range/解码滥用 | no/closed/open/suffix/multi/invalid/unsatisfiable range、伪装 container、超时 | 200/206/416 精确；仅单 range；bounded failure/fallback |
| SEC-003 | 文件内容执行 | plain/JSON control/bidi、CSV formula/quotes、HTML/link-like text；Markdown 仅在未来 contract reopen 后测试 | bounded text/cell nodes；无 HTML/script/network/formula/tool action |
| SEC-004 | report 注入/consumer drift | raw HTML、javascript URL、任意 ECharts option、unknown optional/required、超大 table；Unicode/date-time/duplicate IDs/keys/mismatched chart 的 contract-valid differential fixtures | known invalid/unknown required 拒绝；unknown optional 仅 unsupported marker、payload/type 不投影；contract-valid document 不被额外拒绝；无 raw JSON/遍历/执行 |
| SEC-005 | 越权/资源枚举 | wrong bearer/session/tenant/artifact | fail closed，404 不泄露存在性 |
| SEC-006 | secret/path/body 泄漏 | canary 放入 savedPath、provider error、path/token/digest、未授权内容或超出已批准 bounded projection 的正文；另以授权 preview marker 验证 open/close 生命周期 | 前者 SSE/state/log/DOM/snapshot 命中 0；用户显式打开的 bounded marker 只在当前组件 DOM 存在，小文件 projection 可在 caps 内等于完整正文；close/switch/unmount 后归零且永不进 Pinia/history/log/diagnostics/snapshot |
| SEC-007 | 任意文件写/覆盖 | `../` 名称、symlink、已有文件、取消 dialog、写满磁盘 | 只写用户选择目标；原子覆盖需明确确认；temp 清理 |
| SEC-008 | synthetic 误启用 | production/non-local/default env | 配置启动失败或 capability false |
| SEC-009 | opaque handle/协议重放 | 猜测、重复 GET、跨 WebView/context/session、query/body/HEAD/Range、过期/重启、并发/容量超限 | 仅 first bound GET 200；其它 empty 404 或 stable typed limit；无 CORS/redirect/oracle |
| SEC-010 | CSP/capability 越界 | Artifact 尝试 asset/blob/data/fetch，或新增 fs/shell/dialog plugin/capability | image exact `img-src` + video exact `media-src` 已实现；S8/S9 bounded projection 必须零 config delta；其它 forbidden changes hit count 0 |
| SEC-011 | video handle 重放/内存放大 | >=128 次合法不同/重复 Range；另测跨 WebView/context/session/restart、30min/5min expiry、release、2-read/64MiB in-flight | >=128 次仍有效；TTL/release/restart/binding mismatch 撤销；2 handles/2 concurrent/64MiB 保持；no CORS/fetch/oracle；S6A 行为不变 |

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

## 6B. S7 测试先行门禁与当前 evidence

| Slice/Layer | 必须先失败的测试 | GREEN 必须证明 |
|---|---|---|
| S7F Host canonical conformance | 当前 Host video size/digest 与 Contracts canonical 不同，box audit 找不到 `moov`/track/keyframe | exact raw 1,642 bytes + `96ea070c...77dd5`、front moov、H.264/16×16/0.12s/3 frames/keyframe；completed manifest 一致；GET/HEAD/200/206/416；strict-local/default-off |
| S7A private schema/client | video private schema、3 commands 与 typed TS client 不存在 | exact identity-only payload/result/error；无 bytes/base64/digest/href/path/name/token；image schema/client unchanged |
| S7A SQLCipher authority | ready-video inspect/range reader 不存在 | foreign/not-ready/expired/wrong kind/MIME/size/digest/box/sample fail closed；open + first protocol full validation；每 request authority/BLOB length；no migration |
| S7A registry/protocol | separate multi-request handle/protocol 不存在 | 256-bit/43-char、30min absolute/5min idle、2/WebView/1/artifact/2 reads/64MiB；GET/HEAD 200、single range 206、invalid/multi/unsat 416；no CORS/redirect/query/body/fetch/oracle；release/restart |
| S7A-REPAIR lifecycle | historical request 65 返回 404，WebView metadata 最终 `MEDIA_ERR_SRC_NOT_SUPPORTED(4)` | 无累计 request-count 撤销；同一 handle >=128 legal Range GREEN；real WebView 76/76 partial、metadata/playback/seek PASS、404=0；TTL/release/restart/binding limits 保持 |
| S7A native save/config | video save command/media-src 不存在 | explicit ready-video intent、`.mp4`、dialog/overwrite、0600 same-dir temp、chunk digest/fsync/atomic replace、content-free result；only exact `media-src 'self' yijie-artifact-video:`；deps/capability/lockfile unchanged |
| S7B component | ready video renderer 不存在 | native controls/preload metadata/no autoplay、loading/error/expired/retry/seek、duplicate/stale、pause-clear-load-release、save outcomes、keyboard/focus/reduced-motion/axe、DOM/snapshot leak=0；non-ready/non-video stays generic |

执行顺序 S7F -> S7A -> S7A-REPAIR -> S7B 已完成并分别形成独立 PASS。historical RED 与当前 GREEN 均保留在 08；
这些证据不并入 G3，也不代表 production vertical/G4。

## 6C. S8 测试先行门禁

| Slice/Layer | 必须先失败的测试 | GREEN 必须证明 |
|---|---|---|
| S8A private schema/client | file private schema、2 commands 与 typed client 不存在 | closed <=4,096-byte identity-only request；exact read/save commands；closed text/JSON/CSV projection + content-free save；无 path/name/size/digest/href/token/bytes/base64/raw error |
| S8A SQLCipher authority | ready-file bounded reader/save authority 不存在 | open/save 双次 owner/tenant/session/turn/artifact/state/expiry/kind/MIME/size/BLOB/digest/revision/format 校验；drift fail closed；无 migration |
| S8A UTF/caps/parser | control/bidi、CSV quotes/formula、JSON depth/node 与 truncation 尚无实现 | source<=1,048,576B；projection<=262,144B；response<=524,288B；2,000 lines/8,192B line；CSV 200×50/4,096B cell；JSON depth32/nodes20,000；UTF-8/BOM/newline；拒绝 C0/DEL/C1（TAB/LF/CR 除外）及 `U+061C`,`U+200E-U+200F`,`U+202A-U+202E`,`U+2066-U+2069`；不拆 scalar/cell |
| S8A concurrency/config | file preview concurrency/timeout 与 config negative 不存在 | <=2 preview/WebView、<=2,097,152B source in-flight、same-identity single-flight、10s timeout；无 URL/handle/protocol/CSP/capability/plugin/dependency；S6/S7 exact behavior unchanged |
| S8A native save | five-MIME file save 与 residue verifier 不存在 | explicit intent；ready-file `1..67,108,864B`，与 1MiB preview eligibility 独立；`.txt/.csv/.json/.pdf/.xlsx`；plain/CSV UTF-8 no-NUL、JSON parse；复用 Pattern §9.8 exact bounded PDF preflight（含 expanded visits<=4,096/bytes<=32MiB/form depth<=16/page-tree depth<=64）与 XLSX OOXML validator；dialog前后双验；cancel/mismatch/symlink/nonregular；0600 same-dir temp/chunk digest/fsync/atomic replace；exact `.yijie-artifact-file-save-v1-<media>-<epoch>-<22-char base64url>.tmp` prior-epoch/current-uid/mode/nlink/size/format cleanup；content-free result；attachment/S6/S7 behavior unchanged |
| S8B component（wait） | ready-file renderer/search 尚无实现 | 仅 S8A immutable PASS 与单独授权后：plain/JSON text nodes、CSV cell nodes、PDF/XLSX fallback、truncation、literal query<=128 scalars/<=100 hits、stale/clear/save/axe；no v-html/link/formula/network；authorized-content lifecycle + leak scans |

S8A 使用 current-v3-only Desktop-private fixtures；Contracts canonical CSV 与 Host strict-local CSV 都是合法 synthetic，
但 bytes 不同，不得混称 byte-equal canonical。plain/JSON/PDF/XLSX 由 Desktop-private injection/unit fixtures 覆盖，
不修改 Host/Contracts。S8B 必须等待 S8A immutable PASS 和单独授权。Markdown 继续 BLOCKED；若本期要求它，先重开
G2/G2A 与完整 contract/downstream pin 流程。

S8A/S8B 后续已分别在独立授权下形成 PASS；本节保留其测试先行要求与证据口径，不把 component PASS 冒充
production page/runtime visual。Markdown/AC-005 仍为 PARTIAL。

## 6D. S9 测试先行门禁

| Slice/Layer | 必须先失败的测试 | GREEN 必须证明 |
|---|---|---|
| S9A consumer conformance repair | 当前 Rust adapter 错误拒绝 200 个中文 scalar title、合法 RFC3339 offset、重复 section IDs、重复 table column keys 与 chart labels/values 不等长；这些 fixture 均被 immutable Ajv schema 接受 | string maxLength 按 Unicode scalar；合法 offset 接受；移除未契约化 uniqueness/alignment 拒绝；unknown required/closed invalid 仍拒绝；public schema/pin/fixture/Host 不变 |
| S9A private schema/client | report private schema、2 commands 与 typed client 不存在 | closed <=4,096-byte identity-only request；exact read/save commands；closed projection/content-free save；无 raw JSON/path/name/size/digest/href/token/bytes/base64/raw error |
| S9A SQLCipher/schema authority | ready-report bounded reader/save authority 不存在 | preview/save 双次 owner/tenant/session/turn/artifact/state/expiry/kind/exact MIME/size/BLOB/digest/revision/full-schema 校验；drift fail closed；无 migration |
| S9A caps/projection | typed report projection/caps/unknown omission 不存在 | source 1..4,194,304B；projection<=524,288B；response<=1,048,576B；depth<=12/nodes<=100,000/sections<=64；text/metrics/table/chart caps精确；CRLF/control/bidi可见投影；unknown optional 仅 unsupported marker、unknown required fail closed |
| S9A concurrency/config | report operation limits/config negative 不存在 | <=2 preview/WebView、<=8,388,608B source in-flight、same-identity single-flight、10s timeout；无 URL/handle/protocol/CSP/capability/plugin/dependency；S6-S8 behavior unchanged |
| S9A canonical save | report save/residue verifier 不存在 | explicit intent；validated ready report 1..67,108,864B，与 4MiB preview 独立；exact `.json`；dialog 前后双验；cancel/mismatch/symlink/nonregular；0600 same-dir temp/chunk digest/fsync/atomic replace；exact `.yijie-artifact-report-save-v1-json-<epoch>-<22-char base64url>.tmp` prior-epoch/current-uid/mode/nlink/size/full-schema cleanup；content-free result；无 derived export |
| S9B-D dependency/lock | active package/lock 无 ECharts，theme/card/adapter/bundle checker 不存在 | exact `echarts@6.1.0` + only zrender 6.1.0/tslib 2.3.0；integrity/license/NOTICE exact；root/full/vue-echarts/dynamic/CDN/install-script/额外 package 0；只有 core + Bar/Line/Pie + Grid/Tooltip/Aria + Canvas value imports；`scripts/check-feat128-s9b-d-dependencies.mjs` 与同名 test；JS baseline `655731/206580` raw/gzip-9，delta<=`716800/225280`，final<=`1372531/431860` 由 `scripts/check-feat128-s9b-d-bundle.mjs` 与同名 test 执行 |
| S9B-D theme/closed adapter | semantic chart tokens/theme/closed mapper/card 不存在 | token 仅 `--yj-color-chart-series-1..8` + exact light/dark palette + missing-token fail closed；bar/line<=64 labels/8 series/512 points；pie one aligned non-negative/non-zero series<=32 labels；mismatch/empty/nonfinite/oversize complete table fallback；pure helper 按 ordinal 选前 4 eligible charts/<=2048 points，不用 global/mount/async-order counter；no EChartsOption prop/output |
| S9B-D chart card/lifecycle | one-instance Canvas boundary 不存在 | animation=false/richText confined tooltip/ARIA/decal/HTML legend/visible table；init/update/resize/theme/error/unmount `clear->dispose->disconnect`；exact-key/serializable/no-function/no-URL/no-formatter assertions，不 snapshot projection/model/option values；axe/reduced-motion/no network/storage/log |
| S9B-D visual/bundle | no `tests/visual/feat-128-s9b-d/` harness | exact loopback Vite command启动后执行 full-known/fallback/error × light/dark × 1180×760/720 narrow/200% zoom；no page horizontal scroll/overlap，table local scroll、focus、tooltip confinement、theme re-init；不冒充 happy-dom/axe 或 production page/S10 |
| S9B-R renderer | report component/Shell/List client 透传不存在 | 仅 D immutable PASS + 单独授权后：report+ready explicit open；all known sections/ordinal identity/unknown fixed marker/truncation；unit/source/time range 显示“报告未提供”；chart isolated fallback/table authority；duplicate/stale/clear/dispose顺序；canonical save；keyboard/focus/aria/axe/open canary/close zero-hit/no raw/path/digest/href/token/requestId/error/log/snapshot |

S9A fixture authority 使用 immutable `report-document-v1.schema.json` 与 canonical valid/unknown optional/unknown required/
injection fixtures；Desktop-private differential fixtures只能补 consumer conformance，不得修改或冒充 Contracts canonical。
Host synthetic report 与 Contracts canonical bytes 不同但都必须 schema-valid。S9A、S9B-D、checker repair 与 S9B-R
后续均已独立 PASS；本节保留 readiness/RED 口径，production Chat/Tauri vertical 仍 `NOT RUN`。

## 6E. S10 测试先行门禁

| Slice/Layer | EXPECTED RED | GREEN/stop |
|---|---|---|
| S10A exact profile | as-is real Host 拒绝 synthetic+fake；Desktop sidecar 不映射 v3/synthetic flags | exact S10+FEAT126 local conjunction start session/turn and v3 four-kind GET/ACK；所有不完整/大小写/key/provider/non-loopback 组合 fail before listen/spool/child；fresh source/binary digest、0700 root、20/30/180/10s deadlines、zero child/listener/WAL/spool/temp；否则 STOP |
| S10B v3 decoder/cursor | production 只开 v2；Artifact apply 与 cursor 独立 | single v3 common order；ordinary reducer parity；started/progress/failed+cursor transaction；completed ready+ACK intent+cursor crash points；duplicate/gap/stream restart/identity/terminal fail closed；flag-off v2 equality |
| S10B private event | channel/schema 不存在 | exact content-free closed shape；main-WebView/current context/session subscription；sequence monotonic、queue 64、gap/overflow coalesced resync、restart no replay；DOM/log/schema source无 metadata/body/digest/path/token/error |
| S10C history/store/page | ChatClient/Store 使用 v2；ArtifactStore无 authority reset；Page未挂List | subscribe-first/buffer/control+v3 history/second resync/replay；separate v3 cursor；authority tuple+epoch/reset；empty-text turn；four typed clients；stale/switch/logout/delete zero projection；no direct invoke/wire parse |
| S10D vertical | S7 seeded shell/S9 Vite fake 不能证明 production | fresh exact Host + real Tauri production ChatPage；四 kind lifecycle/ACK/history/pagination/reload/restart/mixed failure/TTL/delete；18+ visual/a11y matrix；manual native save若不可安全自动化则 NOT RUN |
| S10E security/perf | 无真实 12-item/burst/boundary/canary/per-process baseline | unauthorized context/WebView/session与 digest/MIME/size/content mismatch；12 items、100/s×10s、20/64MiB、file/report caps；3 warmup+30 samples，p50/p95；started p95<300ms/hard-stop>=1000，render<=10Hz/hard-stop>20，no >200ms long task，CLS<=0.1，memory target<=2.5x/hard-stop>3x，close residual<=64MiB |

S10A exact focused commands、allowlist 与 process runner 在 07 §23；B-E 均等待前序 immutable PASS 和单独授权。
任何 public contract/pin/fixture、migration、dependency/plugin/capability/CSP/external origin、secret/provider/non-loopback、
monotonic weakening 或 content leakage 立即失败。

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
| announced visible p95 | 3 warmup + 30 measured samples/kind | 未建立 | <300ms | >=1000ms |
| progress render rate | 100 events/sec burst | 未建立 | <=10Hz/component | >20Hz sustained |
| long task/layout | 12 mixed artifacts | 未建立 | no task >50ms target；CLS<=0.1 | any task >200ms |
| preview memory | 20MiB image / 64MiB video | 未建立 | <=2.5x bytes target | >3x or crash/OOM |
| transfer integrity | range/full content | 未建立 | 100% digest match | any silent mismatch |
| cleanup | 128MiB turn | 未建立 | content inaccessible after completion | any residual readable content |
| process residual RSS | Desktop+WebContent+Host, close+30s | 未建立 | <=64MiB aggregate over baseline | >64MiB after cleanup |

这些阈值、样本和 hard-stop 已由 S10 readiness Owner 冻结；未测结果不能写成 PASS。

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
| report document v1 | `yijie-contracts/jsonschema/report/report-document-v1.schema.json` + canonical valid/unknown optional/unknown required/injection fixtures | public synthetic | 虚构指标/日期/来源，无店铺数据；exact MIME `application/vnd.yijie.report+json;version=1`；Host synthetic 为独立 schema-valid bytes；PDF/Markdown/image derived export 延期 | Contracts/Host + S9A/S9B-D/S9B-R PASS；production vertical NOT RUN |
| canonical video resource | `yijie-contracts/tests/fixtures/agent/resources-v3/synthetic-video-16x16.mp4.base64` | public synthetic | generated three identical 16×16 frames；raw 1,642 bytes；no external footage/business data | Contracts/Host S7F/Desktop S7A/S7B PASS |
| file fixture corpus | Contracts `synthetic-data.csv` + Host distinct strict-local CSV + Desktop-private MIME matrix | public synthetic | 两个 CSV 均合法但非 byte-equal；其余只用 local safe fixtures | S8A/S8B PASS；不得修改 immutable source |
| media boundary corpus | implemented S3/S4/S6/S7/S8 testdata + future report UI corpus | public synthetic | generated headers/containers/corruption | image/video/file boundary/renderers PASS；report pending |
| canary leak corpus | implemented native/media/file checks + planned report projection/DOM scanner | restricted synthetic marker only | path/token/body/raw report/unknown payload + authorized preview marker，不含真实 secret | unauthorized/raw zero-hit；authorized bounded marker open-only/close-zero |
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
| S10A Host profile | yijie-agent-host | `go test ./internal/app ./cmd/desktop-host && YIJIE_RUN_FEAT128_S10_PROFILE_INTEGRATION=1 go test ./internal/integration -run '^TestFEAT128S10ExactLocalProfile$' -count=1 -v && go test ./...` | loopback 18080/18082 free；no key/provider | 3-10 min |
| S10A Desktop sidecar | yijie-desktop | `cargo fmt --manifest-path src-tauri/Cargo.toml -- --check && cargo test --manifest-path src-tauri/Cargo.toml chat::sidecar::tests && cargo test --manifest-path src-tauri/Cargo.toml --features feat128-s10-runtime chat::sidecar::tests && cargo clippy --manifest-path src-tauri/Cargo.toml --all-targets --all-features -- -D warnings` | Rust toolchain；no child secrets | 3-10 min |
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
| 安全/数据 Owner | 段成威 | S3/S4/S5 G3 PASS；S6-S9B-R separate PASS | 2026-08-22 |
| Product/Technical/Security/Data Owner | 段成威 | S10-READINESS `READY FOR S10A-LOCAL-PROFILE ONLY`；S10B-E WAIT/NOT RUN | 2026-08-22 |

Contracts、pin conformance、S3/S4/S5 与独立 S6-S9B-R 命令已实际执行并记录于 08；S10-READINESS 只是
docs evidence，S10A-E 尚未实现，不能因 Pattern Accepted 或 Owner readiness 预记 PASS。
