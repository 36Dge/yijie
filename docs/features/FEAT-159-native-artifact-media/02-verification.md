# FEAT-159 验证

2026-10-18，local/demo_fast 本地候选验收 PASS。新普通聊天与已有口播专家通过真实 MCP 登记；最终构建完成 HTML/SVG 内置预览、用户 MP4 音画、原生保存、正常退出及同构建重启恢复。不是公开发布或生产加固结论，未继承旧 D4。

## 真实链路与最终界面

| 项目 | 结果与证据 |
| --- | --- |
| 新普通聊天 | `01a14daa-72e9-7462-9943-94749fc23129`，14:19:38提交，20秒完成。原生 MCP 三次 publish_artifact，HTML/SVG/MP4各一张ready卡片。 |
| 已有专家聊天 | 原跨境电商带货口播专家聊天 `01a14a82-f4dd-7690-aa2a-50a48913c698`，保留原专家及native thread `01a14a82-f558-7032-aaf9-5c31aae2cb4c`。14:33:10新轮次 `01a14db6-d76d-7cd3-a5fd-add53bb67e68`，14:33:36 task_complete，仅3次本地登记。 |
| HTML | 两类聊天重启前后均能打开独立内置预览窗，中文布局完整，按钮0→1；正常关闭返回聊天。 |
| SVG | 两类聊天重启后均可内置预览，100%→125%缩放正常；复用原图片预览与保存。 |
| MP4实际音画 | 首次FAIL，修复后实际瑜伽画面可见，用户明确确认“画面和声音都正常”。进度条点击跳到3秒；最终构建重启后两类聊天均再次显示原视频画面与播放器控件，音量1、未静音。 |
| 切换与退出 | 正在播放时切到已有专家聊天，原播放器卸载、新播放器保持暂停；相应pause/remove-src/load/release控件回归通过。最终构建在视频播放中Cmd+Q正常exit0，Host/adapter和18081监听均退出。 |
| 同构建恢复 | `pnpm tauri:demo-fast:app --reopen`校验receipt通过；新聊天和已有专家聊天的6份产物均恢复，以上预览在此后再次执行。未追加模型请求或重建产物。 |
| 原生保存 | 首次及重启后均使用真实macOS保存对话框保存三类文件；两批共6文件逐字节和SHA-256与输入一致。HTML正常取消保存反馈“已取消保存”，最终构建再次通过。 |
| 外观 | 1180×760最小窗口，亮色和WebKit临时暗色模拟下检查HTML卡片、SVG和视频控件；无关键操作重叠。已恢复System(Light)、原1268×780窗口并关闭Inspector。 |

最终构建沿用已验收的Host/Contracts/Runtime及真实登记产物，播放器与退出修复在最终Desktop上复验；没有把历史模型请求冒充为最终构建后新发送的请求。

## 保存与视频原件

保存目录：`/Users/jack/Desktop/yijie 原生产物链/FEAT159-验收保存-20261018/first` 和 `after-restart`。

| 文件 | 字节数 | SHA-256（两批保存相同） |
| --- | ---: | --- |
| preview.html | 1162 | `265156b54033f5be1f754d10d92258571821af70bfb3a4da94be1195e59cea80` |
| preview.svg | 539 | `41598cc3dec61395d270446678f9e495d85546090addb5c7c2459f1f0ebba6a6` |
| testmp4.mp4 | 3911170 | `598cf3a45b17cf2943d06ffa5c512131d7c34709d83c0b7b89fac0cc543b6c6b` |

用户视频 `/Users/jack/Desktop/testmp4.mp4` 原件只读，未转码或修改、未纳入Git。ffprobe为7.776009秒，H.264/avc1 1280×690和AAC/mp4a 44.1kHz双声道。音轨元数据不替代用户有声确认。

## 发现并修复的真实故障

1. 初次视频实际灰屏且无声，用户已明确确认，不能归因于截图限制。旧冒烟只检查metadata/playing/seek且主动静音，不证明音画。
2. 现有视频协议在音轨、视频轨和元数据并发Range超过两路时撤销整个预览句柄，后续404。修复复用Tokio信号量，在原两路读取与64MiB上限前有界等待（最多16请求、10秒），不换播放器、不修改Runtime。修复后记录612次Range全部206，拒绝、限额、404均0；用户确认音画正常。临时输出已移除，只保留原有feature-gated诊断。
3. 15:08一次正常Cmd+Q出现SIGSEGV。只读系统报告显示主线程 `NSApplication terminate:` → `sqlcipher_atexit`，数据库线程同时读取 `pending_artifact_acknowledgements`。默认macOS Quit绕过原有ExitOwner；主窗口关闭路径能正常exit0。修复仅将默认菜单Quit/Cmd+Q接入已有ExitOwner，复用Coordinator/sidecar/database正常清理。最终播放中Cmd+Q exit0及同构建恢复通过。
4. 更新控件文案断言时触发构建源指纹变化，canonical构建拒绝生成reopen receipt；未绕过检查，冻结源后重新完整构建成功。
5. 之前CUA出现noWindowsAvailable/timeout，用户手动关闭HTML预览并将主窗口置前后恢复；只读sample未证明App死锁，未使用强杀或其他UI控制技术。

## 工程检查

| 检查 | 结果与范围 |
| --- | --- |
| Contracts | 28个JSON Schema校验、新媒体普通conformance 1项、Host/Desktop双consumer生成物及摘要检查通过；旧公共v3源不变。 |
| Host | `YIJIE_TEST_MEDIA_FILE=/Users/jack/Desktop/testmp4.mp4 go test -race ./internal/session -run '^TestArtifactMediaNormal' -count=1`，2项通过。Store/加密spool/EventHub、重复登记、ACK、用户MP4、旧流隔离、混合排序和终态清理。 |
| Native | `YIJIE_TEST_MEDIA_FILE=/Users/jack/Desktop/testmp4.mp4 cargo test --manifest-path src-tauri/Cargo.toml --lib media_normal_`，2项通过。SQLCipher提交、原子保存、正常重开后字节一致；补充MP4跨页及尾部Range逐字节比较通过。 |
| 前端 | 普通控件定向6项、原生视图5项通过；最终视频4项定向回归通过，含单句柄、切换卸载清理和保存。仅文案断言曾失败，按新文案修正后通过。排除.local及历史源副本。 |
| 静态/构建 | vue-tsc、ESLint、Go vet、Rust fmt/check、clippy --lib -- -D warnings、adapter cargo check/clippy、pnpm build、设计文档build、canonical打包通过；仅有既有大chunk提示。 |

首次UI命令误匹配.local历史副本造成14失败，未计作当前源结果；改用规定排除范围后通过。首次SQLCipher测试使用1970时间戳导致重开清理过期记录，已按当前时间修正测试，未改变产品过期规则。

## 未改内核与额度

- yijie-codex Git工作区干净，无Runtime源码、patch或二进制改动。
- Runtime SHA-256：`aad49041bd7d34c853fb55c274711e3cc810725720d2c097469822d310fb02f9`。
- manifest SHA-256：`8b86a1a661f50beda1e0a0c96f81ddbdf959a9a07c2e756cc4b9b0eabc053b27`。
- 用户批准最多4次短文本请求。保守按提交已用3次：新普通聊天成功、旧UI设计师被既有状态阻挡、旧口播专家成功；实际新模型轮次2次。付费图片/视频和外部商家调用0。
- 未提交、推送或发布；只有本地candidate，HTML限自包含资源，MP4编解码支持由系统WebKit提供。

## 已发现但未修改的历史问题

原UI设计师聊天 `01a14a7b-ee79-79d1-9950-a75762a3fbe8` 的Host从2026-10-17T15:29:58Z仍为active，原生rollout在同日15:47:30Z为turn_aborted。本次提交被旧准入检查阻挡，没有新原生turn或Host提交receipt，界面查询原操作。在正常退出后用官方bbolt库ReadOnly核查；未改用户数据库、清除原操作或重复提交。该异常聊天不算通过；本次旧聊天验收使用终态已确认的口播专家聊天。该历史恢复缺陷未被本次产物功能修复。

## 证据与未执行项

Desktop `.local/feat159-evidence/`：`html-after-restart.png`、`svg-after-restart.png`、`video-after-restart.png`、三张`expert-*-after-restart.png`、`minimum-window-*.png`、`saved-first.json`、`saved-after-restart.json`、`video-queue-diagnostics.json`。正常构建/重开日志：`.local/feat159-final-stable-run.log`、`.local/feat159-final-reopen.log`。

跳过历史攻击/故障注入fixture、强杀、权限破坏和恶意资源测试，原因是用户永久安全规则；不声称这些专项覆盖通过。使用正常样本、源码审查、实际保存取消、真实播放与正常退出恢复验证。

最终功能包检查：`node docs/dev/codex-feature-delivery/scripts/validate-feature-package.mjs docs/features/FEAT-159-native-artifact-media --gate D4` exit0。该检查验证记录语义；真实结果由上面的模型、界面、保存摘要和正常退出证据支持。

后续状态：用户已授权复审后提交推送。对应记录见[提交前复审与来源](../FEAT-159-native-artifact-media/03-final-review-and-push.md)；本文保留原验收时间与历史故障事实。
