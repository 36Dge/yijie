# FEAT-153 第 5 步 API 静态宿主与浏览器 AOT 准备

本附件记录已实现与安全本地检查。尚未由本代理启动/停止镜像、加载实际 Coze editor bundle、调用真实服务或执行 dev/packaged WebView 资格。

## 契约和浏览器校验

现有桥源已经包含 connect、ready、request、response、dirty_changed、request_close；本次保持 shape。父页从 EditorOpenedView 取得 E 期限，在父页面计时、移焦点和禁派发；显式同资源重连采用新 bridge/generation/port，不 reload iframe。child 保留 dirty canvas 和原 base revision，不能将新 bootstrap revision 静默替换成其写入基线。

Contracts canonical generator 新增自包含 AOT JS 与类型声明，导出 `validators[name](unknown)` 和 `validateBridge(unknown)`。使用已锁定 Ajv 8.20.0 standalone，编译只发生在生成期；产物不含 runtime require、Buffer、eval、new Function。UTF-8 限额由 TextEncoder codegen 实现，maxLength 保留锁定 Unicode 码点 helper，未退化成 UTF-16 长度。

Bridge TS 继续直接从桥源生成。不同消费者的 type import 由 canonical `typescript-imports-v1` 投影处理；锁同时记录原文件 SHA、映射和结果 SHA，没有手改生成物。工作流 TypeScript generator 设置 `defaultNonNullable=false`，因此源可选的 RunQueryInput/ListRequest.limit 保持 `limit?: number`，无需 consumer 自造 Omit DTO。

生成同步路径：

- Desktop：`src/api/generated/workflow-local-validator.gen.js` / `.d.ts`，`src/domain/workflow-editor-bridge.generated.ts`；引用现有 `workflow-local.generated.ts`。
- Coze：`frontend/apps/workflow-local/src/generated/` 下的 `workflow-local.gen.ts`、`workflow-editor-bridge.gen.ts`、`workflow-local.validators.js` / `.d.ts`，以及 contracts 目录的两个源 schema。
- API/Coze：另同步 canonical `contracts/workflow-local.source-lock.json` 原字节，供生产者和宿主绑定 bundle 的同源锁摘要。

## 先定义再实现的静态产物协议

权威源是 API `config/workflow-editor-assets.schema.json`，说明为 `docs/workflow-editor-assets.md`，已先发 Coze producer 和主任务。

bundle 必须有 root manifest.json，声明 schema_version=1、base_path=/editor/、source_repository=yijie-coze、真实 base commit、candidate digest、canonical source.lock.json SHA 和逐文件 path/hash/bytes/content_type。必须包含唯一 index.html；其余只允许 assets/ 内 JS、CSS、图像、字体。manifest≤256 KiB，≤512 文件、单文件≤16 MiB、合计≤64 MiB。manifest/schema/私有配置/source map 不作为公开资产提供。

API 新私有配置：`YIJIE_WORKFLOW_EDITOR_ENABLED=true`、固定 `YIJIE_WORKFLOW_EDITOR_BUNDLE_DIR=/opt/yijie/workflow-editor` 和 Infra 独立固定的 `YIJIE_WORKFLOW_EDITOR_MANIFEST_SHA256`。默认关闭，不读静态产物。启用时在数据库初始化前检查 manifest hash、编译内嵌 source lock、元数据、MIME、路径、大小、逐文件 hash 与文件读取稳定性，使用 Go os.Root 限定根目录，预读成有界不可变 map。请求阶段不再选择或打开文件路径。

`editorassets.Gateway` 仅把 /editor/ 精确资源交给静态 handler，其他请求仍交原 API handler；没有修改原 /v1 鉴权、epoch 或 Origin gate。静态资源 GET/HEAD 无凭据，未知资源、目录和 manifest 不返回 fallback 或列表。

固定 CSP：default none，script self，style self+必要 inline，img/font self/data，connect/worker/frame/object none，base/form none；frame-ancestors 仅 `http://localhost:1420` 与 `tauri://localhost`。所有静态响应 no-store、nosniff、no-referrer；不设置与跨 origin iframe 冲突的 X-Frame-Options。实际 packaged origin 与 CSP 的 WK 行为不从代码推断通过。

## 实际检查

| 项目 | 实际结果 |
|---|---|
| canonical generate:workflow / check-generated:workflow | PASS；确定性稳定，41 个组件 validator 与 bridge。 |
| API/Coze/Desktop canonical sync + --check | 全部 PASS，包含 type import 投影摘要。 |
| `pnpm test:workflow` | 11 项 PASS：原 7 项 + 4 项 AOT Unicode/UTF8/可选参数/握手/禁运行时字符串代码生成及 TypeScript 正常编译。 |
| AOT 在 Node `--disallow-code-generation-from-strings` 下正常验证 | PASS；没有替换运行时或注入攻击 fixture。实际浏览器 CSP 仍待资格。 |
| API `make workflow-lint workflow-test workflow-build workflow-qualify-build` | exit 0；21 个顶层 focused tests 和现有路由子例 PASS，含 race。新增 3 项正常静态加载/路由/API gate/HEAD/未列资产/默认关闭测试，1 项正常配置测试。 |
| API 两份 deployment JSON 解析、API/Contracts git diff --check | PASS。 |
| 旧 api-server/app/global migration/public lock/public DTO/go.mod/go.sum | 7 项与 API HEAD 字节相同。 |

使用原已验证 Go 1.26.5 缓存，`GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off`；未下载新依赖、未启动数据库。宿主 server/migrate/qualifier 仅标准构建，实际镜像重建与启用由主任务协调。

## 本次锁摘要

| 锁 | SHA-256 |
|---|---|
| Contracts source | `f800e51eb4bd10f574a8ac34222293de0d080c72806ffbb072626e724ebf23fd` |
| API consumer | `45025097b4af2a665e94d90915ca3410bbad317e7869b8ff31bfd03dd688178d` |
| Coze consumer | `63959748561bbca5b6390fcef4ccb6084b3b660943fde5bd166d7b751f19c6f3` |
| Desktop consumer | `ee1d038eeedee98af520a3750db93165218399546f550b97f84c42a314dedff8` |

这些是 local_candidate 工作树的 source/generated digest，不是新 commit、发布 tag 或生产通过。

## 未执行与后续真实资格

本代理没有修改 Infra 或启动/停止镜像，没有执行真实 editor load/create/save、E 到期重连、dirty 保留、dev/packaged handshake、CSP 或完整产品页资格。实际 Coze bundle 的 hash、大小、产物来源及浏览器行为由主任务后续记录。

权限破坏、symlink/危险路径攻击 fixtures、恶意资源、强杀与故障注入均未执行。正常静态单元 fixture 只用于检查宿主，不是“真实 Coze 编辑器可用”的替代证据。
