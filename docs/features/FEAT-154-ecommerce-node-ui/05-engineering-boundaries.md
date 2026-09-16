# FEAT-154 工程事实、取舍与边界

本文件保留需求起草时的调查与候选，当前第1步结论以[07](07-integration-design.md)、[08](08-node-registration-design.md)、[09](09-field-control-design.md)、[10](10-lifecycle-contract-design.md)为准：整体semantic已完成源码方向核对；页面离开保护与原生App退出分开，用户已明确排除原生退出保护。

## 1. 当前源码事实（2026-09-15）

以当前源码为准，FEAT-153 早期最小编辑器说明不覆盖后续原生页。未带仓名前缀的源码路径均相对 `yijie-coze/`。

| 事实 | 来源 |
|---|---|
| 元仓负责需求，Coze负责React工作流UI，Desktop提供Vue产品入口 | repos.yaml、各仓AGENTS/README、Accepted ADR-0019 |
| 真正入口挂载原生WorkflowPlayground，旧native-canvas不是活跃入口 | frontend/apps/workflow-local/src/main.tsx 的 createNativePlayground/NativeEditorBoundary |
| 官方NodePanel、NodeList、AtomNodeList存在且正在使用 | frontend/packages/workflow/playground/src/components/node-panel/components/ 下 panel.tsx/list.tsx/atom-node-list.tsx |
| 本地目录与点击/放置均限制唯一Text节点 | node-panel/hooks/use-template-node-list.ts、components/panel.tsx、toolbar/hooks/use-add-node.ts |
| 本地搜索主动跳过远端查询 | node-panel/hooks/use-search-node.ts 中 localAdapter提前返回 |
| 可提交图只允许1/15/2、两至三节点、最多两边 | frontend/apps/workflow-local/src/canvas-data.ts 的 decodeCanvas/localDocumentMeaning |
| 原生文档也限制类型、每类一个与复制；增删Text会改结束引用 | frontend/packages/workflow/playground/src/services/local-workflow-document.ts |
| 模板Map按type存储，30模板统一type不能直接覆盖注册 | frontend/packages/workflow/playground/src/workflow-playground-context.ts 的 templateMap/setTemplateInfo |
| normalize/change/changeName会改DraftModel，save/test/publish是真实写请求 | main.tsx 的adapter与save_draft/test_draft/publish_internal |
| 保存服务会在clean且revision改变时重载远端图 | frontend/packages/workflow/playground/src/services/workflow-save-service.ts 的 loadLocalDocument订阅 |
| 宿主离开保护当前来自model.dirty或runs.pending | main.tsx refresh/onConnect；bridge.ts dirty向现有dirty_changed事件投影 |
| 最新工作流颜色包含用户未提交的局部修改 | yijie-coze-theme.css；FEAT-153/26、27：#B7F03D / #B1E83C / #ABE03C，浅画布#F2F3F5 |
| 文档未给nodeType、注册ID、完整前端Schema；1–8独立配置，9–30配置在输入对象中 | 原始快照及04目录 |

以上由只读文件检查取得，不代表未来30节点已注册、编译或在App验证。

## 2. 推荐：同一原生页面的内存UI设计状态

以下为候选实现约束，本轮只记录，不编码，不冒称Owner已确认所有技术细节。

1. 复用现有WorkflowPlayground、NodePanel、卡片和NodeSideSheet；用前端“电商节点”类别和30个稳定catalog key区分目录。每次添加另有独立instance ID，并深复制初值，避免按type存储导致覆盖或串值。实际注册值后续核对，不把文档编号当wire enum，不假冒type=15。
2. 实例位置、输入字面值/本地引用、配置、输出定义保存在renderer内存。可采用公共骨架和30份UI元数据；这些是展示模型，不是公共业务契约或执行Schema。
3. 首次添加电商节点建立页面内设计状态，同时保留原provider草稿、原有未保存值、名称和位置。新图不进入DraftModel的可提交canvas；原三节点decoder/后端白名单不放宽。
4. 不只分流change：normalize、changeName、拖动、删除、连线、撤销/重做、复制与原生文档副作用都必须界定到设计状态。放弃设计恢复原草稿及其未保存状态，不修改已保存图、旧结束引用、内部版本或历史。
5. 设计状态中不发保存/自动保存/快捷键保存、试运行、内部发布及其他当前草稿写请求。试运行界面保持可点击，仅前端提示暂未接入，不产生模拟运行结果。不得删掉新节点后偷偷提交剩余三节点，不得过滤未知节点却提示“已保存”。说明为“当前仅配置节点界面，暂不支持保存和运行”。
6. 设计图不得被重连bootstrap、远端revision变化、保存服务clean判断或组件订阅覆盖。保留UI图并显示远端已变化的中性提示；设计值不假称已同步。恢复普通模式时沿用真实资源冲突处理。
7. 原操作在途、未知回执、冲突或只读时不进入设计状态；保留原read_operation/read_run和显式重连入口，不能因禁新写入把已有恢复查询禁掉。自然到期沿用只读保护。
8. 同页切换/关开侧栏保留值。离开提供“继续编辑/放弃本次配置并离开”；返回、宿主路由切换与错误页返回走页面离开保护；历史为同页modal，不离开；正常窗口/App关闭不保证保留（用户已选择）。宿主dirty与确认文案的语义必须单独核对，见第4节，不能只在iframe内拦一个按钮。
9. 删除最后一个电商节点或撤销首次添加，不自动恢复可保存/可运行；设计状态可能还含其他位置、名称或引用改动。仅明确“放弃本次设计并恢复原草稿”结束状态；关闭侧栏不结束设计。
10. 引用只保存页面内描述，不转成当前字符串执行引用。删除被引用节点后显示“引用节点已移除”，保留可修正位置，不静默清空/改绑；不实现业务依赖验证。未填、空字符串、空数组和false保持不同状态。
11. 本期不写localStorage、文件或数据库，不创建版本，不承诺刷新/崩溃/重启恢复。正常离开明确说明未保存；不得利用本期替换用户已有内容或扩大数据范围。

本设计状态是UI编辑，不建立执行状态机或另一套工作流产品。若无法在既有原生组件内满足边界，记录事实并重新评审，不放宽后端或网络来完成界面任务。

## 3. 方案取舍

| 选项 | 价值 | 代价/限制 | 本稿结论 |
|---|---|---|---|
| 官方组件+页面内UI设计状态 | 符合添加/卡片/属性交互，新增业务API为0 | 不跨页面持久保存；需保护原草稿、重连和离开 | 推荐候选 |
| 电商节点直接加入可保存图 | 可保存重开 | 当前多层白名单不支持，需要契约/存储/兼容决策，扩出纯UI范围 | 不纳入 |
| 独立截图/静态页面 | 初期容易展示 | 不满足现有画布点击添加与官方面板复用 | 不作为替代 |

PDF未要求持久化，因此推荐仅同页内存保留；这属于本稿假设，已显式呈现其限制，未冒称用户逐项批准。

## 4. Contract First：当前文档与未来UI候选分别判断

**本次实际改动 `contract-impact=none`：只写需求资料，无运行行为改变。**

**第1步未来实现定稿为 `semantic`：已完成直接消费者方向性源码核对，真实运行验证尚未执行；详见10。** 原因是设计配置不可持久保存，而现有Desktop离开确认由跨renderer的dirty_changed驱动；若把“需保护的未保存内容”扩展到该设计状态，其关闭/恢复文案与解释可能改变。不能只看boolean形状没变就预先认定none。

- 后续先核对 `yijie-contracts` 的 editor bridge权威源，以及Desktop现有dirty/关闭/历史/路由消费者。若现有通用语义确已完整包含这种UI状态，提供源定义和消费者证据后可有据调整为none；不得为通过门禁静默调整。
- 若需澄清/改变现有UI通知语义，先更新权威契约说明/适用示例与生成检查，再同步消费者；其范围只限UI离开保护，不新增商品/模型/媒体业务接口。
- 若导致任一受支持消费者的有效交互失效，升级breaking并先处理兼容，不能硬切。当前semantic是保守候选分类，不是已经证明兼容或取得契约批准。
- 新电商节点内容、nodeType、输出定义都不发送至API/存储/执行协议；不改现有三节点持久化与回放格式。文档里的object名称不是新公共DTO。
- 既有画布读入、会话状态、UI关闭通知可沿用；新增浏览/搜索/添加/填写不产生新增业务请求。不能把整个已联网宿主“零请求”当验收口径，也不能以既有桥可用为由发送新图。
- 权限/部署/执行依照Accepted ADR-0019；不新增native command、capability、token、origin、CSP网络许可或认证方式。固定上游Coze源码仅为原生组件参考，不替代易界wire权威。

D0实际确认状态见07/02，当前不产生第2步实施授权；消费者源码核对已在第1步完成，后续仍需同源生成与运行符合性验证。

## 5. 仓库与已有工作区

| 仓库 | 本次动作 | 后续候选 |
|---|---|---|
| yijie | 仅新增FEAT-154包 | 需求与验证 |
| yijie-coze | 只读源码/规则/状态 | 目录、UI注册、卡片、表单、renderer设计状态及同源构建清单 |
| yijie-desktop | 只读规则/来源 | 复用原入口；核对离开确认/dirty消费者，必要的UI语义适配 |
| yijie-contracts | 记录Git状态，未修改 | 核对UI通知权威语义，必要时source-first；不扩业务协议 |
| yijie-api / yijie-infra | 记录Git状态，未修改 | 服务/wire/数据库不变；后续正常产品构建启动沿用旧入口 |
| 其他兄弟仓 | 不修改 | 不做连接器、模型、Runtime、真实节点业务 |

元仓已有FEAT-153的26/27及两组evidence未跟踪，Coze主题CSS已修改；Desktop/Contracts/API/Infra在本次检查时干净。分支、完整HEAD、远端和状态见evidence/workspace-before.json；逐文件保护摘要见protected-files-before.json。保留当前工作树颜色，不从HEAD覆盖。

## 6. Fact / Assumption / Unknown / Conflict

| 类别 | 项目 | 处理 |
|---|---|---|
| Fact | PDF纯UI范围、30个节点来源、官方面板存在 | 写入Must，完整字段可追踪 |
| Fact | 三节点白名单、原生类型唯一、provider订阅与dirty离开机制 | 不仅添加目录；设计态必须保护这些边界 |
| Assumption | 无跨页面/重启持久化要求 | 推荐内存，明确离开限制 |
| Assumption | 五分组、中文字段拆分、统一电商类别便于卖家 | 作为候选，保留原键/类型/名称 |
| Unknown | 原生registry对一个电商类型+30目录的适配量 | 后续核对，不填虚构注册数字/构建结论 |
| Unknown | dirty_changed是否完整包含不可保存UI配置 | 保守semantic；后续权威源与消费者核对，不能假定none |
| Unknown | 部分object内层key/枚举/必填/默认不完整 | 仅明示项；无定义保留未选择/引用，不补业务规则 |
| Conflict | 添加30节点与现有可保存图限制 | 页面内设计态，不放宽后端 |
| Conflict | 原文有算法/平台写入/门禁，PDF要求忽略 | PDF范围优先，仅字段展示 |
| Conflict | 截图紫色及模型示例与当前主题不同 | 结构参考，颜色取当前用户主题 |

## 7. 验证、生命周期与回滚

本次仅文档包结构、来源/字段覆盖/链接、元仓正常lint/test/Shell语法及diff/status。未控制正在运行的App/栈，未生成/替换业务binary；UI构建、真实产品运行、业务、模型/平台调用均NOT RUN。

后续以同一canonical Desktop入口验证30节点真实UI；用普通表单错误、空态、取消检查恢复，核对新增操作无业务请求、新图不进入保存/运行、原草稿与主题保持。源码/定向测试覆盖引用失效、重连不覆盖、离开保护、移除最后节点不恢复执行；不以静态截图代替真实交互。

永久跳过强杀/崩溃注入、权限破坏、binary替换/伪装、恶意资源/危险归档/攻击fixture。原因：用户长期硬性安全条款；影响：不声称这些场景或全仓通过，不影响本次文档检查。

没有新数据migration。未来撤回UI仅在正常退出并保留用户修改后处理本需求的可复现产物/源码；不改旧工作流/历史/数据卷。若不能正常退出，停止并报告，不强杀。本次不实施回滚、重启、提交、推送或发布。
