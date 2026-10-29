# FEAT-162 — 契约、实现与零费用验证

2026-10-29（Asia/Shanghai）。用户授权按更新后的22号实施契约、代码、零费用验证及最后复审，明确禁止付费调用、Git提交和推送。本轮 contract-impact=breaking。前态见 [implementation-before](evidence/implementation-before-20261029.json)，完整命令/实际退出码见 [implementation-checks](evidence/implementation-checks-20261029.json)，复审见 [25号](25-implementation-reaudit.md)。原20号FAIL、旧台账及历史证据不改。

本地代码及可执行的定向验证完成；整体 implementation 保持 in_progress，AC-021—030仍pending，D4不通过。准确 App 激活/不可变 pin、真正历史重开与E1—E7未执行。没有继承旧额度，没有读取真实凭据或执行供应商/模型HTTP。公开 schema 的只读兼容检查不属于付费调用。

## 实施范围

| 仓库 | 本轮改动 |
|---|---|
| Contracts | web-retrieval0.3.0三工具，冻结0.2.0；Basic正文/Pro参数与结果、逐页状态/丢页；Broker0.7.0 prepare版本及双截止，Host v1 0.4.0/v2 0.6.0投影；同源Rust/Go/TS/validator/锁及本地同步入口 |
| Connectors | Pro固定REST路由；默认Basic/Fetch沿旧逻辑，新Basic正文/Pro独立归一化；旧两工具lease与新三工具lease隔离；完整35秒准入、A/D状态机、一次HTTP与正常取消/撤权 |
| Host | prepare显式声明新版本与60000ms配置；双截止投影和按钮决定；及时批准等待不会在A误过期 |
| Desktop | 生成结果validator与逐页正文/来源详情；旧值可读、未知格式普通文本回退；A到期禁用按钮；新版计量器离线策略和明确的canonical观察配置 |
| 元仓/设计文档 | 授权、实现状态、零费用证据、剩余限制、预算和复审同步 |

不改固定Runtime、依赖锁、数据库/持久化格式或专家内容。Skills 本轮无文件修改；真实不可变资源来源级联须在后续允许形成Git来源后完成，不能靠手改摘要或复用旧批准绕过。

### 契约与结果

新模式保留供应商来源顺序，title/snippet/正文缺失与null/类型错误按22号区分。舍弃无效页，原始空列表成功，原始非空全无效返回invalid_response。dropped_results=原始数−最终数，裁字段不计丢页；同一页多原因只计一次。所有最终JSON转义、文字副本、structuredContent及标记计入65536字节，不剪URL。

available必须有正文；unavailable表示上游未取得正文；原有正文裁至空仍为truncated。标题/摘要裁剪不改正文状态。有丢页/逐页正文截断必须顶层truncated。JSON Schema与生成Rust共同校验，Desktop runtime validator同源执行；TS仅表达结构，不伪造跨字段静态保证。普通大结果、双份转义、混合页和裁至空已验证；极端必要元数据无法交付仍保留response_too_large分支，不以成功空列表代替。

旧Basic省略/false保持旧输出及归一化。旧Host不携新prepare字段时仅看到冻结两工具，新增模式拒绝。新Host遇旧strict Broker在prepare失败关闭。旧0.2.0源与实施前完整commit逐字比较；新reader覆盖旧输出。真实旧App回滚/新历史重开未执行。

### 期限工程决策

固定Runtime tools/call计时从调用操作开始，elicitation等待可暂停；Gateway收到请求不是起点。`internal/session/market_submit.go`先等待owner prepare，再向Runtime提交turn。Broker因此冻结自身单调prepare时刻+固定60秒作为可信保守下界，不晚于真实MCP截止，不因bind/replay/排队重置。原call与lease/scope继续收紧D；A=D−35秒−2秒。

A已到的新提案返回源生成的明确“执行时间不足，请重新发起”工具错误，不创建审批。A只限制Pending→Approved。在A前已批准者仍可于A后、D前执行；到A未批准者不可继续批准，发送前实际剩余不足35秒仍零HTTP。Host与Desktop使用同一A，旧Basic/Fetch无双字段且保持min(剩余,15秒)。新模式窗口至多约23秒减去模型/准备/排队时间，不承诺实际用户能得到23秒；真实正常时序与可用性仍需E2/E4/E6/E7。

### 计量与收费关闭

新版authority为FEAT-162-basic-pro-v2，单独schema2账本；旧账本不复用。出站body保持原字节，tools/include/prompt/结果/输出上限不改，模型次数包含全部请求。E1—E7预算计数17，E5四次/两回合；Basic/Pro/Fetch各3，REST预占0.105元。未知usage保留预占，不把取消、过滤或截断当退款；旧19项计量回归保持。

当前无供应商native搜索硬费用上界，也无本observer停止worker尚未发送许可的已验证链路。因此v2 live入口在读取凭据、监听或发送之前明确拒绝，`LIVE_EXECUTION_QUALIFIED=false`；plan里的hash/布尔值不能解除该门禁。离线计数器不是费用批准，也不是端到端路由或E5/E7来源质量证明。后续必须补齐硬上界依据、正常owner停止/撤销链及准确来源/等价证据并再授权，不能只改布尔值放行。

`daily:prepare --feat162-observe`仅增加显式冻结的本机观察配置，普通环境不采纳ambient override。它继续要求所有源已提交且干净、准确来源批准、同一generation；本轮禁止提交，故未运行daily prepare/open，未制作虚假immutable receipt。

## 已执行零费用验证

| 检查 | 结果与范围 |
|---|---|
| Contracts Node四文件 | 33项通过；闭集输入输出、旧定义、双截止、v2来源与新状态约束 |
| Contracts Rust web / broker | 5项 / 6项通过；普通值、日历、闭集、生成decoder；Go broker/Host生成包检查通过 |
| Connectors Kimi focused | 24项通过；一次自有loopback正常请求与graceful关闭，其余纯值/受控内存响应，未发供应商请求 |
| Connectors标准worker-lint | 来源、四族contract-check、rustfmt、Clippy -D warnings通过 |
| canonical worker build | 通过；独立新generation，未执行该二进制；摘要e61468d473a7223068aba1d9ced8ee4745951c2cbd5b6f3c554908be009d5fdb |
| Host | go vet ./...、两项指定审批测试及race通过；无Runtime/供应商进程 |
| Desktop前端 | 最终5文件28项通过（此前更宽9文件44项亦通过）；lint、vue-tsc、Vite构建通过 |
| Desktop Native | cargo fmt、lib Clippy -D warnings通过，4项observe/history/approval测试通过；未启动App |
| 新旧计量/观察配置 | v2 6项、旧meter19项、纯配置1项通过，均离线 |
| 元仓治理 | D0、lint、57项治理测试通过；不代表D4 |
| Desktop文档 | docs:build通过；保留Vite/VitePress已有大chunk警告 |
| 来源 | Connectors正规sync check、Host/Desktop local候选摘要检查通过，不代表不可变pin或激活 |
| 全量breaking | 8基线中3通过，5因既有scheduled-plan-draft远程$ref EOF退出102；没有关闭checker或伪报全绿 |

完整breaking通过f16a497e…、6f632f15…、811f38d6…；EOF为当前61137174…及bedf4159…、e35ae9a0…、1a213ac8…、35e0949c…。精确commit、命令和日志摘要在机器证据中。checker尚未完成的后续步骤不能宣称通过；本轮未修改该无关远程schema问题。

中途失败亦保留：Pro路由白名单遗漏后已补；新增前端测试初次缺happy-dom环境后修正；v2旧版本断言更新；浏览器validator依赖与字符串替换转义修正；最后新增条件schema使TS投影出现unknown/never，改由结构类型+严格runtime validator处理，最终构建通过。新Ajv生成validator最初被手写代码风格lint报165项；按现有精确生成文件名单加入该文件，仍强制canonical字节及语义检查，不关闭业务代码lint。初次错误路径/无匹配测试命令不计入通过数量。旧日志只作过程证据，不覆盖最终结果。

## Z计划覆盖与未执行项目

| 组 | 本轮覆盖 | 仍缺证据 |
|---|---|---|
| Z1 | 旧schema逐字、默认Basic/Fetch与旧history decoder | 真实旧App回滚/重开 |
| Z2 | 出站原字节等价、显式配置、门禁零发送 | 准确canonical App端到端等价 |
| Z3 | A前/到A、越A已批、短scope、发送不足35s、旧模式 | 实际IPC/调度时延和真实正常时序 |
| Z4/Z5/Z6 | 页状态、裁至空、混合/空/全无效、字段类型、UTF-8、封包上限与去重丢页 | 实际App重开后的同结果；必要元数据失败分支实机证据 |
| Z7 | 未知预占、三工具计数、无硬界live拒绝 | native硬界、真实账单/供应商原始计费事实、owner联动停止 |
| Z8 | 正常批准/拒绝/取消/撤权、一次许可和loopback正常关闭 | canonical新worker的Host进程EOF全链、实机用户恢复 |
| Z9 | 生成校验、可读组件、DOM按钮过期 | 亮暗主题/键盘实测/1180×760/实际App正常重开 |
| Z10 | 参数日历/站点边界、工具描述、旧lease关闭新模式 | 模型实际选择（保持E1—E7 NOT RUN） |

不执行含强杀、权限破坏、二进制替换、攻击fixture的历史整套测试；不运行会在fixture中创建Git提交的旧primary harness。标准make lint/test组合包含不可变pin或未经筛选测试，采用上述明确入口，不将局部检查称整套PASS。所有未执行项影响保留；不能用合成结果证明真实模型质量/费用或完整D4。

## 预算与交接

本轮授权/实际付费次数均0。完整未来费用仍为Σ可证明模型上界+0.105元+R_native，241.421224元仅旧模型界限适用的条件小计。旧20号模型4次、三项未知及42.710457元保守占用不动、不复活。

后续顺序：解决完整兼容检查依赖→形成用户允许的不可变契约/消费者来源与资源级联→canonical准确客户端构建和安全实机预检→取得供应商硬费用界限并完成停止链资格→单独收费授权→执行E1—E7和真实历史重开。当前代码留在原工作树，未提交、推送、激活或发布。
