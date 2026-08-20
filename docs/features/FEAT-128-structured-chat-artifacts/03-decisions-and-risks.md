# FEAT-128 决策与风险

## 1. 已确认决策

| ID | 决策 | 理由 | 状态 |
|---|---|---|---|
| DEC-128-001 | 本地优先，不购买云资源，不部署生产 | 用户明确要求 | Accepted 2026-08-20 |
| DEC-128-002 | 目标 UI 覆盖图片、视频、文件、数据分析报告，并支持流式阶段 | 用户明确要求 | Accepted 2026-08-20 |
| DEC-128-003 | 使用现有 Desktop Design System、Naive UI、YjIcon、ECharts/token | 用户明确要求且仓库规范强制 | Accepted 2026-08-20 |
| DEC-128-004 | 不把“多模态输入”当作“媒体输出生成已可用” | 当前 MiniMax catalog 与 Host 实现只证明输入和文本输出 | Accepted engineering constraint |

## 2. 推荐候选决策

下列选择最初作为推荐候选，直接决策回复见 2A；本轮 G2 closure 已按 2B 的 Owner 明确指令完成冻结。G2 只授权 Contracts S1/S2，不代表 G2A、下游实现或生产批准。

| ID | 推荐方案 | 备选 | 推荐理由 | G2 批准点 |
|---|---|---|---|---|
| DEC-128-005 | 新增 v3 event/history/resource surface | 原地扩充 v2 closed union | 保持 v1/v2 严格 consumer 兼容 | Contract/Consumer Owner |
| DEC-128-006 | Desktop SQLCipher 为长期 authority，Host 仅短期 staging | Host 长期保存，或 event 携带 base64 | 延续本地加密边界，避免大事件与第二业务库 | Data/Security Owner |
| DEC-128-007 | report 使用 closed versioned JSON document | raw HTML/iframe 或任意 ECharts option | 可访问、可测试、无脚本/远程资源攻击面 | Product/Client/Security Owner |
| DEC-128-008 | WebView 仅接 bounded blob preview；超限降级为保存 | 自定义 asset protocol 或直接本地路径 | 首期减少 Tauri capability 和路径暴露 | Client/Security Owner |
| DEC-128-009 | native save dialog + streaming temp file + atomic replace | 浏览器 download、直接 workspace 写入 | 符合 macOS 预期并绑定明确用户意图 | Client/Security Owner |
| DEC-128-010 | local-only synthetic producer 为无云验收入口，默认关闭 | 把 fixture 混入普通 provider | 可重复验证且不误报真实模型能力 | Technical/Reviewer |
| DEC-128-011 | Artifact 默认保留七天，与 FEAT-127 对齐 | 会话永久保留或应用退出即删 | 当前本地数据治理一致，限制 confidential 残留 | Data Owner |

## 2A. G2 Owner Decision Capture（2026-08-20）

> 决策人按 `feature.yaml` 登记为段成威（Feature Owner）；本节依据用户明确授权的直接回复整理。Codex 仅代拟和记录，不把自身描述为独立人工 Reviewer。`Modify` 的完整替代文本已在 2B closure 中冻结。

| ID | 结论 | 完整决策文本 | 理由 | 影响 | 决策人 | 日期 |
|---|---|---|---|---|---|---|
| DEC-128-005 | Approve | 采用显式 v3 event/resource/ack surface，并使用 `event_schema_version=3` 协商；游标参数沿用权威 v1/v2 的 `after`、`stream_id` 与 `Last-Event-ID`。Artifact 只在 v3 surface 发出。v1/v2 endpoint、wire、事件集合、cursor、replay、终态和字节语义保持不变；Desktop durable history/resource 仍是 private surface，本期不新增 Host public history endpoint。 | 隔离 semantic change，保护严格 v1/v2 consumer 兼容性并避免发明第二条 history API。 | S1 必须形成 v3 event、content/poster、ack source 与双基线 equality；G2A 才要求真实生成、不可变引用和 consumer pin。 | 段成威 | 2026-08-20 |
| DEC-128-006 | Modify | Desktop SQLCipher 是 Artifact 唯一长期 authority。Host staging 使用 app-private encrypted spool：文件权限 `0600`、每进程临时密钥且密钥不落盘，Host 重启先清除不可恢复旧 spool；不使用 1 GiB 进程内大对象或 owner-only plaintext。冻结每 session 256 MiB、全局 1 GiB、`staged_at + 24h` TTL。Desktop 校验 scope/size/MIME/magic/SHA-256 并提交 SQLCipher 后，调用 owner/session-scoped 幂等 ACK；ACK、TTL 或 Host 重启触发清理，不驱逐读取中的内容。 | 冻结存储介质、容量、TTL、ack、重启和明文边界。 | S1 定义 ACK operation；Host cleanup transport receipt 与 Desktop 私有 retention cleanup receipt 分开，后者留在 S4 private data design。 | 段成威 | 2026-08-20 |
| DEC-128-007 | Modify | `report-document-v1` 根对象 closed；每个 section envelope 显式包含 `id`、`type`、`required` 和 `payload`。已知 `summary|metrics|paragraph|table|chart|callout` payload 使用 strict safe schema；unknown type 只有 `required=false` 时可由兼容层保留为不渲染的 opaque JSON 并显示 `unsupported`，`required=true` 或已知 payload violation 拒绝整份文档。canonical MIME 为 `application/vnd.yijie.report+json;version=1`；禁止 HTML、script、iframe、URL、远程资源和任意 ECharts option；PDF/Markdown 仅为未来 derived export。 | 让 closed root 与 unknown optional fail-soft 同时可实现、可测试。 | S1 提供 known/unknown requiredness fixtures；Desktop 必须 two-stage decode 且不遍历或执行 unknown payload。 | 段成威 | 2026-08-20 |
| DEC-128-008 | Approve | WebView 只消费 native bridge 提供的 bounded blob/object preview；候选上限为 image 20 MiB、video/file/report 64 MiB，单轮最多 12 项或 128 MiB，超限或不支持时只显示安全 metadata 并保留 native save。WebView 不持有 Host bearer、绝对路径或 provider URL；object URL/preview handle 在关闭、卸载、替换和 session 切换时撤销。 | 有界预览和保存降级减少 capability、路径暴露和 OOM 风险；具体上限和生命周期作为批准边界记录。 | 需要 native fetch 校验、内存/边界测试、CSP 最小变更和 object URL 释放证据；不新增自定义 asset protocol。 | 段成威 | 2026-08-20 |
| DEC-128-009 | Modify | 用户显式触发 native save dialog；使用服务端验证的 safe filename，在目标目录创建同目录 streaming temporary file，禁止 symlink/no-follow 越界，覆盖必须由用户明确确认，成功后执行 atomic replace。保存失败时删除临时文件但保留 SQLCipher authority 副本；仅允许精确 private save capability，禁止通用 filesystem 或 shell capability。 | 原句未确认 safe filename、symlink/overwrite 和 capability 最小权限，存在保存越界风险。 | 需要 Tauri command/capability、安全测试和失败恢复证据；不得使用浏览器 download 或直接 workspace 写入。 | 段成威 | 2026-08-20 |
| DEC-128-010 | Approve | local-only synthetic producer 作为无云验收入口，仅在 `YIJIE_ENV=local`、固定 test manifest 和独立 synthetic flag 同时满足时可启动；它可以为 image/video/file/report 四类发出固定 fixture，默认关闭且不得与真实 provider 同开。每个 Artifact 必须携带并持久化 `provenance=synthetic`；非 local、manifest 不匹配或 capability 不明确时 fail closed，不调用 MiniMax 或任何付费 API。 | 提供完整、可重复、零费用的 walking skeleton，同时把 synthetic 与真实 producer authority 分层。 | 四类 synthetic contract fixtures 属 S1；真实 `provider|tool` producer 仍只由 S12 activation gate 管理。 | 段成威 | 2026-08-20 |
| DEC-128-011 | Modify | Desktop 成功校验并提交 SQLCipher 时记录 `local_committed_at`，并计算 `expires_at = local_committed_at + 168h`；`now >= expires_at` 时进入 `expired`。到期清除 SQLCipher content、preview/object URL、cache 及可清理的 WAL/checkpoint 残留，并写入 Desktop 私有、幂等的 cleanup receipt；历史只保留最小安全 metadata、位置和 `expired`。Host staging 使用独立 `staged_at + 24h` TTL。会话删除 cleanup saga 失败必须可重试且不得报告物理删除完成。 | 冻结起算点、Host/Desktop 两个时钟和 receipt authority。 | retention migration/reopen/forensic 属 S4，不作为 G2 前的实现证据；G2A 前只需 public contract source 与计划一致。 | 段成威 | 2026-08-20 |

Provider gate：`Approve / Keep closed`。真实 MiniMax image、video、file、report producer 按 kind 独立关闭，不调用真实或付费 API，不发出 `provenance=provider/tool` Artifact。任何启用都必须另行固定 capability/API/model、费用与网络授权、格式/容量/失败/取消/合规语义、Host/Desktop conformance 及质量/延迟/成本 Eval，并取得单独 Owner 批准。

取消边界：当前 candidate 只复用既有 turn interrupt；没有 Artifact-specific cancel operation。turn interrupt 将尚未终态项发为 `item.artifact.failed(error_code=turn_interrupted)`，Desktop 显示 `cancelled`。

poster/ACK 边界：`poster_href` 只允许指向同 session 的 `/poster` 相对资源；content 与 poster 均由 owner-only GET/HEAD 读取。ACK 是独立幂等 POST，校验 artifact、session、size、digest 和 Desktop commit identity，成功只表示 Host 可提前清理 staging，不代表 Desktop retention cleanup 完成。

Generator/adapter 边界：OpenAPI、Protobuf 和 TypeScript JSON Schema 继续使用仓库锁定 generator。当前没有获批的 Go/Rust JSON Schema generator；G2 批准沿用显式 adapter 例外方案。Host/Desktop 的 pin-only commits 已记录 Owner、同源 schema/fixture conformance、最晚 2026-11-20 或 G5（以较早者为准）的到期日，以及“接入获批 generator 或生产前重新批准”的移除条件。S3/S4 实现现已分别固定在 Host `4017785adb08e1114781d3d844e9a10a683fa933` 与 Desktop `09220dd8319cfb8ec0c4d1531514bb5169107983`；生产前仍须移除或重新批准例外。

## 2B. G2 Owner Sign-off（2026-08-20）

用户在本轮明确指令执行 G2 closure rewrite，并要求分别记录 Product、Technical、Security/Data Owner 的 `G2 APPROVED`。Codex 只负责把该 Owner 指令和审查结果写入文档；这不是 Codex 自我批准或独立人工 Review。

| Review | Owner | 结论 | 批准范围 | 不包含 |
|---|---|---|---|---|
| Product/Design | 段成威 | APPROVED | 四类 Artifact、流式状态、本地 synthetic、Pattern 1.0.0 Accepted | 真实 provider、生产 UX 验收 |
| Technical/Contracts | 段成威 | APPROVED | v3 event/content/poster/ack、`after` cursor、report envelope、S1/S2 顺序 | Host/Desktop 业务实现、tag/push |
| Security/Data | 段成威 | APPROVED | encrypted spool、owner/session scope、容量/TTL、Desktop commit retention clock、bounded preview/save | Tauri/CSP/DB 实际变更、生产数据 |
| Test/Reviewer | 段成威 | APPROVED FOR G2 | 06 的 synthetic contract、failure、安全、兼容和双 baseline 计划 | G2A/G4 测试结果或“独立人工评审”声明 |

G2 结论：`APPROVED`，只授权 `yijie-contracts` S1/S2。真实 source/generate/lint/test/breaking/semantic review/immutable commit 与下游 exact pin 是 G2A 证据，不是 G2 前置实现证据。

## 3. Provider activation gate

每个真实 kind 单独通过以下条件后才能启用：

1. 权威 API/tool/Runtime item 和 provider capability 有固定版本证据。
2. 用户明确授权可能产生的模型费用与外部网络访问。
3. 内容类型、最大大小、失败、取消、重试、审核和合规语义已冻结。
4. Host producer conformance、Desktop consumer conformance 和真实 local integration 通过。
5. 质量/延迟/成本 Eval 有固定 dataset 和阈值。

当前 image/video/file/report 均未通过完整 gate。固定 Runtime 的 `imageGeneration` item 只满足第 1 项的一部分，MiniMax capability 仍未证明。

## 4. 风险登记

| Risk | 触发条件 | 影响 | 预防控制 | 检测 | 恢复/回滚 | Owner |
|---|---|---|---|---|---|---|
| RSK-128-001 旧 consumer 被未知事件击穿 | 新 variant 发到 v1/v2 | 对话流中断 | 显式 v3 协商、v1/v2 wire equality | compatibility + strict consumer test | 关闭 v3 producer，回退到文本 | Contracts Owner |
| RSK-128-002 confidential 内容泄漏 | bytes/path/token 进入 event/log/DOM | 数据泄漏 | opaque ref、native fetch、日志脱敏、no-store | canary fixture + log/DOM scan | 停止 producer，删除 staging/cache，轮换 token | Security Owner |
| RSK-128-003 媒体炸弹/OOM | 伪装 MIME、巨大尺寸、压缩/解码放大 | crash/卡死 | magic、length、pixel/duration/row limits、lazy decode | adversarial fixture、memory threshold | 终止 decode，降级 metadata + save | Client Owner |
| RSK-128-004 存储不一致 | Host ready 但 Desktop 写入失败 | UI 显示不可用/丢失结果 | staged transfer、digest、原子 commit、ack 后清理 | mismatch metric/log code | 重试 transfer；不可恢复标 failed | Runtime/Client Owner |
| RSK-128-005 保存越界或覆盖错误 | 恶意名称、symlink、已有目标 | 任意文件写/数据覆盖 | native dialog、safe name、no-follow、明确 overwrite、atomic replace | security tests | 删除 temp，保留 authority copy | Client/Security Owner |
| RSK-128-006 raw report 内容执行 | HTML/script/remote URL 进入 renderer | XSS/数据外传 | closed report schema、文本转义、无 iframe/HTML | schema/adversarial UI tests | 拒绝 section，继续已知 section | Security Owner |
| RSK-128-007 伪造进度 | UI 显示无依据百分比 | 误导用户 | percent optional、只显示 provider stage | event/UI conformance | 回退不确定进度文案 | Product Owner |
| RSK-128-008 synthetic 被误当真实 | fixture 在普通模式启用 | 验收/用户信任失真 | exact local env gate、明显 synthetic source、默认 off | startup/config tests | 关闭 profile、清理 fixture session | Technical Owner |
| RSK-128-009 provider 费用失控 | 自动调用媒体生成 API | 不可控成本 | 默认 capability off、显式费用批准、per-turn limits | cost counter/budget stop | kill switch、禁止新请求 | Product/Release Owner |
| RSK-128-010 retention 清理失败 | DB/WAL/cache 或 Host staging 残留 | confidential 长期残留 | TTL job、session cleanup saga、WAL/cache verification | reopen/forensic test | retry cleanup、阻断关闭/发布 | Data Owner |

## 5. 不需要新 ADR 的前提

如果实现保持“v3 expand、Host 临时 staging、Desktop 本地 authority、无云资源、无新跨仓职责”，现有职责方向不变，可在本 Feature 决策记录内评审。若选择 Host/云端长期 Artifact 仓库、自定义共享 URL、公共分享或改变 Runtime 核心协议，必须先建立新 ADR 并取得明确批准。

## 6. 实现前批准清单

- DEC-128-005..011、ACK/poster/cursor/cancel、report compatibility、synthetic/real 分层与 Provider gate 已完成 G2 Owner 冻结。
- Tauri native save command、CSP `media-src blob:` 与 capability 的设计方向已批准；G2A 已通过，实际 Desktop diff 仍须在 S4/S7 单独复核。
- Contracts v3 source、基线、generator/adapter、unknown kind/section 行为和 consumer 顺序已完成 G2 设计评审；S1/S2 真实生成、检查、双 breaking 与不可变 commit 已通过。
- Desktop SQLCipher v8 migration、64 MiB 单 Artifact 上限、七天 retention 起算与恢复边界已在 S4 实现并通过迁移/reopen/TTL/delete 验证；native save/CSP 仍属于后续 S6-S8 安全切片。
- 真实 MiniMax 调用保持关闭；如需启用，另行取得费用和 provider activation 批准。

## 7. 当前 Gate 结论

- G0：PASS，Feature ID、Owner、本地边界和初始 Git 状态已记录。
- G1：PASS，场景、AC、受影响仓库、最高 contract impact 和主要风险已识别。
- G2：`PASS`，Product/Design、Technical/Contracts、Security/Data 与测试计划已由 Owner 明确批准；只允许进入 Contracts S1/S2。
- G2A：`PASS`，Contracts `ea48fe190e18afba728712d1e2cc79cda57f581b`、Host pin `dea84d0768ebc017b7ee5faedab7f9a49ce74875` 与 Desktop pin `96094419d963745529ed0fa246919089e659f20d` 已满足真实 generate、双 breaking、semantic/consumer review 与不可变 pin 条件。批准依据是用户本轮给出的条件授权与实际证据，不声称 Codex 是独立人工 Reviewer。
- G3：对 S3/S4 原子切片已通过；G4-G6 仍未通过。Host/Desktop master/synthetic flags 默认关闭，真实 provider 继续关闭。
