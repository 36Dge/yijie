# FEAT-174 实现自审与使用边界

后续代码复审发现七项问题，现已修复。当前自审、实际维护命令与完整桌面冷恢复结论见[09 最终修复验收](09-review-fixes-verification.md)；本页其余内容保留初次实施时的检查记录。

2026-11-14 最终复核。结论：修订2已形成可运行的本地候选，导入、普通旧格式迁移、原生内容回滚和兼容回滚/恢复均有定向证据。没有另建技能执行器或插件版本更新器。仍保留[验收记录](02-verification.md)中明确的未执行范围。

## 原生复用边界

| 权威 | 实际负责内容 | 本次不重复实现的能力 |
|---|---|---|
| yijie-codex | 本地市场登记；PluginStore安装/卸载/原子替换；配置层与CAS写入；Skill解析、发现、按需读取；原生刷新及失效通知；MCP状态 | Host不解析Skill YAML，不推断缓存目录，不比较semver，不写原生缓存，不做关键词匹配或正文拼装 |
| yijie-contracts | 从实际canonical schemas生成原生投影；skills/market-v2 HTTP/DTO/validator来源 | 消费者不手写重复wire DTO；renderer使用离线生成validator，无运行时编译/eval |
| yijie-skills | 38项完整源、一项一个原生wrapper、确定性内容/来源身份 | 不预安装，不改专家资产，不按点击下载 |
| Host | 用户身份、来源快照、操作意图、目录代际、只读库存投影、迁移/回滚日志 | 不把journal当实时安装事实；全部副作用经原生接口 |
| Native/Desktop | 受控文件选择与摘要绑定、命令/权限边界、进度恢复、展示与精确引用 | renderer不传任意路径、不解包、不改Runtime配置 |

具体入口：Runtime [`0025`](../../../../yijie-codex/.yijie/patches/chat-models/0025-native-skill-marketplace.patch)、Host [`skillmarket`](../../../../yijie-agent-host/internal/skillmarket/)、原生适配 [`skill_marketplace.go`](../../../../yijie-agent-host/internal/codex/skill_marketplace.go)、旧格式适配 [`native_migration.go`](../../../../yijie-agent-host/internal/skills/native_migration.go)、Native [`market_v2.rs`](../../../../yijie-desktop/src-tauri/src/skills/market_v2.rs)。

## 自审发现并修正

1. **真实路径契约**：原生plugin/read/install/refresh的marketplacePath是清单文件路径，marketplace/add接受根。实际协议探测发现后已按canonical语义修正。
2. **正常冷启动**：旧Host配置所有权检查只允许projects/skills，安装后原生写入的plugins/marketplaces会被拒绝。现仅在精确新候选下接纳两个固定本地市场，保留原生配置字节；旧profile仍拒绝扩展表面。冷恢复测试通过。
3. **资源忙碌事实**：PendingInit空根会话曾被误当作活动资源。已接入原生ThreadWatchManager，结合运行中agent、等待初始化的子任务和后台终端；空会话可管理，活动任务仍保护。真实活动turn门闩测试通过。
4. **首次写入与旧数据**：先获取既有Host sessions.db进程锁，再保存迁移前原字节、运行旧合法恢复、准备兼容backend并最后提交v3标记。普通未确认请求不凭指纹重发，以旧错误codec收敛并保留ID/指纹、原始快照及页面提示；专家未决请求不批量改写。
5. **运行目录与发布**：整个服务串行写目录，目录前后摘要有journal；unknown摘要停止写入。prepared个人源不进可选列表，UI成功只在原生确认后提交。下架/孤项继续管理；源缺失独立提示。
6. **取消与代际**：取消意图可与worker并发持久化；补偿仅限本次拥有的首次安装，已有安装通过原生刷新和精确规则编辑恢复。晚到的孤项取消按新查询确认已完成结果，避免永久阻塞。
7. **接口与展示**：原生union投影使用RawMessage别名；新增完整资源槽位纳入既有开发资源校验及bundle配方摘要；移除Starter安装触发。新模式仅发送结构化技能引用，不给自然语言追加匹配前缀。
8. **依赖与历史**：只有可精确对应原生MCP身份的依赖才用原生库存判定；产品工具标签保持unknown。MCP声明不会自动安装。旧接受请求先重放，历史正文和引用不批量改写，冷会话显式选择已验证。
9. **离线浏览与写入归属**：Host/Runtime暂不可用时，从摘要固定的随包来源只生成浏览投影，安装状态为unknown，不能添加或选择；权限错误及迁移未决不走此回退。v3路由记录缺失或读取失败时，普通技能也不重新交给legacy writer；只有显式legacy归属可以写。Native/前端投影及路由纯决策用例已覆盖，未制造服务或文件故障。

## 迁移和回滚操作

常规开发仍使用 `pnpm client:dev`。当前候选默认打开新模块；首次切换会保存旧输入、完成合法恢复、发布降级保护，再迁移普通技能。用户数据、专家记录、旧成功回执和历史来源保留。未能确认规则作用域或并发状态时停止该对象；不要用删除旧目录或修改版本号解除保护。

本次没有切换日常数据。真实窗口采用同一规范入口的显式独立数据选择：

```text
python3 -B scripts/development-client.py start-ui --skill-acceptance feat174-20261113 --tool-search-meter
```

这是独立Native/Host/Runtime验收目录，模型地址绑定既有本机回环，窗口操作没有创建聊天或派发模型请求。入口不清空目录，正常重开复用同一验收身份；退出走菜单和既有专用服务清理。

内容回滚：选择保留的上一完整源→目录代际发布→原生N3 ForceReinstall→N2与原生技能快照→精确规则重绑定→完成回执。回滚不调用首次install制造短暂开启。

兼容模式维护入口为已配对、已构建Host的：

```text
desktop-host --skill-market-maintenance=rollback
desktop-host --skill-market-maintenance=resume
```

必须使用同一可信启动配置，并先正常退出拥有者；现有session数据库锁阻止在线维护。该入口不运行聊天/模型/连接器业务任务。回滚只回到含v3 reader的兼容实现；原普通来源重新接入，个人来源与缓存保留并受控停用。兼容模式的普通技能管理保持只读，可继续使用可确认的旧来源；resume验证本次配置版本后恢复原生路由和本次拥有的个人启停编辑。后续用户意图/配置冲突时停止，不能覆盖。旧二进制及“把schema_version改回2”均不支持。

## 工作区和安全复核

基线保存在元仓 `.local/diagnostics/2026-11-13-feat174/baseline`。Desktop原有26个文件在扣除ChatPage结构化引用所需的一行后，摘要逐项一致；其余既有改动没有重置。六仓HEAD未变化，原有Runtime产物保留，新候选内容寻址生成；canonical codex-rs源文件无diff。最终机器核验见 [workspace-protection.json](references/implementation/workspace-protection.json)。

验收技能已通过应用正常卸载；正常重开与重扫仍为38个安装按钮、零开关。App与专用服务按正常退出流程结束，为验收启动的Docker Desktop也已从菜单正常退出；未清除容器、卷或旧技能来源。

构建使用项目现有工具链/脚本；没有强杀、程序替身、权限故障、攻击fixture、付费供应商调用、清库、提交、推送或发布。真实供应商自主选择、业务技能效果、生产分发和日常数据切换不因本次本地验收被宣称通过。
