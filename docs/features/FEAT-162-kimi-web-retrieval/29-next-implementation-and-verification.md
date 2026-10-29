# FEAT-162 — 方案复审后的实施与验证

2026-10-29。先落28号复审再修改代码；Owner随后明确本轮可收费，并给出新增总额**20元**。本轮实际新增模型/REST/供应商账户调用0，费用0；Git提交/推送0。旧42.710457元及三份未知预占不变。主代理完成审查，无独立人工或子代理批准声明。

## 已实施

- **全量生成闭环**：Contracts入口覆盖23个登记家族、核心OpenAPI/Protobuf/AsyncAPI与Native v3/v4。专用schema由各自canonical producer生成，generic compiler禁HTTP解析；SDK出口以显式源清单维护。检查先在临时目录运行，不发布；正常生成错误不污染工作区。生成发布前后复核输入/输出与并发编辑，短发布阶段保留恢复journal。不声称断电/强杀下多文件原子性，也未执行此类测试。
- **来源保持**：5个leaf generator不再用新HEAD无故替换旧base_commit；全量生成更新7份source.lock的来源摘要，其中Experts两份反映此前FEAT-162已修改的Broker/Host源。全部SDK产物字节、公共出口及所有base_commit保持。没有手改DTO、重写consumer不可变回执或构造新Git引用。
- **停止适配**：meter复用Host现有GET session与normal interrupt接口，仅允许127.0.0.1。冻结case session→实际Runtime thread/turn→Host当前映射必须一致；先持久关闭模型准入，再同步请求停止。204记Host确认，拒绝/缺响应记未确认，不自动重试。停止后不继续转发工具响应。未新增产品权限、审批、API或Runtime补丁。
- **计量修复**：动态client_metadata不再纳入稳定产品配置摘要，但实际thread/turn另行校验，出站请求字节保持。原生搜索事件项即使附带模型usage也不能当作精确计费次数，保留未知预占。支持区分真实请求的输出字段与有证据的供应商默认上界，不向真实请求强加输出限制。
- **20元控制**：保留17次模型HTTP、Basic/Pro/Fetch各3次、REST全额0.105元预留；以“已结算+未知预占+下一次完整预占+REST预留≤20元”逐请求准入。仅完整已知结算可释放差额，禁止并发。不会为凑满七例超预算；不再错误要求先预占全部17次的最坏情况之和。

工具改动本身不改变SDK公共签名或wire语义，停止适配只消费既有Owner接口；FEAT-162整体breaking分类不变。实际App绑定及完整撤权链仍需实机证明，普通loopback适配不能使`LIVE_EXECUTION_QUALIFIED`自动变true。

## 验证与过程失败

完整命令、退出码和日志摘要见[evidence/next-checks-20261029.json](evidence/next-checks-20261029.json)。已执行包括全量generate/check、Workflow只读check、Contracts定向43项、v2计量8项、legacy计量19项、Owner停止适配7项、纯观察配置1项、Native环境1项、Contracts/Desktop lint、元仓治理检查。

本轮先出现以下失败，原日志保留：

1. 首次新全量check准确报7份旧来源摘要漂移；canonical generate仅更新这些摘要，后续full check零差异。
2. Native旧测试对已有环境变量数量断言为2，真实为3；补验证固定meter URL存在、无policy时不产生policy变量，仅改测试，生产环境逻辑未改。
3. 直接Workflow检查时临时目录遗漏pnpm工作区配置，`pnpm exec`触发自动安装并访问包注册表，随后因build策略失败。该过程没有供应商/模型收费，但不能称全轮完全无网络。已补工作区配置、真实安装图与原lock逐值比对、禁止隐式安装及离线配置。保留受影响node_modules到元仓 `.local/feat162-next-20261029/contracts-dependency-backup`，用标准`pnpm install --offline --frozen-lockfile`从已有缓存重建，下载0；声明依赖、版本和源lock均未改。随后完整依赖图及full/Workflow检查通过。
4. 收费授权时间最初只填日期，D0要求ISO-8601瞬时值，导致D0及同期元仓测试失败；已登记收到批准后的首次保护快照时刻并注明不是原消息秒级时间，修复后重验。

此前9个breaking基线及Kimi27/Host真实worker/组件视觉证据仍见26/27；本轮相关wire输入逐字不变，因此不把这些历史结果伪装为本轮重新执行。没有运行包含禁止行为的全套历史fixture测试。

## 尚未执行及影响

| 项目 | 当前事实与影响 |
|---|---|
| 准确canonical App | 当前入口要求六仓来源干净且有完整commit，用户仍禁止提交；不伪造pin，不用旧App替代，因此未构建/激活本轮App |
| 真实Owner停止链 | 正常适配、身份不符、204/409、停后不转发等本机验证通过；真实App→Host→worker的未发送REST撤权未验，不写PASS |
| 费用准入 | 已授权20元；实际产品未传max_output_tokens，默认上界适配已具备，但尚未形成满足20元且含native风险的可证明上界；公开文档复核未找到可核验的原生搜索硬次数限制 |
| E1—E7/D4 | 未发收费请求，均NOT RUN，AC-021—030仍pending，整体in_progress；旧20号FAIL保留 |
| 禁止型验收 | 强杀、权限破坏、攻击fixture、可执行文件替换均未执行；普通值/loopback/正常退出不能冒充这些结果 |

费用参考：[Responses API](https://platform.kimi.com/docs/api/responses)、[组织与Key管理](https://platform.kimi.com/docs/guide/org-best-practice)。这里只记录查阅未找到可核验硬上界，不声称供应商绝对没有该能力，也不把余额/客户端停止当服务端费用上界。

下一步需要闭合真实来源/资源级联与可证明的20元发送策略，随后在准确App上补停止链和E例。收费批准已存在，不重复索取；当前禁止Git操作仍是来源闭合的实际约束。不能为了启动直接删除原生工具、裁剪请求、清除未知占用或把资格布尔值改为true。
