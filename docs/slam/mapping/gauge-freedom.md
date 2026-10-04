---
title: SLAM 可观测性与 Gauge Freedom
description: 哪些方向没有绝对信息，为什么要选定坐标基准？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 39
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# SLAM 可观测性与 Gauge Freedom

## 本章目标

哪些方向没有绝对信息，为什么要选定坐标基准？

## 前置知识

[可观测性](../probabilistic/observability.md)、[EKF-SLAM](ekf-slam.md)。

## 定义与假设

默认讨论相对观测、静态场景且没有绝对位置或航向信息的连通系统。Gauge 的维数随传感器、已知尺度、重力参考和运动激励改变，不能对所有 SLAM 系统固定套用一个数字。

## 核心问题


这一章非常关键，因为它回答一个看似奇怪、但实际上决定 SLAM 数学结构的问题：

>  **为什么 SLAM 里经常要固定第一帧？**

很多人看到代码里：

```
setFixed(first_pose);
```

或者看到优化时：

$$
T_0 = I
$$

会把它理解成一种“工程习惯”。 其实不是。

背后原因是：

SLAM 本身存在不可观测自由度

也就是：

Gauge Freedom 这一章我们把这个问题彻底讲清楚。

## 相对观测与坐标自由度

### 1. 先从一个极简单例子开始

假设二维世界里有一个机器人和两个 Landmark。

机器人轨迹：

```
x0 ---- x1 ---- x2
```

Landmark：

```
      A

              B
```

机器人通过传感器知道：

$$
x_0 \rightarrow A
$$

距离和方向是多少。

又知道：

$$
x_1 \rightarrow A
$$

以及：

$$
x_2 \rightarrow B
$$

这些测量，本质上描述的是：

>  **相对关系。**

比如：

$$
A-x_0
$$

而不是：

$$
A = 12.3m
$$

这种绝对世界坐标。

### 2. 整个地图一起平移会怎样？

假设原来的地图是：

```
A

x0 ---- x1 ---- x2

                B
```

现在我把整个系统向右平移 10 米：

```
          A

          x0 ---- x1 ---- x2

                          B
```

注意：

机器人和 Landmark 全部一起移动。

也就是：

$$
x_i' = x_i + t
$$

$$
m_j' = m_j + t
$$

其中：

$$
t = \begin{bmatrix} 10\\ 0 \end{bmatrix}
$$

问题来了：

机器人测到 Landmark 的相对距离变了吗？ 没有。

比如：

$$
m_j'-x_i'
$$

等于：

$$
(m_j+t)-(x_i+t)
$$

于是：

$$
m_j'-x_i'=m_j-x_i
$$

所以所有 observation：

$$
z
$$

完全不变。

### 3. 这意味着什么？

这意味着：

> 单靠这些相对 measurement，你根本没法知道整个地图是在 $$x=0$$ 附近，还是 $$x=100m$$ 附近。

两套解：

$$
X
$$

和：

$$
X'
$$

会产生完全一样的观测。

所以：

Global Translation is unobservable 这就是不可观测性。

### 4. 再整体旋转一次

假设整个地图：

```
x0 ---- x1 ---- x2
       \
        A
```

整体旋转：

$$
30^\circ
$$

机器人、轨迹、landmarks 全部一起旋转。 相对几何关系仍然不变。

所以：

Global Rotation is also unobservable

对于二维 SLAM：

$$
x,y,\theta
$$

通常有：

$$
\boxed{ 3\ DOF\ gauge\ freedom }
$$

也就是：

- 全局 x 平移
- 全局 y 平移
- 全局旋转

### 5. 三维 SLAM 呢？

三维刚体变换：

$$
SE(3)
$$

有 6 个自由度：

$$
3\ translation + 3\ rotation
$$

如果系统完全依赖相对几何 measurement，没有任何绝对参考，那么：

整个世界做任意刚体变换，measurement 都不变

因此通常有：

$$
\boxed{ 6\ DOF\ gauge\ freedom }
$$

### 6. 这和“估计误差大”不是一回事

这里要特别区分：

#### 情况 A

某个变量很难估准。

例如：

$$
\sigma_x=5m
$$

它虽然非常不确定，但理论上 measurement 里还是有关于它的信息。

这是：

weakly observable

#### 情况 B

无论多少 measurement 都无法区分。

例如整个地图整体平移：

$$
X
$$

和：

$$
X+t
$$

产生完全相同 measurement。

这是：

unobservable 不是“误差比较大”。

而是：

> 根本不存在唯一答案。

### 7. 和我们之前讲的 Observability 接起来

之前我们讲过：

> Observability 是“能不能从 measurement 恢复某个 state”。

现在 SLAM 就是一个非常典型的例子。

比如你能知道：

$$
x_2-x_1
$$

因为 odometry 给了相对运动。

但你不知道：

$$
x_1
$$

在世界坐标系里的绝对位置。

所以：

relative pose 可以 observable，

而：

global pose 不可 observable。

### 8. 为什么这叫 Gauge Freedom？

Gauge 这个词可以理解成：

>  **坐标系选择自由。**

假设你画一个房间地图。

你可以规定左下角是：

$$
(0,0)
$$

但我也可以规定门口是：

$$
(0,0)
$$

甚至把整个坐标轴旋转：

$$
45^\circ
$$

只要内部相对关系保持一致， 两张地图描述的是同一个真实几何结构。

所以：

Gauge Freedom 不是传感器出问题。 也不是算法缺陷。

而是：

> 世界坐标系本来就是人为定义的。

### 9. 一个非常重要的理解

SLAM 真正能恢复的是：

relative geometry

而不是天然存在的：

absolute world coordinates 这句话很重要。

因为现实世界并没有自动给机器人一个：

```
世界 x 轴
世界 y 轴
世界原点
```

这些都是我们人为选的。

## 零空间、Hessian 与固定基准

### 10. 那为什么程序里一定要固定一个 Pose？

现在问题来了。

假设我们做优化：

$$
\min_X \sum_i \|r_i(X)\|^2
$$

如果：

$$
X^*
$$

是最优解。

那么：

$$
T X^*
$$

也可能是最优解。 也就是说有无穷多个等价解。

例如：

```
solution A:
x0 = 0
x1 = 1
x2 = 2
```

和：

```
solution B:
x0 = 100
x1 = 101
x2 = 102
```

residual 完全一样。

那么优化器会遇到一个问题：

Solution is not unique

### 11. Hessian 会发生什么？

后面 Chapter 42 会详细讲 nonlinear least squares。 现在先提前看一点。

优化里经常会得到：

$$
H\Delta x=-b
$$

其中：

$$
H=J^TJ
$$

如果系统有 gauge freedom，

那么存在某个非零方向：

$$
v
$$

使得：

$$
Hv=0
$$

因为沿这个方向移动 state， cost 不变。

所以：

$$
H
$$

会出现：

null space

导致：

$$
H
$$

不可逆或者病态。

### 12. 举个直观的 1D 例子

假设只有两个位置：

$$
x_1,x_2
$$

measurement：

$$
x_2-x_1=1
$$

cost：

$$
E=(x_2-x_1-1)^2
$$

满足条件的解有：

$$
x_1=0,\ x_2=1
$$

也可以：

$$
x_1=10,\ x_2=11
$$

甚至：

$$
x_1=-100,\ x_2=-99
$$

无穷多个解。

因为约束只知道：

$$
x_2-x_1
$$

不知道绝对位置。

### 13. 看 Hessian

Residual：

$$
r=x_2-x_1-1
$$

Jacobian：

$$
J= [-1,\ 1]
$$

于是：

$$
H=J^TJ
$$

得到：

$$
H= \begin{bmatrix} 1 & -1\\ -1 & 1 \end{bmatrix}
$$

它的 determinant：

$$
1\cdot1-(-1)(-1)=0
$$

所以：

H is singular

它有一个 null direction：

$$
v= \begin{bmatrix} 1\\ 1 \end{bmatrix}
$$

这是什么意思？

就是：

$$
x_1\rightarrow x_1+c
$$

$$
x_2\rightarrow x_2+c
$$

同时平移， cost 不变。 这就是 Gauge Freedom 的数学版本。

### 14. 怎么解决？

最常见办法：

Fix one pose

例如：

$$
x_0=0
$$

或者三维里：

$$
T_0=I
$$

这样等于人为规定：

> 第一帧就是世界坐标系。

于是其他 pose 全部相对第一帧表达。

### 15. 固定第一帧以后，是不是突然获得了绝对位置？

不是。 这点非常重要。

当你设置：

$$
T_0=I
$$

不是说：

> 第一帧真的位于宇宙中的绝对原点。

而是说：

> 我人为选择第一帧作为坐标基准。

这叫：

Gauge Fixing 我们只是从无穷多个等价解里选一个代表。

### 16. 一个生活化比喻

假设三个人站成一排：

```
A ---- B ------ C
```

你知道：

$$
AB=1m
$$

$$
BC=2m
$$

那么你完全知道他们之间的相对结构。 但是你不知道他们在地球哪个地方。

可以在：

```
东京
```

也可以在：

```
北京
```

甚至整体转 90°。 只要相对距离没变， 内部 observation 全部一样。

所以你规定：

> A 的位置定义成 $$0$$。

然后：

$$
B=1
$$

$$
C=3
$$

问题就有唯一坐标表达了。

## 传感器、尺度与运动激励

### 17. Absolute Sensor 会发生什么？

如果系统突然加入 GPS：

$$
x_{GPS}
$$

那事情就不一样了。

GPS 会提供：

absolute position 于是 global translation 不再完全自由。

例如：

$$
x_0=GPS
$$

那么整个地图就不能随便平移了。

### 18. IMU 会消除哪些自由度？

这个问题很有意思。 IMU 能测 gravity direction。

重力：

$$
g
$$

定义了一个天然方向。 因此 Roll 和 Pitch 可以被 gravity 约束。

也就是说：

gravity breaks some rotational gauge

但是：

$$
yaw
$$

围绕重力方向旋转， 重力 measurement 不会改变。

所以仅靠 IMU：

$$
Yaw
$$

通常仍然没有绝对参考。

### 19. VIO 中常见的 Gauge Freedom

对于 Visual-Inertial Odometry：

IMU 给 gravity。

所以：

- Roll 可观
- Pitch 可观

但是：

- global position 不可观
- global yaw 不可观

因此通常还有：

$$
\boxed{ 4\ unobservable\ DOF }
$$

即：

$$
x,y,z
$$

加：

$$
yaw
$$

### 20. 这为什么很重要？

因为如果 estimator 错误地认为这些方向是 observable，

它可能会：

> 错误地减少 covariance。

也就是说系统会越来越自信：

$$
P\downarrow
$$

但其实这些方向根本没有 measurement information。

结果就是：

Estimator inconsistency 这在 VIO / EKF 系统里特别重要。

### 21. Monocular Visual SLAM 还有一个更麻烦的东西

如果是单目相机：

Monocular  Camera 仅通过图像，

通常连绝对尺度：

$$
Scale
$$

都不知道。

假设真实世界：

```
相机移动 1 m
物体距离 5 m
```

如果全部乘 10：

```
相机移动 10 m
物体距离 50 m
```

投影图像可能完全一样。

因为透视投影本质：

$$
u=f\frac{X}{Z}
$$

如果：

X →  sX Z →  sZ

那么：

$$
\frac{sX}{sZ}=\frac{X}{Z}
$$

所以图像不变。

### 22. 因此 Monocular SLAM 有 Scale Ambiguity

它只能得到：

up to scale

也就是说地图形状可以正确：

```
房间长 : 宽 = 2 : 1
```

但到底是：

$$
2m\times1m
$$

还是：

$$
20m\times10m
$$

单目视觉本身不知道。

### 23. 所以 Monocular SLAM 的 Gauge 更大

普通三维 SLAM：

$$
SE(3)
$$

对应：

$$
6\ DOF
$$

而 monocular SLAM：

$$
Sim(3)
$$

还多一个：

$$
Scale
$$

所以总共：

$$
\boxed{ 7\ DOF }
$$

即：

$$
3\ translation + 3\ rotation + 1\ scale
$$

### 24. Sim(3) 是什么？

你可能以后会经常看到：

$$
Sim(3)
$$

它比：

$$
SE(3)
$$

多一个 scale：

$$
s
$$

变换：

$$
p' = sRp+t
$$

而普通刚体变换：

$$
SE(3)
$$

是：

$$
p' = Rp+t
$$

没有 scale。

这也是为什么一些 monocular SLAM loop closure 会使用：

$$
Sim(3)
$$

去修正：

scale drift

### 25. Stereo Camera 为什么没有这个问题？

因为 stereo 有 baseline：

$$
b
$$

baseline 是一个真实物理长度。

深度：

$$
Z=\frac{fb}{d}
$$

其中：

- $$f$$：焦距
- $$b$$：baseline
- $$d$$：disparity

因此 metric scale 可以恢复。 这点和你现在做 stereo 很直接相关。

双目系统天然拥有：

metric scale 而单目没有。

### 26. RGB-D 也一样

RGB-D 直接给：

$$
depth
$$

单位通常就是：

$$
m
$$

所以 scale 也是 observable 的。

### 27. Monocular + IMU 呢？

IMU 中有：

acceleration

真实物理单位：

$$
m/s^2
$$

并且 gravity magnitude：

$$
9.81m/s^2
$$

提供 metric information。

因此经过足够运动激励后：

scale can become observable 所以 monocular VIO 可以恢复 metric scale。

### 28. 但注意“有 IMU”不代表立刻可观

这里又回到我们 Part II 讲过的：

Excitation 如果机器人完全静止， 或者运动非常退化， 一些状态还是很难估。 比如 IMU bias、scale 等。

所以：

> 是否 observable 不只取决于有没有 sensor，也取决于机器人怎么运动。

### 29. Degenerate Motion

举个经典例子。

单目相机如果只做纯旋转：

```
camera
↻
```

没有 translation。 那你几乎无法通过 parallax triangulate depth。 因为 triangulation 需要 baseline。

于是 depth：

$$
Z
$$

变得不可观或者极弱可观。

这就是：

Degenerate Motion

## Gauge、退化与弱可观测性

### 30. 这和 Gauge Freedom 不完全一样

要区分两个概念。

#### Gauge Freedom

是系统结构上天然存在的：

例如：

global translation 无论机器人怎么运动都没有绝对参考。

#### Degeneracy

是因为当前 sensor configuration 或 motion 导致的信息不足。

例如：

pure rotation 导致无法 triangulate depth。 如果以后产生 translation， 这个问题可能消失。

所以：

Gauge Freedom ≠  Degeneracy

### 31. Weak Observability

还有第三种情况：

不是完全不可观， 也不是完全没问题。

而是：

information is very weak

比如相机向前运动：

```
→
```

正前方非常远的 feature。 它的 image motion 很小。 所以 depth 对 measurement 的影响非常小。

数学上：

$$
\frac{\partial z}{\partial Z}
$$

很小。

于是：

$$
Depth
$$

虽然理论上 observable， 但估计得很差。

这就是我们之前说的：

> Observability 是理论 Yes/No，而工程上还有 information strength。

### 32. 一个非常好的三层区分

以后判断一个 state 时，可以按这三个层次：

#### Level 1

Unobservable 根本没有信息。

例如：

SLAM global translation

#### Level 2

Observable but weak 理论有信息，但 SNR 很低。

例如：

far depth

#### Level 3

Strongly observable measurement 对 state 非常敏感。 例如有较大 stereo disparity 的近距离目标。 这个分类在工程里非常实用。

### 33. 为什么 Loop Closure 不能消除 Gauge Freedom？

这是一个很好的思考题。

你可能觉得：

> Loop closure 给了很强的全局约束，那是不是就知道绝对位置了？

不是。

假设整个 trajectory 已经形成完美闭环：

```
┌──────┐
│      │
└──────┘
```

你仍然可以把整个闭环：

- 向右平移
- 向上平移
- 整体旋转

所有 loop constraints 仍然成立。

所以：

Loop Closure reduces drift, but does not create an absolute frame 这句话非常重要。

### 34. Loop Closure 到底解决什么？

它解决：

relative inconsistency

例如：

机器人走了一圈以后：

$$
x_{100}
$$

和：

$$
x_0
$$

本来应该重合。

但估计结果：

```
x0 ●

        ● x100
```

Loop closure 会告诉 optimizer：

$$
x_{100}\approx x_0
$$

于是把 trajectory 拉回来。

但最终整个地图位于：

$$
(0,0)
$$

还是：

$$
(100,100)
$$

并不重要。

## 先验、绝对观测与估计一致性

### 35. Anchor 和 Prior

除了直接 fix 一个 pose，

还可以给一个 prior：

$$
x_0\sim\mathcal N(\bar x_0,\Sigma_0)
$$

也就是：

> 我认为第一帧大概在这里。

如果：

$$
\Sigma_0
$$

非常小， 就相当于强约束。

甚至：

$$
\Sigma_0\rightarrow0
$$

就接近 fixed pose。

### 36. Fix 和 Prior 有什么区别？

#### Fix

$$
x_0=\text{constant}
$$

优化器完全不允许它变化。

#### Prior

$$
x_0\approx \bar x_0
$$

允许变化，

但变化会增加 cost：

$$
r_{prior} = x_0-\bar x_0
$$

所以 prior 是一个软约束。

### 37. GPS 本质上是什么？

在 Factor Graph 里，

GPS measurement 本质就是一个：

Absolute Position Factor

比如：

$$
r_{GPS} = p_t-p_{GPS}
$$

它会把 trajectory 锚定到真实世界坐标。

所以从 graph perspective：

```
relative factors
+
absolute factor
```

Gauge Freedom 就会部分或者全部消失。

### 38. Magnetometer 呢？

Magnetometer 可以提供 heading reference。

理论上它可以约束：

$$
Yaw
$$

于是：

global yaw 也可能变得 observable。 当然现实里磁场干扰很多，所以工程上要谨慎。

### 39. 一个很实用的传感器可观测性表

大致可以这样理解：

|Sensor|能提供的绝对参考|
|---|---|
|Camera only|基本没有|
|Stereo|Metric scale|
|RGB-D|Metric scale|
|IMU|Gravity direction + metric acceleration|
|GPS|Global position|
|Magnetometer|Heading|
|Wheel odometry|Relative motion|
|LiDAR|Relative geometry|

所以完整机器人系统往往通过传感器融合逐渐消除不同自由度的不确定性。

### 40. 为什么这一章对工程特别重要？

因为很多“算法崩了”的问题，

其实不是：

```
optimizer 写错
```

而是：

Problem itself is underconstrained

比如：

- 没有 anchor
- 没有足够 parallax
- 纯旋转
- 特征全在同一平面
- IMU 没激励
- sensor configuration 有退化

你如果不知道 observability， 可能一直调参数。 但其实根本没有足够 information。

### 41. 一个很典型的工程判断

以后遇到 estimator 不稳定，你可以先问：

#### 第一问

这个 state 理论上 observable 吗？

如果 No：

> 别调参数，没用。

#### 第二问

如果 observable：

当前 measurement information 强吗？

例如：

- baseline 是否够大
- feature 是否分布合理
- motion excitation 是否充分

#### 第三问

才是：

> 算法、noise、threshold、optimizer 是否合理。

这个思考顺序非常重要。

### 42. 和上一章 EKF-SLAM 连起来

上一章我们讲：

$$
P
$$

表示 uncertainty。 现在如果某个方向完全不可观，

理论上这个方向的 uncertainty：

> 不应该因为相对 measurement 而神奇消失。

但 EKF linearization 如果处理不好， 可能引入虚假的信息。

于是 covariance：

$$
P
$$

错误缩小。

这就是经典：

EKF inconsistency 问题的重要来源之一。

### 43. 为什么现代 VIO 很重视 Observability-Constrained EKF？

像经典 MSCKF 系列等方法，

一个很重要的问题就是：

> 线性化不能破坏系统原本的 unobservable subspace。

如果真实系统中 global yaw 不可观， 但线性化之后 estimator 错误地产生了 yaw information， 那 covariance 就会越来越过度自信。

所以一些方法会特别保持：

Unobservable directions 不被错误更新。

### 44. 这和数学里的 Rank 有关系

Observability 最终往往会落到：

$$
rank
$$

如果 information matrix：

$$
H
$$

或者 observability matrix：

$$
\mathcal O
$$

不满秩：

$$
rank(\mathcal O)<n
$$

说明存在某些 state direction：

$$
v
$$

无法从 measurement 区分。

也就是：

$$
\mathcal O v=0
$$

这就是：

null space

### 45. 一个你以后看论文非常有用的关键词

如果论文里出现：

- null space
- unobservable subspace
- gauge freedom
- rank deficiency
- gauge fixing
- anchor
- prior
- degeneracy

它们其实都围绕同一个大问题：

Measurement 到底能约束 State 的哪些方向？

### 46. SLAM 最漂亮的一个观点

我们甚至可以换个角度看 SLAM。

SLAM 并不是：

> “我要估计所有 state。”

而是：

>  **我要估计 measurement 真正允许我估计的部分。**

剩下那些无法从 measurement 判断的自由度，

要么：

- 人为固定
- 引入 prior
- 引入额外 sensor

否则它就必须保持自由。

### 47. 本章核心总结

你需要牢牢记住下面几件事。

第一：

SLAM 的 measurement 主要提供相对约束 因此绝对坐标通常天然不可观。

第二：

二维 SLAM 通常有：

$$
\boxed{ 3\ DOF }
$$

Gauge Freedom：

$$
x,y,\theta
$$

第三：

三维 metric SLAM 通常有：

$$
\boxed{ 6\ DOF }
$$

即整个：

$$
SE(3)
$$

第四：

Monocular SLAM 还多一个：

$$
Scale
$$

因此通常是：

$$
\boxed{ 7\ DOF\ similarity\ gauge }
$$

第五：

固定第一帧：

$$
T_0=I
$$

并不是获得了真实绝对坐标，

而只是：

Gauge Fixing

第六：

Gauge Freedom

和：

Degenerate Motion 不是一回事。 前者是系统结构天然不可观。 后者是当前 measurement / motion 不够丰富。

> 修订说明：Hessian 的数值因代价是否含 1/2 而相差常数，不影响零空间结论。固定第一帧消除连通 metric SE(3) 图的全局位姿 gauge；单目系统还需选定尺度，欠约束或多个图组件也需分别处理。惯性观测提供重力方向／尺度信息的结论依赖充分激励与模型成立。

## 思考题

### Q1：为什么两套完全不同世界坐标的 SLAM map，可以同样正确？

**参考答案**

因为 SLAM measurement 主要描述：

relative geometry

只要两张地图通过同一个刚体变换：

$$
T
$$

就能互相转换， 它们的所有内部相对关系完全一致。 所以它们代表的是同一个物理解。


### Q2：固定第一帧以后，第一帧真的就成为“世界真实原点”了吗？

**参考答案**

不是。

只是人为定义：

$$
World\ Frame = First\ Camera\ Frame
$$

这是一种坐标 convention。


### Q3：Loop Closure 为什么能消除 drift，却不能消除 global gauge？

**参考答案**

因为 loop closure 增加的是：

relative constraints

例如：

$$
T_{0,100}
$$

但整个系统整体做一个 global transform 后， 所有 relative constraints 仍然不变。


### Q4：单目为什么没有 metric scale？

**参考答案**

因为投影：

$$
u=f\frac{X}{Z}
$$

对：

$$
X,Z
$$

同时乘 scale：

$$
s
$$

结果不变。

所以图像无法区分：

$$
1m
$$

和：

$$
10m
$$

的同比例世界。


### Q5：为什么双目可以恢复 scale？

**参考答案**

因为 baseline：

$$
b
$$

是已知真实长度。

$$
Z=\frac{fb}{d}
$$

因此 disparity 可以恢复 metric depth。


### Q6：纯旋转为什么对单目 depth 很危险？

<details>

<summary>参考答案</summary>

因为没有 translational baseline， 没有足够 parallax。 不同 depth 的点可能产生非常类似的 rotational image motion， 所以 depth information 极弱甚至不可观。

</details>

### Q7：如果 optimization 的 Hessian singular，你第一反应应该是什么？

<details>

<summary>参考答案</summary>

不要立刻怀疑：

> optimizer 有 bug。

应该先检查：

是否存在未处理的 Gauge Freedom 或系统欠约束 这在 SLAM 中非常常见。

</details>

## 相关章节与来源

- 上一章：[Landmark SLAM 与 EKF-SLAM](ekf-slam.md)
- 下一篇：[Visual SLAM 前端](visual-frontend.md)
- 来源：本次新增 Part IV Chapter 39 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
