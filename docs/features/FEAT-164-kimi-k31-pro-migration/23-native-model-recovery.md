# FEAT-164 S2 Native模型选择与显式恢复

Owner在22离线基础完成后要求审计并继续下一步。真实模型HTTP新增0、只本地提交、不推送、保留已有工作区与旧账本/预占、锁屏相关UI延期的边界延续；不覆盖运行中的S1 App，不打开日常数据库。

`contract-impact = semantic`，整体FEAT-164仍breaking。本批消费已固定Contracts f2819c66 chat-models-v2 0.2.0的SelectRequest/ModelOperationReceipt/RecoverRequest/Selection；公共Host/Runtime wire不变。Native私有SQL/IPC按本仓权威新增前向格式，不能更改0038及旧migration。

审计结论：Host3c52898已提供明确的新操作、只读回执与显式恢复；Desktop189019e仍禁止候选begin_model_selection。Native原pending没有请求版本/派发证明，普通refresh可能只看当前Selection而过早解除本地未决意图；必须先保存新v2原始绑定，再接入。普通outbox/market/expert never-sent证明及取消属于下一独立领域步骤，不能用本批模型选择intent替代。

本批实施顺序：新增SQL39私有v2选择intent，原数据不回填/不改；新操作绑定session/Host/thread/原profile/revision/目标并在POST前保存派发阶段。新select与recover分开，普通查询只GET；未派发且Host无记录可按原请求首次发送，已派发/未知且404保持阻断。完整原操作回执通过后再读当前Selection，防止原回执覆盖更高revision。旧pending不自动冒充v2。复用当前scope/SubmitTurn权限、Native串行入口和未决任务检查；不增加新网络目标或凭据权限。

验证使用正常临时存储、原生与前端定向测试、受控本机HTTP和标准构建工具。App构建不覆盖当前活跃bundle，亮暗/最小窗口、历史旧隔离库迁移及完整平台链仍待正常退出旧App后验证。全部未执行项保留NOT RUN，不提升S2 G3。

## 实际实现与审计

本地Desktop提交 `f341636e5935852ebbbd7d86c6b615e0dc8fad7a`，20个专属文件。Host `3c5289854d88ca6ed69b17bd806fca2efc0bbbcd`、Contracts `f2819c66a2368aaff37216a46c48d5cd81df1747`、Runtime `074417e5e2f5f55704ea5e1777e7a22d514076b4` 均未改；所有工作在干净资格工作树完成，再将专属patch应用到原工作树和索引。临时副本反向补丁逐字恢复所有原有改动，staged tree与资格树相同，见evidence/s2-native-isolation.json。

- SQL39新增私有intent/原回执表，逐步保存prepared/dispatched/unknown/committed。不把旧pending改成新v2。旧MAX38 reader拒绝39；新默认v1兼容reader对39模型派发/写入保持关闭。候选仅开放0/38/39，日常库迁移不执行。
- 新选择和显式恢复使用分开的Native命令。沿用原scope/SubmitTurn授权及异步后重验，POST还有生命周期停止/epoch保护。恢复参数必须等于Native保存的原请求；会话/Host/thread/原profile/revision、outbox/turn/草案/专家及预约门禁逐次检查。
- refresh仅查询Host事实；旧pending没有新证明时保持阻断。prepared+Host无记录才可首次发送原意图；dispatched/unknown+404保持未知。已完成回执先保真保存，再读取当前Selection，迟到结果不回退更高revision，不在同revision替换身份。
- UI使用原模型选择器，旧K3显示“已退役”；“刷新状态”和“恢复原切换”语义分开，后者说明未完成时可能重新应用原目标。重开恢复原operation，切scope/聊天后丢弃迟到结果。

真实模型HTTP新增0，旧预算与预占不变。只用了普通临时SQLCipher库、合成状态和localhost Host响应，没有替代可执行程序、攻击fixture、权限破坏或进程强杀。

## 验证

最终候选10项Rust测试（包含正常存储重开、旧pending无回填、派发404、同绑定/同revision、outbox/turn/专家/草案/换scope/换thread阻断、原回执及更高revision保持、HTTP方法/路径/nonce与停止门禁）、默认5项、前端15项、cargo fmt、前端lint/候选前端build、候选与默认产品lib/bins Clippy、固定来源检查通过。精确命令/时间/退出码分别见evidence/s2-native-rust-verification.json和s2-native-ui-verification.json。

审计补齐了v2 404错误解析及recover POST生命周期分类；初次测试私有字段访问、Clippy range与默认v1重复转换均已修正且保留日志。未修改全局规则/关闭lint。前端build有原bundle大于500kB提示；不是App打包或视觉通过。HTTP测试使用普通本机Host响应，不冒称本轮已做真实Host+Native+App全链；Host真实Runtime的既有结果仍按22来源保留。

未执行：新的canonical App构建/启动、锁屏UI/主题/最小窗口、真实平台恢复与旧隔离历史验收、日常库迁移、新模型调用、禁止的历史fixture；完整all-targets Clippy原source_reader_tests位置问题仍保留。本轮只通过相应工程子集，TCONF-164-02、整个S2 G3与final仍未通过。

## 下一步

先为普通/市场/专家请求补持久派发阶段及尝试事实，再做never-sent取消领域事务；attempt_count可被旧重试重置，queued/0/404/无记录不能直接释放占用。保留原payload/profile/digest和未知事实，不删chat、不把模型配置intent当业务发送证明。随后完成S3计划退役/授权迁移与claim/send、S4全部调用面。用户回到电脑后先正常退出旧S1 App，才canonical构建新来源并补延期UI；不覆盖活跃bundle。

## 保留性与治理复核

起始620个已有文件中612个逐字未动；7个Desktop共享文件通过专属patch逆向核验，memory仅FEAT164段替换后逆向恢复起始SHA。42个运行中App文件及两份真实预算账本哈希全同，候选readyz与fixture health仍200。见evidence/s2-native-preservation-audit.json。元仓lint/test、包strict与claims校验通过；S2 G3仍按未完成取消/平台等事实拒绝，无门禁降级。
