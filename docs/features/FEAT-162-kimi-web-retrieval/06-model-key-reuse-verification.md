# FEAT-162 模型密钥复用验证

2026-10-24。本轮按用户要求，先落盘 `05-model-key-reuse-plan.md` 再修改实现。此前独立连接器Key方案已被替代。本文件记录的是本地候选；不声明生产发布或真实Search/Fetch能力验收。

## 已实现

- Host复用已加载的Kimi模型Key快照，经单次匿名启动管道交给其拥有的Connectors worker。版本、长度、完整结尾及EOF校验；worker在创建线程前消费并关闭。Key不进入新的环境变量、argv、控制JSON、Native/UI、日志、第二份Keyring或文件。
- Kimi“使用现有Kimi密钥”仅完成本地绑定：无浏览器凭据页、无HTTP、无自动Probe。缺失来源返回`not_configured`；成功保持disconnected/not_qualified/executionAvailable=false。
- 主按钮随后显示“检查连接并启用”；该显式操作才沿原Probe检查`/models`。本轮不点击该按钮。停用/卸载不删除模型Key。
- 其他连接器继续使用原有凭据流程，原生搜索和调用链保留，不重建Agent循环、不修改Codex内核。
- 同一个Host生命周期内，模型和连接器使用同一快照；正常重启加载新模型Key。持久安装/绑定引用不被当作新的联网资格。

## 检查结果

证据：`evidence/model-key-reuse-checks.json`。

| 检查 | 结果 |
|---|---|
| Contracts broker/provider/host/web-retrieval | 22项JS、3个Go包通过；相关consumer正常生成同步 |
| Connectors | 14项Kimi检查、1项来源解析检查通过；Clippy/格式及canonical构建通过 |
| Host真实worker | 普通内存值/无来源的本地绑定通过；状态无执行资格，正常EOF退出；另4项既有生命周期通过 |
| Host | 模型环境清理/审批/禁用配置3项通过；定向vet通过 |
| Desktop | 84项前端测试、11项Native目录测试、1项本地绑定状态投影测试通过 |
| Desktop静态与构建 | scoped ESLint、Rust fmt、Clippy lib、标准pnpm build通过 |
| 专家来源 | 5项来源刷新测试、Host真实资源manifest启动校验通过；75项metadata与归档不变 |
| Runtime边界 | HEAD `9154f27d0cdb526a5f5ba0913fe3e2448014b4a1`，工作区干净；固定Runtime SHA256 `9766d7e10d25327f0595964a19ad67e1e1c1db0c22e5a65f9af66b547ab316c6`未变 |

首次真实UI已完成本地绑定（诊断仅model_credential_binding started/succeeded，无HTTP阶段），随后发现静态目录not_configured提示遮盖成功说明；已修正为真实operation错误优先、已配置Kimi忽略静态未配置提示，并加入带实际目录blocker的回归；84项再次通过。过程中旧UI/契约文案断言按本轮需求更新后通过。误用`vue-tsc -b --noEmit`触发既有project配置不兼容；标准`pnpm build`通过。第一次freeze正确阻断未同步的专家来源；没有绕过门禁，已通过canonical生成、已验证旧候选证据的来源刷新、Host authority同步及freeze。历史全量breaking基线的既有失败仍见`02-verification.md`，未宣称全量通过。

## 未执行及影响

- 真实`/models`、Search、Fetch和模型回合：NOT RUN；按用户限制，本轮不验证账号实际权限、余额、质量、计费或模型驱动MCP。
- 真实D4：NOT RUN，不继承其他Feature额度或验收结果。
- 禁止的强杀、二进制伪装、权限破坏、攻击注入等验证未执行；采用正常内存值、正常管道与EOF、本地组件/状态测试。
- 暗色实机：NOT RUN；现有App无主题切换入口，未改变系统外观。亮色及最小窗口已检查。

## 最终真实界面结果

本地绑定PASS，无输入/回显密钥或浏览器页。最终文案为“已复用现有Kimi模型密钥；当前尚未验证连接，连接器未启用”；对话选择开关禁用/off。亮色1180×760、恢复1268×780、键盘聚焦与关闭PASS。正常Cmd-Q、canonical `--reopen`及相同来源回执PASS；重开后仍已配置/未启用。最终再次正常Cmd-Q，App/Host/worker均已退出，未强杀。

证据：`evidence/model-key-reuse-ui.json`、`evidence/model-key-reuse-diagnostics.json`、`evidence/model-key-reuse-reopened.jpg`。元仓50项测试、lint及shell语法检查通过。真实`/models`/Search/Fetch/模型回合仍为0。

来源回执SHA256 `796a510907014b0e3dcf394fe75387b23892cf5d96ba3b2362d50968dc312102`；App `0d79ee061c1a284db20e274c66a3aaa8b5f23f194a8cfabf24ffbb5085cb0cc5`；Host `be5a7c27407520bec1975c66ccc4cb0ccb95c36a90c828f17baa8371b97603d8`；worker `7d7842ad9cae62f2913e381e7f4a115e8039e88180656b6c0c788350518a36f8`。当前为local candidate/release=false，未提交、推送或发布。

收尾broker-qualification模块路径修正后，专用验证程序编译、14项Kimi回归、最终worker实际本地绑定、canonical App重构及同构建重开均再次通过。最终界面AX见`evidence/model-key-reuse-final-source-reopened.ax.txt`，全程没有点击启用/检查连接或发送模型任务。
