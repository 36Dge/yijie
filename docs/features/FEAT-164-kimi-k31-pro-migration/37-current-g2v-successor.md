# FEAT-164 当前G2V与schema3预算续期

## 已批准范围

2026-10-26 Owner先确认36中新增1次真实普通文本HTTP，随后直接补充“可以额外新增2次”。已明确回告按1+2解释：本轮最多新增3次、累计最多5次模型HTTP，累计费用仍30元，输出最多8192，所有标题/辅助/工具后续都计数，失败即停、不自动重试，本次不使用搜索或图片。没有日常库迁移、推送或发布授权。原账本及14.188544元unknown预占保持。

## 续期实现与审计

Desktop `ea9b1e499d86bb92eea360a62707027485790e22`仅本地固化5个验收工具/说明文件。contract-impact=semantic限于私有验收账本schema3与消费者，不改产品wire/SQL/权限/Runtime；旧schema1/2解释保持，整项breaking不降级。

新同目录唯一`g2v-real-budget-ledger-r3.json`由显式授权离线创建；源与目标分别flock，原账本SHA/完整原始JSON/解析状态/两行摘要绑定。旧schema2文件逐字保留，已有后继幂等返回而不覆盖或补额。每次先串行预占，真实成功且有明确usage才释放差额；新增unknown、HTTP/终态失败或不完整均停止，即使费用可结算也不继续。金额先于次数，余量不足即拒绝。中文Owner的Python writer→JS reader互操作已验证；旧PASS不能替代新调用。

普通临时文件/内存控制23项及判定器10项通过，ESLint、Python语法、docs build通过；无真实调用、无攻击/权限故障/程序替身。两次命令编排目录错误保留，首次2项为unittest loader错误、测试主体未启动；另一次未成功写入新增JS，Node只执行7旧项，未拿退出0冒称10项。改用绝对路径和精确计数后23/10实际通过。见s4k-meter-qualified-final.log、s4k-verdict-qualified.log及原日志。

## 当前候选和正控

在新物理sibling目录`feat164-s4k-qualification-20261026` canonical构建media组合，旧bundle保留。Host090c2db、Runtimea28130a、Contracts1b357cc、Connectors7ea3df4、Skills595c927保持。新source/完整bundle/worker/adapter由canonical receipt绑定。无签名/发布产物覆盖。

真实App→Host→r4→本机Responses正控1次，观察到K3.1/max和明确合成答复；正常退出、同构建重开后状态及内容保存，重开0模型请求，再正常退出、fixture shutdown。当前工具/本机App资格见s4k-harness-qualification.json；仅限定文本验收资格，不是整项G3或供应商能力通过。

## 真实验收阶段

真实meter已从原owner-only Kimi凭据启动，后继账本仅含保留的旧2行，新增真实HTTP当前0。当前同构建App已启动；最初显示的是2026-10-25的旧42历史，明确不作为本轮结果。两次UI操作被“用户正在操作窗口”保护拦截；已请求在Owner查看完成后交回窗口，预算无需再确认。本轮新建任务及真实发送尚未执行。后续真实结果、费用、保存/重开与清理在下文追加，不用旧历史代替。

## 价格与覆盖限制

2026-10-26复核[官方首页](https://platform.kimi.com/)仍列K3.1 Pro输入/默认缓存写入13、输出68元/百万token；[Responses规范](https://platform.kimi.com/docs/api/responses)固定端点api.moonshot.cn/v1/responses。本次缓存按输入全价保守结算，原8192覆盖及移除原生搜索明确记录，SSE原字节转发；不声称验证原始默认输出上限、真实图片/搜索/工具。旧上界14.328134，单次预占14.188544，在途上界28.516678，仍受累计30元限制。

当前交接记录：真实计量器已通过control/stop返回204并正常退出0，后继账本meter_state=stopped_normally、原2行不变、新增0/3。候选App仍为PID68433，留供Owner查看；没有强行退出、没有把该实例声明teardown完成。继续时先确认窗口控制、核对来源与后继剩余额度，以同一工具正常重开meter（不创建/重置新账本）后再发送；预算不再要求重复批准。

治理自审：首次claims发现文本编辑命中了G2V字段名中的子串并截断了顶层结构。尚未提交，已从本轮原HEAD只重建feature.yaml的本次改动；以锚定顶层块、末尾evidence reason定位，并解析验证整个temporal matrix、gates和其它harness逐值不变。失败日志和RCA保留。修正后claims/strict通过、实际G3/S4仍退出1，元仓53测试和7项Shell语法通过；没有把文档修正或本机正控当真实G2V。

保护审计确认496原dirty、1352旧证据（含原真实账本）、154资源、7日常数据库、406旧bundle文件及5525候选事前备份文件保持；当前bundle/source匹配receipt。当前候选数据库的最终比较等待正常退出后进行，未复制在用数据库或声称live App已清理。新后继账本是受授权的活动账本，后续只允许按范围追加；原schema2账本仍必须逐字保留。
