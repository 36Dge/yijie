# FEAT-152 本地提交与日常 App 交付

后续远端同步与“大模型构思”说明见 [05-remote-sync.md](05-remote-sync.md)；本文保留本地交付时点的原始记录。

本地代码、固定依赖、普通 App 打包和零付费启动/菜单/恢复检查已完成。原功能 S1–S4/D4 结论保留；本次是用户随后授权的交付固化，未重复付费模型验收。

## 固定来源

| 仓库 | 实际完整提交 | 内容 |
|---|---|---|
| Contracts | `0bdef80491db8263bad4d54cfe1d1950785a6b64` | 权限契约族0.1.0、生成物和conformance，7个文件。 |
| Host | `af8d370277569cb5a9b6a229f10386690aaebb0f` | 原生审批适配及Contracts独立pin，18个文件。 |
| Desktop | `af69d6e740351b6006a1b8aaa716d3c2e04df235` | 最终普通App入口；包含下列3个按序提交。 |
| yijie | 本报告所在提交 | 最后固定Feature Package、来源和验证记录；完整SHA见提交后本机回执。 |

Desktop提交顺序：

- `29d6ad462d39f2f7c9410a0da754bd64e16a8c3d`：34个FEAT-152/消费pin文件；混合文件部分提交。
- `d21533bd912ed7994e5f3d5cb4e795c95dcbb204`：普通身份的打包启动入口，保留用户的日常任务历史。
- `af69d6e740351b6006a1b8aaa716d3c2e04df235`：保留原stable分支结构，兼容已有严格启动隔离检查。

Host `api/runtime-permissions.lock.json` 固定实际Contracts提交；Desktop `contracts/runtime-permissions.lock.json` 固定实际Contracts/Host提交、Host lock摘要和消费文件。现有入口实际读取Git对象并核对源文件、生成物及Host整个构建输入；[最终pin检查](evidence/delivery/permission-pins-final.json)通过。旧v4、Skills和Runtime锁未替换，Codex核心干净，Runtime SHA256仍为 `4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d`。

## 日常启动

在CrossBSD目录运行：

```bash
pnpm --dir yijie-desktop tauri:demo-fast:app
```

也可双击本机 `/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/feat152-delivery/启动易界.command`。

入口复用canonical启动器，核验固定来源、构建并携带正确Native环境启动普通 `易界 AI.app`，保留 `com.yijie.ai` 身份和原任务历史。无需验收代理、临时审核策略或手工填写Skills路径。裸开发App包直接双击不等同完整local/demo_fast启动，应使用此入口。

本地包：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI.app`。
主程序SHA256：`1af7c6b6c0058d857d1cd8b4d3d067405620e6e7983d8562caeba97a9bd59898`。
这是项目标准工具生成的未签名本地开发包，应用已留给用户正常使用。没有推送、tag、签名或发布。

## 实际验证

| 检查 | 结果与证据 |
|---|---|
| 固定来源/无验收代理启动 | PASS；permission-pins-final.json、default-skills-pinned.log；自动选择并验证既有固定Skills worktree，未改Skills源码。 |
| 普通App构建 | PASS；normal-app-build.log、daily-launch-fixed.log、daily-restart.log。 |
| Native实际身份与就绪 | PASS；Info.plist为com.yijie.ai，实际运行路径匹配本次包；Host readyz为ready/runtime_state=ready。 |
| 三档权限菜单 | PASS；daily-menu-ax.txt为真实Native菜单，三项文案/说明/选中正确；无伪造菜单截图。 |
| 正常退出/重启与设置恢复 | PASS；原已选择草稿auto重启后仍auto；已有任务ask重启仍ask，历史一轮完成记录与项目保留。 |
| 历史、草稿与权限保护 | 未发送任务、未改变任务/草稿权限或内容。已有选中草稿auto按原值保留，没有为了制造新建默认ask截图重置用户状态；默认规则仍由之前S4与Native检查覆盖。 |
| 聚焦检查 | Host lint/race通过；Desktop lint、81 PASS/1安全SKIP，文档构建通过；启动器语法、固定Git对象和运行输入检查通过。 |
| 核心和其它工作 | 核心及Runtime/manifest hash未改；43个其它Desktop路径排除，两处混合文件仅提交权限片段。 |
| 付费 | 本次0次，历史验收账本仍37/45，剩余8。 |

完整结果见 [delivery-results.json](evidence/delivery/delivery-results.json)、[重启截图](evidence/delivery/daily-after-restart.jpg) 和 [输入来源](evidence/delivery/build-inputs.json)。

## 保留的真实问题与边界

第一次新增普通打包参数时，已有v4隔离检查因stable分支语法形状改变而拒绝启动，见daily-launch.log。随后只在原case之前解析普通打包参数，原stable分支及隔离检查保持，预检与实际启动/重启通过；未放宽门禁，未删除失败证据。

准备期间另有任务更新了导航/配色文档、YjNavItem及混合UI报告。它们未被本次提交或回退，最终工作区状态保留；见concurrent-worktree-updates.json。当前本机包包含已记录的既有UI/图标工作区覆盖层，构建输入没有漂移；不冒称纯净提交源码的发布制品。

用户长期禁止的强杀、攻击注入、危险fixture、权限破坏或Runtime替换测试未执行。只声明所列正常检查；S4真实模型证据与本次零付费交付检查分别记录。应用在用户确认窗口空闲后通过Cmd-Q正常退出，完成重启后已交还用户使用。

最终元仓检查：严格D4、lint和50项测试均通过。日志见[最终D4](evidence/delivery/governance-final-d4.log)与[治理测试](evidence/delivery/meta-final-tests.log)。

证据入库补充：已有忽略规则排除了.log，现已逐文件纳入本Feature提交；文本日志和AX导出只规范化行尾空白，原始字节/hash完整保留在[text-export-normalization.json](evidence/delivery/text-export-normalization.json)。第一次入库空白诊断保留，测试结果没有改写。正在运行的App原始stdout已正常移至私有日志路径，提交的是固定时刻快照。
