# S4K 已批准续期与真实验收

Owner先批准36提案新增1次，随后直接补充“可以额外新增2次”；按在1次之外另增2次记录并已向Owner明示，本轮最多新增3次、累计5次，金额上限仍30元，输出8192、失败即停、无自动重试、本次不使用搜索/图片。旧2/2、unknown预占和历史均保留，不推送、不迁移日常库。授权回执只记录真实本会话批准，不代表模型已调用。

本轮contract-impact=semantic：私有验收账本schema3及只读判定器新版本，旧schema1/2解释和旧文件不改；不是产品wire、SQL、权限、Runtime或公共契约变更，整项breaking不变。新后继文件绑定旧账本SHA、完整旧状态和两行摘要，创建幂等且有源/目标文件锁。旧账本停止态保持。每次先预占、全模型请求统一计数、串行、任何HTTP/terminal/usage失败即停；已结算成功才释放保守差额。重开不续额，不承认新增unknown。

先普通内存/临时文件测试(无真实调用)，审计来源并仅本地固化；新物理sibling资格目录中canonical构建保留旧bundle。以dummy key普通loopback完成新构建正控、正常退出及账本恢复资格，再从已有owner-only Kimi key启动真实meter与同构建App。首先发最小42文本；仅成功且仍有明确余额/次数才按需要验证续轮/重开，不为用完额度调用。正式账本不用于测试fixture，旧未知线程不恢复或换ID。

当前官方首页2026-10-26仍列K3.1 Pro输入/默认缓存写13元、输出68元每百万token；Responses端点仍api.moonshot.cn/v1/responses。沿13/68保守费率，缓存命中按全价输入；单次预占14.188544，旧上界14.328134，单次在途合计28.516678<30。来源：https://platform.kimi.com/ 与 https://platform.kimi.com/docs/api/responses 。官网额外能力不扩本次验收范围。
