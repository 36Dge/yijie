# 原生能力复核与修订2接入依据

2026-11-13。现有源码基线未变；原始来源证据保留于 references/source-evidence.json，补充复核见 references/revision-2-source-evidence.json。修订1位于history/revision-1，其“两处增量即可完成”的结论已被本文件及04替代。

## 1. 已有能力与实际复用

| 已有原生能力 | 源码依据 | 修订2接入 |
|---|---|---|
| 原生本地市场登记 | [marketplace_add.rs](../../../../yijie-codex/codex-rs/core-plugins/src/marketplace_add.rs):134–153 | 复用marketplace/add的Local分支登记固定根；它不会复制／安装所有插件 |
| 本地source和路径约束 | [marketplace.rs](../../../../yijie-codex/codex-rs/core-plugins/src/marketplace.rs):649–685 | 两个固定根内相对source；不可用当前App只读目录直接指向外部备份 |
| 首次安装及默认启用 | [manager.rs](../../../../yijie-codex/codex-rs/core-plugins/src/manager.rs):1427–1483 | 首次plugin/install，不复制安装器；结果不当整笔事务完成 |
| 缓存原子替换 | [store.rs](../../../../yijie-codex/codex-rs/core-plugins/src/store.rs):520 | 原生复制、替换和旧版本处理，Host不写cache |
| 原生卸载 | manager.rs:1530–1547 | 原生删除cache和配置，Host只核对后发布 |
| 既有版本刷新 | [loader.rs](../../../../yijie-codex/codex-rs/core-plugins/src/loader.rs):439、465、478、597 | N3直接调用IfVersionChanged或ForceReinstall，保留原启用配置 |
| 刷新调度状态 | manager.rs:2104、2185 | 复用管理器已有在途与串行机制；薄桥接增加精确触发／完成确认 |
| 配置层与乐观版本检查 | [ConfigReadParams](../../../../yijie-codex/.yijie/schemas/app-server/generated-json-schema/v2/ConfigReadParams.json)、[ConfigBatchWriteParams](../../../../yijie-codex/.yijie/schemas/app-server/generated-json-schema/v2/ConfigBatchWriteParams.json) | includeLayers、expectedVersion、reloadUserConfig；Host不手写TOML或重算优先级 |
| 原生技能规则 | [config_rules.rs](../../../../yijie-codex/codex-rs/core-skills/src/config_rules.rs):30–121 | 保持layer／顺序和name/path语义，迁移精确selector并由原生回读有效结果 |
| 元数据／命名空间 | [loader.rs](../../../../yijie-codex/codex-rs/core-skills/src/loader.rs):734、776、838；[namespace.rs](../../../../yijie-codex/codex-rs/core-skills/src/loader/namespace.rs):127 | 原生解析，Host只使用返回身份；不新增YAML解析器或文本匹配器 |
| 选择／正文与去重 | [injection.rs](../../../../yijie-codex/codex-rs/core-skills/src/injection.rs):63、149、396 | UserInput::Skill与原生点名；正文不经Host拼接 |
| 隐式与预算 | [render.rs](../../../../yijie-codex/codex-rs/core-skills/src/render.rs):18、30 | 原生目录、描述匹配与按需读取保持 |
| 薄Host的旧操作存储基础 | [store_database.go](../../../../yijie-agent-host/internal/skills/store_database.go):16–61 | 复用bbolt与通用幂等设计；新格式隔离，专家旧数据继续原reader |

## 2. F1及F4：旧列表不足以承担安装事实查询

manager.rs:2502的configured_plugin_states先枚举配置键，再检查PluginStore；没有配置的缓存不会进入installed集合。1595–1599又以installed为前提计算installed_version。简单把该字段加入PluginSummary无法发现cache-only，也不能区分正在写入与真正未安装。

manager.rs:1575之后只遍历当前marketplace条目。app-server [plugins.rs](../../../../yijie-codex/codex-rs/app-server/src/request_processors/plugins.rs):878的plugin/installed同样先取市场列表再筛installed。目录删项时两者都可能遗漏实际缓存；但loader.rs:743–815可继续按配置加载缓存。

修订2 N2应直接复用PluginStore与配置读取，把配置键／缓存的并集以及指定ID的缺失事实返回；不能套用上述两层过滤。N2中cacheVersion来自原生active_plugin_version，缓存有效性还需原生manifest／Skill解析；目录是否存在单独返回。Host既有操作前态只用于判断恢复意图和删除归属，不代替实时状态。

## 3. F3：版本来源与回滚不是一个version参数

[PluginInstallParams](../../../../yijie-codex/.yijie/schemas/app-server/generated-json-schema/v2/PluginInstallParams.json)没有指定历史版本参数。本地source必须在市场根内；store.rs:567–573还会移除旧缓存版本，临时备份不构成持久回滚来源。

修订2固定两个App Data运行市场根、保存不可变源快照并切换条目source。App资源仍是本地发行源，无远程下载。选择一个获准来源属于产品版本意图；何时刷新、版本是否不同以及文件如何替换交给N3和既有原生函数，不在Host复制算法。

## 4. F5：既有刷新器必须复用

loader.rs:597根据native active version判断是否变化，604–613直接调用PluginStore，不像manager.rs:1477那样再次写enabled=true。故“Host调用plugin/install再恢复开关”会引入不必要的启用窗口和重复更新组织。

修订2撤回这一做法：Host只调N3；N3限制目标与来源，转调既有刷新函数并返回完成／错误，再用N2核对。回滚同样复用ForceReinstall。来源策略只约束网络来源，显式触发策略只改变调度边界，不能称之为新版本管理器。

## 5. 仍存在的原生缺口

N1、N2、N3是拟议薄扩展，不是已经支持的RPC／配置。N1的必要性：manager.rs:1926、2292开启插件后可启动官方同步；[startup_sync.rs](../../../../yijie-codex/codex-rs/core-plugins/src/startup_sync.rs):95有Git／HTTP／备份下载回退，remote_plugin=false不足以阻止。marketplace allowlist还有官方特例，必须覆盖。

N2缺口是catalog独立库存及部分状态投影；N3缺口是已有刷新器缺少受控、可等待的app-server入口。两者应是原生事实／原生能力的接口接入，不以缺接口为由放到Host重新实现。

## 6. 导入适配为何保留在Host

原生 [external_agent_config.rs](../../../../yijie-codex/codex-rs/app-server/src/config/external_agent_config.rs):1193的技能导入针对外部代理固定目录，不接受任意上传ZIP／单文件；不能伪造外部代理布局来套用。原生 [plugin_bundle_archive.rs](../../../../yijie-codex/codex-rs/core-plugins/src/plugin_bundle_archive.rs):124处理tar.gz，也不是本产品ZIP输入协议。

所以文件选择、ZIP归一化、来源校验和产品ID是必要适配，复用Host现有archive模块可用部分。最终原生manifest是标准制品生产，不是重新实现解析／安装。原生marketplace条目还支持manifest fallback，当前采用显式标准wrapper以固定包摘要与入口，不另写fallback解释器。

[mcp_skill_dependencies.rs](../../../../yijie-codex/codex-rs/core/src/mcp_skill_dependencies.rs):34有first-party及feature限制。保留合法声明不等于自动安装授权；本期不伪装originator，不启动用户上传的server。工具就绪投影只引用已有MCP／连接器事实。

## 7. F6的私有格式和配置证据

Host [store.go](../../../../yijie-agent-host/internal/skills/store.go):184–247严格限制kind/status/phase；store_database.go仍用同一校验读取v2记录。修订2将新阶段放入隔离的新格式，不给旧journal塞新enum，保留旧成功结果精确重放及专家reader。

store.go:93–114在recoverTransactions前只接受schema 1／2，因此修订2还使用公共入口的拟议schema 3路由标记作为旧writer阻断点。新Host版本化loader承接旧codec／兼容backend，专家写入不能覆盖该标记；旧原字节快照保留。该标记是标准格式迁移，不是将旧日志故意改坏后继续运行，也不允许未具reader的旧Host绕过拒绝。

原生config_rules.rs按路径／名称和层顺序处理。旧路径、旧短名原样保留并不能约束新缓存／新命名空间；把所有旧false都抹掉也会丢失用户设置。04明确区分Host生成的普通开关规则与额外用户／会话规则，使用原生带版本检查的配置编辑重绑定，不复制其优先级算法。
