# canonical24/25主题增量验证

以已完整保存并逐SHA验证的23真实产物为基线，24变化2CSS、3JS及HTML，379/385资产字节保持。native9484共4462模块只改628561 expression baseTheme、479639 MiniMap public panelStyles、652102 nodeColor token、951125 ColumnTitles颜色，main639模块字节保持。没有新增/移除模块。

仅对3个变化JS做AST审查，8个原敏感位点均保持原runtime resolver/loader与4个原资源fetch分类，无新Worker/WASM/eval等。原45项目录仅3处hash更新，42项原SHA不动，3项CSP focused测试通过。未重复无关功能测试。

canonical25标准build/check均exit0；24/25产品源/依赖/配置保持冻结，仅审查目录更新，385资产路径/bytes/SHA完全一致。HTML/CSS资源与原预算检查通过。manifest SHA256 `062565c6cfe993f1676a72b4a7e4249d228c628484d75c1ca8b00c440feee147`。

未激活服务/App。配色、onboarding正文/变量列、MiniMap外框及菜单最终效果须在真实App继续验证；构建不代替UI验收。
