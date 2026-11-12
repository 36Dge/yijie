# FEAT-172 真实验收与运营凭据准备

更新时间：2026-11-12T13:47:54.078329+08:00。本地实施验收已通过：文生图、单参考图均实际生成并获得Native committed确认，纯图片分析不生成；正常重开可预览已交付图片。原始失败记录保留，不换算为通过。

## 用量与早期验收记录

- 主聊上限24次，已用22次；Seedream上限6次，实际生成2次；LinkFox0次。
- 首次回合：搜索正确发现MCP，旧系统imagegen指南触发6次读取；正常中断，主聊8次，无生图调用。
- 复测回合：已调用新MCP，但实际Host停在旧式Keychain读取；未进入Seedream HTTP。主聊后续等待使用4次，计数器到限后拒绝额外请求。窗口显示未完成；没有伪造成功。
- 客户端、Runtime、adapter及专用服务均已正常退出；计数器以stdin EOF正常退出。未强杀、未修改凭据、未清理历史。

## 已修复并验证的代码

1. 使用原生Skills API按精确路径停用Runtime自带的旧OpenAI imagegen指南；其他技能保持，Runtime二进制不改。
2. 钥匙串查询保留LAContext禁止交互，并对macOS file-based旧路径设置本Host进程的 `SecKeychainSetUserInteractionAllowed(false)`。不解锁、不改ACL或凭据；无权限快速失败。[Apple接口说明](https://developer.apple.com/documentation/security/keychains)
3. 回合结束/取消时立即发送已有Artifact失败终态，不等待外部读取返回；迟到结果不发布，也不重复发送终态。正常延迟回调的race测试通过。
4. 新增仅供local/demo_fast运营诊断的 `--check-media-credential`：由真实Host身份只读检查，输出仅就绪码，没有Runtime、数据库或外部模型调用。

## 需要运营侧完成的事项

此前Host返回 `credential_unavailable`，已定位为当前构建的访问授权缺失。用户在本人请求的系统弹窗中完成授权后，同一Host的无交互只读检查已返回 `ready=true`（25ms，0个Provider请求）。原始失败证据保留。

在本机“钥匙串访问”中核对现有条目并为当前受管Host配置访问授权（保留原Key，不向聊天粘贴秘密）。若条目缺失，由运营侧补齐，不把这项配置交给普通产品用户。

- Service / 条目名：`com.yijie.ai.seedream`
- Account / 作用域：`119cc9bf2e5a365e7b0eb9be114a3f995711189da3b84893c97781b8dce13c43`
- Host Home：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/demo-fast/host-home`
- 受管可执行文件：`/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/development/bin/yijie-agent-host`
- 当前复审构建SHA-256：`3af821aad977030df95ee85c54adc5052c738b5e24669f5d14be4e73e82f742a`（已完成本人授权；同一构建非交互检查24ms ready；旧真实生成证据对应`007a0069…c7e2f8`，不混用）

只为上述受管Host配置所需权限；不需要解锁其他凭据、复制到聊天或改变系统安全设置。系统SecurityAgent不允许由计算机控制工具访问，因此系统授权步骤需要用户本人完成。

完成后先运行同一Host的零费用只读检查，ready=true后才继续使用剩余主聊和Seedream额度。命令如下（无Key参数）：

```sh
YIJIE_ENV=local YIJIE_LOCAL_PROFILE=demo_fast \
YIJIE_AGENT_HOST_HOME='/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/demo-fast/host-home' \
'/Users/jack/Downloads/Personal_Info/CrossBSD/yijie-desktop/.local/development/bin/yijie-agent-host' --check-media-credential
```

代码、来源回执与用户原改动均保留；没有提交、推送或公开部署。

## 本人请求的单次系统授权

用户明确要求再次显示访问授权弹窗。为此添加独立的、仅local/demo_fast且有人值守终端可调用的 `--authorize-media-credential` 运营入口；它只向系统请求读取上述条目的授权，不收集系统密码、不创建/修改Key。当前构建校验值已更新到本页上方。

该入口不注册为MCP或模型工具，普通生成和 `--check-media-credential` 始终禁止交互；用户通过系统窗口完成后，使用同一二进制进行只读复核。不得在授权后无故改写或重建Host，使当前构建授权失配。

## 最终真实结果

| 场景 | 主聊 | 原生MCP事实 | 交付与界面 |
|---|---|---|---|
| 文生图 | Kimi K3.1 Pro，6次请求（13–18） | yijie_media.generate_image一次，use_current_reference=false | Artifact f984cebc-4edf-4ab6-bcc6-0c33348b420a；get_artifact_status=committed；1536×1536；预览/保存通过 |
| 单参考图 | MiniMax-M3，3次请求（19–21） | yijie_media.generate_image一次，use_current_reference=true | Artifact f60e8125-b943-48d8-9ca5-82482610bd3f；committed；1536×1536；保留杯子主体并换木桌/绿植环境，预览/保存通过 |
| 图片分析 | Kimi K3.1 Pro，1次请求（22） | 无工具调用、无生图 | 正常描述图片颜色与环境，零新Artifact |
| 正常重开 | 无新用户回合 | 两个生成回合的MCP调用数仍各1次 | 原入口恢复、Runtime ready；原生缓存图片仍可预览 |

证据：[最终验证](references/final-verification.json)、[文生图](references/real-text-to-image.json)、[参考图](references/real-reference-image.json)、[分析对照](references/real-image-analysis.json)、[请求账本](references/real-call-ledger.json)。专家选择排除内置仍由固定Runtime回环和Host绑定准入测试验证，未调用LinkFox。

产物位于 Desktop 的 `.local/feat172/live-workspace/feat172-text-to-image.jpg` 与 `feat172-reference-image.jpg`。日常客户端已恢复普通入口，计数器已正常停止；没有提交、推送、公开部署或历史数据清理。

## 实现复审后的运营复核

2026-11-12T16:46:55.891804+08:00：本页上方受管路径已由canonical开发入口更新为修复后Host。新SHA与复审构建一致，非交互检查484ms返回`credential_unavailable`，未触发系统窗口、未调用供应商。需本人再次授权同一条目；普通生成仍禁止弹窗。详情与回执见09及references/credential-readiness-reaudit.json。

2026-11-12T17:05:33.593627+08:00：用户明确要求为本页新SHA再次弹窗，授权完成。相同可执行文件随后通过无弹窗只读复核（24ms、ready=true、Provider请求0），Runtime保持ready。凭据复核证据：`references/credential-readiness-reaudit-authorized.json`。此后未重建Host，没有新增供应商调用。
