# FEAT-173 最终构建与真实验收准备

当前状态：用户已批准本次最终 Host 的授权窗口和下述独立额度；系统授权及同 SHA 无交互只读复核均 ready=true、Provider请求0。真实四场景与正常重开已完成，最终结果见12-real-acceptance.md；独立账本见 references/live-model-ledger.json，不继承 FEAT-172。

## 受管制品与凭据

- Host：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/development/bin/yijie-agent-host`
- Host SHA-256：`16f47fb14b071499fbe3615f1f5cefe6b605be4062a4d617ceb2859e97128a6b`
- media adapter SHA-256：`dc35d62e8b8183bb40ca3c76ecb271aa1cb0d69c1ccd37d214be93249418efe8`
- Desktop SHA-256：`40ce33c72ccc3747b70782aff43189ffef9c203c7ab70df335d692bd2449ac78`
- HostHome：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/demo-fast/host-home`
- 沿用 Keychain service：`com.yijie.ai.seedream`；account 为该 HostHome 的 SHA-256：`119cc9bf2e5a365e7b0eb9be114a3f995711189da3b84893c97781b8dce13c43`。

同一最终 Host 的 `--check-media-credential` 无交互只读结果：`{"code":"credential_unavailable","provider_requests":0,"ready":false}`。这不是 Seedance 账户资格结论；当前构建需要重新核验原条目的系统访问授权。用户显式批准后，可由既有 `--authorize-media-credential` 本人值守入口请求一次系统窗口，用户本人完成，随后同一 SHA 再做只读复核。不接触 SecurityAgent，不读取/传输密码或 Key，不复制、搬迁或新建条目；普通生成依旧不弹窗。授权后不无故重建 Host。

## 已批准的独立验收范围

四个新聊天各 1 个明确生成意图：文生、首帧、首尾帧、图片参考。使用公开合成描述与普通合成参考图；模型固定，全部可选参数省略。复用这四个产物验收播放/seek、音轨（如输出包含）、保存后大小/hash、取消保存与本地重试、正常重开、停止后原操作继续。专家场景仅验证已有选择阻断内置，不调用 LinkFox。

用户批准上限：Seedance POST 4 次，主聊 HTTP 32 次，Seedance GET 120 次、视频下载 8 次，Seedream/LinkFox 0 次。使用原主聊请求计数器；每个 get 工具总窗口 120 秒且最少 10 秒间隔，每个窗口最多一次下载，按工具窗口保守计入 GET 上限（未观测的数量不伪称精确实测）。额度触顶停止，不以网络错误、取消或未知结果为由新增 POST。默认 duration=-1 由供应商决定，不按固定短视频价格估算。无需为验收另建配额/调度平台。

审批依据：Host AGENTS.md 要求“真实模型门禁必须人工显式授权并遵守任务级额度”。Seedance 模型资格只能由独立获准的真实请求验证；非交互 Keychain ready 仅证明当前可执行文件可读取原条目。

## 当前结果与保留未执行项

真实四种输入、正常停止/无编号恢复、Native committed、播放/seek、取消保存/保存重试及正常重开均已执行。主聊32/32、Seedance创建4/4，查询按窗口保守上界120，下载上界4；Seedream/LinkFox为0。计数器已正常退出，日常入口已恢复。

暗色实机未执行，应用跟随macOS外观且没有独立入口，本任务未修改全局外观；1180×760亮色实机已验证，原窗口尺寸已恢复。历史攻击/强杀/权限破坏/可执行文件替换测试按用户安全条款未执行。未调用真实专家供应商，专家隔离由固定Runtime/Host非付费集成验证。公开分发和Git提交推送未授权。

本次授权后不改 Host/adapter 源码与二进制；主聊计数器补充 FEAT-173 独立 ledger 校验分支，复用现有 `start-ui --media-meter` 本地传输选择，不复用 FEAT-172 的账本或授权。计数器不改写模型 payload，达到主聊上限拒绝转发；创建/查询/下载按原工具操作和保守窗口分别记账。

正常重开后当前Desktop SHA-256为 `6fcd7e5f43520e6a9e591e7e1b036c13f1dab6fab9255272ede1efedbd8042cf`；Host和adapter仍为上方相同SHA。验收专用入口的Desktop SHA为 `f5c3a8c75c1f676247e51bb398c09b22741b2494a7301106899ef92a70699f15`，均为canonical开发构建，不混称为发布制品。

实现复审后的当前运行构建和凭据就绪以[13](13-implementation-reaudit.md)为准：Host为692ec26b…42d6caa，经本人再次授权后，独立非交互复核已ready；首次失败仍保留，当前结果见13。上方16f47fb1…及4次真实生成记录保留为原始验收，不冒充本轮重新付费验证。
