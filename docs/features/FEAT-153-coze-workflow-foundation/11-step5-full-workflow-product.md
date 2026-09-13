# 第5步：完整工作流页面与主题、尺寸

2026-09-12。用户在最小 dev/packaged 资格通过后明确要求“完善首次自动适应画布；完整产品页面、全主题/尺寸验证”。沿用 D0、ADR-0019 与既有本地合成文本范围，进入 5.4；本页持续记录本轮事实，尚未取得的真实验证不继承历史 PASS。

## 实施决定

整体 contract-impact=semantic，沿用 FEAT-153 源契约。首次 fit 子项仅在本地视图中调整缩放/滚动，持久坐标不变。完整页面消费已有 save/test/publish/run/query 协议，不增加 native command、身份、网络目标或数据库结构。源锁维持已登记本地候选，不能称为发布来源。

页面保留真实列表/创建；进入编辑时收起方案示意与分类，突出画布。编辑器提供保存、以已保存 revision 试运行、引用同 revision 成功试运行内部发布。Desktop 提供明确版本输入与执行、原操作查询、真实历史分页和完整输入/输出/节点结果。没有版本列表端点时不编造版本元数据；所选版本由服务端校验。

未知写结果保留 operation ID，先查回执和原运行，不自动重发；completed 回执不等于引擎成功。未保存修改、待确认结果与在途写操作继续承接离开提示及显式重连。只使用开始、文本拼接、结束；无 ERP、模型、商家、平台或付费调用。

首次 fit 等待图层、容器与节点真实测量，且只执行一次；用户编辑后不强制重新布局。主题沿用 App 实际系统主题及 CSS color-scheme 的 iframe 继承，先验证现有机制，不预设需要新主题协议。

## 验证计划与状态

- 源与已存在工作区基线：[workspace-before.json](evidence/step5-full-product/workspace-before.json)。
- 聚焦正常状态测试、来源检查、前端/编辑器 canonical 构建：PASS，详见下方证据。
- 真实 dev/packaged 创建、编辑、保存、试运行、内部发布、指定版本执行、结果与历史：待执行。
- light/dark、1180×760/1440×900、键盘焦点及主题切换保留草稿：待执行。
- 真实 API/两库与新增 App 结果对应：待执行。旧 packaged 资源在受控栈恢复后的只读 API 完整读回一致；本轮无新资源/试运行/发布写入。公开产物凭据检查和正常停止已完成，范围见下方。

不强杀、不故障注入、不改权限或运行时、不使用攻击 fixture；开发构建仅由项目标准入口生成。禁止历史测试另记未执行，不冒称全仓绿。没有 commit/push/tag 或对外发布。

## 已执行的检查与独立审查

[完整检查摘要](evidence/step5-full-product/implementation-checks.json)记录实际命令、数量和构建来源：

- Desktop lint、26 项定向测试、标准 unsigned 开发包、docs build：PASS；[测试日志](evidence/step5-full-product/desktop-tests.txt)。
- Coze canonical tsc/rsbuild/check 与21项正常编辑器测试：PASS；[测试日志](evidence/step5-full-product/coze-editor-tests.txt)。其中6项首次测量生命周期、4项发布证明/未知结果保护；不等价于 WebKit 视觉资格。
- 未修改的 native 工作流边界13项定向测试：PASS。不重跑含禁止 fixture 的全仓测试，原 Chat tests-target clippy 限制及 Vite 旧大包软警告保留。
- [独立接口审计](evidence/step5-full-product-api-audit.md)确认现有 source 足够；无版本列表、无运行取消、无新主题消息。
- [独立 UI 时序审查](evidence/step5-full-product-ui-review.md)发现无ID未知执行导致页面困住，以及加载中历史丢失新刷新；已修复，并用正常延迟 Promise 和实际组件的离开确认案例验证。测试替身不证明真实焦点或窗口布局。

[首次适应独立源码复核](evidence/step5-initial-fit-readonly-review.md)未发现普通首屏生命周期阻断；这不替代真实WebKit视觉验证。编辑器首次适应等待真实图层、非零容器与节点的 DOM/引擎尺寸一致后执行一次；完成、用户操作、重新载入或卸载均清理监听和 RAF。不会把图层挂载直接当作测量完成，不改持久位置。后续手动适应仍保留。

试运行只操作已保存 revision。发布要求当前 revision 的 debug + succeeded + terminal 证明；保存使旧证明失效。运行详情保持 state/terminal 分开，节点显示原生 state；未知值不猜成功。非终态保留运行编号与明确更新入口。发布后当前所选旧版本不被自动换成新版本。

需求包 strict/声明检查、元仓 lint 与50项治理测试均通过；仅证明文档与仓库治理，不提升 D4 状态。

## 实际环境与数据保护

原厂 Docker Desktop 正常启动，通过 Infra editor→build→up 登记并构建本次来源、完成两次正常 migration 和六服务/宿主认证 ready。
本次 epoch 为 `864454a9-2674-4614-8bcf-cde02de4d278`，editor manifest 为 `0b704a085096ab82827e96f60b715eda94ecb911481c79a46a93e7cdc365eb87`。
[受控来源与公开产物记录](evidence/step5-full-product/stack-build-and-public-scan.json)保留实际值。

在可信检查进程内扫描整个 canonical App bundle、Desktop dist 和 editor dist 的91个普通文件，当前 K_NA/K_AC 匹配均为0、无超限跳过；没有把秘密送入页面，没有完整 heap/MessagePort dump。固定 `/editor/` 返回200并与构建 entry逐字节相等，CSP仍为 connect-src none及限定父origin。

先前由真实 packaged 创建的 `7684605114128007168` 在新 epoch 下名称、revision、画布、前缀、三节点位置和两条边完整相等；[只读结果](evidence/step5-full-product/prior-packaged-reopen-readonly.json)。这只证明旧资源正常恢复，不是本轮新增 App 全流程验收。

本轮未启动 Desktop App，没有创建或修改工作流/版本/执行记录；服务随后经 canonical stop全部正常退出，8个自有容器exit0/noOOM，四卷保留，1420/18081/18888释放，确认无其它运行容器后原厂Docker正常stop退出0。[清理证据](evidence/step5-full-product/normal-cleanup.json)。

[工作区复核](evidence/step5-full-product/workspace-final.json)：12仓HEAD/branch/origin保持；源契约及全部consumer哈希不变，原生runtime本轮不变；七份原设计逐字保留，WorkflowPage按本轮授权仅增量接入并在编辑时收起示意区域；六份Coze旧缺失保留。未提交、推送、tag或发布。

## 真实验收阻塞与下一次顺序

CUA两次报告 Mac 当前锁定，已异步请求用户手动解锁，尚未收到本轮解锁回复。此前录屏授权仍有效，此处是屏幕锁定，未重复索取权限或绕过锁屏。[阻塞与旧资源对应记录](evidence/step5-full-product/ui-blocker-and-retention.json)。

| 主题 / 实际窗口 | dev完整页 | packaged完整页 |
|---|---|---|
| light / 1180×760 | NOT RUN，锁屏 | NOT RUN，锁屏 |
| light / 1440×900 | NOT RUN，锁屏 | NOT RUN，锁屏 |
| dark / 1180×760 | NOT RUN，锁屏 | NOT RUN，锁屏 |
| dark / 1440×900 | NOT RUN，锁屏 | NOT RUN，锁屏 |

解锁后按 canonical恢复栈 → dev新建并验证自动适应 → 正常未完成图试运行提示/修正保存 → 试运行发布v1 → 修改保存并试运行发布v2 → 明确执行v1且输出保持旧前缀 → 结果/节点/历史 → 两主题两尺寸/焦点 → packaged重复核心流程 → 正常停止重开读回执行。

CUA仅支持可识别的应用；前轮裸dev进程没有bundle ID的限制仍需在实际入口核对，不能用旧Swift/AX辅助程序、第二个App、API写入或旧截图替代本轮UI。首次auto-fit实际效果、完整产品页、主题/尺寸/可访问性及统一fresh D4仍NOT RUN；5.4是源码已实现待真实资格，不能写成需求已验收完成。


## 2026-09-13 后续真实 App 验收

本页之前的锁屏、待执行记录为当时时点事实。后续packaged完整流程、精确两尺寸×亮暗组合、普通错误修正、草稿到期保留、两库与正常重开已实测；暗色背景和取消导航标题缺陷修复见[12](12-full-app-theme-size-qualification.md)。当前dev完整页UI仍受CUA识别限制，D4仍NOT RUN，不以packaged代替dev或全页axe资格。
