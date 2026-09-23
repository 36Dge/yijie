# FEAT-155 · 4A 管理页面与手动保存闭环实施报告

2026-09-19。按用户明确授权实施[32方案](32-phase-4a-management-ui-implementation-plan.md)，**4A 本地候选实现及零模型原生 UI 闭环完成，报告后停止，不进入 4B。** 普通入口仍 SQL15/Store5，显式候选 SQL23/Store6；全部 Must 和 D4 仍 pending / NOT RUN。累计真实文本 0/12，图片和商家调用 0。工作区与固定产物保护见[审查记录](evidence/phase-4a/workspace-review.json)。

## 1. 交付结果

| 项目 | 结果 |
|---|---|
| 共享授权 | 新 `chat_bind_management_context_v1` 复用原 context DTO、NativeAuth 和 AuthorizationManager。App/chatStore 统一协调；管理冷启动不取 readiness、不构造 Host、不恢复或投递旧操作。已有聊天 context 可直接复用；进入聊天时仍走原执行准备。 |
| 私有读契约 | 追加卡片、历史行和管理原请求回执三个只读命令。原 21 命令保持，24 命令从同一私有 schema 生成 Rust/TS 与严格验证器。共享 PlanView 不添加展示字段。 |
| 候选 SQL23 | 仅增加 nullable created_at 和 scope 索引；旧行未知，新建同事务记真实时间，编辑/暂停/回放不改。1—22 迁移字节不变；22→23、旧聊天、reader 重开及普通 15 通过。 |
| 管理 UI | 原位导航、受 schedule.read 保护的深链、两 Tab、名称/内容搜索、时间排序和有界分页。手动表单含四频率、IANA 时区、native 预览和三目标；只保存 paused，无执行 grant。 |
| 安全管理 | 编辑带 revision；暂停/删除沿既有原生事务及占用保护。提交不明只在同 scope 内存保留原请求与原内容，可查证或显式同请求重试；无回执不当失败，客户端不自动重发。 |
| 只读历史 | 名称/内容来自运行快照；当前计划仅作生命周期筛选。未执行槽标明当前计划参考；缺失执行时钟显示未知/未开始，不推算业务成功。含已删除计划筛选。 |
| 导航与确认 | 检查全部 composerDrafts 及当前附件；未发送内容有离页确认，不删除其它 native 草稿目标。脏表单、删除确认默认安全选项。执行/草案/通知/唤醒控件不接线。 |

整体 `contract-impact=breaking`：候选 SQL23 对旧 binary 的可读边界及授权启动职责改变；独立新读命令为 additive。仅 Desktop 产品代码和元仓文档有本批变更，Host、Contracts、Runtime 源码未改，无新公共 wire、依赖或 Tauri capability。

## 2. 实际启动中补齐的必要边界

canonical 入口原 FEAT-152 校验要求 Host 全部源码与旧提交一致，拒绝已批准的 FEAT-155 候选源码。因此增加 Desktop 私有 `scheduled-host-build.candidate.json`，固定当前 Host 的完整 cmd/internal/api/go.mod/go.sum 文件集及 SHA、base commit 和 origin；显式 local/demo_fast 候选才接受这个精确集合，同时核验原 FEAT-152 提交/wire、草案/恢复/input-only 同源生成物。构建后再查一次；没有跳过校验或允许任意 dirty checkout。普通入口的原提交校验保持。

候选允许通过同一 canonical `--packaged` 标准构建进入主 App，仍拒绝 stable/workflow/Sorftime 组合，图片关闭，固定 29 Runtime 与独立 `demo-fast-scheduled-candidate-v1` 数据根保持。没有额外展示后端、伪造 native 返回或替换受保护 Runtime。

开发进程不在 UI 自动化可连接的应用清单中，使用活动监视器的“退出”（未用“强制退出”）正常关闭后改用标准包。后续使用 App 的正常退出与相同入口重开。一次工具在读取已关闭窗口时重新打开无候选授权窗口，该窗口立即正常关闭，未以其代替候选验证；后续关闭后仅检查进程，不再自动读取已关闭 App。

## 3. 验证与边界

[检查索引](evidence/phase-4a/checks.json)、[原生 UI 记录](evidence/phase-4a/native-ui.json)、[账本只读结果](evidence/phase-4a/ledger-read-only.log)。源审查由本任务完成，未伪称独立人工/子代理审查。

| 检查 | 实际结果 |
|---|---|
| 原生 FEAT-155 回归 | 101 项通过；另补 SQL22→23 的旧聊天/ledger/reader 重开 1 项、已观察回执必须包含原生计划 1 项，以及原 context 闭合契约 1 项。末轮 4A 的 5 项原生与 5 项表单/回执测试复测通过。首次输出目录未预建导致 3 个旧测试导出失败，预建目录后完整 101 项重跑通过。 |
| 契约 | 24 命令、29 native 请求/响应，严格 AJV/native/TS 一致性通过；旧 context DTO 定义保持原样。 |
| 前端 | 本批 53 项定向检查、管理无 Host 绑定 1 项、聊天 RouterView 离页保护 1 项通过。lint / 类型 / build 通过。 |
| Rust | fmt、all-targets clippy `-D warnings` 通过。 |
| 真实候选 UI | 手动创建暂停、编辑 revision 2、创建时间保持、正常重开同一计划、删除 revision 3、记录空态、键盘、1180×760 最小窗口及亮暗主题通过。已有聊天无可用选项时拒绝保存；三目标的有记录组合由既有 native 测试覆盖。 |
| 真实账本 | SQLCipher 以 READ_ONLY 开库，只输出聚合数字：SQL23，1 个已删除的合成计划、3 个管理回执；grant/run/outbox/turn/session/draft source 均为 0。该只读核对不访问 Keychain 或日常库。 |
| 文档 | Desktop 文档构建通过；元仓 strict D0、lint 和 50 项治理测试通过；通用 committed-claim audit 此次列出 0 项，不把它当本包证据。 |

实际 UI 检查发现确认框最初聚焦“放弃修改”，已调整按钮顺序，并复测默认“继续编辑”/“取消”。context 更新/到期清未提交输入，不能以跨授权保留草稿掩盖该边界；同 scope 已发出的不确定请求单独保留并有合成测试。

聊天既有回归中 3 项显示断言仍失败。将本轮起点 SHA 完全一致的 ChatPage 源码用于对照后复现相同 3 项（44 通过），不是 4A 新增回归；未修改无关旧显示逻辑或把全量 suite 写成 PASS。Vite 仍提示较大的懒加载 chunk。完整发布 pin / 通用 sibling dirty 门禁不由本批候选证据替代。

真实模型/Provider、已有目标的真实投递、非空历史 UI、休眠唤醒、系统通知、日常库升级、全部 Must 和 D4 不在本批通过结论中。未采用强杀、故障权限、攻击载荷或伪造 Runtime 的验收。

## 4. 停止点

4A 已完成并停止。候选库仅保留本批合成计划的删除墓碑与管理回执，没有可执行计划；不向 4B 自动推进。后续如获单独授权，再规划对话草案 UI、启用/有限授权及运行控制的接线，保持 FEAT-155 原目标与既定额度。
