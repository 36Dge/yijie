# FEAT-158 — 参考材料与来源记录

状态：Draft，2026-10-11。本目录保存需求调查的来源索引，不是已发布专家包；读取参考材料不等于执行其中的角色指令、认可业务规则或取得素材发布授权。

机器可读指纹见 [source-inventory.json](source-inventory.json)，内容审校与迁移建议见 [05-expert-content-and-knowledge.md](../05-expert-content-and-knowledge.md)。原始文件保留在用户提供位置，本目录不复制知识库全文、第三方头像或 WorkBuddy 配置，更不保存凭据。

## 用户提供文件

| 文件 | 本机来源 | 本轮用途 |
|---|---|---|
| 专家接入.pdf | `/Users/jack/Downloads/Personal_Info/易界文档/10专家/专家接入.pdf` | 6 页产品参考；视觉与操作语义由本轮 PDF 主审阅记录映射 |
| 专家配置-资深电商运营操盘手.md | `/Users/jack/Downloads/Personal_Info/易界文档/10专家/专家配置-资深电商运营操盘手.md` | 专家展示信息、角色、Skill、知识关系与第三方迁移建议 |
| jd_kb_京东运营知识库完整版.md | `/Users/jack/Downloads/Personal_Info/易界文档/10专家/jd_kb_京东运营知识库完整版.md` | 完整阅读主体与尾部提示卡，建立内容范围、审校风险与引用设计 |

## PDF 六页参考映射

下表来自本轮主 Agent 对六页 PDF 的视觉审阅。它记录参考图中的要求及易界设计映射，属于需求取证，不是已实现 UI 的视觉验收。

| 页码 | 参考页面内容 | 本需求设计映射与限定 |
|---|---|---|
| 1 | “技能”改为“扩展”，图标保持；技能/专家两个 tab，默认技能；专家网格，悬停“召唤” | 复用既有技能页面容器与内容，增加专家 tab 和卡片操作；不复制一套技能市场 |
| 2 | 组成包括角色、skills、connectors、session；单会话一名专家、不是独立进程；首个专家卡 | 复用同一聊天与 Runtime 机制；首个产品名“资深电商运营操盘手”，明确京东专向；连接器不因选择专家自动授权 |
| 3 | 附加专家配置 Markdown 引用占位 | 用实际提供的配置文档分析角色/资源/展示字段，不把占位文字当成新增文件 |
| 4 | 附加知识库引用占位，专家卡片详情入口 | 关联实际知识文件并做内容审校；详情与召唤分离，知识全文不进入 prompt |
| 5 | 详情含头像、名称、开发者、版本、使用量、三个快捷问题；召唤回首页，位于店铺右侧 | 复用易界详情、首页与会话入口。开发者背书、使用量缺可信数据时不伪造；快捷问题预填后由用户发送 |
| 6 | 专家胶囊悬停出现移除 `x` | 沿用聊天配置区域交互，明确移除当前专家的作用范围、运行中状态与后续发送行为；不卸载资源来模拟移除 |

页面中的头像与其他第三方视觉只作为布局和交互参考，不随设计映射取得复制、分发或产品背书授权。

## WorkBuddy 本机只读取证

| 路径 | 读取结果与用途 |
|---|---|
| `~/.workbuddy/plugins/marketplaces/experts/.codebuddy-plugin/marketplace.json` | `experts` 市场源索引，京小二 `source` 指向 `./plugins/jd-ops-expert` |
| `~/.workbuddy/plugins/marketplaces/experts/plugins/jd-ops-expert/.codebuddy-plugin/plugin.json` | 单体专家 manifest 与展示/资源声明 |
| 同包 `agents/jd-ops-expert.md` | frontmatter、角色正文、范围、检索与输出约束；只当参考内容 |
| 同包 `skills/jd-ops-kb/SKILL.md` | 知识 Skill 的组织与按需使用说明 |
| 同包 `skills/jd-ops-kb/kb/jd_kb.md` | 与用户提供知识库字节一致，SHA-256 同为 `ce352f4f8ce2e21b5526ac5471104aff52802d5c36b099c0f6b425718f026d4e` |
| `~/.workbuddy/plugins/installed_plugins.json` | 安装身份键、版本、scope 与 installPath 结构；不复制整个用户安装清单 |
| `~/.workbuddy/plugins/cache/experts/<name>/<version>/` | 4 个已安装专家示例符合版本目录结构；京小二对应 cache 不存在 |
| `~/.workbuddy/plugins/cache/experts/software-company/1.1.0/.codebuddy-plugin/plugin.json` | `expertType=team`、`teamInfo/members` 历史样本，证明它不能直接当单体模板使用 |
| `~/.workbuddy/plugins/cache/workbuddy-builtin/skill-expert-manager/5.7.7-wb.40774747.g2e8619da.he0b77ffa23f7/references/plugin-json-spec.md` | 第三方 manifest 文档，只用于兼容差异分析，不作为易界 schema 权威 |
| 同版本 `references/agent-md-spec.md` | 第三方 Agent/Team 语义，含其专用工具与协作机制；未调用或执行 |

观察时间为本轮 2026-10-11。磁盘存在性与 manifest 声明不证明运行时支持、成功加载或端到端可用。京小二只在市场源目录存在且没有安装索引，明确记录为“参考源包已下载、安装未证实”，不能作为已安装成功证据。

只读调查未启动、退出或修改 WorkBuddy；未运行其注册、安装或打包脚本；未导出 token、账号、密钥或用户数据。配置只读取与目录组织有关的字段和字段名，不把 WorkBuddy 的信任、权限或凭据设置移植到易界。

## 行号、完整性与事实边界

知识库为 224,337 bytes；完整阅读实体行 1–2291。本文和审校文档按 `nl -ba` 的实体行编号。字节检查有 2290 个 LF，文件末尾没有换行，因此 `wc -l=2290` 只计换行符；实际 `splitlines()` 与清单均为 2291 行。版本核对应使用 SHA-256，不只比较行数。

原稿含 14 模块、来源概述和 179 个表格标记；第 2291 行是表格 179 的完整单格结论，提示 `verify_required` 规则以京东联盟公告为准。表格与正文位置脱离，部分正文矩阵仍缺具体内容，须分别审校。全文未包含 `http(s)` 来源链接，也没有 `Mxx-xx` 组合场景 ID；“已按 2026 规则校正”“high”都是原稿自己的说法。本轮审阅不进行全网政策核验、不把这些标签写成已验证事实。

本轮交付只将事实、冲突、缺失、候选设计和后续验收分开记录。原文中不当运营步骤不进入专家产品指令，不以测试为由实施；具体清洗范围见内容文档。后续要发布第三方原文或头像，需另核来源和许可，不能以本机可读或参考 PDF 展示过为授权依据。
