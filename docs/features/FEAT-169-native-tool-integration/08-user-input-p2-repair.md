# 原生问答四项 P2 修复（2026-11-08）

用户明确要求“分析原因并修复P2的4项问题”。范围为[07复审](07-user-input-context-reaudit.md)的RUI-01至RUI-04；四项修复、定向回归、实际界面问答/取消及日常入口恢复均已完成。未修改其它工具、记忆策略、上下文策略或原生Runtime实现。

| 问题 | 根因 | 修复及行为 |
|---|---|---|
| RUI-01：只读权限暂停问答 | touch被归入ReadSessions，而它会停止倒计时 | Native read使用ReadSessions；touch/answer使用已有SubmitTurn（task.read+task.create），未知action拒绝；前端也禁止只读调用touch。真实应用facade测试证明只读调用在session查询前即被拒绝 |
| RUI-02：过期回执无法恢复 | Bridge/application/API把not_found等错误折叠为通用故障 | 由源契约生成UserInputError，问答专用parser校验HTTP状态/错误码；复用既有IPC错误并严格核对requestId。仅当前snapshot无原请求且原回执明确not_found时撤去旧表单，保留“历史结果无法确认”，不重投、不伪造终态 |
| RUI-03：迟到响应回退终态 | touch成功、poll失败及finally缺少完整版本检查 | 同时检查聊天epoch、mutation、读请求序号；终态不能回到pending，旧touch不能使回答后的回执读取失效；旧异常/finally也不得覆盖新状态 |
| RUI-04：结束后的回答被接收 | activeTurns更新与问答关闭有锁间隙，提交只检查pending | 按Manager→permissionCallbacks→userInputs统一锁顺序检查ready、关闭状态、generation、owned root和原活动turn。answer/touch/到期都用同一准入检查；结束后新提交拒绝，先前已获准操作仍读原写回回执 |

## 来源、兼容与范围

最高 `contract-impact=breaking`：修正Native touch此前错误放行只读调用的权限遗漏，按用户明确授权执行。HTTP/IPC字段、既有错误枚举、schema_version及Runtime canonical协议不变。Owner为段成威；producer为Host，consumer为Desktop Native与前端。源契约0.2.0先明确权限、错误及终结语义，再由原generator生成Go/Rust/TS/同源校验；没有手工修改生成物、另建审批体系或另造Agent执行机制。

源为 `yijie-contracts/openapi/user-input/user-input.yaml`；Runtime问题/答案仍机械投影canonical schema。fallback完整commit为`c24d73fde83a01b5dd2a9ded8defb5bbef34e311`，该基线尚无本工具family。现有family未增加wire结构或错误值，fallback检查仅证明本family没有修改既有已登记协议，不冒充已发布0.1→0.2的生产兼容证明。

本地配对顺序为源契约/生成物→Host→Desktop→定向验证→原开发入口；已有用户未提交工作保持。来源锁和开发构建receipt标记`local_worktree_candidate/release=false`；没有生成发布tag、commit或push。发布前仍须正式不可变pin与consumer审核。本次无数据库/rollout迁移；正常取消/结束活动任务并退出后可切换完整配对构建。安全修复不以恢复旧只读touch行为作为日常回滚方案。

当前Runtime仍为 `tool-search-v1/fac52ad79cc7e0a379fc597a7ecfcee573205d38a60c9d0ed3a2e96871ab0f45/aarch64-apple-darwin`，没有重编或替换Runtime。已启用的后续工具搜索只作为当前配对依赖保持，不扩展其能力。

## 验证

| 验证 | 结果 | 范围 |
|---|---|---|
| 前端问题卡/API/composable | 26 PASS | 原回执失效、未知错误、严格请求关联、同聊天响应乱序、迟到touch/旧poll异常与finally、只读UI、敏感输入卡既有用例 |
| Desktop Native | 5 PASS | 真实授权facade、HTTP Bridge合法/未知错误、内部错误含义、原请求与脱敏回答 |
| Host状态机 | 7顶层+6子场景 PASS，race开启 | 原提交幂等/回执、暂停/超时/跳过、合法turn/completed交错、正常关闭、新旧generation；已获准回执结束后可读取且不重投 |
| Host HTTP | 2 PASS，race开启 | owner认证、原session绑定、no-store、同源错误码，不接受审批决策代替答案 |
| 真实固定Runtime+本地provider | 4 PASS，race开启 | 问答与正常恢复、new_context/历史、旧会话升级不重放、专家/技能/input-only边界；未调用供应商 |
| Contracts | 5 PASS | 原生投影、公共形状、上下文策略、fallback、封闭错误；Redocly lint与generate --check通过 |
| 静态检查 | PASS | 修改前端文件ESLint、vue-tsc；原生测试编译、Go格式和差异空白检查；仅格式化本次新增Rust区块 |

回归命令及机器摘要见`references/user-input-p2-repair.json`。真实Runtime用原审计test-only source overlay，仅使测试配置ToolSearchEnabled匹配当前固定产物，没有替换产品代码、程序或可执行文件；这个结果不是付费模型验收。初次新增错误fixture遗漏既有required message、错误enum比较顺序不同，补齐真实契约后重跑通过；未改宽schema或放松校验。

没有执行全量回归、攻击fixture、权限破坏、强杀或故障注入。没有读取真实答案做验证。开始修复时App/Host/Runtime已退出，未触发原生watcher重启。

## 开发入口与真实界面

用户已批准“仅 Kimi 最多 6 次”。实际调用3次，均为`kimi-k3.1-pro`、HTTP 200；MiniMax/图片/外部业务写操作均为0。复用既有`chat-model-smoke-meter.py --qualify-native-tools --shutdown-on-stdin-eof`，本任务独立ledger，限制6次且请求/响应原样转发。canonical `start-ui --tool-search-meter`仅复用已有固定计数器传输入口，其历史参数名不代表验收或改动工具搜索。

实际macOS App（原日常Homes、标准debug bundle）中新建隔离workspace聊天`01a1bb84-6d78-7232-9491-8219dcb236f1`：

1. 原生问题卡显示2题，选项/自由补充、60秒可选倒计时均来自Kimi原生工具请求。输入后显示“已暂停自动跳过”；分页保留普通合成备注，secure text field与实际截图显示圆点遮罩。
2. 单选切换生效；提交后卡片撤下，显示“回答已发送”，同一轮Kimi返回“问答验收完成”。未自动重发回答。
3. 下一轮原生问题无超时、显示“等待你的回答”；点击主输入区“停止生成”，23秒时显示“已中断”“问题已结束”“已停止”，问题卡撤下。没有用跳过来冒充取消，也没有把取消标记为answered。
4. 通过App自身⌘Q正常退出；Host与受管服务正常清理。计数器stdin EOF后`stopped_normally`，18083监听关闭；随后从不带计数器的原canonical start-ui重开。

额外观察：首轮长时间停留时曾出现“当前进度待确认”并清空未提交草稿；原请求仍可读取，重新填写后提交成功，完成事件使聊天恢复“已完成”。源码显示既有store在context到期时clearAuthority（`src/stores/chat.store.ts:939`），问答对context变更清草稿以避免跨权限继承；这与观察到的重同步现象相符，但本轮没有专门采集授权续期时序，不能断言已完整定位其触发原因。本次没有扩大为授权续期/草稿保留策略改造，也不声称覆盖无限等待期间的无感续期。首次部分AX点击受动态布局/标识变化影响，重新取得控件后操作生效；没有用脚本伪造UI结果。

未进行真实越权、竞争时序故障注入或故意等10分钟淘汰回执；这三类边界由前述普通组件、授权facade及Host状态机定向回归验证，真实模型验证覆盖正常问答与取消。

最终恢复核验：不带验收计数器的canonical start-ui已重开，Host `/readyz=200`，当前Runtime及上述原生配置有效，运行命令中不含18083计数器路由。实际App重开原验收聊天，已完成回答和已中断记录均保留，旧问题卡没有复活。产物SHA-256见机器记录，22项固定修复/生成/配对文件与验证摘要无漂移。未提交或推送。
