# ADR-0019: Coze 工作流基础接入与本地编辑器边界

## 状态

**Accepted** — 2026-09-12。用户在本任务明确回复“批准该方案，继续第 2 步”，批准同窗口独立编辑器、限定本地地址、无编辑器原生权限及固定本地身份/短会话方向。第 2 步已按此范围完成技术细化；这是设计批准，不是已实现、D4 或生产启用。具体实施语义以 [05 本地设计](../features/FEAT-153-coze-workflow-foundation/05-local-integration-design.md) 为准，源契约仍须第 3 步先行。

决策负责人：段成威。关联需求：[FEAT-153](../features/FEAT-153-coze-workflow-foundation/00-feature-brief.md)。

## 背景

易界计划将面向跨境电商卖家的部分服务组织为节点和工作流，主要入口是 Desktop 的“工作流”页面。当前页面只有静态展示与本地选择反馈；Coze 包含真实图编辑、草稿、试运行、内部发布与执行能力，但其账户、空间、React 前端和部署依赖尚未与易界整合。

[接入前审计](../features/FEAT-153-coze-workflow-foundation/03-pre-integration-audit.md)已发现来源、身份、资源归属、WebView 会话和运行限制等阻塞。本 ADR 记录已批准方向，具体技术顺序见[分步计划](../features/FEAT-153-coze-workflow-foundation/04-stepwise-plan.md)，接口、数据和权限范围见 05。实际资格完成前不能宣称 iframe 或基础集成已可用。

## Contract impact

完整集成设计为 **semantic**：新增本地工作流服务的身份、启动和用户操作语义。新 HTTP 操作可以是 additive 子边界；若任何受支持交互失效，整体升级为 breaking。本文及只登记来源/清单的步骤不改变运行边界，单独为 none。

易界拥有的跨仓 HTTP、IPC 和共享 payload 以 `yijie-contracts` 源契约为权威，先源契约与安全生成，再 provider、consumer 和同源 conformance。Coze 原生协议/图格式以固定上游源码为适配依据；不复制第二份公共 DTO，不把本地 sibling 候选称作已发布 tag 或生产兼容批准。

## 决定

### 1. 独立工作流引擎与六仓职责

工作流可独立于 Codex Runtime 和 Agent Host 执行。FEAT-153 不增加 Agent 节点，不改 FEAT-152 权限语义，不恢复已退役 FEAT-137；后续需要 Agent 能力时另行设计节点边界。

| 仓库 | 职责 |
|---|---|
| `yijie` | 仓库清单、源版本记录、跨仓架构、需求治理和开发入口索引。 |
| `yijie-coze` | 独立 React 编辑器、图定义、草稿 revision、内部发布版本、试运行/正式运行及节点执行事实。保留上游构建体系。 |
| `yijie-api` | 工作流业务资源归属、固定本地 scope 映射、编辑/执行授权、业务审计及 Coze 适配。 |
| `yijie-contracts` | 易界工作流 API/IPC 共享契约、状态与错误语义、版本和生成来源。 |
| `yijie-desktop` | 既有“工作流”入口、真实资源列表、编辑器容器、运行操作和结果展示；不持有平台凭据或决定执行事实。 |
| `yijie-infra` | 固定构建/镜像、独立本地数据、受控服务拓扑、readiness、正常启停及配置边界。 |

API 与 Coze 不互读私有表。Coze 管图、版本、run 和节点结果；API 管资源映射和业务审计，只保存必要关联/投影，不再维护竞争的执行状态机。Desktop 不依据计时器、按钮选中或助手文本推定完成。

### 2. 仓库来源先接入，不虚构易界 fork

按用户提供的 `https://github.com/coze-dev/coze-studio` 作为本地 `source origin`，使用实际 `main` 分支和审计固定提交 `fefb05ff27be1da939612fbf9faf5db62583b8ae` 恢复来源与登记清单。保留当前文件及已记录缺失，不改原有 11 仓的分支/远端，不转为 monorepo/submodule。

当前没有已验证可访问的易界 fork。不得把 `36Dge/yijie-coze` 登记为已创建远端，也不向 coze-dev 推送易界修改。后续独立远端、commit/push/tag 另按真实授权处理。运行制品需与固定源码构建或镜像 digest 关联；`latest` 不构成版本基线。

### 3. 同窗口静态 iframe 与受限原生传输

iframe 固定加载 `http://127.0.0.1:18888/editor/` 的独立 Coze React bundle，只包含无认证静态代码/内置资源。主窗口仅新增精确 frame-src；iframe sandbox 只允许 scripts/same-origin，禁止外部导航、新窗口、硬件能力，editor CSP connect-src 为 none。不给 HTTP Remote editor native capability，不把 React 组件体系装入 Vue。

工作流数据走版本化 MessageChannel → 主 Vue 校验精确 frame/source/origin/有限操作 → 具名 workflow Rust commands → 固定 local API → 私有 Coze adapter。没有任意 URL/header/native 命令转发。三个 editor 原生命令只负责 open/exchange/close，其余有限 native 入口供可信父页列表、创建、执行和查询；所有业务授权由 native/API/Coze 分别核验。

短会话 E 由 API 颁发并绑定 actor/workflow/run epoch，绝对有效期 300 秒；只由 Rust/API 内存保管。如果使用 HttpOnly Set-Cookie 交接，仅在原生 HTTP 端使用，不交给 renderer 或 WK cookie store。到期保留未保存图并提供父页显式重连；关闭、换 epoch、正常退出失效，不无限自动续期。K_NA、K_AC 是分离的 256-bit run-scoped 服务凭据，不能作为浏览器 cookie、URL、postMessage 或 Host/Codex 环境传递。

该传输细化避免依赖 WK 第三方 cookie、添加系统 CA 或注册可能被 Tauri 认作 Local 的 custom scheme；保留用户批准的独立 iframe、零登录、秘密不进编辑器及无原生权限边界。不会以 cookie 入队或 store 写入成功冒充网络资格。

启用要求 exact local + demo_fast + workflow enable。固定 owner/tenant 仍由既有 Rust authority 提供，API/Coze 使用持久资源映射核权。ADR-0018 的原有身份体验保持；本 ADR 明确新增工作流 local bridge，不改原 API OIDC/public policy，不调用公开 Coze 注册/PAT，也不信任 renderer 的身份参数。

### 4. 依赖就绪后验证 WKWebView，再扩展 Desktop

执行顺序为：第 2 步确认具体设计并完成 D0 → 第 3 步完成实验必需的最小源契约、provider 与 native/session 桥接 → 第 4 步启动受控本地栈并取得 readiness → 第 5 步首先验证真实编辑器载体，成功后才扩展完整 Desktop 功能 → 第 6 步统一 D4。D0 确认可评审设计，不声称尚无 provider/Infra 的真实编辑器已经通过资格验证。

第 5 步在上述真实依赖就绪后，采用[第 2 步 Desktop 附件的 Q-D01–06](../features/FEAT-153-coze-workflow-foundation/evidence/step2-desktop-feasibility.md)及 05 第 7 节验证 editor-ready、会话、资源创建/保存/重开和正常退出。canonical dev 与 packaged `tauri://localhost` 分别验证 MessageChannel、CSP、具名 IPC 隔离、受控资源传输及返回行为；browser-only 成功不替代真实 App。原第 0 步 EXP-D01–09 保留为候选调查历史，不将已排除的 WK Cookie 条件重新列为当前资格。为验证载体而实现的 native/session 及最小容器仍服从已确认权限范围和 source-first，不提前扩展完整列表、运行结果等产品功能。

只有 iframe 不能满足上述边界时，才评审方案 B：同一 App 内由原生管理的专用 editor WebView/window，仍不授予远程 native capability。不得静默扩大 CSP、关闭浏览器安全、手工登录或创建第二个测试 App 作为替代。

### 5. 本期只做无模型三节点真实闭环

仅允许开始 → 文本处理/拼接 → 结束；前后端一致限制节点、输入、图规模、并发和超时。Code、HTTP、插件、模型、循环、真实店铺与电商服务均不属于首期。数值与草稿/运行的完整性差异按 05 冻结：未完成安全草稿可保存，只有执行/发布才必须是完整三节点；input 4 KiB、prefix 1 KiB、output 5 KiB、canvas 256 KiB、单个在途执行、30 秒合作式预算。

草稿保存、试运行和内部发布版本分别表达；保存使用 Coze 事务 CAS，成功试运行必须绑定同一 revision；内部发布事务化且不开放 Force。内部发布是引擎可执行版本，不是公开到市场或生产。运行固定发布版本及 run ID，保存草稿不改变已发布版本；未知执行状态如实显示。

创建、发布和运行的失败不保证未产生资源；结果不确定时先查询，禁止无条件自动创建或重发运行。并发保存使用明确 revision 冲突，不能静默覆盖。原有八张电商参考卡保持真实展示语义，不连接通用示例后宣称具体电商服务可用。

### 6. 受控本地运行与数据保留

工作流服务采用独立命名空间、数据目录/volume、固定版本及必要 loopback 入口；不直接启动 upstream privileged/latest 默认栈，不复用 Chat/Host 或生产数据库。依赖裁剪以真实初始化和 readiness 为证，不因三节点简单就假设其它依赖可删除。

工作流服务的进程所有者与正常启停由 Infra/launcher 设计唯一确定；只有用户进入工作流时才要求其 ready，不因 Coze 未启动而阻断原 Chat。仅使用合成内容，关闭正文 DEBUG 日志，模型及外部业务调用预算为 0。

短流程完成后验证正常停止、重开及定义/版本/历史保留。容器停止使用 SIGTERM 与 timeout=-1，避免 Docker 有限超时后强杀；观察超时只报告 STOP_PENDING，保留状态，不升级 kill。退出不删除 volume；数据删除另行处理。进程内异步执行和已有 checkpoint 不构成“在途运行可恢复”的证明，本期不承诺调度、补偿或持久队列。

## 安全验证与验收

验证正常输入、空列表、资源读取、保存冲突、已完成流程结果和正常 stop/start；检查新增 UI 的 loading/empty/error/permission denied/retry、键盘、亮暗主题和 1180×760。已有用户保留的白底青柠说明对比度限制独立记录，不暗改颜色，也不记作通过。

遵循用户永久安全条款：不强杀制造故障、不伪装/篡改受保护 binary、不破坏权限、不注入攻击资源。Contracts 使用现有 safe 生成入口，Desktop/各服务执行前审阅命令并选择正常 focused checks；含历史危险 fixture 的全量测试标 NOT RUN，说明覆盖缺口，不关闭门禁或伪造 full-green。

源码审计、本地仓库登记、载体实验均不等于 D4。最终必须从同一 canonical Desktop 正常入口完成一次 fresh run 的完整 Must AC、真实三节点结果、代表性正常错误/恢复和退出重开，并记录真实来源与限制。

## 回滚与停止

- 仓库登记与运行启用分开：尚未启用服务时回滚清单/新增治理内容即可；不 reset、覆盖用户文件或删除来源历史。
- 运行回滚先关闭工作流入口/桥接并正常停止其独占服务，保留 synthetic 数据及映射；原 Chat/Host 不变。无法正常退出时停止步骤并报告，不追加 kill、prune 或 down --volumes。
- 草稿/图/映射格式发生变化时，只回退到已验证兼容 reader；未证明兼容不降级写入，不修改历史 migration 或伪称数据库可逆。
- iframe 消息传输、会话归属或原生隔离无法证明时停止下游扩展，保留事实并评审 B；不通过 mock、静态卡状态或放宽权限完成验收。

## 决策已收口，运行证据仍开放

精确静态 origin、消息/native 传输、actor/两段机器机密/E 生命周期、独立 API/数据及版本/CAS/历史/正常停止语义已在 05 冻结。未拉取的 image digest、实际 bundle 初始化、MessageChannel 在 dev/packaged WKWebView 的表现、迁移/事务和执行预算协作仍须在对应实现步骤验证；它们不是尚未批准的同一架构问题，也不能预先写 PASS。

旧候选中的浏览器 HttpOnly cookie 直传与 custom scheme 不作为实施路径；原同 App 专用 editor WebView 方案 B 仅在真实资格不满足时重新评估，不能静默切换或扩权。

## 明确延后

公开服务、生产 OIDC/RBAC/多租户、PII/平台凭据、电商高风险写入、完整供应链/安全专项、生产迁移、持久调度/补偿、SLA 和发布观察均不在本期。进入公开/生产时按适用 DP 或独立 `production_hardened` 补齐要求，不能沿用 local D4 声称生产可用。

### 2026-09-12 第4步受控栈细化

用户明确要求执行受控 local 栈与真实数据库验证。运行依赖审计将完整 application.Init 收敛为同仓私有 workflowlocal.InitRuntime，继续使用上游真实 workflow repository/service/节点实现，只初始化 MySQL、Redis、MinIO；API 独立 PostgreSQL。未提取或替换引擎，不启动知识库/搜索/MQ/模型。部署 FILE 配置、精确镜像与正常停止要求见 FEAT-153/05 追加记录及 Infra workflow-local 资产。此为已批准范围内的部署实现细化，保留第3步 wire 与既有 App 启动边界；最终产品/D4 仍单独验证。


第4步首次实际启动后，全部服务容器内ready且显式migration成功，但Docker29的internal-only API没有建立host端口（NetworkSettings.Ports为空）；资格工具在status前失败，尚未创建业务流程。已正常SIGTERM停止所有8个自有容器，均exit0/noOOM。拓扑细化为API同时连接本project的workflow-edge桥进行loopback18888发布，Coze及四项依赖保持internal-only；没有新增host端口/通用代理/模型平台调用。API edge不等同于物理禁止出站，实际入口仍固定源定义与私有Coze URL。后续readiness同时要求六服务健康及宿主带K_NA的真实status，不能仅凭容器内probe写PASS。此修正不涉及旧项目或数据库重建。

## 2026-09-13 Git 交付补充

统一local D4通过后，用户明确授权FEAT-153提交/推送，并授权新建私有`36Dge/yijie-coze`。
原先“尚无易界fork”的来源接入状态已由实际仓库创建替代；元仓清单指向该易界仓，
本机原origin改名upstream保留，origin指向易界。上游完整SHA、许可与source lock保持，
原六份工作区缺失不进入提交。Contracts先形成完整提交，再固定三个消费者来源并交付，
真实结果见FEAT-153/18；不授权tag、merge、SDK发布或生产启用。
