# 通用 Provider 实施进行中

2026-10-08。Owner已确认15推荐方案并要求遇到问题深入解决；没有待定审批。仅Tushare真实验收，其余50项代码审计与本地测试。旧诊断不足不阻塞。追加预算仍剩2轮模型/1次只读查询，本阶段尚未消耗。

## 已写入源码（尚未构建/激活新产品worker）

- Contracts Broker 0.3.0：通用profile、完整参数 `argumentsJson`、固定schema摘要及有界策略；Provider 0.2.0保留Tushare工具策略并增加通用准入/安全凭据配置语义。更新生成器和派生消费者，不手改生成文件。
- Connectors `generic.rs`：复用RmcpClient，编译完整JSON Schema并冻结；不下载远程/file引用；同名工具按service+tool摘要隔离；通用风险为write、逐次审批，明确destructive工具无专用策略仍拒绝，保留一次HTTP许可，不自动重发。
- Broker由单Tushare backend改为精确选集中多backend；调用绑定实际service/ref，不再用selection[0]猜归属。Tushare既有参数和结果归一化保留。
- `provider-registry.v1.json`/`provider_registry.rs`覆盖51项固定目录。44 HTTP OAuth走共用授权与metadata逻辑，`oauth_policy.rs`只接受所选服务的HTTPS发现链。Actor仍绑定owner/tenant/epoch/revision/cref，生命周期不变。
- 四种HTTP自备凭据通过worker拥有的一次性本机表单直接进入Codex KeyringStore，UI/Native/Host不收密钥。FTShare固定FTSHARE_API_KEY；其他三项需要用户按官方资料明确Header，代码不猜Bearer。此代码支持header凭据，不宣称未知供应商的非header协议也已支持。
- Native管理和可用性判断按认证策略接线到48项HTTP；浏览器入口分别核对HTTPS OAuth与已知配置服务的精确loopback nonce路径。APIKey配置不冒充OAuth。
- `secret_guard.rs`在连接进程内记住所属transport实际凭据，阻止进入工具定义、参数审批及结果；字段过滤另行拒绝凭据参数。只保留内存，不记录值。
- UI审批显示通用工具完整参数；Host候选识别generic-mcp-v1，canonical worker脚本准备新profile（**尚未运行worker-build**）。

## 新增依赖与来源

JSON Schema校验不是Codex公开client已有的能力，因此复用MIT许可`jsonschema = 0.58.6`，关闭默认HTTP/file resolver，提供只拒绝外部引用的retriever；不自写Schema校验器。额外依赖按版本/source/checksum固定在worker/schema-validation.lock.json，来源检查验证精确额外集合；原Codex源码及实际Runtime二进制不改。使用固定Codex keyring-store路径依赖保存API凭据。

## 当前验证快照

在secret_guard最后几处接线之前：worker44项通过（含3个通用schema/结果测试、1个OAuth发现策略、51项静态对应、1个Header策略）；Native连接器36项通过；Broker+Host源JS15项通过。最近继续修改尚需重新验证，不能把上述中间结果称最终通过。日志在/tmp/feat157-generic-*.log、/tmp/feat157-native-generic-*.log、/tmp/feat157-contracts-generic-tests.log。

## 必须继续完成

1. 通用两服务批准/拒绝/正常EOF的实际进程内协议测试，确保第二个服务ref正确、未批准不调用、消费一次；完整参数UI测试、凭据表单正常单次提交/过期/cancel本地测试。
2. 重新检查secret_guard、APIHeader仅固定资源、metadata分页、所有源码/锁生成一致性；修复Clippy和fmt，更新Makefile构建源码清单。
3. Google两本地服务与淘宝独立适配尚未完成。Google Calendar不能直接运行会写明文tokens.json的包；应查支持的存储接口或用记录固定来源/补丁的canonical项目构建作正常适配，不能伪装程序或绕过凭据边界。Maps需固定包/Keyring注入/EOF owner。淘宝不能复用qwenwork身份。
4. 各服务编译接线不等于已证明供应商专用认证；代码审计未完成处继续记录，不能偷偷恢复51项真实验收门槛。
5. 完成全部本地检查后正常⌘Q旧应用，再canonical worker build、Host freeze、tauri:demo-fast:app重建；新实现变更后必要Tushare代表验证才使用剩余额度。

旧标准应用仍运行上次历史修复构建，worker为d31203bf。本文件不是D4/完成报告。
