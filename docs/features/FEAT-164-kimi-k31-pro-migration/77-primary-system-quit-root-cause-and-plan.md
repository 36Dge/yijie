# FEAT-164 第77号：主目录启动后的系统退出路径审计

2026-10-28。原主目录generation20261028-01已canonical构建并实际启动，App/Host/worker均来自原主目录新输出，Runtime仍为原仓r5。Mac锁屏使UI历史检查按Owner要求跳过。随后发送正常macOS Quit AppleEvent，进程退出0；**后态不通过**，不得把系统请求退出0当作应用完成清理。

## 实证与根因

前后完整冷备份及副本检查：Native71张表的历史、Host所有持久值、Runtime业务行与rollout均保持；Native只有既有connector启动metadata表产生正常增量。`chat_scheduled_stopped_generations`120→120，未产生此代停止证明；Native活动WAL41,232字节、SHM32,768字节。没有删除/截断/手工checkpoint，原件和完整后态副本保留。

`chat/exit_owner.rs`已明确解释macOS predefined Quit直接调用`NSApplication terminate:`，所以此前只把菜单项换成自定义`yijie-normal-quit`。`lib.rs`的menu/Window Close/ExitRequested进入ExitOwner，但普通Quit AppleEvent仍走系统终止。固定tao0.35.3只注册`applicationWillTerminate:`并在其中调用AppState::exit，没有可异步等待的applicationShouldTerminate处理。故本次正常OS退出请求未走Native coordinator→workflow→sidecar→停止代记录→数据库checkpoint链。将AppleEvent等同Command-Q是本轮观测方式的错误假设，同时暴露现有系统退出路径的缺口。

## 最小修复及再次审计

在Owner本轮“遇到执行阻塞深入分析并修复、直到原主目录构建运行完成”的范围内，限定修复Desktop自身正常退出。**不改Runtime核心/补丁、数据库schema、模型wire、权限或执行授权；不改变macOS锁屏设置、不操作锁屏UI。**

1. Desktop `src-tauri/src/chat/exit_owner.rs`使用已锁定objc2/Foundation的标准NSAppleEventManager，仅注册本App的`kCoreEventClass/kAEQuitApplication`（已核对SDK AppleEvents.h：`aevt/quit`）事件。handler只调用现有ExitOwner.request；不调用系统terminate、不改App delegate、不做method swizzling、不接收任意命令。保留现有原生权限失效、重复请求幂等、正常等待、STOP_PENDING和checkpoint链。
2. `src-tauri/src/lib.rs`在主线程setup注册handler；现有ExitOwner完成清理后于主线程卸载。对象由主线程明确保有，不能在回调期间释放；不把AppHandle或selector泄漏到WebView。
3. `src-tauri/Cargo.toml`只开启既有固定Foundation库的NSAppleEventManager/Descriptor SDK feature，不升级版本或引入外部服务。不追加CoreServices依赖；注册/卸载使用既有objc2的标准消息API及SDK确认的u32事件常量。若产生非预期依赖/lock差异先停审计。
4. 同步退出规范与SECURITY；普通安全编译、fmt、Clippy及适用的无破坏性测试后本地提交。新generation独立构建；失败01及其制品/记录保留，不覆盖其回执、不复用其D4结论。
5. 以当前含WAL的完整数据组作新冷备份/副本预检，原件不做维护。新App正常打开后，由产品自身正常SQLite恢复和退出checkpoint完成收尾；通过真实Quit AppleEvent验证停止代+1、所有旧业务行不变、活动WAL/SHM0、无进程/句柄和实例锁释放。0模型HTTP；锁屏UI仍SKIPPED，不改为PASS。

复审结论：这是Desktop私有生命周期semantic修复，借用既有唯一ExitOwner，避免再增加关闭协调器或外部IPC。原先的“Native不改”是第75号预期，不是已确认的事实；新发现以本报告明确扩展这三个Native/配置文件范围。Runtime修改须单独方案确认的边界保持，当前不需要。没有新模型、平台写操作或数据迁移。

停止条件：无法使用既有Foundation版本完成、需要替换框架/Runtime、handler无法保有正确生命周期、正常退出等待未结束、旧数据或授权变化，均停止对应阶段并审计。三次同点失败继续适用项目熔断。不得通过放宽停止代/WAL断言把01伪造通过。

## 执行结果

修复已本地提交`24a231f96f08ed077e53f9bd73a2aac93ee6cba8`。固定Foundation只新增两个SDK feature，Cargo.lock零差异；Clippy -D warnings、fmt、正常停止幂等/等待两项安全测试、文档构建及19项同源检查通过。generation02独立canonical构建后，三轮真实标准Quit均记录`normal system quit requested`和`normal app cleanup complete`，停止代各新增1，活动WAL/SHM均为0，旧业务行/授权/Host值/Runtime业务及rollout保持，无进程和句柄残留。第一轮遗留WAL仅由新App正常读取/退出收尾，完整旧副本保留。

初始01退出仍为FAIL；后续修复通过不改写原结果。三轮新来源及整体回退边界见[76](76-primary-workspace-execution.md)和[机器证据](evidence/primary-workspace-execution-result.json)。UI历史因Mac锁屏跳过，未宣称界面验收通过；真实模型HTTP0，Runtime核心/补丁不改。
