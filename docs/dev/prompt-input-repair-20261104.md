# 提示词链路 P1 整改与本机接入

2026-11-04。Owner 要求复审并实施原生复用方案，优先 P1，保留原 UI 与历史；随后
明确选择仅显式选择/点名加载技能。沿本次修复的本地提交授权固定来源，不推送、
不打 tag。当前原固定开发入口已成功启动，Host/Runtime ready。

整体 `contract-impact = breaking`：新增 text.skills 请求字段是 additive，提示词
装配是 semantic，最高影响来自 Desktop 私有 SQL 43 的前向 reader guard。
Runtime wire、二进制和预算机制不变；公共身份源是 Contracts Agent Host OpenAPI，
Desktop/Host 消费同源生成物。Owner 的本次实施指令确认个人本机范围，不冒充生产
版本、外部 Consumer 审批或真实供应商效果验收。

## 已修复及原生复用

1. Host 原来用仅包含 projects 的影子结构校验原生用户配置，误拒
   `skills/config/write` 自己写出的 skills.config。现在直接校验固定 Runtime 的
   canonical config schema，仅保留 Host 必要的配置所有权与路径约束。
2. Desktop 原来把选择降为 `$name`，同名时丢失准确身份。现在在原文本提交事务
   保存 `{id,version}`；Host 复用目录/安装回执及原生 `skills/list`，解析精确路径
   后发送 `UserInput::Skill`。不接收 renderer 自报路径，不读取/拼接技能正文。
   已接受操作按原持久索引重放，不因后来卸载而再次分派；新操作才验证安装状态。
3. 专家路径原来在 base/developer 各注入一份 6161 字符业务基线；现在只在 developer
   保留一份，base 保留短规则和专家 role/index。取消专家用短的当前角色说明，
   不删历史、不另建提示词引擎。
4. 通过原生 `skills.include_instructions=false` 去掉常驻目录，保留原生显式点名
   与准确选择加载。个人目录/文件保持。旧历史中已经存在的目录不被重写。
5. 技能启停后使用原生 `config/batchWrite` 的空 edits 与 reloadUserConfig，更新
   已加载线程配置。测试证明线程和原生预算保持，没有新配置缓存或预算计数器。

另完成两项 P2：检索能力说明改为供应商无关规则，当前工具定义优先于旧能力描述；
草案文本中的 canonical schema 仅用标准 JSON 排版压紧，原生 outputSchema 和
input-only 保持。标题入口仍关闭，修正其“原生不能禁用工具”的过时错误原因。

## 请求测量与验证

同一固定 Runtime、正式 Host 适配器、本机普通回环的请求对比：

| 场景 | 修复前文本字符 | 修复后文本字符 | 减少 |
| --- | ---: | ---: | ---: |
| 普通新对话 | 20136 | 12802 | 7334 |
| 专家新对话 | 26124 | 13031 | 13093 |
| 计划草案 | 6491 | 3557 | 2934 |

这是实际请求文本以换行连接后的 Unicode 字符数，不是供应商 tokenizer 的 token
或费用比例。普通工具 schema 20064 字符保持原值。13 个请求场景涵盖普通续轮、
加载后恢复、Kimi→MiniMax→Kimi、专家冷恢复/移除、显式技能与草案；相关聊天中
共享规则一份、目录零份，稳定检索规则一份。草案 fallback 解析结果与原生 schema
完全相同，工具仍为空。

- Contracts 全量安全生成、lint、42 项相关检查、Rust 6 项检查，以及 10 个既有/
  发布/fallback 基线的 breaking 检查通过；fallback 为 dfd9012954c716d360f702d6be3bdbdef75e0633。
- Host vet、契约检查、受管身份/重放的 race 检查通过。固定 Runtime 正常技能
  停用→EOF→重启保持配置；同名 A/B 仅选择 A，启用热重载后继续共享预算并原生到额失败。
- 前端完整安全路由回归 2117 项通过，1 项旧来源引用失败修正后所属 5 项全过；
  node:test 27 项通过。原有 20 项跳过保持。lint、构建及文档构建通过。
- Native 普通配置 626 项通过、14 ignored；当前候选 661 项通过、16 ignored，
  1 项写死 SQL 41 的断言更新为当前 reader 版本后精确复测通过。两个配置各排除
  27 个匹配安全过滤的测试。新增 SQL 43 选择持久化/正常重开/旧摘要保持通过。
  fmt、默认及当前候选 Clippy 通过。完整旧失败日志保留，不伪装成首次全绿。

所有攻击 fixture、权限破坏、可执行文件替换和强杀测试均未执行；没有付费模型
请求。上述回环证明适配和输入控制，不声称证明 Kimi 回答质量或真实费用下降比例。
HMR Native 窗口未被桌面自动化识别，未执行完整视觉点选/亮暗/最小窗口验收。

## 实际接入与数据保留

用户通过菜单/⌘Q正常退出后，仅为 SQL 43 迁移保存原加密会话库的定点副本，
没有全量数据备份。固定入口第一次因权限投影仍引用旧 Contracts 而停止；通过
现有同步器更新共享 OpenAPI/生成物并固定提交后重开，未降低来源检查。

原固定入口 `~/Applications/易界.app` 启动成功，Native 增量编译 33.40 秒。
实际 Host build revision 为 b2f4a4fe869decbed3c828be70caa7f9320aa3b4，`/readyz`
返回 200、runtime_state=ready；实际 renderer 结构化技能输入开关为 true。
Runtime 实际 SHA-256 为 50d89e152c90e660331326506d372b986acd0279324376cb77385959698219d7。

只读数据库核验 SQL 41→43，旧 3 会话、12 消息、6 内容块、6 轮、111 原生事实、
6 视图、3 模型选择和专家绑定表的所有原行摘要完全相同；新增技能选择表为空。
原 3 份 rollout 前缀摘要相同，没有新增 task_started/token_count。21 个已有 UI
改动文件逐字节保持且未混入本次提交。客户端保持运行；常规启动恢复既有连接器
就绪检查，不自动发送新聊天。

## 不可变来源、回退与剩余范围

| 仓库/表面 | 完整引用 |
| --- | --- |
| Runtime（未改） | 55b4e51049d6f4fc0af4b35f12832357f5e4ea06 |
| Contracts 原生/模型/权限投影 | 633aa9eee300a3123c1574306234682059f557ec |
| Contracts 最后生成锁提交 | 6aa170b649a773961b211c6bda2099d748740624 |
| Host 公共 API 输入 | 358a4642df9c8be15aea55b08589045669ffefc4 |
| Host 最终实现/投影 | b2f4a4fe869decbed3c828be70caa7f9320aa3b4 |
| Connectors（仅生成来源元数据） | d36d898994384b570530e68e1a0d7f9fd7f44e3c |
| Desktop | 0c78728bdb489a879f7e47d99a8925d7c96057c6 |

依赖顺序是 Contracts→Host→Native SQL 43→renderer 开关。回退可关闭新 renderer
输入，但新库必须保留 SQL 43 reader，不降版本号、不用旧包覆盖数据库、不自动恢复
旧副本；Runtime 无需回退。

剩余 P2 有明确边界：未创建“轻量用途”产品入口，不能按关键词自动关闭多代理或
Goals；未更改自动压缩阈值或自动触发付费压缩；未删减此前明确要求的检索、安全和
输出约束。P3 标题功能保持禁用。以上不被写成已经解决，进一步能力裁剪须先明确
用途和验证影响，并继续仅投影原生配置。

完整机器证据位于工作区 `.local/diagnostics/2026-11-04-prompt-chain-implementation/`：
`prompt-reduction-final.json`、`activation-verification.json`、`database-preservation-before.json`、
`database-preservation-after.json`、`breaking-results.json` 与各检查日志。加密数据库
恢复副本位于同目录 `database-before-sql43`，只在明确恢复任务下使用。
