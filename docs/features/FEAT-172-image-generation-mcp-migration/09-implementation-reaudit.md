# FEAT-172 实现复审与修复

2026-11-12，用户要求再次审计并直接修复。代码修复与定向检查已完成；用户解锁后已通过正常退出与`pnpm client:dev`完成更新，Host/Runtime ready、已有图片原生预览正常。用户明确要求再次弹窗并完成授权后，同一新Host的无弹窗只读检查24ms返回ready；没有新增付费调用。之前的真实生成记录保留为之前构建的证据，不能冒充本轮重新调用。

`contract-impact=semantic`：修复MCP准入与回执的时序行为，沿用现有输入/状态/错误码；不改变Runtime源码、二进制或canonical schema。先更新媒体源契约的行为说明，再由生成器同步消费者。Artifact私有写入清理与生成登记修复不新增业务协议。

## 已确认并修复

| 优先级 | 根因与影响 | 修复与验证 |
|---|---|---|
| P1 | `turn/completed`在Store核对轮次前无条件清除imageTurn。旧A通知到达时会取消已准备/执行的B；迟到停止请求也把未绑定轮次当通配符。 | Store接受终态后才按turnID关闭图片状态；尚未绑定的停止只接受Store当前原生轮次。准备态、活动态旧通知及迟到停止回归通过。 |
| P2 | MCP HTTP与原生通知/RPC独立，正常请求可能先于Host绑定到达而误报cancelled。 | 仅对Host已准备的轮次等待原生绑定信号，最多5000ms，不从模型参数绑定。绑定后重新核验Store；超时state_pending且未占名额，取消/不同绑定0供应商调用。短轮次先结束、后返回start时清理残留引用。 |
| P2 | 图片成功发布后，回执缓存阶段仍因稍后的取消而改写为cancelled，导致UI与MCP回执矛盾。 | 成功/取消仍在原发布锁内裁决；缓存仅保存已定结果。发布后停止或结束均保留成功回执，不追加失败终态。 |
| P1 | Artifact内容写入失败执行`RemoveAll(session directory)`，会删除同会话其他暂存产物。 | 排他创建单个密文文件，失败只删除本次创建的文件；会话目录只尝试空目录删除。同名普通目录冲突复现原误删，修复后旧产物仍可读，移除冲突后正常重试成功。 |
| P2 | canonical生成漏登记保留的runtime-host-images；staging漏复制context-window现有文档输入。旧测试硬编码23族且假定所有receipt.generated均为数组。 | 补齐登记和真实输入，不改旧生成器/pin；测试覆盖所有receipt/producer、数组/映射输出及实际SHA-256。10个定向Contracts测试通过。 |

正常回归在修复前已复现旧通知误取消、提前MCP误拒和误删产物；没有通过强杀、替换可执行文件或破坏权限制造异常。新增测试在`internal/session/media_generation_order_test.go`和`internal/artifact/store_write_test.go`。

## 原生复用、专家与凭据结论

- 固定Runtime原生MCP发现、Code Mode、metadata、审批、通知和继续执行保持；没有新增执行协调器、媒体数据库、任务平台或Runtime补丁。
- 任意显式专家都排除内置MCP。Host继续校验原存储绑定，包括旧历史中的工具调用；专家不可用、失败、输入不支持均不触发内置兜底。现有专家提交/资格协议不变。
- 凭据仍由运营方一次预置；普通Host只读、禁止交互，供应商Key不进入模型、Runtime配置或前端。本轮未扩充凭据协议、复制秘密或增加代理服务。新构建身份须由同一受管Host只读复核，不能沿用旧SHA的授权结论。
- Artifact继续使用现有暂存、提交ACK、状态查询、预览与保存。未增加“生成状态”查询服务。

## 验证及边界

机器记录：[implementation-reaudit-checks.json](references/implementation-reaudit-checks.json)。21个Host顶层用例带`-race`通过、0跳过；Contracts定向10例、消费者同源检查、lint、实施基线breaking、Go vet与标准Host构建通过。最后的源生成后重新构建真实Rust adapter，固定Runtime的Kimi/MiniMax两配置回环均通过、0跳过，证明原生MCP→HTTP桥接→工具结果继续执行与专家排除。元仓lint及57项文档治理测试通过。全量测试中违反用户安全条款的历史fixture仍不执行；不把定向通过表述为全量回归通过。

完整生成登记/文档输入修复后，`generate --check`走完所有producer但仍报告旧`runtime-chat-models`来源漂移：既有生成器用当前Runtime HEAD `fe3f5b1c768f2a1464314e2a350d419a3e63d9c6`覆盖该旧族原`55b4e51049d6f4fc0af4b35f12832357f5e4ea06`。差异仅为该source.lock的`runtime_source.base_commit`。本轮未发布生成结果、未改旧不可变消费者/来源锁以消除红灯；这项保留基线来源治理需单独处理，不影响FEAT-172修改族的同源检查。旧Runtime/schema/binary及同步模式保持。

本轮真实主聊/Seedream/LinkFox均0次；累计仍为22/24、2/6、0/0。没有提交、推送、发布或历史数据清理；原有用户业务/UI改动保持；Desktop仅由既有freeze脚本更新3份开发构建来源记录，以配对本轮Host源码，不改旧发布/Runtime锁。

## 解锁后的更新复核

2026-11-12T16:46:55.891804+08:00：用户确认解锁。旧App通过⌘Q正常退出，canonical停止检查通过；同一日常入口完成原服务/数据验证、Host和adapter构建并启动。`/healthz`与`/readyz`均200，Runtime ready；已提交参考图Artifact可在原生预览中正常打开，未提交新轮次。

当前受管Host SHA-256为`3af821aad977030df95ee85c54adc5052c738b5e24669f5d14be4e73e82f742a`，与审计构建一致。非交互凭据检查484ms内返回`credential_unavailable`、Provider请求0；旧构建授权不能继承为当前构建通过。需用户本人允许同一Host读取原作用域Seedream条目，不需要更换Key或追加计费额度。其余修复已经生效，未以凭据不可用为由扩大权限。

## 新构建授权完成

2026-11-12T17:05:33.593627+08:00：用户明确选择“再次弹出授权窗口”。先核验受管Host仍为`3af821aad977030df95ee85c54adc5052c738b5e24669f5d14be4e73e82f742a`，再调用既有运营CLI请求一次系统授权；系统窗口由用户本人完成，未使用计算机工具访问SecurityAgent。授权CLI返回ready，随后同一Host普通`--check-media-credential`在24ms返回`ready=true`，Provider请求0；`/readyz`仍为200/ready。凭据复核闭环完成，运行中的构建未再修改。原失败证据保留，新增证据为[credential-readiness-reaudit-authorized.json](references/credential-readiness-reaudit-authorized.json)。

修复已在日常客户端激活；原图片预览、定向回归与本地原生回环结论保持。本轮没有重复真实生图或聊天，累计仍22/24主聊、2/6 Seedream、0 LinkFox。全量生成的旧runtime-chat-models来源漂移仍按上节记录，不冒充通过。
