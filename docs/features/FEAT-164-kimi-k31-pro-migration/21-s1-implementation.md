# FEAT-164 S1 活动身份、受管配置与退役准入

用户确认20结果并授权从S1继续实施；本轮真实模型HTTP新增上限为0，旧账本及14.188544元未知预占全部保留。只本地提交，不推送，不迁移日常数据库，不扩展到S2/S3。起始来源与其它需求文件摘要见evidence/s1-start-baseline.json。

## 影响和实施边界

`contract-impact = semantic`：实现已固定chat-models-v2/runtime-kimi-k31-pro契约的活动/退役/activation_required语义，并改变Host私有受管配置过渡及本代执行准入；整体FEAT-164仍breaking。公共DTO、Runtime协议和价格/输出参数不改，继续固定Contracts f2819c66a2368aaff37216a46c48d5cd81df1747与Runtime074417e5e2f5f55704ea5e1777e7a22d514076b4。私有配置前身的权威为Host5022435a6272263e66e46a41b7ed7c3f9fb6caf9，不把未提交FEAT-162/163内容冻结为新来源。

1. 冻结上述Host提交实际产生的早期/当前v1 catalog及TOML模板；验证时使用冻结字节，不根据后续Definitions反推历史。未知漂移或缺半个v1组合拒绝。
2. 保留已存在v1文件，不覆盖其原字节。显式Host受管前身许可才允许在同一独占Home内写v2文件；v2允许空空→新catalog/空→新新，反向缺catalog、未知文件均拒绝。先完成双文件再启动Runtime；重开按精确组合恢复。新v2路径沿已建候选而非改写旧文件，避免旧reader被静默升级；旧Host不作为新数据回滚方案。
3. 新Kimi执行暂停与目录/历史读取分开。暂停仅影响Kimi执行，MiniMax和历史读取保持；通过既有activation_required投影，不增加公共字段。标志只在精确local候选成立，默认值保持已通过候选行为。
4. 候选必须显式活动profile；turn同时匹配同代start/resume完整模型回执。模型配置发出前撤旧绑定，回执缺失不保留旧确认。旧StartTurn、V2、普通start/resume、草案及标题入口纳入。不会用thread/read推定模型，也不写历史记录。
5. 在现有干净资格工作树实施并验证，再将专属patch应用到原工作树/索引；公共来源与Host→Desktop构建pin逐级本地固化，原未提交内容保留。

## 验证与门禁

创建真实存在的TCONF-164-01测试，覆盖普通配置组合、未知内容拒绝（普通文本，非攻击载荷）、旧文件/trust保持、重复启动、暂停/恢复、缺失/退役/错配身份及完整回执绑定。实际固定Runtime用普通loopback server验证，无真实Key或外部Provider连接；进程走正常关闭。Desktop验证严格配置解析及child环境传递，canonical构建/正常本机链路按实际范围记录。

本轮不调用旧meter、不修改其账本、不用剩余金额换取请求。新Host/Desktop来源使上轮真实G2V不能充当本slice fresh真实模型证据；原PASS按其原来源保留，S1若缺required纵向证据则G3保持未通过，不提前进入S2。未执行项及影响明确登记。

## 当前进度

S1源实现、定向测试和canonical构建已完成；本机App新Kimi正控PASS，暂停/历史与清理的UI验证进行中。旧模型新执行从新候选进程验证来源、受管配置完成后的启动边界开始被拒绝；不声明日常应用已切换或全部隐藏工作已迁移。


## 已固化实现与复审

Host `9cf7d4812f8266ae5df5e4b73e78aaab44855ab2` 固化活动身份、冻结前身和本代回执准入；复审发现旧标题只有session引用仍可能推断新身份，追加 `e8ae83f9c53fb41cc80139e0d0f70d7c8268b4ab`：未分类/退役/暂停的新标题拒绝，既有完成回执只读返回。Desktop `174fbaf661e4fdf48828ff8bbabbe5d55c157bed` 固定该Host，增加严格暂停设置传递、正确可用性提示，并修正草稿重置/切换scope仍使用旧profile的遗漏。未改公共DTO/Runtime或旧账本。

受管旧文件保持原字节，升级许可仅在Host显式候选下识别已知v1前身；不会自动开放Desktop旧日常数据库。暂停是启动设置，必须先正常退出；没有热切换或新增取消机制。Native仍按原scope/权限持久化，Host最后准入核对显式活动profile、当前generation真实start/resume回执及精确effort；候选不能通过旧StartTurn或high/none覆盖max。未完成的claim/迁移/计划路径仍归S2/S3。

当前测试命中：TCONF-164-01已创建并独立执行，普通状态10子例通过；Host模型/目录/API/暂停/标题及race检查通过；固定Runtime实际loopback的新Kimi→MiniMax→新Kimi与已知前身+暂停Kimi/MiniMax路径通过，均正常关闭。Frontend 11项模型测试、候选/default两种Rust暂停检查、前端lint/类型/构建、Host make lint及候选产品lib/bins Clippy通过。最终精确命令/退出码集中于evidence/s1-final-tests.json。

保留的失败：初次新增组件测试将reason推宽为string，已用正确的字面量类型修正；初次Rust格式检查已按标准格式化修正。Desktop全targets Clippy被原 `native_conversation_storage.rs` 的source_reader_tests非尾部位置拦住（原6080a568已有）；未修改该其它需求内容或关闭警告。完整make lint先被独立旧Skill provider pin要求1b7bfd1而当前Host为e8ae83f阻断；当前FEAT-164独立来源检查通过，不伪称完整make lint通过。全量test中的权限破坏/攻击fixture未执行，使用已审查安全测试，覆盖缺口保留。

已有495个未提交文件/记录按起始摘要核验；Host共享文件通过在临时副本反向应用本轮专属patch复核，原有差异逐字恢复，证明未混入或丢失。见evidence/s1-preservation-audit.json。只本地提交，不推送，未改远端或分支。

## UI验证状态

canonical同一构建下，11:48:35发送本机新Kimi正控，界面显示已完成及明确合成响应，loopback记录kimi-k3.1-pro/max，外部0。正常退出0后以暂停设置重开，来源校验及readyz200；随后Mac锁屏，已请求用户手动解锁。当前App会话78901、本机fixture会话72636；无真实meter，loopback仅1次。不能把尚未观察的暂停/MiniMax/重开清理步骤写PASS，不强制退出。

## 后续Owner决定（2026-10-25）

Owner因不在电脑旁，明确允许需要解锁的步骤延期并推进后续离线工作。此决定覆盖本记录原“不进入S2”的排序限制；未执行UI仍NOT RUN，S1 G3未通过。S2基础及新的准确续办入口见22；当前App仍是本记录的旧构建，不能覆盖运行中的bundle。
