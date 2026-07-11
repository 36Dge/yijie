# 本地开发

## 基础依赖

- Git、Go、Node.js、pnpm、Rust、Cargo、Make；
- Tauri macOS prerequisites；
- Docker Desktop 或兼容的 Docker Compose 环境。

Node 与 pnpm 版本约束记录在各前端和工具仓库的 `package.json`，Go 版本记录在 `go.mod`，Rust 版本记录在 `yijie-desktop/rust-toolchain.toml`。

## 初始化

```bash
git clone https://github.com/36Dge/yijie.git
cd yijie
./scripts/bootstrap.sh
```

脚本根据 `repos.yaml` 把其余仓库克隆到 `yijie` 的兄弟目录。重复执行是安全的：已有仓库只校验 remote、fetch，并保留当前分支和本地改动。

## 本地依赖

```bash
./scripts/dev-up.sh
```

该命令启动 `../yijie-infra/docker-compose.local.yml` 中的 PostgreSQL、Redis 和 pgvector。

## 启动顺序

```bash
cd ../yijie-api && make dev
cd ../yijie-agent-host && make dev
cd ../yijie-connectors && make dev
cd ../yijie-knowledge && make dev
cd ../yijie-desktop && pnpm tauri:dev
cd ../yijie-admin-web && pnpm dev
```
