# FEAT-164 当前验收与来源矩阵

## 当前D1实施结果（2026-10-27）

当前权威为[60 D1完成与离线资格](60-d1-daily-binding-and-offline-qualification.md)。59号D1已获批并完成六文件Desktop修正、安全测试和新canonical prepare-only/同回执复核；Host/Runtime采用已批准原Home绑定，daily不再隐式workflow-up。真实日常绑定未生成、D2—D5未执行、模型HTTP新增0、Runtime核心/补丁未改。原CUTOVER-01/03已离线修复，日常现场/启动资格仍无授权，G4不自动晋升。58接受的never-sent替代保留，完整App正向取消仍NOT RUN。

下方59及更早“尚未实施D1/原入口缺陷”按当时来源解释，不再作为当前D1未完成项。下一步仅在批准D2后进行完整冷备份和副本只读预检，不顺带迁移或启动。

## 当前日常切换边界（2026-10-27，S4AF）

以[59 日常切换方案](59-daily-cutover-minimal-plan-and-authorization.md)为当前部署权威。源码复审发现daily launcher将Host/Runtime Home改至候选新目录、与原Native日常库缺连续性；正常启动还可能隐式workflow迁移及恢复自动计划。日常activation为NO_GO，当前G4重新pending，先提限定部署入口修正及离线资格，尚未获准实施。58的已接受本地S1—S4/final证据与never-sent替代保持，完整App正向取消原执行仍NOT RUN；不是重新跑失败或取消Owner接受。

本轮仅方案和治理，无产品/Runtime改动，无日常数据访问/备份/预检/迁移/启动，无模型调用。阶段顺序为D1入口修正→D2完整冷备份与副本只读预检→D3一次Native维护→D4首次受限启动及退出核对→D5确认日常启用；D1—D5均未自动授权，具体边界见59。以下早期状态按各自时点解释。

2026-10-27，当前权威为[58](58-owner-accepted-substitute-and-final-closure.md)。目标仍是所有活动调用面使用kimi-k3.1-pro，原历史/operation/授权与MiniMax保持。58已接受本地适用验收保持；59新发现日常Home连续性缺口，当前G4重新pending、日常NO_GO，feature保持active。

## 当前源码和制品

| 对象 | 固定来源 |
|---|---|
| Desktop | ea8763dfc40466e9b808a1b39afad71dbff1ac56；相对c98仅测试修改 |
| Host / Contracts | 4f966e8ea810d5b094d0b797d291955d6c774844 / c5d138374c102f1a8a11e328a869ec8f91724efd |
| Runtime | 11fd4504c28afd0f65c6f5f62a6b5328dd437f5a；r5 SHA283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e |
| Connectors / Skills | cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9 / 595c927ae101d3d31c234f60565041eee0864680 |
| 本轮原隔离App | ea8763dfc40466e9b808a1b39afad71dbff1ac56；SHA4b0ec55e6903bc6aad790a4715d485456ebf0241d10ff6c99e51d67c6aa65e39；119文件；原R1身份，正常退出 |
| 新验证提交 | Desktop4e1f1f980d148a6b46e21e68eb508caa4da5dae4；仅Native/consumer测试及说明3文件，产品与ea相同 |
| 新日常候选 | ea源码；SHAc29f7e07942038d4c3849ef3a711ed4b501d17daab1478329ba5de6b6321a4d0；119文件；prepare-only及只读回执通过，未启动 |

56已核对501份旧证据哈希一致、310个业务实现文件与9f资格源相同。51日常维护入口新增分支不声称全文件相等，由其自然SQL四组合与本轮回归支持；54来源过滤变化由专属来源证据支持。原主工作区dirty与旧制品保留，不是部署来源。

## AC判定与交付边界

以下PASS限已接受的本地实现与验证，不能推导为日常部署已经执行。

| AC | 判定 | 有效证据及边界 |
|---|---|---|
| 001 活动目录/参数 | PASS | S1/49/56/57，K31/MiniMax与有效身份精确；日常未启用 |
| 002 受管配置 | PASS | S1/51/56，已知前身准入、未知拒绝；日常现场未预检 |
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
| G5/G6 | pending | local exposure，无生产/发布资格或授权 |
| 日常候选 | prepare-only PASS | ea制品c29f7e0未启动；日常库未打开/迁移 |

**完整App/WebView正向never-sent取消：NOT RUN。** 正常Native持久正例与生产消费链实际结果重放为ACCEPTED_SAFE_LAYERED_SUBSTITUTE，非完整App执行。原自然unknown继续安全拒绝，既有占用grant不清空。亮暗/键盘/最小窗口及搜索答案质量永久OWNER_EXCLUDED。

## 保护与下一步

本轮587个历史证据引用、12份私有事实、六来源及三套119文件制品核验一致。全部12441保护文件、500份既有dirty和7账本/快照核对，混合memory仅本轮增量。真实HTTP累计13，本轮0；45元cap、29.740299保守累计、两份14.188544预占保持。服务停止，无交接待答。

不再补试已接受项或重复模型回合。60已完成D1部署绑定/ready-only修正及离线资格；下一步仅在获批后进入D2完整备份/预检，D3维护、D4启动、D5日常启用仍分阶段批准。日常候选prepare-only不代表可直接启动；无Runtime核心/补丁新增范围。仅本地提交、不推送。
