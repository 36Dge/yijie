# FEAT-170 复审与实施记录（2026-11-08）

用户最新指令“再次审计方案，审计完成后开做执行”覆盖此前仅方案限制。已授权方案范围内源码实现、正常本机验证及具备资格后的启用；无Git提交/推送或付费调用额度。首批仍为Kimi，MiniMax保持旧路径。00/01/02保留方案时点记录，当前状态以本文件及feature.yaml为准。

## 复审结论

推荐B保持：同一原生ToolSearchHandler/BM25/缓存，标准function输入输出，命中后原生exec调用。未发现需要Host搜索器或新的执行/审批引擎。

实施重点：

1. 模型schema必须从ModelInfo/ModelsResponse原生类型生成；默认字段省略以保持旧目录兼容。
2. 原生缓存比较必须加入transport；不能对同一search_infos复用另一种wire输出的handler。
3. Deferred工具若不可经CodeMode调用（含excluded/direct-only）必须保留原直接路径，Hidden不能复活；function搜索保持DirectModelOnly，不成为exec嵌套工具。
4. 函数调用的call_id、错误、取消与函数输出保持配对；原native模式保留专用item；typed结果生成exec说明，避免字符串反解析。
5. 外部上下文记忆保护在改用function后仍保留，含调用失败/取消；诊断不额外输出结果目录。
6. 新模型目录只在普通根线程创建/冷恢复覆盖；标题默认目录不启用，input-only注册表为空，V2子代理继承限制保持。已加载resume可能忽略config，启用必须正常重开并检查实际声明。
7. 不支持的旧专用ToolSearch历史在function候选发往提供方前明确报错，不删除历史或重放业务。
8. 保留当前上下文浮层及其他前序dirty。开始时未发现运行中的易界/Host进程；Desktop原生文件写入前再核查。

## 初始状态与安全

当前Runtime基线仍为interaction-tools-v1/038d498bda0d4cb8899e15ea81dfa777b6928adc0e389aebf5e20b3038332086，固定上游不变。产品相关五仓HEAD与方案记录相同，已有大量前序未提交文件；不reset、批量格式化或覆盖。允许标准脚本生成新候选，不替换既有已验收制品。所有模型/第三方实际调用目前0。

## 当前进度

复审完成，开始原生适配；产品验收及启用尚未完成。后续逐项记真实检查，不借FEAT-169证据或额度。


## 实施中补充的历史截断缺口

源码复核发现 ContextManager::process_item 对普通 FunctionCallOutput 应用文本截断，而原生 ToolSearchOutput 保留完整定义。仅将输出改为 function 会在较大 schema 时截断 JSON。修复限定在同一原生历史机制：按原 call_id 与最近匹配的 plain tool_search FunctionCall 保留完整定义，不依据结果正文自报类型；其余普通/命名空间工具仍按原策略截断。新增普通约22KB描述、低截断额度及冷读回的定向测试，不扩展执行权限或另建历史库。

最初两次单元检查失败均为测试期望问题：原生augment生成TS声明而非调用字符串；JsonToolOutput::code_mode_result返回结构化值而非JSON字符串。已按源码更正期望，不弱化真实函数wire/名字/完整JSON断言。首轮三个其它用例通过，第二轮16个其它用例通过；最终结果另记。


## 生产目录覆盖与测试辅助差异

深入调用点后纠正方案F15的推断：ThreadManager共享进程模型管理器；Config.to_models_manager_config确实携带model_catalog，但生产construct_model_info_from_candidates此前没有消费它，只有test_support辅助函数先选择了该目录。因此只写thread/start config不足以启用。最小修复在原生生产模型管理器中读取当前线程目录，仅覆盖supports_search_tool与tool_search_transport两个字段，复用现有最长前缀查找；其余模型元数据保持原有解析。新增直接调用StaticModelsManager的隔离测试，普通目录启用→辅助默认关闭→显式基线关闭不污染共享状态。

18项原生搜索相关lib测试已通过（包括较大定义完整历史、输入输出、缓存、路由及中英文普通样本）。首个构建在source-id脚本导入公共runtime_manifest模块时失败，已补脚本目录的正常Python导入路径；不是Runtime执行失败。构建正在正常进行，无强杀。


## 新任务真实验收授权

用户已明确批准仅Kimi最多12次短模型HTTP（含续行/子调用/复验），本地只读合成MCP与隔离临时会话；MiniMax/图片视频/外部业务0。独立FEAT-170计数器账本，不使用FEAT-169余额。已准备两回合：成功搜索→exec→本地只读工具，以及一次无命中。开始前本任务实际0次。

本地验证：Native模型管理器1项+搜索相关18项PASS；Host3项配置/目录单元+4项真实Runtime本地回环PASS，覆盖较大定义完整JSON、恢复/停用/切换/重启、辅助/子代理/input-only、正常取消；Desktop原生cargo check和2项入口selector测试PASS。当前原生候选fac52ad79cc7e0a379fc597a7ecfcee573205d38a60c9d0ed3a2e96871ab0f45已构建，Contracts投影同步/check通过。


## Kimi实测与实际Gateway复审

本包Kimi真实验收PASS：5/12次HTTP，全部200，两个turn均completed，tool_search实际2次、exec1次、本地只读合成MCP1次，外部业务0。独立meter已通过stdin EOF正常退出0；剩余7次不自动消费。证据在Host `.local/tool-search-live/20261108-current-task/`，无其它模型或图片调用。

实际产品Gateway拒绝用例初次停在PrepareMarket，查明 marketDisabledServers仍调用旧的validateMarketEffectiveIsolation（假定memories关闭），而Startup已正确使用ForTools版本。只把这个入口改为现有ForTools校验并传当前NativeToolsEnabled，保持既有feature/profile和子代理MCP隔离约束；不放宽权限。这是当前选集接入的真实缺口，纯MCP回环无法覆盖。正在复跑真实产品worker+原生搜索/exec→绑定审批→正常拒绝，所有提供方调用仍为本地loopback，拒绝前不申请实际外部HTTP许可。


## 最终启用

实际Gateway拒绝链路修复后8项Host race检查通过，Kimi仍5/12；原入口pnpm client:dev已增量启动原数据Homes，实际App50953/Host51062/Runtime51067为观察时PID，readyz200，Model Kimi、stable API。当前Runtime为fac52候选。Host的tool_search/native/interaction三个开关均true；进程默认目录的两模型search=false，普通聊天目录仅Kimi true+function_code_mode，MiniMax false。停用开关保留新reader，避免无意退回旧历史截断行为。完整结果与分层/GUI边界见04。


## 最终记录校正

最初04草稿曾把AC-004/005/008的分层或子集证据列为PASS；最终核对原Must AC后改为pending，implementation complete与实际本机启用不变。未运行的批准/撤销、并行和搜索历史压缩组合、原生GUI全链明确登记，verification PARTIAL、D4不声明通过；不缩写原AC来制造绿色。原方案F15推断也在00标注纠正。


## 同一桌面聊天补验（用户本轮限定）

已用现有start-ui真实原生窗口完成tool_search→exec→原审批允许一次→真实Kimi检索→同一聊天最终答复，AC-008 PASS；本次4个模型HTTP全部200，累计9/12，另经用户单独批准的一次只读检索完成。其余未完成场景未执行，详情见05及ui-e2e-result.json。为保持硬请求上限，仅开发入口增加显式start-ui计数器接线，普通入口保持原配置；不改Runtime/Host/连接器执行和审批。
