# FEAT-164 UI延期与S2离线基础实施

2026-10-25 Owner明确表示本人不在电脑旁，允许需要解锁的实施/验收先延期并继续后续步骤。解释为允许离线工程推进，不把未观察到的产品行为写PASS；S1 required vertical、Harness正控/最终清理及G3仍保留未完成。该决定覆盖21中“不进入S2”的工作排序限制，不修改全局门禁、不授予发布资格。真实模型HTTP新增0；只本地提交，保留已有工作区、旧账本与14.188544元预占。

## 当前审计与顺序

`contract-impact = semantic`，整体需求仍breaking。本批消费固定Contracts f2819c66的chat-models-v2；无新公共wire。Host私有持久操作增加版本化恢复事实，Desktop迁移验证使用本仓已有0038权威源。源格式、旧reader拒绝、暂停兼容reader及正常重开分别验证，不将SQLite迁移测试等同日常数据迁移许可。

1. Host原v1选择的未完成同ID分支绕过revision、活动turn、审批及其他未决工作检查；v2仅有catalog/current selection，操作读取/显式恢复未接通。
2. 先完成原终态回执只读保真、完整恢复绑定和重复前置检查；prepared/apply_dispatched/receipt_validated/committed/uncertain分别持久化。未完成旧v1操作保持unknown，不能拿新目标接管或假定never-sent。
3. 离线验证旧SQL15/29/37→38及38重复打开，检查已有内容、模型快照、digest、nullable、PK/FK/CASCADE和migration ledger。不开放现运行App旧库入口。
4. Native模型选择/恢复接线、普通/市场/专家never-sent取消、计划退役/claim-send和S4全调用面仍需逐项完成。取消需要真实持久派发证明；既有queued/404不是证明，不能先解除阻断。

当前App仍在运行且锁屏。禁止覆盖其canonical bundle/实际可执行文件、强杀或绕过锁屏。基线包含活动bundle逐文件摘要，离线测试仅使用临时存储和本机构造数据。未运行新App、未执行新平台纵向验收，也不以旧G2V替代本批fresh证据。

本轮源状态及所有已有未提交文件摘要见evidence/s2-start-baseline.json。完成后追加精确实现、检查、保留性审计及剩余项。

## 本轮结果与复审

Host本地提交 `3f6b609bc9755f9125636317209f4de07a867590`，14文件；Desktop `83f467b568f6dad03ccb31efe6ff3ddf3673a6d1`，2文件（新Host来源pin与带数据迁移测试）。Contracts/Runtime不变。不存在推送、发布、日常数据库迁移或App重建。

Host实际新增Store11 envelope，保留base schema7/8/9/10及旧v1操作字节；新v2 bucket保存原profile/thread/revision、各阶段及完整thread/model/provider/effort回执。旧reader拒绝11，新候选执行暂停时仍保留兼容读取。原终态回执在实时可用性检查之前只读返回，不装饰v1 result，不回退当前更高revision。旧v1未完成意图缺派发/thread证明，保持unknown，不重配；候选v1新选择拒绝。重复v2 select POST也不重配，必须显式recover原operation，逐次复核自身绑定与所有其他未决工作；标题生成与候选模型切换串行，避免辅助请求跨切换。

当前仅普通session可新选/恢复，market/expert/draft仍受原开关与用途限制；Native begin_model_selection仍保持候选禁止分支。没有把Host能力视为Native产品接线完成，也没有借模型迁移开启其它业务面。

测试及精确命令在evidence/s2-host-verification.json和s2-desktop-verification.json。Host定向race组、make lint及契约固定来源检查通过；实际固定Runtime完成普通合成MiniMax回合→同thread新Kimi选择→正常Runtime/Store关闭重开→已完成回执只读重放→新操作MiniMax选择。最终组1次loopback HTTP，外部0；此前同源联调及复审各1次loopback，故本轮该新测试共3次本机合成HTTP，不进入真实账本。Desktop候选5项/default4项、cargo fmt与产品lib/bins Clippy通过；新测试逐条比较15/29/37/38升级前所有已有列，保留消息、操作profile/revision、payload bytes、pending/inflight/done与attempt_count、既有migration ledger及FK。原独立0038测试继续覆盖nullable及PK/FK/CASCADE。没有声称已验证不存在于普通outbox的独立digest字段；原业务payload bytes与模型快照不改。

初次Go测试unused import、Rust格式及SQL15 SELECT *列数oracle差异已修正；保留s2-iteration-history.json和初次测试日志。首次来源校验未带候选环境被门禁拒绝，随后按明确local候选环境检查通过，未绕过门禁。此前全targets Clippy和全量make lint独立旧问题仍未修复，禁止的全量fixture未执行。

## 剩余项与下一步

1. Native先增加可区分原v1/new v2的持久选择intent，再接source-defined operation只读查询及显式recover。旧pending不能依据目标恰为MiniMax而重分类。原终态回执后单独读取当前Selection；不覆盖更高revision。
2. 取消前先增加普通/market/expert持久派发阶段与attempt事实。审计确认普通重试路径会将attempt_count重置0；因此queued+0不够。不能从404/缺记录/空历史推出never-sent；旧不确定请求继续占用且可读，不删除chat或改payload/profile/digest。需要保守旧数据分类与domain事务，再接UI。
3. 完成这些Native边界及worker准入后，才开放旧隔离库迁移入口；日常库仍未授权。S3计划退役/授权迁移和S4全调用面继续按原设计，不直接改计划profile。
4. 用户回到电脑旁时先正常退出仍运行的S1候选；保留其历史证据。随后才可按新精确来源canonical构建，并补延期的暂停/MiniMax/历史/UI/最终清理，以及新S2产品验收。当前同构建reopen会因源码pin变化失败是预期保护，不能修改receipt或覆盖bundle绕过。

Owner延期只改变工作推进顺序。S1 required vertical/Harness、S2全slice与TCONF-164-02、G3/G4/final保持未完成，不以本批Host/SQL测试替代。

## 最终复审固化

Host `3c5289854d88ca6ed69b17bd806fca2efc0bbbcd` 进一步把已完成操作重放移入真正只读事务，回归检查bbolt写计数不变；Desktop `189019ec5d9f1d7d419b2edf35e6ce53a40be12b` 随即固定该来源。最终race组（含实际Runtime正常关闭/重开）、lint与固定来源校验再次通过。本轮合计Host两笔、Desktop两笔本地提交。Native产品接线仍未放行，现运行S1 App产物未重建。

保留性审计覆盖620个起始已有文件：618逐字未动，Host共享store.go专属补丁逆向复核及memory仅FEAT164段逆向复核均精确恢复起始字节。42个活动App文件哈希全同；旧账本及快照哈希全同，候选/fixture仍为正常ready/health200。元仓lint/test、strict和claims校验通过；S2 G3按真实未完成项拒绝，未修改全局门禁。见evidence/s2-preservation-audit.json、s2-governance-verification.json。
