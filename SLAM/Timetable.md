
> # Robot Perception & SLAM —— 从原理到工程（A Systematic Course）

以后这个课程不仅可以学 SLAM，还可以自然扩展到：
- Robot Perception
- State Estimation
- Motion Planning
- Navigation
- Multi-Sensor Fusion
- 3D Reconstruction
- Robotics AI

最终形成你自己的机器人知识体系。

---

## 整体规划

**初步：20 周（约 5 个月）**

每天：

> **30~60 分钟**

每周：

- 5 天学习
    
- 1 天复习
    
- 1 天自由阅读（论文/视频/答疑）
    

为什么这么慢？

因为我们的目标不是：

> 会用 Cartographer

而是：

> 五年以后看到任何 SLAM 论文，都知道它属于整个知识树的哪一个位置。

---

# 整体知识树

```text
Robot Perception & SLAM

Part I
机器人如何描述世界（Week1-4）

↓

Part II
机器人如何估计自身（Week5-8）

↓

Part III
机器人如何建图（Week9-12）

↓

Part IV
完整SLAM系统（Week13-16）

↓

Part V
现代SLAM与前沿（Week17-20）
```

---

# 第一部分

# Robot Foundations

---

# Week 1

## 机器人为什么需要SLAM？

### 目标

建立整个机器人感知体系。

这一周几乎不讲算法。

而是回答：

机器人到底有哪些能力？

```text
Perception

Localization

Mapping

Planning

Control
```

这些模块之间是什么关系？

---

### 学习内容

#### Chapter 1

什么是机器人？

机器人软件整体架构

机器人信息流

机器人是如何感知世界的

---

#### Chapter 2

什么是 Localization

为什么机器人不知道自己在哪

为什么会迷路

---

#### Chapter 3

什么是 Mapping

地图到底是什么

为什么需要地图

---

#### Chapter 4

Localization 与 Mapping 为什么必须一起做

SLAM 的诞生

经典SLAM发展历史

---

### 推荐资料

阅读：

Probabilistic Robotics

Chapter 1（只读概念）

---

视频：

一门机器人导论（不用太深）

---

### 本周训练

不用写代码。

能够画出来：

```text
Sensor

↓

Perception

↓

Localization

↓

Mapping

↓

Planning

↓

Control
```

整个机器人软件框架。

---

# Week 2

## 坐标系（Coordinate Frames）

这一周非常重要。

以后所有SLAM都会用。

学习：

二维坐标

三维坐标

机器人坐标

世界坐标

传感器坐标

TF Tree

坐标变换

为什么坐标系这么重要

最后能够手推：

二维旋转

二维刚体变换

---

训练：

画各种坐标系。

推导二维变换。

不用任何代码。

---

# Week 3

## 机器人如何表示运动

学习：

Pose

Trajectory

Velocity

Angular Velocity

里程计

Dead Reckoning

误差来源

为什么积分一定漂

---

训练：

自己模拟机器人走一圈。

分析为什么误差越来越大。

---

# Week 4

## 数学准备

这一周补数学。

不会太深。

主要包括：

矩阵

旋转矩阵

欧拉角

四元数

SO(2)

SE(2)

为什么需要这些表示。

注意：

SO(3)先不深入。

建立概念即可。

---

# 第二部分

# State Estimation

---

# Week 5

概率机器人

为什么机器人看到的是概率。

贝叶斯思想。

---

# Week 6

经典滤波器

Bayes Filter

Kalman Filter

EKF

UKF

Particle Filter

它们之间关系。

---

# Week 7

机器人状态估计

Sensor Fusion

IMU

Encoder

Camera

LiDAR

---

# Week 8

误差传播

协方差

不确定性

状态空间

为什么SLAM离不开优化。

---

# 第三部分

# Mapping

---

# Week 9

地图表示

Occupancy Grid

Feature Map

Point Cloud

Semantic Map

Octomap

TSDF

为什么有这么多地图。

---

# Week 10

Scan Matching

ICP

Point-to-Plane

NDT

为什么能够配准。

---

# Week 11

Visual Front-end

Feature

Descriptor

ORB

FAST

Optical Flow

Direct Method

---

# Week 12

Visual Odometry

LiDAR Odometry

Front-end总结

---

# 第四部分

# Complete SLAM

---

# Week 13

Graph SLAM

Pose Graph

Factor Graph

为什么图优化。

---

# Week 14

Least Squares

Gauss Newton

Levenberg

Ceres

g2o

---

# Week 15

Loop Closure

Place Recognition

为什么地图能拉直。

---

# Week 16

完整SLAM系统拆解

GMapping

Cartographer

ORB-SLAM

LIO-SAM

各模块职责。

---

# 第五部分

# Modern Robotics

---

# Week 17

Dense Mapping

Sparse Mapping

3D Reconstruction

---

# Week 18

Visual-Inertial SLAM

Multi-Sensor Fusion

---

# Week 19

Semantic SLAM

Dynamic SLAM

NeRF

Gaussian Splatting

机器人中的AI

---

# Week 20

知识体系总结

能够自己画出：

```text
Robot

↓

Sensor

↓

State Estimation

↓

Front-end

↓

Back-end

↓

Optimization

↓

Loop Closure

↓

Mapping

↓

Navigation
```

完整知识树。

---

# 每周固定模板（我们都会这样进行）

以后每一周都采用统一的节奏：

|星期|内容|
|---|---|
|周一|我讲本周知识框架（为什么学、整体位置）|
|周二|深入第一个核心知识点，建立直觉和原理|
|周三|深入第二个核心知识点，配合经典论文或案例|
|周四|将知识与真实机器人系统（如扫地机、无人机等）联系起来，理解工程意义|
|周五|本周总结，完成知识树与思维导图|
|周六|推荐阅读（教材、论文、课程、视频），你自主学习|
|周日|我负责答疑、查漏补缺，并通过问题检查是否真正掌握|

---

## 额外增加两个内容

这可能是最有价值、也是很多课程没有的。

### ① Robot Encyclopedia（机器人百科）

以后每遇到一个概念，例如：

- ICP
    
- Occupancy Grid
    
- EKF
    
- Pose Graph
    
- Bundle Adjustment
    

我们都会给它建立一张统一格式的知识卡片：

```markdown
# ICP

## 为什么会出现？

## 它解决什么问题？

## 输入

## 输出

## 数学本质

## 优点

## 缺点

## 后续演化

## 在哪些SLAM里使用？

## 面试常问什么？

## 推荐论文
```

20 周结束后，你会拥有一本完全属于自己的 **Robot Encyclopedia**。

---

### ② Robot Timeline（机器人技术演化时间线）

我们还会不断回答一个问题：

> **"为什么会出现这个算法？它解决了上一代方法的什么问题？"**

例如：

```text
Odometry
    ↓
Kalman Filter
    ↓
Particle Filter
    ↓
EKF-SLAM
    ↓
FastSLAM
    ↓
Graph SLAM
    ↓
Visual SLAM
    ↓
ORB-SLAM
    ↓
VIO
    ↓
LIO
    ↓
Semantic SLAM
```

这样你学到的不只是知识点，而是整个领域的发展脉络。