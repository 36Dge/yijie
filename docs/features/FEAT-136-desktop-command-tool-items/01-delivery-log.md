# FEAT-136 原生 Command 调整交付记录

## 阶段与来源

2026-09-09：先完成源码审计并交付 03-native-command-audit-and-plan-2026-09-09.md；用户随后“授权执行”。原四文件已从元仓 7ddf9e64a56df2af4aa4f6906408b0d1a85a48df 逐字节归档，当前包新增八项原生 AC，未继承旧 D4。

开始实施时 Desktop 为 6e5047d1c23041c46dd495ddb89e24c7e4db5d47 且 clean；元仓已有上一轮明确的文档修改，全部保留。Contracts db7a607c1c091fc4f4243829d68d5b673eb7e2c3、Host f4cf01bd6f7e9f37792ef743d44f0ce10527c10b、Codex 6c1ad767f0997845b8258a1c452fd4eb7577579f 未修改。FEAT-134 四个固定提交另已授权普通推送并核对远端 SHA，未混入本轮新修改。

## 已实施

- ConversationCommandExecution 区分旧只读投影与原生对象引用；删除 native Command 的伪 startedSource/lastSource、redacted cwd 和 complete/upstream_truncated output 适配。
- ChatCommandItem 使用现有 native 安全标签、输出、status、exit/duration；0ms/exit 0/空字符串保留，失败/拒绝只映射显式 status 的产品文案。
- 复用既有 busy/activityLabel 区分历史与活跃接收；不回写 Item，未观察到结束时不继续说“正在执行/等待输出”。
- Item partial 文案改为“此项信息不完整”，不暗示一定是正文被截断；pending-final 会话诊断改为历史观察说明。
- 新增 18 项 native view → selector → 真实 Command 卡片定向回归；旧测试只调整明确的 legacy 类型名称和新的准确文案。
- 复用原 SQLCipher reopen/cold conflict 测试，增加真实格式的 Command 安全事实，验证 ID/来源/输出/exit/duration/availability 正常保存及重开。
- 正常入口暴露既有 200% 页面右侧裁切；原外壳只消费缩放高度，宽度仍为 100%。最小修复为消费已经存在的 --yj-ui-viewport-width；不改变缩放机制或权限。

## 删除与保留

删除的是 native Command 中无事实依据的旧 DTO 填充逻辑，未新增 reducer/累积器。旧 v4/v5 IPC、DTO、表与 reader、Host v5 路由/安全 helper/容量计数、Artifact v3 通道都有真实依赖，保留并记录兼容职责。未修改 Host、Runtime、FEAT-137 退役或 FEAT-152 权限逻辑。Tool 仍由 FEAT-144 另行决定，不扩大实现。

## 验证过程与未通过记录

- 首轮新增组件测试 4 处失败：3 处在默认折叠时查询 body 内 aria-live，1 处 axe 未附着文档。修正测试观察时机和 DOM 生命周期后，4 文件 55/55 通过；没有修改产品来迎合错误测试。
- 11 文件前端定向回归 251/251 通过；make lint（含 source generation、ESLint/TypeScript、fmt、clippy all-targets）通过。
- 扩展的 SQLCipher 正常 reopen/cold conflict 测试 1/1 通过；没有破坏权限/DB/进程或攻击 fixture。
- ordinary canonical 构建启动、既有历史/Artifact/附件/权限入口和正常退出已执行；首次正常退出后 8 条 Host 映射及原生终态与实施前逐项相等。
- 200% 首次截图右侧裁切，未记为 PASS；修复后的实际复查结果另记验收文件。
- 当前已检查的普通历史没有可复用的原生 Command 成功/失败样本。已另行申请本次最多 5 次文本请求；收到前不调用模型，不转用任何旧额度。

本地 content-free 日志位于工作区 .local/feat136-native-adjustment-20260909；不保存用户数据库、凭据或完整对话正文。最终验证、调用及提交状态以 02-verification.md 为准。

## 最终真实验收与收尾

用户追加本次独立上限 10 次文本请求后，复用现有固定路由计量器、保持请求批准，仅提交一次验证意图。3 次 API 请求得到两条独立 Command：completed/exit 0 与 failed/exit 128，duration 均 0ms，安全字段/复制/错误说明符合预期。正常退出重启后同一两条记录完整保留；原 8 条 Host 映射不变，仅新增本次验证映射，最终 9 条均 idle。

200% 修复还需 Chat Grid 使用 minmax(0, 1fr)，最终真实页面右侧不再裁切，标题省略、输入/发送控件可见、Command 字段与错误可滚动阅读。已经恢复 100%。五次应用退出和计量器结束均走正常路径，无新请求或强杀。

本次八项 AC/local D4 PASS。验收时工作区候选的逐文件 SHA-256、运行结果及3/10调用台账完整保留；用户授权本次提交与推送后，Desktop 已固定为 8bfa5ca284fddb86d7cdd2a406c5041c49367688。元仓及远端状态见 04-delivery-closure-2026-09-09.md。原范围、失败过程及历史验收完整保留。本地提交与远端交付收尾于 2026-09-10（Asia/Shanghai）完成：Desktop 8bfa5ca284fddb86d7cdd2a406c5041c49367688 → 元仓 4e6645574fdfe7d29f7c551564bf807cf8222d48 两次普通推送及远端 SHA 核验通过，两个精确提交的 CI 均 NOT RUN。详见 04-delivery-closure-2026-09-09.md；当前补记仅保存已发生的回执。
