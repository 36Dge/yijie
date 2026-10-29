# FEAT-162 — 离线兼容续验复审

2026-10-29，当前主代理复审。本轮只修检查工具、补普通验证和文档，不修改产品wire、权限或持久化；修复自身contract-impact=none，原FEAT-162产品breaking分类不变。无子代理/独立人工批准声明。

## 复审结论

原5项schema EOF全部关闭；9个相关完整基线检查通过，包含先前3个通过项的回归及d5792d6a补充基线。修复没有删掉$ref/schema分支、注入当前schema给旧端或忽略错误。缺源失败关闭、non-ref逐值一致、相对引用身份及`--fail-on ERR`的实际失败样例均有普通测试。自动结果仅代表现有工具覆盖的结构兼容。

| 本轮发现 | 最后处置 |
|---|---|
| 只导出OpenAPI，URI所指JSON Schema未带入基线 | 两侧独立读闭合权威源，不下载URI，9/9通过 |
| 绝对临时ref导致oneOf假差异 | 保留稳定相对/内部ref；恢复全部ref后与原解析对象逐值一致 |
| responses.default与字面default混淆 | 字典键按schema遍历，真正例值保留；专项测试通过 |
| oasdiff输出错误仍可能退出0 | 明确fail-on ERR；普通参数收紧退出1，未弱化级别 |
| 新时序测试首次编译缺路径 | 只修测试限定路径；27项Kimi通过，无生产逻辑改动 |
| 旧全量生成入口仍线上取schema且遗漏当前输出 | 保留FAIL_BASELINE；安全恢复35个原干净生成文件、保全并移除3个本次新产物；原dirty字节保持；不伪报全量生成PASS |

Host对真实正规worker的5项正常生命周期/race通过，含正常EOF与未资格关闭；没有真实Key/供应商/模型。Desktop 44项和亮/暗最小窗口组件证据通过其有界范围；预览不代表App激活、真实审批传输、完整页面或历史重开。

## 剩余风险与未通过门禁

- 旧全量生成入口存在独立基线失败，需要统一各家族生成覆盖及SDK出口；九个breaking绿色不能覆盖它。
- 当前没有新不可变消费者来源、资源级联和准确App回执，Git禁止条款未解除；仍未激活。
- prepare保守截止可能因真实模型/IPC耗时缩短窗口；纯值/race/真实worker空选集不证明实际Pro正常时延。
- native搜索硬费用上界与停止未发送REST许可的完整owner链未资格化；v2 live继续固定拒绝，E1—E7 NOT RUN。
- 完整App、全部亮暗/滚动状态、同构建重开以及禁止型攻击/故障项仍未执行；不伪报通过。

本轮改动范围内未再发现确定缺陷；完整生成/激活/收费/产品D4仍有上述条件，不写成完成验收。AC保持pending、feature active、implementation in_progress。证据和保护断言见[eof-checks](evidence/eof-checks-20261029.json)，范围明细见[26号](26-offline-compatibility-and-zero-cost-followup.md)。
