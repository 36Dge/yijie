# ADR-0014: 冻结 Desktop 会话保护、删除、备份与卸载边界

## 状态

Accepted

## 日期

2026-08-02

## 决策负责人

段成威

## 关联需求

- `FEAT-126-public-task-authorization-hardening`
- `ADR-0013-desktop-local-conversation-data-authority`

## 背景

ADR-0013 已冻结 Desktop Rust/Tauri-owned embedded SQLite 为本地会话业务权威，但有意把
driver、migration、加密、文件保护、WAL、物理删除、备份和卸载留给 G2。FEAT-126 的一个
session 同时跨 Desktop SQLite、Agent Host bbolt/in-memory replay 与 Codex Runtime thread tree；
单删一处会造成 UI 已消失但仍可 resume 的假删除，跨进程又不存在单一事务。

2026-08-02 使用固定 Runtime `codex-cli 0.144.6`（macOS arm64，SHA-256
`1ef4f1daba0c5ac267e9bf661d129c3dfc59ffe5cd9ab7767b22a1e9508df1fe`）在自动清理的临时
`CODEX_HOME` 中只创建合成 thread、设置 canary 名称并调用一次 `thread/delete`。没有 provider
凭据、没有模型 turn、没有 MiniMax 调用，也没有访问真实数据。删除通知、同进程读取失败、重启后
读取失败、state DB 行和 rollout/index 清理均通过；但 canary/ID 的字节仍可在 Runtime
`state_5.sqlite-wal`，以及 ID 在 `logs_2.sqlite` 中检测到。因此 Runtime 提供功能删除与重启后
不可恢复，不提供法证级字节抹除；产品不得承诺“删除所有磁盘痕迹”。

## 决策

### 1. SQLite driver 与执行模型

1. Desktop 使用精确锁定的 Rust 依赖：
   - `rusqlite = { version = "=0.40.1", default-features = false, features = ["bundled-sqlcipher", "uuid", "limits"] }`
   - `rusqlite_migration = "=2.6.0"`
2. 不使用 Tauri SQL plugin、SQLx 或 Refinery。临时 Rust 1.95.0/macOS arm64
   `cargo check --locked` 已证明上述组合可构建；Refinery 0.9.2 的 rusqlite feature 只兼容至
   rusqlite 0.39，并与 0.40.1 的 `libsqlite3-sys` native `links` 冲突。
3. 同步 rusqlite 只能运行在 Rust-owned repository worker 上：单一串行 writer、有限只读连接；
   WebView 不接触 SQL/path/key，且不得在 Tauri/Tokio UI async executor 上执行阻塞数据库操作。

### 2. Migration

1. migration 是嵌入二进制、递增编号、forward-only 的 SQL；不提供生产 down migration。
2. `rusqlite_migration` 以 SQLite `user_version` 作为执行版本；每次 migration 在同一原子事务中
   通过 `up_with_hook` 写入 `chat_schema_migrations(version, name, sha256, applied_at)`。第一版
   migration 创建该表。
3. 启动时把数据库记录与二进制内嵌 SHA-256 catalog 对比；历史 checksum 漂移、DB 版本高于
   当前 binary、migration 或 `foreign_key_check` 失败均 fail closed，不打开 Chat。
4. CI 必须执行 migration validate，以及空库、逐版本升级、重复启动、损坏/只读/磁盘满 fixture。
   migration 使用事务原地回滚，不为升级静默生成含正文的数据库副本。修复只允许 forward repair，
   或经用户明确确认的 destructive reset。

### 3. 路径、权限与加密

1. 数据库存放于 bundle identifier `com.yijie.ai` 所解析的 Tauri `app_data_dir` 下的 `chat/`
   子目录；目录 mode `0700`，
   DB、`-wal`、`-shm` mode `0600`。每次 open 前校验 owner、mode、regular-file、非 symlink 且
   link count 为 1；异常 fail closed。
2. 使用 `bundled-sqlcipher` 的 SQLCipher community build 做数据库级 AES-256 加密。每个 OS 用户/
   app install 使用随机 32-byte key，保存在 macOS Keychain，service
   `com.yijie.ai.chat-db`、account/version `default-v1`。
3. Rust 通过 `sqlite3_key_v2` 的 raw bytes 在任何 SQL/PRAGMA/schema read 之前设置 key；key 不进入
   WebView、配置、URL、child env、错误或日志，并在使用后 zeroize。打开已有数据库时 Keychain key
   缺失或错误必须 fail closed，不能生成新 key 覆盖旧库；只可提供明确、不可逆的本地数据 reset。
4. 打开后启用 `cipher_memory_security=ON`。这减少 SQLCipher allocation 的内存残留，但不声称抵御
   已控制同一 OS 账户、进程内存或完整设备取证的攻击者。

### 4. SQLite connection 与删除参数

每个 connection 在 key 成功后设置并验证：

- `foreign_keys=ON`
- `journal_mode=WAL`
- `synchronous=FULL`
- macOS `fullfsync=ON`、`checkpoint_fullfsync=ON`
- `secure_delete=ON`，不得使用可能保留 freelist 内容的 `FAST`
- `busy_timeout=5000`
- `wal_autocheckpoint=1000`
- `journal_size_limit=1048576`
- `trusted_schema=OFF`

FEAT-126 v1 不使用 FTS 或其它 virtual table；SQLite 明确指出部分 shadow table 不保证受
`secure_delete` 完整擦除。对话删除事务提交后必须在独占 maintenance step 执行
`PRAGMA wal_checkpoint(TRUNCATE)` 并验证返回的 busy/result；busy、错误或 WAL 未归零均是
`cleanup_incomplete`，不能向 UI 返回成功。参数用于缩小 app-owned SQLite 的普通残留窗口，
不是 SSD/APFS/OS backup 或 Runtime 日志的法证抹除保证。

### 5. Session 删除范围与顺序

1. 用户对明确 session 做一次不可逆确认。Desktop 创建幂等、加密的 deletion job并获取 durable
   lease，阻断该 session 的新 writer、late SSE 和 outbox retry。
2. active turn 必须先 interrupt 并等待唯一 terminal；不确定或超时即停止删除，session 保持可见的
   `delete_failed` 状态。
3. Host 验证此 session 独占目标 Runtime thread tree；任何另一 session 指向同一 root/descendant
   均中止。Host 调用 Runtime `thread/delete`，验证 response 和 `thread/deleted`，覆盖 spawned
   descendants；随后清除 bbolt 的 task/session/thread/turn mapping 与该 session 的 in-memory replay。
4. 外部表面确认不可 resume 后，Desktop 在一个启用 FK 的事务中级联删除 session、messages、turns、
   public summaries、cursors、outbox、title 和项目引用快照；不删除聊天项目引用本身，更不删除用户目录。
5. Desktop 执行并验证 `secure_delete` + `wal_checkpoint(TRUNCATE)` 后，才将 job 压缩为成功 receipt。
   任何分表面失败都沿同一个 operation ID 前向重试；不能先从 UI 隐藏再声称成功。

### 6. Content-free receipt

进行中的加密 job 可暂存重试必需的技术 ID，但不得包含 title、message、summary 或 path。成功后删除
原始 Runtime/Host/session ID，只保留：deletion operation ID、带应用秘密的 scoped session ID keyed
hash（HMAC-SHA-256，使用独立于 DB key 的 32-byte Keychain receipt key，service
`com.yijie.ai.chat-receipt`、account `default-v1`）、Desktop/Host/Runtime 分表面结果位、稳定
outcome/error code、requested/completed timestamp 与 receipt schema version。成功 receipt 保留
30 天后物理删除并 checkpoint；它不能用于恢复正文，也不是延长正文保留的审计记录。

### 7. 备份与卸载语义

1. FEAT-126 v1 不创建 app-level database backup、export、snapshot、cloud sync 或 iCloud container。
   migration 依赖原子事务和 forward repair，不静默复制 confidential DB。
2. chat 目录及每次创建/rename 的 DB、WAL、SHM 文件都设置并复核 macOS
   `isExcludedFromBackupKey=true`。该控制减少进入 OS backup 的机会，但不能回收已存在的 Time
   Machine local snapshot、第三方备份、APFS snapshot、文件系统/SSD 历史或被用户复制的旧文件。
3. 删除成功文案只能说“已从当前易界应用管理的活动数据中移除，无法在应用中重新打开或恢复”；
   必须披露 OS/第三方备份可能仍保留不受应用控制的副本，不能说“删除所有磁盘痕迹”。
4. 把 `.app` 拖入废纸篓只删除 app bundle；Application Support 数据与 Keychain item 可能保留，
   同一签名/Keychain access 的重装版本可能重新打开数据库。FEAT-126 不把普通卸载定义成擦除数据。
   “删除全部本地聊天数据”或受管卸载需要后续独立 feature、全 session cleanup 和明确确认。

## 备选方案

### 未加密 SQLite + owner-only mode

依赖少，但复制 app-data 后正文直接可读，不能满足 confidential data 的本地保护基线，因此拒绝。

### SQLx 或 Tauri SQL plugin

SQLx 提供 async API、plugin 提供前端便利，但本期是单进程本地嵌入库，最重要的是窄 Rust boundary、
SQLCipher build 与确定 migration；额外 abstraction/IPC 面没有足够收益，因此拒绝。

### Refinery migration

有 checksum 优点，但当前稳定版本与锁定 rusqlite 0.40.1 的 native SQLite dependency 冲突。选择
`rusqlite_migration` 并在同一 migration transaction 中补充 checksum ledger。

### 只删除 Desktop 行

会留下可 resume 的 Host/Runtime 数据，违反用户看到的永久删除语义，因此拒绝。

### 承诺法证级磁盘抹除

SQLite WAL、Runtime logs、APFS/SSD 与备份都超出单个事务的可证明范围；隔离验证也已找到 Runtime
字节残留，因此拒绝该声明。

## 影响

- 未来 `yijie-desktop` 实现需要新增已锁定的 Rust/SQLCipher dependencies、Keychain lifecycle、
  migration fixtures 和 native file protection；本 ADR 本身不授权代码变更。
- Agent Host 必须增加幂等 cleanup operation，清理 bbolt/in-memory replay，并把 Runtime 分表面结果
  传回 Desktop；不能把 `thread/delete` 的 RPC 成功等同于所有磁盘字节已擦除。
- 删除需要可恢复 saga 而非跨数据库事务，只有 required live surfaces 全部验证后才向用户成功。
- Public Tasks、MiniMax reasoning/title 能力和 Desktop Pattern/contract 决策仍独立阻断 G2。

## 风险

- 同一 OS 用户下的恶意软件、已解锁 Keychain 或进程内攻击仍可读取数据；SQLCipher 不是完整 endpoint
  security。
- `secure_delete=ON` 与 FULL/fsync/checkpoint 会增加写放大和删除延迟，需要后续 benchmark 与 timeout
  预算；安全语义优先于无证据的性能优化。
- Runtime 自有 WAL/log 与 OS/第三方备份可保留字节；必须保持限定文案和后续可复现残留测试。
- Keychain item 丢失会使数据库不可读；fail-closed 与 explicit reset 避免静默覆盖，但用户可能失去
  本地历史。

## 证据与参考

- rusqlite feature/build：<https://github.com/rusqlite/rusqlite>
- rusqlite_migration atomic/user_version：<https://docs.rs/rusqlite_migration/latest/rusqlite_migration/>
- SQLCipher key 与 memory security：<https://www.zetetic.net/sqlcipher/sqlcipher-api/>
- SQLite `secure_delete`：<https://sqlite.org/pragma.html#pragma_secure_delete>
- SQLite WAL/checkpoint：<https://sqlite.org/pragma.html#pragma_wal_checkpoint>、<https://sqlite.org/wal.html>
- Apple backup exclusion：<https://developer.apple.com/documentation/foundation/urlresourcekey/isexcludedfrombackupkey>
- Time Machine exclusion/local snapshot 限制：<https://support.apple.com/en-au/guide/mac-help/mh15622/mac>

## 后续动作

- [x] 只在临时 `CODEX_HOME` 对固定 Runtime 执行一次无模型、无真实数据的 delete residue 验证。
- [x] 在临时 Rust 1.95.0 项目验证 rusqlite/SQLCipher/migration 依赖可构建，并记录 Refinery 冲突。
- [x] 段成威于 2026-08-02 批准本 ADR 与 DEC-126-006，并关闭 Q-006/Q-015；该批准不等于
      G2 通过或实现授权。
- [ ] 在实现前冻结 Host cleanup private contract、Desktop schema migration 与 UI 限定披露文案。
- [ ] G4/G5 以合成 canary 重跑 Desktop/Host/Runtime/live-store/backup 边界测试。
