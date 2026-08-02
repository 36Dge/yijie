# FEAT-126 需求与验收标准

> 段成威已于2026-08-01通过G1，并于2026-08-02通过G2及当时的G2A。LIA-126-002复审确认immutable candidate允许任意`input`，且canonical conversation fixture把`input.text`写入Public Tasks并在response回显；这与本需求的content-free-only边界冲突。原G2A结论保留为历史事实，但继续实施所需的G2A readiness现已进入DEC-126-023复审；S4–S6均为Conditional，G3 Partial，G4/G6 Pending。本轮未调用MiniMax或修改candidate。

## 1. 用户与场景

| 角色 | 权限/租户 | 场景 | 期望结果 |
|---|---|---|---|
| 已授权 Desktop 用户 | 已认证；当前 tenant 有 `task.create`，项目上下文有效 | 从新建任务入口提交纯文本 | 一次创建一个 session 并进入可恢复对话 |
| 历史查看者 | 已认证；当前 tenant 有 `task.read` | 打开任务记录并选择 session | 先看元数据，点击后才加载该 session 正文 |
| 只读/无创建权限用户 | 有 `task.read`、无 `task.create` | 深链 `/chat` 或尝试发送 | 服务端/路由 fail closed，不出现可提交假入口 |
| 无读取权限或跨租户用户 | 无 `task.read` 或 session 不属于当前 tenant/user | 猜测 session/task ID | 返回不泄露存在性的拒绝/不存在语义，正文不加载 |
| 本机同一 OS 用户的多租户账户 | tenant 可切换 | 切换租户后查看本地列表 | 立即清空旧投影，按 owner+tenant 隔离，不短暂闪现旧数据 |

## 2. 业务规则

### 2.1 新建任务与 composer

| Rule ID | 规则 | 来源/确认人 | 优先级 |
|---|---|---|---|
| BR-001 | `/chat` 无活跃 session 时展示“易界AI”、稳定可访问名称的多行输入框、项目入口、权限审批入口和新增发送按钮 | 用户需求 | Must |
| BR-002 | composer 和后续 turns 只接受文本；不渲染附件、图片、模型、推理强度、语音入口及其隐藏快捷路径 | 用户需求 | Must |
| BR-003 | 拖入文件、粘贴纯图片或其它非文本数据不得上传/读取；保留文本粘贴并用非阻断提示说明“当前仅支持文本” | 用户需求细化 | Must |
| BR-004 | 空白输入、项目无效/未选、permission policy 未就绪、Runtime 未 ready 或当前 turn 活跃时发送禁用，并给出原因 | 安全/可靠性要求 | Must |
| BR-005 | 键盘语义为 `Enter` 换行、`⌘Enter` 发送；中文 IME composition 期间任何 Enter 都不得发送 | 生产级 macOS 交互 | Must |
| BR-006 | 点击发送必须用 client request/idempotency key 去重；双击、超时重试、窗口重复事件不能产生第二个 session 或首 turn | 可靠性要求 | Must |
| BR-007 | 项目入口选择既有本地目录作为 canonical `cwd`/上下文边界，不等同于在 composer 添加附件。用户明确授权 Runtime 在该根目录内进行只读访问；Runtime 为回答而读取并发送给模型处理的文件片段属于外部模型数据处理，必须在选择器中披露，不做后台全量索引/上传；首次及后续 turn 均要求有效项目 | 用户截图 + Host contract + 隐私边界 | Must |
| BR-008 | 权限审批入口显示当前 session 的有效策略和作用域；UI 不得扩大服务端/Host 权限。本期固定 read-only/deny，不提供权限提升或伪装可写 | 用户需求 + 安全边界 | Must |
| BR-009 | 不显示模型或 reasoning effort 选择；provider/model/effort/summary 由已批准配置控制并可审计 | 用户需求 | Must |
| BR-010 | local DB 事务成功保存 session、首条用户消息和 outbox 后进入稳定 session 路由；DB 失败不跳转并保留输入；Host/模型后续失败在会话页可恢复 | 用户流程 + durability | Must |

### 2.2 对话流

| Rule ID | 规则 | 来源/确认人 | 优先级 |
|---|---|---|---|
| BR-011 | 活跃会话采用单一消息滚动区 + 固定 composer + 项目/session 导航区，不显示右侧上下文面板 | 用户“极大精简”要求 | Must |
| BR-012 | 路由候选为 `/chat/:sessionId`；直接打开时先做 identity/tenant/resource check，再加载元数据与首批消息 | 深链与安全要求 | Must |
| BR-013 | 用户消息、模型消息、处理中、完成、失败和中断需文本/图标双重区分；流式增量按 turn/item/sequence 去重并 durable append | 用户需求 + SSE 语义 | Must |
| BR-014 | 用户消息不提供产品级复制或二次编辑；模型结果不提供复制、like、dislike、分叉或代码块一键复制；系统原生选择/`⌘C` 保留 | 用户需求 + 可访问性细化 | Must |
| BR-015 | 会话页不提供页头“切换置顶”；session 置顶只存在于任务记录菜单 | 用户需求 | Must |
| BR-016 | “不提供显示/隐藏侧边栏”指不新增 Chat 二级侧栏显隐；保留 FEAT-124 全局 240/72 App Shell 收起能力 | 用户需求 + G1 产品决策 | Must |
| BR-017 | 用户处于底部阈值内时自动跟随流；用户上滚后停止抢夺位置，并显示回到底部按钮；点击后到最新消息并恢复跟随 | 用户截图 | Must |
| BR-018 | 回到底部按钮只在离底部超过候选 96px 或有未读增量时出现，位于 composer 上方且不遮挡内容，具有“回到对话底部”名称 | 生产级交互 | Must |
| BR-019 | 每个模型 turn 可显示折叠处理入口；运行中、完成、失败、中断显示对应状态和持续时间，默认终态折叠 | 用户截图 | Must |
| BR-020 | 处理区必须以纯文本展示固定 Runtime/model 实际提供的 raw reasoning，并标注“模型推理记录”；不得声称完整、稳定或等同模型全部内部思维。不得把内容当 HTML/Markdown、命令、tool、approval 或权限授予；不得进入日志/遥测/审计正文 | 段成威 2026-08-02 明确变更 / ADR-0016 | Must |
| BR-041 | reasoning-enabled turn 若没有至少一个非空 raw reasoning item，或 stream gap/invalid/completion conflict 导致内容不可验证，则该 pin/turn 的 reasoning 能力不通过验收；不得用 answer、伪造文本或仅状态/时长冒充，相关 feature flag 不得通过发布 Gate | 段成威 2026-08-02 明确变更 / ADR-0016 | Must |
| BR-021 | 一个 session 同时最多一个 active turn；活跃时发送按钮切换为可访问的“停止生成”，中止等待唯一 terminal event 后才允许下一 turn | Host 现状 + 恢复要求 | Must |

### 2.3 任务记录与标题

| Rule ID | 规则 | 来源/确认人 | 优先级 |
|---|---|---|---|
| BR-022 | 首次加载只读取 session 元数据；点击 session 后才加载该 session 历史，快速切换时旧请求不得覆盖当前选择 | 用户需求 | Must |
| BR-023 | 排序为置顶组在前且按 `pinned_at DESC`；未置顶按 `last_activity_at DESC`；相同时以 `session_id DESC` 稳定排序。重命名不更新活跃顺序 | 用户“倒序”要求细化 | Must |
| BR-024 | session 菜单只提供重命名、置顶/取消置顶、删除，不保留隐藏菜单项或快捷键 | 用户需求 | Must |
| BR-025 | 标题在首轮成功后由模型异步生成，不阻塞回答；生成中显示“新任务”，输出必须转单行纯文本并限制 40 个 grapheme；失败使用首条文本的安全截断 fallback 并允许一次受控重试 | 用户需求 + 可用性/成本 | Must |
| BR-026 | 人工重命名去首尾空白，1–80 grapheme，不允许控制字符；人工标题优先级高于迟到的模型结果且后续不被自动覆盖 | 用户需求细化 | Must |
| BR-027 | 删除前显示 session 标题、“永久删除、无法恢复”和明确影响；确认后在单一事务中物理级联删除 application DB 的 messages、turns、已批准持久化的 reasoning records、cursor/outbox 与 session 行；成功无撤销 | 用户明确要求 + ADR-0014/0016 | Must |
| BR-028 | 删除当前 session 后选择排序上的相邻 session；无剩余 session 时回到新建任务态。运行中删除采用“先确认、停止并等 terminal、再删”，任一步失败均不谎报成功 | 失败恢复要求 | Must |
| BR-029 | 物理删除不删除项目目录；必须清除独占 Runtime thread tree、Host bbolt/replay 与 Desktop rows/WAL，只留 content-free receipt。即使完成也只能承诺当前应用受控 live store 中不可重开/恢复，不得声明“全部磁盘痕迹已删除” | 数据边界 + ADR-0014 Accepted | Must |

### 2.4 聊天项目

| Rule ID | 规则 | 来源/确认人 | 优先级 |
|---|---|---|---|
| BR-030 | 项目显示为本地目录的安全引用与用户可读名称；保存 canonical path、bookmark/授权状态，不把路径放入 URL、日志或遥测 | 用户截图 + macOS 安全 | Must |
| BR-031 | 项目菜单只显示置顶/取消置顶与移除；不显示 Finder、编辑、归档等截图中未要求的 Codex 项 | 用户需求 | Must |
| BR-032 | 项目置顶组按 `project_pinned_at DESC`，未置顶按 `last_used_at DESC`，使用稳定 ID tie-break | 倒序一致性 | Should |
| BR-033 | “移除”是从可选项目列表移除引用，不删除磁盘目录或 session；原 session 仍在任务记录并显示“项目已移除”，新 turn 前要求重新授权/选择有效项目 | 最小破坏原则 | Must |
| BR-034 | 失效、移动、无权限或 symlink 目标变化的项目必须 fail closed；重新选择后才可新建/继续 turn | 路径安全 | Must |

### 2.5 授权、Public Tasks 与数据

| Rule ID | 规则 | 来源/确认人 | 优先级 |
|---|---|---|---|
| BR-035 | Public Tasks 从匿名 legacy 语义迁到 user bearer + untrusted tenant selector + server-authoritative membership/RBAC/resource/action check；不得信任 body `tenant_id` | ADR-0012 / FEAT-125 | Must |
| BR-036 | `task.create`、`task.read`、`task.rename`、`task.pin`、`task.delete` 等 action 的服务端规则必须明确；未知 action/资源默认拒绝 | 安全治理 | Must |
| BR-037 | list/get/update/delete 只能触达当前 identity+tenant 授权资源；跨租户 IDOR 的拒绝不得泄露目标存在性 | 安全治理 | Must |
| BR-038 | FEAT-125 的 host-profile + ingress 双隔离在新契约、consumer migration、安全测试和 activation 证据齐全前继续有效；不得因 Desktop 本地对话完成而提前开放 legacy route | ADR-0012 / FEAT-125 | Must |
| BR-039 | conversation data 按 OS user + authenticated user + tenant 隔离；切换账户/tenant 先清空内存与请求，再加载新 scope | 数据隔离 | Must |
| BR-040 | 云端存储后续通过 versioned storage port/migration 接入；不得把“以后改配置”描述为已证明的 local/cloud 语义兼容 | 用户备注细化 | Must |
| BR-042 | Public Tasks `/v2/tasks`及PostgreSQL不得接收或回显prompt、message、raw reasoning、title派生正文或项目路径；`input`若保留，只能是closed、content-free metadata/reference。本地对话正文只进入Desktop SQLCipher与受控Runtime/provider链 | LIA-126-002明确冻结的数据边界 / ADR-0013 / DEC-126-014 | Must |

## 3. 用户流程

### 3.1 新建与首轮主流程

1. 用户进入 `/chat`，路由确认 `task.create` 且 Runtime/local repository ready。
2. 用户输入纯文本，选择一个有效本地项目，查看固定的权限审批策略摘要。
3. 用户点击发送或 `⌘Enter`；客户端生成 idempotency/request/trace ID 并禁用重复提交。
4. Desktop 在本地事务中创建 session、用户消息、pending outbox 与项目关联。
5. 事务提交后进入 `/chat/:sessionId`；Desktop 创建/恢复 Agent session，启动首 turn 并订阅 SSE。
6. 流式增量按 event ID/sequence 去重、展示并持久化；用户留在底部时自动跟随。
7. terminal event 落库后标记 turn 完成；异步触发独立标题生成，成功后更新列表。

### 3.2 历史主流程

1. 用户打开任务记录/项目树；系统只查询授权 scope 内的 session metadata。
2. 列表按置顶组和 `last_activity_at` 倒序。
3. 用户选择 session；系统取消前一个未完成 history request，验证授权并分页加载所选 history。
4. 若 Host/Runtime 重启，Desktop 用 mapping + thread resume 恢复；正文以 local DB 为历史展示权威，不能依赖旧 SSE 缓存。

### 3.3 失败与恢复

1. local DB 不可写/迁移失败/磁盘满：不创建 session、不清空输入，显示原因和安全恢复入口。
2. Host not ready：发送禁用；已持久化 outbox 在会话页显示“尚未发送”，用户可重试，不能静默重复。
3. SSE 断线：保留最后已提交 cursor，指数退避重连；stream changed/replay unavailable 时以 local DB + session status + thread resume 对账。
4. provider 超时/限流：显示稳定错误和是否可重试；原始 provider 错误/key 不展示。
5. 项目授权失效：保留历史只读显示；新 turn 阻断并要求重新选择。
6. 自动标题失败：不影响会话，保留 fallback；人工标题永不被迟到结果覆盖。

### 3.4 取消、重复与部分成功

- 取消语义：活动 turn 通过 interrupt；只有 terminal `interrupted/failed/completed` 落库后解除 active lock。
- 重试语义：transport retry 重用原 idempotency key；用户发起新 turn 使用新 key；不提供“重新生成回答”。
- 重复请求：local unique constraint + Host 一 task 一 Agent session + event ID/sequence 三层去重。
- 部分成功：local create 成功而 Runtime start 失败时 session 保留为可重试失败态；不回滚用户已确认的本地文本。
- 删除中断：先停止 active turn，等待 bounded terminal/timeout，再进行物理删除；无法证明停止时删除失败并保留记录。

## 4. 可测试验收标准

### 4.1 新建任务

| AC ID | Given | When | Then | 不可接受行为 | 业务确认人 |
|---|---|---|---|---|---|
| AC-001 | 用户有 `task.create` 且没有活跃 session | 打开 `/chat` | 显示 textarea、项目入口、权限审批入口和发送按钮，且无附件/模型/推理/语音入口 | 用隐藏快捷键仍能上传或选模型 | 段成威 |
| AC-002 | 输入为空白、项目无效或策略/Runtime 未 ready | 查看/点击发送 | 按钮禁用并给出可理解原因；输入保留 | 发送空 turn、静默无响应 | 段成威 |
| AC-003 | 合法文本、有效项目和 ready 状态 | 双击发送或在超时后重试 | 只创建 1 个 session、1 条用户消息和 1 个首 turn | 重复任务/重复扣费 | 段成威 |
| AC-004 | 中文 IME 正在组合或 textarea 有多行 | 按 Enter/`⌘Enter` | composition Enter 不发送；Enter 换行；`⌘Enter` 仅提交一次 | 中文选词被误提交 | 段成威 |
| AC-005 | local DB 正常、Host 随后失败 | 用户提交 | durable create 后进入稳定 session 页面并显示可重试失败；文本不丢失 | 先跳转后记录不存在；失败清空输入 | 段成威 |
| AC-006 | 拖入文件、粘贴纯图片或混合 clipboard | 操作 composer | 不读取/上传非文本，只接受明确文本部分并提示当前限制 | 图片被 base64 化或路径泄漏 | 段成威 |

### 4.2 对话流

| AC ID | Given | When | Then | 不可接受行为 | 业务确认人 |
|---|---|---|---|---|---|
| AC-007 | 首 turn 已接受 | SSE 持续返回增量和 terminal | 单一回答按序流式显示并 durable persist；重复 event 不重复文字 | 乱序、双字、terminal 后继续追加 | 段成威 |
| AC-008 | 用户靠近底部 | 模型继续输出 | 视图跟随最新内容且不抢焦点 | 每 token 触发屏幕阅读器或页面抖动 | 段成威 |
| AC-009 | 用户上滚离开候选 96px 阈值 | 新增内容到达 | 不强制下拉；显示不遮挡内容的“回到对话底部”按钮，点击后恢复跟随 | 抢回滚动位置或按钮常驻遮挡 | 段成威 |
| AC-010 | 固定 Runtime/model 为 reasoning-enabled turn 返回非空 raw reasoning | 展开/折叠“处理中/已处理” | `aria-expanded/controls` 正确，以纯文本显示状态、时长和具体“模型推理记录”；流式去重且不执行富文本/链接/命令 | 只显示时长、把 answer 冒充 reasoning、执行模型文本或声称完整真实思维链 | 段成威 |
| AC-011 | raw reasoning 缺失、断流、无效、超限或 completion 对账失败 | 处理 turn/发布 Gate | answer 可独立完成，但 reasoning 明确进入 unavailable/incomplete，验收不通过并阻止相关 flag 发布；不得静默时长-only | 伪造/复用 answer、把 partial 冒充完整、为过 Gate 降低断言 | 段成威 |
| AC-012 | 查看任一用户/模型消息 | hover、键盘或菜单操作 | 不出现被排除的动作按钮/快捷键；原生选择与 `⌘C` 仍可用 | 禁止系统复制导致无障碍退化 | 段成威 |
| AC-013 | 一个 turn 正在运行 | 用户停止 | 发送控件变为停止；只中止当前 turn，terminal 后可再发 | 创建第二 active turn 或误删 history | 段成威 |
| AC-014 | SSE 断线或 Host 重启 | 客户端重连 | 支持游标则去重续接；失效则通过 DB/session resume 进入确定恢复态 | 无限 spinner、丢失已提交消息 | 段成威 |

### 4.3 任务记录与项目

| AC ID | Given | When | Then | 不可接受行为 | 业务确认人 |
|---|---|---|---|---|---|
| AC-015 | 当前 scope 有 1,000 sessions | 首次打开列表 | 只读取 metadata，按 pinned/last activity/id 排序，消息正文读取数为 0 | N+1 加载所有 history | 段成威 |
| AC-016 | 快速点击 A 再点击 B | A 的慢请求后返回 | 页面仍显示 B；A 的结果被丢弃/缓存但不覆盖 | session 串线 | 段成威 |
| AC-017 | 首轮回答完成 | 标题 job 成功/失败 | 成功为安全单行模型标题；失败为确定 fallback；两者均不阻塞消息 | Markdown/HTML 注入或空标题 | 段成威 |
| AC-018 | 用户已人工重命名 | 迟到模型标题到达 | 人工标题保持不变；失败保存可重试且不丢编辑值 | 自动结果覆盖人工意图 | 段成威 |
| AC-019 | 打开 session 菜单 | 查看/键盘导航 | 只有重命名、置顶/取消置顶、删除；Escape 关闭并恢复焦点 | 归档/分叉/复制等隐藏动作仍可触发 | 段成威 |
| AC-020 | 用户确认删除非活动 session | 执行删除 | application DB 关联行在一个事务内物理删除，列表移除且无撤销 | soft-delete 冒充物理删除或残留孤儿行 | 段成威 |
| AC-021 | 用户删除活动 session | 确认“停止并永久删除” | 先取得 terminal，再物理删除；任一步失败则保留并显示失败 | turn 仍写入已删除 session | 段成威 |
| AC-022 | 打开项目菜单 | 查看所有动作 | 只有置顶/取消置顶与移除，且无隐藏快捷路径 | Finder/编辑/归档等超范围动作 | 段成威 |
| AC-023 | 用户移除项目 | 确认操作 | 仅移除 picker 引用；目录与历史 session 不删除，历史标记项目已移除 | 删除本地仓库或级联删 session | 段成威 |
| AC-024 | 用户已看到只读模型处理披露并选择项目；随后项目移动、权限撤销或 symlink 改变 | 首次或再次发送 | 只允许 Runtime 在批准根目录内按需读取；边界失效时阻断并要求重选/授权，不能使用陈旧 canonical path | 未披露读取、后台全量索引、访问越出用户选择边界 | 段成威 |

### 4.4 授权与删除安全

| AC ID | Given | When | Then | 不可接受行为 | 业务确认人 |
|---|---|---|---|---|---|
| AC-025 | 无 bearer、无 capability 或 membership 已撤销 | 调用任一受保护 Tasks operation | fail closed，审计拒绝且不执行 repository write/read | capability UI 状态代替服务端授权 | 段成威 |
| AC-026 | 用户 A 猜到 tenant B 的 task/session ID | get/list/update/delete | 不返回 B 的内容或可枚举差异，数据库 query 带权威 tenant/resource scope | `WHERE id = ?` 单独读取 | 段成威 |
| AC-027 | 请求 body/header 声称另一 tenant | 创建 task | server 从已验证 identity+membership 建立 scope，不信任 body 证明 | 客户端 `tenant_id` 决定归属 | 段成威 |
| AC-028 | 旧 consumer 仍依赖 legacy `/v1/tasks` | 新 provider 候选部署 | route 保持隔离/双轨，直到 consumer migration 与 breaking 证据批准 | 同路径无窗口硬切 | 段成威 |
| AC-029 | 用户切换账户/tenant | 旧列表/请求仍在内存 | 先取消并清空旧 scope，再加载新 scope；旧结果不能闪现/回写 | 跨租户 UI 数据泄漏 | 段成威 |
| AC-030 | 删除完成后重启应用并直接深链 | 查询已删除 session | DB 无正文/索引/outbox/cursor；返回一致不存在状态；DB 外残留按批准策略验证 | 会话可恢复或后台重现 | 段成威 |

### 4.5 生产级 UI 与可访问性

| AC ID | Given | When | Then | 不可接受行为 | 业务确认人 |
|---|---|---|---|---|---|
| AC-031 | 1180×760、亮/暗/跟随系统 | 完成创建、流式、菜单、reasoning 和删除流程 | 无主体横向滚动/重叠；语义 token、焦点和对比度符合基线 | 仅亮色或仅鼠标可用 | 段成威 |
| AC-032 | 仅键盘/VoiceOver 用户 | 完成主流程 | 图标按钮有名称/tooltip/焦点；dialog focus trap/restore 正确；消息流不逐 token 播报 | focus 丢失、hover-only、播报风暴 | 段成威 |
| AC-033 | `prefers-reduced-motion: reduce` | 回到底部、折叠、流式更新 | 关闭非必要动画并即时滚动，功能不受损 | 强制 smooth scroll/闪烁 | 段成威 |
| AC-034 | DB 只读、磁盘满、损坏或 migration 失败 | 读写会话 | 显示具体可恢复错误，不谎报保存、不静默丢输入 | 通用“出错了”且无下一步 | 段成威 |

### 4.6 Local-only Delivery 验收

| AC ID | Given | When | Then | Forbidden | Owner |
|---|---|---|---|---|---|
| AC-035 | 本地合成配置、固定契约SHA和批准的本地依赖均就绪 | 按文档启动API、Agent Host、Desktop和固定Runtime | 四组件在Owner本机ready，进程、端口、契约版本和失败诊断可核对；不依赖线上环境 | 用mock页面或单仓单测冒充四组件启动 | 段成威 |
| AC-036 | 四组件本地ready且fake provider启用 | 选择本地项目并提交纯文本新任务 | 只创建一个session并进入流式对话；assistant文本与具体raw reasoning按契约显示 | 依赖tag、registry、线上API或MiniMax才能跑通主流程 | 段成威 |
| AC-037 | turn正常terminal或受控中断 | 对账并重启Desktop | completed或显式incomplete reasoning写入SQLCipher；重启后随session历史恢复，正文不进入Host durable store/log | 每delta落库、静默丢partial或用Runtime rollout冒充Desktop历史 | 段成威 |
| AC-038 | 已存在多页本地历史 | 打开列表、分页、快速切换session并重启应用 | 元数据倒序/置顶稳定，点击后才懒加载20/50-turn分页，选择与重启恢复不串线 | 首屏全量加载正文、浮动排序或恢复错误session | 段成威 |
| AC-039 | 首轮terminal且存在多个session/project | 自动标题、人工重命名、置顶/取消置顶和排序 | 标题fallback/模型结果、人工优先和稳定排序符合DEC；项目仅置顶/移除 | 未授权动作、迟到标题覆盖人工标题 | 段成威 |
| AC-040 | session包含Desktop records、Host mapping/replay和独占Runtime thread tree | 用户确认永久删除并重启应用 | 按DEC-126-006完成跨表面清理、SQLCipher cascade/secure-delete/checkpoint；历史和深链不可恢复，receipt不含正文/raw ID/path | UI-only/soft delete、跨session误删或承诺清除OS备份/所有磁盘痕迹 | 段成威 |
| AC-041 | 下游本地draft实现获得单独授权 | 解析契约依赖 | 只使用完整SHA、已核验sibling path、workspace/path、生成SDK或已核验tarball，并核对digest；浮动branch不是契约身份 | 创建tag、publish package、配置registry或复制影子DTO | 段成威 |
| AC-042 | 本地链路仍在实现/回归阶段 | 运行模型相关测试 | fake provider与固定fixture覆盖成功、缺raw、断流、partial/completed冲突和重启；MiniMax调用数保持0 | 为“跑通”擅自使用key、真实数据或付费请求 | 段成威 |
| AC-043 | AC-001–042及AC-044适用项、仓库级测试、本地构建和完整E2E均有真实证据 | Owner执行G6本地验收 | 可标记`Local-only Delivery Complete`；同时明确G5=N/A且不是Production Ready | 把本地验收写成已上线、已发布或生产安全已证明 | 段成威 |
| AC-044 | canonical Public Tasks source、fixtures、provider repository及Desktop consumer均可检查 | 创建或读取v2 task | request/response/DB只含批准的content-free metadata/reference；正文/path/raw canary在全部Public Tasks表面为0 | arbitrary `input`、`conversation input.text` fixture、response回显或仅靠Desktop约定避免泄漏 | 段成威 |

## 5. 状态与错误语义

| 状态/错误 | 触发条件 | 用户行为 | 系统行为 | 是否可重试 |
|---|---|---|---|---|
| `entry_ready` | auth/project/policy/repository/Runtime ready | 输入并发送 | 允许 durable create | N/A |
| `entry_blocked` | 缺权限、项目、policy 或 Runtime | 修复对应条件 | fail closed，说明具体原因 | 条件恢复后 |
| `creating_local` | local transaction 进行中 | 等待/不可重复提交 | 原子写 session/message/outbox | 自动否，用户不重复 |
| `queued` | local committed、Host 未接受 | 重试或停止 | 保留 outbox/idempotency | yes |
| `streaming` | turn active | 查看、上滚或停止 | 去重 append、定期持久化 | 断线自动重连 |
| `completed` | terminal completed durable | 继续下一 turn | 关闭 active lock、更新 activity/title | N/A |
| `interrupted` | terminal interrupted | 继续新 turn | 保留部分结果并明确终态 | yes, as new turn |
| `failed_retryable` | 网络/限流/暂时 unavailable | 重试原操作 | 重用 idempotency，不重复扣费 | yes, bounded |
| `failed_terminal` | invalid contract/project or policy deny | 修改输入/上下文 | 不自动重试 | after correction |
| `history_loading` | 选择 session | 等待/切换 | 可取消、结果绑定 selection token | yes |
| `not_found_or_denied` | 已删、无权或跨 tenant | 返回列表/新建 | 不泄露资源存在性 | no until scope changes |
| `deleting` | 已确认永久删除 | 等待 | stop → terminal → DB transaction | failure may retry |

## 6. 数据要求

| 数据 | 来源 | 分类 | 租户边界 | 保留/删除 | 日志可见性 |
|---|---|---|---|---|---|
| prompt/user message | 用户 | confidential | OS user + user + tenant + session | 保留至永久删除/卸载策略 | 正文不可见 |
| assistant message | MiniMax via Runtime | confidential | 同 session | 同上 | 正文不可见 |
| public reasoning summary | Runtime/provider-approved projection | confidential | 同 turn/session | 与 session 级联物理删除 | 正文不可见 |
| hidden reasoning/prompt | Runtime/provider internal | restricted | 不属于产品持久化 | 不收集、不展示 | 永不可见 |
| project path/bookmark | native picker | confidential | OS user + user + tenant | 移除项目时删除/撤销引用；session 仅留批准快照策略 | 绝对路径不可见 |
| session metadata/title | local model/user/system | confidential | user + tenant | session 删除时物理删除 | 仅 ID/hash/长度可观测 |
| SSE cursor/IDs | Host/Runtime | internal | session | session 删除时物理删除 | 可记录脱敏 ID |
| auth/approval decision | authoritative services | confidential | user + tenant + resource/action | 按安全审计政策；不含正文 | 只记录最小字段 |
| deletion receipt | Desktop | internal | OS user + user + tenant | 成功后仅 keyed session hash/分表面 outcome；候选保留 30 天后物理删除/checkpoint | 不含 raw session/thread ID、正文、标题、summary、path |

## 7. 非功能要求

| NFR ID | 类别 | 可测要求 | 阻断阈值 |
|---|---|---|---|
| NFR-001 | 性能 | 1,000 session metadata 列表冷启动 P95 ≤ 200ms；首批 history DB P95 ≤ 300ms | 超过阈值或发生 N+1 body read |
| NFR-002 | 可靠性 | double-submit、retry、replay 均不重复 session/turn/message | 任一重复或丢 durable user input |
| NFR-003 | 安全 | 未认证、无权、跨 tenant、IDOR、path traversal/symlink race 0 次成功 | 任一越权/越界访问 |
| NFR-004 | 隐私 | 正文、reasoning、路径、key 不进入 URL/log/telemetry/error | 任一敏感泄漏 |
| NFR-005 | 可访问性 | 键盘主流程、VoiceOver、焦点恢复、对比度和 reduced motion 通过 | 阻断级 axe/人工问题 |
| NFR-006 | 容量 | 1 MiB UTF-8 Host 硬上限保持；产品候选软上限 64 KiB 并显示计数/错误 | 绕过硬上限或 UI 卡死 |
| NFR-007 | 成本 | 每 session 自动标题最多首次 + 1 次受控重试；不随列表加载重算 | 无界模型调用 |
| NFR-008 | 恢复 | Host 重启、SSE replay loss、DB 重启后进入确定状态，不无限 loading | 无恢复动作或错误状态不一致 |

## 8. 外部副作用与审批

| 操作 | 影响范围 | 是否写操作 | 审批策略 | 审计要求 |
|---|---|---:|---|---|
| 创建本地 session/message | 当前 OS user + tenant | yes | 明确发送即授权；capability/server policy 仍需通过 | request/session/task/user/tenant/outcome，不含正文 |
| MiniMax text/title 请求 | 发送到配置 provider，产生费用 | yes/external | 用户发送意图；标题为已披露的 bounded follow-up | provider/model/prompt-version/latency/outcome，不含正文/key |
| 停止 turn | 当前 active turn | yes | 用户点击停止 | turn/request/outcome |
| 重命名/置顶 | 单 session/project metadata | yes | 直接用户意图 | 本地最小事件；生产服务适用时审计 |
| 永久删除 session | Desktop SQLite + Host bbolt/replay + 独占 Runtime thread tree | destructive | 二次明确确认；活动 turn 先停止；任一分表面不确定即不报成功 | content-free receipt 仅留 keyed session hash、分表面 outcome 与时间；ADR-0014 Accepted |
| 移除项目 | project reference/bookmark only | yes | 影响说明 + 确认 | project ID/outcome；不得记录 path |
| 文件/工具/平台写操作 | 不在本期 | N/A | deny | 记录拒绝，不记录敏感参数 |
| merge到共享`develop` | 源码主线整合；不等于部署 | yes/remote | DEC-126-021要求本地跨仓E2E、audit修复、远端CI全绿后另行Owner批准 | PR/SHA/CI/批准记录；本期HOLD |
| 创建`contracts-v0.3.0` tag | 正式不可移动版本语义 | N/A this scope | DEC-126-022明确本期不创建 | 记录N/A；不得伪造tag |
| publish SDK/package或配置registry | 外部分发与凭据/版本治理 | N/A this scope | DEC-126-022明确本期不执行 | 记录N/A；只允许已核验本地tarball |
| 线上部署/生产灰度/云数据库/真实用户数据 | 生产环境与真实外部副作用 | N/A this scope | 禁止；未来意图必须重开生产轨 | G5=N/A，不产生生产审计声明 |

## 9. 非目标

- 见 `00-feature-brief.md` §5 Out of Scope；任何后续文件/图片/工具/云同步均需独立需求和门禁。
- “模型推理记录”是 provider/Runtime 实际返回的 raw reasoning 文本；产品不保证其完整、稳定、准确或等同模型全部内部思维，也不保证其中不复述 prompt/项目片段。
- “物理删除数据库行”不自动等于磁盘上所有 Runtime/备份痕迹已清除。
- FEAT-126 v1 不创建 app-level backup/cloud sync；OS/第三方备份可能保留不受应用控制的副本。
- 把 `.app` 拖入废纸篓不等于删除 Application Support 或 Keychain；普通卸载不承诺清除聊天数据。
- “项目/工作区”不等同于 FEAT-125 的业务 workspace capability，除非契约评审明确建立映射。

## 10. Open Questions

| ID | 问题 | 推荐结论 | 为什么阻塞 | Owner | 目标 Gate | 状态 |
|---|---|---|---|---|---|---|
| Q-001 | 是否确认把新建任务对话与既有 FEAT-126 Public Tasks hardening 合并？ | 确认合并为安全纵向需求；否则对话迁新 ID | 编号/例外/交付定义 | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-002 | 项目是本地目录、业务 workspace 还是新聊天实体？ | 本期定义为 native local directory reference；业务 workspace 另行映射 | cwd、授权、数据模型 | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-003 | 项目是否必选？ | 首次/继续 turn 均需有效项目，禁止隐式根目录 | Host cwd 必填与路径安全 | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-004 | “权限审批”有哪些策略/作用域？ | 本期只读显示 fixed read-only/deny；可写审批留到工具需求 | 当前 Host `never`，不可假 UI | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-005 | “不显示/隐藏侧栏”是否删除全局 App Shell 收起？ | 仅禁止 Chat 二级侧栏显隐，保留 FEAT-124 全局 240/72 | 与 Accepted Pattern 冲突 | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-006 | 永久删除是否覆盖 Runtime rollout/Host mapping/备份，是否保留 content-free audit receipt？ | 覆盖该 session 独占 Runtime thread tree（含 spawned descendants）、Host bbolt/replay 与 Desktop rows/WAL；跨 session/shared mapping 即中止；成功只留 30 天 content-free receipt，项目目录不删除；OS/第三方 backup 残留单独披露 | 隐私、审计、级联范围与真实删除语义 | 段成威 | G2 | Resolved — ADR-0014/DEC-126-006 Accepted，2026-08-02；固定 Runtime functional/restart PASS，法证抹除明确不在承诺内 |
| Q-007 | Desktop 本地会话的数据权威和数据库引擎是什么？ | Rust/Tauri-owned、版本化 embedded SQLite；PostgreSQL/Redis/pgvector/bbolt 不保存第二份易界会话正文 | 跨仓职责与数据真相 | 段成威 | G2 | Resolved — ADR-0013 Accepted，2026-08-02；不授权实现 |
| Q-008 | 模型标题如何与主 thread 隔离？ | 采用 ADR-0015：Host 在空临时目录创建 pathless ephemeral Runtime thread，使用 `title-v1` + turn-scoped strict `outputSchema`，不复用用户 thread/project/events；最多初次 + 1 次确定失败重试，人工标题优先，失败 deterministic fallback | 对话语义、成本、Runtime 能力 | 段成威 | G2 | Resolved — ADR-0015/DEC-126-007 Accepted，2026-08-02；`MM-126-001` 单次 strict title PASS；不授权实现 |
| Q-009 | 当前 MiniMax/Runtime 是否能稳定提供可公开 reasoning summary？ | 不能：MM-126-002 为 0 public-summary event；public summary 已不再是产品要求。Owner 改为要求 raw reasoning，旧 FAIL 证据保留且不重跑 | 不能用普通 text baseline 推断 feature compatibility，也不能改写历史门槛 | 段成威 | G2 | Resolved — negative conclusion accepted and superseded by ADR-0016/DEC-126-015，2026-08-02 |
| Q-010 | legacy Public Tasks 的已知/未知 consumers 与兼容窗口？ | 仓内 source inventory 未发现 active consumer；generated SDK不算runtime consumer，Host同名route是不同contract，Infra仅作双隔离。外部因Public OpenAPI无法证明为零，固定按`unknown-public`安全类别走`/v2/tasks` expand；v1全程双隔离，退休至少30日+2个Desktop RC+owner attestation+0 approved/authenticated v1 use | breaking hardening | 段成威 | G2 | Resolved 2026-08-02 — DEC-126-011/012 Accepted |
| Q-011 | 项目移除后历史 session 的归属显示？ | 保留在任务记录，归入“项目已移除”，新 turn 要求重选 | 防止误删与孤儿 UX | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-012 | local→cloud 是否要求同步/冲突解决？ | 本期只定义 storage port，不承诺配置切换；云迁移另立 feature | 避免虚假兼容承诺 | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-013 | 选择项目是否授权 Runtime/模型读取项目文件，还是只保存展示元数据？ | 明确授权批准根目录内按需只读，并在选择器披露可能发送给 MiniMax 处理；禁止后台全量索引和越界 | “仅文本输入”与 Codex workspace 读取的隐私边界必须一致 | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-014 | 项目与 session 是截图 4 的树形导航，还是项目列表与“任务记录”两个独立视图？ | Chat 导航区按项目树形展示最近 sessions；`/tasks` 继续提供跨项目完整记录，两处共享同一 metadata/query 规则 | 决定 App Shell/Chat rail、懒加载与最小窗口布局 | 段成威 | G1 | Resolved — 推荐结论获批，2026-08-01 |
| Q-015 | SQLite driver/migration、文件保护/加密、app/OS backup、卸载与 WAL 删除证明如何冻结？ | 精确锁定 `rusqlite 0.40.1 + bundled-sqlcipher`、`rusqlite_migration 2.6.0`；Keychain 32-byte key、0700/0600、WAL/FULL/fullfsync、`secure_delete=ON`、成功前 `wal_checkpoint(TRUNCATE)`；无 app backup、OS backup/普通卸载限定披露 | 新依赖、磁盘恢复边界和“永久删除”真实性 | 段成威 | G2 | Resolved — ADR-0014 Accepted，2026-08-02；Rust 1.95 build PASS，Refinery 因 native links 冲突拒绝 |
| Q-016 | raw reasoning 仅当前流式内存展示，还是写入 Desktop 本地加密 SQLite并随历史加载/物理删除？ | 写入 ADR-0013/0014 已冻结的 Desktop SQLCipher，作为历史 UI 唯一权威；流式在内存展示，terminal/显式incomplete record落库；不写Host业务DB/日志/云端，独立表随session FK cascade并纳入secure-delete/checkpoint | 数据分类、schema/migration、history一致性、容量、backup披露和删除范围 | 段成威 | G2 | Resolved — DEC-126-016 Accepted 2026-08-02；不授权实现 |
| Q-017 | Public Tasks v2的`input`是任意task正文，还是仅content-free metadata/reference？ | 推荐仅content-free，并以新immutable candidate收窄request/response/fixtures；`c000a024`不修改。备选是明确Public Tasks完全不属于local conversation数据面且Desktop永不调用，但仍需处理现有conversation fixture误导 | ADR-0013/DEC-126-014数据权威、PostgreSQL内容边界、provider conformance、G2A identity | 段成威 | G2A re-review | Open — DEC-126-023 Ready for Owner Approval；blocks LIA-126-002/S4 continuation |

## 11. 需求确认

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 需求负责人 | 段成威 | Approved — 同意 FEAT-126 推荐产品方案；Q-001–Q-005/Q-011–Q-014 Resolved；G1 Passed | 2026-08-01 |
| Product/Design | 段成威 | Approved — 极简 Chat/App Shell 产品语义由本需求包承接；Pattern 文件候选转入 G2，未授权代码实现 | 2026-08-01 |
| 架构/数据 | 段成威 | Partial Approval — 接受 ADR-0013 的 Desktop SQLite 数据权威和存储职责；删除保护、Runtime/MiniMax、Public Tasks、Pattern/contract 仍在 G2 评审，不授权实现 | 2026-08-02 |
| 架构/数据删除 | 段成威 | Approved — ADR-0014/DEC-126-006 Accepted，Q-006/Q-015 Resolved；G2 仍未通过、不授权实现 | 2026-08-02 |
| Runtime/模型能力与raw历史 | 段成威 | Approved — ADR-0016/DEC-126-015/016/017 Accepted，展示raw reasoning且禁止静默时长降级；Desktop SQLCipher历史持久化、懒加载和session级联删除；Q-009/Q-016 Resolved。G2/G2A Passed，仍无业务编码授权 | 2026-08-02 |
| G2 Closure | 段成威 | Approved / Passed — DEC-126-017、DEC-126-011/012与Chat/App Shell Pattern Accepted；进入G2A，仍不开始业务编码 | 2026-08-02 |
| G2A source contract | 段成威 | Approved / Passed — DEC-126-018/019 Accepted；`c000a0245acb5c3f7ead5d2a877fb60c281c588c`是唯一candidate；DEC-126-020专用branch远端可用性已完成；不授权merge/tag/发布、downstream pin、业务编码或生产启用 | 2026-08-02 |
| Contract Draft PR / merge readiness | 段成威 | DEC-126-021 Accepted/HOLD；PR #1 exact head保持Draft，CI红灯只阻断merge，不回退G2/G2A | 2026-08-02 |
| Local-only Delivery Strategy | 段成威 | DEC-126-022 Accepted；Local Runtime Ready为目标，tag/publish/deploy/G5 N/A；G6为本地Owner验收 | 2026-08-02 |
| Local Implementation Authorization | 段成威 | LIA-126-001已执行；LIA-126-002已批准但依contract-conflict停止条件暂停。S4–S6为Conditional / Corrective Closure Required，S7–S11/MiniMax/远端与发布动作仍禁止 | 2026-08-02 |
| DEC-126-023 / G2A re-review | 段成威 | Pending — 决定Public Tasks `input`的数据边界与是否形成新immutable candidate | N/A |
