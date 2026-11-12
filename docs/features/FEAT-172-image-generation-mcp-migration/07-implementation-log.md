# FEAT-172 实施记录

用户已接受复审版方案并要求开始实现。记录时间：2026-11-12T10:56:23.985163+08:00。

contract-impact=breaking：替换工具入口与凭据交互；专家提交契约保持；固定Runtime源码、二进制和canonical schema保持不变。

## 当前进度

- 已复核工作区，基线见 references/implementation-baseline.json；Desktop既有改动保留。
- 已将ADR-0025标为Accepted、feature标为active；D0产品方向已接受，所有产品AC仍pending。
- 正在执行源契约→Host/MCP→日常装配→定向无计费验证（修订3不改变专家提交契约或资产）。

## 授权与限制

- 本地代码/契约实现、定向正常验证已授权。
- 真实主聊、Seedream和LinkFox额度均0；不借用旧需求额度。
- 不提交/推送，不公开部署，不重建Runtime，不清库，不覆盖既有用户改动。
- 不执行强杀、权限故障、二进制替换或攻击fixture。

## 验证事实

实现与验证进行中；尚未执行产品验收，不能用方案检查记录代替。

## 修订 3：禁止自动替代选定专家

- 用户最新指令：如果用户选定的专家不可用，不再使用易界默认工具做兜底。
- 已撤回本轮专家 preflight 源与生成物；既有 immutable 同步脚本保持，不新建降级提交协议。
- 已移除专家 native result 归并、跨轮 fallback 状态与双 producer 协调锁；专家审批仍复用原有机制。
- 工具装配按可信选择禁用内置；Host 再检查当前 turn 与存储专家绑定。未知专家也不视为未选专家。
- 日常 launcher 不再读取旧 host-images.json，不再提供 images-enable/pause；新 Host 自动装配 MCP。
- 已通过：媒体/文档源契约6项、Host图片/媒体定向 race、开发入口6项与Shell语法。后续结果继续补充。

## 原生集成复核

- 固定 tool-search Runtime SHA-256 `7d49018c29704fa9863da72a34d780b8ad0e67c9ffe1821ebd1c1b94d9a46d49` 未修改。
- 实际回环发现并修正线程局部 features 表覆盖问题：使用原生 dotted leaf config，保留 Code Mode 与原工具 transport。
- 内置自动许可使用原生逐工具 `approve` 配置，不将 `auto` 误称为无确认；专家审批保持原样。
- MiniMax 应用 MCP namespace 复用固定 Runtime 已有函数适配；Kimi 维持原生 tool_search。两种配置的真实 Runtime + Rust adapter + 本地正常协议响应均通过，metadata、MCP item、同轮继续与选定专家排除已验证。
- 新媒体 capability 在 AdapterStartup 中用一个可选对象完整携带两种 token，类型层面排除半配置；保留原 Artifact token 与 Host token，不新增凭据服务。
- 进一步删除仅为专家兜底准备的 worker 启动/提交降级分支。Native 专家提交、资格和绑定保持原流程；普通生图不要求安装/选择/授权外部市场服务，基础设施故障仍沿原就绪/报错路径。
- Keychain 实现采用 Apple 推荐的 `kSecUseAuthenticationContext` + `LAContext.interactionNotAllowed`；只读查询，无账户录入或解锁。依据：[Apple 文档](https://developer.apple.com/documentation/security/ksecuseauthenticationuifail)。实际预置凭据尚未验收。

## 已知整体检查限制

Contracts 全量安全生成入口在既有 `runtime-host-images` family 未登记处停止；当前基线的 generation-plan 同样遗漏该保留投影。未改写或放宽旧 immutable Runtime 投影门禁。新媒体与修改的 document family 定向生成、consumer check 和源 schema 验证均通过。全量 test 含历史危险 fixture，未执行；本期只运行正常定向测试。

## 本地实施验证结果

原 `pnpm client:dev` 入口已完成当前 Host、真实 Rust adapter 与 Native 客户端构建并启动；`/readyz` 为 ready，实际 UI 显示新建任务页。未发送真实模型任务，未读取/修改供应商 Keychain 凭据，未提交或推送。

最终非计费证据见 [implementation-checks.json](references/implementation-checks.json)：媒体/文档源与受影响消费者同源、Contracts lint、实施前完整基线 breaking checks、Host 定向 race、真实固定 Runtime/MCP 回环、ACK 查询、正常取消、原入口六项和元仓57项通过。全量生成的既有阻塞另列，未冒充通过。

工作区保护：67个此前已有的 Desktop 文件逐字保持；开发文档原内容摘要保持，只追加 FEAT-172 说明；Codex、Skills、Connectors 源工作树保持无改动。应用源码和本地 candidate 尚未 commit/push，不是发布产物。

真实生图验收仍 NOT RUN / D4 未完成。已询问任务级上限：主聊12次 API、Seedream2次生成（文生图和参考图各一次）、LinkFox0；收到明确批准前保持额度0。依据 Host AGENTS.md“真实模型门禁必须人工显式授权并遵守任务级额度”。

## 真实验收授权

2026-11-12T13:04:51.415777+08:00 用户明确批准上述验收额度：主聊12次 API、Seedream2次、LinkFox0次。此授权取代此前额度0的等待状态；原有历史检查记录保持原时间语义。无提交/推送、凭据写入或数据清理授权。计数器复用已有 loopback 验收工具，为 FEAT-172 新建独立 ledger，不借用旧需求余额。

## 真实验收发现：遗漏的系统技能触发

第一次自然文生图回合已成功通过 `tool_search` 发现 `yijie_media.generate_image` 与 `get_artifact_status`，随后因 Runtime 自动注入的 OpenAI `imagegen` 系统技能触发，进行了6次分段指南读取。使用客户端停止按钮正常中断；已计费主聊请求8次（包括中断中的一次），Seedream和LinkFox调用均0。未将此次回合计作通过。

已补齐停用旧入口：在 Runtime 初始化阶段复用原生 Skills API，仅关闭 `$CODEX_HOME/skills/.system/imagegen/SKILL.md` 的自动启用状态；原技能文件、其他系统技能、用户安装技能与专家资源均保持。真实固定 Runtime 的两个模型配置回环重新通过，并新增断言：旧系统技能不出现在模型指令、其他系统技能仍启用。源码与技能文件没有替换，亦未增加 Runtime 补丁。

失败事实与无内容参数摘要见 `references/real-attempt-1.json`。任务剩余额度为主聊4次、Seedream2次、LinkFox0次，继续使用原计数账本，未重置余额。

2026-11-12T13:38:22.592071+08:00 用户追加主聊12次，并将Seedream总上限调整为6次。累计上限：主聊24、Seedream6、LinkFox0；已用主聊12，外部Seedream0。授权记录见 real-acceptance-authorization-2.json。没有重置请求账本。

## Keychain与终态闭环修复

2026-11-12T13:47:54.078329+08:00：一次只读进程采样确认真实Host停在 `SecItemCopyMatching_osx → SecKeychainItemCopyContent`，尚未进入供应商HTTP。旧式Keychain路径没有被LAContext alone覆盖；已增加本Host进程禁止legacy交互设置，未解锁或改任何ACL。计算机控制工具拒绝访问SecurityAgent，未尝试绕过；客户端与服务正常退出。

真实受管Host零费用检查现在在673ms内返回credential_unavailable；不读出Key到日志、不调用Provider。需运营侧为当前构建预置无交互访问资格，详见08-live-verification.md。凭据不可用不通过追加模型额度解决。

同时修复 pending Artifact 在 owning turn结束时不收敛的问题：立即发原失败事件，迟到回调不翻转/重复终态；正常延迟响应race测试通过。此前失败会话作为真实证据保留，不修补历史数据伪造成功。

2026-11-12T14:30:08.186408+08:00：用户表示此前未完成访问授权，并明确要求“再弹窗一次”。已按该指令发起当前受管Host的一次原生系统授权查询；没有使用工具操作受保护的SecurityAgent，也没有调用模型/Seedream。新增运营CLI不进入普通生图流程，普通读取继续禁止UI。当前Host SHA-256为007a0069eef12ff4595c834bba49a2999bab72faa2289a87aa05edec43c7e2f8。

用户完成单次系统授权，运营CLI返回ready；同一SHA-256的Host随后通过无弹窗只读检查（25ms、无供应商请求）。恢复真实验收，第一复测批次模型累计上限18/24，保留后续6次；请求账本12次历史用量保持。

## 最终本地验收结论

2026-11-12T15:24:40.508509+08:00：文生图与单参考图各一次真实生成，两个Artifact均由原生MCP状态查询确认为committed，1536×1536图片预览/保存通过。纯图片分析只输出文本，工具调用和生成均0。正常退出、恢复pnpm client:dev后，缓存图片预览成功，原生成回合调用次数不变，已退出计费观察模式。

累计主聊22/24次、Seedream2/6次、LinkFox0次。实际最终证据在references/final-verification.json。本地功能标记usable；此结论不覆盖公开发布、整个仓库全量生成或被安全规则排除的历史回归。未提交/推送。

## 追加实现复审（2026-11-12）

用户要求再审计并直接修复。已修复轮次身份隔离、原生绑定到达顺序、成功回执被后续取消改写、Artifact失败清理范围，以及生成登记/输入遗漏；21项Host race回归、10项契约用例和两模型固定Runtime回环通过。本轮真实调用0，原预算账本不变。用户解锁后已正常退出并完成日常入口更新，Runtime ready与原生图片预览通过；新Host初次非交互凭据检查不可用；本人明确要求再次弹窗并完成授权后，同一构建24ms复核ready，Provider请求0。无强杀或覆盖运行中的Host。详见[09](09-implementation-reaudit.md)。
