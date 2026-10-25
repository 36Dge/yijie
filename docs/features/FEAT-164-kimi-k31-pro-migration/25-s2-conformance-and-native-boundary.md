# FEAT-164 S2 时序矩阵与Native/Host本机边界

Owner要求审计当前进度与未完成项后继续。当前源基线：Desktop2a746c1、Host3c528985、Contractsf2819c66、Runtime074417e5 r2；完整SHA和原改动在evidence/s2-conformance-start-baseline.json。原账本、预占、活动S1 App和日常库保持，不新增真实模型HTTP；只本地提交，锁屏UI继续NOT RUN。

审计：S1源实现/本机部分已完成但平台延期；S2已有Store11/SQL38—40、v2模型选择恢复、独立派发证明和显式取消，TCONF-164-02仍是未创建名字。S3计划领域与S4调用面尚未实施，三个final未通过。06/07顶部仍停留23，需同步最新24/25；不能把旧G2V或工程子集当作完整Gate。

本批预定contract-impact=none（只补测试/资格driver与证据，不新增wire、持久格式或产品行为）；整体需求仍breaking。若真实联调发现产品缺陷，先在此重新评定并按既有方案修复。使用固定真实Runtime、真实Host handler/service/store及Native Repository/HostBridge，独立临时目录与普通loopback响应；不更改生产端点白名单、不借当前S1 fixture、不覆盖活动bundle。不用假可执行程序或强杀制造窗口；窗口使用已有正常状态fixture，真实子进程只正常EOF退出。

执行顺序：固定可执行TCONF入口并审查安全子例 → 补跨进程Native/Host/Runtime测试及原生正常重开/原回执/无重复模型请求断言 → 逐项运行并核验非零命中 → 审计来源、数据与退出 → 专属本地提交及治理记录。市场/专家取消沿各自领域验证；新模型业务执行的完整调用面留S4，不为验收开启禁用能力。测试中loopback模型响应不等于真实供应商资格或App平台通过。

## 实际结果与来源

本地Host `57c29ea03e3de39161a7c28080f9388f00cd1735`仅新增2个测试文件；Desktop `ddc840f7ed642216bca4b42ab6327d388aa73084`共5个文件，增加Native分阶段边界测试/组合driver、把旧带数据迁移矩阵从SQL38扩到40，并用既有canonical freeze脚本同步Host来源锁。产品wire、持久格式、Runtime和业务实现没有更改，contract-impact保持none；不是新发布。两个资格工作树在最终组合执行时均干净，来源见[最终结果](evidence/s2-conformance-final/result.json)。仅本地提交，不推送，隔离审计见[s2-conformance-host-isolation](evidence/s2-conformance-host-isolation.json)和[Desktop隔离](evidence/s2-conformance-desktop-isolation.json)。

TCONF-164-02由原计划单一Go入口扩为组合driver：保留精确`TestFEAT164MigrationReceiptAndRecovery`，同时强制Native配套。执行前段落记录了入口；当前机器字段使用实际完整driver命令，避免单仓PASS掩盖跨端未执行。最终五组均退出0、零skip：

| 检查 | 结果 | 范围 |
|---|---|---|
| Host时序 | 25个test/subtest PASS（包含父级） | 旧v1回执字节、未完成意图、prepared/apply_dispatched/receipt_validated/uncertain、原请求/线程/revision、其他工作阻断、Store7/8/9/10→11及旧reader拒绝 |
| Host路由 | 2项PASS | bearer/原操作绑定、封闭请求、退役只读与新执行拒绝 |
| Native派发 | 12项PASS | 普通/市场/专家独立证明、从未发送取消、原始事实保持、最终发送守卫及重复禁止 |
| Native恢复/迁移 | 10项PASS | 旧pending不回填、原回执/当前selection及带数据15/29/37/38/39/40→40、重复迁移和原迁移账本保持 |
| 真实本机边界 | 1个Go测试、内部2次精确Rust测试PASS | 实际Host handler/service/Store11、固定真实Runtime、Rust Repository/HostBridge/SQLCipher40；正常停止及重开、原回执与更高当前revision、取消零turn POST |

最终边界只产生1个普通MiniMax本机合成响应，外部模型0；准备阶段Host已提交Kimi选择、Native仅保留dispatched，不伪造失败或用强杀形成窗口。正常退出后更换Host实例/端口并重开相同临时存储，Native通过原operation回执同步，再明确切回MiniMax；旧回执revision2与当前revision3分别保留，thread和原派发fingerprint未变。取消新queued回合后尝试正常发送路径被Native挡在POST前，Host累计turn POST仍1。当前S1 App与18083 fixture未参与此组测试。

测试bootstrap使用独立loopback Provider地址，保留两provider请求/流重试为0，固定真实Runtime自身验证manifest/binary；未更改产品18083白名单、CLI、端点、凭据权限或capabilities。使用普通合成key，不读取真实key；不启用工具/图片/专家业务能力。Runtime通过正常stdin/EOF关闭，HTTP与SQLCipher正常退出，失败时driver保留日志而不强杀。三个本轮运行各1个合成响应，最终新鲜组为1；没有增加真实账本次数或释放预占。

Host make lint、2项路由专项、默认Native5项、cargo fmt/产品Clippy、driver语法及固定来源检查通过；原全targets Clippy位置问题与24的ChatPage文案基线失败未扩散修复。两次草稿组合和最终干净来源组合均PASS；草稿1之后审计补齐SQL40带数据矩阵，最终还包含独立路由组。全部日志及原始哈希见[清单](evidence/s2-conformance-log-manifest.json)，无空跑和skip转PASS。

## 剩余项与下一步

TCONF-164-02现在PASS；S2整体G3仍未通过。仍缺当前源码canonical App构建/旧隔离历史迁移、实际UI/亮暗/1180×760/权限交互、原S1暂停/MiniMax/正常清理，以及对应完整平台/freshness。新测试是headless边界，不是完整AuthorizedApplication/UI链，也不证明新Kimi在市场/专家/计划业务的全调用面；这些受S4与各领域门禁约束。日常库没有迁移。

下一可离线步骤是S3计划领域退役保护：先审计实际worker接管/claim/send、计划授权与future slots，在原领域事务暂停/撤有效授权，保持历史run/grant/额度事实；再实现显式迁移及重新授权。S4全调用面与三个final随后推进。沿用Owner对锁屏相关步骤的顺序例外，不把延期改成PASS；用户回来先正常退出当前S1 App，再canonical构建与补平台验收。真实模型新增许可仍0，旧30元账本/14.188544元预占保留。

## 治理与保留性复核

包strict/claims、元仓lint与53项治理测试通过。首轮G3诊断指出TCONF提交集少列S1两个传递来源；已用git merge-base确认它们是当前Host/Desktop祖先，补入来源集合。这表示来源依赖，不是重验旧App；最终G3仍因S1/S2平台、Harness及slice freshness未完成而拒绝，不能改写为通过。初次诊断和修正后结果均保留于s2-conformance-governance记录。

[保留审计](evidence/s2-conformance-preservation-audit.json)核验620个已有文件（本轮快照495项及前轮补充125项）：618逐字未动，Native共享mod.rs与memory仅当前需求差异经逆向/段落核验。42个活动App文件和两份真实账本哈希全同；原18083 fixture仍1请求、App readyz200。原各仓分支/远端不变，提交没有混入FEAT162/163，所有原索引在治理暂存前为空。
