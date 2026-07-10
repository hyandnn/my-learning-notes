# SLAM 自学

同时定位与建图（SLAM）学习笔记入口。草稿与课程材料可直接放本目录；课程笔记整理规范见 [[.regulation/LearningNoteRules|LearningNoteRules]]。

## 课程

### Part I：Robot Foundations

| 笔记 | 说明 |
| --- | --- |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 1|Week 1 Chapter 1：机器人到底是什么？]] | 建立机器人软件信息流：Sensor、Perception、Localization & Mapping、Planning、Control |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 2|Week 1 Chapter 2：为什么机器人会迷路？]] | 从 Encoder 和 Odometry 误差引出 Localization |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 3|Week 1 Chapter 3：如果机器人不能相信任何一个传感器，它到底应该相信谁？]] | 区分 Observation、Reality、Belief，进入 Information Fusion |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 4|Week 1 Chapter 4：为什么机器人维护的是一个概率分布，而不是一个位置？]] | 理解 Belief over Pose，而不是单点 Pose |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 5|Week 1 Chapter 5：贝叶斯思想到底是什么？]] | 用 Prior、Observation、Posterior 理解 Belief Update |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 5.5|Week 1 Chapter 5.5：为什么机器人能够利用时间？]] | 新增章节：引入 State、Prediction、Temporal Consistency、Markov Assumption |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 6|Week 1 Chapter 6：为什么机器人学本质上是一门建模的学科？]] | 理解 Model、State Design、Prediction / Correction |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 7|Week 1 Chapter 7：如果世界上还没有 Kalman Filter，你会怎么设计一个机器人？]] | 从世界规律、Observation、Model 推导状态估计循环 |
| [[Courses/Part I Robot Foundations/Week 1 Chapter 8|Week 1 Chapter 8：如果世界上没有 Kalman Filter，我们能不能自己推导出来？]] | 从不确定性和信息增益理解 Kalman Gain |
| [[Courses/Part I Robot Foundations/Week 1 Summary|Week 1 Summary：课程总结与 Week 2 调整]] | 总结 Week 1 实际学习轨迹，并更新 Week 2 方向 |

## 阅读顺序

```mermaid
flowchart TD
    C1[Chapter 1<br/>机器人系统信息流]
    C2[Chapter 2<br/>为什么会迷路]
    C3[Chapter 3<br/>Observation 与 Belief]
    C4[Chapter 4<br/>Belief over Pose]
    C5[Chapter 5<br/>Bayesian Thinking]
    C55[Chapter 5.5<br/>时间连续性与 State]
    C6[Chapter 6<br/>Modeling]
    C7[Chapter 7<br/>状态估计循环]
    C8[Chapter 8<br/>Kalman Gain 直觉]
    S[Week 1 Summary]

    C1 --> C2 --> C3 --> C4 --> C5 --> C55 --> C6 --> C7 --> C8 --> S
```

## Week 1 实际主线

Week 1 实际内容已经超过最初“机器人基础”的范围，形成了下面这条主线：

```text
Robot System
  -> Odometry Error
  -> Observation
  -> Belief
  -> Bayesian Update
  -> State
  -> Model
  -> Prediction / Correction
  -> Kalman Gain
```

下一阶段建议进入 `Probabilistic State Estimation`，优先补齐 Information、Probability、Uncertainty、Gaussian，再回到 Bayes Filter 和 Kalman Filter。

## 相关

- 可后续沉淀概念：Coordinate Frame、Occupancy Grid、ICP、Kalman Filter、Bayes Filter
- 与工程侧可对照主题：Lidar 感知、Ground Detection、Mapping、Tracking
