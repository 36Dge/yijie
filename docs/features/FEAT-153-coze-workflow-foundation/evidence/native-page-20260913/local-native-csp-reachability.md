# FEAT-153 local 原生三节点 CSP 可达性复核

只读静态审查；未执行 Function/eval/Worker、网络、危险 fixture 或真实 App。
当前结论限定 start/end 固定只读字符串配置、text 原生拼接编辑，以及 local Header/Toolbar。
不能外推到所有 Coze 节点，也不是运行时 CSP PASS。

## 必经表单链

- start/form-meta.tsx、end/form-meta.tsx、text-process/form-meta.tsx 均是 FormMetaV2。
- createNodeCorePlugin 为 FlowNodeFormData 注册 FormModelV2 factory。
- FlowNodeFormData.createForm -> FormModelV2.init -> @flowgram.ai/form createForm。
- 这些 formMeta 的 render、validate、effect 是已编译函数；没有 Formily {{...}} schema 字符串。
- NodeConfigForm -> @/form/Form 只是 FormProvider，只读参数传给原生 OutputsField/InputsParametersField。
- 因而当前必经链不需要 Formily Schema 的字符串 Function 编译。Formily 模块打入 bundle 不等于该编译器被调用。

## 原生 ExpressionEditor 与 TS Worker 分界

- text-process/ConcatSetting -> nodes-v2/ExpressionEditorContainer -> components/expression-editor-next Renderer。
- Renderer 使用 @coze-editor/editor/react 和 preset-expression；锁定 preset-expression 包只安装 CodeMirror 编辑、历史、输入规则、高亮与预编译解析器相关能力。
- hooks 的 mixLanguages({}) 不提供 innerLanguage 或 outerLanguage；内部是 LRLanguage.define + 预编译 Lezer templateParser.configure/parseMixed，不编译 JS。
- TypescriptEditor 是另一条 React.lazy 路径；该模块求值确会启动 Worker，必须保持不被上述链加载。

06 冻结产物复核：

- assets/js/7705.b045b45d.js：SHA256 d2d2f4d6584c892d84fd6ecfb5babfe5ee16fdc1c12a37600f52c5ddb2dc0dac，10,452,554 bytes。
- assets/js/index.276fc7f5.js：SHA256 6c6de6172cb5ac8a39115faeeb7f70828338d2c95fbbb35b7f0135ec40b4d4b1，6,778,968 bytes。
- 主 index 2,172,828 附近，实际 Expression.Renderer 用 plugins:eP.Z，其中 eP=require(51279) 是原 preset-expression。
- 主 index 2,171,150 附近，实际扩展使用 eR.ut({})，其中 eR=require(11140)，ut 是 mixLanguages。
- 独立 TypescriptEditor lazy loader 在主 index 2,128,598 附近加载 3139 -> 42888；async/3139.e4efd9be.js 2,743 附近在模块顶层构造 Worker。
- async/3139.e4efd9be.js：SHA256 912c9d608b67f67e3a32dd9350c4bae35c802fa51e2c84713b11e7d8a8da0956，3,776 bytes。

## Ajv 的具体 guard

- nodes/validators/json-schema-validator.ts 的 Ajv.compile 仅由 output-tree-validator/schema.ts 的 checkObjectDefaultValue 调用。
- caller 先要求 defaultValue 是非空字符串，再要求 ViewVariableType.isJSONInputType(type)。当前 start/text output 是固定只读字符串、无 JSON default，故不进入 runtime compile。
- end/text 输入当前是 REF；valueExpressionValidator 走 variableValidationService.isRefVariableEligible，不调用 Ajv。
- Toolbar 的 local StartTestRunButton 打开原 TestFlowForm 槽中的 local 面板，未调用原 useTestRunFlowV2/generateTestFormFields 的 Ajv 路径。
- Header 的 local EditModal 使用原 Coze Modal/Input 与 changeName；未实例化上游 CreateWorkflowModal。

## get-intrinsic 别名构造补证

04 和冻结 06 的全部 JS 均检查了数值与字符串 module-ID 调用。06 中 require(94687) 仅见：

- 4823 / call-bound：固定 %String.prototype.indexOf%，再接收下述 Map/WeakMap 固定方法名。
- 93200 / side-channel-map：%Map% 及 Map.prototype.get/set/has/delete/size。
- 59111 / side-channel-weakmap：%WeakMap% 及 WeakMap.prototype.get/set/has/delete。

require(4823) 也只由后两者使用。没有 AsyncFunction、GeneratorFunction、AsyncGeneratorFunction、AsyncIteratorPrototype 的构造请求，因此这些已固定 callers 不进入 needsEval -> Function 别名路径。
逐点上下文：/tmp/feat153-native-csp-06-intrinsic-callers.json。

## 安全处理位置

- 当前不需要放宽 unsafe-eval、worker-src 或 connect-src，保持真实原生组件。
- 如未来打开 JSON 默认值或 schema 输入，使用已核定 schema 的 build-time/AOT validator，或有限类型的函数 validator；不能运行 Ajv.compile 后吞掉 CSP 异常。
- 如未来需要动态表单，优先仍使用现有 FormMetaV2 函数型字段/validator，避免接入 Formily 字符串表达式。
- 文本插值继续使用原 preset-expression 与 Lezer；不能因完整 bundle 包含 TS/Monaco 就启用 Worker。代码节点需要单独范围与部署/CSP设计。
- 上述 SHA 只适用于冻结06，任何重新构建仍需精确复核。真实 App 普通创建/编辑/保存/重开与 CSP violation 观测尚由根代理执行。
