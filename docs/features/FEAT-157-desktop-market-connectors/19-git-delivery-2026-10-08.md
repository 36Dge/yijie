# FEAT-157 Git交付记录

2026-10-08，Owner明确授权git add、git commit及推送对应远端。contract-impact = none：本轮交付不增加wire、权限、持久化或业务语义；提交的是已验收FEAT-157，并补充来源与交付记录。范围仍为49项，本地D4仍采用已接受的分阶段证据。

## 已核实的实现仓库推送

| 仓库 | 远端分支 | 提交 |
| --- | --- | --- |
| yijie-contracts | `chore/retirement-baseline-20260905` | [`2e587b70`](https://github.com/36Dge/yijie-contracts/commit/2e587b708abc83a126adf8cd1d03944adee09e22) |
| yijie-connectors | `develop` | [`629d3975`](https://github.com/36Dge/yijie-connectors/commit/629d3975b793c6a147e8b1027c9035ad870a4fc6) |
| yijie-agent-host | `chore/retirement-baseline-20260905` | [`379542c1`](https://github.com/36Dge/yijie-agent-host/commit/379542c1b3adedfc1dda007f942beb2dd40803ac) |
| yijie-desktop | `feat/157-market-connectors` | [`7a10fb0c`](https://github.com/36Dge/yijie-desktop/commit/7a10fb0c3b40e9aa45746725963d22069e3322e9) |

四项均已完成正常push，随后git ls-remote确认远端分支精确指向上述提交。元仓yijie沿现有`chore/retirement-baseline-20260905`提交本包、ADR及此记录；元仓自身提交号由本文件所属Git提交标识，避免自引用摘要。

## Desktop范围隔离

原工作区有14个文件含其他店铺、工作流及已有对话输入框布局修改，另有本地未推送店铺提交`7c0bf92`。只按片段暂存FEAT-157：原分支本地提交`83800df`保留既有历史；从已推送基线`8d74159`创建功能分支，远端提交`7a10fb0`。两个FEAT-157提交的完整patch逐字节一致，远端分支没有携带该店铺提交；原工作区其他修改与原分支均保留，不reset、不stash、不强推。

提交候选在隔离检出中验证：12文件96项加3文件34项，共130项前端测试通过；lint/type检查及前端构建通过。隔离验证只运行普通本地测试，不运行模型或供应商接口。旧Native/Worker/Host/Tushare证据仍分别保留，未改写为本次发生。

契约与Connectors/Host提交完成后，使用canonical脚本刷新Desktop目录与Host来源快照；协议生成物一致性通过。Rust target缓存不入库。一个导入SVG仅移除行尾空白，已比较XML元素和路径属性语义一致并更新资产摘要；原图文件不改。

39份历史原始log已显式纳入版本控制，其中11份末尾空行被git diff --check提示。为保留既有证据摘要，不改写日志；源代码与文档的whitespace检查通过。新增隔离检查原始日志同样按原字节留存。

用户本轮只授权Git交付：未新增付费调用，未新建PR、打tag、合并或部署，也不声称生产验收。完整机器回执见[Git交付证据](evidence/git-delivery-2026-10-08.json)。
