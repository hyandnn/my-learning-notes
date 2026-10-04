---
title: Part IV · 建图与 SLAM
description: 从轨迹与地图的联合估计走到图优化、回环、惯性融合和现代 SLAM 系统设计。
icon: book-open
---

# Part IV · 建图与 SLAM

Chapter 37–48 已完成。承接 [Part III](../spatial/README.md) 的几何与定位基础，把地图也作为未知量，从 EKF-SLAM 的状态相关性走到稀疏优化与完整系统。

## 学习主线

联合状态 → 可观测性与基准 → 视觉前端与关键帧 → 非线性优化／BA → Factor Graph／Pose Graph → 回环 → 惯性融合 → 实时系统设计。

## 章节目录

| 章节 | 阅读主题 | 本章解决的问题 |
| --- | --- | --- |
| Chapter 37 | [SLAM 问题定义](slam-formulation.md) | 怎样把轨迹与地图写成相互依赖的联合估计问题？ |
| Chapter 38 | [Landmark SLAM 与 EKF-SLAM](ekf-slam.md) | 机器人和地图怎样通过联合协方差相互校正？ |
| Chapter 39 | [SLAM 可观测性与 Gauge Freedom](gauge-freedom.md) | 哪些方向没有绝对信息，为什么要选定坐标基准？ |
| Chapter 40 | [Visual SLAM 前端](visual-frontend.md) | 怎样把图像变成可靠的对应关系与几何约束？ |
| Chapter 41 | [关键帧与局部建图](keyframes-local-mapping.md) | 如何控制状态与地图规模，同时保留有效几何信息？ |
| Chapter 42 | [非线性最小二乘](nonlinear-least-squares.md) | 残差怎样变成 Gauss–Newton、LM 与稀疏线性系统？ |
| Chapter 43 | [Bundle Adjustment](bundle-adjustment.md) | 相机和地图如何联合优化，Schur Complement 怎样减少求解量？ |
| Chapter 44 | [Factor Graph](factor-graphs.md) | 如何用变量与因子统一表示多传感器估计、消元与边缘化？ |
| Chapter 45 | [Pose Graph Optimization](pose-graph.md) | 相对位姿约束怎样修正全局轨迹，并处理错误回环？ |
| Chapter 46 | [回环检测与全局校正](loop-closure.md) | 怎样验证“来过这里”，并把可靠回环用于地图校正？ |
| Chapter 47 | [视觉／激光惯性状态估计](visual-lidar-inertial.md) | IMU 怎样与 Camera、LiDAR 联合约束位姿、速度与 Bias？ |
| Chapter 48 | [现代 SLAM 流程与系统设计](modern-slam-pipeline.md) | 如何把状态估计模块组织成可持续运行的实时机器人系统？ |
| 阶段总结 | [Part IV 回顾与自测](summary.md) | 串联十二章，并完成八道综合自测。 |

## 阅读建议

先理解状态和信息从哪里来，再读矩阵求解。Chapter 42–44 是后端数学主线，Chapter 47 将可观测性、线性化与边缘化汇合；推导需连同假设、符号与修订说明阅读。后续方向见[课程计划](../study-plan.md)。
