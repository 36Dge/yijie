# S4h 预检停止与修正

新入口首次调用在source preflight退出1，0个leaf启动。Contracts gitignore的node_modules/只忽略目录，不忽略同名symlink；新资格目录设置了symlink，预检按设计拒绝dirty。缺陷在本轮准备，非产品生成差异；不存在绕过git status的理由。

已将仅本轮新树的dependency链接转换成正常ignored目录，目录内复用原固定已安装包；未改gitignore、lockfile、任何旧文件/二进制，也未下载安装。六个源checkout现均干净。新入口没有重复执行，原失败证据保留。推荐一次完整19项检查，失败即停；不消耗模型额度。
