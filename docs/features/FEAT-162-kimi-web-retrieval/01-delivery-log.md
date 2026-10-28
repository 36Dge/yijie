# FEAT-162 交付日志

## 2026-10-24 — 实施前

- 用户要求保留原生搜索，在Connectors/MCP接入Kimi Search/Fetch；先落完整方案再执行，不做无头浏览器，不改Runtime/Agent循环。
- 用户追加授权目录增加2项；容量62，实际新增一个服务含两工具，共61项。
- 已检查真实源码、官方API、相关仓库规则和工作区，记录baseline与来源摘要。
- `00-feature-brief.md` 完整方案先于产品代码落盘。D0工程内容已齐；不把用户实施授权当作付费/生产/Git授权。
- 实施待开始；外部收费调用0；真实验收NOT RUN。

## 2026-10-24T00:48:43.202509+08:00 — 开始实施

- 完整方案与feature.yaml已通过 `check-feature-package.sh --strict --gate D0`；证据 `evidence/plan-before-implementation.json`。
- 按契约先行、专用REST Backend、Desktop消费分工实施；生成/同步由单一执行者负责。
- 官方models文档确认GET与Bearer认证，未给出单独计费条款；仅作为基础检查，不宣称供应商保证免费或Search/Fetch业务已验证。
- 官方价格当前Search Basic和Fetch均为成功且有数据时0.01元/次；真实调用仍未授权、不执行。

## 实施审查修订

- 独立审查发现固定HTTP client底层reqwest存在默认协议重试。方案第11节先记录最小修订：Connectors直接使用锁内同版reqwest并显式retry::never，不修改Runtime、不升级外部依赖、不做故障注入。
- Contracts formatter正常检查曾等待stdin EOF。仅定向改为真实formatter读取正规临时文件，7项生成结果SHA一致；旧等待进程保留STOP_PENDING，未强杀。

## 本地实现验证与集成准备

- Contracts独立工具与62容量已生成同步；41 JS、5 Go包、Rust 4+7+7、lint/Clippy及source检查通过。7个完整breaking基线3个通过，4个受既有scheduled-plan-draft远程引用EOF影响，不能声称全绿。
- Desktop前端47/47、Native11/11、fmt/Clippy/lint/typecheck/build/docs通过；Host 4包普通命名allowlist race及focused vet通过。
- Connectors最终13项定向检查及5项普通回归、Go两包、Clippy通过；原传输默认重试P1独立复审关闭。
- 原App以Cmd-Q正常退出，ps确认Desktop/Host/worker/artifact子进程均结束。
- 首次Host候选freeze发现experts间接引用market-connectors的来源摘要过期，已由canonical generator/sync更新Desktop/Host/Skills的来源回执，11项专家业务输出字节不变；不改专家内容或政策。
- 首次canonical worker-build成功；资格描述补齐后重新通过canonical来源检查与构建。真实账户调用仍0。

## 专家资源来源级联收尾

- 标准装配暴露旧专家资源 pin 与已正规同步的 Contracts 来源回执不一致；方案第11节先补充仅限本地的来源刷新办法，再实现显式 `--refresh-provenance`。
- 旧 manifest、authority、75个归档与已安装资源先按原 pin 校验；旧 Contracts lock 和 Skills candidate 从 Git HEAD 读取且匹配旧固定摘要。新候选由既有 Skills canonical packager写入新临时目录。
- 完整75项资源元信息、75个归档字节、37个专家版本的内容审校与授权全等后，才以真实新 producer 记录生成 pin，复用原完整验证及安装；普通38项资源和旧73项保留基线未变。
- 新入口与原 `--check` 均通过，6项正常Node测试、ESLint、diff检查通过。审查指出原 `--package` preflight顺序回归，已恢复打包前的原pin/来源/schema校验并再次通过检查；没有通过删除校验或手改摘要绕过门禁。
- 证据见 `evidence/expert-provenance-refresh.json`。该修复不证明专家模型质量，也不新增真实调用。最终App来源回执须包含最后修复后的脚本字节；标准App构建与正常重开由root另行记录。

## 用户要求暂停

- 2026-10-24 用户明确要求“暂停执行，记录状态”，已停止后续诊断、测试、代码和界面操作。
- 最终canonical App编译、打包与来源回执通过；锁屏解除后实际UI显示本地服务未就绪，正常重试一次未恢复，连接器页不可用。编译成功不能视为启动验收通过，feature.yaml已更正startup为FAIL。
- 新连接器尚未安装，未配置密钥，真实供应商/模型调用0。
- 详细暂停记录、构建摘要、未完成项和恢复入口见04-resume.md。App保持现状，没有强杀任何进程。
- 子代理已停止、无运行中命令。暂停前确认Host专家manifest固定摘要仍为旧033689b0…，与新64721b4b…不一致；仅记录为启动失败遗漏候选，未取得本次错误证明，未继续修复。

## 恢复执行

- 用户明确恢复：先核对Host专家摘要、修复本地服务未就绪、完成连接器UI；真实收费API仍禁止。
- 当前进程观察未发现之前App/Host/worker/Runtime或rustfmt等待进程；本任务没有发送停止信号。源码已有变更保持。
- 确认Host固定旧manifest033689b0…而Desktop已64721b4b…；原freeze只记录Host来源字节而缺少与资源摘要的语义核对，拟按正规来源同步补齐。

- Host真实启动配置测试已以同一资源复现旧pin拒绝，并在canonical --sync-host-authority后通过。常量改为生成文件，freeze/build加入来源一致性只读检查，独立复审通过，见evidence/host-expert-authority-sync.json。
- 恢复后的完整启动先因Docker未运行、再因原六个容器退出255被标准脚本拒绝。通过原Docker正常启动及仓库已有recovery-plan/recover入口完成保护副本、数据核对、原服务启动和正常停止，无强杀/删卷/改源码。记录evidence/local-workflow-recovery.json，恢复ID542b525c-8cb9-4bea-aaf2-e3c5cd1e840a。
- 第三次恢复后canonical build正在运行，真实供应商/模型调用仍0。

- 最终canonical build及实际服务就绪PASS，市场61项正常；Kimi新安装、空密钥配置页、取消回传和对话禁用开关PASS。
- Cmd-Q正常退出，所有自有子进程结束；标准--reopen同构建回执及实际安装状态保留PASS。1180x760布局和键盘焦点PASS，窗口已恢复1268x780。暗色无现有UI切换入口，未改系统外观，记录NOT RUN。
- 仅本机新alias Keyring预检，未输入/保存密钥；models/Search/Fetch及模型回合均0。用户要求的本轮本地修复与UI验收完成，D4真实服务验收保持NOT RUN。最终证据evidence/app-resume-ui.json。

## Kimi模型Key复用调整

- 用户明确授权复用现有大模型Kimi Key，免重复填写，并要求方案先行；收费API仍不执行。
- 05-model-key-reuse-plan.md先于本轮产品代码落盘。本轮选择Host已加载Key→私有一次启动管道→Connectors进程内来源，配置阶段零HTTP，启用Probe仍单独执行。
- 记录现有FEAT-163等并行修改，不覆盖；本轮不派发子代理。

- 用户授权模型Key复用：先落05方案，随后provider/broker语义0.5.0及not_configured错误同源生成，Host已有模型快照经匿名启动管道交worker；取消Kimi独立表单和Auth自动Probe。Native/UI只本地绑定，保持未启用。
- 专家来源因provider schema来源摘要变化需再次刷新；generated/schema、75项metadata/archive未变。canonical刷新增加显式成对旧候选证据且以当前pin/authority验证，随后Host authority同步、资源检查和freeze通过。
- 首次真实UI绑定成功且无HTTP；发现静态not_configured提示误盖成功说明，已修正并通过84项前端回归，正在复构建/重开验收。此前首次构建已正常Cmd-Q退出，所有子进程正常结束。
- 最终本地配置UI与同构建重开全部PASS：配置不联网、不出现Key表单；已配置/未启用文案、任务选择禁用、最小窗口与键盘正常；最终Cmd-Q正常退出并释放共享App窗口。真实Kimi HTTP和模型回合均0。06报告、UI/诊断/来源回执及截图已落盘；其他Feature验收未代为声明。
- 收尾辅助broker-qualification编译发现credentials的隐式presentation子模块路径在独立crate root下不可解析；改为同一源码显式相对路径，无行为/依赖变更。编译和14项Kimi回归通过，再走canonical构建更新来源回执；暂未交接共享窗口。
- 收尾模块路径修正的最终canonical构建、真实worker本地绑定、同构建重开及界面确认PASS。最终Cmd-Q已结束所有App/Host/worker进程，源码与生成物稳定，窗口可交接；最新摘要已更新04/06及model-key-reuse-ui.json。
