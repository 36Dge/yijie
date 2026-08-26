# Codex Desktop 人工参考采集清单

> Target: `codex-desktop-26.818.61809-build-7019-2026-08-26`
> Intended provenance: `reference-observation`
> Current status: `reference-unobserved`

此清单只用于补齐当前安全自动化无法读取的版本专属 UI 证据。采集者必须先核对 version/build；若已漂移，停止并登记 drift，不用新版本覆盖旧基线。完成本清单之前，所有版本专属 Codex Desktop 交互仍保持 `reference-unobserved`。

## 1. 采集前一次性提供的全局资料

采集前先确认 Codex Desktop 仍为 version `26.818.61809`、build `7019`，并提供以下脱敏资料：

- “关于 Codex”中的 version/build 截图；
- App 内主题设置截图；仅有 macOS 系统主题不能证明 App 内主题；
- 一张没有 active Turn 的空闲对话窗口截图，用于记录整体布局；
- `capture-manifest.md`，记录采集时间及时区、macOS 版本、App 语言/地区、App 内主题、窗口宽高像素、显示缩放、App 缩放比例、reduced motion 状态；
- 与交互有关的非敏感配置，例如所选模型、reasoning 档位和权限模式；不得包含账号、组织、订阅或 Provider 凭证；
- 所有裁剪、模糊、静音和录屏剪辑的说明。

如果 version/build 与目标不一致，停止本 baseline 的采集，登记实际 version/build、发现时间和影响，不在旧 Freeze ID 下继续。

## 2. 每个场景都要提供

- 一份场景记录，包含场景 ID、variant、前置条件、用户操作、按时间顺序的可见状态、每个状态可用动作、最终结果和偏差；
- 对实际执行的 scenario/variant，至少提供一张脱敏的最终状态截图；存在状态变化、流式内容、按钮状态变化、滚动或恢复过程时，还需提供从操作前开始、持续到权威终态的短录屏；`NOT RUN` 只交场景记录，不交占位截图；
- 多 variant 场景可分别录制，也可使用一段连续录屏，但必须在记录中标明每个 variant 的开始/结束时间码；
- 每个最终交付文件的文件名和 SHA-256；必须先完成裁剪与脱敏，再计算并登记 SHA-256；
- 无法安全执行的项目写 `NOT RUN`、原因、影响和 Owner；UI 未提供或真实 Provider 未自然产生的能力写明 `not_exposed` 或 `not_naturally_produced`，不能补造；
- synthetic replay 只能登记为 Yijie test-only 证据，不能作为 Codex Desktop 的 `reference-observation`。

录屏或截图只需证明可观察行为，不要求也不得尝试取得隐藏 reasoning、系统 prompt、私有协议或应用内部数据。

### 建议先交的最小首批材料

先只提交“全局环境 + GS-001”，确认版本、脱敏和索引格式后，再批量采集其余场景：

```text
codex-desktop-26.818.61809-build-7019-2026-08-26/
├── capture-manifest.md
├── SHA256SUMS.txt
├── 00-about__redacted.png
├── 00-theme__redacted.png
├── 00-idle-window__redacted.png
└── GS-001/
    ├── GS-001__streaming__record.md
    ├── GS-001__streaming__...__redacted.mov
    ├── GS-001__streaming__...__redacted.png
    ├── GS-001__completed__record.md
    └── GS-001__completed__...__redacted.png
```

`streaming` 与 `completed` 可以由一段连续录屏覆盖，但两项必须分别有记录，或在同一记录中给出明确的开始/结束时间码。所有媒体先脱敏，再计算 SHA-256。

## 3. 十三个场景的最小关键画面

| Scenario | Canonical variant | Owner | 最小截图/录屏要求 |
|---|---|---|---|
| `GS-001` 普通流式完成 | `streaming`、`completed` | FEAT-134 / FEAT-135 | 录屏覆盖发送前 Composer、提交、等待/流式输出、执行中 Stop 和最终完成；截图至少包含流式中与完成后。 |
| `GS-002` 过程更新/推理信息 | `multi-progress`、`reasoning-summary` | FEAT-134 | 录屏覆盖多个可见过程或 reasoning 更新、展开/折叠和最终回答层级；截图包含折叠与展开状态。若 Provider 未产生可见 reasoning，记录 `NOT RUN/not_naturally_produced`。 |
| `GS-003` Command | `success`、`failure` | FEAT-136 | 每个 variant 录到 Command 卡片开始、输出更新、展开/折叠、成功或失败终态以及 Turn 是否继续；每个 variant 一张终态截图。失败只能来自正常、无破坏性的只读检查。 |
| `GS-004` Tool | `success`、`failure` | FEAT-136 | 每个 variant 录到 Tool 名称/安全摘要、执行中状态、结果或错误、展开/折叠和 Turn 后续状态；每个 variant 一张终态截图。没有批准且真实注册的 Tool 时记录 `NOT RUN`。 |
| `GS-005` 审批 | `allow`、`deny`、`expired` | FEAT-137 | 每个 variant 录到审批请求、当时可用按钮、决定后的 disabled/resolved 状态及最终结果；每个 variant 一张截图。`expired` 必须自然发生。 |
| `GS-006` 文件修改与 Diff | `file-change`、`diff` | FEAT-138 | 只在隔离、非敏感临时工作区采集；录到安全测试文件变更、文件列表、逐文件 Diff 展开、可能的审批和最终状态；截图包含展开的 Diff 与最终状态。 |
| `GS-007` active Turn steer | `steer` | FEAT-139 | 录到 Turn 正在执行、输入补充要求、补充内容被接受、同一 Turn 继续及最终状态；截图证明补充后仍延续原 Turn。 |
| `GS-008` Stop | `stop`、`interrupted` | FEAT-139 | 录到 active Turn、Stop 可用、点击一次、按钮进入 disabled/stopping 和权威 interrupted 终态；截图包含停止后的部分内容及状态。只能使用 UI Stop。 |
| `GS-009` Retry/Continue | `retry`、`continue` | FEAT-139 | 录到原 failed/completed/interrupted Turn、Retry 或 Continue 入口、新尝试启动、旧 Turn 保留和新尝试终态；截图应能辨识新旧尝试。可复用 `GS-008` 的正常中断。 |
| `GS-010` 历史切换/恢复 | `switch`、`restore` | FEAT-140 | 使用两个脱敏临时会话 A/B；录到 A→B→A、历史加载和内容不串线；再通过应用正常退出/重开记录恢复结果；截图包含重开后的恢复状态。 |
| `GS-011` 滚动 | `new-message`、`return-to-bottom` | FEAT-141 | 录到位于底部时自动跟随、主动上滚、新内容到达但不抢位置、新内容提示、回到底部，以及加载更早历史时的锚点；截图包含上滚后的新内容提示。 |
| `GS-012` 断线/恢复 | `resync-required`、`recovered` | FEAT-142 | 只在自然连接异常，或应用正常退出/重开时采集异常前、reconnecting/resync 提示及恢复或不可恢复终态。没有自然异常时记录 `NOT RUN`；正常重启只能证明 session restore，不能写成 mid-stream reconnect。 |
| `GS-013` 未知/缺失事件 | `unknown-item`、`missing-delta`、`missing-final` | FEAT-142 | 仅记录自然出现的未知 Item、缺失 delta 或无 final，包括安全占位/恢复提示和其它内容是否仍可用。没有自然现象时记录 `NOT RUN`；不得用 synthetic replay 冒充参考客户端观察。 |

## 4. 单场景记录模板

每个场景建议提供一个 Markdown 文件并包含以下 YAML；未执行的字段也保留，以便区分未观察和不存在：

```yaml
scenario_id: GS-003
variant: failure
freeze_id: codex-desktop-26.818.61809-build-7019-2026-08-26
execution_status: PASS | PARTIAL | NOT RUN | BLOCKED
observation_status: reference-observation | reference-unobserved
provenance: reference-observation | null
observed_outcome: available | not_exposed | not_naturally_produced
captured_at: 2026-08-26T10:30:00+08:00
app_version: 26.818.61809
app_build: 7019
macos_version:
locale:
theme:
window_px:
display_scale:
app_zoom:
reduced_motion:
preconditions:
steps:
visible_timeline:
  - timecode:
    state:
    available_actions:
final_result:
deviations:
redactions:
not_run_reason:
impact:
owner:
artifacts:
  - filename:
    type: screenshot | recording
    sha256:
```

只有实际执行、可复核且与冻结 version/build 匹配的媒体才能同时写 `observation_status: reference-observation` 与 `provenance: reference-observation`。`NOT RUN`/`BLOCKED` 必须写 `observation_status: reference-unobserved`、`provenance: null`，不得填写虚构 artifact。

## 5. 文件命名、哈希与交付目录

使用 ASCII 文件名，避免把 prompt、会话名、账号或项目名写入文件名：

```text
GS-003__failure__codex-26.818.61809-b7019__20260826T023000Z__redacted.mov
GS-003__failure-final__codex-26.818.61809-b7019__20260826T023000Z__redacted.png
GS-003__failure__record.md
```

建议按 Freeze ID 建立内部证据目录，每个 `GS-*` 使用独立子目录，并在根目录提供 `capture-manifest.md` 与 `SHA256SUMS.txt`。所有截图和录屏必须先完成裁剪、脱敏和必要静音，再对最终交付文件执行：

```bash
shasum -a 256 <redacted-file>
```

把最终哈希同时登记到 `SHA256SUMS.txt` 和对应场景记录。不得在计算哈希后继续修改文件，也不得用原始未脱敏文件的哈希代替交付文件哈希。证据只能作为 `internal` 参考资料，不得进入 Yijie 生产 bundle。

## 6. 脱敏规则

交付的截图、录屏、文件名和记录中不得出现：

- 真实 prompt、项目名、仓库名、线程标题、文件正文或敏感命令输出；
- 绝对路径、账号、姓名、头像、邮箱、手机号、组织和订阅标识；
- 通知、其它会话侧栏、菜单栏隐私内容、secret、token、私钥、URL、IP 或内部服务地址；
- 商家、店铺、订单、买家、卖家或其它业务数据。

优先使用无敏感内容的临时会话和临时工作区；采集前关闭通知，只录 App 窗口并关闭不需要的音频。脱敏不得遮住状态文字、按钮是否可用、事件顺序或关键时间码；有裁剪、模糊、静音或剪辑时必须在场景记录中说明。只交付脱敏后的文件，原始媒体不得提交到仓库或证据包。

## 7. 安全禁止项

所有采集都必须使用正常、非破坏性的产品流程：

- 禁止使用 `kill`、`kill -9`、`pkill`、强制退出或频繁终止进程制造异常；
- 禁止替换、篡改或伪装 binary/Runtime，禁止修改权限、属主、数据库、缓存或历史数据制造失败；
- 禁止资源耗尽、攻击载荷、恶意 fixture、凭证攻击、协议拦截、事件删除/篡改或其它故障注入；
- `GS-003`/`GS-004` 的 failure 不得使用破坏性命令、无界执行、真实凭证错误或外部副作用制造；无法正常安全失败时记录 `NOT RUN`；
- `GS-005 expired` 不得修改系统时间、强杀进程或破坏连接制造过期；
- `GS-006` 不得编辑真实用户数据、生产文件或 `yijie-codex` Runtime，只允许隔离临时测试文件；
- `GS-008` 只能点击应用自身的 Stop；`GS-009` 复用自然失败或正常 Stop，不能制造 crash；
- `GS-010` 只能通过正常切换、退出和重开验证，不得删除或篡改会话数据库、缓存和用户历史；
- `GS-012` 不得通过强杀、断电、修改防火墙/代理、破坏网络、权限或数据制造断线；只记录自然异常或正常生命周期；
- `GS-013` 不得用 DevTools、网络拦截、协议篡改、畸形消息或攻击 fixture 向参考 App 制造未知/缺失事件。

无法安全执行的证据项必须写 `NOT RUN`、原因、影响和 Owner；不得生成占位证据或伪造 PASS。

## 8. 当前自动化结论

- 未生成任何 Codex Desktop 截图或录屏；所有版本专属 UI 证据仍为 `reference-unobserved`。
- 未使用系统截图、私有偏好读取、其他 UI 自动化或录屏 API 绕过 Computer Use 安全限制。
- 因此未附带空白占位图，也未把 synthetic replay 冒充为参考客户端观察。
