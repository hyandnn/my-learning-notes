---
title: Part III 回顾与自测
description: 串联空间几何、位姿不确定性、定位与扫描匹配，并进入地图未知的 SLAM 问题。
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter_type: summary
status: organized
---

# Part III 回顾与自测

覆盖 Chapter 24–36：空间表示 → 局部变化与不确定性 → 运动和观测 → 定位与关联 → 扫描匹配。

## 第一层：空间怎么表示？

我们首先解决：

> Robot、Sensor、Point 到底在哪？

二维：

$$
SE(2)
$$

三维 Rotation：

$$
SO(3)
$$

三维 Pose：

$$
SE(3)
$$

Rotation 可以表示为：

$$
R,\quad q,\quad \phi
$$

但它们都在描述同一个物理 Orientation。

核心认识：

$$
\boxed{\text{Pose is geometry, not an ordinary vector}}
$$

---

## 第二层：Pose 怎么变化？

局部变化：

$$
\delta\xi\in\mathfrak{se}(3)
$$

通过：

$$
\operatorname{Exp}(\delta\xi)
$$

映射成有限 Pose Change。

反过来：

$$
\operatorname{Log}(T_1^{-1}T_2)
$$

得到两个 Pose 的局部六维 Difference。

因此：

$$
\boxed{ \text{State on Manifold, Error in Tangent Space} }
$$

这是 Part III 最值得记住的一句话之一。

---

## 第三层：Pose 怎么带 Uncertainty？

不是：

$$
T+\epsilon
$$

而是：

$$
T = \bar T\operatorname{Exp}(\delta\xi)
$$

其中：

$$
\delta\xi\sim\mathcal N(0,P)
$$

Frame 改变时：

$$
\delta\xi_A = Ad_T\delta\xi_B
$$

Covariance：

$$
P_A = Ad_TP_BAd_T^T
$$

于是 Part II 的概率状态估计与 Part III 的几何正式接起来。

---

## 第四层：Robot 如何利用这些东西定位？

Motion：

$$
x_t=f(x_{t-1},u_t)+w_t
$$

Observation：

$$
z_t=h(x_t,m)+v_t
$$

Localization：

$$
Prediction \rightarrow Observation \rightarrow Correction
$$

但 Observation 首先要回答：

$$
\boxed{\text{我看到的东西到底对应 Map 里的谁？}}
$$

于是产生：

$$
Data\ Association
$$

对于 Point Cloud：

$$
Data\ Association + SE(3)\ Optimization
$$

进一步产生：

$$
Scan\ Matching / ICP
$$

所以整个逻辑链现在已经闭合：

$$
\boxed{ \begin{aligned} Motion\ Model &\rightarrow Pose\ Prediction\\ Sensor\ Model &\rightarrow Expected\ Observation\\ Data\ Association &\rightarrow Observation\ Correspondence\\ Residual &\rightarrow State\ Constraint\\ Optimization/Filter &\rightarrow Pose\ Correction \end{aligned} }
$$

---

## Part I、II、III 的连接

我们最开始在 Part I 讨论：

> Robot 永远接触不到 Truth。

现在可以写成：

$$
z=h(x)+v
$$

Robot 只能看到 $$z$$，而真正想知道的是隐藏状态 $$x$$。

---

Part II 我们讨论：

> Robot 应该维护 Belief，而不是一个自信满满的单值答案。

于是：

$$
p(x_t|z_{1:t},u_{1:t})
$$

---

Part III 又进一步回答：

> 如果这个隐藏 State 是 Robot Pose，它甚至不是普通欧氏向量。

而是：

$$
T\in SE(3)
$$

所以最终形成：

$$
\boxed{ \text{Physical World} \rightarrow \text{Sensor Observation} \rightarrow \text{Probabilistic Belief} \rightarrow \text{Geometric State} }
$$

这三部分其实是在从三个不同角度描述同一个机器人问题。

---

## 思考题与参考答案

### 思考题 1

一个 LiDAR Odometry 在长直走廊中出现：

- 沿走廊前后方向位置开始漂；
- 横向位置比较稳定；
- 某个 Rotation Direction 也不稳定；
- ICP Residual 仍然很小。

你认为应该首先怀疑：

A. ICP 没有收敛  
B. Sensor Noise 太大  
C. Geometry Degeneracy  
D. $$SE(3)$$ 实现错误

**参考答案**

选择：

$$
\boxed{C}
$$

很可能是 Geometry Degeneracy。

走廊的几何结构可能对某些 Pose Direction 提供很弱 Constraint。

关键证据是：

> Residual 很小，但某些方向仍然漂。

这正说明：

$$
\text{Good Fit}\neq\text{Fully Observable Pose}
$$

> 修订说明：按理想直走廊两侧墙面的几何，将草稿示例改为沿走廊方向弱约束、横向较强约束。真实弱方向仍需查看法向分布与 Hessian，不能仅凭走廊名称判定。


### 思考题 2

Visual Odometry 得到一个 Pose Increment：

$$
T_{t-1,t}
$$

Wheel Odometry 也得到：

$$
\tilde T_{t-1,t}
$$

两者不一致。

为什么不能简单：

```
Visual 0.5
Wheel 0.5
```

做平均？

**参考答案**

因为两个 Pose Measurement：

- Uncertainty 不同；
- Error Frame 可能不同；
- Rotation 与 Translation 不是普通线性变量；
- 可能存在 Cross-Covariance；
- 两个 Sensor 甚至可能有 Systematic Bias。

正确思路应该是：

1. 把 Measurement 转到统一 Frame；
2. 明确 $$SE(3)$$ Error Definition；
3. 映射到 Tangent Space；
4. 根据 Covariance / Information 进行 Fusion。

不是对两个 $$4\times4$$ Matrix 求平均。


### 思考题 3

机器人使用 ICP 定位。

某一帧：

$$
Residual
$$

突然非常大。

按照我们 Part II + III 的思路，你认为合理的诊断顺序是什么？

**参考答案**

比较合理的是：

$$
\boxed{ Observation \rightarrow Association \rightarrow Model \rightarrow State }
$$

先检查：

- Point Cloud 是否异常；
- Timestamp 是否异常；
- Correspondence 是否突然大量错误；
- Dynamic Objects 是否增多；
- Initial Guess 是否偏离；
- Geometry 是否发生 Degeneracy；
- Motion Model 是否失效。

而不是看到 Residual 大，就立即调 ICP 参数。

这与“分层验证 + 控制变量”的诊断方法一致。


### 思考题 4

Camera Observation 的 Reprojection Error 很小。

能否证明 Camera Pose 很准确？

**参考答案**

不能。

可能：

- Scene Geometry 本身退化；
- Pose 落入 Local Minimum；
- Association 错但内部自洽；
- Observation 只约束某几个 Pose Direction；
- Repetitive Texture 形成错误 Geometry。

所以：

$$
\boxed{ Small\ Residual \not\Rightarrow Correct\ State }
$$


### 思考题 5

一个机器人只有 Wheel Encoder。

在一个完全已知的 Map 中运行。

Encoder 极其精确。

但没有任何 Camera/LiDAR/其他环境 Observation。

它能否长期保持准确 Localization？

**参考答案**

通常不能。

Encoder 再准确，也只是准确测量：

$$
\text{Wheel Rotation}
$$

它无法直接验证：

$$
\text{Robot Motion}
$$

Wheel Slip、碰撞、轮径模型、地面状态都会造成 Motion Model Error。

而且没有外部 Observation，就没有绝对 Correction。

所以 Odometry Error 会持续累积。


### 思考题 6

ICP 的：

$$
J^TJ
$$

有一个非常小的 Eigenvalue。

这个信息比“ICP Score 比较差”多告诉了你什么？

**参考答案**

ICP Score 只是告诉你：

> “匹配得怎么样。”

而 Hessian Eigenstructure 可以进一步告诉你：

> **哪个 Pose Direction 有多少信息。**

如果：

$$
\lambda_i\approx0
$$

那么对应 Eigenvector：

$$
v_i
$$

就指出了：

> 当前 Geometry 无法有效约束的 State Direction。

这比一个单独的 Scalar Score 提供的信息丰富得多。


## 衔接 Part IV：地图也未知

Part III 建立了几何、位姿不确定性、运动与观测模型、定位、关联和扫描匹配的基础。接下来阅读 [Part IV · 建图与 SLAM](../mapping/README.md)，从[轨迹与地图的联合估计](../mapping/slam-formulation.md)开始。Part IV Chapter 37–48 已完成，具体章节与状态见[课程计划](../study-plan.md)。

## 相关笔记与来源

[Part III 章节目录](README.md) · [课程计划](../study-plan.md) · [扫描匹配与 ICP](scan-matching-icp.md)。来源为本次新增的 Part III 综合课堂草稿；保留全部六道阶段思考题及其答案。
