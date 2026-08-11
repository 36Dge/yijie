# 快速开始：创建第一个 v2 Feature Package

以下命令均在 `docs/dev/codex-feature-delivery/` 下执行。

## 0. 管理员一次性建立审批信任根

在 Codex/待审代码不可访问的受保护终端或 CI 管理面执行；私钥必须放在仓库和 Agent sandbox 之外，绝不能提交：

```bash
node ./scripts/init-approver-key.mjs \
  --actor "段成威" --key-id duan-approval-2026 \
  --private-key /protected/feature-delivery/duan-ed25519.pem \
  --trust-root ./approval-trust.yaml \
  --role accountable_owner --role requirement_owner \
  --role technical_owner --role reviewer \
  --gate G0 --gate G1 --gate G2 --gate G2C \
  --gate G3 --gate G4 \
  --profile standard \
  --target local_engineering \
  --valid-until "2026-11-11T00:00:00+08:00"
```

示例 key 只覆盖本页随后创建的 `standard + local_engineering` 包，并且只到 G4。按职责、Gate、Profile、Target 和有效期创建最小 scope；不要为了省一次登记而生成全域 key。G5/G6 必须使用单独的 release-owner key，只开放实际需要的 `staging|production` Target，并采用与发布窗口相称的更短有效期。

默认空 trust root 是有意的 fail-closed 状态。首 key 与以后轮换都必须走独立的 trust-only PR，不能夹带实现、policy 或 Feature Package 变更。先用 base-trusted checker 的 JSON 输出取得该唯一变更的 `change_set_digest`，再由仓库管理员在 PR 之外把它写入 repository variable `CFD_FEATURE_DELIVERY_GOVERNANCE_DIGEST`；候选 trust root 还会经过严格字段、scope、时间、Ed25519 公钥和重复指纹校验。待审 PR 不能设置这个变量，也不能用自己新增的 key 验自己的 Decision。

若 CI 从仓库外只读 mount 提供 trust root，显式设置 `CFD_APPROVAL_TRUST_ROOT=/protected/feature-delivery/approval-trust.yaml` 后再运行 checker/summary materializer；签名命令则同时传 `--trust-root "$CFD_APPROVAL_TRUST_ROOT"`。不要把候选 PR 自己的路径写入该变量。

首次安装本体系且 base 尚无 coverage policy 时，管理员还要把 `change-coverage-policy.yaml` 中 bootstrap `head_content_digest` 的同一值预先写入 GitHub repository variable `CFD_FEATURE_DELIVERY_BOOTSTRAP_DIGEST`；待审 PR 不能修改该变量。摘要只规范化 exemption 自身的 `head_content_digest` 自引用字段，policy 的其余内容与全部候选文件字节都进入摘要。若 base 连 `pull_request_target` workflow 都没有，候选 PR 新增的 workflow 本身不会成为 base-trusted check；首次合并必须由平台级 required workflow 或管理员从已审查的不可变 verifier 独立复算并核对该 pin，不能信任 head CI 自证。合并后 policy/workflow 来自 base，此一次性 pin 不再参与普通 Feature 流程。

## 1. 创建包

```bash
./scripts/new-feature.sh FEAT-123 task-history-export \
  --profile standard \
  --target local_engineering \
  --repository-id yijie \
  --title "导出任务历史" \
  --owner "段成威" \
  --output-root ../../features
```

必填选择：

- `--profile lite|standard|controlled`：控制风险深度和文档裁剪；
- `--target local_engineering|staging|production`：控制必须走到的 Gate 终点。

生成器把当前 Git repo 写成 `repositories[].identity={kind,name,url,root}`。跨 sibling repo 时，不要把 `../yijie-*` 填进授权路径：`kind=managed` 的 identity 必须与中央 `repos.yaml` 的 `name/path/url` 精确一致；`repositories[].path`、`slices[].paths` 和 `authorization.paths` 始终是该 repo **内部**的相对 scope。后两者使用 `{repository, path}`，拒绝绝对路径、`..`、空段和 glob。`.` 代表整仓，必须有 justification；`controlled`/高风险 G2 还要引用逐仓成功的 `exception` Evidence。

不要复制历史 v1 包作为起点。生成器会建立 v2 `feature.yaml`、追加式 `evidence.yaml`/`decisions.yaml`，并按 artifact manifest 创建适用文档。

命令必须从新 Feature 所属的 Git worktree 内运行；可以使用本中央目录中脚本的绝对路径为 sibling repo 建包。生成器把 invocation worktree 作为 `kind: current`，默认输出到该 worktree 的 `docs/features`；脱离 Git 的目录会直接拒绝。

## 2. 先验证骨架

```bash
./scripts/check-feature-package.sh ../../features/FEAT-123-task-history-export
```

默认检查 v2 Schema、策略、引用和产物一致性，不批准任何 Gate。Markdown 完成度按 Gate 分段检查：还未到阶段的模板变量不会阻塞 G0/G1，但一旦请求对应 Gate、将 `lifecycle` 改为 `completed` 或使用 `--strict`，所有已到期的适用文档必须完成。若输出 `INVALID`，按错误位置补事实；不要把 `not_run` 改成 `passed` 来消除报错。

## 3. 完成 G0：接受 Intake

补齐：

- `00-feature-brief.md` 中的问题、价值、范围、非目标和 Owner；
- `feature.yaml` 中的 Profile、Target、仓库线索、外部副作用和数据分类；
- 初始决策问题及明确禁止的动作。

机器评估：

```bash
./scripts/check-feature-package.sh --gate G0 ../../features/FEAT-123-task-history-export
```

机器只报告是否具备决策条件。由有权负责人先在 `decisions.yaml` 起草绑定当前 subject 的 Decision（`attestation: null`），在受保护审批面复核精确内容并签名，再运行同一 Gate 命令：

```bash
node ./scripts/sign-decision.mjs \
  ../../features/FEAT-123-task-history-export DEC-FEAT-123-G0-001 \
  --key-id duan-approval-2026 \
  --private-key /protected/feature-delivery/duan-ed25519.pem \
  --trust-root ./approval-trust.yaml

./scripts/check-feature-package.sh --gate G0 \
  ../../features/FEAT-123-task-history-export
```

未签名记录只是草案；`actor.type: human` 和角色字符串不能认证身份。`sign-decision.mjs` 不覆盖已有 attestation；已签记录一经提交即 append-only，任何内容变化都必须追加带 `supersedes` 的新 Decision 并重新签名。Codex 可以准备草案，不能读取私钥或代替人类/受保护审批流程签名。

## 4. 只读调查、baseline 与切分

第一轮给 Codex：

```text
目标：为 FEAT-123 建立实现前事实，不修改文件、不访问真实数据或外部写接口。

请读取适用的 AGENTS.md 和仓库文档，检查 Git 状态，找到入口、测试、契约、
数据、consumer 和发布控制面。分别输出 Fact / Assumption / Unknown，并记录：
1. 每个仓库的完整 HEAD、工作区状态、可重复 baseline 命令和结果；
2. 每个 producer/consumer/数据/权限/外部系统 boundary；
3. 需求 size、依赖、关键路径和是否必须拆为 Epic；
4. contract、migration、安全、AI、费用与不可逆风险；
5. 需要有权人回答的问题。

不得实现；不得把计划命令写成已执行证据。
```

把真实运行结果追加到 `evidence.yaml`，把调查结论写入 `02-impact-assessment.md`。baseline 必须在 G2 前完成；既有失败单独记录，不能被新需求吞并。大需求拆成 Epic 和可独立接受的 Feature；`controlled` 或跨仓需求在正式铺开前设计 walking skeleton。

## 5. 通过 G1、G2 和适用的 G2C

G1 前确认可判定 AC、边界、依赖和风险；G2 前确认方案、测试、切片、baseline、size 和依赖计划。声明 `BND-001` 时，先在其 `artifact_id` 写约定的 forward ref `ART-BOUNDARY-BND-001`，然后立即运行 materializer：

```bash
node ./scripts/materialize-boundary.mjs \
  ../../features/FEAT-123-task-history-export BND-001
```

forward ref 存在但 artifact 尚未建立的短暂中间态会被 evaluator fail-closed，不得提交或用于 Gate。脚本原子创建 `boundaries/BND-001.md` 和 `boundary_spec` artifact，并回写同一 ID。`04-contract-change-plan.md` 由首个 Boundary materialize 时建立，只是索引。

完成 G2 构建计划和有界 Authorization Packet 后，先对整个 Feature 批准 G2，再对每个受影响 Boundary 分别评估 G2C：

```bash
./scripts/check-feature-package.sh --gate G1 ../../features/FEAT-123-task-history-export
./scripts/check-feature-package.sh --gate G2 ../../features/FEAT-123-task-history-export
./scripts/check-feature-package.sh --gate G2C --instance BND-001 \
  ../../features/FEAT-123-task-history-export
```

不能用一个“Contract Ready”覆盖多个 consumer。每个 G2C 决策绑定具体 `boundary_digest`、schema/语义基线、producer、consumer、生成器和兼容证据；边界改变时只使相关 G2C、依赖 Slice 和后续集成决策失效，不误伤无关 Boundary。

## 6. 按 G2 授权逐切片实现

G2 Authorization Packet 必须显式覆盖将实施的全部 slice instance，并以结构化 `{repository, path}` 精确等于这些 Slice scope，给出每仓 base SHA、允许/禁止 capability、`environment: local_engineering`、`account: null`、数据分类、预算、期限、停止条件、所需 evidence 和重新授权触发器。一个有界 G2 Packet 可覆盖多个 Slice；执行轮次只选择其中一个切片，不额外产生逐 Slice 人工批准。`account: null` 明确不授权真实账号，目标账号只在 G5 新授权中绑定。`allowed_actions`/`excluded_actions` 只能使用 policy 的 canonical capability enum；有效能力是 packet 允许集与 Gate 策略允许集的交集，再扣除禁止集，不能用自由文本同义词绕过。

```text
实现 FEAT-123 的 SLC-001，使用 G2 决策中的有界 Authorization Packet。
仅修改 packet 列出的仓库与路径；先验证前置 SHA 和 Gate。
按测试→最小实现→局部验证→完整 diff 审查闭环执行。
若范围、subject、依赖或前置事实改变，停止并将授权标为失效。
不得自行执行外部写、真实数据读取、付费调用、部署、migration 或不可逆动作。
```

完成后把命令事实追加到 `evidence.yaml`：时间序必须合理，G3/G4 `code_refs` 逐仓包含 `sha + base_sha`，成功测试证据覆盖该 Slice 的 AC，日志/制品有 digest，且 `retention_until` 覆盖所引用 Decision 的 `valid_until`。`controlled` 的 `static_analysis`，以及 G4 的 `review`/`security_review`/适用 `data_review`，都必须逐仓匹配同一 code/base。把面向人的解释写入 `08-verification-report.md`，再对该 slice 评估：

```bash
./scripts/check-feature-package.sh --gate G3 --instance SLC-001 \
  ../../features/FEAT-123-task-history-export
```

新的外部副作用即使与原切片相关，也必须获得新的精确授权。

## 7. 工程完成与目标终点

全部 slice 和 boundary 完成后评估 G4：

```bash
./scripts/check-feature-package.sh --gate G4 ../../features/FEAT-123-task-history-export
```

- `local_engineering`：终点是 G4；G5/G6 由 target policy 派生 `not_applicable`，不在 `decisions.yaml` 追加 N/A decision，不得声称已发布。
- `staging` / `production`：继续准备发布 DAG、制品、迁移、观测、停止和恢复，再走 G5 与 G6。

发布步骤按依赖 DAG 和安全不变量排序，不套用固定 `deploy → migrate`。每个节点必须写明前置、验证、停止条件和补偿/前向修复策略。

```bash
./scripts/check-feature-package.sh --gate G5 <package>
./scripts/check-feature-package.sh --gate G6 <package>
node ./scripts/materialize-delivery-summary.mjs <package>
./scripts/check-feature-package.sh --strict <package>
```

G6 前确认所有 post-G5 Evidence 晚于当前有效 G5，按 `release_execution → smoke → observation/acceptance` 排序；每个使用的 Evidence kind 分别覆盖全部 AC，并与 G5 的 environment、account、artifact refs 连续。再让 Target 终点基于当前 subject 通过，由脚本生成 Delivery Summary 的严格 frontmatter 和派生导航；`terminal_decision_digest` 绑定完整终点 Decision，evaluator 会从 manifest/ledger canonical 重建正文逐字校验，而不只相信 `summary_body_digest`。Summary 是终点后的闭环记录，绝不是 G4/G6 输入。terminal subject 变化时，先追加新 terminal decision，在受审查的变更中移除可由 Git 恢复的旧派生 Summary，再重新生成；脚本本身不覆盖已有文件。`--strict` 要求全部适用 Gate 有有效决策且终点总结与当前 terminal decision/digest 一致；它不是“代码一定正确”的证明。

## 8. 遇到旧包

```bash
./scripts/check-feature-package.sh --allow-legacy <legacy-v1-package>
```

只有 basename 与 `legacy-v1-allowlist.txt` 中的规范化 tree digest 都精确匹配时，JSON 才会显示 `legacy: true`、`recognized: true`、`verdict: LEGACY_RECOGNIZED`；`valid` 仍为 `false`，命令仍以非零状态退出，避免只看退出码的下游误判为 PASS。若旧需求需要继续实施，创建新的 v2 包并以只读引用关联旧包，不修改历史证据。

## 9. 提交前检查 changed-files 覆盖

CI 要求当前 target base 是候选 head 的祖先；路径集合取 `merge-base(target base, head)...head`，但 G2 `base_ref` 必须绑定当前 target base SHA，而不是较旧的 merge-base：

```bash
pnpm feature-delivery:changes \
  --base <BASE_REF> --head <HEAD_REF> --repo-id yijie
```

本地尚未提交时可显式传路径；若路径需要 G2/G3 覆盖，还要给出真实 base/code SHA：

```bash
pnpm feature-delivery:changes \
  --file src/example.ts --repo-id yijie \
  --feature-root docs/features \
  --base-sha <40_HEX_BASE> --code-sha <40_HEX_IMPLEMENTATION_COMMIT>
```

本地 `--file` 只用于预检；合并门禁必须使用 base/head 模式。Git 模式报告 `target_base_sha`、`diff_base_sha`、`head_sha` 和 `code_sha`。沿无 merge 的 first-parent 链，最后一个修改 Feature root 外普通路径的提交是 implementation commit C；C 后只允许 Package 管理文件，G3/G4 的 `code_ref` 绑定 C。纯 Package metadata diff 的 `code_sha` 为 `null`。包内 core/manifest artifacts 之外的文件直接拒绝；Decision/Evidence 在 target base→每个 commit 都只能 canonical 尾部追加。

管理员先创建专用 GitHub App（repository permission 仅 Commit statuses: write），再建立仅允许受保护 base 分支访问的 Environment `feature-delivery-trusted`，其中配置 `CFD_STATUS_APP_CLIENT_ID` 与 `CFD_STATUS_APP_PRIVATE_KEY`。branch protection 要求独立 status context `feature-delivery/trusted-coverage-status`，expected source 固定为该 App，并开启 require branches up to date；不要要求归属 base SHA 的 `Feature Delivery Coverage / base-trusted` job check。

该 `pull_request_target` workflow 只 checkout 受保护 target base，使用 base 中的 verifier/schema/policy，核对 fetched PR ref 等于 event head 后只解析 Git objects，绝不 checkout 或执行候选 package scripts；默认 `GITHUB_TOKEN` 保持只读，专用 App token 负责向精确 head 发布 pending 与最终状态。不要把 `N/A`、PR 文本或普通 CI 环境变量当豁免；只有受保护 base policy 中的精确 exemption，或管理员控制的 bootstrap/governance digest 通道可以放行。

workflow 监听 PR `edited` 并在取得 App token 后立即向 event head 写 pending；治理上仍禁止在旧状态尚未被新事件覆盖时跨 PR/base 复用同一 head。当前没有 `merge_group` verifier，启用 merge queue 前必须先实现同等 base-trusted status，否则保持禁用。

runtime TCB（workflow、scripts/schemas、gate/change/versioned policies、approval trust、legacy pin、package/lock/workspace、pnpm hooks、`repos.yaml`）只能作为隔离的 `external_digest_only` PR，由管理员把精确摘要临时写入 `CFD_FEATURE_DELIVERY_GOVERNANCE_DIGEST`。升级 Gate policy 时，以新 policy 原始 bytes 的 SHA-256 新增不可变 `policies/<digest>.yaml`，并在同一隔离 TCB 变更中切换 active `gate-policy.yaml`；不得混入 Feature Package。既有 Package 与 Decision 保持历史 digest，由 registry 继续解析，不能批量改写；只有升级后创建的新 Package 绑定新 active policy。
