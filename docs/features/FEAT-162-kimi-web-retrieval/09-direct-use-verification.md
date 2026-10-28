# FEAT-162 自动复用凭据与直接可用验证

2026-10-24（Asia/Shanghai）。本轮已按07审计、08实施方案完成本地候选实现和无收费App验收。05/06只保留为旧“手动本地绑定、未启用”流程的历史。本报告不代表生产发布、供应商账号权限验证或完整D4。

## 当前结果

已有Kimi模型凭据的易界客户端，会在读取连接器/任务工具时自动准备Kimi网页检索，无需另行安装连接器、填写Key、点击配置或启用。真实App首次读取直接显示“可使用”，详情只有停用操作，没有单独配置/启用入口；正常退出、同构建重开后仍自动可使用。

任务工具开关已可用，实际验证过选中再取消选中，未提交任务。每个任务仍需选用工具，每次真实Search/Fetch仍沿原调用链请求批准。准备成功仅表示当前本地适配器可以接受受审调用，不表示供应商鉴权、权限、余额或检索结果已验证。

客户端没有统一Kimi模型凭据时会明确显示未配置，不提供第二个密钥表单。Native内存库与store测试覆盖首次默认安装、旧安装升级、重复刷新、无来源、明确停用/卸载保持及新Host重新准备；未在真实用户数据上通过删除安装来伪造全新安装验收。

## 设计和实现

- Contracts先行：management0.7.0、provider/broker0.6.0、web-retrieval0.2.0；整体仍为breaking、本地候选release=false。Native默认产品意图要求当前读/管理/凭据管理权限，复用现有操作和恢复流程，没有新Agent循环或Native命令。
- Host复用已加载模型Key快照，经单次匿名FD3交给拥有的worker。worker在线程前消费关闭，不在新增env/argv、控制JSON、日志或第二份持久存储中保存Key。正常Host重启载入新快照；停用/卸载不删除模型Key。
- Kimi Probe只本地准备canonical两个工具及当前scope/binding，已移除/models请求路径。Legacy Auth兼容仍保持本地且无执行资格，产品UI不再使用该配置步骤。原生搜索、MCP选集、逐次审批、单次HTTP准入和无自动重试保持。
- 准备失败及缺来源不会在刷新中循环重试。明确停用/卸载的用户选择不会被自动恢复覆盖。持久ready不被当作新worker资格。

## 实际检查

| 检查 | 结果 |
|---|---|
| Contracts定向JS及lint | 41项通过；12条既有未使用组件警告 |
| Connectors | 14项Kimi测试、格式/Clippy、canonical worker构建通过 |
| Host真实worker | 直接Probe及Legacy Auth各有/无普通内存来源共4种情况通过；正常EOF；另凭据管道/脱敏及vet通过 |
| Native | 3项默认意图、11项目录/权限/生命周期测试通过 |
| 前端 | 159项定向测试通过；最终详情文案修正后35项相关测试及ESLint再次通过 |
| 构建 | 标准pnpm build、Rust fmt/Clippy及最终canonical App打包通过 |
| 专家资源 | 75项内容/授权不变；canonical来源刷新、Host authority同步、真实Host manifest检查及freeze通过 |
| App UI | 自动可使用、任务开关、亮色1268×780及1180×760、焦点/Escape通过 |
| 同构建重开 | 正常Cmd-Q、--reopen来源校验与自动准备通过；回执字节不变 |
| 边界与收尾 | 7仓diff检查通过；Runtime HEAD与二进制不变、工作区干净；App及所有拥有子进程正常退出 |

主要证据：`evidence/direct-use-checks.json`、`direct-use-ui.json`、`direct-use-diagnostics.json`、`direct-use-packaged-receipt.json`、`direct-use-workspace-final.json`及对应AX/截图。三次canonical App启动均只记录Kimi `model_preparation started/succeeded`，没有HTTP阶段。测试中的普通合成请求不当作供应商验收。

## 发现与修复

第一次构建在Docker不可用处停止，没有绕过服务就绪检查。正常打开Docker后，原6个依赖容器保留退出255事实；使用既有canonical recovery流程完成四份数据保护副本、只读存储核对和正常停止，恢复ID为`7cb2c072-e21e-47d4-8489-325751756d7d`。用户暂停后继续时这些容器均保持Exited(0)，正常启动恢复6项healthy。没有强杀、删卷或权限破坏。

首次真实UI已自动准备成功，但详情仍沿用“启用后／授权连接”通用说明。已改为自动准备后直接选用和逐次操作批准，并将Kimi非就绪标题改为实际状态。最终重新构建及重开均验证新文案。旧目录revision、旧文案断言和测试payload类型不匹配等开发检查失败已修复，未覆盖旧失败日志。

## 未执行与影响

- 本任务真实/models、Search、Fetch、模型回合均为0，遵守用户限制。账号权限、余额、实际正文质量、模型驱动MCP、真实审批拒绝和工具结果历史均未验收；整体D4仍NOT RUN。
- 全新机器的签名安装/分发、生产兼容与发布未执行；首次默认安装由普通内存数据库测试覆盖，真实App覆盖现有安装升级及重开。
- 暗色实机NOT RUN：当前App无切换入口，未改变系统外观。
- 禁止的强杀、二进制伪装、权限故障、攻击注入等未执行；采用正常内存值、真实canonical worker、正常EOF和Cmd-Q。
- 历史全量breaking检查仍保留4个基线因既有远程引用EOF未通过、专家旧基线断言失败的记录；定向检查不等于全量兼容通过。
- FEAT-163共享修改完整保留，没有使用其调用额度或宣称其验收完成。没有提交、推送或发布。

## 最终来源及交接

- 来源回执 SHA256：`b749914b8bbec6341fffb87592c9eecb24ec4e64d597b51cb3df737391a217b1`。
- App SHA256：`a6046baf63260743245d566dfa0df4a12afb7fc3772f72c81fa8152823b621ef`。
- Host SHA256：`7b093b9a0ce5569f4b78157ae6c2d43193f146f5d19e0628f0627167e2d8a338`。
- worker SHA256：`ebf7c834c95f4614365981aa7b99d04dcff37eb4d709cf4f84d0b04a8e073404`。
- Runtime SHA256：`9766d7e10d25327f0595964a19ad67e1e1c1db0c22e5a65f9af66b547ab316c6`。

Runtime HEAD：`9154f27d0cdb526a5f5ba0913fe3e2448014b4a1`。最终App已正常退出，Host/worker/artifact子进程无残留；Kimi默认使用意图保留，下一次正常启动自动准备。本地workflow依赖容器保持健康，未为本任务关闭其他服务。共享源码及生成物已稳定、App构建/验收窗口可交接。
