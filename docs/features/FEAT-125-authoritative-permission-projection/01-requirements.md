# FEAT-125 需求与验收标准

## 1. 用户与场景

| 角色 | 权限/租户 | 场景 | 期望结果 |
|---|---|---|---|
| 已认证卖家用户 | 当前租户成员，拥有部分 capability | 打开 Desktop 或切换租户 | 只看到并进入被授权模块 |
| 已认证受限用户 | 当前租户成员，无某模块 capability | 导航或直接深链 | 入口不渲染；深链进入明确 denied 状态 |
| 成员资格被撤销用户 | 凭证仍在有效期但租户 membership 已失效 | 刷新权限或调用业务 API | 服务端拒绝，Desktop 清空旧投影并提供恢复 |
| 篡改客户端 | 伪造 route、tenant 或前端状态 | 直接调用 API | 服务端重新认证、校验租户和资源权限并拒绝 |
| 发布/安全负责人 | 段成威 | 审核 candidate 与灰度 | 能从 tag、SHA、digest、测试和审计追溯决策 |

## 2. 业务规则

| Rule ID | 规则 | 来源/确认人 | 优先级 |
|---|---|---|---|
| BR-001 | `yijie-api` 是内部用户映射、租户成员关系、角色、权限和最终授权的唯一业务真相 | 已有仓库边界 / 段成威 | Must |
| BR-002 | Principal 来自 API 严格验证的 direct IdP RS256 access JWT；Desktop 不构造 user，且本功能不引入 opaque Yijie session | A1 / 段成威 | Must |
| BR-003 | `GET /v1/me/capabilities` 必须使用 `X-Yijie-Tenant-ID` 表达当前租户选择；该 header 只是选择提示，API 每个请求必须重新验证 membership，禁止把它直接当作授权事实 | A3 / 段成威 | Must |
| BR-004 | 权限状态缺失、加载、过期、格式错误、超时或服务异常时，对所有受保护模块默认拒绝 | Desktop 审核 / 段成威 | Must |
| BR-005 | 授权可见性和产品可用性正交：无权限时隐藏；有权限但未发布时显示 disabled“即将开放” | FEAT-124 / 段成威 | Must |
| BR-006 | Settings 第一版作为已登录用户的本地 recovery/core 入口常显；敏感 section 未来单独授权 | A5 / 段成威 | Must |
| BR-007 | 导航和 Router guard 只改善 UX；生产目标是每个业务 API 都执行服务端 user+tenant+resource+action 授权。FEAT-125 的验收边界是 tenant/capability endpoints 独立认证和逐请求校验 membership；legacy Tasks 在 FEAT-126 完成资源级授权前必须按 BR-021 双重隔离 | 安全审核 / 段成威 | Must |
| BR-008 | capability 仅保存在当前进程内存，不进入 LocalStorage、SessionStorage、IndexedDB 或普通日志 | Desktop 安全规则 / 段成威 | Must |
| BR-009 | login、logout、切租户、到期、前台恢复和显式 retry 都必须刷新；切换前先清空并拒绝迟到响应 | Desktop 审核 / 段成威 | Must |
| BR-010 | 有效主体与租户但零权限返回 `200 + []`；认证、租户和授权依赖故障使用不同稳定错误 | Contracts 审核 / 段成威 | Must |
| BR-011 | capability 是开放、命名空间化字符串；未知值由旧 Desktop 忽略，已发布 key 不重用或改义 | Contracts 审核 / 段成威 | Must |
| BR-012 | 响应不泄漏角色名、策略表达式、凭证、外部 subject 或内部 RBAC 图 | 安全审核 / 段成威 | Must |
| BR-013 | Contracts/API/Desktop 必须固定同一 candidate/tag、完整 SHA、digest 和 generator；禁止 floating sibling 作为发布来源 | Contract-first 政策 / 段成威 | Must |
| BR-014 | FEAT-124 G4-001 在真实 producer、consumer、多角色/多租户集成证据完成前保持 Open | 用户要求 / 段成威 | Must |
| BR-015 | 若 FEAT-125 改动既有 `/v1/tasks` 认证或 `tenant_id` 语义，必须先升级影响分类并另走兼容迁移 | Contracts/API 审核 / 段成威 | Must |
| BR-016 | 未解决现有 Tasks API 的生产暴露策略前，不得宣称整个 yijie-api 已完成生产授权闭环 | API 审核 / 段成威 | Must |
| BR-017 | Desktop 使用系统默认浏览器完成 Authorization Code + PKCE S256；Rust 先绑定精确 `http://127.0.0.1:<ephemeral-port>/oauth/callback`，每次生成一次性 CSPRNG state/nonce，opener 只允许精确 IdP HTTPS origin；禁止 embedded WebView 和 custom deep-link 回调 | A1/A2 / 段成威 | Must |
| BR-018 | access token 有效期 10 分钟并只驻留 Rust 进程内存；不足 2 分钟时 single-flight refresh。refresh token 仅存 macOS Data Protection Keychain service `ai.yijie.desktop.auth`，30 天 idle/90 天 absolute，必须 rotation，reuse 时撤销整个 token family；ID token 仅驻留 Rust 内存。禁止通过 Tauri event/command result 暴露 token，禁止普通前端存储、文件或日志 fallback | A2 / 段成威 | Must |
| BR-019 | `/` 在 ready 投影下依次选择：有 `task.create` 进入 `/chat`；否则有 `task.read` 进入 `/tasks`；否则进入常显 `/settings`。显式 denied deep-link 必须进入 denied 状态且不实例化受保护页面 | A5 / 段成威 | Must |
| BR-020 | 初始 capability 仅为 `task.create`、`task.read`、`store.read`、`workspace.use`、`schedule.read`、`plugin.read`、`knowledge.read`；`tenant_owner` 拥有全部 7 项，`tenant_member` 仅拥有前 2 项 | A4 / 段成威 | Must |
| BR-021 | FEAT-125 不改变既有 Tasks 契约；生产必须同时保持 public ingress 拒绝 legacy Tasks 路由、`yijie-api` 服务不注册 legacy Tasks handlers，FEAT-125 Desktop 也不得调用 Tasks。例外在 `FEAT-126` 生产启用或 2026-09-30（取较早者）到期，到期未完成不得开放 Tasks 且必须重新审批 | A6 / 段成威 | Must |
| BR-022 | Desktop 负责验证 authorization response 的 state、PKCE 绑定和 ID-token nonce；`yijie-api` 是 access JWT issuer/audience/signature/alg/time/kid 的权威验证者，固定 audience 为 `https://api.yijie.ai`。撤销 refresh token 不会即时撤销已经签发的 access JWT，最大残余有效期为 10 分钟 | A1/A2 / 段成威 | Must |
| BR-023 | v1 不持久化 last tenant 或 capability projection；每次 Desktop 进程启动都重新调用 `GET /v1/me/tenants` 并按 0/1/multiple 规则恢复选择，随后重新拉取 capability。禁止从上次运行恢复 tenant/capability 作为当前授权事实 | A3 / 段成威 | Must |
| BR-024 | Rust 持有 access token 时，WebView 只通过两个 operation-scoped native calls 访问 `GET /v1/me/tenants` 与 `GET /v1/me/capabilities`；Rust 使用固定 API HTTPS origin/method/path 并在内部附加 bearer。IPC 不返回 token，也不接受任意 URL、method、Authorization header 或通用代理 payload；响应由固定 contract 生成类型/adapter 消费 | A2 的最小暴露实现 / 段成威 | Must |

## 3. 用户流程

### 主流程

1. Desktop Rust auth boundary 绑定 `127.0.0.1:0` 得到 ephemeral port，生成一次性
   PKCE S256 verifier/challenge、state 与 OIDC nonce，再通过 native opener 打开系统浏览器。
2. Rust listener 只接受 loopback peer、精确 `/oauth/callback` path 和匹配 state，使用
   verifier 交换授权码，并验证 authorization response 的 state/PKCE 绑定与 ID-token nonce。
   access/ID token 留在 Rust 内存，refresh token 写入 Keychain service
   `ai.yijie.desktop.auth`；Desktop 不替代 API 对 access JWT 作权威判定。
3. Desktop 每次进程启动都不读取 last tenant/capability，而以 bearer access JWT 调用
   `GET /v1/me/tenants`；API 独立验证 access JWT，
   映射内部 Principal 并只返回仍有效的 membership。0 个 tenant 时进入 `/settings`
   recovery 且受保护入口为 0；1 个时自动选择；多个时在 Settings tenant chooser 中由
   用户显式选择。
4. Desktop 选择 tenant 后先清空旧投影、递增 request epoch，并以
   `X-Yijie-Tenant-ID` 调用 `GET /v1/me/capabilities`。header 不代表授权结论。
5. API 对每次请求权威验证 bearer access JWT 的 issuer、固定 audience
   `https://api.yijie.ai`、RS256 signature、alg、time 与 kid，映射内部 Principal，并
   逐请求验证 header tenant 的 membership/status；缺失或格式错误返回 `400`，
   membership 拒绝返回 `403`。
6. Authorization Service 从 PostgreSQL 权威数据计算有效 capability，去重并稳定排序。
7. API 返回 `schema_version`、已验证 tenant、`authorization_revision`、`expires_at` 与
   capability。
8. Desktop 核对 schema、header/response tenant、epoch 与过期时间，只识别 7-key
   allowlist 中的已知 key。
9. Navigation Resolver 按 capability 过滤，再按静态 availability 决定 enabled/disabled。
10. Router 按 `task.create`→`/chat`、`task.read`→`/tasks`、否则 `/settings` 选择 root；
    denied deep-link 不实例化页面。tenant/capability endpoints 独立认证；legacy Tasks 在
    FEAT-126 完成资源级授权前保持双重隔离。

### 失败与恢复流程

1. `401`：清空投影和已失效的 Rust 内存 access/ID token；按 single-flight refresh 规则
   恢复或进入系统浏览器登录。refresh token 被撤销不使当前仍有效 access JWT 即时失效，
   其最大残余有效期为 10 分钟。
2. `403`：清空投影，显示成员资格/租户不可用状态；可 logout 或切换合法租户。
3. `400 invalid_tenant_context`：`X-Yijie-Tenant-ID` 缺失或非法；不显示受保护模块，
   Settings core 提供租户选择或恢复。
4. `503`、网络超时或断线：fail-closed，显示 permission-unavailable，可 retry/logout。
5. schema 不支持、tenant 不一致或 payload 非法：视为安全错误，丢弃响应并 fail-closed。
6. 旧 epoch 或旧 tenant 的迟到响应：静默丢弃，不覆盖当前状态。

### 取消、重复与部分成功

- 取消语义：新请求、logout 或租户切换使用 AbortController 取消旧请求并使旧 epoch 失效。
- 重试语义：只重试安全的 GET；用户显式重试或受控退避，不把 401/403 自动重试成风暴。
- 重复请求：响应必须幂等；Store 只接受当前 epoch/context 的最后有效结果。
- 部分成功：权限投影是一个原子快照；不得接收半份 capability 或用旧值补齐失败字段。

## 4. 可测试验收标准

| AC ID | Given | When | Then | 不可接受行为 | 业务确认人 |
|---|---|---|---|---|---|
| AC-001 | 有效 direct IdP JWT 与格式正确的 `X-Yijie-Tenant-ID` | 请求 capability endpoint | API 验证 JWT 和 membership 后返回与 RBAC 一致的 v1 投影 | 未验证 membership 就把 header 当授权事实 | 段成威 |
| AC-002 | 有效主体/租户且无权限 | 请求投影 | `200` 且 capabilities 为显式空数组 | 返回 403 或默认全权限 | 段成威 |
| AC-003 | access JWT 缺失、非法或过期，或 refresh 已失效且没有仍有效 access JWT | 请求 tenant/capability endpoint | `401`、安全错误、no-store 和认证 challenge | 泄漏具体 token 原因，或声称 refresh 撤销可即时作废已签发 access JWT | 段成威 |
| AC-004 | tenant header 缺失/格式错误或 membership 无效 | 请求投影 | 前者 `400 invalid_tenant_context`，后者 `403 tenant_access_denied`，均不返回 capability | 回退其他租户或缓存权限 | 段成威 |
| AC-005 | RBAC/identity 依赖不可用 | 请求投影 | `503` 并 fail-closed、可观测 | 伪装为 200 空权限或放行 | 段成威 |
| AC-006 | 响应含未知 capability/字段 | Desktop 解析 | 忽略未知 capability，容忍额外字段 | 崩溃或默认映射可见 | 段成威 |
| AC-007 | schema、tenant、expiry 或 payload 非法 | Desktop 解析 | 丢弃投影并进入可恢复安全错误 | 部分采用或显示全部 | 段成威 |
| AC-008 | 用户有模块权限且模块已发布 | 渲染导航并访问 route | 入口可见可用，route 可达 | static config 绕过 policy | 段成威 |
| AC-009 | 用户有权限但模块未发布 | 渲染导航 | 入口可见、disabled、显示“即将开放”且无 route | 因 disabled 跳过权限判定 | 段成威 |
| AC-010 | 用户无模块权限 | 渲染导航或直接深链 | 条目不在 DOM/AX tree；页面不实例化 | 仅 CSS 隐藏或仍可深链 | 段成威 |
| AC-011 | 从 tenant A 切到 B | A 请求迟到返回 | B 加载前清空；A 响应被丢弃 | 短暂显示 A 权限 | 段成威 |
| AC-012 | logout、过期、前台刷新或 Desktop 重启 | 状态变化 | 内存投影被清空并按规则刷新；重启后重新 `GET /v1/me/tenants`，按 0/1/multiple 规则选择并重新获取 capability | 持久化/复用 stale 权限或 last tenant，跳过 tenant discovery | 段成威 |
| AC-013 | 篡改 Desktop 或从不可信网络直接发请求 | 调 tenant/capability 或 legacy Tasks 路径 | tenant/capability endpoints 各自认证并校验 context；legacy `/v1/tasks*` 从 internet、Desktop 和 untrusted network 均不可达，且服务不注册对应 handlers | 菜单隐藏被当作授权，或把 FEAT-125 宣称为 Tasks 资源级授权完成 | 段成威 |
| AC-014 | contracts candidate 完成 | API/Desktop 集成 | 两端固定同一 SHA/digest/generator，conformance 通过 | 手写影子 DTO 或浮动分支 | 段成威 |
| AC-015 | 两角色×两租户测试矩阵 | 执行跨仓 E2E | 允许/拒绝与 RBAC 一致，跨租户泄漏为 0 | 合成前端布尔测试冒充 E2E | 段成威 |
| AC-016 | FEAT-125 全部 Must AC 与 G4 通过 | 回到 FEAT-124 | 更新 Desktop SHA、关闭 G4-001 并重新独立 G4 | 仅创建文档或 unit test 就关闭 | 段成威 |
| AC-017 | 未登录 Desktop | 发起登录 | 系统浏览器 Code+PKCE S256 使用精确 `http://127.0.0.1:<ephemeral-port>/oauth/callback`；state/nonce 每次唯一；Desktop 验证 state/PKCE 和 ID-token nonce | embedded WebView、deep-link、固定端口、复用 state/nonce 或接受非 loopback/非精确 path callback | 段成威 |
| AC-018 | OIDC code exchange 成功 | 建立、刷新认证状态并调用 tenant/capability endpoints | 10 分钟 access token 和 ID token 仅 Rust 内存；不足 2 分钟 single-flight refresh；refresh 仅 Keychain service `ai.yijie.desktop.auth`，30 天 idle/90 天 absolute、rotation、reuse-revokes-family；operation-scoped Rust transport 内附加 bearer，WebView/IPC/存储/日志中 token 为 0 | token 经 IPC 返回、generic native proxy、任意 URL/header、LocalStorage/file fallback、并发 refresh 风暴、复用旧 refresh token或 Keychain 失败时继续已登录 | 段成威 |
| AC-019 | ready 投影包含不同 task capability | 打开 `/` 或 denied deep-link | `task.create`→`/chat`；否则 `task.read`→`/tasks`；否则 `/settings`；denied 页面不实例化 | 无条件 `/chat`、重定向到无权页面或仅 CSS 隐藏 | 段成威 |
| AC-020 | `tenant_owner`、`tenant_member` × 2 tenants | 执行跨仓矩阵 | owner 精确 7 key；member 精确 `task.create/task.read`；跨租户泄漏为 0 | 冒号 key、额外隐式 key、角色名直接驱动前端或跨租户 union | 段成威 |
| AC-021 | FEAT-126 未生产启用且日期早于例外期限 | FEAT-125 发布 | Tasks 契约不变；public ingress 拒绝 legacy 路由、服务不注册 handlers、Desktop 不调用；到期自动阻断 Tasks | 用 FEAT-125 静默修改/暴露 Tasks、只做客户端隔离或无限延期例外 | 段成威 |

## 5. 状态与错误语义

| 状态/错误 | 触发条件 | 用户行为 | 系统行为 | 是否可重试 |
|---|---|---|---|---|
| signed-out | 无有效 direct IdP JWT/auth context | 系统浏览器登录 | 清空 Rust token 与所有权限状态 | 登录后可 |
| loading | 获取当前 context 投影 | 等待或取消会话 | 受保护导航为 0，不闪现旧值 | 系统控制 |
| ready-empty | 有效 context、零 capability | 使用 Settings/logout | 仅显示 core/recovery | 刷新可 |
| ready | 有效且未过期投影 | 正常使用 | 按 capability+availability 渲染 | 到期刷新 |
| unauthorized / 401 | access JWT 无效/过期且 refresh 失败 | 重新登录 | 清空失效 Rust token、Keychain 无效 refresh 与投影；refresh 撤销不即时撤销仍有效 access JWT，残余窗口不超过 10 分钟 | 重新认证后 |
| tenant-denied / 403 | membership 被拒绝 | 切租户或 logout | 清空当前 context | 状态修复后 |
| invalid-tenant-context / 400 | tenant header 缺失或格式错误 | 在 Settings 选择/建立租户 | 返回 `invalid_tenant_context`，不显示受保护模块 | 选择后 |
| unavailable / 503 | 授权依赖不可用 | retry/logout | fail-closed，记录脱敏信号 | 是，有上限 |
| invalid-projection | schema/context/payload 非法 | retry/logout | 丢弃全部响应 | 修复后 |

## 6. 数据要求

| 数据 | 来源 | 分类 | 租户边界 | 保留/删除 | 日志可见性 |
|---|---|---|---|---|---|
| 内部用户映射 | 经批准的身份源 | Confidential | 用户可关联多个 membership | 按身份/合规策略 | 仅内部 ID/脱敏状态 |
| 活动租户 membership | PostgreSQL | Confidential | tenant+user 复合边界 | 状态变更可审计 | 可记内部 ID，不记 token |
| role/permission assignment | PostgreSQL | Confidential | 角色不得跨租户分配 | 版本化/可审计 | 只记变更摘要 |
| capability projection | API 临时响应/Desktop 内存 | Confidential | 必须带服务端 tenant_id | 到期或 context 变化立即清空 | 不记完整集合 |
| 当前 tenant selection | `GET /v1/me/tenants` + 本进程用户选择 | Confidential | 只指向当前用户的有效 membership | 仅 Desktop 进程内存；退出/重启清空，不持久化 last tenant | 仅记脱敏切换结果 |
| IdP access/ID token | direct IdP | Restricted | access JWT 固定 audience `https://api.yijie.ai`；绑定 issuer/subject | 仅 Rust 内存；access TTL 10 分钟，不足 2 分钟 single-flight refresh；过期/logout 清空 | 永不记录或返回 WebView |
| IdP refresh token | direct IdP | Restricted | 当前 macOS 用户与环境 | 仅 Data Protection Keychain service `ai.yijie.desktop.auth`；30 天 idle/90 天 absolute、rotation，reuse 撤销 family，logout/invalid_grant 删除 | 永不记录或返回 WebView |

## 7. 非功能要求

| NFR ID | 类别 | 可测要求 | 阻断阈值 |
|---|---|---|---|
| NFR-001 | 安全 | 任意非 ready 状态和未知 capability 默认拒绝 | 任一默认放行即阻断 |
| NFR-002 | 租户隔离 | 两租户资源与投影不可交叉，迟到响应不可覆盖 | 任一跨租户泄漏即阻断 |
| NFR-003 | 可靠性 | logout/切租户/到期均先清空；授权依赖故障可恢复 | 出现 stale 权限闪现即阻断 |
| NFR-004 | 性能 | staging p95 与 SLO 在 G2 固定，查询必须有受控上限 | 无测量基线或无上限即阻断 G5 |
| NFR-005 | 可访问性 | hidden 项不进入 AX tree；错误恢复可键盘操作且有焦点 | 键盘不可恢复即阻断 |
| NFR-006 | 可追溯 | contract、generator、producer、consumer 均有完整 SHA/digest | 任一浮动引用即阻断 |
| NFR-007 | 隐私 | token、外部 subject、完整 capability 不进入日志/fixture | 任一泄漏即阻断 |
| NFR-008 | 原生认证安全 | callback 仅为精确 `http://127.0.0.1:<ephemeral-port>/oauth/callback`；state/PKCE/ID-token nonce 验证；Keychain service 和 token 生命周期符合 BR-018；native opener/listener/transport 最小权限且 transport 仅允许两个固定 GET operations | 任一 deep-link/embedded login、非 loopback/错误 path、generic proxy、任意 URL/header、普通存储 fallback、refresh reuse 未撤销 family 或 token IPC 泄漏即阻断 |

## 8. 外部副作用与审批

| 操作 | 影响范围 | 是否写操作 | 审批策略 | 审计要求 |
|---|---|---|---|---|
| 查询权限投影 | 当前用户/租户 | no | 有效认证与 membership | 仅脱敏请求/结果状态 |
| 创建/变更 membership、role、permission | 租户授权面 | yes | 仅受控 Admin/CLI，默认拒绝 | 与状态变更同事务审计 |
| bootstrap 首个 owner/tenant | 全新环境 | yes | 段成威显式批准的幂等运维流程 | actor、环境、对象、结果 |
| 选择/切换当前租户 | Desktop 当前 context | no；只是后续 header 选择 | 切换前清空；API 对每个请求验证 membership | user、requested/validated tenant、结果 |

## 9. 非目标

- 不把菜单配置变成服务端 UI schema。
- 不实现 Admin Web 权限管理页面。
- 不把 capability 投影当作离线授权票据或业务 API 凭证。
- 不修改 Agent Host owner-only bearer 或 Runtime compatibility。
- G2 已于 2026-07-31 通过，G2A 已于 2026-08-01 通过并仅授权 S3 API foundation；
  仍禁止 production mock 权限，S4+、Desktop 和生产配置必须遵守后续 slice/gate。

## 10. 已批准决策与剩余生产配置

| ID | 问题 | 为什么阻塞 | Owner | 截止日期 | 结论 |
|---|---|---|---|---|---|
| Q-001 | 身份由自建账户还是外部 OIDC 提供？ | 决定 token 验证、供应商、迁移和责任边界 | 段成威 | G1 | Resolved：外部 OIDC；API 直接验证 IdP RS256 access JWT，不采用 opaque session |
| Q-002 | Desktop 凭证与刷新如何承载？ | 决定 PKCE、Keychain、撤销、Tauri 权限与 CSP | 段成威 | G1 | Resolved：系统浏览器 Code+PKCE S256、精确 `/oauth/callback` ephemeral loopback；access/ID Rust memory；refresh Keychain service `ai.yijie.desktop.auth`；10m access、<2m single-flight、30d idle/90d absolute、rotation/reuse-revokes-family |
| Q-003 | 多 membership 下如何选择 tenant？ | 决定 context、错误、并发和数据库约束 | 段成威 | G1 | Resolved：先调 `GET /v1/me/tenants`；0 个进入 Settings recovery，1 个自动选，多个由用户选；`X-Yijie-Tenant-ID` 是选择提示；API 每请求验证 membership；missing/invalid=400、denied=403 |
| Q-004 | 初始 role→capability 矩阵是什么？ | 无矩阵无法验证权威判定 | 段成威 | G2 | Resolved：7 个点号 key；`tenant_owner` 全部，`tenant_member` 仅 task.create/task.read |
| Q-005 | Settings 是否始终作为 recovery/core 可见？ | 决定零权限用户能否 logout/retry | 段成威 | G2 | Resolved：已登录用户常显，敏感 section 单独 gate |
| Q-006 | 权限快照最大时效是多少？ | 决定撤权可见性和刷新负载 | 段成威 | G2 | Resolved：服务端 `expires_at` 上限 5 分钟，过期先清空再刷新 |
| Q-007 | 现有匿名 Tasks API 如何处置？ | 部署 API 时不能误称授权闭环 | 段成威 | G2 | Resolved：contract unchanged；public ingress deny + service 不注册 handlers 双隔离，Desktop 亦不调用；FEAT-126 或 2026-09-30 较早到期 |
| Q-008 | 生产 IdP vendor/issuer/client ID/JWKS、TLS、Secret Manager 与 CSP 是什么？ | 决定 Infra/Desktop 安全配置 | 段成威 | G3/G5 | Open；access JWT audience 已固定 `https://api.yijie.ai`，其余具体生产值禁止 Codex 自行选择 |
| Q-009 | 首个 tenant/owner 与 RBAC 如何 bootstrap？ | 不能在 migration 写真实用户，也不能无审计授权 | 段成威 | G2 | Resolved：显式幂等、可审计运维命令；生产参数仍需 G5 审批 |
| Q-010 | tenant 错误语义如何分界？ | 影响契约、恢复 UI 与监控 | 段成威 | G2 | Resolved：missing/invalid header=`400 invalid_tenant_context`；membership denied=`403 tenant_access_denied`；不使用 409 active-session 语义 |

## 11. 需求确认

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 需求负责人 | 段成威 | Approved：A1—A6，G1/G2/G2A Passed；S3 API foundation 已验证，生产 IdP/config 仍阻断 | 2026-08-01 |
