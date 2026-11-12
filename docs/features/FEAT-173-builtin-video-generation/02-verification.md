# FEAT-173 验证安排与当前证据（修订2）

用户现已接受修订2及09补充并授权实施。本地实现、契约定向检查、固定Runtime/MCP/Host回环和canonical构建已执行，详见[实施记录](10-implementation-log.md)与[证据](references/implementation-checks.json)。独立获准的真实四场景、停止恢复和本地重开已通过，当前证据见[12](12-real-acceptance.md)。下列矩阵继续作为验收标准，不能将本地fixture或FEAT-172结果当作真实Seedance验收。

## 1. 实施后的定向矩阵

| 验证 | AC | 必须观察的事实 |
|---|---|---|
| V01 原生与契约 | 001/009/010 | 两工具正常MCP发现、Code Mode exec/wait/预算/取消；不同RPC结果不伪造视频成功；原生150s是配置，不假设硬限制；旧图片族保持 |
| V02 默认body与图片 | 003/004 | 固定模型、所有可选输出参数省略；文本/首帧/首尾/参考图角色正确；首尾[1,1]可用；普通输入不支持时0POST，无弱参数绕过 |
| V03 凭据 | 002 | 原service/account/resolver，无新secret或用户配置；普通查询无UI，Seedance资格单独验明 |
| V04 专家 | 005 | 创建/恢复/无句柄定位/锁后派单/发布前都校验原绑定；已选专家/切换pending/资源失败/旧工具历史均无新供应商请求；选择前已发请求不伪称未发 |
| V05 异步与查找 | 006/009 | 无句柄找回同root/唯一未决；多条已完成记录返回有界候选且不猜最新；无记录不创建；GET只用本地归属的原供应商ID |
| V06 防重 | 006 | 同root同摘要重放、改参冲突；跨root在同聊天有未决/unknown时仍0新POST；两个并发创建事务只有一个预占；不同已完成需求不按prompt强行去重 |
| V07 观察与停止 | 008 | 创建root与新查询root context分开；旧终态/迟到stop不取消新查询；当前查询停止、模型预算耗尽、自然结束后无新GET/下载/迟到发布，DELETE=0 |
| V08 交付边界 | 007/008 | 一次handoff不代表成功；见下表及09的VD01–03/07。验证真实bytes/事件、schema9/12、当前交付turn→本地turn映射、projection/reference双刷新；原ACK/Status保持 |
| V09 真实视频UI | 007 | 09的VD03–07：对话内播放器自动呈现、用户播放/声音/seek、原生保存hash一致、取消保存、关闭释放、无正文/正文迟到、切换聊天/重开；本地重试供应商请求0；修正provider/video失败文案 |
| V10 回归与私有状态 | 001/010 | FEAT-172时序、重复、图像分析及文档关闭状态查询保持；bucket旧writer保留、未知版本拒绝、cleanup级联；不增加独立TTL/配额后台 |

正常回环采用固定Runtime、真实标准构建adapter、回环供应商和普通MP4；这证明协议/时序，不代替真实Seedance质量/资格或GUI。只有文档检查在本轮实际执行。

## 2. 停止与恢复矩阵

| 位置 | 后续行为 | 必须禁止 |
|---|---|---|
| 明确尚未发POST | 记cancelled_before_submit；新用户需求可走新root | 在已停止root重新发请求 |
| POST可能发出、无供应商ID | get无句柄能找到本地unknown；同聊天未决屏障保留 | 新POST、从账户列表猜ID、把本地stop写远端cancelled |
| 已保存ID但返回给模型丢失 | 在新root的get定位原记录并查同ID | 要求用户记得从未收到的句柄、重新创建 |
| 任务排队/运行或下载中 | 停止当前观察；新合法root继续原任务，原创建context不复用 | 旧创建轮次取消新观察、后台poll |
| 尚未handoff | 下载/校验后在新观察root首次交付 | 跨聊天交付或复用他人供应商ID |
| handoff标记后、事件/ACK不明 | 只查原Artifact；若无法确认返回delivery_unconfirmed | 重发started/completed、换Artifact ID、恢复旧spool或写ACK镜像 |
| 同Host已ACK | 复用原Store事实和现有本地内容 | 再GET供应商/下载/创建 |
| Native已提交但Host重启 | 原UI可预览保存；Host状态可能unknown，明确两者不同 | 假造Host committed或把本地ready改成failed |
| 原Artifact cancelled/failed | 保留原终态并报告，不能补领复活 | 以“恢复”为名另造成功卡片 |
| 当前已选专家 | 阻断内置恢复，只保留既有本地已提交内容读取 | 清除绑定、使用旧时未选专家的许可 |

顺序窗口通过纯函数/普通有界回环与正常退出验证，不强杀制造故障。无法安全进行的进程窗口只记录分层证据，不能冒称进程级E2E。

## 3. 后续真实验收

实现/构建可审查后再申请独立额度：建议文生、单首帧、首尾、参考图各1次，共最多4次Seedance创建，分配到Kimi/MiniMax两个profile。主聊HTTP、创建、查询、下载分账，按默认实际时长制定费用上限；本轮0额度，不借FEAT-172余量。若只获准2次，则其它模式保留未实测结论。

除了手工给ID的回环，必须用自然语言覆盖“刚才的视频呢”“停止后继续”“刚刚网络错了再试”：应调用原查询或报告unknown，计数器证明无新POST；当前已选专家时新供应商请求0。采用合成商品/风景，不读真人/商家隐私素材。真实成功必须来自日常入口并Native提交播放保存；手工seed Artifact不算通过。

## 4. 文档检查与限制

修订1初审的文档检查见references/plan-checks.json；本次重点源码与修订2检查见references/reaudit-source-evidence.json及references/reaudit-checks.json。仅元仓方案/ADR变化，业务源码、制品、数据、凭据与运行状态保持。

本轮不执行产品generate/Go/Rust/前端测试、构建或探针。未来也禁止强杀、二进制替换、权限破坏、攻击fixture和危险归档。默认体积/编码、运营模型资格和实际下载域仍需独立实测。已存在的Contracts来源漂移不通过改旧锁掩盖。没有公开发布、提交或推送。

首期恢复承诺是**供应商任务在首次交付之前可精确继续**；交付之后遵循既有Artifact事实，Host重启不自动补领。unknown明确报告和不重建本身是该边界的正确结果，不记为“已恢复成功”。

## 5. 对话流交付专项（同属修订2，尚未执行）

以[09](09-video-chat-delivery.md) VD01–07为AC-007的具体完成条件。现有ChatArtifactVideo组件单测或MCP返回成功都不够；必须从真实Host视频生产者走进Native提交与对话页。

实施时定向覆盖：Host provider/video生产与事件顺序；Native application/ArtifactTransferService的schema选择和本地ID映射；chat.store的artifact_changed刷新、artifact.store、ChatPage及ChatArtifactShell/Video的组合用例；原Native视频协议、播放/Range/保存边界。新provider/video文案需受影响文件lint和组件用例。所有用例先应用现有安全排除清单，不跑攻击/权限破坏/二进制替换用例。

真实四场景生成后的同一批视频继续执行播放/seek/声音/保存及正常重开检查，不另加生成次数。记录操作引用、两组turn映射、Artifact ID/size/hash、Native ready与ACK状态、实际播放器和保存结果；不记录供应商签名URL或Key。真实四场景及其原生产物体验结果见12；暗色实机与禁止的危险验证仍未执行，范围如实保留。
