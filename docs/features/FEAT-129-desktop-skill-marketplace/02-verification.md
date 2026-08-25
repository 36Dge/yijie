# FEAT-129 Demo 验证

> 当前 checkpoint：`D4 evidence collected / gate not passed`。Desktop 已精确消费 Contracts 0.5.1、Agent Host immutable commit 与 Skills 0.3.0，完成双渠道 38 项资源、38 卡片 UI、真实本地生命周期、四份视觉证据及 `copywriting@0.1.0` 的唯一一次真实付费模型调用；真实 Desktop frame 恶意包和剩余视觉/故障矩阵尚未闭合，因此完整 D4 仍未通过。

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
| `yijie-desktop` | 历史 v1 `pnpm generate:check`、单 Skill resource check/build、517 Vitest、259 Rust tests | 0 | PASS（历史检查点）：单 Skill Tauri/Renderer consumer 与 demo_fast debug app 已闭环；该结果已被下方 0.5.1/38 项验证取代。 | 2026-08-25 |
| `yijie-desktop` | `pnpm skills:sync:all && pnpm skills:check && pnpm skills:release-boundary && pnpm generate:check` | 0 | PASS：精确锁定 Contracts `164b14f609537d727a52326832da04430aecc4ab`、Host `1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`、Skills `10c45bec29603b002e861e1499d5b4e684251af5`；local/release 各 38 个归档、分类 `5/9/7/9/8`、跨渠道字节一致。manifest 分别为 `cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5` 与 `9f8459077615514183fdd4c81ff3b6b2ef1ea735257b04c040399d4c91c1daa2`。 | 2026-08-25 |
| `yijie-desktop` | `pnpm test:demo-fast` | 0 | PASS：`generate:check` 后共 539 项 Vitest；覆盖 v2 catalog/readiness/blocked 语义、双渠道资源边界、native event、store/card/page、安装 loading/error/retry、启停、卸载 modal、路由、导航和权限回归。 | 2026-08-25 |
| `yijie-desktop` | `pnpm lint && pnpm build` | 0 | PASS：全仓 ESLint、Vue typecheck 与 production renderer build 通过；Skill Marketplace chunk 已生成。 | 2026-08-25 |
| `yijie-desktop/src-tauri` | `cargo fmt --all -- --check && cargo clippy --locked --all-targets -- -D warnings && YIJIE_DESKTOP_SKILL_BUNDLE_TEST_ROOT=../.local/skill-packages cargo test --locked --lib` | 0 | PASS：共 267 项，264 passed / 0 failed / 3 environment tests ignored；实际解析 38 项 Manifest v2 与归档，覆盖 App Resource/App Data、owner-only/symlink/重叠、exact profile/root、token、五接口、目录 watcher、重启桥接、升级重放及安全错误投影。 | 2026-08-25 |
| `yijie-desktop` | `pnpm tauri:build:demo-fast`；`pnpm tauri:build -- --debug --bundles app --no-sign` | 0 | PASS：demo_fast app 精确嵌入 `local-development`，默认 Desktop build 强制嵌入 `desktop-release` overlay；两种 macOS app 都包含 38 个已校验归档，release wrapper 拒绝 config 旁路。此处“desktop-release”仅表示审核资源渠道，不等同于已签名/公证/发布。 | 2026-08-25 |

边界说明：上表证明 Contracts v2、38 项确定性 Skill 生产者、Agent Host 五接口/Runtime 投影，以及 Desktop/Tauri/UI 的 0.3.0 精确消费均已闭环；Tauri 只消费 Host API，不实现安装事务。模型真实调用已由下方独立 rollout 证据闭合，但真实 Desktop 恶意 fixture 仍未运行，故不能据此宣布完整 D4。

## 2. D4 真实服务启动与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Startup/readiness | 在 `yijie-desktop` 执行 `pnpm tauri:dev`；确认 Tauri、Agent Host、固定 Runtime readiness，整个正常流程不出现登录页、账号鉴权或手动授权并直接打开 `/plugins`。 | fresh Desktop process；`YIJIE_ENV=local`、`YIJIE_LOCAL_PROFILE=demo_fast`；无云端 Skill 服务 | canonical runner 先复验 exact Host/Contracts/Skills 与 38 项 local-development 资源，再启动 Vite/Tauri/Host/Runtime；fresh app 零登录进入 `/plugins`。无 bearer 的直接 Host 请求返回 401，证明本地免登录没有移除内部边界。 | PASS |
| Real happy path | 断网安装自包含代表 Skill → `skills/list` enabled → 新一轮模型真实调用 → 关闭并验证下一轮不可见 → 重启保持 → 开启 → 卸载 → 外部删除同步。 | 真实 App Resource/App Data、真实 Agent Host 与固定 Runtime；非 mock | 真实窗口显示五类 `5/9/7/9/8` 共 38 项；完成安装默认启用、停用、Desktop/Host 重启保持、重新启用、确认卸载、再次安装、外部移走后 watcher/scan 恢复未安装，并验证原位 retry。唯一一次授权的 `MiniMax-M3/minimax` turn completed，Runtime 注入正文摘要与受管 `copywriting` `SKILL.md` 完全一致。 | PASS |
| Representative failure/retry | 使用摘要损坏或 Zip Slip fixture 点击安装；确认拒绝、无半安装/注册残留、模型不可见、原卡片显示原因并可重试。 | 真实 Host 文件边界与本地恶意 fixture；接 Desktop UI | Host 已真实拒绝摘要损坏与 Zip Slip 且无残留；Desktop 已实现稳定错误映射和原位重试状态并通过组件测试，但尚未经真实 Tauri frame 点击恶意 fixture。 | NOT RUN |

## 3. Focused checks

| Repository | Checks | 当前结果 |
|---|---|---|
| `yijie-contracts` | generate、schema lint/test、breaking、Host 查询投影与 Runtime compatibility projection | PASS：`0.5.1` Catalog First v2 不可变 commit `164b14f609537d727a52326832da04430aecc4ab` 及 Manifest v2 摘要已记录；v1 历史候选保持不变。 |
| `yijie-skills` | frontmatter、38 项来源/许可、安全、能力依赖、eval、确定性双渠道打包、contract lock 与摘要一致 | PASS：38/38 `bundled + installable`，声明 `FEAT-129-DESKTOP-DISTRIBUTION-2026-08-25` 同时授权 local-development 与 desktop-release；0 blocked。 |
| `yijie-agent-host` | 精确 Contracts 0.5.1 与 Skills 0.3.0 producer pin、snapshot drift | PASS：`make contract-check`、`scripts/check-skills-producer.sh`。 |
| `yijie-agent-host` | 38 项查询/扫描/安装/启停/卸载、synthetic blocked、owner-only bearer、权限、Runtime 映射、重启重放、摘要损坏、Zip Slip、资源缺失、目录移动与双渠道 conformance | PASS：`make test`、`make lint`、`make skills-conformance`、`make runtime-test`。 |
| `yijie-desktop` contract/resource | exact Contracts/Host/Skills pin、Manifest v2、38 个归档、双渠道、分类与 release overlay | PASS：local `cc2b9be4...`、release `9f845907...`，各 38 项、分类 `5/9/7/9/8`、全部归档摘要通过；默认 build 强制 desktop-release，demo_fast 只消费 local-development。 |
| `yijie-desktop` TypeScript | navigation/router、权限、闭合 v2 native projection、状态收敛、目录事件、重复点击、modal、错误/重试 | PASS：全量 demo_fast 539 tests；lint/build PASS。外部目录移动和 retry 已在真实窗口实测。 |
| `yijie-desktop` Rust | Resource/App Data、owner-only/symlink/重叠、exact profile/root/token、五个 Host API adapter、v2 catalog、目录 watcher、升级/重启、安全错误 DTO | PASS：共 267 项，264 passed / 0 failed / 3 ignored，fmt/clippy PASS。SHA、Zip Slip、原子安装/回滚和受管删除仍由 Agent Host 独占，不在 Tauri 重复实现。 |
| UI | 设计 Token、YjIcon/Lucide、38 卡片、tooltip、switch、删除危险态、确认弹窗、loading/error/retry、键盘自动化 | 自动化 PASS；真实 light/dark、installed、uninstall modal 四份截图已保存。最小窗口与完整全状态人工矩阵尚未运行，故 AC-009 保持 pending。 |

## 4. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-001 | PASS | fresh `/plugins` 真实展示 38 项与 `5/9/7/9/8`；light/dark 截图和 iconKey 自动化均已保存/通过。 |
| AC-002 | PENDING | 正常离线安装、tooltip、loading 和重复点击已通过；Host 恶意归档 conformance 已通过，但摘要损坏/Zip Slip 尚未接入真实 Desktop frame，不能用分层证据冒充同帧验收。 |
| AC-003 | PASS | 安装默认启用且 Host 投影为 runtime-visible；唯一一次授权的真实 turn 使用 `MiniMax-M3/minimax` 完成，rollout 中 `copywriting` 注入正文与已安装 `SKILL.md` SHA-256 同为 `785a47c...c328`，并产生五段结构化输出与 `task_complete`。见 [脱敏证据](evidence/ac-003-copywriting-real-call.md)。 |
| AC-004 | PASS | 真实 Desktop 完成停用、Desktop/Host 重启保持、再启用；Host/固定 Runtime conformance 同时证明启用态对 Runtime snapshot 的影响。 |
| AC-005 | PASS | hover/focus/cancel 自动化通过；真实窗口保存 installed/modal 证据并确认卸载，只删用户副本、保留内置资源、卡片恢复加号。 |
| AC-006 | PASS | watcher + Host `directory_changed` scan 自动化通过；真实窗口外部移走已安装目录后自动恢复未安装，可重新安装。 |
| AC-007 | PASS | 双渠道资源/版本锁、旧 receipt 重放、自动升级、失败保留旧版、新增/下架投影均由 Rust/Host fixture 覆盖；Tauri 未重复实现事务。 |
| AC-008 | PASS | fresh local + demo_fast 零登录进入 `/plugins`；owner bearer 自动传递，无 bearer 实测 401，401/403/profile/capability/path 负向自动化通过，Renderer 无 bearer。 |
| AC-009 | PENDING | 539 项 UI 自动化及 light/dark/installed/modal 视觉证据通过；最小窗口与完整 loading/empty/error/retry/cancel 人工矩阵未完成。 |
| AC-010 | PENDING | Host 原子失败/回滚与 Desktop 错误/retry 自动化通过、真实 retry 已验证；真实 Desktop 恶意包 frame 及完整磁盘/只读/中断故障矩阵未运行。 |

## 5. UI 与真实结果

- UI 权威：`yijie-desktop/docs/design/docs/design/`；必须遵循 tokens、Naive UI、YjIcon/Lucide、App Shell、亮暗主题和 accessibility 规范。
- 需求输入参考：[Skill 卡片图标区域](references/skill-card-icon-reference.png)。该图仅表达每张卡片具有图标区域，不覆盖设计系统。
- 已保存 [亮色 38 卡片](evidence/desktop-skill-marketplace-light-1180x780.jpeg)、[暗色 38 卡片](evidence/desktop-skill-marketplace-dark-1180x780.jpeg)、[安装启用态](evidence/desktop-skill-installed-1180x780.jpeg) 与 [卸载确认弹窗](evidence/desktop-skill-uninstall-modal-1180x780.jpeg)；采集窗口为 1180×780，macOS 截图内容帧实际为 1162×768。
- Loading/error/retry 不困住用户：自动化 PASS，真实窗口原位 retry PASS；尚未把恶意包接入真实 Desktop frame，不能把它升格为代表性 failure PASS。
- 最终真实用户结果：PARTIAL；38 Skill 页面、本地生命周期和代表 Skill 模型真实调用均已发生，但完整 D4 仍需代表性 Desktop 恶意包失败帧及 AC-009/AC-010 剩余矩阵。

## 6. Diff 与限制

- 当前治理 diff 核对：`git diff --check` exit 0；Feature Package 内无占位词或行尾空白；4 个治理文件均为独立 FEAT-129 分支上的 tracked modifications。仓库其他既有改动不属于本需求并保持原状。
- D4 必须逐仓记录 base/head、完整 diff 审阅、生成文件、无关工作树改动和 focused check 输出。
- 已知限制：38 项源码所有权、桌面再分发、来源摘要和静态安全审核已关闭；授权同时覆盖 local-development 与 desktop-release，不再存在 `copywriting@0.1.0` 或其余 37 项的 FEAT-129 许可阻断。
- 已知限制：外部平台 API、账号、数据访问和高影响写操作仍受 Runtime/Agent Host 权限与对应服务条件控制；这不影响 38 项安装、Runtime 发现和调用，但不能把 Skill 可调用表述为外部平台一定成功。
- 已知限制：Desktop 已形成不可变 commit `ee3c508b7e9af4372c6bea758915ddb8735f422a` 并完成 Manifest v2/38、双渠道 build、目录通知、38 Skill UI 和代表 Skill 模型真实调用；当前缺口仅按证据保留为真实 Desktop 恶意包 frame、最小窗口及完整故障/全状态视觉矩阵。
- 已知限制：Host operation journal 不裁剪已用 ID，达到 4096 条后新 operation 返回 `skill_busy`；后续版本需先在契约中定义 retention/compaction，不能单方面遗忘旧 ID。
- 已知限制：macOS 验证全绿；额外 Windows 交叉编译被既有 `internal/codex/runtime.go` 的 `syscall.Stat_t` 依赖阻断，Windows Desktop 交付前仍需关闭该非 FEAT-129 回归项。

## 7. Public Demo

- `exposure=local`，`public_readiness.required=false`；密钥、鉴权、频率限制和公网 smoke 的 DP gate 不适用。
- `demo_fast` 固定身份例外只能在精确 local profile 中生效，不得扩散到 public/production。
- 免登录只表示 Desktop 自动建立本地身份并透明提供 owner-only bearer；Host 内部 bearer 与 capability 校验必须保留。

## 8. 结论

- `D0` 需求基线：PASS；schema/语义、治理测试、feature audit、lint、项目测试与脚本语法均通过。
- `D4` 本地真实可用：NOT PASS（PARTIAL evidence；AC-003 已闭合，representative failure/retry 与 AC-009/010 仍未闭合）。
- `DP` 公开 Demo 可用：N/A。
- 验证日期：2026-08-25；完整 D4 时间在剩余证据通过后填写。
