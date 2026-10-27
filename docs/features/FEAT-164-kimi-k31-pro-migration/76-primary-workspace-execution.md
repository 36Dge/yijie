# FEAT-164 第76号：原主工作目录构建运行

2026-10-28。**目标已实现：从原`CrossBSD/yijie-desktop`实际源码构建并运行，当前generation为`20261028-02`。** 新来源三轮真实启动、只读模型目录、正常系统退出及完整后态通过；Mac锁屏使App历史界面检查按Owner指示跳过，未记PASS。当前App已正常退出。最后治理检查结果见文末及[机器证据](evidence/primary-workspace-execution-result.json)。下方初期方案/进度保持历史含义。

Owner本轮要求方案形成后再审计、继续实施并修复阻塞，直到直接从原`CrossBSD/yijie-desktop`实际源码构建运行。随后明确“移除审计”为笔误，意思是“再做一次审计”；本轮不清理目录、不删除旧daily-source。第75号历史只读结论保留。

## 当前实施决策与边界

采用第75号A方案：先完整保全所有现有工作及相关旧产物，验证独立恢复；五仓未采纳WIP独立本地保护，不将writer5、Contracts0.5.0或其它需求默默启用。随后在原物理主目录选择已验收FEAT-164基线；其源码为真实编译输入。原分支和新保护引用保持，禁止reset/stash/强行覆盖。保护提交仅是未验收工作检查点，不是产品提交。

新增私有primary部署接口，contract-impact=semantic；权威为Desktop部署规范、构建入口与回执，公共wire/SQL/Runtime不变。v1/v2维持旧分离来源语义，新增v3仅允许原主checkout与原数据Home精确绑定。新输出位于原Desktop`.local/builds/primary/<generation>`，只含制品/回执/授权，没有第二份活动源码。原`target/debug`和旧App不覆盖；前端dist/Skills再生slot先保全再由canonical生成。Worker采用独立target和manifest输出，保留原manifest。D3不再执行。

Runtime r5、writer4/reader5、原Native身份/SQL41、Host11、原Provider引用、权限/计划授权、unknown不重发及workflow ready-only保持。没有新模型调用，不推送；Runtime核心/补丁若确需修改仍须先给具体方案确认。部署启用不是模型发送或工具批准。

## 顺序与验收

1. P0：12仓新鲜基线、全部WIP与必要旧产物归档、元数据清单、独立恢复校验；五受影响仓全部refs制作bundle并在独立bare仓验证，覆盖6个独立tip。旧缺失归档不能充当本次保护证据。
2. P1：逐路径审定258项WIP的保护位置与活动状态；23交叉已有逐段审计，本轮首版不合入未采纳WIP。依Contracts→Host/Connectors/Skills→Desktop选择原主目录精确来源。所有不参与源码的缓存也保全，不作清理。
3. P2：先冻结v3规范及普通样例，再实现受限输出布局、源码/receipt绑定与仓内prepare/open命令；复审后安全离线测试。保留原v1/v2兼容，不放宽原准入或自动刷新摘要。
4. P3：从原主目录canonical实际构建新制品，来源/生成/编译/安全检查及prepare-only通过；不能以转调daily-source或旧App代替。
5. P4：新鲜完整冷备份及副本一致性/全模型无待派发检查，实际workflow ready、实例锁与无占用确认后，Kimi暂停受限启动、历史检查、正常退出及后态审计。依赖未就绪先定位并明确恢复范围，不隐式重建/迁移。
6. P5：实际新候选来源绑定启用及仓内普通/暂停入口验证；不新增模型验收，不清理旧来源。失败正常退出后可受控回到兼容旧来源，不覆盖新数据库、不降schema、不删WAL。

既有never-sent安全分层替代保留；完整App正向取消仍NOT RUN。搜索答案正确性、亮暗/键盘/最小窗口专项仍OWNER_EXCLUDED，不重新计为待办或PASS。

## 实施前再次审计

方案的关键约束逐项核对：当前258条WIP不是可直接复用的已验收输入，必须先保护；原部署拒绝同址是明确语义，需要新版本而非删断言；新target与receipt必须同源解析；只改worker target不能隔离current.json；原Home与输出必须分离；不依赖已消失的旧归档；不把旧D4证据套给新来源。以上均已进入本方案。

本轮授权解释、逐路径保护清单、复核结果、每步命令与实际结果保存在元仓`.local/primary-workspace-execution/20261028-01/`。阶段结果随后据实追加；本段不是完成声明。

## 当前实证进度

P0/P1完成：新压缩归档703,062,946字节、1,629成员、504条当前WIP（含本轮新增方案文档）独立恢复校验通过；内容、mode、ACL、mtime保持，8条macOS provenance/quarantine运输元数据差异原值完整记录。五仓全部refs分别制作两轮bundle并独立bare恢复/fsck；第二轮包含254条源码保护检查点。4个缓存按精确清单保全到私有目录。原分支HEAD未移动，日常Home未迁移；原主目录已正常选择Contracts d5792d6、Host7309101、Connectorscc56cda、Skills595c927、Desktopa211c2d基线。

P2完成：Connectors本地提交`8e62101ff8ca94c2f9e12f4e415f20df41a7deed`仅构建输出接口/测试/文档。Desktop `02aa396dcf3ccdafa70d76b0d4d286af9de284c4`实现primaryv3，后续`08cdb4d`通过canonical生成补齐不变catalog的新来源pin。Worker业务、catalog、API字节不变，无Runtime/Native/公共wire更改。30项Python、9项Node、63项当前启动/回执测试PASS，文档构建及聚焦eslint/Python/Shell语法PASS。

保留失败及RCA：首次备份在metadata清单前发现当前Python没有os.listxattr，改为Darwin只读ABI后新目录重做，原件未改。首次focused Vitest误选`.local`旧checkout并使用`/var`别名临时目录；以既有排除规则和规范fixture根修正调用，63当前测试通过，产品校验未放宽。首次19项来源检查在第12项catalog旧commitpin停止；证明catalog/worker/API无差异后修改权威generator并canonical再生，第二次19项全部PASS。

P3进行中：专家资源已由原Skills595c927正常打包并同步，38普通＋37专家资源；从原Desktop启动canonical `pnpm daily:prepare --generation 20261028-01`，输出在本仓`.local/builds/primary/20261028-01`。尚未据此声明App构建或运行通过。0模型调用、不推送、旧daily-source保留。

## 最终来源、入口与验证

原主目录当前Desktop `24a231f96f08ed077e53f9bd73a2aac93ee6cba8`，Connectors `8e62101ff8ca94c2f9e12f4e415f20df41a7deed`；Host7309101、Contractsd5792d6、Skills595c927、Runtime11fd450/r5保持。五仓工作目录位于原兄弟仓，使用`feat/feat164-primary-20261028`；原分支不移动，未采纳工作留在各仓`retained/primary-wip-20261028-01`及新bundle/压缩归档中。不是将WIP一并判为完成，也不是由原仓脚本转调旧daily-source。

```bash
cd /Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop
pnpm daily:open --generation 20261028-02
# 需先正常退出，再切换暂停入口
pnpm daily:open --generation 20261028-02 --pause-kimi
```

新App位于原仓`.local/builds/primary/20261028-02/target/debug/bundle/macos/易界 AI.app`，该generation只放制品、回执和授权，没有源码worktree。App SHA `c2f5cba634bf4a8d567b534e798d86a076e5a53d98183afd5ce780f8c40a3629`，receipt SHA `28141579143c6da10ac47f11a164e7394cec83ae3559aa9dd50db5057c4cd915`，schema3 D5 binding SHA `169d6713703abaaf35ad84fdcdbdc0778159fec0a18cf50f1bd4a339ad80a87c`；1230输入、119包内文件。App/Host/worker实际进程链均指向此主目录的新产物，Runtime仍为原仓r5；无daily-source活动依赖。没有重建已缺失的桌面.command。

三轮分别为D4暂停、D5正常、D5暂停。真实Host ready200，带既有本机bearer的只读catalog确认正常入口Kimi K3.1 Pro/max/1048576可用，暂停入口为activation_required，MiniMax两种模式均可用；旧K3不在活动目录。只读catalog不是模型请求。每轮系统Quit经ExitOwner完成，停止代120→121→122→123，Host所有值、Runtime业务/rollout和Native原历史/授权保持；最终17401文件/522889712字节完整后态备份，活动WAL/SHM0、无进程/句柄、实例锁释放。未重跑D3、未搬库或手工checkpoint。

初始generation01虽构建/启动成功，系统Quit未进入自定义清理链，**退出资格FAIL保留**。按[77](77-primary-system-quit-root-cause-and-plan.md)修复Desktop自身标准AppleEvent入口后新建generation02，并由新App正常打开/退出处理遗留WAL。旧失败候选、原WAL完整副本和日志均保留。全轮4次实际启动中，最后3次为合格新来源；新增模型HTTP0，最初启动带来既有provider只读metadata HTTP3，合格三轮为0，业务工具0。

## 已保全、未执行及回退

501项原WIP的恢复内容逐项复核通过；254源码路径已独立检查点、4缓存保留；七账本及两预占与原HEAD字节一致。新归档703062946字节、SHA `c1e32f97959cff5a8c9ec82b748e817063e8d0e1053425231262f8d02f566d47`，独立恢复1629条目；五仓最终bundle全部refs独立恢复/fsck通过，包含六个独立tip与保护检查点。581个原App/Runtime/worker关键文件及旧fixed-source的119个App文件保持。旧顶层preservation在本轮开始前已缺失的事实保留，新备份不冒充恢复了旧74份归档。

Mac锁屏：本轮App历史界面观察`SKIPPED_MAC_LOCKED_PER_OWNER`，不是PASS或永久移除；历史库副本可读、旧行保持与实际服务/模型目录另有PASS。旧never-sent接受替代、完整App正向取消NOT RUN及搜索质量/外观专项OWNER_EXCLUDED完全保持。没有借此扩展public/cloud/多人/签名或跨平台发布。

没有清理目录。旧daily-source及其绑定/制品仍保留作受控回退来源；原主目录来源漂移时新入口拒绝启动，应先审查、canonical新generation构建及绑定，不能刷摘要。回退先正常退出、保全当前数据、检查兼容性和来源；不能以旧入口缺失或旧归档缺失为理由覆盖日常库、降schema或删WAL。原未采纳工作可从保护分支/新bundle/私有归档审阅恢复，不能把整份WIP直接启用为已验收来源。

额外观测纠偏保留：新私有mapping检查最初错把Native内部session ID当作Host public task ID，改用实际public-task绑定join后8组匹配；新只读SQLCipher工具从本次canonical静态库构建并用普通加密fixture验证，原工具pin未改；后态脚本最初把历史UI probe的3次metadata当作固定启动要求，现仅在无任何provider操作/增量/诊断时接受0，发生probe仍保留原严格约束。初期runner复用offline描述标签的错误单独记录在`runner-scope-corrections.json`，原process记录、实际启动命令及进程证据不改写。

安全验证：19项来源资格、104项聚焦测试、Rust Clippy/fmt、脚本语法、聚焦eslint、文档构建通过；未运行历史攻击/权限破坏/强杀fixture。最终元仓lint、57项治理测试、claims、strict/G6及7份Shell语法通过。首次文档检查因新证据只有HTML锚而缺机器要求的唯一evidence marker停止；已补齐正确标记并复核全部门禁，原失败日志保留，未改校验器或降低断言。本轮差异仅本地固化，提交号以Git记录为准；不推送。
