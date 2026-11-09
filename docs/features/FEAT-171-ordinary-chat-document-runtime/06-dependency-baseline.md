# FEAT-171 D0依赖版本与分发方案

2026-11-09。本文冻结需求设计的首期选型，替代05早先的多套候选。只查询了官方网页、项目维护者发布的PyPI元数据及字体仓库标签；没有下载/安装大包、编译产品、修改运行中的程序或调用模型。机器证据见[dependency-evidence.json](references/dependency-evidence.json)。

“可分发选型”表示公开来源和许可允许按所列条件安排易界自己的构建与交付；不表示还未产生的易界二进制已经签名、完成SBOM、兼容测试或发行履约。D0决策与后续构建/发行证据分别记录。

## 1. 首期平台和唯一主路径

- 产品支持政策：**macOS 14及以上、Apple Silicon arm64、完整离线依赖包**；不是从上游最低系统要求自动推导所有macOS都支持。首期不承诺Intel、Windows、Linux。
- **文档侧采用专用Python单栈**；DOCX用python-docx，PPTX创建/读改用python-pptx，XLSX用openpyxl，PDF用ReportLab/pypdf。移除Node/PptxGenJS第二套文档运行环境。易界已有其他Node业务模块不因此删除。
- Office渲染和支持集公式重算使用独立LibreOffice进程；PDF页图复用现有Desktop Quartz/CoreGraphics路径，向模型交付页图继续复用Runtime原生`view_image`。
- 不增加Poppler、PyMuPDF或私有Artifact Tool依赖。Quartz为目标macOS原生framework，不等于依赖用户安装的Office/解释器，也不新增一个通用模型看图工具。
- TXT/Markdown/HTML/CSV/JSON使用标准文件/数据能力与既有Native预览。用户不需要选择专家、市场技能、连接器或安装开发工具。

这保留Codex的分层装配与输出质量标准，同时避免把其私有JS文档引擎、云Spaces和本机缓存作为易界的分发基础。

## 2. 精确版本基线

| 组件 | 固定版本 | 职责 | 许可/来源 |
|---|---|---|---|
| CPython | **3.12.16** | 专用解释器与标准库 | [官方安全版本](https://www.python.org/downloads/release/python-31216/)、[Python许可栈](https://docs.python.org/3.12/license.html) |
| python-docx | **1.2.0** | DOCX创建、结构解析与支持范围内修改 | [维护者发布页，MIT](https://pypi.org/project/python-docx/1.2.0/) |
| python-pptx | **1.0.2** | PPTX创建、读取和基础对象修改，统一主路径 | [维护者发布页，MIT](https://pypi.org/project/python-pptx/1.0.2/) |
| openpyxl | **3.1.5** | XLSX读写、公式文本与图表/格式 | [维护者发布页，MIT](https://pypi.org/project/openpyxl/3.1.5/) |
| ReportLab | **4.4.9** | 生成PDF、表格/文本/图形 | [维护者发布页，BSD许可](https://pypi.org/project/reportlab/4.4.9/) |
| pypdf | **6.10.0** | PDF文本/元数据提取、页级提取重排合并 | [维护者发布页，BSD-3-Clause](https://pypi.org/project/pypdf/6.10.0/) |
| LibreOffice | **26.8.2 aarch64** | DOCX/PPTX/XLSX正常渲染、支持公式重算 | [官方版本](https://www.libreoffice.org/download/)、[许可](https://www.libreoffice.org/licenses/) |
| Noto Sans CJK SC源字体 | **Sans2.004** | 中文、英文及常用符号一致排版 | [官方标签](https://github.com/notofonts/noto-cjk/releases/tag/Sans2.004)、[OFL-1.1](https://raw.githubusercontent.com/notofonts/noto-cjk/Sans2.004/LICENSE) |
| fonttools（仅构建字体） | **4.60.1** | 源变量TrueType实例化、修改字体族名 | [维护者发布页，MIT](https://pypi.org/project/fonttools/4.60.1/) |

CPython 3.12.16已于2026-10-25发布为source-only安全版；3.12系列仍有安全维护至2028-10。选择它保留成熟3.12 ABI并包含该系列已发布修复，不沿用本机Codex的3.12.14，也不只为追新跳到3.15。没有官方3.12.16 macOS安装器这一事实不妨碍从源构建，但必须由易界构建并验证自己的专用解释器，不能让用户自行装Python。

LibreOffice官网当前提供26.8.2 Apple Silicon包；官方最低条件是macOS 11、Intel或Apple Silicon。易界14+是更窄的支持政策。[系统要求](https://www.libreoffice.org/system-requirements/)。官方DMG元数据为299,236,406字节，SHA-256为`9f24fe83ab1ed5c95eb3df580119f32932f713e577feeac02bf619fb00749b55`，仅作上游来源/体积参照，本轮未下载或执行。[官方镜像元数据](https://download.documentfoundation.org/libreoffice/stable/26.8.2/mac/aarch64/LibreOffice_26.8.2_MacOS_aarch64.dmg.mirrorlist)

以上版本不会在用户任务中解析成`latest`。进入构建时再次检查维护者安全公告；如必须升级，更新本表、机器证据和适用回归，保留旧基线，不在构建中悄悄漂移。

## 3. Python运行依赖闭包

本轮逐项查询所选版本PyPI `Requires-Dist`。Python 3.12、无extras条件下，除上节五个顶层库外，固定以下运行依赖；每项上游sdist URL/文件大小/SHA-256均已记录在机器证据中，不是本轮构建出的二进制hash。

| 组件 | 版本 | 选择理由 | 发布元数据许可 |
|---|---|---|---|
| lxml | 6.1.1 | DOCX/PPTX XML处理 | BSD-3-Clause，底层libxml2/libxslt另留声明 |
| Pillow | 13.0.0 | python-pptx与ReportLab图像依赖 | MIT-CMU，内嵌原生图像库另留声明 |
| typing_extensions | 4.15.0 | DOCX/PPTX类型兼容依赖 | PSF-2.0 |
| XlsxWriter | 3.2.9 | python-pptx内部图表工作簿依赖 | BSD-2-Clause；不作为第二XLSX产品路由 |
| et_xmlfile | 2.0.0 | openpyxl依赖 | MIT |
| charset-normalizer | 3.4.4 | ReportLab依赖 | MIT |
| defusedxml | 0.7.1 | openpyxl官方建议的XML防护配套 | PSF许可；仍保留Native原件准入与资源限制 |

因此运行Python发行包共12项（5个顶层库＋7个配套库），fonttools是第13项但仅用于构建字体，不随文档运行包部署。未选择ReportLab的renderPM/pycairo/bidi/shaping、pypdf的crypto/full等可选extras；加密PDF及未支持复杂文字排版先保留原件并说明，不隐式下载额外库。

官方openpyxl文档明确其**不会计算公式**。因此其成功保存不能当作重算成功；生成XLSX基线由LibreOffice在禁外链更新/禁宏配置下实际重算，并用独立预期值和再次读取检查。超出支持集的公式保持明确限制。[公式文档](https://openpyxl.readthedocs.io/en/stable/simple_formulae.html)

## 4. CPython、原生库和构建锁

专用解释器从官方`Python-3.12.16.tar.xz`源构建，源SHA-256固定为`b5796915dc45ff745cfb4e990a7e7c93d6f546328a102ce31448d69ebc37575c`。使用应用管理的可重定位prefix/rpath策略，解释器与其stdlib/扩展同包；不得是指向系统Python的venv，不安装到`/usr/local`或Homebrew，不覆盖系统或用户程序。

本方案的“锁版本”分三个层次，不能混为已经完成全量binary lock：

1. **D0设计锁**：本文的组件版本、源发布路径、许可证、Python依赖关系与上游artifact摘要已明确。
2. **实现时构建锁**：canonical构建固定SDK/编译器/构建镜像，解析所有build-only依赖及原生dylib闭包；记录CPython实际启用扩展、编译选项、链接依赖，lxml/Pillow wheel或自编产物所含libxml2/libxslt/JPEG/PNG/zlib等精确版本与许可证。不得使用构建机Homebrew隐式补齐，也不得用运行包12项替代完整native SBOM。
3. **发行制品锁**：实际产物每文件摘要、架构、rpath、签名和配对清单、源码/NOTICE包齐备后才能交付安装候选。没有构建出来的hash保持不存在，不能制造占位hash通过门禁。

CPython不附带面向用户的pip/ensurepip、Tk/IDLE开发界面；用户任务不安装包。构建工具只存在构建环境，不属于用户运行前置。macOS系统framework/系统ABI库属于已声明平台条件；任何非系统、非包内链接都使安装候选检查失败。

LibreOffice采用独立版本的易界受控构建资源，不复制Codex缓存或覆盖官方已签名应用。构建脚本、完整对应源码、外部tarball清单和第三方NOTICE随该版本归档；不把“只用headless”当作可任意剥离内部组件/许可证的依据。无需Java/Base能力，也不携带JDK；如果某转换实际要求该能力，结果应不支持而非自动装Java。

## 5. 字体基线和可复现派生

源固定为`notofonts/noto-cjk`的`Sans2.004`标签commit `523d033d6cb47f4a80c58a35753646f5c3608a78`，文件`Sans/Variable/TTF/NotoSansCJKsc-VF.ttf`，上游git blob `e67840913223f5c5db60570ce5bf001b0e079d42`，源大小36,144,788字节。本轮只读取GitHub树元信息，未下载字体或生成派生字体。

构建阶段用fonttools 4.60.1固定实例化weight 400与700，输出两份带`glyf`表的静态TrueType；派生族名固定为 **YiJie Document Sans**，保留OFL和原作者声明，记录变更。这样避免将CFF OTF或变量字体直接当作ReportLab可处理的静态TTF，也不冒用字体保留名称。派生字体仍按OFL-1.1发布，嵌入文档不要求文档本身采用OFL；不能把字体单独销售。[上游许可证](https://raw.githubusercontent.com/notofonts/noto-cjk/Sans2.004/LICENSE)

首期字体资源上限80MiB，两字重覆盖中文正文/标题和Latin；不从macOS复制PingFang/宋体进包。内置字体目录分别由Office转换器、PDF生成器和用户预览使用，不能以系统已装字体掩盖缺件。字体缺字/布局效果及派生文件SHA-256属于实现验收，不是本轮已生成结果。

## 6. 可分发资格与必须履行的条件

| 许可类别 | D0选型结论 | 易界交付必须保留/提供 |
|---|---|---|
| Python PSF及历史许可栈 | 可安排专用构建与随应用分发 | 完整LICENSE/版权和所含第三方声明；修改按条款说明，不暗示PSF背书 |
| MIT / BSD / PSF配套库 | 有明确公开分发许可依据 | 原版权、许可与免责声明；源或二进制包含的第三方组件逐项处理 |
| LibreOffice主代码MPL-2.0 | 可作为独立进程纳入方案，需履约 | 对应源码的实际可得入口、许可通知、修改记录；不得以易界EULA限制接收者的MPL权利 |
| LibreOffice/Python扩展内含第三方组件 | 不能从顶层许可证推断完整包资格 | 从实际版本LICENSE/SBOM逐项收集；如含LGPL/GPL组件，履行其源码、修改/替换或重链接等适用义务，不能用“主程序MPL”覆盖 |
| OFL-1.1字体及派生字体 | 可随软件/文档嵌入分发 | OFL/版权、派生名称与变更记录，不单售字体，不把派生字体改为专有许可证 |
| Quartz/CoreGraphics | 复用目标macOS平台现有能力 | 不复制系统framework或字体；目标系统兼容及开发者签名资格按Apple平台交付要求执行 |
| 私有Artifact Tool/完整Codex缓存 | 不选 | 本机可读取或plugin标MIT不等于整个库/应用/缓存可再分发 |

LibreOffice官方许可页明确主代码MPL-2.0、含Apache来源和其他第三方许可；贡献者的MPL/LGPL双许可声明不等于整个二进制仅有一个统一许可证。[官方许可](https://www.libreoffice.org/licenses/)。MPL的文件级义务、可执行分发与源码告知要求见[Mozilla官方FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/)。本需求选择更清楚的交付路径：易界为该版本保留并提供对应源码/构建材料及第三方声明，而不是只给一个可能失效的上游首页链接。

上线/分发门禁必须拒绝：无法确认来源、许可证缺失、对应源码缺失、不明原生链接、库版本漂移、字体来源不符、平台/签名不匹配。这里的确定结论是**所选公开组件具有可执行的许可履约路径**；实际安装包合规审阅、签名、公证和公开发行仍未执行，D0不把它们提前记为PASS。

## 7. 对后续工程验收的约束

- 实现前生成机器锁与SBOM，源版本与本表一致；无隐式extras/新二进制依赖。若发现不可满足的许可/兼容问题，更新本页决定及影响，不静默换引擎。
- 同一套完整依赖包在开发入口和安装候选使用；干净macOS 14+ arm64用户不需要源码、系统解释器、Office、市场资源或Codex缓存。
- 非破坏性正常样本验证中文字体、Office编辑子集、公式重算及页面渲染；不执行许可证文档提到的攻击示例。
- 本轮没有构建、安装或运行上述选定版本组合；先前Codex专用环境可加载不替代此组合验证。后续产品验证失败应如实记录，不影响本页仅为D0设计锁的事实范围。


### 实施后补充：平台完整性校验

Native整包SHA-256使用macOS自带CommonCrypto（libSystem，SDK中接口自macOS10.4可用），与既有Quartz同属首期平台基础API。没有引入系统Python/Office、额外下载或新的第三方运行包。流式实现保留原清单/摘要/路径检查，并以跨块普通输入和真实整包定向验证；当前机器首次进程校验约3.04秒、缓存检查约0.36秒，不替代最低配置资格。见11记录。
