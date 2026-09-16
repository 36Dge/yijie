# FEAT-154 本地提交与交付基线

> 2026-09-16 · 已按用户授权执行本地提交；实现完成，验收未全部完成。统一入口见[16](16-delivery-status-and-evidence.md)。

## 1. 实际提交

| 实际顺序 | 仓库/单元 | 完整提交 SHA | 内容 |
|---|---|---|---|
| 1 | yijie-coze / T0 | `cdbc822c8de3207c9e261649e52aa6323eae1ca1` | style(feat-153): preserve workflow canvas and lime theme |
| 2 | yijie / T1 | `8b03461d563cf07566676ca20ca5ce504ff0da9e` | docs(feat-153): record preserved workflow theme |
| 3 | yijie-contracts / C1 | `db4458fe94572c4df41a114005d54a049bb79b1f` | feat(feat-154): clarify page-local dirty bridge semantics |
| 4 | yijie-api / A1 | `041f40c69919e81ec72ccee4ea6dbb3ea012142d` | feat(feat-154): pin workflow contract and add recovery reads |
| 5 | yijie-coze / Z1 | `144e4c259a5460fed57fc280f2439cbbf9a18539` | feat(feat-154): register 30 ecommerce nodes for UI design |
| 6 | yijie-desktop / D1 | `4a8a67bec4903624ca98a1098572fa26f3a20849` | feat(feat-154): clarify page-local design leave protection |
| 7 | yijie-infra / I1 | `66b481552eb76d46b00875ac27794ed8e1eb504a` | feat(feat-154): add explicit local workflow recovery |
| 8 | yijie / M1 | 包含本文的元仓提交，由下述命令解析 | 完整需求、来源、分轮验收、日志归档及本地提交记录 |

元仓自身SHA不能写入同一提交的正文而仍保持该SHA。使用以下只读命令取得本文对应的完整提交：

```sh
git log -1 --format=%H -- docs/features/FEAT-154-ecommerce-node-ui/evidence/local-commits/commit-baseline.json
```

[机器可读基线](evidence/local-commits/commit-baseline.json)保存各仓完整SHA、分支、远端、契约锁、运行产物身份及逐单元收据。Coze主题与元仓主题记录先分别提交，再提交Contracts源、API、Coze、Desktop和Infra；没有切换分支、改远端、推送或发布。

## 2. 来源与运行产物分别记录

Contracts权威源为 `db4458fe94572c4df41a114005d54a049bb79b1f`。三个消费者均由canonical同步脚本使用完整SHA固定，并通过`--check`；版本仍为`1.4.0-local-candidate`、`release=false`，提交不等于supported/tag发布。同步只改变三份consumer lock，不改变生成DTO或validator。

本轮还修正Coze一个原未跟踪文件的末尾多余空行：`reference-picker.tsx`仅删除最后一个LF。初次暂存检查失败记录保留；修正后staged diff检查通过，代码行为不变。详见[格式修正](evidence/local-commits/format-only-correction.json)。

现存编辑器manifest仍为`f608fde5478d47d3db3ee75ea4e14a012025a9436af21e1043439b09d5e43526`，Desktop binary仍为`f5d6966a5f7613d07fddb4aae7e3c728c9e5a8cf21c512980186492434643686`，只读校验与此前相同。本轮没有重建、登记、激活或重做真实App验收，也没有重查运行健康；历史运行epoch和原稿恢复记录保留。

**新源码基线与此前验收构建的来源不同。** 三份pin及格式修正已改变源码身份；未来需要交付新App候选时，须按canonical正常停止、构建、登记、启动与对应复验流程建立新manifest/epoch。不能把旧f608构建冒充新提交的fresh资格。

## 3. 实际检查

| 检查 | 结果 | 证据 |
|---|---|---|
| Contracts生成一致性、16项测试、lint | PASS；12条既有unused警告保留 | [生成](evidence/local-commits/contracts-generation-check.json)、[测试](evidence/local-commits/contracts-focused.json)、[lint](evidence/local-commits/contracts-lint.json) |
| 相对实施前HEAD的结构检查 | PASS；旧32dd历史不兼容结论不变，未冒称全支持发布兼容 | [增量breaking](evidence/local-commits/contracts-incremental-breaking.json) |
| API/Coze/Desktop固定源及同步 | PASS；仅三份lock改变 | [同步审阅](evidence/local-commits/consumer-pin-review.json) |
| Coze 43项聚焦、3项既有CSP产物检查、源文件保护 | PASS；不是新产物构建或真实UI | [聚焦](evidence/local-commits/coze-focused.json)、[CSP](evidence/local-commits/coze-existing-csp-bytes.json)、[源码](evidence/local-commits/coze-source-preservation.json) |
| Desktop 4文件23项测试、lint/typecheck | PASS | [测试](evidence/local-commits/desktop-focused.json)、[lint](evidence/local-commits/desktop-lint.json) |
| 私有恢复9项、既有生命周期13项 | PASS；未启动Docker或操作数据库 | [恢复](evidence/local-commits/pinned-consumer-recovery-focused.json)、[生命周期](evidence/local-commits/infra-lifecycle-focused.json) |
| 元仓文档/资料/链接/保护文件及提交范围 | 见本轮实际输出 | [收口检查](evidence/local-commits/meta-final-checks.json) |

全仓历史攻击fixture、权限故障、强杀和二进制伪装测试未执行，仍属用户禁止项目；使用已审阅的正常聚焦入口。Git提交沿用现有本机身份配置，未修改全局设置；命令归档隐去本机Git身份行。

原始`1-8.md`和5份完整构建/启动日志带有原文空格。为了保持来源快照和归档摘要，不格式化这些证据。元仓`git diff --cached --check`的原始警告、逐路径限定及摘要核对单独记录；不关闭检查、不改全仓忽略或whitespace规则，也不把保留原文警告写成零警告。

## 4. 完成边界与下一步

本轮完成逐仓本地提交及来源固定。保持30节点纯UI范围，试运行可点击且只提示；无接口调用和节点业务处理增量。

AC-009仍pending：浅色1440×900未执行，暗色按用户决定延期；历史真实截图导出缺口仍保留。完整D4为NOT RUN。下一阶段若要让App运行本轮提交基线，应另安排标准构建激活和允许环境内的回归，不能因Git工作完成而关闭D4。
