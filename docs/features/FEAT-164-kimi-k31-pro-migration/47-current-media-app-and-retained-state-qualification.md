# FEAT-164 S4T：同源专家/媒体 App 离线验收

2026-10-26，Owner恢复执行。S4S审计/来源绑定已本地提交`e137722`；本轮继续推进整项目标：所有活动Kimi调用面使用`kimi-k3.1-pro`，保留旧历史与原操作/授权事实，同时保持MiniMax可用。整项仍为IN_PROGRESS；本报告仅确认下述实际覆盖子集，不提升G4/G5/G6或十项AC整体状态。

## 复审和来源

contract-impact=none：本轮无产品源码、Runtime核心/补丁、wire、schema或迁移逻辑修改。使用已固定源码，在新输出目录通过canonical `--packaged --feat164-qualification --kimi-k31-pro --prepare-only`构建media组合，再用`--reopen`校验同源并启动。此前ordinary构建与所有旧制品保留。

| 层 | 当前来源 |
|---|---|
| Desktop | `9f5814fec6cd071d39f0c12f8f48097ce661cb6a` |
| Contracts | `ca06d0999c9a08afe80ab3f34a537d492b830ac7`；r5权威投影仍`5b5dad9` |
| Host | `8cd6bccbdc1ac3906aea53d95441299f7cfefcce`；产品binary保持`1d880cb…` |
| Runtime | `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a`，r5 `283d12e…` |
| Connectors / Skills | `cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9` / `595c927ae101d3d31c234f60565041eee0864680` |
| 新App | `42a23cfbc11cc047b005b8d80dafa2aff243fcc469dd1510d04d88196e85f6a9`；119 bundle文件逐一核对 |

新工作树`feat164-s4t-media-qualification-20261026`的六来源最终均干净。构建回执SHA`6a38d6d428816a3199294299c344e25ec7ec8c0714844e5c7f2f1de4928f556d`，绑定worker、adapter、专家资源及各输入。构建/两次启动均经canonical来源检查，没有覆盖旧App或改写其回执。

## 实际 App 结果

固定身份`com.yijie.ai.feat164-qualification-v1`，沿已合格独立数据根，无日常迁移。正常选择新测试目录、专家与图片，不改库造场景，不给工具额外授权。合成服务仅监听127.0.0.1:18083，使用明确dummy凭据，无外部转发代码，8次硬上限；未接受旧K3 profile。

| 场景 | 实际结果 |
|---|---|
| 活动目录 | 新会话默认Kimi K3.1 Pro；可选MiniMax；旧K3不在可选列表 |
| 专家/媒体 | 正常选择“数据报告可视化专家”，实际准备本地固定资源、绑定专家；原生发布HTML/SVG，完成后两成果ready |
| 文件与预览 | 两成果SHA逐一等于安全静态源文件；HTML独立预览及SVG图片预览可见，未加载外部资源；本轮未做另存为导出验收 |
| 图片输入 | 正常添加179B PNG，一次Kimi/max出站确有`input_image=1`，完成并保存 |
| MiniMax共存 | 显式选择MiniMax-M3，实际本机请求high，完成并保存 |
| 同构建重开 | 专家、两个成果、PNG历史、MiniMax历史和模型身份仍可读；总请求保持5，没有补发 |
| 正常退出 | 两次⌘Q均exit0，App/Host/Runtime/worker/adapter退出、相关端口和数据句柄释放；四Runtime库自然WAL0，完整副本只读integrity均ok |

3个用户任务，5次本机模型HTTP：专家发布HTML、发布SVG、最终答复各1次，PNG1次，MiniMax1次。全部完成，拒绝0，真实HTTP新增0。合成响应不证明供应商模型、搜索、内容质量或真实多模态能力。

原71张SQL表中的每一条既有行hash均保留，旧模型选择、Runtime绑定、计划及grant事实完全保留。重开前后只有正常停止代际表新增1行，其余70表相同；3个新turn均completed，两个成果字节一致。所有数据库和WAL/SHM副本保留，未checkpoint、删/截断WAL或强杀。

## 审计发现与保护

首次进程预检把Codex桌面自己的app-server误纳入目标，立即停在复制/启动前；限定为CrossBSD项目路径后只执行一次修正检查，未碰该进程。原始失败及修正另记。UI文件夹粘贴未生效、一次过期AX索引均在实际提交前通过新观察修正，没有误选目录或新增模型重试。

最终严格文件比较发现唯一资格资源日志变化：`com.yijie.ai.feat164-qualification-v1/skills/installed/.yijie-state/operations.json`因正常选择专家追加1条安装完成记录。它位于同一独立App身份，但在candidate后缀目录之外；原7条记录重建出的完整旧字节与恢复时SHA完全一致。该变化如实作为正常安装追加记录，不宣称全部文件逐字不变，也没有回写旧日志。该日志前后证据另存，其余42097份保护文件逐字保持；新专家资源仅增加于资格身份。

494份原dirty逐字核对；混合memory恢复原暂停块后匹配恢复基线，其余FEAT-164自有治理/账本按独立范围保留。S4S旧保护审计仍成立。日常库、原SQL41候选、原App、旧两账本和14.188544元unknown预占均未改。真实历史仍5/5、累计上限30元、保守14.679001元，不能因本机验收补额。

## 与整项完成的差距及下一顺序

1. 本轮关闭最终来源下的专家资源绑定、媒体交付/预览、图片传递、MiniMax共存与正常重开缺口。ordinary和media的限定App证据现已绑定当前源；不能推导market-only/experts-only全部App组合或完整TCONF04通过。
2. 下一步优先复审现有S4/S4b/S4e安全用例，为标题/草案辅助、子代理终态/历史重放、自动压缩形成**保留全部Runtime home的验证入口**。现有成功清理会RemoveAll临时home，不在本轮直接运行；应只调整测试生命周期，在独立测试来源记录与原测试语义等价，保留正常关闭，禁止强杀/攻击fixture/WAL清理。此处未修改任何测试或Runtime核心。若发现必须改Runtime核心/补丁，先提出最小方案并确认。
3. 再逐条关闭04A/06中仍缺的时序和unknown/never-sent证据，区分领域、Host、App层。不能为制造未知态注入故障或清空旧记录；不可安全构造项如实记录原因和影响，不能伪判通过。
4. 当前三个final仍各为NOT RUN：core缺完整范围；visual本轮只有可达页面/浅色预览，没有fresh亮暗/1180x760完整轮；teardown本轮正常路径通过但完整矩阵未执行。依据最终适用范围补齐后才可提升；历史r4视觉/G2V不冒充r5。
5. r5供应商G2V、日常cutover及推送/发布仍无授权。本轮不以合成答复消除真实供应商资格差距，不开放日常迁移。未来日常切换须给出具体来源、完整备份、兼容reader和安全回退清单，再取对应批准。

已停止App、全部项目sidecar和本机fixture，无在途模型请求、无待答UI交接。后续从本报告和[当前矩阵](current-acceptance-matrix.md)续办，不重复已通过S2/S3任务或本轮三个任务。

证据：[S4T索引](evidence/s4t-audit-index.json)、[限定结论](evidence/s4t-media-verdict.json)。完整私有审计根为`feat164-s4t-audit-20261026`；DB、keys、完整安装副本不提交Git。治理检查结果见同目录`media-governance.json`，本地提交记录见`media-meta-commit.json`。
