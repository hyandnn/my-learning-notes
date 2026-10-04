---
title: 数据关联
description: 如何判断当前观测对应哪个地图对象，并处理错误匹配？
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 35
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 数据关联

## 本章目标

区分外观相似与几何一致，用门控与多假设控制关联错误。

## 前置知识

[观测可信度与门控](../probabilistic/observation-validation.md)、[观测模型](sensor-models.md)、[定位](localization.md)。

## 定义与假设

观测 z 与候选地图对象的预测必须具有相同坐标系、单位和时刻。Mahalanobis 门控假设创新协方差 S 可逆且误差模型适用；关联错误不能当成普通小 Gaussian 噪声。

到这里还有一个巨大问题。

Camera 看见：

```
一个角点
```

地图里有：

```
5000 个角点
```

它对应哪一个？

这就是：

$$
\boxed{\text{Data Association}}
$$

---

## 1. 为什么 Data Association 如此重要？

假设 Observation：

$$
z_i
$$

真正来自 Landmark：

$$
m_j
$$

如果匹配正确：

$$
z_i\leftrightarrow m_j
$$

Residual 可以修正 State。

但如果错误匹配：

$$
z_i\leftrightarrow m_k
$$

优化器仍然会努力降低 Residual。

结果就是：

> 它会主动把正确 Pose 拉向错误的位置。

因此错误 Association 和普通 Gaussian Noise 性质完全不同。

---

## 2. Descriptor Matching

视觉系统中：

```
Feature Detection
      ↓
Descriptor
      ↓
Descriptor Matching
```

例如历史经典方法：

- ORB；
- SIFT；
- SURF；

以及现代 Learned Features。

Descriptor 回答：

> 这两个局部图像区域“长得像不像”。

但：

$$
\boxed{\text{Appearance Similarity}\neq\text{Geometric Consistency}}
$$

两个不同位置可能长得很像。

---

## 3. Geometric Gating

假设当前 Pose Prediction 已知。

地图 Landmark：

$$
P_W
$$

可以预测它应该出现在：

$$
\hat u=\pi(T_{CW}P_W)
$$

附近。

如果 Feature 实际出现在完全不同区域：

$$
\|u-\hat u\|\gg threshold
$$

即使 Descriptor 很像，也应该拒绝。

这就是：

> 用 Geometry 限制 Association Search Space。

---

## 4. Mahalanobis Gating

如果 Observation Prediction 有 Covariance：

$$
S
$$

Residual：

$$
r=z-\hat z
$$

使用：

$$
\boxed{ d_M^2=r^TS^{-1}r }
$$

而不是单纯：

$$
\|r\|^2
$$

判断 Association。

为什么？

假设：

```
横向 uncertainty 很大
纵向 uncertainty 很小
```

同样 5 Pixel Error：

- 横向可能正常；
- 纵向可能非常异常。

Mahalanobis Distance 会考虑这种方向性。

这就是 Part II 的 Gating 在 Data Association 中的具体应用。

---

## 5. Nearest Neighbor 的危险

最简单策略：

> 找距离最近的 Landmark。

在稀疏、Prediction 准确时可以工作。

但在：

- Repetitive Texture；
- Dense Features；
- Large Motion；
- Poor Initialization；

情况下非常危险。

Nearest 不等于 Correct。

---

## 6. RANSAC 的作用

例如 Feature Matching 得到：

```
100 matches
```

其中：

```
70 correct
30 wrong
```

RANSAC 不要求一开始知道谁正确。

它不断：

1. 随机抽少量匹配；
2. 估计一个 Geometry Model；
3. 检查多少匹配支持这个 Model；
4. 找最大 Consensus Set。

例如：

- Fundamental Matrix；
- Essential Matrix；
- Homography；
- PnP Pose。

它实际上在问：

> 哪一组 Association 可以被同一个几何解释统一解释？

---

## 7. 为什么 Outlier 特别危险？

Gaussian Noise：

$$
z=z_{\text{true}}+\epsilon
$$

其中：

$$
\epsilon
$$

通常只是 Truth 附近的小扰动。

Outlier：

$$
z\leftrightarrow\text{wrong object}
$$

它不是“大一点的 Noise”。

它来自：

> 完全不同的数据生成过程。

因此工程中通常需要：

- Gating；
- RANSAC；
- Robust Loss；
- Semantic Constraints；
- Temporal Consistency；

共同处理。

---

## 8. Multi-Hypothesis Data Association

有时候：

```
Feature A
```

可能对应：

```
Landmark 17：45%
Landmark 38：40%
Landmark 52：15%
```

如果信息不足，理论上可以保留多个 Hypothesis。

这就是我们 Part I / II 反复讨论的：

$$
\boxed{\text{Ambiguity should sometimes be represented, not prematurely collapsed}}
$$

但计算复杂度可能快速爆炸。

因此工程系统往往：

- Gating；
- Top-K；
- Pruning；
- Delayed Decision；

折中处理。

## 门控的统计条件

若候选地图对象确定且与状态误差独立，局部线性化下：

$$
S\approx HP^-H^T+R,\qquad d_M^2=r^TS^{-1}r.
$$

地图对象若也有不确定性，应传播到 S；若与状态相关，应包含交叉项。对 k 维、零均值 Gaussian 创新，正确模型下 d_M² 服从 k 自由度的 χ² 分布，可据此选择门限；数据关联搜索后的统计量不应机械视作未经选择的检验。

通过门控只说明候选与当前预测相容，不证明身份正确。RANSAC 也依赖模型选择、内点比例与采样覆盖，不能解决所有重复纹理或退化情形。

## 本章小结

关联决定观测约束的是哪个对象。外观、距离与门控只提供候选证据；几何一致性、时间一致性和多假设机制共同控制错误关联。

## 自测

通过 Mahalanobis 门控是否证明关联正确？

<details>

<summary>参考答案</summary>

不能。门控判断与当前预测是否统计相容，重复纹理和对称结构仍可产生错误候选，需要几何、时间或多假设验证。

</details>

## 相关章节与来源

- 上一章：[已知地图中的定位](localization.md)
- 下一篇：[扫描匹配与 ICP](scan-matching-icp.md)
- 来源：本次新增的 Part III 课堂草稿，按实际课程内容整理。
