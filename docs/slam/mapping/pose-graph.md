---
title: Pose Graph Optimization
description: 相对位姿约束怎样修正全局轨迹，并处理错误回环？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 45
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# Pose Graph Optimization

## 本章目标

相对位姿约束怎样修正全局轨迹，并处理错误回环？

## 前置知识

[SE(3)](../spatial/se3.md)、[Factor Graph](factor-graphs.md)、[Bundle Adjustment](bundle-adjustment.md)。

## 定义与假设

Gaussian 噪声、局部线性化和固定数据关联都是建模条件；相应推导只在这些条件下适用。三维位姿采用 SE(3)，局部扰动按 [δρ,δφ] 排列，平移用 m、旋转用 rad。Exp 输入六维向量时表示先经 hat 映射再取矩阵指数，Log 输出六维坐标；左右更新需与残差和 Jacobian 一致。 T_i 是节点坐标系到世界系的位姿；Z_ij 将 j 系映射到 i 系，预测为 T_i⁻¹T_j。六维残差的协方差／信息矩阵必须使用相同误差坐标与单位。

## 核心问题


先给你一句最核心的话：

$$
\boxed{ Pose\ Graph = 用相对位姿约束，优化整条机器人轨迹 }
$$

## 节点、边与 SE(3) 残差

### 1. 为什么需要 Pose Graph？

假设机器人一直靠 odometry 往前走：

```
x0 ---- x1 ---- x2 ---- x3 ---- x4
```

每一段 odometry 都有一点误差：

$$
z_{01},z_{12},z_{23},z_{34}
$$

即使每一步误差很小，

长期累计以后：

Drift 会越来越明显。

比如真实轨迹应该绕一圈回到起点：

```
┌────────┐
│        │
│        │
└────────┘
```

但估计出来变成：

```
┌─────────
│
│
└──────────●
```

终点没有闭上。

### 2. Loop Closure 给我们什么？

假设机器人最后发现：

> “我现在看到的地方，就是一开始的位置。”

那么得到一个新的相对位姿约束：

$$
z_{0N}
$$

表示：

$$
x_N
$$

和：

$$
x_0
$$

之间应该满足某种关系。 如果真的是回到起点，

可能近似：

$$
T_0^{-1}T_N\approx I
$$

于是图变成：

```
x0 ---- x1 ---- x2 ---- x3 ---- x4
|                             |
└--------- loop --------------┘
```

这条新边会暴露之前积累的 drift。

### 3. Pose Graph 的 Node 是什么？

每个节点：

$$
T_i\in SE(3)
$$

代表某一个关键帧或者机器人状态的 Pose。

二维情况可能是：

$$
x_i= [x_i,y_i,\theta_i]
$$

三维则：

$$
T_i= \begin{bmatrix} R_i&t_i\\ 0&1 \end{bmatrix}
$$

所以：

$$
\boxed{ Node = Pose }
$$

### 4. Edge 是什么？

Edge 表示两个 Pose 之间的相对位姿 measurement。

例如：

$$
Z_{ij}
$$

表示 sensor / front-end 告诉我们：

> 从 $$i$$ 到 $$j$$ 的相对变换应该大概是这个。

预测值：

$$
\hat Z_{ij} = T_i^{-1}T_j
$$

所以 measurement 和 prediction 可以比较。

### 5. Pose Graph Residual 怎么写？

一个常见形式：

$$
r_{ij} = \operatorname{Log} \left( Z_{ij}^{-1} T_i^{-1} T_j \right)
$$

不要先被这个公式吓到。 我们把它拆开。

### 6. $$T_i^{-1}T_j$$ 是什么？

它表示：

> 按照当前优化状态，从 Pose $$i$$ 到 Pose $$j$$ 的预测相对运动。

也就是：

$$
\hat Z_{ij} = T_i^{-1}T_j
$$

### 7. $$Z_{ij}^{-1}\hat Z_{ij}$$ 是什么？

Measurement：

$$
Z_{ij}
$$

Prediction：

$$
\hat Z_{ij}
$$

如果两者完全一样：

$$
Z_{ij}^{-1}\hat Z_{ij}=I
$$

所以这个量表示：

> prediction 相对于 measurement 还差多少。

### 8. 为什么还需要 Log？

因为：

$$
Z_{ij}^{-1}T_i^{-1}T_j
$$

仍然是：

$$
SE(3)
$$

里的一个刚体变换。 但 least squares 喜欢普通向量。

所以通过：

$$
\operatorname{Log}:SE(3)\rightarrow\mathfrak{se}(3)
$$

把它变成一个 6D residual：

$$
r_{ij}\in\mathbb R^6
$$

包含：

- 3D translation error
- 3D rotation error

所以可以简单理解：

$$
\boxed{ Log = 把“位姿差”转换成可以优化的六维小量 }
$$

### 9. 整个 Pose Graph 的优化目标

假设所有 edge 集合：

$$
\mathcal E
$$

那么：

$$
\boxed{ \min_{\{T_i\}} \sum_{(i,j)\in\mathcal E} r_{ij}^T \Omega_{ij} r_{ij} }
$$

其中：

$$
\Omega_{ij} = \Sigma_{ij}^{-1}
$$

表示这条相对 pose measurement 的可信度。 这和我们之前的所有 least squares 完全一样。

## 轨迹冲突与 BA 的区别

### 10. Pose Graph 有哪两类最重要的 Edge？

第一类：

Odometry Edge

连接时间上相邻的 Pose：

```
x0 -- x1 -- x2 -- x3
```

来源可能是：

- wheel odometry
- visual odometry
- lidar odometry
- VIO

第二类：

Loop Closure Edge

连接时间上很远，但空间上重新相遇的 Pose：

```
x0 -- x1 -- x2 -- x3 -- ... -- x100
|                                  |
└------------- loop ---------------┘
```

这类 Edge 对长期 drift 特别重要。

### 11. 为什么 Odometry 会漂，而 Loop Closure 可以拉回来？

Odometry 主要提供局部关系：

$$
T_i^{-1}T_{i+1}
$$

每一步都有小误差。

于是：

$$
T_0\rightarrow T_1\rightarrow T_2\rightarrow\dots
$$

误差层层累积。

Loop Closure 则提供一个长距离 constraint：

$$
T_0^{-1}T_N
$$

它会告诉系统：

> 你这一整圈累计出来的结果和真实几何关系不一致。

于是 optimizer 会把误差重新分配到整条轨迹。

### 12. “拉回来”不是只改最后一帧

这是一个非常重要的点。

假设终点误差：

$$
1m
$$

最简单粗暴的想法：

> 把最后一个 Pose 往回挪 1m。

但这不合理。

因为 drift 是：

整个轨迹逐渐积累 出来的。

所以优化会调整：

$$
x_1,x_2,\dots,x_N
$$

让所有 constraints 综合最小。

结果可能像：

```
before:

x0 ---- x1 ----- x2 ------ x3 -------- x4

after:

x0 --- x1 --- x2 --- x3 --- x4
|                         |
└---------- loop ----------┘
```

误差被平滑地分布到多个 Pose。

### 13. 为什么不是平均分配？

因为每条 edge 的 uncertainty 不一样。

例如：

$$
\Sigma_{01}
$$

很小，说明：

> x0→x1 很可信。

而：

$$
\Sigma_{23}
$$

比较大，

说明：

> x2→x3 不太可信。

那么 optimizer 更愿意修改后者。

所以：

Error distribution follows information 不是简单平均。

### 14. 一个 1D 小例子

假设：

$$
x_0=0
$$

odom measurements：

$$
x_1-x_0=1
$$

$$
x_2-x_1=1
$$

$$
x_3-x_2=1.1
$$

所以直接累计：

$$
x_3=3.1
$$

但 loop closure 告诉：

$$
x_3-x_0=3.0
$$

于是存在：

$$
0.1
$$

的 inconsistency。 Optimization 会根据各 measurement 的信息权重， 把这 0.1 的冲突合理分配。 如果第三段 odom 最不可信，

可能主要修改：

$$
x_2\rightarrow x_3
$$

这一段。

### 15. Pose Graph 本质是“约束冲突协调器”

你可以这样理解：

每个 edge 都在对两个 nodes 说：

> “你们之间应该满足这个关系。”

如果所有 edge 完美一致， 那很简单。

但现实中因为 noise：

Constraints are mutually inconsistent

Pose Graph Optimization 的任务就是：

> 找到一套 Poses，让这些互相有点矛盾的约束总体上最自洽。

### 16. 这和 Chapter 37 的 SLAM 本质完全一致

我们最开始说：

$$
\boxed{ SLAM = 找一个最自洽的世界解释 }
$$

Pose Graph 正是这句话最直观的数学实现之一。

### 17. Pose Graph 和 BA 的区别

这是这一章必须真正搞清楚的地方。

BA 的 Variables：

$$
\boxed{ Poses + Landmarks }
$$

Measurements：

Pixel observations

Residual：

$$
z-\pi(TP)
$$

Pose Graph：

Variables：

Poses only

Measurements：

Relative Pose

Residual：

$$
\operatorname{Log} (Z_{ij}^{-1}T_i^{-1}T_j)
$$

所以：

BA 在 observation level 优化

而：

Pose Graph 在 pose-constraint level 优化

### 18. 为什么 Pose Graph 更轻？

假设：

$$
1000
$$

个 Keyframes，

$$
100000
$$

个 MapPoints。

BA variables：

$$
6\times1000 + 3\times100000
$$

大约：

$$
306000
$$

维。

Pose Graph：

$$
6\times1000 = 6000
$$

维。 差距巨大。

所以做全局修正时：

Pose Graph much cheaper

### 19. 但 Pose Graph 的信息从哪里来？

这是一个关键问题。

它的 relative Pose edge：

$$
Z_{ij}
$$

不是凭空来的。

通常是前端通过：

- PnP
- Essential Matrix
- ICP
- Local BA
- VIO
- LiDAR registration

估出来的。

也就是说：

Low-level measurements  →  Relative Pose constraint Pose Graph 是一种更高层的信息压缩。

### 20. 所以 Pose Graph 丢信息了吗？

严格来说：

通常会丢掉一部分原始信息

比如原来 500 个 feature observations：

$$
z_1,\dots,z_{500}
$$

经过视觉前端后，

可能被压缩成：

$$
Z_{ij}
$$

一个 6DoF relative pose measurement。 这样计算大幅变轻， 但原始 pixel-level structure 不再全部保留。

所以：

$$
\boxed{ Pose\ Graph = computationally cheaper but coarser }
$$

### 21. 为什么这仍然很适合 Loop Closure？

因为 Loop Closure 的目标主要是：

Correct global drift 并不一定需要立刻重新优化所有 pixel observations。

只要得到：

Current KF  ↔  Past KF 之间一个可靠相对 Pose， 就足以对整个轨迹做大尺度 correction。

所以 Pose Graph 非常适合：

Global consistency

## 回环验证与尺度

### 22. Loop Closure Edge 怎么产生？

通常流程：

```
Current Keyframe
↓
Place Recognition
↓
Candidate Historical Keyframe
↓
Feature Matching
↓
Geometric Verification
↓
Relative Pose Estimation
↓
Loop Factor
```

注意：

Place Recognition 只负责“怀疑这里来过” 真正加入 Graph 之前， 必须做 geometric verification。

### 23. 为什么不能只靠图像长得像？

比如两个走廊：

```
Corridor A
Corridor B
```

可能长得几乎一样。 Place recognition 可能误判。

如果直接加 loop edge：

$$
x_{100}\leftrightarrow x_{1000}
$$

但其实这两个地方不同， 整个地图可能被拉坏。

所以：

Appearance similarity  ≠  Geometric consistency

### 24. Loop Closure 的 Relative Pose 怎么验证？

典型方法：

如果有 3D MapPoints：

$$
3D-2D
$$

可以：

$$
PnP + RANSAC
$$

如果是两帧 monocular：

$$
2D-2D
$$

可以 Essential Matrix。

如果有 3D points / LiDAR：

$$
3D-3D
$$

可以 registration / ICP。 只有几何上也说得通， 才接受 loop。

### 25. Monocular Loop Closure 为什么常用 Sim(3)？

因为单目 SLAM 会有：

Scale drift

假设早期地图 scale：

$$
1.0
$$

后来慢慢漂成：

$$
1.1
$$

如果 loop closure 只用：

$$
SE(3)
$$

只能修：

- rotation
- translation

不能直接修：

$$
scale
$$

所以一些 monocular systems 使用：

$$
\boxed{ Sim(3) }
$$

变换：

$$
p'=sRp+t
$$

多一个：

$$
s
$$

来修 scale drift。

### 26. Stereo / RGB-D 为什么通常用 SE(3) 就够？

因为它们已经有 metric scale。

Stereo：

$$
Z=\frac{fb}{d}
$$

RGB-D：

直接有 metric depth。 所以 scale 通常不是 gauge freedom。

因此 loop correction 可以用：

$$
SE(3)
$$

## Gauge、稀疏性与位姿更新

### 27. Pose Graph 的 Gauge Freedom

假设只有 relative pose edges：

```
x0 -- x1 -- x2 -- x3
```

把所有 Pose 一起乘一个 global transform：

$$
T_i' = T_gT_i
$$

所有：

$$
T_i^{-1}T_j
$$

都不变。 所以整个 graph 仍然有 global gauge。

因此：

必须固定至少一个 Pose

通常：

$$
T_0=I
$$

### 28. 这就是 Chapter 39 第三次出现

Chapter 39：

> 为什么固定第一帧？

Chapter 42：

> 不固定会让 Hessian singular。

Chapter 45：

> Pose Graph 全是 relative constraints，本身没有 global frame。

同一个问题从三个角度完全闭环了。

### 29. Pose Graph 的 Hessian 为什么 Sparse？

一个 edge：

$$
(i,j)
$$

只涉及：

$$
T_i,T_j
$$

因此 Jacobian 只在两个 Pose blocks 非零。

所以 Hessian 大概是：

```
        x0 x1 x2 x3
x0      ■  ■
x1      ■  ■  ■
x2         ■  ■  ■
x3            ■  ■
```

局部 odometry 形成一个：

banded structure

### 30. Loop Edge 会改变 Hessian 结构

加入：

$$
x_0\leftrightarrow x_3
$$

之后：

```
        x0 x1 x2 x3
x0      ■  ■     ■
x1      ■  ■  ■
x2         ■  ■  ■
x3      ■     ■  ■
```

出现远距离 off-diagonal block。

这就是：

Long-range constraint 在矩阵里的体现。

### 31. 为什么 Loop Closure 会产生“全局影响”？

因为它虽然只增加一条 edge，

但 graph 已经通过 odometry chain 全连接：

$$
x_0-x_1-x_2-\dots-x_N
$$

所以新 constraint 会改变整个线性系统。

最终：

$$
\Delta x_1,\Delta x_2,\dots
$$

都可能非零。

这就是：

Local new measurement, global correction

### 32. Pose Graph 里也可以加 GPS 吗？

当然可以。

GPS Factor：

$$
f_{gps}(T_i)
$$

提供 absolute position。

那么：

```
       GPS
        |
x0 -- x1 -- x2 -- x3
```

这会消除一部分 global gauge， 并把 trajectory 锚定到全球坐标。

### 33. 也可以加多个 Absolute Factors

比如：

- GPS
- map matching
- AprilTag known world pose
- motion capture

这些都是：

$$
\boxed{ Absolute\ Pose/Position\ Factors }
$$

所以 Pose Graph 不一定只有 relative edges。

### 34. Pose Graph Optimization 还是 GN / LM

不要觉得又来了新算法。

流程仍然：

$$
T^{(k)}
$$

↓

计算每个：

$$
r_{ij}
$$

↓

计算 Jacobians

↓

构造：

$$
H,b
$$

↓

解：

$$
H\Delta x=-b
$$

↓

对每个 Pose：

$$
T_i\leftarrow \exp(\delta\xi_i^\wedge)T_i
$$

↓

重复。 所以 Chapter 42 的数学仍然完全有效。

### 35. 为什么 Rotation Error 不能简单相减？

Translation：

$$
t_1-t_2
$$

还比较自然。

但是 Rotation：

$$
R_1-R_2
$$

不是一个合理的旋转误差表示。

因为：

$$
SO(3)
$$

不是普通 Euclidean space。

所以我们通常用：

$$
R_{err} = R_{meas}^{-1} R_{pred}
$$

然后：

$$
\operatorname{Log}(R_{err})
$$

得到三维小旋转向量。 所以 Lie Group 在 Pose Graph 里特别自然。

### 36. 一个二维版本更直观

二维 Pose：

$$
x_i=[p_{xi},p_{yi},\theta_i]
$$

Measurement：

$$
z_{ij} = [\Delta x,\Delta y,\Delta\theta]
$$

预测：

$$
\hat z_{ij}=x_i^{-1}\oplus x_j
$$

Residual：

$$
r_{ij} = z_{ij}\ominus\hat z_{ij}
$$

本质还是：

> 实际相对位姿和预测相对位姿差多少。

### 37. Pose Graph 为什么通常用 Keyframe，而不是每 Frame？

因为 Keyframe 已经对 trajectory 做了一次信息压缩。

如果 30 FPS 一小时：

$$
108000
$$

nodes， Graph 很大。

但如果只保留重要 Keyframes：

$$
3000
$$

nodes， 计算容易很多。

所以：

Keyframe Graph 是很自然的选择。

### 38. 这和 Chapter 41 又连起来了

Chapter 41 的 Keyframe 不只是为了 Local Mapping。

它还在给 Global Optimization 准备：

Trajectory Skeleton Loop Closure 通常在这套 skeleton 上工作。

## 地图修正、鲁棒回环与增量系统

### 39. Pose Graph 优化后 MapPoints 怎么办？

非常关键。

因为 Pose Graph 只优化了：

Keyframe Poses MapPoints 并没有参与优化。 那 Pose 改了以后， 地图点怎么办？

常见做法之一：

> 根据它所属/参考 Keyframe 的 pose correction，把 MapPoint 一起变换。

例如：

$$
T_i^{old} \rightarrow T_i^{new}
$$

MapPoint 相对 Keyframe 的局部坐标保持不变， 然后重新得到世界坐标。

### 40. 这只是近似吗？

通常是。 Pose Graph 给的是一个比较粗的 global correction。 MapPoints 跟随 Pose correction 后， 整体地图已经大体正确。

如果还需要更精确：

Global BA 再重新优化所有 reprojection measurements。

所以常见流程：

Pose Graph  →  Map Correction  →  Optional Global BA

### 41. 为什么不一检测到 Loop 就直接 Global BA？

因为 Global BA 可能非常贵。

尤其大型地图：

$$
10000\ KFs
$$

$$
1M\ MapPoints
$$

实时系统可能根本承受不了。 Pose Graph 只有 Pose variables，

可以更快完成：

global drift correction 所以更适合先做。

### 42. 一个很重要的“粗到细”思想

Loop Closure 之后：

第一步：

$$
\boxed{ Pose\ Graph = coarse global correction }
$$

第二步：

$$
\boxed{ BA = fine geometric refinement }
$$

这和很多 CV 算法：

coarse →  fine 的思想类似。

### 43. Loop Closure 一定能让结果更好吗？

如果 loop 正确：

通常是。

如果 loop 错：

可能灾难性。

所以系统必须面对：

Outlier Loop Constraints 这比普通 feature outlier 更危险。

### 44. 为什么 Loop Outlier 特别危险？

普通 local edge：

$$
x_{20}\leftrightarrow x_{21}
$$

主要影响局部。

错误 loop：

$$
x_{20}\leftrightarrow x_{2000}
$$

跨越整条 trajectory。 它会强迫两个本来完全不同的地方靠在一起。

因此会：

> 扭曲一大片地图。

### 45. Robust Kernel 能解决所有错误 Loop 吗？

不能保证。

Robust kernel 对：

large residual 有效。 但如果一个错误 loop 恰好形成了一个“看似几何合理”的 constraint， 它的 residual 可能并不明显大。

所以真正关键仍然是：

Loop Verification

### 46. Switchable Constraints

为了提高 robustness，有些图优化方法会给 loop edge 加一个额外变量：

$$
s_{ij}
$$

如果 loop 看起来可信：

$$
s\approx1
$$

如果冲突很大：

$$
s\approx0
$$

于是 loop factor 的影响可以被自动关闭。

直觉上：

> 让 optimizer 不仅优化 Pose，还判断“这条 loop edge 值不值得信”。

### 47. Dynamic Covariance Scaling / Robust PGO

还有很多方法会动态调整 loop constraint 的权重。

总体目标都是：

不要让一个错误的长距离约束毁掉整个图 具体算法现在不用深挖。 你先知道

### 48. Pose Graph 也可以做 Multi-Robot SLAM

假设 Robot A：

```
A0 -- A1 -- A2
```

Robot B：

```
B0 -- B1 -- B2
```

如果某时发现：

$$
A_2
$$

和：

$$
B_1
$$

观察到同一个地方，

可以加入 inter-robot loop：

```
A0 -- A1 -- A2
             |
             |
B0 -- B1 -- B2
```

于是两个 trajectory 可以统一到同一图里。 所以 Pose Graph 天然适合多机器人地图融合。

### 49. Pose Graph 和 Topological Map 有点像吗？

有一点结构上的相似。

Pose Graph 的 Node：

$$
Pose
$$

Edge：

Geometric Constraint

Topological Map 也会用：

$$
Place
$$

和：

Connectivity 但 Pose Graph 的 Edge 一般具有精确几何 measurement 和 uncertainty。

所以它更偏：

metric optimization

### 50. 为什么大型机器人系统特别喜欢图结构？

因为机器人世界天然是：

大量局部关系组成全局结构

比如：

- 这一帧和下一帧
- 这个地点和那个地点
- 当前机器人和某个 landmark
- 当前 pose 和 GPS
- robot A 和 robot B

Graph 非常自然地表达这种局部关系。

### 51. Pose Graph 的一个完整流程

我们现在可以完整画出来：

```
Visual/LiDAR/Wheel Odometry
        ↓
Relative Pose Constraints
        ↓
Create Pose Nodes + Odom Edges
        ↓
Trajectory grows
        ↓
Place Recognition
        ↓
Loop Candidate
        ↓
Geometric Verification
        ↓
Loop Edge
        ↓
Pose Graph Optimization
        ↓
Correct Keyframe Trajectory
        ↓
Correct Map
        ↓
Optional Global BA
```

这就是非常经典的 SLAM global backend pipeline。

### 52. 一个具体例子

假设：

$$
100
$$

个 Keyframes。

Odometry Edge：

$$
(0,1),(1,2),...,(98,99)
$$

共：

$$
99
$$

条。

机器人回到起点后检测到：

$$
(0,99)
$$

loop edge。

优化前：

$$
T_{99}
$$

和：

$$
T_0
$$

差：

$$
0.8m
$$

但 loop measurement 表明：

$$
0.05m
$$

左右。 于是 graph 中出现明显 inconsistency。

Optimizer 会调整：

$$
T_1\dots T_{99}
$$

让：

- 相邻 odometry 尽量满足
- loop edge 也尽量满足

最后闭环。

### 53. 如果 Odometry 非常可信会怎样？

假设：

$$
\Omega_{odom}
$$

特别大。 则 optimizer 不愿意改变局部 odometry。 为了满足 loop， 可调整空间很小。 如果 loop information 也非常强， 两者冲突会导致较高 final cost。 所以 uncertainty 设置必须合理。

### 54. 如果 Loop Edge 权重设得太高呢？

系统可能：

> 为了强行满足 loop，把整条 trajectory 扭得过头。

如果太低：

> loop 几乎不起作用。

因此：

Constraint covariance matters 仍然是同一个核心主题。

### 55. Pose Graph Optimization 后 Residual 为 0 吗？

通常不会。

因为现实 measurements：

$$
noisy
$$

甚至互相有轻微冲突。

Optimization 目标不是：

$$
所有 residual=0
$$

而是：

找到整体概率意义上最合理的妥协 这一点非常重要。

### 56. 一个很常见的误区

有人看到优化后某条 edge residual 还存在，

会觉得：

> “Optimizer 没优化好。”

不一定。 可能它就是正确结果。 因为如果完全满足这条 edge， 就会严重违背其他更可信的 edges。 最优解本来就是一个 weighted compromise。

### 57. Pose Graph 与 Smoothing

Pose Graph 保存：

$$
T_0,T_1,\dots,T_N
$$

并一起优化。

所以它仍然属于：

Smoothing 而不是简单 filtering。

未来 loop measurement 可以直接改变过去的：

$$
T_{10}
$$

这就是 smoothing 的典型特征。

### 58. Incremental Pose Graph

当然也不一定每次 loop / odometry 来都 batch optimize 整张图。

可以使用：

$$
iSAM2
$$

等 incremental 方法。

新 edge 加进来：

> 只重新线性化和更新受明显影响的区域。

所以大规模在线 Pose Graph 也可以很高效。

### 59. Pose Graph 不是只用于 Visual SLAM

任何能产生相对 pose constraints 的系统都能用。

例如：

#### LiDAR SLAM

ICP / scan matching：

$$
T_{ij}
$$

↓

Pose Graph

#### Wheel + LiDAR

Wheel odom edge：

$$
T_{wheel}
$$

LiDAR loop：

$$
T_{loop}
$$

↓

统一优化。

#### Multi-session Mapping

今天建一次图， 明天再跑一次。 不同 session 检测到相同地点， 加入 cross-session edges， 就可以把地图合并。

### 60. Pose Graph 最核心的抽象

不管 edge 来自：

- Camera
- LiDAR
- Wheel
- GNSS-derived relative relation
- human annotation

一旦它被表达成：

两个 Pose 之间应该满足什么关系 就可以进入 Pose Graph。 来源变得不那么重要了。

### 61. 和 BA 再做一次最重要的比较

||Bundle Adjustment|Pose Graph|
|---|---|---|
|Variables|Poses + Landmarks|Poses|
|Measurement|Pixel observations|Relative Pose|
|Precision|更细|更粗|
|State size|大|小|
|适合|Local refinement / high accuracy|Global correction|
|Loop Closure 后|可做，但贵|非常适合|

所以这两者不是竞争关系。

实际系统往往：

$$
\boxed{ Local\ BA + Global\ Pose\ Graph }
$$

一起用。

### 62. 为什么这种组合特别合理？

Local BA：

> 保证当前局部地图精细。

Pose Graph：

> 保证整张地图长期不漂。

于是分别解决：

Local Accuracy

和：

Global Consistency 这是非常经典的分层架构。

### 63. 这其实反映一个机器人系统常见原则

不要让一个算法同时承担所有尺度的问题。

短期：

Tracking

中期：

Local BA

长期：

$$
Pose\ Graph + Loop
$$

不同模块解决不同时间/空间尺度。 这个思想远比具体 ORB-SLAM 实现更值得记。

### 64. 本章最重要的七句话

第一：

Pose Graph 的变量全部是 Pose

第二：

$$
\boxed{ Edge = Relative\ Pose\ Constraint }
$$

第三：

典型 Edge：

$$
\boxed{ Odometry + Loop\ Closure }
$$

第四：

Pose Graph cost：

$$
\boxed{ \sum \|\operatorname{Log}(Z_{ij}^{-1}T_i^{-1}T_j)\|^2_{\Omega_{ij}} }
$$

第五：

Loop Closure 的价值：

Long-range constraint corrects accumulated drift

第六：

Pose Graph 比 BA 更轻，但保留的信息更粗

第七：

经典 SLAM 很常见的分工：

$$
\boxed{ Local\ BA\ for\ local\ accuracy + Pose\ Graph\ for\ global\ consistency }
$$

> 修订说明：第 14 节中有噪声的约束彼此冲突，优化无法同时精确满足所有测量；应表述为按信息权重平衡残差。Switchable Constraints 需要鼓励开关保持激活的先验／正则项，否则把全部 s 设为 0 就能关闭所有回环。残差协方差须与 Log 误差定义一致，不能直接使用任意传感器原始协方差。

## 思考题

### Q1：为什么 Loop Closure 不应该只修改当前 Pose？

**参考答案**

因为 drift 是整个 trajectory 累积产生的。 如果只修改最后一个 Pose，

会让：

$$
T_{N-1}\rightarrow T_N
$$

突然出现不合理的大跳变。 正确做法是让所有相关 Poses 在各自 constraint 和 uncertainty 下共同调整。


### Q2：为什么 Pose Graph 比 BA 更适合大规模全局优化？

**参考答案**

因为 Pose Graph 不再显式保留大量 landmarks。

变量数量通常从：

$$
6N+3M
$$

降低为：

$$
6N
$$

当：

$$
M\gg N
$$

时计算量差别巨大。


### Q3：既然 Pose Graph 更快，为什么不彻底抛弃 BA？

**参考答案**

因为 Pose Graph 使用的是已经被压缩的 relative-pose measurements。 BA 直接利用原始 reprojection observations，

能同时优化：

$$
Pose+Structure
$$

通常精度更高。 所以两者解决不同层次的问题。


### Q4：为什么错误 Loop Closure 比普通 Odometry Error 危险得多？

**参考答案**

因为 loop edge 通常跨越很长时间：

$$
x_i\leftrightarrow x_j,\quad |i-j|\gg1
$$

一个错误的强约束会影响大量中间 Poses， 甚至扭曲整张地图。


### Q5：Monocular SLAM 为什么常用 Sim(3) 做 Loop Correction？

**参考答案**

因为 monocular trajectory 可能存在：

Scale Drift SE(3) 只能调整 rotation + translation。

Sim(3) 还有：

$$
Scale
$$

因此可以同时修正长期尺度漂移。


### Q6：为什么 Pose Graph 也要固定第一帧？

**参考答案**

因为所有相对 pose constraints 对整体 global transform 不敏感。

整个轨迹一起：

$$
T_i\rightarrow T_gT_i
$$

不会改变任何：

$$
T_i^{-1}T_j
$$

所以存在 Gauge Freedom。

必须通过：

$$
Fix\ Pose / Prior
$$

选定坐标系。


### Q7：Pose Graph 优化完以后为什么还可能需要 Global BA？

**参考答案**

因为 Pose Graph 只调整 Keyframe Poses。 MapPoints 通常只是跟随 correction 粗略调整。 Global BA 可以重新利用所有 pixel observations，

同时精调：

$$
Poses+Landmarks
$$

得到更高精度的一致地图。


### Q8：如果一个 Pose Graph 的最终所有 residual 都不是 0，是不是说明优化失败？

<details>

<summary>参考答案</summary>

不是。 现实中的 measurements 有 noise，而且可能互相矛盾。

最优解追求的是：

weighted global consistency 而不是强行让每一条 measurement 都精确成立。

</details>

## 相关章节与来源

- 上一章：[Factor Graph](factor-graphs.md)
- 下一篇：[回环检测与全局校正](loop-closure.md)
- 来源：本次新增 Part IV Chapter 45 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
