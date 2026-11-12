# FEAT-173 官方API审计

审计日期2026-11-12。用户创建链接末尾含全角分号，按同名官方页面去除尾随标点。ark控制台文档在文本浏览工具中不可访问，使用火山官方docs.volcengine.com的同名文档；没有调用API调试按钮或供应商接口。

## 官方事实

| 来源 | 审计结论 | 页面更新时间 |
|---|---|---|
| [创建任务](https://docs.volcengine.com/docs/ark/create-video-generation-task-api?lang=zh) | 指定模型已列入Seedance 2.5；POST为异步创建。必要内容为model/content。文生、单首帧、首尾帧和图片参考均支持；图片角色场景互斥。当前图片限制为边长300–6000、比例0.4–2.5；本地10MiB/10附件限制仍优先。 | 2026-11-12 14:11:13 |
| [查询任务](https://docs.volcengine.com/docs/ark/get-video-generation-task-api?lang=zh) | GET精确ID返回状态与产物。普通任务ID期限7天，视频URL24小时、2.5产物下载最多100次；不能把任务可查询等同URL可继续下载。 | 2026-11-04 11:07:57 |
| [任务列表](https://docs.volcengine.com/docs/ark/list-video-generation-tasks-api?lang=zh) | 账户级列表能按条件筛选；filter.model描述为推理接入点ID，不能假设是模型名称；列表不提供本地聊天归属。首期不调用/不暴露。 | 2026-11-04 11:07:57 |
| [取消或删除](https://docs.volcengine.com/docs/ark/cancel-or-delete-video-generation-tasks-api?lang=zh) | queued可取消，running不可DELETE；完成/失败/已取消/过期状态调用同一DELETE会删除记录。200本身不证明发生哪种操作。 | 2026-10-30 16:10:32 |

创建/查询共用`https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`；GET单任务在末尾加供应商ID，DELETE亦如此。首期产品仅使用POST创建与GET精确任务。

## 默认参数策略

下面是审计时文档的有效默认值，作为验证基线，**不是要求在请求中显式填入这些字段**：

| 参数 | Seedance 2.5默认 |
|---|---|
| resolution | 720p |
| ratio | adaptive |
| duration | -1，模型在4–30秒范围选择 |
| generate_audio | true |
| watermark | false |
| output_format | mp4 |
| draft / return_last_frame | false / false |
| execution_expires_after / priority | 172800秒 / 0 |

以上来源为[创建任务参数](https://docs.volcengine.com/docs/ark/create-video-generation-task-api?lang=zh)。不能把旧模型seed/camera_fixed/service_tier的示例默认直接套用到2.5；没有需要时全部省略。图片content和role属于用户输入的必要描述，和输出参数调优分开。默认duration可能影响费用，后续验收按实际返回时长和使用量记录，不虚构固定5秒成本。

## 网络与能力核验

官方[单任务响应示例](https://docs.volcengine.com/docs/ark/get-video-generation-task-api?lang=zh)使用`ark-content-generation-cn-beijing.tos-cn-beijing.volces.com`，官方[列表响应示例](https://docs.volcengine.com/docs/ark/list-video-generation-tasks-api?lang=zh)还使用`ark-acg-cn-beijing.tos-cn-beijing.volces.com`。建议作为视频独立精确allowlist初始集合；它们是官方示例而非2.5所有结果域的穷举保证。新域须根据真实返回和官方依据评审，不能为跑通而开放任意URL或通配整个TOS域。尤其不能机械复用Seedream的v2域表。

官方文档说明运营账号还需完成对应模型开通；同Key只解决凭据复用，不证明模型资格或余额。本轮未登录核查、未取Key、未请求模型或任务列表。首期不接人像素材库/虚拟人接口；供应商对输入的限制或拒绝按原事实报告，验收采用合成商品/风景图片。

## 分析与取舍（不是供应商承诺）

- 创建无已证明的客户端幂等保障，因此响应未知不能重POST；本地预占/原ID查询不能保证POST丢失响应时找回远端ID。
- GET观察queued与DELETE之间存在竞态；文档未给条件取消保证。首期不做自动DELETE，停止只承诺本地等待/发布停止；远端可能继续和计费。
- 供应商默认超时远长于现有MCP窗口，采用分段查询；这是对本地调用边界的设计，不修改供应商默认任务寿命。
- 默认MP4并不证明任意结果可在当前WebKit播放或小于64MiB；实际兼容在独立获准真实验收中核对，失败不自动重生成。

## 修订2复核

本轮重新读取官方精确查询与取消/删除页面，任务/URL期限和DELETE状态相关语义保持。仍未调用API。150s属于本地当前MCP配置，不是官方任务寿命或原生Runtime的硬上限；分段查询的原因是持久任务归属与恢复需求。远端删除/列表和运行中任务撤销仍不进入首期。
