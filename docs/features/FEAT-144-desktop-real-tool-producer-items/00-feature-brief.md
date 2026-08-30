# FEAT-144 — Desktop 真实 Tool Producer 与执行 Item Demo Brief

> Profile: demo_fast · Exposure: local · Created: 2026-08-30
>
> 当前状态：**D0 package created / D0 BLOCKED / Feature blocked / implementation blocked / verification NOT RUN**。CAP-017 / GS-004 保持 Epic active scope；真实 Tool producer、产品入口和安全边界等待 Owner 决策，因此尚未满足 D0 退出条件。

## 1. 为什么独立成 Feature

FEAT-136 已交付证据充分的 Command vertical，并保留 producer-neutral Tool schema、Host projection 与 Desktop consumer/UI 基础。它们不能回答以下产品问题：

- 哪个真实 Tool 是用户可理解、可授权的产品入口；
- 哪个 repository 和组件拥有真实 producer；
- Tool 的数据分类、允许参数、副作用、权限与失败边界是什么；
- 如何安全执行成功与代表性失败 D4，而不制造 producer 或扩大权限。

因此 CAP-017 / GS-004 由 FEAT-144 独立承接。FEAT-138 已取消/排除，不得复用；CAP-018 experimental dynamic tool image 也不能替代真实产品 Tool。

## 2. D0 目标与阻断

本 Feature 的产品结果是：Owner 选定一个真实 Tool 后，用户通过明确 local 产品入口发起它，并在 Desktop 中看到真实 started/progress、单一 completed 或 failed terminal、安全投影与正常 hydration。

当前核心 blocker 是一项完整的 Owner decision record，至少必须包含：

1. Tool 类型、用户价值与入口。
2. producer owner/repository；默认责任边界为 Connector 执行、Skill 声明、Host 加载与投影、Contracts 约束、Desktop 呈现。
3. 权限模型、数据分类、允许参数、网络/文件/账户访问与副作用边界。
4. 正常成功与安全代表性失败的 D4 方式。
5. 调用额度与证据保留/redaction 规则。

在该决策之前，implementation 必须保持 blocked，verification 与 Tool D4 必须保持 NOT RUN。

## 3. Authority 与冻结边界

- 最终冻结 Runtime：`b2b20e2fc4a0c94834f34d8cc459e488a1b56277`，reported 0.144.6；不允许修改、升级或替换。
- 当前 contract foundation：`yijie-contracts@87f94c9aa6d4848cb67aa8a1265bd21474edb0bb` / v0.7.0。
- 当前 Host foundation：`yijie-agent-host@96b1fa19783694aef583b614c492fd2b6b5c15cc`。
- 当前 Desktop foundation：`yijie-desktop@7026b47828961e58854b06c822c9c9e11252260d`。
- 如果 Owner 选择把业务 Tool producer 放入 Runtime 或 Host，必须先取得新的明确授权并补 ADR；默认路线不修改 Runtime。

## 4. In scope

- Owner-approved real Tool producer 与 user-visible product entrypoint。
- source-first contract、closed identity、started/progress/completed/failed、stable error、caps/redaction。
- event identity/reconciliation/replay、unknown fail-closed 与 SQLCipher hydration。
- Tool Item 的键盘、status/icon、aria-live、safe copy、theme/viewport/200%。
- 单独授权后的 fresh real success 与 representative safe failure D4。

## 5. Out of scope 与安全约束

- 本批不实现代码，不注册 MCP/Connector/dynamic tool，不执行 Tool D4。
- 不用 generic fixture、模型文本或 CAP-018 image 制造 producer。
- 不涉及 Command、FileChange、Diff、审批、写权限扩展或 FEAT-138。
- 不强杀、不故障注入、不破坏权限、不替换/伪装 binary、不使用攻击 fixture。
- 不启动 Desktop、Runtime、Provider 或模型；本批真实调用 0 次。
- 不 amend、push、tag、merge、publish、release 或 deploy。

## 6. D0 verdict

- Feature ID uniqueness：FEAT-144 经全工作区与 Epic source 唯一性检查后分配。
- Product/UX planning：PENDING；Tool 类型/价值、真实入口、producer owner 与安全/权限边界是阻断性空洞，不能由机器 schema gate 代替 Owner decision。
- Must AC：8 条，全部 pending。
- Contract：NOT RUN，等待 producer/entrypoint/security decision。
- Implementation：blocked。
- Verification / Tool D4：NOT RUN。
- D0 gate：BLOCKED；四文件包和可操作 AC 已建立，但 QUALITY_GATES D0 的真实入口与无阻断性逻辑/UX 空洞条件尚未满足。
