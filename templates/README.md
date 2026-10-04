# 章节格式与 GitBook 展示规则

新课从 [chapter.md](chapter.md) 创建；只保留确实有内容的小节，不为了形式补空标题。

| 项目 | 统一约定 |
| --- | --- |
| 目录图标 | Part 概览、课程与总结在 frontmatter 中设置 `icon: book-open` |
| 页面标题 | `title` 与正文唯一的一级标题一致；导航使用具体主题名称 |
| 简介 | `description` 用一句话说明本章解决的问题 |
| 章节信息 | `course`、`part`、`week`、`chapter`、`chapter_type`、`status` 放在 frontmatter |
| 正文层级 | 页面标题用 H1，主要章节用 H2，解释与例子用 H3，避免重复顶级标题 |
| 内容结构 | 目标／前置知识 → 核心问题 → 定义与假设 → 推导 → 例子与边界 → 自测 → 小结与来源；按需要选用 |
| 公式 | GitBook 行内与独立公式均用 `$$...$$`；独立公式前后空行，矩阵用标准 LaTeX |
| 答案 | 纯文字答案用 `<details>` 配 `<summary>参考答案</summary>`；含公式答案直接用正文“参考答案”，避免 GitBook 导入时丢失折叠块内公式，保留推理与适用条件 |
| Part 概览 | 使用“章节／阅读主题／本章解决的问题”三列目录 |
| 维护记录 | 排版或技术修订放在文末，不挤占页面开头 |

三个 Part 的内容类型不同：Part I 偏直觉、Part II 偏概率推导、Part III 偏空间几何，因此不用把每篇文章强制改成同一组小节。统一元数据、导航、标题层级和公式／问答格式即可。

## 发布步骤

将成熟正文放入 `docs/`，更新 `docs/SUMMARY.md` 与所在 Part 的概览。运行 `python3 scripts/check_docs.py` 后提交 PR；合入 `main` 后 GitBook 自动更新。详细流程见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
