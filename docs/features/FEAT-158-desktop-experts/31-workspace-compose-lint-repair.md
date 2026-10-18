# 全工作区 lint：Docker Compose 发现路径修复

2026-10-17。接续[第二组专家真实验收](30-thirteen-second-group-taobao-pdd-integration.md)，用户明确要求解决 Compose 缺失造成的全工作区 lint 阻塞，不降低或绕过门禁，保留已接入专家与历史。

`contract-impact = none`：只恢复本机已有 CLI 插件的发现链接。没有改变业务 wire、Runtime、权限、专家内容、数据库、服务部署拓扑或 lint 规则；没有新增依赖、下载或替换可执行文件。用户当前授权覆盖此次环境修复，不涉及发布或基础设施启动。

## 根因与选择

`docker` CLI 29.6.1 可用，但用户目录 `.docker/cli-plugins/docker-compose` 指向已失效的 macOS AppTranslocation 临时路径。因此 `docker compose version` 无法发现子命令，Infra 的真实 `docker compose ... config` 校验失败。

现有 `~/Applications/Docker.app`（4.82.0 / 233772）仍完整包含 Compose 5.3.0：30,780,320 bytes，SHA-256 `2642b6354b323be90cf28460ac186499fbc85381b9ce5e6681fdefb2d0a7d265`，`codesign --verify --strict` 成功，签名为 Docker Inc / TeamIdentifier `9BNSXJN65R`。其版本和摘要与工程既有 [FEAT-126 技术设计](../FEAT-126-public-task-authorization-hardening/05-technical-design.md)及[测试计划](../FEAT-126-public-task-authorization-hardening/06-test-plan.md)已审记录一致。

选择恢复原用户级发现链接，沿用工程既有修复方式；无需再安装其他版本，也无需调整 Docker 配置或为 lint 添加替代执行器。原失效链接保存在 ignored、owner-only 证据目录，随后原子更新该单一 symlink，指向当前已安装 Docker.app 内原插件。Docker.app、Docker CLI、Compose 文件字节和签名不变，其他插件链接和 `.docker/config.json` 字节不变。

## 修复后验证

以下命令全部使用正常默认 Docker 插件发现，不设置临时 `DOCKER_CONFIG`、隐藏 Docker、伪造 plugin 或跳过 Compose：

1. `docker compose version --short` → `5.3.0`。
2. Infra：`docker compose -f docker-compose.local.yml config --no-interpolate --quiet` → exit 0。
3. 元仓：`make lint CONTRACTS_DIR=<现有 yijie-desktop/.local/demo-fast-contracts 的绝对路径>` → **exit 0**。

第三项使用前序已审 canonical 不可变 Contracts checkout，保留原 origin / commit / clean / digest / generator 检查；当前专家及其他候选仍验证真实 sibling。没有修改任何 source pin、resolver、Makefile、`lint-all.sh` 或 `plan.sh`。

统一入口已完成元仓规则校验和 `repos.yaml` 顺序中的全部 11 个子仓：Codex、Desktop、Admin Web、API、Agent Host、Skills、Connectors、Knowledge、Contracts、Infra、Coze。日志明确包含 `Docker Compose semantic validation passed.`，并成功执行最后一个 Coze lint 目标。Coze 现有目标的范围为 integration governance，本次没有把它扩大表述为上游应用 lint 或全测试套件通过。

此次初次修复命令因工作目录不符未找到证据文件，在链接更新前退出；修正为精确路径后才执行实际更新。没有通过重复运行失败门禁或放宽断言制造通过。

## 保留与影响检查

- 修改前记录元仓及全部 11 个子仓的 HEAD、分支、remote、dirty 状态与普通文件摘要。修复及全量 lint 后，所有原有源文件、HEAD、分支均未变；此报告及关联状态说明是其后新增文档。
- 541 份现有专家资源、Runtime 会话历史及验收输入/报告文件逐字节不变；107 份当前 App、Host、Runtime、worker 构建产物仍匹配上轮 canonical 回执。没有重建 App 或升级专家版本。
- 本轮不打开运行中的 SQLCipher/Bolt 数据库、不进行 migration 或任何历史写入。仅比较数据库文件元数据：App 运行期间 SQL WAL 的大小和时间发生变化，因此不把活跃数据库字节相同作为结论；之前已完成的逐行历史保留验收仍见30号报告。本轮没有启动新会话或发送模型/连接器请求。
- 未启动、停止或删除任何 Docker 容器、镜像、网络或 volume；Compose 仅执行 version/config，不依赖启动 Docker daemon。未执行强杀、故障注入、权限破坏、二进制替换或攻击 fixture。

证据根为 Desktop `.local/workspace-compose-repair-20261017/`：`baseline.json`、`environment-before.json`、`docker-compose.original-symlink`、`repair-result.json`、`compose-config.log`、`workspace-lint.log`、`verification-summary.json`。本轮未提交、推送或发布。

## 复查与回退

后续若 Docker 再次改写用户插件链接，先检查链接是否仍指向稳定安装位置，以及对应插件的实际版本、签名和摘要。不要通过删除 Docker 的 PATH、忽略 `config` 失败或修改门禁应对。需要撤销本轮环境变更时，仅恢复证据中保存的原用户级链接；这会恢复此前不可用的发现状态，不涉及应用二进制或数据。没有修改系统目录、其他插件或 Docker 登录配置。

30号报告中“全工作区 lint 被 Compose 缺失阻塞”的历史记录在本轮关闭：**工程现有全工作区 lint 已真实通过**。这不替代此前未运行的浏览器 CSS、真实商家账号或与本任务无关的完整测试套件。
