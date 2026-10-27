# D2工具首次资格/观测归因

首次Python工具测试3通过/1错误：旧producer-only样例没有secret，reader在inspection key路径检查停止；没有连接原数据库。改用保留的完整自然SQL29/37迁移前快照，4项通过。原数据/reader准入不放宽。

首次Go测试在执行测试前停止：默认Go自动工具链校验与GOSUMDB=off冲突。明确使用已缓存Go1.26.5与GOTOOLCHAIN=local、GOPROXY/GOSUMDB off，1项通过；无网络安装。

真实workflow第一次检查失败，诊断仅有固定错误；补充失败阶段/类型后只再执行一次，证实all_containers阶段WorkflowError。独立只读进程及socket检查显示无Docker进程、现有socket ECONNREFUSED；不再重试，不启动服务，不把state ready当实际ready。两个失败结果和state/key保持记录保留。

catalog临时只读常量比较首次误读Go行注释导致KeyError，未执行任何源代码。排除行注释后只比较字符串/摘要，实际旧catalog匹配原工作区FEAT163 permissionInstructions；不修改原dirty文件或采用其实现。
