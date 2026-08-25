# FEAT-128 Demo 验证

## 1. Focused checks

| Repository/CWD | Command | Exit | Result | 时间 |
|---|---|---:|---|---|
| yijie | `check-feature-package.sh --gate D0 .../demo-fast` | 0 | PASS，账本更新后 schema v3 与 D0 语义复验 | 2026-08-24 00:17 +08:00 |
| yijie | `check-feature-package.sh --gate D4 .../demo-fast` | 0 | PASS，schema v3、8/8 Must AC、真实本地 smoke 与完成态语义门禁通过 | 2026-08-24 10:00 +08:00 |
| yijie | `node --test tests/codex-feature-delivery.test.mjs` | 0 | PASS，47/47 | 2026-08-24 00:17 +08:00 |
| yijie | `node docs/dev/codex-feature-delivery/scripts/audit-feature-packages.mjs` | 0 | PASS，6 个 committed 历史包可读 | 2026-08-23 22:21 +08:00 |
| yijie-agent-host | `go test ./internal/imagegen ./internal/codex ./internal/session ./internal/app` | 0 | PASS | 2026-08-23 22:18 +08:00 |
| yijie-agent-host | `make test` / `make lint` | 0 / 0 | PASS，含 contract 与 race | 2026-08-23 22:19 +08:00 |
| yijie-desktop | `cargo test ... minimax_key_file -- --nocapture` | 0 | PASS，2/2 | 2026-08-23 22:19 +08:00 |
| yijie-desktop | `vitest run ChatArtifactShell.test.ts` | 0 | PASS，6/6 | 2026-08-23 22:19 +08:00 |
| yijie-agent-host | `go test ./...` | 0 | PASS，含 imagegen 稳定 Artifact 名称回归 | 2026-08-24 09:59 +08:00 |
| yijie-desktop | `cargo test --manifest-path src-tauri/Cargo.toml` | 0 | PASS，241 passed / 3 ignored；含 orphaned Host terminal fail-closed 与 v3 coordinator 回归 | 2026-08-24 10:00 +08:00 |
| yijie-desktop | `pnpm lint` / `vue-tsc --noEmit` / `pnpm build` | 0 / 0 / 0 | PASS；build 只有既有 chunk-size warning | 2026-08-24 09:59 +08:00 |
| yijie-desktop | `pnpm test`（默认 demo_fast） | 0 | PASS，63 files / 438 tests；历史 S10D-H checker 不进入默认 Demo 测试面 | 2026-08-24 13:52 +08:00 |
| yijie-desktop | `pnpm test:production-hardened` | 1 | EXPECTED BLOCK，63/64 files、479/480 tests；唯一失败是历史 S10D-H `application.rs` digest，未刷新 digest、未改变 FAIL/PAUSED | 2026-08-24 13:52 +08:00 |
| yijie-desktop | `vitest run check-feat128-s9b-d-dependencies.test.mjs` + actual checker | 0 | PASS，7/7；语义冻结 ECharts 6.1.0、zrender/tslib graph、integrity/license/NOTICE/static imports，允许无关 package scripts、lock、NOTICE 演进 | 2026-08-24 13:51 +08:00 |
| yijie-desktop | `vitest run permission-lifecycle + chat-permission-lifecycle + ChatPage + chat.store` | 0 | PASS，61/61；覆盖 foreground 路由保持、有序 Artifact 刷新、terminal 权威重同步与 live buffer 清理 | 2026-08-24 09:57 +08:00 |
| yijie-desktop | `vitest run local-profile + SettingsPage + permission.store + router/App` | 0 | PASS，37/37；exact local gate、零登录 UI、提前权限续期、恢复态强制 `/chat` | 2026-08-24 00:12 +08:00 |
| yijie-desktop | `cargo test ... demo_fast` / `cargo check` | 0 / 0 | PASS，native local authority、scope/public-task binding 与 default compile | 2026-08-23 23:24 +08:00 |

## 2. 真实服务启动与 Smoke

| Check | Command/steps | Environment | Actual result | Result |
|---|---|---|---|---|
| Historical Host startup | 旧入口下启动 Tauri Desktop、Host 与 bundled Runtime | macOS local，真实 Key 文件 | 仅保留 Host/Runtime 历史事实；依赖人工白名单登录的 Desktop 入口已被 ADR-0018 supersede，且 Keycloak/API/DB/Caddy 不再是 demo_fast 启动依赖 | SUPERSEDED |
| Historical ordinary text | 旧 Host vertical 发送明确“不要生图”的普通文本并读取 v3 replay | local MiniMax-M3 | 返回“普通文本正常。”；sequence 1–7 无 `item.artifact.*` | PASS（历史 Host vertical） |
| Real T2I | 明确要求橙色虎斑猫 1:1 写实图片 | local MiniMax-M3 + image-01 | Artifact `59dbb603-...` ready；JPEG 1024×1024 / 271470 bytes / SHA-256 `5f5901c9...a4f5` | PASS（Host vertical） |
| Real person reference | 生成一张无隐私虚构人物参考图 | local MiniMax-M3 + image-01 | Artifact `4983adb3-...` ready；JPEG 1024×1024 / 277614 bytes / SHA-256 `7f3b7826...1ad9` | PASS |
| Real I2I | 当前轮唯一人物 JPEG + 明确 subject reference 请求 | local MiniMax-M3 + image-01 | Artifact `d6126074-...` ready；JPEG 864×1152 / 220378 bytes / SHA-256 `377f0c09...8e4b`，与参考图不同且主体特征保留 | PASS（Host vertical） |
| Flag-off regression | fresh final Host，不设置 `YIJIE_FEAT128_IMAGE_GENERATION_ENABLED` | local bundled Runtime | `/v1/status` 返回 `experimental_api=false`，未注册 dynamic tool | PASS |
| Representative failure/retry | fake provider/缺失业务状态字段/无效配置 | local isolated | fail closed、无伪 ready、无 raw provider error；缺失 `base_resp.status_code` 回归测试已补 | PASS |
| Desktop preview/save（历史入口） | 在真实 Chat 消息中预览并 native save | local Tauri + 白名单 | 曾因人工登录阻断，现已被 ADR-0018 supersede；不得继续要求输入账号密码 | SUPERSEDED |
| Local direct-entry + ordinary text | fresh isolated Demo DB/secret；以 canonical 等价完整环境运行最新 debug app，检查首屏、Settings、Host listener，发送“只回复 DEMO_FAST_OK，用于本地免登录启动验收。” | exact local+demo_fast；真实 ChatPage；dev-built Host + bundled Runtime；Keycloak/OIDC/API 非依赖 | 2026-08-23 23:31 +08:00 首屏 `tauri://localhost/chat`；无登录/账号/密码/浏览器；Settings 仅本地快速验证模式与 Sidecar；Host 监听 `127.0.0.1:18081`；session `01a02f4b-7028-74b3-9a0f-a53942512d2a` 完成并返回 `DEMO_FAST_OK`；图片 Artifact 0，`image-01` 调用 0 | PASS（debug app equivalent environment） |
| Canonical launcher + fresh GUI | `pnpm tauri:dev`（当时以同一 launcher 的 `pnpm tauri:demo-fast` 名称执行）验证 dev Host build + Tauri dev app + bundled Runtime；同 profile 构建/签名 latest debug app 做可寻址 UI 复核 | exact local+demo_fast，含污染 parent env 负载 | Host `ready`、MiniMax-M3、`experimental_api=true`；fresh 和 Settings→quit→restart 均直达 `/chat`；Settings 无登录/退出/账号/密码；正常退出释放 18081，Desktop SIGKILL 后 Host 约 0.1 秒自退；`tauri:dev` 与 `tauri:demo-fast` 现为同一脚本 | PASS |
| Desktop real T2I + preview | 在真实 Chat 输入蓝色几何山脉海报请求；等待同一消息 Artifact 完成并打开预览；随后重启 Host/Desktop 复核持久化 | exact local+demo_fast；真实 MiniMax-M3 + image-01；付费调用 #4 | session `01a02f89-2c6e-7591-bf2b-22392bc3fcad`；Artifact `b574c1d4-d4d3-40b7-9944-eaa26e02c3e1`；JPEG 1024×1024 / 95393 bytes / SHA-256 `8685a600d566e0f2c7208e013ab05025ac570e9e7b416180bc9877d3a157e46d`；Host v3 sequence 1–16，`turn.completed`；Desktop ready、lightbox 真实可见，重启后仍 completed/ready | PASS |
| Desktop native save | 在上述真实 T2I ready 卡片点击“保存图片”，核对输出文件 | exact local+demo_fast；不调用 Provider | `<workspace>/generated-image.jpg` 为 JPEG 1024×1024 / 95393 bytes / mode 0600 / SHA-256 `8685a600d...7e46d`；与真实 T2I Artifact 精确一致且不是 synthetic fixture，可正常解码 | PASS |
| Desktop analyze-only | 上传 `reference-portrait.jpg`，仅要求分析人物外观、服装和构图，明确禁止生图 | exact local+demo_fast；付费账本调用前后均为 4/5 | session `01a0316d-2347-7ed0-85a3-a10dce02a7bd` 返回中文文字分析；Runtime rollout 无 `response_item function_call`，无新图片 Artifact。首次 queued 的 `ProjectUnavailable` 由重新选择 CrossBSD 刷新 macOS bookmark 后自动恢复，未重复提交 | PASS |
| Desktop real person-reference I2I | 上传同一人物 JPEG，明确要求保持人物身份并改为雨夜上海街头、3:4，只生成一张且不得回显附件 | exact local+demo_fast；真实 MiniMax-M3 + image-01；付费调用 #5（最终额度） | session `01a03176-9a68-7141-8dea-417152f4ba14`；Runtime 仅 1 次 `generate_image` function_call，`mode=subject_reference`、`aspect_ratio=3:4`；输出 JPEG 864×1152 / 247098 bytes / mode 0600 / SHA-256 `e37f769a...57a61`，与参考图 `7f3b7826...1ad9` 不同且主体特征保持；消息、lightbox、保存与重启持久化均 PASS | PASS |
| Terminal UI + restart | 最终 I2I terminal 后重建 latest debug app，精确检查进程、侧栏、历史、Artifact 与 route | exact local+demo_fast；只读取已持久化结果，不调用 Provider | terminal 后权威 resync 清除重复 live answer；重启后侧栏/页头/页尾均为“已完成”，只有一份模型回答，Artifact ready、预览正常；1 Desktop + 1 managed Host，`/readyz` ready | PASS |
| Foreground route retention | 在上述精确图片会话切到 Finder，再切回易界 AI | exact local+demo_fast；真实 Desktop | URL 仍为 `tauri://localhost/chat/01a02f89-2c6e-7591-bf2b-22392bc3fcad`；completed=true、imageReady=true、onSettings=false | PASS |
| Final process hygiene | 精确检查 Desktop/Host parent-child、18081 listener 与 `/readyz` | 当前 local Desktop | 当前仅 PID 10738 Desktop 管理 PID 10754 Host；Host 监听 127.0.0.1:18081，`runtime_state=ready/status=ready`，无第二客户端 | PASS |

## 3. Must AC

| AC | Result | 真实证据/Artifact |
|---|---|---|
| AC-IMG-001 | PASS | 真实 Desktop 同一消息完成 MiniMax-M3 tool decision → image-01 → v3 Artifact → ready 图片与预览，且重启持久化 |
| AC-IMG-002 | PASS | fresh direct-entry Desktop 人物参考 I2I 只调用一次 `generate_image`，`mode=subject_reference`；864×1152 新图摘要与附件不同，主体特征保持，消息/预览/保存/重启持久化通过 |
| AC-IMG-003 | PASS | direct-entry 普通文本真实 1 turn 返回 `DEMO_FAST_OK`，图片 Artifact 0、调用 0；仅看图分析返回文字，Runtime 无 function_call 且无新图片 Artifact |
| AC-IMG-004 | PASS | 真实 loading→success 不再因 Artifact 刷新闪烁；旧 orphaned 10% 轮被明确 fail closed 并释放队列；失败/重试/取消由 focused tests 覆盖 |
| AC-IMG-005 | PASS | 真实 T2I 与 I2I 均可在 Tauri lightbox 预览；native save 输出为 0600 JPEG，可解码且摘要与对应 provider Artifact 一致 |
| AC-IMG-006 | PASS | owner-only Key 文件、child env allowlist、content-free provider/Artifact 测试通过；真实事件无 Key/base64 |
| AC-IMG-007 | PASS | HTTP/业务状态/计数/base64/魔数/尺寸/缺字段均 fail closed，无自动付费重试 |
| AC-IMG-008 | PASS | canonical launcher 进程链与同 profile latest debug app 已 fresh 复跑；fresh 及 Settings→quit→restart 均无登录直达 `/chat`，Settings 零凭据控件，Host 自动启动/退出；exact profile 正负 focused 回归 PASS |

## 4. UI 与真实结果

- 已授权的 5 次 image-01 调用全部完成且均为 `n=1`；最终 Desktop I2I 使用第 5 次后账本为 5/5，不再调用。
- Host 真实事件已证明 `started → progress → completed → turn.completed`；失败与取消由 focused tests 证明不会留下伪 ready。
- fresh Desktop 已无登录直达 `/chat`，完成 ordinary text、T2I、analyze-only 和人物参考 I2I；图片消息展示、预览、保存与重启持久化均通过。
- canonical `pnpm tauri:dev` / `pnpm tauri:demo-fast` 进程链与同 profile latest debug app UI 均已 fresh 通过；旧 bundle 污染已清除。
- I2I terminal live projection 残留已通过终态权威重同步修复；重启后无重复回答或“正在生成”残留，Finder 往返仍保持精确会话路由。
- 默认 Desktop 测试现与治理 Profile 对齐：`demo_fast` 438/438 全绿；S9B-D 不再误报无关 package 变动；S10D-H 只保留在显式 `production_hardened` 入口且继续真实失败。

## 5. Diff 与限制

- `yijie`、`yijie-desktop`、`yijie-agent-host` 的 `git diff --check` 均 exit 0；最终 status/stat 已复核，未提交本地运行产物或凭据。
- 完整 diff 审阅：静态独立审计完成；未发现 P0/P1，审计提出的 response presence P2 已修复。
- 已知限制：单张人物参考；local only；历史 S10D-H 不在本路线内且继续 FAIL/PAUSED。

## 6. Public Demo（仅 exposure=public）

- 本路线 `exposure=local`，DP 不适用；若改为公网，必须新增服务端 Key、费用限制、访问控制、错误脱敏、
  输入/超时限制、恢复方式和公网 smoke。

## 7. 结论

- `D0` 产品/UX完整：PASS
- `D4` 本地真实可用：PASS
- `DP` 公开 Demo 可用：N/A
- 验证时间：2026-08-24 13:54 +08:00（8/8 Must AC 与真实业务 smoke 保持 PASS；默认 demo_fast 测试 438/438，全量 build、治理 47/47 与 D4 PASS；production_hardened 显式入口只保留历史 S10D-H 阻断；付费账本 5/5）
