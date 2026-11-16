# FEAT-175 影响评估

## 当前基线

源码及工作树状态记录在 references/source-evidence.json。设计基于当前 dirty 工作树，不将 HEAD 单独当成可发布来源；现有用户改动保持。前序审计见 [Web Search 审计](../../dev/web-search-audit-20261115.md)，新增原生事实见 [11](11-native-reuse-audit.md)。

| 仓库 | 当前可复用部分 | 拟改变部分 |
| --- | --- | --- |
| yijie-codex | hosted web_search；MCP 注册、enabled_tools；tool_search；Code Mode；原生审批／elicitation；暂停计时；取消／结果续答 | 目标零源码、补丁、schema、二进制变更；若真实协议验证发现缺口另审 |
| yijie-contracts | web-retrieval 0.3 参数／结果约束及生成链；Runtime 兼容投影 | 新应用内置表面、描述／title、服务端请求／错误、worker startup 投影、标准 MCP 审批与 UI 结果的必要消费投影 |
| yijie-agent-host | 受管进程、env、MCP 配置、正常 thread lifecycle、审批 UI 桥接 | 自动装配 yijie_web；去专家全局禁搜索；标题显式隔离；独立于市场选择；非市场标准 elicitation 薄适配；正常产品 Token 供应 |
| yijie-connectors | Kimi REST adapter、归一化、结果预算、rmcp Gateway、正常 EOF | app-owned MCP 路由；移除内置调用对 lease／模型 Key 的依赖；共享执行模块的云端模式；错误文案区分产品用户与运营凭据 |
| yijie-api | identity／tenancy／authorization／audit、PostgreSQL、authn verifier | 有限网页工具 API、服务资格／额度准入、最小调用幂等与费用事实；不增加 LLM／Agent planner |
| yijie-desktop | 普通聊天／专家入口、原生审批、MCP Item、WebRetrievalResult、历史 reader | 内置自动装配与状态；新普通 MCP 结果展示；旧 kimi-web 活动入口退役；必要的兼容投影 |
| yijie-infra | 服务部署边界、秘密注入与环境规范 | API／Connectors 部署、TLS／服务身份、运营 Key、限额配置和观测；不创建新仓库 |
| yijie-skills | 原生显式／隐式 Skills；业务资产／eval 组织 | 只更新实际引用旧安装／选用规则的资产与 eval；不批量改专家角色或复制工具目录 |

## 契约与数据分类

本轮仅文档，impact=none。拟实施整体保守归类 breaking：旧入口／选择前提退役、新客户端默认能力及审批语义变化、closed consumer 不能被假定理解新来源／错误。新公开 API 单独属于 additive；专家继承规则属于 semantic，但不降低整体分类。

数据库以扩展为原则：已有会话历史和市场记录只读兼容；服务端新增最小调用／用量记录属于业务私有状态，由 API migration 管理。不得为迁移自动运行旧 outbox、批量改 tool name、删除旧安装记录或重置授权／预算。

用户查询和目标 URL 可能含机密资料，数据级别按 restricted 规划；模型所需内容沿已有会话机制处理，常规审计只存摘要和状态。公开用户资料不能用 local 固定身份作隔离依据。

## 依赖与不扩大项

公开产品身份、运营凭据、部署目标、额度配置和可分发制品是完成条件。已有 FEAT-125 身份代码和 local lab 成功不等于生产入口已激活；本轮仅记录依赖。不得声称“其他用户安装即用”已经由本机 Keychain 解决。

不改变专家生图／视频选源、不放开平台私有数据、不改原生 Token／Goal／rollout budget、不增加独立搜索缓存／研究 Agent、不迁移所有市场连接器。不升级第三方依赖或 Runtime 作为默认实施步骤。
