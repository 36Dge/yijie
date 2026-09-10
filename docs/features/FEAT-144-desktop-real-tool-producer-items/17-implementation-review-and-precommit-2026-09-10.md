# FEAT-144 候选实现审查与提交准备

2026-09-10。当前完成源契约、兼容reader候选、Host原生薄适配和Desktop展示的实施及定向核验。**尚未本地提交、固定新来源、启动canonical或运行真实D4**。本次为实施后的分离阶段自审及独立源码快照验证，不冒称独立人工批准。活动9项AC保持pending；AC-004始终为用户排除，不实现、不验证、不计PASS。

## 实际复用与边界

- Codex 0.144.6：原生MCP连接/发现/工具执行、Prompt elicitation、thread/start/resume/read、原生Item/Turn与正常进程退出。Runtime源码、版本和保留二进制均不修改。
- FEAT-132：唯一NativeDisplayBuffer、已有原生历史入口、SQLCipher、scope及原子保存。facts仍不回放，不新增历史构建器。
- FEAT-152：现有permissionPolicy、审批回调和实际响应写入确认。新增MCP请求显示，不改变ask/auto/full含义，不恢复FEAT-137。
- 安全投影：复用完整文本脱敏、UTF-8截断、现有1 MiB传输与4 MiB视图上限。JSON转义导致传输超限时进一步缩减显示文本，保留原生身份/状态和内容索引，不把projection问题写成执行失败。

新源规范为native-conversation-v2（native-thread v2、SSE v8）和runtime-permissions-v2。旧源schema保持原样；旧v7/v1出口删除新扩展后继续提供旧语义。`resultSummary`仍是结果接收元数据，业务文本仅在新MCP扩展中。

## 删除与保留

移除新Tool链路中的startedSource、空时间/序号、未知identity、空progress/error等旧DTO伪填；移除容量超限时恢复旧Item/弹掉新Item的分支。不删除仍有消费者的v4/v5/v7协议、DTO、IPC、历史表、安全helper或旧Tool renderer。旧Tool renderer改为遵守可信busy，不把历史in_progress播报成持续执行。

Native Tool卡片直接引用原生Item，显示安全server/tool、实际参数、文本原始索引、空与缺失、availability/诊断及来源；纯文本、链接不激活，复制只复制已有安全文本。Turn结束不封口Item，也不继续显示busy。

## 审查发现与处理

1. 旧规范相对引用在breaking脚本单文件临时副本中失效：改为使用完整baseline OpenAPI目录，三组baseline重跑通过，不跳过比较。
2. 参数availability误改空结果分类：改为独立判定结果内容，合法空列表不被参数警告变成unsupported。
3. JSON转义可突破传输限制：按最终序列化大小缩减当次文本，保留完成对象的原生头部；未新增累积器。
4. 原生reload确认不能证明旧连接停用：使用实际idle、正常EOF、transport清理和来源验证后的重启；有活跃Turn或待决审批则拒绝切换。已有FEAT-152整体Host源码校验继续保留。
5. 稳定Prompt与记住审批边界：显式启用现有稳定tool_call_mcp_elicitation，严格使用Prompt的无persist表单；不自行解释记住批准、未知表单或关联Item。
6. 诊断代理与产品子进程环境不一致：标准入口读取当前系统HTTPS代理，经明确白名单传递；不固定本机地址、不新建代理，MiniMax和loopback路径保持原状。PAC/SOCKS未验证时停止该入口。

## 本轮真实检查结果

| 检查 | 结果与适用范围 |
|---|---|
| Contracts新版本测试 | 3项通过，旧规范字节与新文本/审批边界分别核验 |
| 完整安全生成检查、lint | 57份生成物一致；lint通过；保留2个NativeEvent未引用警告 |
| 三组breaking baseline | db7a607c、f16a497e、6f632f15均通过OpenAPI/AsyncAPI/JSON Schema/protobuf适用检查 |
| Host定向及race | 原生配置/目录schema、实际Prompt、响应写入、旧出口、新HTTP权限边界、文本/容量与原生身份核验通过；没有调用真实服务 |
| Desktop当前Rust | cargo check通过；4项FEAT-144格式/worker/容量测试通过；既有正常重开和前向迁移定向回归通过 |
| Vue/TypeScript | 类型检查、定向lint及33项当前Native显示/IPC/审批测试通过；旧Tool状态定向5项通过，另4项未运行，不声称全文件通过 |
| reader独立源快照 | writer保持1；生成、同一已安装vue-tsc及3项格式测试通过。没有复制用户数据库或凭据 |
| 固定Runtime本地配置解析 | 相同生成配置由0.144.6本地features list成功解析；未提供凭据、未创建MCP客户端或模型Turn，不代替产品验收 |
| 当前源检查 | 新MCP候选来源检查通过；正式committed来源尚未更新，canonical不能用候选绕过 |
| 文档与D0 | 本轮strict、D0与元仓lint已通过；历史诊断/验收结果不继承为本次D4 |

隔离reader最初的pnpm exec试图自动核对依赖并因无TTY停止，未允许清理node_modules；随后直接调用同一已安装的vue-tsc完成验证。保留该准备阶段失败，不把它计为产品缺陷或假造首次成功。

reader候选为`.local/feat144-reader-checkpoint/manifest.json`中的Git blob清单，仍需真实提交才能成为最低回滚基线。其保证格式识别、只读可访问及旧JSON保留，不保证最终Native Tool界面的全部功能。验证记录见[evidence/implementation-checks-2026-09-10.json](evidence/implementation-checks-2026-09-10.json)。

## 提交与真实验收准备

取得本次本地提交授权后按Contracts→Host→Desktop兼容reader→Desktop最终writer/展示→元仓固定来源。Contracts生成入口变更触及现有FEAT-132/152来源摘要，因此更新这些真实摘要和消费者pin；不修改旧权限schema语义、不机械更新无影响的旧锁。每次提交前比对已核验文件SHA保护新增并发修改。仅本地提交，推送仍未授权。

当前预算：业务0/10（含原生重发），元数据8/10，模型/图片均未授权。建议另授权最多8次MiniMax-M3文本API请求，包括正常自动请求/重试；不申请图片。真实验证限定一个新验证线程，初始化/目录核验各使用一次剩余元数据操作，随后同线程完成成功与Prompt正常拒绝。退出重开只读已有数据，不再次启用Sorftime。调用编排详见[16](16-native-implementation-2026-09-10.md)。

真实启动时密钥由用户在系统隐藏输入框输入。任何活跃Turn不能正常结束、来源未通过、有效权限/注册无法确认、余额授权次数到限或数据兼容不明确，均停止对应真实步骤。普通业务失败场景保持排除；原生Prompt拒绝仅作为权限回归。

仍未证明：正常产品接入与业务结果、实际模式切换后的停用、canonical读旧历史/附件/Artifact/Command、真实退出重开，以及light/dark、指定尺寸、200%和键盘/复制的实际UI表现。既有附件过期、冷历史/phase/progress缺失、Command最终输出策略等限制继续如实保留。


## 本次授权补充

用户已明确授权本次 Contracts → Host → Desktop 兼容 reader → Desktop 最终展示/写入 → 元仓的本地提交及同范围必要修复，并单独授权最多 8 次 MiniMax-M3 文本 API 请求（含实际转发的自动请求、重试及审查）。推送、tag、部署未授权。当前累计业务 0/10、元数据 8/10、模型 0/8、图片 0；该授权更新覆盖上文等待授权的阶段状态，不改变既有测试或 D4 结论。详见 [授权与预算](evidence/delivery-authorization-and-budget-2026-09-10.json)。
