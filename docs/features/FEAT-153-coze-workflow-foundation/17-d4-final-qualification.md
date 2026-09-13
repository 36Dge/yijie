# FEAT-153 统一 D4 最终验收

2026-09-13。当前本地候选的真实验收通过，FEAT-153 按 `demo_fast + local` 收口。资格编号 `ea50e666-898c-4107-9568-10e3e3d63416`。本结论不包含提交、推送、公网或生产发布。最终机器门禁结果见同目录证据中的 `final-governance-checks.json`。

## 候选与本轮修复

用户授权 AX/CGEvent 后，先补齐了旧候选真实 dev A/B。随后发现画布缺少键盘移动和连线入口，在正常退出 App、停止栈后修复，并重新冻结候选、创建两个新流程完成以下验收。此前人工 A 的未匹配记录及旧候选结果保留为历史，不替代本轮证据。

仅修改 Coze 本地编辑器 `native-canvas.tsx`、`main.tsx`、`style.css`：标题可用方向键移动，Shift 加速；具名按钮可连接/断开下一合法节点，支持 Enter/Space；保留鼠标拖动/端口，补上可见焦点和字段错误关联。本修复子项 `contract-impact=none`，使用原 WorkflowDocument、canvas 格式及保存路径，不改变身份、会话、wire、版本或持久化语义；整体需求仍 semantic。

最终 Coze 候选 `4d1bf84f7e5ba31fba1516dc1ee0c45697e4c1dadc26c3c16f5c94b573a6f003`；编辑器 manifest `2120725211a538abeb5ca1efbb1c192f6a2e0368dbee031c06935e021744f989`。其余四候选、源契约/消费者锁、十二仓 HEAD/branch/origin 及受保护设计文件保持。见[冻结记录](evidence/step6-d4-keyboard-20260913-1153/candidate-freeze.json)和[最终复核](evidence/step6-d4-keyboard-20260913-1153/final-normal-cleanup-and-candidate.json)。

## 两个真实资源

| 入口 | 流程 ID | 最终 revision | 内部版本 / 成功运行 |
| --- | --- | --- | --- |
| 标准 dev，PID11566，localhost:1420 | 7684864630077784064 | 7684866728114782208 | 2 / 3 |
| 标准 packaged，PID12569，tauri://localhost | 7684868190886690816 | 7684870673625251840 | 2 / 3 |

两入口均从实际 App 创建，首次完整入画；不完整图正常试运行返回明确错误，修正后完成保存—返回—重开、两次试运行/内部发布及显式旧 v0.0.1 执行。新草稿保存后必须重新成功试运行才能发布。旧版输出分别为 `KEY DEV 一：固定版验收`、`KEY APP 一：固定版验收`，没有被第二版或后续草稿覆盖。

dev 通过 Tab、Enter、Shift+方向键完成连线/移动；文本坐标由 `(420,160)` 变为 `(410,110)` 并读回一致。packaged 通过 Tab、Enter、Space 和方向键完成编排，又通过真实端口拖拽和标题拖动复验鼠标路径。最终文本坐标约 `(447.2683,195.1986)`，其完整精度与两条边、三节点及最终前缀均由 API/MySQL 一致读回。

证据：[dev 主链路](evidence/step6-d4-keyboard-20260913-1153/dev-qualification.json)、[packaged API](evidence/step6-d4-keyboard-20260913-1153/app-api-after-expiry.json)、[packaged 两库](evidence/step6-d4-keyboard-20260913-1153/app-db-restarted.json)、[dev 两库](evidence/step6-d4-keyboard-20260913-1153/dev-db-restarted.json)。每个资源均为 10 条 PG 操作、9 条 MySQL 操作，共享回执一致；各自一条 PG-only 为普通无效草稿的 API 前置拒绝，没有虚构引擎运行。

## Must AC 判定

| AC | 结论 | 实际依据 |
| --- | --- | --- |
| AC-001 来源与工作区 | PASS | 十二仓身份保持；Coze 15,297 文件未变、2 个声明 overlay、6 份原缺失保留；无 Git 发布动作 |
| AC-002 同源契约与旧边界 | PASS | 源及三消费者检查；四个未改变候选的普通定向检查；原 Chat/公开 OIDC/Codex Runtime 源码未改 |
| AC-003 身份和凭据 | PASS | 两入口零登录、固定 synthetic scope；真实两库归属一致；300秒自然到期/重连/关闭；实际公开资源及 AX 凭据扫描 |
| AC-004 同 App 编辑器 | PASS | dev 与 packaged 真实独立 Coze iframe；首次 fit、保存/返回/重开；具名 native/有限 MessageChannel 与 CSP 既有定向验证 |
| AC-005 创建保存重开 | PASS | 新资源从真实 UI 创建、编排、保存并读回；正常并发/CAS 定向资格保留，无 seed/API 补写 |
| AC-006 试运行与内部版本 | PASS | 每入口两版；新 revision 发布禁用直至成功试运行；旧版不可变结果 |
| AC-007 结果与历史 | PASS | 每入口三次真实成功运行；显式终态查询、独立历史刷新、三节点结果；重启后选择旧历史读回 |
| AC-008 普通失败与限制 | PASS | 未完成图错误→正常修正；无模型三节点、冻结规模/合作式预算/并发及未知结果定向检查；关闭未伪称取消执行 |
| AC-009 运行与持久化 | PASS | 正常 App/栈 stop-up；新 epoch 下两个资源的完整 workflow/canvas/history/runs/receipts 相等；真实 App 再读回；服务未 ready 时 Chat 正常启动，恢复后显式重试成功 |
| AC-010 UI 与安全验证 | PASS | 键盘核心编排与鼠标路径；亮暗×1180×760/1440×900；焦点/具名控件/错误；预算0，保留已声明配色与未执行测试边界 |

## 会话、主题与窗口

两入口均让带未保存内容的会话自然到期，没有修改时钟、注入延迟或制造故障。到期后画布仍可见，inert 编辑控件退出 AX 可交互树；显式重连保留草稿，再保存。未保存切 Chat 时可用 Tab/Enter 选择继续编辑，保留内容及工作流标题/路由；随后只放弃本轮临时合成修改，正常进入 Chat。

| 主题 / 精确逻辑尺寸 | 画布 | 结果与历史 |
| --- | --- | --- |
| 亮色 1180×760 | [重开](evidence/step6-d4-keyboard-20260913-1153/app-03-light-min-reopened.png) | [结果](evidence/step6-d4-keyboard-20260913-1153/app-04-light-min-results.png)，三条历史经实际 AX 核对 |
| 暗色 1180×760 | [未保存画布](evidence/step6-d4-keyboard-20260913-1153/app-05-dark-min-dirty.png) | [结果/历史](evidence/step6-d4-keyboard-20260913-1153/app-06-dark-min-results-history.png) |
| 暗色 1440×900 | [保存后画布](evidence/step6-d4-keyboard-20260913-1153/app-10-dark-large-canvas.png) | [结果/历史](evidence/step6-d4-keyboard-20260913-1153/app-11-dark-large-results-history.png) |
| 亮色 1440×900 | [画布](evidence/step6-d4-keyboard-20260913-1153/app-13-light-large-canvas.png) | [结果/历史](evidence/step6-d4-keyboard-20260913-1153/app-12-light-large-results-history.png) |

尺寸按实际 AX/native 几何和原尺寸 PNG 核对，不能把 CUA 缩略图高度768当作窗口尺寸。macOS 在默认显示空间及调整位置生效前曾钳制为1346×849/900，这些中间截图（app-07、08、14）不计目标尺寸通过。临时切到1800×1169、正常定位窗口后才取得1440×900；结束已恢复亮色、1512×982默认显示空间，设置窗口关闭，Dock 未改变。

## 正常重启与清理

重启后 epoch 为 `0cb8e640-7ddc-4870-bdfd-8e1353cbe0e4`。两个资源的 workflow、canvas SHA、history、runs 和 receipts 与重启前逐对象相等，见[相等性检查](evidence/step6-d4-keyboard-20260913-1153/restart-api-equality.json)。真实 packaged PID18073 读回最终草稿、两条连接、v0.0.2及三条历史，并选择旧 v0.0.1 记录读回原输出；还从 packaged 读回 dev 资源，未增加运行。见[实际重启画布](evidence/step6-d4-keyboard-20260913-1153/app-restart-canvas-readback.json)、[旧结果](evidence/step6-d4-keyboard-20260913-1153/app-restart-history-readback.json)、[dev跨入口读回](evidence/step6-d4-keyboard-20260913-1153/dev-resource-in-packaged-restart.json)。

旧 Chat 合成记录仍能打开并读到原 `DEMO_FAST_OK` 回答；未发送消息或启动模型。本轮没有把该旧记录同时展示的“删除尚未完成”提示作为工作流故障修复或执行删除，亦不宣称 Chat 全量功能验收。

各 App 使用 Cmd+Q 正常退出，launcher exit0；重启后两个资源的会话均有 native `remote_closed=true`，见[关闭事件](evidence/step6-d4-keyboard-20260913-1153/app-restart-native-close.json)。最终8容器正常exit0、4数据卷保留，1420/1421/18888释放，工作区 App/Host/Runtime 及凭据助手无残留；确认没有其他运行容器后，原厂 Docker Desktop 正常停止。没有强杀、权限破坏、二进制替换或删除数据卷。

## 验证与明确边界

新增修复通过 canonical tsc/editor 构建、21项普通编辑器/首次fit测试和 source/consumer/manifest 检查。四个未改候选沿用本轮已执行的16项UI/state、13项native、11项Contracts、13项Infra及API普通race/Coze正常检查；真实新图运行进一步覆盖最终组合。不是全仓测试或生产安全认证。

实际 dev 五个 public HTTP 资源、最终49个公开产物、真实 native binary 及多次实际 AX 的 K_NA/K_AC 值匹配均为0。没有把凭据放进页面做测试，也未进行 heap/MessagePort dump；E隔离同时依据 source-first native/server实现和实际自然生命周期。

首次打开中的取消在正常快速响应及一次有界 AX 观察中未命中；按13预先约定，单列“真实点击未执行”，使用普通 UI/native pending-open 时序测试作补充，不冒称真实取消点击通过。该项不通过人为延迟、故障注入或修改安全边界制造窗口。

已有白底青柠1.28:1对比度例外保留；本轮只声明新增控件和核心键盘流程可用，不声明全页 axe/WCAG 认证。运行中缩窗不会承诺每次自动重置视口，可使用“适应画布”。模型、商家、平台与付费调用为0；长任务恢复、生产多租户、具体ERP节点及公网服务不在本期范围。

跨仓交付顺序见[14](14-cross-repository-delivery-order.md)。当前为未提交流水线候选；后续需单独授权 Git 动作，并先形成 Contracts 不可变提交，再按 provider/Infra/Desktop/元仓顺序交付。Coze origin 仍是已登记上游，不向上游推送本地适配。


最终检查：D4 strict/schema语义门禁 PASS，FEAT-153限定声明审计 errors=0/warnings=0，十二仓身份/diff检查、候选与受保护文件复核 PASS。历史检查格式缺项已依真实执行证据修正并保留原记录。机器结果见[最终门禁](evidence/step6-d4-keyboard-20260913-1153/final-governance-checks.json)和[最终判定](evidence/step6-d4-keyboard-20260913-1153/final-d4-verdict.json)。

## 验收后的 Git 交付

用户随后于2026-09-13明确授权提交与推送，实际来源固定、逐仓Git结果与工作区保护见[18](18-git-delivery.md)。上述D4冻结与真实运行证据保持原样，不以提交后的HEAD或manifest覆盖历史记录。
