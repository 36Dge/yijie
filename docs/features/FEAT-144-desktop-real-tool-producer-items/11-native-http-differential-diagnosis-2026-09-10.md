# FEAT-144 原生 HTTP 差分诊断

2026-09-10。用户要求再次深入定位固定0.144.6与应用0.153.4结果不同的原因；若仍不能解决，记录问题并继续本需求中不依赖连接的后续工作。本轮未修改Runtime、来源pin、权限或产品代码。

## 新增的实际证据

对两个未修改的实际二进制，使用同一正常localhost MCP服务、公开合成Bearer、空ephemeral线程，捕获其自行发出的HTTP初始化。服务仅支持正常2025-06-18协议和空工具目录，没有业务工具、真实密钥或外部MCP调用。两者都收到原生ready，unsubscribe与EOF退出均成功；没有强杀、异常注入或权限修改。

| 初始化内容 | 固定0.144.6 | 应用0.153.4 |
|---|---|---|
| method / id | initialize / 0 | 相同 |
| protocolVersion | 2025-06-18 | 相同 |
| capabilities | elicitation.form={}、url={} | 相同 |
| clientInfo | codex-mcp-client / Codex / 0.144.6 | 同名同title，真实版本0.153.4 |
| Accept | text/event-stream, application/json | 相同 |
| Content-Type | application/json | 相同 |
| Authorization | 公开合成Bearer，单个header | 相同 |
| Content-Length | 217 | 相同 |
| User-Agent | **未发送** | **codex-mcp-client/0.153.4** |

后续notifications/initialized与tools/list的结构也一致，包括协商后的MCP-Protocol-Version和progressToken。没有观察到新版本先走server/discover，不能将此次成功归因于绕过initialize或新协议。

[线报文证据](evidence/native-local-wire-comparison-2026-09-10.json)包含两版原生启动结果、完整合成请求和SHA。比较仅限本机HTTP服务，不包括Sorftime HTTPS、代理/TLS或服务端行为，因此本地PASS本身不证明远端兼容。

## 源码核对与排除

固定源码确认：JSON只序列化一次；HeaderMap构造后仅明确覆盖Accept、Content-Type、Bearer、session；reqwest直接发送bytes，没有发现双重JSON/base64错误。白名单过滤发生初始化之后，增加timeout也不能解释已经收到400；这些都不是有依据的修正方式。auth_elicitation在两个实际请求中相同，本轮不关闭它或调整审批来试错。

只读获取了对应公开tag rust-v0.153.4，解析完整commit为3d2ee51ca2d5db578f328aa75e20aa22c0197c9a，存于忽略目录；没有checkout到项目、构建或替换二进制。rmcp依赖从1.8.0变为3.1.3，HTTP backend也有变化，但实际请求观察比单看依赖版本更直接。[源码来源与摘要](evidence/upstream-01534-readonly-comparison-2026-09-10.json)明确：公开tag源码并非本次对应用二进制做过可复现构建证明。

官方[Codex MCP配置说明](https://learn.chatgpt.com/zh-Hans/docs/extend/mcp)支持http_headers和bearer_token_env_var；又在固定源码中逐层确认User-Agent能保留到POST发送。因此有依据的最小候选是：

```toml
[mcp_servers.sorftime]
url = "https://mcp.sorftime.com/"
bearer_token_env_var = "YIJIE_FEAT144_SORFTIME_ACCOUNT_SK"
http_headers = { "User-Agent" = "codex-mcp-client/0.144.6" }
```

此片段仅展示本次差异，不替代完整受管配置；原有插件、审批、超时、秘密和来源约束保留。User-Agent声明实际0.144.6，不伪装新版、不更换协议、不用query-key、不引入桥接器。新编排经分离Agent审查，只添加此header、config/read断言和证据标签，SHA为7b8bc45dfc0ff3762b8a63ddbea23b81f82e2d8ea4b05b7579a5dad8dfff0e6a。

## 真实复测状态（已完成）

隐藏输入后，固定0.144.6仅增加真实User-Agent的原生配置，于操作7收到starting→ready，操作8返回97工具，product_detail输入与此前一致。原生unsubscribe/EOF exit0，新目录/输出秘密检查无命中。[成功收据](evidence/fixed-runtime-user-agent-success-2026-09-10.json)和[原生操作8](evidence/sorftime-native-discovery-operation-8-2026-09-10.json)为依据。

累计8/10原生元数据操作、剩余2；模型/业务/图片0。关闭固定Runtime原生连接阻塞，不重复试连。已证明这个原生配置修正有效，但未取得服务端具体拒绝规则，不声称唯一内部根因。没有改Runtime、产品权限或pin，未启动yijie应用；业务/D4仍未执行。此前“等待隐藏输入、6/10”属于复测前状态，已由本节更新。当前完整D0结论见[13](13-connection-closure-and-d0-review-2026-09-10.md)。

## 官方技能包能补充什么

ZIP只读审查及SHA见[技能包证据](evidence/sorftime-archive-audit-2026-09-10.json)。它的Python bridge直接query-key发送tools/call，sync脚本直接tools/list，没有远端initialize；不是原生HTTP初始化修复。安装默认保存密钥并调用get_time，错误isError还被转换为普通文本结果，不能原样接入当前FEAT-144。

包内product_detail输入与原生发现一致，并提供中文键值文本解析和MCP套餐起价说明；后者不是账户实际价格、计数单位或重试扣费保证。没有输出schema、幂等承诺或可核实的安全普通失败样本。工具矩阵为更早的86工具，不覆盖操作5的97工具记录。

## 不依赖连接的实际推进

已完成[12 契约与兼容reader设计](12-independent-contract-and-reader-plan-2026-09-10.md)，明确现有字段复用、真正新增字段、原生failed/error=null的处理、新版本方向、严格reader和旧binary版本拒绝候选，以及安全定向测试准备。未来database_change据此调整为expand候选，当前未执行migration。

D0不能因本机测试、方案细化或历史应用成功而改绿。业务依据不足、真实D4未执行和未授权产品实施仍分别保留；不把本次设计当成Host/Desktop产品代码交付，不提交或推送。
