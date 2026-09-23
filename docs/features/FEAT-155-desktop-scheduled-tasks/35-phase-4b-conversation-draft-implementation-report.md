# FEAT-155 · 4B 对话创建与草案确认闭环实施报告

2026-09-19。按用户授权实施[34 方案](34-phase-4b-conversation-draft-implementation-plan.md)，**4B 本地候选实现和真实对话创建闭环完成，报告后停止，不进入 4C。** 已验证同一受限会话的澄清、候选、编辑确认、唯一暂停保存和正常重开。普通 SQL15/Store5、候选 SQL23/Store6 保持；没有新迁移、Runtime 改动或计划执行激活。全部 Must 的整体 fresh run 和 D4 仍未完成。

本批真实文本 **4 次**，计入总额 **4/12，剩余 8 次**；用户追加授权后本批上限为 5，未使用第 5 次。图片、商家及 MCP 外部调用均为 0。[原始及持续计数](evidence/phase-4b/provider-ledger.json)保留所有失败和成功请求，没有重置额度。

## 1. 交付结果

| 内容 | 实际行为 |
|---|---|
| 原生用途查询 | 新增 `chat_get_session_purpose_v1`，沿原 task.read、scope 和资源授权读取；普通 SQL15 返回 ordinary，不启动 Host。新叶类型由私有 schema 同源生成 Rust/TS，未修改旧会话 DTO。 |
| 原请求查证 | 新增 `schedule_read_draft_submission_receipt_v1`：区分未观察到、已受理及来源已删除；不猜 conversation/turn，不把查询当重发。定时 IPC 共 25 命令。 |
| 对话入口 | 管理页预填到原 ChatComposer，当前输入可明确交接；默认保留未发送草稿，scope/撤权清理遵守原规则。已有会话用途来自 native，不能由 URL 或名称声明。 |
| 受限对话 | 只接文本，隐藏附件、目录及普通权限切换；原 chatStore、native 事实、订阅和历史继续承载会话。后续澄清产生新 request/source/turn，原尝试操作不重发。 |
| 摘要与确认 | UI 只消费 native 校验的澄清/候选；复用手动表单并绑定 source/digest。提交沿原 confirm 事务唯一保存 paused，不走普通 save，不创建执行 grant/run。 |
| 不确定与恢复 | 原请求回执丢失先查证，同请求显式重试；确认不明按 source 查同一计划。正常重开从真实会话/轮次重发现来源，不自动 submit/continue。 |
| 必要显示修正 | 原生可用但不在用户项目列表的受管目录显示“任务目录”，不误报“项目已移除”；不符合草案格式时明确说明未保存，可补充说明。 |

本批 `contract-impact=semantic`，新私有读命令本身 additive。Desktop 与 Host 有实现变更，元仓记录方案/授权/结果；Contracts、Runtime 源码与固定二进制逐字节保持。没有新增依赖、Tauri capability、公共 Host API 或第二套执行状态机。Host 候选来源锁仅更新本批审查的四个构建输入，原完整文件集及原协议 pin 继续校验。

## 2. 真实调用发现的问题及修复

前两次请求均 HTTP 200，但返回 `action/questions` 对象，不符合固定草案 schema；同时 Provider 没有给出 phase。原生拒绝确认，未保存计划。不能把 HTTP 200 等同于产品成功。

首先将 canonical schema 加入开发者指引；本机新建/恢复组合能够观察到它，但原有真实会话仍返回旧格式。只读 rollout 证实原 developer 历史未更新。随后使用固定 Runtime 已支持的 `baseInstructions`，让同一 canonical schema 在新建与正常恢复后的每次 Provider 请求生效，保留历史原文。旧配置正常启动→退出→当前配置恢复的真实 Runtime/本机 Provider 组合验证通过，未改 Runtime，未替换已有二进制或操作历史。

原生草案识别增加受限的无阶段兼容：精确用途/binding、同一成功 completed turn、唯一完整 agentMessage、严格输出 schema 同时成立才能形成结果；明确 commentary、多个不一致答复、partial、失败和错误格式继续拒绝。原 phase 不改写为 final_answer，确认时重新验证 source/digest。该调整不放宽 schema，也不从任意正文截取 JSON。

第 3 次真实调用得到合法 needs_clarification，页面询问时间与时区；第 4 次补齐每天 09:00、Asia/Shanghai 和专属聊天，得到合法 candidate。用户路径中将名称改为“4B 合成摘要验收（已审阅）”，确认后保存为暂停计划。正常重开后从原来源再次定位 **同一 plan_id `01a0b8de-7cf5-7fe3-ab5d-128f81e7a193`**，版本仍为 1，没有重新生成或重复保存。

## 3. 验证证据

[检查索引](evidence/phase-4b/checks.json)、[实际 UI 记录](evidence/phase-4b/native-ui.json)、[只读账本](evidence/phase-4b/ledger-final-read-only.log)、[工作区审查](evidence/phase-4b/workspace-review.json)。由本任务完成源码及反向场景审查，未冒称独立人工或子代理批准。

| 检查 | 结果 |
|---|---|
| 原生定向回归 | 最终 FEAT-155 106 项通过，包含 SQL15 普通读取、私有读授权/回执、草案确认/恢复和无阶段严格识别。使用临时合成 SQLCipher 库，无真实模型调用。 |
| 前端定向回归 | 最终 15 个文件、264 项通过，覆盖普通 composer/store/client、用途契约、预填保护、同请求查证、澄清新轮次、唯一确认和管理页面。 |
| Host | 3 项定向 race 检查及 scoped vet 通过；固定 Runtime + 本机声明式 Provider 验证旧配置正常恢复、canonical 指引、outputSchema、tools=[]、tool_choice=none 和计数通道。与真实 Provider 证据分开记录。 |
| 契约与构建 | 33 组实际 native 请求/响应、25 命令的严格 AJV/native/TS 一致性通过；同源生成、lint/类型、Rust fmt/clippy、canonical packaged 构建及设计文档构建通过。 |
| 真实原生 UI | 预填不发送；未发送输入默认保留；受限模式无附件/目录/普通权限控件；亮暗主题、1180×760、键盘焦点；脏表单默认继续编辑；真实澄清/候选/暂停保存、管理同 ID、正常重开均已观察。 |
| 真实账本 | SQL23；保留 4A 旧墓碑，新增 1 个暂停计划；1 个草案会话、4 turn/source、5 个已完成 outbox（1 create+4 turn）；grant/run=0。重开前后记录数不变，执行记录 UI 为空，Provider 仍为 4 次。 |
| 元仓文档 | strict D0、lint、50 项治理测试及链接检查通过。文档检查不等于完整产品 D4。 |

早期验证中的实际问题如实保留：一次 Vitest 路径匹配意外包含 `.local` 旧工作树，改用当前源码及排除目录；私有 command allowlist/顺序和测试等待选中会话就绪已修正。第一版本本机 Runtime 组合缺少临时 home 目录、无阶段 UI 测试未展开折叠项/缺少 position，修正测试装配后通过，未修改断言伪造结果。

原 `ChatPage.test.ts` 的 3 个显示断言仍失败，与 33 报告中已用起点源码复现的失败一致；本批没有修改无关旧显示语义，也未宣称全量 suite 通过。Vite 的大 chunk 警告保留。Runtime 的 `itemsComplete=false` 仍显示历史内容不完整，不能伪造完整清单；草案来源校验直接读取完整 native item，不依赖展示截断。真实 Provider 本次覆盖 daily/dedicated_chat，其他频率/目标由原生与表单定向检查覆盖，不冒称全部真实组合通过。

## 4. 停止边界

应用、Host、Runtime 通过正常退出完成清理，计数服务正常停止；没有强杀、权限破坏、攻击 fixture、日常库写入或受保护二进制替换。保留隔离候选库中的合成暂停计划供查阅。

**4B 已完成并停止。** 不接计划启用、手动/自动运行、重跑、唤醒或通知，不提交/推送/发布。FEAT-155 总目标和十项 Must 保持；余下执行控制、完整历史、电源/应用内更新及最终验收由后续单独安排。
