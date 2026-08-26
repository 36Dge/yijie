# Codex Desktop 冻结身份（只读证据）

> Freeze ID: `codex-desktop-26.818.61809-build-7019-2026-08-26`
> Freeze started: `2026-08-26T10:01:56+08:00`
> Evidence classification: `local-metadata-observation`

## 已自动核对

| Field | Frozen value | Evidence |
|---|---|---|
| App bundle | `com.openai.codex`（当前 Codex Desktop/ChatGPT.app） | 本机已安装 app bundle；不复制 binary |
| Short version | `26.818.61809` | `plutil -extract CFBundleShortVersionString raw .../Contents/Info.plist` |
| Build | `7019` | `plutil -extract CFBundleVersion raw .../Contents/Info.plist` |
| Info.plist SHA-256 | `c930ae93debd168094467324b8f6c6ecec643fa218dacbbf390de84c9469f55d` | `shasum -a 256` |
| Info.plist local modification time | `2026-08-25T09:50:43+0800` | macOS `stat`，只作本机证据，不视作 OpenAI 发布日期 |
| macOS system appearance | `Light`（推断） | 全局 `AppleInterfaceStyle` key 不存在；这只证明系统默认，不证明 App 内主题 override |

命令中的 App 路径固定为系统 `/Applications/ChatGPT.app`，不包含用户目录、正文、凭据或商家数据。

## 当前不可自动观察

| Field | Status | Reason | Impact |
|---|---|---|---|
| App 内实际主题 | `reference-unobserved` | Codex 自身窗口不可由当前 Computer Use 安全读取 | 人工采集时需同时记录 light/dark |
| 当前窗口尺寸 | `reference-unobserved` | 同上；不通过读取私有偏好或其他屏幕 API 绕过 | 人工截图需记录像素尺寸和缩放 |
| Composer/approval/scroll 等交互配置 | `reference-unobserved` | 同上 | 13 个场景保留版本身份，但不宣称已观察交互 |
| 版本专属截图/录屏 | `reference-unobserved` | Computer Use 返回“不允许操作 `com.openai.codex`”的安全限制 | D4 参考 UX 证据待 Owner 人工补采 |

## Freeze 与 drift 规则

1. 本 Epic 的 reference baseline 始终是 `26.818.61809` build `7019`，不是“本机最新版本”。
2. 后续发现本机 App 版本不同，只登记 `version-drift`；不得自动修改本文件、fixture 或验收期待。
3. 只有 Owner 明确批准新 baseline，才新建独立 Freeze ID 和变更记录；不得覆盖本证据。
4. 官方通用文档、synthetic fixture、Runtime schema 或模型记忆均不能替代此 build 的版本专属 UI 观察。
