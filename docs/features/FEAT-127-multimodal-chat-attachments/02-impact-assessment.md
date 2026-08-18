# FEAT-127 影响评估

## 1. Contract impact

`contract-impact = semantic`。

理由：公共 wire 结构采用并行 v2 operation，纯文本 v1 request 和既有 Desktop `content` 文本投影保持兼容；但本需求同时改变消息在跨进程、持久化和重放边界上的语义，包括有序内容块、附件七天 Context 资格、导入事件顺序、composer 草稿归属和 v6 无归属 ready 草稿的安全清理。按最高风险唯一分类不能仅因新增 v2 形状而标为 additive，因此归类为 `semantic`。新 request 仍按 provider-first 顺序落地，Desktop 只在 Host v2 conformance 后调用。

如果实现改为修改 v1 required 字段、让旧 history consumer 收到无法解析的新形状，或让旧数据库 reader 失败，分类必须升级为 breaking。

## 2. 真实调用链

```text
ChatComposer plus/native drop
  -> chat attachment client
  -> Tauri native import/parser/indexer
  -> SQLCipher attachment/blob/chunk staging
  -> create/submit IPC with attachment IDs
  -> Desktop repository atomically binds blocks to user message
  -> relevance selector builds bounded text context
  -> Desktop HostBridge v2 content blocks
  -> Agent Host validates and maps text/image blocks
  -> pinned Codex Runtime turn/start UserInput[]
```

历史方向：SQLCipher message/block metadata -> Desktop history IPC -> Pinia -> ChatPage。七天清理由 Desktop repository 启动/读/写 maintenance 触发。

## 3. 仓库与 Owner

| Repository | 影响 | Owner | 初始状态 |
|---|---|---|---|
| yijie | 新 FEAT-127 包 | 技术负责人 | 新包前 clean |
| yijie-contracts | 新 Host v2 turn source、fixture、generated SDK | Contracts/Agent Runtime Team | clean `98e89d8...` |
| yijie-agent-host | v2 handler、validation、Runtime mapping、tests、contract pin | Agent Runtime Team | clean `d9c770e...` |
| yijie-desktop | UI、IPC、domain、store、SQLCipher migration、parser/indexer、HostBridge | Client Team | 7 个已有 FEAT-126 dirty 文件，必须保留 |
| yijie-codex | 只读验证既有 UserInput text/image 能力 | Runtime Team | 不修改 |

API、Infra、Knowledge、Connectors、Skills、Admin 不受本地实现直接影响。Public Tasks 仍只接收 content-free reference，不接收附件内容。

## 4. 已有冲突与处理

- Accepted 通用 Chat Pattern 要求活跃会话支持附件。
- FEAT-126 候选 Pattern 为当期范围明确拒绝附件、paste 和 drop。
- 处理：新增 FEAT-127 Pattern，只取代 FEAT-126 中“附件禁用/拒绝”的冲突段落，不改写 FEAT-126 历史。
- `ChatComposer.vue/test`、`ChatPage.vue/test` 和 FEAT-126 visual harness 当前已有用户改动；实现必须逐行融合，不覆盖或回退。

## 5. 存储与 migration

- 权威源依次为 `yijie-desktop/src-tauri/migrations/chat/0006_chat_attachments.sql` 与 `0007_chat_attachment_draft_targets.sql`。
- v6 新增 attachment、message content block、text chunk 表和必要索引；v7 为 ready 草稿增加 `new/session` target identity、约束与索引；不使用 FTS/virtual table。
- BLOB 与 extracted chunks 留在 SQLCipher；不建立 plaintext app-data 文件。
- v1-v5 历史数据升级后由 v7 reader 继续读取。旧 reader 对 `user_version=7` fail closed，不支持就地降级；回退需恢复迁移前的完整加密备份或 roll-forward。v6 已绑定历史保留；无 target 的 ready 草稿在 v7 升级时删除，避免恢复到错误 composer。删除和 TTL maintenance 需要 checkpoint 证据。

## 6. 安全与隐私

- 数据分类：confidential；文件名也可能敏感，不进入日志。
- 信任边界：WebView 只持 opaque attachment ID 和显示元数据；native 边界校验路径/文件/owner/symlink/size/magic。
- Host 只收到选出的文本片段和 image data URL，不持久化正文；bbolt、Public API 和 PostgreSQL 不得出现内容。
- 拒绝 archive、SVG、macro Office、active content 和路径穿越。
- 当前无云 DLP/病毒扫描，因此只允许本地显式选择并保持 read-only Runtime；生产启用需重新做安全评审。

## 7. 依赖和环境

- 预期新增锁定 Rust parser/base64 依赖；必须在 diff 和许可证/漏洞检查中登记。
- macOS native picker 使用既有 `rfd`；不新增 Tauri capability、外部 URL 或网络目标。
- 单元和集成不需要云资源或真实模型。真实 Runtime image turn 属于本地可选集成，不在未授权情况下调用付费模型。

## 8. 初始 Git 证据

- Governance：`e584f15b561c43877b278c19b9dcef643f41051d`，创建 FEAT-127 前 clean。
- Contracts：`98e89d8cccfe15256f09e9329d4bc1980d6da578`，clean。
- Host：`d9c770e27bfa4796d22aa50074652971ae47eff6`，clean。
- Desktop：`16c5b9d5be4723455ea65ae349daab5ce8bbd141`，已有 FEAT-126 UI/verification dirty changes。
- 根目录不是 Git repository；各兄弟仓独立状态与提交历史。

## 9. 交付 Git 证据

- Contracts：`ebdd30f076614ebc7f5149aebf70e851b81ff32b`，已推送到 `origin/feat/feat-126-content-free-candidate`；其中 `bd0dc050...` 为功能契约提交，`ebdd30f...` 补充 Go validator 兼容修复与回归测试。
- Host：`673de86d3d076f4600eb0d0bfb215382677afd72`，已推送到 `origin/feat/feat-126-foundation-closure`，`api/contracts.lock` 精确固定 `ebdd30f...`。
- Desktop：`3efed9aba5faab90ca3ea397a4d6489890df2026`，已推送到 `origin/feat/feat-126-foundation-closure`，Public API 与 Chat authority 均固定 `ebdd30f...`。
- 三个实现仓提交后工作区与上游同步；没有 tag、merge、release artifact 或部署。
