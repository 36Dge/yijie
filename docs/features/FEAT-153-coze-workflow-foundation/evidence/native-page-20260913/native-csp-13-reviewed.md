# canonical13：真实 JavaScript 高亮引擎与 WASM 审查

canonical12真实App出现Shiki WASM拒绝和Copy服务缺失，不能沿用其构建通过当作App资格。统一候选13已补透明Shiki引擎选择、真实Copy服务绑定及原生错误恢复界面。当前记录只覆盖构建和静态来源。

`src/shiki-js.ts`通过exact `shiki$`编译alias保留原API；仅在createHighlighter未提供engine时选用锁内原`createJavaScriptRegexEngine({target: 'ES2018'})`。原始语法、主题、tokenizer、高亮HTML实现保留；没有替换WASM、伪装运行时或扩大CSP。4语言×2主题的普通synthetic smoke全通过，原源码脚本和结果均已归档。

独立实际bundle审查确认：preset-code模块583155顶层高亮器调用main wrapper676463；wrapper传真实JS engine给353201原createHighlighter；core544143的`engine:e.engine??s()`因此不进入默认Oniguruma工厂。当前完整Shiki根消费者仅使用createHighlighter，codemirror-shiki/marked-shiki使用传入实例。

透明适配保留原singleton快捷API及显式engine。未来调用这些入口可能选择Oniguruma，必须重新审查；不能泛称所有Shiki API都不使用WASM。

静态审查43个精确脚本，131个实际语法位点与301辅助命中全部分类。新增57个WASM namespace引用：4个真实instantiate/instantiateStreaming、3个typeof/instanceof能力引用、50个静态语言/说明字符串。4个真正调用均来自原Oniguruma及内嵌WASM loader，调用条件已与实际wrapper路径核对。所有Worker、Function别名、间接eval、动态import、script loader与网络候选分类保留。

source gate现在要求所有WebAssembly命中有精确字节审查；旧清单缺此分类视为0而拒绝非0引用，不能自动继承旧允许项。10项focused tests通过。

canonical13正常构建382文件、45,278,718 bytes，最大11,863,749 bytes，原预算不变；暂在新审查门阻断后登记精确清单，等待canonical14完整build/check及13/14逐文件对比。所有运行时限制不变：script-src self、无unsafe-eval或wasm-unsafe-eval、worker-src none、connect-src none。真实App资格仍需独立完成。

## canonical14最终构建核对

完整build/check均exit 0；全部382个资产与13逐文件路径/字节/SHA一致。预算和HTML/CSS资源引用通过。manifest SHA256 `2dfbe477ac2b38ad6b84093306d34785a91983c9ae6fa2d1cce8742a4cfe03ac`；详细对照见native-build-13-14-reproducibility.json。运行时CSP未变，真实App仍由独立验收给结论。
