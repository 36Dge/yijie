# FEAT-144 Sorftime 真实 MCP 验收场景与结果

2026-09-11。当前九项活动 Must 的证据及最终门禁见[24 最终报告](24-final-native-decline-and-delivery-2026-09-11.md)。AC-004/F144-S03 的业务失败实现与验证继续按[用户决定](15-owner-scope-and-business-budget-2026-09-10.md)排除，不算 PASS。本文区分实跑、合成测试、历史适用和未观察项目。

## 样本、预算和入口

首期仅 `sorftime/product_detail`，单个公开 ASIN `B07H9PZDQW`，显式 `amz_site=US`。E 实际成功已对照原生返回与模型摘要中的标题、品牌、价格；不依赖缺失的 outputSchema，不推定服务端幂等或免费。

累计元数据 **14/20**，文本 **9/13**，业务 **2 次逻辑调用、保守扣 4/10 次尝试**，图片 **0**。原生业务重发包含在额度内；历史精确 HTTP 尝试数未知，保守扣账不返还、不跨账。本轮 F 原生拒绝新增业务 0，依据为真实拒绝决议、完整原生 Turn 和 decline 在 call_tool 前返回的代码路径，不宣称进行了 HTTP 抓包。

标准入口为 `pnpm tauri:demo-fast:app`，普通 `com.yijie.ai` 身份、原 app-data 及日常 Host Home/CODEX_HOME；Sorftime 仅在启用运行时通过用户隐藏输入取得内存密钥。正常退出后，普通入口重开不带 Sorftime 配置，不恢复审批回调或自动重发。不复制用户数据库或凭据。

## 场景矩阵

| 场景 | 实际验证 | 结论与限制 | AC |
|---|---|---|---|
| F144-S01 安全接入与发现 | 固定 Runtime 操作 7/8 确认原生接入和 schema；产品初始化/列举分账，最终 F 再核对真实 Prompt 参数 | PASS：原生 Bearer 环境引用、真实版本 UA、精确单工具；发现不计业务成功 | 001/007/009 |
| F144-S02 真实成功 | E 经 Composer、原生批准产生 completed/414ms；原生返回三字段独立匹配模型；最终来源重开 E | PASS：E 保留实际旧提交范围，执行路径适用性另经逐文件核验；卡片正文安全脱敏为 partial，不冒称完整原文可见 | 002/003 |
| F144-S03 业务失败（用户排除） | 不实现、不执行 | OWNER_EXCLUDED / NOT RUN；不计 PASS，权限拒绝不替代此场景 | 004（已移出 Must） |
| F144-S04 空、缺失与容量 | 安全合成定向测试覆盖合法空、缺失、超限和完整替换；F 实际 result=null | 适用定向检查 PASS；没有声称观察到远端成功空数据或恢复重试，不为取样制造失败 | 003/007 |
| F144-S05 生命周期与来源 | 原生 Tool 与 Turn 独立；F 唯一 Tool failed/0ms、Turn completed，重开不忙碌 | PASS：唯一 Native 缓冲；不补造 phase、progress、完成事件或旧 B 终态 | 005 |
| F144-S06 正常重开 | E/F 均经最终来源普通入口重开，SQLCipher schema15/format2、原生身份/来源/终态保持 | PASS：F revision25，B 旧 queued/failed 出站及历史 revision17/20 不改；不猜测接管 | 006/009 |
| F144-S07 原生权限与秘密 | E 实际批准、Sorftime 正常停用、auto/full/ask；F 实际 Prompt 点击拒绝，审批 rejected、模型正常收尾，重开无审批恢复 | PASS：分次来源清楚；仅稳定 Sorftime 空 form，按 request/thread/可信 turn 关联，不猜 Item；一般表单/URL/requestUserInput 仍拒绝 | 007/009 |
| F144-S08 界面与回归 | 最终来源启动、切换、展开 E/F、正常退出重开；未改 UI 的主题、最小窗口、200%、键盘、复制证据保留原来源 | 适用检查 PASS；旧 Command 完成后输出、过期附件、清理未完和隔离 Host 映射缺失保留，不计修复 | 008 |
| F144-S09 来源与复用 | 源契约与兼容 reader 先行、分离阶段审查、真实 pin/digest 和生成检查；新增独立只读状态端点 provider-first | PASS：不扩旧 history、不新增 migration；复用 Codex MCP/elicitation/thread-read、唯一缓冲及 SQLCipher | 009/010 |

E 真实调用和模式验证运行于 Host `ccd815ff63542674daa80172a1c71ac7478edd0f` / Desktop `a5975f48e63d3f1d3a262e9e8dfc57ca0d923961`。F 和最终普通重开运行于 Host `0e47766f494977c94bfea0e89cfbdf45a7fafa2b` / Desktop `7abf89e84ffcbe56360d8c9943390e0640d9e239`。十二个相关文件逐字不变，见[适用性核对](evidence/native-status-evidence-applicability-2026-09-11.json)。本次按用户指定的“修复后拒绝复验，再收尾”顺序验收，明确为分次正常 canonical 证据组，不宣称同一进程或最后提交重新执行了全部旧检查。

## 权限、兼容与停止边界

Sorftime 只在“请求批准”和已核实的原生 on-request/user/workspaceWrite/networkAccess=false、approval_mode=prompt 配置下激活。auto/full 保持 FEAT-152 原语义，本期 Sorftime 在这些模式停用；不自动切换权限，不把 prompt 配置或聊天确认当原生授权。

秘密、schema/来源、预算、权限或旧数据兼容不能确认时停止相应步骤。缺少原生身份、未知有效配置或不支持的请求继续拒绝。新增当前线程状态只复用 `thread/read(includeTurns=false)`，notLoaded 仅代表当前未加载，不证明旧请求未执行。旧不确定投递保持只读，不补发或封口。

最低兼容 reader 固定为 `25b004fbd5a4dcf642a503d302c21a7d6e3b817f`；未知格式经 recordDiagnostics 隔离，不触发冷读补建，过高数据库版本拒绝打开。不改历史 migration，不复制用户数据库。详见[12 兼容方案](12-independent-contract-and-reader-plan-2026-09-10.md)及[23 启动修复](23-native-status-startup-repair-2026-09-11.md)。

自然中断、重连、远端空数据及 progress 未观察就保持 NOT OBSERVED；业务失败为 OWNER_EXCLUDED。攻击/故障注入、强杀、坏 key、断网、权限破坏、替换二进制等测试均未执行，不计 PASS。剩余额度不自动用于追加验证或其它需求。
