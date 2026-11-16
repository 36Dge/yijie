# FEAT-175 时序契约矩阵

所有场景均为计划，产品验证 NOT RUN。模型／工具真实事件由 Runtime 产生，费用操作记录由 API 产生，不相互冒充。

| 场景 | 有序阶段 | 不变量 |
| --- | --- | --- |
| FLOW-NATIVE | 用户提交→原生工具声明→供应商搜索→native Item→回答→终态 | 未因专家或内置 MCP 可用而关闭 hosted；不填入伪造 sources |
| FLOW-BUILTIN | 用户提交→原生发现／提议→原生权限→tools/call→服务端准入→一次 REST→归一化→MCP Item／回灌→回答→终态 | 工具执行时钟在 call 开始；无市场 prepare 时钟、安装状态或二次审批 |
| FLOW-PROMPT | 提议→原生确认等待→允许→tools/call→HTTP→结果 | 确认等待不侵占 HTTP 预算；等待中未发送供应商请求 |
| FLOW-CANCEL | 提议／执行→本机停止→Host撤销→执行端确认／有界收尾 | 执行端已观察取消早于发送线性化点时零请求；断开不等于远端未执行；未知不免费、不重发、不进入新轮 |
| FLOW-REOPEN | 已保存 Item→正常退出→重开→原生历史／MCP 展示 | 查看不产生工具执行和费用；原 URL／来源关系保持 |
| FLOW-UPGRADE | idle→旧配置解绑→原生 resume 新配置→新 turn | 不在活动 turn 改工具表；旧日志不改写，旧待发操作不静默迁移 |
| FLOW-IDENTITY | Native正常产品会话→仅检索委派→当前调用→退出／换租户撤销 | 主 refresh token 不给worker；公网按可信主体／租户检查；thread/turn不是公网身份 |
| FLOW-DISPATCH | 同 operation查重→额度准入→原子派发标记→一次内部请求→结果／unknown | 派发标记在发出前持久化；已有派发不在重启后自动再次执行；无正文时明确不可恢复 |

| 不变量 | 验证计划 |
| --- | --- |
| TINV-001：原生审批和结果 ID 不由 Host 制造 | 固定 Runtime 的 started/completed／elicitation request-response 对照 |
| TINV-002：模型延迟与审批等待不消耗供应商执行预算 | 正常慢响应与正常确认等待跨过旧阈值，测量实际 tools/call／HTTP 时间 |
| TINV-003：同业务 operation ID 不重复发送 | 普通重复投递同一请求，服务端返回已记录状态，不执行第二次 REST |
| TINV-004：历史读取无执行 | 正常重开与多次展开旧结果，上游调用计数保持零 |
| TINV-005：取消与迟到结果归属不跨轮 | 正常停止后开始新任务，旧结果只结束原操作 |
| TINV-006：服务端身份是收费资格源 | 两个正常测试账户独立使用，额度及审计不串线；不做攻击注入 |

持久化仅记录必要的新业务调用事实和已有会话历史；没有独立工具队列／审批状态机。通知、重放、终态及 cleanup 继续沿原生和现有 owner 生命周期，清理使用正常 EOF／应用退出。
