# FEAT-153 跨仓交付差异与顺序

2026-09-13。此页保留跨仓交付顺序。用户已于2026-09-13明确授权FEAT-153提交/推送，实际执行见18；远端创建需用户另行指定。当前本地D4已通过，最终结果以17和feature.yaml为准。

## 差异归属

| 仓库 | FEAT-153交付内容 | 必须保留的边界 |
| --- | --- | --- |
| yijie-contracts | workflow源OpenAPI/共享消息、schema、Go/TS/Rust派生物、限制/错误/版本语义、来源锁、正常conformance与baseline检查 | 权威源先行；当前local_candidate不是已发布tag；旧public/Chat wire保持 |
| yijie-coze | 上游来源锁和易界接入治理；专用local服务、私有映射/migration、合成三节点执行、编辑器独立构建与键盘等效编排；已登记原生执行注册/合作式预算overlay | origin现为用户授权的私有36Dge/yijie-coze，upstream保留coze-dev；不向上游推送易界修改；六份原缺失文档属于既有状态；保留上游构建和许可证 |
| yijie-api | 固定local scope、资源授权、300秒会话、operation/receipt/audit、PostgreSQL migration、专用静态editor入口、Coze适配与合成资格工具 | 凭据仅native/server；不复制Coze数据主状态；旧OIDC/Chat业务语义保持 |
| yijie-infra | 独立Compose project、固定镜像/候选、私有机密生成、显式migration、宿主认证readiness、正常stop/reopen和保留卷 | 只发布loopback18888；不启动完整上游栈；不把API edge网络描述成禁止全部出站 |
| yijie-desktop | 标准dev/packaged入口装配、具名native工作流客户端/短会话、有限MessageChannel、Vue真实列表/编辑/运行历史、原生关闭/尺寸诊断、取消导航标题修复 | 不新增第二身份系统、不改Codex Runtime；renderer与iframe不获得E/机器凭据；用户原设计改动须按来源区分 |
| yijie | 十二仓清单、Accepted ADR-0019、架构/治理、FEAT-153源/部署/真实验收和交付记录 | 元仓只保存治理与证据；不能代替其它仓实现提交或CI |

冻结记录包含完整git status（含untracked），不只依赖git diff --stat；后者不会显示新增目录。交付审查应同时覆盖新文件和tracked hunks。

Desktop既有设计文件保持原字节，不归作本需求新实现。交付检查发现真实控件依赖原有workflow-showcase.css与YjPageHeader描述插槽，这两份作为具名既有依赖随交付，其余五份纯设计文件留在工作区。WorkflowPage通过恢复前序文件且SHA256与审计快照完全相等确认归属，再仅暂存FEAT-153接入；已对暂存快照执行类型检查、21项测试和构建。具体残余差异与验证见18，不能按整个文件推断归属。Coze六份原缺失文档同样不能被宣称为本需求删除或擅自恢复。

## 后续获授权后的提交顺序

1. **Contracts源与派生物**：先形成权威源的不可变完整commit，核实正常生成、同源、适用baseline与限制语义。尚无正式发布tag时明确标local候选。
2. **Coze与API provider**：按该Contracts完整commit更新各自consumer来源记录，重新检查派生物一致；分别形成可审查提交。Coze部署先于API转发激活，API必须ready后客户端才调用。正常expand migration与旧数据保持策略随实现交付。
3. **Infra装配**：固定已经形成的provider来源和真实构建摘要，保留专用服务、端口、readiness、正常停止与数据卷策略。
4. **Desktop consumer**：固定同一Contracts来源，核验标准dev/packaged构建、生成消费和native/Chat边界；仅加入本需求的实现与已归属修复。元数据更新如导致内容摘要变化，应记录并复核其实际影响，不沿用不匹配的候选摘要。
5. **元仓最终记录**：引用每个实际提交、D4结果和已知限制，记录清单/来源/兼容及必要回滚顺序。提交与推送分别记录；CI、merge、tag、public/production不从本地D4自动推导。

用户已于2026-09-13明确授权新建私有36Dge/yijie-coze，实际创建/推送与来源保持见18；未向Coze上游推送。

## 回退与清理

本期回退为关闭exact-local工作流功能、正常退出App并canonical stop专用栈，保留既有数据库卷与审计。新建草稿/内部版本/历史不以回退名义删除；不降级写入不兼容schema、不重置数据、不强杀进程。原Chat运行边界沿用原平台，不把工作流撤回扩展成Chat迁移。
