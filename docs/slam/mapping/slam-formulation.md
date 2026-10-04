---
title: SLAM 问题定义
description: 怎样把轨迹与地图写成相互依赖的联合估计问题？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 37
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# SLAM 问题定义

## 本章目标

怎样把轨迹与地图写成相互依赖的联合估计问题？

## 前置知识

[已知地图中的定位](../spatial/localization.md)、[Part III 回顾](../spatial/summary.md)。

## 定义与假设

X 表示轨迹，M 表示地图，Z 表示观测，U 表示运动输入；联合状态也会在正文中记为 X，需按上下文区分。MAP 优化需要先验；仅凭相对观测得到的解存在坐标基准自由度。

## 核心问题
 本章先说明 SLAM 为什么是联合估计，再理解模块怎样形成。

因为很多人学 SLAM 时会直接进入：

- ORB
- PnP
- ICP
- Bundle Adjustment
- Factor Graph
- Loop Closure

最后会变成：

> “我大概知道每个模块干什么，但不知道为什么 SLAM 必须长成这个样子。”

这一章解决的就是这个问题。

## 从定位与建图到联合状态

### 1. SLAM 的全称其实已经把问题说完了

SLAM：

>  **Simultaneous Localization and Mapping**

中文一般翻译成：

>  **同时定位与建图**

关键就在  **Simultaneous** 。 因为单独的 Localization 和 Mapping 都没那么麻烦。

#### 情况 A：地图已知

假设机器人已经有一张非常准确的地图。

机器人看到：

```
墙
门
路标
柱子
```

然后问：

> “根据我现在看到的这些东西，我在地图哪个位置？”

这是：

Localization 也就是定位。

未知量主要是机器人位姿：

$$
x_t
$$

#### 情况 B：机器人位置已知

反过来。

假设机器人每一时刻的位姿都由某种“上帝级 GPS”精确告诉你：

$$
x_t
$$

机器人看到一个物体。

你就可以把这个物体投到世界坐标系：

$$
p_w = T_{wc}p_c
$$

于是地图可以慢慢建立出来。

这叫：

Mapping

#### 真正麻烦的是 SLAM

现实中：

```
地图不知道
+
自己的位置也不知道
```

于是：

> 我想知道自己在哪，需要地图。

但：

> 我想建立地图，又需要知道自己在哪。

形成一个循环依赖：

Pose  ↔  Map 这就是 SLAM 最核心的困难。

### 2. 一个非常直观的例子

想象你被蒙着眼睛送进一个完全陌生的办公室。

你睁眼之后看到：

```
左边一个沙发
前面一根柱子
右边一盆植物
```

于是脑子里建立一个局部认识：

```
      柱子

沙发        植物

       我
```

然后你往前走几步。

再次看到：

```
柱子在左后方
植物在右边
新看到一个门
```

你会同时做两件事情。

第一件：

> “根据柱子和植物的位置变化，我应该移动到这里了。”

这是  **Localization** 。

第二件：

> “门应该位于整个环境的这个位置。”

这是  **Mapping** 。 问题来了。

如果你第一次估计自己的移动位置错了：

```
真实移动 1.0 m
你认为移动 1.1 m
```

那么你加入地图里的“门”位置也会错。

于是：

Pose Error  →  Map Error

之后你又用这张错误地图定位：

Map Error  →  Pose Error 两者相互影响。 这就是为什么 SLAM 本质上是一个 **联合估计问题** 。

### 3. SLAM 的 State 是什么？

Part II 我们反复强调一句话：

>  **先定义 State，再谈算法。**

所以现在第一件事情不是问：

> 用 ORB 还是 SuperPoint？

而是问：

> SLAM 到底要估计什么？

最简单的 SLAM 状态可以写成：

$$
X = \left[ x_0, x_1, x_2, \dots, x_T, m_1, m_2, \dots, m_N \right]
$$

其中：

$$
x_t
$$

是机器人在第 $$t$$ 时刻的位姿。

而：

$$
m_j
$$

是地图中的第 $$j$$ 个 Landmark。

因此：

$$
\boxed{ State = Trajectory + Map }
$$

### 4. Pose 是什么？

对于移动机器人，简单一点可以是：

$$
x_t = [x,y,\theta]
$$

也就是二维：

```
x
y
yaw
```

但三维机器人通常需要：

$$
T_t \in SE(3)
$$

包含：

$$
R_t,\quad t_t
$$

也就是：

```
Rotation
+
Translation
```

可以写成齐次变换矩阵：

$$
T = \begin{bmatrix} R & t\\ 0 & 1 \end{bmatrix}
$$

这个我们以后在 Visual SLAM、BA、Pose Graph 中都会不断看到。

现在只要记住：

$$
x_t = \text{robot pose}
$$

即可。

### 5. Map 又是什么？

这件事情其实没有唯一答案。

早期 SLAM 很喜欢用：

$$
m_j=[X_j,Y_j,Z_j]
$$

也就是一些 3D Landmark。

例如：

```
墙角
桌角
纹理点
路标
```

于是地图就是：

$$
M= \{m_1,m_2,\dots,m_N\}
$$

这叫：

> Landmark Map

但现代 SLAM 的 Map 可以完全不同。

例如：

#### Sparse Map

一些离散特征点：

```
.      .
   .
       .   .
 .
```

ORB-SLAM 就很典型。

#### Dense Map

几乎每个位置都有几何：

```
Point Cloud
Voxel
TSDF
Mesh
```

#### LiDAR Map

例如：

```
Point Cloud
Surfel
Voxel Map
```

甚至可以有：

#### Semantic Map

地图元素可能是：

```
chair
table
door
wall
car
```

所以：

>  **SLAM 不等于建立某一种地图。**

更准确地说：

$$
\boxed{ SLAM = Estimate trajectory + some representation of environment }
$$

### 6. SLAM 的 Observation 是什么？

现在按照我们以前的框架：

```
State
Prediction
Observation
Correction
```

State 已经知道：

$$
X=\{poses,map\}
$$

那么 Observation 是什么？ 取决于传感器。

#### Camera

例如图像中的 feature：

$$
z_{t,j}
$$

表示：

> 在第 $$t$$ 帧，我观察到了 Landmark $$j$$。

如果 Landmark 世界坐标：

$$
P_j^w
$$

当前相机位姿：

$$
T_{cw}
$$

理论上可以预测它应该出现在图像哪里：

$$
\hat z_{t,j} = \pi(T_{cw}P_j^w)
$$

其中：

$$
\pi()
$$

就是相机投影模型。

然后实际观察：

$$
z_{t,j}
$$

和预测：

$$
\hat z_{t,j}
$$

比较。

得到 residual：

$$
r_{t,j} = z_{t,j}-\hat z_{t,j}
$$

这就是 Part II、III 那套东西。

### 7. SLAM 其实就是我们之前那套估计框架的巨大版本

以前我们讲：

State  →  Prediction  →  Observation  →  Residual  →  Correction SLAM 一模一样。

例如机器人从：

$$
x_t
$$

根据轮速计 / IMU / motion model：

$$
x_{t+1}^{pred}=f(x_t,u_t)
$$

得到预测位置。

然后相机看到 Landmark：

$$
z_{t+1}
$$

预测它应该看到：

$$
\hat z_{t+1}=h(x_{t+1},m)
$$

计算：

$$
r=z-\hat z
$$

最后修正：

$$
x,\quad m
$$

所以：

SLAM 没有发明一种新的估计理论

它只是把我们之前学的 State Estimation 扩展成：

>  **机器人轨迹 + 环境地图的联合状态估计。**

这就是 Part I–III 和 Part IV 真正接上的地方。

## 跨时间约束与 SLAM 问题

### 8. 为什么需要历史 Pose？

既然机器人现在只需要知道：

$$
x_t
$$

为什么很多 SLAM 系统还保存：

$$
x_0,x_1,\dots,x_t
$$

这么多历史位姿？ 原因马上会出现。

假设：

```
t0
机器人看到 A

↓

t1

↓

t2

↓

t3

↓

t100
再次看到 A
```

机器人发现：

> “等等，这里好像就是我之前来过的地方。”

这就是：

Loop Closure

假设里程计累计误差导致：

```
理论轨迹：

─────────
         │
         │
─────────

实际估计：

─────────
          \
           \
────────────
```

机器人重新看到 A 后发现：

> t100 应该和 t0 在同一个位置附近。

于是产生一个约束：

$$
x_{100} \leftrightarrow x_0
$$

如果想利用这个约束修正过去的误差，你必须保留历史状态。

于是 SLAM 很自然变成：

Trajectory Optimization

这也就是后面：

- Bundle Adjustment
- Factor Graph
- Pose Graph

为什么会成为 SLAM 核心。

### 9. Odometry 和 SLAM 到底差在哪里？

很多人会把：

```
Visual Odometry
Visual SLAM
```

混在一起。 其实区别非常清楚。

#### Odometry

核心目标：

$$
x_t \rightarrow x_{t+1}
$$

不断估计相邻运动：

```
Frame 1 → Frame 2
Frame 2 → Frame 3
Frame 3 → Frame 4
```

于是：

$$
T_{04} = T_{01} T_{12} T_{23} T_{34}
$$

问题是每一步都有误差。

例如每次只有：

$$
0.1\%
$$

误差。 累计 1000 次以后也会出现明显 drift。

所以：

Odometry 天生会漂

#### SLAM

SLAM 会加入额外约束。

例如：

```
x0 ─ x1 ─ x2 ─ x3 ─ ... ─ x100
│                         │
└──────── loop ───────────┘
```

于是：

$$
x_{100}
$$

不能随便漂。

因为它还必须满足：

$$
x_{100}\approx x_0
$$

所以 SLAM 可以利用：

>  **空间中的重复观测来修正时间上的累计误差。**

这是一个清晰的思想。

### 10. 所以 Loop Closure 为什么这么重要？

想象机器人沿走廊运行：

```
A → B → C → D → E
```

每段都有一点误差。

最后估计变成：

```
A → B' → C' → D' → E'
```

如果机器人一直不回头：

> 你很难知道到底哪里漂了。

但如果：

```
A → B → C → D
↑             ↓
←──── E ←─────
```

最后回到 A。

突然获得一个强约束：

$$
x_E \approx x_A
$$

整个轨迹之前累积的误差都暴露出来了。

所以 Loop Closure 本质上不是：

> “发现我来过这里。”

这个描述太表面。

更深一层是：

产生一个长时间跨度的几何约束

### 11. SLAM 可以用概率形式怎么描述？

Part II 学过 Bayesian Estimation。

SLAM 的最终目标可以写成：

$$
p(X,M|Z,U)
$$

其中：

$$
X = \text{trajectory}
$$

$$
M = \text{map}
$$

$$
Z = \text{observations}
$$

$$
U = \text{motion measurements}
$$

意思就是：

> 给定所有运动信息和所有传感器观测，机器人轨迹和地图最可能是什么？

如果采用最大后验：

$$
X^*,M^* = \arg\max_{X,M} p(X,M|Z,U)
$$

这就是：

$$
MAP
$$

Maximum A Posteriori。 后面你会看到一个非常重要的变化。

概率问题：

$$
\arg\max p(X|Z)
$$

通过负对数等操作，会变成：

$$
\arg\min \sum_i \|r_i(X)\|_{\Sigma_i}^2
$$

也就是：

>  **最小化所有测量 Residual。**

然后：

```
SLAM
↓
Maximum Likelihood / MAP
↓
Nonlinear Least Squares
↓
Factor Graph
↓
Optimization
```

整个现代 SLAM 后端就出来了。 Chapter 42–45 我们会把这里彻底拆开。

### 12. 一个小型 SLAM 问题

假设机器人有三个 Pose：

$$
x_0,x_1,x_2
$$

环境中两个 Landmark：

$$
m_A,m_B
$$

观测关系：

```
x0 sees A

x1 sees A
x1 sees B

x2 sees B
```

画出来：

```
       A           B
      / \         / \
     /   \       /   \
   x0 --- x1 --- x2
```

这里其实已经隐藏着整个 SLAM 的结构。 每条线就是一个约束。

例如：

$$
x_0 \leftrightarrow x_1
$$

可能来自里程计。

而：

$$
x_0 \leftrightarrow A
$$

来自相机。

于是整个问题就是：

> 找一组 $$x_0,x_1,x_2,A,B$$，让所有约束尽可能同时成立。

换句话说：

找到一个对所有观测最自洽的世界解释 这句话，我觉得比“同时定位与建图”更能解释 SLAM 的本质。

### 13. 为什么不能一帧一帧独立算？

假设：

```
Frame 1
Frame 2
Frame 3
```

如果每一帧独立估计：

$$
x_1
$$

$$
x_2
$$

$$
x_3
$$

那么你实际上丢掉了一个极其重要的信息：

>  **它们是同一个机器人连续产生的。**

例如：

$$
x_1\rightarrow x_2
$$

和：

$$
x_2\rightarrow x_3
$$

存在运动连续性。

同一个 Landmark：

$$
m_A
$$

还可能同时被：

$$
x_1,x_2,x_3
$$

看到。

因此 SLAM 真正利用的是：

跨时间的信息关联

这也是为什么：

> Data Association

会成为 SLAM 一个巨大的问题。

## 前后端与系统分工

### 14. Data Association 是什么？

假设 Frame 1 看到：

```
● A
```

Frame 10 又看到：

```
● ?
```

问题是：

> 这是同一个 A，还是另一个点 B？

如果认为是同一个：

$$
z_1,z_{10} \rightarrow m_A
$$

就产生跨时间约束。

如果认错：

B  →  A 整个优化系统可能被一个错误约束拉坏。 所以 SLAM 有两个不同层面的问题。

#### Continuous Estimation

例如：

$$
x=1.52m
$$

还是：

$$
x=1.57m
$$

这是连续变量优化。

#### Discrete Association

这个 feature：

```
是 A？
还是 B？
还是新 Landmark？
```

这是离散问题。 现代 SLAM 大量工程难度，其实来自后者。

以后讲：

- Feature Matching
- Tracking
- Loop Closure
- Place Recognition

都会重新遇到它。

### 15. Front-end 和 Back-end 为什么出现了？

现在其实已经可以自然推导出来。

机器人拿到原始数据：

```
Image
LiDAR
IMU
Wheel Encoder
```

首先需要回答：

> 我从传感器里提取出了什么约束？

这是：

Front-end

例如：

```
Feature Detection
Feature Matching
Optical Flow
ICP
PnP
Data Association
```

它们最终产生：

```
x1 ↔ x2
x2 ↔ x3
x1 ↔ Landmark A
x3 ↔ Landmark B
```

然后出现第二个问题：

> 有了这些约束以后，什么状态最合理？

这是：

Back-end

例如：

```
Bundle Adjustment
Factor Graph Optimization
Pose Graph Optimization
```

所以不要机械记：

> SLAM = Front-end + Back-end。

真正的逻辑是：

```
Sensor data

↓

Front-end
“数据里有什么约束？”

↓

Constraints

↓

Back-end
“什么 State 最符合这些约束？”

↓

Trajectory + Map
```

这才是因果关系。

### 16. 为什么还需要 Local Mapping？

如果机器人运行 3 小时：

```
Frame 1
Frame 2
...
Frame 300000
```

难道每收到一帧，都重新优化：

$$
x_1\dots x_{300000}
$$

以及几十万个 Landmark？ 显然不现实。

所以 SLAM 系统自然会发展出：

```
Current Frame
↓
Tracking

Recent Frames
↓
Local Map

Important Frames
↓
Keyframes

Long-term Constraints
↓
Global Optimization
```

这也是后面 Chapter 41：

> Keyframes & Local Mapping

的核心来源。 并不是因为 ORB-SLAM 作者觉得 Keyframe 很酷。

而是计算复杂度逼着 SLAM 必须：

选择性保留信息

### 17. 一套完整 SLAM Pipeline 现在已经可以自己推出来了

暂时完全不考虑任何具体算法名称。

机器人首先获得：

$$
Sensor
$$

↓

处理数据：

Preprocessing

↓

寻找对应关系：

Data Association

↓

估计短期运动：

Odometry

↓

保存关键状态：

Keyframes

↓

构建局部地图：

Local Mapping

↓

统一优化状态：

Backend Optimization

↓

检测以前去过的地方：

Loop Closure

↓

修正长期累计误差：

Global Optimization

最终：

$$
Trajectory + Map
$$

也就是：

```
Sensors
   ↓
Preprocessing
   ↓
Front-end
   ↓
Odometry / Tracking
   ↓
Keyframes + Local Map
   ↓
Backend Optimization
   ↓
Loop Closure
   ↓
Global Optimization
   ↓
Trajectory + Map
```

Part IV 后面几乎就是沿着这条链逐个展开。

### 18. 一个容易混淆的地方：SLAM 不是“地图算法”

名字里虽然有 Mapping，但我希望你现在建立一个更正确的认知：

>  **SLAM 的中心不是 Map，而是 Consistency。**

机器人希望：

```
Motion
Visual Observation
LiDAR Observation
IMU
Loop Closure
Map
```

彼此尽可能一致。

因此最终是：

$$
\arg\min_X \sum_i r_i(X)^T \Sigma_i^{-1} r_i(X)
$$

所有信息都通过 residual 对 State 提要求。

所以 SLAM 更接近：

>  **一个大型的、多传感器、多时刻的状态一致性优化问题。**

而不是：

> “机器人边走边画地图。”

后者虽然直观，但理解深度差很多。

## 与状态估计主线的连接

### 19. 和 Part II 的知识重新连一次

你之前已经学过：

#### State

SLAM：

$$
X=\{poses,map\}
$$

#### Observation

Camera / LiDAR / IMU：

$$
z
$$

#### Measurement Model

$$
\hat z=h(X)
$$

#### Residual

$$
r=z-h(X)
$$

#### Uncertainty

$$
\Sigma
$$

#### Information strength

$$
\Sigma^{-1}
$$

#### Observability

某个状态到底能不能由现有观测确定。

#### Multi-hypothesis / Data Association

这个观测到底属于哪个 Landmark。

所以你会发现：

> 我们其实早就在学 SLAM。

只是 Part II / III 把这些概念一个个拆开，现在 Part IV 第一次把它们装进一个完整机器人系统里。

### 20. 本章最重要的五句话

如果 Chapter 37 最后只记住五句话，我希望是这五句：

 **第一句**

$$
\boxed{ SLAM = Trajectory + Map 的联合估计 }
$$

 **第二句**

Localization 和 Mapping 互相依赖：

Pose  ↔  Map  **第三句**

SLAM 的基本计算模式仍然是：

Prediction  →  Observation  →  Residual  →  Correction  **第四句**

现代 SLAM 后端本质上是在寻找：

最符合所有约束的一组状态  **第五句**

完整系统可以理解成：

Sensor  →  Constraint Generation  →  State Optimization 这句话尤其重要。 以后无论看到 ORB-SLAM、VINS、LIO-SAM、FAST-LIO、DROID-SLAM，先别被算法名称吓住。

第一反应应该是：

>  **它的 State 是什么？**

>  **它有哪些 Measurement / Constraint？**

>  **这些 Constraint 怎么产生？**

>  **最后 State 怎么优化？**

只要能回答这四个问题，一个陌生 SLAM 系统基本就已经拆掉一半了。

> 修订说明：保存全部历史 Pose 并非所有 SLAM 的必要条件。Filtering 可将历史压缩进当前联合 Belief；关键帧与 Smoothing 保留部分历史以便重新线性化。回环能提供长期约束，但不是判定一个系统是否为 SLAM 的唯一标准。

## 本章思考题

先独立回答，再展开参考答案。

### Q1：如果机器人拥有完全精确的 Pose，还需要做 SLAM 吗？

<details>

<summary>参考答案</summary>

严格来说不需要。

因为 Mapping 可以直接变成：

$$
p_w=T_{wc}p_c
$$

这是纯 Mapping。

SLAM 困难正是因为：

$$
Pose
$$

本身也是未知量。

</details>

### Q2：为什么 Odometry 再准确，也不等于 SLAM？

<details>

<summary>参考答案</summary>

因为 Odometry 主要依赖：

$$
x_t\rightarrow x_{t+1}
$$

这种局部约束。

误差会累计：

$$
\epsilon_1+\epsilon_2+\dots+\epsilon_N
$$

而 SLAM 可以通过：

Loop Closure 等长时间跨度约束重新修正过去状态。

</details>

### Q3：SLAM 为什么经常保存 Keyframe，而不是只保存当前 Pose？

<details>

<summary>参考答案</summary>

因为未来的新观测可能反过来修正过去。

如果：

$$
x_{100}
$$

重新观察到：

$$
x_{20}
$$

附近的场景，就可能需要优化：

$$
x_{20}\dots x_{100}
$$

所以历史状态不能全部扔掉。

但全部保留计算量又太高，于是产生：

Keyframe 这种信息压缩。

</details>

### Q4：为什么错误的 Loop Closure 特别危险？

<details>

<summary>参考答案</summary>

因为它不是普通的局部误差。 一个错误 feature match 可能只影响附近几个状态。

但错误 Loop Closure 会建立类似：

$$
x_{20}\leftrightarrow x_{2000}
$$

这种跨越大量时间的强约束。 Backend 为了满足这个错误约束，可能把整个轨迹扭曲。

所以 Loop Closure 的核心难题之一其实是：

Data Association Reliability

</details>

### Q5：一句话区分 Front-end 与 Back-end？

<details>

<summary>参考答案</summary>

我推荐你这样理解：

Front-end：从 Sensor Data 中构造约束 Back-end：利用约束估计 State 比“前端负责感知、后端负责优化”更准确。

</details>

## 相关章节与来源

- 上一章：[扫描匹配与 ICP](../spatial/scan-matching-icp.md)
- 下一篇：[Landmark SLAM 与 EKF-SLAM](ekf-slam.md)
- 来源：本次新增 Part IV Chapter 37 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
