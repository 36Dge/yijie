# GitHub Actions 接入指南

本文描述可选的 GitHub enforcement adapter。它是接入示例，不会因运行初始化器而自动上线。核心规范见 [HANDBOOK.md](../HANDBOOK.md)，Git 对象算法见 [git.md](git.md)。

## 1. 初始化器会做什么

使用 Node.js 24–26。先安装发行源依赖：

```bash
(cd "<DISTRIBUTION_ROOT>" && npm ci --ignore-scripts)
```

再从发行源初始化：

```bash
node <DISTRIBUTION_ROOT>/scripts/init-project.mjs \
  --project-root <PROJECT_ROOT> \
  --project-id <PROJECT_ID> \
  --repository-id <REPOSITORY_ID> \
  --actor-id <ACTOR_ID> \
  --ci github
```

初始化器从 `<DISTRIBUTION_ROOT>` 原子复制发行包到项目 `<FRAMEWORK_ROOT>`，并从发行源的 `integrations/github/` 物化候选 workflow/config 和项目治理文件。成功后安装项目内依赖：

```bash
(cd "<FRAMEWORK_ROOT>" && npm ci --ignore-scripts)
```

初始化器不会也不能自动完成：

- 创建 GitHub App；
- 写入 App private key；
- 创建或保护 Environment；
- 设置 repository variables；
- 修改 branch protection 或 ruleset；
- 设置 required status expected source；
- 开启或关闭 merge queue。

这些都是管理员在 GitHub 控制面执行的外部动作。完成前不得宣称 required enforcement 已启用。

## 2. 信任模型

required workflow 必须：

1. 在 `pull_request_target` 事件中只 checkout 受保护 target-base SHA；
2. 从 target base 执行 verifier、Schema 和 policy；
3. fetch 后证明 PR ref commit 精确等于事件的 `head.sha`；
4. 只把候选 head 作为 Git objects 解析，不 checkout、不执行候选脚本；
5. 用短期、最小权限 GitHub App token 向精确 head 发布独立 status；
6. token 签发、验证或 status 发布失败时 fail closed。

默认 `GITHUB_TOKEN` 应保持只读。专用 App 只需要 `Commit statuses: write`，不要授予内容写入、PR 修改或管理权限。

## 3. 管理员配置

名称应由项目配置确定；以下仅为示例：

| 对象 | 示例值 | 要求 |
|---|---|---|
| Environment | `feature-delivery-trusted` | 仅受保护 base 分支可访问 |
| Required status | `feature-delivery/trusted-coverage-status` | expected source 固定到专用 App |
| App client variable | `CFD_STATUS_APP_CLIENT_ID` | PR 不可写 |
| App private-key secret | `CFD_STATUS_APP_PRIVATE_KEY` | 仅受保护 Environment 可读 |
| Bootstrap digest | `CFD_FEATURE_DELIVERY_BOOTSTRAP_DIGEST` | 一次性接入，由管理员预先写入 |
| Governance digest | `CFD_FEATURE_DELIVERY_GOVERNANCE_DIGEST` | TCB 变更时由管理员写入精确摘要 |

branch protection 或 ruleset 必须：

- 要求独立 status context；
- 将 expected source 固定到专用 App；
- 要求分支基于最新受保护 base；
- 禁止普通开发者绕过；
- 避免把归属 base SHA 的 workflow job check 误当成候选 head required status。

## 4. 首次 Bootstrap

首次接入时，target base 可能尚无 workflow 或 coverage policy。候选 head 不能用自己新增的 verifier 自证。

管理员必须从已审查、不可变的 canonical runtime 运行独立 CLI；不得从候选 checkout、候选依赖或候选 workflow 运行：

```bash
node <CANONICAL_RUNTIME>/scripts/verify-first-bootstrap.mjs \
  --repo-root <PILOT_REPOSITORY> \
  --repository <OWNER/REPOSITORY> \
  --repo-id <REPOSITORY_ID> \
  --target-branch <TARGET_BRANCH> \
  --base <EXACT_TARGET_BASE_SHA> \
  --head <EXACT_CANDIDATE_HEAD_SHA> \
  --authorization-id <UNIQUE_AUTHORIZATION_ID> \
  --approval-reference <EXTERNAL_APPROVAL_REFERENCE> \
  --created-at <RFC3339_CREATED_AT> \
  --expires-at <RFC3339_EXPIRES_AT> \
  --json
```

无 pin 的第一次运行必须退出 `1` 并输出 `BOOTSTRAP_DIGEST_REQUIRED` 与 `expected_bootstrap_digest`；这只是待管理员复算的诊断，不是 PASS。管理员在仓外复核 repository、base/head/tree、完整 changed-file 表、component digests、授权引用和有效期后，把同一摘要放入候选不可写的临时授权通道，再以完全相同参数加 `--bootstrap-digest sha256:...` 复核。只有退出 `0` 且 verdict 为 `BOOTSTRAP_DIGEST_APPLIED` 才表示内容授权匹配。

首次 bootstrap 使用独立 domain `codex-feature-delivery/first-bootstrap/v1`，不是普通 `change-set/v3`。它采用无歧义长度前缀编码，绑定 canonical distribution version/digest、active policy digest、repository full name/ID、target branch、精确 base/head/tree、完整 path/mode/size/content、project config、registry、coverage policy、严格空 trust root、rendered workflow，以及最长 24 小时的外部授权。repository/base/head/path/mode/content 任一变化都必须产生新摘要；跨仓摘要不可互换。

CLI 还会拒绝：base 已有或部分存在 v2 控制面、非线性/merge history、非规范或非法 UTF-8 path、symlink/gitlink/special mode、非空 trust、持久 exemption、非 canonical runtime/manifest/policy snapshot、错误 repository identity，以及会运行候选 head 的 workflow。Git object 没有 checkout inode/hardlink 语义；验证器只接受 manifest 声明的普通 blob，不从候选物理文件系统取信。

若 base 尚无可执行 workflow，则由管理员控制的离线环境、专用 App webhook或平台级 required workflow运行上述 canonical CLI完成首次合并。候选 head workflow 的绿色结果不能作为首次 bootstrap 证据。

首次接入合并后，后续 CI 永远优先使用 target-base 版本。bootstrap pin 不得成为普通 Feature 的长期豁免。

## 5. Trust root 与 TCB 轮换

首个审批 key、key 轮换，以及 workflow、scripts、schemas、policies、trust root、repository registry 和依赖锁等 TCB 变更必须使用隔离变更集：

1. base policy 把全部候选路径归类为 external-digest-only；
2. 管理员在 PR 外复核并登记精确 change-set digest；
3. base-trusted checker 校验 digest 和候选文件结构；
4. 变更中不得混入 Feature 实现或账本更新。

普通 G4、PR 批准或 head 中新增的 key 都不能替代第二通道。

## 6. PR retarget 与状态竞态

workflow 应监听会改变 base 语义的事件，包括 PR `edited`/retarget，并在取得 App token 后尽快把事件 head 状态写为 pending。GitHub commit status 以 SHA 为键，不以 PR/base 组合为键，因此治理上禁止在旧 success 尚未被新事件覆盖时跨 PR 或 base 重用同一 head。

需要完全消除事件竞态时，应使用专用 App webhook 或组织级 required workflow 执行相同的 base-trusted 算法，而不是放宽检查。

## 7. Merge queue

本发行版默认不提供 `merge_group` verifier。启用 merge queue 前，管理员必须部署同等 base-trusted 的 `merge_group` 验证和 status 发布；在此之前保持 merge queue 禁用。缺少 required context 时必须 fail closed。

## 8. 上线验收

- [ ] workflow 从 target base 运行，候选脚本从未被执行
- [ ] App 只有 Commit statuses 写权限
- [ ] Environment 与 secrets 只对受保护 base 可用
- [ ] required status expected source 固定到 App
- [ ] branches-up-to-date 已启用且 bypass 已移除
- [ ] bootstrap/governance digest 不能由 PR 修改
- [ ] retarget 会使旧状态失效或立即变为 pending
- [ ] token/status 发布故障实际阻塞合并
- [ ] merge queue 保持禁用，或已有等价 `merge_group` verifier

完成所有检查后，才可以声明 GitHub required enforcement 已上线。
