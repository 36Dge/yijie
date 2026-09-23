# FEAT-155 · 4D-1 执行记录真实时间与耗时闭环报告

2026-09-23。按用户明确授权完成[44方案](44-phase-4d-1-execution-timing-plan.md)，**4D-1已完成，报告后停止**。列表与详情现可显示运行实际开始时间、时区和原生耗时；未知仍如实未知。普通SQL15/Store5保持，隔离候选SQL26/Store6；没有迁移日常库、修改固定Runtime或进入电源/通知工作。

本批真实文本调用0。用户本轮追加2次文本授权后，累计**10/14，剩余4次**；图片、商家接口及外部MCP调用均0。声明式本机Provider实际2/2次，与真实模型额度分账。

## 实现与兼容边界

固定Runtime稳定 `thread/read` 是唯一时间来源。先在既有SQL25候选通过原手动入口生成本机验证run，确认热读与正常重开后的冷读一致，再启用SQL26 writer和UI。开始、结束使用Unix秒，耗时独立使用原生毫秒；首轮开始/结束落在同一整数秒，但耗时440毫秒，证明不能用秒差代算。来源、固定二进制摘要及原始投影见[资格证据](evidence/phase-4d-1/runtime-clock-qualification.json)。

| 归属 | 最小变更 |
|---|---|
| Contracts | 新增独立本机 `native-turn-timing` v1 GET，生成Go/TS/Rust及严格JSON Schema；known必须有有界整数，unknown/invalid不得带值；身份和字段均严格校验。独立源锁与消费副本保留固定Runtime来源，不改旧pin。 |
| Host | 在明确local候选中注册owner-only查询；复用已有受管Runtime和session→thread映射，精确查询turn。3秒deadline、8MiB投影、1024轮上限，原16MiB transport不变；所有响应no-store。不start/resume/发送，不写Host Store。 |
| Desktop存储 | reader兼容26，候选同一SQLCipher/worker增加时钟缓存、来源和有界补读状态；旧迁移1–25不改，迁移不伪造历史。普通入口15，兼容reader不取得时间写入资格。旧native格式1/2不改。 |
| 观察与恢复 | 原Coordinator拥有后台读取及正常停止；读取前后核对原生read权限、owner/tenant、完整run绑定和删除状态，使用共享单通道。每批最多50条、每次最多3次读取及1/5秒退避；终态释放不等待时间，已释放记录仍可补读。 |
| 页面与IPC | 同源私有Timing扩展；列表和详情按运行快照时区显示到秒及偏移，耗时精确保留毫秒来源。未执行、进行中、未知、已知分开；旧聊天定位、审批、业务结果与执行授权语义保持。 |

新HTTP本身additive；私有closed IPC新增枚举及SQL26持久兼容按最高风险记录为**breaking**。采用新端点、兼容reader先行及显式候选writer，不向严格旧native-thread/SSE DTO追加字段。当前为本地dirty候选，不冒称不可变发布pin、生产兼容或独立人工评审。顺序为Contracts→Host provider→Desktop reader/IPC→候选writer；回退保留26兼容reader，不降数据库版本。

原生复核发现后台补读误依赖dispatch克隆上的临时“发送准入”，前台读取虽正常，后台未启动。现改为检查候选缓存writer和读取权限；新增组合检查证明普通HostBridge无发送准入仍可读已结束运行，POST数不增加。修正后正常重开，9条旧运行均从原Runtime补齐时间；失败记录保持失败。这是有来源的补读，不是迁移回填或时间推断。

## 验证与证据

[检查索引](evidence/phase-4d-1/checks.json)、[原生UI与清理记录](evidence/phase-4d-1/native-ui.json)、[工作区与范围审查](evidence/phase-4d-1/workspace-review.json)。截图及AX在本任务CUA工具记录中，JSON仅作观察索引。

| 检查 | 结果 |
|---|---|
| 契约 | 新族生成/同步/3项conformance通过；全仓lint通过（12个既有提示）；4个登记支持/回退基线breaking比较通过。 |
| Host | lint、时间/恢复定向race检查及4项旧native协议检查通过；临时Store事务与重开证明读取不写执行状态。 |
| Desktop | 130项FEAT-155原生检查、5文件28项前端定向检查、lint/类型、Clippy全targets、IPC生成及文档构建通过；canonical候选构建通过。 |
| 兼容和失败语义 | 合成库15/25→26、重开与旧聊天通过；零值、null/非法、时间单位、独立字段、重复/错绑/晚到、删除、冲突、未知未来格式及有限重试覆盖。时间不改变额度、预约或运行结果。 |
| 固定原生链路 | 声明式本机Provider的原运行和独立重跑分别显示16:14:57、16:50:30（Asia/Shanghai），各0.44秒；老历史、重跑关联和第2轮精确定位保持。 |
| UI与重开 | 亮暗、最小1180×760、详情焦点/键盘、结果定位及正常重开通过；未执行槽仍未开始。最终11条时钟缓存有原生来源，9条由修正后的后台补读，2条本批事实保持。 |
| 无重发和清理 | 重跑后→正常重开→最终退出，除时钟缓存外，grant/run/outbox/计划及旧历史台账一致，预约0；本机请求仍2，无额外真实调用。应用、Provider正常退出，原系统浅色恢复。 |

最初回归还暴露旧IPC版本准入上界25及Availability schema上界22，均已同源修正为26，最终130项通过；初始失败日志保留，不伪装成首次全部通过。

标准Desktop `pnpm test`被既有 `contracts checkout has tracked changes` 保护阻断，未绕过或清除用户改动。Contracts全量生成/测试以及Host/Desktop/Runtime历史故障套件未执行：其中包含长期禁止的强杀、故障可执行文件、权限破坏或攻击/危险归档fixture。适用的新族、兼容与原执行路径以已审查的非破坏性检查验证，**不声称全仓测试通过**。

本机Provider没有上游转发，验证的是真实固定Runtime协议、存储与原生UI，不是新一轮真实模型质量验收。Runtime内部全历史重建成本未优化；超出投影上限、历史缺失或无法核对来源时保留未知。真实Provider、所有Must在同次fresh run通过及完整D4均未在本批完成。

## 收口

本批关闭AC-009的执行时间/耗时缺口及相关AC-010兼容子项。后续卡片操作细节、macOS防自动空闲睡眠、应用内重要更新和整体Must验收仍待后续授权批次；系统通知按既有决定延期。本批没有扩大到这些内容，也没有提交、推送、发布或修改日常库。

工作区保留前序dirty改动；Runtime源和固定产物保持，旧迁移及旧跨仓native契约未改。审查为本任务技术自审。**4D-1完成并停止，FEAT-155整体仍未D4。**
