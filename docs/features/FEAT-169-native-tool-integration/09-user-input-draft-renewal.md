# 问答草稿在授权重同步时的保留（2026-11-08）

用户要求先查清长时间等待后草稿丢失的原因，再修复；继续复用原生能力，明确权限和敏感输入边界。

## 已确认的源码链路

- Permission Store提前30秒更新最长5分钟的原生权限投影。同租户、旧投影尚有效时使用现有preserveProjection路径；新到期时间不代表权限变化。
- `createChatPermissionLifecycle.authorityKey`包含expiresAt。因此即使tenant/revision/capabilities不变，期限更新仍调用原有dispose→bind流程。
- Native `ChatAuthorizationManager.bind`本就撤销旧context并返回新UUID；`chat_projection`在本工具启用的exact local/demo_fast中使用固定原生身份、租户和授权revision。不能延长旧context或绕过原生重新鉴权。
- `chatStore.dispose/bind/clearAuthority`暂时撤掉context和选中会话。`useUserInput`把context变化一律当成新问题，清空current；ChatPage又把contextId放进问题卡key，二者均导致组件卸载。卡片onBeforeUnmount清掉draft/selected/reveal，所以同一原生问题也丢失未提交答案。
- Runtime原生`Session.request_user_input`继续以原turn的oneshot等待；Host问题请求和pause/receipt还在。问题不是Runtime重新发问或丢失已提交答案。

## 修复边界

`contract-impact=semantic`，仅Desktop进程内临时草稿的生命周期；权威源为Desktop组件/composable及现有权限投影。HTTP/Native IPC/Runtime协议、原生鉴权、审批、数据库和rollout格式不变；Contracts新增schema/pin、数据migration为N/A。保留原Native rebind、原请求查询、原回答提交与取消流程，不新增权限续期器、模型调用或持久草稿库。

仅沿工具既有的exact local/demo_fast启用边界（原生固定身份），在原页面、原聊天、相同有效tenant/revision/能力集合下允许短期挂起现有问题卡；不把新contextId当成新表单。重新绑定期间隐藏输入内容、禁用全部回答操作并关闭敏感字段明文显示。新context必须经现有Native/Host查询，确认同一Runtime generation、request、turn、item与题目定义且仍为pending，才恢复原组件中的内存草稿。

身份/租户/权限revision或能力变化、投影过期/无效、读取权限拒绝、历史只读切换、聊天/页面离开、Runtime generation或问题定义变化、终态/提交均清理；敏感值不进入Pinia共享草稿、localStorage、日志、Host额外状态或自动重发。重确认等待设有60秒本地保留上限，到期只清理未发送UI数据，不替代原生timeout，不自动回答/取消任务。

测试以普通合成数据和正常权限投影/事件重排验证真实组件与控制器；不用攻击fixture、强杀、二进制替换或权限破坏。只运行相关前端检查；若需要真实供应商验证，另申请本任务Kimi额度，不借用之前的3次余额。

## 验证与启动来源

- 修复前，用生产composable和真实ChatUserInput组件复现同权限context替换，合成遮罩输入由原内容变为空字符串（断言FAIL，非仅静态推断）。
- 修复后60项定向前端用例通过；包括真实Permission Store的270秒刷新定时器连续执行两轮，既有ChatPermissionLifecycle的dispose/bind仍各执行，选择、分页和遮罩草稿保持；权限/租户/revision/能力改变、过期、迟到读取、只读上下文、原生generation/request/turn/item/题目或敏感标记变化、60秒重新确认上限、终态和页面离开均覆盖。
- vue-tsc与修改前端文件ESLint通过。未修改Native/Host/Runtime实现或任何公共协议，未运行全量/无关原生测试。敏感值仍只在卡片局部ref中，保留上限只约束重新确认期间；正常等待继续遵循原生可选超时/暂停语义。
- 上一任务把全部仓库提交后，本地候选来源回执仍记录旧HEAD，canonical启动按设计拒绝。通过原generator更新Runtime/Contracts的base_commit及其派生摘要，再冻结配对构建回执；生成DTO/schema、Runtime manifest/binary与源文件哈希未变化。
- Desktop目录精确引用更新到Connectors `06e27b85437bba2b91bbcd2ce43ddb45d4ea7337`：它相对旧`de1fcdf8dabd9b08983bbf907f079db41da437fe`只改AGENTS.md，目录Git对象/工作树字节完全相同；保留exact HEAD与生成比较校验。
- Connectors沿既有compatibleRuntimeWrapperCommits机制登记新包装提交`db3c7b56c390215803449b38fd7599ab4f5715f3`。其`codex-rs`树与原库固定提交`7fd463bcef07f37b0211acd9f62b9f93ea0a4b12`均为`755f32c45a4c30e805e3c7fe1db89dcb4dcc6e41`，工作树无差异/未跟踪库源；原check-worker-source验证通过。未更换库、依赖或工具能力，不跳过来源门禁。

本任务真实验收获批Kimi最多4次请求，独立账本`.local/user-input-draft-renewal-live/20261108-current-task/ledger.json`，旧额度不继承；实际使用2次，均为Kimi K3.1 Pro、HTTP 200；计数器已通过stdin EOF正常结束，剩余2次未使用。


## 真实窗口结果

canonical `start-ui --tool-search-meter`、原日常Homes、实际macOS App，新建隔离工作区`draft-renewal-workspace`和聊天`01a1bbae-3a76-7680-b36d-1fb6d4668fc6`。原生模型一次发出两题：普通自由输入与isSecret自由输入，未设置autoResolutionMs。

- 填写普通合成值，在第二题手动开启明文显示；不提交，按真实时钟等待。
- 等待期间已观察到聊天历史重同步，而问题仍在第2页；非空敏感输入自动恢复遮罩，无须再次填写。
- 草稿填写后334.9秒（超过5分半），模型HTTP计数仍为1。通过实际控件显隐/前后页核对两项原值完全一致；恢复第2题时仍为遮罩。
- 用户式单次点击发送后显示“回答已发送”，问题卡撤下；第二次Kimi请求返回“长等待草稿验收完成”，整轮显示449秒完成。
- 未通过缩短生产TTL、改系统时钟、模拟程序、制造异常或改写模型响应来验收。UI等待期间没有额外模型请求或自动重发。未提交草稿只留在组件内存；正式提交的答案仍遵循原生会话保留语义，不宣称其不落盘。
- 权限改变/失效、读取拒绝和原请求变化通过普通定向用例验证，未对真实用户实施越权或攻击测试。UI实际验证为当前亮色窗口；未扩大为主题/布局改版或全量回归。

实际App和专用服务通过⌘Q正常退出，计数器通过stdin EOF正常退出。原日常入口已恢复，Host readyz=200，运行命令不含验收计数器路由；实际App重开原验收聊天后显示完成记录，旧问题表单未复活。完整证据为`references/user-input-draft-renewal.json`；实现验收阶段未提交；后续用户已明确授权本次Git提交与推送，见下节。

## 本次 Git 提交的来源收口

用户随后授权将草稿续期及相关来源更新逐仓提交、推送。提交前纠正了本地候选回执的自失效问题：user-input/context-window生成器复用本仓其它generator已有的“保留生成基线”方式，并验证该完整commit可解析且为当前HEAD祖先；Host构建回执检查同样使用记录的基线。当前源文件、生成物、消费者副本、产物和所有Host构建输入仍逐字节/摘要比较；源码变化仍需显式生成与freeze。没有放宽不可变发布pin或改动运行时权限。这样正常git commit只推进HEAD时，不会让已经验证的内容再次被误判为来源漂移。

Connectors先提交受审包装引用，再由Desktop精确引用其新commit并同步目录回执；Host提交后再冻结配对构建来源。公共协议、Runtime/库树及问答前端行为不因这次Git收口改变；Contracts和Desktop提交后已直接运行生成/消费者及配对来源检查，536项Host构建输入、基线祖先和精确目录引用均验证通过。此前60项前端与Kimi 2/4的验收仍对应相同问答实现。
