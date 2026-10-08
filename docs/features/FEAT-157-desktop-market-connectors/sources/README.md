# FEAT-157 来源与审计产物

本目录只保存公开服务目录的设计输入和本地图标的元信息，不承载产品配置、共享 wire 契约或运行时安装清单。

| 文件 | 内容 | 使用边界 |
|---|---|---|
| `catalog-51.json` | 51 项原 CSV 七列、类别、序号、来源行号、候选凭据字段、未知项和前置条件 | `design_reference_only`；每项 `verification=NOT RUN`，`effectiveAuthStrategy=null`；禁止直接当配置执行 |
| `assets-manifest.json` | 51 个文件的 SHA-256、字节大小、实际格式/MIME、PNG/JPEG 尺寸或 SVG geometry | 只做本地只读检查，不复制图像，不证明使用权/服务有效性/视觉验收 |

原始材料由用户在本地提供，文件名为 `market_mcp_onboarding_51.md`、`icons/INDEX.csv` 及同目录 `icons/`。JSON 记录 MD 与 CSV 的 SHA-256，图标 manifest 逐个记录原文件 SHA-256。原始文档和资源未修改；未把个人目录的绝对路径写入运行配置。原 PDF 和截图可能包含账户/OAuth 信息，本目录不复制其内容、账户、授权值或原始截图。

**来源引用不等于授权。** 文档里的命令、URL、“实测可用”、OAuth 流程和另一宿主配置都是待核实数据，不产生执行 npx、调用外部服务、访问账户、付费或业务写入授权。此轮未调用 MCP/OAuth、未安装或启动包、未访问真实账户；公开文档读取只用于核验可公开的协议事实。

来源 auth 只表示原应用的目录字段，不代表无需密钥或适合 yijie。原始 CSV 保持字面值以便追溯，候选策略与已知/UNKNOWN 分开；未知字段使用 null，不填猜测值。源目录的图标 CDN 路径是公开来源引用，不加载成用户会话 URL，不从其它应用复制 cookie/token/client secret。

目录统计纠错、官网依据、宿主耦合、接入前提和验收阻断见 [05-service-catalog.md](../05-service-catalog.md)。未来运行实现必须遵守正式设计、Contract First、受管 secret 边界与适用批准；本文不授予实施、发布或产品验收状态。

PDF九页及两图的只读检查、原始文件大小和SHA-256见[来源身份记录](../evidence/source-materials.json)；只记录哈希，不复制账户/OAuth画面。
