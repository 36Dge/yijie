# 恢复原生 Skills 显式、隐式与按需加载

2026-11-04，Owner 最新要求覆盖此前仅显式的选择。默认同时支持界面选择/点名与
模型根据任务描述选用；先提供名称、描述、路径，再按需读取 SKILL.md。

最高 `contract-impact = breaking`：聊天行为恢复为原生发现语义；受管模型目录启用
已有原生 `include_skills_usage_instructions` 字段，旧 Host 的精确字节 reader 会
拒绝新目录。权威分别为固定 yijie-codex 55b4e51 的 ModelInfo/加载实现与 Host
已有受管文件生成/升级边界。无新增 HTTP/IPC、Schema、数据库、命令、权限或
自定义 feature。Desktop 精确选择协议保持，Contracts 公共 wire/pin 为 N/A。
此变更由 Owner 当前明确指令授权；不是生产发布或供应商效果资格。

## 原生复用证据

- `codex-rs/core/src/config/mod.rs:3624`：`skills.include_instructions` 缺省 true。
- `codex-rs/core-skills/src/model.rs:28`：`allow_implicit_invocation` 缺省 true；
  原生过滤停用或明确禁止隐式的技能。
- `codex-rs/core-skills/src/render.rs:28`：目录为名称、描述及位置；原生使用说明
  同时涵盖点名和任务描述匹配，并要求决定使用后完整读取 SKILL.md。
- `codex-rs/core-skills/src/render.rs:160`：已有目录预算、描述裁剪和路径别名。
  不在 Host 另造省 token 算法。
- `codex-rs/core-skills/src/injection.rs:67`：只对已选择技能读取/注入正文；
  `:149` 起处理结构化选择、文本点名、路径消歧及同轮去重。
- 隐式选择由模型根据原生元数据判断，通过原生读文件/资源工具加载；本机文件
  调用跟踪也已有 `core-skills/src/invocation_utils.rs` 与 core tool handler。
- `codex-rs/protocol/src/openai_models.rs:377` 及
  `core/src/context/available_skills_instructions.rs:28`：已有模型字段控制是否随
  目录提供原生使用指南；Kimi/MiniMax 目录之前省略该字段，实际缺省 false。
  当前 v2 目录为两个受管模型启用 true，由原生生成触发/全文读取说明，Host 不抄写。

按需加载指模型上下文中的渐进提供；原生扫描器为了提取元数据可能读取源文件，
不将这种内部读取误称为已经把全部正文注入模型。

## 最小实现

删除 Host 的 `promptInputConfig` 及 start/resume 的两处调用，让原生配置决定目录
行为；删去短 base 中强制仅显式使用的句子，不追加另一套 Skill 指南。保留原生
技能级禁用、显式原生配置覆盖、UserInput::Skill、受管身份核验与原生热刷新。
专家与普通聊天共享当前规则；input-only 草案仍由原生策略隔离技能和工具。

v2 受管模型目录仅新增原生指南字段。沿既有 `preflightManagedFile` /
`applyManagedFile` 接受精确的旧目录字节并正常升级；旧 v1 配方、用户 config.toml、
凭据和模型/推理强度/上下文窗口/压缩阈值均保持。不允许任意目录漂移；不创建第二套
迁移器。旧 Host 不可直接复用新目录；回退需显式选定已核验旧目录与对应 Host，
不能关闭精确来源检查或删除历史。日常目录本轮尚未写入。

旧会话不重写：冷恢复采用当前 base/配置，但原生保留历史，不会立即补建先前
缺失的 Host 技能目录；已有原生压缩重建上下文后恢复目录。不会为了此更正自动
发起付费压缩或在 Host 插入目录副本。新建会话直接获得原生元数据目录。
原目录 token 缩减数字只适用于此前已撤销的仅显式策略，不能继续作为当前收益；
现在会恢复元数据成本，
完整技能正文仍按需提供。轻量模式保持撤回。

## 验证与限制

使用固定 Runtime、现有本机回环和普通只读 cat，不替换二进制、不破坏权限、
不引入攻击 fixture、不调用付费供应商。验证目录仅含元数据、隐式选择后读取正文、
结构化与文本同轮去重、纯文本点名、技能级隐式禁用和旧线程恢复；并回归启停热刷新、
原生预算、专家/压缩及此前连续技能输入链路。隐式选择由普通本机响应驱动，
证明已有读取通道，而非真实供应商的自主选择质量。

最终 12 个针对性 race 测试通过，包含：普通元数据目录与原生触发指南、隐式只读
加载、结构化/文字去重、纯文本点名、技能级 opt-out、旧线程原生压缩刷新、受限
草案 start/resume 不继承目录/正文/工具、配置热刷新预算保持、当前/旧模型目录
正规升级与重开，以及 Vue→Native存储→Host→Runtime 的连续技能输入回环。
Go vet、Host 正常开发构建、Desktop 文档构建和元仓 lint 通过。

首次旧会话断言错误地期待 resume 补建初始目录，后按源码和实际请求证明修正为
原生压缩刷新；旧 FEAT-155 metered 用例与当前 Runtime 身份不匹配，改用当前
Runtime 的真实 input-only 入口验证。当前原生空工具请求使用 tool_choice=auto，
没有因此放宽工具/技能隔离检查。所有原始失败日志均保留。

工作区证据在 `.local/diagnostics/2026-11-04-native-skill-discovery/`，最终日志
`final-verification.log`，记录 `verification.json`。本轮没有付费模型请求，未启动
日常客户端、未写日常模型目录或数据库、未提交/推送。Host 构建仅为该目录中的
正常开发候选，不替换日常输出或 Runtime；正常启动原固定开发入口时才会接入。

工作区已有收尾测试、公开进度提示词和 UI 改动均保留。公开进度测试中依赖旧
opt-in-only 规则的一项断言随当前决定调整，其余进度内容不改。
