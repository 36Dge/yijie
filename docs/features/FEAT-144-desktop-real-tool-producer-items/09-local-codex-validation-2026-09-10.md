# Sorftime 配置在本地 Codex 原生运行时验证成功

> 历史阶段记录：操作7/8已在固定0.144.6上成功，累计8/10；连接阻塞已关闭，当前业务依据与D0结论见[13](13-connection-closure-and-d0-review-2026-09-10.md)。下文失败、额度与待验证结论保留当时范围。


2026-09-10。用户再次提供MCP配置，额外授权5次，并允许先用本地Codex应用验证。累计上限由5增至10，原3次记录保留；本次新增2次，**累计5/10，剩余5次**。没有启动yijie应用，没有模型Turn或业务tools/call。

## 本轮结论

**配置有效：本地Codex应用自带运行时已完成Sorftime原生MCP启动和工具发现。** 第4次收到原生starting→ready，第5次取得97个工具，服务返回Sorftime MCP / version 1.1.6。并非只根据Bearer配置标签或HTTP状态判断成功。

这证明本次使用的endpoint、Bearer凭据和服务能够完成MCP握手/元数据读取；不证明商品查询结果正确、业务计费或FEAT-144产品已完成。项目固定Runtime此前400的唯一原因尚未证明，不能据本轮成功自动归因于版本或升级项目Runtime。

## 实际入口与来源

本地应用路径为/Applications/ChatGPT.app，bundle id=com.openai.codex，版本26.903.61454，build8378。其自带 `/Applications/ChatGPT.app/Contents/Resources/codex` 报告codex-cli 0.153.4，SHA-256=c147aa90d34139599711fb568102ceefc6319ca1ac5cb6f4056ca46a1834edd9。

本轮直接运行**该应用自带的原生app-server隔离进程**，不是在桌面UI里添加永久MCP配置，也没有启动本地yijie应用。当前应用配置原本没有Sorftime，本轮没有改写全局config.toml。项目固定0.144.6及其manifest/binary、仓库pin完全保留。来源见[本地应用记录](evidence/local-codex-app-source-2026-09-10.json)。

官方OpenAI说明应用/CLI共享config.toml，并支持原生bearer_token_env_var。为保持既有秘密边界，此次只把变量名放到原生配置，把隐藏输入得到的token放到本次子进程内存环境；不将token作为CLI参数、静态header文件或工具调用文本。[OpenAI MCP配置说明](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

采用已生成核对的本地应用稳定协议：initialize、config/read，随后thread/start(ephemeral=true)、mcpServer/startupStatus/updated、mcpServerStatus/list(toolsAndAuthOnly)、thread/unsubscribe。只创建无消息的临时线程，不发turn/start。保留read-only、on-request、user reviewer；不启用实验API/历史模式，不改FEAT-152。

第4次计作临时线程触发的原生MCP初始化；ready后，第5次单独计作工具列举（可能新建原生连接），不把两组算一次。每次都在触发前登记，授权涵盖原生内部握手/重试/清理。HTTP总尝试数不可精确证明，台账为null。

## 真实工具及schema

服务身份：name=Sorftime MCP，title=Sorftime Model Context Protocol MCP Host，version=1.1.6。97个工具是本次Runtime返回集合，未进一步证明全目录完整性。完整结果与摘要：[原生返回](evidence/sorftime-native-discovery-operation-5-2026-09-10.json)、[单工具schema](evidence/sorftime-product-detail-schema-2026-09-10.json)。

首期工具名现在可以固定为 **product_detail**，不再只是候选。它的原生描述为Amazon单商品详情查询，输入如下：

| 字段 | 原生schema事实 | FEAT-144首期使用策略 |
|---|---|---|
| asin | string，唯一required字段；描述明确single-ASIN | 用户指定的一个公开ASIN，不扩展批量 |
| amz_site | string枚举，包含US；默认值原样为Unknow | 必须显式传US，不依赖默认值、不猜amzSite |

完整枚举及原生schema保留在证据中，没有为了产品范围改写服务schema。inputSchema规范化SHA-256=8fba19a74826bb3fcd9b3a98a6ee74137568194a330cadbdf77c584bc5500f77。

原生返回的该Tool没有outputSchema和annotations；接口schema支持这些字段，但本次返回缺失。不能补造readOnlyHint、幂等保证、结果字段、价格单位或正常业务错误。计划使用原生enabled_tools=[product_detail]，其余工具不开放；发现时只读目录不等于执行或批准目录中97个工具。

## 安全、退出与验证边界

- 本次只用原生客户端，无自建MCP HTTP客户端、代理、业务执行器、状态推演或历史重建。
- 使用已有系统HTTPS代理及原生plugins=false，未修改系统代理、TLS证书或全局应用配置。
- 原生thread/unsubscribe成功，进程stdio EOF正常退出，exit0；无强杀、权限破坏或故障注入。
- 本次新目录、stdout/stderr未检出输入token精确值，未保存token；模型0、业务0、图片0。该检查不替代未来有模型/命令执行时的环境隔离验证。
- 未修改、升级或替换yijie-codex/项目Runtime；没有提交、推送、tag或部署。

## 对FEAT-144 D0的影响

已解除：MCP凭据类型/官方Header支持疑问；本地Codex原生真实连通性；product_detail真实名称、参数键和inputSchema不确定性。

仍待完成：项目冻结Runtime的兼容定位；实际结果结构/安全投影依据；只读/幂等和账户计费正式依据；安全成功样本与普通业务失败条件。这些不能从工具发现自动推导，也不能把本次metadata成功当业务D4或AC-004失败样本。

D0因此保持BLOCKED；不是要求先实现产品或先运行模型才能过规划门禁。稳定elicitation审批薄适配、Contracts→兼容reader→Host/Desktop新producer顺序继续执行。后续优先用相同原生启动通知诊断项目固定Runtime，区分运行时/配置/代理等差异；未经新依据不改Runtime或恢复query-key。

本次用户要求的“配置是否有效”已得到肯定的原生元数据验证结果，暂不继续消耗剩余额度。[共用台账](evidence/sorftime-discovery-ledger-2026-09-10.json)为次数权威。
