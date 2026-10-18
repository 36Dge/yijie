# FEAT-159 原生产物媒体扩展

2026-10-18，demo_fast/local。Owner：段成威。用户已明确批准前轮方案、再次审核后实施、新旧专家聊天、testmp4 有声播放、HTML/SVG 内置预览、保存和正常重启恢复。未授权 Git 提交/推送或发布。

contract-impact=breaking：旧闭集/持久reader不能消费新媒体；独立 schema 9 协商，旧 v3–v8 原样保留。Runtime 核心、二进制、patch 均不改。Source first：Contracts → Host → Desktop；本地 candidate 的源摘要与生成物机械同步，不冒充 release pin。

## 已核实复用
- Codex stable MCP、原生 Thread/Turn/Item、权限、正常 unsubscribe/resume。
- Host Store.GetByThread、受管 Cwd、os.Root、Artifact encrypted spool、EventHub、content/Range/ACK。
- Desktop native+Artifact伴随流、SQLCipher、identity授权、预览租约、atomic_save_content、video controls。
- 固定 rmcp 1.8.0 服务端；固定 Wry/WebKit 无IPC preview容器。只新增薄适配。

## 复核决定
动态工具不适用于旧线程；新增独立Host-owned本地MCP adapter，不将读盘塞进market worker。工具仅接受工作区相对路径，thread/turn来自Runtime metadata且复核Host活动记录。重复登记幂等，Host完成暂存才回成功；Desktop成功持久化才显示ready。草案保持空工具集。MCP进程只以控制管道EOF和正常shutdown退出，超时保持stop_pending，不强杀。
HTML首期自包含、允许内联交互、禁止外网/任意磁盘/宿主IPC/持久网站存储；SVG图片上下文矢量预览；MP4保留完整性检查，播放器使用系统解码，首期H264/AAC。旧文件/报告渲染保持原有语义。

## 必须验收
1. 新普通聊天和既有专家聊天经真实MCP登记文件，无Runtime修改。
2. HTML中文/布局/离线交互与SVG缩放在App内预览。
3. 用户/Users/jack/Desktop/testmp4.mp4画面、声音、进度与关闭停止播放。
4. 保存与原文件摘要一致；正常退出重开恢复三种产物。
5. 重复登记、多个产物、早到/晚到引用稳定；不修改原生执行事实。
6. 正常不支持格式/取消/权限拒绝可理解，旧格式回归。

loading/ready/error/retry/expired复用既有卡片；保存取消不算失败，预览失败与文件可保存分开。切换会话/关闭预览释放租约。

## 安全与验证
只做正常非破坏验证；不运行攻击fixture、权限破坏、强杀或二进制篡改。用户视频仅只读，不纳入Git。标准构建允许生成本项目开发产物，不覆盖用户提供/已签名二进制。本轮已获最多4次短文本请求授权，实际新模型轮次2次、保守提交计3次；外部商家和付费图片/视频调用0，未挪用历史额度。不得用seed或synthetic代替真实D4。

## 回滚
先停新producer；保留已提交的Desktop产物。新持久格式使用前向版本与兼容reader，禁止旧binary降级写入。源码回退不自动删除用户数据。
