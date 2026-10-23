# 双来源进度恢复、真实复测与来源链路扩展（2026-10-23）

状态：本轮实现、标准启动与真实验收完成；四项过程展示及原生搜索来源链路通过，模型独立进度和答案逐条引用仍未产生，不标为通过。用户明确恢复任务，授权非破坏性排查、标准启动、Kimi-K3 完全访问原题验收及必要修复。
本轮证据：`CrossBSD/.local/audits/dual-progress-resume-20261023/`；起始各仓 HEAD、状态及文件哈希见 baseline.json。
没有提交、推送、强杀、故障注入、攻击 fixture、权限破坏或替换既有固定 Runtime。

## Docker 与真实回合

原 Coze/MySQL 退出码 137，OOMKilled=false；仅凭该事实不能断言退出原因。复用 Infra 已有
`workflow-recovery-plan` / `workflow-recover`，恢复 ID `1b3189eb-c1db-4262-8365-588cb07b2f05`。
四份停机数据副本、原身份和退出状态已保存；只读存储审核、原镜像健康启动和正常停止通过。
随后 canonical App 启动完成。没有删除数据卷、重置数据集或绕过异常门禁。

第一轮 09:06:29（北京时间）：原题、kimi-k3/max、never/danger-full-access。
Desktop `01a1664b-8cff-79d0-b23a-89dc73f02496`；Runtime `01a1664b-8d38-7d63-9ef3-333ddfc820cc`。
出现 10 次原生搜索、9 次用于播报的 echo 命令、0 条 assistant 答案，约 94 秒后通过“停止生成”正常中断。
这是失败验收，不能将这些命令表述为有效研究；所有真实记录保留。

Host 普通指令移除“必须先发独立进度”，说明产品已经显示真实执行进度；禁止通过播报命令触发
另一轮响应，证据不足且没有有效检索操作时应说明限制。复用原有 baseInstructions 链路，
不改变工具集、权限、计划器或原生执行。此项 `contract-impact=none`，不改变 wire/持久化语义。

复测 09:11:50：Desktop `01a16650-6fda-7c02-9ff9-30c874fc4831`，Runtime
`01a16650-7045-7851-be02-32f8f6b82bf4`。22 秒完成，一次真实 Provider 请求、一次网页搜索、
零命令、一个空推理条目、一个最终 assistant。界面实际显示带来源标识的执行进度，搜索可展开，
没有新增未知卡片、重复摘要或空命令噪声。被动观察确认新指令已到达 Provider；最终文本
2913 UTF-8 字节，SHA-256 与 Runtime 保存文本完全相同。独立模型进度、URL、annotations、
url_citation、搜索 sources 均为零；因此引用验收尚未通过，不能将其归为前端漏显。

观察器是既有开发回环入口：响应字节原样转发，记录计数/哈希，不记录正文或凭据；单请求
输出上限 8192 token，批次上限 4 个 HTTP 请求，当前第一条复测消耗 1 个。原直连失败回合另计，
不能用该 ledger 声称它也只消耗一次。观察器已在请求结束后正常 Ctrl+C 关闭。

## 原生搜索来源扩展

官方 [Kimi Responses API](https://platform.kimi.com/docs/api/responses) 说明内置搜索由服务端执行并注入模型上下文，
`include: web_search_call.action.sources` 可额外返回命中页面。固定 Runtime 原先没有请求或完整投影该字段。

整个扩展 `contract-impact=breaking`：Runtime 添加可选字段，但闭合 Host/Native/存储 reader 必须版本化。
Owner 为段成威；producer 为固定 yijie-codex 的 canonical app-server，consumers 为 Contracts、Host、Desktop。
只限未发布 `demo_fast + local` 候选，不冒充独立人工批准、生产兼容或已发布版本。

顺序：可重放 0006 patch / 独立 Runtime 构建及 canonical schema → Contracts 精确来源候选 → Host → Desktop。
保留旧固定产物与上游子树；复用现有构建器、manifest、codegen、SSE、唯一 NativeDisplayBuffer 和 SQLCipher。
无新搜索代理、planner、自动追问、执行引擎或旁路模型请求。

- Runtime 仅为有内置搜索工具的 kimi-k3 请求增加 sources include；WebSearchAction 保留实际 URL/title。
- Host history v4 / SSE v11，旧 history v1/v2/v3 和 SSE v7/v8/v10 继续按原封闭格式降级。
- 来源最多 32 条，URL/title 有界；拒绝凭据、控制字符与敏感模式，使用已有秘密检测器；地址不改写成另一个链接。
  命令输出的保守脱敏器完全保留，不能借此扩大命令输出范围。
- Desktop IPC v4 / storage format 4，保留严格的旧格式 reader，未来格式继续拒绝；不迁移重写旧 JSON。
- 网页活动详情用惰性纯文本显示“搜索来源”，说明其不等于回答逐项引用或核验。未提供来源时如实显示缺失。
  不生成引用、不修改最终答案、不新增外部打开权限。

回滚保留原 binary；新格式记录必须使用兼容 reader，禁止降级写入或删除数据。既有 v3 来源和生成物
继续参与校验，避免在新版本生成时丢掉旧 reader 的来源验证。

## 验证进度

- 双来源展示前轮 61 项定向测试已通过；本轮来源扩展的前端 7 文件 246 项通过。
- 旧 v3 与新 v4 契约普通样例 5 项通过；Host 原生投影、来源保留、版本降级和路由权限定向检查通过。
- Runtime 普通 source 解析/原生映射 2 项通过，独立 release 构建进行中。
- Native 新旧 reader 普通测试通过；原生跨仓字节交换、正常重开及最终真实验收待记录。
- 历史未筛选全套攻击/故障测试不运行；未执行项目不计 PASS。

最终结果必须以随后新增的构建、兼容和真实验收记录为准，不能把上述进行中状态当作整体完成。

## 最终真实验收与边界

09:43:03（北京时间）使用标准构建、Kimi-K3/max、完全访问，再次发送未改写的原题。
Desktop `01a1666d-04fd-7ba0-8c67-aa0f38bfd13c`，turn `01a1666d-0588-7121-b78b-3daf994e0c63`。
40 秒完成，1 次搜索、0 条命令、1 个空 reasoning、1 条最终 assistant。Provider 请求 include 已包含
`web_search_call.action.sources`，真实返回 13 条来源；Runtime 的 13 个 URL 哈希与 Provider 全部一致。
最终文本 4221 UTF-8 字节，Provider/Runtime 哈希一致。独立 commentary、正文 URL、annotations 和
url_citation 仍全部为零；来源展示不是逐条引用的替代证明，也未对答案数字做全面事实核验。

Host 保守安全筛选后显示 7 条来源；正常退出、关闭观察器、重新标准构建为直连后，这 7 条仍可读取。
UI 的 7 个 URL 都是原生实际返回的地址，未改写地址或补链接。过滤不证明其余 URL 确定包含秘密，
普通长 URL 也可能被保守模式过滤；显示 availability=partial，执行状态仍为完成。
已将完成搜索的该说明移入详情；不可用/异常信息仍按原规则显示。

| 验收项 | 结果与实际证据 |
| --- | --- |
| 执行进度 | 真实开始时显示等待说明，搜索完成后显示带“执行进度”来源标签的客观段落；没有计时编造研究结论 |
| 模型进度 | 支持真实模型消息独立展示，普通单测通过；本轮 Kimi 未产生，真实分支未触发，不算真实 PASS |
| 网页搜索 | 新回合识别为网页搜索，查询与实际来源可展开；无新增未知内容卡片 |
| 重复摘要 | 原始问题会话 `01a163b5-cb07-78f1-affc-a77e0e613418` 真实回看通过：默认在详细过程，重复摘要折叠且原文可查看 |
| 空命令 | 同一旧会话真实回看通过：默认在详细过程，展开保留 0 毫秒、退出码 0 和“命令已结束，无可显示输出”；记录未删除 |
| 旧未知记录 | 原始已保存未知条目仍在详细过程，不根据旧问题反推搜索或补造来源 |
| 引用/来源 | 13 条原始来源保留、7 条安全投影与 UI 地址逐一匹配；答案逐条引用未产生，不能标为引用充分 |
| 正常重开 | 最终直连构建能读取新旧格式；搜索来源与答案保留，没有冷历史伪运行 |

旧会话的 9 条详细记录仍保留；本轮没有将推理摘要改名为模型进度。代码与截图中的系统说明均明确来源，
与 Codex 截图里模型亲自写出的叙述仍有区别。此差别由上游实际输出决定，不通过前端文案伪装消除。

## 最终检查与产物

- 前端 7 文件 **247 项通过**；ESLint、vue-tsc、文档构建、Native Clippy 和 fmt 通过。
- 契约旧 v3 / 新 v4 普通检查 **5 项通过**，生成和同步检查通过；OpenAPI lint 通过，保留两条既有形态的未使用组件提示。
- Host 定向投影、来源字段、版本降级、鉴权/no-store、producer conformance、go vet 通过。
- Native **8 项定向检查通过**（显示生命周期 5、旧格式/未来格式 1、v3/v4 source reader 1、跨仓正常重开 1）。
- Runtime **6 项定向测试通过**（既有流参数 4、source 解析/映射 2）；补丁重放和反向还原 18 个文件逐字节一致，normal-EOF 握手通过。
- 新 release binary SHA-256：`9766d7e10d25327f0595964a19ad67e1e1c1db0c22e5a65f9af66b547ab316c6`。
  269 个 canonical schema，21 个仅含来源扩展。最初 schema 对比器未处理聚合文件的 v2 命名空间而拒绝；修正对比器后独立检查通过，未重新改写 binary 或关闭门禁。构建日志中这次非零退出保留，不冒充原脚本首次全绿。
- Runtime 首次包含依赖的 Clippy 被未修改的 core-plugins large_enum_variant 阻断；针对四个修改包的 `--no-deps --lib -D warnings` 通过，不称全 workspace Clippy 通过。上游 app-server unused_mut 构建警告保留。
- 旧 v1/v2/v3 源契约与恢复基线哈希一致；未改固定上游子树、旧 Runtime 产物、既有权限或事实记录。
- 亮色原生窗口与 **1180×760** 最小窗口实际检查通过，原窗口尺寸已恢复。暗色原生视觉未执行：应用跟随系统外观且无独立切换入口，本轮未更改用户全局外观。
- 观察器正常退出，无 18083 listener；两个被观察回合共 2 个 HTTP 请求，首轮直连中断回合单独记录。
  最终应用使用 canonical 直连运行并保留最新验收会话；无新模型请求在途。
- 所有仓库 HEAD 未改变，没有 commit/push/tag/发布。旧未提交工作保留；详细变更、来源哈希和截图位于本轮证据目录。

关键证据：`sources-summary.json`、`ledger.json`、`final-history-sources.ax.txt`、`final-history-process.png`、
`minimum-sources.png`、`legacy-details.ax.txt`、`legacy-empty-command.ax.txt`、`source-cross-repo.log`。

未执行：攻击/故障注入、强杀、权限破坏、历史未筛选整套测试、生产发布与全量事实核验；本地定向通过不替代这些项目。
结构化 output_text annotations 通道未在本轮扩展，因为所有实测原始响应均为零；将来上游若实际返回此类注解，仍需沿原生权威和版本化协议接入。
