# 本地开发

## 基础依赖

- Git
- Go
- Node.js
- pnpm
- Rust
- Tauri prerequisites
- Docker
- Docker Compose
- PostgreSQL client
- Redis client
- Make

## 初始化

```bash
./scripts/bootstrap.sh
./scripts/checkout-all.sh
```

## 本地依赖

```bash
./scripts/dev-up.sh
```

当前 `dev-up` 会查找 `platform/yijie-infra/docker-compose.local.yml`。该文件需要在 `yijie-infra` 初始化后补充。

## 启动顺序

```bash
cd services/yijie-api && make dev
cd services/yijie-agent-host && make dev
cd services/yijie-connectors && make dev
cd services/yijie-knowledge && make dev
cd apps/yijie-desktop && pnpm tauri dev
cd apps/yijie-admin-web && pnpm dev
```
