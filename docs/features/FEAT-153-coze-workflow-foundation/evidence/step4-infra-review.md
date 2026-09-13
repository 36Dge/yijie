# FEAT-153 第 4 步 Infra 独立静态审阅

日期：2026-09-12。本附件记录 Infra 前置审计、正常控制路径修正和静态验证；真实 HTTP、CAS、PostgreSQL、停止重开证据由本轮主执行记录承载，不以静态结果代替运行事实。

## 最终检查

| 命令（工作目录 `yijie-infra`） | 结果 |
|---|---|
| `make workflow-check` | PASS；独立模型校验与 10 项测试，0 failed/0 skipped；[原始输出](step4-infra-checks.txt) |
| `python3 -c 'import ast; from pathlib import Path; ast.parse(Path("scripts/workflow-local.py").read_text())'` | PASS；仅解析源码，没有执行控制脚本 |
| `node --check scripts/workflow-local-cas.mjs` | PASS |
| `node scripts/workflow-local-cas.mjs --check-source` | PASS；canonical API/Coze consumer 与源验证，无凭据读取或 HTTP 请求 |
| `git diff --check` | PASS |

新增静态模块为 `yijie-infra/scripts/workflow-local-model.mjs` 与 `tests/workflow-local.test.mjs`。它们读取真实候选文件，显式解析 YAML merge；没有创建坏配置、攻击资源、可执行文件替身或权限故障 fixture。控制脚本的文本断言限定于本次已审阅写法，配合人工式代码复核，不宣称证明任意 Python 程序的完整语义。

## 已关闭问题

1. **tmpfs 被 YAML 拆分**：初稿 flow array 中未加引号的逗号把一个挂载拆成四项，静态测试实际发现失败。最终 API/Coze 都是一个有引号的、有限大小、noexec/nosuid 的临时挂载；见 `yijie-infra/compose/workflow-local.yml:95`、`:134`。
2. **仅 internal 网络不能满足当前宿主入口**：主执行实际发现 internal-only API 没有可用的宿主 18888 映射。最终仅 API 加入本项目 `workflow-edge` bridge，默认 host binding 仍为 127.0.0.1；其余五个服务只连 internal 网络，唯一发布端口仍为 `127.0.0.1:18888:18888`。模型精确限制两网络和每服务成员；见 Compose `:129`、`:161`，model `:68`。这不授予任意 provider 调用；API 上游仍固定 Coze 服务地址。
3. **普通端口冲突导致 epoch 混代**：重开端口探测提前到旧容器删除和凭据轮换之前。新 epoch 与 `credentials_pending` 先原子落账，随后生成两个独立凭据并校验它们与 state 同代；机密文件和状态写入采用新建 0600 临时文件、fsync、原子 replace，不用截断旧 state。见 controller `:41`、`:184`、`:195`、`:205`、`:311`。
4. **旧 ready 不代表当前 ready**：当前 ready 要求六个常驻主实例均 Running/healthy、非 OOM、实际镜像等于本轮固定镜像，排除一次性 migration；再从宿主固定 127.0.0.1:18888 以 K_NA 和当前 epoch 查询源定义的 status。不可达或状态不匹配显示 not_ready，不根据旧 phase 报通过；见 controller `:214`、`:352`。
5. **中断与自有 ID 记录**：启动 CLI 使用独立 session；记录 PID、label、epoch；普通 KeyboardInterrupt 只报告 PENDING，继续观察 CLI 正常结束，再记录新建的自有容器 ID。迁移也显式 `--pull never`，up 保留 `--no-recreate`；对象归属同时核对 project/service/feature/dataset/epoch、记录 ID 和实际 image ID。见 controller `:92`、`:116`、`:141`。
6. **重开抹掉异常容器**：删除已停止自有容器前拒绝 nonzero exit/OOM；停止完成也必须核验实际退出状态。正常操作保留四个数据卷，未运行 `down --volumes`、prune 或 force removal。见 controller `:311`、`:413`。
7. **Docker 工具便携性**：仅在用户 `~/Applications/Docker.app` 和系统 `/Applications/Docker.app` 两处选原厂 CLI/Compose，不引入任意 PATH 工具，不改变用户 Docker 登录配置；请求仍固定当前用户的本地 Docker socket。当前平台范围仍为 macOS arm64；见 controller `:28`。
8. **build 后无法清理已停止旧容器**：新构建更新 `state.built` 后，已记录 container ID 仍严格对照原记录 image ID 和 service；未知新 ID 必须显式允许纳入且匹配当前 pin/build。所有 project/feature/dataset/epoch 检查保留。ready 单独要求当前镜像，不能把旧 running 容器当作新构建已就绪。见 controller `:136`、`:141`、`:214`；新增静态测试覆盖该区分，测试总数为 10。

## 停止、机密与独立验证容器

停止首先自然观察正在运行的 PG 测试容器，20 秒未完成仅报告 STOP_PENDING；随后按 API → Coze → 四项依赖分阶段停止。停止只使用已核对 ID 的 `SIGTERM --timeout -1`，不会因有限 grace 升级强杀。有限观察使用 `Popen.wait(timeout=20)`，没有 `subprocess.run(timeout=...)`、kill 或 terminate 回退。Docker 官方说明默认/有限 stop timeout 到期会发送 SIGKILL，`-1` 则持续等待正常退出。[Docker stop 官方文档](https://docs.docker.com/reference/cli/docker/container/stop/)

运行输入只用精确 FILE 配置和逐文件只读挂载。API/Coze 使用宿主 UID/GID 以读取 owner-only 文件，K_NA 不挂到 Coze。Redis 的 root reader + 仅 DAC_OVERRIDE 是明确评阅的例外，同时 drop ALL、no-new-privileges，仅可写自有 `/data` volume；没有继承上游 privileged 配置。其他服务不添加 capability，没有 Docker socket、host namespace、外部 host mount 或共享旧项目数据库。

PG runner 是辅助服务 `workflow-pg-test`，不进入六个常驻服务列表；单独绑定 api-test 的实际 image ID。它只连已核验的 internal network、同 UID/GID、恰好三个只读私文件、只读 root、drop ALL、no-new-privileges、2 GiB/2 CPU/pids 上限。仅 `/tmp` 允许执行本次标准 Go 测试构建产物，有 1 GiB 上限；不发布端口、不下载依赖、不自动删除测试容器。PASS 需要退出码 0、非 OOM、真实已停止状态。审阅了普通 PG 测试源码：实际 scope/resource、8 并发 Claim、明确标识的 unknown storage receipt、追加审计与正常连接重开；没有删除审计、清表或伪造引擎成功。

CAS 脚本使用源生成验证器和两份 canonical consumer 检查，两次合法保存使用同一 expected revision、不同 operation UUID、独立 TCP；核对一个成功、一个 revision_conflict、实际草稿及操作回执，最后正常关闭编辑会话。此附件只执行其 `--check-source`，没有发起写请求。

## 验证边界

- 最初 PATH 中的 Docker 客户端可用但 Compose 不可发现；原厂 bundle 的 CLI/Compose 只读检查分别为 29.6.1/v5.3.0。未安装、替换或伪装可执行文件。后续 daemon/栈操作由主执行控制。
- 镜像静态检查验证已评阅 vendor/version/digest、实际 image ID 和 Linux/arm64 记录。Docker `image inspect tag@digest` 与 Compose 对组合引用的解析差异由主执行实际核对；保持 runtime 固定 source reference 与 `--pull never`，没有因此放松 pin 或重新下载。
- 未运行历史 Infra 全量攻击/故障套件、权限破坏、信号注入、默认强杀或数据删除。不用模拟失败声明运行恢复已经通过。
- 未执行 Desktop、iframe/MessageChannel/WKWebView、签名或 production 验证。没有改 Desktop 既有用户 dirty 文件。第 5 步真实载体资格与第 6 步 D4 不由本附件判定。
