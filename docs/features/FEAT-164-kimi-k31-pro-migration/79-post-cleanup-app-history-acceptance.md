# FEAT-164 第79号：清理后原主目录 App 启动、历史与正常退出验收

2026-10-28。Owner要求从原`yijie-desktop`主工作目录完成一次清理后的零模型调用启动、历史检查与正常退出，并补齐证据和后态审计。**本轮已完成：同一generation `20261028-02`一次canonical启动、8会话/11轮历史实际界面检查、定时任务历史保护、App自身⌘Q正常退出及完整后态审计通过。新增模型HTTP为0。** 第76/78号因锁屏跳过的这项新来源历史界面检查由本轮实际证据补齐，原跳过记录不改写。

增量`contract-impact=none`：只执行已批准的本机验收和同栈依赖恢复，不改产品、Runtime核心/补丁、契约、权限、模型配置、来源锁或构建制品。旧daily-source仍不存在；完整归档、bundle、原仓、工作区改动、账本和两份预占保持。

## 前置检查与依赖恢复

重新验证原六仓干净来源、1,410项输入/制品和D5绑定；同一正常实例锁下，新完整冷备份包含17,401文件/522,889,712字节，sealed与inspection均逐项匹配，且与第76号最终完整快照一致。数据库检查仅使用inspection：Native SQL41/71表、Host11、8组Native→Host→Runtime/rollout映射、完整性及全模型无待派发检查通过。6个历史已消费grant保留，不清零。

最初workflow就绪检查因Docker未运行失败，App尚未进入canonical启动。沿用Owner此前已批准的第65号同一服务栈恢复范围，正常打开原`/Users/jack/Applications/Docker.app`后核验8个既有容器、镜像、挂载、来源和数据身份。全部停止，其中两个容器保存退出码137，OOMKilled均为false；没有推定其具体退出原因，也没有把原状态改为正常。

新恢复ID为`6ce625bb-9650-443d-8de6-91a9a17b756b`。现有canonical recover先完成四份停止态数据卷copy-out/hash：

|数据卷对应服务|清单项数|字节|
|---|---:|---:|
|workflow-postgres|1,324|65,799,591|
|coze-workflow-mysql|314|228,238,224|
|coze-workflow-redis|5|53,387|
|coze-workflow-minio|34|18,855|

随后正常启动原容器、复核API/Coze业务事实、正常停止，再执行原canonical up。此过程包含既有幂等迁移和正常epoch/凭据轮换；旧private配置/凭据另作完整副本，原四个volume保持，没有新增服务、拉镜像、删除volume或强杀。恢复和up共追加两条预期principal审计，其余业务事实保持。最终六个primary健康，真实鉴权ready通过；App退出后再次检查仍ready，workflow保持运行。

## 一次当前来源启动与实际 UI 历史

本轮唯一canonical App验收启动：

```bash
cd /Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop
pnpm daily:open --generation 20261028-02 --pause-kimi
```

App/Host/worker实际进程链均来自原主目录新产物，Runtime来自原仓r5。Host ready200；本机只读catalog确认Kimi K3.1 Pro/max暂停、MiniMax目录可用、旧K3不在活动目录。未发送聊天、重试任务、切换模型、启用计划或执行业务工具；暂停参数只属于本次进程，不修改正常D5入口的默认启用状态。

通过当前App的真实UI逐一打开8个会话；可访问性快照中的会话ID摘要与Native的8个会话集合完全一致：

- 5个已完成任务的原回答正常显示；项目任务的2轮完成、1轮中断以及命令记录可读，并展开一个历史命令卡查看完成状态/安全输出。
- 附件任务保留`orders.csv`、`tax-rates.csv`两份附件、原专家/技能信息、两轮未完成历史及原历史差异提示；另一失败任务也保留原失败事实。没有把失败变成成功，没有重建或重发历史。
- 共11轮原历史保持。所有8个旧K3会话均显示“已退役”，发送按钮禁用。
- 定时任务当前列表为空；执行记录中的旧记录仍可读。打开已删除计划的详情，显示历史Kimi K3/max、已结束、对应对话已删除；重新执行与查看已删除对话按钮禁用。没有新建、保存、启用或重跑计划。

这次只验证历史可读、原状态及退役/授权保护，不重新验收历史答案内容正确性或已移除的外观专项。

## 正常退出及后态

通过App标准⌘Q菜单路径进入现有ExitOwner；UI工具观察到App已退出，canonical启动进程退出码0，日志包含`normal app cleanup complete`。未调用强杀、未手工checkpoint、未删除/截断WAL。

新完整后态副本17,401文件/523,139,568字节，sealed逐项复核通过。71张Native表中仅`chat_scheduled_stopped_generations`由123增至124，其余表保持；8会话、11轮、6个旧计划、7个旧run、25个grant及全部原授权保留。Host全部持久值一致；Runtime业务行和rollout一致，原日志完整保留并仅追加608行。

文件差异限定为正常数据库文件与相应目录元数据，Native/Provider密钥、其他原文件和历史迁移备份保持。活动数据库WAL/SHM为0，同一实例锁可获取，无App/Host/worker/Runtime残留进程或数据句柄。全模型待派发工作仍0。新增模型HTTP0、provider metadata HTTP0、业务工具调用0；零调用结论同时绑定无UI发送、前后派发/turn/operation不变及当前启动/退出记录。

本轮产品版本及制品不变：Desktop`24a231f96f08ed077e53f9bd73a2aac93ee6cba8`，receipt `28141579143c6da10ac47f11a164e7394cec83ae3559aa9dd50db5057c4cd915`，D5 binding `169d6713703abaaf35ad84fdcdbdc0778159fec0a18cf50f1bd4a339ad80a87c`。普通入口仍为上述命令去掉`--pause-kimi`，当前App已停止。

## 观测问题、保留范围与证据

首次UI选择超时后未观察到App进程；后续完整原数据快照与前次最终快照完全一致，不能将该超时当作成功启动。Docker UI读取也曾超时，但随后实际原Docker进程/socket已就绪。App bundle ID因多个历史App重名而产生歧义，改用已核验的完整路径后成功绑定当前窗口。第一次进程观察过早，canonical仍在预检；同一启动随后通过，未再次启动。后态检查第一次漏传标签参数，在创建副本/打开数据库前停止；修正调用参数后复核同一次退出通过。以上原工具结果和RCA单列，未修改产品或放宽数据断言。

原243项meta未提交改动、其它11原仓状态、七份账本和两份预占保持；本轮仅本地固化所属治理记录、不推送。完整App正向never-sent取消仍NOT RUN，Owner接受的安全分层替代不变；搜索答案正确性、亮暗/键盘/最小窗口专项仍OWNER_EXCLUDED。没有扩展为公开、云端、多人或签名发布。

私有证据目录：`yijie/.local/post-cleanup-acceptance/20261028-01/`，包括完整前后副本、实际UI文本/截图、进程/目录/退出、workflow恢复及逐项审计。真实数据、凭据和完整UI文本不进入Git。可提交摘要见[机器证据](evidence/post-cleanup-app-acceptance.json)，验收标记见[验证记录](08-verification-report.md#E164-POSTCLEANUP-HISTORY)。

最终治理检查：元仓lint、57项测试、claims及strict/G6全部通过。分离复审确认原工作区差异隔离、来源/制品不变、全部原业务行与授权保持，真实UI及正常退出证据有效；本轮只本地提交所属治理记录，不推送。
