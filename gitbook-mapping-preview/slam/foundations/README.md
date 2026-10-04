---
description: 建立机器人系统、状态、Belief、模型和信息融合的共同语言。
icon: book-open
---

# Part I · 机器人基础

这部分从“机器人怎样处理信息”出发，逐步走到预测与校正。目标是理解滤波器出现之前的问题结构。

## 章节目录

| 章节          | 阅读主题                                         | 本章解决的问题                     |
| ----------- | -------------------------------------------- | --------------------------- |
| Chapter 1   | [机器人系统的信息流](robot-systems.md)                | 传感器、感知、定位、规划与控制怎样共同形成闭环。    |
| Chapter 2   | [里程计与定位漂移](odometry-and-drift.md)            | 为什么运动估计会累积误差，环境观测怎样帮助修正。    |
| Chapter 3   | [观测、真实世界与 Belief](observation-and-belief.md) | 区分测量、解释与估计，理解信息融合的起点。       |
| Chapter 4   | [用分布表达位置](belief-over-pose.md)               | 为什么单个位置估计无法表达歧义和不确定性。       |
| Chapter 5   | [贝叶斯更新的直觉](bayesian-thinking.md)             | 先验、似然与后验怎样把新证据接入已有认识。       |
| Chapter 5.5 | [状态与时间连续性](state-and-time.md)                | 状态设计、预测与 Markov 假设之间的关系。    |
| Chapter 6   | [从状态到模型](modeling.md)                        | 用运动模型与观测模型描述可预测、可修正的系统。     |
| Chapter 7   | [预测与校正的循环](prediction-and-correction.md)     | 从问题出发建立递归状态估计的基本结构。         |
| Chapter 8   | [Kalman Gain 的直觉](kalman-gain-intuition.md)  | 怎样按不确定性分配预测和观测的融合权重。        |
| 阶段总结        | [Part I 回顾与自测](summary.md)                   | 把系统、状态、模型、Belief 和融合串成一条主线。 |

## 三个阶段

* Chapter 1–2：认识系统信息流与运动估计的误差。
* Chapter 3–5：区分观测与估计，理解 Belief 和贝叶斯更新。
* Chapter 5.5–8：引入状态、时间和模型，建立预测校正与融合直觉。

## 学完之后

你应当能够为一个简单跟踪或定位问题列出状态、观测与模型，解释为什么需要不确定性，并说明什么时候应更相信预测、什么时候应更相信观测。

本部分保留学习过程中的问答与反例。数学推导逐步在后续概率状态估计部分展开；[贝叶斯更新例题](../../reference/bayes-worked-example.md)提供一个可以独立复算的起点。
