# FEAT-155 · 3C-3B1与3C-3B2本轮执行定义

用户明确授权本次连续完成B1与B2。承接23及后续B2五步答复，完成后停止，不进入页面、真实激活或Provider验收。本轮整体contract-impact=breaking，影响Contracts、Host、Desktop和元仓；Runtime固定只读。

先冻结共享草案执行协议和Desktop私有命令，然后依序实现Host候选Store6/不可变用途、固定schema/受限配置adapter，再实现Desktop候选SQL22、原outbox草案用途、原生完成事实读取与同源唯一确认。普通Host Store5、Desktop SQL15保持；新格式兼容reader先于显式候选writer；旧迁移不改，不访问日常库/Keychain。

B2最小决策：用同库来源账本登记scoped conversation/local turn/operation、固定schema/policy版本。来源唯一键由native产生，renderer不能换request ID绕过。同一来源的最终item摘要和确认定义摘要、plan及原request收据在同一事务提交；不复制聊天正文。提取只接受精确原生绑定、完整未截断final_answer及completed终态，整体视图partial不误拒。删除源聊天使未确认来源失效，已确认来源只保留幂等墓碑；重复确认返回当前plan，不复活删除计划。目标标签不解析成真实ID，确认定义仍由native验证；仅保存paused，grant/启用/run保持分开。

新增私有命令只负责开始/继续受限草案、读取候选及确认保存，复用3C-3A context/native授权、提交期限、typed IPC和原Coordinator/outbox。普通聊天发起时建立独立受限用途会话并只交接用户明确文本，不静默把原会话改用途。原普通发送、权限切换及调度existing target不得把草案会话当普通执行目标。

实际权限资格须如实保留：固定Runtime的thread/start与resume响应activePermissionProfile为experimental字段（protocol/v2/thread.rs:193,426）。本批不能启用experimentalApi或用普通readOnly回执假装证明精细权限；真实固定产物/Provider资格仍NOT RUN。受限配置、用途/路由、组合事务使用普通临时库和进程内声明式协议检查；实际Manager在缺少有效资格时拒绝模型出站，普通入口不激活候选。不得增加布尔开关冒充资格。

输入/输出共享源归Contracts；IPC封套归Desktop；Host Store6和Desktop SQL22为各仓私有格式。执行映射、operation幂等、原生观察与正文清理继续沿原链，不新增第二执行器/数据库/历史状态机。配置、请求及错误均不透传任意schema/path/config/native身份；临时合成目录仅为正常测试资源。

当前模型累计0/12，图片与商家0；本批目标零真实调用。不强杀、不破坏权限、不注入攻击fixture、不替换二进制，不提交推送发布。最终报告分别列源码实现、合成验证、真实资格与未执行项；D4和Must继续pending/NOT RUN。
