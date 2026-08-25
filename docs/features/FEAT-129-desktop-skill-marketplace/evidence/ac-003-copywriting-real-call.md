# FEAT-129 AC-003 — `copywriting@0.1.0` 真实调用证据

> 执行时间：`2026-08-25T15:20:38Z` 至 `2026-08-25T15:21:00Z`  
> 环境：Desktop `local + demo_fast` 启动的真实 Agent Host 与固定 Runtime  
> 数据：完全合成商品规格；未读取真实账号、商家或消费者数据

## 授权与调用计数

- 用户于 `2026-08-25T14:40:52Z` 授权最多 1 次付费模型调用，仅用于 FEAT-129 AC-003 的 `copywriting@0.1.0` 真实验证。
- 实际执行 1 个 Host 模型 turn，客户端请求显式使用 `--retry 0`；未提交第二个 turn，治理额度为 `1/1`，剩余 `0`。
- 本次证据不包含 owner bearer 或 MiniMax API key；生产写入、平台发布及其他付费操作均未执行。

## 安装与 Runtime 前置状态

- Catalog revision：`cc2b9be4d0e640e0888e97f6f7a09149a248386931786a7a089c8094304d94a5`。
- Skill：`yijie.content-marketing.copywriting@0.1.0`，Runtime name `copywriting`。
- 安装操作：`476c9e57-291a-444b-9201-c0a4102dc9a3`，结果 `complete`。
- 调用前 Host 投影：`installation_status=installed`、`enabled=true`、`runtime_visible=true`、`failure_code=""`。
- 已安装 `SKILL.md` SHA-256：`785a47c30626608911e8b3e6221efb533116518b4463bf16f4419ca43ed9c328`。

## 真实模型调用

- Agent session：`9797f6d2-a1d1-416c-87de-0fe10d189a27`。
- Runtime thread：`01a03980-c194-7c62-b7e1-1283e36e70e4`。
- Turn：`01a03982-579a-7be0-a2b1-ef46472c4e7e`。
- Trace / request：`feat129-ac003-paid-call-v1` / `feat129-ac003-turn-v1`。
- Runtime rollout `session_meta.model_provider=minimax`，`turn_context.model=MiniMax-M3`、`effort=none`。
- 输入以显式 `$copywriting` 选择 Skill，并提供完整的合成受众、页面目标、商品事实、证据边界、禁用主张、CTA、语言和语气。

## Skill 使用证明

- Rollout 中存在且仅存在 1 个 `<skill><name>copywriting</name>…</skill>` 注入块。
- 从注入块去除 Runtime XML 包装后，正文 SHA-256 为 `785a47c30626608911e8b3e6221efb533116518b4463bf16f4419ca43ed9c328`，与上述受管安装目录中的 `SKILL.md` 完全一致。
- 同一 rollout 仅有 1 个 assistant message 和 1 个 `task_complete`；SSE 以 `turn.completed`、`status=completed` 终止。
- 模型输出按 Skill 规定提供“文案简报、推荐文案、备选方案、证据与假设、发布前检查”五段，并明确声明内容是草稿、未发布到 Shopify 或其他平台。

## 脱敏运行结果

- 首 token：`2619 ms`；完成耗时：`22237 ms`。
- Token usage：input `9444`、cached input `128`、output `2050`、reasoning output `0`、total `11494`。
- 调用后 Skill 仍为 `installed + enabled + runtime_visible`，Host session 回到 `idle`。

结论：AC-003 所要求的“至少一个不依赖外部连接器的代表 Skill 被真实模型调用”已由安装态、Runtime 注入内容摘要、真实 provider/model、终态事件和结构化输出共同证明。
