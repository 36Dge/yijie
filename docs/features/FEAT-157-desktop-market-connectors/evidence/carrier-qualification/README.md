# FEAT-157 Runtime 数据面环境 carrier 资格

2026-10-07；普通本地资格，**不是 D4、真实供应商资格或产品 Gateway 已实现**。

## 实际结果

`run-02/result.json` 为修正观测器后的 fresh run，两个 case 均 PASS：

- 原有固定 FEAT-156 五补丁 Runtime，binary SHA-256
  `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`；
  没有修改/复制源或重建/覆盖该二进制。
- `shell_command` 和 `exec_command` 各实际执行一次普通环境存在性检查；
  精确 thread/turn/item 的原生 `item/completed` 均 completed、exitCode=0，
  唯一输出为 `MARKER_ABSENT`。没有枚举环境或打印 marker 值。
- 同一进程的 `bearer_token_env_var` 仍可用于普通 loopback MCP；
  initialize/initialized/tools-list/tools-call 均收到正确 bearer，lookup 返回固定公开合成值。
- marker 每 case 随机生成，只在 harness 内存与目标 Runtime 子进程环境中传递；
  provider 输入、原生 stdout/stderr、所有新建临时普通文件（含 config、日志、rollout、SQLite）
  的精确值检查均无命中。检查只保存布尔值/计数，值未保存为 fixture。
- 两个 Runtime 均 stdin EOF 正常退出，exitCode=0，之后正常关闭服务和清理临时目录。

`run-01` 保留原 CHECK_FAILED 与当时 harness。实际命令和 MCP 已完成，失败来自
观测器错误地在冷 `thread/read` 的 items 中寻找 Command；固定 Runtime 的该冷投影
未含 Command。修正后使用带精确 thread/turn/item 身份的真实完成通知，没有解析模型
正文、重建 Command 或修改 Runtime。`run-02` 冷历史 Command 数量仍如实记录为 0。

本次累计 4 次普通环境检查、4 次本地 MCP lookup、12 次合成 Responses HTTP 请求、
4 个正常 EOF 退出。真实模型、外部 MCP、真实账户/凭据读写、强杀及可执行 fixture 均为 0。

## 资格适用范围与实现选择

这证明固定 Runtime 在受管 `inherit="core"`、专用 `exclude`、`set={}`，且关闭
hooks/plugins/apps/shell_snapshot/multi_agent/js_repl 的已声明执行面下，可以同时
保留 HTTP MCP bearer 使用并排除普通 shell/unified exec 的环境继承。它复用了 Host
FEAT-144/156 的既有原生隔离机制，不以 Runtime 默认环境行为替代有效配置检查。

下一步产品可优先采用每 Runtime generation 的**内部数据面能力**：Host 剔除外来同名
环境值，只注入本次受管能力，并在有效配置中核对精确 exclude 和空 set。配置只保存变量名。
该能力不是平台 token；平台凭据仍只归 Connectors。Gateway 仍须核验短期 lease、scope、
选集、实际 turn、generation 和批准，MCP bearer 本身不授予控制面权限。

相比之下，内存 `http_headers` 存在固定 Runtime 可选 config-lock 导出有效配置的源码路径，
不能无条件称不落盘：`codex-rs/core/src/session/config_lock.rs:48`、`:90`。
本资格没有使用 header 中的秘密值、config-lock 导出或恶意配置来测试该路径。

未验证：产品 Host→Broker 控制通道、FD 继承、运行中轮换/撤权、公开部署、PTY/远端 executor、
用户自定义 shell/profile、被本资格关闭的执行面及真实平台。测试的 local `never`/read-only、
MCP `auto` 仅用于普通合成资格，不能自动成为产品批准策略。没有宣称防御同 UID 主动进程
内存读取；没有执行攻击注入、权限破坏或故障强杀。

## 重现

```sh
python3 evidence/carrier-qualification/qualify_environment.py \
  --workspace /Users/jack/Downloads/Personal_Info/CrossBSD \
  --output evidence/carrier-qualification/<new-run-directory>
```

运行目录必须尚不存在。harness 校验当前候选记录中的 binary/manifest digest，环境不继承
用户凭据，网络 endpoint 全部为本次持有的 loopback server。正常退出未确认时保留临时根，
报告 STOP_PENDING 并停止，不强杀、不继续第二个 case。
