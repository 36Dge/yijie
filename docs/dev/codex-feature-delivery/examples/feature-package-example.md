# V2 示例：任务列表按状态筛选

> **Purpose**：展示一个 `standard + local_engineering` 小型 Feature 的声明、Boundary、Slice、Evidence、Decision 与 evaluator 关系。
>
> **Authority**：这是虚构教学快照，不是实际批准或完整物理 package；字段以 v2 policy/schema/templates 为准。
>
> **适用 Profile / Target**：`standard` / `local_engineering`。
>
> **完成时点**：快照停在 G2 已通过、G2C 具备决策条件但尚未批准。

## 1. 需求与物理形态

`FEAT-204` 让有 `task:read` 权限的租户成员按 `running|succeeded|failed` 筛选任务；不改变默认列表，不发布到 staging/production。

真实目录由生成器创建。当前快照包含 core ledgers、`00`–`08` 的适用文档和独立 `boundaries/BND-001.md`；`04-contract-change-plan.md` 只导航该规范，不是共享 Contract 正文。以下两个文件缺席：

- `09-release-and-rollback.md`：target 为 `local_engineering`，不适用；
- `10-delivery-summary.md`：初始为 `conditional`，仅在终点 G4 通过后 materialize。

本文只展示关键片段，不能复制为新的需求包。

## 2. `feature.yaml` 关键声明

```yaml
schema_version: 2
kind: FeaturePackage
policy: {id: codex-feature-delivery/v2, version: 2.0.0, digest: "sha256:d55f4d0a53d2f7170b16bc84bcfca7c7c97aaa6a3791b2ce32f8561edac6bcfb"}

feature:
  id: FEAT-204
  slug: task-status-filter
  title: 任务列表按状态筛选
  summary: 租户成员可选择一个允许状态并获得租户隔离结果
  lifecycle: active
  profile: standard
  delivery_target: local_engineering
  created_at: 2026-08-11
  updated_at: 2026-08-11
  owners:
    accountable: duan.chengwei
    role_assignments:
      - actor: duan.chengwei
        roles: [accountable_owner, requirement_owner, technical_owner, reviewer]

classification:
  risk: medium
  data: internal
  risk_factors: [contract_change]

size: {class: medium, repositories: 3, boundaries: 1, acceptance_criteria: 3, slices: 4, estimated_active_days: 2}

acceptance_criteria:
  - {id: AC-001, statement: 筛选结果仅含本租户指定状态任务且保持分页语义}
  - {id: AC-002, statement: 未提供 status 时行为与当前列表一致}
  - {id: AC-003, statement: 非法 status 返回稳定错误且不执行查询}

repositories:
  - id: contracts
    identity: {kind: managed, name: yijie-contracts, url: "https://github.com/36Dge/yijie-contracts.git", root: ../yijie-contracts}
    path: openapi/internal
    root_scope_justification: null
    root_scope_exception_evidence_id: null
    role: authority
    baseline: {sha: 3333333333333333333333333333333333333333, evidence_id: EV-BASE-CONTRACTS-001}
  - id: api
    identity: {kind: managed, name: yijie-api, url: "https://github.com/36Dge/yijie-api.git", root: ../yijie-api}
    path: src
    root_scope_justification: null
    root_scope_exception_evidence_id: null
    role: producer
    baseline: {sha: 1111111111111111111111111111111111111111, evidence_id: EV-BASE-API-001}
  - id: web
    identity: {kind: managed, name: yijie-desktop, url: "https://github.com/36Dge/yijie-desktop.git", root: ../yijie-desktop}
    path: src
    root_scope_justification: null
    root_scope_exception_evidence_id: null
    role: consumer
    baseline: {sha: 2222222222222222222222222222222222222222, evidence_id: EV-BASE-WEB-001}

boundaries:
  - id: BND-001
    type: generated_schema
    impact: additive
    owner: duan.chengwei
    authority: yijie-contracts@3333333333333333333333333333333333333333:openapi/internal/task-api.openapi.yaml
    producers: [api]
    consumers: [web]
    known_unknowns: [旧 consumer 忽略可选参数, 未知 enum 使用稳定错误 envelope]
    artifact_id: ART-BOUNDARY-BND-001

slices:
  - id: SLC-001
    title: 状态 enum 与纯验证规则
    outcome: 非法状态在访问 repository 前失败
    depends_on: []
    boundary_ids: []
    acceptance_criteria: [AC-003]
    repositories: [api]
    paths: [{repository: api, path: src}]
    authorization_decision_id: DEC-G2-001
  - id: SLC-002
    title: Contract First 参数与生成兼容检查
    outcome: 中央权威契约声明可选 status 且生成物通过兼容校验
    depends_on: []
    boundary_ids: [BND-001]
    acceptance_criteria: [AC-002, AC-003]
    repositories: [contracts]
    paths: [{repository: contracts, path: openapi/internal}]
    authorization_decision_id: DEC-G2-001
  - id: SLC-003
    title: 租户隔离 API 筛选
    outcome: API 仅返回本租户匹配任务
    depends_on: [SLC-001, SLC-002]
    boundary_ids: [BND-001]
    acceptance_criteria: [AC-001, AC-002, AC-003]
    repositories: [api]
    paths: [{repository: api, path: src}]
    authorization_decision_id: DEC-G2-001
  - id: SLC-004
    title: Web 筛选交互
    outcome: 用户可选择和清除筛选
    depends_on: [SLC-003]
    boundary_ids: [BND-001]
    acceptance_criteria: [AC-001, AC-002]
    repositories: [web]
    paths: [{repository: web, path: src}]
    authorization_decision_id: DEC-G2-001

# 完整 manifest 还含 dependencies 与全部 artifact 声明；这里仅展示条件项。
artifacts:
  - {id: ART-CONTRACT, kind: contract_change_plan, path: 04-contract-change-plan.md, authority: index, applicability: required, reason: boundaries_present}
  - {id: ART-BOUNDARY-BND-001, kind: boundary_spec, path: boundaries/BND-001.md, authority: normative, applicability: required, reason: boundary_BND-001}
  - {id: ART-RELEASE, kind: release_and_rollback, path: 09-release-and-rollback.md, authority: normative, applicability: not_applicable, reason: local_engineering_target}
  - {id: ART-SUMMARY, kind: delivery_summary, path: 10-delivery-summary.md, authority: summary, applicability: conditional, reason: materialize after G4}
```

## 3. 具体 Evidence 与 Decision ID

真实 ledgers 保存完整 digest、subject、command、工具版本、时间和 artifact；这里用索引避免重复原始事实。

| Evidence ID | kind | subject/result | 用途 |
|---|---|---|---|
| `EV-BASE-CONTRACTS-001` | baseline | `contracts@333…333 / passed` | G2 Contract authority baseline |
| `EV-BASE-API-001` | baseline | `api@111…111 / passed` | G2 baseline |
| `EV-BASE-WEB-001` | baseline | `web@222…222 / passed` | G2 baseline |
| `EV-BND-001` | boundary_validation | `BND-001 / passed` | 使 G2C 具备决策条件，不自动批准 |

| Decision ID | Gate/instance | state | 绑定与授权 |
|---|---|---|---|
| `DEC-G0-001` | `G0/feature` | passed | 当前 `intake_digest`；允许影响分析 |
| `DEC-G1-001` | `G1/feature` | passed | 当前 `scope_digest`；允许设计与测试计划 |
| `DEC-G2-001` | `G2/feature` | passed | 当前 `build_digest` + 三条 baseline；精确授权 SLC-001..004/repository/base/path，禁止 deploy |

三条 `passed` 都包含由受保护 trust root 中 `duan.chengwei` key 生成的 `ed25519-v1` attestation；表格省略 signature/payload digest 只是为了可读性，不能据此构造真实账本。没有 G2C Decision。G2 先用一个有范围、期限和失效条件的 packet 授权四个 Slice；随后每个受影响 Boundary 单独过 G2C。只有引用该 Boundary 的 Slice 被 G2C 阻塞，无 Boundary 的 SLC-001 可在具备测试证据后独立流动。跨仓 schema 的唯一权威始终是 `yijie-contracts` 的不可变 ref，API/Desktop 不维护影子契约。

## 4. Evaluator 输出

```text
VALID: FEAT-204 profile=standard target=local_engineering
DIGEST intake_digest=sha256:1010…1010 scope_digest=sha256:2020…2020 build_digest=sha256:3030…3030
DIGEST boundary_digest/BND-001=sha256:4040…4040
DIGEST slice_digest/SLC-001=sha256:5151…5151 slice_digest/SLC-002=sha256:5252…5252 slice_digest/SLC-003=sha256:5353…5353 slice_digest/SLC-004=sha256:5454…5454
DIGEST engineering_digest=sha256:6060…6060 release_digest=sha256:7070…7070
GATE G0 instance=feature state=passed eligibility=ELIGIBLE decision=DEC-G0-001
GATE G1 instance=feature state=passed eligibility=ELIGIBLE decision=DEC-G1-001
GATE G2 instance=feature state=passed eligibility=ELIGIBLE decision=DEC-G2-001
GATE G2C instance=BND-001 state=pending eligibility=ELIGIBLE decision=none
GATE G3 instance=SLC-001 state=pending eligibility=BLOCKED decision=none
  - SLC-001 缺少成功测试 Evidence
GATE G3 instance=SLC-002 state=pending eligibility=BLOCKED decision=none
  - 前置 G2C/BND-001 未通过（pending）
GATE G3 instance=SLC-003 state=pending eligibility=BLOCKED decision=none
  - 前置 G2C/BND-001 未通过（pending）
GATE G3 instance=SLC-004 state=pending eligibility=BLOCKED decision=none
  - 前置 G3/SLC-003 未通过（pending）
GATE G4 instance=feature state=pending eligibility=BLOCKED decision=none
GATE G5 instance=feature state=not_applicable eligibility=NOT_APPLICABLE decision=none
GATE G6 instance=feature state=not_applicable eligibility=NOT_APPLICABLE decision=none
```

`VALID` 只表示结构有效；`ELIGIBLE` 只表示可以由 Gate Owner 决策。Evaluator 不替人批准。下一步是追加绑定当前 `boundary_digest[BND-001]` 的 G2C `passed` 决策，再分别实施和验收 Slice；local target 最终止于 G4，G4 通过后才生成 Summary，不能写成生产交付完成。
