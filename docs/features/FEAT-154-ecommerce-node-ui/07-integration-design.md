# FEAT-154 第 1 步：接入方案定稿

> 2026-09-15 · D0 产品/UX 确认及机器门禁均通过 · 第 1 步完成，尚未开始第 2 步

## 1. 本轮结果与用户已确认边界

本轮用户授权执行计划第1步：明确类型/目录/实例、核对草稿隔离/重连/离开、确定字段组与控件，形成具体改动清单、交互方案与契约影响结论。当前仅修改本需求包、生成审阅用交互示意；没有修改业务代码、生成跨仓契约、构建工作流产物或启停App/服务。

用户随后明确选择：**“保持纯前端范围：页面离开确认，关闭应用不保证保留（推荐）”。** 此项已确认，不再询问；当前原生应用确无CloseRequested/ExitRequested保护，先前稿件把“正常关闭保护”作为既有能力的假设已经纠正。

| 项目 | 定稿 |
|---|---|
| 全量范围 | 30种节点、634顶层字段行，输入/业务配置/输出；处理逻辑、业务结果和错误码排除 |
| 载体 | 当前真正的同窗口Coze WorkflowPlayground；复用官方面板、卡片壳、表单和侧栏 |
| 生命周期 | 同一页面内存保存配置；应用内离开确认；关闭窗口、退出App、刷新/重启不保证保留 |
| 电商执行 | 不发送电商图、不保存、不试运行、不内部发布，不调用业务/模型/媒体接口 |
| 原有功能 | 原三节点的可执行图和历史版本保持；历史是同页modal，可继续明确执行原已发布版本 |
| 契约 | 未来实施整体semantic；既有dirty保护语义扩大并明确，无新wire字段/kind/native命令 |
| 当前资格 | 设计可审阅；D0 Owner确认及机器门禁均PASS，见02；真实实现/产品验证/D4全部NOT RUN |

具体附件：[08注册与文件改动](08-node-registration-design.md)、[09字段控件](09-field-control-design.md)、[10生命周期与契约](10-lifecycle-contract-design.md)。本文件与这三份附件是第1步当前权威；00/03/05中较早候选以本次明确结论收敛。

## 2. 类型、目录与实例

- **渲染类型**：`yijie-ecommerce-ui`。只在带localAdapter的前端注册；StandardNodeType数字枚举、Coze IDL、API和执行引擎不增加此值。
- **目录标识**：`ecommerce-01`至`ecommerce-30`，逐项绑定04的原始编号与名称。中文名或目录分组变动不重新分配ID。
- **实例标识**：每次添加调用已有`WorkflowNodesService.createUniqID()`，使用其碰撞检查；不拿catalogId或编号作实例ID。初始值深复制，数组行使用本地rowId，多个同类节点不串值。
- **模板存储**：保留标准节点按type存储的Map；电商另有按catalogId索引的只读目录，在同一个官方NodePanel中组成五组。卡片/表单从实例catalogId查定义。
- **进程内类型**：增加`EditorNodeType = StandardNodeType | 'yijie-ecommerce-ui'`及本地模板联合；不强转为Text，不在全局标准节点枚举中加执行类型。
- **节点数据**：`nodeMeta`加私有`ui`（catalogId、内部结构版本、输入/配置填写状态），只存在renderer。输出定义来自目录，不存业务输出值。没给inner key的字段值保存在UI slot，不拼造业务对象。
- **创建路径**：点击为Must；可沿用的拖动添加也走同一实例工厂，拖动取消不创建。禁止复制入口，通过重复添加满足多实例；原节点的复制/数量限制保持。
- **端口**：本期电商registry不注册真实可连线端口；在原生ports.tsx中增加纯装饰分支，无data-port-id、点击/键盘/连线回调，只保留外观。字段引用在本页可用输出定义中选择，不求值、不构造执行链；原三节点连线规则保持。

metadata查找必须带catalogId：现有格式化按type重写图标/副标题，submit阶段又按nodeDTOType重写type。电商使用自己的UI registry与格式化分支，不借用type15；普通DTO↔VO转换不进入私有ui字段。08列出了具体接入点。

## 3. 状态、恢复与操作规则

### 3.1 两类状态的所有权

`DraftModel`继续只持有原三节点可提交图、名称、revision、baseline、dirty、conflict和回执。新增同iframe的`EcommerceUiDraftModel`持有设计active、完整UI图、设计名称、实例/字段值、本地documentEpoch与待核对的远端快照。

首次添加之前：当前基线已载入且连接就绪，无在途写入/重连/冲突/未知回执；可带着普通未保存草稿进入，不自动保存。同步捕获当前可见三节点图及原名称、dirty等后开启设计；添加取消/失败且图未改变则不留下空设计状态。后续所有normalize/change/changeName、位置/字段/增删/撤销只落在设计副本。

原`canvas-data.ts`和`DraftModel`的可提交校验不放宽。设计存续时保存、快捷键/自动保存、内部发布继续保留提交保护。试运行入口保持可点击，纯前端展示“暂未接入试运行”提示；实际执行action不调用接口，不生成运行结果。禁止过滤新节点后悄悄提交旧图。

### 3.2 保护位和明确退出

`protectedDirty = design.active || model.dirty || unresolvedEditorOperation`，用于当前页面的离开保护。`canSave/canTest/canPublish`独立于保护位判断，设计active时固定false；canTest表示实际执行资格，不用于禁用电商试运行展示入口。关闭侧栏、删最后节点、撤销首次添加都不能自动解禁。

“恢复原草稿”是一个明确的本页动作：提示将放弃本次设计；取消保持，确认后先冻结编辑并递增documentEpoch，保留原稿与设计快照，启动受控reload；只在当前epoch的reload及normalize成功后结束active、清理设计并恢复原图/名称/未保存状态。失败时保留design与保护位，继续阻止写入，提示重试恢复或明确离开。原生HistoryService已有`stop/clear/start`，进入/恢复时隔离撤销栈，避免恢复后撤销又带回电商节点。**保证原稿内容与未保存状态，不承诺恢复进入设计前的撤销历史。** 正常模式编辑不因本期批量清理撤销栈。

documentEpoch只在主动文档切换时递增，不混用server revision、不进入MessageChannel。SaveService据epoch执行受控reload，并核对mounted generation/epoch，清除选择及连接中的临时状态；普通字段变化不触发全图重载。

### 3.3 重连与远端变化

- 原iframe不卸载。断开/重连/bootstrap/主动替换期间只读，仍可查看配置和走页面离开流程。
- 同revision恢复只恢复编辑能力，保留设计图、字段、选择；重新投影当前保护位，不显示“配置已保存”。
- 不同revision时，在新模型中保存远端快照/变化提示，冻结设计编辑；不把远端喂进原模型导致clean基线自动替换，不merge或改写原baseRevision。
- 明确恢复原草稿时仍保留远端变化标记，canSave/canTest/canPublish保持受阻。恢复后选择继续保留原内容，或明确放弃本地内容、重载最新草稿；后者需创建新的候选DraftModel并调用其receive(remote)验证，不能对原dirty模型直接receive（它会拒绝）。main将provider模型保存在可替换的modelRef，稳定adapter在操作边界读取current；候选验证/当前epoch的原生reload与normalize全部成功，才原子切换modelRef并清理pendingRemote/旧快照。失败保留旧模型和快照、继续阻写。只允许在无在途或未知写回执且用户明确放弃时执行；旧回调依generation/epoch失效。原草稿已有dirty时不能自动接受新revision。
- 旧异步结果须符合原operation ticket、bridge generation与当前documentEpoch，才能影响对应状态；未知回执按原ID查询，不自动重发。

### 3.4 动作矩阵

| 动作 | 定稿行为 |
|---|---|
| 关面板、关侧栏、切节点 | 保留各实例字段/展开状态，不结束设计 |
| 返回工作流、宿主侧栏导航、路由参数改变 | 原路由guard统一确认；取消保持路由与内容 |
| 错误页/重连遮罩返回 | 同一宿主确认路径，不提前丢弃iframe |
| 确认页面离开 | 明确放弃本页所有未保存内容及查询入口；不自动保存/取消远端操作；native.close失败保留页面 |
| 恢复原草稿 | 只放弃设计副本，保留进入时原草稿及其未保存修改；与“离开页面丢全部本地内容”分开 |
| 历史按钮/关闭历史面板 | 同页开关modal，设计图不卸载、不reload |
| 历史里运行旧内部版本 | 保留原能力，只发送选定服务端版本，不携带设计图；不把designDirty当作history busy |
| 原会话到期/显式重连 | 保留内存设计，同/异revision按前述规则处理 |
| 关闭窗口、Cmd-Q、退出App、刷新/重启 | 用户已选择不保证保留；不新增native guard。入口常驻说明该限制 |

## 4. 目录、字段分组与控件

五组固定为商品准备与选品1–8、Listing与搜索优化9–16、图片与视频17–22、合规与发布23–26、店铺运营27–30。分组仅供查找，不表达执行顺序。

侧栏采用原生标题/关闭及输入、业务配置、输出三层；输入下按卖家对象再分小组。必填字段可发现，辅助资料折叠；打开/关闭分组按实例保留。原变量键作为辅助字段信息可查看，中文标签为主。

- 1–8独立业务配置沿用原“建议默认值”；文字“当前版本/按策略/必须指定”不能假填成有效引用。
- 9–30配置对象在业务配置区展示，仍对应原输入路径。上层object必填不代表所有子项必填。
- 明确枚举用选择控件；未穷举用可编辑文本/标签。条件必填显示完整条件，只有直接可知的模式改变提示，不检测商品/授权或执行门禁。
- object有机器子键则保留；只有中文子项则用`uiSlotId + sourcePhrase`的小表单；完全缺结构时提供本地引用/内容说明，不以JSON大框为唯一入口，不生成业务Schema。
- unset、false、0、空字符串、显式空数组区分；清除回unset，不凭truthiness恢复默认。缺初值的boolean为“未选择/是/否”。数字格式问题保留编辑文本并就地提示，不执行业务计算。
- 所有输出只读字段树/说明；status/审核/结果等为可能字段定义，无当前值、通过标记、图片或运行进度。

### 三个代表节点

| 节点 | 定稿分组与关键交互 | 详细映射 |
|---|---|---|
| 01 商品采集 | 商品来源可增删卡；商品补充资料；采集设置/更多设置；4输出。6配置建议初值保留，可选false不重置 | 09第2节，13顶层字段 |
| 10 Listing一键优化 | 商品与目标、基线与依据、品牌素材、已有内容组件；业务配置顶部明确选择full_generate/assemble_only，模式初始为空；四组件槽可展开且切换保留 | 09第3节，26顶层字段 |
| 17 商品图片生成 | 商品与素材、品牌权利；图片需求/生成设置；素材列表仅引用，比例/模型/时长均不猜默认；variant_scope保持字符串列表 | 09第4节，18顶层字段 |

静态交互示意展示这3个代表节点的面板/卡片/控件及页面离开确认，当前采用方案已固定的青柠和画布色；示意的简化字段不替代09的全量57行映射。全30仍以04的634行追踪。示意不是Coze产品实现，不能当作真实App、组件集成或D4证据。

## 5. 明确的契约影响结论

**未来整体 `contract-impact=semantic`；本轮文档/设计实际改动 `none`。**

已有dirty原本就包含model.dirty与runs.pending；schema只有boolean，说明未明确覆盖不可保存设计内容。将其定义为“离开会失去的本地内容或查询上下文”，并明确它不代表可保存/可执行/业务终态/原生退出保护。所有现有直接consumer只使用该位决定页面确认，无自动保存，故已完成的方向性源码核对支持semantic，未发现需要新字段或kind。

具体源文字和双向兼容矩阵见10第5节。后续拟采用 **1.4.0-local-candidate** 标识新的语义候选；当前仍为1.3.0-local-candidate。本稿不创建tag、不声称源已生成或发布。OpenAPI的info.version只作为同族候选元数据更新，HTTP paths/DTO/认证/资源/执行约束不改。

后续顺序：Contracts描述/说明/候选版本及适用普通示例→canonical生成和聚焦检查→Desktop确认文案/consumer核对→Coze设计状态/producer→三个consumer同源锁同步与本地资格。source.lock被API/Coze/构建来源链共同消费，必要的自动派生/摘要变化列入清单；不等于新增API行为。禁止手改生成物或保留错误pin。

必须保持：旧Coze→新Desktop、新Coze→当前配套Desktop均能读取相同boolean；dirty不得变成自动save或history忙碌；原1.2 Desktop不支持1.3 request_history的既有边界不扩大。若实施过程中新增kind、改变运行/保存解释或破坏任何支持交互，重新分级，不以本稿semantic掩盖breaking。

## 6. 具体改动清单（后续实施，本轮未改）

| 仓库/模块 | 具体文件或范围 | 变更内容 |
|---|---|---|
| Coze前端类型 | base/src/types/local-editor-node-type.ts（新）、types/registry.ts、相应index | 命名空间UI类型及进程内联合，标准enum不动 |
| Coze目录/工厂/共用UI | playground/src/local-ecommerce/{types,catalog,create-node,node-registry,node-content,form-meta,form,field-control,reference-picker}（新） | 目录按catalogId、独立实例/rowId、字段源追踪、原生表单和卡片内容 |
| Coze注册/metadata | workflow-playground-context.ts、workflow-nodes-v2-contribution.ts、nodes-v2/utils.ts、use-default-node-meta.ts；nodes/typings/playground-context.ts、workflow-json-format.ts、utils/add-node-data.ts | 仅local追加registry，metadata带catalogId，保全UI类型和私有字段 |
| Coze面板/添加 | node-panel的use-template-node-list/use-search-node/panel/custom-drag-card/atom-node-list/atom-category-list；utils/node-template.ts、typing/index.ts；toolbar/use-add-node、workflow-edit-service、workflow-drag-service | 官方面板复用，catalog稳定key；点击/拖动共用工厂，本地搜索不联网 |
| Coze卡片/表单 | node-render-new/content/index.tsx、node-render-new/ports.tsx（电商装饰端口）；既有NodeSideSheet/NodeConfigForm/Section/OutputsParamDisplay按需复用 | 共用卡片内容分支、按node.id表单、可访问中文控件；不把未定义对象送入业务变量服务 |
| Coze设计状态 | workflow-local/src/ecommerce-ui-draft-model.ts（新）、main.tsx；playground/typing/local-workflow-adapter.ts、local-workflow-document.ts、workflow-save-service.ts、必要keyboard UI分支 | 内存副本、保护位、动作guard、documentEpoch、只读/重连、原稿恢复/显式放弃的候选模型切换、撤销栈隔离 |
| Coze治理 | yijie-upstream.lock.json、workflow-editor.mjs精确闭包清单（必要时） | 按真实触达登记源，不改Rush依赖锁或升级库 |
| Contracts | jsonschema/workflow-editor/bridge-v1.schema.json、docs/workflow-local-v1.md、openapi/workflow-local/workflow-local.yaml的info.version、同族正常示例/聚焦检查 | semantic文字、版本候选；无新业务接口/事件形状 |
| Contracts派生与3消费者 | canonical generate-workflow-local/sync-workflow-consumer输出、source.lock、API/Coze/Desktop各自workflow-local.lock及实际消费副本 | 同源自动同步，见10；API业务代码和HTTP语义不改 |
| Desktop UI | WorkflowLocalWorkspace.vue及其正常consumer测试；channel/EditorPane只在适用测试核对 | 确认文案覆盖全部本页内容；dirty不触发保存/禁历史；Rust/native/capability/CSP不变 |
| 元仓 | 当前需求包 | D0实际确认、分项结果、后续验收与限制 |

Coze表内缩写均相对`frontend/packages/workflow/`下对应package，逐项完整路径见08。新文件名为定稿落点，实际因正常类型传播需触达其他前端签名时登记差异；不得扩展业务/权限。保留canvas-data.ts和draft-model.ts的可提交图含义，原数据、历史、用户未提交主题保持。

## 7. 验证设计与未执行项

本次已做原文与源码阅读、消费者方向性复核、交互示意的正常浏览器检查。示意检查覆盖同类实例独立、false保留、模式初始空值/切换保留、搜索空态恢复、取消离开和浅暗/窄幅布局；只证明设计示意自身可用。

后续产品必须额外核对：01/10/17实际原生集成、全部30节点/634字段、UI状态保留/实例不串值、被删引用提示、自然到期同/异revision、不发新图、恢复同revision、原未保存草稿保护、history不卸载且原版本执行仍有效、正常页面离开取消/关闭失败保留、四主题尺寸组合。普通输入/自然生命周期/现有正常测试可使用；不强杀、不注入权限或攻击故障。

本轮Contract源生成/同步、工作流构建、App启动/停止、节点业务/模型/API/媒体操作全部NOT RUN。应用退出确认为用户明确排除能力，不列产品通过项。

## 8. D0确认记录

- 方案编制：Codex；源码/字段独立复核：三个协作子任务，不冒称人工Reviewer。
- 已确认产品边界：段成威在本轮选择纯前端、页面离开确认、App关闭不保证保留。
- 完整D0方案确认：**PASS**。段成威在本轮明确回复“确认这份方案”，确认此前已展示的本文件及08/09/10、交互示意；确认前资料SHA-256逐项相等，记录见[evidence](evidence/step1-design-20260915/d0-owner-confirmation.json)。
- 机器检查：结构/一致性、元仓50项正常测试和静态示意检查已通过，见02。D0机器门禁已执行并PASS，退出0，实际输出及输入摘要见02与d0-gate.json。第1步完成，第2步功能实现不自动开始。

已按元仓AGENTS及项目协作规范记录实际D0确认，不重复索取同一批准；确认不包含第2步实施、提交/推送、业务调用或发布。
