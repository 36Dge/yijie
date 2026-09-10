# FEAT-144 暂停点与恢复说明

> 历史阶段记录：操作7/8已在固定0.144.6上成功，累计8/10；连接阻塞已关闭，当前业务依据与D0结论见[13](13-connection-closure-and-d0-review-2026-09-10.md)。下文失败、额度与待验证结论保留当时范围。


> 恢复后的最新结论：3/5次原生发现，第3次初始化HTTP400，未取schema；已正常退出，剩余2次不自动追加。见[08](08-discovery-results-2026-09-10.md)。下文保留该阶段历史范围。
2026-09-10，用户要求记住执行状态/细节并暂停。已停止推进，不启动第2次发现。没有活跃模型Turn，第1次测试Runtime已通过stdio EOF正常退出，exit0；不存在待强杀或待切换的应用。

## 已核实与已执行

1. Sorftime官方Codex/ClaudeCode页面直接核实无query `https://mcp.sorftime.com/` + `Authorization: Bearer <Account-SK>`；不是仅依据搜索AI摘要。query-only旧路径停用。
2. 用户授权最多5次**原生元数据发现操作**，包含正常握手、自动重试、清理，优先1次。D0不启动模型Turn/业务tools/call，不转用历史额度。
3. 第1次已运行：固定Codex app-server、原生bearer_token_env_var、无threadId的mcpServerStatus/list(toolsAndAuthOnly)。Account-SK通过macOS隐藏输入框进内存，未写脚本/argv/普通文件；进程已退出，密钥未留存。
4. 实际结果：status RPC返回，但serverInfo=null、tools={}。原生日志至少观察到2次initialize发送连接错误；没有成功握手/schema。authStatus=bearerToken仅配置识别，不能判鉴权成功，也不能判密钥无效或工具不存在。
5. 新建运行目录/输出流的精确密钥检查无命中；无thread、模型、业务、图片调用。HTTP完整尝试数不可精确证明，台账为null；不得写0或把span统计当完整wire计数。
6. 原生默认插件目录启动同步也尝试了ChatGPT/GitHub元数据请求。这不是模型或业务调用，已记录为发现隔离范围的额外行为；第2次准备使用原生plugins=false避免它。

当前累计：**1/5次原生发现，剩余4次；模型0、MCP业务0、图片0**。D0 BLOCKED，十项Must pending，产品实现/D4均NOT RUN。

## 已准备但没有执行的第2次

只读诊断发现macOS现有HTTP/HTTPS代理为127.0.0.1:7890，环境未设置代理；普通Python网页读取使用该系统代理成功。第1次Runtime隔离环境未显式承接它，连接失败。不能仅凭这些事实宣称原因已最终验证。

准备仅给本次原生子进程配置已有HTTPS_PROXY，并用原生 `features.plugins=false` 避免无关目录同步；不创建新代理、不修改系统设置、不禁用TLS、不注入CA、不放宽来源/权限门禁、不改Runtime。专项源码复核确认默认reqwest尊重HTTPS_PROXY，plugins原生开关包住相关启动同步。

未运行的本地工具：`.local/feat144-d0-tools/native_metadata_discovery.py`。它只编排固定app-server的initialize/config-read/status-list，不是MCP HTTP客户端。已做AST与分离审查，修正debug:null及输出超限时继续排空、Popen正常关闭保护。它只在实际status发现前预扣一次预算。新的秘密输入仍须macOS隐藏输入，不从聊天记录/用户数据库/keychain扫描或复制。

**恢复时先确认用户已恢复执行，再核对工作区、台账和工具内容。** 第2次优先仅1次，不重复消耗已完成的第1次，也不自动用满5次。未成功时先诊断，不循环试错。运行结束必须检查正常退出、秘密未进入新目录/流、真实服务信息和工具schema；不将空目录或仅bearerToken当成功。

## 来源与待办

Contracts/Host/Desktop/Codex来源未改，Desktop界面提交228a95a4929a53bbb6aafc76156161d642d72153保持。冻结binary/manifest摘要、native/v4来源、FEAT-137永久退役检查和权限生成检查通过。没有提交/推送/部署。

真实manifest、候选product_detail名称/schema、费用/只读幂等及安全成功/正常失败样本仍未取得。固定Runtime只消费第一次tools/list的tools，不读取远端next_cursor；发现返回不能自动称完整目录。审批与reader-first设计沿用05。

当前元仓文档/证据仍未提交，含前序FEAT-144需求调整；不得覆盖、批量暂存或混入Desktop界面提交。06中的执行前“尚未连接/0次”等内容属于第1次运行前的阶段记录；恢复以本文及当前台账为准。恢复后据实际结果同步最终需求/D0结论，再运行适用文档检查；不提前进入产品编码。

证据：[当前台账](evidence/sorftime-discovery-ledger-2026-09-10.json)、[第1次原生返回](evidence/sorftime-native-discovery-operation-1-2026-09-10.json)、[Header与预算方案](06-header-auth-and-discovery-budget-2026-09-10.md)。
