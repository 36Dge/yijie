# FEAT-144 恢复执行后的原生发现结果

> 历史阶段记录：操作7/8已在固定0.144.6上成功，累计8/10；连接阻塞已关闭，当前业务依据与D0结论见[13](13-connection-closure-and-d0-review-2026-09-10.md)。下文失败、额度与待验证结论保留当时范围。


> 后续验证成功：本地Codex应用原生0.153.4已取得Sorftime ready及97工具，累计5/10发现；项目固定Runtime/D4未因此通过。最新结论见[09](09-local-codex-validation-2026-09-10.md)，下文保留此前阶段范围。
2026-09-10。用户明确恢复执行，沿用最多5次原生元数据发现操作的授权（含原生握手、重试、连接清理，优先最少次数）。本轮从暂停点继续了第2、3次。**当前累计3/5，剩余2次；D0 BLOCKED。** 未进入产品编码或真实业务D4。

## 实际结果

| 操作 | 原生配置及观察 | 判定 |
|---|---|---|
| 1，暂停前 | Bearer环境引用、无query；未显式承接系统代理，initialize出现连接错误；status返回serverInfo=null/tools={} | 未发现schema；bearerToken仅配置识别，不能判鉴权成功或密钥错误 |
| 2，恢复后 | 保留现有系统HTTPS代理127.0.0.1:7890，原生plugins=false；约0.26秒返回，观察到一个原生POST span，serverInfo=null/tools={} | 未发现schema；短运行未刷入持久日志，原因未证，不写成空工具目录 |
| 3，增加安全诊断 | 同一原生配置；只增加HTTP状态/错误类别的输出投影。原生POST请求span最终记录HTTP 400，serverInfo=null/tools={} | 初始化阶段请求被返回400；未成功握手，未取得工具schema |

第3次HTTP span有多条进入/退出事件，**不是多次HTTP请求**；native `new` span计数为1。完整底层HTTP尝试数（包括内部跳转等）不能据此精确给出，台账继续为null，不写0。当前授权单位是原生发现操作，实际为3次。

原生status响应没有本次具体startup error字段。HTTP 400不能确定是Account-SK无效、MCP账户状态、请求协议或上游服务处理原因；也不能用该初始化失败代替AC-004要求的真实Tool业务failed。本次未故意使用错误密钥或构造故障。

不自动消耗剩余两次。继续发现之前需有新的修正依据：通过官方MCP控制台核对Account-SK与MCP开通状态，或取得Sorftime对该原生initialize请求HTTP 400的说明。可以提供无密钥的诊断事实；不得将真实密钥/完整认证头送入工单或日志，不能另写HTTP MCP客户端探测、回退query-key、修改Runtime或放宽门禁。

## 安全与正常退出

- 三次均使用固定Codex app-server stdio，调用initialize/config-read及mcpServerStatus/list(toolsAndAuthOnly)，没有thread/start、turn/start、tools/call。
- 原生Bearer支持依据[Sorftime Codex配置](https://www.sorftime.com/zh-CN/mcp/Codex)和[ClaudeCode配置](https://www.sorftime.com/zh-CN/mcp/ClaudeCode)；官方endpoint为无query的https://mcp.sorftime.com/。
- 密钥通过每次macOS隐藏输入框进入内存及本次Runtime子进程环境，CLI/配置仅变量名；未保存密钥，未复制用户数据、数据库或凭据。每次新建运行目录与stdout/stderr的精确密钥检查无命中。这不替代未来产品有模型/命令时的完整环境隔离验收。
- 三次Runtime都通过正常stdio EOF退出，exit0；没有强杀、权限破坏、二进制替换、攻击/故障注入。模型0、MCP业务0、图片0。
- 第1次原生默认插件启动同步产生额外目录元数据尝试，已保留记录；第2、3次用稳定原生features.plugins=false关闭该无关同步，不修改个人配置或权限策略。
- 代理来自当前macOS系统配置，仅映射到本次子进程HTTPS_PROXY；未创建新代理、修改全局设置、禁用TLS校验或注入证书。它使行为从连接重试变为快速HTTP响应，但不能单凭这一点断定第1次问题的唯一原因。

## 交付物及缺失

已交付：官方鉴权依据、可复用的原生配置/发现入口、3次真实元数据操作证据、无秘密调用台账、原生稳定elicitation薄适配设计及reader-first兼容方案。

尚未取得：真实工具集合、候选product_detail的实际名称/inputSchema/outputSchema、只读/幂等正式依据、账户MCP计费、成功样本及安全普通业务失败条件。相应字段保持null/未验证，不能用公开工具矩阵或其它API说明替代。原生工具分页游标未继续消费的限制仍保留；即使后续成功，也只能称Runtime实际返回集合，不能自动宣称完整目录。

D0是方案与边界门禁，不要求先实现产品、通过D4或批准未来模型预算。当前阻断是接入未完成及真实schema/业务验证依据缺失。P144-03审批与兼容设计已明确，保持FEAT-152、唯一NativeDisplayBuffer/SQLCipher及Codex原生历史；不引入新机制，不重启FEAT-137。

## 来源和工作区

本轮Contracts db7a607c1c091fc4f4243829d68d5b673eb7e2c3、Host f4cf01bd6f7e9f37792ef743d44f0ce10527c10b、Desktop 228a95a4929a53bbb6aafc76156161d642d72153、Codex 6c1ad767f0997845b8258a1c452fd4eb7577579f均未修改，工作树干净。元仓仍为6f12939aa85f8a9c1f55e89f1018c60501a2f494，需求文档和证据未提交。没有更新pin、推送、tag或部署。

固定Runtime build b2b20e2fc4a0c94834f34d8cc459e488a1b56277；binary SHA-256为4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d，manifest为1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b，每次启动前均核对。当前D0只写元仓文档及忽略目录中的测试编排，不改变跨仓协议或持久产品语义，实际contract-impact=none；未来实现的breaking保守判定保留。

## 证据索引

- [共用台账](evidence/sorftime-discovery-ledger-2026-09-10.json)：授权单位、每次时间、原生返回与解释分离。
- [第1次](evidence/sorftime-native-discovery-operation-1-2026-09-10.json)、[第2次](evidence/sorftime-native-discovery-operation-2-2026-09-10.json)、[第3次](evidence/sorftime-native-discovery-operation-3-2026-09-10.json)：原生status结果及安全诊断。
- [暂停记录](07-paused-state-2026-09-10.md)保持当时1/5状态的历史语义，不覆盖；恢复后以本文和台账为准。
- 当前适用文档检查结果见[02](02-verification.md)。历史D4、豁免与未执行项目不改写，不继承其它需求的PASS或额度。
