# Sorftime 连接页重设计

2026-10-08。Owner确认Sorftime没有一键OAuth，手工复制Account-SK的接入方式继续采用；要求将配置页提升为正常产品页面，不展示无关实现信息。本决定关闭前次OAuth待确认事项，不恢复旧Sorftime专用执行入口。

contract-impact = semantic：仅worker拥有的私有HTML表单和交互投影变化，提供同源nonce校验的显式取消；公共IPC、认证方式、固定端点、Keyring格式、安装/选集/审批、重试规则保持原样。私有表单以Connectors credentials模块为权威，不增加公共DTO/数据库migration。现有name/scheme字段用隐藏固定值继续提交，服务端仍复验；不会把秘密移入Desktop renderer。

页面结构：易界品牌页头；居中连接卡片；Sorftime标识、简短标题和用途说明；Account-SK密码输入及显示开关；官方获取密钥入口；保存并连接、取消；一条本机保存说明。移除用户可见Header/Bearer格式、旧授权迁移和实现诊断。错误靠近字段，失效、取消与提交回执使用相同样式，接收配置不能显示为已连接。

独立安全页由Rust服务生成，不能导入Vue/Yj组件或把密钥经过Native/Host转交renderer。复用Desktop已接受token和品牌/用户提供Sorftime SVG的本地快照；不加载外部字体、脚本或图片。沿用一次性nonce、Host/Origin、原到期时间、no-store/CSP和正常关闭；新增交互脚本只负责表单显示/校验/提交忙碌及本地过期提示，不使用fetch、存储或自动读取剪贴板。

验证采用真实渲染函数、普通本地表单提交与取消/到期测试，检查亮暗主题、1180×760和窄屏。只用普通非秘密样例，不写真实钥匙串、不调用供应商或模型。正式密钥继续由用户在本机页面亲自填写，此前授权的真实验收额度另行记账。

## 实现与验证

Connectors `worker/src/credentials/presentation.rs`、`page.css`、`page.js` 接入 Sorftime 专用投影；其他连接器原配置页不扩散修改。`scripts/sync-credential-design.py` 从 Desktop 提取实际使用的 tokens，并原样复制三个已接受 SVG，记录来源 SHA-256；`--check` 已通过。亮暗主题跟随浏览器的系统偏好，未新增跨进程主题参数。

私有 POST 保留原固定 Authorization/Bearer 语义和服务端复验。取消与提交争用同一个一次性 sender；已提交后取消只显示页面结束，不宣称撤销保存。空值和正常格式错误可原页纠正，响应不回显输入。提交回执仅表示请求已提交，保存/连接是否成功继续由易界连接器状态给出。脚本使用独立随机 CSP nonce；不外载资源、不读取剪贴板、不写 Web Storage。

本地检查：62 项 worker 测试全部通过，worker-lint（rustfmt/Clippy/契约与固定源码检查）通过，JS 语法与设计快照检查通过。普通本地测试覆盖空值纠正、取消不发送密钥、已提交后的取消、一次性提交、过期以及 CSP/no-store；没有触碰真实 Keyring 或供应商。

CUA 视觉检查使用生产 `page`/`presentation` 函数导出的 HTML 与原 CSP；1180×760 亮暗主题、390×844 错误/过期均无横向溢出。密钥显示/隐藏、空值焦点与本地到期提示已实际操作验证；提交回执、取消、已处理状态由同一渲染器和回归覆盖。预览工具仅切换 CSS media 条件来呈现两套已接受主题；3 秒 TTL 仅用于正常过期展示，不修改生产时限。截图见 `evidence/sorftime-credential-page-20261008/`。

真实 Sorftime 查询尚未作为本次页面验收执行；本阶段模型/供应商发现/业务调用均 0。此前 2 模型、2 连接发现、1 只读业务的授权继续独立记账。

实机补漏：Chrome 正常 POST 取消出现“已过期”，而 Native 操作仍在等待。以无密钥、普通本地表单复现：`no-referrer` 时 `originMatchesHost=false/originIsNull=true`，`same-origin` 时 `originMatchesHost=true/originIsNull=false`。根因是原私有凭据页的 Referrer-Policy 与严格 Origin 校验不兼容。将共用安全响应改为 `same-origin`，保留精确 Host/Origin/nonce；外站继续不接收 Referer，官方链接继续 `rel=noreferrer`。此修复适用于共用私有凭据表单，未放宽 Origin 校验或凭据格式。修复后 62 项回归及 lint 再次通过。未使用故障注入、攻击样例、真实密钥或外部请求。

最终标准构建复验通过：worker `5117eb8606ff5aa6e030ff32c46467948ce295ed0d582f725e54b373ac47ad1f`；App `ae8cfed5b6e43bc8ef9ba500f2863a44ae9c8ec5284c6d07c703e4e9def385fe`。从易界 Sorftime 详情实际打开新版页面，Chrome 中空输入点击“取消”后显示“已取消连接”，Native 同步为“连接已取消，服务未启用。”。操作已正常结束，应用留在 Sorftime 详情，无等待密钥的后台配置操作。两次仅本机 UI 会话均未输入密钥或进入供应商工具发现，真实调用预算未扣减；不把该检查当作 Sorftime 查询验收。最终证据为 `verification.json`、`canonical-app-build.log`、`actual.jpg` 和 `actual-cancelled.jpg`；前一次 `worker-build.log` 明确仅中间产物。

## 2026-10-08 文案跟进与重新输入

Owner要求增加本机保存/不上云的明确说明，并针对“服务暂不可用”正常重启后再试一次，由Owner重新填写密钥。本轮 contract-impact = none：仅私有安全页的说明文案和自动换行布局变化，不改变 IPC、认证、凭据保存/发送路径、错误或重试语义。文案准确区分“易界云端存储”和“向Sorftime认证”：“密钥保存在本机系统钥匙串，不上传至易界云端。仅用于向 Sorftime 验证身份。”

重启前应用已正常退出，无需发送退出或终止信号。62项worker回归、worker-lint再次通过，标准打包启动完成。最新18:57的两份受限诊断只显示Keyring预检成功、metadata_initialize unavailable，未提供HTTP状态，不能归因于密钥/权限/网络中的任何一个。它们是Owner自行提交后留下的历史观察，不算本轮agent发出的请求；本次重试由Owner最新消息明确授权。

为满足重新填写而不是复用已存Keyring，使用产品现有卸载确认→清理完成（已安装0）→重新安装Sorftime（待配置）流程重建本机连接引用。没有直接读取、导出或手工改写钥匙串。下一步打开安全页，由Owner亲自输入并保存；不自动提交、重试或发送模型/业务请求。

## 左对齐及初始化迁移补漏（2026-10-08 后续）

Owner确认已重新填写密钥并要求说明左对齐。最近19:19与19:20的两次初始化仍返回unavailable（约240ms），未到tools/list，未发业务查询；失败不自动重发。左对齐为纯展示调整。

审计发现FEAT-144/13已有明确成功证据：固定Codex客户端带真实版本User-Agent后Sorftime原生初始化成功；现有FEAT-157的Reqwest适配与rmcp默认头均不设User-Agent，迁移时遗漏了该兼容配置。修复方案使用本产品真实 `yijie-mcp-worker/<Cargo版本>`，不冒充浏览器或旧Runtime，不修改固定Codex源码。此证据支持补齐客户端标识，但不证明当前服务端拒绝规则或唯一根因。

contract-impact = semantic：私有provider HTTP适配补充真实客户端标识，受限诊断扩展元数据HTTP阶段（本地枚举+状态码）。公共IPC、keyring、目标URL、认证头、审批与重试规则不变；Contracts=N/A，权威为Connectors适配/诊断模块。验证为普通本机HTTP MCP初始化与工具发现、正常停止，检查线上的标识头及秘密不进入诊断；不调用外部服务。回滚为恢复前一可复现worker；同一新构建的真实复验须遵循此前“失败不自动重发”，本轮先完成可审查修复和本地验证。

实施完成：工作进程发出的允许请求带`yijie-mcp-worker/0.1.0`，元数据初始化/工具发现的HTTP诊断不再静默；审批调用继续使用原调用诊断。新增普通本机HTTP测试经固定Codex rmcp→真实Reqwest→本地标准MCP响应完成initialize/tools/list，检验UA、原Bearer和不含key/URL的诊断，正常停止。63项worker回归与lint通过；标准App重新打包启动。说明块与表单左边缘均为383px（1180宽），390窄屏换行通过。证据见`evidence/sorftime-user-agent-20261008/`。真实修复结果仍未确认；已按Owner“失败不自动重发”约束申请仅1次连接/工具发现复验、0模型/0业务调用，等待答复。


## 已保存密钥真实复验通过（2026-10-08 20:44）

Owner明确授权使用已保存密钥再做1次连接/工具发现，允许失败后的重试及必要模型调用。本轮从标准App的Sorftime详情点击一次“配置连接器”，由现有worker读取Keyring；没有读取/导出密钥，也没有再次打开凭据输入页。

操作`bc3fad0e-bed6-4f56-9920-7536bcebc935`的受限诊断确认：keyring_preflight succeeded、metadata_initialize succeeded、metadata_tools_list succeeded；三个元数据HTTP响应依次200、202、200。App清除旧错误，显示“已安装但未启用”，主按钮为“启用 Sorftime”。补齐真实worker User-Agent的构建在真实服务上已完成连接与发现，关闭此前修复效果未验证项；这不反向证明旧失败只有一个原因。

实际消耗：1次连接/工具发现流程、0重试、0模型、0业务调用。没有点击启用（该动作会再次发现并建立执行后端），本轮结论仅连接与发现通过；业务查询和批准/拒绝仍独立验收。没有新增代码、充值、订阅、Git提交或推送。证据见[evidence/sorftime-metadata-retest-20261008/verification.json](evidence/sorftime-metadata-retest-20261008/verification.json)及同目录受限诊断、实机截图。
