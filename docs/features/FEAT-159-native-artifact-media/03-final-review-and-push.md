# FEAT-159 / FEAT-160 提交前复审

2026-10-18，用户明确授权再次审核 HTML、SVG、有声MP4内置预览及原UI设计师聊天恢复，确认后提交并推送相关远端。安全约束不变；仅源码提交推送，不代表签名、公证、发布、部署或生产激活。

## 审核结论与修正

逐项检查了Contracts源及生成物、Host原生MCP登记/工作区读取/加密spool/事件顺序、Native MIME与SQLCipher迁移/保存/Range/HTML隔离、正常退出清理、原聊天回执查询及终态核对、前端状态显示、canonical来源锁。

发现并修正一个合法SVG兼容问题：Host按XML namespace接受`<s:svg xmlns:s="http://www.w3.org/2000/svg">`，Native原先直接比较根元素字面名`svg`，导致合法带前缀SVG被拒绝。修复直接复用现有quick-xml的NsReader/read_resolved_event，按namespace与local_name确认SVG根节点；保留大小、深度、UTF-8和既有声明限制，不引入依赖、自制解析器或攻击fixture。

新增普通样本包括带XML声明的前缀根节点、空前缀根节点；同一前缀SVG进入Host登记/ACK与Native提交、保存和正常重开测试。修正后未发现尚未解决的阻断性问题。原HTML自包含限制、WebKit解码范围、原生历史部分信息提示均保留。

## 本轮检查

- Contracts 28项JSON Schema、新媒体普通conformance、artifact-media双consumer及experts三consumer同源检查PASS。
- Host媒体与FEAT160恢复定向race PASS；SVG修正后媒体race再次PASS；Go vet覆盖session/artifact/app/codex，gofmt检查PASS。
- Native媒体正常测试2项PASS（包含用户testmp4.mp4、前缀SVG保存/重开）；FEAT160正常恢复测试2项PASS；Rust fmt和clippy `-D warnings` PASS；SVG修正后相关测试和clippy复验PASS。
- 独立MCP adapter fmt/clippy `--locked -D warnings` PASS。
- 前端普通控件、产物引用、未知/终态显示14项PASS，39项未执行；vue-tsc、改动文件ESLint、设计文档build PASS。
- 两个Feature Package D4记录门禁PASS；元仓lint/50项纯治理测试/Shell语法PASS。
- 所有待提交文件按本任务范围逐项核对；无二进制、真实媒体文件或凭据模式命中。既有75份专家资源及prompt不修改，仅来源证据更新。
- Codex源码工作树干净；固定binary/manifest及用户MP4的SHA与之前验收一致。

未运行用户禁止的攻击fixture、强杀、权限破坏或二进制篡改，不宣称这些覆盖通过。本次复审没有追加模型请求；此前FEAT159和FEAT160真实播放、保存、正常重启和两次原聊天收发证据保留，见各自02记录。本次后续只对已提交源码做canonical构建及现有内容观察，不补发旧操作。

## 提交来源

所有提交沿既有工作分支及跟踪远端；未改远端、强推、合并或打tag。Contracts源先提交，Skills同步同源pin，Host实现随后提交，Desktop再使用现有freeze工具锁定Host完整提交和全部文件摘要。

| 仓库 | 当前提交 | 目标远端分支 |
|---|---|---|
| yijie-contracts | `498c4e79c1889e0500caaf69960553e03876dc0b` | origin/chore/retirement-baseline-20260905 |
| yijie-skills | `d2923c697603e14d86ae0047606c7348af88d1ca` | origin/develop |
| yijie-agent-host | `69da2631178bccac783fe6196fc8cd5e41725d96` | origin/chore/retirement-baseline-20260905 |
| yijie-desktop | `77e9b61ec1b1ed5ccc17785d243c8a6c2bd63b96` | origin/chore/retirement-baseline-20260905 |
| yijie | 本记录所在提交，见Git历史 | origin/chore/retirement-baseline-20260905 |

Contracts候选仍是release=false，原生成base/digest证据按其真实含义保留；没有把旧base字段伪装成当前发布tag。Desktop Host build candidate已通过现有freeze锁定`69da2631178bccac783fe6196fc8cd5e41725d96`，逐文件摘要复核一致。Git提交不修改资源内容或用户数据。

最终已提交源码构建及远端核对结果在后续段落记录。

## 已提交构建与远端核对

- Desktop `77e9b61` 的 `pnpm tauri:demo-fast:app` 构建及canonical receipt通过，日志 `.local/feat159-160-committed-build.log`。构建后Desktop工作区干净。
- 实际App原普通聊天的三类ready卡片恢复；HTML独立内置预览按钮0→1、关闭正常；SVG显示原中文图形、100%→125%缩放正常；MP4显示原瑜伽画面，音量1且未静音、播放控件正常。本次未把控件状态冒充新的人工听音确认；音频依据此前用户明确确认，音视频路径未改。
- 只读Host API核对原UI聊天仍为同一session/thread、Host idle且active为空；原生仍恰好3轮（旧interrupted及两条completed验收），没有新增请求或自动补发。JSON证据 `.local/feat159-160-committed-history.json`。导航时工具提示用户正在操作App，已停止进一步导航、重新读取当前状态，未强制抢占操作。
- Contracts、Skills、Host、Desktop四仓普通push均exit0，随后`git ls-remote --heads origin <branch>`逐一核对等于上表完整commit，四仓工作区干净。元仓记录随后作为独立提交推送。
- 本地检查和远端同步是不同结论：当前chore分支不触发既有push CI；Skills develop触发的CI run 39114497051最终为144通过/1失败，未声称远端CI全部通过；原因与父提交既有失败一致，详见下文。

## 远端CI的既有环境缺口

Skills新提交[CI run 39114497051](https://github.com/36Dge/yijie-skills/actions/runs/39114497051)为144/145通过，唯一失败为`tests/thirteen-fourth-sale.test.mjs`读取`../yijie-connectors/worker/fixtures/linkfox-sale-request.json`时ENOENT；既有workflow只checkout Skills，不含所需兄弟仓库。已只读取得父提交`25df87ea261a922881e6b74c640909fcfab0b6a3`的[CI run 39092233163](https://github.com/36Dge/yijie-skills/actions/runs/39092233163)，同样144通过/1失败且路径及错误一致。本次Skills仅改Contracts来源pin，未改该测试、fixture或workflow。

该缺口不作为本次预览/恢复功能回归，不关闭检查、复制fixture或改CI授权来伪造绿色。五仓源码普通push已完成并核对远端；元仓初次记录提交为ae0e477ef40a9095d92bfb05303e53ed0d6334b1，本补充证据作为后续文档提交保存。

同一失败测试在当前本地完整兄弟仓库环境中按精确名称定向执行PASS（1/1），未修改任何测试或fixture。其余仓库的chore分支按既有workflow规则不触发push CI；本地已执行的focused checks和真实验收不等同于远端CI通过。
