# 对话加号菜单级联与精简

2026-10-08，Owner明确要求：缩减菜单行高，区分添加文件与连接器图标；悬停技能/连接器即可展开级联；精简资源弹层、缩小宽度，保留管理按钮并去掉石墨描边。以当前已实现的ChatAddControl/ChatResourcePanel为基础，保留其他未提交改动。

contract-impact = none：只改Desktop内部临时菜单状态、焦点和视觉，不改Native/Host/API契约、持久化、权限、技能全局启停或连接器本轮选择/全局启停语义。既有选择和配置入口继续复用，hover仅展示并读取既有本地状态，不产生授权/启用/业务请求。Sorftime真实复验仍等待此前单次调用确认，本次不触发。

实现结构：主菜单200px、行高36px；添加文件使用既有file图标，连接器保留现有connector图标。父菜单保留，技能/连接器从当前行展开260px子菜单。优先向右、空间不足向左、极窄视口改为上下排列并限高滚动。悬停不抢搜索焦点，点击/键盘进入才聚焦；通过间隙延迟及共同容器保持鼠标移动可达。Esc先关闭子菜单回到父项，再关闭菜单回加号；方向键及触控点击保留。提交/能力撤回收起菜单。

资源面板仅搜索、列表、底部管理；移除标题/数量/关闭按钮与重复说明。普通技能启停由开关表达，错误/同步中/权限不足保留；连接器必要的不可用状态继续显示，选择与全局开关仍分离。管理按钮继续青柠，常态无边框，键盘焦点保留。复用现有tokens、YjIcon、NaiveUI，无新增依赖或外部调用。

验证：组件hover/键盘/焦点/边界行为、已有启停选择契约回归；前端lint/test/build及仓库要求检查；生产组件本地预览亮暗/1180×760/200%缩放和真实标准App窗口。禁止强杀、故障注入及真实供应商调用。截图为普通本地展示证据，不作为Sorftime连接成功证据。

## 实现与检查结果

- 已完成上述紧凑主菜单、不同图标、悬停级联、精简资源面板与无描边管理按钮。管理按钮保留青柠色，键盘焦点仍可见。
- 标准App快速打开主菜单并立刻进入子菜单时，发现Naive Popover缩放动画影响首次几何测量。此菜单关闭缩放动画，直接按最终大小展示；重新标准构建，快速进入连接器后两层保持8px间距。没有新增延时、原生接口或依赖。
- 专项回归4文件36项通过；最终修改后再次通过同一组36项、组件ESLint和vue-tsc。首次最终专项命令漏写仓库的`.local`排除参数，误收集历史副本测试而失败；采用仓库现有排除范围后仅执行活跃源码测试，未删除或修改历史副本。
- `make lint`通过（使用既有干净不可变Contracts/Host本地快照）；`make build`、`pnpm docs:build`通过。最终`pnpm tauri:demo-fast:app`标准应用构建、正常启动成功，开发包未签名，未发布。
- 生产组件预览完成亮/暗主题、1180×760、200%文档缩放、左侧翻转、长列表滚动、悬停与焦点检查。真实App检查紧凑菜单、技能/连接器两层并存、快速展开稳定位置和两个管理按钮导航（`/plugins`、`/connectors?from=/chat`）。没有操作真实开关或配置入口。
- 全量前端测试为1485通过、17失败、2跳过；17项失败均在本轮修改前的菜单组件上复现。涉及已有来源检查、launcher/依赖约束、FEAT-131/137旧回归、Sidebar与ChatPage预期。没有将整套测试写为通过，也未扩大范围改动这些既有问题。基线使用Vite只读载入备份SFC，未回滚工作区。详细失败清单与比对见证据。

## 安全测试执行失误与限制

Agent曾误启动全量Native测试，随后发现其包含Owner禁止的权限、symlink和故障fixture，立即以正常Ctrl-C中断（退出130），并已向Owner披露。中断前已有部分此类测试执行，包括`native_save_rejects_symlink_and_nonregular_targets`、`token_reader_rejects_open_permissions_and_symlinks`、`readonly_and_corrupt_databases_fail_closed`。不能记为完全未执行或通过；没有重跑，也没有强杀。此事属于Agent的检查失误。

本次界面调整不改Rust/native代码；完整Native套件没有验收结论。后续只能执行预先审查过的普通、非破坏性专项，不得再以标准命令为由直接启动含禁止fixture的整套测试。

## 交付与剩余状态

本次菜单调整已在标准App中可见，工作区保留，未commit/push。模型与供应商新增调用均为0；Sorftime连接修复的真实复验仍等待此前单次发现流程的确认，未将本次UI验证当作连接成功。

证据：[verification.json](evidence/composer-cascade-20261008/verification.json)、[测试清单](evidence/composer-cascade-20261008/test-summary.txt)、[标准App技能](evidence/composer-cascade-20261008/cascade-native-skills.jpg)、[标准App连接器](evidence/composer-cascade-20261008/cascade-native-connectors.jpg)。亮暗/缩放/长列表截图同目录。
