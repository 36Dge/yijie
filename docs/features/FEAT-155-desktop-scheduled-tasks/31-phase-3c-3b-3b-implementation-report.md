# FEAT-155 · 3C-3B3B 原生装配与草案恢复实施报告

2026-09-19。**本批候选实现与零真实调用验证完成，报告后停止。** 按[30执行方案](30-phase-3c-3b-3b-implementation-plan.md)接通同一原生启动、worker、Coordinator、Host和固定Runtime的草案路径；没有进入页面、日常库激活、唤醒或真实Provider验收。普通入口SQL15/Store5、候选22/6保持，没有SQL23/Store7，真实文本累计0/12，图片/商家/MCP外部0。FEAT-155全部Must及D4仍未完成。

## 1. 本批结果

| 边界 | 交付结果 |
|---|---|
| 同源契约 | 新增草案专用mapping GET，机械生成/同步Go、Rust、TS与严格schema；原两类恢复查询和固定outputSchema保持。私有IPC增加来源重发现、分操作资格、显式继续，全部21命令同源并注册。 |
| 原生装配 | canonical launcher选择29精确artifact，native计算独立候选数据根及scope目录，原Host入口在开Store6前检查descriptor和artifact。同一SQLCipher worker/Coordinator；本批装配不为已有计划开放manual/automatic出站。 |
| 最后POST准入 | token/readiness等await之后重验当前UI/native授权、source/operation、用途/workspace、Host与lifecycle。只有本代显式submit/continue的限时内存许可可claim。create/turn标记attempted后结果不明保留unknown，不再次授权。 |
| 只读恢复 | 专用mapping与原operation GET核对全部身份、版本和用途。create恢复只绑定事实，不排队turn；已存在pending turn重开也无发送许可。accepted只补原绑定，缺原generation保留NULL；当前回应实例只提供临时观察依据。 |
| 来源与确认 | scoped本地conversation/turn查回source；显式继续复用原正文、原operation及唯一outbox。旧attempted未知阻断，不变成重跑。仅完整final_answer和completed原生事实形成候选；重复确认仍只保存一个paused计划，墓碑不复活。 |
| 观察与并发 | 恢复观察在接收新事件前重验精确依据；Host草案resume与turn准入串行，未决会话拒绝resume；失败恢复不编造旧执行终态。 |

原先推荐的`/scheduled-plan-draft-sessions/by-task/{task_id}`与既有resume路径产生OpenAPI歧义提示，实际采用独立`GET /v1/scheduled-plan-draft-session-mappings/{task_id}`，保持原功能与最小字段。缺少thread/responder时省略，显式null拒绝；bound必须有thread。整体按**contract-impact=breaking**保守审查候选IPC/部署/恢复解释；新增独立GET本身additive。源先生成再由Host/Desktop消费，未把本地dirty源锁称为发布pin或Consumer Owner人工批准。

## 2. 正常入口与兼容边界

Desktop原launcher接受`YIJIE_FEAT155_SCHEDULED_CANDIDATE=true`，仅普通开发入口，排除图片、workflow、Sorftime及其它非本批组合。来自Contracts原生投影的同一artifact lock只供Desktop启动器核对产物；native RPC仍仅由Host消费。新数据根为App data中的`demo-fast-scheduled-candidate-v1`，不复用日常`demo-fast-v1`。没有运行完整Tauri/App页面或读取真实Provider key；本批真实进程验证直接使用同一`cmd/desktop-host`标准构建入口及自有临时数据。

私有`YIJIE_SCHEDULED_CANDIDATE`包含version1、owner、tenant、workspace_root，由native传递；Host检查当前父进程、实例UUID、规范路径、OS属主、0700权限、scope后缀和目录分离，再验证29产物后开Store6。它仅选择装配，不授执行权。普通目标15/5及已有22/6兼容reader保持，关闭候选后应保留reader和历史，不降版、不删表。

固定Runtime未修改、未重建。binary SHA-256 `bd7d26205e2d735dcac0f35fc089a7b30a5c18a54586b94a2c7f624f2f5b7672`，manifest SHA-256 `14d4073de87be137cf39f770c091b8ab62a7c34933bc49dc50f12b4ddd3a494a`，269 stable schema、experimental=false。来源及五仓保护见[工作区审查](evidence/phase-3c-3b-3b/workspace-review.json)。

## 3. 已执行验证

[检查命令/退出码索引](evidence/phase-3c-3b-3b/checks.json)与[真实进程结果](evidence/phase-3c-3b-3b/native-smoke-result.json)分开保留。所有数据均为自有临时SQLCipher/bbolt或明确声明的本机HTTP样例，无真实业务数据。

| 检查 | 结果及证明范围 |
|---|---|
| Desktop FEAT-155 | 97/97定向检查通过；末轮保护修正后12/12草案复测通过。恢复GET及后续Coordinator/SSE轮次POST=0，已有pending重开不claim，显式继续保持原operation；正常撤销/睡眠在最后POST前拒绝。 |
| 旧路径 | 8/8授权、原outbox、原生身份/事实、权限正常重开及只读历史回归通过。 |
| typed IPC / 共享wire | 26组native请求/响应覆盖21命令，Rust/TS/strict AJV一致；14组实际Host/Desktop wire值符合共享源。typed client9/9通过，传输不确定不自动重试。 |
| Host | 12项顶层定向race测试通过（另有3个子场景）；scoped vet通过。历史真实文本fixture集成测试本次SKIP，不把跳过记为通过；另用真实无模型Host入口检查。 |
| 真实Host/Runtime | 最终2次启动、正常SIGTERM退出均exit0；create、只读mapping、同代显式resume成功，重开mapping不变，nonce换代。模型turn POST=0，真实Provider NOT RUN。 |
| 源与构建 | 两契约族leaf生成/同步、9/9 Contracts测试、私有IPC生成一致；Rust clippy全targets无warning，前端lint/build与脚本语法通过。Contracts完整lint通过，保留12条既有Redocly warning；前端build保留既有大chunk提示。 |
| 兼容 | fallback `db4458fe94572c4df41a114005d54a049bb79b1f`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`6f632f155eacdaf93df0e0b00b5dab9e369c5442`、`811f38d6b104fa18477107e7ac91a85e19c445d1`结构检查全部通过。它们不代替部署/权限语义审查。 |

元仓strict、D0、audit-claims、lint及50/50治理测试通过；136处本地链接有效。

## 4. 真实限制与修正

**冷重开的未执行空线程可能没有Runtime持久历史。** 真实检查中，此类线程的mapping可读取，但显式resume返回operation_unknown；Host原idle事实和绑定保持，没有替代thread或新turn。这是本批明确保留的不可恢复情况，不声称“任何旧草案都能继续”。已持久化的完整原生final/terminal事实仍可重开确认；缺事实的旧unknown继续未知，后续页面需要如实呈现。

同代新建空线程也曾因多余resume失败；已用原Manager中“同generation、同workspace、从未尝试turn”的原创建回执闭环，并重新查询实际策略。开始turn前即撤销这项空线程快捷条件；不会把冷历史缺失解释成可新建。真实进程最终复测通过，同时保留冷空历史不可用证据。

开发过程中还修复strict schema条件分支的strictRequired声明、测试构造器遗漏字段及路径未canonicalize、测试中的Option访问编译问题。一次真实预检因测试HOME位于系统临时根导致Runtime version输出附带helper警告而拒绝；改用项目下独立自有临时HOME复测，没有降低产物校验或更改用户HOME。最终以本报告索引的final日志为准，不把中间失败改写为通过。

## 5. 审查与停止边界

主代理完成源→生成→consumer、候选默认/数据隔离、最终POST授权、attempted幂等、事实恢复/NULL来源、普通路径与退出所有权的结构化自审，未委派新代理或声称独立人工批准。五仓HEAD/branch/remotes不变，已有文件未删除；Runtime全起点文件、固定新旧产物与旧migration保持。没有commit/push/tag/发布。

未执行：真实Provider、完整Tauri页面/系统电源/唤醒、日常库迁移、Keychain、签名打包及含强杀/权限破坏/攻击fixture的历史全套测试。原因分别是本批范围或用户硬性安全条款，影响是本批仅完成原生候选装配/恢复，不构成整项FEAT-155或D4验收。正常停止超时的代码仍保留进程所有权，本次进程均已正常退出。

本批完成后停止，不自动推进页面、真实激活或下一批实施。后续继续围绕两种创建、三种运行目标、页面与既定唤醒/限额内真实验收收敛，系统通知仍延期。
