# FEAT-164 S2 派发证明与未发送取消

Owner要求审计现有完成与剩余步骤后执行下一步。延续只本地提交、不推送、保留已有工作区/账本/预占、真实模型HTTP新增0及锁屏UI延期；不覆盖活跃S1 App，不打开日常数据库。

`contract-impact = semantic`，整体需求仍breaking。新增Native私有前向SQL40和本地取消IPC，沿用当前scope/取消权限；Host/Runtime公共wire不变，既有native LocalSubmissionView已包含cancelled。旧SQL、模型operation、payload/profile/digest不回写；旧无证明记录不自动标never-sent。

审计：普通claim/retry计数可重置，market/expert走独立grant/submit路径；普通new-chat还含public-task/create-session。证明必须与新接受事务一起保存，领取与最终发送分别校验，跨重开保留单调claim/attempt事实。普通、市场和专家都必须纳入；scheduled/draft沿原独立派发证明，不将本批取消套用过去。

实施顺序：私有证明/取消回执表 → 新提交冻结原身份与内容摘要 → claim前退役/证明检查 → public/create/turn及market/expert grant/submit前持久尝试边界 → 无任何尝试且无原生执行绑定时的原子取消 → 只读状态与显式取消UI → 正常临时存储/本机HTTP/单调性与迟到处理验证。不会用404/empty/queued/attempt_count=0单独判断未发；取消不调用模型、不删除chat、不生成Runtime终态。

本轮源基线见evidence/s2-delivery-start-baseline.json。S2完整G3、旧库激活、S3计划领域与S4全调用面、实际App/UI仍按证据推进，不把离线工程子集冒充平台通过。

## 实施结果

Desktop本地提交 `2a746c1b39bf1f55f6b317ab570bf93af81ad5dc`，23个FEAT-164专属文件；Host `3c5289854d88ca6ed69b17bd806fca2efc0bbbcd`、Contracts `f2819c66a2368aaff37216a46c48d5cd81df1747`、Runtime `074417e5e2f5f55704ea5e1777e7a22d514076b4`不变。资格工作树先实现，原工作区只应用专属patch；两个索引的tree一致，并在临时副本逆向应用patch恢复每个原文件字节。见[s2-delivery-isolation](evidence/s2-delivery-isolation.json)。无推送/新分支/tag/发布。

- 新SQL40记录普通/市场/专家的原session、逻辑turn operation、create别名、profile/revision、原消息及payload/snapshot摘要、初始/正常确认的Host-thread绑定。与新接受事务一起保存，不回填旧记录；claim_count和public/create/turn尝试计数独立于可重置的旧outbox计数。
- 普通claim及耗尽处理先过滤退役/暂停身份与缺失证明；最终Host HTTP还有原profile、path、operation及生命周期检查。权限回合按既有wire读取`turn.operation_id`。正常创建回执才能安装首轮Host/thread绑定。市场/专家在自己的admission锁中记录claim、public、grant和submit边界；已尝试回执查询仍沿原只读路径。
- 任一发送/注册尝试都保守阻止取消，不用400/404/空结果推导未发。turn实际发送边界最多记录一次；迟到重试无法重新领取/提交。计划与草案保留原专属证明，不套用本批取消。
- 新私有读取命令`chat_delivery_state_v1`和显式命令`chat_cancel_unsent_delivery_v1`复用当前scope、ReadSessions/InterruptTurn权限；异步与DB执行前复核。只有新证明完整、无尝试/Runtime绑定/原生事件且本地仍queued时可取消。回执持久化、重复返回原回执；取消不删除消息/聊天、不修改原模型或payload、不创建Runtime终态，仅更新本地submission_status并关闭原投递占用。
- 已有会话在此类取消后可接受下一次显式提交/模型选择。未创建远端会话的新任务取消后保留历史，不伪造Host绑定或自动新建任务。原无证明请求继续unclassified/阻断。
- UI只显示当前聊天的原生判定；刷新只读，取消必须点击且有原权限。不可判定时无取消按钮；权限不足、读取失败、取消结果待核实、迟到响应/导航隔离均有处理，沿用现有设计token。

## 验证与审计发现

新增12项Rust测试、暂停Kimi专项1项、前序候选10项及默认reader5项通过。覆盖普通临时SQLCipher正常重开、原消息/摘要保持、缺失证明不补录、claim后取消与send后拒绝取消、旧计数重置不能抹除尝试、下一显式操作、市场/专家独立证明、正常会话绑定、两类turn请求形状。实际本机HostBridge测试中，取消请求的POST计数为0、正控为1；未访问外部模型。前端模型+投递22项通过，含取消权限、未知值、回执关联、导航和失败后不自动重试。

`cargo fmt --check`、候选/default产品lib+bins Clippy、`pnpm lint`、候选前端build和精确来源检查通过。前端build仍有既有大chunk警告；不是App打包或视觉验收。证据/命令见[s2-delivery-verification](evidence/s2-delivery-verification.json)。

扩大ChatPage回归结果为94通过、1失败、2既有skip；失败是空reasoning项目期待“正在思考”，实际为“正在等待模型的后续输出”。在未改的f341636源码及相同已安装测试运行器上复现相同断言和输出，因此保留独立缺陷，不混入本批修复。基线诊断首次pnpm自动依赖检查/安装受ignored-build策略阻止，未绕过；随后直接调用已安装测试运行器，补全基线contracts/scripts后完成复现。源文件/lockfile/所有已登记工作区文件保留性另有逐字核验，不将该首次环境失败写为测试结果。

本批审计修复了SQL5失败状态必须含合法诊断码的取消事务兼容问题，以及permission-turn嵌套operation的最终派发校验。初次失败日志和测试导入修正均保留；未关闭规则或伪造全套绿色。

## 边界与下一步

完整S2 local/boundary/required vertical、TCONF-164-02、G3和final保持未通过。本轮未执行新canonical App构建/启动、亮暗主题/1180×760、旧隔离库和日常库激活、真实Host+Native+App完整链、平台恢复/清理。原全targets Clippy source_reader_tests位置问题及独立旧Skill pin问题未扩散修复；禁止的故障/攻击fixture仍不执行。正常临时数据库和localhost响应不替代平台资格。

可继续离线工作：先补齐S2完整TCONF矩阵和普通/市场/专家原回执的真实Host+Native无模型联调，再推进S3计划退役/授权迁移/claim-send与S4全调用面。需要UI的部分继续延期；用户回到电脑后正常退出旧S1 App，才能用新来源canonical构建并验收。当前活跃App仍是S1来源，不能把本批源码验收结果套到它上面。

新增真实模型HTTP为0；旧2次请求、14.188544元未知预占及14.328134元累计保守上界不变，30元额度不增加耗尽的HTTP次数。不启动计量器，不继承FEAT-162/163额度。原账本/快照、42个活跃App文件和已有工作区改动的核验见[s2-delivery-preservation-audit](evidence/s2-delivery-preservation-audit.json)。

## 治理复核

包strict、claims审计、元仓lint及53项治理测试通过；S2 G3检查按现有S1/S2平台、freshness、完整TCONF缺口返回1，保持拒绝，没有提高状态或关闭门禁。见[s2-delivery-governance-verification](evidence/s2-delivery-governance-verification.json)。
