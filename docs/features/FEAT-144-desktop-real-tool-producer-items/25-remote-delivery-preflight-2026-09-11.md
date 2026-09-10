# FEAT-144 远端交付前核验

> 后续状态：已获授权并完成22个提交的普通推送、远端SHA核对，CI未触发。见[26远端结果](26-remote-delivery-2026-09-11.md)。本文保留本地验收/推送前时点的原结论，不将旧待办当作当前操作指令。

2026-09-11。用户要求先复核、取得本次推送授权，再按 Contracts → Host → Desktop → 元仓普通推送。当前本地 D4 已通过，尚未执行推送；本报告不把本地结果写成远端通过。历史验收及调用范围仍以[24](24-final-native-decline-and-delivery-2026-09-11.md)为准。

## 已核实的待推送范围

四仓均使用 `chore/retirement-baseline-20260905`，origin 为 `https://github.com/36Dge/<仓库>.git`；GitHub API 确认均为公开仓库。`git ls-remote` 实际读取远端 SHA，逐仓确认它是本地 HEAD 的祖先，允许普通快进。没有 fetch/merge/rebase、改远端、强推或创建 PR。

| 仓库 | 已观察远端完整提交 | 本地待推送目标 | 数量 |
|---|---|---|---|
| yijie-contracts | db7a607c1c091fc4f4243829d68d5b673eb7e2c3 | 811f38d6b104fa18477107e7ac91a85e19c445d1 | 2，均 FEAT-144 |
| yijie-agent-host | f4cf01bd6f7e9f37792ef743d44f0ce10527c10b | 0e47766f494977c94bfea0e89cfbdf45a7fafa2b | 5，均 FEAT-144 |
| yijie-desktop | 8bfa5ca284fddb86d7cdd2a406c5041c49367688 | 5964e2f7c31ea298f801df02086abbc8d6676b91 | 8：7 个 FEAT-144＋1 个首页动画祖先 |
| yijie | 6f12939aa85f8a9c1f55e89f1018c60501a2f494 | 原本地验收34948cdaa38a153f0e00268d78370bbac1da7b02之后的本报告提交 | 原6＋本报告1；获授权后另记录实际推送/CI结果 |

逐提交标题、完整 SHA、变更文件数量及范围内最终文件 SHA-256 见[机器核验](evidence/remote-preflight-2026-09-11.json)。推送前再次确认远端位置和工作区；若出现新增提交、分歧或并发改动，先重新审查，不擅自合并或推送额外内容。

## Desktop 祖先提交须明确纳入授权

`228a95a4929a53bbb6aafc76156161d642d72153`：`feat(ui): implement 2.2-second Kaijie homepage opening`。这是已有并发首页工作，包含11个界面、样式、文档及测试文件，先于最低兼容 reader `25b004fbd5a4dcf642a503d302c21a7d6e3b817f`。没有改写或拆分它。

审查确认范围为首页动画、文案、进入/聚焦时机与减少动态效果承接，没有 MCP、Runtime、权限或数据库语义修改。当前只执行两个安全定向测试文件，9项通过；既有首页报告记载的全量 ChatPage 三项基线失败与未执行的危险 fixture 仍保留，不宣称全仓绿色。前次 FEAT-144 canonical 本就包含该祖先提交，不需要为推送重建应用或新增调用。

普通推送当前分支无法跳过此祖先。用户本轮“仅FEAT-144”尚未包含其远端交付，必须取得包含该确切提交的范围授权；不通过重写历史/cherry-pick重新生成reader和验收SHA来隐去它。

## CI 来源修正与可执行边界

发现 Desktop workflow 仍固定旧 Contracts `6f632f155eacdaf93df0e0b00b5dab9e369c5442`、Host `f4cf01bd6f7e9f37792ef743d44f0ce10527c10b`，不匹配当前 FEAT-144 来源锁。沿用本需求必要本地修复提交授权，已在 `5964e2f7c31ea298f801df02086abbc8d6676b91` 仅更新这两处 checkout ref。

`contract-impact = none`：仅CI取用已存在的固定提交，不改变产品代码、wire、持久格式、权限或Runtime。结构化YAML比较确认除了两个ref之外，触发器、目录、权限、Skills pin和全部检查步骤逐项相同；原生/MCP/FEAT-152来源及FEAT-137退役检查通过。没有机械更新产品消费者锁或重新执行付费D4；实际产品构建来源仍为7abf89e8，CI补充提交单独记录。

四仓workflow只对main/staging/develop的push和PR触发；本分支push不匹配，未定义workflow_dispatch。当前四个目标SHA的Actions查询均为0条运行。推送后仍须重新查询，不能预写PASS。现有全量产品CI包含历史故障/攻击fixture等本任务禁止执行的测试，未人工触发；保持检查原样，不建PR或改触发器绕过这一边界。安全定向检查已有本地证据，不能冒充远端CI。

## 完整性、秘密与调用

在追加本次远端核验文档之前，核对22项元仓验收文件SHA、13项Desktop提交前SHA、12项E/F证据适用性SHA及现有模型计数器，均未变化；随后仅在元仓追加本报告/证据、交付日志和artifact引用，不改写旧实测结论。对四仓全部待推送提交版本中的310个不同变更blob做通用秘密模式检查。唯一命中为已注明synthetic/localhost、real_credentials_used=false的公开合成Bearer；已定点审查，不包含真实Sorftime密钥，没有通过全局忽略规则放行。该模式检查不宣称证明所有类型的秘密均不存在，也没有读取或复制私人数据库/凭据。

累计文本9/13、元数据14/20、业务2次逻辑调用保守扣4/10、图片0；本次核验新增均为0。AC-004仍OWNER_EXCLUDED / NOT RUN；旧投递不确定、Tool正文脱敏、缺失原生字段/冷历史、Command final-only与旧附件/清理/映射限制保留。

## 下一操作和准确状态

- 本地验收：PASS，范围和来源见24。
- 本地提交：三产品仓已提交；本报告及机器证据单独本地提交，保留并发祖先。
- 推送：PENDING AUTHORIZATION，包含首页祖先及后续实际交付记录的范围须一次性明确。
- CI：当前查询0条，NOT RUN；推送后再按精确SHA核对。
- 外部操作：未push、未merge、未tag、未部署；不手工运行不适用的CI。

授权后先再次只读核对四仓和远端，再以明确完整目标SHA逐仓普通push并立即核对远端；最后补充实际结果记录并在同一授权范围内本地提交、推送元仓。任一来源、范围、快进条件或安全检查不满足时停止对应步骤并说明，不能以提前改变状态字段代替操作成功。

实际命令结果见[检查输出](evidence/remote-preflight-checks-2026-09-11.json)。本报告的Git提交确定自身字节与身份，不虚填自身SHA。
