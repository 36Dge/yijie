# FEAT-164 S4AC：当前证据绑定、业务状态与日常 prepare-only

2026-10-27。第55号旧v3测试修复保持有效；搜索答案正确性继续 OWNER_EXCLUDED。本轮完成当前来源核对、安全业务状态回归、隔离 App 历史重开及日常候选 prepare-only。**真实与本机模型 HTTP 都新增0；日常 App 未启动、日常库未打开或迁移。** 没有修改任何产品实现、Runtime核心或补丁，增量 contract-impact=none。

## 根因复审与证据边界

此前总表仍绑定9f/8cd/ca06，并把“缺真实图片/工具/搜索传输”继续列为阻塞，未吸收52—55的有效证据。这是治理索引滞后；不能用重新调用模型解决，也不能只改SHA把旧测试说成新执行。现保留历史报告，建立逐文件绑定并修正当前矩阵和S4/final判定。

核对46—55的10份索引，共501个证据文件，SHA均一致。Desktop从9f到ea共18个差异路径，310个所核对业务实现文件逐字相同；差异分别是51已批准的日常identity/维护/启动接线、52只移动测试模块、54来源锁和55测试基线。维护入口不是全文件相等，不能沿用50的“五文件全等”说法：它由51自然SQL29/37×隔离/daily四组合验证及本轮Native回归支持。Host从8cd到4f只改一处生产函数safeNativeSourceURL，属于54已批准并验证的来源URL组件筛选；模型执行/恢复/授权未改。Runtime与补丁、Connectors、Skills精确pin不变。

当前Desktop ea8763dfc40466e9b808a1b39afad71dbff1ac56；Host4f966e8ea810d5b094d0b797d291955d6c774844；Contracts c5d138374c102f1a8a11e328a869ec8f91724efd；Runtime11fd4504c28afd0f65c6f5f62a6b5328dd437f5a/r5；Connectors cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9；Skills595c927ae101d3d31c234f60565041eee0864680。各来源干净。实际重开S4AA的c98 App与ea产品/生成物/依赖相同，仅一份前端测试不同，未冒称重建隔离App。

## 本轮实际验证

- 当前前端22项：新K31/暂停MiniMax、旧身份显示、unknown只读刷新和显式原操作恢复、never-sent/取消权限/迟到结果、计划旧模型禁存与新模型保存。
- Host38项（含子测试）：活动身份11、原回执及恢复25、路由授权2。Native未发送取消12、模型恢复及identity21、计划退役/重新授权5项全部通过，无ignored。
- 日常profile入口3项，来源只读检查19项通过。本轮不是51的8项总数，早先进度口述8已在此纠正；不重复计入旧测试，不宣称全仓测试通过。
- 实际隔离App canonical同构建回执校验后重开，活动菜单K3.1/MiniMax、原旧K3线程的已完成/已中断/继续历史、两份保持关闭的K31/MiniMax计划、真实图片和工具回灌完成结果均可读；工具记录显示已完成。旧来源样例18公开URL与partial提示保留，不评判答案正确性、不访问链接。
- 本轮没有点击发送、执行计划、重新授权或恢复。正常⌘Q exit0，fixture正常shutdown204，全部服务停止，0本机/0真实模型HTTP。完整停止副本四Runtime库WAL0、只读integrity ok；71表全部旧行保持，仅正常停止事实追加。

## 三项最终判定及S4

| 项目 | 本轮结论 | 限制 |
|---|---|---|
| S4来源/调用面绑定 | PASS（当前已完成子集） | 48辅助/子代理/压缩、49真实文本、52媒体、53真实图片/工具/搜索传输、54来源显示按各自原始来源关联；不是重新执行这些回合 |
| 核心业务状态安全验证 | PASS（组件/Native与实际App可达子集） | unknown和never-sent已覆盖安全状态/持久边界；固定资格库中没有可自然到达的对应完整App操作链 |
| final core_vertical | NOT RUN完整范围 | 不再缺供应商图片/工具/搜索传输；仅保留上述完整App恢复/取消纵向缺口 |
| final accessibility_visual | NOT RUN完整业务范围 | 名称为治理槽；不含已移除外观专项。实际可达状态已记录，但不冒称完整unknown/never-sent App观察 |
| final teardown | PASS | 当前同源正常退出、无补发、四库WAL0、71表旧行保持；未强杀或手工checkpoint |

S1—S3原G3保持原来源结论，本轮当前源码回归作为补充；S4/TCONF04和G4仍不作全量PASS。避免通过覆盖历史、改写旧库、故意断链或制造故障得到unknown/never-sent。该限制有明确影响，不能因为其它项通过自动消除。

## 日常候选 prepare-only

新目录`feat164-s4ac-daily-candidate-20261027`，从上述干净不可变来源构建，命令：`bash scripts/run-local-demo-fast.sh --packaged --kimi-k31-daily --prepare-only`。最小环境不含模型/工作流凭据；沿canonical标准工具生成，不覆盖旧候选。

构建exit0；直接运行只读receipt `--check` exit0（未用会启动App的daily `--reopen`）。119文件，identity `com.yijie.ai`，App SHA **c29f7e07942038d4c3849ef3a711ed4b501d17daab1478329ba5de6b6321a4d0**，receipt SHA **ee4c53922b9642ffa81c3d6356827df6e8dbdcf6c0ec582e108bc954d768add7**。完整workflow/market/expert/media构建；Runtime仍r5 SHA283d12e…，Host来源4f。构建为未签名本地候选，结论 **OFFLINE_PREPARED_NOT_ACTIVATED**，不代表日常数据资格或发布。

## 保护与异常记录

6673份活动隔离数据外的保护文件、500份本轮开始已存在的dirty文件、7份账本（含历史快照）逐字保持；混合memory只追加本轮段落，原内容另做精确校验。原SQL41 unknown/占用不清理、不退款。累计真实13、45元cap、29.740299元保守累计及两份14.188544元预占全部保持，不重新结算或消费剩余额度。原S4AA、S4X及更早App保留。

只读副本reader首次误用不存在的数据库文件名，在open阶段停止；按目录现存conversations.db和secret路径单次修正后71表完整性通过，未打开源库。审计记录脚本一次缺json导入已修正，仅影响记录写入。保留这些审计错误，未影响产品、无循环重试。没有强杀、攻击fixture、权限破坏、替身程序、WAL删除/截断或手工checkpoint。

## 下一步的唯一边界

先复审完整App unknown/never-sent用例的安全可达入口：优先读取原隔离库已有自然unknown并验证当前兼容候选，不改写该记录、不凭空生成“未发送证明”；若无正常流程可达的never-sent，只保留安全Native/组件证据和NOT RUN，提出具体最小方案再决定，不能把它暗中降成PASS。此步骤不需要新真实模型调用，也不需要为已通过的图片/工具/普通文本重复付费验证。

日常候选已经准备好，实际日常切换另需明确批准具体数据动作：正常关闭旧日常App→完整加密目录备份与句柄核验→仅对备份只读预检→同一候选显式维护→检查迁移/计划/原授权事实→再授权启动。此清单不是本轮执行许可；不能为通过预检清空unknown/占用，也不降库或替换原App。Runtime核心/补丁如确需更改，仍先提方案。

脱敏证据索引：evidence/s4ac-audit-index.json。原始日志与私有完整副本保留在feat164-s4ac-audit-20261027。只提交本轮治理与证据，不合入其它需求，不推送。

治理复核：audit-claims、strict、S1/S2/S3 G3检查、元仓lint、53项manifest测试与7个Shell语法检查通过。S4 G3按预期只报告未完成vertical/TCONF的5项错误，不绕过门禁、不记作新产品故障。
