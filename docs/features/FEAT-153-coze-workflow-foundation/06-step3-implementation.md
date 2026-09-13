# FEAT-153 第 3 步：源契约与最小服务端、原生会话桥接

日期：2026-09-12。用户本轮明确要求“执行第3步后：先定义源契约，再实现最小服务端与原生会话桥接”。本步严格按源→生成/校验→consumer 实现→联审顺序执行。第3步源码、标准构建和定向验证已完成；真实独立栈、migration、React editor 和 canonical App 验收属于后续步骤，D4 保持 NOT RUN。

## 契约先行

权威为 `yijie-contracts/openapi/workflow-local/workflow-local.yaml` 和引用其 DTO 的 `jsonschema/workflow-editor/bridge-v1.schema.json`。现有 Public、Chat、Host、Runtime 源未改，API 旧 public-api.lock 未换。整体 contract-impact=semantic，采用独立 local opt-in 族，版本 `1.0.0-local-candidate`。

初轮源和 Go/TS/Rust/schema 生成完成，6 项源测试通过后，API/Coze/native 才进入实现。实现联审发现列表携带完整画布/运行内容会超过总消息预算，先修正源为 WorkflowSummary/RunSummary，再重生成同步三端；详情仍保留完整数据。随后新增 bridge TS 同源生成、正常 generate/validate/check-generated 入口、来源校验和第7项摘要测试。

本地来源锁如实记录真实 base commit、源/generator/生成物 SHA-256 和 `release=false`；没有虚构契约合并、tag 或 immutable candidate commit。跨仓复制仅由源仓 sync 脚本完成，三个独立 consumer lock 不覆盖旧锁。候选合并前仍须 Contracts 先合并并由下游 pin 完整不可变提交。

三次结构 breaking check 的固定基线为 `811f38d6b104fa18477107e7ac91a85e19c445d1`（本族首次新增 fallback）、`f16a497e1377f45747f8ff9292b4b60cf2027f88`（已发布支持版本）、`29317b6426578749dc698fc2ad32b986ee5c8e9f`（API 旧 pin），均 PASS。本族在这些基线均不存在；检查同时保护已有族，不将结构检查解释为真实业务运行。

## 本步实现边界

| 仓库 | 实现位置与职责 |
|---|---|
| Contracts | 独立 HTTP/IPC/MessageChannel 源、生成类型/验证投影、来源锁、安全生成/漂移/兼容检查 |
| API | 独立 workflow-local-server、固定 scope、PostgreSQL 资源/操作/审计映射、私有 Coze client、300秒 E；旧 api-server/OIDC 不改 |
| Coze | 私有 localadapter 和独立 command，真实领域引擎；Coze 内部事务负责 CAS、成功试运行证明、内部版本、operation/run/slot 原子关联和真实历史 |
| Desktop | workflows 原生模块、8个具名命令、固定身份权威、owner-only机密、E/epoch/generation、固定 HTTP；Vue/CSP/iframe 本步不接 |
| Infra | 本步未改；第4步消费服务仓配置 schema、独立migration与正常停止约定 |

服务不接受 renderer actor/tenant、任意 URL/header/原生命令；K_NA/K_AC 分离，E 不进入 renderer、不转给 Coze。列表/创建/首次打开/运行查询独立于编辑绑定；关闭或到期只撤销编辑能力，不宣布真实运行取消。运行只允许三类节点和已冻结的大小、单槽位、合作式预算。

## 联审记录

以下是工程代码审阅，不能冒称独立人工批准；以下修正已关闭并有正常场景定向测试；真实数据层和平台资格另行验证。

1. 列表超限：在源层新增摘要，三个消费者同步，详情独立读取。
2. Coze runner 静态配置为空时仍须使用本地30秒预算，旧模式保持原行为。
3. NodeResult.output 应投影真实文本，不能把内部 JSON 外壳当作5120字节文本返回。
4. 写入副作用已完成但响应构造/详情查询失败时，必须返回携带原 operation_id 的 unknown，不能当作确定未执行。
5. Coze HTTP 五个写端点必须遵守源的 Workflow/Run 响应与201/200/202状态，operation receipt 通过独立查询保留。
6. 原生open在首次await前绑定context revision，关闭/epoch/上下文失效后的迟到结果正常撤销，不恢复已关闭会话。
7. 凭据正常读取使用 owner-only 边界；native测试的合成token在运行时生成，秘密不经过renderer；容器监听与宿主loopback显式区分。

## 已有验证

Contracts：安全全量生成、完整lint、7项工作流源测试、全量safe生成漂移检查、三个固定baseline breaking均PASS。11条lint warning中9条来自由native/bridge使用的IPC-only组件，保留lint规则；生成入口只新增namespace导出，旧源及SDK字节保持。8份用户原有Desktop修改文件保持不变。

具体命令、逐仓 focused tests、实际结果、源码保护与未执行项在 [02-verification.md](02-verification.md) 和 evidence 第3步附件落账。编译/单测不等于真实Coze三节点执行。

## 尚未执行的范围

- Docker/受控栈、真实PostgreSQL/MySQL migration、服务持久化联调：第4步。
- 同一App内React editor、MessageChannel/WKWebView资格、Vue产品接入与视觉检查：第5步。
- fresh canonical happy path、普通错误修正重跑、真实历史与正常停止重开：第6步/D4。
- 默认历史攻击/危险归档/权限故障测试：按用户永久规则不执行，使用safe/focused路径，不宣称全仓测试通过。
- 模型、商家、平台、付费调用为0；无commit/push/tag/远端创建、公开部署或数据删除。

## 第3步完成结果

| 范围 | 实际结果 | 证据 |
|---|---|---|
| Contracts | 7项定向测试、安全全生成/漂移、全lint、三baseline breaking、三consumer摘要PASS | [检查索引](evidence/step3-checks.json) |
| API | 16项顶层tests与9项路由子例，race/vet/标准两进程构建PASS；无真实PG | [API报告](evidence/step3-api-implementation.md) |
| Coze | 9项正常tests、race、vet、标准构建PASS；真实引擎+SQLite/miniredis验证最大输出及发布v2后执行v1 | [检查输出](evidence/step3-coze-focused.txt)、[race](evidence/step3-coze-race.txt) |
| Desktop | 10项native定向tests、check/fmt、生产lib严格clippy及consumer检查PASS；无App | [native tests](evidence/step3-desktop-native-tests.txt) |

Desktop严格clippy包含tests时被既有 `src/chat/mod.rs:1351` 的 `cloned_ref_to_slice_refs` 阻挡；未改Chat。这项失败保留，不能写全目标clippy PASS。

两个Go服务及API migration开发产物均为项目canonical构建，未启动。第3步没有改Vue/CSP/Infra，没有commit/push或发布。下一技术步骤是第4步：固定受控local栈、显式独立migration、真实readiness与正常退出，再推进第5步编辑器。

独立跨端收尾复核见 [step3-cross-boundary-review.md](evidence/step3-cross-boundary-review.md)，其普通三节点路径/13项私有HTTP操作与部署输入对照已完成；真实MySQL事务仍待第4步。

第4步部署输入已明确：容器设置 `YIJIE_WORKFLOW_NETWORK_SCOPE=container`，Coze另需显式
`YIJIE_WORKFLOW_COZE_LISTEN_ADDR=0.0.0.0:18889`（默认仍为宿主loopback）；Coze `MYSQL_DSN`
必须指向 `coze_workflow_local`、固定服务DNS，并带 `parseTime=true`。容器USER须与机密文件UID一致，
仅API发布宿主 `127.0.0.1:18888`。这些是后续配置要求，本步没有执行部署。

最后的正常时间边界复核确认源不要求宿主与容器严格同钟；native保留服务端expiry，同时以请求开始后的单调时钟300秒封顶。已获会话后的任何安装失败统一正常DELETE，新增纯时间计算测试，不修改系统时钟。

另修正重复内部发布的MySQL语义：若同一revision的发布标记本来就相同，更新返回0个changed rows时，在原事务锁定当前id+revision确认；存在则继续分配新内部版本，不存在才报冲突。没有改clientFoundRows配置。正常同revision再次发布与MySQL dialector/sqlmock检查覆盖此分支；真实MySQL行锁仍留待第4步。
