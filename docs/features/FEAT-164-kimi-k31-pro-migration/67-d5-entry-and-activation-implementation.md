# FEAT-164 D5 日常入口与启用实施

2026-10-27。Owner要求审计后执行并完成D5，修复阻塞；已开始隔离实现。当前尚未启用真实D5，0模型调用。D4通过记录66保持，原工作区/账本/预占保留，仅本地提交。

## 已定位阻塞与最小方案

F61-02：schema1最长24小时且始终零派发，不能用于长期日常入口。新增schema2独立激活policy，绑定精确回执、原Home、D4与本次预检、Owner批准；每次继续原canonical source/artifact检查与workflow ready。仅安装新的用户Desktop `.command`入口，不覆盖App。D3/D4原门禁保持，Native/Host/Runtime产品源码不改。

F61-03有两层：validator错误强制public；ADR-0018第8条还明确禁止production_hardened免登录。已准备保留完整生产链的validator回归和[ADR-0022限定例外](../../adr/ADR-0022-feat164-personal-local-activation.md)。Owner已明确回复“批准该限定例外，继续完成 D5”，ADR-0022已Accepted；校验器仍要求完整生产链及显式local_release范围记录。继续离线实现、同源构建及真实备份资格。

执行顺序：限定设计/来源审计 → 新Desktop部署接口与安全离线验证 → 本地固定来源及canonical新构建 → 完整冷备份/只读检查、源与workflow就绪 → 适用本地G4/G5及Owner限定批准 → 创建精确日常启用记录/新入口、启用K3.1 → UI零请求验证、正常退出/同入口重开及完整后态 → 本地观察/G6与交付记录。不执行D3迁移，不新增模型请求或旧计划授权；不改Runtime核心/补丁。
