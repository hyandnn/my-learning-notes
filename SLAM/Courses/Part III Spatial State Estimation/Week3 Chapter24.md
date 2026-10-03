好，我们正式进入 Part III。

前两部分一直在回答：

> 机器人如何在不确定性下估计 State？

从这一章开始，我们进入空间状态本身：

> Position、Orientation、Pose 到底应该如何表示？

# Part III · Spatial State Estimation

## Chapter 24 — Coordinate Frames & Transformations

# 同一个物体，为什么可以同时拥有多个不同但都正确的坐标？

---

## 1. 坐标不是物体自身的属性

假设房间里有一把椅子。

你说：

[
\mathbf p=
\begin{bmatrix}
2\
1
\end{bmatrix}
]

这个坐标单独拿出来，其实没有完整意义。

必须继续问：

> 相对于哪个坐标系？

例如，相对于房间左下角建立的坐标系：

[
{}^W\mathbf p=
\begin{bmatrix}
2\
1
\end{bmatrix}
]

但如果以机器人当前位置作为坐标系原点，同一把椅子可能是：

[
{}^R\mathbf p=
\begin{bmatrix}
0.5\
-0.3
\end{bmatrix}
]

两个坐标不一样，却都正确。

因为它们描述的是：

> 同一个几何点，在不同参考系中的坐标表达。

所以必须区分：

* **几何对象本身**
* **几何对象在某个坐标系里的数值表示**

坐标值会随参考系改变，物体本身没有因此移动。

---

# 2. 坐标系是什么？

二维坐标系至少包含：

1. 原点在哪里；
2. (x) 轴朝哪里；
3. (y) 轴朝哪里。

三维坐标系还包含 (z) 轴，并通常遵循右手定则。

机器人系统中常见：

```text
World Frame
Map Frame
Odometry Frame
Robot / Base Frame
Camera Frame
IMU Frame
LiDAR Frame
Wheel Frame
```

它们不是重复设计。

每个坐标系都服务于一种表达需要。

例如：

* 地图适合放在 World/Map Frame；
* 机器人局部运动适合在 Base Frame 表达；
* 图像投影必须使用 Camera Frame；
* IMU 测量天然位于 IMU Frame。

---

# 3. 为什么机器人需要这么多坐标系？

因为不同 Sensor 安装在机器人不同位置，朝向也不同。

例如相机在机器人前方 10 cm，IMU 在机器人中心，LiDAR 在顶部。

同一个障碍物：

* 在 Camera Frame 下有一个坐标；
* 在 LiDAR Frame 下有另一个坐标；
* 在 Robot Frame 下又有一个坐标；
* 放到地图里还要转换到 World Frame。

机器人系统真正一直在做的是：

> 把同一个几何对象，从一个坐标系转换到另一个坐标系。

---

# 4. 先从纯平移开始

假设坐标系 (B) 相对于坐标系 (A) 向右平移：

[
{}^A\mathbf t_B
===============

\begin{bmatrix}
2\
1
\end{bmatrix}
]

表示：

> 坐标系 (B) 的原点，在坐标系 (A) 中位于 ((2,1))。

某个点在 (B) 系中的坐标：

[
{}^B\mathbf p=
\begin{bmatrix}
3\
4
\end{bmatrix}
]

如果两个坐标系方向完全相同，那么点在 (A) 系中：

[
{}^A\mathbf p
=============

{}^A\mathbf t_B
+
{}^B\mathbf p
]

即：

[
{}^A\mathbf p
=============

\begin{bmatrix}
2\
1
\end{bmatrix}
+
\begin{bmatrix}
3\
4
\end{bmatrix}
=============

\begin{bmatrix}
5\
5
\end{bmatrix}
]

纯平移时，坐标转换就是加上坐标系原点的偏移。

---

# 5. 再加入旋转

现实中两个坐标系的方向通常不一样。

假设坐标系 (B) 相对 (A) 旋转 (90^\circ)。

点在 (B) 系中：

[
{}^B\mathbf p=
\begin{bmatrix}
1\
0
\end{bmatrix}
]

它表示：

> 沿着 (B) 系的 (x) 轴前进 1。

但 (B) 系的 (x) 轴在 (A) 系里可能朝向上方。

所以在 (A) 系中：

[
{}^A\mathbf p=
\begin{bmatrix}
0\
1
\end{bmatrix}
]

这里需要旋转矩阵。

二维旋转矩阵：

[
R(\theta)
=========

\begin{bmatrix}
\cos\theta & -\sin\theta\
\sin\theta & \cos\theta
\end{bmatrix}
]

当：

[
\theta=90^\circ
]

得到：

[
R=
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
]

于是：

[
{}^A\mathbf p
=============

{}^A R_B,
{}^B\mathbf p
]

---

# 6. 记号到底是什么意思？

[
{}^A R_B
]

表示：

> 把一个在 (B) 坐标系中表达的向量，旋转成在 (A) 坐标系中的表达。

也可以理解为：

> 坐标系 (B) 的各个轴，在 (A) 坐标系里分别是什么方向。

二维情况下：

[
{}^A R_B
========

\begin{bmatrix}
|&|\
{}^A\mathbf e_{x_B}&{}^A\mathbf e_{y_B}\
|&|
\end{bmatrix}
]

第一列是：

> (B) 系 (x) 轴在 (A) 系中的坐标。

第二列是：

> (B) 系 (y) 轴在 (A) 系中的坐标。

这比把旋转矩阵死记成三角函数更本质。

---

# 7. 旋转加平移

一般坐标转换为：

[
\boxed{
{}^A\mathbf p
=============

{}^A R_B,{}^B\mathbf p
+
{}^A\mathbf t_B
}
]

其中：

* ({}^B\mathbf p)：点在 (B) 系中的表达；
* ({}^A R_B)：把方向从 (B) 转到 (A)；
* ({}^A\mathbf t_B)：(B) 系原点在 (A) 系中的位置；
* ({}^A\mathbf p)：最终点在 (A) 系中的表达。

顺序非常重要：

```text
先旋转点的局部坐标
再加上坐标系原点的平移
```

不是简单把旋转和平移随便交换。

---

# 8. 一个具体例子

假设机器人坐标系 (R) 在世界坐标系 (W) 中：

* 位置为 ((2,1))；
* 朝向为 (90^\circ)。

那么：

[
{}^W R_R
========

\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
]

[
{}^W\mathbf t_R
===============

\begin{bmatrix}
2\
1
\end{bmatrix}
]

机器人前方 1 米处有一个点：

[
{}^R\mathbf p=
\begin{bmatrix}
1\
0
\end{bmatrix}
]

转换到世界系：

[
{}^W\mathbf p
=============

{}^W R_R,{}^R\mathbf p
+
{}^W\mathbf t_R
]

# [

\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
\begin{bmatrix}
1\
0
\end{bmatrix}
+
\begin{bmatrix}
2\
1
\end{bmatrix}
]

# [

\begin{bmatrix}
0\
1
\end{bmatrix}
+
\begin{bmatrix}
2\
1
\end{bmatrix}
=============

\begin{bmatrix}
2\
2
\end{bmatrix}
]

机器人虽然局部认为点在“前方 1 米”，但因为机器人朝向世界 (y) 轴，所以世界坐标是 ((2,2))。

---

# 9. Pose 到底是什么？

Pose 不是只有 Position。

二维机器人 Pose 通常写成：

[
\mathbf x=
\begin{bmatrix}
x\
y\
\theta
\end{bmatrix}
]

其中：

* ((x,y))：Position；
* (\theta)：Orientation。

但更严格地说，Pose 是：

> 一个坐标系相对于另一个坐标系的位置和方向关系。

例如：

[
{}^W T_R
]

表示：

> Robot Frame 相对于 World Frame 的 Pose。

所以“机器人 Pose”本质上是在描述：

> Robot Frame 如何嵌入 World Frame。

---

# 10. 为什么要引入齐次坐标？

我们现在的转换是：

[
{}^A\mathbf p
=============

R,{}^B\mathbf p+t
]

它同时包含矩阵乘法和向量加法。

为了把旋转和平移统一成一次矩阵乘法，可以给点增加一维：

[
\tilde{\mathbf p}
=================

\begin{bmatrix}
x\
y\
1
\end{bmatrix}
]

然后定义齐次变换矩阵：

[
\boxed{
{}^A T_B
========

\begin{bmatrix}
{}^A R_B & {}^A\mathbf t_B\
0\quad0 & 1
\end{bmatrix}
}
]

二维情况下：

[
{}^A T_B
========

\begin{bmatrix}
r_{11}&r_{12}&t_x\
r_{21}&r_{22}&t_y\
0&0&1
\end{bmatrix}
]

于是：

[
\boxed{
{}^A\tilde{\mathbf p}
=====================

{}^A T_B,
{}^B\tilde{\mathbf p}
}
]

现在旋转和平移都被统一到矩阵乘法里。

---

# 11. 齐次变换矩阵不是普通矩阵

二维刚体变换矩阵：

[
T=
\begin{bmatrix}
R&t\
0&1
\end{bmatrix}
]

其中 (R) 必须是合法旋转矩阵。

也就是说：

[
R^TR=I
]

且：

[
\det(R)=1
]

不是任意 (3\times3) 矩阵都能表示刚体 Pose。

这类二维刚体变换组成的集合，后面会称为：

[
SE(2)
]

三维则是：

[
SE(3)
]

---

# 12. 坐标变换可以连续组合

假设：

* Camera Frame (C) 相对于 Robot Frame (R) 的变换是 ({}^R T_C)；
* Robot Frame (R) 相对于 World Frame (W) 的变换是 ({}^W T_R)。

那么 Camera 相对于 World：

[
\boxed{
{}^W T_C
========

{}^W T_R
{}^R T_C
}
]

如果点在 Camera Frame 中：

[
{}^C\mathbf p
]

那么：

[
{}^W\mathbf p
=============

{}^W T_R
{}^R T_C
{}^C\mathbf p
]

坐标系下标可以像单位一样“消去”：

```text
W ← R ← C
```

这是一种非常实用的检查方式。

---

# 13. 乘法顺序不能反

一般来说：

[
{}^W T_R,{}^R T_C
]

是合法的，因为中间坐标系 (R) 对接。

但：

[
{}^R T_C,{}^W T_R
]

通常没有正确的几何意义。

矩阵乘法不满足交换律：

[
T_1T_2\neq T_2T_1
]

物理上也很好理解：

```text
先旋转再平移
```

与：

```text
先平移再旋转
```

一般会得到不同结果。

---

# 14. 如何求逆变换？

假设：

[
{}^A T_B
========

\begin{bmatrix}
R&t\
0&1
\end{bmatrix}
]

它把 (B) 系坐标转换到 (A) 系。

反方向变换：

[
{}^B T_A
========

({}^A T_B)^{-1}
]

因为旋转矩阵：

[
R^{-1}=R^T
]

所以：

[
\boxed{
T^{-1}
======

\begin{bmatrix}
R^T&-R^Tt\
0&1
\end{bmatrix}
}
]

注意平移逆变换不是简单：

[
-t
]

而是：

[
-R^Tt
]

为什么？

因为平移向量也必须先被表达进新的坐标系。

---

# 15. 一个逆变换的直觉

已知 Robot Frame 原点在 World Frame 中：

[
{}^W\mathbf t_R
]

要计算 World 原点在 Robot Frame 中的位置，不能只取负号。

因为机器人坐标轴可能已经旋转。

正确步骤是：

1. 世界原点相对于机器人原点的世界系向量是 (-t)；
2. 再用 (R^T) 把这个向量转换到 Robot Frame。

所以：

[
{}^R\mathbf t_W=-R^Tt
]

---

# 16. Active Transformation 与 Passive Transformation

这是坐标变换中一个常见混淆。

## Passive Transformation

几何对象不动，只改变描述它的坐标系。

例如：

> 同一个点，从 Camera Frame 表达到 World Frame。

这是机器人中最常见的坐标转换理解。

---

## Active Transformation

坐标系不动，真正旋转或移动几何对象。

例如：

> 把点本身绕原点旋转 (90^\circ)。

两者可能使用相似的矩阵，但语义不同。

很多旋转方向、正负号问题，根源就是把 Active 和 Passive 混在了一起。

学习和写代码时，最好始终明确：

> 我是在移动对象，还是在改变对象的坐标表达？

---

# 17. 向量和点的变换是否一样？

不完全一样。

点：

[
\mathbf p
]

有位置，因此受旋转和平移影响：

[
\mathbf p'=R\mathbf p+t
]

方向向量，例如速度或法向量：

[
\mathbf v
]

没有固定原点，只受旋转影响：

[
\boxed{
\mathbf v'=R\mathbf v
}
]

不应该加平移。

使用齐次坐标时：

点写作：

[
\tilde{\mathbf p}
=================

\begin{bmatrix}
x\y\1
\end{bmatrix}
]

方向向量写作：

[
\tilde{\mathbf v}
=================

\begin{bmatrix}
v_x\v_y\0
\end{bmatrix}
]

最后一维的 1 和 0 正好区分它们是否受平移影响。

---

# 18. 法向量需要特别小心

对于纯旋转：

[
\mathbf n'=R\mathbf n
]

没有问题。

但对于一般线性变换 (A)，法向量不能简单写为：

[
A\mathbf n
]

而应使用：

[
\mathbf n'
==========

A^{-T}\mathbf n
]

不过刚体变换的旋转矩阵满足：

[
R^{-T}=R
]

所以在纯刚体旋转下，法向量仍然可以直接用 (R) 变换。

这个区别后面处理平面和图形变换时会很重要。

---

# 19. Frame Convention 为什么如此危险？

机器人领域经常存在不同坐标轴约定。

例如 Camera Frame 常见：

```text
x：向右
y：向下
z：向前
```

Robot Base Frame 可能是：

```text
x：向前
y：向左
z：向上
```

如果只看坐标数字，不理解 Frame Convention，非常容易出现：

* 左右颠倒；
* 上下颠倒；
* 旋转方向错误；
* 法向量符号错误；
* 外参看起来差一个 (90^\circ)。

因此任何坐标相关接口，都应该明确：

```text
Frame Name
Origin
Axis Direction
Handedness
Unit
Timestamp
```

坐标系问题特别喜欢伪装成算法问题。这个爱好很坏，但相当稳定。

---

# 20. 机器人系统中的一条典型变换链

假设 Camera 观测到一个点：

[
{}^C\mathbf p
]

要把它放进 World Map，需要：

[
{}^W\mathbf p
=============

{}^W T_R
{}^R T_C
{}^C\mathbf p
]

其中：

* ({}^R T_C)：Camera Extrinsic，通常通过标定获得；
* ({}^W T_R)：Robot Pose，由 Localization 或 SLAM 估计；
* ({}^C\mathbf p)：Sensor Observation。

这条公式实际上把 Part II 与 Part III 接上了：

```text
Sensor Observation
+
Extrinsic Calibration
+
Estimated Robot Pose
↓
World Coordinate
```

每一部分都有不确定性。

因此后续还会讨论：

> 坐标变换中的误差如何传播？

---

# 21. Position、Orientation 与 Pose 的区别

## Position

只表示原点的位置：

[
t
]

## Orientation

只表示坐标轴方向：

[
R
]

## Pose

两者共同组成：

[
T=
\begin{bmatrix}
R&t\
0&1
\end{bmatrix}
]

因此：

[
\boxed{
Pose = Position + Orientation
}
]

但从数学结构上，Pose 不是简单把参数拼成普通向量那么简单。

尤其在三维中：

* Position 属于欧氏空间；
* Rotation 属于旋转群；
* Pose 属于刚体变换群。

这正是后续章节的核心。

---

# 22. 本章最重要的知识链

```text
几何对象
↓
在不同 Frame 中有不同坐标表达
↓
Rotation 改变坐标轴方向
↓
Translation 改变坐标系原点
↓
Rigid Transformation
↓
Homogeneous Matrix
↓
Transformation Composition
↓
Pose
```

---

# 本章核心结论

第一：

> 坐标值不是物体自身的绝对属性，而是物体相对于某个坐标系的表达。

第二：

[
{}^A\mathbf p
=============

{}^A R_B,{}^B\mathbf p
+
{}^A\mathbf t_B
]

表示把点从 (B) 系表达转换到 (A) 系表达。

第三：

[
{}^A T_B
========

\begin{bmatrix}
{}^A R_B&{}^A t_B\
0&1
\end{bmatrix}
]

将旋转和平移统一成齐次变换。

第四：

[
{}^A T_C
========

{}^A T_B,{}^B T_C
]

变换可以按坐标系链进行组合，但顺序不能交换。

第五：

[
T^{-1}
======

\begin{bmatrix}
R^T&-R^Tt\
0&1
\end{bmatrix}
]

逆变换中的平移不能只简单取负。

---

# 思考题与参考答案

## 思考题 1

机器人在 World Frame 中位置为：

[
(2,3)
]

朝向为 (90^\circ)。

机器人坐标系中有一点：

[
{}^R p=
\begin{bmatrix}
2\0
\end{bmatrix}
]

该点在 World Frame 中是什么坐标？

### 参考答案

旋转矩阵：

[
{}^W R_R=
\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
]

平移：

[
{}^W t_R=
\begin{bmatrix}
2\3
\end{bmatrix}
]

所以：

[
{}^W p
======

{}^W R_R,{}^R p+{}^W t_R
]

# [

\begin{bmatrix}
0&-1\
1&0
\end{bmatrix}
\begin{bmatrix}
2\0
\end{bmatrix}
+
\begin{bmatrix}
2\3
\end{bmatrix}
]

# [

\begin{bmatrix}
0\2
\end{bmatrix}
+
\begin{bmatrix}
2\3
\end{bmatrix}
=============

\boxed{
\begin{bmatrix}
2\5
\end{bmatrix}}
]

---

## 思考题 2

为什么方向向量不能加 Translation？

### 参考答案

方向向量描述的是方向和大小，不描述某个固定空间位置。

例如速度：

[
v=
\begin{bmatrix}
1\0
\end{bmatrix}
]

把坐标系原点从一个地方平移到另一个地方，并不会改变速度方向。

所以方向向量只需要旋转：

[
v'=Rv
]

而点的位置需要：

[
p'=Rp+t
]

---

## 思考题 3

为什么：

[
({}^A T_B)^{-1}
]

中的平移是：

[
-R^Tt
]

而不是简单的 (-t)？

### 参考答案

(-t) 仍然是在 (A) 坐标系中表达的反向位移。

求逆变换时，需要得到这个位移在 (B) 坐标系中的表达。

因此必须再乘：

[
R^T
]

得到：

[
{}^B t_A=-R^Tt
]

---

## 思考题 4

已知：

[
{}^W T_R
]

和：

[
{}^R T_C
]

为什么 Camera 到 World 的变换是：

[
{}^W T_C
========

{}^W T_R,{}^R T_C
]

而不是反过来？

### 参考答案

因为一个 Camera Frame 中的点首先需要：

[
C\rightarrow R
]

然后：

[
R\rightarrow W
]

所以：

[
{}^W p
======

{}^W T_R
\left(
{}^R T_C,{}^C p
\right)
]

矩阵从右向左作用，因此组合为：

[
{}^W T_C
========

{}^W T_R,{}^R T_C
]

中间 Frame (R) 正好对接。

---

下一章我们会进入：

# Chapter 25 — 2D Rotation 与 (SO(2))

重点不再只是“旋转矩阵怎么算”，而是：

* 为什么合法 Rotation Matrix 只能满足特定约束；
* 为什么旋转不能被当作普通向量；
* 为什么旋转组合是矩阵乘法；
* 为什么二维旋转交换、三维旋转却不交换；
* (SO(2)) 到底是什么。

