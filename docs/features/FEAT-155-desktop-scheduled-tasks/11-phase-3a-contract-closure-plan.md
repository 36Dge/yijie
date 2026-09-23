# FEAT-155 下一步执行方案：3A 契约校验收口

2026-09-18 · 本页保留方案制定时的记录。用户随后明确授权执行，现已完成收口并停止，实际结果见[12](12-phase-3a-contract-closure-report.md)；下文“本轮仅方案/未执行”指制定方案时。3A原实现和当时检查见[10](10-phase-3a-implementation-report.md)；完整分批安排见[09](09-phase-3-implementation-plan.md)。

## 1. 推荐下一步

**下一次只修复Contracts通用lint与定时契约族的兼容问题，完成验证、报告后停止，再进入3B。** 这是已实施3A的质量收口，不增加产品功能或重做已完成的授权/存储基础。

当前独立execution族严格校验、生成/同步及定向用例已通过，但全仓`pnpm lint`仍失败。它影响后续source-first接入的共同检查入口，修复成本和影响范围可控；继续叠加3B目录/事务会混合新的产品行为与已知校验问题。原3A实现结果保留，不把其定向PASS撤销，也不把通用lint失败忽略。

本轮文档变更`contract-impact=none`。下一次收口目标是**保持所有有效/无效payload及运行行为不变**；涉及源引用、生成和consumer摘要，实施前按实际差异完成方向性分类，不能因为称为lint修复就跳过契约检查。若需要改变输入集合、默认值或业务含义，应单独说明，不能夹带实现。

## 2. 本轮核实的工程事实

- [3A来源证据](evidence/phase-3a-source-20260918.json)中73份业务候选文件摘要全部未变；Contracts/Desktop/Host/Runtime的HEAD与10一致，Runtime clean。本轮没有修改这些仓库。
- `yijie-contracts/scripts/validate-json-schemas.mjs:16,54–65`使用Ajv `strict:true`，但未注册`x-family-version`，且逐文件直接compile。新execution族的leaf checker严格编译的是已解析的标准投影，不能替代通用入口对原始权威源的检查。
- `plan-storage-v1.schema.json`的`$id`位于`…/scheduled-tasks/storage/v1`，文件名式draft引用按URI规则解析到`…/storage/plan-draft-v1.schema.json`，不同于draft真实`$id`；execution引用storage同理。单纯改变文件遍历顺序不能修复这个地址不一致。
- draft/storage的条件`required`和嵌套`properties`需要完整的strict声明；根主要含`$defs`的文档还要逐定义编译，避免只检查未被使用的容器。
- **通用lint checker没有被已核对的旧来源锁固定。** 被固定的是`generate.mjs`等实际generator；不能将二者混为一谈，或以“旧生成器固定”为由永久不修通用checker。后续可以有边界修改checker，同时保护不受影响的旧generator和consumer pin。
- draft源被恢复族来源锁记录，并被计划族生成读取；改动draft的同义schema表达会更新相关摘要。Host可能需要同步恢复族candidate清单，即使Go查询类型和业务处理没有变化。

两个只读技术子任务分别核对通用校验与3B接入边界，不是独立人工批准，没有实施或运行产品检查。

## 3. 按此顺序执行

| 步骤 | 实施内容 | 完成标准 |
|---|---|---|
| 1. 固定修复基线 | 记录原始失败、三个源族与生成物/consumer摘要；保留必要的普通文本源快照用于前后比较 | 能区分本批变化和前序用户改动，不碰用户库/二进制 |
| 2. 规范源与通用校验 | 保留现有`$id`，将外部`$ref`改为被引用源的canonical `$id`+fragment；补严格条件声明；通用checker注册有类型约束的版本注解，先预注册源，再编译根及定时族各定义 | `strict:true`保持；未知关键字、错误类型、缺字段、非法枚举仍拒绝；不靠跳过文件通过 |
| 3. 同源生成与同步 | 定向调整plan/execution的leaf resolver和必要recovery条件投影，按受管canonical ID映射到仓内唯一文件；从源重生受影响的三族产物，更新Desktop及必要Host candidate摘要 | 无网络schema加载、影子定义或手改生成物；不受影响的旧聊天/Runtime来源保持 |
| 4. 验证不改变语义 | 比较修复前后正常有效/无效样例、实际native输出与生成形状；跑完整Contracts lint、适用基线及受影响consumer定向检查 | 通用与leaf均通过；原拒绝边界保持；没有通过修改业务代码迁就schema |
| 5. 审查并收尾 | 逐文件检查差异，记录实际命令、失败/修正、consumer同步、来源摘要和未执行项 | 单独交付收口报告后停止；3B仍未开始 |

具体约束：

1. 版本注解只作为有明确类型/用途的元信息注册，不能全局允许任意`x-*`或删除所有未知关键字。
2. 条件声明采用对原字段定义的引用或必要的同义类型声明，不另写第二套业务校验；保留required、additionalProperties、枚举、边界、null/缺失区别。
3. canonical引用只解析已登记的仓内源，未知ID/fragment明确失败；全仓源预注册时保留其它schema已有行为和workflow的合法既有处理。
4. leaf resolver与通用checker读取同一权威源；生成物只有派生地位。不能只验证剥离注解的投影却继续让原始源在通用入口失败。
5. 修复前后比较覆盖：草案澄清/候选、四频率的条件字段、三种目标及已有聊天ID、有限grant、运行触发来源/逻辑槽/重跑引用、未知字段和显式null。仅使用普通合成输入，不构造攻击fixture。
6. 展开跨源片段时保留引用所属文档的上下文：draft内部的`#/…`不能被原样拷贝后错误地在storage根解释。源、投影、测试及actual-producer checker统一采用适用的`strict:true`；必要修正recovery生成器的条件声明，不留下其投影只能用宽松模式编译的缺口。

## 4. 修改范围和验收命令

预期实际修改以最小diff为准：

| 仓库 | 允许的收口范围 |
|---|---|
| Contracts | `validate-json-schemas.mjs`；定时源的同义规范化；必要leaf resolver/checker和普通conformance用例；生成物与source.lock |
| Desktop | 仅受影响的定时生成类型/schema/candidate摘要同步，以及必要生成符合性检查；不修改执行、目录、数据库或生命周期业务 |
| Host | 仅恢复族来源清单或确有派生差异的规范同步；不修改两个GET的处理逻辑、执行适配或Runtime管理 |
| 元仓 | 本批报告、实际状态、来源与检查结果 |

必须实际完成：

- Contracts完整`pnpm lint`退出0；API已有非阻断提示据实保留，不靠降低规则消除失败。
- 三个定时族的定向generate/check/sync与schema用例通过；新旧源均完成适用严格检查，修复前后有效/无效样例判定一致。
- 四个现有支持/fallback基线逐一检查，沿用10登记的完整SHA；新增或改变引用还需人工确认同义性，结构工具绿色不替代此判断。
- Desktop实际Rust producer与源conformance；生成Rust/TS受影响时做相应编译/静态检查和现有22项安全native回归，不启动App/Host/Runtime。
- Host来源如更新，运行其定向candidate同步/只读恢复检查；不因摘要变化扩写Host业务。
- 元仓strict/D0/audit-claims、适用治理检查、diff/status和源摘要核对。只按实际结果更新最新状态，10中的历史FAIL不改成过去已经PASS。

不运行含禁止故障/攻击fixture的全量测试或全局危险fixture生成；采用既有安全leaf入口与定向集合，并在报告列明未执行项及影响。不新增依赖、提交、推送、发布或改分支/远端。

## 5. 3B的接续前提，当前不实施

收口通过后，3B仍按09处理目录、组合事务、恢复与生命周期。开工先收敛一个具体接入点：`execution.rs:136–170`目前把有conversation_id的目标解释为UserProject，并将完整definition/workspace纳入grant摘要。若直接回写专属会话ID，会改变摘要，使原grant变stale。3B应区分**稳定的已授权目标策略**与**native实际会话/目录绑定**；用户真正修改目标仍需重新授权。这是尚未接入能力的前置设计问题，本次lint收口不顺手修改它。

当前预约primitive只写manual，没有生产调用者；定时outbox仍被guard阻止发送，没有预约释放、Host恢复查询消费、正常退出或sleep/wake屏障。3A通过不能直接成为可投递资格，3B不得通过删除这些保护来“接通”。

## 6. 明确停点

下一次只交付契约收口结果，完成后停止，不自动开始3B目录或事务。本轮只保存方案，没有运行修复、生成器或业务检查。普通入口仍以schema15为迁移目标；不访问/迁移日常库，不启动服务，不调用模型。文本额度仍 **0/12**，图片/商家接口 **0**，完整Must/D4仍NOT RUN。
