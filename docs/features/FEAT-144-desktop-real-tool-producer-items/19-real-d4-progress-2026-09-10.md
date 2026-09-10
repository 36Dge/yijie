# FEAT-144 真实 D4 进度（尚未关闭）

当前已从普通canonical入口完成一次真实Sorftime查询和一次同会话原生Prompt拒绝。完成与来源以真实Runtime事件及原生thread/read为准；D4尚未关闭，AC-004继续OWNER_EXCLUDED/NOT RUN。

实际源码为Contracts `db54c617c65db5431b950eb297ba148a43a8e600`、Host `635846f72ef4b0d940798215e7b79d58aed6c591`、Desktop `95afd425fd5b55ada9f13b43421ad2c06830dc5c`；最低兼容reader仍为 `25b004fbd5a4dcf642a503d302c21a7d6e3b817f`。均只本地提交，Codex Runtime未修改。

## 真实结果

- 有效验证项目为CrossBSD/.local/feat144-d4/scenario-project，普通合成目录，单个公开ASIN/US。第一次位于Desktop仓库内的目录被固定Runtime拒绝：仓库.codex/config.toml含不支持的workspace字段。该失败发生在线程创建前，没有模型/MCP请求；没有修改仓库配置或绕过门禁。原记录保留，其本地投递失败仍显示等待提交，是现存界面限制，不包装成成功。
- 有效项目的原生初始化与唯一工具/schema核验通过，分别消耗第9、10次元数据操作。原生Prompt明确显示sorftime/product_detail和实际ASIN/US，批准本次后Tool原生completed、耗时342ms；助手显示所请求的三个公开商品字段，后续原生历史独立返回值核对通过，见20。
- 原始结果文本被既有安全规则整体脱敏；Tool仍保持completed，availability=partial及content_redacted明确显示，resultSummary仍只有结果元信息。没有为了展示正文放宽安全边界。
- 同一原生线程第二次Prompt经正常拒绝，Tool为原生failed、duration=0、result=null，Turn正常completed；没有第二次Sorftime业务调用或重试。此项是权限回归，不是AC-004业务失败场景。
- 源协议v2/SSEv8、唯一NativeDisplayBuffer、SQLCipher及原生thread/read继续复用。原生读取确认两条Item ID和各自终态；冷历史itemsComplete=false和缺phase未被补造。

## UI与兼容

普通启动、旧会话切换、Command成功/失败历史输出、既有图片Artifact预览通过。过期附件、旧清理未完成、隔离历史缺Host权限映射保持真实提示。原生Tool安全复制只得到脱敏展示文本，粘贴后已清空且未发送；键盘Shift-Tab定位Tool、Return展开通过。通过原生窗口操作到1180×760，检查light/dark与200%滚动可读，已恢复原浅色和100%。

## 调用与剩余工作

模型实际4/8次，均由原计数器记录HTTP200；元数据10/10；图片0。业务只有1次批准后的逻辑调用，实际HTTP级尝试数没有独立观测，按固定原生重发上界保守扣2/10，剩余可用8次尝试；不能写成确定1次HTTP调用。

后续当前临时权限切换已获授权，auto切换在旧Runtime正常退出后因受管配置漂移而失败，模式保持ask；full未尝试。原生历史返回值核对通过，应用/Host/Runtime/计数器均正常退出，普通Tool重开未验证。最新结论见20，D4未关闭。不能为重连自行追加元数据额度，不能继承其它需求授权。当前实际证据见[real-d4-progress](evidence/real-d4-progress-2026-09-10.json)。
