# Step 5 — dev App single-resource database observation

2026-09-12，固定合成资源 `7684595660317786112`，epoch
`bdc6b8e8-0314-4a7d-9e33-f0ea4902c54a`。仅作数据观察，**不表示完整 UI、连线、运行或
App E close 通过**。根代理随后仍可在 UI 保存；下列 revision 不是最终版本声明。

正确 UTF-8 结果见 `step5-dev-app-db-readonly.json`，执行源码见同名 `.py`。
MySQL 快照范围为 **10:50:52.952242–10:50:53.009361 UTC**，随后 PostgreSQL 快照为
**10:50:53.009403–10:50:53.063409 UTC**；两库不是同一分布式事务。

实际观察：

- scoped 资源在两库均唯一，API coze_user/space 与 MySQL creator/space 相同。
- 当时 revision：`7684598045123543040`。
- 当时名称原样为：`FEAT-153 Dev App 闭环 20260912-1840FEAT-153 Dev App 闭环 20260912-1840 自然到期`。
- 三节点、零条已保存边。开始 `100001` 坐标 `(80,160)`；文本 `200001` 坐标
  `(470,131)`，前缀 `真实 Desktop 验收：`；结束 `900001` 坐标 `(760,160)`。
- canvas UTF-8 为 **975 bytes**，SHA-256
  `cc7549f98d9a24a03c403089d503ff9a5b5ebc65b155490de36acd4a10ab2b3c`。
  客户端结果与数据库直接 `OCTET_LENGTH` / `SHA2` 严格一致。
- PG/MySQL 各有一个 create、两个 save，三个回执均 completed，逐 operation 按语义
  归一后的关键字段一致；PG audit 查询返回 19 行，其中包括普通读取审计。
- 该资源当时 version count=0、execution count=0；不把根代理之后尚未保存的 UI 连线
  混入这一快照，也不要求整个保留数据集无历史运行。

| operation | kind | 本操作 revision |
| --- | --- | --- |
| `01a09530-1e63-7463-901f-36df42813e37` | create | `7684595660326174720` |
| `01a09535-fce7-78e1-984b-b2bb56544b34` | save | `7684597312391217152` |
| `01a09538-9748-73a0-981f-64544548bf42` | save | `7684598045123543040` |

连接只使用 Infra 原厂 Docker CLI、独立匿名 Docker config、现有 controller lock /
validate_owned。核验精确 image、epoch、internal network、readonly 密码文件挂载后，
容器内 stock mysql/psql 读取私文件生成临时 owner-only client option/pgpass 文件；密码
不进入 host 输出、argv、证据或导出的环境，临时文件由正常 EXIT trap 清理。查询只在
专用库、固定 scope/资源的只读事务中执行 SELECT。MySQL 结果字段
`session_default_read_only=0` 是会话默认值；实际脚本明确用
`START TRANSACTION WITH CONSISTENT SNAPSHOT, READ ONLY`，不是把默认值写成 true。
没有业务写入、迁移、启停、权限破坏、故障注入或日志 dump。

**保留的初次读取问题：**诊断共执行四次。前两次读取被额外的旧名称前缀假设挡住；
身份约束随后明确为已授权的 exact workflow ID + fixed scope，允许正常 UI 改名。
第三次产出后发现 stock mysql 客户端未显式选择 utf8mb4，中文 name/prefix 被转为 `?`，
其 canvas 字节数/hash 因而不可靠。该原始结果和当时执行源码分别原样保留为
`step5-dev-app-db-readonly-initial-encoding.json/.py`，不能用于文本/hash 验收。
第四次明确 `--default-character-set=utf8mb4`，并增加数据库侧字节数/hash 对照，产生
当前正确原名 JSON；没有覆盖或伪报初次结果。

API session 仅在内存 map，无 session SQL 表或专用 close audit。本观察不能证明
本次 App 的 E 已撤销；该项在 JSON 明确为 `NOT OBSERVED`。执行已完成并释放
controller lock，根代理可以继续原定正常 UI/生命周期流程。
