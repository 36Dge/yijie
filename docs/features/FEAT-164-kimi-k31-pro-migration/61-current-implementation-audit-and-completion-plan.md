# FEAT-164 当前实现复审与最短收尾方案

2026-10-27。本轮按Owner要求审计现有实现、未完成项并给出方案；只修改治理文档，不实施产品修复、不访问日常数据、不启动或探测服务、不新增真实或本机模型HTTP。原工作区、账本与预占保留，仅本地提交。本文更新当前摘要，不改写59/60及更早报告的历史结果。

**结论：K3→K3.1 Pro的核心实现与已接受本地S1—S4验收已经收口；尚未完成的是日常部署资格、长期日常入口与正式交付治理。最优下一步是一次有限的离线补证和部署工具准备，再按D2→D3→D4→D5推进。当前没有证据要求新增Runtime核心/补丁修改，也不需要重跑模型功能或已排除项目。**

## 一、当前事实及审计范围

核对60号58份证据、六个来源、119个新daily包内文件和1207个Desktop构建输入，均未漂移；结果为`PASS_READONLY_BINDING`，不是本轮重新执行了产品测试或App验收。

| 对象 | 当前来源/资格 |
|---|---|
| Desktop | `b789d5c8147fde9890d49b67c6ecb191473793db`；`feat164-d1-candidate-20261027/yijie-desktop`；干净 |
| Host / Contracts | `4f966e8ea810d5b094d0b797d291955d6c774844` / `c5d138374c102f1a8a11e328a869ec8f91724efd`；干净 |
| Runtime / Connectors / Skills | `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a` / `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` / `595c927ae101d3d31c234f60565041eee0864680`；干净 |
| 当前daily App | SHA `944b6b238b7f7b0f36cfab2be358d83b9be044587cc37a3ea5a161fc68b40015`；119文件；identity `com.yijie.ai`；仅prepare-only |
| receipt | SHA `490e35d8e5214d1dddd84def050edf093cdd9f2f7aa9edd5fb83076ebb3c9fc3`；策略`feat164-daily-existing-homes-v1` |
| r5 binary | SHA `283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`；保持原资格，不重新构建 |

D1源码复审覆盖绑定校验→原Home交接→canonical receipt→workflow只读ready→维护/正常启动分支。三个并行Codex审查分别复核实现、数据依赖和需求/治理；这是工程审查，不冒称独立人工批准。本轮未发现可直接证明的新D1产品缺陷。真实日常路径、schema、未决状态、自动计划及workflow状态仍为UNKNOWN，不是已经检查失败。

旧`ea8763d/c29f7e0`保留为历史日常prepare-only来源，不能再称当前候选。原R1 App `4b0ec55`、资格App `179dbd1`以及取消正例测试提交`4e1f1f9`各自证据用途保留；不把旧App验收时间刷新成b789的新执行。旧K3字符串在历史reader/契约及明确旧模式中的存在不等于活动K31调用回退，不能用全仓字符串清零替代兼容迁移。

## 二、已完成与实际剩余

| 范围 | 判定 | 后续处理 |
|---|---|---|
| 活动目录/参数、受管配置、历史SQL兼容、原thread显式迁移/恢复/取消保护、旧计划退役/重审/新授权 | 已接受本地PASS，AC-001—006 | 保留原证据，不重复造旧样本 |
| 普通/专家/媒体/辅助/子代理/压缩接线，r5真实文本、图片、工具、原生sources及正常退出 | 已接受本地PASS，AC-007—010、S1—S4 G3及适用三final | 不新增真实调用；新部署只验证受到部署变化影响的链路 |
| never-sent完整App正向取消 | 原执行NOT RUN；Owner已接受安全分层替代 | 不补造故障，不再作为缺口；原自然unknown安全拒绝保持 |
| 搜索答案正确性、亮暗/键盘/最小窗口专项 | OWNER_EXCLUDED | 永久移出本需求，不写PASS或延期 |
| D1 Home绑定、只读ready、prepare-only | PASS_OFFLINE | 补一个正向组合证据缺口，见下节 |
| 日常备份/预检、Native维护、首次App写入与启用 | D2—D5未执行且未授权 | 依具体现场结果逐阶段推进 |
| 长期日常入口、G4/G5/G6最终交付 | 尚未完成 | 区分受控验收、正常使用与发布，不以离线PASS换算启用 |

## 三、本轮发现与最小处理

### F61-01：D1尚缺真实绑定加载的正向组合验证（P2，验证缺口）

当前测试验证了纯`validate_binding`、模拟正常workflow状态、无授权入口早拒绝及源码接线，但未完整覆盖`load_binding`读取私有文件→receipt/helper SHA→阶段校验→既有两Home返回。依据Desktop `scripts/run-local-demo-fast.test.mjs:443`及`feat164-daily-deployment.py:112`。现有61项PASS不作废，也不把未执行链路宣称已通过。

最小补证：仅在正常新建合成目录放普通私有binding/receipt和两Home，调用当前真实helper函数，分别验证D3、D4暂停、D5明确暂停值；核对Home返回、原记录字节、回执关联、错误阶段/缺字段等普通输入拒绝。Native固定路径仅作字符串比较，不打开；不改HOME、不替换运行时、不伪造canonical App资格、不调用workflow。测试文件和说明为首选改动范围；若发现产品问题，先给确切差异，不扩大Runtime。

### F61-02：D5目前是短时受控入口，尚非长期日常使用入口（P2，交付方案缺口）

helper `89—98`行对D5同样强制24小时内有效记录、`model_http_limit=0`和`no_dispatchable_work=true`，launcher每次非prepare启动都要求绑定。这些条件正确保护受控验证，但次日重启及用户正常授权的计划运行不能自然套用该记录。60只证明D1离线资格，未承诺上述长期语义已实现。

推荐最小设计：**稳定数据/制品绑定与一次性切换批准分离**。D3/D4保持短时逐次准入；完成D4后，D5明确批准的激活记录绑定原Home、identity、精确receipt及D4结果，正常重启不要求每天重建迁移批准。普通运行仍沿产品既有用户意图、模型暂停和计划grant检查；旧计划不因激活而自动恢复。候选、Home、policy或receipt变化仍拒绝并重新审阅。仅激活/维护验收维持0模型调用；后续正常使用的授权与该次零调用验收不能混成一个永久字段。

备选是长期每次重新申请短时D5记录：改动较少，但不能满足稳定日常交付；直接删除过期/零派发检查则混淆首次切换与普通启动，不采用。推荐方案预计仍限Desktop部署helper/launcher/receipt、对应测试、部署说明与SECURITY，不改Native schema、Host业务或Runtime。**这是待具体设计确认的私有部署semantic变更，不是本轮已批准或已实现范围**；不趁补测试放宽现有门禁。新策略若改变构建输入，才生成新canonical候选并重验相关部署链。

### F61-03：G5/G6的local语义与机器规则冲突（治理阻塞）

当前为schema v3、`production_hardened + local`。Handbook第9行称exposure不改变Profile；Accepted ADR-0017保留重要持久数据的G0—G6。但`validate-feature-package.mjs:1627`对v3 G5/G6强制`exposure: public`。这是规则冲突，不能将私人本地应用改标public、降为demo_fast，或直接宣称G6。

推荐单独提出共享治理最小修正：保持全部production_hardened实质检查，明确本地重要持久数据部署的G5/G6适用范围；public额外暴露要求仍按public判定。对应validator、`tests/codex-feature-delivery.test.mjs`及Handbook/适用ADR说明需一起审阅；任何改变Accepted ADR或全局门禁须先获确认。本轮只登记冲突，不修改这些全局文件。D2备份预检可先做；正式D5启用前须消除治理冲突。

### F61-04：D2工具尚未资格，需把依赖检查前移（执行准备缺口）

现有旧reader绑定R1审计目录，不能直接套用日常库；Native维护同时包含快照、预检及原库迁移，也不能当只读reader。先准备只接受明确inspection副本根的SQLCipher/SQLite/bbolt只读检查，使用合成/既有已授权样例资格，任何查询失败不得返回零计数。

D2建议同时包含既有workflow只读资格：固定源码SHA、读取私有state及K_NA/K_AC、Docker inspect、既有本机鉴权GET，提前发现D3之后不能启动的依赖。该范围须在D2授权明确列出；无`up/status/record`、轮换、启停或迁移。当前helper只接受D3/D4/D5，不能伪造D4批准借用；应另备受审只读入口复用固定源码链，未授权前只审代码/纯状态。

Host Artifact spool以进程随机密钥管理，正常启动/关闭会清理并重建/删除（`internal/artifact/store.go:149/339`）。这是既有正常生命周期；D2只能完整备份正常退出后仍存在的内容，不能承诺恢复所有临时spool。D4授权和后态差异白名单应明确此项；长期附件/Artifact以Native实际持久事实为准。

### F61-05：当前摘要存在来源漂移（文档问题，本轮修正）

验收矩阵顶部指向60，下表仍将ea/c29称当前；需求正文仍称Home修正未完成。本轮统一当前来源到b789/944b6/490e，保留58—60原报告、原执行时间和各自限制。避免把历史P1当作仍未修复，或误用旧daily制品。

## 四、推荐实施顺序及明确退出条件

| 顺序 | 要做的最小工作 | 完成/停止边界 |
|---|---|---|
| P0 离线收尾准备 | 补F61-01正向组合；准备D2备份/inspection reader与脱敏清单；把F61-02长期入口和F61-03治理修正形成精确可审差异 | 先完成不接触日常数据的工具资格；不重复已通过S1—S4、不改Runtime、不新模型调用。D5权限/全局规则仍先设计确认 |
| D2 完整冷备份与只读预检 | 获明确授权后识别真实原入口/数据根，正常退出、核验无句柄及相同实例锁；全App数据树＋原Host/Runtime＋必要秘密/外置自有资源冷备份；封存后另复制inspection；核对三存储连续性、已资格schema、unknown/outbox/grant/reservation及所有模型的future/pending工作；同时检查获准workflow依赖 | 只形成实际清单、hash、可迁移/NO-GO及拟绑定，不执行维护/启动/改计划。未知schema、查询失败、来源变化、锁不空、阻断迁移的占用，以及影响准入/三存储一致性/自动派发判定的未知项均停止，不清零；不要求消除已接受的历史unknown |
| D3 一次Native受控维护 | D2具体结果获接受后，按对应候选receipt/目标/备份批准一次canonical维护；检查正式迁移、旧K3计划退役及允许差异 | 成功也停；Host/Runtime未启动。后态副本保留原operation/payload/grant/run；不手工checkpoint、不删截WAL |
| D4 首次受限启动与正常退出 | 独立批准Host/Runtime首次写入、受管文件升级和临时spool正常清理；Kimi暂停、全模型无可派发工作、workflow已ready；查看模型目录、旧历史、计划关闭状态，正常退出并核对数据/句柄/清理 | 0模型HTTP，不发送、不生成标题、不恢复unknown、不切旧thread、不新授权或执行workflow；实际退出证据补齐新daily链，评审G4 |
| D5 日常启用与交付 | 长期入口设计及治理冲突已解决，D4证据经G4评审后，先完成获批local口径的G5和Owner启用批准，再激活合格canonical入口；是否解除Kimi暂停须明确，保留旧App与完整备份 | 启用本身不发验收消息、不恢复旧计划grant；不覆盖签名App、不推送。按约定观察/核验后才评审G6，D5不自动等于G6。后续正常使用与本次0调用验收分别记录 |

P0可并行进行测试审查、reader设计、治理设计，产品来源改变后只重新验证受影响部分；不要建无关新平台或无限扩展验证框架。本轮所有P0代码/工具工作均未执行，下一轮先明确实施清单；工具准备不包含D2真实数据权限。D2/D3/D4/D5是数据操作阶段，不是Handbook的demo_fast D门禁。受控D2—D4资格与正式日常启用分开，避免“G4先过才准取得D4证据、又要D4证据才过G4”的循环；这不是绕过G4/G5直接激活。

执行前必须重现canonical receipt所绑定的编译环境和精确来源；不能凭一个最简启动命令推定receipt有效。实际原Home布局、服务状态和数据量未知，本轮不承诺固定时长或一次成功。若workflow未ready，保持日常App关闭，先给服务/数据变更具体方案，不能自动`workflow-up`。

任何阶段无法正常退出就停；锁屏时不越过依赖UI的前置。维护后失败保留新兼容reader且Kimi暂停或保持关闭；旧writer回写、降schema、覆盖原库均不是默认回退。若必须恢复备份，另行审阅期间新增数据损失与授权。不释放旧预占、不重发unknown、不把无回执猜为never-sent。

## 五、本轮证据、授权与完成口径

本轮`contract-impact=none`：只读审计与文档，没有跨进程、跨仓或持久化行为变化；整需求breaking、D1私有部署semantic保持。未来F61-02按semantic单独确认，F61-03属全局治理决策；本轮不授权二者。

当前仍为D1 PASS_OFFLINE、G4/G5/G6 pending、D2—D5 NOT_AUTHORIZED。本轮不改变Owner已接受替代/排除范围，不要求补跑完整App never-sent或搜索质量。真正交付完成应同时具备：核心模型功能已接受、日常三存储连续且已安全切换、长期入口可按批准正常使用、适用治理与回退记录完成；仅增加报告不能替代这些实际结果。

来源核验见`evidence/final-plan-current-binding.json`，审计发现与只读源码SHA见`evidence/final-plan-findings.json`。后续元仓检查和保护核验见`evidence/final-plan-checks.json`及`evidence/final-plan-preservation.json`。没有重新测试产品、探测真实日常状态、启动服务或模型调用。旧累计13次HTTP、45元上限、29.740299保守累计及两份14.188544预占保持。

元仓audit-claims、strict、S4 G3、lint、53/53测试及7份Shell语法通过；未重跑已知pending的G4，也未修改全局门禁。提交前500份原dirty、混合memory原内容、7账本及原八仓HEAD/分支/远端保护核验通过。完整日志保存在`feat164-final-plan-audit-20261027`；这些结果仅验证本轮治理文档与工作区保护。
