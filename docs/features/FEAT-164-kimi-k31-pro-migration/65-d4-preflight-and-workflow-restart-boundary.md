# FEAT-164 D4预检及workflow恢复边界

2026-10-27。Owner已批准64号之后的D4首次受限启动、历史检查、正常退出和后态审计，Kimi保持暂停，0新增真实模型调用，不进入D5。**当前停止在启动前：Docker Desktop后台未运行，固定Docker socket不存在，无法验证workflow实时ready。App尚未启动，D4启动次数0，未生成D4部署绑定。**

## 已完成的复审与预检

64号D3确实只执行一次：日常Native SQL37→41，67旧业务表全部行保持，3新表为空，原Host/Runtime未启动。当前六个干净来源仍为63固定来源，App仍4f7adcad/receipt0e6fe819；1216源码输入、119包内文件及canonical prepare-only --reopen通过。本轮未构建或修改产品、Runtime核心/补丁。

同一正常App锁下检查原17,397文件/530,142,694字节及D3后态sealed；D2旧完整sealed也保留。新inspection的Native SQL41/71表、完整性/FK通过，未决outbox/selection/reservation/turn、未结清grant及全模型未来/待恢复工作均0；6个已消费grant不改。Host10/8会话idle/ready，无active turn/cleanup；四Runtime库完整性正常，8条Native→Host→Runtime及rollout映射相符。

检查仅打开inspection，未对原库或sealed连接数据库API。原数据/凭据、旧账本/两份预占和用户工作区保留。桌面UI可操作；本轮阻塞与锁屏无关，不做已排除的外观专项。

## 实际失败及根因边界

现有受审`feat164-d2-workflow-ready.py`在`all_containers`阶段返回`WorkflowError`；不是服务鉴权或App启动失败。只读诊断确认：

- 当前context为desktop-linux，未设置DOCKER_HOST；Infra本来使用固定原Docker程序和固定socket，不依赖这个context进行重定向。
- Docker Desktop及backend进程未运行，仅原特权网络helper存在；`~/.docker/run/docker.sock`不存在，docker version无法取得Server。
- 已保存workflow state仍写ready，但此时不能观察容器、健康、epoch和带凭据GET。当前容器状态为UNKNOWN，不推定为健康、正常停止或退出255。
- 源码固定SHA `7fd0450319467d5ad97eb56f2bb713ac411ea19c8708ab2529ffcf6d350194ea`未变，读检查没有改state或凭据。第63号READY仅是其原时点事实。

因此停止D4是正确门禁结果；没有改workflow=false、跳过ready、替换socket/程序、写假状态或反复重试。不能据此认定Native/Host/Runtime存在新缺陷。未执行日常App、模型调用、workflow-up或服务恢复。

## 待确认的最小依赖恢复方案

现有D4批准继续有效，但不自行扩大到workflow生命周期。第59号D4明确要求：“需要启动workflow时，必须另列既有服务/容器与数据库迁移、完整数据保护范围，再授权”。现将必要范围具体化：

1. 正常打开既有原厂`/Users/jack/Applications/Docker.app`，不安装、升级或更改Docker配置。先只读核验原记录的8个容器、6个primary、4个volume、镜像/网络/挂载/epoch和当前停止/运行状态。固定Compose配置为`restart: no`，不能假定打开Docker就恢复业务栈。
2. 若既有栈已经真实ready，保留状态直接回到D4前检。若全部已登记容器停止且身份、镜像、来源一致，使用现有`workflow-local.py recovery-plan`生成新恢复ID，沿`recover --recovery-id <该ID>`先对四个停止态volume完整copy-out/hash，再启动原依赖、执行API/Coze既有只读一致性检查、正常启动原应用并正常停止。原失败状态、数据、回执/业务事实全部保留；不复用63号的旧恢复ID或旧数据副本冒充新备份。
3. 在恢复完成、当前来源/镜像仍匹配后，才执行既有canonical `workflow-local.py up`。此动作明确包含移除已停止的旧容器并按相同服务重建、原volume复用、正常epoch/凭据轮换和既有幂等API/Coze迁移；不新增服务或schema、不删除volume、不拉取镜像、不构建新镜像、不强杀。若有未知/缺失容器、活动未决业务、部分异常运行、来源或镜像漂移，停止并另报，不自动修复或重试。
4. 以现有真实只读ready链再次验证6个primary健康、身份/epoch和鉴权status/editor，同时核对业务事实及允许的正常principal审计增量；之后重新核验日常D3后态、备份、锁、全模型零派发，形成新的D4绑定。
5. 继续本次已批准D4：同一canonical App、原Home、`YIJIE_KIMI_K31_EXECUTION_PAUSED=true`；只查看目录/旧历史/附件/关闭计划，不切换或恢复旧模型、不发送消息、不保存/启用计划、不运行workflow。正常退出、完整后态副本审计后停止，不进入D5。

该方案不改产品/Runtime/Infra源码，沿用已批准的semantic部署接口与既有恢复实现；依赖恢复须另外获得本轮明确许可。它不允许任意数据修复、备份覆盖、schema降级或对非本项目数据集操作。

本轮失败原始日志、副本事实和环境诊断留在`feat164-d4-first-start-audit-20261027`。后续实际批准、动作和结果须追加记录；当前不把计划、历史READY或D4批准标成已经执行/通过。


## 收尾审计与当前交接

复核原日常与D3完整sealed、D2旧sealed均一致，同一App锁可取得且无项目进程/数据句柄。六来源及当前制品保持，原8仓HEAD/分支/远端、500份dirty、混合memory原内容、7账本/两份预占保持。原模型HTTP累计仍13，本轮0；没有原库API open、App启动或workflow生命周期动作。

治理audit-claims、结构检查、S4 G3、lint、修正后53/53测试及7份Shell语法通过。首次strict与连带的1项package audit失败，是新增“待确认”实际授权文字触发模板标记扫描；仅改成明确“尚未获得本轮批准”，没有改校验规则、断言、实际D4阻塞或批准状态。原失败日志/RCA保留，workflow实际失败没有重试或改为PASS。

证据见`evidence/d4-prestart-summary.json`、source-binding、workflow-result、preservation、structured-review、governance-checks和private-evidence-index。仅脱敏计数/状态与摘要进入Git；真实数据库、秘密、原行内容及Docker诊断原文保存在私有目录。当前依赖恢复授权问题仍未答复，D4批准保留但执行前置未通过；不得借本次收尾启动D4/D5。
