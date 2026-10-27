# FEAT-164 当前验收与来源矩阵

2026-10-27。当前权威[63](63-pre-d3-blockers-fixed-and-ready.md)：62号三项技术阻塞已解除，D3_PRECONDITIONS_READY。历史消费/原授权保持，真实Rust对SQL37副本准入通过；第三旧catalog精确兼容且v1/trust不改；workflow正常恢复后六项健康且鉴权ready。原17,389文件与D2封存一致，原daily未迁移/启动；G4/G5/G6仍pending。长期D5及local治理口径仍为后续项。

## 当前源码和制品

| 对象 | 固定来源与作用 |
|---|---|
| 当前App的Desktop来源 | 841f7c71ed3549fe02a70cff608cbbae713d6808；63号干净候选，基于b54/b789 |
| Host / Contracts | a3d8767add3855a28c18adbbd51251fae3520ac0 / c5d138374c102f1a8a11e328a869ec8f91724efd |
| Runtime | 11fd4504c28afd0f65c6f5f62a6b5328dd437f5a；r5 SHA283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e |
| Connectors / Skills | cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9 / 595c927ae101d3d31c234f60565041eee0864680 |
| 当前日常候选 | 841源码；SHA4f7adcadc59db4a6e4cf23e700ebab5858b6ae9d953cd7401780d5778cab0f42；119文件；仅prepare-only |
| 当前receipt | SHA0e6fe8191ffc027d4f1efedf14f7e8562ee1d876068aafa7386410202a2878a7；1216构建源码输入；策略feat164-daily-existing-homes-v1 |
| 历史隔离App | ea源码；SHA4b0ec55e6903bc6aad790a4715d485456ebf0241d10ff6c99e51d67c6aa65e39；原R1已接受证据，非b789实际App运行 |
| 历史取消测试来源 | Desktop4e1f1f980d148a6b46e21e68eb508caa4da5dae4；仅3测试/说明文件，产品与ea相同 |
| 历史日常prepare-only | ea源码；SHAc29f7e07942038d4c3849ef3a711ed4b501d17daab1478329ba5de6b6321a4d0；保留，不再称当前候选 |

61只读核验60的58证据、六源、119包内文件及1207源码输入一致，没有刷新历史执行时间。D1只改六个部署/测试/说明文件；原Native/renderer/Host/Runtime业务依据60源比较保持。不声称新daily实际已启动，也不使用原dirty工作树作为部署来源。

62号测试/工具来源b54及60号b789制品均保留为历史资格。63号新Native私有SQL与Host前身按定向证据资格；不刷新旧完整App执行时间。原Runtime WAL非零完整保留，不手工checkpoint。

## AC判定与交付边界

以下PASS限已接受的本地实现与验证，不能推导为日常部署已经执行。

| AC | 判定 | 有效证据及边界 |
|---|---|---|
| 001 活动目录/参数 | PASS | S1/49/56/57，K31/MiniMax与有效身份精确；日常未启用 |
| 002 受管配置 | PASS | S1/51/56，已知前身准入、未知拒绝；日常D2已预检，63已补第三精确前身兼容；真实日常尚未激活 |
| 003 SQL兼容 | PASS | 46/51/56自然SQL29/37×隔离/daily四组合；真实日常未打开/迁移 |
| 004 原thread/恢复 | PASS | 46同thread迁移/停止/继续，56边界回归，57自然unknown实际App安全拒绝；原unknown仍不ready |
| 005 退役/取消 | PASS，含已接受替代 | 56准入/未知状态，57正常Native入队/领取/取消/重开及真实结果消费；完整App正向原执行NOT RUN，58 Owner接受 |
| 006 计划/授权 | PASS | 46旧计划退役/重审/新grant，51/56定向回归与实际关闭状态；旧授权不复活 |
| 007 全调用面 | PASS | 48辅助/子代理/压缩，52专家媒体/共存，56当前来源19项和58绑定 |
| 008 响应语义 | PASS | 49真实文本、53图片/工具/搜索传输、54来源显示、55v4测试修复、56历史；搜索答案正确性OWNER_EXCLUDED |
| 009 Key/审批/预算 | PASS | 既有共享Key/逐次授权，刷新/重开不调用，全部旧账本与预占保留；本轮不新增调用 |
| 010 生命周期/状态 | PASS，含已接受替代 | 57自然unknown/草案保护、正常退出WAL0，58取消替代；正常计划/Host时间戳变化如实保留 |

## 三项最终判定与门禁

| 项目 | 当前状态 | 解释 |
|---|---|---|
| core_vertical | PASS | 46—57实际App主路径与跨组件结果；never-sent单项采用Owner接受的替代 |
| accessibility_visual | PASS | 现存业务状态范围；完整App正向取消NOT RUN另列；外观专项已排除 |
| teardown | PASS | 57正常退出/数据库业务事实保护，本轮零启动且文件未改 |
| S1/S2/S3/S4 G3 | PASS（58本地范围） | 来源并集8项及已接受替代保持 |
| 当前G4 | pending | 60已离线修复CUTOVER-01/03；新daily bootstrap尚未实际启动，不从prepare-only自动晋升 |
| G5/G6 | pending | 本地加固交付口径与validator public限制冲突，待确认修正；不改标public造绿 |
| 日常候选 | prepare-only PASS | 当前841制品4f7adca、receipt0e6fe81未启动；日常库未打开/迁移 |

**完整App/WebView正向never-sent取消：NOT RUN。** 正常Native持久正例与生产消费链实际结果重放为ACCEPTED_SAFE_LAYERED_SUBSTITUTE，非完整App执行。原自然unknown继续安全拒绝，既有占用grant不清空。亮暗/键盘/最小窗口及搜索答案质量永久OWNER_EXCLUDED。

## 保护与下一步

63完成后日常原文件和D2 sealed保持，旧账本与两份预占不变，真实模型HTTP新增0。workflow已正常恢复，六项服务保持ready；正常两次principal审计及epoch/凭据轮换如实记录，不能称整个Infra状态未变。未启动daily App。

下一步是单独明确D3一次维护，执行时复核同一新制品、有效数据摘要、正常实例锁/句柄和真实批准绑定；成功也停止做后态核对，再推进D4。D5长期入口与local G5/G6规则仍独立；Owner替代/排除保持，不重跑模型或已排除验收。仅本地提交、不推送。
