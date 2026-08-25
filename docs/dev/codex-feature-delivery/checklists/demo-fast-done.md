# demo_fast D0 / D4

## D0：产品与 UX 完整

- [ ] 用户、问题、结果、范围和非目标清楚
- [ ] 主流程与 Must AC 可操作判断
- [ ] idle/loading/success/empty/error/retry/cancel 均有行为或明确理由
- [ ] 布局、主次操作、反馈、预览/保存和视觉方向完整
- [ ] 真实入口、受影响仓库和已有改动已核对
- [ ] contract-impact、权威源和 source-first 顺序明确
- [ ] 付费、破坏性和生产操作未超授权

## D4：本地真实可用

- [ ] 正常入口启动真实服务并达到 ready
- [ ] fresh local 启动零登录交互，自动建立固定本地上下文并直达业务主页面
- [ ] 整个需求已实现且不是 mock-only
- [ ] 一次 fresh run 中全部 Must AC PASS
- [ ] 真实 happy path 产生可见/可保存结果
- [ ] 一个代表性 failure/retry PASS
- [ ] focused build/test/check PASS
- [ ] 有截图、录屏、Artifact 或脱敏 request ID
- [ ] Loading/error/retry 不困住用户
- [ ] 完整 diff/status 已审阅
- [ ] 无崩溃、数据破坏、秘密泄漏、死循环或阻断 Bug
- [ ] 已知非阻断限制已记录

D4 可以关闭 `exposure: local` 的 Demo；它不声明生产可用。
