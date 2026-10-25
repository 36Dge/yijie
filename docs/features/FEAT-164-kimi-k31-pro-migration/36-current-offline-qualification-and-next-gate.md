# FEAT-164 当前离线资格收敛与下一步边界

## 本轮结论

S4J（2026-10-26）补齐当前来源的迁移/恢复/取消、计划、专家/媒体和已启用辅助调用验证。仅修改Desktop既有S2验证脚本；产品代码、wire/SQL、权限和Runtime不变，contract-impact=none，整项breaking保持。整项目标仍是全部活动Kimi使用kimi-k3.1-pro/max/1048576，并安全完成日常cutover；本轮不启用日常入口、不新增真实模型HTTP。

来源：Desktop `bad75a2d3c4a97be903b57e8bb3a3a72915edd18`，Host `090c2dbeeeceb0fc87e576d8e13f5c339bf106f0`，Contracts `1b357cce0575c492f3715b316ee5f254051acf80`，Runtime `a28130abb13d0f99a00107cd513a653bae878b77`，Connectors `7ea3df41818fd69f4736722d01f0686d584d1a71`，Skills `595c927ae101d3d31c234f60565041eee0864680`。

## 验证入口修复与实际执行

原S2 broad selector固定期望10项，当前实际列出17项；新增项是已有reader/草案/暂停及专家切模型回归。提交716a3e4仅更新精确期望17，不删selector或断言。首次运行Host25、路由2、Native派发12通过，但17项中3个草案IPC在新K3.1意图入口拒绝。核对原S4g通过环境，根因为driver仍给这一组传未带候选开关的env。提交bad75a2仅改为同driver已有candidate环境，保持exact local/demo_fast/chat_models/candidate，未改产品门禁。一次修正后完整复验通过，首次FAIL和RCA保留；没有第3次尝试。

| 当前执行 | 结果与确切范围 | 证据 |
|---|---|---|
| S1活动身份/前身 | 10子例+1父项通过，0skip；未知/半配置拒绝，Home/trust保留，退役准入与暂停 | s4j-s1.log |
| S2时序/迁移/恢复/取消 | 五组25/2/12/17/1，共57通过、0skip；真实Host/Runtime/Native正常边界，缺回执不重投 | s4j-s2-qualified/result.json |
| S3计划 | 五个exact入口各1通过；暂停、撤有效授权、重新审阅、worker顺序、旧run/grant保持 | s4j-s3/result.json |
| S4专家/媒体/辅助 | ordinary/market/experts/media四组合source通过；1/3/4/1行为检查，37专家资源，真实worker/adapter/r4 | s4j-s4b/result.json |
| S4旧loaded与自动压缩 | 7项、6个完成账本、23次loopback；旧父子cutover、retired guard、原生failed及冷历史、previous_model/自动压缩 | s4j-s4e/result.json |
| Renderer状态/取消 | 七文件18项通过、0skip；旧retired/unknown只读刷新、原操作显式恢复、迟到结果隔离、取消与计划 | s4j-renderer.log |
| 判定器 | 7项通过；故障归因、未知证据、协作取消与真实结果/保存/重开要求 | s4j-verdict.log |

S4b为13次、本轮S4e为23次本机合成模型HTTP，共36；真实模型HTTP0。没有为了验收启用产品原本禁用的能力；market/expert仍禁multi_agent/memories，普通已启用的原生代理/Guardian单独验证。未执行强杀、恶意/攻击fixture、权限破坏、可执行替身或日常数据migration。

## TINV/AC覆盖收敛

| 领域 | 当前已具备的安全证据 | 尚不可声称 |
|---|---|---|
| TINV01 / AC001–002 | 当前S1、四组合来源、S4I默认值修复及选择器；固定配置/identity/retired截止点 | 日常默认入口已切换、真实Provider全部能力 |
| TINV02 / AC003–005 | 当前S2带数据15/29/37→38/39/40兼容与旧事实；新旧operation恢复、原回执、never-sent取消；前端18项；S4I实际unknown历史保留 | 无原Host回执的unknown已恢复；旧K3 App迁移已实测 |
| TINV03 / AC005–006 | 当前S3五项、S4F/H实际草案/保存paused/单次授权/历史，S4I旧计划/grant/run逐字保持 | 日常旧K3计划已升级或获得新自动授权 |
| TINV04 / AC007–009 | S4I普通/标题/input-only/图片/工具回灌6次独立协议及媒体App；本轮当前专家/媒体/代理/Guardian/自动压缩；旧schema/权限/预算不变 | 真实图片/搜索/工具供应商资格；将多批合成证据拼为完整真实G2V |
| AC010 | S4I正常中断/继续、亮暗1180×760、显式MiniMax兼容、正常重开清理；本轮同产品源连续性及退出检查 | 当前最终freshness、独立三项final、日常cutover已完成 |

04A以前仍称S4测试入口未创建，已纠正为实际存在的三组driver及范围。TCONF-164-01/02/03更新为本轮确切来源和结果。TCONF-164-04保留总体NOT RUN：安全工程覆盖已列全并验证，但现有三个driver分别自声明subset，App/真实Provider/最终freshness属于独立仍缺的证据，不能只改标题或状态声称完整通过。**下一轮不应以重复这些离线子集为主要工作。**

当前Desktop与S4I实机399bb19相比仅`scripts/feat164-s2-conformance.py`变化，产品源相同。原App结果继续归属399bb19，不改写为bad75a2实跑。canonical receipt包含该验证脚本，故新HEAD的完整receipt失效：后续需要新的canonical构建/资格，不能直接用旧receipt启动冒充新来源。本轮保留原bundle不覆盖。

## 旧K3 App场景的真实可达性

只读查询S4I最终SQLCipher快照的非内容metadata：14个K3.1/ready、1个K3.1/unknown、1个MiniMax/ready、1个K3.1计划；旧K3会话/计划均0。没有可在当前候选App自然操作的旧K3升级场景。当前迁移/恢复/取消由正常临时库、原Host服务/真实Runtime、前端领域交互证明；不能改候选库制造旧身份，也不能把该范围当作日常用户库升级实测。

日常库未打开迁移、未作为测试fixture。旧unknown `f38666dc-d2d8-4101-b498-eccf3045b6dd`保持原请求，不按404恢复、不换ID。自然可达App缺项继续明确NOT RUN，后续日常cutover审批必须看到该限制；不偷偷将它记为N/A/PASS或增加无限离线重测。

## 下一步可审阅的执行方案

1. 保持当前产品来源与旧证据，完成新canonical候选和验收工具资格；修正后的验证driver本身不改变产品行为，但不能跳过来源receipt。
2. 当前真实账本schema2、2/2已用、halted且stopped_normally。现有meter/verdict精确锁定2026-10-25的唯一续验授权，这是有效保护，不能重用旧authorization_id来放行第3次。准备新批准时应采用新的明确回执和独立后继账本，绑定旧账本SHA，旧文件/请求行/unknown预占逐字保留；不得先写“已授权”。
3. 建议的最小下一次真实资格仅新增1次普通文本模型HTTP，累计金额上限仍30元、输出最多8192；所有标题/辅助/续请求都计入这一总次数，失败即停、没有自动重试。验证问题为“FEAT164 当前候选验收：计算17+25，仅回复结果42。”；本次不主动调用搜索、图片或工具，仍保持既有审批边界。新授权获准后先完成meter/判定器的对应闭集续期验证及新canonical来源，再启动计量器和App发请求。此方案目前是待批准提案，新增许可仍为0。
4. 取得真实结果后以实际保存/重开/无补发/清理形成当前G2V，再分别给出final core/visual/teardown；真实图片/搜索/工具尚无资格，若最终AC要求实际Provider覆盖，必须单独给出有限次数/费用方案，不能用该1次文本替代。
5. 日常cutover另需明确数据/入口范围批准与兼容reader预检。既有日常数据库和已签名/发布产物不由本轮替换；保留旧历史、授权及来源。最终以活动Kimi全面替换作为FEAT164完成标准。

此方案没有降低Must AC或把真实资格改成单元测试；不能自动豁免旧K3 App场景或用剩余资金增加请求。整体仍IN_PROGRESS，G2V/G3/final不放行。

## 保护与本地固化

496原dirty文件扣除本轮唯一脚本差异后保持；1294旧证据、154既有资源、7日常数据库、406旧bundle文件和5525候选数据文件逐字一致。两条Desktop提交均仅验证脚本，索引/分支/remote边界复核。真实账本原SHA `2dbd19be2a8bda267437bcf0330fff1af122778388d6e3df965291ec840b7dcf`、14.188544元unknown预占及14.328134元累计保守上界保持。检查进程正常退出，无候选App启动；不推送/发布。

与实施分离的复审核对了：两次提交仅改验证driver，17项由实际list锁定、候选环境沿原配置；未移除失败测试或放松阈值。旧账本停止态/原授权ID限制正确，不应为续验先扩额度。当前产品源与原App行为证据的连续性成立，但receipt因脚本变更需重新资格。未发现本轮产品行为回归；实际claims/strict为PASS，G3/S4退出1保持阻断，元仓53项测试/7项Shell语法检查通过。此为Codex结构化自审，不伪称Owner独立人工批准。
