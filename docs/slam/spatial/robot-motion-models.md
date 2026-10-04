---
title: 机器人运动模型
description: 如何把轮速与编码器读数变成带不确定性的位姿预测？
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 32
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 机器人运动模型

## 本章目标

把差速底盘运动学、轮编码器与预测协方差联系起来。

## 前置知识

[二维位姿与 SE(2)](se2.md)、[里程计漂移](../foundations/odometry-and-drift.md)、[EKF](../probabilistic/ekf.md)。

## 定义与假设

状态为世界系平面位姿 [X,Y,θ]；轮速单位 m/s，轮距 b > 0，角速度单位 rad/s。差速模型假设平面运动、轮子纯滚动且无侧滑；Gaussian 过程噪声只是近似。

## 1. Motion Model 到底是什么？

Part II 我们一直写：

$$
x_t=f(x_{t-1},u_t)+w_t
$$

现在终于可以具体化。

对于机器人：

$$
x_t=\text{Pose}
$$

$$
u_t=\text{control / odometry}
$$

Motion Model 描述：

> 已知上一时刻机器人在哪，以及这一段时间机器人“做了什么”，当前应该在哪里？

注意：

$$
\boxed{\text{Control Command}\neq\text{Actual Motion}}
$$

你给扫地机：

```
左轮 0.3 m/s
右轮 0.3 m/s
```

只是 command。

真实运动可能受到：

- 轮胎打滑；
- 地毯；
- 碰撞；
- 电机误差；
- 轮径误差；
- 地面不平；

影响。

所以 Motion Model 给出的永远是：

$$
p(x_t|x_{t-1},u_t)
$$

而不是一个绝对 Truth。

---

## 2. Differential Drive

差速机器人两个驱动轮：

- 左轮速度 $$v_L$$
- 右轮速度 $$v_R$$
- 轮距 $$b$$

机器人中心线速度：

$$
\boxed{ v=\frac{v_R+v_L}{2} }
$$

角速度：

$$
\boxed{ \omega=\frac{v_R-v_L}{b} }
$$

如果：

$$
v_R=v_L
$$

则：

$$
\omega=0
$$

直线运动。

如果：

$$
v_R=-v_L
$$

则：

$$
v=0
$$

原地旋转。

---

## 3. Pose 更新

二维 Pose：

$$
x= \begin{bmatrix} X\\Y\\\theta \end{bmatrix}
$$

小时间：

$$
\Delta t
$$

最简单离散模型：

$$
X_{t+1} = X_t+v\cos\theta_t\Delta t
$$

$$
Y_{t+1} = Y_t+v\sin\theta_t\Delta t
$$

$$
\theta_{t+1} = \theta_t+\omega\Delta t
$$

这就是一个最基本 Motion Model。

---

## 4. 为什么这是近似？

因为这里实际上假设：

$$
\theta
$$

在整个 $$\Delta t$$ 内基本不变。

但如果机器人同时：

- 前进；
- 转弯；

它真实走的是圆弧。

因此更准确的模型可以利用：

$$
R=\frac{v}{\omega}
$$

积分圆弧运动。

这也是前面学习 $$SE(2)$$ Exp 的物理来源之一：

> Lie Group 的指数映射，本质上就是把瞬时速度正确积分成有限刚体运动。

---

## 5. Encoder 如何得到 Motion？

如果左右轮半径为 $$r$$，编码器测得角度变化：

$$
\Delta\phi_L,\quad\Delta\phi_R
$$

轮子走过：

$$
\Delta s_L=r\Delta\phi_L
$$

$$
\Delta s_R=r\Delta\phi_R
$$

于是：

$$
\Delta s = \frac{\Delta s_R+\Delta s_L}{2}
$$

$$
\Delta\theta = \frac{\Delta s_R-\Delta s_L}{b}
$$

再转成机器人 Pose Increment。

这就是 Wheel Odometry。

---

## 6. 为什么 Encoder 很准，Odometry 还是会漂？

这里要区分：

> Measurement Accuracy 与 Model Validity。

Encoder 可以非常准确地告诉你：

> 轮子转了多少。

但它不能保证：

> 机器人真的移动了这么多。

例如机器人卡住：

```
Wheel rotates
Robot doesn't move
```

Encoder 没有测错。

错的是：

$$
\text{wheel rotation}\rightarrow\text{robot displacement}
$$

这个 Motion Model 假设失效。

这和我们 Part II 讲过的：

> Innovation 异常时，不应该第一时间怀疑 Sensor。

完全连起来了。

---

## 7. Process Noise 从哪里来？

写成：

$$
x_t=f(x_{t-1},u_t)+w_t
$$

其中：

$$
w_t\sim\mathcal N(0,Q)
$$

$$Q$$ 表示 Motion Model 的不确定性。

来源可能包括：

- Wheel slip；
- Encoder quantization；
- Wheel radius calibration；
- Uneven ground；
- Mechanical deformation；
- Unmodeled dynamics。

但要注意：

> Wheel Slip 往往并不是真正 Gaussian。

严重打滑属于：

$$
\boxed{\text{Model Failure / Outlier}}
$$

而不是单纯“把 $$Q$$ 调大一点”就解决。

---

## 8. Motion Covariance 如何传播？

状态：

$$
x_t=f(x_{t-1},u_t)
$$

线性化：

$$
F= \frac{\partial f}{\partial x}
$$

$$
G= \frac{\partial f}{\partial u}
$$

输入噪声协方差记为 $$Q_u$$，额外加性状态噪声记为 $$Q_w$$；假设噪声与上一状态误差相互独立。一阶协方差传播：

$$
\boxed{ P_t^- \approx FP_{t-1}F^T + GQ_uG^T + Q_w }
$$

这就是 Part II Kalman Prediction：

$$
P^-=FPF^T+Q
$$

在机器人 Motion Model 中的具体版本。

---

## 9. Motion Model 的核心认识

Motion Model 不是：

> “机器人下一帧在哪。”

而是：

$$
\boxed{ \text{机器人下一帧可能在哪，以及有多不确定} }
$$

随着只靠 Odometry 不断运动，误差通常累积；但协方差矩阵没有逐元素严格递增的一般结论：

$$
\text{纯里程计通常随运动积累不确定性}
$$

Belief 会越来越散。

这就是为什么机器人需要 Observation 来不断 Correction。

## 补充推导与例题：圆弧积分、Jacobian 与噪声

当 v、ω 在 Δt 内恒定，积分 Ẋ = v cos θ、Ẏ = v sin θ、θ̇ = ω，得到（ω ≠ 0）：

$$
\begin{aligned}
\theta'&=\theta+\omega\Delta t,\\
X'&=X+\frac v\omega[\sin(\theta+\omega\Delta t)-\sin\theta],\\
Y'&=Y+\frac v\omega[\cos\theta-\cos(\theta+\omega\Delta t)].
\end{aligned}
$$

ω → 0 时连续退化为直线模型。这里指数映射积分的是恒定 twist；速度随时间改变时，还需逐段积分。

对于前文 Euler 近似，u = [v,ω]ᵀ：

$$
F=\begin{bmatrix}1&0&-v\sin\theta\Delta t\\0&1&v\cos\theta\Delta t\\0&0&1\end{bmatrix},\qquad
G=\begin{bmatrix}\cos\theta\Delta t&0\\\sin\theta\Delta t&0\\0&\Delta t\end{bmatrix}.
$$

设输入噪声协方差 Q_u 为 2×2，额外加性状态噪声协方差 Q_w 为 3×3，并假设它们与上一状态误差相互独立。由 δx' ≈ Fδx + Gδu + w，取协方差得到：

$$
P'\approx FPF^T+GQ_uG^T+Q_w.
$$

### 推导得到什么

Q_u 是速度输入的不确定性，GQ_uGᵀ 才是其在位姿空间中的贡献；Q_w 是额外未建模状态噪声。两者若描述同一误差来源，不能重复计入。

### 在 SLAM 中怎么用

机器人朝向会把前进速度的不确定性旋转到不同的世界方向；F 的第三列体现朝向误差如何变成后续位置误差。

### 例题

轮距 b = 0.5 m，v_L = 0.2 m/s、v_R = 0.4 m/s，起点 [0,0,0]，Δt = 1 s。则 v = 0.3 m/s、ω = 0.4 rad/s，转弯半径为 0.75 m。

$$
X'=0.75\sin0.4\approx0.2921\text{ m},\quad
Y'=0.75(1-\cos0.4)\approx0.0592\text{ m},\quad\theta'=0.4\text{ rad}.
$$

Euler 给出 [0.3,0,0.4]，漏掉转弯产生的侧向位移。

> 修订说明：草稿将加性状态噪声 Q 与输入噪声 Q 混用，现分为 Q_w、Q_u；删除协方差严格逐项递增的写法。草稿末尾预告的 Ackermann 与全向底盘尚无实际讲解，本次不计作已完成内容。

## 本章小结

差速运动学把轮速转成中心速度与角速度，再由时间积分得到位姿增量。编码器准确不代表纯滚动模型始终有效；预测必须同时传播误差，观测用于约束累积漂移。

## 自测

编码器准确为何仍会漂移？

<details>

<summary>参考答案</summary>

它测量轮子转角；从轮转到位移还依赖纯滚动、轮径与轮距模型。打滑时观测可以准确而运动模型失效。

</details>

## 相关章节与来源

- 上一章：[SE(3) 上的位姿不确定性](pose-uncertainty.md)
- 下一篇：[传感器观测模型](sensor-models.md)
- 来源：本次新增的 Part III 课堂草稿，按实际课程内容整理。
