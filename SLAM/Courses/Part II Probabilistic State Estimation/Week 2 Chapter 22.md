---
title: Week 2 Chapter 22：Unscented Kalman Filter
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 22
chapter_type: lecture
tags: [slam, ukf, sigma-points, unscented-transform, nonlinear-filter]
status: organized
---

# Week 2 Chapter 22：Unscented Kalman Filter

## 本章目标

- 理解 Unscented Transform
- 比较 EKF、UKF 与 Particle Filter
- 认识 Sigma Points 的参数和边界

## 核心思想

EKF 近似非线性函数；UKF 选取一组确定性的 Sigma Points，通过真实非线性函数传播，再重建 Mean 与 Covariance。

对 $n$ 维 Gaussian $\mathcal N(\boldsymbol\mu,\mathbf P)$：

$$
\lambda=\alpha^2(n+\kappa)-n
$$

$$
\begin{aligned}
\boldsymbol\chi_0&=\boldsymbol\mu\\
\boldsymbol\chi_i&=\boldsymbol\mu+[\sqrt{(n+\lambda)\mathbf P}]_i\\
\boldsymbol\chi_{i+n}&=\boldsymbol\mu-[\sqrt{(n+\lambda)\mathbf P}]_i
\end{aligned}
$$

传播：

$$
\mathbf y_i=f(\boldsymbol\chi_i)
$$

重建：

$$
\bar{\mathbf y}=\sum_{i=0}^{2n}W_i^{(m)}\mathbf y_i
$$

$$
\mathbf P_y=\sum_{i=0}^{2n}W_i^{(c)}
(\mathbf y_i-\bar{\mathbf y})(\mathbf y_i-\bar{\mathbf y})^\top
$$

标准权重为：

$$
W_0^{(m)}=\frac{\lambda}{n+\lambda},\quad
W_0^{(c)}=\frac{\lambda}{n+\lambda}+1-\alpha^2+\beta
$$

$$
W_i^{(m)}=W_i^{(c)}=\frac1{2(n+\lambda)},\quad i=1,\ldots,2n
$$

常见 Gaussian 先验取 $\beta=2$；$\alpha,\kappa$ 控制点的散布，但没有适用于所有问题的固定最优值。

## Filter 更新

Prediction 将状态 Sigma Points 通过 Motion Model，加入过程噪声后重建 $\hat{\mathbf x}^-$、$\mathbf P^-$。Correction 再将预测 Sigma Points 通过 Observation Model，计算 $\hat{\mathbf z}$、$\mathbf S$ 和交叉协方差：

$$
\mathbf P_{xz}=\sum_iW_i^{(c)}
(\boldsymbol\chi_i^- -\hat{\mathbf x}^-)
(\boldsymbol\zeta_i-\hat{\mathbf z})^\top
$$

$$
\mathbf K=\mathbf P_{xz}\mathbf S^{-1}
$$

## 方法边界

- UKF 仍用一个 Gaussian，不能表达真正多峰 Belief。
- 维度为 $n$ 时通常使用 $2n+1$ 个点，计算代价高于 EKF。
- 角度和流形状态需要专门的 Mean 与差分定义。
- Sigma Point 传播不会消除错误模型、Outlier 或数据关联问题。

| 方法 | 近似对象 | 需要 Jacobian | 多峰 |
| --- | --- | --- | --- |
| EKF | 非线性函数的局部一阶形式 | 是 | 否 |
| UKF | 变换后分布的矩 | 否 | 否 |
| Particle Filter | 用样本近似 Belief | 否 | 是 |

## 思考题

### 思考题 1

UKF 为什么不是 Particle Filter？

> [!answer]- 参考答案
> Sigma Points 是为了匹配 Gaussian 矩而确定性选择的少量点，传播后仍压缩回一个 Gaussian；Particles 是随机或准随机样本，可用于表达非 Gaussian 和多峰分布。

## 下一章

[[Week 2 Chapter 23|Week 2 Chapter 23：Non-Gaussian Filters 与方法选择]]

