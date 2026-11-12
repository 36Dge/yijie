# FEAT-173 实施记录

2026-11-12T19:56:22.016753+08:00：用户接受修订2及09交付补充并授权实施。contract-impact=additive；D0接受，产品AC仍待验证。首先保护现有方案工作区，业务6仓起点clean，记录完整HEAD和摘要。先Contracts源，再Host/MCP/Native接线与文案；固定Runtime不改，不借用FEAT-172费用额度。不提交/推送。

## 本轮实现与本地验证

实现保持已接受的第 2 版及 09 补充边界。Contracts 新增独立 video-generation 源和 Go/Rust/TypeScript 投影，Host 通过既有共享 media MCP 增加 `generate_video`、`get_video_result`，复用固定 Runtime 和图片凭据 resolver。没有 Runtime 源码、专家协议、Artifact/ACK wire 或 SQL migration 改动。

Host 增加 Seedance client 和会话内的最小私有操作索引：同 root 只创建一次、不同输入冲突、同聊天未决跨 root 阻止新创建，无句柄可恢复查询。当前观察 root 与创建 root 分离；停止、旧终态和迟到结果不得污染新轮次。任何已选/待选专家都阻止内置创建与恢复，不清空选择。首帧、首尾帧（含同图两次）与图片参考使用当前附件；供应商 body 只含固定 model/content。下载不带 Ark 凭据，复用原 encrypted spool、media v9、Native 提交/ACK 和视频组件。

实施复核补齐两项边界：30/120 秒预算从入口开始，包含原生绑定等待；保留一个私有 `query_not_before` 节流时间，确保新的工具调用和正常重开仍遵守 10 秒间隔与 Retry-After（秒数或 HTTP 日期），不将节流时间伪作供应商观察。下载前及槽位获得后都检查剩余 60 秒预算。没有新增调度器或后台等待服务。

Desktop 只增加精确的开发回退 selector 传递、视频源契约检查和 provider/video 失败文案；现有播放器、保存、scheme、Range、CSP、command、权限和 SQL schema 全部复用。默认已装配；回退使用 `YIJIE_FEAT173_VIDEO_MCP=false` 正常重开，保留图片能力与原 Homes。

本地证据见 [implementation-checks.json](references/implementation-checks.json)：

- 新源 28 个普通正反例及自包含 MCP schema 共 29 个 Node 检查通过；Go SDK 与 Rust 同源例子通过。Contracts lint、相对实施前完整 fallback 的 breaking 检查通过。
- Host 相关 Go race 用例、gofmt/vet/shell 检查通过。覆盖并发创建、丢失句柄、正常停止后的查询、迟到创建/下载、专家阻断、未知创建/交付、原生事件顺序、同源 ACK、查询节流与正常清理后的迟到写入拒绝。
- 固定未修改 Runtime 与 canonical Rust adapter 的 Kimi/MiniMax 原生发现→创建→查询→exec/wait→Artifact status、专家排除和图片回归通过；完整 Runtime→MCP→真实 Host/session→media 事件→原资源→ACK 集成通过。模型和视频内容仅为普通本机回环 fixture，无外部供应商请求。
- 前端定向 17 项通过、1 项按既有安全清单排除；精确 ESLint、项目 `vue-tsc --noEmit`、开发入口 Python 8 项配置检查通过。此前试用 plain tsc 不适用于该 Vue 项目；已改用仓库规定的 Vue checker，不修改无关组件。
- 全量安全生成检查实际执行后仍发现此前已有的 `compatibility/runtime-chat-models/source.lock.json` 来源漂移；只读检查未修改工作树，没有刷新旧 Runtime 锁。本族和当前 canonical 构建所需检查通过；不能宣称全量生成零漂移。
- 不执行强杀、可执行文件伪装替换、权限破坏、恶意 fixture 或攻击测试；未运行包含这些行为的历史全量测试集合。既有安全排除覆盖范围不变。

## 日常构建与零费用检查

确认日常 App/Host 已退出后，用 `pnpm client:dev` 同一固定入口构建并启动。Host、共享 adapter 和 Desktop 均为标准项目脚本输出；原 Home、身份、历史与固定 Runtime 保留。CUA 观察到“新建任务”主界面、旧聊天列表和 Kimi K3.1 Pro 选择，未发送消息；已有 authenticated workflow ready。

最终制品身份及只读凭据检查见 [11-live-verification.md](11-live-verification.md)。当前受管 Host 读取原运营条目返回 credential_unavailable；没有弹系统窗口、写 Key 或调用供应商。操作系统授权与 FEAT-173 独立真实费用额度尚未取得，真实四种输入、默认视频解码/播放/seek/保存/重开仍 NOT RUN，产品 D4 未通过。不能把本机 fixture 或 FEAT-172 结果代替此门禁。

本轮无 Git commit、push、tag 或公开发布。yijie-codex、yijie-skills、yijie-connectors 源码工作树保持干净。

最终受管 adapter（dc35d62e…18efe8）在 canonical 构建后再次通过两主聊原生 MCP/图片回归和完整 Host 交付集成；对应日志已追加。Feature Package strict/D0、元仓 lint 与受影响仓 diff 检查通过。已向用户提出本次最终 Host 的系统弹窗与独立真实验收额度请求；在收到明确回答前不弹窗、不调用真实模型。

日常受管 Host 的 loopback `/readyz` 已复核为 HTTP 200、runtime_state=ready、status=ready；同一 App→Host→共享 adapter→固定 Runtime 进程链存在。该检查没有模型或供应商调用。人工授权请求仍待回复。

## 本轮收尾

用户后续已批准授权与额度；相关pending叙述为当时状态。本人系统授权及同SHA只读检查通过，真实四场景与正常停止恢复/播放保存/重开验证完成，详见12和live账本。新增计数器仅补FEAT-173独立task模式与非付费启动/额度/EOF检查，不改Host业务二进制；重开后Host仍16f47fb1…7128a6b、adapter仍dc35d62e…18efe8。日常入口恢复，当前Runtime/凭据ready，未提交推送。
