# FEAT-154 当前交付状态与证据入口

> 2026-09-17 · **实现及本地D4验收完成** · `demo_fast / local` · `feature=usable` · 本轮源码和记录未提交；未推送、未发布。

## 当前结论

30个电商节点／634个顶层字段已实现，AC-001–010通过，D4门禁通过。当前候选`586e23d3`在同一次App启动中完成全30节点操作、共用交互及浅/暗色1180×760和1440×900检查。[最终报告与证据](23-final-d4-qualification.md)。

用户已授权临时调整显示缩放；实际使用1800×1169空间取得原生1440×900。结束恢复1512×982默认显示、浅色、1180×780窗口、原名称和已保存原稿。额外原生菜单复验按用户决定跳过；本轮删除/撤销/重做使用正常键盘，取消覆盖目录、历史、恢复和离开。

## 交付边界

- 仅工作流注册、画布卡片、属性表单和页面内交互；299输入、64独立配置、271只读输出，明示子项另行映射。634不代表每个字段都人工填写。
- 不实现节点API或业务处理；试运行可点击、仅提示，无模拟结果。配置限当前页面，关闭App不保证保留。
- 用户另提的拖入、按钮底色、30独立图标和字体适配已完成，单独记在[独立调整](../../dev/workflow-node-panel-adjustments-2026-09-17/README.md)，不加入本需求或AC。
- 本轮最终验收`contract-impact=none`；第2步dirty语义扩大的历史`semantic`记录保留，公共契约消费者仍固定既有Contracts提交。

## 当前候选与检查

| 项目 | 当前事实 |
|---|---|
| manifest | `586e23d360480e758921366a318d980f01d06aa3d4f917366cbc1af7a5d145e2` |
| source digest | `c226f744f587b85f01b31362416d2b946a7c9bf17c86e54a3b7944d75ee03392` |
| Coze基础HEAD | `6d5b309519c2c027fee4a37a107f15c56d554645`，含已登记未提交修改 |
| epoch | `9bb04654-0186-44ba-9467-165fd035bfba` |
| 启动与来源 | canonical构建/CSP/登记/启动通过，六主服务健康；原生App PID36779 |
| 源码检查 | 30节点634字段及明示子项核对，54项聚焦检查通过；类型新增0，继承126 |
| 数据 | 本轮非审计事实全部相等；试运行窄区间全部事实连同审计完全相等 |
| 门禁 | 严格文档、完成声明审计、D4均PASS；元仓lint及50项测试PASS |

[来源候选](../../dev/workflow-node-panel-adjustments-2026-09-17/evidence/mouse-candidate.json)、[当前运行](evidence/final-d4-20260917/runtime-final.json)、[数据比较](evidence/final-d4-20260917/persistence-comparison.json)、[最终完整性](evidence/final-d4-20260917/final-checks.json)。

## 真实截图与历史记录

本轮12张原生JPEG完成原字节导出和SHA256登记，浅/暗两个尺寸均有实拍；加21/22的9张，FEAT-154累计21张。四项独立调整的8张另行保存。[本轮截图清单](evidence/final-d4-20260917/screenshot-ledger.json)。历史不能导出的轮次仍保留0张及限制，不用新截图冒充旧候选。

| 轮次 | 事实与入口 |
|---|---|
| D0 | [Owner确认](evidence/step1-design-20260915/d0-owner-confirmation.json)、[D0门禁](evidence/step1-design-20260915/d0-gate.json) |
| 样板与恢复 | [13](13-recovery-and-sample-verification.md)；旧失败、退出记录及只读保护副本均保留 |
| 全30节点R2 | [14](14-full-node-ui-implementation.md)；旧候选逐项结果不替代23 |
| 目录键盘修复 | [15](15-ac009-keyboard-and-window-verification.md)；当时大窗口/暗色未执行 |
| 证据包及逐仓提交 | [证据包](evidence/delivery-package/README.md)、[17提交计划](17-cross-repository-commit-plan.md)、[18实际提交](18-local-commit-baseline.md) |
| 已提交版本激活 | [19](19-committed-candidate-regression.md) |
| 搜索修复及全30复验 | [20](20-d4-current-environment.md)，Coze搜索修复已提交6d5b3095 |
| 来源对齐 | [21](21-editor-source-alignment.md)，2张真实截图 |
| 暗色最小窗口/图标修复 | [22](22-dark-appearance-verification.md)，7张真实截图；当时大尺寸仍未执行 |
| 当前最终D4 | [23](23-final-d4-qualification.md)，12张新截图；本地纯UI范围完成 |

## 提交与后续

7仓HEAD保持，Contracts源仍为`db4458fe94572c4df41a114005d54a049bb79b1f`，API/Coze/Desktop固定消费；15个受保护主题文件和4份原始资料字节不变。历史FEAT-153主题及Contracts归属见18。

当前剩余交付操作是审阅并提交本轮Coze改动与元仓记录；已有前序未提交改动保留。四项独立调整和前序FEAT-154图标/CSP改动含同文件增量，应按归属拆分审阅。本轮没有获得新的提交/推送指令，因此未执行。业务接口或节点处理不属于FEAT-154后续欠项。
