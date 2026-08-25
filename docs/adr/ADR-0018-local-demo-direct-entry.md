# ADR-0018: Local Demo 免登录直达与公开环境鉴权边界

## 状态

Accepted

## 日期

2026-08-23

## 决策负责人

段成威

## 背景

FEAT-125 的“本地白名单”仍是 synthetic OIDC 登录：用户必须输入账号和密码，Desktop 再通过
Keycloak、证书、Keychain、API tenant/capability projection 才能进入业务页面。它不是免登录机制。
这使每次本地业务验证都可能先被认证环境阻断，与 ADR-0017 的 Demo 快速闭环目标冲突。

本项目当前首先作为本地个人 Demo 使用。段成威明确要求：本地启动后，所有正常用户操作不再要求
任何登录交互，Desktop 直接进入 yijie 主页面；该规则是本地业务验证的最高优先级。

## Contract Impact

`semantic`。本地 Desktop 的身份入口、public-task control-plane 与启动语义发生变化；公共 HTTP、
Agent Host wire 和 production OIDC contract 不变。

## 决策

1. `YIJIE_ENV=local + YIJIE_LOCAL_PROFILE=demo_fast` 是唯一 local Demo direct-entry 门禁；前端使用对应
   `VITE_` 变量。缺少任一值时不启用。
2. 该 profile 启动时由 Rust native authority 自动绑定固定 synthetic owner、tenant、revision，并授予
   Desktop 当前声明的全部本地 capability；后续功能仍需实现自己的业务逻辑，但不得再因用户登录阻断。
   用户无需账号、密码、系统浏览器、Keycloak 或白名单表单。
3. Desktop 继续通过既有 permission store、ChatAuthorizationManager、context、owner/tenant/session 与
   Artifact authority 执行业务边界检查；WebView 不能制造或选择本地身份。
4. local Demo 的 public task 使用固定 scope 校验后本地绑定，不访问 `/v1/me/*` 或 `/v2/tasks`，避免
   yijie-api/OIDC 成为本地 Chat 与 Artifact 验证的启动依赖。
5. direct-entry 绑定完成后 Desktop 自动启动其管理的 Agent Host / Codex Runtime sidecar，并进入
   `/chat`；Settings 不显示登录、退出登录、账号或密码控件。
6. Agent Host owner-only loopback token 继续由 Desktop 自动生成、读取和发送；MiniMax API Key 继续从
   owner-only 文件传递。二者是无用户交互的进程/外部服务凭据，不是本地用户登录。
7. 标准本地命令 `pnpm tauri:dev` 与显式别名 `pnpm tauri:demo-fast` 必须进入同一个 canonical local
   launcher。launcher 必须清理残留 OIDC、JWKS、CA、白名单和专项 test-profile 环境，只装配 Desktop、
   Agent Host、Codex Runtime、MiniMax 与 v3 Artifact 所需变量。裸 Tauri 入口仅以明确命名的
   `pnpm tauri:dev:raw` 保留给底层调试，不得作为正常业务验证入口。
8. `exposure=public`、`production_hardened` 或非 `local` 环境禁止该 profile，继续使用正常 OIDC、
   服务端 tenant/RBAC 与公开安全检查。D4 的 local 证据不得冒充 DP/G5/G6。
9. FEAT-125/126 的历史认证测试资产与失败账本保留；本决策只 supersede “正常 local Demo 必须手工
   白名单登录”的入口语义，不把历史测试改写为 PASS。
10. Desktop 正常退出必须同步停止其持有的 Host；Desktop 崩溃或被强制终止时，Host 必须通过启动时
    精确校验的 parent PID 自行优雅退出。launcher 必须在覆盖 Host binary 前后检查端口，并清除会令
    renderer/native/Host 进入专项 harness 或半边 profile 的历史环境变量。

## 影响

- 正常本地业务验证只有一个命令，并且 fresh process 首屏为 `/chat`。
- Keycloak/Caddy/API permission projection 不再是 FEAT-128 local Demo 主链依赖。
- public/production 鉴权不降级；Host 内部 token 与模型服务 Key 不删除。
- 重复启动不再依赖人工查杀残留 Host；正常退出与父进程崩溃均释放 loopback 端口。
- FEAT-128 的 `contract-impact` 由图片工具的 additive 子变化提升为整体 local-entry `semantic`。

## 验收

- fresh Desktop 启动过程中没有登录页、系统浏览器或凭据输入，最终进入 `/chat`。
- tenant/capabilities 来自 Rust local authority，Chat/Artifact context 仍拒绝伪造或跨 scope 使用。
- public task 不触发 `/v1/me/*` 或 `/v2/tasks`；Agent Host 自动就绪。
- 普通文本、T2I、I2I、preview/save 可在同一 fresh local 会话完成。
- profile 缺失或环境不是 local 时 direct-entry 不可达，原认证路径保持不变。

## 回滚

移除 `YIJIE_LOCAL_PROFILE=demo_fast` 及其 `VITE_` 对应值，使用原 authenticated local-integration 或
production 配置重新启动。不得在公开环境通过设置 local 变量规避认证。
