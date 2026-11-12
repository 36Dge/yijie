# FEAT-173 工作记录

## 授权与来源

2026-11-12，用户要求审计当前生图全流程、原生工具组织，并为Seedance 2.5落实施方案；明确本次不执行。随后确认首期输入采用“文生视频＋图片生视频（复用现有附件链路）”。固定模型ID、同Seedream API Key、全部默认参数、选定专家不兜底均作为硬约束。

首先核对repos.yaml、工程规则/交付手册/长期协作原则及7仓实际HEAD、分支、远端和dirty；当前起点全部clean。读取FEAT-172迁移与复审后的实际入口、凭据、异步取消边界、Artifact交付、视频展示、专家资源、原生MCP及Code Mode源码。原始审计材料见03与references/source-audit.json。

官网控制台文档的文本访问失败后，改查同一供应商官方docs站同名页面；创建链接末尾全角分号仅按排版纠正。当前官方文档确认指定2.5模型、默认值、异步状态和DELETE语义；没有调用API调试或使用账号。详见06。

## 候选决定

- 延续ADR-0025的应用内置MCP归属和Host provider边界；不另建媒体进程、用户安装、hosted/dynamic/native-video扩展或公网媒体平台。
- 为异步供应商任务新增创建与精确取结果两工具，复用原生exec/wait。必要本地任务归属记录放既有Host bbolt，和原生Agent事实/Artifact提交分开。
- 原Keychain resolver直接注入SeedanceClient；不为名字/模型新增secret或搬迁条目。同Key不代表新模型资格。
- 任意选定专家均排除内置视频，包含查询和下载；不改专家原工具/素材/收费规则。
- 默认参数省略，不照搬官方带覆写参数的示例；MP4预览/保存复用当前组件与Native。
- Stop只承诺停止本地等待/发布；首期不调用有状态相关删除语义的DELETE，不暴露账户任务列表。

## 方案交付时状态（历史）

Feature=draft；技术方案Proposed；产品实现pending；D4 NOT RUN；真实模型和所有供应商调用0。仅元仓新增FEAT-173与Proposed ADR，所有业务/Runtime/凭据/数据库/应用状态保持。方案接受后再连续实施，付费验收、Git操作和公开发布另行授权。

## 方案交付检查

严格Feature Package结构/语义检查、元仓lint、57项治理测试和Shell语法通过；所有本地文档链接可解析，git diff --check通过。7仓HEAD、55个已审计源文件保持，业务仓无新增修改。仅本需求文档与ADR提案/索引有差异。结果见references/plan-checks.json；这不是产品实现、供应商资格或D4。

## 深度复审与修订2（2026-11-12）

用户要求重点复审原生复用、异步停止/恢复、专家隔离及过度设计，仍不执行实现。已按源码确认修订1的ACK持久化/manifest恢复会扩大既有Artifact语义；删除该设计，连同独立TTL/配额清理和额外UUID一起收敛。

补齐无句柄get、同聊天未决跨root防重、创建身份与当前观察context分离、锁/槽位等待后的专家/轮次复核；原生150s是配置而非能力上限，next_action不是自动执行命令。一次交付标记仅防重复，不证明Native提交。后handoff的Host重启状态未知如实报告，不重新投递或伪造恢复。

修订1完整文本及原检查记录保留在references/plan-revision-1.json；当前04/05/02/07与ADR、manifest已同步修订2。详细问题、证据、范围与验收增加项见08。没有产品改动、费用或Git操作授权。

## 第2版补充：对话流视频交付

用户要求补齐直接预览、播放、保存的环节，仍按方案任务处理。已只读追踪Host发布→媒体SSE→Native提交→通知/双索引→对话组件→预览协议/保存。确认现有组件与command可复用；将生产者接线、当前交付turn映射、默认schema9订阅、Native ready与ACK区别、端到端验收，以及provider/video失败文案最小修正补入09并同步主方案。没有产品代码、构建、GUI、数据库或供应商调用。

## 实施启动与本地完成

用户接受补充后的第2版，已按权威源顺序实现Contracts/Host/共享MCP/Desktop接线，固定Runtime未改。详细过程、定向检查、canonical启动及凭据/费用尚待人工步骤见[10](10-implementation-log.md)、[11](11-live-verification.md)。当前代码已落地，真实视频D4未通过；费用调用0，未提交推送。

## 真实验收完成

用户批准同一最终Host的系统授权和本任务独立额度。四种输入经日常UI生成并播放保存，首帧在真实running时正常停止后由新轮无编号恢复，无重复创建；正常重开后四条历史仍可播放，文生再保存字节相同。主聊32/32、Seedance4/4，Seedream/LinkFox0；计数器已正常关闭，普通日常入口已恢复。详见[12](12-real-acceptance.md)。专家隔离证据来自固定Runtime/Host本地集成，暗色实机未执行，不扩张为真实专家或全主题/全量验证通过。

## 实现复审与修复

用户要求再次认真审计后，发现并修复下载预算门槛、到期时状态覆盖、期限误报停止、Retry-After丢失、JSON body读取超时分类及能力/状态说明6类问题。先有普通本地失败复现，再验证修复；补齐已知任务正常重开和pending专家隔离覆盖。固定Runtime与旧协议保持，新Host为692ec26b…42d6caa；本人授权后独立无交互凭据ready，新增费用调用0。完整证据见[13](13-implementation-reaudit.md)。
