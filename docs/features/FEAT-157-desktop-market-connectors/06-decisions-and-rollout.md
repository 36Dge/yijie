# FEAT-157 候选决策、依赖与实施顺序

> **2026-10-07实施更新**：用户已明确“根据需求包与设计包，开始实现feat-157需求，逐步实现”。按包内推荐方案开展本地source-first实现，D0产品方案确认；下文起草阶段的“未确认/只落需求”保留为历史。外部账户、付费调用、Git交付未授权，D4仍未完成。进展见[07实施记录](07-implementation-progress.md)。
> 2026-10-07 · 候选设计，未取得实施/新安全边界批准；不修改既有 Accepted ADR。

## 1. 方案比较与推荐

| 方案 | 复用及收益 | 代价/结论 |
|---|---|---|
| A：Desktop/Host直接给Codex配置51个第三方URL、凭据和OAuth | 原生发现/授权/调用最多、开发链最短 | Runtime直接持有平台token违背ADR-0005；原生OAuth Auto可能落明文文件；全局配置不保证本轮选集；不选 |
| B：Connectors凭据/供应商边界＋Codex原生MCP执行 | 保留现有职责；HTTP/OAuth优先复用固定Codex MCP库；复用原生工具、审批、历史 | 要补窄Broker、可信会话能力及工具风险映射；不等于已有成熟Gateway；推荐 |
| C：全部在Go/前端重写MCP、OAuth、工具执行和消息状态 | 可完全控制所有细节 | 重复协议、刷新、执行/历史机制，违背用户复用要求；不选 |

推荐B不表示“零新增后端”：51项异构服务需要共享接入管理和凭据边界，但不创建第二个Agent平台、任务状态机或一套聊天工具时间线。优先复用原生公开接口/固定库，无法安全复用的最小部分单列。

本地候选明确复用Desktop Native已有SQLCipher作为安装、非秘密配置/credentialRef、desiredEnabled、管理operation、聊天选集快照的唯一产品权威；Connectors仅Keyring真实凭据和进程内授权/连接/attempt，Host bbolt仅mapping/能力。Native持久意图→Host/Broker按revision幂等apply→匹配回执更新observed，区分pending/unknown。重开先关闭执行，复验凭据/连接后恢复effective，不恢复旧turn能力。该非秘密安装范围是ADR-0013的Proposed补充，需Owner确认和正常expand migration；不将SQLCipher当平台token vault，不引入第二份业务数据库。public/production另走API租户/RBAC/审计及正式vault，不承诺仅切配置上线。

## 2. 决策登记

以下推荐供一次评审，不把“调查获得事实”写成“Owner已经批准”。

| ID | 问题 | 推荐决定 | 状态/实施前条件 |
|---|---|---|---|
| DEC-157-01 | 范围与完成口径 | 51项全部为最终目标；被供应商阻塞可展示真实状态，不算接入完成 | 用户51目标明确；本轮只需求/继续实施尚未回复 |
| DEC-157-02 | token归属 | 保持ADR-0005；Connectors Broker持凭据，Runtime只得到本地受限能力 | 候选；存储/生命周期/能力设计评审 |
| DEC-157-03 | Codex复用层级 | 固定库复用HTTP/OAuth；原生工具发现执行/历史；不默认改Runtime内核 | 候选；精确source/lock/构建依赖及许可记录 |
| DEC-157-04 | stdio生命周期 | 单独正常EOF进程owner＋受支持transport；不采用包含强杀兜底的上游launcher | 候选；Google实际正常停止资格验证，无法退出则报告阻塞 |
| DEC-157-05 | 凭据持久化 | 本地专属Keyring命名空间，失败即拒绝持久化，不回退明文文件；UI只收引用/状态 | 候选；原生安全输入、secret到Connectors通道、账户/租户绑定确认 |
| DEC-157-06 | 本轮选用 | 与全局启用分离；空选集不调用市场工具；可多选；提交冻结、网关逐调用强制检查 | 候选；可信turn绑定/撤权/冷resume资格通过 |
| DEC-157-07 | 账户模型 | 每本地identity/应用一个当前连接；更换账户显式停用重授权，连接generation改变 | 候选；不从店铺演示推断商家/租户 |
| DEC-157-08 | 审批 | 保留现有权限模式；未知工具默认高风险拒绝；多工具不能使用FEAT144单工具推断 | 候选；高风险可信批准上下文与API/Host现有边界闭环后才激活 |
| DEC-157-09 | 淘宝闪购 | 申请易界/供应商可用官方接入，或得到供应商提供的独立MCP；不用千问私有网关 | 外部依赖；应用资格/业务API/scopes/回调/费用待供给 |
| DEC-157-10 | 旧协议兼容 | 新版本请求/读取投影与兼容reader先行；无选集保持旧行为，有选集不静默丢弃 | 候选；Contracts源先行与跨版本证据 |
| DEC-157-12 | 本地产品状态 | 复用Native SQLCipher安装/非秘密设置，Connectors仅凭据与实时连接，Host仅mapping | 候选；Proposed补充ADR-0013、expand/reader兼容和revision回执 |
| DEC-157-11 | 外部调用及生产 | 本轮零调用；未来元数据、业务、模型分别设预算；生产写入单独授权 | 本轮边界明确；无新调用批准 |

如推荐B需要补充ADR，用新 Proposed ADR明确“本地Broker装配/凭据/执行能力”，不擅自将ADR-0005改为允许Runtime持平台token。审批协议、秘密持久化和新原生权限不以设计包自行批准。

## 3. 外部就绪矩阵与解除条件

| 依赖 | 已知事实 | 缺失项与解除方式 |
|---|---|---|
| 44 OAuth | 参考清单标记oauth，不等于易界已验证 | 每服务合法endpoint、client注册、易界回调、scope、套餐/限额；先官方材料，再获授权的真实发现/授权 |
| 7条宿主渠道URL | 地址含qw/qwenwork/qoderwork | 供应商确认易界可用性；不能删改路径冒充通用endpoint |
| 淘宝 | 地址属于千问网关 | 易界应用与业务资格、独立MCP或获准业务API；无资格时本项blocked |
| FTShare | 维护者明确FTSHARE_API_KEY专有header | 合法测试key/额度及当前HTTP兼容验证；不是Bearer |
| 执中/Agentic Engine/豆蔻 | 来源仅说凭据自备；具体HTTP协议未知 | 供应商HTTP凭据绑定、scope、文档版本；不猜header/env |
| Google Calendar | 第三方包自行Google OAuth；GOOGLE_OAUTH_CREDENTIALS为JSON文件路径 | 固定包版本/来源、包自管凭据与token存储审计、Keyring/内存adapter或明确批准的加密存储方案、最小scope、正常退出；普通私有明文目录不算安全，不能读任意本机密钥文件 |
| Google Maps | 参考包已归档；需GOOGLE_MAPS_API_KEY | 维护状态评审、固定版本与兼容/账单配额；变更包须明示替代服务实现 |
| 图标 | 51个源文件匹配，但thinkingdata.png实际JPEG | 构建时派生正确格式/尺寸与hash映射；保留原件；分发前核对品牌资源许可 |

现有输入不足以完成上述外部资格，但足以形成完整交互/接口/失败语义候选。未核验服务显示“待配置/接入条件待补全”，不会显示“已启用”。此显示规则不降低AC-003/010：全部服务未达到要求时整体D4不能PASS。

## 4. 技术依赖顺序

本期demo_fast不建立治理切片；以下是连续实施的依赖顺序。

1. 评审D0候选、凭据/批准边界与供应商缺项；先做无业务调用的固定Runtime能力资格检查。尤其验证已加载thread的config覆盖限制、多工具批准关联、MCP重载时机和stdio正常退出。
2. 更新Contracts权威源：目录/管理/操作状态、scope/capabilities、可信执行binding、版本化提交及历史投影；执行generate/lint/focused conformance。现有严格消费者未更新前不发新值。
3. Native持久管理意图与Connectors provider观测、凭据安全通道、共享HTTP/OAuth配置器、本地依赖生命周期；逐服务仅声明经证据支持的差异，不复制51套框架。
4. Host将目录/选集/工具风险接入既有Coordinator/原生thread，冻结request/turn能力；Broker以受限能力校验每次调用；卸载/停用提升generation并撤销未来执行。
5. Native同源IPC、兼容reader、SQLCipher出站快照和恢复；覆盖默认模型及模型切换独立submit分支，不改老历史正文。
6. Desktop市场/详情/已安装/Composer，复用Yj/Naive/theme；文字/选集及新任务模型/工作空间意图共享store，回页重新校验；附件复用既有native草稿。
7. canonical日常入口装配必要sidecar，正常启动、实际主路径和代表性失败恢复；逐服务记账；所有Must真实通过后才填写D4。浏览器mock只做UI开发。
8. 提交、推送、tag、部署按另行明确授权执行。本轮不创建分支、不固化虚假版本、不生成发布物。

Runtime尽量不修改；若现有公开接口不能提供可信审批关联或安全退出，先给出最小扩展方案、source-first兼容评估和批准点，不用“复用”掩盖所需改动。不用替换二进制/劫持程序进行资格验证。

## 5. 数据、撤销和回滚

- 已启用意图持久，ready是可失效观测。重开先恢复目录/安装，不以缓存绿色代替当前认证和连接事实；按需连接，避免51服务同时启动。
- 全局停用先撤销新调用能力，再正常清理连接。正在外部执行的请求保留真实in-flight/unknown；不回写完成，不盲目重试写入。
- 卸载先确认，应用进入removing；关闭新的授权attempt及执行能力，正常清理secret/配置/连接元数据后移除安装。失败显示可重试清理，不伪装已删除凭据。远端revoke只有供应商支持且成功才称撤销；否则明确提示去供应商账户撤销。
- Connector安装/凭据不是聊天历史；删除会话不卸载全局连接，卸载不删除历史工具结果。历史仅存安全名称/标识与关联，不存secret。
- 旧数据没有connector refs时按旧语义读取，不回填历史选集。新record版本旧reader不能安全识别时拒绝写入并明确升级要求。
- 回滚优先关新功能、撤销Broker能力并正常停止；不降库、不删除新历史/用户secret、不复制日常数据库。只有通过新格式兼容验证的reader可接管；已发出的第三方操作不能由代码回滚。

## 6. 时间盒与停止条件

12h目标/16h停点是项目demo_fast治理时间盒，不是“51个供应商必能16小时接通”的承诺。30分钟无新事实扩大只读诊断；90分钟同阻塞选择已审定最小方案；非核心验证120分钟登记限制；核心240分钟重新评估。需要缩小51范围时必须由用户明确决定，不能暗中删AC。

不能正常退出、凭据可能暴露、身份/scope未知、外部费用未授权、需改变Accepted边界、真实接口无法取得时停止依赖步骤，继续不依赖它的文档/本地正常验证。跳过任何强杀、权限破坏、可执行文件伪装、攻击fixture测试，并记录未执行项、原因、影响。
