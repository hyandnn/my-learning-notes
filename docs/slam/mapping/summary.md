---
title: Part IV 回顾与自测
description: 串联 Chapter 37–48 的联合状态、几何约束、优化与实时系统，并检验整体理解。
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter_type: summary
status: organized
---

# Part IV 回顾与自测

## Part IV 总回顾

现在把 Chapter 37–48 串起来。

### Chapter 37：SLAM 问题定义

[返回本章](slam-formulation.md)

我们第一次明确：

$$
\boxed{ State = Trajectory + Map }
$$

SLAM 是一个：

Joint Estimation 问题。 而不是简单“边走边画地图”。

### Chapter 38：Landmark SLAM 与 EKF-SLAM

[返回本章](ekf-slam.md)

我们看到：

$$
Robot
$$

和：

Landmark

为什么会产生：

Cross Covariance

并第一次真正理解：

Pose uncertainty ↔  Map uncertainty

### Chapter 39：SLAM 可观测性与 Gauge Freedom

[返回本章](gauge-freedom.md)

我们发现：

Measurement 并不能确定所有 State。

例如：

Global Translation Global Rotation

Monocular 还有：

$$
Scale
$$

所以要理解：

What can actually be estimated?

### Chapter 40：Visual SLAM 前端

[返回本章](visual-frontend.md)

我们从：

$$
Image
$$

得到：

Correspondence

再得到：

Geometric Constraint

核心：

$$
\boxed{ 2D\text{-}2D,\quad3D\text{-}2D,\quad3D\text{-}3D }
$$

以及：

Data Association 的重要性。

### Chapter 41：关键帧与局部建图

[返回本章](keyframes-local-mapping.md)

我们开始控制系统规模：

Not every frame deserves to live forever

Keyframe、Local Map、Covisibility、Local BA 都是在做：

Information Selection

### Chapter 42：非线性最小二乘

[返回本章](nonlinear-least-squares.md)

我们真正打开：

Residual →  Correction

通过：

$$
J
$$

$$
H=J^TJ
$$

$$
H\Delta x=-b
$$

以及：

$$
Gauss\text{-}Newton / LM
$$

理解 Backend 到底怎么算。

### Chapter 43：Bundle Adjustment

[返回本章](bundle-adjustment.md)

Visual SLAM 变成：

$$
\boxed{ Jointly\ optimize\ Camera\ Poses + Landmarks }
$$

我们还认识了：

Schur Complement

也就是：

删除大量 Landmark variables，但保留它们的信息

### Chapter 44：Factor Graph

[返回本章](factor-graphs.md)

所有东西统一成：

$$
\boxed{ Variables + Factors }
$$

Camera、IMU、GPS、Wheel、Loop 都只是不同：

Measurement Factors 从这里开始，多传感器系统有了统一语言。

### Chapter 45：Pose Graph Optimization

[返回本章](pose-graph.md)

我们把低层信息压缩成：

Pose-Pose Constraint

通过：

$$
Odometry\ Edge + Loop\ Edge
$$

解决：

Global Consistency

### Chapter 46：回环检测与全局校正

[返回本章](loop-closure.md)

我们终于搞清楚：

$$
\boxed{ Loop = Long-term Data Association }
$$

完整链：

Retrieval  →  Matching  →  Geometry  →  Loop Factor 而不是简单“图片长得像”。

### Chapter 47：视觉／激光惯性状态估计

[返回本章](visual-lidar-inertial.md)

State 扩展成：

$$
Pose + Velocity + Bias
$$

IMU：

Propagation

Camera / LiDAR：

Correction

并引入：

Preintegration Sliding Window Marginalization 把前面所有理论真正汇合。

### Chapter 48：现代 SLAM 流程与系统设计

[返回本章](modern-slam-pipeline.md)

最后我们看到：

真正的 SLAM 不是一个算法，而是一个多时间尺度的信息处理系统

## Part IV 最后一张总图

你现在可以把整个 SLAM 记成：

```
                ┌──────── IMU ────────┐
                │                     ↓
Sensors → Front-end → Tracking → Current State
                │              │
                │              ↓
                │          Keyframes
                │              ↓
                │        Local Mapping
                │              ↓
                │       Local Optimization
                │
                └──────────────┐
                               ↓
                       Persistent Map
                               ↓
                     Place Recognition
                               ↓
                       Loop Closure
                               ↓
                  Global Pose Optimization
                               ↓
                        Corrected Map
```

而这一切最底层都可以压成：

$$
\boxed{ State + Measurement + Association + Residual + Uncertainty + Optimization }
$$

## Part IV 最值得你带走的 10 个核心认知

1.  **SLAM 本质不是建图，而是联合状态估计与一致性维护。** 

2.  **机器人真正能知道多少，取决于 Measurement 对 State 提供了多少 Information。** 

3.  **不可观的问题不能靠“调参数”解决。** 

4.  **Front-end 的真正目标是产生可靠约束，而不是某个特定 Feature 算法。** 

5.  **Data Association 是 SLAM 从短期 Tracking 到长期 Loop 的共同核心问题。** 

6.  **Backend 的本质是 Nonlinear Least Squares。** 

7.  **Graph topology 决定了 Matrix sparsity，因此系统结构和计算复杂度直接相关。** 

8.  **Keyframe、Schur Complement、Marginalization、Pose Graph 本质都在解决“怎样压缩信息而不是粗暴丢信息”。** 

9.  **多传感器融合不是结果平均，而是让不同 Measurement 同时约束同一个 State。** 

10.  **一个真正可用的机器人 SLAM 系统必须同时考虑 Accuracy、Observability、Latency、Robustness、Recovery 和 Computational Budget。** 

## 思考题与参考答案

这次我给你几道更综合的问题，也直接附答案。

### Q1：为什么说 SLAM 最核心的资源不是“算力”，而是 Information？

**参考答案**

因为再强的 optimizer，如果当前 measurement 对某个方向完全没有信息：

$$
Jv=0
$$

也无法估出它。 算力只能更好地利用已有 information， 不能创造不存在的 observability。


### Q2：为什么 Keyframe、Marginalization 和 Schur Complement 看似完全不同，却可以放在同一个主题下？

**参考答案**

因为它们都在解决：

$$
\boxed{ State / Data 持续增长，但计算资源有限 }
$$

Keyframe：

> 不保留所有 frame。

Schur：

> 消掉 landmarks。

Marginalization：

> 移出旧 states。

共同目标都是：

减少表示规模，同时尽量保留有价值的信息


### Q3：为什么一个拥有非常强 Neural Front-end 的 SLAM，仍然可能因为几何问题失败？

**参考答案**

因为神经网络可以改善：

- matching
- depth
- feature

但如果系统本身：

- motion degenerate
- scale unobservable
- calibration wrong
- timestamp wrong
- long-term constraint absent

这些属于：

$$
State\ Estimation / Geometry
$$

问题。 网络并不会自动让这些物理约束消失。


### Q4：为什么机器人定位系统通常需要“快但不够准”和“慢但更准”的两个层次？

**参考答案**

因为实时控制需要：

Low latency

而高精度优化需要：

$$
More\ measurements + More\ computation
$$

所以：

$$
Fast\ Propagation / Tracking
$$

保证即时响应，

$$
Local / Global Optimization
$$

不断修正结果。 两者是不同需求。


### Q5：如果当前 Camera 突然完全失效 2 秒，VIO 为什么还能暂时工作，但不能长期依赖 IMU？

**参考答案**

因为 IMU 可以：

Propagate 短时间 motion。

但是：

$$
Bias + Noise
$$

会持续积分，

最终导致：

Orientation, Velocity, Position 快速 drift。 所以它是短期桥梁，不是永久替代 Camera。


### Q6：如果系统 Loop Closure 很强，是不是 Odometry 差一点也无所谓？

**参考答案**

不是。 Loop Closure 通常稀疏而偶发。 两次 Loop 之间仍然要靠 Odometry / Tracking。

而且如果 local odometry 太差：

- 地图可能已经变形严重
- candidate search 变难
- geometric verification 也可能失败

所以：

$$
\boxed{ Good\ local\ odometry + Good\ loop\ closure }
$$

缺一不可。


### Q7：为什么真正成熟的 State Estimator 必须有 Failure Detection？

<details>

<summary>参考答案</summary>

因为 estimator 不可能永远拥有足够 information。

如果已经：

Tracking Lost 却继续输出高置信 Pose， 下游会把错误状态当真。

所以真正可靠系统必须同时估计：

> 我在哪里？

以及：

> 我现在有多确定？

</details>

### Q8：如果以后你看到一个新的机器人定位算法，第一步应该看它网络 backbone 还是 State Definition？

**参考答案**

优先看：

State Definition

然后看：

$$
Measurement / Factor
$$

再看：

$$
Optimization / Update
$$

最后再看某个具体 neural backbone。

因为前面三项决定了：

> 它到底在解决什么状态估计问题。


## 下一阶段

Part IV Chapter 37–48 已完成。下一阶段进入 Part V Modern Robot Intelligence，可从动态与语义 SLAM、NeRF／3DGS 的场景表示开始，再学习 World Model 与 Embodied AI。VIO/LIO 基础已在 Chapter 47 完成，后续仅按需要深化。

## 相关笔记与来源

[Part IV 目录](README.md) · [现代 SLAM 系统设计](modern-slam-pipeline.md) · [课程计划](../study-plan.md)。本页由 Chapter 48 草稿中的阶段回顾、系统总图和八道综合自测整理。
