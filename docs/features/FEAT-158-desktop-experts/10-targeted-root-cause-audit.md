# FEAT-158 快捷问题与握手定点排查

状态：两处定点代码修复与局部验证完成；原现场唯一归因和真实产品复验仍保留边界。仅覆盖用户明确指定的快捷问题替换、Shopify初始化握手，不重跑内容Eval、剩余生命周期或外观验收，不用局部结果宣布D4通过。

用户最新指令：“继续认真从代码逻辑上排查快捷问题替换和连接器握手的问题，找到明确根因再修复，不要猜改，可追加真实模型调用，但不要扩大验收范围。”必要实测逐次记入 `evidence/phase7-targeted-ledger.json`；当前真实模型0条、业务tools/call为0。Git与已有改动基线见 `evidence/phase7-baseline.json`。

## 握手根因证据

旧日志只有6次HTTP200和initialize最终Unavailable，不能单独判断响应格式。先审固定SDK解析链，再对编译registry中的公开免密钥端点做一组initialize/notifications初始化元数据观察；随后只补同一响应缺失的长度头证据。两组共4个HTTP请求，无商品查询、tools/list、tools/call、账户、凭据或模型调用；不保存响应正文、session值或任意headers。

两次initialize均返回HTTP200 application/json，JSON-RPC id匹配，result包含protocolVersion=2025-11-25、capabilities、serverInfo，无session。两次notifications/initialized均返回HTTP200 application/json，完整4字节JSON literal null（SHA256 `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b`）；补充观测确认Content-Length=4，无Transfer-Encoding。

固定SDK的HTTP adapter对200 JSON反序列化ServerJsonRpcMessage，null不是该消息类型；initialize需要通知发送成功才能完成。此前“可能是SSE”的假说不再作为根因。现有SDK初始化退避重试说明为什么原UI流程出现三对HTTP200，HTTP成功不代表MCP握手成功。

已在Connectors既有HTTP适配边界兼容这个确切的Shopify通知响应；不改Runtime、SDK版本、协议版本、目标地址、授权或工具策略。不把一般HTTP200视作成功，不忽略业务错误，不扩大metadata白名单或一次性调用许可。

官方依据：[Shopify Global Catalog](https://shopify.dev/docs/agents/catalog/global-catalog)、[MCP 2025-11-25 Streamable HTTP](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)。MCP标准要求已接受通知返回202空体；本次观察到的200/null是需要明确隔离的服务端兼容差异，不声称它符合标准。

## 快捷问题排查边界

上一轮真实界面出现二次替换未生效，但ready常量化的memory-router回归通过。当前代码审计发现其未包含真实权限续期链：本地投影TTL240秒、提前30秒续期；同scope续期更新expiresAt与capabilities，Chat authority key改变引发context重绑；专家确认监听context变化，销毁确认并静默拒绝旧回调，原草稿保留。

这是一条可由正常续期到达的确定机制，但尚无原现场点击与续期的精确时间对应证据，不能直接宣称它就是run8那次事件的唯一原因。接下来只对这条正常续期链做定点回归；保留旧context确认不可执行的安全边界，不修改全局权限生命周期，不跨scope自动重放动作。

## 契约与验证范围

本次增量contract-impact=semantic：第三方已观察通知响应的局部兼容，以及现有确认失效的用户反馈；不新增公共wire/DTO、持久化schema、权限或进程执行器。Feature整体breaking分类不变。第三方协议依据当前官方文档，Runtime依据固定源码，产品行为仍由当前仓库实现负责。

只执行与根因对应的正常局部回归、必要静态检查和canonical来源更新。禁止行为和未执行项目沿用02/09，不能为了证明修复而造断流、权限故障、伪造可执行文件或攻击资源。完整真实产品握手、原现场WebView复验和D4必须与代码回归区别记录。


## 握手修复与已执行验证

`worker/src/tushare_oauth.rs`保留现有admitted鉴权与单次调用许可后，识别固定Shopify目标、POST以及完整的notifications/initialized无id/params消息。只有HTTP200、单个JSON类型头、单个Content-Length=4、无Transfer-Encoding时读取这段流；最多4字节且读到正常EOF，字节恰为null才在内部转换为SDK支持的空204。真实HTTP200诊断在转换前记录。其他响应流不被消费；有效JSON、SSE、平台错误及工具请求沿既有路径。

针对已观察的非标准响应做正常本地协议回归：固定SDK原200/null失败，使用该桥接后成功；既有SDK接受的204与有效200JSON保持正常（这两者不统称标准MCP响应）。同时验证fixed registry分类、现有keyless/admitted/one-shot许可，共7项focused检查通过。使用普通loopback服务与固定SDK，无危险fixture、可执行文件替换或强杀；client.shutdown与服务graceful shutdown正常。Clippy、fmt、diff与canonical worker构建通过，详情见 `evidence/phase7-shopify-checks.json`。

新worker SHA256为`f77ba40baf0c3ae7090bd61f076ade4c62298f138351563c7835556924f88bb3`，旧worker保持原SHA。Runtime、公共契约、目标URL、凭据模式和工具审批未改。源码与解析链由另一代理只读复核，非Owner人工发布批准。

以上确认的是此握手协议缺陷及其局部修复，未再启动产品进行真实启用，也未据此标记连接器工具资格或FEAT-158整体验收通过。本轮真实模型仍0条，业务tools/call仍0。


## 快捷问题的有效复现与最小修复

新增一条正常权限续期回归，保留真实App、permission store定时续期、chat-permission lifecycle、两个expert binding composable、memory router、Naive对话框与专家页。只替换正常Native回复及无关外壳/CSS；没有故障注入。先点击参考问题并保留草稿，再从已选专家胶囊打开第二问题，正常推进210秒触发同tenant、同authorizationRevision的续期。旧context换新、确认关闭、原草稿不变，旧动作不执行；修前有效红例准确失败于详情没有任何失效说明。

修复仅涉及 `src/composables/useExpertSummon.ts` 和 `src/components/experts/ExpertMarketPanel.vue`：同route/scope的待确认动作因上下文变化失效时，明确提示“授权状态已更新，本次操作未执行”，详情和目录复用原NAlert展示；用户再次明确选择后，捕获新上下文并正常替换。保留generation/context/scope守卫，不自动重放或迁移旧确认，不改权限续期、Native、Host、schema或授权。手动关闭/Esc/遮罩关闭即时清理对应确认引用，避免关闭动画期间误报；旧dialog离场不会清掉新dialog。

最终4个相关测试文件共15项PASS，类型、局部ESLint、前端构建、来源/权限/38技能门禁及worker指纹校验通过。证据见 `evidence/phase7-prefill-checks.json`，有效红绿日志归档于 `evidence/phase7-prefill-red.log`、`evidence/phase7-prefill-green.log`。初始测试环境CSS/动画缺失不计作产品红例。原WebView事件无精确续期时间对应，仍不宣称已证明它的唯一原因；本次修的是正常链上明确复现的静默取消缺陷。

## 收口与未执行

本次真实模型0条；公开握手诊断共4个HTTP，业务tools/call为0，无App启动或屏幕操作。没有新profile、Skills/Host/Contracts/Runtime修改、权限扩大或Git提交推送。源码与已记录测试证据摘要一致，范围差异见 `evidence/phase7-final-source-review.json`。

仅局部回归和canonical项目构建通过，不据此宣布真实连接器工具资格、修后WebView或整体验收通过。AC-002/003、AC-006及其余未完成项继续pending，AC-007的历史失败不改，D4未通过；外观继续跳过。最新scope与计数以phase7账本为准，阶段5/6失败记录保持原样。
