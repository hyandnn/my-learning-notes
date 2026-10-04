# Robotics Learning Notes

机器人感知与 SLAM 的个人学习笔记。先理解问题，再建立模型、推导和实验。

## 阅读入口

[在线阅读 · Robotics Notes](https://roborock-1.gitbook.io/merci-robotics-notes/)

- [网站首页源文件](docs/README.md)
- [Part I · 机器人基础](docs/slam/foundations/README.md)
- [Part II · 概率状态估计](docs/slam/probabilistic/README.md)
- [Part III · 空间状态估计](docs/slam/spatial/README.md)
- [术语表](docs/reference/glossary.md)与[贝叶斯更新例题](docs/reference/bayes-worked-example.md)
- [学习路线与进度](docs/roadmap.md)

## 仓库结构

| 路径 | 用途 |
| --- | --- |
| `docs/` | 网站内容的唯一正文来源，首页与导航也在这里维护 |
| `drafts/` | 新增草稿与待整理内容 |
| `experiments/` | 与章节对应的实验代码、Notebook 与结果 |
| `.regulation/` | 公开内容与发布规则 |
| `templates/` | 新章节模板 |
| `scripts/` | 文档检查工具 |

GitBook 映射 `docs/`，目录由 `docs/SUMMARY.md` 控制。仓库独立维护，通过外部链接与私有知识库关联。

## 编辑与维护

日常流程：草稿 → 整理正文 → 分支 / PR → 文档检查与 GitBook 预览 → 合并 `main`。

```bash
python3 scripts/check_docs.py
```

具体步骤见 [CONTRIBUTING.md](CONTRIBUTING.md)、[发布规则](.regulation/Publishing.md)和 [GitBook 接入说明](GITBOOK_SETUP.md)。

已有非空内容已全部迁入 `docs/`：Part I、Part II、Part III Chapter 24–30、状态思维与课程计划。旧源目录与空占位文件已移除。
