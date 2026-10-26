# FEAT-164 S4X：日常候选实现与安全离线验证

2026-10-26。Owner已批准50列明的8个Desktop实现文件及对应测试/文档，并明确“不迁移日常库”。本阶段实现、独立canonical准备构建和安全离线验证完成；真实日常App未启动、日常库未连接/解密/迁移，真实模型HTTP新增0。整项FEAT-164仍IN_PROGRESS，不能把该候选视为日常已切换。

## 实现与来源

Desktop仅本地提交`ec1ab631d76d2f6ba2c74e25eaac1ea60339dfb4`，位于`feat164-s4x-daily-candidate-20261026/yijie-desktop`，基于已资格化9f5814f。修改恰好50号批准的8个实现文件，加1个测试及3个说明文件，共12文件。原主Desktop fd0c575及100份dirty、其它需求差异未应用或覆盖；本候选不包含那些未提交变化。旧source-pin冲突通过独立使用已固定来源避免覆盖，尚未宣称已合入原日常工作区。

增量contract-impact=semantic，权威为Desktop私有部署接口/既有持久兼容；公共wire/新schema N/A。整项breaking保持。Contracts ca06d0999c9a08afe80ab3f34a537d492b830ac7 → Host8cd6bccbdc1ac3906aea53d95441299f7cfefcce、Runtime11fd4504c28afd0f65c6f5f62a6b5328dd437f5a r5、Connectors cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9、Skills595c927ae101d3d31c234f60565041eee0864680不变；没有Runtime核心/补丁、依赖或锁文件变化。Owner的第50号确认覆盖本次私有consumer/权限范围，不冒称独立人工评审。

- 新显式`--packaged --kimi-k31-daily --prepare-only`保留日常identity、完整market/expert/media与默认workflow编译装配，独立输出到新源码目录；prepare-only不启动App、workflow服务或模型，不依赖真实模型/workflow凭据。
- 新`--migrate-daily-k3`仅为后续明确授权的维护动作：同一canonical App、固定`com.yijie.ai/demo-fast-v1`，精确参数与local/model/compiled K31/daily flags配对，维护在auth、DatabaseWorker、sidecar和UI之前返回。无自选数据路径。
- 日常父目录允许既有0700/0755，chat/secrets仍0700；不修改旧目录权限。沿用全局单实例、无打开句柄、完整加密备份、只读副本预检、正式迁移/计划退役和正常close。
- 保留unknown、未决/在途、reservation、occupied grant及非终态原生事实拒绝；不清零、退款、自动重发、手工checkpoint或清WAL。Desktop向Host仅传递已审日常组合的冻结predecessor准入，不产生turn/计划授权。
- 复审修正了两个实际问题：凭据缺失的prepare-only不再记录不可正常重开的provider-only配置；编译了K31的daily binary即使缺少candidate环境也拒绝隐式旧装配。正常启动的凭据/服务要求没有降低。

## 验证及保留的失败

| 分组 | 结果 / 适用范围 |
|---|---|
| Node入口/四隔离组合/日常完整组合 | 8项PASS；无效操作配对在准备前拒绝 |
| Native编译identity/flag与feature-off | identity 2项、feature-off 1项PASS；拒绝发生在数据库访问前 |
| 自然SQL29/37 → 隔离/日常入口 | 四组合PASS；正常锁竞争、held保持、备份逐字一致、旧事实/授权、退役、重复维护/兼容重开均验证 |
| S2原生delivery/recovery | 12＋20项PASS |
| S3退役/重审/授权/暂停/重放/worker顺序 | 5项exact PASS |
| 源码/前端/文档 | 19项FEAT164只读生成检查、fmt、产品lib/bins Clippy `-D warnings`、pnpm lint、docs:build PASS |
| canonical独立日常prepare-only / 同源回执 | 构建exit0、直接只读receipt --check exit0；无App/模型/实际日常数据启动 |

元仓schema/严格包检查、manifest lint、53项测试和7个shell逐文件语法检查通过。

以上测试分组有交集，不相加声称唯一总数。ignored标记的维护测试用`--ignored --exact`显式执行且实际1 passed/0 ignored，非跳过当PASS。没有跑含禁止故障/攻击用例的全量测试，也不声称全仓make/远端CI通过。

SQL37首次验证配置只启用媒体，实际自然生成SQL36；预检发现后没有迁移该错误样本。原目录保留，在新目录加入既有market开关自然生成37后两入口通过。首次source检查缺少旧Skills的固定checkout；首个补齐脚本又遗漏.local父目录，shell继续导致同一检查第二次失败。核对三份干净既有固定来源、补齐父目录/链接后，第三次完整19项通过；没有改锁或产品来绕过。

扩展`cargo clippy --tests -D warnings`失败于未修改基线`native_conversation_storage.rs`的items_after_test_module；逐字确认与9f相同，未扩大8文件范围、未加allow或压制warning。产品lib/bins严格Clippy通过，测试代码全目标Clippy仍记录FAIL_BASELINE。该基线问题不伪装成已修复。

迁移矩阵先在有逐文件hash的未提交候选执行，随后本地固化。其后收紧的compiled identity条件已单独复验，迁移权威文件逐字未变；脚本/receipt最终字节由canonical构建及回执覆盖。详见s4x-verification-source-binding，不把这些分批验证冒充一次fresh完整App运行。

## 新产物与旧资格边界

| 项目 | 当前结果 |
|---|---|
| 日常App identity | `com.yijie.ai` |
| App SHA-256 | `edf9a13820819aaeb260d216cddeb7e5291214be7cc17b76c6f67764a5f227d4` |
| 包内文件 | 119，资源内容与固定slot逐字核验 |
| 同源回执 SHA-256 | `c4401b7ebf04f997bdd4a704dca3070a5c1d14d5b94616704aeb96a270f4d657` |
| Runtime r5 SHA-256 | `283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e` |
| Host SHA-256 | `1d880cb0f6b990940583abf875fc9b7c551e1135174d675f3caae43ed6f0118c`，与既有资格Host一致 |
| worker SHA-256 | `8fda415d596caa24c13dab8a3f3ce5765013e0a94f0ae36739b9e43f2f6660f8` |
| artifact adapter SHA-256 | `dff26bf712e993f7b828bc96186ecedd3ca53f5ab5b9ec0c4f64e3ddc8c56bc9` |

产物在新源码标准target的`易界 AI.app`，未覆盖旧App或任何已签名/已发布产物；这是未签名本地开发包，不是发布。构建日志证明workflow overlay与FEAT164资源overlay被传入；receipt绑定VITE workflow=true和daily开关，prepare-only跳过workflow-up及凭据读取。回执直接只读检查，无需用会启动App的`--reopen`。

49的真实r5文本、46—50的S1—S3 G3/正常teardown结论继续只绑定Desktop9f的隔离资格App42a23cf…；本日常候选的Desktop代码和部署identity已变化，**不得自动继承为新日常App G2V/G3/final PASS**。旧机器证据槽保持原来源，本次独立登记OFFLINE_PREPARED_NOT_ACTIVATED。S4完整TCONF04、真实图片/搜索/工具及unknown/never-sent完整GUI仍为缺项。

## 保留性与下一步

本轮核验11953份旧App数据/制品/回执/账本文件逐字保持、497份原dirty保持，混合memory去除本轮新增块后亦逐字保持（合计498份）；六个候选来源干净。实际日常库仅沿用原保护清单做原始文件hash核验，没有数据库连接或解密。无活动项目服务，18081/18083/18086无监听；新构建目录host-home/codex-home未由进程运行。全部三份模型账本、历史请求及14.188544元预占保留，累计真实请求仍6；本轮0新增、无精确价格门禁。原30元约束及必要功能调用授权仍有效，不把本次离线限定改写为永久禁令。

下一步先以新日常部署源码在**固定隔离资格identity**补齐适用同构建业务验收与S4剩余功能证据，避免直接用真实日常库试错；不重新安排Owner移除的亮暗、键盘/焦点、最小窗口专项。随后提交真实日常完整加密备份、只读副本预检及受控维护的具体执行清单，取得对应授权后才可访问/迁移/启动真实日常库。当前尚不掌握日常schema/unknown/grant事实；occupied_runs保守拒绝不擅自放宽，若触发先审计终态与原reservation关系。

仍只本地提交、不推送/发布。私有完整验证数据、备份、失败日志和原始构建回执位于`feat164-s4x-audit-20261026`及新候选目录；不把数据库或密钥提交Git。批准的实现/离线准备阶段已完成，整项尚未完成。
