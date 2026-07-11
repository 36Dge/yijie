# Local Env Troubleshooting

## bootstrap 失败

- 检查 Git 是否安装；
- 检查当前目录是否为 `yijie`；
- 确认脚本有执行权限。

## dev-up 无动作

`dev-up` 固定读取兄弟目录中的 `../yijie-infra/docker-compose.local.yml`。文件或 Docker 缺失时命令会失败并返回非零状态。

## 子仓缺失

运行：

```bash
./scripts/checkout-all.sh
```

查看哪些路径仍是 placeholder。
