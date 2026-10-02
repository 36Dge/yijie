# FEAT-156：MiniMax 流式工具参数兼容候选

状态：Owner已明确批准；0005已按本方案独立构建、资格验证并完成真实原生回归。当前结果见末节及02 §8。

## 实际问题与证据

日常 canonical App 的 MiniMax 跨模型聊天在请求22–24收到空工具参数，原生解析拒绝，命令未执行。受控诊断25以及独立原生聊天26–27成功，故不能仅凭前三次失败判断所有 MiniMax 工具都不支持。

被动 SSE 元数据记录在请求28–29复现了精确协议差异：

| 请求 | 参数delta合计 | arguments.done | output_item.done.arguments | response.completed中同一Item参数 |
|---|---:|---:|---:|---:|
| 28 | 125 bytes | 0 | 0 | 125 bytes，有效JSON对象，与delta的SHA-256相等 |
| 29 | 18 bytes | 0 | 0 | 18 bytes，有效JSON对象，与delta的SHA-256相等 |

仅存阶段、长度、摘要和JSON对象判定，无正文/密钥；见 `evidence/paid-call-ledger.json`。当前固定上游 `codex-api/src/sse/responses.rs` 使用 `response.output_item.done` 的 Item，忽略 function arguments delta；因此收到空串。官方 Responses 文档定义 function_call.arguments 为JSON字符串，但没有覆盖上述实际中间空值差异：[MiniMax Responses](https://platform.minimaxi.com/docs/api-reference/responses-create.md)。

## 可审阅的最小变更

contract-impact=semantic（需求整体仍breaking）。新增独立0005补丁，仅处理 SSE 中 `function_call.arguments` 为空的完成Item：

1. 普通非空工具参数、文本、图片、reasoning及错误事件保持原路径。
2. 空参数完成Item先暂存，不提交给工具执行器；按响应内的 Item ID、call ID、函数名和输出位置关联。
3. 等 `response.completed` 后，只接受同一Item的完整、非空JSON对象参数；校验与已收集的该Item参数增量一致。保持原调用顺序并在 Completed 之前交付原生工具处理链。
4. 缺少完整终态、身份/参数不一致或超过有界暂存上限时返回安全协议错误，不猜参数、不执行部分命令、不静默换模型。一个Item至多交付一次。
5. 后续仍由原生schema校验、工具路由、sandbox、权限和审批决策承接。input-only的空工具集与工具调用拒绝保持；既有0004的tool_choice=auto保持。

实际实现以固定源码事实为准；若需要扩大到别的行为，再记录决定，不悄然改scope。Host不做响应重写代理，不更换Provider协议。

## 构建与消费顺序

固定上游commit/Rust版本→原0001/0002/input-only0003/已批准0004→新0005；只在canonical临时构建目录重放，不改 `codex-rs/` 原样子树。新产物使用独立 `.yijie/build/chat-models-stream-args/aarch64-apple-darwin/`，原 input-only 与 chat-models 两组产物保留并核验hash。复用现有 `codex-rs/target`，不复制约24GiB缓存。

先用正常SSE数据做非空路径、分片/交错调用、末尾完整参数、普通缺少终态的安全拒绝检查，不使用恶意payload或故障强杀；再canonical构建、269个schema精确比较、握手/空工具input-only检查；随后更新Contracts精确产物投影与Host/Desktop消费pin，再原生真实验收。方案提出时已授权40次HTTP、4次图片理解，已用30/40和2/4，单次8192tokens；不得超额。

## 确认依据

`yijie-codex/AGENTS.md`要求先确认“是否修改 Runtime 核心、协议、沙箱、权限、认证、更新或遥测行为”和“是否新增补丁、依赖、feature flag、构建目标或发布产物”。之前Owner批准的是恢复tool_choice=auto；这次是新增流式工具参数兼容行为，需要本次确认。此为当时的批准门槛；下节记录Owner已明确批准，现已完成实施。


## Owner执行授权

2026-10-02用户明确：“认真审计当前实现情况、遇到的卡点，然后批准最小修复方案，然后执行剩余未完成的需求。”本指令批准上述最小流式兼容范围及必要独立构建/精确投影/正常验收，不扩大工具或权限，不包括Git交付或超额调用。

## 最终实施结果

上述最小方案已完整落地。独立0005产物binary为 `aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`；原两组产物hash不变，原target缓存复用。4新流式用例、34项完整SSE、clippy、269schema、可重放/反向及正常EOF资格通过；Contracts精确投影和Host/Desktop消费已同步。

真实请求33复现中间空参数时原生命令完成exit0，34续推成功；Kimi41/42正常非空路径及MiniMax44空工具结构草案也通过。原生schema继续拒绝32的缺cmd参数，未猜测/改写命令或扩大权限。当前没有待批准的Runtime补丁；本地最终验收见02 §8。累计44/50HTTP、4/4图片，meter已正常停止。
