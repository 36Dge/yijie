# FEAT-164 S4 草案不确定状态与安全处置

本轮依据32与最新用户“审计后继续下一步”推进。先保留496项原工作区文件、旧证据/账本、日常库和旧App；独立s4g干净Desktop资格树，不混入原工作区Native v5等其它需求修改。Runtime a28130a、Contracts1b357cc、Host7927ee7保持。

本轮contract-impact=semantic，实施前先记录Desktop权威说明`docs/feat164-draft-submission-status.md`。修复原queued投影对已尝试、停止且未确认绑定草案的误导；复用已有uncertain而非新增终态，不修改原SQL、原attempt事实或请求。旧failed草案仍禁止重置和自动补发，404不是never-sent证明。

预算维持30元/2次真实HTTP已用，14.188544元预占及14.328134元累计上界不变；本轮新增真实模型HTTP许可0。只本地提交、不推送。先安全结构化回归，再canonical同源App读取原失败记录，真实缺口按实际记录，完整S4/G2V/G3/final继续未通过。

## 实现与分离审计

Desktop仅本地提交`181885b1bfe825bb0e713757e95282e36267aa11`，10个专属文件；原工作区只应用本轮patch，暂存树等于干净资格树，逆向比对保留原Desktop改动。Native reader对匹配scope/会话/turn/operation/version、create_attempted且create outbox failed、无Host/Runtime绑定的queued草案投影为已有uncertain。没有SQL更新、migration、新字段/command或重发逻辑；无证明、正常pending、已绑定及终态不按此规则改写。Renderer用同一source/thread/turn原生状态显示说明，并阻止在该未确认草案内新增提交。

复核真实路径：ChatRepository::local_submissions → 既有NativeHistory → composeConversationView → ChatTurnGroup/useScheduledDraft。仅改变读取解释，原派发器、continue/recovery核权、模型冻结及attempt单调性保持；404不能成为never-sent证明。公共wire保持，私有状态既有enum由v1-v4 reader支持，回滚可读原SQL但会恢复旧误导文案；不以回滚放行发送。没有把Code Review说成独立人工批准。

## 本轮实测

- 原生2项状态回归通过：正常accept/claim/attempt/fail接口形成的结构化状态，重复读取零SQL变化、原行queued保留、缺mapping继续拒绝、无法重新claim、scope/turn匹配；正常可信mapping恢复后queued投影恢复。未尝试的本地失败不凭空生成attempt事实。
- 前轮生产writer→format4草案preview回归1项通过；fmt、候选lib Clippy通过。32项前端回归通过，包含真实Panel的恢复确认取消、只读刷新零写命令及来源隔离；lint、前端build及docs build通过。完整Rust/前端套件不冒称全绿，含历史故障/攻击测试的全入口未运行。
- canonical ordinary构建通过。首次UI选择早于launcher预检完成，getApp有自动启动语义，曾显示仅设置的导航；该观察保留`s4g-settings-only.*`，正常⌘Q退出，没有修改产品来掩盖问题。第二次先确认canonical子进程86027的完整可执行路径后绑定UI，同一构建直接进入正常免登录聊天。后续须等canonical实际exec，再用getApp；不把UI工具自身打开当作canonical启动。
- 从真实保留历史选择原失败会话`01a17315-c3f9-7e93-a6f8-56a7b7876520`，看到“提交结果待确认”和明确勿重复提交说明，发送与模型选择保持禁用。刷新、取消恢复确认及一次明确“检查并继续”后均未发送模型请求；仍保留待确认状态，不冒称远端请求已取消或恢复成功。
- 原已完成草案`01a17323-8807-7680-b4bc-672d4283a226`仍显示已完成，既有计划已暂停；没有新建计划、授权或手动执行。实际1180×760窗口（2360×1520截图）下亮暗提示及按钮无重叠；沿用用户已有外观授权临时切换深色，已恢复原浅色。没有调整其它系统设置。
- 使用既有S4f安全本机fixture，只观察读取路径，最终attempts0/requests0/rejected0/external0，stopped_normally。App均正常退出0，18083/18086释放。cleanup检查器最初误期望state=stopped，读取fixture源后纠正为实际stopped_normally，不改产品生命周期。
- 正常关闭后对新副本immutable只读核验：原失败草案元数据完全一致，已完成草案6条事实hash全同；不改SQL/rollout，不输出密钥或其它聊天正文。预算/旧账本不动。见`s4g-data-audit.json`、`s4g-ui-results.json`及`s4g-cleanup.json`。

## 未通过的通用检查与后续顺序

`pnpm generate:check`连续三次FAIL后停止；前两项是新资格目录缺Host/Skills精确checkout，第三项暴露了其它需求dirty Connectors revision11和通用revision9断言/旧e279锁不匹配。完整RCA见[evidence/s4g-generate-rca.md](evidence/s4g-generate-rca.md)。未修改旧锁、生成物或断言；只把新树Connectors引用纠正到已有干净1f15726。FEAT164的canonical专用验证和构建是本轮原计划的独立检查，不替代通用检查、不把该熔断写resolved。通用入口第四次未运行；G3仍阻断。

本轮完成“旧attempted失败草案状态可见、保留并安全拒绝重发”子集，并非完整恢复/取消功能。对于当前缺失可信mapping的旧请求，最佳安全处置是保留可读历史和待确认状态，不能reset、删除证据或以新请求绕开。后续先审阅通用生成入口RCA并明确与Feature锁的验证分界，再补旧模型计划退役/重新选择与授权、完整恢复取消UI和当前专家/媒体同源App组合。其它平台、当前真实G2V、完整TCONF、G3/freshness和最终E2E仍未完成，新增真实HTTP许可继续0。

治理文档初检两项自身问题保留：新增证据先只有Markdown标题、缺canonical evidence marker，已补唯一marker；strict把真实产品标签中的“待确认”识别成文档占位符。核心机器检查文档改用等价明确uncertain术语，真实UI原文/截图及本报告保留，所有未完成范围和G3阻断不变；不通过删除未完成项制造通过。初始日志见s4g-claims-initial.log和s4g-strict-initial.log。

## 收尾核验

claims/strict、元仓lint、53/53治理测试、7个shell语法检查通过；G3实际返回阻断，含本轮open generic-check breaker及原TCONF/freshness等缺口。保留性审计通过496项原改动、989份旧证据、154资源、7日常库文件、203旧App文件和5522候选事前副本。当前canonical源/Bundle吻合，Host/Runtime/Manifest摘要与上轮相同。结果见[s4g-verdict](evidence/s4g-verdict.json)、[保留审计](evidence/s4g-preservation-audit.json)及[治理结果](evidence/s4g-governance-results.json)。元仓提交以包含本报告的Git记录为准，仅本地、不推送。

提交审核保留原始日志及patch的空白：全量diff --check只指出Vite输出末尾空格、原生/前端日志末尾空行以及patch空上下文行；实际代码及治理文档的空白检查通过。未为消除诊断改写原始证据。长期记忆暂存仅替换确切FEAT164原段落，未假设HEAD含未提交的FEAT163标题。
