# 创建工作流确认弹窗

2026-09-13，FEAT-153 的本地产品交互补充；原始 D4 和第 19 份页面验证保留为各自版本的证据，本次验证单独记录。

用户要求点击“创建工作流”后先展示参考图中的名称、描述表单，确认成功再进入独立工作流页面。用户明确选择继续支持中文名称。采用易界主题、品牌按钮和字段错误样式；新建表单名称 1–30 字、描述 1–600 字，均去除首尾空白，服务既有 1–80 字名称兼容窗口保留。描述用于介绍用途，不会调用模型。

## 源契约与兼容设计

`contract-impact = additive`：新增可选创建描述及显式协商的响应元数据；原有名称、会话、鉴权、操作回执、保存和发布语义保留。权威源是 Contracts `openapi/workflow-local/workflow-local.yaml`，候选版本 `1.1.0-local-candidate`。Owner/产品决策人为段成威；producer 为 Coze、API 和 Desktop native，consumers 为 API、Desktop native/Vue 和 Coze 独立编辑器。用户本次请求授权该本地实现，不冒充额外独立审查、tag 或生产批准。

- `description` 为可选字符串，最大 600 个 Unicode 码点；旧创建请求省略时存为空，旧资源无描述正常读取。
- 新 HTTP caller 使用 `X-Yijie-Workflow-Metadata: description-v1`；API 和 Coze 在未协商时必须省略响应描述，避免旧端严格 schema 拒绝未知字段。新端接受缺失描述。该 header 不承载身份或凭据。
- 描述写入 Coze 已有 `workflow_meta.description`，无需数据库 migration。保存草稿只修改既有名称/画布字段，保留描述。旧请求的幂等 hash 字节必须保持，新增描述参与新请求 hash。
- 生成物由 canonical generator/sync 产生。显式 `--local-candidate` 允许本地源候选同步，移除过期不可变 pin；`--check` 仍核对全部摘要，不能用该候选作为发布来源。
- 未发布工作流契约的 fallback 为 Contracts `32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4`。兼容窗口保留无元数据协商的旧请求和响应，不弃用旧入口；先更新 provider，再更新 caller/原生编辑器配套 bundle。合并/交付前必须先形成 Contracts 不可变提交并逐仓 pin，当前不执行 Git 提交或推送。
- 回滚先退回 Desktop，再退回 API/Coze；数据库描述列保留，不删除新资源。原 Chat/Runtime、public 契约锁与生产配置不在本次变更内。

## 交互与验收目标

1. 点击创建只打开弹窗，取消、关闭、Escape 不产生创建请求。
2. 名称与描述必填，中文可用，显示计数和字段错误；有效后才可确认。请求中禁用重复提交和关闭；结果未知时保留表单并查询原回执，不能重新创建。
3. 服务确认创建 ID 后跳转独立编辑页；编辑会话由目标页打开一次。直接访问 `/workflows/new` 也只展示表单。
4. 保存、返回列表，新流程位于首位并显示真实名称和描述；重开、正常重启读回保留。
5. 验证旧请求/响应、幂等字节、生成物、消费者符合性，以及真实 App 的亮暗主题和 1180×760 最小窗口。

工作区初始状态、验证输出与截图保存在 `evidence/create-dialog-20260913/`。当前状态：本次本地追加交互已实现并完成真实 packaged 验收；范围和证据如下。


## 实际验证结果

- Contracts：canonical workflow generate/check、12 项正常契约/浏览器检查、全仓 lint，以及相对上述 fallback 的 OpenAPI/Proto/AsyncAPI/JSON Schema breaking 检查通过。结构检查之外，`validate-observation.mjs` 使用 fallback 与当前两份真实 schema 分别验证实际 API 响应，旧严格 reader 能读取无描述投影。
- API：workflow lint 和限定 `-race` 测试通过。新增检查覆盖请求描述往返、旧操作意图 JSON 字节保持、响应显式协商与既有会话边界。
- Coze：workflow lint、四个限定包的正常测试通过；描述持久化、旧式保存保留描述、旧 80 字名称、操作幂等/冲突及 HTTP 描述协商均验证。canonical 编辑器重新构建、摘要检查与受控注册通过。
- Desktop：最终 9 个文件共 59 项检查通过，包含真实组件组成的弹窗、必填/超长修正、确认前不跳转、重复提交拦截、结果未知时查询原回执、旧路由/侧栏及 axe。lint/typecheck、文档站与 canonical packaged 构建通过；13 项限定 Rust 工作流测试、`cargo clippy --lib -- -D warnings`、`cargo fmt --check` 通过。
- 真实取消检查：从概览打开表单，填写有效内容后取消；另测 Escape、关闭 X。创建数仍为 14。原生 macOS 鼠标点击不会自然聚焦按钮，已在打开前显式设置返回焦点，并实测 Escape → 焦点回创建按钮 → Return 再开 → 名称聚焦。
- 主闭环：真实 App PID 38552 创建 `7684953519702409216`（FEAT-153 中文创建确认验收），确认后进入 Coze 页面。增加文本处理节点和两条连线，前缀为“创建确认：”，保存 revision `7684953618658623488`。返回后首卡显示真实名称与 38 字描述，点击重开读回三节点、两连线和前缀。两次 native `remote_close_confirmed=true`，Chat 普通入口可用，未发送 Chat 请求。
- 正常重启：App 正常退出、受控 workflow-stop/up 保留卷。新 App PID 41665 从卡片重开成功；`restart-read-api.json` 与保存时的 name/description/revision/canvas 完全一致。
- 视觉：02/03 为亮色 1180×760 / 1440×850，04/05 为暗色相同尺寸的填写表单；06 为暗色最小编辑器，07 为亮色四卡列表，08 为重启后的亮色最小编辑器。所有图片为原始窗口截图；系统外观已恢复浅色。01 是较早候选的字段失焦提示，仅作过程记录，不作为最终空表单证据。
- 最终长描述收口：卡片改为三行预览，完整描述保留在数据、可访问文本和链接 title。最终 App PID 44455 通过表单确认创建 `7684955647779012608`（FEAT-153 长描述确认验收）；600 字全部存储，返回后首卡三行省略，09 截图实际尺寸 1440×850。该阶段仅调整共用卡片摘要样式，弹窗四组截图所对应的弹窗与创建逻辑未再变化。普通 AX 调整尺寸曾返回动画中间值，严格尺寸检查拒绝记录；等待正常布局完成后重新捕获并记录真实尺寸，没有修改图片。

## 交付边界

本轮真实 UI 验证为 canonical packaged；没有将旧 dev、完整试运行/发布/版本执行或自然 300 秒到期验收冒充为本轮重新执行。那些历史资格仍以 17/19 各自候选为准。新描述在旧式保存中保留的 API/Coze/native conformance 已覆盖。全仓历史攻击/故障 fixture 与生产/public 验收未运行；只执行正常、非破坏性的限定开发检查，未调用模型、电商平台、付费服务，未强杀、破坏权限或删除数据。

运行时代码变更为 Contracts → API/Coze/Desktop，Infra 只通过受控入口重新构建/启动，无源码变更。原有未提交设计修改和 Coze 六份既有缺失文档保留。当前 App 在工作流概览，服务 ready；两个新增资源均为具名合成验收数据。最终文件摘要见 `candidate-files.json`，可复核过程日志、响应观察和窗口尺寸 JSON 同目录保留。未执行 Git add/commit/push，也未创建 tag 或声明 CI/生产发布；后续提交时先提交 Contracts 再用不可变 SHA 重新同步三消费者，最后提交元仓交付记录。
