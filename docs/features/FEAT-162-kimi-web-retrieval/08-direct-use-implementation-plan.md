# FEAT-162 自动配置并直接使用：实施方案

2026-10-24。用户已选择“自动复用客户端已有的Kimi模型凭据，不再配置或启用连接器”。本方案替代05中的手动绑定及/models前置检查，并先于本轮实现落盘。07审计结论继续适用。

## 最终行为

易界客户端在读取连接器/任务工具列表时自动准备内置的Kimi网页检索。已经配置Kimi模型凭据的客户端，无需另行安装此连接器、填写Key、点击本地绑定或手动启用。准备成功显示“可使用”，按任务选用及每次实际调用审批沿用既有链路。

未配置统一模型凭据的客户端明确显示“模型凭据未配置”；不打开第二个Key表单，不伪造联网认证成功。正常配置模型并重开后自动准备。用户后续明确停用/卸载的选择保留，不被列表刷新或重开覆盖；恢复使用或重新安装仍可由用户主动操作。

自动安装/准备、轮询和重开都不请求/models、Search、Fetch或模型接口。只在以后用户发起真实任务、选用工具并逐次批准后调用Search/Fetch；首次实际调用的鉴权、账号权限、余额及网络错误如实返回。

## 审计后的实现设计

1. **权威源先行。** management family升至0.7.0，provider/broker语义升至0.6.0。明确一个固定Kimi内置策略：默认安装意图、默认desiredEnabled、复用模型凭据、零供应商HTTP准备、尊重停用/卸载。生成并同步所有consumer，不新增Native命令或第二套DTO。现有Probe消息对Kimi表示本地适配器准备；connected/qualified在此表示当前可发起调用，不声明供应商验证通过。
2. **Native负责默认产品意图。** Snapshot的现有读权限检查保留；只有同一有效Native上下文同时具备manage与credentials.manage且模型/连接器能力开启时，才能按内置策略确保Kimi默认安装和desiredEnabled。只存非秘密安装/操作数据。只读权限不写入、不启动额外服务。其它连接器的Snapshot行为不变。无新增表；复用安装行、generation/revision与已有操作回执来区分首次默认、升级旧绑定、明确停用和已卸载墓碑。
3. **复用现有自动恢复流程。** 前端store已会为desiredEnabled的安装执行一次非交互Enable并轮询原回执；Kimi沿此流程自动准备，允许在无独立credentialRef时由Native创建不透明引用。每个会话/安装generation最多一次自动尝试，缺来源或失败不会形成重试循环。现有scope刷新、请求串行和过期响应保护保留。
4. **重启与取消。** 持久成功不代表当前worker资格，重开由现有恢复流程重新准备。Kimi旧Host下未完成的本地prepare回执只在确认Host/Native epoch已变化时标记为已取消以便新准备；当前Host的原操作继续原ID轮询。明确停用/卸载保持且先撤销原资格，不重放真实工具调用。
5. **worker只做本地准备。** 载入同一模型Key快照，核对固定本地两个工具描述和scope，登记当前owner能力。移除Kimi/models请求路径；保留Legacy Auth本地兼容但不暴露配置入口。Kimi Forget仅撤销当前安装的能力，不读删模型Key或另一份Keyring；此前本地候选没有保存真实独立Kimi Key，不对外部未知旧发行版作迁移承诺。
6. **失败清理。** 接管已验证存在的FD后再判断其管道类型，使所有正常返回路径关闭它；启动提示只含非秘密描述符，不进入后续provider子进程。正常EOF和关闭，不做异常注入。
7. **界面。** 删除Kimi手动配置/绑定提示与“检查连接并启用”按钮。默认准备显示准备中，成功显示可使用；缺模型凭据、失败和被用户停用分别展示。后续明确停用的恢复按钮为“恢复使用”，失败可重试本地准备；没有后台供应商探测。

## 兼容与回滚

整体contract-impact仍为breaking；semantic变更不得与旧consumer混用。仅local candidate/release:false。部署按Contracts→worker/Host→Native/UI及来源freeze/build；不提交、推送或发布。保留原生搜索、Codex内核与Agent循环。回滚须正常退出新worker并撤销资格，旧版本不得把新的本地ready状态解释成通过/models的凭据验证。数据库格式不变，保留安装、历史与墓碑；新默认策略只影响Kimi。

## 验证清单

- source/consumer同步与普通JS/Go/Rust检查。
- 普通内存凭据的真实canonical worker直接Probe：有来源即本地可调用、无来源返回not_configured；不先Auth、不发HTTP；两者均正常EOF退出。
- Native空库自动创建一条Kimi记录；已有05配置自动升级；重复Snapshot不重复安装或修改revision；只读权限不创建；用户停用/卸载保持；重启旧本地prepare正常收敛。
- 前端现有restoreEnabled自动调用一次Enable，从不Configure/Authorize，刷新不循环；成功可选、无来源不可选、停用保持；其他服务原流程回归。
- canonical App首次读取、自动准备成功、任务选择、正常重开；不发送实际模型任务或工具请求，不点击任何真实供应商检查。
- 将新的来源、截图、检查失败及修复、未执行项目写入本Feature。D4/真实账号权限、质量、计费继续NOT RUN；不得使用其它Feature额度或宣称其验收完成。
