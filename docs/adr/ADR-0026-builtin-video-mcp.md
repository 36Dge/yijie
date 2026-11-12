# ADR-0026：应用内置视频MCP与供应商异步任务边界

## 状态

Accepted，修订2及09交付补充，2026-11-12。[FEAT-173](../features/FEAT-173-builtin-video-generation/00-feature-brief.md)深度复审后修订；用户明确接受补充后的第2版并授权实施；费用、Git及公开发布仍未授权。补充ADR-0025的视频范围，不改其已接受的图片决定。修订1归档在FEAT-173 references/plan-revision-1.json。

## 决定提案

1. 沿用应用自动装配的yijie_media、原MCP/Code Mode/搜索/审批/取消，Host调用Seedance；无Runtime补丁、native-image扩展、dynamic/hosted替代或新媒体进程。150s是当前配置，不是原生能力上限。
2. 复用原运营Keychain解析器/条目/作用域，固定doubao-seedance-2-5-260628，可选供应商参数全部省略；用户无需安装/自备Key。
3. 任意显式专家排除内置视频；恢复也检查当前绑定及pending selection，旧许可不能兜底，原专家MCP/权限/角色保持。
4. 创建/取结果两工具适配异步任务；操作引用复用已有root ID。既有bbolt只保存供应商归属、一次提交及一次交付标记，随session cleanup清理，不增加ACK镜像、独立TTL/配额守护或生成ID服务。
5. get可在本聊天内找回丢失引用；有歧义只返回有界本地候选。同聊天未决/unknown操作存在时跨root也不能重复创建，独立并发需求使用已有新建任务入口。
6. 一次Artifact生产后复用原Store/Native ACK/视频卡片与保存，不重发事件或重建旧spool。handoff标记不代表成功；Host unknown不否定Native ready，也不由供应商成功合成committed。
7. Stop停止当前观察和迟到发布；创建root身份与当前观察context分开。无后台轮询、自动DELETE或账户列表。远端running不可取消，DELETE还可能删除完成记录，不能透明映射到Stop。

## 取舍

延长原生timeout能延长等待，不能代替供应商身份持久化/响应丢失恢复。两工具与最小记录解决首次交付前的恢复；交付后的异常坚持原有Artifact边界，不为视频另建恢复系统。临界handoff不确定和Host重启无法补领时如实报告，不追加生成或伪造通过。

详细语义、修改地图、自然语言验收和有限恢复矩阵见FEAT-173的04、05、02；复审问题见08。本ADR接受也不等于真实调用或公开发布授权。

## 实施记录

2026-11-12 已在本机demo_fast实现，普通MCP共享现有媒体进程，固定Runtime未改；4种真实输入、停止恢复、Native提交、播放保存与正常重开验证完成。凭据沿用原条目，未新增用户授权流程。完整结果与限制见[FEAT-173验收](../features/FEAT-173-builtin-video-generation/12-real-acceptance.md)，不代表公开发布。
