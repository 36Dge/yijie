# FEAT-154 步骤 1：字段分组与控件定稿

> 2026-09-15。子任务只读核对及设计建议；没有修改业务代码、启动服务、查询平台或执行节点。作为[07接入定稿](07-integration-design.md)的字段附件供D0审阅。来源仅 04 字段目录及包内原始 1–8 / 9–16 / 17–30 的输入、业务配置、输出小节；没有从处理逻辑、业务结果、错误码章节补字段。

## 1. 全 30 节点共用的最小展示结构

此结构是 renderer 内展示元数据和表单编辑状态，不是业务 schema，不生成 public DTO、执行参数或可保存 canvas。

- 节点目录项：`catalogId`、原文编号/名称、用途一句话、目录分组、已有本地图标、`sections`。
- 字段展示项：`fieldUiId`（UI 稳定键）、`sourceRef`（快照文件+行号）、`sourcePath`（原文明示机器路径；顶层都保留）、`sourceType`、`labelZh`、`helpText`、`required`（yes/no/conditional/unspecified）、`conditionText`（仅原文）、`control`、`suggestedInitial`（值+原文“建议”来源，允许缺省）、`explicitChoices`（仅原文穷举项）、`children`。
- 无原文 inner key 的子控件另用 `uiSlotId`、`sourcePhrase` 和所属顶层 `sourcePath` 定位，**不**假造 `optimization_config.mode`、`image_brief.aspect_ratio`、`target.platform` 等业务路径。控件值只记为该节点的 UI 填写内容，无序列化为源对象的出口。前端私有 key 要带清楚的 UI 命名，不伪装源字段。
- 页面内实例按独立 instanceId 持有：位置、选中状态、分组展开状态、顶层/子控件填写值、引用描述。默认值深复制；同 catalogId 的两个实例互不共享任何可变对象。
- 输入内配置对象在“业务配置”区域展示，但保留它的原输入 sourcePath；不在输入和配置区重复生成两份值。
- 对全无可明确拆分内容的 object，提供“引用页面字段”与“填写内容说明”两种入口；说明是 UI 文本。对有中文子项的 object，则按原说明拆成中文小表单，仍保留整对象引用入口。没有 raw JSON 唯一入口。
- 全量实现逐行建立 634 行 → 展示字段 ID 映射；内层 sourcePhrase 不另计顶层覆盖数。

### 未配置、空值与编辑状态

- `unset` 为尚未填写；不使用 truthiness 判值。已输入 `false`、`0`、空字符串、显式空数组各自保留。源未允许 null 时，清除控件回到 unset，不生成 null；源明确允许 null 时才提供对应选择。
- 数字原始编辑文本与已解析的 UI 值分开；输入不完整或格式有误可保留原文本、就地提示。不得把空文本变成 0、把坏值替换成默认值。
- 无初值的 boolean 使用“未选择/是/否”可清除选择；有明确建议 true 的 01 三项使用开关，并旁注“建议开启”。用户关为 false 后再打开面板仍为 false。
- required=conditional 保留条件文字徽标；只对页面可直接知道的模式切换调整提示。不构造老品检测、组件关键词依赖计算、变体事实解析、授权核验。
- 所有字段可暂时未填；必填星号与就地提示表达资料要求，不能阻止添加、选中、切换节点、关闭侧栏。界面不声称“业务校验通过”。
- 未填写必填项在触达/编辑后提示“请填写…”，初次打开避免满屏红色。空列表显示“尚未添加…”，明确清空后显示“空列表”；切换引用/填写保留各自草稿并明确当前使用方式。
- 默认展开“输入”第一子组和“业务配置”主组；辅助/高级资料与“输出”可折叠。所有字段始终有可发现的展开入口，分组标题显示字段数，不能因折叠遗失必填提示。每实例保留展开状态。

## 2. 01 商品采集：逐顶层字段映射（13 行）

来源：`sources/1-8.md` 输入 8–15，配置 16–26，输出 40–48。`—` 表示原文未规定；不是空值或默认。

| 原路径 / 区域 | 中文标签 / 分组 | 具体控件 | 建议初值 | 必填 |
|---|---|---|---|---|
| `sources` / 输入 | 采集来源 / 商品来源 | 可增删来源卡；整列表本地引用入口；每卡子项见下 | 未配置 | 是 |
| `product_hint` / 输入 | 已知商品信息 / 商品补充信息 | 中文小表单或整对象引用：品牌、型号、GTIN、语言、预期类目 | 未配置 | 否 |
| `idempotency_key` / 输入 | 批次标识 / 商品补充信息 | 单行文本，帮助说明原文字义 | 未配置 | 否 |
| `collection_scope` / 配置 | 采集内容 / 采集设置 | 可编辑标签列表；推荐标签中文显示并保留原值 | `core,attributes,variants,media` | — |
| `max_items` / 配置 | 单批商品上限 / 采集设置 | 整数框；不追加未明示 min/max | `100` | — |
| `follow_pagination` / 配置 | 继续读取分页 / 采集设置 | 开关 | `true`（建议） | — |
| `dedup_strategy` / 配置 | 去重方式 / 更多设置 | 单行文本；推荐值有中文帮助，无虚构下拉选项 | `platform_id_gtin_fingerprint` | — |
| `store_raw_snapshot` / 配置 | 保留来源快照 / 更多设置 | 开关 | `true`（建议） | — |
| `strict_source_policy` / 配置 | 严格来源策略 / 更多设置 | 开关；描述仅呈现文档含义 | `true`（建议） | — |
| `products` / 输出 | 商品列表 / 输出 | 只读 `list<object>` 行；附 ProductObjectV1 名称，不伪造内部 schema | 无输出值 | — |
| `collection_summary` / 输出 | 采集概览 / 输出 | 只读 object + 可展开中文说明项 | 无输出值 | — |
| `rejected_sources` / 输出 | 未处理来源 / 输出 | 只读 list<object> + 可展开说明项 | 无输出值 | — |
| `raw_snapshot_refs` / 输出 | 原始快照引用 / 输出 | 只读 list<object> + 引用/哈希/采集时间说明项 | 无输出值 | — |

### 01 可填子项与来源身份

- `sources[].source_type` → “来源类型”，文本框。原文没有完整 enum，不把 API/文件/URL 拼成封闭选项。
- `sources[].uri` → “来源地址”，文本框；`sources[].file_id` → “文件引用”，文本/本地引用；`sources[].product_id` → “商品标识”，文本框。三个键均在原文斜线并列中出现，界面先并列显示。原文没有明确 oneOf 约束，不能发明强制互斥、额外必填或自动判别；原帮助提示“填写适用的来源定位信息”。
- `sources[].platform` → “平台”，文本框；`sources[].marketplace` → “站点”，文本框；`sources[].credential_ref` → “授权引用”，引用/文本框，三项按原文可选。授权引用不是 token、密码或实际授权操作。
- `product_hint` 的“品牌、型号、GTIN、语言、预期类目”仅 sourcePhrase，无规范 inner key；均是可选 UI 文本槽，不拼成 `brand/model/language/category` 业务对象。
- `collection_scope` 的推荐显示：基础信息（core）、商品属性（attributes）、SKU 与变体（variants）、图片与媒体（media）。这些是建议初值，不代表封闭 enum；仍能编辑 list<string>。
- 输出 `collection_summary` 展开说明：请求数、成功数、部分成功数、失败数、去重数、耗时、来源分布；没有内层键则不制造路径/类型。`rejected_sources` 可展示原明示 `source_ref`；错误码/可重试只作为本输出定义说明，不能从错误码章节导入枚举。

## 3. 10 Listing 一键优化：逐顶层字段映射（26 行）

来源：`sources/9-16.md` 输入 162–180，输出 252–268。本节点所有输入均无原文初值，全部默认未配置；无独立配置字段，optimization_config 在业务配置区展示但仍是原输入字段。

| 原路径 / 区域 | 中文标签 / 分组 | 具体控件 | 默认 | 必填 |
|---|---|---|---|---|
| `product_snapshot` / 输入 | 商品事实快照 / 商品与目标 | 对象引用 + 商品事实说明文本 | 未配置 | 是 |
| `target` / 输入 | 目标平台与站点 / 商品与目标 | 对象引用或中文小表单：平台、站点、locale | 未配置 | 是 |
| `rule_bundle_ref` / 输入 | 目标规则快照 / 商品与目标 | 单行引用文本/本地引用 | 未配置 | 是 |
| `current_listing_snapshots` / 输入 | 当前 Listing 版本 / 基线与依据 | 可增删对象引用卡，每卡内容说明；原条件帮助完整可见 | 未配置 | 条件 |
| `diagnosis_result` / 输入 | Listing 诊断结果 / 基线与依据 | 对象引用，候选可展示节点 09 定义；附用途说明 | 未配置 | 否 |
| `keyword_asset` / 输入 | 关键词资料 / 基线与依据 | 对象引用/内容说明；完整条件帮助 | 未配置 | 条件 |
| `claim_ledger` / 输入 | 商品声明账本 / 基线与依据 | 对象引用/内容说明；提示可由 diagnosis_result.effective_claim_ledger 提供 | 未配置 | 条件 |
| `competitor_gaps` / 输入 | 竞品差异机会 / 品牌与素材 | 可增删说明卡或列表引用 | 未配置 | 否 |
| `brand_voice` / 输入 | 品牌语气 / 品牌与素材 | 中文小表单：语气、品牌术语、禁用表达、样例；整对象引用 | 未配置 | 否 |
| `media_assets` / 输入 | 详情素材 / 品牌与素材 | 可增删素材引用卡；图片、视频、Alt 文本证据的说明槽 | 未配置 | 否 |
| `variant_builder_artifact` / 输入 | SKU／变体结构资料 / 基线与依据 | 对象引用/内容说明；显示原条件 | 未配置 | 条件 |
| `optimization_config` / 输入→业务配置 | 优化设置 / 优化设置 | 整对象引用或中文小表单，见下 | 未配置 | 是 |
| `execution_mode` / 输入→业务配置 | 优化方式 / 优化设置（置顶） | 两项选择：完整生成（full_generate）、组装已有内容（assemble_only）；可清除 | 未配置 | 是 |
| `component_outputs` / 输入 | 已有内容组件 / 组件引用 | 整对象引用或四个明示引用槽，见下 | 未配置 | 条件 |
| `meta` / 输出 | 结果元数据 / 输出 | 只读 object 定义 | 无输出值 | — |
| `optimization_id` / 输出 | 优化标识 / 输出 | 只读 string 定义 | 无输出值 | — |
| `effective_claim_ledger` / 输出 | 使用的声明账本 / 输出 | 只读 object 定义 | 无输出值 | — |
| `optimization_state` / 输出 | 优化状态 / 输出 | 只读 string；展开三个原文可能值说明 | 无输出值 | — |
| `content_package` / 输出 | Listing 内容包 / 输出 | 只读 object；条件输出帮助、ListingContentPackageV1 名称 | 无输出值 | 条件输出 |
| `change_set` / 输出 | 内容变更明细 / 输出 | 只读 list<object>；前后值、原因、证据说明 | 无输出值 | — |
| `component_traces` / 输出 | 组件来源记录 / 输出 | 只读 list<object>；原文版本/hash/结果引用说明 | 无输出值 | — |
| `validation_report` / 输出 | 内容校验报告 / 输出 | 只读 object 定义与校验范围说明 | 无输出值 | — |
| `review_tasks` / 输出 | 待人工确认项 / 输出 | 只读 list<object> 定义 | 无输出值 | — |
| `payload_previews` / 输出 | 请求内容预览定义 / 输出 | 只读 list<object>；条件输出说明，不创建实际请求 | 无输出值 | 条件输出 |
| `apply_eligibility` / 输出 | 审核承接状态 / 输出 | 只读 string；展开三个原文可能值并注明不表示可发布 | 无输出值 | — |
| `platform_readiness` / 输出 | 平台准备情况 / 输出 | 只读 object；结构/资格/预检/提交/异步分离的原文说明 | 无输出值 | — |

### 10 内层小表单与条件

`optimization_config` 所属六个 sourcePhrase，均没有完整 inner key/type/required/默认；UI 槽不制造对象 schema：

| 中文项 | UI 控件建议 | 边界 |
|---|---|---|
| 模式 | 单行文本 | 不自动等同 execution_mode；原文未明确二者同义 |
| 字段范围 | 可增删文本标签 | 无预置 enum，未选择 |
| 候选数 | 数量输入（UI 整数编辑） | “数”支持数量控件的展示判断；不声明源 inner type，不设上下限/初值 |
| 保留字段 | 可增删文本标签 | 无预置 enum，未选择 |
| 审核门槛 | 多行说明文本 | 无阈值单位、范围或判定逻辑 |
| 组件版本 | 可增删“组件 / 版本说明”显示行 | 行键仅 UI，不构造版本 DTO，不查询可用组件 |

- `target` 只明示“平台、站点、locale”；平台在节点 10 未穷举，使用自由文本，不从其它节点借用封闭列表。三个说明槽无新增内层必填星号。
- `brand_voice`：语气单行文本、品牌术语可增删文本标签、禁用表达可增删文本行、样例多行文本；均为 UI 槽。
- `component_outputs.title_result` / `selling_point_result` / `detail_result` / `variant_copy_result` 是原文明示键。中文分别为“标题结果”“卖点结果”“详情结果”“变体文案结果”，候选按原文仅来自 12/13/14/16；节点 15 不进入这四槽。原文没有说四槽全必填，不全部加星。
- `execution_mode=assemble_only` 时组件引用组自动展开并突出条件提示；full_generate 时保持可展开、保留此前已填内容，不偷偷删除。模式为空时显示两种方式说明，不能预选第一项。
- `current_listing_snapshots` 条件：老品、已有 draft/audit candidate 或提供 diagnosis_result 时必选，且老品包含 live；只有不使用诊断结果的从零纯新品可省略。这段原帮助显示完整；不为此新增业务 input `is_new_product` 或解析版本。
- `keyword_asset` 条件：assemble_only 任一组件引用关键词时需完整显式资料；full_generate 缺失可内部构建的原描述仅作为字段帮助，本期不执行。
- `claim_ledger` 条件：assemble_only 由本字段或 diagnosis_result.effective_claim_ledger 提供；full_generate 的构建描述仅保留说明。
- `variant_builder_artifact` 条件：full_generate 涉及变体文案时必选；不从 facts 自动推断。
- 只读 `optimization_state` 三值 generated / baseline_preserved / no_valid_candidate；`apply_eligibility` 三值 ready_for_review / review_required / blocked。只能展示为“可能值”，不突出某一个造成已运行错觉。

## 4. 17 商品图片生成：逐顶层字段映射（18 行）

来源：`sources/17-30.md` 输入 11–24，输出 63–76。所有输入初值未配置，无独立业务配置表。image_brief 与 generation_config 在业务配置区展示但保留其原输入身份。

| 原路径 / 区域 | 中文标签 / 分组 | 具体控件 | 默认 | 必填 |
|---|---|---|---|---|
| `product_snapshot` / 输入 | 商品外观与事实 / 商品与素材 | 对象引用或中文说明小表单，见下 | 未配置 | 是 |
| `source_assets` / 输入 | 来源图片 / 商品与素材 | 可增删图片引用卡；每项有 SKU、视角、来源 UI 说明 | 未配置 | 是 |
| `asset_rights` / 输入 | 素材权利信息 / 品牌与权利 | 中文小表单或整对象引用 | 未配置 | 是 |
| `target` / 输入 | 目标平台与位置 / 商品与素材 | 中文小表单：平台/站点/语言/类目/素材位置；整对象引用 | 未配置 | 是 |
| `image_brief` / 输入→业务配置 | 图片需求 / 图片需求 | 中文小表单：类型/数量/比例/风格/信息层级/禁止内容 | 未配置 | 是 |
| `approved_claims` / 输入 | 可使用的卖点与声明 / 品牌与权利 | 可增删对象说明卡或整列表引用，提示事实/证据支持 | 未配置 | 是 |
| `brand_assets` / 输入 | 品牌视觉资料 / 品牌与权利 | 中文小表单：品牌色/字体/Logo/视觉规范/使用授权；整对象引用 | 未配置 | 否 |
| `variant_scope` / 输入 | 适用 SKU、颜色与尺寸 / 商品与素材 | 可增删字符串行/标签；保持 list<string>，不构造 SKU/color/size 三字段对象 | 未配置 | 是 |
| `generation_config` / 输入→业务配置 | 生成设置 / 生成设置 | 中文小表单：候选数/模型/随机种子/审核门槛/超时/部分成功策略 | 未配置 | 是 |
| `image_set` / 输出 | 图片候选集 / 输出 | 只读 list<image> + 用途/SKU 分组说明；无结果图 | 无输出值 | — |
| `candidate_groups` / 输出 | 图片备选组 / 输出 | 只读 list<object> + 位置/排序/推荐原因说明 | 无输出值 | — |
| `asset_manifest` / 输出 | 图片素材清单 / 输出 | 只读 object + 商品/SKU/用途/来源/生成方式说明 | 无输出值 | — |
| `fact_consistency_report` / 输出 | 商品事实一致性报告 / 输出 | 只读 object + 原文检查项说明 | 无输出值 | — |
| `rights_report` / 输出 | 素材权利报告 / 输出 | 只读 object 定义 | 无输出值 | — |
| `disclosure_advice` / 输出 | AI 标记与披露建议 / 输出 | 只读 object 定义 | 无输出值 | — |
| `review_tasks` / 输出 | 待人工确认项 / 输出 | 只读 list<object> 定义 | 无输出值 | — |
| `missing_capture_requests` / 输出 | 待补拍需求 / 输出 | 只读 list<object> 定义 | 无输出值 | — |
| `task_summary` / 输出 | 图片任务概览 / 输出 | 只读 object + 原文异步/原因/重试建议说明；无进度或状态值 | 无输出值 | — |

### 17 无 inner key 小表单仍可填写

以下中文项全部以其顶层 sourcePath + sourcePhrase + uiSlotId 归档；每个子项默认未配置、必填性未定义，不将父 object 的“是”扩为每个子项必填。

| 所属原路径 | 原文中文项 → 具体 UI 控件 |
|---|---|
| `product_snapshot` | 商品外观 → 多行说明；材质 → 文本；尺寸 → 文本（保留原单位）；颜色 → 文本标签；包装清单 → 可增删文本行；功能 → 多行文本；限制 → 多行文本；变体事实 → 多行文本/对象引用 |
| `source_assets` 各项 | 图片引用 → 本地输出引用或用户填写引用标识；SKU → 文本；视角 → 文本；来源 → 文本。卡片用本地图标占位，不能自动访问 URI、上传文件、下载或预览远程图片 |
| `asset_rights` | 素材所有者 → 文本；授权用途 → 多行文本；平台 → 文本；市场 → 文本；期限 → 文本（不猜日期模型/时区）；人物肖像授权 → 文本/引用（原文未给 boolean，不造授权通过开关） |
| `target` | 平台 → 可清除单选 Amazon / TikTok Shop（本节点原文明示）；站点 → 文本；语言 → 文本；类目 → 文本/引用；素材位置 → 文本（不从处理逻辑补主图/A+ 等枚举） |
| `image_brief` | 图片类型 → 文本；数量 → UI 数量输入，不声明 inner type/边界；比例 → 文本（无 1:1 默认/枚举）；风格 → 文本；信息层级 → 多行文本；禁止内容 → 可增删文本行 |
| `approved_claims` | 每项为声明内容说明 + 对象引用选择；原文未给内层 key，不新增可提交的 claim/evidence wire；用帮助提示须有事实或证据支持 |
| `brand_assets` | 品牌色 → 可增删文本（不强制 HEX）；字体 → 文本（不联网加载字体）；Logo → 素材引用；视觉规范 → 多行文本；使用授权 → 文本/引用 |
| `generation_config` | 候选数 → UI 数量输入；模型 → 文本/引用（无模型市场）；随机种子 → 文本（源未给 inner type/range，不强行安全整数范围）；审核门槛 → 多行文本；超时 → 文本“填写时长与单位”（原文无单位，不偷加秒）；部分成功策略 → 多行文本（无策略 enum） |

图片类型、比例、风格、模型、种子、超时和策略均不能从 PDF 截图或被排除的处理逻辑取默认值/选项。按数量自然含义选择数值控件仅是 UI 编辑建议，与源类型定义严格分开。

## 5. 官方组件复用核对

以 `yijie-coze/frontend/packages/workflow/playground/src/` 为根；固定上游 `fefb05ff27be1da939612fbf9faf5db62583b8ae`，当前工作树包含已登记本地适配。这里只读源码，尚未编译或确认运行适配。

| 路径 | 核对事实及定稿建议 |
|---|---|
| `components/node-side-sheet/index.tsx` | 已有 NodeSideSheet / ResizableSidePanel / EditorThemeProvider / NodeContextProvider，按 node.id 建 context；直接用其壳和滚动区，不建第二种侧栏 |
| `form/components/section.tsx` | Section 使用 FormCard、FieldEmpty，支持 collapsible、open/close；适合输入/配置/输出及子组 |
| `form-extensions/components/literal-value-input/literal-value-input.tsx` | 已有 inputType→控件 registry；可复用原始控件，需 UI state 适配；object 不能自动落到唯一 JSON 框 |
| `form-extensions/components/literal-value-input/input-boolean.tsx` | 当前 Select 为 true/false、支持清除；清除调用 onChange(null)，defaultValue 优先 value，且为 uncontrolled defaultValue。新 UI 必须显式适配 unset、中文标签、清除及实例切换，不能直接用它保证空值/false/重开保留 |
| `form-extensions/components/value-expression-input/typed-value-expression-input.tsx` | 原组件依赖 variableService、会按类型切换初始化 []/{} 或清空旧值；不能直接作为新 UI 对象值/引用状态真值。只复用外观或显式接静态本地候选，不转换当前字符串执行引用 |
| `form-extensions/components/output-param-display/index.tsx` | OutputsParamDisplay 接收 label/type/required 并只读展示，很适合输出行；复杂说明用 Section 展开。输出不需启用可编辑 output-tree/schema JSON import |

尚需主实现核对的行为：新表单更新是否走原生 FlowNodeFormData 的正确 UI 分支、引用候选组件有无隐式网络、副作用是否进入原 DraftModel。不能因组件名可用就声称已完成安全复用。

## 6. 静态交互示意应呈现的关键状态

### 布局

- 沿用现有工作流标题/工具区、点阵画布、底部“添加节点”和右侧原生侧栏；青柠 #B7F03D 与浅画布 #F2F3F5。示意页若用于 D0，要醒目标“设计预览，尚未实现”，并列明所有数据为合成示例。
- 面板用五组、双列节点图标/原名、顶部搜索、滚动；无结果有“清空搜索”。打开侧栏后关闭目录浮层。
- 卡片标题完整 tooltip、输入与输出摘要分别展示，不填运行结果；属性栏中文标签主层级，技术变量名和类型次层级。
- 侧栏固定标题/关闭，主体滚动；输入/业务配置/输出分组。页面提示“当前仅配置节点界面，暂不支持保存和运行”。静态示意禁用状态应真禁用，有说明；“已有结果”不得用彩色成功徽标。

### 必须可评审的状态组合

1. **目录初始与搜索空态**：正式实现展示全部30项目录；本次交互示意只含01/10/17，30项以04为准；搜索一个无匹配词，显示可恢复空态。
2. **01 初次添加**：sources 未配置，6 项推荐配置可见；输出 4 项只读。“继续读取分页”可由 true 改 false。
3. **同类独立实例**：01 第一个写“示例来源 A”，另一个未写或写 B；切换后各自值与 false 不串。关闭侧栏→重新打开仍保留。
4. **10 模式未选**：execution_mode 显示“请选择优化方式”；条件字段有“条件必填”说明。选择 assemble_only 后四引用槽可见，无候选显示“暂无可引用字段”；full_generate 切回保留旧填写且不自动造默认值。
5. **17 未配置/已填**：source_assets 图片占位卡可添加引用，SKU/视角/来源可填写；image_brief 的比例保持未填写/自由填，generation_config 没有模型/600 秒默认；输出没有生成图片。
6. **引用有效/来源删除**：引用条显示节点名 + 输出中文名 + 辅助变量路径；只连接同页输出定义。删除来源后保留引用位置，显示“引用节点已移除”，提供重新选择/清除；不取值/求值，不静默改绑。
7. **格式错误**：01 max_items 普通输入非整数时就地提示，修正为 100 后提示消失；不拦截关闭侧栏或创建其它节点，不调用业务校验。
8. **配置更新**：可见文案“配置已更新，仅保留在当前页面”，不要“保存成功”。推荐常驻范围说明+轻量状态，而非每次打字 toast。
9. **删除/取消**：有填写内容的节点通过更多→删除出现确认，取消保留节点、选择、位置、引用和值。删除最后一个电商节点仍处设计状态，恢复原草稿须显式动作。
10. **离开**：确认标题“放弃本次节点配置？”正文“配置仅保留在当前页面，离开后将丢失。”按钮“继续编辑”（默认焦点）/“放弃配置并离开”。若原三节点草稿另有未保存改动，须先明确呈现后续原草稿保护，不能把当前放弃解释成丢弃全部草稿。
11. **重连/只读**：保留设计值并显示会话只读及重连入口。成功重连恢复编辑不替换设计；若 provider revision 已变化，只显示真实变化提示，不能“配置已同步”。

D0确认与机器检查的实际状态见07和02。本轮用户已明确选择纯前端/页面离开确认、App关闭不保证保留；这不自动等于批准尚未展示的全部具体控件方案。
