---
title: Factor Graph
description: 如何用变量与因子统一表示多传感器估计、消元与边缘化？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 44
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# Factor Graph

## 本章目标

如何用变量与因子统一表示多传感器估计、消元与边缘化？

## 前置知识

[非线性最小二乘](nonlinear-least-squares.md)、[Bundle Adjustment](bundle-adjustment.md)。

## 定义与假设

Gaussian 噪声、局部线性化和固定数据关联都是建模条件；相应推导只在这些条件下适用。三维位姿采用 SE(3)，局部扰动按 [δρ,δφ] 排列，平移用 m、旋转用 rad。Exp 输入六维向量时表示先经 hat 映射再取矩阵指数，Log 输出六维坐标；左右更新需与残差和 Jacobian 一致。 各因子由假设的条件依赖结构决定；同一测量不可重复当作独立证据。完整后验中还应包括先验因子。

## 核心问题


先给你最重要的一句话：

Variable 是未知量，Factor 是对这些未知量施加约束的 Measurement

整个状态估计问题就是：

> 找一组 variable values，让所有 factors 尽可能同时满意。

## 概率分解与变量／因子

### 1. 从最简单的例子开始

假设机器人只有三个 Pose：

$$
x_0,x_1,x_2
$$

Odometry 告诉我们：

$$
x_0\rightarrow x_1
$$

移动了大约 1m。

然后：

$$
x_1\rightarrow x_2
$$

也移动了大约 1m。

图可以画成：

```
x0 ----- x1 ----- x2
```

这里：

$$
x_0,x_1,x_2
$$

是我们不知道的状态。

而两条边：

$$
z_{01}
$$

和：

$$
z_{12}
$$

是 Measurement。

### 2. 普通 Graph 和 Factor Graph 稍微不一样

普通 Graph 常画：

```
x0 -------- x1
```

一条 edge 表示 constraint。 Factor Graph 会把 constraint 本身也画成 node。

例如：

```
x0 --- f01 --- x1
```

其中：

$$
x_0,x_1
$$

叫：

Variable Nodes

而：

$$
f_{01}
$$

叫：

Factor Node

所以 Factor Graph 是一种：

Bipartite Graph

两类节点：

- Variables
- Factors

Factor 只连接 Variable。

### 3. 为什么要把 Factor 单独画出来？

因为一个 measurement 不一定只连接两个变量。

例如：

IMU factor 可能连接：

$$
x_i,v_i,b_i
$$

和：

$$
x_j,v_j,b_j
$$

甚至涉及很多 state components。

如果只画普通 edge：

> “这条边到底是什么 measurement？”

不够明确。

Factor Graph 直接把 measurement 建模成对象：

```
variables ── factor ── variables
```

所以表达能力更强。

### 4. Factor 到底是什么？

数学上，一个 factor 可以理解成：

$$
\phi_i(X_i)
$$

它只依赖整个 State 的一小部分：

$$
X_i\subset X
$$

例如 Odometry Factor：

$$
\phi_{ij}(x_i,x_j)
$$

GPS Factor：

$$
\phi_i(x_i)
$$

Landmark Observation Factor：

$$
\phi_{ij}(x_i,m_j)
$$

IMU Factor：

$$
\phi_{ij}(x_i,v_i,b_i,x_j,v_j,b_j)
$$

所以不同 sensor 只是：

产生了不同类型的 Factor

### 5. 概率形式怎么写？

假设整个状态：

$$
X
$$

所有 observations：

$$
Z
$$

我们想求 posterior：

$$
p(X|Z)
$$

Factor Graph 的核心思想是把这个大概率分布分解：

$$
p(X|Z) \propto \prod_i \phi_i(X_i)
$$

也就是说：

> 整体概率由很多局部 factor 相乘组成。

### 6. 为什么能分解？

因为每个 measurement 通常只和少数 state 有关。

比如 GPS at time 10：

$$
z_{GPS,10}
$$

只和：

$$
x_{10}
$$

有关。

它和：

$$
x_{500}
$$

没有直接 measurement relation。

所以：

$$
p(z_{GPS,10}|X) = p(z_{GPS,10}|x_{10})
$$

这种局部依赖关系正是 Factor Graph 的基础。

### 7. 从概率变成 Optimization

对于 Gaussian measurement：

$$
z_i=h_i(X_i)+\epsilon_i
$$

其中：

$$
\epsilon_i\sim\mathcal N(0,\Sigma_i)
$$

那么 factor 可以写成：

$$
\phi_i(X_i) \propto \exp \left( -\frac12 r_i^T\Sigma_i^{-1}r_i \right)
$$

其中：

$$
r_i = z_i-h_i(X_i)
$$

最大化 posterior：

$$
\max_X\prod_i\phi_i(X_i)
$$

取：

$$
-\log
$$

就变成：

$$
\boxed{ X^* = \arg\min_X \sum_i r_i^T\Sigma_i^{-1}r_i }
$$

你是不是已经完全认识了？ 这就是 Chapter 42 的 Nonlinear Least Squares。

## SLAM 中的观测与先验因子

以下相对位姿因子中 T_i 表示节点到世界的变换，预测为 T_i⁻¹T_j；视觉投影因子中的 T_i 表示 world-to-camera。两种局部例子采用不同方向，放入同一系统时需显式统一或取逆，不能仅按符号相同直接拼接。

### 8. 所以 Factor Graph 不是另一套优化算法

这点非常重要。

不要理解成：

> Gauss-Newton 是一个算法，Factor Graph 又是另一个算法。

不是。

Factor Graph 是：

Problem Representation

而：

- Gauss-Newton
- Levenberg-Marquardt
- Dogleg

是：

Optimization Method 两者处在不同层级。

### 9. 一个很实用的层级关系

可以这样理解：

```
Real Sensors
    ↓
Measurements
    ↓
Factor Graph
    ↓
Residual Functions
    ↓
Nonlinear Least Squares
    ↓
Gauss-Newton / LM
    ↓
Sparse Linear Solver
```

所以：

Factor Graph

负责描述：

> 这个问题是什么。

Solver 负责：

> 这个问题怎么算。

### 10. Factor Graph 的一个简单例子

假设机器人三个 pose：

$$
x_0,x_1,x_2
$$

有：

- 一个 prior
- 两个 odometry measurements

Factor Graph：

```
        f01          f12
x0 ------------ x1 ------------ x2
|
f_prior
```

更严格地画：

```
         [f01]         [f12]
        /     \       /     \
      x0      x1     x1      x2
      |
   [prior]
```

为了简洁，我们通常还是画：

```
prior
  |
 x0 -- odom -- x1 -- odom -- x2
```

### 11. Prior Factor 是干什么的？

假设：

$$
x_0
$$

没有任何绝对 reference。 那么整条轨迹可以一起平移。

Chapter 39 已经知道：

Gauge Freedom

所以我们加入：

$$
f_{prior}(x_0)
$$

例如：

$$
r_{prior} = x_0-\bar x_0
$$

这会固定/约束世界坐标。

所以：

$$
\boxed{ Prior\ Factor = Anchor }
$$

### 12. Odometry Factor 怎么写？

假设 measurement：

$$
z_{ij}
$$

表示：

> 从 pose $$i$$ 到 pose $$j$$ 的相对变换。

预测相对变换：

$$
\hat z_{ij} = x_i^{-1}x_j
$$

残差大致：

$$
r_{ij} = z_{ij}^{-1} \hat z_{ij}
$$

当然 Pose 在：

$$
SE(3)
$$

上，所以真正 residual 会通过：

$$
Log()
$$

映射到：

$$
\mathfrak{se}(3)
$$

例如：

$$
r_{ij} = \operatorname{Log} \left( Z_{ij}^{-1} T_i^{-1}T_j \right)
$$

得到一个：

$$
6D
$$

residual。

### 13. 不用害怕 Log

你现在只需要理解：

$$
Z_{ij}^{-1}T_i^{-1}T_j
$$

表达的是：

> prediction 和 measurement 之间还差多少刚体变换。

然后：

$$
Log
$$

把这个小变换变成一个普通 6D vector：

$$
r\in\mathbb R^6
$$

这样就能放进 Least Squares。

### 14. Landmark Factor 怎么写？

Camera $$i$$ 看到 MapPoint $$j$$。

Variable：

$$
T_i
$$

和：

$$
P_j
$$

Measurement：

$$
z_{ij}
$$

预测：

$$
\hat z_{ij} = \pi(T_iP_j)
$$

Residual：

$$
r_{ij} = z_{ij} - \pi(T_iP_j)
$$

这个 factor 就连接：

```
Pose_i --- VisualFactor --- Landmark_j
```

这正是上一章 BA 的一条 observation。

所以：

BA 本质上就是一种 Factor Graph

### 15. BA 的 Factor Graph 长什么样？

例如：

```
P1       P2       P3
|\       / \      /|
| \     /   \    / |
C1     C2    C3
```

更准确地说，每条 Camera-Landmark relation 中间都有一个 visual factor。

所以 BA 是：

$$
Camera\ Variables + Landmark\ Variables + Reprojection\ Factors
$$

### 16. Pose Graph 又是什么？

如果我们把 Landmark 消掉，

只保留：

$$
T_1,T_2,\dots,T_N
$$

然后 measurement 是：

Relative Pose

那么：

```
T1 --- T2 --- T3 --- T4
|                  |
└------ loop ------┘
```

这就是：

Pose Graph 所以 Pose Graph 也是 Factor Graph 的一个特例。 只是 variables 全是 Pose。

### 17. VIO 的 Factor Graph 更丰富

假设每个时刻 state：

$$
x_i= (T_i,v_i,b_i)
$$

其中：

- $$T_i$$：Pose
- $$v_i$$：Velocity
- $$b_i$$：IMU bias

然后有：

#### IMU Factor

连接：

$$
x_i \leftrightarrow x_{i+1}
$$

#### Visual Factor

连接：

$$
x_i \leftrightarrow Landmark_j
$$

#### Prior Factor

连接：

$$
x_0
$$

于是：

```
x0 ---- IMU ---- x1 ---- IMU ---- x2
|                 |                |
visual            visual           visual
|                 |                |
P1                P2               P3
```

这就是一个典型 Visual-Inertial Factor Graph。

### 18. 加 GPS 怎么办？

超级简单。

在某个 pose：

$$
x_i
$$

旁边加一个 GPS factor：

```
GPS
 |
x_i
```

Residual：

$$
r_{gps} = p_i-p_{gps}
$$

再根据 GPS covariance：

$$
\Sigma_{gps}
$$

加权。

所以：

$$
\boxed{ Sensor\ Fusion = Add\ Factors }
$$

这是 Factor Graph 特别漂亮的地方。

### 19. 加 Wheel Odometry 呢？

再加：

Wheel Factor 连接相邻 poses。

### 20. 加 Loop Closure 呢？

如果：

$$
x_{20}
$$

和：

$$
x_{500}
$$

检测到 loop：

```
x20 ---------------- x500
       loop factor
```

加入一个 relative pose factor：

$$
f_{loop}(x_{20},x_{500})
$$

就行。

### 21. 所以 Factor Graph 为什么适合多传感器融合？

因为不同 sensor 最后都统一成：

$$
\boxed{ Residual + Uncertainty }
$$

Camera：

$$
r_{cam}
$$

IMU：

$$
r_{imu}
$$

GPS：

$$
r_{gps}
$$

Wheel：

$$
r_{wheel}
$$

Loop：

$$
r_{loop}
$$

然后整体：

$$
E(X) = E_{cam} + E_{imu} + E_{gps} + E_{wheel} + E_{loop}
$$

统一 optimize。

### 22. 这就是“公共语言”

不同 sensor 原始数据完全不同。

Camera：

$$
pixel
$$

IMU：

acceleration, angular velocity

GPS：

position

Wheel encoder：

wheel rotation

但进入后端后都变成：

This measurement says these variables should satisfy this relation 所以 Factor Graph 是一种非常强的系统抽象。

### 23. 一个很重要的思想：Factor 是局部的

比如 GPS Factor：

$$
f(x_{10})
$$

只连接一个变量。

Odometry：

$$
f(x_{10},x_{11})
$$

只连接两个。

Visual Factor：

$$
f(x_i,P_j)
$$

也只连接两个。

IMU Factor：

连接有限几个 variable blocks。

因此：

Global problem is built from local constraints 这也是 sparsity 的来源。

## 权重、稀疏结构与图模型

### 24. Graph sparsity 怎么变成 Matrix sparsity？

假设：

$$
x_1
$$

和：

$$
x_2
$$

有 factor。

那 Hessian 中：

$$
H_{12}
$$

可能非零。

如果：

$$
x_1
$$

和：

$$
x_5
$$

没有任何 factor，也没有通过同一个 factor 直接关联，

那么对应 Hessian block 初始上通常是：

$$
0
$$

所以：

Graph connectivity  ↔  Hessian sparsity 这就是上一章最后说的那句话。

### 25. Factor Graph 为什么能帮助我们“看懂”优化问题？

因为一个巨大 Hessian：

$$
10000\times10000
$$

你直接看矩阵， 基本没有直觉。

但是如果看 Graph：

```
x1 -- x2 -- x3
      |
      P1
```

你马上知道：

- 谁约束谁
- 哪个 variable 信息少
- 有没有 loop
- 哪里可能 gauge
- 哪个 node 连接度高

所以 Graph 是一种：

Structural representation

### 26. Factor Graph 也能帮我们看 Observability

例如：

```
x0 -- x1 -- x2
```

但没有 prior。 那么整个链可以整体平移/旋转。

看到图就知道：

> 缺 absolute anchor。

再比如某个 landmark：

```
x1 --- P
```

只被一个 pose 观察一次。 那它 depth 可能很弱。

如果：

```
x1 --- P --- x2 --- P
```

多个不同 viewpoint 观察， information 更强。 所以图结构和 observability 有直接关系。

### 27. Factor 数量多就一定好吗？

不一定。

比如：

$$
1000
$$

个 factors 都表达几乎一样的信息。 那 information gain 并不会线性增加。

而一个非常关键的 loop closure factor：

$$
x_0\leftrightarrow x_{1000}
$$

可能比几百个局部 odometry factors 更有长期价值。

所以：

Factor importance  ≠  Factor count

### 28. Factor 的权重从哪里来？

每个 factor 有 measurement covariance：

$$
\Sigma_i
$$

Information matrix：

$$
\Omega_i=\Sigma_i^{-1}
$$

Cost：

$$
E_i = r_i^T\Omega_i r_i
$$

所以：

$$
\Omega_i
$$

决定这个 factor 对整体优化的话语权。

### 29. 一个例子

GPS：

$$
\sigma=5m
$$

那么它比较不可信。

Camera relative pose：

$$
\sigma=0.05m
$$

局部可能很可靠。

Optimizer 会综合：

Residual magnitude

和：

Measurement uncertainty 来决定怎么调整状态。 不是简单“谁 residual 大听谁”。

### 30. Robust Kernel 在 Factor Graph 里怎么理解？

一个 factor：

$$
E_i=r_i^T\Omega_i r_i
$$

如果 residual 很大， 可能是 outlier。

于是改成：

$$
\rho(E_i)
$$

这等于说：

> 这个 factor 看起来越来越可疑，就逐渐减少它的影响。

所以 robust kernel 可以理解成：

Factor confidence adaptation

### 31. Loop Closure Factor 为什么特别危险？

因为它通常连接：

$$
x_i
$$

和很久以后的：

$$
x_j
$$

跨度很大。

如果正确：

> 可以修正整个长期 drift。

如果错误：

> 可以把整张地图扭曲。

所以 loop factor 通常必须经过非常严格的：

- place recognition
- geometric verification
- RANSAC
- consistency check

之后才加入 graph。

### 32. 一个错误 Factor 为什么会影响很远？

假设：

```
x0 -- x1 -- x2 -- x3 -- x4
```

加入：

```
x0 ----------- x4
```

这条 factor 会要求：

$$
x_0,x_4
$$

满足某种关系。 为了满足它，

optimizer 可能调整：

$$
x_1,x_2,x_3
$$

因为这些状态都通过其他 factors 连在一起。 所以局部 factor 也可以通过 graph 传播影响。

### 33. 这和 EKF 的 Covariance propagation 有什么对应？

EKF 中：

> information 通过 covariance 相关性传播。

Factor Graph 中：

> information 通过 graph constraints 和 optimization 传播。

两者在概率意义上有深层统一。 只是 representation 不一样。

### 34. Factor Graph 和 Bayesian Network 是一回事吗？

不是完全一样。

Bayesian Network 是：

Directed Graph

强调：

conditional probability 和因果/条件依赖结构。

Factor Graph 则是：

Bipartite Undirected Representation

强调：

> 一个大函数如何分解成多个局部 factors。

对于 SLAM optimization，Factor Graph 特别直观。

### 35. Markov Random Field 呢？

你以后可能也会看到：

$$
MRF
$$

它也是无向概率图。 Factor Graph 和 MRF 可以表达很多相似结构， 但 Factor Graph 把高阶 factor 显式画出来，

所以更方便表示：

$$
f(x_1,x_2,x_3,x_4)
$$

这种多变量约束。

## 变量消元与 Fill-in

### 36. Factor Graph 求解本质上还是 Variable Elimination

我们前面 BA 讲 Schur Complement。

那其实就是：

Eliminate Landmark

Factor Graph 里可以更一般地说：

> 选择一个 variable，收集所有和它相关的 factors，然后把它消掉，把信息转移给它的邻居。

这就是：

Variable Elimination

### 37. 一个简单例子

假设：

```
x1 --- x2 --- x3
```

Factor：

$$
f_{12}(x_1,x_2)
$$

和：

$$
f_{23}(x_2,x_3)
$$

如果消掉：

$$
x_2
$$

那么：

$$
x_1
$$

和：

$$
x_3
$$

之间会产生一个新的关系：

```
x1 -------- x3
```

这就是消元带来的：

fill-in

### 38. 所以 Variable Elimination Order 很重要

假设一个 node：

```
        x2
       / | \
     x1 x3 x4
```

如果先消：

$$
x_2
$$

那么：

$$
x_1,x_3,x_4
$$

之间会形成更多 connections。 这会让矩阵变 dense。 所以 solver 会尽量选择好的 elimination ordering。

例如：

- COLAMD
- AMD

之类方法。

目的就是：

Reduce fill-in

### 39. BA 的 Schur Complement 就是一个特殊 ordering

BA 中：

```
Camera --- Point --- Camera
```

我们选择：

> 先消所有 Point。

因为 point blocks：

- 小
- 独立
- 易消

这是一个非常聪明的 elimination order。 所以 Chapter 43 的 Schur Complement 其实就是 Chapter 44 的一个特例。

### 40. Bayes Net / Bayes Tree 为什么会出现？

像 GTSAM / iSAM2 会进一步把 Factor Graph 消元后的结构表示成：

Bayes Net

甚至：

Bayes Tree

这样做的一个巨大好处是：

> 新 factor 加进来以后，不需要整个图重新求。

只更新受影响的那部分。 这就是 incremental smoothing。

## 增量求解、边缘化与全局参数

### 41. 为什么机器人特别需要 Incremental？

因为机器人数据是一帧帧来的：

$$
z_1,z_2,z_3,\dots
$$

不是一开始就拿到全部 measurements。

所以最笨的方法：

```
new measurement
↓
re-optimize everything from scratch
```

会非常浪费。

更理想：

```
new measurement
↓
find affected graph region
↓
update only necessary part
```

这就是：

Incremental Optimization

### 42. iSAM 和 iSAM2 的直觉

你现在不需要掌握它们完整数学。

先知道目标：

高效地做在线 Smoothing

也就是：

> 保留历史状态的优化优势，又避免每次从头做完整 batch optimization。

iSAM2 会利用 Bayes Tree：

> graph 哪块变化，就主要更新哪块。

这和“局部重算”非常类似。

### 43. Batch Optimization vs Incremental Optimization

Batch：

$$
Z_{1:t}
$$

全部拿出来， 从当前 initial guess 做整体优化。

优点：

- 简单
- 全局一致

缺点：

- 每次重新算很贵

Incremental：

新来：

$$
z_{t+1}
$$

只更新受影响结构。

优点：

- 在线效率高

这也是 GTSAM 很重要的方向。

### 44. Sliding Window 又在哪里？

Factor Graph 不一定保存全部历史。

你可以只保留：

$$
x_{t-k},...,x_t
$$

形成 Fixed-Lag Smoother。

老状态：

$$
x_{t-k-1}
$$

Marginalize 掉。

所以 Factor Graph 可以实现：

- Full smoothing
- Fixed-lag smoothing
- Local optimization

非常灵活。

### 45. Marginalization 在 Factor Graph 里怎么理解？

假设：

```
x0 -- x1 -- x2
```

现在要删掉：

$$
x_0
$$

但不能简单把 factor：

$$
f_{01}
$$

一起扔了。 否则 x0 带来的历史信息全丢。

所以我们计算：

$$
\int p(x_0,x_1,\dots)\,dx_0
$$

把：

$$
x_0
$$

积分掉。

最后生成一个新的 prior：

$$
f_{prior}(x_1)
$$

也就是：

```
old:

prior -- x0 -- x1

new:

new_prior -- x1
```

所以：

$$
\boxed{ Marginalization = remove variable, preserve its information as a new factor }
$$

### 46. 这是不是和 Schur Complement 很像？

是的。 在线性 Gaussian 问题里， Marginalization 和 Schur Complement 紧密相关。

都体现：

消掉变量，但把它的信息留下 你会发现 Part IV 一直反复出现这个主题。

### 47. 但 Marginalization 会带来一个问题：Dense Prior

假设旧变量：

$$
x_0
$$

同时和：

$$
x_1,x_2,x_3
$$

都有关系。 把 x0 marginalize 后，

可能得到一个 factor：

$$
f(x_1,x_2,x_3)
$$

于是这些变量被更紧密地连接起来。

也就是说：

Marginalization creates fill-in 所以 sliding-window estimator 的 prior 往往变 dense。

### 48. 这又是为什么窗口不能无限大

窗口越大：

- 精度可能更好
- 保留信息更多

但：

- optimization 更贵
- marginalization 更复杂

所以还是：

Accuracy  ↔  Computation 的平衡。

### 49. Factor Graph 如何表示 Static Parameter？

除了动态 state：

$$
x_t
$$

还可以加入全局参数。

例如：

$$
T_{cam-imu}
$$

相机-IMU 外参。

或者：

time offset

甚至：

camera intrinsic 这些变量可能被所有时刻的 factors 连接。

例如：

```
x0 \
x1  \
x2 --- Extrinsic
x3  /
```

然后在线 calibration。

### 50. 但这种 variable 会造成什么？

它连接很多 factors， 所以 graph degree 很高。

一旦把它加入优化：

- Hessian coupling 增强
- fill-in 变多
- 计算更贵

而且 observability 也更复杂。 所以全局 calibration variable 要谨慎。

### 51. 一个很好用的 Factor Graph 分析法

以后看到一个陌生系统，先别急着看代码。 先问四个问题。

第一：

Variables 是什么？

比如：

- pose
- velocity
- bias
- landmark
- calibration

第二：

Factors 是什么？

比如：

- camera
- IMU
- GPS
- wheel
- loop

第三：

每个 Factor 连接哪些 Variables？

第四：

哪些 Variables 被固定或 marginalize？ 只要回答这四个问题， 整个 estimator 结构基本就清楚了。

### 52. 举个实际机器人例子

假设机器人有：

- Stereo Camera
- IMU
- Wheel Encoder
- GPS

State：

$$
x_i= (T_i,v_i,b_i)
$$

再加一些 landmarks：

$$
P_j
$$

Factor Graph：

```
             GPS
              |
x0 ==== x1 ==== x2 ==== x3
|       |       |       |
IMU     IMU     IMU
|       |       |
wheel   wheel   wheel

 \      |      /
  visual factors
       |
   landmarks
```

整个后端 cost：

$$
E= E_{visual} + E_{imu} + E_{wheel} + E_{gps} + E_{prior}
$$

这就是一个很标准的 multi-sensor estimator。

### 53. 如果 GPS 丢了会怎样？

GPS factors 暂时不再加入。

系统仍然可以靠：

- visual
- IMU
- wheel

保持 relative localization。

但是：

global drift 会逐渐增加。

GPS 恢复后：

absolute factor 重新加入， 可以把 trajectory 拉回 global frame。 这就是 Factor Graph 对 sensor dropout 非常自然的处理方式。

### 54. 如果某个 Sensor 很差怎么办？

两种主要手段。

第一：

正确设置：

$$
\Sigma
$$

让它 information weight 变小。

第二：

如果出现 gross outlier：

Robust Loss

甚至直接：

Reject Factor

所以传感器融合不是：

> 所有 sensor 一视同仁。

而是：

Information-weighted fusion

### 55. Factor Graph 为什么特别适合解释 Fusion？

因为传统说法：

> “融合 Camera 和 IMU。”

太抽象。

Factor Graph 会明确变成：

> Camera factor 在约束哪些 variables？

> IMU factor 在约束哪些 variables？

> 两者在哪些 state 上发生 coupling？

比如：

velocity Camera 通常不直接测。 IMU factor 会直接约束 velocity evolution。 但 Camera 通过 Pose observation 可以间接修正 Velocity。 这就是 graph 中的信息传播。

### 56. Graph 中的信息传播不是“消息真的沿边跑”吗？

不一定。 如果使用某些 message passing 算法，确实可以这么理解。 但在常见 nonlinear least-squares solver 中，

更准确地说：

> 所有 factors 共同形成一个线性系统，解这个系统后 correction 同时作用于多个 variables。

所以“信息沿 graph 传播”主要是一个结构性直觉。

### 57. Factor Graph 和神经网络 Graph 不一样

名字里都有 Graph，但别混。

Factor Graph：

Probabilistic graphical model

描述：

$$
Variables + Constraints
$$

Graph Neural Network：

Neural Architecture 在图结构上学习表示。 两者完全不是一回事。 当然未来也可以把 GNN 用于 SLAM，但概念不同。

### 58. 为什么说 Factor Graph 是“现代机器人状态估计的语言”？

因为它能非常统一地表达：

$$
SLAM
$$

$$
VIO
$$

$$
LIO
$$

Sensor Fusion Calibration Loop Closure GPS Fusion

你只需要不断问：

Variable? Factor? Residual?

$$
Noise?
$$

整个系统就可以被统一表达。

### 59. 一句话把 BA 放进 Factor Graph

BA：

Variables：

$$
\boxed{ Camera\ Poses + Landmarks }
$$

Factors：

Reprojection Measurements

Residual：

$$
\boxed{ z-\pi(TP) }
$$

Noise：

Pixel Measurement Covariance

所以：

$$
\boxed{ BA = Visual Factor Graph Optimization }
$$

### 60. 一句话把 Pose Graph 放进去

Variables：

Poses

Factors：

Relative Pose Measurements

包括：

- odometry
- loop closure

Residual：

$$
\operatorname{Log} (Z_{ij}^{-1}T_i^{-1}T_j)
$$

这就是 Pose Graph。 下一章就会专门讲它。

### 61. 一句话把 VIO 放进去

Variables：

$$
\boxed{ Pose + Velocity + Bias + maybe\ Landmarks }
$$

Factors：

$$
\boxed{ Visual + IMU + Prior }
$$

如果再加 GPS：

$$
+GPS\ Factor
$$

如果加 wheel：

$$
+Wheel\ Factor
$$

系统框架完全不需要推翻。 只是继续加 factor。

### 62. 本章真正应该形成的思维转换

以前看到：

$$
Camera
$$

你可能先想到：

> 图像处理。

看到 IMU：

> 惯导。

看到 GPS：

> 全球定位。

从 Factor Graph 视角：

你应该转换成：

>  **它提供了什么 measurement relation？**

然后问：

>  **这个 relation 连接哪些 State？**

这就是状态估计工程里非常关键的抽象能力。

### 63. Factor Graph 的完整逻辑链

原始世界：

Sensor Measurements

↓

每个 measurement 建立：

$$
Factor
$$

↓

Factor 连接：

Variables

↓

Factor 定义：

Residual

↓

Residual 有：

$$
Covariance / Information
$$

↓

所有 Factor cost 相加：

$$
E(X)=\sum_iE_i
$$

↓

Nonlinear Optimization：

$$
Gauss\text{-}Newton / LM
$$

↓

Linearization：

$$
H\Delta x=-b
$$

↓

Graph topology 决定：

Hessian sparsity

↓

利用：

$$
Sparse\ Solver / Variable\ Elimination
$$

求 State。 这就是整个 Factor Graph framework。

### 64. 本章最重要的七句话

第一：

$$
\boxed{ Variable\ Node = Unknown\ State }
$$

第二：

$$
\boxed{ Factor\ Node = Measurement / Constraint }
$$

第三：

整个 posterior：

$$
\boxed{ p(X|Z)\propto\prod_i\phi_i(X_i) }
$$

第四：

Gaussian factor 最后会变成：

Weighted Least Squares Residual

第五：

Graph Connectivity  ↔  Hessian Sparsity

第六：

$$
\boxed{ Sensor\ Fusion = Add\ Different\ Factors }
$$

第七：

$$
\boxed{ Variable\ Elimination = 删除变量，但把它携带的信息传递给邻居 }
$$

> 整理说明：Factor Graph 表示函数分解，算法还可以采用迭代／直接线性求解等路径；变量消元是重要求解视角，不是唯一算法。Bayesian Network 的有向结构表达条件依赖，未经额外因果假设不能直接解释为因果。非线性边缘化通常是在固定线性化点附近压缩信息，并非完整保留任意状态范围内的历史非线性似然。

## 思考题

### Q1：Factor Graph 为什么比“直接写一个巨大 Cost Function”更好理解？

<details>

<summary>参考答案</summary>

因为它显式展示：

哪个 measurement 依赖哪些 variables

所以：

- sparsity
- observability
- sensor coupling
- loop closure
- marginalization

都能直观看出来。

</details>

### Q2：Factor Graph 自己负责优化吗？

<details>

<summary>参考答案</summary>

不是。

Factor Graph 是：

Problem Representation

真正优化仍然可以用：

Gauss-Newton

$$
LM
$$

等算法。

</details>

### Q3：为什么加入 GPS 只需要增加 GPS Factor，而不用重新设计整个 estimator？

<details>

<summary>参考答案</summary>

因为所有 sensor 都统一表达为：

$$
Residual + Uncertainty
$$

GPS 只是提供一种新的：

Absolute Position Constraint 所以它自然加入现有 graph。

</details>

### Q4：为什么一个 Factor 通常只连接少量 Variables？

<details>

<summary>参考答案</summary>

因为物理 measurement 通常具有局部依赖。

例如：

Camera observation 只依赖当前 Camera Pose 和被观察 Landmark。

这种局部性产生了：

Sparse Graph

和：

Sparse Hessian

</details>

### Q5：为什么消掉一个 Variable 会让它的邻居产生新联系？

<details>

<summary>参考答案</summary>

因为原来它是邻居之间的信息桥梁。

例如：

$$
x_1-f(x_1,x_2)-x_2-f(x_2,x_3)-x_3
$$

把：

$$
x_2
$$

消掉后，

x2 携带的信息必须转移成：

$$
x_1\leftrightarrow x_3
$$

的关系。

所以产生：

fill-in

</details>

### Q6：Marginalization 为什么不是简单删除旧 State？

<details>

<summary>参考答案</summary>

因为简单删除会把过去 measurement 提供的信息也一起删除。

Marginalization 要做到：

remove state, preserve information

通常把历史信息变成剩余状态上的：

Prior Factor

</details>

### Q7：为什么 Loop Closure 可以在 Factor Graph 里非常自然地表示？

<details>

<summary>参考答案</summary>

因为它本质上就是：

> 两个相距很远的历史 Pose 之间，新发现了一条 relative-pose measurement。

所以只需加入：

$$
f_{loop}(x_i,x_j)
$$

图里就多了一条长距离约束。

</details>

### Q8：如果我要分析一个完全陌生的 VIO/LIO/SLAM 系统，最值得先问哪四个问题？

<details>

<summary>参考答案</summary>

先问：

$$
\boxed{1.\ Variables\ 是什么？}
$$

$$
\boxed{2.\ Factors\ 是什么？}
$$

$$
\boxed{3.\ 每个 Factor 连接哪些 Variables？}
$$

$$
\boxed{4.\ 哪些 Variables 被固定、滑窗或 Marginalize？}
$$

这四个问题回答出来，整个 estimator 的骨架基本就已经清楚了。

</details>

## 相关章节与来源

- 上一章：[Bundle Adjustment](bundle-adjustment.md)
- 下一篇：[Pose Graph Optimization](pose-graph.md)
- 来源：本次新增 Part IV Chapter 44 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
- 核验参考：[GTSAM：Factor Graph 入门](https://gtsam.org/tutorials/intro.html)。
