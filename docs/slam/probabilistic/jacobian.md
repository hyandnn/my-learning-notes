---
title: Jacobian 与线性化
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 20
chapter_type: derivation
tags: [slam, jacobian, linearization, taylor-expansion, information]
status: organized
---

# Jacobian 与线性化

## 本章目标

- 从导数推广到 Jacobian
- 推导多变量一阶线性化
- 理解 Jacobian 在敏感度、协方差传播和优化中的角色

## 公式定义

对 $$\mathbf z=h(\mathbf x)$$，其中 $$h:\mathbb R^n\rightarrow\mathbb R^m$$：

$$
\mathbf J=\frac{\partial h}{\partial\mathbf x}
=
\begin{bmatrix}
\frac{\partial h_1}{\partial x_1}&\cdots&\frac{\partial h_1}{\partial x_n}\\
\vdots&\ddots&\vdots\\
\frac{\partial h_m}{\partial x_1}&\cdots&\frac{\partial h_m}{\partial x_n}
\end{bmatrix}
$$

$$J_{ij}$$ 表示输出 $$h_i$$ 对状态分量 $$x_j$$ 的局部敏感度。

## 线性化推导

在当前估计 $$\hat{\mathbf x}$$ 附近令 $$\mathbf x=\hat{\mathbf x}+\delta\mathbf x$$。一阶 Taylor 展开：

$$
h(\hat{\mathbf x}+\delta\mathbf x)
=h(\hat{\mathbf x})
+\mathbf J(\hat{\mathbf x})\delta\mathbf x
+O(\|\delta\mathbf x\|^2)
$$

忽略二阶及以上项：

$$
h(\mathbf x)\approx h(\hat{\mathbf x})
+\mathbf J(\hat{\mathbf x})(\mathbf x-\hat{\mathbf x})
$$

> **近似边界**
> Jacobian 是线性化点附近的局部近似。状态误差大、曲率强或角度跨越边界时，一阶近似可能失效。

## 二维运动模型

$$
f(\mathbf x,\mathbf u)=
\begin{bmatrix}
x+v\cos\theta\Delta t\\
y+v\sin\theta\Delta t\\
\theta+\omega\Delta t
\end{bmatrix}
$$

对状态 $$\mathbf x=[x,y,\theta]^\top$$ 的 Jacobian：

$$
\mathbf F=
\begin{bmatrix}
1&0&-v\sin\theta\Delta t\\
0&1&v\cos\theta\Delta t\\
0&0&1
\end{bmatrix}
$$

朝向误差会通过非零偏导传播到位置误差，这解释了为什么姿态不确定性会快速污染轨迹。

## Jacobian 与 Information

局部 Gaussian 模型下：

$$
\mathbf\Lambda=\mathbf J^\top\mathbf R^{-1}\mathbf J
$$

若某个 State Direction 位于 $$\mathbf J$$ 的 Null Space，该方向不会改变 Observation，因而局部不提供信息。

最小二乘目标线性化后，Gauss-Newton 正规方程为：

$$
(\mathbf J^\top\mathbf W\mathbf J)\delta\mathbf x
=-\mathbf J^\top\mathbf W\mathbf r
$$

## Jacobian 检查

解析 Jacobian 应与有限差分比较：

$$
\frac{\partial h}{\partial x_i}\approx
\frac{h(\mathbf x+\epsilon\mathbf e_i)-h(\mathbf x-\epsilon\mathbf e_i)}{2\epsilon}
$$

$$\epsilon$$ 过大会引入截断误差，过小会受浮点误差影响。

## 思考题

### 思考题 1

Jacobian 某一列接近零意味着什么？

<details>

<summary>参考答案</summary>

在当前线性化点附近，对应 State 分量的变化几乎不改变 Observation，因此该方向局部信息弱；这不自动代表全局不可观测。

</details>

## 下一章

[Week 2 Chapter 21：Extended Kalman Filter](ekf.md)
