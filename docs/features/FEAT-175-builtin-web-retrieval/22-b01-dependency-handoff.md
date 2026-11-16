# FEAT-175 B01依赖交接清单

2026-11-15源码盘点完成。Owner统一为段成威；[机器清单](references/b01-dependency-inventory.json)记录逐项文件、行号、SHA、交接材料及验收编号。所有生产运行资格仍未核验；本轮不读取账户／Key、不访问公共服务或检查实际部署。

| 依赖 | 已有可复用内容 | 缺失交接／实现 | 通过判据 |
| --- | --- | --- | --- |
| DEP-AUTH | Native OIDC登录／refresh／logout；production HTTPS配置；API RS256及tenant/capability模块 | 正常产品origin／issuer／JWKS和部署版本、两个测试账户及成员资格、真实生命周期证据 | 登录、续期、退出／换租户可用；local demo身份不用于公网 |
| DEP-WEB-AUTH | S1委派／撤销／operation等源契约 | web.retrieve权限及方向兼容、server记录、Native续期和私有安装通道、secret wrapper／日志校验 | B1-A1/A2/A3/A8；普通续期不断任务，binding撤销覆盖重叠grant |
| DEP-CARRIER | Native-owned控制通道与5秒交换；S1 loopback MCP配置及进程内回调 | 公开chat/expert的真实scope装配、独立feature协商、Service真实thread/turn/专家绑定、worker取消ACK | 不伪造MarketEnabled或本地身份；单reader；正常停止／账户切换不复活旧调用 |
| DEP-MODEL | 两模型本机profile；既有两供应商计量及原生重试关闭入口 | Q2精确profile／凭据来源资格和专属预算模式；公开模型服务／resolver及真实Responses资格 | 技术Q2与最终产品资格分别记录；新用户两模型真实可用 |
| DEP-CLOUD | API PostgreSQL／事务基础，现有REST参数与结果适配，local Compose及非生产模板 | server target、服务身份／TLS、Secret引用、operation／claim迁移、有限额度和实际HTTP资格 | B1-A4—A7及N06/N07/N09；最多一次派发、取消隔离、unknown不重发 |
| DEP-DIST | 现有打包及38项通用Skill渠道检查 | FEAT-175签名／公证／渠道回执、允许公开的资源集、新设备验收 | B1-A7/B2-A7/Q4；安装后无需额外搜索动作，正常退出和重开 |

## 关键边界

1. 身份代码已支持生产配置形状，不能据此认为公开环境已验收。仓内主要运行证据仍为local-lab；外部是否另有资源本轮未查询，不作不存在的结论。
2. API权限目录目前只有7项，没有web.retrieve。新增权限应源先行并审查旧消费者兼容，不能用workspace.use替代收费工具资格。
3. 当前控制装配明确受local＋demo_fast约束；公开carrier是必要交接。专家产品ResolveExpert路径也尚未调用WithExpertWebPolicy，S1纯配置验证不能代替正式接线。
4. 服务端托管搜索Key不等于主模型推理服务已托管。Q2可先使用经批准的本机技术profile；Q4仍需产品模型服务或明确既有模型配置边界，不在FEAT-175中默默新建推理网关。
5. 现有Kimi Backend含serial／permit／cancelled状态；服务端只共享纯适配逻辑和秘密引用，每operation的I/O状态须独立。不能把Q1中本机停止成功当成云端已停止或免计费。
6. 37项专家bundle目前只声明local-development，三个data-analyst版本的再分发状态未核实。已有38项通用Skill的desktop-distribution资格不覆盖它们；可选的公开资源集需独立形成证据，不能改标签放行。

## 对执行顺序的影响

以上六项不阻止已经完成的Q2离线准备。技术Q2的必要前置是明确的模型profile／凭据来源、专属计量接线及费用授权；无需先建成完整公开云端，避免依赖循环。

S2/S3开发可以复用上述代码基础，但公开启用和Q4必须取得全部交接。交接材料只包含版本、配置引用、secret引用和脱敏验收结果，不要求将真实Key写入仓库或交给模型。
