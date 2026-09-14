# canonical10/11 原生页面构建静态审查

10 与11采用冻结后的同一源码及标准 Rsbuild/Rspack 构建，382个文件的路径、字节数与SHA256全部一致。总45,218,737 bytes，最大11,804,583 bytes，未扩大既有512文件、64MiB总量及16MiB单文件预算。原08/09因修复源码已变化，只作诊断，不纳入此确定性结论。

原生拆包关闭 scope-hoisting（concatenateModules:false），解决06/07中仅模块导入排序和局部变量重命名造成的不可复现字节；没有对构建产物做任何后处理或替换。

## 静态覆盖

对所有JS执行真实 TypeScript AST扫描，包含符号解析的Function别名、间接eval、Worker/SharedWorker、serviceWorker、importScripts、动态import及script元素加载；并分类原保守正则的全部命中。扫描不执行任何bundle、Worker、eval或网络，也不是全程序对抗性污点证明。

| 类别 | 数量 |
|---|---:|
| dynamic_function | 18 |
| dynamic_function_alias | 2 |
| dynamic_import | 10 |
| indirect_eval | 1 |
| network_primitive | 78 |
| script_element_loader | 10 |
| worker_constructor | 7 |
| worker_import_scripts | 1 |

SharedWorker构造、serviceWorker注册、直接eval调用均为0；间接eval为1。244个正则命中含215处语言字符串/模板、1处正则数据、2处非调用标识符/命令表及26处真实构造调用。78处网络语法候选中明确区分KaTeX token fetch（27处）、query/router/completion同名调度方法和实际HTTP原语，不能把它们统称为78次网络调用。每个位点的模块ID、偏移、上下文、分类及触发条件见JSON。

## 关键来源与可见组件边界

- vendor6245的4个Worker来自Prism异步高亮、tt-uploader的Blob/data两级Worker和PDF.js4.4.168；均不在对应模块顶层直接构造。
- 独立TS模块888018在模块求值时调用403356的initTypescriptServer，才构造Worker。CodeEditor878803通过React.lazy进入5838；Text710718使用551279的preset-expression以及628561→520189.mixLanguages({})，未提供innerLanguage，也不进入上述TS模块。
- 其余Worker属于PDF.js4.3.136和Monaco语言服务，当前本地三节点不提供这些功能。
- Function来自Formily字符串schema、d3-dsv列映射、Ajv schema编译、lodash.template、旧环境全局/bind回退、PDF能力探测及get-intrinsic构造探测；现本地Start/Text/End不需要这些受禁分支。此结论仍需真实App验证，不将try/catch吞掉CSP错误视为通过。
- get-intrinsic794687只有604823/693200/659111三个caller，参数固定为String.indexOf与Map/WeakMap内建操作，无Async/Generator/AsyncIterator请求；所有JS里的调用已独立复查。
- 10个动态import来自两版PDF.js的Node-only fs/http/https/url与fake-worker；10个script元素来自tt-uploader6、旧Promise调度2、Monaco1和标准Rspack本地分片1。正常Rspack加载仅使用/editor/的manifest资产。

## 精确清单与运行时限制

scripts/yijie/workflow-editor-csp-reviewed.json仅登记此次人工分类的40个精确文件路径、SHA256、字节数、位点及理由；新增或变化文件不能按包名/模块ID/通配符继承批准。脚本提供无自动刷新审查清单命令。清单检查与9项focused tests通过；最终canonical12仍需完整构建与check。

运行时CSP保持：script-src self且无unsafe-eval；worker-src none；connect-src none；外部脚本、blob/data脚本均未获权限。此记录仅解除已审字节在保守静态辅助检查中的阻断，不授权执行受禁代码。

尚未执行：真实App打开、编辑保存、自然到期/重连、重开及CSP观测。该运行资格由根代理独立记录，不能被本静态审查或构建代替。


## 第三次完整验证

canonical12 标准 build 与 check 均 exit 0，382个资产与10/11逐文件字节及SHA完全一致。HTML/CSS全部资源引用与既有预算检查通过。manifest为84,568 bytes，SHA256 `0647a4ed172b27c4ea7ac806ad00a113514876dbf47fb0c843596418016807c9`。原生App尚待独立资格；构建通过不改变上述静态审查范围。
