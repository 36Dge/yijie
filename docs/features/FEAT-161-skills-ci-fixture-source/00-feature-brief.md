# FEAT-161 Skills CI fixture来源恢复

用户授权审计修复Skills远端CI缺少Connectors fixture，真实验证后提交推送；不复制维护第二份、不绕过检查，全程沿用正常非破坏性安全要求。

contract-impact=none：仅CI装配缺失依赖及更新已有开发校验依赖，不改原fixture、业务输出、对照断言、公共协议、Runtime或持久数据。

原Skills CI只checkout本仓，测试`tests/thirteen-fourth-sale.test.mjs`从`../yijie-connectors/worker/fixtures/linkfox-sale-request.json`读取唯一对照；远端run39114497051以及父提交run39092233163均为该ENOENT，144/145通过。

复用Desktop既有多仓checkout布局，Skills放入yijie-skills，Connectors放入相邻yijie-connectors；沿原固定checkout action，以完整commit e2792f9be5b52cc22d99788157855131224c80dc只稀疏检出该文件。仓库为公开只读，无需新secret，contents:read不变，凭据不持久化。调整原run working-directory、pnpm版本定位及cache lockfile路径，原install/lint/test/audit全部保留。fixture SHA256为fa063bc75ca1c88a1bf070a1291c022e4b04d4c41208215f3cdb20819d151e93。

不添加备用fixture、缺失跳过、自动生成expected、浮动branch或新的拉取引擎。Connectors及其fixture不需要改动。先在临时干净Git检出执行完整原检查，再按用户授权提交推送Skills并等待实际GitHub Actions；真正远端CI只能在提交推送后触发，结果不以本地执行替代。最后元仓记录真实提交和run。

干净检出的原测试145/145通过后，首次到达原audit步骤，发现旧依赖6项high、2项moderate通告。保留原审计阈值与已有override机制，将fast-uri从3.1.5固定到3.1.8，smol-toml从1.7.0固定到1.9.1，用仓库声明的pnpm 11.7.0重新生成锁文件；没有新增依赖、忽略通告或攻击复现。版本依据为[fast-uri 3.1.8官方发布](https://github.com/fastify/fast-uri/releases/tag/v3.1.8)、[smol-toml 1.9.1官方发布](https://github.com/squirrelchat/smol-toml/releases/tag/v1.9.1)与对应审计通告。原schema/manifest/业务资源不变，以完整lint、145项测试和合成eval校验验证现有资源兼容。

pnpm/action-setup沿其固定版本提供的package_json_file输入读取已有package.json中的packageManager，不在workflow重复维护pnpm版本。实施提交后验证远端；如需回滚，使用正常revert退回本次CI配置/依赖提交，不修改fixture来源或用户数据。
