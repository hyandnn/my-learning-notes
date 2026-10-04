---
title: 二维位姿与 SE(2)
description: 二维位姿与 SE(2)的课程笔记。
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 26
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 二维位姿与 SE(2)

上一章我们只讨论二维旋转：

$$
R\in SO(2)
$$
但机器人除了方向，还有位置。

因此二维 Pose 同时包含：

* Translation；
* Rotation。

最常见的参数写法是：

$$
\mathbf{x}
=
\begin{bmatrix}
x\\
y\\
\theta
\end{bmatrix}
$$
但这一章最重要的结论是：

> **([x,y,\theta]) 只是二维 Pose 的一种参数表达，Pose 本身并不是普通三维向量。**

---

## 1. 什么是 (SE(2))？

二维刚体变换写成齐次矩阵：

$$
\boxed{
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
}
$$
其中：

$$
R\in SO(2)
$$
$$
t=
\begin{bmatrix}
x\\y
\end{bmatrix}
\in\mathbb R^2
$$
展开：

$$
T(x,y,\theta)
=
\begin{bmatrix}
\cos\theta&-\sin\theta&x\\
\sin\theta&\cos\theta&y\\
0&0&1
\end{bmatrix}
$$
所有这样的二维刚体变换构成：

$$
\boxed{
SE(2)
=
\left\{
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
\middle|
R\in SO(2),\ t\in\mathbb R^2
\right\}
}
$$
其中：

* (S)：Special；
* (E)：Euclidean；
* (2)：二维空间。

可以把 (SE(2)) 理解为：

> **所有二维坐标系之间合法刚体变换的集合。**

---

## 2. 为什么叫 Euclidean Group？

刚体变换保持：

* 点之间的距离；
* 向量夹角；
* 物体形状。

如果：

$$
p_i'=Rp_i+t
$$
$$
p_j'=Rp_j+t
$$
那么：

$$
p_i'-p_j'
=
R(p_i-p_j)
$$
因此：

$$
|p_i'-p_j'|
=
|R(p_i-p_j)|
=
|p_i-p_j|
$$
所以 (SE(2)) 描述的是：

> 欧氏平面上不会导致形变的旋转和平移。

---

## 3. Pose 参数和 Pose 变换不是同一个东西

参数：

$$
\mathbf{x}
=
\begin{bmatrix}
x\\y\\\theta
\end{bmatrix}
$$
只是三个数。

真正的变换对象是：

$$
T(\mathbf{x})
=
\begin{bmatrix}
R(\theta)&t\\
0&1
\end{bmatrix}
$$
为什么要区分？

因为参数向量可以普通相加：

$$
\mathbf{x}_1+\mathbf{x}_2
$$
但这通常不等于两个 Pose 的真实组合。

例如：

$$
\mathbf{x}_1=
\begin{bmatrix}
1\\0\\90^\circ
\end{bmatrix}
$$
$$
\mathbf{x}_2=
\begin{bmatrix}
1\\0\\0^\circ
\end{bmatrix}
$$
逐元素相加得到：

$$
\begin{bmatrix}
2\\0\\90^\circ
\end{bmatrix}
$$
但如果第二个“前进 1 米”是在第一个 Pose 的机器人局部坐标系中执行，真实结果不是 ((2,0))，而是 ((1,1))。

所以：

$$
\boxed{
\text{Pose composition}
\neq
\text{parameter vector addition}
}
$$
---

## 4. Pose Composition

假设：

$$
{}^A T_B
=
\begin{bmatrix}
{}^A R_B&{}^A t_B\\
0&1
\end{bmatrix}
$$
$$
{}^B T_C
=
\begin{bmatrix}
{}^B R_C&{}^B t_C\\
0&1
\end{bmatrix}
$$
那么：

$$
{}^A T_C
=
{}^A T_B\,{}^B T_C
$$
展开：

$$
\begin{bmatrix}
R_{AB}&t_{AB}\\
0&1
\end{bmatrix}
\begin{bmatrix}
R_{BC}&t_{BC}\\
0&1
\end{bmatrix}
$$
得到：

$$
\boxed{
R_{AC}=R_{AB}R_{BC}
}
$$
$$
\boxed{
t_{AC}=t_{AB}+R_{AB}t_{BC}
}
$$
第二个公式非常重要：

$$
t_{AC}=t_{AB}+R_{AB}t_{BC}
$$
为什么不是：

$$
t_{AB}+t_{BC}
$$
因为：

$$
t_{BC}
$$
是在 (B) 坐标系中表达的，必须先通过：

$$
R_{AB}
$$
转成 (A) 坐标系表达，才能与 (t_{AB}) 相加。

---

## 5. 一个具体例子

机器人初始 Pose：

$$
T_1=
T(1,0,90^\circ)
$$
表示：

* 世界坐标位置为 ((1,0))；
* 朝向世界 (y) 轴。

机器人随后在自己的局部坐标系中前进 1 米：

$$
T_{\Delta}
=
T(1,0,0)
$$
总 Pose：

$$
T_2=T_1T_\Delta
$$
平移部分：

$$
t_2
=
t_1+R(90^\circ)
\begin{bmatrix}
1\\0
\end{bmatrix}
$$
因为：

$$
R(90^\circ)
\begin{bmatrix}
1\\0
\end{bmatrix}
=
\begin{bmatrix}
0\\1
\end{bmatrix}
$$
所以：

$$
t_2=
\begin{bmatrix}
1\\0
\end{bmatrix}
+
\begin{bmatrix}
0\\1
\end{bmatrix}
=
\begin{bmatrix}
1\\1
\end{bmatrix}
$$
最终 Pose：

$$
\boxed{
(1,1,90^\circ)
}
$$
这再次说明：

> 局部位移的效果取决于当前 Orientation。

---

## 6. (SE(2)) 为什么不是交换群？

考虑两个操作。

操作 A：

```text
向前移动 1 米
```

操作 B：

```text
左转 90°
```

## 先移动，再旋转

从原点朝 (x) 正方向：

```text
先到 (1,0)
再原地旋转到 90°
```

结果：

$$
(1,0,90^\circ)
$$
## 先旋转，再移动

```text
先朝向 y 正方向
再沿局部前方移动 1 米
```

结果：

$$
(0,1,90^\circ)
$$
两者不同。

因此：

$$
T_{\text{rotate}}T_{\text{translate}}
\neq
T_{\text{translate}}T_{\text{rotate}}
$$
所以：

$$
\boxed{
SE(2)\text{ generally is non-commutative}
}
$$
虽然二维纯旋转 (SO(2)) 可交换，但加入平移后，(SE(2)) 通常不可交换。

---

## 7. Pose 的逆

已知：

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$
逆变换：

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
它的物理意义是：

> 已知坐标系 (B) 在 (A) 中的 Pose，求坐标系 (A) 在 (B) 中的 Pose。

如果：

$$
{}^A T_B
$$
把 (B) 系点转到 (A) 系：

$$
{}^A p={}^A T_B\,{}^B p
$$
那么：

$$
{}^B p
=
({}^A T_B)^{-1}{}^A p
$$
---

## 8. 参数形式下如何求逆？

假设 Pose：

$$
(x,y,\theta)
$$
那么逆 Pose 的角度：

$$
\theta^{-1}=-\theta
$$
但平移不是简单：

$$
(-x,-y)
$$
而是：

$$
t^{-1}=-R(\theta)^Tt
$$
展开：

$$
\boxed{
x^{-1}
=
-\cos\theta,x
-\sin\theta,y
}
$$
$$
\boxed{
y^{-1}
=
\sin\theta,x
-\cos\theta,y
}
$$
$$
\boxed{
\theta^{-1}=-\theta
}
$$
这也说明 ([x,y,\theta]) 不是普通向量：普通向量的逆通常只是整体取负，但 Pose 不是。

---

## 9. Relative Pose

这是 SLAM 和定位中最常见的操作之一。

假设已知两个绝对 Pose：

$$
{}^W T_A
$$
$$
{}^W T_B
$$
想求：

> (B) 相对于 (A) 的 Pose。

答案：

$$
\boxed{
{}^A T_B
=
({}^W T_A)^{-1}
{}^W T_B
}
$$
为什么？

因为变换链是：

```text
B → W → A
```

从 (B) 到世界：

$$
{}^W T_B
$$
从世界到 (A)：

$$
{}^A T_W
=
({}^W T_A)^{-1}
$$
所以：

$$
{}^A T_B
=
{}^A T_W\,{}^W T_B
$$
即：

$$
({}^W T_A)^{-1}{}^W T_B
$$
---

## 10. Relative Pose 的参数展开

假设：

$$
T_A=(x_A,y_A,\theta_A)
$$
$$
T_B=(x_B,y_B,\theta_B)
$$
先计算世界系位置差：

$$
\Delta t_W
=
\begin{bmatrix}
x_B-x_A\\
y_B-y_A
\end{bmatrix}
$$
但这个差仍在 World Frame 中。

要表达为 (A) Frame：

$$
\Delta t_A
=
R(\theta_A)^T\Delta t_W
$$
所以：

$$
\boxed{
{}^A t_B
=
R(\theta_A)^T
(t_B-t_A)
}
$$
角度差：

$$
\boxed{
{}^A\theta_B
=
\operatorname{wrapToPi}(\theta_B-\theta_A)
}
$$
因此 Relative Pose 不是简单的：

$$
[x_B-x_A,\ y_B-y_A,\ \theta_B-\theta_A]
$$
平移部分还必须旋转到参考坐标系中。

---

## 11. 一个 Relative Pose 例子

Pose A：

$$
T_A=(1,1,90^\circ)
$$
Pose B：

$$
T_B=(1,3,90^\circ)
$$
世界系位置差：

$$
t_B-t_A
=
\begin{bmatrix}
0\\2
\end{bmatrix}
$$
A 朝向 (90^\circ)，所以：

$$
R_A^T
=
R(-90^\circ)
$$
于是：

$$
{}^A t_B
=
R(-90^\circ)
\begin{bmatrix}
0\\2
\end{bmatrix}
=
\begin{bmatrix}
2\\0
\end{bmatrix}
$$
角度差：

$$
0^\circ
$$
所以：

$$
\boxed{
{}^A T_B=(2,0,0^\circ)
}
$$
也就是说：

> 从 A 的局部视角看，B 在正前方 2 米。

这比世界坐标差 ((0,2)) 更符合机器人局部运动语义。

---

## 12. Odometry 为什么通常给 Relative Pose？

轮式里程计更自然地告诉系统：

$$
{}^{R_{t-1}}T_{R_t}
$$
即：

> 当前 Robot Frame 相对于上一时刻 Robot Frame 的相对运动。

例如：

```text
前进 10 cm
旋转 2°
```

它通常不会直接可靠地告诉你：

$$
{}^W T_{R_t}
$$
绝对 Pose 需要通过递推组合：

$$
{}^W T_{R_t}
=
{}^W T_{R_{t-1}}
{}^{R_{t-1}}T_{R_t}
$$
连续相乘后，误差会累积。

这正是 Odometry Drift 的来源之一。

---

## 13. 为什么连续 Pose Composition 会积累误差？

假设每次相对变换：

$$
\hat T_k
=
T_k\Delta T_k
$$
其中 (\Delta T_k) 是小误差。

全局 Pose：

$$
\hat T_{0:n}
=
\hat T_1\hat T_2\cdots\hat T_n
$$
误差并不是简单地只加在位置上。

旋转误差会改变后续所有平移的方向。

例如很小的朝向误差：

$$
\delta\theta
$$
如果随后前进很远，会产生越来越大的横向位置偏差。

所以在 Pose 链中：

> Orientation Error 会通过 Composition 不断污染 Translation。

这和 Part II 中 Jacobian 传播协方差的思想完全一致。

---

## 14. Pose Difference 和 Pose Error

假设 Estimate：

$$
\hat T
$$
Truth 或 Measurement：

$$
T
$$
不能简单写：

$$
T-\hat T
$$
因为 (T) 是群元素，不是普通向量。

更合理的是构造相对误差：

$$
\boxed{
T_{\text{err}}
=
\hat T^{-1}T
}
$$
它表示：

> 从当前 Estimate 走到目标 Pose，还需要什么变换？

然后再把这个小变换映射成局部向量：

$$
\delta\xi
=
\log(T_{\text{err}})
$$
其中 (\log) 是后续会讲的 Lie Logarithm。

这就是现代 Pose Optimization 中常用的误差定义。

---

## 15. 为什么不能直接优化 ([x,y,\theta])？

在二维中，直接使用：

$$
[x,y,\theta]
$$
做小规模优化通常也能工作。

但它存在几个概念风险：

## ① 角度周期性

$$
179^\circ
$$
与：

$$
-179^\circ
$$
差值不能普通计算。

## ② 更新语义不明确

加入：

$$
\delta x\,\delta y
$$
到底是在 World Frame 中加，还是 Robot Local Frame 中加？

两者不一样。

## ③ Composition 非线性

Pose 的真实组合不是逐元素加法。

因此更严格的做法是：

> 在 Pose Manifold 上保存状态，在局部切空间中计算小增量。

---

## 16. (SE(2)) 的自由度

齐次矩阵：

$$
T=
\begin{bmatrix}
r_{11}&r_{12}&t_x\\
r_{21}&r_{22}&t_y\\
0&0&1
\end{bmatrix}
$$
有多个矩阵元素，但二维刚体 Pose 只有：

$$
\boxed{3\text{ DoF}}
$$
分别是：

* (x)；
* (y)；
* (\theta)。

所以我们希望找到一个三维局部变量来描述小 Pose 扰动：

$$
\boxed{
\xi=
\begin{bmatrix}
\rho_x\\
\rho_y\\
\phi
\end{bmatrix}
}
$$
其中：

* (\rho_x,\rho_y)：局部平移扰动；
* (\phi)：旋转扰动。

这个空间叫：

$$
\mathfrak{se}(2)
$$
也就是 (SE(2)) 对应的 Lie Algebra。

---

## 17. (se(2)) 的矩阵形式

局部增量向量：

$$
\xi=
\begin{bmatrix}
\rho_x\\
\rho_y\\
\phi
\end{bmatrix}
$$
可以通过 hat 运算写成矩阵：

$$
\boxed{
\xi^\wedge
=
\begin{bmatrix}
0&-\phi&\rho_x\\
\phi&0&\rho_y\\
0&0&0
\end{bmatrix}
}
$$
这不是一个完整刚体变换，而是：

> (SE(2)) 单位元附近的瞬时运动方向。

可以把它理解为：

* 小平移；
* 小旋转；
* 局部速度或扰动。

---

## 18. 指数映射

通过矩阵指数：

$$
\boxed{
T=\exp(\xi^\wedge)
}
$$
可以把局部向量：

$$
\xi\in\mathbb R^3
$$
映射成一个合法的：

$$
T\in SE(2)
$$
当旋转 (\phi) 很小时：

$$
\exp(\xi^\wedge)
\approx
I+\xi^\wedge
$$
于是：

$$
T
\approx
\begin{bmatrix}
1&-\phi&\rho_x\\
\phi&1&\rho_y\\
0&0&1
\end{bmatrix}
$$
这就是小扰动模型。

---

## 19. (SE(2)) 的精确指数映射

对于：

$$
\xi=
\begin{bmatrix}
\rho\\
\phi
\end{bmatrix}
$$
其中：

$$
\rho=
\begin{bmatrix}
\rho_x\\\rho_y
\end{bmatrix}
$$
指数映射结果：

$$
\boxed{
\exp(\xi^\wedge)
=
\begin{bmatrix}
R(\phi)&V(\phi)\rho\\
0&1
\end{bmatrix}
}
$$
其中：

$$
V(\phi)
=
\frac{\sin\phi}{\phi}I
+
\frac{1-\cos\phi}{\phi}
\begin{bmatrix}
0&-1\\
1&0
\end{bmatrix}
$$
当：

$$
\phi\rightarrow0
$$
时：

$$
V(\phi)\rightarrow I
$$
所以平移近似就是 (\rho)。

这里的 (V(\phi)) 表明：

> 当平移和旋转同时发生时，最终 Translation 并不只是简单的 (\rho)，旋转过程也会影响平移轨迹。

---

## 20. 为什么指数映射中的平移不是直接 (\rho)？

设机器人在一段时间内同时：

* 向前移动；
* 持续旋转。

它走出的轨迹通常是一段圆弧，而不是：

```text
先直线移动
再原地旋转
```

因此局部运动向量中的平移速度经过一段旋转积分后，最终位置变化会由：

$$
V(\phi)\rho
$$
决定。

这正是指数映射将“瞬时运动”整合成“有限 Pose 变换”的过程。

---

## 21. 左扰动和右扰动

假设当前 Pose：

$$
T
$$
有一个小增量：

$$
\delta T=\exp(\delta\xi^\wedge)
$$
有两种更新方式。

## 左扰动

$$
\boxed{
T_{\text{new}}
=
\delta T,T
}
$$
通常可以理解为：

> 在全局或参考坐标系侧施加扰动。

## 右扰动

$$
\boxed{
T_{\text{new}}
=
T\,\delta T
}
$$
通常可以理解为：

> 在机器人自身局部坐标系侧施加扰动。

两者一般不相同，因为：

$$
SE(2)
$$
不可交换。

---

## 22. 左右扰动的直觉区别

假设机器人朝向 (90^\circ)。

右扰动中加入：

$$
\delta\rho=
\begin{bmatrix}
1\\0
\end{bmatrix}
$$
表示：

> 沿机器人局部 (x) 轴前进 1 米。

因此世界中向上移动。

左扰动中加入同样数值：

$$
\begin{bmatrix}
1\\0
\end{bmatrix}
$$
通常表示：

> 沿世界或外部参考系 (x) 轴移动 1 米。

因此世界中向右移动。

所以：

> 相同的增量数字，在左扰动和右扰动中可以具有不同坐标语义。

后面做 Pose Jacobian 和 Graph Optimization 时必须保持统一。

---

## 23. Adjoint 的初步概念

同一个局部扰动，在不同坐标系中表达会不同。

如果：

$$
\delta\xi_B
$$
是在 (B) Frame 中表达的扰动，希望转换成 (A) Frame 表达：

$$
\delta\xi_A
=
\operatorname{Ad}_T
\delta\xi_B
$$
其中：

$$
\operatorname{Ad}_T
$$
叫 Adjoint Matrix。

对于：

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$
二维 (SE(2)) 的一种常见 Adjoint 形式为：

$$
\boxed{
\operatorname{Ad}_T
=
\begin{bmatrix}
R&Jt\\
0&1
\end{bmatrix}
}
$$
其中：

$$
J=
\begin{bmatrix}
0&-1\\
1&0
\end{bmatrix}
$$
具体符号形式可能随扰动定义约定略有变化，但核心意义是：

> **Adjoint 负责把 Pose 的局部速度、误差或协方差从一个 Frame 转换到另一个 Frame。**

---

## 24. Pose Covariance 不能随便搬坐标系

假设局部 Pose Error：

$$
\delta\xi_B
$$
协方差：

$$
P_B
$$
转换到 (A) Frame：

$$
\delta\xi_A
=
\operatorname{Ad}_T\delta\xi_B
$$
那么协方差应传播为：

$$
\boxed{
P_A
=
\operatorname{Ad}_T
P_B
\operatorname{Ad}_T^T
}
$$
不能只是把位置方差和角度方差原样复制过去。

因为当坐标系原点发生变化时：

> Orientation Error 可能转化为 Translation Error。

这和 Position–Velocity Filter 里的交叉协方差非常相似。

---

## 25. 一个物理例子

假设机器人朝向存在一个小误差：

$$
\delta\theta
$$
如果我们在机器人中心讨论位置误差，影响可能不大。

但如果讨论机器人前方 2 米处 Sensor 的位置：

$$
p_s=
\begin{bmatrix}
2\\0
\end{bmatrix}
$$
小角度误差会造成约：

$$
\delta y\approx2\delta\theta
$$
的横向位置误差。

所以：

> 同一个 Orientation Uncertainty，在离旋转中心越远的点上，会产生越大的 Position Uncertainty。

Adjoint 和 Pose Jacobian 正是在数学上表达这种耦合。

---

## 26. (SE(2)) 在 SLAM 中扮演什么角色？

在二维 SLAM 中，每一个机器人 Pose 通常都是：

$$
T_i\in SE(2)
$$
Odometry Constraint：

$$
Z_{ij}
$$
表示：

> 从 Pose (i) 到 Pose (j) 的测量相对变换。

预测相对 Pose：

$$
\hat Z_{ij}
=
T_i^{-1}T_j
$$
Pose Graph Error 常写成：

$$
\boxed{
e_{ij}
=
\log
\left(
Z_{ij}^{-1}
T_i^{-1}T_j
\right)
}
$$
解释：

1. (T_i^{-1}T_j)：当前状态预测的相对 Pose；
2. (Z_{ij}^{-1})：与测量比较；
3. 得到一个误差变换；
4. 用 (\log) 映射到三维局部向量；
5. 在切空间中最小化误差。

这就是后面 Graph SLAM 的基本结构。

---

## 27. 为什么误差要写成变换组合？

普通变量：

$$
e=x_{\text{pred}}-x_{\text{obs}}
$$
Pose 不属于普通线性空间。

所以 Pose Error 更自然地表示成：

$$
T_{\text{err}}
=
T_{\text{obs}}^{-1}
T_{\text{pred}}
$$
它回答：

> 从测量 Pose 走到预测 Pose，需要什么相对变换？

再通过：

$$
\log(T_{\text{err}})
$$
变成一个可以用于最小二乘的小向量。

这就是：

> 在 Manifold 上定义状态，在 Tangent Space 中计算误差。

---

## 本章核心总结

第一：

$$
SE(2)
=
\left\{
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
\right\}
$$
表示所有二维刚体 Pose。

第二：

Pose Composition：

$$
T_{AC}=T_{AB}T_{BC}
$$
展开：

$$
R_{AC}=R_{AB}R_{BC}
$$
$$
t_{AC}=t_{AB}+R_{AB}t_{BC}
$$
第三：

$$
SE(2)
$$
通常不可交换，因此 Pose 不能简单逐元素相加。

第四：

Relative Pose：

$$
{}^A T_B
=
({}^W T_A)^{-1}
{}^W T_B
$$
第五：

Pose Error 应通过相对变换定义，而不是直接做矩阵减法。

第六：

$$
\mathfrak{se}(2)
$$
提供了一个局部三维向量空间，用来表达小 Pose 扰动和优化增量。

---

## 思考题与参考答案

## 思考题 1

机器人当前 Pose：

$$
T_1=(2,1,90^\circ)
$$
随后在自己的局部坐标系中前进 2 米，不旋转。新 Pose 是什么？

<details>

<summary>参考答案</summary>
局部位移：

$$
t_\Delta=
\begin{bmatrix}
2\\0
\end{bmatrix}
$$
当前旋转：

$$
R(90^\circ)
$$
将局部位移转到世界系：

$$
R(90^\circ)
\begin{bmatrix}
2\\0
\end{bmatrix}
=
\begin{bmatrix}
0\\2
\end{bmatrix}
$$
因此：

$$
t_{\text{new}}
=
\begin{bmatrix}
2\\1
\end{bmatrix}
+
\begin{bmatrix}
0\\2
\end{bmatrix}
=
\begin{bmatrix}
2\\3
\end{bmatrix}
$$
角度不变：

$$
\boxed{
T_{\text{new}}=(2,3,90^\circ)
}
$$

</details>

---

## 思考题 2

为什么：

$$
T_A^{-1}T_B
$$
表示 (B) 相对于 (A) 的 Pose？

<details>

<summary>参考答案</summary>
$$
T_B
$$
将 (B) Frame 中的坐标转到公共参考系。

$$
T_A^{-1}
$$
再将公共参考系坐标转到 (A) Frame。

所以组合完成：

```text
B Frame → Common Frame → A Frame
```

因此得到：

$$
{}^A T_B=T_A^{-1}T_B
$$

</details>

---

## 思考题 3

为什么以下更新一般不正确？

$$
\begin{bmatrix}
x\\y\\\theta
\end{bmatrix}_{new}
=
\begin{bmatrix}
x\\y\\\theta
\end{bmatrix}
+
\begin{bmatrix}
\Delta x\\\Delta y\\\Delta\theta
\end{bmatrix}
$$
<details>

<summary>参考答案</summary>
因为没有说明：

* (\Delta x,\Delta y) 在 World Frame 还是 Local Frame；
* 角度需要周期归一化；
* Rotation 和 Translation 存在耦合；
* Pose Composition 不是普通向量加法。

如果增量定义在局部坐标系，应使用：

$$
T_{\text{new}}
=
T\exp(\delta\xi^\wedge)
$$
如果定义在全局参考系，则可能使用左乘更新。

</details>

---

## 思考题 4

为什么 (SE(2)) 不可交换，但 (SO(2)) 可交换？

<details>

<summary>参考答案</summary>
二维纯旋转满足：

$$
R(\theta_1)R(\theta_2)
=
R(\theta_1+\theta_2)

R(\theta_2+\theta_1)
$$
因此 (SO(2)) 可交换。

但 (SE(2)) 中平移会受到前面 Rotation 的作用：

$$
t_{12}=t_1+R_1t_2
$$
交换顺序后：

$$
t_{21}=t_2+R_2t_1
$$
通常：

$$
t_{12}\neq t_{21}
$$
因此 (SE(2)) 不可交换。

</details>

---

## 思考题 5

为什么机器人局部前进 1 米和世界坐标 (x) 增加 1 米不是同一件事？

<details>

<summary>参考答案</summary>
机器人局部前进方向由当前 Orientation 决定。

局部位移：

$$
\begin{bmatrix}
1\\0
\end{bmatrix}
$$
转换到世界系为：

$$
R(\theta)
\begin{bmatrix}
1\\0
\end{bmatrix}
=
\begin{bmatrix}
\cos\theta\\
\sin\theta
\end{bmatrix}
$$
只有当：

$$
\theta=0
$$
时，它才等于世界 (x) 方向增加 1 米。

</details>

---

下一章：

## Chapter 27 — 3D Rotation：为什么三维旋转比二维旋转困难得多？

我们会进入：

* 三维 Rotation Matrix；
* (SO(3))；
* 三维旋转不可交换；
* Euler Angles；
* Gimbal Lock；
* Axis–Angle；
* Rodrigues Formula；
* 为什么三维旋转只有 3 DoF，却常用 9 个矩阵元素或 4 个四元数表示。

## 排版修订记录

迁移时将原记录的方括号公式、误解析的等号和矩阵换行恢复为 LaTeX；保留原有推导与例题。迁移不代表全面技术审校。
