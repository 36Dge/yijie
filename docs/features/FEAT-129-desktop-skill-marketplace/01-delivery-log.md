# FEAT-129 整体实现与调试记录

> 当前 checkpoint：`D4 PASS`。38 项双渠道资源、Tauri 消费层、38 卡片 UI、fresh 本地生命周期、分层失败恢复验证、自动化视觉矩阵及 `copywriting@0.1.0` 的唯一一次真实付费模型调用均已完成。

## 1. 整体实现方案

- 真实调用链：`Vue /plugins → Tauri Resource/App Data 解析与 SidecarSupervisor → yijie-agent-host owner-only API/文件事务 → 固定 codex app-server → SkillsService`。
- 本地状态链：`App Resource/bundle-manifest + zip（只读安装源） → Agent Host → App Data/skills/installed（安装真相） → Runtime skills/list（模型可见快照）`。
- 跨层实现顺序：固定 Runtime 方法/摘要 → `yijie-contracts` 增量 schema 与兼容投影 → `yijie-skills` 许可/安全/eval 与确定性包 → `yijie-agent-host` 管理接口和状态重放 → `yijie-desktop` Tauri、资源、路由和 UI → fresh D4。
- Contract First：不得先在 Desktop 与 Host 各自发明请求体；新增 bundle manifest、Host operation、`plugin.manage` 和 compatibility projection 后，先 generate/lint/test/breaking check，再实现生产者/消费者。
- UI First Facts：实现必须以 `yijie-desktop/docs/design/docs/design/` 为权威，使用设计 Token、Naive UI、YjIcon/Lucide 和既有 App Shell；用户截图只保存为图标区意图参考。
- 不做的生产加固：云端分发、public/production 暴露、签名/公证/自动更新发行、任意第三方包导入及 38 个 Skill 的全部外部连接器。

本 Profile 不建立治理切片。可以按技术依赖顺序编码，但最终以一个完整用户结果统一验收。

## 2. D0 至当前已发生改动

| Repository | 模块/文件 | 行为变化 | 原因 |
|---|---|---|---|
| `yijie` | `docs/features/FEAT-129-desktop-skill-marketplace/` | 新建 schema v3、`demo_fast`、`local` Feature Package，写入 brief、delivery log、verification plan 和截图参考。 | 将用户需求固化为可审计的 D0 基线，不提前声称代码或 D4 已完成。 |
| `yijie-contracts` | Bundle Manifest v1、Agent Host Skills v1、Public capability、Runtime compatibility、fixtures/SDK/docs | 增量固定稳定 Skill 元数据、查询/扫描/安装/启停/卸载 wire、`plugin.manage`、Runtime Skills 投影及正常/SHA 损坏/Zip Slip fixture；形成不可变本地候选 commit `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`。 | 先固定跨仓边界并通过生成、测试和兼容检查，避免 Host/Desktop 各自发明协议。 |
| `yijie-skills` | `yijie-desktop-skills` plugin、重写 `copywriting@0.1.0`、许可/来源审计、NOTICE、eval、确定性 packager、contract snapshot | 形成一个 model-only、无外部工具依赖、`iconKey=edit` 的 local-development 可安装包；5 文件归档 SHA-256 为 `987dae7003064fa1d0b00a37be0f130eb973a55f966fbf43faf2ed8af84c5138`，contract lock 精确指向 `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`。 | 完成首个真实 Skill 的可复现生产者；不复制许可不明的上游文本。 |
| `yijie-skills` | 38 项所有权/桌面再分发声明、源码快照、逐项来源/安全审核、Manifest v2、双渠道确定性 packager | `0.3.0` 在 commit `10c45bec29603b002e861e1499d5b4e684251af5` 将 38 项全部产出为 `bundled + installable`；37 项不重写，保留审核源码快照，`copywriting@0.1.0` 使用易界重写版本；local-development 与 desktop-release 均获授权。 | 关闭 FEAT-129 源码所有权与桌面再分发阻断，同时保留 Runtime 权限控制和逐项摘要审计。 |
| `yijie-agent-host` | contract/producer lock、五个 Host API、Manifest/archive/receipt/store/service、Runtime Skills adapter、fixture 与真实 Runtime integration | 不可变实现 commit `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` 精确 pin `yijie-contracts@0.5.1` commit `164b14f609537d727a52326832da04430aecc4ab` 与 `yijie-skills@0.3.0` commit `10c45bec29603b002e861e1499d5b4e684251af5`，完整消费 v2 来源、许可、风险、能力依赖、`iconKey`、状态和归档；38 项均完成查询/扫描/安装/启停/卸载与 Runtime 投影。 | 以 synthetic blocked、v2 摘要损坏/Zip Slip/资源缺失、目录移走、重启、401/403、双渠道和真实 pinned Runtime 证明 owner-only conformance。 |
| `yijie-desktop` | 历史 v1 contract/resource lock、Tauri `skills`/sidecar/native auth、`/plugins` 路由/导航/store/page/card | 历史 consumer 精确 pin Contracts 0.5.0 commit `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`，并完成单 Skill Tauri/Renderer 闭环；Tauri 仅消费 Host API，不实现安装/解压/回滚/删除事务。 | 保留首个 Contract First consumer 的审计链；该锁已被下方 0.5.1/38 项增量取代。 |
| `yijie-desktop` | Contracts/Host/Skills locks、双渠道 resource sync、Tauri v2 consumer、目录 watcher、38 卡片 UI、release overlays | 最终不可变 commit `6745eb793e417c6685d1900231477c59ec81a5fd` 精确 pin Contracts `164b14f609537d727a52326832da04430aecc4ab`、Host `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` 与 Skills `10c45bec29603b002e861e1499d5b4e684251af5`；local-development/desktop-release 均同步 38 个归档并校验 `5/9/7/9/8`，页面消费完整 v2 元数据和 Host 五接口。 | 完成 Desktop 38 Skill 实现闭环；本地 manifest `cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5`、正式 manifest `9f8459077615514183fdd4c81ff3b6b2ef1ea735257b04c040399d4c91c1daa2`，Tauri 不复制 Host 安装事务。 |

本轮已完成 `yijie-agent-host` lifecycle/conformance，以及 `yijie-desktop` 对 Contracts 0.5.1、Host immutable commit 与 Skills 0.3.0 的精确消费、双渠道 38 项资源、Tauri consumer、UI focused 实现、双 app build 和 fresh local + demo_fast 生命周期 smoke。固定 `yijie-codex` 作为未修改真实上游参与 Host 与 Desktop 启动；已保存亮/暗、安装启用、卸载弹窗和失败恢复证据，并完成 `copywriting@0.1.0` 的唯一一次授权模型真实调用。安全负向验证、自动化视觉矩阵和最终门禁均已闭合，D4 PASS。

## 3. 实施矩阵

| Repository | 计划模块 | 计划行为 | Gate 证据 |
|---|---|---|---|
| `yijie-contracts` | Bundle Manifest schema、Host operation、Runtime compatibility projection、权限枚举 | `0.5.0` v1 历史闭环保持不变；Catalog First v2 已形成 `0.5.1` 不可变 commit `164b14f609537d727a52326832da04430aecc4ab`。 | v2 generate/lint/test/breaking checks PASS；Manifest v2 SHA-256 `39a898111ba3dcae2f369fdcb571a2e892830d1d0a57c90ab6210a0ab897a649`。 |
| `yijie-skills` | 38 项来源/许可、icon、风险、能力依赖、安全审核与确定性 packager | `0.3.0` 精确消费 Contracts 0.5.1 v2；38 项均确定性产出为 local-development 与 desktop-release 的 bundled/installable 条目，无 catalog-only/blocked 项。 | `make lint && make test` PASS；258 个审核文件；双渠道重复构建字节一致，正式包 manifest SHA-256 `9f8459077615514183fdd4c81ff3b6b2ef1ea735257b04c040399d4c91c1daa2`。安装/发现/Runtime 可见由下游 Host conformance 证明。 |
| `yijie-agent-host` | owner-only Skill 管理 API、App Data root 注册、启停重放、变更通知 | 实现 commit `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` 已固定；契约 commit/OpenAPI/Manifest/Runtime projection/fixtures 已精确 pin；查询、扫描、安装、启停、卸载与 Runtime 投影完成。 | `contract-check`、全仓 race tests、lint、恶意 fixture、重启重放、401/403、通知合并、local-development/desktop-release 双渠道完整生命周期及真实 pinned Runtime 38 项生命周期 PASS。 |
| `yijie-desktop` | `/plugins`、导航、store/native client、Tauri commands、resources/app-data、sidecar、目录 watcher、设计系统组件与双渠道 app overlay | 精确消费 v2/0.3.0，按五类展示 38 项并通过 Host 完成安装、启停、卸载、扫描和 Runtime 状态投影；operation/digest/path/bearer 不进入 Renderer，Tauri 不持有第二套文件事务。 | 最终 `generate:check`、548 项 demo_fast Vitest、lint/build、265 passed / 3 ignored Rust library tests、fmt/clippy、双渠道 resource/release checker、macOS app build、fresh 生命周期、401、视觉与失败恢复证据及 `copywriting` 模型真实调用均 PASS。 |
| `yijie` | Feature Package | 按 checkpoint 更新 AC、checks、artifact、diff 和限制。 | D0 与 strict D4 checker、claim audit、feature audit、lint/test 均 PASS。 |

## 4. 调试循环

| 时间 | 真实现象 | 根因/新证据 | 修复/决策 | 结果 | 累计耗时 |
|---|---|---|---|---|---:|
| 2026-08-25 | Desktop 已有“插件”导航文案，但被设为 disabled 且 router 无 `/plugins`。 | 只读检查现有 navigation/router；`plugin.read` 已存在。 | D0 纳入启用导航、新路由和新增 `plugin.manage`，避免把写权限塞入 read。 | 需求边界已固化，代码未改。 | D0 |
| 2026-08-25 | 用户源目录包含 38 个 Skill，但无图标资产、统一许可/来源证明，且部分 Skill 依赖未提供工具。 | 扫描到 5/9/7/9/8 分类、241 文件、无图片/LICENSE；至少 8 个有外部能力缺口。 | UI 使用 YjIcon/Lucide 注册键；打包前增加许可、安全、能力就绪度和 eval 门槛。 | 风险与停止条件已写入 brief，打包未执行。 | D0 |
| 2026-08-25 | 固定 Runtime 已提供 Skills API，但现有 Host compatibility projection 未覆盖。 | 核对固定 Runtime 与 contracts projection。 | 将 contract impact 定为 semantic，明确 source-first 与版本化兼容顺序；不修改 Runtime 核心。 | D0 固化架构边界；随后由本表 Contract First 记录完成增量契约。 | D0 |
| 2026-08-25 | 原始 `copywriting@0.0.94` 无 LICENSE/NOTICE 或可验证上游仓库。 | cache 的 official 标记不是再分发证明；原文件 SHA-256 已记录。 | 当时不复制原文，重写 `yijie.content-marketing.copywriting@0.1.0`；先只授权 exact `local-development`。 | 历史本地候选可确定性打包；该许可阻断后由 38 项 owner attestation 关闭。 | Contract First |
| 2026-08-25 | 跨仓请求体、权限与 Runtime 方法尚未固定。 | Contracts 新增 Bundle Manifest v1、五个 Host operations、`plugin.manage` 与四项 Runtime 投影。 | 生成 SDK，增加 canonical Host fixtures 及正常/SHA 损坏/Zip Slip 包。 | Contracts tests 45/45、双基线 breaking PASS。 | Contract First |
| 2026-08-25 | 本地服务需启动即用，但 Host API 仍应保护本机进程边界。 | 用户明确要求本地 yijie 启动后无需登录鉴权。 | 精确 local + demo_fast 由 Desktop 自动建立固定身份并透明携带 bearer；内部保留 bearer/capability，禁止扩散到 public/production。 | 语义已写入 OpenAPI、Brief 与 D4 验证计划；生产实现待 Host/Desktop。 | Contract First |
| 2026-08-25 | `0.5.0` 工作树候选不能被下游稳定消费。 | 契约内容、生成物、fixture 和原始 manifest 字节摘要语义已完成审核。 | 形成不可变本地候选 commit `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`，记录 OpenAPI/Manifest/Runtime projection 摘要。 | generate/lint/test 与两个 breaking checks 通过；候选未 tag/发布。 | Contract First |
| 2026-08-25 | Host 和 Skills 如仍读取 floating sibling 工作树，无法证明消费者与已审契约一致。 | Host 需同步 OpenAPI/Schema/projection/fixtures，Skills 需锁定 Manifest Schema。 | Host 和 Skills 均改为精确 `git-commit` pin，并对快照摘要执行 drift check。 | Host `make contract-check` 和 Skills contract lock/tests 通过；lifecycle/conformance 仍为后续工作。 | Contract First |
| 2026-08-25 | Runtime 会在 `skills/extraRoots/set` 响应前同步发出 `skills/changed`，在通知回调直接调用 `skills/list` 会阻塞 reader。 | 固定 Runtime transport 的 notification handler 在 reader goroutine 内同步执行。 | 通知回调只校验精确 `{}` 并 nonblocking 写入容量 1 的信号通道，由独立 worker 合并、退避并重放 Runtime 状态。 | response-before-notification、storm coalescing、启动暂时失败自动恢复及 race tests PASS。 | Agent Host conformance |
| 2026-08-25 | Skill archive、外部目录变化、升级中断和并发 operation 可能产生越界、半安装或错误重放。 | 文件系统和跨重启状态是 Host 消费者的持久语义边界。 | 使用 owner-only managed/staging/state、`os.Root` 相对访问、严格 archive 预检、receipt/disabled marker、分阶段 journal 与 rollback；同 operation 复用结果，异 operation 返回 `skill_busy`。 | 正常/SHA 损坏/Zip Slip、移动/损坏、升级回滚、重启冲突与并发测试 PASS。 | Agent Host conformance |
| 2026-08-25 | 技术 fixture 通过仍不能证明真实 Runtime 与真实 Skill producer 可互操作。 | 需要消费固定 Runtime 二进制及 `yijie-skills` 的实际 deterministic package。 | 执行 `make runtime-test`，并以 `YIJIE_SKILLS_BUNDLE_ROOT` 指向新产出的 local-development `copywriting` bundle 跑 race integration。 | 安装默认可见、停用不可见、Host/Runtime 重启重放、重新启用、卸载及真实包消费全部 PASS；未发起模型付费调用。 | Agent Host conformance |
| 2026-08-25 | 独立复审发现整个 managed root 注册会暴露 catalog 外 Skill、`extraRoots/set` 通知会自触发循环、operation 裁剪会遗忘幂等键、rename 后 fsync 被忽略、祖先目录可替换，以及首次 stale 请求错误映射为 409。 | 对照固定 Runtime 递归 loader 与 0.5.0 OpenAPI 逐项核验，原有 focused tests 未覆盖这些时序/安全边界。 | 改为只注册 receipt 有效的具体 Skill 根并双重拒绝嵌套 `SKILL.md`；缓存 roots；operation 永不静默裁剪；提交纳入目录 fsync/回滚；校验 Unix owner/祖先 authority；stale 首次请求映射 400。 | 新增 orphan/嵌套、pre-response feedback、70 operations+重启、fsync 故障、replaceable ancestor、stale 400 回归；全仓 race 与真实 pinned Runtime 再次 PASS，复审无新增阻断。 | Agent Host conformance review |
| 2026-08-25 | Desktop 不能从 Renderer 接收 root、digest、operation ID 或 bearer，也不能重做 Host 文件事务。 | 0.5.0 已把 catalog revision、幂等 operation 与安全错误固定在 Host 边界；App Resource/App Data 必须由 Tauri 平台 API 解析。 | 新增 closed Tauri Skills adapter：原生生成 operation ID、合并 catalog/Host 状态，只向 Renderer 暴露安全 DTO；App Data 首次启动仅创建单层 owner-only 目录，并拒绝 symlink/non-dir/权限不安全/根重叠。 | Skills Rust focused 10/10、全 Rust unit 259 PASS/3 ignored、fmt/clippy PASS；安装事务仍唯一位于 Host。 | Desktop consumer |
| 2026-08-25 | `env_clear` sidecar 必须显式获得 local profile 和两个 Skill root，但 bearer 不应通过进程参数或环境扩散。 | Host 在 readiness 后产生 owner-only token 文件，原生 bridge 已有受控 token reader。 | sidecar allowlist 显式传 `YIJIE_ENV=local`、`YIJIE_LOCAL_PROFILE=demo_fast`、bundle/install root；bearer 仅由 native bridge 从 owner-only 文件读取，Renderer 和 sidecar env/args 不接触。 | 精确环境、token 权限、401/403 与五个 Skills route 的 Rust tests 均包含在 259 项 PASS 中；fresh 进程仍待 D4。 | Desktop consumer |
| 2026-08-25 | 当时代表 Skill 只具 `local-development` 授权，直接写入默认 release 会越过停止条件。 | 历史 Desktop resource lock 的授权范围为 local-development，正式再分发证明当时缺失。 | 资源仅由 demo_fast overlay 映射；默认 build wrapper 拒绝 `--config`/`-c`/`TAURI_CONFIG` 旁路并检查默认包不含 `skill-packages`。 | 历史 resource/release boundary PASS；该许可阻断后由 38 项 owner attestation 关闭，当前待更新 Desktop resource lock。 | Desktop packaging |
| 2026-08-25 | UI 需要调用原生闭环，又不能把未知 native 字段或枚举默认为可操作。 | Renderer authority 必须比 Host wire 更窄；当前真实目录只有一个审核 Skill，并非 38 个可安装包。 | 新增闭合 native client、Pinia 收敛、`/plugins`、导航、卡片、tooltip/switch/卸载弹窗及稳定错误映射；未知字段拒绝、未知枚举降级并禁用操作。 | 10 files/77 focused tests、全量 demo_fast 71 files/517 tests、lint 和 production renderer build PASS；38 Skill 与亮暗视觉仍待验收。 | Desktop UI |
| 2026-08-25 | 第一版 demo_fast debug app 已带入资源，但构建前端时未固定 compile-time local + demo_fast gate，成品可能隐藏 `/plugins`。 | Vite profile 是编译期常量，只有 shell 启动时设置运行时环境不足以证明打包 UI 可见。 | `tauri:build:demo-fast` 显式固定五个 `VITE_*` profile/gate，并增加资源测试防回归；默认 release build 仍不设置该 gate，也不带 Skill 资源。 | 重打 debug app PASS；fresh 成品零登录显示插件入口和 1 个真实卡片。 | Desktop packaging smoke |
| 2026-08-25 | focused/build 通过仍不能证明 Tauri、Host、Runtime 和 App Data 在真实窗口内收敛。 | 需要从 fresh 进程操作真实 App Resource 与用户安装根；付费模型调用未授权。 | 启动 `pnpm tauri:dev` 验证构建/Host readiness，并用同一 demo_fast debug app 完成 `/plugins` 安装、默认启用、停用、重启重放、重新启用、确认卸载；再次安装后将受管目录移出，页面重入触发扫描并恢复未安装。 | 全部本地生命周期行为 PASS，内置 zip 保留、用户副本删除；未发起模型对话，未执行 Desktop 恶意 fixture。 | Desktop fresh happy-path smoke |
| 2026-08-25 | 37 项为 `catalog-only + blocked`，且 `copywriting@0.1.0` 仅有 local-development 授权，无法进入正式桌面资源。 | 缺少覆盖 38 个稳定 ID 的所有权/桌面再分发声明以及逐项源码与安全证据；不需要重写 37 项。 | 记录所有者声明 `FEAT-129-DESKTOP-DISTRIBUTION-2026-08-25`；保存 37 项源码快照并增加 NOTICE，保留易界版 copywriting；逐项固定来源、包树、归档、风险、能力和安全审核；产出 `yijie-skills@0.3.0` 双渠道包。 | 38 项均为 `bundled + installable`，0 blocked；`make lint/test/package/package-desktop-release` 通过，来源/许可阻断关闭。 | 38 Skill distribution closure |
| 2026-08-25 | Host 仍固定 Contracts 0.5.0 / Manifest v1 和单 Skill producer，无法确定性消费正式 38 项。 | v2 wire 只新增 blocked reason，但 Manifest 形状、错误优先级、工具辅助 Skill 可见性、producer pin 和批量生命周期均需精确验证。 | 在独立 FEAT-129 分支同步 Contracts 0.5.1，新增独立 `api/skills.lock`，升级 v1/v2 loader 与投影；以 synthetic blocked 保留 `skill_not_installable`，并对 0.3.0 双渠道和固定 Runtime 执行 38 项完整生命周期。 | `contract-check`、generate、lint、全仓 race tests、`skills-conformance`、`runtime-test` 全绿；产品目录 38 installable / 0 blocked，v1 仅保留兼容与恶意 fixture。 | Agent Host v2/38 conformance |
| 2026-08-25 | Desktop 仍固定历史 v1/单 Skill lock，不能把 Host 的 38 项 conformance 推导成桌面可交付。 | App Resource、默认正式构建、Tauri parser、Renderer catalog 和 watcher 必须同时消费同一组不可变 pin。 | 将 Desktop 迁移到独立 FEAT-129 分支；固定 Contracts `164b14f...`、Host `1b7bfd1...`、Skills `10c45be...`，新增双渠道原子同步/校验和强制 release overlay；Tauri 升级为 Manifest v2 consumer，但继续只调用 Host API。 | local `cc2b9be4...` 与 release `9f845907...` 均含 38 个已校验归档、分类 `5/9/7/9/8`；两种 macOS app build PASS。 | Desktop v2/38 packaging |
| 2026-08-25 | 工具辅助 Skill 的能力未就绪状态、外部目录移动和 Host 重启可能导致 UI 与 Runtime 状态分叉。 | Manifest v2 允许 degraded 但仍 installable；目录变化必须以 App Data 为真相，cached Host bridge 必须重建 nonce-bound 连接。 | Renderer 闭合消费 v2 blocked/readiness/icon 字段；Tauri 递归指纹 watcher 触发 Host `directory_changed` scan 并发出 content-free native event；sidecar start 每次刷新 bridge，scan 在启动/页面/恢复/升级路径自动对账。 | 539 项 Vitest、267 项 Rust tests（264 passed / 3 ignored）、lint/build/fmt/clippy PASS；fresh 真实窗口完成安装、停用、重启重放、再启用、卸载、外部移走自动恢复和原位 retry。 | Desktop lifecycle |
| 2026-08-25 | 自动化通过仍不能证明 38 卡片和危险操作在真实主题/窗口中可理解。 | FEAT-129 设计规范要求亮暗主题、安装态、删除危险态和确认弹窗的可见证据。 | 以 1180×780 真实 Tauri 窗口完成 38 卡片 light/dark、安装启用态和卸载确认弹窗检查；macOS 截图内容帧实际为 1162×768。 | 四份视觉证据已入 `evidence/`；未运行最小窗口全状态矩阵，因此不把 AC-009 或完整 D4 提前标记 PASS。 | Desktop visual evidence |
| 2026-08-25 | AC-003 要求代表 Skill 被模型真实调用，但 Feature Package 明确未授权付费调用。 | Runtime/Host 可见性测试不等于模型在真实对话中选用 Skill；不得伪造或用自动化推导付费调用证据。 | 保持 `paid_calls.allowed=false` 和实际调用 0；记录 Host/Runtime 可见性、Desktop lifecycle 与缺口，等待用户另行授权后再执行该一步。 | AC-003、real_smoke 总项和 D4 保持未通过；同样保留“真实 Desktop 恶意包 frame 未运行”的代表性 failure 缺口。 | D4 evidence review |
| 2026-08-25 | 用户明确要求修改 Brief 并允许付费调用。 | 只需要关闭 AC-003，不应把授权扩张为开放式付费预算。 | 将 `external_authorizations.paid_calls` 更新为 `allowed=true`、`max_actions=1`，用途固定为 `copywriting@0.1.0` 的一次真实模型调用；生产写入与其他付费操作仍未授权。 | 授权于 `2026-08-25T14:40:52Z` 生效；实际调用与结果在执行后回填。 | Paid-call authorization |
| 2026-08-25 | AC-003 已获 1 次限定授权，仍需证明模型使用的是受管安装目录中的准确 Skill，而非只看到目录投影。 | `runtime_visible=true` 与实际上下文注入是两层不同证据；调用必须使用真实 provider/model，并且不能提交第二个 turn。 | canonical Desktop 启动 Host，安装并确认 `copywriting` enabled/runtime-visible；以显式 `$copywriting` 和合成商品事实提交唯一一个 `--retry 0` Host turn，随后对 rollout 注入正文与已安装 `SKILL.md` 分别计算 SHA-256。 | `MiniMax-M3/minimax` turn completed；两份摘要同为 `785a47c...c328`，仅 1 个 Skill 注入、assistant message 和 task_complete；额度 1/1 用尽，AC-003 PASS。 | Paid real-call evidence |
| 2026-08-26 | 安装 tooltip 只支持鼠标，键盘用户无法获得同等提示。 | 加号按钮已有可聚焦语义，但 tooltip trigger 未覆盖 focus。 | 补齐 focus-visible 行为和 Vitest，机器截图保存键盘聚焦时的“安装”提示。 | hover/focus 均 PASS，未改变安装协议或权限边界。 | AC-002/009 accessibility |
| 2026-08-26 | scan 响应会覆盖卡片的失败状态，导致用户看不到原位 retry；Host journal 更新还会触发 watcher 再次 scan。 | Renderer 合并策略未保留可重试错误；目录指纹包含 Host 自己管理的 `.yijie-state/operations.json`。 | 保留 pending/retry 状态直到用户动作；watcher 指纹忽略 Host 管理的 `.yijie-*` 节点，但继续检测真实 Skill 内容、移动与删除；刷新精确 implementation digest lock。 | 正常页面观察期 scan `2 → 2`，真实目录变化测试仍 PASS；最终 Desktop commit 为 `6745eb793e417c6685d1900231477c59ec81a5fd`。 | State convergence |
| 2026-08-26 | AC-002/010 需要证明失败原子性与恢复，同时用户要求停止高敏感操作。 | 安装事务属于 Agent Host；Tauri 只消费接口，重复在真实应用注入危险归档没有必要。 | 真实隔离 Desktop 保留已取得的摘要失败、资源缺失、Host 不可用、安装根不可写和中断恢复证据；Zip Slip 只运行 Host 既有临时目录 fixture，并由 Desktop DTO/UI 自动化验证 `archive_unsafe` 与重试。 | 无半安装、越界文件或 Runtime 误暴露；恢复后同卡片重试 PASS。用户收紧边界后未再执行故障注入。 | Safe D4 failure matrix |
| 2026-08-26 | AC-009 的人工验收门禁已由用户明确移除。 | Checker 不要求人工签字，设计规范可由自动化状态矩阵与机器截图审计。 | Vitest 覆盖亮暗 Token、1180×760、tooltip hover/focus、loading/success/empty/error/retry、删除 danger、取消/确认/Escape 和焦点恢复；复用真实 light/dark/installed/modal 截图。 | 自动化视觉矩阵 PASS，无人工验收门禁。 | AC-009 closure |
| 2026-08-26 | watcher 修复后 implementation digest lock 与源码摘要不一致，最终门禁唯一失败。 | `resources.rs` 已更新，consumer lock 仍固定父提交摘要。 | 将 lock 精确更新为 `5353f19e...` 并重新运行 `generate:check` 与 `test:demo-fast`。 | `generate:check` PASS；72 files / 548 tests PASS，最终工作树干净。 | Final Desktop gate |

调试规则：30 分钟无新事实则停止猜测式补丁；90 分钟同一阻塞则简化到一个代表 Skill 的完整闭环；非核心验证最多 120 分钟；核心阻塞 240 分钟后重新选择架构或缩小 MVP。

## 5. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 付费模型调用 | `MiniMax-M3` / `copywriting@0.1.0` | 当前用户 / `2026-08-25T14:40:52Z` | 1 | 1 | turn `01a03982-579a-7be0-a2b1-ef46472c4e7e` completed；额度用尽，脱敏证据见 `evidence/ac-003-copywriting-real-call.md` |
| Codex 执行破坏性操作 | N/A | N/A | 0 | 0 | 未授权、未执行 |
| 生产写入 | N/A | N/A | 0 | 0 | 未授权、未执行 |

产品内的“确认卸载”已在 fresh demo_fast 窗口中按二次确认执行，只删除可重新安装的受管 Skill 副本并保留 App Resource；外部移走测试产生的临时副本已移入系统废纸篓，可恢复。该产品内、任务内行为不等同于获得删除其他用户文件的外部授权。

## 6. 已知限制与工作区保护

- D0 需求基线、Contracts 0.5.1 v2、38 项双渠道 Skills 生产者、Agent Host v2/38 lifecycle/conformance，以及 Desktop 对 0.5.1/0.3.0 的精确消费、38 卡片、双 app build、fresh 生命周期、代表 Skill 模型真实调用、分层失败恢复和自动化视觉矩阵均已完成，D4 PASS。
- 38 项所有权、桌面再分发、来源摘要和静态安全审核已由声明 `FEAT-129-DESKTOP-DISTRIBUTION-2026-08-25` 覆盖；`copywriting@0.1.0` 与其余 37 项均可进入 local-development 和 desktop-release，不再存在 FEAT-129 源码许可阻断。
- 25 项 tool-assisted Skill 声明了外部能力依赖；Host 不再以此阻断安装、启用和 Runtime 可见，但 D4 仍不能把“Skill 可调用”表述为每个外部平台操作必然成功。
- Desktop Tauri resources/sidecar、local + demo_fast 自动凭据传递、Host API consumer、目录变化通知和 38 卡片 UI 已实现并通过 focused checks；fresh 启动及安装/停用/重启保持/再启用/卸载/外部移走自动恢复/retry/401 已实测，模型真实调用由 rollout 注入摘要闭合。Zip Slip 按最新安全边界由 Agent Host 临时目录 fixture 与 Desktop DTO/UI 自动化分层验证。
- Desktop resource lock 已关闭旧单 Skill 差距并精确固定 `yijie-skills@10c45bec29603b002e861e1499d5b4e684251af5`；`local-development` 与 `desktop-release` 两渠道均为 38 项、0 blocked。最终实现已形成不可变 commit `6745eb793e417c6685d1900231477c59ec81a5fd`，但尚未 tag、push 或发布。
- Host operation journal 为保留 Contracts 0.5.1 未声明过期的幂等语义而不裁剪旧 ID；达到 4096 条后新 operation 会 fail closed 为 `skill_busy`。长期运行前需在后续契约版本明确 retention/compaction。
- 本轮 macOS 全套门禁通过；额外 Windows 交叉编译在既有 `internal/codex/runtime.go` 的 `syscall.Stat_t` 可移植性问题处失败，不由 FEAT-129 新增 authority 文件引起，但在 Windows Desktop 交付前必须另行关闭。
- `yijie`、`yijie-agent-host` 与 `yijie-desktop` 均位于独立 `feat/feat-129-desktop-skill-marketplace` 分支；Desktop 以 `d0b0eee6336550ffded16723390fc9ca01a280d4` 为隔离基线，FEAT-128 分支/提交未受影响。后续仍禁止 reset、checkout 覆盖或顺手整理无关 diff。
- 用户已授权形成不可变 Desktop commit，但未授权 push、pull、rebase、tag 或发布；当前治理文档不虚构远端或发布状态。
