# FEAT-164 二次审计修正

2026-10-24。三个并行只读复核方向：Host/Contracts、Runtime、Desktop/治理。无产品测试、构建、服务或真实推理请求。不是独立人工批准。源码摘要见 [sources](evidence/reviewed-sources.json)。

| ID | 初版不足 | 代码依据及修正 |
|---|---|---|
| REV-01 | 未明确重要数据治理 | ADR-0017:57、HANDBOOK:122：production_hardened/local；不改应用runtime profile |
| REV-02 | 普通未发送可直接正常取消 | Desktop schedules/recovery.rs:245仅scheduled；database.rs:5443是删除chat；普通/市场取消是待实现能力 |
| REV-03 | 无worker接管时序 | Desktop models.rs:385返回1=1；database.rs:2765会领取增attempt；application.rs:643启动循环；connectors/dispatch.rs:84另扫队列；claim/send双门禁须先装 |
| REV-04 | unknown可直接正常恢复 | Host session/chat_models.go:184/206/280：unknown阻新operation，同ID重入会重新SwitchThread并跳过部分前置门禁；需显式恢复设计 |
| REV-05 | status可证明线程模型 | Runtime protocol/v2/thread_data.rs:170无model/effort；config.rs:350无thread_id；Host native_thread_status.go:14只读status；thread/resume才回完整模型配置 |
| REV-06 | 直接resume旧会话 | Host session/service.go:425要求请求profile等于存储；必须先用新operationID+旧revision选择新目标，提交后再turn |
| REV-07 | 压缩总用当前模型 | Runtime core/src/session/turn.rs:803/867/922有previous_model分支；当前无comp_hash且窗口相等通常不触发，但必须验证；OpenAI专属fallback不能当Kimi保障 |
| REV-08 | 只检查父thread与spawn参数 | Runtime agent/control/spawn.rs:150已加载子代理直接复用；role.rs:65可覆盖；multi_agents_common.rs:245只改model不自动改provider；禁用路径不启用 |
| REV-09 | 辅助请求漏Guardian | Host runtime_permissions.go:47 auto启用审核；Runtime guardian/review.rs:695可用专属/override/当前model；计入effective配置审计及HTTP预算 |
| REV-10 | schema迁移只泛称重建 | Desktop SQL0028必须保留原PK/FK/CASCADE/nullable、刻意无outbox FK；migrations.rs:347事务校验；29→38还经过30—37 |
| REV-11 | 旧计划可能只改profile列 | schedules/store.rs:708领域更新会revision+1/paused/撤授权/处理future slots；保留历史grant/run，不单列UPDATE |
| REV-12 | reader回退及配置升级过于笼统 | Host codex/chat_models.go:145两个文件顺序原子更新并非整体事务；baseline.go:157精确验manifest；总模型开关关闭还禁历史/MiniMax，需独立新Kimi准入开关 |
| REV-13 | 标题与缺失记录未细分 | Host session/title.go:58不持modelOperationMu；Desktop title payload只有session ID；Host scheduled_recovery.go:10明确missing不证明未发。标题正常收敛、unknown不能绕过 |
| REV-14 | 新文档恢复重验可能被自身unknown永久阻断 | Host session/chat_models.go:206普通路径要求ready；专用恢复仅处理精确同operation造成的非ready，其他未决工作仍拒绝，已committed只读返回 |
| REV-15 | candidate二选一漏专家组合 | Desktop scripts/chat-model-build-candidate.mjs:18有experts=true/artifact_media=false分支；来源核对覆盖artifact-media/experts/chat-model三种 |

以上Desktop路径前缀为yijie-desktop/src-tauri/src/chat/（SQL为migrations/chat/）；Host为yijie-agent-host/internal/；Runtime为yijie-codex/codex-rs/。根目录为 /Users/jack/Downloads/Personal_Info/CrossBSD。行号依据本轮工作树，后续需重查。

## 保留的正确结论

新profile、精确官方model、原生Responses、0006旧slug条件、0004/0005保留、历史只读兼容、独立候选和锁、FEAT-159实际artifact-media Host组合、MiniMax/kimi-web身份不变。

## 官方核对与Unknown

[Responses](https://platform.kimi.com/docs/api/responses)及[Codex集成](https://platform.kimi.com/docs/guide/codex-kimi)支持目标model/原endpoint/1M；[参数页](https://platform.kimi.com/docs/api/models-overview)主要描述Chat Completions，不能直接套其参数。二次复核[quickstart](https://platform.kimi.com/docs/guide/kimi-k3-1-pro-quickstart)仍有搜索更新和生产限制，而Codex页描述原生web_search可用；不由此删除现有能力或宣称实测通过。

账户资格、reasoning.encrypted_content等额外参数接受情况、真实SSE和质量、effective roles/overrides/子代理状态、新build hash均Unknown/NOT RUN。memories默认关闭且market关闭；review/start未发现由Host暴露，登记关闭/未暴露路径，不扩大范围。

结论：可形成可审阅需求包，不能宣称实施就绪；初版11项旧K3基线检查属于上一轮，本轮未重跑，不能计入FEAT-164产品验收。
