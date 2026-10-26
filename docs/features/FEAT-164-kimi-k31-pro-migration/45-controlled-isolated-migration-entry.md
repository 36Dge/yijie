# FEAT-164 S4R：旧隔离库受控迁移入口

2026-10-26，Asia/Shanghai。Owner授权复审44号最小方案后实施安全离线验证，明确不开放日常库、不新增真实模型HTTP；Runtime核心/补丁须事先确认。本轮没有修改Runtime或补丁。整项继续IN_PROGRESS。

## 实施前复审

44号证明现有迁移/退役函数可处理自然旧数据，但正常candidate open仍拒绝SQL<38。直接删除这项白名单，会把受控迁移扩大成任意启动时自动迁移；把测试expand放进worker，也会混淆迁移与执行资格。两者均不采用。

选定同一canonical候选可执行文件的显式一次性维护模式：持有原App单实例锁，固定隔离身份和数据根，检查正常静止状态，保留完整加密快照，调用已有migration与正常Repository open，然后退出。它在auth、DatabaseWorker、Host、Runtime、WebView之前返回。没有新Tauri command/capability、共享wire、依赖、Runtime target或密钥来源。

增量`contract-impact=semantic`，权威源为Desktop私有部署/存储入口及其既有migration；Contracts公共源字段为N/A，原因是没有改变跨仓wire或schema定义。Owner/consumer是当前已授权本地候选的段成威；整项FEAT-164 breaking保持。输入/输出、失败和回退边界在Desktop的`docs/feat164-isolated-model-migration.md`与SECURITY.md同步。原框架和数据格式不变，Runtime11fd/r5、Contracts5b5dad、Host产品894671b保持。

最小准入在实现复审中进一步收窄为已经由当前正常API产生并验证的SQL29/37；35/36及其它旧版本继续拒绝，不能从迁移函数存在推定全部入口已获资格。

## 实现与安全边界

标准入口：

```sh
bash scripts/run-local-demo-fast.sh --packaged --kimi-k31-pro --migrate-isolated-k3
```

已有同源构建可附加`--reopen`，仍必须通过原来源/回执校验。与`--prepare-only`互斥。launcher以无模型凭据的最小环境执行同一bundle内binary的单一维护参数；普通启动保持原行为。实际consumer/runtime/build来源检查全部保留。

- 仅macOS、编译期candidate、固定`com.yijie.ai.feat164-kimi-k31-r1`、精确local/demo_fast/model/candidate及daily=false通过。没有产品数据路径参数或测试目录环境入口。
- 数据路径固定为该App正常Application Support目录下的`demo-fast-model-candidate-v1`。要求canonical私有目录、owner-only普通单链接文件；文件读取还以O_NOFOLLOW和fstat身份核对保护。普通日常identity拒绝。
- 复用同一App单实例锁，并用系统lsof确认候选目录没有打开句柄；不停止其它进程。正常并发持有锁时直接拒绝。
- 写原库前，完整保留DB/WAL/SHM及原SQLCipher/HMAC key字节与hash，新增目录700、文件600。另建第二份DB/WAL/SHM副本只读检查，防止SQLite更新SHM影响原始快照。两份现存key均先验证，不生成新key，不输出key/正文。
- 校验旧ledger、integrity、FK和固定scope；pending/inflight出站、非ready模型选择、活动/不确定turn、预约、已占用grant、无支持的原生终态历史均拒绝。拒绝不清理、不退款、不补发。
- 原文件再次hash及句柄检查后，调用既有migration到38，再使用真实candidate Repository open完成41和计划退役；不创建worker。正常关闭连接，不手工checkpoint、不删截WAL。
- 快照/闭集结果保留，失败不自动回滚、不启动旧writer。中间状态需用兼容candidate reader审计，既有迁移/退役可重入；不把重入视为授权续额或执行许可。

现有普通open的SQL<38白名单完整保留。这个入口只增加明确的维护路径，不把所有启动都变成迁移入口。

## 安全离线验证

自然旧数据producer使用默认非candidate构建的真实计划API，分别通过普通配置生成SQL29、正常连接器配置生成SQL37；各有无占用review与有旧run/occupied=1的held样本。没有直接改model、授权、user_version或历史SQL。旧producer输出保留，受控测试仅复制这些完整正常fixture至自己的固定候选目录形状，随后调用产品迁移函数。

两版本最终矩阵均通过：相对路径/日常identity拒绝；正常单实例争用拒绝；held库拒绝且原DB/key字节不变；review库29/37→41成功；完整备份逐字相等；旧事实不改；重复执行不重复退役；真实正常Repository重开通过。另一次非candidate进程验证关闭功能时拒绝。没有强杀、错误权限、危险fixture或攻击注入。

独立只读完整副本审计：两版本integrity均ok；原29/37条migration ledger逐行保持并扩展至41；3条模型身份行完全相同；9类原grant/run/recovery/reservation/request/model snapshot/binding/outbox/task事实表完全相同；各有2条退役收据。没有把授权迁移与原grant重写混为一谈。

Rust fmt、产品lib/bins严格Clippy、上述定向测试、Shell语法、Desktop文档构建通过。全量含测试Clippy未复跑，44号既有`native_conversation_storage.rs`排布错误保留；全仓测试、完整Runtime make test与全平台资格未宣称通过。

## 标准构建与实际维护入口

最终来源`bc3b097edf56779a1cfd273063df6d8f4a9c6019`的19项来源检查通过，ordinary canonical App构建及42个bundle文件/回执核验通过。binary SHA为`b8c33a21ed08bfb51c699482c1966af7a3a082ea9e2a356892d652905cf5c321`。本轮只运行维护模式，没有打开普通UI。

实际compiled App对禁用candidate、daily=true均exit1/chat_invalid_configuration，在数据库访问前拒绝。随后canonical `--migrate-isolated-k3 --reopen`在两个模型Key文件均不存在时通过同构建核验，进入维护入口并正常exit1/chat_conversation_conflict。

这个拒绝符合现有数据事实：实际隔离库已经SQL41，pending/inflight outbox=0、非ready模型选择=1、reservation=0、occupied grant=2、不确定/活动turn=0。最早拒绝点是模型选择；占用grant还会独立阻止迁移。**现有库没有被升级或清理，也无需重复结构迁移。** 5,522个原文件逐字保持，仅新增私有备份UUID `01a17722-6db5-7173-9409-6d053287c982`下8个快照/检查/停止记录。原始快照hash全部吻合。原选择、计划占用和真实费用预占是不同事实，分别保留。

原始非绿色记录不改写：首次generation缺新Contracts工作树的既有node_modules，补同版本已安装依赖后通过；首次ordinary prepare-only被原MiniMax文件预检阻止，未开始build。复审发现新增维护模式也经过旧Key预检，随后只给维护模式豁免该检查，普通启动不变；build-only使用新合成Key及loopback地址，实际维护另以缺失模型Key验证。后置归因脚本最初假定pending outbox而断言失败；只读实际计数证伪后仅更正摘要，没有重跑迁移或改断言清数据。

本轮新增真实模型HTTP **0**、loopback模型HTTP **0**。没有启动模型服务、Host/Runtime/计划worker；无日常迁移、push、tag、release或App用户界面验收。

## 本地提交与剩余项

Desktop隔离实现提交`8dcf7a678f02c9bfa74dbf8cea4dff4e7bd2ae00`及最小Key预检修正`bc3b097edf56779a1cfd273063df6d8f4a9c6019`，保留在`feat164-s4r-qualification-20261026/yijie-desktop`。主工作区三处源码已有其它需求改动，**没有向主工作区快进或应用补丁**；其HEAD仍fd0c575，所有原dirty保持。后续继续必须使用这个隔离commit/工作树，不能误称主工作区已包含新入口。

元仓记录由包含本报告的Git提交定位。Runtime核心、补丁、原r5制品、Host/Contracts源码和旧S4P App保持。旧账本、5/5已耗尽次数、30元cap、14.679001元保守累计及14.188544元unknown预占不变。

本轮“受控迁移入口及安全离线资格”已完成；S2/S3完整App纵向、S4/TCONF04和全部final仍未完成。下一步先按原请求只读核对那1条模型选择和2份计划占用的恢复事实；SQL41现有库不需要再次迁移，不为通过检查而清空它们。旧K3自然App场景需要保留现有候选的独立测试数据安排，再完成同源UI的显式恢复/取消/重新审阅授权。任何日常迁移或新增Runtime核心/补丁范围仍须按原授权边界单独审查。

证据：s4r-pre-implementation-review、implementation-review、migration-matrix、sql-preservation-audit、generation-final-result、build-result、compiled-entry-negative、canonical-entry-result、current-refusal-audit与final-build-binding。原始成功/失败日志、可复现源和构建回执的路径/hash见s4r-audit-index；完整DB/key快照不提交。

最终治理claims/strict/manifest/Contract First规则、元仓53项测试和7份Shell语法通过。497份原dirty、8128份受保护文件及旧S4P 119个bundle文件逐一保持；现有候选无打开句柄、18083/18086无监听、无活动受管服务。此结论包含“现有库被拒绝”的真实边界，不是整项完成或日常开放许可。
