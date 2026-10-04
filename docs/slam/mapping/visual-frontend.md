---
title: Visual SLAM 前端
description: 怎样把图像变成可靠的对应关系与几何约束？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 40
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# Visual SLAM 前端

## 本章目标

怎样把图像变成可靠的对应关系与几何约束？

## 前置知识

[数据关联](../spatial/data-association.md)、[观测模型](../spatial/sensor-models.md)、[Gauge Freedom](gauge-freedom.md)。

## 定义与假设

针孔相机已标定；齐次像素与归一化坐标必须区分。投影点位于相机前方；匹配、光流和直接法分别依赖各自的几何、亮度与局部运动条件。

## 核心问题


## 前端职责与特征表示

### 1. 为什么需要 Front-end？

上一章我们已经看到，后端更喜欢处理这种东西：

$$
x_0 \leftrightarrow x_1
$$

$$
x_1 \leftrightarrow m_3
$$

也就是：

> Pose、Landmark 之间的几何约束。

可是 Camera 给我们的不是约束。

Camera 给的是：

$$
I(u,v)
$$

也就是一张像素图像。

比如：

```
Image t
████████████

Image t+1
████████████
```

后端并不知道：

> 图像里的哪个点对应哪个真实世界点？

也不知道：

> 两帧之间相机移动了多少？

所以中间必须有人负责把：

$$
Pixels
$$

变成：

Geometric Constraints

这就是：

Visual Front-end

### 2. Front-end 本质上在解决三个问题

视觉前端大体上一直在回答三件事情。

第一：

>  **我在图像里看到了什么可以跟踪的东西？**

第二：

>  **不同帧里的哪些 observation 属于同一个真实世界点？**

第三：

>  **根据这些对应关系，相机发生了什么运动？**

对应：

Feature Extraction Data Association Motion Estimation

所以可以先画成：

```
Image
  ↓
Extract useful visual information
  ↓
Find correspondence
  ↓
Reject wrong matches
  ↓
Estimate geometry / pose
  ↓
Produce constraint
```

### 3. Front-end 不等于 Feature Extraction

这是我希望你这一章最先纠正的一个常见认知。

很多人说：

> Visual SLAM 前端就是 ORB。

这不准确。 ORB 只是前端里的一个工具。

真正目标是：

建立可靠的跨帧几何关系 你可以不用 ORB。

可以用：

- SIFT
- FAST + BRIEF
- SuperPoint
- Optical Flow
- Direct Method

甚至神经网络做 correspondence。 只要最后能得到可靠约束，就完成了前端的目的。

### 4. Visual SLAM 前端主要有两大路线

经典地看，可以分成：

Feature-based

和：

Direct

中间还有：

Semi-direct 但先把前两种搞懂。

### 5. Feature-based Method

Feature-based 的逻辑：

```
Image
 ↓
Feature Point
 ↓
Descriptor / Track
 ↓
Matching
 ↓
Geometry
```

例如：

ORB-SLAM 就是非常典型的 feature-based SLAM。

### 6. 什么叫 Feature？

理想 feature 应该满足：

> 当相机稍微移动、旋转、亮度变化后，我还能认出它。

例如图像里的：

- 角点
- 纹理明显位置
- 边缘交汇处

比纯色墙面更适合。

假设图像中有：

```
────────
        │
        │
```

这个角点的位置通常比较容易精确确定。

### 7. 为什么角点好？

想象一条纯边缘：

```
────────────
```

如果点沿边缘方向移动：

```
←────────→
```

你很难判断它究竟在哪里。 因为附近图像长得几乎一样。

这就是经典：

Aperture Problem

但是角点：

```
────┐
    │
    │
```

在：

$$
x
$$

和：

$$
y
$$

两个方向都有明显变化。 所以位置更容易确定。

### 8. Detector 和 Descriptor 是两件事

这一点经常被混起来。

#### Detector

回答：

> 哪里值得取 feature？

例如：

- FAST
- Harris
- Shi-Tomasi

输出：

$$
(u_i,v_i)
$$

#### Descriptor

回答：

> 这个 feature 长什么样？

例如：

- SIFT descriptor
- BRIEF
- ORB descriptor

得到一个向量：

$$
d_i
$$

以后另一张图出现 feature：

$$
d_j
$$

我们比较：

$$
distance(d_i,d_j)
$$

判断是不是同一点。

### 9. ORB 是什么？

ORB 大致可以理解成：

$$
\boxed{ FAST\ detector + oriented\ BRIEF\ descriptor }
$$

它为什么在经典 SLAM 中很流行？

因为：

- 快
- descriptor 是二进制
- Hamming distance 计算便宜
- 有旋转处理
- 工程实现成熟

所以 ORB-SLAM 才选择它。

并不是说：

> ORB 是视觉 SLAM 唯一正确方案。

### 10. Matching 是什么？

假设 Frame A 里有：

$$
f_1,f_2,f_3,\dots
$$

Frame B 里有：

$$
g_1,g_2,g_3,\dots
$$

我们想知道：

$$
f_i \leftrightarrow g_j
$$

哪一对对应同一个 3D point。

如果有 descriptor：

$$
d(f_i),d(g_j)
$$

就可以比较距离。

例如 ORB 用：

Hamming Distance

距离越小：

> descriptor 越相似。

### 11. 但“长得像”不代表真的是同一点

这个问题特别重要。

例如办公室里有很多：

```
门
窗户
桌角
重复纹理
```

两个完全不同的位置可能 descriptor 很相似。

所以：

Appearance Match  ≠  Geometric Match 这也是为什么 SLAM 不能只靠 descriptor matching。

必须做：

Geometric Verification

### 12. Data Association 才是前端真正难的地方

还记得前几章我们讲：

Observation  →  Landmark? 这就是 Data Association。

视觉里更具体：

> Frame 20 的这个 feature，到底是不是 Frame 19 的那个 feature？

甚至：

> 是不是 Map 里已经存在的 Landmark 327？

如果关联正确：

$$
z_{20}\rightarrow m_{327}
$$

就形成有价值约束。

如果关联错误：

$$
z_{20}\rightarrow m_{51}
$$

那后端会收到一个假的 constraint。

所以：

Garbage in, Garbage out 后端优化再强，也救不了大量错误对应。

## 三类几何估计问题

### 13. Visual Front-end 最常遇到三类几何问题

这一部分特别重要。

你以后看到视觉定位代码，可以先判断它属于哪一种：

$$
\boxed{ 2D-2D }
$$

$$
\boxed{ 3D-2D }
$$

$$
\boxed{ 3D-3D }
$$

我们一个一个讲。

### 14. 第一类：2D-2D

假设：

Frame 1 中观察到：

$$
p_1=(u_1,v_1)
$$

Frame 2 中观察到同一个世界点：

$$
p_2=(u_2,v_2)
$$

但是我们还不知道这个点的 3D 坐标。

于是只有：

$$
2D \leftrightarrow 2D
$$

问题：

> 根据很多这样的点对应，能不能恢复两个 Camera 之间的相对运动？

答案是：

可以。

这就进入：

Essential Matrix

和：

Epipolar Geometry

### 15. 极线几何的直觉

一个 3D 点：

$$
P
$$

在第一张图中投影为：

$$
p_1
$$

现在相机移动后，它在第二张图中的位置并不是任意的。

它必须落在一条：

epipolar line 上。

所以：

$$
p_1
$$

会在第二张图产生一个搜索约束。

而不是：

> 整张图随便找。

### 16. Essential Matrix

对于归一化相机坐标：

$$
x_1
$$

和：

$$
x_2
$$

有：

$$
x_2^T E x_1 = 0
$$

其中：

$$
E=[t]_\times R
$$

这里：

$$
R
$$

是两个 Camera 的相对旋转，

$$
t
$$

是相对平移。

所以：

$$
\boxed{ 2D-2D\ correspondence \rightarrow E \rightarrow R,t }
$$

### 17. 但这里有一个问题

从 Essential Matrix 恢复的：

$$
t
$$

只能得到方向。

比如：

$$
t= \begin{bmatrix} 1\\0\\0 \end{bmatrix}
$$

但你不知道到底移动了：

$$
1m
$$

还是：

$$
10m
$$

所以 monocular 2D-2D：

Translation scale unknown 这和上一章的 monocular scale ambiguity 完全对应。

### 18. Fundamental Matrix

如果使用的是 pixel coordinate：

$$
p_1,p_2
$$

并且包含相机内参影响，那么：

$$
p_2^T Fp_1=0
$$

这里：

$$
F
$$

是 Fundamental Matrix。

与 Essential Matrix 的关系：

$$
E=K_2^TFK_1
$$

如果两相机内参相同可写得更简洁；一般情况左右相机内参分别进入。

简单理解：

$$
F
$$

作用于 pixel space。

$$
E
$$

作用于 normalized camera coordinate。

### 19. 2D-2D 什么时候特别常见？

最典型：

> Monocular SLAM 初始化。

因为刚开始：

- 没地图
- 没 3D point

只有两张图片。

那自然只能从：

$$
2D-2D
$$

开始。

先估计：

$$
R,t
$$

然后再 triangulate 3D landmarks。

### 20. Triangulation

假设两个 Camera Pose 已知：

```
Camera 1         Camera 2
   \                 /
    \               /
     \             /
         Point
```

同一个世界点分别对应：

$$
p_1,p_2
$$

那么两条射线理论上交于一个 3D point：

$$
P
$$

这个过程叫：

Triangulation 也就是三角化。

### 21. 为什么 baseline 很重要？

如果两个 camera 几乎没移动：

```
C1 C2
 \  \
  \  \
```

两条 ray 很接近。 那么交点位置非常不稳定。

一点点 pixel noise 就可能让：

$$
Z
$$

差非常大。

如果 baseline 较大：

```
C1                C2
 \                /
  \              /
       Point
```

几何条件会更好。

所以：

Parallax 是 triangulation 非常重要的东西。

### 22. 和你熟悉的 Stereo 连起来

Stereo 其实也是 triangulation。

左右相机 baseline 已知：

$$
b
$$

rectified stereo 中：

$$
d=u_L-u_R
$$

所以：

$$
Z=\frac{fb}{d}
$$

本质和普通多视图 triangulation 是同一件事情：

> 不同 viewpoint 的 observation 联合恢复 depth。

只不过 stereo 的 geometry 更固定、更简单。

### 23. 第二类：3D-2D

现在假设 Map 已经建立了一部分。

地图里 Landmark 已知：

$$
P_i^w
$$

当前 Camera 图像中找到它对应的 pixel：

$$
p_i
$$

那么：

$$
3D \leftrightarrow 2D
$$

问题就是：

> Camera Pose 是多少？

这就是：

$$
\boxed{PnP}
$$

Perspective-n-Point。

### 24. PnP 是 Visual SLAM Tracking 的核心之一

假设 Map 中有：

```
P1
P2
P3
P4
...
```

当前图像中匹配到：

```
p1
p2
p3
p4
...
```

希望求：

$$
T_{cw}
$$

满足：

$$
p_i \approx \pi(T_{cw}P_i^w)
$$

于是 residual：

$$
r_i = p_i-\pi(T_{cw}P_i^w)
$$

然后优化：

$$
T_{cw}^* = \arg\min_T \sum_i \|r_i\|^2
$$

这其实已经非常接近 Bundle Adjustment 了。

只不过当前主要优化：

Camera Pose 而 landmarks 暂时固定。

### 25. 这就是 Reprojection Error

你以后在 Visual SLAM 中会疯狂看到这个词：

Reprojection Error 什么意思？

一个已知 3D point：

$$
P
$$

通过当前估计 Pose 投到图像：

$$
\hat p = \pi(TP)
$$

实际 observation：

$$
p
$$

所以：

$$
r=p-\hat p
$$

画出来：

```
actual observation ●

                 × predicted projection
```

两者 pixel distance 就是 reprojection error。

### 26. 为什么 reprojection error 特别自然？

因为 Camera 真正测到的东西就是：

$$
Pixel
$$

不是：

$$
3D\ position
$$

所以直接在 measurement space 比较：

Observation - Prediction 非常自然。

这和我们 Part II 的统一框架完全一致：

$$
r=z-h(x)
$$

在视觉里：

$$
z=p
$$

$$
h(x)=\pi(TP)
$$

所以：

$$
r=p-\pi(TP)
$$

### 27. 第三类：3D-3D

假设两个 frame 都能得到 3D point。

比如：

- RGB-D
- Stereo
- LiDAR
- 已恢复 depth 的 feature

Frame A：

$$
P_i
$$

Frame B：

$$
Q_i
$$

而且知道 correspondence：

$$
P_i\leftrightarrow Q_i
$$

那么想求：

$$
R,t
$$

满足：

$$
Q_i\approx RP_i+t
$$

这就是：

$$
\boxed{ 3D-3D\ Registration }
$$

### 28. 3D-3D 如何求？

通常最小化：

$$
\sum_i \|Q_i-(RP_i+t)\|^2
$$

可以用：

- SVD
- ICP 中的 rigid alignment
- nonlinear optimization

所以：

$$
3D-3D
$$

本质是点云配准。

### 29. 三种问题整理一下

这个表值得记住：

|输入对应关系|典型问题|求什么|
|---|---|---|
|2D-2D|Epipolar Geometry|Relative Pose|
|3D-2D|PnP|Camera Pose|
|3D-3D|Registration / ICP|Rigid Transform|

以后看算法时，先判断：

它手里到底有什么 measurement？ 然后算法选择通常就很自然了。

### 30. Visual SLAM 运行起来后，最常见的是哪种？

初始化阶段：

$$
2D-2D
$$

很常见。

地图建立起来以后 Tracking：

$$
3D-2D
$$

非常常见。 因为已经有 MapPoint 了。

比如 ORB-SLAM 的一个典型思路就是：

```
MapPoint in world
        ↓
project into current image
        ↓
find corresponding feature
        ↓
PnP / pose optimization
```

## 跟踪、光流与直接法

### 31. Tracking 和 Matching 有什么区别？

Matching 往往更强调：

> 两个 observation 是否相同？

Tracking 更强调：

> 一个 feature 随时间去了哪里？

例如：

$$
p_t \rightarrow p_{t+1} \rightarrow p_{t+2}
$$

Optical Flow 就很适合做这种事情。

### 32. Optical Flow

假设某个 pixel neighborhood 在短时间内变化不大。

经典假设：

$$
I(x,y,t) = I(x+\Delta x,y+\Delta y,t+\Delta t)
$$

叫：

Brightness Constancy

意思：

> 同一个点在相邻帧中亮度大致不变。

于是可以估计它移动到哪里。

### 33. Lucas-Kanade Optical Flow

对于小运动：

$$
I_xu+I_yv+I_t=0
$$

其中：

$$
u,v
$$

是图像运动。

一个 pixel 只有一个 equation：

$$
I_xu+I_yv=-I_t
$$

但未知量有两个：

$$
u,v
$$

所以单 pixel 不够。

Lucas-Kanade 假设一个小 patch 内：

$$
u,v
$$

大致一致。 于是多个 pixel 联立求解。

### 34. Optical Flow 为什么在视觉前端常用？

因为相邻帧之间通常：

motion relatively small 所以不用在整张图重新做 descriptor matching。

可以直接从：

$$
p_t
$$

附近找：

$$
p_{t+1}
$$

计算成本较低。

所以很多 VIO / VO 系统会用：

KLT Optical Flow 来 track feature。

### 35. Feature Matching vs Optical Flow

可以粗略理解：

#### Descriptor Matching

更像：

> 我重新在两张图里找点，然后认身份。

适合：

- 间隔较大
- loop closure
- relocalization

#### Optical Flow

更像：

> 我知道上一帧这个点在哪，现在追踪它跑哪里去了。

适合：

- 连续相邻帧
- 小运动
- 高频 tracking

所以两者不是简单谁替代谁。 使用场景不一样。

### 36. 那 Direct Method 又是什么？

Feature Method 说：

> 我先挑一部分 feature。

Direct Method 说：

> 为什么一定要先提 feature？

我可以直接利用 pixel intensity。

例如一个 3D point 在参考帧：

$$
p_1
$$

根据当前 Pose 可以预测它在新帧位置：

$$
p_2
$$

那么可以比较：

$$
I_1(p_1)
$$

和：

$$
I_2(p_2)
$$

如果是同一个点，亮度应该接近。

于是 photometric residual：

$$
\boxed{ r=I_2(p_2)-I_1(p_1) }
$$

### 37. Direct Method 的 optimization

目标可能是：

$$
\min_T \sum_i \left[ I_2(\pi(TP_i))-I_1(p_i) \right]^2
$$

这里没有 descriptor。

直接通过：

Pixel Intensity

优化：

Camera Pose

所以叫：

$$
Direct
$$

### 38. Feature-based 和 Direct 最大区别

Feature-based：

Image  →  Feature  →  Correspondence  →  Geometry

Direct：

Image Intensity  →  Pose Optimization

前者 residual 常见：

Reprojection Error

后者 residual 常见：

Photometric Error

### 39. Direct Method 的优势

第一：

不需要显式 descriptor matching。

第二：

可以利用更多图像信息。 不是只有少量 corner。

第三：

在低纹理但仍有一定 intensity gradient 的地方，有时可以利用比 feature 方法更多的数据。

### 40. 但 Direct Method 的假设也更强

例如：

Brightness Constancy

要求：

> 同一个真实点在两帧看起来亮度差不多。

但现实中会有：

- Auto exposure
- 光照变化
- 阴影
- 镜面反射
- Motion blur

于是：

$$
I_1(p_1) \not\approx I_2(p_2)
$$

所以 direct method 对 photometric calibration 会更敏感。

### 41. Direct Method 对初始化也比较敏感

因为 optimization 通常是局部的。

如果初始 Pose 离真实位置太远：

$$
T_{init}
$$

可能落入错误 local minimum。

所以常常需要：

- image pyramid
- good motion initialization
- small inter-frame motion

### 42. Image Pyramid 为什么常用？

原图：

$$
640\times480
$$

缩小：

$$
320\times240
$$

再缩：

$$
160\times120
$$

先在低分辨率估大运动， 再逐层 refine。

逻辑：

```
coarse
 ↓
medium
 ↓
fine
```

大运动在低分辨率图里看起来会变成较小 pixel displacement。 所以更容易优化。

### 43. Semi-direct 是什么？

Semi-direct 就处于两者之间。

比如：

> 用 feature point 决定关注哪里，但不算 descriptor，而直接利用 patch intensity 做 tracking。

经典：

$$
SVO
$$

就是一种代表。 所以分类并不是绝对的。

## 异常匹配、动态场景与几何条件

### 44. 前端还有一个重要的任务：Outlier Rejection

实际 feature match 中一定有错误。

假设得到 100 个 matches：

```
90 correct
10 wrong
```

如果直接最小二乘：

$$
\min \sum_i \|r_i\|^2
$$

那 10 个错误点可能 residual 巨大。

因为平方项：

$$
r^2
$$

大 residual 会占非常大的 cost。 最终 Pose 可能被严重拉偏。

所以必须：

Reject Outliers

### 45. RANSAC

视觉几何里非常经典。 假设你有 100 个 correspondences。 其中很多正确，但也有一些错误。

RANSAC 做的事情大致是：

第一，随机抽最少数量的 points。 第二，用它们估一个模型。

例如：

$$
E
$$

或者：

PnP Pose 第三，用这个模型检查全部 points。

满足模型的叫：

$$
Inlier
$$

不满足的叫：

Outlier 第四，重复很多次。

最后选：

Inlier 最多的 model

### 46. RANSAC 的核心思想

它并不是想：

> 一次把所有数据都解释好。

而是：

> 我相信至少有一部分数据是对的，我先找到一个“正确的小团体”。

这和普通 least squares 思路很不同。

### 47. 一个具体例子

假设 100 个 feature matches：

$$
80
$$

个是真实对应，

$$
20
$$

个错。

如果直接求 Essential Matrix：

> 错误 correspondence 会破坏结果。

RANSAC 会不断随机采样。 只要某次抽到的 minimal sample 全部来自那 80 个正确点， 就有机会得到接近正确的模型。

然后：

$$
80
$$

个点都支持这个 model。 于是它胜出。

### 48. 但是 RANSAC 也不是万能的

如果错误 match 太多：

$$
90\%\ outliers
$$

随机抽到全正确 sample 的概率会很低。 而且 threshold 选择也很重要。

threshold 太小：

> 真 inlier 也被拒掉。

太大：

> outlier 也混进来。

所以它仍然需要合理 noise model。

### 49. Robust Kernel

除了直接删除 outlier，

后端/前端优化还常使用：

$$
Huber
$$

$$
Cauchy
$$

等 robust loss。

普通 least squares：

$$
\rho(r)=r^2
$$

大 residual 权重非常大。 Robust loss 会让大 residual 的增长变慢。

直觉：

> 小 residual 我相信。

> 大 residual 我开始怀疑它是不是 outlier。

### 50. 为什么既有 RANSAC 又有 Robust Kernel？

两者作用不同。

RANSAC：

> 在几何模型估计早期先大规模清除错误 association。

Robust Kernel：

> optimization 中对剩余异常 measurement 降权。

所以常见 pipeline：

```
descriptor / optical-flow matching
        ↓
RANSAC geometric verification
        ↓
pose optimization
        ↓
robust loss
```

是很合理的。

### 51. 一个真实 Visual Front-end Pipeline

比如单目 feature-based VO：

```
Frame t
   ↓
Detect feature
   ↓
Track / match to Frame t+1
   ↓
RANSAC
   ↓
Essential Matrix
   ↓
Recover R, t
   ↓
Triangulate landmarks
```

如果地图已经存在：

```
Current Image
   ↓
Detect / Track features
   ↓
Match to MapPoints
   ↓
3D-2D correspondence
   ↓
PnP + RANSAC
   ↓
Pose Optimization
   ↓
Current Camera Pose
```

这已经很接近真正 ORB-SLAM 的 tracking 逻辑了。

### 52. Stereo Visual SLAM 有什么不同？

对于 stereo：

左图和右图提供：

disparity

于是某些 feature 可以直接恢复 metric 3D：

$$
P_i^c
$$

因此系统可以更快获得：

$$
3D
$$

信息。

不像 monocular：

> 必须依赖多帧 motion triangulation。

所以 stereo SLAM 初始化通常容易很多。

### 53. 和你当前做 Stereo 的一个连接

你现在熟悉的 stereo 网络主要在解决：

$$
left\ image + right\ image \rightarrow disparity
$$

这相当于非常 dense 地解决：

Correspondence

但这里 correspondence 是：

left  ↔  right

也就是：

Spatial correspondence

而 Visual SLAM 前端更多还需要：

$$
frame_t \leftrightarrow frame_{t+1}
$$

也就是：

Temporal correspondence

这两个方向可以统一看成：

> 找到同一个真实世界 point 在不同 observation 中的位置。

这个视角其实很有意思。

### 54. Stereo correspondence 和 SLAM correspondence 有什么本质差别？

Stereo：

```
Left     Right
  ●  ↔    ●
```

通常相机之间 geometry 已知：

$$
T_{LR}
$$

目标是恢复：

$$
Depth
$$

Temporal SLAM：

```
Frame t     Frame t+1
   ●    ↔      ●
```

这里对应关系帮你反过来估计：

$$
T_{t,t+1}
$$

所以：

Stereo：

Known Pose  →  Depth

Visual Odometry：

Correspondence  →  Pose 这两者其实是几何上的“互逆问题”。

### 55. Dynamic Object 会造成什么问题？

假设 Camera 自己没怎么动。

但图里一辆车：

```
car →→→
```

feature 跟着车移动。 如果 SLAM 把它当静态世界点，

它会解释成：

> “Camera 应该移动了。”

于是产生错误 Pose。

经典 SLAM 有一个很重要假设：

World is mostly static

### 56. 所以动态场景为什么麻烦？

因为 observation motion：

image motion

可以来自：

camera motion

也可以来自：

object motion 如果不能区分， 几何模型就被污染。

现代 SLAM 会加入：

- Semantic segmentation
- Motion consistency
- Optical flow consistency
- Multi-body motion estimation

去排除 dynamic points。

### 57. Feature 分布也非常重要

假设所有 feature 都集中在图像左上角：

```
••••
•••

```

虽然数量很多， 但对某些 pose direction 的约束可能很差。

相比之下：

```
•        •
    •
        •
 •
      •
```

feature 在图像上分布更均匀， 通常几何条件更好。

所以：

Feature Number  ≠  Information Strength 这和我们之前一直讲的信息强弱完全一致。

### 58. 1000 个点一定比 100 个点好吗？

不一定。

如果 1000 个点全来自：

```
一个很远的平面
```

而 100 个点：

- 深度丰富
- 分布均匀
- 有较大 parallax

后者可能提供更强 pose constraint。

所以工程上真正关心：

Geometry 而不是单纯 feature count。

### 59. 一个常见 degeneracy：纯旋转

前一章已经讲过。

纯旋转时：

$$
t\approx0
$$

没有 parallax。

所以：

Triangulation 很差。 但 Rotation 本身其实可以估得不错。

所以：

> “整个 SLAM 都不可用”

不准确。

更准确地说：

Rotation strongly observable

但：

$$
Depth / Translation
$$

信息很弱。

### 60. 另一个情况：远距离场景

假设 feature 在：

$$
100m
$$

之外。

相机平移：

$$
0.1m
$$

图像变化非常小。 所以 translation information 很弱。 但是 rotation 会在图像里产生明显整体运动。

因此：

Rotation

往往比：

Translation 更容易估。 这在 VO 里非常常见。

## 前后端接口与跟踪恢复

### 61. 前端的输出到底是什么？

这一点一定要搞清楚。 Front-end 最终不是一定输出一张图，也不是一定输出 feature。

对后端来说，真正有价值的是：

$$
\boxed{ Constraints + Associated Measurements }
$$

例如：

$$
T_{t,t+1}
$$

或者：

$$
z_{ij} = \text{Landmark }j\text{ observed in frame }i
$$

再附带：

uncertainty 然后交给 backend。

### 62. 所以前端和后端真正的接口是什么？

可以粗略想象成：

```
Front-end
   ↓
“Frame 12 和 Frame 13 之间大概是这个变换”

“Frame 13 看到了 MapPoint 27”

“这个 measurement 的可信度大概是这样”

   ↓
Back-end
```

Backend 不需要知道 ORB descriptor 长什么样。

它更关心：

measurement residual uncertainty

### 63. Front-end 本身也可以优化 Pose

这里别形成一个错误印象：

> 前端只负责 feature，后端才优化。

不是。 Front-end 也经常做局部 pose optimization。

比如：

$$
PnP
$$

之后继续最小化：

Reprojection Error 得到当前 frame 的精确 pose。

只不过这个 optimization 通常：

- 变量少
- 范围局部
- 强调实时

而 Backend：

- 优化更多历史状态
- 处理全局一致性

### 64. Tracking Lost 是怎么发生的？

现在你已经可以理解了。

如果某一帧：

- motion blur
- 太暗
- feature 太少
- feature distribution 太差
- dynamic objects 太多
- camera motion 太快

导致有效 correspondence：

$$
N_{inlier}
$$

太少，

那么：

$$
Pose
$$

无法可靠估计。

于是：

Tracking Lost

### 65. Lost 以后怎么办？

这就需要：

Relocalization

意思：

> 不再假设我知道自己上一帧在哪里，而是在已有地图里重新寻找“我在哪”。

这时 descriptor / place recognition 就非常重要。

因为需要：

Current Image 和很久以前的 Keyframe 做 association。 这和 loop closure 的技术会有很多重合。

### 66. Local Tracking 和 Loop Closure 的 Association 不一样

Local Tracking：

$$
Frame_t \leftrightarrow Frame_{t-1}
$$

有很强 prior：

> 两帧位置不会差太远。

所以 matching 比较容易。

Loop Closure：

$$
Frame_t \leftrightarrow Frame_{t-10000}
$$

没有这么强的 local prior。

可能：

- 光照变了
- viewpoint 变了
- 场景有变化

所以需要更强的 appearance recognition。 这就是为什么 loop closure 是另一个大模块。

### 67. 为什么 learned feature 越来越多？

传统 feature：

- ORB
- SIFT

依赖手工设计。

Learned feature：

- SuperPoint
- DISK
- ALIKED 等

希望学习：

> 什么样的点最稳定、最容易跨 viewpoint 匹配。

Learned matcher：

- SuperGlue
- LightGlue 等

则直接学习 correspondence。 但不管模型名字怎么换，

逻辑还是：

Observation  →  Correspondence  →  Geometry 所以底层 SLAM 思维并没变。

### 68. Deep Visual Odometry 呢？

还有另一条路线：

直接输入：

$$
I_t,I_{t+1}
$$

网络输出：

$$
T_{t,t+1}
$$

看起来：

```
Image Pair
 ↓
Neural Network
 ↓
Pose
```

似乎把 feature、matching、geometry 全藏进网络。

但从系统层面看，它仍然是在构造：

Relative Pose Constraint

所以你以后看任何新方法，都可以问：

> 它到底在给 SLAM graph 提供什么 measurement？

这个问题特别有用。

### 69. 为什么现代 SLAM 仍然离不开 Geometry？

即使 front-end 用 neural network，

最后如果要和：

- IMU
- Loop Closure
- Map
- GPS
- LiDAR

融合，

通常还是需要一个几何状态：

$$
Pose
$$

以及 measurement relation：

$$
r(x)
$$

所以 Geometry 依然是整个系统的公共语言。

### 70. 把整章压成一条主线

现在你可以这样理解 Visual Front-end：

$$
Image
$$

首先得到：

Visual Observation

然后解决：

Correspondence

接着通过：

$$
2D-2D
$$

或者：

$$
3D-2D
$$

或者：

$$
3D-3D
$$

得到：

$$
Pose / Landmark\ Constraint
$$

中间用：

$$
RANSAC
$$

等方法排除错误。

最后给 Backend：

Reliable Constraints

所以：

$$
\boxed{ Visual\ Front-end = 从像素中提取可靠几何信息 }
$$

### 71. 和上一章再接一次

Chapter 39 我们一直问：

Measurement 到底约束 State 的哪些方向？

Chapter 40 实际上就是：

>  **这些 measurement 是怎么从 Image 里制造出来的？**

比如：

$$
2D-2D
$$

提供 relative pose information。

$$
3D-2D
$$

提供 camera pose constraint。

Stereo：

disparity 提供 metric depth。

所以这两章实际上是一前一后的：

```
Chapter 40:
Measurement 怎么生成？

Chapter 39:
Measurement 能约束什么？
```

### 72. 本章最重要的七句话

第一：

Front-end 的目的不是提 Feature，而是生成可靠 Constraint

第二：

Data Association 是视觉前端核心问题

第三：

三种最重要的 geometry：

$$
\boxed{ 2D-2D,\quad3D-2D,\quad3D-3D }
$$

第四：

$$
\boxed{ 2D-2D \rightarrow Essential/Fundamental\ Matrix }
$$

第五：

$$
\boxed{ 3D-2D \rightarrow PnP }
$$

第六：

$$
\boxed{ 3D-3D \rightarrow Registration }
$$

第七：

Appearance similarity 必须经过 geometric verification

> 修订说明：一般内参情况下应写 E = K₂ᵀFK₁，草稿的 E = KᵀFK 只用于两相机内参相同。E 的相对变换采用 P₂ = RP₁ + t。校正后的双目深度 Z = fb/d 要求水平极线、已知 baseline 与非零视差。LK 光流的 u、v 表示像素运动，与相机投影中像素位置同名但语义不同。

## 思考题

### Q1：为什么已经有 descriptor matching 之后，还要 RANSAC？

**参考答案**

因为 descriptor 只说明：

appearance similar

不代表：

$$
same\ 3D\ point
$$

RANSAC 用统一几何模型检查：

> 这些 matches 是否可以被同一个 camera motion 解释。

所以：

Appearance  →  Geometry 是两层 verification。


### Q2：地图已经建立后，为什么 3D-2D 比 2D-2D 更适合 Tracking？

**参考答案**

因为已知：

$$
P_i^w
$$

之后，

可以直接通过：

$$
P_i^w\leftrightarrow p_i
$$

求当前：

$$
T_{cw}
$$

即 PnP。 而 2D-2D 只能得到相对 Pose，并且 monocular translation 还缺 scale。


### Q3：为什么纯旋转情况下 feature matching 可能很好，但 triangulation 很差？

**参考答案**

因为 feature correspondence 和 depth information 是两回事。

纯旋转时：

$$
2D\ correspondence
$$

仍然可以非常稳定。 所以 Rotation 可以估得很好。

但没有 translational baseline：

$$
Parallax\approx0
$$

所以 Depth 无法稳定恢复。


### Q4：为什么 500 个 feature 不一定比 100 个 feature 提供更多 Pose information？

<details>

<summary>参考答案</summary>

因为 information 不只取决于数量。

还取决于：

- spatial distribution
- depth distribution
- parallax
- sensor noise
- geometry

如果 500 个点都集中在一个退化区域，它们可能高度冗余。

</details>

### Q5：为什么 dynamic object 会破坏 classical visual odometry？

**参考答案**

因为经典 VO 默认：

Feature motion comes from Camera motion 但动态物体本身也在运动。

于是：

$$
Observed\ motion = Camera\ motion + Object\ motion
$$

如果不区分，就会把 object motion 错当成 camera motion。


### Q6：Feature Method 和 Direct Method 的 residual 分别通常是什么？

**参考答案**

Feature-based：

Reprojection Error

例如：

$$
r=p-\pi(TP)
$$

Direct：

Photometric Error

例如：

$$
r= I_2(\pi(TP))-I_1(p)
$$


### Q7：Stereo 和 Visual Odometry 中的 correspondence，可以怎么统一理解？

**参考答案**

Stereo：

Left ↔  Right

主要用于恢复：

$$
Depth
$$

Visual Odometry：

$$
Frame_t\leftrightarrow Frame_{t+1}
$$

主要用于恢复：

Camera Motion

但本质都是：

$$
\boxed{ 找到同一个 3D point 在不同 observation 中的对应位置 }
$$

只是一个利用已知相机关系求结构，一个利用观测结构反求相机关系。


## 相关章节与来源

- 上一章：[SLAM 可观测性与 Gauge Freedom](gauge-freedom.md)
- 下一篇：[关键帧与局部建图](keyframes-local-mapping.md)
- 来源：本次新增 Part IV Chapter 40 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
