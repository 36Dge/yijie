# 七项复审修复：最终验收与自审

2026-11-14。七项问题已修复并通过正常本地流程验证，补齐完整桌面提交、实际维护命令和冷启动。结论限定本机候选，不代表真实供应商模型质量或生产分发验收。原始失败证据保留，没有将未知提交重发或改写为成功。

## 问题与关闭证据

| 问题 | 最终修复 | 验证 |
|---|---|---|
| R1 日常聊天阻断 | 启动、提交和清空连接器配置共用完整原生策略。技能预检强制传实际CWD；工具市场预检至turn准入共享资源门闩；接受结果先重放 | 真实Runtime＋产品worker空/非空选集、新建/续聊/冷恢复4次本机完成；Host服务CWD/重放检查；最终GUI组合选择与冷恢复完成 |
| R2 回滚复活卸载项 | 先检查所有对象的原生事实；仅安装前或journal记录的本次回滚卸载阶段接受absence；后续用户卸载在副作用前拒绝回滚 | 正常迁移→用户卸载→回滚拒绝；规则、路由、readiness和旧源保持，安装未复活 |
| R3 跨技能规则回滚 | 全局逆序撤销更新规则，再逆序撤销迁移；完整逆向链先校验，实际写入沿用原生CAS | 两项旧技能、两次原生更新、额外路径opt-out→回滚→resume通过；原规则和停用策略保持 |
| R4 漏掉needs_attention | 维护准入检查完整未决索引，不能用worker队列代替；拒绝时不改变模式/readiness | 缺description导入→needs_attention→拒绝回滚→取消→任务准入恢复→回滚/resume；GUI取消后继续聊天 |
| R5 清单外旧安装遗漏 | 既有回执校验补足发行清单，支持条目移除及catalog-only下架；保留原ID/内容版本/文件/启停，不重新授予发行安装权限 | 实际两个打包器生成下一版本，两种下架均完成迁移、兼容回滚、resume、启停和卸载；卸载后不再提供加号 |
| R6 固定38项打包 | 源打包器和Desktop资源入口按现有0..512契约接纳变化；屏蔽/目录占位项不进入可安装源，专家生产链不变 | 37、39、屏蔽后37、空目录四个发行场景；当前38项重新生产，298文件与实际随包内容逐字节一致 |
| R7 验收缺口 | 增加完整Host提交、产品worker、实际desktop-host维护命令与原生GUI冷恢复；分层记录实际证据 | 25个Host定向根用例及补充Session检查、4项契约、7项前端/资源、动态打包检查通过；详见下文 |

## 验收发现的额外接入遗漏

实际维护命令发现：重复调用原生 `marketplace/add` 会更新 `last_updated`，改变恢复所核对的配置版本。现先通过原生 `config/read` 检查固定根，仅未登记时调用add；没有跳过CAS或放宽配置保护。最终 `rollback → 兼容模式正常冷启动 → resume → 原生模式正常冷启动` 通过，两个旧身份和一个个人源保持，任务准入开放，正常冷启动不改写用户配置字节。

完整GUI发现：普通v2聊天已传CWD，但工具市场提交的提前技能预检遗漏CWD。首次三轮普通/技能/连接器聊天分别通过，转换为工具市场会话并重开后，第四个提交未获确认且未到本机响应服务。修复后将CWD改为必填，补充Host服务回归，再用新的验收会话完成“技能＋连接器”提交及同一会话冷恢复续聊。原会话及未知提交保留，未清库、补写成功或重复发送。

## 完整原生窗口验证

四轮App均通过同一规范入口和同一独立数据集正常重开：

```text
python3 -B scripts/development-client.py start-ui --skill-acceptance feat174-review-20261114 --tool-search-meter
```

未切换日常数据或简化工具市场装配。模型端为 `scripts/skill-market-local-response.py`：固定本机18083、无转发、不产生工具调用，以stdin正常停止。此响应服务验证真实应用传输、原生装配和恢复，不评价模型自主选择或商业效果。

- 初始38项全部有安装按钮，没有自动安装。
- SKILL.md导入默认启用；停用后同内容根ZIP重导不新增、不重新开启；显式启用成功。
- 外层目录ZIP保留参考文件和普通脚本，一次完成安装；脚本未执行。
- 缺description草稿被原生拒绝，不进入可选择技能；正常取消后错误操作消失，后续聊天继续。
- 5次本机请求完成：普通新聊天、显式技能续聊、非空连接器选择但不执行工具、最终修复后的技能＋连接器组合、该会话正常退出后的技能续聊。第2–5次请求含原生加载的技能正文标记。
- 最终冷恢复显示原回答，两个个人技能均保持启用；资源包正常停用/重新启用通过。
- 四轮均菜单正常退出；专用容器正常停止并保留卷和其他项目。本机响应服务及本次启动的Docker Desktop均正常退出。

退出后只读核验：2个Host会话；7笔技能操作complete、1笔cancelled；两个个人源共4文件，在N2实际返回的原生路径中逐字节匹配，没有推导缓存布局。修复前未知聊天提交仍保留，未重新派发。

## 原生复用、数据与工作区自审

Runtime源码、25项补丁、canonical schemas和固定二进制未改。安装/卸载调用原生PluginStore链，更新/内容回滚调用N3及既有刷新算法；技能解析、发现、正文读取、配置优先级和执行仍由原生负责。新增代码只处理Host操作归属、规则编辑逆序、旧回执投影和接口接入，没有另建匹配器、安装器或执行器。

旧JSON/bbolt回执及指纹沿用原codec，v3降级保护不撤销。无法证明归属的回执、未知配置编辑、用户后续卸载/启停意图仍停止自动回滚并保留现场；不以清库、改schema数字或覆盖旧源解决冲突。清单外历史普通身份限定既有五类命名空间，专家维持原边界，未知身份不自动认领。

六仓HEAD不变，canonical `codex-rs` 无diff。Desktop本轮基线69个已有文件中62个逐字节不变，其余7个仅为已授权契约、资源和构建候选更新；已有聊天、图片、视频及媒体验收文件全部保留。

## 证据与未执行范围

- [机器摘要与源码身份](references/review-fixes/checks.json)、[工作区保护](references/review-fixes/workspace-protection.json)
- [Host回归](references/review-fixes/host-tests.log)、[Session补充检查](references/review-fixes/session-tests.log)、[Go vet](references/review-fixes/host-vet.log)
- [契约](references/review-fixes/contract-tests.log)、[前端与资源](references/review-fixes/frontend-tests.log)、[动态打包](references/review-fixes/packaging-tests.log)、[内容再生产](references/review-fixes/source-reproduction.log)
- [GUI本机请求摘要](references/review-fixes/ui-local-responses.jsonl)、[原生缓存字节核验](references/review-fixes/ui-state.json)、[修复前命令冷启动失败](references/review-fixes/cold-command-before-fix.log)

未执行：付费调用、真实供应商业务质量评测、日常用户数据迁移、签名发布、全量历史回归，以及用户禁止的强杀、程序替身、权限故障和攻击fixture。付费/外部业务调用为0；无提交、推送或发布，未执行项目没有记录为通过。
