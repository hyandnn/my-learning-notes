---
title: Bayes Filter
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 15
chapter_type: lecture
tags: [slam, bayes-filter, prediction, correction, markov]
status: organized
---

# Bayes Filter

## 本章目标

- 推导递归 Bayes Filter 的 Prediction 与 Correction
- 明确 Motion Model、Observation Model 和 Markov Assumption
- 理解 Bayes Filter 是框架而非单个算法

## 符号表

| 符号 | 含义 |
| --- | --- |
| $$x_t$$ | 时刻 $$t$$ 的隐藏状态 |
| $$u_t$$ | 从 $$t-1$$ 到 $$t$$ 的控制输入 |
| $$z_t$$ | 时刻 $$t$$ 的观测 |
| $$bel(x_t)$$ | 更新后的 Posterior |
| $$\overline{bel}(x_t)$$ | Observation 更新前的 Predicted Belief |

## 基本假设

一阶 Markov Assumption：给定 $$x_{t-1}$$ 与 $$u_t$$ 后，$$x_t$$ 与更早状态条件独立；给定 $$x_t$$ 后，$$z_t$$ 与其他变量条件独立。

## 公式推导

### 1. Prediction

从全概率公式出发：

$$
p(x_t\mid z_{1:t-1},u_{1:t})
=
\int p(x_t,x_{t-1}\mid z_{1:t-1},u_{1:t})\,dx_{t-1}
$$

使用乘法法则并应用 Markov Assumption：

$$
\begin{aligned}
\overline{bel}(x_t)
&=\int p(x_t\mid x_{t-1},u_t,z_{1:t-1})
p(x_{t-1}\mid z_{1:t-1},u_{1:t-1})\,dx_{t-1}\\
&=\int p(x_t\mid x_{t-1},u_t)bel(x_{t-1})\,dx_{t-1}
\end{aligned}
$$

Motion Model 将每个旧状态的概率质量传播到新状态并求和。

### 2. Correction

使用 Bayes Rule：

$$
bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})
=\eta\,p(z_t\mid x_t)\overline{bel}(x_t)
$$

其中 $$p(z_t\mid x_t)$$ 是 Likelihood，$$\eta$$ 是归一化常数：

$$
\eta^{-1}=\int p(z_t\mid x_t)\overline{bel}(x_t)\,dx_t
$$

### 推导得到什么

历史信息被压缩到上一时刻 Belief；每一步只需先通过 Motion Model 传播，再用当前 Likelihood 修正。

### 在 SLAM 中怎么用

Kalman、EKF、UKF、Histogram 和 Particle Filter 都是在不同假设与表示下实现这两步。

## 易混点

- Likelihood $$p(z\mid x)$$ 不是 Posterior $$p(x\mid z)$$。
- Prediction 不等于确定运动，它传播整个分布。
- $$\eta$$ 只负责归一化，不改变不同 State 的相对排序。

## 本章小结

$$
\boxed{
\overline{bel}(x_t)=\int p(x_t\mid x_{t-1},u_t)bel(x_{t-1})dx_{t-1}
}
$$

$$
\boxed{bel(x_t)=\eta p(z_t\mid x_t)\overline{bel}(x_t)}
$$

## 思考题

### 思考题 1

为什么 Bayes Filter 能递归运行而不保存全部历史？

<details>

<summary>参考答案</summary>

Markov Assumption 使上一时刻 Belief 成为历史信息对当前状态的充分递归摘要，因此更新只依赖上一 Belief、当前控制和当前观测。

</details>

## 下一章

[Week 2 Chapter 16：Kalman Filter](kalman-filter.md)
