# GitBook 接入与发布

## 当前结构

- 在线阅读：https://roborock-1.gitbook.io/merci-robotics-notes/
- GitBook 管理：https://app.gitbook.com/o/sYxx5x49IVH1o6Swx7bu/sites/site_2vD56
- 已完成：20 个页面的首次内容导入、外观配置和公开发布。
- 已补充：PR / main 的自动文档检查、内容纠错模板与维护说明。
- 待完成：GitHub App 与本站点的首次持续 Git Sync 连接、双向同步验证，以及首页布局开关、桌面和手机的浏览器视觉验收。

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
4. Project directory 使用仓库根目录；Content mapping 将现有“机器人学习笔记”空间映射到 `/docs`。此时使用 `docs/.gitbook.yaml` 中的 `root: ./`。
5. 首次方向选择 **GitHub → GitBook**。确认导入目标是本学习站点。
6. 完成同步后检查首页、课程目录和贝叶斯例题。
7. 合并一次小的正文修改，确认 `Docs check` 成功且 GitBook 对应页面已更新。
8. 如需使用 GitBook 编辑，在 GitBook 创建并合并一个小改动，确认回写到正确仓库与分支，再拉取最新内容。

如果采用单空间从仓库根连接，使用根目录 `.gitbook.yaml` 的 `root: ./docs/`。

站点级 Git Sync 会生成 `gitbook-docs.yaml` 映射文件。保留界面为现有空间生成的稳定 `key`，不为已经发布的空间随意换 key。具体以 [GitHub Sync 官方步骤](https://gitbook.com/docs/docs-as-code/git-sync/enabling-github-sync)和[内容配置文档](https://gitbook.com/docs/docs-as-code/git-sync/content-configuration)为准。

## 日常维护

优先在仓库编辑，以分支 / PR 检查后合并到 `main`。完成 Git Sync 连接后，已经发布的站点会随同步分支更新，所以未完成正文留在草稿区。连接完成前，GitHub 提交不会自动更新现有 GitBook 内容。

GitBook 支持双向同步；若在 GitBook 修改内容，先拉取回写到仓库的提交再继续本地工作。

## 外观约定

简洁主题，蓝绿色强调色，正文保持适合长文的宽度；首页使用课程卡片和抽象几何封面。启用章节翻页与系统主题切换，搜索入口保持显眼。

基础站点优先使用免费可用的阅读功能。AI 问答、PDF 导出等功能取决于 GitBook 套餐，不作为第一版运行的前提。

## 验收记录（2026-10-04）

- [x] 仓库独立维护，公开正文均位于 `docs/`。
- [x] 20 页导航、相对路径和锚点通过检查。
- [x] 已通过 GitBook API 确认公开发布、中文、主题切换、搜索和章节翻页设置。
- [ ] 在 GitBook 应用中落实首页布局开关（隐藏目录、页内大纲和首页翻页）；仓库首页 frontmatter 已配置，当前插件的页面更新接口尚未应用这些开关。
- [ ] 桌面和手机浏览器检查：卡片、目录、公式、Mermaid 和折叠问答。
- [ ] GitHub → GitBook 自动同步一次。
- [ ] GitBook → GitHub 回写一次（如使用网页编辑）。

API 可验证内容与配置，但不能代替浏览器视觉验收。GitBook 插件授权与 GitBook GitHub App 的仓库同步授权是两个独立连接。
