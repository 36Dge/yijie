# 原生能力与复用边界

依据 2026-11-13 当前源码和 canonical schemas。仓库版本、原有改动、源文件摘要与包检查见 [source-evidence.json](references/source-evidence.json)。固定上游 rust-v0.144.6 / 5d1fbf26c43abc65a203928b2e31561cb039e06d；实施还需核对日常构建实际采用的完整候选与 patch chain。

## 1. 可直接复用的原生能力

下列路径相对 yijie-codex/codex-rs。源码证明能力存在，本需求的接线尚未运行。

| 能力 | 源码／接口证据 | 复用方式 |
|---|---|---|
| 本地市场格式 | core-plugins/src/marketplace.rs:20、126、961 | .agents/plugins/marketplace.json、local source、分类；所有技能 policy.installation=available |
| 本地源无需下载 | [loader.rs](../../../../yijie-codex/codex-rs/core-plugins/src/loader.rs):1381 | Local 分支返回原路径；不传 Git/npm/remote 来源 |
| 安装并默认启用 | [manager.rs](../../../../yijie-codex/codex-rs/core-plugins/src/manager.rs):1273、1427、1477 | plugin/install；不复制安装与配置写逻辑 |
| 安装缓存与原子替换 | [store.rs](../../../../yijie-codex/codex-rs/core-plugins/src/store.rs):287、520 | Runtime 独占 plugins/cache；Host 不修改缓存内容 |
| 卸载 | manager.rs:1504、1530；store.rs:326 | plugin/uninstall 删除安装缓存并清原生配置 |
| 列表／详情 | [plugins.rs](../../../../yijie-codex/codex-rs/app-server/src/request_processors/plugins.rs):539、986 | plugin/list 指定 marketplaceKinds=[local]；plugin/read 预检本地源 |
| 原生参数 | [PluginListParams](../../../../yijie-codex/.yijie/schemas/app-server/generated-json-schema/v2/PluginListParams.json)、[PluginInstallParams](../../../../yijie-codex/.yijie/schemas/app-server/generated-json-schema/v2/PluginInstallParams.json) | Host 从来源映射构造 marketplacePath/pluginName；不让 renderer 传路径 |
| 插件启停 | [toggles.rs](../../../../yijie-codex/codex-rs/core-plugins/src/toggles.rs) | config/batchWrite 写 plugins.<native-id>.enabled，并 reloadUserConfig；不另存停用标记 |
| 技能实际快照 | [catalog_processor.rs](../../../../yijie-codex/codex-rs/app-server/src/request_processors/catalog_processor.rs):488 | skills/list(forceReload=true)；分别回读安装状态与当前 CWD 可见性 |
| 元数据解析 | [loader.rs](../../../../yijie-codex/codex-rs/core-skills/src/loader.rs):734、776、838 | 原生解析 SKILL.md、agents/openai.yaml；不在 Host 重写 YAML 语义解析器 |
| 命名空间 | [namespace.rs](../../../../yijie-codex/codex-rs/core-skills/src/loader/namespace.rs):118 | 使用原生返回的 plugin:skill 名称 |
| 选择／正文／去重 | [injection.rs](../../../../yijie-codex/codex-rs/core-skills/src/injection.rs):63、149、396 | UserInput::Skill、原生文本触发，不由 Host 拼正文 |
| 隐式发现与预算 | [render.rs](../../../../yijie-codex/codex-rs/core-skills/src/render.rs):18、30 | 保留原生元数据目录、触发说明与按需读取，不恢复仅显式策略 |
| 市场位置配置 | [installed_marketplaces.rs](../../../../yijie-codex/codex-rs/core-plugins/src/installed_marketplaces.rs):18、64 | 原生 marketplaces local source；市场源目录不加入 Skills extra roots |

## 2. 必须处理的真实约束

### 开启插件会产生后台官方市场同步

manager.rs:1926 在 plugins_enabled 且不使用远程全局目录时调用 start_curated_repo_sync；2292 启动官方同步。[startup_sync.rs](../../../../yijie-codex/codex-rs/core-plugins/src/startup_sync.rs):95 有 Git、HTTP、备份下载回退。因此 remote_plugin=false 与 marketplaceKinds=[local] 不是关闭后台同步的充分条件。

当前 Host 的 [market_runtime.go](../../../../yijie-agent-host/internal/codex/market_runtime.go):150 明确关闭 plugins，并校验有效配置。实施必须同时更新配置、有效性检查和来源 pin，不能只开前端开关。

推荐一个原生来源策略扩展，候选名 `plugin_marketplace_mode = "local_only"`，**该字段是方案新增，不是现有能力**。默认保持上游行为；local_only 禁止远程目录同步、官方缓存市场自动并入、Git/npm source 物化，仅允许受准入本地目录，保留原生本地安装和执行。所有来源调用点须复核，不能只挡一次 startup 而漏掉列表刷新／重新配置。

原生 marketplace allowlist 可以复用，但当前对官方市场有特例，单独启用它不足以证明本地边界。限制只作用于技能市场分发，不关闭正常模型与已授权业务连接器网络。不得伪装 git、改系统网络或制造权限故障来规避。

另一个来源刷新副作用在 core-plugins/src/loader.rs:478–613：原生会按已配置插件的来源版本更新缓存。为满足活动回合资源保护及迁移顺序，local_only 将内容版本替换交给 Host 在既有回合空闲边界显式调用原生 install；目录／配置缓存刷新保持。这是来源策略的范围，不引入第二个版本安装器。

### plugin/read 的本地源路径不等于已安装缓存路径

manager.rs:1781–1825 对 local source 读取源目录，即使条目已安装。因此 plugin/read 用于预检／可提供版本，不能直接拿其 Skill path 执行。运行路径必须从 skills/list 的当前已启用快照取得并核验归属。原生 skill metadata 不直接携带产品 ID，Host 的稳定 ID 到原生身份映射属于必要适配。

### 自动依赖安装有第一方限制

[mcp_skill_dependencies.rs](../../../../yijie-codex/codex-rs/core/src/mcp_skill_dependencies.rs):34 要求 first-party originator 与 SkillMcpDependencyInstall；411 起只处理原生 MCP 依赖。不得伪装客户端身份，或把 browser.search 等抽象能力名直接视为 MCP server。

本期关闭自动依赖安装。保留合法技能元数据，安装时不执行其中 server 命令。已有 Runtime MCP／连接器能力继续用于调用；缺失、需授权、未声明分别表达。未来自动安装依赖是独立扩展。

### 原生安装／配置并非跨进程整笔事务

manager.rs:1450 先安装缓存，1477 再写 enabled；卸载也是先移除缓存再清配置。不能把一个 HTTP/RPC 成功或超时直接当最终用户状态。Host 复用原有操作 ID／journal，仅记录请求阶段并通过原生事实对账，不另存独立 installed/enabled 真相。失败时原生缓存不得由 Host 私自修补。

### 已安装版本在原生内部已有，但当前 app-server 投影遗漏

manager.rs:316 的 ConfiguredMarketplacePlugin 已有 installed_version，并在1596由 PluginStore.active_plugin_version 取得；app-server/request_processors/plugins.rs:150 转换成 PluginSummary 时只写 local_version，没有投影 installed_version。对 local source，localVersion 是可提供版本，不能冒充已安装版本。

因此除来源策略外，建议追加一个很薄的原生协议投影：PluginSummary 可选 installedVersion，直接转发已有 installed_version；未安装为 null，不改变现有 localVersion 语义。字段是拟新增，必须 Runtime source/schema → Contracts 投影 → Host/Desktop，禁止在 Host 重造版本扫描器。这不需要新增安装／版本管理机制。

### 名称与版本迁移是真实兼容变化

原生插件技能名包含冒号；现有 Desktop chat-skills.ts:41 及旧契约只接收短名称。原生 injection.rs:396 对文本点名精确匹配，不保证旧 `$copywriting` 自动匹配新 `yj-skill-copywriting:copywriting`。因此本方案按 breaking 评审，不假装仅增加上传字段即可兼容。

## 3. 原有实现的调整落点

| 当前落点 | 事实 | 拟调整 |
|---|---|---|
| Desktop skills/defaults.rs:9、host.rs:249 | 7 项 Starter 自动安装 | 去掉触发行为，保留历史 reader，不批量卸载 |
| Desktop skills/catalog.rs:19、326 | 固定 38 项及 bundle／提交严格校验 | 版本化消费原生目录和只读展示索引；个人导入不伪造内置许可 |
| Host skills/service.go:259、715 | 解包／回执／旧根注册／启停投影 | 普通技能转原生；保留专家资源分支 |
| Host skills/service.go:1156 | 工具型可安装技能统一 degraded | 基于现有能力事实投影缺项，不另建工具注册或执行引擎 |
| Desktop domain/chat-skills.ts:41 | 短名称校验并拼 $name | 新提交优先结构化选择；原生名称按权威协议消费；旧展示 reader 保留 |
| Host skills/selected.go | 核验旧回执后构造 Skill 输入 | 核验新身份映射、原生安装与实际快照，正文仍交给 Runtime |

既有专家、工具搜索、MCP、审批、文档和媒体不能被本地市场策略误关闭。来源策略与安装权威迁移为候选架构决定，尚未批准或实施。
