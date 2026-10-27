# FEAT-164 第74号：当前来源、入口与清理后文档同步

2026-10-28。Owner批准按第73号后态复审修正文档。**当前矩阵、feature.yaml和基础包现统一绑定第71号新位置资格与第73号清理后态；旧67/69来源明确保留为历史。** 本轮仅文档及脱敏检查记录，不修改产品、Runtime、契约源、Gate判定、预算或部署授权；不运行App/模型、不开日常数据库、不操作workflow、不推送。

增量contract-impact=none：没有改变跨进程、跨仓、持久化、权限或部署的可观察行为。整项原breaking分类及ADR-0022个人Mac范围保持。

## 当前事实与来源

- 固定来源：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/.local/daily-source/20261027-01`。8个干净worktree连接原仓Git对象库，Runtime映射到原`yijie-codex`。
- Desktop `a211c2d04def6091352c7b3674a49355cdee18ed`、Host `7309101726dcecd48b2caa02401cfcdd6126f1fb`、Contracts `d5792d6aad18352ce8d1c5d510d345004cab3bd6`。Host/Desktop/Contracts以原仓本地集成分支`feat/feat164-consolidation-20261027`保留；原脏主工作区未切换、未合并到该tip。
- App SHA `80b9514a9a389ed023286eee6f10021efc14caa242677b6af3d22ca192042f4e`，receipt SHA `86de538f8bd6fc49c53a48d7cc3a9942c74a0c4b45d6763fc566602aa7420a8a`，schema2绑定SHA `57edb7a822ee0a9658c18be4efecd5c11bd74cf98689fa79c3eebb42f7aea37c`；119包内文件/1228源码输入。
- 两个桌面入口均指向当前固定来源，正常入口启用K3.1 Pro，暂停入口仅暂停Kimi且保留MiniMax。8个当前来源仍是必要依赖，不能当旧目录删除。
- [71](71-original-repository-daily-entry-consolidation.md)记录独立新位置的3轮实际启动/历史检查/正常退出及入口切换；完整后态17,400文件/522,551,359字节。该轮模型HTTP0、非模型metadata HTTP9。其ready和App停止状态保持原观察时点，不冒充当前实时探测。
- [72](72-final-six-directory-cleanup-audit-and-plan.md)为最终精确清单及恢复边界；[73](73-final-six-directory-cleanup-completed.md)记录获批后的6目录/26 worktree正常移除和清理后prepare-only通过。两轮74个旧顶层目录已不存在，活动旧路径依赖为0；12原仓、新来源、原改动、归档/bundle和账本/预占保留。

## 修正位置与历史保留

1. `current-acceptance-matrix.md`更新当前来源、回执、启用绑定、清理后态和回退边界；原AC及final判定和执行来源不改。同步前完整矩阵原文保存在[67/69历史快照](current-acceptance-matrix-history-report67-69.md)，明确不是现行部署指引。
2. `feature.yaml`将原`current_completion_audit`原值移至`historical_completion_audit_report67_69`，将原产品验证/持久启用摘要分别保留于对应历史字段。新的当前记录分别绑定71运行观察与73清理检查，区分其App启动数、model/metadata调用数和后态。原D1—D5计数/授权标明历史，不再次授权执行；原local release批准时间和范围不改，仅增加新来源证据导航。
3. 00—10及04A共12份基础文档更新当前导航；00/01/03/06/07/09/10的旧D5当前段落标为历史，正文原样保留。00和10补当前收敛摘要，09补清理后恢复限制；08只追加`E164-CONSOLIDATION-CURRENT`锚点，不改旧验证正文。
4. 11—73原报告、所有原证据、来源锁、ADR、Validator和测试实现保持。原G2V、S1—S4、final、失败熔断、BR/AC/时序规则、预算及Owner授权值保持；没有把历史模型或App运行改成新候选实跑。

## 接受范围与回退

S1—S4、D1—D5及后续来源/入口收敛C1—C5在批准范围完成。完整App正向never-sent取消仍NOT RUN，使用Owner已接受的安全分层替代；搜索答案正确性/指定页面命中/确定回答质量与亮暗/键盘/最小窗口专项仍OWNER_EXCLUDED。搜索接线/sources安全传递、业务状态、Key/审批/计量和正常退出要求继续保留。

旧.command不能直接拷回后运行；旧D5恢复须按72/73核验归档、两轮Finder补充、refs/bundle，重建精确目录/worktree和依赖，再建立数据兼容、完整备份、实际ready与零模型运行资格。未执行删除后的旧D5重建运行演练；再生缓存不是完整备份，保全同盘不是异地灾备。不覆盖新数据、不降schema、不重跑D3、不手工checkpoint或删/截断WAL。

## 检查与保存保护

验证对象为文档语义、历史保持、来源绑定和当前文件状态：逐字段核对原YAML历史对象与关键Gate/授权/失败/验收对象保持，逐文件核对基础正文/原报告/证据，复核新hash与既有71/73制品及两入口，执行元仓lint、57项治理测试、claims、strict/G6和7份Shell语法。具体实际返回码与内容检查结论见[文档同步检查](evidence/consolidation-document-sync.json)。这些检查不构成新的App、模型或生产验收。

私有修改前快照、12仓基线、检查脚本/日志和隔离暂存记录位于`yijie/.local/consolidation-doc-sync/20261028-01/`。只本地固化此次文档，不混入原memory、FEAT-162/163、budget lock或其它工作区改动。

## 实际复核结果与检查修正

元仓lint、claims、strict/G6及修正后完整57项测试通过，7份Shell语法通过；12份基础正文可逆比对一致，旧完整矩阵快照逐字相等，原AC/final表和替代/排除行未改，2,254份原报告及证据保持，69个本地链接核对通过。原YAML完成/产品验证/启用对象完整保留于历史字段，原Gate、G2V、切片、final、失败、预算及授权对象值未变。12原仓、8个当前来源、510保护文件、旧归档/bundle和原未暂存patch保持。

私有历史检查首次发现两处文档/观察问题：校验脚本模块相对路径多上溯一级，以及将旧矩阵原文放入evidence子目录导致历史相对链接失效。已修正私有模块定位，将新历史快照放回同级目录并保持完整旧正文；单次复验通过，未修改原历史文件。

首次同一并发批次的claims、strict/G6及元仓测试均指出新增段落缺少治理要求的显式evidence标记；元仓测试为55通过/2失败，两项均调用同一包校验器。已按同点三次条件完成根因复审，确认Markdown标题不能替代HTML evidence标记。只在新追加段落补齐唯一标记，不修改validator或放宽断言；定向门禁通过后，单次完整复验57/57通过。初始日志、三次同点复审及修正证据全部保留。没有新增产品运行或以文档将历史失败改绿。
