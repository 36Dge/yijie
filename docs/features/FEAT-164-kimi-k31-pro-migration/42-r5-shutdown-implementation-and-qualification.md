# FEAT-164 S4O：r5 最小关闭修复与下游资格

2026-10-26，Asia/Shanghai。Owner在质疑fork改动必要性后，明确同意确有必要时按41号最小范围实施。本轮已完成必要性复核、六文件补丁、独立r5、Contract First投影与同源App构建；**原生零回合loaded-thread正常退出子集通过，完整App验收未通过，整项仍IN_PROGRESS。** 新增真实模型HTTP为0。

## 为什么需要增加两处修改范围

增加的是两个**既有实现文件的修改范围**，不是新增产品模块：`thread_state.rs`拥有listener状态/取消发送端，`thread_lifecycle.rs`是实际spawn入口。原四文件可以等待RPC、线程与日志，但拿不到listener的完成证明；`clear_listener`发出cancel不等于任务已经退出。仅在外层sleep、延长超时或观察进程退出不能补足这个所有权缺口，Host也没有关闭Runtime内部池/等待listener的API。

保持fork可维护性的做法是：上游固定源码`codex-rs/`逐字不改，只新增可重放0011补丁，在canonical临时源码中应用。六处仍为40号四处加上述两处；没有改core/thread_manager、turn_processor、command/process管理器、Provider请求、权限、数据库schema、依赖或公共DTO。新增的构建/验证脚本负责独立r5及留存证据，不是新的运行引擎。

## 实现与复审结论

独占stdio退出按原连接正常清理→最终RPC排空→后台任务/会话正常结束→移除已完成线程→关闭listener注册准入、等待已开始注册、正常cancel并join→outbound/transport结束→日志关闭准入、排空并join→await原有四池close。诊断超时不丢弃等待，不重复提交Shutdown。

listener使用每个manager自己的注册/运行tracker及结果标志；注册与关闭共用同步准入锁，没有持锁跨await。日志join由独立所有者持有，多个关闭调用者及取消后的等待共享typed结果，不把异常当成功。仅独占stdio最终关池；in-process调用者的共享StateRuntime、其他transport保留原策略。复审还排除了“强制退出分支会被误当stdio完成”的假设：固定代码的signal handler仅对非single-client transport启用；本轮未发任何信号或运行强制退出路径。

没有手工checkpoint、TRUNCATE/RESTART/VACUUM、WAL删除、权限故障或强杀。正常SQLite close自身释放WAL与人为清理严格区分。

## 不可变来源与本地提交

| 仓库 | 本轮最终完整提交 | 差异 |
|---|---|---|
| Runtime | `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a` | 六既有文件补丁、r5标准构建/检查、说明 |
| Contracts | `5b5dad9d837ba92abc7c2660d1de1a60f4ed1ba2` | r5来源生成器、lock及派生常量 |
| Host | `894671b7288b34ca0493064cded3e461c924cd32` | 固定投影与制品常量，无Host实现修改 |
| Connectors | `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` | 既有wrapper白名单增加精确11fd；库树未变 |
| Desktop | `c76558e8d4531f4f5c2309055da72f35d2ce4158` | r5/Host来源、启动路径、目录来源与生成物；含前序4448ab9 |
| Skills | `595c927ae101d3d31c234f60565041eee0864680` | 未修改 |

按Runtime→Contracts→消费者顺序固化，仅本地，无新分支、push、tag、PR或发布。Contracts业务源未变；r4与r5全部269份canonical schema字节相等。worker仍消费原固定库树`755f32c45a4c30e805e3c7fe1db89dcb4dcc6e41`，新wrapper登记不升级库或工具权限。增量按semantic候选评审，整项FEAT-164保持breaking；静态形状相等不替代行为资格。

r5 binary SHA256：`283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`；manifest SHA256：`935dae6cf1427a8338b2817c4bfd39e9ae837e51a7f9cefd9117ecfed28b4cee`。独立App位于`feat164-s4o-qualification-20261026/yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI FEAT-164.app`。使用标准入口构建，不覆盖任何旧r4/App；只有编译中间缓存作独立APFS clone，未复制旧bundle冒充新制品。

## 实际验证及局限

- fresh十一patch重放、9项关闭/listener/log单元、6项RPC gate单元、两个package Clippy `-D warnings`通过。首个六文件编译因TaskTrackerToken导入路径失败，核对锁定依赖后修正，失败日志留存。
- Runtime lint、11项兼容validator、3项smoke工具安全测试、2项manifest测试、canonical上游零差异通过。完整`make test`仍被既有100644 `build-input-only.sh`执行位检查阻断；没有修改旧权限或宣称全套通过。补丁的空context行保留标准unified-diff格式，实际源码rustfmt/replay通过，其他提交文件文本检查通过。
- **一次有区分力的真实r5原生检查通过**：无凭据、仅本机Provider地址，initialize/initialized/thread-start/thread-read，零turn，正常stdin EOF；真实loaded listener，exit0，shutdown_forced=false。state/logs/goals/memories四库退出后WAL字节均0，完整副本只读integrity_check均ok，检查未改原文件，完整home保留。只证明input-only零回合子集，不能等同全部core/teardown。
- Contracts生成/check与12项定向测试通过，Go投影包编译通过（无test文件）。Host三项配置/准入测试含十个子项共13项、race及`go vet ./internal/codex`通过；没有运行会自动删除Runtime测试home的历史集成测试。
- Desktop 11项来源/组合测试、脚本语法/lint通过。19项生成检查第三次完整通过：第一次缺少旧Skills要求的历史checkout；补齐原有精确干净来源后，第二次暴露目录generator仍指向旧wrapper提交；核对catalog字节未变，再由generator更新来源并通过第三次。三份原记录保留，未跳过检查/放宽断言，无继续重跑。
- ordinary/market/experts/media四组合来源检查通过；完整media组合canonical App构建及`--prepare-only --reopen`同构建回执检查通过，包括38普通Skills和37专家、worker与媒体适配器。该回执不等于真正UI重开验收。

### App实际观察：尚未就绪，不伪造通过

本轮桌面未锁屏。使用已记录的无凭据环境通过同canonical `--reopen`启动一次，主窗口显示Kimi K3.1 Pro，但持续显示“本地服务尚未就绪”“任务记录暂不可用”，模型/发送/权限控件禁用。因此记录`FAIL_APP_READINESS_FIRST_OBSERVATION`；**根因尚未证明，不能直接归因于缺凭据或r5补丁。** 没有点击重试、发送任务或自动替换配置，没有新的Runtime核心修改。

通过CUA ⌘Q正常退出，canonical进程exit0；新资格Host home无文件、18086无监听，候选数据5528文件前后字节相等。因未证明Host/Runtime实际激活，该App退出只能计进程正常退出，不能计r5 App teardown/checkpoint通过。此前r4 App真实模型与视觉证据仍按原来源保存，不改为r5 PASS。

## 数据、预算与已有改动保护

原497份dirty及7643份受保护文件在晋升前校验全部一致。Connectors原`worker/source.lock.json`含另一需求的未提交`sourceCommit`；普通快进预检发现重叠即停止，只将新wrapper的已审查Git blob纳入本次提交，原`sourceCommit`仍完整保留为未提交差异。还原本次新增wrapper一行后原文件校验值完全一致；该隔离操作及前副本见s4o证据。其他原dirty不混入提交。App数据事前完整副本保留，本轮字节未变。

两份旧预算账本、14.188544元unknown预占不变；累计5/5真实HTTP已用尽，保守累计14.679001元、上限30元不变。没有借余额新增调用，没有清理旧unknown、历史、计划grant、WAL或旧制品，没有日常库迁移/日常切换。

## 下一步与整项目标

目标仍是活动调用统一Kimi K3.1 Pro并安全迁移原K3，同时保留历史、unknown与计划授权语义。r5修复只是关闭链的必要前置，不能代替整个目标。

1. 首先零模型排查这次App的Native启动配置与装配，区分环境问题、产品准入和实际Runtime启动；以当前源码和日志取得可证伪原因，再准备标准本机fixture环境。不要机械重跑，不因UI未就绪再扩大Runtime补丁。
2. 在同一r5候选补Host/App正常工作、正常退出及保留历史的纵向证据；安全纯本机模型协议验证可以沿既有授权进行，旧真实G2V不得冒充新来源。
3. 继续S2自然旧K3已加载线程迁移/恢复取消、S3旧计划重新审阅授权、S4完整调用面/TCONF04与三项final。未通过项继续NOT RUN/pending，不刷成PASS。需要新的核心/补丁范围时先交最小方案。
4. r5真实G2V、日常切换和发布仍未获新许可；不新增真实HTTP，不以此阻塞独立离线工作。

回滚保留匹配的r4全套来源/制品和兼容reader，禁止旧r2 writer、数据库降级或清WAL。不得以本次代码和构建已提交宣称FEAT-164完成。

证据入口：`evidence/s4o-implementation-review.json`、`s4o-native-state-close.json`、`s4o-generation-result.json`、`s4o-app-build-receipt.json`、`s4o-app-observation.json`、`s4o-schema-and-upstream.json`。原始成功/失败日志保留于独立审计目录，精确绝对路径、SHA256和字节数见`s4o-raw-log-index.json`；未改写历史报告或原日志。

最终治理检查：claims、strict、manifest/Contract First规则检查、元仓53项测试及7份Shell语法通过。最终再次核验497份原dirty（混合文件仅排除本次明确插入）和7643份受保护文件，无意外差异；候选App/Runtime/worker/adapter、18086监听及候选数据打开句柄均为0。无待答授权或后台验收进程。
