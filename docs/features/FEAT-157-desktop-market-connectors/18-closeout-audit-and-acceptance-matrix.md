# FEAT-157 收尾审计与验收矩阵

2026-10-08，当前49项（已移除淘宝闪购和豆蔻医生），非空选集仅请求批准。真实业务验收仍只Tushare，其他48项采用代码审计与适用的普通本地测试。此前诊断不足不阻塞。

## 本轮实际代码缺口与修复

1. 关闭第三方页面或系统浏览器首次打开失败后，产品缺少重开原页面入口，普通“重新确认状态”只读取回执。已新增“重新打开连接页面”，仅针对同一个pending授权/配置操作，使用其operation ID及回执revision，不新建OAuth/DCR/Probe，不扩大scope、不新增付费调用。
2. 原自动首次打开页面沿用了operation read权限。现无论首次自动打开还是显式重开，均须重新校验connector.credentials.manage；只读用户保留读取回执能力但不打开授权页。
3. 统一完整参数审批、历史查看、正常停止、只读管理等既有实现证据，避免所有AC一直停留在起草时pending。代码实现、针对性验证、真实Tushare与最终Owner验收分开记录。

Contract impact为semantic（修正浏览器副作用权限，命令是additive）。Native IPC family从0.1.0增为0.2.0；既有9命令/请求/响应不删改，新增第10条原操作重开命令。源先行生成，再同步Selection/Broker/Provider/Host依赖摘要及全部消费者。无新迁移、无Runtime或外部HTTP协议变更。旧Native不认识新命令时拒绝，新UI与Native同包发布；仅本地候选，未提交或发布。

## 当前代码与证据映射

| AC | 已实现、已验证的内容 | 证据边界 |
| --- | --- | --- |
| 001 | 唯一49项、六分类2/5/2/14/17/9、品牌图标、两tab、搜索；两项已移除 | 目录/Native/API专项与标准应用实读；无逐服务调用 |
| 002 | 安装原子回执、默认关闭、相同操作重放、重装generation隔离 | Native store、前端store、实际本机AE安装；安装不触发授权、工具发现或下载 |
| 003 | 45 OAuth路径及4凭据路径、Keyring边界、完整工具发现、迟到/取消/过期不反启用；原页面可恢复 | Worker56、Native39、UI59；AE字段由导出配置提供，未声称所有供应商已实连 |
| 004 | 启停/卸载撤销未来准入，正常cleanup与STOP_PENDING保留，历史不删、旧引用失效 | Native/Worker生命周期与UI卸载恢复专项；禁用的故障/攻击测试未执行 |
| 005 | 店铺右侧入口、chip、多选去重、两个提交分支、管理往返保留正文/模型/附件意图 | 当前标准应用草稿往返、旧真实Tusharechip、组件及draft/Composer专项 |
| 006 | 精确多服务binding、单次审批、HTTP一次许可、未知风险write、破坏性工具无专用策略拒绝 | 两普通本地MCP服务集成、真实Tushare批准1发送/拒绝0发送；平台秘密留Connectors |
| 007 | 单一Native状态、原名称快照、旧reader、原operation查询、已发送历史无执行权限 | Native迁移/selection、Host store/submit、历史轮次UI及标准应用历史只读 |
| 008 | 取消/未知/错误有恢复入口，操作幂等、查询不重发业务，浏览器重开不新建授权 | 新重开command/API/store/权限专项；原失败/未知执行记录保留 |
| 009 | 易界亮暗主题、长名称、最小窗口、200%缩放、键盘焦点 | 原UI视觉证据加本轮1180×760亮100%/暗200%真实组件截图观察；新增三按钮均在窗口内 |
| 010 | Tushare canonical批准成功和拒绝零发送已有实据；当前49项标准构建和代码审计完成 | PASS：真实证据对应f8，随后ea84为本地回归；Owner于13:20明确接受分阶段证据完成本地D4，未改写为同构建实跑 |

## 验证原则

原2轮模型/1查询及追加4轮/2查询均已耗尽。本轮新增模型、业务查询、非Tushare真实OAuth/metadata均为0。只做应用本机安装管理、读已有历史和正常重启；未真实配置AE或其他供应商。

本轮UI59、Native39、Worker56，Contracts管理JS11/Rust6/Go及依赖JS22，相关Clippy/lint/source-sync通过。新按钮已在1180×760亮色100%及暗色200%组件页面验证：暗色三按钮bottom=688，小于760；关闭后焦点回原卡片。临时Vite按自身SIGINT正常close，exit0；未强杀。

## Owner最终验收与D4结论

2026-10-08T13:20:34+08:00记录Owner明确回复：“接受分阶段证据，完成本地 D4（推荐）”。AC-001–010与整体本地D4为PASS，implementation为complete，feature为usable。采用既有Tushare真实批准/拒绝加最新标准构建本地回归；原f8实跑与ea84回归保留独立构建标识，不改写为同构建fresh run。

这是Owner针对FEAT-157本地验收的明确决定；仓库AGENTS.md的一般fresh-run规范没有改写，也不据此声明public/production验收通过。其余48家按Owner范围完成代码审计与适用普通本地测试，无需逐家真实调用。未选择同构建付费复验选项，未增加任何调用额度，未提交、推送或发布。

可追踪证据：[真实Tushare](evidence/generic-final-acceptance-2026-10-08.json)、[最新回归与Owner原文](evidence/closeout-verification-2026-10-08.json)、[机器状态](feature.yaml)。

## 标准应用补充结果

当前worker ea84c3604f1c129e244c12966bce3c687a2158dad1ef986c98c5d0653b045c58。AE只做本机无凭据安装（1→2项）、默认待配置、正常退出与重开保持；卸载确认按Escape取消，安装保留且焦点回按钮；随后确认卸载本轮测试记录（2→1项），保留原Tushare。对话正文和Kimi/ask通过管理页往返保留，已清理测试草稿且未发送。鼠标定位曾未打开hover按钮，改用实际聚焦的Tab/Return验证，没有把无响应视作卸载完成。

当前源邻近6文件69项通过。首次宽松文件名过滤误匹配`.local`历史备份（39文件、32失败），这些失败未计通过；改为项目canonical excludes后当前src全部通过，没有改旧备份或放宽断言。日志与摘要见[evidence/closeout-verification-2026-10-08.json](evidence/closeout-verification-2026-10-08.json)。

最后只读打开既有Tushare验收会话，原成功结果（close=11.50）与原拒绝结果均可查看；历史没有重现可执行批准入口或触发新调用。

## 最终交付检查

Owner确认后，本包D4门禁及`--audit-claims`均通过，日志见[最终D4检查](evidence/closeout-checks/final-d4.log)和[声明检查](evidence/closeout-checks/final-claims.log)。元仓lint、50项测试、脚本语法通过；六仓`git diff --check`通过。核验27项源文件、构建产物与专项日志摘要一致，固定Codex Runtime仓库仍干净，Desktop三个受保护店铺文件的差异摘要保持不变。

工作区保留前序及本轮修改，未提交或发布；状态快照见[交付工作区](evidence/closeout-workspace-after.json)。FEAT-157当前49项本地需求无剩余阻塞验收项；供应商账号资格、AE导出配置适用条件及未执行项目继续按上文证据边界记录，未宣称全仓CI或生产验收通过。


本地D4完成后Owner另行授权Git提交推送，交付范围与远端提交记录见[19](19-git-delivery-2026-10-08.md)。本页“未提交”的表述是D4验收时点事实，后续Git交付没有改变验收证据所属构建。
