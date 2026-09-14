# FEAT-153 canonical06 → canonical07 字节漂移定位

两轮相同前端代码的输出在 Rspack 1.1.8 的聚合/拼接模块内出现依赖绑定顺序和局部名分配变化。以下为实际字节/模块证据；没有修改源、产物或审查清单来消除差异。

| 文件 | 事实 |
|---|---|
| vendor 7705 | 均为 10,452,554 bytes；1866 个 Webpack 模块完全同集合，只有 95318 变化。16 个变化字节均为 Row/Col 对应的两个 require 绑定顺序与其局部引用同步交换。其余 1865 模块完全一致。 |
| index | 均为 6,778,968 bytes；524 模块完全同集合，只有 72465、57160 变化。前者是聚合导出的六个相同 require 目标重新排列并同步修改引用；后者是 JSON parse/format 与旧 workflow URL helper 在同一拼接模块中的次序及局部名变化。其余522模块完全一致。另有 runtime fullHash / worker chunk hash 的正常传播。 |
| async 7605 | 均为 2329 bytes。唯一差异是 `o.h()` 返回的 full build hash，由 `6d3f1b4234fd245c` 变成 `a03fb82a8e77fd86`；Worker runtime、本地 importScripts 与全局对象处理代码完全一致。 |

vendor 示例：

- 06：`iR=require(19046), iH=require(65783)`。
- 07：`iR=require(65783), iH=require(19046)`。
- 公共导出名和所有对应引用同步交换，没有增加业务调用。

这说明当前按精确 SHA 的 gate 正确拒绝了未审字节。漂移来源定位于标准 bundler 模块拼接输出，而不是 README 文本被当作业务代码；本审计不宣称已经定位到 Rspack Rust 内部的具体实现行。

建议使用正常构建选项 `optimization.concatenateModules=false`，保留 deterministic module/chunk ids 和既有 LimitChunkCount、全部资源预算与 CSP。随后冻结源及构建输入，连续运行两次标准 build，比较**完整资产文件集合、每个文件字节数与 SHA256**。两次一致后再对那版新字节重新做精确 CSP 审查；不能用“调用数量未变”替代来源或确定性证明，不能后处理/重写输出，也不能自动刷新白名单。

证据：

- `/tmp/feat153-native-06-07-module-diff.json`
- `/tmp/feat153-native-06-07-index-module-diff.json`
- `/tmp/feat153-native-06-07-byte-diff.json`
- 06完整快照：`/tmp/feat153-native-csp-canonical06`
- 07三个变化文件：`/tmp/feat153-native-csp-canonical07-three-files`
