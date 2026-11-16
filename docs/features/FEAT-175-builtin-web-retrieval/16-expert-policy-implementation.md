# FEAT-175 B02：专家网页政策与版本处理

2026-11-15，修订 3 推荐设计，未修改任何角色／Skill 或产品配置。

## 1. 本轮选择的明确规则

默认专家采用 inherit，修复“role 非空就禁用所有专家原生搜索”的条件。对真正声明 agent 级不联网的**现有受管版本保留网页禁用**，不通过全局功能升级偷偷改变其数据边界。无需先决定一套新的专家类别，也不按名称推断。

| 已查来源 | 当前判定 | 推荐执行政策 |
| --- | --- | --- |
| 普通无专家聊天、无特殊网页限制的已验证专家 | 通用网页能力 | inherit |
| data-analyst-pro 0.1.0 | ROLE.md 第 7 行限制整个专家联网 | disabled |
| data-analyst-pro 0.1.1 | 同上 | disabled |
| data-analyst-pro 0.1.2 | 同上 | disabled |
| 分镜专家 agentgrid-comic-storyboard-director | 原文仅说明 validate_storyboard.py 不联网／不装依赖 | inherit；脚本限制保持 |

精确文件及角色 SHA-256 已写入 [版本清单](references/expert-policy-inventory-r3.json)。它是设计证据，不是运行时已经使用的新配置。既有 data-analyst-pro 不因本需求自动升级或改写。

以后如产品需要可联网的数据分析专家，应建立明确的新版本／变体，重新审阅角色说明与公开资料使用边界，再声明 inherit；不复用旧版本号，不重写旧摘要，不自动将用户当前绑定切到新版本。该版本制作不作为 FEAT-175 默认工作量。

此处 disabled **仅表示关闭 hosted 和应用内置网页工具**，不声称整个模型推理离线、不创建新的 OS 网络沙箱，也不代替原有文件／命令权限。

## 2. 单一权威和原生投影

优先沿已有 WithExpertImageRoute 的“已审阅精确身份→受管工具配置”模式，新增 Contracts 负责的 `expert-web-policy/1` 候选源。它是一份小型政策数据，不是 Host 名称白名单或第二个专家安装目录。

源记录限定 expert_id、version、role_sha256、policy=inherit|disabled 和来源审阅引用；生成 Host／Native 所需材料。已有 ResolveExpert 先校验完整 ExpertRef 的 archive、role、knowledge 和安装 receipt，再按已解析身份读取政策；不让 renderer 或模型传 policy 布尔值。

默认行为：

- 对普通聊天及已通过来源校验、没有专门约束的专家，inherit 原有效配置。
- 对上表已登记限制的身份，必须精确匹配版本与角色摘要；同一受限专家的新版本没有审核记录时返回 qualification_required，不能失配后掉回 inherit。
- 新专家／资源版本的正常发布评审必须记录是否存在 agent 级网页限制；对脚本说明只作人审分类，运行时不扫描文本做关键词判断。
- 不为全部专家建立正向联网白名单，也不复制角色正文到 Host。

Host 在已有 contextForExpert／contextForStoredExpert 组合点获得政策，再映射现有原生配置：

| 政策 | hosted | yijie_web | 其他行为 |
| --- | --- | --- | --- |
| inherit | 不覆盖用户已有 web_search 模式 | 普通 App 内置配置 | 专家角色、媒体选源、平台权限照旧 |
| disabled | web_search=disabled | mcp_servers.yijie_web.enabled=false | 不改其他能力的全局权限 |
| 未资格化版本／未知结果 | 不派发新的模型／网页调用 | 同左 | 保留当前绑定和历史，明确资源资格问题 |

真实工具调用入口还要复核当前持久 expert binding／pending 状态，借用媒体入口已有的“历史中可能有旧工具定义，所以实际执行仍查绑定”模式，防止旧定义绕过当前工具范围。只复用其绑定核验，不复制“一轮只能生成一张图”的业务限制；网页研究可以有多个正常调用。

配置合并顺序必须固定：先完成普通模型／权限及 market、artifact、media、tool_search 的现有组合；再合并 yijie_web 和 MiniMax 所需 namespace；最后一次性应用当前网页政策／辅助任务限制。不能先写 disabled 再被自动装配覆盖为 true。namespace 按集合追加／去重，不能由后一个 helper 重建数组而丢掉前一个应用工具。

## 3. 版本与迁移步骤

1. 从当前 Skills 源与已保留版本生成政策审阅清单；本轮已识别上述三版本。Source-first 定义政策源、生成类型和 consumer pin，不改 Runtime schema。
2. 使用现有 ExpertRef／ResolveExpert／安装 receipt 保证同源；所需索引是源政策的生成物，不能手填临时 hash。
3. 新调用在 idle 且无 pending／unknown 操作时，经原正常 unsubscribe/resume 应用配置。已开始的 turn 不热改政策。
4. 旧对话和旧工具结果只读保留；恢复继续使用原已绑定版本的政策，不偷偷换专家。用户正常移除专家后，恢复普通配置，不硬编码 cached 覆盖其原设置。
5. 未来资源版本走原生 Skills／受管资产升级和已有绑定操作；当前版本不修改。已有图片／视频的精确 route 表和禁止替代规则保持。

如果更新了共享政策源而非角色文本，仍要记录政策版本／digest 和实际 thread 配置来源，避免把“角色 hash 没变”误说成执行语义没有变化。旧 reader 保留，不降数据库或改写 rollout。

新用户提交在创建 operation／冻结 digest 之前，按新目录可选性排除已退役 kimi-web 的旧偏好引用，并在 UI 显示为应用内置能力；这样旧聊天不要求用户每次手动清除旧勾选。已冻结的旧 outbox／审批／未知操作绝不据此改写或重签摘要；它们沿原正常结束／恢复边界处理。其他连接器的当前选择保持。

## 4. 与市场框架的区别

当前 ExpertsEnabled() 依赖 MarketEnabled()，专家提交复用 Native-owned typed wrapper 和当前资源／scope 校验。**无需用户选连接器不等于删除市场框架。** FEAT-175 保留这套已验证基础设施，不借此重建专家系统。

验证分成两种合法组合：

- builtin-only、市场功能关闭：普通聊天内置检索可用，不承诺现有专家框架也在此组合可用。
- 专家框架正常开启、市场选集为空：专家可按上述政策使用通用网页能力，无 kimi-web 安装／授权／勾选。

不能使用“市场关闭＋现有专家已启用”的无效组合制造验收，也不能为了让专家可用而自动安装或选中 kimi-web。

## 5. 依赖与验收

| 编号 | 实现／依赖 | 验收标准 |
| --- | --- | --- |
| B2-A1 | 政策源＋三个现有精确版本 | 角色文件／历史摘要完全保持；三版本均解析为 disabled |
| B2-A2 | 默认 inherit | 至少两个已验证普通专家与无专家对照，两模型实际请求均保留原生搜索和允许的内置工具 |
| B2-A3 | 原生配置＋实际调用核验 | disabled 版本的 provider tools 不含 hosted，MCP 当前表面无 yijie_web；历史工具提议也在准入前拒绝，API发送为0 |
| B2-A4 | 资源来源与版本机制 | 保留已验证旧版正常读取；未审阅新版本返回资格不足，不替换绑定或自动放开网页 |
| B2-A5 | 生命周期 | 选中／移除／模型切换／正常重开分别检查实际 tools；无活动 turn 中切换，无历史重写 |
| B2-A6 | 局部限制 | 分镜脚本仍按原说明不联网，整个专家不被误禁；其他平台、媒体路线和正常文件计算不回归 |
| B2-A7 | 公开分发依赖 | 目标发行渠道只含已获该渠道资格的资源；local-use-only 不能因网页政策已定义就公开发布 |

验证只用正常版本、普通输入、合法选择和既有 conformance；不篡改已安装文件、不注入恶意 fixture、不制造权限故障。B02 的推荐政策已经明确，但需要完整方案审阅及后续真实配置／资源验收后才能激活。
