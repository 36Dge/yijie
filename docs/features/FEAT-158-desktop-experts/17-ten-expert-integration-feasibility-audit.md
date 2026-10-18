# 新增 10 位专家接入可行性审计

日期：2026-10-16。范围：现有资深电商运营操盘手的完整执行链、10 位 WorkBuddy 单专家原包、已导出的相关资源，以及易界当前连接器能力。用户已明确排除专家团。

**结论：可接入现有易界专家架构；不能把 WorkBuddy 原目录复制进去就认为原能力全部可用。** 目录、资源准备、单会话选择、发送、恢复和版本引用可以复用。需要逐专家转换资源格式、纠正原包冲突，并适配其实际使用的工具。三位 LinkFox 专家及实时 TikTok/行业数据能力存在实质外部依赖，当前不能承诺完整接通。

本轮完成调查和方案，不实施接入。`contract-impact=none`：只增加审计文档与本地审计证据，没有改变产品代码、资源包、跨仓协议、权限、持久状态或部署。此分类不能沿用于后续实现；原 FEAT-158 的历史验收和分类保持不变。

## 1. 审计对象与证据边界

当前 UI 是 **1 位真实专家 + 10 位展示专家，共 11 张卡片**。展示记录位于 Desktop 的 `expert-showcase-catalog.ts`，使用独立类型和详情组件，不经过安装、会话绑定和发送链。原有真实专家为 `jd-ops-expert@0.1.3`，资源包身份 `yijie.experts.jd-ops-expert`，bundle 为 `0.4.3`。上传的 WorkBuddy 原配置与易界已转换的 0.1.3 不是同一份运行配置。

本轮核对 10 份插件配置、10 份 Agent、42 份文件名为 `SKILL.md` 的子技能说明，以及相关 reference、配置、模板和关键脚本。导出清单中的 233 份原包文件共 10,730,547 bytes，逐一与 WorkBuddy 安装源及导出副本核对 SHA-256，全部一致；没有重新枚举安装源中清单之外可能新增的文件。关联资源另有 1,100 份（包含各专家独立保存的重复依赖）；本轮按调用关系核查必要依赖，没有重验全部关联文件摘要，**没有把全部第三方 vendor/混淆代码声称为已逐行审计**，没有执行这些资源。

完整原资源仍在 [10 专家资料目录](/Users/jack/Downloads/Personal_Info/易界文档/10专家)。原包用于来源保留；易界运行包应只纳入审阅过、确实可用的内容。资料齐全、结构校验通过、模型回答正确、平台能力可用是四种不同结论。

本轮基线：

| 仓库 | HEAD | 审计开始状态 |
| --- | --- | --- |
| yijie | `2c42db6cddddfa6eb44bfab8438f0818b3bb4ba9` | 干净 |
| yijie-desktop | `e2c201c3c154d636c87ff08bdab845cb94966cc7` | 有前序 UI、设计文档与展示专家改动，全部保留 |
| yijie-agent-host | `9acae49ee2bf1fb33ae1da8ef02fd0bd07538d63` | 干净 |
| yijie-skills | `d7a850c9d5c5f8e52b8ab8f631800f671acc60dc` | 干净 |
| yijie-contracts | `e35ae9a0711014e4774a1347413e9a343ce7ab2c` | 干净 |
| yijie-connectors | `23c31e8f3cd467916956e1bbdef428a334de0ca3` | 原有未跟踪 `.local/` |

可复核笔记：[执行链审计](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/expert-integration-audit-20261016/execution.md)、[资源与契约审计](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/expert-integration-audit-20261016/packaging.md)、[逐专家内容审计](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/expert-integration-audit-20261016/content.md)、[源文件校验](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/expert-integration-audit-20261016/source-verification.json)、[工作区基线](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/expert-integration-audit-20261016/baseline.json)。这些是本机审计证据，不是已提交或已发布附件。

## 2. 原有专家实际上如何工作

### 2.1 内容、身份与安装

`yijie-skills` 是专家内容权威源。原专家包含一个根 `SKILL.md`、一个 `ROLE.md`、16 项知识资源声明及来源审校材料；不是直接运行 WorkBuddy 的 `plugin.json`。规范打包器生成 archive、manifest、authority 和文件摘要；Desktop 与 Host 消费精确固定的来源。

Native 根据安全的 `expertId + version` 从可信目录解析资源，不接受页面上传 role、路径或摘要。真实 `ExpertRef` 固定专家 ID、版本、archive、role 和 knowledge-manifest 摘要。资源准备复用已有 Skills 安装器、receipt 和操作 journal，专家资源明确排除在全局 Runtime Skills 之外。

依据：[内容源](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-skills/plugins/yijie-desktop-skills/experts/bundle-source.json:13)、[Native 精确资源解析](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/skills/experts.rs:42)、[Host 准备资源](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/skills/expert_resources.go:48)、[资源身份契约](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/docs/experts-v1.md:61)。

### 2.2 选择、发送与角色注入

选择专家先准备资源，再绑定已有会话或保存新会话草稿；快捷问题只填入输入框，不自动发送。每个会话只绑定一位专家。Native SQLCipher 是绑定的产品权威；发送时在原消息/outbox 事务中冻结专家版本与绑定 revision，再复用原连接器提交链。

Host 每轮重新校验资源和 receipt，将“普通权限基线 + ROLE + 短知识索引”组成完整 `baseInstructions`。知识正文按需通过已有工具读取，不把所有文件一次塞入提示词。更换专家沿用同一个 Runtime thread，重组普通基线与新 ROLE/索引；解除专家才恢复普通基线。既有历史不因此删除，解除专家也不意味着模型遗忘旧历史。

依据：[召唤流程](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src/composables/useExpertSummon.ts:42)、[发送冻结](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/chat/experts/store.rs:403)、[Host 提交](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/session/market_submit.go:148)、[指令组合](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/expert_instructions.go:70)。

### 2.3 权限、恢复与原数据保护

专家不授予工具权限。当前 `ask/auto` 会话使用 `workspaceWrite + networkAccess=false`，`full` 使用 `dangerFullAccess`；不能将专家 manifest 的 `filesystem=read/network=none` 误读成 Runtime 所有模式永远只读禁网。外部连接器仍需要本轮有效选择、资格和审批，非空连接器选集目前只支持 `ask`。不应通过改成 `full` 来绕过接入缺口。

当前专家 v3 元数据只表达本地参考资源、无额外命名工具依赖；契约明确保留既有聊天/连接器权限检查。因此，**由用户授权的会话工具完成本地文件工作，并不当然要求创建新专家协议**。但若产品要声明必需依赖、据此判定“可执行”、自动安装/启用工具，或改变搜索策略，就必须先设计相应能力与准入语义，不能借空依赖字段隐瞒要求。

pending/unknown 会阻止新的冲突操作；恢复查询原操作身份，不自动重发。卸载和升级检查 retained 会话及历史提交引用，当前同一安装 ID 不支持多版本并存。本次扩容应保持原 jd 0.1.3 的所有资源字节、版本和引用不变，不重置数据库、不改旧 outbox、不用新版本顶替旧绑定。

依据：[权限投影](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/runtime_permissions.go:36)、[连接器选择限制](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/market_turns.go:69)、[能力声明含义](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/jsonschema/skills/skill-bundle-manifest-v3.schema.json:836)、[引用保护](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/chat/experts/store.rs:539)。

原模块已有工程验收和日常接入记录，但历史内容质量项 AC-007 已被移出验收范围；不能据此推断新增十位内容质量通过。见 [原日常接入](15-daily-client-integration.md)、[历史工程验收](14-final-engineering-acceptance.md)。

## 3. 真正需要处理的工程差异

| 发现 | 对接入的影响 | 建议 |
| --- | --- | --- |
| Native 目录支持最多 64 位专家；核心按集合处理 | 11 位容量不是问题，无需新 Agent 引擎、专家团或第二套存储 | 复用原模块，增加多专家切换与隔离验证 |
| Desktop 资源同步脚本仍断言 38 普通 + 1 专家，且专家必须是 jd | 新增包会在规范同步阶段被拒绝 | 改为核对受审专家清单，保留普通 38 项和原 jd 的完整性校验 |
| 十个原包均没有根级 `SKILL.md`；合计有 42 份嵌套 `SKILL.md` | 当前安装器要求唯一入口，禁止第二个/嵌套同名入口 | 转成一个根入口、一个 ROLE、按任务分类的参考文件；不能只改后缀就声称技能已适配 |
| 专家资源不进入全局 Skills；plugins/hooks/apps/multi_agent/js_repl 等关闭 | WorkBuddy 的 agents/skills/dependencies 不会自动装载 | 不依赖 WorkBuddy 插件生命周期，不轮流开关全局 Skill 来模拟会话专家 |
| 所有非空专家当前统一 `web_search=disabled`，注释仍以第一位本地专家为背景 | 依赖网页研究的专家会失去预期能力 | 如保留搜索能力，定义逐专家受控策略并做 source-first 适配；原 jd 默认保持原行为，避免按名称打补丁 |
| ROLE 与索引各 ≤32 KiB，knowledge 1–32 项、每项 ≤8 MiB且必须 UTF-8/无 NUL | 原包中图像、PDF/XLSX/PPTX、可执行二进制不能直接作为知识正文 | 文本知识进索引，模板/脚本作为另经审查的附属文件；所有原包大小均未超总体限制，容量不是主要阻碍 |
| 归档允许普通脚本文件，但没有插件依赖安装或执行注册 | 文件被打包不等于解释器、库、工作目录、输出预览可用 | 沿易界现有会话工具审查并验证脚本与产物；不顺带引入包管理器自动安装或改用宽权限 |
| 真实目录仅有 `iconKey`，展示目录有本地 `iconUrl` | 直接替换成真实卡会丢失现有头像 | 优先用受控 expertId→本地头像映射与既有图标兜底，无需让图片路径进入执行身份 |
| manifest 的 category 只接受 5 个现有分类 | WorkBuddy 的分类 ID 不能原样复制 | 显式映射到选品、市场研究、内容营销、流量广告、店铺运营等现有枚举；确需新增公共分类才先修改源契约 |
| 原 v3 专家分支是 `local-development`，分发状态为 `unverified` | 本机接入不等于可公开分发第三方素材/代码 | 每位记录自己的来源与本地使用依据；不得复用京东专家授权结论 |

关键位置：[多专家目录校验](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/src-tauri/src/skills/catalog.rs:315)、[单专家装配断言](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/scripts/sync-desktop-expert-resources.mjs:67)、[唯一入口校验](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/skills/archive.go:80)、[搜索策略](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/expert_instructions.go:42)、[资源读取限制](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/skills/experts.go:102)、[Runtime 插件配置](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-agent-host/internal/codex/market_runtime.go:147)、[分类枚举](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-contracts/jsonschema/skills/skill-bundle-manifest-v2.schema.json:128)。

## 4. 十位专家逐项判断

下表是按本地材料与当前代码得出的工程判断，不是已经完成运行验证。“可先接入”均包含内容适配与正常验收，不能理解为现在已经可执行。

| 专家 / 原版本 | 可以保留的核心 | 完整能力的实际缺口 | 建议位置 |
| --- | --- | --- | --- |
| 小红书爆款笔记策划 / 1.0.0 | 标题、选题、笔记结构、文案和标签；纯 Agent，无子技能 | 趋势与平台事实不能由提示词凭空变成最新数据；不要把发布也纳入承诺 | 第一组，最接近现有角色与资料模型 |
| 漫剧编剧与分镜师 / 1.0.0 | 剧情、分场、镜头和结构化分镜；2 个技能及校验脚本 | 统一时长未知值的 `pending/null` 冲突；如交付 JSON 文件并执行校验，需验证本地输出与 Python；不含视频生成器 | 第一组，文本/分镜核心先接入 |
| 跨境电商运营专家 / 1.2.2 | 6 个技能覆盖电商流程、图片文案、营销长文、视频营销、视频策划及轻流协作；源包明确支持离线规划 | 轻流为可选依赖；连接器已登记但本轮未验证授权/资格。视觉规划不等于已经接通生图 | 第一组，以明确的离线策划范围验收 |
| NextB2B报价专家 / 1.0.5 | 基于用户提供单价与明细计算报价、比较、台账；允许本地表格路线 | 本地 Excel 文件生成与读取需验证；腾讯文档不在当前注册表；行业资产服务为可选私有依赖；不能据空材料编造价格 | 第二组，先打通本地产物；云端协作单列 |
| 数据报告可视化专家 / 1.0.0 | 将用户数据转为图表、HTML 报告、信息图；2 个技能、HTML 模板和渲染器 | 非标准技能 frontmatter 需转换；Node、浏览器/渲染库、CDN与输出预览要明确。联网 CDN 不能作为离线交付的隐含依赖 | 第二组，验收到可打开的本地文件 |
| TikTok店铺运营专家 / 1.0.1 | 店铺诊断方法、指标解释、经营动作建议 | 原核心数据来自出海匠 social_accounts/social_seller/social_analytics，存在连接器授权与 TikTok 卖家授权两层；易界尚无该 provider。发布、评论、私信是额外写能力 | 第三组，真实店铺查询先补连接器；离线咨询不等于原完整能力 |
| 亚马逊1688找货源专家 / 2.2.0 | 14 项技能所表达的选品、货源对比和报告方法 | LinkFox proxy_call、文件上传、异步任务；JungleScout 兜底不在本包声明，参数与子技能不一致；缺失 expert-skill-creator；利润脚本有错配历史及缺值当零的问题 | 第三组，完整货源搜索依赖新适配、计算修正与实际协议核验 |
| 跨境电商服装人台换模特图专家 / 2.1.0 | 衣款保真要求、参考图和提示词组织流程 | LinkFox 出图与上传为核心；Agent 引用缺失 run_mannequin.py，返回字段及模型枚举存在新旧冲突 | 第三组，未打通生图前不得标为可生成模特图 |
| 跨境电商爆款视频复刻专家 / 2.2.0 | 镜头拆解、复刻方案、提示词和质量检查 | LinkFox 视频/图片/上传及异步任务；模型枚举新旧混用，源展示名与 Agent 名也不一致 | 第三组，未打通服务前不得标为可生成视频 |
| 行业研究员 / 0.1.0 | 7 个技能涉及行业框架、竞争分析、可比公司、选题、报告组织 | 搜索关闭；NeoData/WeStock 宿主专属认证；缺失命令/模板；混淆脚本不可直接认定已审；PPT 工具含需排除实现及限制性许可文本 | 第三组，先重建数据与产物依赖；上传材料分析只是有限范围 |

完整逐文件证据、工具名称与冲突位置见 [内容审计](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/expert-integration-audit-20261016/content.md)。三组是实现依赖顺序，**不是将用户要求的 10 位悄悄缩减为 3 或 5 位**。若交付目标是十位原能力完整可用，第三组的服务、认证、费用、结果回收和实际验收都必须纳入最终范围。

## 5. 连接器不能从 WorkBuddy 安装状态继承

易界当前活跃 catalog/registry 各有 **58** 项。它已经支持通用 MCP 发现、schema 冻结、逐次审批和精确调用，不能根据早期文档错误地判断“易界只有状态页、没有可执行连接器”。但注册不代表供应商当前可用。

| 依赖 | 易界当前事实 | 后续处理 |
| --- | --- | --- |
| qingflow | 已登记，HTTP/OAuth；静态目录为 `unverified`、`provider_onboarding_required` | 使用易界自己的配置/授权/完整 tools/list/资格/显式启用；本轮没检查用户实时连接状态，不推断已经可用或不可用 |
| LinkFox | 不在活跃 registry | 核对服务方实际可用于独立客户端的协议与授权；若不是兼容 MCP，应在 Connectors 实现受审适配，不能让角色脚本搬用 WorkBuddy proxy/token |
| chuhaijiang | 不在活跃 registry | 单独实现真实 provider 与卖家授权/店铺选择边界，先只读经营数据，再按明确需求评估平台写操作 |
| tencent-docs / NextB2B 行业资产服务 | 不在活跃 registry | 本地报价文件可独立推进；云文档和私有资产查询另作依赖适配 |
| NeoData / WeStock | 不在活跃 registry | 现有其他金融服务不等于字段、覆盖、费用和来源等价；如采用替代源必须明确重写能力及证据来源 |

依据：[固定 provider registry](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/provider_registry.rs:31)、[轻流注册项](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/catalog/provider-registry.v1.json:126)、[真实资格投影](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/providers.rs:927)、[单次审批与参数校验](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/generic.rs:133)。

通用路径不是无限兼容层：当前 destructive 注解工具拒绝，普通工具按有外部副作用的风险逐次审查，凭据字段不得经模型参数传入，失败/结果未知不自动重试；结果只接受受限惰性文本/JSON，不能直接承接任意图片/视频流。生成服务的任务 ID、轮询、费用、重复请求和媒体保存须专项适配。相关实现位于 [generic.rs](/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-connectors/worker/src/generic.rs:221)。

本轮没有探测上述远端，也没有读取 WorkBuddy 或易界凭据。因此这里只能确认“当前代码有没有接入”和“源包要求什么”，不能确认第三方接口当前状态或商业授权。实施时应按当时官方协议核验，不把源包里的旧 URL/参数当作事实。

## 6. 原包中必须纠正或排除的内容

1. **自动上报与公开上传。** LinkFox 多份说明要求向反馈接口 POST 用户说法、意图和执行情况；上传脚本存在 `x-oss-object-acl: public-read`，且不同专家版本行为并不一致。适配版必须去掉默认反馈行为，并将上传对象、目的地、公开性纳入真实用户操作与现有授权，不由角色提示词默许。
2. **宿主凭据与路径。** NeoData 脚本会读取/迁移 `~/.workbuddy/.neodata_token` 并写本地 token JSON；不应直接带入易界。LinkFox 输出 helper 可能从工作区回退到用户目录或临时目录并维护索引，应改为易界的受控任务输出流程。原凭据未读取、未复制。
3. **不符合长期安全条款的实现。** 行业研究包 `pptx-author/scripts/office/soffice.py` 会编译共享库并通过 `LD_PRELOAD` 使用 shim。该实现不能纳入或执行；可改用正常安装的 Office/LibreOffice 或重新审阅的渲染链。此结论依据用户明确禁止运行时劫持/安全边界绕过的条款，不以“仅本地测试”例外处理。
4. **缺失和冲突不能用模型猜测修复。** 人台包缺失脚本、LinkFox 模型枚举和请求参数冲突、分镜 schema 未知时长冲突、行业研究缺失模板与命令，均须形成适配决定并验证。它们是源材料的静态不一致，本轮没有宣称远端接口已经调用失败。
5. **来源权限不能混同。** 行业研究附带的 `pptx-author/LICENSE.txt` 含限制复制、修改、分发的文本；本地已安装并不能证明可打包进入易界或公开分发。先识别并剔除/替换不适用组件，保留来源证据，不把原京东专家的许可说明复用到十位专家。这里记录文件事实，不替代对适用条款的确认。
6. **利润计算已有明确缺陷。** 1688 原脚本在 ASIN 历史匹配失败时回退到第一份历史，部分缺失价格/FBA/佣金按零计算，缺广告词计数又可能推断零广告；只发出 stderr 警告仍继续产出利润。必须改为精确商品匹配、关键数据缺失阻断或显式情景假设，不能原样用于经营判断。见 [历史匹配](/Users/jack/Downloads/Personal_Info/易界文档/10专家/亚马逊1688找货源专家/原始资源/skills/linkfox-1688-source-profiler/scripts/step_4_calc_profit.py:158)、[缺值处理](/Users/jack/Downloads/Personal_Info/易界文档/10专家/亚马逊1688找货源专家/原始资源/skills/linkfox-1688-source-profiler/scripts/step_4_calc_profit.py:350)、[广告推断](/Users/jack/Downloads/Personal_Info/易界文档/10专家/亚马逊1688找货源专家/原始资源/skills/linkfox-1688-source-profiler/scripts/step_4_calc_profit.py:497)。本轮只读代码，未进行真实利润/费率验收。

上述文件仍完整保留在用户指定的原始资料目录作为来源。本次没有修改或执行它们。完整归档与产品运行子集应分别管理。

## 7. 推荐的最小接入方案

### 7.1 保持现有模块主干

继续使用 `yijie-skills → 规范 bundle/authority → Host + Native → 真正专家目录 → 原会话绑定/发送`。保留 `experts/1`、单会话单专家、SQL34/35、Host10、既有 outbox、权限与连接器审批。现有证据没有显示仅增加十位内容需要数据库迁移、修改 Codex Runtime 核心，或建立第二套专家引擎。

每位建立易界自己的适配版本，原版版本单独记为 provenance，不能用原版本号暗示逐字/行为等价。包结构建议：

```text
experts/<expert-id>/skills/<resource-name>/
  SKILL.md                  唯一受管入口
  ROLE.md                   易界角色、任务流程和真实能力边界
  references/               按任务拆分的方法、字段说明、模板说明
  scripts/、templates/      仅按需纳入经审阅并验证的附属文件
  来源与内容审校材料          按现有打包器实际字段组织
```

来源记录应明确每份原资源是保留、转译、由现有工具替代、延后或排除，以及原因。无外部知识的小红书专家可把其角色方法整理为真实的范围/方法参考，不编造知识库。多技能编排规则可以转换为 ROLE 的路由和参考索引，不必全局注册 42 个 Skill。

### 7.2 依赖顺序

1. 先冻结十位各自的目标输出和完成条件，并区分咨询、文件交付、平台服务能力；按逐项审计修订源内容和提示词。先完成三位文字/规划专家，验证通用目录扩容链。
2. 打通报价与可视化的本地产物：输入材料读取、计算/渲染、输出路径、文件可打开、错误说明；沿当前会话授权，不附带云文档写入。
3. 为五位外部依赖较重的专家分别补连接器、搜索/数据、上传和异步结果能力；仅把已通过实际验收的能力标为可用。文字咨询版若先交付，需明确命名与范围，不能借原生图/找货源标题承诺未实现的结果。
4. 每组仍使用同一套资源与会话模块；这只是依赖先后，不另建多个框架。最终目标若是十位完整接入，就以十位目标都验收为完成条件。

### 7.3 各仓职责与契约判断

| 仓库 | 必要工作或条件工作 |
| --- | --- |
| yijie-skills | 十位适配内容、独立版本、明确 package_files、知识索引、审校/来源/本地使用依据；规范打包 |
| yijie-desktop | 泛化单专家同步断言、同步 pin、真实目录替代同 ID 展示卡、头像映射；复用资源准备/召唤/详情/快捷问题；保持三列和易界 tokens |
| yijie-agent-host | 同步新资产 manifest pin；仅对选定的搜索或额外能力策略做必要适配，保留普通/专家权限与恢复边界 |
| yijie-contracts | 若仍是现有字段与行为下的内容新增，不预设要升级 wire；若表达新增依赖准入、搜索策略、资源类型或新错误状态，则权威契约先行，评估 additive/semantic/breaking，保持旧 jd 行为 |
| yijie-connectors | 对实际缺失服务增加固定注册/适配、认证、资格、逐次审批与结果处理；第三方官方协议为外部权威，不从源插件动态加载任意地址 |
| yijie 元仓 | 记录本次方案、新需求范围、Must AC、实际验证与已知限制；不在元仓实现业务 |

单纯保留本地头像可使用 UI 本地映射，无需扩大执行 wire。需要依赖状态成为机器判定时，不能只写前端静态标签；应由实际服务资格和本轮权限投影产生。不得用每专家名称硬编码网络例外或复制第二份权威 DTO。

规范顺序为：必要的源契约与官方协议核验 → 内容/连接器 provider → Host/Native consumer 与来源固定 → UI → focused checks → 正常本机入口验收。打包可生成新的 bundle，但旧 jd archive/ROLE/knowledge 与原 38 普通包保持不变；Host 源输入改变后按现有 canonical 流程重新冻结 Desktop build pin，禁止手改派生摘要蒙混通过。

### 7.4 UI 如何体现真实状态

同一 ID 接通真实目录后移除对应展示记录，避免出现 21 张重复卡片。头像、名称、描述和标签沿用已改善的三列视觉，但描述和快捷问题必须匹配适配后的能力。真实状态继续区分资源可准备/已准备、当前会话已选择、当前服务依赖不可用；“资源已准备”不能冒充“所有外部业务可执行”。

选择不发送；快捷问题只填草稿；切换专家保留会话历史并复用已有确认；服务不可用时说明具体缺项，不自动换专家、切 full、启用工具或降级到普通发送。待处理/未知操作沿原恢复入口，不新增隐式重试。

## 8. 后续验收与回退

接入至少应验证以下实际结果，而不是只查卡片数量或编译：

1. 十个新包结构、摘要、入口与相对引用正确；11 位真实目录无重复；普通 38 包及 jd 0.1.3 字节不变；专家不出现在全局 Skills 中。
2. 每位正常准备、选择与显式发送；同会话 A→B→解除、模型切换、正常退出重开后，绑定版本、普通基线和旧历史正确。挂起/审批中操作沿既有锁拒绝；恢复只处理原操作。
3. 文案专家交付符合角色任务的内容；分镜输出符合统一 schema；报价用合成输入核对数量/单价/总额；图表报告能打开且与输入数据一致。内容质量单独记录，结构通过不能代替内容验收。
4. 外部依赖分别证明授权、资格、选择、批准后的真实结果及拒绝零执行；任务类服务核对任务 ID、轮询、取消/未知结果和重复费用边界；只在相应调用范围与预算明确后执行。
5. 资料读取/写出/上传/下载遵循本轮权限；无 WorkBuddy 凭据搬运、默认反馈、未确认公开上传、无依据价格/市场事实或自动发品。
6. 本机真实入口、亮暗主题、最小窗口、键盘焦点、弹窗、空/加载/缺依赖/错误/取消/重试状态可用。界面继续不包含专家团。

回退不能直接换回不认识新目录与已保留绑定的旧程序。若要继续执行新增专家，必须保留扩容后的 catalog/pin、精确资源和兼容 reader，不能把“历史可读”当成“旧 pin 仍能执行新引用”。现有 `YIJIE_EXPERTS_ENABLED=false` 是全局专家执行开关，不是只停止新增专家选择的开关；使用它会关闭专家执行，已有绑定应保留可读并拒绝不兼容发送，不能静默改为普通发送。不得删除会话或覆盖安装收据，删除/升级遵守 retained 引用保护。是否需要更细的激活开关或额外版本仓库，应由后续确切目标决定，不为扩容预先重构。

按照用户长期条款，不执行强杀、权限破坏、可执行文件劫持、恶意资源/攻击注入和危险归档测试。相关异常只使用正常拒绝/取消/恢复、静态审查和既有不可变证据；未执行的故障注入路径不标为通过。

## 9. 本轮完成与未执行

已完成：当前源码与历史设计交叉审计、十位资料与依赖审查、233 份原文件来源一致性核对、逐项可行性判断、推荐接入边界与验收计划。

报告经过与初次调查分开的执行链/打包契约两路 Codex 复核，修正了一个来源链接、明确全局开关的回退影响，并补充闭合分类映射要求；这不代表用户或独立人工批准。元仓 `pnpm lint`、`pnpm test`（50/50）和全部 `scripts/*.sh` 语法检查通过，报告 36 个当时已有本地链接无缺失/越界行号。仅新增本报告及本机 `.local` 审计笔记，五个产品仓状态与审计基线一致。这些检查只验证文档/治理和来源事实，不是十位专家的产品验收。

未执行：十位专家运行接入、资源重打包/安装、Runtime/Host/App 重启、模型请求、第三方授权/探测/付费业务、原包脚本、公开发布。没有读取凭据、改数据库、提交或推送。原有专家可用性的历史证据保持为历史，不冒充本轮重新验收。

本报告的建议是：**复用现有架构逐项适配，优先跑通文字与本地产物能力；对必须联网才能交付的专家，把依赖接通列为完成条件。不要以十个提示词能被选中，代替十位专家真正可用。**
