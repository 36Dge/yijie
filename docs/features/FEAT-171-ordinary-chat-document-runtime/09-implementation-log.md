# FEAT-171 实施记录

2026-11-09，Owner确认需求、技术方案和ADR-0024并授权实施。沿已确认breaking范围、原生复用与安全条款，只运行相关验证。真实模型额度0，提交/推送/发布未授权。

## 来源保护

原始产品仓HEAD及dirty以references/source-audit.json为基线。开始时产品仓干净，Contracts已有.local/保留；元仓已有本Feature和ADR文档改动保留。本轮不覆盖已发布/受审二进制，标准新源码构建只写独立内容寻址候选。

## 顺序

原生cooperative_only→canonical配置/兼容投影→文档能力源契约与生成适配→自有专用环境及CLI→Host接入/ACK查询→Native渲染/查看器/正常安装→无计费定向验证→提交可审阅候选后单独申请真实模型额度。

## 结果

已完成首期工程实现与定向无计费检查，完整产品AC/D4仍未宣称通过。真实模型请求0；没有提交、推送、安装到日常入口或发布。实际构建与原始日志索引见 [implementation-checks.json](references/implementation-checks.json)。

### 工程落点

- yijie-codex：0024新增可选cooperative_only，保有进程/输出拥有权、正常中断/关闭及STOP_PENDING；旧上游源和旧二进制保留。新canonical Runtime已构建，app-server wire不变，配置schema与Contracts精确配对。
- Contracts/Host：同源生成文档环境、bundle和ACK状态契约；既有artifact MCP增加两个只读工具。环境缺失不回落系统，也不让普通文本聊天因文档依赖缺失而失去Host；状态只取同代际Native ACK。修正了最初装配中“在Service构造前赋值”的问题，并用真实MCP桥接和会话测试覆盖。
- Desktop：独立CPython3.12.16、十二个固定Python包、LibreOffice26.8.2、私有中文字体和共享Quartz CLI；通用创建/解析/重算/渲染助手、九份内置指南。源版本和每文件摘要固定；自有Python不携pip/ensurepip/Tk/IDLE/venv，不指向系统环境。
- 输入与交付：上传原件的私有副本受原outbox/会话绑定、SHA和期限约束；同会话已提交的最近原件可在缓存过期后从主存储恢复，不改旧请求摘要。JSON原件与receipt分名。沿现有v12产物流、Native存储/ACK/7天保留，无数据库迁移、版本树或执行ledger。
- 预览：DOCX/PPTX版式与正文切换；XLSX数据表与图表版式切换；长文本/CSV有界继续。版式不可用时明确展示正文投影。预览/模型QA共用转换锁和有界派生缓存；退出等待正常工作收尾。
- 装配：新增完整Tauri本地包入口，内含Host/Runtime/MCP/全部文档资源，启动代码不依赖源码、系统开发工具或Docker。源码开发入口可选择同一清单，保持原日常Homes。安装包不把原开发历史自动配给空的新Homes。

### 实际样本暴露并解决的兼容问题

1. PPTX的正常书签含`/Prev`兄弟引用，旧PDF检查把它误当xref增量链；现在只检查trailer的Prev，xref/加密等既有边界保留。
2. python-pptx的正常模板携带打印设置`.bin`；旧Native/Host全部拒绝。现在只接受限定路径、64KiB内且匹配printerSettings声明的数据，宏/OLE等其他二进制仍拒绝。
3. 普通图表PNG在PDF内具有较高压缩率。图像保留8MiB解压和40M像素/边长限制，文字流保留100倍比率；不把合法扁平图表误拒。只使用真实生成的普通图表验证，没有攻击压缩fixture。
4. 可编辑PPTX图表含嵌入XLSX数据包；助手现在允许该受总解压预算约束的数据包，不允许嵌入程序/递归包。外部查询、宏、受限外部域和支持集外公式在转换前拒绝；Calc/Writer链接更新分别按上游枚举设为1/2。
5. macOS原生workspace沙箱不包含Office所需平台IPC。助手先给出明确审批需求，走现有原生单次命令审批，未自动开放网络/更改沙箱或交给Host执行；真实Runtime回环已验证批准后的转换及原生view_image。
6. Tauri通用资源复制会改变嵌套框架符号链接。规范构建脚本在新生成、未签名的项目输出内按原始链接重装配资源，并用Host全清单验证把这个问题纳入打包门禁；旧用户程序和已审计产物未覆盖。

### 已完成的检查与实际边界

- 原生PTY正常完成/协作取消2项；真实Runtime本地回环的正常执行、取消、关闭，以及专用Python→原生单次审批→Office→Quartz→原生view_image。
- 文档源契约严格校验、两族生成无漂移、三个契约用例通过；相对固定fallback的42个既有JSON Schema无结构破坏，旧publisher源逐字不变。未以此冒称所有跨版本语义都自动证明。
- 真实MCP适配器的工具声明/私有thread-turn元信息；真实Host spool的九格式登记/资源/ACK；Native SQLCipher九格式提交、原件另存、正常重开字节一致。
- Native分页/UTF-8/CSV/合法PDF/JSON副本/空容器/同会话恢复定向检查；前端契约与状态25项、阅读模式2项，相关lint和类型检查通过。
- 从完整应用包内的解释器/库/转换器路径运行九格式与可编辑图表、中文字体、公式重算、全页PNG检查通过。基础及丰富样本9张页图经原生看图工具检查；事实核验与视觉检查分开。
- 当前依赖包约375MB压缩、992MB展开；完整应用约1.5GB展开，精确数值在机器记录。一次包内九格式/图表检查16.05秒，`/usr/bin/time -l`报告最大RSS约252MB；这是当前机器的普通样本观测，不代表最低macOS14/8GiB或整机峰值资格。
- 314个Mach-O加载命令审计未发现非系统绝对加载依赖，最低系统声明未超过14；不把LC_ID_DYLIB的上游构建标识当实际加载路径。官方LO对应源码四个归档、Python包源码及原许可证已保留；完整发行资格/签名仍属后续门禁。

真实Kimi/MiniMax、实际客户端GUI亮暗/最小窗与保存面板、干净用户/最低系统、安装升级回退和同次fresh D4未执行。危险/故障注入项按永久安全条款排除；保留替代证据范围，不伪造通过。

### 后续已授权Kimi验收更新

上文“真实模型未执行”保留无计费阶段时点。后续Owner批准30元/80次并最终限定Kimi，已完成九格式生成和四类上传修改两场景，62次请求、13个committed产物。首屏超时、原生看图展示、开发入口Runtime选择顺序及定向生成入口的修正均见[11实际记录](11-real-model-acceptance.md)。文档包和完整应用候选已更新，最新摘要见[真实验收机器记录](references/real-model-checks.json)。当前亮色/最小窗口/保存面板及正常重开通过；完整D4仍待干净安装、最低平台、升级回退与深色GUI，不包括已被Owner排除的MiniMax验收。
