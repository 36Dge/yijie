# FEAT-153 接入前审计

日期：2026-09-12。范围：12 个项目目录的仓库状态，以及 Coze / Desktop / API / Contracts / Infra 的相关代码、构建、身份与部署边界。审计方式为只读源码核查、GitHub 官方源查询及逐文件校验；未启动应用或容器、未运行攻击或故障注入、未调用模型和商家 API。

> 后续状态：用户已批准第 2 步方案，设计收口见 05 和 Accepted ADR-0019；本审计保留第 0 步时点事实，不改写当时的 NOT RUN。

## 结论与执行边界

**有条件接入。** 当前 Coze 具有创建、草稿保存、试运行、内部发布版执行及结果查询代码，可以支撑通用三节点流程。现有易界工作流页面只有静态展示。可以先实施本地 Git 来源恢复、仓库清单与开发治理接入；这一步不启用 Coze 服务，也不改变身份、CSP、公共 API 或产品运行行为。

完整基础集成尚未通过。身份桥接、独立编辑器的 WebView 会话、资源归属、运行限额及安全部署配置必须先落定，并以同一正常 Desktop 入口实测。不能把目录存在、容器 Started、空画布创建或文档校验通过称为工作流可用。

本审计及需求文档变更 `contract-impact=none`；FEAT-153 完整候选实现按 `semantic` 评审，因为将增加本地服务授权与启动语义。新 HTTP 操作可为 additive 子边界；若具体实现使既有受支持交互失效，必须升级 breaking。

## 来源、已有改动与外部事实

- 上游：<https://github.com/coze-dev/coze-studio>，查询时 main 为 `fefb05ff27be1da939612fbf9faf5db62583b8ae`；commit tree 为 `39f5d2befc24de628da7a253c42c9439640049cc`。
- 上游 tree 含 15,305 个文件。本地 15,299 个文件的 Git blob 内容和 Git 可执行/符号链接模式完全一致，修改 0；缺少 docs 下 NATS、OceanBase、Pulsar 六份中英文指南。另有两份 `.DS_Store`。这些缺失文件按既有差异保留，不自动恢复。
- 本地原先无 `.git`。本次只能证明文件与指定上游来源相符，不能声称原有 Git 历史/分支已存在。
- `36Dge/yijie-coze` 经连接器与 gh 两种查询均返回 404：只能结论为当前身份不可访问或仓库不存在，不能登记成已创建远端。
- 首步使用用户已提供的上游 URL 和实际 main 分支，恢复本地 Git 元数据并固定源提交；易界独立 GitHub 远端、提交与推送不在该首步内。不能向 coze-dev 推送易界修改。
- 11 个原有 Git 仓库的 HEAD/branch/origin/status 已记录。Desktop 的 6 个 tracked 修改、2 个 untracked 文件逐文件 SHA-256 固定；保持用户现有布局、青柠色和交互。不继承 FEAT-151 历史 D4。

证据：[仓库快照](evidence/workspace-before.json)、[源文件对比](evidence/coze-source-comparison.json)、[既有改动校验值](evidence/preexisting-dirty-files.json)。完整逐文件哈希仅存本地 `.local/feat153-audit/coze-file-hashes.json`，未把 15,299 项流水数据混入需求正文。

## 主要发现

P1 表示必须在对应阶段关闭的接入阻塞；P2 表示需要明确约束的维护或可靠性问题。下面是静态审计发现，不是通过攻击测试验证的漏洞结论。

| ID | 等级 / 阻塞阶段 | 事实、影响与处置 |
|---|---|---|
| AUD-001 | P1 / 仓库登记 | 清单只有 10 个子仓；验证器只允许 36Dge URL，测试固定 10/develop。Coze 无 AGENTS、根 lint/test 目标。新增精确 Coze 上游例外与 main 覆盖、来源锁及专用治理检查，不放宽所有外部 URL。证据：`yijie/scripts/repo-manifest.mjs:29`、`tests/repo-manifest.test.mjs:5`。 |
| AUD-002 | P1 / 源版本 | 本地没有 Git 元数据，应用镜像使用 latest。先恢复已核验来源并保留 6 份既有缺失；运行阶段固定源构建/image digest，不能以 latest 镜像代表本地源码。 |
| AUD-003 | P1 / 身份与编辑器 | Desktop local identity 由 Rust authority 给出，没有可复用的 API/OIDC/Coze session；Coze Web editor 要求 session cookie，PAT 只解决另一组 OpenAPI。新桥接必须由 native/server 确定固定 scope，不能从页面传入任意 user/space。 |
| AUD-004 | P1 / 资源边界 | Coze Save/Canvas/TestRun/Publish 校验请求 space 后单独按 workflow ID 操作，未见与真实资源 SpaceID 绑定。local 适配也必须限定服务端拥有的资源；public 前另作完整核权。没有进行越权请求或利用测试。 |
| AUD-005 | P1 / 编辑器载体 | Desktop 当前无 frame-src、remote editor 或通用 HTTP gateway。React app bundle 与 Vue 独立构建；iframe 的 WKWebView cookie/导航/返回机制必须实测，不能先宣称可用。 |
| AUD-006 | P1 / 正常启动 | Coze 原 server 脚本可能安装 Deno、goimports -w 全仓格式化、重建 bin/config。Compose 含 privileged、固定容器名、非 loopback 默认端口和不足的 app readiness。易界另建受控入口；可复现项目构建产物允许正常构建，禁止覆盖无关/签名产物。 |
| AUD-007 | P1 / 有界执行 | 默认画布没有有效连线；节点/超时默认限制可能为 0。首期只允许开始、文本处理、结束，前后端同范围，限制输入/图规模/并发/超时。禁止将 Code/HTTP/插件/模型节点作为首期捷径。 |
| AUD-008 | P1 / 验证安全 | Contracts 默认生成包含 zip-slip 危险归档；Desktop 默认检查包含历史攻击 fixture，全量 Rust 测试含权限故障场景。按用户硬规则跳过，使用已存在 safe 入口及逐项审阅的 focused checks。不能记全仓 PASS。 |
| AUD-009 | P2 / 版本与重试 | 草稿、试运行、内部发布版不同；公开 run 要求已发布。创建/发布为多个写入，报错不保证未产生资源。必须读回确认、固定 revision/version/run ID，禁止无条件自动重建/重发运行。 |
| AUD-010 | P2 / 生命周期 | 异步运行使用进程内 goroutine；MySQL execution、Redis checkpoint 存在不证明在途工作会自动恢复。首期仅验短流程完成后正常停止/重开与记录持久化，不承诺调度、补偿、持久队列。 |
| AUD-011 | P1 / 真实数据及公开 | DEBUG 日志记录请求响应片段；PAT 派生和过期校验存在静态复核问题。首期只用合成数据、关闭正文 DEBUG 日志、内部桥接；真实商家与公网另立生产加固，不冒充已解决。 |
| AUD-012 | P2 / 文档事实 | API 实际已有 public-api.lock 和 generate-check，AGENTS 描述已过时；API 固定的 Contracts 提交与当前 sibling 不同。后续按实际锁/source-first 处理，不批量改 pin 或重写历史报告。 |
| AUD-013 | P2 / 既有 UI | 用户保留的白底青柠说明已有 serious contrast 记录；此次不暗改品牌色，不把历史 0 axe 继承为新验收。新功能需检查新增可访问性回归并独立报告该既有限制。 |

详细调用链与行号见 [Coze 审计](evidence/coze-audit.md)、[Desktop 审计](evidence/desktop-audit.md)、[API/Contracts/Infra 审计](evidence/boundaries-audit.md)。

## 环境事实

Docker CLI 29.6.1 可用，当前 daemon 不可达且 PATH 未发现 Compose 插件。进一步只读核查确认 Docker Desktop 4.82.0 已安装于 `/Users/jack/Applications/Docker.app`，其原厂 bundled Compose v5.3.0 可执行。因此环境属于“已安装、尚未启动与验证”，不能说机器没有 Compose，更不能记 readiness PASS。后续使用应用自身正常启动流程及原厂插件，不伪装或替换运行时。

宿主 Go 1.26.4，API go.mod 要求 1.26.5；Node 26.0.0、pnpm 11.19.0；项目指定 packageManager 11.7.0。审计未触发安装。源码构建时要按各仓真正要求固定工具链，保留 Coze Rush/独立 pnpm 版本，不能用易界根 pnpm 重写 Coze lockfile。

## 未执行项目、原因及影响

| 项目 | 状态 / 原因 | 影响 |
|---|---|---|
| Coze / API / Desktop 全栈启动、UI、真实三节点执行 | NOT RUN；审计阶段只读，身份和载体方案未落定 | 不证明基础集成可用 |
| 全量默认 generate/test 与历史攻击 fixture | NOT RUN；用户禁止危险归档、攻击注入、权限破坏 | 无这些历史测试覆盖，不伪造全套通过 |
| 强杀、崩溃注入、权限故障、危险资源测试 | NOT RUN；用户永久禁止 | 不证明这些异常恢复能力；用正常完成后 stop/start 验证 |
| 生产多租户、平台凭据、店铺写入、模型调用 | NOT RUN；本需求明确排除，预算 0 | 不证明生产/ERP/AI 能力 |
| 完整依赖 CVE、公开渗透或供应链专项 | NOT RUN；不是本轮全量安全认证范围 | Apache 文件与源树比对不等于所有依赖安全或许可证均审结 |

## 审计后顺序

1. 完成 FEAT-153 需求包、仓库来源与清单接入，运行安全治理检查。
2. 展示并确认准确的 local identity / editor / Tauri 权限候选方案，完成 D0；实际平台载体资格须等待最小契约/provider/受控栈就绪。
3. 按 Contracts → provider/存储 → Infra → Desktop 顺序实施；上一步真实条件不满足时不跳到下游制造占位成功。
4. 单次 fresh canonical run 覆盖完整 Must AC，D4 才可 PASS。

这里只规定技术执行顺序，不创建 production_hardened 的治理切片，也不将分步检查冒充 D4。
