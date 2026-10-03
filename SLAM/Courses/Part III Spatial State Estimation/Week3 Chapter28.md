# Part III · Chapter 28

# Quaternion（四元数）

## 为什么用 4 个数表示只有 3 个自由度的旋转？

上一章我们讲了三维旋转的几种表示：

* Rotation Matrix：9 个数，稳定但冗余；
* Euler Angles：3 个数，直观但有万向锁；
* Axis–Angle：3 个数，适合表达局部旋转；
* Lie Algebra：适合优化和小扰动。

这一章进入机器人系统中非常常用的姿态表示：

[
\boxed{\text{Quaternion}}
]

它用 4 个数表示三维旋转：

[
q=
\begin{bmatrix}
w\x\y\z
\end{bmatrix}
]

但三维旋转明明只有 3 个自由度。

因此第一个问题就是：

> 第四个数到底在干什么？

---

# 1. 四元数最初并不是为旋转发明的

普通复数可以写成：

[
z=a+bi
]

其中：

[
i^2=-1
]

复数乘法可以自然表示二维旋转。

例如单位复数：

[
z=\cos\theta+i\sin\theta
]

乘以另一个复数，相当于在二维平面旋转角度 (\theta)。

Hamilton 希望把这种结构推广到三维，于是引入了三个虚数单位：

[
i,\quad j,\quad k
]

四元数写作：

[
\boxed{
q=w+xi+yj+zk
}
]

其中：

* (w)：实部；
* ((x,y,z))：虚部。

通常也写成：

[
q=
\begin{bmatrix}
w\
\mathbf v
\end{bmatrix}
]

其中：

[
\mathbf v=
\begin{bmatrix}
x\y\z
\end{bmatrix}
]

---

# 2. 四元数的乘法规则

三个虚数单位满足：

[
i^2=j^2=k^2=-1
]

并且：

[
ij=k,\qquad jk=i,\qquad ki=j
]

交换顺序后符号相反：

[
ji=-k,\qquad kj=-i,\qquad ik=-j
]

这意味着四元数乘法不满足交换律：

[
\boxed{
q_1q_2\neq q_2q_1
}
]

这和三维旋转不交换正好一致。

它不是巧合，而是四元数能够表示三维旋转的关键原因之一。

---

# 3. 四元数的向量形式乘法

设：

[
q_1=
\begin{bmatrix}
w_1\
\mathbf v_1
\end{bmatrix},
\qquad
q_2=
\begin{bmatrix}
w_2\
\mathbf v_2
\end{bmatrix}
]

四元数乘法可以写成：

[
\boxed{
q_1\otimes q_2
==============

\begin{bmatrix}
w_1w_2-\mathbf v_1^T\mathbf v_2\
w_1\mathbf v_2+w_2\mathbf v_1+\mathbf v_1\times\mathbf v_2
\end{bmatrix}
}
]

你可以看到里面同时出现了：

* 点积；
* 叉积。

这正好体现了三维空间旋转的结构。

---

# 4. 并不是所有四元数都表示旋转

一个普通四元数有 4 个自由参数。

但表示旋转时，我们要求：

[
\boxed{
|q|=1
}
]

即：

[
w^2+x^2+y^2+z^2=1
]

满足该约束的四元数叫：

> Unit Quaternion，单位四元数。

4 个数减去 1 个单位长度约束：

[
4-1=3
]

所以单位四元数恰好有：

[
\boxed{3\text{ DoF}}
]

这就回答了最开始的问题。

第四个参数不是额外的旋转自由度，而是通过单位长度约束形成一种冗余表示。

---

# 5. Axis–Angle 如何转换成 Quaternion？

假设旋转表示为：

* 单位旋转轴：

[
\mathbf u=
\begin{bmatrix}
u_x\u_y\u_z
\end{bmatrix}
]

* 旋转角：

[
\theta
]

对应的单位四元数是：

[
\boxed{
q=
\begin{bmatrix}
\cos\frac{\theta}{2}\
\mathbf u\sin\frac{\theta}{2}
\end{bmatrix}
}
]

展开：

[
q=
\begin{bmatrix}
\cos\frac{\theta}{2}\
u_x\sin\frac{\theta}{2}\
u_y\sin\frac{\theta}{2}\
u_z\sin\frac{\theta}{2}
\end{bmatrix}
]

注意角度是：

[
\frac{\theta}{2}
]

而不是 (\theta)。

这是四元数表示旋转时非常重要的结构。

---

# 6. 为什么会出现半角？

单位四元数位于四维单位球面：

[
S^3
]

而三维旋转属于：

[
SO(3)
]

四元数到旋转之间是一个双覆盖关系。

一个完整的三维旋转角 (\theta)，在四元数球面上对应的是半角参数：

[
\frac{\theta}{2}
]

这也直接导致：

[
q
]

和：

[
-q
]

表示同一个旋转。

我们后面会详细解释。

---

# 7. 一个简单例子

绕 (z) 轴旋转 (90^\circ)。

旋转轴：

[
\mathbf u=
\begin{bmatrix}
0\0\1
\end{bmatrix}
]

角度：

[
\theta=90^\circ
]

所以：

[
\frac{\theta}{2}=45^\circ
]

四元数：

[
q=
\begin{bmatrix}
\cos45^\circ\
0\
0\
\sin45^\circ
\end{bmatrix}
]

即：

[
\boxed{
q=
\begin{bmatrix}
\frac{\sqrt2}{2}\
0\
0\
\frac{\sqrt2}{2}
\end{bmatrix}
}
]

---

# 8. Quaternion 的共轭

给定：

[
q=
\begin{bmatrix}
w\
\mathbf v
\end{bmatrix}
]

其共轭定义为：

[
\boxed{
q^*
===

\begin{bmatrix}
w\
-\mathbf v
\end{bmatrix}
}
]

展开：

[
q^*=w-xi-yj-zk
]

四元数满足：

[
q\otimes q^*
============

\begin{bmatrix}
|q|^2\
0
\end{bmatrix}
]

因此四元数逆为：

[
\boxed{
q^{-1}
======

\frac{q^*}{|q|^2}
}
]

如果 (q) 是单位四元数：

[
|q|=1
]

那么：

[
\boxed{
q^{-1}=q^*
}
]

这和旋转矩阵：

[
R^{-1}=R^T
]

非常类似。

---

# 9. Quaternion 如何旋转一个向量？

三维向量：

[
\mathbf p=
\begin{bmatrix}
p_x\p_y\p_z
\end{bmatrix}
]

先把它写成纯虚四元数：

[
\boxed{
p_q=
\begin{bmatrix}
0\
\mathbf p
\end{bmatrix}
}
]

然后使用：

[
\boxed{
p_q'
====

q\otimes p_q\otimes q^{-1}
}
]

最终结果的实部仍为 0，虚部就是旋转后的三维向量。

所以：

[
\mathbf p'
==========

R(q)\mathbf p
]

与旋转矩阵结果完全一致。

---

# 10. 为什么必须左右各乘一次？

如果只计算：

[
q\otimes p_q
]

结果通常仍是一个一般四元数，并不能保证保持向量长度，也不一定是纯虚四元数。

通过：

[
q\otimes p_q\otimes q^{-1}
]

相当于使用共轭作用：

> 用 (q) 改变向量的方向，同时用 (q^{-1}) 消除不需要的四维表示成分。

这一结构可以保证：

* 长度不变；
* 结果仍对应三维向量；
* 旋转组合与四元数乘法一致。

---

# 11. Quaternion 乘法为什么对应旋转组合？

假设：

* (q_1) 表示第一次旋转；
* (q_2) 表示第二次旋转。

一个向量先经过 (q_1)，再经过 (q_2)：

[
p'
==

q_1p q_1^{-1}
]

[
p''
===

q_2p'q_2^{-1}
]

代入：

[
p''
===

q_2q_1p q_1^{-1}q_2^{-1}
]

因为：

[
(q_2q_1)^{-1}
=============

q_1^{-1}q_2^{-1}
]

所以：

[
p''
===

(q_2q_1)p(q_2q_1)^{-1}
]

因此总旋转四元数为：

[
\boxed{
q_{\text{total}}
================

q_2\otimes q_1
}
]

注意矩阵一样：

> 右边的旋转先作用。

顺序同样不能反。

---

# 12. Quaternion 转 Rotation Matrix

设单位四元数：

[
q=
\begin{bmatrix}
w\x\y\z
\end{bmatrix}
]

对应旋转矩阵：

[
\boxed{
R(q)
====

\begin{bmatrix}
1-2(y^2+z^2)
&
2(xy-wz)
&
2(xz+wy)
\
2(xy+wz)
&
1-2(x^2+z^2)
&
2(yz-wx)
\
2(xz-wy)
&
2(yz+wx)
&
1-2(x^2+y^2)
\end{bmatrix}
}
]

不同库可能采用：

* ([w,x,y,z])
* ([x,y,z,w])

两种存储顺序。

公式和 API 使用前必须确认 convention。

这类坑没有数学难度，但非常擅长浪费下午。

---

# 13. Rotation Matrix 转 Quaternion

从旋转矩阵恢复 Quaternion，理论上可以通过矩阵迹：

[
\operatorname{tr}(R)
]

计算：

[
w
=

\frac12
\sqrt{1+\operatorname{tr}(R)}
]

然后求：

[
x,y,z
]

但当 (w) 接近 0，即旋转角接近 (180^\circ) 时，这种直接算法可能数值不稳定。

工程库通常会根据：

* 矩阵迹；
* 最大对角元素；

选择不同计算分支。

因此实际项目中建议使用成熟数学库，而不是随手复制一套未经验证的转换公式。

---

# 14. 为什么 (q) 和 (-q) 表示同一个旋转？

给定：

[
q=
\begin{bmatrix}
\cos\frac\theta2\
\mathbf u\sin\frac\theta2
\end{bmatrix}
]

取负：

[
-q=
\begin{bmatrix}
-\cos\frac\theta2\
-\mathbf u\sin\frac\theta2
\end{bmatrix}
]

对向量执行旋转：

[
(-q)p(-q)^{-1}
]

因为：

[
(-q)^{-1}=-q^{-1}
]

所以：

[
(-q)p(-q)^{-1}
==============

# (-q)p(-q^{-1})

qpq^{-1}
]

两个负号抵消。

因此：

[
\boxed{
q\sim -q
}
]

表示完全相同的 Orientation。

这叫：

> Double Cover，双覆盖。

---

# 15. 双覆盖会导致什么工程问题？

假设连续两帧姿态：

[
q_t
]

和：

[
q_{t+1}
]

真实旋转变化很小。

但某个库可能输出：

[
q_{t+1}\approx -q_t
]

虽然姿态完全连续，但四元数数值会突然整体跳号。

如果直接计算欧氏差：

[
q_{t+1}-q_t
]

会得到一个很大的变化。

因此在处理四元数序列时，常做：

[
\text{if }q_t^Tq_{t+1}<0
]

则：

[
q_{t+1}\leftarrow-q_{t+1}
]

这样让相邻四元数落在同一个半球，保持数值连续。

---

# 16. Quaternion 的距离不能直接用四维欧氏距离

因为：

[
q
]

与：

[
-q
]

表示同一旋转。

所以：

[
|q_1-q_2|
]

不是始终可靠的旋转距离。

一种常见做法是使用内积：

[
|q_1^Tq_2|
]

两个单位四元数之间的相对旋转角可以写成：

[
\boxed{
\Delta\theta
============

2\cos^{-1}
\left(
|q_1^Tq_2|
\right)
}
]

取绝对值就是为了消除 (q) 和 (-q) 的双覆盖歧义。

也可以先计算相对四元数：

[
q_{\text{err}}
==============

q_1^{-1}\otimes q_2
]

然后从中恢复旋转角。

---

# 17. Quaternion 为什么没有 Gimbal Lock？

Euler Angles 使用三个顺序旋转角作为全局参数。

在某些姿态下，参数轴会退化，从而出现 Gimbal Lock。

单位四元数则在四维单位球面上表示 Orientation，没有采用那种三轴顺序参数化，因此不存在 Euler Angle 那种参数奇异点。

所以：

[
\boxed{
\text{Quaternion does not suffer from Euler-angle gimbal lock}
}
]

但这不等于四元数完全没有问题。

它仍然有：

* 单位长度约束；
* (q) 与 (-q) 双覆盖；
* 不能直接普通相加；
* 归一化和 convention 问题；
* (180^\circ) 附近插值路径选择问题。

---

# 18. 为什么 Quaternion 必须归一化？

表示旋转的 Quaternion 必须满足：

[
|q|=1
]

但持续积分和浮点计算会产生误差：

[
|q|\neq1
]

如果不处理，转换出的矩阵可能不再严格保持长度。

因此工程实现中常做：

[
\boxed{
q\leftarrow\frac{q}{|q|}
}
]

尤其在：

* IMU 姿态积分；
* 数值优化；
* 网络预测四元数；

后，需要显式检查归一化。

但也不能依靠“最后归一化”掩盖所有错误。如果范数长期偏差很大，往往说明更新模型或时间步存在问题。

---

# 19. Gyroscope 如何更新 Quaternion？

陀螺仪测量角速度：

[
\boldsymbol\omega=
\begin{bmatrix}
\omega_x\\omega_y\\omega_z
\end{bmatrix}
]

短时间：

[
\Delta t
]

对应旋转增量：

[
\delta\boldsymbol\phi
=====================

\boldsymbol\omega\Delta t
]

可以构造增量四元数：

[
\delta q
========

\begin{bmatrix}
\cos\frac{|\delta\phi|}{2}\
\frac{\delta\phi}{|\delta\phi|}
\sin\frac{|\delta\phi|}{2}
\end{bmatrix}
]

姿态更新：

[
\boxed{
q_{t+1}
=======

q_t\otimes\delta q
}
]

或根据坐标约定使用左乘：

[
q_{t+1}
=======

\delta q\otimes q_t
]

关键仍然是：

> 角速度在哪个坐标系表达，以及 Quaternion 表示哪个 Frame 到哪个 Frame 的旋转。

---

# 20. 小角度 Quaternion

当：

[
|\delta\phi|
]

很小时：

[
\cos\frac{|\delta\phi|}{2}
\approx1
]

[
\sin\frac{|\delta\phi|}{2}
\approx
\frac{|\delta\phi|}{2}
]

所以：

[
\boxed{
\delta q
\approx
\begin{bmatrix}
1\
\frac12\delta\phi
\end{bmatrix}
}
]

注意虚部是：

[
\frac12\delta\phi
]

而不是 (\delta\phi)。

这与四元数的半角结构一致。

在 Error-State Kalman Filter 中，经常使用这个小角度近似。

---

# 21. 为什么不能直接把角速度积分到 Quaternion 四个分量？

Quaternion 的时间导数可以写成：

[
\dot q
======

\frac12
q\otimes
\begin{bmatrix}
0\
\omega
\end{bmatrix}
]

或者另一种乘法顺序，取决于 convention。

简单 Euler 积分：

[
q_{t+\Delta t}
\approx
q_t+\dot q_t\Delta t
]

然后归一化，短时间内可以工作。

但更几何一致的方式是：

[
q_{t+\Delta t}
==============

q_t\otimes
\operatorname{Exp}_q(\omega\Delta t)
]

也就是通过增量旋转组合，而不是把 4 个分量当普通向量累加。

---

# 22. Quaternion 的普通线性插值问题

假设两姿态：

[
q_0,\quad q_1
]

直接线性插值：

[
q(t)
====

(1-t)q_0+tq_1
]

结果通常不再单位长度，所以需要归一化：

[
q_{\text{nlerp}}(t)
===================

\frac{(1-t)q_0+tq_1}
{|(1-t)q_0+tq_1|}
]

这叫 Nlerp。

它：

* 计算便宜；
* 路径通常平滑；
* 但角速度不一定恒定。

---

# 23. SLERP：球面线性插值

更标准的 Quaternion 插值是：

> Spherical Linear Interpolation。

定义：

[
\Omega
======

\cos^{-1}(q_0^Tq_1)
]

则：

[
\boxed{
\operatorname{Slerp}(q_0,q_1;t)
===============================

\frac{\sin((1-t)\Omega)}{\sin\Omega}q_0
+
\frac{\sin(t\Omega)}{\sin\Omega}q_1
}
]

它沿四维单位球面上的大圆路径插值。

优点：

* 保持单位长度；
* 对应恒定角速度；
* 路径几何意义正确。

---

# 24. SLERP 为什么要检查内积符号？

如果：

[
q_0^Tq_1<0
]

说明二者在四维球面上相隔超过 (90^\circ)。

但因为：

[
q_1\sim -q_1
]

可以先令：

[
q_1\leftarrow-q_1
]

这样选择更短的球面路径。

否则 SLERP 可能绕远路，导致 Orientation 插值多转一大圈。

---

# 25. Quaternion 平均为什么不简单？

多个四元数：

[
q_1,q_2,\ldots,q_N
]

不能无条件做普通算术平均。

原因包括：

* (q) 与 (-q) 等价；
* 平均结果可能不在单位球面；
* Orientation Space 不是普通线性空间。

简单场景中可以先统一符号，再加权求和并归一化：

[
\bar q
======

\frac{\sum_iw_iq_i}
{\left|\sum_iw_iq_i\right|}
]

但更严格的姿态平均通常应在 (SO(3)) 或切空间中定义优化问题。

---

# 26. Quaternion 与 Rotation Vector 的关系

给定单位四元数：

[
q=
\begin{bmatrix}
w\
\mathbf v
\end{bmatrix}
]

旋转角：

[
\boxed{
\theta
======

2\operatorname{atan2}
(|\mathbf v|,w)
}
]

如果：

[
|\mathbf v|>0
]

旋转轴：

[
\mathbf u
=========

\frac{\mathbf v}{|\mathbf v|}
]

旋转向量：

[
\boxed{
\phi=\theta\mathbf u
}
]

反过来：

[
q
=

\begin{bmatrix}
\cos(|\phi|/2)\
\frac{\phi}{|\phi|}
\sin(|\phi|/2)
\end{bmatrix}
]

所以 Quaternion、Axis–Angle 和 Lie Algebra 之间可以互相转换。

---

# 27. Quaternion 在优化中如何更新？

虽然 Quaternion 用 4 个参数存储，但不建议直接用一个 4 维普通增量：

[
q_{\text{new}}=q+\delta q
]

因为：

* 结果可能不满足单位长度；
* 4 维增量中有一个冗余方向；
* 几何语义不清楚。

更合理的方法是使用三维局部旋转增量：

[
\delta\phi\in\mathbb R^3
]

构造：

[
\delta q=\operatorname{Exp}_q(\delta\phi)
]

再更新：

[
\boxed{
q_{\text{new}}
==============

q\otimes\delta q
}
]

或左乘。

也就是说：

> Quaternion 负责全局保存 Orientation，三维旋转向量负责局部优化。

---

# 28. Quaternion Convention 的四类常见差异

在工程中，必须确认至少四件事。

## ① 分量顺序

[
[w,x,y,z]
]

还是：

[
[x,y,z,w]
]

---

## ② 主动还是被动旋转

是旋转向量本身，还是改变坐标表达？

---

## ③ Frame 方向

Quaternion 表示：

[
{}^A R_B
]

还是：

[
{}^B R_A
]

---

## ④ Hamilton 还是其他乘法约定

不同系统可能采用不同 Quaternion Product 符号和坐标约定。

例如 Eigen、ROS 消息、某些视觉库、航空系统接口的存储方式可能不同。

看到四个数字相同，不等于语义相同。

---

# 29. Quaternion 的优势与不足

## 优势

* 没有 Euler Angle 的 Gimbal Lock；
* 只需 4 个参数，比旋转矩阵紧凑；
* 组合计算高效；
* 适合姿态积分；
* 适合平滑插值；
* 数值上通常较稳定。

## 不足

* 不直观；
* 有单位长度约束；
* (q) 与 (-q) 双覆盖；
* Convention 容易混乱；
* 不能直接普通相加或平均；
* 优化时仍最好使用 3 维局部扰动。

所以 Quaternion 不是“比其他表示全面高级”。

它只是：

> 在全局姿态存储、组合、积分和插值方面非常实用的一种表示。

---

# 30. Rotation Matrix、Quaternion 与 Lie Algebra 如何配合？

现代机器人系统中非常常见的组合是：

## 内部存储

[
R
]

或：

[
q
]

保证完整姿态表达。

## 局部更新

[
\delta\phi\in\mathbb R^3
]

使用 Lie Algebra 或旋转向量。

## 用户显示

[
roll,\ pitch,\ yaw
]

转换为 Euler Angles。

因此它们并不是互相替代关系，而是分别适合不同任务。

---

# 本章核心总结

第一：

单位 Quaternion：

[
q=
\begin{bmatrix}
w\x\y\z
\end{bmatrix},
\qquad
|q|=1
]

具有 3 个自由度，可以表示三维旋转。

第二：

Axis–Angle 到 Quaternion：

[
q=
\begin{bmatrix}
\cos(\theta/2)\
u\sin(\theta/2)
\end{bmatrix}
]

第三：

向量旋转：

[
p_q'=q\otimes p_q\otimes q^{-1}
]

第四：

Quaternion 乘法对应 Rotation Composition，并且不可交换。

第五：

[
q
]

和：

[
-q
]

表示同一个 Orientation。

第六：

Quaternion 没有 Euler Angle 的万向锁，但仍需处理单位约束、双覆盖、插值和 convention。

第七：

工程中通常使用 Quaternion 保存姿态，使用三维局部旋转向量进行优化和滤波更新。

---

# 思考题与参考答案

## 思考题 1

为什么单位 Quaternion 有 4 个分量，却只有 3 个自由度？

### 参考答案

四元数的 4 个分量受到单位长度约束：

[
w^2+x^2+y^2+z^2=1
]

该约束减少一个独立自由度，因此：

[
4-1=3
]

与三维旋转的 3 DoF 一致。

---

## 思考题 2

绕 (x) 轴旋转 (180^\circ) 的 Quaternion 是什么？

### 参考答案

旋转轴：

[
u=
\begin{bmatrix}
1\0\0
\end{bmatrix}
]

角度：

[
\theta=\pi
]

因此：

[
q=
\begin{bmatrix}
\cos(\pi/2)\
u\sin(\pi/2)
\end{bmatrix}
=============

\begin{bmatrix}
0\1\0\0
\end{bmatrix}
]

同时：

[
\begin{bmatrix}
0\-1\0\0
\end{bmatrix}
]

也表示同一个旋转，因为 (q) 和 (-q) 等价。

---

## 思考题 3

为什么姿态序列中 Quaternion 可能突然整体变号，但 Orientation 并没有跳变？

### 参考答案

因为单位 Quaternion 对 (SO(3)) 是双覆盖：

[
q\sim -q
]

两者对应同一个 Rotation Matrix。

算法或库可能在不同时间选择不同符号表示，所以数值会整体变号，但物理姿态不变。

处理连续序列时，可以根据相邻内积统一符号。

---

## 思考题 4

为什么不能直接对 Quaternion 做：

[
q_{\text{new}}=q+\delta q
]

作为旋转更新？

### 参考答案

因为普通加法：

* 不保证结果仍是单位 Quaternion；
* 不对应正确的 Rotation Composition；
* 4 维增量包含冗余自由度；
* 更新语义不符合 (SO(3)) 的几何结构。

更合理的是用三维旋转增量：

[
\delta\phi
]

生成单位增量 Quaternion：

[
\delta q=\operatorname{Exp}_q(\delta\phi)
]

再通过 Quaternion 乘法更新。

---

## 思考题 5

为什么 Quaternion 没有 Gimbal Lock，但仍然不能说它“没有奇异问题”？

### 参考答案

Quaternion 不采用 Euler Angle 的顺序旋转参数，因此没有 Euler 参数轴重合产生的 Gimbal Lock。

但它仍然存在：

* 单位长度约束；
* (q) 与 (-q) 的双覆盖歧义；
* (180^\circ) 附近符号和插值路径问题；
* 不适合直接做普通线性平均；
* 不同库 convention 不一致。

因此它避免了一类奇异性，但不是毫无使用风险。

---

## 思考题 6

两个单位 Quaternion：

[
q_1,\quad q_2
]

如果：

[
q_1^Tq_2<0
]

在做 SLERP 前通常应该怎么处理？为什么？

### 参考答案

通常令：

[
q_2\leftarrow-q_2
]

因为 (q_2) 和 (-q_2) 表示同一个 Orientation。

翻转符号后，两个四元数在四维单位球面上的距离更短，可以避免 SLERP 沿长路径插值。

---

## 思考题 7

为什么小旋转增量 Quaternion 近似为：

[
\delta q
\approx
\begin{bmatrix}
1\
\frac12\delta\phi
\end{bmatrix}
]

而虚部不是直接等于 (\delta\phi)？

### 参考答案

Quaternion 使用半角表示：

[
q=
\begin{bmatrix}
\cos(\theta/2)\
u\sin(\theta/2)
\end{bmatrix}
]

当 (\theta) 很小时：

[
\cos(\theta/2)\approx1
]

[
\sin(\theta/2)\approx\theta/2
]

且：

[
\delta\phi=\theta u
]

所以虚部约为：

[
\frac12\delta\phi
]

---

下一章：

# Chapter 29 — (SE(3))：三维 Pose 如何同时组合 Rotation 与 Translation？

我们会讨论：

* (SE(3)) 的齐次变换；
* 三维 Pose Composition 与 Inverse；
* Relative Pose；
* (\mathfrak{se}(3)) 的 6 维扰动；
* Twist；
* (SE(3)) 指数映射；
* Rotation 与 Translation 为什么在刚体运动中发生耦合；
* Adjoint 如何转换速度、误差和协方差。

