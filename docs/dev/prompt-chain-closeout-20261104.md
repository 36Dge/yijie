# 提示词链路复审后的收尾

后续更正：Owner 已明确改为默认支持原生显式和隐式调用、按需加载。本文中
仅显式/关闭目录的内容是此前验收的历史状态，当前要求与实现见
[原生技能发现恢复](native-skill-discovery-20261104.md)，不再将目录关闭作为验收目标。

2026-11-04，Owner 要求复核收尾方案并开始执行。沿用今天最终决定：必须复用
yijie-codex、仅明确选择/点名技能、完整聊天能力、无轻量模式、保留 UI 与历史。
这是既有修复的验收及检查工具补齐，不扩展新产品功能。

`contract-impact = none`：本轮计划只改变检查脚本、测试及交付说明；不改变产品
wire、生成 SDK、Runtime、持久格式、权限、预算、提示词或默认行为。若连续验证
发现产品缺陷，先记录具体证据及重新分类，再修复相应实现。

## 复核后的取舍

- 专家跨模型增长来自原生 `context_manager/updates.rs` 的 model_switch 历史；
  旧 developer 指令和技能目录也按原生历史语义保留。不要在 Host 过滤历史，
  不改 Runtime 核心，不静默触发付费压缩或更改全局阈值。
- 原生 `thread/compact/start`、自动压缩、`skills.include_instructions`、
  `UserInput::Skill`、`skills/list` 和配置热刷新已有实现。收尾验证这些原生路径，
  包括压缩后是否回到当前规则、保留普通对话信息；不另造摘要或技能加载器。
- 复用现有 Host→Native 跨语言回环和 Vue 页面测试，将真实页面产生的输入贯通
  到 Native 存储、Host 安装/版本核验和固定 Runtime。测试替代的是本机 IPC
  驱动及供应商响应；Native 授权 facade 和后台 coordinator 不在本次驱动内，
  仍由既有分层测试覆盖。不冒称真实 macOS WebView 或完整 App E2E/模型质量验收。
- 兼容性检查复用现有 oasdiff 投影和 JSON Schema 比较器，自动发现 OpenAPI
  源并纳入 compatibility 的 schema；增加正常旧请求字段删除的回归。
  旧候选之间已发生的不兼容要真实报错，不使用忽略清单让检查变绿。

## 实施及验收顺序

| 顺序 | 实施 | 可判定结果 |
| --- | --- | --- |
| 1 | 扩展已有兼容性检查 | 当前对当前无差异；漏检的协议全部列入；正常字段收紧/删除可被检出；各侧仅使用自己的来源 |
| 2 | 技能连续回环 | 页面选择的 ID/版本与 Native 重开后相同；真实 Host 验证安装；实际 Runtime 输入正文恰好一份；已接受操作重放不多发模型请求 |
| 3 | 上下文矩阵 | 普通/专家新建及恢复、专家跨模型及取消、旧会话恢复和原生压缩均捕获实际请求；区分当前规则与历史副本 |
| 4 | 复审与交付 | 相关检查通过；21 个既有 UI 文件保持；Runtime 身份不变；记录请求数、未执行项和限制 |

最小路径是“补已有门禁和测试”；不重建功能包、模式、数据库或预算体系。
只使用普通合成内容、独立临时目录和 loopback，正常 EOF/HTTP shutdown/worker
退出。无攻击 fixture、权限故障、强杀或可执行文件伪装。日常客户端与数据库不需
因测试变更重新构建或迁移。

真实供应商的调用次数、费用和答案质量仍需任务级明确额度；本轮先完成可独立
执行的零费用验证，不借用其它需求的历史额度。真实原生窗口验收与真实供应商
验收分别记录，不由回环结果自动推定。

## 执行记录

开始状态保存在工作区 `.local/diagnostics/2026-11-04-prompt-chain-closeout/`。
Contracts 64ed36d、Host d6f6bf5、Desktop e6a9522、Runtime 55b4e51；Desktop
21 项原有改动已逐文件记录 SHA-256，其余相关仓库起始干净。

### 已完成的核心验证

1. `TestPromptSelectedSkillBoundary` 使用既有跨语言驱动。真实 Vue 技能菜单点选、
   文本框发送、ChatPage、store、chatModelClient 生成的同一份 IPC 请求交给生产
   Rust decoder；实际 SQLCipher repository 保存，HostBridge 发送给真实 Host
   handler/session/安装服务，最后由固定 Runtime 读取受管技能正文。普通模型技能
   只使用既有正常 ZIP；错误版本被拒；正文一份；正常重开后原 ID/版本保持；
   Native 创建操作与 Host 已接受操作重放不增加模型请求。单次用例仅 1 个本机
   Responses 请求，供应商请求 0。该用例及原跨语言用例的 race 检查通过。
2. `TestPromptExpertSwitchHistoryAndNativeCompaction` 捕获专家新建、同模型恢复、
   切换 MiniMax、切回 Kimi，角色份数依次 1/1/2/3，业务基线一直一份。调用已有
   原生 compact 后下一轮角色回到一份，取消后零份。此前普通笔记仍在上下文中；
   验证后的新问题没有重新携带笔记。该用例 7 个本机请求。
3. `TestPromptLegacyResumeAndNativeCompaction` 证明 resume 保留旧 developer 和
   目录，原生 compact 后下一轮改用当前规则、关闭目录并保留普通笔记。该用例
   4 个本机请求。使用普通历史标记和正常摘要响应，未修改既有 rollout。
4. 原生启停热刷新仍保持线程与共享预算，已接受技能操作仍按原回执重放；相关
   Host race 回归通过。模拟用量不用于证明实际 token、人民币费用或摘要质量。

### 兼容性检查结果的正确解释

原固定 11 个 OpenAPI 入口改为来源自动发现，当前覆盖 18 个；JSON Schema
比较复用原比较器，覆盖 jsonschema 和 compatibility 的共 42 个 schema。
历史 FEAT-164 检查脚本退为同一共享入口的薄转调，删除重复解析实现。
复审报告中“市场/专家 v2 OpenAPI 未列入”表述不够准确：chat-models-v2 属于
OpenAPI，市场和专家的私有 wire 属于 compatibility；现在两种遗漏均有覆盖。

| 比较 | 结果 | 含义 |
| --- | --- | --- |
| 当前 64ed36d → 当前工作树 | PASS | 本轮没有产品契约差异，18 个 OpenAPI 与 42 个 schema 均覆盖 |
| 已发布 f16a497 → 当前 | PASS | 已发布基线的结构检查保持通过，不等于全部行为兼容 |
| P1 前 dfd9012 → 当前 | REVIEW：两个 `$ref` 迁移 | 保守比较器如实报告 TextInput 权威源变更；新增同源测试证明旧文本约束、required、additionalProperties、UTF-8 边界保持，只新增可选 skills，不增加全局忽略规则 |
| 已撤回 ccf8930 → 当前 | FAIL（预期） | 检出 toolProfile 属性与定义删除，证明撤回确有不兼容；不恢复该功能，不把红灯改成绿灯 |

20 个检查器测试、4 个原生复用/技能身份/撤回符合性测试通过。新增 API 会校验
来源闭合，旧 API 删除会报错；每侧只从自己的树读取，未下载 schema URI。
上述都是结构与同源证明，不冒充 Owner 对生产兼容的人工批准。

### 验证范围及最终状态

Desktop lint、构建、候选 Clippy 及修正 test-only cfg 后的默认 Clippy 已通过。
前端安全回归 2113 项先通过，5 项来源检查因当前 Contracts 存在本轮未提交脚本而
失败；使用已有干净 Git 来源目录核验锁定对象后复测通过。其中 v4 测试的负例
曾绕过显式来源目录，已仅修正测试参数。Node 路由 27 项通过。未降低 clean-source
校验、未改 pin、未为通过检查提交或切换用户工作树。原始失败日志保留。
原生完整安全回归最终为默认配置 626 passed / 14 ignored、当前候选 663 passed /
16 ignored；两个配置均 0 failed、27 filtered out，执行器退出 0。沿既有安全
排除清单跳过禁止的测试，不把 skipped/ignored 写成通过。默认回归编译曾出现
测试辅助函数的 unused 警告，随后按同一候选 feature 限定 cfg；最终默认 Clippy
通过，候选完整回归从修正后的源码编译。fmt、限定 ESLint、Host vet 通过；元仓
manifest lint 与 57 项治理测试通过。全部本机测试进程已正常结束。

本轮新增的运行代码只有开发检查工具；Host/Desktop 产品行为不变，无新命令、
Schema、权限、功能开关、模式、预算计数器或提示词重写。无需重启/替换日常客户端。
21 个原 UI 文件 SHA 保持；Runtime commit 和二进制 SHA 保持 55b4e51 / 50d89e15…。
日常数据库没有打开、迁移或写入；没有调用真实供应商。

本次收尾共涉及元仓 2 个、Contracts 8 个、Host 3 个、Desktop 4 个文件，均为
检查工具、测试或说明；Runtime 仓零改动。未新增分支、提交、推送或 tag。
用户可直接审阅当前工作树差异；消费者继续使用原已固定的产品来源。

机器结果：`verification.json`、`breaking-matrix.json`、`preservation-check.json`、
`source-diff-receipt.json`；核心日志为 `skill-boundary-race.log`、
`context-matrix-final.log`、`host-focused-race.log`、`native-safe-tests.log`。
旧的首次失败日志、来源保护失败及修正后的复测日志均保留，不改写为首次全绿。

真实 macOS WebView 的 IPC/Native 授权 facade/后台 coordinator 全链与付费供应商
效果不在此次 headless 证据内，状态仍为 NOT RUN。若需要证明真实 Kimi 的回答、
请求次数和费用，后续按明确任务级额度使用既有入口验证；不能把本轮回环称为
完整 App D4，也不自动压缩用户的旧聊天。本轮验证补齐的是原生能力边界和同一
提交的跨层数据传递，原生自动压缩阈值、完整工具面与历史保存策略保持。
