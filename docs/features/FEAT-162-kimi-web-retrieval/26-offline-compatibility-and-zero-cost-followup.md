# FEAT-162 — 离线兼容检查与零费用续验

2026-10-29。用户授权修复5项远程schema EOF兼容阻塞，补齐其余可零费用验证、同步文档并复审；禁止付费、提交/推送和破坏性/攻击测试的约束继续有效。本轮checker/test/doc修复contract-impact=none：不改变Desktop/API/Host/Runtime的wire、权限、工具执行或持久化；原FEAT-162产品扩展仍为breaking。

前态见evidence/eof-before-20261029.json。26号是实施前方案及后续结果载体；24/25号保留前轮事实，不回写其失败日志。Owner与消费者沿当前需求，不新增发布资格。

## 执行方案

根因：check-breaking.sh只导出baseline的openapi树，scheduled-plan-draft通过自有HTTPS `$id`引用jsonschema树，oasdiff因此访问网络并EOF。按同一来源分别解析baseline和worktree的闭合引用：旧端只读指定Git树，当前端只读当前权威源；临时投影只改`$ref`定位，不改变schema约束或版本，不下载远程兜底，不借用当前schema补旧基线。

保持原oasdiff/buf/AsyncAPI/JSON Schema检查全部执行。普通合成schema验证来源隔离、引用闭合、失败关闭和实际breaking变化可检出；不创建Git fixture提交、不注入攻击样本。八个既有基线全部重跑，额外有价值基线按实际范围记录。

再审现有正常测试入口，补canonical worker由Host持有、正常结束/EOF、时间边界与结果读回等可执行的零费用项；界面如只能组件级预览，明确不能替代准确App/真实历史验收。不可变来源、实机激活与付费硬界不通过伪造回执或修改门禁解决。安全检查、日志、剩余项、最终来源保护与复审在本报告续记。

## 最终结果

五项原EOF阻塞已全部消除；原8基线加明确登记的K3.1补充基线d5792d6a…，完整兼容检查 **9/9 PASS**。原失败日志保留，未删除任何schema约束、降低错误级别或复用当前schema冒充旧基线。完整命令和退出码见[eof-checks](evidence/eof-checks-20261029.json)，每个比较的源摘要见[eof-projections](evidence/eof-projections-20261029.json)。

| 基线 | 新结果 |
|---|---|
| 61137174a25dc368e0006f27633fd4a9ad097aa6 | PASS（原EOF） |
| bedf4159b0fa22e24efe6c295f8b0d4845df56b7 | PASS（原EOF） |
| e35ae9a0711014e4774a1347413e9a343ce7ab2c | PASS（原EOF） |
| 1a213ac8383e95ac6ec69363937687904fa3591c | PASS（原EOF） |
| 35e0949c95d7a59ca5480715c225766dcc822056 | PASS（原EOF） |
| f16a497e1377f45747f8ff9292b4b60cf2027f88 | PASS |
| 6f632f155eacdaf93df0e0b00b5dab9e369c5442 | PASS |
| 811f38d6b104fa18477107e7ac91a85e19c445d1 | PASS |
| d5792d6aad18352ce8d1c5d510d345004cab3bd6 | PASS（补充） |

### 修复与证明

- 新prepare-breaking-inputs入口只读取两侧的openapi/jsonschema权威源，根$id建立唯一索引，查指针/依赖闭合后生成临时比较输入。每次改写记录原ref与目标；逆向恢复ref后必须与完整解析原件deepEqual。临时输入只供固定oasdiff，不成为新的SDK/schema来源。
- 初次实现把内部ref写成含base/current的绝对临时路径，造成oneOf身份假差异；已保留相对文件/内部指针身份。另把responses.default误作字面default值的初次遗漏已修正，字典键与schema/default/示例值分开处理。最终九基线均无EOF及上述假差异。
- oasdiff原调用未指定fail-on，可能只打印breaking而退出0；本轮明确`--fail-on ERR`。5项新正常测试验证来源隔离、缺源/指针/重复ID失败、default响应、普通例值不变，以及真实比较器对参数长度收紧退出1。没有创建测试Git提交或替换可执行文件。
- 新checker限制Go模块下载为GOPROXY=off，保留checksum验证。首次同时设置GOSUMDB=off被既有Go toolchain校验拒绝后已移除该设置，不降低完整性校验。
- 既有OpenAPI检查清单、buf breaking、AsyncAPI和JSON Schema比较均保留；后两者使用同一已解析完整commit，不再后续重复解析浮动ref。

## 补充零费用验证

| 项目 | 本轮结果 | 能证明的范围 |
|---|---|---|
| 完整breaking | 9/9 PASS | 已登记相关基线在现有checker覆盖范围的结构兼容，不等于语义/真实App验收 |
| Contracts focused | 38 PASS | 原33项加5项离线比较测试，含旧定义与正文/双截止来源 |
| Contracts lint | PASS，12项既有Redocly warning保留 | API/schema/Proto/TS/Go静态检查 |
| Kimi focused | 27 PASS | 原24加D前/到/后、提案延迟/短lease和新旧owner晚批准10秒；只普通时间值，无后台HTTP |
| Host→canonical worker | 5个顶层测试（另含2子例）race PASS | e61468d4…实际正规worker，正常prepare/bind/replay/revoke、未资格选集、正常EOF、正常容量终止、同owner单子进程复用；每次NormalExitConfirmed |
| Connectors worker-lint | PASS | 四族来源、固定依赖、rustfmt、Clippy，未改生产Rust逻辑 |
| Desktop focused | 9文件44 PASS | 结果/审批/历史组件及前端状态逻辑 |
| Desktop lint/typecheck | PASS | 含新tests/visual/feat-162预览源；未增加运行时入口或权限 |
| 组件视觉/键盘 | 有界范围PASS | 真实组件的1180×760亮/暗、正文展开、solid焦点、Tab/Enter拒绝事件；两次axe无violations，无横向溢出 |

截图为组件预览，见[亮色](evidence/eof-ui-light-1180.jpg)、[暗色](evidence/eof-ui-dark-1180.jpg)及[视觉证据](evidence/eof-component-ui-20261029.json)。仅普通合成值，不导入Native client/账户/模型/供应商。浏览器标签在后续导航中不可用，完整下方区域与空/错场景实视不声称通过（对应DOM测试通过）。视口已恢复、标签清理；Vite通过其内置SIGTERM正常关闭处理await server.close退出143，端口释放，未强杀或升级信号。首次测试编译漏写CancellationToken路径已修正并重跑27项，未将编译失败计PASS。

Z3纯时间边界明显补强；Z8真实worker/Host owner正常EOF部分已补齐；Z9只增加组件视觉层证据。其余Z组沿24号，准确App与正常历史重开仍NOT RUN。新原始网页内容、真实路由、质量/费用与E1—E7仍NOT RUN，v2 live固定关闭。完整AC-021—030不因局部测试改为pass。

## 新发现：旧全量生成入口的独立基线失败

额外执行`pnpm check-generated:safe`时，**未修改过的旧scripts/generate.mjs**仍在通用JSON Schema编译阶段下载`https://schemas.yijie.ai/chat/model-selection/v1`并失败；它先清空若干SDK目录，却未覆盖当前各家族canonical生成文件/出口，不能直接拿该入口替代当前分族生成流程。该失败不属于九个breaking检查，仍记FAIL_BASELINE，不能报告整仓生成检查全绿。

已从本轮前态确认那些路径原本干净，恢复35个被该失败运行删除/改写的已跟踪生成文件；新生成3个文件先保全于本轮.local记录再移除。所有原有dirty生成文件逐项摘要保持。恢复动作是撤回本轮失败生成的副作用，不是手工修补生成物或放宽checker。详细名单及保全路径见eof-checks中的failed_generation_restoration。当前相关家族各自canonical源/产物检查仍通过。

该旧全量入口需另行统一现有家族的生成覆盖、命名与SDK出口；本轮没有为求绿色扩改公共SDK导出或删除校验。后续不能忽略该FAIL_BASELINE宣称全部发布门禁通过。其余不可变消费引用、专家来源级联和准确App仍受本轮不提交Git及未激活边界限制。

## 文档、费用与交接

主代理最终复审见[27号](27-offline-compatibility-reaudit.md)，不是独立人工批准。D0、元仓lint/57项治理测试、设计构建通过；源码/生成物和历史保护最终结论以机器eof-checks为准。此前24/25号与实现证据按历史时点完整保留；当前00/01/02/04/22/feature.yaml同步最新状态。

新增付费/模型/供应商账户调用均0；未提交、推送或激活。旧20号FAIL、三项未知与42.710457元保守占用保持。完整未来预算仍为Σ模型硬上界+0.105元+R_native；原241.421224仅条件小计，不解锁live。当前已关闭原五项兼容阻塞；剩余真实App/不可变来源、旧全量生成基线、native硬费用界限及owner停止链资格如实保留，D4未通过。
