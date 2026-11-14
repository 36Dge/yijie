# 装配、契约与迁移设计

状态：拟实施方案，未修改任何产品代码／配置。此文同时记录安装权威迁移的候选架构决定；接受后再同步正式 ADR 和各仓规则，不把旧 Accepted 文档直接改成已实施。

## 1. 来源、安装与运行分开

| 对象 | 权威／位置 | 生命周期 |
|---|---|---|
| 内置源 | App Resources 下原生本地 Marketplace；yijie-skills 构建生成 | App 升级替换可提供版本，用户卸载技能不删除它 |
| 个人源 | App Data 下的 yijie-user Marketplace 与受控导入副本 | 导入归一化后发布，卸载成功后移除源条目；用户原文件不动 |
| 安装缓存与启用意愿 | 易界专属 CODEX_HOME 的原生 PluginStore／config | 仅原生安装、卸载和配置接口写入 |
| 本轮技能可见性与加载 | 原生 skills/list、会话配置及 UserInput::Skill | 每轮原生快照、原生显式／隐式规则 |
| 产品映射与操作结果 | Host 私有导入／迁移索引、现有 operation journal | 保存稳定 ID、来源、摘要、映射和请求阶段，不成为第二套 installed/enabled 权威 |
| 工具依赖事实 | 原生 MCP 目录＋现有连接器启用／授权／准入事实 | 随实际配置变化；不用市场静态声明冒充就绪 |

建议资源布局（概念路径，运行时通过平台 API 解析）：

```text
App Resources/skill-marketplace/
  .agents/plugins/marketplace.json          # name=yijie-builtin
  plugins/<stable-plugin-name>/
    .codex-plugin/plugin.json
    skills/main/SKILL.md
    skills/main/references/ ...
  presentation.json                        # 分类排序/图标/中文展示与产品ID映射

App Data/skill-imports/
  .agents/plugins/marketplace.json          # name=yijie-user
  plugins/<generated-plugin-name>/...
  staging/<operation-id>/...

YiJie CODEX_HOME/plugins/cache/...          # 仅由原生管理，不由Host拼路径操作
```

每个插件必须恰好包含一个技能；内置 payload 保持原 Skill 内容与相对资源结构。产品展示索引与原生 manifest 从同一权威内容源生成，并做对应校验。展示索引不存安装状态，不另复制 native interface 已有字段为独立可编辑真相。

普通技能不再以 ZIP 作为运行安装器的输入；构建时将已审资源生成上述原生目录，随 App 打包。源文件内容摘要／许可仍属于发布校验。个人 ZIP 只在导入边界展开为本地目录，最终安装同样交给 PluginStore。

## 2. 原生接口接线

| 用户动作 | Host 适配 | 原生调用与确认 |
|---|---|---|
| 浏览 | 只认两个准入市场及明确产品 ID | plugin/list 指定 local；未安装列表不调用 install；状态来源为原生 |
| 预检导入 | 创建尚未向 UI 发布的受控条目 | plugin/read 解析 source，要求恰好一个合法 Skill；不注入模型 |
| 添加 | 稳定 ID 解析本地 marketplacePath/pluginName | plugin/install → 原生回读 → skills/list(forceReload) |
| 启停 | 仅允许目标插件启用字段，不代理任意 config 编辑 | config/batchWrite 写 plugins.<id>.enabled 并 reloadUserConfig；回读实际状态 |
| 卸载 | 先限制新的提交并等待资源不被活动回合使用 | plugin/uninstall → 回读确认；个人条目再移除源，内置卡片保留 |
| 聊天选择 | 稳定产品 ID＋安装内容版本／摘要核对 | 当前 skills/list 解析真实已安装 name/path → UserInput::Skill → turn/start |
| 自动发现 | 保留 include_skills_usage_instructions 与技能原生 policy | 原生技能目录、描述匹配、按需读取、去重、预算 |

安装和读取源是两个阶段。plugin/read 返回的本地源路径不能用作执行路径；必须使用 skills/list 返回的已安装缓存路径，并校验它属于目标原生插件。列表按实际聊天 CWD 核对配置，不用一个全局可见布尔值替代不同工作区的有效规则。

一技能一插件以插件 enabled 为 UI 唯一写入目标；不再同时维护文件 marker 和 skills/config 的第二开关。已有原生技能级策略／外部配置仍可影响有效可见性，遇到冲突显示原因，不循环覆盖。配置热刷新复用既有 native reload，不重建聊天或清预算。

## 3. 原生来源策略的最小增量

候选配置 `plugin_marketplace_mode = "local_only"`（拟新增，字段及 schema 以 Runtime 变更源为权威），默认值保持既有 upstream 行为。

local_only 的边界：

- 复用原生 MarketplacePolicy／local source 校验，只准入易界内置与个人市场；不能把所有 HOME 或任意项目市场接入页面／模型。
- 跳过官方 curated repo startup sync、远程 catalog/installed bundle 拉取和 Git marketplace 自动更新；读取本地目录不产生这些请求。
- 列表与安装都执行来源限制，不能仅在 UI 过滤；不自动加入已有官方缓存目录，不走 Git/npm/URL 物化。
- 保留原生目录／配置缓存刷新、安装器、卸载器和 Skills 加载；本地源到已安装副本的内容版本替换由 Host 在活动回合结束后显式请求原生 install。local_only 不自行后台替换已安装资源，避免迁移或活动任务期间抢先改写。版本复制／原子替换算法仍只有 PluginStore 一份。
- 当前 tool_suggest=false、remote_plugin=false、hooks=false、apps=false 保持；不向模型暴露可绕过用户加号的安装路径。
- 易界 Host 有效配置检查同步更新为明确的“plugins=true＋local_only＋既有限制”，保留输入草案隔离、现有 MCP、原生工具搜索、文档与媒体配置。
- 不升级上游，不改 canonical codex-rs 源树；若获准，以最小可重放补丁进入独立构建候选，保留当前日常二进制。

当前未发现能独立关闭上述全部同步的现成配置。实现前若新证据证明已有完整扩展点，应删除拟新增配置并直接复用。不得借 local_only 修改模型推理、沙箱、审批或通用网络策略。

此外增加只读 installedVersion 投影：原生 ConfiguredMarketplacePlugin 已有 installed_version，当前 PluginSummary 转换遗漏它。直接把已有事实投影到可选字段，原 localVersion 继续表示可提供版本。来源策略与这个字段是本方案明确提出的两处最小 Runtime 增量；不新增原生安装／卸载／版本管理器。

## 4. 导入边界

Tauri 通过原生文件选择器取得用户选择，仅向 renderer 返回不透明导入句柄／操作 ID 和展示信息。不得从网页 JS 接收任意绝对路径、发送整份 base64 或把本机路径写入公共错误。Host 只消费通过既有本机鉴权、固定导入根和摘要绑定的暂存资源；文件读取与传输适配在契约中定义，不直接复用聊天附件的任务语义。

推荐首期限制沿用现有技能包上限：输入 ZIP 至多 64 MiB、展开总量至多 64 MiB、普通文件至多 2048 个；单文件 SKILL.md 至多 1 MiB（新增产品限制）。流式累计并限制单操作资源，默认同时处理一个导入；正常目录项不计普通文件数。超过边界在提交原生安装前拒绝。

复用 Host 当前 archive 校验的普通文件、路径约束、大小、文件数、重复／大小写碰撞和摘要代码，但把“导入读取”与旧安装 receipt 写入拆开。ZIP 的一个外层目录可以移除，大小写变体入口归一到 SKILL.md；不递归展开嵌套压缩包。安装包和脚本不得在导入时运行。

生成的 wrapper 由 Host 控制，仅指定 skills 路径与明确空 mcpServers，资源放在 skills/main 下。不能把用户提供的 plugin.json、.codex-plugin、.claude-plugin、根 MCP／hooks 配置提升为插件权限；嵌套插件布局明确不支持，给出重新打包提示。合法 agents/openai.yaml 的界面／技能 policy／依赖声明保留，SkillMcpDependencyInstall 关闭，导入不注册或启动第三方 server。

通过 plugin/read 让原生解析元数据；无合法 Skill 即失败。若原生只返回空技能列表而未提供结构化诊断，则给出“未识别到有效技能，请检查 frontmatter 与 description”，不另写一套解析器伪装原生错误。成功预检也不等于工具依赖已满足。

内容摘要对归一化后的普通文件路径、字节与顺序确定性计算；导入 ID 由应用生成，不信任文件声明的产品 ID、来源或“已验证”许可。展示名称相同不导致覆盖。

## 5. 状态、一致性与取消

产品投影至少分开：origin、稳定 skill_id、可提供／已安装版本、installation_status、enabled、runtime_visible、dependency_status、缺项、operation_id／错误。安装事实来自 native snapshot，导入 registry 只补来源／身份。依赖状态使用 ready／missing／needs_authorization／unknown，并在新契约中定义。

操作过程可使用现有 journal 扩展类型：received → validated → native_pending → verifying → complete。异常为 failed 或 reconciliation_required；这些是操作状态，不是第二个安装数据库。

- 同一 operation_id＋相同输入返回同一操作，输入不同拒绝；同一来源内容摘要的重复导入不重新开关已安装项。
- RPC 超时先查原生状态，不能直接反向删除或再安装；原生缓存成功但配置未成功时只恢复受控配置并核对，不能手改缓存。
- 提交前取消只清理该操作暂存。安装请求已发送则记录取消意图，先确认 native 结果；确认为本次新安装后，用原生卸载补偿。确认不了时明确“状态待确认”，不报告取消成功。
- 首次新安装后的同步失败可补偿卸载该新对象；已有安装的重复操作不得被补偿删除。
- 安装／卸载请求只在单个对象上串行。卸载、覆盖升级与旧安装迁移在受影响活动回合结束后执行；首期可复用 Host 活动回合事实采取保守的“当前任务结束后重试”，不新造资源引用计数平台。
- 正常退出时停止接收新操作，等待当前有界提交并保存未决阶段，再用应用自身清理退出；无法安全退出则报告，不强杀。
- 重新启动先查询原生事实，再恢复未决操作；不依据过期 UI 成功态自动重放安装，也不把原生临时备份当永久回滚方案。

## 6. 工具依赖与可用性

对 25 个既有工具型技能逐项建立“原声明 → 已有真实能力”的生成映射，优先采用原生 agents/openai.yaml 能准确表达的声明；工具执行、发现／搜索、schema、权限和连接器凭据仍走既有链路。映射只是产品目录到已存在能力的适配，不新增 registry、搜索索引或执行器。

依赖是否满足取当前作用域真正可用的工具／连接器状态；同名且未授权不算 ready；当前聊天未选择或专家上下文不可用也不能以全局已安装承诺可调用。不存在的能力标 missing；无法可靠解释的个人声明标 unknown。未声明依赖不证明纯模型可用，不靠扫描正文猜测。

导入／安装成功与依赖授权分开：默认启用表示允许原生将技能纳入适用目录，不等于授权平台写操作、执行脚本或新增付费调用。缺项引导已有连接器管理，不替用户开通账户或伪造 first-party 身份。

## 7. 契约权威与跨仓改动

本次只落文档为 none。拟实施总体按 breaking：旧 Desktop 严格限定38项／固定清单，runtimeName 短名称不接受冒号，安装权威与持久 reader 改变；不能仅按上传端点新增判 additive。

| 仓库 | 拟修改面 | 权威／交付顺序 |
|---|---|---|
| yijie-codex | 最小来源策略配置、已有 installed_version 的只读投影、canonical schema／候选身份、原生定向验证 | 先证明既有 Plugin APIs 和新策略，独立构建，不先覆盖日常 |
| yijie-contracts | 原生 Plugin/list/read/install/uninstall、config/batchWrite 的兼容投影；技能管理新版本、导入与投影、命名空间、选择兼容 | 原生协议保持 Runtime 权威；易界导入／UI/Host wire 由 contracts 源先行 |
| yijie-skills | 38 个普通技能逐项生成原生插件／市场；发布摘要、展示映射、合法依赖声明 | 内容仓仍不依赖业务 Runtime；不改现有专家包的权威 |
| yijie-agent-host | Plugin RPC adapter、导入、稳定身份、操作对账、迁移、依赖投影、有效配置准入 | 消费固定契约；普通技能与专家分流，移除普通路径的旧回执写入与同步 |
| yijie-desktop | 新版 API/Tauri、原生选文件、页面分区／状态、去 Starter、聊天身份和图标回退、App Resources | 消费新版契约和来源 pin，复用 UI，不把本地文件权限交给 renderer |
| yijie | 候选 ADR、设计与状态、验证证据 | 正式接受后同步架构文档，不改历史验收结论 |

拟新增语义为“导入开始／上传完成提交／查询操作／取消操作”，可复用已有本地文件传输组件，但必须在 contracts 定义真实边界后生成。Host 新版技能 API／Native IPC 采用版本化入口，具体名称在源契约中冻结；本文不手写影子 DTO 或发明 Codex 不存在的 skills/import RPC。

旧 v1 只表达旧受管内置目录，不给旧 reader 塞个人技能或带冒号的新 runtimeName。启用前必须成对升级 Desktop/Host，启动时检查能力版本；不兼容时明确阻止管理／选择，不自动回退旧写入器。Contracts 的固定提交／digest 在实施中产生，本方案不伪造 pin。

## 8. 迁移、版本与历史

1. 去掉所有 Starter 触发点；已有 starter-skills-v1.json 仅作历史 reader，不根据标记补装。
2. 应用正常退出后的维护启动中读取旧安装回执、内容摘要及启停；先限制新聊天／管理提交，复制保存本次迁移所需旧技能源与配置记录，不清历史库。
3. 建立稳定旧 skill_id → native plugin identity → 安装内容版本的映射。用当前已安装内容生成兼容源，再通过原生 install 迁移，不能用 App 新版本静默替换用户当前版本。恢复原 enabled，核对后才接纳新聊天。
4. 新路径核对成功后，从普通技能 extra roots 移除旧根，并停止旧普通对账 writer；旧源保留作回退材料但不重复注册。专家资源的根、版本、会话绑定按原逻辑保留。
5. 原生 cache 替换后未承诺永久保留旧版本；必要回退从保留的来源再次调用原生安装恢复，不能由 Host 拼 cache 回写。失败只回退本次迁移对象，不删除用户原源或其他插件。
6. 稳定技能 ID 和已存 `{id,version}` reader 保留；历史消息、rollout、已经接受的操作重放结果不改写。旧纯文本 `$copywriting` 不保证匹配新命名空间：新界面选择使用结构化输入；历史文字仍可读／复制。有已存选择的重发走 ID／版本核验；仅有旧纯文本的消息按原文保留，并提供升级说明与重新选择入口，不承诺旧短名仍为确定性点名，也不在 Host 另造匹配器。
7. 草稿、重试、计划任务中持久化的技能引用逐项检查；旧版本仍可映射则按精确内容执行，否则在发送前提示重新选择，不默默选择最新版本。不自动重跑历史任务。
8. 回滚优先回到保留新 reader 的兼容模式，个人技能先停用并保留导入源；不能直接用旧二进制写新状态。若需要回旧安装权威，仅在显式维护流程从保留材料恢复，并移除本需求拥有的原生插件注册，不能两套 writer 并行。

App 升级的内置可提供版本由包内容决定。local_only 禁止后台自动替换已安装内容；Host 在普通启动维护／活动回合结束后，对已安装且确需更新的内置条目显式调用原生 install，并恢复原 enabled。迁移／回退先固定保留源版本，不与升级操作混成一笔。未安装项更新目录后仍不安装，个人导入内容不随 App 升级覆盖。升级前保留原版本来源；失败先回读，必要时通过原生安装恢复旧源并确认，不假设原生 install 的文件原子性覆盖后续配置失败。内容变化必须发布新版本，不能同版本暗改。

原生 plugin/read 仍读 local source，因此展示“可提供版本”与“已安装版本”要分开核验；安装版本使用本节所述原生 installedVersion 投影，执行路径使用实际 skills/list。不能把来源版本覆盖成安装版本，不能通过解析缓存目录名在 Host 复制原生版本算法。

## 9. 实施顺序与范围

按 Runtime 能力及最小来源策略 → Contracts → 技能源／Host → Desktop → 定向检查 → 正常真实客户端验收的技术依赖顺序连续实现，不建立多组 Demo 治理切片。进入实现前明确接受这份方案中 Runtime 来源策略、安装权威迁移和 breaking 兼容设计。

先用普通本地合成技能证明本地列目录、安装、启停、卸载、EOF 正常结束，以及没有远程市场请求，再迁移 38 项和导入 UI。不能因为原生接线困难就悄悄恢复自研安装器。30分钟无新证据扩大只读调查；90分钟同一阻塞比较最小替代；核心240分钟／总16小时未闭环时重定范围，不降低已确认产品规则。

不在本期实现云端市场、账号同步、远程下载、通用插件上传、任意 MCP server 自动安装、新连接器、技能编辑器或批量多技能导入。公开签名分发与生产范围另行执行既有发布门禁。本次任务不授权付费模型、Git 提交推送或日常数据迁移。
