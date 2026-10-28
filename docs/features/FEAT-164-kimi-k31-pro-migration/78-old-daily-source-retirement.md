# FEAT-164 第78号：旧 daily-source 精确清理完成

2026-10-28。Owner明确要求先审计、核验归档/bundle/Git引用/反向依赖，形成精确清单后清除旧`yijie/.local/daily-source/20261027-01`。该目录现已不存在，8个worktree注册均正常移除。原主目录generation`20261028-02`及全部产品来源、制品、D5绑定保持；本轮未启动App、未调用模型、未改Runtime或日常数据，不推送。

增量`contract-impact=none`：仅退役已不参与当前构建运行的本地checkout与缓存；不改变当前部署接口、产品wire、权限、SQL或模型行为。第76/77号的构建、运行及退出修复证据保留原时间；其中“旧daily-source保留回退”的表述仅适用于本次清理前。当前回退须从本报告的归档恢复并重新审定，不能调用已移除路径。

## 审计与恢复保护

清理前8个worktree均干净，真实Git数据库归属原仓；全部提交都有现存引用可达，没有独有未保护tip。五仓现有`primary-workspace-execution/20261028-01/bundles-final/`的bundle重新核验SHA、独立mirror恢复、完整fsck及全部refs一致，覆盖8个提交、原六独立tip及已有WIP保护分支。没有删除分支、移动原仓HEAD、改变远端或执行prune。

新增完整归档位于：

`yijie/.local/daily-source-retirement/20261028-01/daily-source-20261027-01.tar.zst`

- 压缩归档3,701,716,249字节；SHA-256：`7ed1fd6afe1ac8cb7495c7dd04d37c9583a51a9955cc1bce35e539711d10ddbf`。
- 覆盖75,547项，其中65,688个普通文件、1,246个链接，普通文件逻辑大小10,603,249,198字节；无排除，包含忽略文件、旧App、缓存、来源清单和Git指针原值，不解引用Runtime链接。
- 已独立解压并逐项核验内容、类型、mode、UID/GID、mtime、flags、ACL、xattr及链接目标；本轮差异0，原目录同时复核未变。
- 本轮恢复验证用的临时`archive-verification/`在再次逐项比对、确认无占用后正常移除。完整压缩归档、清单、恢复证据、五仓bundle及独立bare验证仓保留。
- 第76号703,062,946字节的原工作保护归档再次核验SHA及压缩流通过，原归档/bundle/旧账本和两份预占保持。

跨工作区检查15,601个符号链接，无外部链接指向待清理根；当前generation的3,163个构建元数据文件、动态库引用、绑定/receipt、安装入口及shell配置无旧来源依赖。12仓精确路径命中仅在元仓9份历史记录/当前文档中的历史块，没有活动产品脚本引用。源码和制品1410项复核通过，实际D5正常/暂停绑定均通过只读校验；旧目录无打开文件/工作目录占用。

## 已执行的精确清单

以下路径均相对于`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie/.local/daily-source/20261027-01`。

|顺序|目标|方式 / 提交|
|---|---|---|
|1|`yijie-desktop/.local/agent-host-pinned-1b7bfd1`|Host原仓普通worktree remove；`1b7bfd1ce4323e52035b2ba1e62842c2d332d9ed`|
|2|`yijie-desktop/.local/agent-host-pinned-96b1fa1`|Host原仓普通worktree remove；`96b1fa19783694aef583b614c492fd2b6b5c15cc`|
|3|`yijie-desktop/.local/skills-pinned-10c45be`|Skills原仓普通worktree remove；`10c45bec29603b002e861e1499d5b4e684251af5`|
|4|`yijie-desktop`|Desktop原仓普通worktree remove；`a211c2d04def6091352c7b3674a49355cdee18ed`|
|5|`yijie-agent-host`|Host原仓普通worktree remove；`7309101726dcecd48b2caa02401cfcdd6126f1fb`|
|6|`yijie-contracts`|Contracts原仓普通worktree remove；`d5792d6aad18352ce8d1c5d510d345004cab3bd6`|
|7|`yijie-connectors`|Connectors原仓普通worktree remove；`cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9`|
|8|`yijie-skills`|Skills原仓普通worktree remove；`595c927ae101d3d31c234f60565041eee0864680`|
|9|`.build-cache`|完整归档后，精确目录正常递归移除，失败即停，不跟随链接|
|10|`source-set.json`|核对原字节/元数据后仅unlink该文件|
|11|`yijie-codex`|仅unlink符号链接；原`CrossBSD/yijie-codex`不动|
|12|`.`|确认完全为空后rmdir容器；保留父级`daily-source/`|

Git操作均为所属原仓的`git worktree remove -- <精确路径>`，没有`--force`、reset、clean或prune。各步前重验对应子树和Git状态，执行记录逐项追加。既有12原仓、原主目录的固定Skills/Host来源、新日常产物、数据、保护引用及全部历史归档不在删除清单内。

## 清理后验证

目标目录和8个worktree注册均不存在；清理前后12原仓HEAD、分支、refs、远端、索引差异及原有工作文件完全一致。源码6仓保持干净，元仓原243项dirty不变（随后仅增加本报告等所属治理记录）。

清理后19项只读来源检查全部通过；重新核对1230项Desktop输入、55项worker输入、119个App文件和6项其他制品，全部匹配。generation、receipt和D5正常/暂停绑定未变，不依赖被清理目录。

Native、Host、Runtime三个活动日常Home的5,629个普通文件按清理前现场完整清单逐项比对保持；此数字是本轮三个活动Home的口径，不代替第76号17,401项完整后态备份口径。没有数据库API打开、迁移、手工checkpoint、WAL清空、强杀或模型请求。App仍未运行；本轮没有重跑第76/77号的App/UI验收或workflow探测。

当前运行方式保持：

```bash
cd /Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop
pnpm daily:open --generation 20261028-02
```

先正常退出后，同命令追加`--pause-kimi`可使用暂停入口。锁屏时跳过的新来源历史界面观察仍是SKIPPED；never-sent接受替代、完整App正向取消NOT RUN、搜索答案/外观专项OWNER_EXCLUDED保持。

## 清理后的回退

优先保留当前已验收primary来源及同源暂停入口。需要恢复旧源码时，先正常退出当前App并保护当前日常数据，核验上述完整归档和五仓bundle，将归档解压到新的审阅目录并比对清单。归档里的8个旧`.git`指针是历史证据，不得直接当有效注册使用。

恢复范围审定后，在原精确路径以所属原仓`git worktree add --detach <path> <head>`重建注册，外层Desktop先于三个嵌套worktree；再补回归档中的普通/忽略文件和链接，排除所有旧`.git`指针、保留Git新生成的注册。原Git库不可用时先从已验证bundle恢复独立Git库。随后核验旧来源、构建环境、制品、receipt、原Home兼容和新的明确启动资格；不得仅因历史D4/D5曾通过就自动启动。

恢复旧源码不恢复或覆盖日常数据库，不降schema、不重跑D3、不删除WAL、不增加模型调用。第76/77号现行primary入口及历史安全约束保持。

完整冻结清单、75,547项私有文件清单、归档/bundle校验与逐项执行证据：`yijie/.local/daily-source-retirement/20261028-01/`。可提交的摘要见[机器证据](evidence/old-daily-source-retirement.json)。

治理检查：元仓lint、57项测试、claims及strict/G6全部通过；只读来源检查19/19通过。独立复审确认无强制删除、无遗留注册，原243项meta改动与其它11原仓状态均保持；本次仅固化所属治理记录，不推送。
