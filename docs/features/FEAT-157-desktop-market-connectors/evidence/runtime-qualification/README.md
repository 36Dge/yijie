# FEAT-157 原生线程选集本地资格

2026-10-07（Asia/Shanghai）。仅本地合成正常 HTTP/MCP/Responses；无真实模型、账号、外部服务或业务调用。不修改 Runtime、Host、二进制或用户库；从 stdin EOF 正常结束，超时无强杀后备。

有效制品为当前 canonical 五补丁 `chat-models-stream-args`，完整来源、binary/manifest/schema 哈希保存在每次 result.json。每次运行前只读验证 binary 和 manifest 与 Desktop 固定来源相同。

## 结论

| 资格/观察 | 实际结果 | 实施含义 |
| --- | --- | --- |
| Q-SEL-01，空 `mcp_servers={}` | **不清除**全局配置，仍发现 global_read | 禁止把空对象当空选集；必须显式关闭已知继承项，或不在基线注册真实市场 server |
| Q-SEL-01，显式 global.enabled=false | status 仍列 global，但 tools 为空；实际模型请求无 MCP namespace/资源工具 | status 的 server 行存在不是已启用；通过工具面与真实 startup/config 投影判断 |
| Q-SEL-01，两线程 A/B | A 仅 alpha_read，B 仅 beta_read；回查 A 不变 | 每线程 start config 的独立工具面可复用 |
| Q-SEL-02，已订阅 idle thread 热 resume | response 成功，但 config 被忽略，仍 alpha；stderr 明确记录 ignored | 不能把成功 response 当选集已改变 |
| Q-SEL-02，正常 unsubscribe 后 cold resume | 同 thread ID，完整新配置实际切换为 beta；先前完整 turn 历史逐值相等 | 无需新建隐藏会话，正常卸订阅与冷恢复有可用公开路径 |
| 真正模型协议工具面 | 本地普通 Responses 请求依次无 MCP、mcp__alpha、mcp__beta；3 次合成文本正常 completed | 不只依赖 status/list 的配置重建，已检查实际 turn 的工具注册投影 |
| 正常结束 | 每轮 Runtime EOF exit0，server.shutdown，退出后才清理临时根 | 没有进程异常注入、强杀或权限破坏 |

Q-SEL-01/02 的**本地原生机制部分**已证明；不等于 Host/Native 产品接通、真实供应商或 AC-005/D4 通过。计划用途、并发订阅者、多窗口与产品 outbox 尚未覆盖；Gateway 撤权、可信 turn 能力、多工具审批（Q-SEL-03～06）仍待后续实现/验证。

`mcpServerStatus/list` 会建立新的本地 MCP 发现客户端。run-03 有16次 initialize、16次 tools/list，而工具执行为0；故此接口不能被当作零外部请求成本的被动状态读取。实际服务接入需计费/限额记账、缓存/有界刷新。

## 三次真实记录

- run-01：首次观察完成空对象合并、显式停用与双线程；cold resume 使用仅含 `alpha.enabled=false` 的不完整新 stanza，正常配置校验拒绝 `invalid transport`。正常 EOF exit0。此轮不算 Q-SEL-02 PASS，原证据保留。
- run-02：改为完整合法 disabled alpha transport，新 beta transport；三个正常文本 turn 证明工具面，cold resume 和历史保留成立，EOF exit0。原生默认 OAuth store 探测隔离 HOME 的 Keychain 返回“default keychain not found”；没有读取到凭据，此轮不是 Keyring 资格。
- run-03：为避免普通无认证资格触及 OS 凭据服务，显式使用**空的隔离合成文件 store**，没有任何 token/secret；全部原生观察重验一致且无 Keychain 探测。生产方案仍强制 Keyring，本次 synthetic 配置不能复制到产品。结果为最终资格来源。

累计仅7次本地合成 Responses 文本请求、44次本地 MCP initialize/tools/list，tools/call=0；真实模型/外部 MCP/OAuth/付费=0。这些数字只统计本目录三次运行，不继承其它需求台账。

## 重现与离线断言

```sh
python3 docs/features/FEAT-157-desktop-market-connectors/evidence/runtime-qualification/qualify_runtime.py --workspace /absolute/CrossBSD --output /new/evidence/directory
python3 docs/features/FEAT-157-desktop-market-connectors/evidence/runtime-qualification/verify_observations.py
```

输出目录必须不存在。harness 只加载固定当前 artifact，env 为新建白名单，HOME/CODEX_HOME/CWD 均为新建临时根，所有 provider/MCP URL 明确指向自有127.0.0.1。工具只读 schema 是普通公开合成样本，provider 不发出工具调用。未知反向请求使流程停止；EOF 后20秒仍未退出会保留 PID/临时根并报 STOP_PENDING，不自动发信号、强杀或删目录。

`wire.jsonl` 保存精确合成输入、回执和普通诊断（含已删除的临时路径），没有用户文件内容或真实秘密。`verify_observations.py` 只读取 run-03 保存证据，不再次启动 Runtime。

## 后续Q-SEL-05

普通工具调用与Gateway-origin标准form elicitation的接受/拒绝关联已在独立 `qsel05-run-01` 完成。详见[qsel05-report.md](qsel05-report.md)；`verify_elicitation.py`只做离线断言。本次新增4个本地Responses和2个本地MCP工具调用，不能混入上文选集资格的“工具调用0”统计；外部/真实模型/凭据仍0。产品能力撤销、正式审批权威和真实供应商资格仍需后续实现。

stdio公开字节桥接的普通initialize/list/lookup及真实child正常EOF回收已另行通过，见[stdio-report.md](stdio-report.md)与`stdio-run-01.json`。真实Google包、凭据及生产bridge仍未资格化；该测试是显式Cargo feature，不扩展产品协议。
