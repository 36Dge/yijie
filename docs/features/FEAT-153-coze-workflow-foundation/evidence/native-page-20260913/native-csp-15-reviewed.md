# canonical15/16局部修复构建审查

实际source仅修原DragTooltip collector同步TDZ和canvas-data对原rawMeta string类型注解的比较兼容；原生组件/服务、数据实际保存内容、CSP、依赖与编译配置均保持。

main共5095模块，仅571362（DragTooltip）和851938（canvas-data）字节变化，其他5093模块、379资产字节与13/14相同。所有敏感调用模块与Shiki引擎路径保持。全AST复核131调用位点、301辅助命中（含WASM）、43精确脚本，无新增未分类项。

普通collector3状态验证、state12项测试（独立agent记录）及10项构建focused tests通过。完整canonical16 build/check均exit0，15/16的382资产路径/bytes/SHA全部一致。预算/HTML/CSS资源引用通过，manifest SHA256 `baa7695f0b480861470826b487eb6cf8dfcd6a73d7d8e3f000ae14e63ed25040`。

本记录不代替真实App资格；canonical14实际失败已保留记录。新候选由正常Infra流程部署后，仍需实际打开/编辑/保存/重开及CSP观察，不能继承旧D4通过。
