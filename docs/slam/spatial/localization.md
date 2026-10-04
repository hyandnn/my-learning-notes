---
title: 已知地图中的定位
description: 如何融合运动与观测，在已知地图中维护位姿 Belief？
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 34
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 已知地图中的定位

## 本章目标

区分局部定位、全局定位与绑架恢复，选择 EKF 或粒子表示。

## 前置知识

[运动模型](robot-motion-models.md)、[观测模型](sensor-models.md)、[Bayes Filter](../probabilistic/bayes-filter.md)、[非 Gaussian 滤波](../probabilistic/non-gaussian-filters.md)。

## 定义与假设

本章地图 m 已知且固定；运动与观测满足 Bayes Filter 的条件独立假设。EKF 需要可局部线性化、近似单峰的 Belief；数据关联应正确或经过验证。

现在：

Motion Model 有了：

$$
p(x_t|x_{t-1},u_t)
$$

Sensor Model 有了：

$$
p(z_t|x_t,m)
$$

假设：

$$
\boxed{\text{Map 已知}}
$$

问题就是：

> Robot 在 Map 中哪里？

这就是 Localization。

---

## 1. Localization 的 Bayesian 形式

Prediction：

$$
\boxed{ bel^-(x_t) = \int p(x_t|x_{t-1},u_t) bel(x_{t-1}) dx_{t-1} }
$$

Correction：

$$
\boxed{ bel(x_t) \propto p(z_t|x_t,m) bel^-(x_t) }
$$

这个结构沿用 Part II 的 Bayes Filter。

区别只是：

> 现在 State 明确变成 Robot Pose。

---

## 2. EKF Localization

如果：

- Belief 基本单峰；
- 初始位置大致知道；
- Model 可以局部线性化；

可以使用：

$$
x\sim\mathcal N(\mu,P)
$$

Motion Prediction：

$$
\mu^-=f(\mu,u)
$$

$$
P^-=FPF^T+Q
$$

Observation：

$$
r=z-h(\mu^-)
$$

$$
S=HP^-H^T+R
$$

$$
K=P^-H^TS^{-1}
$$

Update：

$$
\mu=\mu^-+Kr
$$

$$
P=(I-KH)P^-
$$

这就是我们 Part II 学过的 Kalman Filter，现在终于完整落到 Localization。

---

## 3. EKF Localization 的问题

假设机器人醒来时完全不知道自己在哪。

可能：

```
厨房 30%
卧室 25%
客厅 45%
```

这明显不是一个 Gaussian。

强行用：

$$
\mathcal N(\mu,P)
$$

表示，会把三个可能位置平均成：

> “机器人可能在墙里面。”

这就是单 Gaussian Representation 的根本限制。

---

## 4. Monte Carlo Localization

解决方法之一：

$$
\boxed{\text{Particle Filter}}
$$

用很多 Particle：

$$
\{x_t^{[1]},x_t^{[2]},...,x_t^{[N]}\}
$$

表示 Belief。

每个 Particle 都是假设：

> “机器人可能在这里。”

Motion 后：

```
所有 particle 根据运动模型移动
```

Observation 后：

```
和 sensor 更匹配的 particle → 高权重
不匹配 → 低权重
```

然后 Resampling。

在地图可区分、粒子覆盖充分且模型合适时，权重可逐渐集中到与观测一致的位置；对称环境仍可能保留多峰，重采样也可能丢失正确假设。

---

## 5. Global Localization

如果机器人完全不知道初始 Pose：

$$
p(x_0)
$$

可以在整个 Map 上分布 Particle。

随着机器人：

- 移动；
- 观察；

不同 Hypothesis 被逐渐排除。

这就是：

$$
\boxed{\text{Global Localization}}
$$

你在 Part I 提到的：

> 保留多个 Belief，等待未来 Observation 提供区分信息。

Particle Filter 就是这件事的一个非常具体的实现。

---

## 6. Kidnapped Robot Problem

机器人本来知道自己在哪。

突然有人把它抱起来放到另一个地方。

Motion Model 完全没有记录这次变化。

因此：

$$
Prediction
$$

仍然坚信旧位置。

Observation 却持续严重不匹配。

这叫：

$$
\boxed{\text{Kidnapped Robot Problem}}
$$

如果算法只维护非常窄的单峰 Belief，它可能永远恢复不了。

带随机粒子注入或恢复机制的 MCL 可以重新探索全局假设；普通粒子滤波本身并不保证绑架恢复。

---

## 7. Localization 和 SLAM 的区别

Localization：

$$
\boxed{\text{Map known, Pose unknown}}
$$

Mapping：

$$
\boxed{\text{Pose known, Map unknown}}
$$

SLAM：

$$
\boxed{\text{Pose unknown, Map unknown}}
$$

也就是：

$$
p(x_{1:t},m|z_{1:t},u_{1:t})
$$

因此 SLAM 比 Localization 多出来的真正困难是：

> Robot Pose 与 Map 相互依赖。

Pose 错了，Map 就画错。

Map 错了，又反过来把 Pose 拉错。

## 方法边界

前文 EKF 均值加法更新用于平面坐标参数；θ 应归一化到约定区间。三维 SE(3) 状态必须用局部误差注入。观测噪声协方差 R 与旋转矩阵 R 是不同上下文的记号。

在有限精度实现中，协方差更新可用 Joseph 形式：

$$
P=(I-KH)P^-(I-KH)^T+KRK^T.
$$

它在相同线性化模型与 Kalman Gain 下与简式等价，更适合保持数值对称性与半正定性。粒子数量有限、地图重复、模型错误时，MCL 也可能失败。

> 修订说明：草稿中“逐渐只剩真实位置”改为带条件的后验集中；随机粒子注入属于恢复机制，并非所有 MCL 默认具备。

## 本章小结

已知地图定位沿用 Prediction / Correction 循环。局部单峰 Belief 可使用 EKF，多峰和全局假设可使用 MCL；方法选择仍受模型、初始化、可观测性与关联可靠性约束。

## 自测

全局定位为何通常不适合单 Gaussian EKF？

<details>

<summary>参考答案</summary>

未知初始位置可能产生多个分离假设。单 Gaussian 无法保留这些模式，且局部线性化可能不成立；粒子表示可保留多峰，但依赖充分覆盖。

</details>

## 相关章节与来源

- 上一章：[传感器观测模型](sensor-models.md)
- 下一篇：[数据关联](data-association.md)
- 来源：本次新增的 Part III 课堂草稿，按实际课程内容整理。
