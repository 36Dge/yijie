# {{FEATURE_ID}} Temporal Contract Matrix

> 本文是跨进程、跨仓、跨版本、持久化或重放行为的时序权威索引。即使没有公共 wire 变化，也必须填写；完全不涉及时序边界时写 `N/A + 可复核理由`。

`feature.yaml.temporal_contract_matrix` 是机器可校验索引；本文中的 Scenario、Invariant 与 Test ID
必须与 YAML 精确一致。G2 起 checker 会验证六个 closed phase、场景有向顺序无环、required phase
覆盖、Invariant→Scenario 和 Invariant→Executable Test 引用闭合。

## 1. 适用性与权威源

- 适用结论：TBD
- 权威契约/设计/代码位置：TBD
- Producer Owner：TBD
- Persistence Owner：TBD
- Consumer Owner：TBD

## 2. 事件与持久化阶段

| Phase ID | 前置状态 | Producer 动作 | Durable commit/authority | Notification | Consumer projection | 失败与恢复 |
|---|---|---|---|---|---|---|
| TMP-001 | TBD | TBD | TBD | TBD | TBD | TBD |

阶段必须覆盖适用的 producer、持久化提交、通知、replay、terminal 和 cleanup；不得只描述 happy path。
phase 只有在确实不适用并记录 Technical Owner、批准时间与理由时才能 N/A；declared scope 所强制的
producer/cleanup，以及适用的 persistence/notification/replay/terminal，不接受 N/A 例外。

## 3. 顺序与不变量

| Invariant ID | 不变量 | Duplicate/out-of-order | Terminal rule | Crash/restart rule | Fail-closed behavior |
|---|---|---|---|---|---|
| TINV-001 | TBD | TBD | TBD | TBD | TBD |

至少明确：

- durable commit 与 notification 的先后；
- live notification 与 history/replay 汇合时的去重和顺序；
- terminal 是否允许越过尚未提交或尚未发布的中间状态；
- restart、cancel、failure 与 cleanup 如何清除 pending state；
- ACK、重试、幂等键、ordinal/version/cursor 和过期语义；
- 非法回退、身份冲突和未知状态如何 fail closed。

## 4. 可执行 Temporal Conformance

| Test ID | Invariant IDs | Producer fixture/driver | Consumer/reader | Exact command | Environment | Expected evidence |
|---|---|---|---|---|---|---|
| TCONF-001 | TINV-001 | TBD | TBD | TBD | TBD | TBD |

每个阻断不变量必须至少映射一个能在错误实现下失败的 executable test。只有静态图或文字评审不能替代 temporal conformance。
`feature.yaml.temporal_contract_matrix.executable_tests[]` 还必须把每个 TCONF ID 绑定 repository、
exact command、负责 slice；该 slice 通过 G3 前记录 PASS、exit code、ISO 时间、transitive commits
与唯一 evidence marker。每个 invariant 还必须用 `slice_ids` 列出其适用的 required slices；每个
适用 slice 都必须至少有一条属于自身的 required TCONF，不能借用另一切片尚未执行的测试通过 G3。

## 5. G2V 代表路径

| Harness ID | 覆盖的 Phase/Invariant | 真实平台 | Production bootstrap | 最小代表性数据 | 未覆盖风险 |
|---|---|---|---|---|---|
| H-VERTICAL-001 | TBD | TBD | yes/no | TBD | TBD |

## 6. 变更与失效规则

以下任一变化必须使相关 boundary/vertical evidence 失效，并重跑受影响测试：

- producer/consumer、契约 pin、schema、顺序、默认值或错误语义；
- persistence transaction、notification、replay、terminal 或 cleanup；
- runtime/platform、production bootstrap、harness/controller 或 canonical fixture；
- 任何被 structured freshness 引用的 commit、contract/fixture、harness digest 或平台/环境版本。

## 7. Owner 评审

| Owner | 结论 | 日期 | 证据/例外 |
|---|---|---|---|
| Technical | Approve/Reject | TBD | TBD |
| Producer/Consumer | Approve/Reject/N/A | TBD | TBD |
| Security/Data | Approve/Reject/N/A | TBD | TBD |
