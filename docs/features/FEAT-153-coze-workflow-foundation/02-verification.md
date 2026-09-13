# FEAT-153 验证与未完成项

当前收口结论：2026-09-13 最终本地候选统一 D4 通过，见[最终验收](17-d4-final-qualification.md)。下文保留各阶段的原始事实与当时状态。

当前统一D4进度见[13](13-unified-d4-qualification.md)：2026-09-13 10:41候选已冻结，标准dev与受控栈已启动，人工A/B等待实际反馈；工程定向检查已通过。下文12为前序packaged资格，不等同本轮统一D4。

2026-09-13最新结果见[12](12-full-app-theme-size-qualification.md)：packaged真实创建/编辑/保存/重开/试运行/两次内部发布/指定旧版执行/结果历史通过，light/dark×1180×760/1440×900均有真实CUA与原生尺寸证据。暗色画布及取消Chat导航标题问题已修复复验；149前端定向测试、13native测试、标准构建通过。B两版/四run与两库一致，正常App和栈重开后完整读回相同。当前dev完整页UI仍受CUA无法识别裸进程限制，已由用户正常退出；D4保持NOT RUN。

历史最小真实 App 资格见[10](10-step5-real-app-qualification.md)：dev 与 packaged 均完成真实创建、节点/连线编辑、保存、返回重开；dev 完整草稿自然到期、显式重连再保存，以及两种入口 native 关闭确认和 Chat 切换已实测。API/两库读回一致，91 个公开/包产物凭据匹配 0。标准正常退出和受控清理完成。5.2/5.3 最小资格通过，首次手动 fit 等体验限制保留；5.4 与整体 fresh D4 仍未执行。下方均为所标历史步骤的事实。

此前第5步无界面检查见[09](09-step5-headless-progress.md)：Coze11项、Desktop12+6项、API qualifier4项及自然301秒真实会话、packaged标准构建/进程启动退出、6资源HTTP和90文件凭据静态检查通过。前述各层结果不替代真实WK资格；当时用户将解锁依赖留待后续，D4仍NOT RUN。

日期：2026-09-12。第0—4步及最初第5步证据按时点保留。[08](08-step5-desktop-integration.md)记录解锁前的构建、源锁、受控静态部署及启动检查；当时 Mac 锁屏阻止实际 UI 操作。后续实际结果由09、10分别更新。D0保留PASS、D4 NOT RUN；本页下方历史状态只对应所标步骤。

## 第1步已执行检查

| CWD | 命令/检查 | Exit | 实际结果 |
|---|---|---:|---|
| yijie | pnpm lint | 0 | 清单 11 子仓、中央及 11 份 sibling AGENTS 通过 |
| yijie | pnpm test | 0 | 50 tests、50 PASS、0 FAIL；只覆盖元仓治理 |
| yijie | bash -n scripts/*.sh | 0 | 元仓 Shell 语法通过 |
| yijie | make contract-governance | 0 | require-siblings 检查完整 11 个子仓 |
| yijie-coze | make lint | 0 | 源 origin/基线祖先/tree、接入规则与 diff 空白通过；上游应用 lint 未运行 |
| yijie-coze | make test | 0 | 15,298 未改源文件 + 1 份只追加目标的 Makefile + 6 份保留缺失；不是引擎测试 |
| CrossBSD | 原状态及逐文件 SHA-256 对照 | 0 | Desktop 8 份既有文件不变；原有其它 10 仓 HEAD/branch/origin/status 不变 |

执行摘要和时间：[step1-verification.json](evidence/step1-verification.json)。状态：[接入后快照](evidence/workspace-after-step1.json)。接入前源字节审计和 Git 恢复后的源树检查为两类证据；shallow fetch 不等于完整历史。

## 第1步时的Must AC（最新状态见文末）

| AC | 状态 | 证据或缺口 |
|---|---|---|
| AC-001 | PASS | 来源/清单/Git/已有改动检查；本地接入已完成，无 commit/push |
| AC-002 | NOT RUN | 工作流公共源契约与 provider/consumer 尚未实现 |
| AC-003 | NOT RUN | 新 local native/server/session 具体设计尚未批准 |
| AC-004 | NOT RUN | React editor、WKWebView cookie/CSP 尚未实测 |
| AC-005 | NOT RUN | 真实创建/保存/重开/revision 冲突尚未实施 |
| AC-006 | NOT RUN | 试运行/内部发布/版本读回尚未实施 |
| AC-007 | NOT RUN | 版本执行/结果/节点/历史尚未实施 |
| AC-008 | NOT RUN | 节点范围/限制、普通错误修正重跑尚未实施 |
| AC-009 | NOT RUN | 固定版本 local 栈 readiness、正常 stop/start/持久化未验证 |
| AC-010 | NOT RUN | 本次 UI/键盘/新增可访问性未验；原配色及模型/平台调用 0 已保留 |

## 真实服务与代表性失败

Startup / happy path / representative failure-retry 全部 NOT RUN。当前步骤尚未进入服务实现，没有用 mock 替代。未来在同一 canonical Desktop 完成无外部副作用的三节点创建→保存→重开→试运行→内部发布→执行→历史，普通输入校验错误修正后再跑。短流程完成后才正常停止重开，只核验已完成记录持久化，不证明在途恢复。

## 未执行的项目、原因及影响

| 项目 | 原因 | 影响 |
|---|---|---|
| 根跨仓 make lint/test/generate | 下游链含 injection fixture、zip-slip 归档和权限故障；用户禁止 | 无全仓绿色；后续使用已审查的 safe/focused 检查 |
| 强杀、权限破坏、攻击资源/注入 | 用户长期硬规则 | 不验证攻击或注入式恢复，不伪造通过 |
| Coze 上游完整构建/测试、Docker、UI、真实三节点 | 第 2 步具体设计未批准，实现未开始 | 只有静态可行性和仓库接入证据 |
| 公开多租户、真实身份/商家数据、模型或平台调用、生产认证 | local 合成范围明确排除 | 不证明 ERP/AI/生产或所有依赖安全 |

既有青柠说明 contrast 1.28:1 / 1 项 serious 只引用既有记录，本轮未重跑、未修色。不得继承 FEAT-151 旧 D4/0 axe，不把限制隐藏在新功能 PASS 中。

## 第 1 步结束时的 Gate（第 2 步更新见下方）

- 需求结构/声明检查：`check-feature-package.sh --strict`、`validate-feature-package.mjs --audit-claims`
  实跑 exit 0；9 份 Markdown 的 15 个本地链接及行尾空白检查通过。
  [最终校验与接入文件哈希](evidence/step1-final-review.json) 记录范围；结构通过不是用户批准。
- D0：pending，新 Tauri/编辑会话/固定资源方案仍需确认。
- D4：NOT RUN，9 项运行 AC 未执行，整体集成尚未完成。
- DP/生产：N/A，本需求不公开，无发布批准或结果。
- 独立实现审查：完成只读复核，两项 P2 修正见 01；不冒称独立人工批准。


## 第 2 步验证范围

第2步为设计收口，实际变更contract-impact=none，完整后续实现仍semantic。用户批准原话及范围已记录；ADR-0019 Accepted，05冻结具体设计。D0检查只证明设计/交付声明符合本项目门禁，不证明MessageChannel/WKWebView、API、Coze或数据迁移已经运行通过。

真实平台资格、业务Must AC-002—010、服务启动、正常三节点、代表性错误修正及停止重开仍NOT RUN。AC-001保留第1步已有证据；模型/商家/付费调用0，无强杀/权限破坏/攻击资源。下一步是第3源契约与最小provider/native-session。

### 第 2 步实际结果

| 检查 | Exit | 结果 |
|---|---:|---|
| check-feature-package.sh --strict | 0 | PASS，当前四文件结构与语义 |
| check-feature-package.sh --gate D0 | 0 | **PASS，设计门禁** |
| validate-feature-package.mjs --audit-claims | 0 | PASS，未伪称 D4 或真实运行 |
| yijie pnpm lint / pnpm test | 0 / 0 | PASS，11 子仓治理及 50 项元仓测试 |
| yijie-coze make lint / make test | 0 / 0 | PASS，仅接入规则与源保持；不是 Coze 应用测试 |
| git diff --check、13 份文档/26 个本地链接检查 | 0 | PASS；无行尾空白或无效本地链接 |
| 原有工作区保护 | 0 | 其它原有10仓状态与8份Desktop文件保持 |

原始命令日志：[step2-checks.log](evidence/step2-checks.log)；机器索引：[step2-checks.json](evidence/step2-checks.json)；
审查与保护：[step2-review.json](evidence/step2-review.json)。独立设计复核的五处修正已关闭，未作独立人工批准声明。

**当前 D0 PASS，第 2 步完成；D4 NOT RUN。** 未启动服务、执行 migration、生成工作流公共契约或实现 provider/native/UI，未 commit/push。

## 第 3 步最终验证

第3步源契约、最小API/Coze服务端和原生会话桥接候选已完成。**以下PASS只属于源码、正常定向测试和标准开发构建；D0保留PASS，D4仍NOT RUN。**

| 仓库/范围 | 命令或检查 | 实际结果 |
|---|---|---|
| Contracts | generate:safe、check-generated:safe、完整lint、test:workflow | exit0；7项源测试PASS，11项lint warning保留（9项IPC-only组件实际由native/bridge消费） |
| Contracts | check-breaking.sh，固定811f38d... / f16a497... / 29317b6...三个完整baseline | 三次exit0；已有受支持族结构兼容；新族无已发布baseline，明确当前HEAD fallback |
| 三consumer | sync-workflow-consumer.mjs api/coze/desktop --check | 源/生成摘要与三独立candidate锁PASS，不冒称已发布pin |
| API | make workflow-lint workflow-test workflow-build | exit0；16项顶层tests+9项路由子例，race/vet/两项开发构建PASS；无真实PG |
| Coze | workflow-contract-check/lint/test/build，三包-race | exit0；9项正常tests通过，真实领域引擎+SQLite/miniredis；指定v1在v2发布后执行、5120字节结果及3节点输出、CAS/幂等/历史均有证据 |
| Desktop | cargo check、test --lib workflows::、fmt --check、clippy --lib -D warnings | exit0；10项native定向测试，普通HTTP consumer和正常生命周期；未启动App |
| Desktop额外静态范围 | clippy --lib --tests -D warnings | 被既有src/chat/mod.rs:1351 cloned_ref_to_slice_refs阻挡；未改该文件，不声称全目标PASS |
| Coze来源 | make lint/test、git diff --check | 15,297未改源文件、2个声明overlay、6份保留缺失；源保持检查PASS，应用检查范围另列 |
| 工作区 | 原HEAD/branch/origin、七个未参与仓、8份已有Desktop文件摘要 | 保持；旧API入口/public lock/global migration与所有依赖锁未改 |

详细命令、完整baseline和日志摘要：[step3-checks.json](evidence/step3-checks.json)。
原始证据：[Contracts lint](evidence/step3-contracts-lint.txt)、[Contracts tests](evidence/step3-contracts-tests.txt)、
[API](evidence/step3-api-checks.txt)、[Coze](evidence/step3-coze-focused.txt)、[Coze race](evidence/step3-coze-race.txt)、
[Desktop tests](evidence/step3-desktop-native-tests.txt)、[Desktop验证/限制](evidence/step3-desktop-native-verification.txt)。
保护与差异：[step3-workspace-review.json](evidence/step3-workspace-review.json)。

## 第 3 步后的 Must 与未执行项

AC-001保留PASS；AC-002—010产品完整验收仍pending。AC-002源/最小provider/native conformance与AC-005—008底层正常场景已有上述分项证据，不能把单元/依赖替代测试标成App端到端AC完成。

| 未执行项 | 原因 | 影响 |
|---|---|---|
| 真正PG/MySQL migration、行锁/事务、真实Redis/完整Coze初始化与受控Docker栈 | 按批准技术顺序留在第4步 | 不证明真实持久化、容器readiness或正常stop/reopen |
| Vue/React iframe、MessageChannel/WKWebView dev/packaged、CSP/导航/首次打开取消与视觉 | 第5步产品与平台资格尚未接入 | 不宣称工作流页已经可用；无App或浏览器演示替代 |
| fresh canonical happy path、普通失败修正重跑、正常退出重开 | 第4/5步依赖尚未完成 | D4 NOT RUN，未借用历史验收 |
| 历史危险归档/攻击fixture、强杀/权限或执行程序故障注入 | 用户永久规则禁止 | 只使用已审阅safe/focused链，无这些异常能力或全仓PASS声明 |
| commit/push/tag、易界Coze远端、公开/生产与付费/商家调用 | 不在本步执行范围 | 本地候选无发布身份；业务/模型/付费调用0 |

旧已完成写操作在草稿随后改变时，完整Workflow重放会返回原operation ID的unknown；独立operation查询仍返回真实completed回执。没有回传后来的草稿冒充旧结果，也没有在API复制第二份画布。首次open尚未得到bridge ID时的UI取消属于第5步；本步覆盖已绑定关闭和context变化时迟到open的正常撤销。

## 第4步最终验证

**服务与实库资格完成；完整canonical App验收仍NOT RUN，D4未执行。** 本轮最终事实及全部证据索引见[07-step4-local-stack.md](07-step4-local-stack.md)。

- 固定镜像和双采样本地构建、两库显式migration、六容器及宿主认证ready：PASS。
- 最终W3真实HTTP：4成功原生run、3内部版本、11 API receipt；MySQL58表、10已提交operation、3版本、4execution、12node与HTTP逐项匹配：PASS。
- 最终W4独立TCP普通并发save：1成功、1revision_conflict，真实草稿/回执读回及E关闭：PASS。
- PostgreSQL真实race集成：正常8并发Claim唯一登记、fixed scope/resource、正常审计、重新连接持久化：PASS。
- 同候选正常SIGTERM无限grace停止、所有exit0/noOOM、18888释放；新epoch同镜像/同卷重开，HTTP/MySQL/W4回执读回：PASS。
- Contracts7、API17顶层+9路由子例、Coze11（其中三包race10）、Desktop10、Infra10安全focused范围及适用canonical检查：PASS；不声称全仓或App通过。
- 原有Desktop八文件哈希及原六容器状态/启动时间保持：PASS。

初轮HTTP子检查虽通过，MySQL对账发现API save回执误带旧版本；该语义缺陷已按源澄清修复，初轮W1/失败证据和历史审计不改写，最终W3/W4是新的资格记录。首次internal-only无宿主端口、Dockerignore/tmpfs、轮换与构建重开等实际问题及修复均在07记录。

本轮最终服务栈停止、卷保留。正常Docker Desktop stop命令exit0、daemon socket不可达；早期默认凭据助手客户端仍等待，未反复发信号/强杀或修改登录配置，不宣称宿主进程全部清空。详情见step4-final-cleanup.json。

### 仍未执行

| 项目 | 原因和影响 |
|---|---|
| Vue/React iframe、MessageChannel/CSP、dev/packaged WKWebView与同App零登录 | 第5步依赖现在已就绪，但产品接入尚未开始；AC-002—010的App级部分仍pending |
| 亮暗/尺寸/键盘、普通UI失败修正重试、Chat共存、fresh D4全部Must | 第5/6步；不继承历史D4、对比度或Chat结果 |
| 攻击/危险归档/权限破坏/强杀/执行程序故障测试 | 用户永久条款禁止，安全focused不能替代这些异常或全仓结果 |
| commit/push/tag、易界Coze远端、生产/付费/商家服务 | 未授权且不在本期基础集成范围，预算0 |

## 第5步最小资格与完整产品页当前状态

解锁后的最小真实App资格详见[10](10-step5-real-app-qualification.md)：dev/packaged创建编辑保存重开、自然到期保留草稿和显式重连、原生关闭及Chat边界已实测，范围保持历史时点。

用户随后授权的完整产品页、首次自动fit源码已实现，构建和正常定向检查、受控栈恢复与旧资源读回见[11](11-step5-full-workflow-product.md)。本轮CUA两次报告Mac锁定，完整试运行/发布/指定版本执行/结果历史的真实App闭环及两主题/两尺寸未执行，已请求解锁。未用browser-only、直接API写入、旧截图或单元结果替代；AC-002—010完整fresh验收仍pending，D4 NOT RUN。
