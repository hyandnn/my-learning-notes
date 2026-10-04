---
title: Landmark SLAM 与 EKF-SLAM
description: 机器人和地图怎样通过联合协方差相互校正？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 38
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# Landmark SLAM 与 EKF-SLAM

## 本章目标

机器人和地图怎样通过联合协方差相互校正？

## 前置知识

[SLAM 问题定义](slam-formulation.md)、[EKF](../probabilistic/ekf.md)、[观测模型](../spatial/sensor-models.md)。

## 定义与假设

本章采用二维位姿 [x,y,θ] 与静态二维地标，联合状态维度为 3+2N。距离单位 m，角度单位 rad，bearing 创新须 wrap；观测噪声与预测误差独立，数据关联已验证。Gaussian Belief 与 EKF 更新是局部近似。

## 核心问题


这一章非常重要，因为它是第一个真正把：

$$
\text{机器人位姿} + \text{地图} + \text{Observation} + \text{Uncertainty}
$$

全部装进同一个数学框架里的 SLAM。 而且我建议你不要把 EKF-SLAM 只当成“一个后来不太常用的老算法”。

它真正的价值是：

>  **它能非常直观地解释，为什么机器人位姿的不确定性会传给地图，而地图反过来又能帮助机器人定位。**

这正是 SLAM 最核心的那个：

Pose  ↔  Map

## 联合状态与运动预测

### 1. 先从最简单的问题开始

假设机器人在一个二维平面运动。

它的状态是：

$$
x_r= \begin{bmatrix} x\\ y\\ \theta \end{bmatrix}
$$

表示机器人：

- 横坐标 $$x$$
- 纵坐标 $$y$$
- 朝向 $$\theta$$

现在环境里有两个 landmark：

$$
m_1= \begin{bmatrix} m_{1x}\\ m_{1y} \end{bmatrix}
$$

$$
m_2= \begin{bmatrix} m_{2x}\\ m_{2y} \end{bmatrix}
$$

那么整个 SLAM State 可以直接拼起来：

$$
X= \begin{bmatrix} x\\ y\\ \theta\\ m_{1x}\\ m_{1y}\\ m_{2x}\\ m_{2y} \end{bmatrix}
$$

也就是说：

$$
\boxed{ X= [\text{robot pose},\text{all landmarks}] }
$$

这就是经典 Landmark SLAM 最核心的一步。

### 2. 和普通 Kalman Filter 最大区别是什么？

以前如果做机器人定位，你的状态可能只有：

$$
X= [x,y,\theta]
$$

地图是已知的。 你看到 landmark 之后，只用 landmark 修正机器人位置。

但 EKF-SLAM 中：

地图也是未知量

所以现在测量来了以后，不只是更新：

$$
x,y,\theta
$$

还要更新：

$$
m_1,m_2,\dots
$$

也就是说一个 observation 可能同时改变：

> “我在哪里”

以及：

> “那个 landmark 在哪里”

这非常关键。

### 3. 为什么必须用 EKF，而不是普通 KF？

普通 Kalman Filter 要求系统是线性的。

比如：

$$
x_{t+1}=Ax_t+Bu_t+w_t
$$

$$
z_t=Hx_t+v_t
$$

但机器人运动和 landmark observation 通常都是非线性的。

比如：

$$
x_{t+1} = x_t+v\Delta t\cos\theta_t
$$

$$
y_{t+1} = y_t+v\Delta t\sin\theta_t
$$

这里有：

$$
\sin\theta,\cos\theta
$$

所以不是线性关系。 Measurement 也是一样。

机器人看到一个 landmark，往往测的是：

- 距离 range
- 方位 bearing

假设机器人在：

$$
(x,y)
$$

landmark 在：

$$
(m_x,m_y)
$$

那么距离：

$$
r= \sqrt{(m_x-x)^2+(m_y-y)^2}
$$

角度：

$$
\phi= \operatorname{atan2}(m_y-y,m_x-x)-\theta
$$

这显然也是非线性的。

于是需要：

Extended Kalman Filter 也就是 EKF。

核心思想你应该已经熟悉：

> 在当前估计附近，把非线性函数做一阶线性化。

### 4. EKF-SLAM 的整个流程其实只有两步

整体仍然是：

$$
\boxed{ Prediction + Update }
$$

和普通 Kalman Filter 完全一样。 只是 State 变大了。

### 5. Prediction：机器人移动了

假设机器人当前状态：

$$
X_t
$$

机器人获得 odometry：

$$
u_t
$$

比如：

$$
u_t=[v,\omega]
$$

那么机器人位姿发生变化：

$$
x_{r,t+1} = f(x_{r,t},u_t)
$$

但是地图里的 landmark 呢？ 它们不会因为机器人运动而动。

所以：

$$
m_{j,t+1}=m_{j,t}
$$

因此整个系统 prediction 可以理解为：

$$
X_{t+1} = \begin{bmatrix} f(x_{r,t},u_t)\\ m_1\\ m_2\\ \vdots \end{bmatrix}
$$

注意这里非常重要：

> Prediction 阶段只主动改变 robot pose。

Map 本身不动。

### 6. 一个具体运动模型

比如差速车或者简单二维机器人。

控制量：

$$
u_t= \begin{bmatrix} v\\ \omega \end{bmatrix}
$$

离散时间运动：

$$
x_{t+1} = x_t+ v\Delta t\cos\theta_t
$$

$$
y_{t+1} = y_t+ v\Delta t\sin\theta_t
$$

$$
\theta_{t+1} = \theta_t+ \omega\Delta t
$$

记成：

$$
x_{r,t+1} = f(x_{r,t},u_t)
$$

### 7. 但 EKF 不只是预测 State

它还必须预测：

Covariance

也就是：

$$
P
$$

如果整个 State 有：

$$
3+2N
$$

维，那么：

$$
P\in \mathbb{R}^{(3+2N)\times(3+2N)}
$$

这个矩阵非常重要。

## 协方差与状态相关性

### 8. Covariance Matrix 到底在装什么？

假设只有一个 landmark。

状态：

$$
X= [x,y,\theta,m_x,m_y]^T
$$

那么：

$$
P= \begin{bmatrix} P_{rr} & P_{rm}\\ P_{mr} & P_{mm} \end{bmatrix}
$$

这里：

$$
P_{rr}
$$

表示：

> robot pose 自身的不确定性。

$$
P_{mm}
$$

表示：

> landmark 位置的不确定性。

而真正重要的是：

$$
P_{rm}
$$

以及：

$$
P_{mr}
$$

它们表示：

>  **robot pose 和 landmark 之间的相关性。**

这就是 EKF-SLAM 的灵魂。

### 9. 为什么机器人和 landmark 会产生相关性？

我们来一步一步看。 假设机器人第一次看到一个 landmark。

机器人自己认为：

$$
x=1.0m
$$

然后测得：

> landmark 在自己前方 2m。

于是你估计 landmark：

$$
m_x=3.0m
$$

看起来没问题。

但机器人自己的位置其实不确定：

$$
x=1.0\pm0.2m
$$

那么 landmark 的世界坐标当然也不可能完全确定。

因为：

$$
m_x=x+r
$$

于是 robot pose uncertainty 会传递给 landmark。

如果 robot 实际偏了：

$$
+0.2m
$$

landmark 很可能也一起偏：

$$
+0.2m
$$

所以：

$$
robot
$$

和 landmark 的误差不是独立的。 而是相关的。

### 10. 一个极其重要的直觉

假设机器人自己位置偏右了 20 cm。 那么它之前建立出来的地图，很可能也整体偏右 20 cm。

所以：

```
Robot error:
→ +20 cm

Landmark A:
→ +20 cm

Landmark B:
→ +20 cm
```

它们的误差是一起动的。 这就是 correlation。

可以想象成：

```
Robot ───── Landmark A
   \
    └────── Landmark B
```

不是三个独立的不确定变量。

而是：

> 一整套状态之间互相绑在一起。

### 11. Prediction 时 covariance 会发生什么？

EKF prediction：

$$
P_{t+1} = F_tP_tF_t^T+Q_t
$$

这里：

$$
F_t = \frac{\partial f}{\partial X}
$$

是 Jacobian。

$$
Q_t
$$

是 motion noise。

但因为 map 不动，所以 $$F$$ 的结构大概是：

$$
F= \begin{bmatrix} F_r & 0\\ 0 & I \end{bmatrix}
$$

其中：

$$
F_r
$$

描述 robot motion。

#### 很重要的一点

虽然 map 自己没动：

$$
m_{t+1}=m_t
$$

但 robot 与 map 的 cross-covariance 会跟着变化。

也就是说：

> 你不能说地图不动，所以它和机器人没关系。

它们的状态值可能没更新，但 uncertainty structure 在变。

### 12. Prediction 后 uncertainty 会怎么变化？

机器人在移动。 比如 wheel odometry 有噪声。

因此机器人 position uncertainty 会增加：

$$
P_{rr}\uparrow
$$

直观上：

```
开始：
机器人位置比较确定

↓

走了一段时间

↓

位置越来越不确定
```

这就是：

Dead Reckoning Drift

如果一直只有 prediction，没有 observation：

$$
P
$$

通常会不断增大。

## 观测与联合校正

### 13. 接下来 Observation 来了

假设机器人看到 landmark $$m_j$$。

测量：

$$
z_t= \begin{bmatrix} r\\ \phi \end{bmatrix}
$$

即：

- range
- bearing

measurement model：

$$
z=h(X)+v
$$

### 14. 预测机器人应该看到什么

当前估计里：

$$
Robot=(x,y,\theta)
$$

$$
Landmark=(m_x,m_y)
$$

定义：

$$
\Delta x=m_x-x
$$

$$
\Delta y=m_y-y
$$

预测 range：

$$
\hat r = \sqrt{\Delta x^2+\Delta y^2}
$$

预测 bearing：

$$
\hat\phi = \operatorname{atan2}(\Delta y,\Delta x)-\theta
$$

于是：

$$
\hat z=h(X)
$$

### 15. 然后得到 Innovation / Residual

实际测量：

$$
z
$$

预测：

$$
\hat z
$$

所以：

$$
\boxed{ y=z-\hat z }
$$

注意这里 $$y$$ 经常叫：

innovation 也就是 innovation residual。

假设预测：

$$
\hat r=2.0m
$$

实际：

$$
r=1.8m
$$

那就说明：

$$
r-\hat r=-0.2m
$$

但问题是：

> 为什么少了 20 cm？

可能是机器人位置错了。 也可能是 landmark 位置错了。 甚至二者都有问题。 这就是 SLAM。

### 16. 一个 observation 到底该改 Robot 还是 Map？

答案是：

两个都改 而且具体改多少，取决于 uncertainty。 这和我们之前学过的 Kalman 思想完全一样。

假如：

```
Robot pose 很不确定
Landmark 很确定
```

那么观测来了以后，更倾向于：

> 修 robot。

反过来：

```
Robot 很确定
Landmark 很不确定
```

则更倾向于：

> 修 landmark。

所以 Update 本质仍然是：

谁更不可信，就改谁更多

### 17. EKF Update

Measurement Jacobian：

$$
H_t = \frac{\partial h}{\partial X}
$$

Innovation covariance：

$$
S = HPH^T+R
$$

Kalman Gain：

$$
K = PH^TS^{-1}
$$

状态更新：

$$
X^+ = X^-+Ky
$$

Covariance 更新：

$$
P^+ = (I-KH)P^-
$$

这些公式和普通 EKF 完全一样。

真正不同的是：

> $$X$$ 里面包含全部 robot + map。

因此一次更新可能传播到整个地图。

### 18. 这件事一开始非常反直觉

假设机器人现在观察的是：

Landmark A

为什么：

Landmark B 甚至也可能被更新？

因为：

A  ↔  Robot  ↔  B 它们之间通过 covariance 已经产生相关性。

例如：

```
Robot
├── A
└── B
```

当 observation 告诉你：

> Robot + A 这组关系之前有偏差。

由于 Robot 和 B 也相关，所以 B 的 posterior 也可能变化。

因此：

一个局部 observation 可以产生全局状态更新 这就是 EKF-SLAM 很漂亮、但也很昂贵的地方。

### 19. 一维数值直觉例子

本节的两个更新值用于比较权重，草稿未给定观测噪声与状态相关性。可复算的明确假设和计算放在后文“补充推导”后的修订说明中。

假设机器人认为：

$$
x_r=5m
$$

landmark A：

$$
x_A=8m
$$

所以预测距离：

$$
\hat r=3m
$$

但 sensor 实际测：

$$
r=2.5m
$$

residual：

$$
-0.5m
$$

现在怎么办？

#### 情况 A：Robot 很不可信

假设：

$$
\sigma_r=1m
$$

landmark 非常确定：

$$
\sigma_A=0.1m
$$

那么系统会认为：

> landmark 基本没问题，主要是 robot 估错了。

于是可能更新成：

$$
x_r\approx5.45m
$$

而：

$$
x_A
$$

只改一点点。

#### 情况 B：Robot 很可靠

如果：

$$
\sigma_r=0.05m
$$

但：

$$
\sigma_A=1m
$$

那么系统更可能：

> Robot 基本对，A 估错了。

于是：

$$
x_A\approx7.5m
$$

这就是 Kalman weighting。

## 地标初始化与数据关联

### 20. 新 Landmark 第一次看到怎么办？

这是 Landmark SLAM 一个非常实际的问题。 假设 landmark $$m_3$$ 是第一次出现。

原本状态：

$$
X= [x_r,m_1,m_2]
$$

现在要扩展成：

$$
X'= [x_r,m_1,m_2,m_3]
$$

那 $$m_3$$ 的初始位置怎么得到？ 利用当前 robot pose + measurement。

假设 sensor 测：

$$
z= [r,\phi]
$$

那么：

$$
m_x = x+r\cos(\theta+\phi)
$$

$$
m_y = y+r\sin(\theta+\phi)
$$

于是就能初始化 landmark。

### 21. 但新 landmark uncertainty 不能随便设

因为：

$$
m
$$

是从：

$$
robot\ pose + measurement
$$

推出来的。

所以它的不确定性来源有两个：

Robot uncertainty

和：

Measurement uncertainty

因此新 landmark 绝对不能简单认为：

> “测到了，所以位置确定。”

它实际上继承了 robot uncertainty。

这也意味着：

新 landmark 一出生，就和 robot pose 有 covariance

### 22. 为什么“地图越来越确定”？

假设 Landmark A 第一次看到时：

$$
\sigma_A=0.5m
$$

后来机器人换了几个位置不断观察 A：

```
x1 → A

x2 → A

x3 → A

x4 → A
```

不同位置可提供互补几何约束；共享状态误差使它们不一定统计独立。

于是：

$$
P_A
$$

通常逐渐减小。

直觉上：

> 同一个点，从不同位置看很多次，它在哪里就越来越清楚。

这有点像 triangulation。

### 23. 更重要的是：Landmark 也在帮助 Robot

开始时 landmark 是未知的。

但是经过多次 observation 后：

$$
Landmark\ uncertainty \downarrow
$$

它就逐渐变成了一个稳定 reference。

于是之后机器人再次看到它：

Observation of Landmark

就可以强力修正：

Robot pose

所以整个过程是：

```
Robot initially helps locate Landmark

↓

Landmark becomes more certain

↓

Landmark later helps localize Robot
```

也就是：

Pose  →  Map  →  Pose 这就是 SLAM 的闭环。

### 24. 这也是为什么地图不只是“输出”

这个概念很重要。

很多人会认为 SLAM：

```
传感器
↓
定位
↓
顺便生成地图
```

其实不准确。 Map 不只是一个最终结果。

Map 也是：

>  **下一次 localization 的信息来源。**

所以：

$$
Map
$$

既是：

$$
Output
$$

也是：

$$
State
$$

同时也是未来 estimation 的 reference。

### 25. Data Association 在 EKF-SLAM 里有多重要？

假设机器人看到一个 landmark：

$$
z
$$

它必须先回答：

> 这是已有的 $$m_3$$，还是一个新 landmark？

如果 association 正确：

$$
z\rightarrow m_3
$$

那么 Update 正常。

但如果实际上是：

$$
m_8
$$

却错配成：

$$
m_3
$$

那系统就会说：

> “为什么 m3 出现在这么奇怪的位置？”

然后 EKF 会努力通过修改：

- Robot pose
- m3
- 和它们相关的其他 landmarks

去满足这个错误 measurement。

结果：

一个错误 association 可能污染整个 State

这也是 SLAM 里：

Data Association 一直特别麻烦的原因。

### 26. Mahalanobis Distance

所以 EKF-SLAM 里通常不会单纯用：

$$
\|z-\hat z\|
$$

来判断匹配。

更合理的是：

$$
d^2 = y^TS^{-1}y
$$

其中：

$$
y=z-\hat z
$$

$$
S=HPH^T+R
$$

这就是 Mahalanobis distance。

#### 为什么不用普通欧氏距离？

假设 residual：

$$
y= \begin{bmatrix} 0.5m\\ 2^\circ \end{bmatrix}
$$

它到底算大还是小？

如果 measurement 很精确：

$$
0.5m
$$

可能已经非常离谱。

但如果 sensor 很 noisy：

$$
0.5m
$$

也许完全正常。 Mahalanobis distance 会把 uncertainty 考虑进去。

所以本质是：

$$
\boxed{ Residual / Expected\ uncertainty }
$$

这和我们之前讲 gating 时完全一致。

## 计算成本、线性化与 Filtering

### 27. EKF-SLAM 最大的优势

它最大的优点不是快。

而是：

>  **概率结构非常完整。**

它显式维护：

$$
P
$$

因此它知道：

- Robot uncertainty
- Landmark uncertainty
- Robot-landmark correlation
- Landmark-landmark correlation

整个世界的不确定性结构都存在 covariance 里。 从理论上说清晰。

### 28. 但最大的问题也正是这个 covariance

假设有：

$$
N
$$

个 landmarks。

状态维度大约：

$$
D=3+2N
$$

Covariance：

$$
P\in\mathbb{R}^{D\times D}
$$

也就是说存储复杂度：

$$
O(N^2)
$$

这已经很大。 更麻烦的是 Update 也涉及大矩阵运算。

经典 EKF-SLAM 更新常被近似认为：

$$
O(N^2)
$$

比如：

$$
N=100
$$

还好。

如果：

$$
N=100000
$$

那：

$$
P
$$

就是一个巨大 dense matrix。 这完全无法扩展。

### 29. 为什么 covariance 会是 dense 的？

这是最关键的问题之一。

你可能会想：

> landmark A 和 landmark Z 离得这么远，为什么它们还相关？

因为它们都曾通过 robot pose 建立联系。

例如：

```
Robot at t1 sees A

Robot moves

Robot at t2 sees B

Robot moves

Robot at t3 sees C
```

虽然 A、B、C 没直接互相观测， 但它们都依赖于同一条 robot trajectory。 于是间接建立相关性。

经过时间传播以后：

$$
P
$$

通常会越来越 dense。

### 30. 这就埋下了 Graph SLAM 的伏笔

EKF-SLAM 思路是：

>  **直接维护整个联合 Gaussian distribution。**

也就是：

$$
\mathcal N(\mu,P)
$$

尤其显式维护：

$$
P
$$

而现代 Graph SLAM 更倾向于：

> 我不直接维护所有变量之间的 covariance。

而是保存：

Sparse constraints

比如：

```
x1 ↔ x2
x2 ↔ x3
x1 ↔ Landmark A
x3 ↔ Landmark B
```

然后需要的时候统一 optimize。

这就会自然进入：

- Factor Graph
- Bundle Adjustment
- Pose Graph

### 31. 一个很重要的对比

EKF-SLAM：

```
State:
[robot + all landmarks]

Covariance:
everything correlated with everything

Each measurement:
update the whole probabilistic state
```

Graph-based SLAM：

```
Variables:
poses + landmarks

Measurements:
stored as sparse constraints

Optimization:
solve all constraints together
```

两者其实是在解决同一个问题。 只是计算表示不同。

### 32. EKF-SLAM 是 Filtering

这里再和后面一个大概念连起来。

EKF 是：

Filtering 什么意思？

它通常维护：

$$
p(x_t,m|z_{1:t})
$$

也就是：

> 根据截至当前时刻所有 measurement，估计当前 state。

旧的信息被逐渐压缩进：

$$
\mu_t,P_t
$$

里面。

而 Graph SLAM 更像：

Smoothing

它保留历史状态：

$$
x_0,x_1,\dots,x_t
$$

然后一起优化。 这是一个非常大的思想差别。 后面会专门再讲。

### 33. Filtering vs Smoothing 的直觉

假设：

```
t0 → t1 → t2 → t3 → t4
```

Filtering 更像：

```
历史信息
   ↓
压缩
   ↓
当前 belief
```

也就是：

$$
x_t,P_t
$$

Smoothing 则是：

```
x0 - x1 - x2 - x3 - x4
```

都留着。

然后未来信息到来后：

$$
z_4
$$

可以反过来修改：

$$
x_1,x_2,x_3
$$

这对 SLAM 特别有吸引力。

### 34. EKF 的另一个问题：Linearization

EKF 使用：

$$
f(x) \approx f(\hat x) + F(x-\hat x)
$$

也就是说只保留一阶。

如果 estimate 已经比较接近 truth：

$$
\hat x\approx x
$$

通常还不错。

但如果 initialization 很差，或者运动很非线性：

$$
\hat x
$$

离真实值很远， 线性化可能就非常差。

### 35. 一个简单例子

例如 bearing：

$$
\phi = \operatorname{atan2}(y,x)
$$

这是一个明显非线性函数。

假设你的 estimate 在真实值附近：

```
true ●
estimate ×
```

很近。

做 tangent approximation：

linearization 还比较合理。

但如果：

```
true ●

                    estimate ×
```

离得非常远。 那 tangent 根本不能很好地描述真实曲线。

所以：

EKF 的好坏强烈依赖 linearization point

### 36. EKF-SLAM 的“顺序依赖”

还有一个有趣的问题。

当 EKF 采用逐个 measurement update 并重新线性化时：

$$
z_1 \rightarrow update
$$

然后：

$$
z_2 \rightarrow update
$$

由于每次都重新线性化， 不同 measurement 顺序有时会产生略有不同结果。 理论上的真实 Bayesian inference 不应该依赖 observation 顺序。 但 EKF 是近似。

所以：

Linearization introduces approximation

### 37. EKF-SLAM 为什么历史上非常重要？

因为它第一次很系统地告诉机器人领域：

> Mapping 和 Localization 不是两个独立问题。

landmark 与 robot 的 uncertainty：

必须联合考虑 这就是 SLAM 早期理论真正奠基的地方。 甚至你现在看很多现代方法，虽然已经不用 EKF-SLAM 这种完整形式，

核心思想还是一样：

> 一个 measurement 在连接多个 state。

### 38. 用 Factor Graph 视角提前看一下

刚才状态：

$$
x_0,x_1,x_2
$$

landmarks：

$$
m_1,m_2
$$

观测可能是：

```
x0 → m1
x1 → m1
x1 → m2
x2 → m2
```

从 EKF 角度：

> 它们都在一个巨大 covariance 里。

从 Factor Graph 角度：

```
m1       m2
| \     / |
|  \   /  |
x0--x1---x2
```

你会发现：

> 原始 measurement relation 本身其实很 sparse。

真正 dense 的，是 EKF 中最后维护出来的 covariance。 这个区别极其关键。

### 39. Information Matrix

如果 covariance 是：

$$
P
$$

定义 information matrix：

$$
\Lambda=P^{-1}
$$

很有意思的是，在很多 SLAM 问题中：

$$
P
$$

可能很 dense，

但是：

$$
\Lambda
$$

反而可以非常 sparse。 为什么？

因为 information matrix 更直接对应：

> 哪些 state 之间存在直接 constraint。

例如：

$$
x_1
$$

只和：

$$
x_0,x_2,m_1
$$

直接有 measurement relation。 所以信息结构天然稀疏。

这种结构推动了：

Sparse Graph Optimization 成为主流。

### 40. 你现在应该建立的一个大图景

经典 EKF-SLAM：

$$
Sensor
$$

↓

Prediction

↓

robot uncertainty 增大

↓

看到 landmark

↓

Residual

↓

Kalman Gain

↓

同时更新：

$$
Robot + Map
$$

↓

covariance 建立全局 correlation 这就是它的核心闭环。

### 41. 用一句工程语言总结

如果让我不用公式解释 EKF-SLAM：

> 机器人每走一步，都因为运动噪声变得更不确定；每看到一个曾经见过的 landmark，就利用“我和它之间应该满足什么几何关系”来同时纠正自己的位置和地图。所有状态之间的可信度以及相互关联，都被存在一个巨大的 covariance matrix 里。

这句话基本就是整章。

### 42. 本章你真正应该掌握的六点

第一：

$$
\boxed{ State = Robot + Landmarks }
$$

第二：

Prediction 主要传播 Robot Pose

第三：

Observation 可以同时修正 Robot 和 Map

第四：

Cross Covariance 是 EKF-SLAM 的核心。

第五：

$$
\boxed{ EKF-SLAM 最大的问题是 O(N^2) 的 dense covariance }
$$

第六：

现代 SLAM 转向 graph optimization，很大程度上是为了利用：

Measurement structure is sparse

## 补充推导：新地标的联合协方差

设新地标 m = g(x_r,z)，g 为逆观测模型，令 α = θ + φ，则：

$$
m=\begin{bmatrix}x+r\cos\alpha\\y+r\sin\alpha\end{bmatrix},\quad
G_r=\begin{bmatrix}1&0&-r\sin\alpha\\0&1&r\cos\alpha\end{bmatrix},\quad
G_z=\begin{bmatrix}\cos\alpha&-r\sin\alpha\\\sin\alpha&r\cos\alpha\end{bmatrix}.
$$

令 G_X = [G_r, 0]，维度 2×(3+2N)，测量协方差 R_z 为 2×2，假设新测量噪声与原状态误差独立。一阶展开 δm ≈ G_XδX + G_zδz，得到：

$$
P_{\mathrm{aug}}\approx\begin{bmatrix}
P&PG_X^T\\G_XP&G_XPG_X^T+G_zR_zG_z^T
\end{bmatrix}.
$$

### 推导得到什么

初始化不仅产生新地标自身的协方差，也产生它与机器人及已有地图的交叉协方差；漏掉交叉块会损失相关信息。

### 在 SLAM 中怎么用

状态增广应与逆观测模型一起实现。用于初始化的同一测量不能再被当作新的独立观测重复更新。

> 修订说明：草稿第 19 节只给定直觉更新值，未给观测噪声和交叉协方差，不能据此复算。若明确采用一维模型 z = x_A − x_r、独立先验、测量标准差 0.3 m，情况 A 有 S = 1 + 0.01 + 0.09 = 1.10，K = [−1,0.01]ᵀ/1.10，创新 −0.5 m，得到 x_r⁺ ≈ 5.4545 m、x_A⁺ ≈ 7.9955 m。情况 B 使用同样测量噪声，S = 0.0025 + 1 + 0.09 = 1.0925，得到 x_r⁺ ≈ 5.0011 m、x_A⁺ ≈ 7.5423 m。这是明确假设后的示例，并非对原草稿缺失参数的还原。

> 修订说明：地图不确定性下降是相对于所选坐标基准、并在有效独立信息增加时的趋势；相对观测无法消除 global gauge。EKF-SLAM 历史边缘化后的信息矩阵也可变稠密，不能由完整轨迹图的稀疏性推出当前 Filtering 状态的信息矩阵必然稀疏。观测顺序影响主要来自逐次重新线性化；EKF 也可以批量更新。

## 思考题

### Q1：为什么新 landmark 一初始化，就不能和 robot pose 看成独立变量？

**参考答案**

因为 landmark 的位置就是通过：

$$
Robot\ Pose + Measurement
$$

推出来的。

比如：

$$
m_x=x+r\cos(\theta+\phi)
$$

所以 robot 的误差会直接进入 landmark。 因此二者天然相关。


### Q2：为什么机器人只看到 landmark A，landmark B 也可能被更新？

**参考答案**

因为：

$$
A
$$

和：

$$
Robot
$$

相关，

而 Robot 又和：

$$
B
$$

相关。

因此：

A ↔  Robot ↔  B Measurement information 可以通过 covariance 传播。


### Q3：如果完全忽略所有 cross-covariance，会怎样？

**参考答案**

相当于假设：

$$
Robot,\ Landmark_1,\ Landmark_2
$$

全部互相独立。 这实际上是错误的。

后果通常是：

> 系统会高估自己拥有多少“独立信息”。

从而产生：

overconfidence 也就是 covariance 过小，但真实误差并没那么小。 这是一种典型 estimator inconsistency。


### Q4：为什么 EKF-SLAM 随 landmark 数量增加会越来越难？

**参考答案**

因为 State 维度：

$$
O(N)
$$

但 covariance 大小：

$$
O(N^2)
$$

而且 covariance 通常逐渐变 dense。 所以计算和存储都难以扩展。


### Q5：EKF-SLAM 和 Graph SLAM 最核心的表示差别是什么？

**参考答案**

EKF-SLAM 直接维护：

Joint Gaussian 尤其是 dense covariance。

Graph SLAM 保存：

$$
\boxed{ Variables + Sparse\ Constraints }
$$

然后通过 optimization 求解。


### Q6：为什么 EKF-SLAM 即使现在不常作为大型视觉 SLAM 主流方案，还是值得学？

<details>

<summary>参考答案</summary>

因为它能最清楚地展示：

Pose uncertainty  →  Map uncertainty

以及：

Map observation  →  Pose correction

也就是 SLAM 中：

State Correlation 这个最核心的概念。 如果这一章理解了，后面看 Factor Graph 时你会明显轻松很多。

</details>

## 相关章节与来源

- 上一章：[SLAM 问题定义](slam-formulation.md)
- 下一篇：[SLAM 可观测性与 Gauge Freedom](gauge-freedom.md)
- 来源：本次新增 Part IV Chapter 38 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
