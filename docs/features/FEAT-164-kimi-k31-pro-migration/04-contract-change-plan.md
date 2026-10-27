# FEAT-164 契约与方向兼容计划

> 实施授权更新：Owner现已确认FEAT-164方案并要求开始实施和审计验证。此前“仅文档”段落是上一轮历史边界；当前状态以feature.yaml及13-implementation-log.md为准。G0/G1/G2记录本次方案确认；G2A/G2V及产品完成门禁仍未通过。无新增Git/付费/日常库激活许可。

整体breaking。现已实现独立model-selection-v2/chat-models-v2 0.2.0候选、离线生成与Runtime独立投影；v1源和现有consumer pin保持。G2A pending，实际diff审查入口为14。

## 权威与消费者

| 边界 | 权威/Owner | Producer → Consumer |
|---|---|---|
| 模型身份/选择/目录 | Contracts新增model-selection-v2/schema及openapi/chat-models-v2，保留v1；段成威 | Host → Desktop TS/Native；双方请求/回执 |
| 市场/专家/计划模型快照 | Contracts market-selection、market-host、experts及scheduled源对模型源的引用；段成威 | Desktop/Host双向，存储及replay reader |
| Runtime app-server与制品 | 固定Runtime上游+可重放patch/canonical schema；段成威 | Runtime → Contracts兼容投影 → Host/Desktop来源验收 |
| SQLCipher/bbolt私有存储 | Desktop/Host各自migration及领域事务；段成威 | 同一服务跨版本reader/writer |
| Moonshot API | 当前官方Responses；易界适配Owner段成威 | Runtime → Moonshot；返回SSE |
| 受管配置/启动 | Host authority + Desktop launcher/build candidate；段成威 | Host生成 → Runtime，Native来源核验 |

生成物、candidate和schema副本不是第二权威。角色仍在原仓；不把第三方原始协议或服务私有表搬入Contracts。

## 语义候选

采用“活动定义 / 已知历史身份 / 执行准入”三层：活动定义只含新Kimi/MiniMax；历史decode接受旧K3；每个新执行入口必须核对活动身份。已知退役不能写成Selection.state=unknown（后者为实际选择结果不确定）。保留现有ready/switching/unknown含义，退役可用性从权威定义独立投影，具体wire字段在G2源契约diff固定，不由消费者手写扩展。

目录、新选择目标及新turn只接受活动定义；已完成旧operation查询在身份/权限/session/operation/digest精确校验后读取原事实，不经过新执行allowlist。必须覆盖HTTP header前置过滤、请求schema、响应schema、Native enum、市场/专家回执和计划存储，不能只移动ModelAvailable检查。

建议模型family升为未发布0.2.0候选并明确与0.1.0执行consumer不兼容；不是新发布tag，具体schema版本/路由协商和各引用族版本在G2评审冻结。必须保留当前v1历史解释，并以显式版本/精确来源资格拒绝混用；不允许在未知旧consumer下直接发新枚举。若版本化路由更合适，在源diff中列明producer/consumer顺序后再实施，当前不预造不存在的API。

旧选择operation完成回执与“当前Selection”分开：回执可以含旧身份，不能用它覆盖更高revision。旧pending operation不能原地改成新目标；新模型迁移使用新operation，未决旧操作先安全结清。

错误沿既有invalid_request、busy、revision_conflict、model_unavailable、selection_unknown等语义；旧identity known/retired需准确用户提示。如需新错误或资格字段，先进入Contract源和兼容计划，不将未知字段静默吞掉。

## 方向兼容矩阵

| 组合 | 预期 |
|---|---|
| 旧Host + 旧Desktop | 作为迁移前基线；不称新模型支持 |
| 旧Host + 新reader | 能读取明确支持的旧历史；检测旧版本后阻止新profile请求，不伪装ready |
| 新Host + 旧Desktop | 不激活新响应/写入；精确来源或版本握手拒绝，不降低严格校验 |
| 兼容构建 + 旧数据 | 可读且停派发，执行迁移前检查/恢复；不能自动领取旧K3 |
| 新全链 + 新数据 | sources/pins匹配、准入完成后只执行活动profile |
| 兼容回退 + 新旧数据 | 历史可读，独立停新Kimi，MiniMax保持；旧K3执行仍禁 |
| 原旧binary + 新库 | 明确拒绝；不能作已证明回滚 |

## 基线与不可变来源

已发布支持基线 f16a497e1377f45747f8ff9292b4b60cf2027f88；Native历史基线6f632f155eacdaf93df0e0b00b5dab9e369c5442、811f38d6b104fa18477107e7ac91a85e19c445d1；scheduled登记fallback db4458fe94572c4df41a114005d54a049bb79b1f，experts登记fallback35e0949c95d7a59ca5480715c225766dcc822056。按Contracts docs/supported-baselines.md逐族确定适用范围，已完成7个基线的离线同源OpenAPI/Protobuf/AsyncAPI/JSON Schema检查；原入口网络解析失败及替代证据分别保留于08。

当前chat-model候选锁base_commit=54be9314dce5319b049dc0a236800fd1a1fdd7a1只是来源记录，不自动等于已登记支持基线或包含完整当前工作树。当前Contracts HEAD和dirty摘要见evidence；G2A前须登记当前在用模型家族的适用兼容基线并固化真实候选。manifest immutable_references.contracts暂空，避免伪造尚不存在的版本/hash，故不可能声称G2A通过。

## 生成、pin与顺序

1. 修改实际模型权威源和兼容设计后，生成chat-models。
2. 根据实际引用图刷新market-selection → market-host/experts、scheduled-draft/plan/execution及Native/TS/Rust校验器；每个source lock/generator变化可追踪。
3. Runtime边界先最小可重放candidate，再generate-runtime-chat-models；保留input-only旧权威校验。
4. 同步Host Go artifact/constants和api candidate、Desktop contracts candidate；再freeze实际功能组合选择的artifact-media / experts / chat-model Host candidate，launcher实际路径必须匹配；三个选择分支都要核对，不默认只有两种。
5. 不可变候选和consumer评审就绪→兼容reader/准入→停派发与迁移→新producer激活。发布tag/签名/生产不在本轮。

G2A证据要求：version/full commit/digest/generator、全部适用baseline检查、普通fixture conformance及每个受影响consumer Owner评审。源生成、限定conformance、lint及基线检查已有真实结果；不可变commit和Consumer Owner审查仍未取得。文档baseline或dirty hash不冒充这些证据。

## S3 实际source-first（2026-10-25）

新增scheduled-plan-v2 0.2.0源与生成物，完整commit `2dd214d6a702064edae78510c035442854bf9789`，先固化后由Desktop `4d04597cbf40e1aea2c67607c9d441f888223d96`固定消费；旧v1源/生成字节不变。Native私有IPC v2和SQL41仍归Desktop权威。整体breaking，只有同一候选paired consumer可发新值；默认入口保留v1、不读SQL41。8基线离线比较通过，无发布tag/生产激活。Owner当前S3实施与本地提交授权覆盖本批；完整平台/G3仍延期，细节与偏差见26。


## 第66号 D4 兼容读取增量

本轮semantic只读历史/预检修复；archive输入词汇additive，Contracts d5792d6先于Desktop71e39c4固定，9个既有display类型精确摘要生成。Host公共wire、Runtime协议和Native event v4/writer4不变；私有history可选companion由同一App原子更新，未来版本拒绝、旧JSON不改写。原公共基线字节不变及fallback离线breaking检查留证；未发布SDK/tag。具体Owner范围、方向性验证、回退与fresh D4见[66](66-d4-blockers-fixed-and-restricted-start-passed.md)。
