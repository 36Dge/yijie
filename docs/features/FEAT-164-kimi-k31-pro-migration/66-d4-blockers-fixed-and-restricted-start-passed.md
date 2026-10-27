# FEAT-164 D4 阻塞修复及受限启动验收

2026-10-27。**D4 已通过：新候选在一次 fresh run 中完成日常启动、8 会话/11 回合历史读取、附件与历史计划保护、正常退出和完整后态审计。** 本轮共两次 App 启动：首轮暴露旧历史 reader 缺口后正常退出；定位根因、完成隔离修复与资格验证后，第二轮通过。首轮失败证据完整保留。0 新增真实模型调用，不进入 D5。

Owner 先批准按第65号恢复原依赖并继续 D4，随后明确要求本轮修复全部 D4 阻塞。该授权覆盖必要的隔离 Contracts/ Desktop 修复、离线检查、新 canonical 构建和 D4 复验；不涉及 Runtime 核心或补丁变更。原工作区、旧候选、账本、两份预占及所有数据备份保留，仅本地提交。

## 根因与修复证据

| 阻塞 | 本质原因 | 已完成处理 |
| --- | --- | --- |
| D4-B01 workflow 不就绪 | Docker 未运行；磁盘 state 的 ready 是过去事实 | 正常打开原 Docker，核验原8容器/镜像/volume；4份停止态完整备份后 canonical recover → 正常停止 → canonical up。最终6个primary healthy，鉴权status/editor真实ready |
| D4-B02 旧历史不显示答案 | 原库9条format5、2条format4；候选reader仅支持1–4，预检却只检查1–5数值及根终态 | 先固定Contracts已存在的展示词汇，Desktop生成独立只读format5 reader及validator；预检实际解码。原JSON、SQL41、实时Host/SSE及format4 writer不变 |
| D4-B03 已完成记录误显示待提交 | 没有view时把submitted改为queued，且completed隐藏不可读提示 | 保留原执行事实；未来不可读格式明确提示且不重新提交。新App已复现相同历史并恢复原答案与终态 |

不是 Runtime 响应或数据库丢失：首轮之前的 Native view 本身已有原答案/terminalObserved。没有为了通过验收把失败改成完成，也没有重做旧回合。

Contracts `d5792d6aad18352ce8d1c5d510d345004cab3bd6` 先本地固定，Desktop `71e39c4e9fc38940c03b49f9b945fd4c5f6d987c` 后固定。新增输入词汇为 additive；本轮私有历史读取/预检与UI解释为 semantic，整项需求仍 breaking。其它公共契约及旧基线逐字相同；fallback c5d1383的离线保源 breaking check 通过，默认checker访问远端schema失败的原日志保留，不以网络失败声称兼容性通过。

私有 history 响应的可选 archivedViewsV5 与 Native/renderer 同App原子交付，最多50条；只有同一session/turn/runtime IDs、revision、source、status、terminalObserved和item集合才附加展示。历史文件变更、命令动作与应用信息均为转义文本，不产生命令、文件打开或新授权。未来格式仍拒绝；format5绝不回写为4。未引入FEAT-163实时执行/进度实现。

## 资格与实际 D4

- 88项前端回归、6项来源入口单元、4项D2工具测试、Contracts正常值测试、生产Native repository/worker/历史重开及只读测试通过；真实inspection的Rust预检明确执行1项，9条format5可解码，生成schema检查不可读数0。
- lint/typecheck、严格Clippy、fmt、docs build、19项同源生成检查及canonical daily prepare-only构建通过。新App SHA `b8d68436fb26db18fe838c09dbdac1df2855317fe6068e6356271dbcf51221ff`，receipt SHA `3437292d37e7354ef26765608a01a8195a3efcb8131ed2716ced55d4f2d36694`；119包内文件、1226源码输入核对一致。
- Host a3d8767、Connectors cc56cda、Runtime11fd450/r5、Skills595c927保持。Runtime SHA仍`283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`，无核心/补丁修改。新候选与旧产物分目录，不覆盖原工作区。
- 每次启动前持原实例锁、无原数据句柄，核完整备份/inspection、SQL41/Host及四Runtime库完整性、8条跨存储映射和全模型零派发；第二轮基于首轮完整后态重新检查。fresh D4绑定固定新回执、原Home和Kimi暂停；不重跑D3。
- 实际UI：新建页只列新K31/MiniMax及禁用未来项，K31暂停；8条历史可读，已完成原回答、文件差异/命令动作、失败与中断原状态均可见。2个附件记录保留；旧K3标退役且发送禁用。
- 日常6个旧计划实际为deleted，活动列表为空；原执行/暂停跳过/取消记录可见，详情将K3标为历史模型，已删除目标的重新执行禁用。没有伪造一个活跃旧计划，也没有启用、保存、切换模型或发送。
- 第二轮15:05:39（Asia/Shanghai）以应用⌘Q正常退出，退出码0；App/Host/Runtime/worker/adapter均结束、句柄及实例锁释放。workflow作为原独立依赖保持6 healthy/ready。

首次新UI测试缺happy-dom及completed遮挡提示已修正；首次lint仅新增AJV生成文件未遵循既有精确生成物风格排除；首次Rust错误模块filter为0项，明确不计PASS，纠正后执行1项。扩展回归首次5失败分别为2项候选开关遗漏、3项旧归档/实时进度断言过时，修正配置与测试基线，未改变产品进度逻辑。后态首次递归WAL扫描误包含历史迁移备份；复审改为检查精确活动DB，历史备份原字节保留。没有弱化断言、改执行事实或清理WAL来取得通过。所有原失败和RCA均保留。

## 数据与安全后态

最终完整后态sealed+inspection：17,394文件、522,147,353字节。Native SQL41/71表完整性/FK正常，第二轮67张表逐行相同，包括全部历史、附件、计划、grant与模型操作。仅既有Shopify自动metadata probe产生的installation revision、两种操作回执，以及正常stopped generation改变；原授权generation/凭据引用未变。

首次D4正常将Host10升级11，仅新增/更新元数据；旧业务值保留。第二轮Host全部值逐键一致。Runtime goals/memories/state全行保持，原日志不删，仅追加501条；原rollout未改。活动Native DB及4个Runtime DB的WAL/SHM均不存在，历史备份内WAL/SHM不删、不截断。无强杀、手工checkpoint或自动恢复。

本轮两次启动各有3次既有Shopify初始化/工具目录metadata HTTP，共6次，**它们不是模型HTTP或商家业务工具执行**；不能声称零外部HTTP。模型HTTP新增0，累计仍13；45元上限、29.740299元保守累计及两份14.188544元预占保持，7份旧账本/快照及provider key不变。6个历史已消费grant继续保留，全模型未来/待恢复/活动工作均0。

完整原始UI、日志、DB和私有行事实只保存在`feat164-d4-execution-audit-20261027`，Git只收脱敏计数/判断与SHA索引。证据入口为`evidence/d4-closure-summary.json`、source-binding、checks、structured-review、workflow及private-evidence-index。

## 下一阶段与停止边界

当前没有开放的D4阻塞，下一次可以推进D5的具体日常启用方案与授权。需以本轮已验证的71e39c4候选为准，明确长期入口/短期D4绑定的差异、是否解除Kimi暂停、workflow启动责任和兼容回退，再取得D5执行范围确认。不能复用本轮短期零派发绑定当作长期授权，不覆盖已签名App、不迁回SQL37、不用reader4重开format5历史。

D5本轮未授权/未执行；F61-02长期入口和F61-03本地G5/G6口径仍需收口。D4数据切换验收不是整项G4/G5/G6的自动放行，当前机器门禁保持pending，58已接受本地S1—S4及安全替代证据不改。完整App正向never-sent取消仍NOT RUN；搜索答案正确性及亮暗/键盘/最小窗口均保持Owner排除。没有为这些已排除项追加测试或模型调用。


治理收尾首次audit-claims检测到新增archive immutable引用尚未关联旧G2V/S1—S4记录，已保留原失败。补充逐项当前引用复审，旧真实执行source/time/command/result和原contract集合单列保留；旧r5结果仅用无网络oracle复读，新读取权威由本轮D4独立证据覆盖。没有删除权威、改validator、自动继承新模型结果或新增调用。该关联及最终治理结果见d4-closure-reference-reconciliation与governance-checks。

最终audit-claims、strict包检查、S4 G3、元仓lint、53/53测试及7份Shell语法通过。原10仓HEAD/分支/远端及所有旧dirty字节核对，混合memory只提交新FEAT-164段；六个候选来源干净。最终原日常文件再次匹配完整后态备份，App保持退出，未进入D5。治理初次失败及修正留在证据中，不覆盖原日志。
