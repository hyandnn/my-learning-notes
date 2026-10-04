# 维护学习笔记

## 新增一章

1. 从 `templates/chapter.md` 创建草稿，写清目标和前置知识。
2. 按内容需要补充定义、假设、推导、例子、问答与自测。
3. 确认正文能独立阅读后，将它移入 `docs/` 的对应主题目录。
4. 在 `docs/SUMMARY.md` 加入目录，更新主题概览与前后章节链接。
5. 使用 Python 3.10 或更新版本运行 `python3 scripts/check_docs.py`，再检查 GitBook 预览。PR 的 `Docs check / Navigation and links` 会自动运行同一检查。
6. 合并到 `main`，在更新记录中注明影响阅读或结论的变化。

## 修改现有章节

直接修改 `docs/` 下对应文件。Part I 原目录已迁移，不要在旧路径重新维护正文。现有 Part II / III 仍从 `SLAM/` 编辑，进入网站时再逐章迁移。

技术修正说明原问题与新结论；不能确认时标记待核验。排版修正不必逐项记入公开更新记录。

## 反馈问题

读者可在仓库的 [Issues](https://github.com/hyandnn/my-learning-notes/issues/new/choose) 中选择“内容纠错或阅读问题”，提供具体页面、问题和可复算的依据。

## 检查范围

检查工具核对目录引用、相对路径、锚点、重复目录条目与残留 Obsidian 双链。它不核验公式的数学正确性，也不代替网站的视觉检查。

允许链接到 `SLAM/` 中已有的公开源材料，图片需保存在 `docs/`。GitBook 回写可能将源材料链接改成仓库相对路径，保持该格式即可；不要把草稿或实验目录直接加入正文链接。

修改检查工具时，运行 `python3 -m unittest discover -s scripts -p 'test_*.py'`。如果通过 GitBook 编辑，先合并变更请求并确认回写到 `main`，再拉取最新提交继续修改。

GitBook 外观设置在站点中维护；正文以仓库为主。持续同步首次连接步骤见 [GITBOOK_SETUP.md](GITBOOK_SETUP.md)。
