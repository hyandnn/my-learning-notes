# 维护学习笔记

正文只维护在 `docs/`，GitBook 自动读取 `main`。不要另建一份课程源目录或手工复制到 GitBook。

## 学完新的一课

1. 先拉取最新版本：`git pull --ff-only`，再创建分支，例如 `git switch -c notes/chapter-31`。
2. 学习时记录核心问题、自己的解释、推导、例子、疑问和自测答案。未整理的对话或笔记放在 `drafts/`；公开仓库里的草稿也会被别人看到，内部资料留在私有知识库。
3. 复制 `templates/chapter.md`，整理成一篇能独立复习的章节。保留有用的问答与推理，删去寒暄和重复内容；不确定的结论标记待核验。
4. 整理完成后移入对应目录，例如 `docs/slam/spatial/camera-observation.md`。文件名用稳定的英文主题名，章节编号保存在 frontmatter 中；图片放 `docs/assets/` 或 GitBook 的资源目录。
5. 在 `docs/SUMMARY.md` 添加入口，并更新所在 Part 的 `README.md`、`docs/slam/study-plan.md` 和 `docs/roadmap.md`。重大新增或技术修订记入 `docs/changelog.md`。
6. 运行 `python3 scripts/check_docs.py`。提交、推送分支并创建 PR；确认 `Docs check` 通过，再合入 `main`。通常用 squash 保留一条说明主题的提交。
7. 等待 GitBook 自动更新；刷新新章节，确认目录、公式、图片和问答正确。无需每次手动 Git Sync。检查成功仅说明仓库结构有效，最终仍应看网站实际内容。
8. 删除已经迁入正文的草稿，避免长期维护两份同样内容。实验代码放 `experiments/`，私有库只提炼概念卡与工程经验，并链接完整课程。

## 修改已有内容

直接编辑 `docs/` 对应文件。技术修订说明原问题、新结论与依据，存疑内容标记待核验。排版调整不必逐项写更新记录。

## 检查与同步

文档检查核对目录、相对路径、锚点、重复条目与残留双链，不核验数学正确性或实际视觉效果。修改检查工具后运行：

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```

GitBook 可双向编辑。若在 GitBook 修改，先合并其变更请求，确认回写 `main`，再拉取最新版本继续本地工作，避免同时修改同一章节。

写作要求见 [.regulation/LearningNoteRules.md](.regulation/LearningNoteRules.md)，发布配置见 [GITBOOK_SETUP.md](GITBOOK_SETUP.md)。
