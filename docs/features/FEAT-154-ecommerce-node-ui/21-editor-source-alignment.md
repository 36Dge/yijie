# FEAT-154 编辑器来源对齐与真实截图归档

> 2026-09-16 · 已完成标准重建、登记、激活及定向回归；**实现完成，完整验收未完成**。本轮新增证据尚未提交，无推送。

## 1. 本轮范围与执行结果

用户授权对齐`6d5b3095…`编辑器来源、统一状态、补真实截图，并要求继续后续工作。保持不修改系统显示、暗色延期及跳过额外原生菜单验收的决定。整个需求仍是30节点纯UI；试运行可点击，只显示未接入提示，不调用节点接口、不处理业务、不生成模拟结果。

本轮`contract-impact=none`：没有源码、公共协议、持久化、部署接口或状态语义改动，只使用标准工具重建已提交源码并修正文档证据。此前第2步的semantic契约变更及其先行提交记录保持。

| 授权工作 | 实际结果 |
|---|---|
| 对齐编辑器构建来源 | PASS；canonical build/check/register/up，manifest完整source_commit对应6d5b3095；三个消费者检查通过 |
| 统一当前状态 | 00/01/02/16及feature.yaml关联本轮21；R2、19、20明确作为历史轮次 |
| 补真实截图归档 | PASS；2张1180×760浅色原生App截图字节原样归档，有校验值及候选身份 |
| 浅色1440×900 | NOT RUN；只操作窗口自身zoom，原生测量1512×875，不替代目标；未改变系统显示 |
| 暗色两尺寸 | NOT RUN；按用户决定继续延期 |
| 最终D4 | BLOCKED；AC-009仍pending，没有全部Must在同一最终候选fresh run通过的结论 |

## 2. 启停与数据保护

开始时App不在运行，Docker正常打开后，发现旧Coze/MySQL容器历史exit137、OOMKilled=false，其余旧容器退出0；原因未知，记录在[停止前状态](evidence/editor-source-alignment/runtime-before.json)。没有把历史137改写为正常退出。

使用已有`make workflow-recovery-plan`及`make workflow-recover RECOVERY_ID=e8d6e427-4c70-4132-a813-2088d28ca26f`完成恢复：4份停止状态数据保护副本、原依赖启动、私有只读操作/执行核对、原应用启动、正常停止。最终容器退出均0，数据卷保留，无强杀或故障注入。用户后续“当作正常停止，继续下面任务”作为继续工作的授权；真实退出0已由标准恢复独立核实。见[恢复结果](evidence/editor-source-alignment/recovery-result.json)、[正常停止](evidence/editor-source-alignment/normally-stopped.json)。数据副本不是已执行还原演练的证明。

恢复前只读事实与20最终原稿的非审计事实一致；原有已登记qualification记录没有新增未解释的在途状态。此次新App前后全部非审计事实继续相等：API资源21/操作130；Coze工作流17/执行36/操作117/节点执行108。正常列表、读取、会话bootstrap及历史读取增加11条审计；窄范围两处试运行前后**所有事实含审计完全相等，增量0**。见[整轮比较](evidence/editor-source-alignment/ui-persistence-comparison.json)、[试运行比较](evidence/editor-source-alignment/trial-comparison.json)。这不是全流量抓包；无业务调用结论同时依赖既有调用链审阅、产物字节一致与当前UI结果。

## 3. 当前候选与可复用产物

| 项目 | 当前候选 |
|---|---|
| Coze提交 | `6d5b309519c2c027fee4a37a107f15c56d554645` |
| manifest SHA-256 | `b17f052dc9985579157bfe7bce141951a5f62e9d54d58f7f91a0e6bdda732d22` |
| Coze source digest | `39000526e47f09e2bbf0403a8a87d940733e1532e695efe5033dff6c5d211fad` |
| 契约源提交 | `db4458fe94572c4df41a114005d54a049bb79b1f`，三个消费者锁保持 |
| 激活epoch | `4b160abe-3fee-459e-971b-78d39421df0d` |
| Desktop源码提交 | `4a8a67bec4903624ca98a1098572fa26f3a20849` |
| Desktop binary SHA-256 | `83c22b3fbf4989943bb2e3dcaaaf5839a75f54f2b014609fed287e46e9d18f6f` |
| 本轮原生App进程 | 6596；canonical `pnpm tauri:demo-fast:app` |
| 标准类型检查 | 126条既有诊断，新增0 |

完整锁、摘要及入口见[最终候选](evidence/editor-source-alignment/candidate-final.json)。新manifest与20的77878acf仅source_commit不同，**385项静态资产字节完全相同**；只读内存比较替换回旧commit后可重现旧manifest的精确SHA，未手改产物，见[比较证据](evidence/editor-source-alignment/manifest-comparison.json)。静态CSP检查与真实浏览器资格分别记录。

API/API-test/Coze镜像来源摘要与已登记镜像一致，因此复用原镜像；标准up检查与健康检查通过。Desktop标准packaged入口没有跳过构建的选项，执行其正常增量构建与启动，没有用手动启动绕过运行环境；二进制摘要已更新并记录。见[复用核对](evidence/editor-source-alignment/artifact-reuse.json)、[标准构建](evidence/editor-source-alignment/editor-build.txt)、[登记](evidence/editor-source-alignment/editor-register.txt)、[服务启动](evidence/editor-source-alignment/services-up.txt)、[Desktop日志](evidence/editor-source-alignment/desktop-launch-final.txt)。

## 4. 当前候选定向回归

原生浅色1180×760实际检查：30项目录、`Listing 综合诊断`完整名称搜索、05候选商品`ALIGN-05-A`、最小样本量20→0、对象下界0.05→0.1及上界0.95、Tab焦点、侧栏重开、自然到期重连保留、两处试运行提示、离开取消、恢复原稿。实际步骤及边界见[UI记录](evidence/editor-source-alignment/ui-observations.json)。

原稿已恢复为`FEAT153 原生终验 0913`，Start/Text/End和两连线、已保存；导航展开，窗口还原1180×780，目录关闭。六项主服务健康，App保留运行。没有重跑用户要求跳过的额外原生菜单/删除/撤销验收，也没有声称本轮再次人工填写全部30表单或634字段。20的完整30节点证据保留其原候选身份，不能与本轮拼成完整D4。

窗口正常zoom实测1512×875后已恢复；它只能说明此次窗口操作未达到1440×900，不能推定硬件绝对上限。原生尺寸证据见[尺寸记录](evidence/editor-source-alignment/window-geometry.json)。

## 5. 真实截图

两张图直接来自本轮CUA原生App窗口截图。原始JPEG字节经本地临时TextEdit纯文本转存后解码；捕获时字节数/CRC32与本地导出逐项核对，未生成替代图、重绘或编辑。TextEdit临时文档关闭并正常退出。候选、逻辑尺寸、像素尺寸、主题和SHA-256见[截图登记](evidence/editor-source-alignment/screenshot-ledger.json)。捕获精确时间工具未提供，登记时间为归档时间。

| 截图 | 内容与限制 |
|---|---|
| [01 原生目录](evidence/editor-source-alignment/01-catalog-light-1180x760.jpg) | 目录当前可见部分；总计30项由AX另行核对，不声称截图同时显示30项 |
| [02 对象与键盘焦点](evidence/editor-source-alignment/02-form-focus-light-1180x760.jpg) | 05的下界0.1、上界0.95及清除按钮焦点；零值字段在可见区域外 |

本轮可离线审阅截图为2张；历史轮次仍为0张，不用新图填补过去的视觉证据。

## 6. 收口与剩余条件

本轮构建/登记/check通过；文档严格检查、声明审计、元仓lint/50项测试、Shell语法及最终来源保护检查见[最终检查](evidence/editor-source-alignment/final-checks.json)。D4门禁未通过的实际结果单独留存，不将文档检查当作产品资格。

剩余只在获允许且满足条件的环境补浅色1440×900、暗色1180×760及1440×900，并在同一最终候选执行全部Must的fresh run后通过D4；用户跳过的额外原生菜单复验仍保留说明。没有修改系统外观/显示、排除AC、推定豁免或关闭需求。本轮只新增/更新元仓文档与证据，源码HEAD保持，无新提交或推送。
