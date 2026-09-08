# FEAT-132 原生机制调整：最终验收

2026-09-09，**D4 PASS，十项 Must AC 全部通过；仅限 local/demo_fast**。本次使用新的明确授权与真实结果，不继承旧 FEAT-132 的 D4。

## 固定来源与实际入口

| 仓库 | 本次最终完整 commit |
|---|---|
| Contracts | `6f632f155eacdaf93df0e0b00b5dab9e369c5442` |
| Host | `9e9d317f7e4ecff5f8aeec94fa467f9bede32139` |
| Desktop | `5e6ada73ed8b9d49dde51e4b6659ce5337304a6e` |

所有修改仅本地提交，未推送、打 tag 或部署。两端原生来源锁及 FEAT-152 commit/digest pin 校验通过；三个 D4 修复仅涉及 Desktop，公共 Contracts/Host 来源没有变化。

实际从 `.local/feat132-validation-20260909/yijie-desktop` 的精确提交 worktree 执行既有 `pnpm tauri:demo-fast:stable` 和 `pnpm tauri:demo-fast:app`。沿用同一份受核验 Runtime 0.144.6（保留产物来源 `b2b20e2fc4a0c94834f34d8cc459e488a1b56277`），通过现有绝对路径参数引用 Runtime 和 provider key；没有复制凭据或用户数据库。

旧应用经 ⌘Q 正常退出，Desktop/Host/Runtime 全部结束后启动验证构建；没有绕过全局单实例锁。stable 的 experimental_api=false；普通图片入口只启用 FEAT-128 既有 generate_image 例外。FEAT-137 的历史 SDK 漂移经标准安全生成对齐，仍永久退役。

## 十项 AC

| AC | 实际证据 | 结果 |
|---|---|---|
| AC-001 原生 ID、phase、状态、最终内容 | 真实 Host RPC/SSE 身份与终态；生成 DTO 跨仓传入 Native/SQLCipher；真实 UI 内容与重开一致。MiniMax 本轮未给 phase，界面保留未分类，不伪造 final_answer。 | PASS |
| AC-002 多 Item/segment 与去重 | 安全交错 delta、重复 cursor 定向测试；真实命令后台运行时切换会话不串写。 | PASS |
| AC-003 原生最终 Item 替换 delta | 正常 Host SSE fixture→Native 测试中 draft 被不同的原生最终内容整体替换；打包后的 AJV 真实执行回归通过。 | PASS |
| AC-004 Item/Turn 不互相补造结果 | 定向测试通过；真实命令已完成时 Turn 仍运行；原生中断后未完成 reasoning Item 仍保留进行中，不被客户端封口。 | PASS |
| AC-005 显示问题不伪造执行失败 | 投影/解析/容量定向测试通过；本次实际 WebView 错误未改写 Runtime completed，修复后未重发即可重读。 | PASS |
| AC-006 failed 不被冷历史覆盖 | 实际 SQLCipher 正常 close/reopen 与 Host→Native 集成，保存安全合成的原生 failed，再读取冲突的冷 completed，failed 保留。没有故意制造付费 Provider 失败。 | PASS |
| AC-007 原生集合来源不猜测混合 | 生成类型、集合来源/修订检查及定向测试；真实重启后保持 observed 集合，冷历史 item-N 不与实时 ID 按正文或位置混合。 | PASS |
| AC-008 数据和关联功能 | schema13→14 有内容数据库前向迁移测试；两个 canonical 应用身份的旧档案可读；真实 CSV/PNG、Artifact 预览/保存/重开、Command、Composer 与三种 FEAT-152 模式通过。 | PASS |
| AC-009 旧语义链路删除 | 生产边界扫描、删除清单、自审与来源门禁通过；没有旧 reducer/hydrate/reconcile/fallback 或换名语义引擎。 | PASS |
| AC-010 正常完整流程 | canonical 启动、发送、切换、正常按钮中断、正常退出/重启均通过；中断记录保持 interrupted，重启后继续会话返回 FEAT132_RESTART_OK。 | PASS |

AC-002/003/005/006 中需要精确制造协议组合的部分使用普通内存事件、正常 mock HTTP 和新建 SQLCipher 测试数据；这些不是额外真实模型请求。真实模型结果与定向测试分层记录，不混计。

## 真实场景与预算

- 文本、CSV/PNG：`FEAT132_NATIVE_OK`；CSV total=100，PNG 左红右蓝。普通命令产生 `FEAT132_COMMAND_OK`，原生退出码0。
- 请求批准：批准本次后产生 `FEAT132_APPROVED`；另一请求正常拒绝，rejected.txt 不存在且未重试。
- 帮我批准：原生审查后产生 `FEAT132_AUTO_REVIEW`，台账第12/13次是结构化原生审批审查请求。完全访问模式只写入指定的 `FEAT132_FULL_ACCESS` 文件。验证会话随后恢复请求批准；图片会话也恢复请求批准。
- 中断：`01a08216-156a-77c0-929e-c94f5151e0a2` 的 Runtime 原生状态为 interrupted，Host idle；正常重启及后续新 Turn 没有覆盖它。第一次修复前的长文本自然完成，明确不计为中断通过。
- Artifact：仅生成1张普通几何图片，真实预览与保存成功；正常退出后同入口重启仍可预览。JPEG 76380 bytes，SHA-256 `25319bafd736019f370cffef28fa01e0542dbcece2be415c7d08a383048e9005`。
- 视觉：1180×760 最小窗口，WebView 客户区1180×728、DPR2；亮/暗完整布局无重叠。暗色通过 WebKit 偏好模拟触发应用自身主题，独立诊断窗口下观察完整应用；随后恢复 System (Light) 并关闭诊断窗口。
- **实际共19/25次文本、1/3次图片**，没有追加自动额度。授权时间见用户消息元数据记录；仅提取本任务的授权文本与时间，不涉及产品 Runtime 历史重建。

应用、Host、Runtime 和计量代理均通过正常流程结束，18083/18085端口已释放。旧 FEAT-131 等待记录未删除、补发或伪造结束。

## 发现与修复

| Desktop 提交 | 问题与验证 |
|---|---|
| `17a680f783a9ab2b06e47109247d6e920368ef87` | AJV CommonJS helper 在浏览器打包后不是函数；修正生成入口并再生成。真实打包回归先失败、修复后通过，Unicode 长度门禁仍有效。 |
| `9c5eafd2c31ba65f2a4132a77c6f5aa668c7575f` | 历史接口把空 outbox 助手占位投影为空正文加空格内容块，阻断原生视图；略去无正文/内容块的 pending 占位，不改数据库或实际内容。历史回归及真实重读通过。 |
| `5e6ada73ed8b9d49dde51e4b6659ce5337304a6e` | SSE 长连接阻塞 outbox 分发；在流接收期间复用现有 dispatcher，中断请求不再改写原生执行状态。持有正常 SSE 的定向测试、真实中断与重启通过。 |

追加修复均完成 Clippy、适用定向回归与自审。初始重构已有独立只读审查；没有声称三个追加修复又经过第二次独立审查。原 Desktop 工作区另有3处并发 UI 修改，未覆盖或纳入本次提交。

最终完整 generate:check 通过。一次检查发现隔离 Contracts 的 node_modules 符号链接被严格 clean 检查识别为未跟踪文件；仅移除本任务创建的链接，按原 lockfile 离线安装依赖后复核通过，没有修改或放宽来源门禁。

元仓最终 `pnpm lint`、`pnpm test`（50/50）、`bash -n scripts/*.sh` 与需求包 D4 门禁通过；24 份本地证据的 SHA-256/字节数与版本化索引一致，台账及重启记录的版本化副本与本地原件一致。

## 保留的限制与未执行项

固定 Runtime 的冷历史仍缺少部分 delta、Command、plan、error，Item ID 也可能重建；显示“不完整”是明确的能力边界。未标阶段的消息保留未分类；现有动态图片工具调用本身显示为安全 unknown 内容，独立 Artifact 资源的预览/保存/重开可用。

隔离 Host 不拥有其他原 Host 的映射；这些旧档案可读，但权限同步可能提示不可用。本次没有冒称已迁移原 Host 的全部运行索引，也没有复制它们。

未执行强杀、binary 替换、权限破坏、攻击注入、危险 fixture 或含这些场景的广泛测试集。没有为原生 failed 验证故意制造 Provider 故障。签名、公证、发布和 public/production 验证不属于本次 local D4。

## 证据索引

- [机器可读最终记录](evidence/d4-2026-09-09.json)，含完整来源、AC证据类型、本地日志摘要。
- [文本台账](evidence/d4-text-request-ledger.json)、[图片台账](evidence/d4-image-request-ledger.json)、[授权时间](evidence/d4-user-authorization-times.json)。
- [重启后的原生历史状态](evidence/d4-final-restart-native-history.json)、[Artifact 保存摘要](evidence/d4-image-export.json)。
- [来源固定与推进记录](04-source-freeze-and-d4-2026-09-09.md)、[复用/删除/迁移/回滚清单](03-native-protocol-adjustment.md)。
- [2026-09-08 定向验证归档](history/2026-09-08/02-verification.md)、[原需求历史](history/2026-08-27/02-verification.md)。
