# 两组工具接入执行记录（2026-11-08，进行中）

用户已明确恢复任务。当前范围仅 request_user_input、get_context_remaining/new_context；策略 A 保持，不扩展其它工具。历史 05 暂停已被恢复指令覆盖。接入、定向验证、Kimi 实测及原开发入口加载已完成；验证边界见末尾，不冒称全量回归或完整原生 GUI E2E。

## 实现

- Runtime 0022 补齐原生 options 可选/isSecret、Default 开关、root-only 声明，仍用原生等待和响应；敏感回答只清除诊断预览，原生模型输入与 rollout 保留事实不变。
- 原生 reset_on_compact 默认 true 保留原默认；易界配对 profile 设 false，普通自动/手动仍走原摘要。显式 new_context 走原 fresh-window；取消清除延迟标记。收尾审查再补 direct start_task 清理，以覆盖直接输入与 V2 邮箱启动入口；这不另造执行或恢复机制。
- Contracts 新 runtime-interaction-tools / user-input family，精确候选、canonical 类型机械投影、Go/Rust/TS/JSON Schema 同源生成，无旧审批协议改造。
- Host 独立有界临时回调；generation/root/turn/item/RPC/对外 UUID 绑定；操作幂等、原通道写回确认、取消/结束/失联收束、60–240s 可选倒计时与首次交互暂停。回答不进 Host 业务库、SSE 或诊断日志。Snapshot generation 防止旧待答卡在进程更换后留下。
- Desktop 复用 CommandRequest、鉴权、原会话映射、HostBridge；问题卡多题、选项/自由输入、跳过/关闭、遮罩与显隐、敏感草稿清除、结果未知后只读回执不重发。只在配对 local 开发入口启用。
- 不新增上下文预算条、任务记忆或摘要器；原生 contextCompaction 共用事件不能被称为“已摘要”，当前既有未识别展示不据此伪造摘要/恢复状态。原生历史和实际模型输入分别验证。

## 已观察证据（尚需最终 Runtime 候选复核）

首个可运行候选 `5e94cd8efcd223c8c2f5703c977002f179abcdefb5dfba801944e4e4d470516f` 为新增任务入口清理前版本；完整原生构建/schema 已通过，原四组 dfa05c... 制品未改变。0022 最新补充正在重新构建独立制品，旧候选不得冒充最新源。

- Native lib：自由输入/敏感标记、取消、request_user_input 15 项、配置解析/冻结均通过。
- Native policy：普通自动摘要、普通手动摘要、显式 fresh-window 3 项通过；get_context_remaining 数值、unknown、prefix 与 Code Mode 结构化结果 4 项通过。
- Host：4 个真实 Runtime 本地回环测试通过（问答+同候选正常重开、显式新窗口/历史、原四组旧会话升级、实际专家角色/索引+真实 copywriting 技能+input-only）。更新配置读回检查后 4 项再次通过。
- Host race：4 个顶层问答状态测试（含 3 个暂停/超时/跳过子场景）与 1 个 HTTP bearer/同源契约测试通过。
- Desktop：8 项组件/状态测试、类型检查、定向 ESLint 通过；1 项真实 Rust HostBridge loopback/原请求绑定/Debug 脱敏测试通过。
- 浏览器真实组件：CUA 在 1180×760 浅色/深色检查选项、自由输入、多题、遮罩及提交；DOM 核实 frame/viewport 为1180×760，按钮无重叠。它是产品组件的普通本地预览，不冒充完整原生 App E2E；预览已正常停止、临时页关闭、viewport恢复。
- 普通原生中断探针复核：new_context + 问答等待后正常 turn/interrupt，下一轮任务文本在两次请求都保留；3 次本地 HTTP，0 供应商调用。

失败记录如实保留：最初测试构造缺字段；Rust 测试线程栈不足（为测试进程设 RUST_MIN_STACK 后正常）；上下文测试最初误用了 OpenAI 远程压缩 fixture，改用与易界相同的原生本地摘要路径后通过；Vue 测试初始未指定 DOM 环境，补 happy-dom 后通过；config/read 校验最初误认为 ToolsV2 包含 experimental_request_user_input，源码确认只含 web_search，现只读实际公开的 feature/policy 字段，工具 gate 由 canonical 配置 schema 和真实调用证明。

## 当前继续点

1. 完成最新 0022 的 direct start_task 清理测试/独立构建，再重生成 Runtime/public 来源锁与消费者，复跑相关真实回环及配置检查。
2. 完成来源/格式/生成漂移检查，冻结新的 Desktop interaction-tools-build.candidate，保留旧四组入口与制品。
3. 原开发入口启动/就绪与新环境配置验证（尚未启动）。无日常 Home 重置、迁移、备份或强杀；没有 commit/push。
4. 若需要真实供应商验收，只 Kimi K3.1 Pro；本阶段当前授权额度仍为0，实际调用0。必须准备具体短用例后另行申请本阶段额度，不能借旧40次余额。

日志：Runtime `.local/interaction-tools/`，Host `.local/user-input-*.log`，Desktop `.local/user-input-*.log`，Contracts `.local/user-input-*.log`。当前任务仍在执行，未暂停。

## 最终候选与供应商验收

最终 Runtime 来源 `038d498bda0d4cb8899e15ea81dfa777b6928adc0e389aebf5e20b3038332086` 已构建并生成271个 canonical schema；direct start_task 清理测试、3条上下文策略和正常取消探针通过。Contracts/Host/Desktop 已同步精确来源，旧 native-tools 投影检查仍通过。当前 fallback 的全源离线结构兼容检查 exit 0；仅保留前四组已记录的 Native6 两个新枚举警告，本阶段没有再增加展示变体。

用户本阶段新增授权“批准，仅 Kimi 最多8次”。独立受控计数器只允许 kimi-k3.1-pro，总上限8，0图片/其他模型。实际4次HTTP，全部200；request_user_input/get_context_remaining/new_context 各1次，原生turn completed，contextCompaction存在，Host回执不带答案。计数器经stdin EOF正常关闭，MiniMax实际0次。完整记录在 Host `.local/interaction-tools-live/20261108-current-stage/`；剩余4次不自动使用。

原开发入口第一次启动止于Docker未运行；原session/state均stopped，没有active_child/pending_stop/recovery_active。通过正常应用启动恢复原Docker（daemon已就绪），未重建容器/修改数据，随后正在重试同一 `pnpm client:dev`。此前的构建/接口通过不冒充这一步已完成。

## 原开发入口已加载（最终状态）

原Docker正常启动后，canonical workflow-session ensure 复用原容器，完成健康检查。`pnpm client:dev` 从原Homes增量构建并启动，未安装发布包、迁移、重置或拷贝业务库。Native App PID36098、Host PID36309、Runtime PID36314为本次观察值（不是永久身份）。Host `/readyz` HTTP200，`/v1/status` ready=true、kimi-k3.1-pro、stable experimental_api=false。运行中Runtime绝对路径确为最终038d498...来源；实际启动参数确认 default_mode_request_user_input=true、token_budget.enabled=true、reset_on_compact=false、tools.experimental_request_user_input.enabled=true。

启动日志还确认38个技能目录、7个已安装/启用技能，21个专家目录/19个资源就绪及原1个连接器状态就绪；未为本任务改动这些资源。客户端保持打开。

最终检查：新两族生成/同步/check及旧native-tools投影检查通过；fallback c24d73f完整离线结构比较exit0（前四组两个response enum warning原样保留）；4项新契约conformance、Host9项顶层问答/HTTP测试（另3个子场景）、Native上下文策略3项/剩余上下文4项/最终清理3项、Desktop8项UI状态测试/1项Rust Bridge/2项开发入口配置检查通过；受影响Go vet、TS类型、ESLint、Shell与diff空白检查通过。供应商4/8次，仅Kimi，均200；不继续消耗剩余额度。

未执行：全量回归、用户禁止的强杀/权限破坏/二进制伪装/攻击fixture、MiniMax供应商验收。完整原生窗口内的问答操作未用CUA执行（原开发客户端为此前已确认不可绑定的unbundled入口）；已以实际Vue组件浏览器交互、Rust鉴权/HostBridge、Host HTTP与真实Runtime/Kimi分层证明，不把它称为单次完整Native GUI E2E。前四组旧D4不借用于这一边界。无commit/push。
