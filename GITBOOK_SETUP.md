# GitBook 接入与发布

## 当前结构

- 在线阅读：https://roborock-1.gitbook.io/merci-robotics-notes/
- GitBook 管理：https://app.gitbook.com/o/sYxx5x49IVH1o6Swx7bu/sites/site_2vD56
- 已完成：20 个页面的首次内容导入、外观配置和公开发布。
- 已补充：PR / main 的自动文档检查、内容纠错模板与维护说明。
- 已完成：首页隐藏目录、页内大纲和首页翻页，保留正文页的目录与章节翻页。
- 已检查：GitBook 编辑器阅读视图中的首页封面与卡片、卡片跳转、贝叶斯公式、表格、折叠答案和 Mermaid 流程图（包括全屏查看）。
- 已完成：GitBook.com GitHub App 安装，仓库范围仅选择 `hyandnn/my-learning-notes`。
- 已完成：站点级持续 Git Sync，正式同步 `main` 的 `docs/`，保留现有空间。
- 已验证：GitHub 合并后的内容自动导入 GitBook，GitBook 变更请求合并后回写 `main`。
- 待完成：公开页的桌面、手机、搜索与 Mermaid 视觉验收；当前云浏览器无法打开公开域名。

- 内容仓库：`hyandnn/my-learning-notes`。
- 发布分支：`main`。
- 内容目录：`docs/`。
- 首页：`docs/README.md`。
- 导航：`docs/SUMMARY.md`。

正式连接使用根目录 `gitbook-docs.yaml` 描述站点结构，空间目录为 `./docs`；`docs/.gitbook.yaml` 的 `root: ./` 描述该空间的首页与导航。根目录 `.gitbook.yaml` 留作单空间连接的兼容入口，不叠加 `docs/docs`。

## 首次连接持续 Git Sync

GitBook 插件可以编辑、导入和发布内容；持续 Git Sync 的连接需要在 GitBook 界面完成一次配置。初始内容导入并不等于已建立自动同步。

1. 确认根目录 `gitbook-docs.yaml` 已在 `main`，其唯一空间映射到 `./docs`，语言为 `zh`。
2. 打开本学习站点的 Git Sync，选择已有的 GitBook GitHub App 安装。该应用仅获准访问 `my-learning-notes`。
3. 选择仓库 `hyandnn/my-learning-notes` 和分支 `main`；Project directory 留空，使用仓库根目录。
4. 确认界面识别到 `gitbook-docs.yaml`，首次方向选择 **GitHub → GitBook**，执行 Sync。
5. 确认状态为 Synced，空间目录为 `./docs`；检查首页、课程目录和贝叶斯例题。
6. 合并一次小的正文修改，确认 `Docs check` 成功，并核对 GitBook 内容版本对应这次 GitHub 提交。
7. 在 GitBook 创建并合并一个小改动，确认回写到正确仓库与分支，再拉取最新内容。

如果采用单空间从仓库根连接，使用根目录 `.gitbook.yaml` 的 `root: ./docs/`。

GitBook 的 GitHub App 与 ChatGPT 中的 GitBook 插件是两个独立授权。已完成 **Only select repositories → hyandnn/my-learning-notes** 范围的 GitHub App 安装。应用权限为元数据读取，以及代码、提交状态和 Pull Request 的读写，用于双向同步。

`gitbook-docs.yaml` 已保留 GitBook 原生导出生成的稳定 `key: space-1` 与 `path: robotics-notes`，不要为现有空间随意换 key。目录分组由 `docs/SUMMARY.md` 维护，当前公开章节使用 `slam/foundations/...` 等简洁路径。配置以 [GitBook 官方站点映射 Schema](https://api.gitbook.com/gitbook-docs.yaml) 为准。

## 日常维护

优先在仓库编辑，以分支 / PR 检查后合并到 `main`。已经发布的站点会随同步分支更新，所以未完成正文留在草稿区。

GitBook 支持双向同步；若在 GitBook 修改内容，先拉取回写到仓库的提交再继续本地工作。

GitBook 回写会将图片保存到 `docs/.gitbook/assets/`，并可能把指向同一仓库源材料的 GitHub 链接转成相对路径。文档检查支持 `SLAM/` 中已有的公开源材料链接；图片仍须位于 `docs/`，草稿与实验不作为正文链接目标。

日常检查：`python3 scripts/check_docs.py`。修改检查脚本时，另运行 `python3 -m unittest discover -s scripts -p 'test_*.py'`，验证源材料链接、目录锚点、缺失目标和路径边界。

## 外观约定

简洁主题，蓝绿色强调色，正文保持适合长文的宽度；首页使用课程卡片和抽象几何封面。启用章节翻页与系统主题切换，搜索入口保持显眼。

基础站点优先使用免费可用的阅读功能。AI 问答、PDF 导出等功能取决于 GitBook 套餐，不作为第一版运行的前提。

## 验收记录（2026-10-04）

- [x] 仓库独立维护，公开正文均位于 `docs/`。
- [x] 20 页导航、相对路径和锚点通过检查。
- [x] 已通过 GitBook API 确认公开发布、中文、主题切换、搜索和章节翻页设置。
- [x] 在 GitBook 应用中落实首页布局开关（隐藏目录、页内大纲和首页翻页），并合并变更请求 #4；仓库首页 frontmatter 与正式内容的开关一致。
- [x] GitBook 编辑器阅读视图中检查：首页封面与卡片、卡片跳转、贝叶斯公式、表格、章节翻页、折叠答案和 Mermaid 流程图全屏查看。
- [ ] 公开页的桌面和手机检查，以及公开搜索和 Mermaid 验收。当前云浏览器打开公开域名及独立预览地址返回 `ERR_BLOCKED_BY_CLIENT`；应用内的站点预览返回 404，不能据此认定公开站点可正常访问。
- [x] GitHub → GitBook 自动同步：[PR #6](https://github.com/hyandnn/my-learning-notes/pull/6) 合并后的提交 `3ae60eacb61fd6ae69480b6da1f3214c5880a844` 与 GitBook 导入版本一致，20 篇正文完整，首页布局保留。
- [x] GitBook → GitHub 回写：变更请求 #6 补充贡献方式与更新记录，生成提交 `df1bd2d2d9e8ef5dad2c38d157e4eb4a1629aa8b`，正确更新 `main` 的 `docs/`。
- [x] 回写格式兼容性：文档检查覆盖源材料相对链接与目录 README 锚点；6 项回归测试和 20 页导航检查通过。

当前连接状态为 `active`，两个方向均返回 `success`。公开站点的视觉检查仍待完成；编辑器中的 Mermaid 全屏查看对较长标签有轻微裁切，行内图可正常阅读。

API 可验证内容与配置，但不能代替浏览器视觉验收。GitBook 插件授权与 GitBook GitHub App 的仓库同步授权是两个独立连接。
