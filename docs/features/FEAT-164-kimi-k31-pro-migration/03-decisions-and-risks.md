# FEAT-164 候选决策、风险及阻断

> 实施授权更新：Owner现已确认FEAT-164方案并要求开始实施和审计验证。此前“仅文档”段落是上一轮历史边界；当前状态以feature.yaml及13-implementation-log.md为准。G0/G1/G2记录本次方案确认；G2A/G2V及产品完成门禁仍未通过。无新增Git/付费/日常库激活许可。

下列方案已由Owner当前实施指令确认；实际源diff的Consumer审查与后续Gate另行记录。需求/技术/Reviewer/发布Owner均为段成威。

| 决策 | 推荐与取舍 |
|---|---|
| DEC-01 身份 | 新profile；拒绝旧profile偷偷指新模型和硬删所有历史旧值 |
| DEC-02 治理 | production_hardened/local；重要持久数据触发，运行环境profile保持 |
| DEC-03 协议 | 原Responses/max/1M及最小Runtime修订；不改API、不选highspeed、不夹带预算提升 |
| DEC-04 激活 | reader+停派发准入先就绪，再迁移和激活；不能仅靠最后Host拒绝 |
| DEC-05 unknown | 保留未知；明确恢复原目标resume，重新验证所有门禁；不新造只读线程设置协议 |
| DEC-06 取消 | 补普通/市场never-sent取消的最小领域能力；不能借删除chat |
| DEC-07 回退 | 可读两代且能独立停新Kimi的兼容构建/前向修复；不静默复活旧K3 |
| DEC-08 截止点 | 正常收敛所有受管模型工作后定义cutover；不以父thread idle代替全部工作结束 |

沿既有权威边界，不新建身份/权限/调度主状态；若后续选择新Runtime协议或跨仓职责变动，回G2及适用ADR评审。

## 事实与未知

Fact：旧身份在目录/SQL/HTTP/runtime/worker中存在硬约束；worker会自动领取；thread/read无model/effort；源候选已实施，产品切换未执行。
Assumption：原Key、max/1M可以沿用为配置默认，不代表账户/质量/所有参数已通过。
Unknown：账户资格、完整真实部署配置前身、effective roles/overrides/已加载子代理图、未知操作数、预算及下游候选digest；本轮不读取Key或私密会话解决。
Conflict：初版压缩/普通取消/unknown恢复/兼容激活描述过于乐观，11和05已给出修正。官方搜索能力与生产建议分开保留。

## 阻断台账

| ID | 尚缺事项 | 解除要求 |
|---|---|---|
| BL-01（已解除） | Owner已确认方案并要求实施 | G0/G1/G2记录用户当前指令；不推定Git/发布和付费许可 |
| BL-02 | 三层身份契约及方向兼容仍是候选 | G2审阅；G2A真实源diff、版本/full commit/digest、全部consumer评审 |
| BL-03 | unknown恢复、never-sent取消、准入/激活资格未实现 | 先审设计，再安全状态测试、G2V及slice证据；不称现成机制 |
| BL-04 | 三表/Host状态迁移及兼容回退无运行证据 | 先合成库/正常重开证明，再获准操作日常库；不得先迁后补 |
| BL-05（部分解除） | 新Runtime和独立Contracts投影已构建校验；Host/Desktop候选未产生 | 仍需源候选不可变commit与G2A，再进入最小纵向候选 |
| BL-06 | 真实模型/工具/图片/Guardian/标题无本次额度 | 单独批准用户回合、HTTP、工具次数、tokens/费用上限及停止条件 |
| BL-07 | 加固全门禁未完成且当前local | G5/G6保持pending；不改exposure或借旧D4制造关闭 |

三次同点失败启用append-only RCA，不机械第四次重试。禁止强杀、权限破坏、攻击fixture、可执行伪装/危险归档；若门禁只能靠禁止行为证明则NOT RUN并记录影响，不减弱断言伪造PASS。保留既有工作树改动与日常App；当前仅实施未激活源候选。
