# FEAT-165 当前实现审计与续验

2026-10-29。Owner要求审核实现进度、现有问题并继续执行；随后先批准新增5次、再批准新增10次，累计上限20次。只使用本需求合成样本，不调用外部MCP/图片视频供应商、不迁移日常数据；本阶段未授权新增Git提交/推送。后续Owner已授权最终审计修复、验证后本地提交，最新状态转至[04最终审计](04-final-audit-and-local-delivery.md)。本页保留续验检查点，实时次数与逐笔结果以[机器账本](references/implementation-validation.json)的real_task_submissions为准。

当前结论：本地D4已通过，feature usable、implementation complete。累计真实任务7/20；Owner已接受历史分页分层证据，UI加载更多按钮仍未实测。下面保留恢复时的审计与后续执行链。

## 恢复时审计结论

- D0已接受，实现仍active，D4未通过。上轮AC-001/004 pending，其余8项按02所列范围PASS；不是全部需求交付完成。
- 12种输入/输出和原件另存、普通与专家生成、历史重开已获得实跑证据。拖入失败已定位为Window/WebView事件目标不匹配，改用Tauri已有WebView订阅，用户确认第10个CSV胶囊出现。
- 原生userMessage类型/wire/持久化及yijie-codex源码保持不变。本地附件与原生消息仍是独立事实，只有唯一明确session/turn绑定才替换展示正文；冷历史/歧义不猜关联。没有新增产物引擎、传输或存储系统。
- 来源路径一次不可用观察未定位为稳定缺陷。临时诊断已删除，最终新导入/焦点/Esc/前后台切换均复验正常。保留原观察，不将推测写成根因或无条件保证。
- Contracts61137174a25dc368e0006f27633fd4a9ad097aa6为已批准本地提交；其余源码仍未提交。Runtime、Contracts和Skills工作树clean，产品仓HEAD与上轮一致，元仓FEAT-162并行改动保留。
- 全量契约生成/breaking的其它族引用阻塞仍未解决；受影响源闭包和专项通过仅支持当前local候选，不能扩大为生产兼容/上线结论。

## 下一步执行

1. 第6次任务：当前已有Kimi网页检索选集，附合成CSV/SVG，明确只读附件上下文、不联网/不调用工具；验证现有选集提交包装和原生绑定。已实际完成，CSV/SVG内容正确，未显示工具调用记录。
2. 纯附件任务：沿已验证的普通聊天入口，只发一份合成TXT，不输入正文，第7次已完成，本地提交及native完成后均只有附件行；正常重开继续验证。
3. 历史分页：先使用已有实际任务记录与既有有界reader，核对游标、不同页绑定及原生事实保持。正常UI每页20轮，当前本需求会话不足20轮；不改阈值、不seed历史、不用额外模型凑数。分层证据与UI按钮实测分别记录，若需替代该项Must验收，取得Owner明确接受后才改结论。
4. 实跑发现问题时，先查真实提交/Host/Native及视图绑定，再做最小修复和对应正常测试。完成后正常退出、canonical同构建重开、更新严格检查和claim审计。

预算、权限、数据与安全边界不扩张：不强杀/破坏权限/篡改可执行文件/攻击fixture；只使用标准脚本生成当前项目可复现候选，保留早期失败。任何未覆盖场景不得冒充PASS。


## 本轮执行结果与剩余决定

任务6/7已完成，并在正常Cmd-Q、canonical重新构建及同构建重开后恢复：第一轮CSV/SVG附件行和原文各一份；第二轮只有TXT附件行，无空白正文。两轮Native Item均为userMessage/reasoning/agentMessage，没有工具调用Item。累计7/20，未消耗剩余13次。

真实Native历史用已有reader每页1轮读取，两页游标前进、集合不重叠，TXT空原文与CSV/SVG原文分别匹配原turn；原生历史重复读取值相同，现有页面历史未被修改。新增正常store分页组合回归覆盖同名不同ID、纯附件/正文+附件、加载旧页与两次重开，通过1项；原生输入对象保持且没有submit。当前普通UI每页20轮，按钮本身未实测，已请求Owner决定是否接受上述分层验收；答复前AC-004和D4保持未通过。

审计补正了两份Design Pattern：旧SVG拒绝与全面禁止路径到DOM规则现有FEAT-165限定增补，明确临时draft受权、非持久、图片投影与原生消息独立绑定。没有新产品实现或权限扩张。首次新增测试使用了不存在的historyAvailability=complete，lint检出后已改为源类型partial；最终lint与回归通过，未放宽生产类型。

## 本地契约资格收口

FEAT-165仍为breaking；本轮没有修改Contracts源或提交。local资格基于固定6113717及完整受影响反向来源闭包，不能等同生产兼容。现有检查器再次验证31 schemas、8项输入/媒体/选集/专家专项、媒体生成物一致性；对即时来源2adfa2b和已发布f16a497的JSON Schema比较均PASS；AgentHost OpenAPI对两个基线PASS，runtime-permissions对即时来源PASS、已发布基线不存在该族记N/A。media-v1和v9生成事件相对即时来源字节不变。

输入仅在匹配Host/Native候选激活；SVG/MP4保持file身份，显式v12承载新输出，v9不扩闭集；原私有存储v42只做前向reader拒绝，回退不可用旧binary降级写库。普通、选集、专家实际链路均有证据，Runtime/userMessage未变。因此本地contract.status可记PASS；完整safe生成及跨所有其它族的breaking仍因历史引用阻塞而NOT PASS，不能声称全量/生产资格。此结论按demo_fast无需full-green的范围作出，没有关闭或修改任何检查器。


## Owner分层接受与本地D4结论

Owner明确回复“接受分层验收，记录UI按钮未实测”。AC-004按真实Native两页读取、同源store正常分页/重开回归、实际App正常重开两轮的组合证据通过；UI“读取更早的对话”按钮仍NOT RUN，不改写为人工点击通过。累计真实任务7/20、剩余13次，无新增额度消耗。

其余9项Must已在对应记录列明范围通过，本地契约资格已收口，implementation complete，feature usable。最终严格D4和claim命令均PASS，57项治理测试/元仓lint/Shell语法通过；结果见机器证据；D4只指本机隔离候选可用，不是生产发布、日常数据库迁移或Git合并资格。Contract全量其它族生成/breaking历史引用问题及未确认路径观察保留。没有新增Git提交/推送。
