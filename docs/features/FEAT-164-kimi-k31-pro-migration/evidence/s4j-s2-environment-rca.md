# S2验证环境RCA

首次当前来源完整driver：Host25/路由2/派发12通过；Native17中14通过、3个后续新增草案IPC回归在schedule_submit入口被拒绝。driver原native-recovery组使用无候选开关env；当前三个测试提交K3.1 model_intent，须既有exact local/demo_fast/chat_models/candidate配置。核对S4g已通过的原执行配置相同。并非正文/模型断言失败，没有外部请求或App数据写入。

修正仅把该组的child环境改为driver现有candidate（与native-delivery相同）。不删测试、不改产品门禁、不放宽17精确命中/0skip。保留首次FAIL；以新输出目录仅一次完整driver复验，以验证更正后的入口。失败不机械续跑。原bundle/产品树不变。
