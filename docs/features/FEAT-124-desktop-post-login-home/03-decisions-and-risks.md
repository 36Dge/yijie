# FEAT-124 决策、风险与安全预审

## 1. 关键决策

| Decision ID | 问题 | 可选方案 | 当前选择 | 理由 | Owner | 状态 |
|---|---|---|---|---|---|---|
| DEC-001 | 参考 HTML 的定位 | 生产源码 / 视觉交互参考 | 视觉交互参考 | 必须翻译成 Vue、Router、token 和正式组件，避免第二套实现 | 段成威 | Confirmed |
| DEC-002 | 实现仓库 | yijie / yijie-desktop / yijie-codex | yijie-desktop | 登录后 Mac 用户体验属于 Desktop | Architecture governance | Confirmed |
| DEC-003 | Feature contract-impact | none / additive / semantic / breaking | additive | 输入正文仍为进程内；但新增版本化侧栏偏好使状态跨应用重启可观察。公共 wire 仍为 none | 段成威 | Reclassified 2026-07-30 |
| DEC-004 | 默认路由 | 保持 `/chat` / `/new-task` / `/home` | 保持 `/chat` | 避免路由迁移并与现有默认入口兼容 | 需求提出人 | Confirmed 2026-07-30 |
| DEC-005 | 输入区范围 | 仅输入样式 / 本地草稿 / 真实任务提交 | 首页视觉 + 页面内本地输入 | 不发送、不持久化、不接 API、Agent Host 或 Runtime | 需求提出人 | Confirmed 2026-07-30 |
| DEC-006 | App Shell Pattern 差异 | 参考稿覆盖 / 参考稿仅为入口态 / 合并顶部状态区 | 参考稿定义 `/chat` 新建任务入口态；不展示顶部状态区 | 满足本次首页需求，同时把完整 Chat 工作区留在当前范围之外 | 段成威授权 Codex | Accepted in App Shell 2.0.0 + Chat 1.1.0 |
| DEC-007 | 设计系统落地 | 页面局部硬编码 / 迁移最小 token 与基础组件 | 迁移最小可复用基础能力 | 避免继续扩大设计系统债务 | 段成威 | Approved at G2；实施仍受 G2A/Slice 门禁约束 |
| DEC-008 | 侧栏宽度与控制 | 仅 240px / 240px + 72px / 自适应 | 默认 240px、可收起 72px；按钮固定右边界并与品牌区垂直居中 | 两种宽度已有 token；固定边界位置在两种模式下均可发现 | 段成威授权 Codex | Documented |
| DEC-009 | 导航可用性与位置 | 全部可用 / 占位 / 禁用或隐藏 | “任务记录”紧随“新建任务”；未实现模块禁用；无权限模块隐藏；Settings 置底 | 保持任务创建/历史的邻近关系，避免与工作台、定时任务混淆 | 段成威授权 Codex | Documented |
| DEC-010 | 侧栏状态生命周期 | 仅当前组件 / 跨路由 / 跨应用重启 | 使用 `yijie.desktop.ui.sidebar.v1 = expanded｜collapsed` 跨路由和重启持久化 | 侧栏是低风险个人 UI 偏好；默认/损坏回退均为展开，回滚安全 | 段成威授权 Codex | S0 committed and validated；G2A Approved |
| DEC-011 | Placeholder 播放 | 静态 / 随机 / 固定轮播 | 5 条文案固定顺序每 4 秒轮播；聚焦/输入暂停；reduced-motion 固定第一条 | 可预测、可测试，并减少输入和辅助技术干扰 | 段成威提供文案并授权 Codex 交互设计 | Documented |

## 2. ADR 判定

- 是否改变仓库职责：否，目标仍属于 `yijie-desktop`。
- 是否改变跨仓依赖方向：否。
- 是否改变公共 wire 契约：否。
- 是否改变本地持久化边界：是，新增一个版本化、低风险、Desktop 私有的侧栏偏好 key，分类为 `additive`。
- 是否改变安全边界：否；本需求只改变导航呈现，既有授权层仍为权威。
- 是否改变 Accepted Design Pattern：是。已确认 `/chat` 首页不展示 App Shell 顶部状态区，并作为新建任务入口态而非完整 Chat 三栏工作区。
- 当前结论：相关设计 Pattern 已由段成威确认继续执行。App Shell Pattern 2.0.0 包含迁移/回滚规则；当前不改变跨仓职责或安全边界，暂不新增 ADR。若后续把偏好跨设备/租户同步或扩展为全局导航重构，再补正式 ADR。
- 架构/设计 Owner：段成威。

## 3. 风险登记

| Risk ID | 风险事件/触发条件 | 概率 | 影响 | 预防控制 | 检测 | 恢复/回滚 | Owner | 残余风险 |
|---|---|---:|---:|---|---|---|---|---|
| R-001 | 把静态 HTML 直接复制进 Vue，形成第二套 token/icon/router | 中 | 高 | 明确参考稿只作参考；先列组件/token 迁移计划 | Diff Review、硬编码扫描 | 回退页面提交，保留设计文档 | 段成威 | 低 |
| R-002 | `/chat` 首页改造破坏现有 Tasks、Settings 或深链入口 | 中 | 高 | 保持 `/chat` 路径；明确 Tasks/Settings 独立路由；增加 Router 测试 | 路由单测、返回/深链 smoke | 恢复旧页面提交或 route table | 段成威 | 低-中 |
| R-003 | 后续把当前本地输入扩大为真实任务提交但未重做契约评估 | 低-中 | 高 | 当前明确不提交；范围变化触发 Contract First 和安全预审 | Review Feature 文档与网络调用 diff | 停止实现，回到契约步骤 | 段成威 | 低 |
| R-004 | 实现已确认的新入口态但未同步 Accepted App Shell/Chat Pattern | 中 | 中-高 | G1 前更新并评审设计文档 | Design Review、文档 Diff | 暂停实现或恢复 Accepted Pattern | Product/Design Owner | 低-中 |
| R-005 | 为首页一次性迁移过多 design exports，扩大 diff | 中 | 中 | 只迁移本页必需 token、Logo、Icon、Shell 组件；切片提交 | Diff stat、组件复用审查 | 拆分/回退非必要迁移 | 段成威 | 低 |
| R-006 | 暗色或最小窗口不可用 | 中 | 中 | 主题 token、1180×760/1440×900 验收 | 实际截图/视觉检查 | 修正 token/layout 后再进入 G4 | 段成威 | 低 |
| R-007 | 未实现项未正确禁用，或无权限项仍被展示/可深链访问 | 中 | 高 | 未实现项禁用；无权限项隐藏；服务端授权保持权威 | 导航状态测试、直接深链授权测试 | 隐藏/禁用入口，回退路由 | Product/Security Owner | 低-中 |
| R-008 | 未提交任务文本进入日志或错误上报 | 低-中 | 高 | 不记录 textarea 正文；不擅自持久化 | 日志与遥测 diff 检查 | 删除记录点并清理测试数据 | 段成威 | 低 |
| R-009 | 需求包的本机绝对参考路径在其他开发机不可访问 | 高 | 中 | 入库前登记参考资产的可共享、合规位置或保存批准截图/摘要 | CI/Reviewer 路径检查 | 使用仓库内批准设计资产引用 | Requirement Owner | 中 |
| R-010 | 侧栏偏好值损坏、不可用或回滚后遗留 | 低-中 | 低-中 | 版本化 key、封闭枚举、未知值回退展开；旧版本忽略 | reader 单测、重启 smoke、存储检查 | 删除单一 key，恢复默认展开 | 段成威 | 低 |
| R-011 | 轮播 placeholder 干扰输入或辅助技术 | 中 | 中 | 聚焦/输入暂停；稳定 label；无 aria-live；reduced-motion 固定第一条 | 组件计时测试、键盘/读屏检查 | 关闭轮播并保留第一条 | 段成威 | 低 |
| R-012 | 锁定的传递依赖 `postcss@8.5.16` 命中 GHSA-r28c-9q8g-f849 | 已发生，候选已修复 | 高 | 段成威批准 workspace root override 固定 `8.5.18`；不把构建绿色替代依赖审计 | `pnpm why postcss` 仅 8.5.18；`pnpm audit --prod` 0 known vulnerabilities | 保留 override，直到上游解析天然不低于修复版本；移除前复跑审计 | 段成威 | 低 |

## 4. 威胁建模

| 资产/边界 | 威胁 | 攻击路径 | 服务端/客户端控制 | 安全测试 | 残余风险 |
|---|---|---|---|---|---|
| 登录态与租户上下文 | 页面自行信任本地状态或伪造租户 | 临时 store/localStorage 决定权限 | 只消费既有服务端权威；本需求不改变认证 | 未登录、过期、跨租户状态测试（条件性） | 认证实现尚待定位 |
| 未提交任务文本 | 敏感商家信息进入日志/持久化 | debug log、error payload、自动草稿 | 仅页面内存，不记录正文、不持久化 | 日志/存储检查 | 低 |
| 导航权限 | 用户看到/进入无权限模块 | 静态导航不考虑权限 | 无权限入口隐藏；服务端授权仍是权威 | 隐藏状态、直接深链 | 取决于既有权限投影质量 |
| 品牌/图标资产 | 未授权或不可维护资产进入包 | base64/内联 SVG 直接复制 | 使用批准 Logo 和 Lucide registry | 制品/资源 Diff Review | 活跃 registry 未迁移 |

## 5. 数据生命周期

| 数据类别 | 收集 | 使用 | 存储 | 共享 | 保留 | 删除 | 审计 |
|---|---|---|---|---|---|---|---|
| 任务输入文本 | 用户在 textarea 输入 | 仅用于当前页面本地编辑 | 不持久化 | 不共享 | 页面生命周期 | 离开页面或应用重启后释放 | 不记录正文 |
| 登录/租户状态 | 既有层提供 | 决定进入 App Shell 与权限呈现 | 本需求不改变 | 仅传给必要 UI | 按认证策略 | 按认证策略 | 不记录 token |
| 导航事件 | 用户点击 | 本地 Router | 默认不新增存储 | 默认不共享 | N/A | N/A | 若以后加 analytics 需单独评审 |
| 侧栏偏好 | 用户点击收起/展开 | 恢复 240/72px 模式 | 普通 Web Storage 单一版本化 key | 不共享 | 应用本地数据生命周期 | 删除 key 或清理应用数据 | 不记录业务遥测 |
| 视觉样例 | 合成文案/布局 | 设计与测试 | 文档/测试 fixture | 仓库内 | 随版本 | 随版本 | N/A |

## 6. 高风险操作、审批与审计

| 工具/操作 | 用户意图 | 参数/影响范围 | 审批人/有效期 | 默认行为 | 审计字段 |
|---|---|---|---|---|---|
| 页面导航 | 明确点击模块 | 当前 Desktop 路由 | N/A | allow if visible/authorized | route key（可选） |
| 真实任务创建 | 用户提交业务任务 | 可能触发 Agent/平台工具 | 尚未定义，不在当前范围 | deny/not implemented | 若纳入则需 trace/request/tenant/user/task |
| 平台写操作 | 不在本需求范围 | N/A | N/A | deny/not exposed | N/A |

未被审批策略覆盖的真实写操作默认不得由首页输入框触发。

## 7. 临时例外

| Exception ID | 原因 | 范围 | Owner | 批准证据 | 到期日 | 补偿控制 | 移除条件 |
|---|---|---|---|---|---|---|---|
| N/A | 当前不批准临时例外 | N/A | N/A | N/A | N/A | N/A | N/A |

## 8. Codex 停止条件

- 尚未完成本地侧栏偏好的兼容/回滚测试设计和 Gate 2A 证据计划。
- 04—07 技术、测试与实施文档已完成并通过结构检查；段成威已于 2026-07-30 明确批准 G2，并只授权先执行 S0。
- 需要修改认证、会话、租户、API、Agent Host 或公共契约。
- 需要新增 Tauri plugin/capability/command、外部 URL、sidecar 或安全存储。
- 需要直接从 `docs/design/exports` 导入运行时代码。
- 需要新增依赖或第二套 UI/图标库。
- 基线出现新失败或工作区出现未知改动。
- 视觉实现只能通过硬编码 token、弱化测试或跳过暗色/最小窗口检查。

## 9. 批准记录

| 范围 | 决策人 | 结论 | 日期 | 证据 |
|---|---|---|---|---|
| 业务范围 | 段成威 | Approved：需求范围、五条文案与里程碑 | 2026-07-30 | 用户确认 |
| 产品/设计 Pattern | 段成威授权 Codex 定稿 | Approved | 2026-07-30 | DEC-006、DEC-008—DEC-011 及三份 Accepted 设计文档 |
| 架构/Contract Impact | 段成威 | `additive` / G2A Approved：仅 Desktop 私有侧栏偏好 | 2026-07-30 | 固定实现 `b937eb8fdace6e4a2fcb53c158660ffa92fcf79e`；允许 S1 consumer foundation |
| 安全/数据 | 段成威 | UI 呈现已确认；既有服务端授权不变 | 2026-07-30 | 无权限模块隐藏、输入正文不持久化/不记录 |
