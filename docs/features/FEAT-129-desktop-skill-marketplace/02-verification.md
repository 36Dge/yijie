# FEAT-129 Demo 验证

> 当前 checkpoint：`D0` 实现检查点。38 项所有权/桌面再分发、逐项来源与安全审核、Skills v2 双渠道包及 Agent Host v2/38 conformance 已通过；Desktop 仍需同步 0.3.0 资源并完成 38 卡片 UI，且未执行完整模型调用、Desktop 恶意包失败帧和视觉验收，因此下面的完整 D4 仍未通过。

## 1. D0 治理检查

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| `yijie` | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D0 docs/features/FEAT-129-desktop-skill-marketplace` | 0 | PASS：schema v3 及 D0 范围/语义门禁通过。 | 2026-08-25 |
| `yijie` | `node --test tests/codex-feature-delivery.test.mjs` | 0 | PASS：47/47。 | 2026-08-25 |
| `yijie` | `pnpm feature:audit -- --base-ref HEAD` | 0 | PASS：审计 8 个已提交 Feature Package；仅报告 5 个既有 schema v1 历史警告。FEAT-129 的 4 个治理文件已在独立分支跟踪并由 direct D0 checker 验证，当前为待提交修改。 | 2026-08-25 |
| `yijie` | `pnpm lint` | 0 | PASS：10 个仓库登记及中央 Contract First 治理校验通过。 | 2026-08-25 |
| `yijie` | `pnpm test` | 0 | PASS：48/48。 | 2026-08-25 |
| `yijie` | `bash -n docs/dev/codex-feature-delivery/scripts/*.sh` | 0 | PASS。 | 2026-08-25 |

### 历史 v1 候选与当前 Contracts 0.5.1 / Manifest v2 consumer pin

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| `yijie-contracts` | `git rev-parse HEAD` 及权威源 SHA-256 核对 | 0 | PASS：本地不可变候选 commit 为 `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`（未 tag/发布）；Agent Host OpenAPI `406b55dad02d5a3d489955bcf29c973b94252c3e300f8ff853709a71d6874431`，Manifest v1 `d86185a1d5f4d9a136c88b679d50ac3e83bcc2b722eee39cba674c5be3b88469`，Runtime projection `6b7662d4237486300456f16abd0305fe1ea267b70a85e497ba7ab15a654939ee`。 | 2026-08-25 |
| `yijie-contracts` | `pnpm generate` | 0 | PASS：OpenAPI/Protobuf/12 个 JSON Schema 的 SDK 生成物同步。 | 2026-08-25 |
| `yijie-contracts` | `pnpm lint` | 0 | PASS：OpenAPI、AsyncAPI、JSON Schema、Protobuf 与生成漂移检查通过。 | 2026-08-25 |
| `yijie-contracts` | `pnpm test` | 0 | PASS：45/45 Node tests 与全部 Go packages；包含 Host Skills canonical fixtures、manifest、摘要损坏、Zip Slip 及可复现 fixture。 | 2026-08-25 |
| `yijie-contracts` | `pnpm breaking HEAD` | 0 | PASS：相对当前工作基线无结构 breaking。 | 2026-08-25 |
| `yijie-contracts` | `pnpm breaking ea48fe190e18afba728712d1e2cc79cda57f581b` | 0 | PASS：相对 FEAT-129 契约增量前的完整 commit 无结构 breaking。 | 2026-08-25 |
| `yijie-contracts` | `git rev-parse HEAD`、`pnpm generate && pnpm lint && pnpm test` 及 breaking checks | 0 | PASS：Catalog First `0.5.1` 不可变 commit `164b14f609537d727a52326832da04430aecc4ab`；Manifest v2 SHA-256 `39a898111ba3dcae2f369fdcb571a2e892830d1d0a57c90ab6210a0ab897a649`，38 项 fixture 分类为 `5/9/7/9/8`。 | 2026-08-25 |
| `yijie-agent-host` | 历史 `make contract-check` | 0 | PASS（历史 0.5.0 检查点）：Host 当时精确 pin commit `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`；已被下方 0.5.1/v2 门禁取代。 | 2026-08-25 |
| `yijie-agent-host` | `make test` | 0 | PASS：`contract-check` 后执行全仓 `go test -race -cover ./...`；五接口、wire fixture、原子安装/回滚、路径/祖先安全、70+ operation 幂等/冲突、重启重放、401/403、通知合并与 feedback-loop 上界均通过。 | 2026-08-25 |
| `yijie-agent-host` | `make lint` | 0 | PASS：全仓 `go vet` 与 shell 语法检查通过；Go format 与 `git diff --check` 无输出。 | 2026-08-25 |
| `yijie-agent-host` | `make runtime-test` | 0 | PASS：使用固定本地 Runtime 二进制/manifest 完成精确 Skill roots、catalog 外 orphan 不可见、安装默认可见、停用不可见、Host/Runtime 重启重放、重新启用和卸载不可见。 | 2026-08-25 |
| `yijie-agent-host` | 历史单 Skill producer integration | 0 | PASS（历史 0.5.0 检查点）：消费实际 `copywriting@0.1.0` local-development bundle；已被下方双渠道 38 项 conformance 取代。 | 2026-08-25 |
| `yijie-agent-host` | `make generate && make contract-check && make lint && make test` | 0 | PASS：精确 pin Contracts 0.5.1 commit `164b14f609537d727a52326832da04430aecc4ab`、Manifest v2 SHA-256 `39a898111ba3dcae2f369fdcb571a2e892830d1d0a57c90ab6210a0ab897a649`；生成物、快照、格式、vet、shell 和全仓 race/coverage 无漂移。 | 2026-08-25 |
| `yijie-agent-host` | `make skills-conformance` | 0 | PASS：从干净 `yijie-skills@0.3.0` commit `10c45bec29603b002e861e1499d5b4e684251af5` 重建 local-development/desktop-release；38 项分类 `5/9/7/9/8`、0 blocked、归档逐字节一致，并在两个渠道各完成查询、扫描、安装、启停、目录移走、重启重放与卸载。 | 2026-08-25 |
| `yijie-agent-host` | `make runtime-test`（Contracts 0.5.1 增量） | 0 | PASS：除既有 Runtime 门禁外，真实固定 Codex Runtime 对 38 项执行安装可见、全部停用、Host/Runtime 重启重放、全部重新启用和卸载；不调用模型、不需要用户登录。 | 2026-08-25 |
| `yijie-agent-host` | `git rev-parse HEAD && git status --short` | 0 | PASS：v2/38 consumer 已形成不可变实现 commit `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`，位于独立 `feat/feat-129-desktop-skill-marketplace` 分支；提交后工作树干净。 | 2026-08-25 |
| `yijie-skills` | 历史 `pnpm lint && pnpm test && pnpm package` | 0 | PASS（历史单 Skill 检查点）：代表包重复构建一致；已被下方 0.3.0/38 项门禁取代。 | 2026-08-25 |
| `yijie-skills` | 历史 0.5.0 contract lock 核对 | 0 | PASS（历史单 Skill 检查点）：当时精确锁定 `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`；当前权威为下方 0.5.1/0.3.0 记录。 | 2026-08-25 |
| `yijie-skills` | 历史 `quick_validate.py` copywriting | 0 | PASS（历史单 Skill 检查点）；当前 38 项由 0.3.0 全量 lint/test/audit 取代。 | 2026-08-25 |
| `yijie-skills` | `make lint && make test && make package && make package-desktop-release` | 0 | PASS：`0.3.0` commit `10c45bec29603b002e861e1499d5b4e684251af5` 精确消费 Contracts 0.5.1 v2；38 项均 `bundled + installable`、0 blocked，258 个审核文件，双渠道重复构建字节一致。local manifest `cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5`，desktop-release manifest `9f8459077615514183fdd4c81ff3b6b2ef1ea735257b04c040399d4c91c1daa2`。 | 2026-08-25 |
| `yijie-desktop` | `pnpm generate:check` | 0 | PASS：Public API、Agent Host v2/v3 与 Skills v1 均精确 pin `d6dff903e0c12b6a5e69599df1e33ef46d8bea6b`；Skills lock 固定三份权威摘要、fixture tree 和 10 个已实现 Rust consumer 文件摘要，输出 `native consumer pins are complete`。 | 2026-08-25 |
| `yijie-desktop` | `pnpm skills:sync:local && pnpm skills:check:local && pnpm skills:release-boundary` | 0 | PASS：从 `yijie-skills@c0aaba17f9ba5534e133b67b9eac43bb7210694f` 生成并复验 1 个 local + demo_fast 资源；manifest SHA-256 `091de202783ae2658d3a8ce3c0ceaedfef023d71fa84c94ff040e72c9421bb2c`、archive SHA-256 `987dae7003064fa1d0b00a37be0f130eb973a55f966fbf43faf2ed8af84c5138`。默认 Tauri 配置不含 local-development Skill，配置覆盖旁路 fail closed。 | 2026-08-25 |
| `yijie-desktop` | `pnpm tauri:build:demo-fast` | 0 | PASS：macOS debug app 构建成功；`易界 AI.app/Contents/Resources/skill-packages/` 中 manifest/zip 摘要与 Desktop resource lock 一致。该结果仅证明 local-development 调试包，不是正式发行包。 | 2026-08-25 |
| `yijie-desktop` | `pnpm test:demo-fast` | 0 | PASS：`generate:check` 后 71 files / 517 tests；包含 Skills contract/release boundary、demo_fast 编译期 profile、native client、store、卡片、页面、路由、导航和权限回归。 | 2026-08-25 |
| `yijie-desktop` | `pnpm exec vitest run src/domain/skill-marketplace.test.ts src/api/skill-native-client.test.ts src/stores/skill.store.test.ts src/components/skills/SkillCard.test.ts src/pages/plugins/SkillMarketplacePage.test.ts src/authorization/skill-marketplace-ui-config.test.ts src/navigation/app-nav.test.ts src/authorization/app-permission-policy.test.ts src/router/index.test.ts src/components/yijie/YjSidebar.test.ts` | 0 | PASS：FEAT-129 UI focused 10 files / 77 tests。 | 2026-08-25 |
| `yijie-desktop` | `pnpm lint`；`pnpm build` | 0 | PASS：全仓 ESLint、Vue typecheck 与 production renderer build 通过；Skill Marketplace chunk 已生成。 | 2026-08-25 |
| `yijie-desktop/src-tauri` | `cargo fmt --check`；`cargo clippy --lib -- -D warnings`；`cargo test --lib` | 0 | PASS：Rust format/clippy 通过；259 passed / 0 failed / 3 environment tests ignored。包含 App Resource/App Data、owner-only/symlink/重叠、exact profile/root、owner token、Skills route/401/403 和安全错误投影。 | 2026-08-25 |

边界说明：上表证明 Contracts v2、38 项确定性 Skill 生产者和 Agent Host 五接口/Runtime 投影已经闭环；Desktop/Tauri/UI 仍精确消费旧单 Skill 资源。Tauri 只消费 Host API，不实现安装事务。只有完成 Desktop 0.3.0 资源同步、38 卡片 UI 和 fresh smoke 后，才能证明完整桌面跨仓生命周期；当前仍不证明模型真实对话、完整视觉、Desktop 恶意 fixture 或 D4 已完成。

## 2. D4 真实服务启动与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Startup/readiness | 在 `yijie-desktop` 执行 `pnpm tauri:dev`；确认 Tauri、Agent Host、固定 Runtime readiness，整个正常流程不出现登录页、账号鉴权或手动授权并直接打开 `/plugins`。 | fresh Desktop process；`YIJIE_ENV=local`、`YIJIE_LOCAL_PROFILE=demo_fast`；无云端 Skill 服务 | `pnpm tauri:dev` 完成资源同步、Vite/Rust 构建并启动 Host；随后从 fresh demo_fast debug app 进入 `/plugins`，无登录、账号鉴权或授权弹窗。由于完整 D4 还缺另外两组证据，本项不单独升格总 Gate。 | PASS (partial D4) |
| Real happy path | 断网安装自包含代表 Skill → `skills/list` enabled → 新一轮模型真实调用 → 关闭并验证下一轮不可见 → 重启保持 → 开启 → 卸载 → 外部删除同步。 | 真实 App Resource/App Data、真实 Agent Host 与固定 Runtime；非 mock | 在真实窗口完成安装并显示“模型可用”、停用、Desktop/Host 重启后保持启用、重新启用、确认卸载；核对用户副本删除且内置 zip 保留。再次安装并把目录移走后，页面重入扫描恢复未安装。未发起付费模型真实对话，也未验证即时 watcher 推送，因此完整项仍未通过。 | PARTIAL |
| Representative failure/retry | 使用摘要损坏或 Zip Slip fixture 点击安装；确认拒绝、无半安装/注册残留、模型不可见、原卡片显示原因并可重试。 | 真实 Host 文件边界与本地恶意 fixture；接 Desktop UI | Host 已真实拒绝摘要损坏与 Zip Slip 且无残留；Desktop 已实现稳定错误映射和原位重试状态并通过组件测试，但尚未经真实 Tauri frame 点击恶意 fixture。 | NOT RUN |

## 3. Focused checks

| Repository | Checks | 当前结果 |
|---|---|---|
| `yijie-contracts` | generate、schema lint/test、breaking、Host 查询投影与 Runtime compatibility projection | PASS：`0.5.1` Catalog First v2 不可变 commit `164b14f609537d727a52326832da04430aecc4ab` 及 Manifest v2 摘要已记录；v1 历史候选保持不变。 |
| `yijie-skills` | frontmatter、38 项来源/许可、安全、能力依赖、eval、确定性双渠道打包、contract lock 与摘要一致 | PASS：38/38 `bundled + installable`，声明 `FEAT-129-DESKTOP-DISTRIBUTION-2026-08-25` 同时授权 local-development 与 desktop-release；0 blocked。 |
| `yijie-agent-host` | 精确 Contracts 0.5.1 与 Skills 0.3.0 producer pin、snapshot drift | PASS：`make contract-check`、`scripts/check-skills-producer.sh`。 |
| `yijie-agent-host` | 38 项查询/扫描/安装/启停/卸载、synthetic blocked、owner-only bearer、权限、Runtime 映射、重启重放、摘要损坏、Zip Slip、资源缺失、目录移动与双渠道 conformance | PASS：`make test`、`make lint`、`make skills-conformance`、`make runtime-test`。 |
| `yijie-desktop` contract/resource | Skills v1 pin、fixture 和 10 个 consumer 摘要；旧 local resource sync/check；demo_fast app resource | 历史 focused checks PASS；当前尚未精确消费 Contracts v2 和 `yijie-skills@0.3.0`，因此 38 项正式资源同步为 NOT RUN，不再受许可阻断。 |
| `yijie-desktop` TypeScript | navigation/router、权限、闭合 native projection、状态收敛、重复点击、modal、错误/重试 | PASS：FEAT-129 focused 10 files/77 tests；全量 demo_fast 71 files/517 tests；lint/build PASS。页面重入目录变化已实测；即时通知和升级不由组件测试推导。 |
| `yijie-desktop` Rust | Resource/App Data root、首次启动 owner-only 创建、symlink/non-dir/权限/重叠拒绝、exact profile/root、owner token、五个 Host API adapter、安全错误 DTO | PASS：全 Rust unit 259/0/3 ignored、fmt/clippy PASS。SHA、Zip Slip、原子安装/回滚和受管删除由 Agent Host 独占并使用其 conformance 证据，不在 Tauri 重复实现。 |
| UI | 设计 Token、YjIcon/Lucide、tooltip、switch、删除 hover/focus、确认弹窗、loading/error/retry、键盘交互 | 自动化 PASS；1180×760 亮/暗、最小窗口与真实 native 状态截图仍为 NOT RUN。 |

## 4. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-001 | NOT RUN | `/plugins` 路由、导航、设计系统页面与真实 native DTO 已实现；Skills producer 已产出五类 `5/9/7/9/8` 的 38 项审核包，但 Desktop 资源锁尚未同步 0.3.0，仍需 38 卡片和亮暗主题 fresh 截图。 |
| AC-002 | NOT RUN | 真实 App Resource 点击离线安装已 PASS；Host 恶意归档、Desktop tooltip/重复点击 focused tests 已 PASS。仍缺真实 Desktop 恶意 fixture 与同帧失败无残留证据。 |
| AC-003 | NOT RUN | Host/真实 pinned Runtime 可见性已 PASS；D4 仍需 Desktop frame 和模型真实对话调用证据。 |
| AC-004 | NOT RUN | Host 启停/Runtime 重放与 Desktop 开关、Desktop/Host 重启保持已 PASS；仍缺下一轮真实模型对话可见性证据。 |
| AC-005 | NOT RUN | 指定 modal、确认卸载、用户副本删除和内置源保留已实测，hover/focus 自动化 PASS；仍缺取消/键盘及完整视觉截图。 |
| AC-006 | NOT RUN | 外部移走后页面重入扫描恢复未安装已实测，startup/page_open/window_resume tests PASS；即时目录通知、损坏、升级和完整 Runtime/UI 同步仍待 D4。 |
| AC-007 | NOT RUN | D4 需提供双版本升级、新增、下架与失败回滚测试。 |
| AC-008 | NOT RUN | fresh local + demo_fast 零登录进入 `/plugins`、root/owner bearer 消费已实测；Host 401→403 与 renderer 无 bearer tests PASS。仍缺 public/production 负向真实入口证据。 |
| AC-009 | NOT RUN | 设计系统组件和交互自动化已 PASS；D4 仍需 UI Review Checklist、亮暗/最小窗口和全状态视觉证据。 |
| AC-010 | NOT RUN | Host 原子失败测试及 Desktop 稳定错误/重试映射已 PASS；资源缺失、只读、磁盘失败、Host 不可用和升级中断的真实同帧恢复仍待 D4。 |

## 5. UI 与真实结果

- UI 权威：`yijie-desktop/docs/design/docs/design/`；必须遵循 tokens、Naive UI、YjIcon/Lucide、App Shell、亮暗主题和 accessibility 规范。
- 需求输入参考：[Skill 卡片图标区域](references/skill-card-icon-reference.png)。该图仅表达每张卡片具有图标区域，不覆盖设计系统。
- D4 artifacts：至少包含 1180×760 亮/暗首屏、安装 tooltip/loading/success、删除默认/hover/danger、卸载 modal、empty/error/retry 和键盘 focus。
- Loading/error/retry 不困住用户的判断：NOT RUN；需同时核对 UI 反馈、文件原子性和 Runtime 可见性。
- 最终真实用户结果：PARTIAL；fresh real-service happy path 已发生，但完整 D4 仍需模型真实调用、代表性 Desktop 失败帧和其余 Must AC，不接受以本次部分 smoke 推导全部完成。

## 6. Diff 与限制

- 当前治理 diff 核对：`git diff --check` exit 0；Feature Package 内无占位词或行尾空白；4 个治理文件均为独立 FEAT-129 分支上的 tracked modifications。仓库其他既有改动不属于本需求并保持原状。
- D4 必须逐仓记录 base/head、完整 diff 审阅、生成文件、无关工作树改动和 focused check 输出。
- 已知限制：38 项源码所有权、桌面再分发、来源摘要和静态安全审核已关闭；授权同时覆盖 local-development 与 desktop-release，不再存在 `copywriting@0.1.0` 或其余 37 项的 FEAT-129 许可阻断。
- 已知限制：外部平台 API、账号、数据访问和高影响写操作仍受 Runtime/Agent Host 权限与对应服务条件控制；这不影响 38 项安装、Runtime 发现和调用，但不能把 Skill 可调用表述为外部平台一定成功。
- 已知限制：Agent Host 已完成 Manifest v2/38 conformance；Desktop 仍固定旧单 Skill resource lock，下一步必须同步 Tauri/Desktop 0.3.0 资源并实现 38 卡片 UI。当前模型真实对话、即时目录通知/升级/故障、38 Skill UI 与完整视觉尚未验证。
- 已知限制：Host operation journal 不裁剪已用 ID，达到 4096 条后新 operation 返回 `skill_busy`；后续版本需先在契约中定义 retention/compaction，不能单方面遗忘旧 ID。
- 已知限制：macOS 验证全绿；额外 Windows 交叉编译被既有 `internal/codex/runtime.go` 的 `syscall.Stat_t` 依赖阻断，Windows Desktop 交付前仍需关闭该非 FEAT-129 回归项。

## 7. Public Demo

- `exposure=local`，`public_readiness.required=false`；密钥、鉴权、频率限制和公网 smoke 的 DP gate 不适用。
- `demo_fast` 固定身份例外只能在精确 local profile 中生效，不得扩散到 public/production。
- 免登录只表示 Desktop 自动建立本地身份并透明提供 owner-only bearer；Host 内部 bearer 与 capability 校验必须保留。

## 8. 结论

- `D0` 需求基线：PASS；schema/语义、治理测试、feature audit、lint、项目测试与脚本语法均通过。
- `D4` 本地真实可用：NOT RUN。
- `DP` 公开 Demo 可用：N/A。
- 验证日期：2026-08-25；D4 时间在真实验证后填写。
