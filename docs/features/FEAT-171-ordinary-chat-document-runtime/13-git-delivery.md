# FEAT-171 Git 提交与推送

用户在实现复审后明确要求将易界全部仓库改动 git add、git commit 并推送对应远端分支，提交说明由模型总结。本次授权覆盖源码版本控制交付；产品发布、安装和此前暂缓的四项D4验证未因此获准。

`contract-impact = none`（本次Git操作及来源引用刷新）；FEAT-171产品变更总体仍为`breaking`。没有追加产品行为修改或模型调用。

## 提交顺序与来源

先提交并推送Runtime，再按canonical generator更新Contracts原生来源，随后Host、Desktop；Desktop来源快照固定已提交Host。分支保持既有分支，目标均为各自的`origin`。

| 仓库 | 当前分支 | 提交 |
|---|---|---|
| yijie-codex | `chore/retirement-baseline-20260905` | `fe3f5b1c768f2a1464314e2a350d419a3e63d9c6` |
| yijie-contracts | `feat/feat164-primary-20261028` | `b0fb797b114291769c089021f95eb48a5f45dbd9` |
| yijie-agent-host | `feat/feat164-primary-20261028` | `61bd306f607e1b8604b9e763f633cbc4f8db53d1` |
| yijie-desktop | `feat/feat164-primary-20261028` | `5e8f9d2cb29ceeda8e9f28ff68d6c8923596e46c` |

元仓 `yijie` 在上述四仓之后提交本需求、ADR-0024、验收与复审记录；元仓身份以包含本文件的提交为准，推送后再核对远端HEAD。完整机器记录见[git-delivery.json](references/git-delivery.json)。

另7仓（admin-web、api、skills、connectors、knowledge、infra、coze）没有本地改动或未推送提交，已核对原远端分支。构建产物、受管运行包、测试日志及截图继续保留本机；Contracts的两份`.local`临时展开材料纳入忽略规则。

## 检查与边界

重新执行原生文档投影、文档契约及Host/Desktop消费者一致性检查，并验证Desktop的553个Host来源输入。变更内容、文件类型和提交差异已核对；补丁内20个单空格行是统一diff必须保留的空上下文标记，经过补丁语义检查，未改写已验证的补丁/二进制摘要。没有新增产品测试范围。

12复审记录及机器证据保留当时的未提交HEAD和检查事实；本文件记录随后Git交付，不把历史测试重新标为对另一版本的完整验收。源码与生成引用同步提交不构成发行资格；干净安装、最低配置、升级回退、深色界面仍为NOT RUN，完整D4保持NOT RUN。Kimi请求仍62次、MiniMax0次。
