# FEAT-134 原生展示实施与来源记录

日期：2026-09-09。来源已固定，canonical既有数据验收完成；最终结果见02-verification.md。

## 开始来源

五仓主工作区均干净，分支均为 chore/retirement-baseline-20260905，origin 均为 https://github.com/36Dge/对应仓库.git。

| 仓库 | HEAD |
|---|---|
| 元仓 | 33fd84c9acea2c91a2d2af2a96b8fb8625fad46c |
| Contracts | e63aafbcb3e2f4fabf0064feec48e7eece3d7046 |
| Host | 26ee8a12f737bb258c717a41d829e8ea706197fe |
| Desktop | c0dd70c240d48c2c16d046aa27c9b32ec4d32c5b |
| Codex（只读） | 6c1ad767f0997845b8258a1c452fd4eb7577579f |

两端 native 锁固定 Contracts 6f632f155eacdaf93df0e0b00b5dab9e369c5442；Desktop FEAT-152 固定 Host 9e9d317f7e4ecff5f8aeec94fa467f9bede32139。native 源摘要 ad4c7f0eece6acb99029358a8284535757ee5d7c97858d65b8813631f56ad651；Runtime schema tree 82ee9de771cf1d41bac16d87380f1121e7794107aa3aa526ad702d5d1bf7afe1。完整 digest 继续以已有 native-conversation.lock.json/runtime-permissions.lock.json 为准，不重新手写锁。

保留 Runtime 来源 b2b20e2fc4a0c94834f34d8cc459e488a1b56277，版本0.144.6；binary SHA-256 4efe16d2848680752cf9aacf4c17741ab2eeb7415894a66c2bb03652b00a322d，manifest SHA-256 1cfa2e0a139b2213f4d29b1efeed71d4810110ac865f0bcbd931ff33b0062c1b。不重建、升级或替换 Runtime。

## 原生复用与变更范围

Runtime notifications → Host service/native_conversation → v7 → Desktop stream_native_conversation → NativeDisplayBuffer → SQLCipher native facts/view → 完整 private view → readonly conversation-view/timeline。历史使用 Host ReadThread(includeTurns=true)；不复制 Runtime builder。当前 native buffer 的初始 availability=partial 是历史/集合完整性边界，不能单凭这个值认定执行停止；UI busy 还必须有有效实时订阅、原生 inProgress、Item可用且没有明确缺失诊断。

contract-impact=none：原生 wire、private schema、持久化结构、执行及权限语义不变；summary/content 和 availability/diagnostic 已存在。本次为进程内展示与旧无调用代码、测试、文档和构建来源配置调整。

## 删除清单

- Desktop TurnProjectionSink/IPC 的无调用 publish_feat134、publish_feat136。
- 仅服务于上述发布器的 feat134_subscription_matches、feat134_source_event_envelope；旧发布继承测试改为保留 v5 envelope 的来源验证。
- Feat134Projection::legacy_reasoning 及仅被它调用的状态转换。
- Host maxV4RememberedAgentPhases/maxV4ReasoningItemsPerTurn 两项无人调用常量。
- Host assertFEAT134MalformedTerminalLegacyEvents/assertFEAT134ReasoningLegacyCount 两个无人调用辅助函数。

保留 v4/v5 路由、历史 DTO/IPC/表、历史内容转换、reasoning 原生 completed→旧 finalized 的单向兼容，以及 Artifact、Command、FEAT-152 依赖。保留 FEAT-134/136 local-only high/raw/config gate。不整包删除，不恢复 FEAT-137。

## 展示修复

- summary/content 分类别映射原生 segment index，DOM标识包含类别，插入摘要不更换正文DOM。
- 只有有效订阅的原生视图事件能记录 UI live Turn；读历史不建立，离开 streaming/清除选择即撤销。不会写入数据库或影响发送/权限语义。
- Turn 结束后未 completed 的 Item 保持原生事实，显示缺结束记录并关闭 busy/aria-busy。
- Item availability 原值显示；诊断白名单映射安全文案。当前私有 view 没有范围字段，诊断保守按会话展示，不猜测 Turn/Item 归属，未知原始代码不进入显示模型。

## CI、检查与停止点

Desktop CI 原先旧 C/H 来源缺少 native 脚本且采用嵌套路径。现改为真实兄弟检出、固定源码引用、完整 Git 对象、冻结 Contracts/Skills 依赖及现有 local/demo_fast 配置；原校验命令保留。不声明远端CI已运行。

首次完整 generate:check 因 Contracts 文档仍未提交返回“contracts checkout has tracked changes”。Host 的 FEAT-152 门禁进一步覆盖 cmd/internal 全部构建输入，包括测试文件；因此不能只改16个显式文件摘要或跳过测试路径来继续启动。须在差异核验后取得本次本地提交授权，固定真实 Host 提交及消费者 pin；不借用已完成推送任务的授权。

## 验收和调用台账

原 FEAT-134 2026-08-29 D4 与10/11历史台账完整归档。FEAT-132最终台账为19/25文本、1/3图片，仅原需求历史记录；两份ledger已读取，本轮无转用。本次新增模型调用0，图片0，无自动重试或额外预算。

本次正常入口验证已使用普通com.yijie.ai既有app-data与原.local/demo-fast Host Home完成；详见本次机器证据。旧清理失败、附件过期、隔离会话无Host映射等状态保留真实结果。

## 提交前审查结果

实施与自审分开进行，未发现新的阻断实现问题。源协议/数据库/Runtime均未修改，原生最终对象及执行结果仍由既有机制决定。最新验证：前端233项、Host9项、Native/SQLCipher8项及另1项跨仓集成通过，lint/build/clippy/fmt/docs及元仓50项/D0通过。详细命令集合见feature.yaml及02-verification.md。

待授权本地提交的明确范围：Contracts仅历史适用说明；Host仅无调用常量清理和三项语义测试修订/旧辅助删除；Desktop展示修复、已核实无调用发布残留、CI配置及说明；元仓需求/历史归档/本轮验收记录。随后按真实Host提交更新FEAT-152消费者锁并重验全部来源，不修改权限语义。canonical结果只能在该步骤完成后填写。


## 最终来源与关闭范围

| 仓库 | 本地提交 | 作用 |
|---|---|---|
| Contracts | db7a607c1c091fc4f4243829d68d5b673eb7e2c3 | 旧v4历史适用说明 |
| Host | f4cf01bd6f7e9f37792ef743d44f0ce10527c10b | 无调用常量清理、测试与辅助函数修订 |
| Desktop | 6e5047d1c23041c46dd495ddb89e24c7e4db5d47 | 原生展示修复、旧发布残留清理、CI来源及真实Host pin |

Contracts native源仍固定6f632f155eacdaf93df0e0b00b5dab9e369c5442，因为本轮仅文档变化。Host16个显式来源摘要未变，但全构建输入校验包含本轮测试/常量变化，因此消费者full_commit依法更新为f4cf01b…，没有删减检查或伪造digest。原v4/Skills各自历史锁保持其独立范围。CI配置引用真实本地提交；本轮未推送，远端无法据此视为已验证，不能声明远端CI/可合并/发布通过。

本次八项AC和local D4仅覆盖任务授权的展示调整与canonical现有数据闭环，无新模型Turn。原运行缺口、FEAT-137永久退役、FEAT-152权限语义及历史额度均保留。新证据：[canonical记录](evidence/native-adjustment-canonical-2026-09-09.json)。
