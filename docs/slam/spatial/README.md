---
title: Part III · 空间状态估计
description: Part III · 空间状态估计的核心问题、推导与自测。
icon: book-open
---

# Part III · 空间状态估计

Chapter 24–36 已整理完成：从坐标系与刚体变换，到位姿不确定性、运动和传感器模型，再到已知地图定位、数据关联与扫描匹配。最后通过阶段自测进入 Part IV 的 SLAM 问题。

## 章节目录

| 章节 | 阅读主题 | 本章解决的问题 |
| --- | --- | --- |
| Chapter 24 | [坐标系与坐标变换](coordinate-frames.md) | 坐标系与坐标变换的课程笔记。 |
| Chapter 25 | [二维旋转与 SO(2)](so2.md) | 二维旋转与 SO(2)的课程笔记。 |
| Chapter 26 | [二维位姿与 SE(2)](se2.md) | 二维位姿与 SE(2)的课程笔记。 |
| Chapter 27 | [三维旋转与 SO(3)](so3.md) | 三维旋转与 SO(3)的课程笔记。 |
| Chapter 28 | [四元数](quaternions.md) | 四元数的课程笔记。 |
| Chapter 29 | [三维位姿与 SE(3)](se3.md) | 三维位姿与 SE(3)的课程笔记。 |
| Chapter 30 | [坐标系约定与变换调试](transform-debugging.md) | 坐标系约定与变换调试的课程笔记。 |
| Chapter 31 | [SE(3) 上的位姿不确定性](pose-uncertainty.md) | 位姿协方差应定义在哪里，怎样随扰动约定与坐标系传播？ |
| Chapter 32 | [机器人运动模型](robot-motion-models.md) | 如何把轮速与编码器读数变成带不确定性的位姿预测？ |
| Chapter 33 | [传感器观测模型](sensor-models.md) | 如何从状态与地图预测传感器观测，并构造残差？ |
| Chapter 34 | [已知地图中的定位](localization.md) | 如何融合运动与观测，在已知地图中维护位姿 Belief？ |
| Chapter 35 | [数据关联](data-association.md) | 如何判断当前观测对应哪个地图对象，并处理错误匹配？ |
| Chapter 36 | [扫描匹配与 ICP](scan-matching-icp.md) | 如何在 SE(3) 上对齐点云，并识别局部收敛与几何退化？ |
| 阶段总结 | [Part III 回顾与自测](summary.md) | 串联 Chapter 24–36，检查几何、概率与定位的联系。 |

> 已有内容已迁移；保留课程推导、例题与思考题；新增章节包含必要的技术修订说明。迁移和排版检查不等同于全面技术审校。
