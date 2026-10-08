# FEAT-157 完整范围复审与继续实施

2026-10-08，按 Owner「认真审计、查漏补缺、继续完成整个需求」执行。旧诊断不足仅保留历史事实，**不是阻塞项**。51 项仍是实现范围；真实账号验收只选 Tushare，不要求另外 50 项逐一登录/调用。追加额度余额仍为 2 轮模型、1 次只读查询，本次审计和本地修复不消耗它。

## 审计结论

| 问题 | 代码证据 | 处理 |
| --- | --- | --- |
| 51 项只完成目录，实际执行只有 Tushare 单日行情 | Connectors `providers.rs::validate_authority`、`daily.rs`；Native `connectors/provider.rs`、`store.rs`、`mod.rs`；Provider 契约 `tool_profile` | 未完成，不能用目录或代表性实测替代其余服务实现。需要先扩展 Provider 权威源与适配，不直接删除限制 |
| 旧轮次结果无查看入口，指定旧轮次仍带最新名称快照 | `useMarketChat.ts` 只 observe 最新；Native `observe.rs` 的 display 独立取最新提交 | 本次补正式有界历史索引、按原轮次名称显示、按需读取；只读且不恢复审批或工具能力 |
| 未知审批决定在切换会话后丢失本地防重发状态 | `useMarketChat.ts` session watch 清空 uncertain | 保留当前作用域内按会话隔离的未确认决定，原回执未确认前不再次发送 |
| 无可用连接与运行环境不支持共用文案；未实现安全配置入口却写“通过入口设置” | `ChatConnectorControl.vue`、`market-connectors-ui.ts` | 区分状态，明确当前能力，避免让用户寻找不存在的入口 |
| 包状态过时 | feature.yaml 同时写真实查询 PASS 和“未发金融业务/模型”“Tushare授权失败” | 更新当前状态，保留时间线证据，不改写旧失败 |

本次历史扩展 `contract-impact = semantic`：修正既有指定轮次读取的名称语义，并以 optional response 字段补只读索引；旧读者允许额外响应字段，新读者兼容缺省索引。请求形状/审批权威/持久格式均不变。先 Contracts source 和生成，再 Native/UI；无新迁移、无 Runtime 修改。

## 51 项接入的真实差异

来源表实际为 44 个 HTTP OAuth、4 个 HTTP 自备凭据、2 个 Google stdio、1 个淘宝网关。来源文件摘要的数量有误；按 51 个实际条目计数。参考地址不能自动成为易界已登记的应用身份。

- 44 OAuth 中当前只实现 Tushare 的授权与一个经过完整 schema 约束的只读工具。通用 OAuth、动态工具资格/风险策略、服务级 origin/scope、写操作幂等并未完成。Todoist 官方已有标准远程 OAuth 入口，可作为通用实现的协议依据；本轮不发起其账号授权。
- 4 个自备凭据服务需要各自确定传递方式及 worker 内安全输入路径。FTShare 官方已有 MCP 文档；不能把另外 3 项的 `none` 推断成无认证。
- Google Calendar 上游仍使用 credentials 文件和 tokens.json；普通私有目录不满足既定 Keyring 边界。Google Maps 需固定包与 API key 注入、正常 EOF owner。已有 byte bridge 资格不等于这些包已集成。
- 淘宝地址属于千问网关，不能用其身份代替易界应用。需淘宝开放平台接入依据与易界应用注册配置。

官方只读资料：[Todoist](https://developer.todoist.com/api/v1/#tag/Todoist-MCP)、[FTShare](https://github.com/FTShare-Lab/FTShare-MCP/blob/main/README.md)、[Google Calendar](https://github.com/nspady/google-calendar-mcp)。没有访问其他账户或发起业务查询。

## 执行顺序

1. 修复历史结果、未知审批恢复及误导文案，执行契约方向兼容、Native 和 UI 专项。
2. 将 51 项按实际适配和外部前提登记，给出每项缺口；复用现有 Broker/OAuth/Keyring/EOF owner 扩展 provider，工具调用仍须明确风险、参数和单次审批。
3. 用标准应用重开现有 Tushare 会话验证历史及管理恢复，不为旧诊断重复消耗付费额度。
4. 根据实际代码与证据更新 AC；未实现项继续列缺口，不将代表性 Tushare 成功写成全需求 D4。

全程不强杀、不篡改运行时/可执行文件、不破坏权限、不使用攻击 fixture，不提交、推送或发布。

## 逐项审计结果

全部51项已逐项核对，结果见[Connectors代码审计](../../../../yijie-connectors/docs/market-provider-code-audit-2026-10-08.md)与其JSON来源摘要。缺口是非Tushare分支未实现，不是缺少50项真实调用。Owner再次明确不执行这些服务的真实登录/调用，后续不得把逐项真实验证放回验收门槛。

## 本次修复与验证

- Contracts 增加兼容旧响应的 optional `availableTurns`/`turnsTruncated`，最多128条；Native从已有SQLCipher绑定读取原名称，指定轮次只读，不新建历史库、会话或执行授权。无市场提交的普通会话不访问Host。
- 界面能选历史轮次，当前审批继续使用实时观察；旧读取在导航/新选择后迟到会丢弃。未确认决定按会话保留，缺少回执不推断成功/失败、不再次发送决定。范围是当前ChatPage生命周期内；Native最终审批权威和防重复不依赖这层内存。
- 非Tushare尚未实现入口的文案不再引导用户寻找不存在的安全配置；未启用时提示先启用，不再一律称运行环境不支持。
- 本地专项：前端4文件22项、Host契约JS8项与Go包、Native观察4项、Native all-target Clippy、Desktop lint/check:native、标准应用构建通过。Native新增测试曾发现测试样本SQL整数类型和选集摘要错误，修正为合法合成样本后通过，未触碰真实数据。
- 标准应用通过正常⌘Q/EOF退出后重建，readiness=ready；重开原Tushare四轮会话，历史菜单显示4个原轮次。选“往前第1次”读回09:31批准成功的原始结果（000001.SZ/20260105/close=11.5），最新轮次仍是09:32拒绝且未发送的原始说明。没有恢复旧审批按钮，没有发新模型或外部查询。
- 本次只修复以上缺口，**未把其余50项执行适配标为完成，未标整体D4**。下一项应直接做通用provider执行，不重复构建51个真实服务验收流程。

当前通用执行的具体选择见[15](15-generic-provider-execution-plan.md)。已向Owner请求工具准入语义选择；等待期间不扩大现有白名单或执行权限。该选择与50项是否真实验收无关，后者已确定不执行。Host 9个FEAT157 Market专项race回归通过；一次错误的`^TestMarket`过滤无匹配，未计为测试通过。固定Runtime哈希、Desktop受保护店铺三文件差异摘要均保持原值。
