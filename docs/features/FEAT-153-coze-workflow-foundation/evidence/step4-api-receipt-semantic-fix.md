# 第 4 步真实核对发现的 API 回执版本偏差

日期：2026-09-12。范围：工作流 local candidate 的回执语义修复，`contract-impact=semantic`；没有新增字段、required、状态码或路径。

## 发现与判定

主任务对真实 MySQL 与 API 回执作只读核对时发现：W1 的第二次 save，operation `ae175e12-6f53-4e76-aa2a-8e042c4b7a29`，Coze 持久回执为新 revision `7684523784379826176` 且无 version；API 回执却另有 `version=v0.0.1`，来自保存当时资源的 `published_version`。

这不是 JSON Schema 的对象形状错误：原 `OperationReceipt.version` 是可选字段。但是没有已批准的“回执 version 代表资源最近发布版本”投影语义。`Workflow.published_version` 与本次写入结果是两个不同事实；新的 save revision 并不是旧 v1。API 原正常成功路径无条件复制该资源字段，而未知结果的正常 operation 查询路径直接采用 Coze 持久回执，因此同一操作的回执内容还会取决于响应路径。不能通过放松比较把这个差异解释为通过。

依据：API `internal/modules/workflows/application/service.go` 的原第 133–136 行与 `reconcile` 的原第 183–204 行；Coze `backend/domain/workflow/localadapter/mutations.go:47` 的 save 仅登记 workflow/revision；源文档 `docs/workflow-local-v1.md` 定义 receipt 为派发/副作用登记，另行查询原 operation，不以资源 metadata 替代结果。

## 修复和来源顺序

主任务最初授权仅修 API 映射，API 两文件草稿与一轮 focused 检查先完成，未重建/启用镜像。随后主任务明确要求先补权威源说明；本次最终接受点按源更新、规范生成、下游同步和源检查完成后，再执行 API 最终 lint/test/build。没有把中间草稿当成已激活版本。

1. 在 Contracts `openapi/workflow-local/workflow-local.yaml` 的 `OperationReceipt.version` 添加说明：只表示 publish 新提交的版本或 release run 选择的版本；create/save/debug test 省略，不拷贝 `Workflow.published_version`。同步 `docs/workflow-local-v1.md`。保持原对象结构和可选性。
2. canonical `pnpm generate:workflow`、`pnpm check-generated:workflow`，随后 `sync-workflow-consumer.mjs` 同步 API、Coze、Desktop，再逐项 `--check`。没有手改 SDK/schema/锁。
3. API 仅对 publish 从 Workflow 设置 receipt version；run 继续使用 Run.Version。save HTTP 的 Workflow 响应仍可显示资源已有的 published_version，save operation receipt 不附该字段。
4. 增加一个正常应用层测试，比较“直接保存后的回执”与“独立 recorded 意图正常查询 Coze 回执”两条路径；没有制造网络失败。测试同时确认发布的版本保留，并扩展已有运行回执断言保留指定版本。

Coze 和 Desktop 业务运行代码没有新增行为修改，仅消费规范生成结果。旧 public/Runtime 锁和历史数据库未修改。

## 新锁

Contracts base 仍是 `811f38d6b104fa18477107e7ac91a85e19c445d1`，`mode=local_candidate`、`release=false`，没有 commit/tag/push。

| 文件 | SHA-256 |
|---|---|
| Contracts OpenAPI 源 | `90e13e8a386036ca09e19502204d629417c7b82fbd664d1d063d5cb846316a1c` |
| Contracts source.lock.json | `51ac0d57c102c93016d26c8ec600ca242fe71b8bcbeaa27bdba646df3b221f01` |
| API workflow-local.lock.json | `6ad24a2b1f6b758c2719aed0c8c70a7791e1f278f25d9baef459a0f386bf566b` |
| Coze workflow-local.lock.json | `9e2e54e37931a3eba6da0e46a90913253500e8a147dd40b20dfa3a3e46b95e77` |
| Desktop workflow-local.lock.json | `9aa83fbec1c5f585b677d854da6e4f6d513e0d19a3826479d15f4e69fc468fd6` |

## 实际检查

- 规范生成与确定性检查各 1 次：PASS；41 个组件 validator 与 editor bridge。
- 三个 consumer 同步后检查各 1 次：PASS。
- `pnpm test:workflow`：7 项源测试 PASS，1 次。
- `pnpm exec redocly lint openapi/workflow-local/workflow-local.yaml`：无 error，原 9 项 IPC-only unused-component warning 保留，1 次。
- `scripts/check-breaking.sh` 对 `811f38d6b104fa18477107e7ac91a85e19c445d1`、`f16a497e1377f45747f8ff9292b4b60cf2027f88`、`29317b6426578749dc698fc2ad32b986ee5c8e9f` 各执行 1 次：全部 PASS。结构检查不替代本次语义缺陷判断。
- 源同步后的最终 API 命令：`make workflow-lint workflow-test workflow-build workflow-qualify-build`，`WORKFLOW_GO=/Users/jack/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.26.5.darwin-arm64/bin/go`，环境 `GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off`。exit 0；17 个顶层 focused tests（另有既有路由子例）通过 race 检查，server/migrate/qualifier 宿主标准构建通过。前述未启用 API 草稿另有 1 轮 focused lint/test PASS，不冒充真实运行次数。

## 历史和待重跑边界

W1、原失败 artifact、MySQL 原始 receipt、API 既有 receipt 和审计全部保留，不静默修订。API 对已有 completed receipt 直接读回，本次修复不使旧错误记录自行消失；不能用旧 W1 作为修复后跨端一致性的通过证据。

主任务将正常停止、重新构建记录新 image/source digest、正常启动，并使用新 W3 重跑完整链路与真实回执核对。该实际运行结果必须由主任务另记。本修复代理没有执行 Docker、migration、真实业务或危险测试；未制造攻击、权限故障或强杀。
