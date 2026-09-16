# FEAT-154 步骤 1：注册、模板与原生组件接入设计

调查日期：2026-09-15。只读核对；未实现、构建、启动或修改仓库。以下以 `/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-coze/` 为源码路径基准。

当前权威决策见[07接入定稿](07-integration-design.md)。本文为其注册细节附件；所有文件列为后续实施清单，本次未修改业务代码。

## 一、选定方案

采用 **一个前端电商 UI 类型、30 个不可变目录 ID、每次添加独立实例 ID**。仅有 `localAdapter` 的 WorkflowPlayground 注册此 UI 类型；上游 NODES_V2、StandardNodeType 枚举、Coze IDL、归一化 wire Canvas、后端引擎白名单都不增加电商执行类型。

- 类型：`ECOMMERCE_UI_NODE_TYPE = 'yijie-ecommerce-ui'`。它是编辑器渲染/表单分发标识，不是业务节点/DTO 类型编号。
- 目录：`ecommerce-01` … `ecommerce-30`，与目录 04 的编号一一绑定，之后不随中文名称、分组变化而重新分配。它决定原名、图标、字段组、控件、默认值及只读输出说明。
- 实例：使用已存在的 `WorkflowNodesService.createUniqID()` 在创建时分配 ID，碰撞会检查当前 EntityManager。模板不得固化 ID，同一目录可重复添加。初始化需要深拷贝默认值，数组行亦分配稳定的本地 rowId，不共享可变对象。实例名称复用 `createUniqTitle()`，如“商品采集”“商品采集_1”；目录原名另外保留。
- 私有节点 data：`{ nodeMeta, ui: { catalogId, schemaVersion: 1, inputs, settings } }`。`inputs`/`settings` 按原字段机器名存储前端值，节点 9–30 没有原独立业务配置节的字段仍保留输入对象身份。只读 output definitions 从 catalog 派生；不存放 output result。
- `ui` 与任何 UI 连线只存在当前 iframe 的内存 UI draft。现有 `DraftModel.canvas` 始终只包含原受限三节点图。原公共保存/试运行/发布不接受复合 UI document，不允许靠提交前删掉电商节点来静默保存剩余图。

### 30 个目录 ID

| catalogId | 名称 |
|---|---|
| ecommerce-01 | 商品采集 |
| ecommerce-02 | 商品信息清洗与标准化 |
| ecommerce-03 | 类目与属性智能匹配 |
| ecommerce-04 | SKU／变体结构重建 |
| ecommerce-05 | 选品机会评估 |
| ecommerce-06 | 竞品商品采集 |
| ecommerce-07 | 竞品对标分析 |
| ecommerce-08 | 成本利润与定价测算 |
| ecommerce-09 | Listing 综合诊断 |
| ecommerce-10 | Listing 一键优化 |
| ecommerce-11 | SEO 关键词挖掘 |
| ecommerce-12 | 商品标题优化 |
| ecommerce-13 | 核心卖点／五点描述生成 |
| ecommerce-14 | 商品详情描述／A+ 内容生成 |
| ecommerce-15 | 多语言翻译与本地化 |
| ecommerce-16 | 规格名称与变体文案优化 |
| ecommerce-17 | 商品图片生成 |
| ecommerce-18 | 商品图片处理与平台适配 |
| ecommerce-19 | 图片文案翻译与重绘 |
| ecommerce-20 | 商品视频脚本生成 |
| ecommerce-21 | 商品短视频生成 |
| ecommerce-22 | 视频字幕、配音与本地化 |
| ecommerce-23 | 商品合规判断 |
| ecommerce-24 | 知识产权与品牌侵权风险检查 |
| ecommerce-25 | Listing 全素材合规审核 |
| ecommerce-26 | 商品发布与上架校验 |
| ecommerce-27 | 库存与履约风险监控 |
| ecommerce-28 | 评论与差评洞察 |
| ecommerce-29 | 客服回复生成 |
| ecommerce-30 | 广告与流量投放优化 |

目录来源：元仓 `docs/features/FEAT-154-ecommerce-node-ui/04-node-ui-catalog.md:33–64`。

## 二、现状与必须调整的位置

### 1. 不能把目录 ID 放进 StandardNodeType 或 type-keyed 模板 map

`frontend/packages/workflow/base/src/types/node-type.ts:20–107` 中 StandardNodeType 是现有上游数字字符串枚举。`frontend/packages/workflow/playground/src/workflow-playground-context.ts:84` 的 nodeTemplateMap 为 `Map<StandardNodeType, NodeTemplate>`，本地加载 `123–135` 只设三节点、以 type 作键，类别只含 Text。30 个同类型模板放进去只会剩最后一项。

定稿：保留标准 map；增加进程内 `localEcommerceCatalog: ReadonlyMap<CatalogId, Definition>` 和按分组/目录顺序组织的 `getLocalTemplateCategoryList()`，直接返回同一 NodePanel 的本地类别。电商模板为独立 discriminated union：`LocalEcommerceNodeTemplate { type: ECOMMERCE_UI_NODE_TYPE; catalogId; name; desc; icon_url; ... }`，不复用从服务端模板继承的 NodeTemplate DTO。列表 React key、data-testid 使用 catalogId（当前 atom-node-list.tsx:69/atom-category-list/index.tsx:43 的 type+name 不够稳定）。

`use-template-node-list.ts:61–72` 本地路径目前再滤成唯一 Text；改为原基础类 + 五个目录分组，Text 的唯一限制仍在。`use-search-node.ts:61–99` 已能做本地名称/说明匹配，`111/142` 已阻断后端搜索；增加本地模板 discriminator/编号/变量别名词，不解除后端阻断。`utils/node-template.ts:45–50` 的 isNodeTemplate 目前以排除法把一切非插件当标准模板，须加独立本地判断，避免误缩窄为服务端模板。

### 2. TypeScript 扩展是编辑器类型，不伪装 StandardNodeType

新建 base 私有前端类型导出 `LocalEditorNodeType` / `EditorNodeType = StandardNodeType | LocalEditorNodeType`；StandardNodeType 本体及 Object.values(StandardNodeType) 的上游请求不变。

最低需调整内部签名：

- `base/src/types/registry.ts:60` 的 `NodeMeta.nodeDTOType` 当前强制 StandardNodeType。应允许 EditorNodeType；电商 registry 此值仍是 `yijie-ecommerce-ui`，绝不能借用 `15`。
- `playground/src/typing/index.ts:96–108` 增加 LocalEcommerceNodeTemplate 联合，DragObject.nodeType 用 EditorNodeType；现有 ServerNodeTemplate 和业务 DTO 保持原类型。
- `playground/src/components/node-panel/components/panel.tsx:74`、`custom-drag-card.tsx:44`、`services/workflow-edit-service.ts:79`、`services/workflow-drag-service.ts:43/50/143` 及相关纯 UI 添加/拖动参数改成 EditorNodeType。不要以 `as StandardNodeType` 强转电商类型。
- `nodes/src/typings/playground-context.ts:40–42` 与 playground context 的模板元信息查询增加可选 catalogId/node 数据参数，仅本地分支识别；标准路径仍按 type 查询。
- `nodes-v2/utils.ts:23–30` 的 registry/type 判断增加此类型的只读查询分支；不要直接把电商 registry append 到面向所有场景的 NODES_V2（constants.ts:70–119）。

这是库内 TypeScript/进程内接口，非 yijie-contracts 公共 node enum、HTTP/event payload 或持久化 wire 增量。

### 3. 节点注册及实例创建

`container/workflow-nodes-v2-contribution.ts:45–58` 当前本地只注册 1/15/2，且所有节点禁止复制、单测、编辑头。定稿：保留原三节点注册逻辑，`localAdapter` 存在时追加一个 LOCAL_ECOMMERCE_NODE_REGISTRY。meta保留官方卡片尺寸/标题组件、copyDisable；电商节点的原生试运行位置渲染可点击的纯前端提示按钮，与上游真实执行组件隔离；电商不注册真实端口，并允许删除；电商标题可用唯一默认名，目录原名不可编辑。初期不新增复制入口，重复添加满足多实例。

`LocalWorkflowDocument.createWorkflowNode()` (`services/local-workflow-document.ts:20–40`) 当前拒绝未知 type、同类第二实例和 clone，开始结束固定 ID；这里增加只针对电商 UI 的分支，核验 catalogId 存在、实例 ID 唯一、无 blocks/嵌套文档，并允许同 catalog 多实例；原 1/15/2 规则原样保留。`updateEndBinding()` (`42–53`) 只继续管理 Text→End，不给电商节点修改 End 的机会。

`NodePanel.handleSelectNode()` (`components/node-panel/components/panel.tsx:140–150`) 当前直接克隆固定 Text 模板；改为使用 `createLocalEcommerceNode(catalogId, nodesService)` 工厂，每次建立新实例和独立 defaults。点击与拖动必须共用这个工厂，不能只修点击：`CustomDragCard` (`74–112`) 的 drag item 目前传静态 nodeJson；需让本地拖动在新建时调用工厂，拖动取消不加入 document。`use-add-node.ts:193` 的 canAddNode 也须允许本地电商类型，Text 仍唯一。

### 4. 官方卡片/侧栏不是只注册 form 就够了

侧栏已正确 `NodeContextProvider key={node.id}` (`components/node-side-sheet/index.tsx:159–163`)；NodeRender 读取各节点 FlowNodeFormData (`150–155/196`)，删除节点会关闭侧栏 (`132–138`)。保持此机制，不建按 catalogId 共享的 React state。

共用电商 form-meta 用 FormMetaV2 + 每实例 FormModel；render 读取 node.ui.catalogId 的定义。表单使用 `NodeConfigForm`（node-registries/common/components/node-config-form.tsx:40–65）提供的官方 Header、Form、只读支持，结合官方输入、分组折叠、列表与帮助组件。onChange 更新本实例 FormModel；业务算法、API fetch、模型选择查询或上传回调均没有注册。

原卡片为 `NodeRenderNew`（components/node-render/node-render-new/index.tsx:41–90）；ContentMap 按 type 分发，未认识的类型退回 CommonContent（content/index.tsx:58–106）。增加一个电商 content 分支，复用其 Wrapper/Header/Field/Tag 组件，按照 catalog 定义和实例已填状态显示输入/输出摘要；输出摘要是字段名称+类型，不显示运行结果。

### 5. 本地序列化及 metadata 是两处隐蔽接入点

`nodes/src/workflow-json-format.ts:156–187` 格式化会按 type 覆盖 icon/subTitle，`220–262` 提交会强制 `json.type = String(nodeDTOType || json.type)`。如果只套 Text registry，电商 UI 节点会变成 type 15 并显示 Text 图标；这必须显式解决。

定稿：电商 form 的 `formatOnInit`/`formatOnSubmit` 成对保存 `nodeMeta` 和 `ui`，业务值/引用/数组顺序不变。`variablesMeta: { inputsPathList: [], outputsPathList: [] }` 使通用 DTO/VO 转换不侵入 ui 字段；本地字段引用选择与只读输出结构从私有 catalog/UI draft 派生，不注册为标准三节点可消费的引擎变量。卡片摘要用独立纯展示 content，不误用需要引擎变量实体的 CommonContent。

模板 metadata 查找增加 catalogId 上下文；`workflow-json-format.ts:172` 传入节点 data.ui.catalogId，`nodes/src/utils/add-node-data.ts:37–49` / `playground/src/nodes-v2/hooks/use-default-node-meta.ts:33–45` 对已注册电商实例调用对应定义，在 form 初始化后补全本实例 NodeData；不可用一个 generic type lookup 给全部实例盖同一图标。字段值以及实例 title 不被初始化重新置为默认。

`LocalWorkflowDocument.localDocumentJSON()` (`62–78`) 可继续只做 Text 特例；它只是进程内视图快照，不能视为可持久化 payload。`localDocumentKey()` (`services/local-workflow-document-key.ts:5–17`) 已保留全部作者字段、嵌套数组顺序，适合 UI draft 内的等值比较。

## 三、与 adapter / 草稿逻辑的准确分工

`frontend/apps/workflow-local/src/main.tsx:298` 当前 snapshot document 始终 decode(model.canvas)；`320/325` normalize/change 始终经原三节点 decode；所以 UI 类型会在当前入口抛错。不能放宽 `canvas-data.ts:9–25`（2–3 nodes、1/15/2、最多2边）并把新图交给 DraftModel。

增加 `EcommerceUiDraftModel`，在 main 的 stable adapter 前投影内存视图：

1. 原 DraftModel 保存服务端可执行三节点基线与原未保存改动，capture、uncertain、CAS 仍原样。
2. 首次添加前先捕获完整三节点状态并深拷贝，开启design.active后才调用实例工厂和原生添加；取消或失败且无新增图变更则恢复先前模式。后续 `change(document)` 发给 EcommerceUiDraftModel；不调用 model.canvas 赋值。
3. `snapshot.document` 在 UI 活跃时返回此内存视图；`dirty` 为原 model.dirty OR UI未放弃状态，并持续复用既有 dirty bridge 通知。
4. UI 活跃时 canSave/canTest/canPublish（实际执行资格）全 false；save/test/publish 实际函数入口也不提交。试运行展示入口保持可点击，只显示未接入提示，不调用接口、不产生模拟结果。这里没有“自动滤掉 UI 节点再保存”的降级行为。
5. UI 模式内对基础节点/连接/位置的变更也属于 UI 视图，放弃 UI 时恢复进入前的基础草稿。UI 草稿存在时，bootstrap/read 返回不同 revision 也不能覆盖画布，需保留并标明冲突；不能只依赖 DraftModel.dirty（它看不到 UI）。
6. 需显式 `documentEpoch` 或等效本地快照标识驱动进入/放弃后的 native reload：`workflow-save-service.ts:695` 当前只在 `!next.dirty && next.revision !== localRevision` 时重载；单改 snapshot.document 不能保证放弃 UI 后恢复，同一远端 revision 也必须触发进程内视图切换。此字段仅 LocalWorkflowSnapshot 使用，不进 MessageChannel。
7. 初次 normalize、onContentChange、重连订阅使用相同分流和 UI document 验证（workflow-save-service.ts:681–711）。原 `DraftModel.normalize` 的 meaning 比对（draft-model.ts:30–35）仍仅用于原三节点图；新增 `uiDocumentMeaning` 必须覆盖 catalogId、值、引用、位置、边，不能“清洁化”吞掉输入。

生命周期与离开选择已在07和10定稿；用户已选择纯前端，关闭App不保证保留。关键判据：`canvas-data.ts`/`draft-model.ts` 的可执行图校验不放宽；任何 UI event 都不能触发新的 bridge operation。

## 四、建议实施文件清单（此轮只记录，不修改）

### 新增文件

- `frontend/packages/workflow/base/src/types/local-editor-node-type.ts`：唯一命名空间 UI type + EditorNodeType 联合，仅前端。
- `frontend/packages/workflow/playground/src/local-ecommerce/catalog.ts`：30 定义、目录 ID、分组及只读来源映射。
- `frontend/packages/workflow/playground/src/local-ecommerce/types.ts`：LocalEcommerceNodeTemplate、UI field value、definition/ref 类型。
- `frontend/packages/workflow/playground/src/local-ecommerce/create-node.ts`：独立实例/默认值工厂、catalog 查询与内存节点校验。
- `frontend/packages/workflow/playground/src/local-ecommerce/node-registry.ts`、`form-meta.tsx`、`form.tsx`：一个 registry 和共用表单；按控件复杂度可拆 `field-control.tsx`/`reference-picker.tsx`。
- `frontend/packages/workflow/playground/src/local-ecommerce/node-content.tsx`：官方卡片内的输入/输出摘要。
- `frontend/apps/workflow-local/src/ecommerce-ui-draft-model.ts`：当前 iframe 内存分流、snapshot/dirty/放弃/冲突状态。
- 对应现有 Node test 入口下的正常状态/字段定义核对文件；验证不采用强杀、故障注入、破坏权限或攻击 fixture。

### 必改现有文件

- base 的 types 导出、`types/registry.ts`（内部 nodeDTOType 联合）。
- nodes 的 `typings/playground-context.ts`、`workflow-json-format.ts`、`utils/add-node-data.ts`（带 catalogId 的 metadata，保全 UI type）。
- playground `typing/index.ts`、`typing/local-workflow-adapter.ts`（本地模板联合和视图 generation）。
- `workflow-playground-context.ts`、`nodes-v2/utils.ts`、`nodes-v2/hooks/use-default-node-meta.ts`、`container/workflow-nodes-v2-contribution.ts`。
- `components/node-panel/hooks/use-template-node-list.ts`、`use-search-node.ts`、`utils/node-template.ts`、`components/node-panel/components/panel.tsx`、`custom-drag-card.tsx`、`atom-node-list.tsx`、`atom-category-list/index.tsx`。
- `components/toolbar/hooks/use-add-node.ts`、`services/workflow-edit-service.ts`、`services/workflow-drag-service.ts`（所有入口共享 eligibility/实例工厂）。
- `services/local-workflow-document.ts`、`services/workflow-save-service.ts`（UI-only类型、UI视图切换和分流）。
- `components/node-render/node-render-new/content/index.tsx`（共用电商内容分支）。
- `frontend/apps/workflow-local/src/main.tsx`（独立内存 UI draft、实际操作 guard、snapshot 合成）。
- `yijie-upstream.lock.json`（按真实触达上游文件登记）；如 closure/检查清单精确锁源码，更新 `scripts/yijie/workflow-editor.mjs` 的治理记录，仍使用标准构建。
- `components/node-render/node-render-new/ports.tsx`须增加电商纯装饰分支：原:60–105点击会开启enableBuildLine，:122–130无条件挂点击/键盘，故新分支不得有data-port-id、点击、键盘或连线回调。电商registry的defaultPorts为空，外观独立复用原端口样式。本期不新增电商连线；`options/workflow-document-custom-options.ts` 的原三节点连线限制保持。电商端口不注册可连线/键盘连接动作，避免新增图编排规则。

### 明确保留

`frontend/apps/workflow-local/src/canvas-data.ts`、`draft-model.ts` 的可执行图/持久化路径，bridge形状、业务generated类型、Desktop native、API/Coze backend行为、历史版本运行、业务平台和模型调用均不因为注册UI节点扩展。另有10中现有dirty的semantic说明修订与同源锁同步，不能把这里的注册子边界none误作整体none。原三节点路径适配仅增加分流，原校验保持。

## 五、步骤 1 的可确认结论与验证边界

这是可实施的唯一接入方案：一个 UI type + catalogId 独立映射 + 每次创建新 instance；官方面板/原生 compact card/header/sidebar/form 继续复用；UI 数据不进入公共 wire 图和业务执行。已知需要触达的 registry/template/metadata/form/adapter/序列化入口均明确。

当前只有源码调查和设计定稿，TS/build/真实 App/字段操作一律 NOT RUN。不要将“静态接入可行”写为“已构建通过”。后续实施需以标准 tsc 发现签名传播点，按正常可逆操作核对两实例、点击与拖动、目录名称/图标、保存阻断、重连保留和放弃恢复。源 file list 如因静态类型传播扩大，更新变更清单，不放宽公共边界。
