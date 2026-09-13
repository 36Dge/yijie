# FEAT-153 Git 交付

2026-09-13。FEAT-153 的 `demo_fast + local` 实现与统一真实 D4 已完成，资格编号 `ea50e666-898c-4107-9568-10e3e3d63416`，详见[17](17-d4-final-qualification.md)。用户在此结论之后明确授权 `git add`、`git commit -m` 和推送。本页记录 Git 交付，既有真实验收记录按发生时间保留，不转换为生产、合并或 CI 资格。

## 提交与推送

| 仓库 | 完整提交 | 分支 | 远端结果 |
| --- | --- | --- | --- |
| yijie-contracts | `32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4` | chore/retirement-baseline-20260905 | origin 已推送，远端 SHA 相等 |
| yijie-api | `5e97b18cca1492ac29d4a506411d1e7fc70c9628` | feat/feat-126-foundation-closure | origin 已推送，远端 SHA 相等 |
| yijie-coze | `05a81edab974b3041fa3bae27124d7994ca875ff` | main | 私有origin已推送，远端SHA相等；实现提交为d6b79869 |
| yijie-infra | `2b238d93cecd446dfd9b22fef681e2bd5ed70f02` | feat/feat-126-s10e | origin 已推送，远端 SHA 相等 |
| yijie-desktop | `db3938a24fad2f24c2b72ecc8556b541dc0b1d38` | chore/retirement-baseline-20260905 | origin 已推送，远端 SHA 相等 |
| yijie | 本文所属 FEAT-153 提交 | chore/retirement-baseline-20260905 | 最后提交需求、治理与证据；最终 SHA 由 Git 记录及执行回执确认 |

已使用现有分支逐仓普通推送，无强制推送、rebase、tag、merge 或生产部署。元仓原有本地提交 `d59e1725f988df6f1f3fe1abbf0b4546ab419819` 是 FEAT-144 已有交付记录，未重写，作为当前分支祖先保留。

用户最初提供 `https://github.com/36Dge/yijie` 作为 Coze 目的地，但它是已有元仓；未把 Coze 独立历史推入元仓。用户随后明确授权新建私有`36Dge/yijie-coze`，已创建并验证private=true，补齐上游历史并推送main。本机原origin改名upstream，origin指向易界仓；源lock保持原始上游SHA。来源检查同时支持原工作区的六份既有删除和fresh clone中保留的六份原始文档，不删除或恢复文件。未向`coze-dev/coze-studio`推送。

逐仓远端核对见[提交回执](evidence/git-delivery-20260913/implementation-commits.json)。

## 来源固定与交付验证

整体需求的契约影响仍为 semantic。本次 Git 来源工具修正为 `contract-impact=none`：生成检查重放原 `base_commit`，避免提交自身引起来源锁漂移；消费者同步新增完整 `source_commit` 固定，并在写入前对该提交中的全部源、派生物与来源锁逐字节核对。原 Chat/public/Runtime 锁不变。

Contracts 先提交，再按其完整 SHA 同步 API/Coze/Desktop。三个消费者都固定 `32dd76298fd5ba2346fe2429f78b2b3e2f32a7e4`。九份生成 wire/schema/validator 的 SHA256 与 D4 前完全相等，`release=false`、`1.0.0-local-candidate` 保持。

交付检查包括 Contracts lint、生成检查、11项正常测试及三个已登记完整基线的 breaking 检查；提交后再运行生成与三消费者检查。Infra 13项检查通过。API、Coze消费检查与上游来源检查通过。Coze canonical editor重构建/manifest检查通过，六个资产的内容哈希文件名、尺寸及入口HTML摘要与D4记录一致；新 manifest 为 `b0f90f4d8714c219fc7dccdd1780dfa814ee3a646aa3f818cf8aee5f564d2991`。Git来源/锁元数据改变，未把新manifest替换进旧真实运行证据。

Desktop 从暂存区导出单独快照，使用已安装工具执行类型检查、5文件21项测试和前端构建，全部通过。未启动真实App或Docker，也未重跑无关全仓测试。详细结果、初次命令纠正和明确边界见[交付验证](evidence/git-delivery-20260913/delivery-verification.json)。

## 既有修改与证据保护

先从混合的WorkflowPage反向恢复接入前文件，SHA256与最初审计记录 `7f986634d6933f6cea9696a982d2362fb1aa3da1f52c65857e66ea8e0fcbf11e` 相等，再以Git原页为底仅暂存工作流真实接入。工作区文件本身不改写。真实工作流控件依赖原有 `workflow-showcase.css` 与 `YjPageHeader` 描述插槽，因此两份作为既有设计依赖随提交，不归作新设计。

其余五份纯设计文件及WorkflowPage的既有展示交互保持未提交；八个受保护文件的最终工作区字节均未改变。Coze六份原缺失文档保留未暂存删除状态，不恢复，也不作为本需求删除。原有六个未涉及的兄弟仓库未提交或改动。

提交前扫描591份变更文件，对本地八项机器/数据凭据精确匹配及常见凭据模式匹配均为0；74张原验收图的OCR模式复核未发现邮箱、手机号或凭据模式。截图仍为原始实际证据，未编辑；原合成Chat侧栏属于边界验收上下文。这些检查不声称通用PII认证。见[文本检查](evidence/git-delivery-20260913/prestage-secret-scan.json)、[图像检查](evidence/git-delivery-20260913/image-review.json)。

## 下一次启动

旧ignored运行状态仍指向D4当时的构建。下次运行前按Infra文档正常执行 `make workflow-editor workflow-build workflow-up`，重新登记新来源与构建摘要，不手改旧状态或绕过漂移检查。本次没有启动栈、迁移、删卷或付费调用，四个验收数据卷保留。首次打开瞬时取消的真实点击未执行、既有配色例外以及生产范围仍按17记录。

最终元仓lint、50项测试、D4 strict及声明审计均通过（errors=0/warnings=0）。Coze私有远端的实际fresh clone通过来源检查：15,303个原文件一致、0个本地删除、2个声明overlay；原工作区仍为15,297个原文件一致及6个既有删除。两者均未改变上游基线。

原CLI输出包含工具自身表格尾空格/空行，保留原字节及既有摘要；本需求目录的`.gitattributes`仅对`evidence/**/*.txt`关闭源码空白诊断，Markdown、JSON、源码与辅助脚本继续执行普通diff检查。
