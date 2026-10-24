# FEAT-164 本地源固化与G2A

Owner当前明确接受14的候选和离线比较结论，并授权按隔离清单本地提交及继续实施。无push、tag、分支或发布许可；既有FEAT-162/163改动不混入。

- Runtime：57753db451b29a49315ddcb6449ca146171c4de7，6个清单文件。原binary/manifest不覆盖，候选仍未激活。
- Contracts：b0060c8bc4fb924cec14d98b193c32c69482b7b7，19个清单文件及Makefile/支持基线的FEAT-164局部段落。Runtime投影已指向上述真实完整提交；v1/其它候选源与工作树不改。
- Host/Desktop：通过Host scripts/sync-kimi-k31-pro-contracts.py直接读取该Contracts Git对象，新增独立v2/generated/来源锁；旧pin保留。同步check与新Go包编译通过；此时尚无v2业务接线。
- 元仓：仅FEAT-164包/首次审计及项目记忆的FEAT-164段，提交身份由Git实际结果登记，不写入自身假SHA。

原三次基线解析事件在Owner明确接受后完成一次离线复核，实际exit0，机器事件resolved。G2A只覆盖已批准的模型v2及Runtime源候选；市场/专家/计划其它族在后续切片仍须先做适用source-first版本化，不能凭本次结果放行新值。G2V/final仍NOT RUN；当前仅继续最小默认关闭的纵向候选和安全Harness，未申请或消耗真实模型预算。
