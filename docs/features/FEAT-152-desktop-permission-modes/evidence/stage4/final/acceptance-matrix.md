# FEAT-152 最终本地验收矩阵

最终产品源码未在修复后的真实接管、full 与最终 ask 执行之间改变（见 final-build-source-hashes.json、cleanup.json）。以任务 `01a07aa5-6f91-7133-82c6-0cdd9e9bace4` 四轮连续真实流程作为最终 fresh 验收，正常退出/重启属于恢复验收，不声称全部步骤在一个进程中发生。

| AC | 结论 | 最终证据与边界 |
|---|---|---|
| AC-001 菜单/UI | PASS | final-menu-ax.txt实际三档文案/描述/选中；final-restarted.jpg真实主窗口。S4亮暗1180×760生产组件视觉源在最终逐项hash一致（visual-source-continuity.json），不冒称Native弹出菜单截图。 |
| AC-002 请求批准 | PASS | ask-real-flow.json第4轮：项目内默认写入exit0；独立公网HEAD批准HTTP200，项目外写入拒绝无文件；新任务真实默认ask。 |
| AC-003 自动与接管 | PASS | runtime-observations.json第1/2轮与manual-approval.json：真实原生deny→准确操作上下文恰好1次→同任务auto真实allow和准确文件。用户批准的原生文档复核配置，不代表默认策略自然风险拒绝。 |
| AC-004 完全访问 | PASS | 第3轮never/danger-full-access/user真实写入full-final.txt；此前S3真实首次取消/确认与S4生产组件复核保留，最终组件源码未变，不重置用户确认标记。 |
| AC-005 任务持久化/隔离 | PASS | final-restarted-ax.txt同任务4轮完成/ask；other-task-auto-restarted-ax.txt另一任务auto；新任务ask。正常退出/重启，不用注入或改DB。 |
| AC-006 忙时限制/下一轮生效 | PASS | ask-pending-ax.txt菜单disabled，ask-completed-ax.txt完成恢复；第3轮full、第4轮真实ask配置收敛。Native/Host边界聚焦测试作为补充。 |
| AC-007 准确审批/幂等/反馈 | PASS | ask-decision-results.jpg显示两个准确关联的不同决策，Runtime联网执行与文件拒绝对应；manual-approval.json恰好1条准确原生批准上下文。重复/跨任务/失败反馈另有Host正常协议测试与UI78项，不假装进行了危险故障E2E。 |
| AC-008 核心与退役边界 | PASS | source-identities.json核心仓干净、Runtime/manifest原hash；canonical日志退役检查，diff-check.json五仓通过，cleanup.json正常退出。其它用户改动保留。 |

37个真实请求均已完成HTTP200，含首次转发遗漏问题24–27（保留NOT PASS），成功最终四轮28–37，以及S2/S3/先前S4历史。总授权45，剩余8，不新增调用。最终源码同一任务验证替代先前18–23作为ask的当前真实证据；历史失败不删除。

聚焦验证：严格Native Clippy/fmt，3项Native权限测试与相关派发查询测试，UI78项，Host权限/会话race测试及lint，Contracts3项和生成同步，canonical构建。只声明所列正常检查，不运行用户禁止的强杀/权限破坏/攻击/Runtime替换测试。

D4是本地可用结论；公开/生产、提交/推送/发布均不在本次范围。
