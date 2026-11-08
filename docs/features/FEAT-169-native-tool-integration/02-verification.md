最新复审与修正见 [03-code-audit.md](03-code-audit.md)。下文保留首轮验收事实。

# FEAT-169 定向验收

四组原生工具已接入并由原 `pnpm client:dev` 入口加载。真实模型验收按用户最后指示仅覆盖 Kimi K3.1 Pro：共 19/40 次 HTTP 请求（含原生子代理），全部 HTTP 200；MiniMax 实际调用为 0。共享计量器已正常 EOF 退出，没有继续消耗余量。

| 编号 | 检查及证据 | 结果 |
|---|---|---|
| AC-001 | 两模型新建/恢复的原生回环；原制品创建 V1、Disabled 各类旧会话，新制品恢复仅声明 V2；JSONL 原前缀保留 | PASS；Kimi 另有真实验收 |
| AC-002 | V2 六工具真实调用、两个子任务轮次；本地真实 Runtime 子审批归根会话、父 MCP 不继承、原生正常中断 | PASS |
| AC-003 | Kimi 真正 apply_patch 创建普通文件，文件字节核验；本地原生审批拒绝后文件不创建；真实 FileChange 仅做展示投影 | PASS |
| AC-004 | Kimi 真正 exec 挂起并 wait 得到 42；本地原生嵌套 exec_command 与 V8 正常 terminate | PASS |
| AC-005 | Kimi 四记忆工具保存/列出/读回/检索普通笔记；本地正常重开、重名拒绝、启动零后台推理 | PASS |
| AC-006 | 两模型 input-only 保持空工具与原生禁止执行注册表；既有检索/专家/生图配置未扩展；原生错误照实返回并正常纠正 | PASS（本次定向范围） |
| AC-007 | canonical 来源/生成投影/配对检查、编译、race；原入口成功启动，/readyz 返回 200 ready，实际 Runtime 路径为新候选 | PASS |

## 来源与证据

- Runtime 候选源码 ID：`34d25437dac82d1e11b33b770bdb0dd28aed7b3482d03b13ad2ebe40f2ffe1fc`，位于 `yijie-codex/.yijie/build/native-tools-v1/<ID>/aarch64-apple-darwin/`；原 FEAT-168 制品与前两候选保留。
- binary SHA-256：`d8ec38a27b03c2c3f5fdab41807a679da771943a0883b5a380f040bc9d57da60`。stable app-server schema 未变，树摘要 `79b27b23a58249dc700567c4c0c824c222bbf4c5b81b894dea5fe8d84f34eb78`，271 文件。
- `yijie-codex/.local/native-tools/build-3.log`：正规构建、锁文件差异验证、stable app-server schema/config schema 生成；`unit-3.log`：4 个定向原生 Rust 用例通过。
- `yijie-agent-host/.local/native-tools-race-final.log`：13 个顶层定向 Go 用例及子例通过；`native-tools-both-prior-generations.log` 补验两模型 V1/Disabled 共四个真实恢复场景；`native-tools-market-startup.log` 验证真实 Runtime 与 canonical 市场 worker 一起启动，0 次模型请求。
- `yijie-agent-host/.local/native-tools-vet.log`：受影响三个 Go package vet 通过。未运行全量 Go/Rust suite。
- Desktop `ChatNativeToolItem.test.ts` 4 用例、相关文件 ESLint、Vue 类型检查、Cargo check 通过。原入口另完成实际增量 Native/Host 编译。
- Runtime 原生来源生成器、Native6 定向生成/同步、Desktop 正常入口完整源码准入均通过；`contracts/native-tools-build.candidate.json` 固定实际 Host 工作树，不伪装 commit/release。
- 真实 Kimi 的脱敏摘要：[kimi-live-acceptance.json](references/kimi-live-acceptance.json)。原账本、测试日志与原生 rollout 保存在 `yijie-agent-host/.local/native-tools-live/20261107-153444/`。进一步核对了真实工具输出：补丁成功、四个记忆工具的数据、exec/wait 的 42、V2 后续任务的 56。
- 正常入口日志：`yijie-desktop/.local/native-tools-entry-final.log`；就绪结果：`.local/native-tools-readiness.json`。新进程使用上述新 Runtime，Skills、专家、连接器启动完成。原三个数据 Home 与数据库保留。
- 组件视觉：CUA 检查真实 Vue 组件的合成记录，亮/暗色、普通宽度与 360px 宽度均可读，折叠/展开正常；子任务显示“已记录”，未伪装为子任务完成。浏览器检查页 `.local/native-tools-visual.html` 仅是视觉 fixture，不写入聊天历史。

## 真实失败与修正

1. 配置整数经 JSON 转 TOML 时曾变为 4.0，引起 FeatureToml 启动失败；已保持整数类型。
2. V2 默认加密参数和 agent_message 不能直接交给本次提供方；已增加显式配置的原生明文通信路径，以及仅作用于出站副本的普通 message 投影。内部历史、邮箱、调度仍归原生 Runtime。
3. 测试曾错误要求 input-only 的 tool_choice=none；核对已有 canonical 行为后按 auto + 空工具表 + 禁止执行注册表验证，没有改用户功能。MiniMax 独立 Server Tools 官方文档支持 web_search，本次保留其原有声明。
4. 原入口的专家资源检查被已有 Skills AGENTS.md 修改阻止；通过固定提交的 detached 工作树承接原专家产物，执行原 manifest/authority/逐归档摘要校验。未改写用户修改、未放宽原门禁，38 Skills + 37 专家资源保持原值。
5. 初次日常启动仍使用旧“memories=false”市场校验，导致 Host 不能就绪。已将启动调用接到当前精确 profile 的校验函数；新增真实市场组件启动测试通过，再由用户正常退出后从原入口重开，最终 ready。
6. 真实 Kimi 第一次读笔记只用了文件名，原生返回 not found；它使用 search 获取规范路径后成功读回。这是正常可恢复错误，未将第一次失败写成成功。

付费验收使用的 Runtime 与最终激活 Runtime 完全相同；其后 Host 只修正了市场启动准入函数的选择，该分支由真实市场启动用例和最终日常入口验证。没有将分层证据伪称为一次自动化全 UI 录制。

## 验收边界

- 用户明确不做 MiniMax 实际验收；其源码配置、两个模型的本地原生回环通过不能替代 MiniMax 真实模型结论。
- Native 主窗口的 CUA 绑定不支持当前未打包进程，按用户正常退出/重开完成生命周期；主窗口没有全流程自动化录制。真实入口就绪、实际工具结果和真实组件视觉分别核验。
- 原生 interrupt 会使子任务进入 interrupted，不构成远端模型立即停止 HTTP 或计费的保证。本次取消均使用原生 API 和正常 EOF，无强杀。
- 只运行相关定向检查。未执行故障注入强杀、可执行文件替换、权限破坏、攻击 fixture；未声称全量回归、所有历史治理生成器或生产发布已通过。Rustfmt 检查发现 sidecar.rs 原有 FEAT-168 段落格式差异，本次新增段落无差异，未格式化无关行。
- Native6 新枚举为 breaking，本地 Host/Desktop 配对升级；回退执行器仍须保留兼容新记录的读者，不降库或改写历史。没有 Git 提交、推送、签名或公开发布。
