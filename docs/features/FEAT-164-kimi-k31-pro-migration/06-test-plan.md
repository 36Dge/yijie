# FEAT-164 测试与证据计划

> 当前S1（2026-10-25）：源实现、local/boundary及canonical构建已完成；本机新Kimi正控通过，暂停/MiniMax/重开及最终清理因Mac锁屏未完成，S1 G3不放行。新增真实模型HTTP为0，旧账本逐字保持。最新来源、未执行项和续办见[21](21-s1-implementation.md)。下方20及更早阶段结论按原来源和时间保留。

## 当前有效状态（2026-10-25，30元单次续验）

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

当前批准累计30元、总模型HTTP最多2次（已有1次＋只新增1次），覆盖标题、Guardian、压缩、子代理、工具后续及重试；任何额外HTTP均拒绝。此次只发1个普通文本回合，输出上限8192、原生搜索移除，不使用图片/工具。搜索与图片授权仍保留，但本次不消耗；不得以剩余资金增加调用。旧unknown预占不返还，失败即停。账户资格/余额未知，不自动查账户或充值，不借前序Feature余额。

使用实际预算计量器须先审查其旧model白名单和是否注入max_output_tokens；原始产品请求与预算覆盖测试分开。缺用量按未知，不能按0计；没有cache_write_tokens时不宣称精确费用。失败不自动加额度或更改max档。

## 验收解释

通过阈值是AC全部可判定满足、三个final verdict分别PASS且refs fresh、没有退役请求/历史错写/重复执行/秘密泄露。模型质量仅对获批任务记录结果，不能预先说升级解决FEAT-163。未启用能力不为验收启用，其禁用事实要由effective配置证明。所有相同失败累计三次进入RCA，原记录保留。
