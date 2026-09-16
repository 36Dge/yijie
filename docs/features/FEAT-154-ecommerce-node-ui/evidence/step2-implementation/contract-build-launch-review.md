# 第 2 步：本地构建与启动入口只读核对

核对时间：2026-09-15T13:08:26.840763+00:00

## 观察结果

- 没有发现 yijie-desktop / yijie-agent-host 进程；18081、1420、18888 均无监听。
- `.local/demo-fast/workflow-dev/processes.json` 记录 `phase=stopped`、CLI exit 0、signal null。
- `make workflow-status` 本次退出 2：`Docker read failed; check original local Docker Desktop`。
- Infra 留存 state.json 仍为 `phase=ready`，无 pending_stop；因此不能确认真实容器已正常停止。
- 原厂 Docker 位于 `/Users/jack/Applications/Docker.app`；此核对没有启动 Docker、App 或服务。
- 既有编辑器登记 385 个文件，manifest SHA-256 `b732e7eb505cea4ff5704af8fec99608e2954784818a74f816a21006f3584d6c`，引用旧 1.3 source lock。第 2 步源/锁已改变，必须正常停止后重新构建和登记。

## Root 后续执行顺序

所有源修改及测试完成、源码冻结后，执行以下正常路径。若 App 实际重新出现，先通过自身退出菜单/Cmd-Q 正常退出并保护已有未保存内容；不能用 kill/强杀、Ctrl-C 转发代替。正常打开原厂 Docker，等待其 ready，再核对实际容器；所有启停由 root 统一操作。

```sh
# 正常打开原厂 Docker；然后在 Infra
make workflow-status
make workflow-stop
make workflow-status
# 需要确认 phase=stopped、所有自有容器非 Running/非 OOM/exit 0。
# STOP_PENDING 时保留等待，不能继续覆盖产物或强杀。

# yijie-coze；标准脚本只更新本项目 ignored 开发输出
node scripts/yijie/workflow-editor.mjs prepare
node scripts/yijie/workflow-editor.mjs install
node scripts/yijie/workflow-editor.mjs build
node scripts/yijie/workflow-editor.mjs check

# yijie-infra；现有数据集不需要重新 init
make workflow-check
make workflow-editor
make workflow-build
make workflow-up
make workflow-status

# yijie-desktop；普通 packaged 入口（同时构建 Desktop/Host 并正常启动 App）
YIJIE_WORKFLOW_ENABLED=true \
YIJIE_WORKFLOW_CREDENTIAL_FILE=/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-infra/environments/local/generated/feat-153/private/k-na.json \
pnpm tauri:demo-fast:app

# 若另需真实 dev 资格，同样 env 下用 pnpm tauri:demo-fast；先正常退出 packaged。
```

`workflow-stop` 使用 `docker stop --signal SIGTERM --timeout -1` 并有限观察；超时返回 STOP_PENDING，保留依赖和状态。`workflow-up` 正常移除已停止且有来源记录的自有容器、保留 volume，轮换本地 epoch/凭据，再执行既有幂等 migration/ready。不要直接 Docker Compose down 或修改 controller state。

## 输出与敏感边界

- Coze live bind 来源：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-coze/bin/workflow-editor/dist`，包含 `manifest.json`。API 容器只读挂载 `/opt/yijie/workflow-editor`，对外 `/editor/`。
- Coze 构建工作区：`bin/workflow-editor/build-workspace`；安装 receipt：`bin/workflow-editor/install-receipt.json`。build 内部再次 prepare，校验固定依赖 receipt，运行真实 strict typecheck 和 Rsbuild，不能绕过新诊断。
- Desktop Vite：`yijie-desktop/dist`；packaged App：`yijie-desktop/src-tauri/target/debug/bundle/macos/易界 AI.app`；其启动文件为 `Contents/MacOS/yijie-desktop`。
- Launcher 使用固定既有 Runtime digest，标准 `go build` 输出 `yijie-agent-host/.local/bin/yijie-agent-host`；不改被保留的 Runtime。
- Launcher 在构建阶段移除 workflow 凭据文件路径，只在最终 native 启动时传递路径，不打印/传递 credential 值。Sorftime opt-in 默认 false，不应额外开启。
- 正常 dev launcher 自有 Vite，退出 App 后等 CLI 正常完成及 `server.close()`；不向 child 转发 SIGINT/SIGTERM。端口占用时 launcher 会停止，不能强杀占用者。
- Infra build/up 每次再次核对完整源码/manifest/三个 consumer 锁。构建后若继续改 Coze/API 源码或锁，需重新构建登记，不能伪造旧 digest。

## 核对来源

Infra AGENTS.md、docs/workflow-local.md、scripts/workflow-local.py；Coze README.yijie.md、scripts/yijie/workflow-editor.mjs、workflow-editor-typecheck.mjs；Desktop AGENTS.md、package.json、scripts/run-local-demo-fast.sh、scripts/run-workflow-dev.mjs、src-tauri/tauri.workflow-local.conf.json。

本记录是源码与现状核对，不代表构建、启动或产品资格完成。
