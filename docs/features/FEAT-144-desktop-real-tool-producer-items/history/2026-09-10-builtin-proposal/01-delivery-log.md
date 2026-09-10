# FEAT-144 — 需求调整记录

## 2026-08-30 原始范围（完整归档）

原包承接FEAT-136拆出的真实MCP CAP-017/GS-004，四文件结构可验证，但具体producer/入口/安全决策未定，D0 BLOCKED、implementation blocked、8AC pending、Tool D4 NOT RUN、调用0。完整原记录见 [history/2026-08-30](history/2026-08-30/01-delivery-log.md)，不追溯改写。

## 2026-09-10 只读审计与需求定稿

1. 用户先要求完整审计；核对四文件、Runtime/Host/Desktop/Contracts、Connectors/Skills，确认原生MCP已具备、产品接入未定、当前Tool适配缺口及旧v5条款过期。复查原D0 exit1，未启动或调用模型。
2. 用户要求记住完整信息、所有可复用机制必须复用，并委托模型选内置工具、确定产品入口/访问/安全验收；明确仅落需求、不执行。
3. 选择view_image为唯一新增类型；现有exec_command仅可选只读检查/代表性失败回归。明确ImageView不是MCP、无status/error/duration/progress、失败可能无Item、completed不证明图像理解；原MCP目标延期未交付。
4. 原四文件逐字归档；重写四文件、完整审计/决策及场景，十项Must从pending开始。更新项目记忆和Epic范围说明，不继承旧D4/额度。
5. 记录固定来源、native/permission pin及Desktop十个并发路径的SHA-256；本轮不触碰产品仓，不修改Runtime或权限。
6. 计划按breaking治理新增安全ImageView版本面，Contract First与单一NativeDisplayBuffer/SQLCipher强制复用；不新增执行器、对账、历史重建或自动封口。没有实施契约/生成代码或更新pin。

## 当前交付边界

本批产物仅为需求文档与审计记录；分离阶段文档审查、适用治理检查结果见02-verification.md。当前实现/启动/真实模型调用/Tool D4均NOT RUN，模型调用0；未来10次含图Responses建议不是授权。当前提交、推送、发布、部署未执行；先前FEAT-136授权不转用。
