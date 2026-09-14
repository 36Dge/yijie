# 2026-09-14 全仓审计、提交与远端同步

用户明确授权审计项目所有仓库的改动，由Codex拟定提交说明并执行git add、commit、push；中途两次暂停，随后明确恢复。范围是`repos.yaml`中的11个子仓和元仓，共12仓，沿用当前工作分支及各自`36Dge` origin，不切换分支、不强推、不推上游、不创建tag或部署。

## 当前交付进度

本次开始时5仓有改动、7仓工作树干净且远端一致。已完成4个子仓的5个提交；Contracts在暂停前已推送成功，恢复后的`ls-remote`再次确认。API、Desktop、Coze已按顺序普通推送成功，元仓最后提交本报告和FEAT-153追加证据。逐仓观测保存在[证据目录](evidence/workspace-git-sync-2026-09-14/)。元仓自身提交与远端SHA由该文件Git历史及最后的远端核对定位，不在提交内容中预填未来SHA。

FEAT-153的19—25文档中“未提交”“App运行中”等表述保留各自验收时点的历史含义；当前Git交付以本报告及实际Git远端为准。本次没有重新启动App或将Git推送当作新部署。

| 仓库 | 当前分支 | 本次提交 / 最终子仓HEAD | 内容 |
|---|---|---|---|
| yijie-contracts | chore/retirement-baseline-20260905 | `0543b21c61c39ea1d18833b25c5d376a32913979` | 描述协商、版本绑定软删除、原生历史导航源契约及生成物 |
| yijie-api | feat/feat-126-foundation-closure | `d38bb9e851a34244498e09c8b188901f9261b9b9` | 描述元数据、归属/审计、版本绑定软删除 |
| yijie-desktop | chore/retirement-baseline-20260905 | `d546c3c9698bb1f5cfe84b7f556798f8e7d5bbc2` → `6078855f7966a531b4d740dd6e654cf60d4180d8` | 先修两处既有Clippy问题，再交付独立编辑页、创建/删除确认与工作流卡片 |
| yijie-coze | main | `10faf164d7af194b7697a93cb3c4a6886ddc64b5` | 原生Coze完整页、本地适配、软删除与青柠主题；记录六份既有文档缺失 |
| yijie | chore/retirement-baseline-20260905 | 由本报告所在Git提交定位 | 追加需求文档、真实验收记录与本轮全仓同步说明 |

以下7仓没有本次改动或待推送提交，恢复时通过真实远端查询确认HEAD一致：

| 仓库 | 分支 | HEAD |
|---|---|---|
| yijie-admin-web | develop | `d009cafccb112c098114c075d60f67ee5e0296d8` |
| yijie-agent-host | chore/retirement-baseline-20260905 | `0e47766f494977c94bfea0e89cfbdf45a7fafa2b` |
| yijie-codex | chore/retirement-baseline-20260905 | `6c1ad767f0997845b8258a1c452fd4eb7577579f` |
| yijie-connectors | develop | `273eec40bbbfeb17e817643f283db7c81e9b190c` |
| yijie-infra | feat/feat-126-s10e | `2b238d93cecd446dfd9b22fef681e2bd5ed70f02` |
| yijie-knowledge | develop | `e9091d2b673ba779ecb39271ce9148e3a41fc256` |
| yijie-skills | develop | `488714a8d96f40806a257aae097683815b1dd458` |

## 审计发现与处理

1. **整批最高契约影响为breaking。** 新Coze的`request_history`会被旧Desktop严格validator拒绝，并触发`protocol_mismatch`恢复遮罩、使画布inert；该分支不会直接撤销API会话或销毁草稿。Contracts说明和[原生页面方案](../features/FEAT-153-coze-workflow-foundation/22-native-coze-workflow-page.md)原先的additive/semantic分类已纠正。结构检查通过不代表新事件被旧reader接受。只允许同源配套local候选，先Desktop reader、后Coze producer，正常停用后配对回退；没有批准新旧混用或生产滚动升级。纯主题子集的`none`分类保持。
2. **源契约先固定。** Contracts提交完成后，通过canonical同步脚本为API、Coze、Desktop写入完整`source_commit=0543b21c61c39ea1d18833b25c5d376a32913979`并逐仓`--check`；生成的wire/schema/validator字节没有因pin更新改变，原public/Runtime锁不动。
3. **主题来源可追踪。** Desktop最终提交后重新生成主题来源记录，`source_head=6078855f7966a531b4d740dd6e654cf60d4180d8`；颜色源与生成CSS摘要保持原值，44个token未改变。
4. **修复两处既有Clippy问题。** 测试中的克隆改为`slice::from_ref`，local gate测试模块移动到普通item之后；独立提交，运行行为与授权条件不变。
5. **保留改动来源。** Desktop包含之前已确认的FEAT-151推荐卡收敛及设计记录。Coze六份NATS/OceanBase/Pulsar中英文指南在接入前已缺失，本次全量授权将删除纳入Git；固定上游提交仍保留原文，source checker继续允许缺失或原字节/模式存在，未放宽其余源文件校验。README同步更正旧状态。
6. **证据与秘密边界。** 审计包含待提交完整文本、当前机器凭据精确匹配和高置信秘密特征扫描；恢复后对52张PNG补充只读Vision OCR秘密模式扫描，均无命中。7个文本候选确认是运行时拼接Bearer的代码。没有构建二进制、node_modules、target或私密环境文件混入。匹配为0仅表示实际扫描范围，不是所有历史Git对象或所有敏感信息的完整证明。元仓保留合成工作流的实际截图和只读观察，不把候选/暂停记录重写为后来时点的验证。

## 验证与证据范围

以下提交前检查已在本任务暂停前真实执行并返回通过。临时`/tmp/yijie-git-audit-*`日志在恢复时已不存在，本表依据本任务保留的工具执行记录与代理回报整理，不伪造遗失日志或称为恢复后重跑：

| 范围 | 结果及限制 |
|---|---|
| Contracts | lint通过，保留12个Redocly warning；21个JSON Schema有效；20项工作流/浏览器/兼容检查测试通过；canonical生成前后15项源、生成物及锁字节相同 |
| 四个契约基线 | OpenAPI/Proto/AsyncAPI/JSON Schema结构检查通过：`32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4`、`811f38d6b104fa18477107e7ac91a85e19c445d1`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`29317b6426578749dc698fc2ad32b986ee5c8e9f`；语义限制以上述breaking结论为准 |
| API | `make workflow-lint workflow-test`通过，race及9个有测试包、consumer来源检查通过 |
| Desktop | lint、12文件50项前端定向测试、前端和文档构建通过；修复后fmt、all-targets严格Clippy、14项工作流Rust测试和1项相关Chat测试通过 |
| Coze | 来源治理、4包Go测试和vet、33项Node测试通过；15,237上游文件保持、6项缺失、62个overlay；190 workspace、44主题token、7,511源文件/2,127alias零差异、Shiki8例与拖拽3例正常smoke通过 |
| 真实App | 既有本轮功能及主题验收详见FEAT-153的19—24文档；最新实际试运行及13项两库定向核对见[24](../features/FEAT-153-coze-workflow-foundation/24-native-coze-lime-refinement.md)，不是本次Git同步新跑的UI/D4 |

恢复后只复核不可变提交/consumer来源、远端、元仓证据与文档门禁；新增日志保存在本报告证据目录。三consumer canonical来源检查、主题44token及CSS字节检查通过，元仓lint、50项测试与7份Shell逐文件语法检查通过；元仓扫描时点562文件、30.58MB，99个本地Markdown引用存在，最终7张截图SHA/尺寸与记录相符。日志及本报告在扫描后增加的文件单独做暂存检查，不将旧计数充作最终文件数。

本轮不再次启动App、容器或数据库，不消耗模型/商家/付费调用。用户禁止的攻击fixture、强杀、权限破坏、可执行文件劫持测试均未执行；安全定向检查不冒充上游全量或生产资格。

## 构建、发布和回退限制

canonical29是先前实际验收的构建。此次immutable pin、Desktop来源HEAD及Git HEAD变化后，其manifest不能被称作当前提交重新构建的结果。本次Git同步没有覆盖在线编辑器产物，也没有制作或激活新构建；下次本地更新仍走正常退出/受控停止→标准构建→登记→恢复入口。配对类型检查历史保留126项原上游诊断，不称上游TypeScript完全干净。

本次只推送各自当前分支，不合并、不签名发布、不打tag、不迁移数据库。远端CI和生产资格不由Git推送成功推导。元仓提交自身SHA由Git历史和推送后的最终核对给出，不在其内容中预填未来SHA。
