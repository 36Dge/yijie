> 已获用户明确授权并执行。最终来源、普通App入口、打包/恢复结果见[本地交付报告](04-local-delivery.md)。下文保留批准时的范围和顺序，不表示仍在等待授权。

# FEAT-152 提交与本地交付清单

状态：第1项整理完成，等待用户明确的本地 Git 提交授权。S1–S4/D4既有完成结论保留；本节记录后续固化交付，不开启新的功能需求。未提交、未推送、未打tag、未发布；本轮0次模型调用，原账本仍37/45。

## 四仓提交顺序

| 顺序 | 仓库 | 建议提交标题 | 当前准确范围 |
|---|---|---|---|
| 1 | yijie-contracts | feat(FEAT-152): define native runtime permission contracts | 7个文件：新权限OpenAPI、生成Go/TS、专属生成入口、conformance与source-first评审。 |
| 2 | yijie-agent-host | feat(FEAT-152): adapt native permissions and approval decisions | 17个当前文件，加实际Contracts提交的独立pin；原生模式/请求/自动审核/接管适配、会话/恢复、正常测试及本地计数支持。 |
| 3 | yijie-desktop | feat(FEAT-152): deliver task permission controls in local demo | 33个当前文件，其中2个仅部分片段，加实际Contracts/Host pin与必要的既有预检接入；Native存储/IPC、UI菜单和卡片、日常入口/重试和相关测试。 |
| 4 | yijie | docs(FEAT-152): record verified local delivery and source pins | 仅本Feature Package及本次交付记录，登记前三仓实际完整SHA、依赖与构建证据。 |

机器可读的逐文件选择、内容hash、排除清单和patch校验见 [commit-manifest.json](evidence/delivery/commit-manifest.json)。三个实现仓的候选patch已生成到 `yijie/.local/feat152-delivery/`，实际执行 `git apply --check --cached` 全通过；没有修改真实索引。提交时重新核对HEAD、已暂存内容和文件hash，任何漂移先重新区分来源，不覆盖工作区。

## 两个必须部分提交的文件

- Desktop `package.json`：仅选取两个本地App构建命令中的权限启用配置。`icons:sync`、`icons:check`及其脚本不纳入本次提交。
- Desktop `src/components/chat/ChatComposer.vue`：只提交 `permission-control` 插槽。当前hover/focus/drag边框改色不纳入本次提交，原样保留在工作区。

Desktop其余43个文件/删除记录排除，包括导航组件配色、设计规则/颜色文档、proposal删除、App图标及图标同步脚本、聊天构建同步报告。权限图标在通用registry里的新注册属于FEAT-152，应纳入。

2026-09-08已有的日常启动器双开关、取消对验收代理的必选依赖、新建任务/继续任务菜单与失败重试检查，确属本需求交付范围，当前文件差异已核对后纳入。它们与其它界面任务的改色分开选择。不会把整个Desktop工作区直接 `git add -A`。

## 依赖固定方案

保留旧v4、Skills与retained Runtime固定来源；不改Codex核心或二进制、不重新启用FEAT-137。新权限契约族版本为0.1.0，独立记录，避免重写旧v1–v6锁与历史证据。

1. Contracts提交成功后读取该真实完整SHA；从该提交Git对象核验原OpenAPI、bundle和Go/TS生成物摘要，不能用浮动HEAD或工作区内容冒充已提交来源。
2. Host新增 `api/runtime-permissions.lock.json`，固定上一步Contracts完整SHA、0.1.0契约族、源/消费摘要及生成器身份，确认现有消费文件与固定Git对象一致，再提交Host。
3. Desktop新增 `contracts/runtime-permissions.lock.json`，固定实际Contracts与Host完整SHA、Host的上述lock摘要及FEAT-152实际消费/实现源摘要。复用现有本地权限预检核对这些对象，不替换旧v4/Skills/Runtime校验。
4. Desktop提交后在元仓Feature Package登记前三仓SHA与验证/打包结果；元仓自身提交SHA由提交完成后的交付回执记录，不写自指的虚假SHA。

新SHA必须在前仓实际commit之后产生，因此当前不预填不存在的commit，也不把候选patch hash当作commit。未来新增lock及最小预检接入属于用户已要求的“固定依赖”，完成后先验证再提交消费者。

## 本地入口与打包安排（在提交和固定来源后执行）

- 复用canonical normal/stable本地入口，权限默认ask、Native与renderer同时启用；本地启动不要求手动运行验收计数器。明确移除临时复核策略环境变量。
- Skills当前HEAD为 `488714a8d96f40806a257aae097683815b1dd458`，与旧独立固定来源不同。沿用已存在且核验干净的 `.local/skills-pinned-10c45be`，通过现有配置覆盖/入口解析消费；不改Skills源码、不擅自更新旧pin。
- 不复用遗漏FEAT-152的旧隔离App。以最新已接受代码与本次固定来源构建；其它仍未提交的本地界面/图标改动继续保留，若进入本机包则单独登记输入hash，不伪称为纯净提交制品。不会为了让构建目录干净而回退用户改动。
- 正常退出旧App后构建/启动；若任务仍运行或不能正常退出，停止相应步骤并反馈，不强杀。现有用户提供/签名App和retained Runtime不覆盖，只使用项目canonical可复现开发产物。
- 验证正常免登录启动、三档菜单、新任务ask、既有任务模式读取、正常重启恢复和实际运行包来源；本轮交付核对不提交模型任务，不消耗剩余8次额度。
- 本地未签名开发包及正常入口说明/制品hash进入交付报告。推送、远端合并、tag、公网或生产发布不包含在本次提交授权请求内。

## 已完成的零付费检查

- Desktop `pnpm lint`：PASS。
- 6个聚焦测试文件：80 PASS、1 SKIP。跳过的唯一旧用例包含script注入，遵循用户长期安全条款，未执行攻击注入或篡改验收结果。
- Contracts两项基础检查PASS；随后使用S1真实保留Runtime配置观察复核，第3项也PASS。该检查读取真实既有证据，未发起新Runtime回合。
- 不设置验收代理的本地入口Contracts/Host预检：PASS；不代表固定新FEAT-152 commit已完成。
- 三仓候选patch的索引适用性：PASS；Codex核心干净；未暂存、提交或触发付费调用。

## 本次需要确认的唯一动作

请用户明确授权按本清单依次执行四仓本地Git提交及必要的实际依赖pin，随后完成已要求的本地打包与零付费入口验证。授权到位后连续推进，不重复请求同一提交授权。

此确认来自用户本轮第2条“获得提交授权后”，以及项目长期规则“commit、push、tag、发布、生产迁移和外部写操作仍需要段成威的明确授权”。前置变更/候选patch/验证已准备，尚未越过提交边界。

准备过程中另一个任务新增 `docs/verification/FEAT-152-ui-integration-fix-20260908.md`，同时覆盖入口和首页配色。该混合报告原样保留并排除本次提交；其中入口变更已通过当前源码、独立测试和既有构建证据交叉核对。没有将其配色工作混入权限提交。
