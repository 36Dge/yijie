# FEAT-154 跨仓改动与原提交清单（已执行）

> 本文保留2026-09-16授权前清单。用户随后授权并继续执行，实际提交/检查见[18](18-local-commit-baseline.md)，当前状态见[16](16-delivery-status-and-evidence.md)。下文“待授权”及旧摘要属于当时记录。

## 1. 审阅入口与范围

[逐文件清单](evidence/delivery-package/cross-repository-files.json)按仓记录 branch、完整 HEAD、origin、Git状态、文件用途、拟提交单元及 SHA-256；未跟踪目录已经展开，不只列目录名。[可读文件表](evidence/delivery-package/cross-repository-files.md)供人工逐项核对。清单是当前工作树快照，提交前必须核对新鲜度；自引用清单和最后检查文件的摘要例外有明确原因。

本轮只写元仓 FEAT-154 资料。下表是前序累计改动，不能解读为本轮重新修改了六仓实现。各角色的 Owner 为段成威；Codex 整理，未声称独立人工评审或新的提交授权。

| 仓库 | 展开后的累计文件 | 拟交付内容 | 审阅重点 |
|---|---:|---|---|
| Contracts | 10 | dirty通知说明、版本、同源SDK/Schema/源锁、符合性测试 | semantic；形状不变不代表语义无影响；来源必须先提交 |
| Coze | 72：FEAT-154为71，独立主题为1 | 30目录/控件/画布、实例与草稿隔离、恢复/撤销/键盘、生成定义、私有恢复读取、契约消费者与CSP记录 | 不加入节点API/执行逻辑；`yijie-upstream.lock.json`含既有主题项排序，不能删除已有来源声明 |
| Desktop | 7 | 页面离开保护说明、消费者派生物及页面测试 | 没有新增native退出保证；试运行UI可点击与执行发送资格分开 |
| API | 4 | 源/消费者锁2份，恢复只读SQL/Python2份 | 无新增电商节点handler、业务处理或数据库迁移 |
| Infra | 6 | 显式恢复命令、阶段与保护副本、私有核验编排、聚焦测试和runbook | 不修改既有历史退出记录；正常停止与失败留现场；禁止项不执行 |
| 元仓 yijie | 见动态文件清单 | 来源快照、需求/D0/实施/验收记录、本证据包；另列14份FEAT-153文档/证据 | FEAT-153依赖与FEAT-154分别提交；不将运行数据、App或镜像收入元仓 |
| Agent Host | 0 | 无提交 | 只记录清洁基线 |

## 2. FEAT-153 主题依赖

当前实际验收包包含 `yijie-coze/frontend/apps/workflow-local/src/yijie-coze-theme.css` 的既有用户修改，SHA-256为 `c05eb803a63a84e1097fb2851109c2302e8c7d76e8ffe53d409f0014c1593820`。主题说明和证据是元仓 FEAT-153 的26、27及对应两个证据目录，共14个文件。

上述15个文件本轮全部保护。它们不混入FEAT-154实现提交，也不能在记录构建来源时忽略。建议将Coze主题与元仓主题记录作为两个明确的FEAT-153依赖提交；这两项列在待授权清单内，不能借用历史其他任务的Git授权。如果用户仅授权FEAT-154，不触碰这15个文件，交付仍须注明含未提交主题依赖，不能声明完整可复现提交基线。

## 3. 生成物来源及验证说明

| 生成物/记录 | 权威来源与生成入口 | 已有验证与限制 |
|---|---|---|
| Contracts Schema/SDK/source.lock | `jsonschema/workflow-editor/bridge-v1.schema.json`、`openapi/workflow-local/workflow-local.yaml`；`make workflow-generate` | [source-first记录](evidence/step2-implementation/contract-source-consumer-checks.json)：专用generate/check、16项测试、lint通过；12条既有unused警告；旧32dd基线FAIL保留 |
| API/Coze/Desktop契约派生与lock | Contracts `scripts/sync-workflow-consumer.mjs`，按仓同步；仅TypeScript导入路径做canonical投影 | 当前为`--local-candidate`，`source_commit`尚未固定；待来源提交后逐个使用`--source-commit`完整SHA并`--check`，不手改生成物 |
| Coze `local-ecommerce/catalog-source.ts` | 元仓三份MD来源快照；`python3 scripts/yijie/workflow-editor-ecommerce-source.py` | 634行原文/类型/帮助/必填与目录聚焦检查；对象子项、中文标签、控件映射是受审手写UI元数据，不冒称全部自动生成 |
| Coze upstream/CSP记录 | 固定上游源、声明的overlay列表、标准构建资产调用点审阅 | 43项focused、3项CSP；126既有类型诊断、新增0；15221原文件不变、78 overlay、6处保留删除。不是上游全套测试零诊断 |
| Editor/App/服务镜像 | Coze canonical `workflow-editor.mjs`构建；Infra登记/build/up；Desktop `pnpm tauri:demo-fast:app` | [候选身份](evidence/delivery-package/candidate.json)。二进制/镜像不纳入源码提交；来源锁变更后不得沿用旧manifest声称新候选通过 |
| API/Coze私有恢复读取、Infra阶段记录 | 各自私有存储模型及显式恢复脚本，无公共节点协议 | [恢复记录](evidence/recovery-execution/recovery-result.json)：9项恢复＋13项既有生命周期检查，失败0；正常停止成功。停止卷副本未做还原演练 |
| Desktop页面与消费者 | 现有页面保护及同源桥定义 | [源与消费者检查](evidence/step2-implementation/contract-source-consumer-checks.json)：4文件23项测试及lint；后续真实页面交互另见R7/R2 |
| 元仓证据归档 | 既有真实日志/JSON、用户决定、当前只读SHA；非重新执行产品 | [本轮检查](evidence/delivery-package/package-checks.json)。真实截图未能导出，登记缺口，不能以静态预览代替 |

完整需求累计 `contract-impact=semantic`；本轮证据与清单整理 `none`。Infra恢复入口的阶段/失败含义由其私有部署runbook负责，不扩展节点业务协议。

## 4. 授权后的提交顺序

下列为待授权本地提交单元；不包含 push、tag、PR合并、部署或系统设置操作。当前保持原分支，未擅自创建或切换；分支名和完整HEAD见清单。授权时若指定新分支，再按该指令执行。

| 顺序/单元 | 仓库及精确范围来源 | 建议提交标题 | 依赖与操作 |
|---|---|---|---|
| 1 / T0 | Coze：仅主题CSS 1文件 | `style(feat-153): preserve workflow canvas and lime theme` | 独立既有主题依赖；需提交授权明确包含 |
| 2 / C1 | Contracts：清单10文件 | `feat(feat-154): clarify page-local dirty bridge semantics` | 先检查专用生成一致性并提交源；取得真实完整commit，不虚构预填SHA |
| 3 / A1 | API：清单4文件 | `feat(feat-154): pin workflow contract and add recovery reads` | 用C1完整SHA canonical同步，复查只读恢复代码及实际生成差异，再提交 |
| 4 / Z1 | Coze：除T0的71文件 | `feat(feat-154): register 30 ecommerce nodes for UI design` | 依赖T0/C1及已核对摘要的元仓资料快照；同步C1并检查源定义/锁/纯UI隔离/CSP；含私有恢复读取 |
| 5 / D1 | Desktop：清单7文件 | `feat(feat-154): clarify page-local design leave protection` | 同步C1；页面保护与消费者聚焦检查后提交 |
| 6 / I1 | Infra：清单6文件 | `feat(feat-154): add explicit local workflow recovery` | A1/Z1提供私有恢复读取；执行非破坏性聚焦检查；提交不触发恢复/服务重启 |
| 7 / T1 | 元仓：FEAT-153主题14文件 | `docs(feat-153): record preserved workflow theme` | 与T0关联，独立提交；不归入FEAT-154完成项 |
| 8 / M1 | 元仓：完整FEAT-154需求包及全部选中可跟踪证据 | `docs(feat-154): record implementation and pending acceptance` | 回填实际跨仓commit及重新验证结果；保持AC-009 pending、D4 NOT RUN；不得写“全部验收完成” |

提交前先按来源记录核对元仓四份原资料及三份Markdown快照。它们已在当前兄弟仓工作区可供Coze生成器读取，最后随完整需求包M1提交并记录该元仓commit；跨机器复现需同时取用该元仓版本。不要提前只提交零散资料而留下缺失feature.yaml/核心文档的不完整需求包。

API、Coze、Desktop的sync在Contracts仓逐条执行：`node scripts/sync-workflow-consumer.mjs <consumer> --source-commit <C1完整SHA>`，随后逐条`--check`。这是授权后的命令说明，本次未执行。源提交后仅consumer lock变化也会影响构建来源摘要；如需交付新App候选，应另按既有canonical流程构建/登记/激活与定向复验，不能把现有f608候选改名当作新产物。提交本身不需要本轮重复启动服务。

## 5. 执行前后的检查清单

1. 对照精确清单重算工作树SHA，确认HEAD、分支、远端和index没有非预期变化；发现新改动先更新清单。只暂存逐仓所选文件，不使用跨仓或整仓`git add .`。
2. 先处理明确列出的资料/主题依赖，Contracts源先于消费者。专用workflow生成/同步若产生新增路径，重新列入审阅范围；当前清单不能掩盖后续生成差异。
3. 复用仍同源的历史测试证据；对固定commit带来的源锁/生成物变化执行对应source/consumer一致性检查。Coze或Desktop实现若变化，运行对应聚焦测试和必要构建。用户禁止的故障/攻击场景继续NOT RUN，不执行泛化全仓危险fixture。
4. 每个提交前审阅staged diff、排除真实凭据、原始运行目录、数据库副本、二进制和38份未选中日志；提交后记录实际SHA及剩余工作树状态。
5. 最后更新元仓交付表。Git提交、历史记录归档、当前UI可用和完整D4是不同结论，分别如实记录。没有推送、发布或关闭D4的默认授权。
