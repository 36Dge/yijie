# FEAT-164 时序契约矩阵

> 当前口径：原主工作目录构建/日常入口及正常系统退出资格以[76](76-primary-workspace-execution.md)、[77](77-primary-system-quit-root-cause-and-plan.md)和[当前验收矩阵](current-acceptance-matrix.md)为准。当前源码为原`CrossBSD/yijie-desktop`，generation `20261028-02`；71—74保留为上一来源/清理历史。新来源三轮服务/模型目录/正常退出/数据后态通过，App历史界面因锁屏按Owner指示跳过，未记PASS；既有接受替代和永久移除范围保持。

## 第59号部署推进记录（历史）

当前部署推进以[59](59-daily-cutover-minimal-plan-and-authorization.md)为准：G4因daily Home连续性问题重新pending。原时序不变量、S1—S4及三项final的已接受本地证据保持；本轮不改时序契约、不运行日常数据。下方58判定按其本地历史范围解释。

## 第58号本地验收结论（历史，2026-10-27，S4AE）

以[58 安全替代接受与最终收口](58-owner-accepted-substitute-and-final-closure.md)、feature.yaml和[当前矩阵](current-acceptance-matrix.md)为准。Owner明确接受57号never-sent正常Native API与生产消费链的安全分层替代；S4/TCONF04及三项适用最终验收按该方式收口，G4为本地代码完成。**完整App正向never-sent取消的原始执行状态仍为NOT RUN**，没有改写为已执行。原自然unknown缺Host回执，安全拒绝重发通过，原记录仍未恢复ready。

本轮仅只读审计和治理更新，真实/本机模型HTTP新增均0；产品、Runtime核心/补丁、来源锁不变。不启动或迁移日常库，日常候选保持prepare-only，G5/G6及正式交付仍pending。搜索答案正确性、亮暗/键盘/最小窗口专项保持OWNER_EXCLUDED，不恢复为待办。以下早期阶段记录按原时间和来源解释；本节覆盖其中过期的推进顺序、预算授权和“当前未通过”描述。

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
| TINV-164-04 | FLOW-LIVE-164、FLOW-REPLAY-164、FLOW-PLAN-164 | S4 / TCONF-164-04 | 真实启用调用面/流式/辅助模型/正常重开不恢复退役执行；来源、预算、退出和剩余适用final verdict独立（排除Owner已移除的外观专项） |

## 已实现的精确测试入口

| Test | Repository | 命令 | 当前状态 |
|---|---|---|---|
| TCONF-164-01 | yijie-agent-host | go test ./internal/codex -run '^TestFEAT164ActivationAndRetiredAdmission$' -count=1 | PASS；真实存在、已执行10个普通子例，证据s1-tconf-164-01.log |
| TCONF-164-02 | yijie-desktop（组合Host） | 下方完整driver命令，保留Host精确子入口 | PASS；五组零skip、源工作树干净，见25/evidence/s2-conformance-final/result.json；平台不在此PASS内 |
| TCONF-164-03 | yijie-desktop | node scripts/feat164-s3-conformance.mjs /tmp/feat164-s3-native-final | PASS；5项模块限定exact入口各1通过/0ignored，见26/evidence/s3-native-final |
| TCONF-164-04 | Desktop/Host | feat164-s4-conformance.py、feat164-s4b-conformance.py、Host feat164-s4e-conformance.py；完整参数见s4j-qualified-driver-results.json与S4I | 三组safe subset均有实际证据；完整资格仍NOT RUN，不代替App/真实E2E |

TCONF-164-01、02、03均已实现并有本轮当前来源结果，精确命令在feature.yaml和s4j证据中。04的closure单测及三个driver也已真实存在，不再称“待创建”；其各自覆盖边界保持，不能只运行closure五项就宣称完整TCONF。所有driver必须非零命中且零skip，失败保留。S2当前native组精确17项并使用原candidate环境；修前3个IPC门禁失败、修后57项通过见36。

## 安全恢复案例

普通状态机输入表示：意图已存未调用、Runtime回执已获未提交、Host已提交Desktop未收、已完成重复查询、unknown、已确认never-sent、计划due但退役。用纯逻辑/普通本机协议正常返回验证，不强杀、不破坏文件权限、不伪装Runtime。原生只读状态只能帮助判断idle/运行，不用于证明模型。

完整实际调用路径的harness为H-F164-LOCAL，历史资格与真实r2结果见20；当前来源仍需新资格和真实G2V。分类器7项普通状态/协作取消检查已通过，不表示完整当前harness qualified。禁止行为不能成为negative control。

任何source/pin/runtime/schema/migration/role/参数/准入顺序/测试driver/平台变化均使相应证据STALE，按transitive依赖重验。当前范围沿用已批准设计及本轮S1实施许可；不伪造独立人工审查或发布批准。

## 历史S2配套入口（当前命令见feature.yaml）

`python3 scripts/feat164-s2-conformance.py --host-source ../yijie-agent-host --runtime-binary /Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/build/kimi-k31-pro-r2/aarch64-apple-darwin/codex --runtime-manifest /Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/build/kimi-k31-pro-r2/aarch64-apple-darwin/runtime-manifest.json --output /tmp/feat164-s2-conformance-final` 从Desktop资格工作树执行。输出目录必须新建，失败保留，不覆盖旧run。Host入口保持原精确名字；driver组合Host25个状态/迁移子例、Native派发/恢复/迁移与实际边界。边界中的Rust忽略测试只由独立Go Host test传入新建临时根/端口启动，默认不运行，不接受当前App作为验收目标。

Host实际handler/service/Store及固定Runtime在测试bootstrap中运行，正常EOF停止后重开；Native正常SQLCipher重开。与canonical App/GUI、公开部署或供应商资格明确分开。结果与剩余门禁按25及实际run追加。

S3实际入口为Desktop `scripts/feat164-s3-conformance.mjs`，核心模块全名`chat::schedules::model_retirement_tests::feat164_plan_retirement_before_dispatch`。当前S3 source/local时序PASS，App/跨端/平台完整门禁延期；清理/退款保护也覆盖三条expiry路径。完整五项与S2当期来源复验见26；不把原占位命令空跑当PASS。
