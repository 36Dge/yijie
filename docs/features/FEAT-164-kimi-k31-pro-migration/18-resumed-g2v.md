# FEAT-164 恢复实施与最小 G2V（2026-10-25）

用户已明确恢复，继续按治理实施，沿用人民币 20 元总费用上限及搜索、图片授权；只本地提交，不推送，保留所有其它需求改动。17 是暂停时的历史快照，当前进度以本文件、feature.yaml 和实际证据为准。

## 来源与范围

恢复检查：Host `ff7d05dae4b3a48285e9bed63ba7253081da234c`、Desktop `3dc2205fba79a0a1d7fdea8a4b767d35f2c286b1` 与暂停时一致，进入暂停前记录的工作文件摘要未改变，index 为空。

本轮新增 Desktop 本地提交：

- `0cbb950817ce05bdd79d969bce88c33c066d834c`：Host build pin 由 Git 对象固定到 `ff7d05dae4b3a48285e9bed63ba7253081da234c`，构建时分别验证 Git 源与实际文件，拒绝工作树漂移。
- `8aaa8be1764030f58b0445ada8dfbabb4e7a4ecc`：独立 G2V 费用计量器及 6 项无外网普通状态测试。没有编辑其它需求的旧 K3 meter。

独立验收工作区为 `CrossBSD/.local/feat164-qualification-20261025`，Host/Desktop/Contracts 均采用完整提交的 detached worktree；原工作区不切换分支、不清理。普通安装依赖及项目标准 Cargo 编译缓存可复用；没有运行时程序替身，也没有故障注入。来源详情见 [隔离工作区](evidence/g2v-isolated-workspace.json)。

第一次 canonical prepare-only 在生成器依赖解析处停止，没有启动 App 或模型调用。补齐与原 package/lock 字节一致的既有生成器依赖后重新构建，不跳过来源检查。原日志 `g2v-clean-candidate-build.log` 保留。第二次在独立工作区要求固定 Skills checkout 处停止，未启动 App；已找到原项目已有、干净且精确为 `10c45bec29603b002e861e1499d5b4e684251af5` 的 checkout，通过标准 `YIJIE_DESKTOP_SKILLS_DIR` 指定复用。第二/三次分别见 `g2v-clean-candidate-build-02.log` 和 `g2v-clean-candidate-build-03.log`。两次是不同的依赖/来源前置失败，不是产品或供应商调用失败。

## 已批准预算的操作边界

20 元是此 FEAT-164 批次累计上限，不是每次请求上限，不复用 FEAT-162/163 账本。最小 G2V 自限为最多 4 个普通用户回合、8 次全部模型 HTTP、1 个含图请求；包括辅助调用/重试。费用上限或证据未知会更早停止，不为了用完额度追加任务。后续改变细分限额仍须保留同一累计费用账本。

当前计量器只转发 `kimi-k3.1-pro / max` 的同步流式 Responses 到固定 `https://api.moonshot.cn/v1/responses`。只接受默认 5m cache，不使用 server-stored conversation、previous_response_id 或后台任务。请求先原子预占再出站，同时只允许一个在途；进程重开继承账本。缺少/异常 usage、未完成传输或未知终态不会按零计费，而保留全额预占并停止后续调用。正常停止通过受控 HTTP 接口和 server 自身 shutdown，不发终止信号。

2026-10-25 再次核实的[官方首页价目](https://platform.kimi.com/)为：K3.1 Pro 输入及默认缓存写入 13 元/百万 token，输出 68 元/百万 token，缓存命中 1.30 元/百万 token。本轮计量对全部输入按 13 元计，不扣缓存优惠，记录的是保守费用上界而非精确供应商账单。按 1,048,576 输入 + 8,192 输出的保守单请求上界预占 **14.188544 元**；剩余额度不足该预占值即不发送。

**本轮 G2V 是明确的预算受限文本/图片验证，不是原始请求或搜索资格验证。** 计量器将 `max_output_tokens` 限定为 8192，省略 Responses 原生 `web_search` 声明，并记录原输出上限、工具选择和调整类型；响应 SSE 字节不改写，prompt/answer/key 不进入账本。原因是默认输出上限较大，且 Responses 原生搜索独立计费上界尚未确认。用户的搜索授权保留，但本轮不把旧 Chat Completions `$web_search` 价格套用过来。图片生成、独立 Search/Fetch、商家平台工具和其它模型均不在此最小验证中启用。

省略搜索与限制输出的结果只证明最小真实模型→返回→持久化→重开方向；不能支持 S4 原生搜索、工具完整性、默认输出参数或全部 AC 的通过结论。后续必须用适用的原始产品请求独立验证这些能力。

## 安全 Harness 与当前门禁

继续使用已提交的 `scripts/feat164-verdict.mjs` 与测试：closed、content-free 布尔观测，四类失败与歧义区分，协作取消与恰好一次 cleanup。资格验证须包含当前不可变候选的 canonical App 普通本机正控和可回查的实际 UI/保存/重开/退出观测，再结合普通状态负控；不能只把布尔正例单测称为完整资格。

[预算控制日志](evidence/g2v-budget-controls.log)为 6 项 PASS，无 Provider 连接。完整 Harness 资格和真实 G2V 此刻仍未执行，不提前填写 PASS；真实费用仍为 0。完成相应步骤后在本文件追加真实结果。

## 07:34 实际进展与待解锁项

本轮进一步本地提交：`f0c04552c7a9344e935ffdfe622e0369bbd6a89c` 要求终态 usage 才释放费用预占，并仅摘要实际成功转发的响应字节；`9d35ba1` 增加每进程最多一次的候选启动阶段/现有错误码诊断，无正文、路径或凭据；`ba3ed160fc2c0bab04ccbe80c45457b30af233bd` 将不可变候选身份固定为 `com.yijie.ai.feat164-kimi-k31-r1`。元仓已以 `a0f2933` 固化此前批准的下游审计及恢复预算记录，未混入项目记忆中的 FEAT-163 段。

独立源码装配过程中，编译缓存软链接曾被 regular-file 来源检查拒绝。移除了本轮创建的链接，保持检查不变，改用独立普通 Cargo 输出目录；随后 canonical 构建通过。Contracts 的任务自建依赖链接也已改为按原 lock 离线安装的普通目录。三个隔离 worktree 均干净，App/Host 产物与精确来源见 [当前快照](evidence/g2v-r1-current-state.json)。

首次使用旧工作树候选的 App 数据目录时，本地服务未就绪；通过 UI 正常重试仍未发出模型请求，然后 App 正常退出（exit 0），fixture 正常 shutdown（exit 0）。只读核对发现旧候选的 Kimi managed catalog 指令字节与独立 Host 提交不同：旧目录继承了 FEAT-163 工作区指令，本 skeleton 的 fresh-only exact-file 准入不能接受它。见 [目录审计](evidence/g2v-candidate-home-audit.json)。没有覆盖配置、篡改数据或放宽准入；新 r1 身份建立独立数据目录，保留旧候选及日常目录。

r1 canonical 构建和同产物重开检查通过；原生启动后 `/readyz` 实际 HTTP 200，返回 `runtime_state=ready,status=ready`。普通 fixture `/health` 实际 HTTP 200，Responses 数为 0。当前 Runtime 握手已就绪，源检查、Clippy `-D warnings`、4 项状态控制及 6 项预算控制通过；共享文件反向核验保留原内容，见 [保留证据](evidence/g2v-diagnostic-preservation.json)。

尝试读取 r1 App 窗口时，CUA 明确返回 Mac 已锁屏且自动解锁失败。已请用户手动解锁，不索取密码、不绕过锁屏。**当前停止依赖 UI 的验收，G2V 与完整 Harness 正控仍 NOT RUN，不得据后台 ready 宣称通过。** 本轮没有启动真实计量器或真实模型请求，费用仍为 0；20 元授权保留。

当前保留就绪的 r1 候选和普通本机 fixture 等待解锁：exec App 会话 `44670`，fixture 会话 `49478`；端口分别 18086/18083。fixture 只给出明确标注的合成答复，无外部转发。解锁后先完成本机正控、正常退出和同产物重开，记录完整 Harness 资格，再按同一预算进行真实 G2V。若需结束，必须通过 App 正常退出与 fixture `/shutdown`，不强杀。已结束的旧候选/fixture 会话 `61687`/`29400` 不再使用。
