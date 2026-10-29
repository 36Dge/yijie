# FEAT-166 — Codex fork 与既有产物机制复用审计

> 本文为需求分析/复用审计时点依据；当前实施与真实客户端结果见[08 D4验收](08-d4-acceptance.md)，下文的未实现描述不代替当前交付状态。

> 2026-10-29 · 只读源码/manifest审计；本文件不代表运行验证、Runtime改动或用户批准实施。

## 1. 用户约束与结论

用户明确要求：对话流生成物的预览必须先检查`yijie-codex` fork是否已有封装工具，已有机制必须复用，不能从头发明一套工具。本条作为FEAT-166的实现前提。

本次确实检查了固定Runtime源码、工具注册/handler、app-server文件与MCP协议、扩展模块、依赖及当前r5构建清单。**已存在文件读写/命令、模型图片读取、MCP工具与资源桥接等基础机制，必须保留并复用既有生成和接入链；本次核对范围内未发现可直接用于用户侧DOCX/PPTX/XLSX/PDF正文/页面或HTML右侧栏的现成阅读器。**后者只是阅读呈现能力缺口，不能推导成“重造文件工具、产物传输、存储、权限或Runtime”。

本次用户已明确：HTML允许隔离渲染脚本，禁文件操作和页面业务操作；Office/PDF必须正文或页面预览。不能以Runtime未带阅读UI为由退回信息卡或缩减这些目标。

## 2. 来源、版本与审计范围

| 项目 | 本次读到的事实 |
|---|---|
| yijie-codex分支/HEAD | `chore/retirement-baseline-20260905` / `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a` |
| 工作区 | `git status --short`为空；未修改源码/patch/制品 |
| 上游 | `https://github.com/openai/codex.git`，`rust-v0.144.6`，完整commit `5d1fbf26c43abc65a203928b2e31561cb039e06d` |
| fork范围 | `UPSTREAM.md`与`.yijie/upstream.env`固定`codex-rs/` Runtime子树；不导入IDE extension、cloud或其它非Runtime源码 |
| r5来源 | `scripts/build-kimi-k31-pro-r5.sh:38`—`:47`的精确补丁表，以及已存在的`.yijie/build/kimi-k31-pro-r5/aarch64-apple-darwin/runtime-manifest.json` |
| 已存r5 manifest | Runtime `codex-cli 0.144.6`，target `aarch64-apple-darwin`，stdio；269个schema、tree SHA-256 `d8c3265d8923ef4437203c0a2ded954549b4abc0c5079ecd6bcdf7c6da72f11e`；binary摘要记载为`283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e` |

manifest中的值是既有文件记载，本轮没有重建/启动binary、重生成schema或重新验证digest，不将其写成新的运行资格。当前实际App使用哪个制品仍以其来源绑定/FEAT-165交付记录为准；不能从源码目录或manifest存在推断进程已经加载。

消费侧也已核对：Desktop的`contracts/runtime-kimi-k31-pro.candidate.json`固定Contracts来源`61137174a25dc368e0006f27633fd4a9ad097aa6`、上述Runtime源commit和r5制品摘要；`scripts/run-local-demo-fast.sh:274—288`校验该candidate并选择r5路径。Host当前源码HEAD为`36ec8c62cca771b479b317d209da50d6acda0989`。这是配置/来源证据，不是本轮启动或真实调用成功；快照见`references/reaudit-source-snapshot.json`。

当前r5按序使用以下11个补丁；路径是身份的一部分，不能与同数字的历史FEAT-137补丁混淆：

1. `0001-feat-126-filter-persistent-diagnostics.patch`
2. `0002-feat-136-unified-exec-pre-emitter-command-lifecycle.patch`
3. `input-only/0003-input-only-execution.patch`
4. `chat-models/0004-feat-156-upstream-tool-choice.patch`
5. `chat-models/0005-feat-156-terminal-tool-arguments.patch`
6. `chat-models/0006-native-web-search-sources.patch`
7. `chat-models/0007-feat-164-kimi-k31-pro.patch`
8. `chat-models/0008-feat-164-kimi-responses-include.patch`
9. `chat-models/0009-feat-164-native-failure-terminals.patch`
10. `chat-models/0010-feat-164-sanitized-persistence-metrics.patch`
11. `chat-models/0011-feat-164-graceful-state-close.patch`

以上相对路径均位于`.yijie/patches/`。根目录历史`0003-feat-137-*`、`0004-feat-137-*`不在此r5表中，不因旧README段落仍存在而恢复其工具或执行路径。input-only补丁只在`config.input_only`时将可见/可执行工具表置空（补丁`:668`—`:678`），不能将“源码里有工具”误称为所有模式下可调用。

负向查找范围包括`codex-rs/core/src/tools/{handlers,spec_plan.rs,registry.rs}`、`app-server/src/request_processors`、`app-server-protocol/src/protocol`、`exec-server`、`ext`、相关`Cargo.toml`及`.yijie/patches`。搜索Office/PDF/HTML/viewer/artifact关键字后回到命中代码核对注册与行为；技能样例里出现`.docx`或`.pdf`不算存在阅读器。没有检查或声称掌握上游未导入的商业客户端/云端私有实现，也没有为找能力加载个人外部MCP配置或凭据。

## 3. 原生能力与用户预览的区别

下表路径均相对`yijie-codex/`。代码存在与当前配置可用是两件事；本轮只确认源码及固定候选包含的机制，没有实际调用工具。

| 能力 | 实码证据 | 已有行为与FEAT-166复用边界 |
|---|---|---|
| `exec_command` / shell / `apply_patch` | `core/src/tools/spec_plan.rs:629`、`:738`；`core/src/tools/handlers/mod.rs:2`—`:37`（以上均在`codex-rs/`下） | 复用Runtime正常任务执行、工作区文件生成和原生事件，不新造文件生成执行器。点击预览不是新的模型任务，不应为了阅读再调用shell或模型 |
| app-server `fs/readFile` | `codex-rs/app-server-protocol/src/protocol/common.rs:743`—`:753`；`v2/fs.rs:7`—`:22`；`app-server/src/message_processor.rs:958`—`:962`；`request_processors/fs_processor.rs:64`—`:78` | 已有绝对路径读盘→`dataBase64`字节服务，不是格式解码/页面阅读器。该请求没有易界session/turn/artifact/message授权语义，不能让renderer传任意路径来替代现有Native产物授权 |
| 原生filesystem抽象 | `codex-rs/exec-server/src/{local_file_system,sandboxed_file_system,remote_file_system}.rs`；`fs_processor.rs:44`—`:49` | Runtime已有环境文件系统，不重复发明运行时文件访问栈；预览本地已提交加密产物仍沿易界Native读取，不能绕回工作区路径改变真相源 |
| `view_image` | `codex-rs/core/src/tools/handlers/view_image_spec.rs:15`—`:48`；`view_image.rs:151`—`:201`；注册`spec_plan.rs:750`—`:758` | 按环境sandbox读取图片，生成`ImageView` item及模型图片输出。是模型视觉输入，不是PDF分页、Office阅读器或用户侧文件预览；本需求排除顶层图片，不新增调用此工具的预览路径 |
| MCP工具注册和分发 | `codex-rs/core/src/tools/spec_plan.rs:855`—`:880`，`handlers/mcp.rs` | 已有适配框架，若既有已接入工具产生文件，继续使用原producer/ID/事件；框架可分发不表示内置了每一种文档工具，不为预览新增第二套MCP体系 |
| MCP资源读取 | `spec_plan.rs:669`—`:674`；`handlers/mcp_resource/read_mcp_resource.rs:28`—`:120`；app-server `common.rs:978`—`:987` | 调用已配置server的`resources/read`并返回text/blob结果，读取能力由该server提供；可以复用已存在且获准的资源链，但它本身不把PDF/Office变成页面，不自动授权新增外部server |
| 动态/扩展工具 | `spec_plan.rs:886`—`:928` | 接入外部定义的工具/执行器，受模式及配置限制。不能把能力入口当作已封装Office预览，也不能为了FEAT-166解禁当前配置中关闭的工具 |
| MCP App上下文 | `codex-rs/app-server-protocol/src/protocol/v2/item.rs:301`—`:318`、`:401`—`:407` | `appContext.resourceUri`等为下游小部件/工具来源元信息，不是本仓自带的本地Office阅读组件；不能将任意URI直接加载进具有宿主权限的右栏 |
| Apps文件参数桥接 | `codex-rs/core/src/mcp_openai_file.rs:1`—`:12`、`:112`—`:118`、`:152`—`:176` | 对声明`openai/fileParams`的外部工具，将本地文件上传OpenAI文件存储并改写参数；需要ChatGPT auth。不是本机只读预览，FEAT-166不得为了“复用”自动上传用户文件 |
| 图片生成产物 | `codex-rs/ext/image-generation/src/tool.rs:182`—`:210` | 已有imagegen结果落盘/Item机制，但属于图片生成和外部服务，不是通用文档预览或本需求调用理由 |
| DOCX/PPTX/XLSX/PDF正文/页面阅读器、HTML用户右栏 | 上述注册表、handler、app-server/fs/MCP实现及扩展/依赖范围内未发现对应格式renderer或viewer | 当前fork核对不能提供可直接搬入右栏的阅读UI。不得声称“Codex产品能预览，所以这个Runtime fork必然已有相同组件”，也不得据此重写已有产物基础机制 |

## 4. 必须复用的易界端到端链

与Runtime核对同时，主审按当前兄弟仓源码确认既有产物接入链（详见03及FEAT-165）：

```text
固定Codex正常任务/既有生产工具产生文件
  → 已有 yijie_artifacts.publish_artifact 或原provider产物路径
  → Host既有登记、来源校验、加密暂存与资源流
  → Desktop Native校验、加密持久提交后ACK
  → 已有artifact_reference / 真实消息附件绑定
  → 同一Native授权读取与TTL/完整性检查
  → 本需求右栏与对应内容阅读适配
```

- publisher现有入口：`yijie-agent-host/artifact-mcp/src/main.rs:52`—`:101`。不新造第二个publish工具，也不为每个文件格式注册一个模型工具。
- Host接入/资源链：`yijie-agent-host/internal/session/artifact_media.go:154`—`:257`；v12沿用既有v9资源机制。保留artifactId/provenance、幂等、容量、暂存/ACK边界，不由对话正文或路径扫描补登记。
- Native提交后ACK：`yijie-desktop/src-tauri/src/chat/artifact.rs:523`—`:566`。预览不能把Host staged当成本地ready，不重新下载/登记已提交原件。
- 同一授权读取：`yijie-desktop/src-tauri/src/chat/artifact_file_native.rs:412`—`:455`及既有私有schema。继续以context/session/turn/artifact身份读取；已发送附件维持独立message/attachment绑定，不能冒充artifact ID。
- 现有文本/表格投影与HTML隔离实现、文件结构验证、图片有界解码和Native资源生命周期优先复用。新标签和栏宽只属于展示层，不能重建Turn/Item状态机或改变原生userMessage。

## 5. 经核对后仍需补齐的最小边界

1. **页面容器与交互：**右侧栏、多标签、拖动分割、只读工具条和焦点规则是Desktop展示适配，不是Runtime模型工具。
2. **HTML同页只读承载：**复用已有隔离策略、授权原件、资源释放原语，补同页承载和禁业务操作；保留内联渲染能力。先比较已有载体/宿主能力能否直接复用，不先预定新增Native command或插件数量。
3. **Office/PDF阅读适配：**Desktop已有`zip`、`quick-xml`、`pdf-extract`和文件预检/提取基础；必须优先复用，不能将给模型的扁平文本当已实现结构化阅读。DOCX段落/表格、PPTX真实页序、XLSX真实单元格与PDF页面输出属于需要补证/补齐的阅读层。优先接入可用的成熟本机阅读/页渲染能力或已有解析原语，不能从零写一套完整办公引擎；具体依赖/载体尚未选定，不在本轮安装。
4. **已发送附件读取：**复用现有附件加密存储、校验和真实消息身份；仅在现接口无法提供该绑定下阅读时补窄接口，不能扩成任意文件服务器或扩大草稿读取含义。

若实施调查发现已有封装能完成某一条，必须改为直接复用并更新本矩阵；“未发现”不是允许忽略后续证据的永久结论。每项新增代码前应能回答：已有入口在哪里、为何不能直接用、最小缺口是什么、如何验证继续使用原产物/授权链。新增阅读器不得独立接管生成、MCP发现、存储、传输、审批或Runtime协议。

## 6. 未执行与下一阶段证据

本轮没有执行`make build/generate/runtime-test`、patch应用、Runtime握手、MCP工具、模型、文件脚本或外部服务，也没有改变Runtime pin、补丁、配置、权限或二进制。仓库源码检查不代表任何新格式或真实预览已通过。

后续验收应确认：点击预览不会触发模型/重生成/重复publisher；生成产物仍是原artifact ID和Native已提交字节；授权、TTL、完整性、资源配额与原回收规则保持；新Office/PDF只补阅读输出。所需契约以实际边界的权威源先行；若无需Runtime协议变更，`yijie-codex`继续只读且无新patch。任何新的Runtime核心/协议改动都必须先证明必要性，不能以“复用Codex”名义绕过现有稳定链路。
