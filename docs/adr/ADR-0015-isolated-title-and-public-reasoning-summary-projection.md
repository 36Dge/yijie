# ADR-0015: 隔离模型标题与公开 Reasoning Summary 投影

## 状态

Accepted — 2026-08-02；public-summary-only 部分于同日被 ADR-0016 取代，标题隔离部分继续有效

## 日期

2026-08-02

## 决策负责人

段成威

## 关联需求

- `FEAT-126-public-task-authorization-hardening`
- `DEC-126-007`
- `Q-008`、`Q-009`

> 取代说明：段成威于 2026-08-02 明确要求 UI 展示 raw reasoning、不得静默降级为时长-only。
> ADR-0016 因此取代本文第 2–3 节及相关 public-summary-only 影响/风险/后续动作；本文第 1 节的隔离
> 标题 operation、MM-126-001/002 历史门槛和实际验证证据继续有效，不得被事后改写。

## 背景

FEAT-126 要求首轮完成后自动生成 session 标题，并在对话流中提供可展开/折叠的“模型思考过程”。
产品决策已经把后者限定为 provider/Runtime 明确允许公开的 reasoning summary，而不是隐藏
chain-of-thought。当前 Agent Host 只暴露 `thread/start`、`thread/resume`、`turn/start`、
`turn/interrupt` 和 8 类 Runtime notification，`model_reasoning_summary` 默认 `none`，既没有独立
标题 operation，也没有 reasoning-summary public event。

固定 Runtime `codex-cli 0.144.6` 的 canonical schema/source 提供：

- `thread/start.ephemeral=true`，返回 `thread.ephemeral=true` 且 `thread.path=null`；
- turn-scoped `turn/start.outputSchema`；
- `item/reasoning/summaryTextDelta` 与 `item/reasoning/summaryPartAdded`；
- `item/reasoning/textDelta` raw reasoning，以及可能同时包含 `summary` 和 raw `content` 的 reasoning
  `item/completed`。

2026-08-02 在清除 MiniMax/OpenAI 等模型 key 的环境下运行固定源码既有 fake Responses provider
fixture：ephemeral thread pathless、`outputSchema` 转换、`outputSchema` 仅当前 turn 生效、
reasoning summary 请求参数、summary delta 与 reasoning item ID 关联均通过。summary item 测试第一次
因 Tokio worker 默认栈溢出中止；仅设置 `RUST_MIN_STACK=33554432` 后，同一源码和断言通过。整个
评审没有调用 MiniMax、没有真实数据、没有业务代码或契约源变更。

这些证据只能证明固定 Runtime 和 fake provider 的能力，不能证明 MiniMax-M3 的 Responses
structured output 或 public reasoning summary 兼容性。

## 决策

### 1. 标题必须使用隔离 operation

1. 模型标题不得在用户 conversation thread 中插入隐藏 turn，也不得复用该 thread 的历史、项目
   `cwd`、工具或 event stream。
2. 未来 Agent Host 提供独立、异步于主回答的 title-generation operation。Desktop 只提交一个
   `operation_id`、关联 session/task ID 与首条用户文本；Host 不读取 Desktop conversation DB，
   不保存标题为业务权威。
3. Host 在新建的空临时目录上创建 `ephemeral=true` Runtime thread，固定 read-only、
   `approvalPolicy=never`、无 project environment，并拒绝/中断任何 tool、approval 或 file/platform
   write item。ephemeral thread 没有 rollout path；完成后 unsubscribe 并清除 Host correlation。
   canonical Runtime 明确拒绝对 ephemeral thread 调用 `thread/delete`，因此不得伪称已执行该删除。
4. Title prompt 固定为 `title-v1`，只把首条用户文本放在明确的 untrusted-data delimiter 内。输出使用
   turn-scoped strict object schema：

   ```json
   {
     "type": "object",
     "properties": { "title": { "type": "string" } },
     "required": ["title"],
     "additionalProperties": false
   }
   ```

5. Runtime/provider 输出不是可信数据。Host/Desktop 在 parse 后执行 NFC normalization、去首尾空白、
   单行化，并拒绝空值、控制字符、bidi override、HTML/Markdown 结构或超过 40 grapheme 的原始结果；
   不依赖 provider 对 `maxLength` 的实现。
6. 每个 session 的自动标题预算是首次 1 次、仅在确定失败时允许 1 次受控重试，总计最多 2 次模型
   调用。timeout、429/5xx、refusal、incomplete、schema invalid、未知响应或取消都不得影响主回答；
   未知结果不自动 retry。fallback 是首条用户文本第一条非空单行的安全 40-grapheme 截断，无可用文本
   才使用“新任务”。
7. Desktop SQLite 是标题权威。`title_source=user` 后，迟到的 model result 必须丢弃；相同
   `operation_id` 幂等，列表加载不得触发生成。Runtime `thread/name/set` 只保存调用方提供的名称，
   不是生成器，也不是 Desktop 标题权威。

### 2. 只允许公开 summary 的最小事件投影

1. Host 新增的 Runtime 输入 allowlist 仅为：
   - `item/reasoning/summaryPartAdded`；
   - `item/reasoning/summaryTextDelta`；
   - reasoning 类型的既有 `item/completed`，仅用于完成边界。
2. 对外只新增两个 session-event v2 variant：
   - `item.reasoning_summary.part_added`：既有 envelope 必含 `turn_id`、`item_id`，payload 只含非负
     `summary_index`；
   - `item.reasoning_summary.delta`：同一 envelope，payload 只含 `summary_index` 与 `delta`。
   reasoning `item/completed` 继续使用既有 `item.completed` + `payload.item_type="reasoning"` 作为完成
   边界，不新增第三个 completed variant，也不携带 summary/raw content。
3. `item/reasoning/textDelta` 永远丢弃；reasoning `item/completed` 中的 raw `content` 永远不解析、
   不投影、不记录。Host 也不从 completed item 的 `summary` 重建正文；只有明确的 public summary
   notifications 可以成为产品数据。
4. Desktop 按 `(turn_id, item_id, summary_index)` 累积 delta。首个 delta 可以隐式创建 index 0，
   `part_added` 是可幂等的边界提示，不能要求其一定先于 delta；Host envelope 的 event ID/stream
   sequence 负责至少一次交付去重。
5. Host 只接受 `summary_index` 0–31、单 delta 最多 16 KiB UTF-8、每 turn 累计最多 128 KiB
   public-summary text。缺 ID、负数/越界 index、无效 UTF-8、超限或内部状态冲突时，丢弃该 summary
   item 的全部已累积正文并标记 unavailable；主 answer/turn 继续。日志和 metric 只记录 method、稳定
   reason 和非内容计数，不记录 delta。
6. summary 未请求、provider 不支持、没有事件、事件被拒绝或中途丢失，都是正常降级：UI 只显示
   “处理中/已处理 + 时长”，不展示正文、不报 conversation 失败、不尝试从 raw reasoning 回退。

### 3. Contract 与启用顺序

1. 当前 `agent/session-event.schema.json` 是 `schema_version=1` 的 closed `oneOf`。向 v1 producer
   直接加入新 variant 会破坏严格旧 consumer，因此最高 contract impact 是 `breaking`，不能标为
   普通 additive。
2. yijie-contracts 未来必须新增 session-event v2 权威 schema/fixtures。现有 event endpoint 默认只
   返回 v1；新 Desktop 通过明确 `event_schema_version=2` negotiation 订阅 v2。先发布能忽略未知 v2
   variant 且不推进非法 terminal/cursor 的 consumer，再发布 Host producer，最后分别打开
   summary/title flags。
3. 在 G2A 前不得修改 Host/Runtime/Contracts/Desktop 业务源；在 v2 immutable contract pin 和
   consumer conformance 之前，Host 保持现有 8-event allowlist、summary=`none`、标题 model flag off。

### 4. MiniMax 合成验证审批方案

本 ADR 不授权外部调用。Owner 可单独批准最多两个、每项仅一次的合成短请求；不能把其中任一项
重跑到成功：

1. `MM-126-001 / title`：固定 Runtime/Host candidate、临时 app-data/CODEX_HOME/空 cwd、
   `ephemeral=true`、read-only/never、无工具、合成中文首条消息、`title-v1` strict schema。验证请求
   被 MiniMax Responses 接受、terminal 完成、JSON 可解析且经 sanitizer 为 1–40 grapheme、无 rollout
   path/项目读取/额外 action。一次 timeout/429/5xx/refusal/incomplete/schema invalid 即记录 FAIL 或
   DEGRADED，不重试。
2. `MM-126-002 / public-summary`：同一固定 pin 与临时边界，合成不超过 200 字的简单推理题，显式
   `effort=high`、`summary=concise`，答案要求不超过 80 字。验证 answer terminal 与是否收到 canonical
   public-summary notifications；收到且只命中 allowlist 为 PASS，没有 summary 但 answer 正常为
   DEGRADED（采用时长-only），出现 raw reasoning/secret/tool 或 answer 被 summary failure 破坏为 FAIL。

两个请求均要求 key 只从 owner-only provider 配置注入，日志/文档不记录 key、完整 request/response、
真实路径或用户文本；单请求 hard timeout 120 秒，总调用数 hard cap=2，记录实际 model、Runtime/Host
full SHA、请求计数、latency、status、provider usage/cost（若响应提供）和脱敏断言结果。任一 auth、
rate-limit、provider 5xx 或协议异常都停止该请求，不扩大次数；验证完成后删除临时目录。

### 4.1 Owner 批准与一次性验证结果

段成威于 2026-08-02 批准 ADR-0015、DEC-126-007，以及 `MM-126-001/002` 各一次、总计最多两次
MiniMax 合成验证；同时明确 G2 仍不通过、不开始编码。验证使用固定 `codex-cli 0.144.6`
（SHA-256 `1ef4f1daba0c5ac267e9bf661d129c3dfc59ffe5cd9ab7767b22a1e9508df1fe`）、
Host candidate `34e94acf293f6daad61c4d42fa47028a2d1318e4`、`MiniMax-M3`/`minimax`，并把
request/stream retry 均设为 0。key 仅注入预期 Runtime child；两次均使用 0700 临时根、临时
`CODEX_HOME`、空 cwd、read-only/never、`ephemeral=true`，完成后清理临时根。未输出或写入 key、
完整 request/response、标题、answer 或 reasoning 正文。

| Validation | Calls | Latency | Terminal/usage | 安全与契约断言 | 结论 |
|---|---:|---:|---|---|---|
| `MM-126-001 / title` | 1，0 retry | 1,853 ms | completed；5,217 input / 15 output / 0 reasoning / 5,232 total tokens；cost 未提供 | strict object 可解析；sanitizer PASS，18 grapheme；`thread.path=null`；0 tool、0 rollout candidate、0 secret leak；临时根已删除 | PASS；证明该固定 pin 的单样本 structured title 可用，不替代后续 Eval |
| `MM-126-002 / public-summary` | 1，0 retry | 9,256 ms | answer completed；5,521 input / 143 output / 121 reasoning / 5,664 total tokens；cost 未提供 | 0 `summaryPartAdded`、0 `summaryTextDelta`；收到 7 个 raw `reasoning/textDelta`，completed reasoning 含 1 个 raw content part；0 tool、0 secret leak；`thread.path=null`；临时根已删除 | FAIL；命中 frozen raw-reasoning fail-closed 条件，不能公开 summary |

因此两次调用预算已经耗尽，不得重跑。标题方案保留，但 production flag 仍须等待 Host/contract/Desktop
实现、conformance 与 Eval。按本文当时的 public-summary-only 门槛，MM-126-002 为 FAIL；段成威随后通过
ADR-0016 明确改变产品边界，要求展示 raw reasoning。该历史结果不能事后改写为 PASS，但可以作为新
raw-reasoning 设计的能力输入。Q-009 按“public summary不稳定且不再作为产品要求”关闭；G2仍不通过。

## 备选方案

### 在用户 thread 中增加隐藏标题 turn

会污染历史、token/context、恢复和用户可见语义，也让删除/重放更复杂，因此拒绝。

### 只使用 `thread/name/set`

它只持久化调用方提供的字符串，不执行模型生成，无法满足自动标题，因此拒绝作为生成方案。

### 转发完整 reasoning item 或 raw delta

completed item 同时可能含 public summary 与 raw content；整体转发会突破 confidential/restricted 边界，
因此拒绝。只允许 explicit summary notifications。

### 直接给 v1 event union 加 variant

旧严格 consumer 会验证失败；在 consumer inventory/兼容窗口未完成前风险不可接受，因此拒绝。

## 影响

- 未来 yijie-agent-host 需要隔离 title operation、ephemeral lifecycle、strict output validation、summary
  allowlist/caps 和 v2 event projection；Host 仍不成为 conversation/title 数据库。
- 未来 yijie-contracts 需要 versioned v2 source/fixtures/generation 与 breaking/consumer matrix；本 ADR
  不修改契约源。
- 未来 yijie-desktop 需要按 index 累积 public summary、fail-closed 降级、model/user title precedence 与
  独立 flags；本 ADR 不授权实现。
- 固定 Runtime source 预计无需变更；只有后续 approved conformance 证明 canonical capability 不足时，
  才停止并重新评审 Runtime candidate。

## 风险

- MiniMax 在本次固定 pin 中接受 `text.format` structured title，但 public-summary 请求未产生 public
  summary event，反而提供 raw reasoning。本文门槛下该结果为 FAIL；ADR-0016 已取代“永远丢弃 raw”与
  “时长-only”结论，未来按 versioned raw-reasoning contract重新设计，不追加本轮 provider调用。
- ephemeral thread 不写 rollout，但可能在 Runtime 进程内保留至 unsubscribe 后的延迟卸载；不能宣称
  内存即时法证擦除。
- provider summary 的内容仍是不可信模型输出；即使公开也可能错误或含用户输入，需要安全渲染和删除
  级联，不能作为权限/审计事实。
- summary caps/事件版本属于 wire 语义；未经 v2 contract/consumer conformance 直接实现会造成丢流或
  旧客户端崩溃。

## 证据与参考

- 固定 Runtime source：`yijie-codex@3aa317cebbbc9c743f6b1a18522be11a7ebb5d6f`
- 固定 Runtime artifact：`codex-cli 0.144.6`，SHA-256
  `1ef4f1daba0c5ac267e9bf661d129c3dfc59ffe5cd9ab7767b22a1e9508df1fe`
- Agent Host baseline：`yijie-agent-host@34e94acf293f6daad61c4d42fa47028a2d1318e4`
- Agent event contract baseline：`yijie-contracts@9ec34abd6e7dfb5a23b0154d467694167224ebbb`
- OpenAI Responses public summary event：<https://developers.openai.com/api/reference/resources/responses/streaming-events#response.reasoning_summary_part.added>
- OpenAI Responses Structured Outputs：<https://developers.openai.com/api/docs/guides/structured-outputs>

## 后续动作

- [x] 段成威于 2026-08-02 批准 ADR-0015 与 DEC-126-007；Q-008 已关闭，但不等于 G2 通过或实现授权。
- [x] 段成威批准 `MM-126-001/002` 各一次；两次预算已按边界执行完毕，未重试。
- [x] 已回填 title PASS 与 public-summary FAIL 历史证据；Q-009 按负向事实关闭，reasoning产品语义由 ADR-0016 接续。
- [ ] G2 继续关闭 Q-010、DEC-126-011/012、Desktop Pattern 与 versioned contract design。
