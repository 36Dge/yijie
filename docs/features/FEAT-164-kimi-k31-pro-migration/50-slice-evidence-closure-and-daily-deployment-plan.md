# FEAT-164 S4W：前三切片证据收口与日常部署最小方案

2026-10-26。Owner要求执行下一步并深入审计修复阻塞。本轮完成当前r5的S1—S3定向复验、317项既有证据/来源核验及暂停App验收，修复S2测试成功后删除Runtime数据的问题。真实模型新增0；沿用49已通过的真实资格，不重复发送42。整项仍IN_PROGRESS，日常数据未读取、迁移或激活。

## 完成结果及判定口径

| 切片 | 当前来源下的验证 | 代表性实际路径 |
|---|---|---|
| S1 | Host11项；暂停App实际Kimi禁用/MiniMax可选/真实历史42可读/发送禁用；0模型尝试 | 49真实K31完成/保存/重开＋本轮同源暂停/正常退出 |
| S2 | Host25+2、Native12+20、实际Native/Host/r5边界1项，共60项 | 46自然旧App迁移/显式选择/正常取消/继续；本轮原生正常重启、原回执/当前选择、never-sent取消0POST |
| S3 | 5项exact计划退役/重审/授权/暂停/重放/worker顺序测试 | 46自然旧计划重审保存仍关闭、新单次grant运行完成、原grant保持、计划关闭及重开 |
| S4 | 46—49已通过子集的317项索引文件逐字核验，6产品来源干净 | 48当前调用面/辅助/子代理/压缩、47媒体、49真实文本继续有效；完整TCONF04/final未通过 |

共76项定向检查全部通过，0ignored；S2边界内部两次Rust phase各1项另有日志，不重复计入76。唯一新增模型协议请求是S2本机MiniMax合成1次，真实HTTP0。暂停App没有提交任务、模型请求或切换旧会话身份。

S1—S3按local、boundary、代表性canonical纵向分别绑定当前产品来源；旧r4命令/来源不再作为当前索引。G3是切片工程完成门禁，不能与全功能GUI/final混为一谈：未决与never-sent的安全语义已有普通状态、真实Native→Host、前端行为验证；代表性旧App迁移/取消/计划纵向已有46的证据。所有未知/never-sent GUI形态尚未自然实跑，继续作为完整业务状态final缺项，不因G3而改成已观察。没有降低不变量、改变AC、伪造例外或修改全局门禁。

46的实际compiled迁移来源是54921df；迁移入口/database/migrations/计划退役/identity五份权威文件与当前9f逐字相同，最终App行为是9f。该组合称source-bound证据，不声称当前media binary重新执行过一次SQL29迁移，也不把多批验证冒充一次fresh全链路。当前执行时刻与证据归并时刻分别由原日志及本轮绑定记录追踪。

产品仍为Desktop9f5814fec6cd071d39f0c12f8f48097ce661cb6a、Host8cd6bccbdc1ac3906aea53d95441299f7cfefcce、Contracts ca06d0999c9a08afe80ab3f34a537d492b830ac7、Runtime11fd4504c28afd0f65c6f5f62a6b5328dd437f5a、Connectors cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9、Skills595c927ae101d3d31c234f60565041eee0864680。App沿用42a23cf…/119文件，Runtime沿用283d12e…r5。

## 修复与安全审查

增量contract-impact=none：只改Host一个测试的输出目录/正常退出后保留行为，不改产品wire、存储、Runtime核心或补丁。提交`f97d2216001e78df02e93c972a6aec2e1d772f58`基于S4U测试提交7bf43fe，299个非测试产品文件与App固定Host8cd逐字相同；App不重建、不刷新pin。

旧`TestFEAT164NativeHostBoundary`的defer会在成功stop后RemoveAll(root)。已改成必需显式绝对保留父目录、创建独立新root、记录路径，仅调用原stop，不删任何Runtime/Host/Native数据。原断言、协议、单次请求及cleanup次序保持；没有新增强杀/timeout-kill、故障注入或权限破坏。当前一轮通过，保留完整副本、无打开句柄、四Runtime库WAL0/integrity ok。Host make lint通过。默认缺少显式integration输入仍不运行该测试，不能把skip算PASS。

暂停App也正常⌘Q exit0，71表全部旧行保持，只有正常停止代际表追加；四Runtime库WAL0/只读副本完整性通过。没有重新安排Owner已移除的亮暗、键盘/焦点或最小窗口专项。

## 日常集成阻塞及根因

原Desktop主树fd0c575仍有100份dirty。将已批准FEAT164六提交（18文件）做只读git apply --check，唯一应用冲突在`contracts/runtime-chat-models.candidate.json`：base为7fd463b，原工作区已有9154f27，新合格候选为11fd450。差异只有runtime_source.base_commit，其余artifact/patch/schema字段相同。五个文件与原dirty有重叠，列表见s4w-source-evidence-binding；原文件逐字保留，没有实际应用patch。

这是旧投影来源锁的集成冲突，不是模型故障。下一步在新隔离集成目录使用已验证的Contracts ca06及原generator结果，保留原主树9154修改及其它需求差异，逐hunk对照；不能手改生成物、强制快进或从干净9f直接覆盖日常工作区。仅FEAT164差异可提交；其它需求不混入。

日常装配还有三个真实边界：当前K31入口强制scheduled candidate并关闭workflow；维护入口只准入两个隔离identity；已有predecessor许可只对固定资格identity开放。日常根现有0755父目录也与隔离维护要求不同，不能机械复用0700限制后chmod日常目录。先前对路径仅确认存在，未打开日常库或密钥；具体schema/未决/计划仍未知。

## 下一阶段可审阅方案（未实施）

推荐分成“实现/独立构建与离线验证”和“日常数据执行”两步。本轮先提交以下确定范围，Runtime/core/补丁不需要改；公共wire/schema无需变化，增量为Desktop私有部署/维护语义变化（semantic），整项breaking保持。唯一Owner/consumer为段成威，不冒充独立人工批准。

限定8个既有实现文件，加对应测试及README/SECURITY说明：

| 文件 | 最小变化 |
|---|---|
| scripts/run-local-demo-fast.sh | 增加显式日常K31选择与独立prepare-only；保留workflow/market/expert/media日常装配；prepare-only不调用workflow-up、不启动App/worker、不读写日常数据库；旧默认入口先保持 |
| scripts/kimi-k31-build-candidate.mjs | 明确区分原隔离四组合和日常完整组合，只有已选择日常profile才接受workflow；来源锁/固定Runtime检查不放宽 |
| scripts/kimi-k31-packaged-receipt.mjs | 独立日常构建输出及receipt，绑定com.yijie.ai、K31编译特性、workflow与完整输入；不覆盖旧bundle/receipt，不将隔离App回执复用为日常资格 |
| src-tauri/src/feat164_qualification.rs | 校验编译identity与日常/隔离flag的配对；隔离规则保持，拒绝混用与仅环境冒充；不增加通用路径参数 |
| src-tauri/src/lib.rs | 明确日常维护参数在auth/worker/Host/UI之前处理，并使用原单实例边界；普通启动不隐式执行维护 |
| src-tauri/src/chat/mod.rs | 仅增加对应native维护入口转发/旧终态读取既有逻辑复用，不建新业务状态机 |
| src-tauri/src/chat/isolated_model_migration.rs | 共享正式迁移但显式区分固定隔离根与com.yijie.ai/demo-fast-v1；保留备份、旧schema保护、静止/unknown/在途/授权拒绝和正常close。日常父目录按既有权限接受规范审计，不改权限；旧隔离入口行为保持 |
| src-tauri/src/chat/sidecar.rs | 将既有受审predecessor许可仅扩到已由native验证的日常K31组合；不授予turn或计划权限，不放宽Host冻结配置对与回执校验 |

实现阶段只使用新独立源码和自然合成数据做离线验证，不启动或迁移真实日常库；旧App/文件/账本/预占全部保留。验证包括：入口与配对矩阵、prepare-only无启动副作用、workflow装配保持、正常锁竞争/静止拒绝、SQL29/37自然迁移、原事实/授权保持、正常关闭/重开、同源回执；不用攻击/破坏或替身binary。source-first仅复用已固定权威，不改公共契约。

日常实际执行必须随后展示具体产物hash、完整加密备份清单、实际只读预检结果及回退路径并取得对应批准。本轮方案不授权日常开库/迁移、推送、发布或替换已签名App。旧guard对occupied_runs>0一律拒绝，已消耗的终态grant不等于全局busy；先保留该拒绝，不清零/退款绕过。若实际日常数据触发，基于终态/原reservation事实提出独立最小判定修复，不猜测它安全。

回退方向为新兼容reader＋暂停Kimi，不恢复旧K3 writer、不覆盖回写原库。失败先正常停止并保留所有新旧状态；新增核心或不在8文件内的权限范围另报。

## 尚未完成

S4完整TCONF04/core与剩余业务状态final仍缺供应商图片/搜索/工具样例及unknown/never-sent完整GUI自然观察；正常teardown与r5文本G2V保持PASS。必要真实功能调用已获Owner授权，无需再次精确查价或重复询问旧6次额度；30元约束与旧预占保持。本文不把本轮零新增调用变成新的付费禁令。

当前只本地提交，原工作区及三份模型账本保持；没有修改日常代码/数据权限。S1—S3 G3与剩余S4机器实检结果及保护计数写入本轮索引。完整私有审计目录`feat164-s4w-audit-20261026`；数据库/密钥不提交Git。

## 实检与后续授权

本轮G3/S1、G3/S2、G3/S3实际退出0；G3/S4退出1，仅保留S4总状态/完整vertical及TCONF04未通过，不再有旧前三片缺项。正常teardown保持PASS。Owner随后明确批准上述8文件实现及安全离线验证，明确“不迁移日常库”。后续实现只在新隔离目录，具体结果另记，不将此批准改写为日常激活许可。
