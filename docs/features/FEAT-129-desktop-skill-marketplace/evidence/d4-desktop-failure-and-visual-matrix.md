# FEAT-129 Desktop D4 失败恢复与视觉矩阵

验证日期：2026-08-26（Asia/Shanghai）

## 固定版本与安全边界

- Contracts：`164b14f609537d727a52326832da04430aecc4ab`
- Agent Host：`1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`
- Skills producer：`10c45bec29603b002e861e1499d5b4e684251af5`
- Desktop 最终提交：`6745eb793e417c6685d1900231477c59ec81a5fd`
- Manifest v2 SHA-256：`39a898111ba3dcae2f369fdcb571a2e892830d1d0a57c90ab6210a0ab897a649`
- local-development manifest SHA-256：`cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5`

真实 Desktop 检查只使用独立应用标识、独立 App Resource 和独立 App Data。收尾时只读取正式 App Data 的文件计数、权限和时间戳元数据，未读取文件内容，也未写入或删除正式用户的 Skill 安装目录。用户明确收紧安全边界后，不再执行故障注入、权限变更、进程强制结束或资源替换；Zip Slip 仅由 Agent Host 既有的临时目录契约测试验证。D4 收尾阶段未调用模型，付费调用保持历史记录 `1/1`，本阶段新增调用为 `0`。

## 失败、原子性与恢复

| 场景 | 验证层级 | 可观察结果 | 原子性与 Runtime | 恢复/重试 |
|---|---|---|---|---|
| 摘要损坏 | 隔离的真实 Desktop + Agent Host | 安装返回 `archive_checksum_mismatch`，卡片保留错误和重试入口 | 无目标目录、staging、安装回执；`runtime_visible=false`；只读源包保留 | 恢复已审核资源后，在同一卡片点击重试，状态收敛为 installed + enabled + runtime-visible |
| 资源缺失 | 隔离的真实 Desktop + Agent Host | 安装返回 `bundle_missing` | 无目标目录、staging、安装回执；`runtime_visible=false`；其他内置资源不受影响 | 恢复资源后同卡片重试成功 |
| Host 不可用 | 隔离的真实 Desktop | 卡片显示服务不可用并提供重试 | 未创建目标目录或 staging，内置源包保留 | Host 正常恢复后同卡片重试成功 |
| 安装根不可写 | 隔离的真实 Desktop + Agent Host | 安装返回 `install_failed` | 无目标目录、staging、安装回执；`runtime_visible=false`；源包保留 | 恢复目录正常状态后同卡片重试成功 |
| 安装中断/重放 | 隔离的真实 Desktop + Agent Host | 观察到事务 staging 后重启隔离 Host | 重启重放清理 staging 和未提交目标，Runtime 保持不可见，源包保留 | 正常资源下可重新安装；此场景同时发现并修复 Host journal 触发 watcher 自反馈的问题 |
| Zip Slip | Agent Host 既有临时目录契约 fixture + Desktop DTO/UI 自动化 | Host 返回 `archive_unsafe`；Desktop 将该错误稳定映射为可理解、可重试状态 | 临时受管根中无目标、staging、backup 或 failed 残留，受管根外无 `escape.txt`，Runtime 不可见 | 使用正常 fixture 的后续安装通过；未在真实 Tauri 应用中注入危险归档 |

对应截图：

- [摘要失败](desktop-checksum-failure.jpeg) / [摘要恢复后重试成功](desktop-checksum-retry-success.jpeg)
- [资源缺失](desktop-resource-missing.jpeg) / [资源恢复后重试成功](desktop-resource-missing-retry-success.jpeg)
- [Host 不可用](desktop-host-unavailable-retry.jpeg) / [Host 恢复后重试成功](desktop-host-retry-success.jpeg)
- [安装根不可写](desktop-readonly-install-failure.jpeg) / [恢复后重试成功](desktop-readonly-retry-success.jpeg)
- [安装中断后恢复](desktop-install-interrupted-recovered.jpeg)

Zip Slip 安全边界由以下只使用临时目录的既有测试验证，均 exit 0：

```text
go test ./internal/skills -run '^TestArchivePreflightRejectsUnsafeEntrySets$/zip_slip$' -count=1
go test ./internal/integration -run '^TestManagedSkillRejectsPinnedChecksumAndZipSlipFixturesAtomically$/zip_slip$' -count=1
go test ./internal/app -run '^TestSkillArchiveUnsafeErrorMatchesPinnedFixture$' -count=1
```

## 视觉与交互矩阵

自动化验收覆盖以下状态，AC-009 不设置人工验收门禁：

- tooltip 同时支持鼠标悬停与键盘聚焦；焦点截图见 [keyboard focus tooltip](desktop-install-tooltip-keyboard-focus.jpeg)。
- loading、success、empty、error/retry 与重复操作锁定。
- 删除按钮的操作区 hover、按钮 danger 状态、确认/取消/Escape、确认后的焦点恢复。
- 亮色/暗色主题 Token，以及 1180×760 最小窗口下的关键操作可达性和静态 overflow 检查。
- watcher 修复后的正常页面在观察窗口内 scan 计数保持 `2 → 2`，Host journal 不再触发自反馈；截图见 [fixed watcher](desktop-fixed-watcher-light-1180x780.jpeg)。

已有真实窗口证据：

- [亮色 38 卡片](desktop-skill-marketplace-light-1180x780.jpeg)
- [暗色 38 卡片](desktop-skill-marketplace-dark-1180x780.jpeg)
- [安装并启用](desktop-skill-installed-1180x780.jpeg)
- [卸载确认](desktop-skill-uninstall-modal-1180x780.jpeg)

## 最终正常门禁

- Skill resource sync/check/release-boundary：PASS，38 项，分类严格为 `5/9/7/9/8`。
- `pnpm generate:check`：PASS；最终 implementation digest lock 与 `resources.rs` 一致。
- `pnpm test:demo-fast`：72 files、548 tests 全部 PASS。
- `pnpm lint`、`pnpm build`：PASS。
- `cargo fmt --all -- --check`、`cargo clippy --locked --all-targets -- -D warnings`：PASS。
- Rust library tests：265 passed、0 failed、3 ignored；忽略项均为既有环境型测试。

这些证据共同证明 Desktop 消费层只解析平台根目录并调用 Host API，安装事务仍由 Agent Host 独占；失败时不会出现半安装、越界文件或错误 Runtime 暴露，恢复正常依赖后可从原卡片重试。
