# 可跟踪证据包（提交准备阶段）

入口：[当前交付状态](../../16-delivery-status-and-evidence.md) · [逐仓提交计划](../../17-cross-repository-commit-plan.md)。

当前本地提交及新来源见[18](../../18-local-commit-baseline.md)。本目录candidate和cross-repository-files保留准备阶段身份，不作为提交后的动态工作树清单。

本包整理既有真实记录，不构成新的产品验收。原始 `.log` 保持原样；选中日志以脱敏 `.txt` 归档，不修改全仓忽略规则。`${WORKSPACE}` 表示七个兄弟仓所在目录，`${LOCAL_HOME}` 表示开发机用户目录。

共选择 **33 份完整命令输出**；其余 **38 份**中间或重复日志保留本地，逐一列在[归档清单](log-archive-manifest.json)。每份记录原文/归档双 SHA-256、字节数和替换次数；失败和警告保留。

## 阅读顺序

1. [候选身份](candidate.json)：源码摘要、manifest、契约锁、Desktop 校验值及资格边界。
2. [日志索引](log-archive-manifest.json)：按轮次定位可提交日志；历史 JSON 内的旧 `.log` 路径使用此表映射，旧路径本身不承诺随 Git 提交。
3. [截图登记](screenshot-ledger.json)：真实 App 本地导出 0 张；现有 3 张仅为 D0 静态示意。没有伪造截图路径或视觉通过证据。
4. [逐文件归属与摘要](cross-repository-files.json)：Contracts / Coze / Desktop / API / Infra / 元仓及独立主题依赖。
5. [本轮检查](package-checks.json)与[真实文档命令输出](document-checks.json)：文档检查、脱敏/归档/链接校验、保护文件和 Git 身份/index 核对。

## 完整输出索引

| 轮次 | 原始命令输出名 | 可跟踪副本 |
|---|---|---|
| ac009-verification | `focused-checks-final.log` | [查看](command-output/ac009-verification/focused-checks-final.txt) |
| ac009-verification | `csp-checks-final.log` | [查看](command-output/ac009-verification/csp-checks-final.txt) |
| ac009-verification | `editor-build-final.log` | [查看](command-output/ac009-verification/editor-build-final.txt) |
| ac009-verification | `source-checks-final.log` | [查看](command-output/ac009-verification/source-checks-final.txt) |
| ac009-verification | `editor-registration-final.log` | [查看](command-output/ac009-verification/editor-registration-final.txt) |
| ac009-verification | `service-build-final.log` | [查看](command-output/ac009-verification/service-build-final.txt) |
| ac009-verification | `service-up-final.log` | [查看](command-output/ac009-verification/service-up-final.txt) |
| ac009-verification | `desktop-launch-final.log` | [查看](command-output/ac009-verification/desktop-launch-final.txt) |
| ac009-verification | `runtime-before.log` | [查看](command-output/ac009-verification/runtime-before.txt) |
| ac009-verification | `runtime-final.log` | [查看](command-output/ac009-verification/runtime-final.txt) |
| ac009-verification | `service-stop-before-fix.log` | [查看](command-output/ac009-verification/service-stop-before-fix.txt) |
| ac009-verification | `service-stop-before-focus-order-fix.log` | [查看](command-output/ac009-verification/service-stop-before-focus-order-fix.txt) |
| full-ui-implementation | `focused-checks-r2.log` | [查看](command-output/full-ui-implementation/focused-checks-r2.txt) |
| full-ui-implementation | `csp-checks-r2.log` | [查看](command-output/full-ui-implementation/csp-checks-r2.txt) |
| full-ui-implementation | `editor-build-reviewed-r2.log` | [查看](command-output/full-ui-implementation/editor-build-reviewed-r2.txt) |
| full-ui-implementation | `editor-build-r2.log` | [查看](command-output/full-ui-implementation/editor-build-r2.txt) |
| full-ui-implementation | `editor-registration-r2.log` | [查看](command-output/full-ui-implementation/editor-registration-r2.txt) |
| full-ui-implementation | `service-build-r2.log` | [查看](command-output/full-ui-implementation/service-build-r2.txt) |
| full-ui-implementation | `service-up-r2.log` | [查看](command-output/full-ui-implementation/service-up-r2.txt) |
| full-ui-implementation | `desktop-launch-r2.log` | [查看](command-output/full-ui-implementation/desktop-launch-r2.txt) |
| full-ui-implementation | `service-stop-r1.log` | [查看](command-output/full-ui-implementation/service-stop-r1.txt) |
| full-ui-implementation | `upstream-source-check.log` | [查看](command-output/full-ui-implementation/upstream-source-check.txt) |
| recovery-execution | `focused-recheck-r7.log` | [查看](command-output/recovery-execution/focused-recheck-r7.txt) |
| recovery-execution | `value-state-recheck-r6.log` | [查看](command-output/recovery-execution/value-state-recheck-r6.txt) |
| recovery-execution | `csp-tests-r7.log` | [查看](command-output/recovery-execution/csp-tests-r7.txt) |
| recovery-execution | `editor-check-r7.log` | [查看](command-output/recovery-execution/editor-check-r7.txt) |
| step2-implementation | `coze-focused-tests.log` | [查看](command-output/step2-implementation/coze-focused-tests.txt) |
| step2-implementation | `contract-breaking-29317b64.log` | [查看](command-output/step2-implementation/contract-breaking-29317b64.txt) |
| step2-implementation | `contract-breaking-32dd7629.log` | [查看](command-output/step2-implementation/contract-breaking-32dd7629.txt) |
| step2-implementation | `contract-breaking-811f38d6.log` | [查看](command-output/step2-implementation/contract-breaking-811f38d6.txt) |
| step2-implementation | `contract-breaking-f16a497e.log` | [查看](command-output/step2-implementation/contract-breaking-f16a497e.txt) |
| light-large-verification | `editor-source-check.log` | [查看](command-output/light-large-verification/editor-source-check.txt) |
| light-large-verification | `runtime-before.log` | [查看](command-output/light-large-verification/runtime-before.txt) |

## 使用限制

- `contract-breaking-32dd7629` 是历史既有不兼容的 FAIL，不能算作全部兼容通过。
- R2 `editor-build-r2` 保留 CSP 待审门禁；后续 `editor-build-reviewed-r2` 才是通过产物。
- 历史观测 JSON 中部分绝对路径用于记录原环境，不是可移植链接；以本包相对路径和摘要定位文件。
- 运行镜像、App、数据卷与保护副本均为本地运行产物，不能随文档提交或从此包宣称已测试还原。
- `cross-repository-files.json` 与本轮检查采用明确的自引用排除项；提交授权后需重新核对清单新鲜度，不能照旧摘要提交后续改动。
