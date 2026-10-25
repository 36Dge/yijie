# FEAT-164 阶段交付

> 当前（2026-10-25，方案A原生终态修复）：Runtime r4 a28130a → Contracts1b357cc → Hostb9155a3 → Desktop2fb8989已本地固化。原子代理错误被completed覆盖及冷历史丢失失败已修复；10项核心、269 schema零差异、7项原生/23次本机HTTP证据复核、3辅助/9次与4调用面/6次均通过。新增受管writer标记阻止旧r2候选写入新历史；不改旧历史。全轮50次合成本机HTTP、真实新增0，旧账本/预占保留。App本批仅构建，完整UI/计划/恢复取消/平台/G2V/G3/final仍未通过。最新权威见[31](31-s4-native-terminal-repair.md)及feature.yaml；以下旧阶段保持历史含义。

> 当前（2026-10-25，S4旧线程/子代理/自动压缩）：Host验证提交df06a3c仅新增测试、driver和说明，产品组合仍为Desktopa0a4743/Hostcac2d4d/Runtime074417e5。干净来源独立子集6项PASS、14次loopback，覆盖旧父子loaded后正常停机/显式切换、当前及迁移后自动压缩、previous_model两分支零旧出站。但旧模型子代理被guard拒绝后，wait_agent和thread/read仍报告completed，实际缺陷保持FAIL；S4 blocked，完整TCONF/G2V/G3/final不放行。全轮71次合成本机HTTP、真实新增0；旧账本/预占保留。最新权威见[30](30-s4-loaded-legacy-compaction.md)及feature.yaml；下方各批次保留原来源。

> 当前（2026-10-25，S4同源App/UI）：Desktopa0a4743在固定Hostcac2d4d/Runtime074417e5及专家资源上完成本机App验收子集；修复Worker物理路径、最小窗口裁切和暂停Kimi历史阻断启动。普通/专家媒体、历史重开、暂停与MiniMax、亮暗最小窗口及正常清理已验证。10次loopback、真实模型新增0；系统浅色已恢复，旧账本/预占和原工作区保留。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final仍pending。最新权威见[29](29-s4-canonical-app-ui.md)与feature.yaml；下方记录按原时间与来源保留。

> 当前（2026-10-25，S3）：Contracts2dd214d / Desktop4d04597已本地固化计划退役、SQL41和授权保护；TCONF-164-03五项、70前端及当前源S2复验通过。App/UI/平台与完整G3仍NOT RUN，真实模型新增0，旧账本/预占保留。最新见[26](26-s3-plan-retirement.md)及feature.yaml；下面旧阶段结论按原来源保留。

> 当前（2026-10-25，Native恢复接线）：Desktop f341636已完成SQL39新意图、只读查询和显式恢复，定向检查通过；旧pending不回填，已发/未知且404不重发。App未重建，平台UI继续延期。完整S2还缺never-sent证明与取消，G3/final未通过。最新见[23](23-native-model-recovery.md)和feature.yaml，较早记录按原来源保留。

> 当前（2026-10-25，UI延期/S2基础）：Owner允许锁屏所需步骤延期并先推进离线实施，UI仍NOT RUN。Host Store11、v2原回执/显式恢复及带数据SQL升级验证已本地固化；Native恢复接线/never-sent取消、S3/S4与完整G3/final尚未完成。真实模型新增0。最新权威见[22](22-ui-deferral-and-s2-foundation.md)和feature.yaml；下方旧阶段记录仅按其原来源和时间解释。

> 当前S1（2026-10-25）：源实现、local/boundary及canonical构建已完成；本机新Kimi正控通过，暂停/MiniMax/重开及最终清理因Mac锁屏未完成，S1 G3不放行。新增真实模型HTTP为0，旧账本逐字保持。最新来源、未执行项和续办见[21](21-s1-implementation.md)。下方20及更早阶段结论按原来源和时间保留。

> 2026-10-25本轮更新：已完成验收判定、30元/唯一新增HTTP恢复及实际文本G2V（PASS）；本地固化与最终审计见[20](20-budget-resume-and-g2v.md)。累计2 HTTP，新请求次数耗尽；旧预占保留。整体FEAT-164仍active，S1—S4及最终迁移验收未完成。以下旧阶段记录按原时点解释。

> 最新（2026-10-25）：首次真实G2V返回HTTP400、无usage，14.188544元预占保留。已自行修正include规范差异并本地固化r2，离线验证进展见[19](19-responses-400-audit.md)；更早阶段的授权、预算与通过结论仅按当时范围解释。

> 2026-10-25 用户已明确恢复，沿用 20 元及搜索/图片授权。当前进度与预算边界见 [18 恢复实施记录](18-resumed-g2v.md)；17 保留暂停时历史状态。G2V 尚未通过。

> 2026-10-25 当前进度：原隔离清单三仓已本地提交，G2A PASS；Host/Desktop 最小候选及普通本机联调完成，G2V、S1—S4/final 仍 pending。当前证据和续办边界以 [16 下游候选审计](16-downstream-candidate-audit.md) 与 feature.yaml 为准；以下早期阶段记录保留其历史含义。

Owner确认后的第一阶段已实现：独立模型v2契约/生成SDK、历史v1请求与结果snapshot读取、新执行活动身份约束、显式恢复/只读回执路由；独立Runtime 0007补丁及未激活kimi-k31-pro-r1候选；对应Contracts来源投影和安全验证。实际审计与验证见08/13/14。

本阶段修复了历史成功回执不能改为v2、OpenAPI模型准入错误未完整声明、目录可用性与原因矛盾、生成枚举重复和离线canonical引用问题。旧v1源、旧Runtime补丁/制品、现有Host/Desktop/Connectors工作树保持；没有应用切换、用户库操作、真实模型/业务调用或Git动作。

整体仍未完成：G0/G1/G2 pass；G2A/G2V及S1—S4、G4—G6 pending。源检查通过不能替代Consumer Owner批准、不可变来源、迁移与真实端到端资格。

下一步是审阅14与隔离变更清单，批准仅FEAT-164的本地Runtime→Contracts→治理材料提交，形成G2A所需不可变引用；不包含推送、不混入FEAT-162/163既有改动。之后继续最小纵向候选和后续切片，真实付费/日常库激活仍按本Feature范围确认。
