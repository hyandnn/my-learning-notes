---
title: Extended Kalman Filter
description: Extended Kalman Filter的核心问题、推导与自测。
icon: book-open
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 21
chapter_type: derivation
status: organized
tags: [slam, ekf, nonlinear-filter, jacobian, linearization]
---


# Extended Kalman Filter

## 本章目标

- 将局部线性化装入 Kalman Filter
- 推导 EKF Prediction 与 Correction
- 理解 EKF 的一致性和发散风险

## 基本模型

$$
\mathbf x_t=f(\mathbf x_{t-1},\mathbf u_t)+\mathbf w_t,
\qquad \mathbf w_t\sim\mathcal N(\mathbf0,\mathbf Q_t)
$$

$$
\mathbf z_t=h(\mathbf x_t)+\mathbf v_t,
\qquad \mathbf v_t\sim\mathcal N(\mathbf0,\mathbf R_t)
$$

EKF 仍用单个 Gaussian 近似 Belief，只是用 Jacobian 局部传播 Covariance。

## Prediction

$$
\hat{\mathbf x}_{t|t-1}=f(\hat{\mathbf x}_{t-1|t-1},\mathbf u_t)
$$

$$
\mathbf F_t=\left.\frac{\partial f}{\partial\mathbf x}\right|_{\hat{\mathbf x}_{t-1|t-1},\mathbf u_t}
$$

$$
\mathbf P_{t|t-1}=\mathbf F_t\mathbf P_{t-1|t-1}\mathbf F_t^\top+\mathbf Q_t
$$

若控制噪声 $$\mathbf n_t$$ 通过 $$f(\mathbf x,\mathbf u,\mathbf n)$$ 进入，还需：

$$
\mathbf P_{t|t-1}=\mathbf F_t\mathbf P\mathbf F_t^\top
+\mathbf L_t\mathbf M_t\mathbf L_t^\top
$$

## Correction

$$
\begin{aligned}
\hat{\mathbf z}_t&=h(\hat{\mathbf x}_{t|t-1})\\
\mathbf H_t&=\left.\frac{\partial h}{\partial\mathbf x}\right|_{\hat{\mathbf x}_{t|t-1}}\\
\boldsymbol\nu_t&=\mathbf z_t-\hat{\mathbf z}_t\\
\mathbf S_t&=\mathbf H_t\mathbf P_{t|t-1}\mathbf H_t^\top+\mathbf R_t\\
\mathbf K_t&=\mathbf P_{t|t-1}\mathbf H_t^\top\mathbf S_t^{-1}\\
\hat{\mathbf x}_{t|t}&=\hat{\mathbf x}_{t|t-1}+\mathbf K_t\boldsymbol\nu_t
\end{aligned}
$$

数值实现优先使用 Joseph Form：

$$
\mathbf P_{t|t}=(\mathbf I-\mathbf K_t\mathbf H_t)
\mathbf P_{t|t-1}(\mathbf I-\mathbf K_t\mathbf H_t)^\top
+\mathbf K_t\mathbf R_t\mathbf K_t^\top
$$

## 为什么会发散

- 当前估计偏离 Truth，Jacobian 在线性化错的位置计算。
- 一阶近似低估非线性造成的分布畸变。
- 角度 Innovation 未归一化。
- 错误数据关联或 $$Q/R$$ 失配造成过度自信。
- 单 Gaussian 无法表达多峰 Belief。

> **导师提示**
> EKF 的脆弱点不是“不会求导”，而是它用当前 Mean 决定怎样近似世界，并让这个近似继续影响下一次 Mean。

## 适用范围

EKF 适合初值较好、非线性在局部温和、维度可控且实时性重要的系统。EKF-SLAM 经典但联合 Covariance 随 Landmark 数量平方增长，扩展性有限。

## 思考题

### 思考题 1

为什么角度 Innovation 需要归一化？

<details>

<summary>参考答案</summary>

$$179^\circ$$ 与 $$-179^\circ$$ 实际只差 $$2^\circ$$。直接相减会得到接近 $$358^\circ$$ 的错误 Innovation，使线性更新失效。

</details>

## 下一章

[Week 2 Chapter 22：Unscented Kalman Filter](ukf.md)
