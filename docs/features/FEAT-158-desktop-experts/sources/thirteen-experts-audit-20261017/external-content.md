# 13 位专家审计分工：6 位外部依赖专家（只读）

日期：2026-10-17。任务分类 `contract-impact=none`，仅资料/实现审计和方案记录，未修改任何产品、归档、配置、凭据、历史库或安装资源。未执行原包程序、依赖安装、认证、外部业务或攻击/故障注入。以下指出的是静态实现证据与拟迁移方案，不是线上服务可用性结论。

## 阅读基线与引用约定

`A=/Users/jack/Downloads/Personal_Info/易界文档/10专家`。

- `M=A/行业研究专家-MOSS/原始资源`，原包 moss-industry-research 1.0.6：1 Agent、9 Skills、292文件；已核对 Agent/Skill 调度、计算器、交付冻结/清单、Office helper、PPT模板引用和许可证。
- `E=A/股票研究专家/原始资源`，equity-research 2.1.2：1 Agent、15声明Skills＋1已废弃Skill；重点核对金融规则、DCF/首次覆盖/组合与产物依赖。
- `Q=A/量化策略回测师/原始资源`，strategy-backtest-expert 1.0.0：1 Agent、4 Skills；核对策略规范、两个实际Python策略、结果导出、WeStock脚本形态与NeoData查询器。
- `W=A/WindAlice万得金融专家/原始资源`，alice-financial-copilot 1.1.2：远程Agent CLI。读取压缩后的实际request/session/tasks/CLI/download源码；这些JS原文件多为1行，故用行1与函数名/字符位置帮助定位，不把它们称作已完成源码可复现验证。
- `T=A/美团生活助手/原始资源`，meituan-living-assistant 1.0.9：核对授权/业务/支付脚本、Skill、包依赖与多平台二进制清单。只读文件，不加载运行期登录态。
- `L=A/跨境电商带货口播专家/原始资源`，linkfox-expert-aigc-videogen-sale 2.1.0：4 Skills及全部API/prompt参考。

当前易界对照：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-skills`、`yijie-connectors` 的 AGENTS/README/SECURITY 已读；涉及后续修订覆盖旧README状态的规则，以当前文件/代码为准。本文主要对照路径：

- `yijie-skills/plugins/yijie-desktop-skills/experts/market-researcher/skills/industry-research/ROLE.md:7-23`：现有研究员只用当前选中连接器，Tushare仅单股单日，NeoData/WeStock不执行，HTML/XLSX已实现，DOCX/PPTX未实现。
- `.../industry-research/references/data-and-search.md:1-7`：金融MCP当前schema优先、来源不等价、真实工具资格待验证。
- `yijie-skills/plugins/yijie-desktop-skills/experts/linkfox-expert-aigc-videogen-viral-replicate/skills/video-replica/ROLE.md:4-12`：公开HTTPS、逐次审批、任务ID/制作单对应、不自动重发、不自动上传下载。
- 同目录 `scripts/prepare_video.py:45-117`：现有本地参数校验及构参，当前视频审阅子集仅SEED/SEED_FAST，显式声音/Pro等参数，16KiB Broker参数上限。
- `yijie-connectors/catalog/provider-registry.v1.json:263-268,327-332,511-521`：现有 wind、fanruan-growth-advisor、linkfox 是三个固定远程MCP；wind为 `https://mcp.wind.com.cn/vserver_qwenwork/mcp/`，不是WindAlice A2A。
- `yijie-connectors/catalog/provider-candidates.v1.json:407-414`：MOSS静态候选 `qualification:not_run`、无 verifiedTargets/supportedTools；目录存在不证明此账号可用。

所有新增仍应复用 ROLE/Knowledge索引→受管精确版本资源→Native绑定/outbox→Host compose→现有连接器选择/资格/审批；不复制WorkBuddy运行程序或认证状态，不向Skill注入secret，不另建专家业务数据库。文件型研究状态/输出可在当前任务工作区保存，不能成为第二套会话/授权权威。

## 1. 跨境电商带货口播专家：可优先做有界真实接入

**真实核心**：不是普通“写口播文案”卡片；商品事实/图片→图文理解→恰好三套结构化方案→用户选择→对应视频创建→原taskId查询。真实生成复用已经接入的LinkFox proxy_call，不创建新HTTP客户端。源 `L/agents/linkfox-expert-aigc-videogen-sale.md:19-42`、`L/skills/linkfox-aigc-videogen-sale/SKILL.md:34-57,107-165`。

**明确缺口/必须修正**：

1. 原包反复说“脚本拒绝参数/执行下载”，但本专家资源只有MD/JSON/图片，没有其描述的口播业务脚本。必须在易界实现并测试本地方案/参数校验器，不能把自然语言描述当已实现代码；`SKILL.md:55-57,84-90,156-171`。
2. 模型文档互相矛盾：口播根Skill要求各模型 `voice=true`，并列HAPPY_HORSE；底层多图API表声明HAPPY_HORSE不支持voice，字段说明又说“仅SEED”而支持表还列SEED_FAST。根Skill允许SEED adaptive，但底层支持表只列16:9/9:16；两个文档默认比例也不同。证据 `sale/SKILL.md:72-105,149-155` 与 `videogen-multi/references/api.md:55-76`。首批限定现有审阅SEED/SEED_FAST子集，声音与比例按实际schema和明确选择；不能宣称WAN/HAPPY_HORSE均完成有声口播。
3. 图片不能证明功能/材质：`sale/references/prompt.md:14-36`鼓励从静态图“推导”工作原理、材质与卖点，应沿用现有XHS/跨境事实保真：用户确认事实、可见外观、未证实推断分栏，口播只消费已确认事实；禁止生成虚构功效/销量/促销承诺。
4. `prompt.md:76-84`把销售地区强制映射人种并排除面孔，不宜直接继承；演员外观设定由用户明确选择或采用中性描述，地区只决定语言/场景等已确认输入。
5. 原包只接受公开图片URL，不负责上传 (`sale/SKILL.md:118-123,195-199`)；它又要求最终只展示本地MP4 (`:167-171`)。易界现有复刻明确不下载，不能复用时假称已落盘；首批保留真实task状态/结果URL与交付限制。若要求本地MP4须另做受管产物下载，限制来源、类型、大小、重定向和目标目录，不能直接搬远程脚本。
6. 当前公开资料模型名称/费用/账户额度、实际音轨/口型和商品保真未验证；无账号在线部分NOT RUN。

**建议迁移**：新增独立专家ID与0.1.0 ROLE/knowledge，保留此前复刻原版本；最小知识只纳入四项能力所需参考。复用现有LinkFoxBroker、prepare/observe/任务ID方式；新本地帮助器负责三方案JSON、选中索引、制作单hash、事实来源与最终prompt组合，不绕过审批。需要新的业务任务不能冒用“查询已有任务”。

**正常验收**：无需账号可验证三方案→显式选择→构参；选项/原图/事实保留；同taskId查询；请求金额相关操作只有一次审批许可；普通成功/处理中/缺权限响应不重复创建；不同语言、5/10/15秒与声音参数一致；本地未下载明确为空。有独立LinkFox账号后再做一次真实文本任务+视频任务，人工查看口型、音轨、商品、事实，记录成本与taskId。

## 2. 股票研究专家：可接入用户资料/现有金融MCP研究，但须先修计算规范

**真实核心**：15个工作流（财报分析、首次覆盖、DCF、可比、memo、多空、事件、组合、模型更新等），不是15个外部工具。Agent职责 `E/agents/equity-research-expert.md:10-28`；声明清单 `E/.codebuddy-plugin/plugin.json:8-24`。多出的 `earnings-preview/SKILL.md:2-9`明确deprecated、disable=true、合并earnings-analysis，不能额外注册可用Skill。

**确定性问题**：`E/skills/dcf-model-builder/SKILL.md:42-45`先定义 `Kd=借款利率×(1-T)`，随后WACC债务项又乘 `(1-T)`，重复税盾。必须统一Kd税前/税后定义，在易界自有计算器与真实XLSX公式验算，不能仅改文字。另需WACC>g、币种/期间、稀释股数、净债务等输入完整性，缺失不默认零。

**数据/产物依赖**：

- `E/rules/equity_research_rules.md:21-29`写已连接金融MCP→agentic search→WebSearch；Bloomberg/FactSet/EDGAR只是来源例子，没有随包客户端/许可。易界内置web_search仍关闭，需复用当前金融MCP与LinkFox发现，实际原披露正文/时间戳支撑，不虚构“已使用Bloomberg”。
- 包内无实际计算程序或可执行commands目录；绝大部分为研究方法/模板，不能把prompt名称当自动工具。已有16份Skill中只有15有效，不应从旧行业研究员的“缺失note-writer”误推本包也缺这个命令。
- 完整首次覆盖要求6页签模型＋4估值页签＋25–35张图＋30–50页DOCX (`initiating-coverage/SKILL.md:12-18,49-115`)；现有研究员仅HTML/XLSX可比表，不能宣称已复用实现完整三表DCF或DOCX。应先实现能实际运行的最小研究/DCF/comps产物，再单列首次覆盖高级产物阶段。
- 所有数值来源/期间/最新披露需核实；默认90d陈旧标准不可代替实际市场/报表发布判断。评级要求与缺数据边界冲突时，优先报告证据不足、待评估，不强制凑Buy/Hold/Sell（Agent:46-60）。
- 原包没有清晰整包许可文件，开发者字段不等于可分发授权；先自有实现/记录来源、确认资源授权范围。

**建议迁移**：保持与现有“行业研究员”两个独立专家；复用其现有数据/搜索与证据模型，新增真正DCF/三表/敏感性本地计算与XLSX公式测试，不改旧专家精确版本。前期能力明示“用户财报/授权连接器数据→财报分析、可比/DCF、研究稿”；完整首次覆盖页数、图表、DOCX需单独产物门禁。

**正常验收**：一份合成且明确标记的多期三表输入，资产=负债+权益、现金流闭合、WACC只扣税一次、WACC≤g拒绝估值、缺股数不出每股价、负倍数NM、同币种同期间；模型更新保持旧源/新源可追踪。HTML/XLSX可打开、公式与独立计算一致；不得将这些当模型投资质量或真实金融账号验收。未来有账号才测实际schema、财报期、行情时点及证据归属。

## 3. 量化策略回测师：本地数据回测可行，原包取数及示例不能直接上线

**真实核心**：自然语言策略→Python+pandas→equity.csv/trades.csv/summary.json→离线HTML；覆盖规则、事件、多标的、组合再平衡，非分钟/tick/衍生品；见 `Q/agents/strategy-backtest-expert.md:15-39,61-70`。

**原包的优点**：规范明确次日执行、防前视、warmup与评估分离、A/H/US规则、费用、样本覆盖披露，事件研究不能套组合Sharpe；`quant-backtest-lab/SKILL.md:83-109,180-204,236-301,315-321,384-397`。但规范不是代码已实现证明。

**实际代码缺陷（静态确认，未执行）**：

1. `examples/ma_cross.py:144-168`、`examples/grid_trading.py:179-204`末日强平不检验 `entry_bar`/T+1，末日新开仓可当日平仓；正常交易路径虽有T+1检查，最后强平绕开它。迁移需末日禁止新增或保留未平仓并按期末估值，不能伪造已平仓。
2. MA例 `:89-101,149-161`、网格例 `:86-98,185-197`金额PnL扣佣金，但pnl_pct只用价格比，非净收益；输出定义需一致并分gross/net。例子无独立滑点/最低佣金/涨跌停不可成交建模，费用描述不能等价于真实交易成本。
3. MA例计算所有输入行指标并从头交易 (`:38-64,116-142`)，没有显式评估起日；配合要求提前加载warmup时，不能简单将整段输入交给例子后仅输出切片。`reference/common_pitfalls.md:25-40`本身要求warmup不得产生交易副作用。
4. `reference/export_results.py:224-239,388-400`用评估切片首个收盘权益作收益基数，丢失起点至首收盘变动（如果首日产生费用/持仓），需明确期初权益/前收盘基准。`:303-311`只在明确False时拒绝未平仓，`:347-365`只检验“权益变但无交易”，不是完整现金/成交账勾稽。不能称它自动保证回测正确。

**在线数据/运行阻塞**：

- WeStock是结构化行情/筛选主来源，NeoData只是文本补充，不能替代K线 (`Agent:31-41`)。两个WeStock index.js分别约3.35MB/2.35MB、3行、几十万 `_0x` 标识；缺可读源码/可复现构建/清楚许可与授权适配，不能放入Skill直接执行。
- NeoData `scripts/query.py:31-61,63-76,81-128,131-163`自动pip安装requests、读取/迁移明文token、通过腾讯WorkBuddy代理发请求；不能迁移认证文件或直接HTTP绕过Connectors。
- 现有Tushare只有单股单日未复权，不能当历史复权行情/历史成分/幸存者无偏全市场数据。可先支持用户授权CSV/明确来源数据文件；真实线上模式需确认现有金融MCP实际暴露历史序列、复权、停牌/退市、成分as-of、分红与币种；若新建WeStock/NeoData适配须走独立Connectors/Contracts资格流程。
- 原包自身某参考链接缺失：westock-tool/SKILL.md:303 指 `references/ai_usage_guide_workbuddy.md`，实际仅 `ai_usage_guide.md`，迁移索引要修正。

**建议迁移**：独立专家，以版本化自有本地回测核心＋数据来源契约＋可验证结果为第一阶段；本地策略范围严格限定而非宣称任何自然语言策略都正确。取数通过既有可用连接器或用户文件，遇不可用历史数据明确阻塞。历史成分、复权、数据发布时间、交易日历、手续费和滑点必须进入输入/结果；禁止用真实当前成分回放过去而不披露幸存偏差。

**正常验收**：普通合成价格序列/用户授权CSV，先独立手算5–10条交易；跨日信号、末日新买/T+1、warmup无交易、费用净收益、价格跳空、零交易、缺价、多个市场lot、数据覆盖不足、事件与组合指标分离。检查首末交易/现金权益勾稽并打开真实离线dashboard。无在线数据账号则数据覆盖与交易可执行性NOT RUN。

## 4. 行业研究专家-MOSS：方法与本地HTML可迁移，MOSS和多格式须分层资格

**真实核心**：边界/Plan→单一research_state证据台账→TAM/SAM/SOM/CAGR/集中度/评分/敏感性→冻结内容→交付清单与格式验收，默认HTML，可选DOCX/PDF/PPTX/XLSX。不是现有行业研究员简单换名。证据 `M/agents/moss-industry-research.md:124-145,186-216`、`skills/business-analysis-calculator/SKILL.md:42-135`。

**可复用外部边界**：易界已注册 `fanruan-growth-advisor`，可复用现有OAuth/generic-MCP/schema/逐次审批，不应新增SkillHTTP。原包 `M/../关联资源/fanruan-growth-advisor/市场副本参考/mcp.json:4-9`固定同一URL但额外 `X-Moss-WorkBuddy:1`；不是易界可直接冒用身份的依据。账号/独立客户端兼容性尚未验证。

**必要修订/阻塞**：

1. Agent `:39`规定任何请求（含澄清）均先MOSS授权；行业Skill `:224-227`则WebSearch主来源、MOSS补充。迁移必须明确：保留MOSS原体验时无资格应停；若支持用户资料离线行业研究，应标为易界明确的新能力，不能假称已调用MOSS。
2. MOSS `caller_expert`仅在当前schema有字段时传 (`Agent:29-35`)，不能捏造工具；`industry-research/SKILL.md:553-559`要求真实发现/查询与状态记录。现有内置web_search关闭，原ToolSearch/WebSearch/present_files/execute_python等宿主名要映射实际易界能力，不能保留不存在的工具承诺。
3. `skills/moss-ppt/templates`目录缺失。`references/executor-base.md:29,160`、`template-designer.md:221`、`template-compatibility.md:86`引用template_contract、charts_index、layouts_index、compatibility_manifest；不能据完整292文件归档宣称模板路线可运行。可补自有模板并独立验收，但不能伪造原模板通过。
4. **禁止原样启用Office shim**：`skills/moss-word/scripts/office/soffice.py:24-30,53-64,109-174`和同路径moss-ppt副本编译LD_PRELOAD库拦截socket/listen/close，遇边界阻断绕过，并在close `_exit(0)`。用户明确禁止此类运行时劫持；迁移排除此路径，用正常标准Office/LibreOffice运行，无法安全运行就标缺依赖。
5. **许可单独门槛**：`skills/moss-pdf/LICENSE.txt:13-27`明确限制提取/复制/衍生/分发；归档占有不代表迁移权。不能默认把整包PDF/文档组件打进易界，需授权范围核对或从获许可/自有实现重建。其他包无许可证不意味着开放许可。
6. 文档Python依赖多且无requirements锁，系统Office/字体/图片后端不随包。正式XLSX的 `execute_python` 是宿主机制 (`moss-xlsx/SKILL.md:36-59`)，DOCX/PDF/PPTX要真实生成并渲染，不能只通过扩展名检查。
7. `validate_frozen_package.py:7-20`校验结构、content哈希及选格式规格；`delivery_runner.py:43-57`再校验清单。它们不等价于事实正确/内容与所有产物语义一致；易界需实际生成回执和文件hash，不由模型自己标validation=pass。
8. 源跨专家转交列8位MOSS兄弟 (`Agent:84-108`)，易界未必安装，且用户不希望专家团。仅在真实已有专家中给建议，不自动启动团队或转发。

**建议分期**：MOSS连接器可用性与受控普通查询资格→研究+计算+自有HTML真实交付→可选DOCX/XLSX→正常Office PDF/PPTX。若未获取MOSS账号，本地材料模式可有独立验收，但MOSS数据能力仍NOT RUN；严禁拿既有行业研究员的数据来源冒充MOSS。

**正常验收**：市场边界/年份/单位/来源不混合，TAM≥SAM≥SOM前提明确，缺值不默认0，敏感性可重算；冻结后多格式用同一内容/证据版本，变更使相关分支失效；文件真实可打开且渲染完整，缺模板/Office时报告未完成，不采用shim。未来账号实测同一MOSS endpoint的OAuth/调用schema/caller字段/范围与来源回执。

## 5. WindAlice万得金融专家：不能通过现有wind MCP冒充原远程Agent，后置专项

**真实核心与区别**：`W/README.md:5,30-40`、`scripts/request.js:1`为 Alice A2A JSON-RPC SSE，`message/stream`、`tasks/get`、`tasks/resubscribe`，目标 `https://alice.wind.com.cn/Weaver/ChatAgent`、`alice-channel:Tencent.Workbuddy`。本地仅转发用户原话/管理任务/下载成果，真正工具、模型、Wind数据在远程Agent。现有易界wind远程MCP是不同协议/端点/认证，不等价替换。

**阻塞/具体代码问题**：

1. Agent `:66,84-101`要求Key写进agent_md记忆并命令行apikey-set；Skill `:206-241`写本地明文config.env。这与易界Connector Keyring/secret只在边界内冲突，必须独立受管认证，不能让Runtime读取Key。
2. `request.js:1` 的 `collectDownloadLinks`、`extractPresentFilesDownloads` 接受结果里的任意HTTP(S)文件URL（字符位置约33100–36400），`Zt`对每个URL附 `Authorization:Bearer <API key>`（约37126），下载调用约41257携Key。此处没有固定来源/主机检查，不能原样迁移；需要受控附件允许源、重定向策略、大小/类型/路径/会话归属和鉴权作用域，公共附件不转发API key。
3. `dataDir.js:1`、`sessionState.js:1`实际是cwd/temp/current-session.json（默认30min复用），Skill `:25`写cwd/.wind-alice路径；README:35/CLI帮助又声称必须显式contextId、默认全新。实际request代码默认调用resolveSessionContextId。易界多个会话可共用工作区，按cwd不够，必须以既有conversation/task/connection身份精确绑定，不能平行创建“共享全局会话”。
4. `tasksRegistry.js:1`存prompt预览/哈希、taskId/contextId、下载路径并自动清理日志/结果/锁（6小时等TTL）；导入会与易界历史保留/正常停止要求冲突。可为连接器异步外部任务保留必要私有映射，但必须方案评审、复用既有任务权威，不能整套CLI状态搬进Skill。
5. request代码普通SSE主路径有最多10次重连、attach失败自动新建分支 (`Y`/shouldFallbackToNew; char约79700–82400)，需要区分“恢复监听”与新的收费任务；易界不应遇未知状态自动再发付费创建。
6. `cli.mjs:2`支持detached子进程、60min内部轮询；不适合Skill自起脱管后台程序。必须经Connectors owner正常生命周期/取消流程；禁止因为源包建议而强杀/开启全权限。
7. Agent/Skill大量“正文逐字转发”“不得审阅附件”“present_files拆回合”是WorkBuddy专属UI约定（Skill:8-41），不应覆盖易界原始来源/不可信输出边界；远程报告保留署名/来源，不能冒充本地已核验结论。
8. 缺独立可读构建来源/许可/正式API说明；服务端付费/数据授权/业务调用还未验证。

**方案**：将其列为独立第三方Agent connector adapter评审，先确认官方A2A版本、易界客户端可用认证、费用、异步任务与产物协议，再在Connectors实现Keyring、固定目的地、审批、精确任务、结果归属、正常取消，不改专家架构。若临时只用现有wind MCP做数据研究，应另明确是易界本地Wind数据研究模式，不可称“WindAlice远程专家已接入”。

**正常验收条件**：普通本地协议stub验证提交/处理中/完成/取消与恢复监听；每次新收费任务必须fresh授权，无法判断状态不重复创建；两个会话同工作区不串context；正常附件固定源不泄密；无账号真实A2A任务、额度和数据能力NOT RUN。未具备官方协议/资格时不以UI占位冒充完成。

## 6. 美团生活助手：交易/授权/二进制专项，当前不宜直接原包迁移

**真实核心**：官方生产授权、发券、近期位置、餐饮团购搜索、选品下单、跳转支付；不是单纯推荐店铺。源 `T/agents/meituan-living-assistant.md:13-25`、`scripts/run.js:8-23`。外卖只领券，不支持外卖商品搜索/下单，源Skill:3。

**明确阻塞**：

1. 固定WorkBuddy身份：`run.js:38-40`client_id与WorkBuddy凭据路径；`run.js:1024-1044`clientSource=coupon-fusion-workbuddy，调用真实orderByAgent；Skill:185固定生产环境。缺正式适用于易界的客户端/API/授权scope/沙箱与交易资格，不可用原登录态试跑。
2. `run.js:281-285,294-304,338-353`会将真实token写stdout给模型，Skill:130-146要求读为USER_TOKEN。必须改为Connector私有Keyring或批准vault，仅返回状态/凭据引用，不能靠提示“别展示”保护。
3. `run.js:995-1044`只检查商品/店铺/城市/uuid存在后直接下单，未见绑定易界审批、金额/数量摘要、服务端幂等/未知结果恢复；Skill:600-639对话确认不替代机器边界。支付x402依赖WorkBuddy weixinpay插件探测（run.js:1007-1022、Skill:613-655），易界无该能力；“订单创建成功”不等于支付成功。
4. 包含 `@mtuser/pt-passport@1.1.0`（package.json:1-43），依赖 `@sec/cliguard@1.5.0`，配套六个平台原生二进制。cliguard package.json:4声明全HTTP签名与指纹守护进程；README:24-25说明自动patch和自升级。包中是分发后的混淆JS/二进制，不是可复现源码构建链；不能把它们当普通文档资源放入Skill直接启动，须官方SDK来源/许可/校验/更新/进程生命周期审计。
5. `run.js:200-242`init会npm安装tgz到专家包；违反易界受管资源不可变/运行不自动安装依赖约定。auth.py:27-39、run.js:40写外部WorkBuddy目录，必须排除。
6. Skill:358-372提自行cron与~/.config/meituan-huisheng状态，不能复制为第二套调度；若要日常领券，须另行限定既有定时任务支持的授权/失效/写操作范围，不默认开启。
7. 位置信息有静默近期位置、长期记忆授权与城市推断（Skill:424-454），迁移需用户当前授权范围和最少位置输入；不能把包内惯例当用户授权。
8. 发券当天缓存不是可靠账户级幂等（run.js:520-568按日期文件）；原业务平台幂等/账户隔离仍待查。`run.js:1133-1141`即使runPassport返回非0也把cli_cleared设true，是退出成功误报，需要改真实状态，不能测试强杀。

**方案**：与WindAlice分开，先专门审查美团Connector官方授权、只读搜索/定位scope，再发券写操作，最后订单/支付（支付可先留用户在美团完成）。每阶段都有真实功能边界与审批/去重/错误状态，不发布只有卡片的“已接入”标志；除非取得可用官方协议与可审计SDK，否则保留未接入并列阻塞。

**正常验收条件**：普通本地协议stub验证只读范围、匿名/缺授权不调用、用户确认的城市/位置、发券和订单fresh审批/重复请求只产生一个业务效果、超时unknown不重发、商品/价格/数量变更使旧审批失效、支付状态独立。所有真账号授权/生产领券/下单/支付继续NOT RUN；不能拿缓存或UI展示作通过。

## 跨这6位的分组建议（供总方案合并）

1. **优先：口播**。已存在LinkFox传输/审批/async基础，新增有界本地编排＋事实保真＋方案选择即可形成真实链路；在线无账号清楚跳过，不自加上传下载承诺。
2. **金融本地组：股票研究＋量化回测**。共享数据来源/时间口径/结果产物基础，但分别解决WACC错误和回测执行偏差；先用户资料/合成可计算回归再授权金融工具。不能以“无账号”跳过本地计算和真实性边界。
3. **MOSS组**。复用现有MOSS connector，但独立资格与文档/模板/许可问题大；先行业方法/计算/HTML，源MOSS和Office产物能力分别验收。
4. **专门适配后置：WindAlice；美团**。两个都不是现有generic MCP直接可消费的原包；各走正式Connectors/Contracts设计，单独认证、异步/交易状态、附件/二进制/许可与正常生命周期。不能把拦路问题压成“以后有账号再测”后先上线原CLI。

新增工程保持已接入11专家ID/14版本与历史绑定不变，新增版本/资源候选而非原位替换；采用原full lint、来源锁、确定性打包、安装/绑定/权限测试、数据库/历史资源保全及canonical构建流程。每组报告区分“本地真实计算/产物PASS”“连接器代码/普通协议PASS”“账号线上NOT RUN”“未实现能力”，不把结构eval或合成MCP成功当线上业务证明。
