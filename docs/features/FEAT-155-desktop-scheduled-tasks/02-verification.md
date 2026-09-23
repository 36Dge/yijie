# FEAT-155 当前验收矩阵

2026-09-24版本固化补充：最终来源及正常重开已复核，见[50关闭报告](50-local-version-freeze-and-closure-report.md)。该轮修复旧interrupt领取遗漏，132项原生复验PASS；付费/本机请求均0。以下保留48的实际D4证据，不把不同批次冒称同一fresh run。

2026-09-23。范围以[00现行定义](00-feature-brief.md)及用户最新指令为准。防自动空闲睡眠、睡眠后停止发送均为OWNER_EXCLUDED；系统通知延期。这些不记PASS、不作为本期阻断。原逐阶段计划归档于[历史](history/before-remaining-delivery/02-verification.md)。

本轮验证基于同一最终源码候选，包含必要的正常退出/重开。实际macOS界面使用CUA，固定Runtime、Host及SQLCipher均由canonical入口装配；本机Provider与真实Provider分账。没有将35/37/39/41/45拼成一次fresh run，也没有把声明式Provider写成真实模型质量验证。

## 适用Must

| 用例 / AC | 当前验证与结果 | 证据 |
|---|---|---|
| T01 / 001 | PASS：实际导航、两Tab、搜索/刷新、筛选空态及清空、无营销；排序/分页由当前原生管理检查覆盖。 | native-ui-observations、native-regression |
| T02 / 002 | PASS：当前真实输入保护确认→受限草案→校验摘要→审阅→唯一暂停保存→回查；澄清、无效/多候选、未知回执及重复保存由当前定向测试覆盖。未声称本批重跑所有真实澄清组合。 | provider-ledger #1、native-ui-observations、frontend-focused-current、native-regression |
| T03 / 003 | PASS：跨境占位词、四频率/三目标选项；25:61、空星期、已有聊天未选目标禁保存；每周计划暂停保存并焦点定位；取消及重开。 | 原生UI、管理/兼容定向测试 |
| T04 / 004 | PASS：当前四频率/DST/有界计算及三目标绑定/删除保护/去重定向检查；当前真实专属目标与未来自动执行，待审批时实际忙碌阻断。其它两目标的既有真实结果在当前候选仍可回读，37仅作历史补充，不冒称本轮新付费运行。 | native-regression、真实自动run、当前原生审批链 |
| T05 / 005 | PASS：实际主体编辑、controlled开关、有限审阅→启用→暂停→重启用；重开保留22:52未来槽，到点一次后额度耗尽；revision2编辑不改旧快照。 | 原生UI、Provider #2、只读账本 |
| T06 / 006 | PASS：三图标hover/focus/tooltip与键盘；实际手动和独立重跑，新run/turn及配置差异；待审批重复请求明确拒绝，释放后重新审阅执行成功。 | 本机Provider #1/#2/#3/#4/#5、原生UI/账本、定向去重测试 |
| T07 / 007 | PASS：合成计划删除默认取消；取消无副作用；带历史删除保留两次记录/原对话，重跑禁用；另一个待审批计划确认删除被native拒绝。 | native-ui-observations、ledger-after-local/after-approval |
| T08 / 008 | PASS：无项目筛选；全部状态/已开启/已暂停/已完成文案；按稳定plan ID进入历史；已删除记录可搜索，运行状态独立。 | 原生UI、管理query定向检查 |
| T09 / 009 | PASS：整条记录/按钮均可详情；真实开始时间到秒和IANA偏移、原生耗时；审批未知耗时不代算；自动及重跑分别定位正确第1/2/3轮，旧拒绝仍保留。 | 原生UI与Runtime时间账本 |
| T10 / 010 | PASS（排除项除外）：source-first私有只读IPC，真实未来自动、正常退出/重开、权限预算/同库预约；应用内完成/需处理提示和深链，固定Runtime产生原生批准、正常拒绝及恢复；亮暗、1180×760和键盘。 | 下列定向检查、当前真实与本机原生证据 |

## 验证分层与调用

- 真实Provider本轮3次HTTP请求均200：完整草案、22:52自动纯文本、普通Ask文本确认；累计13/14，余1。第三次模型只输出文字请求批准，没有调用工具，**不算原生审批证据**。
- 本机声明式Provider5次HTTP请求：初次手动、独立重跑、普通`exec_command`批准请求、拒绝后的续文、新配置重跑。真实固定Runtime生成待审批；原生UI拒绝，无命令执行、文件或网络副作用。此Provider无上游代码，不伪造Runtime批准/完成事件。
- 代表性正常failure/retry：已有待审批run时再次确认重跑→原生busy拒绝；删除也拒绝→进入原对话拒绝批准→原生工具标为已拒绝并完成收尾→预约归零→修改配置、重新审阅差异并建立新run→真实Runtime完成。不是表单校验冒充服务失败，也不是攻击/异常注入。
- 真实自动run：`01a0cec0-8aa3-7f73-b13b-46b52b913f36`，22:52:00开始，4147ms；真实文本在未分类消息中可展开，未伪造最终回答phase或业务成功。
- 原生审批run：`01a0cec4-e3f7-7de1-92ac-bbf5ced96e0b`；恢复重跑：`01a0cec6-e85e-7d00-841c-9cbeddbf496c`。原`true`工具已拒绝；不同轮次和历史快照不变。

## 当前检查

| 检查 | 结果 |
|---|---|
| 私有IPC生成/严格一致性 | PASS，ipc-check.log |
| Desktop当前定向前端 | PASS，8文件34项，排除.local等旧副本；frontend-focused-current.log |
| FEAT-155原生回归 | PASS，132项；native-regression.log。新增只读scope/有界/普通SQL15保护2项另有native-updates-verified.log |
| pnpm lint / Vue TypeScript | PASS，frontend-full-lint.log、frontend-lint-final.log |
| cargo fmt / all-targets clippy -D warnings | PASS，fmt-check.log、clippy.log |
| 前端build / docs build / canonical原生build | PASS；既有chunk>500KB警告保留，不扩成分包优化专项 |
| 标准make lint | BLOCKED：Contracts tracked changes保护；standard-lint.log。未清空或修改用户工作区以绕过。 |
| 标准全量make test/cargo test | 未执行完整面：相同dirty生成门禁且历史含禁止fixture。使用安全定向集，不宣称全仓full-green。 |

## 证据索引与限制

目录为[evidence/remaining-delivery](evidence/remaining-delivery/)。关键文件：initial-workspace.json、provider-ledger.json、local-provider-ledger.json、native-ui-observations.json、各检查日志、最终源码审查/状态摘要及重开对照。截图和AX观察来自本任务CUA原生轨迹；原PDF不是验收截图。

- 范围仅macOS本人本机隔离候选。普通SQL15/Store5保持；候选SQL26/Store6。本轮无新migration，无日常库迁移，无生产或发布证据。
- 系统通知延期；两项电源需求明确移除，不进行专项实现或真实睡眠验收。既有公共生命周期代码未扩展或重构。
- 冷空历史与Provider缺phase仍沿原有诚实未知/可展开显示。运行completed不代表工具批准或业务成功。
- 应用内提示按scope/run/state内存去重；首开只提示未处理事项，最多50条有界原生feed、最多3个提示，结束提示15秒。历史持久可查；不建设通知中心或跨设备送达保证。
- 强杀、恶意载荷、权限破坏、可执行伪装、系统时钟修改、生产/商家调用未执行；不伪造相关韧性覆盖。

最终正常重开对照PASS，账本逐行一致，预约0，无新增请求；D4结论及机器声明校验见48报告、feature.yaml与d4-check.log。

固定版本关闭：Runtime→Contracts→Host→Desktop完整SHA及源差异、后续缺陷修复、两次canonical正常启动/退出与不变账本见50。全仓门禁当前阻断从Contracts dirty前进到既有Skills HEAD不匹配；未改变Skills锁或降低门禁。D4的本地范围保持，不代表远端CI/public/生产通过。
