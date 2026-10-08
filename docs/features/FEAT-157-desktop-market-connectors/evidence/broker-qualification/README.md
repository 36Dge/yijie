# 实际 Runtime → Rust Gateway 本地资格

2026-10-07。最终证据是 [run-06/result.json](run-06/result.json)、[同源验证](run-06/verification.json) 和该目录原始 wire；这是普通本地协议资格，不是产品 D4 或 51 项供应商验收。

使用既有固定 Codex 0.144.6 五补丁产物，binary SHA `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`，manifest SHA `8b86a1a661f50beda1e0a0c96f81ddbdf959a9a07c2e756cc4b9b0eabc053b27`，未重建或改写它。Rust 使用项目标准脚本构建独立 `market-broker-qualification`；每次启动核验 binary/manifest/编译源摘要。最终资格 SHA `68d4e5c98d3ce46fc9703133f20bb8c2dc3e697ef6792219ec182f2893fb4fea`。

run-06 后 Clippy 要求将取消判断的嵌套 if 等价改为 let-chain；标准脚本重新编译后两个产物逐字节相同、SHA不变。run-06 保留当时的源摘要，当前 manifest 记录改写后的 gateway.rs 摘要，来源衔接见 Connectors `docs/market-broker-verification.json`；没有把不同源摘要说成同一文件，也没有为纯等价且产物相同的改写再消耗验证调用。

## 最终观察

1. 私有 owner 管道 initialize → prepare(null) 得到非秘密 capabilityRef，原 prepare 重读不续期。
2. thread/start 携带完整 Gateway 配置，真实 turn/start 后 bind 实际 Thread/Turn；无额外暖机轮。
3. 实际 tools/call 产生唯一 callRef，原生 elicitation 只携带关联 metadata；通过私有 pending_call 获得冻结身份和参数摘要。
4. control approve_once 与原生 accept 都完成后，原生 Tool 为 completed，结果是对应同一 `query` 的合成公开值。重复控制决定只读原回执。
5. 终态 revoke 后重读原 prepare 得到 lease_revoked。相同 thread 的下一轮通过正常 unsubscribe/cold-resume 使用新 capabilityRef；control reject + native decline 的 Tool 为 failed，结果明确未准入。
6. 40 个控制请求/响应帧逐项通过 Contracts 当前 bundled schema；2 个真实原生 Turn、2 个 Gateway elicitation、1 个获准的合成 lookup、1 个拒绝的 lookup，4 次本地合成 Responses 请求。
7. Runtime 与 worker 均正常 EOF、exit 0 后移除临时目录；内部 bearer 原值没有出现在观测 wire 或临时 config/log/rollout/SQLite 文件中。没有运行 shell/PTY/外部 executor，不将此结果扩展到这些未覆盖面。

Gateway 使用官方 rmcp server，未在 Python 重写 MCP 服务；Python 仅托管普通合成 Responses、持有独占控制管道及观察固定 Runtime。控制 scope 和审批 ref 是清楚标注的资格数据，不代表 Native/Host 产品授权链已经装配。`default_tools_approval_mode=auto` 仅用于声明准确只读的合成工具，Gateway 的两次批准要求仍存在，不能视为真实写工具审批策略。

## 保留的尝试

| Run | 实际结果 | 本地 Responses | 正常退出 |
|---|---|---:|---|
| 01 | 新 thread 无 rollout，冷恢复失败；由此修正 prepare 新会话意图及真实双 ID 绑定 | 0 | 两进程 exit 0 |
| 02 | synthetic lookup 缺少准确只读 annotations，收到原生前置工具审批；未批准，不当作 Gateway 审批 | 1 | 两进程 exit 0 |
| 03 | 官方 rmcp 已将 `_meta` 移入 RequestContext，原实现读错位置，Gateway 拒绝实际调用 | 2 | 两进程 exit 0 |
| 04 | 首轮批准执行成功；观察器在续轮重复读取旧 Turn 的 elicitation，提前停止 | 2 | 两进程 exit 0 |
| 05 | 修正观察器的 Thread+Turn 过滤，完整首次/续轮批准拒绝通过 | 4 | 两进程 exit 0 |
| 06 | 取消边界修复后的最终产物 fresh 重跑，完整观察与同源检查 PASS | 4 | 两进程 exit 0 |

每次目录保存当时 harness 源和产物来源，失败记录不覆盖。合计 13 次本地合成 Responses；所有真实模型、平台元数据/业务、OAuth 和真实凭据操作为 0。未发进程信号、未强杀、未替换现有可执行文件、未破坏权限、未运行攻击性 fixture。

## 复现入口

从元仓执行以下命令，输出目录必须是一个尚不存在的新目录；不得覆盖上述证据：

```bash
python3 docs/features/FEAT-157-desktop-market-connectors/evidence/broker-qualification/qualify_broker_runtime.py --workspace /absolute/path/to/CrossBSD --worker-manifest /absolute/path/to/CrossBSD/yijie-connectors/bin/market-broker-qualification/current.json --output /absolute/path/to/new-run
node docs/features/FEAT-157-desktop-market-connectors/evidence/broker-qualification/verify_broker_runtime.mjs /absolute/path/to/CrossBSD /absolute/path/to/new-run
```

Host 对产品 canonical worker 的实际独占管道、正常退出和满容量退役证据另见 Host `docs/market-broker-verification.json`。这里没有把 Python 资格驱动称为 Host 产品实现，没有把合成记录称为供应商结果。
