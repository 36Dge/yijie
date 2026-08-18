# FEAT-127 决策与风险

## 1. 已采用决策

| ID | 决策 | 理由 | 状态 |
|---|---|---|---|
| DEC-127-001 | 本地优先，零云资源、零生产激活 | 用户明确说明当前无部署和云资源计划 | Accepted 2026-08-17 |
| DEC-127-002 | Host 新增并行 v2 multimodal turn，v1 保持逐字节兼容 | 避免修改已支持的 text-only v1 | Accepted for local design |
| DEC-127-003 | SQLCipher 保存原始 BLOB、解析文本和普通 chunk 表 | 延续 ADR-0013/0014 confidential local authority；不引入 pgvector/FTS | Accepted for local design |
| DEC-127-004 | 到期后保留 metadata，清除 BLOB 与 chunk | 同时满足“跟随会话加载”和“七天不再进入上下文” | Accepted for local design |
| DEC-127-005 | 图片以 data URL 通过 Host 映射为 Runtime image UserInput | 不传本地路径，不创建持久 plaintext cache | Accepted for local design |
| DEC-127-006 | 文档在 Desktop 解析、分块、相关性选取后变成 Runtime text input | Host 保持薄适配层，Knowledge/pgvector 不进入本期 | Accepted for local design |
| DEC-127-007 | 允许 attachment-only message | 多模态容器不应强制存在文本；空消息仍拒绝 | Accepted for local design |
| DEC-127-008 | 新 FEAT-127 Pattern 覆盖附件冲突段落 | 不篡改 FEAT-126 的历史范围决定 | Accepted for local design |
| DEC-127-009 | 单项 10 MiB、每消息 10 项、图片字节合计 10 MiB | 满足需求并控制 16 MiB Runtime frame 与内存峰值 | Accepted for local design |
| DEC-127-010 | native 导入进度使用 operation 级聚合事件 | 全局 Tauri event 只暴露 opaque IDs、sequence、stage、item count 和 issue，避免广播文件名、路径、正文、digest、data URL 或完整附件 metadata | Accepted for local design |
| DEC-127-011 | 本地 G3 使用“自动证据替代/可访问性延期”的临时 Gate 例外 | 用户在 2026-08-19 明确批准；替代项已有针对性自动回归，当前无分发或生产计划，同时保留人工结果 `PARTIAL` 与可访问性 `NOT RUN` 的真实状态 | Accepted 2026-08-19 as `EXC-127-001` |
| DEC-127-012 | Desktop 暂用受锁定 conformance 约束的手写 Rust Agent Host v2 request adapter | 当前没有批准的 Rust OpenAPI generator；完整源摘要、canonical fixture、schema validator 和 Rust serialization test 共同 fail closed，且设置期限与移除触发 | Accepted 2026-08-19 as `EXC-127-002` |

这些本地工程选择来自用户“模型补足高质量交互”的授权范围。Contracts/consumer 对当前本地 semantic candidate 的 review 已批准，但不代表最终 merge、release version/tag 或生产批准。

## 2. 格式策略

允许图片：JPEG、PNG、WebP、GIF。允许文档：PDF、TXT、Markdown、CSV、JSON、YAML、XML、HTML、RTF、DOCX、XLSX、PPTX。OOXML 需校验容器内 canonical entries、条目数量、解压总量和 compression ratio；legacy DOC、宏扩展名与 archive 一律拒绝。

解析器无法可靠提取文本时返回 terminal error，不把乱码或原始 binary 拼入 prompt。HEIC/HEIF 暂不进入首期，因为固定 Runtime image decoder 的兼容证据尚未建立。

## 3. 风险登记

| Risk | 触发 | 影响 | 预防/检测 | 恢复 | Owner |
|---|---|---|---|---|---|
| RSK-127-001 parser bomb | 恶意 PDF/OOXML 高压缩或深层结构 | 内存/CPU 耗尽 | 条目、解压、文本、时间和深度上限；合成 adversarial tests | 拒绝单项，保留其余草稿 | Client Team |
| RSK-127-002 MIME spoof | 扩展名与内容不符 | parser 漏洞或 active content | native magic + semantic container validation | terminal reject | Client Team |
| RSK-127-003 sensitive leak | path/name/content 进入日志或 Host store | 隐私泄漏 | Debug 只记 byte counts/IDs presence；denylist tests | 删除本地候选并修复 | Client/Host |
| RSK-127-004 partial commit | 消息写入但附件未绑定 | 历史不一致 | 单 SQLCipher transaction + FK/unique constraints | idempotent retry/forward repair | Client Team |
| RSK-127-005 expiry race | 发送和 TTL cleanup 并发 | Runtime 缺 Context | 串行 repository worker；绑定/选取同一 authority check | 明确 `attachment_expired`，保留文本 | Client Team |
| RSK-127-006 transport overflow | 多张大图 base64 膨胀 | Host/Runtime request 失败 | 图片 binary aggregate 10 MiB；JSON/frame size test | UI 要求移除部分图片 | Host/Client |
| RSK-127-007 old consumer reject | v1 响应出现新字段 | 旧版失败 | 新 v2 endpoint；旧 history `content` 保留；bundled IPC 原子升级 | 回退并停用 v2 | Contracts Owner |
| RSK-127-008 plaintext residue | parser 临时文件或 cache | 本地内容泄漏 | 解析内存/原路径读取；BLOB SQLCipher；不建 plaintext cache | cleanup + WAL truncate | Client Team |
| RSK-127-009 false AI quality claim | chunk selector 相关性差 | 回答遗漏 | deterministic fixture retrieval tests；不声称语义检索 | 提供文件名/片段标记，后续独立 Eval | Product/AI |
| RSK-127-010 dirty overlap | 覆盖 FEAT-126 composer 改动 | 回归/用户工作丢失 | 修改前后完整 diff；独立文件优先 | 手工融合，不 reset | Client Team |
| RSK-127-011 transient drop path | Tauri drag event 把路径交给 JS callback | 路径进入 state/log/DOM | 只作 command 局部参数；响应无路径；denylist tests | 移除 JS listener，改 Rust window event import | Client Team |
| RSK-127-012 PDF compatibility reduction | PDF 使用现代 xref/object stream、增量 `/Prev`、加密或复杂过滤器 | 常规查看器可打开但本地导入被拒绝 | 经典 xref、对象/流、Form 深度与展开预算的 fail-closed 预检；正反向合成测试 | 用户另存为兼容 PDF 后重新选择；未来更换隔离解析器需独立 Feature | Client Team |
| RSK-127-013 automated evidence substitution gap | Store/native 分层自动测试未覆盖真实 Desktop 窗口、系统文件选择器与重启组合中的全部集成差异 | 移除、边界或 10+1 容量问题可能在本地真实交互中晚发现 | 保留精确 Store/native tests、完整 Desktop 门禁和人工/自动证据标签；触发条件出现即撤销例外 | G3 回退 `PENDING`，在真实 Desktop 补验三项并记录 | 段成威 |
| RSK-127-014 deferred macOS accessibility | VoiceOver、真实系统 200% 缩放或 reduced motion 与 axe/CSS 等效视图不一致 | 键盘焦点、朗读、缩放布局或动效偏好缺陷可能在分发前才暴露 | 保留 axe、键盘、light/dark、等效 200% 自动证据；禁止把延期写成人工通过 | 形成可分发候选前完成真实 macOS/Tauri 手工补验；失败则修复并重跑 G3 | 段成威 |
| RSK-127-015 hand-written Rust adapter drift | Desktop adapter、readiness pin、OpenAPI 或 fixture 独立变化，或手写 DTO 被误称为 generator 产物 | 请求字段/顺序/失败语义偏离 Host，自动门禁误绿 | `747cf740...` 精确 pin；OpenAPI/fixture/adapter/readiness SHA；Redocly+Ajv；byte-identical snapshot；Rust canonical serialization；expiry/negative tests | 任一 digest/schema/generator/发行触发发生即 fail closed，移除 adapter 或重新完成 Owner/consumer review | 段成威 |

## 4. 临时 Gate 例外

| Exception | Gate / scope | 控制或替代证据 | 延期/移除触发 | 批准证据 | Owner | 有效期 | 状态 |
|---|---|---|---|---|---|---|---|
| `EXC-127-001` | 仅 FEAT-127 当前本地候选的 G3 | 附件移除后重开；10 MiB/10 MiB+1 与压缩包边界；已有 10 项时第 11 项容量保护 | VoiceOver、真实系统 200% 缩放、reduced motion | 用户在当前 Codex 任务于 2026-08-19 明确批准“自动证据替代/可访问性延期”的 Gate 例外 | 段成威 | 至 2026-11-17，或任一触发条件更早发生 | ACTIVE；G3 `PASS WITH EXCEPTION` |
| `EXC-127-002` | 当前本地候选的 G2A/G4；Desktop 手写 Rust v2 request adapter | Contracts `747cf740...`、OpenAPI `3d2f2273...`、fixture `ec464ce5...`、adapter `c6e90e0e...`、readiness `9a070251...`；结构化 schema/byte snapshot/Rust serialization/negative tests | 出现批准的 Rust generator、request schema 或任一受锁源变化，或进入 signed/release candidate 时移除或重审 | 用户在当前 Codex 任务于 2026-08-19 要求完成 Owner/consumer review 并记录 Reviewer 批准；Desktop lock 明确记录 exception owner、期限与触发 | 段成威 | 至 2026-11-17，checker 自 2026-11-18 起 fail closed；任一触发条件可更早失效 | ACTIVE；G2A `PASS WITH EXCEPTION`，纳入本地 G4 |

例外绑定的最终本地候选身份为 Contracts `747cf740f2d91e76e5c1a130e8e009f1efa821b8`、Agent Host `e2f0f5d0e7273331e7e9eaeeb82be15955e94c86` 与 Desktop `2cb4ffdd87055e5f70aafacc63479154e0c62cad`。任何相关生产逻辑、契约或受锁 adapter/readiness source 变化均按触发条件处理。

`EXC-127-001` 的自动替代不改变证据类型：上述三项仍是 `AUTOMATED ONLY`，Desktop 功能人工验收仍是 `PARTIAL`，三个可访问性手工项仍是 `NOT RUN`。两项例外都不覆盖 PR/merge、tag、supported/release-ready、签名/公证、G5/G6、真实模型质量或生产激活；G2A semantic review 与 G4 Reviewer approval 是另外完成并记录的门禁，不由例外替代。

下列任一条件发生时，`EXC-127-001` 立即失效，G3 回退为 `PENDING`，直至在当时的真实 Desktop 候选上完成受影响项目的人工补验并更新证据：

- 创建签名、公证或其他可分发 Desktop candidate。
- 进入 staging/main、release 或生产准备流程。
- 修改 composer、附件 Store、native importer、草稿恢复、拖拽、主题或可访问性生产逻辑。
- 升级 macOS、Tauri 或 WebView 基线。
- 收到附件验收、可访问性或平台兼容性问题。
- 当前日期晚于 2026-11-17。

| Follow-up | 内容 | Owner | 截止/触发 |
|---|---|---|---|
| `FEAT-127-ACCEPTANCE-EXCEPTION` | 跟踪例外有效性；触发后补做三项真实 Desktop 功能验收与 VoiceOver/真实 200% 缩放/reduced motion，并关闭或重新审批例外 | 段成威 | 2026-11-17 或任一上述触发条件，以较早者为准 |
| `FEAT-127-RUST-GENERATOR` | 跟踪 `EXC-127-002`；评估批准的 Rust OpenAPI generator，或在受锁 source/schema/发行触发时重做 adapter semantic review | 段成威 | 2026-11-17 或任一 `EXC-127-002` 触发条件，以较早者为准 |

## 5. ADR 判定

不新增跨项目高成本 ADR。数据权威与保护已由 ADR-0013/0014 冻结；本次用 forward-only v6/v7 migration 和 versioned Host operation 扩展既有方向，整体 contract impact 按持久化与重放语义归类为 `semantic`。若未来引入云对象存储、服务端解析、向量索引或跨设备同步，必须新建 ADR/feature。

## 6. 生产阻断

- 未购买或配置云资源、生产 IdP、对象存储、监控和告警。
- 没有签名/公证产物、发布 tag、生产安全评审或真实数据验证。
- 因此只能登记 `Local candidate / Production Activation Blocked`，不能声明 G5/G6 passed 或生产可用；本地范围下 G5/G6 记为 `N/A` 仅表示未进入这些阶段。
