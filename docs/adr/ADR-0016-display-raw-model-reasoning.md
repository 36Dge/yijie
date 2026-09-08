# ADR-0016: 展示 Raw Model Reasoning 并阻止静默降级

## 状态

Accepted

## 日期

2026-08-02

## 决策负责人

段成威

## 关联需求

- `FEAT-126-public-task-authorization-hardening`
- `DEC-126-008`（仅 reasoning 展示部分被本 ADR 取代）
- `DEC-126-015`
- `Q-009`、`Q-016`
- `ADR-0015`（标题隔离部分继续有效；public-summary-only 部分被本 ADR 取代）

## 背景

FEAT-126 原 Accepted 决策只允许展示 provider/Runtime 明确标记为公开的 reasoning summary，禁止
投影 raw reasoning；没有 summary 时 UI 降级为状态/时长。Owner 批准的 `MM-126-002` 单次验证中，
固定 `MiniMax-M3`/Runtime pin 正常完成 answer，但没有产生 `summaryPartAdded` 或
`summaryTextDelta`，而是产生 7 个 `item/reasoning/textDelta` 和 1 个 completed raw content part。

段成威在审阅该证据后于 2026-08-02 明确改变产品与安全边界：不再要求 public summary；UI 必须展示
Runtime/模型提供的具体 raw reasoning 文本，不能静默退化为仅状态/时长，并批准按下述六点执行。
这是对 Accepted ADR/产品语义的显式取代，不把历史验证结果改写成另一套门槛下的 PASS。

## Contract Impact

- 分类：`semantic`（FEAT-126 reasoning 子边界；Feature Package 总体仍因 Public Tasks 为 `breaking`）。
- 原因：从“raw 永不成为产品数据”改为“raw 是可展示的模型输出”，改变 Host event projection、Desktop
  consumer、失败语义、数据分类与未来持久化边界；即使 event v2 尚未形成 source contract，也不能按
  `none` 或普通 UI 文案处理。
- 权威源：上游 Runtime canonical app-server schema → 未来 yijie-contracts session-event v2 兼容投影
  → Agent Host producer → Desktop consumer。不得由 Host/Desktop 手写相互漂移的影子 payload。

## 决策

### 1. Raw reasoning 成为明确的产品输出

1. UI 展示固定 Runtime 提供的 `item/reasoning/textDelta`，并在 terminal/completed item 中存在 raw
   reasoning content 时按未来契约完成去重、对账和封口。
2. 产品名称使用“模型推理记录”，不得声称它完整、稳定、真实揭示模型全部内部思维，也不得把它
   描述成 provider 审核过的 public summary。
3. `MM-126-002` 继续记录为 ADR-0015 public-summary-only 门槛下的 FAIL；它同时证明该固定 pin 在该
   合成样本中存在 raw reasoning，但不证明跨输入稳定性、内容安全、持久化正确性或生产质量。

### 2. UI 不允许静默降级

1. 选择的 Runtime/model pin 若不能为 reasoning-enabled turn 提供至少一个非空 raw reasoning item，
   则判定该组合与 FEAT-126 不兼容，相关功能不得通过 G2/G4/G5 或打开 feature flag。
2. 不得用 answer、工具输出、伪造模板、public summary 缺失提示或仅状态/时长冒充具体推理文字。
3. 单 turn 的断流、无效 UTF-8、越界、缺 completed、顺序/去重冲突必须进入明确的
   `reasoning_incomplete`/`reasoning_unavailable` 错误状态；answer 可独立完成和保存，但该结果不能作为
   reasoning 验收 PASS，且达到发布停止阈值时关闭相关 feature flag。

### 3. 只按纯文本和不可信模型输出处理

1. Desktop 以纯文本节点渲染；不执行 HTML，不把 Markdown 当可信富文本，不自动打开 URL，不把文本
   解释为命令、tool、approval 或权限授予。
2. UI 保留系统原生选择与复制语义，但不增加产品级复制按钮；折叠入口、状态、时长和具体文本均需
   满足键盘、VoiceOver、reduced-motion 与流式防播报风暴要求。
3. raw reasoning 可能复述用户输入、项目片段、system/developer instructions 或其它敏感内容；产品披露
   必须说明其由模型生成且可能不准确/不完整。不能声称 sanitizer 能可靠删除所有语义性秘密。

### 4. 禁止进入日志、遥测和审计正文

Host、Desktop、Runtime adapter、metrics、trace、crash report、receipt 和 provider error projection 均不得
记录 raw reasoning 正文。允许的 content-free 观测仅限 IDs 的受控关联、event/byte count、duration、
status、drop/error reason 和 provider/model/runtime pin；label 不含正文、prompt、路径、title 或 key。

### 5. 持久化边界已批准

段成威于 2026-08-02 批准 `DEC-126-016` 并关闭 `Q-016`：raw reasoning 在流式阶段由 Desktop 内存
reducer 展示，terminal 对账后写入 Desktop 本地 SQLCipher；中断时允许保存显式 `incomplete` partial
record。历史 session 按需加载，并随 session 通过 FK cascade、`secure_delete` 与批准的 WAL checkpoint
边界物理删除。不得使用 localStorage、Host bbolt/log/replay、云端或 Runtime rollout 作为 Desktop 历史权威。

选择本地加密持久化，理由如下：

- FEAT-126 已要求点击 session 加载完整历史；仅内存展示会让同一 turn 重开后语义消失，造成历史与
  实时视图不一致；
- ADR-0013/0014 已冻结 Desktop SQLCipher authority、Keychain key、文件权限、backup 披露与永久删除
  流程，可在既有边界中承载这类更敏感的模型输出；
- Desktop 不应依赖 Runtime rollout 或 Host replay 作为产品历史权威；
- 独立表/FK cascade 可把 raw reasoning 与 session 删除、WAL checkpoint 和 content-free receipt 对齐。

代价是本地敏感数据量和泄露面扩大，因此 G2 后续设计必须冻结 schema/migration、单 turn容量/写放大、
partial/interrupted状态、历史分页及删除验证；数据分类采用 `restricted`，OS backup/普通卸载披露沿用
ADR-0014，不能只增加一个 `text` 字段。DEC-126-016的批准不是schema或代码实施授权。

### 6. Gate 与调用边界不变

- G2 已于2026-08-02通过；仅允许进入G2A source-contract candidate评审，仍不开始Host/Desktop/Runtime/API业务代码。
- `MM-126-001/002` 两次批准预算已经耗尽，不新增第三次调用，不把旧请求按新门槛重跑到成功。
- 新的 raw-reasoning fixture、contract/conformance、migration/security/E2E/Eval 计划必须在 G2 冻结，
  真实 provider 扩展验证需段成威另行明确批准。

## 备选方案

### 继续 public-summary-only + 时长降级

风险最小，但与段成威最新明确产品要求冲突；被拒绝。ADR-0015 的历史证据与标题决策继续保留，
summary-only 产品结论由本 ADR 取代。

### 仅当前流式内存展示

减少持久化暴露和 migration，但历史 session 无法恢复具体推理，重启/切换 session 后同一 turn 表现不
一致；被 DEC-126-016 拒绝。

### Desktop SQLCipher 本地持久化

历史一致、可懒加载、可纳入既有 session 物理删除和无云端正文边界；代价是 schema、容量、敏感数据
分类、backup 和删除验证扩大。由 DEC-126-016 选定。

## 影响

- ADR-0015 的隔离标题、strict output、title fallback/call cap 继续有效；其 public-summary-only、raw drop
  和时长降级条款停止指导 FEAT-126 新设计。
- DEC-126-008 reasoning 展示结论被 DEC-126-015/本 ADR 取代；G1 原产品范围的其它结论不变。
- 未来 yijie-contracts 需要新的 versioned raw-reasoning event schema；consumer-first 后 Host 才能发送。
- yijie-agent-host 必须精确投影、限流、去重并脱敏，不得把完整 Runtime item 或 provider response透传。
- yijie-desktop 必须纯文本渲染，并将terminal/显式incomplete reasoning record写入SQLCipher；不能用
  localStorage、日志、Host replay或Runtime rollout顶替。
- Public Tasks auth、SQLite/delete、Pattern 和 contract 其它 G2 blockers 不因本 ADR 自动关闭。

## 风险

- raw reasoning 可能包含 prompt、项目片段、错误内容或模型不希望作为稳定接口的数据；纯文本渲染只能
  阻止主动 HTML/命令执行，不能消除语义性敏感信息。
- provider/Runtime 版本可能改变 raw event 的存在、顺序、内容和 completed 对账；必须固定 pin 并做
  consumer conformance/Eval。
- 不允许静默降级意味着 provider 兼容性问题会阻断 feature 发布；不能为了过 Gate 伪造或复用 answer。
- 若批准持久化，SQLCipher/secure-delete 仍不能承诺清除 APFS、SSD、OS backup 或第三方备份中的所有
  物理痕迹；沿用 ADR-0014 限定披露。

## 后续动作

- [x] 段成威于 2026-08-02 明确批准六点 raw-reasoning 展示建议，取代 public-summary-only 产品语义。
- [x] 保留 `MM-126-002` 原 FAIL 证据，不追加 provider 调用，不开始编码。
- [x] 段成威于 2026-08-02 批准 DEC-126-016并关闭Q-016：Desktop SQLCipher持久化、历史懒加载、session级联物理删除。
- [x] DESIGN-126-003 已冻结 raw-reasoning v2 schema、caps/sequence/finalized reconciliation、SQLCipher migration/history/cascade候选，并提交 DEC-126-017；fixed Runtime fixtures 4/4 PASS，等待 Owner 批准。
- [x] 段成威于2026-08-02批准DEC-126-017、DEC-126-011/012与Desktop Pattern并宣布G2通过；进入G2A source-contract candidate评审，业务编码仍未授权。

## 2026-09-08 FEAT-132 已授权替代条款

用户授权原生接入改造。本节替代上文“去重、对账和封口”中由客户端解释 reasoning 执行结果的要求；允许展示 Runtime 实际提供且现有权限允许的 raw reasoning 的产品边界保持。

- 传输重复只按原生 stream cursor 去重；唯一 Native 显示缓冲按原生 Item ID / contentIndex / summaryIndex 追加。
- item/completed 的 content/summary 最终对象直接替换临时内容，不做正文前缀比较，不因 Turn 结束制造 reasoning complete/incomplete/failed。
- 缺 completed、断线、解析或容量问题通过独立 availability / diagnostic 明示；不能覆盖 Turn 原生执行状态。保留已观察内容，不把 summary 或合成文案冒充 raw reasoning。
- 原生事实及显示副本仍在 SQLCipher 加密保存，旧 reasoning 作为只读档案可访问；不得运行旧 accumulator 或历史 reducer。

见 [FEAT-132 调整说明](../features/FEAT-132-desktop-conversation-domain-state-machine/03-native-protocol-adjustment.md)。原历史验证和额度不转移到本次 D4。
