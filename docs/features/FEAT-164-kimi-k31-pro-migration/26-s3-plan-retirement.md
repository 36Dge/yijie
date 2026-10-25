# FEAT-164 S3 计划退役与授权保护

2026-10-25，Owner已授权实施S3，仅本地提交、不推送。新增真实模型HTTP为0，30元旧账本、14.188544元未知请求预占与已有工作区均保留；不操作活动S1 App及其数据库。起始状态见evidence/s3-start-baseline.json。

## 实施前审计与设计

S1/S2源实现和TCONF-164-02已完成，但App、旧隔离历史、UI、平台与freshness仍延期，S2整体G3未通过。S3现有计划契约只认识旧K3/MiniMax；worker与scheduled outbox领取/发送路径尚无独立退役守卫。直接改模型列会使读取/重放失败，并错误继承旧授权。

contract-impact=breaking：旧模型执行能力退役，新的持久计划模型值需要版本化consumer。Owner/producer/唯一登记consumer为段成威/Native Desktop/同一候选Desktop；无public或已发布激活。先新增Contracts scheduled-plan-v2源与派生物并本地固化精确commit，再同步Desktop。旧v1源/生成物保持；Execution/Draft公共wire无模型枚举，本批不改。Native私有IPC使用候选v2源投影和同源validator；非候选入口仍消费旧v1。

SQL41只新增私有退役回执。候选开库、worker启动前通过计划领域事务暂停旧K3计划、revision递增、清除authorization_ref/expires和未来尚无run的planned slot。保留profile原值、历史run/grant/snapshot/digest、已占额度和未知派发；回执令重复开库幂等。另在新保存、授权、预备、领取、最终发送处检查模型身份与候选暂停状态，避免异步期间越界。

新模型须用户在计划表单明确选择并保存，再按既有领域操作重新授权。已绑定会话要求当前确认selection一致且无pending；不得替用户切换会话模型。旧无model_profile计划保持MiniMax兼容解释。MiniMax计划不受退役迁移影响。

验证使用正常临时SQLCipher、领域API和本机合成fixture，禁止强杀、权限破坏、可执行程序替换及攻击注入。覆盖已启用/已暂停/有保留run/已删除旧计划、MiniMax、幂等重开、旧回执重放、新模型保存再授权、领取前/发送前屏障和历史事实保全。App/UI/Windows/Linux仍NOT RUN，不把headless结果换算G3。

回滚使用认识SQL41和v2历史的候选reader并暂停Kimi执行；不允许旧SQL40 reader打开新库，不降级删除回执或改历史事实。契约无发布tag，本地commit不冒充生产发布。

## 实际实施与最终验证

Contracts `2dd214d6a702064edae78510c035442854bf9789`（10个新增源/生成/测试文件）先本地固化；Desktop `4d04597cbf40e1aea2c67607c9d441f888223d96`（56文件）按精确commit同步，包含SQL41、领域事务、授权/调度/claim/send保护、候选私有IPC与前端、测试driver。Host57c29ea、Runtime074417e5 r2未改。原工作区按专属补丁应用，逆向补丁逐字还原所有被触及文件的原有改动；两个隔离清单见evidence/s3-yijie-contracts-isolation.json和s3-yijie-desktop-isolation.json。仅本地提交，没有推送、tag或发布。

实现保留MiniMax原有保存/开启语义；模型改变或新K3.1计划保存为paused，独立重新授权。历史缺省profile只按MiniMax解释并在新提交冻结为MiniMax，未把历史字段改成新模型。已删除/已完成旧计划保持终态。旧运行snapshot仍可读取；自动expiry的manual/rerun/automatic三条路径根据原snapshot阻断隐式取消或退款，显式取消保持独立。新发现的扫描批次问题也已修复：暂停Kimi在LIMIT32之前过滤，33个暂停Kimi不会挡住MiniMax。

TCONF-164-03使用实际存在的模块限定入口，组合命令为`node scripts/feat164-s3-conformance.mjs /tmp/feat164-s3-native-final`。driver逐一执行5个`cargo test --offline --locked --lib --features kimi-k31-pro-candidate chat::schedules::model_retirement_tests::<name> -- --exact --nocapture`，每组必须1 passed/0 failed/0 ignored，零命中即失败。核心名字`feat164_plan_retirement_before_dispatch`已从原占位名落地。最终来源树干净，5/5 PASS，见[最终结果](evidence/s3-native-final/result.json)：

- 旧enabled/paused、deleted与MiniMax/缺省计划；领域事务前也拒绝退役身份，重开后revision只增一次；原授权回执变stale、原run回执可重放，新授权/新运行拒绝，旧future slots关闭。
- run/grant/snapshot/digest、outbox/public binding、model selection/operation、reservation/额度在退役与重复重开前后逐字保持；unknown不重发、不自动退款；启动expiry也不取消旧run。
- 显式模型保存、旧授权无效、单独新授权、绑定会话冻结新profile；正常preclaimed状态下最终发送检查拒绝pending模型选择。
- Kimi执行暂停时不生成新grant；MiniMax可正常开启，扫描分页不受33个暂停Kimi影响。
- SQL38/39/40→41保留原migration ledger；实际DatabaseWorker首个任务前已完成退役，无新future takeover/claim，正常channel关闭和thread join。

S2组合在当前Desktop干净提交上复验，五组25/2/12/10/1 PASS、零skip，见[evidence/s3-s2-final/result.json](evidence/s3-s2-final/result.json)。带数据迁移矩阵扩为15/29/37/38/39/40/41→41；不等于允许实际日常库迁移。真实Native→Host→固定Runtime本机边界仍仅1个loopback MiniMax合成响应并正常EOF退出；真实Provider HTTP新增0。S2 driver显式排除独立S3命名空间，原10项恢复组未减少，S3由自己的5项driver覆盖。

前端10文件70项PASS（含新v2请求/响应validator、退役/绑定/暂停模型UI逻辑）；Contracts9项PASS、8个已登记基线离线比较PASS，make lint通过；Desktop默认启动/有限grant/保存回执3项、产品Clippy、fmt、lint/类型检查及候选前端build通过。两代私有生成器和canonical候选来源检查通过；App bundle未重建。前端build保留既有大chunk提示。

## 失败记录、未执行项与范围

扩大默认自动计划三目标组合在本轮与实施前ddc840f完整源码导出中均于dispatch_tests.rs:463返回OrchestrationUnavailable；日志和baseline来源均保留，不混入S3修复，也不宣称全量计划E2E通过。原全targets Clippy位置问题、ChatPage原文案断言和旧Skill pin限制继续保留。S3草稿4因一次编辑范围错误造成Rust分隔符错误，未运行产品；修正后草稿5与干净提交最终5组均通过。

安全流程偏差：本轮曾误用旧`make generate`入口，它调用Skill fixture生成器（包含旧路径穿越归档fixture的生成）并重建SDK目录，随后因canonical schema URL解析失败退出。没有执行这些fixture的解压、安装、攻击或消费测试；不把该入口记为安全验证通过。资格工作树原本干净，所有无关tracked生成物按原HEAD逐字恢复，本次新产生的两项无关普通TS生成物移除；原工作区与fixture原文件哈希无变化。后续只使用已审查的leaf generator、strict schema和离线比较；不再调用全量生成/test入口。此记录保留事实，不以“隔离测试”为豁免。

S3源实现和时序子集已完成；S1—S3完整G3均仍受canonical App/WebView、旧隔离历史、实际亮暗/1180×760/权限UI、S1正常退出清理、跨平台和freshness限制。Owner已允许锁屏相关步骤延期，仍记NOT RUN。当前App维持原S1构建及其数据，不拿headless或旧G2V冒充新来源App验收。下一步是S4全调用面审计/接线与安全离线验证；回来后先正常退出旧App，再按当前同源canonical构建补验收。禁止新增真实模型HTTP，原30元账本与14.188544元未知预占继续保留。

## 治理与保留性最终复核

首次claims审计正确指出新增scheduled-plan-v2后旧G2V contract_refs不再覆盖当前集合。未把新契约硬塞进旧证据，已将当前G2V置pending、当前证据标NOT RUN；原PASS完整对象另存evidence/s3-prior-vertical-feasibility.json，原账本和实际成功事实不变。恢复门禁需要当前来源重新资格，不能据此新增真实HTTP。S1/S2/S3整体G3及final仍不放行。

[evidence/s3-preservation-audit.json](evidence/s3-preservation-audit.json)核验620个已有文件：618逐字未动；database.rs用逆向本轮补丁、memory用逆向FEAT164段落，均恢复启动快照哈希，FEAT162/163与其他既有改动保留。42个活动App文件、两份真实账本哈希全同，18086 readyz200，18083 fixture仍1请求。所有原分支/远端未变，治理暂存前各仓索引为空。

修正当前G2V freshness声明后，feature claims审计与strict包检查通过，元仓lint和53项治理测试通过；G3/S3明确拒绝（当前G2V、前置slice、App边界/纵向和freshness未完成）。首次与最终检查日志均保留。没有通过删除新契约引用、放宽validator或套用旧PASS来过门禁。
