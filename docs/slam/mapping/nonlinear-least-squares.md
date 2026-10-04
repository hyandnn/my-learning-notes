---
title: 非线性最小二乘
description: 残差怎样变成 Gauss–Newton、LM 与稀疏线性系统？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 42
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# 非线性最小二乘

## 本章目标

残差怎样变成 Gauss–Newton、LM 与稀疏线性系统？

## 前置知识

[Jacobian](../probabilistic/jacobian.md)、[扫描匹配与 ICP](../spatial/scan-matching-icp.md)、[Gauge Freedom](gauge-freedom.md)。

## 定义与假设

Gaussian 噪声、局部线性化和固定数据关联都是建模条件；相应推导只在这些条件下适用。三维位姿采用 SE(3)，局部扰动按 [δρ,δφ] 排列，平移用 m、旋转用 rad。Exp 输入六维向量时表示先经 hat 映射再取矩阵指数，Log 输出六维坐标；左右更新需与残差和 Jacobian 一致。 加权最小二乘使用 W = Σ⁻¹，Σ 假设正定；测量条件独立且协方差与状态无关时，Gaussian 似然才直接给出固定权重二次代价。

## 核心问题


$$
\boxed{ SLAM\ 后端 = 找一组 State，让所有 measurement residual 尽可能小 }
$$

比如 Visual SLAM：

$$
r_{ij} = z_{ij}-\pi(T_iP_j)
$$

然后我们希望：

$$
\min_X \sum_{i,j}\|r_{ij}(X)\|^2
$$

这个看似简单的式子，就是 Bundle Adjustment、Pose Graph、Factor Graph Optimization 背后的核心。

## 从 Gaussian 似然到加权最小二乘

### 1. 先别碰 SLAM，来看一个最简单的问题

假设我们有一些 measurement：

$$
z_1,z_2,z_3
$$

例如：

$$
z_1=4.9,\quad z_2=5.1,\quad z_3=5.0
$$

我们想估一个真实值：

$$
x
$$

measurement model 非常简单：

$$
z_i=x+\epsilon_i
$$

那么 residual：

$$
r_i=z_i-x
$$

我们希望 residual 越小越好。

于是定义：

$$
E(x)=\sum_i(z_i-x)^2
$$

求：

$$
x^* = \arg\min_xE(x)
$$

结果当然就是平均值：

$$
x^*=5.0
$$

这就是最简单的：

Least Squares

### 2. 为什么是平方？

为什么不直接：

$$
\sum_i r_i
$$

？ 因为正负 residual 会抵消。

例如：

$$
r_1=+10
$$

$$
r_2=-10
$$

那么：

$$
r_1+r_2=0
$$

看起来完美，但实际错误非常大。

所以要么绝对值：

$$
|r|
$$

要么平方：

$$
r^2
$$

Least Squares 使用：

$$
\boxed{r^2}
$$

### 3. 为什么最小二乘和概率有关？

这一步特别重要。

假设 measurement noise：

$$
\epsilon_i\sim\mathcal N(0,\sigma_i^2)
$$

也就是 Gaussian noise。

那么：

$$
p(z_i|x) \propto \exp \left( -\frac{(z_i-h_i(x))^2}{2\sigma_i^2} \right)
$$

所有 observations 独立时：

$$
p(Z|x) = \prod_i p(z_i|x)
$$

Maximum Likelihood：

$$
x^* = \arg\max_x p(Z|x)
$$

取负 log：

$$
-\log p(Z|x)
$$

乘法变加法。

最后：

$$
x^* = \arg\min_x \sum_i \frac{(z_i-h_i(x))^2}{\sigma_i^2}
$$

也就是：

$$
\boxed{ Maximum\ Likelihood \Longleftrightarrow Weighted\ Least\ Squares }
$$

所以最小二乘不是一个随便想出来的数学技巧。 它直接来自 Gaussian measurement model。

### 4. 如果 Measurement 的维度不止一维呢？

假设 residual 是向量：

$$
r_i= \begin{bmatrix} r_x\\ r_y \end{bmatrix}
$$

并且 covariance：

$$
\Sigma_i
$$

那么 cost：

$$
E_i = r_i^T\Sigma_i^{-1}r_i
$$

记成：

$$
\|r_i\|_{\Sigma_i}^2
$$

所以整体：

$$
\boxed{ E(X) = \sum_i r_i(X)^T \Sigma_i^{-1} r_i(X) }
$$

你应该已经非常熟悉：

$$
\Sigma^{-1}
$$

就是 Information Matrix。

所以 measurement 越可靠：

$$
\Sigma\downarrow
$$

则：

$$
\Sigma^{-1}\uparrow
$$

这个 residual 的权重就越大。

### 5. 先看 Linear Least Squares

如果 measurement model 是线性的：

$$
z=Hx+\epsilon
$$

那么 residual：

$$
r=z-Hx
$$

cost：

$$
E(x) = (z-Hx)^T W (z-Hx)
$$

其中：

$$
W=\Sigma^{-1}
$$

求导并令：

$$
\frac{\partial E}{\partial x}=0
$$

得到：

$$
H^TWHx = H^TWz
$$

于是：

$$
\boxed{ x^* = (H^TWH)^{-1}H^TWz }
$$

这是标准 Weighted Least Squares。

### 6. 那为什么 SLAM 叫 Nonlinear Least Squares？

因为 SLAM 的 measurement model 通常不是：

$$
z=Hx
$$

而是：

$$
z=h(x)
$$

比如 Camera projection：

$$
u=f_x\frac{X}{Z}+c_x
$$

$$
v=f_y\frac{Y}{Z}+c_y
$$

里面有：

$$
\frac{X}{Z}
$$

明显是非线性的。

再比如 Pose：

$$
T\in SE(3)
$$

Rotation 本身也是非线性的。

所以 residual：

$$
r(x)=z-h(x)
$$

最终：

$$
\boxed{ \min_x \sum_i \|r_i(x)\|^2 }
$$

是 Nonlinear Least Squares。

### 7. 非线性的问题在哪里？

如果：

$$
r(x)
$$

是线性的， 我们可以直接一次求解。

但如果：

$$
r(x)
$$

是非线性的， 通常没有漂亮的 closed-form solution。

比如：

$$
E(x) = (\sin x-0.5)^2
$$

你很难像线性方程那样：

> 一次矩阵求逆直接得到答案。

所以我们采用一种很自然的办法：

Iterative Optimization

## 线性化与 Gauss–Newton 推导

### 8. Iterative Optimization 的基本思想

假设当前 estimate：

$$
x_k
$$

我们不尝试直接找到最终：

$$
x^*
$$

而是先找一个小修正：

$$
\Delta x
$$

得到：

$$
x_{k+1} = x_k+\Delta x
$$

然后不断重复：

$$
x_0 \rightarrow x_1 \rightarrow x_2 \rightarrow ... \rightarrow x^*
$$

问题就变成：

> 当前应该往哪个方向走多少？

### 9. Linearization 出现了

在当前：

$$
x_k
$$

附近，

对 residual 做一阶 Taylor expansion：

$$
r(x_k+\Delta x) \approx r(x_k) + J\Delta x
$$

其中：

$$
J = \frac{\partial r}{\partial x}
$$

就是：

Jacobian

于是原本非线性的：

$$
r(x)
$$

在当前点附近，被近似成一个线性函数。 这与 Part II 的 EKF 线性化思路一致。

### 10. Jacobian 到底是什么意思？

我不希望你只把它理解成：

> “一堆偏导数。”

更直觉一点：

$$
\boxed{ Jacobian 描述 State 变化一点点时，Measurement / Residual 会怎么变化 }
$$

假设：

$$
r= \begin{bmatrix} r_1\\ r_2 \end{bmatrix}
$$

State：

$$
x= \begin{bmatrix} x_1\\ x_2\\ x_3 \end{bmatrix}
$$

那么：

$$
J = \begin{bmatrix} \frac{\partial r_1}{\partial x_1} & \frac{\partial r_1}{\partial x_2} & \frac{\partial r_1}{\partial x_3} \\ \frac{\partial r_2}{\partial x_1} & \frac{\partial r_2}{\partial x_2} & \frac{\partial r_2}{\partial x_3} \end{bmatrix}
$$

它告诉你：

> 每个 state direction 对 residual 的影响有多大。

### 11. 这和 Observability 又连起来了

假设某个 state：

$$
x_j
$$

怎么变化， residual 都几乎不变。

那：

$$
\frac{\partial r}{\partial x_j}\approx0
$$

也就是说 Jacobian 对这个方向非常弱。

那么这个 state 就：

weakly observable

如果完全为 0：

$$
Jv=0
$$

说明存在一个 null direction。

这又回到了 Chapter 39：

Gauge Freedom

所以：

Observability  ↔  Jacobian  ↔  Information 其实是同一件事的不同表达。

### 12. 把线性化代回 Cost

原问题：

$$
\min_{\Delta x} \|r(x_k+\Delta x)\|^2
$$

近似：

$$
\min_{\Delta x} \|r+J\Delta x\|^2
$$

注意：

$$
r=r(x_k)
$$

在当前 iteration 已知。

所以现在变成一个：

Linear Least Squares 问题。

### 13. 展开一下

定义：

$$
E(\Delta x) = (r+J\Delta x)^T(r+J\Delta x)
$$

展开：

$$
E = r^Tr + 2r^TJ\Delta x + \Delta x^TJ^TJ\Delta x
$$

对：

$$
\Delta x
$$

求导：

$$
2J^Tr + 2J^TJ\Delta x = 0
$$

于是：

$$
J^TJ\Delta x = -J^Tr
$$

定义：

$$
H=J^TJ
$$

$$
b=J^Tr
$$

得到：

$$
\boxed{ H\Delta x=-b }
$$

这就是 SLAM 优化里你会疯狂看到的方程。

### 14. Gauss-Newton 出现了

所以 Gauss-Newton Algorithm 本质非常简单：

当前：

$$
x_k
$$

计算：

$$
r(x_k)
$$

计算 Jacobian：

$$
J
$$

构造：

$$
H=J^TJ
$$

$$
b=J^Tr
$$

解：

$$
H\Delta x=-b
$$

然后：

$$
x_{k+1}=x_k+\Delta x
$$

不断重复。

这就是：

$$
\boxed{ Gauss\text{-}Newton }
$$

### 15. 为什么 $$H=J^TJ$$ 被叫 Hessian？

严格来说真正 Hessian 是：

$$
\nabla^2 E
$$

对于：

$$
E=\frac12r^Tr
$$

真正 Hessian 中还有 residual 的二阶导项。

大致是：

$$
\nabla^2E = J^TJ + \sum_i r_i\nabla^2r_i
$$

Gauss-Newton 忽略第二项。

所以使用：

$$
\boxed{ H\approx J^TJ }
$$

因此经常叫：

Approximate Hessian

### 16. 为什么可以忽略第二阶项？

当 optimization 已经靠近最优解时：

$$
r_i
$$

比较小。

那么：

$$
r_i\nabla^2r_i
$$

这一项影响也比较小。

所以：

$$
J^TJ
$$

是一个很好的 Hessian approximation。

这也是为什么：

Gauss-Newton 在 least-squares 问题里特别合适。

### 17. 但是初始值差的时候呢？

这就是问题。

如果：

$$
x_0
$$

离正确答案非常远，

那么：

linearization 可能很差。

比如一条弯曲函数：

```
             /
           /
       ___/
______/

          x0
```

你在 $$x_0$$ 处画 tangent， 这个局部线性模型可能根本不能代表远处函数。

于是计算出来：

$$
\Delta x
$$

可能太大。

甚至：

> Cost 反而升高。

### 18. 这就是 Gauss-Newton 的主要弱点

依赖一个比较好的 initialization 这也解释了 SLAM 为什么如此重视 Front-end。

前端给后端的初值如果太差：

- PnP 错
- loop closure 错
- odometry 漂太远

后端并不是神仙。 非线性 optimizer 可能掉进错误 local minimum。

## 梯度、Newton 与 LM

### 19. Gradient Descent 又是什么？

最基本的优化方法：

$$
x_{k+1} = x_k-\alpha\nabla E
$$

沿负梯度方向走。

这里：

$$
\alpha
$$

是 learning rate / step size。 你之前做深度学习训练已经非常熟悉了。

其实：

> 神经网络训练和 SLAM optimization，在“优化”这一层有很多共同语言。

### 20. Gradient Descent 和 Gauss-Newton 差在哪？

Gradient Descent 只看：

Gradient

告诉你：

> 往哪边下降。

Gauss-Newton 还利用：

$$
J^TJ
$$

描述 cost surface 的局部 curvature。

因此它不仅知道：

> 往哪里走，

还近似知道：

> 每个方向应该走多少。

所以对于典型 SLAM least-squares：

Gauss-Newton 往往比简单 Gradient Descent 收敛快很多。

### 21. 一个二维直觉

假设 cost surface 是：

```
     __________
   /            \
  /              \
 |       ●        |
  \              /
   \____________/
```

但实际更像一条很窄的山谷：

```
      /
     /
    /
   /
```

不同方向 curvature 差很多。

Gradient Descent 容易：

```
↘
 ↙
  ↘
   ↙
```

左右震荡着走。

而二阶信息可以知道：

> 这个方向非常陡，少走一点；那个方向很平，走多一点。

### 22. Newton Method 呢？

真正 Newton Method：

$$
H_{true}\Delta x = -\nabla E
$$

使用真实 Hessian：

$$
H_{true} = \nabla^2E
$$

理论上局部收敛很快。

但真实 Hessian 计算昂贵，而且 least-squares 问题有：

$$
J^TJ
$$

这么好用的结构。

所以 SLAM 中通常更喜欢：

Gauss-Newton

或：

Levenberg-Marquardt

### 23. Levenberg-Marquardt 是什么？

简称：

$$
LM
$$

它是 SLAM / BA 中非常经典的算法。

核心形式：

$$
\boxed{ (H+\lambda I)\Delta x=-b }
$$

相比 Gauss-Newton：

$$
H\Delta x=-b
$$

多了：

$$
\lambda I
$$

### 24. 这个 $$\lambda I$$ 是干什么的？

假设：

$$
\lambda
$$

很小：

$$
H+\lambda I \approx H
$$

于是 LM 很像：

Gauss-Newton

如果：

$$
\lambda
$$

非常大：

$$
H+\lambda I \approx \lambda I
$$

那么：

$$
\Delta x \approx -\frac1\lambda b
$$

而：

$$
b=J^Tr
$$

基本就是 gradient。

所以这时 LM 更像：

Gradient Descent

因此：

LM 在 Gradient Descent 和 Gauss-Newton 之间动态切换

### 25. 为什么这么做？

当当前模型很可信、接近 optimum：

> 大胆使用 Gauss-Newton，快速前进。

如果 linearization 不太可信：

> 步子缩小，变得保守。

所以 LM 通常比纯 Gauss-Newton：

more robust

### 26. Trust Region 的直觉

LM 可以从：

Trust Region 角度理解。

我们刚才通过 Taylor expansion：

$$
r(x+\Delta x) \approx r(x)+J\Delta x
$$

但这个 approximation 只在：

$$
\Delta x
$$

比较小的时候可信。

所以我们实际上应该说：

> 我只相信当前 linear model 附近这一小块区域。

这就是：

Trust Region

### 27. Step 太大为什么危险？

想象真实 cost：

```
       __
     _/
   _/
 _/
```

局部 tangent 在附近不错。

但 extrapolate 太远：

> 完全不准。

所以 optimizer 不能盲目按照一次 linearization 走很远。

这就是：

- LM
- line search
- trust region

这些机制存在的根本原因。

## 流形更新与 SLAM 的稀疏结构

### 28. Gauss-Newton 的一次完整迭代

以后你看到 Ceres、g2o、GTSAM 之类库时，可以把底层抽象成：

$$
X_k
$$

↓

计算所有：

$$
r_i(X_k)
$$

↓

计算：

$$
J_i
$$

↓

assemble：

$$
H
$$

和：

$$
b
$$

↓

solve：

$$
H\Delta X=-b
$$

↓

update：

$$
X_{k+1}=X_k\boxplus\Delta X
$$

↓

重新 linearize。

这里我故意用了：

$$
\boxplus
$$

而不是普通：

$$
+
$$

原因马上讲。

### 29. Pose 不能简单做普通加法

假设 State 是：

$$
x\in\mathbb R^3
$$

普通 update：

$$
x\leftarrow x+\Delta x
$$

没问题。

但是 Camera Pose：

$$
T\in SE(3)
$$

不能简单：

$$
T+\Delta T
$$

因为两个 rotation matrix 相加后：

$$
R+\Delta R
$$

不一定还是合法 rotation matrix。

### 30. Rotation 有约束

Rotation Matrix 满足：

$$
R^TR=I
$$

以及：

$$
\det(R)=1
$$

如果直接优化 9 个 matrix elements：

$$
R_{11},R_{12},...,R_{33}
$$

你还必须始终保证这些约束。 很麻烦。

所以我们一般在：

Lie Algebra 的局部空间里优化。

### 31. SE(3) 与 se(3)

Pose：

$$
T\in SE(3)
$$

它位于一个非线性 manifold。

但它附近可以用一个六维向量表示小扰动：

$$
\delta\xi = \begin{bmatrix} \delta\rho\\ \delta\phi \end{bmatrix} \in\mathbb R^6
$$

其中：

$$
\delta\rho
$$

表示小 translation，

$$
\delta\phi
$$

表示小 rotation。

这个六维局部空间就是：

$$
\mathfrak{se}(3)
$$

### 32. Pose Update 怎么做？

例如采用左扰动：

$$
T_{new} = \exp(\delta\xi^\wedge)T
$$

或者采用右扰动：

$$
T_{new} = T\exp(\delta\xi^\wedge)
$$

具体 convention 不同系统可能不同。 现阶段你不需要展开 Lie Algebra 的全部推导。

先记住：

优化器优化的是 Pose 的小增量，而不是直接随便修改 Rotation Matrix

### 33. 为什么这很像“局部坐标”？

你可以把地球表面想象成一个曲面。 整个地球不是平的。

但是你站在一个城市附近：

> 可以用二维平面近似这一小块。

Manifold optimization 类似：

$$
SE(3)
$$

全局不是普通 Euclidean space，

但当前 Pose 附近可以用：

$$
\mathbb R^6
$$

描述一个小 perturbation。

### 34. 现在回到 Visual SLAM

假设一个 MapPoint：

$$
P_j^w
$$

被 Camera $$i$$ 看到。

当前 Camera Pose：

$$
T_{cw,i}
$$

预测 pixel：

$$
\hat z_{ij} = \pi(T_{cw,i}P_j^w)
$$

实际：

$$
z_{ij}
$$

Residual：

$$
r_{ij} = z_{ij} - \pi(T_{cw,i}P_j^w)
$$

这是一个二维向量：

$$
r_{ij} = \begin{bmatrix} r_u\\ r_v \end{bmatrix}
$$

### 35. 这个 residual 对谁求 Jacobian？

它同时依赖：

Camera Pose

和：

Landmark

所以有：

$$
J_{pose} = \frac{\partial r}{\partial \delta\xi}
$$

和：

$$
J_{point} = \frac{\partial r}{\partial P}
$$

于是一个 observation：

```
Camera i -------- Landmark j
```

只影响：

$$
T_i
$$

和：

$$
P_j
$$

不会直接影响：

$$
T_{100}
$$

或者：

$$
P_{5000}
$$

如果它们没有 measurement relation。

### 36. Sparse Structure 出现了

这件事情极其重要。

假设 State：

$$
X= [T_1,T_2,\dots,T_N, P_1,P_2,\dots,P_M]
$$

一个 observation：

$$
r_{ij}
$$

只和：

$$
T_i,P_j
$$

有关。

所以 Jacobian 一行大概长这样：

```
         Ti                Pj
          ↓                 ↓
[0 0 0  Jpose 0 0 ... 0  Jpoint 0 0]
```

绝大多数位置都是：

$$
0
$$

因此：

J is sparse

于是：

$$
H=J^TJ
$$

也有很强的 sparse block structure。

### 37. 这就是为什么 SLAM 可以优化很多变量

如果真的把：

$$
H
$$

当普通 dense matrix 处理， 几千、几万个变量就非常恐怖。 但 measurement graph 是局部连接的。

所以：

$$
H
$$

是稀疏的。

现代 SLAM backend 的核心能力之一就是：

Exploit sparsity

### 38. Block Structure 更重要

Pose 是：

$$
6D
$$

Landmark 是：

$$
3D
$$

所以 Hessian 不是随机的 scalar matrix。

而是：

```
       poses        landmarks
     ┌──────────┬───────────┐
pose │ Hpp      │ Hpl       │
     ├──────────┼───────────┤
land │ Hlp      │ Hll       │
     └──────────┴───────────┘
```

这叫：

Block Hessian

后面的 Bundle Adjustment 会利用这个结构干一件清晰的事情：

Schur Complement 把大量 landmarks 先消掉。 Chapter 43 会重点讲。

## 信息、异常观测与优化边界

### 39. 为什么 Hessian 表示 Information？

还记得：

$$
H=J^TWJ
$$

如果某个 state direction 对 residual 非常敏感：

$$
Jv
$$

很大，

那么：

$$
v^THv
$$

也大。

说明：

> measurement 对这个方向提供很多信息。

反过来：

$$
Jv\approx0
$$

则：

$$
Hv\approx0
$$

说明：

> 沿这个方向 state 怎么变化，measurement 都没什么感觉。

所以：

Hessian 可以近似理解为局部 Information Matrix

### 40. 这和 EKF 的 Information Matrix 又接上了

EKF 中：

$$
\Lambda=P^{-1}
$$

代表 information。

Optimization 中：

$$
H\approx J^T\Sigma^{-1}J
$$

也代表 measurement 对 state 的局部 information。 所以 Filtering 和 Optimization 虽然形式不同， 背后的概率含义是统一的。

### 41. Gauge Freedom 为什么让 Hessian Singular？

Chapter 39 已经讲过。

如果存在：

$$
v
$$

使得整个地图沿 $$v$$ 变化时所有 measurement 都不变：

$$
Jv=0
$$

于是：

$$
Hv = J^TJv = 0
$$

所以：

$$
H
$$

存在零特征值。 因此不可逆。

这就是：

Gauge Freedom  →  Null Space  →  Singular Hessian 这三个概念现在正式连起来了。

### 42. Fixed Pose 怎么解决？

例如固定：

$$
T_0
$$

等于不再把：

$$
T_0
$$

当作 optimization variable。 这样 global gauge 被移除。 于是 Hessian 的相关 null space 消失。 这就是为什么 Chapter 39 不是理论闲聊。 它直接影响数值求解。

### 43. Outlier 又回来了

普通 Least Squares：

$$
E=\sum_i r_i^2
$$

如果一个正确 measurement：

$$
r=1
$$

贡献：

$$
1
$$

一个错误 association：

$$
r=20
$$

贡献：

$$
400
$$

一个 outlier 就可能抵得上几百个正常 residual。 所以平方损失对 outlier 很敏感。

### 44. Robust Loss

于是把：

$$
r^2
$$

改成：

$$
\rho(r^2)
$$

例如 Huber loss：

小 residual 时：

$$
\rho(s)\approx s,\qquad s=r^2
$$

大 residual 时：

$$
\rho(s)
$$

增长变慢。

意思就是：

> 正常 measurement 按标准最小二乘处理。

> 特别离谱的 measurement 不让它拥有无限大的影响力。

### 45. 这实际上是“动态降低可信度”

你甚至可以把 robust kernel 理解成：

> residual 大到可疑时，我自动降低这个 measurement 的 information weight。

也就是：

$$
W_i \downarrow
$$

所以它和我们以前的：

confidence uncertainty 完全是一脉相承的。

### 46. Cost 下降就一定说明结果正确吗？

不一定。 这是 Nonlinear Optimization 很重要的一点。

可能存在多个 Local Minima：

```
      \__/      \____/
       A          B
```

如果初始化在 A 附近， optimizer 可能收敛到 A。 即使 B 才是真实正确解。

因此：

Low Cost  ≠  Globally Correct 尤其错误 data association 可能构造一个“自洽但错误”的解。

### 47. 所以前端和后端不是谁替代谁

Front-end 的职责之一是：

good initialization

和：

correct association

Backend：

refine continuous states

所以可以简单理解：

Front-end 决定你优化的是不是“对的问题” Back-end 决定这个问题解得有多精确 这个区分非常有用。

### 48. 一个小例子：PnP Pose Optimization

假设 MapPoint 固定：

$$
P_1,\dots,P_{100}
$$

当前 Camera Pose：

$$
T
$$

有 100 个 observations：

$$
z_i
$$

Residual：

$$
r_i(T) = z_i-\pi(TP_i)
$$

目标：

$$
T^* = \arg\min_T \sum_{i=1}^{100} \|r_i(T)\|^2
$$

假设 PnP 给初始：

$$
T_0
$$

然后 optimizer：

$$
T_0 \rightarrow T_1 \rightarrow T_2 \rightarrow T_3
$$

直到 reprojection error 不再明显下降。 这就是一个小型 nonlinear least-squares problem。

### 49. Bundle Adjustment 和它有什么区别？

Pose Optimization：

$$
P_i
$$

固定，只优化：

$$
T
$$

BA 则是：

$$
T_i
$$

也优化，

$$
P_j
$$

也优化。

也就是：

$$
\boxed{ Camera + Structure\ jointly\ optimized }
$$

所以变量更多。

但数学核心仍然：

$$
r=z-\pi(TP)
$$

完全一样。

### 50. Pose Graph 又有什么区别？

Pose Graph 没有大量 landmarks。

变量主要是：

$$
T_1,T_2,\dots,T_N
$$

measurement 是相对 pose：

$$
Z_{ij}
$$

预测相对 pose：

$$
T_i^{-1}T_j
$$

Residual 大概表达：

$$
Z_{ij}^{-1} T_i^{-1}T_j
$$

与 identity 的偏差。

最后仍然：

$$
\min \sum_{ij} \|r_{ij}\|^2
$$

所以：

> BA、Pose Graph、PnP Optimization，数学骨架其实完全一样。

只是：

$$
State
$$

和：

Measurement Model 不同。

### 51. 这就是“Factor”概念的来源

每一个 measurement：

$$
z_i
$$

产生一个 residual：

$$
r_i(X_i)
$$

其中只依赖部分 states。

我们可以把它理解成：

$$
\boxed{ 一个 measurement = 一个 factor }
$$

所以最终：

$$
E(X) = \sum_iE_i(X_i)
$$

每个：

$$
E_i
$$

都是一个局部 cost。 这就是下一阶段 Factor Graph 的基本思想。

## 增量计算与线性求解

### 52. Incremental Optimization 又是什么？

传统方式可能：

> 新 measurement 来了，整个问题重新优化。

但机器人 measurement 不断到来：

$$
z_1,z_2,z_3,\dots
$$

每次从零开始太浪费。 所以一些 solver 会复用之前结果和矩阵结构。

例如：

$$
iSAM
$$

$$
iSAM2
$$

这就是：

Incremental Optimization 不过 Factor Graph 那章再详细展开。

### 53. 什么时候停止迭代？

Optimization 不会无限跑。

通常会看：

$$
\|\Delta x\|
$$

是否已经很小。

或者：

$$
|E_k-E_{k+1}|
$$

是否很小。

或者达到：

max iterations

例如：

$$
10
$$

次。 实时 SLAM 很多时候没必要追求数学上的极高精度。

只要：

good enough 就继续处理下一帧。

### 54. 所以实时 SLAM 的优化目标不是“算到完美”

而是：

Accuracy within computational budget 这点很工程。

例如 Local BA：

> 跑 5 次 iteration 就已经足够好。

再跑 20 次，

cost 可能只下降：

$$
0.01\%
$$

却影响实时性。 没必要。

### 55. 一个 Solver 真正在做什么？

以后你使用：

- Ceres
- g2o
- GTSAM

别把它们看成“神秘 SLAM 库”。

最底层其实都在做类似：

```
Define State Variables

Define Residual Functions

Linearize

Build Sparse Linear System

Solve Δx

Update State

Repeat
```

最大的区别在：

- manifold handling
- sparse linear solver
- factorization
- marginalization
- incremental update
- numerical robustness

### 56. Linear Solver 为什么重要？

Nonlinear Optimization 每一次 iteration 都会转成：

$$
H\Delta x=-b
$$

所以最终大量时间花在：

Solve Linear System 上。

也就是说：

> Nonlinear Optimization 外面是 nonlinear，里面核心工作反复在解 sparse linear system。

### 57. 为什么不直接求 $$H^{-1}$$？

理论：

$$
\Delta x=-H^{-1}b
$$

但实际算法几乎不会真的计算：

$$
H^{-1}
$$

因为：

- 贵
- 数值稳定性差
- 破坏 sparsity

而是直接求：

$$
H\Delta x=-b
$$

通过：

- Cholesky
- QR
- PCG 等

解决线性系统。

所以代码里如果没看到：

```
H.inverse()
```

反而是正常的。 真正大型优化里直接 inverse 通常不是好习惯。

### 58. Cholesky 为什么常见？

如果：

$$
H
$$

是 symmetric positive definite，

可以分解：

$$
H=LL^T
$$

然后：

$$
LL^T\Delta x=-b
$$

先解：

$$
Ly=-b
$$

再解：

$$
L^T\Delta x=y
$$

比直接 inversion 高效且稳定。 Sparse Cholesky 是 SLAM backend 很重要的工具。

### 59. 为什么 Hessian 有时不是正定？

比如：

- Gauge Freedom
- 欠约束
- 数值问题
- 当前 Jacobian 的秩或尺度不合适

可能导致：

$$
H
$$

singular / ill-conditioned。

LM 加：

$$
\lambda I
$$

还有一个作用：

$$
H+\lambda I
$$

更容易变成数值上稳定的 positive definite matrix。 所以 damping 既控制 step，也改善 conditioning。

### 60. Condition Number 的直觉

如果 Hessian 某些方向：

information very strong

而另一些方向：

information extremely weak

特征值可能：

$$
\lambda_{max} \gg \lambda_{min}
$$

那么矩阵 condition number：

$$
\kappa = \frac{\lambda_{max}}{\lambda_{min}}
$$

很大。

系统称为：

ill-conditioned 这时候一点 measurement noise 就可能让弱方向变化很大。

这其实就是：

Weak Observability 的数值版本。

### 61. 再把这三件事连起来

物理层面：

这个方向 Measurement 信息弱

数学层面：

$$
Jv\approx0
$$

矩阵层面：

$$
Hv\approx0
$$

数值层面：

small eigenvalue

工程表现：

> estimate 对 noise 很敏感，容易跳。

这就是同一件事从五个角度来看。

### 62. Normalization 为什么有时重要？

假设 State 同时包含：

position [m]

和：

rotation [rad]

甚至还有：

velocity, bias, scale 它们数值尺度可能完全不同。 如果尺度差异过大， 优化的 conditioning 可能变差。

所以合理的：

- parameterization
- weighting
- noise covariance

非常重要。 不能只是把所有 residual 裸地加在一起。

### 63. Measurement Weight 绝不是“调参权重”

这个概念你以后要特别警惕。

比如：

$$
E = r_{camera}^TW_cr_{camera} + r_{imu}^TW_ir_{imu}
$$

这里：

$$
W_c
$$

$$
W_i
$$

理论上应该来自：

measurement uncertainty

而不是：

> Camera 不听话，那就乘 100。

更正确的理解是：

$$
W=\Sigma^{-1}
$$

这代表 sensor information。 当然工程上 noise model 也要调，但它应该有概率意义。

### 64. 为什么 Noise Model 错会出问题？

如果 Camera 实际很 noisy，

但你设：

$$
\Sigma_{cam}
$$

特别小，

就等于告诉 optimizer：

> Camera 是绝对真理。

于是其他 sensors 都会被它拉过去。

反之 IMU noise 设得过大：

> estimator 几乎不相信 IMU。

所以 sensor fusion 本质上很大程度就是：

Information weighting

### 65. Nonlinear Least Squares 的完整图景

现在你可以把整个过程理解成：

Measurements

↓

定义：

Residuals

↓

考虑：

$$
Covariance / Information
$$

↓

得到：

$$
Cost
$$

↓

当前状态附近：

Linearization

↓

得到：

$$
J
$$

↓

构造：

$$
H=J^TWJ
$$

$$
b=J^TWr
$$

↓

解：

$$
H\Delta x=-b
$$

↓

State Update：

$$
X\boxplus\Delta x
$$

↓

重新 Linearize

↓

直到收敛。 这就是现代 SLAM backend 最重要的 computational loop。

### 66. 用一句话区分我们已经学过的几个概念

Residual：

当前 Prediction 到底错了多少

Jacobian：

State 改一点，Residual 会怎么改

Hessian：

所有 Measurement 综合起来，对各 State direction 提供多少局部 Information

$$
\Delta x
$$

：

为了降低所有 Residual，这一轮 State 应该怎么修

Optimizer：

不断重复上述过程 只要这四句话真的理解，后面 BA 会容易很多。

### 67. 本章最重要的一条思想

我们之前大量讨论：

Prediction  →  Observation  →  Residual  →  Correction

Chapter 42 终于把最后一个箭头打开：

$$
Residual \quad \xrightarrow[\text{Jacobian/Hessian}]{Optimization} \quad Correction
$$

也就是：

Residual 怎么真正变成 State Correction 这就是本章最大的意义。

> 修订说明：统一鲁棒损失记号为 ρ(s)，s = rᵀWr ≥ 0；小残差时 ρ(s) ≈ s，不能同时把 ρ 的输入写成 r² 又说 ρ(r) ≈ r²。JᵀWJ 在 W 半正定时始终半正定；线性化点差本身不使这个 Gauss–Newton 矩阵变成不定，可能带来秩亏、病态或差的局部模型。完整 Newton Hessian 则可能不定。逆矩阵表达式要求满秩；实际解线性系统。H 的逆只在固定 gauge、可辨识且模型合适时近似给出局部协方差。

## 本章思考题

### Q1：为什么 SLAM 通常是 Nonlinear Least Squares，而不是 Linear Least Squares？

<details>

<summary>参考答案</summary>

因为 Camera projection、rotation、3D geometry 等 measurement models 都是非线性的：

$$
z=h(X)
$$

因此 residual：

$$
r=z-h(X)
$$

也是 State 的非线性函数。

只能通过不断：

linearize →  solve →  update 进行迭代求解。

</details>

### Q2：Jacobian 非常小意味着什么？

<details>

<summary>参考答案</summary>

说明：

State 变化

几乎不会改变：

Residual 所以 measurement 对这个 state direction 不敏感。 也就是 information weak。

从工程上看意味着：

weak observability

</details>

### Q3：如果某个方向 Jacobian 完全为零呢？

<details>

<summary>参考答案</summary>

存在：

$$
v\neq0
$$

使：

$$
Jv=0
$$

那么：

$$
Hv=J^TJv=0
$$

因此 Hessian 有 null space。 这个方向是不可观的。 例如 SLAM global translation gauge。

</details>

### Q4：为什么 Gauss-Newton 需要较好初始化？

<details>

<summary>参考答案</summary>

因为它通过：

$$
r(x+\Delta x) \approx r(x)+J\Delta x
$$

做局部线性近似。 如果当前状态离真值太远， 这个 approximation 可能完全不准确。

于是算出的：

$$
\Delta x
$$

可能错误。

</details>

### Q5：LM 相比 GN 最大的意义是什么？

<details>

<summary>参考答案</summary>

Gauss-Newton：

$$
H\Delta x=-b
$$

LM：

$$
(H+\lambda I)\Delta x=-b
$$

通过 damping 控制 step。 当前模型可信时像 GN，模型不可信时更接近 Gradient Descent。

所以通常：

更稳健

</details>

### Q6：为什么 SLAM 的 Hessian 通常很 sparse？

<details>

<summary>参考答案</summary>

因为一个 measurement 只连接少量 states。

例如一个 camera observation：

$$
r_{ij}
$$

只依赖：

$$
Pose_i
$$

和：

$$
Landmark_j
$$

不会依赖所有其他 variables。 所以 Jacobian 和 Hessian 都天然具有 sparse block structure。

</details>

### Q7：为什么实际实现不会计算 $$H^{-1}$$？

<details>

<summary>参考答案</summary>

虽然理论：

$$
\Delta x=-H^{-1}b
$$

但直接求 inverse：

- 计算贵
- 数值稳定性差
- 不利于利用 sparsity

所以实际直接求解：

$$
H\Delta x=-b
$$

</details>

### Q8：为什么一个 Outlier 对普通 Least Squares 特别危险？

<details>

<summary>参考答案</summary>

因为：

$$
E=r^2
$$

residual 增大 10 倍，

cost 增大：

$$
100
$$

倍。 所以一个错误 measurement 可以压倒大量正常 observations。 这就是 RANSAC 和 Robust Kernel 必要的原因。

</details>

## 相关章节与来源

- 上一章：[关键帧与局部建图](keyframes-local-mapping.md)
- 下一篇：[Bundle Adjustment](bundle-adjustment.md)
- 来源：本次新增 Part IV Chapter 42 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
- 核验参考：[Ceres：非线性最小二乘](https://ceres-solver.readthedocs.io/latest/nnls_tutorial.html)。
- 核验参考：[Ceres：鲁棒损失定义](https://ceres-solver.readthedocs.io/latest/nnls_modeling.html)。
