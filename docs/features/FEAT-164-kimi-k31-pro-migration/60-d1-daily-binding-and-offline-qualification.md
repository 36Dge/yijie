# FEAT-164 D1：日常Home绑定与只读ready门禁完成

2026-10-27。Owner已明确批准59号D1。本轮复审后完成限定六文件修正、安全离线验证及新canonical prepare-only构建；**没有访问日常库，没有生成真实日常部署绑定、执行D2—D5或启动App/workflow，没有新增真实或本机模型HTTP，没有修改Runtime核心/补丁、Native/SQL或Infra源码。**

D1工程阶段PASS_OFFLINE。原日常Home不连续和隐式workflow-up问题已经在入口修正并离线验证；实际日常状态、备份/预检、维护、启动资格仍未执行。G4保持pending，不把新daily bootstrap的prepare-only或纯状态测试自动换算成最终实际启动资格。58原已接受范围、完整App正向never-sent仍NOT RUN及Owner替代接受均保留。

## 批准范围、实现与来源

Desktop本地提交`b789d5c8147fde9890d49b67c6ecb191473793db`，独立目录`feat164-d1-candidate-20261027/yijie-desktop`，基于ea8763dfc40466e9b808a1b39afad71dbff1ac56。恰好六文件：两个既有入口/receipt、新feat164-daily-deployment.py、既有入口测试、daily部署说明和SECURITY。原dirty工作树不应用、不覆盖。

增量contract-impact=semantic，权威是Desktop私有部署策略`feat164-daily-existing-homes-v1`，Owner本轮确认覆盖该部署/文件系统范围。整需求breaking不降级；公共wire/新schema/Native command N/A。Host4f966e8、Contractsc5d1383、Runtime11fd/r5、Connectorscc56、Skills595固定不变。Native、renderer、契约生成物、依赖及Cargo文件逐项Git对象比较无差异。

| 修正 | 当前行为 |
|---|---|
| 制品与数据Home分离 | `.local/feat164-daily`只存构建制品；prepare-only不创建host-home/codex-home。执行必须读取批准绑定，沿原Desktop的`.local/demo-fast`既有两Home，不创建、复制或修权限 |
| 执行准入 | 非prepare daily只准`--reopen`。绑定文件owner/类型/模式、独立摘要、精确policy/identity/receipt/helper hash、固定Native根、原数据根、原provider引用、Infra源码摘要及D3/D4/D5批准字段均核验；未知/缺失/过期不继续 |
| 运行与维护分开 | D3仅显式维护；D4首次启动要求Kimi暂停，D5也须明确true/false。批准记录必须声明零模型预算与全模型无可派发工作；它不是替代D2现场事实的密码学授权。维护仍无provider/workflow凭据及服务启动 |
| workflow只读ready | daily不再调用workflow-up。exact bundle receipt检查后，仅用固定SHA的真实Infra源码执行read_state、container inspect/ownership及原鉴权observed_ready；明确ready=true才成功。没有record/status/up/init/build/render/credentials/verify_editor调用，不改服务/DB，不输出Key或内层异常 |
| 入口兼容 | 普通/旧隔离入口保留原选择语义；新绑定文件/摘要/stage环境不继续传给Native。日常新制品不能复用旧receipt或默认为新空Home |

Infra源码SHA `7fd0450319467d5ad97eb56f2bb713ac411ea19c8708ab2529ffcf6d350194ea`在helper中固定；评估已核验源码字节，不从未核验的路径重新加载代码。使用`-B`，不写Infra pycache。其原observed_ready在未来获准执行时会验证K_NA/K_AC配对/epoch并GET本机状态/editor；本轮未调用这条真实服务路径，只有纯进程内状态验证。

为避免D2现场未知导致擅自猜测，D1没有生成真实绑定。记录格式、审批引用、24小时以内有效期、required字段和固定布局已写入Desktop权威说明。实际原Home布局若不同，后续停止另报，不能扩成任意目录迁移器。

## 安全验证与首次失败的处理

| 验证 | 实际结果 |
|---|---|
| 入口Vitest完整文件 | 61/61 PASS、0skip，含7项D1测试；其中纯绑定14个正常子例、workflow 3种正常状态，不重复相加为测试总数 |
| 原daily profile/模式拒绝Node组 | 3/3 PASS |
| 新Home连续性 | 新保留合成目录内正常SQLite记录：绑定后仍读原两Home，原字节保持；没有复制真实数据或造unknown/never-sent |
| 新准入拒绝 | 无prepare、无阶段、无绑定时在凭据/服务前停止；普通结构化错误与过期输入不涉及攻击载荷、权限破坏或可执行替身 |
| 静态/前端/文档 | Bash语法、Python AST、pnpm lint、docs:build PASS；文档构建原chunk体积警告保留 |
| 同源资格 | 19项FEAT164只读generation/source checks全部PASS；六个产品来源干净 |
| canonical准备与同回执检查 | 两条命令均exit0，见下节；没有App或workflow启动 |

首轮完整入口测试43PASS/18FAIL。复审Git基线确认：11个旧截取脚本用例遗漏外层workflow_requested初值，5个旧expert-root用例遗漏kimi_k31_candidate初值，2个旧断言仍匹配更早错误文案。仅在同一获批测试文件补两个fixture初值并匹配原入口实际拒绝文案，未放宽产品准入；修后61通过。初轮日志、归因与修后结果全部保留，不把18个断言错误当作18次重试。

只执行相关安全测试，不运行含禁止行为的全量业务仓suite；不声称全仓make test或远端CI通过。Rust/Native/Runtime未改，本轮没有重复已通过的模型/历史/取消/计划业务回合。

## 新制品（仅prepare-only）

实际命令：

- `bash scripts/run-local-demo-fast.sh --packaged --kimi-k31-daily --prepare-only`
- `bash scripts/run-local-demo-fast.sh --packaged --kimi-k31-daily --prepare-only --reopen`

第二条保留prepare-only，校验同一来源/环境/制品receipt，不构建或启动App，也不读取真实绑定；不能省略prepare-only拿来启动。完整源码和环境由canonical脚本记录；无provider/workflow凭据，编译依赖离线，正常构建工具生成新输出，没有替换旧制品。

新App：`feat164-d1-candidate-20261027/yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI.app`；identity `com.yijie.ai`，包内119文件，1207个构建源码输入复核一致。

- App SHA `944b6b238b7f7b0f36cfab2be358d83b9be044587cc37a3ea5a161fc68b40015`。
- receipt SHA `490e35d8e5214d1dddd84def050edf093cdd9f2f7aa9edd5fb83076ebb3c9fc3`，含新deployment_policy。
- Runtime仍r5 SHA `283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`。

两数据Home均未创建；旧c29f7e0日常App、4b0ec55原R1及179dbd1资格App及三个receipt共360文件记录保持。未签名本地开发构建不是发布，也不等于真实日常首次启动资格。

## 完成后复审、保护与下一步

完成后独立结构化审查覆盖路径/owner、无默认空Home、stage与回执一致性、旧入口隔离、workflow调用链、失败信息、权限与回退。CUTOVER-01/03记FIXED_AND_OFFLINE_VERIFIED；没有新增Runtime核心修复需求。审查是Codex工程复核，不冒称独立人工批准或日常通过。

原500份dirty（另含混合memory）、7份账本/历史快照和360份旧App/receipt逐字保持；混合memory仅本轮专属段落进入提交。累计真实HTTP13、45元cap、29.740299保守累计及两份14.188544预占不变。实际日常数据完全未访问，不声称本轮重新核验了日常DB内容或可迁移性。

D1到此完成。下一步只有用户明确批准D2后，才可正常停止原应用、完整冷备份及第二副本只读预检，确认实际Home/schema/unknown/grant/全模型自动工作及部署记录。D3维护、D4首次App/Host/Runtime写入、D5启用仍独立批准。继续使用59的停止条件和兼容reader回退；不清unknown、不退款、不恢复旧writer、不手工checkpoint/删WAL、不强杀，不恢复已移除的搜索质量或外观专项。

当前G4没有因本轮离线结果自动晋升：新daily执行绑定及真实启动链尚无获准现场事实，D2—D5未执行；旧accepted local证据按原来源保留。不以再跑模型回合代替这些数据部署边界。

证据索引：evidence/d1-audit-index.json。完整私有审计与合成目录保存在feat164-d1-audit-20261027。仅本地提交、不推送；无运行中的验收App或本轮服务需用户交接。

元仓audit-claims、strict、S4 G3、lint、53/53测试和7份Shell语法通过；G4实检仅因当前pending返回1，记录EXPECTED_BLOCK，未降低门禁。提交前500份dirty、7账本及360旧制品记录保护检查PASS。精确日志见d1-governance-checks.json及d1-preservation.json。
