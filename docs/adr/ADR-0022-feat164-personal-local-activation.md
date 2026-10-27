# ADR-0022: FEAT-164 个人本机日常启用范围

## 状态

Accepted。Owner于2026-10-27T16:23:36.126125+08:00明确回复“批准该限定例外，继续完成 D5”。本批准限定下列范围；G5/G6仍须依据实际检查与观察分别判定。

## 背景与冲突

FEAT-164因为重要持久数据迁移而采用production_hardened治理；现有D1—D4运行环境为原个人Mac上的local/demo_fast、固定Native owner/tenant。ADR-0017/Handbook将治理Profile与exposure区分，validator却禁止local G5/G6；更关键的是ADR-0018第8条明确禁止production_hardened使用免登录profile。仅删除validator的public限制不能解决这条Accepted ADR的冲突。

本条记录Owner明确批准的限定例外。不改变原ADR对公开、云端、多租户或其他生产环境的要求；不把已执行D4倒写为G5/G6。

## 已批准决定

1. 仅批准FEAT-164当前本机单一Owner的日常入口继续使用已有固定Native owner/tenant免登录模式。identity仍com.yijie.ai，原Home/SQLCipher/凭据边界、loopback bearer、Native scope/context/资源权限、用户意图、审批及计划grant均保持；不新增权限或服务暴露。
2. 治理仍production_hardened + local，完整G0—G6、Contract First、S1—S4、三类最终证据、失败账本、备份/回退、Owner启用与观察检查不裁剪。G5/G6结论只代表该限定本机范围，不是公网、组织/多人、多租户、云端、签名/商店发布资格。
3. 日常启用记录绑定精确新制品回执、原数据Home、D4与激活预检摘要，允许用户正常使用Kimi K3.1 Pro；本次Agent验收0模型调用，旧账本/两预占保持。旧K3、unknown及旧计划grant不因启用恢复或重发。
4. workflow维持既有ready-only前置，不隐式启动/恢复/迁移；原Docker/服务状态若变化仍走原受控恢复边界。退出/回退使用正常流程及兼容reader暂停Kimi，不覆盖旧App、不删WAL或回写旧库。
5. 修正validator的local/public混淆时，local G5/G6必须带显式Owner批准和Accepted ADR、范围与证据引用；完整生产链检查仍先执行。不得只改gate状态或exposure绕过。

## 备选及边界

保持原ADR原文且不增加例外，则可完成新入口的离线准备，但不能正式启用D5；需另建正常OIDC、服务端tenant/RBAC的部署方案。那会扩大现有任务的账号与基础设施范围，不自动实施。

## 授权与验证

Owner答复为“批准该限定例外，继续完成 D5”，实际确认时间见状态节。此前当前用户请求已授权D5工程准备和阻塞修复，本条确认专门针对新发现的Accepted ADR免登录例外。测试使用普通结构化配置与正常退出，不涉及攻击/故障注入；Runtime核心/补丁不变。
