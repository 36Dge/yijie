# Dev final resource — read-only database observation

2026-09-12，workflow `7684595660317786112`，epoch
`bdc6b8e8-0314-4a7d-9e33-f0ea4902c54a`。结果为 `dev-final-db-readonly.json`，
诊断源码为同名 `.py`。根代理在此读取期间暂停修改该资源。

本轮执行一次受控诊断：MySQL 只读快照 **11:00:18.590803–11:00:18.651132 UTC**，
PostgreSQL 只读快照 **11:00:18.651179–11:00:18.705901 UTC**。二者不是分布式原子快照。
沿用原厂 Docker CLI、独立 config、controller lock/validate_owned、精确镜像/内部网络/
readonly 私文件挂载校验；密码仅在容器内消费，不进入输出、argv 或证据。

观察与根代理指定的最终 dev 资源事实一致：

- revision：`7684601577516040192`；名称：`FEAT-153 Dev App 验收 20260912-1840`。
- 开始 `100001` `(80,160)`；文本 `200001` `(405,91)`；结束 `900001` `(760,160)`。
  相对中途快照文本位置 `(470,131)`，保存后的差值为 `(-65,-40)`。
- 前缀：`真实 Desktop 到期重连：`；两条保存边为 `100001→200001`、`200001→900001`。
- UTF-8 canvas 为 **1079 bytes**；SHA-256
  `2d2236353cdb83e3b0663d254fc1f9eccbc7462948ee0c9b495dd56489947f0c`。
  显式 utf8mb4 客户端读回与数据库 `OCTET_LENGTH/SHA2` 严格一致。
- PG/MySQL 固定 scope 身份一致；各有 **1 create + 4 save**，五个规范化回执关键字段
  均一致、completed，且保持各操作自己的 revision。最新 save operation 为
  `01a09545-2402-7c20-986b-d461d3736ecd`，revision 对应该最终草稿。
- PostgreSQL 查询获得 33 条该资源/其真实 operation 的 audit；该资源 versions=0、
  executions=0。创建/保存没有被误记为运行或发布。

本轮只读数据匹配检查均满足；没有 HTTP、业务写入、migration、启停、权限改变、
故障/攻击测试或日志 dump。controller lock 已释放。之前的中途快照与错误编码结果
完整保留，没有覆盖。

**范围限制：**本文件只证明上述时刻的持久数据；不能单独证明鼠标交互、视觉布局、
自然到期时画布保留、Chat 切换或 packaged App。API editor session 仅在内存 map，
本次 App E close 在数据库中不可独立观察，JSON 仍明确 `NOT OBSERVED`。
