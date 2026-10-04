---
title: 扫描匹配与 ICP
description: 如何在 SE(3) 上对齐点云，并识别局部收敛与几何退化？
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 36
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 扫描匹配与 ICP

## 本章目标

理解 ICP 的对应搜索、残差、局部更新、退化与 SLAM 前端角色。

## 前置知识

[SE(3)](se3.md)、[位姿不确定性](pose-uncertainty.md)、[数据关联](data-association.md)、[可观测性](../probabilistic/observability.md)。

## 定义与假设

T 把源点 p_i 映射到目标坐标系；对应 q_i 与单位法向 n_i 也在目标系中。每次线性化暂时固定对应关系，采用左扰动及 [δρ,δφ] 排列；要求足够重叠、合理初值和有效几何约束。

现在来到 Part III 最后一章。

我们有两帧 Point Cloud：

$$
P=\{p_i\}
$$

$$
Q=\{q_j\}
$$

希望找到：

$$
T\in SE(3)
$$

使：

$$
TP
$$

尽可能与：

$$
Q
$$

对齐。

这就是：

$$
\boxed{\text{Scan Matching}}
$$

ICP 是其中最经典的方法之一。

---

## 1. ICP 的基本思想

ICP：

> Iterative Closest Point。

最基础流程：

```
Initial Pose
    ↓
Transform Source Cloud
    ↓
Find Correspondence
    ↓
Estimate Better Pose
    ↓
Transform Again
    ↓
Repeat
```

即：

$$
T_0 \rightarrow T_1 \rightarrow T_2 \rightarrow\cdots
$$

直到收敛。

---

## 2. Point-to-Point ICP

假设 Correspondence 已知：

$$
p_i\leftrightarrow q_i
$$

优化：

$$
\boxed{ \min_{R,t} \sum_i \|Rp_i+t-q_i\|^2 }
$$

Residual：

$$
r_i=Rp_i+t-q_i
$$

每个点贡献三维 Residual。

---

## 3. Point-to-Plane ICP

如果目标点：

$$
q_i
$$

对应表面法向：

$$
n_i
$$

则：

$$
\boxed{ r_i = n_i^T(Rp_i+t-q_i) }
$$

只惩罚沿 Normal Direction 的距离。

直觉上：

> 一个点只要落到目标表面上就够了，不必强迫它精准对应目标点本身。

对于局部平滑 Surface，Point-to-Plane 往往比 Point-to-Point 收敛更快。

---

## 4. 为什么 Point-to-Plane 更符合 Surface Alignment？

想象两面墙。

Source Point：

```
•
```

Target 上最近点：

```
        •
```

沿墙面切向可能差很多，但两者其实属于同一面墙。

Point-to-Point 会惩罚切向差异。

Point-to-Plane 主要看：

> Source 有没有落到目标 Plane 上。

因此对于连续 Surface：

$$
\boxed{\text{Normal Direction carries stronger geometric constraint}}
$$

---

## 5. ICP 中 $$SE(3)$$ 如何出现？

当前估计：

$$
T
$$

使用六维小增量：

$$
\delta\xi\in\mathbb R^6
$$

更新：

$$
T_{\text{new}} = \operatorname{Exp}(\delta\xi^\wedge)T
$$

Residual 线性化：

$$
r(T_{\text{new}}) \approx r(T)+J\delta\xi
$$

然后求：

$$
\boxed{ \delta\xi^* = \arg\min \|r+J\delta\xi\|^2 }
$$

这就是我们前面为什么花那么多时间学：

$$
SE(3),\quad \mathfrak{se}(3),\quad Exp
$$

它们现在真正进入 Optimization。

---

## 6. Gauss–Newton

把所有 Residual 堆起来：

$$
r
$$

Jacobian：

$$
J
$$

优化：

$$
\min_{\delta\xi} \|r+J\delta\xi\|^2
$$

Normal Equation：

$$
\boxed{ J^TJ\delta\xi=-J^Tr }
$$

所以：

$$
\delta\xi = -(J^TJ)^{-1}J^Tr
$$

实际工程不会真的显式求逆，通常使用线性求解器。

更新：

$$
T\leftarrow \operatorname{Exp}(\delta\xi)T
$$

不断迭代。

---

## 7. ICP 为什么需要 Initial Guess？

ICP 的 Correspondence 通常基于当前 Pose 找最近点。

如果 Initial Pose 太差：

```
真正对应 A ↔ A
```

但当前位置太远：

```
算法找到 A ↔ B
```

于是优化会根据错误 Correspondence 往错误方向走。

所以 ICP 通常是：

$$
\boxed{\text{Local Optimization}}
$$

而不是 Global Localization Algorithm。

Initial Guess 可以来自：

- Wheel Odometry；
- IMU；
- Constant Velocity；
- Previous Frame；
- Feature Matching。

---

## 8. ICP 的 Local Minimum

即使 Residual 最后很小：

$$
\sum r_i^2\rightarrow small
$$

也不能证明：

$$
T=T_{\text{truth}}
$$

因为可能存在：

- Repetitive Structure；
- Wrong Correspondence；
- Symmetry；
- Partial Overlap；
- Local Minimum。

这与 Part II 的残差诊断结论一致：

> **Residual 很小并不意味着 State Estimate 一定可靠。**

扫描匹配提供了这一结论的具体例子。

---

## 9. Degeneracy

想象 LiDAR 只看到一面巨大平墙。

Point-to-Plane ICP 可以很好约束：

> 垂直于墙面的 Translation。

但沿墙面滑动：

$$
\delta t_{\parallel}
$$

Residual 几乎不变。

某些 Rotation Direction 也可能约束很弱。

于是：

$$
J^TJ
$$

出现很小的 Eigenvalue。

这意味着：

$$
\boxed{\text{某些 Pose Direction 几乎不可观测}}
$$

这就是 Part II 的 Observability / Information Strength 在 Scan Matching 中最具体的体现之一。

---

## 10. Hessian 的 Eigenvalue

近似 Hessian：

$$
H=J^TJ
$$

Eigen Decomposition：

$$
H=V\Lambda V^T
$$

如果：

$$
\lambda_i\gg0
$$

说明对应方向有很强 Constraint。

如果：

$$
\lambda_i\approx0
$$

说明对应方向：

> 数据几乎提供不了信息。

因此 Degeneracy 不是一句：

> “点云质量不好。”

而可以具体分析：

> 哪个 State Direction 缺乏 Information？

---

## 11. Correspondence Filtering

实际 ICP 不会接受所有最近点。

通常加入：

- Maximum distance；
- Normal consistency；
- Boundary rejection；
- Robust kernel；
- Trimmed ICP；
- Semantic filtering。

因为 Correspondence 本身就是 Data Association。

所以 Chapter 35 和 Chapter 36 并不是两个完全独立的话题。

---

## 12. Robust Loss

普通 Least Squares：

$$
\min\sum r_i^2
$$

会让巨大 Outlier 产生巨大影响。

可以改为：

$$
\boxed{ \min\sum\rho(r_i) }
$$

例如：

- Huber；
- Cauchy；
- Tukey。

对于小 Residual：

$$
\rho(r)\approx r^2
$$

对于巨大 Residual：

> 不再让 Cost 二次爆炸。

本质上是在说：

> 我不完全相信每一个 Correspondence 都来自同一个 Gaussian Noise Model。

---

## 13. Scan-to-Scan 与 Scan-to-Map

### Scan-to-Scan

当前帧：

$$
S_t
$$

匹配上一帧：

$$
S_{t-1}
$$

得到：

$$
T_{t-1,t}
$$

优点：

- Map 小；
- 计算简单。

缺点：

> Error 一帧一帧累积。

---

### Scan-to-Map

当前 Scan：

$$
S_t
$$

直接匹配 Local Map：

$$
M
$$

多个历史帧共同形成 Map。

通常提供：

- 更丰富 Geometry；
- 更强 Constraint；
- 更稳定 Pose。

现代 LiDAR Odometry 很多会使用类似思想。

---

## 14. ICP 和 SLAM 是什么关系？

ICP 本身不是 SLAM。

它解决的是：

$$
\boxed{\text{Relative Pose / Registration}}
$$

它可以成为 SLAM Front-end 的一部分：

```
Sensor
  ↓
Scan Matching
  ↓
Relative Pose
  ↓
Odometry
  ↓
Keyframes
  ↓
Backend Optimization
  ↓
Map
```

所以：

$$
\boxed{ \text{ICP 可用于 Scan Matching，并构成 SLAM Frontend 的一个模块} }
$$

大致可以这么理解。

## 补充推导：左扰动下的 ICP Jacobian

令 s_i = Rp_i + t，左扰动使 δs_i ≈ δρ − s_i^∧δφ。因此点到点与点到面 Jacobian 分别是：

$$
J_i^{\mathrm{point}}=[I\; -s_i^\wedge],\qquad
J_i^{\mathrm{plane}}=n_i^T[I\; -s_i^\wedge].
$$

维度分别为 3×6 与 1×6，法向在本次局部求解中固定。对目标 E = ‖r+Jδξ‖² 求导：

$$
\nabla E=2J^T(r+J\delta\xi)=0
\quad\Longrightarrow\quad J^TJ\delta\xi=-J^Tr.
$$

### 推导得到什么

Gauss–Newton 解出的是当前对应与线性化点附近的增量。前文逆矩阵表达式只在 JᵀJ 非奇异时成立；退化时需要阻尼、先验或处理零空间，不能直接求逆。

### 在 SLAM 中怎么用

每次求解并更新位姿后重新建立对应关系。若加入测量权重，信息矩阵为 JᵀWJ；其特征值大小受残差单位、平移与旋转尺度和采样密度影响，跨场景比较前应统一尺度。

对于单一理想平面，沿平面两个方向的平移及绕法向的旋转不改变点到面残差。丰富点数不能替代丰富约束方向。

> 修订说明：草稿的 ICP ⊂ SLAM Frontend 仅表示模块关系，改为文字说明；补充 Jacobian、正规方程推导与 Hessian 可逆条件。小残差只能说明当前关联下拟合较好。

## 本章小结

ICP 交替建立对应并优化局部位姿增量。小残差不证明位姿正确，Hessian 的弱方向揭示局部退化；扫描匹配还需要初值、异常对应过滤与更完整的 SLAM 系统。

## 自测

ICP 残差很小但 Hessian 有小特征值，说明什么？

<details>

<summary>参考答案</summary>

当前对应下拟合良好，但某个局部位姿方向约束弱。应结合特征向量、统一尺度和场景几何诊断，而非只看一个匹配分数。

</details>

## 相关章节与来源

- 上一章：[数据关联](data-association.md)
- 下一篇：[Part III 回顾与自测](summary.md)
- 后续应用：[非线性最小二乘](../mapping/nonlinear-least-squares.md)、[视觉／激光惯性状态估计](../mapping/visual-lidar-inertial.md)
- 来源：本次新增的 Part III 课堂草稿，按实际课程内容整理。
