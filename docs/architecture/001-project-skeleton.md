# 易界 AI 项目骨架说明

> 文档版本：v0.1  
> 适用对象：产品、研发、AI Agent、后端、前端、桌面端、连接器、知识库、DevOps 团队  
> 项目定位：服务跨境电商卖家的 AI native TOB 产品，基于 Codex Runtime 构建跨境电商领域智能体应用  
> 技术栈：Vue、Go、Tauri、Codex Runtime、RAG、MCP/工具调用、OpenAPI/Protobuf

---

## 1. 文档目标

本文用于固化易界 AI 项目的初始工程骨架，包括：

1. 总项目 README 结构；
2. 多仓库分工与职责边界；
3. 每个仓库的标准目录；
4. 每个仓库的 README / AGENTS / ADR / 开发说明要求；
5. Codex 开发协作规范；
6. 本地开发、联调、测试、发布、安全、审计、可观测性基础约定；
7. 后续团队扩展时的文档治理方式。

本文不是某一个仓库的 README，而是整个易界 AI 多仓项目的**骨架说明文档**。建议将本文放入：

```text
yijie-workspace/docs/architecture/001-project-skeleton.md
```

同时可以将其中的模板拆分到各个仓库的 `README.md`、`AGENTS.md`、`CONTRIBUTING.md`、`SECURITY.md`、`docs/adr/` 中。

---

## 2. 项目分库结论

易界 AI 项目建议使用 11 个仓库：

```text
yijie-ai/
  01. yijie-workspace       # 项目元仓库 / 多仓入口 / 文档中心 / submodule 管理
  02. yijie-codex           # Codex 上游 fork / Agent Runtime 内核
  03. yijie-desktop         # 易界 AI Mac 桌面端，Tauri + Vue
  04. yijie-admin-web       # Admin 管理后台，Vue
  05. yijie-api             # Go 业务后端，模块化单体优先
  06. yijie-agent-host      # Codex Runtime 宿主适配层，不是自研 Agent 平台
  07. yijie-skills          # 跨境电商领域 Skills / Plugins / Prompt Packs / Evals
  08. yijie-connectors      # 电商平台与三方应用连接器，Go + MCP 工具服务
  09. yijie-knowledge       # RAG 知识库、规则库、政策库、检索服务
  10. yijie-contracts       # OpenAPI / Protobuf / JSON Schema / SDK
  11. yijie-infra           # IaC / K8s / CI/CD / 观测 / 安全配置
```

核心判断：

```text
Codex               = Agent Runtime 内核
Yijie Agent Host    = 很薄的 Runtime 宿主适配层
Yijie Skills        = 跨境电商领域智能能力
Yijie Connectors    = 外部平台 API 工具执行层
Yijie Knowledge     = RAG 知识层
Yijie API           = 易界业务系统
Yijie Desktop       = 卖家产品入口
Yijie Admin Web     = 内部运营 / 管理后台
Yijie Contracts     = 多仓 API 契约
Yijie Infra         = 云资源、部署、安全、观测
```

---

## 3. 分库原则

### 3.1 必须拆开的边界

| 边界 | 是否独立仓 | 原因 |
|---|---:|---|
| Mac 桌面端 | 是 | 卖家主产品入口，Tauri + Vue，发布、签名、升级独立 |
| Admin 管理后台 | 是 | Web 后台，权限、安全、发布节奏与桌面端完全不同 |
| Go 业务后端 | 是 | 租户、店铺授权、任务、计费、审计等核心业务域 |
| Codex Runtime | 是 | 上游 Runtime fork，需要独立 patch、构建、升级 |
| Agent Host | 是 | 业务系统与 Codex Runtime 的薄适配层 |
| Skills / Plugins | 是 | 跨境电商智能能力变化快，需要独立评测、灰度、发布 |
| Connectors | 是 | 外部平台 API、token、限流、审计、安全边界独立 |
| Knowledge / RAG | 是 | 规则、政策、法律、平台规范的更新节奏独立 |
| Contracts | 是 | 多仓共享 API 契约，避免类型和协议复制 |
| Infra | 是 | 环境、部署、观测、安全策略与业务代码解耦 |

### 3.2 明确禁止的错误做法

1. **禁止把桌面端和 admin 后台放同一个仓库。** 这两个产品运行形态、权限边界、发布节奏不同。
2. **禁止把跨境电商业务逻辑直接写进 Codex 仓库。** Codex 只作为 Runtime 内核。
3. **禁止重新自研完整 `yijie-agent-platform`。** 已决定使用 Codex 的任务编排、状态管理、上下文、提示词、可观测性机制。
4. **禁止 Codex 直接接触平台 token。** Token 必须留在业务后端或连接器的安全边界内。
5. **禁止在 MVP 阶段把 Amazon、Temu、Shopee、TikTok Shop 拆成多个连接器仓库。** 先放在 `yijie-connectors` 内按模块隔离。
6. **禁止前端、后端、连接器各自手写重复 DTO。** 统一从 `yijie-contracts` 生成。

---

## 4. 总项目 README 模板

建议放置在：

```text
yijie-workspace/README.md
```

示例内容如下。

````markdown
# 易界 AI

易界 AI 是服务跨境电商卖家的 AI native TOB 产品。卖家授权店铺权限后，易界 AI 结合店铺数据、平台规则、跨境电商 SOP 和外部平台 API，在选品、合规、Listing 优化、广告投流、物流追踪、经营分析、客户沟通等场景中提供智能体能力。

## 产品形态

当前唯一面向卖家的产品形态是：

- 易界 AI Mac 桌面端应用；
- 另有一个 Admin Web 管理后台，用于租户、权限、插件、知识库、审计和运营管理。

## 技术栈

- 桌面端：Tauri + Vue；
- Admin Web：Vue；
- 后端：Go；
- Agent Runtime：Codex Runtime；
- 连接器：Go + MCP 工具服务；
- 知识库：RAG 架构；
- API 契约：OpenAPI / Protobuf / JSON Schema；
- 基础设施：Kubernetes / Terraform / Helm / CI/CD / OpenTelemetry。

## 仓库结构

```text
yijie-ai/
  yijie-workspace
  yijie-codex
  yijie-desktop
  yijie-admin-web
  yijie-api
  yijie-agent-host
  yijie-skills
  yijie-connectors
  yijie-knowledge
  yijie-contracts
  yijie-infra
```

## 架构分层

```text
Product Experience Layer
  yijie-desktop
  yijie-admin-web

Business Platform Layer
  yijie-api

Agent Runtime Adapter Layer
  yijie-agent-host

Agent Runtime Kernel
  yijie-codex

Domain Capability Layer
  yijie-skills

Tool Execution Layer
  yijie-connectors

Knowledge Layer
  yijie-knowledge

Contract & Infra Layer
  yijie-contracts
  yijie-infra
```

## 本地启动

```bash
git clone <yijie-workspace-repo>
cd yijie-workspace
./scripts/bootstrap.sh
./scripts/dev-up.sh
```

常用命令：

```bash
./scripts/checkout-all.sh        # 拉取所有子仓
./scripts/update-submodules.sh   # 更新 submodule
./scripts/dev-up.sh              # 启动本地开发依赖
./scripts/dev-down.sh            # 停止本地开发依赖
./scripts/lint-all.sh            # 多仓 lint
./scripts/test-all.sh            # 多仓测试
```

## 文档入口

```text
docs/
  architecture/      # 架构文档
  adr/               # 架构决策记录
  product/           # 产品与跨境电商 SOP
  dev/               # 开发说明
  security/          # 安全规范
  runbook/           # 运维手册
  release/           # 发布规范
```

## Codex 开发约定

本项目全部使用 Codex 辅助开发。每个仓库必须包含：

```text
AGENTS.md
.codex/
  config.toml
  prompts/
  tasks/
```

Codex 修改代码时必须遵循对应仓库的 `AGENTS.md`。

## 安全红线

- 不得提交任何平台 token、secret、cookie、access key；
- Codex Runtime 不得直接持有商家平台 token；
- 高风险写操作必须经过 approval policy；
- 所有外部平台 API 调用必须有审计日志；
- 所有日志必须做 PII 和密钥脱敏；
- 所有 API 契约变更必须先更新 `yijie-contracts`。

## 仓库 Owner

| 仓库 | Owner |
|---|---|
| yijie-workspace | Platform Team |
| yijie-codex | Agent Runtime Team |
| yijie-desktop | Client Team |
| yijie-admin-web | Admin Platform Team |
| yijie-api | Backend Team |
| yijie-agent-host | Agent Runtime Team |
| yijie-skills | AI Product Team |
| yijie-connectors | Integration Team |
| yijie-knowledge | Data AI Team |
| yijie-contracts | Platform Team |
| yijie-infra | DevOps Team |
````

---

## 5. 项目元仓库：`yijie-workspace`

### 5.1 仓库职责

`yijie-workspace` 是整个易界 AI 的项目入口，不放具体业务代码，主要负责：

1. 管理多仓结构；
2. 管理 submodule 或 repo manifest；
3. 承载顶层架构文档；
4. 承载跨仓 ADR；
5. 提供本地开发一键启动脚本；
6. 统一多仓代码规范、提交规范、发布规范；
7. 作为新人 onboarding 入口。

### 5.2 不负责

`yijie-workspace` 不负责：

- 具体业务代码；
- Codex Runtime 源码；
- 前端应用代码；
- Go 服务代码；
- 平台连接器实现；
- RAG 检索实现。

### 5.3 推荐目录

```text
yijie-workspace/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  CODEOWNERS
  repos.yaml
  .gitmodules

  docs/
    architecture/
      000-overview.md
      001-project-skeleton.md
      002-repo-strategy.md
      003-agent-runtime.md
      004-security-boundary.md
      005-data-flow.md
      006-release-strategy.md
      007-observability.md
    adr/
      README.md
      ADR-0001-use-codex-runtime.md
      ADR-0002-split-desktop-and-admin.md
      ADR-0003-skills-outside-codex-core.md
      ADR-0004-contract-first-api.md
      ADR-0005-token-boundary-and-approval-policy.md
    product/
      seller-sop-map.md
      ecommerce-platform-scope.md
      ai-native-ux-principles.md
      mvp-scope.md
    dev/
      local-development.md
      code-style.md
      testing.md
      debugging.md
      codex-development.md
      branch-and-release.md
    security/
      security-model.md
      data-classification.md
      secret-management.md
      audit-policy.md
      approval-policy.md
    runbook/
      local-env-troubleshooting.md
      connector-failure.md
      agent-runtime-failure.md
      knowledge-ingestion-failure.md
    release/
      desktop-release.md
      backend-release.md
      skills-release.md
      codex-runtime-upgrade.md

  scripts/
    bootstrap.sh
    checkout-all.sh
    update-submodules.sh
    dev-up.sh
    dev-down.sh
    lint-all.sh
    test-all.sh
    generate-all.sh

  codex/
    yijie-codex/

  apps/
    yijie-desktop/
    yijie-admin-web/

  services/
    yijie-api/
    yijie-agent-host/
    yijie-connectors/
    yijie-knowledge/

  packages/
    yijie-skills/
    yijie-contracts/

  platform/
    yijie-infra/
```

### 5.4 `repos.yaml` 示例

```yaml
repos:
  - name: yijie-codex
    path: codex/yijie-codex
    type: runtime
    owner: agent-runtime-team

  - name: yijie-desktop
    path: apps/yijie-desktop
    type: app
    owner: client-team

  - name: yijie-admin-web
    path: apps/yijie-admin-web
    type: app
    owner: admin-platform-team

  - name: yijie-api
    path: services/yijie-api
    type: backend
    owner: backend-team

  - name: yijie-agent-host
    path: services/yijie-agent-host
    type: runtime-adapter
    owner: agent-runtime-team

  - name: yijie-skills
    path: packages/yijie-skills
    type: ai-capabilities
    owner: ai-product-team

  - name: yijie-connectors
    path: services/yijie-connectors
    type: platform-connectors
    owner: integration-team

  - name: yijie-knowledge
    path: services/yijie-knowledge
    type: rag
    owner: data-ai-team

  - name: yijie-contracts
    path: packages/yijie-contracts
    type: contracts
    owner: platform-team

  - name: yijie-infra
    path: platform/yijie-infra
    type: infra
    owner: devops-team
```

---

## 6. Codex Runtime 仓库：`yijie-codex`

### 6.1 仓库职责

`yijie-codex` 是 Codex 上游源码的易界 fork，用作易界 AI 的 Agent Runtime 内核。

它负责：

1. 同步 Codex 上游源码；
2. 管理易界必要 patch；
3. 构建 Codex runtime binary / app-server；
4. 维护 runtime 兼容性测试；
5. 暴露给 `yijie-agent-host` 使用的 app-server 能力；
6. 管理 runtime 安全策略和默认配置。

### 6.2 不负责

`yijie-codex` 不负责：

- Listing 优化业务；
- 广告投流业务；
- 平台 API 调用；
- RAG 知识库；
- 店铺授权；
- 租户、计费、审计；
- 易界业务 prompt；
- 跨境电商领域 skill。

### 6.3 推荐目录

```text
yijie-codex/
  README.md
  AGENTS.md
  UPSTREAM.md
  CHANGELOG.yijie.md
  SECURITY.md

  codex-rs/
    app-server/
    core/
    protocol/
    cli/
    tui/
    mcp-server/
    ...

  docs/
    yijie-integration.md
    yijie-patch-policy.md
    upstream-sync.md
    runtime-security.md
    runtime-compatibility.md

  .yijie/
    patches/
      0001-runtime-policy-hooks.patch
      0002-app-server-compatibility.patch
    build/
      macos/
        build-codex-sidecar.sh
      linux/
        build-cloud-runner.sh
    config/
      desktop-default.config.toml
      cloud-runner.config.toml
      test.config.toml
    schemas/
      app-server/
        generated-ts/
        generated-json-schema/

  scripts/
    sync-upstream.sh
    apply-yijie-patches.sh
    build-all.sh
    test-runtime.sh
```

### 6.4 README 必须说明

```markdown
# yijie-codex

本仓库是 Codex Runtime 的易界 fork。它只作为易界 AI 的 Agent Runtime 内核，不承载跨境电商业务逻辑。

## 职责

- 同步上游 Codex；
- 管理易界 runtime patch；
- 构建桌面端和云端 runner 所需 binary；
- 维护 app-server 协议兼容性；
- 输出 runtime 版本给 yijie-agent-host 使用。

## 禁止事项

- 禁止写入跨境电商业务逻辑；
- 禁止写入平台 API token 处理逻辑；
- 禁止写入 Listing / Ads / Compliance 等领域 prompt；
- 禁止破坏上游目录结构。

## 上游同步流程

1. 拉取上游 tag；
2. 执行 `scripts/sync-upstream.sh`；
3. 执行 `scripts/apply-yijie-patches.sh`；
4. 执行 runtime 测试；
5. 更新 `CHANGELOG.yijie.md`；
6. 通知 `yijie-agent-host` 做兼容性验证。
```

---

## 7. 桌面端仓库：`yijie-desktop`

### 7.1 仓库职责

`yijie-desktop` 是易界 AI 面向卖家的唯一客户端，运行形态是 Mac OS 桌面应用。

它负责：

1. 卖家登录；
2. 店铺授权引导；
3. Chat 对话流；
4. Agent 任务进度展示；
5. 工具调用审批；
6. 任务结果展示；
7. 插件市场展示；
8. 本地 sidecar 进程管理；
9. Mac App 打包、签名、升级；
10. 本地安全存储。

### 7.2 不负责

`yijie-desktop` 不负责：

- Admin 管理后台；
- 业务后端状态机；
- 平台 API token 管理；
- 连接器实现；
- RAG 检索实现；
- Codex 源码维护。

### 7.3 推荐目录

```text
yijie-desktop/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  package.json
  pnpm-lock.yaml
  vite.config.ts
  tsconfig.json
  index.html

  .codex/
    config.toml
    prompts/
      desktop-dev.md
    tasks/
      implement-page.md
      fix-ui-bug.md
      add-tauri-command.md

  docs/
    architecture.md
    local-development.md
    tauri-sidecar.md
    desktop-release.md
    adr/
      ADR-0001-tauri-vue-structure.md
      ADR-0002-sidecar-process-model.md

  src/
    main.ts
    App.vue
    app/
    router/
    stores/
    pages/
      login/
      onboarding/
      chat/
      tasks/
      stores/
      listing/
      ads/
      compliance/
      logistics/
      analytics/
      plugins/
      settings/
    components/
    composables/
    api/
    domain/
    assets/
    i18n/
    styles/

  src-tauri/
    Cargo.toml
    tauri.conf.json
    capabilities/
    icons/
    src/
      main.rs
      commands/
      runtime/
      security/
      system/

  sidecars/
    macos/
      codex/
      yijie-agent-host/

  tests/
    unit/
    e2e/
    fixtures/

  scripts/
    dev.sh
    build-macos.sh
    package-dmg.sh
    notarize.sh
    release.sh
```

### 7.4 README 必须说明

````markdown
# yijie-desktop

易界 AI Mac 桌面端，面向跨境电商卖家。

## 核心能力

- Chat 对话流；
- 店铺授权；
- Agent 任务执行与进度展示；
- 工具调用审批；
- Listing、广告、合规、物流、经营分析等工作台；
- 本地 Codex / Agent Host sidecar 管理；
- Mac App 签名、打包、自动更新。

## 本地开发

```bash
pnpm install
pnpm dev
```

Tauri 开发：

```bash
pnpm tauri dev
```

## 安全要求

- 不得在前端持久化平台 access token；
- 本地敏感信息必须使用系统 Keychain；
- 所有高风险 agent 操作必须展示审批卡片；
- 不得绕过后端权限校验直接调用连接器。
````

---

## 8. Admin 后台仓库：`yijie-admin-web`

### 8.1 仓库职责

`yijie-admin-web` 是易界内部管理后台。

它负责：

1. 租户管理；
2. 用户与 RBAC；
3. 店铺授权查看与撤销；
4. 平台 API 配置；
5. Skill / Plugin 上架、版本、灰度；
6. 知识库数据源、版本、入库任务管理；
7. Agent 任务审计；
8. 工具调用审计；
9. 计费套餐；
10. 系统运行状态。

### 8.2 不负责

`yijie-admin-web` 不负责：

- 卖家桌面端体验；
- 桌面端 sidecar 管理；
- 连接器执行逻辑；
- 知识库入库和检索实现；
- Codex Runtime 维护。

### 8.3 推荐目录

```text
yijie-admin-web/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  package.json
  pnpm-lock.yaml
  vite.config.ts
  tsconfig.json
  index.html

  .codex/
    config.toml
    prompts/
      admin-dev.md
    tasks/
      implement-admin-page.md
      add-permission-check.md

  docs/
    architecture.md
    local-development.md
    permission-model.md
    adr/
      ADR-0001-admin-rbac-model.md

  src/
    main.ts
    App.vue
    app/
    router/
    stores/
    pages/
      login/
      dashboard/
      tenants/
      users/
      rbac/
      stores/
      platforms/
      agent/
      skills/
      plugins/
      knowledge/
      audit/
      billing/
      ops/
    components/
    api/
    domain/
    assets/
    i18n/
    styles/

  tests/
    unit/
    e2e/

  scripts/
    dev.sh
    build.sh
    release.sh
```

---

## 9. Go 业务后端仓库：`yijie-api`

### 9.1 仓库职责

`yijie-api` 是易界 AI 的核心业务后端。MVP 阶段建议采用模块化单体，后续再按业务压力拆服务。

它负责：

1. 用户认证；
2. 租户管理；
3. RBAC；
4. 店铺授权业务；
5. 会话与任务；
6. Agent session 元数据；
7. 审批策略；
8. 业务工作台 API；
9. 插件注册；
10. 知识库版本注册；
11. 计费与用量；
12. 审计日志；
13. Webhook；
14. 与 `yijie-agent-host`、`yijie-connectors`、`yijie-knowledge` 的服务间调用。

### 9.2 不负责

`yijie-api` 不负责：

- 具体平台 API 调用细节；
- Codex Runtime 内部状态管理；
- Skill prompt；
- RAG chunking / embedding；
- 桌面端 UI；
- Admin UI。

### 9.3 推荐目录

```text
yijie-api/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  go.mod
  go.sum
  Makefile

  .codex/
    config.toml
    prompts/
      backend-dev.md
    tasks/
      add-module.md
      add-api.md
      write-tests.md

  docs/
    architecture.md
    local-development.md
    module-guideline.md
    database-guideline.md
    api-guideline.md
    adr/
      ADR-0001-modular-monolith.md
      ADR-0002-transaction-boundary.md
      ADR-0003-audit-first-design.md

  cmd/
    api-server/
    admin-server/
    worker/
    scheduler/
    webhook-server/

  api/
    openapi/
      public.yaml
      admin.yaml
      internal.yaml
    protobuf/
    asyncapi/

  internal/
    app/
    modules/
      auth/
      tenant/
      user/
      rbac/
      storeauth/
      chat/
      task/
      agent_session/
      approval/
      listing/
      ads/
      analytics/
      notification/
      plugin_registry/
      knowledge_registry/
      billing/
      audit/
      webhook/
    platform/
      database/
      redis/
      queue/
      objectstorage/
      secret/
      eventbus/
      config/
      logger/
      metrics/
      tracing/
      errors/
      idgen/
      crypto/
      rate_limit/
      idempotency/
    clients/
      agent_host/
      connectors/
      knowledge/
      payment/
      email/
      sms/

  migrations/
  configs/
  deploy/
  tests/
    unit/
    integration/
    contract/
    fixtures/
  scripts/
```

### 9.4 模块目录标准

每个业务模块推荐使用：

```text
module-name/
  domain/             # 实体、值对象、领域服务、领域事件
  application/        # 用例、命令、查询、事务编排
  infrastructure/     # DB、外部服务、repository 实现
  interfaces/         # HTTP handler、DTO、mapper
```

示例：

```text
storeauth/
  domain/
    store.go
    platform.go
    permission.go
    token_status.go
  application/
    connect_store_usecase.go
    refresh_token_usecase.go
    revoke_store_usecase.go
  infrastructure/
    store_repository_pg.go
    token_vault_client.go
  interfaces/
    http_handler.go
    dto.go
    mapper.go
```

---

## 10. Codex 宿主适配层仓库：`yijie-agent-host`

### 10.1 仓库职责

`yijie-agent-host` 是易界业务系统与 Codex Runtime 之间的薄适配层。

它负责：

1. 启动或连接 Codex app-server；
2. 维护 `yijie_task_id` 与 `codex_thread_id` 映射；
3. 加载易界 skills / plugins；
4. 生成 MCP 工具配置；
5. 把 Codex 事件转成易界任务事件；
6. 执行租户权限校验；
7. 执行工具调用审批策略；
8. 做 token 边界控制；
9. 做日志脱敏；
10. 作为桌面端 sidecar 和云端 runner 的统一宿主。

### 10.2 不负责

`yijie-agent-host` 不负责：

- 自研 Agent planner；
- 自研任务编排系统；
- 自研 prompt engine；
- 直接实现 Amazon / Temu / Shopee / TikTok Shop API；
- 直接实现 RAG 检索；
- 承载业务数据库主状态。

### 10.3 推荐目录

```text
yijie-agent-host/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  go.mod
  go.sum
  Makefile

  .codex/
    config.toml
    prompts/
      agent-host-dev.md
    tasks/
      add-codex-event-mapping.md
      add-approval-policy.md

  docs/
    architecture.md
    codex-app-server-integration.md
    sidecar-mode.md
    cloud-runner-mode.md
    policy-model.md
    event-model.md
    adr/
      ADR-0001-thin-host-not-agent-platform.md
      ADR-0002-task-thread-mapping.md
      ADR-0003-tool-approval-boundary.md

  cmd/
    desktop-host/
    cloud-runner/
    runtime-healthcheck/

  api/
    openapi/
      agent-host.yaml
    protobuf/
      agent_host.proto
    schemas/
      codex-events.json
      yijie-agent-events.json

  internal/
    app/
    codex/
      process/
      appserver/
      schema/
      version/
    session/
    workspace/
    policy/
    skills/
    plugins/
    tools/
    context/
    events/
    telemetry/
    security/
    clients/
      yijie_api/
      connectors/
      knowledge/

  configs/
    desktop/
    cloud/

  deploy/
  tests/
  scripts/
```

### 10.4 README 必须说明

```markdown
# yijie-agent-host

本仓库是易界 AI 对 Codex Runtime 的宿主适配层。它不是自研 Agent 平台。

## 核心边界

允许：

- 管理 Codex Runtime 进程；
- 连接 Codex app-server；
- 映射业务 task 和 Codex thread；
- 注入上下文；
- 加载 skills；
- 写入 MCP 配置；
- 转发事件；
- 执行审批策略；
- 执行安全边界。

禁止：

- 自研 planner；
- 自研任务编排；
- 直接写跨境电商业务逻辑；
- 直接处理平台 token；
- 直接调用平台 API。
```

---

## 11. Skills / Plugins 仓库：`yijie-skills`

### 11.1 仓库职责

`yijie-skills` 是易界 AI 的跨境电商领域能力资产库。

它负责：

1. Codex skills；
2. Codex plugins；
3. Prompt packs；
4. MCP tool manifests；
5. 输出 JSON Schema；
6. 跨境电商 SOP；
7. Agent eval 数据集；
8. Golden cases；
9. Rubrics；
10. 插件市场元信息；
11. Skill 版本、灰度、发布包。

### 11.2 不负责

`yijie-skills` 不负责：

- 真实商家数据；
- 平台 access token；
- 外部平台 API 客户端；
- 数据库访问；
- Codex Runtime 源码；
- 桌面端 UI；
- 后端业务状态。

### 11.3 推荐目录

```text
yijie-skills/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md

  .codex/
    config.toml
    prompts/
      skill-dev.md
    tasks/
      create-skill.md
      improve-prompt.md
      add-eval.md

  docs/
    skill-authoring.md
    plugin-authoring.md
    prompt-style-guide.md
    eval-guideline.md
    release-guideline.md
    adr/
      ADR-0001-skill-package-format.md
      ADR-0002-eval-required-before-release.md

  marketplace/
    yijie-marketplace.toml
    README.md

  plugins/
    amazon-listing-optimizer/
      plugin.toml
      README.md
      skills/
        listing-diagnosis/
          SKILL.md
          examples/
          checklists/
        listing-rewrite/
          SKILL.md
          examples/
        keyword-research/
          SKILL.md
          examples/
      mcp/
        servers.toml
        tools.md
      prompts/
      evals/
      tests/

    amazon-ads-optimizer/
    temu-compliance-checker/
    shopee-store-operator/
    tiktok-shop-content-optimizer/
    logistics-tracking-agent/
    store-analytics-agent/
    compliance-research-agent/
    third-party-ops-agent/

  shared/
    ecommerce-sop/
    output-schemas/
    prompt-parts/
    rubrics/

  evals/
    runner/
    reports/
    datasets/
      listing/
      compliance/
      ads/
      logistics/
      analytics/

  tools/
    local-debug/
    prompt-lint/
    skill-packager/

  scripts/
    lint-skills.sh
    package-plugin.sh
    run-evals.sh
    publish-marketplace.sh
```

### 11.4 Skill 标准结构

每个 skill 必须包含：

```text
skill-name/
  SKILL.md
  examples/
    input-001.json
    output-001.json
  checklists/
    quality-checklist.md
  evals/
    dataset.jsonl
    rubric.md
  tests/
```

`SKILL.md` 必须包含：

```markdown
# Skill Name

## 目标
说明这个 skill 解决什么跨境电商场景。

## 适用场景
说明用户在什么情况下调用。

## 输入
说明需要哪些输入，例如商品链接、店铺数据、平台、站点、类目、目标语言。

## 输出
说明输出结构，并引用 JSON Schema。

## 可调用工具
列出允许调用的 MCP 工具。

## 禁止行为
说明哪些操作不能做，例如直接发布商品、直接改价、直接调广告预算。

## 审批要求
说明哪些动作需要用户审批。

## 失败处理
说明数据不足、平台 API 失败、知识库无结果时如何处理。

## 示例
给出输入输出示例。

## 评测标准
说明质量 rubrics。
```

---

## 12. 连接器仓库：`yijie-connectors`

### 12.1 仓库职责

`yijie-connectors` 是外部平台 API 和三方应用的工具执行层。

它负责：

1. Amazon、Temu、Shopee、TikTok Shop 等电商平台 API；
2. 物流服务商 API；
3. 邮箱 API；
4. 飞书、钉钉；
5. LinkedIn 等三方应用；
6. MCP 工具服务；
7. OAuth / token vault / token refresh；
8. API 限流、重试、熔断；
9. 幂等；
10. 高风险操作 guard；
11. 外部 API 审计日志。

### 12.2 不负责

`yijie-connectors` 不负责：

- 用户产品 UI；
- 业务主状态；
- Codex Runtime；
- Skills prompt；
- RAG 检索；
- 租户套餐和计费规则。

### 12.3 推荐目录

```text
yijie-connectors/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  go.mod
  go.sum
  Makefile

  .codex/
    config.toml
    prompts/
      connector-dev.md
    tasks/
      add-platform-tool.md
      add-mcp-server.md
      add-api-client.md

  docs/
    architecture.md
    connector-guideline.md
    mcp-tool-guideline.md
    token-security.md
    idempotency.md
    rate-limit.md
    audit-log.md
    adr/
      ADR-0001-single-connectors-repo.md
      ADR-0002-token-vault-boundary.md
      ADR-0003-mcp-tool-execution-contract.md

  cmd/
    connector-gateway/
    mcp-amazon/
    mcp-temu/
    mcp-shopee/
    mcp-tiktok-shop/
    mcp-logistics/
    mcp-email/
    mcp-feishu/
    mcp-dingtalk/
    mcp-linkedin/
    sync-worker/
    webhook-server/

  api/
    openapi/
      connectors.yaml
    mcp/
      amazon.tools.json
      temu.tools.json
      shopee.tools.json
      tiktok-shop.tools.json
      logistics.tools.json
      email.tools.json
      feishu.tools.json
      dingtalk.tools.json
      linkedin.tools.json

  internal/
    gateway/
    platforms/
      amazon/
      temu/
      shopee/
      tiktokshop/
    third_party/
      logistics/
      email/
      feishu/
      dingtalk/
      linkedin/
    auth/
      oauth/
      token_vault/
      permission_scope/
      refresh_token/
      credential_rotation/
    mcp/
    safety/
    reliability/
    audit/
    platform/
      database/
      redis/
      queue/
      secret/
      logger/
      metrics/
      tracing/

  configs/
  deploy/
  tests/
  scripts/
```

### 12.4 高风险操作

以下操作必须强制走审批策略：

| 操作 | 风险 |
|---|---|
| 发布或下架 listing | 影响商品销售 |
| 修改标题、图片、描述、变体 | 影响流量和合规 |
| 修改价格 | 影响收入与利润 |
| 修改库存 | 影响履约和排名 |
| 修改广告预算 | 影响资金消耗 |
| 暂停或开启广告活动 | 影响投放效果 |
| 给买家发送消息 | 影响客服和合规 |
| 批量操作订单 | 影响履约和售后 |

---

## 13. 知识库仓库：`yijie-knowledge`

### 13.1 仓库职责

`yijie-knowledge` 是易界 AI 的 RAG 知识层。

它负责：

1. 平台规则源管理；
2. 法律政策源管理；
3. 文档抓取；
4. 文档解析；
5. 文档清洗；
6. chunking；
7. embedding；
8. 索引；
9. 检索；
10. rerank；
11. citation；
12. 版本管理；
13. freshness 检查；
14. RAG eval。

### 13.2 不负责

`yijie-knowledge` 不负责：

- 业务主状态；
- 外部平台 API 写操作；
- Codex Runtime；
- 桌面端 UI；
- Admin UI；
- 计费逻辑。

### 13.3 推荐目录

```text
yijie-knowledge/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  go.mod
  go.sum
  Makefile

  .codex/
    config.toml
    prompts/
      knowledge-dev.md
    tasks/
      add-source.md
      improve-retrieval.md
      add-rag-eval.md

  docs/
    architecture.md
    ingestion-guideline.md
    retrieval-guideline.md
    citation-guideline.md
    freshness-policy.md
    rag-eval-guideline.md
    adr/
      ADR-0001-rag-source-versioning.md
      ADR-0002-hybrid-search-first.md
      ADR-0003-citation-required-for-policy-answer.md

  cmd/
    knowledge-api/
    ingestor/
    scheduler/
    retriever/
    admin-tool/

  api/
    openapi/
      knowledge.yaml
    schemas/
      document.schema.json
      chunk.schema.json
      retrieval-result.schema.json
      citation.schema.json

  internal/
    sources/
      amazon/
      temu/
      shopee/
      tiktokshop/
      country_laws/
      logistics/
      tax/
      prohibited_items/
      customs/
    ingestion/
      crawler/
      parser/
      normalizer/
      splitter/
      chunker/
      embedder/
      deduper/
      versioner/
      validator/
    retrieval/
      hybrid_search.go
      vector_search.go
      keyword_search.go
      reranker.go
      citation_builder.go
      answer_context_builder.go
    policy/
    jobs/
    admin/
    platform/
      database/
      vectorstore/
      objectstorage/
      queue/
      logger/
      metrics/
      tracing/

  configs/
    sources/
    retrieval/

  data/
    seed/
    samples/
    fixtures/

  migrations/
  deploy/
  tests/
  scripts/
```

---

## 14. API 契约仓库：`yijie-contracts`

### 14.1 仓库职责

`yijie-contracts` 是多仓协作的协议中心。

它负责：

1. OpenAPI；
2. Protobuf；
3. AsyncAPI；
4. JSON Schema；
5. TypeScript SDK；
6. Go SDK；
7. Codex app-server 兼容 schema；
8. breaking change 检查。

### 14.2 不负责

`yijie-contracts` 不负责：

- 具体业务实现；
- 数据库实现；
- 前端页面；
- Runtime 逻辑；
- 部署配置。

### 14.3 推荐目录

```text
yijie-contracts/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  package.json
  go.mod
  Makefile

  .codex/
    config.toml
    prompts/
      contracts-dev.md
    tasks/
      add-openapi.md
      add-protobuf.md
      check-breaking-change.md

  docs/
    api-design-guideline.md
    versioning.md
    sdk-generation.md
    breaking-change-policy.md
    adr/
      ADR-0001-contract-first-development.md
      ADR-0002-openapi-for-http-protobuf-for-events.md

  openapi/
    public/
    admin/
    internal/

  protobuf/
    yijie/
      common/
      events/
      services/

  asyncapi/
    events.yaml
    topics/

  jsonschema/
    chat/
    task/
    agent/
    skills/
    ecommerce/

  sdks/
    typescript/
    go/
    generated/

  codex/
    app-server/
      version-lock.json
      generated-ts/
      generated-json-schema/

  scripts/
    lint-openapi.sh
    generate-ts-sdk.sh
    generate-go-sdk.sh
    generate-all.sh
    breaking-change-check.sh

  tests/
    contract/
```

### 14.4 契约优先流程

```text
需求提出
  -> 修改 yijie-contracts
  -> 生成 SDK
  -> yijie-api 实现
  -> yijie-desktop / yijie-admin-web 接入
  -> contract tests
  -> release
```

---

## 15. Infra 仓库：`yijie-infra`

### 15.1 仓库职责

`yijie-infra` 是易界 AI 的基础设施仓库。

它负责：

1. Terraform；
2. Kubernetes；
3. Helm；
4. Docker base images；
5. CI/CD 模板；
6. 环境配置；
7. 观测配置；
8. 安全策略；
9. 回滚脚本；
10. 灾备与运行手册。

### 15.2 不负责

`yijie-infra` 不负责：

- 业务代码；
- 前端页面；
- Skill prompt；
- Codex Runtime 源码；
- 平台连接器业务实现。

### 15.3 推荐目录

```text
yijie-infra/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md

  .codex/
    config.toml
    prompts/
      infra-dev.md
    tasks/
      add-service-deploy.md
      add-alert-rule.md
      update-terraform.md

  docs/
    architecture.md
    environment.md
    deployment.md
    rollback.md
    observability.md
    security.md
    adr/
      ADR-0001-environment-separation.md
      ADR-0002-observability-baseline.md

  terraform/
    modules/
      network/
      postgres/
      redis/
      object-storage/
      vector-db/
      queue/
      secrets/
      observability/
    envs/
      dev/
      staging/
      prod/

  kubernetes/
    namespaces/
    base/
    overlays/
      dev/
      staging/
      prod/

  helm/
    yijie-api/
    yijie-agent-host/
    yijie-connectors/
    yijie-knowledge/
    yijie-admin-web/
    common/

  docker/
    base/

  ci/
    github-actions/
    scripts/

  observability/
    grafana/
    prometheus/
    otel/
    loki/
    alerts/

  security/
    iam/
    secret-policy/
    network-policy/
    runtime-policy/
    audit-policy/
    data-retention/
    pii-redaction/

  environments/
    dev.yaml
    staging.yaml
    prod.yaml

  scripts/
    plan.sh
    apply.sh
    deploy.sh
    rollback.sh
```

---

## 16. 每个仓库都必须有的标准文件

所有仓库必须包含：

```text
README.md
AGENTS.md
CONTRIBUTING.md
SECURITY.md
CHANGELOG.md
CODEOWNERS
.gitignore
.env.example
Makefile 或 scripts/
docs/
  architecture.md
  local-development.md
  adr/
.codex/
  config.toml
  prompts/
  tasks/
tests/
```

### 16.1 `README.md` 必须包含

```markdown
# 仓库名称

## 仓库职责

## 不负责什么

## 技术栈

## 目录结构

## 本地开发

## 测试

## 构建

## 发布

## 依赖仓库

## 安全要求

## Codex 开发说明

## Owner
```

### 16.2 `AGENTS.md` 必须包含

````markdown
# AGENTS.md

## 仓库职责

说明这个仓库做什么。

## 禁止事项

说明 Codex 不能做什么。

## 技术栈

说明语言、框架、包管理器、测试工具。

## 目录约定

说明代码应该放在哪里。

## 开发命令

```bash
make dev
make test
make lint
make generate
```

## 测试要求

说明修改后必须运行哪些测试。

## 安全要求

说明密钥、token、PII、日志、审批等规则。

## API 契约要求

说明是否必须先改 `yijie-contracts`。

## PR 要求

- 必须更新测试；
- 必须更新文档；
- 涉及 API 必须更新 contract；
- 涉及 DB 必须更新 migration；
- 涉及高风险工具必须更新 approval policy。
````

### 16.3 `CONTRIBUTING.md` 必须包含

```markdown
# Contributing

## 开发流程

1. 从 main 拉分支；
2. 修改代码；
3. 运行测试；
4. 更新文档；
5. 提交 PR；
6. Code Review；
7. CI 通过后合并。

## 分支命名

- feature/<scope>-<desc>
- fix/<scope>-<desc>
- chore/<scope>-<desc>
- refactor/<scope>-<desc>

## Commit 规范

- feat: 新功能
- fix: 修复
- docs: 文档
- refactor: 重构
- test: 测试
- chore: 工程化
- security: 安全修复

## PR 检查项

- [ ] 是否更新测试
- [ ] 是否更新文档
- [ ] 是否涉及 API contract
- [ ] 是否涉及 DB migration
- [ ] 是否涉及安全边界
- [ ] 是否涉及高风险工具调用
```

### 16.4 `SECURITY.md` 必须包含

```markdown
# Security Policy

## 密钥管理

禁止提交：

- 平台 access token；
- refresh token；
- cookie；
- private key；
- 数据库密码；
- OpenAI/API key；
- 云厂商 access key。

## 数据分类

- Public：公开文档；
- Internal：内部配置；
- Confidential：商家经营数据；
- Restricted：平台 token、PII、财务数据。

## 日志规范

日志必须脱敏：

- token；
- email；
- 电话；
- 地址；
- 订单号；
- 买家信息；
- 店铺敏感经营数据。

## 高风险操作

涉及价格、库存、广告预算、listing 发布、买家消息等操作必须经过审批。

## 漏洞响应

发现安全问题后必须通知 Security Owner，并创建 private security issue。
```

---

## 17. ADR 目录规范

ADR 是 Architecture Decision Record，用于记录关键架构决策。

### 17.1 顶层 ADR

放置在：

```text
yijie-workspace/docs/adr/
```

用于记录跨仓、跨团队、长期影响的架构决策。

建议初始 ADR：

```text
ADR-0001-use-codex-runtime.md
ADR-0002-split-desktop-and-admin.md
ADR-0003-skills-outside-codex-core.md
ADR-0004-contract-first-api.md
ADR-0005-token-boundary-and-approval-policy.md
ADR-0006-modular-monolith-first.md
ADR-0007-single-connectors-repo-first.md
ADR-0008-rag-knowledge-service-boundary.md
ADR-0009-admin-web-as-independent-repo.md
ADR-0010-desktop-sidecar-runtime-model.md
```

### 17.2 仓库内 ADR

每个仓库可以有自己的局部 ADR：

```text
repo-name/docs/adr/
```

用于记录只影响该仓库的技术决策。

### 17.3 ADR 模板

```markdown
# ADR-000X: 决策标题

## 状态

Proposed | Accepted | Deprecated | Superseded

## 日期

YYYY-MM-DD

## 背景

说明为什么需要做这个决策。

## 决策

说明最终选择了什么方案。

## 备选方案

### 方案 A

优点：

缺点：

### 方案 B

优点：

缺点：

## 影响

说明对仓库、团队、发布、安全、成本的影响。

## 风险

说明可能的问题。

## 后续动作

- [ ] 动作 1
- [ ] 动作 2
```

### 17.4 初始 ADR 示例

```markdown
# ADR-0001: 使用 Codex Runtime 作为易界 AI 的 Agent Runtime 内核

## 状态

Accepted

## 日期

YYYY-MM-DD

## 背景

易界 AI 是跨境电商领域的 AI native 应用，需要 agent 具备任务执行、上下文管理、工具调用、状态管理、可观测性等能力。团队决定不从 0 自研完整 agent platform，而是基于 Codex Runtime 构建。

## 决策

采用 Codex Runtime 作为易界 AI 的 Agent Runtime 内核。易界保留一个很薄的 `yijie-agent-host`，用于连接业务系统与 Codex Runtime。

## 备选方案

### 方案 A：自研 yijie-agent-platform

优点：完全可控。

缺点：研发成本高、演进慢、容易重复造轮子。

### 方案 B：使用 Codex Runtime

优点：复用已有 agent runtime 能力，聚焦跨境电商业务价值。

缺点：需要管理上游同步、兼容性和 patch。

## 影响

- 必须独立维护 `yijie-codex`；
- 必须独立维护 `yijie-agent-host`；
- 领域能力必须放到 `yijie-skills`、`yijie-connectors`、`yijie-knowledge`；
- 不允许把业务逻辑写进 Codex 内核。

## 后续动作

- [ ] 创建 `yijie-codex` fork；
- [ ] 创建 `yijie-agent-host`；
- [ ] 定义 runtime compatibility tests；
- [ ] 定义上游同步流程。
```

---

## 18. Codex 开发规范

项目全部使用 Codex 开发，因此需要明确 Codex 的行为边界。

### 18.1 每仓 Codex 配置

每个仓库必须包含：

```text
.codex/
  config.toml
  prompts/
    dev.md
    review.md
    test.md
  tasks/
    implement-feature.md
    fix-bug.md
    write-tests.md
    refactor.md
```

### 18.2 Codex 修改代码前必须读取

Codex 在每个仓工作前必须读取：

```text
README.md
AGENTS.md
CONTRIBUTING.md
SECURITY.md
docs/architecture.md
```

如果涉及 API，必须读取：

```text
yijie-contracts/openapi/
yijie-contracts/protobuf/
yijie-contracts/jsonschema/
```

如果涉及高风险工具调用，必须读取：

```text
docs/security/approval-policy.md
```

### 18.3 Codex 禁止行为

Codex 禁止：

1. 生成真实 token、secret、cookie；
2. 把密钥写入代码或文档；
3. 绕过审批策略；
4. 在 `yijie-codex` 中写业务逻辑；
5. 在 `yijie-agent-host` 中重建完整 agent platform；
6. 在前端持久化平台 access token；
7. 未更新 contract 就修改接口；
8. 未更新测试就修改核心业务逻辑；
9. 未写 migration 就修改数据库结构；
10. 将真实商家数据写入 fixtures。

### 18.4 Codex 任务模板

```markdown
# Task: 实现功能

## 背景

说明业务背景。

## 目标

说明本次要完成什么。

## 影响仓库

- yijie-contracts
- yijie-api
- yijie-desktop

## 约束

- 先改 contract；
- 不得引入真实 token；
- 高风险操作必须走 approval；
- 必须补测试。

## 验收标准

- [ ] API 契约已更新；
- [ ] 后端实现已完成；
- [ ] 前端页面已接入；
- [ ] 单元测试通过；
- [ ] 集成测试通过；
- [ ] 文档已更新。
```

---

## 19. 本地开发说明

### 19.1 基础依赖

本地开发建议准备：

```text
Git
Go
Node.js
pnpm
Rust
Tauri prerequisites
Docker
Docker Compose
PostgreSQL client
Redis client
Make
```

### 19.2 多仓初始化

```bash
git clone <yijie-workspace-repo>
cd yijie-workspace
./scripts/bootstrap.sh
./scripts/checkout-all.sh
```

### 19.3 启动本地依赖

```bash
./scripts/dev-up.sh
```

本地依赖包括：

```text
PostgreSQL
Redis
Object Storage Mock
Vector DB / Vector Store Mock
Queue
OpenTelemetry Collector
Mock Platform API
```

### 19.4 启动后端

```bash
cd services/yijie-api
make dev
```

### 19.5 启动 Agent Host

```bash
cd services/yijie-agent-host
make dev
```

### 19.6 启动连接器

```bash
cd services/yijie-connectors
make dev
```

### 19.7 启动知识库

```bash
cd services/yijie-knowledge
make dev
```

### 19.8 启动桌面端

```bash
cd apps/yijie-desktop
pnpm install
pnpm tauri dev
```

### 19.9 启动 Admin

```bash
cd apps/yijie-admin-web
pnpm install
pnpm dev
```

---

## 20. API 契约开发流程

所有 API 变更遵循 contract-first。

```text
1. 在 yijie-contracts 中修改 OpenAPI / Protobuf / JSON Schema
2. 执行 generate-all.sh
3. 提交 contract PR
4. 下游仓库更新 SDK
5. yijie-api 实现服务端
6. yijie-desktop / yijie-admin-web 接入
7. yijie-agent-host / connectors / knowledge 做集成测试
8. 合并发布
```

### 20.1 禁止流程

```text
前端先写字段 -> 后端临时返回 -> contract 后补
```

这是禁止的。

### 20.2 Breaking Change 处理

Breaking change 必须：

1. 增加新字段或新版本接口；
2. 保留旧字段一段兼容期；
3. 更新 SDK；
4. 更新迁移文档；
5. 通知所有依赖仓库；
6. 在 changelog 标记。

---

## 21. 测试策略

### 21.1 测试分层

| 测试类型 | 主要仓库 | 目的 |
|---|---|---|
| Unit Test | 所有仓库 | 验证小粒度逻辑 |
| Integration Test | API、Agent Host、Connectors、Knowledge | 验证服务间调用 |
| Contract Test | Contracts、API、前端、连接器 | 验证接口兼容 |
| E2E Test | Desktop、Admin | 验证关键用户路径 |
| Runtime Compatibility Test | Codex、Agent Host | 验证 Codex 版本兼容 |
| Skill Eval | Skills | 验证 AI 结果质量 |
| Retrieval Eval | Knowledge | 验证 RAG 检索效果 |
| Security Test | API、Connectors、Infra | 验证权限、token、审计 |

### 21.2 PR 必跑测试

| 仓库 | 必跑测试 |
|---|---|
| yijie-codex | runtime compatibility tests |
| yijie-desktop | unit + e2e smoke + tauri build smoke |
| yijie-admin-web | unit + e2e smoke |
| yijie-api | unit + integration + contract |
| yijie-agent-host | unit + integration + codex compatibility |
| yijie-skills | prompt lint + skill eval |
| yijie-connectors | unit + integration + mcp contract |
| yijie-knowledge | unit + retrieval eval |
| yijie-contracts | schema lint + breaking change check + SDK generation |
| yijie-infra | terraform plan + policy check |

---

## 22. 发布策略

### 22.1 发布节奏

| 仓库 | 发布节奏 |
|---|---|
| yijie-desktop | 独立版本，走 Mac App 打包、签名、升级 |
| yijie-admin-web | 独立 Web 发布 |
| yijie-api | 后端服务发布 |
| yijie-agent-host | 跟随 runtime / API 兼容性发布 |
| yijie-codex | 上游同步后发布 runtime build |
| yijie-skills | 独立 skill/plugin 版本和灰度 |
| yijie-connectors | 按平台 API 变更和功能发布 |
| yijie-knowledge | 按知识库版本和检索服务发布 |
| yijie-contracts | 先于依赖方发布 |
| yijie-infra | 按环境变更发布 |

### 22.2 版本命名

```text
yijie-desktop:     desktop-vX.Y.Z
yijie-admin-web:   admin-vX.Y.Z
yijie-api:         api-vX.Y.Z
yijie-agent-host:  agent-host-vX.Y.Z
yijie-codex:       codex-yijie-vX.Y.Z
yijie-skills:      skills-vX.Y.Z
yijie-connectors:  connectors-vX.Y.Z
yijie-knowledge:   knowledge-vX.Y.Z
yijie-contracts:   contracts-vX.Y.Z
yijie-infra:       infra-vX.Y.Z
```

### 22.3 发布前检查

- [ ] Contract 是否兼容；
- [ ] Migration 是否可回滚；
- [ ] 高风险工具是否配置审批；
- [ ] 日志是否脱敏；
- [ ] 关键路径测试是否通过；
- [ ] 观测 dashboard 是否更新；
- [ ] Runbook 是否更新；
- [ ] Changelog 是否更新。

---

## 23. 安全边界

### 23.1 Token 边界

```text
Desktop
  不保存平台 access token
  只保存用户登录态和必要的本地安全信息

Yijie API
  管理店铺授权状态
  管理租户权限
  不直接暴露 token 给前端或 Codex

Yijie Connectors
  管理平台 token vault
  执行平台 API 调用
  做 token refresh 和 rotation

Yijie Agent Host
  不直接持有平台 token
  只能请求连接器执行工具

Codex Runtime
  不直接接触平台 token
  通过 MCP 工具间接完成任务
```

### 23.2 审批边界

高风险操作必须经过：

```text
Codex tool call proposal
  -> yijie-agent-host policy check
  -> yijie-api approval task
  -> desktop approval card
  -> user approve / reject
  -> connectors execute
  -> audit log
```

### 23.3 日志边界

日志中不得出现：

- access token；
- refresh token；
- cookie；
- 平台密钥；
- 买家邮箱；
- 买家电话；
- 买家地址；
- 完整订单号；
- 银行卡或支付信息；
- 未脱敏经营敏感数据。

---

## 24. 可观测性要求

### 24.1 Trace ID

所有跨服务请求必须包含：

```text
trace_id
request_id
tenant_id
user_id
task_id
agent_session_id
codex_thread_id
```

### 24.2 关键指标

| 模块 | 指标 |
|---|---|
| API | QPS、P95、P99、错误率 |
| Agent Host | task success rate、event lag、runtime crash count |
| Codex Runtime | turn duration、tool call count、runtime error |
| Connectors | API quota、rate limit、external error、retry count |
| Knowledge | retrieval latency、hit rate、citation coverage |
| Desktop | crash rate、update success rate、sidecar health |
| Skills | eval score、approval rate、tool failure rate |

### 24.3 日志分类

```text
application log
access log
audit log
security log
agent event log
tool call log
external api log
```

---

## 25. 数据与环境隔离

### 25.1 环境

```text
local
  本地开发

dev
  团队联调

staging
  预发验证

prod
  生产环境
```

### 25.2 数据隔离

- 不允许将生产数据复制到 local；
- staging 如需使用生产样本，必须脱敏；
- fixtures 只能使用合成数据；
- eval 数据集不得包含真实商家敏感数据；
- 本地 mock 平台 API 不得使用真实 token。

---

## 26. MVP 建设顺序

推荐按以下顺序建设：

```text
1. yijie-workspace
2. yijie-contracts
3. yijie-codex
4. yijie-agent-host
5. yijie-api
6. yijie-desktop
7. yijie-connectors
8. yijie-knowledge
9. yijie-skills
10. yijie-admin-web
11. yijie-infra
```

### 26.1 MVP 第一条闭环

建议先打通：

```text
用户在桌面端输入 Amazon 商品链接
  -> yijie-api 创建任务
  -> yijie-agent-host 创建 Codex session
  -> Codex 加载 listing diagnosis skill
  -> 调用 connectors 抓取公开 listing 信息
  -> 调用 knowledge 检索 listing 规则
  -> 生成 listing 诊断报告
  -> desktop 展示结果
  -> audit log 记录完整链路
```

这个闭环能验证：

1. 桌面端 Chat；
2. API 任务；
3. Agent Host；
4. Codex Runtime；
5. Skill；
6. Connector；
7. Knowledge；
8. 审计；
9. 流式事件；
10. 结果展示。

---

## 27. 首批必须创建的文档清单

### 27.1 yijie-workspace

```text
README.md
AGENTS.md
CONTRIBUTING.md
SECURITY.md
repos.yaml
docs/architecture/000-overview.md
docs/architecture/001-project-skeleton.md
docs/architecture/002-repo-strategy.md
docs/architecture/003-agent-runtime.md
docs/security/security-model.md
docs/security/approval-policy.md
docs/dev/local-development.md
docs/dev/codex-development.md
docs/adr/README.md
```

### 27.2 yijie-codex

```text
README.md
AGENTS.md
UPSTREAM.md
CHANGELOG.yijie.md
docs/yijie-integration.md
docs/upstream-sync.md
docs/runtime-security.md
```

### 27.3 yijie-desktop

```text
README.md
AGENTS.md
docs/local-development.md
docs/tauri-sidecar.md
docs/desktop-release.md
```

### 27.4 yijie-admin-web

```text
README.md
AGENTS.md
docs/local-development.md
docs/permission-model.md
```

### 27.5 yijie-api

```text
README.md
AGENTS.md
docs/architecture.md
docs/module-guideline.md
docs/api-guideline.md
docs/database-guideline.md
```

### 27.6 yijie-agent-host

```text
README.md
AGENTS.md
docs/codex-app-server-integration.md
docs/event-model.md
docs/policy-model.md
docs/sidecar-mode.md
docs/cloud-runner-mode.md
```

### 27.7 yijie-skills

```text
README.md
AGENTS.md
docs/skill-authoring.md
docs/plugin-authoring.md
docs/prompt-style-guide.md
docs/eval-guideline.md
```

### 27.8 yijie-connectors

```text
README.md
AGENTS.md
docs/connector-guideline.md
docs/mcp-tool-guideline.md
docs/token-security.md
docs/idempotency.md
docs/audit-log.md
```

### 27.9 yijie-knowledge

```text
README.md
AGENTS.md
docs/ingestion-guideline.md
docs/retrieval-guideline.md
docs/citation-guideline.md
docs/freshness-policy.md
docs/rag-eval-guideline.md
```

### 27.10 yijie-contracts

```text
README.md
AGENTS.md
docs/api-design-guideline.md
docs/versioning.md
docs/sdk-generation.md
docs/breaking-change-policy.md
```

### 27.11 yijie-infra

```text
README.md
AGENTS.md
docs/environment.md
docs/deployment.md
docs/rollback.md
docs/observability.md
docs/security.md
```

---

## 28. CODEOWNERS 建议

顶层 `CODEOWNERS` 示例：

```text
# Workspace
/docs/architecture/ @platform-team @backend-team @agent-runtime-team
/docs/adr/ @platform-team @cto-office
/docs/security/ @security-team @platform-team
/repos.yaml @platform-team

# Apps
/apps/yijie-desktop/ @client-team
/apps/yijie-admin-web/ @admin-platform-team

# Services
/services/yijie-api/ @backend-team
/services/yijie-agent-host/ @agent-runtime-team
/services/yijie-connectors/ @integration-team
/services/yijie-knowledge/ @data-ai-team

# Packages
/packages/yijie-skills/ @ai-product-team
/packages/yijie-contracts/ @platform-team

# Runtime
/codex/yijie-codex/ @agent-runtime-team

# Infra
/platform/yijie-infra/ @devops-team @security-team
```

---

## 29. PR 模板建议

```markdown
# PR 标题

## 背景

说明为什么改。

## 变更内容

- 

## 影响范围

- [ ] yijie-contracts
- [ ] yijie-api
- [ ] yijie-desktop
- [ ] yijie-admin-web
- [ ] yijie-agent-host
- [ ] yijie-codex
- [ ] yijie-skills
- [ ] yijie-connectors
- [ ] yijie-knowledge
- [ ] yijie-infra

## 是否涉及安全

- [ ] token / secret
- [ ] PII
- [ ] 审批策略
- [ ] 高风险工具调用
- [ ] 权限控制
- [ ] 审计日志

## 是否涉及 API 契约

- [ ] OpenAPI
- [ ] Protobuf
- [ ] JSON Schema
- [ ] SDK

## 测试

- [ ] Unit Test
- [ ] Integration Test
- [ ] Contract Test
- [ ] E2E Test
- [ ] Skill Eval
- [ ] Retrieval Eval

## 发布说明

说明是否需要 migration、灰度、回滚、手动操作。
```

---

## 30. Issue 模板建议

### 30.1 Feature

```markdown
# Feature Request

## 背景

## 用户场景

## 目标

## 非目标

## 影响仓库

## API 变更

## 安全影响

## 验收标准
```

### 30.2 Bug

```markdown
# Bug Report

## 问题描述

## 复现步骤

## 期望结果

## 实际结果

## 影响范围

## 日志 / Trace ID

## 临时绕过方案
```

### 30.3 Architecture Decision

```markdown
# Architecture Decision Proposal

## 背景

## 决策点

## 备选方案

## 推荐方案

## 风险

## 需要评审的人
```

---

## 31. 仓库依赖方向

推荐依赖方向如下：

```text
yijie-desktop
  -> yijie-contracts
  -> yijie-api
  -> yijie-agent-host sidecar binary

yijie-admin-web
  -> yijie-contracts
  -> yijie-api

yijie-api
  -> yijie-contracts
  -> yijie-agent-host
  -> yijie-connectors
  -> yijie-knowledge

yijie-agent-host
  -> yijie-contracts
  -> yijie-codex binary / app-server protocol
  -> yijie-skills
  -> yijie-connectors
  -> yijie-knowledge

yijie-skills
  -> yijie-contracts
  -> yijie-connectors tool schemas
  -> yijie-knowledge retrieval schemas

yijie-connectors
  -> yijie-contracts

yijie-knowledge
  -> yijie-contracts

yijie-infra
  -> deploys all service repos

yijie-codex
  -> 不依赖任何易界业务仓
```

关键红线：

```text
yijie-codex 不能依赖 yijie-api / yijie-connectors / yijie-skills / yijie-knowledge
```

---

## 32. 后续可拆分仓库

当前不建议提前拆，但后续可以根据团队和业务规模拆出：

| 未来仓库 | 触发条件 |
|---|---|
| yijie-billing | 计费复杂，有独立财务和用量团队 |
| yijie-ads-engine | 广告投流算法和归因复杂化 |
| yijie-analytics | 经营分析成为独立数据产品 |
| yijie-ui-kit | 桌面端和 admin 共享大量组件 |
| yijie-evals | AI eval 平台化 |
| yijie-amazon-connector | Amazon 连接器体量巨大且团队独立 |
| yijie-mobile | 真正启动移动端产品时 |

---

## 33. 项目骨架验收清单

项目初始化完成后，应满足：

- [ ] 11 个仓库已创建；
- [ ] `yijie-workspace` 已能拉取所有子仓；
- [ ] 每个仓库都有 `README.md`；
- [ ] 每个仓库都有 `AGENTS.md`；
- [ ] 每个仓库都有 `SECURITY.md`；
- [ ] 每个仓库都有 `.codex/config.toml`；
- [ ] 顶层 ADR 已创建；
- [ ] contract-first 流程已定义；
- [ ] 本地开发脚本已定义；
- [ ] 高风险操作审批策略已定义；
- [ ] token 边界已定义；
- [ ] Codex Runtime 与业务代码边界已定义；
- [ ] MVP 第一条闭环已明确；
- [ ] CODEOWNERS 已配置；
- [ ] PR 模板已配置；
- [ ] Issue 模板已配置。

---

## 34. 最终建议

易界 AI 的工程骨架要围绕一个核心原则设计：

```text
不要把 Agent Runtime、业务系统、领域能力、工具执行、知识检索混在一起。
```

推荐的长期稳定结构是：

```text
yijie-codex        管 Runtime
yijie-agent-host   管 Runtime 适配和安全边界
yijie-skills       管 跨境电商智能能力
yijie-connectors   管 外部平台工具执行
yijie-knowledge    管 RAG 和规则知识
yijie-api          管 易界业务系统
yijie-desktop      管 卖家产品入口
yijie-admin-web    管 内部管理后台
yijie-contracts    管 多仓契约
yijie-infra        管 部署和基础设施
yijie-workspace    管 项目入口和架构治理
```

这样拆分后，易界 AI 可以在不自研完整 agent platform 的前提下，充分复用 Codex Runtime，同时把真正有商业壁垒的跨境电商能力沉淀在 `yijie-skills`、`yijie-connectors` 和 `yijie-knowledge` 中。
