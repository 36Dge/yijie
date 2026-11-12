# FEAT-173 方案自审（修订2）

修订1的自审未充分识别ACK恢复扩张和无句柄恢复缺口，已撤回相关“闭环”表述；原文保存在references/plan-revision-1.json。此次发现、源码依据与改动见08。以下为当前候选自检，不是独立人工批准或实施验收。

| 检查点 | 修订2决定 |
|---|---|
| 原生复用 | MCP/搜索/Code Mode/审批/取消/模型预算保持；150s是配置，不是能力上限；next_action不冒充Runtime自动执行 |
| 持久状态是否必要 | 只存原root→供应商ID及一次交付标记；复用既有root ID和session cleanup，不存ACK/manifest，不建独立配额/TTL守护 |
| 句柄丢失 | get可定位当前root或同聊天唯一未决；歧义只返回本地候选，不能猜最新/查账户列表 |
| 跨轮防重 | 同root预占之外，同聊天未决时跨root也拦截新创建；首期并发独立需求用新建任务 |
| 停止与恢复 | 创建身份与当前观察context分开；每次网络/锁后/交付前检查；local stop不等于远端cancelled，不自动DELETE |
| Artifact复用 | 一次生产者交付后只查原Store；无ACK/Status/Native恢复修改、无spool重建；Host unknown不否定本地Native ready |
| 专家隔离 | 原持久绑定/revision、原Idle条件及Runtime排除；恢复也重新鉴权，旧许可/旧工具历史不能兜底 |
| 凭据与参数 | 原Keychain条目/作用域/解析器；模型固定且可选参数省略；不复制Key，不开放用户设置或CLI绕行 |
| 输入范围 | 仅文字与本轮图片；首尾同图复用索引；不扩视频/音频参考、编辑、延长或素材库 |
| UI与资格 | 现有MP4/64MiB/Native播放保存；实际默认有声视频和运营资格尚未验证 |
| 授权边界 | 只改方案，无产品实现/构建/应用启停/Keychain访问/真实调用/Git操作 |

方案明确承认：POST无ID时无法凭空找回远端任务；handoff后Host重启无法承诺自动补领。它们必须返回可理解的不确定状态并禁止重复付费，不能用影子ACK或重复生产掩盖。其余未知项有明确验收安排，产品AC全部pending。

## 对话流交付补充

后续只读追踪确认播放器与保存command已存在，但还需将新生产者接入事件、Native提交和projection/reference双刷新，并验收实际播放。ChatArtifactShell通用失败文案会引导video重新提交，需要本期最小修正。已同步04/05/02及09；这不是新增播放器或恢复状态机，产品实现仍未执行。
