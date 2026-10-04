---
title: 三维位姿与 SE(3)
description: 三维位姿与 SE(3)的课程笔记。
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 29
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 三维位姿与 SE(3)

这一章把前面的内容正式合并起来：

* Chapter 27：(SO(3))，三维旋转；
* Chapter 28：Quaternion，三维姿态的另一种表示；
* Chapter 29：把三维 Rotation 与 Translation 组合成完整的 6-DoF Pose。

核心结论是：

> **三维 Pose 不是普通的六维向量，而是 (SE(3)) 上的一个刚体变换。**

---

## 1. 三维 Pose 到底包含什么？

一个刚体在三维空间中的 Pose 包含：

* 三维位置；
* 三维方向。

位置：

$$
t=
\begin{bmatrix}
t_x\\
t_y\\
t_z
\end{bmatrix}
\in\mathbb R^3
$$
方向：

$$
R\in SO(3)
$$
因此齐次变换矩阵写成：

$$
\boxed{
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
}
$$
展开：

$$
T=
\begin{bmatrix}
r_{11}&r_{12}&r_{13}&t_x\\
r_{21}&r_{22}&r_{23}&t_y\\
r_{31}&r_{32}&r_{33}&t_z\\
0&0&0&1
\end{bmatrix}
$$
所有合法三维刚体变换组成：

$$
\boxed{
SE(3)
=
\left\{
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
\middle|
R\in SO(3),\ t\in\mathbb R^3
\right\}
}
$$
---

## 2. (SE(3)) 有几个自由度？

三维 Translation 有：

$$
3\text{ DoF}
$$
三维 Rotation 有：

$$
3\text{ DoF}
$$
所以：

$$
\boxed{
SE(3)\text{ has }6\text{ DoF}
}
$$
分别是：

* (x,y,z)
* roll, pitch, yaw

不过后面这三个只是一种参数表达。更严格地说是：

* 三维平移自由度；
* 三维旋转自由度。

齐次矩阵虽然有 16 个元素，但绝大多数元素受结构约束，并不是 16 个独立变量。

---

## 3. 三维点如何通过 Pose 变换？

某个点在坐标系 (B) 中表示为：

$$
{}^B p
$$
坐标系 (B) 相对于 (A) 的 Pose：

$$
{}^A T_B
=
\begin{bmatrix}
{}^A R_B&{}^A t_B\\
0&1
\end{bmatrix}
$$
则：

$$
\boxed{
{}^A p
=
{}^A R_B\,{}^B p
+
{}^A t_B
}
$$
使用齐次坐标：

$$
{}^A\tilde p
=
{}^A T_B\,{}^B\tilde p
$$
其中：

$$
\tilde p=
\begin{bmatrix}
p\\1
\end{bmatrix}
$$
---

## 4. Translation 的真正含义

$$
{}^A t_B
$$
表示：

> 坐标系 (B) 的原点，在坐标系 (A) 中的坐标。

它不是一个没有 Frame 的普通位移。

例如：

$$
{}^W t_C
$$
和：

$$
{}^R t_C
$$
即使描述同一个 Camera 原点，数值也可能完全不同，因为表达坐标系不同。

所以看到一个三维 Translation 时，必须问：

> 它是在哪个 Frame 中表达的？

---

## 5. Pose Composition

假设：

$$
{}^A T_B
=
\begin{bmatrix}
R_{AB}&t_{AB}\\
0&1
\end{bmatrix}
$$
$$
{}^B T_C
=
\begin{bmatrix}
R_{BC}&t_{BC}\\
0&1
\end{bmatrix}
$$
则：

$$
\boxed{
{}^A T_C
=
{}^A T_B\,{}^B T_C
}
$$
展开得到：

$$
\boxed{
R_{AC}
=
R_{AB}R_{BC}
}
$$
以及：

$$
\boxed{
t_{AC}
=
t_{AB}+R_{AB}t_{BC}
}
$$
这和 (SE(2)) 完全同构，只是 Rotation 从二维变成三维。

---

## 6. 为什么 Translation 不能直接相加？

因为：

$$
t_{AB}
$$
在 (A) Frame 中表达。

而：

$$
t_{BC}
$$
在 (B) Frame 中表达。

不同坐标系中的向量不能直接相加。

必须先：

$$
R_{AB}t_{BC}
$$
把 (t_{BC}) 转成 (A) Frame，再与 (t_{AB}) 相加。

所以：

$$
t_{AC}
=
t_{AB}+R_{AB}t_{BC}
$$
这就是 Rotation 和 Translation 在 Pose Composition 中发生耦合的地方。

---

## 7. 一个具体的三维例子

假设机器人 Base Frame (B) 在 World Frame (W) 中：

* 位置：

$$
{}^W t_B=
\begin{bmatrix}
1\\2\\0
\end{bmatrix}
$$
* 朝向：绕世界 (z) 轴旋转 (90^\circ)

所以：

$$
{}^W R_B
=
R_z(90^\circ)

\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}
$$
Camera Frame (C) 位于机器人局部前方 1 米：

$$
{}^B t_C=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
并且与 Base 朝向相同：

$$
{}^B R_C=I
$$
那么 Camera 在 World 中的位置：

$$
{}^W t_C
=
{}^W t_B+{}^W R_B\,{}^B t_C
$$
$$
\begin{bmatrix}
1\\2\\0
\end{bmatrix}
+
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
$$
\begin{bmatrix}
1\\2\\0
\end{bmatrix}
+
\begin{bmatrix}
0\\1\\0
\end{bmatrix}
=
\boxed{
\begin{bmatrix}
1\\3\\0
\end{bmatrix}
}
$$
局部“前方 1 米”由于机器人已经旋转，在世界中变成了 (y) 方向。

---

## 8. (SE(3)) 为什么不可交换？

一般来说：

$$
T_1T_2\neq T_2T_1
$$
原因有两层。

第一，三维 Rotation 本身不可交换：

$$
R_1R_2\neq R_2R_1
$$
第二，前一个 Rotation 会改变后一个 Translation 的方向：

$$
t_{12}=t_1+R_1t_2
$$
而交换顺序后：

$$
t_{21}=t_2+R_2t_1
$$
通常完全不同。

所以 (SE(3)) 是典型非交换群。

---

## 9. Pose Inverse

已知：

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$
则：

$$
\boxed{
T^{-1}
=
\begin{bmatrix}
R^T&-R^Tt\\
0&1
\end{bmatrix}
}
$$
验证：

$$
TT^{-1}
=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
\begin{bmatrix}
R^T&-R^Tt\\
0&1
\end{bmatrix}
$$
旋转部分：

$$
RR^T=I
$$
平移部分：

$$
R(-R^Tt)+t=-t+t=0
$$
所以结果是单位变换。

---

## 10. 为什么逆平移不是简单的 (-t)？

因为：

$$
t
$$
是在原参考系中表达的。

反向变换需要把这个反向位移表达在新的坐标系中，所以还要乘：

$$
R^T
$$
得到：

$$
-R^Tt
$$
这点在三维外参和 Pose 链里极其重要。

---

## 11. Relative Pose

已知两个 Pose：

$$
{}^W T_A
$$
和：

$$
{}^W T_B
$$
希望求 (B) 相对于 (A) 的 Pose：

$$
\boxed{
{}^A T_B
=
({}^W T_A)^{-1}
{}^W T_B
}
$$
展开 Rotation：

$$
\boxed{
{}^A R_B
=
({}^W R_A)^T
{}^W R_B
}
$$
展开 Translation：

$$
\boxed{
{}^A t_B
=
({}^W R_A)^T
\left(
{}^W t_B-{}^W t_A
\right)
}
$$
注意平移差先在 World Frame 中计算，再转到 (A) Frame。

---

## 12. Relative Pose 在机器人里为什么重要？

大量 Sensor 和算法输出的不是绝对 Pose，而是相对 Pose。

例如：

* Visual Odometry：

$$
{}^{C_{t-1}}T_{C_t}
$$
* Wheel Odometry：

$$
{}^{B_{t-1}}T_{B_t}
$$
* ICP：

$$
{}^{L_{t-1}}T_{L_t}
$$
* Loop Closure：

$$
{}^{K_i}T_{K_j}
$$
SLAM 的核心之一，就是把大量 Relative Pose Constraints 组合成全局一致的 Pose Graph。

---

## 13. 三维 Pose 为什么不能直接写成普通六维向量相加？

我们可以用参数表示：

$$
x=
\begin{bmatrix}
t_x\t_y\t_z\\
\phi_x\\phi_y\\phi_z
\end{bmatrix}
$$
但这只是局部或参数表示。

一般而言：

$$
x_{\text{new}}=x+\Delta x
$$
没有完整定义几何意义，因为：

* 平移增量在哪个 Frame 表达？
* 旋转增量左乘还是右乘？
* 大旋转不能简单相加；
* Rotation 与 Translation 会通过 Composition 耦合。

更合理的更新是：

$$
\boxed{
T_{\text{new}}
=
T\operatorname{Exp}(\delta\xi^\wedge)
}
$$
或者：

$$
T_{\text{new}}
=
\operatorname{Exp}(\delta\xi^\wedge)T
$$
---

## 14. (\mathfrak{se}(3))：(SE(3)) 的局部向量空间

三维 Pose 有 6 DoF。

因此可以用一个六维局部向量：

$$
\boxed{
\xi=
\begin{bmatrix}
\rho\\
\phi
\end{bmatrix}
=
\begin{bmatrix}
\rho_x\\
\rho_y\\
\rho_z\\
\phi_x\\
\phi_y\\
\phi_z
\end{bmatrix}
}
$$
其中：

* (\rho\in\mathbb R^3)：平移部分；
* (\phi\in\mathbb R^3)：旋转向量。

这个六维空间就是：

$$
\mathfrak{se}(3)
$$
也叫 (SE(3)) 的 Lie Algebra。

---

## 15. Hat 运算

六维向量：

$$
\xi=
\begin{bmatrix}
\rho\\
\phi
\end{bmatrix}
$$
通过 hat 运算映射成 (4\times4) 矩阵：

$$
\boxed{
\xi^\wedge
=
\begin{bmatrix}
\phi^\wedge&\rho\\
0&0
\end{bmatrix}
}
$$
其中：

$$
\phi^\wedge
=
\begin{bmatrix}
0&-\phi_z&\phi_y\\
\phi_z&0&-\phi_x\\
-\phi_y&\phi_x&0
\end{bmatrix}
$$
(\xi^\wedge) 可以理解为一个瞬时刚体运动：

* (\rho)：线速度方向；
* (\phi)：角速度方向。

因此 (\xi) 也常叫：

> Twist。

---

## 16. Twist 的物理意义

一个刚体的瞬时运动可以由：

$$
\xi=
\begin{bmatrix}
v\\
\omega
\end{bmatrix}
$$
描述。

其中：

* (v)：线速度；
* (\omega)：角速度。

如果把它乘以短时间：

$$
\Delta t
$$
得到：

$$
\xi\Delta t
$$
就可以通过指数映射生成这段时间内的有限刚体变换。

因此：

$$
T(\Delta t)
=
\operatorname{Exp}
((\xi\Delta t)^\wedge)
$$
这把：

> 瞬时速度

转换成：

> 有限 Pose Increment。

---

## 17. (SE(3)) 指数映射

给定：

$$
\xi=
\begin{bmatrix}
\rho\\
\phi
\end{bmatrix}
$$
则：

$$
\boxed{
\operatorname{Exp}(\xi)
=
\exp(\xi^\wedge)

\begin{bmatrix}
R&J(\phi)\rho\\
0&1
\end{bmatrix}
}
$$
其中：

$$
R=\operatorname{Exp}(\phi)
$$
是 (SO(3)) 指数映射。

而：

$$
J(\phi)
$$
通常称为：

> (SO(3)) Left Jacobian。

常见形式：

$$
\boxed{
J(\phi)
=
I
+
\frac{1-\cos\theta}{\theta^2}\phi^\wedge
+
\frac{\theta-\sin\theta}{\theta^3}
(\phi^\wedge)^2
}
$$
其中：

$$
\theta=|\phi|
$$
---

## 18. 为什么 Translation 不是直接 (\rho)？

因为 (\rho) 表示的是局部瞬时平移成分。

如果运动过程中同时发生 Rotation，那么线速度方向会随姿态变化。

最终有限 Translation 是：

$$
J(\phi)\rho
$$
而不总是：

$$
\rho
$$
这和 (SE(2)) 中的 (V(\phi)\rho) 是同一类结构。

---

## 19. 一个直观运动：一边前进一边转弯

假设机器人持续：

* 沿自身前方向前运动；
* 同时绕 (z) 轴旋转。

它最终走的是一段圆弧。

如果简单把局部平移 (\rho) 直接当作最终世界位移，就相当于假设：

```text
先直线移动
再原地旋转
```

这不符合真实连续运动。

指数映射会正确积分 Rotation 对 Translation Direction 的持续影响。

---

## 20. 小扰动近似

当：

$$
|\phi|\approx0
$$
有：

$$
R\approx I+\phi^\wedge
$$
并且：

$$
J(\phi)\approx
I+\frac12\phi^\wedge
$$
所以：

$$
\operatorname{Exp}(\xi)
\approx
\begin{bmatrix}
I+\phi^\wedge&
\rho+\frac12\phi^\wedge\rho\\
0&1
\end{bmatrix}
$$
一阶最粗略近似可写成：

$$
\operatorname{Exp}(\xi^\wedge)
\approx I+\xi^\wedge
$$
但更高精度时要保留 Jacobian 项。

---

## 21. (SE(3)) 对数映射

给定：

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$
希望恢复：

$$
\xi=
\operatorname{Log}(T)
$$
首先：

$$
\phi=\operatorname{Log}(R)
$$
然后：

$$
\boxed{
\rho
=
J(\phi)^{-1}t
}
$$
所以：

$$
\boxed{
\operatorname{Log}(T)
=
\begin{bmatrix}
J(\phi)^{-1}t\\
\phi
\end{bmatrix}
}
$$
注意不是简单：

$$
[t,\phi]
$$
因为 Translation 与 Rotation 在指数映射中发生了耦合。

---

## 22. Pose Error

假设：

* 测量 Pose：

$$
T_m
$$
* 预测 Pose：

$$
T_p
$$
不能用：

$$
T_p-T_m
$$
定义误差。

更合理的是构造相对误差变换：

$$
T_{\text{err}}
=
T_m^{-1}T_p
$$
然后：

$$
\boxed{
e
=
\operatorname{Log}
(T_m^{-1}T_p)
\in\mathbb R^6
}
$$
这个六维误差可以用于：

* Pose Graph；
* Bundle Adjustment；
* ICP；
* Kalman Innovation；
* Calibration；
* Control。

---

## 23. 为什么误差要映射到 Lie Algebra？

因为：

$$
T_{\text{err}}\in SE(3)
$$
仍然是一个群元素，不能直接放进普通最小二乘。

通过：

$$
\operatorname{Log}
$$
把它映射为：

$$
e\in\mathbb R^6
$$
就可以计算：

$$
e^T\Omega e
$$
并对局部增量做优化。

所以：

> State 保存在 Manifold 上，Error 和 Update 在 Tangent Space 中计算。

这是现代三维 SLAM 和视觉优化最基本的模式。

---

## 24. 左扰动与右扰动

右扰动：

$$
\boxed{
T_{\text{new}}
=
T\operatorname{Exp}(\delta\xi)
}
$$
通常表示增量在当前 Body / Local Frame 中表达。

左扰动：

$$
\boxed{
T_{\text{new}}
=
\operatorname{Exp}(\delta\xi)T
}
$$
通常表示增量在 Reference / Global Frame 中表达。

由于：

$$
SE(3)
$$
不可交换，两种更新不等价。

它们会导致不同的：

* Jacobian；
* Error Definition；
* Covariance Frame；
* Adjoint 转换。

不存在绝对“哪个更正确”，但整个系统必须保持一致。

---

## 25. 同一个小旋转对 Translation 的不同影响

假设 Camera 离机器人旋转中心有 1 米。

机器人发生小角度误差：

$$
\delta\theta
$$
即使机器人中心 Translation 没变，Camera 位置也会发生近似：

$$
\delta p
\approx
\delta\theta\times t
$$
的变化。

因此三维 Pose Error 中：

* Rotation Error；
* Translation Error；

并不是完全独立。

变换 Frame 或参考点后，它们会发生耦合。

---

## 26. (SE(3)) Adjoint

设：

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$
一个常见的 (SE(3)) Adjoint 形式为：

$$
\boxed{
\operatorname{Ad}_T
=
\begin{bmatrix}
R&t^\wedge R\\
0&R
\end{bmatrix}
}
$$
这里采用：

$$
\xi=
\begin{bmatrix}
\rho\\
\phi
\end{bmatrix}
$$
的排列。

不同教材若使用：

$$
[\phi,\rho]
$$
顺序，矩阵块排列会改变。

Adjoint 的作用是：

$$
\boxed{
\xi_A
=
\operatorname{Ad}_T\xi_B
}
$$
即把同一个 Twist、局部误差或扰动从一个 Frame 转换到另一个 Frame。

---

## 27. 为什么 Adjoint 中出现 (t^\wedge R)？

角速度在不同原点观察时，会产生额外线速度。

假设刚体绕某轴旋转，离旋转中心越远的点，线速度越大：

$$
v=\omega\times t
$$
这正是：

$$
t^\wedge R
$$
块表达的耦合。

所以 Adjoint 不是单纯把 Translation 和 Rotation 分别乘一个 (R)。

坐标系原点变化会让 Angular Component 转化成 Linear Component。

---

## 28. Twist 的 Frame 转换

假设：

$$
\xi_B=
\begin{bmatrix}
v_B\\
\omega_B
\end{bmatrix}
$$
是在 Frame (B) 中表达的刚体速度。

若：

$$
{}^A T_B
$$
已知，则：

$$
\boxed{
\xi_A
=
\operatorname{Ad}_{{}^A T_B}
\xi_B
}
$$
展开：

$$
\omega_A=R_{AB}\omega_B
$$
$$
v_A
=
R_{AB}v_B
+
t_{AB}\times
R_{AB}\omega_B
$$
第二项说明：

> 改变参考原点后，纯旋转会表现出额外的线速度。

---

## 29. Pose Covariance 的 Frame 转换

假设一个小 Pose Error：

$$
\delta\xi_B
$$
协方差：

$$
P_B
$$
通过：

$$
\delta\xi_A
=
\operatorname{Ad}_T\delta\xi_B
$$
转换到 Frame (A)。

则：

$$
\boxed{
P_A
=
\operatorname{Ad}_T
P_B
\operatorname{Ad}_T^T
}
$$
这与普通线性协方差传播：

$$
P_y=JP_xJ^T
$$
完全一致。

这里只是 Jacobian 由群结构中的 Adjoint 给出。

---

## 30. 外参不确定性如何影响世界坐标点？

假设 Camera 中观测点：

$$
{}^C p
$$
转换到 Robot Frame：

$$
{}^B p
=
{}^B R_C\,{}^C p
+
{}^B t_C
$$
如果 Camera Extrinsic Rotation 有小误差：

$$
\delta\phi
$$
点的位置误差近似包含：

$$
\delta p
\approx
-\left(Rp\right)^\wedge\delta\phi
+
\delta t
$$
所以：

* 点离 Camera 越远；
* Rotation 外参误差越小但不为零；

最终 Position Error 仍可能很大。

这也是三维标定中 Rotation Error 通常极其敏感的原因。

---

## 31. Camera–Robot–World 变换链

视觉系统中典型关系：

$$
{}^W T_C
=
{}^W T_B
{}^B T_C
$$
其中：

* ({}^W T_B)：机器人 Pose；
* ({}^B T_C)：Camera Extrinsic；
* ({}^W T_C)：Camera 在 World 中的 Pose。

如果 Camera 看到点：

$$
{}^C p
$$
则：

$$
{}^W p
=
{}^W T_B
{}^B T_C
{}^C p
$$
这里任何一个变换方向写反，最终结果都会严重错误。

最稳定的检查方法仍然是：

> 从右向左读 Frame Chain。

---

## 32. IMU 与 Camera 的 Pose 关系

视觉惯性系统中常见：

$$
{}^W T_C
=
{}^W T_I
{}^I T_C
$$
其中：

* ({}^W T_I)：IMU Pose；
* ({}^I T_C)：Camera–IMU Extrinsic。

IMU 的角速度、加速度天然在 IMU Frame 中表达。

视觉 Observation 天然在 Camera Frame 中表达。

因此 VIO 的一个核心工作就是：

> 在多个 Frame 之间正确转换 State、Measurement、Noise 和 Covariance。

数学公式本身不一定最难，Frame Convention 往往才是隐藏 Boss。

---

## 33. (SE(3)) 与 Quaternion 的关系

(SE(3)) 中 Rotation 部分可以使用：

* Rotation Matrix；
* Quaternion；
* Axis–Angle。

例如程序内部常保存：

$$
T=(q,t)
$$
而不是完整 (4\times4) Matrix。

Pose Composition：

$$
q_{AC}=q_{AB}\otimes q_{BC}
$$
$$
t_{AC}=t_{AB}+R(q_{AB})t_{BC}
$$
所以 Quaternion 只是 (SE(3)) 中 Orientation 部分的一种存储方式。

Pose 的群结构仍然是 (SE(3))。

---

## 34. (SE(3)) 与 Dual Quaternion

还有一种方法叫 Dual Quaternion，可以使用 8 个数统一表示：

* Rotation；
* Translation。

它在：

* 机器人运动学；
* 图形学；
* 骨骼动画；

中很有价值。

但 SLAM 和状态估计里，齐次矩阵、Quaternion + Translation、Lie Algebra 更常见。

这里知道它存在即可，暂时不展开。

---

## 35. Pose Graph 中的 (SE(3))

在三维 Pose Graph 中，每个节点：

$$
T_i\in SE(3)
$$
测量边：

$$
Z_{ij}\in SE(3)
$$
预测相对 Pose：

$$
\hat Z_{ij}=T_i^{-1}T_j
$$
误差：

$$
\boxed{
e_{ij}
=
\operatorname{Log}
\left(
Z_{ij}^{-1}
T_i^{-1}T_j
\right)
}
$$
其中：

$$
e_{ij}\in\mathbb R^6
$$
优化目标：

$$
\sum_{ij}
e_{ij}^T
\Omega_{ij}
e_{ij}
$$
这就是三维 Graph SLAM 中非常经典的基本形式。

---

## 36. ICP 中的 (SE(3))

假设源点：

$$
p_i
$$
目标点：

$$
q_i
$$
希望求：

$$
T\in SE(3)
$$
使：

$$
Tp_i
$$
与：

$$
q_i
$$
对齐。

Point-to-Point Residual：

$$
r_i
=
q_i-(Rp_i+t)
$$
Point-to-Plane Residual：

$$
r_i
=
n_i^T
(Rp_i+t-q_i)
$$
优化过程中使用：

$$
T\leftarrow
T\operatorname{Exp}(\delta\xi)
$$
这就是 (SE(3)) 在 Scan Matching 中的直接应用。

---

## 37. Bundle Adjustment 中的 (SE(3))

Camera Pose：

$$
T_{CW}
\in SE(3)
$$
World Point：

$$
P_W
$$
转换到 Camera：

$$
P_C=T_{CW}P_W
$$
再投影：

$$
u=\pi(P_C)
$$
重投影残差：

$$
r=u_{\text{obs}}-\pi(T_{CW}P_W)
$$
Pose 增量通常在 (\mathfrak{se}(3)) 中优化：

$$
T\leftarrow
\operatorname{Exp}(\delta\xi)T
$$
或右乘，取决于约定。

---

## 38. 为什么三维 SLAM 到处都是 (SE(3))？

因为 SLAM 中几乎所有核心对象都是 Pose：

* Robot Pose；
* Camera Pose；
* LiDAR Pose；
* Keyframe Pose；
* Relative Pose Constraint；
* Extrinsic Calibration；
* Loop Closure Transform。

而所有这些对象都需要：

* Composition；
* Inverse；
* Relative Transform；
* Small Perturbation；
* Covariance Transformation。

(SE(3)) 正是统一这些操作的数学结构。

---

## 39. 不要把 (\rho) 直接理解为最终 Translation

这是学习 (SE(3)) Exp/Log 时最常见的误区之一。

在：

$$
\xi=
\begin{bmatrix}
\rho\\
\phi
\end{bmatrix}
$$
中，(\rho) 是 Lie Algebra 坐标中的平移成分。

最终变换 Translation 是：

$$
t=J(\phi)\rho
$$
只有在：

$$
\phi\approx0
$$
时：

$$
t\approx\rho
$$
所以：

$$
\operatorname{Log}(T)
$$
的前三维一般也不等于直接的 (t)。

---

## 40. 数值实现中的小角度处理

Left Jacobian：

$$
J(\phi)
=
I
+
\frac{1-\cos\theta}{\theta^2}\phi^\wedge
+
\frac{\theta-\sin\theta}{\theta^3}
(\phi^\wedge)^2
$$
当：

$$
\theta\rightarrow0
$$
时会出现表面上的：

$$
0/0
$$
必须使用泰勒展开：

$$
\frac{1-\cos\theta}{\theta^2}
\approx
\frac12-\frac{\theta^2}{24}+\cdots
$$
$$
\frac{\theta-\sin\theta}{\theta^3}
\approx
\frac16-\frac{\theta^2}{120}+\cdots
$$
成熟库通常已经处理这些数值细节。

---

## 本章核心总结

第一：

$$
SE(3)
=
\left\{
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
\middle|
R\in SO(3)
\right\}
$$
是三维刚体 Pose 的数学空间。

第二：

Pose Composition：

$$
T_{AC}=T_{AB}T_{BC}
$$
平移部分为：

$$
t_{AC}=t_{AB}+R_{AB}t_{BC}
$$
第三：

Relative Pose：

$$
{}^A T_B
=
({}^W T_A)^{-1}
{}^W T_B
$$
第四：

$$
\mathfrak{se}(3)
$$
使用六维 Twist 表达局部 Pose 增量。

第五：

$$
T=\operatorname{Exp}(\xi)
$$
把局部瞬时运动映射成有限刚体变换。

第六：

Adjoint 用于在不同 Frame 之间转换：

* Twist；
* Pose Error；
* Covariance。

---

## 思考题与参考答案

## 思考题 1

为什么 (SE(3)) 有 6 DoF，但齐次矩阵有 16 个元素？

<details>

<summary>参考答案</summary>
齐次矩阵结构为：

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$
最后一行固定，不提供自由度。

(R) 虽有 9 个元素，但受：

$$
R^TR=I,\qquad\det R=1
$$
约束，只有 3 DoF。

(t) 有 3 DoF。

因此总计：

$$
3+3=6
$$

</details>

---

## 思考题 2

已知：

$$
{}^W T_A,\quad{}^W T_B
$$
为什么：

$$
{}^A T_B
=
({}^W T_A)^{-1}{}^W T_B
$$
而不是：

$$
{}^W T_B({}^W T_A)^{-1}
$$
<details>

<summary>参考答案</summary>
要把 (B) Frame 中的点转换到 (A) Frame，需要路径：

```text
B → W → A
```

从 (B) 到 (W) 使用：

$$
{}^W T_B
$$
从 (W) 到 (A) 使用：

$$
{}^A T_W
=
({}^W T_A)^{-1}
$$
矩阵从右向左作用，所以：

$$
{}^A T_B
=
{}^A T_W{}^W T_B

({}^W T_A)^{-1}{}^W T_B
$$

</details>

---

## 思考题 3

为什么一个纯旋转在改变参考原点后，可能产生线速度分量？

<details>

<summary>参考答案</summary>
离旋转中心距离为 (t) 的点，在角速度 (\omega) 下具有线速度：

$$
v=\omega\times t
$$
因此相同刚体运动，如果从不同原点描述，线速度部分会不同。

Adjoint 中的：

$$
t^\wedge R
$$
正是表达这种 Rotation-to-Translation Coupling。

</details>

---

## 思考题 4

为什么 Pose Error 更适合写成：

$$
e=
\operatorname{Log}
(T_m^{-1}T_p)
$$
而不是直接：

$$
T_p-T_m
$$
<details>

<summary>参考答案</summary>
(T_p) 和 (T_m) 属于 (SE(3))，不是普通线性空间中的向量。

矩阵相减：

* 没有明确刚体运动意义；
* 结果也不属于 (SE(3))；
* 不能自然表示“从一个 Pose 到另一个 Pose 的最小相对运动”。

而：

$$
T_m^{-1}T_p
$$
是合法的相对 Pose。

再通过 Log 映射得到六维局部误差，可以用于最小二乘与状态更新。

</details>

---

## 思考题 5

为什么 (\xi=[\rho,\phi]) 中的 (\rho) 一般不等于最终变换矩阵中的 Translation (t)？

<details>

<summary>参考答案</summary>
指数映射为：

$$
T=
\begin{bmatrix}
\operatorname{Exp}(\phi)&J(\phi)\rho\\
0&1
\end{bmatrix}
$$
当平移和旋转同时发生时，局部线速度方向在运动过程中持续旋转，因此最终 Translation 是积分结果：

$$
t=J(\phi)\rho
$$
只有在旋转很小时：

$$
J(\phi)\approx I
$$
才有：

$$
t\approx\rho
$$

</details>

---

## 思考题 6

Camera Extrinsic Translation 为 0，但 Rotation Extrinsic 有 (1^\circ) 误差。是否意味着世界坐标点只有角度误差、没有位置误差？

<details>

<summary>参考答案</summary>
不是。

对于 Camera 中距离较远的点，小 Rotation Error 会造成：

$$
\delta p
\approx
-\left(Rp\right)^\wedge\delta\phi
$$
的位置误差。

误差大小通常与点到 Camera 的距离成正比。

因此即使 Translation Extrinsic 完全正确，Rotation Extrinsic Error 也会直接造成三维位置偏差。

</details>

---

## 思考题 7

左乘更新和右乘更新为什么不能混用？

<details>

<summary>参考答案</summary>
左扰动与右扰动中的增量通常在不同 Frame 中表达：

$$
T_{\text{new}}
=
\operatorname{Exp}(\delta\xi)T
$$
与：

$$
T_{\text{new}}
=
T\operatorname{Exp}(\delta\xi)
$$
在非交换群 (SE(3)) 上结果不同。

它们对应不同：

* Error Definition；
* Jacobian；
* Covariance Frame；
* Update Semantics。

如果推导使用右扰动，代码却使用左扰动，优化方向和 Jacobian 会不一致，可能造成收敛错误。

</details>

---

下一章建议进入：

## Chapter 30 — Coordinate Frame Conventions & Transform Debugging

我们会从工程角度集中处理：

* ({}^A T_B) 到底表示什么；
* World-to-Camera 与 Camera-to-World；
* Active 与 Passive；
* 左乘与右乘；
* ROS、OpenCV、相机坐标系的常见轴约定；
* 如何用单位向量和简单点验证外参；
* 如何系统定位“方向反了、轴换了、变换乘反了”的问题。

## 排版修订记录

迁移时将原记录的方括号公式、误解析的等号和矩阵换行恢复为 LaTeX；保留原有推导与例题。迁移不代表全面技术审校。
