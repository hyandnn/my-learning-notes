# GitBook 接入与发布

## 当前结构

- 在线阅读：https://roborock-1.gitbook.io/merci-robotics-notes/
- GitBook 管理：https://app.gitbook.com/o/sYxx5x49IVH1o6Swx7bu/sites/site_2vD56
- 已完成：20 个页面的首次内容导入、外观配置和公开发布。
- 待完成：GitHub App 与本站点的首次持续 Git Sync 连接，以及一次提交回写验证。

- 内容仓库：`hyandnn/my-learning-notes`。
- 发布分支：`main`。
- 内容目录：`docs/`。
- 首页：`docs/README.md`。
- 导航：`docs/SUMMARY.md`。

根目录 `.gitbook.yaml` 供从仓库根连接时使用；`docs/.gitbook.yaml` 供内容映射直接选择 `docs/` 时使用。选择其中一种映射方式，不叠加 `docs/docs`。

## 首次连接持续 Git Sync

GitBook 插件可以编辑、导入和发布内容；持续 Git Sync 的连接需要在 GitBook 界面完成一次配置。初始内容导入并不等于已建立自动同步。

1. 打开本学习站点的 Git Sync。
2. 连接 GitHub，并给 GitBook GitHub App 授权访问 `my-learning-notes`。
3. 选择仓库 `hyandnn/my-learning-notes` 和分支 `main`。
4. 将本站点的内容空间映射到 `/docs`；空间中的配置使用 `root: ./`。
5. 首次方向选择 **GitHub → GitBook**。确认导入目标是本学习站点。
6. 完成同步后检查首页、课程目录和贝叶斯例题。
7. 提交一次小的正文修改，确认 GitBook 也更新，再开始日常维护。

如果采用单空间从仓库根连接，使用根目录 `.gitbook.yaml` 的 `root: ./docs/`。

## 日常维护

优先在仓库编辑，以分支 / PR 检查后合并到 `main`。已经发布的站点会随同步分支更新，所以未完成正文留在草稿区。

GitBook 支持双向同步；若在 GitBook 修改内容，先拉取回写到仓库的提交再继续本地工作。

## 外观约定

简洁主题，蓝绿色强调色，正文保持适合长文的宽度；首页使用课程卡片和抽象几何封面。启用章节翻页与系统主题切换，搜索入口保持显眼。

基础站点优先使用免费可用的阅读功能。AI 问答、PDF 导出等功能取决于 GitBook 套餐，不作为第一版运行的前提。
