# 日常启动技能、专家与连接器审计

> 后续状态语义纠正：用户明确要求“连接器全局已启用，但当前对话选用开关关闭”。本文中“启动全局默认关闭”是前一轮解释和测试的历史记录，已被后续修正取代。技能/专家资源修复保持；最新连接器结论见 [连接器启用与对话选用纠正](connector-enabled-selection-20261101.md)。

2026-11-01，用户要求审计并修复日常客户端的七项默认技能消失、专家服务未接通及连接器状态混乱。范围为现有个人本地开发客户端；继续使用“易界.app”和原身份、原数据。已有未提交改动的清单和补丁保存在工作区 `.local/audits/startup-capabilities-20261101/`，不提交或覆盖其他任务的工作。

## 事实与根因

- 七项 starter skill 的安装目录和完成记录仍存在，原专家版本目录也仍存在。
- 固定开发入口设置独立 `CARGO_TARGET_DIR` 和 `CARGO_BUILD_BUILD_DIR`。当前固定 tauri-build 2.6.3 从 `OUT_DIR` 的三级父目录推导资源输出，因此把两套技能资源复制到中间缓存的 `desktop/debug`。Tauri 2.11.5 / tauri-utils 2.9.3 从实际开发可执行文件所在的 `target/debug` 读取资源，该目录缺少两个资源槽。
- Native 解析资源失败后创建 unavailable SkillRuntime，没有向 Host 提供技能根和专家开关。Host/Runtime ready 仍可成功，因此健康检查不足以判断这些业务入口可用。
- 连接器 renderer 每次绑定/刷新会自动重放已保存的 desiredEnabled 意图。历史 provider 操作绑定旧 Host/native epoch 后查询返回 outcome_unknown，界面仍把保存的 pending 文案显示为正在启用。配置、授权、连接、对话选用是不同事实，不能简单清库或伪造已就绪。

## 修复与验收边界

`contract-impact = semantic`：本地开发部署补齐资源装配，并修正本地启动与连接器展示/恢复行为。资源权威为现有 Tauri 配置、普通技能锁和专家资源 pin；复用既有资源同步/校验器、Native SkillRuntime、Host 管理器和固定 Runtime 的 `skills/list`、`skills/config/write`。不重写 Runtime，不增加网络目标、权限或公共 wire 字段；不迁移业务数据库、不改历史执行结果。

本轮用户已授权调查、修复与正常重启验证。Must AC：

1. 正常入口在独立增量缓存下装配实际运行目录的资源，并逐文件校验来源与摘要。
2. 保留原七项安装和用户启停选择；聊天技能列表恢复读取实际安装状态。
3. 专家读取同一受审目录和既有资源准备记录，显示原专家；不模拟可执行服务。
4. 用户本轮已明确确认：每次启动默认关闭，手动启用后连接。连接器安装与配置保留；未决连接操作必须经过真实正常停用才可转为取消，已安装未启用项明确显示“待启用”。
5. 同一日常入口正常退出并再次启动后，三个入口保持可用；检查真实 Host/Runtime 与业务返回。

测试限于正常配置、普通资源、只读查询及应用自身的正常退出。不执行强杀、权限故障、可执行文件替换或攻击注入；不发送模型请求或外部业务工具调用。相关历史攻击/故障测试跳过，不能据此宣称全量安全或生产验收通过。

## 验证记录

已完成代码修复、静态/定向回归及两轮真实日常入口启动。用户在第一轮明确确认“三个菜单正常”；后续正常退出已获进程和生命周期证据确认，第二轮重开也已通过，当前保持易界运行。

- 资源修复复用 `sync-desktop-skill-resources.mjs` 的精确文件校验及原子装配，不更换 Native 路径解析器，不放宽 manifest/归档 pin。两套运行目录资源分别 39、77 个文件，与受审源逐文件 SHA-256 一致。
- Native 每进程使用独立 StartupState 串行发起正常 disable，重复读取或身份续期沿用同一个 operation ID。继续走原 scope/capability、Host owner pipe、Broker suspend 与终态回执。旧成功记录保持；只有真实 suspend 成功后，旧非终态连接检查才按原有逻辑记为取消。正在卸载的条目不被重新安装或改为停用。
- 删除 renderer 的自动重新启用；Kimi 默认只安装。前端展示区分待启用与正在处理/失败，配置或授权要求仍通过原操作入口处理。
- 补齐不含路径、凭据或会话内容的资源初始化、技能扫描、专家目录、连接器启动诊断，避免以后只看到 Host ready 却漏掉目录故障。

验证命令与结果：

| 检查 | 结果与边界 |
|---|---|
| Vitest：development-client、development-resources、market-connectors.store、market-connectors-ui、ChatConnectorControl | 5 文件、57 项通过。排除 `.local` 及固定 source checkout；验证独立缓存/运行资源目录、普通重开不重写、无自动启用、明确手动启用和失败提示。 |
| Python development-client tests | 2 项通过，固定身份/Home 与环境白名单。 |
| Native `startup_suspends_old_probe_preserving_installation_credentials_and_terminal_history` | 1 项通过：旧 pending probe 经实际 store 的正常 suspend 回执结束，安装身份/generation/凭据保留、历史成功结果不改、之后可显式启用。 |
| Native `suspend_preserves_credentials_authorization_and_reenable_after_normal_reopen` | 1 项通过：正常 DB 关闭/重开保留配置和授权，重新启用使用同一凭据。 |
| Native `kimi_default_installs_disabled_once_and_preserves_explicit_removal` | 1 项通过：默认停用，重复初始化幂等，不重装明确卸载项。 |
| `pnpm lint`、`pnpm build`、`pnpm docs:build` | 通过；构建保留既有 chunk-size 提示。 |
| 当前 K31 profile 的 `cargo clippy --offline --all-targets --no-default-features --features kimi-k31-pro-candidate -- -D warnings` | 通过。与正常开发共用既有构建锁/缓存，App 已正常退出。 |
| `git diff --check` / 已有 dirty 补丁逐文件对比 | 通过；8 仓初始已有 dirty 文件的补丁均保持，未自动提交、推送或切分支。 |
| 元仓 `pnpm lint && pnpm test && bash -n scripts/*.sh` | 通过，57 项测试；11 个 sibling 治理规则检查通过。 |

首次 Vitest 命令误纳入 ignored `.local` 中的历史 UI 备份，出现旧快照缺依赖/旧断言失败；当前用例还暴露了需要随新明确规则更新的旧 Kimi 自动启用断言。调整为当前规范的 source checkout 排除项，并改为显式启用/禁用检查后得到以上 57 项结果，未改写旧备份或隐藏产品失败。

第一轮实际启动（2026-11-01）：用户先在 App 正常退出，确认原进程结束；从原 `~/Applications/易界.app` 重开，使用原数据、实际代码与受管 Host/Runtime。真实 Native/Host 返回：

- 普通技能目录 38 项；已安装 7、enabled 7、runtime_visible 7、failure 0。原七项 ID 与 starter 记录一致。
- 原生专家目录 21 位，19 位资源 ready，其余 2 位保持原生实际状态；未替用户安装新专家或伪造 ready。
- 连接器安装 4，desired_enabled 0，pending 0，2 次普通 suspend 已确认（其余项本来没有活动连接）。
- Host `/readyz` 为 ready，工作流带凭据就绪检查通过，六个原容器均 healthy。

脱敏机器证据在工作区 `.local/audits/startup-capabilities-20261101/startup-1-services.json`。电脑控制工具无法定位未打包开发进程的原生窗口（裸 executable 无可选择的 App 标识）；以上机器事实来自实际 renderer 触发的 Native 目录/启动返回和直接 Host 只读检查。用户随后亲自确认三个菜单正常，构成该轮真实界面复核。

第二轮最初暂停记录（现已续办）：用户首次回复“已退出”时，进程检查仍发现原 Native PID 28516、Host/Runtime 及 launcher，开发入口记录为 `cli_running`，未观察到 cleanup complete。当时保留现场，未启动重复实例、未发送终止信号、未强杀，未将未执行的重开记为通过。

第二轮最终结果：**PASS，2026-11-01**。用户随后再次确认“已经退出”；检查确认原受管进程为 0、开发入口 `phase=stopped`，日志存在 `FEAT-164 normal app cleanup complete`。随后通过同一个 `~/Applications/易界.app` 启动，不修改代码或运行身份：

- 两套资源输出分别 39 / 77 个文件，启动报告均为 unchanged；逐文件摘要与受审源及第一轮结果一致。
- Native：技能 38 项目录、7 已安装、7 已启用；Host 再读确认 7 项 Runtime 可见、failure 0，七项安装投影与第一轮逐项一致。
- Native：专家 21 位、资源 ready 19，保留原目录与准备状态。
- Native：连接器 installed=4、desired_enabled=0、pending=0，2 次正常 suspend 确认，未自动启用或重放业务工具。
- Host/Runtime ready，工作流带凭据就绪检查通过，六个原容器 healthy。5 个受管客户端/入口/Host/媒体/Runtime 进程运行中，应用保持打开。

第二轮机器证据：`.local/audits/startup-capabilities-20261101/startup-2-services.json`；第二轮启动日志起点记录在同目录 `second-start-offset.txt`。本轮只追加正常退出/重开和只读业务状态证据，没有重复已通过的代码测试，也没有新增模型或第三方业务调用。

未执行：强杀/权限故障/二进制替换/攻击注入测试（用户禁止）；真实付费模型轮次和第三方业务工具调用（本修复不需要）；完整旧仓全量测试及公开/生产资格。影响：本结论限定于本机启动、目录读取、正常停用与普通回归，不代表各外部平台账号的当前授权或完整业务可用性。
