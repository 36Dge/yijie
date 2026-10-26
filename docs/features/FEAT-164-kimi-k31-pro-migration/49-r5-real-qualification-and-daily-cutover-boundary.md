# FEAT-164 S4V：r5真实功能资格、证据判定与日常切换边界

2026-10-26。Owner要求继续证据判定、r5真实资格及日常切换边界，并明确“需要调用就直接调用，无需精确计算，我要的是功能验证通过，逻辑没有错误”。本轮按此授权完成一次真实功能验证；价格精确核验不再作为前置门禁。整项仍IN_PROGRESS；日常库迁移、推送及新Runtime核心修改没有发生。

## 实际结果

当前同源App→Native→Host→r5→官方Kimi Responses→事件→保存→重开完整通过。新会话`01a17863-e581-7211-b735-3c160677762c`输入“FEAT164 r5 资格验证：计算17+25，仅回复结果42，不调用工具。”，实际答案42、App已完成。唯一新HTTP为200、kimi-k3.1-pro/max、response.completed、status completed、完整SSE；输入8539/output86 token。没有图片、搜索、工具或标题辅助调用。

同一canonical media App正常⌘Q退出0，再经原`--reopen`入口重开，42及完成状态保持；调用总数仍6，无补发。实际模型菜单Kimi K3.1 Pro/MiniMax-M3可选、旧K3不存在。再次正常退出0；计量器control/stop为204、退出0。App/Host/Runtime/worker/adapter及18083/18086均无活动服务或数据句柄，两轮四Runtime库均自然WAL0、完整副本只读integrity ok。未手工checkpoint或删除WAL。

71表的全部旧行保持；新增1个用户turn为completed/submitted，选择kimi-k3-1-pro-max-v1/ready。答案42保存于原生item/completed agentMessage，native view为completed/format4；重开前后仅正常停止代际表追加记录，其余70表完全一致，标题仍fallback/not_started。

来源继续为Desktop9f5814fec6cd071d39f0c12f8f48097ce661cb6a、Host8cd6bccbdc1ac3906aea53d95441299f7cfefcce、Contracts ca06d0999c9a08afe80ab3f34a537d492b830ac7、Runtime11fd4504c28afd0f65c6f5f62a6b5328dd437f5a、Connectors cc56cdaa616c9d9eff8efa1f9e1307d084f3dff9、Skills595c927ae101d3d31c234f60565041eee0864680。App SHA42a23cfbc11cc047b005b8d80dafa2aff243fcc469dd1510d04d88196e85f6a9，r5 SHA283d12e16b124942302fcdc8281c729a8a7f676498f06df1d2646292905f579e；119 bundle文件和原receipt核验一致，两次canonical来源检查通过，未重建产品。

使用固定资格App身份及原资格数据，Native仅访问已固定loopback18083；本轮loopback后是明确授权的真实计量代理，非合成服务。因此计为1次真实请求，不把“资格”身份名或localhost地址当作离线证明。日常com.yijie.ai数据未用于本次验证。

## 最小工具修复与失败复审

contract-impact=none：本轮只修改不可发布的本地验收计量/判定工具及其测试；没有改变产品wire、公共DTO、业务存储、Runtime核心或补丁。私有测试账本schema4另存，schema2/3兼容与原字节保留。Desktop工具提交`92cbe3d78fef499f9f1904727b1a5a48be632218`只有4文件，基于9f5814f；App来源仍9f，不把工具提交冒充App重建来源。

复审发现未创建r5文件会继承旧计量器默认20元/8次入口，已使保留r5文件名必须通过显式离线账本创建，拒绝隐式新额度。schema4严格保留5条旧记录，只接受1个新slot、累计30元、精确r5/App绑定、原unknown保留；失败或已用完即停止，重启和重复创建不补额。费用使用原13/68历史估算并明确标识，不能称当前精确账单或已核验费率上界；按Owner新指令无需以查价阻塞功能。原价格审计及当时提案保留为被新指令取代的过程记录。

34项Python计量/结果判定＋10项既有失败分类/正常协作取消控制通过；均为安全纯状态输入，不发模型请求。早期unittest复用类导致重复发现，已改为组合fixture，最终44项为非重复计数。

首次数据观察把旧chat_messages占位assistant行当作答案权威，断言失败；源码显示当前原生事实/视图才是答案来源，原始副本保留，改为读取item/completed agentMessage及native view后一次只读验证通过。没有改数据库或新增真实调用来满足断言。另有工具目录/文件名误用、canonical就绪前UI取句柄超时、bundle ID多路径歧义和保存AX后索引失效，均在新观察/精确路径纠正；只有一次发送动作。全部这些是审计/操作工具问题，不是Kimi或Runtime失败，未隐瞒产品失败或绕过准入。

## 证据判定

| 范围 | 当前结论 | 边界 |
|---|---|---|
| r5最小真实G2V | PASS | 本轮真实文本、保存、同构建重开、正常退出；输出上限8192/无原生搜索，不能替代供应商图片/工具/搜索资格 |
| 正常退出final | PASS | 本轮真实路径＋46正常取消/计划停止＋47媒体＋48十home按同一源码绑定；旧unknown保持，不宣称已取消或清除 |
| core final | NOT RUN完整范围 | 46—48的普通/专家/媒体/辅助/旧历史/计划安全子集有效；供应商图片/工具/搜索结果及unknown/never-sent完整App可达观察仍未覆盖 |
| 剩余业务状态final | NOT RUN完整范围 | 正常完成/重开/活动目录及既有退役/计划审阅已覆盖；unknown/never-sent仍只有领域、Native/前端分层证据，无安全自然App样本 |
| 日常切换 | 未执行 | 资格App和日常入口的构建、identity、数据、workflow及受控维护边界不同 |

修正机器清单曾沿用r4 G2V/S1总PASS的问题：旧38/r4结果和原manifest完整保留；当前G2V改绑本轮r5真实证据，S1总门禁未直接继承。Runtime权威投影改绑已有5b5dad9/source.lock SHA75867f5e…，不产生新公共契约。不会把多个分批测试写成一次fresh全链路运行。完整TCONF04、各slice G3与G4/G5/G6仍不提前晋升。

用户已移除亮暗、键盘/焦点、最小窗口专项，本轮未执行、不是缺项、不是PASS。上述业务状态缺口指恢复/取消的功能行为，不重新引入外观验收。禁止强杀或故障注入才能构造的App未决态保持NOT RUN及影响记录；正常状态机/原生协议验证仍有效。

## 日常切换最小方案与停止边界

已核对真实代码：`run-local-demo-fast.sh --kimi-k31-pro`固定candidate=true/daily=false；日常入口的Runtime/profile及workflow装配仍不同。`isolated_model_migration.rs::admit`只允许两个FEAT164身份，明确拒绝com.yijie.ai；`sidecar.rs::kimi_k31_predecessor_setting`仅对candidate且qualification允许；`kimi-k31-build-candidate.mjs`拒绝workflow=true。因此不能靠改环境变量或把验收App覆盖日常App完成替换。

日常路径已定位为`/Users/jack/Library/Application Support/com.yijie.ai/demo-fast-v1`，本轮仅确认存在及既有保护hash，未打开/解密/复制日常库。schema、旧计划数量、未决操作和权限保持Unknown，不据资格库推断日常状态。

推荐下一步只先实施可审查的日常部署候选，不直接打开日常库。最小文件面为Desktop现有canonical launcher、kimi-k31-build-candidate/packaged-receipt配置、native环境准入/受控maintenance入口、sidecar predecessor准入及对应测试；复用已验证迁移事务、原生回执和Runtime r5，不计划修改Runtime核心/补丁。涉及这些Native/sidecar权限边界的具体diff先交Owner确认，再激活日常维护。

1. 固定包含FEAT164的独立集成来源，并列明原工作区FEAT162/163等已有改动的保持办法。当前日常Desktop主树仍fd0c575且有100项dirty，不能拿干净9f候选覆盖，也不能将这些差异混入FEAT164提交。保留旧App/binary/receipt及校验值，不覆盖已签名或来源不明制品。
2. 明确日常workflow与K31/market/expert/media组合的兼容装配，复用原能力，不能因候选禁止workflow就静默关闭日常工作流。先canonical独立构建和安全离线组合验证；新候选不得复用本轮App PASS而不重验影响面。
3. Owner批准具体日常读写清单后，正常退出日常App，核对无服务/在途/句柄，保存完整加密DB/WAL/SHM、managed配置、Runtime/Host状态与receipt的原始备份。只读预检实际schema、pending/unknown/grant和reader兼容；不满足则停止，禁止清理unknown、退款、换operation重发或强杀。
4. 单独的显式日常维护入口仅准入固定com.yijie.ai/demo-fast-v1，使用原单实例/静止门禁和正式migration；不引入任意path、通用跳过guard或自动维护。旧计划仍暂停并重新审阅/新授权，不复用旧grant。迁移后校验原行/历史、backup、selection与计划授权，再启动同源App。
5. 回退以新兼容reader＋暂停Kimi执行为主，继续读新旧历史；不得用旧K3 writer写新历史、恢复退役执行或覆盖回写整个旧库。异常先正常退出并保留新旧数据和账本，必要时只在新副本诊断。

这份方案说明执行顺序和有限文件面；本轮没有批准日常数据迁移、没有实施上述Native边界扩展。尚未发现需要新Runtime核心修改的依据。

## 账本、保护和交接

新增真实HTTP1，历史5条逐字保留；新独立r5账本共6条、halted=true/stopped_normally，无在途。原schema2/3账本和14.188544元unknown预占完全保持；新账本沿用历史估算累计14.795856元，仅作可追溯估算，不作为精确供应商账单。不得将新账本停止解释为撤销Owner后续功能验证授权，后续必要调用按实际任务最小追加并记录，不再因精确查价反复询问。

原497份dirty与资格活动数据之外71457份保护文件保持；当前6来源干净；全部旧数据/证据/构建保留。完整DB/密钥及日志只在私有`feat164-s4v-audit-20261026`，不提交Git。仅FEAT164工具和治理本地提交，不推送。

下一步以日常部署兼容方案/具体diff评审为主，同时逐项决定剩余功能样例；不要重复已通过真实42、38次离线Runtime组或外观专项。遇到真实功能失败再沿实际链路定位，不以增大验收框架替代修复。索引见`evidence/s4v-audit-index.json`。

## 最终治理检查

claims、strict、G2V门禁、元仓lint/53项测试及7份Shell语法通过。G3/S4实际返回1，记录为明确未通过：S1—S3总状态/来源freshness仍有旧r4引用，S2/S3纵向和S4完整TCONF04/边界/纵向还未独立归并；不能解释成新r5模型调用失败，也不能仅复制新SHA和PASS放行。下轮先将46—49的每项实际覆盖与源码无变化证明按slice登记，未覆盖项保持缺口，再进入日常部署候选；不要重新做已证实的子集来掩盖记录差异。

记录脚本首次在内存替换YAML时把命令中的正则美元符号当作替换模板，解析保护在写入前阻止；改为回调替换后，语义检查通过，并对未变记录恢复原格式。该失败保留为治理工具RCA，无产品变化、数据写入或额外模型调用。
