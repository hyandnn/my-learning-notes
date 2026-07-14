# Part III · Chapter 25

# 2D Rotation 与 (SO(2))

## 为什么旋转不能简单地当成普通向量？

上一章我们已经知道，一个二维 Pose 可以写成：

[
T=
\begin{bmatrix}
R&t\
0&1
\end{bmatrix}
]

其中 (R) 表示 Orientation。

这一章只讨论旋转，不考虑平移。

核心问题是：

> **什么样的矩阵才是合法旋转？旋转为什么具有自己特殊的数学结构？**

---

# 1. 从二维旋转矩阵开始

二维向量：

[
p=
\begin{bmatrix}
x\
y
\end{bmatrix}
]

绕原点逆时针旋转 (\theta) 后：

[
p'=R(\theta)p
]

其中：

[
\boxed{
R(\theta)
=========

\begin{bmatrix}
\cos\theta&-\sin\theta\
\sin\theta&\cos\theta
\end{bmatrix}
}
]

例如：

[
\theta=90^\circ
]

则：

[
R=
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
]

将：

[
p=
\begin{bmatrix}
1\0
\end{bmatrix}
]

旋转后：

[
p'
==

\begin{bmatrix}
0\1
\end{bmatrix}
]

---

# 2. 旋转矩阵的列到底是什么？

观察：

[
R(\theta)
=========

\begin{bmatrix}
\cos\theta&-\sin\theta\
\sin\theta&\cos\theta
\end{bmatrix}
]

第一列：

[
\begin{bmatrix}
\cos\theta\
\sin\theta
\end{bmatrix}
]

表示：

> 旋转后的 (x) 轴在原坐标系中的方向。

第二列：

[
\begin{bmatrix}
-\sin\theta\
\cos\theta
\end{bmatrix}
]

表示：

> 旋转后的 (y) 轴在原坐标系中的方向。

所以旋转矩阵不是一张抽象数字表。

它的列向量就是：

> 新坐标系的基向量，在旧坐标系中的表达。

---

# 3. 合法旋转必须保持长度

旋转之后，向量方向改变，但长度不应该改变：

[
|Rp|=|p|
]

平方后：

[
(Rp)^T(Rp)=p^Tp
]

即：

[
p^TR^TRp=p^Tp
]

这个关系要对任意 (p) 成立，所以必须：

[
\boxed{
R^TR=I
}
]

这种矩阵叫：

> Orthogonal Matrix，正交矩阵。

因此：

[
R^{-1}=R^T
]

这解释了为什么旋转的逆可以直接使用转置。

---

# 4. 正交意味着什么？

如果：

[
R=
\begin{bmatrix}
r_1&r_2
\end{bmatrix}
]

其中 (r_1,r_2) 是列向量。

条件：

[
R^TR=I
]

意味着：

[
r_1^Tr_1=1
]

[
r_2^Tr_2=1
]

[
r_1^Tr_2=0
]

也就是：

* 两个轴长度均为 1；
* 两个轴相互垂直。

所以旋转以后，坐标系不会：

* 拉伸；
* 压缩；
* 剪切；
* 让两根坐标轴不再垂直。

---

# 5. 仅有正交性还不够

考虑矩阵：

[
M=
\begin{bmatrix}
1&0\
0&-1
\end{bmatrix}
]

它满足：

[
M^TM=I
]

但它做的是：

> 关于 (x) 轴镜像。

它不是旋转。

区别在于行列式：

[
\det(M)=-1
]

而合法旋转要求：

[
\boxed{
\det(R)=1
}
]

因此二维合法旋转矩阵同时满足：

[
\boxed{
R^TR=I,\qquad\det(R)=1
}
]

---

# 6. (SO(2)) 到底是什么？

二维旋转矩阵的集合写作：

[
\boxed{
SO(2)
=====

\left{
R\in\mathbb R^{2\times2}
\mid
R^TR=I,\ \det(R)=1
\right}
}
]

其中：

* (O)：Orthogonal；
* (S)：Special，表示行列式为 (+1)；
* (2)：二维空间。

所以：

> (SO(2)) 是所有二维纯旋转组成的集合。

它不只是一个矩阵格式，而是一个具有特殊运算结构的空间。

---

# 7. 为什么称为 Group？

一个集合要成为群，需要满足四个条件。

## ① 封闭性

两个旋转组合后，仍然是旋转：

[
R_1R_2\in SO(2)
]

---

## ② 结合律

[
(R_1R_2)R_3
===========

R_1(R_2R_3)
]

矩阵乘法天然满足。

---

## ③ 单位元

存在：

[
I=
\begin{bmatrix}
1&0\
0&1
\end{bmatrix}
]

满足：

[
IR=RI=R
]

它对应：

[
0^\circ
]

旋转。

---

## ④ 逆元

每个旋转都有逆旋转：

[
R^{-1}=R^T
]

对应角度：

[
-\theta
]

因此 (SO(2)) 是一个群。

---

# 8. 旋转组合为什么是矩阵乘法？

假设先旋转 (\theta_1)，再旋转 (\theta_2)：

[
p'
==

R(\theta_1)p
]

[
p''
===

R(\theta_2)p'
]

代入：

[
p''
===

R(\theta_2)R(\theta_1)p
]

所以总旋转为：

[
R_{\text{total}}
================

R(\theta_2)R(\theta_1)
]

在二维中可以证明：

[
\boxed{
R(\theta_2)R(\theta_1)
======================

R(\theta_1+\theta_2)
}
]

所以旋转组合对应角度相加。

---

# 9. 二维旋转可以交换

因为：

[
R(\theta_1)R(\theta_2)
======================

R(\theta_1+\theta_2)
]

而：

[
\theta_1+\theta_2
=================

\theta_2+\theta_1
]

所以：

[
\boxed{
R(\theta_1)R(\theta_2)
======================

R(\theta_2)R(\theta_1)
}
]

因此 (SO(2)) 是：

> Abelian Group，交换群。

但三维旋转通常不交换。

这是二维和三维旋转一个非常重要的区别。

---

# 10. 既然二维旋转就是一个角度，为什么还要用矩阵？

二维旋转确实可以用一个标量：

[
\theta
]

表示。

但旋转矩阵有几个优势：

## ① 直接作用于向量

[
p'=Rp
]

---

## ② 易于与坐标变换组合

可以直接放入：

[
T=
\begin{bmatrix}
R&t\
0&1
\end{bmatrix}
]

---

## ③ 无角度跳变问题

角度：

[
179^\circ
]

和：

[
-181^\circ
]

表示同一个方向附近，但数值看起来差很远。

旋转矩阵没有这种人为跳变。

---

## ④ 更容易推广到三维

二维角度很简单，三维旋转就复杂得多。

矩阵表示能够统一处理。

---

# 11. 为什么旋转不能简单当普通向量相加？

二维中看起来可以：

[
\theta_{\text{new}}
===================

\theta_1+\theta_2
]

但这里的角度存在周期性：

[
\theta
\equiv
\theta+2k\pi
]

例如：

[
0^\circ
\equiv360^\circ
]

所以角度不是普通实数轴上的普通变量。

更准确地说：

> 二维旋转空间是一个圆，而不是一条无限直线。

也就是：

[
SO(2)\cong S^1
]

其中 (S^1) 表示单位圆。

---

# 12. 角度差必须归一化

假设：

[
\theta_1=179^\circ
]

[
\theta_2=-179^\circ
]

直接相减：

[
\theta_2-\theta_1=-358^\circ
]

但真正最短旋转差是：

[
2^\circ
]

所以必须做角度归一化：

[
\boxed{
\Delta\theta
============

\operatorname{wrapToPi}(\theta_2-\theta_1)
}
]

把结果约束到：

[
(-\pi,\pi]
]

这在：

* Kalman Innovation；
* 控制误差；
* Pose Optimization；
* 轨迹比较；

中都非常重要。

---

# 13. 为什么两个角度不能直接算普通平均？

假设：

[
\theta_1=179^\circ
]

[
\theta_2=-179^\circ
]

普通平均：

[
\frac{179+(-179)}2=0^\circ
]

显然错误。

合理平均应该接近：

[
180^\circ
]

正确方法是先映射到单位圆：

[
c=
\sum_iw_i\cos\theta_i
]

[
s=
\sum_iw_i\sin\theta_i
]

再计算：

[
\boxed{
\bar\theta
==========

\operatorname{atan2}(s,c)
}
]

这说明：

> Rotation State 不能总用普通欧氏空间中的加减平均来处理。

---

# 14. 旋转矩阵如何表示复数乘法？

二维旋转还可以写成单位复数：

[
z=e^{i\theta}
=============

\cos\theta+i\sin\theta
]

一个二维点：

[
p=x+iy
]

旋转：

[
p'=e^{i\theta}p
]

因为：

[
e^{i\theta_1}e^{i\theta_2}
==========================

e^{i(\theta_1+\theta_2)}
]

所以复数乘法与二维旋转矩阵乘法完全对应。

这也是为什么二维旋转如此简单。

三维中没有同样简单的单个复数表示，需要使用四元数。

---

# 15. (SO(2)) 的一个微小扰动

假设当前旋转：

[
R(\theta)
]

加入一个很小角度：

[
\delta\theta
]

新的旋转可以写作：

[
R_{\text{new}}
==============

R(\theta)R(\delta\theta)
]

当：

[
\delta\theta\approx0
]

时：

[
\cos\delta\theta\approx1
]

[
\sin\delta\theta\approx\delta\theta
]

所以：

[
R(\delta\theta)
\approx
\begin{bmatrix}
1&-\delta\theta\
\delta\theta&1
\end{bmatrix}
]

写成：

[
\boxed{
R(\delta\theta)
\approx
I+\delta\theta
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
}
]

定义：

[
J=
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
]

那么：

[
R(\delta\theta)\approx I+\delta\theta J
]

这个 (J) 是二维旋转的生成元。

后面学习 Lie Algebra 时会再次出现。

---

# 16. 指数映射的雏形

二维旋转可以写成：

[
\boxed{
R(\theta)=\exp(\theta J)
}
]

其中：

[
J=
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
]

矩阵指数展开：

[
\exp(\theta J)
==============

I+\theta J+\frac{\theta^2J^2}{2!}+\cdots
]

因为：

[
J^2=-I
]

最终得到：

[
\exp(\theta J)
==============

I\cos\theta+J\sin\theta
]

也就是：

[
\begin{bmatrix}
\cos\theta&-\sin\theta\
\sin\theta&\cos\theta
\end{bmatrix}
]

这说明：

> 普通标量角度可以通过指数映射，生成一个合法旋转矩阵。

后面 (SO(3)) 和 (SE(3)) 也会使用类似思想。

---

# 17. 为什么不能直接优化旋转矩阵的四个元素？

二维旋转矩阵看起来有四个元素：

[
R=
\begin{bmatrix}
r_{11}&r_{12}\
r_{21}&r_{22}
\end{bmatrix}
]

但合法旋转只有一个自由度：

[
\theta
]

因为矩阵元素受到：

[
R^TR=I
]

和：

[
\det(R)=1
]

约束。

如果把四个元素当作四个独立普通变量优化，更新后可能得到：

[
R^TR\neq I
]

也就是矩阵不再代表旋转。

因此更合理的方法是：

* 用最小参数 (\theta) 更新；
* 或在 Lie Algebra 中更新；
* 更新后重新投影到 (SO(2))。

---

# 18. Degree of Freedom

二维旋转矩阵虽然是：

[
2\times2
]

包含 4 个数，但只有：

[
\boxed{1\text{ DoF}}
]

因为只需要一个角度确定。

二维刚体 Pose：

* (x)
* (y)
* (\theta)

因此：

[
SE(2)
]

共有：

[
\boxed{3\text{ DoF}}
]

这也提醒我们：

> 矩阵的元素个数不等于系统自由度。

---

# 19. 旋转矩阵漂移问题

理想旋转矩阵满足：

[
R^TR=I
]

但在数值计算中，经过大量乘法和浮点误差后，可能出现：

[
R^TR\approx I
]

但不再严格等于 (I)。

例如：

```text
轴长度略微不再为 1
轴之间略微不再垂直
```

常见处理方式：

* 使用角度重新生成 (R(\theta))；
* 使用 SVD 做正交化；
* 在 Lie Group 上更新；
* 三维中使用单位四元数并归一化。

---

# 20. (SO(2)) 与坐标变换的关系

假设：

[
{}^A R_B\in SO(2)
]

它表示：

> (B) 坐标系的方向，相对于 (A) 坐标系如何旋转。

点转换：

[
{}^A p
======

{}^A R_B,{}^B p
]

反向转换：

[
{}^B R_A
========

# ({}^A R_B)^{-1}

({}^A R_B)^T
]

所以：

[
{}^B p
======

{}^B R_A,{}^A p
]

---

# 本章核心总结

第一：

[
SO(2)
=====

{R\mid R^TR=I,\det R=1}
]

是所有二维合法旋转矩阵组成的集合。

第二：

> 旋转矩阵的列表示旋转后坐标轴在原坐标系中的方向。

第三：

[
R^{-1}=R^T
]

因为旋转保持长度和夹角。

第四：

[
R(\theta_1)R(\theta_2)=R(\theta_1+\theta_2)
]

二维旋转可交换。

第五：

> 二维旋转虽然可以用一个角度表示，但旋转空间具有周期性，不是普通实数直线。

第六：

> 对 Rotation 做平均、求差和优化时，必须尊重其空间结构。

---

# 思考题与参考答案

## 思考题 1

矩阵：

[
M=
\begin{bmatrix}
0&1\
1&0
\end{bmatrix}
]

是否属于 (SO(2))？

### 参考答案

先检查：

[
M^TM=I
]

所以它是正交矩阵。

但：

[
\det(M)=-1
]

因此它是镜像变换，不是纯旋转。

所以：

[
\boxed{M\notin SO(2)}
]

---

## 思考题 2

为什么二维旋转矩阵有四个元素，却只有一个自由度？

### 参考答案

因为四个元素不是独立的。

它们必须满足：

[
R^TR=I
]

以及：

[
\det(R)=1
]

这些约束将合法矩阵限制为：

[
R(\theta)
=========

\begin{bmatrix}
\cos\theta&-\sin\theta\
\sin\theta&\cos\theta
\end{bmatrix}
]

所以只需要一个参数 (\theta)。

---

## 思考题 3

为什么直接对两个方向角做算术平均可能错误？

### 参考答案

因为角度具有周期性。

例如：

[
179^\circ
]

和：

[
-179^\circ
]

实际上只相差 (2^\circ)，但普通平均得到：

[
0^\circ
]

正确方法是把角度映射到单位圆，分别平均正弦和余弦，再使用：

[
\operatorname{atan2}
]

恢复平均方向。

---

## 思考题 4

为什么优化旋转时不应该直接把旋转矩阵四个元素当作独立变量？

### 参考答案

因为任意元素更新后，矩阵可能不再满足：

[
R^TR=I,\qquad\det(R)=1
]

从而产生缩放、剪切或镜像，不再是合法旋转。

应该使用：

* 角度参数；
* Lie Algebra 增量；
* 或更新后重新正交化。

---

## 思考题 5

已知：

[
R(30^\circ)
]

和：

[
R(60^\circ)
]

两者相乘结果是什么？

### 参考答案

二维旋转组合对应角度相加：

[
R(60^\circ)R(30^\circ)
======================

R(90^\circ)
]

因此：

[
\boxed{
R=
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
}
]

---

下一章：

# Chapter 26 — (SE(2))：二维 Pose 为什么不是普通的 ([x,y,\theta]) 向量？

我们会讨论：

* 如何把 (SO(2)) 与 Translation 合成 (SE(2))；
* Pose Composition；
* Relative Pose；
* Pose Inverse；
* 为什么两个 Pose 不能直接逐元素相加；
* 左扰动与右扰动的初步区别；
* 二维 Pose 的指数映射。

