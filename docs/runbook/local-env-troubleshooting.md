# Local Env Troubleshooting

## bootstrap 失败

- 检查 Git 是否安装；
- 检查当前目录是否为 `yijie`；
- 确认脚本有执行权限。

## dev-up 无动作

`platform/yijie-infra/docker-compose.local.yml` 尚未配置时，`dev-up` 只会提示，不会启动服务。

## 子仓缺失

运行：

```bash
./scripts/checkout-all.sh
```

查看哪些路径仍是 placeholder。
