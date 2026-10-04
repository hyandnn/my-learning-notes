---
title: 位置与速度 Kalman Filter
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 17
chapter_type: derivation
tags: [slam, kalman-filter, motion-model, covariance, observability]
status: organized
---

# 位置与速度 Kalman Filter

## 本章目标

- 从运动学建立二维状态的线性模型
- 推导过程噪声协方差与协方差传播
- 理解位置观测如何间接修正速度

## 符号与模型

状态为一维空间中的位置和速度：

$$
\mathbf x_t=\begin{bmatrix}p_t\\v_t\end{bmatrix}
$$

采用采样间隔内恒定速度、未知加速度作为白噪声的模型：

$$
\mathbf x_t=\mathbf F\mathbf x_{t-1}+\mathbf G a_t
$$

$$
\mathbf F=\begin{bmatrix}1&\Delta t\\0&1\end{bmatrix},\qquad
\mathbf G=\begin{bmatrix}\frac12\Delta t^2\\\Delta t\end{bmatrix}
$$

若 $$a_t\sim\mathcal N(0,\sigma_a^2)$$，则：

$$
\mathbf Q=\mathbf G\sigma_a^2\mathbf G^\top
=\sigma_a^2
\begin{bmatrix}
\frac14\Delta t^4&\frac12\Delta t^3\\
\frac12\Delta t^3&\Delta t^2
\end{bmatrix}
$$

> **模型边界**
> 某些教材使用连续白噪声加速度模型，会得到不同 $$\Delta t$$ 次幂的 $$\mathbf Q$$。两种形式对应不同噪声假设，不能只比较矩阵外观。

## Prediction 推导

$$
\hat{\mathbf x}_t^-=\mathbf F\hat{\mathbf x}_{t-1}
$$

$$
\mathbf P_t^-=\mathbf F\mathbf P_{t-1}\mathbf F^\top+\mathbf Q
$$

令：

$$
\mathbf P=\begin{bmatrix}P_{pp}&P_{pv}\\P_{pv}&P_{vv}\end{bmatrix}
$$

忽略 $$\mathbf Q$$ 时展开得：

$$
\mathbf F\mathbf P\mathbf F^\top=
\begin{bmatrix}
P_{pp}+2\Delta tP_{pv}+\Delta t^2P_{vv}&P_{pv}+\Delta tP_{vv}\\
P_{pv}+\Delta tP_{vv}&P_{vv}
\end{bmatrix}
$$

即使初始 $$P_{pv}=0$$，只要 $$P_{vv}>0$$ 且 $$\Delta t>0$$，运动模型也会产生位置-速度交叉协方差。

## Correction 推导

若传感器只测位置：

$$
z_t=\mathbf H\mathbf x_t+v_t,qquad
\mathbf H=\begin{bmatrix}1&0\end{bmatrix},\quad v_t\sim\mathcal N(0,R)
$$

$$
\begin{aligned}
\nu_t&=z_t-\mathbf H\hat{\mathbf x}_t^-\\
S_t&=\mathbf H\mathbf P_t^-\mathbf H^\top+R=P_{pp}^-+R\\
\mathbf K_t&=\mathbf P_t^-\mathbf H^\top S_t^{-1}
=\frac1{P_{pp}^-+R}
\begin{bmatrix}P_{pp}^-\\P_{pv}^-\end{bmatrix}
\end{aligned}
$$

所以速度更新为：

$$
\hat v_t=\hat v_t^-+
\frac{P_{pv}^-}{P_{pp}^-+R}\nu_t
$$

### 推导得到什么

位置观测能够修正速度，不是因为 Sensor 直接测了速度，而是 Motion Model 在 Covariance 中建立了二者相关性。

### 在 SLAM 中怎么用

未被直接测量的 State 可以通过动力学和交叉协方差接受间接信息。这自然引出下一章的 Observability。

## 数值例子

取 $$\Delta t=1$$、$$\mathbf P_0=\operatorname{diag}(1,4)$$、暂忽略 $$\mathbf Q$$：

$$
\mathbf P_1^-=\begin{bmatrix}5&4\\4&4\end{bmatrix}
$$

若 $$R=1$$，则：

$$
\mathbf K=\frac16\begin{bmatrix}5\\4\end{bmatrix}
$$

位置 Innovation 因而同时更新位置和速度。

## 思考题

### 思考题 1

若 $$P_{pv}^-=0$$，一次位置观测能否修正速度？

<details>

<summary>参考答案</summary>

不能。速度对应的 Kalman Gain 分量为 $$P_{pv}^-/(P_{pp}^-+R)$$。不过后续 Prediction 可能通过 $$\mathbf F$$ 再次建立交叉协方差。

</details>

## 下一章

[Week 2 Chapter 18-19：Observability 与 Information Strength](observability.md)
