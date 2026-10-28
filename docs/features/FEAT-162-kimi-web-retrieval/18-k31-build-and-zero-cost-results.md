# K3.1基线整合、零费用验证与新构建结果

2026-10-28。用户已授权本需求必要本地提交并继续构建，未授权收费、推送、发布或数据迁移。该报告只覆盖本轮准确来源，不将旧K3的Search/Fetch真实结果冒充新模型客户端端到端结果。

## 实现与来源

沿现有Native/Host/MCP/Broker调用链加入原Kimi REST Search/Fetch，实现标题、URL、摘要列表及指定URL Markdown正文提取。现有Kimi模型凭据通过Host已有装配及匿名FD交给worker，不增加用户填写/绑定/启用步骤；普通工具审批仍保留。没有重建Agent循环、修改Codex内核或实现无头浏览器。

目录revision11、61项、容量上限62。K3.1模型身份、max推理profile、退役K3只读、SQL41/Host11兼容边界、旧会话和数据迁移代码保持。补齐market-host/2 0.5.0的缺凭据错误，通过canonical v2同步保留新模型身份。

| 仓库 | 本次本地提交 |
|---|---|
| Contracts | `2adfa2bef43d38a932f6249dbb0a229c173ff103` |
| Connectors | `d88b8d0b8e95978ef3494c90bb5e0e619aa3a27d` |
| Skills | `704d2cc85a85d0759e6103e3f539552f3d63b1e9` |
| Host | `20539889259587a66a574201e521c2ea9469c54d` |
| Desktop | `446a5ac71b9a6767f2c8944178692c654e90df5c` |
| Runtime | 保持 `11fd4504c28afd0f65c6f5f62a6b5328dd437f5a`，未提交修改 |

专家包canonical重建后75项metadata/归档逐字保持，37专家版本可安装、读取、正常重开；Host/Native同一manifest `423621cd1da5087e7ee0ed575c985c4fd8e3b0fdf9c69db376f11fde1de51fa2`。旧producer/slot保全于本轮本地日志目录，旧generation原样保留。

## 零费用检查

| 检查 | 实际结果与边界 |
|---|---|
| Contracts | 定向46项通过；Rust Web工具4项通过；完整lint通过，12项既有unused警告 |
| Worker | Kimi14项、格式/Clippy、canonical构建通过；独立预检先拒绝、0供应商请求、正常EOF |
| Host | v2来源、K3.1共享Key有/无来源、本地Probe/旧Auth通道、37专家版本正常重开及lint通过 |
| 前端 | K3.1连接器68项、模型路由2项、完整ESLint及类型检查通过 |
| Native | 默认连接器58项；canonical K3.1调用面4项；新增K3.1选择kimi-web、冻结回执及正常重开1项通过；Rust fmt/候选Clippy通过 |
| 构建来源 | 19项准确提交来源检查、四种功能组合来源闭合、14项入口规则测试通过 |
| 资源保留 | Skills lint及2项包检查通过；旧App119文件、Host/worker/adapter/Runtime与旧回执一致 |

未跑包含用户禁止行为的全量故障/攻击测试。保留本轮真实失败记录：宽匹配Native候选组44通过/16失败，原因是旧K3 fixture和缺少候选环境；随后使用既有canonical K3.1精确入口通过，未改退役或迁移逻辑。Host专家测试首次使用含`..`路径被正常拒绝，规范绝对路径复验通过。这些失败不抹除，也不记作全量测试通过。

## 新客户端构建

`pnpm daily:prepare --generation 20261028-03` **成功，退出码0**。Go固定已安装1.26.5、依赖离线、全部六源码仓已提交且干净。仅prepare-only；没有打开用户数据库、读取真实Key或启动App，没有新建激活批准/数据Home。新产物是本地未签名开发构建，不代表安装、激活、发布或真实UI验收。

- App：`yijie-desktop/.local/builds/primary/20261028-03/target/debug/bundle/macos/易界 AI.app`
- App二进制SHA：`9c7ebfea56398a0b7a20ba9dbe714f86715fabdfbcf8a5e7e92c74f1e466c9f6`
- Host SHA：`0df0ea2e30aed754aa6b99ba142b0f2336b3e0990b9647dc428c6bda9b732ee8`
- Worker SHA：`f0e5059386fe244bad93c911608b6b2d431951759fb44988ecec1bb90a448065`
- Runtime沿用SHA：`283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e`
- 回执SHA：`fea236b9a0067e4ce6b1c47af6c4c0f65bec83efec2c073974ee0666a8588d9c`

实际打包worker又通过独立新一轮预检：拒绝后供应商HTTP0、模型0、正常EOF。构建后逐项验证1231份客户端来源文件、新App119文件、旧App119文件和新旧Host/worker/adapter/Runtime摘要；未覆盖旧generation。具体证据见[汇总](evidence/k31-build-zero-cost-results-20261028.json)、[canonical构建回执](evidence/k31-build-receipt-20261028-03.json)、[实际打包worker预检](evidence/k31-packaged-worker-preflight-20261028.json)。

本轮真实模型、Search、Fetch和其它供应商账户API均0次，费用¥0。真实客户端对话、实际UI审批/结果和新构建业务历史重开仍NOT RUN。收费提案见[17号](17-k31-client-e2e-proposal.md)：模型最多3次、Search/Fetch各1次、保守总上限¥43；未获批准，不执行。

收尾检查：元仓lint及57项治理测试通过，报告本地链接与证据一致性通过。需求文档随本次授权仅在本机提交；未推送、合并、打tag或发布。旧失败记录和暂停检查点保留，当前状态以本报告和04号最新段落为准。
