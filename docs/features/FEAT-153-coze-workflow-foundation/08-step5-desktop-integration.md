# FEAT-153 第5步：真实Desktop载体与产品接入

日期：2026-09-12。用户明确要求依序执行环境核对、最小真实编辑器闭环、会话与dev/packaged资格、资格后完整产品页。目标为同一个canonical App稳定完成创建→编辑→保存→返回→重开，并保持身份/会话及原Chat边界。本步整体contract-impact=semantic，D0沿用已批准05设计，D4留第6步；不新增ERP/模型/平台调用或提交/发布授权。

最新状态：[11](11-step5-full-workflow-product.md)已实现首次自动fit及5.4完整产品页面；本轮Mac锁屏，新增App/主题尺寸验证待执行、D4 NOT RUN。下方10与早期记录保留原时点。

此前补充：用户恢复解锁后，dev/packaged 最小真实编辑闭环、完整草稿自然到期重连、native 关闭确认及 Chat 切换已实测，见[10](10-step5-real-app-qualification.md)。5.2/5.3 最小资格通过，5.4 未开始、D4 NOT RUN；App/栈/Docker 已正常停止。此前用户外出时的无界面补齐见[09](09-step5-headless-progress.md)，下方运行来源和早期阻塞按历史时点保留。

## 执行顺序

| 阶段 | 退出条件 | 状态 |
|---|---|---|
| 5.1 环境核对 | 原厂Docker正常启动、旧助手影响核对、精确受控栈和宿主认证ready，无新默认凭据助手链 | 完成；step5-workspace-before.json、step5-environment-restored.json |
| 5.2 最小编辑器 | 真实Coze画布在同main App加载；native零登录读取/保存/返回/重开，机密不进入renderer | 通过；dev/packaged 两个实际App资源、UI与API/两库读回见10；隔离检查范围明确记录 |
| 5.3 载体与会话 | dev和packaged实际握手/CSP/正常到期保留草稿/显式重连/关闭撤销，正常退出 | 最小资格通过；真实完整草稿到期、重连保存、两入口native关闭确认/Chat切换及正常退出见10；完整主题/视觉AC留后续 |
| 5.4 完整产品页 | 在前项通过后连接真实列表、试运行、内部发布、指定版本执行、结果及历史 | 源码已实现，真实App全流程与主题/尺寸待解锁；见11 |

## 本轮事实与技术决定

- 本轮真实启动发现并修复 Chat 边界冲突：FEAT-153 曾扩展 Contracts 的全局 `scripts/generate.mjs` 与 `package.json`，使 FEAT-132 已提交来源校验拒绝启动。现仅撤回本需求对这两个文件的新增，恢复与原提交逐字节一致；工作流走独立 `make workflow-generate/workflow-check/workflow-test` 和 leaf generator。原 native committed check 完整保留并通过；工作流源输出漂移检查与11项测试通过，源/consumer锁未变。没有新增commit或把本地候选冒充已提交来源。
- Coze canonical tsc/rsbuild/check 最终通过，6项静态资产，manifest SHA `dc5c1f979d4475ff4210d74c3312910ce6384888522b48de9c110c325e740b48`。按受控入口登记→精确API/API-test/Coze镜像构建→两库migration→六服务与宿主认证ready，epoch `8f00e418-a7e5-47a5-a945-f60c9285c9e5`。6项无凭据GET返回200且逐字节符合manifest；CSP仍无unsafe-eval且connect-src none。
- `pnpm lint` 与 `pnpm build` 通过；当前源码的 WorkflowPage/新增workspace共12项测试通过。首次手工聚焦vitest漏带canonical的`.local`排除，误匹配历史构建副本，产生8项旧副本Vue双实例失败；补齐标准排除后仅2个当前测试文件12/12通过。此失败不隐藏，也不修改历史副本或降低断言。
- 正常 `pnpm tauri:dev` 已完成所有原native/MCP/v4/retirement来源检查、技能资源同步和Rust构建，真实主App及其Host/Codex已启动。CUA首次打开真实App时返回Mac锁屏、无法自动解锁；已要求用户手动解锁。未尝试绕过锁屏，未进行编辑器UI操作，5.2实际闭环/5.3/5.4均未通过。
- 旧默认凭据助手由最初5个变为4个原PID仍等待，未新增助手；未重复信号或强杀。当前栈与dev App保留供解锁后的正常资格使用，尚未声称退出清理完成。

- 第4步的精确镜像/四个数据卷恢复，正常ready成立；早期5个凭据助手和其CLI父进程仍等待，没有新的助手进程。独立匿名Docker配置与缓存固定镜像不依赖这些旧登录请求；不反复发信号、不强杀、不改Keychain。
- Desktop原生8个workflow command和300秒E已在第3/4步实现；shared DTO仍由Contracts生成。MessageChannel现有connect/ready/request/response/dirty_changed/request_close及bridge/generation/request ID可承接本轮，不发明第二套DTO。
- 浏览器CSP不允许运行时eval编译schema。新增canonical AOT browser校验产物与桥TS消费，生成期使用已锁Ajv，产物不依赖Buffer/require/eval/new Function；UTF8字节限制继续按TextEncoder，不能降为UTF16长度。
- Coze完整WorkflowPlayground会读取空间并直接调用公共API，不适合connect-src none。专用local editor复用同仓@coze-workflow/render的真实WorkflowRenderProvider、PlaygroundReactRenderer、WorkflowPortRender与受限document/renderer贡献，只注册开始/文本concat/结束；不挂全Studio模型/插件/运行/保存store。节点属性输入属于真实画布，不用普通表单替代编辑器。
- API在/v1原身份gate之外增加精确/editor/静态asset handler；只服务有界manifest列出的公共构建资源，启动校验源/文件hash并读入内存，不开放任意FS/代理/SPA fallback。CSP仅允许本地asset，frame-ancestors只接受既定dev/packaged父origin；实际WK验证前不写PASS。
- canonical Desktop旧Chat sidecar有image-enabled路径的有限等待→强杀/drop回退。本轮exact local+demo_fast+workflow启用路径关闭该回退，正常停止只等待/报告PENDING；Host本身已核对正常Shutdown/CloseInput等待，无需改Host/固定Codex二进制。
- 同一main窗口通过现有config构建并挂有限导航/新窗口边界；保留原Chat artifact preview/video路径及既有capability，不把editor origin加入remote native capability。K_NA文件路径仅交给native运行进程，不进入VITE或Host/Codex环境。

## 页面结构与状态计划

现有“工作流”页保留标题层级、自然换行能力分类、工具条、自适应网格、中性标签和青柠执行主按钮。用户8份既有改动已保存第5步前哈希；本轮按新授权增量修改WorkflowPage并增加真实区域，不覆盖用户设计，不将此前字节保护误读为永久禁止产品接入。其它原卡片/样式优先保持。

最低阶段仅增加真实连接状态、创建/真实资源列表和同页编辑器承载；原ERP推荐保留明确示意语义。编辑器保留返回、保存、工作流名称、真实画布和节点属性。loading/empty/error/unauthorized/expired分别表达，写操作没有provider确认不显示成功；未知写结果用原operation查询，不能自动重发。

父容器先native open，加载固定/editor/后按精确contentWindow/origin传MessagePort；校验source envelope与内外ID一致，每个generation绑定一个资源。E到期父UI保留iframe且覆盖交互/移焦点/禁派发；不广播无关联response，不重新加载画布。显式重连取得新binding/port，同一iframe保留dirty名称/canvas/base revision，若远端revision改变显示冲突，不能偷偷换base覆盖。返回遇未保存内容有明确保留或放弃，关闭调用native revoke；迟到open也需正常close。

完整运行/发布/结果动作在5.3通过后实现，不将最小壳或browser-only结果算产品资格。

## 验证与保留

只用普通输入、真实服务、正常到期和正常退出；不改时钟/TTL伪造过期，不注入攻击/故障fixture，不强杀或篡改执行程序。验证期间可做正常定向单元检查，但真实资格必须来自同一App的dev与packaged入口。包使用canonical可复现unsigned开发构建，不覆盖用户签名/已发布二进制。源码、锁、快照和真实结果分别记录；测试/视觉/身份/secret/退出未知项在完成后更新，不能继承第4步或历史D4。


## 2026-09-13 后续真实 App 验收

本页之前的锁屏、待执行记录为当时时点事实。后续packaged完整流程、精确两尺寸×亮暗组合、普通错误修正、草稿到期保留、两库与正常重开已实测；暗色背景和取消导航标题缺陷修复见[12](12-full-app-theme-size-qualification.md)。当前dev完整页UI仍受CUA识别限制，D4仍NOT RUN，不以packaged代替dev或全页axe资格。
