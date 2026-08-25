# ADR-0017: 双 Profile 需求交付与 Demo Fast 默认值

## 状态

Accepted

## 日期

2026-08-23

## 决策负责人

段成威

## 背景

现有 `codex-feature-delivery` 只面向生产级交付。它要求 00—10、04A、G0—G6、G2A/G2V、
per-slice G3、runtime harness qualification、freshness、三项最终 E2E、failure ledger、独立加固、
发布/回滚和线上观察。该模式适合生产服务，但个人作品 Demo 的主要目标是快速获得逻辑完整、交互
清晰、真实本地可用的业务结果；同一流程导致实现工时被治理和非必要生产证明放大。

段成威明确决定：新需求默认以约原工时十分之一为目标，不拆治理切片；实现前由 Codex 补全业务逻辑、
交互和 UI，随后整体实现并立即启动真实服务，有 Bug 就修复，直到正常使用。当前项目暂无云资源或
正式部署计划，本地可用即可；标准仍需区分未来公开 Demo 与生产激活。

## Contract Impact

`semantic`。Feature Package 的新建默认、机器 schema、Gate 语义和 Codex 长期工作方式改变，但不改变
业务 wire contract、ADR-0011 的 Contract First 权威源或各服务的认证/数据边界。

## 决策

1. 建立两个互斥 Profile：
   - `demo_fast`：所有新需求默认；目标 8—16 小时内完成真实可用 Demo。
   - `production_hardened`：用户显式选择或命中生产升级条件；完整保留原生产流程。
2. 增加 `exposure: local | public`：
   - local Demo 在 D4 后可关闭；
   - public Demo 在 D4 后还必须通过 DP 最小公开安全检查。
3. 新 Feature Package 使用 schema v3，显式声明 Profile/Exposure；历史 schema v1/v2 不改语义，
   schema v2 继续视为原生产加固包，不要求迁移。
4. `demo_fast` 只保留四份紧凑材料：`feature.yaml`、Demo Brief、Delivery Log、Verification。
5. `demo_fast` 执行顺序为：一次补全产品逻辑/UX/UI/Must AC → D0 → 整体实现 → 真实服务启动 →
   Bug 修复/重启/复测 → 一次 fresh run 通过全部 Must AC、真实 happy path 和代表性 failure/retry → D4。
6. Demo 不建立治理切片、per-slice G3、Temporal Matrix、harness qualification、freshness、三项拆分
   E2E、完整性能/安全/韧性专项、full-green、灰度或线上观察。
7. Demo 调试使用 30/90/120/240 分钟时间盒和 16 小时硬停止；时间盒触发扩大真实调用链诊断、
   简化、登记非核心限制或缩小 MVP，不允许隐藏失败或“重跑到绿”。
8. `production_hardened` 继续执行 G0→G1→G2→G2A→Harness Qualification→G2V→per-slice G3→
   G4→G5→G6，三次同类失败熔断和 append-only failure ledger 不变。
9. 下列红线对两个 Profile 都强制：Contract First 权威源和 source-first、无影子 DTO、公开/生产服务端授权、
   secret/PII、安全审批与审计、已有工作区保护、真实命令/服务事实，以及 commit/push/tag/部署/付费/
    破坏性/生产写操作的明确授权。
   `demo_fast + local` 的免登录直达例外由 ADR-0018 单独约束；它保留 native scope/context 边界，
   不适用于 public/production。
10. public Demo 最少验证服务端密钥、鉴权/数据边界、输入/文件/超时、付费成本上限、安全错误、
    最简恢复和公网 smoke。
11. 付费用户、SLA、多租户/PII、重要持久数据、不可逆 migration、合规或组织级生产责任触发
    `production_hardened`。D4/DP 不自动转换为 G4/G5/G6；升级时建立显式生产包并复用可追溯事实。

## 备选方案

### 继续单一生产流程

证据最完整，但与个人 Demo 的时效目标冲突，已拒绝。

### 在 schema v2 原地增加可选字段

改动较少，但会改变既有 v2 的机器语义并给历史包带来歧义，已拒绝。

### 完全取消治理

最快，但会丢失业务逻辑、Contract First、真实服务验证、外部授权和公开安全边界，已拒绝。

## 影响

- `new-feature.sh` 默认生成 schema v3 `demo_fast + local`，生产 Profile 必须显式参数。
- validator/checker/audit 同时支持历史 v1/v2 和 schema v3 双 Profile。
- Codex 默认不再为 Demo 拆切片或先建设生产 harness，而是先完成完整 UX 后进入真实服务闭环。
- 公开与生产成为两个清晰升级点，避免把本地 Demo 写成生产就绪。
- 历史 Feature Package、Gate、failure ledger 和证据不被重写。

## 风险

- Demo 可能积累性能、可访问性、韧性和运维债务；必须在 Verification 中明确限制，并在公开/生产升级时补齐。
- 使用者可能把 D4/DP 误称为生产完成；schema、checker 和文档必须拒绝这种映射。
- 时间盒可能诱发过度简化；Contract First、安全、授权和真实服务红线不得纳入可裁剪范围。

## 后续动作

- [x] 新增 schema v3 双 Profile/Exposure validator 与历史兼容规则。
- [x] `new-feature.sh` 默认 `demo_fast + local`，显式支持 `production_hardened/public`。
- [x] 新增紧凑 Demo 模板、D0/D4/DP 和直接测试。
- [x] 同步 README、Quickstart、Handbook、Quality Gates、AGENTS 与项目长期记忆。
- [ ] 首个新需求使用后复盘 8—16 小时时间盒和 D4/DP 字段是否需要精简。
