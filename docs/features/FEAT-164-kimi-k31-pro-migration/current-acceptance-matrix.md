# FEAT-164 当前验收与来源矩阵

> 当前以[49 r5真实功能与日常边界](49-r5-real-qualification-and-daily-cutover-boundary.md)为准：Owner已明确授权必要真实功能调用且不要求精确查价；本轮1次r5真实42、保存/重开零补发和正常退出通过。旧账本/预占保持，日常迁移未执行；完整core/剩余业务状态仍按明确缺口判定。已移除外观专项不再作为门槛。

2026-10-26。整项目标是活动Kimi全面替换为kimi-k3.1-pro，同时保留历史、原操作与授权事实、MiniMax能力；完成标准仍为01的十项Must AC。独立验收身份只是取得缺失证据的手段。当前整项IN_PROGRESS，十项AC整体pending，不以局部PASS或本地提交代替完成。

## 当前唯一来源组合

| 模块 | 固定来源 / 适用范围 |
|---|---|
| Runtime | 11fd4504c28afd0f65c6f5f62a6b5328dd437f5a；新r5 binary283d12e…；旧producer binary9766d7e…均保留 |
| Contracts | ca06d0999c9a08afe80ab3f34a537d492b830ac7；只刷新旧制品来源元数据，r5权威投影仍5b5dad |
| Host | 8cd6bccbdc1ac3906aea53d95441299f7cfefcce；产品实现与894671b逐字相同，仅legacy consumer元数据 |
| Desktop | 9f5814fec6cd071d39f0c12f8f48097ce661cb6a；固定独立资格入口、受控旧配置许可及退役终态历史读取 |
| Connectors / Skills | cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9 / 595c927ae101d3d31c234f60565041eee0864680 |
| 本轮App | 旧producer Desktop54921df，新candidate Desktop9f5814f，分别在独立目录canonical构建；后续差异为前身许可接线、退役终态历史读取及测试/文档；维护入口源码保持；ordinary组合见46；同Desktop9f5814f的media组合App42a23cf…/119文件及5次本机验收见47 |

以上是本地验收来源，未推送/发布。主Desktop仍fd0c575且保留用户dirty，不能据主工作区HEAD判断新入口内容。Runtime源码/补丁未新增修改；两次失败来源检查、首轮启动失败与修正分别留存。

## AC与剩余判定

| AC | 已有有效证据 | 本轮推进及仍需补齐 | 整体判定 |
|---|---|---|---|
| 001 活动目录/默认参数 | S1源/生成/离线参数；r4最小真实文本 | 当前App新旧目录/明确选新模型；日常活动默认尚未切换 | pending |
| 002 受管配置 | r5已知前身/漂移准入源码和定向资格 | 独立自然旧Home→r5，保留trust/配置；最终现场cutover待授权 | pending |
| 003 SQL兼容 | 44/45自然SQL29/37、ledger/原事实/备份保持 | 实际compiled canonical入口旧→新及正常重开；其它支持路径按原范围补证 | pending |
| 004 原thread迁移/恢复 | 44旧Runtime→Host实际same-thread切换/取消/重开 | 46已通过当前App自然旧线程显式切换/正常停止/继续及重开；unknown恢复及终态回执完整UI仍须独立结论 | pending |
| 005 退役与取消 | claim/send准入、never-sent领域/API定向检查 | 已发/未知不重发；完整UI取消场景不可靠制造故障得到 | pending |
| 006 旧计划/新授权 | 44/45自然领域退役与新grant，原事实保持 | 46已通过App自然旧计划→退役→明确审阅→新单次授权；仍需全范围最终证据 | pending |
| 007 全调用面 | S4接线、专家/媒体/辅助、子代理终态/自动压缩离线组 | 在最终来源按适用性绑定；47已补当前media App专家/成果预览/PNG/MiniMax及重开；48补四组合来源、当前r5辅助/子代理终态/重放/自动压缩；完整真实/最终资格仍缺 | pending |
| 008 响应语义 | 旧源真实最小文本及离线图片/工具/search sources | r5与最终候选完整TCONF04；真实供应商新增范围当前无授权 | pending |
| 009 Key/审批/预算 | 原机制和安全离线检查，账本独立保留 | 当前源计量与普通恢复零业务调用，不能继承过期预算 | pending |
| 010 生命周期/业务状态/回退 | r5有限正常退出、43号两次ready/历史/自然WAL0；旧r4视觉 | 47新增media两次正常退出/四库WAL0及0补发；剩余适用final仍须独立判定；亮暗/键盘/最小窗口已由Owner移除 | pending |

r4 G2V及视觉PASS为历史证据，不自动变成r5 PASS。核心、视觉、teardown必须各有当前来源判定；现有关闭子集不是完整teardown。G4/G5/G6保持pending。

## 当前数据与授权边界

原SQL41只读归因：1条unknown模型选择是原K3.1→MiniMax操作f38666dc…；2份occupied grant对应completed且native_terminal释放的运行，无reservation。占用数记录消耗，不能推导全局busy，也不能为了维护准入而退款/清理。固定独立资格数据与该库、日常库隔离。

S4V新增真实1：Owner明确授权必要功能调用，不要求精确查价。本轮1/1、累计6次，30元cap保持；历史估算累计14.795856含14.188544 unknown预占，旧两账本逐字保持。本机合成HTTP单独计数，不伪装供应商调用。未开放日常迁移/发布/推送；新Runtime核心或补丁修改先提方案。

下一步按48的实际结果继续：46的自然旧App→受控迁移→新App S2/S3子集已完成；同源media子集也已完成，48已补保留Runtime home的辅助/子代理/压缩资格；下一步收敛剩余时序、源连续性和适用final，已移除的外观专项不再执行；不再重复没有新变化的已通过子集。最后另行形成可审阅的日常cutover清单，取得对应授权后才执行。

本轮最终判断：r5最小真实G2V及正常teardown PASS；完整core/剩余业务状态仍按49列明缺项，日常cutover未执行。下一步形成日常部署兼容的具体diff与授权清单，不重复已合格的42/Runtime组。
