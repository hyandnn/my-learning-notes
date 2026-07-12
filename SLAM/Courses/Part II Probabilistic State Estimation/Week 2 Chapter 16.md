---
title: Week 2 Chapter 16：Kalman Filter 的一维推导
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 16
chapter_type: derivation
tags: [slam, kalman-filter, gaussian, kalman-gain, innovation]
status: organized
---

# Week 2 Chapter 16：Kalman Filter 的一维推导

## 本章目标

- 从两个 Gaussian 相乘推导更新公式
- 理解 Kalman Gain、Innovation 和 Posterior Variance
- 给出完整的一维递归流程

## 基本假设

线性模型、Gaussian Belief、零均值且相互独立的过程噪声与观测噪声。

## 公式推导

Prediction 与 Measurement 分别为：

$$
x\sim\mathcal N(\mu^-,P^-),\qquad z=x+v,\quad v\sim\mathcal N(0,R)
$$

由 Bayes Rule：

$$
p(x\mid z)\propto
\exp\left[-\frac{(x-\mu^-)^2}{2P^-}
-\frac{(z-x)^2}{2R}\right]
$$

展开所有含 $x$ 的项：

$$
-2\log p(x\mid z)
=x^2\left(\frac1{P^-}+\frac1R\right)
-2x\left(\frac{\mu^-}{P^-}+\frac zR\right)+C
$$

与 Gaussian 标准形式配方，可得：

$$
P=\left(\frac1{P^-}+\frac1R\right)^{-1}
=\frac{P^-R}{P^-+R}
$$

$$
\mu=P\left(\frac{\mu^-}{P^-}+\frac zR\right)
=\frac{R\mu^-+P^-z}{P^-+R}
$$

定义 Kalman Gain：

$$
K=\frac{P^-}{P^-+R}
$$

则：

$$
\mu=\mu^-+K(z-\mu^-),\qquad P=(1-K)P^-
$$

### 推导得到什么

Posterior Mean 是 Prediction 与 Measurement 按相对不确定性加权后的结果；Posterior Information 是两者 Information 的和。

### 在 SLAM 中怎么用

$z-\mu^-$ 是一维 Innovation。$P^-$ 大或 $R$ 小时 $K$ 较大，系统更多相信 Observation；反之更多保留 Prediction。

## 加入时间递归

对一维线性系统：

$$
x_t=Fx_{t-1}+Bu_t+w_t,\quad w_t\sim\mathcal N(0,Q)
$$

$$
z_t=Hx_t+v_t,\quad v_t\sim\mathcal N(0,R)
$$

完整流程为：

$$
\begin{aligned}
\mu_t^- &= F\mu_{t-1}+Bu_t\\
P_t^- &= F^2P_{t-1}+Q\\
\nu_t &= z_t-H\mu_t^-\\
S_t &= H^2P_t^-+R\\
K_t &= \frac{P_t^-H}{S_t}\\
\mu_t &= \mu_t^-+K_t\nu_t\\
P_t &= (1-K_tH)P_t^-
\end{aligned}
$$

## 易混点

- Innovation 小不等于 Estimate 准，只表示观测与预测接近。
- $Q$ 表示 Process Model 的不确定性，$R$ 表示 Measurement 的不确定性。
- 若 $P^-$ 与 $R$ 都很大，Innovation 即使不大也不代表系统可靠。

## 本章小结

> [!tip] 导师提示
> Kalman Gain 不是手工调出来的融合权重，而是在线性 Gaussian 假设下由相对不确定性推导出的权重。

## 思考题

### 思考题 1

$P^-=9$、$R=1$ 时，$K$ 是多少？如何解释？

> [!answer]- 参考答案
> $K=9/(9+1)=0.9$。Prediction 比 Measurement 更不确定，因此更新会吸收 90% 的 Innovation。

## 下一章

[[Week 2 Chapter 17|Week 2 Chapter 17：位置-速度 Kalman Filter]]

