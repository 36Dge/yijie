# FEAT-175 S1／Q1 实施记录

后续状态：本文保留本次原生验证及当时阻塞事实；生成／schema阻塞已在[20](20-s1-closeout-and-preparation.md)对应批次关闭，Q2仍未真实执行。

2026-11-15。用户明确授权按修订3实施S1及Q1零费用原生协议验证；不含Q2真实模型、付费搜索、公开激活、提交或发布。既有方案的“尚未授权实施”按本次明确授权更新，不扩大到S2—S5。

整体contract-impact=breaking。S1新增独立builtin-web-retrieval/1候选与显式启用的最小本机接线；旧市场工具源、已安装专家及日常App保持。Runtime核心、补丁及已生成二进制不改；由固定产物执行正常本机协议验证。原有dirty文件及完整HEAD记录在references/s1-q1-baseline.json。

## 本轮结果

**S1的源契约／最小候选接线完成，Q1限定的原生／本机验证通过。** 正式S1后续真实路由前置Q2未执行；没有把此检查点换算为全功能、公开环境或G2A/G2V/G3正式门禁通过。

Contracts增加独立工具／应用错误／专家政策、public/internal API与委派／取消／claim控制载荷；复用旧工具输入和成功结果。Go/TS原生回调来自固定canonical；新增SDK和Host消费逐字节一致。详见[契约说明](../../../../yijie-contracts/docs/builtin-web-retrieval-v1.md)。

Host增加显式候选的原生MCP装配、末尾专家政策、namespace集合合并、单次原生确认回调与I/O生命周期通知。默认开关关闭，没有日常App激活；共享worker执行器、正式ResolveExpert接线、公开身份／云端Key和UI仍在S2／S3。详见[Host说明](../../../../yijie-agent-host/docs/feat175-builtin-web-q1.md)。

| 证据 | 实际结果 | 限定范围 |
| --- | --- | --- |
| [最终race日志](references/s1-q1-native-race-final.log) | 11个顶层用例＋10个子例全部通过，132.294秒 | 固定Runtime＋真实Host适配，模型／MCP均为普通本机合成响应 |
| Kimi与MiniMax工具链 | Kimi tool_search→Code Mode→MCP；MiniMax直接函数；各3次工具执行、0次额外确认，真实Item与回灌 | 协议能力，不是自然语言路由指标 |
| 原生等待 | 确认90001ms、模型提议120002ms；之后各完成1次工具调用 | 等待中没有MCP执行，尚未验证云端45/35秒预算 |
| 原生有效时间暂停 | canonical codex-rmcp-client既有测试1项通过，77项未运行 | 离线正规编译库测试，没有更新已审Runtime二进制 |
| 专家／辅助／恢复 | 双模型ordinary/inherit/三个disabled政策、移除、同线程跨模型切换、标题、input-only、正常冷恢复 | 完整受管资源安装／公开分发未验收 |
| 正常取消／并发 | 停止时1个在途I/O被撤销；另一轮完成；峰值并发2；原生MCP取消通知0 | 已完成的另1次调用保持完成；不宣称云端即时停止 |
| 拒绝／晚到确认 | 各1个真实原生确认，MCP执行均0 | 回答原opaque request，空turn拒绝；没有新审批状态机 |
| 市场／媒体共存 | builtin-only、market-only、both、both-with-media启动／正常EOF通过 | 现有canonical市场worker；共享worker内web transport仍待S3 |
| 原生本地工作 | 检索后文件计算及经原生批准的loopback开发服务请求通过 | 原沙箱和权限保留，无公网抓取替代 |
| 静态／源检查 | 7项契约测试、生成一致性、新API lint、TS、Go vet／gofmt／shell通过 | [机器检查](references/s1-q1-checks.json)、[源码证据](references/s1-q1-source-evidence.json) |

固定Runtime为现有tool-search-v1技术profile，binary SHA-256 `7d49018c29704fa9863da72a34d780b8ad0e67c9ffe1821ebd1c1b94d9a46d49`，manifest SHA-256 `5d1113d0333e5b677fc9cfa5ae441872bc4797f1ca6328ad4936b1e99480ee89`；完整路径与源码提交在机器证据。后续更换Runtime／模型profile／工具表必须按修订3重新判断证据适用性。

## 完整复核新增发现与处理

1. 标题线程原先仍声明hosted搜索，仅有“不要用工具”的文本要求。候选改为原生web_search=disabled及yijie_web禁用；两个模型实际工具表复验通过。
2. 新内置capability排除列表最初重复Artifact并无条件加入Media，与市场严格隔离检查不一致。改为复用原列表、按实际能力追加Media/Web，严格等值检查保持；市场与媒体四种组合通过。
3. 首轮并发测试把停止前已完成的调用也计入应取消集合。修正为停止前记录实际在途数，分别验证已完成、被取消和另一轮完成；没有把已完成重写为未执行。
4. 普通loopback命令最初受原沙箱网络限制。通过原生请求和批准该次明确命令完成验证，没有改全局权限或关闭沙箱。
5. 真实停止场景没有出现MCP CancelledNotification，证实不能依赖丢弃future自动取消远端；本轮Host生命周期通知有效。API claim／cancel竞争和共享worker私有ACK仍须S2／S3证明。

每次调试的已有日志均保留。对应日志中的某项通过不覆盖同批失败；当前最终结论只依据final race及各项最终检查。

## 保留的阻塞与未执行项

全量`pnpm check-generated:safe`被任务开始前已有的FEAT-174 `runtime-skill-marketplace`未登记family阻塞；全量`pnpm lint`在已有`jsonschema/skills/market-v2.schema.json`的`x-feature`未注册处停止。任务前dirty哈希及HEAD生成注册表证明这些状态已存在，相关文件保持。本批单独运行了TS／Go及全部新契约检查，不借此宣称全仓通过。

[兼容证据](references/s1-contract-compatibility.json)记录9个适用保留基线均无此新family，以及两份新API的4文件／130引用本地闭合。没有执行或宣称全局历史breaking PASS；正式源合并、发布pin和完整门禁仍需补齐。没有手动修改生成物或绕过校验器。

Q1不覆盖真实API事务、公开carrier、主体／租户委派、共享worker transport、正式UI、真实供应商与自然语言选路。这些分项按17号的层次留在S2／S3、Q2／Q3／Q4，N06／N09本轮只覆盖普通schema状态和历史不重发的适用部分。

真实模型、供应商检索、部署／迁移、日常App启动／更新、提交／推送均为0。禁止的强杀、可执行文件替换、权限破坏、攻击fixture及全量历史产品测试未执行；影响是未声称其故障／安全／生产覆盖。

## 契约投影首轮问题及根因复盘

新生成器的前三次运行分别遇到属性名format被误作schema关键字、以及canonical布尔schema不能直接交给OpenAPI 3.0代码生成器。第三次后停止重复生成，读取实际canonical文件定位：form分支_meta及无约束requestedSchema为JSON Schema true；同时properties字典中的同名字段必须保留，数组map不能把索引当成递归选项。

修复限定在新机械投影器：字典键与schema关键字分开；true转换为等价空schema，additionalProperties布尔值保持；数组显式传值；保留完整原canonical副本及nullable turnId。先以普通结构一致性检查验证区分证据，再恢复同源生成。没有改Runtime协议、手改生成物、放宽业务授权或制造攻击fixture。

结构问题解决后，固定Go生成器另报告不能处理独立type=null分支；将canonical的anyOf[引用,null]机械映射为OpenAPI nullable引用，完整canonical仍是有效性权威，Go类型仅作消费投影。

本文件继续记录实际结果；未执行项保持NOT RUN，不把本机合成路由计为真实模型或云端资格。
