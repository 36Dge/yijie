# Q-SEL-05 Gateway-origin 审批关联本地资格

2026-10-07（Asia/Shanghai）。本次使用与 Q-SEL-01/02 相同的现存五补丁 Runtime，未改源码或二进制。原 `run-03` 是已完成的选集/冷恢复证据，故本次独立保存于 `qsel05-run-01/`，没有覆盖既有记录。

## 结果

**标准 form elicitation 足以携带不透明关联引用，无需 Runtime patch 或 URL-mode 兜底。** 两个正常本地回合分别接受与拒绝，原生请求 `_meta` 中的 `yijieCallRef` 和 `yijieKind` 原样到达宿主。宿主不从审批文案猜工具，不依赖缺失的 Tool Item 关联字段，而是用该引用经独立控制通道读取 Gateway 已登记的实际调用。

| 观察 | 接受 | 拒绝 |
| --- | --- | --- |
| 本地 Responses 请求 | 工具请求 + 正常最终文本，共2次 | 工具请求 + 正常最终文本，共2次 |
| 实际 MCP tools/call | 1，`lookup({key: public-synthetic-record})` | 1，相同安全只读用例 |
| 原生 elicitation request | 1，form，准确 thread/turn/server | 1，form，准确 thread/turn/server |
| Gateway 控制面决定 | 先登记 accept，再回原生 accept | 先登记 decline，再回原生 decline |
| 查询实际执行 | 1次，公开合成值 | 0次 |
| Gateway 工具结果 | isError=false | isError=true，明确未获批准且未执行 |
| 原生 Tool / Turn | Tool completed；Turn completed | Tool failed；Turn completed |

Runtime 最终 stdin EOF，进程58909正常 exit0；自有HTTP server正常 shutdown；确认退出后移除临时根。工具参数和结果均为公开合成常量。真实模型/外部服务/OAuth/凭据读写/付费均0；本次2次initialize、2次tools/list、2次tools/call、2次elicitation response，4次合成Responses。与选集资格共用历史台账时需单独加算，不把本次2次安全工具调用误写成0。

## 本次证明的完整顺序

1. 本地 Responses 服务按普通协议发出合法 namespace function_call；固定 Runtime 使用自己的工具注册与执行链调用本地 Gateway，没有客户端直接替代执行器。
2. Gateway **先登记收到的实际 tools/call**，形成新的 UUID callRef，并保留原 MCP RPC ID、server/tool、原始参数摘要及原生 `_meta` 中的 threadId/turn_id。
3. Gateway 在尚未执行查询时，通过该 tools/call 的正常 Streamable HTTP SSE 通道发送 `elicitation/create`。form 的 requestedSchema 为普通空 object，`_meta` 只带 opaque callRef 和消息类型，不放授权凭证、参数或秘密。
4. 固定 app-server 发出标准 `mcpServer/elicitation/request`，保留 metadata，投影真实 threadId、turnId 与 serverName。宿主先比对这些上下文，再通过独立受控的本地 control 路径查询该 ref 的真实登记记录；此通道的临时 owner capability 只在测试宿主与 Gateway 间，不发送给 Runtime。
5. 宿主比对真实调用的当前 thread/turn、工具及参数摘要，经同一控制面登记该次决定，之后才回复 app-server 对应 JSON-RPC 请求的 accept/decline。回调的 metadata 本身从未获得执行权限。
6. Gateway 收到 RMCP 对应 elicitation response 后，再同时检查**控制面决定、原生 action、当前 thread/turn**；接受才进行一次合成查询。工具结果使用原实际 tools/call RPC ID 返回，拒绝产生普通错误结果且不查询。
7. Runtime 自己产生 Tool/Turn 终态与历史。离线断言核对了记录→elicitation→可信查询→决定→工具返回的顺序、调用参数及独立callRef。两个线程的 MCP RPC ID 都为2，仍由不同callRef隔离，不能用RPC ID全局唯一假设建立关联。

本次仅合成场景配置 `default_tools_approval_mode=auto`，目的是不让原生工具预审批与 Gateway 审批各弹一次；thread 仍为 on-request/user/read-only。**这不授权产品直接改成 auto**：产品必须先完成真实 Gateway 执行闸门、Host/current-turn能力、风险策略和审批权威绑定，然后才可在相同受管能力内讨论避免双审批。没有 Gateway 可信决定时的外部执行仍不得开启。

## 固定源码依据

路径相对 `yijie-codex`，来源 `7fd463bcef07f37b0211acd9f62b9f93ea0a4b12`；实际 binary SHA `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`，manifest SHA `8b86a1a661f50beda1e0a0c96f81ddbdf959a9a07c2e756cc4b9b0eabc053b27`。

| 位置 | 依据 |
| --- | --- |
| `codex-rs/app-server-protocol/src/protocol/v2/mcp.rs:635-663` | Form、OpenAiForm、Url均有 `_meta: Option<JsonValue>`；不需要发明协议字段 |
| 同文件`:666-700` | Core elicitation 转为 app-server typed request 时保留 meta |
| 同文件`:297-312` | thread/server/可空turn存在，但仍无通用 Tool Item 关联；本方案不依赖这个缺失字段 |
| `codex-rs/rmcp-client/src/elicitation_client_service.rs:70-101` | 标准 elicitation经过服务处理器并以自定义响应保留适用结果语义 |
| 同文件`:154-175` | 恢复 RMCP 从请求搬入context的metadata，仅删除协议progressToken |
| `codex-rs/app-server/src/bespoke_event_handling.rs:735-781` | 投影thread/active turn/server和typed request，再等待宿主响应 |
| 同文件`:1660-1671` | 宿主响应映射到原始 server_name/request_id 的 ResolveElicitation，保留 action/content/meta |
| `codex-rs/core/src/mcp_tool_call.rs:577,1083-1124` | 真实工具调用带原生thread及turn metadata；本轮观察到双方均与真实回合匹配 |

## 限制与后续实现

Q-SEL-05 的**原生转发与实际调用关联机制**已通过本地资格；这不是已完成的 Host/Broker 产品审批系统，更不是高风险服务批准。本次控制通道是本地资格服务器，不是正式HTTP契约、部署或认证方案；实际产品需source-first设计固定路径/权限/范围/有效期、可信caller、single-use决定、generation撤销、并发、取消和结果不确定。没有测试攻击输入、伪造批准、权限破坏或强杀，不声称完成攻击测试或生产安全验收。

没有运行真实模型/供应商或读取真实凭据。真实OAuth、Keyring、已授权平台scope、风险判断与外部幂等仍NOT RUN。Q-SEL-03/06的能力撤销与恢复也未由这两次正常回合覆盖。原生metadata能传递不代表它是可信授权；Gateway必须继续独立登记与最终核验。

重现命令（输出目录必须新建）：

```sh
python3 docs/features/FEAT-157-desktop-market-connectors/evidence/runtime-qualification/qualify_elicitation.py --workspace /absolute/CrossBSD --output /new/evidence/directory
python3 docs/features/FEAT-157-desktop-market-connectors/evidence/runtime-qualification/verify_elicitation.py
```

脚本复用已检查的正常EOF owner；失败或超时也不强杀，保留STOP_PENDING和临时根。所有精确输入、原生回执、控制面记录与合成结果在 `qsel05-run-01/wire.jsonl`；摘要在同目录 `result.json`。

本次执行后的唯一harness改动是显式关闭Python字节码缓存，协议逻辑未变；`qsel05-run-01/harness-at-run.py`保存与结果中harness_sha256逐字匹配的运行源。后续命令使用`PYTHONDONTWRITEBYTECODE=1`，当前主脚本也在import前设置dont_write_bytecode；本次生成的单个缓存已移除，没有纳入交付。
