# FEAT-154：30 个电商节点 UI 字段目录

## 1. 使用范围与来源边界

本目录是待确认的需求稿，服务于“添加节点弹出面板、节点卡片、属性配置面板”的前端设计。当前只落需求，未实施或运行节点。

- **原文事实**：逐节点保留三份 Markdown 中“输入”“业务配置”“输出”的完整小节正文，包括表后条件、补充说明和输出示例。名称、类型、必填性、明确枚举和建议默认值均以这些摘录为准。
- **UI 候选**：本目录的五个分组、每节点控件差异说明是为了形成可评审界面而给出的推荐，不是原文已有界面设计或已获批准的决定。共通控件、变量绑定、卡片、属性面板与前端状态遵循 [UI 需求](03-ui-requirements.md)。
- **执行边界**：PDF 明确忽略 Markdown 的处理逻辑、业务结果和错误码章节，本目录没有摘入这些章节。输入/输出原文中出现计算、采集、校验、审核、发布、费用、API、重试等描述，仅解释字段含义；不产生 FEAT-154 的算法、外部服务、API 接入或编排执行需求。状态字段仅作为输出元信息展示，不伪造运行结果。
- **标识边界**：三份文档没有定义节点 `nodeType`、注册 ID 或组件名。目录编号与原名用于核对覆盖，不代表执行顺序；具体前端标识方案见 [UI 需求](03-ui-requirements.md)。
- **默认值边界**：节点 1–8 的配置列明确称“建议默认值”。明确字面值可作为前端初值候选；“当前稳定版本/快照/规则”等是要求描述，不能杜撰具体 ID。“必须指定/显式选择”保持未填写提示。节点 9–30 没有独立业务配置表；配置藏于输入对象，内层多数未给完整 Schema、机器键、枚举、单位、数值范围或默认。推荐复用现有对象编辑/变量绑定与卖家说明，不据此补造业务规则；未设置的可选布尔须能与显式 false 区分。
- **嵌套对象边界**：原文列出子项且结构足够明确时可拆分卖家控件，但仍保留所属原对象与字段身份。内层结构不全时只做可编辑/可绑定的对象输入，不凭示例建立封闭枚举，也不要求卖家理解节点处理算法。

来源快照：[节点 1–8](sources/1-8.md)、[节点 9–16](sources/9-16.md)、[节点 17–30](sources/17-30.md)、[PDF 界面任务](<sources/电商节点 UI界面.pdf>)。下文行号均指包内快照，不依赖用户电脑原始绝对路径。

## 2. 覆盖核对与计数口径

计数以原文表格中每个顶层变量/配置项的数据行为单位，排除表头和分隔行；同名字段在不同节点或不同小节分别计数。表后说明、嵌套子项及 JSON 示例完整保留，但不再重复计为顶层字段行。原文“必选/必填”的不同表头保留原样。

| 原文小节类型 | 小节数 | 顶层字段行数 |
| --- | ---: | ---: |
| 输入 | 30 | 299 |
| 业务配置 | 8 | 64 |
| 输出 | 30 | 271 |
| **合计** | **68** | **634** |

原文节点 9–30 缺少独立业务配置节，这是来源结构差异，不是遗漏；其配置对象已经计入“输入”。目录仅有 30 个节点，无合并、删减或额外执行节点。

## 3. 推荐分组与节点总表

五组只用于卖家查找节点，保留节点编号与原名。其精确空格、斜线和全角符号以原名列为准；不按分组生成固定执行链。

| 编号 | 原名 | 推荐分组 | 输入行 | 配置行 | 输出行 | 合计 | 原文起始行 |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | [商品采集](#node-01) | 商品准备与选品 | 3 | 6 | 4 | 13 | [1-8.md](sources/1-8.md) 第 3 行 |
| 2 | [商品信息清洗与标准化](#node-02) | 商品准备与选品 | 4 | 5 | 5 | 14 | [1-8.md](sources/1-8.md) 第 55 行 |
| 3 | [类目与属性智能匹配](#node-03) | 商品准备与选品 | 6 | 8 | 4 | 18 | [1-8.md](sources/1-8.md) 第 109 行 |
| 4 | [SKU／变体结构重建](#node-04) | 商品准备与选品 | 10 | 9 | 9 | 28 | [1-8.md](sources/1-8.md) 第 225 行 |
| 5 | [选品机会评估](#node-05) | 商品准备与选品 | 9 | 9 | 7 | 25 | [1-8.md](sources/1-8.md) 第 313 行 |
| 6 | [竞品商品采集](#node-06) | 商品准备与选品 | 11 | 9 | 5 | 25 | [1-8.md](sources/1-8.md) 第 436 行 |
| 7 | [竞品对标分析](#node-07) | 商品准备与选品 | 8 | 8 | 6 | 22 | [1-8.md](sources/1-8.md) 第 515 行 |
| 8 | [成本利润与定价测算](#node-08) | 商品准备与选品 | 13 | 10 | 7 | 30 | [1-8.md](sources/1-8.md) 第 596 行 |
| 9 | [Listing 综合诊断](#node-09) | Listing与搜索优化 | 11 | 0 | 18 | 29 | [9-16.md](sources/9-16.md) 第 3 行 |
| 10 | [Listing 一键优化](#node-10) | Listing与搜索优化 | 14 | 0 | 12 | 26 | [9-16.md](sources/9-16.md) 第 156 行 |
| 11 | [SEO 关键词挖掘](#node-11) | Listing与搜索优化 | 10 | 0 | 6 | 16 | [9-16.md](sources/9-16.md) 第 282 行 |
| 12 | [商品标题优化](#node-12) | Listing与搜索优化 | 10 | 0 | 8 | 18 | [9-16.md](sources/9-16.md) 第 428 行 |
| 13 | [核心卖点／五点描述生成](#node-13) | Listing与搜索优化 | 11 | 0 | 8 | 19 | [9-16.md](sources/9-16.md) 第 541 行 |
| 14 | [商品详情描述／A+ 内容生成](#node-14) | Listing与搜索优化 | 12 | 0 | 9 | 21 | [9-16.md](sources/9-16.md) 第 675 行 |
| 15 | [多语言翻译与本地化](#node-15) | Listing与搜索优化 | 18 | 0 | 16 | 34 | [9-16.md](sources/9-16.md) 第 813 行 |
| 16 | [规格名称与变体文案优化](#node-16) | Listing与搜索优化 | 9 | 0 | 10 | 19 | [9-16.md](sources/9-16.md) 第 965 行 |
| 17 | [商品图片生成](#node-17) | 图片与视频 | 9 | 0 | 9 | 18 | [17-30.md](sources/17-30.md) 第 5 行 |
| 18 | [商品图片处理与平台适配](#node-18) | 图片与视频 | 9 | 0 | 8 | 17 | [17-30.md](sources/17-30.md) 第 93 行 |
| 19 | [图片文案翻译与重绘](#node-19) | 图片与视频 | 8 | 0 | 8 | 16 | [17-30.md](sources/17-30.md) 第 182 行 |
| 20 | [商品视频脚本生成](#node-20) | 图片与视频 | 10 | 0 | 8 | 18 | [17-30.md](sources/17-30.md) 第 263 行 |
| 21 | [商品短视频生成](#node-21) | 图片与视频 | 9 | 0 | 11 | 20 | [17-30.md](sources/17-30.md) 第 353 行 |
| 22 | [视频字幕、配音与本地化](#node-22) | 图片与视频 | 10 | 0 | 11 | 21 | [17-30.md](sources/17-30.md) 第 447 行 |
| 23 | [商品合规判断](#node-23) | 合规与发布 | 9 | 0 | 11 | 20 | [17-30.md](sources/17-30.md) 第 543 行 |
| 24 | [知识产权与品牌侵权风险检查](#node-24) | 合规与发布 | 11 | 0 | 11 | 22 | [17-30.md](sources/17-30.md) 第 643 行 |
| 25 | [Listing 全素材合规审核](#node-25) | 合规与发布 | 10 | 0 | 12 | 22 | [17-30.md](sources/17-30.md) 第 745 行 |
| 26 | [商品发布与上架校验](#node-26) | 合规与发布 | 13 | 0 | 12 | 25 | [17-30.md](sources/17-30.md) 第 851 行 |
| 27 | [库存与履约风险监控](#node-27) | 店铺运营 | 10 | 0 | 8 | 18 | [17-30.md](sources/17-30.md) 第 985 行 |
| 28 | [评论与差评洞察](#node-28) | 店铺运营 | 11 | 0 | 9 | 20 | [17-30.md](sources/17-30.md) 第 1079 行 |
| 29 | [客服回复生成](#node-29) | 店铺运营 | 10 | 0 | 9 | 19 | [17-30.md](sources/17-30.md) 第 1171 行 |
| 30 | [广告与流量投放优化](#node-30) | 店铺运营 | 11 | 0 | 10 | 21 | [17-30.md](sources/17-30.md) 第 1259 行 |

## 4. 逐节点字段与 UI 差异

“原文摘录”正文逐字保留。其上方“UI 候选”只从该节点输入、业务配置、输出提取界面需求；不得用摘录中的执行说明补增算法或执行验收。

<a id="node-01"></a>

### 01. 商品采集

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 3–54 行。
- 覆盖：输入 3 行、业务配置 6 行、输出 4 行，共 13 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `sources` 以可增删来源行或对象变量绑定呈现；原文列出必要子字段，但未给 `source_type` 完整枚举。`product_hint` 与 `idempotency_key` 保持可选。
- 范围用多值控件、`max_items` 用整数控件、三个布尔配置用开关；`dedup_strategy` 只有一个建议初值，不能补造其他策略选项。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 8–15 行；表格顶层字段 3 行。

<!-- source-excerpt node=01 section=输入 start=8 end=15 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `sources` | `list<object>` | 是 | 每项包含 `source_type`、`uri/file_id/product_id`、可选 `platform`、`marketplace`、`credential_ref`。 |
| `product_hint` | `object` | 否 | 已知品牌、型号、GTIN、语言或预期类目，用于校验，不可覆盖来源事实。 |
| `idempotency_key` | `string` | 否 | 同一批采集请求的幂等键，防止重复写入和重复计费。 |
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 16–26 行；表格顶层字段 6 行。

<!-- source-excerpt node=01 section=业务配置 start=16 end=26 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `collection_scope` | `list<string>` | `core,attributes,variants,media` | 需要采集的字段范围。评论和竞品经营信号由“竞品商品采集”负责。 |
| `max_items` | `integer` | `100` | 批处理上限；超出时分页或返回明确错误，不静默截断。 |
| `follow_pagination` | `boolean` | `true` | 对授权 API 或文件分片是否继续翻页。 |
| `dedup_strategy` | `string` | `platform_id_gtin_fingerprint` | 依次使用平台 ID、GTIN/MPN、稳定字段指纹去重。 |
| `store_raw_snapshot` | `boolean` | `true` | 保存原始响应快照引用及哈希，便于审计和重放。 |
| `strict_source_policy` | `boolean` | `true` | 只允许授权接口、用户上传文件和允许访问的来源；不绕过登录、验证码或访问控制。 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 40–48 行；表格顶层字段 4 行。

<!-- source-excerpt node=01 section=输出 start=40 end=48 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `products` | `list<object>` | 统一为 `ProductObjectV1` 的商品列表。 |
| `collection_summary` | `object` | 请求数、成功数、部分成功数、失败数、去重数、耗时、来源分布。 |
| `rejected_sources` | `list<object>` | 无法处理的来源及 `source_ref`、错误码、是否可重试。 |
| `raw_snapshot_refs` | `list<object>` | 原始快照引用、内容哈希和采集时间。 |
<!-- /source-excerpt -->

<a id="node-02"></a>

### 02. 商品信息清洗与标准化

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 55–108 行。
- 覆盖：输入 4 行、业务配置 5 行、输出 5 行，共 14 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `target_marketplace`、`fx_rates`、`normalization_dictionary` 使用对象编辑/变量绑定；保留目标市场、汇率来源及时间等原文说明。
- `strictness` 可选 `conservative/balanced/strict`，建议 `balanced`；`currency_policy` 可选 `preserve_original/convert_with_supplied_rate`，建议前者；其他字符串配置未给完整枚举。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 60–68 行；表格顶层字段 4 行。

<!-- source-excerpt node=02 section=输入 start=60 end=68 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `products` | `list<object>` | 是 | `ProductObjectV1` 或可映射到该结构的商品列表。 |
| `target_marketplace` | `object` | 是 | 包含平台、国家/站点、语言、目标币种和单位制。 |
| `fx_rates` | `object` | 否 | 显式提供汇率、基准币种、报价币种、时间和来源；缺失时不得自行猜测汇率。 |
| `normalization_dictionary` | `object` | 否 | 品牌保护词、属性别名、颜色/材质/单位词典等用户扩展规则。 |
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 69–78 行；表格顶层字段 5 行。

<!-- source-excerpt node=02 section=业务配置 start=69 end=78 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `strictness` | `string` | `balanced` | `conservative`、`balanced`、`strict`。影响自动修复与转人工门槛。 |
| `html_policy` | `string` | `preserve_structure` | 去除脚本和标签，但保留段落、列表及必要换行。 |
| `unit_system` | `string` | `target_market_default` | 目标站点常用单位；始终保留原始值。 |
| `currency_policy` | `string` | `preserve_original` | 可选 `preserve_original` 或 `convert_with_supplied_rate`。 |
| `deduplicate_media` | `boolean` | `true` | 使用 URL 规范化、内容哈希和感知哈希识别重复媒体。 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 93–102 行；表格顶层字段 5 行。

<!-- source-excerpt node=02 section=输出 start=93 end=102 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `normalized_products` | `list<object>` | 清洗后的 `ProductObjectV1`，包含原值引用。 |
| `change_log` | `list<object>` | 字段级原值、新值、规则、原因、置信度和是否可回滚。 |
| `quality_reports` | `list<object>` | 每个商品的完整度、合法率、一致性、异常字段和待补字段。 |
| `review_items` | `list<object>` | 需要人工确认的冲突或低置信度映射。 |
| `unmapped_attributes` | `list<object>` | 无法进入统一模型但被保留的来源属性。 |
<!-- /source-excerpt -->

<a id="node-03"></a>

### 03. 类目与属性智能匹配

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 109–224 行。
- 覆盖：输入 6 行、业务配置 8 行、输出 4 行，共 18 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `targets` 为可增删目标对象列表，保留 `target_id/platform/marketplace/locale`；`matching_overrides` 与 `visual_features` 各自独立。
- 三个 registry/crosswalk 引用及 `semantic_model_ref` 未给实际版本 ID，显示引用输入及提示，不将“当前稳定版本”写成虚构 ID；数值和布尔建议初值见原文配置表。
- 输出 JSON 是结构示例；其中 demo 标识、日期版本和分数均非前端默认值或真实运行结果。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 114–124 行；表格顶层字段 6 行。

<!-- source-excerpt node=03 section=输入 start=114 end=124 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `normalized_products` | `list<object>` | 是 | 节点 2 输出，必须包含商品 ID、内容、属性和来源证据。 |
| `targets` | `list<object>` | 是 | 每项包含 `target_id`、`platform`、`marketplace`、`locale`；每个目标独立计算。 |
| `category_hints` | `list<object>` | 否 | 来源类目或卖家提示，默认只是软提示，不能直接当最终结果。 |
| `visual_features` | `list<object>` | 否 | 已有图片识别结果，必须包含图片哈希、模型版本和置信度。 |
| `matching_overrides` | `object` | 否 | 允许/禁止类目、卖家确认属性；覆盖操作必须记录原因和时间。 |
| `reference_time` | `string` | 否 | 选择平台类目和属性规则快照的基准时间。 |
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 125–137 行；表格顶层字段 8 行。

<!-- source-excerpt node=03 section=业务配置 start=125 end=137 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `taxonomy_registry_ref` | `string` | 当前稳定快照 | 平台、站点对应的类目树、Product Type、弃用和迁移关系。 |
| `attribute_schema_registry_ref` | `string` | 与类目快照一致 | 必填、推荐、枚举、单位和条件属性规则。 |
| `crosswalk_ref` | `string` | 当前稳定版本 | 来源类目、平台中立本体和目标类目的映射。 |
| `candidate_top_k` | `integer` | `20` | 混合召回保留的候选数量。 |
| `min_auto_confidence` | `float` | `0.90` | 自动匹配门槛，实际由平台/类目族校准配置覆盖。 |
| `min_score_margin` | `float` | `0.15` | 第一、第二候选最小分差。 |
| `enable_visual_signal` | `boolean` | `true` | 图片可用时启用视觉信号，失败后可降级。 |
| `semantic_model_ref` | `string` | 固定已发布版本 | 只用于候选召回/重排，不能生成不存在的类目 ID。 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 168–218 行；表格顶层字段 4 行。

<!-- source-excerpt node=03 section=输出 start=168 end=218 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `matched_products` | `list<object>` | 原标准商品加各目标平台映射引用，不丢失原始商品事实。 |
| `category_matches` | `list<object>` | 按“商品 × 目标”展开的匹配详情。 |
| `matching_report` | `object` | 自动匹配率、复核率、未匹配率、属性覆盖率和版本统计。 |
| `review_items` | `list<object>` | 类目歧义、属性冲突、必填缺失及低置信度建议。 |

`category_matches[]` 至少包含：

```json
{
  "match_id": "match_demo_001_amazon_us",
  "product_id": "prod_demo_001",
  "target_id": "amazon_us",
  "state": "review_required",
  "taxonomy_version": "taxonomy-snapshot-2026-08",
  "selected_category": {
    "category_id": "demo-category-100",
    "name": "Illustrative category",
    "path": ["Home", "Drinkware"],
    "product_type": "DEMO_PRODUCT_TYPE",
    "score": 0.86,
    "confidence": 0.86,
    "reason_codes": ["SEMANTIC_AND_ATTRIBUTE_MATCH"]
  },
  "confidence": 0.86,
  "score_breakdown": [
    {"signal": "semantic", "score": 0.91, "weight": 0.55},
    {"signal": "attribute_compatibility", "score": 0.84, "weight": 0.45}
  ],
  "alternatives": [
    {
      "category_id": "demo-category-101",
      "name": "Illustrative alternative",
      "path": ["Home", "Kitchen Storage"],
      "product_type": "DEMO_ALTERNATIVE",
      "score": 0.81,
      "confidence": 0.81,
      "reason_codes": ["SEMANTIC_MATCH"]
    }
  ],
  "mapped_attributes": [],
  "missing_required_attribute_ids": [],
  "recommended_attribute_ids": [],
  "conflict_codes": [],
  "review_reasons": []
}
```
<!-- /source-excerpt -->

<a id="node-04"></a>

### 04. SKU／变体结构重建

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 225–312 行。
- 覆盖：输入 10 行、业务配置 9 行、输出 9 行，共 28 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 保留父商品、来源 SKU、目标、现有结构和三类关联记录的独立输入；`platform_schemas` 标记条件必填并展示原文条件，前端不接规则连接器。
- `rebuild_mode` 为 `validate_only/rebuild`；`unsupported_axis_policy` 为 `reject/split_parent`；其余策略未列完整枚举，只保留配置表给出的建议初值。
- `is_variant_ready` 的输出说明是“所有目标变体映射均就绪”，不可把卖家标签写成“商品已可上架”。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 230–244 行；表格顶层字段 10 行。

<!-- source-excerpt node=04 section=输入 start=230 end=244 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `product` | `object` | 是 | 标准商品事实，至少包含 `product_id`、标题和基础属性。 |
| `source_skus` | `list<object>` | 是 | 每项至少包含稳定 `source_sku_id` 和 `options`；可含条码、价格、库存、媒体引用。 |
| `targets` | `list<object>` | 是 | 平台、站点、节点 3 选定的类目 ID/Product Type 和 Schema 版本。 |
| `platform_schemas` | `list<object>` | 条件必填 | 平台类目允许的变体主题/销售属性、值域和限制；未传入时由版本化连接器取得。 |
| `existing_structure` | `object` | 否 | 已有父 SKU、子 SKU 和平台商品 ID，用于保持 ID 稳定和增量重建。 |
| `inventory_records` | `list<object>` | 否 | 按 SKU/仓库提供的可用库存和快照时间。 |
| `price_records` | `list<object>` | 否 | 按 SKU 提供的价格、币种、价格类型和生效时间。 |
| `media_records` | `list<object>` | 否 | 与来源 SKU、条码或已确认组合绑定的媒体。 |
| `alias_dictionary` | `object` | 否 | 版本化规格别名，例如 `Colour → Color`、`2pcs → pack_quantity=2`。 |
| `locked_mappings` | `list<object>` | 否 | 人工确认且本次不得覆盖的轴和值映射。 |
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 245–258 行；表格顶层字段 9 行。

<!-- source-excerpt node=04 section=业务配置 start=245 end=258 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `rebuild_mode` | `string` | `rebuild` | `validate_only` 或 `rebuild`。 |
| `combination_policy` | `string` | `observed_only` | 只输出真实观察到的 SKU 组合。 |
| `duplicate_policy` | `string` | `quarantine` | 同组合多 SKU 默认隔离，不自动合并价格、库存或条码。 |
| `unsupported_axis_policy` | `string` | `reject` | 可选 `split_parent`，禁止静默删除平台不支持的规格轴。 |
| `auto_mapping_threshold` | `float` | `0.90` | 轴/值自动映射最低置信度。 |
| `candidate_gap_threshold` | `float` | `0.10` | 最佳与次佳候选分差不足时转复核。 |
| `max_cartesian_size` | `integer` | `5000` | 理论组合超过上限时只返回计数和诊断，不展开。 |
| `sku_id_strategy` | `string` | `preserve_then_hash` | 优先保留现有 ID；新 ID 由稳定组合键生成。 |
| `strict_mode` | `boolean` | `false` | 关闭时隔离问题 SKU 并返回部分结果。 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 293–306 行；表格顶层字段 9 行。

<!-- source-excerpt node=04 section=输出 start=293 end=306 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `canonical_parent` | `object` | 标准父商品 ID、父 SKU、共享属性及来源。 |
| `canonical_axes` | `list<object>` | 标准轴、标准值、来源别名和映射证据。 |
| `canonical_skus` | `list<object>` | 组合键、规格值、价格、库存、条码、媒体、来源和状态。 |
| `platform_structures` | `list<object>` | 各目标平台的父/子体或销售属性/SKU 映射，以及独立 `variant_ready`、`evaluated_fields` 和未决项。 |
| `combination_report` | `object` | 理论、观察、缺失、重复、无效组合数量及稀疏矩阵状态。 |
| `quarantined_records` | `list<object>` | 被隔离记录、冲突对象、错误码和修复建议。 |
| `mapping_issues` | `list<object>` | 未映射轴/值、歧义候选和平台不兼容项。 |
| `quality_report` | `object` | 来源有效率、规格完整率、映射覆盖率和变体映射就绪率。 |
| `is_variant_ready` | `boolean` | 只有全部目标的变体映射均就绪时为 `true`；不表示商品整体可上架。 |
<!-- /source-excerpt -->

<a id="node-05"></a>

### 05. 选品机会评估

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 313–435 行。
- 覆盖：输入 9 行、业务配置 9 行、输出 7 行，共 25 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `winsorize_bounds` 与 `score_thresholds` 已给对象子键及数字，可分别用两项数值输入；`policy_version` 必须指定，保持未填写提示。
- 配置节还给七项建议维度权重及平台 profile 说明；可作为策略权重分组的 UI 候选，原文没有为该组给独立顶层机器字段名，不能新增影子字段或实现评分。
- 条件必填的 `economics/compliance_results/fx_rates` 保留条件说明；候选输出三组分别显示变量元信息。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 318–331 行；表格顶层字段 9 行。

<!-- source-excerpt node=05 section=输入 start=318 end=331 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `candidate_products` | `list<object>` | 是 | 候选商品，至少包含唯一 `candidate_id`、商品事实和目标类目。 |
| `market_context` | `object` | 是 | 平台、站点、币种、评估截止日期、时间窗和类目；不可比市场应拆分运行。 |
| `metric_observations` | `list<object>` | 是 | 指标名、数值/文本、单位、观察周期、来源、采集时间、样本量和可靠性。 |
| `economics` | `list<object>` | 条件必填 | 来自节点 8 的利润情景；缺失时候选只能 `hold`。 |
| `compliance_results` | `list<object>` | 条件必填 | 来自后续合规能力的结果引用；缺失或未知时只能 `hold`，本节点不重新定义合规节点。 |
| `benchmarks` | `list<object>` | 否 | 同平台/站点/类目/周期的 P10、P50、P90 或业务阈值及来源。 |
| `review_insights` | `list<object>` | 否 | 评论痛点、提及数、样本数、严重度和证据。 |
| `content_gap_observations` | `list<object>` | 否 | 竞品内容缺口、样本量、重要度和候选能否有证据地补足。 |
| `fx_rates` | `list<object>` | 条件必填 | 跨币种数据使用，必须包含汇率日期和来源。 |
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 332–347 行；表格顶层字段 9 行。

<!-- source-excerpt node=05 section=业务配置 start=332 end=347 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `policy_version` | `string` | 必须指定 | 指标、权重、门禁、公式和来源可靠度版本。 |
| `normalization_method` | `string` | `benchmark_percentile` | 优先使用外部可比基准，无基准才使用候选集合百分位。 |
| `min_cohort_size` | `integer` | `20` | 小于此样本数时不使用候选集合做相对归一。 |
| `winsorize_bounds` | `object` | `{"lower":0.05,"upper":0.95}` | 仅限制评分用值，原始观测不修改。 |
| `min_observed_weight` | `float` | `0.80` | 有效观测权重不足时不输出正式总分。 |
| `max_imputed_weight` | `float` | `0.20` | 普通指标最大插补权重；合规和利润禁止插补。 |
| `score_thresholds` | `object` | `{"prioritize_min":75,"validate_min":60}` | 优先、验证和降低优先级阈值，分数范围 `[0,100]`。 |
| `min_evidence_confidence` | `float` | `0.70` | 置信度统一为 `[0,1]`；得分高但证据置信度低时只能验证。 |
| `sensitivity_weight_delta` | `float` | `0.20` | 单个维度权重上下浮动比例。 |

建议默认维度权重：需求热度 `0.25`、竞争机会 `0.15`、价格带适配 `0.10`、利润空间 `0.25`、季节与进入时机 `0.10`、评论痛点机会 `0.08`、内容缺口机会 `0.07`。这是初始策略而非永久规则；Amazon 与 TikTok Shop 可配置不同 profile。合规风险不参与加权稀释，直接作为硬门禁。
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 416–429 行；表格顶层字段 7 行。

<!-- source-excerpt node=05 section=输出 start=416 end=429 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `evaluation_id` | `string` | 本次评估稳定 ID。 |
| `policy_version` | `string` | 实际使用的策略版本。 |
| `ranked_candidates` | `list<object>` | 仅硬门禁通过的正式排名。 |
| `held_candidates` | `list<object>` | 因证据、利润或合规未确认而待审核的候选。 |
| `rejected_candidates` | `list<object>` | 硬门禁失败候选及原因。 |
| `portfolio_summary` | `object` | 各决策数量、Top 候选、共同风险和数据覆盖。 |
| `data_quality_report` | `object` | 缺失率、过期率、插补率、来源冲突和隔离指标。 |

每个候选至少输出 `gate_results`、`decision`、`rank`、`opportunity_score`、`evidence_confidence`（范围 `[0,1]`）、`dimension_scores`、利润摘要、`score_min/max`、决策/排名稳定度、正负驱动项、缺失字段及证据引用。
<!-- /source-excerpt -->

<a id="node-06"></a>

### 06. 竞品商品采集

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 436–514 行。
- 覆盖：输入 11 行、业务配置 9 行、输出 5 行，共 25 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `platform` 明确为 `amazon/tiktok_shop`；`discovery_mode` 明确为 `keyword/category/seed_product/mixed`；关键词、类目、种子输入保留对应条件提示及至少一类来源的前端校验。
- `entity_level` 明确四项；`target_count` 是最终竞品目标数唯一配置源，建议 30，不是硬上限。`collection_scope` 不再放一个重复的最终目标数。
- `freshness_policy` 与 `adapter_version` 没有实际字面默认值；`uncertain_candidate_policy/evidence_level` 只有建议初值，没有完整枚举。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 441–458 行；表格顶层字段 11 行。

<!-- source-excerpt node=06 section=输入 start=441 end=458 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `platform` | `string` | 是 | `amazon` 或 `tiktok_shop`。 |
| `marketplace` | `string` | 是 | 明确站点/国家，不允许只传平台名。 |
| `discovery_mode` | `string` | 是 | `keyword`、`category`、`seed_product` 或 `mixed`。 |
| `keywords` | `list<object>` | 条件必填 | 每项含查询词、语言和可选权重。 |
| `category_id` | `string` | 条件必填 | 类目模式下的平台有效类目 ID。 |
| `seed_products` | `list<object>` | 条件必填 | 种子商品 ID/URL，以及可选标准商品事实。 |
| `collection_scope` | `object` | 是 | 单次来源的最大候选数、页数上限、字段范围、评论/媒体采样范围；不重复承载最终目标竞品数。 |
| `filters` | `object` | 否 | 品牌排除、价格范围、履约方式、是否排除配件/翻新/不同比例套装等。 |
| `market_context` | `object` | 否 | 语言、币种、非个性化地域上下文和搜索排序。 |
| `credential_ref` | `string` | 否 | 授权凭证引用，不传明文 Token。 |
| `existing_snapshot` | `object` | 否 | 可复用历史快照，必须包含采集时间、来源和版本。 |

`keywords`、`category_id`、`seed_products` 至少满足一个。
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 459–472 行；表格顶层字段 9 行。

<!-- source-excerpt node=06 section=业务配置 start=459 end=472 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `entity_level` | `string` | `parent_listing` | 可选 `marketplace_item`、`variant`、`offer`，决定父子体和多 Offer 合并粒度。 |
| `target_count` | `integer` | `30` | 最终目标竞品数的唯一配置源；“Top 30”是模板默认值，不是节点硬上限。实际采用值回传至 `collection_summary.requested_count`。 |
| `candidate_oversampling` | `float` | `3.0` | 先扩大候选池再筛同类性，避免过滤后样本不足。 |
| `include_sponsored` | `boolean` | `true` | 广告位与自然位必须分开标记。 |
| `freshness_policy` | `object` | 版本化配置 | 价格、库存、排名的 TTL 短于静态属性。 |
| `comparability_threshold` | `float` | `0.75` | 直接竞品最低同类性；需按类目校准。 |
| `uncertain_candidate_policy` | `string` | `review` | 低置信候选进入相邻竞品、排除或人工复核。 |
| `evidence_level` | `string` | `field` | 关键字段建议字段级证据。 |
| `adapter_version` | `string` | 固定稳定版本 | 页面/API 结构变化时可追溯并可停止错误适配器。 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 497–508 行；表格顶层字段 5 行。

<!-- source-excerpt node=06 section=输出 start=497 end=508 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `competitor_set_id` | `string` | 由平台、站点、研究条件、时间及方法版本生成的集合 ID。 |
| `competitors` | `list<object>` | 去重后的竞品，包含商品事实、公开信号、发现位置、同类性、新鲜度和证据。 |
| `excluded_candidates` | `list<object>` | 被排除的候选及原因码。 |
| `collection_summary` | `object` | 请求、候选、去重、直接/相邻/排除数量和采集时间。 |
| `data_quality` | `object` | 关键字段覆盖、新鲜率、冲突数、置信度和限制。 |

每个 `competitors[]` 至少包含平台商品/父体/变体 ID、URL、品牌标题、类目、条件化价格、评分及评论数、属性、变体摘要、卖点、媒体、公开信号、`discovery_occurrences`、`comparability`、`freshness` 和证据 ID。
<!-- /source-excerpt -->

<a id="node-07"></a>

### 07. 竞品对标分析

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 515–595 行。
- 覆盖：输入 8 行、业务配置 8 行、输出 6 行，共 22 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 自有商品、竞品、市场与分析目标为必填；`analysis_objective` 的四个值由“如”引出，是示例，可提供预设候选但不擅自封闭枚举。
- 策略对象与 `feature_rubric_version` 均未给实际默认 ID/内容；`benchmark_statistics` 可用多值控件，`compliance_guardrail` 建议开。
- 输出中的维度状态、差距和优先级保持字段说明；本目录不生成对标数据。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 521–533 行；表格顶层字段 8 行。

<!-- source-excerpt node=07 section=输入 start=521 end=533 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `own_product` | `object` | 是 | 自有商品事实、Listing、变体、媒体和价格；未知字段保持未知。 |
| `competitors` | `list<object>` | 是 | 建议直接使用节点 6 的输出，必须带同类性、新鲜度和证据。 |
| `market_context` | `object` | 是 | 平台、站点、语言、币种和类目。 |
| `analysis_objective` | `string` | 是 | 如 `new_product_positioning`、`listing_conversion`、`content_gap`、`pricing`。 |
| `keyword_evidence` | `list<object>` | 否 | 关键词、来源、搜索量/趋势和时间；无来源时只能分析覆盖，不能声称热度。 |
| `review_evidence` | `list<object>` | 否 | 评论主题、样本量、时间窗和证据。 |
| `own_performance` | `object` | 否 | 自有曝光、CTR、CVR、退货等，必须定义统计窗口和口径。 |
| `business_constraints` | `object` | 否 | 商品不可改变的事实、成本、品牌定位、素材能力和禁止声明。 |
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 534–546 行；表格顶层字段 8 行。

<!-- source-excerpt node=07 section=业务配置 start=534 end=546 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `peer_policy` | `object` | 直接竞品为统计基准 | 相邻竞品仅用于定位/趋势探索。 |
| `freshness_policy` | `object` | 版本化配置 | 价格、排名、内容和评论分别定义最大时效。 |
| `normalization_policy` | `object` | 当前稳定版本 | 币种、单位、包装量和变体层级统一规则。 |
| `benchmark_statistics` | `list<string>` | `median,p25,p75,top_quartile` | 避免只看最大值或简单平均。 |
| `feature_rubric_version` | `string` | 固定版本 | 文本、图片、视频、变体和评论特征定义。 |
| `missing_value_policy` | `string` | `skip_and_lower_confidence` | 未知值不按 0 处理。 |
| `priority_policy` | `object` | 分档规则 | 输出行动优先级，而非虚假精确 ROI。 |
| `compliance_guardrail` | `boolean` | `true` | 过滤无法证明、潜在侵权或违规建议。 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 579–589 行；表格顶层字段 6 行。

<!-- source-excerpt node=07 section=输出 start=579 end=589 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `analysis_summary` | `object` | 直接/相邻竞品数、目标、整体置信度、关键发现和局限。 |
| `benchmarks` | `list<object>` | 维度、特征、样本数、覆盖率、中位数/分位数、单位、置信度和证据。 |
| `dimension_results` | `list<object>` | 自有值、基准、`behind/parity/ahead/unknown`、差距严重度和证据。 |
| `gaps` | `list<object>` | 差距 ID、类型、描述、影响对象、严重度和证据。 |
| `opportunities` | `list<object>` | 建议动作、作用机制、P0/P1/P2、影响、证据、可行性、成本、风险和依赖。 |
| `data_quality` | `object` | 样本量、字段覆盖、新鲜度、模型抽取质量及不可比较项。 |
<!-- /source-excerpt -->

<a id="node-08"></a>

### 08. 成本利润与定价测算

- 推荐分组：**商品准备与选品**。
- 原文节点范围：[1-8.md](sources/1-8.md) 第 596–724 行。
- 覆盖：输入 13 行、业务配置 10 行、输出 7 行，共 30 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `product_cost_profile` 只收非金额商品事实；全部金额/费率成本保留在 `cost_items`，避免 UI 在商品事实组另建采购或物流成本入口。
- `pricing_input` 的折前价、卖家折扣、平台买家折扣、卖家应收补贴、买家运费、税与可选实付观察值有独立身份；可拆卖家标签，仍归属原对象，不合并成单个“优惠”。
- `tax_mode` 必须显式选择；原文给三个中文语义但没有机器枚举键。其余策略对象无完整子 Schema 和字面默认；不预填费率、税额、价格范围或敏感性范围。

#### 原文摘录：输入

来源：[1-8.md](sources/1-8.md) 第 601–622 行；表格顶层字段 13 行。

<!-- source-excerpt node=08 section=输入 start=601 end=622 -->
| 变量名 | 类型 | 必填 | 说明与约束 |
| --- | --- | --- | --- |
| `product_cost_profile` | `object` | 是 | 仅包含 SKU、包装尺寸/重量、原产地和数量等非金额商品事实；不承载采购或物流成本。 |
| `market_context` | `object` | 是 | 平台、站点、目的国、结算币种和计算时间。 |
| `fulfillment_scenarios` | `list<object>` | 是 | Amazon FBA/FBM、TikTok 平台履约/商家履约等情景及参数。 |
| `pricing_input` | `object` | 是 | 当前/候选价格或搜索区间，以及折扣、补贴、买家运费和含税口径；字段定义见下文。 |
| `cost_items` | `list<object>` | 是 | 采购、头程、清关、包装、仓储、广告、联盟、退货等金额/费率的唯一权威输入。 |
| `fee_policy_refs` | `list<object>` | 条件必填 | 平台佣金、交易、履约和仓储规则引用、版本及有效期。 |
| `exchange_rates` | `list<object>` | 条件必填 | 多币种时必须提供或由授权服务获取，包含汇率时间和来源。 |
| `tax_profile` | `object` | 条件必填 | 含税市场、VAT/GST/销售税或进口税参与时提供。 |
| `customs_profile` | `object` | 否 | HS 编码、原产地、目的地、税基和规则引用。 |
| `competitor_price_context` | `object` | 否 | 节点 7 的直接竞品单位价格带、样本量、同类性和新鲜度。 |
| `target_metrics` | `object` | 否 | 目标贡献率、完全成本利润率、ROI、最大广告率等。 |
| `uncertainty_ranges` | `list<object>` | 否 | 汇率、运费、广告、退货等驱动的低/基准/高值；每个驱动独立一项。 |
| `volume_assumptions` | `object` | 否 | 月销量、批量和仓储月数；完全成本分摊时必需。 |

`pricing_input` 必须显式区分：`gross_item_price`（折扣前商品价）、`seller_funded_discount`、`platform_funded_buyer_discount`、`seller_receivable_platform_subsidy`、`buyer_shipping_charge`、`buyer_tax_if_exclusive`、`tax_included` 和可选 `buyer_paid_amount_observed`。计算权威顺序是先由前述分项推导买家支付与卖家结算前收入，再用观察值做校验；观察值与推导值不一致时返回冲突，不能覆盖公式。只有明确结算给卖家的补贴才进入卖家收入，买家折扣与卖家应收补贴不得用同一个金额重复计入。

`cost_items[]` 必须声明 `cost_item_id`、`cost_code`、金额/费率、币种、`per_unit/per_order/per_shipment/per_period/percent_of_revenue` 计费基础、数量、卖方是否承担、时间、来源和置信度。对同一 `sku_id + scenario_id + cost_code + basis + effective_period` 只允许一个 canonical 成本项；如 Policy Store 与自定义输入同时命中，默认视为 `DOUBLE_COUNT_RISK`，除非显式 `override_of_cost_item_id` 且审计记录允许覆盖。未知成本不能用 0 代替。
<!-- /source-excerpt -->

#### 原文摘录：业务配置

来源：[1-8.md](sources/1-8.md) 第 623–639 行；表格顶层字段 10 行。

<!-- source-excerpt node=08 section=业务配置 start=623 end=639 -->
| 配置项 | 类型 | 建议默认值 | 说明 |
| --- | --- | --- | --- |
| `calculation_view` | `string` | `contribution_and_fully_loaded` | 同时输出贡献利润和可用时的完全分摊利润。 |
| `tax_mode` | `string` | 必须显式选择 | 含税价拆税、税额另加或不计间接税。 |
| `fee_lookup_policy` | `object` | 版本化规则 | 按平台、站点、类目、履约、尺寸档和生效日选择。 |
| `currency_policy` | `object` | 明确来源和最大时效 | 结算汇率、计划汇率或现货汇率不能混用。 |
| `allocation_policy` | `object` | 按成本项配置 | 批次/周期费用按件数、重量、体积或销量分摊。 |
| `returns_policy` | `object` | 当前稳定版本 | 明确退款、费用返还、库存恢复和报废损失口径。 |
| `rounding_policy` | `object` | 按收费规则 | 金额内部使用 Decimal/最小货币单位，最后按规则层级舍入。 |
| `missing_cost_policy` | `string` | `fail_affected_scenario` | 不得把关键缺失成本默认成 0。 |
| `price_search_policy` | `object` | 显式范围 | 搜索上下界、步长、平台价格约束和目标利润率。 |
| `sensitivity_policy` | `object` | 使用输入范围 | 不静默采用通用 ±10%。 |

平台费率、税费和履约费不硬编码在节点代码中，必须按 `marketplace + category + fulfillment_mode + effective_at` 从版本化 Policy Store 解析。
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[1-8.md](sources/1-8.md) 第 708–719 行；表格顶层字段 7 行。

<!-- source-excerpt node=08 section=输出 start=708 end=719 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `calculation_currency` | `string` | 统一计算币种。 |
| `scenario_results` | `list<object>` | 每个 SKU/履约/价格情景的收入、逐项账本、利润、利润率、ROI、盈亏平衡和置信度。 |
| `price_recommendation` | `object` | `feasible/no_benchmark_overlap/no_feasible_price/insufficient_market_data`、经济底线、促销底线、允许域、经济可行带、市场观察带和交集。 |
| `profit_curve` | `list<object>` | 价格点、贡献利润、完全成本利润和利润率，用于后续图表或决策。 |
| `sensitivity` | `list<object>` | 驱动项低/基准/高输入、利润变化和盈亏平衡位移。 |
| `assumptions_used` | `list<object>` | 所有输入假设、来源、时间和置信度。 |
| `formula_manifest` | `list<object>` | 费用项公式、计费基础、规则 ID/版本和中间值。 |
<!-- /source-excerpt -->

<a id="node-09"></a>

### 09. Listing 综合诊断

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 3–155 行。
- 覆盖：输入 11 行、业务配置 0 行、输出 18 行，共 29 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `diagnosis_config` 保持必填对象，可按输入说明提供诊断模式/维度/观察窗口等卖家分区；`live/draft_precheck` 有明确值，其他子键、单位、候选和默认未完整定义。
- `current_listing_snapshots` 为版本角色列表，模式对应的基线条件显示在输入旁；`target` 仍为单目标对象。A+ 来源说明保留为帮助文本，不添加读取按钮或接口调用。
- 关键词、平台观测、绩效、评论、权利和对标对象为补充输入，不因未填而伪造默认数据。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 9–24 行；表格顶层字段 11 行。

<!-- source-excerpt node=09 section=输入 start=9 end=24 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `current_listing_snapshots` | `list<object>` | 是 | 同一商品的版本化快照集；`live` 模式必须含 live，`draft_precheck` 必须含 draft 或 audit candidate，其他版本可作为对照。每项包含角色、seller SKU、状态、版本／更新时间、标准 Listing 字段、属性、变体、媒体、价格、库存、履约、平台 issue／audit／warning 及内容哈希；平台 product ID／ASIN 仅在平台已创建对象时必填，未上架新品使用 seller SKU + 不可变 draft artifact ID 绑定基线。Amazon A+ 必须从 A+ Content API 独立取得正文、metadata/status 和 ASIN 关系，并保存 `contentReferenceKey`、`retrieved_at` 与内部计算的 `document_hash`；不能假设 Listings Items 返回 A+ 正文或平台提供稳定文档版本号 |
| `product_snapshot` | `object` | 是 | 不可变标准商品事实、SKU 真值、包装／尺寸／数量、适用范围、声明证据及 `facts_hash` |
| `target` | `object` | 是 | `platform`、shop／seller、marketplace、country、locale、类目／product type 和货币；一次只诊断一个目标 |
| `rule_bundle_ref` | `string` | 是 | 当前目标的字段 Schema、必填／条件必填、字符计量、媒体、禁限售、声明及本地化规则快照 |
| `diagnosis_config` | `object` | 是 | `live` 或 `draft_precheck` 模式、诊断维度、观察窗口、样本门槛、严重度规则、优先级权重、允许的缓存时长及人工复核门槛 |
| `keyword_asset` | `object` | 否 | 节点 11 输出或等价关键词资产；缺失时可做基础语义诊断，但不得宣称完成真实搜索需求覆盖分析 |
| `platform_observations` | `object` | 否 | 平台只读接口返回的 buyable／discoverable、issues、restrictions、audit、listing quality、warning、推荐、关联内容版本和获取时间；必须保留平台原始 code，用作动态状态证据而非重复的内容基线 |
| `performance_observations` | `list<object>` | 否 | 搜索曝光、点击、加购、购买、页面流量、转化和渠道归因；每条必须带来源、时间窗、时区、粒度、口径和数据延迟，organic、paid、video、LIVE、product card 不混算 |
| `review_feedback` | `object` | 否 | 评论主题、星级趋势、退货／退款原因、问答和客服主题；应去除个人信息并记录样本范围 |
| `rights_compliance_evidence` | `object` | 否 | 品牌授权、商标／版权素材授权、专利／外观筛查记录、认证、测试报告、警示标签、制造商／责任人等证据及有效期 |
| `benchmark_snapshot` | `object` | 否 | 历史版本、同类基线或可比竞品的合规公开指标；只能用于相对比较，不能替代平台规则和商品事实 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 112–134 行；表格顶层字段 18 行。

<!-- source-excerpt node=09 section=输出 start=112 end=134 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据、trace、模型／规则版本及开始结束时间 |
| `diagnosis_id` | `string` | 本次诊断唯一 ID |
| `diagnosis_state` | `string` | `complete`、`partial`、`stale` 或 `blocked` |
| `baseline` | `object` | 平台、目标身份、选定 Listing role／version／content hash、A+ 的 document hash／retrieved_at／contentReferenceKey／metadata status（如适用）、facts hash、规则版本、关键词 asset ID／version／hash／target（如适用）及各数据窗口 |
| `scope_coverage` | `list<object>` | 每个维度的 `diagnosed`、`not_diagnosed` 或 `not_applicable`、数据新鲜度、样本量与缺失原因 |
| `platform_status` | `object` | live／buyable／discoverable／audit／restriction／listing quality 及平台原始 code；不推导为综合合规结论 |
| `dimension_assessments` | `list<object>` | 完整度、搜索、转化、可读性、本地化、素材一致性、合规／IP、Offer／库存／履约和反馈等已执行维度的 `healthy`、`issue_found` 或 `unknown`、可选分数、置信度与证据 |
| `issues` | `list<object>` | 字段／SKU／媒体级 issue ID、维度、观察值、预期条件、P0–P3、证据、置信度、平台 code、根因组、`remediation_domain`、`content_optimizable` 和修复 brief |
| `root_cause_groups` | `list<object>` | 症状、候选根因、支持／反证、受影响范围及因果置信度 |
| `effective_claim_ledger` | `object` | 跨字段与媒体的完整原子声明账本；含 ledger ID／hash、target、facts hash、rule version、evidence snapshot hash、完整性状态，以及每条声明的适用 SKU、事实／证据、状态、范围和禁止改写边界 |
| `cross_field_matrix` | `object` | Listing、属性、变体、图片、视频、包装和商品事实的一致性结果 |
| `search_diagnostics` | `object` | 意图覆盖、关键词放置、查询漏斗、organic／paid 边界和数据限制 |
| `conversion_diagnostics` | `object` | 曝光到购买漏斗、样本充分性、内容与经营干扰项及候选原因 |
| `compliance_ip_screening` | `object` | 规则命中、声明证据、权利来源、有效期和人工复核项；只表达风险，不裁定侵权 |
| `prioritized_backlog` | `list<object>` | 去重后的修复顺序、影响、证据、依赖、责任角色、`remediation_domain`、`content_optimizable`、禁止改动项和完成判断；不含替换文案或 payload |
| `review_tasks` | `list<object>` | 需要卖家、运营、法务／合规或商品负责人确认的事项 |
| `data_quality_report` | `object` | 缺失、过期、权限、口径、归因、样本和污染窗口说明 |
| `optimization_scope` | `object` | 仅收录 `content_optimizable=true` 的 issue IDs、字段范围、锁定事实、关键词资产版本、保留项与禁止改动项；价格、库存、履约、身份、执法、合规／IP 问题不得进入，且不包含生成内容或平台提交指令 |
<!-- /source-excerpt -->

<a id="node-10"></a>

### 10. Listing 一键优化

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 156–281 行。
- 覆盖：输入 14 行、业务配置 0 行、输出 12 行，共 26 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `execution_mode` 为明确的 `full_generate/assemble_only` 选择，但没有默认值；`optimization_config` 内层未给完整 Schema，不把候选标签当新增字段。
- 快照、关键词、声明账本、变体产物和组件输出的条件必填按输入原文呈现；纯新品省略条件与老品要求分开提示。
- `component_outputs` 的明确引用槽是 `title_result/selling_point_result/detail_result/variant_copy_result`；节点 15 不在此对象引用范围。UI 只编辑/绑定这些输入，不触发组装执行。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 162–180 行；表格顶层字段 14 行。

<!-- source-excerpt node=10 section=输入 start=162 end=180 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 不可变标准商品事实快照；运行前重算 `facts_hash` |
| `target` | `object` | 是 | 一次只处理一个平台、站点和 locale；多目标由 Batch 展开 |
| `rule_bundle_ref` | `string` | 是 | 当前目标规则快照 |
| `current_listing_snapshots` | `list<object>` | 条件必选 | 老品、已有 draft／audit candidate，或提供 `diagnosis_result` 时必选，并包含节点 9 所诊断的不可变基线，使节点 10 可重算 content hash；老品必须含 live，其他版本仅在实际存在时传入。只有不使用诊断结果、从零生成的纯新品可省略 |
| `diagnosis_result` | `object` | 否 | 节点 9 输出；仅消费其 `optimization_scope` 中 `content_optimizable=true` 的 issue，不能把价格、库存、履约、身份、执法、合规／IP 等 P0/P1 当作内容改写任务 |
| `keyword_asset` | `object` | 条件必选 | 节点 11 完整输出；`full_generate` 缺失时可内部调用相同组件，`assemble_only` 任一组件引用关键词时必须显式提供并核对 ID/version/hash |
| `claim_ledger` | `object` | 条件必选 | `full_generate` 缺失时可从事实构建；`assemble_only` 必须由本字段或 `diagnosis_result.effective_claim_ledger` 提供完整账本 |
| `competitor_gaps` | `list<object>` | 否 | 只用于识别差异化机会，不复制受保护表达 |
| `brand_voice` | `object` | 否 | 语气、品牌术语、禁用表达和样例 |
| `media_assets` | `list<object>` | 否 | 详情/A+ 可用图片、视频、Alt 文本证据 |
| `variant_builder_artifact` | `object` | 条件必选 | `full_generate` 涉及变体文案时必选；封装第一阶段 `VariantBuilderOutputV1`、稳定 payload hash 及排除路径 |
| `optimization_config` | `object` | 是 | 模式、字段范围、候选数、保留字段、审核门槛和组件版本 |
| `execution_mode` | `string` | 是 | `full_generate` 或 `assemble_only` |
| `component_outputs` | `object` | 条件必选 | `assemble_only` 时使用强类型 `title_result/selling_point_result/detail_result/variant_copy_result`；只接收节点 12、13、14、16，不包含节点 15 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 252–268 行；表格顶层字段 12 行。

<!-- source-excerpt node=10 section=输出 start=252 end=268 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据 |
| `optimization_id` | `string` | 本次优化 ID |
| `effective_claim_ledger` | `object` | 本次各字段共同使用的完整声明账本；内部构建时也必须返回 |
| `optimization_state` | `string` | `generated`、`baseline_preserved` 或 `no_valid_candidate` |
| `content_package` | `object` | 条件输出；有有效候选或可明确保留的基线时才返回 `ListingContentPackageV1` |
| `change_set` | `list<object>` | 字段级前后值、原因和证据 |
| `component_traces` | `list<object>` | 关键词、标题、卖点、详情、变体组件的版本、输入/输出哈希与结果引用；不包含后续节点 15 |
| `validation_report` | `object` | Schema、事实、声明、关键词、跨字段和渲染校验 |
| `review_tasks` | `list<object>` | 人工确认项 |
| `payload_previews` | `list<object>` | 条件输出；每个 HTTP 请求一个强类型预览，含依赖顺序，不含凭证、不执行提交；Listing、A+ 文档和 ASIN relations 可同时存在 |
| `apply_eligibility` | `string` | `ready_for_review`、`review_required`、`blocked`；不表示可发布 |
| `platform_readiness` | `object` | 结构就绪、上架资格、预检、提交和异步处理的分离状态 |
<!-- /source-excerpt -->

<a id="node-11"></a>

### 11. SEO 关键词挖掘

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 282–427 行。
- 覆盖：输入 10 行、业务配置 0 行、输出 6 行，共 16 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 种子词、第一方观测、官方推荐、竞品、评论和既有关键词资产各自保留可选来源输入，不合并丢失字段身份。
- `keyword_config` 的来源优先级、意图分类、权重、证据、最大候选和放置策略仅有说明，内层键、完整枚举、数值范围和默认未定义；配置区使用既有对象编辑/绑定方案。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 288–302 行；表格顶层字段 10 行。

<!-- source-excerpt node=11 section=输入 start=288 end=302 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 不可变标准商品事实快照；运行前重算 `facts_hash` |
| `target` | `object` | 是 | 平台、市场、locale、类目/商品类型 |
| `rule_bundle_ref` | `string` | 是 | 字段、禁词和计量规则 |
| `seed_terms` | `list<object>` | 否 | 卖家种子词，含原始语言和来源 |
| `first_party_observations` | `list<object>` | 否 | Amazon Brand Analytics/广告 Search Term 或 TikTok Shop 搜索/SEO 数据；必须标明数据表面与样本条件 |
| `official_recommendations` | `list<object>` | 否 | 平台官方推荐词及获取时间 |
| `competitor_corpus` | `list<object>` | 否 | 可比竞品标题/卖点/属性；需带商品、站点和采集时间 |
| `review_corpus` | `list<object>` | 否 | 评论/问答主题及样本范围，不含个人标识 |
| `existing_keyword_asset` | `object` | 否 | 增量更新时使用 |
| `keyword_config` | `object` | 是 | 来源优先级、意图分类、评分权重、最低证据、最大候选数和放置策略 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 405–415 行；表格顶层字段 6 行。

<!-- source-excerpt node=11 section=输出 start=405 end=415 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据 |
| `keyword_asset` | `object` | `KeywordAssetV1`，含候选、词群、意图、分数、证据和完整 exclusion ledger，防止下游重新引入排除词 |
| `placement_plan` | `list<object>` | 平台字段、词群、优先级、预算成本和理由 |
| `excluded_terms` | `list<object>` | 原词、排除原因、风险和证据 |
| `source_coverage` | `object` | 来源等级、窗口、指标和新鲜度概况 |
| `unresolved_concepts` | `list<object>` | 事实不足、歧义或需本地专家确认的概念 |
<!-- /source-excerpt -->

<a id="node-12"></a>

### 12. 商品标题优化

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 428–540 行。
- 覆盖：输入 10 行、业务配置 0 行、输出 8 行，共 18 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `current_title` 是对象而非普通标题字符串，保持 `ContentUnitV1` 输入说明；`current_amazon_item_highlights` 单独保留可选对象。
- `title_config` 可按生成模式、候选数、最小改动、目标槽位、权重和锁定片段分区，但内层 Schema 与默认未定义；品牌保护片段和人工编辑简报分别保留。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 434–448 行；表格顶层字段 10 行。

<!-- source-excerpt node=12 section=输入 start=434 end=448 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 不可变商品事实和变体快照 |
| `target` | `object` | 是 | 平台、站点、locale、类目/商品类型 |
| `rule_bundle_ref` | `string` | 是 | 标题长度、字符、重复、模板和类目规则 |
| `keyword_asset` | `object` | 是 | 目标语言关键词资产 |
| `claim_ledger` | `object` | 是 | 可用声明及限定条件 |
| `current_title` | `object` | 否 | 改写/压缩/最小修复模式的 `ContentUnitV1` |
| `current_amazon_item_highlights` | `object` | 否 | Amazon 老品改写时与 Item name 一起读取，用于迁移和去重 |
| `protected_tokens` | `list<object>` | 否 | 品牌、型号、标准缩写、商标大小写及不可翻译片段 |
| `optimization_brief` | `object` | 否 | 人工确认后的可编辑路径、目标 issue、锁定片段和改动预算 |
| `title_config` | `object` | 是 | 生成模式、候选数、最小改动、目标槽位、评分权重和人工锁定片段 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 516–528 行；表格顶层字段 8 行。

<!-- source-excerpt node=12 section=输出 start=516 end=528 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据 |
| `selected_title` | `object` | 条件输出；有通过硬门禁的候选时才存在，含 segment、计数和 claim/keyword/evidence 引用 |
| `amazon_item_highlights` | `object` | Amazon 目标且 capability 支持时输出；包含真实字段路径、文本和校验 |
| `alternatives` | `list<object>` | 通过门禁的备选标题和维度得分 |
| `rejected_candidates` | `list<object>` | 候选、失败规则和字段证据 |
| `coverage_report` | `object` | 核心概念覆盖、重复度、可读性和本地语言检查 |
| `omitted_terms` | `list<object>` | 未放入标题的词及原因 |
| `change_summary` | `object` | 与当前标题的差异、变更风险和建议审核级别 |
<!-- /source-excerpt -->

<a id="node-13"></a>

### 13. 核心卖点／五点描述生成

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 541–674 行。
- 覆盖：输入 11 行、业务配置 0 行、输出 8 行，共 19 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 当前卖点、评论洞察与竞品缺口是不同对象列表；受众上下文、声明和关键词各保留原字段与必填性。
- `selling_point_config` 描述目标条数、主题权重、结构、重复阈值、候选数及品牌语气；原文未给数字或固定“必须五条”，不能因节点名称把条数预填为 5。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 549–564 行；表格顶层字段 11 行。

<!-- source-excerpt node=13 section=输入 start=549 end=564 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 不可变商品事实、属性、包装内容和变体快照 |
| `target` | `object` | 是 | 平台、市场、locale、类目/商品类型 |
| `rule_bundle_ref` | `string` | 是 | bullet/highlight/描述块的当前规则与能力 |
| `claim_ledger` | `object` | 是 | 允许、受限、禁止声明及证据 |
| `keyword_asset` | `object` | 否 | 用于自然覆盖，不以堆词为目的 |
| `audience_context` | `object` | 否 | 目标人群、购买任务、使用阶段；必须与事实和市场相容 |
| `review_insights` | `list<object>` | 否 | 用户痛点主题、样本量和证据 |
| `competitor_gaps` | `list<object>` | 否 | 可比竞品内容空白，不含可复制表达 |
| `current_selling_points` | `list<object>` | 否 | 改写或最小修改使用 |
| `optimization_brief` | `object` | 否 | 人工确认后的可编辑路径、目标 issue、锁定片段和改动预算 |
| `selling_point_config` | `object` | 是 | 目标条数、主题权重、结构、重复阈值、候选数和品牌语气 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 650–662 行；表格顶层字段 8 行。

<!-- source-excerpt node=13 section=输出 start=650 end=662 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据 |
| `selling_points` | `list<object>` | 文本、结构、顺序、claim/keyword/evidence 和适用 SKU |
| `amazon_bullet_points` | `list<object>` | Amazon 目标时输出，每条带内容、声明、关键词与证据；非 Amazon 标为不适用 |
| `tiktok_product_highlights` | `list<object>` | 能力支持时输出，每条带内容和 lineage |
| `fallback_description_block` | `object` | TikTok Shop 不支持独立 highlights 时使用 |
| `coverage_matrix` | `list<object>` | 主题、事实、用户问题和关键词覆盖 |
| `rejected_claims` | `list<object>` | 无证据、受限或禁止声明及原因 |
| `validation_report` | `object` | 长度、规则、事实、重复和跨 SKU 校验 |
<!-- /source-excerpt -->

<a id="node-14"></a>

### 14. 商品详情描述／A+ 内容生成

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 675–812 行。
- 覆盖：输入 12 行、业务配置 0 行、输出 9 行，共 21 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `a_plus_context` 是 Amazon 的可选上下文；详情、媒体、FAQ、当前版本与人工简报分别编辑/绑定；不以 A+ 作为全部平台通用必填组。
- `detail_config` 的内容目标、模块偏好、最大模块数、重复阈值和资产策略没有完整子 Schema/默认；`selling_points` 的节点 13 引用保留为字段说明，不据此建立自动执行顺序。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 683–699 行；表格顶层字段 12 行。

<!-- source-excerpt node=14 section=输入 start=683 end=699 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 不可变商品事实、属性、包装、变体和使用信息快照 |
| `target` | `object` | 是 | 平台、站点、locale、类目/商品类型 |
| `rule_bundle_ref` | `string` | 是 | 描述字段、HTML、A+ 模块、图片和类目规则 |
| `claim_ledger` | `object` | 是 | 可用声明及限定条件 |
| `keyword_asset` | `object` | 否 | 详情词群，不能主导事实 |
| `selling_points` | `list<object>` | 否 | 节点 13 输出，用于互补和去重；精细流程中建议明确为 13 → 14 |
| `media_assets` | `list<object>` | 否 | 已存在的图片/视频引用、权利状态、尺寸和内容标签 |
| `a_plus_context` | `object` | 否 | Amazon 的资格/状态、contentReferenceKey、当前与目标全量 ASIN 集合及哈希、完整快照、移除审批和 API 模型 |
| `faq_inputs` | `list<object>` | 否 | 用户真实问题或卖家提供的 FAQ；答案仍需事实支持 |
| `current_detail` | `object` | 否 | 现有标准描述/A+/TikTok Shop HTML 描述 |
| `optimization_brief` | `object` | 否 | 人工确认后的可编辑路径、目标 issue、锁定内容和改动预算 |
| `detail_config` | `object` | 是 | 内容目标、模块偏好、最大模块数、重复阈值和资产策略 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 783–796 行；表格顶层字段 9 行。

<!-- source-excerpt node=14 section=输出 start=783 end=796 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据 |
| `content_mode` | `string` | `amazon_standard`、`amazon_a_plus` 或 `tiktok_description` |
| `standard_description` | `object` | 纯文本/允许格式描述及声明、关键词引用 |
| `a_plus_plan` | `object` | Amazon 编辑蓝图、完整 ContentDocument artifact、当前/目标全量 ASIN 集合及哈希、增删差异、移除审批、关系校验状态、资产需求和资格/文档状态 |
| `tiktok_description` | `object` | HTML、纯文本、内容块和字段能力 |
| `content_modules` | `list<object>` | 平台中立的结构化模块 |
| `asset_requirements` | `list<object>` | 缺失素材的用途、尺寸/比例、文案和证据要求 |
| `seller_questions` | `list<object>` | 无事实答案的 FAQ/披露问题 |
| `validation_report` | `object` | Schema、事实、声明、资产、HTML 和跨字段检查 |
<!-- /source-excerpt -->

<a id="node-15"></a>

### 15. 多语言翻译与本地化

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 813–964 行。
- 覆盖：输入 18 行、业务配置 0 行、输出 16 行，共 34 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `source_locale` 明确 BCP-47；`target` 是同平台目标市场对象；源包、事实、账本、验证报告各自保留必填输入。
- `target_keyword_asset` 标明 `market_localization` 条件必填；该字符串不能据此补齐整个模式枚举。`localization_config` 内层模式/策略/门槛未给完整 Schema 和默认。
- `local_override_inventory_complete` 是可选布尔，原文无默认，不能将未设置静默当作 true 或 false；三个跨市场快照、目标商品 ID 和本地覆盖列表保持各自身份。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 825–847 行；表格顶层字段 18 行。

<!-- source-excerpt node=15 section=输入 start=825 end=847 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `source_content_package` | `object` | 是 | 已通过事实校验的源语言内容包 |
| `source_product_snapshot` | `object` | 是 | 生成源包时使用的不可变 `ProductFactsSnapshotV1`；用于重算 product/facts identity |
| `source_claim_ledger` | `object` | 是 | 源内容包引用的完整 `ClaimLedgerV1`，用于重新验证声明和限定词 |
| `source_validation_report` | `object` | 是 | 源内容包对应的完整 `ValidationReportV1`；ID、不可变 hash、规则和通过状态必须与 package 一致 |
| `source_locale` | `string` | 是 | BCP-47 locale；必须等于源内容包 target.locale |
| `target` | `object` | 是 | 同平台的目标市场、locale、类目/商品类型；跨 Amazon/TikTok Shop 不走翻译节点 |
| `rule_bundle_ref` | `string` | 是 | 目标市场字段、语言、类目和本地化规则 |
| `target_keyword_asset` | `object` | 条件必选 | `market_localization` 必选；product/facts/target/category/locale/rule/hash 必须全部匹配 |
| `terminology` | `list<object>` | 否 | 品牌术语、批准译法、禁译词、法定术语、大小写和适用 locale |
| `translation_memory` | `list<object>` | 否 | 已确认分段及质量/来源 |
| `locked_entities` | `list<object>` | 否 | 品牌、型号、GTIN、SKU、认证编号、URL/代码和人工锁定片段 |
| `local_overrides` | `list<object>` | 否 | 目标市场人工定制字段，默认不得覆盖 |
| `source_management_snapshot` | `object` | 否 | 当前 Product Management workflow 下的跨市场源商品完整快照；含 canonical product、merchant/target 授权、workflow、raw ref、hash 和覆盖域 |
| `source_listing_snapshot` | `object` | 否 | 跨市场同步时的权威源市场 Listing 快照；用于绑定源 platform product ID、marketplace、locale 与店铺 |
| `current_target_listing` | `object` | 否 | 当前目标市场本地 Listing 快照，含 target/product ID、版本角色、字段值与 hash；用于身份与并发校验 |
| `target_market_product_id` | `string` | 否 | 目标市场商品 ID；用于防止把跨市场更新应用到错误商品 |
| `local_override_inventory_complete` | `boolean` | 否 | 是否已完整获取当前 workflow 更新可能覆盖的本地定制字段 |
| `localization_config` | `object` | 是 | 模式、单位策略、术语冲突策略、质量门槛和人工审核级别 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 931–951 行；表格顶层字段 16 行。

<!-- source-excerpt node=15 section=输出 start=931 end=951 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据 |
| `localized_content_package` | `object` | 条件输出；关键实体/数值未阻断时返回目标 locale 的 `ListingContentPackageV1` |
| `effective_target_claim_ledger` | `object` | 目标规则重评后的完整声明账本；以源账本为 parent，但有独立 ID/hash/target/rules |
| `segment_alignments` | `list<object>` | 源/目标分段、claim、术语、状态和质量问题 |
| `field_ownership` | `list<object>` | 跨市场继承、平台翻译、本地覆盖和锁定状态 |
| `entity_integrity` | `object` | 品牌、型号、SKU、数字、单位和否定关系校验 |
| `localized_attribute_mapping` | `list<object>` | source/global category、attribute、value ID 到 target/local ID 的显式映射、状态与证据 |
| `image_translation_tasks` | `list<object>` | 图片文字翻译的 capability、task ID、源资产、目标 locale、异步状态和错误 |
| `unresolved_terms` | `list<object>` | 歧义、术语冲突、法定/高风险文本和处理建议 |
| `translation_memory_updates` | `list<object>` | 仅包含经批准可回写的分段建议 |
| `patch_strategy` | `object` | 保护本地覆盖的后续更新策略 |
| `target_baseline_hash` | `string` | 老品目标 Listing 的并发基线；新品可缺失 |
| `change_set` | `list<object>` | 本地化前后字段级 diff、声明/关键词来源与审批状态 |
| `payload_previews` | `list<object>` | 条件输出；按目标平台当前 create/edit/replicate workflow 生成的一个或多个强类型、可重算请求预览 |
| `apply_eligibility` | `string` | `ready_for_review`、`review_required` 或 `blocked`；不代表已发布/已审核 |
| `platform_readiness` | `object` | 目标平台适用的 Schema、新品检查或老品 edit/audit 状态 |
<!-- /source-excerpt -->

<a id="node-16"></a>

### 16. 规格名称与变体文案优化

- 推荐分组：**Listing与搜索优化**。
- 原文节点范围：[9-16.md](sources/9-16.md) 第 965–1077 行。
- 覆盖：输入 9 行、业务配置 0 行、输出 10 行，共 19 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 标准变体事实与 `variant_builder_artifact` 分别绑定；保留后者 `output` 及 hash 的输入说明，不在前端生成或改写产物。
- `variant_copy_config` 的单位显示、缩短、碰撞消歧、锁定和未知值策略只有描述，没有完整子 Schema/默认；当前轴值文案、术语和可编辑简报可分组呈现。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[9-16.md](sources/9-16.md) 第 973–986 行；表格顶层字段 9 行。

<!-- source-excerpt node=16 section=输入 start=973 end=986 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 不可变商品及标准变体事实快照 |
| `variant_builder_artifact` | `object` | 是 | 第一阶段节点 4 输出封装；`output` 为原始 `VariantBuilderOutputV1`，hash 覆盖规范轴、SKU、平台结构、报告、问题和 readiness |
| `target` | `object` | 是 | 平台、市场、locale 和目标类目/商品类型 |
| `rule_bundle_ref` | `string` | 是 | 变体主题/Sales Attributes、枚举、长度和自定义值能力 |
| `current_variant_copy` | `list<object>` | 否 | 当前轴名、值名和平台 ID |
| `terminology` | `list<object>` | 否 | 颜色、尺寸、材质、容量、数量等受控词典 |
| `keyword_asset` | `object` | 否 | 仅用于术语一致性，不允许变体标签 SEO 堆词 |
| `optimization_brief` | `object` | 否 | 人工确认后的可编辑轴/值、目标 issue、锁定项和改动预算 |
| `variant_copy_config` | `object` | 是 | 单位显示、缩短、碰撞消歧、人工锁定和未知值策略 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[9-16.md](sources/9-16.md) 第 1049–1063 行；表格顶层字段 10 行。

<!-- source-excerpt node=16 section=输出 start=1049 end=1063 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `meta` | `object` | 通用结果元数据 |
| `optimized_option_definitions` | `list<object>` | 轴 ID、规范概念、平台属性和目标显示名 |
| `sku_display_labels` | `list<object>` | SKU 身份、属性组合和消费者显示标签 |
| `source_to_target_mapping` | `list<object>` | 原始值、规范值、平台 ID/value ID 和目标显示值 |
| `collision_report` | `list<object>` | 碰撞范围、原因、自动消歧或人工任务 |
| `identity_integrity` | `object` | SKU/GTIN/价格/库存关联未改变的校验结果 |
| `family_integrity` | `object` | 品牌、商品类型、核心功能和平台变体主题是否仍属于同一家族 |
| `split_recommendations` | `list<object>` | 不应作为变体的商品及拆分理由 |
| `change_log` | `list<object>` | 字段前后值、规则和原因 |
| `copy_ready` | `boolean` | 只表示文案层可用 |
<!-- /source-excerpt -->

<a id="node-17"></a>

### 17. 商品图片生成

- 推荐分组：**图片与视频**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 5–92 行。
- 覆盖：输入 9 行、业务配置 0 行、输出 9 行，共 18 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `source_assets` 是多图片输入/绑定，`variant_scope` 是必填字符串列表；权利对象、品牌对象、卖点声明、图片 brief 分别保留。
- `image_brief` 与 `generation_config` 可分为图片需求和高级设置；数量/比例/风格/模型/种子/超时等仅有说明，完整子键、选项、范围和默认未定义，不新增模型调用。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 11–24 行；表格顶层字段 9 行。

<!-- source-excerpt node=17 section=输入 start=11 end=24 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 已确认的商品外观、材质、尺寸、颜色、包装清单、功能、限制和变体事实 |
| `source_assets` | `list<image>` | 是 | 商品实拍图、包装图、细节图和 Logo；需标记 SKU、视角和来源 |
| `asset_rights` | `object` | 是 | 素材所有者、授权用途、平台、市场、期限和人物肖像授权 |
| `target` | `object` | 是 | Amazon 或 TikTok Shop、站点、语言、类目和素材位置 |
| `image_brief` | `object` | 是 | 图片类型、数量、比例、风格、信息层级和禁止内容 |
| `approved_claims` | `list<object>` | 是 | 有事实或证据支持、允许视觉化的卖点和声明 |
| `brand_assets` | `object` | 否 | 品牌色、字体、Logo、视觉规范及使用授权 |
| `variant_scope` | `list<string>` | 是 | 本次图片对应的 SKU、颜色和尺寸 |
| `generation_config` | `object` | 是 | 候选数、模型、随机种子、审核门槛、超时和部分成功策略 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 63–76 行；表格顶层字段 9 行。

<!-- source-excerpt node=17 section=输出 start=63 end=76 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `image_set` | `list<image>` | 按用途和 SKU 分组的有效图片候选 |
| `candidate_groups` | `list<object>` | 各位置的备选图、排序和推荐原因 |
| `asset_manifest` | `object` | 图片对应商品、SKU、用途、来源素材和生成方式 |
| `fact_consistency_report` | `object` | 外观、数量、颜色、尺寸、文字和声明检查结果 |
| `rights_report` | `object` | 输入素材、人物、品牌和生成内容的权利状态 |
| `disclosure_advice` | `object` | AI 标记、披露要求和禁止发布位置 |
| `review_tasks` | `list<object>` | 待确认的事实、权利、主图和高风险声明 |
| `missing_capture_requests` | `list<object>` | 因缺少真实视角或细节产生的补拍需求 |
| `task_summary` | `object` | 整体及逐图异步状态、失败原因和重试建议 |
<!-- /source-excerpt -->

<a id="node-18"></a>

### 18. 商品图片处理与平台适配

- 推荐分组：**图片与视频**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 93–181 行。
- 覆盖：输入 9 行、业务配置 0 行、输出 8 行，共 17 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `source_images` 为多图片，`slot_plan` 为图片用途对象列表；变体映射、允许编辑区域、质量阈值分别保留。
- 可选 `upload_mode` 原文只有“仅输出资产/同时上传平台素材服务”两种语义，没有机器枚举或默认；这里只编辑配置，不提供真实上传动作。`processing_config` 内层未完整定义。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 99–112 行；表格顶层字段 9 行。

<!-- source-excerpt node=18 section=输入 start=99 end=112 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `source_images` | `list<image>` | 是 | 原始图片、不可变版本、来源和权利状态 |
| `product_snapshot` | `object` | 是 | 用于核对商品、SKU、颜色、尺寸和包装内容 |
| `target` | `object` | 是 | 平台、站点、类目、图片位置和目标比例 |
| `slot_plan` | `list<object>` | 是 | 图片拟用于主图、附图、变体图、尺寸图、描述图或封面图 |
| `variant_mapping` | `object` | 是 | 输入图与目标 SKU/变体的映射 |
| `edit_scope` | `object` | 是 | 允许动作及禁止改变区域 |
| `quality_thresholds` | `object` | 是 | 清晰度、压缩、主体占比、背景和安全区要求 |
| `upload_mode` | `string` | 否 | 仅输出资产，或同时上传平台素材服务 |
| `processing_config` | `object` | 是 | 批量大小、超时、重试和部分成功策略 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 152–164 行；表格顶层字段 8 行。

<!-- source-excerpt node=18 section=输出 start=152 end=164 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `adapted_images` | `list<image>` | 按平台位置和 SKU 输出的处理后图片 |
| `slot_assignments` | `list<object>` | 推荐顺序、用途和不适用原因 |
| `processing_report` | `object` | 每张图片的处理动作和前后质量变化 |
| `platform_validation` | `object` | 技术、内容和类目规则检查结果 |
| `platform_media_receipts` | `list<object>` | 条件输出；上传后的素材 ID/URL 和回读信息 |
| `missing_asset_requests` | `list<object>` | 缺少视角、细节、尺寸或合格主图的补拍需求 |
| `review_tasks` | `list<object>` | 裁剪、颜色、透明部件、权利或商品不一致问题 |
| `task_summary` | `object` | 批量及逐图状态、失败和重试信息 |
<!-- /source-excerpt -->

<a id="node-19"></a>

### 19. 图片文案翻译与重绘

- 推荐分组：**图片与视频**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 182–262 行。
- 覆盖：输入 8 行、业务配置 0 行、输出 8 行，共 16 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 源图与原语言/目标语言、商品、声明分组；术语和版式素材是独立可选对象。
- `localization_config` 的单位转换、语气、双语、置信阈值和审核策略未给完整子 Schema/默认；可提供按说明分区的对象输入，不生成重绘图或 OCR 结果。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 188–200 行；表格顶层字段 8 行。

<!-- source-excerpt node=19 section=输入 start=188 end=200 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `source_images` | `list<image>` | 是 | 待翻译图片及来源、SKU、用途和权利信息 |
| `source_locale` | `string` | 是 | 原文语言和地区 |
| `target` | `object` | 是 | 平台、站点、目标语言、类目和图片位置 |
| `product_snapshot` | `object` | 是 | 商品名称、参数、尺寸、单位、包装和限制条件 |
| `approved_claims` | `list<object>` | 是 | 允许翻译或改写的声明及证据 |
| `terminology` | `object` | 否 | 品牌词、行业词、禁译词、固定译法和禁用表达 |
| `layout_assets` | `object` | 否 | 可商用字体、图标、Logo、品牌色和原始设计文件 |
| `localization_config` | `object` | 是 | 单位转换、语气、双语策略、置信度阈值和审核策略 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 233–245 行；表格顶层字段 8 行。

<!-- source-excerpt node=19 section=输出 start=233 end=245 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `localized_images` | `list<image>` | 通过回读校验的目标语言图片 |
| `text_free_images` | `list<image>` | 因目标位置禁止文字生成的无文案版本 |
| `extracted_copy` | `list<object>` | 原文、位置、角色和 OCR 置信度 |
| `translation_report` | `object` | 原文、译文、术语、单位换算和声明依据 |
| `layout_report` | `object` | 字体、字号、溢出、对比度和指向关系检查 |
| `fact_conflicts` | `list<object>` | 源图与商品事实不一致的文字或数值 |
| `review_tasks` | `list<object>` | 低置信度、法规标签、单位和版面问题 |
| `task_summary` | `object` | 逐图、逐语言状态和失败原因 |
<!-- /source-excerpt -->

<a id="node-20"></a>

### 20. 商品视频脚本生成

- 推荐分组：**图片与视频**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 263–352 行。
- 覆盖：输入 10 行、业务配置 0 行、输出 8 行，共 18 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `creative_goal` 为必填字符串，原文给商品介绍、演示、开箱、种草、安装、FAQ、品牌故事等中文选项语义，未给机器枚举键/默认。
- 受众、可用资产、商品事实、声明与时效 offer 分开；`script_config` 只描述时长/候选数/语速/复杂度/审核门槛，未定义单位、范围和默认，不自动预填。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 269–283 行；表格顶层字段 10 行。

<!-- source-excerpt node=20 section=输入 start=269 end=283 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `product_snapshot` | `object` | 是 | 商品功能、参数、使用步骤、包装内容、限制和目标 SKU |
| `target` | `object` | 是 | 平台、站点、视频位置、目标语言和类目 |
| `audience` | `object` | 是 | 目标用户、场景、痛点、购买阶段和待消除疑虑 |
| `creative_goal` | `string` | 是 | 商品介绍、演示、开箱、种草、安装、FAQ 或品牌故事 |
| `approved_claims` | `list<object>` | 是 | 允许口播和展示的声明及证据 |
| `keyword_asset` | `object` | 否 | 消费者常用语言、场景词和问题词 |
| `available_assets` | `list<object>` | 是 | 可用图片、视频、人物、场地、道具及权利状态 |
| `offer_snapshot` | `object` | 否 | 价格、促销、库存等时效信息及有效期 |
| `brand_voice` | `object` | 否 | 语气、禁用表达、CTA 和品牌表达 |
| `script_config` | `object` | 是 | 时长、候选数、语速、镜头复杂度和审核门槛 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 325–337 行；表格顶层字段 8 行。

<!-- source-excerpt node=20 section=输出 start=325 end=337 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `recommended_script` | `object` | 推荐脚本、目标时长、结构和推荐理由 |
| `script_candidates` | `list<object>` | 不同钩子和叙事结构的候选 |
| `shot_list` | `list<object>` | 逐镜头时长、SKU、画面、动作、口播、字幕和道具 |
| `claim_trace` | `list<object>` | 每条声明的事实、证据和限定条件 |
| `asset_requirements` | `list<object>` | 已有素材、补拍需求和不可执行镜头 |
| `platform_fit_report` | `object` | 视频位置、时长、比例、语言和 CTA 检查 |
| `rights_and_risk_report` | `object` | 人物、音乐、素材和敏感声明风险 |
| `review_tasks` | `list<object>` | 待确认声明、镜头、促销和高风险内容 |
<!-- /source-excerpt -->

<a id="node-21"></a>

### 21. 商品短视频生成

- 推荐分组：**图片与视频**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 353–446 行。
- 覆盖：输入 9 行、业务配置 0 行、输出 11 行，共 20 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `voice_assets/music_assets` 均为可选音频列表，可复用素材输入/变量绑定；`source_media` 是混合素材对象列表，不擅自改成只接视频。
- `render_config/disclosure_config` 是必填对象，品牌样式可选；分辨率、比例、帧率、码率、候选、超时、重试等未给完整子 Schema/默认，不新增渲染任务。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 359–372 行；表格顶层字段 9 行。

<!-- source-excerpt node=21 section=输入 start=359 end=372 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `approved_script` | `object` | 是 | 节点 20 输出并完成必要审核的脚本和分镜 |
| `product_snapshot` | `object` | 是 | 商品、SKU、外观、功能、包装和限制条件 |
| `source_media` | `list<object>` | 是 | 实拍视频、图片、Logo、动画和背景素材及授权 |
| `target` | `object` | 是 | 平台、站点、视频位置、语言和目标规格 |
| `voice_assets` | `list<audio>` | 否 | 已授权口播、配音或声音风格 |
| `music_assets` | `list<audio>` | 否 | 有目标平台、市场、商业用途和期限授权的音乐 |
| `brand_style` | `object` | 否 | 字体、颜色、转场、Logo 和字幕样式 |
| `render_config` | `object` | 是 | 分辨率、比例、帧率、码率、候选数、超时和重试 |
| `disclosure_config` | `object` | 是 | AIGC、商业内容、人物和素材披露要求 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 413–428 行；表格顶层字段 11 行。

<!-- source-excerpt node=21 section=输出 start=413 end=428 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `video_candidates` | `list<video>` | 通过自动校验的成片候选 |
| `recommended_video` | `video` | 条件输出；硬门禁通过后的推荐版本 |
| `master_video` | `video` | 高质量母版，供字幕和多语言处理 |
| `platform_renditions` | `list<video>` | 按平台位置生成的比例、码率和文件版本 |
| `thumbnail_candidates` | `list<image>` | 与商品和视频内容一致的封面候选 |
| `shot_trace` | `list<object>` | 镜头与脚本、商品、SKU 和源素材的对应关系 |
| `quality_report` | `object` | 技术、商品连续性、字幕、音频和内容检查 |
| `rights_report` | `object` | 音乐、人物、声音、素材和商标授权状态 |
| `disclosure_advice` | `object` | AIGC 和商业内容披露要求 |
| `review_tasks` | `list<object>` | 事实、权利、生成漂移和高风险内容 |
| `task_summary` | `object` | 整体及逐版本异步状态和重试信息 |
<!-- /source-excerpt -->

<a id="node-22"></a>

### 22. 视频字幕、配音与本地化

- 推荐分组：**图片与视频**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 447–542 行。
- 覆盖：输入 10 行、业务配置 0 行、输出 11 行，共 21 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `source_video` 是单视频；`targets` 是可增删目标对象列表；原脚本可选，前端不执行其说明中的 ASR 重建。
- 配音配置、术语、跨市场音频权利分别保留；`localization_config` 仅描述字幕/语速/单位/口型同步/审核，口型同步等子项无明确类型或默认，不从处理章节补充。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 453–467 行；表格顶层字段 10 行。

<!-- source-excerpt node=22 section=输入 start=453 end=467 -->
| 变量名 | 类型 | 必选 | 说明 |
| --- | --- | ---: | --- |
| `source_video` | `video` | 是 | 已确认商品和 SKU 的视频母版 |
| `source_script` | `object` | 否 | 原脚本、镜头、口播和声明引用；缺失时由 ASR 重建 |
| `source_locale` | `string` | 是 | 原始语言和地区 |
| `targets` | `list<object>` | 是 | 一个或多个目标平台、站点、语言和视频位置 |
| `product_snapshot` | `object` | 是 | 商品名、型号、参数、尺寸和使用步骤 |
| `approved_claims` | `list<object>` | 是 | 可翻译和配音的声明及限定条件 |
| `terminology` | `object` | 否 | 品牌词、型号、禁译词、固定译法和目标市场术语 |
| `voice_profile` | `object` | 否 | 声音、语气及其授权范围 |
| `music_and_audio_rights` | `object` | 是 | 原音乐、音效和声音的跨市场使用权 |
| `localization_config` | `object` | 是 | 字幕样式、语速、单位、口型同步和审核门槛 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 508–523 行；表格顶层字段 11 行。

<!-- source-excerpt node=22 section=输出 start=508 end=523 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `localized_videos` | `list<video>` | 按语言和平台位置输出的本地化视频 |
| `subtitle_files` | `list<object>` | 带时间戳字幕和烧录字幕版本 |
| `localized_scripts` | `list<object>` | 目标语言口播、字幕和 CTA 文稿 |
| `audio_tracks` | `list<audio>` | 条件输出；授权配音、人声和混音轨 |
| `transcript_report` | `object` | 原文转写、说话人、时间戳和低置信度片段 |
| `translation_report` | `object` | 术语、单位、声明和反向校验结果 |
| `sync_and_quality_report` | `object` | 音画同步、字幕版面、混音和技术检查 |
| `rights_report` | `object` | 音乐、原声、配音和声音克隆授权状态 |
| `disclosure_advice` | `object` | AIGC、声音和身份披露要求 |
| `review_tasks` | `list<object>` | 低置信度语音、高风险声明、声音权利和口型问题 |
| `task_summary` | `object` | 逐语言和逐平台版本的异步状态 |
<!-- /source-excerpt -->

<a id="node-23"></a>

### 23. 商品合规判断

- 推荐分组：**合规与发布**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 543–642 行。
- 覆盖：输入 9 行、业务配置 0 行、输出 11 行，共 20 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 商品 ID、事实、目标、类目与卖家上下文必填；变体、物流、证据与规则快照可折叠为补充信息。
- 本节点无独立业务配置表或命名配置对象；不要新增“检查深度/通过门槛/自动放行”等原文未定义参数。原文对象内层键与默认未给完整 Schema。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 551–564 行；表格顶层字段 9 行。

<!-- source-excerpt node=23 section=输入 start=551 end=564 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `product_id` | `string` | 是 | 与商品事实、变体和证据文件绑定的内部商品标识 |
| `product_facts` | `object` | 是 | 名称、用途、人群、年龄、材质、成分、尺寸、重量、功率、电池、无线功能、生产国、包装和警示等事实 |
| `variants` | `list<object>` | 否 | 各 SKU 的容量、配方、功率、电池、数量等差异 |
| `target_context` | `object` | 是 | 平台、国家或地区、Amazon marketplace 或 TikTok Shop 店铺、销售主体和发货国 |
| `category_mapping` | `object` | 是 | Amazon product type、ASIN（如已有）或 TikTok Shop 叶子类目及映射置信度 |
| `seller_context` | `object` | 是 | Seller ID／Shop ID、账号类型、类目资格、品牌资格、邀请资格和有效期 |
| `logistics_context` | `object` | 否 | FBA／FBM、TikTok Shop 履约方式、仓库、承运方式和目的国 |
| `evidence_documents` | `list<object>` | 否 | 认证、检测报告、SDS、成分表、标签、说明书、制造商或责任人资料等 |
| `rule_snapshot` | `object` | 否 | 已缓存的官方政策、类目规则和接口响应；提供后仍需校验市场、店铺和时效 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 609–624 行；表格顶层字段 11 行。

<!-- source-excerpt node=23 section=输出 start=609 end=624 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `decision` | `string` | `ELIGIBLE_CANDIDATE`、`QUALIFICATION_REQUIRED`、`EVIDENCE_REQUIRED`、`MANUAL_REVIEW_REQUIRED`、`PROHIBITED` 或 `INDETERMINATE` |
| `risk_level` | `string` | 风险等级及依据，不单独作为准入结论 |
| `restriction_findings` | `list<object>` | 禁售、受限、年龄或主体限制及规则来源 |
| `qualification_requirements` | `list<object>` | 所需资格、当前状态、申请入口、覆盖类目和有效期 |
| `compliance_requirements` | `list<object>` | 所需认证、报告、标签、警示和责任主体资料 |
| `evidence_gaps` | `list<object>` | 缺失、失效、范围不匹配或冲突的证据 |
| `transport_findings` | `list<object>` | 与销售资格分离的运输和履约结果 |
| `platform_check_receipts` | `list<object>` | 实时查询范围、时间、结果摘要和追踪标识 |
| `remediation_actions` | `list<object>` | 按阻断程度排序的整改动作 |
| `manual_review_items` | `list<object>` | 需要合规或法律人员判断的问题 |
| `rule_snapshot` | `object` | 平台、市场、规则版本、获取时间和来源 |
<!-- /source-excerpt -->

<a id="node-24"></a>

### 24. 知识产权与品牌侵权风险检查

- 推荐分组：**合规与发布**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 643–744 行。
- 覆盖：输入 11 行、业务配置 0 行、输出 11 行，共 22 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 品牌/标识清单与素材清单为两个必填对象列表；来源、供应链证据、历史通知、官方登记结果各自可选，不合并成单一附件字段。
- `seller_brand_role` 只给中文身份语义，无机器枚举键/默认；本节点没有独立配置表，不添加检索深度、风险阈值或自动通过选项。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 651–666 行；表格顶层字段 11 行。

<!-- source-excerpt node=24 section=输入 start=651 end=666 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `product_id` | `string` | 是 | 与商品、素材、Listing 和证据统一绑定的标识 |
| `product_facts` | `object` | 是 | 商品名称、品牌、制造商、型号、来源、包装和外观特征 |
| `brand_and_mark_inventory` | `list<object>` | 是 | 商品、包装和素材中的品牌词、Logo、口号、角色、人物、图案和其他标识 |
| `listing_content` | `object` | 是 | 标题、卖点、描述、属性、搜索词和 A+／详情内容 |
| `media_assets` | `list<object>` | 是 | 原图、编辑图、视频、字幕、配音、音乐、字体和缩略图 |
| `asset_provenance` | `list<object>` | 否 | 作者、来源、生成方式、许可文本、地域、用途和期限 |
| `supply_chain_evidence` | `list<object>` | 否 | 发票、采购合同、品牌授权书、许可协议、实拍和供应商身份 |
| `target_context` | `object` | 是 | Amazon marketplace 或 TikTok Shop 市场、店铺、销售地域和语言 |
| `seller_brand_role` | `string` | 否 | 商标权人、一级／二级授权商、经销商或无品牌卖家 |
| `known_notices` | `list<object>` | 否 | 平台警告、权利人通知、投诉编号或历史下架记录 |
| `official_registry_results` | `list<object>` | 否 | 目标法域官方商标、专利或外观检索结果 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 707–722 行；表格顶层字段 11 行。

<!-- source-excerpt node=24 section=输出 start=707 end=722 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `decision` | `string` | `LOW_INITIAL_RISK`、`EVIDENCE_GAP`、`PLATFORM_AUTHORIZATION_REQUIRED`、`SUSPECTED_CONFLICT`、`LEGAL_REVIEW_REQUIRED` 或 `BLOCKED` |
| `ip_findings` | `list<object>` | 按商标、版权、专利、外观、商业外观和人格权分类的问题 |
| `asset_findings` | `list<object>` | 精确到字段、图片、视频时间段、字幕、音轨或包装位置的发现 |
| `brand_consistency_result` | `object` | 实物、包装、品牌字段、素材和文件的一致性结果 |
| `authorization_chain` | `object` | 权利人至卖家的授权链、覆盖范围、缺口和有效期 |
| `provenance_gaps` | `list<object>` | 无法证明来源或商用许可的素材 |
| `registry_candidates` | `list<object>` | 官方检索候选；不直接标记为侵权 |
| `platform_authorization_status` | `object` | 平台品牌资格及核验时间 |
| `recommended_actions` | `list<object>` | 删除、替换、补证、暂停或转法律复核等动作 |
| `review_queue` | `list<object>` | 需要品牌、法务或知识产权专业人员判断的事项 |
| `evidence_snapshot` | `object` | 内容版本、文件哈希、检索时间和目标法域 |
<!-- /source-excerpt -->

<a id="node-25"></a>

### 25. Listing 全素材合规审核

- 推荐分组：**合规与发布**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 745–850 行。
- 覆盖：输入 10 行、业务配置 0 行、输出 12 行，共 22 个顶层字段行。

#### UI 候选：差异控件与未定义项

- Listing 包、全素材、商品事实、商品合规/IP结果、目标为必填；变体、声明证据、现有 Listing 与政策快照可选。
- 本节点没有独立业务配置表；可按内容、素材、前序结果、补充证据分区，但不新增审核级别、自动批准阈值等字段；内层 Schema 与默认保持未定义。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 753–767 行；表格顶层字段 10 行。

<!-- source-excerpt node=25 section=输入 start=753 end=767 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `listing_package` | `object` | 是 | 标题、卖点／五点、描述、A+／详情模块、属性、规格、搜索词和变体文案的最终候选版本 |
| `media_assets` | `list<object>` | 是 | 主图、附图、信息图、A+ 图片、视频、封面、字幕、配音、音乐及用途 |
| `product_facts` | `object` | 是 | 经确认的商品事实和版本，不允许用 Listing 反向证明事实 |
| `variant_matrix` | `list<object>` | 否 | 各 SKU 的颜色、尺寸、数量、材质、包装和实物差异 |
| `claim_evidence` | `list<object>` | 否 | 测试报告、认证、研究、授权、保修政策和其他声明证据 |
| `product_compliance_result` | `object` | 是 | 节点 23 的结论、规则快照和未解决问题 |
| `ip_risk_result` | `object` | 是 | 节点 24 的结论、素材风险和授权缺口 |
| `target_context` | `object` | 是 | 平台、市场、店铺、类目、product type、语言和受众 |
| `existing_listing_snapshot` | `object` | 否 | 修改已有商品时的当前 Listing，用于识别错误复用商品页 |
| `policy_snapshot` | `object` | 否 | 当前平台和市场的字段、素材与内容政策 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 812–828 行；表格顶层字段 12 行。

<!-- source-excerpt node=25 section=输出 start=812 end=828 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `decision` | `string` | `PASS`、`CONDITIONAL_PASS`、`MANUAL_REVIEW_REQUIRED` 或 `BLOCKED` |
| `reviewed_version` | `object` | Listing、素材、商品事实和上游报告的版本及哈希 |
| `findings` | `list<object>` | 问题位置、规则、严重度、证据和整改建议 |
| `claim_ledger` | `list<object>` | 原子声明、出现位置、适用 SKU、证据和状态 |
| `cross_channel_conflicts` | `list<object>` | 标题、属性、图片、视频和商品事实间的冲突 |
| `media_compliance` | `list<object>` | 每个图片和视频的技术、内容和角色检查 |
| `platform_rule_result` | `object` | 平台与类目规则的逐项结果和快照 |
| `auto_fix_proposals` | `list<object>` | 不改变事实或声明含义的安全修改 |
| `manual_review_items` | `list<object>` | 需要编辑、合规或法律复核的事项 |
| `warning_acceptance` | `object` | `CONDITIONAL_PASS` 时列出非阻断警告、具名责任人、接受范围、时间和版本；未接受时不得交接发布 |
| `approved_package` | `object` | `PASS` 时返回；`CONDITIONAL_PASS` 仅在全部非阻断警告由授权责任人接受后返回，且与审核版本完全一致 |
| `recheck_required` | `list<string>` | 哪些字段或素材变化会使审核失效 |
<!-- /source-excerpt -->

<a id="node-26"></a>

### 26. 商品发布与上架校验

- 推荐分组：**合规与发布**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 851–984 行。
- 覆盖：输入 13 行、业务配置 0 行、输出 12 行，共 25 个顶层字段行。

#### UI 候选：差异控件与未定义项

- `submission_mode` 必填，明确 `PREVIEW_ONLY/SAVE_DRAFT/PUBLISH`，没有默认；可提供卖家中文标签并保留原值，模式选择本身不发送/发布。
- `existing_listing_snapshot/idempotency_key/submission_approval` 分别标“编辑时/新建时/平台写入时”；前端可展示原文条件，不能自行引入真实写入确认流程。
- 草稿作用域差异与最终状态保留为输入/输出说明；此节点没有独立业务配置表，不新增轮询、上传、提交或重试执行。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 859–876 行；表格顶层字段 13 行。

<!-- source-excerpt node=26 section=输入 start=859 end=876 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `approved_listing_package` | `object` | 是 | 节点 25 为 `PASS`，或 `CONDITIONAL_PASS` 的全部非阻断警告已由授权责任人接受后生成，且版本未变化的 Listing 和素材包 |
| `product_compliance_result` | `object` | 是 | 节点 23 的结论、资格和证据状态 |
| `ip_risk_result` | `object` | 是 | 节点 24 的结论和授权状态 |
| `material_review_result` | `object` | 是 | 节点 25 的审核结论、规则快照和版本哈希 |
| `target_context` | `object` | 是 | 平台、市场、Seller ID／Shop ID、语言、币种和授权上下文 |
| `category_and_attributes` | `object` | 是 | Amazon product type 或 TikTok Shop 叶子类目、属性和条件字段 |
| `sku_plan` | `object` | 是 | 父子体／SKU 关系、seller SKU、商品编码、价格、库存和变体值 |
| `fulfillment_data` | `object` | 是 | FBA／FBM 或 TikTok Shop 仓库、配送、包裹尺寸和重量 |
| `platform_asset_refs` | `list<object>` | 是 | 已上传到平台或平台认可地址的图片、视频和文件引用 |
| `submission_mode` | `string` | 是 | `PREVIEW_ONLY`、`SAVE_DRAFT` 或 `PUBLISH`；Amazon 的 `SAVE_DRAFT` 仅保存工作流内部草稿，TikTok Shop 才可在接口支持时保存平台草稿 |
| `existing_listing_snapshot` | `object` | 编辑时是 | 当前平台商品、基线版本和待修改字段 |
| `idempotency_key` | `string` | 新建时是 | 与店铺、商品和提交内容绑定，防止重试创建重复商品 |
| `submission_approval` | `object` | 平台写入时是 | 用户或授权角色对目标、内容版本和具体写入动作的确认；适用于 TikTok Shop 平台草稿及两平台真实发布 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 933–949 行；表格顶层字段 12 行。

<!-- source-excerpt node=26 section=输出 start=933 end=949 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `operation` | `string` | 新建、创建 offer、全量更新、局部更新、跨市场复制、保存内部／平台草稿或仅预检 |
| `submission_mode` | `string` | 实际执行的 `PREVIEW_ONLY`、`SAVE_DRAFT` 或 `PUBLISH`，并标明草稿作用域为 `INTERNAL` 或 `PLATFORM` |
| `mapped_payload_summary` | `object` | 平台字段映射、来源、请求版本和内容哈希，不含密钥 |
| `local_validation_result` | `object` | 本地确定性检查和字段级问题 |
| `platform_preflight_result` | `object` | 平台预检响应、问题、时间和是否落库 |
| `submission_result` | `object` | 是否真实提交、submission／feed／product ID、同步状态和时间 |
| `item_results` | `list<object>` | 每个商品、父 SKU 和子 SKU 的独立结果 |
| `platform_issues` | `list<object>` | 平台原始问题码、严重度、字段路径和建议动作 |
| `final_state` | `string` | `READY_TO_SUBMIT`、`DRAFT_SAVED`、`SUBMITTED_PENDING_REVIEW`、`PUBLISHED`、`PUBLISHED_WITH_ISSUES`、`REJECTED`、`PARTIAL_SUCCESS` 或 `STATUS_UNKNOWN` |
| `post_publish_verification` | `object` | 商品身份、属性、素材、价格、库存、可购买和可发现状态 |
| `retry_state` | `object` | 是否可重试、幂等键、重试次数和下一次允许时间 |
| `remediation_actions` | `list<object>` | 按商品和字段生成的修复、补证或复核动作 |
<!-- /source-excerpt -->

<a id="node-27"></a>

### 27. 库存与履约风险监控

- 推荐分组：**店铺运营**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 985–1078 行。
- 覆盖：输入 10 行、业务配置 0 行、输出 8 行，共 18 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 库存快照、订单需求、履约事件保留三类输入；SKU/仓库映射独立对象；供应、业务事件、成本约束和既有动作可选。
- `monitoring_policy` 必填，但预测周期/阈值/最低样本/延迟/频率只有描述，没有完整键、单位、范围和默认；配置字段不创建计时器或监控任务。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 993–1007 行；表格顶层字段 10 行。

<!-- source-excerpt node=27 section=输入 start=993 end=1007 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `platform_context` | `object` | 是 | Amazon 或 TikTok Shop、市场、店铺／卖家、时区和币种 |
| `sku_warehouse_mapping` | `object` | 是 | 商品 ID、平台 SKU、卖家 SKU、变体、仓库和履约渠道的稳定映射 |
| `inventory_snapshots` | `list<object>` | 是 | 可售、预留／占用、冻结、不可售、在途、待质检、来源和快照时间 |
| `orders_and_demand` | `list<object>` | 是 | 订单创建、支付、取消、发货、送达及 SKU 数量和历史销量 |
| `fulfillment_events` | `list<object>` | 是 | 发货截止时间、包裹、承运商、运单、揽收／轨迹和取消原因 |
| `supply_plan` | `object` | 否 | 采购单、在途批次、最早／最晚到货、交期分布、MOQ、箱规和收货耗时 |
| `business_events` | `list<object>` | 否 | 促销、广告放量、价格变化、节假日、断货区间和异常大单 |
| `cost_and_constraints` | `object` | 否 | 采购／仓储／缺货成本、安全库存、目标服务水平、容量和最大库存天数 |
| `monitoring_policy` | `object` | 是 | 预测周期、风险阈值、最低样本、数据最大延迟和提醒频率 |
| `existing_actions` | `list<object>` | 否 | 已补货、调拨、暂停推广或人工忽略记录，用于防止重复建议 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 1049–1061 行；表格顶层字段 8 行。

<!-- source-excerpt node=27 section=输出 start=1049 end=1061 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `monitoring_status` | `string` | 正常、有风险、数据不完整或已阻断，附数据截止时间 |
| `inventory_health` | `list<object>` | SKU／仓库级可承诺库存、未来可用、覆盖天数和周转状态 |
| `risk_alerts` | `list<object>` | 风险类型、严重度、概率、预计时间、影响数量／订单、证据和置信度 |
| `inventory_forecast` | `list<object>` | 需求情景、预计缺货日、缺口区间、积压量和预测假设 |
| `fulfillment_risks` | `list<object>` | 订单／包裹、截止时间、当前状态、缺失步骤、归因等级和处置时限 |
| `reconciliation_gaps` | `list<object>` | 平台与 ERP／WMS 的数量差、状态差、时间差和采用口径 |
| `recommended_actions` | `list<object>` | 动作、优先级、数量／范围、依赖、风险、人工门禁和回滚 |
| `coverage_and_next_check` | `object` | 未覆盖 SKU／仓库，缺失数据和建议下次检查时间 |
<!-- /source-excerpt -->

<a id="node-28"></a>

### 28. 评论与差评洞察

- 推荐分组：**店铺运营**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 1079–1170 行。
- 覆盖：输入 11 行、业务配置 0 行、输出 9 行，共 20 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 评论、平台聚合洞察、退货退款、客服四种来源至少提供一类；UI 保留四个独立输入及分组提示，不将聚合数据伪装成评论行。
- `analysis_policy` 的语言/样本/主题粒度/周期/严重度/隐私保留未给完整子 Schema/默认；竞品反馈保持独立可选分区。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 1087–1104 行；表格顶层字段 11 行。

<!-- source-excerpt node=28 section=输入 start=1087 end=1104 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `platform_context` | `object` | 是 | 平台、市场、店铺、商品 ID／ASIN、SKU／变体和时间窗 |
| `review_records` | `list<object>` | 条件必填 | 可合法访问的逐条评论；包含评论 ID、评分、标题、正文／片段、语言和时间等可用字段 |
| `platform_insights` | `object` | 条件必填 | 平台直接提供的聚合主题、趋势、样本口径、更新时间和覆盖范围；不得伪装成逐条评论 |
| `return_refund_records` | `list<object>` | 条件必填 | 订单／SKU、原因、状态、数量、金额和消费者说明 |
| `service_feedback` | `list<object>` | 条件必填 | 已脱敏工单／会话、咨询意图、问题与处理结果 |
| `product_and_listing_snapshot` | `object` | 是 | 商品事实、当前标题、卖点、图片信息、规格、使用说明和版本 |
| `sku_variant_mapping` | `object` | 是 | 评论、退货和订单到 SKU／变体的稳定映射 |
| `sales_denominators` | `object` | 否 | 订单、销量、访问或评论基数，用于计算发生率 |
| `competitor_feedback` | `list<object>` | 否 | 具备合法来源的竞品评论或平台主题，必须与自有商品分区 |
| `analysis_policy` | `object` | 是 | 目标语言、最低样本、主题粒度、趋势周期、严重度和隐私保留规则 |
| `known_issues_and_changes` | `list<object>` | 否 | 已知缺陷、供应批次、包装／Listing 改版和既有改进动作 |

逐条评论、平台聚合洞察、退货退款、售后客服四类输入至少提供一类；缺失其他来源时必须输出覆盖限制。
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 1141–1154 行；表格顶层字段 9 行。

<!-- source-excerpt node=28 section=输出 start=1141 end=1154 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `insight_status` | `string` | 成功或部分成功，附来源、市场、时间窗、更新时间和覆盖率 |
| `issue_topics` | `list<object>` | 主题、分类、提及数、涉及用户、评分／退货影响、趋势和置信度 |
| `aspect_sentiment` | `list<object>` | 商品属性、正负反馈、使用场景和可回溯证据 |
| `segment_distribution` | `list<object>` | SKU、变体、批次、市场和时间的问题差异 |
| `attribution_findings` | `list<object>` | 产品、Listing、包装物流、使用兼容、服务或未知，附证据、反证和级别 |
| `critical_signals` | `list<object>` | 安全、伤害、过敏、批量故障等强制人工复核信号 |
| `prioritized_actions` | `list<object>` | 问题优先级及产品、Listing、素材、包装履约和客服动作 |
| `validation_plan` | `object` | 改动后观察指标、基线、建议观察期和停止条件 |
| `data_limitations` | `list<object>` | 样本、语言、聚合数据、权限和来源偏差 |
<!-- /source-excerpt -->

<a id="node-29"></a>

### 29. 客服回复生成

- 推荐分组：**店铺运营**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 1171–1258 行。
- 覆盖：输入 10 行、业务配置 0 行、输出 9 行，共 19 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 会话、商品、店铺政策与允许动作必填；订单/物流/售后为条件必填，原文未完整列出触发条件，使用说明提示，不凭猜测增加阻断规则。
- `reply_preferences` 可选，语言/语气/长度/称谓/禁语/审批要求没有完整子 Schema/默认；回复历史为单独列表。输出是草稿与交付条件，不新增“发送消息”按钮。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 1179–1193 行；表格顶层字段 10 行。

<!-- source-excerpt node=29 section=输入 start=1179 end=1193 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `platform_context` | `object` | 是 | 平台、市场、店铺、时区和授权上下文 |
| `conversation_context` | `object` | 是 | 会话／消息 ID、最新消费者消息、必要历史、时间和消费者语言 |
| `product_facts` | `object` | 是 | 商品 ID／SKU、规格、兼容性、功能、限制、使用和安全说明 |
| `order_context` | `object` | 条件必填 | 订单、商品行、支付、取消、发货、送达状态和更新时间 |
| `logistics_context` | `object` | 条件必填 | 包裹、承运商、运单、预计送达、最后轨迹和异常 |
| `aftersales_context` | `object` | 条件必填 | 退货／退款申请、原因、状态、可执行动作、金额和时限 |
| `store_policy` | `object` | 是 | 退换货、保修、补发、退款、发票和服务时限，附市场与版本 |
| `allowed_actions` | `list<object>` | 是 | 当前订单／会话可用消息类型、卡片、售后资格和限制 |
| `reply_preferences` | `object` | 否 | 目标语言、语气、长度、品牌称呼、禁用表达和审批要求 |
| `sent_reply_history` | `list<object>` | 否 | 已发送文本、时间、平台回执和处理人，用于防重与一致性检查 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 1226–1239 行；表格顶层字段 9 行。

<!-- source-excerpt node=29 section=输出 start=1226 end=1239 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `reply_status` | `string` | 可生成、需补信息、需人工审核、必须升级或不可发送 |
| `intent_and_risk` | `object` | 主／次意图、情绪、紧急度、高风险标签和依据 |
| `fact_summary` | `list<object>` | 本次使用的商品、订单、物流、售后和政策事实及时间 |
| `reply_drafts` | `object` | 目标语言正式版和可选简短版，不含内部推理 |
| `recommended_message_type` | `object` | Amazon 消息动作或 TikTok Shop 卡片／消息类型 |
| `next_actions` | `list<object>` | 客服、仓库、物流或售后需执行的动作与前置条件 |
| `draft_delivery_guard` | `object` | 草稿能否提交客服审核、建议消息类型、审批要求、阻断原因、有效期和需重查状态；不代表已发送 |
| `unresolved_questions` | `list<object>` | 需向消费者追问或需内部核实的信息 |
| `audit_summary` | `object` | 来源、草稿版本、防重结果和生成审计信息；不包含发送回执 |
<!-- /source-excerpt -->

<a id="node-30"></a>

### 30. 广告与流量投放优化

- 推荐分组：**店铺运营**。
- 原文节点范围：[17-30.md](sources/17-30.md) 第 1259–1348 行。
- 覆盖：输入 11 行、业务配置 0 行、输出 10 行，共 21 个顶层字段行。

#### UI 候选：差异控件与未定义项

- 广告实体、报表、归因设置、商品指标、成本利润、策略和变更历史各自保留；内容表现、搜索信号与实验上下文可选。
- `optimization_policy` 的目标 ROAS/ACOS/CPA/GMV、预算、最大调整、库存覆盖和风险偏好只有描述，没有完整子键/单位/枚举/默认；本阶段不新增广告投放或预算修改动作。
- 本节点没有独立业务配置节；原文未给出的默认值保持未设置，不从处理逻辑章节补齐。

#### 原文摘录：输入

来源：[17-30.md](sources/17-30.md) 第 1267–1282 行；表格顶层字段 11 行。

<!-- source-excerpt node=30 section=输入 start=1267 end=1282 -->
| 变量名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `platform_context` | `object` | 是 | Amazon Ads 或 TikTok Ads、广告账户、市场、店铺、时区和币种 |
| `ad_entities` | `object` | 是 | 活动、广告组、广告、商品、关键词／搜索词、素材、达人或直播的平台标识 |
| `performance_report` | `list<object>` | 是 | 展示、点击、花费、CTR、CPC、订单、归因销售／GMV、CVR、CPA、ROAS 和报告日期 |
| `attribution_settings` | `object` | 是 | 点击／浏览归因窗、报告时间口径和转化成熟期 |
| `commerce_metrics` | `list<object>` | 是 | 商品 ID／SKU、价格、折扣、订单、取消退款、库存、Listing 状态和评分 |
| `cost_and_profit` | `object` | 是 | 商品成本、平台费、履约费、促销、售后损耗和目标贡献利润 |
| `content_performance` | `list<object>` | 否 | 视频播放、停留、互动、点击、商品卡访问、达人／affiliate 内容及授权 |
| `search_and_traffic_signals` | `list<object>` | 否 | Amazon 搜索词、关键词、匹配方式、placement；TikTok 搜索／内容信号按实际可用字段提供 |
| `optimization_policy` | `object` | 是 | 目标 ROAS／ACOS／CPA／GMV、预算、最大调整比例、最低库存覆盖和风险偏好 |
| `change_history` | `list<object>` | 是 | 预算、出价、素材、Listing、价格和促销变更时间 |
| `experiment_context` | `object` | 否 | 对照组、测试组、周期、主指标、最低样本和停止条件 |
<!-- /source-excerpt -->

#### 原文摘录：输出

来源：[17-30.md](sources/17-30.md) 第 1315–1329 行；表格顶层字段 10 行。

<!-- source-excerpt node=30 section=输出 start=1315 end=1329 -->
| 变量名 | 类型 | 说明 |
| --- | --- | --- |
| `analysis_scope` | `object` | 时间窗、成熟度、时区、币种、归因窗和覆盖实体 |
| `performance_summary` | `object` | 展示、点击、花费、转化、归因收入／GMV、净收入、贡献利润、ROAS／ACOS／CPA |
| `funnel_diagnosis` | `list<object>` | 展示、点击、转化和利润阶段的问题、根因、证据和置信度 |
| `attribution_notes` | `object` | 付费、自然、达人／affiliate 和总渠道边界及不可比项 |
| `opportunity_items` | `list<object>` | 活动、商品、关键词／搜索词、placement、素材或达人的低效与机会 |
| `optimization_actions` | `list<object>` | 当前值、建议值／区间、预期影响、证据、依赖、风险和优先级 |
| `gate_results` | `object` | 库存、利润、样本、冷却、预算、权限和平台能力检查 |
| `experiment_plan` | `object` | 假设、测试对象、对照、周期、主指标、最低样本和停止条件 |
| `execution_and_rollback` | `object` | 立即止损、稳态优化、学习实验顺序，审批、观察期和回滚 |
| `data_limitations` | `list<object>` | 缺失成本、未成熟转化、归因限制、聚合数据和权限说明 |
<!-- /source-excerpt -->

## 5. 目录验收边界

后续实现只按 [UI 需求](03-ui-requirements.md) 验证节点可发现、可添加、卡片一致、属性可编辑、输入/输出元信息完整和前端状态可恢复。本目录提供 30 节点 / 68 小节 / 634 字段行的覆盖依据，不另建业务执行 AC。

原文仍有未完整定义的对象内层 Schema、条件必填触发结构、规则版本 ID、字符串枚举和默认值。需求稿以明确原文、保留未知和复用现有结构化控件处理，不将这些未知描述成已接入平台能力或已实现后端契约。
