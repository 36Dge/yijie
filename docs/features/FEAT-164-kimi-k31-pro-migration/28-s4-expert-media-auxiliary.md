# FEAT-164 S4 专家资源、媒体与辅助调用续办

2026-10-25，Owner授权先解决专家资源pin，再推进专家/媒体/辅助调用的安全离线验证；仅本地提交、不推送，真实模型HTTP新增0。总需求contract-impact=breaking保持。本批资源来源重新固定为semantic部署/资产兼容变更；若验证发现wire变化，须另行走权威源，不手写影子DTO。正常临时状态与loopback响应可以验证固定真实Runtime/Worker；不触发真实供应商、账号或商家操作。旧账本、预占、活动S1 App与原工作区全部保留，基线见`s4b-start-baseline.json`。

## 执行前审计与方案

原Native pin对应bundle0.25.0、75项资源、working-tree4247a4f；现有producer输出为working-tree595c927。两者tree_sha256一致。干净Skills595c927已通过原Contracts leaf消费检查，原源码无新增修改；两次标准打包得到77文件逐字一致，75归档和全部公开条目与原producer完全一致。仅在内存恢复旧source元数据即可重算得到原Native manifest摘要033689b，证明旧差异不是内容变化。证据见`s4b-expert-reproduction.json`。

本批以Skills完整commit595c927和不可变git-commit来源产生独立FEAT-164资源pin、producer output与Native slot，旧FEAT-158 pin/output/slot不覆盖。Host与编译的候选Native都选同一新pin，普通构建保持原选择；不能把renderer或env任意hash作为权威。原75个版本/归档/角色/知识摘要、原安装和历史均保留，先验证真实受管安装/解析/重开再进入Runtime组合。

进一步检查canonical Worker/媒体adapter固定源码和库来源，再用标准构建生成独立可复现开发产物，正常EOF清理。辅助调用使用固定Runtime的原生代理/审批/压缩入口与本机合成Responses，不创建协作子agent处理本任务，不修改模型结果，不启动真实模型请求。暂不重建活动S1 App，不将headless结果写成App/平台或完整G3通过。

## 实际修复与固定来源

| 仓库/资源 | 本轮不可变来源 | 变化 |
|---|---|---|
| Skills | `595c927ae101d3d31c234f60565041eee0864680` | 只读固定源码；没有修改或提交Skills，原dirty candidate保留 |
| Connectors | `1f157260d6dd339172712e1c649258902db45050` | 保留Worker原库pin7fd463b，只允许明确登记的Runtime074417e5 wrapper，且每次校验其codex-rs树完全一致 |
| Host | `03d26a374fd5ea0dfd238276b735d445e93d4f2e` → `cac2d4d7e1df02868a370e204959e1842c3362c3` | 候选专家pin、进程级本机计量路由、专家/媒体/辅助调用验证；后续提交只补强原生子代理completed判定和集成测试显式opt-in |
| Desktop | `cba29c4e6c125817c0bd109ba966b58d0e05926f` → `56f52843b543a4276eb6221abf3d589582b8c480` | 独立专家pin/slot/同步入口/资源overlay、固定上述Host和Connectors、严格非零离线driver |
| Contracts / Runtime | `eddc64f95d81c26ca1678cc648d177c081f7904d` / `074417e5e2f5f55704ea5e1777e7a22d514076b4` | 本轮未修改；真实Runtime继续使用既有canonical r2制品 |

新资源manifest为`3facbb1a63f15f6e9c089b61955c2edc34f341d89dd659175131d246909f76ed`，authority为`7f3eb9424e00bfc588b3962a2532d0225aa593cf5e6a537a0e6c374f61dddba0`。75项资源/公开metadata/归档逐字不变，保留73项历史基线和38项普通Skills。新pin同时嵌入Host与候选Native；普通构建仍使用原pin。所有原manifest/authority/授权/角色/知识/归档校验仍执行，不接受调用方任意摘要。

原工作区`sync-desktop-expert-resources.mjs`含其它需求的未提交重构。首次apply-check在写原仓之前拒绝冲突，随后采用独立`sync-feat164-expert-resources.mjs`，复用原受管文件/归档校验helpers；旧脚本逐字保留。候选producer输出为`dist/skills-experts-feat164-s4`，Native资源槽为`.local/feat164-kimi-k31/skill-packages-experts`。新同步入口要求显式local/demo_fast/K31、干净且HEAD等于固定Skills来源；Host/Native pin逐字段相同。未使用原dirty资源刷新摘要。

Worker的原库7fd463b与Runtime wrapper074417e5的codex-rs Git树均为`755f32c45a4c30e805e3c7fe1db89dcb4dcc6e41`。兼容名单只有这一明确完整commit，检查仍拒绝其它HEAD、不同库树、tracked差异、未跟踪源码和原依赖/Rust/schema锁偏离。公共wire、Provider、凭据、工具权限和库版本均未变。canonical Worker及artifact adapter只写独立本地构建目录，未覆盖活动App或既有binary。完整来源与摘要见[构建记录](evidence/s4b-build-provenance.json)。

辅助调用的关键修复是把已选择的本机meter同时写入Runtime进程provider配置层，保持原thread覆盖。候选且已有受限loopback meter时，Kimi/MiniMax均指向同一meter且request/stream retries为0；未启用候选/未选meter保持原逻辑。外部环境装配仍只接受18083/v1，测试私有Config才允许动态loopback端口；没有新增外部目标、审批绕过或自动授权。这样子代理、Guardian与压缩不会因读取进程配置而绕过本机计量。实际config/read已核验两条provider URL。

## 验收范围与未执行项

专家/媒体测试使用真实资源服务、领域grant/submit及原回执重放、canonical Worker、固定真实Runtime、项目标准构建的artifact MCP adapter和已认证Host路由。媒体只登记普通临时HTML/SVG文件，并核对真实staged回执、ready完成事件和资源字节。没有前端ACK/WebView断言，不将后台资源读取称为UI验收。专家配置仍禁搜索，本轮未调用外部商家工具。

子代理从父回合继承K3.1 Pro/max，核对原生wait的completed正文与持久化child记录。Guardian对用户明确要求的普通临时文件复制走原生审批，并核对实际文件；合成模型评估只证明调用身份/路由，不证明真实模型审批质量。压缩使用正常thread/compact/start和真实contextCompaction完成状态；没有制造超大输入/耗尽上下文或模拟攻击。辅助验证是产品原生能力测试，不是将本开发任务委派给协作agent。

本轮仍未执行：同源canonical App打包/打开、WebView亮暗/窄屏/权限与媒体渲染、当前新源旧隔离历史的完整UI重开/暂停Kimi/MiniMax回退、跨平台、自动大上下文压缩/已加载旧模型子代理跨cutover，以及真实供应商图片/搜索/工具质量。前几项受活动S1 App和用户离机延期约束；平台/真实调用也没有当前授权或环境。安全长期禁止的强杀、权限破坏、恶意fixture/攻击注入和程序替换一律未执行，不能据此伪造异常路径PASS。

完整TINV-164-04/TCONF-164-04仍NOT RUN，S4 boundary/vertical/G3、当前源G2V与三个final继续pending。这里的离线扩展PASS仅证明本节明确覆盖的来源与路径。

## 诊断与纠错记录

早期harness曾使用错误Worker library-home、媒体namespace/session ID/ready状态和agent wait参数；均按固定源协议改正后复验，不修改真实Runtime回执来适配测试。首次Skills检出命令在错误仓库执行失败，随后从实际Skills原仓创建detached检出；原文件未改。依赖目录改用忽略目录中的包链接，保持producer源码干净。初次子代理断言只检查wait有一个结果；复审补为精确completed正文，并在最终固定来源重新执行。所有草稿失败只用于诊断，不累计成产品通过。

## 最终验证与保护审计

最终干净来源矩阵见[evidence/s4b-qualified-final/result.json](evidence/s4b-qualified-final/result.json)：ordinary/market/experts/media四组合来源全部PASS；Host资源1、专家/媒体3、辅助4、Native资源1全部PASS且0skip。37专家版本正常安装/解析/重开，0全局专家Skill根；新扩展13次loopback（专家1、媒体3、子代理4、压缩2、Guardian3），新增真实模型HTTP为0。旧S4安全子集7/4/4/4/5、S2 25/2/12/10/1、S3五项在最终来源复验通过。子集边界不变，不当完整TCONF/G3通过。

ESLint、Shell语法、Rust fmt、候选Clippy lib、默认Rust check及相关Go vet通过（s4b-final-*日志）。TS/Vue与公共wire本轮无改动，未重复扩大到全量前端/危险fixtures；保留前轮202前端结果和既有无关基线失败，不能把旧结果标为本轮重跑。没有全量generate/test、强杀或真实网络业务。

[保护审计](evidence/s4b-preservation-audit.json)逐项核对本轮基线7仓496个既有变更文件；对重叠文件只在临时副本逆向移除本轮差异后比对原字节，跨仓隔离清单见s4b-*-isolation.json。154个原忽略资源文件、42个活动S1 App文件及两份旧账本均逐字保持；fixture18083仍只有原1请求，S1 readyz18086仍ready。累计30元、2/2 HTTP已耗尽、14.188544元未知预占+0.139590元保守费用=14.328134元上界保持；剩余费用不产生新调用许可。.lock不暂存。全部仅本地提交，无push/tag/PR/发布。

## 下一步执行顺序

1. 当前离线目标已完成。用户能操作电脑时，先让活动S1 App通过应用自身正常退出，确认Host/Runtime/fixture正常清理；不可强杀或覆盖活动bundle。
2. 复用本节固定来源和专属资源槽，按canonical入口构建同源候选；先本机meter正控，再做正常UI重开、旧隔离历史、暂停Kimi/MiniMax回退与专家/媒体UI组合。日常库仍不迁移，不从余额推断真实HTTP许可。
3. 补当前来源G2V、S1—S4完整G3、跨平台/freshness和三项final所缺的适用证据。已加载旧模型子代理/自动压缩cutover单列验证边界，不能用新建子代理/显式压缩替代。真实供应商质量若必需，另需明确调用次数授权；本轮不请求、不执行。

最终复审另将两个要求专属资源/二进制的集成测试改为显式opt-in：普通测试缺少路径时清楚标记SKIP，不阻断无产物的日常测试。专用driver在启动前要求全部产物存在，并强制每组精确命中数及0skip，不能借默认跳过取得验收PASS。调整只影响测试入口，产品代码不变；s4b-*-before-optin保留前次同产品代码结果，最终固定来源重新执行于s4b-*-final。

治理复核：claims与strict均PASS，元仓lint和53项治理测试PASS；[G3实际门禁](evidence/s4b-g3.log)仍拒绝放行，缺口为当前G2V、前置slice、完整TCONF及App/平台/freshness，未关闭或绕过门禁。完整结果与命令见[s4b-governance-results.json](evidence/s4b-governance-results.json)。

差异检查保留原始cargo日志末尾空行及其SHA；9处空行只存在于原始日志，源/文档/JSON差异检查通过，未改写日志制造绿色，详见[s4b-diff-audit.json](evidence/s4b-diff-audit.json)。
