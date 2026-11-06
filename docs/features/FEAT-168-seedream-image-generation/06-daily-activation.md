# FEAT-168 个人日常客户端启用记录

2026-11-07，Owner 授权在本机原日常客户端启用 FEAT-168，保留会话、历史图片及配置，并另行批准为此创建本地 Git 提交。03:22 从原「易界.app」重开后已看到主窗口，Host 就绪，客户端留在打开状态。日常使用范围为既有个人 Mac 的 `demo_fast/local`。隔离 D4 的供应商调用授权按原批次结算。[机器回执](references/daily-activation.json) · [此前的隔离 D4](05-local-verification.md)

## 日常入口与生图选择

桌面和用户 Applications 中的「易界.app」指向同一启动器。它通过 `development-client.py start` 启动原 `com.yijie.ai` 客户端，使用既有的日常 Host、Runtime 和 Native 数据目录。显式选择保存在本机开发目录的 `host-images.json` 中。桌面图标、终端 `pnpm client:dev` 均读取该设置。

直接在原对话中要求画图，默认由 `doubao-seedream-5-0-pro-260628` 生成，使用 `1.5K`、`watermark=false`，请求省略 `stream`。文字点名或手动选择具备生图工具的专家后，其工具优先，直至移除或切换。当前日常 Host 的钥匙串账户尚未配置方舟 Key，首次实际调用内置生图时会显示原生掩码输入框。隔离账户的 Key 留在其原有作用域。

## 来源与实际启动

先固定 fork 的补丁及构建脚本，再固定 Contracts 权威投影、Host 和 Desktop 消费者。工作目录中的 483 个 Host 构建输入和原生图像请求的 271 个 schema 均已校验。连接器 worker 继续使用原 `codex-rs` 库树。严格的市场目录检查在首次准备阶段发现 Connectors 引用落后一版，于 Native 数据库打开前停止。核对差异仅为 Runtime 兼容提交列表后，同步目录的固定提交，61 项目录的内容摘要保持一致。下表为最终实际使用的本地提交。

| 仓库 | 完整提交 |
| --- | --- |
| yijie-codex | `7171b0b262c67a72725fa54f9ed39b50edd94b54` |
| yijie-contracts | `c24d73fde83a01b5dd2a9ded8defb5bbef34e311` |
| yijie-agent-host | `435747780feaec2b8e914a97081024dc26730e0c` |
| yijie-connectors | `de1fcdf8dabd9b08983bbf907f079db41da437fe` |
| yijie-desktop | `b7ce363eb9ac8a37ba0f4fb1a178d392ba106b8c` |

两次均从 Finder 入口启动，检查真实 Native → Host → Runtime/worker 进程关系、原数据库的打开文件句柄、Host 生图准入、专家开关、两个主聊模型的可用状态和 `127.0.0.1:18081/readyz`。两次都返回 HTTP 200，且各看到一个日常主窗口。中间由启动器处理 macOS 的正常退出请求，Native 退出码为 0，专用工作流服务正常停止。两次启动器、Host、worker 和 Runtime 的摘要相同，Runtime 与隔离 D4 的出图版本相同。固定开发入口在两次启动时都重新编译了 Native 调试程序，其两个摘要在回执中分别记录。

## 数据保全

首次启动前取得既有实例锁，确认已退出且数据文件无人占用，调用项目冷备份函数生成封存副本与独立检查副本。覆盖 Native 完整目录、Host、Runtime、客户端偏好、WebKit、模型和工作流配置，共 17,458 个文件、514,120,377 字节。每个文件在原位置、封存副本、检查副本均已核对。明细和带凭据的数据仅存于本机私有目录，启用前的封存副本位于工作区 `.local/feat168-daily-20261107-030348-TPwxJO/before/sealed`。

| 对象 | 首次正常退出后的只读核对 |
| --- | --- |
| 会话与历史图片 | 加密会话库的 schema 版本为 45。原 1 个会话、1 轮、2 条消息、消息内容及原生视图逐行摘要相同。该日常库原有生成图片 0 张、图片附件 0 张。备份覆盖同一 Native 根下的其他既有目录；此前隔离 D4 的两张真实 JPEG 另行按原件摘要核对。 |
| Host 与 Runtime | Host 52 条记录均保留，仅一条会话的更新时间变化。Runtime 的会话文件及状态、记忆、目标表原有数据一致；日志表保留原有 44,892 行，增加 480 行。 |
| 配置与例行记录 | 偏好、WebKit、已有模型凭据、工作流配置、Runtime 配置文件、技能和既有专家配置逐项核对。Kimi Web 同一安装记录仅更新修订号和时间，另外增加本地探测与正常停止记录。 |
| 文件及完整性 | 所有备份范围内的原文件均有对应项。Native 完整性和外键检查、Host bbolt 结构检查、四个 Runtime SQLite 的完整性检查通过。正常退出后，Apple 虚拟化服务对工作流配置仍持有只读句柄，单独确认系统进程身份、只读访问模式以及原件与副本的逐字节一致性。 |

验收仅访问本机就绪与模型目录接口，向主聊模型、Seedream 和 LinkFox 提交任务均为 0 次。真实文生图与参考图已有隔离 D4 原件，LinkFox 的本次证据为离线路由检查。未执行数据迁移、故障或攻击注入、远端推送及公开发布。

需求包通过严格 D4 检查及仓库的需求声明审计。日常验收另行保留真实进程回执、数据比较和上一次正常退出记录。

## 暂停与恢复

正常退出后，在 `yijie-desktop` 仓执行 `python3 -B scripts/development-client.py images-pause`，再从原图标打开。该路径使用通过校验的同一 Host、既有前序 Runtime 及媒体历史读回能力。恢复内置生图使用 `images-enable` 后重开。临时目录中的设置切换用例及暂停配置的不可变源码门禁已通过。本次保留新能力开启供日常使用，未通过恢复备份覆盖现用数据。
