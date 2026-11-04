# FEAT-167 复审修复

用户已授权按复审报告完成 P1、活动行投影、命令安全预览、工具标题与分组交互，逐项验证 v2 A01–A26。保护现有 format6 会话，不清库、不重放；不包含 diff。原 08 报告仅保留前轮实际验证范围，不作为本次修复已完成的证明。

`contract-impact = semantic`：修正原生内容可用性与实时资格的解释，以及安全展示标签和阅读投影；不新增公共 wire 字段、不改变 Native6/SSE13/format6/IPC6 的形状或必填项。原生执行状态、原始 phase、身份、事件顺序、审批和终态不改。继续精确消费 Contracts `dfd9012954c716d360f702d6be3bdbdef75e0633`；契约原已定义 availability 独立于执行结果、Security projection label、原始动作 index、toolDisplay 三种 provenance。受影响 producer 为 Host，consumers 为 Desktop Native/Vue，Owner 为段成威。

采用现有 `commandLabel` 与 `commandActions[].label` 承载受限安全预览；预览不是原始命令、没有执行权限、不能回传执行。read/list/search 使用 Runtime 结构化目标，不在前端或 Host 重新解析 shell 推断动作。unknown 动作可使用其原生 command 的安全展示预览。工具标题仅来自 canonical appContext、已知受信注册描述或明确允许工具的 title；不泛化 raw 参数输出。新增 ActivityEntry 只在前端进程内派生，不是 wire DTO 或执行事件。

数据与兼容：不迁移、不修改数据库 schema；新 reader 读取现有 format6 缺少丰富标签的记录，使用诚实兜底，不编造历史未保存的信息。已保存 command_output_pending_final 仅在阅读时作为非阻断策略提示解释，不重写原事实；真实 stream_gap 等仍限制实时资格。所有状态读取保留 context/session/revision 约束。V4/SSE11 维持退役。

实施顺序：先 P1 与正常序列回归；再 Host 标签/路径与 consumer conformance；再纯活动行、分组状态和组件；最后全量安全检查、现有会话正常重开与界面复验。现有工作树基线见 `evidence/repair-baseline.json`。

未知 phase 规则：最后一条可读未知阶段回答在运行中和终态都保留；仅在存在后续可读回答且观察到工具继续时，把前一条消息纳入过程。显式 commentary/final_answer 原样保留；末尾可读 commentary 单独标记为阅读候选并保持可见，不升级为 final_answer。失败、待审批外显及会话挂载期内的展开选择仍是易界产品策略。

只采用正常、非破坏性测试；无强杀、权限故障、二进制替换和攻击 fixture。此前两模型共四轮额度已耗尽，不追加真实模型调用。界面使用既有会话及正常组件样例，真实服务历史读取不等同于新模型执行。原 production_hardened 门禁状态不降级、不冒充签名发布或独立人工评审；修复结果另记逐项证据。

独立复核补充：已结束单条活动减少一层分组；单条命令从无动作补齐单个动作时保持行身份；耗时元数据刷新保留行锚点但显示“耗时待确认”，不把临时耗时当最终值。最终证据见 10 号交付报告。
