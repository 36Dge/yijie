# FEAT-170 同一桌面聊天端到端验收

**本场景 PASS。** 用户本轮只要求补验“桌面同一聊天的完整端到端链路”，其它未完成场景不执行，整体 D4 仍保持未通过。

2026-11-08 16:53—16:54（Asia/Shanghai），通过 CUA 在真实易界原生窗口完成一次用户可见操作：新建隔离工作空间的聊天，选择 Kimi K3.1 Pro、Kimi 网页检索连接器与“请求批准”，输入并发送任务；模型搜索工具后通过 exec 发起调用，原审批卡展示完整参数，点击“允许一次”，收到真实工具结果及最终回答。没有用 Host 直调、浏览器预览、合成模型响应或数据库写入代替桌面提交。

## 实际链路和结果

| 环节 | 观察与证据 |
|---|---|
| 桌面提交 | 原 Vue/Tauri 窗口，真实聊天 `01a1ba5c-e312-7de3-8490-b7fbc78692aa` |
| Runtime | 同一线程 `01a1ba5c-e37a-75f3-92c3-649cef8a9b18`、同一轮次 `01a1ba5c-e3e2-7101-a11e-0234e71b6469` |
| 工具发现 | tool_search 一次；query=`Kimi Basic 网页搜索 kimi_web_search`，limit=1 |
| 执行 | 原生 exec 根据返回定义调用 `mcp__yijie_market__kimi_web_search`；原生 wait 一次等待审批/执行完成 |
| 权限审批 | 原桌面卡片显示 query=`IANA example domains`、limit=1、include_content=false；点击一次“允许一次” |
| 真实结果 | 原产品 Gateway/worker 的 `kimi_web_search` 完成一次；无抓取、重试或第二次查询；原生日志 MCP result 为 Ok |
| 桌面终态 | 同一聊天显示“已完成 61s”，连接器工具“已完成” |
| 最终回答 | “检索成功，返回 1 条相关结果，来源为 Instructions and Guides。”并展示 `iana.org/help` 链接；标题与网址均存在于真实 MCP 返回材料 |

公开检索结果不是固定fixture，不要求命中预先指定网页。这里核对的是回答引用确实来自本次工具返回。工具结果卡仍沿用已有脱敏预览，显示“[内容已脱敏]”；这不影响模型读取原工具结果及最终来源展示，本轮不扩展其它展示需求。

## 原入口、计数与最小接线

当前普通 HMR 窗口不能被 CUA 绑定。用户已正常退出后，复用项目已有的 `development-client.py start-ui` 标准 Tauri debug 构建，沿用原身份、原 Native/Host/Runtime Homes，只在界面新建一个独立聊天和空验收工作空间。没有重置日常数据或覆盖已发布应用。

本次仅补开发脚本显式 `--tool-search-meter` 参数：限定 start-ui 和已启用 tool_search，把既有固定 `http://127.0.0.1:18083/v1` 计数器接入原生 sidecar；正常入口继续过滤环境中的任意观察地址。现有 Host/Runtime/连接器与审批代码不改。私有启动语义影响为 semantic，不新增公共协议或审批机制。两项普通配置定向测试、Shell语法和diff检查通过，随后标准UI构建及实际启动通过。

Runtime仍为 `fac52ad79cc7e0a379fc597a7ecfcee573205d38a60c9d0ed3a2e96871ab0f45`；3个开发脚本/测试来源摘要记录在结果证据中。此前final-source.json是接入阶段快照，本次追加摘要不覆盖原验收来源。

- 原任务模型额度：仅 Kimi 最多12次，续验前5次；本次新增4次全部HTTP 200，**累计9/12次**。
- 本轮用户单独批准一次只读联网检索；实际1次，query和参数与批准相同。原授权中的外部业务0次限制仅对此明确授权的一次查询追加例外。
- MiniMax、图片视频、页面抓取、外部写操作均0。剩余3次不自动消费。
- 验收App通过⌘Q正常退出，canonical清理退出0；计数器通过stdin EOF正常退出0。随后恢复不带计数器的原 `pnpm client:dev`；恢复后的只读状态以结果JSON的cleanup记录为准。

## 可追溯记录与状态

- [具体验收计划及本轮授权](references/ui-e2e-plan.json)
- [同一聊天实测结果、调用ID、来源与额度](references/ui-e2e-result.json)
- 本机原始日志：Desktop `.local/tool-search-ui-client.log`；原生日志路径及SHA-256在结果JSON；模型账本沿用Host `.local/tool-search-live/20261108-current-task/ledger.json`。
- AC-008本桌面完整链路已补验通过。AC-004的批准成功分支得到补充证据，但其它撤销子场景未执行；AC-005的并行/上下文组合未执行。两项维持pending，不把本场景换算成整体D4通过。
- 未提交、推送或发布；用户先前工作树改动保留。

恢复确认：原pnpm client:dev已重新就绪，Host readyz=200，实际Runtime仍为fac52候选且tool_search开启；Host没有计数器地址，18083无监听，累计模型请求仍9次。验收聊天与历史保留。D0文档/声明检查、受影响仓diff检查通过；原接入来源仅3个已列出的开发脚本/测试摘要变化，其余25项不变。
