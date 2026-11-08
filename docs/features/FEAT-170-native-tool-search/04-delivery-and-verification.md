# FEAT-170 本机接入、启用与验证（2026-11-08）

> 桌面续验更新：同一条真实桌面聊天的完整链路已通过；模型累计9/12次，另获批并完成1次只读联网检索。当前结果见[05桌面验收](05-desktop-chat-e2e.md)。以下费用、GUI未执行等内容保留其先前记录时点语义；其它未完成场景不执行，整体D4保持未通过。

**原生 tool_search 已接入，并在原开发入口默认启用。范围为普通Kimi K3.1 Pro根聊天中当前可检索的有效工具；无目录时原生不声明该工具。MiniMax保持原配置。**

本次遵循用户“复审后执行”指令，没有提交、推送或公开发布。已复用原生搜索/缓存/目录/CodeMode/MCP执行与原审批机制，没有新增Host搜索服务、索引库、已加载状态或新的审批平台。**实现完成、已本机启用；完整D4验收尚未通过。**

## 1. 实现与复审修正

- Runtime 0023：同一ToolSearchHandler的function输入/输出适配，typed定义使用原生CodeMode命名和声明；native专用协议分支保持。
- 缓存加入transport维度；function搜索保持直接调用；不把CodeMode排除或Hidden策略变成额外执行权限。
- 原生生产模型管理器补齐当前线程目录的两个搜索字段；进程默认目录不开，普通线程按原config机制覆盖，辅助线程不继承新能力。
- 精确call_id对应的搜索函数结果保留完整schema，避免普通文本截断破坏JSON；外部上下文记忆标记和日志保护保持。
- Host只装配和核验目录/制品。修复选集准备中遗留的旧隔离校验，统一复用已有ForTools校验，不放宽scope或审批。
- Desktop原入口严格匹配来源；开关只控制发现能力，停用仍保留兼容Runtime reader，显式恢复基线模型目录。
- 当前受管模型固定tool_mode=code_mode；不把其它自定义模型/CodeModeOnly组合描述为已资格化的产品能力。

运行制品源：`fac52ad79cc7e0a379fc597a7ecfcee573205d38a60c9d0ed3a2e96871ab0f45`。271个stable app-server schema树保持不变；模型schema由原生ModelsResponse派生。旧Dfa/038制品保留，首个03ab草稿候选从未启用。

## 2. 已执行验证

| 层次 | 实际结果 | 证据位置 |
|---|---|---|
| Native模型管理器 | 1项生产StaticModelsManager线程目录/辅助隔离测试PASS | codex `.local/tool-search/scoped-catalog.log` |
| Native搜索 | 18项PASS，含wire配对、缓存、暴露、完整定义/历史、24工具中英文12查询及普通热查询时间界限 | codex `.local/tool-search/unit-scoped.log` |
| 标准构建与schema | canonical build/prepare check及model/config/app-server schema生成PASS | codex `.local/tool-search/build-scoped.log` |
| Contracts | 新family生成/同步/check、2项conformance PASS；fallback全源离线结构比较exit0 | contracts `.local/tool-search-breaking.log`、tests/runtime-tool-search.test.mjs |
| Host当前候选 | 8项顶层race测试PASS：5项实际Runtime/Gateway和3项配置/目录测试；live用例在此无授权环境下正确SKIP | host `.local/tool-search-race.log` |
| 原生问答/上下文回归 | 当前候选4项PASS，包括实际问答/恢复及新窗口/历史、旧配置保留 | host `.local/tool-search-interaction-regression.log` |
| 保留四组基线 | 5项顶层+2个模型子场景PASS，真实原生V2/Guardian/冷恢复/补丁/四记忆/exec/wait | host `.local/tool-search-retained-baseline.log` |
| Desktop | 受影响Rust cargo check PASS；canonical客户端实际增量构建PASS；2项selector单元PASS；Shell/JS语法PASS | desktop `.local/tool-search-native-check.log`、`.local/tool-search-client.log` |
| 计数器 | 4个普通无效配置在读凭据/开服务前拒绝；不发HTTP | 实际命令记录与03 |
| Go静态/空白 | 受影响codex/app go vet及仓内diff空白检查PASS | 本轮实际命令 |
| Kimi真实模型 | 5/12 HTTP，全部200；tool_search2次、exec1次、本地只读MCP1次，两个turn completed | [实测摘要](references/kimi-live-acceptance.json) |
| 原开发入口 | pnpm client:dev启动原Homes，Host readyz200，实际Runtime是fac52候选；Host三个开关true；Kimi专用目录true、默认目录与MiniMax false | [入口观察](references/activation.json) |

源码与构建来源见 [最终来源](references/final-source.json)。没有把早期失败记录覆盖为通过：原生测试的两处期望、Go临时目录创建方式、source-id脚本导入路径、选集旧校验均在03如实记录。一次误把旧四组专用harness放到当前候选，两个测试在精确制品配对处被拒绝；随后在其保留制品上正常通过，不放宽配对门禁。

旧Native6两个响应枚举的历史兼容警告保留，不属于本次新增。结构比较绿色不代表生产滚动发布兼容。

## 3. Must AC

| AC | 本次范围内结论 | 依据 |
|---|---|---|
| AC-001 | PASS | 原生委托/缓存源码、Native单元及实际调用 |
| AC-002 | PASS | Kimi真实function搜索→exec→本地MCP，所有请求200 |
| AC-003 | PASS | 无目录/空结果、原生cache变化、中英文固定样本；不承诺所有供应商自然语言召回 |
| AC-004 | pending（部分已通过） | 真实产品worker/Gateway、原thread/turn绑定及正常reject通过；批准后业务调用与正常撤销未执行，外部业务额度0 |
| AC-005 | pending（部分已通过） | 普通取消、下一轮、旧会话、模型切换、关闭/重开已通过；并行搜索及搜索历史与compact/new_context组合未全部动态执行 |
| AC-006 | PASS | 子代理/input-only/辅助目录隔离、新候选问答/上下文与保留四组回归；原生标记保持 |
| AC-007 | PASS | Runtime→canonical schema→Contracts→Host/Desktop精确来源与实际启动 |
| AC-008 | pending（分层证据通过） | 原入口Ready，Kimi隔离会话实际工具链通过，未资格模型保持旧路径；原桌面同一聊天完整链未执行 |
| AC-009 | PASS（固定普通样本范围） | 初始请求与exec说明无完整延迟schema，长定义JSON完整，原生热查询界限通过 |

## 4. 证据边界与未执行项

- 本次实际修改不增加UI。真实Kimi在隔离临时会话使用本地只读合成MCP；真实产品Gateway拒绝使用本地模型回环；原客户端另做实际启动/就绪和配置观察。这是明确的分层证据，**没有宣称同一条聊天的完整Native GUI E2E**。
- 未操作原生GUI提交额外模型任务，不为证明界面增加供应商调用；已有unbundled开发入口的自动化绑定限制保持。
- MiniMax模型请求、图片视频、外部业务调用均为0；剩余7次不自动消耗，也不转移到其它任务。
- 没有执行全量回归、攻击fixture、权限破坏、强杀或可执行文件替换；仅正常EOF、中断、拒绝和普通合成数据。
- 源码仍为本地工作树候选，未commit/push/tag、签名或发布。根据治理手册，分层结果不能替代一次fresh原客户端全Must AC；因此feature保持active，implementation为complete，verification为PARTIAL，不声明D4、production_hardened或生产批准。

## 5. 使用与停用

普通Kimi聊天选中已有效启用的连接器后，模型可按任务需要使用tool_search；它查找元数据，不自动安装、授权或执行业务。后续exec调用仍受原审批控制。无可检索目录时不出现tool_search，属于原生设计。

需要停用时先正常退出易界，再运行 `YIJIE_FEAT170_TOOL_SEARCH=false pnpm client:dev`。该操作保留兼容reader和六组能力，只恢复普通线程的直接工具目录。未经单独兼容验证，不降级旧Runtime/Host、不降数据库、不删历史。

本次启动后的应用保持打开供用户使用；没有额外数据迁移、清库、全量备份或容器重建。

## 6. 方案用例的实际覆盖

T01—T06、T11的相关定向范围已执行；T07只完成真实Gateway拒绝，未走批准后的外部业务；T08完成辅助/V2/input-only与暴露隔离，未把它写成完整多会话并发验收；T09完成正常取消和下一轮，未执行所有并行查询组合；T10完成旧会话、停用、切换和正常重开，搜索历史结合compact/new_context未完整执行；T12完成获批Kimi隔离会话实测，原生GUI链未执行；T13完成来源与原入口启动/目录核验，没有额外GUI历史交互；T14通过固定目录召回、定义完整和热查询100ms界限，但未保存逐条耗时/字节比较或发布token降幅。初始02文件的NOT RUN表格是方案时点快照，不作为当前测试结果。

最终只读核验：2026-11-08T08:34:45Z，28项产品源码摘要全部与final-source一致，App/Host/Runtime原进程仍在，readyz200；各相关仓HEAD未变且git diff --check为0。

最终文档/来源检查见 [final-checks.json](references/final-checks.json)：D0结构、声明一致性、链接和来源校验通过。元仓测试首次因把canonical verification指针改为04而使两项包审计失败，已恢复为02并分别复测两项通过；未重跑整套，未把文档检查折算D4。
