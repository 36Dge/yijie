# FEAT-162 真实 Search / Fetch 最小验收结果

2026-10-24，Asia/Shanghai。**本轮未完成验收；按用户要求已立即停止，没有重试。**

用户授权：继续复用既有Kimi模型Key，Search最多1次、Fetch最多1次，预算¥0.02，模型调用0次；先验证拒绝零请求，失败立即停止。授权原文与范围已记录在 `evidence/live-minimal-authorization.json`。

## 实际结果

| 项目 | 结果 | 供应商请求 |
|---|---|---:|
| 正常拒绝后零发送 | NOT RUN，测试入口尚未执行 | 0 |
| Search Basic | NOT RUN | 0 |
| Fetch | NOT RUN | 0 |
| 大模型推理 | 未调用 | 0 |
| /models、余额接口及其他Kimi接口 | 未调用 | 0 |

本轮供应商费用为¥0.00（因为没有请求）；未查账户账单。¥0.02预算未消耗，不将未消耗预算视为自动重试许可。

## 阻塞原因与责任

执行命令添加了 `GOPROXY=off GOSUMDB=off`，原意是避免拉取依赖，但 `GOSUMDB=off` 与当前Go自动选择1.26.5工具链的校验流程冲突。Go立即退出1，错误为 `verifying module: checksum database disabled by GOSUMDB=off`。这是本地验收启动配置错误，不是Kimi API、Key或连接器错误。

启动前，新增的opt-in测试入口已通过默认不激活的编译检查、普通JSON/SSE解析检查及go vet；它未调用供应商。正式命令失败时没有进入测试函数，运行目录仍为空，无一次性started记录、无worker诊断或子进程，因此不能声称拒绝门禁已验证，也不能声称Search/Fetch已通过或失败。

停止后只检查了日志、目录和进程并保存事实，没有再次运行测试、读取密钥值或修复后重发。为防止误用同一入口重跑，已将本轮运行目录的started.json写为明确的“operator closure / closed_without_execution”，该文件不是测试执行回执。无进程需要停止，没有强杀或权限故障操作。

## 实现与证据

只增加 `yijie-agent-host/internal/app/kimi_web_live_test.go`：默认skip、固定两个参数、真实canonical产品worker、正常PendingCall/approve_once/reject及elicitation双决策、持久一次性额度记录、结果校验及正常EOF。属于测试驱动，contract-impact=none；未修改生产代码、Codex内核、Agent循环或批准门禁。测试驱动中的线程/回合ID只是正常协议测试身份，不冒充真实Native或模型回合。

证据：`evidence/live-minimal-driver-review.json`、`live-minimal-run-location.json`、`live-minimal-run.log`、`live-minimal-result.json`。当前worker SHA256仍为`ebf7c834c95f4614365981aa7b99d04dcff37eb4d709cf4f84d0b04a8e073404`；未重建或替换产品worker。

完整D4及两接口真实能力仍NOT RUN。若用户另行要求继续，先恢复正常的Go工具链校验配置并做本地预检，再按新的明确授权建立新的执行记录；禁止复用本次记录重试或擅自改为模型对话/直接curl读取Key。
