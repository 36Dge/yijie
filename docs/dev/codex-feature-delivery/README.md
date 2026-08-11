# Codex Feature Delivery v2

这是一套面向后续新需求的、可执行且可审计的交付协议。它把需求事实、工程证据和有权决策分开：Codex 可以调查、起草、实现、验证和审查，但不能用总结文字替代真实证据，也不能替人批准 Gate。

新需求只使用 `schema_version: 2`。历史 v1 Feature Package 原样只读保留，不批量回填、不把旧记录伪装成 v2。`legacy-v1-allowlist.txt` 固定四个历史目录的 basename 与规范化 tree digest；`--allow-legacy` 只能输出 `LEGACY_RECOGNIZED` inventory 元数据，`valid` 与进程退出码仍为失败，绝不返回 Gate PASS。任何非 `.DS_Store` 文件的增删、重命名或内容变化都会使 pin 失配。

## 体系的六个支点

1. **一个当前声明**：`feature.yaml` 保存 Profile、交付目标、边界、切片和产物索引；Gate 当前状态只从决策账本派生。
2. **两本追加账本**：`evidence.yaml` 保存实际执行事实，`decisions.yaml` 保存有权 Gate 决策。既有记录不得原地改写。
3. **内容寻址策略与 Schema**：`gate-policy.yaml` 是新包使用的 active policy；`policies/<sha256>.yaml` 保存逐字节不可变快照，JSON Schema 约束每个 active/历史版本。
4. **按实例交付**：`G2C` 对每个受影响 boundary 分别判断，`G3` 对每个 slice 分别判断，不能以一个总勾选覆盖所有消费者或切片。
5. **判定、身份与批准分离**：对适用 Gate，机器只计算 eligibility 的 `ELIGIBLE` 或 `BLOCKED`；裁剪项由 policy 派生 `not_applicable`。只有绑定精确 subject/evidence、且由包外 trust root 中有效 Ed25519 key 签名的决策才构成 `passed`。`actor.type: human` 自报不算身份认证。
6. **分段 digest 与分段完成**：G0/G1/G2 分别绑定 intake/scope/build，G2C/G3 绑定自己的 boundary/slice，G4/G5/G6 绑定 engineering/release。未到阶段的 Markdown 占位不阻塞早期 Gate；`--strict` 和 `lifecycle: completed` 才校验全部适用文档与终点摘要。

## Profile 与交付目标

两者正交，不能把风险等级和发布环境混成一个开关。

| 维度 | 取值 | 含义 |
|---|---|---|
| Profile | `lite` | 低风险、边界清晰、范围小；物理裁剪非必要文档 |
| Profile | `standard` | 常规跨模块需求；保留完整设计与验证链 |
| Profile | `controlled` | 高风险、受监管、跨仓、迁移或难回滚；强化审批和证据 |
| Target | `local_engineering` | 交付到 G4；G5/G6 由 policy 派生 `not_applicable`，不追加 N/A decision |
| Target | `staging` | 交付到目标环境并完成 G6 |
| Target | `production` | 生产发布并完成观察，终点为 G6 |

Profile 决定风险控制和产物深度，Target 决定生命周期终点。比如 `controlled + local_engineering` 仍需受控工程证据，但不因此宣称已经生产发布。

`controlled` 不是只多写几份文档：它使用更短的授权有效期、更严的代码/安全/数据审查和持久证据要求，并对环境、账户、数据分类、路径与动作做精确授权。

## Gate 路径

```text
G0 Intake Accepted
  → G1 Scope Ready
  → G2 Build Authorized
  → G2C Boundary Ready × 每个受影响 boundary
  → G3 Slice Accepted × 每个 slice
  → G4 Engineering Complete
  → G5 Release Authorized
  → G6 Outcome Verified
```

Gate 派生状态只有：`pending`、`blocked`、`ready`、`in_review`、`passed`、`failed`、`stale`、`not_applicable`；Decision 不允许自报 `not_applicable`。证据结果 `not_run`、计划执行、占位符、未签名的人类标签和 Codex 自述都不能显示为绿色。任何 subject、关键证据或前置 Gate 变化后，相关旧决策必须转为 `stale`，重新评估并批准。

G2 先批准整个 Feature 的有界构建范围；之后每个 G2C 只证明一个 Boundary 已就绪，并只解锁依赖它的 Slice。`04-contract-change-plan.md` 是 Boundary 索引，不是把所有边界混在一起的规范；每个受影响 Boundary 都有自己的 `boundaries/BND-NNN.md` 和 `boundary_digest`。

`approval-trust.yaml` 是 Feature Package 之外的身份信任根，默认没有 key，因此默认不能伪造出任何 `passed`。管理员在 Codex 不可访问的受保护环境生成/保管私钥，只把公钥、actor、role、Gate、Profile、Target 和有效期登记进受保护 base；CI 从 base 读取，或用 `CFD_APPROVAL_TRUST_ROOT` 指向独立只读 mount。`sign-decision.mjs` 对除 `attestation` 外的完整 Decision、Feature ID 与精确 gate-policy bytes digest 生成签名；签名后任何字段变化都会失效。信任根、verifier 或私钥若与待审代码处于同一可写信任域，密码学验证不构成独立授权。

## 完整目录

```text
codex-feature-delivery/
├── README.md
├── QUICKSTART.md
├── HANDBOOK.md
├── DOCUMENT_CATALOG.md
├── CODEX_PLAYBOOK.md
├── QUALITY_GATES.md
├── MIGRATION_V1_TO_V2.md
├── gate-policy.yaml
├── policies/
│   └── d55f4d0a53d2f7170b16bc84bcfca7c7c97aaa6a3791b2ce32f8561edac6bcfb.yaml
├── approval-trust.yaml
├── change-coverage-policy.yaml
├── legacy-v1-allowlist.txt
├── schemas/
│   ├── feature-package.schema.json
│   └── gate-policy.schema.json
├── checklists/
│   ├── definition-of-ready.md
│   ├── definition-of-done.md
│   └── production-readiness.md
├── examples/
│   └── feature-package-example.md
├── scripts/
│   ├── new-feature.sh
│   ├── check-feature-package.sh
│   ├── check-all-feature-packages.mjs
│   ├── check-changed-feature-coverage.mjs
│   ├── evaluate-feature-package.mjs
│   ├── policy-registry.mjs
│   ├── approval-attestation.mjs
│   ├── init-approver-key.mjs
│   ├── sign-decision.mjs
│   ├── legacy-v1.mjs
│   ├── materialize-boundary.mjs
│   └── materialize-delivery-summary.mjs
├── tests/
│   ├── evaluator.test.mjs
│   ├── change-coverage.test.mjs
│   ├── gate-policy-schema.test.mjs
│   └── policy-registry.test.mjs
└── templates/
    └── feature-package/
        ├── feature.yaml
        ├── evidence.yaml
        ├── decisions.yaml
        ├── boundary-spec.md
        ├── 00-feature-brief.md
        ├── 01-requirements.md
        ├── 02-impact-assessment.md
        ├── 03-decisions-and-risks.md
        ├── 04-contract-change-plan.md
        ├── 05-technical-design.md
        ├── 06-test-plan.md
        ├── 07-implementation-plan.md
        ├── 08-verification-report.md
        ├── 09-release-and-rollback.md
        └── 10-delivery-summary.md
```

仓库级 base-trusted 接线也属于本体系的必要交付物：

```text
yijie/
├── .github/workflows/feature-delivery-coverage.yml
└── docs/dev/codex-feature-delivery/   # 上述完整目录
```

生成器在初建时根据 Profile、Target 和 `feature.yaml.artifacts` 物理创建所需文档；后续新增风险或边界时，由 evaluator 按 policy 要求补充/物化对应产物。目录中存在模板，不代表每个包都必须复制全部模板。省略项必须在 artifact manifest 中记录策略依据和理由，不能用一堆空白文件假装“完整”。Boundary 由 `materialize-boundary.mjs` 按 ID 建立独立规范；Delivery Summary 只在 Target 终点 Gate 有效通过后由机器生成，frontmatter 绑定完整 terminal Decision digest，evaluator 从 manifest/ledger canonical 重建正文逐字比较，不只信任自报 `summary_body_digest`。生成后不手改，且不是 G4/G6 的输入证据。

## Changed-files required check

本仓 CI 已接入 `check-changed-feature-coverage.mjs`。target base 必须是 candidate head 的祖先，变更路径取 `merge-base(target base, head)...head`，G2 精确绑定当前 target base；报告分别给出 `target_base_sha`、`diff_base_sha`、`head_sha` 与 `code_sha`。沿无 merge 的 first-parent 链，`code_sha=C` 是最后一个修改 Feature root 外普通路径的实现提交；C 后只能追加 evaluator 识别的 Package 管理文件，最终普通路径 tree 必须与 C 相同。G3/G4 绑定 C，不绑定会因签名账本而变化的最终 head；纯 Package metadata diff 报告 `code_sha=null`。

普通实现路径仍须命中 G2 repository/path、最具体 Slice scope和所需 G3/G4。Feature Package 内只允许 core 文件与 `feature.yaml.artifacts[].path` 声明的文件，夹带未声明文件直接拒绝；重复 v2 `feature.id` 也直接拒绝。既有 v2 `decisions.yaml`、`evidence.yaml` 按 target base→每个后续 commit 逐步做 canonical prefix 校验，只能尾部追加，不能先追加再改写。

一次性豁免不是自由文本开关。repo 内 `change-coverage-policy.yaml` 必须按 lexical repo-relative path 从受保护 target-base Git blob 读取，并拒绝 symlink/tree mode；v3 摘要纳入 Git blob mode（`100644`/`100755`），只规范化匹配 exemption 自身的 `head_content_digest`，policy 其余语义与完整 changed-file set/内容全部入摘要。首次接入且 base 尚无 policy 时，head bootstrap 仍不能自证：管理员必须把同一 digest 写入不可由 PR 修改的 repository variable `CFD_FEATURE_DELIVERY_BOOTSTRAP_DIGEST`，workflow 映射为 `CFD_BOOTSTRAP_APPROVAL_DIGEST` 后双重匹配。

`approval-trust.yaml` 首 key/轮换和下一轮会执行的 runtime TCB（workflow、framework scripts/schemas、gate/change/versioned policies、legacy pin、package/lock/workspace、pnpm hooks、`repos.yaml`）使用独立两通道：PR 的全部变更都必须命中 base policy 的 `external_digest_only`，管理员在 PR 外把精确 change-set digest 写入 `CFD_FEATURE_DELIVERY_GOVERNANCE_DIGEST`，checker 再对候选文件执行适用的结构校验。普通 Feature、G4 或 head 自增信任均不能代替该通道。Gate policy 升级在同一受治理 TCB 变更中先新增以新 bytes SHA-256 命名且内容完全相同的快照，再切换 active `gate-policy.yaml`；不得覆盖/删除任何历史快照，也不得把 Package 更新混入策略 TCB 变更。旧 Package 与 Decision 继续按 manifest 中的历史 digest 解析，新 Package 由生成器绑定 active 的 id/version/digest。

`pull_request_target` workflow 只 checkout 受保护 target base 并执行其中 verifier/schema/policy，fetch 后先证明 PR ref commit 精确等于 event `head.sha`；候选 head 只作为 Git objects 被解析，不 checkout、不执行其 package scripts。它通过受分支限制的 `feature-delivery-trusted` Environment 中专用 GitHub App 的短期 token，先后向精确 head 发布 pending 与最终 success/failure，独立 context 为 `feature-delivery/trusted-coverage-status`。默认 `GITHUB_TOKEN` 没有 statuses 写权限。

workflow 监听 `edited` 以覆盖 PR retarget，并在取得专用 App token 后立即把 event head 状态改为 pending。Commit status 本身按 SHA 而不是 PR/base 组合存储，因此治理上禁止在旧 success 尚未被新事件覆盖时复用同一 head 或改投目标分支；branch protection 的 up-to-date 要求必须保持开启。需要消除这段事件处理竞态时，应把同一 base-trusted 校验移到专用 App webhook/平台级 required workflow，而不是放宽检查。

当前接线只支持 `pull_request_target` 到精确 PR head 的 status，尚未实现 `merge_group`。启用 merge queue 前必须增加同等 base-trusted 的 `merge_group` verifier/status；否则保持 merge queue 禁用，缺少 required context 会 fail closed 并卡住队列。

workflow 存在不等于 branch protection 已不可绕过。管理员必须要求上述独立 status context、将 expected source 固定为专用 App、开启 require branches up to date，并移除 bypass；不要要求 `Feature Delivery Coverage / base-trusted` 这个归属 base 的 job check。App 只授予 Commit statuses: write，Environment 仅允许受保护 base 分支访问，并配置 `CFD_STATUS_APP_CLIENT_ID`、`CFD_STATUS_APP_PRIVATE_KEY`；两个 digest variables 同样必须由 PR 不可写的管理员面保护。App token 无法签发或 status 无法发布时，required context 缺失，门禁 fail closed。每个兄弟代码仓仍须独立安装同等检查；中央元仓不能替兄弟仓强制执行。

## 从这里开始

- 15 分钟创建并检查一个 v2 包：[QUICKSTART.md](QUICKSTART.md)
- 完整生命周期、状态和失效规则：[HANDBOOK.md](HANDBOOK.md)
- 机器账本与每份文档的职责：[DOCUMENT_CATALOG.md](DOCUMENT_CATALOG.md)
- Codex 的上下文、授权和切片规程：[CODEX_PLAYBOOK.md](CODEX_PLAYBOOK.md)
- Gate 断言、实例和判定规则：[QUALITY_GATES.md](QUALITY_GATES.md)
- 历史包继续演进规则：[MIGRATION_V1_TO_V2.md](MIGRATION_V1_TO_V2.md)

## 责任边界

同一位负责人可以同时承担业务、技术、验证和发布角色，并在一次决策记录中声明其在 `feature.yaml` 已分配、且被签名 key scope 允许的多个 `roles`；不得伪造 actor、角色或不存在的独立人审。Codex Review、静态分析和测试结果都是 evidence，不是 APPROVED；Codex 不能接触审批私钥或替人运行签名。真实数据、外部写入、付费调用、部署、migration 和不可逆动作必须获得针对精确目标的新授权。有效权限是 Codex sandbox/approval policy、当前路径适用的 `AGENTS.md` 与 Feature Authorization Packet 的交集。
