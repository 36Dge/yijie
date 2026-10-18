# 第五组：跨境电商爆款视频复刻专家接入

2026-10-17，demo_fast + local。用户指定剩余三位中的视频复刻专家，复用现有专家架构和LinkFox；保留原专家/历史，深入代码审计与全量lint，无账号真实验证继续跳过。

## 方案回顾与实施边界

完整回顾17的九节及18—23累积结果，核对原专家ROLE/知识精确引用→Skills安装收据→Native绑定/outbox→Host普通基线合成→当前连接器选择/审批→Tool历史。当前49资源（38普通+11专家版本）、8原生+3展示、60连接器revision9，SQL35/Host10；均复用，不增加数据库、专家团、Runtime逻辑、第二套任务引擎或OAuth服务。

`contract-impact=semantic`：视频卡从展示转为可准备/绑定的版本化资源，新增内容行为和本地部署pin；experts/1、manifest v3、market协议/目录、权限/审批/搜索策略均不变。Skills为本次权威源，规范打包新增0.1.0；原49项、所有已安装版本与历史引用保持。Contracts本轮无源改动，不重生成无关族，也不重新宣称修复上一组全局breaking历史远程schema EOF；当前生成一致性仍须检查。发布/回退须同步兼容Host/Native与新bundle，保留旧包和旧绑定，不用全局专家开关冒充只停用新增专家。

本机视频原包2.2.0共22文件，导出与WorkBuddy缓存重新枚举、SHA256逐项一致，原文件不执行/修改。其4个子技能收敛为单SKILL/ROLE、分镜/商品事实/替换/异步结果参考与无网络脚本。视频来源、商品图、可见事实、模型、5/10/15秒、比例、清晰度、声音、Pro选项均显式；生成前展示替换计划，每次调用沿现有审批。参考视频/商品分析/替换提示词的三个文本任务与最终视频任务各自记录真实taskId，查询从原Native工具历史恢复，不靠本地JSON产生执行权限。

接受已授权公开HTTPS媒体直链；可选用户已准备的8—10张公开帧图与单调时间戳，仅做无音轨的近似分析。原任意下载/ffmpeg脚本、公开PUT、隐式上传、默认反馈不引入。没有直链时明确缺输入；视频理解失败不自动抽帧上传、不切full、不改HTTP或换模型重试。交付实际服务结果链接，未下载不声称本地MP4，未查看不声称质量/保真通过。自动本地上传、下载、剪辑/BGM和抽帧上传尚未实现。

公开来源审阅：LinkFox官方仓库树 `ea5581c8c727f259a4fa5ea3df00e7cec77bf5ce` 的textgen/video API/model-config与本机MCP包并不完全同一接口配置。当前公开HTTP文档使用GEM名称，而安装MCP子技能写LF_GEM；没有凭据和真实schema时不推定等价、不自动映射。原包给SEED_FAST透传isPro=true，但底层明确不支持，本版拒绝该组合；同样不把1080p/宽比例静默降级。采用原包与公开文档均包含的窄子集：SEED/SEED_FAST、1—9图、5/10/15秒、9:16/16:9、兼容清晰度、prompt≤2000字符。实际调用还需当前工具schema/供应商能力确认，未在线资格化。

证据根：`yijie-desktop/.local/fifth-group-video-20261017`，含7仓开始状态/diff/摘要、22文件来源验证、公开官方文件固定树与摘要。无真实OAuth/模型/业务API，GET仅用于公开文档核查；本轮不替换正在运行的App、不写日常数据库、不提交推送。

## 接入后的深入代码审计

同一Codex在实现后单独复读代码与协议，不冒称独立人工审批。审阅本组14份运行文件、22份原资源的文本/脚本与头像摘要、全部增量及其调用的已有核心路径。没有把整个Runtime、全部第三方代码或真实服务列为本次完整验收。

| 层 | 实际复核 | 处理与结果 |
| --- | --- | --- |
| 唯一资源入口 | 新 `video-replica/ROLE.md`、SKILL、索引/参考/例子/checklist/eval | 4个原子技能重组为单一受管专家，不全局注册或动态加载WorkBuddy插件；角色/索引不扩大权限。 |
| 参数与内容 | `scripts/prepare_video.py` 的prepare/compose/video | 参考视频和主商品图分开；三阶段真实文本回执独立、同制作单SHA匹配，重复任务或错配停止。最终只取私有JSON的video_prompt，保持换行、商品主体与参考图顺序，不把替换表/整个JSON当prompt。 |
| 时长/模型 | brief校验与video_options | Auto需要可靠已知时长，未知不猜；SEED_FAST禁Pro/1080p，不静默降档。参数范围明确窄于当前公开服务完整目录，实际MCP资格仍待账号确认。 |
| 事实保真 | analysis参考、构参提示词、ROLE | 商品外观/用户事实/未知分开；不伪造材质、尺寸、认证、价格；帧图不能听音频，不通过可读口型“确认”口播。未播放实际视频不得报保真或声音质量通过。此为规则和代码审查，不是模型质量PASS。 |
| 异步回执 | observe/payload | MCP→代理/业务→taskId→状态依序核对；text层JSON只解一次，prompt中的显式私有JSON另行解析。created≠生成完成；PROCESSING待显式继续；FAILED/未知/空结果/类型错配不重建。视频结果仅接受实际video URL，不造MP4路径。 |
| 审批容量 | proxy_request +既有Broker源常量 | 复审发现两段较长中文分析合并可能超过既有16 KiB参数容量；新增按完整JSON UTF-8字节预检查，超限停止并保留原回执，不截断、不重发、不改Broker门禁。普通长中文输入回归PASS。 |
| 资源安装与历史 | Host `internal/skills/experts.go`/`expert_resources.go`、session生命周期；Native `skills/catalog.rs`/`experts.rs` | 只更新精确manifest pin与本地测试期望；ROLE/knowledge/archive SHA、receipt、原Core journal、retained保护、旧新版本共存机制不变。50资源中38普通Skills投影不变；专家仍expert_only。 |
| 选择/发送 | 原Native目录、useExpertSummon、专家store/outbox、Host `expert_instructions.go` | 9位原生+2位展示，共11，无专家团；移除同ID展示卡，保留本地头像与三列样式。快捷问题仅准备/预填不发送，旧目录/错误不伪造原生卡。 |
| LinkFox执行 | `generic.rs`/`broker.rs`及固定registry/OAuth策略 | 生产注册/鉴权/审批完全未改；新增cfg(test)视频协议测试。现有schema冻结、安装与scope精确绑定、write风险和ApproveOnce、一次网络许可保持；拒绝0执行、批准1次、重复consume拒绝，旧Sorftime测试保持通过。 |
| 权限/数据 | 现有ask、web_search disabled、SQL35/Host10、Runtime | 无新数据库/表、后台轮询或任意网络脚本。源码摘要确认Contracts全部531个基线文件和Runtime5575个基线文件未变，Runtime Git干净。日常数据库与运行App未操作。 |

原抽帧脚本具有任意HTTP下载、依赖探测和无界外部进程执行，上传脚本具有public-read PUT；本组排除这些代码，复用上一组公开直链边界。用户已准备帧图的分析只处理其URL/时间索引，不宣称完成原包全自动抽帧上传。URL格式检查不证明公开可达性、素材版权、实际媒体内容或模型支持。

本地制作单摘要、source_operation_id和回执检查仅防止操作混用，不能证明服务器来源、用户授权或服务取消。Native原始Tool历史仍为执行事实；机器逐次审批仍在Broker，不用提示词或本地JSON替代。无账号下只能检查本地协议和结构，不能据官方公开HTTP参考推断当前MCP帐号可用。

实现期两项普通检查失败已修复并保留日志：首次来源审核记录遗漏canonical要求的decisions字段，补全真实本机授权与未核实再分发声明；Native测试新增身份时误合并成三元tuple，拆成正确独立二元组。没有放宽打包器/Native检查。后续UTF-8容量修复重新打包、更新pin、冻结Host来源并重跑受影响检查。

## 实际检查结果

所有检查遵循用户长期安全条款，仅正常输入、正常拒绝、临时/内存数据库、in-process MCP和正常关闭。没有强杀、权限破坏、可执行替换/劫持、攻击资源或危险归档。宽泛历史测试中含这些场景的部分未执行，不计PASS。

| 项目 | 结果与证据（证据根下） |
| --- | --- |
| Skills全量lint/test | PASS；`skills-final.log`：45测试，80条合成eval格式；新12项视频helper测试含完整构参→实际形状回执→合成prompt→视频参数/链接、长中文16 KiB边界；不计真实模型Eval。 |
| Host全量lint与实际包测试 | PASS；`host-audited.log`：最终50资源、12专家版本的安装/精确读取、原39资源升级保留、Core journal生命周期、3组历史版本共存，4组race测试。新专家实际包安装于临时测试根。 |
| Desktop全量lint | PASS；`desktop-lint-audited.log`：`make lint CONTRACTS_DIR=.local/demo-fast-contracts`，完整generate一致性、ESLint零warning、vue-tsc、cargo fmt、all-targets Clippy。沿用工程合法的历史干净Contracts来源验证旧锁；当前候选来源仍单独精确核验。 |
| Native实际资源与目录 | PASS；`native-functional-final.log`覆盖目录/未授权LinkFox不能启用；UTF-8修复后的最终包重跑在`native-audited-bundle.log`，实际50项加载、9位最新专家精确身份、普通38项隔离。 |
| 当前Host/资源来源 | PASS；`source-freeze-final.log`、`current-preflight-final.log`，canonical冻结后校验实际Host源码、专家资源、原38普通包及既有权限/FEAT-137永久退役权威。FEAT-137历史acceptance NOT PASSED未改写。 |
| Connectors全量lint | PASS；`connectors-checks.log`：Go vet/catalog race、固定Runtime库来源、Rust格式、worker Clippy；新增测试文件另做rustfmt check。 |
| LinkFox普通协议/审批 | PASS；`worker-functional.log`共7项，包含新四任务九次显式调用的in-process视频流程、上组图片流程与metadata、LinkFox/Sorftime一次审批及60注册/header检查。无账户、真实网络生成或付费操作。 |
| UI与前端构建 | PASS；`ui-build.log`：4文件78测试及pnpm build，既有大chunk提示保留。无CSS/布局组件改动，无真实App主题/最小窗/E2E验证。 |
| Contracts与元仓 | Contracts全量lint PASS，`contracts-checks.log`；元仓pnpm lint/50测试/shell语法PASS，`meta-checks.log`。本轮Contracts无增量，不重跑或冒称清除上组全局breaking的3个历史远程schema EOF阻塞。 |
| 原数据/资源 | `preservation-final.json`：原49条manifest与49归档字节相等；日常已安装9专家版本逐文件匹配对应canonical档案；9原Runtime会话文件、110旧资源/收据摘要保持。未打开日常数据库写入，不对动态WAL作伪造一致性结论。 |
| 工作区 | 7仓git diff --check PASS，HEAD/分支未改，无提交/推送；`baseline.json`、`increment-source-changes.json`、`final-repository-state.json`。Contracts/Runtime和连接器生产授权/注册/审批字节保持见`architecture-source-preservation.json`。 |

## 最终候选与后续

- Bundle `0.9.0`，路径`yijie-skills/dist/skills-experts-fifth-group-v010`；50资源=38普通+12专家版本，9位原生专家+2展示。
- Manifest SHA-256：`843b38bd3b079243d6093271f5ef0f8fa7f6cfc93c8c98146f2ef27f572b097a`。
- Authority SHA-256：`6dce01a3a104aa4a4a03827bab0f9bc8afb51175c081e19871b4d00467f44bb1`。
- 内容源树：`eb74cabcc18cf97814547bd77d377554ef5ef69c8ad7365dcdabae614a2d1b24`；expert Contracts source lock继续为`fe49fb6cd83e11dba69861025a23a8faf1d9d3740c887c1716a3637eb34154cb`。
- 新专家`linkfox-expert-aigc-videogen-viral-replicate@0.1.0`，原八位及历史版本保留，共十二专家版本；未新建连接器，目录仍60/revision9。

这些是release=false本机工作树候选，不是发布或在线功能合格证。未替换运行中的App，源码目录不等于当前正在运行的旧二进制已更新。

按用户指令NOT RUN：真实LinkFox授权/资格、当前模型和额度、付费分析/视频创建、真实媒体质量/音频/时长、账号中原任务续查、App真实D4。没有凭据，不读取/搬用WorkBuddy登录态。尚未实现的本地上传/自动下载/自动抽帧上传在描述、ROLE和参考中已明示，未按“账号验证跳过”伪装为已实现。

剩余亚马逊1688找货源专家与行业研究员仍为展示态。后续按17审计分别处理来源匹配/利润缺值和数据/搜索/产物依赖，不能用本组视频协议合成测试替代其业务接入。
