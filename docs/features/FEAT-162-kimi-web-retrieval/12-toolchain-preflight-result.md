# FEAT-162 Go启动修复与第二轮本地预检结果

2026-10-24，Asia/Shanghai。**Go工具链启动配置已修复；本地预检未通过，按要求停止，没有重跑，未进入真实付费验收。**

## 已完成修复

新增仅测试用的 `yijie-agent-host/scripts/run-kimi-web-minimal-acceptance.sh`，先在正常校验配置下解析已经安装的官方Go工具链，再使用该版本的bin/go，确认与go.mod的1.26.5一致。仅本命令设置GOTOOLCHAIN=local、GOSUMDB=sum.golang.org、GOPROXY=off，不修改全局Go环境、不关闭校验、不下载替换任何产品二进制。

脚本分为--preflight与--execute-approved。预检清除真实Kimi凭据来源，测试驱动仅用普通内存值准备canonical产品worker并检查本地MCP元数据，在任何tools/call或批准前返回。真实执行仍要求明确授权标志和新的独占运行记录，保持Search1、Fetch1、模型0和失败停止。旧失败运行目录未复用。

Shell语法、Go编译、普通JSON/SSE解析检查、默认真实执行skip、go vet及diff检查通过。当前生产worker、Host产品代码、App、Codex Runtime和批准门禁未改。

## 本地预检的实际结果

新入口已正常进入Go测试并启动canonical产品worker，说明此前工具链校验问题已消除。worker完成本地准备（model_preparation started/succeeded），随后测试客户端在mcp_initialize阶段失败，退出1；正常EOF清理确认，没有遗留进程。

当前日志只有安全的阶段错误，未保留握手响应正文，因此不能据此断定是认证、HTTP状态、协议或SSE解析哪一个原因。停止后的静态检查发现测试SSE读取器没有特殊处理空data事件，而当前rmcp存在priming事件；这是待验证线索，不冒充已确认根因。未为验证该线索再启动进程或重跑预检。

## 次数与费用

| 项目 | 状态 | 实际供应商请求 |
|---|---|---:|
| 拒绝后零请求验收 | NOT RUN，尚未到tools/call | 0 |
| Search Basic | NOT RUN | 0 |
| Fetch | NOT RUN | 0 |
| 模型推理 | 未调用 | 0 |
| /models、余额及其他Kimi接口 | 未调用 | 0 |

本轮费用¥0.00，预算¥0.02未消耗。预检未读取真实Kimi Key，所有供应商发送计数均0。没有执行真实验收或重试，不以未用额度继续请求。此前第一轮同样0请求；两轮累计仍为0。

证据：`evidence/live-minimal-round2-result.json`、`live-minimal-round2-preflight-result.json`、`live-minimal-round2-preflight.log`、`live-minimal-round2-source.json`。

当前停止点是测试客户端本地MCP初始化，不是供应商接口失败；Kimi账号权限及真实Search/Fetch能力仍未验收。下次须获用户明确指令后处理初始化线索、完成无真实凭据预检，再按新的执行授权安排一次真实验收。未提交、推送或发布。
