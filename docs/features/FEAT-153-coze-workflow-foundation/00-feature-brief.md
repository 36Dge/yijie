# FEAT-153 — yijie-coze 仓库接入与工作流基础集成

当前收口结论：2026-09-13 最终本地候选统一 D4 通过，见[最终验收](17-d4-final-qualification.md)。下文保留各阶段的原始事实与当时状态。

> Profile: `demo_fast` · Exposure: `local` · Created: `2026-09-12`

用户要求先认真审计、再分步接入；本需求不实现具体电商服务。第0—4步已完成，具体设计见 [05 本地集成设计](05-local-integration-design.md) 与 Accepted ADR-0019，D0保留PASS。第5.2/5.3步的dev/packaged真实最小编辑资格已完成，见[10](10-step5-real-app-qualification.md)。active表示需求仍在实施；5.4完整产品页和packaged真实全流程/四主题尺寸组合已完成，见[12](12-full-app-theme-size-qualification.md)；当前dev完整页UI受CUA控制限制，第6步统一fresh D4尚未完成。

## 1. 用户问题与结果

- 目标用户：在本机验证易界平台的产品负责人；后续跨境卖家工作流服务以本次基础能力为起点，本期只使用合成通用数据。
- 当前问题：Coze 源码目录没有接入项目仓库治理；易界“工作流”页只有静态展示和本地交互，没有同一个产品入口的真实编排、保存、执行、结果与历史。
- 用户结果：在现有“工作流”页零登录打开真实编辑器，创建“开始→文本拼接→结束”流程，保存并重新打开，试运行成功后内部发布，执行固定版本并查看结果与历史；正常退出/停止后重开仍保留数据。
- In scope：已核实 source provenance、Git 元数据与 12 仓清单；六仓基础接入；独立 React editor；固定 local identity/resource bridge；真实 list/create/read/save/test-run/publish-internal/run/get-run/list-runs；独立本地数据、受控部署、readiness、正常启停、合成 focused checks。
- Out of scope：ERP 服务、真实店铺/用户/商家数据、平台凭据或写入、模型/HTTP/Code/插件/Agent 节点、外部 provider 与付费调用、定时/补偿/持久队列、在途恢复承诺、public/production、完整 Coze Agent/知识库产品、Codex Runtime 改动、既有 Chat 数据迁移、FEAT-137 恢复、远端创建与 commit/push/tag/release。模型、商家 API 和付费调用预算均为 **0**。

## 2. 完整主流程

1. 通过现有 canonical local demo_fast 启动器进入同一个 Desktop 主页面，再进入 `/workflows`。不要求账号、密码、Keycloak 或第二次登录；用户没有选用工作流时，Coze 未就绪不阻断原 Chat 启动。
2. 工作流页读取真实列表。服务未 ready 时明确提示正常启动/重试；空列表提供创建入口。现有静态 ERP 推荐只能作为示意，不能通过绑定通用流程冒充具体服务已经实现。
3. 点击创建，受信 native/server 绑定固定 synthetic owner/tenant 与 Coze user/space/resource，打开同一 App 内独立 React editor。renderer 不选择身份或获得 PAT/session 秘密。
4. 配置有效连线的开始、文本拼接、结束三节点。首期禁止循环和其它节点；按05冻结input 4KiB、prefix 1KiB、output 5KiB、canvas 256KiB、message 512KiB和共用1个在途槽位；30秒为Coze合作式预算而非HTTP超时/强杀。安全但不完整的草稿可以保存，运行/发布才要求完整三节点；服务端已实现，完整运行/发布产品交互留第5.4步。
5. 命名并保存草稿；只有 provider 确认后显示保存成功。返回列表重开同一 ID/revision 和内容。保存带预期 revision，冲突时保留未保存内容并提示重读，不静默覆盖。
6. 试运行草稿并核对文本输出及节点结果；成功后内部发布固定版本，不开放 Force。这里的“内部发布”只是本地 Coze 可执行版本，不是公网发布或 Git tag。
7. 从易界执行选定版本，保存真实 run ID，查询原生状态、输出、节点结果与历史。修改草稿不会回写已发布版本或旧执行结果；状态未知就显示未知，不由前端猜 completed。
8. 普通输入错误可修正重试。创建/内部发布/运行的结果不确定时先查询，禁止无条件自动重发。返回/关闭若取消的是本地等待，不宣称远端执行已经取消；首期不承诺运行中止。
9. 短流程正常完成后，正常退出 Desktop 并停止自己管理的服务，保留数据 volume；以同一个正常入口重开，核对草稿、内部版本、历史及原 Chat 数据。

## 3. 交互与 UI

- 视觉方向：保留用户当前工作流页布局、自然换行分类、无图标底板、灰色热门/推荐标签、青柠执行主按钮与中性演示次按钮。新 editor 有明确返回、保存、试运行、内部发布、固定版本执行入口，不重做整个 Coze 产品。
- 已批准载体与具体传输：同一main窗口的 `/workflows` iframe加载固定 `http://127.0.0.1:18888/editor/` 无认证静态React壳，connect-src none、无native capability。数据走有限MessageChannel→具名native→API。E只在native/API内存，300秒到期；不依赖WK Cookie、不装系统CA、不加新scheme。真实消息/CSP/返回/重连资格仍第5步实测。
- Idle：真实列表显示草稿/内部版本、可执行性和最近运行；服务未准备时保留清晰入口。
- Loading：区分服务准备、列表、editor、保存、试运行与执行；禁止重复写入，保留操作对象和已知状态，避免整页被无限等待锁住。
- Success：根据 provider 响应更新 ID/revision/version；运行成功必须有原生终态和实际输出。
- Empty：无流程提示创建；无历史明确空历史，静态推荐不进入真实历史计数。
- Error：清楚区分服务不可用、editor 加载失败、无权/资源不存在、保存冲突、普通输入错误和运行失败；错误不泄漏 token、原始凭据或内部堆栈。
- Retry：读取可显式重试；写请求结果不确定先查资源或 run。普通输入错误修正后再发起，不无限重建或重发。
- Cancel：未保存离开时提示保留或放弃；取消本地等待不改变远端状态。首期等待真实终态后再正常停止服务，不能把强杀当取消。
- 视觉验收：亮/暗主题、1180×760、1440×900、键盘 Tab/Enter/返回、焦点可见和主体无横向溢出。已有白底青柠说明实测 **1.28:1、1 项 serious color-contrast**，按用户要求保留且单独记录；本需求检查新增回归，不继承旧“0 axe”或 FEAT-151 历史 D4，也不暗改品牌色。

## 4. Must 验收

| AC | 可观察行为 | 验证方式 |
|---|---|---|
| AC-001 | 已核实 Coze main/source SHA 接入 12 仓清单，6 份既有缺失及其它工作区改动保留；不虚构远端、commit/push。 | 源 blob/mode 与恢复前后差异、Git/source lock、manifest 和专用治理检查；步骤 1 完成后登记证据。 |
| AC-002 | 工作流协议 source-first、provider/consumer 同源；原 Chat、公开 OIDC 与既有 wire 保持有效。 | 安全生成、candidate 来源/摘要、focused conformance、旧入口差异及正常回归；不冒称发布/生产兼容。 |
| AC-003 | 全程 local 零登录，native/server 固定 scope 并核验实际资源；renderer 不选择身份或取得秘密，非 local/缺 gate 不启用 bridge。 | 具体设计确认后的边界审查、同一 App 零登录实测、正常配置和合成 scope focused checks；不发越权/攻击请求。 |
| AC-004 | 同一 App 加载真实独立 editor，可返回/重开，仅使用批准的 origin/消息且无 native capability。 | canonical dev 与 packaged WebView 真实加载、MessageChannel握手/绑定、IPC隔离、CSP/到期重连/导航/失败恢复，不保存秘密值。 |
| AC-005 | 真实创建并保存有效三节点流程，列表重开同 ID/revision/内容，保存冲突不静默覆盖。 | UI happy path、provider read-back/ID/revision、正常并发 focused test，禁止 seed Store 模拟成功。 |
| AC-006 | 草稿试运行成功后内部发布固定版本，三个动作语义清楚、无 Force；后来改草稿不改变内部版本。 | 真实节点输出、发布响应/版本读回、草稿/版本对照。 |
| AC-007 | 执行指定内部版本，结果、节点信息和历史对应真实 run ID/version，未知状态不猜完成。 | 同一正常入口执行及文本结果对照、原生状态/历史读回；验证真实历史列表能力。 |
| AC-008 | 节点/输入/图/并发/超时有明确上限，普通错误修正后可重试，未知结果先查，取消不伪称远端中止。 | 原生与契约共同冻结限制；正常错误→修正→成功、重复动作/未保存返回 focused checks，无故障注入。 |
| AC-009 | 独立固定来源 local 栈 loopback/ready；完成后正常停止/重开保留草稿/版本/历史、原 Chat 数据不变，Coze 未 ready 不挡 Chat。 | 来源/数据范围、实际 ready、正常退出后端口/进程、保留 volume 重开；不能正常退出就停止并报告。 |
| AC-010 | 新 UI 沿用现有布局/配色且键盘可用，示意卡不冒充 ERP；安全验证和合成数据、模型/平台/付费调用 0，既有对比度与禁止测试如实记录。 | 主题/窗口截图、键盘/新增可访问性复核、diff/旧文件摘要、预算和未执行项表；不记全仓 PASS。 |

AC-001 已通过第 1 步本地仓库接入检查，证据见 02 和 evidence/step1-verification.json。AC-002—010 的完整 fresh D4 结论仍保留 pending/NOT RUN；其中源契约/服务实库分项见06、07，dev/packaged最小编辑、自然会话、关闭和Chat边界的真实分项见10。分项通过不等于完整运行/发布/历史及视觉AC通过。随后完整产品页与首次fit源码已实现，见11；本轮Mac锁屏，新增真实App及全主题/尺寸仍NOT RUN。

## 5. 工程事实与边界

- 受影响仓库仅六个：`yijie`、`yijie-coze`、`yijie-contracts`、`yijie-api`、`yijie-infra`、`yijie-desktop`；更新后项目共 12 仓。本期不改 Host、Codex、Connectors、Knowledge、Skills 或 Admin 业务。
- 源码基线：上游 `coze-dev/coze-studio@fefb05ff27be1da939612fbf9faf5db62583b8ae`，tree `39f5d2befc24de628da7a253c42c9439640049cc`。本地 15,299 个文件内容与 Git mode 完全相符，缺 docs 下 6 份 NATS/OceanBase/Pulsar 中英文指南；缺失按既有差异保留。第 1 步只恢复 Git 元数据、不 checkout 工作文件，source origin 使用用户提供的上游、分支 main；不向上游推送。
- 远端边界：`36Dge/yijie-coze` 当前双渠道查询 404，只能确认不可访问或不存在。不得登记成已经创建；独立易界远端的归属/可见性/创建与 commit/push/tag 另行决定。
- 真实入口：目标复用 `yijie-desktop` 的 canonical `pnpm tauri:demo-fast:app`，开发链同源，从 `/workflows` 进入 editor。专用 Coze up/status/stop 入口尚未实现，不能用占位脚本退出码、Docker Started、browser-only 或第二个测试 App 冒充正常产品结果。
- 环境事实：Docker Desktop 4.82.0 在本机用户 Applications 中，原厂 bundled Compose 5.3.0 可执行；daemon 不可达，PATH docker 未发现 plugin。宿主 Go 1.26.4、API 要求 1.26.5；Node 26.0.0、pnpm 11.19.0 与各仓精确版本仍需构建前核对。第0/2步审计未启动、安装或下载；第3步使用已缓存原厂Go1.26.5，并正常下载Coze锁定Go依赖用于编译测试。未重写Go/pnpm/Cargo锁或Coze Rush。
- 身份边界：用户已批准并由ADR-0019明确新增local bridge，按05的exact三项gate、固定native owner/tenant、分离K_NA/K_AC与300秒resource-bound E实施；不借用FEAT-125/126历史profile、不接受renderer自证身份、不放秘密到URL/消息/页面存储/日志。public/production原OIDC/权限保持；设计批准不等于服务已实现。
- 契约影响：完整设计 **semantic**，因为新增 local 服务身份、权限与启动语义；若破坏既有受支持交互则升级 breaking。第0/1/2步的审计、需求、登记和设计自身为 **none**；本轮第3步新增源wire、独立expand migration与native/provider实现，实际影响 **semantic**。
- 权威顺序：local/editor决策已批准，第3步已在 `yijie-contracts` 定义归一化操作、状态、revision/version、失败与幂等；源先生成/验证，然后API/Coze/native候选实现，之后Infra和Desktop产品。API 现有 lock 必须按真实 source 校验；demo_fast 本地 candidate 不冒称不可变发布 tag 或生产全基线兼容。Coze 原始 IDL 固定上游来源，新增易界跨仓协议仍必须 source-first。
- 数据权威：API 维护明确的资源归属/映射及业务审计，Coze 管理图、版本和执行事实；不互读私有表、不复制第二个执行状态机。仅独立合成数据，已规划的新增私有 schema 走所属仓 expand migration；正常停止保留 volume，不改既有 Chat/Host 数据，不承诺在途执行恢复。
- 既有改动：原有 11 仓状态已记录；Desktop 6 个 tracked 修改与 2 个 untracked 文件有逐文件摘要，保持用户当前布局、青柠说明和交互，不 reset、覆盖、全仓格式化或混入无关变更。上游缺失文档和两份 `.DS_Store` 不作为“恢复源码”的理由改写。
- 验证安全：Contracts 默认生成会写 zip-slip archive；Desktop 默认检查含历史攻击 fixture，Rust 全测含权限故障。依用户硬规则跳过这些路径，使用已有 safe 与源码审阅后的 focused checks，记录未执行项目/原因/影响；禁止强杀、binary 伪装/替换、权限破坏、攻击注入。允许本项目 canonical 构建生成可复现开发产物，不覆盖用户签名/发布/无关 binary。

## 6. 推荐方案与停止条件

- 推荐保留 Coze 独立仓库、原有 React 构建和执行引擎；易界保留 Vue 产品入口、API 资源边界、独立 Infra 生命周期。先证明三节点真实闭环，不拆出一个纯 workflow engine，不扩建 ERP 节点或重写整个编辑器。
- 技术分步：0 审计完成 → 1 Git/来源/清单治理完成 → 2 local/editor/native/session具体设计完成与D0 → 3 最小 Contracts/provider/native-session → 4 Infra 受控栈 → 5 先真实载体资格再完整 Desktop → 6 单次 fresh canonical 验收。按用户要求逐步执行，但采用 demo_fast 技术顺序，不建立 G0–G6/per-slice G3 治理切片，不将步骤完成换算 D4。
- 第2步授权已取得，05对批准范围作可实施细化，D0检查见02。保留MessageChannel真实平台表现、受控栈、事务/预算等后续实现证据，不把这些NOT RUN写为再次等待同一批准；不将本轮技术细化伪称用户逐字段审查。
- 30 分钟没有新证据：读取真实日志与完整调用链，停止猜测式补丁；不重复改变权限开关碰运气。
- 90 分钟同一核心阻塞：明确失败点并简化非核心载体；iframe 不可行则展示同 App 无 native 能力 WebView 的具体替代，不默默开放外部 origin 或要求手工登录。
- 非核心检查累计 120 分钟：登记限制；核心零登录/真实执行累计 240 分钟仍不可用：暂停扩建并收口一个根因或范围决定，不能降成 mock。
- 总计 16 小时未 D4：重新决定范围与估时；保留已完成仓库接入及失败证据，不把未完成集成标为可用。
- 任一启动/停止无法安全完成：停止该步骤并报告；不得强杀、删 volume 或破坏权限制造验收。出现真实敏感数据、外部付费、公开部署或不可逆操作立即回到对应授权边界。

## 7. 当前证据与完成判定

第3步实现与联审见 [06 源契约与最小桥接](06-step3-implementation.md)。源与三个consumer均为未发布本地候选，不冒称不可变契约提交。

只读审计已完成，见 [03 接入前审计](03-pre-integration-audit.md)、[04 分步执行与决策](04-stepwise-plan.md) 及 `evidence/` 三份专项审计。第 1 步已完成，source lock、Git/worktree 保护、清单与实际检查见 01、02 及 step1-verification.json；AC-001 的 PASS 只限仓库接入。

受控服务栈和数据库资格已在第4步实测；第5步真实App创建、画布/连线编辑、保存重开、自然到期重连、关闭确认与Chat切换已在dev/packaged范围实测。完整App试运行/内部发布/版本执行/结果历史，以及全主题/尺寸/新增可访问性与一次fresh D4仍未完成。不同步骤证据单独记账，不能合并冒称D4。危险 fixture、权限故障、强杀/攻击测试永久不执行；本轮不宣称全仓绿色或完整生产安全认证。

最终 D4 需要一次 fresh canonical local run 覆盖全部 10 条 Must AC、真实输出、正常错误修正/重试、正常停止重开、相关 safe/focused checks 和完整 diff/status，附截图/脱敏 request ID/结果 Artifact，并保留已知颜色限制。单次 source 审计、文档检查或容器 ready 不能替代这个用户结果。
