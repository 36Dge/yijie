# FEAT-153 分步执行与决策

日期：2026-09-12。用户明确要求“审计之后开始、务必分步执行”。沿用 schema v3 `demo_fast + local`，按技术依赖推进；不是 G0–G6 或 per-slice G3。

## 顺序与退出条件

| 步骤 | 内容 | 退出条件 | 当前状态 |
|---|---|---|---|
| 0 | 接入前源码、Git、边界、环境及安全审计 | 事实有路径/来源；未知、既有改动、未执行项明确 | 完成，见 03 与 evidence |
| 1 | 本地 Git 元数据、上游锁、12 仓清单及开发治理 | 保留现有文件；源 SHA 可核对；清单/治理/新增检查真实通过 | 完成，见 02 与 step1-verification.json |
| 2 | editor + 固定 local scope 具体设计确认 | 准确 native/CSP/服务身份边界已确认；D0 通过，运行资格尚未声称 | **完成，D0 实跑 PASS**；05/02 为设计与结果 |
| 3 | 契约与 provider | 源契约在先、安全生成、旧路径兼容；真实 Coze adapter 的创建/保存/试运行/内部发布/运行/结果/历史 | 完成：源先行、最小provider/native与定向验证；真实栈在第4步 |
| 4 | Infra 受控本地运行 | 固定版本/独立数据/loopback/ready/正常停止；工作流依赖保持opt-in | 完成：真实HTTP/并发CAS/两库验证与正常重开通过；见07，App资格留第5步 |
| 5 | 真实载体资格 → Desktop 产品接入 | 最小契约/provider/受控栈就绪后，先验证真实 editor 的会话/CSP/返回，再接完整列表/执行/结果；示意卡不冒充服务 | 已授权执行；5.1完成，5.2实施中，见08 |
| 6 | 真实统一验收 | 一次 fresh canonical run 的所有 Must AC、focused checks、结果 Artifact、正常退出/重开 | NOT RUN |

## 已有授权与独立未决项

用户于 2026-09-12 明确授权：先认真审计，再分步做 yijie-coze 仓库接入与工作流基础集成，落成 FEAT-153；上一轮明确排除具体电商服务。此授权覆盖只读审计、需求文档和必要本地仓库接入。用户提供的源 URL 是 `https://github.com/coze-dev/coze-studio`。

仓库首步采用该已验证上游作为 source origin、实际 main 分支；不虚构 36Dge 远端、Owner 批准、发布 tag 或消费者批准。新的易界 GitHub 远端、commit/push、生产发布没有被本次首步执行。既有 11 仓分支/远端保持原值。

用户随后明确回复“批准该方案，继续第 2 步”。该确认已经满足本任务的同窗口、限定本地地址、无 editor native capability、固定 local actor 与短会话方向批准，不再重复索取同一许可。

第 2 步已将实现细化为：固定 `http://127.0.0.1:18888/editor/` 静态 iframe；有限 MessageChannel 业务请求经主 Vue 的具名 Rust workflow command 进入 API；E 和两段服务机密只在 native/server 端；无 WK 第三方 cookie、系统 CA、新 scheme 或任意 native/HTTP 中继。具体命令、CSP、会话时效、资源归属、数据/操作限制见 [05 本地设计](05-local-integration-design.md)。

ADR-0019 已转 Accepted，表示方向与设计基线；未实施服务、未放开运行权限，真实资格仍待第 3/4 步依赖就绪后执行。第 2 步只写文档，不写业务 wire/provider/native 实现，也不推进未授权的 commit/push/发布。

## 冻结的接口与数据边界（具体定义见 05）

- 易界 `Workflow`：稳定 string ID、名称、草稿 revision、内部已发布版本、可执行性；不要把 JS number 用于 Coze int64 ID。
- `WorkflowRun`：workflow ID、固定 version、run ID、原生状态、输入/输出的受控文本、可查询节点结果。状态未知时显示未知，不由前端猜 completed。
- 操作：list/create/read/save（预期 revision）/test-run/publish-internal/run/get-run/list-runs。Coze get_run_history 只按 execute ID 查询，第2步已核实上游trace/list_spans是stub，由Coze新增归属过滤的真实分页查询。
- 已发布版本不可随保存草稿变动；编辑和运行分别授权。publish 必须试运行成功，不开放 Force。
- API 维护资源归属、映射与业务审计；Coze 维护图、版本、执行事实。禁止互读对方私有表或复制第二个执行状态机。
- input≤4 KiB、prefix≤1 KiB、output≤5 KiB、canvas≤256 KiB、port消息≤512 KiB；草稿≤3节点/2边且可不完整，运行/发布要求完整三节点线性图。debug/release 共用1个在途槽位，Coze绑定30秒合作式预算；HTTP超时不制造终态。
- 创建/运行不做无条件自动重试。结果不确定时先查询；明确失败可由用户再次发起。并发保存以 revision 冲突提示处理，不静默覆盖。
- 本地数据只存合成演示内容。草稿/内部版本/历史保留在 FEAT-153 独立 Coze 数据目录或 volume，正常停止保留，删除另行操作；不迁移用户现有 Chat/Host 数据。

## 验证路线与停止条件

先使用原厂 Docker Desktop 正常启动和原厂 bundled Compose，仅启动审查过的独立工作流栈。无需安装替代运行时或触碰其它容器。不得直接执行 `make clean`，不覆盖签名/无关二进制，不以强杀退出。

Contracts 使用已存在 safe 生成入口并逐项审阅依赖；Desktop/Infra 只运行安全 focused checks。普通输入校验错误→修正→重跑、完成后正常 stop/start 是代表性验证；不进行故障或攻击注入。

30 分钟无事实：查日志/真实调用链；90 分钟相同 blocker：简化非核心载体或提出替代；240 分钟仍不能零登录进入/真实执行：暂停扩建，明确一个根因与范围决定；总 16 小时未 D4 重新定范围。不得将权限关闭、mock 或静态卡状态作为替代结果。

## 第3步授权与执行记录

用户继续要求先定义源契约，再实现最小服务端与原生会话桥接。按该授权执行本地候选代码、标准构建与安全定向测试；实现内容与联审见06，最终检查见02。不重复索取已批准的身份/会话方案，不扩到具体ERP、电商/模型服务或提前启动第4/5步。

## 第4步授权与完成

用户明确要求受控local栈与真实数据库验证。按07完成精确构建、两库显式migration、真实ready、普通HTTP/并发CAS/PG事务/MySQL事实、正常停止与新epoch保卷重开；实测发现API回执语义偏差并按源澄清后修复、新流程重验。保留初轮失败和历史合成记录、原六容器及八份Desktop文件。最后专用栈停止，Docker凭据助手残留单独报告；不推进第5步或冒称D4完成。
