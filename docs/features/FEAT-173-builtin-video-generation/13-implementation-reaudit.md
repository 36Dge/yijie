# FEAT-173 实现复审与修复

本轮针对已落地代码重新核对需求、修订2/09补充、实际4场景记录及Contracts→Runtime MCP→Host→Artifact→Native/UI全链。发现下列问题并直接修复。新增费用调用为0；此前主聊32/32与Seedance创建4/4均已用完，没有借用其他需求额度。未提交/推送，固定Runtime源码不改。

本轮 `contract-impact=semantic`：修正既有观察、超时、限流和能力声明的含义；wire字段、枚举、工具名、私有HTTP路径及原Artifact/ACK协议不变。先在video-generation权威源补充语义与普通回执例子，再同步派生物和Host。新旧输入/回执类型仍互通；这是同一未发布本地候选的修复，不伪造新发布来源。

## 问题、影响和修复

| 项目 | 复现或源码证据 | 修复与验证 |
|---|---|---|
| 1. 下载上限误作最低剩余预算 | 原逻辑在剩余时间少于60秒时直接pending；5秒可完成的普通小视频也完全不尝试下载 | 60秒是下载最大超时。观察context显式继承更早的caller deadline，下载受剩余总预算约束；小视频可在5秒窗口完成原交付链，总预算不增加 |
| 2. 刚收到的终态被改回pending | provider返回failed/expired/cancelled与观察期限同时结束时，原ctx分支先返回provider_pending | 先持久化实际状态；预算到期保留已知终态，显式用户/root停止仍保持本地停止语义。3种终态回归通过 |
| 3. 单次期限被误报为用户停止 | 首次handoff前仅ctx到期时，原发布函数返回local_cancelled | 区分caller期限与实际取消；handoff前仅预算耗尽返回pending继续原任务；handoff之后仍沿原delivery_unconfirmed和原Artifact事实，不重新发布 |
| 4. 限流信息丢失 | 查询Retry-After与取消/期限同时到达时未落盘；CDN下载429也没有保留Retry-After | 查询与下载都在退出观察前保留已收到的节流时间，复用现有query_not_before；新调用不缩短该时间，不新增调度/配额数据库。普通429和正常取消/期限回环复现后通过 |
| 5. 响应体超时错误分类 | HTTP 200响应头已收到、JSON body读取超时时，原client归为invalid_response，提前结束可恢复查询 | 传输/读取中断按Unavailable或实际取消处理，可在本轮剩余预算内重试原GET；完整无效JSON仍保持unknown，不放宽解析，也不重POST |
| 6. 状态和能力声明不够准确 | provider已成功但待交付时仍显示“生成正在处理中”；尚无操作身份的准备阶段也未区分。原真实MiniMax答复曾主动提出“加长时长”，而首期不支持原视频编辑/延长 | 显示区分“尚未确认受理”“任务处理中”“已生成，等待取回交付”。权威工具描述和普通聊天提示明确仅支持文本/当前图片，视频音频参考、原片编辑/延长和精确输出参数控制不可承诺；修改须是用户明确要求的新生成。专家路径不套用内置能力限制 |

问题1–5在修改前均有失败复现日志，不是只改期望后声明通过。全部使用普通本机HTTP响应、正常context取消、正常Store/Service关闭重开和既有MP4 fixture；没有真实供应商、强杀、权限破坏、可执行文件伪装或攻击fixture。问题6有原始真实答复和源码依据；本轮无额度重新验证自然语言模型是否遵守新提示，因此只声称能力描述/指令和原生装配已修正，不把旧4次生成当成新提示实测。

## 补齐的覆盖与复核结论

- 增加已知task ID在正常Store与Service重开后的无句柄恢复：同聊天新root创建仍被原未决操作挡住，查询原任务只下载/交付一次，delivery_turn属于新观察轮。
- 增加专家选择pending时创建/恢复全部拒绝、保留pending选择和原视频记录、供应商调用为0的用例；既有明确专家、不可用/失败不兜底的原生配置与Host拒绝链仍通过。
- 复核输入三种图片模式、同图首尾、默认model/content、同Key非交互、同root幂等/跨root未决屏障、单操作观察租约、2个下载槽位、既有输入/视频体积上限、handoff前持久标记、当前交付turn、Native ready/ACK区别及历史视频本地播放保存链。
- 默认参数、凭据条目/作用域、Nativecommand/CSP/SQL、Artifact wire/ACK、专家协议、原图片MCP及固定Runtime均未改；视频输入仍是既有每图10MiB、视频64MiB上限。没有新增后台轮询、自动DELETE、任务中心或第三方依赖。

## 验证

本轮新源31项Node同源/schema检查、Go SDK例子、Rust同源例子、Contracts lint、fallback结构比较、Host相关race/静态检查、两主聊固定Runtime+共享adapter发现/执行/等待/专家排除、真实Host/session→原Artifact事件/资源/ACK本机集成通过。新的日常构建已完成。最终受管adapter的联调日志与本轮起点、逐项结果见references下的implementation-reaudit记录。

旧全量生成漂移已定位：FEAT-156的 `generate-runtime-chat-models.mjs` 以当前Runtime HEAD填旧制品来源，保留锁仍记录55b4e510…；这不是video family的DTO或当前tool-search Runtime变化。没有为让全量检查变绿而刷新旧来源锁。该历史family的来源治理需要单独处理，当前视频源/canonical装配检查通过。

## 当前构建及运营步骤

- Host SHA-256：`692ec26b7db08eb4669e208350688a7a343ec0ba5fc43ddd0db2f148e42d6caa`
- 共享adapter SHA-256：`0cc2064c4ad1fd416910c6a62aa6cc001a0f83e55669ededc38708c09ec07d47`
- Desktop SHA-256：`8c655090a794829c2ced5a261162ed9c88b13e1742d8bf14be4584a7d04b8ce6`
- 普通日常入口与原Homes已启动，Runtime ready；此前已提交视频继续保留。
- 新Host首次独立无交互检查未通过；经用户本人完成同一条目的系统授权后，独立无交互检查已ready、provider_requests=0。旧授权对应16f47fb1…；本次不修改/新建Key、不申请新增费用额度，详见下方两次复核记录。

本轮修复没有新增真实模型/Seedance/Seedream/LinkFox调用。12号报告保留为修复前真实4场景证据；本轮新增边界的证据来自上述非付费回环。暗色实机及用户禁止的危险验证仍未执行。修复构建的运营访问就绪与后续只读检查在本页追加，不覆盖旧证据。

## 最终运营复核

用户明确批准新692ec26b…42d6caa构建的系统窗口。第一次有人值守读取返回ready=true，但随后独立进程无交互检查仍返回credential_unavailable；这次失败如实保留。按用户已批准的同一构建、同一条目范围再次由本人处理系统授权后，新的独立进程无交互检查已返回ready=true、provider_requests=0。Runtime ready，Host未再次重建。

没有写入/复制/新建Key，没有新增费用调用。原4场景视频保留，修复构建中的历史视频可正常播放。只读回执和两次结果见[reaudit-credential-ready.json](references/reaudit-credential-ready.json)。本轮首次观察开发页为空白，普通Cmd-R恢复后主界面及历史视频正常；未假称这一瞬态已定位根因，未修改数据或强杀进程。
