# FEAT-154 当前交付状态与证据入口

> 2026-09-16 · **实现完成，验收未全部完成** · `demo_fast / local` · 本地源码提交完成；未推送、未发布。

## 0. 本地提交已执行

用户已授权并继续执行逐仓本地提交。Contracts源为 `db4458fe94572c4df41a114005d54a049bb79b1f`，API、Coze、Desktop已同步固定；FEAT-153主题和实现仓分别提交。各仓完整SHA、实际检查及元仓自身提交解析方式见[18 本地提交基线](18-local-commit-baseline.md)。

现有App/编辑器保留此前验收构建，本轮未重新构建或激活。下文候选表及各轮通过项描述的是该历史运行产物；当前源码身份以18为准，不能互相替代。

## 1. 交付结果与边界

30 个电商节点已在原生 Coze 工作流目录注册，并具备画布卡片、属性表单和页面内交互。覆盖 634 个顶层字段（299 输入、64 独立配置、271 只读输出），明示嵌套内容另行映射；634 不代表每个字段都人工填写，也不代表原文未定义的内层 Schema 已补全。

整个需求不实现节点接口调用或业务处理。试运行入口保持可点击，仅显示前端未接入提示，不发送请求或生成模拟结果。配置只在页面内保留，页面离开确认；用户已选择关闭 App／刷新不保证保留。详见 [需求边界](00-feature-brief.md)和[原始资料](sources/README.md)。

证据准备阶段仅归档证据、整理跨仓归属及准备提交，`contract-impact=none`。第2步扩大既有 dirty 页面保护含义的 `semantic` 历史仍保留，不能以本次文档工作覆盖它。

## 2. 此前验收候选（现存构建，本轮未重新激活）

| 项目 | 当前记录 |
|---|---|
| 编辑器 manifest SHA-256 | `f608fde5478d47d3db3ee75ea4e14a012025a9436af21e1043439b09d5e43526` |
| Coze 源码摘要 | `e4d15b39758eea4eecafc3d5008dfb88795765abcf37e44c23ef12b504452350` |
| Coze 基础 HEAD | `10faf164d7af194b7697a93cb3c4a6886ddc64b5`，含当时清单所列未提交增量及 FEAT-153 主题 |
| 最后验收激活 epoch | `8d5a65b9-8656-430d-9554-e6ffd490f253` |
| 编辑器产物 | 385 项，45,568,238 字节 |
| Desktop 可执行文件 SHA-256 | `f5d6966a5f7613d07fddb4aae7e3c728c9e5a8cf21c512980186492434643686`；本次只读重算一致 |
| Contracts | `1.4.0-local-candidate`；API／Coze／Desktop 同源本地消费，表中为历史构建的旧锁；当前源码已固定新提交，见18 |
| 原稿与运行状态 | 上轮已恢复原 Start/Text/End、两条连线、原名称和“已保存”；六项主服务当时健康。本次不启停或重做 UI／健康验收 |

全部源锁、消费者锁及 binary 路径见[机器可读候选](evidence/delivery-package/candidate.json)，原始激活记录见[AC-009 final](evidence/ac009-verification/activated-runtime-final.json)。这固定的是此前**本地运行候选身份**。当前源码已在18所列提交固定，三份消费者锁已变化；本轮没有产生新manifest，仍需未来标准构建重新建立运行产物关联。

## 3. 分轮验收及可信范围

| 轮次 | 已取得的证据 | 结论边界与入口 |
|---|---|---|
| D0 接入定稿 | Owner 明确确认；机器 D0 PASS | [Owner 确认](evidence/step1-design-20260915/d0-owner-confirmation.json)、[D0 门禁](evidence/step1-design-20260915/d0-gate.json)；预览是静态设计示意 |
| Contracts／样板 R7 | 权威源先行、三消费者同步；01/10/17 共57字段及共用生命周期 | [契约检查](evidence/step2-implementation/contract-source-consumer-checks.json)、[样板结果](13-recovery-and-sample-verification.md)；旧 `32dd7629…` 基线已有 request_history 不兼容，未假报通过 |
| 环境恢复 | 显式恢复阶段、停止数据副本、私有只读状态核对、正常退出 | [首次恢复](evidence/recovery-execution/recovery-result.json)、[全量前恢复](evidence/full-ui-implementation/recovery-result.json)；不是数据副本还原演练，未解释的历史退出原因保留 |
| 全量 R2：`a9317ebc…` | 同一候选逐个添加30节点、打开侧栏、填写代表字段；同类隔离、手动拖入、撤销、重连、离开取消、原稿恢复 | [逐节点矩阵](evidence/full-ui-implementation/ui-r2-node-matrix.json)、[交互记录](evidence/full-ui-implementation/ui-r2-shared-observations.json)、[持久数据比较](evidence/full-ui-implementation/ui-r2-persistence-comparison.json)、[R2报告](14-full-node-ui-implementation.md) |
| AC-009 final：`f608fde5…` | 修复目录焦点裁切、Esc 退出、重复 Tab 停靠；30目录键盘顺序、05复杂表单、24长标题、试运行与恢复回归；浅色1180×760通过 | [操作与原生尺寸](evidence/ac009-verification/final-ui-observations.json)、[持久数据比较](evidence/ac009-verification/persistence-comparison.json)、[报告](15-ac009-keyboard-and-window-verification.md)；没有在此候选重跑全量 Must |
| 大窗口预检 | 来源核对、显示条件及用户决定 | [不允许调整显示](evidence/light-large-verification/owner-display-change-decision.json)；1440×900未执行，不用1512×875替代 |

当前沿用 AC-001–008、AC-010 的历史通过记录；最新候选的定向回归有单独记录。完整 D4 需要同一最终候选的一次 fresh run 覆盖全部 Must，不能拼接历史轮次宣称通过。

| 剩余验收 | 当前状态 | 后续条件 |
|---|---|---|
| 浅色1440×900 | NOT RUN | 需可提供目标逻辑尺寸的允许环境；用户已拒绝调整当前系统显示，不重复请求或擅改 |
| 暗色1180×760、1440×900 | NOT RUN | 用户明确延期；等待后续安排，保持现有外观 |
| 历史真实截图的离线复核 | 缺口已登记 | 没有可导出的本地文件；后续获准实际验收时保留可导出的原始截图 |
| AC-009／完整 D4 | pending／NOT RUN | 上述条件齐备后再安排完整真实验收；未删除 AC、未取得验收豁免 |

## 4. 可交付证据包

[证据包 README](evidence/delivery-package/README.md)是日志、摘要及检查入口。

- 从71份原始日志选择33份必要完整输出，保存为可跟踪 `.txt`；178处开发机路径替换，原件不变。逐份原文/归档 SHA-256、字节数、替换次数和另外38份本地中间日志的保留原因见[归档清单](evidence/delivery-package/log-archive-manifest.json)。历史失败和CSP待审门禁也保留。
- 当前人类可读报告及 `feature.yaml` 的选中日志引用已改到归档副本。历史 JSON 内原日志路径保持其原始记录身份，由归档清单映射，不当作可点击交付链接。
- 可导出的 FEAT-154 真实 App 截图 **0 张**；现存3张仅为 D0 静态示意。[截图登记](evidence/delivery-package/screenshot-ledger.json)逐轮列明缺口及影响：审阅者可核对操作记录、原生尺寸与数据比较，但不能仅靠本包重新判断历史视觉效果。未生成替代图片或冒称已导出。
- [检查结果](evidence/delivery-package/package-checks.json)记录提交准备阶段的文档、归档、链接、来源及保护检查；本轮提交检查见[收口检查](evidence/local-commits/meta-final-checks.json)。文档检查不是新的产品验收。

## 5. 跨仓交付与下一动作

[原逐仓提交计划](17-cross-repository-commit-plan.md)列明文件归属、生成来源、FEAT-153主题依赖、顺序和验证说明；[精确逐文件清单](evidence/delivery-package/cross-repository-files.json)包含完整路径、Git状态和工作树 SHA-256。

本地提交已按用户授权执行，实际结果见18。系统外观、显示设置、运行数据和15个主题保护文件字节保持；未推送、创建分支或更改远端。下一阶段如需运行新提交基线，应标准构建、登记、激活及对应复验；AC-009与D4继续保持未完成。
