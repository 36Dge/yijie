# ADR-0025：应用内置媒体 MCP 与显式能力优先

## 状态

Accepted，2026-11-12。用户明确“接受修订后的实施方案，开始实现”；本期授权限本地实现及不计费验证。关联[FEAT-172](../features/FEAT-172-image-generation-mcp-migration/00-feature-brief.md)。用户要求迁移、内置可用；最新追加选定专家不可用不再内置兜底；真实模型调用、提交/推送与公开部署未授权。

## 背景与事实

当前原生图片扩展经Host反向请求执行Seedream。Runtime已有普通MCP装配、审批、结果事件及工具后的继续执行，也已有可关闭图片扩展的配置。Host已有Seedream客户端、Keychain读取及Artifact交付。

初稿把迁移扩成新媒体API/数据库/额度平台及0019补丁重基。复审认为这些超出当前非公开本机范围；完整依据见[06复审](../features/FEAT-172-image-generation-mcp-migration/06-design-reaudit.md)。

## 修订后的决定

1. 应用自动装配yijie_media.generate_image，复用当前Runtime原生MCP/搜索/Code Mode/审批/needs_follow_up；不造新执行循环。
2. 用既有配置明确关闭原生图片，旧业务handler不绑定、dynamic producer不注册；原生Skills配置按应用Home内精确路径停用旧OpenAI imagegen系统指南，其他技能保持；固定Runtime源码/schema/补丁链不变。不可达通用代码无需在本期删除，不保留产品旧入口或切回开关。
3. 保留Host现有Seedream/附件/Artifact适配。运营方在当前非公开部署预置易界拥有的凭据，Host非交互读取；用户不安装工具、不填自己的供应商Key。API/Infra/新数据库/额度平台不进入本期。
4. 显式专家绑定排除内置生图。不可用、能力不匹配、失败、处理中、未知、拒绝与取消均保留选择并报告，不自动替代。原专家提交与审批协议保持；Runtime工具配置和Host准入共同执行，不增加preflight或终态归并。
5. 复用get_artifact_status与Native ACK，不新增get_generation、生成ID服务或Broker结果协议。短期准入状态只适配外部副作用，不成为另一个Agent/业务主状态系统。
6. 一次切换活动入口，无过渡双写、历史迁移、公开部署或Seedance实现；新请求重复提交与取消仍须正确。

## 凭据适用范围

运营方预置不是用户自备授权，也不是把共享Key写入App。Keychain读取必须禁止认证UI，缺配置/需交互时报告服务不可用。预置与实际供应商资格是后续交付输入，不能用缺Key环境冒称开箱可用。

公开分发时不能依赖把共享Key保存在用户客户端；服务端代理/身份/额度应随公开交付另行设计。本次仅本机非公开范围，不提前建设公网平台，也不宣称公网可用。

## 取舍与验证

选择配置复用而非 Runtime 补丁重基；复用当前 Host provider、原生事件和继续执行。最新用户政策删除自动兜底，因此不需要专家预检、双选集、跨轮兜底状态或业务终态解析器。

整体入口/凭据行为为 breaking，Runtime canonical 协议不变。MCP/共享 adapter startup 源先行，再消费者。必须验证选定专家时内置调用数为零、普通生图真实交付和凭据零交互。

当前本地实现、定向检查及获准真实生图验收已完成，具体见 [07实施记录](../features/FEAT-172-image-generation-mcp-migration/07-implementation-log.md)。真实模型调用已按独立额度完成；提交/推送与公开部署仍未授权。
