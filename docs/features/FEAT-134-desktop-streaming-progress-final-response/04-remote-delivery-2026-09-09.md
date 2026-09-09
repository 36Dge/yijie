# FEAT-134 远端交付核验

日期：2026-09-09。当前状态：**用户“授权执行”后，四个提交已按序推送，远端 SHA 核验通过；CI 未触发**。原 local D4 结论不变；本文件独立记录远端同步，不改写此前“未推送”的历史事实。

## 精确推送对象

目标为各仓 `origin` 的 `chore/retirement-baseline-20260905`，按下表顺序普通推送，不强推、不附带 tag、不合并、不部署。

| 顺序 | 仓库与远端 | 本次已核验本地提交 |
|---|---|---|
| 1 | https://github.com/36Dge/yijie-contracts.git | db7a607c1c091fc4f4243829d68d5b673eb7e2c3 |
| 2 | https://github.com/36Dge/yijie-agent-host.git | f4cf01bd6f7e9f37792ef743d44f0ce10527c10b |
| 3 | https://github.com/36Dge/yijie-desktop.git | 6e5047d1c23041c46dd495ddb89e24c7e4db5d47 |
| 4 | https://github.com/36Dge/yijie.git | 7ddf9e64a56df2af4aa4f6906408b0d1a85a48df |

四仓 fetch 成功；每仓本地领先 1、落后 0，初始工作区干净，push URL 与目标匹配。本轮新文档不在上述四个提交中，不得暗中混入推送。Codex 仓库不推送或修改。

## 来源与 CI 边界

- Host/Desktop native 锁仍指向 Contracts `6f632f155eacdaf93df0e0b00b5dab9e369c5442`；Desktop 权限锁/CI 的 Host 固定为 `f4cf01bd6f7e9f37792ef743d44f0ce10527c10b`。文档 HEAD 前进不要求改动未受影响的 source lock。
- Desktop `pnpm generate:check` 已重新通过：生成来源、native 消费者快照和退役引擎边界有效。另对 native/权限锁 42 个条目逐项比较固定 Git 对象及当前源文件 SHA-256，相等。这些是本地安全检查，不能写成远端 CI PASS。
- 四仓 workflow 的 push 分支只有 main/staging/develop，另监听 pull_request；当前 chore 分支不在 push 匹配范围。
- `gh pr list --head chore/retirement-baseline-20260905 --state open` 四仓均为空。普通 push 预计不触发 CI，推送后需按精确 SHA 再查 Actions runs；无运行记为 NOT RUN，不伪造 PASS。
- 广泛 Host/Rust/Contracts 套件含本任务禁止的测试场景；本轮不创建 PR 或手动 dispatch 来触发它们，也不删除检查或改分支过滤器制造绿色。
- 四次普通推送依次 exit 0；随后 git ls-remote 返回的四个目标分支 SHA 与上表逐一相等，没有附带新文档或额外提交。
- 对上述四个精确 SHA 分别执行 gh run list，均返回空数组；CI 为 NOT RUN（分支不匹配且无 PR），不是 PASS。没有手动触发广泛套件，也没有改检查规则。
- 本次远端分支同步完成；没有合并、tag、部署或发布，不能写成生产交付/全套 CI 通过。

本轮调用文本 0、图片 0。FEAT-134 本地验收、数据范围及保留限制见 [02-verification.md](02-verification.md)。
