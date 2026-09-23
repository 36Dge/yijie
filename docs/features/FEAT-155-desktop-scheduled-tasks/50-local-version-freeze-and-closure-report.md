# FEAT-155 本地版本固化与交付关闭报告

2026-09-24。用户对[49的具体五仓文件、来源锁修订、本地提交和零模型复验清单](49-five-repository-audit-and-freeze-plan.md)明确回复“授权”。据此完成本地固化；没有把授权扩大到push、tag、合并、发布或日常库迁移。

结论：FEAT-155在已批准的`demo_fast + local`隔离候选范围内可以关闭。本地依赖来源已固化，最小缺陷修复后定向回归、最终版本正常启动/退出/重开通过。全仓Skills来源门禁仍单列BLOCKED，不冒称全仓CI或发布完成。

## 1. 最终源码版本

| 依赖顺序 | 本地最终完整commit | 范围与说明 |
|---|---|---|
| Runtime | `fb79b1d53501ec90084b584af5fdbe221c7a25aa` | 278个路径；已审计input-only最小扩展、独立canonical构建和269份schema。 |
| Contracts | `54be9314dce5319b049dc0a236800fd1a1fdd7a1` | 77个路径；6族同源契约、生成器及精确consumer来源。 |
| Host | `56e9a924454e850bd181c452c35078b3e0a36954` | 58个路径；原有执行链上的恢复/草案薄适配，锁定最终C。 |
| Desktop | `be15d237fc0422f6072d0b6ec6d668b49d4c692e` | 162个路径；完整需求实现、精确C/H、版本复验发现的旧中断claim修复。 |
| 元仓 | 以包含本报告的Git提交定位 | 最后提交需求、ADR、授权、原验收及本轮固化证据；不填写自身尚不存在的SHA。 |

主实现按Runtime→Contracts→Host→Desktop顺序提交。Contracts主提交`ccbae065f0294db25562c90cd4d39cf112129d23`之后补生成基线修正；Host主提交`a885c1deea7c8faf9cff140ad8f9d13b837604fb`之后仅跟进最终C；Desktop主提交`98447609e16b5c63781dbeedfd6bc32d8c343807`之后单独修复原生回归发现的问题。七个产品仓本地提交均保留，不amend、改写历史或强行凑成五个提交。

[逐文件增量与最终来源](evidence/version-freeze/source-delta-from-d4-audit.json)以49审计清单为基准。四产品仓原有573个路径均纳入；新增路径只有Contracts来源helper与Desktop既有权限锁（最终575）。无关工作区未清空、未混入。既有Skills版本未改。

## 2. 来源锁与实际产物

本轮contract-impact为semantic：精确部署/构建来源的含义变更；整体FEAT-155仍为breaking。各族wire、DTO、旧迁移、权限和执行授权语义不改，普通SQL15/Store5、隔离候选SQL26/Store6保持。

- Runtime增加真实`runtime_source.full_commit`，保留旧`active_base_commit`的有效补丁来源语义。原269份schema和补丁/构建源逐项与R的Git对象核对。
- Contracts保留历史`base_commit`，同步脚本显式接收已存在的C，consumer快照新增`source_commit/source_lock_path`；来源、生成脚本及输出都与该commit对象核对。没有自引用SHA或任意dirty放行。
- 草案生成器检查模式原先读取当前HEAD，提交后误报生成漂移；改为读取锁中已记录的比较基线。源与生成锁一起提交，实际DTO不变。
- Desktop的Host候选锁按H的Git对象列出封闭输入集，保留旧baseline、`local_candidate/release:false`。已有FEAT152权限锁仅把相同Host来源固定到H，其Contracts权限wire来源不变。
- Desktop私有IPC生成器删除一处行尾空格，通过原生成器刷新脚本摘要；未手改DTO。

保留的合格input-only Runtime二进制SHA-256为`bd7d26205e2d735dcac0f35fc089a7b30a5c18a54586b94a2c7f624f2f5b7672`，356184808字节，本轮未重建或覆盖；见[产物核对](evidence/version-freeze/runtime-artifact-check.json)。新构建仅使用项目既有canonical脚本生成本项目Host/Desktop开发产物。

## 3. 复验发现并修复的最小缺陷

首次固定版本原生检查为131 PASS/1 FAIL，未写成全绿。失败是已释放unknown的旧interrupt仍被普通idle分支领取：SQL的普通分支只检查`scheduled_run_id IS NULL`，使interrupt绕开自身quiescent条件。既有最后发送guard仍拒绝该请求，未观察到真实出站，但claim/租期逻辑不符合既定“旧操作不重发、不占用”的需求。

原测试使用fixture开始时刻，若enqueue跨秒，旧interrupt尚未到查询时刻而偶尔掩盖问题。先把查询时间移到已到期范围，稳定复现失败，再增加普通分支的`kind!='interrupt_turn'`。测试同时使用真实claim方法证明正常interrupt仍可领取，释放后的旧interrupt即使租期已过也不能领取；系统时钟未改变，无进程故障或攻击注入。历史状态、额度、预约释放事实和发送前guard保持。

这是本需求内恢复/防误发缺陷的独立小提交，不混成来源元数据修改；未新增职责、契约、迁移或功能。修复后132项原生回归、fmt/clippy通过。证据保留[首次失败](evidence/version-freeze/desktop-native-regression.txt)、[确定性复现](evidence/version-freeze/stopped-unknown-deterministic-before-fix.txt)及[修复后132项](evidence/version-freeze/desktop-native-regression-after-guard.txt)。一次诊断命令错误使用完整名匹配、实际0项，不计入PASS；单项偶然PASS也不替代根因修复。

## 4. 验证结果与明确限制

| 检查 | 当前结论与证据 |
|---|---|
| Contracts六族来源/生成一致性 | PASS；[最终29项测试](evidence/version-freeze/contracts-final-tests.txt)、[Git来源正反检查](evidence/version-freeze/frozen-source-check.txt)。缺少source_commit或只有旧Host baseline均拒绝。 |
| Contracts lint、四登记基线breaking | PASS；[lint](evidence/version-freeze/contracts-lint.txt)、[四基线结果](evidence/version-freeze/breaking-results.json)。后续只改生成基线读取，不改wire/DTO。 |
| Host安全定向race、lint/vet | PASS；[定向检查](evidence/version-freeze/host-tests.txt)、[lint](evidence/version-freeze/host-lint.txt)。最终H仅补来源锁及说明，所有Go产品代码相同。 |
| Desktop前端、私有IPC | PASS；9文件35项[定向检查](evidence/version-freeze/desktop-focused.txt)、[ESLint/TypeScript](evidence/version-freeze/desktop-lint.txt)、[私有IPC](evidence/version-freeze/desktop-final-ipc.txt)。前端产品代码与48逐字相同。 |
| Desktop原生 | 修复后132 PASS；[fmt](evidence/version-freeze/desktop-fmt-after-guard.txt)、[all-targets clippy](evidence/version-freeze/desktop-clippy-after-guard.txt) PASS。 |
| 标准make lint | BLOCKED于既有Skills HEAD不匹配；[普通](evidence/version-freeze/desktop-standard-lint.txt)及[显式候选](evidence/version-freeze/desktop-candidate-lint.txt)。原Contracts dirty阻断已清除，未绕过现有门禁。 |
| 固定版canonical构建、启动与重开 | PASS；[最终启动](evidence/version-freeze/canonical-final-start.txt)、[最终重开](evidence/version-freeze/canonical-final-reopen.txt)、[原生观察](evidence/version-freeze/native-ui-observations.json)。两次均通过Cmd+Q正常退出、launcher退出0，所管Host/Runtime均退出。 |
| 元仓规则、声明检查 | [lint/governance](evidence/version-freeze/meta-lint.txt)、[测试](evidence/version-freeze/meta-tests.txt)、Shell语法通过；[strict/D4](evidence/version-freeze/meta-d4.txt)仅验证声明结构，不替代原生事实。 |

Skills实际`488714a8d96f40806a257aae097683815b1dd458`，全仓来源门禁期望`10c45bec29603b002e861e1499d5b4e684251af5`；本轮不擅改无关Skills锁。它是全仓检查的明确残余限制，不能把focused PASS或canonical成功写成全仓CI通过。完整历史故障/攻击fixture套件未执行，遵守用户安全条款；未声明完整make test、远端CI、生产/public或跨平台验收。

过程中保留Contracts提交前consumer无法锁定未来C导致的1项失败、初次Host来源校验被草案HEAD基线误报阻断等日志；修复后以最终29项和Git来源检查为准。Runtime `diff --check`提示的13处空白在`.patch`的空上下文行中，为补丁语法，未为消警修改已合格补丁。Desktop普通行尾空格已修正。元仓暂存差异另有62处提示，全部在原始diff上下文与命令输出中，保留证据字节；非evidence文档的暂存diff检查PASS，详见[分类记录](evidence/version-freeze/evidence-whitespace-classification.json)。

## 5. 调用、范围与关闭边界

本轮付费文本0，本机Provider请求0，图片/商家/外部MCP0。累计真实文本仍13/14、余1，见[本轮空Provider账本](evidence/version-freeze/local-provider-ledger.json)；未使用剩余额度重复已完成验收。

[48本地D4](48-remaining-delivery-report.md)的既有Must证据保留；本轮由来源差异审查、最小缺陷修复回归及固定版零调用复验补充，不冒称又做了一轮付费完整D4。范围继续是本人macOS本机显式隔离候选；两项电源需求OWNER_EXCLUDED，系统通知延期，应用内重要更新已完成。普通入口15/5不启用定时执行，日常库不迁移；无云调度、跨设备、通知中心或生产发布承诺。


最终固定D的原生页面重新确认计划暂停/额度耗尽、原生开始时间与0.426秒耗时，记录正确定位同一聊天第3轮；前一轮命令仍为已拒绝。正常重开后同一历史保留。[启动前](evidence/version-freeze/ledger-before.txt)、[最终启动后](evidence/version-freeze/ledger-final-start.txt)、[最终重开后](evidence/version-freeze/ledger-final-reopen.txt)账本逐字相同：12计划、17运行、33 outbox、22轮、11聊天、5草案来源，预约0。原生运行未知/显示不完整仍如实显示，没有补写结果或重发。

退出后的CUA观察曾另开无配置设置窗口，已立即正常退出，无发送或迁移；原始canonical进程已先正常结束。该工具行为单列原生观察，未充作重开验收；后续两次最终版使用canonical入口启动，只用进程/退出码核对关闭。

本地五仓收尾不等于远端交付。若另行需要推送/PR/合并/发布，须按新的明确范围处理；不自动把既有Skills门禁、普通入口迁移或系统通知纳入FEAT-155。
