# FEAT-154 第2步：共用骨架与三个样板

当前恢复与实际验收结果见[13](13-recovery-and-sample-verification.md)；本文保留首次代码实施及当时环境阻塞的历史依据。

## 首次实施结论（历史）

用户明确要求“第二步方案是什么？输出后，开始执行”，已在D0确认基础上实施。

**共用骨架及01/10/17三个样板代码已落地，离线检查通过；第2步尚未完成实际 App 验证。** 本地栈存在此前的非零退出记录，正常停止门禁未通过，未更新可服务的 dist、登记新制品或启动产品。全部30节点的Must和D4保持待验收。

## 执行方案与代码结果

| 工作 | 本轮结果 |
|---|---|
| 源契约先行 | 既有dirty通知明确涵盖不可保存的页面设计；1.4.0-local-candidate，形状/事件/字段不变；canonical生成后同步API、Coze、Desktop |
| 目录与原生组件 | 私有类型`yijie-ecommerce-ui`；独立`ecommerce-01/10/17`目录；原NodePanel分组/搜索，点击和拖入共用实例工厂；原生卡片/侧栏、纯装饰端口 |
| 三个样板 | 01商品采集13项、10 Listing一键优化26项、17商品图片生成18项；合计57个顶层字段逐行追踪原Markdown |
| 字段状态 | 中文分组/帮助、只读输出定义、引用占位、列表独立row ID、建议初值深复制；未配置与false/0/空字符串/空列表区分；无依据的内层字段只存私有UI slot |
| 草稿隔离 | 首添加前同步切换页面保护状态；`EcommerceUiDraftModel`只在内存保存新图；原`DraftModel`及1/15/2解码器不接收新节点；删除最后节点不退出设计 |
| 恢复/重连 | 明确确认恢复进入设计前原草稿及其未保存内容；当前epoch的原生读取与规范化成功才提交切换；服务端冲突保留到明确放弃并读最新；重连保留配置 |
| 提交保护 | 保存/试运行/发布按钮和实际action同时保护；原生图加载期间也禁止提交；页面内离开提示，历史modal保留，已有版本显式执行能力保留 |

主文件位于：

- Coze：`frontend/apps/workflow-local/src/main.tsx`、`ecommerce-ui-draft-model.ts`。
- Coze：`frontend/packages/workflow/playground/src/local-ecommerce/`及既有NodePanel、原生注册/格式化、`local-workflow-document.ts`、`workflow-save-service.ts`、header与进程内adapter。
- Coze：`base/src/types/local-editor-node-type.ts`及相关编辑器类型；没有扩展StandardNodeType数字枚举、后端IDL或可执行图白名单。
- Desktop：`WorkflowLocalWorkspace.vue`离开说明及聚焦测试；其余改动为同源派生消费内容。
- Contracts：bridge源说明、候选版本、迁移说明、正常conformance及派生物；API仅同步派生契约和来源锁。

当前源锁登记77个上游覆盖文件，其中本轮新增登记15个。既有主题CSS及另外14个受保护文件摘要不变；全部六仓分支/HEAD不变，没有提交推送。

## 交互与实现细节

1. 添加样板前捕获原生文档和原草稿状态，同步发布mode/dirty与提交守卫，再创建独立实例；同一事件内连续添加也不会重复进入模式或清除第一项添加的撤销历史。
2. 输入和移动只修改设计内存；切节点、折叠侧栏与查看历史保留值。清除字段保留触达提示，实际值回到unset。
3. 恢复原稿先确认，再冻结原生编辑并发起有epoch的替换；替换失败保留原稿/设计并允许重试或离开。原稿进入前未保存的名称/内容可恢复，旧撤销栈不恢复。
4. 自动远端更新采用串行读取队列；新版本在旧版本原生加载期间到达时继续消费最新快照。加载状态同步到App，避免画布与模型不一致期间发生提交。
5. 关闭窗口/退出App不保证保留，沿用用户已明确选择的纯前端边界；未新增native退出消息、权限或持久化。

**一项等效实现调整：**设计稿写stop/clear/start；实际固定Flowgram只公开start/stop/clear，没有读取启停状态的公共API。实现使用公开`history.clear()`，在首创建前或只读替换前后清理；这样保持原有禁用配置，避免调用start意外启用历史。不访问私有锁状态。

## 验证结果

| 验证 | 结果与范围 |
|---|---|
| Contracts专用生成与确定性检查 | PASS；三消费者锁检查PASS；没有手改生成物或伪造source_commit |
| Contracts聚焦测试/lint | 16项PASS；lint通过，12条既有unused-component警告 |
| Desktop聚焦测试/lint | 23项PASS；eslint与vue-tsc通过 |
| Coze聚焦测试 | 47项PASS：真实私有状态模型、源字段、空值与列表、原生创建集成的明确内存testdouble，以及原三节点模型/来源投影；不是App资格 |
| 固定编译器检查 | canonical prepare后运行`workflow-editor-typecheck.mjs`：126条诊断全部为固定上游原有诊断，新增0条，`PASS_WITH_REPORTED_UPSTREAM_BASELINE` |
| Coze治理/源保持 | make lint/test PASS；15222个源文件保持、6个既有删除保留、77个已登记覆盖；不是全量应用lint |
| 元仓 | pnpm lint、50项test、Shell语法PASS |
| 最终diff/保护 | 六仓diff空白检查PASS；15个保护文件摘要相同，分支/HEAD不变 |
| dist构建、登记、真实Desktop与D4 | NOT RUN，受下节环境阻塞；不使用旧截图或D0示意冒充新产品验收 |

本次1.4相对当前Contracts HEAD的结构检查通过。历史32dd基线仍检出1.3已有的`request_history`分支变化，其余登记的三条历史基线通过；不得称全部基线兼容，也不得将旧Desktop与新Coze混用。

证据：[实现检查与来源摘要](evidence/step2-implementation/implementation-checks.json)、[契约与消费者](evidence/step2-implementation/contract-source-consumer-checks.json)、[47项测试原始输出](evidence/delivery-package/command-output/step2-implementation/coze-focused-tests.txt)、[编译器结论](evidence/step2-implementation/coze-typecheck-summary.json)。

## 实际环境阻塞与下一步

正常打开原厂Docker后，canonical `make workflow-status`确认所有工作流容器已经退出；Coze和MySQL两项保留`ExitCode=137`，结束时间为2026-09-14 18:38:30 UTC，早于本轮修改。没有将该历史状态归因为本轮，也不能称它们正常退出。

本轮仅尝试一次`make workflow-stop`，返回2：`Containers retained; inspect nonzero exit or OOM before claiming normal stop`。没有运行中的目标被停止。现有controller的stop/editor/up都要求原容器正常退出，文档明确没有异常退出恢复入口；重复执行stop/init无法消除这个事实。

依照用户长期安全条款及Coze“先正常停止再更新产物”的规则，本轮停止激活。没有裸docker start/rm、清理volume、改状态/退出码、替换binary或使用强杀。canonical prepare仅同步被工具明确拥有的隔离源码副本，类型检查未写可服务的dist。

下一步需要先明确受控恢复路径：保留原异常容器身份、镜像、挂载和退出事实；为现有数据集提供可审查的canonical恢复流程，正常启动旧依赖并核验健康、正常退出后，再登记和激活新候选。该恢复能力超出现有controller支持范围，本轮未实现或绕过。具体入口和阻塞证据见[构建入口核对](evidence/step2-implementation/contract-build-launch-review.md)、[环境事实](evidence/step2-implementation/activation-blocker.json)。恢复后再完成三个样板的实际添加、独立编辑、切换保留、撤销/删除、取消离开、恢复原稿与旧三节点回归，满足这些条件后才标第2步完成。

强杀、权限故障、攻击fixture、危险归档与二进制伪装测试永久未执行；本轮无业务/模型/平台/媒体调用，无生产或公网操作。
