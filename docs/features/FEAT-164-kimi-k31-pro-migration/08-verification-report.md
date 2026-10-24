# FEAT-164 实际验证记录

## 当前结论

Owner已确认方案并授权实施。G0/G1/G2 pass，G2A及后续Gate/slices pending，整体产品未完成。当前完成的是未激活源契约和独立Runtime候选；Host/Desktop、数据库迁移、实际模型/工具调用、应用切换和三项final E2E均未执行。

## 本次源候选验证

所有结果来自2026-10-24本机实际执行，不继承其它Feature通过。代码版本仍为工作树候选，不能冒充不可变commit。

| 检查 | 真实结果 | 证据 |
|---|---|---|
| 模型v2生成同步、Node契约回归、Rust往返 | PASS；12项Node（含3项保留v1）+2项Rust | [最终回执](evidence/candidate-contract-fixed-results.json)、[日志](evidence/candidate-contract-fixed-01.log) |
| v2 OpenAPI离线bundle Redocly | PASS | [日志](evidence/candidate-contract-fixed-02.log) |
| Contracts `pnpm lint` | PASS；API警告保留，29个JSON Schema、buf、TS、Go静态检查 | [日志](evidence/candidate-contract-fixed-03.log) |
| 新Go包编译和TS类型检查 | PASS；Go无测试文件，只记编译 | [回执](evidence/candidate-contract-fixed-results.json) |
| 独立Runtime来源投影check | PASS；实际binary、manifest、269 schema、patch摘要匹配 | [回执](evidence/candidate-contract-checks.json)、[日志](evidence/candidate-contract-check-02.log) |
| 7个基线离线breaking | PASS；完整比较各baseline已有OpenAPI、Protobuf、AsyncAPI、JSON Schema | [结果](evidence/contracts-breaking-offline-results.json) |
| Runtime canonical构建 | PASS；4项保留SSE、2项sources、3项FEAT-164测试；clippy；release构建；269 schema与保留web-sources候选相同；stdio initialize/initialized及正常EOF退出 | [完整构建日志](evidence/runtime-candidate-build.log) |
| Runtime `make lint`、安全脚本定向测试 | PASS；11项来源兼容、3项正常退出逻辑、2项patch清单 | [回执](evidence/runtime-focused-results.json) |
| Runtime原始上游源码核验 | PASS，canonical subtree保持固定上游原样 | [日志](evidence/runtime-upstream-check.log) |
| 旧input-only/web-sources binary与0001—0006 | PASS，摘要仍匹配保留manifest和HEAD | [保留证据](evidence/runtime-preservation.json) |
| 最终Feature strict、G2、claims | PASS；仅确认当前包与已批准G2，不授予G2A/G2V | [回执](evidence/implementation-governance-fixed-results.json) |
| 工作区与来源保留 | 12仓HEAD保持；9个未修改仓库tracked diff/status相同，8个原产品源码锚点摘要相同 | [工作区](evidence/implementation-workspace-review.json)、[锚点](evidence/preserved-source-anchors.json) |

候选binary SHA-256：`bfb116b7bd79d11ffd593a0bf1b4be681f3081d6705a018a4a69665984e1ebc8`；schema tree：`d8c3265d8923ef4437203c0a2ded954549b4abc0c5079ecd6bcdf7c6da72f11e`。真实来源仍须由后续明确授权的提交固化。

## 失败、修复与未执行项

- 初始严格schema检查发现约束缺少类型/字段声明，已在源修正；原始工具输出保留在会话，未将失败计为通过。
- API原始canonical引用不能由网络取得，离线生成补齐本仓引用及discriminator具名组件；bundle及引用回归通过。
- 二次实现审计发现旧成功回执被投影成v2的风险，已增加原版本SelectionResultSnapshot，直接引用v1/v2权威验证；旧result不加availability、不改schema_version，当前Selection独立查询。
- 补目录一致性时重复加入已存在的activation_required；Rust/Go编译失败已保留在[candidate-contract-checks](evidence/candidate-contract-checks.json)。修复源枚举，并让generator提前拒绝重复值/符号碰撞；重新生成后的最终检查通过，没有手改SDK。
- 原breaking批次有一次baseline拼写错误（exit128）；已按支持清单使用正确完整SHA。另3个baseline因scheduled canonical URL网络解析失败（exit102），原日志和[结果](evidence/contracts-breaking-results.json)保留。独立离线比较的RCA、差异与Owner审查要求见14；不把原入口记成PASS。
- Runtime `make test`在既有`build-input-only.sh`非可执行检查处停止（exit2），该文件HEAD本身为100644，未修改权限。已单独运行安全相关测试和上游核验，不能称全量`make test`通过。见[失败日志](evidence/runtime-fork-tests.log)。
- 新增失败台账时首次文档校验因证据引用不是要求的08锚点而失败；已补真实原失败日志锚点，最终strict/G2/claims通过。原[失败回执](evidence/implementation-governance-results.json)保留，未放宽checker。
- 全量Contracts generate/test未运行：旧生成/测试入口包含本次禁止的攻击fixture路径，且可能重写已有多族工作树生成物。本轮用独立family canonical generate及普通契约测试；完整旧suite覆盖缺口保持，不以限定测试替代全仓通过。
- 日常App/Host/Desktop尚未接入；三表/Host迁移、worker退休准入、计划领域事务、TCONF-164-01—04、G2V和final core/visual/teardown均NOT RUN，不能证明用户端可用。
- 真实模型/业务调用、图片、账户资格、余额及性能质量均NOT RUN，预算为0；长期禁止项未执行。无强杀、权限破坏、攻击载荷、可执行替身或已发布binary覆盖。

## 前轮文档证据（历史）

前轮只做审计落盘时的strict、claims、50项元仓治理测试、文档链接及12仓基线仍保留在evidence；其时“实施未授权/Gate全pending”是历史状态。当前授权以feature.yaml和13为准。文档检查不等于模型、数据或App验收；FEAT-163仍独立FAIL/in_progress。

<a id="E164-RAW-BASELINE-1"></a>
<!-- evidence: E164-RAW-BASELINE-1 -->

原入口失败 1：raw-baseline-35e0949c95d7a59ca5480715c225766dcc822056，2026-10-24T15:37:42.513045+00:00，exit 102 / gate_failure；canonical scheduled schema URL解析失败，未得出本族兼容结论。[原日志](evidence/contracts-breaking-35e0949c.log)。

<a id="E164-RAW-BASELINE-2"></a>
<!-- evidence: E164-RAW-BASELINE-2 -->

原入口失败 2：raw-baseline-54be9314dce5319b049dc0a236800fd1a1fdd7a1，2026-10-24T15:37:44.172197+00:00，exit 102 / gate_failure；canonical scheduled schema URL解析失败，未得出本族兼容结论。[原日志](evidence/contracts-breaking-54be9314.log)。

<a id="E164-RAW-BASELINE-3"></a>
<!-- evidence: E164-RAW-BASELINE-3 -->

原入口失败 3：raw-baseline-bedf4159b0fa22e24efe6c295f8b0d4845df56b7，2026-10-24T15:37:45.649259+00:00，exit 102 / gate_failure；canonical scheduled schema URL解析失败，未得出本族兼容结论。[原日志](evidence/contracts-breaking-bedf4159.log)。

<a id="E164-OFFLINE-RCA"></a>
<!-- evidence: E164-OFFLINE-RCA -->

Owner当前已明确接受候选与离线比较结论；按此授权单次运行bedf4159完整离线基线比较，exit0，原失败不删除。[实际复核日志](evidence/accepted-offline-baseline-recheck.log)。Runtime本地提交57753db451b29a49315ddcb6449ca146171c4de7、Contracts本地提交b0060c8bc4fb924cec14d98b193c32c69482b7b7，双consumer pin已从对应Git对象同步并校验；Go新包仅编译通过，不算行为测试。
