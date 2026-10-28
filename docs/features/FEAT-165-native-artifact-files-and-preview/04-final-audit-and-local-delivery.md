# FEAT-165 最终实现审计与本地交付

2026-10-29。Owner要求再次逐项核对需求和真实实现，修复遗漏/矛盾，全部完成验证后做本地提交，不推送。此授权覆盖本需求受影响仓库；元仓中已有FEAT-162改动保持不动。真实任务仍7/20，本轮审计不需要额外模型调用。

## 逐项复核

| 需求 | 实现依据与审计结论 |
|---|---|
| R-01 / AC-001 格式 | Native `attachment.rs`、Host `multimodal.go`与固定Contracts输入包装保持SVG/MP4的file身份；MP4仅描述已知元信息，不声称读取音画。12种正常样本逐件导入、登记、Native接收和原件保存已有真实证据。本轮再次运行正常12文件Host登记/ACK与Native往返。 |
| R-02/03 / AC-002/003 胶囊 | 复用YjIcon、tokens、NPopover和原导入流程；临时来源只绑定context/draft/attachment，不落库、不进Pinia/Host。图片投影复用有界解码和读租约；发送/移除/切换清理。此次发现两处键盘焦点问题，见下文。 |
| R-04 / AC-004 消息 | `composeConversationView`仅在同session/turn唯一local提交与唯一native userMessage时投影本地正文；附件保持独立产品记录，native对象不变。无本地绑定和多个native userMessage不猜关联；纯附件不造空正文。正常store分页/两次重开、实际Native两页和真实App重开维持通过。UI加载更多按钮仍未实测，沿用Owner明确接受的分层验收。 |
| R-05 / AC-005 预览 | MD扩展原有文本投影，Office/PDF保留信息卡＋保存；HTML隔离窗、图片/SVG与MP4播放器复用原能力。没有新增Office/PDF阅读器、转码器、文件服务器。已有逐格式真实UI、视频用户听音和亮暗最小窗口证据仍适用。 |
| R-06 / AC-006/007 保存恢复 | 同一publisher→encrypted spool→media事件→Native校验提交→ACK；保存仍用既有授权、原生面板和atomic写入。.jpeg保留后缀；预览失败不禁止有效原件保存。已Native提交正常重开，Host staged不承诺重启重投递。v42仅沿既有前向reader guard，不加表/路径字段、不迁移日常库。 |
| R-07 / AC-008/010 状态 | 原子批次、10件边界、取消/重选、已成功草稿/正文保留已有正常实测；本轮修复Esc后重开及键盘重试焦点丢失。没有扩大资源上限、权限或错误恢复协议。 |
| R-08 / AC-009 复用 | `yijie-codex`与Skills未改；Runtime Thread/Turn/Item、publish MCP、工具配置、spool/content/Range/ACK、HTML/图片/视频/保存全部沿既有机制。新MD/DOCX/PPTX只经显式v12准入，v9生命周期与原格式闭集保持；未开启K31禁用的dynamic tools。Host Office校验属于既有spool接纳边界，Native复用原OOXML preflight。 |

## 本次发现与修复

1. **Esc后Enter无法重开**：胶囊键盘处理直接调用`read()`，而该函数要求active已经为true；Esc关闭后焦点未移动，Enter会直接返回。改为未打开时发出原有activate事件，已打开时才读取/重试，不新建状态机。
2. **键盘无法进入重试按钮**：从胶囊移入浮层中的重试按钮会触发原blur关闭。改用focusout检查焦点是否仍在当前胶囊或其浮层中；真正离开才关闭，Esc仍关闭。原有失败状态组件回归证明问题；没有人为破坏真实资源或注入攻击样本。
3. **图标类型别名未对应不同图形**：原registry中JPEG/PNG、Markdown/SVG/HTML共用组件。仍使用现有Lucide依赖，为11格式族选择不同图形；jpg/jpeg继续共用JPEG。增加实际registry组件唯一性回归，避免只检查别名而遗漏相同图形。
4. **需求当前状态矛盾**：brief顶部仍写实施active/Must未通过，第5节仍标未来pending；03与长期记忆还写其它提交未授权，feature.yaml引用旧10.3节。更新当前状态和入口，保留02/03各阶段失败、NOT RUN及后续接受的时间顺序，不抹掉历史问题。

本次焦点/图标修复及文档补正`contract-impact=none`：只调整组件内焦点事件和现有图标映射，Desktop↔Host/native协议、持久状态与重放值不变。完整FEAT-165仍为breaking，继续固定Contracts `61137174a25dc368e0006f27633fd4a9ad097aa6`，不改源契约或userMessage。

## 验证与提交记录

本轮已通过：21项胶囊/类型/原生绑定专项、1项同源store分页与重开、9项Native正常格式/投影/保存/并发/reader/真实事件回放、Host正常12文件race回归与vet、8项Contracts专项及媒体/Connectors来源check、Desktop lint、Native fmt/clippy。首次新增测试使用ES2022 `Array.at`被现有TS目标拒绝，已改为兼容的slice后重验；没有放宽编译目标。最新canonical构建与实际UI复验通过：十种普通附件自然换行、实际图标可区分，CSV路径与PNG图片均可Esc关闭后在原焦点Enter重开；切回两轮历史仍三附件、无重复/空正文。1180×760亮暗实际布局通过，已恢复原浅色和窗口尺寸。错误浮层键盘重试由普通组件状态回归覆盖，不破坏真实文件制造错误。16份已另存原件再次逐字节/SHA-256核对一致。Design docs构建、57项治理测试、lint及严格D4/claim检查通过。

完整常规测试包含用户永久禁止的故障注入/攻击fixture，因此未运行；只执行检查过的正常样本与纯值状态回归。全量契约生成和跨其它族breaking仍有前序未解析引用，本次未声称全量绿色，也未削弱检查器。当前本机D4不代表生产发布、外部provider实测或日常数据迁移。

前序路径暂时不可用现象仍未确认根因；最终无诊断候选新导入、Esc及前后台切换正常，不为未复现观察添加猜测性修改。用户接受的历史分页限制不变。所有临时诊断已移除，退出一律正常Cmd-Q。

本次首个UI恢复尝试仅观察到设置页，未记为启动通过；正常退出后等canonical实际进程启动就绪，再选中完整bundle路径，最终进入真实聊天并完成以上复验。期间Mac锁屏已请求Owner解锁，没有绕过锁屏或强杀。最新候选正常Cmd-Q退出码0，之后固定本地提交来源。

## 提交来源复核

Host已本地提交`36ec8c62cca771b479b317d209da50d6acda0989`，Connectors已本地提交`ff436bb9bfe23297a1c5891a06fe6f6280c04e6d`，两仓工作树干净。现有`kimi-k31-build-candidate.mjs --freeze-commit`已将434份Host构建输入固定到真实commit；没有手改构建receipt。

首次提交后canonical构建被目录校验器拒绝：其精确HEAD仍要求旧Connectors `d88b8d0`。对新旧commit的`catalog/market-catalog.v1.json`执行字节比较无差异；仅更新原校验脚本的精确commit，并用两个原目录同步器生成来源manifest，两个`--check`再次通过，目录仍61项且未激活新provider。保留该首次FAIL日志；没有删除HEAD或Git对象内容一致性断言，历史FEAT-164整体验证脚本仍保留自己的原基线，不把本次提交当成其重新认证。

Desktop已本地提交`a2cc89c9cf2e36f8c5b9154e5694c38e601e140a`，共71个本需求文件。提交后的目录来源同步及canonical构建通过；详细检查与日志摘要见[最终机器记录](references/final-audit-20261029.json)。Contracts沿用已批准的`61137174a25dc368e0006f27633fd4a9ad097aa6`，不重复制造提交。

最终在上述本地commit来源上完成canonical同构建重开：十份合成草稿恢复，切回FEAT165_F两轮仍为SVG/CSV/TXT三份附件、单份原文，无空白气泡或自动派发。源仓均干净，真实任务仍7/20，未推送。本页、完整需求包、机器账本和元仓长期记忆由同一次仅FEAT-165本地文档提交交付；元仓FEAT-162并行工作保留，不混入该提交。

本需求10项Must按已明确范围通过，无剩余授权内实现工作。历史UI分页按钮未实测、完整其它契约族未全绿、Office/PDF预览深度与Host staged恢复等边界维持原记录，不扩大为生产发布结论。
