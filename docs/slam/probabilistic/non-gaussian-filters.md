---
title: 非 Gaussian 滤波与方法选择
course: Robot Perception & SLAM
part: Part II Probabilistic State Estimation
week: 2
chapter: 23
chapter_type: lecture
tags: [slam, particle-filter, histogram-filter, mcl, non-gaussian]
status: organized
---

# 非 Gaussian 滤波与方法选择

## 本章目标

- 理解 Histogram 与 Particle Filter
- 推导 Sequential Importance Sampling 的基本权重
- 根据 Belief、维度和实时预算选择方法

## Histogram Filter

将状态空间划分为网格并保存每格概率。离散 Bayes Filter 为：

$$
\overline{bel}_t(x_i)=\sum_jp(x_i\mid u_t,x_j)bel_{t-1}(x_j)
$$

$$
bel_t(x_i)=\eta p(z_t\mid x_i)\overline{bel}_t(x_i)
$$

它可表达任意离散多峰分布，但网格数量随维度指数增长。

## Particle Filter

用带权样本集表示 Belief：

$$
bel(x_t)\approx\{(x_t^{[i]},w_t^{[i]})\}_{i=1}^N
$$

基本流程：

1. 从 Proposal $$q(x_t\mid x_{t-1}^{[i]},u_t,z_t)$$ 采样。
2. 根据 Target 与 Proposal 的比值更新权重。
3. 归一化并按需要 Resample。

一般重要性权重：

$$
w_t^{[i]}\propto w_{t-1}^{[i]}
\frac{p(z_t\mid x_t^{[i]})p(x_t^{[i]}\mid x_{t-1}^{[i]},u_t)}
{q(x_t^{[i]}\mid x_{t-1}^{[i]},u_t,z_t)}
$$

若 Proposal 直接取 Motion Model：

$$
q=p(x_t\mid x_{t-1},u_t)
$$

则简化为：

$$
w_t^{[i]}\propto w_{t-1}^{[i]}p(z_t\mid x_t^{[i]})
$$

## Resampling 与退化

有效样本数常估计为：

$$
N_{eff}=\frac1{\sum_i(\tilde w_t^{[i]})^2}
$$

$$N_{eff}$$ 低于阈值时 Resample，可删除低权重样本并复制高权重样本；副作用是 Sample Impoverishment。可通过自适应重采样、改进 Proposal、Roughening 或随机粒子注入缓解。

## Monte Carlo Localization

MCL 用粒子表示机器人 Pose Belief，天然支持全局定位、多峰和 Kidnapped Robot Recovery。其代价与状态维度、地图查询、观测似然计算和所需粒子数有关。

## 方法选择

| Belief / 条件 | 常见选择 |
| --- | --- |
| 线性、Gaussian | KF |
| 局部非线性、初值好 | EKF |
| 中等维度、避免 Jacobian | UKF |
| 低维、多峰或全局定位 | Particle / Histogram |
| 高维稀疏 SLAM | 通常考虑图优化等方法 |

> **导师提示**
> 先判断 Belief 的形状和 State 维度，再选择 Filter；不要从算法名字反推问题表示。

## 易混点

- Particles 仍是有限样本近似，不等于真实分布。
- Resampling 不是 Correction；权重计算才吸收 Observation。
- Filter 只是系统后端的一部分，不能替代前端关联、异常值处理和模型设计。

## 思考题

### 思考题 1

为什么高维 State 通常不适合朴素 Particle Filter？

<details>

<summary>参考答案</summary>

概率质量会集中在高维空间的极小区域，合理覆盖 Posterior 所需样本数迅速增长，且 Observation Likelihood 计算也更加昂贵。

</details>

## 下一章

[Week 2 Summary：Probabilistic State Estimation](summary.md)
