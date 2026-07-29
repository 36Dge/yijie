# FEAT-124 契约与兼容变更计划

## 1. Contract Impact 结论

- 分类：`additive`
- 理由：首页输入、路由和视觉均为进程内变化；但侧栏模式新增版本化 Web Storage key，使该 UI 偏好跨路由、跨应用重启和跨 Desktop 版本可观察。
- 边界：仅 `yijie-desktop` 私有本地偏好；不进入 `yijie-contracts`，不改变 HTTP、RPC、事件、Agent Host、Codex Runtime、Tauri command/capability、数据库或跨仓 DTO。
- 业务/安全语义：不改变业务权限或用户数据。偏好值只允许 `expanded`、`collapsed`，不得包含用户、租户、权限、任务正文或 secret。
- 最高风险唯一分类理由：新增持久状态但不改变旧 key/旧 reader 的解释，且旧版本会忽略新 key，因此为 `additive`，不是 `semantic` 或 `breaking`。

## 2. 权威源与责任

| 契约/边界 | 权威源类别 | 仓库与路径 | Owner | Producer | Consumers |
|---|---|---|---|---|---|
| 侧栏本地偏好 v1 | Desktop 私有持久状态 | `yijie-desktop/docs/design/docs/design/05-patterns/01-app-shell-navigation.md` 2.0.0 | 段成威 | 计划中的 `sidebar-preference.ts` writer | 计划中的 `sidebar-preference.ts` reader、`sidebar.store.ts`、`YjSidebar` |
| 公共 wire | N/A：无公共契约变化 | `yijie-contracts` 不改动 | 段成威 | N/A | N/A |

设计文档定义 key、值域、默认值、错误回退和回滚语义。实现中的常量和 adapter 是该设计的投影，必须通过 conformance test 保持一致，不能形成第二套独立语义。

## 3. 语义设计

### 写入输入

- 用户意图：用户明确点击“收起侧栏”或“展开侧栏”。
- Key：`yijie.desktop.ui.sidebar.v1`。
- Value：字符串枚举 `expanded | collapsed`。
- 默认值：存储缺失时为 `expanded`。
- 写入约束：每次只写单一枚举值；禁止写 JSON 用户对象、租户、权限、任务输入或时间戳。
- 认证、租户、权限：N/A；这是设备本地、非敏感的 UI 偏好，不影响服务端授权。
- 幂等：重复写入相同值结果相同。
- 分页、排序：N/A。

### 读取输出

- 合法值：原样解析为 `expanded` 或 `collapsed`。
- 缺失、空字符串、未知值、损坏值：统一返回 `expanded`，不得抛出到页面。
- Web Storage 读取异常：捕获并返回 `expanded`。
- Web Storage 写入异常：当前内存状态仍允许切换，但不声明已持久化；下一次启动回到可读取值或 `expanded`。
- 错误码/事件/顺序/重复/乱序：N/A；没有跨进程响应或事件流。

### 审批与审计

- 审批语义：点击切换按钮即是该低风险本地写入的用户意图，不需要二次确认。
- 审计：不进入服务端审计或业务遥测；测试只检查枚举值，不记录用户输入。
- 高风险操作：N/A。

## 4. 兼容方向

| Version combination | 存储状态/写入 | Reader 行为 | Expected | Test |
|---|---|---|---|---|
| old app + no key | 旧应用不读写该 key | 旧逻辑 | 维持旧页面行为 | 回滚 smoke |
| new app + no key | 首次安装或旧版本升级 | 返回 `expanded` | 240px 默认展开 | `PREF-001` |
| new app + `expanded` | 新 writer 写合法值 | 返回 `expanded` | 240px | `PREF-002` |
| new app + `collapsed` | 新 writer 写合法值 | 返回 `collapsed` | 72px | `PREF-003` |
| new app + unknown/corrupt | 外部或未来版本留下未知值 | 回退 `expanded` | 页面可用且不抛错 | `PREF-004` |
| new writer + old app | 新应用写 v1，随后回滚 | 旧应用忽略 key | 回滚不受阻；key 可遗留 | `PREF-005` |
| storage throws + new app | WebView storage 不可用 | 读回退、写不传播异常 | 当前 UI 可操作，重启不保证保留 | `PREF-006` |

## 5. 支持基线与兼容检查

| Baseline | Full commit | Support window | Check | Result/evidence |
|---|---|---|---|---|
| yijie-desktop develop before FEAT-124 | `09d987f09c2f2eac2575187ef57b9b65d1e89ae3` | FEAT-124 发布及回滚窗口 | 新 reader 对“无 key”兼容；旧 app 忽略新 key | PASS：`PREF-001`、`PREF-005`；baseline `git grep` 无 v1 key |
| App Shell Pattern | 2.0.0 | FEAT-124 当前设计基线 | key/value/default/rollback 人工语义检查 | Accepted；S0 conformance PASS |

公共 `yijie-contracts` breaking checker 不适用，因为没有公共 wire 或公共 consumer。私有持久状态使用本节矩阵和 `PREF-*` 测试代替结构 breaking 工具。

## 6. Generator 与下游 Pin

| Consumer | Contract version | Full commit | Digest | Generator/version | Owner |
|---|---|---|---|---|---|
| yijie-desktop 内部 reader/store/sidebar | `sidebar-preference-v1` / App Shell 2.0.0 | `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e`；设计前置 `4480f4a93eac59b3277fb0650e25f156e7fbc6a9` | Candidate files SHA-256：implementation `aa21e9f487c6942edc74a0d124e88f3fb9b86001070ccb384312f442796ee638`；test `50d97f9952f9508dd3a7983c5391351a9e2c849f876da1881160e5a0275f7965` | N/A：无 generator；使用同源常量和 conformance test | 段成威 |
| 公共 consumer | N/A：不存在 | N/A | N/A | N/A | 段成威 |

发布制品只能来自最终干净提交；当前 dirty 工作区只用于设计候选，不能作为发布来源。

## 7. Fixtures 与 Conformance

| Fixture/Test case | 唯一权威位置 | Writer test | Reader test | 状态 |
|---|---|---|---|---|
| `expanded` / `collapsed` 合法值 | App Shell Pattern 2.0.0 + `SIDEBAR_PREFERENCE_STORAGE_KEY`/`SidebarMode` | 写入仅接受两个值 | 两值原样读取 | PASS：`PREF-002`、`PREF-003` |
| 无 key、空、未知、损坏 | App Shell Pattern 2.0.0 | N/A | 全部回退 `expanded` | PASS：`PREF-001`、`PREF-004` |
| storage `getItem/setItem` 抛错 | `sidebar-preference.test.ts` 中合成 Storage stub | 异常不泄漏 | 读取回退 `expanded` | PASS：`PREF-006` |

测试数据全部为合成枚举，不含真实用户或商家数据。

## 8. 合并、部署、启用与清理顺序

| 顺序 | 动作 | Repository/Owner | 前置证据 | 回滚点 |
|---:|---|---|---|---|
| 1 | 合并 Accepted 设计规范与 FEAT-124 G2 文档 | yijie-desktop + yijie / 段成威 | 文档构建、G2 文档检查、人工批准 | 恢复旧 Pattern/Feature 文档 |
| 2 | 仅实现 `sidebar-preference.ts` reader/writer 与 `PREF-*` 测试 | yijie-desktop / 段成威 | G2 通过；不接 UI | 删除新增 domain/adapter 文件 |
| 3 | 执行局部 test、完整 lint/test/build 与兼容矩阵，登记实现完整 SHA | yijie-desktop / 段成威 | 全部检查真实通过 | 停止，不进入 UI consumer |
| 4 | G2A 由段成威批准后，实现 sidebar store/UI consumer | yijie-desktop / 段成威 | G2A 证据齐全 | 不启用写入；保持默认展开 |
| 5 | 在 App Shell 启用切换与恢复 | yijie-desktop / 段成威 | 组件、路由、视觉、Tauri smoke | 回滚 UI 提交；遗留 key 被旧版忽略 |
| 6 | 观察并清理 | yijie-desktop / 段成威 | 发布后 smoke 无存储/布局错误 | 删除单一 key 可恢复默认 |

## 9. 检查证据

### G2 文档阶段实际结果

| 检查 | Command | CWD | SHA/版本 | 结果 |
|---|---|---|---|---|
| Design docs build | `pnpm docs:build` | `yijie-desktop` | base `09d987f...` + 当前设计文档 diff | PASS，exit 0，2026-07-30 |
| Feature structure/G2 | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G2 ./docs/features/FEAT-124-desktop-post-login-home` | `yijie` | base `82f39ee...` + FEAT-124 | PASS，exit 0，2026-07-30；不替代人工批准 |
| Baseline lint | `make lint` | `yijie-desktop` | `09d987f...` + 仅设计文档 diff | PASS，exit 0，2026-07-30 |
| Baseline test | `make test` | `yijie-desktop` | `09d987f...` + 仅设计文档 diff | PASS，Vitest 1/1、Rust 0 tests，exit 0，2026-07-30 |
| Baseline build | `make build` | `yijie-desktop` | `09d987f...` + 仅设计文档 diff | PASS，Vue typecheck + Vite build，exit 0，2026-07-30 |

### G2A 实施证据

| 检查 | Command | 状态 | 通过条件 |
|---|---|---|---|
| Feature structure/G2A | `./docs/dev/codex-feature-delivery/scripts/check-feature-package.sh --gate G2A ./docs/features/FEAT-124-desktop-post-login-home` | PASS，2026-07-30；仅证明文档结构无未完成标记 | 不替代下列实现、兼容与回滚证据 |
| generate | `pnpm generate` | N/A | 当前命令只是占位，且私有偏好无 generator；不得把占位输出当证据 |
| conformance unit | `pnpm exec vitest run src/domain/sidebar-preference.test.ts` | PASS，1 file、9 tests，exit 0，2026-07-30 | `PREF-001`—`PREF-006` 全通过 |
| lint | `make lint` | PASS at `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e`，exit 0，2026-07-30 | ESLint、Vue typecheck、Cargo fmt/clippy 全通过 |
| test | `make test` | PASS at `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e`，exit 0，2026-07-30 | Vitest 2 files/10 tests；Rust 0 tests 全通过 |
| build | `make build` | PASS at `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e`，exit 0，2026-07-30 | Vue typecheck 与 Vite build 通过 |
| public breaking | N/A | N/A | 无公共 wire；由私有兼容矩阵和 conformance test 替代 |
| rollback source/unit smoke | baseline `git grep` + `PREF-001`/`PREF-005` | PASS，2026-07-30 | baseline 源码无 v1 key；新版无 key 默认展开；专用 key 不改变旧偏好 |

## 10. Owner 评审

| Consumer/Owner | 结论 | 日期 | 证据/例外 |
|---|---|---|---|
| Product/Design / 段成威 | Approved design semantics | 2026-07-30 | App Shell 2.0.0、Chat 1.1.0、Navigation 1.1.0 |
| Technical / 段成威 | G2 Approved | 2026-07-30 | 用户明确指令“批准 G2，执行 S0 侧栏偏好契约切片” |
| Local reader/writer consumer / 段成威 | Ready for G2A review | 2026-07-30 | S0 full SHA、测试、完整门禁和回滚检查均已登记；等待 Owner 明确批准 |
