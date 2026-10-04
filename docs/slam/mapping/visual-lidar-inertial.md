---
title: 视觉／激光惯性状态估计
description: IMU 怎样与 Camera、LiDAR 联合约束位姿、速度与 Bias？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 47
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# 视觉／激光惯性状态估计

## 本章目标

IMU 怎样与 Camera、LiDAR 联合约束位姿、速度与 Bias？

## 前置知识

[传感器观测模型](../spatial/sensor-models.md)、[Gauge Freedom](gauge-freedom.md)、[Factor Graph](factor-graphs.md)。

## 定义与假设

R_i 将 IMU 系映射到世界系，p_i、v_i、g 在世界系表达；gyro、比力和 bias 在 IMU 系表达。状态的局部维度通常为 15（位姿 6、速度 3、bias 6），额外估计重力或标定参数时会增加。

## 核心问题


先给你这一章最核心的一句话：

$$
\boxed{ Camera/LiDAR 负责纠正长期几何漂移，IMU 负责提供高频短期运动约束 }
$$

但这句话只是第一层。 真正理解 VIO / LIO，要先看两类传感器各自“擅长什么、缺什么”。

## 传感器互补与扩展状态

### 1. Camera 有什么优点和缺点？

Camera 很擅长：

Geometry

因为通过 feature / optical flow / reprojection，可以看到：

> 当前观测和过去地图之间是否一致。

它可以很好地约束：

$$
Pose
$$

特别是在纹理丰富、视差充足时。 但它的问题也很明显。

Camera 通常是：

$$
20\sim30\ Hz
$$

甚至更低。

而且遇到：

- Motion Blur
- 低光
- 低纹理
- 快速旋转
- 动态场景

Tracking 很容易变差。

所以 Camera 是：

几何信息强，但瞬时运动感知并不总稳定

### 2. LiDAR 呢？

LiDAR 直接测量 3D 几何。

通过：

Scan Matching

可以估计：

$$
T_{t,t+1}
$$

优点是：

- 不依赖光照
- 有直接 metric geometry
- 深度精确
- 对很多纹理缺失环境仍然有效

但它也有退化。

例如长走廊：

```
|                    |
|                    |
|                    |
```

沿走廊方向运动时， 几何变化可能很弱。

于是某些方向：

weakly observable 所以 LiDAR 也不是万能的。

### 3. IMU 和它们完全不一样

IMU 通常测两种东西：

Gyroscope：

$$
\omega_m
$$

Accelerometer：

$$
a_m
$$

而且频率很高：

$$
100\sim1000\ Hz
$$

甚至更高。 所以 IMU 对快速运动非常敏感。

相机发生：

快速旋转 时， 图像可能 blur。

但 gyro 仍然可以清楚测到：

Angular Velocity

因此 IMU 特别适合：

Short-term motion propagation

### 4. 但 IMU 有一个致命问题

IMU 会：

Drift 而且是非常严重的 drift。 为什么？

因为 acceleration 要积分一次得到 velocity：

$$
v(t) = v_0+\int a(t)dt
$$

再积分一次得到 position：

$$
p(t) = p_0+ \int v(t)dt
$$

如果 acceleration 有一个小 bias：

$$
b_a
$$

那么 position error 会快速积累。

### 5. 一个非常直观的例子

假设 accelerometer 有：

$$
0.01m/s^2
$$

的小 bias。 听起来非常小。

如果一直积分：

$$
\Delta p = \frac12bt^2
$$

10 秒：

$$
\Delta p = \frac12\times0.01\times100 = 0.5m
$$

60 秒：

$$
\Delta p = \frac12\times0.01\times3600 = 18m
$$

只是一个很小的 bias， 最终 position 已经错很多。

所以：

IMU 很强，但绝不能长期单独相信

### 6. Gyro Bias 也一样危险

Gyroscope：

$$
\omega_m = \omega_{true}+b_g+n_g
$$

如果：

$$
b_g
$$

有一点误差，

rotation 不断积分：

$$
R_{t+1} = R_t\exp((\omega\Delta t)^\wedge)
$$

orientation 会慢慢漂。 而 orientation 一错， gravity compensation 也会错。

然后：

acceleration 又错。

最后：

velocity

和：

position 都会跟着错。 所以 IMU error 会层层传播。

### 7. 为什么 Camera / LiDAR + IMU 很互补？

Camera / LiDAR：

> 长期可以提供几何 reference。

IMU：

> 短期可以提供连续、高频 motion information。

所以：

IMU  →  Prediction

Camera / LiDAR：

→  Correction

这其实就是我们最早讲的：

$$
\boxed{ Prediction + Observation Correction }
$$

### 8. VIO 的 State 不再只是 Pose

纯视觉 SLAM 里：

$$
x_i=T_i
$$

可能就够了。

但 VIO 中每个时间状态通常至少包含：

$$
x_i= \{ R_i, p_i, v_i, b_{g,i}, b_{a,i} \}
$$

也就是：

$$
\boxed{ Pose + Velocity + Gyro\ Bias + Accel\ Bias }
$$

为什么多了这些东西？ 因为 IMU measurement model 依赖它们。

### 9. 为什么 Velocity 必须进入 State？

Camera 可以直接约束：

$$
Pose
$$

但 IMU dynamics 是：

$$
\dot p=v
$$

$$
\dot v= R(a_m-b_a-n_a)+g
$$

所以：

velocity 是系统动力学的一部分。

如果不显式维护：

$$
v
$$

就很难正确连接 IMU measurements。

### 10. Gravity 也会出现

IMU accelerometer 并不是简单测：

robot linear acceleration 它测的是 specific force。

常见连续模型：

$$
a_m = R^T(\dot v-g) + b_a+n_a
$$

反过来：

$$
\dot v = R(a_m-b_a-n_a)+g
$$

所以：

$$
g
$$

天然进入系统。

这也是为什么：

> VIO 初始化要估 Gravity Direction。

### 11. IMU Bias 为什么必须估？

真实 IMU：

$$
\omega_m = \omega+b_g+n_g
$$

$$
a_m = a+b_a+n_a
$$

其中：

$$
b_g,b_a
$$

不是一次 calibration 之后永远固定。

它们会随：

- 温度
- 时间
- 设备状态

缓慢变化。

所以常建模成 random walk：

$$
b_{g,t+1} = b_{g,t}+n_{bg}
$$

$$
b_{a,t+1} = b_{a,t}+n_{ba}
$$

也就是说：

Bias 本身也是动态 State

### 12. VIO 的 State 一下子变复杂了

一个 Keyframe State 可以写：

$$
X_i= [ R_i, p_i, v_i, b_{g,i}, b_{a,i} ]
$$

如果用最小局部参数看：

$$
3+3+3+3+3=15
$$

维。

所以一个时刻就是：

$$
15D
$$

state。

如果滑窗 10 帧：

$$
150
$$

维， 还没算 landmarks、extrinsics、time offset。 这也是为什么 VIO 比纯视觉 Pose Optimization 明显复杂。

## IMU 预积分与残差

### 13. IMU measurement frequency 很高怎么办？

假设 Camera：

$$
20Hz
$$

意味着两帧间隔：

$$
50ms
$$

而 IMU：

$$
200Hz
$$

那么两张图之间有大约：

$$
10
$$

组 IMU measurements。

如果 IMU：

$$
1000Hz
$$

那可能有：

$$
50
$$

组。

如果 Factor Graph 里每条 IMU measurement 都创建一个 State：

```
Camera state
x
|
imu
|
x
|
imu
|
x
|
imu
...
```

State 数量会暴涨。 不划算。

### 14. 于是出现 IMU Preintegration

这是 VIO 最重要的概念之一：

IMU Preintegration

核心思想：

> 把两帧 Camera / Keyframe 之间大量 IMU measurements 压缩成一个 IMU Factor。

比如：

```
Keyframe i

imu1
imu2
imu3
...
imu10

Keyframe j
```

最终变成：

```
Xi ===== IMU Factor ===== Xj
```

这就是 Preintegration 的目的。

### 15. 为什么不能简单把 acceleration 平均一下？

因为 IMU 的积分涉及：

Rotation 而 rotation 一直在变化。

例如：

$$
a^w = R(t)a^b
$$

每个时刻：

$$
R(t)
$$

不一样。

所以不是：

average(a) 然后乘时间就结束。

必须正确处理：

$$
SO(3)
$$

上的积分。

### 16. Preintegration 最终得到什么？

在两个 Keyframes：

$$
i
$$

和：

$$
j
$$

之间，

预积分大致产生：

$$
\Delta R_{ij}
$$

$$
\Delta v_{ij}
$$

$$
\Delta p_{ij}
$$

代表在局部参考 frame 下 IMU 测到的：

- rotation change
- velocity change
- position change

然后形成一个 factor：

$$
r_{imu}(X_i,X_j)
$$

### 17. Rotation Preintegration 的直觉

连续 gyro：

$$
\omega_k
$$

逐步积分：

$$
\Delta R = \prod_k \exp \left( ((\omega_k-b_g)\Delta t_k)^\wedge \right)
$$

意思就是：

> 两个 Keyframes 之间，IMU 认为总共旋转了这么多。

然后和 State prediction：

$$
R_i^{-1}R_j
$$

比较。 形成 rotation residual。

### 18. Velocity residual

IMU 预积分会预测：

$$
v_j
$$

应该满足：

$$
v_j \approx v_i + g\Delta t + R_i\Delta v_{ij}
$$

所以 residual 类似：

$$
r_v = R_i^T (v_j-v_i-g\Delta t) - \Delta v_{ij}
$$

直觉上：

> State 中的速度变化，应该和 IMU 积分结果一致。

### 19. Position residual

类似：

$$
p_j \approx p_i + v_i\Delta t + \frac12g\Delta t^2 + R_i\Delta p_{ij}
$$

于是：

$$
r_p = R_i^T \left( p_j-p_i-v_i\Delta t-\frac12g\Delta t^2 \right) - \Delta p_{ij}
$$

所以一个 IMU Factor 同时约束：

R,p,v,bias 多个变量。

### 20. 这和 Visual Factor 非常不同

Visual Factor：

$$
r_{cam} = z-\pi(TP)
$$

主要连接：

$$
Pose + Landmark
$$

IMU Factor：

$$
r_{imu}
$$

连接：

$$
Pose_i
$$

$$
Velocity_i
$$

$$
Bias_i
$$

和下一时刻：

$$
Pose_j
$$

$$
Velocity_j
$$

$$
Bias_j
$$

所以它是一个更高阶 factor。

### 21. VIO Factor Graph 长什么样？

可以想象：

```
X0 ===== X1 ===== X2 ===== X3
|        |        |        |
visual   visual   visual   visual
|        |        |        |
P1       P2       P3       P4
```

其中：

$$
=====
$$

是 IMU Factors。

每个：

$$
X_i
$$

包含：

$$
Pose + Velocity + Bias
$$

### 22. Bias 改了，Preintegration 怎么办？

因为：

$$
\Delta R,\Delta v,\Delta p
$$

都是基于某个 bias estimate 积出来的。

如果 optimizer 后来把：

$$
b_g,b_a
$$

改了， 难道要重新把几百个 IMU measurements 全积分一遍？ 如果每次迭代都重做，会很贵。

### 23. Bias Jacobian

所以 Preintegration 通常还保存：

$$
\frac{\partial \Delta R}{\partial b_g}
$$

$$
\frac{\partial \Delta v}{\partial b_g}
$$

$$
\frac{\partial \Delta v}{\partial b_a}
$$

等等。 当 bias 只是小幅变化时，

可以一阶修正：

$$
\Delta v(b+\delta b) \approx \Delta v(b) + J_b\delta b
$$

这样不用完全重新积分。

这就是：

Preintegration with bias correction

### 24. 这是不是又回到 Linearization？

完全是。

我们一直都在做：

$$
f(x+\delta x) \approx f(x)+J\delta x
$$

Bias correction 只是这个思想的又一个实际应用。

## 初始化、尺度与运动激励

### 25. Camera 和 IMU 怎么互相帮助？

假设机器人快速转头。

Camera：

- Motion Blur
- Feature tracking 变差

但 Gyro：

$$
\omega
$$

非常稳定。

于是 IMU 给出很好的 rotation prediction：

$$
R_{pred}
$$

Camera 可以在这个 prediction 附近找 feature。

所以：

IMU helps visual tracking

### 26. 反过来 Camera 怎么帮助 IMU？

IMU 单独积分会 drift。

Camera 看到稳定 scene 后：

$$
Pose
$$

被几何约束回来。

于是：

- orientation error 被修
- velocity 被间接修
- bias 也被重新估计

所以：

Vision corrects IMU drift

### 27. 最重要的是 Bias 可以通过视觉“看出来”

例如 Gyro bias 稍微错了。

那么 IMU 预测：

$$
R_{pred}
$$

长期就会和视觉估计：

$$
R_{visual}
$$

出现系统偏差。

Optimizer 会发现：

> 如果调整 $$b_g$$，IMU residual 和 visual residual 可以一起变小。

于是：

$$
b_g
$$

被估出来。 这就是多传感器融合的真正力量。

### 28. 不是简单做加权平均

有时初学者会把 Fusion 理解成：

$$
Pose = 0.5Pose_{camera} + 0.5Pose_{imu}
$$

不是这样。

更准确是：

> 不同 sensors 对共同 State 的不同部分施加不同 Measurement Constraints。

然后联合估计：

$$
\arg\min_X E_{visual} + E_{imu}
$$

所以：

$$
\boxed{ Fusion = Joint State Estimation }
$$

不是结果平均。

### 29. VIO 为什么要初始化？

因为刚启动时，有一堆东西不知道：

Velocity Gravity Direction

$$
Bias
$$

Monocular 情况下甚至：

$$
Scale
$$

也不知道。 如果这些初值太差， 后面的 nonlinear optimization 可能直接崩掉。 所以 VIO initialization 是一个大问题。

### 30. Monocular VIO 最有意思的是 Scale

纯 monocular：

$$
scale
$$

不可观。

但 IMU 有：

$$
m/s^2
$$

这个物理量。 因此视觉轨迹的 arbitrary scale 可以通过 IMU dynamics 对齐到 metric scale。

假设视觉告诉你：

$$
\Delta p_{visual}=2.0\ units
$$

IMU 根据 acceleration 认为实际应该：

$$
0.8m
$$

那么系统可以估：

$$
s=0.4m/unit
$$

所以：

IMU can make monocular scale observable

### 31. 但为什么需要“运动激励”？

假设机器人完全静止。

IMU 读到的主要是：

gravity 你很难通过这段数据分清很多变量。

再比如机器人以恒定速度匀速直线：

$$
a\approx0
$$

scale 信息也可能很弱。

所以要估：

- scale
- bias
- gravity

通常需要一定的：

Excitation 也就是足够丰富的 motion。

### 32. 一个简单例子：Accel Bias 和 Gravity

Accelerometer measurement：

$$
a_m = R^T(\dot v-g)+b_a
$$

如果机器人长时间姿态和运动变化非常少，

你可能很难分辨：

> 这是 gravity direction 有一点错？

还是：

> accelerometer bias 有一点错？

因为它们的效果可能相似。

这就是：

State Coupling 和 weak observability。

### 33. 为什么多方向旋转有帮助？

当机器人姿态变化时：

$$
R^Tg
$$

在 IMU body frame 中也变化。

而：

$$
b_a
$$

相对 sensor frame 更像固定偏移。 通过不同 orientation 下反复观察，

就能逐渐把：

gravity

和：

$$
bias
$$

区分开。 所以运动本身可以创造 information。

### 34. 这就是 Active Observability 的味道

传感器没变。

但机器人怎么运动，会决定：

Measurement 对 state 有多少信息。

所以：

Motion is part of sensing

### 35. VIO 的不可观方向是什么？

对于典型 monocular VIO，

在充分激励后：

- metric scale 可以变得 observable
- roll / pitch 可由 gravity 约束

但通常仍然存在：

global position 3 DoF，

以及：

global yaw 1 DoF。

总共：

$$
\boxed{ 4\ unobservable\ directions }
$$

### 36. 为什么 global yaw 仍不可观？

Gravity 给了：

vertical 方向。 所以 roll / pitch 有参考。

但绕 gravity axis：

```
   ↑ g

   ↻ yaw
```

旋转， gravity 不会变化。 Camera 又主要给相对 geometry。

所以没有：

- magnetometer
- global map
- GPS heading

时， global yaw 没有绝对 reference。

### 37. 为什么 global position 不可观？

因为 Camera 和 IMU 都主要提供：

relative motion

把整个 trajectory：

$$
p_i
$$

全部加同一个：

$$
t
$$

IMU 和 visual relative measurements 都不会变。 所以 global translation 仍是 Gauge Freedom。

### 38. Stereo VIO 呢？

Stereo 已经有 metric scale。 所以初始化比 monocular VIO 容易一些。 不需要靠 IMU 去恢复视觉 scale。

但仍然需要估：

- velocity
- gravity
- biases

所以问题仍然不是简单的 Visual SLAM + IMU。

## 滑动窗口、边缘化与 Landmark 表示

### 39. 为什么实际 VIO 常用 Sliding Window？

假设 Camera：

$$
20Hz
$$

运行十分钟：

$$
12000
$$

frames。

每个 State：

$$
15D
$$

如果全部优化：

$$
180000
$$

维， 再加 landmarks， 显然太重。

所以保留最近：

$$
N
$$

个 Keyframes。

例如：

$$
N=10
$$

形成：

Sliding Window

### 40. Sliding Window 内优化什么？

比如窗口：

$$
X_{k-9},...,X_k
$$

同时包含：

- IMU factors
- visual factors
- landmarks / inverse depth
- prior factor

每来新帧：

```
old:

X0 X1 X2 ... X9

new:

   X1 X2 ... X9 X10
```

最旧：

$$
X_0
$$

离开窗口。

### 41. 最旧 State 能直接删吗？

不能。 因为它承载了大量历史信息。

比如：

$$
X_0
$$

通过 IMU factor 约束：

$$
X_1
$$

又通过 visual factors 关联 landmarks。

如果直接删除：

> 这些历史 measurements 的信息也全部丢了。

所以必须：

Marginalize

### 42. Marginalization 再解释一次

原来：

```
Historical factors
      |
      X0
      |
      X1
```

Marginalize：

$$
X_0
$$

以后：

```
New Prior
    |
    X1
```

把历史信息压缩成：

Prior Factor 继续作用于窗口。

所以：

$$
\boxed{ Sliding Window = Optimization + Information Compression }
$$

### 43. 为什么 Marginalization 是 VIO 难点之一？

因为系统是：

Nonlinear Marginalization 时，

你是在某个：

linearization point 附近把历史信息压成 prior。 之后 State 又继续变化。 但过去的原始 measurements 已经删了， 不能随便重新 linearize。

所以会产生：

Linearization inconsistency 这是 fixed-lag smoother 很核心的技术问题。

### 44. First Estimate Jacobian

你以后看 VIO 文献可能会看到：

$$
FEJ
$$

First Estimate Jacobian。

核心动机之一就是：

> 不要因为后来反复改变 linearization point，错误地改变本该不可观的方向。

也就是保持：

Unobservable Subspace 的一致性。 这又回到了 Chapter 39。

### 45. 你应该发现课程已经闭环了

Chapter 39：

Observability

Chapter 42：

Linearization

Chapter 44：

Marginalization

现在 VIO 中三者真正碰到一起：

> Linearization + Marginalization 如果处理不好，会制造假的 information，从而破坏真实 observability。

这就是很多 VIO 算法理论难点所在。

### 46. Visual Factor 怎么参数化 Landmark？

VIO 滑窗里不一定把 landmark 存成：

$$
P_w=[X,Y,Z]
$$

常见做法是：

Inverse Depth

例如一个 feature 首次在某 Keyframe 看到：

$$
(u,v)
$$

只优化：

$$
\rho=\frac1Z
$$

结合 anchor camera pose， 就能恢复 3D point。

### 47. 为什么 Inverse Depth 很常用？

对于远点：

$$
Z\rightarrow\infty
$$

普通 depth 数值很大。

但：

$$
\rho=\frac1Z\rightarrow0
$$

更稳定。 而且对 monocular triangulation 来说， inverse depth 对远距离 point 的参数化通常更合适。

所以 VIO 常看到：

$$
Feature\ State = Inverse\ Depth
$$

### 48. MSCKF 又是什么思路？

有些 VIO 并不把所有 landmarks 长期放进 State。

例如 MSCKF 思路之一：

> 一个 feature 被多帧观察后，利用它形成 pose constraints，然后把 feature 本身消掉。

是不是很熟？

这就是：

Eliminate Landmark, preserve pose information 和 BA 的 Schur Complement 思想非常接近。

### 49. Filter-based 和 Optimization-based VIO

VIO 大体历史上有两条路线。

一类是：

EKF-based 如 MSCKF 家族思想。

另一类是：

$$
\boxed{ Optimization / Smoothing-based }
$$

例如滑窗 nonlinear optimization。

### 50. 两者本质区别还记得吗？

Filtering：

历史信息不断压进当前 belief

Smoothing：

保留一段历史 states，一起优化

Optimization-based VIO 常用：

Sliding Window

所以是：

Fixed-Lag Smoothing

## LIO、去畸变与融合方式

### 51. 那 LIO 呢？

LiDAR-Inertial Odometry：

$$
\boxed{ LiDAR + IMU }
$$

思想其实和 VIO 很像。

IMU：

high-frequency propagation

LiDAR：

geometric correction

只是 Visual Factor 被换成：

LiDAR Geometric Factor

### 52. LiDAR measurement residual 长什么样？

一种经典形式是：

Point-to-Plane

假设当前 LiDAR point：

$$
p
$$

通过 Pose 变换到 Map：

$$
Tp
$$

地图里对应平面：

$$
n^Tx+d=0
$$

Residual：

$$
r = n^T(Tp)+d
$$

也就是：

> 当前 point 到地图平面的距离。

于是 optimizer 同样最小化：

$$
\sum r^2
$$

### 53. 所以 VIO 和 LIO 的后端其实非常统一

VIO：

$$
E= E_{IMU} + E_{visual}
$$

LIO：

$$
E= E_{IMU} + E_{lidar}
$$

如果再加 GPS：

$$
+E_{GPS}
$$

再加 wheel：

$$
+E_{wheel}
$$

所以：

Factor Graph 真的成了统一语言

### 54. LiDAR + IMU 为什么也很互补？

LiDAR 一帧 scan 并不是瞬间完成。

比如机械旋转 LiDAR：

> 一帧点云其实是在几十毫秒内逐点扫出来的。

机器人在这期间还在运动。

于是同一帧点云会发生：

Motion Distortion

### 55. Deskew 是什么？

IMU 可以估计 scan 内部短时间运动。 于是把不同 timestamp 的 LiDAR points 校正到同一个参考时刻。

这个过程叫：

Deskew 没有 IMU 时，

快速运动下点云可能：

```
一面直墙
```

变成：

```
弯的 / 拉伸的墙
```

IMU 对 LIO 最大的直接价值之一就是：

> 提供 scan 内高频运动补偿。

### 56. Camera 也有类似问题吗？

有。 Rolling Shutter Camera 中， 一张图不同 row 的曝光时间不同。

机器人快速运动时：

> 一张 image 也不是一个单一时刻。

所以严格模型里也会出现：

motion distortion 只不过形式和 LiDAR 不一样。 IMU 同样可以帮助建模。

### 57. LIO 中的 Degeneracy

比如 LiDAR 在一条长直隧道。 Point-to-plane constraints 很多。

你可能觉得：

> 几万个点，信息肯定很强。

但这些平面法向可能高度相似。

例如只有：

left wall, right wall

沿 tunnel direction：

$$
x
$$

可能非常弱约束。

所以：

Point count  ≠  Observability 又回来了。

### 58. IMU 能完全解决 LiDAR Degeneracy 吗？

不能完全。 IMU 对短期 motion 有帮助，

尤其：

- rotation
- acceleration

但如果长时间某方向没有外部几何约束， IMU bias 仍会积累。 所以系统可能仍然在某些方向 drift。

融合只是：

互补弱点 不是“一个传感器把另一个所有问题消灭”。

### 59. VIO 也一样

低纹理场景：

Visual constraint weak IMU 能让系统撑一段时间。

但如果长时间完全没有视觉信息：

IMU drift 最终还是会积累。

所以“Fusion”并不等于：

No failure 而是让系统 failure envelope 更大。

### 60. Tightly Coupled 和 Loosely Coupled

这是多传感器融合里非常重要的两个词。

#### Loosely Coupled

比如视觉系统先输出：

$$
Pose_{visual}
$$

IMU 系统输出：

$$
Pose_{imu}
$$

然后在更高层融合。

也就是：

```
Vision Frontend → Pose
                     \
                      Fusion
                     /
IMU Estimator → Pose
```

### 61. Tightly Coupled

直接把原始 / 低层 measurement factors 放进同一个 estimator：

Visual Reprojection IMU Preintegration

共同优化：

Pose,Velocity,Bias,Landmarks

即：

```
pixels ──┐
         ├── Joint State Estimator
IMU ─────┘
```

这叫：

Tightly Coupled

### 62. 为什么 Tight Coupling 通常信息利用更充分？

因为没有先把视觉信息压缩成单一 Pose。

例如：

$$
100
$$

个 feature observations， 每个有不同 geometry 和 uncertainty。

Loose coupling 可能先压成：

$$
Pose_{visual}
$$

再融合， 会损失一些 measurement-level information。 Tight coupling 直接利用原始 residual。 所以理论上更充分。

### 63. 但 Tight Coupling 也更复杂

因为：

- State 更多
- residual 更多
- Jacobian 更复杂
- timing 更敏感
- calibration 更重要
- debugging 更难

所以：

Higher information efficiency  ↔  Higher system complexity

## 同步、外参、噪声与多频率系统

### 64. Time Synchronization 为什么突然很重要？

Camera frame timestamp：

$$
t_c
$$

IMU sample：

$$
t_i
$$

如果两者存在：

$$
10ms
$$

的时间偏移， 快速运动时就会造成明显几何误差。

系统可能把这种误差错认为：

- Pose error
- Bias error
- Extrinsic error

所以：

Temporal Calibration 非常重要。

### 65. Extrinsic Calibration 也一样

相机坐标系和 IMU 坐标系：

$$
T_{CI}
$$

必须知道。

LiDAR 和 IMU：

$$
T_{LI}
$$

也一样。

如果 extrinsic 有误：

> IMU prediction 和 visual/LiDAR measurement 永远对不齐。

所以很多系统会：

- 离线 calibration
- 或在线优化 extrinsic

### 66. Online Extrinsic Calibration 有代价

把：

$$
T_{CI}
$$

作为 State：

$$
X= \{poses,velocity,bias,T_{CI}\}
$$

那么所有 visual + IMU factors 都会和它耦合。

优点：

> 可以在线校正。

问题：

> 需要充分运动激励，否则 extrinsic 可能 weakly observable。

所以还是那句：

能加进 State  ≠  一定能可靠估出来

### 67. IMU Noise 有两种东西要分清

一个是 measurement white noise：

$$
n_g,n_a
$$

表现为每个 sample 的随机波动。

另一个是 bias random walk：

$$
n_{bg},n_{ba}
$$

表示 bias 自身慢慢漂。 这两个 noise 在 IMU model 中扮演不同角色。 实际配置 VIO 时非常重要。

### 68. IMU 参数为什么不好“随便调”？

因为预积分 covariance：

$$
\Sigma_{imu}
$$

会根据这些 noise 参数传播。

如果你把 noise 设得过小：

> optimizer 过度相信 IMU。

设得太大：

> optimizer 几乎不信 IMU。

所以好的系统通常会参考：

- datasheet
- Allan variance
- 实际静态测试

估计 noise。

### 69. Allan Variance 是什么？

现在不用深入推导。 只要知道它是分析 IMU noise 特性的一种经典方法。

通过长时间静止数据，可以估计：

- white noise
- bias instability
- random walk

从而给 estimator 更合理的 noise parameters。

### 70. VIO Failure 通常有哪些原因？

现在你已经可以自己推出来。

如果 Visual：

$$
weak
$$

同时 IMU initialization / bias 也不准， 系统很容易失败。

典型包括：

- 长时间低纹理
- 极强 motion blur
- IMU saturation
- 时间戳错误
- 外参错误
- 初始化运动不足
- 动态物体占据大部分视野
- 高振动

所以 VIO failure 往往不是“某个算法模块单独坏了”，而是整个 measurement consistency 被破坏。

### 71. 为什么 IMU Saturation 很危险？

Gyro / Accel 有量程。

例如真实：

$$
\omega
$$

超过 sensor maximum。 测出来被截断。 那么这不再是普通 Gaussian noise。

而是：

Model violation Preintegration 会彻底错误。 所以高动态机器人要特别注意 IMU range。

### 72. 一个成熟 VIO Pipeline

我们可以把它压成：

```
Camera + IMU
      ↓
Time Synchronization
      ↓
IMU Propagation
      ↓
Visual Tracking
      ↓
Keyframe Selection
      ↓
IMU Preintegration
      ↓
Build Visual + IMU Factors
      ↓
Sliding Window Optimization
      ↓
Marginalize Old State
      ↓
Current Pose / Velocity / Bias
```

如果再有 Loop Closure：

```
      ↓
Long-term Global Optimization
```

这就是非常典型的现代 VIO 架构。

### 73. LIO Pipeline 也几乎同构

```
LiDAR + IMU
      ↓
Time Synchronization
      ↓
IMU Propagation
      ↓
Deskew
      ↓
Scan / Map Matching
      ↓
LiDAR Geometric Residuals
      ↓
IMU Factors
      ↓
State Estimation
      ↓
Pose / Velocity / Bias
```

所以 VIO 和 LIO 在系统层的共性很强。

### 74. 差别主要在哪？

VIO 的外部观测：

$$
Photometric / Reprojection\ Geometry
$$

LIO：

$$
3D\ Geometric\ Alignment
$$

但：

- State
- IMU model
- bias
- gravity
- propagation
- observability
- optimization

很多部分是共享思想。

### 75. Filter-based LIO 为什么也很流行？

并不是所有 LIO 都是 Factor Graph / Sliding Window。

一些系统更偏：

Iterated EKF 路线。

原因之一是：

- 高频
- 点云 measurement 多
- 需要高实时性

所以 Filter 仍然非常有竞争力。

这再次说明：

Filtering 和 Smoothing 没有绝对谁淘汰谁 它们是不同计算-精度权衡。

### 76. 什么情况下更偏 Filtering？

如果：

- 高频实时
- State 规模相对固定
- 计算预算严格
- 需要低延迟

Filtering 很有吸引力。

### 77. 什么情况下 Smoothing 更有优势？

如果：

- 非线性强
- 希望重新 linearize
- 多 sensor factors
- 可以维护一小段窗口

Sliding-window optimization 往往更强。 所以 VIO 里两种路线长期并存。

### 78. IMU Propagation 和 Optimization 为什么同时需要？

实时系统经常：

IMU 每来一帧：

propagate state

得到高频：

$$
Pose_{pred}
$$

Camera / LiDAR measurement 到来后：

$$
optimize / update
$$

修正 drift。 所以输出频率甚至可以跟 IMU 走。

### 79. 这其实就是 Fast Loop / Slow Loop

IMU：

Fast loop

负责：

Prediction

视觉 / LiDAR：

Slower loop

负责：

Correction 这种多频率架构在机器人系统里非常常见。

### 80. 为什么 IMU 适合作为 Motion Prior？

比如 Visual Tracking 当前帧到来。

不用从：

unknown pose 开始搜。

IMU 已经给：

$$
T_{pred}
$$

于是 feature projection：

$$
\hat p_j=\pi(T_{pred}P_j)
$$

可以只在附近搜索。 因此 IMU 不只是 backend sensor。

它还直接帮助：

Front-end Association

### 81. Camera / LiDAR Failure 时 IMU 可以撑多久？

没有一个固定答案。

取决于：

- IMU quality
- bias accuracy
- motion intensity
- initial state

通常：

> 短时间很好用，长时间不可依赖。

这是 IMU 最典型的特性。

### 82. 这里有一个很重要的 Sensor Fusion 思维

不要问：

> “哪个 sensor 更准？”

更应该问：

哪个 sensor 在什么时间尺度、什么 state direction 上提供更强 information？

例如：

Gyro：

short-term rotation 极强。

Camera：

longer-term geometric orientation 更稳定。

GPS：

global position 但频率低。 不同 sensors 是在不同 state direction / frequency range 上互补。

### 83. 这就是 Frequency Complementarity

可以粗略理解：

IMU：

High Frequency

Camera/LiDAR：

Medium Frequency

GPS：

Low Frequency, Global

所以成熟机器人定位系统常常：

Multi-rate State Estimation 而不是“挑一个最强 sensor”。

### 84. 本章最重要的十句话

如果最后只记这些就够了。

$$
\boxed{ 1.\ IMU\ 负责高频短期 Propagation }
$$

$$
\boxed{ 2.\ Camera/LiDAR\ 负责长期几何 Correction }
$$

$$
\boxed{ 3.\ VIO/LIO\ State 不只有 Pose，还有 Velocity + Bias }
$$

$$
\boxed{ 4.\ Gravity 是 IMU 系统的重要状态/参考 }
$$

$$
\boxed{ 5.\ IMU Bias 必须在线估计，否则积分 Drift 很快 }
$$

$$
\boxed{ 6.\ Preintegration 把两帧之间大量 IMU Measurements 压成一个 Factor }
$$

$$
\boxed{ 7.\ VIO/LIO 本质仍然是 Factor / Residual / State Estimation }
$$

$$
\boxed{ 8.\ Sliding Window 控制状态规模 }
$$

$$
\boxed{ 9.\ Marginalization 删除旧 State，但保留其 Information }
$$

$$
\boxed{ 10.\ 多传感器 Fusion 的本质不是平均，而是 Joint State Estimation }
$$

> 修订说明：草稿把三维 gyro 向量直接放进矩阵 exp，现补上 hat 映射。旋转预积分为 ΔR = ∏ₖ exp(((ωₖ − b_g)Δtₖ)^∧)，按时间顺序右乘；噪声、bias 更新与线性化误差另通过预积分协方差和 bias Jacobian 处理。R_i 是 IMU-to-world，残差中的 R_iᵀ 将世界系差量转回起始 IMU 系。单目 VIO 的 metric scale 可观测要求有效加速度激励与 bias／重力的可区分性，不能仅凭“有 IMU”保证。

> 适用边界：本章讲解预积分状态量、主要残差与 bias 修正的结构，未给出完整噪声离散化及协方差递推，不应直接作为完整 VIO 实现公式。VIO/LIO 首先是里程计或状态估计；与回环、全局地图管理结合后才形成完整 SLAM 系统。

## 思考题

### Q1：为什么 IMU 频率很高，却不能单独长期定位？

**参考答案**

因为：

$$
Gyro
$$

需要积分得到 Orientation， Accelerometer 要积分一次得到 Velocity、再积分一次得到 Position。

任何：

$$
Bias + Noise
$$

都会被积分积累。 特别是 position error 可能随时间快速增长。

所以 IMU 适合：

Short-term propagation 不适合单独长期绝对定位。


### Q2：为什么 VIO 必须把 Velocity 放进 State？

**参考答案**

因为 IMU dynamics：

$$
\dot p=v
$$

$$
\dot v=R(a_m-b_a)+g
$$

Velocity 是连接 Position 和 Acceleration 的核心状态。

如果没有：

$$
v
$$

无法正确表达连续运动模型。


### Q3：为什么 Bias 不能只在出厂时 calibration 一次然后固定？

<details>

<summary>参考答案</summary>

因为真实 IMU bias 会随：

- 时间
- 温度
- 设备状态

缓慢变化。

所以一般建模成：

Random Walk 作为动态 state 在线估计。

</details>

### Q4：为什么需要 IMU Preintegration？

**参考答案**

因为 Camera 两帧之间可能有几十甚至上百个 IMU measurements。 如果每个 IMU sample 都创建一个 state / factor，问题太大。

Preintegration 把这段高频 measurements 压缩成：

$$
\Delta R,\Delta v,\Delta p
$$

形成一个 Keyframe-to-Keyframe IMU Factor。


### Q5：为什么 Monocular + IMU 可以恢复 Metric Scale？

**参考答案**

纯视觉投影对整体 scale 不敏感。

但 IMU acceleration 使用真实物理单位：

$$
m/s^2
$$

所以视觉 trajectory 必须选择一个正确 scale，才能与 IMU dynamics 一致。

因此充分运动条件下：

$$
Scale
$$

可以变得 observable。


### Q6：为什么有 IMU 还需要充分运动激励？

<details>

<summary>参考答案</summary>

因为某些 states 会耦合。

例如：

Gravity, Accel Bias, Scale 在静止或退化运动下可能很难区分。 不同方向的 rotation / acceleration 会让 measurement 对这些 states 的影响变得不同， 从而提供可观测信息。

</details>

### Q7：为什么 Sliding Window 中旧 State 不能直接删除？

<details>

<summary>参考答案</summary>

因为旧 state 承载了历史 measurements 对当前状态的约束。 直接删除会丢 information。

所以要：

Marginalization

把历史信息压成新的：

Prior Factor

</details>

### Q8：为什么 Marginalization 可能带来一致性问题？

<details>

<summary>参考答案</summary>

因为它是在某个 linearization point 上把历史 nonlinear information 压缩成 prior。 之后 state 继续变化， 但历史原始 measurements 已经不存在，不能完全重新 linearize。 因此不恰当处理可能引入虚假 information。

</details>

### Q9：VIO 和 LIO 最大的共同点是什么？

**参考答案**

两者都可以看成：

$$
\boxed{ IMU\ Motion\ Model + External\ Geometric\ Observation }
$$

VIO 外部 observation 来自：

$$
Camera
$$

LIO 来自：

$$
LiDAR
$$

但 State、Bias、Gravity、Propagation、Observability 等思想高度统一。


### Q10：Tightly Coupled 为什么通常比 Loosely Coupled 信息利用更充分？

**参考答案**

因为 Tight Coupling 直接使用：

$$
Pixel / Feature / LiDAR\ Residual
$$

和：

IMU Residual 联合优化原始 State。

而 Loose Coupling 往往先把一个 sensor 的大量原始信息压成：

$$
Pose
$$

再融合。 因此会丢失一部分 measurement-level structure。


## 相关章节与来源

- 上一章：[回环检测与全局校正](loop-closure.md)
- 下一篇：[现代 SLAM 流程与系统设计](modern-slam-pipeline.md)
- 来源：本次新增 Part IV Chapter 47 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
- 核验参考：[Forster 等：On-Manifold Preintegration](https://arxiv.org/abs/1512.02363)。
