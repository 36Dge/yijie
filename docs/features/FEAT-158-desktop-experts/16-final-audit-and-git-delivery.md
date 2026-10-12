# FEAT-158 最终审计与 Git 交付

2026-10-13。本轮由用户明确要求认真审计后提交并推送，只处理 FEAT-158，不扩大验收范围、外观继续跳过。确认六个相关远端均为公开仓库后，用户明确回复“包含知识正文与脱敏评测记录，允许公开推送”。该授权只覆盖本次 Git 内容上传，不表示签名发行、生产部署、第三方许可证核验或政策质量背书。

## 审计范围与发现

以 [phase13 Git 基线](evidence/phase13-git-baseline.json) 为界核对每个路径和 diff。提交前 Desktop 913 项、worker 43 项、Host 351 项构建输入分别与 phase12 已验收来源一致，见 [源码比对](evidence/phase13-precommit-source-comparison.json)。复核生成契约安全投影、Native scope 与冻结 outbox、Host 同 Thread 角色组合、原操作恢复、资源引用保护、普通/专家分流、关闭专家后的兼容 reader、SQL34/35 增量及日常身份/单实例锁。快捷问题仍保留目标/授权时效检查及草稿确认；Shopify 适配仅针对已观察的固定 URL 完成通知 null ACK，业务 one-shot 审批与其他服务认证未放宽。

发现并修正的明确缺口：

1. Git 提交会改变来源 HEAD。使用原 canonical 打包器和同步/冻结脚本更新 Skills 来源、Host 编译目录摘要、Desktop 资源与专家开/关构建摘要。Connectors 提交也要求原 catalog 同步脚本更新 base_commit；首次 freeze 正确拒绝旧引用，随后同源同步通过，catalog 正文无变化。
2. Native 的 `validate_expert_manifest` 写死 `working-tree`，与打包器/同步器已经支持的 `git-commit` 不一致。提交包正常启动后旧专家会话仍可读，但出现资源不可用；新增只读实际 canonical 包测试先复现 `Invalid`，再最小修复为接受两种源类型且继续逐项等于编译 pin。保留 manifest/authority/来源树/完整 commit、渠道、归档和内容检查，无数据迁移。此增量 `contract-impact=semantic`；整项需求仍为 breaking。详见 [前后根因证据](evidence/phase13-compatibility-finding.json)。
3. Contracts 概述中的旧数量修正为 10 个 safe commands、11 个 private methods；各仓加入当前来源/交付说明，保留历史阶段结果。

## 来源和数据兼容

[提交来源核对](evidence/phase13-source-and-publication-audit.json) 从 Contracts 完整 Git 对象核对 30 项 source/generated 摘要，并从 Host 完整提交核对两份 Desktop 构建 pin 的各 351 项输入。源锁的 base_commit 保留真实 pre-change 基线，不伪造自引用 SHA；consumer 文档记录实际完整 Contracts 提交。

[资源重建比较](evidence/phase13-committed-source-repin.json) 证明 39 个归档、所有 skill/expert metadata 和资源树字节保持；知识仍为 0.1.3 / bundle 0.4.3。只改变 manifest 来源身份与相应审核摘要。安装收据、ROLE、knowledge manifest、原会话 ExpertRef 无需替换。本轮没有删除或改写用户数据库、会话文件或既有安装；正常启动继续复用原 `com.yijie.ai` 与 daily 根。phase12 已证明原 667 条 SQL 记录、8 条 Host 会话及6份 Runtime 历史保留，原证据不改。

## 必要验证与边界

- Contracts 同源生成校验、12 项普通契约测试通过；Skills 同源同步及5项内容结构/确定性包测试通过。没有新增内容质量评分。
- Host 使用提交后实际包运行5项资源生命周期、引用保护及兼容 reader 测试通过；同命令中的 app 包无匹配测试，不计入5项。
- Desktop 启动/profile/receipt 配置4文件52项通过、1项可选实源测试跳过；实际 canonical source gate 单独执行通过。
- 新增 Native 实际包回归先失败，修复后1项通过；格式初检指出新增断言排版，按 rustfmt 修正，最终 fmt 与 Clippy 结果单列。
- 历史完整 D4 和日常最小模型 smoke 继续引用 [14](14-final-engineering-acceptance.md)、[15](15-daily-client-integration.md)。本轮无真实模型、Shopify 元数据或平台业务调用；累计模型消息仍29。
- 外观 **SKIPPED**；AC-007 已移除，历史 FAIL/NOT RUN 不变；不运行用户禁止的强杀、故障注入、恶意资源、权限破坏或可执行文件伪装测试。未运行全库/全平台新验收，不宣称绝对无 bug、生产就绪或模型质量通过。

## 最终构建与远端交付

最终日常构建 **PASS**：由已提交 Desktop `d89b487842c5af4768beb1b00e6b04bb739bdb0e` 的 canonical `--packaged` 入口生成；App `4904e480c25ea5a82a6a116bc3ef54d38c2dcc3311054019bbf1da61d49bd440`，Host `5b42149c6e5230ad828fdd94e81d06cb7e682bc3002060b11e319fc676c5c603`，worker `0406274199b635b96649394ff636bc8d68b8465b98660f949ec476503a906710`（worker 与此前相同）。回执 SHA-256 `e068d9dfef8c89723d095acc85ae40d0cad1af9f4e16962c5bad7635fa1f310f`；913 项 Desktop 和43 项 worker 输入及全部制品摘要核对通过，详见 [最终启动](evidence/phase13-final-startup.json)、[构建回执](evidence/phase13-final-build-receipt.json)。

原专家会话、0.1.3 绑定、原回答和 Kimi 模型均可读取；目录显示“资源已准备／已选用”，资源不可用提示消失。未点击安装、移除或发送。phase12 原 Runtime rollout SHA-256 逐字节不变，因此本轮未新增该会话模型 turn。当前 App 保持运行在原专家会话，输入为空。旧 pre-fix 构建回执保留，不能当成通过。

产品仓推送结果已逐一读取远端 refs 验证，见 [推送回执](evidence/phase13-product-pushes.json)：

| 仓库 | 完整提交 | 原分支 | 结果 |
|---|---|---|---|
| yijie-contracts | `e35ae9a0711014e4774a1347413e9a343ce7ab2c` | `chore/retirement-baseline-20260905` | 已推送，远端 SHA 一致 |
| yijie-skills | `d7a850c9d5c5f8e52b8ab8f631800f671acc60dc` | `develop` | 已推送，远端 SHA 一致 |
| yijie-agent-host | `9acae49ee2bf1fb33ae1da8ef02fd0bd07538d63` | `chore/retirement-baseline-20260905` | 已推送，远端 SHA 一致 |
| yijie-connectors | `23c31e8f3cd467916956e1bbdef428a334de0ca3` | `develop` | 已推送，远端 SHA 一致 |
| yijie-desktop | `d89b487842c5af4768beb1b00e6b04bb739bdb0e` | `chore/retirement-baseline-20260905` | 已推送，远端 SHA 一致 |

Desktop 包含主功能提交 `c0b4e7b8164bdd228acf3cdafafc5d656aa010db` 和明确根因修复提交；其余每仓1项功能提交，没有混入原分支以外的未推送历史。元仓本交付记录随本次 FEAT-158 独立提交，具体 SHA 由 Git 本身定位，避免文档自引用；最终回答报告其推送后 SHA。没有创建 tag、PR、merge 或 release。

136 份历史验收文件摘要均未改变，见 [历史证据检查](evidence/phase13-historical-evidence-check.json)。最终修复没有复跑整套真实验收，不能把阶段11/12旧模型证据说成本轮模型结果。

仅显式暂存审计过的路径。Runtime 仓保持原提交且无改动；Connectors `.local` 的3份原始诊断文件保留本机。原始附件不复制进 Git；知识正文为已审 derivative，评测仅脱敏结果/合成输入/公开回答/状态摘要，不包含隐藏推理、凭据、数据库、个人会话原文或本机缓存。源码推送不改变服务 exposure=local，也不自动创建 release/tag 或部署。

元仓全暂存 `git diff --check` 返回2：仅历史 `evidence/phase5-final-contract-checks.json:60` 的末尾多余空行。该文件属于已冻结136份证据，不为消除格式提示改写其字节；保留此非代码告警，不能标作全暂存检查通过。排除这一份历史证据后，其余全部暂存路径检查通过。严格 D4 文档、claims 审计与元仓 lint 均通过，详见 [最终检查](evidence/phase13-final-checks.json)。
