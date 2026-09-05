# FEAT-137 永久终止收尾记录

## 最终需求裁决

Owner 段成威在 2026-09-05 本轮执行中重申：因实现耗时过长，FEAT-137 永久终止，不再实施，未来也不重启。本日期是重申及收尾执行日期，不冒充首次关闭授权日期。

需求状态为 **Owner 永久终止、未完成验收**。`feature.status` / `implementation.status` 为 `terminated`，`verification.status` 保留 `BLOCKED`。原 D0、源码检查和失败记录是历史证据；未完成的真实审批、expiry/reconnect、视觉和 D4 验收不改写为 PASS。收尾验证通过不等于功能验收通过。

## 归档与保留边界

执行前归档位于 `/Users/jack/Downloads/Personal_Info/FEAT-137-retirement-2026-09-05/`：五个完整 Git bundle、16 条本地分支的精确 refs、五条远端头、三份失效 worktree 元数据、唯一未提交补丁及校验清单。每个 bundle 已在独立空裸仓库验证、导入并检查连通性；Desktop 补丁已在其原始 HEAD 验证可应用。

补丁源为 Desktop `.local/yijie-desktop-runtime-50fef9f/src-tauri/src/chat/mod.rs`，基底 `50fef9fee117d9c2436dda03f7b0ce994f600184`。它的 `SessionNotFound` 简单跳过逻辑已被当前主工作区更完整的恢复分支覆盖，因此只存档、不回灌。

保留现有 v1-v5 协议、历史记录读取、SQLCipher 数据与脱敏安全逻辑，以及 FEAT-151 等已共享工作。v6 schema、历史锁文件、D4 producer 源码和原验证文档仅作历史材料，不是重新启用入口。没有数据库清理、广泛代码回滚或删除其他 Feature 的工作区。

## 源头先行的停用

- Contracts 冻结不可变终止权威：`4d3f967938dde1c86ca34003a0a5628717f96262:docs/retirements/FEAT-137.json`，SHA256 `67d7dfe8d539668a366ed744d92483d39597208259fe929d32d6d811c79ffbb8`。
- Host 在加载配置时拒绝旧审批与 deterministic producer 启用值；正常政策保持 `never` / `read-only`。
- Desktop 普通及 stable 入口移除 v6 激活、原生配置拒绝旧 opt-in，审批 UI 永久关闭；stable 保留 FEAT-134/136。
- 当前普通 Runtime 构建路径原本不存在，旧 FEAT-137 artifact 为三补丁而当前 Host 旧 policy 要求四补丁；不能仅删除产物而保留旧入口。
- 改用已经存在、未改写的 FEAT-136 canonical artifact `feat-136-b2b20e2fc4a0`，精确 binary / manifest / schema / 两补丁校验由 Contracts 与 Host/Desktop 一致锁定。

## 执行及验证

已完成的精确清理：

| 对象 | 结果 |
| --- | --- |
| Desktop `.local/yijie-desktop-runtime-50fef9f` | 唯一补丁归档后恢复为原基底，使用不带 force 的 Git worktree remove 移除 |
| `yijie-feat137-d4`、`yijie-desktop-feat137-d4`、`yijie-desktop-feat137-native-boundary` | 再确认目录不存在后逐个移除失效登记；未使用全局 worktree prune |
| 五仓库 16 条本地 FEAT-137 分支、5 条远端 FEAT-137 分支 | bundle 可恢复，新分支远端确认后删除；远端删除带精确旧 SHA lease；无关联 open PR |
| `feat-137-acf2da55d8a5` artifact | binary/manifest 校验与无进程占用检查后移除；manifest 与 binary 身份记录存档，不保存旧 binary 本体 |
| 旧 Runtime 的 3 个 arg0 临时软链接 | 校验精确链接目标且确认无使用后移除，未触及 CodexHome 数据库或其他状态 |
| 其余工作区、分支与共享实现 | 保留；尤其 FEAT-151 原 Desktop `ef1b6117…` 与 meta `1088d1a5…` 历史仍为新分支祖先 |

五仓库新的活动承载分支统一为 `chore/retirement-baseline-20260905`，已推送 origin。没有合并到 main/develop，也没有对默认分支做回滚或强推。源码/治理收尾提交：

| 仓库 | 收尾提交 |
| --- | --- |
| Contracts | `4d3f967938dde1c86ca34003a0a5628717f96262` |
| Agent Host | `4dce4546f8fcf2427e246e43f4de08264fa7e328` |
| Desktop | `40766179c6a74bc0b4c0c893b9536d05dc025ecd` |
| Runtime | `ac37b2ef50f2276c409adbb01df430aa7687a7e1`（文档及基线身份，不改 binary） |
| yijie | 本记录所在提交；完整 SHA 另见外部归档 `final-verification.json` |

正常、非破坏性检查：

- yijie：`pnpm test` 50/50；`pnpm lint`；Feature audit 18/18。新增两项测试覆盖终止记录必填、禁止重新打开及禁止宣称验收 PASS。旧 schema v1 的历史只读 warning 保留。
- Host：新增终止/Runtime 权威一致性 2 项测试；`scripts/test-feat136-safe.sh` 的 21 项白名单测试含 race；`make lint`；所有 Go 包编译检查通过。
- 真实 FEAT-136 Runtime：`TestPinnedRuntimeIntegration` 1/1，真实 stdio 启动、ready、正常 EOF 退出通过；无模型调用。
- Desktop：停用入口与保留 FEAT-134/136 的 11 文件、91 项检查通过；`pnpm lint`、`pnpm generate:check`、retirement checker 与 Bash 语法检查通过。清理后重复上述 91 项检查仍通过。
- Native：`cargo fmt --all -- --check`；`chat::sidecar::tests::feat137_retirement_rejects_former_exact_activation` 1/1；本次 Rust 测试目标正常编译。第一次短名加 `--exact` 匹配到 0 项，不计为测试通过，已用完整名称重跑并命中 1 项。
- Desktop canonical `pnpm tauri:build:demo-fast:stable` 通过，使用 `--debug --no-sign` 更新本项目可复现开发包，不覆盖已发布或已签名交付物；保留 FEAT-134/136、关闭审批 UI。既有大 chunk warning 非阻断。
- Runtime fork：`make lint` 通过；未构建或启用历史四补丁 producer。

未执行 FEAT-137 D4/真实审批/模型回合/人工 UI 验收；因需求永久终止，不再需要补做。没有运行含强杀、攻击注入、破坏权限、伪装运行时等禁止行为的全量旧套件。因此上述结果只证明本次停用和保留基线检查，不是完整产品回归或 FEAT-137 功能验收。

归档内 `ref-retirement-results.json` 保存逐 ref 删除记录，`final-verification.json` 保存最终 11 仓库状态、其余 16 个失效登记未变、无关 refs/HEAD 未变以及保留 Runtime hash。约 4.7 GiB 工作区构建缓存及 340 MiB 旧 Runtime 已清理，实际释放空间受文件系统共享块影响；约 20 MiB 的源码/补丁/来源归档保留。
