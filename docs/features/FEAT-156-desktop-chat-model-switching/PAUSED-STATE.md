> 已于2026-10-02T17:16:40+08:00收到Owner“继续执行任务”，本暂停已解除；以下为暂停时历史快照。

# FEAT-156 暂停与恢复状态

记录时间：2026-10-02T10:46:34+08:00。Owner最新指令：**暂停执行，记住任务状态**。当前停止实施与验收，只有收到用户明确恢复指令后继续。FEAT-156未完成，D4未通过，10项Must AC仍pending。

## 已完成

- 此前已落地模型入口、Kimi/max与MiniMax/high路由、选择/operation快照、草案与计划模型流；详情见01交付日志和02验证记录。日常模型writer仍默认false。
- Owner本轮明确授权最小Runtime补丁：恢复上游tool_choice=auto，保留tools=[]、input-only、原生非文本响应拒绝、沙箱/权限/扩展限制。该限制只适用于受限草案；普通任务工具能力沿既有规则。
- 新补丁：yijie-codex/.yijie/patches/chat-models/0004-feat-156-upstream-tool-choice.patch。仅作用于临时构建源core/src/client.rs；原codex-rs子树仍与固定上游一致。
- 新canonical入口make chat-models-build；9分36秒构建完成。直接复用现有约24GiB codex-rs/target缓存，没有另复制缓存。新产物独立存放：/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-codex/.yijie/build/chat-models/aarch64-apple-darwin。脚本拒绝覆盖已存在的新候选。
- 新binary SHA256：2d970213298964c8e65887631528b6d6efaa800ccc7c7da4dd7334b62f057d46；manifest SHA256：537b9bdb8ba2da7426815ee1cfce55483239bf412aa41a56c0fa115c8bfe6bf4。新269份stable schema与旧input-only逐文件一致，tree SHA256：34d353815dc8d800cb432a876d5b43350511f63b91ad9766f861e8bc8290cc92。旧固定binary/manifest暂停时重新hash，均未改变。
- make chat-models-test已正常完成exit0：补丁重放/反向恢复、client.rs恢复上游字节、独立schema重生成、无凭据stdio初始化与正常EOF退出、Runtime→Contracts→Host/Desktop候选投影检查均通过。
- 新Contracts独立runtime-chat-models artifact投影已生成/同步；旧runtime-input-only锁和DTO保留。Host已添加新精确artifact pin与input-only资格判断，Desktop launcher/候选来源检查已加入新family。**这些最后的Host改动尚未编译/测试，Host源候选快照尚未重新freeze，Desktop尚未重新构建。**
- 真实集成测试已加强：检查实际对话记号连续性及草案canonical Output，而非仅HTTP200/turn completed；新Runtime下尚未运行。
- 计数器补充tool_choice/tool_count元数据和正常启动/退出状态保存，不记录prompt/响应正文/凭据；未重新启动。
- 本轮早段Host TestChatModel通过；前端模型/composer三文件29项及计划表单1项通过。旧pnpm generate:check通过，使用下列现存干净固定工作树，无新增clone、无放宽旧锁：
  - YIJIE_DESKTOP_CONTRACTS_DIR=$PWD/.local/demo-fast-contracts
  - YIJIE_DESKTOP_AGENT_HOST_DIR=$PWD/.local/host-contract-source-f77c689
  - YIJIE_DESKTOP_SKILLS_DIR=$PWD/.local/skills-pinned-10c45be

## 暂停时运行状态与额度

- 旧候选App已通过Command-Q正常退出；没有启动新App或Host。最后在途资格检查已自然完成。暂停时进程列表未见本任务yijie构建/服务/计数器。未强杀任何进程。
- 真实调用仍5/24，剩余19；图片理解0/2；本机synthetic累计7。最后两次旧Runtime草案HTTP400原因是tool_choice=none；新Runtime尚未真实重测，不声称问题已解决。
- 付费meter状态stopped_normally。本轮新增模型HTTP调用0。必须续用evidence/paid-call-ledger.json，禁止重置额度。标题、工具续推、重试均计入24，每请求最多8192输出tokens；不调用图片生成或外部MCP。
- 密钥仅使用Host被忽略的owner-only文件.local/secrets/kimi-api-key和minimax-api-key，禁止读取到输出或写进代码/文档/参数。
- 所有修改仍在工作树；未commit/push/切分支。Desktop此前用户改动完整保留，初始状态详见evidence/implementation-initial-state.json。

## 恢复后按顺序继续

1. 先复查当前diff与本暂停记录，保持用户长期安全条款；不要重新构建或覆盖已验证的新/旧Runtime，不复制编译缓存。
2. 编译/定向检查最后Host消费改动，使用新Runtime运行TestFEAT156NativeModelProfiles的4次普通本机Responses（非付费模式）；统计新增synthetic次数。正确处理任何实际失败，不伪造PASS。
3. 续开24次上限meter，优先paid+draft-only验证新Runtime的Kimi草案（预期仅1次请求），检查canonical输出/原生input-only回执。剩余额度允许才继续。
4. 审核并重新freeze Desktop contracts/chat-model-host-build.candidate.json（目前因最后Host变更已过期），继续canonical --packaged构建启动，仍用显式local候选/18087/计数器；原18081占用不干预。
5. 完成真实UI模型切换与可见上下文、标题、图片/文件、安全只读工具续推、草案/确认/三目标计划、正常失败恢复/退出重开验收；严格记账。复核1180×760/200%浮层缩放修复和暗色，不能以之前构建代替最终视觉。
6. 完成适用生成/静态/focused检查、文档/证据、最终diff。既有ChatPage同名5项失败有HEAD对照证据，不能篡改断言掩盖。全部Must实际通过后才D4与日常默认启用Kimi；不擅自提交/发布。

## 关键命令与位置

- 新产物：.yijie/build/chat-models/aarch64-apple-darwin/（yijie-codex）
- Native集成指定YIJIE_CODEX_INTEGRATION_BINARY与YIJIE_CODEX_INTEGRATION_MANIFEST指向新产物。非付费模式不要启动meter；付费模式须额外YIJIE_FEAT156_PAID_VERIFY=true，草案单独用YIJIE_FEAT156_DRAFT_ONLY=true，凭据只传FILE路径。
- 资格证据：evidence/runtime-chat-models-qualification.json。构建/检查原始日志：/tmp/feat156-runtime-build.log、/tmp/feat156-runtime-qualification.log。
- canonical App启动：YIJIE_ENV=local YIJIE_LOCAL_PROFILE=demo_fast YIJIE_CHAT_MODELS_ENABLED=true YIJIE_FEAT155_SCHEDULED_CANDIDATE=true YIJIE_RUNTIME_PERMISSIONS_ENABLED=true YIJIE_PERMISSION_VERIFICATION_BASE_URL=http://127.0.0.1:18083/v1 YIJIE_DEMO_FAST_HOST_PORT=18087 ./scripts/run-local-demo-fast.sh --packaged。

用户禁止故障强杀、可执行文件伪装/劫持、权限破坏和攻击fixture；只允许正常开发测试。无需重新询问已授权最小Runtime补丁或剩余调用额度。
