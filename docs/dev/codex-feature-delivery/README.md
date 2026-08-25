# Codex 双模式需求交付

本目录提供两个互斥的交付 Profile。新需求默认使用 `demo_fast`；只有用户明确选择、准备生产激活，
或现有 Accepted ADR/高风险边界要求完整加固时，才使用 `production_hardened`。

| Profile | 目标 | 实现方式 | 完成定义 |
|---|---|---|---|
| `demo_fast`（默认） | 8–16 小时内形成逻辑完整、交互清晰、真实服务可用的 Demo | 一次补全产品/UX，整个需求连续实现，随后真实启动并修 Bug | D0 产品/UX完整；D4 一次 fresh real-service run 通过全部 Must AC |
| `production_hardened`（显式） | 可维护、可测试、可回滚、可发布的生产服务 | 原 G0→G6、G2A/G2V、per-slice G3、harness、freshness 与发布观察 | G6 Delivery Complete |

`exposure` 与 Profile 正交：

- `local`：只有开发者本机可以访问；`demo_fast` 在 D4 后可关闭。
- `public`：非本人或不可信客户端可以访问；`demo_fast` 还必须通过 DP 最小公开安全检查。
- `public` 不等于 `production_hardened`。出现付费用户、SLA、多租户/PII、重要持久数据、不可逆
  migration、合规或组织级生产责任时，应新建或显式选择 `production_hardened`。

## 不随 Profile 降级的红线

- 每次都分类 `contract-impact = none | additive | semantic | breaking`；契约变更先改权威源，不复制影子 DTO。
- 不提交或输出 secret、token、PII；真实敏感数据、生产写入、破坏性操作和付费调用需要明确授权。
- public/production 的身份、资源授权、租户、审批和审计仍由服务端权威控制，不能交给 UI 或 prompt。
- `demo_fast + local` 默认采用 ADR-0018 `local_demo_direct`：native 固定本地 identity/tenant/capability，
  无登录页、浏览器或账号密码并直达首个业务主页面；保留进程内 scope/context 校验，禁止扩散到公网。
- 不覆盖用户已有改动，不用 mock/synthetic 结果冒充真实服务可用，不把未运行命令写成 PASS。
- commit、push、tag、部署、公开暴露和生产迁移仍需明确授权。

## 新建需求

默认创建 `schema_version: 3`、`demo_fast`、`local`：

```bash
./scripts/new-feature.sh FEAT-123 task-history-export ./work
```

生成四个文件：

```text
FEAT-123-task-history-export/
  feature.yaml
  00-feature-brief.md
  01-delivery-log.md
  02-verification.md
```

公开 Demo：

```bash
./scripts/new-feature.sh --exposure public FEAT-123 task-history-export ./work
```

显式生产加固：

```bash
./scripts/new-feature.sh \
  --profile production_hardened \
  --exposure public \
  FEAT-123 task-history-export ./work
```

`production_hardened` 继续生成原来的 `feature.yaml + 00—10 + 04A` 完整包。

## demo_fast 闭环

```text
一次补全业务逻辑、Must AC、交互与 UI 状态
  → D0
  → local exposure 装配免登录 direct-entry 与真实主页面
  → 确认真正入口、官方 API 与 Contract First 顺序
  → 整体实现（不建立治理切片）
  → 启动真实服务
  → 发现 Bug 即修复、重启、复测
  → 一次 fresh run 通过 Must AC、真实 happy path 和代表性失败
  → D4
  → exposure=public 时再通过 DP
```

```bash
./scripts/check-feature-package.sh --gate D0 <feature-dir>
./scripts/check-feature-package.sh --gate D4 <feature-dir>
./scripts/check-feature-package.sh --gate DP <feature-dir> # 仅 public
```

D4 不要求 Temporal Matrix、per-slice G3、harness qualification、三项拆分 E2E、性能/安全专项、
full-green、发布/回滚或线上观察；但要求真实入口、focused checks、真实服务 smoke、一个代表性失败、
可视 Artifact、diff 审阅及全部 Must AC 一次通过。

## production_hardened 闭环

原生产流程完整保留：

```text
G0 → G1 → G2 → G2A（条件性）→ Harness Qualification → G2V
   → G3/S1 → G3/S2 → ... → G4 → G5 → G6
```

```bash
./scripts/check-feature-package.sh --gate G2 <feature-dir>
./scripts/check-feature-package.sh --gate G2V <feature-dir>
./scripts/check-feature-package.sh --gate G3 --slice S1 <feature-dir>
./scripts/check-feature-package.sh --strict <feature-dir>
```

详细规则见 [HANDBOOK.md](HANDBOOK.md)、[QUALITY_GATES.md](QUALITY_GATES.md) 和
[checklists/production-readiness.md](checklists/production-readiness.md)。

## Demo 时间盒

- 目标 12 小时，硬停止 16 小时。
- 30 分钟无新增事实：停止猜测式补丁，读取真实日志和完整调用链。
- 90 分钟同一阻塞：选择最简单方案或 workaround。
- 非核心测试/harness 最多 120 分钟，不能长期阻断业务结果。
- 核心路径 240 分钟仍不通：缩小 MVP、改变实现方案或请求用户决策。

这不是允许隐藏失败。D4 仍必须真实可用；时间盒决定何时简化，不决定何时伪造绿色。

## Schema 与历史兼容

- schema v1：历史只读，保持既有兼容。
- schema v2：按原 `production_hardened` 语义继续校验；已有包和 failure ledger 不改变。
- schema v3：显式声明 `delivery_profile` 与 `exposure`；新需求必须使用 v3。
- Profile 创建后不可静默改名以绕过门禁。`local → public` 可以升级，但必须补 DP；`public → local`
  不得用来删除公开安全事实。Demo 进入生产时建立显式 `production_hardened` 包并复用已有事实，
  不把 D4 自动换算成 G4/G5/G6。

仓库审计仍扫描全部 committed Feature Package：

```bash
node docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs \
  --audit-claims docs/features/FEAT-123-example

pnpm feature:audit -- --base-ref <BASE_COMMIT>
```

## 文档入口

- [QUICKSTART.md](QUICKSTART.md)：两种 Profile 的最短上手路径。
- [HANDBOOK.md](HANDBOOK.md)：Demo 快速闭环和完整生产生命周期。
- [DOCUMENT_CATALOG.md](DOCUMENT_CATALOG.md)：两种 Profile 的产物边界。
- [CODEX_PLAYBOOK.md](CODEX_PLAYBOOK.md)：Codex 的 profile-aware 操作方式。
- [QUALITY_GATES.md](QUALITY_GATES.md)：D0/D4/DP 与 G0–G6。
- `templates/demo-fast-feature-package/`：默认紧凑模板。
- `templates/feature-package/`：完整生产加固模板。

Codex 可以起草方案和记录实际结果，但不能虚构用户批准、命令输出、真实服务状态、外部调用或发布事实。
