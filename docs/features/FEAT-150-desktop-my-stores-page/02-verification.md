# FEAT-150 Demo 验证

## 1. 自动化与构建

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| `yijie` | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate D0 docs/features/FEAT-150-desktop-my-stores-page` | 0 | PASS：schema v3 / demo_fast / local D0 | 2026-08-26 |
| `yijie-desktop` | `pnpm exec vitest run <10 个 FEAT-150 focused files> --maxWorkers=4` | 0 | PASS：10 files / 80 tests；含领域映射、组件、页面、profile、导航、权限、路由、Sidebar | 2026-08-26 |
| `yijie-desktop` | `make lint` | 0 | PASS：contract generation check、ESLint、Vue typecheck、Rust fmt、Clippy | 2026-08-26 |
| `yijie-desktop` | `make test` | 0 | PASS：81 frontend files / 641 tests；Rust 265 passed / 0 failed / 3 environment integrations ignored | 2026-08-26 |
| `yijie-desktop` | `make build` | 0 | PASS：production renderer build；独立 StorePage chunk 生成 | 2026-08-26 |
| `yijie-desktop` | `pnpm tauri:build:demo-fast` | 0 | PASS：local debug `.app` bundle 构建成功 | 2026-08-26 |
| `yijie` | `pnpm lint && pnpm test` | 0 | PASS：repository governance lint；48 tests | 2026-08-26 |
| `yijie` | `check-feature-package.sh --gate D4`；`check-feature-package.sh --strict` | 0 | PASS：schema v3、D4 范围与语义、文档结构、模板变量/未完成标记 | 2026-08-26 |

全量测试输出中的 Happy DOM worker module 提示属于既有 FEAT-128 测试路径；Vitest 最终汇总为 81/81 files、641/641 tests PASS，不影响 FEAT-150 结果。所有执行均为正常、非破坏性验证。

## 2. 真实入口与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Fresh canonical startup/readiness | `pnpm tauri:dev`，等待 Vite/Tauri/Host 就绪后正常 Ctrl-C 退出 | macOS local / demo_fast / final source | Vite `localhost:1420` ready；Rust 编译完成并 Running `target/debug/yijie-desktop`；Agent Host 监听 `127.0.0.1:18081`；实时 renderer 模块包含最终 tabpanel 关联；退出后 1420/18081 均释放 | PASS |
| Native happy path | 从主页面点击“我的店铺”，切换广告、防差评、供应链；在供应链 selected 时按 Left | 同一 local demo 启动器的可枚举 debug app bundle，真实 Tauri WebView，1162×768 | 到达 `tauri://localhost/store`；标题“我的店铺 · 易界 AI”、侧栏 selected、三个模块和对应卡片均可观察；Left 从供应链切换到广告优化师 | PASS |
| 1180×760 visual matrix | production-component harness：light、dark、广告、防差评、供应链、角色键盘 | Browser viewport 1180×760 | 无关键重叠、主体横向滚动或不可达标签；所有截图刷新自最终代码 | PASS |
| Accessibility | 读取最终 harness axe JSON；YjTabs/StorePage 单测 | 1180×760 light + Happy DOM | `violations: []`；tablist/tab、roving tabindex、`aria-selected`、`aria-controls`、tabpanel/`aria-labelledby` 关联通过 | PASS |
| Representative failure/recovery | 缺少 `store.read` 访问 `/store`；关闭 store profile 访问 `/store`；切换合法筛选恢复内容 | Vitest memory router + local component | 无权限时进入 `/access-denied` 且 Store loader 未调用；非 exact local/demo_fast 回退 Settings；页面无远程重试，切换标签即时恢复 | PASS |

说明：canonical `pnpm tauri:dev` fresh run 绑定最终源码并独立 PASS。macOS Computer Use 无法枚举未签名裸 dev binary，因此原生点击截图使用同一启动器的可枚举 debug app bundle；这不是 browser-only 或 mock-only 替代。

## 3. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-001 | PASS | 原生 WebView 从左侧进入 `/store`；标题、URL、selected 均由 AX tree 确认；navigation/router/Sidebar 测试通过 |
| AC-002 | PASS | AX tree 与 `store-native-local-demo.png` 显示经营快报、精选场景、角色场景推荐及“本地合成/不代表真实店铺”提示 |
| AC-003 | PASS | 3 个快报标签、每组严格 5 指标由 domain/page tests 固定；原生广告切换显示广告销售额、花费、订单、ACOS、ROAS |
| AC-004 | PASS | 9 个精选标签顺序固定；“防差评”原生状态显示 4 个对应场景；全部 PDF 精选映射单测通过 |
| AC-005 | PASS | 6 个角色标签顺序固定；“供应链”原生状态显示 6 个 FBA 场景；全部角色映射单测通过 |
| AC-006 | PASS | 组件否定断言与 source search 均无多端同步、授权、查看全部、搜索、分页或场景执行控件；卡片是非交互 article |
| AC-007 | PASS | 目标 production source 对 `fetch/axios/invoke/localStorage/sessionStorage/indexedDB` 搜索为空；页面只消费本地只读常量 |
| AC-008 | PASS | `make lint/build`；新样式无裸色值/px 值，复用 design token 与 `YjIcon`；light/dark 1180×760 截图通过 |
| AC-009 | PASS | 原生 Left 键 smoke、YjTabs Arrow/Home/End 单测、明确 tab→tabpanel 关联及 axe 0 violations |
| AC-010 | PASS | 无 `store.read` 时导航不可见、深链拒绝且 Store loader 未调用；exact local/demo_fast 外 `/store` 不开放 |

## 4. UI Artifact

- `evidence/store-native-local-demo.png`：真实 local demo 首屏，导航、标题、合成提示与默认销售快报。
- `evidence/store-native-ads.png`：真实 Tauri WebView 广告快报五指标。
- `evidence/store-native-review-filter.png`：真实 Tauri WebView “防差评” selected。
- `evidence/store-native-supply-chain.png`：真实 Tauri WebView 供应链 6 张场景卡。
- `evidence/store-native-keyboard.png`：原生 Left 键从供应链切换到广告优化师后的状态。
- `evidence/store-light-1180x760.png`、`store-dark-1180x760.png`：最终代码的两主题最小窗口首屏。
- `evidence/store-filters-1180x760.png`、`store-role-keyboard-1180x760.png`：最终筛选与键盘状态。
- 九个 artifact 均为真实 PNG；1180×760 与原生 1162×768 尺寸已通过文件检查。

## 5. Diff、审查与限制

- 独立只读审查覆盖 Store page/domain/components、route/navigation/permission、visual harness、Feature Package 与 FEAT-131 边界；提出的 tab→tabpanel、透明边框 token、denied Store loader 三项均已修复并回归，最终无剩余可操作代码问题。
- `git diff --check` PASS；目标 production source 无 API/Runtime/persistence 调用和排除控件。
- `contracts/agent-host-skills-v1.lock.json`、`package.json`、`scripts/run-local-demo-fast.sh`、`src-tauri/src/chat/sidecar.rs`、`src-tauri/src/lib.rs` 五个既有 FEAT-131 脏文件在三轮启动前后 SHA-256 完全一致；本需求未 reset、checkout、覆盖或提交它们。
- 两个“全部”按参考稿首屏展示 6/12 张卡；54 个去重场景均可从具体经营目标或角色标签访问。按需求不增加搜索或分页。
- 功能仅在 local demo_fast 暴露，未发布 public/production，也不连接真实店铺。

## 6. Public Demo

- `exposure=local`，`public_readiness.required=false`；DP 不适用。
- 不创建公网入口，不调用付费 API，不处理用户输入、密钥或真实店铺数据。

## 7. 结论

- FEAT-150 实现、Must AC、自动化、构建、light/dark、无障碍与真实 local Tauri smoke：PASS。
- D4：PASS（以最终 Feature Package checker 输出为准）。
- DP：N/A。
- 验证时间：2026-08-26T16:37:22+08:00。
