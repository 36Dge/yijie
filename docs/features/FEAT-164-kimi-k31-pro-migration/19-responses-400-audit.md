# FEAT-164 首次真实 Responses 400 审计

## 已确认事实

2026-10-25 09:59:12，通过已完成本机 Harness 资格的 canonical App 提交了一个普通计算任务。唯一真实模型 HTTP 为 `kimi-k3.1-pro / max`；供应商返回 HTTP 400、211 字节响应，未形成可确认 usage。界面显示“生成失败/未完成”，没有模型答复；正常退出并重新打开后，失败事实及用户消息保留，没有自动补发。App 与计量器均正常退出 0。

权威记录为 `evidence/g2v-real-budget-ledger.json`、`g2v-real-first-result.ax.txt/.png`、`g2v-real-failed-history-reopen.ax.txt`。账本保留 **14.188544 元预占**，`halted=true`、`meter_state=stopped_normally`。这不是供应商实际扣费；不因 HTTP 400 或缺少 usage 将其改为 0。20 元总授权保持，未新增额度，也未重发真实请求。

## 请求与官方规范核对

用户要求自行分析后，使用同一 canonical App/Runtime 和普通本机 HTTP fixture 采集封闭的字段元数据，不记录 prompt、凭据或完整供应商响应，不转发外网。一次普通请求实际包含：

- model 为 `kimi-k3.1-pro`，effort 为 `max`，tool_choice 为 `auto`；
- include 为 `reasoning.encrypted_content` 与 `web_search_call.action.sources`；
- 工具类型为 function、namespace、web_search；reasoning.summary 未出现。

见 `evidence/g2v-request-shape-ledger.json` 和对应 fixture 源 `feat164-request-shape-loopback.py`。这次采集是单独的本机证据，不是对首个真实请求正文的重建或第二次真实调用。其 App/fixture 同样正常退出 0。

当前 [Responses 官方规范](https://platform.kimi.com/docs/api/responses#body-include) 的 include 仅列两个搜索元数据值；推理强度支持 max。本机实际请求中的 `reasoning.encrypted_content` 不在该枚举中。另一个确定问题是原预算适配器省略 web_search 工具时未同步省略依赖该工具的 include。

官方 [错误说明](https://platform.kimi.com/docs/api/errors) 表明 HTTP 400 可以有多个原因。旧计量器只保存状态码和响应摘要，未保留封闭错误类型或参数提示；Runtime 也没有在本轮 rollout 中保存原始错误。因此**上述规范不一致已确认，但不能宣称它就是首个 400 的唯一原因**。可用浏览器的官方平台页面处于未登录状态，无法取得该请求的账户明细；未绕过登录、读取其它浏览器凭据或请求充值。

## 范围内修正

这是 FEAT-164 最小垂直候选的修正，不进入尚未获 G2V 放行的 S1—S4。

1. Runtime 增加 r2 的独立补丁 0008，仅对新 Kimi 省略 OpenAI 专用 encrypted-content include；保留 max、搜索来源、响应解码与历史重放，MiniMax 不变。原 0001—0007、r1 脚本和产物保留。沿 Runtime → Contracts → Host → Desktop 的来源顺序重新固定；不得手改派生物或直接替换 binary。
2. 预算适配器在出站前拒绝未列入官方枚举的 include；移除原生搜索时同时移除搜索 include，并在账本记录调整。它不能掩盖 Runtime 的不兼容字段。
3. 非成功 HTTP 的诊断只保留封闭错误类别及已知参数名提示，正文不落盘，SSE/HTTP 响应仍原样转发；缺 usage 的费用预占及停止规则不变。8 项普通离线控制通过，Desktop 本地提交 `098c634`，没有推送。

修正后须重新验证当前产物和 Harness；r1 的本机通过不能直接成为 r2 的真实通过。原真实账本不重置、不释放预占。G2V 当前未通过，后续结论必须基于新的实际证据。

## r2 来源固化与离线验证

完整来源为 Runtime `074417e5e2f5f55704ea5e1777e7a22d514076b4` → Contracts `f2819c66a2368aaff37216a46c48d5cd81df1747` → Host `5022435a6272263e66e46a41b7ed7c3f9fb6caf9` → Desktop `74f2f74d866483463df7236f891aae62b00539ba`。均仅本地提交；Host 的最终提交含实际 Runtime include 边界测试，Desktop 的共享 launcher 仅提交 r2 路径与精确 Contracts preflight 两处差异。原有其它需求改动保留。

- Runtime canonical release 构建、4 项保留 SSE、2 项 sources、4 项 FEAT-164 请求构造、core Clippy `-D warnings`、fmt、脚本语法、正常 stdio 握手均通过。269 份 schema 与 r1 逐字相同，旧产物摘要保持。完整构建仍显示上游 app-server 的既有 `unused_mut` 警告，未改无关源码，也不称全量 fork suite 通过。
- Contracts 实际 binary/manifest/patch/schema 投影检查、12 项 Node、2 项 Rust、Go constants 编译及全部 7 个支持基线的离线比较通过。没有改公共 DTO 或旧 family。
- Host 在干净不可变工作区中通过 3 项候选/历史准入检查及 vet；实际固定 r2 Runtime 完成同 thread 的新 Kimi → MiniMax → 新 Kimi 三次普通 loopback 调用，Kimi include 全部符合官方枚举，旧 K3 请求被拒绝。
- Desktop canonical 打包及来源校验通过。4 项 Harness 状态控制、8 项预算控制在当前固定工作区复验通过。当前 App 的普通回合、保存/同产物重开、模型标识及正常退出已实际通过，fixture仅收到1次请求、重开无补发，H-F164-LOCAL在r2组合重新合格。App两次退出0，fixture自身shutdown退出0，18083/18086释放；见g2v-r2-harness-positive.json及AX证据。

实际摘要、构建 receipt、Harness 源及 fixture 摘要见 `evidence/g2v-r2-provenance.json`；测试日志使用 `g2v-r2-*` 前缀，Runtime 构建/核心检查使用 `g2v-runtime-r2-*` 前缀。更早的失败日志和预占账本保留。


## 收尾审计与实际阻塞

原工作区的65个Contracts、54个Host、100个Desktop范围外文件摘要保持；共享launcher反向移除本轮两行修改后，与改前字节相同。各业务仓index为空，三个验收worktree干净，未推送。证据见 `g2v-r2-workspace-preservation.json`。

当前源码与本机资格均已重新核对；r2真实供应商复验、S1—S4以及最终core/visual/teardown仍未完成。累计真实请求仍是1次，20元预算中14.188544元预占未结清，余量5.811456元不足当前单请求保守预占；账本同时处于未知usage停止状态。没有可验证的用量证据前，不清空账本、不把400当免费、不提高预算、不通过改小预占来绕过停止。

安全上未执行任何强杀、运行时替身、权限破坏或攻击fixture。全量旧fork/Contracts攻击fixture测试仍未运行，影响是该部分不在本轮覆盖范围；已用普通状态控制、固定Runtime loopback、标准构建与正常EOF/App退出完成允许的验证。此处不宣布FEAT-164整体完成。
