# FEAT-164 时序契约矩阵

本文件与feature.yaml保持同一Scenario/Invariant/Test/Slice ID。TCONF-164-01已在Host S1实现并通过普通状态conformance；S2 Host子集已实现并验证，TCONF-164-02全链及S3—S4仍为计划目标。当前结果与范围见21/22，不把本机检查记为真实模型验证。

## 六阶段

| Phase | 权威动作 | 提交/通知与失败语义 |
|---|---|---|
| producer | 受管Host/Native接收明确切换或新turn意图；拒绝退役新执行 | 先验身份/权限/来源/未决状态；缺项不产生模型请求 |
| persistence | 保存新迁移operation意图、兼容schema和准入状态；Runtime确认后提交selection/revision | 不把原操作payload或历史身份改为新模型；跨Runtime与Host无分布式原子事务 |
| notification | 提交后公布回执/Selection和UI状态 | Desktop失联可重读终态回执及当前Selection，不能用旧回执回退revision |
| replay | 读取原operation/plan/run及持久阶段 | missing不证明never-sent；只读回执不触发标题/模型；未知保持 |
| terminal | 所有required提交与回执已确认后标成功；取消/失败/未知分别保存 | Runtime成功但Host未提交不能显示成功，不自动业务重试 |
| cleanup | 正常退出/收敛collector、worker及临时资格 | 不强杀；未安全退出则停止激活并报告，无旧请求跨cutover |

## 有向场景

- FLOW-LIVE-164：producer → persistence → notification → terminal → cleanup。
- FLOW-REPLAY-164：persistence → replay → notification → terminal → cleanup。
- FLOW-PLAN-164：producer → persistence → notification → terminal → cleanup。

这些是一次操作/恢复的逻辑阶段：恢复中读取durable意图后可产生新的审计记录，但不在机器阶段图中制造循环。不同重试实例保留同一operation绑定和阶段事实，不重用历史成功标签。

## 不变量与测试

| Invariant | 场景 | 切片/测试 | 断言 |
|---|---|---|---|
| TINV-164-01 | FLOW-LIVE-164 | S1 / TCONF-164-01 | 未确认来源及活动身份不产生新执行；catalog/TOML任一未知组合不放宽校验；切换截止点后零K3 |
| TINV-164-02 | FLOW-LIVE-164、FLOW-REPLAY-164 | S2 / TCONF-164-02 | 原operation/payload/profile/digest保留；Runtime回执与Host提交窗口区分；unknown不推定模型；无证明不取消 |
| TINV-164-03 | FLOW-PLAN-164、FLOW-REPLAY-164 | S3 / TCONF-164-03 | worker claim/send之前准入生效；计划领域事务撤有效授权并处理future slots，历史run和额度事实不改 |
| TINV-164-04 | FLOW-LIVE-164、FLOW-REPLAY-164、FLOW-PLAN-164 | S4 / TCONF-164-04 | 真实启用调用面/流式/辅助模型/正常重开不恢复退役执行；来源、预算、退出和三项final verdict独立 |

## 拟实现的精确测试入口

| Test | Repository | 拟用命令 | 当前状态 |
|---|---|---|---|
| TCONF-164-01 | yijie-agent-host | go test ./internal/codex -run '^TestFEAT164ActivationAndRetiredAdmission$' -count=1 | PASS；真实存在、已执行10个普通子例，证据s1-tconf-164-01.log |
| TCONF-164-02 | yijie-agent-host | go test ./internal/session -run '^TestFEAT164MigrationReceiptAndRecovery$' -count=1 | PLANNED，NOT RUN；并需Desktop私有迁移/取消跨端配套 |
| TCONF-164-03 | yijie-desktop | cargo test --manifest-path src-tauri/Cargo.toml feat164_plan_retirement_before_dispatch -- --exact | PLANNED；最终模块限定名在实现后固定，NOT RUN |
| TCONF-164-04 | yijie-desktop | node --test scripts/tests/feat164-candidate-closure.test.mjs | PLANNED，NOT RUN；不代替真实E2E |

TCONF-164-01已存在并执行；其余名字仍为计划，不声称文件/用例已存在。运行前必须读取测试代码、核实selector实际命中、正确模块全名及执行数非0；最终exact命令在首次产品执行前写入本文件/YAML，禁止空跑PASS。每个test同时有本slice的local/boundary/vertical证据，不借其它slice旧通过。

## 安全恢复案例

普通状态机输入表示：意图已存未调用、Runtime回执已获未提交、Host已提交Desktop未收、已完成重复查询、unknown、已确认never-sent、计划due但退役。用纯逻辑/普通本机协议正常返回验证，不强杀、不破坏文件权限、不伪装Runtime。原生只读状态只能帮助判断idle/运行，不用于证明模型。

完整实际调用路径的harness为H-F164-LOCAL，未来使用canonical受控本机bootstrap、合成数据和获授权的真实小规模调用。harness分类product/harness/platform/gate，qualification/timeout/normal cleanup均NOT RUN；禁止行为不能成为negative control。

任何source/pin/runtime/schema/migration/role/参数/准入顺序/测试driver/平台变化均使相应证据STALE，按transitive依赖重验。当前范围沿用已批准设计及本轮S1实施许可；不伪造独立人工审查或发布批准。
