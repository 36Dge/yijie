# FEAT-129 — Desktop 本地 Skill 广场 Demo Brief

> Profile: `demo_fast` · Exposure: `local` · Checkpoint: `D4 PASS` · Created: `2026-08-25` · Verified: `2026-08-26`

## 1. 用户问题与结果

- 目标用户：使用易界 AI 桌面端开展跨境电商选品、调研、内容营销、广告投放与店铺运营工作的本地用户。
- 当前问题：桌面端左侧“插件”入口当前不可用，用户没有统一入口发现、离线安装、启停、卸载领域 Skill，也无法确认某个 Skill 是否真正向模型开放。
- 真实结果：用户进入 Skill 广场后，可以在五个业务分类中查看首批 Skill，离线安装随客户端分发的资源，控制模型可见性，安全卸载，并在文件被外部移动或客户端升级后看到与本地真实状态一致的结果。
- 首批清单：以用户提供目录扫描出的 38 个 Skill 为 D0 基线，分类数量为“货源与选品”5、“市场调研与分析”9、“内容创作与营销”7、“流量获取与广告”9、“店铺运营与基建”8。正式打包前需经过版本、许可、来源、安全和能力依赖审核；审核未通过的项不得被伪装成可用。

### In scope

- 启用 Desktop 左侧“插件”入口，新增 `/plugins` 的 Skill 广场首屏。
- 卡片展示每个 Skill 的规范图标、中文名称、简介、分类、版本、来源/维护状态、能力就绪度、安装与启用状态；分类标题展示真实数量。
- 首批资源随客户端安装包分发，不依赖云端服务器或网络下载。
- 从只读 App Resource 安全、原子地安装到当前用户的受管 App Data 目录。
- 安装成功后默认启用；启停状态持久化，并由 Agent Host 投影到真实 Codex Runtime。
- 二次确认卸载只删除受管安装副本；内置源包与用户提供的源目录永不被卸载操作删除。
- 监听/扫描本地文件真实状态，并处理随客户端版本进行的 Skill 新增、升级、下架和回滚。
- 增加浏览与管理权限分层、安全边界、错误恢复、自动化测试和 fresh real-service 证据。

### Out of scope

- 云端 Skill 市场、在线下载、独立热更新服务和账号间同步。
- 公网或生产环境开放、正式签名/公证/自动更新发行流程。
- 用户导入任意第三方压缩包，或读取、写入、删除受管目录之外的路径。
- 在本 Feature 内建设浏览器、Web Search、Jungle Scout、供应商搜索等全部外部连接器。
- 修改 `yijie-codex` Runtime 核心；本 Feature 复用固定版本已有的 Skills API。
- 宣称 38 个 Skill 的全部外部工具链已经真实可执行。D4 至少验证一个无需外部连接器的代表性 Skill，其他卡片按真实依赖展示“可用”或“能力未就绪”。

## 2. 完整主流程

1. 用户通过 `yijie-desktop` 的 canonical `YIJIE_ENV=local` + `YIJIE_LOCAL_PROFILE=demo_fast` 启动器进入桌面端；依据 ADR-0018，Desktop 自动建立固定本地身份、授予该 profile `plugin.read`/`plugin.manage` 并透明携带 owner-only Host bearer。用户不经过登录页、账号鉴权或手动授权即可直接使用本地服务，但 Host 进程边界仍校验 bearer/capability，public/production 不适用该入口。
2. 用户点击左侧“插件”。Desktop 校验 `plugin.read` 后进入 `/plugins`，读取客户端内置 `bundle-manifest.json`，扫描受管安装根目录，并按五类渲染目录、数量和卡片状态。
3. 未安装卡片右侧显示加号。鼠标悬停或键盘聚焦时显示 tooltip“安装”；用户点击后，该卡片进入局部 loading 并禁止重复操作。
4. Tauri 解析只读 App Resource 与私有 App Data 根目录并以精确 local + demo_fast 配置启动 Agent Host；Desktop 调用 Host 安装接口。Host 固定按 bearer、`plugin.manage`、受信任 Skill ID 的顺序校验，再验证 manifest schema、SHA-256、文件数量、解压大小、路径穿越、绝对路径和符号链接，通过同一受管根内的 staging/rollback 原子提交到 App Data。
5. 安装成功后 Host 写入 owner-only 安装回执，默认不写停用标记；随后将受管根目录通过 `skills/extraRoots/set` 注册给固定 Runtime，并用 `skills/config/write` 同步启用状态。
6. Runtime 的新一轮 Skill snapshot 只包含“目录有效且已启用”的 Skill；用户在后续对话或任务中可被模型选择调用。安装完成不等于所有外部依赖就绪，卡片必须如实披露依赖状态。
7. 用户关闭开关后保留文件并写入 `.yijie-disabled` 或等价持久状态，Host 立即同步；从下一轮起模型不可见。再次开启删除停用标记并恢复可见。重启后 Desktop/Host 从 App Data 权威状态重放。
8. 已安装卡片操作区在 hover/focus 时显示灰色删除按钮，直接 hover/focus 删除按钮时使用危险色。点击后显示“卸载此技能 / 卸载后需要重新安装才能使用。 / 取消 / 确认”。取消、关闭或 Escape 不变更任何状态。
9. 用户确认卸载后，Host 先停止暴露，再只删除 `<App Data>/skills/installed/<skill-id>/` 受管副本和注册状态；Desktop 根据响应把卡片恢复为加号。只读内置资源仍在，用户可再次离线安装。
10. Desktop 在应用启动、页面进入、升级完成、窗口恢复及目录变化通知时重新对账。用户手工移走 Skill 目录后，Host 停止暴露，页面恢复未安装；目录损坏时进入错误/重装态而不是继续向模型开放。
11. 新客户端内置新清单后进行版本对账：未安装项只更新可安装版本；已安装项在完整验证后原子替换并保留启停状态；失败继续使用旧版；新增项不自动安装；下架项保留用户副本并标记“不再随客户端维护”。

## 3. 分发、目录与契约设计

### 3.1 只读安装源

```text
<App Resource>/skill-packages/
├── bundle-manifest.json
└── packages/
    ├── <skill-id>.zip
    └── ...
```

`bundle-manifest.json` 由 `yijie-contracts` 的增量 schema 约束，由 `yijie-skills` 确定性生成，至少记录：schema 版本、稳定 Skill ID、Runtime name、分类/排序、中文名称/简介、版本、归档相对路径、SHA-256、压缩/解压大小、文件数、入口文件、`YjIcon` 注册键、风险级别、来源/许可、维护状态和能力依赖/就绪度。清单只能引用 App Resource 内的相对路径。

### 3.2 用户安装真相

```text
<YiJieAI App Data>/skills/
├── installed/
│   └── <skill-id>/
│       ├── SKILL.md
│       ├── .yijie-install.json
│       ├── .yijie-disabled   # 仅停用时存在
│       └── ...
└── staging/
```

- `<YiJieAI App Data>` 必须通过 Tauri 平台 API 解析；macOS 对应当前用户的 Application Support，Windows 对应当前用户的 AppData。运行时代码不得硬编码个人绝对路径。
- `installed/` 是安装状态的最终依据；Agent Host 独占受管文件事务，安装回执记录 Skill ID、安装版本、包摘要、安装时间和清单版本，Desktop/Tauri 不另建第二套安装真相。
- App Resource 只作为离线安装源，不直接注册给模型；Host 只注册已安装根目录。
- 不直接写 Host 管理的 `$CODEX_HOME/skills`。Desktop 平台 API 解析的 App Data 根由 Agent Host 作为启停/安装权威并在启动时重放到 Runtime，避免 Host 重建配置后丢失用户状态。
- staging 与 installed 使用同一文件系统；安装、升级、回滚和删除只能按 manifest 中解析出的稳定 ID 操作受管子目录。

### 3.3 权威来源和 source-first 顺序

```text
固定 yijie-codex Runtime Skills API
          ↓ 兼容投影
yijie-contracts：Host API + bundle manifest schema
          ↓
yijie-skills：内容、版本、来源、许可、安全、eval、可复现包
          ↓
yijie-agent-host：owner-only 管理接口 + Runtime 状态投影
          ↓
yijie-desktop：App Resource/App Data/Tauri/UI 消费者
```

- Runtime 上游方法：`skills/list`、`skills/extraRoots/set`、`skills/config/write`、`skills/changed`；实现前在固定 Runtime 版本和摘要上再次核实。
- `contract-impact=semantic`。Manifest v2、目录安装状态与 Runtime 投影改变了跨仓语义；通过版本化 schema 保留 v1 兼容，并执行 generate、lint、test、breaking/compatibility checks。
- 浏览需要 `plugin.read`；安装、启停、升级、卸载需要新增 `plugin.manage`。精确 local + demo_fast 固定身份默认拥有这两项能力，Desktop 自动提供 Host bearer，因此正常本地用户流程不得出现登录或权限弹窗；直接调用 Host 仍必须通过 bearer/capability 校验，public/production 仍走正式鉴权。

## 4. 交互与 UI 规范

UI 实现以 [`yijie-desktop/docs/design/docs/design`](../../../../yijie-desktop/docs/design/docs/design/README.md) 为权威，不以需求截图中的像素或临时样式覆盖系统规范。重点遵循：

- [插件市场模式](../../../../yijie-desktop/docs/design/docs/design/05-patterns/10-plugin-marketplace.md)：卡片必须让用户理解名称、能力、平台/依赖、版本、来源/维护方和状态；紧凑卡片可展示摘要，详情入口/辅助信息承载完整披露。
- [App Shell 与导航](../../../../yijie-desktop/docs/design/docs/design/05-patterns/01-app-shell-navigation.md)：复用既有左侧导航、路由权限和页面容器。
- [图标规范](../../../../yijie-desktop/docs/design/docs/design/03-ui-system/02-iconography.md)：每个 Skill 卡片配置语义化 `iconKey`，通过 `YjIcon` 的 Lucide 闭集渲染；不得使用 emoji、未知来源 SVG 或绕过 registry。用户截图仅作为“卡片需有独立图标区”的视觉意图参考：[skill-card-icon-reference.png](references/skill-card-icon-reference.png)。
- [Action](../../../../yijie-desktop/docs/design/docs/design/04-components/03-action-components.md)、[Feedback](../../../../yijie-desktop/docs/design/docs/design/04-components/05-feedback-components.md) 与 [Data Display](../../../../yijie-desktop/docs/design/docs/design/04-components/06-data-display-components.md)：复用 Naive UI、设计 Token、tooltip、switch、dialog、skeleton、alert/toast 和危险态语义。
- [暗色主题](../../../../yijie-desktop/docs/design/docs/design/03-ui-system/05-theme-dark-mode.md)、[错误/空态/加载](../../../../yijie-desktop/docs/design/docs/design/06-content/03-error-empty-loading.md) 和 [UI Review Checklist](../../../../yijie-desktop/docs/design/docs/design/07-ai-codex/03-ui-review-checklist.md)：亮暗主题均需验收，不能硬编码颜色；覆盖键盘焦点、Escape、对比度、tooltip 可达性、文本截断与最小窗口。

### 状态定义

- Idle：读取清单和目录后显示真实分类/卡片。未安装显示加号；已安装显示开关；删除仅在相关 hover/focus 上下文出现。
- Loading：页面首次扫描使用结构稳定的 skeleton；单卡安装、卸载、同步或升级显示局部进度，禁止重复点击但不冻结整页。
- Success：安装成功默认开启并提示；启停、删除、升级均在 UI 与 Host/Runtime 已收敛后更新为最终状态。
- Empty：清单为空时显示原因、客户端版本和恢复建议；分类为空显示 0，不复制假数据填充。
- Error：区分清单无效、资源缺失、校验失败、写入失败、目录损坏、Host/Runtime 不可用；错误项不向模型暴露。
- Retry：错误卡片原位提供重试或重新扫描；先清理本次 staging，保留仍可用的旧版本。
- Cancel：卸载弹窗取消、关闭、Escape 均不执行；由于安装为短时本地原子操作，不提供可能破坏一致性的中途取消，离开页面也不影响安全完成或回滚。

## 5. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | `/plugins` 展示五类、5/9/7/9/8 数量和 38 张有规范图标与状态的卡片。 | fresh local 进程在 1180×760 亮/暗主题中核对路由、计数、卡片、图标与截图。 |
| AC-002 | 加号 tooltip 为“安装”，断网时 Host 可从本地 bundle 安全原子安装，重复点击与恶意归档被拒绝且无残留。 | 成功安装 + SHA 错误 + Zip Slip + 符号链接 + 重复点击 focused checks。 |
| AC-003 | 安装后默认启用，下一轮 Runtime 可见，至少一个自包含 Skill 被模型真实调用。 | `skills/list`/Host 证据 + 新一轮真实对话的脱敏调用证据。 |
| AC-004 | 启停即时影响下一轮模型可见性，并在 Desktop/Host 重启后保持。 | 关闭、重启、查询、新对话、开启、再次查询。 |
| AC-005 | 删除 hover/focus、危险色和指定弹窗文案正确；取消无副作用，确认只删受管副本并恢复加号。 | 鼠标/键盘视觉检查 + 文件与 Runtime 状态核对。 |
| AC-006 | 外部移走/损坏目录后 UI 与 Runtime 自动收敛到未安装或可重装错误态。 | 监听、窗口恢复、页面重入三条触发路径的真实文件测试。 |
| AC-007 | 客户端版本升级正确处理未安装、已安装、新增、下架和失败回滚，保留启停状态。 | 双版本 fixture 与原子回滚测试。 |
| AC-008 | 精确 local + demo_fast 零登录直达且 Desktop 透明携带 owner bearer；Host 仍执行 `plugin.read`/`plugin.manage` 分权，缺失/错误 bearer、越权、未知 ID、越界路径被拒绝，public/production 无免登录例外。 | fresh 启动零登录检查 + Desktop/Tauri/Host 权限、profile 与能力矩阵测试。 |
| AC-009 | 页面符合 Desktop 设计系统，完整覆盖亮暗主题、所有 UI 状态、键盘焦点和最小窗口。 | 自动化 UI 状态矩阵 + 键盘可达性测试 + 机器截图；不设置人工验收门禁。 |
| AC-010 | 所有失败路径不留半安装、不误删源包、不破坏旧版、不暴露无效 Skill，且用户可理解并重试。 | 隔离环境恢复检查 + 临时目录负向 fixture，核对文件、注册、模型可见性、文案和恢复。 |

## 6. 工程事实与边界

- 受影响仓库：`yijie`（Feature Package）、`yijie-contracts`（增量契约）、`yijie-skills`（内容与构建）、`yijie-agent-host`（本机管理接口和 Runtime 投影）、`yijie-desktop`（导航、页面、Tauri、资源与 App Data）。`yijie-codex` 仅作为固定上游依赖，不计划修改。
- 真实入口：在 `yijie-desktop` 执行 `pnpm tauri:dev`，由 Tauri 启动 Agent Host sidecar 和固定 Runtime；最终 D4 必须 fresh process 验证，不能用 mock-only 页面或旧服务进程代替。
- 本地服务可用性：上述精确 local + demo_fast 入口启动成功后，Skill 广场及其本地服务必须无需用户登录、账号鉴权或手工授权即可直接使用；这是 Desktop 自动引导的本机身份流程，不得通过删除 Host bearer/capability 校验实现。
- D0 时 Desktop 仅有禁用的“插件”导航和 `plugin.read`；历史单 Skill consumer 随后补齐 `/plugins` 与 `plugin.manage`。当前 Desktop 增量已经精确同步 Contracts 0.5.1、Agent Host `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`、Skills `10c45bec29603b002e861e1499d5b4e684251af5` 和 38 项双渠道资源。
- 用户提供的本地构建输入记为 `<local-skill-source>/05Skill广场`。D0 只记录该来源类别；实现不得在运行时代码、清单或发布包中硬编码个人绝对路径，也不得修改或删除该源目录。
- D0 原始扫描为 38 个 Skill、241 个文件、约 2.6 MiB；排除 cache/debug 文件并补 NOTICE 后，`yijie-skills@0.3.0` 的正式审核集合为 258 个打包文件，逐项具备稳定版本、来源、许可、风险、能力依赖和 `iconKey`。
- 38 项中 13 项为 model-only、25 项为 tool-assisted。能力依赖不阻断安装、启用或 Runtime 可见；具体外部平台操作仍取决于本地 Runtime 能力、账号、数据权限与服务状态。
- `yijie`、`yijie-agent-host` 与 `yijie-desktop` 均已迁移到独立 `feat/feat-129-desktop-skill-marketplace` 分支；Agent Host v2/38 实现 commit 为 `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`，Desktop D4 最终实现 commit 为 `6745eb793e417c6685d1900231477c59ec81a5fd`。Desktop 以 `d0b0eee6336550ffded16723390fc9ca01a280d4` 为隔离基线，既有 FEAT-128 分支与提交保持不变。
- 本需求授权最多 **1 次**付费模型调用，且仅可用于 FEAT-129 D4 中 `copywriting@0.1.0` 的真实模型调用验证；该额度已于 `2026-08-25T15:20:38Z` 执行并用尽，不得扩展到其他付费操作。生产写入和 Codex 执行受管功能以外的破坏性删除仍未授权。产品内卸载仍需用户在 UI 二次确认，并受原生路径边界保护。

## 7. 推荐方案、前置条件与停止条件

### 推荐方案

- 使用“App Resource 只读源 + App Data 安装真相 + Agent Host Runtime 投影”三层结构，避免把内置未安装资源直接暴露给模型，也避免把用户状态托管给可能被重建的 `$CODEX_HOME`。
- 从 `yijie-contracts` 开始 source-first，先定版本化清单与管理接口，再构建包、Host 投影和 Desktop 消费者。
- 第一批所有卡片可以进入目录展示，但只有来源/许可/安全审核通过且运行依赖明确的包可进入可安装集合；不可用项必须显式说明原因。
- 卡片图标优先使用 `YjIcon`/Lucide 语义键，无需引入缺少版权来源的图片资源。

### 实施前置条件

- 为进入安装包的 Skill 建立稳定版本、来源、再分发权利、风险等级、能力依赖和最低 eval 证据。
- 从源目录排除 `.DS_Store`、`remote_skills_cache.json`、`skills_config.json`、调试和临时文件，只打包经过白名单的 Skill 目录内容。
- 固定并校验 Runtime 版本摘要，新增 `plugin.manage` 权限和跨仓契约后再实现写路径。

### 首个 Contract First 闭环（2026-08-25）

- 代表 Skill：`yijie.content-marketing.copywriting@0.1.0`，Runtime name 为 `copywriting`，风险 `medium`，`iconKey=edit`，执行模式 `model-only`，无网络、文件系统或外部工具依赖。
- 当时原始 `copywriting@0.0.94` 只有本地 cache 的 official 标记，无 LICENSE/NOTICE 或可验证上游仓库；其文本未进入候选包，初始候选因此仅使用易界重写文本。
- 当时易界重写候选仅授权 `local-development` Contract First 测试；该历史阻断已由下文覆盖 38 项的所有权/桌面再分发声明、逐项来源摘要和安全审核关闭。
- `yijie-contracts@0.5.0` 已形成不可变的本地候选 commit `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`（未 tag、未发布、未升格为 supported baseline），固定 Bundle Manifest v1、Host 查询/扫描/安装/启停/卸载接口、`plugin.manage` 与 Runtime Skills 投影。
- 不可变候选的审核摘要为：Agent Host OpenAPI `406b55dad02d5a3d489955bcf29c973b94252c3e300f8ff853709a71d6874431`；Skill Bundle Manifest v1 `d86185a1d5f4d9a136c88b679d50ac3e83bcc2b722eee39cba674c5be3b88469`；Runtime compatibility projection `6b7662d4237486300456f16abd0305fe1ea267b70a85e497ba7ab15a654939ee`。
- 正常、摘要损坏和 Zip Slip fixture 已随候选固定；`pnpm generate`、`pnpm lint`、`pnpm test`以及相对 `HEAD` 和 `ea48fe190e18afba728712d1e2cc79cda57f581b` 的 breaking checks 通过。
- `yijie-agent-host` 已精确 pin 上述 commit/OpenAPI/Manifest/Runtime projection/fixture 快照并通过 `make contract-check`；`yijie-skills` 也以 `git-commit` 锁定同一 commit 和 Manifest 摘要，相关测试通过。
- `yijie-agent-host` 已完成五个管理接口、owner-only 文件事务、操作重放以及 `skills/list`、`skills/extraRoots/set`、`skills/config/write`、`skills/changed` 投影；契约 fixture、真实 pinned Runtime 重启生命周期和实际 local-development `copywriting` 包消费均已通过 conformance。
- 该阶段结论证明首个本地 Skill 可确定性打包、跨仓契约已固定且 Agent Host 精确消费；当时 Tauri resources/sidecar 配置、Desktop UI、模型真实对话调用和 D4 尚未完成。

### Tauri 与 Desktop consumer checkpoint（2026-08-25）

- `yijie-desktop` 已通过 `contracts/agent-host-skills-v1.lock.json` 精确 pin `yijie-contracts@0.5.0` commit `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`，并固定 Agent Host OpenAPI `406b55dad02d5a3d489955bcf29c973b94252c3e300f8ff853709a71d6874431`、Skill Bundle Manifest v1 `d86185a1d5f4d9a136c88b679d50ac3e83bcc2b722eee39cba674c5be3b88469`、Runtime projection `6b7662d4237486300456f16abd0305fe1ea267b70a85e497ba7ab15a654939ee` 以及 fixture/10 个 Rust consumer 文件摘要。当前使用有时限的 reviewed hand-written Rust adapter `EXC-129-001`，并由 checker 防止漂移。
- Tauri 已通过平台 API 解析 App Resource/App Data，并把 canonical `skill-packages/` 与 owner-only `skills/installed/` 作为精确根传给 Agent Host；资源或 manifest 缺失、非目录、符号链接、权限不安全及根目录重叠均 fail closed。精确 `local + demo_fast` profile 和两个根通过受控 sidecar 环境传递，bearer 不进入子进程参数/环境或 Renderer，由原生 Host bridge 从 owner-only token 文件读取并用于 Host API。
- Tauri 暴露查询、扫描、安装、启停、卸载五个窄化 command，并仅调用 Agent Host Skills v1 API；operation ID、catalog revision、摘要、路径与 bearer 均留在原生边界。安装、解压、回滚、持久回执、停用标记和受管删除仍由 Agent Host 独占，Desktop/Tauri 未实现第二套文件事务或状态真相。
- 该检查点的 Desktop 已新增 `/plugins` 路由、导航、`plugin.read`/`plugin.manage` UI 投影、闭合 IPC adapter、Pinia 状态收敛、Skill 卡片和错误/重试/卸载确认交互，并复用设计 Token、Naive UI 与 YjIcon/Lucide；当时 App Resource 只有一个完成审核的 `copywriting@0.1.0`，其余 37 项尚未进入可安装资源。
- 该检查点的本地资源同步锁记录 manifest SHA-256 `091de202783ae2658d3a8ce3c0ceaedfef023d71fa84c94ff040e72c9421bb2c` 与 archive SHA-256 `987dae7003064fa1d0b00a37be0f130eb973a55f966fbf43faf2ed8af84c5138`，producer 固定至 `yijie-skills@c0aaba17f9ba5534e133b67b9eac43bb7210694f` 且 `source_revision_kind=git-commit`。当时该资源只进入 `local-development` 调试包，默认配置因尚无桌面再分发声明而排除它。
- Desktop contract/resource checker、全量 `demo_fast` Vitest、TypeScript lint/build、Rust fmt/clippy/unit tests 与实际 macOS debug app 打包已通过。随后从 fresh local + demo_fast 进程验证了零登录进入 `/plugins`、离线安装默认启用、停用、Desktop/Host 重启重放、重新启用、确认卸载，以及外部移走受管目录后页面重入恢复“未安装”；未执行付费模型真实对话、Desktop 恶意包失败帧、38 Skill/亮暗视觉和完整 D4/AC 验收。

### 38 项所有权、桌面再分发与安全审核关闭点（2026-08-25）

- FEAT-129 产品与仓库所有者提供声明 `FEAT-129-DESKTOP-DISTRIBUTION-2026-08-25`，覆盖 38 个稳定 Skill ID，授权 `local-development` 与正式桌面再分发；许可表达式为 `LicenseRef-YiJie-Desktop-Distribution-Owner-Attestation`。该声明是用户提供的项目所有权/授权记录，不虚构第三方法务签字，也不把缓存中的 `official` 标记当作许可证据。
- 37 项直接采用用户提供目录中的审核源码快照，只做 LF 归一化并增加包内 NOTICE，不重新编写；`copywriting@0.1.0` 保留易界重新编写的窄化 model-only 实现。`.DS_Store` 与抓取调试页 `amz-hot-keywords/scripts/debug_page.html` 被排除。
- 每项已固定来源摘要、包树摘要、归档摘要、风险等级、能力依赖、`iconKey` 和静态安全审核；共审核 258 个打包文件，不在构建期执行 Skill 脚本、不安装依赖，也不访问真实账号或商家数据。外部平台 API、账号、数据和高风险写操作仍受 Runtime/Agent Host 权限与审计控制，但不再构成源码安装或桌面再分发阻断。
- `yijie-skills@0.3.0` 不可变 commit 为 `10c45bec29603b002e861e1499d5b4e684251af5`，精确消费 `yijie-contracts@0.5.1` commit `164b14f609537d727a52326832da04430aecc4ab` 的 Manifest v2（SHA-256 `39a898111ba3dcae2f369fdcb571a2e892830d1d0a57c90ab6210a0ab897a649`）。38 项均为 `bundled + installable`，分类保持 `5/9/7/9/8`，不存在 `catalog-only`、`blocked` 或 `skill_not_installable` 产品条目。
- 本地包 manifest SHA-256 为 `cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5`，桌面正式包 manifest SHA-256 为 `9f8459077615514183fdd4c81ff3b6b2ef1ea735257b04c040399d4c91c1daa2`，两渠道共享源码树 SHA-256 `3247a14004c76170cf41a2d854e2ceffa1fd43de6e0ca8bb596f1d61d9be1029`；重复构建字节一致，`make lint` 与 `make test` 通过。
- 来源/许可阻断至此关闭。Agent Host 已精确消费 Contracts 0.5.1 / Manifest v2 与 `yijie-skills@0.3.0`，完成 38 项双渠道生命周期和固定 Runtime conformance；Host 解析并校验全部 v2 来源、许可、风险、能力依赖、`iconKey`、安装状态和归档字段，content-free Host wire 只投影契约定义的运行状态/blocked reason，卡片元数据由 Desktop 从同一份已验证 App Resource manifest 读取。截至本历史关闭点，剩余差距是 Tauri/Desktop 的 0.3.0 资源锁、正式资源同步与 38 卡片 UI；该差距已由下一检查点关闭。

### Desktop Contracts 0.5.1 / 38 Skill 消费检查点（2026-08-25）

- `yijie-desktop` 已在独立 FEAT-129 分支形成不可变 commit `ee3c508b7e9af4372c6bea758915ddb8735f422a`，精确固定 Contracts `164b14f609537d727a52326832da04430aecc4ab`、Agent Host `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` 与 Skills producer `10c45bec29603b002e861e1499d5b4e684251af5`；Manifest v2 schema 摘要为 `39a898111ba3dcae2f369fdcb571a2e892830d1d0a57c90ab6210a0ab897a649`。
- 资源同步器分别生成 `local-development` 与 `desktop-release` 目录，校验 38 个归档、`5/9/7/9/8` 分类、来源/许可/风险/能力依赖/`iconKey` 以及跨渠道字节一致性。本地 manifest 为 `cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5`，桌面正式 manifest 为 `9f8459077615514183fdd4c81ff3b6b2ef1ea735257b04c040399d4c91c1daa2`。
- `demo_fast` 构建只消费 `local-development`，默认桌面构建强制消费 `desktop-release` overlay；两种 macOS app build 均通过。Tauri 只解析 App Resource/App Data、传递 exact profile/root 并调用 Host 五接口，不解压、回滚、删除或另建安装事务。
- `/plugins` 已真实展示 38 张卡片和五类计数，完成 `iconKey`、安装 tooltip/loading/error/retry、启停、卸载 hover/danger/modal 与目录变化通知投影；全量 Vitest 为 539 项，Rust library tests 共 267 项（264 passed / 0 failed / 3 ignored），lint/build/fmt/clippy 均通过。
- fresh local + demo_fast 真实窗口已完成零登录进入、安装默认启用、停用、Desktop/Host 重启重放、重新启用、确认卸载、再次安装后外部移走目录并自动恢复未安装，以及错误态原位重试；内部 owner bearer 与 `plugin.read`/`plugin.manage` 仍保留，并实测无 bearer 返回 401。
- 视觉证据已保存为 [亮色 38 卡片](evidence/desktop-skill-marketplace-light-1180x780.jpeg)、[暗色 38 卡片](evidence/desktop-skill-marketplace-dark-1180x780.jpeg)、[安装启用态](evidence/desktop-skill-installed-1180x780.jpeg) 与 [卸载确认弹窗](evidence/desktop-skill-uninstall-modal-1180x780.jpeg)。
- 该检查点不等于 D4 PASS：当时尚未发起模型付费对话，AC-003 所要求的“代表 Skill 被模型真实调用”没有证据；用户已于 `2026-08-25T14:40:52Z` 将授权增补为最多 1 次、仅限本 AC 的真实调用。真实 Desktop frame 也尚未加载摘要损坏或 Zip Slip 包，代表性 failure/retry 仍只由 Host conformance 与 Desktop 自动化分别证明。

### AC-003 真实付费调用检查点（2026-08-25）

- canonical `pnpm tauri:dev` 启动的 Desktop/Agent Host 在 Catalog revision `cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5` 下安装 `yijie.content-marketing.copywriting@0.1.0`；调用前后均为 `installed + enabled + runtime_visible`。
- 唯一一次授权的真实模型 turn 使用 `MiniMax-M3/minimax`，显式选择 `$copywriting` 并输入完全合成的 Shopify 商品事实；turn `01a03982-579a-7be0-a2b1-ef46472c4e7e` 以 `status=completed` 结束，未提交第二个 turn，也未执行平台发布或其他外部写入。
- Runtime rollout 中仅有一个 `copywriting` Skill 注入块；去除 XML 包装后的正文 SHA-256 为 `785a47c30626608911e8b3e6221efb533116518b4463bf16f4419ca43ed9c328`，与受管安装目录中的 `SKILL.md` 完全一致。模型按 Skill 要求输出五段文案并声明仅为未发布草稿，因此 AC-003 已闭合。
- 脱敏证据见 [AC-003 copywriting 真实调用](evidence/ac-003-copywriting-real-call.md)。完整 D4 仍不因此自动通过：真实 Desktop 恶意包 frame、最小窗口和完整故障/全状态视觉矩阵仍需单独验收。

### Desktop D4 最终关闭点（2026-08-26）

- 上一节是 `2026-08-25` 的历史检查点；其余 AC 已在本关闭点完成。Desktop 最终提交为 `6745eb793e417c6685d1900231477c59ec81a5fd`：补齐安装 tooltip 的键盘焦点，保持 scan 后的原卡片 retry 状态，并修复 Host journal 触发目录 watcher 自反馈的问题；implementation digest lock 已同步。
- 最终正常门禁通过：38 项资源和 `5/9/7/9/8` 分类检查、`generate:check`、72 files / 548 Vitest、lint/build、Rust fmt/clippy，以及 265 passed / 3 ignored 的 library tests。
- AC-002/010 采用分层安全证据：隔离真实 Desktop 完成摘要失败、资源缺失、Host 不可用、安装根不可写、安装中断及恢复；Zip Slip 由拥有安装事务的 Agent Host 临时目录 fixture 验证，Desktop 自动化验证 `archive_unsafe` 投影和原位重试。所有场景均无半安装或 Runtime 误暴露，恢复正常依赖后可从原卡片重试。用户收紧安全边界后未再向 Tauri 注入危险归档。
- AC-009 由设计规范驱动的自动化矩阵与机器截图闭合，不设置人工验收门禁；覆盖亮暗主题、1180×760、tooltip hover/focus、loading/success/empty/error/retry、删除 hover/danger、取消/确认/Escape 和焦点恢复。
- 详细证据见 [D4 失败恢复与视觉矩阵](evidence/d4-desktop-failure-and-visual-matrix.md)；D4 收尾未执行付费模型调用，历史额度仍为 `1/1`。

### 停止条件

- 30 分钟没有新事实：停止猜测式补丁，收集最小复现、Host/Runtime 原始帧、文件树和权限日志。
- 90 分钟卡在同一核心问题：缩小到一个自包含代表 Skill，保持完整安装—启用—调用—停用—卸载闭环，再增量扩展目录。
- 发现来源/许可无法支持随客户端再分发：停止把相关包写入 App Resource；保留目录元数据并标记不可安装，升级为产品/法务决策。
- 发现固定 Runtime 方法或摘要不匹配：停止 Desktop 旁路实现，回到 `yijie-contracts` 修正兼容投影。
- 接近 16 小时 hard stop：保留五类目录、单个真实代表 Skill、全套安全/权限/状态闭环；将其余已审核包的批量导入与版本更新 fixture 顺延，不牺牲真实调用与失败回滚证据。
