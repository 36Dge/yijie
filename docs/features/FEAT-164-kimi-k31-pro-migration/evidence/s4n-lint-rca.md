# S4N 三次 Clippy 失败后的停止与完整复核

Owner本轮已明确批准40号四文件、独立r5及零真实HTTP验证。三次相同scoped Clippy命令均101，已停止第四次机械重跑，未构建r5、未固定Runtime提交、未生成Contracts或更新下游。没有新模型请求/强杀/权限故障/删除WAL。时间、原日志hash见s4n-lint-failure-timeline.json；原日志保留在独立审计目录，不能覆盖。

1. run1：state日志关闭等待跨await持有tokio::MutexGuard，违反clippy.toml明示禁令。原设计虽然意图保留被取消等待者的JoinHandle，仍不符合项目并发约束。改为独立join owner持有worker，完成后watch共享typed result；等待者取消不消费结果，不需要持锁await。
2. run2：上述实现已替换，但wait_for使用冗余Option闭包，违反workspace冗余闭包deny。已经改为Option::is_some。此前只逐条修诊断，未一次核对完整crate/workspace规则，是连续失败的过程根因。
3. run3：codex-state已完成Clippy，app-server新eprintln触发crate第2行print_stderr deny。这里不是数据库、模型或运行环境失败；也不是需要放宽lint。新增错误输出应复用既有tracing stderr层，日志receiver已经关闭，不会重写SQLite或递归入队。

## 扩大审计与可证伪结论

实际读取固定Cargo.toml全部workspace.lints.clippy、clippy.toml的invalid await types/disallowed methods、四个修改文件的crate allow/deny、完整新增Rust差异、日志sender/receiver/Join/watch持有与正常关闭阶段。无新的依赖/公共DTO/权限/数据库变更；新版没有跨await锁，无生产unwrap/expect，普通日志仍保持原无偏select和容量策略；错误固定文案，不带SQL/路径/正文。stdin专用RPC wrapper先真正排空，原in-process及非stdio有界入口保持。

事实：最早卡在源静态资格，尚未到新binary/checkpoint实测。原4项及后6项unit成功分别对应修正前/后Mutex版，**不能称watch版当前测试已通过**。第三次只证明state正常库编译/lint推进到app-server，不证明完整Runtime或新关闭行为通过。原r4 EOF缺口不因Lint失败被推翻。

候选原因排序：新增源代码未遵守完整lint政策（已由三个明确诊断证实）；工具链/依赖漂移不支持（固定1.95、132本地lock正规化已核对）；存储/权限/模型错误没有证据。不能通过变更deny或allow条目、跳过app-server、修改canonical源、清WAL或改测试判定来规避。

唯一下一修正：把新增eprintln改为现有tracing error固定诊断，保留返回错误；日志shutdown已经关闭receiver，此事件不可能进入该SQLite队列。重新生成仅四文件的0011 patch，对当前十patch做fresh canonical replay。然后**仅一次**新来源完整定向资格：6项安全unit、既有纯RPC gate检查、相同两package Clippy -D warnings。全部通过才固定source；若任一步仍失败立即停，不再自动进入下一改动/重试。失败保留候选源/日志/原制品，不启用、不构建、不更新下游。

此修正及静态验证完全在用户刚批准的四文件与安全验证范围内，无新写入面、外部副作用或额外真实Runtime/模型请求，因此不制造新的确认流程。后续独立r5 build/正常EOF仍受40号已批准范围、零真实模型、保护WAL与失败即停约束；不是无限重试许可。build中的历史smoke使用TemporaryDirectory会自动清理文件，本轮新r5必须使用留存完整home的正常EOF检查入口，不能删除残留WAL。该测试入口尚未执行。
