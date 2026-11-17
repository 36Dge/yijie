# 连接器 P1/P2 剩余实机验收方案

已执行；最新结果、发现的修复与未覆盖边界见 [2026-11-17 实机验收记录](2026-11-17-local-acceptance-results.md)。下列进度段保留执行时序，不作为最终通过声明。

2026-11-17。用户先授权继续本地协议实机验收并允许真实模型，随后明确允许增加隔离验收入口。
当前六仓基线已记录；没有活动易界进程。不得提交、推送、强杀、替换/伪装二进制、破坏权限或注入攻击 fixture。

`contract-impact=semantic`：新增显式隔离部署配置与仅在该模式可见的本地工具目录；日常 wire、审批语义、Runtime、数据库迁移不变。
权威源为 Contracts `compatibility/market-local-acceptance/profile.json`，版本 0.1.0，来源本地候选，不作发布承诺。
用户是本次全部 consumer 的 Owner；新增范围已明确批准。旧 qualificationOnly 测试 worker 仍不得充当产品 worker。

## 接入方式

1. 使用正常构建的同一产品 worker，增加显式本地验收参数；日常参数不启用本地服务。
2. Native/Host/worker 各自验证验收标签和独立路径；Native 使用独立 App Data 子目录，Host/Runtime 使用独立 Home。仅暴露名为“本地连接器验收”的 keyless 服务，不冒充 Kimi、Shopify 等平台，不读取供应商凭据。
3. MCP 端点固定为 127.0.0.1:18085/mcp。复用原生 codex-rmcp-client、通用 schema 资格与 generic adapter、真实 Gateway、owner/native 双决定和一次 HTTP 许可。
4. 默认用原已支持的 127.0.0.1:18083/v1 Responses 验收路由，普通协议响应仅触发固定无害工具请求，不代替工具结果/审批/SQL写入。必要时再使用用户已许可的真实模型短任务；不会把本地协议驱动写成真实模型效果。
5. 所有审批点击通过真实 App；决定留痕由现有 Native persist 触发 SQL47，结果关联只消费 worker 生成并经原生保存的 _meta。现有观察组件、native事件订阅与Host缓存不另造替代实现。

## 用例和判定

| 用例 | 实际动作 | 必须观察到的证据 |
| --- | --- | --- |
| A 拒绝 | 发起本地样本工具，点击拒绝 | 上游 tools/call=0；本次拒绝回执及 SQL requested/ack；工具结果不能报成功 |
| B 两次批准 | 同一轮用相同参数调用两次，分别允许一次 | 第二次仍有新审批；两个不同 callRef/approvalId/decisionId，实际上游调用恰为2；原生 Item/_meta 与原轮次完全对应 |
| C 结构化与双表示 | 调用 structured 与 dual 场景 | 纯 JSON 可见；不同正文和 JSON 都保留；无虚构 native content index；原生结果状态保持 |
| D 普通业务错误 | 本地服务正常返回 isError=true | UI失败，_meta/决定留痕仍对应，不把批准当成功 |
| E 事件刷新 | slow 场景正常延迟返回 | 审批后先执行中，再由原生事件更新完成；不点刷新。活动时仅轻量审批轮询；空闲后不继续整线程读 |
| F 正常停止 | slow 场景批准后，用户正常停止任务 | 真实停止/返回事实如实保留；若实际无结果，决定记录独立只读。不会故意丢回包或强杀制造 unconfirmed |
| G 正常重开 | 完成任务后菜单退出，再用同标签重开 | SQL47 reader可读；历史决定/原始名称/结果关联保持；上游调用计数不因观察或重开增加 |

对128条窗口、精确竞态、送达不确定等不能在正常实机动作稳定产生的边界，保留已有定向测试证据并明确不是本轮GUI覆盖；不人为破坏环境追求全绿。

## 执行顺序与回滚

先完成来源/同源同步和隔离配置检查，再生成正常构建、启动普通本地协议端、启动显式验收App。
逐例记录截图、协议请求计数、原生实际身份、SQL只读核对与Host读日志。任何必要链路失败即记录失败并修复真实问题，不注入成功状态。
正常退出验收App和协议端后，可恢复原日常入口；验收数据单独保留，不删除/降级日常库。

## 当前基线与进度补充

2026-11-17 的当前源码已包含独立于本轮的 migration 48（builtin web selection origins）。
“SQL 47 决定留痕”验证以 migration 47 的事实表和真实决定写入为准；若正常产品路径
已升级为 48，不将其错误地报告为恰好 47，也不降版本。

隔离模式代码、同源配置已接入，Native/worker cargo check、Host scoped test/go vet、
42 项前端回归与各 1 项 Native/worker 新隔离测试通过。Worker strict Clippy 通过。
Native strict Clippy 目前被 HEAD 已存在的 `src-tauri/src/native_auth/local_service.rs`
六处 unit_arg 告警阻挡，该文件本轮未修改，不能声称 Native 全量 lint 通过。

首次 canonical start-ui 已通过来源检查，但原 Docker Desktop 没有运行，workflow
就绪检查拒绝继续。CUA 打开已安装的 Docker 时报告 Mac 锁定并要求用户手动解锁。
已请求解锁；未绕过系统锁定、未改写服务 ready、未打开日常App或发送模型请求。
本地协议端目前收到业务工具调用 0、模型请求 0；实机用例尚未开始。


## 解锁后的启动检查修复

用户已确认手动解锁。原 Docker 正常启动并返回 ServerVersion 29.6.1；第二次启动
进入旧 v4 契约检查时，generate-market-connectors 的 gofmt 阻塞于 stdin 读取。
只读 sample 证实 read 等待；该子进程仅 stdin/stdout 格式化、未带 -w。对这一个本轮
只读格式化器发出一次普通 SIGINT 取消，无 SIGKILL、无产品进程终止；失败记录保留，
原生命周期随后正常停止专用服务。

检查器改用完整临时 .go 文件传入标准 gofmt；7 份 SDK 输出逐字保持，重新按 canonical
脚本生成来源并同步三个消费者。此 IO 修复自身 contract-impact=none，不改变 wire
或绕过校验。现在按完整原检查流程重试，尚未发起模型或业务工具请求。

## 实机发现后的最小调整

实际完成拒绝、同轮两次分别批准、纯 JSON/双表示和 isError 检查后，慢调用发现协议
驱动未接续原生 Code Mode yielded cell，提前发出最终回答。本次慢调用不计为事件
刷新通过；驱动应只从最新原生输出读取 cell ID，使用原生 wait，不能臆造完成。

同时发现 Native DecisionFact writer 复用了安装状态的秒级 now()，违反既有
observedAtUnixMs 毫秒契约。维持本任务 semantic 分类，修复 writer 为独立毫秒时间；
不改变 wire/schema47、不改安装时间单位，不回写旧 append-only 事实。历史候选错误
时间仅在展示层标为“旧记录时间单位异常”，不猜测修正值；排序和关联仍以 append
顺序与身份为准。旧 reader 可读取新毫秒事实；回滚 writer 会重新产生错误单位，因此
应保留修复或停用新增决定写入，不降级/删除 SQL47。补单位回归与真实新决定检查。

正常停止实测另发现：Native history 已保存带 _meta 的取消结果（failed/outcome unknown），
但停止时 event snapshot 仍只有 in_progress。前端在 active→idle 的最后事件读取后，
仅当仍有未结束项时补一次原生 history 对账；不新增 wire、Runtime patch 或空闲轮询，
不从停止事实推断执行状态。通过普通停止复验及定向用例确认不会重新发送决定。
