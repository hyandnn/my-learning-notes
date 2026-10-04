---
title: 坐标系约定与变换调试
description: 坐标系约定与变换调试的课程笔记。
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 30
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# 坐标系约定与变换调试

## 为什么很多“算法问题”，最后其实只是坐标系写反了？

前面我们已经学过：

$$
SO(3),\quad SE(3),\quad Quaternion,\quad Exp/Log
$$
从数学上看，我们已经知道怎样表示和组合三维 Pose。

但工程中真正高频、也最折磨人的问题往往不是不会推公式，而是：

* 变换方向写反；
* Frame 名称理解错；
* 矩阵乘法顺序错误；
* 坐标轴约定不一致；
* 主动旋转和被动变换混用；
* Quaternion convention 不一致；
* 时间戳对应错位。

这些错误通常不会让程序直接崩溃。

它们更喜欢输出一个“看起来有点像对的结果”，然后让人调参数调三天。

---

## 1. 本章要解决的核心问题

看到：

$$
{}^A T_B
$$
你必须能够立刻回答三个问题：

1. 它描述的是谁相对于谁的 Pose？
2. 它把哪个 Frame 中表达的坐标转换到哪个 Frame？
3. 其中的平移向量在哪个 Frame 中表达？

我们采用前面一直使用的约定：

$$
\boxed{
{}^A T_B
}
$$
表示：

> 坐标系 (B) 相对于坐标系 (A) 的 Pose。

同时，它可以把一个在 (B) Frame 中表达的点转换为在 (A) Frame 中的表达：

$$
\boxed{
{}^A p
=
{}^A T_B\,{}^B p
}
$$
这两个说法是一致的。

---

## 2. 为什么“B 相对于 A”容易让人迷惑？

假设：

$$
{}^W T_C
$$
很多人会在脑中混淆成：

* World 相对于 Camera；
* Camera 到 World；
* World 到 Camera；
* Camera 在 World 中的位置。

我们统一一下。

$$
{}^W T_C
$$
表示：

> Camera Frame (C) 在 World Frame (W) 中的 Pose。

也就是说：

* Rotation 部分描述 Camera 坐标轴在 World 中的方向；
* Translation 部分描述 Camera 原点在 World 中的位置。

它的坐标转换作用是：

$$
{}^W p
=
{}^W T_C\,{}^C p
$$
也就是：

> Camera coordinates → World coordinates。

因此可以记成：

$$
\boxed{
{}^{\text{输出 Frame}}T_{\text{输入 Frame}}
}
$$
---

## 3. 下标消去法

判断变换链是否正确，最有效的方法之一是把 Frame 当作单位。

例如：

$$
{}^W T_B\,{}^B T_C
$$
中间的 (B) 可以“消去”：

$$
W\leftarrow B\leftarrow C
$$
所以结果是：

$$
{}^W T_C
$$
即：

$$
\boxed{
{}^W T_C
=
{}^W T_B\,{}^B T_C
}
$$
如果你写成：

$$
{}^B T_C\,{}^W T_B
$$
Frame 无法对接：

```text
B ← C     W ← B
```

中间不是同一个 Frame，因此从语义上就已经错误。

矩阵维度可能完全合法，但几何意义不合法。

这也是坐标变换 bug 很难被编译器发现的原因。

---

## 4. 从右向左读变换链

考虑：

$$
{}^W p
=
{}^W T_B
{}^B T_C
{}^C p
$$
应该从右往左读：

1. 点最初在 Camera Frame 中；
2. 通过 ({}^B T_C)，转换到 Base Frame；
3. 通过 ({}^W T_B)，转换到 World Frame。

因此：

```text
Camera
  ↓
Base
  ↓
World
```

与函数调用嵌套类似：

$$
{}^W T_B
\left(
{}^B T_C
(
{}^C p
)
\right)
$$
不要按照矩阵从左往右的书写顺序想象实际作用顺序。

---

## 5. World-to-Camera 与 Camera-to-World

这是视觉系统最常见的混淆之一。

## Camera-to-World

$$
{}^W T_C
$$
把 Camera Frame 中的点转换到 World：

$$
{}^W p
=
{}^W T_C\,{}^C p
$$
它描述 Camera 在 World 中的 Pose。

---

## World-to-Camera

$$
{}^C T_W
$$
把 World Point 转换到 Camera：

$$
{}^C p
=
{}^C T_W\,{}^W p
$$
二者互为逆：

$$
\boxed{
{}^C T_W
=
({}^W T_C)^{-1}
}
$$
---

## 6. 为什么计算机视觉里经常使用 World-to-Camera？

因为图像投影要求点先进入 Camera Frame：

$$
{}^C p
=
{}^C R_W\,{}^W p
+
{}^C t_W
$$
然后：

$$
u=\pi({}^C p)
$$
所以视觉投影公式天然需要：

$$
{}^C T_W
$$
也就是 World-to-Camera。

但 SLAM 系统在展示轨迹时，经常保存 Camera 在 World 中的 Pose：

$$
{}^W T_C
$$
因此常见工作流是：

```text
系统内部保存 T_WC
↓
做投影时求逆
↓
得到 T_CW
```

或者系统直接保存 (T_{CW})。

两种都可以，但变量名必须诚实。

---

## 7. OpenCV 外参中的 (R,t) 是什么？

OpenCV 常见投影模型：

$$
p_C
=
Rp_W+t
$$
因此这里的：

$$
R,\ t
$$
通常组成：

$$
{}^C T_W
$$
即：

> World-to-Camera 变换。

特别注意：

$$
t
$$
并不直接等于 Camera 在 World 中的位置。

Camera Center (C_W) 满足：

$$
0
=
RC_W+t
$$
所以：

$$
\boxed{
C_W=-R^Tt
}
$$
这是非常常见的误区。

---

## 8. 一个具体例子

假设 Camera 在 World 中的位置为：

$$
C_W=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
Camera 朝向与 World 相同：

$$
{}^W R_C=I
$$
那么：

$$
{}^W T_C
=
\begin{bmatrix}
I&C_W\\
0&1
\end{bmatrix}
$$
其逆：

$$
{}^C T_W
=
\begin{bmatrix}
I&-C_W\\
0&1
\end{bmatrix}
$$
所以 OpenCV 形式中的平移是：

$$
t=
\begin{bmatrix}
-1\\0\\0
\end{bmatrix}
$$
而不是 Camera Position：

$$
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
二者方向相反，因为它们属于逆变换。

---

## 9. Extrinsic 到底是什么意思？

“Camera Extrinsic”这个词本身不够精确。

有人可能用它表示：

$$
{}^B T_C
$$
即 Camera 到 Base。

另一些人可能存：

$$
{}^C T_B
$$
即 Base 到 Camera。

两者都可能被叫作：

```text
camera extrinsic
```

所以不能仅凭变量名 `extrinsic` 判断方向。

必须检查它实际满足哪个公式。

例如：

$$
p_B=T_{BC}p_C
$$
那么 `T_BC` 就是：

$$
{}^B T_C
$$
如果：

$$
p_C=T_{CB}p_B
$$
则是：

$$
{}^C T_B
$$
---

## 10. 最可靠的命名方式

不推荐：

```cpp
camera_pose
extrinsic
transform
rotation
```

它们缺少 Frame 语义。

更推荐：

```cpp
T_world_camera
T_camera_world
T_base_camera
R_world_imu
p_camera
p_world
```

或者更简洁但保持统一：

```cpp
T_WC
T_CW
T_BC
R_WI
p_C
p_W
```

尤其不要让变量名和实际方向相反。

例如变量叫：

```cpp
T_camera_to_world
```

实际却用于：

```cpp
p_camera = T_camera_to_world * p_world;
```

这种命名会持续制造新的 bug。

---

## 11. Active Rotation 与 Passive Transformation

再系统地区分一次。

## Active Rotation

点或物体真的在固定坐标系中旋转。

$$
p'=Rp
$$
含义：

> 坐标系不动，向量本身转动。

---

## Passive Transformation

几何向量不动，只改变表达它的坐标系。

例如同一向量从 (B) Frame 表达到 (A) Frame：

$$
{}^A p
=
{}^A R_B\,{}^B p
$$
数值发生变化，但真实几何对象没有移动。

---

## 12. 为什么二者常出现转置关系？

假设 Frame (B) 相对于 Frame (A) 旋转了 (+\theta)。

那么 (B) 的轴在 (A) 中由：

$$
{}^A R_B=R(\theta)
$$
描述。

同一个几何向量从 (A) 表达到 (B) 时：

$$
{}^B p
=
({}^A R_B)^T{}^A p
$$
即：

$$
{}^B p
=
R(-\theta){}^A p
$$
这看起来像是反方向旋转。

原因是：

> 坐标轴向一个方向旋转后，同一个向量的坐标数值会向相反方向变化。

因此“旋转坐标系”和“旋转向量”经常相差一个逆或转置。

---

## 13. Fixed Axes 与 Body Axes

三维连续旋转时，还要区分旋转是绕：

* 固定参考系轴；
* 当前物体局部轴。

假设当前姿态：

$$
R
$$
## 绕世界轴施加增量

通常使用左乘：

$$
R_{\text{new}}
=
\Delta R,R
$$
## 绕当前局部轴施加增量

通常使用右乘：

$$
R_{\text{new}}
=
R,\Delta R
$$
因为三维旋转不可交换，结果不同。

所以代码里看到：

```cpp
R = dR * R;
```

和：

```cpp
R = R * dR;
```

不能认为只是写法不同。

它们表达的是不同 Frame 中的旋转增量。

---

## 14. Camera Frame 常见轴约定

OpenCV 风格 Camera Frame 常见约定：

```text
x：图像右方
y：图像下方
z：相机前方
```

这通常是右手坐标系，因为：

$$
x\times y=z
$$
即右 × 下 = 前。

图像坐标原点通常在左上角：

```text
u：向右
v：向下
```

所以 Camera Frame 的 (x,y) 方向与图像轴比较直观。

---

## 15. 机器人 Base Frame 常见约定

ROS REP-103 常见移动机器人机体坐标约定：

```text
x：前
y：左
z：上
```

也是右手坐标系：

$$
x\times y=z
$$
Camera Frame 和 Base Frame 即使安装方向“看起来一致”，轴定义也可能完全不同：

```text
Base x 前      Camera z 前
Base y 左      Camera x 右
Base z 上      Camera y 下
```

因此它们之间必然存在一个轴置换与符号翻转旋转。

---

## 16. Camera Optical Frame 与普通 Camera Frame

某些系统会同时存在：

```text
camera_link
camera_optical_frame
```

例如 ROS 中：

* `camera_link` 可能遵守机器人机体风格；
* `camera_optical_frame` 通常遵守光学约定：

```text
x 右
y 下
z 前
```

如果算法使用的是 Optical Frame，但外参标定给的是 `camera_link`，中间少了一层固定旋转，就会出现明显轴错位。

因此 Frame 名称不只是标签。

它往往暗含轴 convention。

---

## 17. IMU Frame 常见问题

IMU 输出：

* Angular velocity；
* Linear acceleration；
* Orientation。

但必须确认：

1. 数值在哪个 IMU Frame 中表达；
2. IMU Frame 的轴朝向；
3. 输出是否已经减去重力；
4. Orientation 表示 World-to-IMU 还是 IMU-to-World；
5. World Frame 使用 ENU、NED 还是其他 convention。

如果把 NED 和 ENU 混用，常见表现包括：

* (z) 轴正负颠倒；
* yaw 方向相反；
* roll/pitch 对应错误；
* 重力朝上。

---

## 18. ENU 与 NED

## ENU

```text
x：East
y：North
z：Up
```

## NED

```text
x：North
y：East
z：Down
```

航空与无人机系统中经常使用 NED。

机器人和地理系统中可能使用 ENU。

它们不仅是轴顺序不同，(z) 方向也相反。

因此在系统接口处必须显式转换，不能只交换 (x,y)。

---

## 19. 左手系与右手系

大多数机器人学和几何推导使用右手坐标系。

右手系满足：

$$
x\times y=z
$$
某些图形引擎或历史接口可能使用左手系。

如果混用，可能出现：

* 旋转方向反了；
* 法向量方向反了；
* 三角形 winding 反了；
* Quaternion 结果看起来镜像；
* 矩阵行列式为负。

检查一个变换是否混入镜像，可以看：

$$
\det(R)
$$
合法纯旋转应满足：

$$
\det(R)=1
$$
如果：

$$
\det(R)=-1
$$
通常说明发生了反射或手性转换。

---

## 20. 行向量与列向量约定

我们一直使用列向量：

$$
p'=Rp+t
$$
齐次形式：

$$
\tilde p'=T\tilde p
$$
但某些图形学系统使用行向量：

$$
p'=pR+t
$$
齐次变换也从右侧作用：

$$
\tilde p'=\tilde pT
$$
这时：

* 矩阵布局看起来可能转置；
* Composition 顺序会反过来；
* Translation 位于最后一列还是最后一行也会不同。

不能把列向量系统的矩阵直接复制到行向量系统中。

---

## 21. Row-major 与 Column-major 不等于行向量与列向量

这是另一个常见混淆。

`row-major` 和 `column-major` 主要描述：

> 矩阵在内存中的存储顺序。

而行向量/列向量描述：

> 数学上向量从哪一侧与矩阵相乘。

二者不是同一个概念。

例如一个库可以：

* 使用 column-major 内存；
* 但数学上仍支持列向量左乘；

也可以反过来。

不能通过内存布局推断几何 convention。

---

## 22. Quaternion 顺序检查

常见两种：

$$
[w,x,y,z]
$$
与：

$$
[x,y,z,w]
$$
例如：

* Eigen 构造函数常使用 `(w,x,y,z)`；
* `coeffs()` 的排列可能是 `(x,y,z,w)`；
* ROS geometry message 常见字段是 `x,y,z,w`。

如果直接把内存数组复制过去，可能得到一个完全错误但仍接近单位长度的 Quaternion。

最可靠的方法是：

> 按字段明确赋值，不要假设连续数组顺序一致。

---

## 23. Quaternion 表示方向也可能相反

一个 Quaternion 可能表示：

$$
{}^W R_B
$$
也可能表示：

$$
{}^B R_W
$$
二者互为逆：

$$
q_{BW}=q_{WB}^{-1}
$$
对于单位四元数：

$$
q^{-1}=q^*
$$
即虚部取负。

所以看到同一组姿态数据符号“似乎反了”，可能不是轴错，而是方向相反。

---

## 24. 时间戳也是坐标变换的一部分

严格来说，Frame Transform 不只依赖 Frame，还依赖时间：

$$
{}^W T_B(t)
$$
如果 Camera Frame 点来自时间：

$$
t_c
$$
但使用 Robot Pose：

$$
{}^W T_B(t_b)
$$
且：

$$
t_b\neq t_c
$$
那么即使空间变换链完全正确，结果仍然会错。

运动时常见表现：

* 点云拖影；
* 物体重影；
* 地图边缘双层；
* 速度越快误差越大；
* 静止时看起来正常。

这类问题本质上是：

> Temporal Extrinsic / Synchronization Error。

---

## 25. 如何用单位轴验证 Rotation？

假设你拿到一个不确定方向的旋转矩阵：

$$
R
$$
不要直接拿复杂点云测试。

先测试三个单位向量：

$$
e_x=
\begin{bmatrix}
1\\0\\0
\end{bmatrix},
\quad
e_y=
\begin{bmatrix}
0\\1\\0
\end{bmatrix},
\quad
e_z=
\begin{bmatrix}
0\\0\\1
\end{bmatrix}
$$
计算：

$$
Re_x,\quad Re_y,\quad Re_z
$$
结果分别是 (R) 的三列。

然后问：

* 输入 Frame 的前方映射到输出 Frame 的哪个方向？
* 左方映射到哪里？
* 上方映射到哪里？

这比看九个矩阵元素更直观。

---

## 26. 如何用原点验证 Translation？

齐次变换：

$$
T=
\begin{bmatrix}
R&t\\
0&1
\end{bmatrix}
$$
将输入 Frame 原点：

$$
p=
\begin{bmatrix}
0\\0\\0\\1
\end{bmatrix}
$$
变换后：

$$
Tp=
\begin{bmatrix}
t\\1
\end{bmatrix}
$$
因此：

> 输入 Frame 的原点在输出 Frame 中的位置，就是 Translation (t)。

这个测试可以快速验证：

$$
{}^A t_B
$$
到底是不是 (B) 原点在 (A) 中的位置。

---

## 27. 最小测试集

验证一个三维刚体变换时，建议至少测试四个点：

$$
p_0=
\begin{bmatrix}
0\\0\\0
\end{bmatrix}
$$
$$
p_x=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
$$
p_y=
\begin{bmatrix}
0\\1\\0
\end{bmatrix}
$$
$$
p_z=
\begin{bmatrix}
0\\0\\1
\end{bmatrix}
$$
结果应当分别是：

$$
Tp_0=t
$$
$$
Tp_x=t+r_x
$$
$$
Tp_y=t+r_y
$$
$$
Tp_z=t+r_z
$$
其中 (r_x,r_y,r_z) 是 Rotation Matrix 的列。

这四个点可以完整揭示：

* 原点位置；
* 三根轴方向；
* 是否有镜像；
* 是否变换反了。

---

## 28. Round-trip Test

若：

$$
p_A
=
{}^A T_B,p_B
$$
再反变换：

$$
\hat p_B
=
({}^A T_B)^{-1}p_A
$$
应该满足：

$$
\hat p_B\approx p_B
$$
即：

$$
\boxed{
T^{-1}(Tp)\approx p
}
$$
这能检查：

* 求逆是否正确；
* Translation 是否处理正确；
* Quaternion 是否归一；
* Matrix 是否合法。

但注意，它不能发现所有方向语义错误。

一个错误但内部自洽的 (T) 和 (T^{-1}) 仍然能通过 round-trip。

所以还必须配合单位轴与现实场景测试。

---

## 29. Composition Identity Test

应验证：

$$
T_{AB}T_{BC}\approx T_{AC}
$$
以及：

$$
T_{AB}T_{BA}\approx I
$$
如果 Frame Chain 来自多个模块，可以随机取简单点进行端到端验证：

$$
p_A
=
T_{AB}(T_{BC}p_C)
$$
与：

$$
p_A=T_{AC}p_C
$$
结果应一致。

---

## 30. 用一个“非对称测试点”

测试坐标变换时不要只使用：

$$
(0,0,0)
$$
或：

$$
(1,1,1)
$$
因为对称点可能掩盖轴交换错误。

更推荐：

$$
p=
\begin{bmatrix}
1\\2\\3
\end{bmatrix}
$$
或者：

$$
\begin{bmatrix}
0.3\\-1.7\\4.2
\end{bmatrix}
$$
非对称数值能更容易暴露：

* (x/y) 交换；
* 正负号错误；
* 行列转置；
* Translation 放错位置。

---

## 31. 如何判断变换是否乘反？

假设相机看到一个点：

$$
{}^C p=
\begin{bmatrix}
0\\0\\2
\end{bmatrix}
$$
它位于 Camera 前方 2 米。

已知 Camera 在 Base Frame 前方 0.2 米：

$$
{}^B t_C=
\begin{bmatrix}
0.2\\0\\0
\end{bmatrix}
$$
并假设 Camera (z) 轴对应 Base (x) 轴。

正确转换后，该点应大约位于 Base 前方：

$$
2.2\text{ m}
$$
如果结果变成：

* Camera 后方；
* Base 左侧；
* 距离变成 1.8 m；
* 原点方向相反；

就可以根据物理场景判断是否使用了逆变换或轴约定错误。

---

## 32. 一套系统化调试流程

遇到空间结果异常时，建议按以下顺序排查。

## 第一步：写清 Frame 定义

对于每个 Frame，明确：

```text
Origin
x axis
y axis
z axis
Right/left handed
Unit
Timestamp
```

不要只写 `camera frame`。

---

## 第二步：写清每个变换的语义

例如：

$$
{}^B T_C
$$
明确写成：

> 将 Camera coordinates 转换为 Base coordinates。

以及：

> Camera origin expressed in Base Frame。

---

## 第三步：画 Frame Chain

例如：

```text
Point_C
  ↓ T_BC
Point_B
  ↓ T_WB
Point_W
```

确保矩阵顺序与链一致。

---

## 第四步：使用原点与单位轴测试

不要先上真实点云。

---

## 第五步：检查逆变换

$$
T^{-1}
=
\begin{bmatrix}
R^T&-R^Tt\\
0&1
\end{bmatrix}
$$
避免手工只对 Translation 取负。

---

## 第六步：检查数值合法性

$$
R^TR\approx I
$$
$$
\det(R)\approx1
$$
$$
|q|\approx1
$$
---

## 第七步：检查时间同步

静止正常、运动异常时，优先怀疑时间戳。

---

## 第八步：再检查算法本身

很多时候做到前七步，算法已经无罪释放。

---

## 33. 常见错误现象与可能原因

| 现象              | 常见原因                         |
| --------------- | ---------------------------- |
| 整体左右镜像          | 手性、轴符号或反射矩阵                  |
| 整体旋转 (90^\circ) | Camera/Base 轴 convention 未转换 |
| 点出现在相机后方        | 使用了逆变换或 (z) 方向错误             |
| 静止正确，运动拖影       | 时间同步或 motion compensation    |
| 平移方向随姿态异常       | Local/World 增量混用             |
| Quaternion 偶发跳变 | (q/-q) 双覆盖未连续化               |
| 轨迹朝向正确但位置转着漂    | Translation 未先转换 Frame       |
| 逆变换后位置不对        | 使用 (-t) 而非 (-R^Tt)           |
| 点云比例或形状变形       | Rotation Matrix 不正交或包含缩放     |
| Euler 角突然跳跃     | 角度 wrap 或参数奇异性               |

---

## 34. 一个完整 Camera–Base 轴转换例子

假设：

Base Frame：

```text
x_B：前
y_B：左
z_B：上
```

Camera Optical Frame：

```text
x_C：右
y_C：下
z_C：前
```

我们希望构造：

$$
{}^B R_C
$$
即 Camera 各轴在 Base 中的表达。

Camera (x_C) 向右，对应 Base 的右方：

$$
x_C=-y_B
$$
Camera (y_C) 向下：

$$
y_C=-z_B
$$
Camera (z_C) 向前：

$$
z_C=x_B
$$
因此 ({}^B R_C) 的三列为：

$$
{}^B x_C=
\begin{bmatrix}
0\\-1\\0
\end{bmatrix}
$$
$$
{}^B y_C=
\begin{bmatrix}
0\\0\\-1
\end{bmatrix}
$$
$$
{}^B z_C=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
所以：

$$
\boxed{
{}^B R_C
=
\begin{bmatrix}
0&0&1\\
-1&0&0\\
0&-1&0
\end{bmatrix}
}
$$
检查：

$$
\det({}^B R_C)=1
$$
说明它是合法旋转，没有镜像。

---

## 35. 用列向量验证上面的矩阵

输入 Camera 前方单位向量：

$$
{}^C p=
\begin{bmatrix}
0\\0\\1
\end{bmatrix}
$$
则：

$$
{}^B p
=
{}^B R_C\,{}^C p
$$
结果就是矩阵第三列：

$$
{}^B p=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
即 Base 前方，符合预期。

Camera 右方：

$$
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$
映射为：

$$
\begin{bmatrix}
0\\-1\\0
\end{bmatrix}
$$
即 Base 右方，也符合预期。

这种单位轴测试比背矩阵可靠得多。

---

## 36. Frame Error 和 Calibration Error 的区别

假设点云整体旋转固定的 (90^\circ)。

这更像：

> Frame convention 错误。

假设点云整体只有几度的小偏差。

可能是：

> Extrinsic calibration error。

假设误差随时间变化。

可能是：

* Mechanical movement；
* Timestamp；
* Online calibration drift；
* Pose estimation error。

所以错误形态本身可以提供诊断线索。

---

## 37. Transform Tree 不等于所有 Pair 都直接标定

复杂机器人可能有：

```text
World
 └── Base
      ├── IMU
      ├── Camera
      └── LiDAR
```

通常只需要维护树边：

$$
{}^W T_B,\quad
{}^B T_I,\quad
{}^B T_C,\quad
{}^B T_L
$$
Camera 到 LiDAR 可以通过组合得到：

$$
{}^L T_C
=
({}^B T_L)^{-1}
{}^B T_C
$$
不需要为每对 Sensor 单独维护一份外参。

否则容易产生闭环不一致：

$$
T_{BC}T_{CL}T_{LB}\neq I
$$
---

## 38. Transform Tree 的一个隐患

如果同时维护：

$$
T_{BC}
$$
$$
T_{CL}
$$
$$
T_{LB}
$$
而它们来自不同标定结果，可能形成不一致环：

$$
T_{BC}T_{CL}T_{LB}\neq I
$$
这意味着：

> 从不同路径转换同一个点，会得到不同结果。

更可靠的做法是：

* 维护一个有向树；
* 或将多传感器外参作为图优化问题联合标定；
* 避免重复且独立维护互逆变换。

---

## 本章核心总结

第一：

$$
{}^A T_B
$$
表示 Frame (B) 在 Frame (A) 中的 Pose，同时将 (B) 坐标转换为 (A) 坐标。

第二：

$$
{}^A p
=
{}^A T_B\,{}^B p
$$
上标是输出 Frame，下标是输入 Frame。

第三：

World-to-Camera 与 Camera-to-World 互为逆，视觉投影通常需要 World-to-Camera。

第四：

Active Rotation、Passive Frame Change、Left/Right Multiplication 必须明确区分。

第五：

坐标轴 convention、手性、Quaternion 顺序、行列向量约定和时间戳，都是变换语义的一部分。

第六：

调试变换最有效的方法不是盯矩阵，而是使用：

* 原点；
* 三个单位轴；
* 非对称测试点；
* Round-trip；
* Frame Chain。

---

## 思考题与参考答案

## 思考题 1

已知：

$$
{}^W T_C
$$
表示 Camera 在 World 中的 Pose。要把 World Point 转到 Camera Frame，应使用什么？

<details>

<summary>参考答案</summary>
应使用逆变换：

$$
{}^C T_W
=
({}^W T_C)^{-1}
$$
因此：

$$
{}^C p
=
({}^W T_C)^{-1}{}^W p
$$
因为 ({}^W T_C) 的作用方向是 Camera → World。

</details>

---

## 思考题 2

OpenCV 投影公式：

$$
p_C=Rp_W+t
$$
中的 (t) 是否是 Camera 在 World 中的位置？

<details>

<summary>参考答案</summary>
通常不是。

这里的 (R,t) 组成 World-to-Camera 变换：

$$
{}^C T_W
$$
Camera Center 在 World 中为：

$$
C_W=-R^Tt
$$
只有在特殊姿态下，(t) 才可能与 Camera Position 存在简单数值关系。

</details>

---

## 思考题 3

为什么验证 Rotation Matrix 时，测试单位向量比直接观察九个元素更可靠？

<details>

<summary>参考答案</summary>
矩阵的三列直接表示输入 Frame 的三个单位轴在输出 Frame 中的方向。

通过测试：

$$
Re_x,\ Re_y,\ Re_z
$$
可以直接用物理语言判断：

* 前方映射到哪里；
* 左方映射到哪里；
* 上方映射到哪里。

这更容易发现轴交换、符号错误和逆变换问题。

</details>

---

## 思考题 4

一个点云静止时对齐正常，但机器人运动时出现明显双层和拖影。优先怀疑什么？

<details>

<summary>参考答案</summary>
优先怀疑时间同步或运动补偿，而不是固定外参。

因为固定 Extrinsic Error 在静止和运动时通常都会存在。

只有运动时显著恶化，往往说明 Sensor Data 与 Pose 使用了不同时间戳：

$$
T(t_{\text{pose}})
\neq
T(t_{\text{sensor}})
$$

</details>

---

## 思考题 5

为什么：

$$
T_{AB}T_{BC}
$$
有意义，而：

$$
T_{BC}T_{AB}
$$
一般没有相同几何意义？

<details>

<summary>参考答案</summary>
$$
T_{AB}
$$
把 (B) 坐标转换为 (A)。

$$
T_{BC}
$$
把 (C) 坐标转换为 (B)。

因此：

$$
T_{AB}T_{BC}
$$
形成：

```text
C → B → A
```

中间 Frame 可以对接。

反过来的顺序中 Frame 不能正确衔接，而且矩阵作用顺序也改变，因此结果通常错误。

</details>

---

## 思考题 6

已知 Camera Optical Frame：

```text
x 右
y 下
z 前
```

Base Frame：

```text
x 前
y 左
z 上
```

Camera 前方单位向量在 Base Frame 中是什么？

<details>

<summary>参考答案</summary>
Camera 前方是：

$$
{}^C p=
\begin{bmatrix}
0\\0\\1
\end{bmatrix}
$$
Camera 的 (z_C) 轴对应 Base 的 (x_B) 轴，因此：

$$
{}^B p=
\begin{bmatrix}
1\\0\\0
\end{bmatrix}
$$

</details>

---

## 思考题 7

为什么一个错误但自洽的 Transform 仍可能通过 Round-trip Test？

<details>

<summary>参考答案</summary>
假设错误变换为 (\tilde T)。

只要逆矩阵正确计算：

$$
\tilde T^{-1}\tilde T=I
$$
那么：

$$
\tilde T^{-1}(\tilde Tp)=p
$$
仍然成立。

Round-trip 只能验证变换和其逆在代数上自洽，不能证明它与真实 Frame 语义一致。

因此还需要使用单位轴、现实方向和已知几何位置验证。

</details>

---

## 思考题 8

为什么变量名 `camera_extrinsic` 不足以确定矩阵方向？

<details>

<summary>参考答案</summary>
“Extrinsic”只说明它描述不同 Frame 的相对关系，但没有说明：

* Camera-to-Base；
* Base-to-Camera；
* Camera-to-World；
* World-to-Camera。

必须检查矩阵实际作用公式，或采用明确名称：

$$
T_{BC},\quad T_{CB}
$$
并写清输入和输出 Frame。

</details>

---

下一章可以进入：

## Chapter 31 — Pose Uncertainty on (SE(3))

我们会把 Part II 的概率状态估计与 Part III 的空间几何真正合并起来：

* 为什么不能简单给 (4\times4) Pose Matrix 的 16 个元素定义协方差；
* 6 维 Pose Error 应该在哪个 Tangent Space 中表达；
* 左不变误差与右不变误差；
* Rotation–Translation Cross-Covariance；
* 如何通过 Adjoint 转换 Pose Covariance；
* 为什么“同一个 Pose 协方差”脱离 Frame 和扰动约定没有完整意义。

## 排版修订记录

迁移时将原记录的方括号公式、误解析的等号和矩阵换行恢复为 LaTeX；保留原有推导与例题。迁移不代表全面技术审校。
