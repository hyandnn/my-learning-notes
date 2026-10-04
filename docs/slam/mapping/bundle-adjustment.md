---
title: Bundle Adjustment
description: 相机和地图如何联合优化，Schur Complement 怎样减少求解量？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 43
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# Bundle Adjustment

## 本章目标

相机和地图如何联合优化，Schur Complement 怎样减少求解量？

## 前置知识

[非线性最小二乘](nonlinear-least-squares.md)、[Visual SLAM 前端](visual-frontend.md)。

## 定义与假设

Gaussian 噪声、局部线性化和固定数据关联都是建模条件；相应推导只在这些条件下适用。三维位姿采用 SE(3)，局部扰动按 [δρ,δφ] 排列，平移用 m、旋转用 rad。Exp 输入六维向量时表示先经 hat 映射再取矩阵指数，Log 输出六维坐标；左右更新需与残差和 Jacobian 一致。 T_i 将世界点映射到第 i 个相机系，P_j 为世界系三维地标；像素观测 z_ij 为二维向量。标准重投影 BA 每个观测只连接一个相机与一个地图点。

## 核心问题


## 联合状态、残差与块稀疏性

### 1. BA 到底是什么？

先用最简单的一句话定义：

$$
\boxed{ Bundle\ Adjustment = 同时调整相机位姿和3D点，使所有重投影误差最小 }
$$

假设有三个 Camera：

$$
T_1,T_2,T_3
$$

还有四个 3D landmarks：

$$
P_1,P_2,P_3,P_4
$$

每个 Camera 看到其中一部分点。

比如：

```
       P1      P2      P3      P4
       |\      /|\     /|      /
       | \    / | \   / |     /
      C1 ---- C2 ---- C3
```

每一条“Camera 看到了 Point”的关系，就是一个 observation。

BA 要做的，就是调整：

$$
T_i
$$

和：

$$
P_j
$$

让所有这些 observation 尽可能互相一致。

### 2. 为什么相机 Pose 和 Landmark 要一起优化？

假设一个 3D point：

$$
P_j^w
$$

被 Camera $$i$$ 看到。

预测像素位置：

$$
\hat z_{ij} = \pi(T_iP_j)
$$

实际 measurement：

$$
z_{ij}
$$

于是 residual：

$$
r_{ij} = z_{ij}-\pi(T_iP_j)
$$

问题是：

如果 residual 很大， 到底是谁错了？

可能是：

$$
T_i
$$

错。

也可能是：

$$
P_j
$$

错。 甚至两个都错。

所以最合理的方式就是：

Both are variables 一起优化。

### 3. 这和 PnP 的区别是什么？

PnP：

$$
3D\ points\ fixed
$$

只求：

Camera Pose

也就是：

$$
\min_T \sum_j \|z_j-\pi(TP_j)\|^2
$$

BA：

Camera Pose

和：

Landmark

都优化：

$$
\min_{\{T_i,P_j\}} \sum_{ij} \|z_{ij}-\pi(T_iP_j)\|^2
$$

所以可以理解：

$$
\boxed{ PnP = BA 的一个特例 }
$$

只是把 Landmark 固定了。

### 4. BA 为什么名字叫 Bundle Adjustment？

这个名字最早来自摄影测量。

每个 3D point 到 Camera image plane 都形成一条光线：

```
Camera
   \

    \

      Point
```

很多 Camera、很多 points，就形成一束束：

ray bundles BA 就是在调整 Camera 和 3D points， 让这些“光束”更好地汇聚。

所以：

Bundle Adjustment

可以理解成：

> 调整整束多视图光线的几何一致性。

### 5. BA 的 State 是什么？

假设有：

$$
N
$$

个 Camera Poses，

每个：

$$
T_i\in SE(3)
$$

有 6 DoF。

还有：

$$
M
$$

个 3D Points：

$$
P_j\in\mathbb R^3
$$

整个 State：

$$
X= [ T_1,\dots,T_N, P_1,\dots,P_M ]
$$

如果简单按维度数：

$$
dim(X)=6N+3M
$$

比如：

$$
N=100
$$

$$
M=10000
$$

那么：

$$
6\times100+3\times10000 = 30600
$$

个变量。 已经不小了。

### 6. Observation 数量可能更多

每个 landmark 通常被多个 Camera 看到。

假设平均每个 MapPoint 被：

$$
5
$$

个 Keyframes 看到。

那么 observation 数量：

$$
50000
$$

每个 visual observation 是二维 pixel：

$$
(u,v)
$$

所以 residual 总维数：

$$
100000
$$

这是一个很大的 nonlinear least-squares problem。 但它为什么还能高效求？

因为：

它非常稀疏

### 7. BA 的稀疏性来自哪里？

一个 observation：

$$
r_{ij}
$$

只依赖两个变量：

$$
T_i
$$

和：

$$
P_j
$$

不会依赖：

$$
T_k,\quad k\neq i
$$

也不会依赖：

$$
P_l,\quad l\neq j
$$

所以：

$$
\frac{\partial r_{ij}}{\partial T_k}=0
$$

如果：

$$
k\neq i
$$

同样：

$$
\frac{\partial r_{ij}}{\partial P_l}=0
$$

如果：

$$
l\neq j
$$

所以 Jacobian 绝大部分都是 0。

### 8. 画成 Jacobian 很直观

假设：

$$
r_{12}
$$

表示 Camera 1 观察 Point 2。

那么 Jacobian 这一行只有：

```
T1        T2      T3       P1      P2      P3
↓                                  ↓
[J_pose    0       0        0     J_point   0]
```

所以 BA 天然具有：

Block Sparse Structure

### 9. BA 的 cost

通常写成：

$$
E = \sum_{(i,j)\in\mathcal O} r_{ij}^T \Omega_{ij} r_{ij}
$$

其中：

$$
\mathcal O
$$

表示所有有效 observation。

$$
\Omega_{ij} = \Sigma_{ij}^{-1}
$$

是 information matrix。

Residual：

$$
r_{ij} = z_{ij} - \pi(T_iP_j)
$$

这就是标准 BA。

### 10. 每次迭代还是 Chapter 42 那套流程

当前：

$$
T_i,\ P_j
$$

↓

计算：

$$
r_{ij}
$$

↓

计算 Jacobian：

$$
J_{T_i},J_{P_j}
$$

↓

构造：

$$
H=J^TWJ
$$

和：

$$
b=J^TWr
$$

↓

求：

$$
H\Delta X=-b
$$

↓

更新：

$$
T_i
$$

和：

$$
P_j
$$

↓

重新 linearize。 所以 BA 本身没有新的优化理论。

它最特别的地方是：

如何利用 BA 特有的矩阵结构

## Schur Complement 的推导与解释

### 11. 先看看 Hessian 长什么样

把 State 分成两部分：

$$
X= \begin{bmatrix} x_c\\ x_p \end{bmatrix}
$$

其中：

$$
x_c = \text{all camera poses}
$$

$$
x_p = \text{all 3D points}
$$

那么 Hessian：

$$
H= \begin{bmatrix} H_{cc} & H_{cp}\\ H_{pc} & H_{pp} \end{bmatrix}
$$

对应线性系统：

$$
\begin{bmatrix} H_{cc} & H_{cp}\\ H_{pc} & H_{pp} \end{bmatrix} \begin{bmatrix} \Delta x_c\\ \Delta x_p \end{bmatrix} = - \begin{bmatrix} b_c\\ b_p \end{bmatrix}
$$

### 12. 这里最大的变量是谁？

通常：

$$
M\gg N
$$

MapPoints 数量远多于 Camera Poses。

比如：

$$
100
$$

个 Keyframes，

但：

$$
10000
$$

个 MapPoints。

所以：

$$
x_p
$$

远大于：

$$
x_c
$$

如果直接解整个系统，会比较贵。

于是我们自然会问：

> 能不能先把大量 Landmark variables 消掉？

答案就是：

Schur Complement

### 13. Schur Complement 的目标

原系统：

$$
H_{cc}\Delta x_c + H_{cp}\Delta x_p = -b_c
$$

第二行：

$$
H_{pc}\Delta x_c + H_{pp}\Delta x_p = -b_p
$$

从第二式先解：

$$
\Delta x_p = -H_{pp}^{-1} (b_p+H_{pc}\Delta x_c)
$$

然后代回第一式。

### 14. 代回去

第一式：

$$
H_{cc}\Delta x_c + H_{cp}\Delta x_p = -b_c
$$

代入：

$$
\Delta x_p = -H_{pp}^{-1} (b_p+H_{pc}\Delta x_c)
$$

得到：

$$
H_{cc}\Delta x_c - H_{cp}H_{pp}^{-1} (b_p+H_{pc}\Delta x_c) = -b_c
$$

整理：

$$
\left( H_{cc} - H_{cp}H_{pp}^{-1}H_{pc} \right) \Delta x_c = - b_c + H_{cp}H_{pp}^{-1}b_p
$$

定义：

$$
S = H_{cc} - H_{cp}H_{pp}^{-1}H_{pc}
$$

这就是：

Schur Complement

### 15. 为什么这有用？

原来需要同时求：

$$
Camera + Points
$$

现在变成：

先只求 Camera Poses

得到：

$$
\Delta x_c
$$

以后，

再回代得到：

$$
\Delta x_p
$$

也就是：

```
Huge BA system
    ↓
Eliminate landmarks
    ↓
Solve pose-only system
    ↓
Recover landmark updates
```

这非常适合 BA，

因为：

MapPoints 很多，Poses 相对少

### 16. 可是 $$H_{pp}^{-1}$$ 不也很大吗？

这是关键。

看起来：

$$
H_{pp}
$$

对应几万个 landmarks， 好像求 inverse 很恐怖。

但 BA 有一个非常特殊的性质：

> 不同 landmarks 之间通常没有直接 measurement factor。

例如 observation 是：

$$
Camera_i\leftrightarrow Point_j
$$

而不是：

$$
Point_j\leftrightarrow Point_k
$$

所以：

$$
H_{pp}
$$

基本是：

Block Diagonal

### 17. $$H_{pp}$$ 长这样

假设三个 landmarks：

$$
P_1,P_2,P_3
$$

每个 3D。

那么：

$$
H_{pp} = \begin{bmatrix} H_{P_1} & 0 & 0\\ 0 & H_{P_2} & 0\\ 0 & 0 & H_{P_3} \end{bmatrix}
$$

每一个：

$$
H_{P_i}
$$

只是：

$$
3\times3
$$

矩阵。

所以：

$$
H_{pp}^{-1}
$$

根本不需要反一个巨大 dense matrix。

只需要分别处理：

$$
3\times3
$$

的小 block。 这就便宜很多。

### 18. 为什么 Landmark block 互相独立？

因为一个 reprojection factor：

$$
r_{ij}
$$

只连接：

$$
T_i
$$

和：

$$
P_j
$$

没有 measurement 同时直接连接：

$$
P_j,P_k
$$

因此 Hessian 中：

$$
\frac{\partial^2E} {\partial P_j\partial P_k}
$$

通常为 0。 所以 MapPoint 部分天然 block diagonal。 这就是 Schur Complement 在 BA 中异常有效的根本原因。

### 19. Schur Complement 的物理意义是什么？

如果只看代数，很容易觉得它只是矩阵技巧。 其实它有一个清晰的图解释。

假设一个 Landmark：

$$
P
$$

被三个 Camera 看到：

```
C1 ── P
C2 ── P
C3 ── P
```

原本三个 Camera 之间没有直接边。

但是把：

$$
P
$$

消元以后，

会产生：

```
C1 ─── C2
 \     /
  \   /
    C3
```

也就是说：

> Landmark 被消掉以后，它携带的信息会变成 Camera 之间的间接约束。

这就是 Schur Complement 的深层含义。

### 20. 一个 Landmark 其实在“绑定多个 Camera”

假设同一个 3D point 被：

$$
C_1,C_2,C_3
$$

看到。

它意味着：

> 这三个 Camera Pose 必须共同解释同一个世界点。

所以这个 landmark 本身就是多个 Camera 之间的桥。 消掉 landmark 并不等于丢掉它的信息。

而是：

把 Landmark information 压缩成 Pose-Pose relation 这非常重要。

### 21. 这和 Marginalization 很像

你有没有发现一个熟悉的模式？

我们把一个变量：

$$
P
$$

消掉， 但保留它对其他变量的影响。

这和以后 Sliding Window 中：

Marginalize old states 思想非常相似。

都是：

Remove variable, keep information 只是数学细节和使用场景不同。

### 22. BA 中的 Schur Complement 可以理解成一种“消元”

从图的视角：

```
Pose — Landmark — Pose
```

消去 Landmark：

```
Pose — Pose
```

所以 optimization 中：

Variable Elimination 和 graph structure 有非常紧密的联系。 这也是后面 Factor Graph 会继续讲的核心。

### 23. 那为什么不干脆一开始就不要 Landmark？

很好的问题。 如果最终都要消掉 MapPoint， 为什么不直接只做 Pose Graph？

因为视觉 measurement 原本就是：

$$
3D\ Point \leftrightarrow 2D\ Pixel
$$

Landmark 是真实 measurement model 的一部分。

BA 能同时调整：

$$
Structure + Motion
$$

所以精度通常更高。

Pose Graph 则是把很多低层 visual measurements：

压缩成 Pose-Pose Constraint 它计算更轻， 但损失了一部分原始信息。

### 24. BA 和 Pose Graph 可以这样对比

BA：

```
Camera --- Landmark
Camera --- Landmark
Camera --- Landmark
```

保留原始 observation level。

Pose Graph：

```
Pose ---- Pose ---- Pose
```

直接使用相对 Pose constraints。

所以：

BA 更细粒度

而：

Pose Graph 更粗粒度、更轻量

## 局部／全局 BA 与坐标基准

### 25. Local BA 与 Global BA

Chapter 41 已经提过。 现在正式区分。

#### Local BA

只优化当前附近：

$$
KFs_{local}+Points_{local}
$$

其他外围 Pose 固定。

优点：

$$
fast
$$

适合实时运行。

#### Global BA

优化：

$$
all\ Keyframes + all\ MapPoints
$$

精度更高， 但计算更贵。 通常不会每一帧都做。

### 26. Global BA 什么时候会做？

典型情况：

- 初始化后 refine
- Loop Closure 后
- 离线优化
- 地图规模还不大时

因为 Loop Closure 会提供一个强烈的新全局约束， 此时历史 trajectory / landmarks 都可能需要重新调整。

### 27. Local BA 为什么可以只优化附近？

因为新加入的 measurement 大多数连接：

current KF

与：

$$
nearby\ KFs / Points
$$

对非常远的状态影响通常通过很多层间接传播。

所以实时阶段先修好局部：

Most useful improvement per unit computation 这就是 Local BA。

### 28. Fixed Keyframes 在 Local BA 里非常重要

假设 local variables：

$$
T_5,T_6,T_7
$$

还有外围：

$$
T_4,T_8
$$

那么可以固定：

$$
T_4,T_8
$$

优化中间：

```
T4(fixed) -- T5 -- T6 -- T7 -- T8(fixed)
```

这样 local map 会继续和 global map 保持一致。 否则局部整体可能漂。

### 29. Gauge Freedom 在 BA 里再次出现

如果你做 Global BA：

$$
T_1,\dots,T_N
$$

和：

$$
P_1,\dots,P_M
$$

全部都是 variables， 却一个 Pose 都没固定，

那么整个 reconstruction 可以整体做：

$$
SE(3)
$$

变换而 reprojection 不变。

单目情况下甚至还有：

$$
Scale
$$

所以必须：

Fix Gauge

例如：

$$
T_1=I
$$

### 30. Monocular BA 还有 Scale 问题

如果是纯单目 BA：

$$
T_i
$$

和：

$$
P_j
$$

全部同时乘一个 scale：

$$
s
$$

投影仍然可能一样。

所以 reconstruction 只有：

up to scale 这还是 Chapter 39 的内容。 BA 本身无法凭空创造 metric scale。

## 投影 Jacobian、初值与异常观测

### 31. Reprojection Error 真的合理吗？

非常合理。

因为 Camera 真正测量的是：

$$
Pixel
$$

所以 prediction：

$$
\hat z=\pi(TP)
$$

应该与实际：

$$
z
$$

比较。

这意味着 BA 优化的是：

Measurement space consistency 而不是直接最小化一个人为构造的 3D distance。

### 32. 为什么不直接比较两个 triangulated 3D point？

比如同一个点在两个 Camera 都能估深度，

为什么不比较：

$$
P_1-P_2
$$

？

可以，但深度 uncertainty 往往：

- 非线性
- anisotropic
- 远距离很差

而 image measurement 的 noise 往往更容易建模成：

$$
\sim 1\ pixel
$$

所以对普通 monocular/multi-view geometry 来说， reprojection residual 更自然。

### 33. 一个 Observation 的 Jacobian 是怎么来的？

Residual：

$$
r = z-\pi(TP)
$$

要对 Pose 和 Point 求导。 可以用 chain rule。

先：

$$
P_c = TP_w
$$

然后：

$$
p=\pi(P_c)
$$

于是：

$$
\frac{\partial r}{\partial P_w} = - \frac{\partial \pi}{\partial P_c} \frac{\partial P_c}{\partial P_w}
$$

Pose 也类似：

$$
\frac{\partial r}{\partial \delta\xi} = - \frac{\partial \pi}{\partial P_c} \frac{\partial P_c}{\partial \delta\xi}
$$

所以：

$$
\boxed{ Geometry + Chain Rule }
$$

就能得到 BA Jacobian。

### 34. Projection Jacobian 长什么样？

假设：

$$
P_c= [X,Y,Z]^T
$$

投影：

$$
u=f_x\frac{X}{Z}+c_x
$$

$$
v=f_y\frac{Y}{Z}+c_y
$$

那么：

$$
\frac{\partial u}{\partial X} = \frac{f_x}{Z}
$$

$$
\frac{\partial u}{\partial Z} = -\frac{f_xX}{Z^2}
$$

同理：

$$
\frac{\partial v}{\partial Y} = \frac{f_y}{Z}
$$

$$
\frac{\partial v}{\partial Z} = -\frac{f_yY}{Z^2}
$$

于是：

$$
J_\pi = \begin{bmatrix} \frac{f_x}{Z} & 0 & -\frac{f_xX}{Z^2}\\ 0 & \frac{f_y}{Z} & -\frac{f_yY}{Z^2} \end{bmatrix}
$$

### 35. 这个 Jacobian 透露了什么？

注意里面有：

$$
\frac{1}{Z}
$$

和：

$$
\frac{1}{Z^2}
$$

当：

$$
Z
$$

很大时， Jacobian 变小。

也就是说：

> 远距离点的位置发生变化，对 image projection 的影响很小。

所以远点 depth 很难估。

这就是之前讲：

Weak Observability 的数学表现。

### 36. 远点对 Rotation 有时仍然很有用

虽然远点对 translation / depth 信息弱， 但 Camera rotation 会明显改变它在图像中的位置。

所以远景 feature 对：

Rotation 可能仍然非常有价值。

这也是为什么：

不同 landmarks 对不同 state directions 提供的信息不同 不能只看 point 数量。

### 37. BA 为什么对初始化敏感？

因为 projection 是 nonlinear。

如果：

$$
Pose
$$

初始错误很大，

预测 projection：

$$
\hat z
$$

可能距离真实 observation 很远。

甚至错到：

> 对应 feature 都找错了。

此时 local linearization 很难救回来。

所以 BA 更像：

Refinement

而不是：

> 从完全随机状态里找到真实世界。

### 38. 所以完整 pipeline 是什么？

不是：

```
Images
↓
BA
↓
done
```

而通常是：

```
Images
↓
Feature / Tracking
↓
Geometry / PnP / Triangulation
↓
Initial poses + landmarks
↓
Bundle Adjustment
↓
Refined poses + landmarks
```

BA 的作用是把一个已经大概正确的 reconstruction：

$$
\boxed{ 变得全局/局部更自洽 }
$$

### 39. Data Association 错了，BA 能自己发现吗？

有时 residual 很大，可以：

- robust kernel 降权
- outlier rejection 删除

但不要期待 BA 自动解决所有 association。 如果错误 association 本身几何上也能形成一个低 residual 解， optimizer 可能非常开心地收敛到错误结果。

所以：

BA optimizes correspondences; it does not fundamentally discover identity 前端 Data Association 仍然非常关键。

### 40. Robust BA

实际 BA 通常不会直接：

$$
\sum r^2
$$

而是：

$$
\sum \rho \left( r^T\Omega r \right)
$$

其中：

$$
\rho
$$

可能是：

- Huber
- Cauchy

防止错误 observations 破坏整个 solution。

### 41. 为什么还要做 Outlier Removal？

Robust kernel 只是：

> 降低 outlier 的影响。

如果一个 observation 已经非常明显错误， 保留它仍然浪费计算。

所以常见做法：

第一轮优化：

Robust Kernel

↓

检查 reprojection error：

$$
\chi^2
$$

↓

标记 outliers

↓

第二轮：

> 删除/忽略 outlier，再优化。

这是很常见的工程模式。

### 42. $$\chi^2$$ 检验是什么直觉？

如果：

$$
r^T\Sigma^{-1}r
$$

非常大，

说明：

> 这个 residual 相对于它理论上的 noise 大得不正常。

例如 sensor 正常误差：

$$
1\ pixel
$$

但 residual：

$$
20\ pixels
$$

那它很可能不是普通 noise，

而是：

- mismatch
- dynamic point
- bad landmark

所以可以作为 outlier criterion。

### 43. BA 后为什么地图会“收缩”或者“展开”？

因为之前各个 MapPoints 可能由局部 triangulation 得到。 每个局部 estimate 都有误差。

BA 把：

multiple views 一起考虑，

会重新调整：

- Camera Poses
- Landmark positions

所以整个地图可能发生细微的整体形变。 这是正常的。

### 44. Loop Closure 后为什么 BA 变化更明显？

假设轨迹因为 drift：

```
start ●

       trajectory

                  ● end
```

实际 end 应该接近 start。

Loop closure 加入约束后：

$$
T_{end}\approx T_{start}
$$

轨迹会整体重新调整。 如果随后执行 Global BA， MapPoints 也会一起移动。

于是：

$$
\boxed{ trajectory + structure }
$$

共同重新变得一致。

### 45. 但大型系统 Loop Closure 后不一定立刻 Global BA

因为 Global BA 很贵。

有些实时系统会先：

Pose Graph Optimization 快速修正 Keyframe poses。 然后把 MapPoints 跟着所属 Keyframe 变换。 之后如果计算预算允许， 再做 Global BA。

这是典型：

Coarse global correction  →  Fine BA

### 46. 为什么 Pose Graph 比 BA 快？

BA 的状态：

$$
Poses + Thousands/Millions\ of\ Points
$$

Pose Graph：

Poses only 变量数量少很多。 所以 global correction 特别适合先用 Pose Graph。 后面 Chapter 45 会详细讲。

## 消元顺序、Fill-in 与方法边界

### 47. Schur Complement 再深入一点

我们刚才说：

$$
S = H_{cc} - H_{cp}H_{pp}^{-1}H_{pc}
$$

这里的：

$$
S
$$

叫 reduced camera matrix。

它把所有 landmark information：

压缩进 Camera-Pose system

然后求：

$$
S\Delta x_c = \tilde b
$$

### 48. Reduced Camera Matrix 会更 dense 吗？

会。 这是一个重要现象。

原来：

```
Camera 1 --- Point A --- Camera 2
```

没有直接 Camera-Camera edge。

消掉 Point A 后：

```
Camera 1 -------- Camera 2
```

所以 Schur elimination 会产生：

fill-in 也就是原本为 0 的矩阵位置变成非零。

### 49. Fill-in 为什么重要？

如果一个 landmark 被很多 Cameras 同时看到：

```
    C1
     \
C2 -- P -- C3
     /
    C4
```

把：

$$
P
$$

消掉以后：

$$
C1,C2,C3,C4
$$

之间会形成大量联系。 所以 reduced Hessian 会变得更 dense。

这意味着：

Variable elimination order 非常重要。

### 50. 为什么“先消 Landmark”通常合理？

因为 landmarks：

- 数量很多
- 每个维度小
- $$H_{pp}$$ block diagonal
- 很容易独立消元

如果反过来先消 Cameras， 可能会在 landmark 之间制造巨量 fill-in。

所以 BA 的自然结构决定：

Eliminate points first 这就是 Schur BA 的核心。

### 51. 这和 Factor Graph 的 elimination order 是同一类问题

Factor Graph 求解中，也会问：

> 哪个 variable 先消？

因为不同顺序会产生不同程度：

fill-in 从而极大影响计算量。

所以 BA 的 Schur Complement 其实是：

一种特别针对 Camera-Landmark bipartite graph 的高效 elimination strategy 后面 Chapter 44 会继续把这个思想泛化。

### 52. BA 的 Graph 长什么样？

它本质是一个二部图：

```
Camera nodes:   C1    C2    C3
                 \   / \   /
                  \ /   \ /
Point nodes:      P1    P2
```

一边：

Camera Poses

另一边：

Landmarks

边：

Observation

这种结构叫：

Bipartite Graph BA 的数学稀疏结构直接来自这张图。

### 53. 所以“图”和“矩阵”不是两件事

这是一个非常重要的思想。

Graph：

```
C1 -- P1 -- C2
```

意味着 Jacobian / Hessian 中：

> C1 与 P1 有非零 block，

> C2 与 P1 有非零 block。

也就是说：

Graph topology  ↔  Matrix sparsity 这句话你后面学 Factor Graph 时会反复看到。

### 54. Observation 越多越好吗？

仍然不一定。

假设同一个 Camera 和同一个平面上有：

$$
10000
$$

个非常相似 points。 可能信息高度冗余。

真正决定 BA conditioning 的还有：

- viewing geometry
- depth
- baseline
- point distribution
- uncertainty

所以：

More residuals  ≠  proportionally more information

### 55. BA 能估 Camera Intrinsics 吗？

可以。 这就是 BA 很强的地方。

你可以把：

$$
f_x,f_y,c_x,c_y
$$

甚至 distortion parameters：

$$
k_1,k_2,p_1,p_2
$$

也放进 State。

Residual 仍然：

$$
z-\pi(T,P,K,D)
$$

于是可以一起优化：

$$
Pose + Point + Intrinsics
$$

这在：

- SfM
- Camera calibration
- offline reconstruction

很常见。

### 56. 为什么在线 SLAM 通常不随便优化所有东西？

因为 State 越多：

- 计算更贵
- observability 更复杂
- 参数之间更容易耦合

例如同时在线估：

$$
Pose + Landmark + Intrinsics + TimeOffset + Extrinsics
$$

如果运动激励不足， 很容易出现弱可观方向。

所以：

> 能估，不代表应该随时估。

这又回到了 observability。

### 57. 一个简单例子：焦距和深度可能耦合

投影：

$$
u=f\frac{X}{Z}
$$

如果：

$$
f
$$

和：

$$
Z
$$

都未知， 某些有限 motion 条件下， 二者可能互相补偿。

也就是：

$$
f\uparrow
$$

同时：

$$
Z\uparrow
$$

仍然可能产生类似 projection。 如果 motion/scene 信息不足， 这两个 state 就会强耦合。 所以自标定并不是“把参数加到 optimizer 就完事”。

### 58. BA 输出 uncertainty 吗？

理论上，在 optimum 附近：

$$
H
$$

近似 information matrix。

因此：

$$
H^{-1}
$$

与 covariance 有联系。

但大型 BA 一般不会真的把整个：

$$
H^{-1}
$$

算出来。 因为代价太高。 如果需要某些 state 的 marginal covariance， 可以用更专门的方法计算。

### 59. BA 和 EKF-SLAM 的一个清晰的对比

EKF-SLAM：

> 每来 measurement，立即更新整个 joint distribution。

BA：

> 保存很多 observations，然后一起重新优化历史 states。

所以：

EKF →  Filtering BA →  Smoothing

BA 允许未来 measurement：

$$
z_t
$$

直接修正过去：

$$
T_{t-50}
$$

和过去 landmarks。 这就是 smoothing 的力量。

### 60. 为什么 BA 常常比纯 Filtering 精度高？

因为 BA 保留更多原始历史 information。

EKF 会不断把历史压缩进：

$$
\mu,P
$$

而且每一步做一次 linearization。 一旦过去的 linearization 被固定下来， 后面不一定能完全重新修正。

BA 则可以：

> 在新的估计点重新 linearize 过去的 measurements。

所以对于高度 nonlinear 的 SLAM：

Repeated relinearization 通常很有价值。

### 61. 但代价就是计算量

Filtering：

online, compact

Smoothing/BA：

more accurate, more expensive

所以工程系统一直在做平衡：

- Sliding Window
- Local BA
- Keyframe
- Marginalization

本质都是：

在 Filtering 和 Full Smoothing 之间找平衡

### 62. Full BA 和 Fixed-Lag Smoothing

Full BA：

$$
x_0,\dots,x_t
$$

全保留。

Fixed-Lag：

只保留最近：

$$
x_{t-k},\dots,x_t
$$

旧状态 marginalize 掉。 这就是现代 VIO 很常见的模式。 所以 BA 的思想并不限于“纯视觉”。

### 63. BA 在 SfM 中也极其重要

Structure from Motion：

$$
Images \rightarrow Camera\ Poses + 3D\ Structure
$$

和 Visual SLAM 非常像。

区别主要是：

SfM 通常：

- 离线
- 不强调实时
- 可以反复全局优化

SLAM：

- 在线
- 必须实时
- 要处理 tracking / loop / map maintenance

但核心 geometric optimization：

Bundle Adjustment 是共享的。

### 64. 一个真正的 BA 系统流程

大概是：

```
Initial Poses + Landmarks
        ↓
Build observations
        ↓
Compute reprojection residuals
        ↓
Apply robust loss
        ↓
Linearize
        ↓
Build block sparse Hessian
        ↓
Schur eliminate landmarks
        ↓
Solve camera increments
        ↓
Back-substitute point increments
        ↓
Update poses and points
        ↓
Re-linearize
        ↓
Repeat
```

这就是你应该在脑子里形成的完整 BA computational picture。

### 65. Schur Complement 用一句人话再说一次

如果你最后只想保留一句：

> 地图点虽然数量巨大，但每个点只和少量相机相连，所以我们可以先把地图点从方程里“消掉”，把它们包含的信息转成相机之间的约束，只解更小的相机系统，最后再把地图点更新算回来。

这就是：

Schur Complement in Bundle Adjustment

### 66. 这章最重要的知识链

从 measurement：

$$
z_{ij}
$$

到 residual：

$$
r_{ij} = z_{ij} - \pi(T_iP_j)
$$

到 Jacobian：

$$
J_{pose},J_{point}
$$

到 Hessian：

$$
H= \begin{bmatrix} H_{cc}&H_{cp}\\ H_{pc}&H_{pp} \end{bmatrix}
$$

再利用：

$$
H_{pp}
$$

block diagonal，

进行：

Schur Complement

最后只解：

Camera Pose 系统。 这就是整章的数学主线。

### 67. 本章最重要的七句话

第一：

$$
\boxed{ BA = jointly optimize camera poses and 3D landmarks }
$$

第二：

$$
\boxed{ Residual = Reprojection\ Error }
$$

第三：

BA 的 Hessian 天然具有：

Block Sparse Structure

第四：

Landmark-landmark 部分：

$$
H_{pp}
$$

通常：

Block Diagonal

第五：

Schur Complement 可以：

先消掉 Landmarks，只求 Poses

第六：

消掉 Landmark 并不是丢掉信息，而是：

把 Landmark information 转成 Pose-Pose information

第七：

Graph structure  ↔  Matrix sparsity 这句话将直接带我们进入 Factor Graph。

> 修订说明：Schur Complement 中 H_pp⁻¹ 要求被消元的地图点块可逆；缺乏视差等情况需先筛点、阻尼或秩处理，不能机械求逆。临时消元并回代仍在当前线性化问题中求联合更新；永久边缘化则通常固定历史线性化信息，二者不能等同。局部信息与协方差也需处理 gauge。

### Jacobian 的符号与位姿约定

设 s = T_iP_j，采用相机系左扰动，δs ≈ [I,−s^∧]δξ。草稿定义残差 r = z − π(s)，故由链式法则：

$$
J_T=-J_\pi[I\; -s^\wedge],\qquad J_P=-J_\pi R_i.
$$

二者维度分别为 2×6、2×3。若定义预测减观测，两个 Jacobian 的符号同时改变；实现必须与残差一致。

## 思考题

### Q1：为什么 BA 不应该只优化 Camera Pose？

<details>

<summary>参考答案</summary>

因为 Landmark 本身通常也是由 noisy triangulation 得来的。

如果把 Landmark 固定：

> 它自己的误差会被迫全部由 Camera Pose 承担。

Joint optimization 可以让：

$$
Pose
$$

和：

Structure 共同找到更一致的解。

</details>

### Q2：为什么 Landmark 多很多，BA 却还能做？

<details>

<summary>参考答案</summary>

因为不同 landmarks 没有直接连接，

所以：

$$
H_{pp}
$$

是 block diagonal。

可以高效地用：

Schur Complement 先消掉它们， 把问题缩成 Pose-only system。

</details>

### Q3：Schur Complement 把 Landmark 删除后，它的信息是不是没了？

<details>

<summary>参考答案</summary>

不是。

Landmark 原来连接：

$$
C_1,C_2,C_3
$$

消元后会在这些 Cameras 之间形成等价信息约束。

所以是：

information compression 不是 information deletion。

</details>

### Q4：为什么一个 Landmark 被越多 Camera 看到，消元后可能产生越多 fill-in？

<details>

<summary>参考答案</summary>

因为这个 Landmark 把所有观察它的 Cameras 联系在一起。

假设被：

$$
K
$$

个 Camera 看到， 消掉它后这些 Camera 之间会形成更密集的关系。 所以连接度越高，潜在 fill-in 越多。

</details>

### Q5：为什么 BA 不能解决严重错误的 Data Association？

<details>

<summary>参考答案</summary>

因为 BA 默认给定：

> 哪个 observation 属于哪个 Landmark。

它主要优化连续变量：

Pose, Point 如果离散对应关系本身错了， 优化器可能会努力满足一个错误约束。 所以 association 必须主要由前端解决。

</details>

### Q6：为什么远距离 MapPoint 对 Translation 约束通常比较弱？

<details>

<summary>参考答案</summary>

投影 Jacobian 中有：

$$
\frac1Z,\frac1{Z^2}
$$

当：

Z →  large 时， translation / depth 变化对 pixel 的影响变小。 所以 measurement information 变弱。

</details>

### Q7：为什么 Local BA 比 Global BA 更适合实时 SLAM？

<details>

<summary>参考答案</summary>

因为新 measurement 主要影响当前附近状态。

Local BA 只处理：

$$
Active\ Keyframes + Local\ Points
$$

可以获得大部分精度收益， 而避免每一帧都优化整张地图。

</details>

### Q8：BA 和 EKF-SLAM 最重要的区别是什么？

<details>

<summary>参考答案</summary>

EKF-SLAM：

Filtering 持续把历史压进当前 joint Gaussian。

BA：

Smoothing 保留多个历史 states 和 observations， 可以重新 linearize、重新修正过去。

</details>

## 相关章节与来源

- 上一章：[非线性最小二乘](nonlinear-least-squares.md)
- 下一篇：[Factor Graph](factor-graphs.md)
- 来源：本次新增 Part IV Chapter 43 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
- 核验参考：[Ceres：Schur 求解器](https://ceres-solver.readthedocs.io/latest/nnls_solving.html)。
