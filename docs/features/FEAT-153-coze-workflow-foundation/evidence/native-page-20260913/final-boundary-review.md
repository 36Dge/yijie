# FEAT-153 原生 Coze 页面替换：最终边界审查与交付清单

最新结论见末尾 **23:04 CST 最终补充**：canonical 20 的受控功能及正常重启持久化证据已补齐；主题 **DEFERRED BY USER**，dev/统一 fresh D4 **NOT RUN**。较早章节保留审查过程中的候选状态。

- 审查时间：2026-09-13 22:42 CST。
- 性质：独立、只读源码与现有证据复核；本文件自身 `contract-impact=none`，不改变任何运行边界。
- 截止状态：canonical 18 已有部分真实 App 记录；19 正在重建，计划由 canonical 20 固定最终候选并复验。这里的“最终”指交付审查清单，不表示 20 已验收或整个需求已 fresh D4。
- 操作范围：读取源码、Git 差异、摘要和证据，执行正常 focused 检查。未启动/停止 App 或栈，未连接数据库，未改业务源码、构建产物、权限或 Git 状态。只新增本审查文件。

## 结论与确定问题

当前实现实际挂载仓库内的原生 `WorkflowPlayground`，复用 Coze 的 Header、无限画布、节点渲染、表单和底部工具栏；不是原先自行绘制页面的换肤。Desktop 完整页的重复顶栏已移除，原有版本与运行记录弹窗由一个有限的 `request_history` 事件打开。

本次源码审查未发现新增凭据权限、HTTP 操作、Tauri 命令或 Chat 传输边界。Contracts 1.3 三个已登记消费者的同源检查通过。该结论限于当前受控 local 三节点能力，不等于启用 Coze 全部节点、外部服务或生产部署。

仍有必须准确披露的事项：

1. **最终候选尚未在此审查中固定。** 重建期间 `workflow-editor.mjs check` 返回 `Editor source digest differs`；此时源码已前进而旧 manifest 尚未更新，是正在重建的状态，不可记录 PASS。canonical 20 的 manifest、来源摘要、完整静态资源检查和真实加载须使用 builder/root 的后续记录。
2. **canonical 18 首次保存的 native reload/Undo 保留问题正在修复。** 后续已经验证一次画布键盘移动及 native Undo 读回，但不能据此声明首次保存从未清空历史；20 仍需实际复验首次保存不 reload、Undo 保持。
3. **Tauri listener cleanup 的既有错误仍是已知边界。** 详见 [基线说明](native-tauri-listener-baseline.md)。源码和锁版本早于本轮，不代表已证明无影响。基线有 3 条 `listeners[eventId].handlerId` rejection；不能把源码未修改等同于 Chat 生命周期已通过，最终正常 Chat 切换应另记观察结果。
4. **当前 dev 和统一 fresh D4：NOT RUN。** 历史 FEAT-153 D4、旧 packaged 和旧主题尺寸证据不得替代当前原生页面候选的验收。

## Contracts 来源、方向及消费者

权威源是 `yijie-contracts/jsonschema/workflow-editor/bridge-v1.schema.json`，生成物、迁移语义及激活顺序见同仓 `docs/workflow-local-v1.md`、`docs/workflow-local-candidate-generation.md`。本轮先改权威源、生成与检查，再以 `--local-candidate` 同步 API、Coze、Desktop；没有手写第二份 wire DTO。

| 核对项 | 当前事实 |
| --- | --- |
| 计划版本 | `1.3.0-local-candidate`，`mode=local_candidate`，不是发布 tag |
| 基线 commit | `32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4` |
| 权威 `source.lock.json` SHA-256 | `86a5e8158aa492630e7494eb9f021b6feb8d9a710cd73bb3bfe934a955a4381d` |
| 登记消费者 | `yijie-api`、`yijie-coze`、`yijie-desktop`；三份投影和来源锁均通过 fresh `--check` |
| 本次桥接增量 | 仅新增 `kind=request_history`；沿用 `protocol_version=1`、`request_id`、`bridge_id`、`generation` |
| 载荷限制 | `request_history` 不携带 `dirty/request/response/error`；不接收任意 workflow ID、URL、命令或凭据 |
| 既有交互 | connect/ready/request/response/dirty_changed/request_close 的原约束保持可读 |
| 旧严格消费者 | 会拒绝新 kind；必须先就绪 Desktop consumer，再启用同源 Coze producer，不承诺新 producer 可向旧 Desktop 发送此事件 |
| 保留的前序增量 | 1.2 description、metadata opt-in 及 revision 绑定删除；未回退，不能归因成这次原生页面新加的权限 |

结构 additive 与定向本地激活的条件均已明确；旧 consumer 拒绝新事件的事实没有被 schema checker 绿色掩盖。JSON Schema 检查器的本次增强只接受严格证明“不约束旧必填闭合 enum 有效值”的追加条件分支；旧分支被收紧、判别字段非必填等情况继续拒绝。

本轮此前已对已交付工作流来源及登记 fallback 基线执行过兼容检查；本文件新增的 fresh 检查是下面列出的 focused tests，不把历史 breaking 检查冒充本次重新执行。尚未形成此次 1.3 的不可变 source commit/pins。后续合并顺序仍为 Contracts 源提交 → API/Coze/Desktop 同步并固定完整 commit → consumer 就绪后激活 producer；公开或生产交付不得直接使用 dirty sibling candidate。

## Desktop 与原生页边界

| 边界 | 源码核对结果 |
| --- | --- |
| 完整页布局 | `WorkflowEditorPane.vue` 的外层 header 使用 `v-if="!fullPage"`；Workspace 传入 `full-page`。原生 Header 承担标题、返回、保存、发布和运行记录入口；非 fullPage 模式保留原 header/actions 兼容性 |
| 加载与错误退出 | Desktop 初次打开有返回/取消；连接阻断 overlay 有返回及显式重连；Coze lazy-loading 和 ErrorBoundary 均保留返回入口 |
| 会话载体 | Pane 以 workflow ID 为 key，更新 bridge generation 时保留同一 iframe DOM；会话到期通过遮罩/inert 阻止操作，保持草稿；重连必须显式触发 |
| iframe | 固定 `http://127.0.0.1:18888/editor/`，固定 origin 及 MessagePort；sandbox/拒绝 camera、microphone、geolocation、clipboard/no-referrer 设置保持 |
| 消息校验 | 生成 validator、524,288 字节上限、当前 bridge ID/generation、ready 前置；旧端口关闭后停止接受消息 |
| history | 校验后只调用当前 UI hook；打开已有记录弹窗，数据仍绑定当前 editor。该事件本身不执行 native exchange，也不向页面下发凭据 |
| 保存与离开 | pending write、创建、重连、关闭及运行期间阻止离开；dirty 或结果待确认时显示继续编辑/放弃本地内容确认；正常关闭仍经过现有 native 会话撤销 |
| 原有边界保护 | 当前 diff 未改变 Tauri capabilities、Tauri 配置、Chat 页面/store/传输客户端、Desktop pnpm/Cargo 锁；Infra 工作树无改动 |

“iframe 页面可见”不等同于“可以凭页面自行执行服务操作”。认证仍留在既有 native/API/Coze 服务链路，桥只接受既有有限操作；本轮没有将 Coze 全站账号、工作空间或 provider 权限引入 Desktop。

Coze 适配器保持稳定实例及缓存 snapshot，订阅不因 render 创建新 DI 容器。保存服务的本地加载/订阅以 dispose 与 generation 守卫收尾；同一草稿收到自身保存回执时比较归一化后的文档 key，避免不必要 reload。真正远端更新仅在干净、同版本且仍存活的状态下替换。`DraftModel.normalize` 对节点、位置、连线及文本含义进行保义核对，只有本地字符串的冗余类型提示等明确等价表示可归一化；新 focused tests 也验证其余元数据不能静默变成“已保存”。

原生组件依赖图较广，不以“UI 没显示”推断全部代码休眠。现有 [CSP 可达性说明](local-native-csp-reachability.md)、[17 精确字节审查](native-csp-17-reviewed.md) 和 builder 的最终资源审查共同约束实际加载。当前 Text 用原生 ExpressionEditor/CodeMirror；没有新增可达的 TypeScript Worker 功能。Shiki 通过透明的原 API wrapper 选择锁内 JavaScript regex engine，修复实际出现过的 eager WASM 初始化；没有放宽 `worker-src`、`connect-src` 或加入 `unsafe-eval`。这不代表未来任意 Shiki singleton/其他节点也自动符合该结论，增加节点需重新审查。

## 本次 fresh 检查与证据适用范围

以下命令在 2026-09-13 22:37–22:41 CST 对当前工作树执行，退出码及结果来自实际工具输出。均为正常、有限测试，没有异常注入或攻击 fixture。

| 仓库 / 检查 | 结果 | 能证明 / 不能证明 |
| --- | --- | --- |
| Contracts：`node scripts/sync-workflow-consumer.mjs api --check`，对 coze、desktop 同样执行 | PASS，3 consumers | 同源 source/generated/projection/lock；不是发布 pin |
| Contracts：`make workflow-test` | PASS，14 tests | 有限工作流契约与浏览器一致性；不是整个 Contracts 仓全量测试 |
| Contracts：`node --test tests/jsonschema-breaking.test.mjs` | PASS，6 tests | 检查器的兼容/收紧分支；不代替真实消费者方向审查 |
| Desktop：`pnpm lint` | PASS | 当前 lint；不证明 UI 或 native 会话运行 |
| Desktop：Vitest 四个文件 `WorkflowEditorPane`、`WorkflowLocalWorkspace`、`use-workflow-workspace`、`workflow-navigation` | PASS，4 files / 16 tests | 完整页 header、history、同 iframe 显式重连、离开等 focused 行为；不是 App/E2E |
| Coze：`node --test scripts/yijie/workflow-editor-bridge.test.mjs scripts/yijie/workflow-editor-state.test.mjs` | PASS，15 tests | 回执关联、重连、history 当前绑定、草稿保留、归一化保义；不是原生画布实际渲染 |
| Coze：`node scripts/yijie/workflow-editor.mjs check` | NOT PASS：`Editor source digest differs` | 19 重建期间运行，旧 manifest 与当前源不一致；未改 manifest 或重建以覆盖该记录，最终 20 由 builder 复核 |
| 上条失败后同一命令串中的 Coze `make lint && make test` | NOT RUN | 串行命令在前置 check 失败后未执行；不把之前源保持检查当作此刻 fresh PASS |

Desktop 测试出现 Node `localStorage` 实验性提示；Coze state tests 出现 package module 类型推断警告，均未造成用例失败。没有为消除提示修改依赖或运行时。

此前 `native-build-18-typecheck.json` 的结论是 `PASS_WITH_REPORTED_UPSTREAM_BASELINE`：当前与固定原版各有 126 条诊断，新增/修改源诊断为空；它不是全上游“零类型错误”。此前 bridge-state 记录为 13 tests；本次已包含后续普通归一化新增用例而 fresh 通过 15 tests。

## 已有工作区与改动范围

当前 Git diff 是首次 FEAT-153 已提交版本之后多个连续 UI 调整的累计差异，不能全部归因于此次 native 页面。以 `card-menu-20260913/candidate-files.json` 已记录文件为参照，fresh SHA-256 比较结果如下；未列入旧清单的新文件由本轮源码/构建清单审查覆盖。

| 仓库 | 旧清单文件数 | 字节保持 | 已变化 | 缺失 |
| --- | ---: | ---: | ---: | ---: |
| Contracts | 10 | 5 | 5（来源锁、版本、生成物、相关测试） | 0 |
| API | 12 | 10 | 2（consumer lock 与 source-lock） | 0 |
| Coze | 15 | 10 | 5（生成契约/来源锁/validator 与主入口） | 0 |
| Desktop | 37 | 31 | 6（锁/validator/Pane/Workspace/相关测试） | 0 |

因此，前序已完成的 description/delete API 与 Coze 后端实现未被本轮替换；创建表单中文名称、概览颜色、卡片横向列表和更多菜单等前序改动仍保留。另有两项曾明确保护的 Desktop 用户工作区文件，当前 hash 与旧记录相同：

- `src/components/workflows/RecommendedWorkflowCard.vue`：`3ededb7050fb50450e72daed9592a9ec9af631d9e51450cede893780bd600c8a`。
- `docs/verification/workflow-interactions-and-lime-20260911.md`：`e69a2073873d6f548011d149c83fe15245c98fddbab12eea953fdb95fba8799b`。

Coze 仍基于原来源 `fefb05ff27be1da939612fbf9faf5db62583b8ae`。六份 NATS/OceanBase/Pulsar 中英文集成文档的既有删除保留，不能记成此次删除；源码保留门禁将其作为已登记状态。未 reset、checkout、格式化无关文件或创建/推送提交。

## 交付前还需挂接的最终证据

| 项目 | 截止本记录的状态 |
| --- | --- |
| 原生页面存在并复用 | 源码确定；仓库原生 `WorkflowPlayground` 是活动入口，旧自画 `native-canvas.tsx` 不再由主入口使用 |
| 18 同一 App 创建、保存、文本/坐标读回 | 有 `native-workflow-created.json`、`native-first-saved.json` 及 keyboard move/undo 证据；这里只核对记录存在和内容，不冒充本审查员操作 |
| 18 自然到期、重连、保存 | 有 `app18-natural-expiry-dirty.json`、`app18-reconnected-saved.json`；不能替代 20 变更后的剩余确认 |
| 18 版本执行与普通错误修正 | 有 `app18-run-version-success.json`、`app18-version-error-recovered.json` |
| 20 来源与可复现构建 | PENDING：需最终 source digest、manifest、检查及重复构建记录；旧 `candidate-before-activation.json` 是早期候选，不能视为最终跨仓 freeze |
| 20 首次保存不 reload、native Undo | PENDING：root 计划实际复验 |
| 20 亮/暗主题与两种窗口尺寸 | PENDING：需实际截图、焦点/布局观察 |
| 20 正常关闭取消、Chat 切换、重启读回 | PENDING：需真实 App 与原生日志；不可由源码 guard 推导 PASS |
| 20 新合成流程与原有资源保留 | PENDING：等受控服务健康及 root 指定新合成 ID 后，只读核对数据库/API；本审查尚未连接 |
| 当前 dev 验收 | NOT RUN |
| 当前统一 fresh D4 | NOT RUN；不以旧需求结论、单元测试或分散旧候选记录拼接通过 |
| public / production / 商家模型节点 | OUT OF SCOPE；没有新增授权或生产资格 |

最终结论应由同一固定候选的构建、实际 App、必要数据库读回及已知限制共同形成。后续实际记录如补齐，更新这些具体状态；保留历史失败和本次重建期间 check 不匹配的事实。

本文件完成后的元仓门禁：`pnpm lint` PASS、`pnpm test` 50/50 PASS、`bash -n scripts/*.sh` PASS、`git diff --check` PASS；没有运行会递归触发兄弟仓全量测试的根 `make lint/test`。

## 22:54 CST 补充：canonical 20 来源及只读持久化核对

以下新增事实更新上表对应的 PENDING 项，不改写 22:42 时重建尚未结束的历史记录，也不替代 root 的实际 UI 结论。

- [20 实际服务激活记录](activation-20-verification.json) 与 [19/20 可复现构建记录](native-build-19-20-reproducibility.json) 已产生：385 项资源、45,282,354 字节；manifest SHA-256 为 `d5176e19616f5935ec85d1aa3e9efa7c54ef8d15d7de97a19270009b0a5fa79a`，source digest 为 `feaa8e90180db13d2b479c0cd36bd24c624df20dc176e144837c5e950ab4d95c`。激活记录显示资源与 manifest 一致、实际入口一致、公开资源中两个机器凭据匹配数为 0；这不是浏览器 heap 扫描。
- 本审查员在 root 告知受控栈 ready 后执行 [只读 API/MySQL/PostgreSQL 读回](canonical20-readback.json)：旧截图工作流 `7684953519702409216` 的完整 legacy 与 metadata 响应仍与 `existing-screenshot-workflow-before.json` 完全相同。18 合成流程 `7685009958215090176` 的画布、名称、描述及 revision 保留，内部版本 `v0.0.1` 及“易界验收 / 版本执行验收 / 修正验收”三次精确成功结果均由 API 与 MySQL 读回，PG/MySQL 共享回执一致。18 Undo 保存记录早于发布，故发布版本及更新时间的正常变化明确单列，未要求其与发布前字节相同。
- [20 首存读回](canonical20-first-save-db-readback.json) 核对新合成流程 `7685031373442121728`，revision `7685031776485376000`：与 `native20-saved.json` 的首次保存画布一致，三节点、两连线及 `原生终验：{{input}}` 前缀保留；API 与 MySQL UTF-8 字节数和 SHA-256 一致。这证明持久化，不独立证明首次保存没有 UI reload 或 Undo/Redo 表现。
- [20 正常重启前完整快照](canonical20-final-before-normal-restart.json) 已固定同一新流程的草稿、`v0.0.1` 版本、完整两条历史、两个 run 及 PG/MySQL 持久化状态：试运行 `7685032443987886080` 的 `页面终验 → 原生终验：页面终验`、版本执行 `7685032637395632128` 的 `版本终验 → 原生终验：版本终验` 均为实际成功终态，输入/输出精确相等，版本画布与草稿一致，5 份共享操作回执均一致。

这些脚本仅对 root 明确指定的工作流执行 GET 与 SQL `SELECT`，没有发出 INSERT/UPDATE/DELETE、事务写入、UI 或服务生命周期命令。API 的正常 GET 会按已有服务规则追加读取审计，不改变工作流业务数据。数据库密码读取既有只读挂载后仅驻留容器进程内存/环境，没有写新凭据文件、命令行参数或证据；落盘前检查机器 token 不在结果中。数据库采用普通独立 SELECT 读，不声称跨库原子快照。20 的正常重启后对照、主题尺寸、Chat 等仍需后续记录；dev/统一 fresh D4 状态不变。

## 23:04 CST 最终补充：功能与重启读回完成，主题由用户延期

**当前限定结论：原生页面替换的受控功能主链路和正常重启后的持久化已取得 canonical 20 证据；本记录不宣布整个 FEAT-153 获得新的统一 D4。** Root 实际操作的页面证据与本审查员执行的数据库/API 读取分别列出，来源不混淆。

| 功能项 | 当前证据与结论 |
| --- | --- |
| 原生首存、配置面板及 Undo | Root 实际 App 记录 [首存面板保留](app20-first-save-sidebar-preserved.json)、[首次保存后 Undo 保留](app20-first-save-undo-preserved.json)；本审查员的 [首存数据库核对](canonical20-first-save-db-readback.json) 独立确认原生三节点两连线、文本及坐标持久化，revision `7685031776485376000` |
| 试运行、内部发布、版本执行与历史 | [真实页面成功记录](app20-version-run-and-history-success.json)；两库与 API 精确对应 `页面终验 → 原生终验：页面终验` 和 `版本终验 → 原生终验：版本终验`，没有通过测试脚本执行这些业务写操作 |
| 关闭取消、Chat 切换及重开 | Root 已记录未保存离开取消、干净关闭再切换、重新打开；[Chat 实际页面](app20-chat-after-clean-close.json) 可见任务输入区。没有修改 Chat/native event cleanup 源码；较早 Tauri 错误来源分析继续保留，本记录不扩展成任意 Chat 生命周期无问题的保证 |
| 正常重启后的真实画布 | Root 的 [App 重启实际前缀读回](app20-restart-actual-prefix.json) 可见正确标题、已保存状态及 `原生终验：{{input}}` |
| 正常重启后的完整数据 | 本审查员执行 [重启后完整只读对照](canonical20-final-after-normal-restart.json)：manifest、source digest、完整 workflow、画布 hash、完整 history、两次 run 全字段、MySQL 资源/版本/执行/操作行与 PostgreSQL 资源/操作行，全部与 [重启前](canonical20-final-before-normal-restart.json) 相同 |
| 审计保留 | 原有 32 行工作流审计完整保留，新增 11 行仅成功 `read/bootstrap/history/read_run`。GET 及重开产生正常读取审计，因此验证追加语义，不错误要求审计总行数不变 |
| 原有用户资源 | 旧截图流程完整 legacy/metadata 响应已证明保持，18 合成流程三次成功结果也已重启读回；没有对其执行保存、删除或重新发布 |
| 主题及主题尺寸资格 | **DEFERRED BY USER，未通过主题验收。** 用户明确暂停，后续统一易界品牌颜色；已观察的暗色可读性问题保留于 [延期审计](native-theme-deferred-audit.md)，不得用已拍截图冒充通过 |
| dev / 统一 fresh D4 | **NOT RUN**，没有从之前 FEAT-153 或不同候选借用 PASS |

主题相关的短暂源改动已由所属实施者精确撤销，未发布主题修复，也未构建 canonical 21/22。[恢复检查](native20-source-restored-check.txt) 和 [20 重启实际激活验证](activation-20-restart-verification.json) 确认继续使用相同 `feaa8e90180db13d2b479c0cd36bd24c624df20dc176e144837c5e950ab4d95c` 来源、相同 manifest、385 项资源，公开资源机器凭据匹配数仍为 0，CSP 未放宽。

此次正常恢复建立新 run epoch `b13e0089-5888-43ac-b25b-0440956373ea`，原 epoch 为 `28a9b428-3eed-4b0e-ae96-5d1dc2001b92`。观察脚本首次因固定旧 epoch 正确停止，随后依据 root 提供的明确 ready/activation 记录固定新 epoch 才继续；没有绕过 guard 或把恢复解释成旧会话复用。业务数据逐字段比较通过不能独自证明内存会话撤销，该项继续依据 native/实际 App 证据。

本次交付清单包括 source-first 契约/消费者、原生页面适配及 canonical 构建、Desktop 有限桥接与完整页、上述真实功能及只读持久化记录、已保留的工作区差异、主题延期与 dev/D4 限制。没有执行提交、推送、公开激活或生产部署。

最终补充后再次执行元仓 `pnpm lint`、50 项 `pnpm test`、Shell 语法和 `git diff --check`，均通过；三个只读观察脚本也通过 Python AST 语法核对。观察脚本产生的自身 import cache 已正常清理。
