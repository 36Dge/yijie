# FEAT-144 原生当前线程状态与启动恢复

> 本文保留该阶段的来源、结果、预算与未完成事项；当前原生拒绝和普通重开已完成，最终来源/分账/D4见[24最终报告](24-final-native-decline-and-delivery-2026-09-11.md)。以下“当前/下一步/未执行”仅指本文记录时点，不作为继续调用指令。

本次继续正常拒绝验收时发现第二个启动问题，已完成源契约及最小修复并本地提交，canonical复验进行中。它与20记录的原生trust/受管配置冲突不同；21/22的既有修复、成功调用及正常退出证据保留原来源范围。未提前关闭D4。

## 根因与原记录保护

标准应用启动后Host/Runtime健康检查均ready，但Desktop绑定失败，显示任务记录不可用。只读检查定位到旧B任务的本地Turn `01a08b84-6737-71e3-8459-b5f3f06c7096`：status=queued、runtime_turn_id=null、submission_status=queued；相应text v1 start_turn outbox为failed。原启动条件将任何本地queued候选当作活跃执行，因此阻断全局入口。

failed outbox不能证明Runtime没有执行。旧v1对传输不确定也采用failed且不再自动派发；Host operation receipt同样不能反证旧执行结果。不能改写该Turn、补造失败或完成、删除历史，也不能重发POST查询状态。现有安全历史接口只传前1024个Turn且无当前Thread.status，不足以从历史反推空闲。

## 最小原生复用修复

通过独立GET `/v2/agent-sessions/{agent_session_id}/native-thread-status`，复用Codex稳定 `thread/read(includeTurns=false)`。Host沿已有会话绑定核对原生ID，仅投影原生status.type的notLoaded/idle/systemError/active；保留owner bearer、no-store及安全错误。旧history DTO、端点、SSE及数据库格式不变，未知或缺失不默认idle。

Desktop只有同时满足以下条件才允许保留旧历史并打开新任务：本地Turn为queued且无原生Turn绑定；scope、公共任务、session与operation精确一致；对应start_turn outbox为failed；同任务无pending/inflight出站；原生状态精确idle或notLoaded。原生读取await后再次核对同一数据库只读条件。notLoaded仅表示当前Runtime未加载，不能称旧请求未执行或已完成。

所有原生Turn绑定、可派发出站、active/systemError、身份不符、未知或读取失败仍阻断。该路径不resume、不发现MCP、不更新verified scope、不持久化当前状态，也不更改旧Turn/outbox/receipt。既有dispatcher不取failed，恢复流不取queued；旧冷线程不自动续跑，权限及后续原生接入门禁保持。

## 来源、兼容与检查

源契约新增独立只读端点为additive；产品readiness条件修正消费新的原生事实，未改变FEAT-152审批或权限含义。按provider-first固定：

- Contracts `811f38d6b104fa18477107e7ac91a85e19c445d1`。
- Host `0e47766f494977c94bfea0e89cfbdf45a7fafa2b`。
- Desktop `7abf89e84ffcbe56360d8c9943390e0640d9e239`。

共用generator摘要确有变化，因此native-mcp、native-conversation和runtime-permissions的真实来源锁均更新；旧v1/v2历史、权限wire字节不变。保留旧Go client接口并提供新增操作的opt-in接口；Rust/TS由源生成，不手改DTO。新增操作不写history，无migration或新回滚reader；旧Host不支持该读操作时明确拒绝，不回退历史猜测。最低SQLCipher reader仍是25b004fbd5a4dcf642a503d302c21a7d6e3b817f。删除清单为空。

Contract安全生成及57份产物检查、5项Node/2项Go定向测试、lint、三固定基线breaking通过。Host新状态读取及既有FEAT144/FEAT132安全定向回归通过，make lint通过。Desktop七项Rust定向测试、clippy、fmt及文档构建通过；测试首次重开失败源于合成测试重新创建了随机scope，修正为同一scope后通过，未修改产品安全校验。分离阶段审查确认无权限放宽/补发/历史改写，并补入await后的条件复核。见[提交前证据](evidence/native-status-repair-precommit-2026-09-11.json)。

当前以原app-data与日常Home重新标准构建，完成后通过隐藏输入继续原生拒绝。累计文本7/13、元数据12/20、业务2逻辑调用保守扣4/10、图片0；本次修复没有新增外部调用，已预留的新线程初始化/目录2次仍未执行。AC-004仍用户排除；原生缺字段、冷历史不完整、旧附件/清理/隔离映射等限制保持。未修改Runtime、FEAT-137或FEAT-152，未推送/tag/部署。
