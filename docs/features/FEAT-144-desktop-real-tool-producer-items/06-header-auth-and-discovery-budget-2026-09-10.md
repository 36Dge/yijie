# FEAT-144 官方 Header 鉴权核实与发现调用授权

> 历史阶段记录：操作7/8已在固定0.144.6上成功，累计8/10；连接阻塞已关闭，当前业务依据与D0结论见[13](13-connection-closure-and-d0-review-2026-09-10.md)。下文失败、额度与待验证结论保留当时范围。


> 恢复后的最新结论：3/5次原生发现，第3次初始化HTTP400，未取schema；已正常退出，剩余2次不自动追加。见[08](08-discovery-results-2026-09-10.md)。下文保留该阶段历史范围。
> 当前执行已由用户暂停：已完成1/5次原生发现，因初始化连接错误未取得schema；模型/业务均0，第2次尚未启动。最新恢复依据见[07暂停点](07-paused-state-2026-09-10.md)及当前台账。
2026-09-10。用户提供搜索截图及官网地址，并明确授权“真实的调用测试（5次）”。本阶段继续执行D0元数据核验，0模型Turn、0业务tools/call；不是产品实施或D4授权。本文更新05中“官方Header支持未知”及最小发现入口的结论，05中的query-key泄漏证据仍成立。

## 官方依据已经确认

截图为搜索引擎AI摘要，不能单独证明MCP鉴权。随后已从以下**官方MCP专用页面**核实：

- [Sorftime Codex配置](https://www.sorftime.com/zh-CN/mcp/Codex)：要求开通MCP并取得Account-SK；填写Streamable HTTP、URL `https://mcp.sorftime.com/`，Header为 `Authorization`，值为 `Bearer <Account-SK>`。
- [Sorftime Claude Code配置](https://www.sorftime.com/zh-CN/mcp/ClaudeCode)：给出相同无query endpoint及Authorization Bearer格式。
- [用户提供的MCP介绍页](https://www.sorftime.com/zh-CN/mcp/index?tag=)：产品说明入口，不能把其网站URL当MCP endpoint，也不能把网站其它API定价套作本账户MCP费用。

搜索索引与无凭据直接读取的官方HTML相互印证；web工具直接open超时，随后普通网页读取成功，未对MCP endpoint发请求。没有执行官网中的安装、全局配置或模型测试指令。文档只保留模板，不保存用户密钥。

现在Header支持状态为 **CONFIRMED BY OFFICIAL DOCUMENTATION**。可选择官方无query的Bearer接入；不能再把“只支持query-key”当当前阻塞，也不能因此宣称实际鉴权/连接成功。账户有效性、实时工具、schema及费用仍未验证。

## 最小原生发现方案

固定Runtime与原生来源门禁保持。采用Codex原生 `bearer_token_env_var`：命令参数只含变量名和无秘密URL，启动器在内存中把秘密注入该Runtime子进程环境，不写CLI值/配置文件/日志；不把整个用户环境或其它服务配置带入。凭据须从受管的本地秘密输入取得，不能为执行方便把聊天中的值写进工具参数、临时脚本或普通文件。

原生app-server通过无秘密CLI overrides取得以下配置语义（不是已运行命令）：

- `mcp_servers.sorftime.url = "https://mcp.sorftime.com/"`
- `mcp_servers.sorftime.bearer_token_env_var = "YIJIE_FEAT144_SORFTIME_ACCOUNT_SK"`
- 使用原生有限startup/tool超时，保留原生重试；不加载无关MCP服务，不配置模型提供商或实验API。
- 只调用app-server初始化及不带threadId的 `mcpServerStatus/list`，显式 `detail=toolsAndAuthOnly`。
- **没有thread/start、turn/start、tools/call或shell执行**。读取后正常关闭stdio并确认退出，不强杀。

这只是对既有Codex app-server的薄调用编排，不是自建MCP客户端/HTTP代理。真实产品仍按Contracts→兼容reader→Host/Desktop适配实施；不得把D0发现脚本变成新的生产执行链。

源码：cli/src/main.rs:1140传递根CLI overrides；app-server/src/request_processors/mcp_processor.rs:233无thread时使用已加载配置。无需thread/start.config，避免其先初始化MCP、随后status再次初始化的两组开销。

### 安全复审结论与适用范围

- 原生auth_status.rs:128识别bearer环境引用/Authorization，跳过OAuth metadata探测；rmcp_client.rs:787选择Bearer transport，不借用OAuth令牌。
- 无query URL使正常URL日志不再带密钥；审读的HTTP日志只投method/host/port/error类别和Authorization存在性，没有输出header值。源码：exec-server/src/client/reqwest_http_client.rs:151、rmcp-client/src/http_client_adapter.rs:432。
- 配置中只有变量名，config/read或debug config-lock不应包含环境变量的秘密值。此次不创建thread，亦不启用debug导出。
- 本次没有模型/命令执行，秘密不传给模型发起的shell。**这一点不自动证明未来产品环境隔离完成**；正式接入前仍须原生shell_environment_policy及实际执行环境定向验证。
- 原生仍Follow redirect。reqwest删除跨host/port跳转的Authorization；这不等于已经禁用所有重定向，也不改变来源/权限门禁。引用固定reqwest 0.12.28 redirect.rs:239；未知认证/错误不自动换凭据或回退query-key。

本次静态审查已形成比query-only更合适的原生路径；实际运行安全检查与发现仍未执行。不读取用户会话数据库、遍历keychain、复制用户凭据或修改现有应用配置来准备测试。

## 5次授权的准确边界

已收到最多5次真实测试授权，不再次要求授权同一事项。用户已明确选择：**最多5次原生元数据发现操作，包含正常握手、自动重试和清理；优先只做1次**。不将该授权伪装为最多5个底层HTTP请求。

一次正常有session的发现可能包含initialize POST、initialized通知POST、GET事件流、tools/list POST及DELETE清理，已可能达到5个HTTP请求；初始化/列表瞬态重试、404重建、跳转和SSE重连会增加次数。SSE默认max_times=None；原生超时不是总HTTP计数器。当前没有不改Runtime即可执行“全链路最多5 HTTP”的已证实开关，不能通过强杀、新代理或自行改重试保证。

- 若授权单位为原生发现操作：最多5次，优先只执行1次；包含必要的原生握手/重试/清理，发现操作、可观察到的HTTP尝试、模型和业务次数分账。原生正常退出不能确认则停止，不追加操作。账目不能把不可观察的HTTP数写成0。
- 若所有HTTP合计最多5：当前原生链无法保证，保持停止，不自动增加额度。
- 当前尚未连接：原生发现0，MCP业务0，模型0，图片0。公开网页阅读不属于对MCP服务的元数据/业务调用。

当前台账见 [发现授权与调用台账](evidence/sorftime-discovery-ledger-2026-09-10.json)。此前0预算记录为前一阶段历史，不再表述为“用户尚未授权任何测试”。

## 工具清单完整性限制

当前Codex只调用一次远端tools/list(params=None)，取resp.tools而不继续resp.next_cursor（codex-mcp/src/rmcp_client.rs:575）。app-server status的nextCursor仅分页服务器列表，不能用于远端工具翻页。

因此未来证据必须称“本次原生发现返回的工具集合”；不能把它自动写成Sorftime完整目录。候选product_detail若在集合中，保存其真实名称及schema；不在集合中时不能猜别名、自行翻页或绕过Codex另写客户端。完整目录性若无法证明，如实保留限制。工具schema及annotations不独自证明幂等、价格、正常失败或业务成功。

## 当前验证与D0状态

冻结codex二进制与manifest的SHA-256匹配canonical；native来源/生成物检查、v4固定来源检查、FEAT-137永久退役检查通过。本任务未改变各仓提交、源码、pin、Runtime或Desktop界面。

D0仍BLOCKED，但阻塞已推进：官方Bearer支持已确认，原生无thread最小方案已明确；计数口径已明确，真实发现等待安全输入及实际运行，manifest/费用/成功及普通失败依据尚未取得。无需先实现产品或批准D4模型额度来通过规划门禁。审批和reader-first设计沿用05。
