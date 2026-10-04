---
title: 为什么 Gaussian 如此常用？
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 14
chapter_type: lecture
tags: [slam, gaussian, mean, variance, covariance]
status: organized
---

# 为什么 Gaussian 如此常用？

## 本章目标

- 理解 Gaussian 是 Belief Model，不是 Reality
- 掌握 Mean、Variance 与 Covariance 的含义
- 认识 Gaussian 的计算优势和失效边界

## 符号表

| 符号 | 含义 | 维度 |
| --- | --- | --- |
| $$\boldsymbol\mu$$ | 均值向量 | $$n\times1$$ |
| $$\mathbf\Sigma$$ | 协方差矩阵 | $$n\times n$$ |
| $$\sigma^2$$ | 一维方差 | 标量 |

## 正文

### 1. Gaussian 是压缩模型

一维 Gaussian：

$$
x\sim\mathcal N(\mu,\sigma^2),\qquad
p(x)=\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\left[-\frac{(x-\mu)^2}{2\sigma^2}\right]
$$

多维 Gaussian：

$$
\mathbf{x}\sim\mathcal N(\boldsymbol\mu,\mathbf\Sigma)
$$

它用 Mean 和 Covariance 压缩完整分布。现实误差可以偏态、长尾、多峰或含 Outlier，因此 Gaussian 是计算假设。

### 2. Mean 与 Variance

$$
\mu=\mathbb E[x],\qquad
\sigma^2=\mathbb E[(x-\mu)^2]
$$

Mean 给出中心，Variance 表示围绕中心的分散程度。Gaussian 对称且单峰，所以 Mean、Median 与 Mode 重合；一般分布不具备这个性质。

### 3. Covariance

$$
\mathbf\Sigma
=
\mathbb E\left[(\mathbf{x}-\boldsymbol\mu)
(\mathbf{x}-\boldsymbol\mu)^\top\right]
$$

对二维状态：

$$
\mathbf\Sigma=
\begin{bmatrix}
\sigma_x^2 & \sigma_{xy}\\
\sigma_{xy} & \sigma_y^2
\end{bmatrix}
$$

对角项是各方向方差，非对角项表达变量共同变化。它决定误差椭圆的尺度和方向，而不只是一个“误差大小”。

### 4. 为什么计算方便

- 线性变换后仍为 Gaussian。
- 独立 Gaussian 噪声相加仍为 Gaussian。
- Gaussian Prior 与 Gaussian Likelihood 相乘后仍可归一化为 Gaussian。
- 只递归维护 Mean 与 Covariance，计算量可控。

若 $$\mathbf y=\mathbf A\mathbf x+\mathbf b$$ 且 $$\mathbf x\sim\mathcal N(\boldsymbol\mu,\mathbf\Sigma)$$：

$$
\mathbf y\sim\mathcal N(
\mathbf A\boldsymbol\mu+\mathbf b,
\mathbf A\mathbf\Sigma\mathbf A^\top)
$$

### 5. 适用边界

- 多峰 Belief 无法由单个 Gaussian 忠实表达。
- Outlier 和长尾噪声会破坏 Gaussian 假设。
- 非线性变换后分布通常不再是 Gaussian。
- Covariance 低估会造成危险的过度自信。

> **导师提示**
> Gaussian 受欢迎，不是因为世界服从它，而是因为它在“表达能力”和“可计算性”之间给出了极强的工程折中。

## 本章小结

$$
\boxed{\text{Gaussian} = \text{Belief Compression by Mean and Covariance}}
$$

## 思考题

### 思考题 1

为什么错误匹配不能简单当作更大的 Gaussian Noise？

<details>

<summary>参考答案</summary>

错误匹配常形成偏置、长尾或另一种数据生成机制，不只是同一分布方差变大。强行 Gaussian 化可能严重低估极端错误概率。

</details>

## 下一章

[Week 2 Chapter 15：Bayes Filter](bayes-filter.md)
