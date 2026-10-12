# FEAT-158 分阶段实施记录

## 授权与当前状态

2026-10-11，用户在需求与设计交付后明确要求“分阶段开始执行158需求，一步步思考，认真落地”。据此按需求包推荐方案开展本地实现，D0产品方案确认。该授权包含必要的正常代码、契约、内容整理、构建与非破坏性测试；不包含Git提交推送、公开发布、付费模型、外部经营服务或生产写入。用户长期禁止的强杀、二进制伪装、权限破坏和攻击fixture继续有效。

整体 `contract-impact=breaking` 保守分类保持；旧包v1/v2及既有普通聊天语义不改变，采用版本化扩展。分阶段用于安排技术依赖与审查，不把局部完成换算成D4。当前D4未完成。

## 阶段与退出证据

| 阶段 | 范围 | 本阶段退出条件 | 状态 |
|---|---|---|---|
| 1 资格与源契约 | 固定原生Runtime同Thread角色切换、共享包v3与专家wire、首个专家审校内容 | 真实固定binary正常无模型资格结果；源/生成一致及focused conformance；内容结构与来源映射验证；明确未覆盖项目 | 完成本地候选阶段，真实模型效果未验收 |
| 2 受管安装与执行 | 同一Skills安装核心支持专家资源且不全局投影；Host指令组合、绑定与快照 | 契约先行的consumer适配、普通技能回归、同Thread持续/移除/恢复的正常验证 | 本地安装、执行与回执链已接通，正在核对独立候选启动 |
| 3 Native与交互 | SQLCipher绑定/快照/引用、扩展双Tab、详情/召唤/胶囊 | 真实Native链路与原有聊天/连接器/模型共存，正常状态和权限反馈 | Native与UI完整发送已接线；正在修复交叉审查发现的边界并做集成检查 |
| 4 完整验收 | 最终构建、全部Must、内容Eval、亮暗/最小窗口/键盘与正常恢复 | 授权额度内一次fresh run完成，结构化复审，无阻断缺陷 | 静态与正常focused检查进行中；真实模型验收未执行 |

首阶段已取得无费用、正常生命周期证据。本机协议请求确认了指令应用/移除语义；真实Provider行为、模型质量和正式安装目录的读取仍需后续产品验收。

## 基线与职责

[实施基线](evidence/implementation-baseline.json)记录开始时各仓分支、HEAD、origin和改动；既有未跟踪需求包来自上轮交付，保留。新工作只进入对应职责仓库，使用现有工作分支，不创建或提交Git状态。

- Contracts：公共包schema v3和独立版本化专家family，普通条目引用v2权威定义，避免复制旧字段独立演进。
- Skills：角色、14模块审校reference、索引、来源映射和良性内容评测；先不改旧bundle pin。
- Host：固定真实Runtime、隔离临时HOME及工作目录的正常资格；不改Runtime核心或用户二进制，不读取日常历史。
- Desktop：先核查发送/模型/连接器/草稿/受管目录的真实边界；源契约稳定后接消费实现。

## 本阶段实际调用

真实模型/embedding：0；外部MCP元数据/业务：0；WorkBuddy修改：0；生产写入：0；Git提交/推送：0。固定Runtime资格中实际有12次正常synthetic turn、14次仅本机Responses请求；这是正常协议测试，未调用真实Provider或计费模型。

无模型资格允许读取新建隔离运行自身的元数据并正常EOF退出。若正常退出超时，保留进程及位置并报告，不追加强杀。命令、结果、摘要和资格限制随实际发生追加，未执行项不填PASS。

## 阶段1历史记录

以下至“阶段2与3当前实现”之前保留阶段1时点；其中“尚未”“最终”只指当时。当前实现、摘要与验证以下方阶段2/3为准。

### 原生资格第一轮结果

1. 无模型、无turn的固定Runtime资格确认了一个限制：空Thread尚无rollout，unsubscribe后resume返回no rollout found。0 HTTP、0 turn、0付费；正常EOF退出0。这不是专家切换PASS，也不是需要通过补丁掩盖的失败。新草稿只保存Native选择，首发才创建Thread；产品不得预创建空Thread后用切换逻辑套入角色。
2. 后续使用同一真实固定Runtime与本机普通Responses测试服务，完成3次正常synthetic turn。同一Thread实际发出的instructions依次精确等于完整普通base、base加短role、完整普通base；保持never/readOnly/networkAccess=false，正常EOF退出0。该结果证明原生组合与正常切换协议，不证明真实Provider/模型效果。
3. 原生session_meta只记录最初base，不能作为当前专家状态权威。冷恢复、模型切换、权限与市场重绑都必须从已确认快照显式投送当前完整base；不能从历史推断或省略字段。

报告：[无turn限制](evidence/runtime-no-turn.json)、[本地Responses协议资格](evidence/runtime-local-responses.json)。真实模型与受管资源读取资格仍分别记录，不把普通协议测试等同D4。

4. 普通reference读取资格：同一真实Runtime通过实际暴露的 `exec_command` 读取隔离目录中、工作空间外的一份自建普通文本，返回预期文本且命令退出0；权限保持readOnly/never/networkAccess=false。该结果不证明正式app_data安装目录全部可读。[报告](evidence/runtime-reference.json)。
5. 正常退出重开资格：已应用专家后EOF退出0，在同一隔离HOME重启真实Runtime、显式投送完整专家base后恢复原Thread，随后移除专家；两个进程均正常退出0，实际请求中的base符合预期。[报告](evidence/runtime-reopen.json)。

Runtime SHA-256固定为 `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`，manifest为 `8b86a1a661f50beda1e0a0c96f81ddbdf959a9a07c2e756cc4b9b0eabc053b27`。没有改Runtime源码、替换binary、读取用户日常对话或故障退出。无turn报告的passed=false保留，不把已发现的空Thread限制改写成通过。

实际UI核对还确认：当前连接器入口已进入“+”菜单，所选项在正文行内展示。专家胶囊仍按PDF放店铺授权右侧，不恢复已经移除的旧连接器按钮；03、AC表与机器文案已同步这项工程校正。

### 源契约与内容已落地（阶段1时点）

Contracts新增 `compatibility/experts/`、共享包schema v3及独立生成/消费脚本。8个安全UI命令与5个私有方法已定义，私有方法复用现有Native拥有的Host管道。普通Skill引用v2权威定义；旧schema与旧pin不被改写。专家快照和知识清单摘要由同一源生成JS/Go/Rust实现，不在消费者另造算法。

最终Contracts `source.lock.json` SHA-256为 `6b5a8da6c749cad5a28e75ddf9432dbc50ddcdc984b595a31c5b24d2d7861d52`；Desktop、Host、Skills均通过canonical同步检查。它是 `local_worktree_candidate / release=false`，不是不可变发布commit。候选说明见兄弟仓 `yijie-contracts/docs/experts-v1.md`。

Skills专家内容落在 `plugins/yijie-desktop-skills/experts/jd-ops-expert/skills/jd-ops-kb/`：短ROLE、14模块42场景、索引、原稿行号映射、算例、12条良性内容Eval数据。资料缺失、冲突和待核政策保留状态；排除原稿中的不当建议、虚构资历、跨平台承诺及WorkBuddy专有设置。结构检查不等于真实模型Eval。

候选打包继续使用现有 `package-desktop-skills.mjs`，显式v3源输出到 `dist/skills-experts-candidate`，共38旧技能加1专家；38个旧归档字节相同。仅本地实施授权，专家公开再分发未确认，desktop-release分支正常拒绝此候选。完整审校见兄弟仓 `yijie-skills/docs/provenance/FEAT-158-jd-ops-content-review.md`。

| 当前候选内容身份 | SHA-256 |
|---|---|
| authority.json | `acf0d2959e1b332d2050b3893eb4927af19b7adb2e73d5db492377df1763931d` |
| bundle-manifest.json | `156fa3da100f82985087637ea3e94138d1f6ff813fedc8a4275b0dcad591e355` |
| source tree | `2fae182bcdbf41e2a6f7418fa1e64d94282a851c5cc0550feb213dac8ad4fef6` |
| 专家ZIP | `d56ce92e8b7559a5b5e04805c2b99c82dd770c3b70dc61169fd18f1700a04799` |

这些摘要只用于受信本地装配的精确固定；renderer不能上传任意目录、hash、ROLE或authority自证为可信内容。任何内容或源锁变更都须canonical重建并复核。

### Native基础与当前边界（阶段1时点）

新增0034迁移仅向前添加绑定、绑定操作journal和原market submission下的专家快照表，不另建消息投递队列。迁移已用正常内存库证明旧会话/消息/迁移ledger不被回写；日常writer仍保持原有最高33路径，未打开实际日常SQLCipher库。

绑定store运行于原SQLCipher worker的调用方事务：requested与confirmed分开，pending/unknown保留旧ref和revision；成功才+1，拒绝不增加。完整Host apply payload先持久化，回执必须匹配原Host实例、agent session、native thread、ref和revision。相同operation重放返回原结果，跨会话或不同意图冲突；unknown不能提交新变更。`updated_at`为壁钟记录，跨operation顺序以revision为权威，不能按时间戳替代CAS。

10项正常store测试加1项真实迁移测试通过。测试只创建内存库、普通记录和正常事务rollback/commit，没有强杀、攻击资源或权限故障。独立只读复查未发现当前存储范围阻断缺陷；该结论不覆盖尚未接通的命令/执行入口。

**尚未接通**：8个Native命令及ACL、受信候选目录与准备回执、完整NativeSubmitPayload进入原消息/outbox事务、同一dispatch和新私有receipt恢复、所有普通发送/模型/权限变更入口的互锁、资源引用与升级/移除门禁。当前只有快照表和源生成算法，不宣称已做到产品发送的原子冻结。

UI候选使用显式local/demo_fast开发开关，默认关闭；缺少Native命令必须显示不可用。首阶段不会把专家选中状态交给旧普通submit，也不会显示虚假的专家生效。完整召唤、快捷问题回填、持续绑定和胶囊移除留待真实链路完成后接线。

### 检查范围与后续阶段（阶段1时点）

已通过的源与基础检查：Contracts 9项Node、5项Go、3项Rust及类型/strict schema/登记基线检查；Skills 11项Node及16条合成数据格式检查（其中12条是专家数据）；Native 10项store+1项迁移、cargo fmt、全目标clippy。Host `go build ./...`、10项FEAT-158正常测试、2项原FEAT-157普通路径回归及1项实际候选包临时安装/解析检查通过；ROLE1730 bytes、索引4420 bytes、全局投影0项。完整Host命令和限制见兄弟仓 `yijie-agent-host/docs/experts-host-candidate.md`。不把测试数量相加当作AC数量。

Host候选复用现有market grant/submit及串行锁，完整expert snapshot进入原HMAC和原operation回执，不能通过普通submit丢弃专家身份。schema9仅 `WithExpertStorage` 显式开启，`cmd/desktop-host`未修改；旧writer拒绝读取9。普通start/resume在没有专家上下文时保留旧base行为。受管安装和receipt复用原核心；专家升级/卸载/禁用目前保守禁止，引用释放门禁与unknown正常恢复出口仍待补齐。

未运行含用户禁止动作的既有全量测试入口。源码检查发现部分既有测试包含权限故障、假可执行文件或攻击性fixture；按用户硬性条款使用已审查的正常focused测试与静态编译。影响是这些故障专项和全套回归没有本轮PASS证据。真实Provider/内容质量、正式app_data可读性、全部权限模式、Native亮暗/1180×760/键盘、一次完整fresh run均未完成。

下一阶段依赖顺序保持不变：

1. 完成受信本地候选装配，Native通过原Skills核心准备资源并验证真实安装receipt，落实引用保留/移除互锁；保持38个普通技能路径。
2. 把完整专家wrapper纳入原Native admission、消息/outbox事务和dispatcher，使用新family私有grant/submit/read；特征关闭或旧reader不能把专家投递降级成普通投递。
3. 串联已有线程切换、正常冷恢复、模型/权限/市场重绑；处理未知apply的正常恢复出口。无rollout草稿首次发送才创建Thread。
4. 接通召唤返回上下文、三条预填问题、胶囊及移除；做正常本地E2E，再固定实际模型验收范围和额度，完成T01–T10。当前不申请尚未准备好的付费验收。

Feature保持active，D4保持NOT RUN。首阶段交付的是可审查、可重复本地验证的代码与资源基础，不是可日常使用的完整专家功能。


## 阶段2与3实现记录（历史时点）

源契约目前为8个Native命令、9个私有方法。新增资源状态/准备/移除/原操作查询，继续走已有Native拥有的Host管道。`BindingView.managed`明确区分从未进入专家family的普通会话与显式无专家、revision=0的受管会话；后者仍走完整专家wrapper，避免移除或首次选择失败后丢失历史身份。Renderer不接受资源路径、ROLE或摘要作为可信输入。

当前Contracts源锁为`762fa86dedad71afef0c2a0e37d7945202ca961cdddb6e7c188aaa6c7d657259`，Skills authority为`8cefd1e0fc0c80739018b37293e44550dd2b0c6a0fdb96f7ea08b28e7e356d3b`。manifest、source tree与专家ZIP沿用上表；普通38个技能归档未变化。三消费者同步检查通过，仍为`local_worktree_candidate / release=false`。

### 资源与Host

复用现有Skills安装、校验、receipt与卸载核心；专家候选使用独立打包资源槽`skill-packages-experts`，安装仍落同一受管机制的`skills/installed`。专家资源不会进入全局Skills根、启用投影和普通自动升级。Native校验目录/authority/清单，Host使用编译固定清单，执行前解析已安装真实receipt、ROLE和索引，不内联整份知识库。

Host schema10增加资源操作恢复，显式writer允许9→10；新版feature-off reader可读取9/10而不创建桶或升级，普通聊天不因关闭专家开关而失效。旧binary仍不能读新存储，不能宣称支持二进制回滚。绑定和发送复用原market授权、grant、单次消费、串行锁与HMAC，重新开始、恢复、模型/权限/市场重绑都显式组合完整普通基础指令和当前已确认专家。专家绑定不自动选连接器，不改变批准策略。

Native在SQLCipher35持久保存资源操作与原请求：先commit再发送；超时/unknown只查原操作；空Host status不能清除未知状态。资源移除检查所有本机保留会话绑定、历史快照与pending操作；新版prepare也不能覆盖被旧版历史引用的同安装目录。现阶段引用仍在就明确ResourceInUse，不另造版本缓存或悄悄删除知识。

### 会话、发送与交互

8个Native命令已注册，复用现有task/plugin能力租约与market admission锁。专家绑定日志保存原Host、Thread、权限、模型、连接器快照，成功receipt才推进revision；未知时保留原有效绑定并阻止新修改。普通模型切换、权限调整与删除也受未完成绑定互锁。空草稿只在内存选用，首次发送才创建Runtime Thread。

完整专家wrapper进入既有消息/outbox/market submission同一事务，原操作重放优先于新安装检查；dispatcher复用原队列并带原专家快照走私有grant/submit/read。关闭开关后不执行新专家消息，但可只读查询原inflight回执；普通消息不会被冻结专家消息饿死。已进入专家family的会话不允许回退裸普通发送。

UI已接通扩展双Tab、卡片与详情、三条只预填快捷问题、召唤与会话胶囊。侧栏召唤进入新草稿，“+”菜单召唤返回原对话，保留原文字/附件/模型/工作空间。胶囊位于店铺授权右侧；移除仅改变之后的指令，不清历史或承诺失忆。未知提交保留完整原operation/wrapper，仅允许原查询。原历史消息尚无装饰性专家徽标，不能按当前绑定倒推历史专家；Native原消息快照和资源引用已保留。

交叉审查发现两处异步UI边界：离开会话后晚到的已受理回执可能遗留可重复发送草稿，召唤等待中离开页面可能被旧结果导航拉回。已修复并以正常deferred回归验证：保留原完整wrapper与已受理receipt直到草稿按operationId消费；导航/组件离开取消过时预填与跳转。专家发送receipt也已补对原持久Host nonce核验，正常数据库重开测试通过，恢复认原Host而非重启后当前Host。

### 本地装配与当前检查

专家默认关闭，显式`YIJIE_EXPERTS_ENABLED=true`仅在local/demo_fast和现有模型/连接器/权限机制同时有效时开放。候选overlay使用`com.yijie.ai.feat158-local`与“易界 AI FEAT-158”，独立app_data（含SQLCipher及Skills安装）、Host/Runtime home和Host生成产物；候选默认Host端口18158。单实例锁仅在精确编译identifier与本地专家gate同时成立时独立，日常锁不变。首次候选目录不存在已只读核对；首次packaged窗口已正常启动，见后文实际记录。共享Provider密钥仅作为既有只读输入，不在证据中输出；预算仍0，浏览/准备不发送turn。

当前通过的normal检查：Contracts11项Node、5项Go、3项Rust与生成/消费检查；Host18项FEAT158（含3项实际候选包检查）、2项普通market回归、构建与focused vet；Native12项binding store、8项resource journal、原有feat158发送/迁移/技能回归、全目标clippy、独立锁正常生命周期；launcher20项正常测试。UI已通过类型、lint、构建与多组聚焦检查；最终异步修复后store/summon14项、ChatPage/chat.store6项、Host身份精确Rust1项、类型/ESLint/clippy均通过。数量只作覆盖说明，不能合并换算Must已通过。

测试曾真实发现并修正回执状态期望、脚本旧字面断言与原managed字段缺口；失败记录不当作PASS。一次Vitest选择未排除`.local`历史副本，读到了历史脚本测试；最终使用明确排除本地副本的当前仓命令重跑。所有测试仍遵守安全条款，不执行强杀、权限破坏、伪装binary或攻击资源。

接下来完成候选源码冻结校验、canonical打包与独立窗口检查；在可评审的本地结果就绪后再申请明确上限的真实模型验收。尚未执行真实Provider、内容Eval、安装目录全权限模式读取和完整产品fresh run，Feature仍active，D4保持NOT RUN。


### 首次独立应用观察

canonical `YIJIE_EXPERTS_ENABLED=true pnpm tauri:demo-fast:app`已完成未签名debug `.app`打包，实际启动独立identifier与18158 Host；日常App继续运行，没有被关闭。窗口免登录进入，默认技能显示原38项，专家Tab显示唯一京东专家，详情含真实范围/版本及三条预填问题。

实际资源prepare首次失败：页面传完整ExpertDisplay，严格ExpertSelection只允许ID/version，client在Native invoke前即拒绝多余展示字段。两人独立只读诊断与generated validator普通对象复现一致；新安装核心操作日志仍为空，没有安装和模型调用。此前UI mock测试未覆盖此实际边界，因此不宣称整链已通过；正在补最小投影与真实validator回归，不放宽契约。

本次通过应用菜单Quit正常退出，launcher exit=0，候选App和Host进程均已结束。CUA在Quit后的AX读取因窗口消失超时，不作为退出失败或采用强杀的理由。后续修复后将重新canonical构建与检查。实际记录见[evidence/phase2-local-checks.json](evidence/phase2-local-checks.json)。


### 第二次独立应用观察

投影修复后27项含真实validator的正常回归通过，再次canonical打包启动。实际prepare成功，既有安装核心只有1项完成操作；安装ROLE摘要为`7173636f07506ce525c15af7b6fc29b564536c3be41798ac614714a26b4c70f0`，receipt的RuntimeVisible=false，未投影为全局技能。召唤返回新草稿，保留已输入合成文字和Kimi-K3模型，焦点落输入区，未创建消息。

窗口拖到1180×760（截图2360×1520），输入区与专家胶囊无重叠。实际键盘进一步发现两个UI细节待最终重建：按钮原生appearance未重置，以及Naive确认框初始焦点落“替换文字”而非“保留”。显式点击保留确实保留文字。局部Web Inspector颜色覆盖可触发data-theme=dark，但关闭检查器即还原；尚不据此声称完整深色视觉通过，没有修改系统主题。第二次也通过App菜单Quit退出，exit=0，无候选进程残留，Provider turn仍0。


### 第三次独立应用与当时待办

最终UI修正后11项测试、类型与ESLint通过，第三次canonical debug打包成功。实际WebView已验证确认框初始焦点落“保留当前草稿”，按Return保留原合成文本、选择专家并聚焦输入区，没有自动发消息。按钮恢复项目主题样式，正常重开仍显示资源已准备；没有重复安装。

在同一最终构建下检查了1180×760逻辑窗口（2360×1520像素捕获）的亮/暗详情和输入区、搜索空状态及清空恢复、Tab可达移除按钮和Return移除。深色通过Web Inspector自带Color scheme覆盖并分离检查器进行，只改变当前候选WebView媒体环境，没有改系统设置或伪造DOM样式。原草稿文字与模型保持，全部页面观察仍为0模型turn。

继续验证普通自建文本附件时Mac锁定，文件选择尚未完成；已请求用户手动解锁，不尝试绕过。候选App当前仍运行，不能称本轮最终清理已完成；前两次正常Quit均exit=0，日常App未受影响。

本地可审评结果已具备，已提出下一阶段最多18条用户发起的真实模型测试消息（现有Kimi/MiniMax、专家知识片段与合成数据、无连接器业务调用）的明确授权请求。收到明确答复前模型额度仍0。最终Must、真实知识Eval、实际安装目录全部权限模式与D4仍未完成。当前源码指纹见[implementation-source-snapshot.json](evidence/implementation-source-snapshot.json)，运行与构建摘要见[phase2-local-checks.json](evidence/phase2-local-checks.json)。


## 阶段4：跳过锁屏步骤后的审计与补齐

用户明确继续完成FEAT-158内部未完成需求，并先跳过需要屏幕解锁的实现和验收。本阶段未使用CUA、没有启动或关闭候选App，没有调用真实Provider或外部经营服务。基线复核确认各仓HEAD和上阶段源码指纹没有外部漂移，见[non-screen-audit-baseline.json](evidence/non-screen-audit-baseline.json)。源码审查按Host、Native、UI交叉分工，根代理复核新增恢复与整合边界；未把机器或代理审查当作Owner发布批准。

### 已落实的缺口

- **绑定未决的显式恢复**：新增安全Native `chat_expert_binding_recover_v1` 与原管道 `expert_binding_recover`。原Apply先取自Native日志；当前外层身份授权此次恢复，原完整payload用于HMAC及receipt核验。原Host未收到与已经pending/unknown均沿原ID处理；终态先返回。保持原ref、模型修订、权限、会话/Thread及Host nonce，在空闲、无审批/未知turn/计划预约条件下正常重新应用完整配置，不发消息、不补发旧连接器授权。
- **资源未决的显式结束**：新增 `experts_operation_recover_v1` / `expert_resources_recover`。只观察原Skills日志，或在既有mutation lane及operation锁内明确终结未开始的原ID。对于正常重开已由核心完成回滚、无执行者且无事务残留的reserved记录，也保留原fingerprint原子写入拒绝终态；晚到同ID不能重新执行。恢复不安装、不移除、不把当前文件存在当原操作成功，不另造安装器。
- **当前授权回包**：绑定查询即使Host返回错误并回退到原本地记录，也统一在返回数据前重新校验当前Native task.read。恢复落原回执与向UI回包分开：context变更不能伪造成功或暴露旧授权数据。
- **异步UI一致性**：保留/替换草稿、更换专家、移除/恢复资源确认都绑定原路由/身份/context并在失效时销毁。资源明确成功后清除旧“待确认”；失效读取代际和同原ID终态保护阻止晚到目录/原调用把成功倒退为pending。未知恢复失败仍保留原请求，不生成替代ID。
- **实际资料与普通附件**：固定Runtime已补实际安装资料的三模式只读资格；普通自建文本附件已通过原有prepare/store/materialize及专家wrapper冻结，正常数据库重开后仍按原请求重放且只有一条快照。
- **canonical打包入口**：发现专家资源同步脚本的`--package`分支传了不存在的相对源路径，修正为现有`plugins/yijie-desktop-skills/experts/bundle-source.json`。使用原packager重新打包并核对，38个原技能、专家archive和manifest字节保持；只有追随新源契约的authority来源摘要变化。

源契约先于实现生成同步，当前100个定义、10条Native命令、11条private方法，仍是breaking的本地未发布候选。普通旧族源、旧FEAT-156构建pin不改。Native schema35 / Host schema10沿用现有扩展，不为恢复增加新表、第二队列或新权限。

### 本阶段验证结果

| 范围 | 结果与边界 |
|---|---|
| Contracts | 12 Node、5 Go、3 Rust，vet/clippy及三消费者同步通过；四个登记基线JSON Schema结构检查通过，不能替代语义审核 |
| Host | 最终源码24个FEAT158正常顶层测试（包含真实候选包，无skip）、2个旧市场回归通过；新增恢复6个顶层/14个叶子race测试、vet及`go build ./...`通过 |
| Native | 29个专家store/resource/command测试、14个FEAT158迁移/预约/投递/附件测试、9个普通market回归通过；fmt及全目标clippy通过 |
| UI | 最终8个expert API/store/component/gate文件共50项通过；ChatPage/chat.store定向7项另有通过记录；完整lint、Vue类型和Vite构建通过，既有500 kB分块警告保留 |
| 资源 | 实际安装回执与26个文件摘要先验通过；原canonical打包+资源同步/检查通过，不触碰当前安装文件 |
| 文档 | 需求包strict结构、D0、声明审计及元仓lint通过，D4未声明通过 |

固定Runtime三模式成功运行各4个合成turn、5个localhost Responses请求，均真实调用原生exec_command只读实际M03文件，普通→专家→普通完整base走同一Thread，实际policy/reviewer/sandbox匹配Host模式，正常EOF退出码0。首次三轮中文marker判断因ASCII转义误判为失败，保留原报告后修正比较并重跑；含失败轮本阶段共21个合成turn/27个本机HTTP请求，真实模型请求0。它证明有限协议与文件读取条件，不证明模型角色质量、全部知识条目、auto-review决策或真实产品恢复。

新增附件测试前两次断言使用了UI字段名，按既有Host生成类型修正为`attachment_id/name/context_chunks`后通过，未改变原材料化实现。一条额外测试筛选命中0项未计PASS覆盖；预约互锁的3项实际位于已通过的14项中。首次手动完整权限链检查遗漏launcher的scheduled-daily选择，被旧不可变pin检查正确拒绝；按canonical gate和重新审查冻结后核验，不放宽检查器。详细命令与全部范围见[non-screen-audit-checks.json](evidence/non-screen-audit-checks.json)。

### 当前来源和下一阶段边界

本阶段最终源/构建摘要在上述JSON逐项记录；原phase2-local-checks与前三次运行仍作为历史证据保留。Host构建候选经显式重新冻结，仍`release=false`；源码未提交、未推送、未发布。最新工作树指纹在[implementation-source-snapshot.json](evidence/implementation-source-snapshot.json)，上阶段原指纹另存[implementation-source-snapshot-phase3.json](evidence/implementation-source-snapshot-phase3.json)。

需要解锁的系统文件选择、更新源码后的视觉/键盘/产品恢复fresh run及候选App最终正常Quit按用户要求**跳过**，没有通过其他UI方式绕过锁屏，也没有强杀。真实模型及固定知识Eval尚未得到此前额度请求的明确答复，额度仍0；完整Must/D4保持未完成。平台政策官方逐项核验及公开再分发也没有宣称完成。本轮无需屏幕即可落实的恢复、异步一致性、授权及普通资源/附件工程缺口已完成；进入真实验收时需使用当前最终构建，不能拼接前三次旧构建冒称同轮通过。

## 阶段5：真实模型与功能审计结果

用户已解除屏幕限制、授权18条真实模型消息，后续明确跳过外观。已完成审计修复、正常定向检查及A/B隔离、解绑、历史-only资源守卫、重绑与MiniMax正常冷恢复；原生/Host/焦点与内容0.1.1修复、旧运行失败事实均见[08](08-real-model-audit.md)。18/18消息已用完。固定内容评测未全部通过，AC-007=FAIL，Feature保持active、D4未通过；未执行内容修订后的新付费轮，不把功能链通过或23/23引用可定位当作全部内容Must通过。
