# ADR-0013: 固定 Desktop 本地会话数据权威与存储职责

## 状态

Accepted

## 日期

2026-08-02

## 决策负责人

段成威

## 关联需求

- `FEAT-126-public-task-authorization-hardening`
- `ADR-0012-authoritative-identity-tenant-and-permission-boundary`
- `ADR-0014-desktop-conversation-protection-and-deletion-boundary`（Accepted 2026-08-02）

## 背景

FEAT-126 需要在 macOS Desktop 中持久化 confidential 的 session、消息、公开 reasoning
summary、游标与 outbox，并支持离线列表、按 session 懒加载、事务去重和可验证的物理删除。
项目的本地开发环境同时已有 PostgreSQL、Redis 和 PostgreSQL + pgvector，容易把“本机运行”
误解成“适合嵌入 Desktop”。这些服务分别服务于 API、短期协调和 Knowledge/RAG，并不是
Desktop 用户会话正文的既有权威源。

Desktop 的仓库边界还明确禁止 WebView 或 Desktop 直接访问 PostgreSQL/Redis；Agent Host 的
bbolt 只保存 task/session/thread/turn 映射，Runtime 自有状态也不应成为易界产品列表与历史
展示的业务数据库。因此必须先冻结数据职责，再评审驱动、保护和删除实现。

## 决策

1. FEAT-126 的本地会话正文与产品状态由 `yijie-desktop` 的 Rust/Tauri 原生边界持有，使用
   Desktop app-data 中的嵌入式、版本化 SQLite。Vue 只能通过窄、带 identity/tenant scope 的
   typed commands 访问，不得取得数据库路径、SQL 入口或数据库密钥。
2. SQLite 是本期以下数据的本地业务权威：chat projects 的安全引用、sessions、messages、
   turns、允许公开的 reasoning summaries、event cursors、outbox 与标题元数据。表级 scope、
   migration checksum、外键、唯一约束和物理删除语义由 Desktop migration source 定义。
3. `yijie-api` 的 PostgreSQL 继续作为服务端 Public Tasks、身份/租户/RBAC 和审计等服务端业务
   状态的权威源。FEAT-126 不把 conversation message body、reasoning summary 或本地项目路径
   上传到该数据库，也不引入 Desktop 与 Public Tasks 的逐 turn 双写。
4. Redis 不作为任何 FEAT-126 业务真相源。本期不因会话功能而引入 Redis；未来只有在有明确
   指标与失效语义的缓存、限流、幂等或短期协调需求出现并通过独立设计评审后才可使用。
5. PostgreSQL + pgvector 继续属于 `yijie-knowledge` 的 Knowledge/RAG 方向。FEAT-126 不做
   embedding、语义检索或向量索引，因此 pgvector 不进入本期数据路径。
6. Agent Host 的 bbolt 只保存本地适配映射/状态；Codex Runtime 只持有其 canonical thread/
   rollout/state。二者都不是易界会话正文和任务记录列表的业务权威，但属于永久删除必须清理
   或明确披露的外部数据表面。
7. 本期是 local-first，不承诺“以后只改配置”即可切换云数据库。云同步、多设备合并、冲突解决、
   上传同意、迁移和回滚必须由后续 feature 与版本化 storage contract 单独批准。
8. 本 ADR 只冻结数据权威和存储职责，不授权业务实现，也不决定：
   - SQLite Rust driver/crate、连接池与 migration library；
   - 文件加密、Keychain 密钥管理、OS Data Protection、目录权限与 threat-model 结论；
   - WAL/checkpoint/`secure_delete` 的最终参数与磁盘残留证明；
   - app-level backup、OS backup 可恢复边界、卸载和保留策略；
   - Host/Runtime 删除契约、模型标题/summary 能力、Public Tasks API 版本与 consumer 迁移。
   这些项目继续阻断 FEAT-126 G2 通过。

## 备选方案

### Vue localStorage / IndexedDB

优点是接入快；缺点是 confidential 数据、事务/迁移、原生密钥、租户绑定和可验证删除边界弱，
且扩大 WebView 攻击面，因此拒绝。

### Agent Host bbolt 保存全部会话

可以减少一个数据库，但会把产品业务 schema、历史查询和租户生命周期耦合到薄 Runtime adapter，
与现有职责冲突，因此拒绝。

### Desktop 直连本机 PostgreSQL/Redis/pgvector

可复用开发 compose，但要求用户安装和维护服务进程，扩大端口、凭证、升级、备份和故障面，
也违反 Desktop 仓库边界。Redis 不提供所需关系事务真相，pgvector 没有本期检索用途，因此拒绝。

### 会话正文直接写 Public API PostgreSQL

便于未来云访问，但立即引入网络可用性、跨库双写、隐私上传、服务端保留和多设备冲突语义，
与本期 local-first 范围不符，因此拒绝。

## 影响

- `yijie-desktop` 将在 G2/G2A 以后才可能新增 Rust-owned SQLite repository、版本化 migration
  和窄 IPC；本 ADR 不选择依赖，也不授权添加依赖。
- `yijie-agent-host` 与 `yijie-codex` 仍需提供或桥接可验证的 cleanup 能力，但不保存第二份易界
  业务正文。
- `yijie-api` 的 Public Tasks hardening 可独立使用 PostgreSQL，不因 Desktop 会话完成而上传正文
  或提前开放 legacy routes。
- 2026-08-02 LIA-126-002 conformance note：既有`c000a024`候选的Public Tasks v2允许任意
  `input`，且canonical fixture携带并回显conversation `input.text`。该shape不能作为本ADR第3项
  “不上传conversation正文”的实现证据；DEC-126-023/G2A复审关闭前，相关provider/consumer实现暂停。
- Redis 与 pgvector 保持现有平台职责，避免为没有明确价值的本地会话增加服务依赖。
- 未来云同步不是存储 adapter 替换，而是新的产品、安全、契约、迁移和发布问题。

## 风险

- SQLite driver、加密/文件保护、WAL 残留、备份/卸载尚未冻结；在这些问题关闭前不能宣称
  “数据已安全落盘”或“永久删除所有痕迹”。
- 同一 session 横跨 Desktop SQLite、Host bbolt 与 Runtime state，无法使用单个数据库事务；
  删除必须采用可重试、幂等的跨进程清理状态机。
- OS 账户被攻陷时 owner-only 文件权限不能提供完整保护；需要后续 threat review 决定是否引入
  数据库级加密和 Keychain 密钥。
- 未来云同步若绕过独立 feature，可能造成重复、丢失、隐私和保留策略冲突。

## 后续动作

- [x] 段成威同意 Desktop 会话使用 Rust/Tauri-owned embedded SQLite，PostgreSQL/Redis/pgvector
      保持各自职责（2026-08-02）。
- [x] ADR-0014 已于 2026-08-02 接受 SQLite driver/migration、文件保护/加密、backup/卸载与
      WAL 删除边界。
- [x] ADR-0014 已于 2026-08-02 接受 Desktop/Host/Runtime 跨进程物理删除状态机和
      content-free receipt。
- [ ] 在任何代码切片前完成 Desktop Pattern、contract design、test plan 与人工 G2 批准。
