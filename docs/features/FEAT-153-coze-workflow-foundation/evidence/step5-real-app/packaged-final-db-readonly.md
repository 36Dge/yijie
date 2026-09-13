# Packaged final resource — read-only database observation

2026-09-12，独立 packaged 资源 `7684605114128007168`，epoch
`bdc6b8e8-0314-4a7d-9e33-f0ea4902c54a`。完整事实与诊断源码分别为
`packaged-final-db-readonly.json` / `.py`；没有复用 dev 资源或覆盖先前快照。

本轮一次受控读取：MySQL 快照 **11:18:53.683725–11:18:53.744078 UTC**，
PostgreSQL 快照 **11:18:53.744121–11:18:53.799995 UTC**。根代理在此期间不再修改内容；
两库仍是各自的只读事务，不是分布式原子快照。

观察匹配根代理给出的 packaged 最终事实：

- 名称 `FEAT-153 Packaged App 验收 20260912-1912`，revision `7684605840325607424`。
- 开始 `100001` `(80,160)`；文本 `200001` `(452.5842696629214,111.68539325842696)`；
  结束 `900001` `(760,160)`。文本前缀 `Packaged 中文验收：`。
- 三节点，两条已保存边 `100001→200001`、`200001→900001`。
- UTF-8 canvas **1103 bytes**，SHA-256
  `816b358192a921523e9ac4e8d821890914f5e2fc745bd0d12104f5a64658c93c`；
  显式 utf8mb4 客户端字节与 hash 同数据库 `OCTET_LENGTH/SHA2` 严格一致。
- PG/MySQL 固定 scope 身份相同；均 **1 create + 1 save**，规范化 receipt 字段一致且
  completed。create `01a09551-b49a-7800-b2df-5ac70766494f` 的 revision 为
  `7684605114132201472`；save `01a09554-48f9-7420-96e8-bcbc40740217` 的 revision
  为 `7684605840325607424`。旧操作 revision 未被最终草稿覆盖。
- 该资源 PostgreSQL audit 12 行；versions=0、executions=0。

使用原厂 Docker CLI、独立 config、controller lock/validate_owned，核验数据库精确镜像、
内部网络和 readonly 私文件挂载。只在容器内 stock mysql/psql 消费密码文件，密码不进入
host 输出、argv、证据或导出的环境。查询严格限该资源/固定 scope，临时 client 文件正常
清理。没有 HTTP、业务写入、迁移、启停、权限变更、故障/攻击测试或日志 dump。

读取已结束并释放 controller lock，已明确通知根代理可以正常停栈。此文件证明持久数据
一致性；真实 UI、runnable、返回重开和原生 stderr remote_closed 的观察由根代理另外
关联。本数据库快照没有 session 记录，不能独立证明 App E close；JSON 中该项保留
`NOT OBSERVED`，不会冒用根代理尚未关联到本文件的日志事实。
