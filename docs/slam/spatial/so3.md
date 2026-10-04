---
title: 三维旋转与 SO(3)
description: 三维旋转与 SO(3)的课程笔记。
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 27
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 三维旋转与 SO(3)

## 为什么三维旋转比二维旋转困难得多？

二维旋转只需要一个角度：

$$
\theta
$$
所有旋转都绕垂直于平面的同一根轴完成，因此：

$$
R(\theta_1)R(\theta_2)=R(\theta_2)R(\theta_1)
$$
但进入三维以后，旋转不但要描述：

> 转多少？

还要描述：

> 绕哪一根轴转？

而且不同旋转的执行顺序通常会改变最终结果。

这就是三维姿态表示复杂起来的根本原因。

---

## 1. 三维 Orientation 到底描述什么？

二维 Orientation 描述一根局部 (x) 轴在平面中的方向。

三维 Orientation 则需要描述一个完整的局部坐标系：

* 局部 (x) 轴朝哪里；
* 局部 (y) 轴朝哪里；
* 局部 (z) 轴朝哪里。

因此一个三维旋转矩阵可以写成：

$$
R=
\begin{bmatrix}
|&|&|\\
r_x&r_y&r_z\\
|&|&|
\end{bmatrix}
$$
其中：

* (r_x)：旋转后局部 (x) 轴在参考系中的表达；
* (r_y)：旋转后局部 (y) 轴在参考系中的表达；
* (r_z)：旋转后局部 (z) 轴在参考系中的表达。

所以三维旋转矩阵的本质仍然是：

> **一个坐标系的三根单位轴，在另一个坐标系中的表达。**

---

## 2. 三维旋转矩阵

三维点：

$$
p=
\begin{bmatrix}
x\\y\\z
\end{bmatrix}
$$
旋转后：

$$
p'=Rp
$$
其中：

$$
R\in\mathbb R^{3\times3}
$$
合法三维旋转矩阵满足：

$$
\boxed{
R^TR=I
}
$$
以及：

$$
\boxed{
\det(R)=1
}
$$
因此三维旋转集合定义为：

$$
\boxed{
SO(3)
=
\left\{
R\in\mathbb R^{3\times3}
\mid
R^TR=I,\ \det(R)=1
\right\}
}
$$
和 (SO(2)) 一样：

* (S)：Special；
* (O)：Orthogonal；
* (3)：三维空间。

---

## 3. 为什么 (R^TR=I)？

因为旋转必须保持长度和夹角。

对任意向量 (p)：

$$
|Rp|^2
=
(Rp)^T(Rp)

p^TR^TRp
$$
要使：

$$
|Rp|=|p|
$$
对任意 (p) 成立，就必须：

$$
R^TR=I
$$
这意味着三列向量：

$$
r_x,r_y,r_z
$$
分别满足：

$$
|r_x|=|r_y|=|r_z|=1
$$
并且：

$$
r_x^Tr_y=r_y^Tr_z=r_z^Tr_x=0
$$
也就是三根轴：

* 单位长度；
* 两两垂直。

---

## 4. 为什么还必须要求 (\det(R)=1)？

所有正交矩阵满足：

$$
\det(R)=\pm1
$$
当：

$$
\det(R)=1
$$
表示保持坐标系手性，是纯旋转。

当：

$$
\det(R)=-1
$$
矩阵中包含镜像反射。

例如：

$$
M=
\begin{bmatrix}
1&0&0\\
0&1&0\\
0&0&-1
\end{bmatrix}
$$
保持长度和正交性，但它把 (z) 方向翻转了，是镜像，不属于 (SO(3))。

---

## 5. 绕三个坐标轴的基础旋转

按照右手定则，绕 (x) 轴旋转角度 (\alpha)：

$$
\boxed{
R_x(\alpha)
=
\begin{bmatrix}
1&0&0\\
0&\cos\alpha&-\sin\alpha\\
0&\sin\alpha&\cos\alpha
\end{bmatrix}
}
$$
绕 (y) 轴旋转角度 (\beta)：

$$
\boxed{
R_y(\beta)
=
\begin{bmatrix}
\cos\beta&0&\sin\beta\\
0&1&0\\
-\sin\beta&0&\cos\beta
\end{bmatrix}
}
$$
绕 (z) 轴旋转角度 (\gamma)：

$$
\boxed{
R_z(\gamma)
=
\begin{bmatrix}
\cos\gamma&-\sin\gamma&0\\
\sin\gamma&\cos\gamma&0\\
0&0&1
\end{bmatrix}
}
$$
这些矩阵都满足：

$$
R^TR=I,\qquad\det(R)=1
$$
---

## 6. 三维旋转最大的变化：顺序很重要

考虑两个旋转：

1. 绕 (x) 轴转 (90^\circ)；
2. 绕 (y) 轴转 (90^\circ)。

通常：

$$
\boxed{
R_yR_x\neq R_xR_y
}
$$
也就是说，三维旋转不可交换。

---

## 一个具体向量例子

初始向量：

$$
p=
\begin{bmatrix}
0\\0\\1
\end{bmatrix}
$$
### 先绕 (x) 轴 (90^\circ)，再绕 (y) 轴 (90^\circ)

先进行：

$$
R_x(90^\circ)p
=
\begin{bmatrix}
0\\-1\\0
\end{bmatrix}
$$
再绕 (y)：

$$
R_y(90^\circ)
\begin{bmatrix}
0\\-1\\0
\end{bmatrix}
=
\begin{bmatrix}
0\\-1\\0
\end{bmatrix}
$$
最终：

$$
p_1=
\begin{bmatrix}
0\\-1\\0
\end{bmatrix}
$$
---

### 先绕 (y) 轴，再绕 (x) 轴

先进行：

$$
R_y(90^\circ)p
=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
再绕 (x)：

$$
R_x(90^\circ)
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
最终：

$$
p_2=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
显然：

$$
p_1\neq p_2
$$
所以旋转顺序不能随意交换。

---

## 7. 为什么二维旋转可交换，三维不行？

二维中所有旋转都绕同一根轴：

> 垂直于二维平面的 (z) 轴。

因此只是角度累加：

$$
R(\theta_1)R(\theta_2)=R(\theta_1+\theta_2)
$$
三维中旋转轴可以不同。

第一个旋转不仅改变物体方向，也可能改变后续局部旋转轴在世界中的方向。

所以：

> **第二次旋转作用在哪根轴上，取决于前面的旋转和采用的坐标约定。**

这使 (SO(3)) 成为一个非交换群。

---

## 8. 三维旋转有几个自由度？

旋转矩阵包含：

$$
3\times3=9
$$
个元素。

但三维 Orientation 只有：

$$
\boxed{3\text{ DoF}}
$$
因为三维姿态只需要三个独立量描述。

为什么 9 个元素只剩 3 个自由度？

约束：

$$
R^TR=I
$$
提供 6 个独立约束：

* 三个列向量长度为 1；
* 三组列向量两两正交。

因此：

$$
9-6=3
$$
而 (\det(R)=1) 用于从正交矩阵的两个离散分支中选出纯旋转分支，不再额外减少连续自由度。

---

## 9. 既然只有 3 DoF，为什么还要保存 9 个数？

旋转矩阵存在冗余，但优点明显：

* 没有奇异姿态；
* 可以直接作用于向量；
* 组合直接用矩阵乘法；
* 逆就是转置；
* 几何意义清晰。

缺点是：

* 存储 9 个数；
* 数值计算后可能偏离正交约束；
* 优化时不能把 9 个元素独立更新。

所以实际系统会根据场景使用不同表示：

| 表示              | 参数数量 | 主要特点       |
| --------------- | ---: | ---------- |
| Rotation Matrix |    9 | 稳定直观，但冗余   |
| Euler Angles    |    3 | 易理解，但有奇异性  |
| Axis–Angle      |    3 | 最小局部表示     |
| Quaternion      |    4 | 无万向锁，需单位约束 |
| Lie Algebra     |    3 | 适合局部扰动和优化  |

---

## 10. Euler Angles：用三个角度描述旋转

一个常见想法是连续绕三个轴旋转，例如：

$$
R
=
R_z(\psi)R_y(\theta)R_x(\phi)
$$
通常称为：

* Roll：(\phi)
* Pitch：(\theta)
* Yaw：(\psi)

这类约定常称为 ZYX Euler Angles，或在某些语境下称为 Roll–Pitch–Yaw。

但必须注意：

> Euler Angles 并不是唯一的三角表示。

可能存在：

$$
XYZ,\ XZY,\ ZYX,\ ZXZ,\ldots
$$
不同顺序对应完全不同的含义。

所以看到：

```text
roll = ...
pitch = ...
yaw = ...
```

必须确认：

* 旋转顺序；
* 绕固定轴还是移动轴；
* 主动旋转还是被动坐标变换；
* 角度正方向；
* 左乘还是右乘。

---

## 11. Intrinsic 与 Extrinsic Rotation

这两个概念经常造成混乱。

## Extrinsic Rotation

每次都绕固定的世界坐标轴旋转。

例如：

```text
先绕世界 x
再绕世界 y
再绕世界 z
```

## Intrinsic Rotation

每次绕物体当前的局部坐标轴旋转。

例如：

```text
先绕局部 x
旋转后再绕新的局部 y
再绕新的局部 z
```

一个 Intrinsic 顺序通常可以等价为反序的 Extrinsic 旋转。

例如：

> Intrinsic (XYZ) 与 Extrinsic (ZYX) 可描述相同组合关系。

因此只说“先 Roll，再 Pitch，再 Yaw”往往不够精确。

---

## 12. Euler Angles 的优点

Euler Angles 很适合：

* 人类阅读；
* UI 显示；
* 简单姿态限制；
* 飞行器直观解释；
* 调试日志。

例如：

```text
Roll  = 2°
Pitch = -5°
Yaw   = 90°
```

比九个旋转矩阵元素容易理解得多。

但它有一个根本缺陷：

> **存在奇异性。**

---

## 13. Gimbal Lock（万向锁）

以 ZYX Euler Angles 为例：

$$
R=R_z(\psi)R_y(\theta)R_x(\phi)
$$
当 Pitch：

$$
\theta=\pm90^\circ
$$
时，原本不同的两个旋转轴会重合。

结果是：

> Roll 和 Yaw 不再能被独立区分。

系统从三个独立旋转自由度，在该参数化位置上退化为只能区分两个组合方向。

这叫：

$$
\boxed{\text{Gimbal Lock}}
$$
---

## 14. Gimbal Lock 是否意味着真实物体少了一个自由度？

不是。

真实三维 Orientation 始终有 3 DoF。

发生退化的是：

> Euler Angle 这套坐标参数化。

就像地球经纬度在南北极附近出现问题，并不意味着地球表面少了一个方向。

因此 Gimbal Lock 是：

$$
\boxed{\text{Representation Singularity}}
$$
不是物理旋转本身的奇异性。

---

## 15. 为什么 Gimbal Lock 会影响滤波和优化？

在奇异位置附近：

* 很小的姿态变化可能导致 Euler Angles 巨大跳动；
* 不同角组合可能表示几乎相同 Orientation；
* Jacobian 可能病态；
* Covariance 很难正确解释；
* 插值可能出现奇怪路径。

因此 Euler Angles 通常不适合：

* 长时间积分姿态；
* 三维姿态滤波内部状态；
* 全范围无人机姿态；
* 通用旋转优化。

它们更适合作为：

> 显示层或受限场景参数。

---

## 16. Axis–Angle：绕一根轴转一个角度

Euler Angles 使用三次旋转组合。

Axis–Angle 则基于一个重要事实：

> 任意三维旋转，都可以表示为绕某根单位轴旋转一个角度。

写成：

$$
(\mathbf u,\theta)
$$
其中：

$$
\mathbf u=
\begin{bmatrix}
u_x\u_y\u_z
\end{bmatrix},
\qquad
|\mathbf u|=1
$$
$$
\theta\in[0,\pi]
$$
也常组合成旋转向量：

$$
\boxed{
\boldsymbol\phi=\theta\mathbf u
}
$$
旋转向量的：

* 方向：旋转轴；
* 模长：旋转角。

它只有三个参数，与三维旋转 3 DoF 对应。

---

## 17. Skew-Symmetric Matrix（反对称矩阵）

给定向量：

$$
\mathbf a=
\begin{bmatrix}
a_x\a_y\a_z
\end{bmatrix}
$$
定义 hat 运算：

$$
\boxed{
\mathbf a^\wedge
=
[\mathbf a]_\times

\begin{bmatrix}
0&-a_z&a_y\\
a_z&0&-a_x\\
-a_y&a_x&0
\end{bmatrix}
}
$$
它满足：

$$
\boxed{
\mathbf a^\wedge\mathbf b
=
\mathbf a\times\mathbf b
}
$$
所以反对称矩阵可以把叉乘写成矩阵乘法。

同时：

$$
(\mathbf a^\wedge)^T=-\mathbf a^\wedge
$$
这类矩阵构成 (SO(3)) 对应的 Lie Algebra：

$$
\mathfrak{so}(3)
$$
---

## 18. Rodrigues Formula

给定单位旋转轴 (\mathbf u) 和角度 (\theta)，旋转矩阵为：

$$
\boxed{
R
=
I
+
\sin\theta,\mathbf u^\wedge
+
(1-\cos\theta)(\mathbf u^\wedge)^2
}
$$
这就是 Rodrigues Formula。

也可以用旋转向量：

$$
\boldsymbol\phi=\theta\mathbf u
$$
写成：

$$
R=\exp(\boldsymbol\phi^\wedge)
$$
它是 (SO(2)) 中：

$$
R(\theta)=\exp(\theta J)
$$
向三维的推广。

---

## 19. Rodrigues Formula 的几何理解

任意向量 (p) 可以分解成：

* 平行旋转轴的部分；
* 垂直旋转轴的部分。

平行部分在旋转中不变。

垂直部分在垂直于 (\mathbf u) 的平面中完成二维旋转。

Rodrigues 公式作用于向量时可以写成：

$$
\boxed{
Rp
=
p\cos\theta
+
(\mathbf u\times p)\sin\theta
+
\mathbf u(\mathbf u^Tp)(1-\cos\theta)
}
$$
三项分别表达：

1. 原向量缩放部分；
2. 垂直方向的旋转贡献；
3. 保留轴向分量。

---

## 20. 小角度旋转

当：

$$
|\boldsymbol\phi|\approx0
$$
有：

$$
\sin\theta\approx\theta
$$
$$
1-\cos\theta\approx\frac12\theta^2
$$
一阶近似：

$$
\boxed{
R
\approx
I+\boldsymbol\phi^\wedge
}
$$
因此小旋转作用于向量：

$$
Rp
\approx
p+\boldsymbol\phi^\wedge p
$$
也就是：

$$
Rp
\approx
p+\boldsymbol\phi\times p
$$
这个公式在：

* IMU 姿态更新；
* 视觉 SLAM Jacobian；
* ICP；
* Bundle Adjustment；
* Error-State Kalman Filter；

中极其常见。

---

## 21. 为什么旋转向量不能简单长期累加？

对于非常小的旋转增量：

$$
\delta\phi_1\,\delta\phi_2
$$
可以近似：

$$
R(\delta\phi_1)R(\delta\phi_2)
\approx
R(\delta\phi_1+\delta\phi_2)
$$
但对于较大三维旋转：

$$
\boxed{
\exp(\phi_1^\wedge)\exp(\phi_2^\wedge)
\neq
\exp((\phi_1+\phi_2)^\wedge)
}
$$
因为三维旋转不可交换。

所以旋转向量是很好的：

> 局部增量表示。

但它不是普通的全局线性坐标。

---

## 22. (SO(3)) 的指数映射

Lie Algebra 中的小向量：

$$
\boldsymbol\phi\in\mathbb R^3
$$
通过：

$$
\boxed{
R=\operatorname{Exp}(\boldsymbol\phi)
=
\exp(\boldsymbol\phi^\wedge)
}
$$
映射到：

$$
R\in SO(3)
$$
其中：

$$
\theta=|\boldsymbol\phi|
$$
当 (\theta\neq0)：

$$
\mathbf u=\frac{\boldsymbol\phi}{\theta}
$$
再使用 Rodrigues Formula。

指数映射保证：

> 任意局部旋转向量都会生成一个合法旋转矩阵。

---

## 23. (SO(3)) 的对数映射

给定：

$$
R\in SO(3)
$$
希望恢复旋转向量：

$$
\boldsymbol\phi=\operatorname{Log}(R)
$$
旋转角满足：

$$
\boxed{
\theta
=
\cos^{-1}
\left(
\frac{\operatorname{tr}(R)-1}{2}
\right)
}
$$
因为三维旋转矩阵迹满足：

$$
\operatorname{tr}(R)=1+2\cos\theta
$$
当 (\theta) 不接近 0 或 (\pi) 时：

$$
\boxed{
\boldsymbol\phi^\wedge
=
\frac{\theta}{2\sin\theta}
(R-R^T)
}
$$
然后通过 vee 运算，从反对称矩阵恢复三维向量。

---

## 24. Log Map 有什么用？

假设估计旋转：

$$
\hat R
$$
测量旋转：

$$
R_m
$$
旋转误差不应该写成：

$$
R_m-\hat R
$$
而可以写成相对旋转：

$$
R_{\text{err}}
=
\hat R^TR_m
$$
再映射到局部向量：

$$
\boxed{
e_R
=
\operatorname{Log}
(\hat R^TR_m)
}
$$
得到：

$$
e_R\in\mathbb R^3
$$
这个三维向量可以用于：

* 最小二乘；
* Kalman Innovation；
* 姿态控制；
* Graph Optimization。

它表达：

> 从当前估计姿态旋转到测量姿态，还需要一个多大的局部旋转。

---

## 25. 为什么旋转矩阵优化后会失效？

假设直接把 (R) 的九个元素作为普通变量更新：

$$
R_{\text{new}}=R+\Delta R
$$
一般不会继续满足：

$$
R_{\text{new}}^TR_{\text{new}}=I
$$
因此会混入：

* 缩放；
* 剪切；
* 非正交误差。

更合理的更新方式是：

$$
\boxed{
R_{\text{new}}
=
R\operatorname{Exp}(\delta\phi)
}
$$
或者左乘：

$$
R_{\text{new}}
=
\operatorname{Exp}(\delta\phi)R
$$
这样无论 (\delta\phi) 是什么，更新后的结果始终属于 (SO(3))。

---

## 26. 左扰动和右扰动

右扰动：

$$
\boxed{
R_{\text{new}}
=
R\operatorname{Exp}(\delta\phi)
}
$$
通常表示 (\delta\phi) 在当前局部坐标系中表达。

左扰动：

$$
\boxed{
R_{\text{new}}
=
\operatorname{Exp}(\delta\phi)R
}
$$
通常表示 (\delta\phi) 在外部参考坐标系中表达。

因为 (SO(3)) 不可交换，两者不等价。

这会直接影响：

* Jacobian；
* Error Definition；
* Covariance Frame；
* EKF 状态误差定义。

---

## 27. Rotation Matrix 的数值漂移

理论上：

$$
R^TR=I
$$
但连续积分和浮点计算后，可能出现：

$$
R^TR\neq I
$$
常见修正方法包括：

## 方法一：SVD 投影

对近似矩阵：

$$
\tilde R=U\Sigma V^T
$$
令：

$$
R=UV^T
$$
必要时修正行列式符号。

## 方法二：通过 Lie Group 增量更新

每次使用：

$$
R\leftarrow R\operatorname{Exp}(\delta\phi)
$$
## 方法三：使用单位四元数并周期归一化

下一章会详细讨论。

---

## 28. 三维旋转的拓扑特点

二维旋转：

$$
SO(2)\cong S^1
$$
本质上是一个圆。

三维旋转空间 (SO(3)) 更复杂。

一个重要现象是：

> 绕轴 (\mathbf u) 转 (\theta)，与绕轴 (-\mathbf u) 转 (-\theta) 表示同一个旋转。

即：

$$
(\mathbf u,\theta)
\sim
(-\mathbf u,-\theta)
$$
当角度为 (\pi) 时：

$$
(\mathbf u,\pi)
$$
和：

$$
(-\mathbf u,\pi)
$$
也是同一个旋转。

这会导致 Axis–Angle 和 Log Map 在接近 (180^\circ) 时存在表示歧义与数值困难。

---

## 29. 不同旋转表示的比较

| 表示              | 参数数 | 奇异性         | 约束   | 适合场景    |
| --------------- | --: | ----------- | ---- | ------- |
| Rotation Matrix |   9 | 无参数奇异       | 正交约束 | 变换、组合   |
| Euler Angles    |   3 | 有万向锁        | 角度约定 | 显示、受限姿态 |
| Axis–Angle      |   3 | (\pi) 附近有歧义 | 角度范围 | 局部误差、优化 |
| Quaternion      |   4 | 无万向锁        | 单位长度 | 插值、积分   |
| Lie Algebra     |   3 | 局部表示        | 局部有效 | 优化、滤波   |

没有一种表示在所有场景下都最好。

成熟系统经常同时使用多种表示：

```text
内部存储：
Rotation Matrix / Quaternion

局部优化：
Rotation Vector / Lie Algebra

用户显示：
Euler Angles
```

---

## 30. 与 IMU 姿态积分的关系

Gyroscope 测量角速度：

$$
\omega=
\begin{bmatrix}
\omega_x\\
\omega_y\\
\omega_z
\end{bmatrix}
$$
在短时间：

$$
\Delta t
$$
内，旋转增量近似：

$$
\delta\phi=\omega\Delta t
$$
姿态可更新为：

$$
\boxed{
R_{t+\Delta t}
=
R_t
\operatorname{Exp}
((\omega\Delta t)^\wedge)
}
$$
这比简单把：

$$
roll,\ pitch,\ yaw
$$
分别加上角速度积分更符合三维旋转结构。

但陀螺仪存在 Bias 和 Noise，连续积分仍然会漂移，需要其他 Observation 修正。

---

## 本章核心总结

第一：

$$
SO(3)
=
{R\in\mathbb R^{3\times3}\mid R^TR=I,\det R=1}
$$
表示全部三维纯旋转。

第二：

> 三维旋转通常不可交换，旋转顺序会改变最终结果。

第三：

> Euler Angles 容易理解，但存在 Gimbal Lock，且必须明确旋转顺序和坐标约定。

第四：

> 任意三维旋转可以表示为绕某单位轴旋转一个角度。

第五：

$$
R
=
\exp(\phi^\wedge)
$$
将三维局部旋转向量映射成合法旋转矩阵。

第六：

> 旋转矩阵属于流形，不能把九个元素作为独立普通变量随意更新。

---

## 思考题与参考答案

## 思考题 1

为什么三维旋转不可交换？

<details>

<summary>参考答案</summary>
因为不同旋转可能绕不同轴执行。

第一个旋转会改变物体姿态，也可能改变后续局部旋转轴在参考系中的方向。因此：

$$
R_1R_2
$$
和：

$$
R_2R_1
$$
通常对应不同的空间运动，最终结果不同。

</details>

---

## 思考题 2

Gimbal Lock 是否说明三维旋转在某些姿态下只有两个自由度？

<details>

<summary>参考答案</summary>
不是。

真实三维旋转始终有 3 DoF。

Gimbal Lock 是 Euler Angle 参数化的奇异性：在特定姿态下，两个参数轴重合，使不同参数变化无法被独立区分。

问题出在表示方式，而不是物理 Orientation。

</details>

---

## 思考题 3

为什么一个 (3\times3) 旋转矩阵只有 3 DoF？

<details>

<summary>参考答案</summary>
矩阵有 9 个元素，但正交条件：

$$
R^TR=I
$$
提供 6 个独立连续约束：

* 三个单位长度约束；
* 三个两两正交约束。

因此：

$$
9-6=3
$$
行列式为 (+1) 用来排除镜像分支。

</details>

---

## 思考题 4

为什么用：

$$
R_{\text{new}}=R+\Delta R
$$
更新旋转通常不合理？

<details>

<summary>参考答案</summary>
普通矩阵加法不会保持：

$$
R^TR=I,\qquad\det(R)=1
$$
更新后的矩阵可能包含缩放或剪切，不再是合法旋转。

更合理的是：

$$
R_{\text{new}}
=
R\operatorname{Exp}(\delta\phi)
$$
通过群上的乘法更新，使结果始终属于 (SO(3))。

</details>

---

## 思考题 5

为什么远离奇异点时可以使用三维旋转向量作为局部误差，但不适合无条件地把两个大旋转向量直接相加？

<details>

<summary>参考答案</summary>
旋转向量是 (SO(3)) 单位元附近 Lie Algebra 的局部坐标。

对于小旋转：

$$
\operatorname{Exp}(\delta\phi_1)
\operatorname{Exp}(\delta\phi_2)
\approx
\operatorname{Exp}(\delta\phi_1+\delta\phi_2)
$$
但大旋转中，非交换性和高阶项不可忽略，因此：

$$
\operatorname{Exp}(\phi_1)
\operatorname{Exp}(\phi_2)
\neq
\operatorname{Exp}(\phi_1+\phi_2)
$$
通常必须通过旋转乘法进行组合。

</details>

---

## 思考题 6

一个向量绕单位轴：

$$
u=
\begin{bmatrix}
0\\0\\1
\end{bmatrix}
$$
旋转 (90^\circ)。向量：

$$
p=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
旋转后是什么？

<details>

<summary>参考答案</summary>
这是绕 (z) 轴逆时针旋转 (90^\circ)：

$$
R_z(90^\circ)
=
\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}
$$
因此：

$$
Rp
=
\begin{bmatrix}
0\\1\\0
\end{bmatrix}
$$

</details>

---

下一章：

## Chapter 28 — Quaternion：为什么用四个数表示只有三个自由度的旋转？

将重点讨论：

* Quaternion 的组成与几何意义；
* 单位四元数如何表示旋转；
* 四元数乘法为什么对应旋转组合；
* 为什么 (q) 和 (-q) 表示同一个姿态；
* 四元数如何旋转向量；
* Quaternion 与 Axis–Angle 的转换；
* SLERP；
* 为什么四元数没有 Gimbal Lock，但仍然不是“完全没有坑”。

## 排版修订记录

迁移时将原记录的方括号公式、误解析的等号和矩阵换行恢复为 LaTeX；保留原有推导与例题。迁移不代表全面技术审校。
