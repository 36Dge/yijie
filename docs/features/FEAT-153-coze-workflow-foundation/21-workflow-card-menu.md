# 工作流卡片编辑与删除菜单

2026-09-13，FEAT-153 local 产品追加。用户要求真实工作流卡片的“更多”提供“编辑”“删除”，编辑打开对应工作流页面，删除先提示确认。保留前序工作区与原 D4 证据。

`contract-impact = additive`。Owner 为段成威；Contracts 源 `openapi/workflow-local/workflow-local.yaml` 新增 `DeleteInput/DeleteRequest/DeleteResult` 和 `DELETE /v1/workflows/{workflow_id}`，版本 `1.2.0-local-candidate`。Producer 为 Coze/API/native，consumer 为 API/native/Vue；Coze iframe 仅同步生成物，不获得删除桥操作。固定 local scope、鉴权和 Chat 边界保留。用户本次操作要求授权其必要的本地跨仓实现，不构成生产、tag 或独立评审批准。

- 编辑使用既有资源 ID 路由。四张静态示例没有真实资源，保留示例语义，不假造后端编辑/删除。
- 删除为 Coze 已有 `workflow_meta.deleted_at` 软删除；草稿、版本、运行历史、API 资源归属与审计行保留，无数据库迁移或物理清除。本地旧二进制的 GORM 默认读取也会排除已删除记录。
- 以原 ID + `expected_revision` 幂等删除，不扩展旧 `OperationKind` 或回执模型。普通重试返回相同结果；若版本变化或目标仍在运行，分别返回已有 `revision_conflict` / `run_busy`。并发删除/保存/运行登记共用现有 scope 行锁。
- API 先登记删除尝试，再请求 Coze，确认后登记结果；尝试日志按调用追加。结果不确定时保留原目标/版本并重试幂等 DELETE，不能改版本、改目标或乐观移除卡片。已有编辑会话在确认删除后撤销，后续服务操作仍由资源存活检查拒绝。
- 新 native `workflow_delete` 只接受既有可信 App 主窗口和 exact local profile，无新网络目标、iframe 能力或安全权限。菜单与确认层保留键盘、焦点和可访问名称；删除中禁止重复提交，错误保持提示，成功后才从列表移除。
- 源候选先生成并同步到三消费者；仍使用显式 local-candidate，不冒充不可变发布 pin。Fallback 为 Contracts `32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4`。未来提交时先 Contracts，再消费者精确 pin，最后元仓；本次不提交或推送。

验证只使用本次新建的具名合成流程，不删除截图或既有验收流程，不执行强杀/攻击/权限破坏测试。物理数据保留，不宣称已有回收站或恢复 UI。部署顺序为 provider → native/UI；回滚保留 tombstone 和历史数据，旧读取继续隐藏软删除项。

状态：本次 local 卡片菜单追加已实现并通过限定验收。工作区基线及证据：`evidence/card-menu-20260913/`。


## 验证结果

- Contracts canonical generate/check、13 项正常 schema/browser 检查、全仓 lint，以及 fallback OpenAPI/Proto/AsyncAPI/JSON Schema breaking 检查通过；旧 OperationKind 原样保留。API/Coze/Desktop 生成消费副本同步，source-first 始终先于实现。
- Desktop lint/typecheck、64 项定向组件/状态/路由/侧栏测试、文档站和 canonical packaged 构建通过。测试包含真实菜单点击事件、带名称确认、取消零写入、收到真实成功前保留卡片、过期列表不能恢复已删除项、相同 ID/revision 重试、重试前置失败保留原不确定状态，以及 axe。14 项限定 native 测试、Clippy `--lib -D warnings` 与 `cargo fmt --check` 通过。
- API workflow lint/race 测试通过，覆盖归属校验、按尝试追加审计和确认删除后撤销已有编辑会话。Coze workflow 定向测试通过：软删除/旧记录保留、版本冲突、正常运行状态拦截、HTTP 请求响应、幂等重试及删除后 read/bootstrap/save 拒绝。
- 开发检查发现并修复 GORM 链式 `Unscoped` 复用会污染后续查询的问题：只给 metadata 单次读取设置包含软删除项，其余归属、操作、草稿查询继续使用原 transaction。没有修改测试断言来回避该问题。
- 真实 packaged App PID 52971 新建 `7684967100560965632`，名称“FEAT-153 卡片删除菜单验收”，revision `7684967100565159936`。只使用本次新建合成资源，截图及原有 16 条工作流未删除。
- 真实“更多”鼠标点击打开且仅显示编辑/删除（01）。菜单项的 CUA AX 点击一次返回外部状态变化，随后使用正常方向键/Return 验证选择；“编辑”进入同 ID 的真实 Coze 页面。不能把该 AX 自动化限制写成鼠标菜单项已逐项实测；组件 click handler 另由正常 DOM 测试验证。
- 删除菜单先出现具名影响提示，取消后卡片仍在、API detail 完全保留，焦点回到“更多”。亮/暗 1180×760 提示原始截图为 02/03，系统外观已恢复浅色。
- 点击确认后，App 显示已删除并移除唯一目标，焦点落到创建按钮。切换 Chat 再返回工作流，目标仍不存在，其余 16 个真实菜单保持可用。API detail 为 404/resource_not_found，完整剩余列表与创建测试资源之前的 16 条记录逐字一致（after-delete-api.json）。最终列表截图 04 的实际尺寸为 1346×849；不声称是请求但未达成的 1440×850。
- MySQL 只读查询确认 metadata 行和 tombstone 存在，draft 及原 revision 仍保留（mysql-readback.json）。PostgreSQL 的一次 UI 删除记录 requested/success 各一次。随后仅对已经删除的同一 ID/revision 执行一次正常 API 幂等重试，返回相同 DeleteResult；复查审计 requested/success 各两次（postgres-audit-after-retry.txt）。没有物理清理数据。
- candidate-files.json 冻结的代码摘要始终一致；99 个来源/日志/JSON 文件针对 K_NA/K_AC 两个当前凭据值扫描无命中。截图目视未见凭据。保持原生凭据边界，不调用模型、商家平台或付费服务。

## 范围与交付

本轮为真实 packaged 菜单/删除专项，不冒充 dev 或整项 fresh D4 重跑。运行中拦截、旧会话撤销、普通异步结果不确定由服务/native/组件定向检查覆盖，没有真实故障注入、强杀、权限破坏、攻击 fixture 或生产公开验收。保留原始 17、前序 19/20 的候选范围。

当前 App 留在工作流列表，受控栈 ready；本次只有一条新建合成流程被软删除。没有数据库 migration、Codex Runtime、Tauri capability、CSP 或新网络目标变化；新增 command 使用原可信主窗口与 local 权限检查。Infra 无源码更改，只通过 canonical 入口正常停止、构建、启动。旧 Chat/公共契约锁和用户已有未提交改动保留。

变更仍在工作区，未 git add/commit/push。后续交付先形成 Contracts 不可变提交并逐仓重新 pin，再提交 API/Coze/Desktop 与元仓记录，不能发布当前无 source_commit 的 local-candidate 副本。
