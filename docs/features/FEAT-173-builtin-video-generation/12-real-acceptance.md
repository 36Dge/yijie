# FEAT-173 实施与真实验收结果

本页保留初版实现的4场景真实验收记录；后续实现复审发现并修复的边界、当前构建和0新增费用验证见[13](13-implementation-reaudit.md)。

2026-11-12，已按接受的第 2 版及 09 补充实现并完成本机真实验收。固定 Runtime 未改，普通 MCP `yijie_media.generate_video` / `get_video_result`、默认参数、原凭据和原 Artifact/Native/视频组件链路均已接通。正常日常入口已恢复为 `pnpm client:dev`，Runtime ready，原 HostHome 和聊天历史保留。无 Git 提交、推送或公开发布。

## 真实四种输入

| 输入 | 主聊 | Seedance 创建 | 默认产物 | 交付/播放/保存 | 证据 |
|---|---|---:|---|---|---|
| 文生视频 | Kimi K3.1 Pro | 1 | H.264/AAC、1280×720、约12秒、8,838,483 bytes | Native committed；播至12秒；时间轴跳至6秒；取消保存后重试成功 | [文生](references/real-text-to-video.json) |
| 唯一首帧 | Kimi K3.1 Pro | 1 | H.264/AAC、约10秒、7,824,458 bytes | 真实running时停止；新轮无编号续查原操作；新delivery_turn交付；播放保存成功 | [停止与恢复](references/real-first-frame-stop-resume.json) |
| 同图首尾帧 | Kimi K3.1 Pro | 1 | H.264/AAC、960×960、约5秒、3,322,639 bytes | `first_last_frames [1,1]` 被真实服务接受；Native committed；播放保存成功 | [首尾帧](references/real-first-last-frames.json) |
| 两张图像参考 | MiniMax-M3 | 1 | H.264/AAC、1280×720、约15秒、9,107,768 bytes | `reference_images [1,2]`；Native committed；播放保存成功 | [多图参考](references/real-reference-images.json) |

四个请求都只使用 model/content，未传 duration、ratio、resolution、generate_audio、watermark 等可选输出参数；表中的时长和尺寸是实际结果，不是验收覆写。两个输入 JPG 是此前公开合成马克杯素材，本次没有调用 Seedream。产物保存在 Desktop `.local/feat173/live-workspace/`；每个文件的完整 SHA-256、字节数和 ffprobe 结果在对应证据中。音轨与原生音量控件可见，文生文件的非零音量测量为 mean=-30.1dB / max=-10.7dB；不把此测量写成主观听感验收。

## 停止、恢复与本地重开

首帧原操作 `01a1cff2-3b70-7413-8f6b-2ef62107da87` 在 provider_status=running 时通过 UI 正常停止。Host 回执为 local_cancelled，原轮保留已中断状态，不宣称远端取消。随后用户消息不提供任务编号，新轮查询原记录，生成次数仍为1，产物交付到新的 `01a1cff5-6034-7301-ac17-57b8ceca45eb`。没有重新上传参考图或执行 DELETE。

四条视频全部提交后，使用 ⌘Q 正常退出，Host/Runtime/adapter 和所属 workflow 服务正常收尾；计数器以 stdin EOF 正常停止。再以普通日常入口重开，四条历史卡片均为 ready 并能开始播放，首帧场景的原中断轮与后续成功轮同时保留。文生视频再经原生保存得到 `feat173-text-reopened.mp4`，与首次保存逐字节相同。没有新的媒体 MCP 调用或生成，见 [正常重开](references/real-normal-reopen.json)。

亮色实机在 1180×760 窗口验证，截图2360×1520、scale=2；播放器、时间轴和保存可用，纵向滚动正常，控件无重叠。窗口恢复到原1339×843。暗色实机未执行：应用跟随 macOS 外观，没有单独主题入口；本任务没有改变用户全局系统设置。已有主题 token/播放器样式未改，不能把亮色结果冒充暗色实测。

## 授权与用量

用户明确批准独立额度，并本人完成最终 Host 对原 Seedream 条目的系统访问授权。Host SHA-256 始终为 `16f47fb14b071499fbe3615f1f5cefe6b605be4062a4d617ceb2859e97128a6b`；授权后及正常重开后，无弹窗检查均 ready=true、provider_requests=0。同条目、同作用域、同 resolver，没有新建、复制或修改 Key。

| 项目 | 授权上限 | 结果 |
|---|---:|---:|
| 主聊实际HTTP | 32 | 32（Kimi25、MiniMax7） |
| Seedance创建 | 4 | 4，四个操作均成功 |
| Seedance查询 | 120 | 按get窗口保守上界120；不冒充供应商逐请求精确计量 |
| 视频下载 | 8 | 按工具结果保守上界4 |
| Seedream / LinkFox | 0 / 0 | 0 / 0 |

主聊计数器原样转发 payload，32条记录全部 completed；使用独立 FEAT-173 ledger，未借用 FEAT-172。窗口计数包含一个没有原任务的本地查找，保守多计，不据此宣称真实调用了120次供应商GET。详细记录见 [授权](references/live-authorization.json)、[主聊账本](references/live-model-ledger.json)、[视频操作](references/live-video-ledger.json)、[正常关闭](references/live-meter-closure.json)。验收代理现已关闭，普通日常入口不依赖它。

## 专家、兼容与检查范围

专家不兜底通过最终受管 adapter + 固定 Runtime 的 Kimi/MiniMax 工具配置集成，以及 Host 当前持久专家绑定/创建/恢复拒绝测试验证；原生工具集合排除内置媒体，Host 再次阻断，不清空选择。没有调用真实专家供应商，更没有将旧生图验收冒充本次视频证据。图片工具与视频创建名额独立、原图片 MCP 回归通过。

新 Contracts 29项例子/schema检查、Go/Rust同源例子、相对实施前完整fallback的结构比较、Contracts lint、Host race/静态检查、真实固定Runtime/Host/MCP本地交付回环、前端定向17项、开发入口配置8项和新计数器离线授权/正常EOF用例通过。定向前端1项及历史危险测试按安全清单排除，未执行攻击fixture、强杀、权限破坏或可执行文件伪装。证据见 [本地检查](references/implementation-checks.json)。

完整安全生成检查仍报告既有 `runtime-chat-models/source.lock.json` provenance 漂移；新video family与canonical实际使用的来源检查通过，旧锁没有为本需求刷新。此结果不是全量仓库回归零缺陷、公开发布或生产签名资格。

## 保留的设计边界

视频64MiB上限不变；停止不取消远端running任务或承诺停止计费；一次handoff后不重建spool/ACK，不保证Host重启后的未提交产物可补领；已提交的视频由Native本地持久化，实测可正常重开播放保存。没有账户级任务列表、自动DELETE、后台轮询worker、通用任务中心或新增Runtime补丁。
