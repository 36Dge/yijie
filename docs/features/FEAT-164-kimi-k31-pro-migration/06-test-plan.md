# FEAT-164 测试与证据计划

> 最新按[39 证据绑定与三项最终验收](39-evidence-binding-and-final-verdicts.md)：当前来源141项＋4source和可达App验证通过，新增真实模型0；S1证据收口，S2/S3/S4保留完整纵向缺项。视觉单项PASS；core及Runtime checkpoint完整teardown未通过。两份真实账本、旧预占和日常库保持。以下旧记录按原时间与来源解释。

> 2026-10-26最新续办以[36 当前离线资格与下一步](36-current-offline-qualification-and-next-gate.md)为准：当前S1/S2/S3及S4专家/媒体/辅助/旧线程安全检查通过，产品代码未改；候选无旧K3会话/计划可自然升级。完整G2V/TCONF/final与日常cutover仍缺，新真实HTTP许可0；后续避免反复运行已通过子集。

> 最新续办与整项目标以[35 当前组合与完成差距](35-s4-current-media-and-completion-audit.md)、feature.yaml及S4I证据为准。旧阶段记录保留其原来源和时间；当前仍未切换日常入口，不新增真实模型HTTP。

> S4I结果：Desktop399bb19/Host090c2db配对专家切换、r4媒体/正常中断/图片、同源重开及清理通过；旧unknown仍保留阻断。当前安全子集分组通过不等于完整TCONF/G2V/G3/final。后续按35末节整项执行单推进。

> 当前（2026-10-25，S4f普通App与计划）：Host7927ee7补齐已有v2草案三路由，Desktop277f59e兼容读取原生事实2/3/4；Runtimea28130a r4与Contracts1b357cc保持。同源App验证旧历史、input-only草案、只读恢复零补发、关闭保存、单次执行、取消编辑和正常重开；App模型协议loopback共3次，真实新增0。旧失败请求/事实/账本保留；完整恢复取消、旧模型计划、专家媒体当前组合、平台/G2V/G3/final仍未通过。权威见[32](32-s4-r4-app-plan-acceptance.md)。以下记录保持原来源与时间语义。

> 当前（2026-10-25，方案A原生终态修复）：Runtime r4 a28130a → Contracts1b357cc → Hostb9155a3 → Desktop2fb8989已本地固化。原子代理错误被completed覆盖及冷历史丢失失败已修复；10项核心、269 schema零差异、7项原生/23次本机HTTP证据复核、3辅助/9次与4调用面/6次均通过。新增受管writer标记阻止旧r2候选写入新历史；不改旧历史。全轮50次合成本机HTTP、真实新增0，旧账本/预占保留。App本批仅构建，完整UI/计划/恢复取消/平台/G2V/G3/final仍未通过。最新权威见[31](31-s4-native-terminal-repair.md)及feature.yaml；以下旧阶段保持历史含义。

> 当前（2026-10-25，S4旧线程/子代理/自动压缩）：Host验证提交df06a3c仅新增测试、driver和说明，产品组合仍为Desktopa0a4743/Hostcac2d4d/Runtime074417e5。干净来源独立子集6项PASS、14次loopback，覆盖旧父子loaded后正常停机/显式切换、当前及迁移后自动压缩、previous_model两分支零旧出站。但旧模型子代理被guard拒绝后，wait_agent和thread/read仍报告completed，实际缺陷保持FAIL；S4 blocked，完整TCONF/G2V/G3/final不放行。全轮71次合成本机HTTP、真实新增0；旧账本/预占保留。最新权威见[30](30-s4-loaded-legacy-compaction.md)及feature.yaml；下方各批次保留原来源。

> 当前（2026-10-25，S4同源App/UI）：Desktopa0a4743在固定Hostcac2d4d/Runtime074417e5及专家资源上完成本机App验收子集；修复Worker物理路径、最小窗口裁切和暂停Kimi历史阻断启动。普通/专家媒体、历史重开、暂停与MiniMax、亮暗最小窗口及正常清理已验证。10次loopback、真实模型新增0；系统浅色已恢复，旧账本/预占和原工作区保留。完整旧K3 cutover、计划/恢复UI、跨平台、当前G2V/G3/final仍pending。最新权威见[29](29-s4-canonical-app-ui.md)与feature.yaml；下方记录按原时间与来源保留。

> 当前（2026-10-25，S4专家/媒体/辅助续办）：专家pin已按Skills595c927不可变同内容来源修复；Hostcac2d4d、Desktop56f5284、Connectors1f15726已仅本地固化。四组合source、37专家版本安装/解析/重开及专家/媒体/原生辅助调用安全离线验证通过；S2/S3/S4当前源回归通过。完整TCONF-164-04、App/平台/G2V/G3/final仍未完成，真实模型新增0，旧账本/预占保留。最新见[28](28-s4-expert-media-auxiliary.md)及feature.yaml；下方段落保留各阶段历史范围。

> 当前（2026-10-25，S4）：Contracts eddc64f → Host9ffcb6f → Desktop704cfdb/e408047已仅本地固化全调用面接线；安全子集7/4/4/4/5、S2和S3当前源回归通过。完整TCONF-164-04、专家资源/媒体、辅助动态调用、App/平台/G3/final仍未完成；真实模型新增0，旧账本/预占保留。最新见[27](27-s4-call-surface-wiring.md)及feature.yaml。

> 当前（2026-10-25，S3）：Contracts2dd214d / Desktop4d04597已本地固化计划退役、SQL41和授权保护；TCONF-164-03五项、70前端及当前源S2复验通过。App/UI/平台与完整G3仍NOT RUN，真实模型新增0，旧账本/预占保留。最新见[26](26-s3-plan-retirement.md)及feature.yaml；下面旧阶段结论按原来源保留。

> 当前（2026-10-25，S2时序与真实本机边界）：TCONF-164-02五组组合已在Host 57c29ea/Desktop ddc840f干净来源通过；正常Host/Native重开与取消零POST验证完成。平台/UI仍延期、完整S2 G3未过，下一步可离线推进S3。真实模型新增0；详见[25](25-s2-conformance-and-native-boundary.md)及feature.yaml，下面保留阶段历史。

> 当前（2026-10-25，Native恢复接线）：Desktop f341636已完成SQL39新意图、只读查询和显式恢复，定向检查通过；旧pending不回填，已发/未知且404不重发。App未重建，平台UI继续延期。完整S2还缺never-sent证明与取消，G3/final未通过。最新见[23](23-native-model-recovery.md)和feature.yaml，较早记录按原来源保留。

> 当前（2026-10-25，UI延期/S2基础）：Owner允许锁屏所需步骤延期并先推进离线实施，UI仍NOT RUN。Host Store11、v2原回执/显式恢复及带数据SQL升级验证已本地固化；Native恢复接线/never-sent取消、S3/S4与完整G3/final尚未完成。真实模型新增0。最新权威见[22](22-ui-deferral-and-s2-foundation.md)和feature.yaml；下方旧阶段记录仅按其原来源和时间解释。

> 当前S1（2026-10-25）：源实现、local/boundary及canonical构建已完成；本机新Kimi正控通过，暂停/MiniMax/重开及最终清理因Mac锁屏未完成，S1 G3不放行。新增真实模型HTTP为0，旧账本逐字保持。最新来源、未执行项和续办见[21](21-s1-implementation.md)。下方20及更早阶段结论按原来源和时间保留。

## 历史有效状态（2026-10-25，30元单次续验）

| 项目 | 当前结论 |
|---|---|
| 来源与工程门禁 | Runtime r2 / Contracts / Host固定；Desktop40908c7独立固化；G2A及当前Harness PASS |
| 真实G2V | 本次新增唯一HTTP200，正确答复42、usage/保存/重开/无补发/正常清理及组合oracle PASS；r1 FAIL保留 |
| 预算与请求 | 累计30元；仅新增1HTTP已耗尽。旧预占14.188544元＋本次保守0.139590元＝14.328134元；不再新增请求 |
| 已通过历史 | r2 canonical实际App本机合成答复、保存、重开、正常退出；不等于真实模型通过 |
| 尚未完成 | S1—S4、TCONF-164-01—04及三个final；不放行日常库迁移或发布 |
| Git | 仅FEAT-164本地提交已获授权，不推送；保留其它需求改动 |

本轮权威为[20 单次续验](20-budget-resume-and-g2v.md)、feature.yaml和追加后的真实账本。13—19按各自时间与来源保留历史语义。TCONF-164-01—04仍为计划目标，执行前核实selector存在且测试命中数非零。

## 分层验证

| 层级 | 覆盖 | 所需证据 |
|---|---|---|
| Contract | 活动/历史身份、旧header与新执行、封闭enum、market/expert/plan引用、unknown/retired区分、来源锁 | source-first生成diff、lint、逐支持baseline breaking、方向conformance |
| 普通单元 | 配置前身/双文件过渡、CAS/revision、lost receipt状态机、never-sent证明、grant领域更新、claim/send准入 | 审查过的安全allowlist与非零执行数，逐AC结果 |
| 私有迁移 | 旧基础/29/37库正常前向、新库重开；原列/主键/外键/原payload/digest保留；兼容回退reader | 合成数据库正常事务；不复制用户私密库为fixture，不破坏权限 |
| 实际Runtime本机协议 | 新候选start/resume/turn、SSE/function/web sources/图片、previous_model压缩、启用子代理/Guardian路由 | canonical binary和普通本机HTTP server；真实请求解析，明确非供应商资格 |
| G2V | 最小真实App→Host→Runtime→新模型→返回→保存/重开链 | qualified H-F164-LOCAL、精确refs/平台及批准的合成数据真实调用 |
| final core | AC001—009；主聊/标题/专家/草案/计划/工具/图片/搜索/旧历史 | 同一source组合；完整request-call-result关联及正常恢复 |
| final visual | AC010；长名称/焦点/键盘/亮暗/最小窗口/错误与重试 | 独立可访问性/视觉结果，不借API PASS |
| final teardown | AC004/005/010；正常取消、退出/重开、无在途/重复派发 | 正常EOF/应用退出/实际状态；不能以强杀获得结果 |

## 正常状态案例

1. 空库/新聊天，新身份精确；MiniMax往返保持provider匹配。
2. 已知旧catalog/TOML及可达混合组合正常升级；以普通内存值测试未知配置拒绝，不篡改用户配置造故障。
3. 旧idle会话、已完成回执、已知退役身份、pending/uncertain、missing但不能证明未发分别处理。
4. 通过纯函数/正常协议driver传入“Runtime已回执但Host未提交”等状态，不靠杀进程模拟。
5. 定时plan的paused/enabled、future slot、已占run snapshot、授权digest和旧revision保持/失效符合领域事务。
6. worker启动前/claim前/send前的准入与普通恢复查询并存，退役操作不被反复增attempt。
7. 标题与切换并发的正常顺序、Guardian在auto模式下的模型路由、整个已启用代理图正常收敛。
8. 预算内文本/图片/合法工具/搜索、流式done及completed/failed/incomplete如实显示；无攻击载荷。

## Harness资格和安全替代

H-F164-LOCAL默认禁用；production_bootstrap表示产品canonical启动链，不是生产网络或新权限。需验证product_failure/harness_failure/platform_failure/gate_failure四类结果、正控、正常超时及cleanup、无正文判定。使用普通无副作用返回值、纯状态输入和正常取消验证分类；禁止强杀、二进制替身、权限破坏、危险fixture。不能安全验证的项目列NOT RUN/原因/影响，阻断对应Gate，不伪造例外批准。

## 真实费用与副作用

2026-10-26当前：schema3本轮3/3及累计5/5均已用完，累计保守上界14.679001元；没有新增HTTP授权。原schema2与预占保持，下一次付费调用需新明确授权且不得重置账本。下段保留2026-10-25旧schema2的历史范围。

当时批准累计30元、总模型HTTP最多2次（已有1次＋只新增1次），覆盖标题、Guardian、压缩、子代理、工具后续及重试；任何额外HTTP均拒绝。此次只发1个普通文本回合，输出上限8192、原生搜索移除，不使用图片/工具。搜索与图片授权仍保留，但本次不消耗；不得以剩余资金增加调用。旧unknown预占不返还，失败即停。账户资格/余额未知，不自动查账户或充值，不借前序Feature余额。

使用实际预算计量器须先审查其旧model白名单和是否注入max_output_tokens；原始产品请求与预算覆盖测试分开。缺用量按未知，不能按0计；没有cache_write_tokens时不宣称精确费用。失败不自动加额度或更改max档。

## 验收解释

通过阈值是AC全部可判定满足、三个final verdict分别PASS且refs fresh、没有退役请求/历史错写/重复执行/秘密泄露。模型质量仅对获批任务记录结果，不能预先说升级解决FEAT-163。未启用能力不为验收启用，其禁用事实要由effective配置证明。所有相同失败累计三次进入RCA，原记录保留。

## S4g 旧草案状态续办（2026-10-25）

本轮限定验证2项Native状态、1项原writer回归、32前端、lint/fmt/lib Clippy/build/docs及当前App亮暗1180×760。完整通用generate失败/RCA保留，未跑攻击/故障注入和真实模型。见33与s4g证据。

## S4h 生成入口与计划验收（2026-10-25）

本轮19项生成、6项配置测试、S3五项、18前端、当前ordinary App计划审阅/单次授权/重开通过；1次模型loopback，真实0。旧K3产品UI与完整恢复取消/媒体仍单列未验，详见34。

## S4M正常关闭候选验证（待实施）

40号追加四池、日志clone/queue排空、正常stdio等待及same-source重开验证；本轮仅未修改r4的一次零回合EOF和4个只读integrity_check。不得把S4M审计完成改成teardown PASS；真实HTTP授权仍0。
