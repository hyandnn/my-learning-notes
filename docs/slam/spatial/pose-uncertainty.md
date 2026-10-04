---
title: SE(3) 上的位姿不确定性
description: 位姿协方差应定义在哪里，怎样随扰动约定与坐标系传播？
icon: book-open
course: Robot Perception & SLAM
part: Part III Spatial State Estimation
week: 3
chapter: 31
chapter_type: lecture
status: organized
tags: [slam, geometry, state-estimation]
---

# SE(3) 上的位姿不确定性

## 本章目标

理解六维局部误差、左右扰动、Adjoint 与位姿协方差传播。

## 前置知识

[Gaussian 与协方差](../probabilistic/gaussian.md)、[三维位姿与 SE(3)](se3.md)、[变换约定](transform-debugging.md)。

## 定义与假设

令 T = {}^A T_B 把 B 系坐标映射到 A 系；扰动排列为 [δρ, δφ]，平移单位 m，旋转单位 rad。局部 Gaussian 与一阶传播只适用于名义位姿附近；Exp 的六维输入统一理解为经 hat 映射后的矩阵指数，Log 输出六维坐标。

## 位姿有不确定性时，协方差究竟应该定义在哪里？

前面两部分终于在这里合流：

- Part II：Belief、Covariance、Kalman Filter；
- Part III：Rotation、Pose、$$SO(3)$$、$$SE(3)$$。

我们已经知道，普通欧氏状态可以写成：

$$
x\sim\mathcal N(\mu,P)
$$

但三维 Pose 是：

$$
T\in SE(3)
$$

它是一个 $$4\times4$$ 刚体变换矩阵，不是普通向量。

因此本章的核心问题是：

> **一个 Pose 的 Gaussian Belief 到底是什么意思？**

---

## 1. 为什么不能直接给 $$T$$ 的 16 个元素定义协方差？

一个三维 Pose：

$$
T= \begin{bmatrix} R&t\\ 0&1 \end{bmatrix}
$$

表面上包含 16 个矩阵元素。

但真正只有：

$$
6\text{ DoF}
$$

其中：

- Translation：3 DoF；
- Rotation：3 DoF。

如果直接把矩阵展开成 16 维向量：

$$
\operatorname{vec}(T)
$$

再定义：

$$
P_T\in\mathbb R^{16\times16}
$$

会有几个问题。

第一，最后一行固定为：

$$
[0,0,0,1]
$$

不应该存在随机变化。

第二，Rotation Matrix 的 9 个元素受到：

$$
R^TR=I,\qquad \det(R)=1
$$

约束，不能独立变化。

第三，普通高斯扰动可能让：

$$
R+\Delta R
$$

不再属于 $$SO(3)$$。

所以：

$$
\boxed{ \text{Pose uncertainty cannot be modeled as independent noise on matrix entries} }
$$

更合理的方式是：

> Pose 保存在 $$SE(3)$$ 上，不确定性定义在它附近的六维 Tangent Space 中。

---

## 2. Pose Belief 的基本形式

假设平均或名义 Pose 为：

$$
\bar T\in SE(3)
$$

真实 Pose 位于它附近。

我们用六维小扰动：

$$
\delta\xi = \begin{bmatrix} \delta\rho\\ \delta\phi \end{bmatrix} \in\mathbb R^6
$$

描述真实 Pose 与名义 Pose 的差异。

然后假设：

$$
\boxed{ \delta\xi\sim\mathcal N(0,P) }
$$

其中：

$$
P\in\mathbb R^{6\times6}
$$

这才是 Pose Covariance。

因此所谓：

$$
T\sim\mathcal N(\bar T,P)
$$

并不是普通意义上的矩阵高斯分布。

更准确的含义是：

> Pose 以 $$\bar T$$ 为中心，其局部六维误差服从 Gaussian。

---

## 3. 但局部扰动加在哪一边？

这里马上出现两个选择。

### 右扰动

$$
\boxed{ T = \bar T\operatorname{Exp}(\delta\xi^\wedge) }
$$

### 左扰动

$$
\boxed{ T = \operatorname{Exp}(\delta\xi^\wedge)\bar T }
$$

两者都合法，但含义不同。

因为：

$$
SE(3)
$$

不可交换，所以：

$$
\bar T\operatorname{Exp}(\delta\xi) \neq \operatorname{Exp}(\delta\xi)\bar T
$$

---

## 4. 右扰动的含义

右扰动：

$$
T = \bar T\operatorname{Exp}(\delta\xi^\wedge)
$$

可以理解为：

> 在当前 Pose 的局部 Body Frame 中，对名义 Pose 施加一个小误差。

假设机器人朝世界 $$y$$ 方向。

若：

$$
\delta\rho = \begin{bmatrix} 1\\0\\0 \end{bmatrix}
$$

在右扰动语义下，它通常表示：

> 沿机器人自己的局部 $$x$$ 轴前进。

因此，实际在世界中可能沿 $$y$$ 方向移动。

所以右扰动中的 Translation Error 通常是：

> Local / Body-frame error。

---

## 5. 左扰动的含义

左扰动：

$$
T = \operatorname{Exp}(\delta\xi^\wedge)\bar T
$$

可以理解为：

> 在外部 Reference Frame 中，对名义 Pose 施加小误差。

同样：

$$
\delta\rho = \begin{bmatrix} 1\\0\\0 \end{bmatrix}
$$

通常表示：

> 沿参考系或世界系的 $$x$$ 方向平移。

所以左扰动中的误差通常更接近：

> Global / Reference-frame error。

不过具体名称仍取决于 Pose 的方向定义，例如 $$T_{WB}$$ 还是 $$T_{BW}$$。不能只背“左等于世界、右等于局部”，必须结合实际变换语义。

---

## 6. 同一个 Pose 可以有不同 Covariance

假设名义 Pose 完全相同：

$$
\bar T
$$

但一个系统使用右扰动：

$$
T=\bar T\operatorname{Exp}(\delta\xi_R)
$$

另一个系统使用左扰动：

$$
T=\operatorname{Exp}(\delta\xi_L)\bar T
$$

那么：

$$
\delta\xi_R
$$

与：

$$
\delta\xi_L
$$

不是同一个随机向量。

在相容的局部 Log 分支内，由共轭与指数映射的恒等式得到：

$$
\boxed{ \delta\xi_L = \operatorname{Ad}_{\bar T} \delta\xi_R }
$$

因此协方差满足：

$$
\boxed{ P_L = \operatorname{Ad}_{\bar T} P_R \operatorname{Ad}_{\bar T}^T }
$$

这说明：

> **Pose Covariance 脱离扰动定义和表达 Frame，没有完整意义。**

只给出一个 $$6\times6$$ 矩阵，而不说明：

- Pose 方向；
- 左扰动还是右扰动；
- 分量排列；
- Translation/Rotation 的表达 Frame；

这个协方差基本只完成了一半的信息传递。

---

## 7. 六维 Pose Covariance 长什么样？

采用：

$$
\delta\xi= \begin{bmatrix} \delta\rho\\ \delta\phi \end{bmatrix}
$$

则：

$$
P = \begin{bmatrix} P_{\rho\rho}&P_{\rho\phi}\\ P_{\phi\rho}&P_{\phi\phi} \end{bmatrix}
$$

其中每个块都是 $$3\times3$$。

---

### Translation Covariance

$$
P_{\rho\rho}
$$

描述三个平移方向上的不确定性及相关性。

---

### Rotation Covariance

$$
P_{\phi\phi}
$$

描述三个小旋转方向上的不确定性及相关性。

它的单位通常是：

$$
\text{rad}^2
$$

不是度平方，除非系统明确这样定义。

---

### Rotation–Translation Cross-Covariance

$$
P_{\rho\phi}
$$

描述：

> Translation Error 与 Rotation Error 如何相关。

这个交叉项非常重要，不能轻易全部设为零。

---

## 8. 为什么 Rotation Error 会与 Translation Error 相关？

假设机器人通过视觉观测一个远处 Landmark。

某种几何情况下，系统可能难以区分：

- Camera 向侧面平移了一点；
- Camera 朝向发生了一点旋转。

这两种变化都可能在图像中产生相似的 Pixel Motion。

于是估计误差可能表现为：

```
Yaw 偏大时
横向 Translation 也倾向偏小
```

这就是 Rotation–Translation Correlation。

再例如连续里程计中，一个轻微朝向误差会逐渐产生横向位置误差。

所以：

$$
P_{\rho\phi}\neq0
$$

往往是正常现象。

---

## 9. 一个小角度误差如何影响空间点？

名义 Pose：

$$
\bar T= \begin{bmatrix} \bar R&\bar t\\ 0&1 \end{bmatrix}
$$

点：

$$
p
$$

变换后：

$$
p'=\bar Rp+\bar t
$$

假设存在小旋转误差：

$$
\delta\phi
$$

采用一种局部近似：

$$
R\approx\bar R(I+\delta\phi^\wedge)
$$

则：

$$
Rp \approx \bar Rp+\bar R(\delta\phi\times p)
$$

利用：

$$
\delta\phi\times p = -p^\wedge\delta\phi
$$

得到：

$$
\delta p' \approx -\bar Rp^\wedge\delta\phi+\delta t
$$

具体形式会随左/右扰动改变，但共同结论是：

> Rotation Error 会被点到旋转中心的杠杆臂放大成 Position Error。

点越远，这种影响通常越大。

---

## 10. Pose Covariance 与 Point Covariance 的传播

假设一个点在局部 Frame 中固定：

$$
p_B
$$

通过 Pose：

$$
p_A=Rp_B+t
$$

Pose 有六维小误差：

$$
\delta\xi \sim\mathcal N(0,P_T)
$$

点本身也可能有测量不确定性：

$$
P_p
$$

对函数：

$$
p_A=f(T,p_B)
$$

线性化后：

$$
\delta p_A \approx J_T\delta\xi + J_p\delta p_B
$$

所以：

$$
\boxed{ P_{p_A} \approx J_TP_TJ_T^T + J_pP_pJ_p^T }
$$

若二者相关，还需要交叉协方差项。

其中通常：

$$
J_p=R
$$

而 $$J_T$$ 会包含：

- Translation 部分；
- 点位置对应的 Rotation Lever Arm。

因此远处点对 Orientation Uncertainty 更敏感。

---

## 11. 一个简单的 Jacobian

采用左侧小扰动的一种常见形式：

$$
T'=\operatorname{Exp}(\delta\xi^\wedge)T
$$

其中：

$$
\delta\xi= \begin{bmatrix} \delta\rho\\ \delta\phi \end{bmatrix}
$$

对于已经位于输出 Frame 的点：

$$
p'=Rp+t
$$

小扰动作用后近似：

$$
p'_{\text{new}} \approx p' + \delta\rho + \delta\phi\times p'
$$

又因为：

$$
\delta\phi\times p' = -p'^\wedge\delta\phi
$$

所以：

$$
\delta p' = \begin{bmatrix} I&-p'^\wedge \end{bmatrix} \begin{bmatrix} \delta\rho\\ \delta\phi \end{bmatrix}
$$

因此：

$$
\boxed{ J_T = \begin{bmatrix} I&-p'^\wedge \end{bmatrix} }
$$

这个结构在：

- ICP；
- Bundle Adjustment；
- Calibration；
- Pose Uncertainty Propagation；

中经常出现。

---

## 12. 为什么相同角度方差在不同距离下意义不同？

假设 Orientation 标准差为：

$$
\sigma_\theta=1^\circ\approx0.0175\text{ rad}
$$

一个点距离旋转中心：

$$
r=0.1\text{ m}
$$

对应侧向位置误差量级：

$$
r\sigma_\theta \approx1.75\text{ mm}
$$

如果点距离：

$$
r=10\text{ m}
$$

则：

$$
r\sigma_\theta \approx17.5\text{ cm}
$$

同一个 Orientation Covariance，对远处空间点的影响可以大两个数量级。

所以不能简单说：

> “旋转误差只有 1 度，很小。”

它是否可接受，取决于下游几何尺度。

---

## 13. Adjoint 如何转换 Pose Error？

假设：

$$
{}^A T_B=T
$$

同一个小扰动在 $$B$$ Frame 中表达为：

$$
\delta\xi_B
$$

在 $$A$$ Frame 中表达为：

$$
\boxed{ \delta\xi_A = \operatorname{Ad}_T \delta\xi_B }
$$

若采用排列：

$$
\delta\xi= \begin{bmatrix} \delta\rho\\ \delta\phi \end{bmatrix}
$$

则：

$$
\operatorname{Ad}_T = \begin{bmatrix} R&t^\wedge R\\ 0&R \end{bmatrix}
$$

展开：

$$
\delta\phi_A = R\delta\phi_B
$$

$$
\delta\rho_A = R\delta\rho_B + t\times R\delta\phi_B
$$

第二项非常关键。

它表示：

> 改变 Pose Error 的参考原点时，Rotation Error 会产生附加 Translation Error。

---

## 14. 为什么只旋转 $$P_{\rho\rho}$$ 不够？

有人转换 Pose Covariance 时可能这样做：

$$
P'_{\rho\rho}=RP_{\rho\rho}R^T
$$

$$
P'_{\phi\phi}=RP_{\phi\phi}R^T
$$

然后忽略其他部分。

这只适用于非常特殊的情况。

完整变换应为：

$$
\boxed{ P_A = \operatorname{Ad}_T P_B \operatorname{Ad}_T^T }
$$

因为：

- Rotation Error 会影响 Translation；
- Cross-Covariance 也需要变化；
- 改变参考原点与只改变轴方向不是一回事。

如果两个 Frame 原点不同，只做块对角旋转通常是不完整的。

---

## 15. 一个纯 Rotation Error 的例子

假设在 Frame $$B$$ 中：

$$
\delta\rho_B=0
$$

但存在：

$$
\delta\phi_B\neq0
$$

转换到一个原点相距 $$t$$ 的 Frame $$A$$：

$$
\delta\rho_A = t\times R\delta\phi_B
$$

所以在 $$A$$ 中，误差不再是“纯旋转”。

这是因为：

> 绕旧原点发生的小旋转，会让新原点的位置发生摆动。

这和刚体上不同点的速度不同是同一个物理事实。

---

## 16. Pose Composition 的协方差如何传播？

假设：

$$
T_{AC}=T_{AB}T_{BC}
$$

并且两个变换都有小误差。

采用某一种统一扰动约定后，可以写出近似：

$$
\delta\xi_{AC} \approx J_1\delta\xi_{AB} + J_2\delta\xi_{BC}
$$

因此：

$$
P_{AC} \approx J_1P_{AB}J_1^T + J_2P_{BC}J_2^T
$$

若二者相关，还需要加入交叉项。

在常见右扰动约定下，Jacobian 中通常会出现相应的 Adjoint。具体位置取决于误差定义。

因此工程上不能只写：

$$
P_{AC}=P_{AB}+P_{BC}
$$

因为两个误差：

- 表达 Frame 可能不同；
- Rotation 与 Translation 耦合；
- 前一段 Pose 会改变后一段误差的方向。

---

## 17. 为什么连续里程计协方差不是简单逐项累加？

假设每一帧 Odometry 增量都有：

$$
P_{\Delta T}
$$

机器人不断组合：

$$
T_k=T_{k-1}\Delta T_k
$$

如果每次只是：

$$
P_k=P_{k-1}+P_{\Delta T}
$$

会忽略：

- 机器人朝向改变后，局部前后方向映射到不同世界方向；
- Orientation Error 对后续 Translation 的放大；
- 交叉协方差的形成；
- 每次增量误差 Frame 不同。

正确做法需要根据 Composition Jacobian 或 Adjoint，把每一段局部误差传播到统一 Tangent Space。

---

## 18. Pose Covariance 的单位问题

六维误差：

$$
\delta\xi= \begin{bmatrix} \delta x\\ \delta y\\ \delta z\\ \delta\phi_x\\ \delta\phi_y\\ \delta\phi_z \end{bmatrix}
$$

前三维单位：

$$
\text{m}
$$

后三维单位：

$$
\text{rad}
$$

因此协方差块单位分别为：

$$
P_{\rho\rho}:\text{m}^2
$$

$$
P_{\phi\phi}:\text{rad}^2
$$

$$
P_{\rho\phi}:\text{m}\cdot\text{rad}
$$

这会带来一个问题：

> 不能简单比较六维协方差矩阵各元素的数值大小，就说哪个状态更不确定。

例如：

$$
0.01\text{ m}^2
$$

和：

$$
0.01\text{ rad}^2
$$

物理意义完全不同。

---

## 19. 六维 Pose Error 的“大小”如何定义？

直接使用：

$$
\|\delta\xi\|^2 = \|\delta\rho\|^2+\|\delta\phi\|^2
$$

把米平方和弧度平方相加，缺少自然统一尺度。

在优化中通常使用信息矩阵：

$$
\Omega=P^{-1}
$$

定义：

$$
\boxed{ e^T\Omega e }
$$

这样 Translation 和 Rotation 的相对权重由 Measurement Uncertainty 决定。

或者人为引入尺度参数：

$$
\|\delta\rho\|^2 + \lambda\|\delta\phi\|^2
$$

但 $$\lambda$$ 必须有任务或统计依据。

---

## 20. 为什么不能说“这个 Pose Covariance 是 0.1”？

因为 Pose Uncertainty 至少需要说明：

- Translation 哪些方向？
- Rotation 哪些方向？
- 是否存在相关性？
- 在哪个 Frame？
- 关于哪个参考点？
- 使用左扰动还是右扰动？
- 单位是什么？

一个标量无法完整描述这些结构。

即使取：

$$
\operatorname{tr}(P)
$$

也会混合米平方与弧度平方，通常缺乏明确物理意义。

---

## 21. Pose Covariance Ellipsoid

Translation Covariance：

$$
P_{\rho\rho}
$$

可以画成三维椭球。

它表达：

- 椭球长轴：最不确定平移方向；
- 短轴：最确定方向；
- 朝向：Translation Error Correlation。

Rotation Covariance：

$$
P_{\phi\phi}
$$

也可以在小角度 Tangent Space 中画成旋转误差椭球。

但完整六维 Pose Covariance 无法直接在普通三维图中完整显示。

通常需要分别展示：

- Position Covariance Ellipsoid；
- Orientation 标准差；
- Cross-Correlation 指标。

---

## 22. 左不变误差与右不变误差

假设真实 Pose：

$$
T
$$

估计 Pose：

$$
\hat T
$$

常见两种误差定义。

### 左不变误差

一种常见写法：

$$
\boxed{ \eta_L = \hat T^{-1}T }
$$

如果同时左乘同一个全局变换 $$G$$：

$$
\hat T\rightarrow G\hat T,\qquad T\rightarrow GT
$$

则：

$$
(G\hat T)^{-1}(GT) = \hat T^{-1}T
$$

误差不变。

因此它对全局左侧坐标变化不敏感。

---

### 右不变误差

另一种常见写法：

$$
\boxed{ \eta_R = T\hat T^{-1} }
$$

如果同时右乘同一个变换 $$G$$：

$$
T\rightarrow TG,\qquad \hat T\rightarrow\hat TG
$$

则误差保持不变。

> 修订说明：原草稿把左右不变误差的名称写反。本章按保持误差不变的群作用命名：左乘不变的是左不变误差，右乘不变的是右不变误差。右扰动对应的局部误差不应因此被叫作右不变误差。

---

## 23. 为什么不变误差重要？

普通欧氏误差：

$$
x-\hat x
$$

在改变参考 Frame 后，结构可能发生复杂变化。

Lie Group 上的不变误差能够让：

- Error Definition；
- Dynamics；
- Jacobian；

更好地尊重系统对称性。

这也是：

> Invariant EKF

背后的核心思想之一。

它不是简单更换一套符号，而是选择一种与系统几何结构更匹配的 Error State。

---

## 24. Error-State Kalman Filter 的基本思想

假设系统名义状态中包含：

- Position；
- Velocity；
- Quaternion；
- Bias。

Quaternion 本身有 4 个分量和单位约束。

如果直接把 Quaternion 四个分量放入普通 EKF，并用加法更新，会很别扭。

Error-State KF 通常做：

### 名义状态

保存完整非线性状态：

$$
\hat q,\hat p,\hat v,\ldots
$$

### 误差状态

维护小误差：

$$
\delta x = \begin{bmatrix} \delta p\\ \delta v\\ \delta\phi\\ \delta b \end{bmatrix}
$$

并假设：

$$
\delta x\sim\mathcal N(0,P)
$$

滤波更新后，将误差注入名义状态：

$$
q\leftarrow q\otimes\operatorname{Exp}(\delta\phi)
$$

$$
p\leftarrow p+\delta p
$$

随后将误差状态重置到零附近。

这就是 Pose Tangent-space Uncertainty 的直接应用。

---

## 25. 为什么误差状态适合 Gaussian？

完整 Rotation State 位于：

$$
SO(3)
$$

不是欧氏空间。

但在当前姿态附近，小旋转误差：

$$
\delta\phi\in\mathbb R^3
$$

位于局部 Tangent Space。

只要不确定性不太大，就可以合理近似：

$$
\delta\phi\sim\mathcal N(0,P_\phi)
$$

因此：

> Gaussian 不直接放在整个 Rotation Manifold 上，而放在局部小误差空间中。

这正是 EKF 与 Lie Group 结合的核心逻辑。

---

## 26. 误差注入后为什么要重置 Covariance？

滤波更新得到：

$$
\delta\hat x
$$

将其注入名义状态后：

$$
\hat T\leftarrow \hat T\operatorname{Exp}(\delta\hat\xi)
$$

新的误差坐标系中心已经发生变化。

原来的 Covariance 是围绕旧线性化点定义的。

因此严格来说，需要通过 Reset Jacobian：

$$
G_{\text{reset}}
$$

重新表达协方差：

$$
\boxed{ P\leftarrow G_{\text{reset}} P G_{\text{reset}}^T }
$$

小误差下它可能接近单位矩阵，但在高精度 ESKF 中不能完全忽略。

---

## 27. 一个 Pose Covariance 接口应该说明什么？

理想的接口文档至少应说明：

```
Pose direction:
T_WB or T_BW

Error convention:
left perturbation or right perturbation

Error ordering:
[translation, rotation] or [rotation, translation]

Translation unit:
meters

Rotation unit:
radians

Error expression frame:
world, body, sensor, or another frame

Reference point:
base origin, camera origin, IMU origin...

Covariance layout:
row-major storage is irrelevant mathematically, but array order must be clear
```

否则即使收到合法的 $$6\times6$$ 数值矩阵，也可能完全错误地使用。

---

## 28. Pose Inversion 后 Covariance 怎么变？

已知：

$$
T^{-1}
$$

如果 Pose 有误差，求逆后的误差不会简单保持不变。

局部线性化后，需要使用 Inversion Jacobian，通常与：

$$
-\operatorname{Ad}_T
$$

或其逆相关，具体取决于左右扰动约定。

因此不能简单认为：

$$
P_{T^{-1}}=P_T
$$

即使两者表达同一个物理不确定性，它们位于不同的 Tangent Space 和 Frame 中，数值一般不同。

---

## 29. 同一个物理 Pose，在 Camera 原点和 Base 原点的 Covariance 不同

假设 Camera 与 Base 之间存在固定杠杆臂：

$$
t_{BC}
$$

Base Orientation 存在不确定性。

在 Base 原点处，这主要表现为 Rotation Error。

但 Camera 位于离旋转中心一定距离的位置。

同一个 Rotation Error 会让 Camera Position 摆动。

所以 Camera Pose 的 Translation Covariance 会变大，并且出现 Translation–Rotation Cross-Covariance。

这不是系统凭空增加了不确定性，而是：

> 同一个刚体误差在不同参考点下呈现不同的分量结构。

---

## 30. 本章与 Part II 的最终连接

Part II 中我们写：

$$
x\sim\mathcal N(\mu,P)
$$

现在对于 Pose，更准确的是：

$$
\boxed{ T = \bar T\operatorname{Exp}(\delta\xi^\wedge), \qquad \delta\xi\sim\mathcal N(0,P) }
$$

或者左扰动版本。

所以：

- $$\bar T$$：Manifold 上的名义 Pose；
- $$\delta\xi$$：Tangent Space 中的局部误差；
- $$P$$：局部误差的 Covariance；
- Exp：把误差注入 Pose；
- Log：把相对 Pose 转换为局部误差。

这就是：

> Probabilistic State Estimation on Lie Groups。

---

## 补充推导：统一右扰动下的组合与求逆

设两个名义变换为 A、B，真实变换为 A Exp(a^∧)、B Exp(b^∧)，误差 a、b 都是六维列向量。由共轭恒等式与一阶 BCH 展开：

$$
\begin{aligned}
T_{AC}&=A\operatorname{Exp}(a^\wedge)B\operatorname{Exp}(b^\wedge)\\
&=AB\operatorname{Exp}((\operatorname{Ad}_{B^{-1}}a)^\wedge)\operatorname{Exp}(b^\wedge),\\
c&\approx\operatorname{Ad}_{B^{-1}}a+b.
\end{aligned}
$$

因此 J₁ = Ad(B⁻¹)、J₂ = I。若 a、b 独立：

$$
P_{AC}\approx\operatorname{Ad}_{B^{-1}}P_{AB}\operatorname{Ad}_{B^{-1}}^T+P_{BC}.
$$

若交叉协方差为 C = Cov(a,b)，还需加上 J₁C + CᵀJ₁ᵀ。求逆则有：

$$
(A\operatorname{Exp}(a^\wedge))^{-1}
=\operatorname{Exp}(-a^\wedge)A^{-1}
=A^{-1}\operatorname{Exp}((-\operatorname{Ad}_Aa)^\wedge).
$$

故同样采用右扰动表示逆位姿时，误差为 −Ad(A)a，协方差为 Ad(A)P Ad(A)ᵀ。

### 推导得到什么

组合前要把两个局部误差放进同一坐标表示；求逆也会改变误差坐标。上述协方差传播使用小误差近似，不能直接推广到任意大范围的 Gaussian 位姿分布。

### 在 SLAM 中怎么用

可用于里程计增量累积、外参变换链与逆位姿接口。右扰动中的 δρ 不是世界系位置误差；左扰动的平移坐标也包含旋转绕参考原点产生的耦合。

> 修订说明：补充了草稿中仅给通式的右扰动组合与求逆 Jacobian；点与组合协方差传播统一标为一阶近似。误差注入后的协方差重置 Jacobian 随误差定义而变，草稿未给完整 ESKF 动力学，本章不扩展为完整 ESKF 推导。


## 本章核心总结

第一：

> Pose Covariance 不应该定义在 $$4\times4$$ 矩阵的 16 个独立元素上，而应定义在六维局部 Tangent Space 中。

第二：

$$
T=\bar T\operatorname{Exp}(\delta\xi)
$$

与：

$$
T=\operatorname{Exp}(\delta\xi)\bar T
$$

对应不同扰动语义。

第三：

$$
P= \begin{bmatrix} P_{\rho\rho}&P_{\rho\phi}\\ P_{\phi\rho}&P_{\phi\phi} \end{bmatrix}
$$

中的交叉协方差表达 Translation 与 Rotation Error 的相关性。

第四：

Pose Error 或 Covariance 变换 Frame 时，需要使用：

$$
\operatorname{Ad}_T
$$

而不能只分别旋转平移块和旋转块。

第五：

> Pose Covariance 脱离 Pose 方向、扰动约定、表达 Frame、参考原点和单位，没有完整意义。

第六：

> Error-State Filter 通过在 Tangent Space 中维护 Gaussian Error，把 Kalman Filter 与 $$SO(3)/SE(3)$$ 结合起来。

---

## 思考题与参考答案

### 思考题 1

为什么不能给 Rotation Matrix 的 9 个元素分别添加独立 Gaussian Noise？

**参考答案**

因为 Rotation Matrix 的元素不是独立变量，必须满足：

$$
R^TR=I,\qquad\det(R)=1
$$

对九个元素独立加噪后，矩阵通常不再属于 $$SO(3)$$，会混入缩放、剪切或反射。

更合理的是在三维局部旋转向量：

$$
\delta\phi\in\mathbb R^3
$$

上定义 Gaussian，再通过 Exp 映射到合法 Rotation。


---

### 思考题 2

两个系统都给出同一个 $$6\times6$$ Pose Covariance，能否认为它们表达相同的不确定性？

**参考答案**

不能。

还必须确认：

- 一个使用左扰动还是右扰动；
- Translation 和 Rotation 的排列；
- 误差在哪个 Frame 中表达；
- Pose 是 $$T_{WB}$$ 还是 $$T_{BW}$$；
- Rotation 单位是否为 rad；
- 参考原点是否相同。

相同数值矩阵在不同约定下可能表示完全不同的物理不确定性。


---

### 思考题 3

为什么一个纯 Orientation Uncertainty 转换到远离旋转中心的 Sensor Frame 后，会产生 Position Uncertainty？

**参考答案**

Sensor 与旋转中心之间存在杠杆臂 $$t$$。

小角度误差会造成 Sensor 原点位置变化：

$$
\delta p \approx \delta\phi\times t
$$

因此在新参考点下，原来的纯 Rotation Error 会表现为 Translation Error。

Adjoint 中的：

$$
t^\wedge R
$$

正是描述这种耦合。


---

### 思考题 4

为什么不能简单将两个独立 Pose Increment 的协方差相加？

<details>

<summary>参考答案</summary>
因为两个 Pose Increment 的误差可能：

- 在不同局部 Frame 中表达；
- 经过前一个 Pose 的 Rotation 后方向发生变化；
- Rotation Error 会影响后续 Translation；
- 产生 Translation–Rotation Cross-Covariance。

必须先通过 Composition Jacobian 或 Adjoint 将误差传播到同一个 Tangent Space，再进行协方差合成。

</details>

---

### 思考题 5

为什么 Error-State Kalman Filter 不直接把 Quaternion 的四个分量作为四维普通误差？

**参考答案**

Quaternion 有单位长度约束：

$$
\|q\|=1
$$

并且只有 3 DoF。

四维普通加性误差：

- 包含冗余方向；
- 不保证更新后仍为单位 Quaternion；
- 不符合三维 Rotation 的局部几何结构。

ESKF 使用三维小旋转误差：

$$
\delta\phi
$$

并通过 Quaternion 乘法或 Exp 注入姿态。


---

### 思考题 6

如果一个 Pose 的 Position Covariance 很小，是否说明所有由该 Pose 变换出的空间点位置都很准确？

**参考答案**

不一定。

即使 Position Covariance 很小，只要 Orientation Covariance 不小，远离旋转中心的点仍可能具有很大的位置误差：

$$
\delta p \approx -\left(Rp\right)^\wedge\delta\phi
$$

点越远，Orientation Error 产生的位置偏差通常越大。


---

### 思考题 7

为什么 Pose Covariance 的 Trace 通常不是一个很好的总体不确定性指标？

**参考答案**

因为 Pose Covariance 混合了不同单位：

- Translation：$$\text{m}^2$$
- Rotation：$$\text{rad}^2$$

直接相加缺乏自然物理尺度。

同时 Trace 还忽略：

- 不确定方向；
- Cross-Covariance；
- 任务对 Translation 和 Rotation 的不同敏感性。

更合理的是根据具体任务，将 Pose Uncertainty 传播到目标量，或使用带统计意义的信息矩阵评价。


## 相关章节与来源

- 上一章：[坐标系约定与变换调试](transform-debugging.md)
- 下一篇：[机器人运动模型](robot-motion-models.md)
- 来源：本次新增的 Part III 课堂草稿，按实际课程内容整理。
