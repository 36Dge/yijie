# FEAT-171 真实模型验收记录

本轮Kimi真实模型验收通过：九格式生成、四类上传解析修改、Native预览及桌面另存完成。Owner在MiniMax首次请求前明确要求只验收Kimi，因此MiniMax状态为**按Owner排除，0次调用**，不再执行其验收。

使用本聊天批准的30元／80次请求上限，实际62次，保守计费13.160158元，未知费用0。计量器与客户端均正常退出。最后退出时曾自然出现STOP_PENDING日志，随后正常清理完成，未升级为强杀。未提交、推送、安装到日常入口、签名或发布。完整D4仍有未验证项目，不能由本轮Kimi结果替代。

## 验收准备

- 仍使用原日常Native/Host/Runtime Homes，通过固定开发入口 `start-ui --document-meter` 装配专用文档包；没有重置或迁移用户历史。
- 启动前没有运行中的易界进程。计量器独立启动、默认不准入，每个用例绑定原生thread；原总额度未增加。最新计量代码已移除MiniMax验收入口。
- 原生开发入口的文档Runtime曾被后续工具搜索基线覆盖；已修正为最后选定文档完整链。Host/Runtime原生配置和来源校验仍保留。
- 文档focused生成对通用 `generate.mjs` 的扩展与既有原生族不可变来源锁冲突；已恢复通用入口原始字节，新增 `yijie-contracts/scripts/generate-documents.mjs`，复用同一stage/compare/publish机制执行两族生成。既有Native/MCP来源校验与新文档定向无漂移检查均通过，没有刷新旧锁或假称已提交。
- 构建缓存到达两个bucket的正常门限。确认没有活跃项目构建且磁盘余量超过500GiB后，仅清理一个约492MB的过时可再生中间缓存；保留源码、数据Homes、最终二进制和不可变包。具体清单在 `.local/feat171-real-acceptance/cache-maintenance.json`。
- 真实请求前执行4个纯本地计量用例（预占/结算/重开、两模型共用额度、未知usage保留预占、请求/金额边界）及原开发入口7个正常配置用例；不连接供应商，不进行强杀、权限故障或攻击注入。

## 测试输入及证据位置

工作目录：`/Users/jack/Documents/FEAT-171验收-20261109`。上传样本复用本轮已通过包内验证的普通DOCX/PPTX/XLSX/PDF：Word有插图、PPTX和XLSX有可编辑图表、XLSX含SUM/AVERAGE。副本与原件SHA记录在 Desktop `.local/feat171-real-acceptance/upload-sources.json`。

Desktop `.local/feat171-real-acceptance/client-start.log` 保留原始启动失败及后续构建记录，不能把其中旧失败抹去或算作通过。`ledger.json` 为当前请求数及保守费用的权威本地证据；它不是供应商账单。`control-token` 为私有控制凭据，不复制到需求证据。

## 实际结果

| 场景 | 请求数 | 结果 |
|---|---:|---|
| Kimi生成 | 37 | TXT、Markdown、HTML、CSV、JSON、DOCX、PPTX、XLSX、PDF各一个；9个不同artifact_id收到Native提交ACK |
| Kimi上传修改 | 25 | 四份上传原件解析后分别产生新DOCX/PPTX/XLSX/PDF；4个新artifact_id提交成功，原件SHA不变 |
| MiniMax | 0 | Owner取消，未执行，不计通过或失败 |

两项任务位于同一新验收会话，共三个用户轮次（第一项含一次明确继续）。Desktop session为`01a1bffe-b5f3-74f3-a187-8ebc8f18897a`，原生thread为`01a1bffe-b62b-7a92-9893-1967519643df`。请求数包括每次模型续轮，不把37次供应商请求称作“一次调用”。

实际调用链为：内建环境工具→专用Python和指南→原生执行/单次审批→Office或Quartz→原生view_image→publisher→同代际committed查询。共13次原生view_image，无自建看图替身，没有专家/技能/连接器选择或系统Python兜底。

独立复核真实产物（`yijie-desktop/.local/feat171-real-acceptance/independent-real-output-check.json`）确认：

- CSV编号保留前导零；第一项XLSX合计9、均值3，并有可编辑柱状图。
- 修改后的Word只追加指定段落，原表格和嵌入图片内容不变。
- PPTX仅`ppt/slides/slide1.xml`改变，第二页图表等其他包内部件不变。
- XLSX的B2为4，SUM/AVERAGE仍在且缓存结果为7/3.5，图表类型与数据引用保留。LibreOffice会规范化等价引用和锚点表示，不能把这个结果描述为OOXML包字节完全不变。
- PDF原页内容流逐字节相同，新增修订说明页后共2页。

## GUI与保存

九份生成件和四份修订稿均实际在Native文件面板加载。Word版式/正文与分页、XLSX表格/图表切换通过；表格显示4、3、7、3.5。HTML实际WebView的中文、段落和表格已检查；这项操作者验证不改写模型此前“未做浏览器视觉检查”的真实声明。

原生保存面板先取消，显示“已取消保存”且没有目标导出文件；随后确认保存。两份桌面文件与聊天原件SHA相同：

- `/Users/jack/Desktop/FEAT-171验收/Kimi-杭州文化简介.docx`
- `/Users/jack/Desktop/FEAT-171验收/Kimi-杭州样本-第二版.docx`

第一份桌面原件再次导入成功，检查后仅移除未发送草稿附件。正常退出重开后，原会话及13份产物仍可读取。1180×760窗口下的表格、图表和HTML布局通过；实际JPEG截图2360×1520，原生比例2。验证后恢复1339×843及Kimi默认选择，正常退出。

## 真实执行暴露的问题及修正

1. 首次计量器在前一SSE尚未收尾时拒绝了已到达的正常续轮。第一轮真实请求保留在账本，客户端显示未完成；修正为等待上次结算后再准入，用户轮次明确继续，没有重置次数或伪造成功。
2. 开发构建首次校验大包叠加Office转换，超过旧15秒界面等待时间，Word首次点击超时而正常重试成功。保留全部文件摘要检查，采用macOS CommonCrypto流式SHA-256，并给Office保留与180秒转换软期限匹配的200秒有界加载等待。进程内首次完整校验3.039秒、热校验0.361秒；未清空操作系统文件缓存。修正后当前包首次Word点击约3.55秒即加载。
3. 上游已有`imageView`未进入v6展示枚举，实际看图被显示成未知内容。已先扩展源契约并生成配对consumer，再接Host标签和Desktop展示；新调用实际显示“查看图片／已完成”。旧未知记录保持，不篡改历史。
4. 指南现直接为Office转换申请既有单次审批，避免先运行已知会被拒绝的命令；文本/HTML指南明确不调用仅支持Office/PDF的render。无永久沙箱、网络或执行权限扩张。

新增定向检查：Native SHA一致性及真实整包冷/热校验、Host看图事实投影、前端正常20秒首次Office加载和原生看图生命周期均通过；相关lint、类型检查、源/consumer生成检查通过。计量最终7个普通本地用例通过。新版包内九格式及丰富图表样本再验证通过，10张PNG与此前已检查样本逐字节一致（其中包含1张插图，不将其计为额外页面）。

## 费用证据与资格边界

初始全价上界记录保留在`ledger-before-cache-reconciliation.json`。已知缓存usage只在同一原生thread、输入/输出token数完全相同且接收时间有界、唯一匹配时参与对账；精确原生快照和摘要单独保留。21条匹配，3条继续保留原全价上界；没有返还未知费用，没有改动供应商请求数或提高30元/80次授权。后续直接从供应商SSE读取合法缓存计数。记录见`cache-reconciliation.json`，不是供应商账单。

当前文档包为`b9334b12900a2476f05a2aa3e9d86ed307fe499d98368ce438e6de0b5c3cc665`，展开992,351,822字节，本地体积测量归档383,712,685字节（不是已安装或发行的分发包）；完整本地release构建候选为`ed619231340b81e76426bdd616c6bf574941f1ec3df67f7a2a401a9c5d40fa73`，展开1,521,638,869字节。配套回执、文件摘要和原始日志见[机器记录](references/real-model-checks.json)。

本机为macOS26.5/arm64/24GiB。干净用户安装、macOS14/8GiB最低配置、正常安装升级回退仍未验证；当前设置和菜单没有应用级外观切换入口，未更改系统外观，深色Native GUI也未验证。正式分发许可/SBOM复核、签名公证属独立发行门禁。D4保持NOT RUN，未执行项不记为通过。

全程只采用正常开发、公开合成样本、普通取消和正常退出；没有强杀、替换程序制造故障、权限破坏、攻击载荷或危险归档，没有运行全量回归。
