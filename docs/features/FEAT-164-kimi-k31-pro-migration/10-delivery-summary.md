# FEAT-164 当前交付状态

## 当前D4启动前状态（2026-10-27）

当前权威[65](65-d4-preflight-and-workflow-restart-boundary.md)：Owner已批准D4首次受限启动，但预检在workflow读取容器时停止。原Docker Desktop/backend未运行、固定socket不存在，实时ready未获确认。候选、完整D2/D3备份、日常SQL41/三存储映射、实例锁与全模型零派发检查通过；App启动次数0、D4绑定未生成，0模型调用，不进入D5。新增依赖恢复范围已具体列入65，尚未获得本轮批准；既有D4授权不丢失，不改数据绕过ready。以下64及更早描述按各自时点解释。

## 当前D3实施结果（2026-10-27）

当前权威为[64 D3一次维护与后态审计](64-d3-controlled-migration-and-post-state-audit.md)。Owner批准的一次维护已完成，日常Native由SQL37升级到41后正常退出；候选、完整D2备份、实例锁/句柄及数据一致性先行核验，后态完整备份与只读复核通过。67张既有业务表全部旧行不变，仅新增4条迁移记录和3张空表；原Host/Runtime、密钥、账本/预占保持。

当前D3_COMPLETE_STOPPED，不进入D4。无GUI、Host、Runtime启动或新模型调用，无Runtime核心/补丁修改。下一步仍须单独批准D4并重验后态/锁/全模型无派发工作/既有workflow ready；D5长期入口、local G5/G6口径继续待收口。旧SQL37构建不可直接重开SQL41，未执行回退。58接受范围与Owner排除项保持。下列旧阶段按原时点解释。

当前候选仍Desktop841f7c7/Hosta3d8767，App SHA4f7adcadc59db4a6e4cf23e700ebab5858b6ae9d953cd7401780d5778cab0f42、receipt0e6fe8191ffc027d4f1efedf14f7e8562ee1d876068aafa7386410202a2878a7；119包内文件/1216源码输入不变。本轮未改产品代码或重建制品；原工作区、全部账本及两份14.188544元预占保持，累计13次、45元cap及29.740299元保守累计不变。只做本地治理提交，不推送。
