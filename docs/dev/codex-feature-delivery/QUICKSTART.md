# 快速开始

## 1. 先选 Profile 与 Exposure

默认值为 `demo_fast + local`。不要因为需求跨仓、涉及 Runtime 或第三方 API 就自动升级；先按 Demo
目标实现真实用户结果。只有用户明确选择、准备生产激活，或命中生产升级条件时使用
`production_hardened`。

```bash
# 默认：本地 Demo
./scripts/new-feature.sh FEAT-123 task-history-export ./work

# 公开 Demo
./scripts/new-feature.sh --exposure public FEAT-123 task-history-export ./work

# 完整生产加固
./scripts/new-feature.sh --profile production_hardened --exposure public \
  FEAT-123 task-history-export ./work
```

## 2. demo_fast：先一次补全逻辑与 UI

第一轮 Codex 输出一个推荐完整方案，不拆治理切片：

```text
请按 demo_fast 完成产品与 UX 定稿：
1. 核对真实代码入口、已有工作区改动和 contract-impact；
2. 补全目标用户、问题、主流程、业务规则和明确非目标；
3. 补全 idle/loading/success/empty/error/retry/cancel；
4. 给出布局、主要操作、反馈、预览/保存等高质量交互；
5. 写出 5—10 条可操作判断的 Must AC；
6. 对不影响目标/安全/成本的未知项使用推荐默认值继续。
不要实现，不要创建切片。
```

完成后：

```bash
./scripts/check-feature-package.sh --gate D0 <feature-dir>
```

## 3. demo_fast：整个需求连续实现

```text
按已确认的 Demo Brief 完成整个需求。

要求：
- 契约变更先改权威源，再改 producer/consumer；
- 可按技术依赖顺序工作，但不建立治理切片或逐切片 evidence；
- 复用现有组件，不扩展到性能、安全专项或无关重构；
- 只补能保护核心逻辑的 focused tests；
- 保护已有工作区，付费/破坏性/生产操作必须在批准上限内。

实现完成后立即启动真实服务，不要停在“代码已写完”。
```

`exposure=local` 的应用入口默认遵循 ADR-0018：使用 canonical `local + demo_fast` 启动器，自动建立
固定本地身份/租户上下文，零登录交互并直达业务主页面。不得把手工输入白名单账号密码、启动
Keycloak/OIDC 或先修认证测试环境当作正常 Demo 前置条件。进程间 token 与外部 Provider Key 可由
本地服务自动管理，但不能进入 UI、日志或仓库。

## 4. demo_fast：真实启动—修 Bug 循环

```text
正常启动真实本地服务
  → 执行全部 Must AC
  → 验证一个真实 happy path
  → 验证一个代表性 error/retry
  → 有 Bug：定位、修复、重启、复测
  → 全部在一次 fresh run 中通过
```

只把真实 Provider/Runtime/数据库/桌面组合写成真实服务；mock、synthetic Artifact 或独立测试 App
不能满足 D4。最终执行：

```bash
./scripts/check-feature-package.sh --gate D4 <feature-dir>
```

## 5. 调试时间盒

- 30 分钟没有新事实：停止局部猜测，读取完整日志和调用链。
- 90 分钟同一阻塞：采用最简单实现、关闭非核心花活或提出一个 workaround。
- 非核心 harness、accessibility、完美 cleanup 或全量测试最多 120 分钟；本地 Demo 可登记限制。
- 240 分钟核心结果仍不可用：缩小 MVP 或更换架构。
- 16 小时仍未 D4：必须重新定范围，不继续累积流程与基础设施。

## 6. exposure=public：再补 DP

首次让非本人访问之前，完成最小公开安全底线：服务端密钥、鉴权/数据边界、输入/文件/超时限制、
付费成本上限、安全错误、最简恢复方式及公网真实 smoke。

```bash
./scripts/check-feature-package.sh --gate DP <feature-dir>
```

公开 URL、云资源、真实用户账户/数据、外部可重复触发的付费 API 都会触发 DP。若同时存在付费用户、
SLA、多租户/PII、重要持久数据、不可逆 migration 或合规责任，应使用 `production_hardened`。

## 7. production_hardened

显式选择后沿用原完整流程：实现前完成 00—07，按 G2A、Harness Qualification、G2V、per-slice G3、
三项最终 E2E、G4、G5、G6 推进。详见 [HANDBOOK.md](HANDBOOK.md)。

## 8. 共同红线

- 不伪造测试、调用、批准、commit、tag、部署或服务 ready。
- 不提交 secret/PII；public/production 不绕过服务端授权、审批和审计。local direct-entry 只按
  ADR-0018 在固定 native scope 内免用户登录。
- 不在未知 dirty worktree 上 reset、覆盖或批量格式化。
- 不从 mock-only 绿色推断真实服务可用。
- 不自动 commit、push、部署或执行超出授权的付费/破坏性操作。
