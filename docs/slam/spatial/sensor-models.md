---
title: 传感器观测模型
description: 如何从状态与地图预测传感器观测，并构造残差？
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 33
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 传感器观测模型

## 本章目标

理解 Range–Bearing、相机、LiDAR 与 IMU 如何把状态变成观测。

## 前置知识

[坐标变换](coordinate-frames.md)、[Jacobian](../probabilistic/jacobian.md)、[位姿不确定性](pose-uncertainty.md)。

## 定义与假设

观测函数 h 由状态、地图和传感器标定共同决定；加性零均值噪声是一种建模选择。不同观测分量单位不同，必须连同噪声协方差一起定义。

Motion Model 回答：

> 我根据过去认为自己在哪？

Sensor Model 回答：

> 如果我真的在这里，我应该看到什么？

这两个方向正好相反。

---

## 1. Observation Model

一般写成：

$$
\boxed{ z_t=h(x_t,m)+v_t }
$$

其中：

- $$x_t$$：机器人 State；
- $$m$$：Environment / Map；
- $$z_t$$：Sensor Measurement；
- $$v_t$$：Measurement Noise。

例如：

> 如果机器人真的在 Pose $$x$$，地图里这堵墙应该在 Camera 什么位置？

预测：

$$
\hat z=h(x,m)
$$

真实 Sensor 得到：

$$
z
$$

Innovation：

$$
\boxed{ r=z-\hat z }
$$

于是 Observation 开始约束 State。

---

## 2. Range-Bearing Model

假设地图中 Landmark：

$$
m_i= \begin{bmatrix} m_x\\m_y \end{bmatrix}
$$

机器人：

$$
x= \begin{bmatrix} x\\y\\\theta \end{bmatrix}
$$

距离预测：

$$
\hat r = \sqrt{(m_x-x)^2+(m_y-y)^2}
$$

方向预测：

$$
\hat\alpha = \operatorname{atan2}(m_y-y,m_x-x)-\theta
$$

所以：

$$
\hat z= \begin{bmatrix} \hat r\\ \hat\alpha \end{bmatrix}
$$

真实 Sensor：

$$
z= \begin{bmatrix} r\\ \alpha \end{bmatrix}
$$

两者差异就提供 Localization Information。

---

## 3. Camera Sensor Model

三维 Landmark：

$$
P_W
$$

Camera Pose：

$$
T_{CW}
$$

先转换：

$$
P_C=T_{CW}P_W
$$

然后 Perspective Projection：

$$
u=f_x\frac{X_C}{Z_C}+c_x
$$

$$
v=f_y\frac{Y_C}{Z_C}+c_y
$$

所以：

$$
\boxed{ z=h(T_{CW},P_W) }
$$

Observation 是：

$$
(u,v)
$$

State 是：

$$
T
$$

Map 是：

$$
P_W
$$

这就是 Visual SLAM 最基本的 Observation Model。

---

## 4. LiDAR Sensor Model

LiDAR 情况下，可以预测：

> 如果机器人在这个 Pose，从这个方向打一束 Laser，理论上应该撞到地图哪个位置？

实际测量：

$$
z
$$

预测：

$$
\hat z
$$

二者差异约束 Pose。

实际工程里不一定显式做 Ray Casting。

ICP / Scan Matching 本质上也是：

> 找一个 Pose，让当前 Observation 与 Map / Previous Scan 尽可能一致。

---

## 5. IMU Observation 有点特殊

Gyroscope：

$$
\omega_m=\omega+b_g+n_g
$$

Accelerometer：

$$
a_m=R^T(a-g)+b_a+n_a
$$

IMU Measurement 同时受到：

- Motion；
- Gravity；
- Bias；
- Noise；

影响。

因此 VIO State 通常不仅有 Pose：

$$
x= [ p,v,R,b_a,b_g ]
$$

这也是为什么 IMU Fusion 比“Camera + Encoder 做个加权平均”复杂得多。

---

## 6. Measurement Jacobian

Observation Model：

$$
z=h(x)
$$

如果非线性，EKF 在当前 State 附近线性化：

$$
h(x+\delta x) \approx h(x)+H\delta x
$$

其中：

$$
\boxed{ H=\frac{\partial h}{\partial x} }
$$

Part II 我们讲 Observability 时说：

> Observation 是否能约束 State，取决于 State 变化能否反映到 Measurement 上。

现在数学上就是：

$$
H
$$

如果 State 某个方向变化，对 Observation 几乎没有影响：

$$
H\delta x\approx0
$$

那么这个方向的信息就很弱。

---

## 7. Sensor Model 最核心的思想

不是：

> Sensor 告诉机器人 State 是多少。

而是：

$$
\boxed{ State \xrightarrow{Observation\ Model} Expected\ Measurement }
$$

然后比较：

$$
Expected\ Measurement \quad vs\quad Actual\ Measurement
$$

反过来修正 State。

这其实是一个非常重要的思想转变。

## 模型边界与 Range–Bearing Jacobian

为避免状态与坐标同名，令机器人状态为 [X,Y,θ]ᵀ，d_x = m_x − X、d_y = m_y − Y，q = d_x² + d_y² > 0。对距离与方向预测分别求导：

$$
H=\begin{bmatrix}
-d_x/\sqrt q&-d_y/\sqrt q&0\\
d_y/q&-d_x/q&-1
\end{bmatrix}.
$$

第一行来自平方根的链式法则；第二行使用 atan2 对横、纵坐标的偏导，并考虑 d_x、d_y 对机器人坐标的负号。方向创新必须 wrap 到一致的角度区间，不能把跨越 ±π 的差当作接近 2π 的误差。

### 推导得到什么

H 是 2×3 矩阵：一项二维地标观测只提供两个局部约束，单次观测不足以单独确定三个位姿自由度。

### 在 SLAM 中怎么用

H 用于 EKF 校正、创新协方差和候选地标门控。地标与机器人重合时 q = 0，方向未定义，此模型不适用。

相机公式采用已标定、忽略畸变的针孔模型，要求 Z_C > 0；P_C = T_CW P_W 应理解为齐次坐标变换，输出三维坐标后再投影。IMU 公式中 R 把 IMU 系映射到世界系，a 与 g 均在世界系表达，a_m 是 IMU 系的比力，单位 m/s²；角速度单位 rad/s，bias 与对应测量同单位。

> 修订说明：补充了方向残差 wrap、针孔模型条件与 IMU frame 定义。前文 h(x+δx) 只用于欧氏状态；位姿状态应改用与左右扰动一致的 Exp 更新后求导。

## 本章小结

传感器模型从状态与地图预测观测，残差在观测空间中计算，Jacobian 表达状态变化如何影响观测。坐标系、单位、角度区间和标定条件共同决定残差是否有意义。

## 自测

为什么必须先预测观测，再构造残差？

<details>

<summary>参考答案</summary>

预测与实测必须在同一观测空间比较，残差才有正确的单位和几何含义。通过 Jacobian 可把观测差异转换为状态约束。

</details>

## 相关章节与来源

- 上一章：[机器人运动模型](robot-motion-models.md)
- 下一篇：[已知地图中的定位](localization.md)
- 来源：本次新增的 Part III 课堂草稿，按实际课程内容整理。
