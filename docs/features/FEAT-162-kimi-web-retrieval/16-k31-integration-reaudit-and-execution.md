# FEAT-162 K3.1基线整合前复审与执行记录

2026-10-28。Owner已明确授权先完整审计15号方案，随后整合现有Search/Fetch、完成零费用验证与新构建；继续复用现有Key、保留数据与模型迁移成果，不改Codex内核。真实收费调用尚未授权。本文件先于本轮产品修改落盘。

## 复审结论与补齐项

实施方向成立，但不能直接整包恢复保全分支。最高契约影响仍为breaking（60→62目录reader、not_configured闭集错误、凭据交接/本地准备语义）；源契约先行、按当前K3.1消费者重新生成。以下遗漏先补入执行边界：

1. 保全代码含其它需求与较早FEAT164状态。只取明确FEAT162路径/代码段；保留当前writer4/reader5、SQL41、Host11、K3.1 profile/退役保护、模型暂停、正常退出和primary输出布局。Runtime r5源码/补丁/制品均不改。
2. 修正web-retrieval credentials残留的独立Keyring说明。Key仍由现有Host loader加载并用原匿名FD3交给worker；不读取/展示其值，不另建密钥持久存储。工具不按旧K3模型名选凭据。模型暂停/退役准入仍由现有模型链控制；工具本地准备不构成模型或业务HTTP授权。
3. 保留新primary worker `--output-root`接口，不恢复旧覆盖current.json的构建脚本；只增加web-retrieval来源检查。旧generation、数据、账本和预占不动。
4. 当前`daily:prepare`要求六源码仓已提交且干净，catalog与Host构建锁要求真实来源一致。当前指令没有明确Git提交授权。先完成整合/本地检查及可审查差异；如最终新generation必须本地提交，届时请求精确本地提交授权，不绕过clean/pin门禁，不推送。这是15号遗漏的构建前置，不是收费批准。
5. 新构建prepare-only不启动App、不打开原日常Home或迁移库。零费用正反例先用现有普通测试、合成内存值、canonical worker、本地HTTP响应和正常EOF；真实Key仅保留产品复用路径，本轮不为测试读取。实际用户数据App验收必须先满足新来源/无派发/正常启动退出要求，不能以构建通过冒充UI通过。
6. 原5元方案输入上界尚未实现，不能直接运行旧meter。收费方案将用新模型和当前可证明的费用预留单独给出；旧FEAT162及FEAT164台账不消费、不复制为新授权。

## 选择性整合清单

- Contracts：web-retrieval源/schema/generator/tests；market管理容量/默认意图、provider/broker凭据与本地准备、必要错误传播；保留当前native-display-archive-v5/native sources/model-call-surfaces-v2。只通过canonical生成/同步派生物，不复制旧source.lock或生成文件。
- Connectors：kimi_web/model_credentials；ProviderBackend与Gateway执行分支、providers本地准备、一次HTTP许可、凭据页面拒绝独立Kimi配置、目录/registry和普通测试；保留worker当前Runtime库兼容pin与primary输出发布器。
- Host：market_runtime装配、marketbroker凭据/owner及普通测试、旧零费用预检测试驱动；不覆盖app/session/native_process等其它差异。
- Desktop：连接器默认意图/本地准备、错误/文案、Kimi目录图标及测试；保留K3.1活动模型、所有迁移与历史reader和ExitOwner修复。契约、目录、Host/专家回执由原生成入口重建，不能伪造来源。
- Skills：仅必要的专家契约间接来源，内容/授权保持不变。

## 执行及结果

顺序：记录新鲜基线/精确差异→Contracts源与定向conformance→三消费者与Skills必要同步→普通离线测试及canonical worker→审查可提交差异→满足真实来源门禁后新generation prepare-only→检查制品/Runtime保持→提交独立收费验收方案。每次失败保留日志，修复需有证据；不运行强杀、权限破坏、攻击fixture或替身二进制测试。

本轮所有真实模型/Search/Fetch请求上限为0。以下实施结果按实际追加，当前未声明完成。

## 源码整合与实际检查进展

Contracts源先行恢复管理0.7、Provider/Broker0.6和web-retrieval0.2，Key语义残留已修正，当前native archive、K3.1模型源及Runtime保持。worker/Host/Native/UI已按清单选择性整合；Cargo正常解析只为worker根包增加现有reqwest0.12.28直接依赖，908项外部package记录逐字保持。

新发现并修正的方案遗漏：K3.1实际消费market-host/2等v2调用面，旧同步脚本会给Host写回v1 model enum，前端又出现not_configured不在v2闭集的类型错误。因此不能把旧消费者同步完成当K3.1整合完成。当前源已补market-host/2 0.5.0并canonical生成；selection/2与experts/2只刷新间接来源（业务shape/digest不变）。46项契约检查含新模型身份/旧形状/摘要保持与缺凭据错误通过。消费同步须沿原严格immutable脚本取得本次Contracts提交，不修改脚本放过未提交源。未启动App，不存在将中间v1生成物投入使用的行为。

已通过：14项worker Kimi普通测试、worker格式/Clippy与canonical新worker构建；58项Native连接器测试；63项前端连接器测试；Host现有K3.1准入/退役检查、凭据管道/解析检查、4种canonical worker本地准备、2种Manager K3.1实际装配；新worker全MCP预检（正常拒绝、0供应商HTTP、正常EOF）。worker SHA为129b2535bb83c92badb2a2654263cc71ada1d25f0651e9cf69e8d11fd7274f40，独立输出，旧manifest不覆盖。

保留的检查失败：首次前端测试revision10断言不匹配最终revision11，已按源修正；首次命令未排除.local，后改为4个精确活动测试文件且63通过，不把旧副本测试计入；Go本机默认1.26.4与项目1.26.5不匹配，现使用已安装官方1.26.5绝对工具链；新Manager测试的生成ID类型和新临时Home权限前置已修正，没有制造权限故障；新v2测试最初误把专家自身ErrorCode视作Provider错误，按真实独立域修正断言，专家wire保持不变。前端整体类型检查待v2消费者同步后复验，尚不记PASS。

当前需要本地提交的具体原因：`scripts/sync-model-call-surfaces-v2.mjs`从精确Git commit验证源与全部生成物；Desktop `scripts/feat164_primary.py::source_facts`要求六仓提交且干净。既有AGENTS禁止未明确授权自动commit，因此在本次Contracts源/测试已可审查、主要整合及零费用worker检查完成后，向Owner申请仅本需求的本地来源固化；不得推送、发布或借此调用收费API。批准后按依赖顺序提交并生成真实pin；所有后续相关检查通过才提交消费者，不以构建门禁要求为由跳过检查。

补充检查：v2源变更后的Contracts完整lint再次通过（12项既有unused OpenAPI警告）；Skills lint及2项canonical专家包测试通过，75项资源、38项普通Skills与73项历史版本保持。Native缺共享凭据的错误提示已明确，活动前端文件5项测试通过；首次同名过滤误包含.local副本，随后显式排除并以单文件结果为准。该5项目前覆盖默认validator，K3.1 validator及整体类型检查待不可变v2同步后复验，不冒充已通过。

续办顺序固定：授权本次必要本地提交→Contracts提交并canonical同步v2至Desktop/Host→验证K3.1 model enum、not_configured及原摘要→Skills小范围提交后canonical重包（先保全旧producer/slot），逐项比较75资源并从真实manifest/authority更新成对Host/Native资源来源→Connectors提交后刷新固定61项目录来源→Host检查后提交→freeze Host、更新Desktop准确来源pin并完成K3.1构建组合检查→Desktop提交→使用新generation执行daily:prepare。Runtime pin、模型权威5b5dad9d、计划权威2dd214d6及旧generation不变。原始日志在`.local/feat162-k31-integration-20261028`，不得把测试日志中的旧来源复制为新回执。

真实收费提案另列[17号](17-k31-client-e2e-proposal.md)：模型最多3次、Search/Fetch各1次、保守总上限¥43，基于整个模型上下文而非未实现的20k输入假设。该提案及对应新台账均未授权执行；本地提交授权不会开放收费调用。

当前检查点见[evidence/k31-integration-checkpoint-20261028.json](evidence/k31-integration-checkpoint-20261028.json)。七仓diff空白检查通过，Runtime工作树干净；旧20261028-02 App内119文件、旧Host/worker/adapter和Runtime二进制及manifest逐项与原回执一致。元仓lint/test通过。新App尚未构建，真实客户端UI/新模型E2E未执行；没有打开用户数据库或迁移数据，不以保护检查冒充数据库重开验收。

## 本地提交授权后的续办

Owner已明确回复“授权本次必要的本地提交，继续构建”。授权仅覆盖本次必要本地提交与构建，未授权收费、推送、发布或数据迁移。

按依赖顺序已固化Contracts `2adfa2bef43d38a932f6249dbb0a229c173ff103`、Skills `704d2cc85a85d0759e6103e3f539552f3d63b1e9`、Connectors `d88b8d0b8e95978ef3494c90bb5e0e619aa3a27d`、Host `20539889259587a66a574201e521c2ea9469c54d`、Desktop `446a5ac`。未推送。v2 canonical同步现已完成，Host生成物相对当前K3.1基线仅增加`not_configured`，不再丢失K3.1身份；前端整体类型检查通过。

专家producer及Native资源槽先完整保全再canonical重包，新旧75项公开metadata和归档逐字一致。新manifest `423621cd1da5087e7ee0ed575c985c4fd8e3b0fdf9c69db376f11fde1de51fa2`，authority `bdb53b6e776701bd767d8139e31d9dc467178a644639984f784f45903b690132`，Host/Native使用同一准确来源。Host真实资源验证通过37版本安装/读取/正常重开、0全局投影；首次测试传入含`..`路径被正常目录校验拒绝，改为规范绝对路径后通过，未放宽目录校验。

K3.1前端68项及路由2项、全部Desktop lint、Rust fmt和候选Clippy通过。首次用candidate feature宽匹配旧Native测试组时44通过/16失败：旧K3 fixture被退役准入拒绝，两个新模型case又缺少canonical候选环境；保留失败日志。改用既有S4候选环境/精确测试入口后4项通过，并新增K3.1选择kimi-web、冻结回执与正常重开1项通过。无需更改退役/数据库迁移逻辑，不能把首个宽匹配结果称为全量PASS。先前默认feature58项仍是单独的默认兼容证据。

19项准确提交来源生成检查、ordinary/market/experts/media四组合来源闭合检查和14项入口规则测试通过。新增primary generation `20261028-03`已按`pnpm daily:prepare`开始构建，使用已安装Go1.26.5及离线依赖。只prepare-only，不启动App、不读取真实Key、不访问用户Home数据库。最终构建结论随后补录。

最终补录：`20261028-03`标准构建成功，实际打包worker拒绝零请求预检通过。1231来源文件、新旧App各119文件及相关二进制摘要核对通过。完整结论、准确来源与未执行项见[18号](18-k31-build-and-zero-cost-results.md)。本轮授权的整合、零费用检查和新构建已完成；新客户端未激活/启动，真实对话与收费仍等待独立确认，FEAT-162 D4不变。
