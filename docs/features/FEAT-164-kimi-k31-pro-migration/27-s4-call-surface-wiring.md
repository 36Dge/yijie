# FEAT-164 S4 全调用面接线与安全离线验证

2026-10-25，Owner明确授权S4实施及仅本地提交、不推送；真实模型HTTP新增0。启动快照 `evidence/s4-start-baseline.json` 保护原工作区620项、两份旧账本及活动S1 App 42项文件。S1—S3源与时序子集已有证据，App、旧隔离历史、平台、完整G3及final仍延期；G2V保持pending，旧PASS仅适用于原来源。

## 审计和源顺序

contract-impact=breaking。市场选择、市场Host及专家的旧封闭模型枚举不能表达新身份，先建立独立v2源及配对消费者；旧v1源、命令名、envelope、selection/expert/knowledge摘要域不变。这里扩展的是known身份，不能据此将旧K3或暂停Kimi解释为可执行。

Contracts `eddc64f95d81c26ca1678cc648d177c081f7904d`先固化45文件，随后Host `9ffcb6f55bb6b2db3aacdee61693063767139ba7`固化12文件，Desktop `704cfdb915b682c4aa3bf3cc62bb33da18f698f2`固化61文件，再由`e4080474e8bd691622cf269e400f8ae4bbcbd041`独立固化目录来源4文件。源清单和可逆保留证明见`s4-*-isolation.json`；Desktop第一批证明单独保存在`s4-yijie-desktop-primary-isolation.json`。无推送、分支、tag、PR、发布；仅创建了detached本地资格检出。

新增market-selection-v2 0.3.0、market-host-v2 0.4.0、experts-v2 0.2.0。Host/Native/renderer精确固定完整commit，同源schema/validator/Rust/Go/TS生成；没有手改DTO或借生成物改变权威。Native私有草案IPC v2此前已引用storage-v2的模型，审计后确认无需额外schema变更。Provider/Broker/Skills不承载主模型身份，继续原协议。9个登记基线离线比较通过；4个新schema测试覆盖已知/未知身份、旧数据与原摘要向量。

## 实际接线与证据

| 调用面 | 本轮实现/核验 | 证据边界 |
|---|---|---|
| 普通新建/续聊/图片/文件 | 原S1/S2显式profile链保持；固定Runtime实际收到K3.1 Pro/max、普通PNG与文本附件投影；S2真实Native/Host边界复验 | 图片和附件只验证本机请求序列化；真实供应商能力未新增验收 |
| 标题 | 修复收集器误拒Runtime正常userMessage started/completed；仅assistant文本作为标题，未知项/工具项仍拒绝 | 固定Runtime返回严格JSON标题通过，无真实模型 |
| 计划草案 | renderer从legacyProfile改为executionProfile；Native草案实际claim/create/turn保存新身份，Host沿原input-only proof | 固定Runtime草案请求/正常resume通过，empty tools、无网络/文件/扩展源policy证明保持 |
| 计划保存/退役 | 修复S3表单valid仍使用旧白名单；保存与可提交判断同用executionProfile | mounted真实组件确认新Kimi可保存、旧K3不能提交；S3五项时序复验通过 |
| 市场/专家 | 配对v2生成与Native cfg；store/model intent传新身份；Host仍经checkModelRequest与原审批、快照、幂等 | Host实际域服务新提交/回执重放、暂停后读取及两类退役/暂停拒绝；Native各自正常重开、snapshot/digest保持 |
| 工具后续 | 固定Runtime读取普通临时note.txt，然后把真实function_call_output送入下一次本机请求 | 相同K3.1 Pro/max；不调用外部业务工具，不使用空操作或替代执行程序 |
| 同源候选/媒体 | 显式ordinary/market/experts/media组合；普通缺省不变；Host允许原Market assembly，独立动态产图仍禁用 | 配置单测通过；ordinary/market来源PASS；experts/media被既有资源pin不一致阻断，实际Worker/媒体未运行 |

候选launcher与Native都校验组合；expert overlay只提供资源，保留FEAT-164标识、端口、Host和数据根。receipt增加组合、worker源码/制品、专家资源槽与媒体adapter摘要，同源重开不重建adapter。Host构建来源固定上述commit，包含可选artifact adapter源；未运行App打包，不能宣称这些打包变化已完成实机资格。

草案私有Config允许动态分配的`http://127.0.0.1:<port>/v1`以避开活动18083 fixture，严格拒绝其它host/scheme/path/query。外部`YIJIE_PERMISSION_VERIFICATION_BASE_URL`环境装配仍精确锁定18083/v1；没有新增公开网络目标或权限。输入限制、native policy proof和0重试保持。

## 辅助调用面的审计边界

实际固定Runtime普通请求仍投影`multi_agent_v1`；effective config的multi_agent为未显式设置，memories=false，review_model未设置。不能声称普通会话已禁用所有辅助能力，也没有为测试开启它们。原生辅助代理、Guardian审批和压缩动态运行本轮未执行；完整TINV-164-04/TCONF-164-04仍NOT RUN。

源审计定位：固定上游`core/src/tools/handlers/multi_agents_common.rs`从当前turn继承model/provider，模型override来自catalog；`guardian/review.rs`优先目录内的review模型，否则当前turn身份，Kimi目录只支持max且无auto_review_model_override；`session/turn.rs`旧模型压缩受comp_hash变化或降context条件约束。当前受管catalog仅K3.1 Pro/MiniMax，无旧K3、override或comp_hash。r2请求构造仍在发HTTP前拒绝kimi-k3。源审计说明选择规则，不能代替动态辅助执行或大上下文资格；不通过触发额外代理/付费调用填补证据。

## 验证结果与纠错

最终干净来源：Desktop e408047 / Host9ffcb6f / Contractseddc64f。`evidence/s4-conformance-final/result.json`为**安全子集PASS**：Host域服务7、固定Runtime4、Native4、renderer4、组合5，全部0skip；最终Runtime6次loopback Responses。`s4-s2-regression-final`为25/2/12/10/1通过，`s4-s3-regression-final`五项通过。完整TCONF-164-04保持NOT RUN，S4 local_evidence仅记录该子集，不宣称完整边界或纵向PASS。

另有202现有前端测试、TypeScript、ESLint、Rust fmt、候选Clippy lib、默认Rust check、go vet、2个既有安全草案单测、Vite前端build通过。前端输出只在资格树`.local/feat164-s4-web-build`，没有写活动App bundle。保留既有全targets Clippy、ChatPage断言、自动三目标和其它来源失败，不混入修复。未运行全量make generate/test或危险fixture入口。

诊断过程保留事实：初版专家回执测试错用市场read接口，修正为原专家read后通过；初版PNG fixture无效，改由标准PNG编码生成普通图片后通过；标题userMessage误拒是真实接线缺陷，已修复；旧草案测试对tool_choice=none的预期与已固定FEAT-156 upstream-tool-choice patch不一致，实际正确组合为auto+empty tools，native input-only proof仍证明工具/网络/文件/扩展均关闭，未改Runtime或放宽proof。测试草稿失败不计为产品PASS。

原Connectors工作区的既有生成物改动使source检查失败，已保留。独立detached `connectors-s4-source`固定251a0e8，资格树symlink指向该检出；原仓和所有改动不变。复核发现旧catalog lock的基线e2792f9与当前Provider投影不同步，且原工作区catalog已有其它需求的新摘要。本轮新增FEAT-164专用catalog来源锁/leaf checker，只引用251a0e8中原60项目录；旧catalog文件/lock/checker全部保留，未混入其它需求摘要。隔离提交的两次apply-check冲突均在写原仓前停止，最终采用专属文件解决。

`evidence/s4-source-results.json`最终ordinary/market PASS；experts/media在原专家manifest `64721b4…` 与Native pin `033689b…`不一致处失败。不得只刷新摘要或重写已审计资源来制造通过。它们需要按资源所属需求完成同源审计与正常构建后，再做本需求组合验收。原pin标记working-tree/revision4247a4f及tree_sha256，不能仅检出该commit就宣称恢复了对应未提交资源；本轮未重包或改写该pin。

## 未完成项与下一步

1. 先独立核对专家资源版本、来源和Native pin，形成可复现且不混入其它需求的候选；补专家/媒体来源、实际Worker及媒体工具链验证。普通/市场source PASS不替代这个步骤。
2. 辅助代理、Guardian/压缩需要适用的安全动态资格；本轮仅源审计/配置观察，不伪造已执行或改变现有功能。完整TCONF-164-04尚未通过。
3. 用户回到电脑后，先通过应用自身正常退出活动S1 App，再从当前不可变来源canonical构建。补亮暗/1180×760/权限、旧隔离历史、正常重开/清理与暂停Kimi/MiniMax回退；日常库不迁移。
4. 完成当前来源G2V、S1—S4完整G3、三项final及freshness。若需要真实供应商资格，必须另有新次数授权；本轮允许新增真实HTTP为0。

旧30元累计预算、2/2已使用请求、14.188544元未知预占与0.139590元保守费用均保留，上界14.328134元。两份账本逐字哈希不变，`.lock`不暂存。活动S1 App与fixture保持原状态；最终保护审计见`s4-preservation-audit.json`，fixture请求仍1。无强杀、权限破坏、攻击fixture、程序替换或真实供应商/商家调用。

治理复核：claims/strict检查PASS，元仓lint及53项test PASS；第一次元仓test发现新增evidence marker缺失，补齐标记后复验通过，初次日志保留。`s4-g3.log`为预期不放行结果，包含当前G2V、前置slice、完整TCONF和平台/freshness缺口，未关闭或绕过门禁。
