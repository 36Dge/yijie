# FEAT-158 日常客户端接入（2026-10-13）

用户明确授权将FEAT-158接入日常客户端，要求保留现有数据和历史会话、只做必要验证、控制模型调用，外观继续跳过。日常接入已完成；本次独立核对了原数据迁移、实际执行和同构建重开，阶段11的隔离候选D4及原始评分保留。

## 实施边界与兼容方案

本次增量 `contract-impact=semantic`：改变canonical本地启动默认值与部署选择，复用已实现的SQL33→35、Host8→10增量迁移与兼容reader；没有新共享wire、Runtime修改或新的存储版本。整个FEAT-158的既有breaking分类不改写。权威源是Desktop启动器/闭集部署表及两仓既有迁移实现。

直接把原专家候选开关设为true会切换App身份和数据根，不能满足日常接入。采用现有部署表增加daily项：保持`com.yijie.ai`、原`demo-fast-v1` SQLCipher与密钥、`.local/demo-fast` Host/Runtime Home、18081端口、原Host binary路径及日常单实例锁；仅增加专家资源overlay。原隔离profile继续独立，既有普通Skills沿用原安装根和版本，不将专家变成全局Skill。显式false回退保持新版兼容reader，禁止数据库降级、重置或改写旧outbox。

默认启用仅适用于现有daily模型/市场/权限组合，stable、旧模型、隔离定时验证和workflow特定入口保持原边界。模型参数、连接器审批、计划授权及旧历史读取不因部署选择获得新的执行权限。原生启动、Host和Renderer三个入口保持同一开关。

## 升级前事实

日常客户端已停止，文件无打开者。复用既有SQLCipher/Bolt只读检查器，仅记录表/桶计数与内容摘要，不输出密钥或用户正文。实际日常库为SQL33、Host8，包含5个会话、22轮、44条消息和30条outbox；Runtime历史6个文件。原已安装普通Skill文件6份。

原加密数据库及WAL/SHM、Host数据库已复制到项目私有`.local/feat158-daily-preservation-20261013-012949`，4份文件逐字一致；原密钥保留原保护路径，不导出。证据见`phase12-sql-before.json`、`phase12-host-before.json`、`phase12-data-preservation-baseline.json`和工作树基线`phase12-baseline.json`。

## 必要验证

先验证daily/隔离/false/stable启动选择、共享单实例锁、SQL33→35历史保留和Host兼容reader，再经canonical构建启动原日常App。核对升级后旧表/桶摘要、原会话与普通Skills、专家目录与本地资源准备、正常退出重开。优先0新增模型；如确有日常绑定/执行证据缺口，最多补1条合成问题，不重跑内容评测、不执行平台业务操作。遇到新错误先查根因，不重复调用碰取成功。

## 实际结果

普通入口 `./scripts/run-local-demo-fast.sh --packaged` 已默认装配专家，不再需要环境变量或独立候选参数。原始隔离身份仍可用 `YIJIE_EXPERTS_ENABLED=true ... --experts-local` 选择，三个内容profile参数不变。本次只改变Desktop部署选择、回执中日常Host路径和单实例分支；Host、Runtime、共享契约、内容包和迁移SQL均未修改。

canonical构建通过后，两次正常Quit退出码均为0、18081端口正常释放；两次 `--reopen` 均通过原来源与同制品检查，没有重建。最终App保持运行，原生会话 `01a13135-dcf7-7bc1-9c47-9c7b0d040e80` 的专家0.1.3、Kimi模型和已完成回答恢复。回执SHA为 `b13b187a2c6318234134bcd67ab5d3f089ebd32656df817e346ac9239a847997`，App SHA为 `335b54c49ee50ab59ccd19accae27f41db3c50fb5987029027a1c433e644a3a4`，完整来源见 [日常构建回执](evidence/phase12-daily-build-receipt.json)。

### 原数据保留

| 检查 | 实际结果 |
|---|---|
| SQL33→35首次启动 | 原63张表中仅迁移账本从33条增至35条；62张旧业务表计数与原列摘要完全一致，新增4张专家表均为空 |
| 完成一次合成调用后 | 对原加密备份与当前库执行只读逐行摘要包含检查：原63张表的667条记录全部保留，缺失或变化0；原33条迁移记录也全部保留 |
| 当前数量 | 6会话、23轮、46消息、32outbox；比原数据仅增加本次合成专家会话及其正常发送记录，原5会话/22轮/44消息/30outbox均在 |
| Host8→10 | 新增3个专家桶；原8条会话全部保留，逐字段比较仅4条的`updated_at`在正常启动/恢复时更新，身份、内容索引、状态等其他字段完全一致；合成调用后另新增1条会话 |
| Runtime历史 | 原6个历史文件逐字不变；只新增本次合成会话文件，没有重发旧轮次 |
| 普通Skills | 发票生成仍安装且启用；原5份安装内容/回执文件逐字不变。共享操作journal在正常准备专家时增加操作，不将该文件的合法变化称为未变化 |

证据：[升级对照](evidence/phase12-upgrade-comparison.json)、[原记录逐行保留](evidence/phase12-original-row-preservation.json)、[Host逐字段对照](evidence/phase12-host-final-session-diff.json)。检查器仅以只读方式打开SQLCipher/Bolt，密钥仅在本机检查进程中使用并清零，不输出密钥或历史正文，不手工改库。

### 最小功能验收

打开一条原日常会话，5轮历史可见、已完成、未被自动绑定专家；原有`conversation_warning`如实保留，不伪称历史所有内容完整。扩展默认技能页与已安装发票Skill保留；专家通过原受管安装器准备后返回草稿，版本0.1.3且未自动发送。

唯一新增问题使用合成文本；实际Kimi-K3/max、on-request、workspace-write/network=false原生执行完成，唯一工具调用为读取日常安装路径中的 `references/m03-listing.md`。无联网、连接器业务调用或文件写入。普通新草稿无专家，最终重开后本次专家会话及其回答、模型、绑定恢复。详见 [实际Runtime记录](evidence/phase12-daily-runtime-smoke.json) 和 [最终验收](evidence/phase12-final-acceptance.json)。

本次模型1条，FEAT-158累计29条；外部元数据0、平台业务0。没有重跑固定内容题，AC-007移除决定与外观SKIPPED均保持。

### 检查与审查

4个启动/部署/来源/UI开关文件的定向测试52 PASS、1个显式来源检查用例SKIPPED；实际来源检查由canonical构建/重开另外执行并通过。SQL33→35历史保留和日常/隔离锁各1项通过，Host正常重开与feature-off reader共3项通过；Rust格式、all-targets Clippy、局部ESLint、文档构建、canonical构建/来源门禁通过。最初Vitest文件名过滤误选了`.local`中的两份历史checkout测试并失败，收窄到当前仓4个文件后通过；未修改历史副本掩盖失败。

与实现分开的结构化复核覆盖了原数据根、同库互斥、部署配置唯一来源、启动开关组合、资源版本、旧reader拒绝与新版回退reader、旧outbox不重投；详见 [实现审查](evidence/phase12-implementation-review.json)。元仓及D4检查单独记在 [阶段12文档检查](evidence/phase12-meta-checks.json)。

回退必须正常退出并以当前兼容源码、`YIJIE_EXPERTS_ENABLED=false`重新canonical构建；保留SQL35/Host10，不恢复旧写入器或降级数据。加密备份留在上方私有目录供必要恢复，不自动覆盖现在的新记录。裸开发App不提供完整启动环境；日常仍使用本节canonical入口。

本次未改业务权限、未提交推送或公开发布；未执行破坏性故障测试或外观验收。既有无关worker全量格式检查限制保持，不作为全仓通过声明。当前日常接入范围没有未完成项。
