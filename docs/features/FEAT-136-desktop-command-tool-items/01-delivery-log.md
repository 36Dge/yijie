# FEAT-136 整体实现与调试记录

> 当前状态：D0 PASS；Contracts slice complete；overall Feature in progress。
>
> 本批范围：只完成 D0 + Contracts，完成 Contracts 后立即停止。

## 1. D0 结论与实施方案

- Feature ID：FEAT-136 已复核可用，正式 schema v3、demo_fast + local 四文件包已建立。
- contract-impact：semantic。原因是 v4 event/item union 闭合；采用显式协商 v5，保留 v1 至 v4。
- Command：CAP-016 / GS-003，是本 Feature Must，当前稳定 Runtime facts 足以建立安全契约。
- Tool：CAP-017 / GS-004 只建立 generic stable projection。真实产品 Tool/producer 保持 capability gap；Runtime MCP Tool 没有 declined status。
- Contract First 顺序：固定 Runtime只读 → Contracts v5 source → generated projections → compatibility → immutable local commit → 下一批 Host → Desktop。
- 事件原则：event_id 去重而不是内容去重；item.completed 封口 Item；turn.completed 唯一封口 Turn。
- 安全原则：allowlist、redaction before byte counting、bounded summaries/output、显式 truncation、unknown fail-soft/closed、无 raw wire。

## 2. Git 与治理记录

| 时间 | Repository | 动作 | 结果 |
|---|---|---|---|
| 2026-08-29 | yijie | 从 FEAT-135 dependency-complete HEAD 创建 feat/feat-136-desktop-command-tool-items | PASS |
| 2026-08-29 | yijie | 先独立提交 FEAT-138 取消范围的 6 个 FEAT-131 正式文档 | PASS：67f219b6cf825357285215fcbaafb33c3978acb3 |
| 2026-08-29 | yijie-contracts | 从 FEAT-134 candidate 3832a6c5e99b2a6365f193280fdb887c8fdbc2de 创建同名 FEAT-136 分支 | PASS；创建时 clean |
| 2026-08-29 | yijie-contracts | 提交 v5 source/generated candidate | PASS：3c3000a6fbe2f08ab2131a463a1691e867d661b1；提交后 clean，未 push/tag/publish |
| 2026-08-29 | yijie-agent-host | 只读核验 b9358f06f3a15aa17a2471cf0bb8bfd0e2b29bfe | clean；未创建分支、未修改 |
| 2026-08-29 | yijie-desktop | 只读核验 fc52ef33cdf040d9b6e8d71bd7498811c5c38c51 | clean；未创建分支、未修改 |
| 2026-08-29 | yijie-codex | 只读核验 0ce5902ed400866be0196886bb78f693a004d68d | clean；未 fetch/pull/build/modify |

## 3. Contracts 已交付改动

| Authority / projection | 已交付行为 | 边界 |
|---|---|---|
| AgentSessionEventV5 JSON Schema | named v4 families + closed generic allowlist + Command/Tool strict lifecycle/delta/progress | JSON/SSE authority；v1 至 v4 权威源不变 |
| Protobuf v5 | typed transport projection；JSON-equivalent semantic gate | 新 package/tag numbers，不修改旧 proto；可解码不等于有效 |
| Agent Host OpenAPI v5 route | required event_schema_version=5 | 旧 route 保留 |
| AsyncAPI v5 | channel/message/operation | 旧 channel 保留 |
| Runtime compatibility manifest | 仅增加两个已存在 stable notification | Runtime identity、sandbox、approval 不变 |
| v5 fixtures/tests | 11 个无敏感 synthetic conformance fixtures | 不冒充 Host sanitizer/Desktop/real-runtime |
| generated SDK/bundle | 只通过 repository generator 产生 | 禁止手改 sdks |
| version/release/review docs | 0.7.0 local candidate 与 semantic review | 不创建 tag、不发布 |

## 4. Contracts 验证结果

1. `pnpm install --frozen-lockfile`：PASS。
2. Buf、Agent Host OpenAPI Go/TS、AsyncAPI bundle 与 v5 JSON Schema TS 定向生成：PASS；重复生成的 7 项 generated/protected SHA-256 完全一致。
3. `make lint`：PASS；OpenAPI/AsyncAPI、15 个 JSON Schema、Buf、TypeScript no-emit、Go vet 全部通过。
4. 全部非 archive Node tests：63/63 PASS；`go test ./...` PASS；`pnpm exec tsc -p tsconfig.json` PASS。
5. v1 wire equality 对 published f16a497e1377f45747f8ff9292b4b60cf2027f88：PASS（Public 2 paths、Agent Host 7 paths/reference closure）。
6. breaking check 对 FEAT-134 candidate 3832a6c5e99b2a6365f193280fdb887c8fdbc2de：PASS。
7. breaking check 对 published baseline f16a497e1377f45747f8ff9292b4b60cf2027f88：PASS。
8. `git diff --check`、v1-v4 protected-source review、source/generated digest 与两轮独立 semantic review：PASS；最终无 open P0/P1/P2。
9. Contracts 本地不可变 commit 3c3000a6fbe2f08ab2131a463a1691e867d661b1 已形成，工作树 clean。

仓库 composite generate/test/build 路径会创建或读取预存 Zip Slip archive fixture，违反长期安全条款；初始标准门禁审计中识别该事实前曾各调用一次，其机械 exit-0 结果不作为 FEAT-136 证据，之后不再运行。最终只采用上述安全定向替代并如实登记影响。

## 5. 外部授权与实际调用

| 类型 | 授权 | 上限 | 当前结果 |
|---|---|---:|---|
| yijie / yijie-contracts 本地分支与 commits | 当前用户明确授权 | 本批所需 | Contracts 已提交；yijie 治理提交待本包最终门禁后形成 |
| push/tag/merge/PR/publish/deploy | 未授权 | 0 | 未执行 |
| Provider/模型/Tool 请求 | 未授权 | 0 | 未执行 |
| 破坏性、生产写、权限扩大 | 未授权 | 0 | 未执行 |

## 6. 已知限制与下一批输入

- Contracts 可以定义 generic Tool surface，但当前固定 Runtime 没有 MCP declined status，也没有已批准的真实产品 Tool producer；真实 GS-004 继续 blocked/not run。
- Synthetic fixtures 只能证明 contract shape 和确定性 reducer model，不能证明 Runtime producer、Host redaction 或 Desktop UI。
- 下一批输入必须精确固定 `yijie-contracts@3c3000a6fbe2f08ab2131a463a1691e867d661b1`，并消费 v5 schema/route、caps/redaction/Proto semantic gate、unknown/reconciliation 规则与 fixtures。
- 下一批顺序为 Host mapper/pin/conformance → Desktop adapter/reducer/persistence/UI → focused checks → 在额外授权下执行真实 D4。
- 本批已经到达停止边界；未开始 Host/Desktop 源码、真实 Runtime vertical 或 D4。
