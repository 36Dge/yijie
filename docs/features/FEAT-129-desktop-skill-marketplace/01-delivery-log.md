# FEAT-129 整体实现与调试记录

> 当前 checkpoint：`D0` 实现检查点。38 项 Skill 的所有权/桌面再分发声明、逐项来源摘要与安全审核已完成，`yijie-skills@0.3.0` 已产出双渠道确定性包，Agent Host 已完成 Contracts 0.5.1 / Manifest v2 的 38 项 conformance；下一步是同步 Tauri/Desktop 的 0.3.0 正式资源与 38 卡片 UI，再执行完整 D4。

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
| `yijie-desktop` | `contracts/agent-host-skills-v1.lock.json`、`contracts/desktop-skill-bundle-local.lock.json`、resource/release checker、Tauri `skills`/sidecar/native auth、`/plugins` 路由/导航/store/page/card | 历史 consumer 精确 pin Contracts 0.5.0 commit `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`；解析并校验 App Resource/App Data，向 Host 传递 exact profile/root，原生读取 owner-only bearer；实现五个安全 Tauri command、闭合 Renderer projection、页面状态和设计系统交互。Tauri 仅消费 Host API，不实现安装/解压/回滚/删除事务。 | 保持“App Resource 安装源、Host 文件事务、App Data 安装真相、Renderer 无 authority”的单一边界；0.5.1/0.3.0 精确消费仍待下一阶段。 |
| `yijie-desktop` | resource sync、`tauri.demo-fast.conf.json`、默认 build wrapper | 历史检查点只把一个已审核 `local-development` Skill 同步到 `.local/skill-packages` 并映射进 demo_fast debug app；默认 Tauri 配置不带该资源且配置旁路 fail closed。 | 当时用于隔离尚未关闭的许可风险；许可现已关闭，当前差距是 Desktop consumer 版本与 38 项资源同步。 |

本轮已完成 `yijie-agent-host` lifecycle/conformance，以及 `yijie-desktop` 的契约快照、资源打包、Tauri consumer、UI focused 实现和 fresh local + demo_fast happy-path smoke。固定 `yijie-codex` 作为未修改真实上游参与 Host 与 Desktop 启动；没有发起付费模型对话，Desktop 恶意包失败帧与完整视觉验收尚未执行。

## 3. 实施矩阵

| Repository | 计划模块 | 计划行为 | Gate 证据 |
|---|---|---|---|
| `yijie-contracts` | Bundle Manifest schema、Host operation、Runtime compatibility projection、权限枚举 | `0.5.0` v1 历史闭环保持不变；Catalog First v2 已形成 `0.5.1` 不可变 commit `164b14f609537d727a52326832da04430aecc4ab`。 | v2 generate/lint/test/breaking checks PASS；Manifest v2 SHA-256 `39a898111ba3dcae2f369fdcb571a2e892830d1d0a57c90ab6210a0ab897a649`。 |
| `yijie-skills` | 38 项来源/许可、icon、风险、能力依赖、安全审核与确定性 packager | `0.3.0` 精确消费 Contracts 0.5.1 v2；38 项均确定性产出为 local-development 与 desktop-release 的 bundled/installable 条目，无 catalog-only/blocked 项。 | `make lint && make test` PASS；258 个审核文件；双渠道重复构建字节一致，正式包 manifest SHA-256 `9f8459077615514183fdd4c81ff3b6b2ef1ea735257b04c040399d4c91c1daa2`。安装/发现/Runtime 可见由下游 Host conformance 证明。 |
| `yijie-agent-host` | owner-only Skill 管理 API、App Data root 注册、启停重放、变更通知 | 实现 commit `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed` 已固定；契约 commit/OpenAPI/Manifest/Runtime projection/fixtures 已精确 pin；查询、扫描、安装、启停、卸载与 Runtime 投影完成。 | `contract-check`、全仓 race tests、lint、恶意 fixture、重启重放、401/403、通知合并、local-development/desktop-release 双渠道完整生命周期及真实 pinned Runtime 38 项生命周期 PASS。 |
| `yijie-desktop` | `/plugins`、导航、store/native client、Tauri commands、resources/app-data、sidecar、设计系统组件 | 已实现一个审核 Skill 的离线目录投影及安装/启停/卸载 Host API 消费；operation/digest/path/bearer 不进入 Renderer，Tauri 不持有第二套文件事务。升级/目录监听全路径和 38 Skill 尚未验收。 | `generate:check`、517 项 demo_fast Vitest、lint/build、259 项 Rust unit、fmt/clippy、资源/release checker、macOS demo_fast debug app build及一轮 fresh 安装/启停/重启/卸载/外部移走 smoke PASS；完整 D4 与视觉截图待执行。 |
| `yijie` | Feature Package | 按 checkpoint 更新 AC、checks、artifact、diff 和限制。 | D0/D4 checker 与 feature audit PASS。 |

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

调试规则：30 分钟无新事实则停止猜测式补丁；90 分钟同一阻塞则简化到一个代表 Skill 的完整闭环；非核心验证最多 120 分钟；核心阻塞 240 分钟后重新选择架构或缩小 MVP。

## 5. 外部授权与实际调用

| 类型 | Provider/目标 | 批准人/时间 | 上限 | 已用 | 结果 |
|---|---|---|---:|---:|---|
| 付费调用 | N/A | N/A | 0 | 0 | 未授权、未调用 |
| Codex 执行破坏性操作 | N/A | N/A | 0 | 0 | 未授权、未执行 |
| 生产写入 | N/A | N/A | 0 | 0 | 未授权、未执行 |

产品内的“确认卸载”已在 fresh demo_fast 窗口中按二次确认执行，只删除可重新安装的受管 Skill 副本并保留 App Resource；外部移走测试产生的临时副本已移入系统废纸篓，可恢复。该产品内、任务内行为不等同于获得删除其他用户文件的外部授权。

## 6. 已知限制与工作区保护

- D0 需求基线、Contracts 0.5.1 v2、38 项双渠道 Skills 生产者、Agent Host v2/38 lifecycle/conformance，以及 Desktop Tauri/UI focused 实现和旧单 Skill fresh happy-path smoke 已完成；由于 Desktop 尚未同步 0.3.0/38 项，且仍缺模型真实调用、Desktop 恶意包失败帧和完整视觉，所有完整 AC/D4 仍为 `NOT RUN`/`pending`。
- 38 项所有权、桌面再分发、来源摘要和静态安全审核已由声明 `FEAT-129-DESKTOP-DISTRIBUTION-2026-08-25` 覆盖；`copywriting@0.1.0` 与其余 37 项均可进入 local-development 和 desktop-release，不再存在 FEAT-129 源码许可阻断。
- 25 项 tool-assisted Skill 声明了外部能力依赖；Host 不再以此阻断安装、启用和 Runtime 可见，但 D4 仍不能把“Skill 可调用”表述为每个外部平台操作必然成功。
- Desktop Tauri resources/sidecar、local + demo_fast 自动凭据传递、Host API consumer 与 UI 已实现并通过 focused checks；fresh 启动及安装/启停/重启/卸载/页面重入外部移走已实测，但仍不替代真实模型对话、即时目录通知、升级、故障注入和完整视觉验收。
- Agent Host 的 Contracts v2 与 Skills 0.3.0 消费已关闭；Desktop resource lock 仍固定旧的单 Skill producer `yijie-skills@c0aaba17f9ba5534e133b67b9eac43bb7210694f`。下一步只能更新 Tauri/Desktop 资源与 38 卡片，不能据 Host conformance 提前宣称 AC-001 已完成。
- Host operation journal 为保留 Contracts 0.5.1 未声明过期的幂等语义而不裁剪旧 ID；达到 4096 条后新 operation 会 fail closed 为 `skill_busy`。长期运行前需在后续契约版本明确 retention/compaction。
- 本轮 macOS 全套门禁通过；额外 Windows 交叉编译在既有 `internal/codex/runtime.go` 的 `syscall.Stat_t` 可移植性问题处失败，不由 FEAT-129 新增 authority 文件引起，但在 Windows Desktop 交付前必须另行关闭。
- `yijie` 与 `yijie-agent-host` 已迁移到独立 `feat/feat-129-desktop-skill-marketplace` 分支；`yijie-desktop` 仍保留既有 FEAT-128 分支/工作，不在本阶段修改。后续仍禁止 reset、checkout 覆盖或顺手整理无关 diff。
- 用户已明确授权形成不可变 Agent Host commit；未授权 push、pull/rebase 或提交 Desktop/其他仓库，故这些外部状态保持不变。
